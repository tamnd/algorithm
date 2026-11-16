---
tag: SG2YSF
kind: theorem
slug: nemhauser-trotter-theorem
name: Nemhauser-Trotter theorem
aliases:
- Nemhauser-Trotter kernel
area: complexity/parameterized-complexity
level: advanced
summary: "The vertex cover LP has a half-integral optimum, and some least cover takes every vertex of value 1 and none of value 0. This gives a kernel with at most 2k vertices."
prereqs: [parameterized-vertex-cover, lp-relaxation, half-integrality]
see_also: [crown-reduction, lp-kernelization, kernelization, bipartite-double-cover, konig-theorem, lp-rounding-vertex-cover, vertex-cover-2-approximation, buss-kernel]
sources:
  - paper: doi:10.1007/BF01580444
    title: "George L. Nemhauser and Leslie E. Trotter Jr., Vertex packings: structural properties and algorithms, Mathematical Programming 8, 232-248 (1975)"
    locator: the persistence result for the LP relaxation of vertex packing (vertex cover is the complement)
  - paper: doi:10.1007/BF01580222
    title: "George L. Nemhauser and Leslie E. Trotter Jr., Properties of vertex packing and independence system polyhedra, Mathematical Programming 6, 48-61 (1974)"
    locator: the extreme points of the fractional vertex packing polytope are half-integral
  - paper: doi:10.1006/jagm.2001.1186
    title: "Jianer Chen, Iyad A. Kanj and Weijia Jia, Vertex cover: further observations and further improvements, Journal of Algorithms 41(2), 280-301 (2001)"
    locator: the kernel with at most 2k vertices from the Nemhauser-Trotter theorem
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 2, Kernelization (the LP-based kernel for vertex cover and the proof for an arbitrary optimal solution)
  - book: isbn:9781107057760
    title: Fedor V. Fomin, Daniel Lokshtanov, Saket Saurabh and Meirav Zehavi, Kernelization, Theory of Parameterized Preprocessing, Cambridge University Press, 2019
    locator: Section 6.1, The theorem of Nemhauser and Trotter
  - paper: doi:10.1145/2566616
    title: "Daniel Lokshtanov, N. S. Narayanaswamy, Venkatesh Raman, M. S. Ramanujan and Saket Saurabh, Faster parameterized algorithms using linear programming, ACM Transactions on Algorithms 11(2), article 15 (2014)"
    locator: a kernel for vertex cover with at most 2k - c log k vertices
---

The Nemhauser-Trotter theorem is a structural fact about the [LP relaxation](/lp-relaxation/) of [vertex cover](/parameterized-vertex-cover/). The relaxation has an optimal solution with all values in $\{0, \tfrac12, 1\}$, and for any optimal solution there is a least vertex cover that contains every vertex with value above $\tfrac12$ and no vertex with value below $\tfrac12$. In [kernelization](/kernelization/) it gives a kernel for vertex cover, with the cover size $k$ as the parameter, that has at most $2k$ vertices. Nemhauser and Trotter proved it for vertex packing, which is independent set, the complement of vertex cover.

## Statement

Let $G = (V, E)$ be a graph. The LP relaxation of vertex cover is

$$\mathrm{LP}(G):\quad \min \sum_{v \in V} x_v \quad \text{subject to}\quad x_u + x_v \ge 1 \text{ for each edge } uv,\qquad x_v \ge 0 \text{ for each } v.$$

Write $\mathrm{lp}(G)$ for its optimal value and $\mathrm{vc}(G)$ for the size of a least vertex cover. Every cover gives a feasible 0/1 solution, so $\mathrm{lp}(G) \le \mathrm{vc}(G)$.

**Theorem.**

1. *(Half-integrality.)* Every extreme point of the feasible region of $\mathrm{LP}(G)$ has all values in $\{0, \tfrac12, 1\}$. So $\mathrm{LP}(G)$ has a half-integral optimal solution.
2. *(Persistence.)* Let $x$ be any optimal solution, and let $V_0 = \{v : x_v < \tfrac12\}$, $V_{1/2} = \{v : x_v = \tfrac12\}$ and $V_1 = \{v : x_v > \tfrac12\}$. Then some least vertex cover $S$ of $G$ satisfies $V_1 \subseteq S \subseteq V_1 \cup V_{1/2}$.
3. *(Kernel.)* With $x$ half-integral and $k' = k - |V_1|$, the graph $G$ has a vertex cover of size at most $k$ if and only if $G[V_{1/2}]$ has one of size at most $k'$. If this holds, then $|V_{1/2}| \le 2k'$.

A half-integral optimal solution can be computed in time $O(m \sqrt{n})$ with a bipartite matching, as shown below. So part 3 gives a kernel with at most $2k$ vertices.

## In plain words

You want the fewest guards on the points of a network so that every line has a guard at one end. Now allow half a guard on a point. Two halves cover a line, and so do a whole guard and nothing. The best plan with halves is easy to compute, and it never costs more than the real answer.

The theorem says two things about that easy plan. First, the best plan only ever needs nothing, a half or a whole guard on each point. Second, it does not lie about the whole guards and the empty points: some real best plan puts a guard on every point that got a whole guard and on no point that got nothing. Only the points with halves stay open, and there cannot be more than twice as many of them as the guards you still have.

## Proof

**Part 1.** Let $x$ be feasible and not half-integral. If some $x_v > 1$, then $x \pm \varepsilon e_v$ are both feasible for small $\varepsilon > 0$, so $x$ is not an extreme point. Assume all values are in $[0, 1]$, and let $V^+ = \{v : 0 < x_v < \tfrac12\}$ and $V^- = \{v : \tfrac12 < x_v < 1\}$. One of them is nonempty. For $\varepsilon > 0$ define $x^{+}$ by adding $\varepsilon$ on $V^+$ and subtracting $\varepsilon$ on $V^-$, and $x^{-}$ by the opposite changes. Then $x = \tfrac12 (x^+ + x^-)$ and $x^+ \ne x^-$.

Both are feasible for small $\varepsilon$. The values on $V^+ \cup V^-$ are strictly between 0 and 1, so nonnegativity holds. An edge with $x_u + x_v > 1$ has slack, and a small $\varepsilon$ keeps it. Let $x_u + x_v = 1$. If $u \in V^+$, then $x_v = 1 - x_u \in (\tfrac12, 1)$, so $v \in V^-$, and the two changes cancel. The case $u \in V^-$ is the same. Otherwise neither endpoint is in $V^+ \cup V^-$, and neither value changes. So $x$ is the midpoint of two feasible points and is not an extreme point. The feasible region lies in $x \ge 0$, so it has extreme points, and the objective is bounded below by 0, so some extreme point is optimal.

**Part 2.** Let $S^*$ be a least vertex cover and let $S = (S^* \setminus V_0) \cup V_1$. Then $V_1 \subseteq S \subseteq V_1 \cup V_{1/2}$.

$S$ is a vertex cover. Take an edge $uv$. If $u \in V_0$, then $x_v \ge 1 - x_u > \tfrac12$, so $v \in V_1 \subseteq S$. If neither endpoint is in $V_0$, then the endpoint that $S^*$ contains is in $S^* \setminus V_0 \subseteq S$.

$|S| \le |S^*|$. Since $|S| = |S^*| - |S^* \cap V_0| + |V_1 \setminus S^*|$, it suffices to show $|V_1 \setminus S^*| \le |S^* \cap V_0|$. Assume the opposite. Let $\varepsilon > 0$ be at most $|x_v - \tfrac12|$ for every $v \in V_0 \cup V_1$. Define $y$ by $y_v = x_v - \varepsilon$ for $v \in V_1 \setminus S^*$, $y_v = x_v + \varepsilon$ for $v \in V_0 \cap S^*$, and $y_v = x_v$ otherwise. Then $\sum y_v < \sum x_v$. We show that $y$ is feasible, which contradicts the optimality of $x$.

Values only drop on $V_1 \setminus S^*$, and there they stay at least $\tfrac12$, so $y \ge 0$. Take an edge $uv$ with $u \in V_1 \setminus S^*$; edges with no such endpoint do not lose value. Since $S^*$ covers $uv$ and $u \notin S^*$, we have $v \in S^*$, so $y_v \ge x_v$. If $v \in V_0$, then $v \in V_0 \cap S^*$ and $y_u + y_v = x_u + x_v \ge 1$. If $v \in V_{1/2} \cup V_1$, then $y_u \ge \tfrac12$ and $y_v = x_v \ge \tfrac12$. In each case the edge constraint holds. $\square$

**Part 3.** Let $S$ be the cover from part 2. Its part $S \cap V_{1/2}$ covers $G[V_{1/2}]$, so $\mathrm{vc}(G) = |S| \ge |V_1| + \mathrm{vc}(G[V_{1/2}])$. Conversely, let $T$ be a cover of $G[V_{1/2}]$. Every edge with an endpoint in $V_0$ has its other endpoint in $V_1$, as shown above, so $V_1 \cup T$ covers $G$. Hence $\mathrm{vc}(G) = |V_1| + \mathrm{vc}(G[V_{1/2}])$, and the two instances are equivalent. For the size bound, if $\mathrm{vc}(G) \le k$ then $|V_1| + \tfrac12 |V_{1/2}| = \mathrm{lp}(G) \le \mathrm{vc}(G) \le k$, so $|V_{1/2}| \le 2(k - |V_1|) = 2k'$. $\square$

**Computing a half-integral optimum.** Build the [bipartite double cover](/bipartite-double-cover/) $B$: two copies $v'$ and $v''$ of each vertex, and the edges $u'v''$ and $v'u''$ for each edge $uv$. Find a least vertex cover $Y$ of $B$ from a maximum matching by [König's theorem](/konig-theorem/), and set $x_v = \tfrac12 |Y \cap \{v', v''\}|$. For an edge $uv$, $Y$ covers $u'v''$ and $v'u''$, so $x_u + x_v \ge 1$. For any feasible $z$ of $\mathrm{LP}(G)$, putting $z_v$ on both copies of $v$ gives a fractional cover of $B$ of value $2 \sum z_v$. The LP of a bipartite graph has an integral optimum, so $|Y| \le 2\,\mathrm{lp}(G)$ and $\sum x_v = |Y|/2 \le \mathrm{lp}(G)$. So $x$ is optimal. With [Hopcroft-Karp](/hopcroft-karp/) this takes $O(m \sqrt{n})$ time.

## Consequences

- **A kernel with 2k vertices.** Compute $x$ by the double cover, return $(G[V_{1/2}], k - |V_1|)$, and answer NO if $|V_{1/2}| > 2(k - |V_1|)$. Chen, Kanj and Jia used this for the kernel with at most $2k$ vertices. It has $O(k^2)$ edges.
- **A crown.** If $V_0$ is nonempty for a half-integral optimum, then $V_0$, $V_1$ and $V_{1/2}$ form a crown decomposition. This links the theorem to [crown reduction](/crown-reduction/).
- **A 2-approximation.** $V_1 \cup V_{1/2}$ is a vertex cover of size at most $2\,\mathrm{lp}(G) \le 2\,\mathrm{vc}(G)$. See [LP rounding for vertex cover](/lp-rounding-vertex-cover/) and [half-integrality](/half-integrality/).
- **Parameters above the LP.** Since $\mathrm{lp}(G) \le \mathrm{vc}(G)$, the gap $k - \mathrm{lp}(G)$ is a smaller parameter than $k$. Lokshtanov, Narayanaswamy, Raman, Ramanujan and Saurabh solve vertex cover in time $O^*(2.3146^{k - \mathrm{lp}(G)})$, where $O^*$ hides factors polynomial in $n$. See [LP kernelization](/lp-kernelization/).

**Worked example.** The graph has a star with center 0 and leaves 1, 2 and 3, a triangle on 4, 5 and 6, and the edge 0-4. A scratch script computed $x$ with the double cover and got $x_0 = 1$, $x_1 = x_2 = x_3 = 0$ and $x_4 = x_5 = x_6 = \tfrac12$, with value $\tfrac52$. A search over all half-integral vectors gives the same LP value, and the least cover has 3 vertices. So $V_1 = \{0\}$ and $V_{1/2} = \{4, 5, 6\}$. For $k = 3$ the kernel is the triangle with $k' = 2$, a yes-instance. For $k = 2$ we get $k' = 1$ and $|V_{1/2}| = 3 > 2$, so the answer is NO at once. The script also checked parts 2 and 3 on 300 random graphs with up to 9 vertices (seed 7).

## Tightness

- **The bound 2k' is reached.** For a perfect matching on $2k$ vertices, the all-$\tfrac12$ vector is optimal with value $k$, and the double cover method returns it (the script confirms this for $k = 3$). So $V_{1/2}$ has all $2k$ vertices, the instance is a yes-instance with $\mathrm{vc} = k$, and the kernel keeps all of it. Lokshtanov et al. improve the kernel to $2k - c \log k$ vertices for a constant $c$, by more than this theorem.
- **"Some" cannot become "every".** For a single edge $uv$, the solution $x_u = 1$, $x_v = 0$ is optimal, but the least cover $\{v\}$ does not contain $V_1 = \{u\}$. Persistence holds for one least cover, not for all of them.
- **No integrality.** For a triangle the only optimal solution is all $\tfrac12$, with value $\tfrac32$, while the least cover has 2 vertices. The LP fixes no vertex, and the kernel keeps the whole triangle.
- **No analog for larger sets.** For [hitting set](/parameterized-hitting-set/) with sets of size $d \ge 3$, the LP with constraints $\sum_{v \in S} x_v \ge 1$ has no half-integral optimum in general, and this proof does not carry over. For the 7 lines of the Fano plane, each a set of 3 of its 7 points, the value $\tfrac13$ on every point is feasible with value $\tfrac73$, and summing the 7 constraints shows that no solution is smaller, because each point lies on 3 lines. A search over all half-integral vectors (a scratch run) finds the least value 3.

## History

Nemhauser and Trotter proved the half-integrality of the fractional vertex packing polytope in 1974 and the persistence result in 1975, in the language of vertex packing, which is maximum weight independent set. Since the complement of an independent set is a vertex cover, the results move to vertex cover directly, also with weights. Chen, Kanj and Jia (2001) observed that the theorem gives a kernel for vertex cover with at most $2k$ vertices. The proof of part 2 above, for an arbitrary optimal solution, follows the presentation of Cygan et al.

## References
