---
tag: CZ84MC
kind: data-structure
slug: brodal-queue
name: Brodal queue
aliases:
- Brodal's priority queue
- worst-case efficient priority queue
area: data-structures/heaps
level: research
summary: Priority queue with worst-case O(1) insert, find-min and decrease-key, and O(log n) extract-min.
implements: [priority-queue, meldable-priority-queue]
model: comparison-model
prereqs: [fibonacci-heap, binomial-heap, decrease-key, redundant-number-system, amortized-vs-worst-case]
see_also: [fibonacci-heap, strict-fibonacci-heap, hollow-heap, relaxed-heap, binomial-heap, skew-binary-random-access-list, comparison-sort-lower-bound, purely-functional-data-structure]
sources:
  - paper: "Gerth Stølting Brodal, Worst-case efficient priority queues, Proceedings of the 7th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA), 1996"
    locator: pages 52 to 58, the two trees, the rank and violation invariants, the guides, and the operations
  - paper: "Gerth Stølting Brodal and Chris Okasaki, Optimal purely functional priority queues, Journal of Functional Programming 6(6), 1996"
    locator: the skew binomial queue with a global minimum, which is the teaching version on this page
  - paper: "Gerth Stølting Brodal, George Lagogiannis and Robert E. Tarjan, Strict Fibonacci heaps, Proceedings of the 44th ACM Symposium on Theory of Computing (STOC), 2012"
    locator: the introduction, which compares the bounds and the machine models of the earlier worst-case heaps
---

A Brodal queue is a meldable [priority queue](/priority-queue/) of Brodal (1996) that does FIND-MIN, INSERT, MELD and [DECREASE-KEY](/decrease-key/) in $O(1)$ time and DELETE-MIN and DELETE in $O(\log n)$ time, all in the worst case. These are the amortized bounds of the [Fibonacci heap](/fibonacci-heap/), made to hold for every single operation, and they are optimal for a comparison-based queue: with $O(1)$ inserts, DELETE-MIN must cost $\Omega(\log n)$, else $n$ inserts and $n$ deletes would sort faster than the [comparison sort lower bound](/comparison-sort-lower-bound/) allows. The structure is heap-ordered trees with ranks, as in a [binomial heap](/binomial-heap/), but it allows a bounded number of nodes to break the heap order and records them, and it keeps all its counts in range with small steps per operation, in the style of a [redundant number system](/redundant-number-system/). It is complex, and it is mostly of theoretical interest. The code on this page is a simplified teaching version, the skew binomial queue with a pointer to the minimum, which has the worst-case bounds for FIND-MIN and INSERT but $O(\log n)$ for MELD and DECREASE-KEY.

## In plain words

A Fibonacci heap is fast on average over many steps, but one step can now and then take a long time. That is bad for a program that must answer each request within a fixed time.

A Brodal queue makes every step fast, not only the average. It keeps its keys in trees and allows a few keys to sit in the wrong place, below a larger key. It keeps a list of these wrong places and fixes a small number of them in each step, before they become too many. It also keeps its trees in balance with small repairs in each step, never with one big repair. The smallest key is always at the top, so you can read it at once, and to remove it you look at a small number of places where the next smallest can be.

## The abstract type

The Brodal queue implements the meldable, addressable min-[priority queue](/priority-queue/): INSERT$(e, k)$ returns a handle to the item $e$, and FIND-MIN, MELD, DECREASE-KEY$(e, k)$ for a key $k$ not larger than the current key, DELETE$(e)$ and DELETE-MIN work through handles. Keys come from a [total order](/total-order/) and are only compared.

## Representation

**The Brodal queue.** The items are in at most two trees, $T_1$ with the root $t_1$ and $T_2$ with the root $t_2$, and $t_1$ holds an item of minimum key. Each node $x$ has a rank $r(x)$. The children of a node have smaller ranks, and for each rank $i < r(x)$ a node has at least two children of rank $i$ and at most a constant number of them. So a node of rank $r$ has at least $2^r$ descendants, and all ranks are at most $\lg n$.

The heap order may fail: a node whose key is smaller than the key of its parent is a *violation*. Each violation is recorded in one of two sets, $V(y)$ and $W(y)$, of a node $y$ whose key is not larger, mostly $t_1$, and the number of violations of each rank is kept below a constant. So there are $O(\log n)$ violations, and the minimum after $t_1$ is among the children of $t_1$, the root $t_2$ and the recorded violations.

To keep the counts of children per rank and of violations per rank in range, each count changes by $O(1)$ per operation, and when a count reaches its bound, a constant number of links or cuts brings it back. The *guides* of the paper decide where to do these steps, so that a fix at one rank never starts a chain of fixes; this is the same idea as a redundant number system in which an increment changes only $O(1)$ digits.

**The teaching version.** The code keeps a list of heap-ordered trees, the *roots*, sorted by rank, where only the first two roots may have the same rank, and a pointer $\mathit{min}$ to a root of smallest key. Each node has a rank, its children have smaller ranks, and a node of rank $r$ has at least $2^r$ descendants. This is the skew binomial queue of Brodal and Okasaki, without their bootstrapping step for MELD. It has no violations: the heap order always holds.

## Operations

**The Brodal queue.** FIND-MIN returns the item of $t_1$. INSERT is MELD with a queue of one node. MELD compares the roots of the two queues, makes the smaller one the new $t_1$, and places the other trees below it or as $T_2$, with a constant number of links and repairs. DECREASE-KEY$(x, k)$ sets the key; if it is now smaller than the key of $t_1$, the items of $x$ and $t_1$ change places, so that $t_1$ stays the minimum. If $x$ is now smaller than its parent, it is added to a violation set of $t_1$, and a constant number of *violation reductions* follow: two violations of the same rank are removed by cutting and relinking a few nodes, which lowers their number. DELETE-MIN removes $t_1$, moves the subtrees of $T_2$ below the new root, finds the new minimum among the $O(\log n)$ children and violations, makes it the root, and adds its children and violation sets to the new root, with $O(\log n)$ steps of repair. DELETE$(x)$ decreases the key of $x$ to below every other key and then calls DELETE-MIN.

### The teaching version

```pseudo id=main
LINK(s, t)                                    ▷ two roots of the same rank r
L1  if key(t) < key(s) then swap s and t
L2  make t a child of s; r(s) ← r(s) + 1; return s

INSERT(e, k)
L3  x ← a new node for e with key k and rank 0
L4  if the first two roots have the same rank then
L5      u ← LINK of the two; if one of them was min then min ← u
L6      make x a child of u
L7      if key(x) < key(u) then swap the items of x and u
        replace the two roots by u; x ← u
L8  else put x in front of the roots
L9  if min = nil or key(x) < key(min) then min ← x

DELETE-MIN()
L10 if min = nil then error "underflow"; m ← min; REMOVE-ROOT(m); return the old item of m

REMOVE-ROOT(m)
L11 remove m from the roots
L12 T ← the other roots and the children of m; B ← an empty map from ranks to trees
L13 for each t in T: while B has a tree s of rank r(t): t ← LINK(t, s), removing s from B; B[r(t)] ← t
L14 roots ← the trees of B in order of rank; min ← a root of smallest key

DECREASE-KEY(e, k)
L15 x ← node(e); if key(x) < k then error "new key is larger"
L16 key(x) ← k; while x has a parent p and key(x) < key(p) do swap the items of x and p; x ← p
L17 if x is a root and key(x) < key(min) then min ← x

DELETE(e)
L18 x ← node(e); while x has a parent p do swap the items of x and p; x ← p
L19 REMOVE-ROOT(x)

MELD(Q′)
L20 join the roots of both queues as in line L13; min ← the smaller of the two minima
```

**Insert.** If the first two roots have the same rank $r$, line L5 links them into one tree of rank $r + 1$, and line L6 hangs the new node below it as a leaf. If the new key is smaller than the root's, line L7 exchanges the two items, which keeps the heap order, since the leaf has no children. So INSERT does at most one link and two comparisons, and the root list stays sorted with at most one pair of equal ranks at its front. This is the skew binary increment of a [skew binary random-access list](/skew-binary-random-access-list/), applied to heap-ordered trees.

**Delete-min and delete.** REMOVE-ROOT puts the children of the removed root among the roots and links roots of equal rank until all ranks differ, as in a binomial heap. DELETE first moves the item to the root of its tree by exchanges, as if its key were smaller than every key; each item that moves down one level was at most every key below its old place, so the heap order holds.

## Example

Insert $a$ with key 6, then $b$ 4, $c$ 9, $d$ 2, $e$ 7, $f$ 5 and $g$ 8 into the teaching version. A tree is written as key/rank[children], and the roots are listed in order.

| step | roots | what happens |
|---|---|---|
| insert 6, 4 | 4/r0, 6/r0 | each goes to the front |
| insert 9 | 4/r1[6/r0 9/r0] | the two roots of rank 0 are linked, and 9 is a leaf below |
| insert 2, 7 | 7/r0, 2/r0, 4/r1[...] | for 2 there is only one root, and for 7 the first two ranks 0 and 1 differ, so each goes to the front |
| insert 5 | 2/r1[7/r0 5/r0], 4/r1[6/r0 9/r0] | 7 and 2 are linked, and 5 is a leaf below 2 |
| insert 8 | 2/r2[7/r0 5/r0 4/r1[6/r0 9/r0] 8/r0] | the two rank-1 trees are linked, and 8 is a leaf |
| DECREASE-KEY($e$, 1) | 1/r2[2/r0 5/r0 4/r1[...] 8/r0] | 1 is smaller than its parent 2, so the items change places |
| DELETE-MIN | 8/r0, 2/r2[5/r0 4/r1[6/r0 9/r0]] | returns $e$; the children 2, 5 and 4 are linked by rank, and 8 stays alone |
| DELETE-MIN | 4/r2[6/r0 9/r0 5/r1[8/r0]] | returns $d$; 8 and 5 make a rank-1 tree, which is linked with 4 |
| DELETE($c$) | 4/r2[6/r0 5/r1[8/r0]] | 9 changes places with 4, the root is removed, and 6 and 4 are linked, then with 5 |

## Correctness

For the teaching version, the invariants are: (O) the heap order on each edge; (K) the children of a node have smaller ranks, and a node of rank $r$ has at least $2^r$ descendants; (L) the roots are sorted by rank and only the first two may have equal ranks; (M) $\mathit{min}$ is a root of smallest key; and (I) each item is in exactly one node, which its handle names. LINK and the leaf of line L6 keep (O) and (K); the exchanges of lines L7, L16 and L18 keep (O) by the argument of [sift-up](/sift-up/); and REMOVE-ROOT ends with distinct ranks. By (O), every key is at least the key of its root, so by (M) FIND-MIN is right. The full proof is in [the correctness proof](proofs/correctness.md).

For the Brodal queue itself, the paper proves that each operation keeps the rank and violation invariants with $O(1)$ or $O(\log n)$ steps, and that $t_1$ holds the minimum.

## Complexity

| operation | Brodal queue, worst case | teaching version, worst case |
|---|---|---|
| FIND-MIN | $O(1)$ | $O(1)$ |
| INSERT | $O(1)$ | $O(1)$ |
| MELD | $O(1)$ | $O(\log n)$ |
| DECREASE-KEY | $O(1)$ | $O(\log n)$ |
| DELETE-MIN, DELETE | $O(\log n)$ | $O(\log n)$ |
| space | $O(n)$ | $O(n)$ |

In the teaching version, (K) gives ranks of at most $\lg n$, and a node has a height of at most its rank, so the exchanges of DECREASE-KEY and DELETE take $O(\log n)$ steps. By (L) there are at most $\lg n + 2$ roots. A node of rank $r$ gains at most two children per rank increase, so it has at most $2r$ children, and REMOVE-ROOT links $O(\log n)$ trees. Brodal and Okasaki make MELD $O(1)$ by *bootstrapping*: a queue is stored as its minimum together with a queue of queues.

The constant factors of the full Brodal queue are large: each node carries the counts and violation sets, and each operation does many small repairs. For this reason, programs use simpler heaps, such as a [binary heap](/binary-heap/), a pairing heap or a [hollow heap](/hollow-heap/).

## Variants

- **Strict Fibonacci heaps.** Brodal, Lagogiannis and Tarjan (2012) gave a structure with the same worst-case bounds that is simpler and works on a pointer machine; see [strict Fibonacci heap](/strict-fibonacci-heap/).
- **Purely functional queues.** Brodal and Okasaki (1996) gave a purely functional queue with $O(1)$ worst-case FIND-MIN, INSERT and MELD and $O(\log n)$ DELETE-MIN, without DECREASE-KEY; see [purely functional data structure](/purely-functional-data-structure/).
- **Relaxed heaps.** The [relaxed heaps](/relaxed-heap/) of Driscoll, Gabow, Shrairman and Tarjan (1988) already allowed heap-order violations to get $O(1)$ DECREASE-KEY in the worst case, but they do not support a fast MELD.

## When to use it

Use the ideas of a Brodal queue when every single operation must be fast, as in a real-time system or a parallel algorithm in which one slow step delays all processors, and when MELD and DECREASE-KEY are both needed. In ordinary programs the amortized bounds of a Fibonacci, pairing or hollow heap are enough and the code is much simpler; when a worst-case bound is needed with less code, a strict Fibonacci heap is the usual choice.

## Pitfalls

- **Amortized versus worst case.** The Brodal queue has the same asymptotic total time as a Fibonacci heap on every sequence; its gain is only that no single operation is slow. Choose it for that reason, not for speed. See [amortized versus worst-case analysis](/amortized-vs-worst-case/).
- **Partial implementations.** A code that is called a Brodal queue may implement only part of the structure, as the code on this page does. Check which operations are really $O(1)$ in the worst case.
- **The minimum after an exchange.** In the teaching version, a link in INSERT can move the old minimum root below a new root; the pointer $\mathit{min}$ must then move to the new root, as line L5 does.
- **Handles and exchanges.** Exchanging items between nodes moves the items. A handle must name the item, and each item must point to its current node.

## Implementations

The Python class `BrodalQueue` is the teaching version. It keeps `roots` as a list sorted by rank, `min` as a node, and `Node` objects with `item`, `key`, `rank`, `children` and `parent`; an `Item` handle points to its node. `insert`, `find_min`, `delete_min`, `decrease_key`, `delete` and `meld` follow the pseudocode, and `check_invariant` checks (O), (K), (L), (M) and the handles. Keys need only the operation "<". The code does not implement the two-tree structure, the violation sets or the guides of the full Brodal queue.

## History

Brodal presented the structure at SODA 1996, as the first priority queue with the amortized bounds of Fredman and Tarjan's Fibonacci heap (FOCS 1984, journal version 1987) in the worst case and with MELD. It built on the relaxed heaps of Driscoll, Gabow, Shrairman and Tarjan (1988), which had worst-case decrease-key without meld. In the same year, Brodal and Okasaki gave the purely functional skew binomial queue. In 2012 Brodal, Lagogiannis and Tarjan gave the strict Fibonacci heap, with the same bounds and a simpler pointer-based structure.

## References
