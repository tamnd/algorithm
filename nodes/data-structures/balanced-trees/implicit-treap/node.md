---
tag: 47AZT5
kind: data-structure
slug: implicit-treap
name: Implicit treap
aliases:
- Implicit Treap
area: data-structures/balanced-trees
level: advanced
summary: A treap keyed by position in the sequence rather than by stored key, supporting insertion, deletion, reversal and range operations on arrays.
implements: [list]
model: word-ram
complexity:
  vars: {n: the number of items in the list}
  time: {expected: Θ(log n), worst: Θ(n)}
  space: {extra: Θ(n)}
prereqs: [treap, treap-split, treap-merge, order-statistic-tree]
see_also: [rope, segment-tree, splay-tree, link-cut-tree, persistent-treap, weight-balanced-tree, cartesian-tree]
sources:
  - paper: doi:10.1007/BF01940876
    title: Raimund Seidel and Cecilia R. Aragon, Randomized search trees, Algorithmica 16(4/5), 1996
    locator: pages 464 to 497, the expected depth, and split and join on treaps
  - url: https://cp-algorithms.com/data_structures/treap.html
    title: cp-algorithms, Treap (Cartesian tree)
    locator: the section Implicit Treaps, with insertion by position, reversal by a lazy flag, and range queries
---

An implicit treap is a [treap](/treap/) that stores a list instead of a set. The nodes hold the items of the list, and the in-order sequence of the nodes is the list itself, so the "key" of a node is its position, which is never stored. Each node stores the size of its subtree instead, and the position of a node is found from the sizes on the way down. Every operation is built from two primitives: [split](/treap-split/) by position, which cuts the list into its first $i$ items and the rest, and [merge](/treap-merge/), which concatenates two lists. With them, the tree inserts and deletes at any position, cuts and pastes whole ranges, reverses a range with a lazy flag, and answers range queries such as sums, all in $O(\log n)$ expected time. The random priorities keep the tree balanced in expectation, whatever the operations are.

## In plain words

Think of an array where you want to insert in the middle, cut a piece out and paste it elsewhere, or turn a piece around, and you want each of these to be fast. An array is slow at this, because it must move many items.

An implicit treap keeps the items in a tree. To reach the $i$-th item, each node tells how many items lie below it, so you know whether to go left or right. To work on a range, you cut the tree into three pieces, before, inside and after the range, work on the middle piece, and glue the pieces back. Turning a range around is done lazily: you mark the middle piece "reversed" and do the actual swapping only when you visit it later.

## The abstract type

The tree implements the [list](/list/) type: a sequence $L = \langle x_0, \ldots, x_{n-1} \rangle$ with GET$(i)$, INSERT$(i, x)$ (before position $i$), DELETE$(i)$, and also two operations that a plain list does not have:

- REVERSE$(lo, hi)$, which reverses the items at positions $lo$ to $hi - 1$;
- RANGE-SUM$(lo, hi)$, the sum of those items; any associative operation, such as minimum or maximum, works the same way.

Positions start at 0, and ranges are half open.

## Representation

A node holds:

1. $value$, the item;
2. $prio$, a random priority, drawn once when the node is made;
3. $left$ and $right$;
4. $size$, the number of nodes in the subtree;
5. $total$, the sum of the values in the subtree;
6. $rev$, a lazy flag that means "this subtree must still be mirrored".

The list that a subtree represents is its in-order sequence, read backwards when $rev$ is set (and the same rule applies inside, with the flags of the children). The invariants are the heap order on priorities, a parent's priority at least its children's, and correct $size$ and $total$ fields. A reversal changes neither the size nor the sum, so these fields stay right under a pending flag.

No keys are compared. The only order is the order of the nodes in the tree.

## Operations

PUSH$(t)$ applies a pending flag at $t$: it swaps the children of $t$, toggles their flags and clears its own. UPDATE$(t)$ recomputes $size$ and $total$ from the children. Each node is pushed before its children are used.

```pseudo id=main
SPLIT(t, i)                                ▷ returns (A, B): A has the first i items
L1  if t = nil then return (nil, nil)
L2  PUSH(t)
L3  if size(t.left) < i then (A, B) ← SPLIT(t.right, i − size(t.left) − 1); t.right ← A; UPDATE(t); return (t, B)
L4  else (A, B) ← SPLIT(t.left, i); t.left ← B; UPDATE(t); return (A, t)

MERGE(a, b)                                ▷ the items of a, then those of b
L5  if a = nil then return b; if b = nil then return a
L6  if a.prio > b.prio then PUSH(a); a.right ← MERGE(a.right, b); UPDATE(a); return a
L7  else PUSH(b); b.left ← MERGE(a, b.left); UPDATE(b); return b

INSERT(i, x)
L8  (A, B) ← SPLIT(root, i); root ← MERGE(MERGE(A, NEW-NODE(x)), B)

DELETE(i)
L9  (A, B) ← SPLIT(root, i); (M, C) ← SPLIT(B, 1); root ← MERGE(A, C); return M.value

REVERSE(lo, hi)
L10 (A, B) ← SPLIT(root, lo); (M, C) ← SPLIT(B, hi − lo)
L11 if M ≠ nil then M.rev ← not M.rev;  root ← MERGE(A, MERGE(M, C))

RANGE-SUM(lo, hi)
L12 (A, B) ← SPLIT(root, lo); (M, C) ← SPLIT(B, hi − lo); s ← total(M); root ← MERGE(A, MERGE(M, C)); return s
```

GET$(i)$ walks down from the root: after PUSH at a node $t$, it goes left if $i < size(t.left)$, returns $t.value$ if $i = size(t.left)$, and otherwise goes right with $i - size(t.left) - 1$. Compared with the treap split by key, line L3 replaces the key test by a size test and subtracts the items it passes; merge is the same as for keyed treaps, plus PUSH and UPDATE.

## Example

Build the list $\langle 10, 20, 30, 40, 50 \rangle$ with the priorities 3, 5, 1, 4, 2. The highest priority, 5, belongs to 20, so 20 is the root, with 10 on its left. On the right, 40 has the highest priority, with 30 and 50 below it. Writing a tree as (left, value, right), it is $(10, 20, (30, 40, 50))$.

Now REVERSE$(1, 4)$, which should give $\langle 10, 40, 30, 20, 50 \rangle$.

1. SPLIT(root, 1) cuts off $A = 10$, and $B = (\text{nil}, 20, (30, 40, 50))$ holds $\langle 20, 30, 40, 50 \rangle$.
2. SPLIT($B$, 3) gives $M = (\text{nil}, 20, (30, 40, \text{nil}))$ for $\langle 20, 30, 40 \rangle$, and $C = 50$.
3. Line L11 sets the flag of $M$'s root 20. Nothing else moves yet.
4. MERGE($M$, $C$): 20 has priority 5 and 50 has 2, so 20 stays on top. PUSH(20) swaps its children: the subtree of 40 goes to the left, with its own flag now set, and the right becomes empty and then receives 50.
5. MERGE($A$, that): 20 again wins over 10. Its new left is MERGE(10, subtree of 40). There 40 (priority 4) beats 10 (priority 3); PUSH(40) swaps the children of 40, so 30 moves to its right, and 10 becomes its left child.

The result is $((10, 40, 30), 20, 50)$, whose in-order sequence is $\langle 10, 40, 30, 20, 50 \rangle$. Then INSERT(2, 25) with priority 6 splits after $\langle 10, 40 \rangle$ and puts the new node above both pieces: $((10, 40, \text{nil}), 25, (30, 20, 50))$. RANGE-SUM(1, 4) is $40 + 25 + 30 = 95$.

## Correctness

Define the sequence a subtree represents, reading it backwards when its flag is set. Toggling a flag reverses that sequence. PUSH keeps the sequence, because the reverse of $s_l \cdot \langle v \rangle \cdot s_r$ is the reverse of $s_r$, then $v$, then the reverse of $s_l$, and that is exactly what swapping the children and toggling their flags gives. After PUSH, the sequence of $t$ is the left part, the value, and the right part, so line L3 is right: when the left part has fewer than $i$ items, all of it and the root go to $A$, together with the first $i - size(t.left) - 1$ items of the right part. MERGE puts the root with the higher priority on top and merges into the side that faces the other tree, which keeps both the order of the items and the heap order. All other operations are splits, one change to the middle piece, and merges. The full proof, by induction on the size, is in the proofs folder.

## Complexity

**Shape.** After all flags are pushed, the tree is the unique tree with the current node sequence as its in-order sequence and the priorities in heap order: the [Cartesian tree](/cartesian-tree/) of the priorities. A pending flag only swaps children, so it changes no depth. The priorities are independent of the operations, so the tree has the shape of a random binary search tree on $n$ items, and the expected depth of each node is at most $2 \ln n + O(1)$, by the analysis of Seidel and Aragon.

**Time.** SPLIT and MERGE follow one or two paths and do $O(1)$ work per node, so they take $O(\log n)$ expected time. Each operation is a constant number of them, so all take $O(\log n)$ expected time, and with high probability $O(\log n)$ as well. The worst case, with very unlucky priorities, is $\Theta(n)$.

**Space.** The tree uses $\Theta(n)$ space, a few words per item. The recursion uses stack space equal to the depth.

## Variants

- **Other lazy updates.** The flag $rev$ is one example of a lazy tag. Adding a constant to a range, or assigning a value to it, works the same way: store the pending change at the root of the middle piece, apply it to $total$ at once, and pass it to the children in PUSH. The tags must compose, and the order of application must be fixed.
- **Ropes.** A [rope](/rope/) stores a string as a balanced tree of pieces with the same split and concatenate operations. An implicit treap with one character per node is a simple rope.
- **Splay trees by position.** A [splay tree](/splay-tree/) keyed by position supports the same operations in $O(\log n)$ amortized time, and is the basis of [link-cut trees](/link-cut-tree/), where whole paths are such sequences.
- **Persistence.** Copying each node before changing it gives a [persistent treap](/persistent-treap/): each version is kept, and a range can be copied into another place in $O(\log n)$ time by sharing.
- **Segment trees.** A [segment tree](/segment-tree/) answers range queries and range updates over a fixed array more simply and faster; it cannot insert or delete in the middle.

## When to use it

Use an implicit treap when a sequence must support insertion and deletion at arbitrary positions together with range work: reversing, moving or copying ranges, and range sums, minima or updates. Typical uses are text editors and string problems, and contest problems on dynamic arrays. If the array never changes length, a [segment tree](/segment-tree/) is simpler and faster. If the bound must hold in the worst case, use a balanced tree by position, such as a [weight-balanced tree](/weight-balanced-tree/) with split and join.

## Pitfalls

- **Forgetting PUSH.** Every place that reads the children of a node, in SPLIT, MERGE, GET and the in-order walk, must push first. A missed push reads the children in the wrong order.
- **UPDATE before PUSH of the children.** UPDATE reads only sizes and totals, which a pending flag does not change, so it does not need the children pushed. A tag that does change the totals, such as "add $c$", must be applied to the node's total when it is set, not when it is pushed.
- **Off-by-one in split.** SPLIT$(t, i)$ puts $i$ items in the first part; the right subtree gets $i - size(t.left) - 1$, which counts the root. Half-open ranges make the calls for $[lo, hi)$ come out as SPLIT$(lo)$ and then SPLIT$(hi - lo)$ on the second part.
- **Priorities that are not random.** Using a fixed or increasing priority turns the tree into a path. Draw them from a good generator, once per node, and do not reuse them when a node moves.
- **Recursion depth.** The recursion depth is the tree depth, about $2 \ln n$ on average, but deeper for unlucky draws; very large lists may need iterative versions or a larger stack.

## Implementations

## History

Seidel and Aragon introduced treaps, with split and join, in 1989 (journal version 1996). Using the subtree size in place of the key, so that a treap stores a sequence, is the same idea that turns any balanced tree with sizes into a list, as in Knuth's balanced trees with a RANK field and in Sleator and Tarjan's use of splay trees for paths. The name "implicit treap", and its use with lazy reversal, comes from the competitive programming community, where it is also called a Cartesian tree by implicit key; it is presented, for example, on cp-algorithms.

## References
