#!/usr/bin/env bash
# =====================================================================
# launch_revision_queue.sh
#
# Reviewer-requested extra calculations for the DFT+U study of Pr- and
# Rb-substituted anatase TiO2 (Quantum ESPRESSO 7.5, PBE, PAW PSlibrary
# 1.0.0, HUBBARD ortho-atomic, Gamma-only 47/48-atom cells).
#
# Builds every pw.x / hp.x input from templates/ -- atomic positions are
# taken from the production relaxation outputs in $QE_HOME with the same
# extract_positions() logic as the U-sensitivity launcher -- and runs the
# jobs one after the other in priority order:
#
#   P1 (default)        job 1  cut-off convergence 55/70 Ry (+40 Ry refs, O2)
#                       job 2  pristine V_O SCF at 2x2x2
#                       job 3  smearing test on the odd-electron Pr cells
#                       job 4  D3(BJ) single points (Pr_perfect, Rb_perfect, O2)
#                       job 5  nosym symmetry-broken hole search (SCF)
#   P2 (RUN_P2=1)       job 6  nosym re-relaxation, ONLY if a job-5 SCF is
#                              lower than the production energy
#                       job 7  dual-U Pr_VO relaxation (+ dual-U O2 box)
#                       job 7b dual-U Rb_VO relaxation restart (only if
#                              DUALU_RBVO_OUT is set)
#                       job 8  tight (0.001 Ry/Bohr) relaxations
#   P3 (RUN_P3=1)       job 9  linear-response U, pw.x + hp.x (meant for HPC)
#
# A job whose .out already contains "JOB DONE" is skipped, so the script
# can be re-launched at any time without repeating finished work. An
# interrupted relaxation is restarted from the last complete geometry in
# its .out (the old file is kept as *.out.interrupted_<date>).
# Start and end times go to the log and to runs/queue_times.tsv.
#
# USAGE (from ~/tio2_vo/revision_calculations):
#   bash launch_revision_queue.sh --dry-run 2>&1 | tee dryrun.log
#   nohup bash launch_revision_queue.sh > revision.log 2>&1 & disown
#   RUN_P2=1 nohup bash launch_revision_queue.sh > revision_p2.log 2>&1 & disown
#
# Every setting in section 1 can be overridden from the environment, e.g.
#   PRISTINE_VO_OUT=Pristine_VO_v3.out nohup bash launch_revision_queue.sh ...
# =====================================================================

set -u
set -o pipefail

# ---------------------------------------------------------------------
# 1. SETTINGS -- check these before the first launch
# ---------------------------------------------------------------------
# Output of the PRISTINE oxygen-vacancy relaxation (name in $QE_HOME or an
# absolute path). THE NAME IS NOT KNOWN TO THIS SCRIPT -- SET IT.
PRISTINE_VO_OUT="${PRISTINE_VO_OUT:-Pristine_VO.out}"

# Output of the unfinished dual-U Rb_VO relaxation (job 7b). Name unknown;
# leave empty to skip job 7b.
DUALU_RBVO_OUT="${DUALU_RBVO_OUT:-}"
# Output of the finished dual-U Rb_perfect relaxation (optional; only used
# by the analysis to form the dual-U E_f(V_O; Rb)). Leave empty if unknown.
DUALU_RBP_OUT="${DUALU_RBP_OUT:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QE_HOME="${QE_HOME:-$HOME/tio2_vo}"             # production runs live here
PSEUDO_DIR="${PSEUDO_DIR:-$QE_HOME/pseudo}"
TEMPLATE_DIR="${TEMPLATE_DIR:-$SCRIPT_DIR/templates}"
WORK_DIR="${WORK_DIR:-$SCRIPT_DIR/runs}"        # generated .in and .out files
SCRATCH="${SCRATCH:-./scratch}"                 # pw.x outdir (relative to WORK_DIR)
NP="${NP:-4}"
MPIRUN="${MPIRUN:-mpirun}"
PW_BIN="${PW_BIN:-pw.x}"
HP_BIN="${HP_BIN:-hp.x}"
PW_FLAGS="${PW_FLAGS:-}"    # extra pw.x flags, e.g. "-nk 2" (spin pools: faster, ~2x memory)
HP_FLAGS="${HP_FLAGS:-}"

RUN_P1="${RUN_P1:-1}"
RUN_P2="${RUN_P2:-0}"
RUN_P3="${RUN_P3:-0}"
JOBS="${JOBS:-}"            # explicit list overriding RUN_P*, e.g. JOBS="2 3" or JOBS="7 7b 8"
DRY_RUN="${DRY_RUN:-0}"     # 1 = build inputs only (same as --dry-run)

# Smearing width (Ry) of all replicate runs. 0.005 is the production value
# as far as known; the launcher reads the width printed in every production
# output and refuses to start if it differs (override: ALLOW_DEGAUSS_MISMATCH=1).
DEGAUSS="${DEGAUSS:-0.005}"
ALLOW_DEGAUSS_MISMATCH="${ALLOW_DEGAUSS_MISMATCH:-0}"
# Job 2: the converged pristine V_O relaxation used 0.01 Ry (SI S1); the
# default keeps the study value so that the 2x2x2 E_f is comparable with
# the doped cells. JOB2_GAMMA_REF=1 adds a Gamma SCF at the same width.
JOB2_DEGAUSS="${JOB2_DEGAUSS:-$DEGAUSS}"
JOB2_GAMMA_REF="${JOB2_GAMMA_REF:-0}"

# Job 1 options
JOB1_CUTS="${JOB1_CUTS:-55 70}"                       # ecutwfc values (ecutrho = 8x)
JOB1_REF_CELLS="${JOB1_REF_CELLS:-Pr_perfect Pr_VO Rb_perfect Rb_VO}"  # 40 Ry refs ("" = none)
JOB1_O2="${JOB1_O2:-1}"                               # O2 box at 40 and every JOB1_CUTS value
# Job 7 option: dual-U O2 single point
JOB7_O2="${JOB7_O2:-1}"

# Production geometry sources (names in $QE_HOME or absolute paths)
SRC_Pr_perfect="${SRC_Pr_perfect:-Pr_perfect.out}"
SRC_Pr_VO="${SRC_Pr_VO:-Pr_VO.out}"
SRC_Rb_perfect="${SRC_Rb_perfect:-Rb_perfect.out}"
SRC_Rb_VO="${SRC_Rb_VO:-Rb_VO.out}"
SRC_Pristine_perfect="${SRC_Pristine_perfect:-Pristine_perfect.out}"   # job 0 (single-point output; positions only)
SRC_Pristine_VO="$PRISTINE_VO_OUT"
SRC_dualU_Rb_VO="$DUALU_RBVO_OUT"

# Starting magnetisation of the replicate runs (jobs 1-4, 7b, 8), as
# "Ti O dopant". "auto" = read the "Starting magnetic structure" block that
# pw.x printed in the production output (run log: 0 on all species).
MAG_Pr_perfect="${MAG_Pr_perfect:-auto}"
MAG_Pr_VO="${MAG_Pr_VO:-auto}"
MAG_Rb_perfect="${MAG_Rb_perfect:-auto}"
MAG_Rb_VO="${MAG_Rb_VO:-auto}"
MAG_Pristine_perfect="${MAG_Pristine_perfect:-auto}"
MAG_Pristine_VO="${MAG_Pristine_VO:-auto}"
MAG_dualU_Rb_VO="${MAG_dualU_Rb_VO:-auto}"
FALLBACK_MAG="0.0 0.0 0.0"           # used only if "auto" finds no block

# Job 5 seeds. Rb_VO: pw.x atom numbers of the oxygen relabelled O1 (tags: Oh<n>).
RBVO_OH_SEEDS="${RBVO_OH_SEEDS:-8 6}"
# Rb_perfect: empty = the oxygen with the shortest Rb-O bond, computed from
# the extracted production coordinates (python3); or set the atom number.
RB_PERFECT_OH_INDEX="${RB_PERFECT_OH_INDEX:-}"

# Job 6 trigger: production totals (Ry) and tolerance
E_PROD_Rb_VO="${E_PROD_Rb_VO:--4289.17135}"
E_PROD_Rb_perfect="${E_PROD_Rb_perfect:--4330.38890}"
P2_ETOL_RY="${P2_ETOL_RY:-1.0e-4}"   # job 6 runs if E(job 5) < E_prod - P2_ETOL_RY
# Continue relaxations that stopped at nstep (they print JOB DONE)
RESTART_MAXSTEP="${RESTART_MAXSTEP:-0}"

# ---------------------------------------------------------------------
# 2. Command line
# ---------------------------------------------------------------------
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=1 ;;
        -h|--help) sed -n '2,42p' "${BASH_SOURCE[0]}"; exit 0 ;;
        *) echo "Unknown argument: $arg (use --dry-run or --help)"; exit 2 ;;
    esac
done

# ---------------------------------------------------------------------
# 3. Constants
# ---------------------------------------------------------------------
UPF_LIST="Ti.pbe-spn-kjpaw_psl.1.0.0.UPF O.pbe-n-kjpaw_psl.1.0.0.UPF Pr.pbe-spdn-kjpaw_psl.1.0.0.UPF Rb.pbe-spn-kjpaw_psl.1.0.0.UPF"
SPECIES_Pr="  Pr  140.908  Pr.pbe-spdn-kjpaw_psl.1.0.0.UPF"
SPECIES_Rb="  Rb  85.468   Rb.pbe-spn-kjpaw_psl.1.0.0.UPF"
POSDIR="$WORK_DIR/_positions"
TIMES="$WORK_DIR/queue_times.tsv"
export OMP_NUM_THREADS=1             # 4 MPI ranks on 4 cores; no OpenMP threads

declare -A CELL_STATE CELL_UNITS CELL_MAGS
Q_TAG=(); Q_BIN=(); Q_KIND=()
N_RUN=0; N_SKIP=0; N_FAIL=0; N_BUILD_FAIL=0
RBP_OH=""

# ---------------------------------------------------------------------
# 4. Helpers
# ---------------------------------------------------------------------
log()    { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
die()    { log "FATAL: $*"; exit 1; }
hms()    { printf '%dh%02dm%02ds' $(($1 / 3600)) $(($1 % 3600 / 60)) $(($1 % 60)); }
fless()  { awk -v a="$1" -v b="$2" 'BEGIN { exit !((a + 0) < (b + 0)) }'; }
fequal() { awk -v a="$1" -v b="$2" -v t="$3" 'BEGIN { d = a - b; if (d < 0) d = -d; exit !(d <= t) }'; }
queue_add() { Q_TAG+=("$1"); Q_BIN+=("$2"); Q_KIND+=("$3"); }
selected()  { case " $SELECTED " in *" $1 "*) return 0 ;; esac; return 1; }

cell_nat()    { case "$1" in *_perfect) echo 48 ;; *) echo 47 ;; esac; }
cell_dopant() { case "$1" in Pr_*) echo Pr ;; Rb_*|dualU_Rb_*) echo Rb ;; *) echo "" ;; esac; }
cell_src() {
    local v="SRC_$1" f
    f="${!v}"
    [ -z "$f" ] && { echo ""; return; }
    case "$f" in /*) ;; *) f="$QE_HOME/$f" ;; esac
    echo "$f"
}
species_line() { case "$(cell_dopant "$1")" in Pr) echo "$SPECIES_Pr" ;; Rb) echo "$SPECIES_Rb" ;; esac; }
mag_kv() {   # key=value words for build_input from CELL_MAGS
    local a b c
    read -r a b c <<< "${CELL_MAGS[$1]}"
    echo "MAG_TI=$a MAG_O=$b MAG_DOP=${c:-0.0}"
}
final_energy() { grep '^!' "$1" | tail -1 | awk '{print $5}'; }
scf_ok() {
    [ -f "$1" ] && grep -q "JOB DONE" "$1" && ! grep -q "convergence NOT achieved" "$1" && grep -q '^!' "$1"
}

# --- extract the final ATOMIC_POSITIONS of a relax .out ----------------
# Same strategy as extract_positions() of launch_U_sensitivity_queue.sh:
#   1) the 'Begin final coordinates' block (relaxation finished cleanly)
#   2) otherwise the LAST complete ATOMIC_POSITIONS block (relaxation
#      stopped by hand or interrupted; a truncated last block is ignored)
# Writes the atom lines to $3; sets EXTRACT_UNITS and EXTRACT_STRATEGY.
extract_positions() {
    local OUTFILE="$1" NATOMS="$2" DEST="$3" TMP HDR
    TMP=$(mktemp)
    awk -v N="$NATOMS" '
        function flush() { if (n == N + 0) { bh = hdr; bn = n; for (i = 1; i <= n; i++) best[i] = line[i] } n = 0; cap = 0 }
        /Begin final coordinates/ { inb = 1; next }
        /End final coordinates/   { if (cap) flush(); inb = 0; next }
        inb && /^ATOMIC_POSITIONS/ { hdr = $0; cap = 1; n = 0; next }
        inb && cap {
            if (NF >= 4 && $1 ~ /^[A-Z][A-Za-z0-9_]*$/ && $2 ~ /^[-+.0-9]/) { line[++n] = $0 }
            else if (NF > 0) flush()
        }
        END { if (cap) flush(); if (bn == N + 0) { print bh; for (i = 1; i <= bn; i++) print best[i] } }
    ' "$OUTFILE" > "$TMP"
    EXTRACT_STRATEGY="'Begin final coordinates' block"
    if [ "$(wc -l < "$TMP")" -ne $((NATOMS + 1)) ]; then
        awk -v N="$NATOMS" '
            function flush() { if (n == N + 0) { bh = hdr; bn = n; for (i = 1; i <= n; i++) best[i] = line[i] } n = 0; cap = 0 }
            /^ATOMIC_POSITIONS/ { if (cap) flush(); hdr = $0; cap = 1; n = 0; next }
            cap {
                if (NF >= 4 && $1 ~ /^[A-Z][A-Za-z0-9_]*$/ && $2 ~ /^[-+.0-9]/) { line[++n] = $0; next }
                flush()
            }
            END { if (cap) flush(); if (bn == N + 0) { print bh; for (i = 1; i <= bn; i++) print best[i] } }
        ' "$OUTFILE" > "$TMP"
        EXTRACT_STRATEGY="last complete ATOMIC_POSITIONS block"
    fi
    if [ "$(wc -l < "$TMP")" -ne $((NATOMS + 1)) ]; then
        log "  ERROR: no complete block of $NATOMS atomic positions in $OUTFILE"
        rm -f "$TMP"
        return 1
    fi
    HDR=$(head -1 "$TMP")
    EXTRACT_UNITS=$(echo "$HDR" | tr -d '(){}' | awk '{print tolower($2)}')
    [ -z "$EXTRACT_UNITS" ] && EXTRACT_UNITS="alat"
    tail -n +2 "$TMP" > "$DEST"
    rm -f "$TMP"
    return 0
}

# --- replace the ATOMIC_POSITIONS block of an existing input ------------
replace_positions() {   # IN POSFILE NAT UNITS
    awk -v pf="$2" -v n="$3" -v u="$4" '
        /^ATOMIC_POSITIONS/ { print "ATOMIC_POSITIONS " u; while ((getline l < pf) > 0) print l; close(pf); skip = n + 0; next }
        skip > 0 { skip--; next }
        { print }
    ' "$1" > "$1.tmp" && mv "$1.tmp" "$1"
}

# --- starting magnetisation printed by pw.x in a production output ------
read_startmag() {   # $1 = .out, $2 = species label
    awk -v sp="$2" '
        /Starting magnetic structure/ { blk = 1; next }
        blk == 1 && /atomic species/  { blk = 2; next }
        blk == 2 { if (NF == 0) exit; if ($1 == sp) { print $2; exit } }
    ' "$1"
}

get_mags() {   # $1 cell key, $2 source .out, $3 dopant -> CELL_MAGS[$1], MAGSRC
    local CELL="$1" SRC="$2" DOP="$3" v="MAG_$1" SETTING VAL OUT="" I=0 SP
    SETTING="${!v:-auto}"
    if [ "$SETTING" != "auto" ]; then
        CELL_MAGS[$CELL]="$SETTING"; MAGSRC="set by MAG_$CELL"; return
    fi
    MAGSRC="read from production output"
    for SP in Ti O $DOP; do
        I=$((I + 1))
        VAL=$(read_startmag "$SRC" "$SP")
        if [ -z "$VAL" ]; then
            VAL=$(echo "$FALLBACK_MAG" | awk -v k="$I" '{print $k}')
            MAGSRC="FALLBACK $FALLBACK_MAG (no 'Starting magnetic structure' block found) -- check"
        fi
        OUT="$OUT $VAL"
    done
    CELL_MAGS[$CELL]="${OUT# }"
}

# --- cut-offs and smearing printed in a production output ---------------
DEGAUSS_MISMATCH=0
check_prod_params() {   # $1 = .out, $2 = 1 if the width must equal $3
    local F="$1" STRICT="$2" WANT="$3" EC ER W SN
    EC=$(awk '/kinetic-energy cutoff/ {print $(NF-1); exit}' "$F")
    ER=$(awk '/charge density cutoff/ {print $(NF-1); exit}' "$F")
    W=$(awk '/smearing, width \(Ry\)/ { s = $0; sub(/.*width \(Ry\)=[ ]*/, "", s); print s + 0; exit }' "$F")
    SN=$(grep -m1 -o '[A-Za-z-]* smearing, width' "$F" | awk '{print $1}')
    log "  production output: ecutwfc=${EC:-?} ecutrho=${ER:-?} Ry, smearing=${SN:-?}, width=${W:-?} Ry"
    if [ -n "$EC" ] && ! fequal "$EC" 40 1e-6; then log "  WARNING: production ecutwfc is $EC Ry, not 40"; fi
    if [ -n "$ER" ] && ! fequal "$ER" 320 1e-6; then log "  WARNING: production ecutrho is $ER Ry, not 320"; fi
    if [ -n "$W" ] && ! fequal "$W" "$WANT" 1e-6; then
        if [ "$STRICT" = 1 ]; then
            log "  WARNING: production smearing width $W Ry differs from DEGAUSS = $WANT Ry"
            DEGAUSS_MISMATCH=1
        else
            log "  NOTE: production smearing width $W Ry, this job uses $WANT Ry"
        fi
    fi
}

# --- positions, composition, settings and magnetisation of one cell -----
prepare_cell() {   # $1 = Pr_perfect | Pr_VO | Rb_perfect | Rb_VO | Pristine_VO | dualU_Rb_VO
    case "${CELL_STATE[$1]:-}" in ok) return 0 ;; bad) return 1 ;; esac
    CELL_STATE[$1]=bad
    _prepare_cell "$1" && return 0
    N_BUILD_FAIL=$((N_BUILD_FAIL + 1))
    return 1
}
_prepare_cell() {
    local CELL="$1" SRC NAT DOP NTI NO NDOP ETI EO EDOP WANT STRICT
    SRC=$(cell_src "$CELL"); NAT=$(cell_nat "$CELL"); DOP=$(cell_dopant "$CELL")
    log "Geometry of $CELL <- ${SRC:-<not set>}"
    if [ -z "$SRC" ] || [ ! -f "$SRC" ]; then
        log "  ERROR: source output not found; every job on $CELL is skipped."
        [ "$CELL" = Pristine_VO ] && log "  Set PRISTINE_VO_OUT (section 1 of this script) to the pristine V_O relaxation output."
        return 1
    fi
    extract_positions "$SRC" "$NAT" "$POSDIR/$CELL.pos" || return 1
    CELL_UNITS[$CELL]="$EXTRACT_UNITS"
    log "  $NAT atoms from the $EXTRACT_STRATEGY (units: $EXTRACT_UNITS)"
    case "$CELL" in
        Pristine_VO) ETI=16; EO=31; EDOP=0 ;;
        Pristine_perfect) ETI=16; EO=32; EDOP=0 ;;
        *_perfect)   ETI=15; EO=32; EDOP=1 ;;
        *)           ETI=15; EO=31; EDOP=1 ;;
    esac
    NTI=$(awk '$1 == "Ti"' "$POSDIR/$CELL.pos" | wc -l)
    NO=$(awk '$1 == "O"' "$POSDIR/$CELL.pos" | wc -l)
    NDOP=0
    [ -n "$DOP" ] && NDOP=$(awk -v d="$DOP" '$1 == d' "$POSDIR/$CELL.pos" | wc -l)
    if [ "$NTI" -ne "$ETI" ] || [ "$NO" -ne "$EO" ] || [ "$NDOP" -ne "$EDOP" ]; then
        log "  ERROR: composition Ti=$NTI O=$NO ${DOP:-dopant}=$NDOP, expected $ETI/$EO/$EDOP"
        return 1
    fi
    case "$CELL" in
        Pristine_VO) WANT="$JOB2_DEGAUSS"; STRICT=0 ;;
        *)           WANT="$DEGAUSS"; STRICT=1 ;;
    esac
    check_prod_params "$SRC" "$STRICT" "$WANT"
    get_mags "$CELL" "$SRC" "$DOP"
    log "  starting magnetisation (Ti O${DOP:+ $DOP}) = ${CELL_MAGS[$CELL]}  [$MAGSRC]"
    CELL_STATE[$CELL]=ok
    return 0
}

# --- build one input from a template ------------------------------------
# build_input TEMPLATE TAG POSFILE|- UNITS KEY=VALUE ...
build_input() {
    _build_input "$@" && return 0
    N_BUILD_FAIL=$((N_BUILD_FAIL + 1))
    return 1
}
_build_input() {
    local TPL="$TEMPLATE_DIR/$1" TAG="$2" POS="$3" UNITS="$4" KV
    shift 4
    local IN="$WORK_DIR/$TAG.in" OUT="$WORK_DIR/$TAG.out"
    if [ -f "$OUT" ] && [ -f "$IN" ] && grep -q "JOB DONE" "$OUT"; then
        log "  kept  $TAG.in (finished output exists)"
        return 0
    fi
    [ -f "$TPL" ] || { log "  ERROR: template $TPL not found"; return 1; }
    local ARGS=(-e "s|__PREFIX__|$TAG|g" -e "s|__OUTDIR__|$SCRATCH|g" -e "s|__PSEUDO_DIR__|$PSEUDO_DIR|g")
    for KV in "$@"; do ARGS+=(-e "s|__${KV%%=*}__|${KV#*=}|g"); done
    tr -d '\r' < "$TPL" | sed "${ARGS[@]}" > "$IN.partial" || { rm -f "$IN.partial"; return 1; }
    if [ "$POS" != "-" ]; then
        awk -v pf="$POS" '/__ATOMIC_POSITIONS__/ { while ((getline l < pf) > 0) print l; close(pf); next } { print }' \
            "$IN.partial" > "$IN.partial2" && mv "$IN.partial2" "$IN.partial"
        [ "$UNITS" = "angstrom" ] || sed -i "s|^ATOMIC_POSITIONS angstrom\$|ATOMIC_POSITIONS $UNITS|" "$IN.partial"
    fi
    if grep -n '__[A-Z_]*__' "$IN.partial"; then
        log "  ERROR: unfilled placeholder(s) in $TAG.in (lines above)"
        rm -f "$IN.partial"
        return 1
    fi
    mv "$IN.partial" "$IN"
    log "  built $TAG.in"
    return 0
}

# --- relabel one oxygen as O1 (output tags keep "Oh<n>") --------------------------------------------
make_oh_pos() {   # $1 cell, $2 atom number, $3 destination
    awk -v n="$2" 'NR == n { if ($1 != "O") bad = 1; else sub(/O/, "O1") } { print } END { exit bad }' \
        "$POSDIR/$1.pos" > "$3"
}

# --- oxygen with the shortest Rb-O bond (minimum image, orthorhombic cell)
nearest_o() {   # $1 positions file, $2 units, $3 dopant label -> atom number on stdout
    python3 - "$1" "$2" "$3" <<'PYEOF'
import math, sys
path, units, dop = sys.argv[1], sys.argv[2].lower(), sys.argv[3]
cell = (7.63632, 7.63632, 9.77900)          # production cell (angstrom), orthorhombic
factor = {"angstrom": 1.0, "bohr": 0.529177210903, "alat": 7.63632}
atoms = []
for line in open(path):
    f = line.split()
    if len(f) < 4:
        continue
    xyz = [float(v) for v in f[1:4]]
    if units == "crystal":
        xyz = [xyz[k] * cell[k] for k in range(3)]
    else:
        xyz = [v * factor[units] for v in xyz]
    atoms.append((f[0], xyz))
dops = [i for i, (s, _) in enumerate(atoms) if s == dop]
if len(dops) != 1:
    sys.exit("expected one %s atom, found %d" % (dop, len(dops)))
r0 = atoms[dops[0]][1]
def dist(a, b):
    d2 = 0.0
    for k in range(3):
        dx = a[k] - b[k]
        dx -= cell[k] * round(dx / cell[k])
        d2 += dx * dx
    return math.sqrt(d2)
near = sorted((dist(r0, xyz), i + 1) for i, (s, xyz) in enumerate(atoms) if s == "O")
sys.stderr.write("      %s is atom %d; its six nearest oxygens (atom, distance):\n" % (dop, dops[0] + 1))
for d, i in near[:6]:
    sys.stderr.write("        O%-3d %.4f A\n" % (i, d))
if near[1][0] - near[0][0] < 0.01:
    sys.stderr.write("      NOTE: the two shortest %s-O bonds differ by < 0.01 A; the first one is used.\n" % dop)
print(near[0][1])
PYEOF
}

rb_perfect_oh() {   # sets RBP_OH once
    [ -n "$RBP_OH" ] && return 0
    prepare_cell Rb_perfect || return 1
    if [ -n "$RB_PERFECT_OH_INDEX" ]; then
        RBP_OH="$RB_PERFECT_OH_INDEX"
        log "  Rb_perfect: Oh = atom $RBP_OH (set by RB_PERFECT_OH_INDEX)"
        return 0
    fi
    if ! command -v python3 > /dev/null 2>&1; then
        log "  ERROR: python3 not found; set RB_PERFECT_OH_INDEX by hand"
        return 1
    fi
    log "  Rb_perfect: Rb-O distances in the production geometry:"
    RBP_OH=$(nearest_o "$POSDIR/Rb_perfect.pos" "${CELL_UNITS[Rb_perfect]}" Rb) || { RBP_OH=""; log "  ERROR: nearest-oxygen search failed"; return 1; }
    log "  Rb_perfect: Oh = atom $RBP_OH (shortest Rb-O bond; override with RB_PERFECT_OH_INDEX)"
    return 0
}

# ---------------------------------------------------------------------
# 5. Job builders (the order of the calls below is the run order)
# ---------------------------------------------------------------------
build_job0() {
    log "--- job 0: relaxation of the pristine perfect cell (production value is an unrelaxed single point) ---"
    prepare_cell Pristine_perfect || return 0
    build_input job0_pristine_perfect_relax.in job0_Pristine_perfect_relax "$POSDIR/Pristine_perfect.pos" "${CELL_UNITS[Pristine_perfect]}" \
        DEGAUSS="$DEGAUSS" $(mag_kv Pristine_perfect) \
        && queue_add job0_Pristine_perfect_relax pw relax
}

build_job1() {
    log "--- job 1: cut-off convergence (40 Ry references, ${JOB1_CUTS// /, } Ry, O2 boxes) ---"
    local EC ER CELL CUTS="$JOB1_CUTS"
    if [ -n "$JOB1_REF_CELLS" ] || [ "$JOB1_O2" = 1 ]; then CUTS="40 $CUTS"; fi
    for EC in $CUTS; do
        ER=$((EC * 8))
        for CELL in Pr_perfect Pr_VO Rb_perfect Rb_VO; do
            if [ "$EC" = 40 ]; then case " $JOB1_REF_CELLS " in *" $CELL "*) ;; *) continue ;; esac; fi
            prepare_cell "$CELL" || continue
            build_input job1_cutoff_scf.in "job1_${CELL}_ec${EC}" "$POSDIR/$CELL.pos" "${CELL_UNITS[$CELL]}" \
                NAT="$(cell_nat "$CELL")" ECUTWFC="${EC}.0" ECUTRHO="${ER}.0" DEGAUSS="$DEGAUSS" \
                DOPANT_SPECIES="$(species_line "$CELL")" $(mag_kv "$CELL") \
                && queue_add "job1_${CELL}_ec${EC}" pw scf
        done
        if [ "$JOB1_O2" = 1 ]; then
            build_input job1_O2_box_cutoff.in "job1_O2_ec${EC}" - - \
                ECUTWFC="${EC}.0" ECUTRHO="${ER}.0" DEGAUSS="$DEGAUSS" \
                && queue_add "job1_O2_ec${EC}" pw relax
        fi
    done
}

build_job2() {
    log "--- job 2: pristine V_O cell at 2x2x2 k-points ---"
    prepare_cell Pristine_VO || return 0
    local DG="${JOB2_DEGAUSS/./p}"
    build_input job2_pristine_VO_k222.in job2_Pristine_VO_k222 "$POSDIR/Pristine_VO.pos" "${CELL_UNITS[Pristine_VO]}" \
        DEGAUSS="$JOB2_DEGAUSS" KPOINTS="2 2 2 0 0 0" $(mag_kv Pristine_VO) \
        && queue_add job2_Pristine_VO_k222 pw scf
    if [ "$JOB2_GAMMA_REF" = 1 ]; then
        build_input job2_pristine_VO_k222.in "job2_Pristine_VO_G_dg${DG}" "$POSDIR/Pristine_VO.pos" "${CELL_UNITS[Pristine_VO]}" \
            DEGAUSS="$JOB2_DEGAUSS" KPOINTS="1 1 1 0 0 0" $(mag_kv Pristine_VO) \
            && queue_add "job2_Pristine_VO_G_dg${DG}" pw scf
    fi
}

build_job3() {
    log "--- job 3: smearing test on the odd-electron Pr cells ---"
    local V SM DG LBL CELL
    for V in "gaussian 0.002 gauss0p002" "mv 0.005 mv0p005"; do
        read -r SM DG LBL <<< "$V"
        for CELL in Pr_perfect Pr_VO; do
            prepare_cell "$CELL" || continue
            build_input job3_smearing_scf.in "job3_${CELL}_${LBL}" "$POSDIR/$CELL.pos" "${CELL_UNITS[$CELL]}" \
                NAT="$(cell_nat "$CELL")" SMEARING="$SM" DEGAUSS="$DG" $(mag_kv "$CELL") \
                && queue_add "job3_${CELL}_${LBL}" pw scf
        done
    done
}

build_job4() {
    log "--- job 4: D3(BJ) single points (Pr_perfect, Rb_perfect, O2) ---"
    local CELL
    for CELL in Pr_perfect Rb_perfect; do
        prepare_cell "$CELL" || continue
        build_input job4_d3_scf.in "job4_${CELL}_D3" "$POSDIR/$CELL.pos" "${CELL_UNITS[$CELL]}" \
            NAT="$(cell_nat "$CELL")" DEGAUSS="$DEGAUSS" DOPANT_SPECIES="$(species_line "$CELL")" $(mag_kv "$CELL") \
            && queue_add "job4_${CELL}_D3" pw scf
    done
    build_input job4_O2_box_d3.in job4_O2_D3 - - DEGAUSS="$DEGAUSS" && queue_add job4_O2_D3 pw relax
}

# shared by jobs 5 and 6: $1 = template, $2 = tag suffix ("" or "_relax"), $3 = 1 to queue
build_nosym_set() {
    local TPL="$1" SUF="$2" QUEUE="$3" S TAG A3 PFX
    case "$TPL" in job5*) PFX=job5 ;; *) PFX=job6 ;; esac
    if prepare_cell Rb_VO; then
        A3=$(awk 'NR == 3 {print $1}' "$POSDIR/Rb_VO.pos")
        [ "$A3" = Rb ] || log "  WARNING: atom 3 of Rb_VO is '$A3', not Rb; the seed numbers in RBVO_OH_SEEDS follow the pw.x numbering of the brief -- check them."
        for S in $RBVO_OH_SEEDS; do
            TAG="${PFX}_Rb_VO_nosym_Oh${S}${SUF}"
            if make_oh_pos Rb_VO "$S" "$POSDIR/$TAG.pos"; then
                build_input "$TPL" "$TAG" "$POSDIR/$TAG.pos" "${CELL_UNITS[Rb_VO]}" \
                    NAT=47 DEGAUSS="$DEGAUSS" DOPANT_SPECIES="$SPECIES_Rb" \
                    && { [ "$QUEUE" = 1 ] && queue_add "$TAG" pw scf; }
            else
                log "  ERROR: atom $S of Rb_VO is not an oxygen; $TAG skipped"; N_BUILD_FAIL=$((N_BUILD_FAIL + 1))
            fi
        done
    fi
    if rb_perfect_oh; then
        TAG="${PFX}_Rb_perfect_nosym_Oh${RBP_OH}${SUF}"
        if make_oh_pos Rb_perfect "$RBP_OH" "$POSDIR/$TAG.pos"; then
            build_input "$TPL" "$TAG" "$POSDIR/$TAG.pos" "${CELL_UNITS[Rb_perfect]}" \
                NAT=48 DEGAUSS="$DEGAUSS" DOPANT_SPECIES="$SPECIES_Rb" \
                && { [ "$QUEUE" = 1 ] && queue_add "$TAG" pw scf; }
        else
            log "  ERROR: atom $RBP_OH of Rb_perfect is not an oxygen; $TAG skipped"; N_BUILD_FAIL=$((N_BUILD_FAIL + 1))
        fi
    fi
}

build_job5() {
    log "--- job 5: symmetry-broken hole search (nosym, Oh seed, SCF) ---"
    build_nosym_set job5_nosym_hole_scf.in "" 1
}

build_job6() {
    log "--- job 6: nosym re-relaxations (run only if a job-5 SCF is below production) ---"
    build_nosym_set job6_nosym_hole_relax.in "_relax" 0
    queue_add DECIDE_JOB6 - decide6
}

build_job7() {
    log "--- job 7: dual-U Pr_VO relaxation (+ dual-U O2 box) ---"
    if [ "$JOB7_O2" = 1 ]; then
        build_input job7_O2_box_dualU.in job7_O2_dualU - - DEGAUSS="$DEGAUSS" && queue_add job7_O2_dualU pw scf
    fi
    prepare_cell Pr_VO || return 0
    build_input job7_dualU_PrVO_relax.in job7_Pr_VO_dualU_relax "$POSDIR/Pr_VO.pos" "${CELL_UNITS[Pr_VO]}" \
        DEGAUSS="$DEGAUSS" && queue_add job7_Pr_VO_dualU_relax pw relax
}

build_job7b() {
    log "--- job 7b: dual-U Rb_VO relaxation, restart from its last geometry ---"
    if [ -z "$DUALU_RBVO_OUT" ]; then
        log "  DUALU_RBVO_OUT is not set -- job 7b skipped (optional)."
        return 0
    fi
    prepare_cell dualU_Rb_VO || return 0
    if grep -q "bfgs converged" "$(cell_src dualU_Rb_VO)"; then
        log "  NOTE: $(cell_src dualU_Rb_VO) already reports 'bfgs converged'; job 7b only confirms it (JOBS can drop 7b)."
    fi
    build_input job7b_dualU_RbVO_relax.in job7b_Rb_VO_dualU_relax "$POSDIR/dualU_Rb_VO.pos" "${CELL_UNITS[dualU_Rb_VO]}" \
        DEGAUSS="$DEGAUSS" $(mag_kv dualU_Rb_VO) && queue_add job7b_Rb_VO_dualU_relax pw relax
}

build_job8() {
    log "--- job 8: tight relaxations (forc_conv_thr 0.001 Ry/Bohr) ---"
    local CELL
    for CELL in Pr_VO Rb_VO Pr_perfect Rb_perfect; do
        prepare_cell "$CELL" || continue
        build_input job8_tight_relax.in "job8_${CELL}_tight" "$POSDIR/$CELL.pos" "${CELL_UNITS[$CELL]}" \
            NAT="$(cell_nat "$CELL")" DEGAUSS="$DEGAUSS" DOPANT_SPECIES="$(species_line "$CELL")" $(mag_kv "$CELL") \
            && queue_add "job8_${CELL}_tight" pw relax
    done
}

build_job9() {
    log "--- job 9: linear-response U, 12-atom anatase (pw.x then hp.x) ---"
    build_input job9_anatase_lr_scf.in job9_anatase_lr_scf - - DEGAUSS="$DEGAUSS" \
        && queue_add job9_anatase_lr_scf pw scf
    build_input job9_anatase_hp.in job9_anatase_hp - - && queue_add job9_anatase_hp hp hp
}

# ---------------------------------------------------------------------
# 6. Running
# ---------------------------------------------------------------------
job_status() {   # $1 = .out, $2 = kind
    if ! grep -q "JOB DONE" "$1"; then echo "CRASHED_OR_KILLED"; return; fi
    if grep -q "convergence NOT achieved" "$1"; then echo "SCF_NOT_CONVERGED"; return; fi
    if [ "$2" = relax ]; then
        if grep -q "bfgs converged" "$1"; then echo "RELAX_CONVERGED"
        elif grep -q "maximum number of steps" "$1"; then echo "RELAX_STOPPED_AT_NSTEP"
        else echo "RELAX_UNCLEAR"; fi
        return
    fi
    echo "OK"
}

summarize() {   # one-line result summary
    local F="$1" E TS EF M MA
    E=$(final_energy "$F")
    TS=$(grep 'smearing contrib. (-TS)' "$F" | tail -1 | awk '{print $(NF-1)}')
    EF=$(grep -E 'the Fermi energy is|Fermi energies are' "$F" | tail -1 \
         | awk '{for (i = 1; i <= NF; i++) if ($i ~ /^-?[0-9]+\.[0-9]+$/) printf "%s ", $i}')
    M=$(grep 'total magnetization' "$F" | tail -1 | awk -F= '{print $2}' | awk '{print $1}')
    MA=$(grep 'absolute magnetization' "$F" | tail -1 | awk -F= '{print $2}' | awk '{print $1}')
    log "       E_tot = ${E:-n.a.} Ry | -TS = ${TS:-n.a.} Ry | E_F = ${EF:-n.a. }eV | m = ${M:-n.a.} | m_abs = ${MA:-n.a.}"
    if grep -q "Program HP" "$F"; then
        grep -A 12 "Hubbard U parameters" "$F" | sed 's/^/       /'
    fi
}

pre_run_hook() {   # job-specific adjustments right before a run
    case "$1" in
        job7_O2_dualU)
            # use the relaxed O2 geometry of the job-1 40 Ry PBE box when available
            if [ -f job1_O2_ec40.out ] && grep -q "JOB DONE" job1_O2_ec40.out \
               && extract_positions job1_O2_ec40.out 2 "$POSDIR/O2_relaxed.pos"; then
                replace_positions "$1.in" "$POSDIR/O2_relaxed.pos" 2 "$EXTRACT_UNITS"
                log "NOTE   $1: O2 geometry taken from job1_O2_ec40.out"
            else
                log "NOTE   $1: job1_O2_ec40 not finished; using d(O-O) = 1.23 A from the template"
            fi ;;
    esac
}

run_job() {   # $1 tag, $2 pw|hp, $3 scf|relax|hp
    local TAG="$1" BIN="$2" KIND="$3" IN="$1.in" OUT="$1.out" OLD NAT T0 T1 RC ST BINARY FLAGS
    if [ -f "$OUT" ] && grep -q "JOB DONE" "$OUT"; then
        if [ "$KIND" = relax ] && [ "$RESTART_MAXSTEP" = 1 ] && grep -q "maximum number of steps" "$OUT"; then
            log "NOTE   $TAG stopped at nstep; continuing it (RESTART_MAXSTEP=1)"
        else
            log "SKIP   $TAG (output already contains JOB DONE)"
            N_SKIP=$((N_SKIP + 1)); return 0
        fi
    fi
    if [ ! -f "$IN" ]; then
        log "SKIP   $TAG (input was not built; see messages above)"
        return 1
    fi
    if [ "$KIND" = hp ] && ! scf_ok job9_anatase_lr_scf.out; then
        if [ "$DRY_RUN" = 1 ]; then log "DRY    $TAG (needs job9_anatase_lr_scf first)"; return 0; fi
        log "SKIP   $TAG (job9_anatase_lr_scf has not finished cleanly)"
        N_FAIL=$((N_FAIL + 1)); return 1
    fi
    if [ "$BIN" = hp ]; then BINARY="$HP_BIN"; FLAGS="$HP_FLAGS"; else BINARY="$PW_BIN"; FLAGS="$PW_FLAGS"; fi
    if [ "$DRY_RUN" = 1 ]; then
        log "DRY    $TAG  would run: $MPIRUN -np $NP $BINARY $FLAGS -in $IN > $OUT"
        return 0
    fi
    if [ -f "$OUT" ]; then
        OLD="$OUT.interrupted_$(date +%Y%m%d_%H%M%S)"
        mv "$OUT" "$OLD"
        log "NOTE   $TAG: previous incomplete output kept as $OLD"
        if [ "$KIND" = relax ]; then
            NAT=$(awk -F= '/^[[:space:]]*nat[[:space:]]*=/ { gsub(/[ ,]/, "", $2); print $2; exit }' "$IN")
            if extract_positions "$OLD" "$NAT" "$POSDIR/restart_$TAG.pos"; then
                replace_positions "$IN" "$POSDIR/restart_$TAG.pos" "$NAT" "$EXTRACT_UNITS"
                log "NOTE   $TAG: restarting from the $EXTRACT_STRATEGY of the interrupted run"
            else
                log "NOTE   $TAG: no complete geometry in the interrupted run; starting from the original geometry"
            fi
        fi
    fi
    pre_run_hook "$TAG"
    T0=$(date +%s)
    log "START  $TAG"
    # shellcheck disable=SC2086
    $MPIRUN -np "$NP" "$BINARY" $FLAGS -in "$IN" > "$OUT" 2>&1
    RC=$?
    T1=$(date +%s)
    ST=$(job_status "$OUT" "$KIND")
    log "END    $TAG  status=$ST  exit=$RC  elapsed=$(hms $((T1 - T0)))"
    printf '%s\t%s\t%s\t%s\t%s\n' "$TAG" "$(date -d "@$T0" '+%F %T')" "$(date -d "@$T1" '+%F %T')" \
        "$((T1 - T0))" "$ST" >> "$TIMES"
    summarize "$OUT"
    N_RUN=$((N_RUN + 1))
    case "$ST" in OK|RELAX_CONVERGED) return 0 ;; esac
    log "       tail of $OUT:"; tail -15 "$OUT" | sed 's/^/       | /'
    N_FAIL=$((N_FAIL + 1))
    return 1
}

decide_job6() {
    log "--- job 6 decision (production: Rb_VO $E_PROD_Rb_VO Ry, Rb_perfect $E_PROD_Rb_perfect Ry; tolerance $P2_ETOL_RY Ry) ---"
    local S T O E BEST_T="" BEST_E="" LIM
    for S in $RBVO_OH_SEEDS; do
        T="job5_Rb_VO_nosym_Oh${S}"; O="$T.out"
        if ! scf_ok "$O"; then log "job 6: $T has no converged result; not considered"; continue; fi
        E=$(final_energy "$O")
        log "job 6: $T  E = $E Ry"
        if [ -z "$BEST_E" ] || fless "$E" "$BEST_E"; then BEST_E="$E"; BEST_T="$T"; fi
    done
    LIM=$(awk -v p="$E_PROD_Rb_VO" -v t="$P2_ETOL_RY" 'BEGIN { printf "%.8f", p - t }')
    if [ -n "$BEST_T" ] && fless "$BEST_E" "$LIM"; then
        log "job 6: $BEST_T is below production by more than $P2_ETOL_RY Ry -> re-relaxing it without symmetry"
        run_job "${BEST_T/job5_/job6_}_relax" pw relax
    else
        log "job 6: no Rb_VO nosym state below $LIM Ry -> no Rb_VO re-relaxation"
    fi
    if [ -n "$RBP_OH" ]; then
        T="job5_Rb_perfect_nosym_Oh${RBP_OH}"; O="$T.out"
        if scf_ok "$O"; then
            E=$(final_energy "$O")
            LIM=$(awk -v p="$E_PROD_Rb_perfect" -v t="$P2_ETOL_RY" 'BEGIN { printf "%.8f", p - t }')
            log "job 6: $T  E = $E Ry"
            if fless "$E" "$LIM"; then
                log "job 6: $T is below production by more than $P2_ETOL_RY Ry -> re-relaxing it without symmetry"
                run_job "job6_Rb_perfect_nosym_Oh${RBP_OH}_relax" pw relax
            else
                log "job 6: Rb_perfect nosym state not below $LIM Ry -> no Rb_perfect re-relaxation"
            fi
        else
            log "job 6: $T has no converged result; not considered"
        fi
    fi
}

# ---------------------------------------------------------------------
# 7. Main
# ---------------------------------------------------------------------
if [ -n "$JOBS" ]; then
    SELECTED="$JOBS"
else
    SELECTED=""
    [ "$RUN_P1" = 1 ] && SELECTED="1 2 0 3 4 5"
    [ "$RUN_P2" = 1 ] && SELECTED="$SELECTED 6 7 7b 8"
    [ "$RUN_P3" = 1 ] && SELECTED="$SELECTED 9"
fi

mkdir -p "$WORK_DIR" "$POSDIR" || die "cannot create $WORK_DIR"
cd "$WORK_DIR" || die "cannot cd to $WORK_DIR"
[ -f "$TIMES" ] || printf 'tag\tstart\tend\tseconds\tstatus\n' > "$TIMES"

if command -v flock > /dev/null 2>&1; then
    exec 9> "$WORK_DIR/.launcher.lock"
    flock -n 9 || die "another launch_revision_queue.sh is already using $WORK_DIR"
fi

echo "============================================================"
log "REVISION QUEUE $( [ "$DRY_RUN" = 1 ] && echo '(DRY RUN: inputs only)')"
echo "    QE_HOME        = $QE_HOME"
echo "    PSEUDO_DIR     = $PSEUDO_DIR"
echo "    TEMPLATE_DIR   = $TEMPLATE_DIR"
echo "    WORK_DIR       = $WORK_DIR   (pw.x outdir: $SCRATCH)"
echo "    PRISTINE_VO_OUT= $PRISTINE_VO_OUT"
echo "    DUALU_RBVO_OUT = ${DUALU_RBVO_OUT:-<not set>}"
echo "    jobs selected  = $SELECTED"
echo "    DEGAUSS        = $DEGAUSS Ry (job 2: $JOB2_DEGAUSS Ry)"
echo "    command        = $MPIRUN -np $NP $PW_BIN $PW_FLAGS -in <tag>.in"
echo "============================================================"

# --- pre-flight -------------------------------------------------------
if [ "$DRY_RUN" != 1 ]; then
    command -v "$PW_BIN" > /dev/null 2>&1 || die "$PW_BIN not found on PATH"
    command -v "$MPIRUN" > /dev/null 2>&1 || die "$MPIRUN not found on PATH"
    if selected 9 && ! command -v "$HP_BIN" > /dev/null 2>&1; then log "WARNING: $HP_BIN not found; job9_anatase_hp will fail"; fi
    if pgrep -x 'pw\.x|hp\.x|projwfc\.x' > /dev/null 2>&1; then
        pgrep -a -x 'pw\.x|hp\.x|projwfc\.x'
        die "pw.x, hp.x or projwfc.x is already running -- wait for it to finish (4 cores only)"
    fi
fi
for ps in $UPF_LIST; do
    if [ ! -f "$PSEUDO_DIR/$ps" ]; then
        [ "$DRY_RUN" = 1 ] && log "WARNING: pseudopotential not found: $PSEUDO_DIR/$ps" || die "pseudopotential not found: $PSEUDO_DIR/$ps"
    fi
done
FREE_GB=$(df -Pk "$WORK_DIR" | awk 'NR == 2 {print int($4 / 1048576)}')
log "free disk in $WORK_DIR: ${FREE_GB} GB; memory: $(free -g 2> /dev/null | awk '/Mem:/ {print $2 " GB total, " $7 " GB available"}')"
[ "${FREE_GB:-0}" -lt 15 ] && log "WARNING: less than 15 GB free; see README (disk)"

# --- phase A: build every input --------------------------------------
log "PHASE A: building inputs"
for J in 1 2 0 3 4 5 6 7 7b 8 9; do
    selected "$J" && "build_job$J"
done
if [ "$DEGAUSS_MISMATCH" = 1 ]; then
    if [ "$ALLOW_DEGAUSS_MISMATCH" = 1 ]; then
        log "WARNING: production smearing width differs from DEGAUSS=$DEGAUSS (allowed by ALLOW_DEGAUSS_MISMATCH=1)"
    elif [ "$DRY_RUN" = 1 ]; then
        log "WARNING: production smearing width differs from DEGAUSS=$DEGAUSS -- a real launch will stop here."
        log "         Re-run with DEGAUSS=<production width> (preferred) or ALLOW_DEGAUSS_MISMATCH=1."
    else
        die "production smearing width differs from DEGAUSS=$DEGAUSS; re-run with DEGAUSS=<production width> or ALLOW_DEGAUSS_MISMATCH=1"
    fi
fi
log "Queue (${#Q_TAG[@]} entries, in run order):"
for i in "${!Q_TAG[@]}"; do echo "      $((i + 1)). ${Q_TAG[$i]}"; done

# --- phase B: run ------------------------------------------------------
log "PHASE B: $( [ "$DRY_RUN" = 1 ] && echo 'dry run, nothing is executed' || echo 'running')"
for i in "${!Q_TAG[@]}"; do
    if [ "${Q_KIND[$i]}" = decide6 ]; then
        if [ "$DRY_RUN" = 1 ]; then log "DRY    job 6 decision (needs the job-5 outputs)"; else decide_job6; fi
    else
        run_job "${Q_TAG[$i]}" "${Q_BIN[$i]}" "${Q_KIND[$i]}"
    fi
done

echo "============================================================"
log "QUEUE FINISHED: $N_RUN run, $N_SKIP skipped (already done), $N_FAIL failed"
[ "$N_BUILD_FAIL" -gt 0 ] && log "WARNING: $N_BUILD_FAIL input(s) or geometries could not be prepared -- see the ERROR lines of PHASE A"
echo "    wall times: $TIMES"
if [ "$DRY_RUN" != 1 ] && command -v python3 > /dev/null 2>&1; then
    ANA_ARGS=("$WORK_DIR" --prod-dir "$QE_HOME" --pristine-vo-out "$(cell_src Pristine_VO)")
    [ -n "$DUALU_RBP_OUT" ] && ANA_ARGS+=(--dualu-rb-perfect "$(case "$DUALU_RBP_OUT" in /*) echo "$DUALU_RBP_OUT" ;; *) echo "$QE_HOME/$DUALU_RBP_OUT" ;; esac)")
    ANA_OUT="$(dirname "$WORK_DIR")/revision_analysis.txt"
    if python3 "$SCRIPT_DIR/analyze_revision_runs.py" "${ANA_ARGS[@]}" > "$ANA_OUT" 2>&1; then
        log "analysis written to $ANA_OUT"
    else
        log "analysis script reported a problem; see $ANA_OUT"
    fi
fi
echo "    next: python3 $SCRIPT_DIR/analyze_revision_runs.py $WORK_DIR | tee revision_analysis.txt"
echo "============================================================"
[ "$N_FAIL" -eq 0 ] && [ "$N_BUILD_FAIL" -eq 0 ]
