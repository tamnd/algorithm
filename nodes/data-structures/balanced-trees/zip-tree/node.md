---
tag: 4VXZ7W
kind: data-structure
slug: zip-tree
name: Zip tree
aliases:
- zip tree
area: data-structures/balanced-trees
level: research
summary: A randomized BST with random ranks where insertion and deletion are simple zip and unzip operations on sorted lists.
implements: [ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys in the tree}
  time: {expected: Θ(log n), worst: Θ(n)}
  space: {extra: Θ(n)}
prereqs: [treap, skip-list, binary-search-tree, treap-split, treap-merge]
see_also: [treap, skip-list, implicit-treap, random-binary-search-tree, random-bst-expected-depth, join-based-tree-algorithms]
sources:
  - url: https://arxiv.org/abs/1806.06726
    title: Robert E. Tarjan, Caleb C. Levy and Stephen Timmel, Zip trees, Workshop on Algorithms and Data Structures (WADS), 2019, and ACM Transactions on Algorithms 17(4), 2021
    locator: the rank rule, insertion by unzipping, deletion by zipping, the expected depth, and the relation to skip lists
  - paper: doi:10.1007/BF01940876
    title: Raimund Seidel and Cecilia R. Aragon, Randomized search trees, Algorithmica 16(4/5), 1996
    locator: treaps, the heap order on random priorities, and split and join
  - paper: doi:10.1145/78973.78977
    title: William Pugh, Skip lists, a probabilistic alternative to balanced trees, Communications of the ACM 33(6), 1990
    locator: the geometric levels of skip-list nodes
---

A zip tree is a randomized [binary search tree](/binary-search-tree/) in which each node gets a random *rank* when it is inserted, drawn from the geometric distribution: rank $k$ with probability $1/2^{k+1}$. The ranks are in heap order, a parent's rank at least its children's, with ties allowed only for right children. So a zip tree is a [treap](/treap/) whose priorities are small integers, with ties broken by key. Insertion and deletion use no rotations. To insert, the tree *unzips* the search path below the new node's place into two paths, one with the smaller keys and one with the larger. To delete, it *zips* the two spines below the deleted node back into one path, like a zipper. Robert Tarjan, Caleb Levy and Stephen Timmel introduced zip trees in 2018. They are a binary-tree form of a [skip list](/skip-list/), and the expected depth of a node is at most about $1.5 \lg n$.

## In plain words

Give each key a random number by tossing a coin until it lands tails, and count the heads. Most keys get 0, a quarter get 1, an eighth get 2, and so on. Build the search tree so that keys with bigger numbers sit higher, like a tournament where the winner rises.

To insert a key, walk down until you reach a node with a smaller number than the new one. That is where the new key belongs. The part of the tree below that point is cut along the search path into two pieces, the keys smaller than the new key and the keys larger, and these pieces become its two subtrees. Deletion does the reverse: the two pieces below the deleted node are merged along their facing edges, like closing a zipper.

## The abstract type

The tree implements an [ordered set](/ordered-set/): CONTAINS$(k)$, INSERT$(k)$ and DELETE$(k)$ on keys from a totally ordered universe, and the keys in increasing order. INSERT returns false when the key is present, and DELETE returns false when it is absent.

## Representation

A node holds a key, a left and a right child, and a rank, a small non-negative integer. The rules are:

1. (Z1) The tree is a binary search tree.
2. (Z2) A left child has a smaller rank than its parent, and a right child has a rank at most its parent's.

Say that $u$ beats $v$ when $u$ has the larger rank, or the same rank and the smaller key. Then (Z2) says that each node beats its children, so the zip tree is the treap for the priority $(rank, -key)$. Given the keys and their ranks, there is exactly one zip tree, whatever the order of insertions and deletions.

The largest rank among $n$ nodes is $\lg n + O(1)$ with high probability, so a rank fits in $O(\log \log n)$ bits, about one byte. A treap needs priorities of $\Theta(\log n)$ bits to avoid ties.

## Operations

CONTAINS is the search of a binary search tree; it never reads ranks.

```pseudo id=main
INSERT(k)
L1  if k is in the tree then return false; x ← a node with key k and rank RANDOM-RANK()
L2  cur ← root; walk down the search path of k while cur ≠ nil and cur beats x
L3  (x.left, x.right) ← UNZIP(cur, k)
L4  put x in the place of cur (as the child of the last node passed, or as the root); return true

UNZIP(t, k)                                ▷ k is not in t
L5  P ← nil; Q ← nil
L6  while t ≠ nil: if t.key < k then hang t at the bottom of the right spine of P; t ← t.right
                   else hang t at the bottom of the left spine of Q; t ← t.left
L7  end both spines with nil; return (P, Q)

DELETE(k)
L8  find the node x with key k (else return false); put ZIP(x.left, x.right) in its place; return true

ZIP(a, b)                                  ▷ all keys of a are less than all keys of b
L9  while a ≠ nil and b ≠ nil: if a.rank ≥ b.rank then hang a; a ← a.right
                               else hang b; b ← b.left
L10 hang the one of a, b that is not nil; return the first node hung
```

"Hang" means: attach the node at the current hook, the place where the previous node wants its next child, and then make the hook its right child (after taking $a$) or its left child (after taking $b$). RANDOM-RANK counts heads before the first tail. On a tie in ZIP, $a$ stays on top, because it has the smaller key; that is the tie rule of (Z2).

UNZIP is the split of a treap, and ZIP is the merge, written as loops over the two paths. Both change only the pointers where the path switches between $P$ and $Q$, or between the spines of $a$ and $b$.

## Example

Take the keys 10 to 70 with the ranks 10: 0, 20: 2, 30: 0, 40: 1, 50: 3, 60: 0, 70: 1. The root is 50, with the largest rank. On the left, 20 has the largest rank, with 10 to its left and 40 (above 30) to its right. On the right, 70 has rank 1, above 60. Writing a tree as (left, key, right):

$$((10, 20, (30, 40, \text{nil})), 50, (60, 70, \text{nil})).$$

**Insert 35 with rank 2.** The walk passes 50 (rank 3 beats 2) and 20 (rank 2, the same, but key 20 is smaller, so 20 beats 35), and stops at 40 (rank 1). UNZIP cuts the subtree $(30, 40, \text{nil})$ along the search path of 35: 40 goes to $Q$, then 30 to $P$. So $P = 30$ and $Q = 40$, and 35 takes the place of 40 as the right child of 20:

$$((10, 20, (30, 35, 40)), 50, (60, 70, \text{nil})).$$

Here 35 has the same rank as its parent 20, which is allowed because it is a right child.

**Delete 50.** ZIP merges the right spine of the left subtree, 20, 35, 40, with the left spine of the right subtree, 70. It takes 20 (rank 2 against 1), then 35 (rank 2 against 1), then 40 (rank 1 against 1: a tie, so the smaller key 40 stays above), and then hangs 70, with 60 still below it, as the right child of 40:

$$(10, 20, (30, 35, (\text{nil}, 40, (60, 70, \text{nil})))).$$

## Correctness

Since "beats" is a strict total order, a zip tree is a treap, and the proofs for treap split and merge apply. When INSERT stops at $cur$, every node above it beats $x$, and $x$ beats $cur$ and so every node below $cur$. UNZIP divides the subtree of $cur$ along the search path: a node with a smaller key goes to $P$ with its left subtree, and the next such node, which lay in its old right subtree, becomes its right child; this keeps the search order and the heap order. ZIP is the merge of two treaps in loop form, and on a tie the left node beats the right one, as the rule asks. The full proof is in the proofs folder.

## Complexity

**Depth.** Tarjan, Levy and Timmel show that the expected depth of a node is at most about $1.5 \lg n + O(1)$, and the height is $O(\log n)$ with high probability. A treap with continuous priorities has expected depth about $2 \ln n \approx 1.39 \lg n$; the ties among the small ranks cost a little. In a test with $n = 2^{15}$ random keys, the average depth was 21.3, while $1.5 \lg n = 22.5$.

**Time.** All operations follow one search path, and UNZIP and ZIP follow paths below one node, so each takes $O(\log n)$ expected time. The worst case is $\Theta(n)$.

**Pointer changes.** An insertion or deletion changes $O(1)$ pointers in expectation, as for a treap, because the paths unzipped or zipped have $O(1)$ expected switches between the two sides. The tree is also *history independent*: its shape reveals nothing about the order of past operations.

**Space.** Two pointers and a rank of $O(\log \log n)$ bits per node.

## Variants

- **Skip lists.** A node of rank $r$ corresponds to a skip-list node of height $r + 1$. Tarjan, Levy and Timmel show that the zip tree is a binary-tree representation of the skip list with the same levels, and that a search in one corresponds to a search in the other.
- **Treaps.** With a continuous random priority instead of a geometric rank, the same code gives a [treap](/treap/) that inserts by split and deletes by merge, with no rotations.
- **Zip-zip trees.** Gila, Goodrich and Tarjan (2023) add a second, small random rank to break ties among nodes of the same rank, which brings the expected depth close to the $1.39 \lg n$ of a treap while keeping ranks of $O(\log \log n)$ bits.
- **Biased ranks.** Choosing larger ranks for keys that are searched often makes them shallow, as in biased skip lists.

## When to use it

Use a zip tree when you want a randomized search tree that is short to write, uses no rotations, keeps very small balance data, and has a shape independent of the history. It is a good teaching link between skip lists and treaps. For worst-case guarantees, use a deterministic tree such as a [red-black tree](/red-black-tree/).

## Pitfalls

- **Wrong tie rule.** Equal ranks are common: half of all nodes have rank 0. The rule must allow equal ranks only for right children, and every test must use it: the walk in INSERT stops at the first node that does not beat $x$, and ZIP keeps the left node on a tie. Mixing rules gives a valid search tree but loses the uniqueness of the shape and can break the depth analysis.
- **Rank from a bad generator.** The rank must be geometric with parameter $\frac12$ and independent of the keys. A rank derived from a hash of the key is fine only if the hash behaves randomly on the keys used.
- **Not checking for an existing key.** The walk of line L2 may stop above the node with key $k$; then UNZIP would see $k$ itself. Search first, or handle equal keys in UNZIP.
- **Losing the end of a spine.** UNZIP must end both spines with nil (line L7), or the last node keeps a stale child from the other side.

## Implementations

## History

Robert Tarjan, Caleb Levy and Stephen Timmel posted "Zip trees" in 2018; it appeared at WADS 2019 and in ACM Transactions on Algorithms in 2021. They built on Seidel and Aragon's treaps (1989) and on Pugh's skip lists (1990), and the insertion and deletion by unzipping and zipping paths go back to treap insertion by split. Ofek Gila, Michael Goodrich and Tarjan later proposed zip-zip trees to tighten the depth.

## References
