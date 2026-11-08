---
tag: 0CRF9T
kind: problem
slug: trigonometric-interpolation
name: Trigonometric interpolation
aliases:
- Discrete Fourier interpolation
- Fourier interpolation
- Periodic interpolation
area: numerical/interpolation-and-approximation
level: core
summary: Find the trigonometric polynomial that matches periodic data at N points. At equispaced points its coefficients are a discrete Fourier transform, computed by the FFT in O(N log N).
prereqs: [discrete-fourier-transform, polynomial-interpolation]
see_also: [fast-fourier-transform, chebyshev-interpolation, aliasing, sinc-interpolation, gibbs-phenomenon, spectral-methods, nonuniform-fft, barycentric-interpolation]
sources:
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 13, The approximation of periodic functions (trigonometric interpolation at equally spaced points)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 3.8, Trigonometric interpolation (with the fast Fourier transform)
  - book: isbn:9780521890533
    title: Antoni Zygmund, Trigonometric Series, third edition, Cambridge University Press, 2002
    locator: Volume II, Chapter X, Trigonometric interpolation
  - paper: "Peter Henrici, Barycentric formulas for interpolating trigonometric polynomials and their conjugates, Numerische Mathematik 33 (1979) 225-234"
    locator: the barycentric formulas with cosecant and cotangent weights for equispaced points
  - paper: "Grady B. Wright, Mohsin Javed, Hadrien Montanelli and Lloyd N. Trefethen, Extension of Chebfun to periodic functions, SIAM Journal on Scientific Computing 37(5) (2015) C554-C573"
    locator: the convergence theorems for trigonometric interpolants of smooth and analytic periodic functions
  - paper: "Michael T. Heideman, Don H. Johnson and C. Sidney Burrus, Gauss and the history of the fast Fourier transform, IEEE ASSP Magazine 1(4) (1984) 14-21"
    locator: Gauss's trigonometric interpolation of asteroid orbits (about 1805) and his fast algorithm for it
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 3, Chebyshev polynomials and series (the link between Chebyshev and Fourier series through x = cos θ)
---

Trigonometric interpolation is the periodic counterpart of [polynomial interpolation](/polynomial-interpolation/): given $N$ samples of a $2\pi$-periodic function, find the trigonometric polynomial of the lowest degree that passes through them. At equispaced points, the usual case, the solution is unique once a convention fixes the highest frequency for even $N$, its coefficients are the [discrete Fourier transform](/discrete-fourier-transform/) of the samples, and the [FFT](/fast-fourier-transform/) computes them in $O(N \log N)$ operations. For smooth periodic functions the interpolants converge very fast, and they are the basis of Fourier [spectral methods](/spectral-methods/) and, through $x = \cos\theta$, of [Chebyshev interpolation](/chebyshev-interpolation/).

## In plain words

Many quantities repeat: the position of a planet over a year, a sound wave, the temperature over a day. If you measure such a quantity at evenly spaced times in one period, you can ask for the smoothest sum of waves (a constant, one full wave per period, two waves, and so on) that matches all the measurements.

With as many measurements as there are wave strengths to choose, there is exactly one such sum. Its wave strengths are what the discrete Fourier transform computes, and the fast Fourier transform computes them quickly. If the true quantity is smooth, the sum is extremely close to it between the measurements too.

## Definition

Notation on the interpolation pages: $f$ is a real or complex $2\pi$-periodic function; the nodes are $\theta_0 < \theta_1 < \cdots < \theta_{N-1}$ in $[0, 2\pi)$, equispaced unless said otherwise, $\theta_j = 2\pi j/N$; the data are $y_j = f(\theta_j)$. A **trigonometric polynomial of degree at most $m$** is $t(\theta) = \sum_{k=-m}^{m} c_k e^{ik\theta}$, equivalently $a_0/2 + \sum_{k=1}^{m} (a_k \cos k\theta + b_k \sin k\theta)$; these form the space $\mathcal{T}_m$ of dimension $2m + 1$.

**Problem.** Given the nodes and data, find $t$ with $t(\theta_j) = y_j$ for $j = 0, \ldots, N - 1$.

**Odd $N = 2m + 1$.** There is exactly one $t \in \mathcal{T}_m$, and at equispaced nodes
$$t(\theta) = \sum_{k=-m}^{m} c_k e^{ik\theta}, \qquad c_k = \frac{1}{N} \sum_{j=0}^{N-1} y_j e^{-ik\theta_j}.$$
*Proof.* The discrete orthogonality $\sum_{j=0}^{N-1} e^{i(k - l)\theta_j} = N$ if $k \equiv l \pmod N$ and 0 otherwise (a geometric sum of $N$-th roots of unity) shows that the $N \times N$ matrix $(e^{ik\theta_j})$ with $k = -m, \ldots, m$ satisfies $V^* V = N I$. So it is invertible, and the coefficients are $c = V^* y/N$, as displayed. For any distinct nodes, existence and uniqueness also hold: $t \in \mathcal{T}_m$ is $e^{-im\theta} q(e^{i\theta})$ with $q$ an algebraic polynomial of degree at most $2m$, and $q$ is fixed by its values at the $2m + 1$ distinct points $e^{i\theta_j}$ on the unit circle.

**Even $N = 2m$.** $\mathcal{T}_m$ has dimension $N + 1$, one too many, and at equispaced nodes $e^{im\theta_j} = e^{-im\theta_j} = (-1)^j$, so $\sin m\theta$ vanishes at every node. The standard convention keeps only $\cos m\theta$ for the top frequency, splitting $c_m$ evenly:
$$t(\theta) = \sum_{k=-m+1}^{m-1} c_k e^{ik\theta} + c_m \cos m\theta,$$
with the same formula for $c_k$. This is the unique interpolant in $\mathcal{T}_{m-1} \oplus \operatorname{span}\{\cos m\theta\}$, and it is real when the data are real.

**Barycentric form.** At equispaced nodes (Henrici 1979),
$$t(\theta) = \frac{\sum_j (-1)^j y_j\, \operatorname{cst}\big(\tfrac{\theta - \theta_j}{2}\big)}{\sum_j (-1)^j \operatorname{cst}\big(\tfrac{\theta - \theta_j}{2}\big)}, \qquad \operatorname{cst} = \csc \text{ for odd } N,\ \cot \text{ for even } N,$$
which evaluates $t$ at one point in $O(N)$ operations and is numerically stable.

## Variants

- **Non-equispaced nodes.** For odd $N$ and any distinct nodes the interpolant exists and has a Lagrange form with basis functions $\prod_{l \ne j} \sin\frac{\theta - \theta_l}{2} / \sin\frac{\theta_j - \theta_l}{2}$ (Gauss's formula). The DFT no longer applies; [nonuniform FFT](/nonuniform-fft/) methods or a linear solve are used.
- **Cosine and sine interpolation.** Even data $f(-\theta) = f(\theta)$ give a cosine sum, computed by a [discrete cosine transform](/discrete-cosine-transform/). With $x = \cos\theta$ this is polynomial interpolation at Chebyshev points: the [Chebyshev interpolant](/chebyshev-interpolation/) of $g$ on $[-1, 1]$ is the cosine interpolant of $g(\cos\theta)$.
- **Least squares.** With $N$ data and a degree $m' < (N-1)/2$, the best fit in the discrete $\ell^2$ norm is the truncation of the interpolant to $|k| \le m'$, again by orthogonality.
- **Hermite and derivative data.** Values and derivatives at $N$ equispaced points determine a trigonometric polynomial of twice the degree.
- **Several dimensions.** On a tensor grid, a multidimensional DFT gives the tensor-product interpolant (see [tensor-product interpolation](/tensor-product-interpolation/)).
- **Band-limited interpolation.** On the whole line with spacing $h$, the analogue is [sinc interpolation](/sinc-interpolation/) of the [sampling theorem](/sampling-theorem/); the periodic interpolant is the periodic sum of sinc functions.

## Examples

**$N = 4$.** Data $1, 2, 0, 1$ at $\theta = 0, \pi/2, \pi, 3\pi/2$. The DFT gives $c_0 = 1$, $c_{1} = \tfrac14 - \tfrac14 i$, $c_{-1} = \tfrac14 + \tfrac14 i$ and $c_2 = -\tfrac12$, so
$$t(\theta) = 1 + \tfrac12 \cos\theta + \tfrac12 \sin\theta - \tfrac12 \cos 2\theta.$$
Check: $t(0) = 1 + \tfrac12 - \tfrac12 = 1$, $t(\pi/2) = 1 + \tfrac12 + \tfrac12 = 2$, $t(\pi) = 1 - \tfrac12 - \tfrac12 = 0$, $t(3\pi/2) = 1 - \tfrac12 + \tfrac12 = 1$. Adding any multiple of $\sin 2\theta$ would also interpolate; the convention removes it.

**Convergence.** Maximum error on a grid of 3001 points of $[0, 2\pi)$, odd $N$, in double precision:

| $N$ | $e^{\sin\theta}$ | $1/(1 + 25\sin^2(\theta/2))$ | $\lvert\sin\theta\rvert$ |
|---|---|---|---|
| 5 | $9.3 \times 10^{-2}$ | 0.40 | 0.29 |
| 11 | $9.1 \times 10^{-5}$ | 0.11 | 0.21 |
| 21 | $5.0 \times 10^{-11}$ | $1.5 \times 10^{-2}$ | $8.7 \times 10^{-2}$ |
| 41 | $4.0 \times 10^{-15}$ | $2.9 \times 10^{-4}$ | $4.6 \times 10^{-2}$ |
| 81 | $4.4 \times 10^{-15}$ | $1.0 \times 10^{-7}$ | $2.3 \times 10^{-2}$ |

The entire function converges faster than any geometric rate and stops at rounding level. The second function has poles at $\operatorname{Im}\theta = \pm 2\operatorname{arsinh}(1/5) \approx \pm 0.397$; from $N = 41$ to $81$, $m$ grows by 20 and the error falls by about $2800 \approx e^{0.397 \cdot 20}$, the rate predicted below. The kinked $|\sin\theta|$ converges only like $1/N$. The DFT and barycentric evaluations agreed to $2 \times 10^{-14}$ in all cases. For data with a jump, the interpolants oscillate near the jump and do not converge uniformly (the [Gibbs phenomenon](/gibbs-phenomenon/)).

## Known algorithms

- **FFT.** The coefficients $c_k$ of equispaced data cost $O(N \log N)$ operations by the [fast Fourier transform](/fast-fourier-transform/), for any $N$ (with Bluestein's or Rader's algorithm for prime $N$). Evaluating $t$ back at the nodes is the [inverse DFT](/inverse-discrete-fourier-transform/).
- **Evaluation on a finer grid.** Padding the coefficient vector with zeros to length $M$ and applying an inverse FFT gives $t$ at $M$ equispaced points in $O(M \log M)$: this is Fourier resampling. For even $N$ the top coefficient must be split in half between $\pm m$.
- **Evaluation at arbitrary points.** The barycentric formula costs $O(N)$ per point; Horner's rule in $z = e^{i\theta}$ also costs $O(N)$; a nonuniform FFT handles $M$ points in $O(N \log N + M \log(1/\varepsilon))$ to accuracy $\varepsilon$.
- **Non-equispaced nodes.** Gauss's Lagrange form costs $O(N^2)$ setup and $O(N)$ per point in barycentric form; general linear solves cost $O(N^3)$.

## Bounds

- **Aliasing error.** Let $f$ have an absolutely convergent Fourier series $f = \sum_k a_k e^{ik\theta}$, and $N = 2m + 1$. Since $e^{ik\theta_j} = e^{i(k + lN)\theta_j}$, the computed coefficients are $c_k = \sum_{l} a_{k + lN}$ ([aliasing](/aliasing/)). Each $a_j$ with $|j| > m$ enters the error once as itself and once through some $c_k$, so
$$\|f - t\|_\infty \le 2 \sum_{|k| > m} |a_k|.$$
The interpolant is within a factor 2 of the truncated Fourier series in this bound.
- **Analytic functions.** If $f$ is analytic and $|f| \le M$ in the strip $|\operatorname{Im}\theta| < \alpha$, then $|a_k| \le M e^{-\alpha|k|}$, and the bound gives $\|f - t\|_\infty \le 4M e^{-\alpha m}/(e^\alpha - 1)$, a geometric rate fixed by the width of the strip (Wright, Javed, Montanelli and Trefethen 2015).
- **Finite smoothness.** If $f^{(\nu - 1)}$ is absolutely continuous and $f^{(\nu)}$ has bounded variation $V$, then $|a_k| \le V/(2\pi|k|^{\nu+1})$ and $\|f - t\|_\infty = O(m^{-\nu})$.
- **Lebesgue constant.** At equispaced nodes, the operator norm of interpolation in the maximum norm grows like $\tfrac{2}{\pi}\log N + O(1)$ (Zygmund, Chapter X), so for any continuous $f$, $\|f - t\| \le (1 + \Lambda_N) E^{\mathcal{T}}_m(f)$, where $E^{\mathcal{T}}_m$ is the best error by trigonometric polynomials. Equispaced nodes play for periodic functions the role that Chebyshev nodes play on an interval. As for polynomials, some continuous functions have divergent interpolants.
- **Lower bound for the transform.** In the model of linear algorithms with bounded coefficients, computing the DFT needs $\Omega(N \log N)$ operations (Morgenstern 1973); see the [FFT](/fast-fourier-transform/) page.

## Reductions

- **To and from the DFT.** At equispaced nodes, trigonometric interpolation is the DFT up to scaling and reindexing, so the two problems have the same cost.
- **Chebyshev interpolation reduces to it.** For $g$ on $[-1, 1]$, the polynomial interpolant at Chebyshev points $\cos(\pi j/n)$ equals $t(\arccos x)$, where $t$ is the cosine interpolant of $g(\cos\theta)$ at $2n$ equispaced points. This is how Chebyshev coefficients are computed by FFT in $O(n \log n)$.
- **Polynomial interpolation on the circle.** With $z = e^{i\theta}$, odd-$N$ trigonometric interpolation is algebraic interpolation of degree $N - 1$ at $N$ points of the unit circle, multiplied by $z^{-m}$. At roots of unity the [Vandermonde matrix](/vandermonde-matrix/) is unitary up to scaling, the reason the problem is perfectly conditioned.

## Applications

- **Spectral methods.** Fourier [spectral methods](/spectral-methods/) differentiate the interpolant to solve periodic differential equations with geometric accuracy.
- **Signal and image processing.** Resampling, fractional delays and zero-padding upsampling of periodic or windowed signals.
- **Quadrature.** Integrating the interpolant gives the trapezoidal rule, which is therefore geometrically accurate for analytic periodic integrands.
- **Astronomy, its origin.** Gauss interpolated the orbits of the asteroids Pallas and Juno with trigonometric sums around 1805 and found a divide-and-conquer method for the coefficients, a precursor of the FFT (Heideman, Johnson and Burrus 1984).
- **Chebyshev technology.** Through $x = \cos\theta$, all fast Chebyshev interpolation, quadrature ([Clenshaw-Curtis](/clenshaw-curtis-quadrature/)) and coefficient computation.

## References
