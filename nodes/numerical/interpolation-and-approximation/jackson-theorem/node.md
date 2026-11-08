---
tag: D5NKDF
kind: theorem
slug: jackson-theorem
name: Jackson theorem
aliases:
- Jackson's inequality
- Jackson's theorems
- Jackson-type estimate
- direct theorem of approximation theory
area: numerical/interpolation-and-approximation
level: research
summary: The best approximation error of a continuous f by polynomials of degree n is at most a constant times its modulus of continuity at 1/n, and smoother f gain a factor 1/n per derivative.
prereqs: [weierstrass-approximation-theorem, minimax-approximation]
see_also: [chebyshev-equioscillation-theorem, lebesgue-constant, chebyshev-interpolation, chebyshev-series, kolmogorov-width, trigonometric-interpolation, approximation-theory, stone-weierstrass-theorem]
sources:
  - paper: "Dunham Jackson, Über die Genauigkeit der Annäherung stetiger Funktionen durch ganze rationale Funktionen gegebenen Grades und trigonometrische Summen gegebener Ordnung, dissertation, Göttingen, 1911"
    locator: the original direct theorems for trigonometric and algebraic polynomials
  - book: isbn:9780821813744
    title: E. W. Cheney, Introduction to Approximation Theory, second edition, AMS Chelsea, 1998
    locator: Chapter 4, The degree of approximation (Jackson's theorems I to V and the Bernstein inverse theorems)
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 15, Jackson's theorems, and Chapter 16, The theorems of Bernstein
  - book: isbn:9783540506270
    title: Ronald A. DeVore and George G. Lorentz, Constructive Approximation, Springer, 1993
    locator: Chapter 7, Approximation by polynomials (direct and inverse theorems, the Jackson kernel, Timan's pointwise estimates)
  - book: isbn:9780387965369
    title: Z. Ditzian and V. Totik, Moduli of Smoothness, Springer, 1987
    locator: Chapters 2 and 7, the modulus ω_φ and the two-sided characterization of E_n(f) on an interval
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 7, Convergence for differentiable functions (Theorem 7.2 and the notes on Jackson's theorems)
  - paper: "R. S. Varga and A. J. Carpenter, On the Bernstein conjecture in approximation theory, Constructive Approximation 1 (1985) 333-348"
    locator: the Bernstein constant β = 0.2801694990... for E_n(|x|)
---

Jackson's theorem bounds how well a continuous function can be approximated by polynomials of a given degree, in terms of how smooth the function is. If $f$ is continuous on $[-1, 1]$ with modulus of continuity $\omega(f, \delta)$, then its best uniform approximation error $E_n(f)$ by polynomials of degree at most $n$ satisfies $E_n(f) \le C\,\omega(f, 1/n)$. Each additional derivative improves the bound by a factor of order $1/n$. It is the basic direct theorem of approximation theory. It quantifies the [Weierstrass theorem](/weierstrass-approximation-theorem/), and together with the [Lebesgue constant](/lebesgue-constant/) it gives convergence rates for interpolation and for spectral methods. Bernstein's inverse theorems show that the rates are sharp for periodic functions. On an interval they are sharp only in the interior, which led to the moduli of Ditzian and Totik.

## Statement

Notation on the interpolation and approximation pages: $f$ is continuous on $[-1, 1]$ (or $2\pi$-periodic for the trigonometric case); $\|\cdot\|$ is the maximum norm; $E_n(f) = \min_{\deg p \le n}\|f - p\|$; $E_n^T(g)$ is the same for trigonometric polynomials of degree at most $n$ and a continuous $2\pi$-periodic $g$. The modulus of continuity is
$$\omega(f, \delta) = \sup\{|f(x) - f(y)| : |x - y| \le \delta\},$$
which tends to $0$ as $\delta \to 0$ by uniform continuity, and satisfies $\omega(f, \lambda\delta) \le (1 + \lambda)\omega(f, \delta)$ for $\lambda \ge 0$.

**Theorem (Jackson, 1911).** There is an absolute constant $C$ such that for all $n \ge 1$:

1. *(Trigonometric.)* For continuous $2\pi$-periodic $g$, $E_n^T(g) \le C\,\omega(g, 1/n)$.
2. *(Algebraic.)* For continuous $f$ on $[-1, 1]$, $E_n(f) \le C\,\omega(f, 1/n)$.
3. *(Lipschitz.)* If $|f(x) - f(y)| \le M|x - y|$, then $E_n(f) \le CM/n$.
4. *(Derivatives.)* If $f \in C^k[-1, 1]$ and $n > k$, then
$$E_n(f) \le \frac{C^{k+1}}{n(n - 1)\cdots(n - k + 1)}\;\omega\Big(f^{(k)}, \frac{1}{n - k}\Big),$$
in particular $E_n(f) = O(n^{-k}\omega(f^{(k)}, 1/n))$, and $E_n(f) = O(n^{-k-\alpha})$ if $f^{(k)}$ is Hölder continuous of order $\alpha \in (0, 1]$.

The proof below gives $C \le 192$. The best constants are much smaller: for periodic $g$, $E_n^T(g) \le \omega(g, \pi/(n + 1))$ (Korneichuk, 1962), and for Lipschitz $g$, $E_n^T(g) \le \frac{\pi M}{2(n + 1)}$ (Favard and Akhiezer-Krein), both sharp.

## In plain words

A wiggly or kinked function is hard to copy with a polynomial; a smooth one is easy. Jackson's theorem makes this exact. It measures roughness by how much the function can change over a short distance, and says that a polynomial of degree $n$ can match the function to within a constant times the change over a distance $1/n$. If the function has a corner, like $|x|$, the error falls like $1/n$. If it has three smooth derivatives, the error falls like $1/n^3$. The higher the degree, the finer the scale the polynomial can resolve.

## Proof

**Step 1: the Jackson kernel.** Let $m = \lfloor n/2\rfloor + 1$ and $D(t) = \sin(mt/2)/\sin(t/2)$. Then $D(t)^2 = \sum_{|j| < m}(m - |j|)e^{ijt}$ is a nonnegative trigonometric polynomial of degree $m - 1$, so $D^4$ is one of degree $2m - 2 \le n$. Define $J(t) = D(t)^4/A$ with $A = \int_{-\pi}^{\pi}D^4\,dt$, so $J \ge 0$, $J$ is even and $\int_{-\pi}^{\pi}J = 1$.

**Step 2: the kernel concentrates at scale $1/n$.** We show $\int_{-\pi}^{\pi}|t|J(t)\,dt \le c/n$ with $c = \pi^3(1 + \pi^4)/16 < 191$.

- *Lower bound for $A$.* For $|t| \le \pi/m$, $\sin(m|t|/2) \ge \frac2\pi\cdot\frac{m|t|}2$ (concavity of $\sin$ on $[0, \frac\pi2]$) and $|\sin(t/2)| \le |t|/2$, so $|D| \ge 2m/\pi$. Hence $A \ge \frac{2\pi}m\big(\frac{2m}{\pi}\big)^4 = \frac{32m^3}{\pi^3}$.
- *Upper bound for $B = \int|t|D^4$.* Always $|D| \le m$, and for $|t| \le \pi$, $|\sin(t/2)| \ge |t|/\pi$, so $|D| \le \pi/|t|$. Then $B \le 2\int_0^{1/m}tm^4\,dt + 2\int_{1/m}^\infty t\cdot\pi^4t^{-4}\,dt = m^2 + \pi^4m^2$.

So $\int|t|J = B/A \le \pi^3(1 + \pi^4)/(32m) < \pi^3(1 + \pi^4)/(16n)$, using $m > n/2$.

**Step 3: the trigonometric case.** For continuous $2\pi$-periodic $g$ let $T(x) = \int_{-\pi}^{\pi}g(x - t)J(t)\,dt$. Writing $J$ as a sum of $e^{ijt}$, $|j| \le n$, shows that $T$ is a trigonometric polynomial of degree at most $n$. Since $\int J = 1$ and $J \ge 0$,
$$|g(x) - T(x)| \le \int|g(x) - g(x - t)|J(t)\,dt \le \int\omega(g, |t|)J(t)\,dt \le \omega(g, \tfrac1n)\int(1 + n|t|)J(t)\,dt \le (1 + c)\,\omega(g, \tfrac1n).$$
So part 1 holds with $C = 1 + c < 192$.

**Step 4: the algebraic case.** Given $f$ on $[-1, 1]$, put $g(\theta) = f(\cos\theta)$. Since $|\cos a - \cos b| \le |a - b|$, $\omega(g, \delta) \le \omega(f, \delta)$. The function $g$ is even and $J$ is even, so $T$ is even, $T(\theta) = \sum_{k \le n}a_k\cos k\theta = \sum a_kT_k(\cos\theta)$ in terms of Chebyshev polynomials. So $p = \sum a_kT_k$ is an algebraic polynomial of degree at most $n$ with $\|f - p\| = \|g - T\| \le C\omega(f, 1/n)$. This is part 2, and part 3 follows from $\omega(f, \delta) \le M\delta$.

**Step 5: derivatives.** Let $f \in C^1$ and let $q$ be the best approximation of degree $n - 1$ to $f'$. With $Q(x) = \int_0^xq$, of degree at most $n$, the function $f - Q$ has derivative $f' - q$, so $\omega(f - Q, \delta) \le \delta E_{n-1}(f')$. Applying part 2 to $f - Q$, and using $E_n(f) = E_n(f - Q)$,
$$E_n(f) \le C\,\omega(f - Q, \tfrac1n) \le \frac{C}{n}E_{n-1}(f').$$
Applying this $k$ times gives $E_n(f) \le \frac{C^k}{n(n-1)\cdots(n-k+1)}E_{n-k}(f^{(k)})$, and part 2 bounds $E_{n-k}(f^{(k)}) \le C\omega(f^{(k)}, 1/(n - k))$ for $n > k$. This is part 4. $\square$

## Consequences

**Weierstrass with a rate.** Since $\omega(f, 1/n) \to 0$, the theorem reproves the Weierstrass theorem and says how fast the best error goes to zero.

**Convergence of interpolation.** Combined with the Lebesgue inequality $\|f - p_n\| \le (1 + \Lambda_n)E_n(f)$ and $\Lambda_n \le \frac2\pi\log(n + 1) + 1$ for Chebyshev points, [Chebyshev interpolation](/chebyshev-interpolation/) converges for every $f$ with $\omega(f, \delta)\log\delta \to 0$ (the Dini-Lipschitz condition), and at the rate $O(n^{-k-\alpha}\log n)$ for $f^{(k)} \in \operatorname{Lip}\alpha$.

**Example: $|x|$.** Here $\omega(|x|, \delta) = \delta$, so $E_n(|x|) \le C/n$. The true behaviour is $E_{2n}(|x|) \sim \beta/(2n)$ with the Bernstein constant $\beta = 0.2801694990\ldots$ (Bernstein 1914 proved the limit exists; Varga and Carpenter 1985 computed it). The order $1/n$ is right; the constant in the proof is far from it.

**Example: smooth functions.** For $e^x$, all derivatives are bounded by $e$, and part 4 gives $E_n = O(n^{-k})$ for every $k$, but no geometric rate. Analytic functions converge geometrically ([Chebyshev series](/chebyshev-series/), Bernstein ellipses), which Jackson's theorem does not capture.

**Error of Chebyshev truncation.** For $f$ whose $k$-th derivative has bounded variation, ATAP Theorem 7.2 gives explicit bounds of the same order $n^{-k}$ for Chebyshev truncation and interpolation, a concrete Jackson-type estimate with good constants.

**Function spaces.** Jackson and Bernstein theorems together identify the approximation spaces $\{f : E_n(f) = O(n^{-s})\}$ with Hölder-Zygmund (Besov) spaces in the periodic case. This is the model for the theory of approximation spaces and for wavelet and adaptive approximation.

## Tightness

- **Periodic case: sharp, with a converse (proved).** Bernstein's inverse theorem: if $E_n^T(g) \le Mn^{-\alpha}$ with $0 < \alpha < 1$, then $g \in \operatorname{Lip}\alpha$; and if $E_n^T(g) = O(n^{-k-\alpha})$ then $g^{(k)} \in \operatorname{Lip}\alpha$. For $\alpha = 1$ the converse gives the Zygmund class instead of Lipschitz. So $\omega(g, 1/n)$ cannot be replaced by anything smaller for the whole Hölder class.
- **Constants (proved).** Korneichuk's bound $\omega(g, \pi/(n + 1))$ and Favard's $\frac{\pi M}{2(n + 1)}$ are attained for suitable $g$, so no smaller constants hold uniformly.
- **Algebraic case: not sharp at the endpoints (proved).** Polynomials approximate better near $\pm1$. For $f(x) = \sqrt{1 - x}$, $\omega(f, \delta) = \sqrt\delta$, so Jackson gives only $E_n(f) = O(n^{-1/2})$. But $f(\cos\theta) = \sqrt2|\sin(\theta/2)|$ is Lipschitz, its Chebyshev coefficients are $a_k = -\frac{4\sqrt2}{\pi(4k^2 - 1)}$ for $k \ge 1$, and truncation gives $E_n(f) \le \sum_{k>n}|a_k| = \frac{2\sqrt2}{\pi(2n + 1)}$. The rate is $1/n$, not $1/\sqrt n$. Timan's pointwise theorem explains this: there are polynomials with $|f(x) - p_n(x)| \le C\,\omega\big(f, \frac{\sqrt{1 - x^2}}n + \frac1{n^2}\big)$, which is finer near the ends. Ditzian and Totik's modulus $\omega_\varphi^r(f, t)$ with step $t\sqrt{1 - x^2}$ gives a two-sided characterization: $E_n(f) = O(n^{-\alpha})$ if and only if $\omega_\varphi^r(f, t) = O(t^\alpha)$, for $0 < \alpha < r$.
- **Analytic functions.** For these the bound $O(n^{-k})$ for every $k$ is far from the true geometric rate; Jackson's theorem is a statement about finite smoothness.
- **Several variables.** On a cube in $\mathbb{R}^d$ the analogous bound is $E_n(f) \le C_d\,\omega(f, 1/n)$ with total degree $n$, so for a fixed number of parameters $N \approx n^d$ the rate is $\omega(f, N^{-1/d})$, the curse of dimensionality. [Kolmogorov widths](/kolmogorov-width/) show that no linear method does better on the whole Hölder class.

## History

Dunham Jackson proved the direct theorems in his 1911 Göttingen dissertation, written under Landau, answering questions raised by Lebesgue and de la Vallée Poussin about the speed of convergence in the Weierstrass theorem. Sergei Bernstein proved the inverse theorems (1912) and found the asymptotics of $E_n(|x|)$ (1914). Favard (1937) and Akhiezer and Krein (1937) found the sharp constants for classes of periodic functions with bounded derivatives, and Korneichuk (1962) the sharp constant for the modulus of continuity. Nikolskii, Timan (1951) and Dzyadyk gave the pointwise refinements on an interval, and Ditzian and Totik (1987) the moduli that make the algebraic theory two-sided. Varga and Carpenter (1985) computed Bernstein's constant to 50 digits and disproved his conjecture that $\beta = 1/(2\sqrt\pi)$.

## References
