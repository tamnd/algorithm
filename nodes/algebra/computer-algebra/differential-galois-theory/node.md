---
tag: 4B8QRZ
kind: concept
slug: differential-galois-theory
name: Differential Galois theory
aliases:
- Picard-Vessiot theory
- Galois theory of linear differential equations
area: algebra/computer-algebra
level: research
summary: Galois theory for linear differential equations, classifying their closed-form solutions.
prereqs: [liouville-theorem, abel-ruffini-theorem]
see_also: [kovacic-algorithm, closed-form-ode-solving, risch-algorithm, holonomic-function, sturm-liouville-problem, finite-group]
sources:
  - book: isbn:9783540442288
    title: Marius van der Put and Michael F. Singer, Galois Theory of Linear Differential Equations, Grundlehren der mathematischen Wissenschaften 328, Springer, 2003
    locator: Chapter 1 (Picard-Vessiot extensions, the Galois correspondence and Liouvillian extensions), Chapter 4 (algorithmic considerations and Kovacic's algorithm) and Chapter 5 (monodromy and Schlesinger's theorem)
  - paper: "Ellis R. Kolchin, Algebraic matric groups and the Picard-Vessiot theory of homogeneous linear ordinary differential equations, Annals of Mathematics 49(1), 1-42, 1948"
    locator: the differential Galois group as a linear algebraic group and the theorem that Liouvillian solutions exist exactly when the identity component is solvable
  - paper: doi:10.1016/S0747-7171(86)80010-4
    title: Jerald J. Kovacic, An algorithm for solving second order linear homogeneous differential equations, Journal of Symbolic Computation 2(1), 3-43, 1986
    locator: the classification of the algebraic subgroups of SL(2) into four cases and the algorithm that decides which case occurs
  - book: isbn:9783540214939
    title: Manuel Bronstein, Symbolic Integration I, Transcendental Functions, second edition, Springer, 2005
    locator: Chapter 3 (differential fields, constants, and elementary and Liouvillian extensions)
  - paper: "Ehud Hrushovski, Computing the Galois group of a linear differential equation, Differential Galois Theory, Banach Center Publications 58, 97-138, 2002"
    locator: the first algorithm computing the differential Galois group of an equation of any order
  - paper: "Michael F. Singer, Liouvillian solutions of n-th order homogeneous linear differential equations, American Journal of Mathematics 103(4), 661-682, 1981"
    locator: the decision procedure for Liouvillian solutions of equations of any order, through the finite groups and the Riccati equation
---

Differential Galois theory, also called Picard-Vessiot theory, attaches to a linear differential equation a group of symmetries of its solutions, the *differential Galois group*, much as classical Galois theory attaches a group to a polynomial equation. The group is a linear algebraic group: a group of invertible matrices defined by polynomial equations. Its structure decides which closed-form solutions exist. The equation can be solved by Liouvillian functions, built from the coefficients by algebraic operations, integrals and exponentials of integrals, exactly when the identity component of the group is solvable (Kolchin 1948). This is the analogue of solving polynomial equations by radicals, and it is the theory behind [Kovacic's algorithm](/kovacic-algorithm/) and the other algorithms for [closed-form solutions of linear ODEs](/closed-form-ode-solving/).

## In plain words

Classical Galois theory explains why some polynomial equations have no formula in radicals: the solutions can be permuted in ways that are too complicated. Differential Galois theory does the same for linear differential equations.

The solutions of such an equation form a space. The symmetries that keep all the relations between the solutions and their derivatives form a group of matrices. When the group is small and simple in structure, the equation has solutions built from integrals, exponentials and roots. When the group is as large as possible, no such solution exists. Computer algebra uses this to prove that some equations, such as the Airy equation, have no closed-form solution, and to find the solutions of the others.

## The idea

**Setting and notation.** A *differential field* is a field $K$ with a derivation $\partial$, a map with $\partial(a + b) = \partial a + \partial b$ and $\partial(ab) = a\,\partial b + b\,\partial a$. Its *constants* are the $c$ with $\partial c = 0$; they form a field $C$, assumed of characteristic 0 and algebraically closed. The standard case is $K = C(x)$ with $\partial = d/dx$; computer algebra works with $C = \overline{\mathbb{Q}}$ and coefficients in $\mathbb{Q}(x)$. A linear equation of order $n$ is

$$L(y) = y^{(n)} + a_{n-1} y^{(n-1)} + \cdots + a_0 y = 0, \qquad a_i \in K,$$

an element of the ring of operators $K[\partial]$, with leading coefficient $\operatorname{LC}(L) = 1$ after division. Degrees $d$ of the coefficients and the number of terms $t$ measure the input of algorithms, whose costs are counted in operations in $C$; no monomial order is used, since $K[\partial]$ is ordered by the order in $\partial$ alone.

**Picard-Vessiot extension.** A differential field extension $E \supseteq K$ is a *Picard-Vessiot extension* for $L$ if $E$ is generated over $K$ by $n$ solutions $y_1, \ldots, y_n$ that are linearly independent over $C$, together with their derivatives, and $E$ has no new constants. In characteristic 0 with $C$ algebraically closed, it exists and is unique up to isomorphism. The solutions of $L$ in $E$ form a $C$-vector space $V$ of dimension $n$.

**The group.** The *differential Galois group* $G = \operatorname{Gal}_\partial(E/K)$ is the group of field automorphisms of $E$ that fix $K$ and commute with $\partial$. Each $\sigma \in G$ maps solutions to solutions, so it acts on $V$, and in the basis $y_1, \ldots, y_n$ it is a matrix in $\mathrm{GL}_n(C)$. The image is Zariski closed: $G$ is a linear algebraic group. The main facts:

- **Galois correspondence.** Closed subgroups $H \subseteq G$ correspond to intermediate differential fields $K \subseteq F \subseteq E$, by $H \mapsto E^H$ and $F \mapsto \operatorname{Gal}_\partial(E/F)$. In particular $E^G = K$: an element of $E$ fixed by all of $G$ lies in $K$. Normal closed subgroups correspond to Picard-Vessiot subextensions.
- **Dimension.** The transcendence degree of $E$ over $K$ equals the dimension of $G$ as an algebraic variety. $G$ is finite exactly when all solutions are algebraic over $K$.
- **Wronskian.** The Wronskian $W = \det(y_i^{(j)})$ satisfies $W' = -a_{n-1} W$. So $G \subseteq \mathrm{SL}_n(C)$ exactly when $W \in K$, which holds for instance when $a_{n-1} = 0$.
- **Liouvillian solutions (Kolchin).** A *Liouvillian extension* is a tower $K = K_0 \subseteq \cdots \subseteq K_m$ where each step adjoins an algebraic element, an integral ($u' \in K_{i-1}$) or the exponential of an integral ($u'/u \in K_{i-1}$). $E$ lies in a Liouvillian extension exactly when the identity component $G^\circ$ is solvable. Then $L$ has a solution $y$ whose logarithmic derivative $y'/y$ is algebraic over $K$ (Singer 1981).

**Second-order equations.** After a change of variables, $y'' = r y$ with $r \in K$, and $G \subseteq \mathrm{SL}_2(C)$. The algebraic subgroups of $\mathrm{SL}_2$ fall into four cases, which Kovacic's algorithm decides:

1. $G$ is reducible, a subgroup of the triangular group: there is a solution with $y'/y \in K$;
2. $G$ is imprimitive, a subgroup of the infinite dihedral group: $y'/y$ is algebraic of degree 2 over $K$;
3. $G$ is one of the finite primitive groups, the preimages in $\mathrm{SL}_2$ of the tetrahedral, octahedral and icosahedral groups: all solutions are algebraic, and $y'/y$ has degree 4, 6 or 12;
4. $G = \mathrm{SL}_2(C)$: there is no Liouvillian solution.

**Computing the group.** For order 2, Kovacic's algorithm determines $G$; for order 3 there are similar algorithms (Singer and Ulmer). Hrushovski (2002) gave the first algorithm for every order; its cost has no practical bound, and Feng (2015) made the bounds explicit. For Fuchsian equations, those with only regular singular points, the monodromy group, obtained by continuing solutions around the singular points, is Zariski dense in $G$ (Schlesinger's theorem). For irregular singularities the Stokes matrices and the exponential torus must be added (Ramis).

## Examples

Each solution below was checked by substituting it into the equation.

| equation over $C(x)$ | basis of solutions | $G$ | closed form |
|---|---|---|---|
| $y' = y$ | $e^x$ | $C^*$, the multiplicative group | exponential of an integral |
| $x y'' + y' = 0$ | $1$, $\log x$ | $\{\left(\begin{smallmatrix} 1 & b \\ 0 & 1 \end{smallmatrix}\right)\}$, the additive group | integral |
| $y'' + y = 0$ | $e^{ix}$, $e^{-ix}$ | the diagonal torus $\{\operatorname{diag}(c, c^{-1})\}$ | exponentials |
| $y'' = -\frac{3}{16x^2} y$ | $x^{1/4}$, $x^{3/4}$ | cyclic of order 4, generated by $\operatorname{diag}(i, -i)$ | algebraic |
| $y'' = (x^2 + 1) y$ | $e^{x^2/2}$, $e^{x^2/2} \int e^{-x^2}$ | the triangular group $\{\left(\begin{smallmatrix} a & b \\ 0 & a^{-1} \end{smallmatrix}\right)\}$ | Liouvillian, case 1 |
| $y'' = x y$ (Airy) | $\operatorname{Ai}(x)$, $\operatorname{Bi}(x)$ | $\mathrm{SL}_2(C)$ | none, case 4 |

For the fourth row, $(x^{1/4})'' = \frac14 \cdot (-\frac34) x^{-7/4} = -\frac{3}{16x^2} x^{1/4}$, and similarly for $x^{3/4}$. An automorphism must send $x^{1/4}$ to a root of $z^4 = x$, so to $i^k x^{1/4}$, and then $x^{3/4} = (x^{1/4})^3$ goes to $i^{3k} x^{3/4} = i^{-k} x^{3/4}$. For the fifth row, the Riccati equation $u' + u^2 = x^2 + 1$ has the rational solution $u = x$, so the group is reducible; it is the whole triangular group because $e^{x^2/2}$ and $\int e^{-x^2}$ are algebraically independent over $C(x)$. For the Airy equation, Kovacic's algorithm finds no solution in any of the first three cases; in fact, by the same reasoning, $y'' = r y$ with $r$ a polynomial of odd degree never has a Liouvillian solution. The Bessel equation $x^2 y'' + x y' + (x^2 - \nu^2) y = 0$ has Liouvillian solutions exactly when $\nu - \frac12$ is an integer; for $\nu = \frac12$ they are $\sin x / \sqrt{x}$ and $\cos x / \sqrt{x}$.

## Where it is used

- **Closed-form ODE solving.** [Kovacic's algorithm](/kovacic-algorithm/), Singer's algorithm and their successors decide whether a linear equation has Liouvillian solutions and find them; see [closed-form ODE solving](/closed-form-ode-solving/). The theory justifies the search: it says which forms of solutions are possible and bounds the algebraic degrees involved.
- **Proving non-existence.** Showing that the group of an equation is $\mathrm{SL}_n$ or another group with non-solvable identity component proves that no Liouvillian solution exists, as for the Airy equation and most Bessel equations.
- **Integration.** Integrals and exponentials of integrals are the simplest Picard-Vessiot extensions; their groups are the additive and multiplicative groups. [Liouville's theorem](/liouville-theorem/) and the [Risch algorithm](/risch-algorithm/) work in the same framework of differential fields.
- **Integrability of Hamiltonian systems.** Morales-Ruiz and Ramis proved that if a Hamiltonian system is integrable by meromorphic first integrals, the identity component of the Galois group of its variational equation along a solution is abelian. This has been used to prove the non-integrability of many mechanical systems.
- **Special functions and holonomic functions.** The group explains the algebraic relations among solutions of an equation, such as those between $\operatorname{Ai}$, $\operatorname{Bi}$ and their derivatives, and the algebraic dependence of [holonomic functions](/holonomic-function/).
- **The inverse problem.** Over $\mathbb{C}(x)$ every linear algebraic group occurs as a differential Galois group (Tretkoff and Tretkoff 1979); over $C(x)$ for other algebraically closed $C$, Mitschi and Singer (1996) proved it for connected groups and Hartmann (2005) in general.

## References
