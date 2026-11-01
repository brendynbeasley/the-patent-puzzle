"""Boldrin and Levine's patent puzzle on 1948-2025 US data, and a value-weighted counter-test.

Boldrin and Levine (2008 book; 2013 Journal of Economic Perspectives) argue that US patent grants
roughly quadrupled after 1983 while productivity growth did not speed up, so patent counts carry no
information about measured productivity. This script:

    1. checks their headline grant counts against the USPTO's own table,
    2. compares TFP growth across eras and decades as patent flows rose,
    3. regresses annual TFP growth on the patent flow and on patent growth (Newey-West errors),
    4. runs the extension: Kogan, Papanikolaou, Seru and Stoffman's (2017) stock-market value of
       patents in place of the raw count, as a predictor of TFP growth over the next 1, 3 and 5 years,
    5. builds a table of the companies that received the most US patents in 2015-2024.

Run src/build_patent_data.py first (it writes data/derived/). Everything else is committed in
data/raw/. Outputs go to results/.

Usage (from the repository root):
    python src/patent_puzzle.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
DERIVED = ROOT / "data" / "derived"
OUT = ROOT / "results"

# Boldrin and Levine's figures, from "The Case Against Patents," St. Louis Fed WP 2012-035A, p. 6
# (the same passage appears in the 2013 JEP article): patents issued and applications filed.
PAPER = {1983: (59_715, 105_704), 2003: (189_597, 355_418), 2010: (244_341, None)}

# Eras: before the Court of Appeals for the Federal Circuit opened (October 1982), the paper's own
# window (1983 to 2010), and everything since.
ERAS = [(1953, 1982), (1983, 2010), (2011, 2025)]
FIRST_YEAR = 1949        # first year with a TFP growth rate (BLS index starts 1948)
NW_LAGS = 3              # Newey-West lags for annual regressions (about T^(1/4) for T = 76)
DIST_LAGS = 5            # lags of patent growth in the distributed-lag test
STOCK_YEARS = 20         # patent "stock" = grants over the previous 20 years (the patent term)
HORIZONS = [1, 3, 5]     # years ahead for the KPSS-style predictive regressions
BLOCK = 5                # non-overlapping block length, in years

# Companies for the names table: US-headquartered, US-listed filers among the 2015-2024 leaders,
# plus the firms Boldrin and Levine discuss (Microsoft, Google, Motorola, Texas Instruments, Apple)
# and two drug makers. Foreign firms are left out because KPSS values them through their US listing
# (often a thin ADR), which understates them badly.
NAMES = {
    "International Business Machines Corporation": "IBM",
    "QUALCOMM Incorporated": "Qualcomm",
    "Intel Corporation": "Intel",
    "Apple Inc.": "Apple",
    "MICROSOFT TECHNOLOGY LICENSING, LLC": "Microsoft",
    "GOOGLE LLC": "Google",
    "Amazon Technologies, Inc.": "Amazon",
    "Ford Global Technologies, LLC": "Ford",
    "Micron Technology, Inc.": "Micron",
    "General Electric Company": "General Electric",
    "THE BOEING COMPANY": "Boeing",
    "Texas Instruments Incorporated": "Texas Instruments",
    "NVIDIA Corporation": "Nvidia",
    "Motorola Mobility LLC": "Motorola Mobility",
    "MERCK SHARP & DOHME LLC": "Merck",
}

BLUE, ORANGE, INK, MUTED, SURFACE = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#fcfcfb"


def fred(series):
    d = pd.read_csv(RAW / "fred" / f"{series}.csv", parse_dates=["observation_date"])
    d["year"] = d.observation_date.dt.year
    return d.groupby("year")[series].mean()


def load():
    p = pd.read_csv(DERIVED / "patents_by_year.csv").set_index("year")
    d = pd.DataFrame(index=pd.RangeIndex(1945, 2026, name="year"))
    # Utility grants: USPTO table through 2020, PatentsView after (the two agree within 0.1% on 1976-2020).
    d["grants"] = p.utility_grants.combine_first(p.pv_utility_grants)
    d["apps"] = p.utility_apps
    d["total_grants"] = p.total_grants
    d["total_apps"] = p.total_apps
    d["foreign_share"] = 100 * (1 - p.utility_grants_us_origin / p.utility_grants_all_origin)
    d["kpss_xi"] = p.kpss_xi_nominal_musd
    d["kpss_n"] = p.kpss_patents
    tfp = fred("MFPNFBS")
    d["tfp"] = tfp
    d["g"] = 100 * np.log(tfp).diff()
    f = pd.read_excel(RAW / "frbsf" / "quarterly_tfp.xlsx", sheet_name="annual", engine="openpyxl")
    f = f[pd.to_numeric(f.date, errors="coerce").notna()].astype({"date": int}).set_index("date")
    d["g_util"] = pd.to_numeric(f.dtfp_util, errors="coerce")
    d["g_lp"] = 100 * np.log(fred("OPHNFB")).diff()
    d["rd_share"] = 100 * fred("Y006RC1A027NBEA") / fred("GDPA")
    d["mcap"] = fred("NCBEILQ027S")
    d["cpi"] = fred("CPIAUCSL")
    # Patent stock: utility grants over the previous 20 years (needs grants back to 1925).
    hist = p.utility_grants.reindex(range(1900, 1945))
    early = pd.concat([hist, d.grants]).shift(1).rolling(STOCK_YEARS).sum()
    d["stock"] = early.reindex(d.index)
    d["flow_to_stock"] = np.log(d.grants / d.stock)
    d["dlnP"] = 100 * np.log(d.grants).diff()
    d["kpss_index"] = np.log(d.kpss_xi / d.mcap)
    d["mret"] = 100 * np.log(d.mcap).diff()
    print(f"Loaded annual panel {d.index.min()}-{d.index.max()}: grants {int(d.grants.notna().sum())} years, "
          f"BLS TFP growth {int(d.g.notna().sum())} years, Fernald {int(d.g_util.notna().sum())}, "
          f"KPSS index {int(d.kpss_index.notna().sum())}")
    return d


def nw(y, X, lags=NW_LAGS):
    X = sm.add_constant(X)
    ok = y.notna() & X.notna().all(axis=1)
    return sm.OLS(y[ok], X[ok]).fit(cov_type="HAC", cov_kwds={"maxlags": lags}), int(ok.sum())


def years(res):
    """First and last year actually used in a fitted regression."""
    idx = res.model.data.row_labels
    return f"{min(idx)}-{max(idx)}"


def row(test, outcome, term, res, n, sample, note=""):
    b, se = res.params[term], res.bse[term]
    if sample is None or sample.startswith("h="):   # record the years the regression actually used
        sample = years(res) if sample is None else f"{sample}, {years(res)}"
    return {"test": test, "outcome": outcome, "term": term, "coef": b, "se": se,
            "ci_low": b - 1.96 * se, "ci_high": b + 1.96 * se, "p": res.pvalues[term], "n": n,
            "r2": res.rsquared, "sample": sample, "note": note}


def headline(d):
    rows = []
    for yr, (g_paper, a_paper) in PAPER.items():
        rows.append({"year": yr, "paper_grants": g_paper, "uspto_total_grants": d.total_grants[yr],
                     "paper_apps": a_paper, "uspto_total_apps": d.total_apps[yr],
                     "uspto_utility_grants": d.grants[yr]})
    t = pd.DataFrame(rows)
    t.loc[len(t)] = {"year": 2020, "uspto_total_grants": d.total_grants[2020], "uspto_total_apps": d.total_apps[2020],
                     "uspto_utility_grants": d.grants[2020]}
    t.loc[len(t)] = {"year": 2024, "uspto_utility_grants": d.grants[2024]}
    ratios = pd.DataFrame([
        {"measure": "paper: grants 2010 / 1983", "ratio": PAPER[2010][0] / PAPER[1983][0]},
        {"measure": "USPTO total grants 2010 / 1983", "ratio": d.total_grants[2010] / d.total_grants[1983]},
        {"measure": "USPTO utility grants 2010 / 1983", "ratio": d.grants[2010] / d.grants[1983]},
        {"measure": "utility grants 2020 / 1983", "ratio": d.grants[2020] / d.grants[1983]},
        {"measure": "utility grants 2024 / 1983", "ratio": d.grants[2024] / d.grants[1983]},
        {"measure": "utility applications 2020 / 1983", "ratio": d.apps[2020] / d.apps[1983]},
        {"measure": "TFP level 2025 / 1983", "ratio": d.tfp[2025] / d.tfp[1983]},
        {"measure": "TFP level 1983 / 1953", "ratio": d.tfp[1983] / d.tfp[1953]},
        {"measure": "foreign-origin share of utility grants 1983 (%)", "ratio": d.foreign_share[1983]},
        {"measure": "foreign-origin share of utility grants 2020 (%)", "ratio": d.foreign_share[2020]},
    ])
    t.to_csv(OUT / "headline_counts.csv", index=False)
    ratios.to_csv(OUT / "headline_ratios.csv", index=False)
    print("Headline counts checked against USPTO:")
    print(t.to_string(index=False))
    print(ratios.to_string(index=False))


def period_table(d, spans, label):
    rows = []
    for a, b in spans:
        s = d.loc[a:b]
        rows.append({label: f"{a}-{b}", "mean_utility_grants": s.grants.mean(), "mean_utility_apps": s.apps.mean(),
                     "patent_growth_pct": s.dlnP.mean(), "tfp_growth_pct": s.g.mean(),
                     "tfp_growth_util_pct": s.g_util.mean(), "labor_prod_growth_pct": s.g_lp.mean(),
                     "rd_share_gdp_pct": s.rd_share.mean(),
                     "tfp_growth_per_100k_patents": s.g.mean() / s.grants.mean() * 1e5,
                     "years_with_patents": int(s.grants.notna().sum()), "years_with_tfp": int(s.g.notna().sum())})
    return pd.DataFrame(rows)


def eras(d):
    e = period_table(d, ERAS, "era")
    dec = period_table(d, [(y, y + 9) for y in range(1950, 2030, 10)], "decade")
    e.to_csv(OUT / "eras.csv", index=False)
    dec.to_csv(OUT / "decades.csv", index=False)
    print("Eras:\n" + e.round(3).to_string(index=False))
    print("Decades:\n" + dec.round(3).to_string(index=False))


def replication_tests(d):
    s = d.loc[FIRST_YEAR:].copy()
    s["P100k"] = s.grants / 1e5
    s["A100k"] = s.apps / 1e5
    s["post1983"] = (s.index >= 1983).astype(float)
    rows = []
    for out, lab in [("g", "BLS TFP growth"), ("g_util", "Fernald util-adjusted TFP growth"),
                     ("g_lp", "Labor productivity growth")]:
        r, n = nw(s[out], s[["P100k"]])
        rows.append(row("flow: g_t on grants (100k)", lab, "P100k", r, n, None))
        r, n = nw(s[out], s[["post1983"]])
        rows.append(row("era break: g_t on 1[t>=1983]", lab, "post1983", r, n, None))
    r, n = nw(s.g, s[["A100k"]])
    rows.append(row("flow: g_t on applications (100k)", "BLS TFP growth", "A100k", r, n, None))

    # Distributed lag: g_t on patent growth this year and the five before.
    lags = pd.concat({f"dlnP_l{k}": s.dlnP.shift(k) for k in range(DIST_LAGS + 1)}, axis=1)
    for out, lab in [("g", "BLS TFP growth"), ("g_util", "Fernald util-adjusted TFP growth")]:
        r, n = nw(s[out], lags)
        names = list(lags.columns)
        w = np.ones(len(names))
        b = r.params[names].values @ w
        se = np.sqrt(w @ r.cov_params().loc[names, names].values @ w)
        joint = r.wald_test(", ".join(f"{c} = 0" for c in names), scalar=True)
        rows.append({"test": f"distributed lag: sum of {DIST_LAGS + 1} coefficients on patent growth",
                     "outcome": lab, "term": "sum_dlnP", "coef": b, "se": se, "ci_low": b - 1.96 * se,
                     "ci_high": b + 1.96 * se, "p": 2 * stats.norm.sf(abs(b / se)),
                     "n": n, "r2": r.rsquared, "sample": years(r),
                     "note": f"joint test all lags = 0: p = {float(joint.pvalue):.3f}"})

    # Non-overlapping five-year blocks starting 1950.
    s["block"] = (s.index - 1950) // BLOCK
    blk = s.loc[1950:2024].groupby("block").agg(start=("g", lambda x: x.index.min()), g=("g", "mean"),
                                                g_util=("g_util", "mean"), dlnP=("dlnP", "mean"),
                                                grants=("grants", "mean"), n=("g", "size"))
    blk = blk[blk.n == BLOCK].astype({"start": int, "n": int})
    blk.to_csv(OUT / "five_year_blocks.csv", index=False)
    X = sm.add_constant(blk[["dlnP"]])
    r = sm.OLS(blk.g, X).fit(cov_type="HC1")
    rows.append(row("5-year blocks: mean g on mean patent growth", "BLS TFP growth", "dlnP", r, len(blk),
                    "1950-2024", "HC1 errors"))
    corr = np.corrcoef(blk.g, blk.dlnP)[0, 1]
    t = pd.DataFrame(rows)
    t.loc[len(t)] = {"test": "5-year blocks: correlation of mean g and mean patent growth",
                     "outcome": "BLS TFP growth", "term": "corr", "coef": corr, "n": len(blk), "sample": "1950-2024"}
    t.to_csv(OUT / "replication_tests.csv", index=False)
    print("Replication tests:\n" + t[["test", "outcome", "coef", "se", "p", "n"]].round(4).to_string(index=False))
    return s


def kpss_tests(d):
    """TFP growth over the next h years on the patent-value index and on two count indexes."""
    rows = []
    s = d.loc[1948:].copy()
    s["trend"] = (s.index - 1948) / 10
    for col in ["kpss_index", "flow_to_stock", "dlnP"]:
        z = s[col]
        s[col + "_z"] = (z - z.mean()) / z.std()
    for tfp_col, lab in [("tfp", "BLS TFP"), ("util", "Fernald util-adjusted TFP")]:
        if tfp_col == "util":
            lnA = (s.g_util / 100).fillna(0).cumsum()
            lnA[s.g_util.isna()] = np.nan
        else:
            lnA = np.log(s.tfp)
        for h in HORIZONS:
            y = 100 * (lnA.shift(-h) - lnA) / h
            for reg, sample_note in [("kpss_index_z", "patent value / market cap"),
                                     ("flow_to_stock_z", "grants / prior 20-year grants"),
                                     ("dlnP_z", "growth of grants")]:
                r, n = nw(y, s[[reg]], lags=max(h, NW_LAGS))
                rows.append(row(f"TFP growth next {h}y on {sample_note}", lab, reg, r, n, f"h={h}"))
                X = pd.concat([s[reg], s.g.rename("g_lag"), s.mret], axis=1)
                r, n = nw(y, X, lags=max(h, NW_LAGS))
                rows.append(row(f"TFP growth next {h}y on {sample_note}, controls", lab, reg, r, n, f"h={h}",
                                "controls: this year's TFP growth and stock-market growth"))
                X = pd.concat([s[reg], s.trend], axis=1)
                r, n = nw(y, X, lags=max(h, NW_LAGS))
                rows.append(row(f"TFP growth next {h}y on {sample_note}, trend", lab, reg, r, n, f"h={h}",
                                "linear time trend removes the drift in the index"))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "kpss_tests.csv", index=False)
    s[["tfp", "grants", "apps", "kpss_n", "kpss_xi", "mcap", "kpss_index", "flow_to_stock", "dlnP", "g", "g_util"]].to_csv(
        OUT / "annual_series.csv")
    print("KPSS extension (coefficient = pct points of annual TFP growth per 1 s.d. of the index):")
    print(t[["test", "outcome", "coef", "se", "p", "n"]].round(3).to_string(index=False))
    return s


def names_table(d):
    a = pd.read_csv(DERIVED / "assignees_2015_2024.csv")
    total = a.total_grants_2015_2024.iloc[0]
    to_2024 = d.cpi[2024] / d.cpi[1982]   # KPSS xi_real is in 1982 dollars (xi_nominal = xi_real for 1982 grants)
    t = a[a.assignee.isin(NAMES)].copy()
    missing = set(NAMES) - set(t.assignee)
    if missing:
        print(f"  names not found in assignee table: {missing}")
    t["company"] = t.assignee.map(NAMES)
    t["share_of_all_grants_pct"] = 100 * t.patents / total
    t["value_bn_2024usd"] = t.kpss_value_m1982 * to_2024 / 1e3
    t["value_per_patent_m_2024usd"] = t.kpss_value_m1982 / t.kpss_matched * to_2024
    t = t.sort_values("patents", ascending=False)
    by = t.set_index("company")
    cols = ["company", "assignee", "patents", "share_of_all_grants_pct", "kpss_matched", "value_bn_2024usd",
            "value_per_patent_m_2024usd"]
    t[cols].to_csv(OUT / "top_patent_holders.csv", index=False)
    rank = pd.DataFrame({"statistic": ["utility grants 2015-2024 (all owners)", "CPI factor 1982 to 2024 dollars",
                                       "Spearman rank correlation, patents vs value per patent (table firms)",
                                       "Nvidia patents as % of IBM patents",
                                       "Nvidia value per patent / IBM value per patent"],
                         "value": [total, to_2024, t.patents.corr(t.value_per_patent_m_2024usd, method="spearman"),
                                   100 * by.patents["Nvidia"] / by.patents["IBM"],
                                   by.value_per_patent_m_2024usd["Nvidia"] / by.value_per_patent_m_2024usd["IBM"]]})
    rank.to_csv(OUT / "top_patent_holders_notes.csv", index=False)
    pd.read_csv(DERIVED / "build_log.csv").to_csv(OUT / "sample_counts.csv", index=False)
    print("Top patent holders:\n" + t[cols[:1] + cols[2:]].round(2).to_string(index=False))


def style(ax):
    ax.set_facecolor(SURFACE)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.grid(axis="y", color="#e4e3df", linewidth=0.8)
    ax.set_axisbelow(True)


def figures(d, s):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7), sharex=True, facecolor=SURFACE)
    x = d.loc[1948:2025]
    ax1.plot(x.index, x.apps / 1e3, color=ORANGE, lw=2, label="Utility applications filed")
    ax1.plot(x.index, x.grants / 1e3, color=BLUE, lw=2, label="Utility patents granted")
    ax1.set_ylabel("Thousands per year", color=MUTED)
    ax1.set_title("US patents per year", loc="left", color=INK, fontsize=11)
    ax1.legend(frameon=False, fontsize=9, loc="upper left")
    ax1.annotate(f"{x.apps[2020] / 1e3:.0f}k filed in 2020", (2020, x.apps[2020] / 1e3), xytext=(2003, 640),
                 color=MUTED, fontsize=8, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
    ax1.annotate(f"{x.grants[1983] / 1e3:.0f}k granted in 1983", (1983, x.grants[1983] / 1e3), xytext=(1986, 15),
                 color=MUTED, fontsize=8, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
    ax2.bar(x.index, x.g, color=BLUE, alpha=0.25, width=0.8, label="Annual")
    roll = x.g.rolling(10).mean()
    ax2.plot(x.index, roll, color=BLUE, lw=2, label="Trailing 10-year average")
    ax2.axhline(0, color=MUTED, lw=0.8)
    ax2.set_ylabel("Percent per year", color=MUTED)
    ax2.set_title("Growth of total factor productivity, private nonfarm business (BLS)", loc="left",
                  color=INK, fontsize=11)
    ax2.legend(frameon=False, fontsize=9, loc="lower left")
    for ax in (ax1, ax2):
        style(ax)
        ax.axvline(1982.8, color=MUTED, lw=0.8, ls=":")
    ax1.text(1983.5, 560, "Federal Circuit opens, Oct. 1982", color=MUTED, fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "patents_and_tfp.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)

    h = 5
    lnA = np.log(s.tfp)
    s = s.assign(y5=100 * (lnA.shift(-h) - lnA) / h)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), sharey=True, facecolor=SURFACE)
    for ax, col, title, color in [(axes[0], "flow_to_stock", "Patent count: grants / prior 20 years' grants", ORANGE),
                                  (axes[1], "kpss_index", "Patent value: KPSS value / stock-market value", BLUE)]:
        ok = s[[col, "y5"]].dropna()
        ax.scatter(ok[col], ok.y5, s=34, color=color, edgecolor=SURFACE, linewidth=1.2, zorder=3)
        b = np.polyfit(ok[col], ok.y5, 1)
        xs = np.linspace(ok[col].min(), ok[col].max(), 50)
        ax.plot(xs, b[1] + b[0] * xs, color=INK, lw=1.2)
        for yr in [1955, 1979, 2000, 2019]:
            if yr in ok.index:
                ax.annotate(str(yr), (ok.loc[yr, col], ok.loc[yr, "y5"]), fontsize=7.5, color=MUTED,
                            xytext=(4, 3), textcoords="offset points")
        ax.set_title(title, loc="left", color=INK, fontsize=10)
        ax.set_xlabel("Index in year t (log)", color=MUTED)
        style(ax)
    axes[0].set_ylabel("TFP growth, t to t+5 (% per year)", color=MUTED)
    fig.tight_layout()
    fig.savefig(OUT / "count_vs_value.png", dpi=150, facecolor=SURFACE)
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    d = load()
    headline(d)
    eras(d)
    replication_tests(d)
    s = kpss_tests(d)
    names_table(d)
    figures(d, s)
    print(f"Wrote CSVs and PNGs to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
