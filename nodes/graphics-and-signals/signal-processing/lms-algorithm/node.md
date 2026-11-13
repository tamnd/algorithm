---
tag: 7A11YC
kind: algorithm
slug: lms-algorithm
name: Least mean squares algorithm
aliases:
- LMS
- Widrow-Hoff rule
area: graphics-and-signals/signal-processing
level: core
summary: "Adapt the taps of an FIR filter on each sample by the stochastic gradient step w <- w + mu e u. It costs O(M) per sample, and the mean taps converge to the Wiener solution for 0 < mu < 2/lambda_max."
solves: [adaptive-filtering]
model: real-ram
complexity:
  vars: {M: the number of taps, N: the number of samples}
  time: {worst: O(N M)}
  space: {extra: O(M)}
properties: {deterministic: true, online: true, recursive: false, exact: false}
history:
  year: 1960
  people: [Bernard Widrow, Marcian E. Hoff]
  note: "Widrow and Hoff introduced the rule at Stanford in 1960 to train the ADALINE, an adaptive linear element, by estimating the gradient of the mean-square error from one sample."
prereqs: [adaptive-filtering, wiener-filter]
see_also: [rls-algorithm, stochastic-gradient-descent, gradient-descent, perceptron, linear-regression, eigenvalue, beamforming, linear-prediction]
sources:
  - paper: "B. Widrow and M. E. Hoff, Adaptive switching circuits, IRE WESCON Convention Record, Part 4, 1960"
    locator: "pages 96 to 104, the adaptive linear element and the rule that estimates the gradient of the mean-square error from the current error and input"
  - book: isbn:9780132671453
    title: "Simon Haykin, Adaptive Filter Theory, fifth edition, Pearson, 2014"
    locator: "Chapters 5 and 6 (the method of stochastic gradient descent, the LMS algorithm, its convergence in the mean and in the mean square, and the misadjustment)"
  - paper: doi:10.1109/PROC.1975.10036
    title: "B. Widrow, J. R. Glover, J. M. McCool and others, Adaptive noise cancelling: Principles and applications, Proceedings of the IEEE 63(12), 1975, pages 1692 to 1716"
    locator: "the adaptive noise canceller with a reference input, adapted by the LMS algorithm, and its applications"
  - book: isbn:9780131873742
    title: "John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007"
    locator: "Chapter 13 (adaptive filters: applications, and the LMS algorithm with its properties of convergence)"
---

The least mean squares (LMS) algorithm adapts the taps of an FIR filter while the data arrive, so that the output follows a desired signal in the least mean-square sense. It does not need the statistics of the signals. On each sample it computes the output $y = w^T u$ from the last $M$ inputs $u$, the error $e = d - y$, and the update $w \leftarrow w + \mu\, e\, u$. This is a step against the gradient of the instantaneous square error, an unbiased estimate of the gradient of the mean-square error, so LMS is [stochastic gradient descent](/stochastic-gradient-descent/) on the error surface of the [Wiener filter](/wiener-filter/). It costs $2M + 1$ multiplications per sample. Under the usual independence assumption, the mean of the taps converges to the Wiener solution if and only if $0 < \mu < 2/\lambda_{\max}$, where $\lambda_{\max}$ is the largest [eigenvalue](/eigenvalue/) of the input correlation matrix.

## In plain words

A filter mixes the last few input samples with a set of weights. You want its output to match a target signal, but you do not know the right weights. LMS starts from any weights. After each sample it looks at the error, the target minus the output. It then moves each weight a little: up if that input and the error have the same sign, down if they have opposite signs, by an amount proportional to both. Each move reduces the error on the current sample, and over many samples the weights settle near the best ones. A small step size gives slow but steady learning and weights that stay close to the best values. A large step size learns fast but jitters. A step size that is too large makes the weights grow without limit.

## The problem

The inputs are two sequences, an input signal $x[0], x[1], \ldots$ and a desired signal $d[0], d[1], \ldots$, a number of taps $M$, and a step size $\mu > 0$. At each time $n$ the algorithm must output an estimate $y[n] = \sum_{k=0}^{M-1} w_k[n]\, x[n-k]$ of $d[n]$, using only the data up to time $n$. The goal is that the taps approach the minimizer $w^\ast$ of the mean-square error $E[(d[n] - w^T u[n])^2]$, which solves the Wiener-Hopf equations $R w^\ast = p$ with $R = E[u u^T]$ and $p = E[d\, u]$, although $R$ and $p$ are not known. This is the problem of [adaptive filtering](/adaptive-filtering/).

## The algorithm

```pseudo id=main
LMS(x, d, M, μ)
L1  w ← (0, .., 0)                                ▷ M taps, or any start value
L2  for n ← 0, 1, 2, ... do
L3      u ← (x[n], x[n − 1], .., x[n − M + 1])    ▷ x[m] = 0 for m < 0
L4      y[n] ← wᵀ u
L5      e[n] ← d[n] − y[n]
L6      w ← w + μ · e[n] · u
L7  return w, y, e
```

Line L1 sets the start value; zero is usual, and a good guess speeds up convergence. Line L3 shifts the newest sample into the tap vector, the delay line of an FIR filter. Line L4 is the filter output and line L5 is its error. Line L6 is the update. The gradient of $e[n]^2$ with respect to $w$ is $-2\, e[n]\, u$, so line L6 is a step of length $\mu/2$ against it. The algorithm needs no matrix, no correlation estimate and no division. In the implementation, the function that runs lines L4 to L6 also takes any regressor vector $u$, not only a delay line, as in [beamforming](/beamforming/) or [linear regression](/linear-regression/).

## Example

Identify the unknown system $d[n] = x[n] + \frac12 x[n-1]$ with $M = 2$, $\mu = \frac14$, $w = (0, 0)$, on the input $x = (1, -1, 2, 0, 1, -2)$, which gives $d = (1, -\frac12, \frac32, 1, 1, -\frac32)$.

| $n$ | $u$ (line L3) | $y[n]$ (line L4) | $e[n]$ (line L5) | $w$ after line L6 |
|---|---|---|---|---|
| 0 | $(1, 0)$ | $0$ | $1$ | $(1/4,\ 0)$ |
| 1 | $(-1, 1)$ | $-1/4$ | $-1/4$ | $(5/16,\ -1/16)$ |
| 2 | $(2, -1)$ | $11/16$ | $13/16$ | $(23/32,\ -17/64)$ |
| 3 | $(0, 2)$ | $-17/32$ | $49/32$ | $(23/32,\ 1/2)$ |
| 4 | $(1, 0)$ | $23/32$ | $9/32$ | $(101/128,\ 1/2)$ |
| 5 | $(-2, 1)$ | $-69/64$ | $-27/64$ | $(1,\ 101/256)$ |

At $n = 3$ the first input is zero, so only $w_1$ changes, by $\frac14 \cdot \frac{49}{32} \cdot 2 = \frac{49}{64}$. After six samples the taps are $(1, 0.395)$, against the true $(1, 0.5)$. With no noise in $d$, LMS keeps moving toward $(1, \frac12)$ on every input that excites both taps.

For the mean behavior, let the regressor $u$ be one of $(1, 1)$, $(1, 0)$ and $(0, 1)$ with equal probability, independently at each step. Then $R = \frac13 \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$, with eigenvalues $1$ and $\frac13$, so $\lambda_{\max} = 1$ and the bound is $\mu < 2$. The tests average the taps over all $3^n$ input sequences in exact arithmetic. The mean converges for $\mu = \frac12$ and $\mu = \frac{19}{10}$. For $\mu = 2$ it oscillates: the mean error along the eigenvector $(1, 1)$ changes sign at each step and keeps its size. For $\mu = \frac52$ it grows like $(\frac32)^n$.

## Correctness

**Claim.** Line L6 is a stochastic gradient step on the mean-square error. If the pairs $(u_n, d_n)$ are independent and identically distributed and $R$ is positive definite, then $E[w_n] - w^\ast = (I - \mu R)^n (w_0 - w^\ast)$, and $E[w_n] \to w^\ast$ from every start if and only if $0 < \mu < 2/\lambda_{\max}$.

**Key invariant.** The taps $w_n$ depend only on the data before time $n$. So under independence, the mean error $v_n = E[w_n] - w^\ast$ follows the deterministic recursion $v_{n+1} = (I - \mu R)\, v_n$, the recursion of [gradient descent](/gradient-descent/) with step $\mu/2$ on the error surface.

In the eigenvector coordinates of $R$, mode $i$ of the mean error is multiplied by $1 - \mu \lambda_i$ at each step, and it decays if and only if $|1 - \mu \lambda_i| < 1$. The full proof is below. It also shows that, on every sample, the error after the update is $(1 - \mu \|u\|^2)$ times the error before it.

## Complexity

Line L4 costs $M$ multiplications and line L6 costs $M + 1$, with $\mu e[n]$ formed once, so each sample costs $2M + 1$ multiplications and $2M$ additions, $O(M)$ time in the [real RAM](/real-ram/), and $N$ samples cost $O(NM)$. Line L3 is a shift of the delay line, $O(1)$ with a circular buffer. The extra space is $O(M)$ for $w$ and $u$. This is the lowest cost of any adaptive FIR algorithm, against $O(M^2)$ per sample for the [RLS algorithm](/rls-algorithm/).

## Properties

- **Mean convergence and its speed.** Mode $i$ of the mean error decays like $(1 - \mu \lambda_i)^n$, with time constant about $1/(\mu \lambda_i)$ samples for small $\mu$. The slowest mode belongs to $\lambda_{\min}$, so the eigenvalue spread $\lambda_{\max}/\lambda_{\min}$ of $R$ sets the speed: LMS is fast on white input and slow on strongly colored input.
- **A practical bound.** For a tapped delay line, $\lambda_{\max} \le \operatorname{tr} R = M\, r_x[0]$, $M$ times the input power. So $\mu < 2/(M\, r_x[0])$ guarantees convergence in the mean and needs no eigenvalue.
- **Mean-square convergence needs a smaller step.** The mean can converge while the taps themselves swing more and more. In the example with three regressors, $E\|w_n - w^\ast\|^2$ tends to zero only for $\mu < 3 - \sqrt3 \approx 1.268$, although the mean converges up to $\mu = 2$; the tests check that this second moment grows for $\mu = \frac{19}{10}$ and falls for $\mu = 1$.
- **Misadjustment.** With noise, the taps never settle: they jitter around $w^\ast$ and add an excess error. For small $\mu$, the excess error is about $\frac{\mu}{2} \operatorname{tr} R$ times the minimum error $J_{\min}$. A smaller step gives a smaller excess error and a slower convergence.
- **Tracking.** Because the step does not shrink, LMS follows slow changes of the statistics, with a lag that grows as $\mu$ falls.
- **Robustness.** LMS needs no model of the noise and no matrix inverse, and it does not break down on rank-deficient or nonstationary input. It is known to minimize the worst-case ratio of error energy to disturbance energy, an $H^\infty$ criterion.

## Variants and improvements

- **Normalized LMS.** Use the step $\tilde\mu / (\epsilon + \|u\|^2)$ with $0 < \tilde\mu < 2$ and a small $\epsilon > 0$. The step adapts to the input power, the algorithm converges for $0 < \tilde\mu < 2$ whatever the scale of the input, and $\tilde\mu = 1$ with $\epsilon = 0$ makes the error after the update zero. The implementation includes it.
- **Leaky LMS.** $w \leftarrow (1 - \mu\gamma) w + \mu e u$ minimizes the error plus $\gamma \|w\|^2$, as in [ridge regression](/ridge-regression/). It keeps the taps bounded when $R$ is singular.
- **Sign algorithms.** Replace $e$, $u$ or both by their signs in line L6. They need fewer multiplications and are common in hardware, and they converge more slowly.
- **Block and frequency-domain LMS.** Update once per block of $L$ samples with the summed gradient, and compute the convolution and the correlation with the [fast Fourier transform](/fast-fourier-transform/). For long filters, such as acoustic echo cancellers with thousands of taps, this cuts the cost to $O(\log M)$ per sample.
- **Complex LMS.** For complex signals, $y = w^H u$ and $w \leftarrow w + \mu\, \bar e\, u$, with the same bound. Adaptive [beamforming](/beamforming/) uses it.
- **Affine projection and RLS.** The affine projection algorithm uses the last $K$ input vectors and lowers the effect of colored input; the [RLS algorithm](/rls-algorithm/) whitens the input completely, at $O(M^2)$ per sample.

## When to use it

Use LMS when the statistics of the signals are unknown or change slowly, the filter is long or the hardware is small, and a modest convergence speed is acceptable: echo cancellation, channel equalization, noise cancellation with a reference input, and system identification. Use normalized LMS when the input power varies, as for speech. Use [RLS](/rls-algorithm/) when the input is strongly colored and fast convergence matters more than cost, and a [Kalman filter](/kalman-filter/) when a state-space model of the signals is available.

## Pitfalls

- **The factor 2 in the step.** Some texts write line L6 as $w \leftarrow w + 2\mu\, e\, u$, the full gradient step. Their bound is $\mu < 1/\lambda_{\max}$. Using a step from such a text in this line L6, or the reverse, changes the step by a factor of 2. Check the convention before you use a published bound.
- **A step too large for the input power.** A step that works for one input level diverges when the input is ten times stronger, because $\lambda_{\max}$ grows with the square of the level. Line L6 must use a step below $2/\lambda_{\max}$ for the largest input power expected, or the normalized step.
- **The output after the update.** Computing $y[n]$ in line L4 with the taps after line L6 uses $d[n]$ to predict itself. Line L4 must use the taps from before the update.
- **The wrong sign of the error.** With $e[n] = y[n] - d[n]$ in line L5 and the plus sign of line L6, the algorithm climbs the error surface and diverges for every step. Line L5 must be $d[n] - y[n]$.
- **Taps and inputs in the wrong order.** Line L3 must put $x[n]$ first, so that $w_k$ multiplies $x[n-k]$; a reversed delay line converges to the reversed impulse response or not at all.
- **Expecting exact convergence.** With noise in $d$, the taps keep moving by about $\mu\, e\, u$ on each sample. To read off the identified system, decrease $\mu$ over time or average the taps.

## Implementations

## History

Bernard Widrow and his student Marcian Hoff found the rule at Stanford in 1959 and published it in 1960 to train the ADALINE, an adaptive linear element for pattern classification. Their idea was to use the square of the current error as an estimate of the mean-square error and to follow its gradient. The same rule was called the delta rule in neural network work, and it was an early relative of the [perceptron](/perceptron/) rule. In the 1960s and 1970s LMS became the standard algorithm for adaptive equalizers in data modems, for echo cancellers on telephone lines and for adaptive antenna arrays. In 1975 Widrow and his colleagues described adaptive noise cancelling, in which LMS removes interference with the help of a reference input.

## References
