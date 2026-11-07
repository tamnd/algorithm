---
tag: 0QX1QC
kind: algorithm
slug: kovacic-algorithm
name: Kovacic's algorithm
aliases:
- Kovacic's method
- Kovacic algorithm
- algorithm for Liouvillian solutions of second-order ODEs
area: algebra/computer-algebra
level: research
summary: Decides and solves second-order linear ODEs with rational coefficients in closed form.
solves: [closed-form-ode-solving]
model: blum-shub-smale-machine
complexity:
  vars: {k: the number of finite poles of r, T: the degree of the denominator t, D: the largest degree bound d met in a family}
  time: {worst: O(13^(k+1) (D + T)^3)}
  space: {extra: O((D + T)^2)}
properties: {deterministic: true, recursive: false, in_place: false, online: false}
history:
  year: 1986
  people: [Jerald J. Kovacic]
  note: Kovacic found the algorithm in the late 1970s and published it in 1986; Saunders implemented it in 1981, and Ulmer and Weil simplified case 3 in 1996.
prereqs: [differential-galois-theory, liouville-theorem, partial-fraction-decomposition, gaussian-elimination]
see_also: [risch-algorithm, symbolic-integration, holonomic-function, ore-algebra, petkovsek-hyper-algorithm, finite-group, closed-form-ode-solving]
sources:
  - paper: "Jerald J. Kovacic, An algorithm for solving second order linear homogeneous differential equations, Journal of Symbolic Computation 2(1), 1986"
    locator: the four possible Galois groups, the necessary conditions on the orders of the poles, and the algorithm for cases 1, 2 and 3 with its proof
  - paper: "B. David Saunders, An implementation of Kovacic's algorithm for solving second order linear homogeneous differential equations, SYMSAC 1981"
    locator: the first implementation, in MACSYMA
  - book: isbn:9783540442288
    title: Marius van der Put and Michael F. Singer, Galois Theory of Linear Differential Equations, Springer, 2003
    locator: Chapter 4, the algebraic subgroups of SL2 and the algorithm for Liouvillian solutions of order 2 equations
  - paper: "Felix Ulmer and Jacques-Arthur Weil, Note on Kovacic's algorithm, Journal of Symbolic Computation 22(2), 1996"
    locator: cases 2 and 3 recast through invariants and semi-invariants of the finite groups, with simplifications of the search
---

Kovacic's algorithm decides whether a linear differential equation $y'' = r\, y$ with $r \in \mathbb{Q}(x)$ has a Liouvillian solution, one built from rational functions by integrals, exponentials of integrals and algebraic functions, and finds one if it exists. Every equation $y'' + a y' + b y = 0$ with rational $a, b$ reduces to this form by $y = z\, e^{-\int a/2}$, with $r = a^2/4 + a'/2 - b$. The algorithm rests on the classification of the [differential Galois group](/differential-galois-theory/), an algebraic subgroup of $\mathrm{SL}_2$: it is reducible, imprimitive, finite primitive, or all of $\mathrm{SL}_2$. In the first three cases the logarithmic derivative $w = y'/y$ of some solution is algebraic over $\mathbb{Q}(x)$ of degree $n = 1$, $2$, or $4$, $6$ or $12$. The algorithm reads candidate exponents from the Laurent series of $r$ at its poles and at infinity, combines them into finitely many families, and for each family looks for a polynomial solution of an auxiliary linear equation. If no family succeeds, no Liouvillian solution exists.

## In plain words

Some second-order differential equations have solutions you can write down with exponentials, integrals and roots, and most do not. This algorithm tells them apart, and it writes the solution down when there is one. It uses a deep fact: only four kinds of symmetry are possible, and three of them force a solution of a simple shape. Near each point where the coefficient blows up, the solution must start in one of a few ways, found by a short series computation. Picking one start at each point gives finitely many guesses. Each guess leaves one polynomial to find, and that is a linear system. If some guess works, it gives the solution. If every guess fails, the equation has no closed-form solution of this kind.

## The problem

Notation: $K$ is a field of characteristic $0$, here $K = \mathbb{Q}$, and $K[x]$ and $K(x)$ are the polynomials and rational functions in one variable $x$, with derivation $d/dx$. Only one variable occurs, so no monomial order is needed, and for $p \in K[x]$, $\mathrm{LC}(p)$ is the leading coefficient and $\mathrm{LT}(p) = \mathrm{LM}(p) \cdot \mathrm{LC}(p)$ the leading term with leading monomial $\mathrm{LM}(p)$. The input is $r = s/t$ with $s, t \in K[x]$ coprime and $t$ monic. A pole $c$ of $r$ is a root of $t$, of order its multiplicity, and the order of $r$ at infinity is $o = \deg t - \deg s$. This implementation needs the poles in $K$; in general they lie in $\overline{K}$ and the algorithm runs over the splitting field of $t$. The output is either "no Liouvillian solution" or the case $n$ and a polynomial $F(w) = \sum_{i \le n} F_i w^i \in K(x)[w]$ of degree $n$ whose roots are logarithmic derivatives $w = y'/y$ of solutions. Then $y = e^{\int w}$ solves $y'' = r y$, since $y'' = (w' + w^2)\, y$, so $w$ solves the Riccati equation $w' + w^2 = r$.

## The algorithm

Cases 1, 2 and 3 each have a necessary condition on the pole orders. Case 1 needs every pole of order $1$ or even, and $o$ even or $o > 2$. Case 2 needs a pole of order $2$ or of odd order at least $3$. Case 3 needs every pole of order at most $2$ and $o \ge 2$. Case 4, the full group $\mathrm{SL}_2$, has no Liouvillian solution.

```pseudo id=main
KOVACIC(r = s/t)
L1  reduce s/t; find the poles c of r with their orders, and the order o of r at infinity
L2  for each case in (1, 2, 3) whose necessary condition holds do
L3      for each n allowed in the case (n = 1 in case 1, n = 2 in case 2, n in 4, 6, 12 in case 3) do
L4          at each pole and at infinity, list the local choices: exponents e, and in case 1 a square-root part [√r] with residue α
L5          for each family (one choice per point) whose degree d = (n/12)(e_∞ − Σ e_c), or α_∞ − Σ α_c in case 1, is a nonnegative integer do
L6              form ω = Σ ±[√r]_c + Σ α_c/(x − c) ± [√r]_∞ in case 1, or θ = (n/12) Σ e_c/(x − c) in cases 2 and 3
L7              search for a polynomial P of degree d solving the auxiliary linear equation of (ω or θ, n), by linear algebra over K
L8              if P exists then return (case, F) with F the degree-n polynomial built from P and ω or θ
L9  return "no Liouvillian solution"
```

The local data come from short Laurent expansions. In case 1, at a pole of order $1$, $[\sqrt r]_c = 0$ and $\alpha_c = 1$. At a pole of order $2$ with $r = b/(x - c)^2 + \cdots$, $[\sqrt r]_c = 0$ and $\alpha_c^{\pm} = \frac12 \pm \frac12 \sqrt{1 + 4b}$. At a pole of order $2v \ge 4$, $[\sqrt r]_c$ is the polar part of order at least $2$ of a square root of the Laurent series, $a/(x - c)^v + \cdots$, and $\alpha_c^{\pm} = \frac12 (\pm b/a + v)$ with $b$ the coefficient of $(x - c)^{-v-1}$ in $r - [\sqrt r]_c^2$. At infinity the same holds with $o$ in place of the pole order, $[\sqrt r]_\infty$ the polynomial part of a square root, and $\alpha_\infty^{\pm} = \frac12(\pm b/a - v)$ for $o = -2v$. The auxiliary equation of case 1 is $P'' + 2\omega P' + (\omega' + \omega^2 - r) P = 0$, and then $F = w - (\omega + P'/P)$. In case 2, $e_c = 4$ at a simple pole, $e_c \in \{2, 2 \pm 2\sqrt{1 + 4b}\} \cap \mathbb{Z}$ at a double pole and $e_c = m$ at a pole of odd order $m \ge 3$, and the auxiliary equation is the third-order equation $P''' + 3\theta P'' + (3\theta^2 + 3\theta' - 4r) P' + (\theta'' + 3\theta\theta' + \theta^3 - 4r\theta - 2r') P = 0$, with $d = \frac12 (e_\infty - \sum e_c)$. Case 3 uses $e_c \in \{6 + \frac{12k}{n}\sqrt{1 + 4b} : |k| \le n/2\} \cap \mathbb{Z}$, $e_c = 12$ at a simple pole, and a recursion $P_{i-1} = -S P_i' + ((n - i) S' - S\theta) P_i - (n - i)(i + 1) S^2 r P_{i+1}$ from $P_n = -P$, where $S = \prod_c (x - c)$, and asks for $P_{-1} = 0$.

## Example

Take $r = x^2 + 3$, so $y'' = (x^2 + 3)\, y$. There are no finite poles and $o = 0 - 2 = -2$, which is even, so case 1 applies. The square root of $r$ at infinity is $x + \frac{3}{2x} + \cdots$, so $[\sqrt r]_\infty = x$ with $a = 1$, $v = 1$ and $b = 3$.

| Step | Data |
| --- | --- |
| Poles and order at infinity | none, $o = -2$ |
| Necessary conditions | case 1 holds |
| Local data at infinity | $[\sqrt r]_\infty = x$, $\alpha_\infty^{\pm} = \frac12(\pm 3 - 1) \in \{1, -2\}$ |
| Family $(+x, 1)$ | $d = 1$, $\omega = x$ |
| Auxiliary equation | $P'' + 2xP' + (1 + x^2 - x^2 - 3)P = P'' + 2xP' - 2P = 0$ |
| Polynomial of degree 1 | $P = x$ |
| Output | $F = w - (x + 1/x)$ |
| Solution | $y = P\, e^{\int \omega} = x\, e^{x^2/2}$ |

Indeed $y' = (1 + x^2) e^{x^2/2}$ and $y'' = (x^3 + 3x) e^{x^2/2} = (x^2 + 3)\, y$. The family $(-x, -2)$ has $d = -2 - 0 < 0$ and is skipped. For $r = 1/x - \frac{3}{16 x^2}$, the double pole at $0$ has $b = -\frac{3}{16}$ and $o = 1$, so case 1 fails its condition and case 2 runs with $e_0 \in \{1, 2, 3\}$ and $e_\infty = 1$. Only $e_0 = 1$ gives an integer $d = 0$, $\theta = \frac{1}{2x}$, $P = 1$, and $F = w^2 - \frac{1}{2x} w + \frac{1/16 - x}{x^2}$, whose roots $w = \frac{1}{4x} \pm x^{-1/2}$ give $y = x^{1/4} e^{\pm 2\sqrt{x}}$. Both examples are checked by the test file.

## Correctness

If line L8 returns, the output is a solution: in case 1, substituting $y = P e^{\int \omega}$ gives $y'' - r y = e^{\int \omega} (P'' + 2\omega P' + (\omega' + \omega^2 - r)P) = 0$. In cases 2 and 3, $F$ is built so that each of its roots satisfies the Riccati equation, which is equivalent to $F$ dividing $F_x + F_w\, (r - w^2)$ in $K(x)[w]$, and the implementation checks this identity on every output. Conversely, Kovacic's theorem says that if a Liouvillian solution exists, the Galois group is in one of the first three cases, and then some solution has $w$ algebraic of degree $n$ with $n$ in the allowed list. The Laurent expansion of the Riccati equation at each pole and at infinity forces the leading terms of $w$, which are exactly the local choices of line L4, and comparing residues at infinity with the residues at the poles gives the degree $d$ of line L5. So the right family is tried, and its $P$ exists. The proof file gives the full argument for case 1 and the soundness of case 2, and cites Kovacic for the rest.

## Complexity

The cost model counts operations in $K$, as on a [BSS machine](/blum-shub-smale-machine/) over $\mathbb{Q}$. Finding the poles, the factorization of $t$, is a separate cost, and so are the square roots of the numbers $1 + 4b$; both are done once per input. These bounds are proved:

- **Families.** With $k$ finite poles, there are at most $2^{k+1}$ families in case 1, $3^{k+1}$ in case 2 and $13^{k+1}$ for $n = 12$ in case 3, which dominates.
- **One family.** The auxiliary equation for $P$ of degree $d$ is a linear system with $d + 1$ unknowns and $O(d + T)$ equations, solved by [Gaussian elimination](/gaussian-elimination/) in $O((d + T)^3)$ operations, where the factor depending only on $n \le 12$ is a constant. In total, $O(13^{k+1} (D + T)^3)$ operations and $O((D + T)^2)$ extra space.

The degree $D$ is not polynomial in the input size: $r = x^2 + 2D + 1$ has the solution $H_D(x)\, e^{x^2/2}$ for a polynomial $H_D$ of degree $D$, related to the Hermite polynomials, from coefficients of size $\log D$. The exponential number of families is rarely met in practice, which is an observation: most families fail the integrality test of line L5 at once. On the random tests of the implementation, whole runs take milliseconds, and the planted solutions are always found.

## Properties

- **A decision procedure.** It decides whether a Liouvillian solution exists, and the answer "none" is a proof, through Kovacic's theorem, that no solution in closed form of this kind exists.
- **Deterministic and exact.** All arithmetic is in $K$ or in the field of the poles, with no randomness.
- **One solution or two.** In case 1 it finds one solution $y_1$, and a second one is $y_1 \int y_1^{-2}$, also Liouvillian. In cases 2 and 3 all roots of $F$ give solutions.
- **Group information.** The first case that succeeds tells the Galois group: reducible, imprimitive, or finite primitive with $n = 4$ tetrahedral, $n = 6$ octahedral, $n = 12$ icosahedral.

## Variants and improvements

- **Ulmer and Weil (1996).** Cases 2 and 3 are recast through invariants and semi-invariants of the possible groups, which shortens the search and tells the group directly.
- **Higher order.** Singer's method finds Liouvillian solutions of linear equations of any order, and van Hoeij, Ragot, Ulmer and Weil gave practical versions for order $3$.
- **Algebraic extensions.** Instead of splitting $t$, one can work with the poles as conjugate roots, which avoids building the splitting field.
- **Reduction to known equations.** Methods by van Hoeij and others recognise $y'' = r y$ as a transform of a Bessel, Whittaker or hypergeometric equation, which finds closed forms in special functions that Kovacic's algorithm rejects.

## When to use it

Use it to solve a second-order linear ODE with rational coefficients in closed form, or to prove that no Liouvillian solution exists, for instance to show that the Airy equation $y'' = x y$ has none. It is a step in [closed-form ODE solving](/closed-form-ode-solving/) in computer algebra systems. For first-order equations, an integral and an exponential are enough. For equations of order above two, use Singer's method or its successors, and for solutions in special functions, use the methods that reduce to known equations.

## Pitfalls

- **The normal form.** The algorithm needs $y'' = r y$ with no $y'$ term. Forgetting the substitution $y = z e^{-\int a/2}$ applies the conditions to the wrong function.
- **Irrational poles and exponents.** The poles can be irrational, and $\sqrt{1 + 4b}$ may be irrational, so a complete implementation works over the splitting field of $t$. This implementation stops with an error instead of answering wrongly.
- **Large degree bounds.** The bound $d$ can be large for small inputs, as in the Hermite example, which makes the linear systems large.
- **Case 3 cost.** For $n = 12$ the recursion produces polynomials of large degree, and the number of exponents is large. Ulmer and Weil's version is much faster.
- **A wrong sign at infinity.** The residue at infinity has the opposite sign convention to the residues at the poles, $\alpha_\infty = \frac12(\pm b/a - v)$, a frequent slip.

## Implementations

## History

Liouville showed in the 1830s and 1840s that some equations, such as Airy's, have no solution in closed form, and Picard and Vessiot built the Galois theory of linear differential equations around 1900. Kovacic found his algorithm in the late 1970s, and it circulated as a preprint before its 1986 publication in the Journal of Symbolic Computation. Saunders implemented it in MACSYMA in 1981. Singer extended the idea to equations of any order in 1981, and Ulmer and Weil simplified the third case in 1996.

## References
