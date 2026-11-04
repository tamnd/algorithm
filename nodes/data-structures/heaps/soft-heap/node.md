---
tag: C1G5PQ
kind: data-structure
slug: soft-heap
name: Soft heap
aliases:
- Chazelle soft heap
area: data-structures/heaps
level: research
summary: Approximate meldable heap that corrupts a fixed fraction of keys to reach O(1) amortized operations.
implements: [meldable-priority-queue]
model: comparison-model
complexity:
  vars: {n: the number of insertions, ε: the error rate}
  time: {amortized: O(log(1/ε))}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [binomial-heap, meldable-priority-queue, priority-queue]
see_also: [chazelle-mst, minimum-spanning-tree, selection-problem, median-of-medians, binomial-heap, fibonacci-heap, comparison-model, heapsort]
sources:
  - paper: doi:10.1145/355541.355554
    title: "Bernard Chazelle, The soft heap: an approximate priority queue with optimal error rate, Journal of the ACM 47(6), 2000, pp. 1012 to 1027"
    locator: the whole paper (definition, the binomial-tree implementation with car-pooling, the error bound, the lower bound and the applications)
  - paper: doi:10.1137/120880185
    title: Haim Kaplan, Robert E. Tarjan and Uri Zwick, Soft heaps simplified, SIAM Journal on Computing 42(4), 2013, pp. 1660 to 1673
    locator: the whole paper (binary trees with item lists, sift, the rank threshold, the amortized analysis)
  - paper: "Haim Kaplan and Uri Zwick, A simpler implementation and analysis of Chazelle's soft heaps, Proceedings of the 20th ACM-SIAM Symposium on Discrete Algorithms (SODA 2009), pp. 477 to 485"
    title: "Haim Kaplan and Uri Zwick, A simpler implementation and analysis of Chazelle's soft heaps, SODA 2009"
    locator: the conference paper that the 2013 journal paper simplifies further
  - paper: doi:10.1145/355541.355562
    title: Bernard Chazelle, A minimum spanning tree algorithm with inverse-Ackermann type complexity, Journal of the ACM 47(6), 2000, pp. 1028 to 1047
    locator: the use of soft heaps in the minimum spanning tree algorithm
---

A soft heap is a meldable priority queue that is allowed to make errors. From time to time it raises the key of some items: such an item is *corrupted*, and the heap then treats it as if it had the larger key. In exchange, the operations are faster than the $\Omega(\log n)$ lower bound for exact heaps in the [comparison model](/comparison-model/). For an error rate $0 < \varepsilon < 1$ fixed in advance, at most $\varepsilon n$ items are corrupted at any time, where $n$ is the number of insertions so far, and all the operations take $O(1)$ amortized time except one, which takes $O(\log(1/\varepsilon))$. Bernard Chazelle introduced the soft heap in 1998 and used it for his [minimum spanning tree algorithm](/chazelle-mst/). This page follows the simpler version of Kaplan, Tarjan and Zwick (2013).

## In plain words

An exact heap must keep every key in order, and this costs $\log n$ comparisons per item on average. A soft heap saves work by putting items in groups that share one key. The group key is the largest key in the group. When the heap moves a group up a tree, it does not sort the group; all the items in it now have the group key. An item whose own key is smaller than its group key is corrupted.

Groups are small near the leaves and grow by a factor of $3/2$ for each level above a threshold $T$. Below the threshold, every group has one item, so no item is corrupted there. The threshold is about $\lg(1/\varepsilon)$, and the number of high nodes is small, so few items can be corrupted at any time.

## The abstract type

A soft heap holds items with keys and has these operations.
- `insert(e)`: add item $e$.
- `meld(H1, H2)`: return a heap with the items of both.
- `find-min()`: return an item $e$ and its current key $ckey(e)$, such that $ckey(e)$ is the smallest current key of all items.
- `delete-min()`: the same as find-min, and remove $e$.

For every item, $ckey(e) \ge key(e)$, and the item is corrupted if $ckey(e) > key(e)$. The current key of an item never decreases. The guarantee is that at any time at most $\varepsilon n$ items are corrupted, where $n$ is the number of insertions. So a soft heap is not a [priority queue](/priority-queue/) in the exact sense: delete-min returns an item of smallest *current* key, which may not be the item of smallest key. Some versions also have delete of an arbitrary item; this page does not.

## Representation

The heap is a list of binary trees. Each node $x$ has a rank $r(x)$, two children $left$ and $right$ (each may be NIL), a list of items $list(x)$, and a key $ckey(x)$, which is the current key of all the items in $list(x)$. A new node has rank 0, one item, and the key of that item. A node of rank $k > 0$ is made by a link of two roots of rank $k - 1$, so a child of a node of rank $k$ has rank $k - 1$, but a child can be missing.

The *target size* of a node of rank $k$ is

$$s_k = 1 \text{ for } k \le T, \qquad s_k = \lceil 3 s_{k-1} / 2 \rceil \text{ for } k > T.$$

With $T = 2$ the target sizes for the ranks 0 to 6 are $1, 1, 1, 2, 3, 5, 8$.

The roots are kept in order of rank, at most one root of each rank. For each position in this list the heap keeps a pointer to the root of smallest $ckey$ among the roots of larger or equal rank, so find-min is one pointer step. Kaplan, Tarjan and Zwick call these the suffix-min pointers.

**Invariants.**
1. *Heap order of the current keys.* For a node $x$ and a child $c$, $ckey(x) \le ckey(c)$.
2. *Current keys.* For every item $e$ in $list(x)$, $key(e) \le ckey(x)$, and the current key of $e$ is $ckey(x)$.
3. *Lists.* Every node that is not a leaf has a non-empty list. A node of rank at most $T$ has at most one item.

**The threshold.** The page uses $T = \lceil \lg(1/\varepsilon) \rceil + 5$. The paper uses $T = \lceil \lg(3/\varepsilon) \rceil$ with a sharper count; the larger $T$ here makes the short proof below work, and it changes the costs only by a constant.

## Operations

```pseudo id=main
LINK(x, y)                              ▷ two roots of rank r
L1  z ← a new node of rank r + 1 with the children x and y and an empty list
L2  SIFT(z); return z

SIFT(x)
L3  while |list(x)| < s_{r(x)} and x is not a leaf:
L4      if x.left = NIL or (x.right ≠ NIL and ckey(x.right) < ckey(x.left)) then exchange x.left and x.right
L5      append list(x.left) to list(x); ckey(x) ← ckey(x.left); list(x.left) ← empty
L6      if x.left is a leaf then x.left ← NIL else SIFT(x.left)

INSERT(H, e)
L7  add a new node of rank 0 with the item e as a root; while two roots have the same rank, LINK them

MELD(H1, H2)
L8  add the roots of the heap with fewer roots to the other heap, one at a time, as in line L7

FIND-MIN(H)
L9  x ← the root of smallest ckey (a suffix-min pointer); return an item of list(x) and ckey(x)

DELETE-MIN(H)
L10 x ← the root of smallest ckey
L11 remove an item e from list(x)
L12 if 2 |list(x)| ≤ s_{r(x)} then
L13     if x is not a leaf then SIFT(x)
L14     else if list(x) is empty then remove x from the roots
L15 update the suffix-min pointers from x to the roots of smaller rank; return e and the old ckey(x)
```

SIFT is where items are corrupted. Line L5 moves a whole list up one level and gives it the key of the list of the child, which is the largest key in it. The old items of $x$ keep their place, but their current key goes up to $ckey(x.left)$. For $k > T$ the target size $s_k$ is larger than 1, so the loop of line L3 can take lists from both children, several times. This branching is what gives the soft heap its speed: one SIFT moves many items with few comparisons.

The recursion of SIFT goes down at most the rank of the node, which is at most $\lg n$, so the depth is small.

## Example

Take $T = 2$ (so $s_3 = 2$) and insert the keys $5, 3, 8, 1, 7, 2, 6, 4, 9$. Write a node as `ckey{list}(children)`. The first eight inserts make, by carries as in a binary counter, 7 links and one tree of rank 3, and the last insert adds a root of rank 0:

```text
2{1,2}(4{4}(6{6} 7{7}) 3{3}(5{5} 8{8}))   9{9}
```

Look at the top link. Its children were the trees of rank 2 with the root lists $\{1\}$ and $\{2\}$. The new node of rank 3 has target size 2. SIFT took the list $\{1\}$ (the smaller $ckey$), then the list $\{2\}$, and the key of the node became 2. So the item 1 now has the current key 2, and it is corrupted. Each node of rank at most 2 holds one item with its own key.

Now call delete-min four times. Each call takes an item from the root of rank 3, and its list drops to one item, so $2 \cdot 1 \le s_3$ and line L13 sifts again.

| call | returns (item, current key) | root of rank 3 after the call |
| --- | --- | --- |
| 1 | (2, 2) | `3{1,3}(5{5}(8{8}) 4{4}(6{6} 7{7}))` |
| 2 | (3, 3) | `4{1,4}(6{6}(7{7}) 5{5}(8{8}))` |
| 3 | (4, 4) | `5{1,5}(8{8} 6{6}(7{7}))` |
| 4 | (5, 5) | `6{1,6}(7{7} 8{8})` |

The item 1 stays in the root list and its current key goes up each time. The next delete-min calls return $(6, 6)$, $(7, 7)$, $(8, 8)$, $(1, 8)$ and $(9, 9)$. So the item of smallest key comes out eighth, with the current key 8. The sequence of current keys, $2, 3, 4, 5, 6, 7, 8, 8, 9$, is sorted, as it must be. The test file checks this trace.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). These are the main points.
- *Exact answers for the current keys.* SIFT gives $x$ the $ckey$ of its child of smaller $ckey$, and the child then gets a $ckey$ that is not smaller; so heap order holds. Items move up with the list, and they get a current key at least their old one. So the root of smallest $ckey$ holds an item of smallest current key, and find-min and delete-min are right with respect to the current keys.
- *Few corrupted items.* An item can be corrupted only in a node of rank more than $T$, because lower nodes hold one item and its own key. A node of rank $k$ holds at most $6 (3/2)^{k - T}$ items, since SIFT stops as soon as the list reaches $s_k$. At most $n / 2^k$ nodes of rank $k$ are ever made, because each link uses up two roots of rank $k - 1$. Summing,

$$\#\text{corrupted} \le \sum_{k > T} \frac{n}{2^k} \cdot 6 \left(\frac{3}{2}\right)^{k-T} = \frac{6n}{2^T} \sum_{j \ge 1} \left(\frac{3}{4}\right)^j = \frac{18 n}{2^T} \le \frac{18}{32} \varepsilon n < \varepsilon n.$$

## Complexity

| operation | Chazelle (2000), amortized | Kaplan, Tarjan and Zwick (2013), amortized |
| --- | --- | --- |
| insert | $O(\log(1/\varepsilon))$ | $O(1)$ |
| meld | $O(1)$ | $O(1)$ |
| find-min | $O(1)$ | $O(1)$ |
| delete-min | $O(1)$ | $O(\log(1/\varepsilon))$ |

These bounds are the theorems of the two papers, and this page does not prove them. Chazelle also shows that this trade-off between time and error rate is optimal in the comparison model. The idea of the upper bound is that a node of rank $k > T$ is reached by SIFT only after many items have gone through the nodes below it, and the target sizes grow like $(3/2)^{k}$ while the number of nodes falls like $2^{-k}$.

In the implementation on this page, find-min is $O(1)$, and an update of the suffix-min pointers costs the number of roots of smaller rank, so it is $O(\log n)$ in the worst case. Meld adds the roots of one heap one at a time, which costs $O(\log n)$; the papers meld in $O(1)$ amortized time by a merge of the two root lists. The implementation counts links and list moves. For $40000$ inserts of random keys followed by $40000$ delete-min calls, the count per operation was $1.59$ for $T = 0$, $2.58$ for $T = 2$, $3.58$ for $T = 4$, $4.56$ for $T = 6$, $5.52$ for $T = 8$ and $6.42$ for $T = 10$. This grows by about $1/2$ for each step of $T$, which matches $O(\log(1/\varepsilon))$.

Space is $\Theta(n)$: there are at most $2n$ nodes, since each link makes one node out of two, and each item is in one list.

## Variants

- *Chazelle's original soft heap* uses binomial trees, and a node holds a list of items, which Chazelle calls car-pooling. It makes inserts cost $O(\log(1/\varepsilon))$ and all other operations $O(1)$ amortized.
- *Kaplan and Zwick (2009)* replaced the binomial trees by binary trees and gave a simpler analysis. *Kaplan, Tarjan and Zwick (2013)* removed more cases and moved the $O(\log(1/\varepsilon))$ cost to delete-min; this page follows their structure.
- *Delete of an arbitrary item.* Chazelle's version and later versions can delete a given item; this page leaves it out.

## When to use it

A soft heap is useful when an algorithm needs an approximate order and can repair the errors later.
- *Linear-time [selection](/selection-problem/).* Insert all $n$ items into a soft heap with $\varepsilon = 1/3$ and call delete-min $n/3$ times. Let $x$ be the largest *original* key among the deleted items. Then at least $n/3 - 1$ items have keys at most $x$, the other deleted items. Every item that is still in the heap has a current key at least the current key of every deleted item, and so at least $x$. At least $2n/3 - n/3 = n/3$ of them are not corrupted, so they have keys at least $x$. So $x$ is a good pivot, and the rest is as in [median of medians](/median-of-medians/). This takes $O(n)$ time.
- *[Minimum spanning trees](/minimum-spanning-tree/).* Chazelle's [algorithm](/chazelle-mst/) uses soft heaps to find a minimum spanning tree in $O(m \, \alpha(m, n))$ time.
- *Approximate sorting.* Soft heaps sort a sequence so that only a few items are out of place.

Do not use a soft heap where you need exact order, such as [Dijkstra's algorithm](/dijkstra/) or [heapsort](/heapsort/).

## Pitfalls

- **Comparing original keys after the fact.** delete-min returns the current key. To use the order, an algorithm must reason about current keys, as the selection argument does, and not assume that the returned items come out in order of their own keys.
- **Choosing $T$ too small.** With $T = 0$ almost every item can be corrupted. The error bound needs $2^T$ to be a constant times $1/\varepsilon$.
- **Counting $n$ wrongly.** The bound is $\varepsilon$ times the number of *insertions*, not the current size. After many deletions, almost all the items that are left can be corrupted.
- **Forgetting to clean up empty leaves.** A leaf whose list was taken by its parent must go, or a later SIFT reads an empty list and a stale $ckey$.
- **Updating only one suffix-min pointer.** After a delete-min the $ckey$ of the root changes, and the pointers of all roots of smaller rank can change.
- **Different thresholds in a meld.** The target size depends on $T$, so two heaps can be melded only if they use the same $T$.

## Implementations

The Python implementation in `impl/python/soft_heap.py` follows the pseudocode. It keeps the roots in a list of decreasing rank, and a list `best` in the place of the suffix-min pointers. A heap is made with an error rate `eps`, which gives $T = \lceil \lg(1/\varepsilon) \rceil + 5$, or with `t` directly, as in the example. `check_invariant` checks the ranks, the heap order of the current keys, the keys of the items, the list sizes and the bound of $18 n / 2^T$ corrupted items. The tests check the example, meld, the error rate for $5000$ items, and 600 random sequences of inserts, melds and delete-mins, in which every delete-min must return the smallest current key.

## History

Bernard Chazelle presented the soft heap at ESA 1998 and published it in the Journal of the ACM in 2000, next to his minimum spanning tree algorithm, which is its main application. The ESA paper received the ESA Test-of-Time Award in 2018. Haim Kaplan and Uri Zwick gave a simpler implementation and analysis at SODA 2009, and Kaplan, Tarjan and Zwick published a further simplified version in 2013.

## References
