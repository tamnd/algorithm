---
tag: ZES8KF
kind: theorem
slug: four-point-condition
name: Four-point condition
aliases:
- Buneman's theorem
- four-point theorem
area: biology/phylogenetics
level: core
summary: A metric is a tree metric exactly when, for every four points, the two largest of the three pair sums are equal. The tree is then unique.
prereqs: [tree-metric]
see_also: [four-point-method, additive-tree-reconstruction, ultrametric, quartet, splits-of-a-tree, neighbor-joining, split-decomposition, metric-tree-embedding]
sources:
  - paper: doi:10.1016/0095-8956(74)90047-1
    title: Peter Buneman, A note on the metric properties of trees, Journal of Combinatorial Theory, Series B 17(1), 1974, pages 48 to 50
    locator: the theorem that a metric is a tree metric if and only if it satisfies the four-point condition
  - paper: "Peter Buneman, The recovery of trees from measures of dissimilarity, in F. R. Hodson, D. G. Kendall and P. Tautu (eds), Mathematics in the Archaeological and Historical Sciences, Edinburgh University Press, 1971"
    title: Buneman 1971
    locator: pages 387 to 395, the four-point condition and the uniqueness of the tree
  - paper: "K. A. Zaretskii, Constructing a tree on the basis of a set of distances between the hanging vertices, Uspekhi Matematicheskikh Nauk 20(6), 1965, in Russian"
    title: Zaretskii 1965
    locator: pages 90 to 92, the characterization of the leaf distances of a tree
  - paper: "J. M. S. Simões-Pereira, A note on the tree realizability of a distance matrix, Journal of Combinatorial Theory 6(3), 1969"
    title: Simões-Pereira 1969
    locator: pages 303 to 310, the conditions under which a distance matrix is realized by a tree, and its uniqueness
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, 2003
    locator: Section 7.2, Definition 7.2.1 (tree metric) and Theorem 7.2.6 (the tree-metric theorem)
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, 2004
    locator: Chapter 12, Quartets of species, the four-point metric condition
---

The four-point condition is a test on four points at a time that tells exactly which distance matrices come from trees. A metric $D$ on a finite set is a [tree metric](/tree-metric/), that is, the path-length distance between some vertices of a tree with positive edge lengths, if and only if for every four points the two largest of the three sums $D_{xy} + D_{zw}$, $D_{xz} + D_{yw}$, $D_{xw} + D_{yz}$ are equal. The tree is then unique once vertices of degree 2 outside the set are suppressed. Buneman proved the theorem in 1971 and 1974, after related results of Zaretskii (1965) and Simões-Pereira (1969).

## Statement

Let $X$ be a finite set and $D : X \times X \to \mathbb{R}$ a function with $D_{xx} = 0$, $D_{xy} = D_{yx}$ and $D_{xy} > 0$ for $x \ne y$. A **realization** of $D$ is a tree $T$ with $X \subseteq V(T)$ and a positive length on each edge, such that $D_{xy}$ is the length of the path from $x$ to $y$ for all $x, y \in X$, and every vertex not in $X$ has degree at least 3. Two realizations are **equivalent** if a graph isomorphism between them fixes each element of $X$ and keeps edge lengths. $D$ satisfies the **four-point condition** if

$$D_{xy} + D_{zw} \le \max\bigl(D_{xz} + D_{yw},\ D_{xw} + D_{yz}\bigr) \qquad \text{for all } x, y, z, w \in X,$$

not necessarily distinct. Equivalently, among the three sums $D_{xy} + D_{zw}$, $D_{xz} + D_{yw}$ and $D_{xw} + D_{yz}$ the two largest are equal.

**Theorem.** $D$ has a realization if and only if $D$ satisfies the four-point condition. The realization is then unique up to equivalence.

With repeated points the condition says nothing new except the triangle inequality: for $w = z$ it reads $D_{xy} \le D_{xz} + D_{yz}$, and every other pattern of repeats makes it trivial. So for a [metric](/metric-space/) it is enough to test the $\binom{|X|}{4}$ sets of four distinct points.

For example, the matrix on A to E below is the leaf metric of the tree `((A:2,B:7):1,E:5,(C:3,D:6):2);`. Its five quartets give the sums $(18, 24, 24)$ for ABCD, $(19, 21, 21)$ for ABCE, $(22, 24, 24)$ for ABDE, $(21, 21, 17)$ for ACDE and $(26, 26, 22)$ for BCDE, listed as $D_{xy} + D_{zw}$, $D_{xz} + D_{yw}$, $D_{xw} + D_{yz}$ in alphabetical order. In each the two largest are equal, and the smallest names the split of the quartet in the tree; for ABCD it is $D_{AB} + D_{CD} = 18$, so the tree separates A, B from C, D.

| | A | B | C | D | E |
|---|---|---|---|---|---|
| A | 0 | 9 | 8 | 11 | 8 |
| B | 9 | 0 | 13 | 16 | 13 |
| C | 8 | 13 | 0 | 9 | 10 |
| D | 11 | 16 | 9 | 0 | 13 |
| E | 8 | 13 | 10 | 13 | 0 |

## In plain words

Take four species and pair them up in the three possible ways. For each pairing, add the two distances inside the pairs. If the distances come from a tree, the pairing that matches the tree gives the smallest total, and the other two pairings give the same larger total, because both of them use the middle branch of the four species twice. The theorem says that the converse also holds. If every group of four behaves like this, then there is a tree with branch lengths that gives exactly these distances, and there is only one such tree.

## Proof

Write $d$ for path length in a tree, and $[u, v]$ for the path between vertices $u$ and $v$.

**Necessity.** Let $T$ realize $D$ and let $x, y, z, w \in X$. In a tree the intersection of two paths is empty or a path. *Case 1:* $[x, y]$ and $[z, w]$ have no common vertex. Let $[u, v]$ be the shortest path from a vertex $u$ of $[x, y]$ to a vertex $v$ of $[z, w]$, of length $\delta > 0$. Then $D_{xz} = d(x, u) + \delta + d(v, z)$, and similarly for the other crossing pairs, so
$$D_{xz} + D_{yw} = D_{xw} + D_{yz} = D_{xy} + D_{zw} + 2\delta.$$
*Case 2:* the paths share the path $[u, v]$, with $u$ closer to $x$ than $v$ on $[x, y]$; swapping the names $z$ and $w$ if needed, $u$ is also closer to $z$ on $[z, w]$. The pieces $[x, u]$, $[u, v]$, $[v, w]$ meet only at their ends, so $D_{xw} = d(x, u) + d(u, v) + d(v, w)$; in the same way $D_{yz} = d(y, v) + d(v, u) + d(u, z)$, $D_{xz} = d(x, u) + d(u, z)$ and $D_{yw} = d(y, v) + d(v, w)$. Hence
$$D_{xy} + D_{zw} = D_{xw} + D_{yz} = D_{xz} + D_{yw} + 2\, d(u, v).$$
In both cases the two largest sums are equal.

**Sufficiency.** We induct on $|X|$. For $|X| = 1$ the realization is one vertex, and for $|X| = 2$ it is one edge of length $D_{xy}$. Let $|X| \ge 3$, pick $x \in X$, let $X' = X \setminus \{x\}$, and let $T'$ realize $D$ on $X'$, which exists by induction since the condition holds on $X'$. For $y, z \in X'$ put
$$h_{yz} = \tfrac{1}{2}\bigl(D_{xy} + D_{xz} - D_{yz}\bigr) \ge 0,$$
where $h_{yz} \ge 0$ is the triangle inequality. Choose $y \ne z$ in $X'$ with $h = h_{yz}$ smallest. Let $a = D_{xy} - h$; then $0 \le a \le D_{yz}$ by the triangle inequality, and we let $p$ be the point of $[y, z]$ in $T'$ at distance $a$ from $y$, so at distance $D_{xz} - h$ from $z$. Attach $x$ at $p$ by a new edge of length $h$, subdividing an edge of $T'$ if $p$ is inside one; if $h = 0$, $x$ becomes the point $p$ itself.

*Claim: $d(x, w) = D_{xw}$ for every $w \in X'$.* For $w \in \{y, z\}$ this holds by the choice of $a$. Otherwise let $m$ be the vertex of $[y, z]$ closest to $w$, and put $\alpha = d(y, m)$, $\beta = d(z, m)$, $\gamma = d(w, m)$, so $D_{yz} = \alpha + \beta$, $D_{yw} = \alpha + \gamma$ and $D_{zw} = \beta + \gamma$. Swapping $y$ and $z$ if needed, $p$ lies on $[m, z]$, at distance $t \ge 0$ from $m$; then $D_{xy} = \alpha + t + h$, $D_{xz} = \beta - t + h$, and in the new tree $d(x, w) = h + t + \gamma$. Consider
$$S_1 = D_{xw} + D_{yz}, \qquad S_2 = D_{xy} + D_{zw} = \alpha + \beta + \gamma + h + t, \qquad S_3 = D_{xz} + D_{yw} = \alpha + \beta + \gamma + h - t.$$
So $S_2 \ge S_3$. The choice of $h$ gives $h \le h_{zw} = \frac{1}{2}(D_{xz} + D_{xw} - D_{zw})$, that is $D_{xw} \ge 2h - (\beta - t + h) + \beta + \gamma = h + t + \gamma$, so $S_1 \ge S_2$. The four-point condition for $x, w, y, z$ gives $S_1 \le \max(S_2, S_3) = S_2$. So $S_1 = S_2$, which is $D_{xw} = h + t + \gamma = d(x, w)$.

*The result is a realization.* If $h = 0$ and $p$ were a vertex $q \in X'$, the claim would give $D_{xq} = 0$, which is excluded. So either $h > 0$, and the new vertex $p$ (if $p$ was inside an edge) has degree 3, or $h = 0$ and $x$ is a new vertex of degree 2 inside an edge or takes the place of a vertex not in $X'$. In all cases every vertex not in $X$ keeps degree at least 3, and all edge lengths are positive.

**Uniqueness.** Let $T$ realize $D$. A leaf of $T$ has degree 1, so it is in $X$. If $v \notin X$, then $v$ has at least three neighbors, and beyond each of them there is a leaf, so $v$ is the **median** of three elements $x, y, z \in X$: the common vertex of $[x, y]$, $[x, z]$ and $[y, z]$, with $d(x, v) = \frac{1}{2}(D_{xy} + D_{xz} - D_{yz})$. Call a triple $(x, y, s)$ with $x, y \in X$ and $0 \le s \le D_{xy}$ an **address**; in $T$ it names the point $\pi_T(x, y, s)$ of $[x, y]$ at distance $s$ from $x$. Every vertex has an address: $(x, x, 0)$ for $x \in X$, and $(x, y, d(x, v))$ for a median $v$.

The distance between two addressed points is a function of $D$ alone. Let $u$ be any vertex and $f(w) = d(u, w)$ for $w \in X$. The path from $u$ meets $[x', y']$ first at the point $q$ with $d(u, q) = \frac{1}{2}(f(x') + f(y') - D_{x'y'})$ and $d(x', q) = \frac{1}{2}(f(x') + D_{x'y'} - f(y'))$, so
$$d\bigl(u, \pi_T(x', y', s')\bigr) = \tfrac{1}{2}\bigl(f(x') + f(y') - D_{x'y'}\bigr) + \Bigl|\, s' - \tfrac{1}{2}\bigl(f(x') + D_{x'y'} - f(y')\bigr) \Bigr|.$$
Applying this with $u \in X$ shows that $f$ for $u = \pi_T(x, y, s)$ is a function of $D$ and the address, and applying it again gives $d(\pi_T(x, y, s), \pi_T(x', y', s'))$ as a function of $D$ and the two addresses.

Now let $T_1$ and $T_2$ both realize $D$. For a vertex $v$ of $T_1$ with address $\alpha$, put $\varphi(v) = \pi_{T_2}(\alpha)$. If $v$ has two addresses, their points in $T_2$ are at distance $d_{T_1}(v, v) = 0$, so $\varphi$ is well defined, and $d_{T_2}(\varphi(u), \varphi(v)) = d_{T_1}(u, v)$ for all vertices. A median in $T_1$ of $x, y, z$ has the address $(x, y, \frac{1}{2}(D_{xy} + D_{xz} - D_{yz}))$, which names the median of $x, y, z$ in $T_2$; a median is in $X$ or has three directions, so it is a vertex. So $\varphi$ maps vertices to vertices, fixes $X$, and keeps distances, so it is injective; by symmetry there is such a map $\psi$ from $T_2$ to $T_1$. The vertex $\psi(\varphi(v))$ has the same distances to all of $X$ as $v$, and a vertex is fixed by its distances to $x, y$ with $d(x, v) + d(v, y) = D_{xy}$, so $\psi \circ \varphi$ is the identity, and likewise $\varphi \circ \psi$. Finally $u$ and $v$ are adjacent exactly when no third vertex $w$ has $d(u, w) + d(w, v) = d(u, v)$, so $\varphi$ keeps edges and their lengths. $\blacksquare$

## Consequences

- **Reconstruction.** The sufficiency proof is an algorithm: add the points one at a time and attach each at the point found from the smallest $h_{yz}$. The [four-point method](/four-point-method/) finds the attachment edge with $O(1)$ quartet tests per node of a walk, in $O(n^2)$ time in total. [Neighbor-joining](/neighbor-joining/) is also exact on tree metrics. See [additive tree reconstruction](/additive-tree-reconstruction/).
- **Quartets and splits.** On a tree metric of a binary tree the strictly smallest sum of each quartet names its split, so the metric determines all [quartets](/quartet/) and hence all [splits](/splits-of-a-tree/) of the tree.
- **Ultrametrics.** Every [ultrametric](/ultrametric/) satisfies the four-point condition, so it is a tree metric; its realization has a root at equal distance from all points of $X$.
- **The Gromov form.** Fix $r \in X$ and put $(x \mid y)_r = \frac{1}{2}(D_{rx} + D_{ry} - D_{xy})$. The condition for the four points $r, x, y, z$ is $(x \mid z)_r \ge \min\bigl((x \mid y)_r, (y \mid z)_r\bigr)$, the min form of the three-point condition. This links tree metrics to ultrametrics; see the Farris transform on the page on [additive tree reconstruction](/additive-tree-reconstruction/).
- **Testing.** Checking all quartets takes $O(n^4)$ time; building a candidate tree and comparing its leaf metric with $D$ takes $O(n^2)$.

## Tightness

- **Equality is needed, not just an inequality.** The 4-cycle with unit edges, $D_{12} = D_{23} = D_{34} = D_{41} = 1$ and $D_{13} = D_{24} = 2$, is a metric. Its sums are $D_{12} + D_{34} = 2$, $D_{13} + D_{24} = 4$ and $D_{14} + D_{23} = 2$, so the largest is alone and no tree realizes it.
- **Three points are not enough.** Every metric on three points is a tree metric, the star with edge lengths $\frac{1}{2}(D_{xy} + D_{xz} - D_{yz})$, so no condition on triples alone can characterize tree metrics.
- **The degree condition is needed for uniqueness.** Without it, subdividing an edge or adding a pendant path to a new unlabeled vertex gives other trees with the same distances on $X$. Zero-length edges likewise allow contracting or expanding a vertex.
- **Approximate versions.** If every quartet satisfies the condition up to an additive $2\delta$, the metric is close to a tree metric in a quantitative sense; this is Gromov's notion of a $\delta$-hyperbolic metric. With $\delta > 0$ the tree is no longer unique.

## History

Zaretskii (1965) characterized the distances between the leaves of a tree, and Simões-Pereira (1969) gave conditions for a distance matrix to be realized by a tree and studied uniqueness. Buneman (1971) stated the four-point condition for the recovery of trees from dissimilarities, and in 1974 published the short proof that a metric is a tree metric exactly when it satisfies the condition. The condition is the base of distance-based and quartet-based phylogenetics, and in metric geometry the four-point condition with an additive error defines Gromov hyperbolicity.

## References
