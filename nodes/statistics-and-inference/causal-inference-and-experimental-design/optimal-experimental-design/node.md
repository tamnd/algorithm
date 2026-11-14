---
tag: P9PTC4
kind: problem
slug: optimal-experimental-design
name: Optimal experimental design
aliases:
- D-optimal design
- A-optimal design
- optimal design of experiments
area: statistics-and-inference/causal-inference-and-experimental-design
level: advanced
summary: Choose design points that optimize a criterion of the information matrix, such as its determinant for D-optimality or the trace of its inverse for A-optimality.
prereqs: [ordinary-least-squares, linear-regression, positive-definite-matrix, determinant, fisher-information-matrix]
see_also: [kiefer-wolfowitz-equivalence-theorem, fedorov-exchange-algorithm, response-surface-methodology, factorial-design, fractional-factorial-design, plackett-burman-design, orthogonal-array, minimum-volume-enclosing-ellipsoid]
sources:
  - paper: doi:10.1111/j.2517-6161.1959.tb00338.x
    title: "J. Kiefer, Optimum experimental designs, Journal of the Royal Statistical Society, Series B 21(2), 1959, pp. 272 to 304"
    locator: The whole paper (approximate designs and the criteria named by letters)
  - paper: doi:10.4153/CJM-1960-030-4
    title: "J. Kiefer and J. Wolfowitz, The equivalence of two extremum problems, Canadian Journal of Mathematics 12, 1960, pp. 363 to 366"
    locator: The whole paper (D-optimality and G-optimality are equivalent)
  - paper: doi:10.1214/aoms/1177696809
    title: "Henry P. Wynn, The sequential generation of D-optimum experimental designs, Annals of Mathematical Statistics 41(5), 1970, pp. 1655 to 1664"
    locator: The whole paper (adding the point of largest variance converges to a D-optimal design)
  - book: "V. V. Fedorov, Theory of Optimal Experiments, translated and edited by W. J. Studden and E. M. Klimko, Academic Press, 1972"
    locator: The whole book (continuous designs, the iterative procedure that adds the point of largest variance, and the exchange of points for exact designs; general locator)
  - paper: doi:10.1214/09-AOS761
    title: "Yaming Yu, Monotonic convergence of a general algorithm for computing optimal designs, Annals of Statistics 38(3), 2010, pp. 1593 to 1606"
    locator: The whole paper (the multiplicative algorithm of Silvey, Titterington and Torsney increases the criterion at every step and converges)
  - paper: doi:10.1137/S0895479896303430
    title: "Lieven Vandenberghe, Stephen Boyd and Shao-Po Wu, Determinant maximization with linear matrix inequality constraints, SIAM Journal on Matrix Analysis and Applications 19(2), 1998, pp. 499 to 533"
    locator: The section on experiment design (D-, A- and E-optimal designs as determinant maximization and semidefinite programs)
  - paper: doi:10.1080/00949658208810560
    title: "William J. Welch, Algorithmic complexity: three NP-hard problems in computational statistics, Journal of Statistical Computation and Simulation 15(1), 1982, pp. 17 to 25"
    locator: The whole paper (exact D-optimal design is NP-hard)
  - paper: doi:10.1016/j.tcs.2009.06.018
    title: "Ali Çivril and Malik Magdon-Ismail, On selecting a maximum volume sub-matrix of a matrix and related problems, Theoretical Computer Science 410(47-49), 2009, pp. 4801 to 4811"
    locator: Theorem 4 (the maximum volume subset problem is NP-hard) and Theorem 6 (it has no polynomial approximation scheme)
  - book: isbn:9780898716047
    title: Friedrich Pukelsheim, Optimal Design of Experiments, SIAM Classics in Applied Mathematics 50, 2006 (reprint of the Wiley edition of 1993)
    locator: Chapter 9 (D-, A-, E- and T-optimality) and Chapter 12 (efficient designs for finite sample sizes)
  - book: isbn:9780199296606
    title: A. C. Atkinson, A. N. Donev and R. D. Tobias, Optimum Experimental Designs, with SAS, Oxford University Press, 2007
    locator: Chapter 10 (criteria of optimality), Chapter 11 (D-optimum designs) and Chapter 12 (algorithms for the construction of exact D-optimum designs)
---

Optimal experimental design is the problem of choosing where to take observations so that a model fitted to them is as precise as possible. For a linear model $y = f(x)^\top\theta + \varepsilon$, the precision of the [ordinary least squares](/ordinary-least-squares/) estimate depends only on the chosen settings, through the information matrix $\sum_i f(x_i)f(x_i)^\top$, and not on the responses. So the design can be optimized before any data exist. Each scalar summary of the information matrix gives a criterion: the determinant gives D-optimal designs, the trace of the inverse gives A-optimal designs, and the largest prediction variance gives G-optimal designs. The [Kiefer-Wolfowitz equivalence theorem](/kiefer-wolfowitz-equivalence-theorem/) characterizes the solutions, and the [Fedorov exchange algorithm](/fedorov-exchange-algorithm/) finds good designs with a fixed number of runs.

## In plain words

Before you run an experiment, you decide which settings to try and how often. Some choices teach you much more than others. To fit a straight line, runs at the two ends of the range pin down the slope far better than runs bunched in the middle. The problem asks for the best choice, given a model and a measure of what "precise" means. For linear models, precision depends only on where you measure, not on what you see, so the whole plan can be fixed in advance. Several measures of precision exist. One makes the region of plausible coefficient values small, one makes the average uncertainty small, and one makes the worst prediction good. They often agree, but not always.

## Definition

**Input.**

- A design region $\mathcal X$: a compact set, or a finite list of $n$ candidate settings.
- Regression functions $f : \mathcal X \to \mathbb R^p$ for the model $y = f(x)^\top\theta + \varepsilon$, with uncorrelated errors of mean 0 and variance $\sigma^2$. For a nonlinear model or a [generalized linear model](/generalized-linear-model/), $f(x)$ is the gradient of the mean at a guessed parameter $\theta_0$, and the information matrix is the [Fisher information matrix](/fisher-information-matrix/) at $\theta_0$ (a locally optimal design).
- A number of runs $N$ (exact designs), or none (approximate designs).
- A criterion $\Phi$.

**Output.** An exact design is a list of $N$ points of $\mathcal X$, repeats allowed. An approximate design $\xi$ is a finite set of points $x_i$ with weights $w_i > 0$ that sum to 1; it is turned into runs by rounding $Nw_i$. The moment matrix is

$$M(\xi) = \sum_i w_if(x_i)f(x_i)^\top,$$

and the least squares estimate from $N$ runs has covariance $\sigma^2M(\xi)^{-1}/N$. For an exact design, $M = X^\top X/N$ with $X$ the $N \times p$ matrix of rows $f(x_i)^\top$.

**Criteria.** With $d(x, \xi) = f(x)^\top M(\xi)^{-1}f(x)$, the standardized variance of the predicted mean at $x$:

| criterion | optimize | meaning |
|---|---|---|
| D | maximize $\log\det M$ | smallest volume of the confidence ellipsoid of $\theta$ |
| A | minimize $\operatorname{tr}M^{-1}$ | smallest mean variance of the $p$ coefficients |
| E | maximize $\lambda_{\min}(M)$ | smallest worst variance of $c^\top\hat\theta$ over unit vectors $c$ |
| c | minimize $c^\top M^{-1}c$ | smallest variance of one linear combination $c^\top\hat\theta$ |
| G | minimize $\max_{x \in \mathcal X}d(x, \xi)$ | smallest worst prediction variance over the region |
| I (or V) | minimize $\int d(x, \xi)\,\mu(dx)$ | smallest mean prediction variance over a measure $\mu$ |

D-optimality does not depend on the scale of the coordinates of $f$: a linear change $f \mapsto Tf$ with $T$ nonsingular multiplies $\det M$ by $(\det T)^2$ for every design. A, E and c depend on the parametrization.

## Variants

- **Approximate versus exact.** Over approximate designs, the set of moment matrices is convex and D, A, E, c and I are concave criteria (after a sign change where needed), so the problem is a convex optimization problem with a global optimum that can be checked. With $N$ runs it becomes a combinatorial problem.
- **Finite candidate list.** With $n$ candidates, the approximate problem has $n$ weights on the simplex. Many algorithms and the proofs of their convergence use this case.
- **Constraints.** Fixed blocks, hard-to-change factors (split-plot designs), costs per run, forbidden regions and mixture constraints (the factors sum to 1) change $\mathcal X$ or add terms to $M$.
- **Nonlinear and Bayesian designs.** Locally optimal designs depend on the guess $\theta_0$. Bayesian designs average a criterion over a prior for $\theta$, and sequential designs update the guess after each batch.
- **Partial interest.** $D_s$-optimality maximizes the determinant of the information for $s$ of the parameters; model discrimination designs maximize the power to tell two models apart.
- **Robust designs.** Designs that keep a good efficiency for several candidate models, or that guard against an omitted higher-order term, are the subject of model-robust design.

## Examples

- **Straight line on $[-1, 1]$.** Weight $1/2$ at $-1$ and at $1$ is D-, A-, E- and G-optimal: $M = I$ and $d(x) = 1 + x^2 \le 2 = p$.
- **Quadratic on $[-1, 1]$.** The D-optimal design puts weight $1/3$ at $-1$, $0$ and $1$, with $\det M = 4/27$ and $\operatorname{tr}M^{-1} = 9$. The A-optimal design puts weights $1/4$, $1/2$, $1/4$ at the same points, with $\operatorname{tr}M^{-1} = 8$ and $\det M = 1/8$. Both are proved optimal by the equivalence theorem: for D, $d(x) = 3 - \frac92x^2(1 - x^2) \le 3$; for A, $f(x)^\top M^{-2}f(x) = 8 - 20x^2(1 - x^2) \le 8 = \operatorname{tr}M^{-1}$. So the two criteria give different designs from the same support points.
- **First-order model on the cube.** For $f(x) = (1, x_1, \dots, x_k)$ on $[-1, 1]^k$, the full two-level [factorial design](/factorial-design/) has $M = I$ and $d(x) = 1 + \sum_jx_j^2 \le k + 1 = p$, so it is D-optimal. A regular [fractional factorial design](/fractional-factorial-design/) of resolution at least III, a [Plackett-Burman design](/plackett-burman-design/) or a two-level [orthogonal array](/orthogonal-array/) of strength 2 also has $M = I$ for this model and is D-optimal with far fewer runs.
- **Exact second-order design in two factors.** The model $f(x) = (1, x_1, x_2, x_1x_2, x_1^2, x_2^2)$ with $N = 6$ runs on the $3 \times 3$ grid $\{-1, 0, 1\}^2$: an exhaustive search over all 3003 multisets of 6 grid points gives the largest $\det X^\top X = 256$, reached for instance by the four corners, the center and the edge point $(-1, 0)$.

## Known algorithms

| method | designs | guarantee |
|---|---|---|
| vertex direction (Wynn 1970, Fedorov 1972) | approximate D | converges to the optimum; same update as [Khachiyan's algorithm](/khachiyans-algorithm/) |
| multiplicative weights (Silvey, Titterington and Torsney 1978) | approximate D, A, c | criterion increases at every step and converges (Yu 2010) |
| semidefinite and determinant maximization programs | approximate D, A, E | polynomial time by interior point methods (Vandenberghe, Boyd and Wu 1998) |
| [Fedorov exchange](/fedorov-exchange-algorithm/) | exact D | determinant increases at every exchange; stops at a local optimum |
| modified Fedorov, DETMAX, coordinate exchange | exact D and others | heuristics; local optima only, restarted from random designs |
| rounding of the approximate optimum | exact | efficiency close to 1 when $N$ is large compared with the support size |

**Vertex direction.** Find $x^+ = \arg\max_xd(x, \xi)$ and move weight toward it: $\xi \leftarrow (1 - \alpha)\xi + \alpha\delta_{x^+}$. The best step is $\alpha = (d^+ - p)/(p(d^+ - 1))$ with $d^+ = d(x^+, \xi)$. The value $\max_xd(x, \xi)$ is a stopping rule with a guarantee: the D-efficiency $(\det M(\xi)/\det M^*)^{1/p}$ is at least $p/\max_xd(x, \xi)$.

**Multiplicative algorithm.** On $n$ candidates, $w_i \leftarrow w_i\,d(x_i, \xi)/p$ for all $i$ at once. The weights stay positive and sum to 1, by Lemma 1 on the equivalence theorem page. On the 9 points $-1, -\frac34, \dots, 1$ for the quadratic model, from equal weights ($\det M = 0.0557$, $\max d = 5.95$), the determinant after 10 updates is 0.1399, after 50 updates 0.14790 with $\max d = 3.005$, and after 200 updates it equals $4/27 \approx 0.148148$ to 8 digits, with the weight on $-1$, $0$, $1$.

**Exact designs.** The exchange methods start from a random nonsingular design and move one point, or one coordinate of one point, while the criterion improves. They are fast and give no guarantee; the usual practice is many random starts and a report of the D-efficiency against the approximate optimum, which bounds the exact optimum from above.

## Bounds

- **Optimal value of the approximate problem.** At a D-optimal design $\max_xd(x, \xi^*) = p$, and $d(x_i, \xi^*) = p$ at the support points. Some D-optimal design has between $p$ and $p(p+1)/2$ support points, and the optimal moment matrix is unique (proofs on the [equivalence theorem](/kiefer-wolfowitz-equivalence-theorem/) page).
- **Exact against approximate.** Any exact design with $N$ runs is an approximate design with weights $k/N$, so $\det X^\top X \le N^p\det M^*$. In the two-factor example on the $3 \times 3$ grid, the approximate optimum puts weight about 0.1458 on each corner, 0.0802 on each edge midpoint and 0.0962 on the center, with $\det M^* \approx 0.011427$. The best exact designs for $N = 6, 7, 8, 9$ have $\det X^\top X = 256, 960, 2304, 5184$, so their D-efficiencies $(\det X^\top X/(N^p\det M^*))^{1/p}$ are 0.885, 0.945, 0.957 and 0.974: the gap shrinks as $N$ grows.
- **Hardness.** Welch (1982) proved that exact D-optimal design is NP-hard. The closely related problem of choosing $k$ vectors of largest volume is NP-hard and has no polynomial approximation scheme (Çivril and Magdon-Ismail 2009). So exact algorithms such as branch and bound are exponential in the worst case, and the exchange methods are heuristics.

## Reductions

- **Minimum volume enclosing ellipsoid.** For a finite candidate set, the approximate D-optimal design problem is the Lagrange dual of finding the [minimum volume enclosing ellipsoid](/minimum-volume-enclosing-ellipsoid/) centered at 0 of the points $f(x_i)$: at the optimum the ellipsoid is $\{z : z^\top M^{*-1}z \le p\}$, every $f(x_i)$ lies in it because $d(x_i, \xi^*) \le p$, and the support points lie on its boundary. Algorithms for one problem solve the other.
- **Semidefinite programming.** A-optimality is a semidefinite program in the weights, and E-optimality maximizes the smallest eigenvalue of a matrix linear in the weights. D-optimality is a determinant maximization problem.
- **Subset selection.** With a finite candidate list and $N = p$ runs, the exact D-optimal design chooses $p$ of the $n$ rows with the largest $|\det|$, a maximum volume submatrix problem.

## Applications

Optimal designs are used where runs are expensive and the model is trusted: chemical and process experiments with constrained regions in [response surface methodology](/response-surface-methodology/), dose finding and pharmacokinetic sampling times with nonlinear models, choice experiments in marketing, sensor placement, computer experiments, and the choice of measurements in linear bandits, where the G-optimal design bounds the worst prediction error. When randomization of treatments to units is the main goal, a [randomized experiment](/randomized-experiment/) with a classical design is used instead.

## References
