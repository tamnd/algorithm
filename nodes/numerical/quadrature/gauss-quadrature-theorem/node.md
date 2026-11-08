---
tag: 48ZFB6
kind: theorem
slug: gauss-quadrature-theorem
name: Gaussian quadrature exactness theorem
aliases:
- Gauss degree 2n-1 theorem
- Gauss-Christoffel quadrature theorem
- fundamental theorem of Gaussian quadrature
area: numerical/quadrature
level: advanced
summary: An n-point interpolatory rule with nodes at the roots of an orthogonal polynomial is exact to degree 2n-1, and no n-point rule does better.
prereqs: [degree-of-precision, orthogonal-polynomials, interpolatory-quadrature]
see_also: [gaussian-quadrature, gauss-legendre-quadrature, golub-welsch-algorithm, gauss-radau-quadrature, gauss-lobatto-quadrature, legendre-polynomials, hermite-interpolation, gauss-kronrod-quadrature]
sources:
  - book: isbn:9780198506720
    title: Walter Gautschi, Orthogonal Polynomials, Computation and Approximation, Oxford University Press, 2004
    locator: Chapter 1, Section 1.4 (Gauss-type quadrature rules, their exactness, the positivity of the weights and the error term)
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 2, the section on integration rules of Gauss type (Section 2.7)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 10, Numerical integration II (the construction of Gauss quadrature, its exactness and its error)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Section 5.3, Gaussian numerical integration (the theorem on the error of Gaussian quadrature); Chapter 3 for Hermite interpolation and divided differences
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 19, Clenshaw-Curtis and Gauss quadrature (the error bound for functions analytic in a Bernstein ellipse); Chapter 8 for the bound on Chebyshev coefficients
  - paper: "Carl Friedrich Gauss, Methodus nova integralium valores per approximationem inveniendi, Commentationes Societatis Regiae Scientiarum Gottingensis Recentiores 3 (1814)"
    locator: the n-point rules of maximal degree for the weight 1 on a finite interval
  - paper: "Carl Gustav Jacob Jacobi, Ueber Gauss' neue Methode, die Werthe der Integrale näherungsweise zu finden, Journal für die reine und angewandte Mathematik 1 (1826) 301-308"
    locator: the proof by orthogonality and the Legendre polynomials
  - paper: "Elwin Bruno Christoffel, Über die Gaußische Quadratur und eine Verallgemeinerung derselben, Journal für die reine und angewandte Mathematik 55 (1858) 61-82"
    locator: the extension to general weight functions
---

The Gauss quadrature theorem says that for a positive weight function $w$, the $n$-node rule whose nodes are the zeros of the degree-$n$ [orthogonal polynomial](/orthogonal-polynomials/) of $w$, and whose weights are the integrals of the Lagrange basis polynomials, integrates every polynomial of degree at most $2n - 1$ exactly. No rule with $n$ nodes reaches degree $2n$, and this rule is the only one with degree $2n - 1$. Its weights are positive, and its error on a smooth $f$ is a multiple of $f^{(2n)}$. The theorem is the base of [Gaussian quadrature](/gaussian-quadrature/) and of its special cases such as [Gauss-Legendre quadrature](/gauss-legendre-quadrature/).

## Statement

**Notation.** As on all quadrature pages: $I(f) = \int_a^b f(x)\,w(x)\,dx$, a rule $Q_n(f) = \sum_{i=1}^n w_i f(x_i)$ with $n$ nodes, $E_n(f) = I(f) - Q_n(f)$, and $d$ the [degree of precision](/degree-of-precision/). On this page the Gauss weights are written $\lambda_i$ to keep them apart from the weight function $w$. $\mathcal{P}_k$ is the set of real polynomials of degree at most $k$.

**Hypotheses.** $-\infty \le a < b \le \infty$. The weight $w$ is measurable on $(a, b)$, $w \ge 0$, $w > 0$ on a set of positive measure, and all moments $\int_a^b |x|^k w(x)\,dx$, $k \ge 0$, are finite. Let $\langle f, g \rangle = \int_a^b f g\, w$, and let $p_n$ be the monic polynomial of degree $n \ge 1$ with $\langle p_n, q \rangle = 0$ for all $q \in \mathcal{P}_{n-1}$.

**Theorem.**

1. $p_n$ exists and is unique, and its $n$ zeros $x_1 < \cdots < x_n$ are real, simple and lie in $(a, b)$.
2. With $\ell_i(x) = \prod_{j \ne i} \frac{x - x_j}{x_i - x_j}$ and $\lambda_i = \int_a^b \ell_i\, w$, the rule $Q_n(f) = \sum_i \lambda_i f(x_i)$ satisfies $Q_n(p) = I(p)$ for every $p \in \mathcal{P}_{2n-1}$.
3. $\lambda_i = \int_a^b \ell_i^2\, w > 0$ for each $i$, and $\sum_i \lambda_i = \int_a^b w$.
4. For any $n$ distinct nodes and any weights, some $p \in \mathcal{P}_{2n}$ has $Q(p) \ne I(p)$. So $d \le 2n - 1$ for every $n$-node rule.
5. If an $n$-node rule with distinct nodes is exact on $\mathcal{P}_{2n-1}$, its nodes are $x_1, \ldots, x_n$ and its weights are $\lambda_1, \ldots, \lambda_n$.
6. If $[a, b]$ is finite and $f \in C^{2n}[a, b]$, then for some $\xi \in [a, b]$,
$$E_n(f) = \frac{f^{(2n)}(\xi)}{(2n)!} \int_a^b p_n(x)^2\, w(x)\,dx.$$

## In plain words

A rule that samples a function at a few points and adds the samples with weights can be exact for all polynomials up to some degree. If you fix the sample points, you can choose the weights so that the rule is exact up to one less than the number of points. Gauss saw that you can do twice as well if you may also move the points. The best points are the roots of one special polynomial, the one that is "perpendicular" to all polynomials of lower degree under the integral. With those points, the rule is exact up to almost twice the number of points, and no other choice of points does as well. The weights come out positive, which makes the rule stable on a computer.

## Proof

The proof has seven short steps; it is given in full in [the proof](proofs/main.md). The two key steps are these.

*Zeros (part 1).* Let $z_1, \ldots, z_k$ be the points of $(a, b)$ where $p_n$ changes sign. If $k < n$, then $q = \prod_j (x - z_j) \in \mathcal{P}_{n-1}$ and $p_n q$ does not change sign on $(a, b)$, so $\langle p_n, q \rangle \ne 0$ because $w > 0$ on a set of positive measure. This contradicts orthogonality. So $k = n$.

*Exactness (part 2).* For $f \in \mathcal{P}_{2n-1}$, divide by $p_n$: $f = q p_n + r$ with $q, r \in \mathcal{P}_{n-1}$. Then $I(f) = \langle q, p_n \rangle + I(r) = I(r)$, and $Q_n(f) = Q_n(r)$ because $p_n(x_i) = 0$. The rule is interpolatory, so $Q_n(r) = I(r)$.

Part 3 applies part 2 to $\ell_i^2 \in \mathcal{P}_{2n-2}$. Part 4 uses $p = \prod_i (x - y_i)^2$, for which $Q(p) = 0 < I(p)$. Part 5 shows that the node polynomial of an exact rule is orthogonal to $\mathcal{P}_{n-1}$, hence equal to $p_n$. Part 6 integrates the error of the Hermite interpolant of $f$ at the doubled nodes, $f - h = f[x_1, x_1, \ldots, x_n, x_n, x]\, p_n^2$, and applies the mean value theorem for integrals, which is allowed because $p_n^2 w \ge 0$. $\blacksquare$

## Consequences

- **[Gaussian quadrature](/gaussian-quadrature/)** for each classical weight: [Gauss-Legendre](/gauss-legendre-quadrature/) ($w = 1$), [Gauss-Jacobi](/gauss-jacobi-quadrature/), [Gauss-Laguerre](/gauss-laguerre-quadrature/) and [Gauss-Hermite](/gauss-hermite-quadrature/). For $w = 1$ on $[-1, 1]$, $p_n$ is the monic [Legendre polynomial](/legendre-polynomials/), $\langle p_n, p_n \rangle = \frac{2^{2n+1}(n!)^4}{(2n+1)((2n)!)^2}$, and part 6 reads $E_n(f) = \frac{2^{2n+1}(n!)^4}{(2n+1)((2n)!)^3} f^{(2n)}(\xi)$; for $n = 2$ the constant is $\frac{1}{135}$.
- **Computation.** Part 1 and the three-term recurrence of $p_n$ make the nodes the eigenvalues of a symmetric tridiagonal matrix, and part 3 makes the weights the squared first components of its eigenvectors times $\int w$: the [Golub-Welsch algorithm](/golub-welsch-algorithm/). See [computing Gaussian nodes and weights](/gauss-nodes-and-weights/).
- **Convergence for every continuous $f$.** On a finite interval, part 3 gives $\sum_i |\lambda_i| = \int w$ for every $n$, and part 2 gives $d_n = 2n - 1 \to \infty$. By the convergence theorem on the [degree of precision](/degree-of-precision/) page, $Q_n(f) \to I(f)$ for every $f \in C[a, b]$. The rule is also stable: an error $\delta$ in each value $f(x_i)$ changes $Q_n(f)$ by at most $\delta \int w$.
- **Geometric convergence for analytic $f$.** Let $w = 1$ on $[-1, 1]$, $n \ge 2$, and let $f$ be analytic in the open Bernstein ellipse $E_\rho$ (foci $\pm 1$, semi-axes summing to $\rho > 1$) with $|f| \le M$ there. Then
$$|E_n(f)| \le \frac{64}{15}\,\frac{M \rho^{2 - 2n}}{\rho^2 - 1}.$$
*Proof.* The Chebyshev series $f = \sum_k a_k T_k$ converges uniformly on $[-1, 1]$ and $|a_k| \le 2M\rho^{-k}$ (Trefethen, Chapter 8). $E_n$ is a bounded linear functional on $C[-1, 1]$, so $E_n(f) = \sum_k a_k E_n(T_k)$. By part 2, $E_n(T_k) = 0$ for $k \le 2n - 1$. For odd $k$, $I(T_k) = 0$, and $Q_n(T_k) = 0$ because the nodes and weights are symmetric about $0$. For even $k \ge 2n \ge 4$, $|I(T_k)| = \frac{2}{k^2 - 1} \le \frac{2}{15}$ and $|Q_n(T_k)| \le \sum_i \lambda_i = 2$. So $|E_n(f)| \le \sum_{k \text{ even} \ge 2n} 2M\rho^{-k}(2 + \tfrac{2}{15}) = \frac{64}{15} M \frac{\rho^{-2n}}{1 - \rho^{-2}}$. $\square$ This is the bound of Trefethen, Chapter 19, written for $n$ nodes; the rate $\rho^{-2n}$ is twice the rate of interpolation in the same $n$ points.
- **Variants with fixed nodes.** Fixing one or two endpoints as nodes and applying the same argument to the remaining free nodes gives [Gauss-Radau](/gauss-radau-quadrature/) (degree $2n - 2$) and [Gauss-Lobatto](/gauss-lobatto-quadrature/) (degree $2n - 3$). Adding $n + 1$ nodes to a Gauss rule in the same way gives [Gauss-Kronrod](/gauss-kronrod-quadrature/) rules.

## Tightness

Part 4 shows that $2n - 1$ cannot be raised, and part 6 shows that the error formula is sharp. For $f = p_n^2$, of degree $2n$, the rule gives $Q_n(f) = 0$ and $f^{(2n)} = (2n)!$, so part 6 holds with equality: $E_n(p_n^2) = \langle p_n, p_n \rangle$. For $n = 2$ and $w = 1$ on $[-1, 1]$: $p_2 = x^2 - \tfrac13$, the nodes are $\pm 1/\sqrt{3}$ with weights $1$, $Q_2(x^4) = \tfrac29$, $I(x^4) = \tfrac25$, and $E_2(x^4) = \tfrac{8}{45} = \langle p_2, p_2 \rangle$.

The positivity of $w$ is needed. For a weight that changes sign, $p_n$ may fail to exist or may have complex or repeated zeros, and the weights can be negative.

## History

Gauss found the $n$-point rules of maximal degree for $w = 1$ in 1814, by a route through continued fractions and the hypergeometric series. Jacobi gave the proof by orthogonality in 1826, with the nodes as the zeros of the Legendre polynomial. Christoffel extended the theorem to general weight functions in 1858, and the weights $\lambda_i$ are often called Christoffel numbers. Gautschi's book traces the later development and the computational methods.

## References
