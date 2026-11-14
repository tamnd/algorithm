---
tag: AWK35P
kind: technique
slug: response-surface-methodology
name: Response surface methodology
aliases:
- central composite design
- Box-Wilson method
area: statistics-and-inference/causal-inference-and-experimental-design
level: advanced
summary: Box and Wilson's sequence of designed experiments and fitted quadratic models that climbs toward the optimum of a response. Central composite designs fit the quadratic.
prereqs: [factorial-design, linear-regression, ordinary-least-squares, positive-definite-matrix, gradient]
see_also: [optimal-experimental-design, fractional-factorial-design, plackett-burman-design, balanced-incomplete-block-design, kiefer-wolfowitz-equivalence-theorem, fedorov-exchange-algorithm, hill-climbing, symmetric-eigenproblem]
sources:
  - paper: doi:10.1111/j.2517-6161.1951.tb00067.x
    title: "G. E. P. Box and K. B. Wilson, On the experimental attainment of optimum conditions, Journal of the Royal Statistical Society, Series B 13(1), 1951, pp. 1 to 38, with discussion pp. 38 to 45"
    locator: The whole paper (sequential first-order experiments with steepest ascent, composite designs for the second-order model and canonical analysis)
  - paper: doi:10.1214/aoms/1177707047
    title: "G. E. P. Box and J. S. Hunter, Multi-factor experimental designs for exploring response surfaces, Annals of Mathematical Statistics 28(1), 1957, pp. 195 to 241"
    locator: The whole paper (rotatable designs and the moment conditions for them)
  - paper: doi:10.1080/00401706.1960.10489912
    title: "G. E. P. Box and D. W. Behnken, Some new three level designs for the study of quantitative variables, Technometrics 2(4), 1960, pp. 455 to 475"
    locator: The whole paper (three-level second-order designs built from incomplete block designs)
  - book: isbn:9781118916018
    title: Raymond H. Myers, Douglas C. Montgomery and Christine M. Anderson-Cook, Response Surface Methodology, Process and Product Optimization Using Designed Experiments, fourth edition, Wiley, 2016
    locator: The chapters on the method of steepest ascent, the analysis of second-order response surfaces and experimental designs for fitting response surfaces (general locator)
  - book: isbn:9780898716047
    title: Friedrich Pukelsheim, Optimal Design of Experiments, SIAM Classics in Applied Mathematics 50, 2006 (reprint of the Wiley edition of 1993)
    locator: Chapter 15 (rotatability and response surface designs)
---

Response surface methodology (RSM) finds the settings of a few continuous factors that give the best value of a response, such as the yield of a chemical process, by a sequence of small designed experiments. Box and Wilson (1951) gave the strategy. Far from the optimum, a two-level [factorial design](/factorial-design/) fits a plane, and the next runs move along the path of steepest ascent of that plane. Near the optimum, the plane no longer fits, and a second-order design, most often a central composite design, fits a quadratic. The eigenvalues of the quadratic's matrix then say whether the fitted surface has a maximum, a minimum, a saddle or a ridge, and where it is.

## In plain words

You want to find the best settings of a process, but you can only learn about it by running it. So you climb a hill in the fog. First you take a few steps around where you stand and fit a flat slope to what you see. You walk uphill along that slope and keep checking until things stop getting better. There the ground is no longer flat, so you take a richer set of steps around the new spot, fit a curved bowl shape, and read off where its top is. Then you go there and confirm. Each stage uses a small, well planned set of runs, so you learn a lot from few trials.

## When it applies

- The factors are continuous and can be set at chosen levels, and the response changes smoothly with them, so that a plane fits a small region and a quadratic fits a larger one.
- Runs can be done in stages, and the result of one stage can guide the next.
- The number of factors is small, usually 2 to 5. With more, screen first with a [fractional factorial design](/fractional-factorial-design/) or a [Plackett-Burman design](/plackett-burman-design/).
- The error is moderate compared with the effects in the region. If the noise is large, the path of steepest ascent is poorly estimated.

It does not apply to categorical factors alone, where a factorial design with an [analysis of variance](/two-way-anova/) is the tool, or to a response with many local optima.

## The template

**1. Code the factors.** For each natural variable $\zeta_j$ with center $c_j$ and half-range $h_j$, use $x_j = (\zeta_j - c_j)/h_j$, so that the design runs at $x_j = \pm1$.

**2. First-order phase.** Run a $2^k$ factorial or a fraction of resolution III or more, plus $n_c$ center runs, and fit by [least squares](/ordinary-least-squares/)

$$\hat y = b_0 + \sum_{j=1}^kb_jx_j.$$

With runs at $\pm1$ and an orthogonal design, $b_j$ is half the main effect. Check for curvature: the difference $\bar y_F - \bar y_C$ of the means of the factorial runs and the center runs estimates $\sum_j\beta_{jj}$, the sum of the pure quadratic coefficients, and the center runs give a pure error estimate to test it. Check the two-factor interactions as well.

**3. Steepest ascent.** The [gradient](/gradient/) of the fitted plane is $b = (b_1, \dots, b_k)$. Make runs along the path $x(t) = t\,b/\lvert b_m\rvert$, where $m$ is the factor with the largest $\lvert b_m\rvert$, so that $x_m$ changes by 1 coded unit per step. Continue while the response improves; after one or two steps without improvement, make the best point the new center and go back to step 2. This is [hill climbing](/hill-climbing/) with a designed estimate of the slope.

**4. Second-order phase.** When curvature or interactions show up, run a second-order design. The central composite design (CCD) of Box and Wilson combines

- a $2^k$ factorial, or a fraction of resolution V, with $F$ runs at $x_j = \pm1$;
- $2k$ axial runs at distance $\alpha$ along each axis: $x_j = \pm\alpha$, the other coordinates 0;
- $n_c$ center runs.

The factorial part from step 2 can be reused, which is why the CCD fits a sequential strategy. Fit

$$\hat y = b_0 + x^\top b + x^\top Bx, \qquad B_{jj} = b_{jj}, \quad B_{jl} = B_{lj} = b_{jl}/2.$$

**5. Canonical analysis.** Setting the gradient $b + 2Bx$ to 0 gives the stationary point and its predicted value

$$x_s = -\tfrac12B^{-1}b, \qquad \hat y_s = b_0 + \tfrac12x_s^\top b.$$

With the spectral decomposition $B = P\Lambda P^\top$ ([symmetric eigenproblem](/symmetric-eigenproblem/)) and $w = P^\top(x - x_s)$, the fitted model is exactly

$$\hat y = \hat y_s + \sum_{j=1}^k\lambda_jw_j^2.$$

If all $\lambda_j < 0$ ($B$ negative definite, see [positive definite matrix](/positive-definite-matrix/)), $x_s$ is a maximum; if all $\lambda_j > 0$, a minimum; if the signs differ, a saddle. A $\lambda_j$ near 0 means a ridge: along the axis $w_j$ the response hardly changes, which leaves room to choose settings for cost or robustness. If $x_s$ lies far outside the design region, the fit cannot be trusted there; use ridge analysis (the best response on spheres of growing radius) instead.

**6. Confirm.** Run the process at the predicted best settings and compare the result with the prediction interval.

**Rotatability.** A design is rotatable if the prediction variance $\operatorname{Var}(\hat y(x))$ depends only on $\lVert x\rVert$, so no direction is favored before the optimum's direction is known. Box and Hunter (1957) showed that for a second-order design with zero odd moments this needs every pure fourth moment to be three times every mixed fourth moment: $\sum_ux_{uj}^4 = 3\sum_ux_{uj}^2x_{ul}^2$. For a CCD the left side is $F + 2\alpha^4$ and the right side is $3F$, so the CCD is rotatable exactly when $\alpha = F^{1/4}$: $\alpha = \sqrt2$ for $k = 2$, $\alpha = 8^{1/4} \approx 1.682$ for $k = 3$.

## Classic examples

**A two-stage climb.** Two factors in coded units. The first-order design is a $2^2$ factorial with 3 center runs:

| $x_1$ | $x_2$ | $y$ |
|---|---|---|
| $-1$ | $-1$ | 62.0 |
| $1$ | $-1$ | 65.0 |
| $-1$ | $1$ | 63.0 |
| $1$ | $1$ | 66.0 |
| $0$ | $0$ | 64.0, 63.8, 64.2 |

The fit is $\hat y = 64.0 + 1.5x_1 + 0.5x_2$. The interaction estimate is $(62 - 65 - 63 + 66)/4 = 0$, and $\bar y_F - \bar y_C = 64.0 - 64.0 = 0$, so the plane fits. The path of steepest ascent moves $x_2$ by $0.5/1.5 = 1/3$ for each unit of $x_1$. Runs at steps $1, 2, \dots, 7$ give 66.6, 70.1, 73.9, 77.2, 79.6, 78.4, 75.9. The best is step 5, at $(5, 5/3)$ in the old coded units, which becomes the new center.

Around it, a rotatable CCD with $\alpha = \sqrt2$ and 5 center runs (13 runs) gives:

| run | $(x_1, x_2)$ | $y$ |
|---|---|---|
| factorial | $(-1, -1), (1, -1), (-1, 1), (1, 1)$ | 76.0, 78.9, 78.1, 78.6 |
| axial | $(-\sqrt2, 0), (\sqrt2, 0), (0, -\sqrt2), (0, \sqrt2)$ | 76.3, 78.9, 77.7, 78.9 |
| center | $(0, 0)$ five times | 80.1, 79.8, 80.0, 80.2, 79.9 |

Least squares gives

$$\hat y = 80.000 + 0.885x_1 + 0.437x_2 - 0.600x_1x_2 - 1.213x_1^2 - 0.863x_2^2.$$

The residual sum of squares is 0.116 with 7 degrees of freedom. The 5 center runs give a pure error sum of squares of 0.100 with 4 degrees of freedom, so the lack of fit sum of squares is 0.016 with 3 degrees of freedom and $F = (0.016/3)/(0.100/4) = 0.21$: no sign of lack of fit. Here

$$B = \begin{pmatrix} -1.2125 & -0.3 \\ -0.3 & -0.8625 \end{pmatrix}, \qquad x_s = (0.331, 0.138), \qquad \hat y_s = 80.18,$$

and the eigenvalues of $B$ are $-0.690$ and $-1.385$. Both are negative, so $x_s$ is a maximum inside the region, and the response falls about twice as fast along the second canonical axis as along the first.

**Rotatability in numbers.** For this CCD, $X^\top X$ has the entries $13$ for the intercept, $8$ for each linear term, $4$ for the interaction, $12$ for each pure quadratic and $8$ for the cross terms of the intercept with each square, and $4$ between the two squares. The standardized prediction variance $f(x)^\top(X^\top X)^{-1}f(x)$ is $0.26875$ at every point at distance 1 from the center and $0.625$ at every point at distance $\sqrt2$, whatever the direction.

**Box-Behnken design.** For $k = 3$, take the 4 runs of a $2^2$ factorial in each of the 3 pairs of factors, with the third factor at 0, plus center runs: 12 edge midpoints of the cube and, for example, 3 centers, 15 runs in all at three levels per factor. It has no runs at the corners, which helps when the corners are expensive or unsafe. Box and Behnken (1960) built such designs from [balanced incomplete block designs](/balanced-incomplete-block-design/).

## Variations

- **Face-centered CCD** ($\alpha = 1$): three levels per factor and all runs in the cube, at the cost of rotatability.
- **Orthogonal blocking.** A CCD splits into a factorial block and an axial block; with the right $\alpha$ and center runs per block, the block effect is orthogonal to the model terms.
- **Optimal designs.** For constrained regions, odd run budgets or nonstandard models, compute a design by the criteria of [optimal experimental design](/optimal-experimental-design/), for example with the [Fedorov exchange algorithm](/fedorov-exchange-algorithm/). The [Kiefer-Wolfowitz theorem](/kiefer-wolfowitz-equivalence-theorem/) explains why such designs spread runs over the corners, the faces and the center.
- **Ridge analysis.** Maximize $\hat y$ on spheres $\lVert x\rVert = r$ for growing $r$; the solution solves $(B - \mu I)x = -\frac12b$ for a Lagrange multiplier $\mu$ larger than the largest eigenvalue.
- **Several responses.** Overlay contour plots, or maximize a desirability function that maps each response to $[0, 1]$ and combines them by a geometric mean.
- **Evolutionary operation.** Small factorial changes around the running process, repeated many times, so that the process climbs while it produces.
- **Computer experiments.** For expensive deterministic simulations, a Gaussian process model and Bayesian optimization replace the quadratic.

## Pitfalls

- **Scale dependence.** The path of steepest ascent depends on the coding. Doubling the half-range of a factor doubles its coefficient per coded unit, and the path in the natural units turns toward that factor. The canonical analysis is also in coded units.
- **Extrapolation.** A quadratic fit describes the region of the design only. A stationary point outside it, or a saddle, is a direction to explore, not an answer.
- **Too few center runs.** Without them there is no pure error, no test of lack of fit, and a poor estimate of the prediction variance near the center.
- **A plane fitted over curvature.** If $\bar y_F - \bar y_C$ is large, the first-order fit is wrong and steepest ascent can point the wrong way. Move to the second-order phase.
- **Noise and drift.** Randomize the run order within each stage. A drift in time looks like a factor effect, and a steepest ascent path run in order is exposed to it.
- **Many factors.** A CCD in $k$ factors has at least $2^{k-q} + 2k + 1$ runs. Screen to the few important factors first.

## Exercises

1. Show that the fitted second-order model equals $\hat y_s + (x - x_s)^\top B(x - x_s)$ exactly, and derive $\hat y_s = b_0 + \frac12x_s^\top b$.
2. For a CCD with a $2^{5-1}$ fraction of resolution V, give the number of runs with 6 center points and the rotatable $\alpha$. (Answer: $16 + 10 + 6 = 32$ runs, $\alpha = 16^{1/4} = 2$.)
3. In the climb above, change the coding of $x_2$ so that its half-range doubles. Compute the new path of steepest ascent in the old units and show that it differs from the first one.
4. Prove that a $2^k$ factorial with center runs cannot estimate the pure quadratic coefficients separately: all the columns $x_j^2$ are equal.
5. For the fitted model of the example, find the canonical axes $P$ and the predicted response at $x_s + 1.0\,p_1$ and at $x_s + 1.0\,p_2$, where $p_1, p_2$ are the unit eigenvectors.

## References
