import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# =====================================================================
#  01_01 — WATER CONTENT DISTRIBUTION
# =====================================================================

def generate_01_01_plots(data_path='01_01_1_4_test_watercontent_derived.csv',
                         save_prefix='01_01_plot'):

    df = pd.read_csv(data_path)

    paddles = ['paddle1', 'paddle2', 'paddle3', 'paddle4']

    # convert to %
    for p in paddles:
        df[p] = df[p] * 100
    df['mean_w'] = df['mean_w'] * 100
    df['std_w'] = df['std_w'] * 100
    df['sem_w'] = df['sem_w'] * 100

    # ---------------------------------------------------------
    # PLOT 1 — Trials 2 & 3
    # ---------------------------------------------------------
    df_sub = df[(df['trial'].isin([2, 3])) & (df['variable'] == 'w')].copy()

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))

    x_labels = ['Paddle 1', 'Paddle 2', 'Paddle 3', 'Paddle 4']

    time_colors = {0: '#1f77b4', 1: '#d62728', 5: '#ff7f0e', 10: '#2ca02c'}
    trial_markers = {2: 'o', 3: 's'}
    theory_styles = {2: '--', 3: '-.'}

    ax.axhspan(60, 70, color='green', alpha=0.12, label='Target Range (60–70%)')

    for trial in [2, 3]:
        df_t = df_sub[df_sub['trial'] == trial]

        for time in sorted(df_t['time_min'].unique()):
            row = df_t[df_t['time_min'] == time].iloc[0]

            y_vals = [row[p] for p in paddles]
            std_val = row['std_w']

            ax.plot(
                x_labels,
                y_vals,
                marker=trial_markers[trial],
                markersize=9,
                linewidth=2.2,
                linestyle='-',
                color=time_colors[time],
                label=f"Trial {trial} — {int(time)} min"
            )

            ax.errorbar(
                x_labels,
                y_vals,
                yerr=std_val,
                fmt='none',
                ecolor=time_colors[time],
                elinewidth=1.5,
                capsize=5,
                alpha=0.8
            )

        # theoretical line
        theory_val = df_t['w_theory'].iloc[0] * 100
        ax.axhline(
            theory_val,
            linestyle=theory_styles[trial],
            linewidth=2.2,
            color='black',
            alpha=0.8,
            label=f"Trial {trial} theoretical = {theory_val:.1f}%"
        )

    ax.set_title("Water Content Distribution — Trials 2 & 3", fontsize=14, fontweight='bold')
    ax.set_xlabel("Paddle Position")
    ax.set_ylabel("Water Content (%)")
    ax.set_ylim(0, 80)
    ax.legend(loc='lower right', fontsize=7)

    plt.tight_layout()
    plt.savefig(f"{save_prefix}_trial2_3.png", dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # PLOT 2 — Trial 4
    # ---------------------------------------------------------
    df_t4 = df[(df['trial'] == 4) & (df['variable'] == 'w')].copy()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axhspan(60, 70, color='green', alpha=0.12, label='Target Range (60–70%)')

    for time in sorted(df_t4['time_min'].unique()):
        row = df_t4[df_t4['time_min'] == time].iloc[0]

        y_vals = [row[p] for p in paddles]
        std_val = row['std_w']

        ax.plot(
            x_labels,
            y_vals,
            marker='s',
            markersize=9,
            linewidth=2.5,
            linestyle='-',
            color=time_colors[time],
            label=f"{int(time)} min Mixing Time"
        )

        ax.errorbar(
            x_labels,
            y_vals,
            yerr=std_val,
            fmt='none',
            ecolor=time_colors[time],
            elinewidth=1.5,
            capsize=5,
            alpha=0.8
        )

    ax.set_title("Water Content Distribution — Trial 4", fontsize=14, fontweight='bold')
    ax.set_xlabel("Paddle Position")
    ax.set_ylabel("Water Content (%)")
    ax.set_ylim(0, 80)
    ax.legend(loc='lower right', fontsize=9)

    plt.tight_layout()
    plt.savefig(f"{save_prefix}_trial4.png", dpi=300)
    plt.close()

    print("[Plot Pipeline] 01_01 plots successfully generated.")



# =====================================================================
#  01_03 — AGITATOR LONGITUDINAL TRANSPORT
# =====================================================================

def generate_01_03_plots():

    df = pd.read_csv('01_03_1_3_agitator_longitudinal_derived.csv')
    df['test_id'] = df['test_id'].astype(str).str.strip()

    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({
        'font.family': 'serif',
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'legend.fontsize': 11,
        'figure.dpi': 300
    })

    x_positions = [1, 2, 3, 4]
    x_labels = ['Paddle 1', 'Paddle 2', 'Paddle 3', 'Paddle 4']

    for t_id in ['1.1', '1.2']:
        df_test = df[df['test_id'] == t_id]
        if df_test.empty:
            continue

        fig, ax = plt.subplots(figsize=(8, 6))

        unique_csr = sorted(df_test['n_csr'].unique())
        colors = plt.cm.tab10(np.linspace(0, 1, len(unique_csr)))

        for idx, csr in enumerate(unique_csr):
            df_csr = df_test[df_test['n_csr'] == csr]
            df_plot = df_csr[['paddle_position', 'mean_fill_height', 'std_fill_height']].drop_duplicates()

            means = df_plot['mean_fill_height'].values
            stds = df_plot['std_fill_height'].values

            ax.plot(x_positions, means, marker='o', color=colors[idx],
                    linewidth=2, label=f'{int(csr)} Rotations')

            ax.fill_between(x_positions,
                            means - stds,
                            means + stds,
                            color=colors[idx],
                            alpha=0.2)

        placement = df_test['placement'].iloc[0].capitalize()
        ax.set_title(f'Longitudinal Fill Height - Test {t_id} ({placement} Placement)', fontweight='bold')
        ax.set_xlabel('Paddle Position')
        ax.set_ylabel('Fill Height (cm)')
        ax.set_xticks(x_positions)
        ax.set_xticklabels(x_labels)

        max_y = (df_test['mean_fill_height'] + df_test['std_fill_height']).max()
        ax.set_ylim(bottom=0, top=max_y * 1.15)

        ax.legend(title='Crankshaft\nRotations', loc='upper right')

        plt.tight_layout()
        plt.savefig(f'01_03_{t_id}_plot.png')
        plt.close()

    print("[Plot Pipeline] 01_03 plots successfully generated.")



# =====================================================================
#  01_04 — MANIFOLD FLOW
# =====================================================================

def generate_01_04_plots():

    df = pd.read_csv('01_04_1_3_manifold_derived.csv')

    vel_terms = df.sort_values('orifice')['theory_vel_m_s'].unique()
    d_theory_mm = df['theory_bore_mm'].unique()[0]

    A_theory = (np.pi / 4) * (d_theory_mm / 1000)**2
    theory_flows = [A_theory * v * 60000 for v in vel_terms]

    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({
        'font.family': 'serif',
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'legend.fontsize': 11,
        'figure.dpi': 300
    })

    fig, ax = plt.subplots(figsize=(10, 7))

    bore_values = sorted(df['bore_mm'].unique())
    cmap = plt.cm.get_cmap('viridis', len(bore_values))

    for i, bore in enumerate(bore_values):
        df_b = df[df['bore_mm'] == bore].drop_duplicates(subset=['test_id', 'orifice'])

        df_avg = df_b.groupby(['orifice']).agg(
            mean_flow=('mean_flow', 'mean'),
            std_flow=('std_flow', 'mean')
        ).reset_index()

        orifices = df_avg['orifice']
        means = df_avg['mean_flow']
        stds = df_avg['std_flow']

        color = cmap(i)

        ax.plot(orifices, means, marker='o', color=color, linewidth=2,
                label=f'Experiment with Nozzle {bore} mm')

        ax.fill_between(orifices, means - stds, means + stds,
                        color=color, alpha=0.15)

    ax.plot(
        np.arange(1, len(vel_terms) + 1),
        theory_flows,
        linestyle='--',
        color='black',
        linewidth=2.2,
        label=f'Theoretical Limit (d = {d_theory_mm:.2f} mm)'
    )

    ax.set_xlabel("Nozzle Position (1 = Inlet Side)")
    ax.set_ylabel("Volumetric Flow (L/min)")
    ax.set_xticks(range(1, len(vel_terms) + 1))

    ax.legend(loc='upper right')
    plt.tight_layout()

    plt.savefig("01_04_plot.png")
    plt.close()

    print("[Plot Pipeline] 01_04 plots successfully generated.")



# =====================================================================
#  MAIN
# =====================================================================

if __name__ == "__main__":
    generate_01_01_plots()
    generate_01_03_plots()
    generate_01_04_plots()
