---
tag: 87C07Z
kind: data-structure
slug: parent-pointer-tree
name: Parent-pointer tree
aliases:
- parent array
- parent pointers
area: graphs/graph-representation
level: intro
summary: Rooted tree stored as an array in which each vertex records its parent.
implements: [tree]
model: word-ram
complexity:
  vars: {n: the number of vertices, h: the depth of the vertex of the call}
  time: {worst: O(1 + h)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [tree, rooted-tree]
see_also: [disjoint-set-forest, left-child-right-sibling, breadth-first-search, bfs-tree, lowest-common-ancestor, binary-lifting, functional-graph, counting-sort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.3 (Representing rooted trees); Section 20.2, the predecessor attribute and the breadth-first tree; Section 19.3 (Disjoint-set forests)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.3 (Other representations of trees), trees with parent links only, and Algorithm E for equivalence classes
  - book: isbn:9780201000238
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, Data Structures and Algorithms, Addison-Wesley, 1983
    locator: Chapter 3 (Trees), the array representation by parents
---

A parent-pointer tree stores a [rooted tree](/rooted-tree/) on the vertices $0, \ldots, n - 1$ as one array $\text{parent}$, in which $\text{parent}[x]$ is the parent of $x$ and NIL marks the root. It is the smallest pointer form of a [tree](/tree/): one word per vertex, with $O(1)$ access to the parent and $O(1 + h)$ time to walk from a vertex of depth $h$ to the root. It cannot list the children of a vertex without scanning the whole array, so it is the form for algorithms that only walk up. The predecessor array $\pi$ of [breadth-first search](/breadth-first-search/), [depth-first search](/depth-first-search/) and shortest-path algorithms, and the [disjoint-set forest](/disjoint-set-forest/), are parent-pointer trees, and one $\Theta(n)$ pass of [counting sort](/counting-sort/) turns the array into child lists when an algorithm must walk down.

## In plain words

Give every person in a family a number. On one sheet of paper, write next to each number the number of that person's mother. The oldest ancestor has no mother on the sheet, so you write "none" there.

To find all the ancestors of a person, read their mother, then her mother, and so on until you reach "none". That is fast. To find all the children of a person, there is no shortcut: you must read the whole sheet and pick out the people whose mother is that person. If you need children often, sort the sheet by mother once, and then each list of children is one block of the sorted sheet.

## The abstract type

The structure implements the [tree](/tree/) type for a rooted tree, or a forest of rooted trees, in which the children of a vertex need no order. The operations here are:

- `parent(T, x)`, and `root-of(T, x)`, the root of the tree that holds $x$.
- `add-child(T, p) → x`, a new leaf $x$ with the parent $p$.
- `path-to-root(T, x)`, the vertices $x, \text{parent}(x), \ldots$ up to the root, and `depth(T, x)`, the number of edges on it.
- `child-lists(T)`, the children of every vertex at once.
- `children(T, v)`, by a scan of the array.

## Representation

The tree $T$ has a count $T.n$ and an array $T.\text{parent}[0 \,..\, n - 1]$ of integers. Vertices are the indices $0, \ldots, n - 1$, and NIL is a value that is not an index, such as $-1$. Data on vertices, such as keys, depths or ranks, is kept in other arrays with the same index.

**Invariant.**

- **(P1)** For each $x$, $\text{parent}[x]$ is NIL or an index in $\{0, \ldots, n - 1\}$.
- **(P2)** For each $x$, the sequence $x, \text{parent}[x], \text{parent}[\text{parent}[x]], \ldots$ reaches NIL after at most $n$ steps. That is, the parent links have no cycle.

A vertex $x$ with $\text{parent}[x] = $ NIL is a root. Under (P1) and (P2), the edges $\{x, \text{parent}[x]\}$ form a forest with one tree for each root, and $T$ is a tree when it has exactly one root. The edges number $n$ minus the number of roots. Read as a directed graph with the edges $(x, \text{parent}[x])$, the array is a [functional graph](/functional-graph/) with the roots removed from its domain, and (P2) says that this graph has no cycle.

Some code marks a root $r$ by $\text{parent}[r] = r$ instead of NIL. That is a [self-loop](/self-loop/), and (P2) then reads "reaches a fixed point". The disjoint-set forest of CLRS uses this form.

## Operations

```pseudo id=main
ADD-CHILD(T, p)                     ▷ p is a vertex of T; returns the new vertex
L1  x ← T.n
L2  T.parent[x] ← p;  T.n ← T.n + 1
L3  return x

PATH-TO-ROOT(T, x)
L4  while x ≠ NIL do
L5      report x
L6      x ← T.parent[x]

CHILD-LISTS(T)                      ▷ the children of v are kids[off[v] .. off[v+1] − 1]
L7  off[0 .. n] ← 0
L8  for x ← 0 to n − 1 do if T.parent[x] ≠ NIL then off[T.parent[x] + 1] ← off[T.parent[x] + 1] + 1
L9  for v ← 1 to n do off[v] ← off[v] + off[v − 1]
L10 next[0 .. n − 1] ← off[0 .. n − 1]
L11 for x ← 0 to n − 1 do
L12     if T.parent[x] ≠ NIL then
L13         kids[next[T.parent[x]]] ← x
L14         next[T.parent[x]] ← next[T.parent[x]] + 1
L15 return (off, kids)
```

**Add a child.** Lines L1 to L3 give the new vertex the next free index and record its parent. With $\text{parent}$ in a [dynamic array](/dynamic-array/), this costs $O(1)$ amortized time.

**Walk up.** Lines L4 to L6 report the path from $x$ to its root. The last vertex reported is `root-of`$(x)$, and the number of steps minus one is `depth`$(x)$. Each step is one array read.

**Child lists.** Lines L7 to L15 are a stable [counting sort](/counting-sort/) of the non-root vertices by their parent. Line L8 counts the children of each vertex into $\text{off}[v + 1]$. Line L9 takes [prefix sums](/prefix-sums/), so $\text{off}[v]$ is the number of non-root vertices whose parent is less than $v$, which is where the block of $v$ starts. Lines L11 to L14 put each vertex into the next free slot of its parent's block. The result is the [compressed sparse row](/compressed-sparse-row/) form of the child lists, and in each block the children appear in increasing order, because line L11 visits $x$ in increasing order.

**Children of one vertex.** Without child lists, the children of $v$ are the $x$ with $\text{parent}[x] = v$, found by a scan of all $n$ entries.

**Lowest common ancestor.** For $u$ and $v$ in one tree, compute both depths, move the deeper vertex up until the depths are equal, then move both up together until they meet. This takes $O(1 + \text{depth}(u) + \text{depth}(v))$ time. Faster methods, such as [binary lifting](/binary-lifting/), add tables to the parent array; see [lowest common ancestor](/lowest-common-ancestor/).

## Example

Take $n = 7$ and $\text{parent} = [\text{NIL}, 3, 0, 0, 3, 2, 4]$. Vertex 0 is the root; its children are 2 and 3; the children of 3 are 1 and 4; 5 is a child of 2 and 6 is a child of 4.

```
          0
        /   \
       2     3
       |    / \
       5   1   4
               |
               6
```

**Walk up from 6.** PATH-TO-ROOT reports $6, 4, 3, 0$ and stops at $\text{parent}[0] = $ NIL. So `root-of`$(6) = 0$ and `depth`$(6) = 3$. The lowest common ancestor of 1 and 6: the depths are 2 and 3, so 6 moves up to 4, and then $1 \to 3$ and $4 \to 3$ meet at 3.

**Child lists.** Line L8 counts 2 children for 0, 1 for 2, 2 for 3 and 1 for 4.

| step | array |
|---|---|
| after L8 | $\text{off} = [0, 2, 0, 1, 2, 1, 0, 0]$ |
| after L9 | $\text{off} = [0, 2, 2, 3, 5, 6, 6, 6]$ |
| after L15 | $\text{kids} = [2, 3, 5, 1, 4, 6]$ |

The children of 0 are $\text{kids}[0..1] = 2, 3$; of 1, the empty block $\text{kids}[2..1]$; of 2, $\text{kids}[2] = 5$; of 3, $\text{kids}[3..4] = 1, 4$; of 4, $\text{kids}[5] = 6$. The blocks hold the $6 = n - 1$ non-root vertices once each.

**Growing the tree.** ADD-CHILD$(T, 5)$ returns $x = 7$ and sets $\text{parent}[7] = 5$. Now `depth`$(7) = 3$, along $7, 5, 2, 0$.

## Correctness

ADD-CHILD keeps (P1) because $p$ is a vertex. It keeps (P2) because the new vertex $x$ has no children: no old chain passes through $x$, so the old chains are unchanged, and the chain of $x$ is $x$ followed by the chain of $p$, which reaches NIL by (P2). PATH-TO-ROOT reports the chain of $x$, and it stops because (P2) bounds the chain by $n$ steps. CHILD-LISTS is a counting sort of the non-root vertices by the key $\text{parent}[x]$: after line L9, $\text{off}[v]$ is the number of non-root vertices with key less than $v$, so the vertices with key $v$ fill exactly the positions $\text{off}[v], \ldots, \text{off}[v + 1] - 1$, and line L11 fills them in increasing order of $x$. The full proofs are in `proofs/correctness.md`.

## Complexity

The model is the [word RAM](/word-ram/), with a vertex index in one word. The times are worst case; $h$ is the depth of the vertex of the call, and $k$ the number of children of $v$.

| operation | time |
|---|---|
| parent$(x)$, is-root$(x)$ | $O(1)$ |
| add-child$(p)$ | $O(1)$ amortized, $O(1)$ with a preallocated array |
| path-to-root$(x)$, depth$(x)$, root-of$(x)$ | $\Theta(1 + h)$ |
| lowest common ancestor$(u, v)$, by walking up | $O(1 + h_u + h_v)$ |
| children$(v)$ from the array alone | $\Theta(n)$ |
| child-lists, all vertices | $\Theta(n)$, then $\Theta(1 + k)$ for children$(v)$ |
| all depths at once, in an order with parents first | $\Theta(n)$ |
| check (P1) and (P2) for a given array | $\Theta(n)$ |
| space | $n$ words, plus $2n + 1$ words for the child lists |

The depth of a vertex can be $n - 1$ in a path, so a walk up is $\Theta(n)$ in the worst case. All depths are computed in $\Theta(n)$ time by setting $\text{depth}[x] = \text{depth}[\text{parent}[x]] + 1$ in an order where each parent comes before its children, such as the order of BFS, or by memoising the walks. Checking (P2) for an array from outside also takes $\Theta(n)$: walk up from each vertex, mark the vertices on the current walk, stop at a vertex already finished, and report a cycle on reaching a vertex of the current walk. Each vertex is marked once.

## Variants

- **Self-loop at the root.** $\text{parent}[r] = r$ instead of NIL, as in CLRS for disjoint sets. The walk stops when $\text{parent}[x] = x$.
- **Forest.** Several roots, one tree each. The [disjoint-set forest](/disjoint-set-forest/) is a forest of this kind with [union by rank](/union-by-rank/) and [path compression](/path-compression/), which change the parents to keep the trees shallow.
- **Predecessor arrays.** BFS, DFS, Dijkstra and Bellman-Ford store $v.\pi$, the vertex before $v$ on the found path. The set of $\pi$ links is a parent-pointer tree rooted at the source, the [BFS tree](/bfs-tree/) or the shortest-path tree, and the path to $v$ is PATH-TO-ROOT$(v)$ reversed.
- **Parent and children.** Keep the parent array next to child lists or a [left-child right-sibling](/left-child-right-sibling/) form, to walk both ways. Each update must change both.
- **Ancestor tables.** [Binary lifting](/binary-lifting/) stores the $2^j$-th ancestor of each vertex for $j < \lg n$, so a jump of $d$ levels costs $O(\log d)$; it is a stack of parent arrays.
- **Packed arrays.** Store each entry in $\lceil \lg(n + 1) \rceil$ bits, one value kept for NIL. For labeled trees this is within a lower-order term of the $(n - 2)\lg n$ bits needed by [Cayley's formula](/cayley-formula/).

## When to use it

Use a parent array when the algorithm walks from vertices toward the root: finding paths found by a search, finding the representative of a set in union-find, computing depths, or finding ancestors. It is also the simplest input format for a rooted tree, and the natural output of any search. Use child lists, or the [left-child right-sibling](/left-child-right-sibling/) form, when the algorithm walks down, as in traversals and tree dynamic programming; build them from the parent array in $\Theta(n)$ time once rather than scanning the array for each vertex.

## Pitfalls

- **Children by scanning.** Calling `children`$(v)$ for each vertex by a scan costs $\Theta(n)$ per call and $\Theta(n^2)$ in total. Build the child lists once instead.
- **Cycles in outside input.** An array read from a file may not meet (P2). A walk up from a vertex on a cycle never ends. Check the array in $\Theta(n)$ time before walking, or bound each walk by $n$ steps.
- **Two ways to mark a root.** Code that tests $\text{parent}[x] = $ NIL loops forever on an array that marks roots by $\text{parent}[r] = r$, and code that tests $\text{parent}[x] = x$ reads index $-1$ on an array that uses NIL. Keep one convention.
- **Deep trees.** A recursive walk up, or a recursive depth computation, reaches a depth of $n - 1$ on a path and overflows the call stack. Use a loop.
- **Removing a vertex.** Deleting a vertex with children leaves them pointing at a missing index. Either remove only leaves, or move the children to a new parent first; compacting the indices changes the names of other vertices.

## Implementations

The Python module keeps the array with $-1$ for NIL, checks (P1) and (P2) when it is built from an outside array, and provides the walk up, depths, the naive lowest common ancestor, the child lists by counting sort, and the parent array of a BFS tree.

## History

Parent links are the oldest tree representation in programs. Knuth, in Section 2.3.3, describes trees stored with only a link to the parent of each node, notes that they are poor for most tree algorithms but right for some, and gives Algorithm E for equivalence classes, which uses them; Galler and Fischer introduced that method in 1964, and it became the [disjoint-set forest](/disjoint-set-forest/). CLRS present the predecessor attribute of breadth-first search as a breadth-first tree held in this form.

## References
