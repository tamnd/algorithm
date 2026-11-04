---
tag: 1EX9SR
kind: data-structure
slug: fibonacci-heap
name: Fibonacci heap
aliases:
- Fibonacci queue
area: data-structures/heaps
level: advanced
summary: Heap with O(1) amortized insert, merge and decrease-key, giving O(m + n log n) Dijkstra.
implements: [priority-queue, meldable-priority-queue]
model: comparison-model
prereqs: [heap, heap-property, binomial-heap, potential-method, circular-linked-list, fibonacci-numbers]
see_also: [binary-heap, pairing-heap, hollow-heap, strict-fibonacci-heap, rank-pairing-heap, brodal-queue, dijkstra, prim]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 19 (Fibonacci Heaps), Sections 19.1 to 19.4
  - paper: doi:10.1145/28869.28874
    title: Michael L. Fredman and Robert E. Tarjan, Fibonacci heaps and their uses in improved network optimization algorithms, Journal of the ACM 34(3), 1987
    locator: Sections 2 and 3 (the data structure and its amortized analysis) and Section 4 (network algorithms)
  - book: isbn:9783540779773
    title: Kurt Mehlhorn and Peter Sanders, Algorithms and Data Structures, The Basic Toolbox
    locator: Section 6.2 (Addressable priority queues), Fibonacci heaps
---

A Fibonacci heap is a [heap](/heap/) made of a collection of heap-ordered trees, with a pointer to the root of minimum key. It does as little work as it can at each operation and pays the cost later: insert, find-min, union and [decrease-key](/decrease-key/) take $O(1)$ amortized time, and extract-min and delete take $O(\log n)$ amortized time. Fredman and Tarjan introduced it in 1984 and published it in 1987. With it, [Dijkstra's algorithm](/dijkstra/) and [Prim's algorithm](/prim/) run in $O(m + n \log n)$ time on a graph with $n$ vertices and $m$ edges, because these algorithms do up to $m$ decrease-keys and only $n$ extract-mins. The name comes from the [Fibonacci numbers](/fibonacci-numbers/) in the proof that the trees stay bushy.

## In plain words

Picture a set of family trees where each parent is smaller than each child. You keep a finger on the smallest top person. A new person starts a new tree, at no cost. Two heaps join by laying their trees side by side.

Only when you take out the smallest person do you tidy up. Their children become tops of trees. Then you join trees of the same size, two at a time, until no two trees have the same number of children.

To make a key smaller, you cut its tree part loose and make it a new tree. A parent that loses a second child is cut loose too. This rule keeps each tree large compared with its number of children, so the number of trees after the tidy-up stays small.

## The abstract type

A Fibonacci heap implements the [meldable priority queue](/meldable-priority-queue/), a [priority queue](/priority-queue/) with union. It stores a multiset of items with keys from a [total order](/total-order/) and has these operations. INSERT$(H, x)$ adds the node $x$, whose key is set. FIND-MIN$(H)$ returns a node of minimum key. EXTRACT-MIN$(H)$ removes and returns it. UNION$(H_1, H_2)$ moves all items of $H_2$ into $H_1$. DECREASE-KEY$(H, x, k)$ sets the key of $x$ to $k \le x.key$. DELETE$(H, x)$ removes $x$. For the last two, the caller holds the node $x$ as a handle, which INSERT gave it.

## Representation

The heap $H$ has a pointer $H.min$ and a count $H.n$. Each node $x$ has a key $x.key$, a parent pointer $x.p$, a pointer $x.child$ to any one of its children, pointers $x.left$ and $x.right$ to its siblings, its number of children $x.degree$, and a bit $x.mark$.

- The children of each node are in a [circular](/circular-linked-list/) [doubly linked list](/doubly-linked-list/), so a node can be removed from its list, and two lists can be joined, in $O(1)$ time.
- The roots of the trees are in one more circular list, the *root list*, and $H.min$ points to a root of minimum key. An empty heap has $H.min = \text{nil}$.

The invariants are:

1. **(order)** each tree has the min-[heap property](/heap-property/): $x.p.key \le x.key$ for each non-root $x$;
2. **(min)** $H.min$ is a root, and no key in the heap is smaller than $H.min.key$;
3. **(marks)** a non-root node that is not marked has lost no child since it last became the child of another node, and a marked non-root node has lost exactly one; a root may keep an old mark, which has no effect;
4. **(degree)** a node of degree $k$ has at least $F_{k+2}$ nodes in its subtree, where $F_0 = 0$, $F_1 = 1$ and $F_{j} = F_{j-1} + F_{j-2}$.

Invariant 4 follows from the others and the rule of the cascading cut, see the complexity section. It gives the bound $D(n) \le \lfloor \log_\varphi n \rfloor$ on the degree of each node in a heap of $n$ nodes, where $\varphi = (1 + \sqrt 5)/2$.

## Operations

```pseudo id=main
INSERT(H, x)                               ▷ x is a new node, x.key is set
L1  x.degree ← 0, x.p ← nil, x.child ← nil, x.mark ← false
L2  add x to the root list of H
L3  if H.min = nil or x.key < H.min.key then H.min ← x
L4  H.n ← H.n + 1

UNION(H1, H2)                              ▷ moves the items of H2 into H1
L5  join the root list of H2 to the root list of H1
L6  if H1.min = nil or (H2.min ≠ nil and H2.min.key < H1.min.key) then H1.min ← H2.min
L7  H1.n ← H1.n + H2.n
L8  H2.min ← nil, H2.n ← 0

EXTRACT-MIN(H)
L9  z ← H.min
L10 if z = nil then error "heap underflow"
L11 for each child x of z do add x to the root list of H, x.p ← nil
L12 remove z from the root list of H
L13 if H.n = 1 then H.min ← nil
L14 else H.min ← any root of H, CONSOLIDATE(H)
L15 H.n ← H.n − 1
L16 return z

CONSOLIDATE(H)
L17 T ← an empty table from degrees to roots
L18 for each root w in the root list of H do
L19     x ← w, d ← x.degree
L20     while T[d] ≠ nil do
L21         y ← T[d]                       ▷ another root of degree d
L22         if y.key < x.key then exchange x and y
L23         LINK(H, y, x)
L24         T[d] ← nil, d ← d + 1
L25     T[d] ← x
L26 H.min ← nil, make the root list of H empty
L27 for each d with T[d] ≠ nil, in increasing order of d, do
L28     x ← T[d]
L29     add x to the root list of H
L30     if H.min = nil or x.key < H.min.key then H.min ← x

LINK(H, y, x)                              ▷ x and y are roots of equal degree, x.key ≤ y.key
L31 remove y from the root list of H
L32 make y a child of x, x.degree ← x.degree + 1
L33 y.mark ← false

DECREASE-KEY(H, x, k)
L34 if k > x.key then error "new key is larger than the current key"
L35 x.key ← k, y ← x.p
L36 if y ≠ nil and x.key < y.key then
L37     CUT(H, x, y)
L38     CASCADING-CUT(H, y)
L39 if x.key < H.min.key then H.min ← x

CUT(H, x, y)                               ▷ x is a child of y
L40 remove x from the child list of y, y.degree ← y.degree − 1
L41 add x to the root list of H, x.p ← nil, x.mark ← false

CASCADING-CUT(H, y)
L42 z ← y.p
L43 if z = nil then return
L44 if y.mark = false then y.mark ← true, return
L45 CUT(H, y, z), CASCADING-CUT(H, z)

DELETE(H, x)
L46 DECREASE-KEY(H, x, −∞)
L47 EXTRACT-MIN(H)
```

**Insert** (lines L1 to L4) makes $x$ a tree of one node and puts it in the root list. No tree is linked, so the cost is $O(1)$.

**Union** (lines L5 to L8) joins two circular lists, which takes four pointer changes, and keeps the smaller of the two minima. The cost is $O(1)$.

**Extract-min** (lines L9 to L16) is the only operation that cleans up. It moves the children of the minimum $z$ into the root list, removes $z$, and calls CONSOLIDATE. That procedure goes over the roots and keeps, in the table $T$, at most one root of each degree. When a root of degree $d$ meets another root of degree $d$, LINK makes the one with the larger key a child of the other, and the result has degree $d + 1$, which may meet a root of degree $d + 1$ in turn (lines L20 to L24). At the end, each root has a different degree, and lines L26 to L30 rebuild the root list and find the new minimum.

**Decrease-key** (lines L34 to L39) lowers the key. If the heap order breaks between $x$ and its parent $y$, it cuts $x$ off and makes it a root (CUT). Then the *cascading cut* goes up from $y$: an unmarked $y$ gets marked, which records that it lost one child; a marked $y$ loses its second child now, so it is cut too, and the cut goes on at its parent. The cascade stops at the latest at a root, whose mark is never read.

**Delete** (lines L46 and L47) makes $x$ the minimum and extracts it.

## Example

Insert the keys 7, 18, 38, 24, 17, 23, 21, 39 and 41, in this order, into an empty heap. In the table, $a(b\ c)$ is a tree with the root $a$ and the children $b$ and $c$, a star marks a marked node, and the bar separates the trees.

| step | what happens | trees |
|---|---|---|
| 9 inserts | nine trees of one node, $H.min$ at 7 | 7 \| 18 \| 38 \| 24 \| 17 \| 23 \| 21 \| 39 \| 41 |
| EXTRACT-MIN | returns 7; CONSOLIDATE links 38 under 18, 24 under 17, then 18 under 17, then 23 under 21, 41 under 39, 39 under 21, and 21 under 17 | 17(24 18(38) 21(23 39(41))) |
| DECREASE-KEY 41 to 15 | 15 < 39, cut 15; 39 has a parent and no mark, so mark 39 | 15 \| 17(24 18(38) 21(23 39\*)) |
| DECREASE-KEY 39 to 16 | 16 < 21, cut 16; mark 21 | 15 \| 16 \| 17(24 18(38) 21\*(23)) |
| DECREASE-KEY 23 to 5 | 5 < 21, cut 5; 21 is marked, so cut 21 too; its parent 17 is a root, stop; $H.min$ at 5 | 5 \| 21 \| 15 \| 17(24 18(38)) \| 16 |
| EXTRACT-MIN | returns 5; CONSOLIDATE meets the roots 21, 15, 17 and 16, and links 21 under 15 | 16 \| 15(21) \| 17(24 18(38)) |
| DELETE 38 | cut 38 from 18 and mark 18; 38 becomes the minimum and EXTRACT-MIN removes it; all roots have different degrees, so nothing links | 16 \| 15(21) \| 17(24 18\*) |

After the first extract-min, one tree of degree 3 holds all 8 nodes. Invariant 4 asks for at least $F_5 = 5$ nodes. The three decrease-keys cost one cut, one cut, and two cuts.

## Correctness

The invariants (order) and (min) give the result of FIND-MIN. Each operation keeps them. INSERT and UNION add whole trees and keep the smaller minimum. LINK puts the root with the larger key under the root with the smaller key, so each new edge is heap-ordered. CUT removes an edge, and a tree part with a root keeps its order. DECREASE-KEY lowers one key: the edges from $x$ to its children stay ordered, and the only edge that may break, the one from $y$ to $x$, is cut. CONSOLIDATE moves each node to one root of $T$ at a time and keeps all nodes, and lines L26 to L30 scan all final roots, so $H.min$ is a minimum. The marks and the degrees are kept by the same case analysis. [The correctness proof](proofs/correctness.md) gives the full argument.

## Complexity

The analysis uses the [potential method](/potential-method/) with

$$\Phi(H) = t(H) + 2\,m(H),$$

where $t(H)$ is the number of trees and $m(H)$ is the number of marked nodes. The actual cost is counted in units of $O(1)$ work. Let $D(n)$ be the largest degree of a node in a heap of $n$ nodes.

- **Insert.** Actual cost 1, and $\Phi$ grows by 1. Amortized cost $O(1)$.
- **Union.** Actual cost 1, and $\Phi(H_1) + \Phi(H_2)$ does not change. Amortized cost $O(1)$.
- **Extract-min.** At most $D(n)$ children become roots, so CONSOLIDATE starts with at most $t + D(n) - 1$ roots. Each LINK lowers the number of roots by 1, so the work of CONSOLIDATE is $O(t + D(n))$. At the end there are at most $D(n) + 1$ roots, with different degrees. The marks do not grow. The amortized cost is $O(t + D(n)) + (D(n) + 1) - t = O(D(n))$, after the unit of potential is scaled to cover a unit of work.
- **Decrease-key.** Let $c$ be the number of cuts. The actual cost is $O(c)$. The cuts make $c$ new trees. Each cut in the cascade except the last one clears a mark, and the last step sets at most one mark. So $\Phi$ changes by at most $c + 2(2 - c) = 4 - c$, and the amortized cost is $O(c) + 4 - c = O(1)$. A marked node pays with its 2 units: one for its cut, and one for the new tree it becomes.
- **Delete.** One decrease-key and one extract-min, $O(D(n))$ amortized.

**The degree bound.** Let $x$ be a node, and let $y_1, \ldots, y_k$ be its children in the order in which they were linked to $x$. When $y_i$ was linked, $x$ had at least the $i - 1$ children $y_1, \ldots, y_{i-1}$, and LINK joins only roots of equal degree, so $y_i$ had degree at least $i - 1$. Since then $y_i$ has lost at most one child, because a second loss cuts it. So $y_i$ has degree at least $i - 2$. Let $s_k$ be the least size of a subtree whose root has degree $k$. Then $s_0 = 1$, $s_1 = 2$ and

$$s_k \ge 2 + \sum_{i=2}^{k} s_{i-2},$$

which gives $s_k \ge F_{k+2} \ge \varphi^k$ by induction. So a node of degree $k$ in a heap of $n$ nodes has $n \ge \varphi^k$, and $D(n) \le \lfloor \log_\varphi n \rfloor \approx 1.44 \lg n$. [The complexity proof](proofs/complexity.md) gives the details.

| operation | amortized time | worst-case time of one call |
|---|---|---|
| insert | $O(1)$ | $O(1)$ |
| find-min | $O(1)$ | $O(1)$ |
| union | $O(1)$ | $O(1)$ |
| extract-min | $O(\log n)$ | $O(n)$ |
| decrease-key | $O(1)$ | $O(h)$, for a tree of height $h$ |
| delete | $O(\log n)$ | $O(n)$ |
| space | $O(n)$ | four pointers, a degree and a bit per node |

One extract-min right after $n$ inserts costs $\Theta(n)$, because CONSOLIDATE links $n - 1$ roots. One decrease-key costs one step for each level of its cascade, so its worst case is the height of the tree, and after many cuts a tree can be a path of $\Theta(n)$ nodes. The amortized bounds hold for each sequence of operations that starts with an empty heap.

**Dijkstra and Prim.** On a graph with $n$ vertices and $m$ edges, these algorithms do $n$ inserts, $n$ extract-mins and at most $m$ decrease-keys. With a Fibonacci heap the total is $O(m + n \log n)$, against $O((n + m) \log n)$ with a [binary heap](/binary-heap/). By the comparison lower bound on the [heap](/heap/) page, no comparison-based heap can make the $n \log n$ term smaller.

## Variants

- **[Strict Fibonacci heap](/strict-fibonacci-heap/).** Brodal, Lagogiannis and Tarjan (2012) gave a pointer-based heap with the same bounds in the worst case.
- **[Brodal queue](/brodal-queue/).** The first heap with these bounds in the worst case (1996), more complex.
- **[Hollow heap](/hollow-heap/).** The same amortized bounds with simpler code: decrease-key moves the item to a new node and leaves the old node hollow, with no cascading cuts.
- **[Rank-pairing heap](/rank-pairing-heap/), [thin heap](/thin-heap/) and [violation heap](/violation-heap/).** Other structures with the same amortized bounds and one tree shape rule in place of the marks.
- **[Pairing heap](/pairing-heap/).** A simpler self-adjusting heap that is often faster in practice; its decrease-key is not $O(1)$ amortized in the worst case.

## When to use it

Use a Fibonacci heap when the number of decrease-keys is much larger than the number of extract-mins, as in [Dijkstra's algorithm](/dijkstra/) and [Prim's algorithm](/prim/) on dense graphs, and when you need the theoretical bound. In practice, its pointer structure and large constant factors make it slower than a [binary heap](/binary-heap/) or a [pairing heap](/pairing-heap/) at most sizes, so many libraries choose those. It is also the structure that most proofs of an $O(m + n \log n)$ time bound refer to.

## Pitfalls

- **No search.** DECREASE-KEY and DELETE need the node of the item. The heap cannot find a key; the caller must keep the node that INSERT returned, or a map from items to nodes.
- **Forgetting the cascade.** Without CASCADING-CUT, a node can lose many children, its subtree can become small, and the degree bound $D(n) = O(\log n)$ fails. Extract-min then becomes slow.
- **Changing the root list while scanning it.** CONSOLIDATE removes roots from the root list while it goes over that list. Save the list of roots before the loop of line L18, as the Python code does.
- **A table that is too small.** The table $T$ needs the indices $0 \ldots D(n)$. A fixed size of $\lfloor \lg n \rfloor + 1$ is too small; use $\lfloor \log_\varphi n \rfloor + 1$ or a map.
- **Recursion depth.** CASCADING-CUT is tail-recursive, and the cascade can be long. Write it as a loop.
- **A node that is no longer in the heap.** Calling DECREASE-KEY on a node that was extracted corrupts the heap. The Python code keeps a flag and raises an error.

## Implementations

The Python class `FibonacciHeap` follows the main block. `insert` returns a `Node`, which is the handle for `decrease_key` and `delete`. `union` empties the other heap. The table of CONSOLIDATE is a dictionary, and its roots go back into the root list in increasing order of degree. CASCADING-CUT is a loop. DELETE does the cut and the cascade of a decrease to $-\infty$ directly, sets the minimum to $x$, and extracts it, so the keys need only the operation "<".

## History

Michael Fredman and Robert Tarjan presented the Fibonacci heap at the IEEE Symposium on Foundations of Computer Science in 1984 and published the full paper in the Journal of the ACM in 1987. They built it from the binomial queue of Vuillemin (1978) by making the links lazy and by adding the cuts and the marks. Their paper also used it to speed up shortest paths, minimum spanning trees and other network algorithms. The third edition of CLRS gives it a full chapter, Chapter 19; the fourth edition removed that chapter.

## References
