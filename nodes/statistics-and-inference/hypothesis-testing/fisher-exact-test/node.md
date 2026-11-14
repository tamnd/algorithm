---
tag: PNP35A
kind: algorithm
slug: fisher-exact-test
name: Fisher's exact test
aliases:
- Fisher-Irwin test
area: statistics-and-inference/hypothesis-testing
level: core
summary: Tests independence in a 2 x 2 table exactly, from the hypergeometric distribution of one cell given the margins. It stays valid for small counts.
model: real-ram
complexity:
  vars: {n: the total count, m: the number of tables with the observed margins (at most n + 1)}
  time: {worst: Θ(n), best: Θ(m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1935
  people: [Ronald A. Fisher, J. O. Irwin, Frank Yates]
  note: Fisher described the test in 1934 and 1935, with the twins data and the lady tasting tea. Irwin (1935) and Yates (1934) gave the same test independently.
prereqs: [statistical-hypothesis-test, p-value, binomial-test]
see_also: [chi-squared-test-of-independence, mcnemar-test, permutation-test, test-interval-duality, binomial-coefficient-computation, karlin-rubin-theorem, logistic-regression, statistical-power]
sources:
  - paper: doi:10.2307/2342435
    title: R. A. Fisher, The logic of inductive inference, Journal of the Royal Statistical Society 98(1), 1935
    locator: pp. 39 to 82 (the exact test for a 2 x 2 table, with the data on convictions of twins)
  - book: isbn:9780470463635
    title: Alan Agresti, Categorical Data Analysis, third edition, Wiley, 2013
    locator: Chapter 3 (inference for two-way contingency tables, with small-sample tests of independence) and Chapter 16 (small-sample exact inference)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Chapter 4 (unbiased tests, with the comparison of two binomial populations by a conditional test)
---

Fisher's exact test checks whether two binary variables are independent, or whether two groups have the same success probability, from the four counts of a $2 \times 2$ table. It conditions on both row totals and both column totals. Given these margins, the whole table is fixed by its top-left cell, and under the null hypothesis that cell has a hypergeometric law that contains no unknown parameter. The p-value is a tail sum of that law, so the test is valid for every sample size, however small the counts. The code computes the hypergeometric weights as exact integers, so the p-values have no rounding error before the final division.

## In plain words

A lady says she can tell whether milk or tea went into the cup first. You give her 8 cups, 4 of each kind, and she must pick the 4 with milk first. If she is only guessing, every choice of 4 cups out of 8 is equally likely, and there are 70 such choices. Only one of them is fully correct. So if she gets all 4 right, the chance of doing that well by luck is $1/70$. Fisher's test does this counting for any $2 \times 2$ table: keep the row and column totals fixed, count how many ways each table can arise, and add up the share of tables that are at least as extreme as the one you saw.

## The problem

**Model.** A $2 \times 2$ table of counts

| | column 1 | column 2 | total |
|---|---|---|---|
| row 1 | $a$ | $b$ | $r_1$ |
| row 2 | $c$ | $d$ | $r_2$ |
| total | $c_1$ | $c_2$ | $n$ |

arises from two independent binomial rows ($r_1$ and $r_2$ fixed), from one multinomial sample ($n$ fixed), or from a design with both margins fixed.

**Hypotheses.** $H_0$: the rows have the same probability of column 1 (equivalently, the two variables are independent, or the odds ratio $\psi = \frac{p_1/(1 - p_1)}{p_2/(1 - p_2)}$ equals 1). Alternatives: $\psi > 1$ ("greater", large $a$), $\psi < 1$ ("less") or $\psi \neq 1$ (two-sided).

**Statistic.** The top-left count $a$.

**Null distribution.** Conditional and exact. Given all margins, $A$ takes the values $k$ from $k_{lo} = \max(0, c_1 - r_2)$ to $k_{hi} = \min(r_1, c_1)$ with

$$P(A = k \mid \text{margins}) = \frac{w(k)}{\binom{n}{c_1}}, \qquad w(k) = \binom{r_1}{k}\binom{r_2}{c_1 - k},$$

the hypergeometric law. The common success probability cancels, as the correctness proof shows.

**Rejection rule and size.** Reject when $p \le \alpha$. The conditional size is at most $\alpha$ for every set of margins, so the unconditional size is also at most $\alpha$. Because the conditional law is discrete, the size is usually well below $\alpha$; see Properties.

**P-values.** $P_{hi} = P(A \ge a)$ for "greater", $P_{lo} = P(A \le a)$ for "less", and for the two-sided test the minimum-likelihood rule $p_{ml} = \sum_{k : w(k) \le w(a)} w(k)/\binom{n}{c_1}$, the total probability of the tables that are at most as likely as the observed one. This is the rule of R's `fisher.test` and of the code. Doubling the smaller tail is the other common rule; it can differ.

**Sensitivity and power.** Under the alternative the conditional law is $w(k)\psi^k/\sum_j w(j)\psi^j$, which depends only on the odds ratio. The one-sided test is the uniformly most powerful conditional test, but the conditioning costs power against the unconditional alternatives; see Properties.

## The algorithm

```pseudo id=main
FISHER-EXACT(a, b, c, d, alternative)
L1  r1 ← a + b;  r2 ← c + d;  c1 ← a + c;  lo ← max(0, c1 - r2);  hi ← min(r1, c1)
L2  w[lo] ← C(r1, lo) · C(r2, c1 - lo)
L3  for k ← lo to hi - 1
L4      w[k + 1] ← w[k] · (r1 - k)(c1 - k) / ((k + 1)(r2 - c1 + k + 1))   ▷ exact integer division
L5  N ← w[lo] + ... + w[hi]                                          ▷ equals C(n, c1)
L6  if alternative = greater then return (w[a] + ... + w[hi]) / N
L7  if alternative = less then return (w[lo] + ... + w[a]) / N
L8  return (sum of w[k] over all k with w[k] ≤ w[a]) / N
```

All values in lines L2 to L8 are exact integers. Line L4 uses the ratio of consecutive terms, so the loop needs one multiplication and one division per table instead of two binomial coefficients. The comparison in line L8 is exact, so two tables with equal probability are always treated as tied; floating-point code needs a tolerance here, as the [binomial test](/binomial-test/) does. The code returns the `Fraction` on request, or the correctly rounded float of it.

## Example

**The lady tasting tea.** Table $\begin{pmatrix} 4 & 0 \\ 0 & 4 \end{pmatrix}$: rows are the true kind of cup, columns are her answer. The margins are all 4, so $k$ runs from 0 to 4 with weights $w = (1, 16, 36, 16, 1)$, total $70 = \binom{8}{4}$. Line L4 gives them in turn: $w(1) = 1 \cdot 4 \cdot 4/(1 \cdot 1) = 16$, $w(2) = 16 \cdot 3 \cdot 3/(2 \cdot 2) = 36$, and so on. The one-sided p-value is $P(A \ge 4) = 1/70 = 0.0143$. The two-sided value is $2/70 = 1/35 = 0.0286$. With 3 of 4 right, the one-sided value would be $17/70 = 0.243$: the design cannot reach significance unless she is perfect.

**Convictions of twins (Fisher 1935).** Of 13 monozygotic twins of convicted criminals, 10 had a twin who was also convicted; of 17 dizygotic twins, 2 had. The table is $\begin{pmatrix} 10 & 3 \\ 2 & 15 \end{pmatrix}$ with $r_1 = 13$, $r_2 = 17$, $c_1 = 12$, $n = 30$. The weights for $k = 0, \ldots, 12$ are

6188, 160888, 1516944, 6952660, 17381650, 25029576, 21237216, 10618608, 3063060, 486200, 38896, 1326, 13,

with total $\binom{30}{12} = 86493225$. So $P_{hi} = (38896 + 1326 + 13)/86493225 = 619/1330665 = 0.000465$, which is about $1/2150$. The two-sided minimum-likelihood value adds the tables with weight at most 38896, which are $k = 0$ (6188) on the other side, so $p_{ml} = 46423/86493225 = 3571/6653325 = 0.000537$. Doubling would give $0.000930$.

**A one-sided result that is not two-sided.** For $\begin{pmatrix} 7 & 2 \\ 3 & 8 \end{pmatrix}$, $P_{hi} = 293/8398 = 0.0349$ and $p_{ml} = 293/4199 = 0.0698$. At $\alpha = 0.05$ only the one-sided test rejects; choose the alternative before seeing the data.

**Against the chi-squared test.** For $\begin{pmatrix} 12 & 5 \\ 7 & 16 \end{pmatrix}$, $n = 40$, Fisher's two-sided p-value is $0.02384$ and the one-sided one is $0.01357$. The [chi-squared test of independence](/chi-squared-test-of-independence/) gives $X^2 = 6.3199$ and $p = 0.01194$; with Yates's continuity correction, $X^2 = 4.8123$ and $p = 0.02826$, closer to Fisher's value.

All the fractions above are computed exactly by the code, and the tests check them.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). In each sampling model, the joint law of the table under $H_0$ is $w(k)$ times a factor that depends only on the margins, so conditioning on the margins leaves $w(k)/\binom{n}{c_1}$ (Vandermonde's identity gives the total). Line L4 is exact because $w(k)(r_1 - k)(c_1 - k) = w(k + 1)(k + 1)(r_2 - c_1 + k + 1)$ is an identity of integers. Each p-value is a tail $P(T(A) \ge T(a))$ of a finite law, so the lemma on the binomial test page gives conditional validity, and averaging over the margins gives unconditional validity.

## Complexity

Line L2 takes $O(n)$ arithmetic operations, and lines L3 to L8 take $\Theta(m)$, where $m = k_{hi} - k_{lo} + 1 \le n + 1$ is the number of tables with the observed margins. So the count of operations is $O(n)$ and the extra space is $\Theta(m)$ integers. Each weight is below $2^n$, so on a machine with fixed-size words every operation on a weight costs $O(n)$ bit operations, and the total is $O(n^2)$ bit operations. For $n$ in the thousands this is still fast; the tests run a table with $n = 1000$ in exact arithmetic. A floating-point version with $\log$ weights from $\operatorname{lgamma}$ costs $\Theta(m)$ operations but needs a tolerance in line L8.

## Properties

- **Exact and conditional.** The size is at most $\alpha$ given every set of margins. The tests check this in exact arithmetic for all margins with $r_1, r_2 \le 10$.
- **Conservative unconditionally.** For two binomial rows of 10 trials with a common $p$, the two-sided test at $\alpha = 0.05$ rejects for 34 of the 121 possible tables, and its unconditional size, measured on a grid of $p$ with step 0.001, is at most $0.01278$, reached at $p = 0.5$. The one-sided test rejects 23 tables and has size at most $0.02110$. These are measured on the grid, not proved maxima.
- **Power.** The one-sided test is uniformly most powerful among conditional tests, by the Karlin-Rubin theorem applied to the conditional family $w(k)\psi^k$, and with randomization it is uniformly most powerful unbiased for $\psi$ (Lehmann and Romano, Chapter 4). Against two binomial rows it loses power to unconditional tests. For rows of 10, with $p_1 = 0.7$ and $p_2 = 0.2$, the one-sided Fisher test at $\alpha = 0.05$ has power $0.622$.
- **Symmetric in the roles of rows and columns.** Transposing the table, or swapping both rows and columns, does not change any p-value. Swapping only the rows exchanges "greater" and "less".
- **Inverting the test.** The conditional law $w(k)\psi^k$ also gives an exact confidence interval for the odds ratio, by [test-interval duality](/test-interval-duality/), and the conditional maximum likelihood estimate of $\psi$.

## Variants and improvements

- **Boschloo's test.** Use Fisher's p-value as the statistic, but find the cut-off from the unconditional law, maximized over the common $p$ (Boschloo 1970). It is never less powerful than Fisher's test. For rows of 10 and the one-sided test at $\alpha = 0.05$, the largest Fisher p-value cut-off whose size stayed below 0.05 on the grid was $0.0849$ (size $0.0447$), so the test rejects 27 tables instead of 23, and its power at $(0.7, 0.2)$ rises from $0.622$ to $0.733$; at $(0.6, 0.3)$ it rises from $0.247$ to $0.359$. These numbers are computed exactly per table and maximized over a grid of $p$.
- **Barnard's test.** An unconditional test that orders the tables by a statistic such as the pooled z statistic and maximizes the size over the nuisance $p$ (Barnard 1945). It is more powerful than Fisher's test in many cases, at a higher cost: a search over $p$ for every candidate table.
- **Mid-p value.** $P(A > a) + \tfrac12 P(A = a)$. For the twins it is $0.000240$. It is less conservative, but its size can exceed $\alpha$.
- **Larger tables.** The Freeman-Halton extension sums the multivariate hypergeometric probabilities of all $r \times c$ tables with the observed margins that are at most as likely as the observed one. The number of tables grows fast, and network algorithms or Monte Carlo sampling are used.
- **Stratified tables.** Several $2 \times 2$ tables with a common odds ratio are combined by conditioning on the margins of each; the exact conditional test and the Mantel-Haenszel test do this.
- **Paired data.** For matched pairs, use the [McNemar test](/mcnemar-test/) instead; Fisher's test assumes independent units.

## When to use it

Use it for a $2 \times 2$ table when some expected counts are small, so that the chi-squared approximation is doubtful, and in designs where both margins are fixed, such as the tea experiment, where it is exactly right. With large counts it agrees with the chi-squared test with continuity correction. When the two rows are independent binomial samples and power matters, an unconditional test such as Boschloo's is a better choice at the same guaranteed level. For an effect size, report the odds ratio with an exact or a likelihood interval.

## Pitfalls

- **Small size is not a guarantee of good power.** Because the test is conservative, a nominal 5% test can have actual size near 1% to 2%, and the sample size needed for a given power is larger than a calculation at size 5% suggests.
- **Which two-sided rule.** Software differs: R uses the minimum-likelihood rule with a relative tolerance on the probabilities; some packages double the one-sided value. For the twins the two rules give $0.000537$ and $0.000930$.
- **Floating-point ties.** A floating-point implementation can miss ties between tables with equal probability, which changes the two-sided p-value. Exact integer weights, as here, avoid this.
- **Dependence.** Paired or clustered units break the hypergeometric law. Use McNemar's test or a model for clusters.
- **The choice of one side after the fact.** As the second example shows, picking "greater" after seeing a large $a$ halves the p-value in effect.

## Implementations

## History

R. A. Fisher described the test in the fifth edition of *Statistical Methods for Research Workers* (1934) and in "The logic of inductive inference" (1935), where he analysed J. Lange's data on the convictions of twins of criminals. The lady tasting tea appears in *The Design of Experiments* (1935). J. O. Irwin (1935) and Frank Yates (1934), who also proposed the continuity correction for the chi-squared test, reached the same test independently. G. A. Barnard (1945) proposed an unconditional alternative and later withdrew his preference for it in favour of conditioning; R. D. Boschloo (1970) gave the raised conditional level that bears his name.

## References
