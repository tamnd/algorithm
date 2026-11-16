---
tag: FKD67C
kind: technique
slug: bidimensionality-theory
name: Bidimensionality theory
aliases:
- bidimensionality
area: complexity/parameterized-complexity
level: research
summary: "If a minor-closed graph parameter is at least c t^2 on the t x t grid, a planar instance either answers at once or has treewidth O(sqrt k). This gives 2^O(sqrt k) n^O(1) algorithms."
prereqs: [grid-minor-theorem, treewidth, planar-graph, dp-on-tree-decompositions]
see_also: [subexponential-parameterized-algorithm, baker-technique, irrelevant-vertex-technique, courcelle-theorem, parameterized-vertex-cover, parameterized-dominating-set, planar-separator-theorem, meta-theorems]
sources:
  - paper: doi:10.1145/1101821.1101823
    title: "Erik D. Demaine, Fedor V. Fomin, MohammadTaghi Hajiaghayi and Dimitrios M. Thilikos, Subexponential parameterized algorithms on bounded-genus graphs and H-minor-free graphs, Journal of the ACM 52(6), 866-893 (2005)"
    locator: the main theorems, 2^O(sqrt k) n^O(1) algorithms for dominating set, vertex cover and related problems on H-minor-free graphs
  - paper: doi:10.1093/comjnl/bxm033
    title: "Erik D. Demaine and MohammadTaghi Hajiaghayi, The bidimensionality theory and its algorithmic applications, The Computer Journal 51(3), 292-302 (2008)"
    locator: the survey, the definitions of minor- and contraction-bidimensionality and the list of applications
  - book: isbn:9783319212746
    title: "Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015"
    locator: "Section 7.7, Win/win approaches and planar problems (7.7.1 the planar grid theorem with 9t/2, 7.7.2 bidimensionality with planar vertex cover), and Section 14.4.1, Planar and geometric problems (the ETH lower bounds)"
  - paper: doi:10.1016/S0022-0000(03)00074-6
    title: "Liming Cai and David Juedes, On the existence of subexponential parameterized algorithms, Journal of Computer and System Sciences 67(4), 789-807 (2003)"
    locator: no 2^o(sqrt k) n^O(1) algorithm for planar vertex cover, planar dominating set and related problems unless ETH fails
---

Bidimensionality theory gives [subexponential parameterized algorithms](/subexponential-parameterized-algorithm/) for many problems on [planar graphs](/planar-graph/) and on graphs that exclude a fixed minor. The parameter is the solution size $k$. If the solution value of a problem cannot grow when you take a minor, and is at least $c t^2$ on the $t \times t$ grid, then a planar instance either has the answer at once or has [treewidth](/treewidth/) $O(\sqrt{k})$. A dynamic program then finishes in time $2^{O(\sqrt{k})} \cdot n^{O(1)}$. Unlike the [irrelevant vertex technique](/irrelevant-vertex-technique/), it never deletes vertices: a large grid decides the instance.

## In plain words

Some problems ask for a set of at least or at most a certain size, and on a square grid the best set grows with the area of the grid, not with its side. For such problems, a large grid inside the graph gives the answer at once. If the graph has no large grid, then by a theorem on planar graphs it is thin, and thin graphs are easy for dynamic programming. The trick is to choose the grid side so that the two cases meet. Because the area grows like the square of the side, the width that you must handle is only about the square root of the target size. That turns a cost that is exponential in the target into a cost that is exponential in its square root.

## When it applies

Let $\pi$ be a graph parameter, such as the size of a minimum vertex cover, and consider the problem "is $\pi(G) \le k$?" (or "$\ge k$" for a maximization problem).

- $\pi$ is **minor-bidimensional** if $\pi(H) \le \pi(G)$ for every [minor](/graph-minor/) $H$ of $G$, and $\pi(\boxplus_t) \ge c t^2$ for a constant $c > 0$, where $\boxplus_t$ is the $t \times t$ grid. Examples: vertex cover, feedback vertex set, and the length of a longest path.
- $\pi$ is **contraction-bidimensional** if $\pi$ does not grow under edge contractions, and $\pi$ is at least $c t^2$ on a fixed triangulated version of the grid, $\Gamma_t$. Examples: dominating set and its variants.
- The graph class must satisfy a linear grid theorem. On planar graphs, treewidth at least $9t/2$ gives a $\boxplus_t$ minor (Cygan et al., Section 7.7.1), and treewidth at least $9t + 5$ gives $\Gamma_t$ as a contraction. Demaine, Fomin, Hajiaghayi and Thilikos (2005) extend this to graphs of bounded genus and to graphs that exclude a fixed minor $H$.
- The problem has a dynamic program on a tree decomposition of width $w$ in time $2^{O(w)} \cdot n^{O(1)}$, or at least $2^{O(w \log w)} \cdot n^{O(1)}$.

## The template

The template is for a minimization problem on planar graphs. For a maximization problem, line L3 answers YES.

```pseudo id=template
BIDIM(G, k)                                     ▷ G planar, decide pi(G) ≤ k
L1  t ← smallest t with GRIDVALUE(t) > k        ▷ hole: a lower bound on pi of the grid
L2  (D, M) ← GRID-OR-DECOMPOSITION(G, t)        ▷ hole: planar grid theorem, minor or contraction form
L3  if M is a model of the t × t grid
L4      return NO                                ▷ pi(G) ≥ pi(grid) ≥ GRIDVALUE(t) > k
L5  return DP(G, D, k)                           ▷ hole: dynamic program on D, width O(t)
```

**Lemma (correctness).** If $M$ is a minor model of $\boxplus_t$, then $\pi(G) \ge \pi(\boxplus_t) \ge \mathrm{GRIDVALUE}(t) > k$ by minor monotonicity, so NO is correct. Otherwise $D$ is a tree decomposition of width $O(t)$ and the dynamic program is exact. $\square$

**Lemma (time).** If $\mathrm{GRIDVALUE}(t) \ge c t^2$, then $t = O(\sqrt{k})$. The planar grid theorem has an $O(n^2)$ algorithm that returns either a tree decomposition of width $(9/2 + \varepsilon) t$ or a grid minor model (Cygan et al., Section 7.7.1). A dynamic program in time $2^{O(w)} \cdot n^{O(1)}$ on width $w = O(\sqrt{k})$ gives total time $2^{O(\sqrt{k})} \cdot n^{O(1)}$.

## Classic examples

### Planar vertex cover

Fill the holes with $\mathrm{GRIDVALUE}(t) = \lfloor t^2/2 \rfloor$ and the minor form of the planar grid theorem. The grid $\boxplus_t$ has a matching of size $\lfloor t^2/2 \rfloor$, and every vertex cover has one vertex of each matching edge. An exact search gives vertex cover numbers 2, 4, 8 and 12 for $t = 2, 3, 4, 5$, equal to $\lfloor t^2/2 \rfloor$. A vertex cover of $G$ restricts to a vertex cover of each minor, so the parameter is minor-monotone. The dynamic program for [vertex cover](/parameterized-vertex-cover/) on width $w$ takes time $2^{w} \cdot w^{O(1)} \cdot n$.

For $k = 50$: $\lfloor 10^2/2 \rfloor = 50$ is not larger than 50, but $\lfloor 11^2/2 \rfloor = 60$ is, so $t = 11$. A planar graph of treewidth at least $9 \cdot 11 / 2 = 49.5$, that is, at least 50, has an $11 \times 11$ grid minor, so its vertex cover number is at least 60 and the answer is NO. Otherwise the treewidth is at most 49 and the dynamic program runs on a tree decomposition of width about $(9/2) \cdot 11$.

### Planar dominating set

[Dominating set](/parameterized-dominating-set/) is not closed under minors. A star with $m$ leaves has a dominating set of size 1, but deleting its edges leaves $m + 1$ isolated vertices, which need $m + 1$ vertices. It is closed under contraction, because the image of a dominating set after a contraction still dominates. So the contraction form of the grid theorem is used, with $\Gamma_t$. Demaine, Fomin, Hajiaghayi and Thilikos (2005) give time $2^{O(\sqrt{k})} \cdot n^{O(1)}$ for dominating set on planar graphs and on graphs that exclude a fixed minor.

### Longest path (a maximization problem)

The question is whether $G$ has a path with $k$ vertices. A path in a minor of $G$ lifts to a path in $G$ that is at least as long, by walking through the branch sets. The grid $\boxplus_t$ has a Hamiltonian path with $t^2$ vertices. So if $t^2 \ge k$ and a $\boxplus_t$ minor exists, L3 answers YES. Otherwise the treewidth is $O(\sqrt{k})$, and a dynamic program in time $2^{O(w \log w)} \cdot n^{O(1)}$ gives time $2^{O(\sqrt{k} \log k)} \cdot n^{O(1)}$. See [parameterized longest path](/parameterized-longest-path/).

## Variations

- **H-minor-free and bounded-genus graphs.** The same template works on graphs of bounded genus and on graphs that exclude a fixed minor $H$, with grid theorems for these classes in place of the planar one (Demaine, Fomin, Hajiaghayi and Thilikos 2005). For contraction-bidimensional problems the class must exclude an apex graph, that is, a graph that becomes planar after deleting one vertex.
- **Minor-closed classes.** For a minor-monotone parameter $\pi$ and a fixed $k$, the graphs with $\pi(G) \le k$ form a minor-closed class. So the [graph minor theorem](/graph-minor-theorem/) gives a polynomial test for each $k$, but without an explicit algorithm or a bound on $f(k)$. Bidimensionality gives an explicit algorithm in time $2^{O(\sqrt{k})} \cdot n^{O(1)}$ on planar graphs.
- **Approximation and kernels.** The same grid argument gives approximation schemes and linear kernels for many bidimensional problems. The survey of Demaine and Hajiaghayi (2008) lists these uses. For kernels see [meta-theorems](/meta-theorems/).
- **Baker's technique.** [Baker's technique](/baker-technique/) also uses the bounded treewidth of planar graphs, but it cuts the graph into BFS layers and gives approximation schemes. Bidimensionality gives exact algorithms.
- **Separators.** The [planar separator theorem](/planar-separator-theorem/) gives treewidth $O(\sqrt{n})$, in terms of the number of vertices. Bidimensionality gives treewidth $O(\sqrt{k})$, in terms of the parameter, which is smaller when $k$ is much smaller than $n$.

## Pitfalls

- **Check the closure property.** Dominating set is not minor-closed. Using the minor form of the grid theorem for it is a common mistake.
- **The grid value must be quadratic.** If $\pi(\boxplus_t)$ grows only like $t$, the treewidth bound becomes $O(k)$, and nothing subexponential follows.
- **The dynamic program must be single-exponential.** A dynamic program in $w^{O(w)}$ gives only $2^{O(\sqrt{k} \log k)}$. Connectivity problems such as longest path need special dynamic programs on planar graphs to reach $2^{O(\sqrt{k})}$.
- **Planarity or an excluded minor is needed.** On general graphs, vertex cover has no algorithm in time $2^{o(k)} \cdot n^{O(1)}$ unless ETH fails, so the method cannot work there.
- **The bound is tight under ETH.** Cai and Juedes (2003) proved that planar vertex cover, planar dominating set and related problems have no algorithm in time $2^{o(\sqrt{k})} \cdot n^{O(1)}$ unless ETH fails (see also Cygan et al., Section 14.4.1). So the square root in the exponent cannot be improved under ETH.

## Exercises

1. Prove that the vertex cover number of $\boxplus_t$ is exactly $\lfloor t^2/2 \rfloor$. Use a matching for the lower bound and a checkerboard coloring for the upper bound.
2. Show that the size of a minimum feedback vertex set of $\boxplus_t$ is at least $\lfloor t/2 \rfloor^2$. Hint: find that many vertex-disjoint 4-cycles. Conclude that feedback vertex set is minor-bidimensional.
3. For planar vertex cover with $k = 200$, find the smallest $t$ with $\lfloor t^2/2 \rfloor > k$, and the treewidth above which BIDIM answers NO.

## References
