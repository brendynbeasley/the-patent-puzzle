# Methods review: Boldrin and Levine (2008, 2013)

- **Paper.** Michele Boldrin and David K. Levine, *Against Intellectual Monopoly*, Cambridge University Press, 2008;
  and "The Case Against Patents," *Journal of Economic Perspectives* 27(1), Winter 2013, pp. 3–22.
- **Statistical focus.** The aggregate "patent puzzle" comparison, that US patents issued rose from 59,715 in 1983 to
  244,341 in 2010 while R&D and total factor productivity showed no upward trend; and the claim, resting on Boldrin,
  Correa, Levine and Ornaghi (2011), that patenting has no statistically significant correlation with productivity
  across sectors.
- **Review standard.** Standard reporting of estimates, uncertainty and sample construction for the empirical
  claims, as in the current AEA Data and Code Availability Policy; internal consistency and explicit assumptions for
  the theoretical argument; and whether the central prediction is stated in a testable form.
- **What was read.** The full text of the working-paper version of the JEP article, "The Case Against Patents,"
  Federal Reserve Bank of St. Louis Working Paper 2012-035A (draft of June 29, 2012), from the St. Louis Fed's site;
  the published abstract on the AEA's article page (the JEP full text was behind a browser check and was not read);
  and the book chapters posted on David Levine's website, of which I read the patent and productivity passage of
  Chapter 4 ("The Evil of Intellectual Monopoly," pp. 78–79 of the online text) in full and searched Chapters 1 to 10 for figures and statistics.
  Page references below are to the working paper unless a chapter is named. The published JEP text may differ in
  wording, numbering and figures.

## Methods summary

The work is a policy argument that combines a theory of competitive innovation (developed in the authors' earlier
journal articles and summarized in Chapters 2 and 3 of the book) with a review of empirical evidence. It contains no
new econometric estimation of its own except two small exercises in the working paper, a residual table relating
R&D intensity to an index of IP protection and two scatter plots reproduced from Boldrin, Correa, Levine and Ornaghi
(2011).

### Research design

A narrative review. The aggregate claim is a descriptive before-and-after comparison of US patent counts with
productivity trends, with 1983 as the starting point. The cross-sector claim is reported from a companion working
paper rather than carried out in the text.

### Sampling strategy

Not stated for the aggregate comparison beyond the choice of years (1983, 2003, 2010). The metastudy cited in Section
4 gathered "the 24 studies we could find in 2006" on whether strengthening patent protection raises innovation, with
no search protocol reported.

### Sample size

Three years of US patent counts in the aggregate comparison; 24 studies in the metastudy; 31 countries over 1981–1990
in the reanalysis of Anwar and Evenson's data; the sector-level panels of the companion paper are not sized in the
text.

### Inclusion and exclusion criteria

Not reported for the metastudy or for the case studies (Apple and Android, Microsoft and Motorola, Texas
Instruments, the Wright brothers, Marconi, the Cornish steam engine). Case selection is illustrative.

### Independent and dependent variables

Aggregate claim: patents issued and applications filed (independent) against R&D spending and TFP (dependent),
neither of which is given as a number in the working paper. Cross-sector claim: patents and patent citations against
labor productivity and TFP growth. Residual table: an IP-protection index from 0 to 4 against the residual of R&D per
capita on GDP.

### Statistical methods

Descriptive comparison for the aggregate claim. For the 31-country data, an OLS regression of R&D intensity on GDP,
then mean residuals by IP level. For the cross-sector results, regressions summarized verbally from the companion
paper.

### Reported effect sizes

The patent counts; an elasticity of 0.34 of the R&D-to-GDP ratio with respect to GDP; mean residuals by IP level; and
a productivity-growth gap of "up to 2%" between the most and least competitive sectors (p. 18).

### Confidence intervals

None reported anywhere in the material read.

### P-values, if applicable

None reported. Results are described as "statistically significant" or "not statistically different from zero"
without test statistics.

### Missing data treatment

Not discussed.

### Stated limitations

The authors acknowledge that patents may matter in pharmaceuticals and medical instruments (p. 7), that the effect of
patents on the location rather than the amount of innovation is unknown (p. 3), and that strengthening IP raises
foreign direct investment in countries with weak regimes, which they treat as irrelevant to innovation (p. 15).

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| Patents issued, 1983 | 59,715 patents | WP p. 6, "Arms Races and Patent Trolls" | Annual US grants | The current USPTO table gives 61,982 total grants for 1983, so the figure appears to come from an earlier vintage or a narrower count; the source is not named |
| Applications, 1983 | 105,704 applications | WP p. 6 | Annual US applications | Current table gives 112,040; same caveat |
| Patents issued, 2003 | 189,597 patents | WP p. 6 | Annual US grants | Current table gives 187,012 |
| Applications, 2003 | 355,418 applications | WP p. 6 | Annual US applications | Current table gives 366,043 |
| Patents issued, 2010 | 244,341 patents | WP p. 6 | Annual US grants | Matches the current USPTO total exactly; says nothing about the quality or use of the patents |
| Growth of patent flow | "roughly quadrupled" in under 30 years | WP p. 6 | Ratio 2010/1983, which is 4.09 on the paper's numbers | That TFP or R&D lacked a trend; no TFP or R&D series is shown in the working paper |
| Applications in the 1990s | about 345,000 by the end of the 1990s, from about 90,000 in the 1960s; up 50% from 1997 to 2001 | Book, Chapter 4, p. 78 | Growth of applications | The source of the counts is not given in the passage read |
| TFP trend | No strong trend over 50 years; rise in the 1950s and 1960s, fall to the late 1980s or early 1990s, slight recovery in 1995–2000 | Book, Chapter 4, p. 79 | Verbal description of TFP growth | No series, source or test is given |
| Metastudy | 24 studies, "weak or no evidence" that stronger patents raise innovation | WP p. 15 | Summary of prior literature | Weighting, quality assessment or search method; vote counting cannot measure effect size |
| Elasticity of R&D share to GDP | 0.34 | WP p. 16 | OLS slope in 31-country data, 1981–1990 | Standard error and sample details are not shown |
| Mean R&D residual by IP level | −0.95, −0.46, 0.20, 0.20, 0.10 for levels 0 to 4 | WP p. 16, table | Non-monotone relation between IP protection and residual R&D | Counts per cell, dispersion, or significance |
| Sector-level correlation of patents and productivity | Not significant except two specifications with "very small" positive coefficients | WP pp. 16–17, citing Boldrin, Correa, Levine and Ornaghi (2011) | Correlation of patent counts or citations with labor productivity or TFP across sectors | Coefficients, standard errors and sample sizes are not reported in this text |
| Competition and productivity | Up to 2% faster annual productivity growth in the most competitive sectors | WP p. 18 | Correlation of competition (inverse profitability) with productivity growth | Causality; the authors note profitability is endogenous |
| Cost of a patent application | about $40,000 | WP p. 7 | Private filing cost | Social cost of defensive patenting |

## Interpretation notes

- The aggregate claim is a statement about trends and is not accompanied by a figure, a test or a TFP source in the
  working paper. It is a reasonable descriptive claim, and this repository's rerun on BLS TFP data is consistent with
  it, but the paper itself provides no way to check it.
- Four of the five patent counts quoted differ from the current USPTO summary by between 1% and 6%, most likely a
  data-vintage issue rather than an error. The 2010 count matches exactly. None of the differences changes the
  "roughly quadrupled" conclusion.
- The step from "patent counts do not track productivity" to "patents do not increase innovation" requires that
  patent counts and TFP are adequate proxies for patent protection and innovation respectively. The authors argue
  this themselves when they say most patents are defensive, which makes the count a poor measure of protection as
  well as of ideas.
- The cross-sector evidence is reported from a companion paper and is described only verbally. A reader cannot judge
  magnitudes from this text.
- The policy conclusion (abolition through gradual shortening of the term) is argued, not estimated. The paper is
  explicit that the reform is reversible if it proves harmful.
- No published correction or comment documenting an analytical error was found in the material read. The limitations
  above are reporting limitations.

## Unanswered questions

- Which TFP series, vintage and period underlie the claim that productivity showed no upward trend?
- What is the source and vintage of the 1983 and 2003 patent counts?
- How would the aggregate comparison change if patents were weighted by value or citations rather than counted?
- Do the sector-level null results survive controls for industry and year effects, and what are their confidence
  intervals?
- How much of the post-1983 rise in patents reflects foreign applicants, whose inventions may raise productivity
  outside the United States?

## Items requiring expert verification

- Whether the JEP version contains a figure or table on patents and productivity not present in the working paper.
- Whether the JEP text keeps the working paper's patent counts and its statement on R&D and productivity trends word
  for word; all page numbers above are the working paper's printed pages and were not checked against the journal.
- The exact coefficients and standard errors in Boldrin, Correa, Levine and Ornaghi (2011).
- Whether the metastudy's 24 studies are listed in the book, and how each was classified.
- Whether the 31-country data and IP index are those of Anwar and Evenson as published.

This repository does not reproduce the paper's results, which rest on sources it does not report in full. It reruns
the aggregate comparison on current USPTO, PatentsView and BLS data through 2025 and adds a value-weighted counter-test.
