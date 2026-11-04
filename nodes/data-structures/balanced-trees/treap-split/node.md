---
tag: WYJ3AW
kind: algorithm
slug: treap-split
name: Treap split
aliases:
- Split (treap)
area: data-structures/balanced-trees
level: core
summary: Splits a treap by key or position into two treaps, one holding smaller elements and one holding the rest, in expected logarithmic time.
uses: [treap]
model: comparison-model
complexity:
  vars: {n: the number of keys in the treap}
  time: {expected: Θ(log n), worst: Θ(n)}
  space: {extra: Θ(log n)}
prereqs: [treap, binary-search-tree, recursion]
see_also: [treap-merge, implicit-treap, join-based-tree-algorithms, cartesian-tree, persistent-treap, random-bst-expected-depth]
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

Treap split cuts a [treap](/treap/) at a key $k$ into two treaps: one with the keys less than $k$, and one with the keys at least $k$. It walks down the search path of $k$ once and moves each node on that path to the left or the right result, with one pointer change for each node. The two results are treaps with the old priorities, and no rotation is needed. The time is the length of the search path, which is $O(\log n)$ in expectation over the random priorities. Together with [treap merge](/treap-merge/), split gives insertion, deletion, range queries and set operations in a few lines each.

## In plain words

Think of the treap as a search tree. Draw a vertical line at the place where $k$ would go. Every node is on one side of the line: its key is less than $k$, or it is not. The nodes to the left must form one tree and the nodes to the right another.

Start at the top. If the top key is less than $k$, the top node and everything on its left belong to the left tree. Only its right side has nodes of both kinds, so cut that side in the same way, and hang the left piece back in place of the old right side. If the top key is not less than $k$, do the mirror image. Each step goes one level down, so the work is the depth of the place of $k$.

## The problem

Input: a treap $t$, which is a binary tree with search order on the keys and max-heap order on the priorities, and a key $k$. Output: two treaps $L$ and $R$ such that the keys of $L$ are the keys of $t$ less than $k$, and the keys of $R$ are the keys of $t$ that are at least $k$. The nodes of $t$ may be reused, and $t$ is no longer valid after the call.

## The algorithm

The procedure is recursive and returns the pair $(L, R)$.

```pseudo id=main
SPLIT(t, k)                                ▷ returns (L, R), with keys < k in L and keys ≥ k in R
L1  if t = nil then return (nil, nil)
L2  if t.key < k then
L3      (A, B) ← SPLIT(t.right, k)
L4      t.right ← A
L5      return (t, B)
L6  else
L7      (A, B) ← SPLIT(t.left, k)
L8      t.left ← B
L9      return (A, t)
```

When $t.key < k$, the root and its left subtree have keys less than $k$, so they go to $L$, and only the right subtree must be cut; line L4 keeps the part of it below $k$ as the new right subtree. The other case is the mirror image.

## Example

Take the treap with the keys 10 to 80 and the priorities 10: 20, 20: 10, 30: 60, 40: 80, 50: 30, 60: 50, 70: 40, 80: 70. A tree is written as (left, key, right), and a leaf as its key:

$$t = (((\text{nil}, 10, 20), 30, \text{nil}), 40, ((50, 60, 70), 80, \text{nil})).$$

Split it at $k = 55$.

| call | test | goes to | link set on the way back |
|---|---|---|---|
| SPLIT(40) | 40 < 55 | 40 to $L$, recurse right | 40.right ← (part of the subtree of 80 below 55) = 50 |
| SPLIT(80) | 80 ≥ 55 | 80 to $R$, recurse left | 80.left ← (part of the subtree of 60 at least 55) = (nil, 60, 70) |
| SPLIT(60) | 60 ≥ 55 | 60 to $R$, recurse left | 60.left ← (part of 50 at least 55) = nil |
| SPLIT(50) | 50 < 55 | 50 to $L$, recurse right | 50.right ← nil |
| SPLIT(nil) | | | returns (nil, nil) |

The results are $L = (((\text{nil}, 10, 20), 30, \text{nil}), 40, 50)$ and $R = ((\text{nil}, 60, 70), 80, \text{nil})$. The calls visit the search path 40, 80, 60, 50 of the key 55, and they change four pointers. Merging $L$ and $R$ with [treap merge](/treap-merge/) gives $t$ back.

## Correctness

The proof is by induction on the size of $t$. If $t.key < k$, every key in $t.left$ is less than $t.key < k$, so the root and its left subtree belong in $L$. By induction, line L3 cuts $t.right$ into a treap $A$ with its keys less than $k$ and a treap $B$ with its keys at least $k$. Line L4 hangs $A$ as the right subtree of $t$: all keys of $A$ are greater than $t.key$, because they came from $t.right$, so the search order holds; and every priority in $A$ is at most $t.pri$, because $A$ is made of nodes that were below $t$, so the heap order holds. So $(t, B)$ is the right answer. The other case is the mirror image. The full proof is in the proofs folder.

## Complexity

Each call does $O(1)$ work and recurses on a child, so the time is proportional to the number of nodes on the search path of $k$, at most the height plus one. In a treap with random priorities, the expected number of nodes on the search path of any key, present or not, is $O(\log n)$: as for the depth of a node, a key $x_i$ is on the path to the gap of $k$ exactly when its priority is the highest among the keys between $x_i$ and $k$, and the sum of these probabilities is at most $2 H_n$, where $H_n$ is the $n$-th harmonic number. The worst case is $\Theta(n)$, when the treap is a path.

The extra space is the recursion stack, as deep as the path. A loop version that keeps the last node of each result needs $O(1)$ extra space.

## Properties

- It uses one comparison for each node on the path.
- It does no rotation and keeps every priority, so the results are the treaps of their key sets.
- It is *destructive*: it reuses the nodes. A persistent version copies each node on the path instead; see [persistent treap](/persistent-treap/).

## Variants and improvements

- **Split by position.** If each node stores the size of its subtree, SPLIT can cut after the first $i$ keys instead of at a key: go left when $i \le$ size of $t.left$, and else go right with $i$ minus that size minus one. This is the main step of the [implicit treap](/implicit-treap/).
- **Three-way split.** A split that also returns the node with key equal to $k$, if any, gives membership and deletion in one pass.
- **Insertion and deletion by split and merge.** To insert $k$ with priority $p$: split at $k$, then merge $L$, the new node and $R$. To delete $k$: split at $k$ and at the successor of $k$ and merge the outer parts. A faster insertion goes down to the first node of lower priority than $p$, splits its subtree at $k$, and hangs the two parts below the new node.
- **Split for other trees.** The same idea works for any balanced tree that has a join operation; see [join-based tree algorithms](/join-based-tree-algorithms/).

## When to use it

Use split when you need to cut an ordered set at a key: range queries and range updates, moving a block of keys to another set, or the set operations union, intersection and difference. With merge it is the simplest way to build these operations on a balanced tree.

## Pitfalls

- **The side of an equal key.** Line L2 tests $t.key < k$. A key equal to $k$ goes to $R$. Code that tests $\le$ in one place and $<$ in another loses the key or puts it in both. A test of the implementation checks that 40 goes to $R$ when the split is at 40.
- **Using $t$ after the split.** The nodes are reused. The old root is now the root of $L$ or of $R$, and the old tree no longer exists.
- **Forgetting to update the summary.** If nodes store subtree sizes or sums, each node whose child changed at line L4 or L8 must recompute them before it returns.

## Implementations

## History

Seidel and Aragon described split and join for treaps when they introduced the structure, in 1989, and gave their expected cost in the 1996 journal version. The pair of operations became the standard way to write treaps in programming contests, where the implicit form keyed by position is also common.

## References
