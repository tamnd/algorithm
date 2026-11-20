---
tag: 7E2NVC
kind: theorem
slug: bramble-hilbert-lemma
name: Bramble-Hilbert lemma
area: scientific-computing/finite-element-practice
level: advanced
summary: Bounds the error of polynomial approximation on a domain by a seminorm of the function, which with scaling gives h^k interpolation error estimates.
prereqs: [cea-lemma, sobolev-space, ciarlet-finite-element]
see_also: [lagrange-finite-element, isoparametric-mapping, finite-element-method, polynomial-interpolation, hp-finite-element-method, adaptive-finite-element-method, residual-error-estimator]
sources:
  - paper: doi:10.1137/0707006
    title: J. H. Bramble and S. R. Hilbert, Estimation of linear functionals on Sobolev spaces with application to Fourier transforms and spline interpolation, SIAM Journal on Numerical Analysis 7(1) (1970) 112-124
  - paper: doi:10.1090/S0025-5718-1980-0559195-7
    title: Todd Dupont and Ridgway Scott, Polynomial approximation of functions in Sobolev spaces, Mathematics of Computation 34(150) (1980) 441-463
    locator: averaged Taylor polynomials on domains star-shaped with respect to a ball
  - book: isbn:9780387759333
    title: Susanne C. Brenner and L. Ridgway Scott, The Mathematical Theory of Finite Element Methods, third edition, Springer, 2008
    locator: Chapter 4 (averaged Taylor polynomials, the Bramble-Hilbert lemma as Lemma 4.3.8, local and global interpolation estimates)
  - book: isbn:9780387205748
    title: Alexandre Ern and Jean-Luc Guermond, Theory and Practice of Finite Elements, Applied Mathematical Sciences 159, Springer, 2004
    locator: Chapter 1 (finite element interpolation)
---

The Bramble-Hilbert lemma says that a function in $H^{k+1}$ can be approximated by a polynomial of degree $k$ with an error bounded by its seminorm $|u|_{k+1}$ alone. In the equivalent functional form, a bounded linear functional on $H^{k+1}$ that vanishes on all polynomials of degree $k$ is bounded by $|u|_{k+1}$. Combined with scaling from a reference element, it gives the interpolation estimate $|u - I_h u|_m \le C h^{k+1-m}|u|_{k+1}$, which turns [Céa's lemma](/cea-lemma/) into the convergence rates of the [finite element method](/finite-element-method/).

## Statement

Let $\mathcal{P}_k$ be the polynomials of total degree at most $k$ in $d$ variables, and let $|\cdot|_m$ and $\|\cdot\|_m$ be the [Sobolev](/sobolev-space/) seminorm and norm of order $m$.

**Theorem (Bramble and Hilbert, 1970).** Let $\Omega \subset \mathbb{R}^d$ be a bounded connected domain with a Lipschitz boundary, for example a domain that is star-shaped with respect to a ball, and let $k \ge 0$. There is a constant $C = C(\Omega, k)$ such that:

1. *(Polynomial approximation.)* For every $u \in H^{k+1}(\Omega)$ there is $q \in \mathcal{P}_k$ with $\|u - q\|_{k+1} \le C|u|_{k+1}$.
2. *(Functionals.)* If $\ell$ is linear on $H^{k+1}(\Omega)$ with $|\ell(u)| \le C_\ell\|u\|_{k+1}$ and $\ell(q) = 0$ for all $q \in \mathcal{P}_k$, then $|\ell(u)| \le C\,C_\ell\,|u|_{k+1}$.
3. *(Scaling.)* If $\Omega_\delta = x_0 + \delta\Omega$ with $\delta > 0$, then for every $u \in H^{k+1}(\Omega_\delta)$ there is $q \in \mathcal{P}_k$ with $|u - q|_{m, \Omega_\delta} \le C\,\delta^{k+1-m}|u|_{k+1, \Omega_\delta}$ for $m = 0, \ldots, k+1$, with the same $C$.

**Corollary (interpolation estimate).** Let $\mathcal{T}_h$ be a shape regular family of simplicial meshes, with $h_K/\rho_K \le \sigma$ for every cell $K$, and let $I_h$ be the nodal interpolant into continuous piecewise polynomials of degree $k$ ([Lagrange elements](/lagrange-finite-element/)). If $k + 1 > d/2$, then for $m = 0, 1$ and $u \in H^{k+1}(\Omega)$,

$$|u - I_h u|_{m, K} \le C\,h_K^{k+1-m}|u|_{k+1, K}, \qquad |u - I_h u|_m \le C\,h^{k+1-m}|u|_{k+1},$$

with $C$ that depends only on $d$, $k$ and $\sigma$.

**Uniform form.** Brenner and Scott state the lemma for a domain that is star-shaped with respect to a ball $B$ of radius larger than half the largest such radius. There the polynomial is the averaged Taylor polynomial of Dupont and Scott, and the constant depends only on $d$, $k$ and the chunkiness parameter $\operatorname{diam}\Omega/\rho_{\max}$. The scaling argument below reaches the same estimate for meshes through a fixed reference cell.

## In plain words

A smooth function looks almost like a polynomial when you zoom in on a small piece of it. This lemma makes that exact. It says how far a function is from the nearest polynomial of a given degree, and it measures the distance only by the next higher derivatives of the function, the ones that a polynomial of that degree cannot have. Any measurement that ignores polynomials of that degree is therefore controlled by those higher derivatives. When the piece of the domain gets smaller, the bound gets smaller by a fixed power of its size. On a finite element mesh this gives the rate at which the error falls as the cells get smaller, provided the cells do not become too thin.

## Proof

The full proof is in [the proof file](proofs/main.md). In outline:

1. **A norm equivalence.** On $H^{k+1}(\Omega)$ the quantity $|u|_{k+1} + \sum_{|\alpha| \le k}\bigl|\int_\Omega D^\alpha u\bigr|$ is a norm equivalent to $\|u\|_{k+1}$. The proof is by contradiction with the Rellich compactness theorem. A limit with zero seminorm is a polynomial of degree $k$, because $\Omega$ is connected, and zero moments then force it to be zero.
2. **The polynomial.** Choose $q \in \mathcal{P}_k$ with $\int_\Omega D^\alpha(u - q) = 0$ for all $|\alpha| \le k$. The equivalence applied to $u - q$ gives part 1, since $|u - q|_{k+1} = |u|_{k+1}$.
3. **Functionals.** $|\ell(u)| = |\ell(u - q)| \le C_\ell\|u - q\|_{k+1}$.
4. **Scaling.** Under $x = x_0 + \delta\hat x$ the seminorm $|\cdot|_m$ scales by $\delta^{d/2 - m}$. Applying part 1 on $\Omega$ and changing variables gives the factor $\delta^{k+1-m}$.
5. **Interpolation.** On the reference cell, $\hat u - \hat I\hat u = (\mathrm{id} - \hat I)(\hat u - \hat q)$ because $\hat I$ reproduces $\mathcal{P}_k$, and $\hat I$ is bounded on $H^{k+1}$ because $k+1 > d/2$. The affine map $F_K(\hat x) = B_K\hat x + b_K$ with $\|B_K\| \le h_K/\hat\rho$ and $\|B_K^{-1}\| \le \hat h/\rho_K$ carries the bound to $K$, and shape regularity turns $h_K^{k+1}/\rho_K^m$ into $C h_K^{k+1-m}$.

## Consequences

**A one-dimensional check.** On $K = [0, h]$ with $k = 1$ and $u = x^2$, the linear interpolant is $I u = hx$ and the error is $e = x^2 - hx$. Then $|e|_1^2 = \int_0^h (2x - h)^2\,dx = h^3/3$, $\|e\|_0^2 = \int_0^h x^2(x-h)^2\,dx = h^5/30$ and $|u|_2^2 = 4h$. So

$$\frac{|e|_1}{|u|_2} = \frac{h}{2\sqrt3}, \qquad \frac{\|e\|_0}{|u|_2} = \frac{h^2}{\sqrt{120}},$$

which are the powers $h^{k+1-m}$ for $m = 1$ and $m = 0$.

**A quadrature error.** The trapezoidal rule error $\ell(u) = \int_0^1 u\,dx - \tfrac12\bigl(u(0) + u(1)\bigr)$ vanishes on $\mathcal{P}_1$ and is bounded on $H^2(0,1)$, so the lemma gives $|\ell(u)| \le C|u|_2$. Here the constant is explicit: integration by parts twice gives $\ell(u) = -\tfrac12\int_0^1 x(1-x)u''(x)\,dx$, so $|\ell(u)| \le \tfrac12\|x(1-x)\|_0\,|u|_2 = |u|_2/(2\sqrt{30}) \approx 0.0913\,|u|_2$. For $u = x^2$ the error is $\tfrac13 - \tfrac12 = -\tfrac16$ and the bound is $0.1826$. The same argument on a cell of size $h$ is the standard proof that quadrature errors are of high order.

**Finite element rates.** With Céa's lemma the corollary gives $\|u - u_h\|_1 \le C h^k|u|_{k+1}$ for degree $k$ elements. The Aubin-Nitsche duality argument then gives $\|u - u_h\|_0 \le C h^{k+1}|u|_{k+1}$ when the problem has full elliptic regularity.

**Local estimates for adaptivity.** The element-wise bound $|u - I_h u|_{1,K} \le C h_K^k|u|_{2,K}$ (for $k = 1$) is local, so small cells pay off where $u$ has large derivatives. This is the basis of graded meshes near corners and of [adaptive refinement](/adaptive-finite-element-method/).

**Other interpolants.** The same proof works for every interpolant that reproduces $\mathcal{P}_k$ and is bounded on the reference cell. This covers Hermite elements, the Clément and Scott-Zhang quasi-interpolants for $u \in H^1$ only, and [isoparametric](/isoparametric-mapping/) cells close to affine ones.

## Tightness

**The power of $h$ cannot be higher.** For $u = x_1^{k+1}$ the interpolation error on a cell of size $h$ is a nonzero polynomial of degree $k+1$ that vanishes at the nodes, and its $m$-th seminorm is exactly of size $h^{k+1-m}$ times $|u|_{k+1, K}$, as the one-dimensional check shows for $k = 1$.

**Connectedness is needed.** On $\Omega = (0, 1) \cup (2, 3)$ the function equal to $0$ on the first interval and $1$ on the second has $|u|_1 = 0$. But $\|u - c\|_0^2 = c^2 + (1 - c)^2 \ge \tfrac12$ for every constant $c$, so part 1 fails with $k = 0$.

**The shape of the cell matters.** Take the triangle with vertices $(0,0)$, $(h,0)$ and $(h/2, \varepsilon)$ and $u = x^2$. The linear interpolant is $hx - \tfrac{h^2}{4\varepsilon}y$, so $\partial_y(u - I u) = \tfrac{h^2}{4\varepsilon}$ on the whole triangle, while $|u|_{2,K} = 2\sqrt{|K|}$. The ratio $|u - Iu|_{1,K}/|u|_{2,K} \ge h^2/(8\varepsilon)$ is unbounded as $\varepsilon \to 0$. The maximum angle tends to $\pi$ here. Babuška and Aziz showed in 1976 that a bound on the maximum angle away from $\pi$ is enough for the $H^1$ estimate, so shape regularity is sufficient but not necessary.

**Point values need smoothness.** For $k + 1 \le d/2$, for example $k = 0$ in 2D, the nodal interpolant is not defined on $H^{k+1}$, because such functions need not be continuous. The Clément or Scott-Zhang operators replace it.

## History

James Bramble and Stephen Hilbert published the lemma in 1970 in the form for linear functionals, with applications to spline interpolation. A norm equivalence of the same kind appears earlier in the work of Jacques Deny and Jacques-Louis Lions on Beppo Levi spaces, and some books call it the Deny-Lions lemma. Philippe Ciarlet and Pierre-Arnaud Raviart built the affine-equivalence and scaling argument for finite element interpolation around 1972. Todd Dupont and Ridgway Scott gave a constructive proof in 1980 with averaged Taylor polynomials, which shows how the constant depends on the shape of the domain.

## References
