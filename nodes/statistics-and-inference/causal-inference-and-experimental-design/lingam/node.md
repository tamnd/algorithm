---
tag: YZF859
kind: algorithm
slug: lingam
name: LiNGAM
aliases:
- linear non-Gaussian acyclic model
area: statistics-and-inference/causal-inference-and-experimental-design
level: research
summary: Identifies the full causal DAG of a linear model with non-Gaussian noise, by independent component analysis or by DirectLiNGAM's search for exogenous variables.
model: real-ram
complexity:
  vars: {n: the number of variables, m: the number of samples}
  time: {worst: "Θ(n^3 m + n^4)", best: "Θ(n^3 m + n^4)"}
  space: {extra: "Θ(n m)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2006
  people: [Shohei Shimizu, Patrik O. Hoyer, Aapo Hyvärinen, Antti Kerminen]
  note: Shimizu, Hoyer, Hyvärinen and Kerminen showed that non-Gaussian errors make the whole causal DAG of a linear model identifiable, and found it with independent component analysis. DirectLiNGAM (2011) replaced the ICA step by a search for exogenous variables.
prereqs: [independent-component-analysis, structural-causal-model, directed-acyclic-graph, ordinary-least-squares, pc-algorithm]
see_also: [greedy-equivalence-search, fci-algorithm, fastica, lasso-regression, bayesian-network-structure-learning, central-limit-theorem, topological-sort, covariance-matrix]
sources:
  - paper: "Shohei Shimizu, Patrik O. Hoyer, Aapo Hyvärinen and Antti Kerminen, A linear non-Gaussian acyclic model for causal discovery, Journal of Machine Learning Research 7, 2006, pp. 2003 to 2030"
    locator: The whole paper (the model, its identifiability through independent component analysis, and the ICA-LiNGAM algorithm with its permutation and pruning steps)
  - paper: "Shohei Shimizu, Takanori Inazumi, Yasuhiro Sogawa, Aapo Hyvärinen, Yoshinobu Kawahara, Takashi Washio, Patrik O. Hoyer and Kenneth Bollen, DirectLiNGAM: A direct method for learning a linear non-Gaussian structural equation model, Journal of Machine Learning Research 12, 2011, pp. 1225 to 1248"
    locator: The whole paper (the lemmas on exogenous variables and residuals, and the DirectLiNGAM algorithm)
  - paper: "Aapo Hyvärinen and Stephen M. Smith, Pairwise likelihood ratios for estimation of non-Gaussian structural equation models, Journal of Machine Learning Research 14, 2013, pp. 111 to 152"
    locator: The whole paper (the likelihood ratio of two causal directions and its entropy approximation, used in line L5)
  - paper: "doi:10.1016/0165-1684(94)90029-9"
    title: "Pierre Comon, Independent component analysis, a new concept?, Signal Processing 36(3), 1994, pp. 287 to 314"
    locator: The whole paper (identifiability of the mixing matrix up to permutation and scale when at most one source is Gaussian)
  - paper: doi:10.2307/1401511
    title: "Georges Darmois, Analyse générale des liaisons stochastiques: étude particulière de l'analyse factorielle linéaire, Revue de l'Institut International de Statistique 21, 1953, pp. 2 to 8"
    locator: The whole paper (the Darmois half of the Darmois-Skitovich theorem)
  - paper: "V. P. Skitovich, On a property of the normal distribution, Doklady Akademii Nauk SSSR 89, 1953, pp. 217 to 219 (in Russian)"
    locator: The whole paper (the Skitovich half of the Darmois-Skitovich theorem)
---

LiNGAM, the linear non-Gaussian acyclic model, is a [structural causal model](/structural-causal-model/) in which each variable is a linear function of its causes plus an independent error, the causes form a [directed acyclic graph](/directed-acyclic-graph/), and the errors are not Gaussian. The same name is used for the methods that learn the graph from data. Methods such as the [PC algorithm](/pc-algorithm/) and [greedy equivalence search](/greedy-equivalence-search/) use only conditional independences, so they can return only a Markov equivalence class, and they cannot orient $X - Y$ for two variables. LiNGAM uses the shape of the distribution, not only its covariances. Shimizu, Hoyer, Hyvärinen and Kerminen (2006) proved that this identifies the whole DAG and its weights, and found it with [independent component analysis](/independent-component-analysis/). DirectLiNGAM (Shimizu et al. 2011), the version on this page, finds the causes one at a time instead.

## In plain words

Suppose one quantity causes another, and each also has its own random push from outside. If the pushes follow the bell curve, the data look the same in both directions, and no method can tell cause from effect. If the pushes have any other shape, the directions differ. When you predict the effect from the cause, what is left over is the effect's own push, and it has nothing to do with the cause. When you predict the cause from the effect, what is left over still depends on the effect, even if it is uncorrelated with it. DirectLiNGAM uses this to find a variable that nothing else causes, removes its influence from all other variables, and repeats. This gives an order from causes to effects. Regression along this order then gives the arrows and their strengths.

## The problem

The data are $m$ samples of $n$ variables from the model

$$x = Bx + e,$$

where $B_{ji} \ne 0$ means the edge $i \to j$, the graph of $B$ has no directed cycle, and the components of $e$ are independent, non-Gaussian, with mean 0 and finite positive variance. There are no hidden common causes: every dependence between errors would have to come from such a cause, and the model forbids it. A causal order is an order of the variables in which every edge points forward, a [topological order](/topological-sort/) of the graph. A variable is exogenous when it has no parent, so it equals its own error.

The task is to estimate a causal order and $B$. Then $x = (I - B)^{-1}e$ is a linear mixture of independent non-Gaussian sources, which is the model of independent component analysis, with the extra structure that $I - B$ is triangular up to a permutation.

## The algorithm

For two centred variables, the residual of $x_i$ on $x_j$ is $r_i^{(j)} = x_i - \frac{\operatorname{Cov}(x_i, x_j)}{\operatorname{Var}(x_j)}x_j$, the error of the [least-squares](/ordinary-least-squares/) fit. Hyvärinen and Smith (2013) compare the two directions between standardized $x_i$ and $x_j$ by the log-likelihood ratio

$$R(i, j) = H(x_j) + H(r_i^{(j)}) - H(x_i) - H(r_j^{(i)}),$$

where $H$ is the differential [entropy](/shannon-entropy/) of a standardized variable, with $r$ standardized too. $R(i, j) > 0$ favours $x_i \to x_j$. The implementation uses their approximation $H(u) \approx \frac{1 + \log 2\pi}{2} - k_1(\mathrm{E}\log\cosh u - \gamma)^2 - k_2(\mathrm{E}\,u e^{-u^2/2})^2$ with $k_1 = 79.047$, $k_2 = 7.4129$ and $\gamma = 0.37457$; the first term is the entropy of a standard Gaussian, the largest entropy at unit variance.

```pseudo id=main
DirectLiNGAM(X)
L1  U ← the variables of X, sorted by name;  K ← the empty list
L2  while U has more than one variable do
L3      S(i) ← 0 for each i in U
L4      for each i in U do
L5          for each j in U after i do compute R(i, j)
L6              S(i) ← S(i) + min(0, R(i, j))^2;  S(j) ← S(j) + min(0, -R(i, j))^2
L7      m ← the i in U with the smallest S(i), ties by name;  append m to K
L8      for each j in U other than m do x_j ← the standardized residual of x_j on x_m
L9      remove m from U
L10 append the last variable of U to K
L11 B ← least squares of each x_j on the variables before j in K, with the original data;  set every |b| < τ to 0
L12 return K and B
```

The score $S(i)$ is the total evidence against $x_i$ being a cause of the others: it grows only when some pair favours the direction into $x_i$. An exogenous variable should have a score near 0. Line L8 removes the influence of the chosen variable, and the residuals follow a LiNGAM model with the same weights on the remaining variables, so the loop can repeat. The implementation uses $\tau = 0.1$. The original DirectLiNGAM measures the dependence between $x_i$ and its residuals with a kernel independence measure instead of $R$; the structure of the loop is the same.

## Example

Take $A \to B$, $A \to C$, $B \to D$, $C \to D$, $D \to E$ with $B = 0.8A + e_B$, $C = 0.7A + e_C$, $D = 0.6B + 0.6C + e_D$, $E = 0.9D + e_E$, and errors uniform on $[-\sqrt3, \sqrt3]$, so of unit variance. The implementation draws $m = 1000$ samples with seed 1 and gives the columns in the order $E, C, A, D, B$, so the input order tells nothing.

In round 1, all four ratios of $A$ are positive: $R(A, B) = 0.103$, $R(A, C) = 0.0935$, $R(A, D) = 0.045$, $R(A, E) = 0.035$. So $S(A) = 0$, while every other variable loses at least one pair, for example $S(B) = 0.0106$ and $S(D) = 0.0023$. DirectLiNGAM takes $A$ and replaces $B, C, D, E$ by their residuals on $A$.

| round | scores | chosen |
|---|---|---|
| 1 | $A$: 0, $B$: 0.0106, $C$: 0.0088, $D$: 0.0023, $E$: 0.0032 | $A$ |
| 2 | $B$, $C$: both below 0.00001, $D$: 0.0051, $E$: 0.0043 | $C$ |
| 3 | $B$: below 0.00001, $D$: 0.0071, $E$: 0.0042 | $B$ |
| 4 | $D$: below 0.00001, $E$: 0.0076 | $D$ |

The order is $A, C, B, D, E$. After round 1, $B$ and $C$ are both exogenous in the residual model, so the order of $C$ and $B$ is free, and both orders are causal orders. Line L11 gives the weights $A \to B$: 0.83, $A \to C$: 0.71, $B \to D$: 0.61, $C \to D$: 0.63, $D \to E$: 0.91, and sets the five other coefficients, all below 0.1 in size, to 0. This is the true graph with all five edges oriented. On the same data, PC or GES could orient only $B \to D \leftarrow C$ and $D \to E$.

**Why the direction shows.** Take $x = e_1$ and $y = x + e_2$, where $e_1$ and $e_2$ are independent and each is $-1$ or $1$ with probability $1/2$. The forward residual $y - x = e_2$ is independent of $x$. The backward regression of $x$ on $y$ has slope $1/2$, and its residual $r = (e_1 - e_2)/2$ is uncorrelated with $y$. But $r = 0$ and $y = 0$ never happen together, while each has probability $1/2$, so $r$ and $y$ are dependent. The tests check this with exact fractions.

**Why Gaussian errors fail.** With Gaussian errors, uncorrelated means independent. Then every order of the variables gives a linear model with independent errors and the same covariance matrix, so all orders fit equally well. The tests check this exactly for all 6 orders of a model on three variables.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It is partial. It cites the Darmois-Skitovich theorem (Darmois 1953, Skitovich 1953): if two linear combinations of independent variables are independent, then every variable that appears in both is Gaussian. From it the proof shows:

1. **Identifiability.** If $x = Bx + e = B'x + e'$, both with acyclic graphs and independent errors, and at most one component of $e$ is Gaussian, then $B' = B$. The matrix $M = (I - B')(I - B)^{-1}$ maps $e$ to $e'$; Darmois-Skitovich makes it a scaled permutation, and acyclicity with the unit diagonal makes it the identity.
2. **Exogenous variables.** An exogenous variable is independent of all its residuals, and a variable with a parent has a dependent residual: the one of its last parent in a causal order.
3. **Residual model.** Regressing out an exogenous variable leaves a model with the same weights and errors on the other variables.
4. **DirectLiNGAM with an exact test.** If line L7 chooses a variable that is independent of its residuals, the loop runs $n - 1$ rounds, $K$ is a causal order, and line L11 without the threshold returns $B$ in the population.

Not proved: that the approximate score of line L6 picks an exogenous variable. Hyvärinen and Smith (2013) show that the exact likelihood ratio has the right sign for two variables in the population (cited). For the approximation and for finite samples the rates are measured, see Pitfalls.

## Complexity

Round $k$ has $n - k + 1$ variables and computes one ratio $R$ for each pair, and each ratio costs $\Theta(m)$ for two regressions and four entropies. Summed over the rounds this is $\Theta(n^3 m)$. Line L8 adds $\Theta(n^2 m)$ in total. In line L11, the regression of the $t$-th variable needs $\Theta(t^2 m)$ for its covariances and $\Theta(t^3)$ to solve the system, so $\Theta(n^3 m + n^4)$ in total. The work does not depend on the data, so the best and worst cases agree. The standardized copies of the data take $\Theta(nm)$ space. A kernel independence measure, as in the original DirectLiNGAM, costs far more per pair than the entropy approximation.

## Properties

- **Full orientation.** The output is one DAG, not an equivalence class. This is possible only because the errors are not Gaussian.
- **Weights included.** Line L11 gives the strength of each edge, so total effects follow from $(I - B)^{-1}$.
- **Deterministic.** Ties in line L7 are broken by name, and the result does not depend on the order of the input columns.
- **Consistent, not exact.** The identifiability theorem holds for the population. On a finite sample the order can be wrong, and the threshold can drop weak edges.
- **No conditional independence tests.** Unlike PC, it never tests conditional independence, and it needs no faithfulness assumption for the order.

## Variants and improvements

- **ICA-LiNGAM.** The first method (Shimizu et al. 2006) runs ICA, for example [FastICA](/fastica/), to estimate $W = I - B$ up to the order and scale of its rows. It permutes the rows so that no diagonal entry is near 0, divides each row by its diagonal entry, sets $B = I - W$, and permutes the variables to make $B$ as near to strictly lower triangular as possible. Comon (1994) showed that ICA identifies the mixing matrix up to permutation and scale when at most one source is Gaussian. ICA can stop at a local optimum and depends on its start; DirectLiNGAM avoids this.
- **Kernel measure.** DirectLiNGAM as published measures independence with a kernel method, which is slower but uses no entropy approximation.
- **Pairwise measures.** Hyvärinen and Smith (2013) give the likelihood ratio used here, and other approximations of it.
- **Pruning.** Instead of a fixed threshold, use the adaptive [lasso](/lasso-regression/) or tests of the coefficients along the order.
- **Extensions.** Later work extends LiNGAM to hidden common causes, to time series, and to cyclic models, each with weaker identification results.

## When to use it

Use LiNGAM when the relations are close to linear, all common causes are measured, and the errors are clearly not Gaussian, for example skewed, heavy-tailed or bounded. It gives a full DAG where PC or GES leave edges undirected. If the errors look Gaussian, or the data come from sums of many small effects (the [central limit theorem](/central-limit-theorem/) makes such errors near Gaussian), use PC or GES and accept the equivalence class. If hidden common causes are likely, use the [FCI algorithm](/fci-algorithm/) or a LiNGAM variant made for them.

## Pitfalls

- **Gaussian errors.** With Gaussian errors the direction is not identified. On two variables $X \to Y$ with 1000 samples, the implementation found $X$ first in 24 of 50 runs, close to a coin flip, against 50 of 50 with uniform errors. On 50 random models with five variables, the order was a causal order in 3 of 50 runs with Gaussian errors, and in 50 of 50 with uniform errors.
- **Weak edges.** The threshold drops small weights, and sampling noise can keep a spurious one. In the 50 uniform runs, all orders were right, but the set of edges was exactly right in 43. These rates are measured on the implementation, not proved.
- **Hidden common causes.** A hidden cause of two variables makes their errors dependent, and the model fails. The method still returns a DAG, with no warning.
- **Non-linear relations.** A non-linear effect leaves residuals that depend on the cause, which can point the arrow the wrong way.
- **Weak non-Gaussianity.** The signal is in the higher moments. When the errors are nearly Gaussian, many more samples are needed, and the approximate entropy can rank the directions wrongly.
- **Measurement error.** Noise added to a cause after it acts makes the cause look like an effect, so the order can reverse.

## Implementations

## History

Darmois (1953) and Skitovich (1953) proved, independently, that two independent linear combinations of independent variables can share only Gaussian variables. Comon (1994) used this to show that independent component analysis identifies its mixing matrix up to permutation and scale when the sources are not Gaussian. In 2006 Shimizu, Hoyer, Hyvärinen and Kerminen applied this to causal discovery: in a linear acyclic model with non-Gaussian errors, the triangular structure of $I - B$ fixes the permutation and scale, so the whole DAG is identified. Their ICA-LiNGAM found it with FastICA. Shimizu and co-authors gave DirectLiNGAM in 2011, which finds exogenous variables one at a time and needs no iterative ICA, and Hyvärinen and Smith (2013) gave the pairwise likelihood ratios that many implementations use.

## References
