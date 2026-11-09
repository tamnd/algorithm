---
tag: 32F5MK
kind: algorithm
slug: tsukiyama-algorithm
name: Tsukiyama algorithm
aliases:
- Tsukiyama-Ide-Ariyoshi-Shirakawa algorithm
area: combinatorics/exhaustive-search
level: advanced
summary: Output-sensitive algorithm that lists all maximal independent sets with polynomial time per output.
solves: [maximal-independent-set-enumeration]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the number of maximal independent sets}
  time: {worst: O(n (n + m) k), best: O(n (n + m))}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: true}
history:
  year: 1977
  people: [Shuji Tsukiyama, Mikio Ide, Hiromu Ariyoshi, Isao Shirakawa]
  note: The first algorithm to list all maximal independent sets with time per set bounded by a polynomial, published in SIAM Journal on Computing in 1977.
prereqs: [maximal-independent-set, maximal-independent-set-enumeration, depth-first-search]
see_also: [maximal-independent-set-enumeration, maximal-clique-enumeration, bron-kerbosch, output-sensitive-enumeration, reverse-search, maximal-independent-set, independent-set, enumeration-problem]
sources:
  - paper: doi:10.1137/0206036
    title: Shuji Tsukiyama, Mikio Ide, Hiromu Ariyoshi and Isao Shirakawa, A new algorithm for generating all the maximal independent sets, SIAM Journal on Computing 6(3), 1977, 505 to 517
    locator: the extension of the maximal independent sets of the graph on the first i vertices to the graph on the first i + 1 vertices, the test that makes each set appear once, and the bound O(nmμ) time with O(n + m) space
  - paper: doi:10.1016/0020-0190(88)90065-8
    title: David S. Johnson, Mihalis Yannakakis and Christos H. Papadimitriou, On generating all maximal independent sets, Information Processing Letters 27(3), 1988, 119 to 123
    locator: the polynomial delay of the method of Tsukiyama and others, and the listing in lexicographic order with polynomial delay
  - paper: "Kazuhisa Makino and Takeaki Uno, New algorithms for enumerating all maximal cliques, in Algorithm Theory, SWAT 2004, Lecture Notes in Computer Science 3111, Springer, 2004, 260 to 272"
    locator: the parent-child form of the method of Tsukiyama and others, and faster versions with matrix multiplication and for sparse graphs
---

The Tsukiyama algorithm, by Tsukiyama, Ide, Ariyoshi and Shirakawa (1977), lists all [maximal independent sets](/maximal-independent-set/) of a graph with $n$ vertices and $m$ edges, each exactly once, in $O(n(n + m))$ time per set. It was the first method with a polynomial bound per output for this problem. It adds the vertices one at a time and turns each maximal independent set of the smaller graph into one or two maximal independent sets of the larger graph, with a test that gives each new set exactly one parent. Since every branch of the search ends in an output, the delay between two outputs is polynomial. The same algorithm on the complement graph lists all [maximal cliques](/maximal-clique-enumeration/).

## In plain words

An independent set is a group of vertices with no edge between any two of them. It is maximal when no other vertex can join without breaking this rule. A graph can have a very large number of maximal independent sets, and the goal is to list them all quickly.

The algorithm adds the vertices one by one. It keeps the maximal sets of the part of the graph seen so far. When a new vertex comes, each old set either takes the new vertex, if it fits, or stays as it is. It can also make a second set: drop the neighbors of the new vertex and add the new vertex. A simple rule decides which old set is in charge of making this second set, so no set is made twice. Every path in the search ends with a set to print, so no time is wasted.

## The problem

Given a simple undirected graph $G = (V, E)$ with $V = \{v_1, \ldots, v_n\}$, list every set $S \subseteq V$ that is independent (no edge has both ends in $S$) and maximal (every vertex outside $S$ has a neighbor in $S$). This is the problem of [maximal independent set enumeration](/maximal-independent-set-enumeration/). The number $k$ of such sets can be as large as $3^{n/3}$, so the goal is a bound per output.

## The algorithm

Let $G_i$ be the subgraph induced by $v_1, \ldots, v_i$, and $N(v)$ the set of neighbors of $v$. The search tree has the maximal independent sets of $G_i$ at level $i$. For a set $X$ that is independent in $G_i$, GREEDY$_i(X)$ adds $v_1, \ldots, v_i$ to $X$ in this order, each one that has no neighbor in the set so far. The result is the first maximal independent set of $G_i$, in this order, that contains $X$.

```pseudo id=main
TSUKIYAMA(S, i)                       ▷ S is a maximal independent set of G_i
L1  if i = n then OUTPUT(S) and return
L2  v ← v_{i+1}
L3  if S ∩ N(v) = ∅ then
L4      TSUKIYAMA(S ∪ {v}, i + 1)
L5  else
L6      TSUKIYAMA(S, i + 1)
L7      T ← (S \ N(v)) ∪ {v}
L8      if T is maximal in G_{i+1} and GREEDY_i(S \ N(v)) = S then
L9          TSUKIYAMA(T, i + 1)
```

The first call is TSUKIYAMA$(\emptyset, 0)$; the empty set is the only maximal independent set of the empty graph $G_0$. If $v$ has no neighbor in $S$, the only child is $S \cup \{v\}$ (line L4). Otherwise $S$ stays maximal in $G_{i+1}$, because $v$ has a neighbor in $S$ (line L6). The set $T$ of line L7 makes room for $v$ by dropping its neighbors. Line L8 accepts $T$ only if it is maximal and $S$ is the *canonical parent* of $T$: the greedy extension of $T \setminus \{v\}$ in $G_i$. So each maximal independent set of $G_{i+1}$ that holds $v$ but does not come from line L4 is made by exactly one $S$.

## Example

Take the 5-cycle with edges $v_1v_2$, $v_2v_3$, $v_3v_4$, $v_4v_5$, $v_5v_1$, and write $j$ for $v_j$.

| level $i$ | node $S$ | new vertex $v$ | children |
|---|---|---|---|
| 0 | $\emptyset$ | 1 | $\{1\}$ (line L4) |
| 1 | $\{1\}$ | 2 | $\{1\}$; $T = \{2\}$ is maximal in $G_2$ and GREEDY$_1(\emptyset) = \{1\}$, so also $\{2\}$ |
| 2 | $\{1\}$ | 3 | $\{1, 3\}$ (line L4) |
| 2 | $\{2\}$ | 3 | $\{2\}$; $T = \{3\}$ is not maximal in $G_3$, since 1 has no neighbor in it |
| 3 | $\{1, 3\}$ | 4 | $\{1, 3\}$; $T = \{1, 4\}$ is maximal and GREEDY$_3(\{1\}) = \{1, 3\}$, so also $\{1, 4\}$ |
| 3 | $\{2\}$ | 4 | $\{2, 4\}$ (line L4) |
| 4 | $\{1, 3\}$ | 5 | $\{1, 3\}$; $T = \{3, 5\}$ is maximal and GREEDY$_4(\{3\}) = \{1, 3\}$, so also $\{3, 5\}$ |
| 4 | $\{1, 4\}$ | 5 | $\{1, 4\}$; $T = \{5\}$ is not maximal, since 2 has no neighbor in it |
| 4 | $\{2, 4\}$ | 5 | $\{2, 4\}$; $T = \{2, 5\}$ is maximal and GREEDY$_4(\{2\}) = \{2, 4\}$, so also $\{2, 5\}$ |

The outputs at level 5, in order, are $\{1, 3\}$, $\{3, 5\}$, $\{1, 4\}$, $\{2, 4\}$, $\{2, 5\}$: the five maximal independent sets of the 5-cycle, each once. The two rejected sets $\{3\}$ and $\{5\}$ are not maximal at their level, and their subtrees would only repeat sets that the tree reaches in another way.

## Correctness

The claim is that, for each $i$, the nodes at level $i$ are exactly the maximal independent sets of $G_i$, each once. It holds at level 0. For the step, every child is a maximal independent set of $G_{i+1}$: $S \cup \{v\}$ because $S$ was maximal in $G_i$, $S$ because $v$ has a neighbor in $S$, and $T$ by the test of line L8. Conversely, a maximal independent set $T$ of $G_{i+1}$ has exactly one parent. If $v \notin T$, its parent is $T$ itself, through line L6. If $v \in T$ and $T \setminus \{v\}$ is maximal in $G_i$, its parent is $T \setminus \{v\}$, through line L4. If $v \in T$ and $T \setminus \{v\}$ is not maximal, its only possible parent is GREEDY$_i(T \setminus \{v\})$, through line L9, and the maximality of $T$ shows that this parent produces exactly $T$ at line L7. The full proof is below.

## Complexity

Every node at a level below $n$ has one or two children, so every branch reaches level $n$ and ends in an output. The tree has $k$ leaves and height $n$, so it has at most $nk + 1$ nodes. At each node, lines L3, L7 and the two tests of line L8 take $O(n + m)$ time with adjacency lists and a marker array. The total time is $O(n(n + m)k)$, and the best case, a graph with one maximal independent set, takes $O(n(n + m))$.

The delay is also bounded. Between two consecutive outputs, the depth-first search climbs at most $n$ levels and descends at most $n$ levels, and it meets no dead end. So the time from one output to the next is $O(n(n + m))$: the algorithm has polynomial delay.

The simple recursive form keeps a set at each of the $n$ levels, which is $O(n^2)$ space. The original paper keeps one set and a record of the changes at each level, and needs only $O(n + m)$ space.

## Properties

- **Polynomial delay.** At most $O(n(n + m))$ time between two outputs, before the first and after the last.
- **No repeats and no dead ends.** Each maximal independent set has exactly one path from the root.
- **Output order.** Fixed by the vertex order. It is not lexicographic in general.
- **Deterministic and depth-first.** The search can stop after any number of outputs.

## Variants and improvements

- **Maximal cliques.** The maximal independent sets of the complement graph are the maximal cliques of $G$. The [Bron-Kerbosch algorithm](/bron-kerbosch/) with pivoting is often faster in practice, and with a good pivot rule it lists all maximal cliques in $O(3^{n/3})$ worst-case time, which matches the largest possible output.
- **Lexicographic order.** Johnson, Yannakakis and Papadimitriou (1988) list the maximal independent sets in lexicographic order with polynomial delay, using a priority queue and exponential space. In reverse lexicographic order no polynomial delay is possible unless $\mathrm{P} = \mathrm{NP}$.
- **Faster per output.** Makino and Uno (2004) give a reverse search form with time per output bounded by matrix multiplication for dense graphs, and by the maximum degree for sparse graphs. Chiba and Nishizeki (1985) list maximal cliques in time proportional to the arboricity times $m$ per clique.
- **Reverse search view.** The parent of a set at level $n$ can be computed directly, which places the method in the frame of [reverse search](/reverse-search/).

## When to use it

Use the algorithm when a guaranteed bound per output matters, for example when the graph is adversarial or when the output is consumed as a stream. On typical sparse graphs from practice, a Bron-Kerbosch search with pivoting and a degeneracy order is usually faster. If only the size of a largest independent set is needed, use an exact [maximum independent set](/maximum-independent-set/) algorithm instead.

## Pitfalls

- **Missing the parent test.** Without the GREEDY test of line L8, the same set is produced from several parents.
- **Missing the maximality test.** Without it, the search enters subtrees that only repeat sets or end with non-maximal sets.
- **Comparing with the wrong graph.** GREEDY uses the graph $G_i$, without the new vertex, and the maximality test uses $G_{i+1}$, with it.
- **Shared mutable sets.** In a recursive program, a child that changes the set of its parent in place must undo the change before the parent goes on.
- **Self-loops.** A vertex with a loop is in no independent set. Remove such vertices or reject the input.

## Implementations

## History

Tsukiyama, Ide, Ariyoshi and Shirakawa published the algorithm in 1977, with the bound $O(nm\mu)$ for $\mu$ maximal independent sets and $O(n + m)$ space. Johnson, Yannakakis and Papadimitriou (1988) gave the formal definitions of polynomial delay and noted that this method has it. Later work by Chiba and Nishizeki (1985), Makino and Uno (2004), and others improved the time per output for cliques in sparse and dense graphs.

## References
