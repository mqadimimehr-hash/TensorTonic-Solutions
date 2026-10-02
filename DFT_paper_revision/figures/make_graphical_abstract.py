import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
S1,S2,S3,INK,INK2,GRID="#2a78d6","#eb6834","#1baf7a","#0b0b0b","#52514e","#d9d8d4"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9})
fig=plt.figure(figsize=(13/2.54,5/2.54),dpi=300)
ax=fig.add_axes([0.09,0.2,0.42,0.62])
vals=[4.74,1.29,-4.06]; labs=["pristine","Pr$_{\\mathrm{Ti}}$","Rb$_{\\mathrm{Ti}}$"]
b=ax.bar(range(3),vals,color=[S1,S2,S3],width=0.6,zorder=3)
ax.axhline(0,color=INK2,lw=0.7); ax.set_xticks(range(3)); ax.set_xticklabels(labs,fontsize=8)
ax.set_ylabel("$E_{\\mathrm{f}}(V_{\\mathrm{O}}^{0})$ (eV)",fontsize=8); ax.set_ylim(-5.2,5.8)
ax.yaxis.grid(True,color=GRID,lw=0.5,zorder=0); ax.set_axisbelow(True)
for s in ["top","right"]: ax.spines[s].set_visible(False)
for bar,v in zip(b,vals):
    ax.text(bar.get_x()+bar.get_width()/2, v+(0.25 if v>0 else -0.25), f"{v:+.2f}", ha="center", va="bottom" if v>0 else "top", fontsize=7.5, fontweight="bold")
ax.set_title("Anatase TiO$_2$, PBE+U, $\\mu_\\mathrm{O}=\\frac{1}{2}E(\\mathrm{O}_2)$",fontsize=7.5,color=INK2)
fig.text(0.56,0.80,"Oxygen vacancies in Pr- and\nRb-substituted anatase TiO$_2$",fontsize=8,fontweight="bold",color=INK,va="top",linespacing=1.3)
fig.text(0.56,0.58,"Both dopants lower the vacancy cost;\nPr stays uphill, Rb goes downhill:\na 5.36 eV contrast.",fontsize=7,color=INK,va="top",linespacing=1.35)
fig.text(0.56,0.36,"The order follows the formal hole count\n(0, 1, 3 per cell); hole localisation in the\nPr cell depends on an O-2p Hubbard term.",fontsize=7,color=INK,va="top",linespacing=1.35)
fig.text(0.56,0.08,"Same supercell, pseudopotentials, U and O$_2$ reference",fontsize=6,color=INK2)
fig.savefig("Graphical_Abstract.png"); fig.savefig("Graphical_Abstract.pdf"); print("GA written")
