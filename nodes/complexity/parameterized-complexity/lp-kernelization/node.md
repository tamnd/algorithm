---
tag: 1VXMVM
kind: technique
slug: lp-kernelization
name: LP-based kernelization
aliases:
- linear programming kernel
area: complexity/parameterized-complexity
level: advanced
summary: "Solve the LP relaxation, fix the variables that some optimal solution shares with it, and bound what is left by the LP value. For vertex cover this gives a kernel with 2k vertices."
prereqs: [kernelization, nemhauser-trotter-theorem, lp-relaxation]
see_also: [crown-reduction, half-integrality, parameterized-vertex-cover, bipartite-double-cover, lossy-kernelization, odd-cycle-transversal, parameterized-hitting-set, polynomial-kernel]
sources:
  - book: isbn:9781107057760
    title: Fedor V. Fomin, Daniel Lokshtanov, Saket Saurabh and Meirav Zehavi, Kernelization, Theory of Parameterized Preprocessing, Cambridge University Press, 2019
    locator: Chapter 6, Linear programming (Section 6.1, The theorem of Nemhauser and Trotter)
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 2, Kernelization (the LP-based kernel for vertex cover), and Chapter 3, Bounded search trees (vertex cover above LP)
  - paper: doi:10.1007/BF01580444
    title: "George L. Nemhauser and Leslie E. Trotter Jr., Vertex packings: structural properties and algorithms, Mathematical Programming 8, 232-248 (1975)"
    locator: the persistence result that the kernel uses
  - paper: doi:10.1006/jagm.2001.1186
    title: "Jianer Chen, Iyad A. Kanj and Weijia Jia, Vertex cover: further observations and further improvements, Journal of Algorithms 41(2), 280-301 (2001)"
    locator: the kernel with at most 2k vertices
  - paper: doi:10.1145/2566616
    title: "Daniel Lokshtanov, N. S. Narayanaswamy, Venkatesh Raman, M. S. Ramanujan and Saket Saurabh, Faster parameterized algorithms using linear programming, ACM Transactions on Algorithms 11(2), article 15 (2014)"
    locator: vertex cover above LP in O*(2.3146^k), the same bound for above guarantee vertex cover, odd cycle transversal and Almost 2-SAT, and a kernel with 2k - c log k vertices
---

LP-based kernelization builds a [kernel](/kernel/) from the [LP relaxation](/lp-relaxation/) of a problem. The method solves the relaxation in polynomial time, fixes every variable that some optimal integral solution shares with the LP solution, and deletes the fixed part. The LP value is a lower bound on the optimum, so a yes-instance with parameter $k$ has LP value at most $k$, and if each remaining variable carries a fixed share of the LP value, then at most a constant times $k$ variables remain. For [vertex cover](/parameterized-vertex-cover/) with the cover size $k$ as the parameter, the [Nemhauser-Trotter theorem](/nemhauser-trotter-theorem/) supplies the persistence step and the result is a kernel with at most $2k$ vertices.

## In plain words

Many hard choice problems become easy if you allow fractions: half of an item, a third of a guard. The answer with fractions is fast to compute, and it is never worse than the true best answer, so it is a lower bound.

Sometimes the fractional answer also gives sure decisions. If it takes an item fully, some true best answer takes it too. If it leaves an item out fully, some true best answer leaves it out too. You make those decisions and remove those items.

What is left are the items that got a fraction. Each of them adds at least a fixed amount, such as one half, to the fractional answer. That answer is at most your budget, so only a few such items can remain. A larger rest means that the answer is no.

## When it applies

- The problem is a minimization problem with a natural LP relaxation, and the parameter $k$ is the solution size, so $\mathrm{LP} \le \mathrm{OPT} \le k$ for a yes-instance.
- The relaxation has a *persistence* property: for some optimal LP solution $y$, there is an optimal integral solution that agrees with $y$ on all variables where $y$ is 0 or 1.
- Each variable that the LP does not fix has a value bounded away from 0, for example exactly $\tfrac12$. Then the number of such variables is at most a constant times the LP value.
- A suitable optimal solution, for example a half-integral extreme point, can be found in polynomial time.

## The template

The template has four holes. LP(x) is the relaxation, with optimal value $\mathrm{lp}(x) \le \mathrm{opt}(x)$. PERSIST(y) is the set of variables, with their values, that some optimal integral solution shares with the optimal LP solution $y$. FIX(x, k, F) applies those values and returns the smaller instance with the parameter lowered by the cost of $F$. BOUND(k) is the size bound that follows from the LP value, for example $2k$ when each unfixed variable has value $\tfrac12$.

```pseudo id=main
LP-KERNEL(x, k)
L1  y ← an optimal solution of LP(x) with the needed structure
L2  if value(y) > k then return NO          ▷ lp(x) ≤ opt(x)
L3  F ← PERSIST(y)
L4  (x, k) ← FIX(x, k, F)                   ▷ safe by persistence
L5  if SIZE(x) > BOUND(k) then return NO
L6  return (x, k)
```

**Lemma.** Assume that $\mathrm{lp}(x) \le \mathrm{opt}(x)$, that some optimal integral solution agrees with $y$ on $F$, that the optimum of the reduced instance is the old optimum minus the cost of $F$, and that every reduced instance with $\mathrm{opt} \le k$ has size at most BOUND(k). Then LP-KERNEL is a kernelization of size BOUND(k).

*Proof.* Line L2 is correct because a yes-instance has $\mathrm{lp}(x) \le \mathrm{opt}(x) \le k$. By persistence, fixing $F$ keeps an optimal solution, and the reduced instance has a solution of size at most $k - \mathrm{cost}(F)$ exactly when the old instance has one of size at most $k$. So line L4 is safe. Line L5 is correct by the size assumption, and every output has size at most BOUND(k). Each line runs in polynomial time, because an LP can be solved in polynomial time with the [ellipsoid method](/ellipsoid-method/), and often faster by a combinatorial method. $\square$

For vertex cover the holes are: LP(G) minimizes $\sum x_v$ subject to $x_u + x_v \ge 1$ for each edge and $x \ge 0$; $y$ is a half-integral optimum, computed by a matching in the [bipartite double cover](/bipartite-double-cover/) in time $O(m \sqrt{n})$; PERSIST takes the vertices of value 1 into the cover and the vertices of value 0 out of it; FIX returns $(G[V_{1/2}], k - |V_1|)$; and BOUND is $2k$ vertices, because $|V_1| + \tfrac12 |V_{1/2}| = \mathrm{lp}(G) \le k$.

## Classic examples

### Vertex cover: a kernel with 2k vertices

This is the example that the template comes from. The [Nemhauser-Trotter theorem](/nemhauser-trotter-theorem/) proves that the vertices of value above $\tfrac12$ are in some least cover and the vertices below $\tfrac12$ are not, and that the least cover of $G$ has exactly $|V_1| + \mathrm{vc}(G[V_{1/2}])$ vertices. Chen, Kanj and Jia (2001) used this for the kernel with at most $2k$ vertices. A perfect matching on $2k$ vertices shows that the bound $2k$ is reached: all values are $\tfrac12$ and nothing is fixed. Lokshtanov et al. (2014) cut it to $2k - c \log k$ vertices for a constant $c$.

### The LP kernel against crowns

The graph from the [crown reduction](/crown-reduction/) page has 12 vertices: vertex 0 with leaves 2, 3 and 4, vertex 1 with leaves 4, 5 and 6, a 5-cycle on 7 to 11, and the edge 0-7. A scratch script computed the half-integral optimum with the double cover: $x_0 = x_1 = 1$, the five leaves get 0, and the cycle vertices get $\tfrac12$, with LP value $\tfrac92$. A search over all half-integral vectors gives the same value. So $V_1 = \{0, 1\}$ and $V_{1/2}$ is the 5-cycle.

- $k = 4$: line L2 returns NO, because $\tfrac92 > 4$. Line L5 would also reject, because $k' = 2$ and $|V_{1/2}| = 5 > 4$.
- $k = 5$: the kernel is the 5-cycle with $k' = 3$, a yes-instance.

The crown kernel reaches the same 5-cycle, but it needs two rounds and a separate rule for the isolated vertices. In general, an optimal half-integral solution with $V_0 \ne \emptyset$ gives the crown $(V_0, V_1)$, so the LP kernel applies every crown at once, and its bound $2k$ beats the crown bound $3k$.

### Parameters above the LP

Since $\mathrm{lp}(G) \le \mathrm{vc}(G)$, the gap $\ell = k - \mathrm{lp}(G)$ is a smaller parameter than $k$, and the question whether vertex cover is FPT in $\ell$ is natural. Lokshtanov, Narayanaswamy, Raman, Ramanujan and Saurabh showed that the known reduction rules with the simplest branching give time $O^*(2.618^\ell)$, and a finer branching gives $O^*(2.3146^\ell)$. Here $O^*$ hides factors polynomial in $n$. The LP is the tool in both: the reduction rules use persistence to fix vertices, and the analysis measures progress by the drop of $\ell$ in each branch, not by the drop of $k$. The same paper gives $O^*(2.3146^\ell)$ for vertex cover above a maximum matching, for [odd cycle transversal](/odd-cycle-transversal/) and for Almost 2-SAT, because these reduce to vertex cover above LP with a parameter that does not grow.

### Hitting set with sets of size 3: where the method stops

For [hitting set](/parameterized-hitting-set/) with sets of size $d \ge 3$, the LP has the constraints $\sum_{v \in S} x_v \ge 1$. It gives a lower bound, so line L2 still works, but the persistence step fails: the LP need not have a half-integral optimum. For the 7 lines of the Fano plane, the value $\tfrac13$ on each point is optimal with value $\tfrac73$, while the best half-integral vector has value 3 (a scratch search). Without persistence nothing can be fixed, and the unfixed elements can have values as small as $\tfrac1d$, so the count at line L5 has nothing to work with. The polynomial kernels for $d$-hitting set come from the [sunflower lemma](/sunflower-lemma/) instead.

## Variations

- **Weighted vertex cover.** Nemhauser and Trotter stated their results for weighted vertex packing, so persistence also holds for weighted vertex cover. It is a safe reduction rule there even when no size bound follows.
- **Approximate kernels.** If a constant loss is allowed, the LP gives smaller kernels. The table of Lokshtanov, Panolan, Ramanujan and Saurabh lists an $\alpha$-approximate kernel for vertex cover with $2(2 - \alpha)k$ vertices for $1 < \alpha < 2$; see [lossy kernelization](/lossy-kernelization/).
- **LP-guided branching.** Instead of a kernel, the LP value can measure the progress of a [bounded search tree](/bounded-search-tree/), as in vertex cover above LP.
- **Crowns without an LP.** The [crown reduction](/crown-reduction/) finds the structure behind $V_0$ and $V_1$ with matchings only.

## Pitfalls

- **A non-half-integral optimum.** A general LP solver can return an optimum with values such as $\tfrac13$ and $\tfrac23$. Persistence still holds with the thresholds at $\tfrac12$, but the count $|V_{1/2}| \le 2k'$ needs a half-integral solution. Use the double cover or round to an extreme point.
- **Persistence is for some optimal solution.** For a single edge $uv$, both $(x_u, x_v) = (1, 0)$ and $(0, 1)$ are optimal. Fixing from the first puts $u$ in and $v$ out, and fixing from the second puts $v$ in and $u$ out, which together is no cover at all. Fix the variables of one LP solution, then re-solve on the reduced instance.
- **The LP bound is for minimization.** For a maximization problem the LP value is an upper bound, and line L2 must be turned around.
- **The unit of size.** $2k$ counts vertices. The kernel can have $\Theta(k^2)$ edges, which is $\Theta(k^2)$ bits up to a log factor, and Dell and van Melkebeek showed that no compression of vertex cover has $O(k^{2 - \varepsilon})$ bits unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$.
- **Floating point.** The persistence test compares values with $\tfrac12$. Compute with exact rationals or with the combinatorial double-cover method.

## Exercises

1. Prove that the reduced graph $G[V_{1/2}]$ has the all-$\tfrac12$ vector as an optimal LP solution.
2. Give a graph where the double cover method returns $V_0 = \emptyset$ although $G$ has a crown.
3. Show that the vertex cover LP of a bipartite graph has an integral optimum, and use this to explain why the double cover method works.
4. For $d$-hitting set, show that line L2 answers NO on every instance with more than $k$ pairwise disjoint sets, and explain why this test alone is not a kernel.
5. Write the LP relaxation for weighted vertex cover and state the persistence property for it.

## References
