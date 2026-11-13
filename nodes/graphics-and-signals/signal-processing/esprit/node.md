---
tag: X5EKAZ
kind: algorithm
slug: esprit
name: ESPRIT
aliases:
- estimation of signal parameters via rotational invariance
area: graphics-and-signals/signal-processing
level: advanced
summary: "Estimate the frequencies of d sinusoids in white noise, or d arrival directions, from the shift invariance of the signal subspace: a small least-squares fit whose eigenvalues are e^{iω}."
solves: [spectral-estimation]
model: real-ram
complexity:
  vars: {m: the size of the covariance matrix, d: the number of sinusoids}
  time: {worst: Θ(m³ + d^4), average: Θ(m³ + d^4), best: Θ(m³ + d^4)}
  space: {extra: Θ(m²)}
properties: {deterministic: true, parametric: true, subspace_method: true, search_free: true}
history:
  year: 1986
  people: [Richard Roy, Arogyaswami Paulraj, Thomas Kailath]
  note: Roy, Paulraj and Kailath introduced the subspace rotation approach in 1986, and Roy and Kailath gave the full form for sensor arrays with a displacement invariance in 1989.
prereqs: [power-spectral-density, eigenvector, least-squares-problem]
see_also: [spectral-estimation, music-algorithm, prony-method, beamforming, periodogram, singular-value-decomposition, jacobi-eigenvalue-algorithm, burg-method]
sources:
  - paper: doi:10.1109/TASSP.1986.1164935
    title: Richard Roy, Arogyaswami Paulraj and Thomas Kailath, ESPRIT, a subspace rotation approach to estimation of parameters of cisoids in noise, IEEE Transactions on Acoustics, Speech, and Signal Processing 34(5), 1986
    locator: pp. 1340 to 1342 (the rotation of the signal subspace between two shifted subsets of samples)
  - paper: doi:10.1109/29.32276
    title: Richard Roy and Thomas Kailath, ESPRIT, estimation of signal parameters via rotational invariance techniques, IEEE Transactions on Acoustics, Speech, and Signal Processing 37(7), 1989
    locator: pp. 984 to 995 (the array model with two identical displaced subarrays, the least-squares and total least-squares forms)
  - book: isbn:9780131139565
    title: Petre Stoica and Randolph L. Moses, Spectral Analysis of Signals, Pearson Prentice Hall, 2005
    locator: Section 4.7 (ESPRIT for sinusoids in noise) and Section 6.4.5 (ESPRIT for sensor arrays)
---

ESPRIT (estimation of signal parameters via rotational invariance techniques) estimates the frequencies $\omega_1, \dots, \omega_d$ of $d$ complex sinusoids in white noise, or the directions of $d$ sources seen by an array made of two identical shifted subarrays, from an $m \times m$ covariance matrix. Like [MUSIC](/music-algorithm/), it splits the eigenvectors of the covariance into a signal and a noise subspace. It uses the signal subspace and a structural fact. The steering vectors of a tone, cut to their first $m - 1$ entries or to their last $m - 1$ entries, differ only by the factor $e^{i\omega}$. So the two cut copies of the signal subspace are related by a $d \times d$ matrix $\Phi$ whose eigenvalues are $e^{i\omega_k}$. ESPRIT fits $\Phi$ by least squares and reads off the frequencies, with no search over a grid. It is a subspace answer to [spectral estimation](/spectral-estimation/), and the statistically sound form of the idea behind the [Prony method](/prony-method/).

## In plain words

A tone at frequency $\omega$ turns each sample by the same angle $\omega$ relative to the sample before. Look at the data through two windows, one sample apart. In the second window every tone has turned by its own angle. From the covariance, find the few directions that the tones occupy. Ask what small matrix turns the first window's view of those directions into the second window's view. The answer is a rotation in disguise, and its eigenvalues are the turns $e^{i\omega_k}$. Their angles are the frequencies, read off directly.

## The problem

The data are $x[n] = \sum_{k=1}^{d} \alpha_k e^{i\omega_k n} + e[n]$ with distinct frequencies $\omega_k$ in radians per sample, amplitudes with independent uniform phases, and complex white noise of variance $\sigma^2$. With the windows $y_t = (x[t], \dots, x[t+m-1])^T$ the covariance is $R = \sum_k |\alpha_k|^2 a(\omega_k)a(\omega_k)^H + \sigma^2 I$ with $a(\omega) = (1, e^{i\omega}, \dots, e^{i(m-1)\omega})^T$ and $d < m$. From an estimate of $R$, such as the sample covariance $\frac{1}{K}\sum_t y_t y_t^H$ over the $K = N - m + 1$ windows, find the $\omega_k$. For an array of sensor pairs with a common displacement $\Delta$, a source at angle $\theta$ gives $\omega = 2\pi(\Delta/\lambda)\sin\theta$, and the two subarrays play the role of the two windows.

## The algorithm

For an $m$-row matrix $X$, $X_1$ drops the last row and $X_2$ drops the first row.

```pseudo id=main
ESPRIT(R, d)                         ▷ R: m × m Hermitian estimate, 0 < d < m
L1  (λ, U) ← eigendecomposition of R, sorted so that λ_1 ≥ … ≥ λ_m
L2  S ← (u_1, …, u_d)                ▷ the signal subspace, m × d
L3  S_1 ← S without its last row,  S_2 ← S without its first row
L4  Φ ← (S_1^H S_1)^{−1} S_1^H S_2    ▷ least squares S_1 Φ ≈ S_2
L5  φ_1, …, φ_d ← the eigenvalues of Φ
L6  return arg φ_1, …, arg φ_d
```

Line L1 uses the same cyclic complex Jacobi method as the MUSIC page. Line L4 forms the $d \times d$ normal equations and solves them by Gaussian elimination. $\Phi$ is not Hermitian, so line L5 needs a general eigenvalue method. For the small $d$ of practice the implementation forms the characteristic polynomial by the Faddeev-LeVerrier recursion and finds its roots by Durand-Kerner iteration. A QR iteration would also work.

## Example

Take the data of the MUSIC page: two unit-power tones at $\omega = 0.5$ and $0.9$ rad/sample, noise variance $0.1$, $m = 8$, and the exact covariance $R = a(0.5)a(0.5)^H + a(0.9)a(0.9)^H + 0.1\,I$.

| quantity | value |
|---|---|
| eigenvalues of $R$ | $13.1313,\ 3.0687$ and six times $0.1$ |
| $\operatorname{tr}\Phi$ | $1.499193 + 1.262752i = e^{0.5i} + e^{0.9i}$ |
| eigenvalues of $\Phi$ | $0.877583 + 0.479426i$ and $0.621610 + 0.783327i$ |
| their moduli | $1.0000000000000000$ and $0.9999999999999997$ |
| their arguments | $0.5000000000000001$ and $0.9$ |

The entries of $\Phi$ depend on which orthonormal basis of the signal subspace the eigen solver returns, but its trace and eigenvalues do not. The errors are at the level of rounding, about $10^{-16}$, while MUSIC on the same matrix stops at about $10^{-9}$ because its minimum is flat. ESPRIT solves for the frequency instead of searching for a zero.

## Correctness

The signal eigenvectors span the range of $A = (a(\omega_1), \dots, a(\omega_d))$, so $S = AT$ for a nonsingular $d \times d$ matrix $T$. The Vandermonde structure gives $A_2 = A_1 D$ with $D = \operatorname{diag}(e^{i\omega_k})$. Hence $S_2 = A_1 D T = S_1 (T^{-1} D T)$. $S_1 = A_1 T$ has full column rank, because $A_1$ is an $(m - 1) \times d$ Vandermonde matrix with $d \le m - 1$. So the least-squares solution of line L4 is exact and unique, $\Phi = T^{-1}DT$. Similar matrices have the same eigenvalues, so line L5 gives $e^{i\omega_k}$ and line L6 the frequencies. The full proof is below.

## Complexity

**Time.** Line L1 costs $\Theta(m^3)$ per Jacobi sweep, with few sweeps. Line L4 costs $\Theta(md^2)$ to form the normal equations and $\Theta(d^3)$ to solve them. Line L5 costs $\Theta(d^4)$ with Faddeev-LeVerrier, or $\Theta(d^3)$ with a QR iteration. The total is $\Theta(m^3 + d^4)$ in the real-RAM model, plus $\Theta(Km^2)$ to form a sample covariance. Unlike MUSIC, there is no term for a grid. Only the $d$ signal eigenvectors are needed, so a partial method such as [subspace iteration](/subspace-iteration/) or a truncated [SVD](/singular-value-decomposition/) of the data matrix can reduce line L1.

**Space.** $\Theta(m^2)$ for the covariance and the eigenvectors.

## Properties

- **Exact with the exact covariance.** Over 200 random cases with $3 \le m \le 8$, $d \le \min(3, m - 1)$, frequencies at least $0.2$ apart, random powers and noise levels (seed 4903), every frequency was recovered to within $10^{-7}$.
- **Accuracy with a sample covariance.** On the data of the MUSIC page ($N = 200$, noise variance $0.1$, seeds 4803 to 4852), the root mean square error over both tones was $0.0018$ rad for $m = 8$, $0.00049$ for $m = 16$ and $0.00034$ for $m = 32$. MUSIC on the same records gave $0.0019$, $0.00050$ and $0.00036$. The Cramér-Rao bound for one tone is $0.00027$.
- **Resolution.** For tones at $0.5$ and $0.6$, noise variance $0.1$ and seeds 9000 to 9099, with "resolved" meaning both estimates within $0.05$ of their tones: at $N = 32$ and $m = 12$, ESPRIT resolved 42 records and 66 with forward-backward averaging, against 13 and 41 for MUSIC and 1 for the periodogram. At $N = 64$ and $m = 16$, ESPRIT resolved all 100.
- **No search, no spurious peaks.** The output is exactly $d$ numbers, so there is no grid to choose and no peak picking, which is the main practical advantage over MUSIC.
- **Needs the shift structure.** The method needs two identical subarrays related by one displacement. A uniform line array or a uniformly sampled record has it; an arbitrary array does not, where MUSIC still works.
- **Damping.** The eigenvalues of $\hat\Phi$ are not forced onto the unit circle. For damped exponentials their modulus estimates the damping, as in the matrix pencil form of Prony's method.

## Variants and improvements

- **Total least squares ESPRIT.** Line L4 treats $S_1$ as exact and $S_2$ as noisy. TLS-ESPRIT allows errors in both and solves through the SVD of $(S_1, S_2)$; it has a smaller bias at low signal to noise ratio.
- **Unitary ESPRIT.** For centrosymmetric arrays a unitary transform makes all the computation real, halves the cost and includes forward-backward averaging.
- **Matrix pencil.** Working with a Hankel matrix of the samples instead of a covariance gives the matrix pencil method of Hua and Sarkar, which also handles damped exponentials; see [Prony's method](/prony-method/).
- **Larger shifts.** Using subarrays displaced by $s$ entries gives eigenvalues $e^{is\omega}$, with better accuracy but an ambiguity of $2\pi/s$ in $\omega$.
- **Two-dimensional ESPRIT.** Shifts along two axes of a planar array give azimuth and elevation, paired by a joint diagonalization.

## When to use it

Use ESPRIT for a few sinusoids or narrowband sources in white noise when the sampling or the array has a shift invariance, and when a direct answer without a grid is wanted: frequency estimation of close tones, direction finding with uniform linear or rectangular arrays, and channel parameter estimation in wireless systems. It needs the number of sources $d$ and, for coherent sources, forward-backward averaging or spatial smoothing, as MUSIC does. For an array without the shift structure use [MUSIC](/music-algorithm/). For broadband spectra use a nonparametric estimator such as the [Welch method](/welch-method/).

## Pitfalls

- **Taking the wrong eigenvectors in line L2.** $S$ must hold the eigenvectors of the $d$ largest eigenvalues. A solver that returns them in increasing order, or the wrong $d$, gives a $\Phi$ whose eigenvalues mix signal and noise. Sort in line L1 and check the gap.
- **Swapping $S_1$ and $S_2$ in line L4.** Solving $S_2 \Phi = S_1$ gives eigenvalues $e^{-i\omega}$ and frequencies of the wrong sign. The convention has to match the definition of the steering vector.
- **Coherent sources.** If the sources are fully correlated, the signal part of $R$ has rank less than $d$ and Lemma 1 of the proof fails. Use forward-backward averaging or spatial smoothing when forming $R$.
- **Ill-conditioned $S_1$ in line L4.** With $m - 1$ close to $d$, or tones far closer than $2\pi/m$, $S_1^H S_1$ is close to singular. Choose $m$ well above $d$.
- **Calibration.** The two subarrays must be identical. A gain or phase error between them goes straight into $\Phi$ and biases every estimate.

## Implementations

## History

Richard Roy, Arogyaswami Paulraj and Thomas Kailath introduced ESPRIT in 1986 as a subspace rotation approach to the parameters of cisoids in noise, and Roy and Kailath developed it for sensor arrays with displacement invariance in 1989, with least-squares and total least-squares forms. It followed Schmidt's MUSIC and removed both the search and the need to know the array response at every angle; only the displacement between two subarrays matters. Hua and Sarkar's matrix pencil (1990) is the same idea applied to a Hankel matrix of samples. Unitary and multidimensional versions followed in the 1990s, and ESPRIT became a standard tool for direction finding and channel estimation.

## References
