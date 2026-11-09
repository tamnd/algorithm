---
tag: 9ARADQ
kind: definition
slug: total-unimodularity
name: Total unimodularity
aliases:
- totally unimodular matrix
- TU matrix
- totally unimodular
area: optimization/integer-programming
level: core
summary: A matrix whose every square submatrix has determinant 0, 1 or -1.
prereqs: [polyhedron, basic-feasible-solution, cramers-rule]
see_also: [hoffman-kruskal-theorem, totally-dual-integrality, ideal-formulation, incidence-matrix, flow-integrality-theorem, bipartite-matching, unimodular-matrix, min-cost-flow-problem]
sources:
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 19 (totally unimodular matrices, characterizations and examples), Chapter 20 (recognizing total unimodularity) and Chapter 21 (further theory)
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 4 (totally unimodular matrices, network matrices and Ghouila-Houri's theorem)
  - book: isbn:9780471828198
    title: George L. Nemhauser and Laurence A. Wolsey, Integer and Combinatorial Optimization, Wiley, 1988
    locator: Part III, Chapter 1 (integral polyhedra and totally unimodular matrices)
  - paper: "Alan J. Hoffman and Joseph B. Kruskal, Integral boundary points of convex polyhedra, in H. W. Kuhn and A. W. Tucker (eds.), Linear Inequalities and Related Systems, Annals of Mathematics Studies 38, Princeton University Press, 1956, 223 to 246"
    locator: the integrality theorem
  - paper: "Alain Ghouila-Houri, Caractérisation des matrices totalement unimodulaires, Comptes Rendus de l'Académie des Sciences Paris 254 (1962), 1192 to 1194"
    locator: the row partition characterization
  - paper: "Paul D. Seymour, Decomposition of regular matroids, Journal of Combinatorial Theory Series B 28 (1980), 305 to 359"
    locator: the decomposition theorem and its consequence for totally unimodular matrices
---

## Definition

A matrix $A$ with integer entries is *totally unimodular* (TU) if every square submatrix of $A$ has determinant $0$, $+1$ or $-1$.

Taking $1 \times 1$ submatrices shows that each entry is $0$, $+1$ or $-1$. The matrix need not be square. A square TU matrix that is nonsingular is a [unimodular matrix](/unimodular-matrix/), but most unimodular matrices are not TU: the matrix with rows $(1, 2)$ and $(0, 1)$ has determinant 1 and an entry 2.

**Why it matters.** If $A$ is TU and $b$ is integral, every vertex of $P = \{x : Ax \le b\}$ is integral. A vertex $\bar x$ is the unique solution of $A' x = b'$, where $A'$ is a nonsingular $n \times n$ submatrix of $A$ and $b'$ the matching part of $b$. Since $\det A' = \pm 1$, [Cramer's rule](/cramers-rule/) gives $\bar x_j = \det A'_j / \det A' = \pm \det A'_j$, where $A'_j$ is $A'$ with column $j$ replaced by $b'$. This is an integer. So $P$ is an [ideal formulation](/ideal-formulation/) of its integer points, and the [simplex method](/simplex-method/) returns an integer optimum. The [Hoffman-Kruskal theorem](/hoffman-kruskal-theorem/) gives the converse.

**Operations that keep total unimodularity.** If $A$ is TU, then so are:

- $A^T$, and $A$ with rows or columns permuted;
- $A$ with a row or column multiplied by $-1$;
- $A$ with a repeated row or column, or with a unit row or column added; so $[A \ \ I]$, $\begin{bmatrix} A \\ -A \\ I \\ -I \end{bmatrix}$ and similar stacks are TU;
- the matrix after a pivot on a nonzero entry, as in a simplex step.

The stacked forms show that, with $A$ TU and integral $b$, $\ell$, $u$, $d$, the polyhedra $\{x : Ax \le b,\ x \ge 0\}$, $\{x : Ax = b,\ \ell \le x \le u\}$ and $\{x : d \le Ax \le b\}$ are integral. Since $A^T$ is TU, the dual $\min\{y^T b : y^T A = c^T,\ y \ge 0\}$ also has an integral optimal solution for each integral $c$ for which it is finite. Primal and dual integrality together give min-max theorems such as König's theorem and the [max-flow min-cut theorem](/max-flow-min-cut-theorem/).

**Ghouila-Houri's characterization.** A matrix $A$ is TU if and only if each set $R$ of rows can be split into two parts $R_1$ and $R_2$ such that

$$\sum_{i \in R_1} a_i - \sum_{i \in R_2} a_i \in \{0, +1, -1\}^n,$$

where $a_i$ is row $i$. By transposition, the same holds with columns.

**A sufficient condition.** Let $A$ have entries in $\{0, \pm 1\}$ and at most two nonzeros in each column. If the rows can be split into two classes such that two nonzeros of the same sign in a column lie in different classes and two of opposite sign lie in the same class, then $A$ is TU. This follows from Ghouila-Houri's theorem: give the rows of one class the sign $+1$ and the rows of the other the sign $-1$.

**Network matrices.** Let $T$ be a directed tree and $D$ a directed graph on the same vertex set. The network matrix has a row for each arc $a$ of $T$ and a column for each arc $(u, v)$ of $D$. Its entry is $+1$ if $a$ lies on the path from $u$ to $v$ in $T$ in the forward direction, $-1$ if in the backward direction, and $0$ otherwise. Every network matrix is TU (Tutte). Seymour (1980) proved that every TU matrix can be built from network matrices, their transposes and two special $5 \times 5$ matrices

$$B_1 = \begin{bmatrix} 1 & -1 & 0 & 0 & -1 \\ -1 & 1 & -1 & 0 & 0 \\ 0 & -1 & 1 & -1 & 0 \\ 0 & 0 & -1 & 1 & -1 \\ -1 & 0 & 0 & -1 & 1 \end{bmatrix}, \qquad B_2 = \begin{bmatrix} 1 & 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 0 & 0 \\ 1 & 0 & 1 & 1 & 0 \\ 1 & 0 & 0 & 1 & 1 \\ 1 & 1 & 0 & 0 & 1 \end{bmatrix}$$

by the operations above and by 1-sums, 2-sums and 3-sums. A consequence is that total unimodularity can be tested in polynomial time, while the definition alone suggests a check of exponentially many determinants.

## Examples and non-examples

**The incidence matrix of a bipartite graph** is TU. The [incidence matrix](/incidence-matrix/) has a row for each vertex and a column for each edge, with two 1s per column. Put the rows of one side in one class and the rows of the other side in the other, and apply the sufficient condition. For $K_{2,3}$, every square submatrix has determinant $0$ or $\pm 1$, and the polytope $\{x \ge 0 : x(\delta(v)) \le 1\}$ has 13 vertices, which are the 13 matchings of $K_{2,3}$. This is why [bipartite matching](/bipartite-matching/) and the [assignment problem](/assignment-problem/) are linear programs.

**The incidence matrix of a directed graph** is TU. Each column, for an arc $(u, v)$, has $+1$ in row $u$ and $-1$ in row $v$. Put all rows in one class. This gives integral optima for [maximum flow](/max-flow-problem/), [min-cost flow](/min-cost-flow-problem/) and shortest paths with integral data, which is the [flow integrality theorem](/flow-integrality-theorem/). For the directed triangle with arcs $1 \to 2$, $2 \to 3$, $1 \to 3$, the matrix

$$\begin{bmatrix} 1 & 0 & 1 \\ -1 & 1 & 0 \\ 0 & -1 & -1 \end{bmatrix}$$

is TU, and its determinant is 0, since the rows sum to zero.

**Interval matrices** are TU. A 0/1 matrix whose columns each have their 1s in consecutive rows, such as

$$\begin{bmatrix} 1 & 0 & 1 & 0 \\ 1 & 1 & 1 & 0 \\ 0 & 1 & 1 & 1 \\ 0 & 1 & 0 & 1 \end{bmatrix},$$

is a network matrix: take for $T$ a directed path whose arcs are the rows, in order, and for each column an arc of $D$ from the start of its interval to its end. Interval matrices model shift scheduling, where a worker covers consecutive hours, and the maximum weight set of disjoint intervals.

**The incidence matrix of an odd cycle** is not TU. For the triangle,

$$\begin{bmatrix} 1 & 1 & 0 \\ 1 & 0 & 1 \\ 0 & 1 & 1 \end{bmatrix}$$

has determinant $-2$, and for the 5-cycle the determinant is $2$. Correspondingly, $x = (1/2, 1/2, 1/2)$ is a fractional vertex of the matching relaxation of the triangle. The incidence matrix of the 4-cycle is TU, since that graph is bipartite. In general, the incidence matrix of an undirected graph is TU if and only if the graph is bipartite.

**Entries in $\{0, \pm 1\}$ are not enough.** The matrix with rows $(1, 1)$ and $(1, -1)$ has determinant $-2$. The system $x_1 + x_2 \le 1$, $x_1 - x_2 \le 0$ has the fractional vertex $(1/2, 1/2)$.

## Related definitions

- **[Unimodular matrix](/unimodular-matrix/).** A square integer matrix with determinant $\pm 1$. In integer programming, an integer matrix $A$ of full row rank is also called unimodular when each basis of $A$ has determinant $\pm 1$. This weaker property is exactly what makes $\{x \ge 0 : Ax = b\}$ integral for every integral $b$ (Veinott and Dantzig).
- **[Total dual integrality](/totally-dual-integrality/).** A property of a system $Ax \le b$, not of the matrix alone. If $A$ is TU, then $Ax \le b$ is TDI for each $b$.
- **Balanced matrix.** A 0/1 matrix with no square submatrix of odd order that has exactly two 1s in each row and each column. TU 0/1 matrices are balanced. Balanced matrices give integral set packing and set covering polytopes, though they need not be TU.
- **Regular matroid.** A matroid that can be represented over every field. These are exactly the matroids represented by TU matrices, which is the setting of Seymour's decomposition theorem.
- **Equimodular and $k$-regular matrices.** Generalizations in which all bases have the same determinant up to sign, or in which a scaled form of the integrality property holds.

## References
