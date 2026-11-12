---
tag: BS0MJQ
kind: algorithm
slug: pruefer-decoding
name: Prüfer decoding
aliases:
- Pruefer decoding
- Prüfer sequence to tree
- Prufer decoding
- Decoding a Prüfer code
area: combinatorics/generating-partitions-and-trees
level: core
summary: Reconstructs the unique labeled tree from a Prüfer sequence in Θ(n) time, or Θ(n log n) with a heap of leaves.
solves: [labeled-tree-generation]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1918
  people: [Heinz Prüfer]
  note: Prüfer introduced the code in 1918 to give a new proof of Cayley's formula for the number of labeled trees.
prereqs: [pruefer-code, labeled-graph, free-tree-properties]
see_also: [pruefer-code, prufer-sequence, cayley-formula, labeled-tree-generation, uniform-spanning-tree-sampling, spanning-tree-enumeration, ranking-unranking, free-tree-generation]
sources:
  - url: https://cp-algorithms.com/graph/pruefer_code.html
    title: cp-algorithms, Prüfer code
    locator: the sections Restoring the tree using the Prüfer code, Restoring the tree using the Prüfer code in linear time, and Bijection between trees and Prüfer codes
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 2.2, Spanning trees and enumeration (the Prüfer code, the algorithm that rebuilds the tree from the code, and Cayley's formula)
  - paper: Heinz Prüfer, Neuer Beweis eines Satzes über Permutationen, Archiv der Mathematik und Physik, series 3, volume 27, 1918
    locator: pages 142 to 144, the original encoding of labeled trees by sequences
---

Prüfer decoding rebuilds the labeled tree on the vertex set $[n] = \{1, \ldots, n\}$ from its [Prüfer code](/pruefer-code/), a sequence $a_1, \ldots, a_{n-2}$ of elements of $[n]$. At step $i$ it joins $a_i$ to the smallest vertex that is not yet used and does not occur in $a_i, \ldots, a_{n-2}$, and at the end it joins the last such vertex to $n$. A pointer that only moves forward, plus one shortcut for a vertex that has just become a leaf, finds each of these vertices in $O(1)$ amortized time, so the whole tree takes $\Theta(n)$ time. Since every sequence in $[n]^{n-2}$ decodes to a different tree, decoding all of them lists all $n^{n-2}$ [labeled trees](/labeled-tree-generation/).

## In plain words

The code of a tree records, step by step, which vertex lost a leaf when the smallest leaf was cut off. To undo this, you must know which leaf was cut at each step. A vertex is still a leaf at some step exactly when its number does not appear again later in the code, because each later appearance means that it still has a leaf to lose. So, at each step, take the smallest unused vertex whose number does not appear in the rest of the code, and join it to the code letter.

To do this fast, count how many times each number still appears. A vertex with count 0 is a leaf. Keep a pointer that moves from small to large numbers to find the next leaf. When a vertex reaches count 0 and it is smaller than the pointer, it is the next leaf at once.

## The problem

The input is an integer $n \ge 2$ and a sequence $a = (a_1, \ldots, a_{n-2})$ with each $a_i \in [n]$. The output is the edge set of the tree $T$ on $[n]$ whose Prüfer code is $a$. The code of a tree is computed by removing the leaf with the smallest label $n - 2$ times and writing down the neighbor of the removed leaf each time. The [Prüfer sequence](/prufer-sequence/) page shows that this map from trees to $[n]^{n-2}$ is a bijection; the proof below shows it again, as a by-product of the correctness of decoding.

## The algorithm

Let $\deg[v]$ be one more than the number of times $v$ occurs in the part of the code not yet read. A vertex not yet used with $\deg[v] = 1$ is a leaf of the tree that is still to be built.

```pseudo id=main
PRUEFER-DECODE(a[1 .. n−2])
L1  for v ← 1 to n do deg[v] ← 1
L2  for i ← 1 to n − 2 do deg[a[i]] ← deg[a[i]] + 1
L3  ptr ← the smallest v with deg[v] = 1
L4  leaf ← ptr
L5  for i ← 1 to n − 2 do
L6      v ← a[i]; output the edge {leaf, v}
L7      deg[v] ← deg[v] − 1
L8      if deg[v] = 1 and v < ptr then leaf ← v
L9      else ptr ← ptr + 1; while deg[ptr] ≠ 1 do ptr ← ptr + 1
L10         leaf ← ptr
L11 output the edge {leaf, n}
L12 return the n − 1 edges
```

The variable $\mathit{leaf}$ is the leaf to remove at the current step. Line L8 is the shortcut: the code letter $v$ has just lost its last later occurrence, so it is a leaf now, and if it is below the pointer it is the smallest leaf. Otherwise line L9 moves the pointer to the next leaf. The used vertices keep $\deg = 1$, but they all lie at or below the pointer, so the scan of line L9 never meets them.

## Example

Decode $a = (4, 4, 2, 7, 7, 1)$, so $n = 8$. Line L2 gives $\deg = (2, 2, 1, 3, 1, 1, 3, 1)$ for the vertices $1, \ldots, 8$, and lines L3 and L4 give $\mathit{ptr} = \mathit{leaf} = 3$.

| $i$ | $v = a_i$ | edge | $\deg[v]$ after L7 | branch | $\mathit{ptr}$ | new $\mathit{leaf}$ |
|---|---|---|---|---|---|---|
| 1 | 4 | $\{3, 4\}$ | 2 | L9, scan | 5 | 5 |
| 2 | 4 | $\{5, 4\}$ | 1 | L8, $4 < 5$ | 5 | 4 |
| 3 | 2 | $\{4, 2\}$ | 1 | L8, $2 < 5$ | 5 | 2 |
| 4 | 7 | $\{2, 7\}$ | 2 | L9, scan | 6 | 6 |
| 5 | 7 | $\{6, 7\}$ | 1 | L9, $7 > 6$ | 7 | 7 |
| 6 | 1 | $\{7, 1\}$ | 1 | L8, $1 < 7$ | 7 | 1 |

Line L11 adds $\{1, 8\}$. The tree has the edges $\{3,4\}$, $\{4,5\}$, $\{2,4\}$, $\{2,7\}$, $\{6,7\}$, $\{1,7\}$ and $\{1,8\}$. Vertices 4 and 7 occur twice in the code and have degree 3; vertices 1 and 2 occur once and have degree 2; the other four vertices do not occur and are the leaves. Encoding this tree, by removing the smallest leaf six times, gives back $3 \to 4$, $5 \to 4$, $4 \to 2$, $2 \to 7$, $6 \to 7$ and $7 \to 1$, that is, the code $(4, 4, 2, 7, 7, 1)$.

## Correctness

Let $b_i$ be the leaf that the encoder removes at step $i$. In the tree that is left before step $i$, each vertex has degree one more than its number of occurrences in $a_i, \ldots, a_{n-2}$. So the leaves are the remaining vertices that do not occur later in the code, and $b_i$ is the smallest of them. This rule depends only on $a$, so the code determines the tree, and an induction on $n$ shows that every sequence is the code of the tree it determines. The algorithm computes the same $b_i$: line L8 and line L9 keep the invariant that all used vertices are at most $\mathit{ptr}$ and all other current leaves except $\mathit{leaf}$ are above it. Vertex $n$ is never the smallest of two or more candidates, so it is never removed, and the last edge is $\{b_{n-1}, n\}$. The full proof is below.

## Complexity

- **Time.** Lines L1 and L2 take $\Theta(n)$. The pointer starts at 1, only moves forward and never passes $n$, so all scans of line L9 together take $O(n)$ steps. Each pass of the main loop does $O(1)$ other work. The total is $\Theta(n)$, in the worst and in the best case, since the input alone has $n - 2$ letters.
- **Space.** The array $\deg$ of $n + 1$ entries and the output of $n - 1$ edges.
- **With a priority queue.** Keeping the current leaves in a [binary heap](/binary-heap/) and taking the minimum at each step is simpler to prove but costs $\Theta(n \log n)$.
- **The naive method.** Searching for the smallest leaf from scratch at every step costs $\Theta(n^2)$.

## Properties

- **Degrees.** The decoded tree has $\deg(v) = 1 + \#\{i : a_i = v\}$ for every $v$. So the leaves are the labels that do not occur in the code, and trees with a given degree sequence correspond to codes with given letter counts.
- **Bijection.** Different codes give different trees, and every tree on $[n]$ is the decoding of its own code. Hence there are $n^{n-2}$ labeled trees on $[n]$, which is [Cayley's formula](/cayley-formula/).
- **The last edge.** Vertex $n$ is never removed, so the last edge always contains $n$. For $n \ge 3$ the vertex $a_{n-2}$ is never removed either, so the last edge is $\{a_{n-2}, n\}$ when $a_{n-2} \ne n$.
- **Edge order.** The edges come out in the order in which the encoder removes the leaves. Orienting each edge $\{b_i, a_i\}$ from $b_i$ to $a_i$, and the last one toward $n$, gives the parent array of the tree rooted at $n$.

## Variants and improvements

- **Encoding.** The inverse map uses the same pointer idea: count the degrees, remove the smallest leaf, and when its neighbor becomes a leaf with a smaller label, remove it next. It also runs in $\Theta(n)$ time. See [Prüfer code](/pruefer-code/).
- **All labeled trees.** Run an odometer over $[n]^{n-2}$ and decode each sequence. This lists every tree once, with $O(n)$ time per tree. See [labeled tree generation](/labeled-tree-generation/) for faster ways to step from one tree to the next.
- **Ranking.** Reading the code $(a_1 - 1, \ldots, a_{n-2} - 1)$ as a number in base $n$ gives a rank in $[0, n^{n-2})$, and writing a number in base $n$ and decoding it unranks. See [ranking and unranking](/ranking-unranking/).
- **Random trees.** A uniform random code, decoded, gives a uniform random tree on $[n]$, in $O(n)$ time. This is a uniform [spanning tree](/uniform-spanning-tree-sampling/) of the complete graph $K_n$.
- **Given degrees.** A random arrangement of the multiset with $d_v - 1$ copies of each $v$ gives a uniform random tree with degrees $d_1, \ldots, d_n$, and listing the arrangements lists those trees.
- **Other codes.** Other bijections between trees on $[n]$ and $[n]^{n-2}$ exist, built on other rules for which leaf to remove. The algorithm above works for any total order on the labels.

## When to use it

Use Prüfer decoding to generate all labeled trees on a small vertex set, to draw uniform random labeled trees for tests, to store a labeled tree as $n - 2$ numbers, or to count labeled trees with constraints on the degrees. To list unlabeled trees, use [free tree generation](/free-tree-generation/) instead, because each unlabeled tree appears up to $n!$ times among the labeled ones.

## Pitfalls

- **0-based and 1-based labels.** With labels $0, \ldots, n-1$, the last edge goes to $n - 1$. Mixing the two conventions joins the last leaf to a vertex that does not exist.
- **Dropping the shortcut.** Without line L8, a vertex that becomes a leaf below the pointer is never found, and the output is wrong. Moving the pointer back instead makes the method $\Theta(n^2)$ in the worst case.
- **Small $n$.** For $n = 2$ the code is empty and the tree is the single edge $\{1, 2\}$. For $n = 1$ the tree has no edge, and the code length $n - 2$ is negative, so it needs a special case.
- **Invalid input.** A letter outside $[n]$ breaks the degree array. Check the range first.

## Implementations

## History

Prüfer introduced the code in 1918, in a new proof of the formula $n^{n-2}$ for the number of labeled trees that Cayley had stated in 1889. Textbooks such as West's present the rebuilding of the tree as the inverse of the removal process. The linear-time version with a forward pointer is standard in programming references such as cp-algorithms.

## References
