---
tag: J8TN0B
kind: algorithm
slug: treap-merge
name: Treap merge
aliases:
- Merge (treap)
area: data-structures/balanced-trees
level: core
summary: Joins two treaps where all keys of one precede the other into a single treap, following heap priorities, in expected logarithmic time.
uses: [treap]
model: comparison-model
complexity:
  vars: {n: the total number of keys in the two treaps}
  time: {expected: Θ(log n), worst: Θ(n)}
  space: {extra: Θ(log n)}
prereqs: [treap, binary-search-tree, recursion]
see_also: [treap-split, implicit-treap, join-based-tree-algorithms, cartesian-tree, persistent-treap, merge-sort]
sources:
  - paper: doi:10.1007/BF01940876
    title: Raimund Seidel and Cecilia R. Aragon, Randomized search trees, Algorithmica 16(4/5), 1996
    locator: pages 464 to 497 (the operations split and join, and their expected cost)
  - url: https://opendatastructures.org/
    title: Pat Morin, Open Data Structures
    locator: Chapter 7, Section 7.2 Treap (the exercises on split and absorb)
  - url: https://cp-algorithms.com/data_structures/treap.html
    title: cp-algorithms, Treap (Cartesian tree)
    locator: the operations split and merge, and the implicit treap
---

Treap merge joins two [treaps](/treap/) $A$ and $B$, where every key of $A$ is less than every key of $B$, into one treap with all the keys. It compares the priorities of the two roots: the root of higher priority becomes the root of the result, and the merge goes on between its inner subtree and the other treap. So it walks down the right spine of $A$ and the left spine of $B$, and it zips them together in decreasing order of priority. The time is the sum of the lengths of the two spines, which is $O(\log n)$ in expectation over the random priorities. Merge is the inverse of [treap split](/treap-split/), and the two give insertion, deletion and range operations on treaps.

## In plain words

You have two search trees side by side, and every key on the left is smaller than every key on the right. You want one tree. Put them together at the seam: the right edge of the left tree and the left edge of the right tree.

Each node has a random ticket, and the higher ticket must be on top. Compare the two tops. The one with the higher ticket stays the top of the result, and its outer side stays as it is. Its inner side, the part that touches the seam, must be joined with the whole other tree, in the same way. Each step goes one level down one of the two edges, so the work is the length of the two edges.

## The problem

Input: two treaps $A$ and $B$ (binary trees with search order on keys and max-heap order on priorities), such that every key of $A$ is less than every key of $B$. Output: a treap whose keys are the keys of $A$ and $B$. The nodes may be reused, and $A$ and $B$ are no longer valid after the call.

## The algorithm

The procedure is recursive and returns the root of the result.

```pseudo id=main
MERGE(A, B)                                ▷ precondition: every key of A < every key of B
L1  if A = nil then return B
L2  if B = nil then return A
L3  if A.pri > B.pri then
L4      A.right ← MERGE(A.right, B)
L5      return A
L6  B.left ← MERGE(A, B.left)
L7  return B
```

If the root of $A$ has the higher priority, it must be the root of the result. Its left subtree has the smallest keys and stays where it is. Its right subtree and all of $B$ have keys greater than the root, so they are merged into the new right subtree. The other case is the mirror image.

## Example

Merge $A = (((\text{nil}, 10, 20), 30, \text{nil}), 40, 50)$ and $B = ((\text{nil}, 60, 70), 80, \text{nil})$, where the priorities are 10: 20, 20: 10, 30: 60, 40: 80, 50: 30, 60: 50, 70: 40, 80: 70. A tree is written as (left, key, right), and a leaf as its key. These are the two parts that [treap split](/treap-split/) gives at 55.

| call | priorities | winner | next call |
|---|---|---|---|
| MERGE(40, 80) | 80 > 70 | 40 | 40.right ← MERGE(50, 80) |
| MERGE(50, 80) | 30 < 70 | 80 | 80.left ← MERGE(50, 60) |
| MERGE(50, 60) | 30 < 50 | 60 | 60.left ← MERGE(50, nil) |
| MERGE(50, nil) | | 50 | returns 50 |

The result is $(((\text{nil}, 10, 20), 30, \text{nil}), 40, ((50, 60, 70), 80, \text{nil}))$, the treap from before the split. The calls walk the right spine 40, 50 of $A$ and the left spine 80, 60 of $B$, and they put the four nodes on one path in the order of their priorities: 40 (80), 80 (70), 60 (50), 50 (30).

## Correctness

The proof is by induction on the total size. If one treap is empty, the other is the answer. If $A.pri > B.pri$, the root of $A$ has the highest priority of all nodes, since it is above every other node of $A$ and above $B$'s root, which is above all of $B$. So it must be the root. By induction, line L4 makes a treap of $A.right$ and $B$; its keys are greater than $A.key$, and its priorities are at most $A.pri$, so $A$ with this right subtree is a treap. The other case is the mirror image. The full proof is in the proofs folder.

## Complexity

Each call does $O(1)$ work and moves one step down the right spine of $A$ or the left spine of $B$. So the time is at most the sum of the two spine lengths plus one. In a treap with random priorities and $m$ keys, the right spine is the set of keys that have a higher priority than all keys to their right, and the $j$-th largest key is on it with probability $1/j$; so its expected length is $H_m \le 1 + \ln m$. Hence a merge of treaps of sizes $m_1$ and $m_2$ takes $H_{m_1} + H_{m_2} = O(\log n)$ expected time. When $A$ and $B$ come from a split of a random treap, the spines are parts of the search path of the split key, and the same bound holds. The worst case is $\Theta(n)$.

The extra space is the recursion stack, as deep as the result path. A loop version that keeps the last attached node needs $O(1)$ extra space.

## Properties

- It compares only priorities, never keys. The precondition on the keys is what makes the result a search tree.
- It does no rotation and keeps every priority, so the result is the unique treap of the union.
- It is *destructive*: it reuses the nodes. A persistent version copies each node on the two spines.

## Variants and improvements

- **Insertion and deletion.** To delete the key at a node $x$, replace $x$ by MERGE$(x.left, x.right)$. This is the same as rotating $x$ down to a leaf. To insert $k$, split at $k$ and merge the three parts.
- **Merge with sizes.** If nodes store subtree sizes or other summaries, each node whose child changes at line L4 or L6 recomputes its summary. This gives the [implicit treap](/implicit-treap/), where merge concatenates two sequences.
- **Union.** When the key ranges overlap, the union of two treaps is a different algorithm: split one treap at the root key of the other and recurse on both sides. See [join-based tree algorithms](/join-based-tree-algorithms/).
- **Join with a middle key.** Join of $A$, a key $k$ and $B$ is the basic operation of join-based algorithms for any balanced tree. For treaps it is MERGE$(A$, MERGE$(\{k\}, B))$.

## When to use it

Use merge to concatenate two ordered sets whose key ranges do not overlap, or two sequences stored in implicit treaps. With split, it gives short code for insertion, deletion, cutting and pasting ranges, and moving a block from one place to another.

## Pitfalls

- **Overlapping key ranges.** MERGE does not check its precondition. If a key of $A$ is greater than a key of $B$, the result is not a search tree, and later searches fail. A test of the implementation merges $\{1, 5\}$ with $\{3\}$ and finds the order broken.
- **The argument order in line L6.** The recursive call is MERGE$(A, B.left)$, with $A$ first. Swapping the arguments breaks the order.
- **Forgetting to update the summary.** In an augmented treap, a node whose child changed must recompute its summary before it returns.

## Implementations

## History

Seidel and Aragon described join (merge) and split for treaps in their work of 1989, and analyzed them in the 1996 journal version. The same zip of two spines by priority appears in the merge of leftist heaps and of skew heaps, where the order on keys is not needed.

## References
