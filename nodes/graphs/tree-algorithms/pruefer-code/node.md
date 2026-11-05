---
tag: YTVMT5
kind: concept
slug: pruefer-code
name: Prüfer code
aliases:
- Pruefer code
- Prufer code
- Prüfer sequence
area: graphs/tree-algorithms
level: core
summary: A bijection between labeled trees on n vertices and sequences of length n-2 over {1..n}.
prereqs: [prufer-sequence, tree-rooting, degree]
see_also: [prufer-sequence, cayley-formula, tree-center-leaf-peeling, parent-pointer-tree, labeled-graph, matrix-tree-theorem, uniform-spanning-tree-sampling, tree-edge-count]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 2.2 (Spanning trees and enumeration), the Prüfer code, the algorithm that rebuilds the tree from the code, and Cayley's formula
  - paper: Heinz Prüfer, Neuer Beweis eines Satzes über Permutationen, Archiv der Mathematik und Physik, series 3, volume 27, 1918
    locator: pages 142 to 144, the original encoding of labeled trees by sequences
  - url: https://cp-algorithms.com/graph/pruefer_code.html
    title: cp-algorithms, Prüfer code
    locator: the encoding and decoding in O(n log n) time with a set, and in O(n) time with a pointer to the smallest leaf
---

The Prüfer code turns a labeled [tree](/tree/) on $n \ge 2$ vertices into a sequence of $n - 2$ labels, and back, by removing the smallest leaf again and again and writing down its neighbour. The bijection itself and its use for [Cayley's formula](/cayley-formula/) are on the [Prüfer sequence](/prufer-sequence/) page. This page is about the computation: with the vertices numbered $0, \ldots, n-1$, both directions run in $\Theta(n)$ time without a heap, by a pointer that only moves up and a shortcut for a neighbour that has just become a small leaf.

## In plain words

Number the dots of a tree from 0 up. Find the leaf with the smallest number, write down the dot it hangs from, and erase the leaf. Repeat until two dots are left. The list you wrote is the code.

To do this fast, do not search the whole tree for the smallest leaf each time. Keep a finger on the numbers and move it only to the right. There is one exception: when you erase a leaf, the dot it hung from may become a leaf. If its number is below your finger, it is the next smallest leaf, so take it at once. Otherwise move the finger right to the next leaf. The finger crosses each number once, so the whole job takes time in step with the number of dots. Rebuilding the tree from the code works the same way.

## The idea

**Conventions.** The tree is free, not weighted, and has the vertices $0, \ldots, n-1$ with $n \ge 2$. The code is the sequence $(a_1, \ldots, a_{n-2})$ with entries in $\{0, \ldots, n-1\}$; it is the code of the [Prüfer sequence](/prufer-sequence/) page with every label lowered by one. For $n = 2$ it is empty, and for $n = 1$ it is not defined. Each vertex $v$ occurs $\deg(v) - 1$ times in the code, so the leaves are the vertices that do not occur.

**The vertex $n - 1$ stays.** While the tree has two or more leaves, the smallest leaf is not $n - 1$. So $n - 1$ is never removed, it is one of the two vertices left at the end, and the neighbour of each removed vertex is its parent when the tree is rooted at $n - 1$. The encoder therefore first [roots the tree](/tree-rooting/) at $n - 1$ and stores a [parent array](/parent-pointer-tree/) $p$, with an iterative search, and then never looks at the adjacency lists again.

**Encoding in linear time.** Keep $\deg[v]$, a pointer $\mathit{ptr}$, and the current leaf $\mathit{leaf}$.

1. Compute $p$ and $\deg$. Set $\mathit{ptr}$ to the smallest $v$ with $\deg[v] = 1$, and $\mathit{leaf} \leftarrow \mathit{ptr}$.
2. For $i = 1, \ldots, n - 2$: let $a \leftarrow p[\mathit{leaf}]$, write $a_i \leftarrow a$, and lower $\deg[a]$ by one.
3. If $\deg[a] = 1$ and $a < \mathit{ptr}$, set $\mathit{leaf} \leftarrow a$. Otherwise move $\mathit{ptr}$ up to the next $v > \mathit{ptr}$ with $\deg[v] = 1$, and set $\mathit{leaf} \leftarrow \mathit{ptr}$.

**Why the pointer is right.** At the start of each step, two facts hold: $\mathit{leaf} \le \mathit{ptr}$ is the smallest leaf, and every other leaf of the current tree is larger than $\mathit{ptr}$. Each removed vertex was the current $\mathit{leaf}$ at its step, and $\mathit{ptr}$ never goes down, so every removed vertex is at most $\mathit{ptr}$. Removing $\mathit{leaf}$ can make only one new leaf, its neighbour $a$. If $a$ is a leaf and $a < \mathit{ptr}$, it is smaller than all other leaves, and the shortcut takes it. If not, every leaf is larger than $\mathit{ptr}$, and the scan from $\mathit{ptr} + 1$ meets only vertices that are still in the tree, since the removed ones are at most $\mathit{ptr}$. So the first $v$ with $\deg[v] = 1$ is the smallest leaf. The stale counter $\deg[\mathit{leaf}] = 1$ of a removed vertex never misleads the scan.

**Cost.** The rooting takes $\Theta(n)$ time. Each step does $O(1)$ work besides the scan, and the scan moves $\mathit{ptr}$ from $0$ to at most $n - 1$ in total. So the encoder takes $\Theta(n)$ time and $\Theta(n)$ extra words. A min-heap of the leaves gives a simpler $O(n \log n)$ method.

**Decoding in linear time.** Given the code, set $\deg[v] = 1 + $ the number of times $v$ occurs. Set $\mathit{ptr}$ and $\mathit{leaf}$ as in step 1. For $i = 1, \ldots, n-2$: add the edge $\{\mathit{leaf}, a_i\}$, lower $\deg[a_i]$ by one, and choose the next leaf by step 3 with $a = a_i$. At the end, add the edge $\{\mathit{leaf}, n - 1\}$. The same invariant holds, so the decoder also takes $\Theta(n)$ time. The last edge goes to $n - 1$ because $n - 1$ is never chosen while another vertex has counter 1, as above.

**Peeling one leaf, not all leaves.** The encoder removes leaves one at a time in order of label, so it is not the [leaf peeling](/tree-center-leaf-peeling/) of the centre algorithm, which removes all leaves of a round together. Both use the same degree counters, and both rely on the fact that removing a leaf leaves a tree whose only possible new leaf is the neighbour.

## Examples

Take the tree on $\{0, \ldots, 7\}$ with the edges $01, 02, 13, 14, 25, 46, 47$. Rooted at $7$, its parents are $p = [1, 4, 0, 1, 7, 2, 4, -1]$, and its degrees are $2, 3, 2, 1, 3, 1, 1, 1$.

| step | $\mathit{ptr}$ | $\mathit{leaf}$ removed | $a_i$ | new counter of $a_i$ | next leaf |
|---|---|---|---|---|---|
| 1 | 3 | 3 | 1 | 2 | scan to 5 |
| 2 | 5 | 5 | 2 | 1, and $2 < 5$ | 2 (shortcut) |
| 3 | 5 | 2 | 0 | 1, and $0 < 5$ | 0 (shortcut) |
| 4 | 5 | 0 | 1 | 1, and $1 < 5$ | 1 (shortcut) |
| 5 | 5 | 1 | 4 | 2 | scan to 6 |
| 6 | 6 | 6 | 4 | 1, and $4 < 6$ | 4, the last leaf |

The code is $(1, 2, 0, 1, 4, 4)$, and the vertices left are $4$ and $7$. The vertices $1$ and $4$ have degree 3 and occur twice, $0$ and $2$ have degree 2 and occur once, and the leaves $3, 5, 6, 7$ do not occur. Decoding starts from the counters $2, 3, 2, 1, 3, 1, 1, 1$ and adds the edges $31, 52, 20, 01, 14, 64$ in the same order, and then $\{4, 7\}$.

The small cases:

- **One edge** ($n = 2$). The code is empty, and the decoder adds only the last edge $\{0, 1\}$.
- **Path** $0, 1, \ldots, n-1$. The smallest leaf is always the left end, so the code is $(1, 2, \ldots, n-2)$, and every step after the first uses the shortcut.
- **Star** with centre $0$ and $n \ge 3$. The leaves $1, 2, \ldots, n-2$ are removed in order, so the code is $(0, 0, \ldots, 0)$, and the vertices left are $0$ and $n - 1$. With the centre at $c$, the code is $c$ written $n - 2$ times.

## Where it is used

- **Random labeled trees.** Decoding a uniform random sequence in $\{0, \ldots, n-1\}^{n-2}$ gives a uniform random labeled tree in $\Theta(n)$ time, which is a common way to make test inputs for tree algorithms.
- **Counting and listing.** The code proves [Cayley's formula](/cayley-formula/) and counts trees with given degrees. Listing all sequences lists all labeled trees, $n^{n-2}$ of them, which the [matrix-tree theorem](/matrix-tree-theorem/) also counts.
- **Compact storage.** A labeled tree is stored as $n - 2$ numbers, and every sequence of the right length is a valid tree, so no check is needed after a change. Search methods on trees use this, although a change of one entry can change many edges.
- **Contest problems.** Questions on labeled trees with given degrees, or on the number of ways to connect $k$ components into one tree, reduce to counting codes.

## References
