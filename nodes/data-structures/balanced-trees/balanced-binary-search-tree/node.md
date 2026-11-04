---
tag: NK90JR
kind: concept
slug: balanced-binary-search-tree
name: Balanced binary search tree
aliases:
- balanced BST
- height-balanced search tree
area: data-structures/balanced-trees
level: intro
summary: A BST whose shape is kept near-minimal height so that search, insert and delete take O(log n) time in the worst case.
prereqs: [binary-search-tree, asymptotic-notation]
see_also: [tree-rotation, tree-rebalancing, avl-tree, red-black-tree, two-three-tree, treap, skip-list, b-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 12 (binary search trees, operations in O(h) time) and Chapter 13 (red-black trees, Lemma 13.1)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.3, Balanced Trees (Theorem A on the height of AVL trees, and weight-balanced trees)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.3, Balanced Search Trees (2-3 search trees and red-black BSTs)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 3, Section 3.4, Binary Search Trees (balanced search trees)
  - paper: "Luc Devroye, A note on the height of binary search trees, Journal of the ACM 33(3), 1986"
    locator: the height of a random binary search tree is about 4.311 ln n with high probability
---

A balanced binary search tree is a [binary search tree](/binary-search-tree/) that keeps a rule on its shape, so that its height stays $O(\log n)$ for $n$ keys after any sequence of insertions and deletions. Search, insertion, deletion, minimum, maximum, predecessor and successor all take time proportional to the height, so a balanced tree gives each of them in $O(\log n)$ time in the worst case, or amortized, or in expectation, depending on the scheme. It implements the [ordered set](/ordered-set/) and the [ordered symbol table](/ordered-symbol-table/), and it is the sorted map of most standard libraries.

## In plain words

A search tree finds a key by walking down from the top. At each node it goes left for a smaller key and right for a larger key. The walk is as long as the tree is tall. If you insert keys that are already sorted into a plain search tree, each new key goes to the bottom right, and the tree becomes one long path. Then a search looks at every key, as in a list.

A balanced tree adds a rule that stops this. After each insertion or deletion, it checks the rule on the path it walked, and it fixes the shape with small local moves called rotations. The rule is weak enough to fix cheaply, but strong enough to keep the tree short. With a million keys, a balanced tree is about 20 to 40 levels tall instead of a million.

## The idea

**Height decides the cost.** Let $h$ be the height of the tree, the number of nodes on the longest path from the root down (the empty tree has height 0). The operations of a binary search tree all follow one path from the root, so they take $O(h)$ time. A tree of height $h$ has at most $2^h - 1$ nodes, so each tree with $n$ nodes has

$$h \ge \lceil \lg(n + 1) \rceil.$$

Insertions in sorted order without balancing give $h = n$. A scheme is *balanced* when it guarantees $h = O(\log n)$ for every sequence of updates, in the sense that the scheme states (worst case, amortized or expected).

**Kinds of balance rule.**

| scheme | the rule | height bound for $n$ keys | sense |
|---|---|---|---|
| [AVL tree](/avl-tree/) | at each node, the two subtree heights differ by at most 1 | $h < 1.4405 \lg(n+2) - 0.3277$ | worst case |
| [red-black tree](/red-black-tree/) | colors, no red node with a red child, equal [black-height](/black-height/) | $h \le 2\lg(n+1)$ | worst case |
| [2-3 tree](/two-three-tree/), [2-3-4 tree](/two-three-four-tree/) | nodes with 2 to 3 (or 4) children, all leaves at one depth | $h \le \lg(n+1)$ levels of nodes | worst case |
| [weight-balanced tree](/weight-balanced-tree/) | each subtree has at least a fixed fraction of the weight of its parent | $O(\log n)$ | worst case |
| [treap](/treap/), [zip tree](/zip-tree/) | random priorities in heap order | expected depth $O(\log n)$ | expected |
| [scapegoat tree](/scapegoat-tree/) | depth at most about $\log_{1/\alpha} n$, kept by rebuilding | $\log_{1/\alpha} n + O(1)$ | worst-case height, amortized time |
| [splay tree](/splay-tree/) | no rule, the accessed node moves to the root | none | amortized time only |

The AVL bound is Theorem A of Knuth, Section 6.2.3, and is proved on the page [AVL height bound](/avl-height-theorem/). The red-black bound is Lemma 13.1 of CLRS and is proved on the page [red-black height bound](/red-black-height-theorem/).

**How the rule is restored.** An insertion or a deletion changes the tree along one root-to-leaf path. So the rule can break only at the nodes of that path. Each scheme repairs it with [rotations](/tree-rotation/), with changes of colors or ranks, or with the rebuild of a subtree, and it works on the path only. The repair costs $O(h) = O(\log n)$, and in AVL, red-black and WAVL trees it uses $O(1)$ rotations per insertion. The page [tree rebalancing](/tree-rebalancing/) compares the repairs.

**What the balance buys besides search.** A path of length $O(\log n)$ also gives fast [order statistics](/order-statistic-tree/) when each node stores its subtree size, fast split and join of whole sets (see [join-based tree algorithms](/join-based-tree-algorithms/)), and cheap [persistent versions](/persistent-red-black-tree/) by copying the $O(\log n)$ nodes of a path.

**Lower bound.** In the [comparison model](/comparison-model/), a search among $n$ keys needs $\lceil \lg(n+1) \rceil$ comparisons in the worst case, because a search that fails must tell apart the $n + 1$ gaps between the keys, and each comparison has at most two outcomes that continue the search. So a balanced tree is optimal up to a constant factor, and the schemes differ only in the constant: about 1 for 2-3 trees counted in levels, 1.44 for AVL trees and 2 for red-black trees.

## Examples

**Sorted insertions.** Insert the keys 1 to 7 in order. A plain search tree becomes a right chain of height 7. An AVL tree that receives the same keys ends as the perfect tree with root 4, children 2 and 6, and leaves 1, 3, 5, 7, of height 3, which is $\lceil \lg 8 \rceil$. The trace is on the page [AVL tree](/avl-tree/).

**Heights for large $n$.** The bounds of the table give, rounded down to whole levels:

| $n$ | least height $\lceil \lg(n+1) \rceil$ | AVL bound | red-black bound | chain |
|---|---|---|---|---|
| $10^3$ | 10 | 14 | 19 | 1000 |
| $10^6$ | 20 | 28 | 39 | 1000000 |
| $10^9$ | 30 | 42 | 59 | 1000000000 |

So with a billion keys, a search in a red-black tree visits at most 59 nodes, and in an AVL tree at most 42.

**Random order is not a guarantee.** If the keys arrive in a uniformly random order, a plain search tree has expected depth about $2 \ln n \approx 1.39 \lg n$ for a node, and height about $4.311 \ln n$ with high probability (Devroye, 1986). This is good on average, but a sorted or nearly sorted input, which is common in practice, gives height $\Theta(n)$. A [treap](/treap/) gets the random shape for every input by drawing the random order itself.

**A non-example.** The rule "the root has two subtrees of equal size" is not a balance rule: both subtrees of the root can still be chains, so the height is about $n/2$. A balance rule must hold at every node, or it must bound the depth directly.

## Where it is used

- Sorted maps and sets of standard libraries: `std::map` and `std::set` in C++ and `TreeMap` in Java are red-black trees in the common implementations.
- The [sweep-line technique](/sweep-line-technique/) keeps its [sweep status](/sweep-status-structure/) in a balanced tree, for example in [rectangle intersection](/rectangle-intersection-sweep/).
- [Interval trees](/interval-tree/) and [order-statistic trees](/order-statistic-tree/) are balanced trees with extra fields.
- On disk, the same idea with wide nodes gives the [B-tree](/b-tree/).
- [Skip lists](/skip-list/) reach the same expected bounds with random levels instead of a tree shape.

## References
