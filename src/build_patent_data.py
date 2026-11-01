"""Reduce the large public patent files to the small annual tables the analysis needs.

Three sources, all free:

    USPTO Patent Technology Monitoring Team tables (committed in data/raw/uspto/): utility patent
        applications and grants by calendar year, 1790-2020 ("U.S. Patent Activity") and total
        grants of every kind, 1963-2020 ("U.S. Patent Statistics Chart").
    PatentsView (USPTO, final release of 12/31/2024, Zenodo record 15783125): every granted patent
        with its grant date and its disambiguated assignee. Used to extend utility grant counts past
        2020 and to name the organizations that hold the patents.
    KPSS (Kogan, Papanikolaou, Seru & Stoffman 2017, extended data released September 9, 2026): the
        private value xi of every patent granted to a firm listed on a US stock exchange, 1926-2025,
        estimated from the owner's stock-market reaction on the grant date.

The three big downloads (about 0.6 GB) are too large for the repository. They are fetched into
data/raw/ if missing (ignored by git), or read from any folder given with --big-files. The script
writes three small committed files to data/derived/:

    patents_by_year.csv     one row per year: USPTO counts, PatentsView utility grants, KPSS count
                            and summed value
    assignees_2015_2024.csv utility patents granted 2015-2024 by first-listed assignee, with the
                            KPSS value of those that belong to US-listed firms
    build_log.csv           rows loaded, kept and dropped at each step

Usage (from the repository root):
    python src/build_patent_data.py                       # downloads into data/raw/ if needed
    python src/build_patent_data.py --big-files ../cache  # or reuse copies kept elsewhere
"""

import argparse
import html
import re
import urllib.request
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
DERIVED = ROOT / "data" / "derived"

KPSS_URL = ("https://raw.githubusercontent.com/KPSS2017/"
            "Technological-Innovation-Resource-Allocation-and-Growth-Extended-Data/master/KPSS_2025.zip")
PV_URL = "https://zenodo.org/api/records/15783125/files/{}/content"  # PatentsView 12/31/2024, CC-BY 4.0
DOWNLOADS = {
    "KPSS_2025.zip": KPSS_URL,
    "g_patent.tsv.zip": PV_URL.format("g_patent.tsv.zip"),
    "g_assignee_disambiguated.tsv.zip": PV_URL.format("g_assignee_disambiguated.tsv.zip"),
}

NAMES_FIRST, NAMES_LAST = 2015, 2024  # the last ten full grant years in the PatentsView release

LOG = []
BIG = RAW  # folder holding the three large downloads; set from --big-files


def log(step, rows, note=""):
    print(f"  {step}: {rows:,} {note}")
    LOG.append({"step": step, "rows": rows, "note": note})


def fetch(name):
    """Return the local path of a raw file, downloading it first if it is missing."""
    path = BIG / name
    if not path.exists():
        BIG.mkdir(parents=True, exist_ok=True)
        print(f"  downloading {name} (large; this takes a while) ...")
        tmp = path.with_suffix(path.suffix + ".part")
        urllib.request.urlretrieve(DOWNLOADS[name], tmp)
        tmp.rename(path)
    return path


def html_rows(path):
    """Every table row of a USPTO report page as a list of cell strings."""
    text = path.read_text(errors="ignore")
    rows = []
    for row in re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", text):
        cells = re.findall(r"(?is)<t[dh][^>]*>(.*?)</t[dh]>", row)
        rows.append([html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in cells])
    return rows


def number(s):
    """'1,234' -> 1234.0; 'n/a', '' -> NaN. The 2013 foreign-origin cell is printed as '283.781'."""
    s = s.replace(",", "").replace(".", "") if re.fullmatch(r"\d{1,3}\.\d{3}", s) else s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return float("nan")


def uspto_history():
    """Utility applications and grants 1790-2020, plus all-kind totals 1963-2020."""
    rows = [r for r in html_rows(RAW / "uspto" / "h_counts.htm") if len(r) == 9 and r[0].isdigit()]
    h = pd.DataFrame({"year": [int(r[0]) for r in rows],
                      "utility_apps": [number(r[1]) for r in rows],
                      "utility_grants": [number(r[4]) for r in rows]})
    log("USPTO U.S. Patent Activity table (h_counts.htm), years", len(h), f"{h.year.min()}-{h.year.max()}")

    # The page's HTML runs the reissue and total-grant cells together ("576   388,900"), so the
    # total is the last number in cell 15.
    rows = [r for r in html_rows(RAW / "uspto" / "us_stat.htm") if len(r) == 18 and r[0].isdigit()]
    s = pd.DataFrame({"year": [int(r[0]) for r in rows],
                      "total_apps": [number(r[7]) for r in rows],
                      "utility_grants_us_origin": [number(r[9]) for r in rows],
                      "utility_grants_all_origin": [number(r[12]) for r in rows],
                      "total_grants": [number(r[15].split()[-1]) for r in rows]})
    log("USPTO Patent Statistics Chart (us_stat.htm), years", len(s), f"{s.year.min()}-{s.year.max()}")
    return h.merge(s, on="year", how="left")


def patentsview_grants():
    """Utility grants per calendar year from PatentsView, plus the ids of the 2015-2024 grants."""
    g = pd.read_csv(fetch("g_patent.tsv.zip"), sep="\t", usecols=["patent_id", "patent_type", "patent_date",
                                                                   "withdrawn"], dtype=str)
    log("PatentsView g_patent rows loaded", len(g))
    g = g[g.patent_type.eq("utility")]
    log("  kept utility patents", len(g), "(design, plant, reissue, defensive publications dropped)")
    g = g[g.withdrawn.ne("1")]
    log("  kept after dropping withdrawn patents", len(g))
    g["year"] = g.patent_date.str[:4].astype(int)
    counts = g.groupby("year").size().rename("pv_utility_grants").reset_index()
    ids = g.loc[g.year.between(NAMES_FIRST, NAMES_LAST), ["patent_id", "year"]]
    log(f"  utility grants {NAMES_FIRST}-{NAMES_LAST} kept for the assignee table", len(ids))
    return counts, ids


def kpss():
    k = pd.read_csv(fetch("KPSS_2025.zip"), usecols=["patent_num", "issue_date", "filing_date", "xi_nominal",
                                                      "xi_real"])
    log("KPSS patents loaded (patents of US-listed firms)", len(k))
    k = k.dropna(subset=["xi_nominal"])
    log("  kept with a value estimate", len(k))
    k["year"] = k.issue_date.astype(str).str[:4].astype(int)
    by_year = k.groupby("year").agg(kpss_patents=("patent_num", "size"),
                                    kpss_xi_nominal_musd=("xi_nominal", "sum"),
                                    kpss_xi_real_m1982=("xi_real", "sum")).reset_index()
    return k, by_year


def assignee_table(ids, k):
    """First-listed assignee of each 2015-2024 utility grant, with KPSS value where the owner is listed."""
    a = pd.read_csv(fetch("g_assignee_disambiguated.tsv.zip"), sep="\t", dtype=str,
                    usecols=["patent_id", "assignee_sequence", "disambig_assignee_organization"])
    log("PatentsView assignee rows loaded", len(a))
    a = a[a.assignee_sequence.eq("0")]
    a = ids.merge(a[["patent_id", "disambig_assignee_organization"]], on="patent_id", how="left")
    a = a.rename(columns={"disambig_assignee_organization": "assignee"})
    no_org = a.assignee.isna().sum()
    log("  2015-2024 utility grants with no organizational assignee (individuals, unassigned)", int(no_org))
    a = a.dropna(subset=["assignee"])

    kv = k[["patent_num", "xi_real"]].copy()
    kv["patent_id"] = kv.patent_num.astype(str)
    a = a.merge(kv[["patent_id", "xi_real"]], on="patent_id", how="left")
    log("  of which matched to a KPSS value (owner listed in the US)", int(a.xi_real.notna().sum()))

    t = a.groupby("assignee").agg(patents=("patent_id", "size"),
                                  kpss_matched=("xi_real", "count"),
                                  kpss_value_m1982=("xi_real", "sum")).reset_index()
    t["total_grants_2015_2024"] = len(ids)
    return t.sort_values("patents", ascending=False)


def main():
    global BIG
    ap = argparse.ArgumentParser()
    ap.add_argument("--big-files", default=str(RAW), help="folder with KPSS_2025.zip and the PatentsView zips")
    BIG = Path(ap.parse_args().big_files)
    DERIVED.mkdir(parents=True, exist_ok=True)
    print("Building annual patent series")
    hist = uspto_history()
    pv, ids = patentsview_grants()
    k, kby = kpss()
    years = hist.merge(pv, on="year", how="outer").merge(kby, on="year", how="outer").sort_values("year")
    years.to_csv(DERIVED / "patents_by_year.csv", index=False)
    log("patents_by_year.csv rows written", len(years))

    overlap = years.dropna(subset=["utility_grants", "pv_utility_grants"])
    gap = (overlap.pv_utility_grants / overlap.utility_grants - 1).abs().max()
    log("max gap between PatentsView and USPTO utility grant counts, overlap years", len(overlap),
        f"largest relative gap {gap:.4f}")

    print("Building assignee table")
    t = assignee_table(ids, k)
    t.head(400).to_csv(DERIVED / "assignees_2015_2024.csv", index=False)
    log("assignees_2015_2024.csv rows written (top 400 by patent count)", min(len(t), 400))
    pd.DataFrame(LOG).to_csv(DERIVED / "build_log.csv", index=False)


if __name__ == "__main__":
    main()
