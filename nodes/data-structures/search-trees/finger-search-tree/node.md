---
tag: X7SV6M
kind: data-structure
slug: finger-search-tree
name: Finger search tree
aliases:
- finger tree
area: data-structures/search-trees
level: advanced
summary: Search tree where a search from a stored finger costs time logarithmic in the distance to the target.
implements: [ordered-set]
model: pointer-machine
complexity:
  vars: {n: the number of keys, d: the number of keys between the finger and the target}
  time: {worst: O(log d), amortized: O(1)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [two-three-four-tree, b-plus-tree, exponential-search]
see_also: [finger-tree, splay-tree, skip-list, treap, adaptive-sorting, blink-tree, working-set-theorem, ordered-set]
sources:
  - paper: doi:10.1145/800105.803395
    title: Leo J. Guibas, Edward M. McCreight, Michael F. Plass and Janet R. Roberts, A new representation for linear lists, Proceedings of the 9th ACM Symposium on Theory of Computing, 1977
    locator: pages 49 to 60
  - paper: doi:10.1007/BF00288968
    title: Scott Huddleston and Kurt Mehlhorn, A new data structure for representing sorted lists, Acta Informatica 17(2), 1982
    locator: pages 157 to 184
---

A finger search tree is a balanced search tree in which a search can start at a *finger*, a pointer to a node near the target, instead of at the root. The search costs $O(\log d)$ time, where $d$ is the number of keys between the finger and the target, rather than $O(\log n)$. Guibas, McCreight, Plass and Roberts introduced the idea in 1977, and Huddleston and Mehlhorn (1982) gave the level-linked (2,4)-tree, in which a finger search takes $O(\log d)$ time and an insert or delete at a finger takes $O(1)$ amortized time. The structure is the tree form of [exponential search](/exponential-search/).

## In plain words

Looking up a word in a dictionary always from the first page is wasteful when you already have your finger on a page near the word. A finger search tree lets a search start where your finger is.

From the finger, the search walks up the tree only as high as it must to see past the target, and then walks down to it. Each level up covers about twice as many keys as the level below. So if the target is ten keys away, the search goes up about three or four levels, not to the top of the tree. Keys close to the finger are cheap to find, whatever the size of the whole tree.

## The abstract type

A finger search tree implements the [ordered set](/ordered-set/) operations, with an extra argument: a finger $f$, a handle to a position in the set. FINGER-SEARCH$(f, k)$ returns a finger at the position of $k$ (the node of $k$ or of the gap where $k$ would go) and whether $k$ is present. INSERT$(k, f)$ and DELETE$(k, f)$ do the update near the finger and return a new finger. Searches from the root are the special case of a finger at the root.

## Representation

This page uses a level-linked (2,4)-tree with keys in the bottom nodes, in the style of a [B+ tree](/b-plus-tree/).

- **Bottom nodes** hold 1 to 3 keys in increasing order. All bottom nodes are at the same depth.
- **Internal nodes** have 2 to 4 children $c_0, \ldots, c_{m-1}$ and $m - 1$ separators $s_1 < \cdots < s_{m-1}$. The root may be a bottom node with 0 to 3 keys.
- **Ranges.** Each node $v$ stores its key range $(v.lo, v.hi]$, with $-\infty$ and $+\infty$ for the root. Child $c_j$ of $v$ has range $(s_j, s_{j+1}]$, with $s_0 = v.lo$ and $s_m = v.hi$. Each key of a bottom node lies in its range.
- **Level links.** All nodes of one level form a doubly linked list in key order, by $prev$ and $next$. Each node also has a $parent$ pointer.

A finger is a pointer to a bottom node. The ranges of the nodes on one level partition the keys, so each key $k$ has exactly one bottom node whose range holds it.

The separators do not need to be keys of the set. A delete does not change them, because a separator that is larger than or equal to each key on its left and smaller than each key on its right stays so when keys leave. So the ranges change only at the nodes that split, merge or share keys.

## Operations

```pseudo id=main
FINGER-SEARCH(f, k)                       ▷ f is a bottom node
L1  v ← f
L2  while not (v.lo < k ≤ v.hi) do
L3      if k > v.hi then w ← v.next else w ← v.prev   ▷ the neighbour on the side of k
L4      if w ≠ NIL and w.lo < k ≤ w.hi then v ← w; break
L5      v ← v.parent
L6  return DESCEND(v, k)

DESCEND(v, k)
L7  while v is not a bottom node do
L8      j ← the least index with k ≤ s_{j+1} (the last child if none)
L9      v ← c_j
L10 return v                              ▷ the bottom node whose range holds k

INSERT(k, f)
L11 b ← FINGER-SEARCH(f, k); if k is in b then return b
L12 put k into b in sorted order
L13 v ← b
L14 while v has 4 keys (bottom) or 5 children (internal) do
L15     split v into v and a new right node u with separator s; u.lo ← s, u.hi ← old v.hi, v.hi ← s; link u after v on its level
L16     if v is the root then make a new root with children v, u and separator s; break
L17     insert u just after v in v.parent, with separator s between them
L18     v ← v.parent
L19 return the bottom node that holds k
```

**Finger search.** Lines L1 to L5 climb from the finger. At each level the search tests the current node and its neighbour on the side of $k$; if one of them has $k$ in its range, the search stops climbing. Else it goes to the parent. The root has range $(-\infty, +\infty]$, so the climb ends. Lines L7 to L10 then go down to the bottom node whose range holds $k$, by the separators.

**Insert.** A split of a bottom node with keys $a < b < c < d$ gives $(a, b)$ and $(c, d)$ with separator $s = b$. A split of an internal node with 5 children gives a node of 3 children and a node of 2 children, and moves the middle separator up. The ranges of the children do not change, only those of $v$ and $u$.

**Delete.** Find the bottom node $b$ of $k$ from the finger and remove $k$. If a non-root node $v$ falls below its minimum (0 keys at the bottom, 1 child above), look at an adjacent sibling. If the sibling has more than the minimum, *share*: move one key or child across and replace the separator between them in the parent; only the ranges of $v$ and the sibling change. Else *merge* $v$ into the sibling, remove the separator from the parent (for internal nodes it moves down into the merged node), unlink $v$ from its level, and repeat at the parent. If the root is left with one child, that child becomes the root.

## Example

Insert 10, 20, ..., 90 in increasing order, each time from the finger returned by the previous insert. The bottom node $(10, 20, 30, 40)$ splits at 20, then $(30, 40, 50, 60)$ splits at 40, then $(50, 60, 70, 80)$ splits at 60. The result:

| node | keys or separators | range |
|---|---|---|
| root | 20, 40, 60 | $(-\infty, +\infty]$ |
| bottom 1 | 10, 20 | $(-\infty, 20]$ |
| bottom 2 | 30, 40 | $(20, 40]$ |
| bottom 3 | 50, 60 | $(40, 60]$ |
| bottom 4 | 70, 80, 90 | $(60, +\infty]$ |

**Finger search from bottom 1 for 35.** The range of bottom 1 does not hold 35, but its right neighbour, bottom 2, has range $(20, 40]$: the search stops there without climbing, and 35 is absent. **For 75.** Neither bottom 1 nor bottom 2 holds 75, so the search climbs one level to the root and goes down past the separator 60 to bottom 4. The keys strictly between the finger and 75 are 30, 40, 50, 60 and 70, so $d = 5$, and the climb of 1 level is within $\lg d + 1$.

**Delete 30, then 40.** After the second delete, bottom 2 is empty. Its left sibling has 2 keys, so it shares: 20 moves into bottom 2, and the separator becomes 10. Bottom 1 is now $(10)$ with range $(-\infty, 10]$, and bottom 2 is $(20)$ with range $(10, 40]$. **Delete 10.** Bottom 1 is empty, and its sibling has only one key, so the two merge into $(20)$ with range $(-\infty, 40]$, and the root keeps the separators 40 and 60.

## Correctness

The invariant is the shape (bottom nodes at one depth, the sizes above), the ranges (each child's range is the interval between its separators, and each key lies in the range of its bottom node), and the level lists (each level linked in key order). The climb of lines L1 to L5 stops at a node whose range holds $k$, and DESCEND keeps the invariant that the range of $v$ holds $k$, so it ends at the bottom node of $k$. Splits, shares and merges keep the ranges because they move whole subtrees and separators together, and the separator values they create or move lie between the keys on their two sides. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Height.** Each internal node has at least 2 children and each non-root bottom node at least 1 key, so a node at height $i$ has at least $2^i$ keys below it, and the height is at most $\lg n + 1$.

**Finger search.** Suppose the climb leaves level $i$ for level $i + 1$ at node $v$, with $k > v.hi$. Then the neighbour $w = v.next$ does not hold $k$, so $k > w.hi$, and all keys below $w$ lie strictly between $v.hi$ and $k$. There are at least $2^i$ of them. The finger lies below $v$, so these keys also lie between the finger and $k$, and $d \ge 2^i$. So a climb to level $i$ needs $d \ge 2^{i-1}$, and the climb stops at a level $\le \lg d + 1$. The descent has the same number of levels, and each level costs $O(1)$ since a node has at most 4 children. So FINGER-SEARCH costs $O(\log d + 1)$ in the worst case.

**Updates.** After the finger search, an insert or delete does a sequence of splits, or of merges and at most one share, each in $O(1)$ time. Huddleston and Mehlhorn show that in a (2,4)-tree, any sequence of $m$ inserts and deletes at known positions does $O(m)$ splits, merges and shares in total, by a potential that charges the nodes that are close to a split or a merge. The [complexity proof](proofs/complexity.md) gives such a potential for this tree. So an insert or delete at a finger costs $O(\log d)$ for the search plus $O(1)$ amortized.

| operation | cost |
|---|---|
| finger search | $O(\log d + 1)$ worst |
| search from the root | $O(\log n)$ worst |
| insert or delete at a finger | $O(\log d + 1)$ worst for the search, plus $O(1)$ amortized |
| space | $\Theta(n)$ |

**Consequences.** Inserting $n$ keys in sorted order, each from the previous finger, costs $O(n)$ in total. Merging two sorted lists of sizes $m \le n$ costs $O(m \log(n/m + 1))$ by inserting the shorter one from left to right, each from the previous finger, since the distances add up to at most $n + m$ and $\lg$ is concave. [Adaptive sorting](/adaptive-sorting/) by insertion with fingers costs $O(n + n \log(1 + I/n))$ for $I$ inversions.

## Variants

- **Guibas, McCreight, Plass and Roberts (1977).** The first finger structure, a B-tree variant with a fixed set of fingers, and $O(\log d)$ search and update.
- **Brown and Tarjan; Huddleston and Mehlhorn.** Level-linked 2-3 and (2,4)-trees with any number of fingers. Huddleston and Mehlhorn give the $O(1)$ amortized bound for updates.
- **Worst-case constant updates.** Later structures give $O(1)$ worst-case insert and delete at a finger, at the cost of much more complex rebalancing.
- **Randomized.** [Treaps](/treap/) and [skip lists](/skip-list/) support finger searches in $O(\log d)$ expected time, with simpler code.
- **Self-adjusting.** A [splay tree](/splay-tree/) has no explicit fingers, but by the dynamic finger theorem an access costs $O(\log(d + 1))$ amortized, where $d$ is the distance to the previous access, so the last accessed key acts as a finger.
- **Finger trees for sequences.** The functional [finger tree](/finger-tree/) of Hinze and Paterson keeps fingers at the two ends of a sequence; it is a [persistent](/persistent-data-structure/) relative of the same idea.

## When to use it

Use a finger search tree when accesses have spatial locality, that is, when each access is near a recent one: merging sorted lists, sorting nearly sorted data, sweeping through keys in order with updates, or keeping a sorted list where most changes happen near a cursor. If accesses are spread at random, the plain $O(\log n)$ search of a [B+ tree](/b-plus-tree/) or a red-black tree is simpler and as fast.

## Pitfalls

- **Climbing by parent pointers alone.** Without the level links, the climb must go up to the lowest common ancestor of the finger and the target, which can be the root even when $d = 1$, for example when the finger is the largest key of the left half and the target is the smallest key of the right half. The test of the neighbour in lines L3 and L4 is what bounds the climb by $\lg d + 1$.
- **Stale fingers.** A merge removes a node. A finger to that node is no longer valid. The operations return a new finger, and old ones must not be reused after a delete.
- **Ranges after a share.** A share moves a key or a subtree across, and the separator in the parent and the ranges of both nodes must change together. Changing only the separator breaks the climb test of line L2.
- **Using exact maxima as separators.** If each separator must equal the largest key on its left, a delete of that key changes separators up to the root, which costs $\Theta(\log n)$. Separators that are only bounds avoid this.

## Implementations

The Python class follows the main block. Nodes store their ranges, with `None` for the infinite ends, so the climb test of line L2 is a pair of comparisons. `finger_search` records how many levels it climbed, and the tests check this against $\lg d + 1$ on random fingers and targets, and check all operations against a sorted list.

## History

Guibas, McCreight, Plass and Roberts introduced finger search in 1977, in a representation of linear lists by B-trees with fingers. Brown and Tarjan used level-linked 2-3 trees for fast merging, and Huddleston and Mehlhorn (1982) gave the level-linked (2,4)-tree with $O(\log d)$ finger search and $O(1)$ amortized updates, with the potential argument for (a,b)-trees with $b \ge 2a$.

## References
