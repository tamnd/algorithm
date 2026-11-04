---
tag: 096NRC
kind: data-structure
slug: scapegoat-tree
name: Scapegoat tree
aliases:
- scapegoat tree
area: data-structures/balanced-trees
level: advanced
summary: A BST without per-node balance data that rebuilds a subtree rooted at a scapegoat when it becomes too unbalanced; O(log n) amortized.
implements: [ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys in the tree}
  time: {worst: Θ(n), amortized: Θ(log n)}
  space: {extra: Θ(n)}
prereqs: [binary-search-tree, balanced-binary-search-tree, tree-rebalancing]
see_also: [weight-balanced-tree, tree-rebalancing, avl-tree, red-black-tree, splay-tree, treap, order-statistic-tree]
sources:
  - paper: Igal Galperin and Ronald L. Rivest, Scapegoat trees, Proceedings of the Fourth Annual ACM-SIAM Symposium on Discrete Algorithms (SODA), 1993
    locator: pages 165 to 174, the scapegoat search, rebuilding, and the amortized analysis
  - url: https://opendatastructures.org/ods-python/8_1_ScapegoatTree_Binary_Se.html
    title: Pat Morin, Open Data Structures, Section 8.1, ScapegoatTree
    locator: the counters n and q, Lemma 8.1, and the analysis with alpha = 2/3
  - paper: Arne Andersson, General balanced trees, Journal of Algorithms 30(1), 1999
    locator: partial rebuilding with a height bound and no balance data in the nodes
---

A scapegoat tree is a [binary search tree](/binary-search-tree/) that stores no balance data at all: no color, no height and no size in the nodes. It keeps only two counters for the whole tree, the number of keys $n$ and an upper bound $q$ on it. When an insertion puts a node deeper than $\log_{1/\alpha} q$, for a fixed $\frac12 < \alpha < 1$, the tree walks back up from the new node to an ancestor whose subtree is lopsided in size, the *scapegoat*, and rebuilds that subtree into a perfectly balanced tree. When deletions shrink $n$ below $\alpha q$, it rebuilds the whole tree. The height stays at most $\log_{1/\alpha} n + 1$, so a search takes $O(\log n)$ time in the worst case, and insertion and deletion take $O(\log n)$ amortized time. Igal Galperin and Ronald Rivest named and analyzed the tree in 1993; Arne Andersson had found the same method in 1989.

## In plain words

Most balanced trees fix small problems at once, with a rotation here and a recoloring there, and they store some data in every node to see the problems. A scapegoat tree waits. It lets the tree get a little out of shape, and it only checks one thing: is the new key too deep?

When a key lands too deep, some ancestor must have most of its nodes on one side. The tree blames that ancestor, takes all the keys below it in sorted order, and builds them again into a perfectly balanced subtree. That is slow for a big subtree, but a big lopsided subtree needs many updates to happen, so the cost spread over all those updates is small.

## The abstract type

The tree implements an [ordered set](/ordered-set/): CONTAINS$(k)$, INSERT$(k)$ and DELETE$(k)$ on keys from a totally ordered universe, and the keys in increasing order. INSERT returns false when the key is present, and DELETE returns false when it is absent.

## Representation

Each node holds a key and two child pointers, as in a plain binary search tree. The tree holds the root, the parameter $\alpha$ with $\frac12 < \alpha < 1$, and two counters:

1. $n$, the number of keys;
2. $q$, a counter that each insertion increases and each full rebuild resets to $n$.

Write $\text{size}(x)$ for the number of nodes in the subtree of $x$; it is not stored, but counted when needed. The tree keeps three invariants:

1. (S1) It is a binary search tree on the current keys.
2. (S2) $\alpha q \le n \le q$.
3. (S3) Each node has depth at most $\log_{1/\alpha} q$, with the root at depth 0.

A node $w$ with a child $c$ such that $\text{size}(c) > \alpha \cdot \text{size}(w)$ is *$\alpha$-weight-unbalanced*. The tree does not forbid such nodes; it only removes the ones on a path that has grown too long.

## Operations

CONTAINS is the search of a binary search tree. The code below follows Galperin and Rivest, with the counters of Morin's Open Data Structures.

```pseudo id=main
INSERT(k)
L1  search for k from the root, keeping the path P; if k is found, return false
    attach a new leaf u with key k below the last node of P
L2  n ← n + 1; q ← q + 1
L3  if depth(u) > log_{1/α} q then
L4      walk up from u: w ← the first ancestor with size(child of w on P) > α · size(w)
L5      replace the subtree of w by REBUILD(w)
    return true

DELETE(k)
L6  delete k as in a binary search tree; if k is absent, return false
L7  n ← n − 1
L8  if n < α · q then root ← REBUILD(root); q ← n
    return true

REBUILD(w)
L9  a ← the nodes of the subtree of w, in key order
L10 return BUILD(a, 0, |a|)

BUILD(a, lo, hi)                           ▷ a perfectly balanced tree on a[lo .. hi − 1]
L11 if lo ≥ hi then return nil
L12 mid ← ⌊(lo + hi)/2⌋; t ← a[mid]; t.left ← BUILD(a, lo, mid); t.right ← BUILD(a, mid + 1, hi); return t
```

Line L4 counts sizes as it walks up: the size of an ancestor is the size of the child on the path, plus one, plus the size of the other child, which is counted by a traversal. All these traversals stay inside the subtree of $w$, so line L4 costs $O(\text{size}(w))$, the same as the rebuild. Line L3 needs no real logarithm: $d > \log_{1/\alpha} q$ holds exactly when $(1/\alpha)^d > q$, which a program can test with integers when $\alpha$ is a fraction. REBUILD reuses the nodes and only changes their pointers; it lists them by an in-order walk, iteratively or with a stack.

## Example

Take $\alpha = 2/3$ and insert 1, 2, 3, 4 in order. Each key goes to the right of the last one, and the tree is a chain. The depth of 4 is 3, and $\log_{3/2} 4 \approx 3.42$, so no rebuild is needed.

Insert 5. It lands at depth 4, and $\log_{3/2} 5 \approx 3.97$, so line L3 starts a scapegoat search. Going up from 5:

| node | child on the path, its size | size of the node | child $> \frac23$ size? |
|---|---|---|---|
| 4 | 5, size 1 | 2 | $1 > 1.33$? no |
| 3 | 4, size 2 | 3 | $2 > 2$? no |
| 2 | 3, size 3 | 4 | $3 > 2.67$? yes |

Node 2 is the scapegoat. Its subtree holds 2, 3, 4, 5. BUILD takes $a[2] = 4$ as the root, then $a[1] = 3$ from $[2, 3]$ with left child 2, and 5 on the right. The tree is now the root 1 with right child 4, where 4 has left child 3 (with left child 2) and right child 5. Its height drops from 4 to 3 edges, and $n = q = 5$.

Now delete 1. The root has no left child, so 4 takes its place, $n = 4$ and $q = 5$, and since $4 \ge \frac23 \cdot 5$, nothing more happens. Delete 5. Then $n = 3 < \frac23 \cdot 5$, so line L8 rebuilds the whole tree from $[2, 3, 4]$ into 3 with children 2 and 4, and sets $q = 3$.

## Correctness

The proof keeps invariants (S1), (S2) and (S3). The key step is that a scapegoat always exists and that the rebuild always helps.

1. **A scapegoat exists.** If every node on the path from the new leaf $u$ at depth $d$ up to the root had its child on the path of size at most $\alpha$ times its own size, the root would have at least $(1/\alpha)^d > q \ge n$ nodes, which it does not.
2. **The rebuild shortens the path.** Let $u$ be $i$ levels below the scapegoat $w$, whose subtree has $m$ nodes. Before the insertion, all nodes were at depth at most $\log_{1/\alpha} q$, so the subtree of $w$ had height at most $i - 1$ and at most $2^i - 1$ nodes; it could not be the perfect tree of that height, because then $w$ would not be unbalanced. So $m < 2^i$, and the rebuilt subtree has height $\lfloor \lg m \rfloor \le i - 1$. Every node in it is now at depth at most $d - 1 \le \log_{1/\alpha} q$.
3. **Deletion.** Removing a node never makes another node deeper, and the full rebuild of line L8 gives height $\lfloor \lg n \rfloor \le \log_{1/\alpha} n$, because $1/\alpha < 2$.

Rebuilding keeps the nodes in key order, so the search order and the key set are kept. The full proof is in the proofs folder.

## Complexity

**Search.** By (S2) and (S3), the height is at most $\log_{1/\alpha} q \le \log_{1/\alpha} n + 1$, so CONTAINS takes $O(\log n)$ time in the worst case. For $\alpha = 2/3$, this is about $1.71 \lg n$.

**Updates, worst case.** One insertion can rebuild a subtree with a constant fraction of all the nodes, and one deletion can rebuild the whole tree, so a single update takes $\Theta(n)$ time in the worst case.

**Updates, amortized.** Let $D(x) = |\text{size}(x.left) - \text{size}(x.right)|$. Right after a rebuild, $D(x) \le 1$ at each node $x$ in the rebuilt subtree, and a new leaf has $D = 0$. Each update changes $D(x)$ by at most one, and only at nodes $x$ on its path. At a scapegoat $w$ of size $m$, the heavy child has more than $\alpha m$ nodes and the other child $m - 1$ minus that, fewer than $(1 - \alpha) m - 1$, so $D(w) > (2\alpha - 1) m + 1$. So more than $(2\alpha - 1) m$ updates have passed through $w$ since it was last rebuilt or created. If each update pays $O(1/(2\alpha - 1))$ credits to each of the $O(\log n)$ nodes on its path, the credits at $w$ pay for the $O(m)$ work of the scapegoat search and the rebuild. A full rebuild in DELETE happens only after more than $(1 - \alpha) q$ deletions since the last full rebuild, because $q - n$ counts those deletions; they pay $O(1/(1 - \alpha))$ each for the $O(n)$ work. So a sequence of $m$ operations from the empty tree takes $O(m \log m)$ time, $O(\log n)$ amortized per update.

**Space.** The tree uses $\Theta(n)$ space and two pointers per node, which is the least of all balanced trees. A rebuild needs an array of $m$ pointers, or $O(\log m)$ extra space with an in-place method.

The choice of $\alpha$ trades the two costs. An $\alpha$ close to $\frac12$ keeps the tree almost perfectly balanced, with fast searches and many rebuilds; an $\alpha$ close to 1 allows deep trees and rebuilds rarely.

## Variants

- **Height-based scapegoat.** Galperin and Rivest also allow the scapegoat to be the deepest ancestor $x$ that is $i$ levels above $u$ with $i > \log_{1/\alpha} \text{size}(x)$. This gives the same bounds.
- **General balanced trees.** Andersson's general balanced trees (1989, journal version 1999) use the same partial rebuilding, with a height criterion, and show a rebuild in linear time and constant extra space.
- **Rebuild in place.** The method of Day, Stout and Warren straightens a subtree into a list by rotations and then folds it into a balanced tree, with $O(1)$ extra space.
- **Order statistics.** Storing subtree sizes makes the scapegoat search cheaper and adds rank and select, as in an [order-statistic tree](/order-statistic-tree/), at the cost of the main advantage.
- **Weight balance kept at all times.** A [weight-balanced tree](/weight-balanced-tree/) keeps every node $\alpha$-weight-balanced with rotations, and so needs sizes in the nodes but no rebuilds.

## When to use it

Use a scapegoat tree when nodes must be small, with no balance field, or when a node layout is fixed by someone else; when restructuring by rotation is awkward but rebuilding is easy, as for trees with large per-subtree data such as range trees and other multi-level structures, where a rotation would need its secondary structures rebuilt anyway; and when amortized bounds are enough. Avoid it when each update needs a worst-case bound, as in real-time systems, or when the tree is persistent, where a rebuild copies many nodes.

## Pitfalls

- **Sizes stored in the nodes by mistake.** The point of the tree is that nodes hold only a key and two pointers; the sizes on the path are counted during the scapegoat search, and this counting is already paid for.
- **Comparing with $n$ instead of $q$.** The depth test of line L3 uses $q$. With $n$, a long series of deletions without a full rebuild could leave the bound and the analysis out of step.
- **Forgetting the full rebuild on deletion.** Without line L8, deletions can make $n$ much smaller than $q$, and the height bound $\log_{1/\alpha} q$ then says nothing useful about $n$.
- **Floating-point logarithms.** Computing $\log_{1/\alpha} q$ in floating point can give the wrong answer when $(1/\alpha)^d$ is close to $q$. Compare $(1/\alpha)^d$ with $q$ in exact arithmetic, or compare with an integer threshold that is updated with $q$.
- **Off-by-one in BUILD.** The middle index must split the range so that the two sides differ by at most one; any such rule works, but the rule changes the shapes, so tests that check exact shapes must use the same rule. The code here takes $\lfloor (lo + hi)/2 \rfloor$.
- **Deep recursion in REBUILD.** A recursive in-order walk of the subtree to rebuild can be deep, up to $\log_{1/\alpha} q$ levels, which grows fast as $\alpha$ nears 1; an explicit stack avoids the limit.

## Implementations

## History

Rebuilding a whole subtree when it gets out of shape is the idea of *partial rebuilding*, which Mark Overmars used in the early 1980s for dynamic geometric data structures. Arne Andersson applied it to binary search trees in "Improving partial rebuilding by using simple balance criteria" (WADS 1989), with a height criterion and no data in the nodes, and later published the full method as general balanced trees (1999). Igal Galperin and Ronald Rivest found the method independently and published it as scapegoat trees at SODA 1993, with the weight criterion, the amortized analysis, and the name. Pat Morin's Open Data Structures presents the version with the counter $q$ and $\alpha = 2/3$ that most textbooks now follow.

## References
