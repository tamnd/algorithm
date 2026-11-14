---
tag: WNY22A
kind: algorithm
slug: knockoff-filter
name: Knockoff filter
aliases:
- model-X knockoffs
- Barber-Candes knockoffs
area: statistics-and-inference/hypothesis-testing
level: research
summary: Build copies of the features that keep their correlations but not their link to the response, and select features that beat their copies. Knockoff+ keeps the FDR at most q in finite samples.
model: real-ram
complexity:
  vars: {n: the number of observations, p: the number of features, S: the number of Jacobi sweeps}
  time: {construction: Θ(n p² + S p³), filter: Θ(n p + p log p)}
  space: {extra: Θ(n p)}
properties: {deterministic: false, randomized: true, exact: false, online: false, recursive: false}
history:
  year: 2015
  people: [Rina Foygel Barber, Emmanuel J. Candès]
  note: Barber and Candès introduced fixed-X knockoffs in the Annals of Statistics in 2015. Candès, Fan, Janson and Lv extended them to model-X knockoffs for random features in 2018.
prereqs: [false-discovery-rate, linear-regression, lasso-regression]
see_also: [benjamini-hochberg-procedure, storey-q-value, multiple-comparisons-problem, post-selection-inference, feature-selection, jacobi-eigenvalue-algorithm, gram-schmidt-process, optional-stopping-theorem]
sources:
  - paper: doi:10.1214/15-AOS1337
    title: Rina Foygel Barber and Emmanuel J. Candès, Controlling the false discovery rate via knockoffs, Annals of Statistics 43(5) (2015), pages 2055 to 2085
    locator: Definitions 1 and 2 (the knockoff and knockoff+ thresholds), Theorems 1 and 2 (modified FDR and FDR control), Section 2.1 (construction and the equicorrelated choice), Section 2.2 (sufficiency, antisymmetry and example statistics), Lemmas 1 to 3 in Section 2.3 (i.i.d. signs for the nulls)
  - paper: doi:10.1111/rssb.12265
    title: Emmanuel Candès, Yingying Fan, Lucas Janson and Jinchi Lv, Panning for gold, model-X knockoffs for high dimensional controlled variable selection, Journal of the Royal Statistical Society Series B 80(3) (2018), pages 551 to 577
    locator: model-X knockoffs for a known distribution of the features, with FDR control of knockoff+ for any n and p, and the Gaussian construction
---

The knockoff filter selects features in a linear regression $y = X\beta + z$ and controls the [false discovery rate](/false-discovery-rate/) of the selected set, the expected share of selected features $j$ with $\beta_j = 0$. It does not use p-values. For each feature $X_j$ it builds a knockoff $\tilde X_j$, a fake feature with the same correlations to the other features as $X_j$ but known to have no effect on $y$. It then computes a statistic $W_j$ for each pair, large and positive when $X_j$ explains $y$ better than its knockoff, and with a sign that is a fair coin when $\beta_j = 0$. The negative $W_j$ estimate how many null features pass any positive threshold, and the filter takes the lowest threshold $T$ at which the estimated FDR is at most $q$. The version called knockoff+ adds 1 to the count of negatives and has $\text{FDR} \le q$ in finite samples. The plain version controls only a modified FDR.

## In plain words

You want to find which of many measured factors really affect an outcome, and you accept a set share of false finds. For each factor, make a fake twin: a made-up factor that is related to the other factors in the same way as the real one, but that cannot affect the outcome. Then let each real factor compete with its twin. A useless factor wins or loses at random, like a coin toss. A useful factor usually wins by a wide margin. Count how many twins win by a wide margin. That count tells you about how many useless factors also won by a wide margin by luck. Keep the factors that won by a margin large enough that this estimate of false finds stays below your limit.

## The problem

**Input.** A design $X \in \mathbb R^{n \times p}$ with $n \ge 2p$ and full column rank, a response $y \in \mathbb R^n$, and a target $q \in (0, 1]$. The model is $y = X\beta + z$ with $z \sim N(0, \sigma^2I_n)$, $X$ fixed, and $\beta$ and $\sigma$ unknown. The null hypotheses are $H_j : \beta_j = 0$; $m_0$ of the $p$ are true.

**Output.** A set $\hat S$ of selected features.

**Error rate controlled.** For knockoff+, the FDR, $E[V/\max(R, 1)] \le q$, where $R = |\hat S|$ and $V$ is the number of null features in $\hat S$. For the plain knockoff filter, the modified FDR $E[V/(R + q^{-1})] \le q$. Both bounds hold for every $\beta$, so the control is strong.

**Dependence assumption.** None on the features beyond full rank: the knockoffs absorb the correlations of $X$. The assumptions are the Gaussian linear model with fixed $X$ and $n \ge 2p$. Model-X knockoffs, the variant named in the aliases, replace them by a known joint law of the rows of $X$ and work for any $n$ and $p$.

**Exact or asymptotic.** Finite-sample, as an inequality. The proof is a theorem of Barber and Candès, cited and not proved here; the page proves the steps that lead to it.

## The algorithm

Normalize the columns so that $\Sigma = X^\top X$ has unit diagonal. With $s \in (0, 2\lambda_{\min}(\Sigma)]$, the knockoffs are
$$\tilde X = X(I - s\Sigma^{-1}) + \tilde UC, \qquad C^\top C = 2sI - s^2\Sigma^{-1},$$
where $\tilde U$ is $n \times p$ with orthonormal columns orthogonal to those of $X$. Then $\tilde X^\top\tilde X = \Sigma$ and $X^\top\tilde X = \Sigma - sI$: the knockoffs have the correlations of $X$, and $\langle X_j, \tilde X_j\rangle = 1 - s$. The equicorrelated choice is $s = \min(2\lambda_{\min}(\Sigma), 1)$, the largest equal value allowed.

```pseudo id=main
KNOCKOFF-FILTER(X, y, q, plus)
L1  normalize the columns of X; Σ ← XᵀX
L2  s ← min(2 λ_min(Σ), 1)                     ▷ Jacobi eigenvalues of Σ
L3  C ← a square root of 2sI - s²Σ⁻¹, so CᵀC = 2sI - s²Σ⁻¹
L4  Ũ ← n × p orthonormal, orthogonal to X      ▷ Gram-Schmidt
L5  X̃ ← X(I - sΣ⁻¹) + ŨC; W ← statistics on [X X̃] and y
L6  sort the distinct values t of |W_j| ≠ 0 in increasing order
L7  T ← the first t with (plus + #{W_j ≤ -t}) ≤ q · max(#{W_j ≥ t}, 1), or ∞
L8  return {j : W_j ≥ T}
```

Here `plus` is 1 for knockoff+ and 0 for the plain filter. The statistic must satisfy two rules. Sufficiency: $W$ depends on the data only through $[X\ \tilde X]^\top[X\ \tilde X]$ and $[X\ \tilde X]^\top y$. Antisymmetry: swapping $X_j$ and $\tilde X_j$ changes the sign of $W_j$ and leaves the other $W_k$ unchanged. The code gives two such statistics: the marginal $W_j = |X_j^\top y| - |\tilde X_j^\top y|$, and the least-squares $W_j = |\hat b_j| - |\hat b_{j+p}|$ from the regression of $y$ on $[X\ \tilde X]$. The usual choice in practice is a lasso statistic, such as the value of the penalty at which $X_j$ enters the [lasso](/lasso-regression/) path, signed by whether it enters before its knockoff.

The equicorrelated $s$ makes $2sI - s^2\Sigma^{-1}$ singular when $s = 2\lambda_{\min}$, so $[X\ \tilde X]$ has rank below $2p$. The lasso and marginal statistics do not mind; the least-squares statistic needs a slightly smaller $s$, and the tests use $0.9$ times the equicorrelated value.

## Example

**The threshold by hand.** Take $p = 14$ statistics
$$W = (9, 8, 7.5, 7, 6, 5.5, -5, 4, 3, -2.5, 2, -1, 0.5, -0.3)$$
and $q = 0.2$. Line L7 scans $t$ upward:

| $t$ | $\#\{W_j \ge t\}$ | $\#\{W_j \le -t\}$ | knockoff+ ratio | plain ratio |
|---|---|---|---|---|
| 0.3 | 10 | 4 | 0.5 | 0.4 |
| 1 | 9 | 3 | 0.444 | 0.333 |
| 2 | 9 | 2 | 0.333 | 0.222 |
| 2.5 | 8 | 2 | 0.375 | 0.25 |
| 3 | 8 | 1 | 0.25 | 0.125 |
| 5 | 6 | 1 | 0.333 | 0.167 |
| 5.5 | 6 | 0 | 0.167 | 0.167 |

The plain filter stops at $T = 3$ and selects the 8 features with $W_j \ge 3$. Knockoff+ needs $(1 + \#\text{neg}) \le 0.2 \cdot \#\text{pos}$, first true at $T = 5.5$, and selects 6. Since the numerator is at least 1, knockoff+ selects nothing unless it can select at least $1/q$ features.

**Why the +1.** With one feature, null, and $W_1 > 0$, the plain ratio is $0/1 \le q$ and the plain filter selects it. This happens with probability $1/2$, so its FDR is $1/2$ for every $q$. Knockoff+ has ratio $1/1 > q$ and never selects it.

**Two correlated features.** If $\Sigma$ has off-diagonal $\rho = 0.6$, then $\lambda_{\min} = 0.4$, $s = 0.8$, and $\langle X_j, \tilde X_j\rangle = 0.2$: the knockoff is nearly orthogonal to its original. If $\rho = 0.9$, then $s = 0.2$ and $\langle X_j, \tilde X_j\rangle = 0.8$. A knockoff so close to its original is hard to beat, and power drops.

**A simulation.** In the tests, a fixed design has $n = 40$, $p = 10$ and column correlation about 0.2, so $s = 0.455$. Five coefficients are 4, five are 0, $\sigma = 1$, and $q = 0.2$. Over 1000 responses:

| method | FDR | power |
|---|---|---|
| knockoff+, marginal $W$ | 0.120 | 0.462 |
| knockoff+, least-squares $W$ ($s$ times 0.9) | 0.111 | 0.402 |
| plain knockoff, marginal $W$ | 0.227 | 0.853 |
| BH on exact $z$-tests, $\sigma$ known | 0.101 | 0.925 |

Knockoff+ stays below $q$, as proved. The plain filter goes above it, by more than four standard errors (the standard error is about 0.005): its guarantee is for the modified FDR only. With only 10 features the knockoff+ rule needs 5 selections before it can select anything, and [Benjamini-Hochberg](/benjamini-hochberg-procedure/), which is given the true $\sigma$ here, is far more powerful. Knockoffs gain when $p$ is in the hundreds or thousands, when $\sigma$ is unknown, and when a good selection statistic like the lasso is used.

## Correctness

Three facts lead to the guarantee, and the [correctness proof](proofs/correctness.md) proves them. First, the construction gives $[X\ \tilde X]^\top[X\ \tilde X] = G$ with $\Sigma$ on the diagonal blocks and $\Sigma - sI$ off them, and it exists exactly when $s \le 2\lambda_{\min}(\Sigma)$. Second, swapping $X_j$ and $\tilde X_j$ for any set of null features leaves the Gram matrix unchanged and, under the Gaussian model, leaves the law of $[X\ \tilde X]^\top y$ unchanged, because $X_j^\top X\beta = \tilde X_j^\top X\beta$ when $\beta_j = 0$. Third, with sufficiency and antisymmetry, this makes the signs of the null $W_j$ independent fair coins, independent of all $|W_j|$ and of the non-null signs (Lemma 1 of Barber and Candès).

So among the features with $|W_j| \ge t$, the nulls split into $W_j \ge t$ and $W_j \le -t$ like coin tosses, and $\#\{W_j \le -t\}$ overestimates the number of nulls with $W_j \ge t$. The step from there to $\text{FDR} \le q$ at the data-dependent threshold is Theorem 2 of Barber and Candès, proved with a supermartingale and [optional stopping](/optional-stopping-theorem/); it is cited here. The tests check it in the coin model: for 150 random sets of magnitudes and non-null signs, they enumerate all $2^{m_0}$ null sign patterns and compute the FDR of knockoff+ and the modified FDR of the plain filter in exact rational arithmetic, and both are at most $q$. In the same enumeration the plain filter's FDR exceeds $q$.

## Complexity

On a [real RAM](/real-ram/), forming $\Sigma$ costs $\Theta(np^2)$. The [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/) costs $\Theta(p^3)$ per sweep and is used twice, for $\lambda_{\min}(\Sigma)$ and $\Sigma^{-1}$ and for the square root $C$. [Gram-Schmidt](/gram-schmidt-process/) on $2p$ vectors of length $n$ costs $\Theta(np^2)$, and so do the products at line L5. A [Cholesky decomposition](/cholesky-decomposition/) of $2sI - s^2\Sigma^{-1}$ also works when $s$ is below $2\lambda_{\min}$. The marginal statistic costs $\Theta(np)$, and the threshold at lines L6 and L7 costs $\Theta(p\log p)$: sort once, then count with binary search or a two-pointer sweep. The space is $\Theta(np)$ for $\tilde X$. With a fixed design the knockoffs are built once, and each new response costs only the statistic and the threshold.

## Properties

- **FDR control of knockoff+** in finite samples, for any $\beta$ and any fixed design with $n \ge 2p$. Cited.
- **Modified FDR control of the plain filter.** Cited. Its FDR can exceed $q$; shown by a hand example and measured.
- **Signs of null statistics are fair coins.** Proved.
- **No p-values and no $\sigma$.** The filter never estimates the noise level, and it allows any statistic with the two properties.
- **Randomized.** $\tilde U$ is random, so the selected set depends on a random draw. Two runs on the same data can select different sets.
- **Needs at least $1/q$ selections.** Knockoff+ selects nothing if fewer than $1/q$ features would be selected.

## Variants and improvements

- **Model-X knockoffs.** Candès, Fan, Janson and Lv (2018) treat the rows of $X$ as random with a known law, and build $\tilde X$ so that swapping any $X_j$ and $\tilde X_j$ leaves the joint law of $(X, \tilde X)$ unchanged and $\tilde X$ is independent of $y$ given $X$. Then knockoff+ controls the FDR for any model of $y$ given $X$, linear or not, and for $p > n$. For Gaussian rows with covariance $\Sigma$, $\tilde X$ given $X$ is Gaussian with mean $X - X\Sigma^{-1}D$ and covariance $2D - D\Sigma^{-1}D$, the same algebra as here.
- **SDP knockoffs.** Choose a different $s_j$ for each feature to minimize $\sum_j(1 - s_j)$ subject to $\operatorname{diag}(s) \preceq 2\Sigma$, a semidefinite program. It gives more power than equicorrelated knockoffs when the features have unequal correlations.
- **$p < n < 2p$.** Barber and Candès add $2p - n$ synthetic rows to $y$ and $X$, using an estimate of $\sigma$ from the full regression.
- **Multiple knockoffs, derandomized knockoffs and e-values.** Several knockoff copies or repeated runs reduce the randomness of the selected set; one way to aggregate is through [e-values](/e-variable/).

## When to use it

Use knockoffs to select variables in a regression with FDR control when the p-values for individual coefficients are unreliable or unavailable, when $\sigma$ is unknown, or when you want to use a selection method such as the lasso and still have a finite-sample guarantee. Fixed-X knockoffs need $n \ge 2p$ and a Gaussian linear model; model-X knockoffs need a good model of the features, as in genetics, where the law of genotypes is well understood. With few features, or when exact p-values are available, [Benjamini-Hochberg](/benjamini-hochberg-procedure/) or [Storey's method](/storey-q-value/) are simpler and often stronger.

## Pitfalls

- **Using the plain filter and calling it FDR control.** Only knockoff+ controls the FDR. The plain filter controls $E[V/(R + q^{-1})]$, which is close to the FDR only when many features are selected.
- **Statistics that break antisymmetry.** A statistic that treats $X_j$ and $\tilde X_j$ differently, for example through the order of a coordinate descent with ties, or that uses $y$ in a way other than through the inner products, loses the coin-flip property.
- **Building knockoffs from $y$.** The knockoffs must be computed from $X$ alone. Choosing $s$ or $\tilde U$ after looking at $y$ voids the proof.
- **Unnormalized columns.** The equicorrelated formula $s = \min(2\lambda_{\min}, 1)$ assumes unit column norms.
- **Too few features.** With $p$ small, knockoff+ often selects nothing at the usual $q$, since it needs at least $1/q$ selections.
- **Wrong feature model in model-X.** The guarantee holds for the law used to build the knockoffs. If that law is estimated badly, the FDR can be above $q$.

## Implementations

## History

Rina Foygel Barber and Emmanuel Candès introduced the knockoff filter in a paper published in the Annals of Statistics in 2015. They proved the FDR control with a martingale argument that also covers a class of sequential testing problems. Candès, Fan, Janson and Lv (2018) extended the idea to random designs with model-X knockoffs, which removed the limit $n \ge 2p$ and the linear model. Later work studied power, knockoffs for hidden Markov models in genetics, derandomized and multiple knockoffs, and robustness to a misspecified feature law.

## References
