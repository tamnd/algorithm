---
tag: G7BE09
kind: data-structure
slug: pairing-heap
name: Pairing heap
aliases:
- pairing heaps
area: data-structures/heaps
level: advanced
summary: Simple self-adjusting heap whose practical performance rivals Fibonacci heaps.
implements: [priority-queue, meldable-priority-queue]
model: comparison-model
complexity:
  vars: {n: the number of items in the heap}
  time: {worst: O(n), amortized: O(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [priority-queue, heap-property, rooted-tree, potential-method]
see_also: [fibonacci-heap, skew-heap, leftist-heap, binomial-heap, splay-tree, meldable-priority-queue, rank-pairing-heap, decrease-key]
sources:
  - paper: doi:10.1007/BF01840439
    title: Michael L. Fredman, Robert Sedgewick, Daniel D. Sleator and Robert E. Tarjan, The pairing heap, a new form of self-adjusting heap, Algorithmica 1(1), 1986
    locator: pages 111 to 129 (the two-pass pairing heap, its variants, and the O(log n) amortized analysis)
  - paper: Michael L. Fredman, On the efficiency of pairing heaps and related data structures, Journal of the ACM 46(4), 1999
    locator: the lower bound of Ω(log log n) amortized for decrease-key
  - paper: Seth Pettie, Towards a final analysis of pairing heaps, Proceedings of the 46th IEEE Symposium on Foundations of Computer Science (FOCS), 2005
    locator: the bound O(2^(2 sqrt(lg lg n))) amortized for insert, meld and decrease-key
  - paper: John T. Stasko and Jeffrey Scott Vitter, Pairing heaps, experiments and analysis, Communications of the ACM 30(3), 1987
    locator: the experiments that compare pairing heaps with other heaps, and the auxiliary two-pass variant
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3 (Sorting by selection), the part on priority queues and mergeable heaps
---

A pairing heap is a [meldable priority queue](/meldable-priority-queue/) stored as one heap-ordered tree in which each node may have any number of children. Insert, meld and [decrease-key](/decrease-key/) each do one *link* of two trees, and delete-min removes the root and joins its children by *two-pass pairing*: link them in pairs from left to right, then link the results from right to left. There are no ranks, no marks and no balance rules, which makes it short to code and fast in practice. Fredman, Sedgewick, Sleator and Tarjan introduced it in 1986 as a simple rival of the [Fibonacci heap](/fibonacci-heap/) and proved $O(\log n)$ amortized time per operation; the exact amortized cost of decrease-key is still open.

## In plain words

Think of a family tree of a sports club, where each coach is better ranked than the players they coach. To add a player, compare the new player with the head coach. The better of the two becomes the head, and the other becomes one more direct report of the head. To join two clubs, do the same with the two heads.

When the head coach leaves, the direct reports must pick a new head. They pair up, left to right, and the better of each pair becomes the boss of the other. Then the pair winners join from right to left, one at a time, into one tree. The best of all ends at the top. The tree is never balanced on purpose, but this pairing keeps it shallow enough on average over many operations.

## The abstract type

A pairing heap implements the [priority queue](/priority-queue/) on a multiset of keys from a total order, with the operations of a [meldable priority queue](/meldable-priority-queue/): `insert(H, k)` returns a handle to the new item, `find-min(H)`, `delete-min(H)`, `meld(H1, H2)`, `decrease-key(H, x, k)` and `delete(H, x)` for a handle $x$. This page uses a min-heap.

## Representation

Each node $x$ holds a key and three pointers: $x.child$ to its first child, $x.sibling$ to the next child of its parent, and $x.prev$ to its parent if $x$ is a first child, or to its left sibling otherwise. So the children of a node form a doubly linked list, and the tree is stored as a binary tree in the *child-sibling* form. The heap holds a pointer $H.root$ and a count $n$. The pointer $prev$ is needed only for decrease-key and delete.

**Invariant.**

- **(P1) One tree.** The nodes form one rooted tree with root $H.root$, which has no siblings, or the heap is empty.
- **(P2) Heap order.** The key of each node is at least the key of its parent.
- **(P3) Links.** The pointers $child$, $sibling$ and $prev$ match the tree as described, and $n$ is the number of nodes.

By (P2), the root holds a smallest key. Nothing else is required: a node may have any number of children, and the tree may have any shape.

## Operations

```pseudo id=main
MELD(H1, H2)
L1  return LINK(H1.root, H2.root)

LINK(a, b)                              ▷ two roots without siblings; either may be NIL
L2  if b.key < a.key then swap a and b  ▷ a is the smaller root
L3  make b the first child of a
L4  return a

INSERT(H, k)
L5  x ← a new node with key k; H.root ← LINK(H.root, x); return x

DELETE-MIN(H)                           ▷ H is not empty
L6  r ← H.root; H.root ← MERGE-PAIRS(the children of r)
L7  return r.key

MERGE-PAIRS(x1, x2, ..., xk)            ▷ the list of children, left to right
L8  for i ← 1, 3, 5, ... while i ≤ k do                ▷ first pass
L9      y ← LINK(x_i, x_{i+1}), or x_k alone if i = k; add y to the list Y
L10 r ← NIL; for each y in Y from right to left do     ▷ second pass
L11     r ← LINK(y, r)
L12 return r
```

**Link** (lines L2 to L4) compares two roots and makes the larger one the first child of the smaller one. It takes $O(1)$ time. If one tree is empty, it returns the other.

**Insert and meld** (lines L1 and L5) do one link, so they take $O(1)$ time in the worst case.

**Find-min** returns $H.root.key$ in $O(1)$ time.

**Delete-min** (lines L6 to L12) removes the root and joins its $k$ children with $k - 1$ links. The first pass links $x_1$ with $x_2$, $x_3$ with $x_4$, and so on. The second pass starts with the last tree of the first pass and links each earlier tree into it. The actual time is $\Theta(k + 1)$, which is $\Theta(n)$ in the worst case: after $n$ inserts in increasing order, the root has $n - 1$ children.

```pseudo id=decrease-key
DECREASE-KEY(H, x, k)                   ▷ k ≤ x.key
L13 x.key ← k
L14 if x ≠ H.root then cut the subtree of x from its parent; H.root ← LINK(H.root, x)

DELETE(H, x)
L15 if x = H.root then return DELETE-MIN(H)
L16 cut the subtree of x; H.root ← LINK(H.root, MERGE-PAIRS(the children of x))
```

**Decrease-key** lowers the key and, unless $x$ is the root, cuts the subtree of $x$ out of the child list of its parent by the $prev$ pointer, then links it with the root. The subtree of $x$ is still heap-ordered, because its keys did not change except that of $x$, which went down. The actual time is $O(1)$.

**Delete** cuts out the subtree of $x$, pairs the children of $x$ with MERGE-PAIRS, and links the result with the root. It costs as much as a delete-min.

## Example

Insert 7, 3, 9, 5, 8, 2, 6, 4 into an empty heap. A tree is written as key[children, left to right].

| operation | links | tree after |
|---|---|---|
| insert 7 | | 7 |
| insert 3 | 3 wins | 3[7] |
| insert 9 | 3 wins | 3[9, 7] |
| insert 5 | 3 wins | 3[5, 9, 7] |
| insert 8 | 3 wins | 3[8, 5, 9, 7] |
| insert 2 | 2 wins | 2[3[8, 5, 9, 7]] |
| insert 6 | 2 wins | 2[6, 3[8, 5, 9, 7]] |
| insert 4 | 2 wins | 2[4, 6, 3[8, 5, 9, 7]] |

Now call delete-min twice.

| operation | first pass | second pass | tree after |
|---|---|---|---|
| delete-min returns 2 | children 4, 6, 3: link (4, 6) gives 4[6]; 3 alone | link 4[6] into 3 | 3[4[6], 8, 5, 9, 7] |
| delete-min returns 3 | children 4[6], 8, 5, 9, 7: (4, 8) gives 4[8, 6]; (5, 9) gives 5[9]; 7 alone | 5[9] with 7 gives 5[7, 9]; 4[8, 6] with 5[7, 9] gives 4[5[7, 9], 8, 6] | 4[5[7, 9], 8, 6] |

The second delete-min does 4 links for 5 children. Its root first had five children; after it, the new root has three. The first pass halves the number of trees, and the potential argument below shows that this pays for the links.

## Correctness

Each operation keeps (P1) to (P3), and the multiset of keys changes as the priority queue requires. A link of two heap-ordered trees makes the larger root a child of the smaller root, so the new edge is in heap order and all old edges are unchanged. Insert, meld and both passes of MERGE-PAIRS are sequences of links, so they keep heap order and produce one tree from the trees they get. Delete-min removes the root, which holds a smallest key by (P2), and MERGE-PAIRS joins all its subtrees, so no node is lost. Decrease-key keeps heap order inside the cut subtree, because only the key of its root changed and it went down. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | worst case | amortized |
|---|---|---|
| find-min | $O(1)$ | $O(1)$ |
| insert | $O(1)$ | $O(\log n)$ in the analysis below; $O(1)$ by Iacono |
| meld | $O(1)$ | $O(\log n)$ |
| delete-min | $O(n)$ | $O(\log n)$ |
| decrease-key | $O(1)$ | $O(\log n)$; at most $O(2^{2\sqrt{\lg \lg n}})$ by Pettie; at least $\Omega(\log \log n)$ by Fredman |
| delete | $O(n)$ | $O(\log n)$ |
| space | $\Theta(n)$: one key and three pointers per node | |

**The $O(\log n)$ amortized bound.** Fredman, Sedgewick, Sleator and Tarjan use the [potential method](/potential-method/) on the child-sibling binary tree. Let $s(x)$ be the number of nodes in the binary subtree of $x$: $x$, its children and all their descendants, and all its right siblings and their descendants. The potential is $\Phi = \sum_x \lg s(x)$. A link changes $\Phi$ by at most $2 \lg n$. In the first pass of a delete-min, the link of a pair at the chain size $s_i$, followed by the chain size $s_{i+1}$, raises $\Phi$ by at most $2 \lg S_i - 2 \lg S_{i+2} - 2$, where $S_i$ is the binary subtree size of the $i$-th child, so the sum telescopes to at most $2 \lg n - 2 \lfloor k/2 \rfloor + 2$. The second pass raises $\Phi$ by at most $\lg n$, and removing the root lowers it by $\lg n$. So a delete-min with $k$ children costs at most $k + 1$ actual steps and at most $2 \lg n + 4$ amortized. The full proof is in [the complexity proof](proofs/complexity.md).

**Better bounds.** The bound for decrease-key is the open question of the structure. Fredman proved in 1999 that pairing heaps and a class of similar heaps need $\Omega(\log \log n)$ amortized time per decrease-key when the other operations take $O(\log n)$, so pairing heaps cannot match the $O(1)$ of Fibonacci heaps. Pettie proved in 2005 an upper bound of $O(2^{2\sqrt{\lg \lg n}})$ amortized for insert, meld and decrease-key, which is $o(\log n)$, with $O(\log n)$ for delete-min. Iacono showed that insert takes $O(1)$ amortized time when meld is not used.

## Variants

- **Forward pairing.** Do the second pass from left to right instead. FSST define this variant and others beside the two-pass form, and they prove weaker bounds for them. The two-pass form with a right-to-left second pass has the best known bounds.
- **Multipass.** Repeat the pairing pass until one tree is left. It is simpler to state but is slower in experiments.
- **Auxiliary list.** Stasko and Vitter keep new trees in a list beside the root and pair them only at the next delete-min. Their experiments found this variant fast in practice.
- **Rank-pairing heap.** The [rank-pairing heap](/rank-pairing-heap/) adds ranks to the pairing idea and gets the Fibonacci bounds, with $O(1)$ amortized decrease-key.
- **Skew and leftist heaps.** The [skew heap](/skew-heap/) and the [leftist heap](/leftist-heap/) are binary-tree meldable heaps with $O(\log n)$ meld but without $O(1)$ insert.

## When to use it

Use a pairing heap when you need a priority queue with meld or decrease-key and want a short program that is fast in practice. Experiments, starting with Stasko and Vitter, have often found it faster than Fibonacci heaps and binomial heaps for [Dijkstra's algorithm](/dijkstra/) and [Prim's algorithm](/prim/). When only insert and delete-min are needed, a [binary heap](/binary-heap/) in an array is smaller and has better cache use. When a proven $O(1)$ amortized decrease-key matters, for example for the $O(m + n \log n)$ bound of Dijkstra's algorithm, use a [Fibonacci heap](/fibonacci-heap/) or a rank-pairing heap.

## Pitfalls

- **One left-to-right pass only.** Linking the children one after another from left to right, without pairing, gives a long chain, and a sequence of delete-mins can cost $\Theta(n)$ each. The two passes of lines L8 to L11 are needed.
- **Recursion in MERGE-PAIRS.** The root can have $n - 1$ children, for example after inserts in increasing order. A recursive MERGE-PAIRS then needs a stack of depth $n$. Use the loop of lines L8 to L11, with a list or by reversing the sibling pointers.
- **Forgetting the prev pointers.** A cut in decrease-key must update the pointer of the left sibling or of the parent, and the $prev$ of the right sibling. A missing update breaks a later cut without an error.
- **Decrease-key on the root.** If $x$ is the root, line L14 must not cut it. A cut of the root with its own parent pointer NIL corrupts the heap.
- **A stale handle.** After delete or delete-min, the handle of the removed item must not be used again.

## Implementations

The Python version uses a list for the results of the first pass and a loop for both passes, so it uses no recursion. Its `check_invariant` method checks heap order, the $prev$ pointers and the count.

## History

Michael Fredman, Robert Sedgewick, Daniel Sleator and Robert Tarjan presented the pairing heap in 1986, after Fredman and Tarjan's Fibonacci heap of 1984 and Sleator and Tarjan's [splay tree](/splay-tree/). Its analysis uses the same potential function as the splay tree, and they proved the $O(\log n)$ amortized bound and conjectured that pairing heaps match the Fibonacci bounds. Stasko and Vitter published experiments in 1987. Fredman disproved the conjecture for decrease-key in 1999, and Pettie gave the best known upper bound in 2005.

## References
