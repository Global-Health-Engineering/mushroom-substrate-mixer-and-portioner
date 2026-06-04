import pandas as pd
import numpy as np
import math
import os


# =====================================================================
#  01_01 — WATER CONTENT DISTRIBUTION
# =====================================================================

def process_01_01_data(input_path='01_01_1_4_test_watercontent_raw.csv',
                       output_path='01_01_1_4_test_watercontent_derived.csv'):

    df_raw = pd.read_csv(input_path)

    # theoretical water contents
    w_theory_map = {1: 0.667, 2: 0.667, 3: 0.682, 4: 0.651}
    df_raw['w_theory'] = df_raw['trial'].map(w_theory_map)

    # split wet/dry
    df_wet = df_raw[df_raw['variable'] == 'm_wet'].copy()
    df_dry = df_raw[df_raw['variable'] == 'm_dry'].copy()

    df_merged = pd.merge(
        df_wet, df_dry,
        on=['trial', 'time_min', 'w_theory'],
        suffixes=('_wet', '_dry')
    )

    paddles = ['paddle1', 'paddle2', 'paddle3', 'paddle4']
    rows = []

    for _, row in df_merged.iterrows():
        out = {
            'trial': row['trial'],
            'time_min': row['time_min'],
            'variable': 'w',
            'w_theory': row['w_theory'],
            'observation': row['observation_wet']
        }

        vals = []
        for p in paddles:
            mw = row[f'{p}_wet']
            md = row[f'{p}_dry']
            if pd.notna(mw) and pd.notna(md) and mw > 0:
                w = (mw - md) / mw
                out[p] = w
                vals.append(w)
            else:
                out[p] = np.nan

        # derived stats
        vals = np.array(vals, dtype=float)
        out['mean_w'] = np.nanmean(vals)
        out['std_w'] = np.nanstd(vals, ddof=1)
        out['sem_w'] = out['std_w'] / np.sqrt(len(vals)) if len(vals) > 0 else np.nan

        # deviations
        for i, p in enumerate(paddles):
            out[f'dev_{p}'] = (out[p] - out['mean_w']) if pd.notna(out[p]) else np.nan

        rows.append(out)

    df_w = pd.DataFrame(rows)

    # combined 5‑min deviation metrics
    df_5 = df_w[(df_w['trial'].isin([2, 3, 4])) & (df_w['time_min'] == 5)]
    all_devs = []

    for _, r in df_5.iterrows():
        vals = [r[p] * 100 for p in paddles if pd.notna(r[p])]
        if len(vals) > 0:
            m = np.mean(vals)
            for v in vals:
                all_devs.append(abs(v - m))

    if len(all_devs) > 0:
        all_devs = np.array(all_devs)
        comb_mean = np.mean(all_devs)
        comb_sem = np.std(all_devs, ddof=1) / np.sqrt(len(all_devs))
    else:
        comb_mean = np.nan
        comb_sem = np.nan

    df_w['combined_5min_mean_dev_pct'] = comb_mean
    df_w['combined_5min_sem_pct'] = comb_sem

    df_final = pd.concat([df_raw, df_w], ignore_index=True)
    df_final.to_csv(output_path, index=False)

    print(f"[Data Pipeline] 01_01 derived data saved to {output_path}")
    return df_final



# =====================================================================
#  01_02 — PORTIONING HOMOGENEITY
# =====================================================================

def process_01_02_watercontent(df_raw):
    rows = []

    for trial in sorted(df_raw['trial'].unique()):
        df_t = df_raw[df_raw['trial'] == trial]
        df_probe = df_t.dropna(subset=['m_probe_wet', 'm_probe_dry']).copy()
        df_probe.loc[:, 'w'] = (df_probe['m_probe_wet'] - df_probe['m_probe_dry']) / df_probe['m_probe_wet']



        if df_probe.empty:
            continue

        df_probe['w'] = (df_probe['m_probe_wet'] - df_probe['m_probe_dry']) / df_probe['m_probe_wet']

        w_mean = df_probe['w'].mean()
        w_std = df_probe['w'].std(ddof=1)
        w_sem = w_std / np.sqrt(len(df_probe))

        rows.append({
            'trial': trial,
            'prototype': df_probe['prototype'].iloc[0],
            'n_probes': len(df_probe),
            'mean_watercontent': w_mean,
            'std_watercontent': w_std,
            'sem_watercontent': w_sem
        })

    return pd.DataFrame(rows)



def process_01_02_data(input_path='01_02_1_3_test_portions_raw.csv',
                       output_path='01_02_1_3_test_portions_derived.csv'):

    df = pd.read_csv(input_path)
    df_water = process_01_02_watercontent(df)

    inserted_mass = {1: 30.36, 2: 29.952, 3: 22.51}

    rows = []

    for trial in sorted(df['trial'].unique()):
        df_t = df[df['trial'] == trial]
        masses = df_t['m_bag'].dropna()
        n = len(masses)

        mean_mass = masses.mean()
        std_mass = masses.std(ddof=1)
        sem_mass = std_mass / np.sqrt(n) if n > 0 else np.nan
        std_err = std_mass / np.sqrt(2*(n-1)) if n > 1 else np.nan

        std_pct = (std_mass / mean_mass) * 100 if mean_mass > 0 else np.nan

        if n > 1 and mean_mass > 0:
            rsd_err = 100 * np.sqrt(
                (std_err / mean_mass)**2 +
                (std_mass * sem_mass / mean_mass**2)**2
            )
        else:
            rsd_err = np.nan

        ins = inserted_mass.get(trial, np.nan)
        total_out = masses.sum()
        loss_pct = (1 - total_out / ins) * 100 if ins > 0 else np.nan

        # per‑bag deviations
        df_t = df_t.copy()
        df_t['dev_from_mean'] = df_t['m_bag'] - mean_mass

        # water content stats
        wc = df_water[df_water['trial'] == trial]
        if not wc.empty:
            wc_mean = wc['mean_watercontent'].iloc[0]
            wc_std = wc['std_watercontent'].iloc[0]
            wc_sem = wc['sem_watercontent'].iloc[0]
        else:
            wc_mean = wc_std = wc_sem = np.nan

        rows.append({
            'trial': trial,
            'prototype': df_t['prototype'].iloc[0],
            'mean_bag_mass': mean_mass,
            'std_bag_mass': std_mass,     
            'std_bag_mass_pct': std_pct,
            'std_bag_mass_err_pct': rsd_err,
            'sem_bag_mass': sem_mass,
            'mass_loss_pct': loss_pct,
            'mean_watercontent': wc_mean,
            'std_watercontent': wc_std,
            'sem_watercontent': wc_sem,
            'note': 'all bags included'
        })

    # annotated trial 3 (bags 6–18)
    df_t3 = df[df['trial'] == 3]
    df_t3_clean = df_t3[df_t3['bag_id'].between(6, 18)]
    masses = df_t3_clean['m_bag'].dropna()
    n = len(masses)

    mean_mass = masses.mean()
    std_mass = masses.std(ddof=1)
    sem_mass = std_mass / np.sqrt(n)
    std_err = std_mass / np.sqrt(2*(n-1)) if n > 1 else np.nan
    std_pct = (std_mass / mean_mass) * 100

    rsd_err = 100 * np.sqrt(
        (std_err / mean_mass)**2 +
        (std_mass * sem_mass / mean_mass**2)**2
    ) if n > 1 else np.nan

    wc = df_water[df_water['trial'] == 3]
    wc_mean = wc['mean_watercontent'].iloc[0]
    wc_std = wc['std_watercontent'].iloc[0]
    wc_sem = wc['sem_watercontent'].iloc[0]

    rows.append({
        'trial': 3,
        'prototype': df_t3['prototype'].iloc[0],
        'mean_bag_mass': mean_mass,
        'std_bag_mass': std_mass,     
        'std_bag_mass_pct': std_pct,
        'std_bag_mass_err_pct': rsd_err,
        'sem_bag_mass': sem_mass,
        'mass_loss_pct': np.nan,
        'mean_watercontent': wc_mean,
        'std_watercontent': wc_std,
        'sem_watercontent': wc_sem,
        'note': 'Trial 3 (bags 6–18 only); user errors excluded'
    })

    df_out = pd.DataFrame(rows)
    df_out.to_csv(output_path, index=False)

    print(f"[Data Pipeline] 01_02 derived data saved to {output_path}")
    return df_out



# =====================================================================
#  01_03 — AGITATOR LONGITUDINAL TRANSPORT
# =====================================================================

def process_01_03_data():

    df_raw = pd.read_csv('01_03_1_3_agitator_longitudinal_raw.csv')
    df_raw['test_id'] = df_raw['test_id'].astype(str).str.strip()

    id_vars = ['trial', 'test_id', 'n_csr', 'RPM_agitator', 'm_substrate', 'placement']
    value_vars = ['paddle1', 'paddle2', 'paddle3', 'paddle4']

    df_long = pd.melt(
        df_raw,
        id_vars=id_vars,
        value_vars=value_vars,
        var_name='paddle_position',
        value_name='fill_height_cm'
    )

    df_long['paddle_position'] = df_long['paddle_position'].str.replace('paddle', '').astype(int)

    group_cols = ['test_id', 'n_csr', 'paddle_position']

    df_stats = df_long.groupby(group_cols)['fill_height_cm'].agg(
        mean_fill_height='mean',
        std_fill_height='std',
        n='count'
    ).reset_index()

    df_stats['std_fill_height'] = df_stats['std_fill_height'].fillna(0)
    df_stats['sem_fill_height'] = df_stats['std_fill_height'] / np.sqrt(df_stats['n'])

    df_derived = pd.merge(df_long, df_stats, on=group_cols, how='left')
    df_derived['rel_dev_pct'] = (
        (df_derived['fill_height_cm'] - df_derived['mean_fill_height'])
        / df_derived['mean_fill_height'] * 100
    )

    df_derived.to_csv('01_03_1_3_agitator_longitudinal_derived.csv', index=False)
    print(f"[Data Pipeline] 01_03 derived data saved to 01_03_1_3_agitator_longitudinal_derived.csv")



# =====================================================================
#  01_04 — MANIFOLD FLOW
# =====================================================================

def calculate_01_04_theory(n_holes=11, delta_h=0.4, Q_inlet_l_min=4.0):

    g = 9.81
    h = delta_h
    Q_tot = Q_inlet_l_min / 60000.0
    r = 0.99
    N = n_holes

    v1 = np.sqrt(2 * g * h)
    vel_terms = v1 * r**np.arange(N)

    v_sum = np.sum(vel_terms)
    A = Q_tot / v_sum
    d_theory = np.sqrt(4 * A / np.pi)
    d_theory_mm = d_theory * 1000

    return vel_terms, d_theory_mm



def process_01_04_data():

    vel_terms, d_theory_mm = calculate_01_04_theory()

    df_raw = pd.read_csv('01_04_1_3_manifold_raw.csv')
    df_raw['flow_l_min'] = (df_raw['volume_ml'] / 1000) / (df_raw['time_s'] / 60)

    grouped = df_raw.groupby(['test_id', 'bore_mm', 'orifice'])['flow_l_min'].agg(
        mean_flow='mean',
        std_flow='std',
        n='count'
    ).reset_index()

    grouped['std_flow'] = grouped['std_flow'].fillna(0)

    def get_theoretical_flow(bore_mm, orifice_idx):
        A = (np.pi / 4) * (bore_mm / 1000)**2
        v = vel_terms[orifice_idx - 1]
        return A * v * 60000

    grouped['theory_flow'] = grouped.apply(
        lambda r: get_theoretical_flow(r['bore_mm'], int(r['orifice'])),
        axis=1
    )

    grouped['theory_vel_m_s'] = grouped['orifice'].apply(lambda i: vel_terms[i - 1])
    grouped['theory_bore_mm'] = d_theory_mm

    def compute_velocity(row):
        A = (np.pi / 4) * (row['bore_mm'] / 1000)**2
        Q_mean = row['mean_flow'] / 60000
        Q_std = row['std_flow'] / 60000
        v = Q_mean / A
        v_err = Q_std / A
        return pd.Series({'vel_meas_m_s': v, 'vel_meas_err_m_s': v_err})

    grouped = pd.concat([grouped, grouped.apply(compute_velocity, axis=1)], axis=1)

    def add_velocity_loss(group):
        ref = group[group['orifice'] == 1].iloc[0]
        v1 = ref['vel_meas_m_s']
        dv1 = ref['vel_meas_err_m_s']

        vi = group['vel_meas_m_s']
        dvi = group['vel_meas_err_m_s']

        ratio = vi / v1
        rel_err_vi = dvi / vi
        rel_err_v1 = dv1 / v1

        sigma_ratio = ratio * np.sqrt(rel_err_vi**2 + rel_err_v1**2)

        group['vel_loss_pct_vs_1'] = (1 - ratio) * 100
        group['vel_loss_err_pct_vs_1'] = sigma_ratio * 100
        return group

        grouped = grouped.groupby(['test_id', 'bore_mm'], group_keys=False).apply(add_velocity_loss)

            

    # RSD + error
    rsd_rows = []

    for (test_id, bore), df_t in grouped.groupby(['test_id', 'bore_mm']):
        std_across = df_t['std_flow'].mean()
        mean_flow = df_t['mean_flow'].mean()
        n = len(df_t)

        rsd = (std_across / mean_flow * 100)

        sem_mean = std_across / np.sqrt(n)
        std_err = std_across / np.sqrt(2*(n-1))

        rsd_err = 100 * np.sqrt(
            (std_err / mean_flow)**2 +
            (std_across * sem_mean / mean_flow**2)**2
        )

        # aggregated values
        v_max = df_t['vel_meas_m_s'].max()
        v_min = df_t['vel_meas_m_s'].min()
        dv_pct = (v_max - v_min) / v_max * 100

        total_flow = df_t['mean_flow'].sum()

        req_rsd_ok = (rsd <= 10)
        req_dv_ok = (dv_pct <= 10)

        rsd_rows.append({
            'test_id': test_id,
            'bore_mm': bore,
            'rsd_pct': rsd,
            'rsd_err_pct': rsd_err,
            'total_flow_l_min': total_flow,
            'v_max_m_s': v_max,
            'v_min_m_s': v_min,
            'dv_pct': dv_pct,
            'req_rsd_ok': req_rsd_ok,
            'req_dv_ok': req_dv_ok
        })

    df_rsd = pd.DataFrame(rsd_rows)
    grouped = pd.merge(grouped, df_rsd, on=['test_id', 'bore_mm'], how='left')

    df_derived = pd.merge(df_raw, grouped, on=['test_id', 'bore_mm', 'orifice'])
    df_derived.to_csv('01_04_1_3_manifold_derived.csv', index=False)

    print("[Data Pipeline] 01_04 derived data saved to 01_04_1_3_manifold_derived.csv.")



# =====================================================================
#  MAIN
# =====================================================================

if __name__ == "__main__":
    process_01_01_data()
    process_01_02_data()
    process_01_03_data()
    process_01_04_data()
