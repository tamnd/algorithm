---
tag: XM4DVE
kind: data-structure
slug: persistent-treap
name: Persistent treap
aliases:
- persistent randomized BST
area: data-structures/persistent-structures
level: advanced
summary: A treap updated by path copying, whose expected O(log n) depth holds for each version.
implements: [ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys in the version, N: the number of nodes made by all updates}
  time: {contains: Θ(log n) expected, insert: Θ(log n) expected, delete: Θ(log n) expected, split: Θ(log n) expected, merge: Θ(log n) expected, kth: Θ(log n) expected}
  space: {total: Θ(N)}
history:
  year: 1989
  people: [Raimund Seidel, Cecilia R. Aragon]
  note: Seidel and Aragon introduced treaps; since each update of a treap touches O(log n) expected nodes, path copying makes them persistent at that cost.
prereqs: [treap, path-copying, persistent-binary-search-tree]
see_also: [treap-split, treap-merge, implicit-treap, persistent-red-black-tree, persistent-dynamic-set, join-based-tree-algorithms, rope, random-binary-search-tree]
sources:
  - paper: doi:10.1007/BF01940876
    title: Raimund Seidel and Cecilia R. Aragon, Randomized search trees, Algorithmica 16(4/5), 1996
    locator: the expected depth of a node, and the split and join operations
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: the path copying method for linked data structures
  - url: https://cp-algorithms.com/data_structures/treap.html
    title: cp-algorithms, Treap (Cartesian tree)
    locator: the split and merge operations, insertion and deletion by them, and implicit treaps
---

A persistent treap is a [treap](/treap/) in which no node is changed after it is made: [split](/treap-split/), [merge](/treap-merge/), insert and delete copy each node they would change and share all others, by [path copying](/path-copying/). Each version is a treap of its own keys, so the expected depth of each node is less than $2 \ln n$, and each operation takes $O(\log n)$ expected time and makes $O(\log n)$ expected new nodes. Because the balance comes from random priorities and not from colors or heights, the code is short, and split and merge make the structure good for persistent sequences and [ropes](/rope/) as well as for [persistent sets](/persistent-dynamic-set/).

## In plain words

A treap is a search tree where each key also has a random ticket, and higher tickets sit higher in the tree. The random tickets keep the tree short on average, whatever the order of the keys.

To make it persistent, never change a node. When an operation would change a node, make a new copy instead, with the new links, and let the copy point to the old nodes for the parts that stay the same. Only the nodes on a short path are copied, and the rest of the tree is shared by the old and new versions.

Each version is a treap in its own right, so each version is short on average too.

## The abstract type

The structure implements an immutable [ordered set](/ordered-set/) of keys from a total order. Each update returns a new set and leaves its argument as it was:

- `contains(S, k)`, `min(S)`, `max(S)`, `kth(S, i)` (the key of rank $i$, from 0), `size(S)`;
- `insert(S, k)` and `delete(S, k)`;
- `split(S, k)`, which returns the set of keys less than $k$ and the set of keys at least $k$;
- `merge(A, B)`, for sets with every key of $A$ less than every key of $B$, which returns $A \cup B$.

Every version stays valid and can be the input of any operation, so the structure is fully persistent. Merge takes two versions, so it is also confluently persistent in the sense of the [version tree](/version-tree/).

## Representation

A node has a key, a priority, two child pointers and the size of its subtree. A set is a pointer to its root, or nil for the empty set. The priority of a node is drawn at random when the key is inserted, and it is copied with the node.

**Invariant.** (I1) The keys are in search-tree order. (I2) The priorities are in heap order: no node has a higher priority than its parent. (I3) Each size field is one plus the sizes of the two children. (I4) No field of a node changes after the node is made.

By (I1) and (I2), the tree of a set is the [Cartesian tree](/cartesian-tree/) of its (key, priority) pairs, and it is unique if the priorities are distinct.

## Operations

```pseudo id=main
SPLIT(t, k)                                 ▷ (keys < k, keys ≥ k), as two treaps
L1  if t = nil then return (nil, nil)
L2  if t.key < k then (a, b) ← SPLIT(t.right, k); return (COPY(t, right ← a), b)
L3  (a, b) ← SPLIT(t.left, k); return (a, COPY(t, left ← b))

MERGE(a, b)                                 ▷ each key of a is below each key of b
L4  if a = nil then return b
L5  if b = nil then return a
L6  if a.prio > b.prio then return COPY(a, right ← MERGE(a.right, b))
L7  return COPY(b, left ← MERGE(a, b.left))

INSERT(t, k)
L8  if CONTAINS(t, k) then return t
L9  return INS(t, k, a random priority)

INS(t, k, p)
L10 if t = nil or p > t.prio then (a, b) ← SPLIT(t, k); return NEW-NODE(k, p, a, b)
L11 if k < t.key then return COPY(t, left ← INS(t.left, k, p))
L12 return COPY(t, right ← INS(t.right, k, p))

DELETE(t, k)
L13 if not CONTAINS(t, k) then return t
L14 return DEL(t, k)

DEL(t, k)
L15 if k < t.key then return COPY(t, left ← DEL(t.left, k))
L16 if k > t.key then return COPY(t, right ← DEL(t.right, k))
L17 return MERGE(t.left, t.right)

CONTAINS(t, k)
L18 while t ≠ nil do
L19     if k = t.key then return true
L20     if k < t.key then t ← t.left else t ← t.right
L21 return false
```

COPY$(t, f \gets x)$ makes a new node with the fields of $t$, except that field $f$ is $x$, and with the size computed from its children. It is the only way the procedures make a node other than the new leaf, so (I4) holds. The guards in lines L8 and L13 make an insertion of a present key or a deletion of a missing key return the same version with no copies. `kth` walks down by the size fields, and `min` and `max` follow the left or right spine.

INS goes down the search path of $k$ while the priorities of the nodes are higher than $p$ (L11, L12), and at the first node with a lower priority it splits that subtree at $k$ and puts the new node on top (L10). This makes exactly the tree that the definition requires, and it copies only the nodes on the search path down to that point and the nodes on the split path below it.

## Example

Insert the keys 20, 30, 40, 50, 60, 70 and 80 with the priorities 0.3, 0.6, 0.5, 0.9, 0.7, 0.8 and 0.4. Since 50 has the highest priority it is the root, 30 and 70 are the roots of its two sides, and the tree $v_0$ is perfectly balanced:

- $v_0$: root 50; left child 30 with children 20 and 40; right child 70 with children 60 and 80.

**Insert 65 with priority 0.75** into $v_0$. INS passes 50 (priority 0.9, go right) and 70 (priority 0.8, go left), and reaches 60, whose priority 0.7 is lower than 0.75. So line L10 splits the subtree of 60 at 65 into (60, nil), which copies 60, and makes the node 65 with left child 60. Then 70 and 50 are copied with the new child. The new version $v_1$ is

- $v_1$: root 50; left child 30 (shared, with 20 and 40); right child 70 with children 65 and 80, and 65 has the left child 60.

The update made 4 new nodes (50, 70, 65 and a copy of 60) and shares the nodes 30, 20, 40 and 80 with $v_0$. The two versions use 11 nodes in total.

**Delete 50** from $v_1$. The root holds 50, so line L17 merges its subtrees, rooted at 30 (priority 0.6) and 70 (priority 0.8). Line L7 keeps 70 on top and merges 30 into its left side; then 65 (0.75) beats 30, then 60 (0.7) beats 30, and 60 has no left child, so 30 with its whole subtree becomes the left child of a copy of 60. The new version $v_2$ is

- $v_2$: root 70; left child 65; 65 has the left child 60; 60 has the left child 30, with 20 and 40; the right child of 70 is 80.

The deletion made 3 nodes (copies of 70, 65 and 60), and all three versions are still valid: $v_0$ has 7 keys, $v_1$ has 8 and $v_2$ has 7.

**Split.** SPLIT$(v_1, 45)$ returns $\{20, 30, 40\}$ and $\{50, 60, 65, 70, 80\}$. It copies the three nodes on the search path of 45, which are 50, 30 and 40; the copy of 50 gets a nil left child, while the copies of 30 and 40 have the same children as before. A test that returns $t$ itself when no child changed would avoid those two copies. MERGE of the two gives back the key set of $v_1$.

## Correctness

The procedures are those of the ephemeral treap, except that each write to a field of a node $t$ becomes a new node COPY$(t, \ldots)$ that takes the place of $t$ in the result. So the result of each operation is the treap that the ephemeral operation would make, and (I1) to (I3) hold for it by the correctness of the ephemeral split, merge, insert and delete. Since no node is changed, the tree reachable from each old root is the same as before, and so is its set (I4). For the expected bounds, fix a version; its shape is the Cartesian tree of its keys and their priorities, and those priorities are independent and uniform, as long as the sequence of operations does not depend on the priorities. So each version is a random treap, and the depth bound of Seidel and Aragon holds for it. The full proof is in the proofs folder.

## Complexity

| operation | time | new nodes |
|---|---|---|
| contains, min, max, kth | $O(\log n)$ expected | none |
| insert, delete | $O(\log n)$ expected | $O(\log n)$ expected |
| split | $O(\log n)$ expected | one per node on the split path |
| merge of sets of sizes $n_1$ and $n_2$ | $O(\log(n_1 + n_2))$ expected | one per node on the two spines visited |

**Time.** SPLIT visits one node per level along the search path of $k$, MERGE visits the right spine of $a$ and the left spine of $b$ down to the meeting point, INS visits a search path and then a split path below it, and DEL visits a search path and then a merge below it. In a treap of $n$ keys with random priorities, each such path has expected length $O(\log n)$: the expected depth of each node is $H_i + H_{n - i + 1} - 1 < 2 \ln n + 1$ for the node of rank $i$, where $H_i$ is the $i$-th harmonic number, and the spines and split paths are made of nodes that lie on such search paths.

**Space.** Each operation makes at most one new node per node that it visits, so $O(\log n)$ expected nodes per update, and the total space is $\Theta(N)$ for $N$ nodes made by all updates. A garbage collector frees nodes that no live version reaches.

**Expected, not worst case.** The bounds are averages over the random priorities, for every fixed sequence of operations. A version can be deep with small probability. If the operations depend on the shape of the tree, for example if an adversary sees the priorities, the bounds no longer hold.

## Variants

- **Implicit persistent treap.** Drop the keys and order the nodes by position, using the size fields, as in the [implicit treap](/implicit-treap/). Split by position and merge then give a persistent sequence with $O(\log n)$ expected concatenation, cut and index, a persistent [rope](/rope/).
- **Merge by size.** When a sequence is merged with a copy of itself, the two sides share nodes and priorities, and the priorities are no longer independent. A common fix is to choose the root in MERGE at random with probability $|a| / (|a| + |b|)$ for the root of $a$, instead of comparing stored priorities; this is the rule of the randomized binary search trees of Martínez and Roura, and keeps the shape random.
- **Set operations.** Union, intersection and difference of two sets by recursive split and merge take $O(m \log(n/m + 1))$ expected time for sizes $m \le n$, and the persistent form shares all untouched subtrees; see [join-based tree algorithms](/join-based-tree-algorithms/).
- **Deterministic alternative.** The [persistent red-black tree](/persistent-red-black-tree/) has worst-case $O(\log n)$ bounds, at the cost of more cases in the code.
- **Hash priorities.** Use a hash of the key as the priority. Then the tree of a set does not depend on its history, and two versions with the same keys have the same shape, which allows comparison of subtrees by pointer when combined with [hash-consing](/hash-consing/).

## When to use it

Use a persistent treap when a program needs many versions of an ordered set or a sequence, and wants split and merge as well as insert and delete: undo in an editor built on a rope, backtracking search over sets, or functional code that needs a balanced tree in a few lines. Expected bounds are enough for most such uses. When the input may be chosen by someone who can see the priorities, or when worst-case bounds are required, use a persistent red-black tree instead.

## Pitfalls

- **Writing a field in place.** Every change must make a new node, including a change of the size field after a split or a merge. One in-place write of $t.left$ changes all versions that share $t$.
- **Copies of the same node in one tree.** In the implicit form, merging a version with itself puts two equal priorities on one path, and repeated doubling makes the tree degenerate. Use merge by size, or fresh priorities, for this case.
- **A new random source per version.** All versions should draw priorities from one stream, or from a hash of the key, not from a generator that restarts for each version, which would give equal priorities to many keys.
- **Recursion depth.** The recursion of SPLIT, MERGE, INS and DEL is as deep as the tree, which is $O(\log n)$ expected; it is safe, but an unbalanced tree built with bad priorities can still overflow the stack.
- **Merge of overlapping sets.** MERGE requires every key of $a$ to be below every key of $b$. The implementation checks the maximum of $a$ against the minimum of $b$; skipping the check gives a tree that breaks (I1) without any error.

## Implementations

## History

Raimund Seidel and Cecilia Aragon introduced treaps in 1989, with the journal version in Algorithmica in 1996. Since each update touches $O(\log n)$ expected nodes, path copying turns a treap into a persistent set at that cost. Path copying itself was studied as a general method by Driscoll, Sarnak, Sleator and Tarjan in 1989. Persistent treaps with split and merge, and their implicit form for sequences, later became a standard tool in functional programming and in programming contests.

## References
