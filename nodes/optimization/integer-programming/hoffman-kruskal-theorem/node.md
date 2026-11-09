---
tag: 7273HV
kind: theorem
slug: hoffman-kruskal-theorem
name: Hoffman-Kruskal theorem
aliases:
- total unimodularity integrality theorem
- Hoffman and Kruskal integrality theorem
area: optimization/integer-programming
level: advanced
summary: 'If A is totally unimodular and b is integral, the polyhedron {x : Ax <= b} is integral.'
prereqs: [total-unimodularity, basic-feasible-solution, cramers-rule, polyhedron]
see_also: [total-unimodularity, totally-dual-integrality, ideal-formulation, flow-integrality-theorem, bipartite-matching, integer-hull, unimodular-matrix, lp-relaxation]
sources:
  - paper: "Alan J. Hoffman and Joseph B. Kruskal, Integral boundary points of convex polyhedra, in H. W. Kuhn and A. W. Tucker (eds.), Linear Inequalities and Related Systems, Annals of Mathematics Studies 38, Princeton University Press, 1956, 223 to 246"
    locator: the main theorem
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 19 (totally unimodular matrices, the Hoffman-Kruskal theorem and the Veinott-Dantzig form)
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 4 (totally unimodular matrices)
  - paper: "Arthur F. Veinott and George B. Dantzig, Integral extreme points, SIAM Review 10 (1968), 371 to 372"
    locator: the short proof by unimodular bases
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming, Wiley, 1998
    locator: Chapter 3 (well-solved problems, total unimodularity)
---

## Statement

**Theorem (Hoffman and Kruskal, 1956).** Let $A$ be an $m \times n$ integer matrix. Then $A$ is [totally unimodular](/total-unimodularity/) if and only if, for every integral vector $b \in \mathbb{Z}^m$, the polyhedron

$$P(b) = \{x \in \mathbb{R}^n : Ax \le b,\ x \ge 0\}$$

is integral, that is, each vertex of $P(b)$ is an integer vector.

**The direction used most.** If $A$ is totally unimodular and $b$ is integral, then each vertex of $\{x : Ax \le b\}$ is integral, with or without the condition $x \ge 0$. The same holds for $\{x : Ax = b,\ \ell \le x \le u\}$ with integral $\ell$ and $u$.

## In plain words

Some integer programs are secretly easy: if you solve them as ordinary linear programs, the answer comes out in whole numbers anyway. The theorem names the property of the constraint matrix that makes this happen for every whole-number right side: every square piece of the matrix must have determinant 0, 1 or minus 1.

The reason is the formula for solving a square system of equations. The answer is a ratio of two determinants. If the bottom one is 1 or minus 1, the answer is a whole number. The theorem also says that nothing weaker works in general: if the answers come out whole for every right side, then all those determinants must be 0, 1 or minus 1.

## Proof

Let $\bar A = \begin{bmatrix} A \\ -I \end{bmatrix}$, so that $P(b) = \{x : \bar A x \le (b, 0)\}$. Recall that a vertex of a polyhedron $\{x : Mx \le d\}$ is a point of it that is the unique solution of $M' x = d'$ for some subsystem $M' x \le d'$ of $n$ linearly independent rows.

*($\Rightarrow$)* Let $A$ be TU and $b$ integral. Adding unit rows and multiplying rows by $-1$ keeps total unimodularity, so $\bar A$ is TU. Let $\bar x$ be a vertex of $P(b)$, and let $M' x = d'$ be the subsystem of $n$ independent tight rows of $\bar A x \le (b, 0)$. Then $M'$ is a nonsingular square submatrix of $\bar A$, so $\det M' = \pm 1$. By [Cramer's rule](/cramers-rule/), $\bar x_j = \det M'_j / \det M'$, where $M'_j$ is $M'$ with column $j$ replaced by $d'$. The matrix $M'_j$ is integral, so $\bar x_j$ is an integer.

The same argument with $M$ any TU matrix proves the second form of the statement. For $\{x : Ax = b,\ \ell \le x \le u\}$, the matrix with blocks $A$, $-A$, $I$, $-I$ is TU.

*($\Leftarrow$)* Assume that $P(b)$ is integral for each integral $b$. Let $A'$ be a $k \times k$ submatrix of $A$ with rows $R$ and columns $C$. If $\det A' = 0$ there is nothing to show, so let $A'$ be nonsingular. We prove $|\det A'| = 1$.

*Step 1: a basis.* Consider the $m \times (n + m)$ matrix $[A \ \ I]$. Let $B$ be its $m \times m$ submatrix formed by the columns of $A$ in $C$ and the unit columns $e_i$ for $i \notin R$. Order the rows with $R$ first. Then

$$B = \begin{bmatrix} A' & 0 \\ * & I \end{bmatrix},$$

so $\det B = \pm \det A' \ne 0$, and $B$ is a basis of $[A \ \ I]$.

*Step 2: $B^{-1}$ is integral.* Fix $i \in \{1, \ldots, m\}$. Choose an integer vector $z \in \mathbb{Z}^m$ with $z + B^{-1} e_i \ge 0$, for example $z_r = \lceil |(B^{-1} e_i)_r| \rceil$. Let

$$b = B z + e_i \in \mathbb{Z}^m, \qquad w = z + B^{-1} e_i \ge 0,$$

so that $B w = b$. Define $(\bar x, \bar s) \in \mathbb{R}^n \times \mathbb{R}^m$ by putting the entries of $w$ in the positions of the columns of $B$ and zeros elsewhere. Then $(\bar x, \bar s)$ is a [basic feasible solution](/basic-feasible-solution/) of

$$Q(b) = \{(x, s) : Ax + s = b,\ x \ge 0,\ s \ge 0\},$$

and hence a vertex of $Q(b)$. The map $x \mapsto (x, b - Ax)$ is an affine bijection from $P(b)$ onto $Q(b)$, so $\bar x$ is a vertex of $P(b)$. By assumption $\bar x$ is integral, and then $\bar s = b - A \bar x$ is integral too. So $w$ is integral, and $B^{-1} e_i = w - z$ is integral. This holds for each $i$, so $B^{-1}$ is an integer matrix.

*Step 3.* Both $\det B$ and $\det B^{-1}$ are integers, and their product is 1. So $|\det B| = 1$ and $|\det A'| = 1$. Since $A'$ was any nonsingular square submatrix, $A$ is TU. $\blacksquare$

The same proof, with $B$ any basis of a full row rank matrix $A$ and $Q(b) = \{x \ge 0 : Ax = b\}$, gives the theorem of Veinott and Dantzig: $\{x \ge 0 : Ax = b\}$ is integral for all integral $b$ if and only if every basis of $A$ has determinant $\pm 1$.

## Consequences

- **Integer programs that are linear programs.** If $A$ is TU and $b$, $c$ are integral, the [simplex method](/simplex-method/) returns an integer optimum of $\max\{c^T x : Ax \le b,\ x \ge 0\}$. Since $A^T$ is TU too, the dual has an integral optimal solution as well.
- **Flows.** The incidence matrix of a directed graph is TU, so a [flow network](/max-flow-problem/) with integral capacities has an integral maximum flow, and [min-cost flow](/min-cost-flow-problem/) with integral data has an integral optimum. This is the [flow integrality theorem](/flow-integrality-theorem/).
- **Bipartite matching.** The incidence matrix of a bipartite graph is TU. So [bipartite matching](/bipartite-matching/) and the [assignment problem](/assignment-problem/) are solved by their LP relaxations, and LP duality with integral duals gives König's theorem: in a bipartite graph, the largest matching and the smallest vertex cover have the same size.
- **Birkhoff's theorem.** The polytope of doubly stochastic $n \times n$ matrices is $\{x \ge 0 : \sum_j x_{ij} = 1,\ \sum_i x_{ij} = 1\}$, whose matrix is the incidence matrix of $K_{n,n}$. Its vertices are integral, so they are the permutation matrices.
- **Interval and network matrices.** Shift scheduling with consecutive hours, and problems whose matrix is a network matrix, are solved as linear programs.
- **Ideal formulations.** In modeling, showing that a block of constraints is TU proves that the formulation of that block is [ideal](/ideal-formulation/).

## Tightness

- **The condition $x \ge 0$ is needed for the converse.** The matrix with rows $(2, 1)$ and $(1, 1)$ is not TU, since it has the entry 2. But its determinant is 1 and its inverse, with rows $(1, -1)$ and $(-1, 2)$, is integral. So the only vertex of $\{x : Ax \le b\}$ is $A^{-1} b$, which is integral for each integral $b$. With $x \ge 0$ added, $b = (1, 1)$ gives the vertex $(1/2, 0)$, as the theorem predicts.
- **The condition must hold for every integral $b$.** For one fixed $b$, $P(b)$ can be integral although $A$ is not TU. For example, with the incidence matrix of a triangle and $b = 0$, $P(b) = \{0\}$. With $b = (1, 1, 1)$, the vertex $(1/2, 1/2, 1/2)$ appears.
- **Integral $b$ is needed.** For $A = [1]$ and $b = 1/2$, $P(b) = [0, 1/2]$ has the fractional vertex $1/2$.
- **TU is not necessary for integrality of the optimum values.** Systems that are [totally dual integral](/totally-dual-integrality/) give integral polyhedra for integral $b$ with matrices that are far from TU, such as the matching polytope with Edmonds' odd set constraints.

## History

Hoffman and Kruskal presented the theorem in 1956, in the volume *Linear Inequalities and Related Systems* edited by Kuhn and Tucker. In the same volume, Heller and Tompkins gave the sufficient condition for matrices with at most two nonzeros per column, which covers incidence matrices of bipartite and directed graphs. Earlier special cases include König's theorem of 1931 on bipartite graphs and Birkhoff's theorem of 1946 on doubly stochastic matrices. Veinott and Dantzig gave the short proof by unimodular bases in 1968. Ghouila-Houri characterized TU matrices by row partitions in 1962, and Seymour's decomposition theorem of 1980 gave a structure theorem and a polynomial-time test.

## References
