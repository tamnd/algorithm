---
tag: RFEBRV
kind: definition
slug: legendre-polynomials
name: Legendre polynomials
aliases:
- Legendre orthogonal polynomials
- Legendre polynomials P_k
- Zonal spherical harmonics in three dimensions
area: numerical/interpolation-and-approximation
level: advanced
summary: The orthogonal polynomials on [-1, 1] with weight 1, normalized by P_k(1) = 1. They satisfy (k+1)P_(k+1) = (2k+1)x P_k - k P_(k-1), and their zeros are the Gauss-Legendre nodes.
prereqs: [orthogonal-polynomials]
see_also: [chebyshev-polynomials, gauss-legendre-quadrature, least-squares-approximation, hilbert-matrix, golub-welsch-algorithm, spectral-methods, chebyshev-series, gram-schmidt-process]
sources:
  - paper: "Adrien-Marie Legendre, Recherches sur l'attraction des sphéroïdes homogènes, Mémoires de Mathématiques et de Physique, présentés à l'Académie Royale des Sciences par divers savans 10 (1785) 411-434"
    locator: the coefficients of the expansion of the inverse distance, which are the polynomials now named after Legendre
  - book: isbn:9780821810231
    title: Gábor Szegő, Orthogonal Polynomials, fourth edition, American Mathematical Society Colloquium Publications 23, 1975
    locator: Chapter IV, Jacobi polynomials (Legendre polynomials as the case alpha = beta = 0), and Chapter VII, inequalities for the polynomials
  - url: https://dlmf.nist.gov/18
    title: NIST Digital Library of Mathematical Functions, Chapter 18, Orthogonal Polynomials
    locator: Sections 18.3 (definitions), 18.5 (Rodrigues formula), 18.9 (recurrences) and 18.12 (generating functions), for the Legendre case
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 17, Orthogonal polynomials (Legendre polynomials and least-squares approximation)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 4.4, Orthogonal polynomials (the Legendre case and least squares approximation)
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 11, The theory of best L2 approximation, and Chapter 12, Properties of orthogonal polynomials
---

The Legendre polynomials $P_0, P_1, P_2, \ldots$ are the [orthogonal polynomials](/orthogonal-polynomials/) on $[-1, 1]$ for the constant weight, normalized so that $P_k(1) = 1$. They are the natural basis for least-squares polynomial approximation in the plain $L^2$ norm. Their zeros are the nodes of [Gauss-Legendre quadrature](/gauss-legendre-quadrature/), and they arose as the coefficients in Legendre's expansion of the gravitational potential, where they still serve as the zonal spherical harmonics.

## Definition

Notation on the interpolation pages: functions live on $[-1, 1]$, $\mathcal{P}_n$ is the space of polynomials of degree at most $n$, $\langle f, g \rangle = \int_{-1}^{1} f(x) g(x)\, dx$, and $T_k$ denotes the Chebyshev polynomials.

**Definition.** The **Legendre polynomial** $P_k$ is the polynomial of exact degree $k$ such that

1. $\langle P_k, q \rangle = 0$ for every $q \in \mathcal{P}_{k-1}$ (orthogonality), and
2. $P_k(1) = 1$ (normalization).

Existence and uniqueness: applying Gram-Schmidt to $1, x, x^2, \ldots$ gives, for each $k$, a polynomial $\pi_k$ of exact degree $k$ orthogonal to $\mathcal{P}_{k-1}$, unique up to a constant factor, since the orthogonal complement of $\mathcal{P}_{k-1}$ in $\mathcal{P}_k$ is one-dimensional. A real polynomial orthogonal to $\mathcal{P}_{k-1}$ for a positive weight has $k$ simple zeros in $(-1, 1)$, so $\pi_k(1) \ne 0$ and the normalization fixes the factor.

**Equivalent descriptions.**

- **Rodrigues formula:** $P_k(x) = \dfrac{1}{2^k k!} \dfrac{d^k}{dx^k} (x^2 - 1)^k$. Repeated integration by parts shows that it is orthogonal to $\mathcal{P}_{k-1}$, because $(x^2 - 1)^k$ and its first $k - 1$ derivatives vanish at $\pm 1$.
- **Three-term recurrence (Bonnet):** $P_0 = 1$, $P_1 = x$, and $(k + 1) P_{k+1}(x) = (2k + 1)\, x\, P_k(x) - k\, P_{k-1}(x)$.
- **Generating function:** $\dfrac{1}{\sqrt{1 - 2xt + t^2}} = \sum_{k \ge 0} P_k(x)\, t^k$ for $|t| < 1$, $x \in [-1, 1]$. This is Legendre's original setting: $1/|r - r'|$ expanded in powers of $|r'|/|r|$, with $x$ the cosine of the angle between $r$ and $r'$.
- **Differential equation:** $y = P_k$ solves $(1 - x^2) y'' - 2x y' + k(k + 1) y = 0$.

**Basic facts.**

- $\langle P_j, P_k \rangle = \dfrac{2}{2k + 1}\, \delta_{jk}$.
- Leading coefficient $\dfrac{(2k)!}{2^k (k!)^2}$; parity $P_k(-x) = (-1)^k P_k(x)$; $P_k(\pm 1) = (\pm 1)^k$.
- $|P_k(x)| \le 1$ on $[-1, 1]$, with equality only at $\pm 1$ for $k \ge 1$; inside the interval the polynomials are smaller, of size about $(2/(\pi k \sin\theta))^{1/2}$ at $x = \cos\theta$ (Szegő, Chapter VII).
- $P_k$ has $k$ simple zeros in $(-1, 1)$, and the zeros of $P_k$ and $P_{k+1}$ interlace.
- **Least squares.** For $f \in L^2[-1, 1]$, the best approximation from $\mathcal{P}_n$ in the $L^2$ norm is the truncated **Legendre series** $\sum_{k=0}^{n} a_k P_k$ with $a_k = \tfrac{2k+1}{2} \langle f, P_k \rangle$.

## Examples and non-examples

**The first six.** From the recurrence:

| $k$ | $P_k(x)$ |
|---|---|
| 0 | $1$ |
| 1 | $x$ |
| 2 | $\tfrac12 (3x^2 - 1)$ |
| 3 | $\tfrac12 (5x^3 - 3x)$ |
| 4 | $\tfrac18 (35x^4 - 30x^2 + 3)$ |
| 5 | $\tfrac18 (63x^5 - 70x^3 + 15x)$ |

For example $P_2 = \big(3x \cdot x - 1\big)/2$ from the recurrence with $k = 1$, and $\langle P_0, P_2 \rangle = \tfrac12 \int_{-1}^{1} (3x^2 - 1)\, dx = \tfrac12 (2 - 2) = 0$. The zeros of $P_2$ are $\pm 1/\sqrt{3}$, the nodes of the two-point Gauss-Legendre rule.

**Legendre series.** For $e^x$ the coefficients are $a_0 = \sinh 1 \approx 1.175$, $a_1 = 3/e \approx 1.104$, then $0.358$, $0.0705$, $9.97 \times 10^{-3}$, $1.10 \times 10^{-3}$, $9.95 \times 10^{-5}$, $7.62 \times 10^{-6}$, $5.07 \times 10^{-7}$ for $k = 2, \ldots, 8$: faster than geometric decay, as for any entire function. For $|x|$ the odd coefficients vanish and the even ones are $\tfrac12, \tfrac58, -\tfrac{3}{16}, \tfrac{13}{128}, \ldots$, decaying like $k^{-3/2}$ because of the kink at 0.

**Conditioning, compared with monomials.** The Gram matrix $G_{ij} = \langle \phi_i, \phi_j \rangle$ of a basis decides how well least-squares coefficients can be computed from the normal equations. For the Legendre basis it is diagonal, $\operatorname{diag}(2/(2k+1))$, with 1-norm condition number $2n + 1$. For the monomials $1, x, \ldots, x^n$ on $[-1, 1]$ (entries $2/(i + j + 1)$ for $i + j$ even, else 0) the exact 1-norm condition numbers are $2.8 \times 10^3$, $1.9 \times 10^7$, $1.2 \times 10^{11}$ and $7.3 \times 10^{14}$ for $n = 5, 10, 15, 20$; on $[0, 1]$ the Gram matrix is the [Hilbert matrix](/hilbert-matrix/), with $2.9 \times 10^7$ and $1.2 \times 10^{15}$ for $n = 5, 10$. This is the main numerical reason to expand in Legendre or Chebyshev polynomials rather than in powers of $x$.

**Evaluation in floating point.** The three-term recurrence is stable for $|x| \le 1$: in double precision, $P_{20}$, $P_{50}$ and $P_{100}$ computed by it differ from the exact values (in rational arithmetic, at the same 30 random points) by at most $2.8 \times 10^{-16}$, $2.2 \times 10^{-16}$ and $5.3 \times 10^{-16}$. A Legendre series $\sum a_k P_k(x)$ is evaluated by Clenshaw's recurrence in $O(n)$ operations without forming the monomial coefficients, which grow like $2^k$ and cancel.

**Non-examples.**

- The monomials $1, x, x^2$ are not orthogonal on $[-1, 1]$: $\langle 1, x^2 \rangle = 2/3$.
- The [Chebyshev polynomials](/chebyshev-polynomials/) $T_k$ are orthogonal for the weight $(1 - x^2)^{-1/2}$, not for weight 1: $\langle T_0, T_2 \rangle = \int_{-1}^{1} (2x^2 - 1)\, dx = -2/3$.
- The Legendre functions of the second kind $Q_k$ solve the same differential equation but are not polynomials ($Q_0 = \tfrac12 \log\frac{1+x}{1-x}$).
- The [Legendre symbol](/legendre-symbol/) of number theory is unrelated.

## Related definitions

- **Orthogonal polynomials** for a general weight: Legendre is the case $w = 1$ on $[-1, 1]$ ([orthogonal polynomials](/orthogonal-polynomials/)); it is the Jacobi family with $\alpha = \beta = 0$, and the Gegenbauer family with $\lambda = 1/2$.
- **Shifted Legendre polynomials** $\tilde P_k(x) = P_k(2x - 1)$ are orthogonal on $[0, 1]$.
- **Orthonormal Legendre polynomials** $\sqrt{(2k+1)/2}\, P_k$; the monic ones $\tfrac{2^k (k!)^2}{(2k)!} P_k$ have the least $L^2$ norm among monic polynomials of degree $k$, the $L^2$ analogue of the extremal property of $2^{1-k} T_k$ in the maximum norm.
- **Associated Legendre functions** $P_k^m(x) = (-1)^m (1 - x^2)^{m/2} \frac{d^m}{dx^m} P_k(x)$, which with $e^{im\phi}$ form the spherical harmonics.
- **Gauss-Legendre quadrature** uses the zeros of $P_{n+1}$ as nodes; the [Golub-Welsch algorithm](/golub-welsch-algorithm/) computes them as eigenvalues of the symmetric tridiagonal matrix of the recurrence, with off-diagonal entries $k/\sqrt{4k^2 - 1}$.

## References
