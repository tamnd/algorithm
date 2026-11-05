---
tag: PNZ7QC
kind: theorem
slug: fractional-cascading-lower-bound
name: Chazelle-Liu lower bound for fractional cascading
aliases:
- Chazelle-Liu lower bound
area: searching/fractional-cascading
level: research
summary: Lower bounds on space and query time for intersection searching and fractional cascading in higher dimensions, showing the savings cannot be unbounded.
model: pointer-machine
history:
  year: 2001
  people: [Bernard Chazelle, Ding Liu]
  note: Presented at STOC 2001 and published in the Journal of Computer and System Sciences in 2004.
prereqs: [catalog-graph, fractional-cascading-bridge, pointer-machine, planar-point-location]
see_also: [multiple-list-search, dynamic-fractional-cascading, range-searching-lower-bound, planar-subdivision, hive-graph, kirkpatrick-point-location]
sources:
  - paper: doi:10.1016/j.jcss.2003.07.003
    title: Bernard Chazelle and Ding Liu, Lower bounds for intersection searching and fractional cascading in higher dimension, Journal of Computer and System Sciences 68(2) (2004)
    locator: pages 269 to 284; Section 2 (Definitions 2.1 and 2.2, Lemma 2.3), Section 3 (Theorem 3.1 and Facts 3.3 to 3.5), Section 4 (Theorem 4.1)
  - paper: "Bernard Chazelle and Burton Rosenberg, Simplex range reporting on a pointer machine, Computational Geometry: Theory and Applications 5 (1996)"
    locator: pages 237 to 247 (the volume argument behind Lemma 2.3)
  - paper: "Bernard Chazelle, Lower bounds for orthogonal range searching I, The reporting case, Journal of the ACM 37 (1990)"
    locator: pages 200 to 212 (the pointer machine model for reporting and the first form of the volume argument)
  - paper: doi:10.1007/BF01840440
    title: Bernard Chazelle and Leonidas J. Guibas, Fractional cascading I, A data structuring technique, Algorithmica 1 (1986)
    locator: pages 133 to 162 (the one-dimensional technique that the theorem shows cannot be extended)
---

The Chazelle-Liu lower bound says that [fractional cascading](/fractional-cascading-bridge/) has no general version for planar maps: there is a path of planar subdivisions such that any [pointer machine](/pointer-machine/) structure that locates one query point in all $k$ of them in $O(k + \operatorname{polylog} n)$ time needs $n^2 / \operatorname{polylog} n$ space. With sorted lists as catalogs, the same query takes $O(\log n + k)$ time with $O(n)$ space. Chazelle and Liu proved the bound in 2001 by a reduction from line intersection searching, and their counterexample uses only subdivisions into parallel strips.

## Statement

**The model.** A search structure for a set $S$ of objects is a directed graph of bounded out-degree, the [pointer machine](/pointer-machine/) model of Tarjan. Some nodes are assigned objects of $S$. A query starts at a fixed node and follows edges; it is answered when the set of visited nodes contains, for each object of the answer, a node assigned to that object. The query cost is the number of visited nodes, and the size of the structure is its number of nodes. This charges the structure nothing for computation, so a lower bound in the model is strong.

**2D catalogs.** A path $v_1 v_2 \cdots v_L$ in which each vertex $v_s$ holds a planar subdivision $P_s$ is a [catalog graph](/catalog-graph/) with planar catalogs. A query is a point $q$ and a connected subgraph $H$, and its answer is the face of $P_s$ that contains $q$, for each vertex $v_s$ of $H$. The size $n$ is the total number of edges of all the subdivisions.

**Theorem (Chazelle and Liu, Theorem 4.1 in the journal version).** Let $\omega \ge 2$ with $\omega \le \sqrt{n}/2$, and let $a$ be a positive constant. There is a path of $L = \lceil \omega \rceil$ vertices whose catalogs are subdivisions of the plane into parallel strips, of total size $\Theta(n)$, with this property. If $\omega$ is larger than a constant that depends on $a$, then each pointer machine structure that answers every query $(q, H)$ with $H$ the whole path by visiting at most $a(L + \omega)$ nodes has
$$\Omega\!\left(\frac{n^2}{\omega^2}\right)$$
nodes. In particular, a query time of $O(k + \log^c n)$ for queries with $k$ vertices, for a constant $c$, needs $\Omega(n^2 / \log^{2c} n)$ space.

## In plain words

With sorted lists, a few copied items let a search jump from one list to the next in one step. The question was whether the same trick works when each list is replaced by a map of the plane, and the search asks which region of each map contains a point.

The answer is no. Chazelle and Liu build a short chain of maps, each a set of parallel stripes at a different slant. Many query points cross the stripes in patterns that share almost nothing: two of them never fall in the same pair of stripes. A pointer-based structure that answers each query fast must store, for each query, a nearly private route through its memory, and with this many different patterns the memory has to be close to the square of the input size. Searching each map on its own needs only linear memory but loses the speed-up.

## Proof

The proof has three steps: a general lemma on pointer machines, a hard set of segments and lines, and a duality that turns lines into points and segments into strips.

**Step 1: the volume lemma.** For a set $S$ of objects and a set $Q$ of queries, where each query $q$ selects a subset $S \cap q$:

- a search structure is $(a, \omega)$-*effective* if every query visits at most $a(|S \cap q| + \omega)$ nodes (Definition 2.1);
- $Q$ is $(m, \omega)$-*favorable* if $|S \cap q| \ge \omega$ for each $q \in Q$ (relevance) and $|S \cap q_1 \cap \cdots \cap q_m| = O(1)$ for any $m$ distinct queries (independence) (Definition 2.2).

*Lemma 2.3.* If a search structure for $S$ is $(a, \omega)$-effective for a constant $a$, and $Q$ is $(m, \omega)$-favorable, then for $\omega$ large enough the structure has $\Omega(|Q|\,\omega / m)$ nodes.

This lemma is the volume argument of Chazelle (1990) and Chazelle and Rosenberg (1996), and we use it as stated. *Idea (a sketch, not a proof):* the nodes visited by one query form a connected part of the structure of size $O(|S \cap q|)$ that reaches all of $S \cap q$. The proof cuts these parts into small connected pieces, each of which reaches many objects of one answer. By independence, a piece that reaches more than a constant number of objects can lie in the parts of fewer than $m$ queries. So the pieces of different queries are mostly distinct, and counting them gives $\Omega(|Q|\,\omega / m)$ nodes.

**Step 2: a hard set of segments (Section 3).** Let $L = \lceil \omega \rceil$ and $t = \lceil n / \omega \rceil$. Place $L$ vertical segments of the same length at the $x$-coordinates $x_s = -s$ for $s = 1, \ldots, L$, from $y = 0$ to $y = t$, and cut each into the $t$ unit subsegments $[r-1, r]$ for $r = 1, \ldots, t$. The midpoint of subsegment $r$ of segment $s$ is $(x_s, r - \tfrac12)$. In total there are $Lt = \Theta(n)$ subsegments. For $i, j \in \{1, \ldots, t\}$, let $\ell_{ij}$ be the line through the midpoint of subsegment $i$ of segment 1 and the midpoint of subsegment $j$ of segment 2. At segment $s$ it passes through the height
$$y_s = \bigl(i + (s-1)(j - i)\bigr) - \tfrac12,$$
because the segments are equally spaced. Call $\ell_{ij}$ *hitting* if $1 \le i + (L-1)(j-i) \le t$.

- *Fact A (Fact 3.3).* A hitting line crosses each of the $L$ segments at the midpoint of a subsegment. *Proof.* The value $r_s = i + (s-1)(j-i)$ is an integer, and it is a linear function of $s$, so it lies between $r_1 = i$ and $r_L$. Both are in $[1, t]$, so each $r_s$ is in $[1, t]$, and $y_s = r_s - \tfrac12$ is the midpoint of subsegment $r_s$. $\square$
- *Fact B (Fact 3.4).* There are $\Omega(n^2 / \omega^3)$ hitting lines. *Proof.* For fixed $i$, the line is hitting when $d = j - i$ lies in the interval $[(1-i)/(L-1), (t-i)/(L-1)]$ of length $(t-1)/(L-1)$. The bound $\omega \le \sqrt n / 2$ gives $t - 1 \ge L - 1$, so the interval holds at least $\lfloor (t-1)/(L-1) \rfloor \ge (t-1)/(2(L-1))$ integers, and each gives a $j = i + d \in [1, t]$ by Fact A with $s = 2$. Over the $t$ choices of $i$ this gives at least $t(t-1)/(2(L-1)) = \Omega(n^2/\omega^3)$ distinct lines. $\square$
- *Fact C (Fact 3.5).* Let the canonical subset of a hitting line be the set of subsegments it crosses. It has exactly $L$ elements, and two distinct hitting lines share at most one subsegment. *Proof.* By Fact A, a hitting line crosses each segment in exactly one subsegment, at its midpoint. If two lines share two subsegments, they pass through the same two midpoints, so they are equal. $\square$

Let $S$ be the set of subsegments and $Q$ the set of hitting lines, where a line selects its canonical subset. Then $|S \cap q| = L \ge \omega$, and any two queries share at most one object, so $Q$ is $(2, \omega)$-favorable.

**Step 3: duality (Section 4).** Map the line $y = \alpha x + \beta$ to the point $(\alpha, \beta)$. The line crosses subsegment $r$ of segment $s$ exactly when $r - 1 \le \alpha x_s + \beta \le r$, that is, when the point $(\alpha, \beta)$ lies in the closed strip between the parallel lines $\beta = -x_s \alpha + r - 1$ and $\beta = -x_s \alpha + r$. For each $s$, these $t + 1$ lines cut the plane into a subdivision $P_s$ of $t$ strips and two half-planes. Put $P_s$ at vertex $v_s$ of a path. The total size is $\Theta(Lt) = \Theta(n)$.

For a hitting line $\ell$ with dual point $q$, the face of $P_s$ that contains $q$ is the strip of the subsegment that $\ell$ crosses on segment $s$, by Fact A. So the answer to the 2D catalog query $(q, \text{whole path})$ is the canonical subset of $\ell$, one strip per vertex. A structure for the 2D catalog query is therefore a search structure for $(S, Q)$, with $k = L = |S \cap q|$ answers. If it visits at most $a(L + \omega)$ nodes, it is $(a, \omega)$-effective. By Lemma 2.3 and Fact B, it has
$$\Omega\!\left(\frac{|Q|\,\omega}{2}\right) = \Omega\!\left(\frac{n^2}{\omega^3} \cdot \omega\right) = \Omega\!\left(\frac{n^2}{\omega^2}\right)$$
nodes. For the last claim, a query time of at most $a'(k + \log^c n)$ is at most $a'(L + \omega)$ with $\omega = \log^c n$, which gives $\Omega(n^2/\log^{2c} n)$. $\blacksquare$

**A small instance.** With $L = 4$ segments and $t = 8$ subsegments each, there are 32 subsegments and 22 hitting lines, and no two of them share two subsegments.

## Consequences

- **No 2D fractional cascading.** The one-dimensional technique of Chazelle and Guibas gives $O(\log n + k)$ time with $O(n)$ space on a [catalog graph](/catalog-graph/) of bounded degree. For planar catalogs, no structure with $n^2/\operatorname{polylog} n$ space or less has query time $O(k + \operatorname{polylog} n)$ on every catalog graph. Separate [planar point location](/planar-point-location/) at each vertex gives $O(k \log n)$ time with $O(n)$ space.
- **Line intersection searching.** The same construction, made into a convex subdivision with thin strips, gives Theorem 3.1: reporting the $k$ edges of an $n$-vertex planar subdivision crossed by a query line in $O(k + \omega)$ time needs $\Omega(n^2/\omega^2)$ space. An extension gives Theorem 3.2 for a query plane and the edges of a convex polytope in three dimensions.
- **The Dobkin-Kirkpatrick hierarchy.** Chazelle and Liu also show that some convex polytope has no Dobkin-Kirkpatrick hierarchy that is boundary dominant, which was an open question since the mid-1980s. It is the polytope analogue of the hierarchy behind [Kirkpatrick point location](/kirkpatrick-point-location/).
- **Special catalog graphs remain possible.** The bound is for a worst-case family. Some special planar settings, such as navigation among geodesic triangles in a simple polygon, behave like 2D fractional cascading, and the [hive graph](/hive-graph/) is a planar structure with the speed-up for one fixed problem.

## Tightness

The bound is tight up to the polylogarithmic factor for the instance of the proof. A query point $q = (\alpha, \beta)$ is the dual of the line $y = \alpha x + \beta$, and the strip of $P_s$ that contains $q$ is the subsegment of segment $s$ that this line crosses. Chazelle and Liu note that $O(n^2)$ space suffices to report the $k$ edges of a planar subdivision crossed by a query line in $O(k + \log n)$ time, by the filtering search of Chazelle (1986). Applied to the subsegments, this reports the strips that contain $q$. For each vertex whose segment the line misses, one evaluation of $\alpha x_s + \beta$ tells which of the two half-planes holds $q$. So all $L$ answers cost $O(\log n + L)$ time with $O(n^2)$ space. The other end of the trade-off is separate point location at each vertex, with $O(n)$ space and $O(L \log n)$ time.

Chazelle and Liu also remark that the lower bound holds, up to a factor $n^{\epsilon}$, when the polylogarithmic term in the query time is replaced by $n^{\delta}$ for small enough $\delta, \epsilon > 0$.

## History

Chazelle and Guibas introduced fractional cascading in 1986, and the extension to planar maps was an open problem from then on. Chazelle and Liu presented the lower bound at STOC 2001 and published the journal version in 2004. The proof uses the volume argument for pointer machines from the earlier range searching lower bounds of Chazelle (1990) and Chazelle and Rosenberg (1996).

## References
