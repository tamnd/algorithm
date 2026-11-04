---
tag: HWWSW6
kind: data-structure
slug: violation-heap
name: Violation heap
aliases:
- violation heaps
area: data-structures/heaps
level: research
summary: Heap that tracks heap-order violations to achieve Fibonacci-heap bounds with simpler structure.
implements: [priority-queue, meldable-priority-queue]
model: comparison-model
complexity:
  vars: {n: the number of items in the heap}
  time: {worst: O(n), amortized: O(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [fibonacci-heap, decrease-key, potential-method, fibonacci-numbers]
see_also: [fibonacci-heap, rank-pairing-heap, thin-heap, pairing-heap, relaxed-heap, hollow-heap, strict-fibonacci-heap, dijkstra]
sources:
  - paper: doi:10.1007/978-3-642-14031-0_51
    title: "Amr Elmasry, The violation heap: a relaxed Fibonacci-like heap, COCOON 2010, Lecture Notes in Computer Science 6196, Springer, 2010, pp. 479 to 488"
    locator: Section 3 (structure, formula (1) for the rank, the 3-way join, the operations, Lemmas 1 to 5 and Theorem 1)
  - paper: arXiv:0812.2851
    title: "Amr Elmasry, The violation heap: a relaxed Fibonacci-like heap, arXiv:0812.2851, version 2, 2010"
    locator: Section 3; Section 2 gives the motivation and Section 4 the comments on the pointer machine
  - paper: doi:10.1142/S1793830910000838
    title: Amr Elmasry, The violation heap, a relaxed Fibonacci-like heap, Discrete Mathematics, Algorithms and Applications 2(4), 2010, pp. 493 to 504
    locator: the journal version of the same paper
  - paper: doi:10.1145/28869.28874
    title: Michael L. Fredman and Robert E. Tarjan, Fibonacci heaps and their uses in improved network optimization algorithms, Journal of the ACM 34(3), 1987
    locator: Sections 2 and 3 (the bounds that the violation heap matches)
---

A violation heap is a collection of heap-ordered multiway trees with the amortized bounds of the [Fibonacci heap](/fibonacci-heap/): $O(1)$ for find-min, insert, meld and [decrease-key](/decrease-key/), and $O(\log n)$ for delete-min. It does not do cascading cuts. When a key decreases, the node is cut, its largest recent child takes its place, and the ranks of the ancestors are lowered by a fixed formula until a rank does not change. The structure is "relaxed": the degree of a node is not bounded in terms of its subtree size, and only the rank is. Each node has a key, an integer rank and three pointers, and there is no parent pointer and no mark bit. Amr Elmasry described the violation heap in 2010.

## In plain words

Trees join three at a time: three roots of the same rank become one tree, the smallest root on top, and its rank goes up by one. So a node collects its children in pairs, and the last two children of a node, the *active* children, are the two from the newest join.

The rank of a node depends only on the ranks of its two active children. When decrease-key cuts a node, the heap does not repair the shape of the tree. It only lowers ranks: the parent of the cut position gets a new rank from its active children, and if that rank is lower, the same is done one level up. The other children of a node can lose any number of descendants and this costs nothing, because the rank does not look at them.

## The abstract type

A violation heap implements the [meldable priority queue](/meldable-priority-queue/) with decrease-key: `insert(k)` returns a handle, and there are `find-min()`, `delete-min()`, `meld(H1, H2)` and `decrease-key(handle, k)`. This page uses a min-heap. Delete of an arbitrary item is decrease-key to $-\infty$ and then delete-min.

## Representation

Each node $x$ has a key, a rank $r(x) \ge 0$, and three pointers:
- $last$: the last (newest) child of $x$,
- $left$: the previous (older) sibling, or NIL for the first child and for a root,
- $right$: the next (newer) sibling; for the last child it is the parent, and for a root it is NIL.

So the children of a node are in a doubly linked list, oldest first. The heap keeps a list of roots and a pointer $min$ to a root of smallest key. The paper keeps the roots in a singly linked circular list with the minimum first; the implementation below uses an array.

A child is *active* if it is one of the last two children of its parent. The parent of an active node is one or two $right$ steps away, so it is found in $O(1)$ time. The parent of any other node cannot be found quickly, and it is never needed. The rank of a missing child is $-1$. For a node $z$ with active children $z_1$ and $z_2$, define

$$\rho(z) = \left\lceil \frac{r(z_1) + r(z_2)}{2} \right\rceil + 1,$$

which is formula (1) of the paper. A leaf has $\rho = 0$, and a node with one child of rank 0 has $\rho = 1$.

**Invariants.**
1. *Heap order.* The key of each node is at least the key of its parent.
2. *Rank rule.* Every node $z$ has $0 \le r(z) \le \rho(z)$.

The paper also defines the *violation* of a node, $\max(0, d(z)/2 - r(z))$, where $d(z)$ is the number of children. It is used only in the analysis, and the heap does not store it.

**Size bound.** A subtree whose root has rank $r$ has at least $F_{r+2}$ nodes, where $F$ are the [Fibonacci numbers](/fibonacci-numbers/) with $F_1 = F_2 = 1$. So every rank is at most $\log_\varphi n$, with $\varphi = (1 + \sqrt 5)/2$. The proof is in [the correctness proof](proofs/correctness.md); the paper proves the weaker bound $F_r$ as Lemma 5.

## Operations

```pseudo id=main
JOIN3(z, z1, z2)                        ▷ three roots of equal rank
L1  rename the three so that z has the smallest key
L2  if the last child of z has smaller rank than the one before it, swap these two children
L3  make z1 and z2 the last two children of z; r(z) ← r(z) + 1; return z

INSERT(H, k)
L4  add a new root of key k and rank 0; update H.min

MELD(H1, H2)
L5  join the root lists; H.min ← the smaller of the two minima

DELETE-MIN(H)                           ▷ H is not empty
L6  z ← H.min; remove z and make each of its children a root
L7  for each root x: while the bucket of rank r(x) holds two roots y1, y2: empty it; x ← JOIN3(x, y1, y2)
L8      put x in the bucket of rank r(x)
L9  make the buckets the root list; H.min ← the smallest root; return z.key

DECREASE-KEY(H, x, k)                   ▷ k ≤ x.key
L10 x.key ← k; if x is a root then update H.min and return
L11 p ← the parent of x if x is active, else NIL; if p ≠ NIL and k ≥ p.key then return
L12 z1 ← the active child of x with the larger rank, or NIL if x is a leaf
L13 remove z1 from the children of x, and put it in the place of x (if z1 = NIL, just remove x)
L14 r(x) ← ρ(x); make x a root; update H.min
L15 while p ≠ NIL: if ρ(p) ≥ r(p) then return
L16     r(p) ← ρ(p); p ← the parent of p if p is active, else NIL
```

Line L2 is in the paper: it keeps the larger of the two old active children next to the new pair. The analysis uses it, and the correctness does not depend on it.

Line L11 has two jobs. An active node whose key is still at least its parent's key stays where it is. For a node that is not active, the parent is unknown, so it is always cut, and no rank changes above it, because only active children count in $\rho$.

## Example

Insert the keys $10, 20, \ldots, 100$ and call delete-min. It returns 10 and leaves nine roots of rank 0. The bucket loop joins them three at a time: $(20, 30, 40)$, $(50, 60, 70)$ and $(80, 90, 100)$ give three roots of rank 1, and these join into one tree. That is 4 joins. Write a tree as `key:rank(children, oldest first)`:

```text
20:2(40:0, 30:0, 80:1(100:0, 90:0), 50:1(70:0, 60:0))
```

The children of 20 are two pairs: 40 and 30 from the first join, then 80 and 50 from the last one. The active children of 20 are 80 and 50, so $\rho(20) = \lceil (1 + 1)/2 \rceil + 1 = 2$. Now do five decrease-key operations.

| step | operation | what happens | rank changes |
| --- | --- | --- | --- |
| 1 | 90 to 5 | 90 is an active leaf under 80; it is cut. Now $\rho(80) = \lceil (0 - 1)/2 \rceil + 1 = 1 = r(80)$, so the loop stops at once. | 0 |
| 2 | 50 to 45 | 50 is active and $45 \ge 20$, so line L11 returns. | 0 |
| 3 | 40 to 35 | 40 is not active; it is cut, and nothing is checked above it. | 0 |
| 4 | 45 to 15 | the active children of 45 are 60 and 70, both of rank 0, and the last one, 60, takes the place of 45. The node 15 becomes a root with the child 70 and rank 1. Then $\rho(20) = \lceil (1 + 0)/2 \rceil + 1 = 2$, so the loop stops. | 0 |
| 5 | 100 to 8 | 100 is cut from 80, which is now a leaf: $\rho(80) = 0 < 1$, so $r(80) \leftarrow 0$. The node 80 is active, so go up: $\rho(20) = \lceil (0 + 0)/2 \rceil + 1 = 1 < 2$, so $r(20) \leftarrow 1$. 20 is a root, so stop. | 2 |

Step 1 shows the parity effect of formula (1): if the sum of the two active ranks is even, one of them can drop by one and the parent keeps its rank. The heap is now

```text
20:1(30:0, 80:0, 60:0)  5:0  35:0  15:1(70:0)  8:0
```

A delete-min now returns 5. The four other roots have the ranks 1, 0, 1, 0, and no three have the same rank, so there is no join. The test file checks this trace step by step.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). The main points are these. Heap order holds because a cut makes a node a root and a join puts the smallest root on top. A node that takes the place of its parent $x$ had a key at least $x.key$, and so at least the key of the parent of $x$. Each root holds the smallest key of its tree, so $H.min$ holds a smallest key.

For the rank rule, look at what changes $\rho(p)$. It is a function of the active children of $p$ only, so it changes when an active child is replaced or removed (line L13 at the parent of $x$), when the rank of an active child drops (line L16), or when $p$ gets children in a join (line L3). A join sets $r(z) = \rho(z)$ exactly. In the other two cases the loop of lines L15 and L16 visits $p$, and sets the rank down to $\rho(p)$ if it was larger. A rank never goes up except in a join or at line L14, where the node is a root. So $r \le \rho$ holds for all nodes when the operation ends. When the loop stops at a node whose rank did not change, its parent sees no change.

The size bound follows from the rank rule by induction. Let the active children of $z$ have ranks $a \ge b$. From $r(z) \le \lceil (a + b)/2 \rceil + 1$ we get $r(z) \le a + 1$, and if $a = r(z) - 1$ then $b \ge r(z) - 2$ (the paper's Lemma 3). In the first case the subtree of the child of rank $a \ge r(z)$ alone has $F_{r(z)+2}$ nodes, and in the second the two children give $1 + F_{r(z)+1} + F_{r(z)} > F_{r(z)+2}$.

## Complexity

| operation | amortized | worst case |
| --- | --- | --- |
| find-min | $O(1)$ | $O(1)$ |
| insert, meld | $O(1)$ | $O(1)$ |
| decrease-key | $O(1)$ | $O(n)$ |
| delete-min | $O(\log n)$ | $O(n)$ |

The amortized bounds are Theorem 1 of the paper. The paper gives no worst-case bound for decrease-key. Each step of the loop goes one level up, so the cost is at most the height of the tree plus one, and the paper proves no bound on the height, because the shape is never repaired. Delete-min can meet $n - 1$ roots after $n$ inserts.

The amortized analysis in the paper uses the potential $3\gamma + 2\vartheta + \tau + \Delta$. Here $\tau$ is the number of trees, $\vartheta$ is the sum of the violations, $\gamma$ is the number of *critical* nodes (active nodes whose two active children have an odd rank sum), and $\Delta$ counts some decrease-key operations that stopped at the third and fourth child from the end of a node. The steps of the argument are these.
- A join removes two trees, so $\tau$ drops by 2, and it adds no violation, because $d(z)/2 - r(z)$ does not change when $z$ gets two children and one rank (Lemma 1). So each join is free.
- In decrease-key, a rank drops only at a critical node, and then the node becomes non-critical. So each step of the loop is paid by the drop of $3\gamma$, less the $2\vartheta$ for one more unit of violation. The cut node $x$ itself may lose rank at line L14; the paper bounds the extra violation by the drop in $\Delta$ plus 2.
- In delete-min, the $d$ children of the minimum become trees, so $\tau$ grows by $d$, while $\vartheta$ drops by at least $d/2 - r$. So the potential grows by at most $2r = O(\log n)$. After the joins at most two roots of each rank are left, so at most $2 \log_\varphi n + 2$ roots.

This page does not give a separate full proof of the amortized bounds; the test file checks, on 600 random sequences, that the number of joins, loop steps and surviving roots stays below 8 per operation plus $8(\log_2 n + 1)$ per delete-min.

Space is $\Theta(n)$: three pointers and one integer per node.

## Variants

- *The technical report version* of the paper (arXiv version 1, 2008) is different from the published one, as the paper says in its comments.
- *Rank-pairing heaps* use the same idea of rank updates in place of cascading cuts, on half-ordered binary trees. The violation heap paper says that this idea appeared in the [rank-pairing heap](/rank-pairing-heap/) paper independently, and that the update rules differ.
- *Two-way joins.* The paper uses 3-way joins on purpose: after a plain link of two trees the new root can be critical, which would need more potential.

## When to use it

Use a violation heap when you want Fibonacci-heap amortized bounds with less bookkeeping than a [Fibonacci heap](/fibonacci-heap/): no parent pointers, no marks and no cascading cuts. The paper expects good practical behaviour but does not give experiments. For most programs a [pairing heap](/pairing-heap/) or a binary heap is simpler and fast. If you need worst-case bounds, use a [strict Fibonacci heap](/strict-fibonacci-heap/) or a [Brodal queue](/brodal-queue/).

## Pitfalls

- **Recomputing the rank of a node that is not active.** Only the last two children count in $\rho$. A change below an older child must not go up, and the code cannot find the parent of such a child anyway.
- **Forgetting the new active child.** When an active leaf is removed, the third child from the end becomes active, and its rank enters $\rho$ of the parent. The loop must start at the parent in this case too.
- **Using a plain 2-way link.** The 3-way join keeps $d(z)/2 - r(z)$ fixed. A 2-way link that adds one child and one rank breaks the analysis.
- **Unbounded degree.** A node can have many more than $2 \log n$ children, so do not size an array of children by the rank.
- **Rounding.** Formula (1) uses the ceiling of a possibly negative half sum: a node with one child of rank 0 has $\rho = \lceil -1/2 \rceil + 1 = 1$. In Python, `-((-s) // 2)` gives the ceiling; `s // 2` and `int(s / 2)` do not.
- **Recursion.** Trees can be deep, so walk them with an explicit stack.

## Implementations

The Python implementation in `impl/python/violation_heap.py` follows the pseudocode line by line. It keeps the three pointers of the paper and finds the parent of an active node through the $right$ pointers. It counts joins and loop steps, and `check_invariant` checks the links, heap order, the rank rule and the size bound $F_{r+2}$ on every node. The tests compare it with `heapq` on 600 random sequences of inserts, decrease-keys and delete-mins.

## History

Amr Elmasry put the first version of the paper on arXiv in December 2008, under the title "Violation heaps: an alternative to Fibonacci heaps", and presented the violation heap at COCOON 2010. His aim was a heap with the bounds of the Fibonacci heap of Fredman and Tarjan (1987) that is also fast in practice, and the paper compares it with [thin heaps](/thin-heap/), 2-3 heaps and [relaxed heaps](/relaxed-heap/). The idea to replace a cut node by one of its children comes from his earlier work on pairing heaps with $O(\log \log n)$ decrease-key (SODA 2009). Haeupler, Sen and Tarjan published [rank-pairing heaps](/rank-pairing-heap/) at ESA 2009 with a related idea.

## References
