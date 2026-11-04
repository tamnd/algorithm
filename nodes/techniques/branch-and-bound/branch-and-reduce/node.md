---
tag: HSNMTD
kind: algorithm
slug: branch-and-reduce
name: Branch and reduce
aliases:
- branch-and-reduce algorithm
area: techniques/branch-and-bound
level: advanced
summary: Exact branching algorithm that applies reduction rules at each node before branching, giving fast exponential bounds.
solves: [maximum-independent-set]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(1.3803^n n^4)}
  space: {extra: O(n^3)}
properties: {deterministic: true, recursive: false}
prereqs: [maximum-independent-set, bounded-search-tree, dominance-pruning]
see_also: [exact-exponential-algorithms, measure-and-conquer, bounded-search-tree, kernelization, dominance-pruning, vertex-cover, independent-set, depth-first-branch-and-bound]
sources:
  - book: isbn:9783642165320
    title: Fedor V. Fomin and Dieter Kratsch, Exact Exponential Algorithms
    locator: Chapter 2, Branching (branch-and-reduce algorithms, branching vectors and branching numbers, maximum independent set)
  - paper: doi:10.1137/0206038
    title: Robert Endre Tarjan and Anthony E. Trojanowski, Finding a maximum independent set, SIAM Journal on Computing 6(3), 1977
    locator: pp. 537 to 546
  - paper: doi:10.1145/1552285.1552286
    title: Fedor V. Fomin, Fabrizio Grandoni and Dieter Kratsch, A measure and conquer approach for the analysis of exact algorithms, Journal of the ACM 56(5), 2009
    locator: Article 25
---

A branch and reduce algorithm solves an NP-hard problem exactly by a search tree in which every node first applies *reduction rules* and then *branches*. A reduction rule replaces the instance by a smaller one with a known relation between the answers, such as "a vertex of degree 0 is in some maximum independent set". A branching rule splits the instance into a few smaller ones whose answers give the answer of the whole. The reductions make sure that the search branches only on instances where branching removes much of the instance, and this gives a running time of the form $O(c^n)$ with $c < 2$. This page develops the method on [maximum independent set](/maximum-independent-set/).

## In plain words

You want the largest group of people in which no two are friends. Some choices are easy. A person with no friends can always join. A person with one friend can always join too: if the friend is in the group, swap the two. Make every easy choice first, until none is left.

Only then guess. Take the person with the most friends. Either this person is out, which removes one person, or this person is in, which removes the person and all of their friends, at least four people. Each guess shrinks the problem a lot, so the total number of guesses grows much more slowly than trying every group.

## The problem

Given a graph $G = (V, E)$ with $n$ vertices, find an independent set of largest size: a set $I \subseteq V$ with no edge inside it. Its size is $\alpha(G)$. For a vertex $v$, $N(v)$ is the set of its neighbors and $N[v] = N(v) \cup \{v\}$.

## The algorithm

The search keeps a stack of pairs $(H, I)$, where $H$ is an induced subgraph of $G$ and $I$ is an independent set of $G$ with no vertex in $H$ and no neighbor in $H$. The reduction rules are applied until none applies; then the node is solved directly or split.

```pseudo id=main
BRANCH-AND-REDUCE-MIS(G)
L1  best ← ∅; PUSH(Q, (G, ∅))
L2  while Q is not empty do
L3      (H, I) ← POP(Q)
L4      repeat until no rule applies                      ▷ reduce
L5          if some v has degree 0 then I ← I ∪ {v}; H ← H − v
L6          else if some v has degree 1 then I ← I ∪ {v}; H ← H − N[v]
L7          else if some edge uv has N[v] ⊆ N[u] then H ← H − u   ▷ u is dominated
L8      if every vertex of H has degree at most 2 then     ▷ H is a union of cycles
L9          add ⌊k/2⌋ vertices of each cycle of length k to I; if |I| > |best| then best ← I; continue
L10     v ← a vertex of H of maximum degree                ▷ degree at least 3
L11     PUSH(Q, (H − v, I))                                ▷ v is not in the set
L12     PUSH(Q, (H − N[v], I ∪ {v}))                       ▷ v is in the set
L13 return best
```

After the reductions, no vertex has degree 0 or 1. So at line L8 every vertex has degree exactly 2, and $H$ is a disjoint union of cycles, or empty. A cycle of length $k$ has $\lfloor k/2 \rfloor$ as the size of its largest independent set: every second vertex. At line L10 the chosen vertex has degree at least 3, so the branch at line L12 removes at least 4 vertices.

## Example

The cube graph has the 8 vertices $0, \ldots, 7$, with an edge between two numbers whose binary forms differ in one bit. Every vertex has degree 3, and no rule applies at the root: there is no vertex of degree 0 or 1, and as the graph has no triangle, no $N[v]$ lies in another $N[u]$.

1. **Root.** Branch on vertex 0, with neighbors 1, 2 and 4.
2. **Take 0.** Delete $N[0] = \{0, 1, 2, 4\}$. Left are 3, 5, 6 and 7, where 7 is adjacent to the other three. Vertex 3 has degree 1: take it and delete 7. Then 5 and 6 have degree 0: take both. Leaf with $I = \{0, 3, 5, 6\}$, so $best$ has size 4.
3. **Leave out 0.** The graph on $1, \ldots, 7$ has vertices 1, 2 and 4 of degree 2, and no rule applies. Branch on vertex 3, the vertex of degree 3 with the smallest number.
4. **Take 3.** Delete $N[3] = \{1, 2, 3, 7\}$. Left is the path $5 - 4 - 6$. Take 5, which deletes 4, then take 6. Leaf with $\{3, 5, 6\}$, size 3.
5. **Leave out 3.** Left are 1, 2, 4, 5, 6, 7, where 1 and 2 now have degree 1. Take 1 (delete 5), take 2 (delete 6), and then 4 and 7 have degree 0. Leaf with $\{1, 2, 4, 7\}$, size 4.

The answer is $\alpha = 4$ with $\{0, 3, 5, 6\}$, after 5 nodes, 3 leaves and 9 reductions. A plain search over all subsets would look at $2^8 = 256$ sets.

## Correctness

Each reduction keeps the answer. A vertex $v$ of degree 0 can be added to any independent set. For a vertex $v$ of degree 1 with neighbor $u$, a maximum independent set that contains $u$ can swap $u$ for $v$, so some maximum independent set contains $v$, and then none of $N(v)$. If $N[v] \subseteq N[u]$ for an edge $uv$, a maximum independent set $J$ that contains $u$ contains no other vertex of $N[u]$, hence no neighbor of $v$, and $J - u + v$ is independent and as large; so $u$ can be deleted. The two branches cover all independent sets of $H$: those without $v$, and those with $v$, which avoid $N(v)$. So the answer of each node is $|I| + \alpha(H)$, and it is the larger of the answers of its children. Each step deletes at least one vertex, so the search is finite. The [proof](proofs/correctness.md) gives the details.

## Complexity

Let $L(n)$ be the largest number of leaves of the search tree on a graph with at most $n$ vertices. The reductions only delete vertices, and a branch removes 1 vertex in one child and at least 4 in the other, so

$$L(n) \le L(n - 1) + L(n - 4),$$

with $L(n) = 1$ for $n \le 3$, as a graph with at most 3 vertices has no vertex of degree 3. The *branching vector* is $(1, 4)$, and its *branching number* is the positive root $\tau \approx 1.38028$ of $x^4 = x^3 + 1$. By induction, $L(n) \le \tau^n$. The tree has fewer inner nodes than leaves.

A node costs $O(n^4)$ as written: at most $n$ reductions, each found by a scan of $O(n^3)$ for the dominance test, and copying the graph takes $O(n^2)$. So the time is $O(1.3803^n n^4)$. The stack holds at most $n + 1$ graphs, as each branch deletes a vertex, so the space is $O(n^3)$ with adjacency sets.

## Properties

- **Exact.** It returns a maximum independent set.
- **Measured by the instance size.** The bound follows from the branching vector alone; it does not depend on bounds or on an incumbent, as in branch and bound.
- **Reductions decide the branching vector.** Without the degree rules, a branch on a vertex of degree 1 has vector $(1, 2)$ and branching number $1.618$; the reductions are what allow the vector $(1, 4)$.
- **Polynomial space.** The search is depth-first and keeps only the stack.
- **Path and cycle cases.** Graphs of maximum degree 2 are solved without branching.

## Variants and improvements

- **More cases.** Tarjan and Trojanowski (1977) gave an algorithm for maximum independent set with time $O(2^{n/3})$ by a careful case analysis of the branching.
- **Branching on degree.** Fomin and Kratsch develop branching algorithms for independent set in which the rules on small degrees and on dominated vertices give branching vectors better than $(1, 4)$.
- **Measure and conquer.** Fomin, Grandoni and Kratsch (2009) analyze such algorithms with a measure that weights vertices by their degree, instead of the number of vertices, and get better bounds for the same kind of algorithm; see [measure and conquer](/measure-and-conquer/).
- **Pruning by bound.** Adding a bound, such as $|I| + |V(H)| \le |best|$, makes it a [branch and bound](/depth-first-branch-and-bound/) and often cuts the tree in practice, with the same worst case.
- **Parameterized problems.** The same scheme with a parameter $k$ instead of $n$ gives [bounded search tree](/bounded-search-tree/) algorithms, for example for [vertex cover](/vertex-cover/), where the reductions are often [kernelization](/kernelization/) rules.

## When to use it

Use branch and reduce for exact solutions of NP-hard graph and satisfiability problems on instances of moderate size, and when a proved worst-case bound matters. The method is also the standard way to derive upper bounds of the form $O(c^n)$ in exact exponential algorithms.

## Pitfalls

- **Unsafe reductions.** Each rule must keep an optimal solution, not only a good one. The dominance rule deletes the vertex $u$ with the larger closed neighborhood, never $v$.
- **Branching before reducing.** If the search branches on a vertex of low degree, the branching vector becomes worse, and the bound fails.
- **Deep recursion.** A recursive version can reach depth $n$, so use an explicit stack for large graphs.
- **Small cases.** The proof needs every leaf case, here the union of cycles, to be solved correctly; a cycle of odd length $k$ has only $\lfloor k/2 \rfloor$ independent vertices.

## Implementations

## History

Tarjan and Trojanowski (1977) gave an algorithm for maximum independent set with time $O(2^{n/3})$, based on a case analysis of the branching. Fomin and Kratsch present the method as branch and reduce, with branching vectors and branching numbers as the tool of analysis. Fomin, Grandoni and Kratsch (2009) introduced measure and conquer to analyze such algorithms more tightly.

## References
