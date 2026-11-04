---
tag: 82JNAM
kind: algorithm
slug: bst-insertion
name: Binary search tree insertion
aliases:
- BST insert
area: data-structures/search-trees
level: intro
summary: Walk down to a missing child position and attach the new key as a leaf.
model: comparison-model
complexity:
  vars: {n: the number of keys, h: the height of the tree}
  time: {worst: Θ(h), average: Θ(log n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false, in_place: true}
prereqs: [binary-search-tree, bst-search]
see_also: [bst-deletion, random-binary-search-tree, tree-sort, treap, red-black-tree, quicksort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 12.3 (Insertion and deletion), TREE-INSERT
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.2 (Binary tree searching), Algorithm T (tree search and insertion) and the analysis of random insertions
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.2 (Binary search trees), insert, and the correspondence with quicksort partitioning
---

BST insertion adds a key to a [binary search tree](/binary-search-tree/) by running the [search](/bst-search/) for the key and, when the search falls off the tree, attaching a new leaf at the empty child position where it stopped. It keeps the [binary search tree property](/binary-search-tree-property/) without moving any existing node. It takes $O(h)$ time on a tree of height $h$, so it is fast on a bushy tree and linear on a chain. The shape of the tree depends only on the order of the inserts, which is why sorted input is the bad case and random input gives height $O(\log n)$.

## In plain words

To add a new book to a shelf system where each shelf sign says "smaller titles to the left, larger to the right", walk the signs exactly as if you were looking for the book. At some point the sign tells you to go to a branch that does not exist yet. Build that branch and put the book there.

Nothing that is already in the tree moves. The new key always ends at the bottom, as a leaf. If you find the key on the way, the key is already present, and you only update the data stored with it.

## The problem

The input is a binary search tree $T$ with $n$ distinct keys and a key $k$ with a value $v$. The output is a binary search tree whose keys are the old keys and $k$, where $k$ has value $v$ and each other key keeps its value. If $k$ is already a key, only its value changes.

## The algorithm

Each node has the fields $key$, $value$, $left$, $right$ and $p$ (the parent).

```pseudo id=main
TREE-INSERT(T, k, v)
L1  y ← NIL; x ← T.root
L2  while x ≠ NIL do                       ▷ the search for k
L3      y ← x                               ▷ y is the last node of the path
L4      if k < x.key then x ← x.left
L5      elseif k > x.key then x ← x.right
L6      else x.value ← v; return x          ▷ k is already a key
L7  z ← a new node (k, v) with no children; z.p ← y
L8  if y = NIL then T.root ← z              ▷ the tree was empty
L9  elseif k < y.key then y.left ← z
L10 else y.right ← z
L11 T.n ← T.n + 1; return z
```

Lines L1 to L6 are the [BST search](/bst-search/), with a trailing pointer $y$ that is one step behind $x$. When $x$ becomes NIL, $y$ is the last node of the search path, and the empty child of $y$ on the side of $k$ is the place where the search fell off. Lines L7 to L10 put the new node $z$ there and set its parent. Line L8 handles the empty tree.

## Example

Insert 50, 30, 70, 20, 40, 60, 80, 35, 45 and 65 into an empty tree, then insert 42.

| insert | comparisons | parent and side | depth of the new node |
|---|---|---|---|
| 50 | none | the root | 0 |
| 30 | 50 | left of 50 | 1 |
| 70 | 50 | right of 50 | 1 |
| 20 | 50, 30 | left of 30 | 2 |
| 40 | 50, 30 | right of 30 | 2 |
| 60 | 50, 70 | left of 70 | 2 |
| 80 | 50, 70 | right of 70 | 2 |
| 35 | 50, 30, 40 | left of 40 | 3 |
| 45 | 50, 30, 40 | right of 40 | 3 |
| 65 | 50, 70, 60 | right of 60 | 3 |
| 42 | 50, 30, 40, 45 | left of 45 | 4 |

```
              50
           /      \
         30        70
        /  \      /  \
      20    40   60   80
           /  \    \
         35    45   65
               /
             42
```

The ten first inserts make 19 comparisons in total, the sum of the depths. The insert of 42 compares with 50 ($42 < 50$, left), 30 (right), 40 (right) and 45 (left), and the left child of 45 is empty, so 42 becomes that child. A second insert of 45 would stop at line L6 after three comparisons and change only the value.

## Correctness

Assume $k$ is not a key. The search path for $k$ goes left at a node $u$ exactly when $k < u.key$. The new node $z$ is placed at the end of that path, so for each ancestor $u$ of $z$, $z$ is in the left subtree of $u$ exactly when $k < u.key$. That is the BST property at $u$ for the new key. No other node changes its subtree except by gaining $z$ below it, so the property holds everywhere. If $k$ is a key, the search finds it and only a value changes. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The loop of lines L2 to L6 runs once for each node on the search path, and the rest takes $O(1)$ time. So the time is $\Theta(d + 1)$, where $d$ is the depth of the new node (or of the found node).

- **Worst case.** $d \le h + 1$ for a new leaf, so the time is $O(h)$. On a chain, $h = n - 1$, so one insert can take $\Theta(n)$ time.
- **Building a tree.** Inserting $n$ keys into an empty tree costs, in comparisons, the sum of the depths of the nodes. For keys in increasing order the $i$-th key ($i = 0, 1, \ldots$) has depth $i$, so the total is $\sum_{i=0}^{n-1} i = n(n-1)/2$. For $n = 2000$ that is 1999000.
- **Random order.** If the $n$ distinct keys come in a uniformly random order, the expected total number of comparisons to build the tree is $2(n+1)H_n - 4n$, which is about $2 n \ln n \approx 1.39\, n \lg n$. This is the same as the expected number of comparisons of [quicksort](/quicksort/) with a random pivot: the root plays the role of the first pivot, and each key is compared with exactly the keys that are its ancestors, as in the partitions of quicksort. For $n = 3$ the expected total is $8/3$. So one insert into a random tree costs $O(\log n)$ expected time, and the height is $O(\log n)$ in expectation (see [randomly built BSTs](/random-binary-search-tree/)).
- **Space.** $O(1)$ extra space for the loop, plus the new node.

## Properties

- **Leaf insertion.** The new key is always a leaf. Existing nodes keep their positions, so pointers to them stay valid.
- **Order dependent.** The final shape is a function of the insertion order alone.
- **Online.** Each insert works on the current tree; no knowledge of later keys is needed.
- **Not self-balancing.** Nothing limits the height.

## Variants and improvements

- **Recursive insert.** Sedgewick and Wayne write `put(x, k, v)` that returns the new root of the subtree: if $x$ is NIL return a new node, else recurse to the correct side and assign the result to that child. It needs no parent pointer and no trailing pointer, but uses $\Theta(d)$ stack space.
- **Insert at the root.** Insert $k$ as a leaf, then rotate it up with [tree rotations](/tree-rotation/) until it is the root. Recent keys are then near the top. Randomized BSTs of Martinez and Roura make the new key the root of a subtree of $m$ nodes with probability $1/(m+1)$, which keeps the shape of a random BST.
- **Balanced insertion.** [Red-black trees](/red-black-tree/), [AVL trees](/avl-tree/) and [treaps](/treap/) do this leaf insertion, then repair a balance condition with rotations on the path back to the root, which bounds $h$ by $O(\log n)$.
- **Augmented insertion.** In an [order statistic tree](/order-statistic-tree/), each node on the search path gains 1 in its subtree size. See [augmenting data structures](/augmenting-data-structures/).
- **Duplicates as a multiset.** To keep equal keys, send them always to the right (test $k < x.key$ only), or store a count in each node. The count is simpler and keeps the strict BST property.
- **Tree sort.** Inserting all items and walking the tree in in-order is [tree sort](/tree-sort/).

## When to use it

Use it as the insert of a plain BST, and as the first step of the insert of most balanced trees. On its own it is safe only when the keys come in an order that is close to random. If the order is not under your control, use a balanced tree or shuffle the keys before you build a static tree.

## Pitfalls

- **Losing the parent.** If the loop keeps only $x$ and not $y$ (line L3), it ends with $x = $ NIL and has no node to attach to. Keep the trailing pointer, or use the recursive form that returns the subtree.
- **Wrong side at the end.** Lines L9 and L10 must compare $k$ with $y.key$ again, or remember the side of the last step. Attaching $z$ always to the left of $y$ breaks the BST property.
- **Forgetting the empty tree.** Without line L8, inserting into an empty tree dereferences NIL.
- **No equality test.** Without line L6, a second insert of the same key adds a second node. The map then holds two values for one key, and a delete removes only one of them.
- **Sorted input.** Building a tree from sorted data, such as rows that come from an index, costs $n(n-1)/2$ comparisons and gives a chain. Shuffle first, or build a balanced tree directly from the sorted array by taking the middle key as the root of each subtree.
- **Not updating augmented fields.** In an augmented tree, each node on the search path must update its field (for example the subtree size) during or after the insert. A forgotten update makes later rank queries wrong.

## Implementations

The Python function follows the main block, keeps parent pointers, and returns the node of $k$. It uses a loop, so a chain of thousands of nodes does not overflow the stack.

## History

Algorithm T in Knuth, Section 6.2.2, combines search and leaf insertion, and Knuth reports in the history of that section that the method was found by several people in the 1950s. The link between random insertion order and the comparisons of quicksort is classical; Knuth and Sedgewick and Wayne both use it to analyse random trees.

## References
