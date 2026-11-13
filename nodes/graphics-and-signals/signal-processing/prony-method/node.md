---
tag: ATNC9Z
kind: algorithm
slug: prony-method
name: Prony's method
aliases:
- Prony analysis
area: graphics-and-signals/signal-processing
level: advanced
summary: "Fit a sum of p damped complex exponentials to equally spaced samples: solve a linear prediction system, take the roots of its polynomial, then fit the amplitudes."
solves: [spectral-estimation]
model: real-ram
complexity:
  vars: {N: the number of samples, p: the number of exponentials}
  time: {worst: Θ(N p²), average: Θ(N p²), best: Θ(N p²)}
  space: {extra: Θ(N p)}
properties: {deterministic: true, parametric: true, exact_without_noise: true, noise_sensitive: true}
history:
  year: 1795
  people: [Gaspard Riche de Prony]
  note: Prony fitted sums of exponentials to measurements of the expansion of gases and vapors, and reduced the fit to a linear recurrence and the roots of a polynomial.
prereqs: [linear-prediction, polynomial-root-finding, least-squares-problem]
see_also: [spectral-estimation, esprit, music-algorithm, burg-method, vandermonde-matrix, durand-kerner-method, ben-or-tiwari-algorithm, z-transform]
sources:
  - paper: "Gaspard Riche de Prony, Essai expérimental et analytique sur les lois de la dilatabilité des fluides élastiques et sur celles de la force expansive de la vapeur de l'eau et de la vapeur de l'alkool, à différentes températures, Journal de l'École Polytechnique, vol. 1, cahier 22, 1795"
    locator: pp. 24 to 76 (the interpolation of measured values by a sum of exponentials through a linear recurrence)
  - book: isbn:9780471594314
    title: Monson H. Hayes, Statistical Digital Signal Processing and Modeling, Wiley, 1996
    locator: Chapter 4, Signal Modeling (Section 4.4, Prony's method, and the least-squares form of the prediction equations)
  - paper: doi:10.1109/TASSP.1982.1163974
    title: Ramdas Kumaresan and Donald W. Tufts, Estimating the parameters of exponentially damped sinusoids and pole-zero modeling in noise, IEEE Transactions on Acoustics, Speech, and Signal Processing 30(6), 1982
    locator: pp. 833 to 840 (the noise sensitivity of Prony's method and the fix with a higher order, backward prediction and a truncated SVD)
  - paper: doi:10.1109/29.56027
    title: Yingbo Hua and Tapan K. Sarkar, Matrix pencil method for estimating parameters of exponentially damped/undamped sinusoids in noise, IEEE Transactions on Acoustics, Speech, and Signal Processing 38(5), 1990
    locator: pp. 814 to 824 (the matrix pencil form, which replaces the polynomial roots by a generalized eigenvalue problem)
---

Prony's method fits the model $x[t] = \sum_{j=1}^{p} h_j z_j^t$ to $N \ge 2p$ equally spaced samples. Each $z_j = \rho_j e^{i\omega_j}$ is a damped complex sinusoid: $\rho_j$ is the damping per sample and $\omega_j$ the frequency in radians per sample. The complex amplitude $h_j$ holds the size and the phase. The method needs three linear algebra steps. First, a [linear prediction](/linear-prediction/) system gives the coefficients of a polynomial whose roots are the $z_j$. Second, a [polynomial root finder](/polynomial-root-finding/) gives the roots. Third, a [Vandermonde](/vandermonde-matrix/) least-squares fit gives the amplitudes. On noiseless data it recovers the model exactly from $2p$ samples. With noise its error grows quickly, and the modern forms of the method, [ESPRIT](/esprit/) and the matrix pencil, keep its idea but add a subspace step. It is a parametric answer to [spectral estimation](/spectral-estimation/) for line spectra and damped modes.

## In plain words

A sum of a few decaying or rotating terms follows a fixed rule: each sample is a fixed mix of the few samples before it. Find that rule from the data by solving a small set of linear equations. The rule is a polynomial, and its roots tell you how fast each term decays and how fast it turns. When you know the roots, the sizes of the terms come from one more set of linear equations. Without noise, twice as many samples as terms are enough, and the answer is exact. With noise, the rule is fitted by least squares and the roots move, sometimes a lot.

## The problem

Given samples $x[0], \dots, x[N-1]$, real or complex, and an order $p$ with $N \ge 2p$, find distinct nonzero $z_1, \dots, z_p$ and amplitudes $h_1, \dots, h_p$ so that $\sum_j h_j z_j^t$ matches $x[t]$, exactly if possible and otherwise in the least-squares sense of the prediction equations. With a sampling interval $T$, the continuous-time exponent of term $j$ is $s_j = (\ln z_j)/T$, with real part the decay rate and imaginary part the angular frequency.

## The algorithm

```pseudo id=main
PRONY(x[0 .. N − 1], p)                          ▷ N ≥ 2p
L1  form the N − p equations Σ_{i=1}^{p} c[i]·x[t − i] = −x[t],  t = p, …, N − 1
L2  c ← the least-squares solution of L1          ▷ exact solve when N = 2p
L3  z_1, …, z_p ← the roots of z^p + c[1]z^{p−1} + … + c[p]
L4  h ← the least-squares solution of Σ_j h_j z_j^t = x[t],  t = 0, …, N − 1
L5  return z, h
```

Line L1 is the forward linear prediction system. Its matrix has the entries $x[t-i]$, which are constant along the antidiagonals, so it is a Hankel matrix in reversed column order. Line L2 solves it. The implementation forms the normal equations and uses Gaussian elimination with partial pivoting, which works in exact rationals as well as in floating point. Line L3 uses the [Durand-Kerner](/durand-kerner-method/) iteration. Line L4 is a Vandermonde system with one column per root.

## Example

Take $x[t] = 2\,(1/2)^t + (-1/3)^t$ and $p = 2$, with the smallest record $N = 4$: $x = (3,\ 2/3,\ 11/18,\ 23/108)$.

| step | equations | result |
|---|---|---|
| L1 | $\tfrac{2}{3}c_1 + 3c_2 = -\tfrac{11}{18}$ and $\tfrac{11}{18}c_1 + \tfrac{2}{3}c_2 = -\tfrac{23}{108}$ | 2 by 2 system |
| L2 | solve | $c_1 = -1/6$, $c_2 = -1/6$ |
| L3 | $z^2 - z/6 - 1/6 = 0$, $z = (1/6 \pm 5/6)/2$ | $z_1 = 1/2$, $z_2 = -1/3$ |
| L4 | $h_1 + h_2 = 3$ and $h_1/2 - h_2/3 = 2/3$ | $h_1 = 2$, $h_2 = 1$ |

In the language of frequencies, $z_1 = 1/2$ is a term at $\omega = 0$ that halves at each sample, and $z_2 = -1/3$ is a term at $\omega = \pi$, the highest frequency, that decays by a factor of 3 at each sample. The implementation runs lines L1, L2 and L4 in exact rationals and gives these values exactly. In floating point it gives the roots to within $10^{-12}$. For three terms, $z = (1/2, -1/3, 3/4)$ and $h = (1, -2, 3/2)$, six samples give $c = (-11/12, -1/24, 1/8)$, which is exactly $(z - 1/2)(z + 1/3)(z - 3/4)$.

## Correctness

If $x[t] = \sum_j h_j z_j^t$, then for $P(z) = \prod_j (z - z_j) = z^p + c_1 z^{p-1} + \dots + c_p$, $\sum_{i=0}^{p} c_i x[t-i] = \sum_j h_j z_j^{t-p} P(z_j) = 0$, so the coefficients of $P$ solve the equations of line L1 with residual zero. The matrix of line L1 factors as $W\,\operatorname{diag}(h)\,U$ with two Vandermonde matrices in the distinct $z_j$, so it has full column rank when all $h_j \ne 0$ and $N \ge 2p$. Hence the least-squares solution of line L2 is unique and equals the coefficients of $P$. The roots of line L3 are the $z_j$, and the Vandermonde matrix of line L4 has full column rank, so the fit returns the $h_j$. The full proof is below.

## Complexity

**Time.** Line L1 has $(N - p)\,p$ entries. Forming the normal equations of line L2 costs $(N - p)\,p^2$ multiplies and solving them $p^3/3$. One Durand-Kerner sweep in line L3 costs $\Theta(p^2)$, and the sweep count is a small constant for well separated roots. Line L4 costs $N p^2 + p^3/3$ in the same way. With $p \le N/2$ the total is $\Theta(N p^2)$ in the real-RAM model. With a fast Hankel or Toeplitz solver line L2 costs $O(Np + p^2)$ instead.

**Space.** The implementation stores the $(N - p) \times p$ and $N \times p$ matrices, $\Theta(N p)$ numbers. Accumulating the normal equations row by row needs only $\Theta(p^2)$.

## Properties

- **Exact without noise.** Exactly $2p$ samples determine $p$ exponentials. Measured: over 500 random cases with $p \le 3$, distinct rational $z_j$ with numerators $-7$ to $7$ and denominators 1 to 5, nonzero rational amplitudes and $2p \le N \le 2p + 4$ (seed 4701), lines L1, L2 and L4 in exact rationals gave the exact polynomial and the exact amplitudes every time.
- **Floating point.** Over 500 random cases with $p \le 4$, $0.7 \le |z_j| \le 1$, roots at least $0.3$ apart and $2p \le N \le 2p + 6$ (seed 4702), every root was recovered to within $10^{-6}$.
- **Sensitive to noise.** For $z = (0.95e^{0.5i}, 0.9e^{1.3i})$, $h = (1, 0.8)$, $N = 24$, $p = 2$, and complex white Gaussian noise of standard deviation $\sigma$ in each part (200 draws per level, seed 4703), the largest root error had these medians:

| $\sigma$ | median error | mean error | largest error |
|---|---|---|---|
| 0 | $4.7 \times 10^{-16}$ | $4.7 \times 10^{-16}$ | $4.7 \times 10^{-16}$ |
| $10^{-6}$ | $5.3 \times 10^{-7}$ | $6.1 \times 10^{-7}$ | $1.8 \times 10^{-6}$ |
| $10^{-4}$ | $6.0 \times 10^{-5}$ | $6.5 \times 10^{-5}$ | $1.6 \times 10^{-4}$ |
| $10^{-2}$ | $8.2 \times 10^{-3}$ | $8.8 \times 10^{-3}$ | $2.1 \times 10^{-2}$ |

The error grows about linearly with $\sigma$ at these levels. More samples help: at $\sigma = 10^{-3}$ (seed 4710) the median error was $0.0111$ for $N = 4$, $0.0011$ for $N = 8$ and $0.00055$ for $N = 24$.
- **Biased in noise.** The least-squares estimate of line L2 is biased, because the noise appears in the matrix and on the right side of the same equations. For undamped tones in white noise of power $\sigma^2$, the equations of line L2 tend to $(R + \sigma^2 I)c = -r$ instead of $Rc = -r$ as $N$ grows, so the estimate does not converge to the true polynomial. The subspace methods do converge in this case.
- **Damping is free.** Unlike [MUSIC](/music-algorithm/) and the [periodogram](/periodogram/), which assume constant amplitudes, the model allows each term to decay or grow.

## Variants and improvements

- **Extended order with a truncated SVD.** Kumaresan and Tufts fit a prediction polynomial of order $L > p$, often $L \approx N/3$, keep only the $p$ largest singular values of the prediction matrix, and pick the $p$ roots of the correct kind among $L$. Backward prediction puts the signal roots outside the unit circle and the extra roots inside, which separates them. This nearly reaches the Cramér-Rao bound at moderate signal to noise ratios.
- **Matrix pencil.** Hua and Sarkar replace lines L1 to L3 by the generalized eigenvalues of a pair of shifted Hankel matrices. This avoids the polynomial, whose roots can be ill conditioned, and is the same idea as [ESPRIT](/esprit/) applied to one record.
- **Pisarenko and MUSIC.** For undamped sinusoids in white noise, put the roots on the unit circle and use the noise eigenvectors of a covariance estimate instead of the prediction equations; see [MUSIC](/music-algorithm/).
- **Exact arithmetic.** Over a field, finding the recurrence from $2p$ terms is the [Berlekamp-Massey](/berlekamp-massey/) problem, and [sparse polynomial interpolation](/sparse-polynomial-interpolation/) by the [Ben-Or and Tiwari algorithm](/ben-or-tiwari-algorithm/) is Prony's method with the samples taken at powers of a point.
- **Pole-zero modeling.** Prony's name is also used for fitting a rational transfer function to an impulse response: the denominator comes from line L1 as above, and the numerator from the first samples.

## When to use it

Use Prony's method when the data really are a few damped exponentials with a high signal to noise ratio, for example the ringdown of a mechanical structure, the modes of a power system after a disturbance, transient analysis of circuits and nuclear magnetic resonance signals. Use it also as the core of an exact algorithm over the rationals or a finite field. For noisy data, use the matrix pencil or [ESPRIT](/esprit/), which have the same model and far better statistics, and for undamped tones in white noise use [MUSIC](/music-algorithm/) or ESPRIT. For a broadband spectrum use a nonparametric estimator, such as the [Welch method](/welch-method/).

## Pitfalls

- **The wrong order in line L1.** If the data hold fewer than $p$ terms, the matrix of line L1 is singular without noise, and with noise line L3 gives extra roots that fit the noise. If they hold more than $p$ terms, the fit is wrong for all of them. Choose $p$ from the singular values of the prediction matrix, or fit a larger order and select roots.
- **Normal equations in line L2.** Forming $M^H M$ squares the condition number of the Hankel matrix, which is already large when roots are close or strongly damped. Use a QR factorization or an SVD for anything beyond small, well separated problems.
- **Ill-conditioned roots in line L3.** Roots of a polynomial can move far under small changes of its coefficients when they are clustered (Wilkinson's example), so a small error in line L2 can become a large error in frequency. This is the main reason to prefer the matrix pencil.
- **Roots outside the unit circle in line L4.** With noise, a root can come out with $|z| > 1$. Its powers $z^t$ grow along the record and dominate the Vandermonde fit of line L4. Check $|z_j|$ before trusting the amplitudes.
- **Real data.** A real damped cosine is two conjugate exponentials, so a real signal with $K$ cosines needs $p = 2K$. With $p = K$ the fit fails.

## Implementations

## History

Gaspard Riche de Prony published the method in 1795 in the first volume of the Journal de l'École Polytechnique. He wanted interpolation formulas for his measurements of the expansion of gases and the pressure of water and alcohol vapor at different temperatures, and noted that a sum of exponentials satisfies a linear difference equation with constant coefficients, so its exponents follow from the roots of a polynomial. The method stayed in numerical analysis as a way to fit exponentials. In the 1970s and 1980s signal processing took it up for damped sinusoids, and its poor behavior in noise was studied. Kumaresan and Tufts (1982) improved it with a higher order and a truncated SVD, and Hua and Sarkar (1990) replaced the polynomial with a matrix pencil. Subspace methods such as ESPRIT (1986 and 1989) use the same shift structure.

## References
