---
tag: BZE2V0
kind: theorem
slug: curry-schoenberg-theorem
name: Curry-Schoenberg theorem
aliases:
- B-spline basis theorem
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: The n + 1 B-splines of degree p on a knot vector form a basis of the splines of degree p on the domain [t_p, t_(n+1)] with the smoothness that the knot multiplicities allow.
prereqs: [b-spline, knot-vector, linear-independence]
see_also: [spline, schoenberg-whitney-theorem, partition-of-unity, knot-refinement, cox-de-boor-recursion, polynomial, cubic-spline-interpolation, approximation-theory]
sources:
  - paper: doi:10.1007/BF02788653
    title: Haskell B. Curry and Isaac J. Schoenberg, On Pólya frequency functions IV, the fundamental spline functions and their limits, Journal d'Analyse Mathématique 17 (1966), 71 to 107
    locator: the fundamental spline functions (B-splines) of a knot sequence and their use as a basis of the spline space
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter VIII, The spaces of piecewise polynomials and the truncated power basis; Chapter IX, The representation of piecewise polynomial functions by B-splines (Marsden's identity and the Curry and Schoenberg theorem)
  - paper: doi:10.1016/0021-9045(70)90058-4
    title: Martin J. Marsden, An identity for spline functions with applications to variation-diminishing spline approximation, Journal of Approximation Theory 3 (1970), 7 to 49
    locator: the identity that writes the powers (y - x)^p as B-spline series
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 2.2, Definition and properties of B-spline basis functions (the basis functions and the continuity at a knot of multiplicity k)
  - paper: "I. J. Schoenberg, Contributions to the problem of approximation of equidistant data by analytic functions, Quarterly of Applied Mathematics 4 (1946), Part A 45 to 99 and Part B 112 to 141"
    locator: Part A, the spline functions with equally spaced knots and the basic spline curves
---

The Curry-Schoenberg theorem says that the [B-splines](/b-spline/) of a [knot vector](/knot-vector/) are a basis of the [spline](/spline/) space that the knots describe. Every piecewise polynomial of degree $p$ on the domain, with the smoothness at each knot that its multiplicity allows, is a combination $\sum_i c_i N_{i,p}$ in exactly one way. The theorem has two parts: a count, the dimension of the spline space is $p + 1$ plus the number of interior knots, and a spanning result, which comes from Marsden's identity. Because the count equals the number of B-splines, the B-splines are linearly independent. This is the reason that a spline can be stored as its knots and its coefficients, and the reason that a B-spline curve with free control points is the general spline curve.

## Statement

Let $p \ge 0$, $n \ge p$ and $t_0 \le t_1 \le \cdots \le t_{n+p+1}$, and let $N_{0,p}, \ldots, N_{n,p}$ be the B-splines of degree $p$ from the [Cox-de Boor recursion](/cox-de-boor-recursion/), with half-open spans. Put $a = t_p$ and $b = t_{n+1}$, and suppose

1. $t_p < t_{p+1}$ and $t_n < t_{n+1}$, so that no interior knot is at $a$ or $b$;
2. every value occurs at most $p + 1$ times among $t_{p+1}, \ldots, t_n$.

Let $\xi_1 < \cdots < \xi_l$ be the distinct values of $t_{p+1}, \ldots, t_n$, with multiplicities $m_1, \ldots, m_l$, so that $m_1 + \cdots + m_l = n - p$. Let $S$ be the set of functions $s$ on $[a, b]$ such that $s$ is a [polynomial](/polynomial/) of degree at most $p$ on each of $[a, \xi_1), [\xi_1, \xi_2), \ldots, [\xi_l, b]$, and the two pieces that meet at $\xi_j$ have equal derivatives of the orders $0, 1, \ldots, p - m_j$ there. A knot with $m_j = p + 1$ gives no condition, and $s$ is continuous from the right there.

**Theorem.** (a) $\dim S = p + 1 + \sum_{j=1}^{l} m_j = n + 1$. (b) The restrictions of $N_{0,p}, \ldots, N_{n,p}$ to $[a, b]$, with the closing rule at $b$, are a basis of $S$.

The knots $t_0, \ldots, t_{p-1}$ below $a$ and $t_{n+2}, \ldots, t_{n+p+1}$ above $b$ are free. They change the basis, but not the space.

## In plain words

Fix a degree and a list of knots. The splines on these knots are all the piecewise polynomials that join at each knot as smoothly as the knot allows: a single knot asks for many matching derivatives, and a repeated knot asks for fewer. The theorem says two things. You can build every such spline from the B-splines of the knots. And no B-spline is wasted: each spline has exactly one set of coefficients. So the number of B-splines, which you can read off from the length of the knot list, is the number of free parameters of the spline space. This is why a designer can move control points freely and always gets a spline of the right kind, and why a spline can be stored as knots and coefficients.

## Proof

The full proof is in [the proof of the Curry-Schoenberg theorem](proofs/main.md). It has three steps.

- **The dimension.** The functions $1, x, \ldots, x^p$ and the truncated powers $(x - \xi_j)_+^k$ for $p - m_j + 1 \le k \le p$ are a basis of $S$. On $[a, \xi_1)$ a spline is a polynomial; at each $\xi_j$ the difference of the two pieces is a polynomial whose derivatives of orders up to $p - m_j$ vanish at $\xi_j$, so it is a combination of $(x - \xi_j)^k$ with $k > p - m_j$. Peeling off the pieces from left to right gives the spanning, and evaluating on the pieces from left to right gives the independence. The count is $(p + 1) + \sum_j m_j$. The knots $t_0, \ldots, t_p$ are at most $a$ and $t_{n+1}, \ldots, t_{n+p+1}$ are at least $b$, so by condition 1 the interior knots are exactly $t_{p+1}, \ldots, t_n$, and the count is $n + 1$.
- **Marsden's identity.** For $a \le x \le b$ and every real $y$,
$$(y - x)^p = \sum_{i=0}^{n} \psi_i(y) \, N_{i,p}(x), \qquad \psi_i(y) = (y - t_{i+1})(y - t_{i+2}) \cdots (y - t_{i+p}).$$
The proof is by induction on the degree: one step of the recursion turns the sum of degree $q$ into $(y - x)$ times the sum of degree $q - 1$, because $(1 - \alpha)(y - t_i) + \alpha (y - t_{i+q}) = y - x$ for the weight $\alpha = (x - t_i)/(t_{i+q} - t_i)$ of the recursion.
- **Spanning.** Differentiate Marsden's identity $p - k$ times in $y$ and set $y = \xi$. This gives $(x - \xi)^k$ as a B-spline series for $0 \le k \le p$, and so every polynomial. If $\xi = \xi_j$ starts at the index $r$, that is $t_{r-1} < t_r = \xi$, and $k > p - m_j$, the same series with only the terms $i \ge r$ is $(x - \xi)_+^k$: for $x < \xi$ these terms vanish, and the terms $i < r$ that can be nonzero to the right of $\xi$ have all $m_j$ copies of $\xi$ among $t_{i+1}, \ldots, t_{i+p}$, so $\psi_i^{(p-k)}(\xi) = 0$. So the span of the B-splines contains the basis of the first step.

Then $S \subseteq \operatorname{span}\{N_{i,p}\}$ and $\dim S = n + 1$, so the $n + 1$ functions span a space of dimension at least $n + 1$. They are therefore [linearly independent](/linear-independence/), and their span is $S$. The proof does not need the smoothness of the B-splines at the knots: it is a consequence.

## Consequences

- **The B-form.** Every $s \in S$ has unique coefficients $c_i$ with $s = \sum_i c_i N_{i,p}$ on $[a, b]$. For a curve the coefficients are the control points. A [spline](/spline/) given piece by piece, in the pp-form of de Boor, has a B-form, and the conversion is a linear map with a unique result.
- **Polynomials.** Marsden's identity with $y$ expanded gives the coefficients of each power. For $k = 0$ they are all $1$, which is the [partition of unity](/partition-of-unity/) on the domain. For $k = 1$ they are the Greville abscissae $(t_{i+1} + \cdots + t_{i+p})/p$, so $x = \sum_i t_i^* N_{i,p}(x)$. For $p = 2$ the coefficients of $x^2$ are $t_{i+1} t_{i+2}$.
- **Local independence.** On a nonempty span $[t_\mu, t_{\mu+1})$, the $p + 1$ functions $N_{\mu-p,p}, \ldots, N_{\mu,p}$ restricted to the span are a basis of the polynomials of degree at most $p$: they span them, by Marsden's identity, and there are $p + 1$ of them.
- **Refinement.** If $\tau$ is a knot vector and $t$ contains every knot of $\tau$, with the same end conditions, then every spline on $\tau$ satisfies the weaker smoothness conditions of $t$. So it has a B-form on $t$, and the coefficients are unique. This is why [knot refinement](/knot-refinement/) always has exactly one answer.
- **Interpolation needs the right count.** An interpolation problem in $S$ has $n + 1$ unknowns, so it needs $n + 1$ conditions. The [Schoenberg-Whitney theorem](/schoenberg-whitney-theorem/) says which $n + 1$ sites give a nonsingular system, and [cubic spline interpolation](/cubic-spline-interpolation/) uses this count to add end conditions.

**Example.** Take $p = 2$ and $t = (0, 0, 0, 1, 1, 2, 3, 3, 3)$, so $n = 5$, $a = 0$, $b = 3$, $\xi_1 = 1$ with $m_1 = 2$ and $\xi_2 = 2$ with $m_2 = 1$. The space $S$ has the quadratics on $[0, 1)$, $[1, 2)$ and $[2, 3]$ that are continuous at $1$ and $C^1$ at $2$, and $\dim S = 3 + 2 + 1 = 6$, the number of B-splines. The truncated power basis is $1, x, x^2, (x - 1)_+, (x - 1)_+^2, (x - 2)_+^2$, and the proof gives its B-forms:

| Function | $c_0$ | $c_1$ | $c_2$ | $c_3$ | $c_4$ | $c_5$ |
|---|---|---|---|---|---|---|
| $1$ | $1$ | $1$ | $1$ | $1$ | $1$ | $1$ |
| $x$ | $0$ | $1/2$ | $1$ | $3/2$ | $5/2$ | $3$ |
| $x^2$ | $0$ | $0$ | $1$ | $2$ | $6$ | $9$ |
| $(x - 1)_+$ | $0$ | $0$ | $0$ | $1/2$ | $3/2$ | $2$ |
| $(x - 1)_+^2$ | $0$ | $0$ | $0$ | $0$ | $2$ | $4$ |
| $(x - 2)_+^2$ | $0$ | $0$ | $0$ | $0$ | $0$ | $1$ |

The row of $x$ is the Greville abscissae, and the row of $x^2$ is the products $t_{i+1} t_{i+2}$. The function $(x - 1)_+$ has a kink at the double knot $1$ and is still in $S$, but $(x - 2)_+$ is not, because the single knot $2$ asks for a continuous first derivative. Each row was checked exactly against the B-spline values at the parameters $k/7$ in $[0, 3)$.

## Tightness

Each condition of the statement is needed.

- **A knot of multiplicity $p + 2$.** If $t_i = t_{i+p+1}$, then $N_{i,p} \equiv 0$ and the B-splines are dependent. For $p = 1$ and $t = (0, 0, 1, 1, 1, 2, 2)$ there are five B-splines, $N_{2,1}$ on the knots $1, 1, 1$ is zero, and the space of piecewise linear functions on $[0, 1)$ and $[1, 2]$ with a free jump at $1$ has dimension $4$.
- **An interior knot at an end of the domain.** If $t_p = t_{p+1}$, then $N_{0,p}$ has the support $[t_0, t_{p+1}) = [t_0, t_p)$, which is outside the domain, and it is zero on $[a, b]$. For $p = 2$ and $t = (0, 0, 0, 0, 1, 2, 2, 2)$ there are five B-splines, $N_{0,2} \equiv 0$ on $[0, 2]$, and $\dim S = 3 + 1 = 4$. The same happens at the right end if $t_n = t_{n+1}$. The statement in the form "$\dim S = n + 1$" is false without condition 1.
- **Outside the domain.** On all of $[t_0, t_{n+p+1})$ the B-splines are still independent, but they do not span the splines there. For the uniform knots $0, 1, \ldots, 6$ and $p = 2$, only $N_{0,2}(x) = x^2/2$ is nonzero on $[0, 1)$, so the constant $1$ is not a B-spline series on $[0, 1)$. The partition of unity fails there for the same reason.
- **The right end.** Without the closing rule, every B-spline of a clamped knot vector is $0$ at $b$, and the restrictions to the closed interval $[a, b]$ do not contain the constant $1$.

## History

Schoenberg introduced spline functions with equally spaced knots in 1946, together with the basic spline curves that are now the uniform B-splines. Curry and Schoenberg defined the B-spline of an arbitrary knot sequence as a divided difference of truncated powers and showed that these functions are a basis of the spline space, in the paper "On Pólya frequency functions IV" (1966). Marsden published his identity in 1970, as a tool for Schoenberg's variation-diminishing approximation, and de Boor's A Practical Guide to Splines gives the identity and the theorem, under the name Curry and Schoenberg theorem, in its Chapter IX. The recurrence of Cox and de Boor (1972) made the basis practical to compute.

## References
