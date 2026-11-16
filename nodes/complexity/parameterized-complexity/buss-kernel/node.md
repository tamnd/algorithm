---
tag: 0V3DF3
kind: algorithm
slug: buss-kernel
name: Buss kernel for vertex cover
aliases:
- Buss kernelization
area: complexity/parameterized-complexity
level: intro
summary: "Put every vertex of degree above k into the cover, drop isolated vertices, and answer no if more than k^2 edges or k^2 + k vertices remain. A vertex cover kernel in O(n + m) time."
solves: [parameterized-vertex-cover]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the bound on the size of the cover}
  time: {worst: O(n + m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, kernel_edges: k^2, kernel_vertices: k^2 + k, output_is_subgraph: true}
history:
  year: 1993
  people: [Jonathan F. Buss, Judy Goldsmith]
  note: Buss and Goldsmith used the high-degree rule in their 1993 paper on limited nondeterminism.
prereqs: [kernel, parameterized-vertex-cover, degree]
see_also: [kernelization, vertex-cover-branching, crown-reduction, nemhauser-trotter-theorem, lp-kernelization, polynomial-kernel, sunflower-lemma, vertex-cover]
sources:
  - paper: doi:10.1137/0222038
    title: "Jonathan F. Buss and Judy Goldsmith, Nondeterminism within P, SIAM Journal on Computing 22(3), 560-572 (1993)"
    locator: the high-degree rule and the bound on the reduced graph for vertex cover
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Section 2.2.1, Vertex Cover (the reduction rules and the kernel with O(k^2) vertices and edges)
  - book: isbn:9780198566076
    title: Rolf Niedermeier, Invitation to Fixed-Parameter Algorithms, Oxford University Press, 2006
    locator: Chapter 4, Vertex Cover, an illustrative example; Chapter 7, Data reduction and problem kernels
  - book: isbn:9781447155584
    title: Rodney G. Downey and Michael R. Fellows, Fundamentals of Parameterized Complexity, Springer, 2013
    locator: Chapter 4, Kernelization
  - paper: doi:10.1145/2629620
    title: "Holger Dell and Dieter van Melkebeek, Satisfiability allows no nontrivial sparsification unless the polynomial-time hierarchy collapses, Journal of the ACM 61(4), article 23 (2014)"
    locator: no kernel of O(k^(2-e)) bits for vertex cover unless NP is a subset of coNP/poly
---

The Buss kernel is a [kernelization](/kernelization/) for [vertex cover](/parameterized-vertex-cover/) with the parameter $k$, the size of the cover. It uses two reduction rules. A vertex of degree more than $k$ must be in every cover of size at most $k$, so the algorithm puts it in the cover and lowers $k$ by one. An isolated vertex covers no edge, so the algorithm deletes it. When no rule applies, every vertex has degree at most $k$, so $k$ vertices cover at most $k^2$ edges, and a graph with more than $k^2$ edges or more than $k^2 + k$ vertices has no cover of size $k$. The output is an equivalent instance $(G', k')$ with $k' \le k$, at most $k'^2$ edges and at most $k'^2 + k'$ vertices, and it is computed in $O(n + m)$ time. The size of the result does not depend on $n$, which makes it a [polynomial kernel](/polynomial-kernel/).

## In plain words

You must guard every road in a road network with at most $k$ guards, and each guard stands at a crossing. Look at a crossing with more than $k$ roads. If it has no guard, each of its roads needs a guard at the other end, so you need more than $k$ guards. So that crossing must get a guard. Place one there, forget its roads, and keep one guard fewer.

Repeat until no crossing has too many roads, and forget crossings with no road left. Now each guard can watch only a few roads. If there are still too many roads or too many crossings for the guards you have left, the answer is no. If not, the network that is left is small, and its size depends only on the number of guards. You can solve it with any method.

## The problem

The input is a graph $G = (V, E)$ given by its edges, with $n$ vertices and $m$ edges, and an integer $k \ge 0$. The question is [p-Vertex-Cover](/parameterized-vertex-cover/): is there a set $S \subseteq V$ with $|S| \le k$ such that every edge has an endpoint in $S$? We write $\tau(G)$ for the least size of a vertex cover.

The output is an instance $(G', k')$ and a set $F \subseteq V$ such that:

- $(G, k)$ is a yes-instance exactly when $(G', k')$ is one;
- $k' \le k$, $G'$ has at most $k'^2$ edges and at most $k'^2 + k'$ vertices;
- if $S'$ is a cover of $G'$ with $|S'| \le k'$, then $S' \cup F$ is a cover of $G$ with $|S' \cup F| \le k$.

The size is counted in vertices and edges. As an edge list, the kernel takes $O(k^2 \log k)$ bits.

## The algorithm

Let $K_2$ denote the graph with one edge. The instance $(K_2, 0)$ is a fixed no-instance.

```pseudo id=main
BUSS-KERNEL(G, k)                    ▷ G = (V, E), k ≥ 0
L1  F ← ∅
L2  while k ≥ 0 and some vertex v of G has deg(v) > k do
L3      G ← G - v;  F ← F ∪ {v};  k ← k - 1
L4  if k < 0 then return (K2, 0), ∅
L5  delete every isolated vertex of G
L6  if |E(G)| > k^2 or |V(G)| > k^2 + k then return (K2, 0), ∅
L7  return (G, k), F
```

Line L3 removes $v$ and all its edges. Line L4 handles the case where the rule fired $k + 1$ times: then $G$ needs more than $k$ vertices. Line L6 is the size test. It is valid only after the loop, when every vertex has degree at most $k$.

For a linear running time, keep the vertices in buckets by degree and a pointer $d$ to the highest nonempty bucket. Removing $v$ moves each neighbor one bucket down. Degrees never grow, so $d$ only moves down, and the scans of $d$ cost $O(n)$ in total.

## Example

Let $G$ have the vertices $0, \ldots, 9$ and the 10 edges $\{0, i\}$ for $i = 1, \ldots, 6$, $\{1, 2\}$, $\{3, 4\}$, $\{7, 8\}$ and $\{8, 9\}$. The degrees are 6 for vertex 0, 2 for vertices 1, 2, 3, 4 and 8, and 1 for vertices 5, 6, 7 and 9.

| step | $k = 3$ | $k = 4$ |
|---|---|---|
| L2, L3 | $\deg(0) = 6 > 3$: $F = \{0\}$, $k = 2$ | $\deg(0) = 6 > 4$: $F = \{0\}$, $k = 3$ |
| L2 | largest degree is $\deg(8) = 2 \le 2$: stop | largest degree is $2 \le 3$: stop |
| L5 | delete 5 and 6 | delete 5 and 6 |
| L6 | 4 edges $\le 4$, but 7 vertices $> 6$ | 4 edges $\le 9$ and 7 vertices $\le 12$ |
| result | $(K_2, 0)$: no | $G'$ with edges $\{1,2\}, \{3,4\}, \{7,8\}, \{8,9\}$, $k' = 3$, $F = \{0\}$ |

Both answers are right. The graph $G'$ needs one vertex for each of $\{1, 2\}$ and $\{3, 4\}$ and vertex 8 for the path $7, 8, 9$, so $\tau(G') = 3$ and $\tau(G) = 4$. For $k = 4$, the cover $\{1, 3, 8\}$ of $G'$ and $F$ give the cover $\{0, 1, 3, 8\}$ of $G$. For $k = 3$ the edge test alone would pass; the vertex test catches the no-instance.

## Correctness

The proof has three parts. First, the high-degree rule is safe: if $\deg(v) > k$, a cover $S$ with $|S| \le k$ and $v \notin S$ must contain every neighbor of $v$, which is more than $k$ vertices. So $(G, k)$ is a yes-instance exactly when $(G - v, k - 1)$ is one, and a cover of $G - v$ plus $v$ covers $G$. Second, deleting isolated vertices changes no cover. Third, the size lemma: if no vertex has degree above $k$, there is no isolated vertex and $\tau(G) \le k$, then a cover $S$ of size at most $k$ covers all edges with at most $k$ edges each, so $|E| \le k^2$; and each vertex outside $S$ has an edge, whose other end is in $S$, so $|V \setminus S| \le k^2$ and $|V| \le k^2 + k$. A larger reduced graph is therefore a no-instance, which justifies line L6. The full proof, with the loop invariant and the lifting of covers, is in the proof file of this page.

## Complexity

Building the adjacency sets and the degree buckets takes $O(n + m)$ time. Each pass of the loop at L2 removes one vertex $v$ and does $O(1)$ work per edge at $v$; each edge is removed once, so all passes cost $O(n + m)$, plus $O(n)$ for the moves of the pointer $d$. Lines L5 and L6 scan the remaining graph once. The total is $O(n + m)$ time and $O(n + m)$ space.

The loop runs at most $k + 1$ times. The kernel has at most $k^2$ edges and $k^2 + k$ vertices. Followed by the [edge branching](/vertex-cover-branching/) on the kernel, it decides vertex cover in $O(n + m + 2^k k^2)$ time.

## Properties

- **Kernel size.** At most $k'^2$ edges and $k'^2 + k'$ vertices, with $k' \le k$. The bound is reached: $k$ disjoint stars with $k$ leaves each have $k^2$ edges, $k^2 + k$ vertices, maximum degree $k$ and $\tau = k$.
- **A subgraph.** Unless it returns the fixed no-instance, the output graph is an induced subgraph of the input.
- **Lifting.** The set $F$ turns each cover of the kernel into a cover of the input. Every vertex of $F$ is in every cover of $G$ of size at most $k$.
- **Deterministic and simple.** No matching, no LP and no randomness.
- **Bits.** $O(k^2 \log k)$ bits as an edge list. Dell and van Melkebeek proved that no kernel has $O(k^{2 - \varepsilon})$ bits unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$, so the bound in bits is near the best possible.

## Variants and improvements

- **Degree-1 rule.** If $v$ has degree 1 with neighbor $u$, put $u$ in the cover. It does not change the worst-case bound but often shrinks real inputs.
- **Crown reduction.** A [crown](/crown-reduction/) decomposition gives a kernel with at most $3k$ vertices.
- **LP kernel.** By the [Nemhauser-Trotter theorem](/nemhauser-trotter-theorem/), the vertices of value $\tfrac{1}{2}$ in an optimal half-integral LP solution form a kernel with at most $2k$ vertices; see [LP kernelization](/lp-kernelization/).
- **Hitting set.** For sets of size $d$, the same idea with the [sunflower lemma](/sunflower-lemma/) gives a kernel with $O(d!\,k^d)$ sets.
- **Search after the kernel.** Running the [bounded search tree](/vertex-cover-branching/) on the kernel instead of the input moves the exponential factor off $n$.

## When to use it

Use it as the first step of any exact vertex cover solver when $k$ is small compared with $n$: it costs one pass over the graph and removes all vertices of high degree. It is also the easiest kernel to implement and to check. When a smaller kernel matters, for example when $k$ is close to $n / 2$, use the crown or LP kernel, which bound the vertices by $3k$ or $2k$. The bound $k^2 + k$ helps only when $k^2 + k < n$.

## Pitfalls

- **Degree at least k.** Writing $\deg(v) \ge k$ in line L2 is wrong; the right test is $\deg(v) > k$. With $k = 2$, let $v$ have the neighbors $a$ and $b$, and add the edges $\{a, a'\}$ and $\{b, b'\}$. The cover $\{a, b\}$ has size 2, but no cover of size 2 contains $v$. The rule $\deg(v) \ge 2$ may take $v$ and then report no.
- **Size test too early.** Testing $|E| > k^2$ before the loop at L2 ends is wrong; line L6 must come after the loop. A star with 50 leaves and $k = 1$ has 50 edges but a cover of size 1.
- **No vertex bound.** Testing only the edges at L6, and skipping L5, leaves the isolated vertices in the output, so its size depends on $n$ and it is not a kernel. Delete isolated vertices at L5 and test both bounds at L6.
- **Lost forced vertices.** A cover of $G'$ alone is not a cover of $G$. Return $F$ at L7 and add it to the cover of the kernel.
- **A negative budget.** If the rule fires $k + 1$ times, $k$ becomes $-1$ and the bounds at L6 make no sense. Line L4 must return the no-instance first.

## Implementations

## History

Buss and Goldsmith (1993) described the high-degree rule for vertex cover in their paper on classes with limited nondeterminism, and the kernel is named after Jonathan Buss. Later work reduced the kernel to $3k$ vertices with crowns and to $2k$ vertices with the LP relaxation (Chen, Kanj and Jia, 2001). Dell and van Melkebeek (2014) showed that the number of bits cannot be pushed much below $k^2$ unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$.

## References
