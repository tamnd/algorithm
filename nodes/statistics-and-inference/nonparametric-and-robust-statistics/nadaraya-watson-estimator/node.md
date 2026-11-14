---
tag: HA8PMS
kind: algorithm
slug: nadaraya-watson-estimator
name: Nadaraya-Watson estimator
aliases:
- kernel regression estimator
- local constant regression
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: Estimates a regression function at x by a weighted average of the responses, with kernel weights that fall with the distance of each x_i from x.
model: real-ram
complexity:
  vars: {n: the number of data points, q: the number of points where the estimate is wanted, m: the number of grid points}
  time: {worst: O(n q), binned: O(n + m log m)}
  space: {extra: O(1)}
properties: {deterministic: true, randomized: false, exact: true, linear_smoother: true, reproduces_constants: true, reproduces_lines: false}
history:
  year: 1964
  people: [E. A. Nadaraya, Geoffrey S. Watson]
  note: Nadaraya and Watson proposed the estimator independently in 1964, as the ratio of a kernel estimate of the joint density moment to a kernel density estimate of x.
prereqs: [kernel-density-estimation, conditional-expectation, weighted-least-squares]
see_also: [local-polynomial-regression, kde-bandwidth-selection, k-nearest-neighbors, smoothing-spline, kernel-ridge-regression, gaussian-process, regression-discontinuity-design, cross-validation]
sources:
  - paper: doi:10.1137/1109020
    title: E. A. Nadaraya, On estimating regression, Theory of Probability and Its Applications 9(1), 1964
    locator: pp. 141 to 142 (the estimator and its consistency)
  - paper: "Geoffrey S. Watson, Smooth regression analysis, Sankhyā Series A 26(4), 1964, pp. 359 to 372"
    locator: The whole paper (the same estimator, from a kernel estimate of the joint density)
  - book: isbn:9780412552700
    title: M. P. Wand and M. C. Jones, Kernel Smoothing, Chapman and Hall, 1995
    locator: Chapter 5 (kernel regression; the bias and variance of the local constant estimator, the design bias and the boundary bias)
  - book: isbn:9780412983214
    title: Jianqing Fan and Irène Gijbels, Local Polynomial Modelling and Its Applications, Chapman and Hall, 1996
    locator: Chapter 3 (the Nadaraya-Watson estimator as a local polynomial fit of degree 0, and its comparison with the local linear fit)
---

The Nadaraya-Watson estimator estimates a regression function $m(x) = \mathbb{E}[Y \mid X = x]$ without a model for its shape. At each point $x$, it takes a weighted average of the responses $y_i$, and the weights come from a kernel: points with $x_i$ near $x$ count much, distant points little or not at all. The bandwidth $h$ sets how near is near. It is the regression form of [kernel density estimation](/kernel-density-estimation/), and it is local polynomial regression of degree 0, a constant fitted by weighted least squares around each point. It reproduces a constant exactly, but not a line, so it has a bias of order $h$ at the ends of the data.

## In plain words

To guess the value of a curve at some place, look at the data points with nearby positions and average their values. Give close points more say than far points: a point right at the place gets the most weight, a point at the edge of the window gets almost none, and points outside the window get none.

This works well in the middle of the data, where there are neighbours on both sides. At the ends, all the neighbours lie on one side. If the curve rises there, the neighbours are all higher (or all lower) than the curve at the end, and the average is pulled away. The wider the window, the larger this error.

## The problem

The input is $n$ pairs $(x_1, y_1), \ldots, (x_n, y_n)$, a kernel $K \ge 0$ and a bandwidth $h > 0$. The model is $y_i = m(x_i) + e_i$ with errors of mean 0. The output is the estimate
$$\hat m_h(x) = \frac{\sum_{i=1}^n K\!\left(\frac{x - x_i}{h}\right) y_i}{\sum_{j=1}^n K\!\left(\frac{x - x_j}{h}\right)}$$
at each point $x$ where it is wanted. It is undefined where the denominator is 0, which happens with a compact kernel far from all the data. Equivalently, $\hat m_h(x)$ is the constant $\beta_0$ that minimizes $\sum_i K((x - x_i)/h)\,(y_i - \beta_0)^2$, a [weighted least squares](/weighted-least-squares/) fit of degree 0.

## The algorithm

```pseudo id=main
NADARAYA-WATSON(x, (x_1, y_1), ..., (x_n, y_n), h)
L1  num ← 0;  den ← 0
L2  for i ← 1 to n do  w ← K((x − x_i)/h)
L3      num ← num + w · y_i;  den ← den + w
L4  if den = 0 then return undefined          ▷ no data within the kernel's reach
L5  return num / den
```

The numerator divided by $nh$ estimates $m(x) f(x)$, and the denominator divided by $nh$ is a kernel density estimate of $f(x)$, the density of the $x_i$. Their ratio estimates $m(x)$. That is how Watson derived it.

For many points on a grid, both sums are discrete convolutions of binned data with the sampled kernel, so the FFT method of kernel density estimation computes the whole curve in $O(n + m\log m)$ time. To choose $h$, the code minimizes the leave-one-out prediction error $\frac1n\sum_i (y_i - \hat m_{h,-i}(x_i))^2$. The estimate without point $i$ is $(N_i - K(0)y_i)/(D_i - K(0))$, where $N_i$ and $D_i$ are the full sums at $x_i$, so each score costs $O(n^2)$ and not $O(n^3)$.

## Example

Seven points on the line $y = 2x$, at $x = 0, 1, \ldots, 6$, with the Epanechnikov kernel $K(u) = \frac34(1 - u^2)$ on $[-1, 1]$ and $h = 2$. At $x = 0$, the point 0 has $u = 0$ and weight $K(0) = 3/4$, the point 1 has $u = -1/2$ and weight $9/16$, and the point 2 is at the edge with weight 0. So
$$\hat m(0) = \frac{\frac34 \cdot 0 + \frac9{16}\cdot 2}{\frac34 + \frac9{16}} = \frac{9/8}{21/16} = \frac67 \approx 0.857.$$

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| true $m(x) = 2x$ | 0 | 2 | 4 | 6 | 8 | 10 | 12 |
| $\hat m(x)$, $h = 2$ | 6/7 | 2 | 4 | 6 | 8 | 10 | 78/7 |
| $\hat m(x)$, $h = 3$ | 18/11 | 8/3 | 4 | 6 | 8 | 28/3 | 114/11 |

At $x = 1, \ldots, 5$ with $h = 2$, the neighbours lie symmetrically on both sides, and the estimate is exact. At the two ends it is pulled toward the inside by $6/7$. With $h = 3$ the error at the ends grows to $18/11 \approx 1.64$, and it reaches $x = 1$ and $x = 5$ as well. If all the $y_i$ were equal to one constant, the estimate would equal that constant everywhere. The test file checks these values in exact arithmetic.

## Correctness

The weights $w_i(x) = K((x - x_i)/h)/\sum_j K((x - x_j)/h)$ are non-negative and sum to 1, so the estimate is a convex combination of the responses. If all $y_i = c$, it is exactly $c$, and it always lies between the smallest and the largest $y_i$. For a line $m(x) = a + bx$ the error is $b\sum_i w_i(x)(x_i - x)$, which is 0 only when the weighted mean of the $x_i$ is $x$. At the end point 0 of an equally spaced design on $[0, 1]$, with $m$ twice differentiable, the bias is
$$\mathbb{E}\,\hat m(0) - m(0) = h\,m'(0)\,\frac{\int_0^1 uK(u)\,du}{\int_0^1 K(u)\,du} + O\!\left(h^2 + \frac1N\right),$$
which is $\frac38 h\,m'(0)$ for the Epanechnikov kernel: a bias of order $h$, not $h^2$. At interior design points the neighbours are symmetric, the linear term cancels, and the bias is $O(h^2)$. The full proofs are below; the bias and variance for a random design are cited.

## Complexity

- **One point.** Lines L1 to L5 take $O(n)$ time and $O(1)$ extra space. For $q$ points, $O(nq)$.
- **Compact kernel and sorted data.** Only the points within $h$ of $x$ count. Binary search finds them, so a point costs $O(\log n + k)$ for $k$ points in the window, and a sweep over sorted query points updates the two sums as the window moves.
- **Grid.** With linear binning, two FFT convolutions give the numerator and the denominator on $m$ grid points in $O(n + m\log m)$ time.
- **Choosing $h$.** Leave-one-out cross-validation costs $O(n^2)$ for each candidate bandwidth.

## Properties

- **Linear smoother.** $\hat m = W y$ with weights that depend only on the $x_i$, so the variance and the leave-one-out residuals have simple formulas.
- **Rate.** In the interior, the bias is $h^2\mu_2\big(\tfrac12 m'' + m'f'/f\big)$ and the variance $\sigma^2 R(K)/(nhf(x))$, to first order, where $f$ is the density of the $x_i$. With the best $h$ of order $n^{-1/5}$, the mean squared error falls like $n^{-4/5}$ (Wand and Jones 1995). These are cited, not proved here.
- **Design bias.** The term $m'f'/f$ means the estimate is biased where the design density changes, even for a straight line. The [local linear](/local-polynomial-regression/) fit has no such term.
- **Boundary bias.** Of order $h$ at the ends of the data, as in the example and the theorem above.
- **Bounded output.** The estimate never leaves the range of the responses, so it never overshoots. This is useful for probabilities and other bounded responses, and the reason why it flattens peaks.

## Variants and improvements

- **Local polynomial regression.** Fit a line, not a constant, in each window. [Local linear regression](/local-polynomial-regression/) removes the boundary bias and the design bias, at a small cost in variance.
- **Nearest-neighbour windows.** Use the $k$ nearest $x_i$ instead of a fixed $h$, so the window widens where the data are sparse; with a uniform kernel this is [k-nearest neighbour](/k-nearest-neighbors/) regression.
- **Gasser-Müller and Priestley-Chao.** Weights from the spacing of a fixed design instead of a density estimate. They have no design bias, but a larger variance for random designs.
- **Boundary kernels.** Kernels that change shape near the ends of the data, so that the first moment of the weights is 0 there.
- **Several predictors.** Use a product kernel or a kernel on a distance. The rate becomes $n^{-4/(d+4)}$, and the method needs very many points for more than a few predictors.
- **Classification.** With $y_i \in \{0, 1\}$, the estimate is a smoothed class proportion, a kernel classifier.

## When to use it

Use it for a quick smooth curve through a scatter plot, for a nonparametric estimate of a conditional mean or a conditional probability, and as a building block, for example inside kernel estimates of conditional densities. Its output stays within the range of the data, which suits bounded responses. When the curve matters near the ends of the data, or when the $x_i$ are unevenly spread, prefer a local linear fit. When you need a smooth function with good extrapolation, consider a [smoothing spline](/smoothing-spline/) or a [Gaussian process](/gaussian-process/).

## Pitfalls

- **Bias at the boundary.** A rising curve is estimated too low at its right end and too high at its left end, or the opposite for a falling curve. In a [regression discontinuity design](/regression-discontinuity-design/), the effect is estimated exactly at a boundary, and the Nadaraya-Watson estimate is biased there; local linear fits are the standard choice.
- **Empty windows.** With a compact kernel and a small $h$, the estimate is undefined in gaps of the data. Use a kernel with unbounded support, a larger $h$, or nearest-neighbour windows.
- **The bandwidth for density is not the bandwidth for regression.** A bandwidth chosen for the density of the $x_i$ ignores how fast $m$ changes. Use cross-validation on the prediction error, or a plug-in rule for regression.
- **Outliers in $y$.** The estimate is a weighted mean, so one wild response moves it. A robust local fit, such as LOWESS, guards against this.
- **Heteroscedastic errors.** The variance of the estimate follows $\sigma^2(x)/f(x)$; confidence bands must allow for it.

## Implementations

## History

Nadaraya and Watson published the estimator independently in 1964. Nadaraya proved its consistency; Watson derived it as the ratio of kernel estimates and applied it to data. Priestley and Chao (1972) and Gasser and Müller (1979) proposed weights for fixed designs. In the early 1990s, Fan showed that the local linear fit has better bias at the boundary and in designs that are not uniform, with the same variance order. Since then the Nadaraya-Watson estimator has been seen as the degree 0 case of local polynomial regression.

## References
