---
tag: MBF8HP
kind: data-structure
slug: binary-search-tree
name: Binary search tree
aliases:
- BST
- ordered binary tree
area: data-structures/search-trees
level: intro
summary: Binary tree satisfying the BST property; supports dictionary operations in time proportional to its height.
implements: [dictionary, ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys, h: the height of the tree}
  time: {worst: Θ(h), average: Θ(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [binary-tree, binary-search-tree-property, inorder-traversal]
see_also: [bst-search, bst-insertion, bst-deletion, random-binary-search-tree, balanced-binary-search-tree, red-black-tree, splay-tree, ordered-set]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 12 (Binary search trees), Sections 12.1 to 12.3
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.2 (Binary tree searching), Algorithm T and Algorithm D, and the history at the end of the section
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.2 (Binary search trees)
  - paper: doi:10.1145/321105.321108
    title: Thomas N. Hibbard, Some combinatorial properties of certain trees with applications to searching and sorting, Journal of the ACM 9(1), 1962
    locator: pages 13 to 28 (the deletion method and the analysis of trees built from random insertions)
---

A binary search tree (BST) is a [binary tree](/binary-tree/) whose nodes hold keys from a totally ordered set and satisfy the [binary search tree property](/binary-search-tree-property/): each key in the left subtree of a node is smaller than the key of the node, and each key in the right subtree is larger. It implements the [dictionary](/dictionary/) and the [ordered set](/ordered-set/) operations (search, insert, delete, minimum, maximum, predecessor, successor) in $O(h)$ time, where $h$ is the height of the tree. The height is between $\lfloor \lg n \rfloor$ and $n - 1$, so a plain BST is fast only when its shape is good. The [balanced search trees](/balanced-binary-search-tree/) add rules that keep $h = O(\log n)$.

## In plain words

Think of a guessing game. Someone picks a word from a dictionary, and you may ask "is it before or after this word?". A good player asks about a word in the middle, then about the middle of the half that is left, and so on.

A binary search tree stores these questions in advance. Each node holds one key. Everything smaller is down the left branch, and everything larger is down the right branch. To find a key, start at the top and go left or right at each node. To add a key, walk down the same way until the path stops, and hang the new key there.

The tree is fast when it is bushy, because then each step cuts the work in half. If you add the keys in sorted order, the tree becomes one long chain, and it is as slow as a list.

## The abstract type

A BST implements the [dictionary](/dictionary/): it keeps a finite map from distinct keys to values, with `insert(T, k, v)`, `search(T, k)` and `delete(T, k)`. Because the keys are in order, it also implements the [ordered set](/ordered-set/) operations `minimum(T)`, `maximum(T)`, `successor(T, x)` and `predecessor(T, x)`, the [floor and ceiling](/bst-floor-and-ceiling/) queries, [range search](/bst-range-search/), and a walk of all keys in sorted order. A BST needs only a comparison of two keys; it never computes with the bits of a key. So all its bounds hold in the [comparison model](/comparison-model/).

## Representation

Each node $x$ has the fields $x.key$, $x.value$, $x.left$, $x.right$ and $x.p$ (the parent). A missing child or parent is NIL. The tree $T$ has a field $T.root$, which is NIL for the empty tree, and a count $T.n$ of its nodes.

**Invariant.**

- **(B1) Order.** For each node $x$, each node $y$ in the left subtree of $x$ has $y.key < x.key$, and each node $y$ in the right subtree of $x$ has $y.key > x.key$.
- **(B2) Links.** $T.root.p = $ NIL, and for each node $x$ and each child $c$ of $x$, $c.p = x$.
- **(B3) Count.** $T.n$ is the number of nodes.

By (B1), the keys are distinct, and an [in-order traversal](/inorder-traversal/) lists them in increasing order. Many shapes hold the same set of keys: there are $\frac{1}{n+1}\binom{2n}{n}$ binary trees with $n$ nodes, the [Catalan number](/catalan-numbers/), and each one becomes a BST in exactly one way when the sorted keys are put on its nodes in in-order.

The *depth* of a node is the number of edges from the root to it. The *height* $h$ of the tree is the largest depth, and the empty tree has height $-1$.

## Operations

The main block has the operations of CLRS Chapter 12, written for a map with distinct keys. MAXIMUM and PREDECESSOR are the mirror images of MINIMUM and SUCCESSOR, with left and right swapped.

```pseudo id=main
TREE-SEARCH(T, k)
L1  x ← T.root
L2  while x ≠ NIL and k ≠ x.key do
L3      if k < x.key then x ← x.left else x ← x.right
L4  return x

TREE-MINIMUM(x)
L5  while x.left ≠ NIL do x ← x.left
L6  return x

TREE-SUCCESSOR(x)
L7  if x.right ≠ NIL then return TREE-MINIMUM(x.right)
L8  y ← x.p
L9  while y ≠ NIL and x = y.right do x ← y; y ← y.p
L10 return y

TREE-INSERT(T, k, v)
L11 y ← NIL; x ← T.root
L12 while x ≠ NIL do
L13     y ← x
L14     if k < x.key then x ← x.left elseif k > x.key then x ← x.right
L15     else x.value ← v; return                  ▷ k is already a key
L16 z ← a new node with key k, value v, no children; z.p ← y
L17 if y = NIL then T.root ← z                    ▷ the tree was empty
L18 elseif k < y.key then y.left ← z
L19 else y.right ← z

TRANSPLANT(T, u, v)                               ▷ put subtree v in the place of subtree u
L20 if u.p = NIL then T.root ← v
L21 elseif u = u.p.left then u.p.left ← v
L22 else u.p.right ← v
L23 if v ≠ NIL then v.p ← u.p

TREE-DELETE(T, z)                                 ▷ z is a node of T
L24 if z.left = NIL then TRANSPLANT(T, z, z.right)
L25 elseif z.right = NIL then TRANSPLANT(T, z, z.left)
L26 else y ← TREE-MINIMUM(z.right)                ▷ the successor of z
L27     if y ≠ z.right then TRANSPLANT(T, y, y.right); y.right ← z.right; y.right.p ← y
L28     TRANSPLANT(T, z, y); y.left ← z.left; y.left.p ← y
```

**Search.** Lines L1 to L4 follow one path down from the root. At each node, (B1) says on which side $k$ must be, so the other subtree is never visited. The cost is $O(d + 1)$, where $d$ is the depth where the search stops. The page [BST search](/bst-search/) has the details.

**Minimum and successor.** The minimum is the end of the path of left children (lines L5 and L6). The successor of $x$ is the minimum of its right subtree if that subtree is not empty (line L7). Otherwise it is the lowest ancestor of $x$ whose left subtree holds $x$: lines L8 to L10 go up while $x$ is a right child. Both take $O(h)$ time.

**Insert.** Lines L11 to L15 search for $k$ and keep $y$, the last node of the path. If $k$ is found, its value is replaced. Else the search ends at an empty child position of $y$, and lines L16 to L19 attach the new node there, as a leaf. The cost is $O(h)$. See [BST insertion](/bst-insertion/).

**Delete.** TRANSPLANT (lines L20 to L23) replaces the subtree rooted at $u$ by the subtree rooted at $v$ in the parent of $u$. If $z$ has at most one child, lines L24 and L25 lift that child into the place of $z$. If $z$ has two children, its successor $y$ is the minimum of the right subtree, so $y$ has no left child. Line L27 first cuts $y$ out (if it is not the right child of $z$), and line L28 puts $y$ in the place of $z$, with the two subtrees of $z$. The cost is $O(h)$. See [BST deletion](/bst-deletion/).

## Example

Insert the keys 15, 6, 18, 3, 7, 17, 20, 2, 4, 13 and 9, in this order, into an empty tree. Each key goes down from the root and becomes a leaf.

| insert | path of comparisons | new node is |
|---|---|---|
| 15 | (empty tree) | the root |
| 6 | 15 | left child of 15 |
| 18 | 15 | right child of 15 |
| 3 | 15, 6 | left child of 6 |
| 7 | 15, 6 | right child of 6 |
| 17 | 15, 18 | left child of 18 |
| 20 | 15, 18 | right child of 18 |
| 2 | 15, 6, 3 | left child of 3 |
| 4 | 15, 6, 3 | right child of 3 |
| 13 | 15, 6, 7 | right child of 7 |
| 9 | 15, 6, 7, 13 | left child of 13 |

```
            15
          /    \
         6      18
        / \    /  \
       3   7  17   20
      / \   \
     2   4   13
             /
            9
```

The height is 4, on the path 15, 6, 7, 13, 9. An in-order walk gives 2, 3, 4, 6, 7, 9, 13, 15, 17, 18, 20.

- **search(13)** compares with 15, 6, 7 and 13, and stops at depth 3.
- **search(8)** compares with 15, 6, 7, 13 and 9, then reaches the empty left child of 9, and returns NIL.
- **successor(13)**: 13 has no right child. It is the right child of 7, and 7 is the right child of 6, but 6 is the left child of 15. So the successor is 15.
- **successor(4)**: 4 has no right child and is the right child of 3, and 3 is the left child of 6. So the successor is 6.
- **delete(6)**: 6 has two children. Its successor is 7, which is the right child of 6, so line L27 does nothing. Line L28 puts 7 in the place of 6, with 3 as its left child. The subtree of 7 is now 7 with children 3 and 13.
- **delete(15)**: the root has two children. Its successor is 17, the minimum of the right subtree, and 17 is not the right child of 15. Line L27 cuts 17 out (it has no right child, so the left child of 18 becomes NIL) and gives 17 the right subtree 18. Line L28 makes 17 the root with the left subtree rooted at 7. The keys are now 2, 3, 4, 7, 9, 13, 17, 18, 20.

## Correctness

Each operation keeps (B1) to (B3), and each query returns the answer of the [ordered set](/ordered-set/). The key facts are these. A search loses nothing when it skips a subtree, because (B1) puts all keys of that subtree on the wrong side of $k$. An insert puts the new key at the one place where the search for it ends, and each ancestor of that place has the new key on the right side. A delete with two children puts the successor $y$ in the place of $z$; no key lies strictly between $z.key$ and $y.key$, so $y.key$ is larger than each key of the left subtree of $z$ and smaller than each other key of the right subtree. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Each operation does $O(1)$ work at each node of one or two paths that go up or down the tree, so it takes $O(h + 1)$ time.

| operation | worst case | tree of random insertions (expected) |
|---|---|---|
| search | $\Theta(h)$, up to $\Theta(n)$ | $\Theta(\log n)$ |
| insert | $\Theta(h)$, up to $\Theta(n)$ | $\Theta(\log n)$ |
| delete | $\Theta(h)$, up to $\Theta(n)$ | $\Theta(\log n)$ for a delete in a random tree, but see the pitfalls |
| minimum, maximum | $\Theta(h)$ | $\Theta(\log n)$ |
| successor, predecessor | $\Theta(h)$; $O(1)$ amortized in a full walk | |
| in-order walk of all keys | $\Theta(n)$ | $\Theta(n)$ |
| space | $\Theta(n)$ | |

**The range of $h$.** A binary tree of height $h$ has at most $2^{h+1} - 1$ nodes, so $n \le 2^{h+1} - 1$ and $h \ge \lceil \lg(n+1) \rceil - 1 = \lfloor \lg n \rfloor$ for $n \ge 1$. A tree where each node has at most one child has $h = n - 1$. Inserting keys in increasing order gives exactly this chain, so $n$ inserts then cost $\sum_{i=0}^{n-1} i = n(n-1)/2$ comparisons, which is $\Theta(n^2)$.

**Random insertions.** If the $n$ keys are inserted in a uniformly random order, the expected depth of a node is about $2 \ln n \approx 1.39 \lg n$ and the expected height is $\Theta(\log n)$ (see [randomly built BSTs](/random-binary-search-tree/) and [the expected depth theorem](/random-bst-expected-depth/)).

**Full walk.** Starting at the minimum and calling SUCCESSOR $n - 1$ times visits each edge at most twice, once down and once up, so the walk takes $\Theta(n)$ time in total.

**Lower bound.** In the comparison model, a search among $n$ keys needs $\lceil \lg(n+1) \rceil$ comparisons in the worst case (see the [sorted search lower bound](/sorted-search-lower-bound/)). So no search tree has height below $\lfloor \lg n \rfloor$, and a balanced tree is optimal up to a constant factor.

## Variants

- **Balanced trees.** [AVL trees](/avl-tree/), [red-black trees](/red-black-tree/), [AA trees](/aa-tree/), [weight-balanced trees](/weight-balanced-tree/) and [scapegoat trees](/scapegoat-tree/) keep $h = O(\log n)$ in the worst case or amortized, with [tree rotations](/tree-rotation/) or rebuilds.
- **Randomized trees.** A [treap](/treap/) or a [zip tree](/zip-tree/) gives each key a random priority, so the tree has the shape of a random BST whatever the order of the operations.
- **Self-adjusting trees.** A [splay tree](/splay-tree/) moves each accessed key to the root and has $O(\log n)$ amortized cost, with better bounds on skewed access sequences.
- **Augmented trees.** Extra fields in each node, kept up to date on each change, give new queries: the size of each subtree gives rank and select in an [order statistic tree](/order-statistic-tree/), and the largest endpoint gives an [interval tree](/interval-tree/). See [augmenting data structures](/augmenting-data-structures/).
- **Threaded trees.** A [threaded binary tree](/threaded-binary-tree/) uses the empty child pointers to point to the predecessor and the successor, so a walk needs no stack and no parent pointers.
- **Optimal static trees.** For a fixed set of keys with known search probabilities, the [optimal BST](/optimal-binary-search-tree/) minimizes the [expected search cost](/expected-search-cost-bst/).
- **Multiway trees.** A [B-tree](/b-tree/) stores many keys in a node, to cut the number of disk reads.

## When to use it

Use a plain BST to learn the method, or when the keys come in a random order and the worst case does not matter. In production code, use a balanced tree or a skip list: the cost of the plain tree depends on the order of the inserts, and sorted or nearly sorted input is common. Use a [hash table](/hash-table/) when you do not need ordered queries, because its operations take $O(1)$ expected time. Use a sorted array with [binary search](/binary-search/) when the set does not change.

## Pitfalls

- **Sorted input.** Inserting keys that are already sorted (from a file, from a database index, from a counter) builds a chain of height $n - 1$, and each operation takes linear time. Shuffle the keys first, or use a balanced tree.
- **Recursion on a deep tree.** A recursive search, insert or walk uses stack space $\Theta(h)$, and $h$ can be $n - 1$. In a language with a small stack, such as Python, use loops, as the code of the main block does.
- **Duplicate keys.** With the test "if $k < x.key$ then left else right" and no equality test, a second insert of the same key adds a second node in the right subtree. Then (B1) fails with $<$ replaced by $\le$, a delete removes only one copy, and the map meaning of the tree breaks. Line L15 handles the equal case.
- **Deleting with the predecessor or successor always.** The delete of lines L24 to L28 always takes the successor. After a long random sequence of inserts and deletes, the tree drifts out of balance: the average depth of a node becomes larger than for a tree of random inserts only. Choosing the predecessor or the successor at random avoids most of this effect.
- **Forgetting the parent pointer.** A delete that sets the child link of the parent but not $v.p$ (line L23) breaks (B2), and a later SUCCESSOR walks to the wrong node.
- **Wrong successor when there is no right child.** The successor is the lowest ancestor whose *left* subtree holds $x$, not simply the parent. In the example, the parent of 13 is 7, but the successor is 15.

## Implementations

The Python class keeps parent pointers, as in the main block, and all its loops are iterative, so a chain of thousands of nodes does not overflow the stack. Keys need only the `<` operator; equality is tested as "neither $a < b$ nor $b < a$".

## History

Knuth, in the history at the end of Section 6.2.2, reports that the idea of binary tree search was found by several people in the 1950s, and that P. F. Windley, A. D. Booth and A. J. T. Colin, and T. N. Hibbard published it independently around 1960. Hibbard's paper of 1962 gave the deletion method that replaces a node with two children by its successor, and analysed trees built from random insertions.

## References
