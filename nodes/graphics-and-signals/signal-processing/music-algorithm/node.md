---
tag: PF6V7J
kind: algorithm
slug: music-algorithm
name: MUSIC algorithm
aliases:
- multiple signal classification
area: graphics-and-signals/signal-processing
level: advanced
summary: "Estimate the frequencies of d sinusoids in white noise, or d arrival directions, as the points where the steering vector is orthogonal to the noise eigenvectors of a covariance."
solves: [spectral-estimation]
model: real-ram
complexity:
  vars: {m: the size of the covariance matrix, d: the number of sinusoids, L: the number of grid points}
  time: {worst: Θ(m³ + L m), average: Θ(m³ + L m), best: Θ(m³ + L m)}
  space: {extra: Θ(m²)}
properties: {deterministic: true, parametric: true, subspace_method: true, consistent: true}
history:
  year: 1979
  people: [Ralph O. Schmidt, Georges Bienvenu, Laurent Kopp]
  note: Schmidt presented MUSIC in 1979 and published it in 1986; Bienvenu and Kopp found the same noise subspace idea at the same time. Pisarenko's 1973 method is the case m = d + 1.
prereqs: [power-spectral-density, eigenvector, covariance-matrix]
see_also: [spectral-estimation, esprit, prony-method, periodogram, beamforming, jacobi-eigenvalue-algorithm, golden-section-search, burg-method]
sources:
  - paper: doi:10.1109/TAP.1986.1143830
    title: Ralph O. Schmidt, Multiple emitter location and signal parameter estimation, IEEE Transactions on Antennas and Propagation 34(3), 1986
    locator: pp. 276 to 280 (the data model, the signal and noise subspaces and the MUSIC spectrum)
  - book: isbn:9780131139565
    title: Petre Stoica and Randolph L. Moses, Spectral Analysis of Signals, Pearson Prentice Hall, 2005
    locator: Section 4.5 (Pisarenko and MUSIC methods for sinusoids in noise) and Section 6.4.3 (MUSIC for sensor arrays)
  - paper: doi:10.1111/j.1365-246X.1973.tb03424.x
    title: V. F. Pisarenko, The retrieval of harmonics from a covariance function, Geophysical Journal of the Royal Astronomical Society 33(3), 1973
    locator: pp. 347 to 366 (the harmonics as the roots of the eigenvector of the smallest eigenvalue)
  - paper: doi:10.1109/29.17564
    title: Petre Stoica and Arye Nehorai, MUSIC, maximum likelihood, and Cramér-Rao bound, IEEE Transactions on Acoustics, Speech, and Signal Processing 37(5), 1989
    locator: pp. 720 to 741 (the asymptotic variance of MUSIC compared with the Cramér-Rao bound)
---

MUSIC (multiple signal classification) estimates the frequencies $\omega_1, \dots, \omega_d$ of $d$ complex sinusoids in white noise, or the directions of $d$ sources seen by a uniform array of sensors, from an $m \times m$ covariance matrix. It finds the eigenvectors of the covariance. The $d$ largest span the signal subspace, and the other $m - d$ span the noise subspace, which is orthogonal to the steering vector $a(\omega_k)$ of every true frequency. MUSIC scans $\omega$ and reports the $d$ points where $a(\omega)$ is closest to orthogonal to the noise subspace. These are the peaks of the pseudospectrum $1/\|E^H a(\omega)\|^2$. With the exact covariance the peaks are infinite and exactly at the true frequencies. With an estimate they are sharp and resolve tones closer than the $2\pi/N$ limit of the [periodogram](/periodogram/). It is a subspace answer to [spectral estimation](/spectral-estimation/) for line spectra, and the sibling of [ESPRIT](/esprit/).

## In plain words

Each tone at a known frequency would add one fixed pattern, its steering vector, to the data. The covariance matrix of the data has a few large directions, made by the tones, and many small equal ones, made only by the noise. The noise directions are at right angles to every tone pattern. So try every frequency: build its pattern and measure how much of it falls in the noise directions. At a true frequency the answer is zero, and everywhere else it is positive. MUSIC plots one over this amount and reports the highest peaks.

## The problem

The data are $x[n] = \sum_{k=1}^{d} \alpha_k e^{i\omega_k n} + e[n]$ with distinct frequencies $\omega_k$ in radians per sample, complex amplitudes $\alpha_k$ with independent uniform phases, and complex white noise $e$ of variance $\sigma^2$. With the windows $y_t = (x[t], \dots, x[t+m-1])^T$ the covariance is $R = E[y_t y_t^H] = \sum_k |\alpha_k|^2 a(\omega_k)a(\omega_k)^H + \sigma^2 I$, where $a(\omega) = (1, e^{i\omega}, \dots, e^{i(m-1)\omega})^T$ and $d < m$. From an estimate of $R$, find the $\omega_k$. A usual estimate is the sample covariance $\hat R = \frac{1}{K}\sum_{t=0}^{K-1} y_t y_t^H$ with $K = N - m + 1$, which costs $\Theta(K m^2)$. For a uniform line of $m$ sensors at spacing $\Delta$ and a far source at angle $\theta$ to the broadside, the same model holds with $\omega = 2\pi(\Delta/\lambda)\sin\theta$, $t$ indexes snapshots in time, and the sensors index the entries of $y_t$.

## The algorithm

```pseudo id=main
MUSIC(R, d, L)                         ▷ R: m × m Hermitian estimate, 0 < d < m
L1  (λ, U) ← eigendecomposition of R, sorted so that λ_1 ≥ … ≥ λ_m
L2  E ← (u_{d+1}, …, u_m)               ▷ the noise subspace
L3  for ω on L grid points in [−π, π) do D(ω) ← ‖E^H a(ω)‖²
L4  take the d deepest local minima of D on the grid
L5  refine each minimum by golden-section search
L6  return the d frequencies            ▷ the pseudospectrum is 1 / D(ω)
```

Line L1 uses a cyclic complex Jacobi method: each step removes the phase of one off-diagonal entry with a diagonal unitary matrix and then zeroes it with a real plane rotation, as in the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/). Line L3 does not form $E^H a(\omega)$ directly. With $q_k$ the sum of the $k$th superdiagonal of the projector $EE^H$, $D(\omega) = q_0 + 2\operatorname{Re}\sum_{k=1}^{m-1} q_k e^{i\omega k}$, which costs $O(m)$ per point. Line L5 is a [golden-section search](/golden-section-search/) on the bracket of two grid steps around each grid minimum.

## Example

Take two unit-power tones at $\omega = 0.5$ and $0.9$ rad/sample, noise variance $\sigma^2 = 0.1$ and $m = 8$, and use the exact covariance $R = a(0.5)a(0.5)^H + a(0.9)a(0.9)^H + 0.1\,I$. The implementation, with a grid of $L = 1024$ points, gives:

| quantity | value |
|---|---|
| eigenvalues of $R$ | $13.1313,\ 3.0687,\ 0.1,\ 0.1,\ 0.1,\ 0.1,\ 0.1,\ 0.1$ |
| $D(0)$, $D(0.7)$, $D(1.5)$, $D(3.0)$ | $4.020,\ 0.0757,\ 5.466,\ 7.584$ |
| $D(0.5)$, $D(0.9)$ | $-6.5 \times 10^{-16}$, $2.6 \times 10^{-16}$ (zero up to rounding) |
| estimates | $0.4999999984$ and $0.8999999959$ |

The two large eigenvalues are $\sigma^2$ plus the eigenvalues of the signal part. Their sum $16.2 - 0.2 = 16 = 2m$ is the total signal power over the 8 entries. The other six are exactly $\sigma^2$. The errors of about $2 \times 10^{-9}$ and $4 \times 10^{-9}$ come from rounding: $D$ is quadratic near its zero, so an error of $10^{-16}$ in $D$ shifts the minimum by about $10^{-8}$ divided by the curvature. The midpoint $0.7$ has $D = 0.0757$, small but not zero, which is the dip between two close peaks.

## Correctness

Write $R = APA^H + \sigma^2 I$ with $A = (a(\omega_1), \dots, a(\omega_d))$. Its first $d$ rows form a Vandermonde matrix in distinct points, so $A$ has rank $d$, and $APA^H$ is positive definite on the range of $A$ and zero on $\ker A^H$. So the $m - d$ smallest eigenvalues of $R$ are all $\sigma^2$, the others are larger, and the noise eigenvectors of line L2 span $\ker A^H$, whatever basis the eigen solver picks inside the repeated eigenvalue. Then $D(\omega)$ is the squared distance from $a(\omega)$ to the range of $A$. It is zero at each $\omega_k$. At any other $\omega$ it is positive, because $d + 1 \le m$ steering vectors at distinct frequencies are linearly independent. A fine enough grid puts each zero alone in its bracket, and the golden-section search converges to it. The full proof is below.

## Complexity

**Time.** Line L1 costs $\Theta(m^3)$ per Jacobi sweep, with a number of sweeps that is small in practice (the method converges quadratically in the end). Line L2 and the diagonal sums cost $\Theta(m^2(m - d))$. Line L3 costs $\Theta(Lm)$. Line L5 costs $O(m \log(1/\text{tol}))$ per frequency. The total is $\Theta(m^3 + Lm)$ in the real-RAM model, plus $\Theta(Km^2)$ to form the sample covariance. Root-MUSIC replaces lines L3 to L5 by the roots of a polynomial of degree $2m - 2$.

**Space.** $\Theta(m^2)$ for the covariance and the eigenvectors.

## Properties

- **Exact with the exact covariance.** Over 60 random cases with $4 \le m \le 8$, $d \le \min(3, m/2)$, frequencies at least $1.5 \cdot 2\pi/m$ apart, random powers and noise levels (seed 4802), every frequency was recovered to within $10^{-6}$.
- **Accuracy with a sample covariance.** For the tones of the example with random phases, $N = 200$ samples, noise variance $0.1$ (10 dB per tone) and $m = 8$, over seeds 4803 to 4852, the root mean square errors were $0.0018$ and $0.0020$ rad, with biases of $0.0004$. The Cramér-Rao bound for one tone at this signal to noise ratio has standard deviation $\sqrt{6\sigma^2/(N(N^2-1))} = 0.00027$. A larger $m$ brings MUSIC closer: on the same data the root mean square error was $0.0019$ for $m = 8$, $0.00050$ for $m = 16$ and $0.00036$ for $m = 32$ (grid $L = 2048$).
- **Resolution beyond the periodogram.** For tones at $0.5$ and $0.6$ (separation $0.1$), noise variance $0.1$, seeds 9000 to 9099, "resolved" means two estimates, each within $0.05$ of its tone. With $N = 64$ (separation about $2\pi/N$) and $m = 16$, MUSIC resolved 100 of 100 records and the periodogram showed two such peaks in 65. With $N = 32$ (separation about half of $2\pi/N$) and $m = 12$, MUSIC resolved 13, MUSIC on the forward-backward averaged covariance 41, and the periodogram 1.
- **Consistent.** As the number of snapshots grows, $\hat R \to R$ and the estimates converge to the true frequencies, unlike the least-squares [Prony method](/prony-method/) in noise. Stoica and Nehorai derived the asymptotic variance of MUSIC and showed that it approaches the Cramér-Rao bound when both $m$ and the number of snapshots are large.
- **Not a power spectrum.** The height of a peak of $1/D$ does not measure the power of the tone. Powers come from a separate least-squares fit with the estimated frequencies.

## Variants and improvements

- **Pisarenko's method.** The case $m = d + 1$: one noise eigenvector $e$, and the frequencies are the arguments of the roots of the polynomial $\sum_k e_k z^k$. It is cheap but has a large variance.
- **Root-MUSIC.** $D$ on the unit circle is $z^{-(m-1)}$ times a polynomial of degree $2m - 2$ with coefficients $q_k$. Its roots come in pairs $z$ and $1/\bar z$, and the $d$ roots inside the unit circle and closest to it give the frequencies. There is no grid, and the threshold at low signal to noise ratio is lower.
- **Min-norm.** Uses the one vector in the noise subspace with first entry 1 and least norm, which gives fewer spurious peaks.
- **Forward-backward averaging and spatial smoothing.** Averaging $\hat R$ with its exchanged conjugate $J\hat R^{*}J$, or averaging over subarrays, restores the rank of the signal part when sources are coherent, as in multipath.
- **ESPRIT.** Uses the signal subspace and its shift structure instead of a search; see [ESPRIT](/esprit/).
- **Order estimation.** The number $d$ is chosen from the eigenvalues, by AIC or MDL, or by a gap above the noise floor.

## When to use it

Use MUSIC for a few sinusoids or narrowband sources in white noise when resolution matters more than speed, for example in direction finding with an antenna array, radar and sonar, and the frequency estimation of closely spaced tones from a short record. It needs a good estimate of $d$, a noise that is white (or known, so it can be whitened), and uncorrelated sources unless smoothing is used. If the array is a shift of itself, as a uniform line is, [ESPRIT](/esprit/) avoids the search and gives the same accuracy. For broadband spectra and for a power scale, use the [Welch method](/welch-method/) or an AR model such as the [Burg method](/burg-method/).

## Pitfalls

- **Coherent sources break line L2.** If two sources are fully correlated, $P$ is singular, the signal part has rank less than $d$, and the noise subspace of line L2 is no longer orthogonal to both steering vectors. Use forward-backward averaging or spatial smoothing when forming $R$.
- **The wrong $d$ in line L2.** Too small a $d$ puts a signal eigenvector into $E$ and removes a peak. Too large a $d$ removes noise directions and can add a spurious peak. Look at the eigenvalues before choosing.
- **Too coarse a grid in line L3.** The peaks of $1/D$ are very narrow at high signal to noise ratio, and a grid can step over one. Use a grid several times finer than $2\pi/m$, or use root-MUSIC.
- **Spurious minima in line L4.** At low signal to noise ratio or with few snapshots the noise subspace estimate has random dips, and one of them can be deeper than a true one. This is the threshold effect, and below it the error jumps from small to large.
- **Colored noise.** The $m - d$ equal noise eigenvalues of the proof need white noise. With a known noise covariance $Q$, whiten with $Q^{-1/2}$ first.

## Implementations

## History

Pisarenko (1973) found the frequencies of harmonics in noise from the eigenvector of the smallest eigenvalue of a covariance matrix of size $d + 1$. Ralph Schmidt generalized this to the whole noise subspace and to arbitrary arrays, presenting MUSIC at a RADC estimation workshop in 1979 and in his Stanford thesis of 1981, and publishing it in IEEE Transactions on Antennas and Propagation in 1986. Bienvenu and Kopp independently gave the same approach in 1979. Subspace methods then spread through array processing. ESPRIT (1986 and 1989) used the signal subspace instead, and Stoica and Nehorai (1989) found the statistical performance of MUSIC and its relation to the maximum likelihood estimator and the Cramér-Rao bound.

## References
