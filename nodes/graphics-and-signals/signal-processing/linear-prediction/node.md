---
tag: TWX23X
kind: problem
slug: linear-prediction
name: Linear prediction
aliases:
- autoregressive modelling
area: graphics-and-signals/signal-processing
level: core
summary: "Find the p coefficients that predict each sample of a stationary signal from the p samples before it with the least mean-square error. They solve the Toeplitz normal equations."
prereqs: [autocorrelation, toeplitz-system-solving]
see_also: [levinson-durbin-recursion, linear-predictive-coding, burg-method, wiener-filter, predictive-coding, power-spectral-density, spectral-estimation, lms-algorithm]
sources:
  - paper: doi:10.1109/PROC.1975.9792
    title: "John Makhoul, Linear prediction: A tutorial review, Proceedings of the IEEE 63(4), 1975, pages 561 to 580"
    locator: "the least-squares formulation, the autocorrelation and covariance methods, and the minimum prediction error as a function of the order"
  - book: isbn:9780131873742
    title: "John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007"
    locator: "Chapter 12, Linear Prediction and Optimum Linear Filters (Section 12.3 forward and backward linear prediction, Section 12.4 solution of the normal equations, Section 12.5 properties of the linear prediction-error filters)"
  - book: isbn:9780132671453
    title: "Simon Haykin, Adaptive Filter Theory, fifth edition, Pearson, 2014"
    locator: "Chapter 3, Linear Prediction"
  - book: isbn:9780387974293
    title: "Peter J. Brockwell and Richard A. Davis, Time Series: Theory and Methods, second edition, Springer, 1991"
    locator: "Section 5.8, Kolmogorov's formula (Theorem 5.8.1, the one-step prediction error from the infinite past)"
  - paper: "N. Levinson, The Wiener RMS (root mean square) error criterion in filter design and prediction, Journal of Mathematics and Physics 25, 1947"
    locator: "pages 261 to 278, the recursive solution of the Toeplitz normal equations"
---

Linear prediction is the problem of estimating each sample $x[n]$ of a signal as a fixed linear combination of the $p$ samples before it, $\hat x[n] = \sum_{k=1}^{p} a_k\, x[n-k]$, with coefficients $a_1, \ldots, a_p$ that make the mean-square prediction error as small as possible. For a real wide-sense stationary signal with [autocorrelation](/autocorrelation/) $r[k]$, the best coefficients solve the $p \times p$ symmetric Toeplitz system $\sum_{k} a_k\, r[|i - k|] = r[i]$, the normal equations (also called the Yule-Walker equations). The [Levinson-Durbin recursion](/levinson-durbin-recursion/) solves this system in $O(p^2)$ operations. The prediction-error filter $A(z) = 1 - \sum_k a_k z^{-k}$ makes the error close to white noise, and $1/A(z)$ is an all-pole, or autoregressive, model of the signal.

## In plain words

Many signals change slowly enough that the recent past says a lot about the next value. Linear prediction makes a guess for the next value from a weighted sum of the last few values, and it picks the weights so that the guesses are wrong by as little as possible on average. The best weights depend only on how much the signal resembles a shifted copy of itself. They come from a small set of linear equations with a regular shape, and a fast method solves them. What the guess cannot explain is the new part of each sample. That part is often much smaller and more random than the signal, so it is cheaper to store or send. The weights also describe the shape of the spectrum of the signal, which is why speech coders and spectrum estimators use them.

## Definition

**Input.** An order $p \ge 1$ and the autocorrelation values $r[0], r[1], \ldots, r[p]$ of a real wide-sense stationary process $x$, where $r[k] = E[x[n]\, x[n-k]]$. In the finite-data versions, a record $x[0 \ldots N-1]$ takes the place of $r$.

**Output.** Coefficients $a = (a_1, \ldots, a_p)$ that minimize the mean-square forward prediction error

$$E(a) = E\Big[\big(x[n] - \sum_{k=1}^{p} a_k\, x[n-k]\big)^2\Big] = r[0] - 2\sum_{k} a_k\, r[k] + \sum_{i,k} a_i a_k\, r[|i-k|],$$

and the minimum value $E_p$.

**Normal equations.** $E(a)$ is a quadratic function of $a$ with the Hessian $2R$, where $R = (r[|i-k|])_{i,k=1}^{p}$ is a symmetric Toeplitz matrix. The gradient is zero exactly when the error is orthogonal to each past sample, $E[(x[n] - \hat x[n])\, x[n-i]] = 0$ for $i = 1, \ldots, p$. This is the system

$$R\, a = (r[1], \ldots, r[p])^T, \qquad E_p = r[0] - \sum_{k=1}^{p} a_k\, r[k].$$

$R$ is positive semidefinite, because $c^T R c = E[(\sum_k c_k x[n-k])^2] \ge 0$. It is positive definite unless some nonzero filter of length $p$ maps $x$ to zero. By the spectral representation, that happens only when the spectrum of $x$ is made of at most $p - 1$ lines, counted as frequencies in $[-\pi, \pi)$ radians per sample. When $R$ is positive definite, the minimizer is unique and $E_p > 0$.

## Variants

- **Autocorrelation method.** For a record of $N$ samples, set $x[n] = 0$ outside the record (usually after a window) and estimate $r[k] = \sum_n x[n]\, x[n-k]$. The matrix stays Toeplitz and positive definite for a record that is not all zero, and the filter $A(z)$ is minimum phase. This is the method of [linear predictive coding](/linear-predictive-coding/).
- **Covariance method.** Minimize $\sum_{n=p}^{N-1} (x[n] - \sum_k a_k x[n-k])^2$ over the samples that have a full past, with no window. This is a [least-squares problem](/least-squares-problem/). Its matrix $\Phi_{ik} = \sum_{n=p}^{N-1} x[n-i]\, x[n-k]$ is symmetric but not Toeplitz, so it is solved by a [Cholesky decomposition](/cholesky-decomposition/) in $O(p^3)$. The fit is better on short records, but $A(z)$ can have zeros outside the unit circle.
- **Backward prediction.** Predict $x[n-p]$ from $x[n-p+1], \ldots, x[n]$. For a real stationary process the best backward coefficients are the forward ones in reverse order, with the same error $E_p$. The forward and backward errors of consecutive orders are the two outputs of a lattice filter, and the [Burg method](/burg-method/) estimates its reflection coefficients from data.
- **Prediction $h$ steps ahead.** Predict $x[n+h-1]$ from $x[n-1], \ldots, x[n-p]$. The matrix is the same and the right side becomes $(r[h], \ldots, r[h+p-1])$.
- **Complex and vector signals.** For complex signals $R$ is Hermitian Toeplitz. For a vector signal it is block Toeplitz, and a block form of the Levinson recursion solves it.
- **Infinite order.** As $p \to \infty$ the predictor uses the whole past. This is the prediction case of the causal [Wiener filter](/wiener-filter/), and its error is given by Kolmogorov's formula below.
- **Online versions.** When the statistics are unknown or change, an adaptive filter in prediction mode, such as the [LMS algorithm](/lms-algorithm/) or the [RLS algorithm](/rls-algorithm/), updates $a$ at each sample.

## Examples

**A first-order autoregressive signal.** Let $x[n] = \tfrac12 x[n-1] + e[n]$, with white noise $e$ of variance $1$. Then $r[k] = \tfrac43 (\tfrac12)^{|k|}$, so $r[0] = \tfrac43$, $r[1] = \tfrac23$ and $r[2] = \tfrac13$.

| order $p$ | $R$ | right side | $a$ | $E_p$ |
|---|---|---|---|---|
| 1 | $[\tfrac43]$ | $[\tfrac23]$ | $(\tfrac12)$ | $\tfrac43 - \tfrac12 \cdot \tfrac23 = 1$ |
| 2 | $\begin{bmatrix} 4/3 & 2/3 \\ 2/3 & 4/3 \end{bmatrix}$ | $[\tfrac23, \tfrac13]$ | $(\tfrac12, 0)$ | $1$ |

The second coefficient is zero and the error stays at the noise variance $1$: for an autoregressive process of order $p_0$, every predictor of order $p \ge p_0$ is the model itself, and the error is the variance of the innovation $e$. A longer predictor cannot do better.

**A sinusoid.** Let $x[n] = \cos(\omega_0 n + \phi)$ with $\phi$ uniform on $[0, 2\pi)$ and $0 < \omega_0 < \pi$. Then $r[k] = \tfrac12 \cos(\omega_0 k)$. Write $c = \cos \omega_0$. For $p = 2$ the normal equations are $a_1 + c\, a_2 = c$ and $c\, a_1 + a_2 = 2c^2 - 1$, with the solution $a = (2c, -1)$ and $E_2 = \tfrac12(1 - 2c^2 + 2c^2 - 1) = 0$. The recurrence $x[n] = 2\cos\omega_0\, x[n-1] - x[n-2]$ predicts the sinusoid exactly. Its spectrum is two lines, so $R$ is singular for $p \ge 3$, as the definition says.

## Known algorithms

- **[Levinson-Durbin recursion](/levinson-durbin-recursion/).** Solves the Toeplitz normal equations for all orders $1, \ldots, p$ in $O(p^2)$ operations and $O(p)$ space. It also gives the reflection coefficients $k_1, \ldots, k_p$ and the errors $E_1, \ldots, E_p$. The exact-arithmetic version for general Toeplitz systems is the [Levinson-Durbin algorithm](/levinson-durbin-algorithm/).
- **General dense solvers.** [Cholesky decomposition](/cholesky-decomposition/) or [Gaussian elimination](/gaussian-elimination/) in $O(p^3)$. They are needed for the covariance method, where $R$ is not Toeplitz.
- **Superfast Toeplitz solvers.** $O(p \log^2 p)$ methods exist, see [Toeplitz system solving](/toeplitz-system-solving/). For the orders used in practice, often $p \le 50$, the $O(p^2)$ recursion is simpler and fast enough.
- **[Burg method](/burg-method/).** Estimates the reflection coefficients from a record by minimizing the sum of forward and backward errors at each order, with no window. The model is always stable.
- **[Linear predictive coding](/linear-predictive-coding/).** The full analysis of a framed signal: window, autocorrelation, the recursion, gain and the synthesis filter.
- **Adaptive predictors.** The [LMS algorithm](/lms-algorithm/) at $O(p)$ per sample and the [RLS algorithm](/rls-algorithm/) at $O(p^2)$ per sample follow a predictor when the statistics change.

## Bounds

- **The error does not increase with the order.** $E_p = E_{p-1}(1 - k_p^2)$ with $|k_p| \le 1$, so $r[0] = E_0 \ge E_1 \ge E_2 \ge \cdots \ge 0$. This is proved on the [Levinson-Durbin recursion](/levinson-durbin-recursion/) page.
- **The limit is Kolmogorov's formula.** For a stationary process with power spectral density $S(\omega)$, $\omega$ in radians per sample,

$$\lim_{p \to \infty} E_p = \exp\Big(\frac{1}{2\pi} \int_{-\pi}^{\pi} \ln S(\omega)\, d\omega\Big),$$

and the limit is zero when the integral is $-\infty$, as for a spectrum with lines or with a band of zeros (Brockwell and Davis, Theorem 5.8.1). For the first-order example, $S(\omega) = 1/|1 - \tfrac12 e^{-i\omega}|^2$, the integral of $\ln |1 - \tfrac12 e^{-i\omega}|^2$ over a period is zero, and the limit is $1$, the value already reached at $p = 1$. The formula gives a lower bound on the error of every linear predictor with a finite past.
- **Cost.** The input has $p + 1$ numbers, so $\Omega(p)$ operations are needed. The Levinson-Durbin recursion uses about $2p^2$ arithmetic operations, half of them multiplications. The superfast methods are $O(p \log^2 p)$. No better general bound is known.

## Reductions

- **To a Toeplitz system.** The autocorrelation version is exactly a symmetric positive definite [Toeplitz system](/toeplitz-system-solving/), and every such system with a right side of the form $(r[1], \ldots, r[p])$ is a prediction problem.
- **To the Wiener filter.** Linear prediction is the FIR [Wiener filter](/wiener-filter/) with the desired signal $d[n] = x[n]$ and the input vector $(x[n-1], \ldots, x[n-p])$. The Wiener-Hopf equations of that filter are the normal equations above.
- **To least squares.** The covariance method is an ordinary [least-squares problem](/least-squares-problem/) with a data matrix of shifted samples, solved by [normal equations](/normal-equations/) or a QR factorization.
- **To autoregressive spectrum estimation.** The model $\hat S(\omega) = E_p / |A(e^{i\omega})|^2$ is the maximum-entropy spectrum that matches $r[0], \ldots, r[p]$. It is one of the methods of [spectral estimation](/spectral-estimation/).
- **To orthogonal polynomials.** The polynomials $z^p A_p(z)$ for $p = 0, 1, 2, \ldots$ are the monic orthogonal polynomials on the unit circle for the spectral measure of $x$, and the recursion over $p$ is the Szegő recursion.

## Applications

- **Speech coding and analysis.** [Linear predictive coding](/linear-predictive-coding/) models the vocal tract by $1/A(z)$. Code-excited and other analysis-by-synthesis coders send the coefficients and a coded residual.
- **Lossless audio compression.** Coders such as Shorten and FLAC predict each sample and code the residual with an entropy coder. This is [predictive coding](/predictive-coding/) with a linear predictor.
- **Spectral estimation.** The all-pole model gives a smooth spectrum with sharp peaks from a short record.
- **Seismic deconvolution.** Predictive deconvolution removes reverberations from a seismic trace with a prediction-error filter.
- **Time-series forecasting.** Autoregressive models fitted by the Yule-Walker equations forecast economic and sensor data.
- **Feature extraction.** Prediction coefficients and their [cepstrum](/cepstrum/) are features for speech recognition and [pitch detection](/pitch-detection/).

## References
