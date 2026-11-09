---
tag: 3T1R8X
kind: theorem
slug: lindstrom-gessel-viennot-lemma
name: Lindström-Gessel-Viennot lemma
aliases:
- LGV lemma
- Gessel-Viennot lemma
- Gessel-Viennot method
area: combinatorics/counting-algorithms
level: advanced
summary: Counts nonintersecting path families as a determinant.
prereqs: [counting-lattice-paths, determinant]
see_also: [counting-lattice-paths, determinant, hook-length-formula, counting-standard-young-tableaux, catalan-numbers, kasteleyn-method, counting-perfect-matchings, matrix-tree-theorem]
sources:
  - paper: doi:10.1112/blms/5.1.85
    title: Bernt Lindström, On the vector representations of induced matroids, Bulletin of the London Mathematical Society 5 (1973), 85-90
    locator: the whole paper (the determinant of path sums in an acyclic graph)
  - paper: doi:10.1016/0001-8708(85)90121-5
    title: Ira Gessel and Gérard Viennot, Binomial determinants, paths, and hook length formulae, Advances in Mathematics 58 (1985), 300-321
    locator: the whole paper (nonintersecting lattice paths, binomial determinants and their combinatorial use)
  - paper: doi:10.2140/pjm.1959.9.1141
    title: Samuel Karlin and James McGregor, Coincidence probabilities, Pacific Journal of Mathematics 9 (1959), 1141-1164
    locator: the whole paper (the probabilistic form for Markov processes)
  - book: isbn:9783662572641
    title: Martin Aigner and Günter M. Ziegler, Proofs from THE BOOK, sixth edition, Springer, 2018
    locator: Chapter Lattice paths and determinants (the lemma, its proof and the Catalan Hankel determinants)
  - book: isbn:9780521560696
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 2, Cambridge University Press, 1999
    locator: Chapter 7, Section 7.21, The hook-length formula (MacMahon's formula for plane partitions in a box)
---

The Lindström-Gessel-Viennot lemma says that in a directed acyclic graph, the determinant of the matrix of path counts from $k$ sources to $k$ sinks is a signed count of the families of $k$ pairwise vertex-disjoint paths. When the geometry forces every such family to join the $i$-th source to the $i$-th sink, the sign disappears, and the [determinant](/determinant/) counts the nonintersecting families exactly. This turns hard counting problems about plane partitions, rhombus tilings, Young tableaux and Hankel determinants into $k \times k$ determinants of binomial coefficients, which take $O(k^3)$ arithmetic operations.

## Statement

**Notation.** $k \ge 1$ is an integer, $[k] = \{1, \ldots, k\}$, and $S_k$ is the set of permutations of $[k]$, with sign $\operatorname{sgn} \sigma$. $C(n, k)$ is the binomial coefficient. $G$ is a directed acyclic graph with finitely many paths between any two vertices, and each edge $e$ has a weight $w(e)$ in a commutative ring. The weight $w(P)$ of a path is the product of the weights of its edges (1 for a path with one vertex), and

$$e(u, v) = \sum_{P : u \to v} w(P).$$

With all weights 1, $e(u, v)$ is the number of paths from $u$ to $v$.

Let $a_1, \ldots, a_k$ be sources and $b_1, \ldots, b_k$ sinks, and let $M = [e(a_i, b_j)]_{i, j = 1}^{k}$. A *path system* is a permutation $\sigma \in S_k$ with paths $P_i : a_i \to b_{\sigma(i)}$ for $i \in [k]$. It is *nonintersecting* if no two of its paths share a vertex.

**Theorem (Lindström, Gessel and Viennot).**

$$\det M = \sum_{(\sigma, P_1, \ldots, P_k) \text{ nonintersecting}} \operatorname{sgn}(\sigma) \prod_{i=1}^{k} w(P_i).$$

**Corollary.** If every nonintersecting path system has $\sigma = \mathrm{id}$, then $\det M$ is the total weight, and with weights 1 the number, of the nonintersecting families of paths $P_i : a_i \to b_i$.

## In plain words

Several walkers start at different places in a one-way street network and each must reach a different goal. Count the ways in which no two walkers ever stand on the same corner. Counting the routes of one walker at a time is easy. Put these single counts in a square table, one row per walker and one column per goal. The determinant of the table cancels every plan in which two walkers meet, because each such plan pairs up with a plan of opposite sign. What is left counts the plans in which nobody meets.

## Proof

Expand the determinant and the path sums:

$$\det M = \sum_{\sigma \in S_k} \operatorname{sgn}(\sigma) \prod_{i=1}^{k} e(a_i, b_{\sigma(i)}) = \sum_{(\sigma, P_1, \ldots, P_k)} \operatorname{sgn}(\sigma) \prod_{i=1}^{k} w(P_i),$$

over all path systems. It is enough to find an involution $\Phi$ on the intersecting systems that keeps the multiset of edges, hence the weight, and changes the sign of $\sigma$. Then the intersecting systems cancel in pairs.

*The involution.* Let $(\sigma, P_1, \ldots, P_k)$ be intersecting. Let $i$ be the smallest index such that $P_i$ shares a vertex with another path. Let $v$ be the first vertex on $P_i$ that lies on some other path, and let $j$ be the smallest index $j \ne i$ with $v \in P_j$. Swap the tails after $v$: $P'_i$ is $P_i$ up to $v$ followed by $P_j$ after $v$, and $P'_j$ is $P_j$ up to $v$ followed by $P_i$ after $v$. The other paths stay. The new paths end at $b_{\sigma(j)}$ and $b_{\sigma(i)}$, so the new permutation is $\sigma \circ (i\ j)$, with the opposite sign. The edges used, with multiplicity, are the same, so the weight is the same.

*$\Phi$ is an involution.* We show that $\Phi$ picks the same $i$, $v$ and $j$ in the new system, so applying it twice gives back the original.

- The set of vertices covered by $P'_i$ and $P'_j$ together is that of $P_i$ and $P_j$, and the other paths are unchanged. So for each $l < i$, $P_l$ still meets no other path, and $P'_i$ meets $P'_j$ at $v$. So $i$ is again the smallest index.
- The part of $P'_i$ before $v$ is the part of $P_i$ before $v$. None of its vertices lies on $P_l$ for $l \ne i, j$, by the choice of $v$. None lies on $P'_j$ either: not on $P_j$ before $v$, by the choice of $v$, and not on $P_i$ after $v$, because a path in an acyclic graph does not repeat a vertex. So $v$ is again the first vertex of $P'_i$ on another path.
- The paths through $v$ have the same indices as before, since $v \in P'_i$, $v \in P'_j$ and the others are unchanged. So $j$ is again the smallest index $j \ne i$ with $v$ on its path.

So $\Phi$ is a fixed-point-free involution on the intersecting systems that reverses the sign and keeps the weight, and the intersecting systems contribute 0. The corollary follows, since every remaining term has $\operatorname{sgn}(\mathrm{id}) = 1$. $\blacksquare$

## Consequences

- **Two paths in the grid.** In $\mathbb{Z}^2$ with steps $E = (1, 0)$ and $N = (0, 1)$, take $a_1 = (0, 1)$, $a_2 = (1, 0)$, $b_1 = (n - 1, n)$ and $b_2 = (n, n - 1)$. A path $P$ from $a_1$ to $b_2$ and a path $Q$ from $a_2$ to $b_1$ must meet: each path has exactly one point on each line $x + y = s$, the difference of their $x$-coordinates goes from $-1$ at $s = 1$ to $1$ at $s = 2n - 1$, and it changes by at most 1 at each step, so it is 0 somewhere. So the corollary applies, and with the free counts of [counting lattice paths](/counting-lattice-paths/), the nonintersecting pairs number

$$C(2n - 2, n - 1)^2 - C(2n - 2, n - 2)^2:$$

$1, 3, 20, 175, 1764, 19404, 226512$ for $n = 1, \ldots, 7$ (OEIS A000891). For $n = 3$ this is $6 \cdot 6 - 4 \cdot 4 = 20$.
- **Catalan Hankel determinants.** With $C_m$ the [Catalan numbers](/catalan-numbers/), $\det[C_{i+j}]_{i, j = 0}^{n-1} = 1$ and $\det[C_{i+j+1}]_{i, j = 0}^{n-1} = 1$ for all $n \ge 1$. Take $a_i = (-2i, 0)$ and $b_j = (2j, 0)$ for Dyck paths with steps $(1, \pm 1)$ that stay at height $\ge 0$. Then $e(a_i, b_j) = C_{i+j}$, and exactly one nonintersecting family exists (Aigner and Ziegler).
- **Plane partitions in a box.** A plane partition with $a$ rows, $b$ columns and entries at most $c$ is a family of $a$ nonintersecting lattice paths, one per row, and the lemma gives the count $\det[C(b + c, b - i + j)]_{i, j = 1}^{a}$. Its value is MacMahon's product $\prod_{i=1}^{a} \prod_{j=1}^{b} \prod_{l=1}^{c} \frac{i + j + l - 1}{i + j + l - 2}$ (Stanley, EC2, Section 7.21). For $a = b = c = n$ the counts are $1, 2, 20, 980, 232848$ for $n = 0, \ldots, 4$ (OEIS A008793). These are also the rhombus tilings of a hexagon with sides $n, n, n, n, n, n$.
- **Young tableaux and symmetric functions.** The lemma proves the Jacobi-Trudi identity for Schur functions, and from it Aitken's determinant for the number of standard Young tableaux of a skew shape, see [counting standard Young tableaux](/counting-standard-young-tableaux/). Gessel and Viennot also derived [hook length formulas](/hook-length-formula/) for some shapes this way.
- **Cauchy-Binet.** For matrices $A$ of size $k \times m$ and $B$ of size $m \times k$, take a graph with layers $\{a_i\}$, $[m]$ and $\{b_j\}$, edges $a_i \to l$ of weight $A_{il}$ and $l \to b_j$ of weight $B_{lj}$. The lemma gives $\det(AB) = \sum_{S} \det A_{[k], S} \det B_{S, [k]}$ over the $k$-subsets $S$ of $[m]$.
- **Algorithms.** A count of nonintersecting families becomes a $k \times k$ determinant: $O(k^3)$ operations modulo a prime with Gaussian elimination, or exactly with the [Bareiss algorithm](/bareiss-algorithm/), whose intermediate numbers stay as small as the minors.

## Tightness

- **Compatibility is needed for the corollary.** Take sources $a_1, a_2$, sinks $b_1, b_2$ and the four edges $a_i \to b_j$. Both the identity and the swap give a nonintersecting system, so there are 2 families, but $\det M = 1 \cdot 1 - 1 \cdot 1 = 0$. Without compatibility the lemma gives only the signed count.
- **Vertex-disjoint, not edge-disjoint.** The involution needs a shared vertex. Families of edge-disjoint paths that share vertices are not counted by the determinant.
- **Acyclic graphs.** The proof uses that a path does not repeat a vertex and that the path sums are finite. For graphs with cycles, Fomin gave a version with loop-erased walks.
- **Sources equal to sinks.** If $a_i = b_j$ for some $i, j$, a one-vertex path is allowed and it blocks that vertex for the others. This is consistent with the lemma, as the Catalan example shows with $a_0 = b_0$.

## History

Karlin and McGregor proved the probabilistic form in 1959: for a strong Markov process with continuous paths, the probability that $k$ particles never meet is a determinant of transition probabilities. Lindström proved the lemma for acyclic graphs in 1973, in a paper on matroids. Gessel and Viennot found it independently and made it a standard tool of enumeration in their 1985 paper, with binomial determinants and hook length formulas as applications. The name records these three authors.

## References
