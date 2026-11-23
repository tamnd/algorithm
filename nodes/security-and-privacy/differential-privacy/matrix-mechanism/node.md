---
tag: 73DA32
kind: algorithm
slug: matrix-mechanism
name: Matrix mechanism
aliases:
- strategy matrix mechanism
area: security-and-privacy/differential-privacy
level: research
summary: Answers a workload of linear queries by adding Laplace noise to a chosen strategy set of queries and then deriving the workload answers by least squares.
model: real-ram
complexity:
  vars: {n: the number of cells, p: the number of strategy queries, m: the number of workload queries}
  time: {worst: "O(p n^2 + n^3 + m n)"}
  space: {extra: "O(p n + m n)"}
history:
  year: 2010
  people: [Chao Li, Michael Hay, Vibhor Rastogi, Gerome Miklau, Andrew McGregor]
  note: Li, Hay, Rastogi, Miklau and McGregor gave the mechanism at PODS 2010. It unified the hierarchical and wavelet methods of the same year.
prereqs: [differential-privacy-definition, laplace-mechanism, pseudoinverse, least-squares-problem]
see_also: [binary-tree-mechanism, private-query-release, gaussian-mechanism, normal-equations, histogram, prefix-sums, mwem, post-processing-theorem]
sources:
  - paper: "Chao Li, Michael Hay, Vibhor Rastogi, Gerome Miklau and Andrew McGregor, Optimizing linear counting queries under differential privacy, PODS 2010"
    locator: the definition of the matrix mechanism, its error formula, and the search for good strategies
  - paper: "Chao Li, Gerome Miklau, Michael Hay, Andrew McGregor and Vibhor Rastogi, The matrix mechanism, optimizing linear counting queries under differential privacy, The VLDB Journal, 2015"
    locator: the journal version, with the (epsilon, delta) form
  - paper: "Michael Hay, Vibhor Rastogi, Gerome Miklau and Dan Suciu, Boosting the accuracy of differentially private histograms through consistency, PVLDB 3(1), 2010"
    locator: the hierarchical strategy for range queries and the least squares step
  - paper: "Xiaokui Xiao, Guozhang Wang and Johannes Gehrke, Differential privacy via wavelet transforms, ICDE 2010"
    locator: the wavelet strategy for range queries
  - paper: "Ryan McKenna, Gerome Miklau, Michael Hay and Ashwin Machanavajjhala, Optimizing error of high-dimensional statistical queries under differential privacy, PVLDB 2018"
    locator: HDMM, the search for strategies over data with many attributes
  - paper: "Ilya Mironov, On significance of the least significant bits for differential privacy, ACM CCS 2012"
    locator: the attack on floating-point Laplace noise and the snapping defense
---

The matrix mechanism answers a set of linear queries on a histogram, such as all range counts, by a detour. It picks a second set of linear queries, the strategy, and answers those with the [Laplace mechanism](/laplace-mechanism/). Then it finds the [least squares](/least-squares-problem/) estimate of the histogram from the noisy strategy answers, and computes the wanted queries from that estimate. The choice of strategy changes the error, often by a large factor, and the privacy cost stays $\varepsilon$. The identity strategy, the [binary tree](/binary-tree-mechanism/) of ranges and wavelets are all special cases, and the mechanism gives one formula to compare them.

## In plain words

You must publish many totals from one table of counts, for example the number of people in every age range. Many of the totals overlap, so each person affects many of them, and noise on each total must be large.

The matrix mechanism asks a different set of questions first. It picks them so that each person affects few of them, and so that the wanted totals can be built from them. It adds noise to those answers. Then it finds the table of counts that best fits the noisy answers, and computes all the wanted totals from that table. A good choice of the first questions gives much less noise in the totals.

## The problem

The data is a histogram $x \in \mathbb{N}^n$: $x_j$ is the number of records in cell $j$. The workload is an $m \times n$ matrix $W$, and the goal is to release an estimate of $W x$. Two histograms are neighbors if one is the other with one record added or removed: $x' = x \pm e_j$. The release must be $\varepsilon$-DP, and the goal is a small expected total squared error $\mathbb{E}\|\hat w - W x\|_2^2$.

A strategy is a $p \times n$ matrix $A$ of full column rank. Its sensitivity $\Delta_A$ is the largest $\ell_1$ norm of a column of $A$, because a change in cell $j$ moves $A x$ by the column $A e_j$.

$\mathrm{Lap}(b)$ is the Laplace distribution with density $\frac{1}{2b} e^{-|z|/b}$. It has variance $2b^2$, and $P(|Z| > t) = e^{-t/b}$.

## The algorithm

```pseudo id=main
MATRIX-MECHANISM(W, A, x, ε)
L1  Δ_A ← max over columns j of Σᵢ |Aᵢⱼ|          ▷ the l1 sensitivity of x ↦ Ax
L2  y ← A x + z, with zᵢ ~ Lap(Δ_A/ε) independent  ▷ the Laplace mechanism on the strategy
L3  A⁺ ← (AᵀA)⁻¹ Aᵀ                               ▷ the pseudoinverse
L4  x̂ ← A⁺ y                                       ▷ the least squares estimate of x
L5  output W x̂
```

Line L2 is the only step that reads the data. Lines L3 to L5 are post-processing, so they cost no privacy. Line L4 picks the $\hat x$ that minimizes $\|A \hat x - y\|_2$, which also makes the answers consistent: they all come from one histogram. The [pseudoinverse](/pseudoinverse/) in line L3 can be computed by the [normal equations](/normal-equations/) as written, or more stably by a [QR decomposition](/qr-decomposition/).

## Example

Take $n = 4$ cells with $x = (3, 0, 5, 2)$ and $\varepsilon = 1$. The workload $W$ is all 10 range queries $x_i + \cdots + x_j$. The table compares three strategies by the error formula of the Correctness section. The values are exact and the test file checks them.

| strategy $A$ | rows $p$ | $\Delta_A$ | total squared error over the 10 ranges |
|---|---|---|---|
| identity: one count per cell | 4 | 1 | 40 |
| hierarchical: the cells, the two halves and the total | 7 | 3 | $876/7 \approx 125.1$ |
| the workload itself | 10 | 6 | 288 |

Answering the 10 ranges directly is the worst choice, because a middle cell lies in 6 of them. At this small $n$ the identity is the best of the three. The run of the code with the hierarchical strategy and `random.Random(1)` draws the noisy strategy answers $y = (-0.94, 3.56, 7.25, -0.02, 2.97, 6.68, 11.08)$ for the true answers $(3, 0, 5, 2, 3, 7, 10)$. Least squares gives $\hat x = (-0.63, 3.87, 7.26, -0.01)$, and the 10 range answers follow from $\hat x$.

The hierarchical strategy wins for large $n$: its error for one range grows as $(\log n)^3$ (a theorem, from the [binary tree](/binary-tree-mechanism/) bound), and the error of the identity grows as $n$. The crossover is late. At $n = 64$ the code gives a total error of 91520 for the identity and about 264672 for the hierarchical strategy (a measurement).

## Correctness

**Privacy (a theorem).** For neighbors $x' = x \pm e_j$, $\|A x - A x'\|_1$ is the $\ell_1$ norm of column $j$, at most $\Delta_A$. So line L2 is the Laplace mechanism with the right scale, and $y$ is $\varepsilon$-DP. Lines L3 to L5 do not read $x$, so the output is $\varepsilon$-DP by [post-processing](/post-processing-theorem/).

**Unbiased (a theorem).** $A^+ A = I$ for a strategy of full column rank, so $\mathbb{E}[W \hat x] = W x$.

**Error (a theorem, Li et al. 2010).** The expected total squared error is

$$\frac{2\Delta_A^2}{\varepsilon^2} \operatorname{tr}\big(W (A^\top A)^{-1} W^\top\big).$$

The key step is $A^+ (A^+)^\top = (A^\top A)^{-1}$. For a fixed $A$, least squares is the best linear reconstruction, by the Gauss-Markov argument. The full proofs are in proofs/correctness.md.

## Complexity

In the [real-RAM model](/real-ram/) with one Laplace draw at unit cost:

- Line L2 costs $O(pn)$ and $p$ draws.
- Line L3 costs $O(pn^2 + n^3)$: it forms $A^\top A$ and inverts it.
- Line L5 costs $O(mn)$.
- The space is $O(pn + mn)$ for the matrices.

Lines L1 and L3 do not depend on the data. For a fixed strategy they can be done one time and reused. The hard part in practice is not the mechanism but the choice of $A$: the search for the best strategy is an optimization over matrices, and it is much more costly than one run.

## Properties

- **Pure DP.** With Laplace noise the output is $(\varepsilon, 0)$-DP.
- **Unbiased and consistent.** The answers are unbiased, and they all come from one estimate $\hat x$, so overlapping answers agree.
- **Data independent.** The error depends on $W$, $A$ and $\varepsilon$, not on $x$. So the error can be computed and compared before any data is touched.
- **Linear queries only.** The workload must be linear in the histogram.
- **Negative estimates.** The estimate $\hat x$ can have negative cells, as in the example. Rounding or clipping it is post-processing, so it is still private, but it breaks the unbiased property.

## Variants and improvements

- **Gaussian noise.** For $(\varepsilon, \delta)$-DP, use the [Gaussian mechanism](/gaussian-mechanism/) in line L2. The sensitivity becomes the largest $\ell_2$ norm of a column, and the error has the same form with the Gaussian variance.
- **Strategy search.** Li et al. give methods to search for a good $A$ for a given $W$. HDMM (McKenna, Miklau, Hay and Machanavajjhala 2018) searches over strategies with a product structure, which scales to data with many attributes.
- **Known strategies.** The identity, the hierarchical strategy of Hay, Rastogi, Miklau and Suciu (2010) and the wavelet strategy of Xiao, Wang and Gehrke (2010) are all instances. The binary tree mechanism for continual counting is the hierarchical strategy run online.
- **Factorization mechanisms.** In general any factorization $W = B A$ gives the release $B(Ax + z)$. The matrix mechanism takes $B = W A^+$, the best $B$ for a given $A$. Later work on prefix sums and on private training searches over such factorizations directly.
- **Adaptive data methods.** Methods that adapt the strategy to the data, such as [MWEM](/mwem/), can do better on some data, but their error is no longer data independent.

## When to use it

Use the matrix mechanism when the workload is a fixed, known set of linear queries on a histogram of moderate size, such as range queries, marginals of a few attributes, or the cells of a census table. It is best when many queries overlap, so that a good strategy shares the noise. For one query, or for queries on disjoint cells, the plain Laplace mechanism is already best. For a very large or unknown workload, see [private query release](/private-query-release/).

## Pitfalls

- **Sensitivity of the wrong matrix.** Line L1 must use the strategy $A$, not the workload $W$. The noise is added to $A x$, so its scale is set by the columns of $A$. Using $\Delta_W$ is wrong in both directions: it gives too much noise when $\Delta_W > \Delta_A$, and a privacy failure when $\Delta_W < \Delta_A$.
- **Row norms in place of column norms.** The sensitivity in line L1 is the largest column norm, because one record changes one cell. The largest row norm measures the size of one query, not the effect of one record. For the hierarchical strategy on $n$ cells it is $n$, while $\Delta_A = \log_2 n + 1$, and for a strategy with one long column it is smaller than $\Delta_A$.
- **A strategy without full column rank.** Line L3 needs $A^\top A$ to be invertible. If $A$ does not have full column rank, some queries of $W$ cannot be built from $A$. The code raises an error.
- **Unstable algebra.** For large or badly conditioned $A$, the normal equations in line L3 lose precision. Use a QR or [Cholesky](/cholesky-decomposition/) solve. The privacy proof does not depend on how line L3 is computed, but the error formula does.
- **Float noise.** The code uses float Laplace noise from `random.Random`, for tests only. A deployment needs a cryptographic source of randomness and exact sampling (Mironov 2012; Canonne, Kamath and Steinke 2020); see the [discrete Gaussian mechanism](/discrete-gaussian-mechanism/).

## Implementations

## History

In 2010 two groups gave strategies for range queries that beat noise on each cell: Hay, Rastogi, Miklau and Suciu with a hierarchy of intervals and a least squares step, and Xiao, Wang and Gehrke with wavelets. Li, Hay, Rastogi, Miklau and McGregor (PODS 2010) showed that both are instances of one mechanism, gave its error formula, and studied the search for the best strategy. The journal version appeared in The VLDB Journal in 2015. HDMM (2018) made the strategy search practical for data with many attributes.

## References
