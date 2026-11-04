---
tag: DBACA1
kind: data-structure
slug: thin-heap
name: Thin heap
aliases:
- thin heaps
area: data-structures/heaps
level: research
summary: Fibonacci-bound heap with a simpler structure and less space than Fibonacci heaps.
implements: [priority-queue, meldable-priority-queue]
model: comparison-model
complexity:
  vars: {n: the number of items in the heap}
  time: {worst: O(n), amortized: O(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [fibonacci-heap, binomial-heap, decrease-key, potential-method]
see_also: [fibonacci-heap, rank-pairing-heap, violation-heap, hollow-heap, pairing-heap, strict-fibonacci-heap, dijkstra, prim]
sources:
  - paper: doi:10.1145/1328911.1328914
    title: Haim Kaplan and Robert E. Tarjan, Thin heaps, thick heaps, ACM Transactions on Algorithms 4(1), Article 3, 2008
    locator: the sections on thin heaps (thin trees, the rank rules, the repair of decrease-key, and the amortized analysis)
  - paper: doi:10.1145/28869.28874
    title: Michael L. Fredman and Robert E. Tarjan, Fibonacci heaps and their uses in improved network optimization algorithms, Journal of the ACM 34(3), 1987
    locator: Sections 2 and 3 (the Fibonacci heap, whose bounds the thin heap matches)
---

A thin heap is a collection of heap-ordered *thin trees*, with a pointer to the root of minimum key. It has the amortized bounds of the [Fibonacci heap](/fibonacci-heap/): $O(1)$ for insert, find-min, meld and [decrease-key](/decrease-key/), and $O(\log n)$ for delete-min. It needs no parent pointer and no mark bit. A node keeps its key, a rank and three pointers, and the information that a Fibonacci heap keeps in the mark bit is in the ranks: a node is *thin* when it has lost its child of highest rank. Haim Kaplan and Robert Tarjan published thin heaps in 2008, in a paper that also describes thick heaps.

## In plain words

Think of a [binomial heap](/binomial-heap/). Each tree has a rank $k$, and the root has exactly one child of each rank $k - 1, k - 2, \ldots, 0$. Two trees of the same rank join into one tree of the next rank.

A thin heap allows one defect: a node may be missing its largest child. Such a node is "thin". When decrease-key cuts a node out of a tree, the tree is repaired with a small number of local steps. A node that is not thin gives up its largest child and becomes thin. A node that is already thin drops one rank, and the problem moves one step to the left or up. Each such step removes one thin node, so the steps are paid for in advance.

## The abstract type

A thin heap implements the [meldable priority queue](/meldable-priority-queue/) with decrease-key: `insert(k)` returns a handle to the new node, and there are `find-min()`, `delete-min()`, `meld(H1, H2)` and `decrease-key(handle, k)`. This page uses a min-heap. Delete of an arbitrary node is decrease-key to $-\infty$ and then delete-min.

## Representation

Each node $x$ has a key, a rank $r(x) \ge 0$, and three pointers:
- $child$: the first child, which has the highest rank among the children,
- $right$: the next sibling, or the next root in the root list,
- $left$: the previous sibling, or the parent if $x$ is a first child; for a root it is NIL.

The children of a node are in a list in decreasing order of rank. A node with no child has rank 0 or 1. The root list is a singly linked list with a head and a tail, and the heap also keeps a pointer $min$ and the count $n$. For the rank of NIL, use $-1$.

**Invariants.**
1. *Heap order.* The key of each node is at least the key of its parent.
2. *Thin-tree ranks.* The children of a node $x$ have the ranks $r(x) - 1, r(x) - 2, \ldots, 0$ (then $x$ is *normal*), or $r(x) - 2, \ldots, 0$ (then $x$ is *thin*). So $x$ is thin exactly when $r(x) = r(x.child) + 2$.
3. *Roots are normal.*

A normal tree with no thin node is a binomial tree. A thin node has lost its child of highest rank, as a marked node in a Fibonacci heap has lost one child, but the thin heap sees this from the ranks.

**Rank bound.** Let $s_k$ be the smallest number of nodes in a subtree whose root has rank $k$. The smallest subtrees have thin roots and thin children, so $s_0 = s_1 = 1$ and $s_k = 1 + s_0 + \cdots + s_{k-2}$. This gives $s_k = F_{k+1}$, the $(k+1)$-th [Fibonacci number](/fibonacci-numbers/). So a node in a heap of $n$ items has rank at most $\log_\varphi n + 1$, where $\varphi = (1 + \sqrt 5)/2$.

## Operations

```pseudo id=main
LINK(x, y)                              ▷ two normal roots of equal rank
L1  if y.key < x.key then swap x and y
L2  make y the first child of x; r(x) ← r(x) + 1; return x

INSERT(H, k)
L3  add a new node of rank 0 to the root list; update H.min

DELETE-MIN(H)                           ▷ H is not empty
L4  z ← H.min; put the children of z with the other roots, and give each thin one the rank r(c.child) + 1
L5  for each root x: while a root y of rank r(x) is in the bucket: x ← LINK(x, y)
L6      put x in the bucket of rank r(x)
L7  make the buckets the root list; H.min ← the smallest root; return z.key

DECREASE-KEY(H, x, k)                   ▷ k ≤ x.key
L8  x.key ← k; if x is a root then update H.min and return
L9  y ← x.left; cut x and its subtree, make x a normal root, update H.min
L10 loop                                ▷ the rank sequence at y has a defect
L11     if x was the first child of y then
L12         if y is a root then r(y) ← r(y.child) + 1; return
L13         if r(y) = r(y.child) + 2 then return       ▷ y was normal and is now thin
L14         x ← y; y ← y.left; cut x, make it a normal root   ▷ parent violation
        else                                           ▷ y is the left sibling of the hole
L15         if y is normal then move y.child to the place just right of y; return
L16         r(y) ← r(y) − 1; x ← y; y ← y.left          ▷ y was thin and is now normal
```

**Link** (lines L1 and L2) is the link of a binomial heap. Both roots are normal with rank $k$, and the result is a normal root of rank $k + 1$ whose first child has rank $k$.

**Delete-min** (lines L4 to L7) removes the minimum root, puts its children in the root list, and links roots of equal rank until all ranks differ, as in a Fibonacci heap. A thin child would be a thin root; line L4 lowers its rank by one, which makes it normal without any other change.

**Decrease-key** (lines L8 to L16) lowers the key. If $x$ is not a root, it may now break heap order, so line L9 cuts $x$ with its subtree and makes it a root. If $x$ was thin, its rank drops by one, so the new root is normal. The hole that $x$ leaves breaks the rank rule of its parent. Let $y$ be the node just left of the hole: the parent of $x$ if $x$ was a first child, and the left sibling of $x$ otherwise. There are two cases.

- *Sibling case.* The right neighbor of $y$ now has a rank two less than $r(y)$. If $y$ is normal (line L15), its first child has the missing rank: move it into the hole. Then $y$ is thin, and every rule holds. If $y$ is thin (line L16), drop its rank by one; $y$ is then normal and fills the missing rank, and the hole moves to the place just left of $y$.
- *Parent case.* The first child of $y$ now has a rank one less than before. If $y$ is a root, fix its rank and stop (line L12). If $y$ was normal, it is now thin, which is allowed (line L13). If $y$ was already thin, its rank is now 3 more than its first child, which is not allowed. Line L14 cuts $y$ and makes it a root, and the hole is now where $y$ was.

Each step goes one place to the left or one level up, so the loop ends.

**Insert, meld and find-min.** Insert adds a root of rank 0 (line L3). Meld joins the two root lists at the tail and keeps the smaller minimum. Find-min returns $H.min$.

## Example

Write a node as key:rank, add t after the rank if the node is thin, and put the children in parentheses in list order. Insert 10, 20, ..., 90, and delete the minimum. The delete-min returns 10 and makes 7 links on the 8 other roots, which leaves one binomial tree:

20:3(60:2(80:1(90:0), 70:0), 40:1(50:0), 30:0)

**Decrease 50 to 5.** Node 50 is the first child of 40, so this is the parent case. 40 was normal with rank 1, and now has no child. It is thin, 40:1t, and the loop stops. The heap is 20:3(60:2(80:1(90:0), 70:0), 40:1t, 30:0) and the root 5:0.

**Decrease 30 to 3.** Node 30 is the last child of 20, and its left sibling is 40. This is the sibling case. 40 is thin, so line L16 drops its rank to 0, and 40:0 now fills rank 0. The hole moves left: it is now between 60 (rank 2) and 40 (rank 0). The left sibling 60 is normal, so line L15 moves its first child 80:1(90:0) into the hole, and 60 becomes thin. The heap is 20:3(60:2t(70:0), 80:1(90:0), 40:0), with the roots 5:0 and 3:0.

**Decrease 70 to 7.** Node 70 is the first child of 60, which is thin. After the cut, 60 has rank 2 and no child, 3 more than the rank $-1$ of NIL. This is a parent violation, so line L14 cuts 60 and makes it a root of rank 0. The hole is now at the first child of 20, which is a root, so line L12 sets the rank of 20 to $1 + 1 = 2$. The heap is 20:2(80:1(90:0), 40:0), with the roots 5:0, 3:0, 7:0 and 60:0.

**Delete-min.** It returns 3. The other roots are 20:2, 5:0, 7:0 and 60:0. One link joins 5 and 7 into 5:1(7:0), so the roots are 60:0, 5:1(7:0) and 20:2(80:1(90:0), 40:0), with minimum 5.

## Correctness

Heap order holds because a link puts the larger root under the smaller one, a cut makes a node a root, and decrease-key cuts the node whose key went down. Inside the subtree of a cut node, the keys are at least the old key of the root of that subtree, so heap order there still holds. The rank rules are repaired by the loop of decrease-key. In every iteration, the only defect is a single hole at $y$, and each branch either removes the hole or moves it to the left neighbor or the parent of $y$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | worst case | amortized |
|---|---|---|
| find-min | $O(1)$ | $O(1)$ |
| insert, meld | $O(1)$ | $O(1)$ |
| decrease-key | $O(\log n)$ | $O(1)$ |
| delete-min | $O(n)$ | $O(\log n)$ |
| space | key, rank and three pointers per node | |

**Worst case.** In the loop of decrease-key, each step goes to a node of higher rank: a left sibling has rank one more, and a parent has rank one or two more than its first child. Ranks are at most $\log_\varphi n + 1$, so one decrease-key does $O(\log n)$ steps. A delete-min can find up to $n - 1$ roots, after $n$ inserts.

**Amortized cost.** Count one unit for each root that delete-min looks at, one for each link, and one for each step of the loop of decrease-key. Use the [potential method](/potential-method/) with
$$\Phi = 2 \cdot (\text{number of trees}) + 4 \cdot (\text{number of thin nodes}).$$
- *Insert* adds one tree: amortized cost 3. *Meld* does not change $\Phi$.
- *Decrease-key.* The first cut adds one tree, $+2$, and if $x$ was thin, it is no longer thin. Each step of line L16 makes a thin node normal: actual cost 1, potential $-4$. Each step of line L14 makes a thin node a normal root: actual cost 1, potential $+2 - 4 = -2$. The last step makes at most one node thin, $+4$. So the amortized cost is at most 8, which is $O(1)$.
- *Delete-min.* Let $t$ be the number of trees before, $d = r(z) \le \log_\varphi n + 1$ the number of children of the minimum, and $t'$ the number of trees after. The operation looks at $t - 1 + d$ roots and makes $\ell = t - 1 + d - t'$ links, because each link removes one tree. No node becomes thin. With one more unit for the operation and $t'$ units to build the new root list, the amortized cost is at most $1 + (t - 1 + d) + \ell + t' + 2(t' - t) = 2d - 1 + 2t'$. All ranks at the end differ and are at most $\log_\varphi n + 1$, so $t' \le \log_\varphi n + 2$, and the amortized cost is $O(\log n)$.

The full proof is in [the complexity proof](proofs/complexity.md).

## Variants

- **Thick heaps.** The same paper describes a second version of thin heaps and a related structure, thick heaps, with a repair step of its own. All of them have the amortized bounds of Fibonacci heaps.
- **Fat heaps.** In a separate paper, Kaplan and Tarjan give fat heaps, which get the bounds of the Fibonacci heap in the worst case, except meld.
- **Other simple Fibonacci-bound heaps.** The [rank-pairing heap](/rank-pairing-heap/) does not cut subtrees out of the middle of a tree and needs no cascade of cuts. The [violation heap](/violation-heap/) and the [hollow heap](/hollow-heap/) are other heaps with the same amortized bounds.

## When to use it

Use a thin heap where a Fibonacci heap fits: in algorithms with many more decrease-keys than delete-mins, such as [Dijkstra's algorithm](/dijkstra/) or [Prim's algorithm](/prim/) on dense graphs, where the $O(1)$ amortized decrease-key gives $O(m + n \log n)$ time. It uses less memory per node than a Fibonacci heap and has fewer cases to code. In many practical tests, a [binary heap](/binary-heap/) or a [pairing heap](/pairing-heap/) is still faster, because the constant factors of a thin heap are larger.

## Pitfalls

- **Thin roots.** A child of the deleted minimum can be thin. If it becomes a root without the rank fix of line L4, two roots of the same rank can have different shapes, and LINK makes a tree that breaks the rank rule.
- **The left pointer has two meanings.** The left pointer of a first child points to the parent. Code must test `y.child = x` to know if $y$ is the parent or the left sibling, before it changes any pointer.
- **Stopping too early in the parent case.** When the parent was already thin, lowering its rank is not enough: its rank would then clash with the rank of its right sibling. The node must be cut, as in line L14.
- **Stale handles.** The handle that insert returns is the node. After delete-min removes a node, its handle must not be used again.

## Implementations

The Python version follows the pseudocode, with `_cut` for the cut of lines L9 and L14. It keeps the root list as a singly linked list with a tail pointer, so that meld is $O(1)$, and it collects the roots in a dictionary by rank during delete-min. The `check_invariant` method checks heap order, the rank rules, the pointers and the bound $s_k \ge F_{k+1}$.

## History

Fredman and Tarjan introduced Fibonacci heaps in 1984. Kaplan and Tarjan published thin heaps, with thick heaps, in ACM Transactions on Algorithms in 2008, building on ideas of Peter Høyer from 1995. Their goal was a heap with the same amortized bounds but with less space per node and a simpler structure, in which the state of a node is part of its rank.

## References
