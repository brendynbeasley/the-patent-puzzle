# Boldrin and Levine's patent puzzle on 1948–2025 data: findings

## In plain English

Michele Boldrin and David Levine (2008, 2013) pointed out that US patent grants roughly quadrupled between 1983 and
2010 while productivity growth did not speed up, and argued that patents mostly do not represent new ideas. This rerun
extends their comparison to 2025 and tries the strongest counter-measure, patents weighted by their stock-market value.

- **The puzzle has grown.** Utility patents granted per year rose 6.2 times from 1983 to 2020. Total factor
  productivity grew 1.09% a year before 1983, 0.98% in 1983–2010 and 0.74% since 2011.
- **Patent counts do not predict productivity.** Neither the number of patents nor their growth predicts TFP growth
  in the same year or the next five.
- **Market value does not rescue the count.** Weighting each patent by the stock-market value Kogan, Papanikolaou,
  Seru and Stoffman assign it gives no better prediction. Around its long-run trend, patenting does move with
  productivity, but the raw count captures that as well as the value measure does.
- **The biggest patent holders are not the most valuable.** IBM received 70,954 US patents in 2015–2024, worth about
  $5.0 million each by this measure. Apple's 24,112 averaged $184 million and Nvidia's 2,666 about $1.09 billion.

A friendlier tour is in the [README](../README.md), and [TECHNICAL.md](../TECHNICAL.md) has the method.

**Key to the labels.** *g* = annual TFP growth in percent (100 × log change of the BLS private nonfarm business
index). *g_util* = Fernald's utilization-adjusted TFP growth. *dlnP* = growth of utility grants in percent.
*tfp_growth_per_100k_patents* = average g divided by average grants in hundreds of thousands. *Value index* = log of
the summed KPSS value of patents granted in a year over the market value of nonfinancial corporate equities. *Count
index* = log of grants over the previous 20 years' grants. Coefficients in the extension are percentage points of
annual TFP growth per standard deviation of the index. Standard errors are Newey-West (3 lags, or max(h, 3) lags for
h-year horizons) except where noted.

## The paper's counts against the USPTO table

Boldrin and Levine's figures (paper_grants, paper_apps) are total grants of all kinds and total applications. The current USPTO table matches their 2010 figure exactly and revises 1983 and 2003 slightly. Source: `headline_counts.csv`.

| year | paper_grants | uspto_total_grants | paper_apps | uspto_total_apps | uspto_utility_grants |
|---|---|---|---|---|---|
| 1983 | 59,715 | 61,982 | 105,704 | 112,040 | 56,860 |
| 2003 | 189,597 | 187,012 | 355,418 | 366,043 | 169,023 |
| 2010 | 244,341 | 244,341 |  | 520,277 | 219,614 |
| 2020 |  | 388,900 |  | 646,244 | 352,066 |
| 2024 |  |  |  |  | 324,053 |

## Growth ratios

Source: `headline_ratios.csv`.

| measure | ratio |
|---|---|
| paper: grants 2010 / 1983 | 4.09 |
| USPTO total grants 2010 / 1983 | 3.94 |
| USPTO utility grants 2010 / 1983 | 3.86 |
| utility grants 2020 / 1983 | 6.19 |
| utility grants 2024 / 1983 | 5.70 |
| utility applications 2020 / 1983 | 5.76 |
| TFP level 2025 / 1983 | 1.42 |
| TFP level 1983 / 1953 | 1.42 |
| foreign-origin share of utility grants 1983 (%) | 42.19 |
| foreign-origin share of utility grants 2020 (%) | 53.25 |

## Eras

Source: `eras.csv`. The 2011–2025 era has patent counts through 2024 and TFP through 2025.

| era | mean_utility_grants | mean_utility_apps | patent_growth_pct | tfp_growth_pct | tfp_growth_util_pct | labor_prod_growth_pct | rd_share_gdp_pct | tfp_growth_per_100k_patents | years_with_patents | years_with_tfp |
|---|---|---|---|---|---|---|---|---|---|---|
| 1953-1982 | 57,959 | 91,800 | 0.944 | 1.092 | 1.621 | 2.093 | 0.973 | 1.885 | 30 | 30 |
| 1983-2010 | 124,112 | 257,475 | 4.762 | 0.982 | 0.968 | 2.284 | 1.666 | 0.791 | 28 | 28 |
| 2011-2025 | 305,509 | 581,452 | 2.779 | 0.741 | 0.763 | 1.488 | 2.381 | 0.242 | 14 | 15 |

## Decades

Source: `decades.csv`. The 2020s cover 2020–2024 for patents and 2020–2025 for TFP.

| decade | mean_utility_grants | mean_utility_apps | patent_growth_pct | tfp_growth_pct | tfp_growth_util_pct | labor_prod_growth_pct | rd_share_gdp_pct | tfp_growth_per_100k_patents | years_with_patents | years_with_tfp |
|---|---|---|---|---|---|---|---|---|---|---|
| 1950-1959 | 42,599 | 72,410 | 4.000 | 1.873 | 2.043 | 2.713 | 0.646 | 4.397 | 10 | 10 |
| 1960-1969 | 56,786 | 88,225 | 2.539 | 1.870 | 1.827 | 2.694 | 0.977 | 3.292 | 10 | 10 |
| 1970-1979 | 69,043 | 101,952 | -3.242 | 1.050 | 1.296 | 1.904 | 1.048 | 1.521 | 10 | 10 |
| 1980-1989 | 70,847 | 119,528 | 6.707 | 0.148 | 0.633 | 1.450 | 1.383 | 0.209 | 10 | 10 |
| 1990-1999 | 110,839 | 200,261 | 4.741 | 0.817 | 0.925 | 2.065 | 1.643 | 0.737 | 10 | 10 |
| 2000-2009 | 162,415 | 384,154 | 0.865 | 0.930 | 1.291 | 2.625 | 1.828 | 0.572 | 10 | 10 |
| 2010-2019 | 285,826 | 570,757 | 7.504 | 0.745 | 0.399 | 1.249 | 2.117 | 0.261 | 10 | 10 |
| 2020-2029 | 327,696 | 597,175 | -1.792 | 1.030 | 1.184 | 2.157 | 2.738 | 0.314 | 5 | 6 |

## Replication tests

Source: `replication_tests.csv`. Flow tests use utility grants (or applications) in units of 100,000.

| test | outcome | coef | se | ci_low | ci_high | p | n | note |
|---|---|---|---|---|---|---|---|---|
| flow: g_t on grants (100k) | BLS TFP growth | -0.172 | 0.156 | -0.479 | 0.135 | 0.271 | 76 |  |
| era break: g_t on 1[t>=1983] | BLS TFP growth | -0.370 | 0.465 | -1.281 | 0.541 | 0.426 | 77 |  |
| flow: g_t on grants (100k) | Fernald util-adjusted TFP growth | -0.232 | 0.158 | -0.542 | 0.078 | 0.143 | 76 |  |
| era break: g_t on 1[t>=1983] | Fernald util-adjusted TFP growth | -0.725 | 0.298 | -1.308 | -0.141 | 0.015 | 77 |  |
| flow: g_t on grants (100k) | Labor productivity growth | -0.201 | 0.178 | -0.550 | 0.148 | 0.258 | 76 |  |
| era break: g_t on 1[t>=1983] | Labor productivity growth | -0.253 | 0.395 | -1.027 | 0.520 | 0.521 | 77 |  |
| flow: g_t on applications (100k) | BLS TFP growth | -0.148 | 0.079 | -0.302 | 0.006 | 0.059 | 72 |  |
| distributed lag: sum of 6 coefficients on patent growth | BLS TFP growth | 0.012 | 0.067 | -0.120 | 0.144 | 0.861 | 71 | joint test all lags = 0: p = 0.851 |
| distributed lag: sum of 6 coefficients on patent growth | Fernald util-adjusted TFP growth | 0.037 | 0.053 | -0.068 | 0.142 | 0.490 | 71 | joint test all lags = 0: p = 0.368 |
| 5-year blocks: mean g on mean patent growth | BLS TFP growth | -0.033 | 0.027 | -0.086 | 0.020 | 0.225 | 15 | HC1 errors |
| 5-year blocks: correlation of mean g and mean patent growth | BLS TFP growth | -0.261 |  |  |  |  | 15 |  |

## Five-year blocks

Source: `five_year_blocks.csv`. Means over non-overlapping five-year blocks, 1950–2024.

| start | g | g_util | dlnP | grants | n |
|---|---|---|---|---|---|
| 1950 | 2.087 | 2.396 | -0.767 | 41,051 | 5 |
| 1955 | 1.659 | 1.690 | 8.767 | 44,146 | 5 |
| 1960 | 2.325 | 1.924 | -2.019 | 48,856 | 5 |
| 1965 | 1.414 | 1.731 | 7.098 | 64,715 | 5 |
| 1970 | 0.896 | 1.496 | 2.428 | 73,595 | 5 |
| 1975 | 1.204 | 1.097 | -8.911 | 64,490 | 5 |
| 1980 | -0.037 | 0.137 | 6.377 | 61,908 | 5 |
| 1985 | 0.332 | 1.130 | 7.037 | 79,787 | 5 |
| 1990 | 0.475 | -0.004 | 1.246 | 96,868 | 5 |
| 1995 | 1.158 | 1.855 | 8.236 | 124,810 | 5 |
| 2000 | 1.583 | 2.005 | 1.361 | 164,835 | 5 |
| 2005 | 0.276 | 0.577 | 0.369 | 159,996 | 5 |
| 2010 | 0.812 | -0.031 | 11.719 | 255,157 | 5 |
| 2015 | 0.678 | 0.828 | 3.289 | 316,495 | 5 |
| 2020 | 1.071 | 1.310 | -1.792 | 327,696 | 5 |

## Extension: patent value against patent counts

Source: `kpss_tests.csv`. The dependent variable is average annual TFP growth from year t to t+h. Controls are this year's TFP growth and the growth of nonfinancial corporate equity value, and the trend is linear in decades. With 54 regressions, two or three p-values below 0.05 would be expected by chance. Seven fall below 0.05, all on Fernald TFP: the count index with a trend at all three horizons, growth of grants at one year in all three specifications, and the value index without controls at five years, with a negative sign.

| test | outcome | coef | se | p | n |
|---|---|---|---|---|---|
| TFP growth next 1y on patent value / market cap | BLS TFP | -0.229 | 0.205 | 0.264 | 77 |
| TFP growth next 1y on patent value / market cap, controls | BLS TFP | -0.249 | 0.239 | 0.297 | 76 |
| TFP growth next 1y on patent value / market cap, trend | BLS TFP | 0.054 | 0.266 | 0.838 | 77 |
| TFP growth next 1y on grants / prior 20-year grants | BLS TFP | 0.060 | 0.233 | 0.796 | 77 |
| TFP growth next 1y on grants / prior 20-year grants, controls | BLS TFP | 0.091 | 0.278 | 0.744 | 76 |
| TFP growth next 1y on grants / prior 20-year grants, trend | BLS TFP | 0.310 | 0.236 | 0.190 | 77 |
| TFP growth next 1y on growth of grants | BLS TFP | 0.252 | 0.224 | 0.262 | 77 |
| TFP growth next 1y on growth of grants, controls | BLS TFP | 0.250 | 0.231 | 0.279 | 76 |
| TFP growth next 1y on growth of grants, trend | BLS TFP | 0.232 | 0.196 | 0.237 | 77 |
| TFP growth next 3y on patent value / market cap | BLS TFP | -0.144 | 0.168 | 0.389 | 75 |
| TFP growth next 3y on patent value / market cap, controls | BLS TFP | -0.114 | 0.143 | 0.428 | 74 |
| TFP growth next 3y on patent value / market cap, trend | BLS TFP | 0.184 | 0.187 | 0.326 | 75 |
| TFP growth next 3y on grants / prior 20-year grants | BLS TFP | 0.038 | 0.221 | 0.862 | 75 |
| TFP growth next 3y on grants / prior 20-year grants, controls | BLS TFP | 0.163 | 0.193 | 0.397 | 74 |
| TFP growth next 3y on grants / prior 20-year grants, trend | BLS TFP | 0.287 | 0.240 | 0.233 | 75 |
| TFP growth next 3y on growth of grants | BLS TFP | 0.196 | 0.139 | 0.158 | 75 |
| TFP growth next 3y on growth of grants, controls | BLS TFP | 0.180 | 0.133 | 0.177 | 74 |
| TFP growth next 3y on growth of grants, trend | BLS TFP | 0.181 | 0.126 | 0.152 | 75 |
| TFP growth next 5y on patent value / market cap | BLS TFP | -0.158 | 0.131 | 0.227 | 73 |
| TFP growth next 5y on patent value / market cap, controls | BLS TFP | -0.110 | 0.133 | 0.410 | 72 |
| TFP growth next 5y on patent value / market cap, trend | BLS TFP | 0.101 | 0.151 | 0.505 | 73 |
| TFP growth next 5y on grants / prior 20-year grants | BLS TFP | 0.046 | 0.146 | 0.755 | 73 |
| TFP growth next 5y on grants / prior 20-year grants, controls | BLS TFP | 0.135 | 0.130 | 0.300 | 72 |
| TFP growth next 5y on grants / prior 20-year grants, trend | BLS TFP | 0.282 | 0.148 | 0.057 | 73 |
| TFP growth next 5y on growth of grants | BLS TFP | 0.091 | 0.098 | 0.353 | 73 |
| TFP growth next 5y on growth of grants, controls | BLS TFP | 0.068 | 0.090 | 0.452 | 72 |
| TFP growth next 5y on growth of grants, trend | BLS TFP | 0.085 | 0.087 | 0.333 | 73 |
| TFP growth next 1y on patent value / market cap | Fernald util-adjusted TFP | -0.169 | 0.171 | 0.324 | 77 |
| TFP growth next 1y on patent value / market cap, controls | Fernald util-adjusted TFP | -0.219 | 0.199 | 0.271 | 76 |
| TFP growth next 1y on patent value / market cap, trend | Fernald util-adjusted TFP | 0.282 | 0.219 | 0.199 | 77 |
| TFP growth next 1y on grants / prior 20-year grants | Fernald util-adjusted TFP | 0.096 | 0.186 | 0.607 | 77 |
| TFP growth next 1y on grants / prior 20-year grants, controls | Fernald util-adjusted TFP | 0.165 | 0.186 | 0.376 | 76 |
| TFP growth next 1y on grants / prior 20-year grants, trend | Fernald util-adjusted TFP | 0.399 | 0.166 | 0.016 | 77 |
| TFP growth next 1y on growth of grants | Fernald util-adjusted TFP | 0.272 | 0.125 | 0.030 | 77 |
| TFP growth next 1y on growth of grants, controls | Fernald util-adjusted TFP | 0.286 | 0.123 | 0.020 | 76 |
| TFP growth next 1y on growth of grants, trend | Fernald util-adjusted TFP | 0.249 | 0.114 | 0.029 | 77 |
| TFP growth next 3y on patent value / market cap | Fernald util-adjusted TFP | -0.250 | 0.156 | 0.108 | 75 |
| TFP growth next 3y on patent value / market cap, controls | Fernald util-adjusted TFP | -0.233 | 0.172 | 0.176 | 74 |
| TFP growth next 3y on patent value / market cap, trend | Fernald util-adjusted TFP | 0.073 | 0.186 | 0.694 | 75 |
| TFP growth next 3y on grants / prior 20-year grants | Fernald util-adjusted TFP | 0.023 | 0.148 | 0.874 | 75 |
| TFP growth next 3y on grants / prior 20-year grants, controls | Fernald util-adjusted TFP | 0.051 | 0.154 | 0.738 | 74 |
| TFP growth next 3y on grants / prior 20-year grants, trend | Fernald util-adjusted TFP | 0.316 | 0.116 | 0.006 | 75 |
| TFP growth next 3y on growth of grants | Fernald util-adjusted TFP | 0.082 | 0.086 | 0.339 | 75 |
| TFP growth next 3y on growth of grants, controls | Fernald util-adjusted TFP | 0.070 | 0.091 | 0.440 | 74 |
| TFP growth next 3y on growth of grants, trend | Fernald util-adjusted TFP | 0.063 | 0.078 | 0.419 | 75 |
| TFP growth next 5y on patent value / market cap | Fernald util-adjusted TFP | -0.348 | 0.144 | 0.015 | 73 |
| TFP growth next 5y on patent value / market cap, controls | Fernald util-adjusted TFP | -0.315 | 0.171 | 0.066 | 72 |
| TFP growth next 5y on patent value / market cap, trend | Fernald util-adjusted TFP | -0.100 | 0.164 | 0.544 | 73 |
| TFP growth next 5y on grants / prior 20-year grants | Fernald util-adjusted TFP | -0.013 | 0.153 | 0.933 | 73 |
| TFP growth next 5y on grants / prior 20-year grants, controls | Fernald util-adjusted TFP | 0.030 | 0.151 | 0.842 | 72 |
| TFP growth next 5y on grants / prior 20-year grants, trend | Fernald util-adjusted TFP | 0.288 | 0.100 | 0.004 | 73 |
| TFP growth next 5y on growth of grants | Fernald util-adjusted TFP | 0.114 | 0.081 | 0.161 | 73 |
| TFP growth next 5y on growth of grants, controls | Fernald util-adjusted TFP | 0.089 | 0.076 | 0.244 | 72 |
| TFP growth next 5y on growth of grants, trend | Fernald util-adjusted TFP | 0.105 | 0.061 | 0.086 | 73 |

## Top US patent holders, 2015–2024

Source: `top_patent_holders.csv` and `top_patent_holders_notes.csv`. Value is the KPSS private value restated from 1982 to 2024 dollars with the CPI-U (factor 3.250, the ratio of the 2024 to the 1982 annual average CPI-U). Across these 15 companies, the Spearman rank correlation between patent count and value per patent is −0.40. Patents are counted by first-listed assignee as disambiguated by PatentsView, so subsidiaries filing under other names are not added in.

| company | assignee | patents | share_of_all_grants_pct | kpss_matched | value_bn_2024usd | value_per_patent_m_2024usd |
|---|---|---|---|---|---|---|
| IBM | International Business Machines Corporation | 70,954 | 2.20 | 69,719 | 346.3 | 5.0 |
| Qualcomm | QUALCOMM Incorporated | 27,385 | 0.85 | 27,159 | 480.0 | 17.7 |
| Intel | Intel Corporation | 25,556 | 0.79 | 25,334 | 515.0 | 20.3 |
| Apple | Apple Inc. | 24,112 | 0.75 | 23,942 | 4415.4 | 184.4 |
| Microsoft | MICROSOFT TECHNOLOGY LICENSING, LLC | 22,842 | 0.71 | 22,650 | 3403.3 | 150.3 |
| Google | GOOGLE LLC | 21,030 | 0.65 | 20,876 | 1103.2 | 52.8 |
| Amazon | Amazon Technologies, Inc. | 18,288 | 0.57 | 18,144 | 3612.7 | 199.1 |
| Ford | Ford Global Technologies, LLC | 16,461 | 0.51 | 15,143 | 170.4 | 11.3 |
| Micron | Micron Technology, Inc. | 14,061 | 0.44 | 13,901 | 298.8 | 21.5 |
| General Electric | General Electric Company | 13,498 | 0.42 | 13,396 | 396.6 | 29.6 |
| Boeing | THE BOEING COMPANY | 11,161 | 0.35 | 11,083 | 521.8 | 47.1 |
| Texas Instruments | Texas Instruments Incorporated | 9,265 | 0.29 | 9,201 | 320.1 | 34.8 |
| Nvidia | NVIDIA Corporation | 2,666 | 0.08 | 2,583 | 2807.9 | 1087.1 |
| Motorola Mobility | Motorola Mobility LLC | 1,282 | 0.04 | 1,271 | 37.9 | 29.8 |
| Merck | MERCK SHARP & DOHME LLC | 1,110 | 0.03 | 1,104 | 172.6 | 156.4 |

## Sample construction

Source: `sample_counts.csv` (copied from `data/derived/build_log.csv`).

| step | rows | note |
|---|---|---|
| USPTO U.S. Patent Activity table (h_counts.htm), years | 230 | 1790-2020 |
| USPTO Patent Statistics Chart (us_stat.htm), years | 58 | 1963-2020 |
| PatentsView g_patent rows loaded | 9,075,421 |  |
|   kept utility patents | 8,206,140 | (design, plant, reissue, defensive publications dropped) |
|   kept after dropping withdrawn patents | 8,187,839 |  |
|   utility grants 2015-2024 kept for the assignee table | 3,220,883 |  |
| KPSS patents loaded (patents of US-listed firms) | 3,831,908 |  |
|   kept with a value estimate | 3,831,908 |  |
| patents_by_year.csv rows written | 235 |  |
| max gap between PatentsView and USPTO utility grant counts, overlap years | 45 | largest relative gap 0.0010 |
| PatentsView assignee rows loaded | 8,385,078 |  |
|   2015-2024 utility grants with no organizational assignee (individuals, unassigned) | 186,568 |  |
|   of which matched to a KPSS value (owner listed in the US) | 1,106,455 |  |
| assignees_2015_2024.csv rows written (top 400 by patent count) | 400 |  |
