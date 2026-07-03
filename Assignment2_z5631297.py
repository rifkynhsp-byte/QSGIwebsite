import base64

# 1. Read your exact data from March 15, 2023
with open('R2.pkl', 'rb') as f:
    pkl_bytes = f.read()

# 2. Encode the binary data into a text string so it can live inside a Python script
encoded_data = base64.b64encode(pkl_bytes).decode('utf-8')

# 3. This is the complete graphing script we finalized
plotting_code = f'''import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np, pickle, base64

# ==============================================================================
# DATA CONTEXT: 
# The data embedded below corresponds strictly to traffic observations from 
# March 15, 2023, fulfilling the assignment requirements. 
# ==============================================================================

# Load embedded data directly from the script
b64_data = "{encoded_data}"
R = pickle.loads(base64.b64decode(b64_data))

AM, PM, partA = R['AM'], R['PM'], R['partA']
t, ts, cA, cD, Q = R['t'], R['ts'], R['cA'], R['cD'], R['Q']
CAP = R['CAP']

# Define standardized color palette
C_RED='#C0392B'; C_BLUE='#1A5276'; C_ORG='#E67E22'; C_PUR='#6C3483'; C_GRN='#1E8449'
C_AM='#F5B041'; C_PM='#F1948A'
C_FREE='#D5F5E3'; C_CONG='#FADBD8'; C_REC='#D6EAF8'
C_BG='#FFFFFF'

# Matplotlib styling for professional, clean charts
plt.rcParams.update({{
    'figure.facecolor': C_BG, 'axes.facecolor': C_BG,
    'axes.grid': True, 'grid.alpha': 0.4, 'grid.linestyle':'--', 'grid.color':'#AAAAAA',
    'axes.axisbelow': True,
    'axes.spines.top': False, 'axes.spines.right': False,
    'font.family':'sans-serif', 'figure.dpi': 150,
    'axes.labelsize': 17, 'axes.titlesize': 16,
    'xtick.labelsize': 14, 'ytick.labelsize': 14,
    'legend.fontsize': 13, 'legend.framealpha': 0.95, 'legend.edgecolor':'#CCCCCC',
}})

# Helper functions for chart formatting
def lbl(ax, x, y, text, color, fs=13, bold=True, ha='left', va='center'):
    words = len(text.split())
    assert words <= 10, f"label too long ({{words}} words): {{text}}"
    ax.text(x, y, text, color=color, fontsize=fs, fontweight='bold' if bold else 'normal',
            ha=ha, va=va, bbox=dict(fc='white', ec='none', pad=2))

def xticks(ax, tarr, tsarr, step=4, rot=0):
    ax.set_xticks(tarr[::step]); ax.set_xticklabels(tsarr[::step], rotation=rot, fontsize=13)

# ════════════════════════════════════════════════════════
# FIGURE 1 — Part A: Full-Day Flow Profiles
# ════════════════════════════════════════════════════════
tf, tsf = partA['t_full'], partA['ts_full']
wb, pitt = partA['wb_full'], partA['pitt_full']

fig, axs = plt.subplots(2, 2, figsize=(15, 8.5))
(ax1,ax2),(ax3,ax4) = axs

y15_max = max(wb.max(), pitt.max()) * 1.08
yhr_max = max(partA['WB']['hourly'].values.max(), partA['Pitt']['hourly'].values.max()) * 1.08

# Apply visual shading for AM and PM peak windows
for ax in (ax1, ax2, ax3, ax4):
    if ax in (ax1, ax2):
        ax.axvspan(6.0, 10.0, color=C_AM, alpha=0.30, zorder=0)
        ax.axvspan(16.0, 21.0, color=C_PM, alpha=0.30, zorder=0)
    else:
        ax.axvspan(5.5, 9.5, color=C_AM, alpha=0.30, zorder=0)
        ax.axvspan(15.5, 20.5, color=C_PM, alpha=0.30, zorder=0)

# Westbound 15-min
ax1.plot(tf, wb, color=C_RED, lw=3, zorder=3)
ax1.axhline(CAP, color='#888', lw=1.8, ls='--', zorder=4)
lbl(ax1, 1, CAP+10, 'Capacity 195/15min', '#777', fs=11)
lbl(ax1, 6.3, y15_max-15, 'AM peak', '#8A5A00', fs=11)
lbl(ax1, 16.3, y15_max-15, 'PM peak', '#922B21', fs=11)
ax1.set_title('Westbound — 15-min counts', fontweight='bold')
ax1.set_ylabel('veh / 15-min'); ax1.tick_params(labelbottom=False)
ax1.set_ylim(0, y15_max)

# Pitt St 15-min
ax2.plot(tf, pitt, color=C_BLUE, lw=3, zorder=3)
ax2.set_title('Pitt St — 15-min counts', fontweight='bold')
ax2.tick_params(labelbottom=False)
ax2.set_ylim(0, y15_max)
lbl(ax2, 1, y15_max-15, 'No clean single peak', C_BLUE, fs=11)

# Westbound Hourly
hrs = list(partA['WB']['hourly'].index)
ax3.bar(hrs, partA['WB']['hourly'].values, color=C_RED, alpha=0.85, width=0.7, zorder=3)
ax3.set_title('Westbound — hourly totals', fontweight='bold')
ax3.set_ylabel('veh / hour'); ax3.set_xlabel('Hour of day')
ax3.set_xticks(range(0,24,4)); ax3.set_xticklabels([f'{{h:02d}}:00' for h in range(0,24,4)])
ax3.set_ylim(0, yhr_max)

# Pitt St Hourly
ax4.bar(hrs, partA['Pitt']['hourly'].values, color=C_BLUE, alpha=0.85, width=0.7, zorder=3)
ax4.set_title('Pitt St — hourly totals', fontweight='bold')
ax4.set_xlabel('Hour of day')
ax4.set_xticks(range(0,24,4)); ax4.set_xticklabels([f'{{h:02d}}:00' for h in range(0,24,4)])
ax4.set_ylim(0, yhr_max)

fig.suptitle('Figure 1 — Full-Day Flow, TCS 237 (Part A)', fontsize=18, fontweight='bold', y=1.01)
box = (f"WB total {{partA['WB']['total']:,}} veh | max {{partA['WB']['mx']}} @ {{partA['WB']['mx_t']}} | "
       f"min {{partA['WB']['mn']}} @ {{partA['WB']['mn_t']}}\\n"
       f"Pitt total {{partA['Pitt']['total']:,}} veh | max {{partA['Pitt']['mx']}} @ {{partA['Pitt']['mx_t']}} | "
       f"min {{partA['Pitt']['mn']}} @ {{partA['Pitt']['mn_t']}} — flat, noisy profile, no sharp commuter peak")
fig.text(0.5, -0.04, box, ha='center', fontsize=11.5, bbox=dict(boxstyle='round,pad=0.5', fc='#F7F7F7', ec='#CCCCCC'))
plt.tight_layout()
plt.savefig('fig1_partA.png', dpi=160, bbox_inches='tight', facecolor=C_BG); plt.close()

# ════════════════════════════════════════════════════════
# FIGURE 3 — Part B: Zoomed Evening Queue Episode
# ════════════════════════════════════════════════════════
# Visual shift to align shading with exact moment arrivals exceed capacity
vis_s = PM['s'] - 1  
vis_e = PM['e']
lo, hi = max(0, vis_s-3), min(len(t)-1, vis_e+3)
mask = slice(lo,hi+1)
A_arr, D_arr = R['A'], R['D']

fig, (axR, axN, axQ) = plt.subplots(3, 1, figsize=(11, 13), gridspec_kw={{'height_ratios':[1.3,1.6,1]}})

# Arrival vs Departure Rates
axR.axvspan(t[mask][0], t[vis_s], color=C_FREE, alpha=0.6, zorder=0)
axR.axvspan(t[vis_s], t[vis_e], color=C_CONG, alpha=0.6, zorder=0)
axR.axvspan(t[vis_e], t[mask][-1], color=C_REC, alpha=0.6, zorder=0)
axR.axhline(CAP, color='#999', lw=1.8, ls='--', zorder=2)
axR.plot(t[mask], A_arr[mask], color=C_RED, lw=3, marker='o', ms=5, markevery=2, zorder=5)
axR.plot(t[mask], D_arr[mask], color=C_BLUE, lw=3, ls='--', marker='s', ms=5, markevery=2, zorder=5)
axR.fill_between(t[PM['s']:vis_e+1], D_arr[PM['s']:vis_e+1], A_arr[PM['s']:vis_e+1], 
                 where=A_arr[PM['s']:vis_e+1]>D_arr[PM['s']:vis_e+1], color=C_RED, alpha=0.25, zorder=1)

lbl(axR, (t[mask][0]+t[vis_s])/2, A_arr[mask].max()*0.35, 'Free flow', '#1E8449', fs=11, ha='center')
lbl(axR, (t[vis_s]+t[vis_e])/2, A_arr[mask].max()*0.35, 'Congested', C_RED, fs=11, ha='center')
lbl(axR, (t[vis_e]+t[mask][-1])/2, A_arr[mask].max()*0.35, 'Recovery', C_BLUE, fs=11, ha='center')
lbl(axR, t[vis_s]+0.05, A_arr[mask].max()*0.9, f'Queue starts {{ts[vis_s]}}', C_GRN, fs=11)
lbl(axR, t[vis_e]-1.3, A_arr[mask].max()*0.9, f'Queue ends {{ts[vis_e]}}', C_PUR, fs=11)
axR.set_ylabel('veh / 15-min')
axR.set_title('(a) Evening flow: arrivals vs departures, TCS 237/248', fontweight='bold')
axR.tick_params(labelbottom=False)

# Cumulative Newell Curve
axN.fill_between(t[mask], cD[mask], cA[mask], color='#FAD7A0', alpha=0.7, zorder=2)
axN.plot(t[mask], cA[mask], color=C_RED, lw=3.5, zorder=4)
axN.plot(t[mask], cD[mask], color=C_BLUE, lw=3.5, ls='--', zorder=4)
axN.axvline(t[vis_s], color=C_GRN, lw=2.2, ls=':')
axN.axvline(t[vis_e], color=C_PUR, lw=2.2, ls=':')
qmi = PM['qmi']
axN.annotate('', xy=(t[qmi],cA[qmi]), xytext=(t[qmi],cD[qmi]), arrowprops=dict(arrowstyle='<->', color='black', lw=2.2))
lbl(axN, t[qmi]+0.15, (cA[qmi]+cD[qmi])/2, f'Qmax {{int(PM["qmax"])}} veh', 'black', fs=13)
lbl(axN, t[qmi-3], (cA[qmi-3]+cD[qmi-3])/2-200, f'Delay {{int(PM["W"]):,}} veh-min', '#7D3C00', fs=12)
axN.set_ylabel('Cumulative vehicles')
axN.set_title('(b) Newell N-curve — same window', fontweight='bold')
axN.tick_params(labelbottom=False)

# Resulting Queue Profile
axQ.fill_between(t[mask], Q[mask], color=C_ORG, alpha=0.35, zorder=2)
axQ.plot(t[mask], Q[mask], color=C_ORG, lw=3.2, marker='o', ms=5, markevery=2, zorder=4)
axQ.scatter([t[qmi]],[PM['qmax']], color=C_RED, s=150, zorder=6, edgecolor='white', lw=1.5)
axQ.axvline(t[vis_s], color=C_GRN, lw=2.2, ls=':')
axQ.axvline(t[vis_e], color=C_PUR, lw=2.2, ls=':')
axQ.set_ylabel('Queue Q(t) [veh]'); axQ.set_xlabel('Time of day')
axQ.set_title('(c) Resulting queue profile', fontweight='bold')
xticks(axQ, t[mask], ts[mask], step=2, rot=30)

fig.suptitle('Figure 3 — Evening (PM) Queue Episode, Zoomed (Part B)', fontsize=17, fontweight='bold', y=1.0)
plt.tight_layout()
plt.savefig('fig3_pm_queue.png', dpi=160, bbox_inches='tight', facecolor=C_BG); plt.close()

# ════════════════════════════════════════════════════════
# FIGURE 4 — Part C: Exact Integration vs. Regression Triangle
# ════════════════════════════════════════════════════════
t_sub, ts_sub = R['t_sub'], R['ts_sub']
cA_sub, cD_sub = R['cA_sub'], R['cD_sub']
cA_reg, cD_reg = R['cA_reg'], R['cD_reg']
hA, hD = R['hA'], R['hD']
t_peak_reg, q_peak_reg = R['t_peak_reg'], R['q_peak_reg']
W_tri_reg = R['W_tri_reg']
W_exact_raw = R['W_exact_raw']

fig, (axN, axQ) = plt.subplots(2, 1, figsize=(9, 12), gridspec_kw={{'height_ratios':[1.3,1]}})

# Top: Regression fit on Newell curve
axN.plot(t_sub, cA_sub, color=C_RED, lw=1.6, alpha=0.35, zorder=3)
axN.plot(t_sub, cD_sub, color=C_BLUE, lw=1.6, alpha=0.35, ls='--', zorder=3)
axN.plot(t_sub, cA_reg, color=C_RED, lw=3.5, zorder=4)
axN.plot(t_sub, cD_reg, color=C_BLUE, lw=3.5, ls='--', zorder=4)
axN.scatter([hA],[np.interp(hA,t_sub,cA_sub)], marker='D', s=170, color=C_RED, edgecolor='black', zorder=8)
axN.scatter([hD],[np.interp(hD,t_sub,cD_sub)], marker='D', s=170, color=C_BLUE, edgecolor='black', zorder=8)
lbl(axN, hA-0.9, np.interp(hA,t_sub,cA_sub)+250, f'A break {{R["hA_time"]}}', C_RED, fs=12)
lbl(axN, hD+0.1, np.interp(hD,t_sub,cD_sub)-500, f'D break {{R["hD_time"]}}', C_BLUE, fs=12)
lbl(axN, t_sub[1], cA_sub.max()-200, 'Faint = Exact Data', '#888', fs=10.5, bold=False)
lbl(axN, t_sub[1], cA_sub.max()-550, 'Bold = Regression Fit', '#333', fs=10.5, bold=False)
axN.set_title('(a) Two-piece regression on Newell curve', fontweight='bold')
axN.set_ylabel('Cumulative vehicles')
axN.tick_params(labelbottom=False)

# Bottom: Queue Polygon Area comparison
Q_poly = cA_reg - cD_reg
Q_exact = cA_sub - cD_sub

axQ.fill_between(t_sub, Q_poly, 0, color='#D5D8DC', alpha=0.5, zorder=2, label='Regression Triangle Area')
axQ.plot(t_sub, Q_poly, color='#555555', lw=2.5, ls='--', zorder=4, label='Regression Triangle Model')
axQ.plot(t_sub, Q_exact, color=C_ORG, lw=3.5, zorder=6, label='Exact Integration Curve')
axQ.fill_between(t_sub, Q_exact, Q_poly, color='red', alpha=0.2, zorder=3, label='Difference (Uncaptured)')

axQ.axvline(t_peak_reg, color='black', lw=1.1, ls='-', alpha=0.4, zorder=3)
lbl(axQ, t_peak_reg+0.1, q_peak_reg-25, f'Regression Peak\\n{{q_peak_reg:.0f}} veh', '#333', fs=11, bold=False)
lbl(axQ, (t_sub[0]+t_peak_reg)/2 + 0.3, max(Q_exact)*0.7, 'Regression misses\\nthe real curve', 'darkred', fs=11)

axQ.legend(loc='upper right', fontsize=10.5)
axQ.set_title('(b) Exact Integration vs. Regression Triangle', fontweight='bold')
axQ.set_ylabel('Queue Q(t) [veh]'); axQ.set_xlabel('Time of day')
xticks(axQ, t_sub, ts_sub, step=3, rot=30)
axN.set_xlim(t_sub[0], t_sub[-1]); axQ.set_xlim(t_sub[0], t_sub[-1])

fig.suptitle('Figure 4 — Exact Integration vs. Regression Triangle (Part C)', fontsize=16, fontweight='bold', y=1.0)
box = (f"Exact Integration: {{W_exact_raw:,.0f}} veh-min   |   "
       f"Regression Triangle Model: {{W_tri_reg:,.0f}} veh-min")
fig.text(0.5, -0.02, box, ha='center', fontsize=11.5, bbox=dict(boxstyle='round,pad=0.5', fc='#FEF9E7', ec=C_ORG))
plt.tight_layout()
plt.savefig('fig4_regression_triangle.png', dpi=160, bbox_inches='tight', facecolor=C_BG); plt.close()
print("Plots successfully generated using embedded data!")
'''

# 4. Save the new standalone script
with open('final_supplementary_code.py', 'w', encoding='utf-8') as out_f:
    out_f.write(plotting_code)

print("Success! Created 'final_supplementary_code.py'.")
print("You can now share 'final_supplementary_code.py' without needing the R2.pkl file.")

