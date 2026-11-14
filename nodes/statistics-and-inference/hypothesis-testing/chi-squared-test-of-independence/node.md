---
tag: E5V169
kind: algorithm
slug: chi-squared-test-of-independence
name: Chi-squared test of independence
aliases:
- contingency table chi-squared test
- chi-squared test of association
area: statistics-and-inference/hypothesis-testing
level: intro
summary: Tests whether two categorical variables are independent by comparing a contingency table with the product of its margins, with (r - 1)(c - 1) degrees of freedom.
model: real-ram
complexity:
  vars: {r: the number of rows, c: the number of columns}
  time: {worst: Θ(r·c), best: Θ(r·c)}
  space: {extra: Θ(r·c)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1900
  people: [Karl Pearson, Ronald A. Fisher, Frank Yates, William G. Cochran]
  note: Pearson's 1900 statistic was applied to contingency tables by Pearson in 1904. Fisher gave the correct (r - 1)(c - 1) degrees of freedom in 1922. Yates added the continuity correction in 1934 and Cochran gave rules for small expected counts in 1954.
prereqs: [chi-squared-goodness-of-fit-test, statistical-hypothesis-test, p-value]
see_also: [fisher-exact-test, mcnemar-test, likelihood-ratio-test, wilks-theorem, permutation-test, logistic-regression, statistical-power, central-limit-theorem]
sources:
  - paper: doi:10.2307/2340521
    title: Ronald A. Fisher, On the interpretation of χ² from contingency tables, and the calculation of P, Journal of the Royal Statistical Society 85(1), 1922
    locator: pp. 87 to 94 (the degrees of freedom of a contingency table)
  - paper: doi:10.1080/14786440009463897
    title: Karl Pearson, On the criterion that a given system of deviations from the probable in the case of a correlated system of variables is such that it can be reasonably supposed to have arisen from random sampling, Philosophical Magazine, series 5, 50(302), 1900
    locator: pp. 157 to 175 (the statistic)
  - paper: doi:10.2307/3001616
    title: William G. Cochran, Some methods for strengthening the common χ² tests, Biometrics 10(4), 1954
    locator: the recommendations on the smallest expected counts
  - book: isbn:9780470463635
    title: Alan Agresti, Categorical Data Analysis, third edition, Wiley, 2013
    locator: Chapter 3 (inference for two-way contingency tables, with the sampling schemes and residuals)
---

The chi-squared test of independence checks whether two categorical variables are related, from an $r \times c$ table of counts. If the variables are independent, the count in cell $(i, j)$ should be close to $E_{ij} = R_i C_j/n$, the product of its row and column totals divided by the grand total. The test adds up $(O_{ij} - E_{ij})^2/E_{ij}$ over all cells. Under independence and for large samples this sum has approximately the chi-square law with $(r - 1)(c - 1)$ degrees of freedom.

## In plain words

Give 100 patients one of two treatments and record whether each one improved, stayed the same or got worse. If the treatment makes no difference, the share of patients who improved should be about the same in both groups, and also in the whole sample. So the overall shares tell you what each cell of the table should contain. The test measures how far the real table is from that "no difference" table. The degrees of freedom count how many cells you can fill in freely once the row and column totals are fixed: $(r - 1)(c - 1)$, which is 2 for a table with 2 rows and 3 columns.

## The problem

**Model.** Three sampling schemes give the same test:

1. $n$ units are sampled and classified by both variables; the table is multinomial.
2. The row totals are fixed by design, as in a trial with set group sizes; each row is an independent multinomial sample.
3. Both margins are fixed, as in Fisher's tea tasting experiment; the table is multiple hypergeometric under the null.

**Hypotheses.** $H_0$: independence, $\pi_{ij} = \pi_{i+} \pi_{+j}$ in scheme 1, or equal row distributions (homogeneity) in scheme 2. $H_1$: any other table of probabilities. There is no direction.

**Statistic.**

$$X^2 = \sum_{i = 1}^r \sum_{j = 1}^c \frac{(O_{ij} - E_{ij})^2}{E_{ij}}, \qquad E_{ij} = \frac{R_i C_j}{n}.$$

The likelihood-ratio form is $G = 2 \sum_{ij} O_{ij} \log(O_{ij}/E_{ij})$. For a $2 \times 2$ table, Yates's corrected statistic subtracts $1/2$ from each $\lvert O_{ij} - E_{ij} \rvert$ (but not below 0).

**Null distribution.** Asymptotic: $X^2$ tends to $\chi^2_{(r - 1)(c - 1)}$. The table has $rc - 1$ free cell probabilities, and the null fits $(r - 1) + (c - 1)$ of them from the margins, which leaves $rc - 1 - (r - 1) - (c - 1) = (r - 1)(c - 1)$.

**Rejection rule and size.** Reject when $p \le \alpha$, that is when $X^2 \ge \chi^2_{((r - 1)(c - 1),\ 1 - \alpha)}$. The size tends to $\alpha$ (proved for scheme 1). For finite $n$ it is not controlled. The exact computations below show sizes close to $\alpha$ even with small expected counts, and show that Yates's correction is very conservative.

**P-values.** $p = P(\chi^2_{(r - 1)(c - 1)} > X^2)$, the upper tail only.

**Sensitivity and power.** For a fixed dependent table the power tends to 1. For alternatives near independence, $X^2$ is approximately noncentral chi-square with noncentrality $n \sum_{ij} (\pi_{ij} - \pi_{i+}\pi_{+j})^2/(\pi_{i+}\pi_{+j})$. As with the goodness-of-fit test, the power is spread over all directions, so for ordered categories a trend test is more powerful against a trend.

## The algorithm

```pseudo id=main
CHI-SQUARED-INDEPENDENCE(O[1..r][1..c])
L1  R[i] ← row totals;  C[j] ← column totals;  n ← total     ▷ every R[i] and C[j] must be positive
L2  for i ← 1 to r, j ← 1 to c do
L3      E ← R[i] · C[j] / n
L4      add (O[i][j] - E)^2 / E to the sum                      ▷ or 2 O log(O / E); Yates: (max(0, |O - E| - 1/2))^2 / E
L5  X2 ← the sum
L6  df ← (r - 1)(c - 1)
L7  return (X2, df, P(χ²_df > X2))
```

Line L7 uses `chi2_sf` from the shared helper module. The code raises an error for a table with an empty row or column, because then some $E_{ij}$ is 0; such a row or column carries no information about the association, and dropping it gives the right table.

## Example

**Treatment and outcome.** One hundred patients get treatment A (40) or B (60). The outcomes are:

| | improved | same | worse | total |
|---|---|---|---|---|
| A | 20 | 15 | 5 | 40 |
| B | 10 | 20 | 30 | 60 |
| total | 30 | 35 | 35 | 100 |

The expected counts are $E_{11} = 40 \cdot 30/100 = 12$, and in full

| | improved | same | worse |
|---|---|---|---|
| A | 12 | 14 | 14 |
| B | 18 | 21 | 21 |

The cell terms are $64/12 = 5.333$, $1/14 = 0.071$ and $81/14 = 5.786$ for A, and $64/18 = 3.556$, $1/21 = 0.048$ and $81/21 = 3.857$ for B. So $X^2 = 1175/63 = 18.651$ on $(2 - 1)(3 - 1) = 2$ degrees of freedom, and $p = 8.91 \times 10^{-5}$. The likelihood-ratio form gives $G = 19.900$ and $p = 4.77 \times 10^{-5}$. The adjusted residuals $(O_{ij} - E_{ij})/\sqrt{E_{ij}(1 - R_i/n)(1 - C_j/n)}$ are $3.56$, $0.43$ and $-3.85$ for row A, so the association is in the "improved" and "worse" columns: A patients improved more often and got worse less often.

**A 2 x 2 table.** With rows $(12, 5)$ and $(7, 16)$, $n = 40$:

- $X^2 = 40(12 \cdot 16 - 5 \cdot 7)^2/(17 \cdot 23 \cdot 19 \cdot 21) = 6.320$ and $p = 0.0119$.
- This is $z^2$ for the two-proportion comparison $12/17 = 0.706$ against $7/23 = 0.304$.
- With Yates's correction, $X^2 = 4.812$ and $p = 0.0283$.
- The two-sided [Fisher exact test](/fisher-exact-test/) gives $p = 0.0238$.

The tests check these numbers, and check $X^2$ against exact rational arithmetic for 300 random tables of up to $5 \times 5$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The expected counts $R_i C_j/n$ are the maximum likelihood fit of the independence model, so this is a [goodness-of-fit test](/chi-squared-goodness-of-fit-test/) with $(r - 1) + (c - 1)$ fitted parameters. The proof writes the residual matrix $V_{ij} = (O_{ij} - E_{ij})/\sqrt{n \pi_{i+} \pi_{+j}}$ as a fixed linear map of the standardized counts plus a term that tends to 0. In the limit the linear map becomes $Z \mapsto Q_\alpha Z Q_\beta$, where $Z$ is a matrix of independent standard normals and $Q_\alpha$ and $Q_\beta$ project out the square roots of the row and column probabilities. This is an orthogonal projection of rank $(r - 1)(c - 1)$, so $X^2 = \lVert V \rVert^2 + o_P(1)$ tends to $\chi^2_{(r - 1)(c - 1)}$. For the $2 \times 2$ table every cell has $\lvert O_{ij} - E_{ij} \rvert = \lvert ad - bc \rvert/n$, which gives the closed form above.

## Complexity

The margins take $\Theta(rc)$ additions and the statistic takes $\Theta(1)$ work per cell, so the time is $\Theta(rc)$. The code keeps the $rc$ terms for an exactly rounded sum, so it uses $\Theta(rc)$ extra space; a running sum needs only $\Theta(r + c)$ for the margins. The p-value is one incomplete gamma evaluation.

## Properties

- **Size for small samples (computed exactly).** Under multinomial sampling with independent variables, summing over all tables gives the true size at $\alpha = 0.05$. A table with an empty row or column has no test and counts as not rejected.

  | table | $n$ | margins | smallest expected count | size of $X^2$ | size with Yates |
  |---|---|---|---|---|---|
  | $2 \times 2$ | 20 | $(0.5, 0.5)$ and $(0.5, 0.5)$ | 5 | 0.0512 | 0.0128 |
  | $2 \times 2$ | 40 | $(0.5, 0.5)$ and $(0.5, 0.5)$ | 10 | 0.0508 | 0.0206 |
  | $2 \times 2$ | 40 | $(0.8, 0.2)$ and $(0.8, 0.2)$ | 1.6 | 0.0417 | |
  | $2 \times 3$ | 15 | $(0.4, 0.6)$ and $(0.2, 0.3, 0.5)$ | 1.2 | 0.0420 | |

  The tests compute these values and check the last one against a simulation (seed 6, 20000 tables).
- **Yates's correction is conservative.** It brings the statistic close to the conditional exact test, which is itself conservative under multinomial sampling, so it loses power. Many authors now advise against it.
- **Symmetric.** Transposing the table, or permuting its rows or columns, does not change $X^2$.
- **Scales with $n$.** Multiplying every count by $m$ multiplies $X^2$ by $m$. So $X^2$ measures evidence, not the strength of the association. Cramér's $V = \sqrt{X^2/(n \min(r - 1, c - 1))}$ is a measure of strength; it is $0.432$ in the treatment example.
- **The 2 x 2 test is the two-proportion z test.** $X^2 = z^2$ for the pooled two-proportion statistic, so the two-sided tests are the same.

## Variants and improvements

- **Fisher's exact test.** For a $2 \times 2$ table with small counts, the [Fisher exact test](/fisher-exact-test/) conditions on both margins and has size at most $\alpha$. The Freeman-Halton extension does the same for $r \times c$ tables.
- **Monte Carlo and permutation p-values.** Fix both margins, draw random tables with those margins (by permuting one variable against the other), and compare $X^2$ with the simulated values, as in a [permutation test](/permutation-test/).
- **Likelihood-ratio statistic $G$.** The code computes it with `statistic="g"`. It splits into parts for nested tables, which is the basis of log-linear models.
- **Ordered categories.** The Cochran-Armitage trend test and the linear-by-linear association test use one degree of freedom and have more power against a trend.
- **Stratified tables.** With a third variable, the Cochran-Mantel-Haenszel test combines $2 \times 2$ tables across strata.
- **Paired data.** For the same units measured twice, use [McNemar's test](/mcnemar-test/), not this test.

## When to use it

Use it to test association between two unordered categorical variables from independent units, when most expected counts are not tiny. Cochran's rule (no expected count below 1, and at most 20% of them below 5) is a common guide, and the exact sizes above show that the Pearson statistic does well even near those limits. For $2 \times 2$ tables with small counts, or whenever an exact level is needed, use Fisher's exact test or a Monte Carlo p-value.

## Pitfalls

- **Units that are not independent.** Repeated measurements on the same subjects, or several answers from one person, break the multinomial model. For two measurements on the same units, use McNemar's test.
- **Percentages instead of counts.** The test needs counts. Percentages change $n$.
- **Reading $X^2$ or $p$ as the strength of the association.** A tiny p-value with a large $n$ can come from a very weak association. Report a measure such as a difference of proportions, an odds ratio or Cramér's $V$.
- **Merging categories after seeing the data.** Choosing which cells to combine to get significance changes the null law.
- **Simpson's paradox.** An association in the combined table can reverse inside each level of a third variable. Stratify when a confounder is known.
- **Expecting the test to say which cells matter.** A significant result says only that the table is not independent. Look at the adjusted residuals.

## Implementations

## History

Karl Pearson published the $X^2$ statistic in 1900 and applied it to contingency tables in 1904. He used $rc - 1$ degrees of freedom. In 1922 Ronald Fisher showed that the expected counts use the margins, which removes $(r - 1) + (c - 1)$ degrees of freedom and leaves $(r - 1)(c - 1)$; Pearson did not accept this at first. Frank Yates (1934) proposed the continuity correction for $2 \times 2$ tables, and Fisher (1935) gave the exact conditional test. William Cochran (1952, 1954) reviewed the test and gave the rules for small expected counts that are still in common use.

## References
