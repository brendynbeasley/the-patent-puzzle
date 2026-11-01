# Technical notes

This is the technical companion to the [README](README.md). It covers the data, the method, the full set of tests
and how to reproduce everything. Every table is in [results/FINDINGS.md](results/FINDINGS.md), and a methods review
of the original work is in [METHODS_REVIEW.md](METHODS_REVIEW.md).

## The original study

Michele Boldrin and David K. Levine, *Against Intellectual Monopoly*, Cambridge University Press, 2008, and "The Case
Against Patents," *Journal of Economic Perspectives* 27(1), 2013, pp. 3–22. The working-paper version (Federal Reserve
Bank of St. Louis WP 2012-035A, p. 6) states the headline numbers: 59,715 US patents issued in 1983 against 105,704
applications, 189,597 issued in 2003 against 355,418 applications, and 244,341 issued in 2010, so that "the flow of
patents roughly quadrupled" while neither R&D nor total factor productivity showed an upward trend. Chapter 4 of the
book ("The Evil of Intellectual Monopoly," pp. 78–79 of the authors' online text) makes the same comparison for
applications, which rose from about 90,000 a year in the 1960s to about 345,000 by the end of the 1990s, and says
that if patents measured progress, TFP "should have increased remarkably." The central claim, in the JEP abstract, is that patent counts have "no correlation with
measured productivity."

## Headline results

| Test | Estimate (SE) | 95% CI | p | N |
|---|---|---|---|---|
| BLS TFP growth on utility grants (per 100,000) | −0.17 (0.16) | [−0.48, 0.14] | 0.27 | 76 |
| BLS TFP growth, 1983 on vs. before | −0.37 (0.46) | [−1.28, 0.54] | 0.43 | 77 |
| Fernald utilization-adjusted TFP growth, 1983 on vs. before | −0.72 (0.30) | [−1.31, −0.14] | 0.015 | 77 |
| Sum of 6 lags of patent growth, BLS TFP growth | 0.012 (0.067) | [−0.12, 0.14] | 0.86 | 71 |
| Next-5-year TFP growth on KPSS value index (per s.d.) | −0.16 (0.13) | [−0.41, 0.10] | 0.23 | 73 |
| Same, with linear trend | 0.10 (0.15) | [−0.20, 0.40] | 0.51 | 73 |
| Next-5-year TFP growth on count index, with trend | 0.28 (0.15) | [−0.01, 0.57] | 0.057 | 73 |
| Same, Fernald utilization-adjusted TFP | 0.29 (0.10) | [0.09, 0.48] | 0.004 | 73 |

Utility grants rose 6.19 times from 1983 to 2020 (56,860 to 352,066). BLS TFP grew 1.09% a year in 1953–1982, 0.98%
in 1983–2010 and 0.74% in 2011–2025.

## Data

| File | Source | Used for |
|---|---|---|
| `data/raw/uspto/h_counts.htm` | USPTO Patent Technology Monitoring Team, "U.S. Patent Activity, Calendar Years 1790 to the Present" (Internet Archive capture of November 28, 2023; the uspto.gov page now returns 404) | Utility applications and grants, 1790–2020 |
| `data/raw/uspto/us_stat.htm` | USPTO PTMT, "U.S. Patent Statistics Chart, Calendar Years 1963–2020" (capture of January 15, 2024) | Total grants and applications, foreign-origin share |
| `g_patent.tsv.zip`, `g_assignee_disambiguated.tsv.zip` | PatentsView release of December 31, 2024, Zenodo record 15783125 (CC-BY 4.0), fetched by the build script | Utility grants 2021–2024; assignees |
| `KPSS_2025.zip` | Kogan, Papanikolaou, Seru and Stoffman extended data through 2025 (KPSS2017 repository on GitHub), fetched by the build script | Patent value ξ, 1926–2025 |
| `data/raw/fred/MFPNFBS.csv` | BLS total factor productivity, private nonfarm business, via FRED | TFP, 1948–2025 |
| `data/raw/frbsf/quarterly_tfp.xlsx` | John Fernald, utilization-adjusted TFP, FRBSF, vintage of October 1, 2026 | Robustness TFP |
| `data/raw/fred/OPHNFB.csv` | BLS output per hour, nonfarm business | Labor productivity |
| `data/raw/fred/Y006RC1A027NBEA.csv`, `GDPA.csv` | BEA private R&D investment and GDP | R&D share |
| `data/raw/fred/NCBEILQ027S.csv` | Federal Reserve Financial Accounts, nonfinancial corporate equities, market value | Denominator of the value index |
| `data/raw/fred/CPIAUCSL.csv` | BLS CPI-U | 1982 dollars to 2024 dollars (factor 3.250) |

All files were downloaded on November 1, 2026. `src/build_patent_data.py` reduces the large files to
`data/derived/patents_by_year.csv` and `data/derived/assignees_2015_2024.csv`, which are committed.

## Method

Rules fixed before looking at results:

- A patent is a utility grant counted in its calendar year of issue, the paper's own unit. USPTO counts are used
  through 2020 and PatentsView counts (withdrawn patents dropped) after; the two differ by at most 0.1% in 1976–2020.
- TFP growth is the log change of the BLS index, in percent. Fernald's utilization-adjusted series is the robustness
  check, and output per hour a second one.
- The break year is 1983, the first full year of the Court of Appeals for the Federal Circuit, as in the paper.
- Annual regressions use Newey-West errors with 3 lags (about the fourth root of 76). Horizon-h regressions use
  max(h, 3) lags.
- The count index is grants divided by grants over the previous 20 years, the patent term. The value index follows
  Kogan et al. (2017) with one substitute, the Financial Accounts market value of nonfinancial corporate equities in
  place of CRSP total market capitalization.
- The names table uses US-headquartered, US-listed companies only, because KPSS values foreign firms through their
  US listings.

The estimating equations are

```math
\begin{aligned}
g_t &= \alpha + \kappa\, P_t/10^{5} + \varepsilon_t \\
g_t &= \alpha + \delta\, \mathbf{1}[t \ge 1983] + u_t \\
g_t &= \alpha + \textstyle\sum_{k=0}^{5} \beta_k\, \Delta \ln P_{t-k} + v_t
\end{aligned}
```

with $`g_t = 100\,\Delta \ln A_t`$, and the extension

```math
\frac{100}{h}\left(\ln A_{t+h} - \ln A_t\right)
  = a + b\, z_t + c\, \frac{t-1948}{10} + e_t
```

where $`z_t`$ is the standardized value index $`\ln(\sum_i \xi_{i,t}/M_t)`$, count index
$`\ln(P_t / \sum_{s=t-20}^{t-1} P_s)`$ or growth of grants $`\Delta \ln P_t`$, run with and without the trend and with controls for current TFP growth and
the growth of $`M_t`$, for h = 1, 3, 5, on BLS and Fernald TFP.

The structural link behind the first equation is that if each patent raises TFP by a fraction $`\theta`$, then
$`g_t \approx \alpha + 100\,\theta P_t`$, so $`\kappa = 10^{7}\theta`$ and the descriptive ratio
$`\bar g / (\bar P/10^5)`$ by decade estimates it with $`\alpha = 0`$.

## Full test statistics

The replication tests are in `results/replication_tests.csv` (11 rows) and the extension in `results/kpss_tests.csv`
(54 rows). The pattern across the extension is as follows. Without a trend, the value index has negative
coefficients at every horizon on both TFP series (from −0.11 to −0.35), significant only for Fernald TFP at five years
(p = 0.015). With a trend, its coefficients range from −0.10 to 0.28, and every p is above 0.19. The count index with a
trend is positive in all six cases (0.28 to 0.40), significant for Fernald TFP at every horizon (p = 0.016, 0.006,
0.004) and not for BLS TFP (p = 0.19, 0.23, 0.057). Patent growth predicts next-year Fernald TFP growth
(0.27, p = 0.030) and nothing at longer horizons.

## Reproducing the results

```bash
pip install -r requirements.txt
python src/build_patent_data.py        # optional: rebuilds data/derived/, downloads about 0.6 GB
python src/patent_puzzle.py            # writes every CSV and PNG in results/
```

The first step can point at existing copies with `--big-files <folder>`. The second step runs offline from the
committed files in a few seconds.

## Repository layout

| Path | What it is |
|---|---|
| [src/build_patent_data.py](src/build_patent_data.py) | Reduces USPTO, PatentsView and KPSS files to annual and assignee tables |
| [src/patent_puzzle.py](src/patent_puzzle.py) | Headline check, eras, regressions, KPSS extension, names table, figures |
| `data/raw/` | USPTO tables, FRED series, Fernald workbook |
| `data/derived/` | Annual patent series, assignee table, build log |
| `results/` | Every CSV and PNG cited in the README |

## References

- Boldrin, M. and Levine, D. K. (2008). *Against Intellectual Monopoly*. Cambridge University Press.
- Boldrin, M. and Levine, D. K. (2013). The case against patents. *Journal of Economic Perspectives* 27(1), 3–22.
- Fernald, J. (2014). A quarterly, utilization-adjusted series on total factor productivity. FRBSF Working Paper
  2012-19.
- Kogan, L., Papanikolaou, D., Seru, A. and Stoffman, N. (2017). Technological innovation, resource allocation, and
  growth. *Quarterly Journal of Economics* 132(2), 665–712.
- Newey, W. and West, K. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent
  covariance matrix. *Econometrica* 55(3), 703–708.
