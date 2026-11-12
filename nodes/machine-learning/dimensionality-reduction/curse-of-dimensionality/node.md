---
tag: QWKNH3
kind: concept
slug: curse-of-dimensionality
name: Curse of dimensionality
aliases:
- Bellman's curse of dimensionality
- dimensionality curse
area: machine-learning/dimensionality-reduction
level: intro
summary: "As the dimension grows, volume moves to the corners and the surface, nearest and farthest distances become nearly equal, and the data and work needed grow exponentially."
prereqs: [euclidean-distance]
see_also: [concentration-of-measure, hubness, intrinsic-dimensionality, approximate-nearest-neighbor-search, johnson-lindenstrauss-lemma, smolyak-sparse-grids, monte-carlo-integration, feature-selection]
sources:
  - book: isbn:9780486428093
    title: Richard Bellman, Dynamic Programming, Princeton University Press, 1957, reprinted by Dover, 2003
    locator: Preface (the phrase curse of dimensionality, for the growth of the state space with the number of state variables)
  - paper: "Richard Bellman, Adaptive Control Processes, a guided tour, Princeton University Press, 1961"
    locator: the discussion of computational limits of dynamic programming in several state variables
  - paper: doi:10.1007/3-540-49257-7_15
    title: Kevin Beyer, Jonathan Goldstein, Raghu Ramakrishnan and Uri Shaft, When is nearest neighbor meaningful?, Database Theory, ICDT 1999, Lecture Notes in Computer Science 1540, Springer, 1999
    locator: pp. 217 to 235 (Section 3, Theorem 1 on the ratio of the largest to the smallest distance)
  - paper: doi:10.1214/aos/1176345969
    title: Charles J. Stone, Optimal global rates of convergence for nonparametric regression, Annals of Statistics 10(4), 1982
    locator: pp. 1040 to 1053 (the optimal rate n^(-p/(2p+d)) for p-smooth functions of d variables)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, 2nd edition, Springer, 2009
    locator: Section 2.5 (local methods in high dimensions, the subcube edge and the median nearest neighbour distance)
  - paper: doi:10.1007/3-540-44503-X_27
    title: Charu C. Aggarwal, Alexander Hinneburg and Daniel A. Keim, On the surprising behavior of distance metrics in high dimensional space, Database Theory, ICDT 2001, Lecture Notes in Computer Science 1973, Springer, 2001
    locator: pp. 420 to 434 (relative contrast for Lp norms, smaller p keeps more contrast)
  - paper: "Keith Ball, An elementary introduction to modern convex geometry, in Flavors of Geometry, MSRI Publications 31, Cambridge University Press, 1997"
    locator: Lecture 1 (the volume of the Euclidean ball, comparison with the cube, concentration of volume)
  - paper: "David L. Donoho, High-dimensional data analysis, the curses and blessings of dimensionality, lecture at the AMS conference Mathematical Challenges of the 21st Century, 2000"
    locator: Sections on the curse and on the blessings of dimensionality (concentration of measure as a help)
---

The curse of dimensionality is the name, due to Richard Bellman (1957), for the ways in which problems get harder, often exponentially, as the number of variables $d$ grows. Bellman meant the cost of [dynamic programming](/dynamic-programming/) over a grid of states: with $k$ values for each of $d$ state variables there are $k^d$ states. In statistics and machine learning the same growth shows up as data: to keep a fixed number of samples near every point, the sample size must grow exponentially in $d$. It also shows up in geometry. The unit ball fills a vanishing part of its enclosing cube, almost all of its volume lies in a thin shell near the surface, and the distances from a query to its nearest and its farthest data point become nearly equal (Beyer and colleagues 1999). Methods that work by looking at neighbourhoods, such as [k-nearest neighbors](/k-nearest-neighbors/), [kd-trees](/kd-tree/), histograms and grids, are hit hardest.

## In plain words

Adding more measurements to each data point sounds like it should help. Often it does the opposite.

Think of a grid. Ten steps along one line make ten boxes. Ten steps along each side of a square make a hundred boxes, and in ten directions there are ten billion boxes. You can never have enough data to put a few points in every box.

Space also behaves in strange ways. In many directions, almost all of a ball lies just under its surface, and the ball fills almost none of the box around it. Random points all end up about the same distance from each other, so "the nearest point" is barely nearer than the farthest one.

The cure is structure. Real data usually lies near a much smaller set of directions, and methods that find and use that structure can escape the curse.

## The idea

**Grids and sample size.** A grid with $k$ cells per axis has $k^d$ cells. Any method that must see data in every cell, or must evaluate a function at every grid point, needs work or data of order $k^d$. A cube that holds a fraction $p$ of the uniform data in $[0, 1]^d$ has edge $p^{1/d}$. In $d = 10$ dimensions, a neighbourhood that holds 10% of the data has edge $0.1^{1/10} \approx 0.79$, so it covers 79% of the range of every input and is no longer local.

**Volume.** The volume of the unit ball in $\mathbb{R}^d$ is
$$ V_d = \frac{\pi^{d/2}}{\Gamma(d/2 + 1)} , \qquad V_d = \frac{2\pi}{d} V_{d-2}, \quad V_0 = 1, \ V_1 = 2 . $$
It grows up to $d = 5$ and then decreases to 0 faster than exponentially; the recursion shows that $V_d < V_{d-2}$ once $d > 2\pi$. The cube $[-1, 1]^d$ around the ball has volume $2^d$, so the ball fills a fraction $V_d / 2^d$ of it, which is $0.25\%$ for $d = 10$. The rest of the cube is in the $2^d$ corners. Inside the ball, the part with norm at most $1 - \varepsilon$ has volume $(1 - \varepsilon)^d V_d$, so a fraction $1 - (1 - \varepsilon)^d \to 1$ of the volume lies in the shell of width $\varepsilon$.

**Distance concentration.** Let $D_{\min}$ and $D_{\max}$ be the smallest and largest distances from a query to $n$ data points, and call $(D_{\max} - D_{\min}) / D_{\min}$ the relative contrast. Beyer, Goldstein, Ramakrishnan and Shaft (1999) proved: if the distance $D_d$ from the query to a random data point satisfies
$$ \lim_{d \to \infty} \operatorname{Var}\!\left( \frac{D_d^{\,p}}{\mathbb{E}[D_d^{\,p}]} \right) = 0 $$
for some $p > 0$, then for every fixed $n$ and every $\varepsilon > 0$, $\Pr[D_{\max} \le (1 + \varepsilon) D_{\min}] \to 1$. So the relative contrast goes to 0 in probability. The condition holds, for example, when the coordinates are independent and identically distributed, because the squared distance is then a sum of $d$ independent terms and its relative spread shrinks like $1/\sqrt{d}$ by the [law of large numbers](/law-of-large-numbers/) and [concentration of measure](/concentration-of-measure/). The condition fails when the data lie near a low-dimensional set or in well-separated clusters, which is why nearest neighbour search still works on many real data sets. Aggarwal, Hinneburg and Keim (2001) showed that the contrast shrinks more slowly for $L_p$ norms with small $p$.

**Rates of estimation.** Stone (1982) found the best possible rate for nonparametric regression. If the regression function has $s$ bounded derivatives in $d$ variables, no estimator can have a mean squared error that goes to 0 faster than $n^{-2s/(2s+d)}$, and local polynomial estimators reach that rate. To reach a squared error $\varepsilon$, about $\varepsilon^{-(2s+d)/(2s)}$ samples are needed, which is exponential in $d$ for fixed $s$. Smoothness that grows with $d$, or structure such as additivity or a low [intrinsic dimension](/intrinsic-dimensionality/), changes $d$ in the exponent to something smaller.

**Blessings.** Donoho (2000) points out that concentration also helps. [Random projections](/random-projection/) preserve distances by the [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/), and [Monte Carlo integration](/monte-carlo-integration/) has an error of order $n^{-1/2}$ in every dimension.

## Examples

**Volume of the unit ball.** Exact values follow from the recursion:

| $d$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 10 | 20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $V_d$ | $2$ | $\pi$ | $\frac{4}{3}\pi$ | $\frac{1}{2}\pi^2$ | $\frac{8}{15}\pi^2$ | $\frac{1}{6}\pi^3$ | $\frac{16}{105}\pi^3$ | $\frac{1}{120}\pi^5$ | $\frac{1}{10!}\pi^{10}$ |
| value | 2 | 3.1416 | 4.1888 | 4.9348 | 5.2638 | 5.1677 | 4.7248 | 2.5502 | 0.0258 |
| $V_d / 2^d$ | 1 | 0.785 | 0.524 | 0.308 | 0.164 | 0.081 | 0.037 | 0.0025 | $2.5 \times 10^{-8}$ |

The shell of width $\varepsilon = 0.01$ holds 2% of the volume of the disk, 9.6% in $d = 10$, 63% in $d = 100$ and 99.3% in $d = 500$.

**Nearest neighbours move out.** For $n$ points uniform in the unit ball of $\mathbb{R}^d$, the median distance from the centre to the nearest point is $(1 - 2^{-1/n})^{1/d}$. For $n = 500$ this is 0.037 in $d = 2$ but 0.52 in $d = 10$: the nearest of 500 points is more than halfway to the boundary (Hastie, Tibshirani and Friedman, Section 2.5).

**Relative contrast.** In a simulation with 100 points and a query, all uniform in $[0, 1]^d$, averaged over 20 draws, the mean relative contrast was:

| $d$ | 2 | 10 | 100 | 1000 |
| --- | --- | --- | --- | --- |
| $(D_{\max} - D_{\min}) / D_{\min}$ | 48.2 | 1.73 | 0.31 | 0.09 |

In 1000 dimensions the farthest of the 100 points is only about 9% farther away than the nearest.

**Samples for a target error.** With $s = 2$ derivatives and target squared error $\varepsilon = 0.01$, Stone's rate asks for about $\varepsilon^{-(4 + d)/4}$ samples, up to constants:

| $d$ | 1 | 2 | 5 | 10 | 20 |
| --- | --- | --- | --- | --- | --- |
| samples | 316 | $10^3$ | $3.2 \times 10^4$ | $10^7$ | $10^{12}$ |

**Grids.** A grid with 10 cells per axis has $10^{10}$ cells in 10 dimensions. A dynamic program over 6 state variables with 100 levels each has $10^{12}$ states.

## Where it is used

- **Dynamic programming and control.** Bellman's original setting. The [Bellman equation](/bellman-equation/) over a discretized state space needs $k^d$ states, which drives approximate dynamic programming and reinforcement learning with function approximation.
- **Numerical integration.** Product rules with $k$ nodes per axis need $k^d$ evaluations. [Monte Carlo integration](/monte-carlo-integration/), quasi-Monte Carlo and [Smolyak sparse grids](/smolyak-sparse-grids/) avoid the full product; see [multidimensional integration](/multidimensional-integration/).
- **Nearest neighbour search and indexing.** Exact search structures such as [kd-trees](/kd-tree/) degrade toward a linear scan as $d$ grows. This motivates [approximate nearest neighbour search](/approximate-nearest-neighbor-search/), and distance concentration produces [hubness](/hubness/).
- **Nonparametric statistics and machine learning.** Kernel density estimates, histograms and k-nearest-neighbour rules converge at rates that depend on $d$ as in Stone's bound.
- **Dimensionality reduction and feature selection.** [Principal component analysis](/principal-component-analysis/), [random projection](/random-projection/), the [manifold hypothesis](/manifold-hypothesis/) and [feature selection](/feature-selection/) all try to replace the ambient dimension by a smaller effective one.
- **Clustering.** In high dimensions, clusters may exist only in subsets of the features, which leads to subspace clustering.

## References
