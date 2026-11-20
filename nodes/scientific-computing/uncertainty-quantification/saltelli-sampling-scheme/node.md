---
tag: SEW99Y
kind: algorithm
slug: saltelli-sampling-scheme
name: Saltelli sampling scheme
aliases:
- Saltelli estimator
area: scientific-computing/uncertainty-quantification
level: core
summary: Estimates all first order and total Sobol indices from two sample matrices and their column swaps, at N(d + 2) model runs, or N(2d + 2) with second order indices.
model: real-ram
complexity:
  vars: {N: the number of rows of each sample matrix, d: the number of inputs, F: the cost of one model run}
  time: {worst: O(N d F + N d^2)}
  space: {extra: O(N d)}
properties: {deterministic: false, randomized: true, exact: false, iterative: false}
history:
  year: 2002
  people: [Andrea Saltelli, Ilya M. Sobol, Michiel J. W. Jansen, Toshimitsu Homma]
  note: Sobol estimated first order indices with two sample matrices in 1990. Homma and Saltelli added total indices in 1996, Jansen gave the total estimator used here in 1999, and Saltelli arranged all indices at N(d + 2) runs in 2002.
prereqs: [sobol-indices, monte-carlo-integration]
see_also: [sobol-indices, hoeffding-sobol-decomposition, morris-method, fourier-amplitude-sensitivity-test, sobol-sequence, quasi-monte-carlo-integration, latin-hypercube-sampling, polynomial-chaos-expansion]
sources:
  - paper: doi:10.1016/S0010-4655(02)00280-1
    title: Andrea Saltelli, Making best use of model evaluations to compute sensitivity indices, Computer Physics Communications 145(2), 2002, 280-297
    locator: the design with the matrices A, B and the column swaps, N(d + 2) runs for first order and total indices and N(2d + 2) runs with second order indices
  - paper: doi:10.1016/j.cpc.2009.09.018
    title: Andrea Saltelli, Paola Annoni, Ivano Azzini, Francesca Campolongo, Marco Ratto and Stefano Tarantola, Variance based sensitivity analysis of model output. Design and estimator for the total sensitivity index, Computer Physics Communications 181(2), 2010, 259-270
    locator: the comparison of estimators, the first order estimator f(B)(f(AB_i) - f(A)) and the recommendation of the Jansen total estimator
  - paper: doi:10.1016/S0010-4655(98)00154-4
    title: Michiel J. W. Jansen, Analysis of variance designs for model output, Computer Physics Communications 117(1-2), 1999, 35-43
    locator: the estimator of the total variance from squared differences of runs that differ in one input
  - paper: doi:10.1016/0951-8320(96)00002-6
    title: Toshimitsu Homma and Andrea Saltelli, Importance measures in global sensitivity analysis of nonlinear models, Reliability Engineering and System Safety 52(1), 1996, 1-17
    locator: the total sensitivity index and its Monte Carlo estimate
  - paper: "Ilya M. Sobol, Sensitivity estimates for nonlinear mathematical models, Mathematical Modeling and Computational Experiment 1(4), 1993, 407-414"
    locator: the Monte Carlo estimate of the first order indices with two independent samples (translation of the 1990 Russian paper)
  - book: isbn:9780470059975
    title: Andrea Saltelli, Marco Ratto, Terry Andres, Francesca Campolongo, Jessica Cariboni, Debora Gatelli, Michaela Saisana and Stefano Tarantola, Global Sensitivity Analysis, The Primer, Wiley, 2008
    locator: Chapter 4 (variance-based methods and the computation of first order and total indices)
  - paper: doi:10.1109/ISUMA.1990.151285
    title: Tsutomu Ishigami and Toshimitsu Homma, An importance quantification technique in uncertainty analysis for computer models, Proceedings of the First International Symposium on Uncertainty Modeling and Analysis (ISUMA 1990), IEEE, 1990, 398-403
    locator: the test function sin x1 + a sin^2 x2 + b x3^4 sin x1
---

The Saltelli sampling scheme estimates all first order and all total [Sobol indices](/sobol-indices/) of a model with $d$ independent inputs from one set of $N(d + 2)$ model runs. It draws two independent sample matrices $A$ and $B$ with $N$ rows, and builds $d$ more matrices $AB_i$: the matrix $A$ with its column $i$ taken from $B$. Two rows that share all inputs but $x_i$ tell how much the output moves with $x_i$ alone, and two rows that share only $x_i$ tell how much of the output is fixed by $x_i$. Averages of products and squared differences of the outputs then give unbiased estimates of the conditional variances in the definitions. The scheme is a design of model runs. It is not the [Sobol sequence](/sobol-sequence/), a low discrepancy point set by the same author, although the rows of $A$ and $B$ are often taken from one, which turns the plain Monte Carlo estimate into [quasi-Monte Carlo integration](/quasi-monte-carlo-integration/).

## In plain words

You want to know which inputs of a model matter most. A simple way is slow: fix one input, vary all the others many times, and repeat for many values of the fixed input. The Saltelli scheme gets the same numbers with far fewer runs.

Make two random tables of inputs. Then, for each input, make a mixed table: the first table with that one column copied from the second. Run the model on every row of every table. If changing one column changes the output a lot, the input matters a lot in total. If the second table and the mixed table, which share only that column, give outputs that rise and fall together, the input matters a lot on its own. A few averages turn these comparisons into shares of the output spread.

## The problem

The input is a model $Q = f(\xi)$ with independent inputs $\xi = (\xi_1, \ldots, \xi_d)$ of known laws, and $D = \mathrm{Var}(Q) > 0$. The output is estimates of the first order and the total indices

$$S_i = \frac{\mathrm{Var}(\mathbb{E}[Q \mid \xi_i])}{D}, \qquad S_{Ti} = \frac{\mathbb{E}[\mathrm{Var}(Q \mid \xi_{\sim i})]}{D}, \qquad i = 1, \ldots, d,$$

where $\xi_{\sim i}$ is the vector of all inputs except $\xi_i$. The cost is the number of model runs; everything else is cheap.

## The algorithm

```pseudo id=main
SALTELLI(f, d, N, DRAW)
L1  A, B ← two independent N × d matrices; each row is a draw of ξ by DRAW
L2  y_A ← f(rows of A), y_B ← f(rows of B)                    ▷ 2N runs
L3  D ← sample variance of the 2N values y_A, y_B
L4  for i = 1..d do
L5      AB_i ← A with its column i replaced by column i of B
L6      y_ABi ← f(rows of AB_i)                                ▷ N runs
L7      t1_j ← y_B[j] (y_ABi[j] - y_A[j]) for j = 1..N
L8      t2_j ← (y_A[j] - y_ABi[j])^2 / 2 for j = 1..N
L9      S_i ← mean(t1) / D,  S_Ti ← mean(t2) / D
L10 return S_1..S_d, S_T1..S_Td and the run count N(d + 2)
```

Line L5 is the column swap. A row of $AB_i$ shares $\xi_{\sim i}$ with the same row of $A$ and only $\xi_i$ with the same row of $B$. Line L7 is the first order estimator of Saltelli et al. (2010): given $\xi_i$, the outputs of $B$ and $AB_i$ are independent with the common mean $\mathbb{E}[Q \mid \xi_i]$, so the mean of their product is $\mathbb{E}[\mathbb{E}[Q \mid \xi_i]^2]$, and subtracting $y_A$ removes $\mathbb{E}[Q]^2$. Line L8 is the total estimator of Jansen (1999): given $\xi_{\sim i}$, the outputs of $A$ and $AB_i$ are two independent draws, and half the mean squared difference of two such draws is the conditional variance. Line L3 uses all $2N$ independent outputs for the denominator.

## Example

The Ishigami function $f(x) = \sin x_1 + 7 \sin^2 x_2 + 0.1\, x_3^4 \sin x_1$ with inputs uniform on $[-\pi, \pi]^3$ is a standard test. Its exact values are $\mathbb{E}[Q] = 3.5$, $D = 13.84459$ and

| input | $S_i$ exact | $S_{Ti}$ exact |
|---|---|---|
| $x_1$ | 0.3139 | 0.5576 |
| $x_2$ | 0.4424 | 0.4424 |
| $x_3$ | 0 | 0.2437 |

They follow from $V_1 = \frac{1}{2}(1 + 0.1\pi^4/5)^2$, $V_2 = 49/8$ and the interaction $V_{13} = 0.01\, \pi^8 (1/18 - 1/50)$. The input $x_3$ has no effect alone, but acts through its product with $\sin x_1$; $x_2$ has no interaction.

A run with `random.Random(2002)` gives (a measurement):

| $N$ | runs | $\widehat{S}_1, \widehat{S}_2, \widehat{S}_3$ | $\widehat{S}_{T1}, \widehat{S}_{T2}, \widehat{S}_{T3}$ |
|---|---|---|---|
| 1000 | 5000 | 0.3074, 0.4637, -0.0141 | 0.5011, 0.4624, 0.2546 |
| 10000 | 50000 | 0.3092, 0.4503, 0.0118 | 0.5562, 0.4425, 0.2414 |

At $N = 10000$ the standard errors of the first order estimates are about 0.0145, 0.0124 and 0.0112, and those of the total estimates about 0.0151, 0.0050 and 0.0049, so all six estimates are within one or two standard errors of the exact values. The estimate $-0.0141$ at $N = 1000$ is a negative estimate of a zero index, which is a normal sampling error. The gap $\widehat{S}_{T3} - \widehat{S}_3$ shows the interaction of $x_3$ at both sizes.

## Correctness

The claim is that the means in line L9 are unbiased for the numerators $V_i = \mathrm{Var}(\mathbb{E}[Q \mid \xi_i])$ and $V_{Ti} = \mathbb{E}[\mathrm{Var}(Q \mid \xi_{\sim i})]$, that $D$ is unbiased for the variance, and that the ratios converge almost surely to $S_i$ and $S_{Ti}$ as $N \to \infty$. The key fact is that a row of $AB_i$ has the law of $\xi$, because the inputs are independent; it shares exactly the right inputs with the rows of $A$ and $B$, and the two conditional independence arguments above then give the two numerators. The strong law of large numbers gives convergence, and the [central limit theorem](/central-limit-theorem/) gives standard errors of order $N^{-1/2}$. The full proof is in the proof file. The ratios themselves have a bias of order $1/N$.

## Complexity

The scheme makes $2N$ runs in line L2 and $N$ in each of the $d$ passes of line L6, which is $N(d + 2)$ runs, or $O(N d F)$ time for a run cost $F$. Building each $AB_i$ copies $N$ rows of length $d$, which is $O(N d^2)$ arithmetic in the [real RAM](/real-ram/) model; a version that changes one entry of a row in place needs only $O(N d)$. Lines L7 to L9 cost $O(N)$ per input. The matrices $A$ and $B$ take $O(N d)$ space, and the outputs $O(N)$ per pass. A double loop that estimates each $V_i$ by an inner and an outer sample needs $N_{\mathrm{outer}} N_{\mathrm{inner}}$ runs per input instead.

## Properties

- **Unbiased numerators.** Both numerators are unbiased for every $N$; the indices are ratios and are only consistent.
- **Exact zeros.** If $f$ does not depend on $\xi_i$, then $y_{AB_i} = y_A$ row by row, and both estimates of input $i$ are exactly 0.
- **One design for all indices.** The same runs give all $2d$ indices; adding an input costs $N$ more runs.
- **Randomized.** The estimates are random; negative estimates of small indices and first order estimates above the total estimate happen at small $N$.
- **Independent inputs only.** The mixed rows are draws of $\xi$ only if the inputs are independent.

## Variants and improvements

- **Second order indices.** Add the $d$ matrices $BA_i$, the matrix $B$ with its column $i$ from $A$. A row of $BA_i$ and the same row of $AB_j$ share exactly $\xi_i$ and $\xi_j$, so the mean of $y_{BA_i} y_{AB_j}$ minus $\mathbb{E}[Q]^2$ estimates $\mathrm{Var}(\mathbb{E}[Q \mid \xi_i, \xi_j])$, and subtracting $V_i$ and $V_j$ gives $V_{ij}$. This costs $N(2d + 2)$ runs for all first order, second order and total indices (Saltelli 2002).
- **Other estimators.** Sobol's original first order estimator is the mean of the products of two outputs that share only $\xi_i$, minus the squared sample mean; it loses precision when $|\mathbb{E}[Q]|$ is large against the standard deviation. Other total estimators exist, for example that of Homma and Saltelli; Saltelli et al. (2010) compare several and recommend Jansen's.
- **Quasi-random rows.** Take the rows of $A$ and $B$ from one $2d$-dimensional [Sobol sequence](/sobol-sequence/), the first $d$ coordinates for $A$ and the last $d$ for $B$. For smooth models the error then falls faster than $N^{-1/2}$.
- **Error bars by bootstrap.** Resample the rows with replacement and recompute the indices, to get confidence intervals that include the error of $D$.
- **Surrogate models.** For an expensive model, compute the indices of a [polynomial chaos expansion](/polynomial-chaos-expansion/) of it instead; they follow from its coefficients without sampling.

## When to use it

Use the Saltelli scheme when you need quantitative first order and total indices with error bars, the inputs are independent, and you can afford $N(d + 2)$ runs with $N$ in the hundreds to thousands. Use the [Morris method](/morris-method/) first when $d$ is large and runs are expensive, to screen out the inputs that do not matter. Use the [Fourier amplitude sensitivity test](/fourier-amplitude-sensitivity-test/) when the model is smooth and the cost per index must be lower, and a bias without error bars is acceptable. Use a [polynomial chaos expansion](/polynomial-chaos-expansion/) when the model is smooth in few inputs and a surrogate fits it well. For dependent inputs, none of these variance splits holds; use a method built for dependence, for example indices based on the [Shapley value](/shapley-value/).

## Pitfalls

- **Dependent inputs.** Line L5 builds rows with $\xi_i$ from one draw and $\xi_{\sim i}$ from another. With dependent inputs these rows can be inputs that the real system never takes, and the estimates are not conditional variances. Transform to independent inputs first, if the model allows it.
- **The variance of one matrix.** Line L3 can use $y_A$ alone, but then $D$ comes from $N$ values instead of $2N$, and its sampling error is larger at no saving in runs. Use the pooled values.
- **The original first order estimator with a large mean.** Replacing line L7 by the mean of $y_B\, y_{AB_i}$ minus the squared sample mean subtracts two large numbers when $|\mathbb{E}[Q]|$ is large, and the estimate loses digits. Line L7 subtracts $y_A$ inside the sum, which is robust to a shift of $f$.
- **Swapping the roles of A and B.** Line L7 pairs $AB_i$ with $B$ (shared $\xi_i$) and line L8 pairs it with $A$ (shared $\xi_{\sim i}$). If the matrix is built as $B$ with column $i$ from $A$, the two pairings must swap too, or the first order estimator estimates the total one and the other way round.
- **Reading noise as a result.** A small negative $\widehat{S}_i$, or $\widehat{S}_i > \widehat{S}_{Ti}$, is sampling error at small $N$. Report the indices with their standard errors.

## Implementations

## History

Sobol published the Monte Carlo estimate of first order indices with two independent samples in Russian in 1990; the English translation appeared in 1993. Homma and Saltelli introduced the total sensitivity index in 1996, with its estimate. Jansen gave the estimator of the total variance from squared differences in 1999. Saltelli showed in 2002 how one design of $N(d + 2)$ runs gives all first order and total indices, and $N(2d + 2)$ runs also all second order ones. Saltelli and coauthors compared the estimators in 2010 and recommended the forms of lines L7 and L8. Ishigami and Homma had proposed the test function of the example in 1990.

## References
