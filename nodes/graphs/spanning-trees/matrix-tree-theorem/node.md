---
tag: EB7F97
kind: theorem
slug: matrix-tree-theorem
name: Kirchhoff's matrix-tree theorem
aliases:
- Kirchhoff's theorem
- Matrix-tree theorem
- matrix-tree theorem
area: graphs/spanning-trees
level: advanced
summary: The number of spanning trees equals any cofactor of the graph Laplacian.
prereqs: [spanning-tree, laplacian-matrix, determinant, incidence-matrix]
see_also: [counting-spanning-trees, cayley-formula, uniform-spanning-tree-sampling, aldous-broder, arborescence, multigraph, fundamental-cycle, spanning-tree-enumeration]
sources:
  - paper: doi:10.1002/andp.18471481202
    title: "Gustav Kirchhoff, Ueber die Auflösung der Gleichungen, auf welche man bei der Untersuchung der linearen Vertheilung galvanischer Ströme geführt wird, Annalen der Physik und Chemie 72 (148 in the Wiley numbering) (1847), 497-508"
    locator: the whole paper (the solution of the circuit equations by sums over spanning trees)
  - book: isbn:9780521560696
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 2, Cambridge University Press (1999)
    locator: Section 5.6, Oriented trees and the Matrix-Tree Theorem
  - book: isbn:9780387952208
    title: Chris Godsil and Gordon Royle, Algebraic Graph Theory, Springer Graduate Texts in Mathematics 207 (2001)
    locator: Chapter 13, The Laplacian of a Graph
---

Kirchhoff's matrix-tree theorem says that the number of [spanning trees](/spanning-tree/) of a loopless undirected [multigraph](/multigraph/) $G$ equals each cofactor of its [Laplacian matrix](/laplacian-matrix/) $L = D - A$: delete any one row $i$ and the column $i$, and take the [determinant](/determinant/) of what remains. So the number of spanning trees, which can be exponential in $n$, is computed in $O(n^3)$ arithmetic operations. Equivalent forms give the count as $\frac{1}{n}$ times the product of the nonzero eigenvalues of $L$, and as a sum over weighted trees when the edges carry weights. Tutte's directed form counts arborescences. The theorem is the base of [counting spanning trees](/counting-spanning-trees/), of [Cayley's formula](/cayley-formula/) $n^{n-2}$ and of the analysis of [uniform spanning trees](/uniform-spanning-tree-sampling/).

## Statement

Let $G = (V, E)$ be an undirected multigraph with $V = \{1, \dots, n\}$, $n \ge 1$. Parallel edges are allowed. Self-loops are in no spanning tree and are ignored below. Let $\tau(G)$ be the number of spanning trees of $G$, counted as edge sets, so two parallel edges give different trees.

The *Laplacian* of $G$ is the $n \times n$ matrix $L$ with

$$L_{ii} = \deg(i), \qquad L_{ij} = -(\text{the number of edges between } i \text{ and } j) \quad (i \ne j),$$

where $\deg(i)$ counts the edges at $i$ other than self-loops. For a set of indices, $L^{(i)}$ is $L$ with row $i$ and column $i$ deleted.

**Theorem (matrix-tree theorem).**

1. **Cofactor form.** For each $i \in V$, $\tau(G) = \det L^{(i)}$. More generally, each cofactor $(-1)^{i+j} \det L^{(i, j)}$, with row $i$ and column $j$ deleted, equals $\tau(G)$.
2. **Eigenvalue form.** If $0 = \mu_1 \le \mu_2 \le \dots \le \mu_n$ are the eigenvalues of $L$, then $\tau(G) = \frac{1}{n} \mu_2 \mu_3 \cdots \mu_n$.
3. **Weighted form.** If edge $e$ has a weight $x_e$ in a commutative ring, and $L$ is built with $L_{ii} = \sum_{e \ni i} x_e$ and $L_{ij} = -\sum_{e = ij} x_e$, then $\det L^{(i)} = \sum_{T} \prod_{e \in T} x_e$, the sum over all spanning trees $T$.
4. **Directed form (Tutte).** Let $G$ be a directed multigraph, and let $L^{\mathrm{in}} = D^{\mathrm{in}} - A$, where $D^{\mathrm{in}}$ holds the in-degrees and $A_{uv}$ is the number of arcs from $u$ to $v$. Then $\det L^{\mathrm{in}\,(r)}$ is the number of spanning [arborescences](/arborescence/) rooted at $r$, that is, of spanning trees in which every arc points away from $r$.

If $G$ is not connected, each side of part 1 is 0. For $n = 1$, the matrix $L^{(1)}$ is empty, its determinant is 1, and the single vertex is the one spanning tree.

## In plain words

The number of ways to pick a tree that connects all points of a network can be huge, far too large to list one by one. This theorem gives the number by one calculation on a table of numbers.

Build a square table with one row and one column per point. On the diagonal, write how many links each point has. Off the diagonal, write minus the number of links between the two points. Now cross out one row and the matching column, any one you like, and compute the determinant of what is left, a standard calculation from linear algebra. The result is the number of trees.

Kirchhoff found it while solving the equations of electrical circuits.

## Proof

The proof is for part 1 with $i = j$, then part 3, by the Cauchy-Binet formula. Parts 2 and 4 and the general cofactors follow after it.

**The incidence matrix.** Orient each edge $e$ of $G$ in an arbitrary way, from $u$ to $v$. Let $B$ be the $n \times m$ matrix with $B_{ue} = +1$, $B_{ve} = -1$ and 0 elsewhere in column $e$. Then $L = B B^{\mathsf T}$: the entry $(i, i)$ of $B B^{\mathsf T}$ is the number of edges at $i$, and the entry $(i, j)$ is $\sum_e B_{ie} B_{je}$, which is $-1$ for each edge between $i$ and $j$ and $0$ for the others. Let $B_i$ be $B$ with row $i$ deleted. Then $L^{(i)} = B_i B_i^{\mathsf T}$.

**Cauchy-Binet.** For an $(n-1) \times m$ matrix $B_i$,

$$\det(B_i B_i^{\mathsf T}) = \sum_{S \subseteq E,\ |S| = n - 1} \det(B_i[S])^2,$$

where $B_i[S]$ is the square submatrix formed by the columns in $S$. If $m < n - 1$, the sum is empty, $G$ has no spanning tree, and $L^{(i)}$ has rank at most $m < n - 1$, so both sides are 0.

**Lemma.** For a set $S$ of $n - 1$ edges, $\det B_i[S] = \pm 1$ if $S$ is a spanning tree, and $0$ otherwise.

*Proof.* If $S$ is not a spanning tree, then $(V, S)$, which has $n - 1$ edges, is not connected, since a connected graph with $n$ vertices and $n - 1$ edges is a tree. Let $K$ be a component of $(V, S)$ that does not contain $i$. Add up the rows of $B_i[S]$ that belong to the vertices of $K$. A column of an edge inside $K$ has $+1$ and $-1$ in these rows, and a column of an edge outside $K$ has 0 in them; no edge of $S$ has exactly one end in $K$. So the sum is the zero row, the rows are dependent, and the determinant is 0.

If $S$ is a spanning tree, use induction on $n$. For $n = 1$, the matrix is empty and its determinant is 1. For $n \ge 2$, the tree has at least two leaves, so it has a leaf $v \ne i$. The row of $v$ in $B_i[S]$ has exactly one nonzero entry, $\pm 1$, in the column of the leaf edge $f$. Expand the determinant along this row: $\det B_i[S] = \pm \det M$, where $M$ is $B_i[S]$ without the row $v$ and the column $f$. The matrix $M$ is the matrix $B_i[S \setminus \{f\}]$ of the tree $S \setminus \{f\}$ on $V \setminus \{v\}$, with the row $i$ deleted, so $\det M = \pm 1$ by induction. $\square$

**Part 1 with $i = j$.** By Cauchy-Binet and the lemma, $\det L^{(i)} = \sum_S \det(B_i[S])^2$ adds 1 for each spanning tree and 0 for each other set. So $\det L^{(i)} = \tau(G)$.

**Part 3.** Let $B'$ be $B$ with column $e$ multiplied by $x_e$. Then $L = B' B^{\mathsf T}$, over any commutative ring. Cauchy-Binet for two different matrices gives $\det L^{(i)} = \sum_S \det B'_i[S] \det B_i[S] = \sum_S \big(\prod_{e \in S} x_e\big) \det(B_i[S])^2$, and the lemma ends the proof.

**All cofactors are equal.** Each row and each column of $L$ sums to 0. So the adjugate matrix $\operatorname{adj}(L)$ satisfies $L \operatorname{adj}(L) = \det(L) I = 0$. If $G$ is connected, $L$ has rank $n - 1$ (the cofactor $\det L^{(1)} = \tau(G) \ne 0$), so its kernel is spanned by the all-ones vector $\mathbf{1}$, and each column of $\operatorname{adj}(L)$ is a multiple of $\mathbf{1}$. By symmetry of $L$, the same holds for each row. So all entries of $\operatorname{adj}(L)$, which are the cofactors, are equal, and they equal $\det L^{(1)} = \tau(G)$. If $G$ is not connected, $L$ has rank less than $n - 1$, and all cofactors are 0.

**Part 2.** The characteristic polynomial $\det(t I - L) = t \prod_{k \ge 2} (t - \mu_k)$ has the coefficient of $t$ equal to $(-1)^{n-1} \mu_2 \cdots \mu_n$. The same coefficient is $(-1)^{n-1}$ times the sum of the $n$ principal minors of size $n - 1$ of $L$, which is $n \tau(G)$. So $\mu_2 \cdots \mu_n = n \tau(G)$.

**Part 4** has the same shape. Let $B$ now have $-1$ at the tail and $+1$ at the head of each arc, and let $H$ be the $n \times m$ matrix with $H_{ve} = 1$ if the arc $e$ enters $v$ and 0 otherwise. Then $H B^{\mathsf T} = (L^{\mathrm{in}})^{\mathsf T}$, and Cauchy-Binet gives $\det L^{\mathrm{in}\,(r)} = \sum_S \det H_r[S] \det B_r[S]$. The lemma becomes: the product $\det H_r[S] \det B_r[S]$ is 1 if $S$ is an arborescence rooted at $r$ and 0 otherwise. Stanley, Section 5.6, gives the full proof. $\blacksquare$

## Consequences

- **[Cayley's formula](/cayley-formula/).** For the complete graph $K_n$, $L = n I - J$, where $J$ is the all-ones matrix. Its eigenvalues are 0 once and $n$ with multiplicity $n - 1$, so $\tau(K_n) = \frac{1}{n} n^{n-1} = n^{n-2}$.
- **Complete bipartite graphs.** For $K_{a,b}$, the eigenvalues of $L$ are $0$, $a$ ($b - 1$ times), $b$ ($a - 1$ times) and $a + b$, so $\tau(K_{a,b}) = a^{b-1} b^{a-1}$.
- **A polynomial algorithm.** The count takes $O(n^3)$ arithmetic operations by Gaussian elimination; with exact integers, fraction-free elimination keeps the numbers at $O(n \log n)$ bits. See [counting spanning trees](/counting-spanning-trees/).
- **Uniform spanning trees.** The probability that an edge $e = uv$ is in a uniform random spanning tree is the effective resistance between $u$ and $v$ when each edge is a unit resistor, a fact that goes back to Kirchhoff's analysis. Part 3 with one variable weight gives it: the probability is $\tau(G \text{ with } e \text{ contracted}) / \tau(G)$.
- **Deletion and contraction.** $\tau(G) = \tau(G - e) + \tau(G / e)$ for each edge $e$ that is not a self-loop, since the trees that avoid $e$ are the trees of $G - e$ and the trees that contain $e$ correspond to the trees of $G / e$. In part 3, these are the terms of $\det L^{(i)}$ without and with the factor $x_e$.

## Tightness

- **A cofactor, not the determinant.** Each row of $L$ sums to 0, so $\det L = 0$ for every graph. One row and one column must be deleted.
- **Directed graphs need the directed form.** For the directed graph with one arc $a \to b$, $L^{\mathrm{in}} = \begin{pmatrix} 0 & -1 \\ 0 & 1 \end{pmatrix}$. Deleting row and column $a$ gives $1$, the one arborescence rooted at $a$; deleting $b$ gives $0$, since no arborescence is rooted at $b$. So in the directed case the cofactor depends on the deleted index, and the undirected statement "every cofactor is equal" fails.
- **Self-loops must be ignored.** Some texts add 2 to the diagonal entry for each self-loop. That matrix gives wrong counts. For the graph with the vertices 1 and 2, one edge $12$ and a self-loop at 1, the count is 1, and the Laplacian that ignores the loop gives $L^{(2)} = (1)$; with the loop counted, the entry would be $3$.

**Example: $K_4$ without one edge.** Take the vertices $a, b, c, d$ and the edges $ab$, $ac$, $bc$, $bd$, $cd$. Deleting the row and column of $a$,

$$L^{(a)} = \begin{pmatrix} 3 & -1 & -1 \\ -1 & 3 & -1 \\ -1 & -1 & 2 \end{pmatrix}, \qquad \det L^{(a)} = 3 \cdot 5 + 1 \cdot (-3) - 1 \cdot 4 = 8.$$

The 8 spanning trees are the 10 sets of three of the five edges, less the two triangles $\{ab, bc, ca\}$ and $\{bc, cd, db\}$.

**Example: a graph with six vertices.** For the vertices $a$ to $f$ and the edges $ab$, $ac$, $bc$, $bd$, $cd$, $ce$, $de$, $df$, $ef$, the Laplacian in the order $a, \dots, f$ is

$$L = \begin{pmatrix} 2 & -1 & -1 & 0 & 0 & 0 \\ -1 & 3 & -1 & -1 & 0 & 0 \\ -1 & -1 & 4 & -1 & -1 & 0 \\ 0 & -1 & -1 & 4 & -1 & -1 \\ 0 & 0 & -1 & -1 & 3 & -1 \\ 0 & 0 & 0 & -1 & -1 & 2 \end{pmatrix}.$$

Each of the six principal cofactors equals 55, the number of spanning trees, which a direct count of the $\binom{9}{5} = 126$ sets of five edges confirms. The nonzero eigenvalues multiply to $6 \cdot 55 = 330$.

## History

Kirchhoff (1847) solved the linear equations of an electrical network and expressed the currents as sums over the spanning trees of the network; the counting theorem is implicit in that paper. Borchardt (1860) and Cayley (1889) used determinants to count the trees of complete graphs. Tutte (1948) proved the directed form for arborescences. Modern statements, with the proof by Cauchy-Binet, are in Stanley's Section 5.6 and in Godsil and Royle, Chapter 13.

## References
