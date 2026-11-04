---
tag: 6S4865
kind: theorem
slug: red-black-height-theorem
name: Red-black tree height bound
aliases:
- red-black height lemma
area: data-structures/balanced-trees
level: core
summary: A red-black tree with n internal nodes has height at most 2 log2(n+1).
prereqs: [red-black-tree, black-height, induction]
see_also: [avl-height-theorem, red-black-correspondence-with-2-3-4-trees, two-three-four-tree, left-leaning-red-black-tree, balanced-binary-search-tree, wavl-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 13.1, Properties of red-black trees, Lemma 13.1 and its proof
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.3, Balanced Search Trees, Proposition G (the height of a red-black BST is at most 2 lg N)
  - paper: doi:10.1109/SFCS.1978.3
    title: Leo J. Guibas and Robert Sedgewick, A dichromatic framework for balanced trees, FOCS 1978
    locator: the height bound for red-black trees
  - url: "https://opendatastructures.org/"
    title: Pat Morin, Open Data Structures
    locator: Chapter 9, Red-Black Trees (Section 9.1, the height of a 2-4 tree, and Section 9.2, the height of a red-black tree)
---

A [red-black tree](/red-black-tree/) with $n$ internal nodes has height at most $2 \lg(n + 1)$. The proof has two steps: a subtree whose root has [black-height](/black-height/) $b$ holds at least $2^b - 1$ internal nodes, and the black-height of the root is at least half the height, because red nodes cannot follow each other. So search, insertion and deletion in a red-black tree take $O(\log n)$ time. The bound is Lemma 13.1 of CLRS, and it is tight up to an additive constant: there are red-black trees with $2^{j+1} - 2$ internal nodes and height $2j$.

## Statement

A red-black tree is a binary search tree whose $n$ internal nodes hold the keys and whose leaves are the empty nodes nil. Each node is red or black, and (R1) the root is black, (R2) each leaf is black, (R3) a red node has two black children, and (R4) for each node $x$, all paths from $x$ down to a leaf have the same number of black nodes. The black-height $bh(x)$ is the number of black nodes on such a path, not counting $x$ itself. The height of the tree is the number of edges on a longest path from the root to a leaf, which is the number of internal nodes on that path.

**Theorem.** Let $T$ be a red-black tree with $n$ internal nodes and height $h$. Then

1. **(Size.)** For each node $x$, the subtree of $x$ has at least $2^{bh(x)} - 1$ internal nodes.
2. **(Black-height.)** $bh(\text{root}) \ge h/2$.
3. **(Height.)** $h \le 2 \lg(n + 1)$.

Only (R2), (R3) and (R4) are needed; the color of the root plays no part.

## In plain words

Look only at the black nodes. Every path from the top down to the bottom meets the same number of them, so the black nodes alone form a tree with no short or long branches, and such a tree is bushy: it holds about two to the power of that number of nodes.

The red nodes can make some paths longer, but not much. A red node always has black children, so at most every second node on a path is red. A path is then at most twice as long as its count of black nodes. Together, the longest path is at most about twice the base-2 log of the number of nodes.

## Proof

**Part 1.** By induction on the height of $x$, the number of edges on a longest path from $x$ down to a leaf. If the height is 0, then $x$ is a leaf, $bh(x) = 0$, and its subtree has $0 = 2^0 - 1$ internal nodes.

Let $x$ be an internal node of height at least 1. It has two children $y$ and $z$, each of smaller height. Take a path from $x$ to a leaf through $y$. Its black nodes after $x$ are $y$, if $y$ is black, and the black nodes after $y$. So $bh(x) = bh(y) + 1$ if $y$ is black and $bh(x) = bh(y)$ if $y$ is red; in both cases $bh(y) \ge bh(x) - 1$, and the same holds for $z$. By (R4), $bh(x)$ does not depend on which path is chosen. By the induction hypothesis, the subtree of $x$ has at least
$$1 + (2^{bh(x) - 1} - 1) + (2^{bh(x) - 1} - 1) = 2^{bh(x)} - 1$$
internal nodes.

**Part 2.** Let $v_0, v_1, \ldots, v_h$ be a path of length $h$ from the root $v_0$ to a leaf $v_h$. The nodes $v_1, \ldots, v_h$, not counting the root, are $h$ nodes. The leaf $v_h$ is black by (R2). If $v_i$ is red for some $1 \le i < h$, then $v_{i+1}$ is black by (R3). So the map $v_i \mapsto v_{i+1}$ sends the red nodes among $v_1, \ldots, v_h$ to distinct black nodes among them, and there are at least as many black nodes as red ones. Hence at least $h/2$ of these nodes are black, and $bh(v_0) \ge h/2$.

**Part 3.** Apply part 1 to the root and use part 2: $n \ge 2^{bh(\text{root})} - 1 \ge 2^{h/2} - 1$. So $2^{h/2} \le n + 1$, and taking $\lg$ gives $h \le 2 \lg(n + 1)$. $\blacksquare$

## Consequences

- **Logarithmic operations.** A search follows one path, so it takes $O(\log n)$ time in a red-black tree. Insertion and deletion walk one path and do $O(1)$ work per level, so they take $O(\log n)$ time too.
- **Left-leaning red-black trees.** A [left-leaning red-black tree](/left-leaning-red-black-tree/) is a red-black tree with one more rule, so the bound holds for it, and Sedgewick and Wayne state it as their Proposition G.
- **2-3-4 trees.** Merging each red node into its black parent gives a [2-3-4 tree](/two-three-four-tree/) whose height is the black-height (see [the correspondence](/red-black-correspondence-with-2-3-4-trees/)). Part 1 is the statement that a 2-3-4 tree of height $b$ has at least $2^b - 1$ keys, and part 2 says each 2-3-4 level is at most two binary levels.
- **Average-case cost.** The bound is for the worst case. In practice the depth of a typical node in a red-black tree is close to $\lg n$.
- **Other balanced trees.** The same two-step argument, a size bound from a rank and a bound on how much the height can exceed the rank, works for [AA trees](/aa-tree/) and [WAVL trees](/wavl-tree/).

## Tightness

The bound is tight up to an additive constant. For $j \ge 1$, build a tree $Z_j$ with $bh = j$ at the root: $Z_1$ is a black node with one red child, and $Z_j$ is a black root whose right child is a perfect all-black tree $P$ with $2^{j-1} - 1$ internal nodes, and whose left child is a red node with left child $Z_{j-1}$ and right child another copy of $P$. Each of $Z_{j-1}$ and $P$ has $j - 1$ black internal nodes on every path, so (R3) and (R4) hold. The height grows by 2 at each step, so $Z_j$ has height $h = 2j$, and its number of internal nodes satisfies $n_j = n_{j-1} + 2 + 2(2^{j-1} - 1) = n_{j-1} + 2^j$ with $n_1 = 2$, so $n_j = 2^{j+1} - 2$. Then
$$h = 2j = 2 \lg(n + 2) - 2,$$
which is within 2 of the bound $2 \lg(n + 1)$. For $j = 2$ this is a tree with 6 internal nodes and height 4, while $2 \lg 7 \approx 5.6$.

In the other direction, a red-black tree with only black nodes is perfect, so its height is $\lg(n + 1)$. The ratio between the worst and the best height is 2, while for [AVL trees](/avl-height-theorem/) the worst height is about $1.44 \lg n$.

## History

Bayer (1972) introduced symmetric binary B-trees, the binary form of 2-3-4 trees, and their height bound follows from that of B-trees. Guibas and Sedgewick (1978) recast them with red and black colors and proved the bound in this form. The two-step proof with the black-height is the one in CLRS, Lemma 13.1, since its first edition.

## References
