---
tag: EZ41AA
kind: algorithm
slug: tree-diameter-double-sweep
name: Tree diameter by double sweep
aliases:
- two-BFS tree diameter
area: graphs/tree-algorithms
level: intro
summary: Search from any node to the farthest node, then from there; the second distance is the diameter.
solves: [tree-diameter]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, weighted: true}
prereqs: [tree-diameter, depth-first-search, breadth-first-search]
see_also: [tree-center, tree-center-leaf-peeling, eccentricity, tree-dynamic-programming, rerooting-technique, iterative-depth-first-search, lowest-common-ancestor, tree-isomorphism]
sources:
  - paper: Ruud W. Bulterman, Frans W. van der Sommen, Gerard Zwaan, Tom Verhoeff, A. J. M. van Gasteren and W. H. J. Feijen, On computing a longest path in a tree, Information Processing Letters 81(2), 93 to 96 (2002)
    locator: the whole note, the two-search method and its correctness proof
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 22.2 (Breadth-first search), Exercise 22.2-8 (the diameter of a tree)
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 14, Tree algorithms, Section 14.2 (Diameter, Algorithm 2, two depth-first searches)
---

The double sweep finds the [diameter of a tree](/tree-diameter/) with two searches. The first search starts at any vertex and finds a vertex $a$ that is farthest from it. The second search starts at $a$ and finds a vertex $b$ farthest from $a$. Then $d(a, b)$ is the diameter, and the path from $a$ to $b$ is a longest path of the tree. The method works for unweighted trees and for trees with non-negative edge lengths, and it takes $\Theta(n)$ time, since each search visits each vertex once.

## In plain words

Stand in any town of a tree-shaped road network and find the town that is farthest away. Walk there. Now find the town that is farthest from this new place. The route between these two towns is a longest route in the whole network.

Why does this work? The first far town lies at an end of the network, at the tip of some longest route. From such a tip, the town farthest away is the other tip of a longest route. Each search is a walk through the network that records the distance to each town, so the work is two walks.

## The problem

The input is a free tree with the vertices $0, \ldots, n-1$, $n \ge 1$, and $n - 1$ edges $(u, v, w)$, where $w \ge 0$ is the length of the edge. An unweighted tree has $w = 1$ on each edge. No root is given. The output is the diameter $D = \max_{u, v} d(u, v)$, where $d$ is the length of the unique path, together with one path that has length $D$. This is the [tree diameter](/tree-diameter/) problem.

## The algorithm

```pseudo id=main
DOUBLE-SWEEP(T)                         ▷ T: a tree on 0 .. n−1, lengths w ≥ 0
L1  (d, ·) ← DISTANCES(T, 0)
L2  a ← a vertex with the largest d[a]
L3  (d, par) ← DISTANCES(T, a)
L4  b ← a vertex with the largest d[b]
L5  path ← [b]
L6  while the last vertex of path is not a do
L7      append par[last vertex of path] to path
L8  return (d[b], path reversed)

DISTANCES(T, s)                         ▷ one search of the tree from s
L9  d[s] ← 0, par[s] ← −1, mark s, S ← a stack that holds s
L10 while S is not empty do
L11     u ← POP(S)
L12     for each neighbour v of u, with edge length w, that is not marked do
L13         mark v, d[v] ← d[u] + w, par[v] ← u
L14         PUSH(S, v)
L15 return (d, par)
```

DISTANCES is a search that reaches each vertex once. In a tree, the first time a vertex $v$ is found, it is found from its neighbour on the unique path from $s$, so $d[v]$ is the true distance and no priority queue is needed. The search can use a stack, as here, or a queue, as in [breadth-first search](/breadth-first-search/); the order does not matter. The explicit stack avoids recursion, so a path of $10^5$ vertices is safe in Python. Lines L5 to L7 follow the parent links from $b$ back to $a$ to list the path.

## Example

Take the weighted tree on $\{0, \ldots, 6\}$ with the edges $01$ of length $2$, $12$ of length $7$, $13$ of length $3$, $04$ of length $4$, $45$ of length $1$ and $46$ of length $5$.

```
            0
       2 /     \ 4
        1       4
     7 / \ 3  1/ \ 5
      2   3   5   6
```

| step | from | distances to $0, 1, 2, 3, 4, 5, 6$ | farthest |
|---|---|---|---|
| first sweep (L1, L2) | $0$ | $0, 2, 9, 5, 4, 5, 9$ | $a = 2$ (tied with $6$) |
| second sweep (L3, L4) | $2$ | $9, 7, 0, 10, 13, 14, 18$ | $b = 6$ |

The diameter is $D = 18$. The parent links of the second sweep give $6 \to 4 \to 0 \to 1 \to 2$, so the path is $2, 1, 0, 4, 6$, with lengths $7 + 2 + 4 + 5 = 18$. Had line L2 picked $a = 6$ from the tie, the second sweep would have found $b = 2$ and the same value.

On the unweighted tree with the edges $01, 02, 13, 14, 25, 46, 47$, the first sweep from $0$ finds a vertex at distance $3$ ($6$ or $7$), and the second sweep from it finds $5$ at distance $D = 5$. On the single vertex, both sweeps return $0$, and $D = 0$. On the path $0, \ldots, n-1$, the first sweep finds $a = n - 1$ and the second finds $b = 0$, with $D = n - 1$. On a star with $n \ge 3$, the first sweep from the centre finds a leaf, and the second finds another leaf at distance $2$.

## Correctness

Let $x, y$ be the ends of a diametral path $P$, and for each vertex $v$ let $\pi(v)$ be the vertex of $P$ closest to $v$ and $h(v) = d(v, \pi(v))$. In a tree, the path from $v$ to each vertex $z$ of $P$ passes through $\pi(v)$, so $d(v, z) = h(v) + d(\pi(v), z)$. The key lemma is that a farthest vertex $a$ from any start $s$ has $\mathrm{ecc}(a) = D$. The proof compares $d(s, a)$ with $d(s, x)$ and $d(s, y)$, in two cases: $\pi(a) = \pi(s)$, or $\pi(a) \ne \pi(s)$. In both cases it gives $d(a, x) \ge D$ or $d(a, y) \ge D$. The case $\pi(a) = \pi(s)$ uses $d(s, a) \le h(s) + h(a)$, which needs $w \ge 0$. Then the second sweep, from $a$, finds a vertex $b$ with $d(a, b) = \mathrm{ecc}(a) = D$. The full proof, with the proof of DISTANCES, is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model with adjacency lists.

- **DISTANCES.** Each vertex is marked and pushed once, and popped once. When a vertex $u$ is popped, line L12 reads its adjacency list, of length $\deg u$. The total is $\sum_u \deg u = 2(n - 1)$ by the [tree edge count](/tree-edge-count/). So one call takes $\Theta(n)$ time.
- **Lines L2 and L4** each scan $n$ distances. Lines L5 to L7 follow at most $n - 1$ parent links.

So the time is $\Theta(n)$ in every case, and the extra space is $\Theta(n)$ for $d$, $par$, the marks and the stack. On a star, the stack holds $n - 1$ vertices at once.

## Properties

- **Deterministic.** The result depends only on the tie-breaking rule at lines L2 and L4, and the value $D$ does not depend on it.
- **Not recursive.** Both searches use an explicit stack.
- **Any start.** Line L1 may start at any vertex, not only $0$.
- **Ends of diameters.** The proof shows more: each vertex that is farthest from some vertex is an end of a diametral path.
- **Eccentricities for free.** With $d_a$ and $d_b$, the distances from $a$ and from $b$, $\mathrm{ecc}(v) = \max(d_a(v), d_b(v))$ for each vertex $v$. So one third sweep from $b$ gives all [eccentricities](/eccentricity/), the radius and the centre.

## Variants and improvements

- **Breadth-first sweeps.** On an unweighted tree, use a queue. The last vertex dequeued is a farthest vertex, so line L2 needs no scan.
- **Dynamic programming.** The [tree dynamic program](/tree-dynamic-programming/) that adds the two largest child heights at each vertex finds $D$ in one postorder pass and also works with negative lengths.
- **Centre.** The middle of the path $a, \ldots, b$ is the [tree centre](/tree-center/). For an unweighted tree, it is the vertex at position $\lfloor D/2 \rfloor$ of the path, plus the vertex at position $\lceil D/2 \rceil$ when $D$ is odd.
- **General graphs.** On a general graph, the double sweep with breadth-first search returns the eccentricity of some vertex, which is a lower bound on the diameter. It is exact on trees, but not on all graphs.
- **Iterated sweeps.** Heuristics for large sparse graphs repeat the sweep from new start vertices to raise the lower bound.

## When to use it

Use the double sweep for the diameter of a tree with non-negative lengths when you also want the path or the ends: it is short, needs no recursion and gives the ends $a$ and $b$, which also yield the centre and all eccentricities. Use the dynamic program when lengths can be negative, when you need the diameter of every subtree, or when the diameter is part of a larger bottom-up computation. For many diameter queries on a tree that grows, keep the ends and use [LCA](/lowest-common-ancestor/) distances.

## Pitfalls

- **Negative lengths.** On the path $0, 1, 2$ with $w(01) = -2$ and $w(12) = 1$, line L1 gives the distances $0, -2, -1$, line L2 picks $a = 0$, and the result is $0$, while $D = 1$. Use the dynamic program when some length is negative.
- **Returning the first distance.** The largest value of the first sweep (line L2) is only $\mathrm{ecc}(0)$, which can be as small as about $D/2$. The answer is the largest value of the second sweep, at line L4.
- **Recursive search.** A recursive DISTANCES overflows the call stack on a path of $10^5$ vertices in Python. Keep the explicit stack of lines L9 to L14.
- **Counting vertices instead of edges.** Some problems define the diameter as the number of vertices on the path, which is $D + 1$ in the unweighted case. Check the definition before returning $d[b]$.
- **General graphs.** Using the double sweep on a graph with cycles gives only a lower bound on the diameter.

## Implementations

## History

The two-search method is folklore, and its first source is not clear. Bulterman and coauthors, in a note of 2002, give a careful proof of its correctness for trees. CLRS pose the diameter of a tree as an exercise of the section on breadth-first search, and Laaksonen's handbook gives both the two-search method and the dynamic program.

## References
