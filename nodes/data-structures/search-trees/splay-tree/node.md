---
tag: MX6QFK
kind: data-structure
slug: splay-tree
name: Splay tree
aliases:
- self-adjusting binary search tree
area: data-structures/search-trees
level: advanced
summary: Self-adjusting BST that splays every accessed key to the root; amortized O(log n) per operation.
implements: [ordered-set, ordered-symbol-table, dictionary]
model: comparison-model
complexity:
  vars: {n: the number of keys}
  time: {amortized: O(log n), worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [binary-search-tree, splaying, potential-method]
see_also: [static-optimality-theorem, working-set-theorem, dynamic-optimality-conjecture, tango-tree, link-cut-tree, red-black-tree, treap, move-to-front]
sources:
  - paper: doi:10.1145/3828.3835
    title: Daniel D. Sleator and Robert E. Tarjan, Self-adjusting binary search trees, Journal of the ACM 32(3), 1985
    locator: Section 2 (Lemma 1, the Access Lemma; Theorem 1, Balance; Theorem 2, Static Optimality; Theorem 3, Static Finger; Theorem 4, Working Set), Section 3 (update operations, join and split), Section 4 (top-down splaying)
  - paper: doi:10.1007/bf02579253
    title: Robert E. Tarjan, Sequential access in splay trees takes linear time, Combinatorica 5(4), 1985
    locator: pages 367 to 378
  - paper: doi:10.1137/s0097539797326988
    title: Richard Cole, Bud Mishra, Jeanette Schmidt and Alan Siegel, On the dynamic finger conjecture for splay trees, Part I, SIAM Journal on Computing 30(1), 2000
    locator: pages 1 to 43
  - paper: doi:10.1137/s009753979732699x
    title: Richard Cole, On the dynamic finger conjecture for splay trees, Part II, SIAM Journal on Computing 30(1), 2000
    locator: pages 44 to 85
---

A splay tree is a [binary search tree](/binary-search-tree/) that keeps no balance information and instead, after each access, moves the accessed node to the root by [splaying](/splaying/). A single operation can take $\Theta(n)$ time, but each sequence of $m$ operations on a tree of at most $n$ keys takes $O((m + n) \log n)$ time, so the [amortized cost](/amortized-cost/) is $O(\log n)$. Sleator and Tarjan (1985) introduced it and proved much more: a splay tree is as good as the best static tree for the access frequencies ([static optimality](/static-optimality-theorem/)), and fast on accesses to recently used keys ([working set](/working-set-theorem/)). Whether it is within a constant factor of every binary search tree algorithm is the [dynamic optimality conjecture](/dynamic-optimality-conjecture/).

## In plain words

A splay tree is a search tree that rearranges itself each time you use it. Whenever you look for a key, the tree pulls that key up to the top, with a few local turns that also pull the other keys on the way up closer to the top.

So keys you use often or used recently stay near the top and are fast to find. A key you have not used for a long time can sink deep, and finding it once can be slow, but that slow search also repairs the tree. Over many operations the average cost is never worse than for a balanced tree, and it is often much better.

## The abstract type

A splay tree implements an [ordered set](/ordered-set/) or an [ordered symbol table](/ordered-symbol-table/): search, insert, delete, minimum, maximum, floor, ceiling and iteration in order. It also has split (cut the set at a key into the smaller and the larger keys) and join (concatenate two sets whose keys do not overlap) in $O(\log n)$ amortized time. Each operation, including a search, changes the tree.

## Representation

Each node has a key, a value, left and right children and a parent pointer. There are no extra fields.

**Invariant.** The tree has the strict [binary search tree property](/binary-search-tree-property/), and parent and child pointers agree. Nothing constrains the shape: any BST on the keys is a valid splay tree.

## Operations

All operations use SPLAY$(T, x)$ from [splaying](/splaying/), which moves $x$ to the root by zig, zig-zig and zig-zag steps.

```pseudo id=main
ACCESS(T, k)                       ▷ splay k, or the last node of its search path
L1  x ← T.root; last ← NIL
L2  while x ≠ NIL and x.key ≠ k do last ← x; x ← (x.left if k < x.key else x.right)
L3  if x = NIL then x ← last
L4  if x ≠ NIL then SPLAY(T, x)
L5  return T.root if T.root ≠ NIL and T.root.key = k else NIL

INSERT(T, k)
L6  if T.root = NIL then T.root ← a node (k); return
L7  if ACCESS(T, k) ≠ NIL then return       ▷ already present; r = T.root is now the floor or ceiling of k
L8  z ← a node (k); r ← T.root
L9  if k < r.key then z.left ← r.left; z.right ← r; r.left ← NIL
L10 else z.right ← r.right; z.left ← r; r.right ← NIL
L11 set the parents of the children of z to z; T.root ← z

DELETE(T, k)
L12 if ACCESS(T, k) = NIL then return false
L13 L ← T.root.left; R ← T.root.right; detach both from the root
L14 T.root ← JOIN(L, R); return true

JOIN(L, R)                         ▷ every key of L is less than every key of R
L15 if L = NIL then return R
L16 m ← the maximum of L; SPLAY(L, m)       ▷ now m is the root of L and has no right child
L17 m.right ← R; R.p ← m; return m

SPLIT(T, k)                        ▷ into the keys ≤ k and the keys > k
L18 ACCESS(T, k); r ← T.root
L19 if r.key ≤ k then return (r without its right subtree, r.right)
L20 else return (r.left, r without its left subtree)
```

**Access.** Search as in a BST, then splay the node found, or the last node visited if the key is absent (line L3). The splay of a miss is needed for the amortized bound, and it puts the floor or the ceiling of $k$ at the root.

**Insert.** After ACCESS, the root $r$ is the floor or the ceiling of $k$. If $k < r.key$, all keys of the left subtree of $r$ are less than $k$ (they are less than $r.key$, and $r$ is the smallest key above $k$), so the new node $z$ takes them as its left subtree and $r$, with its right subtree, as its right subtree. This is a split at $k$ followed by making $z$ the root. A leaf insert followed by a splay of the new node, as in the Python code of [splaying](/splaying/), also works.

**Delete.** Splay $k$ to the root, remove it, and join its two subtrees: splay the maximum of the left subtree, which then has no right child, and hang the right subtree there.

**Split and join.** Split splays $k$ (or its neighbour) to the root and cuts one link of the root. Join is lines L15 to L17.

## Example

Insert 1, 2, 3, 4, 5, 6, 7 in this order. Each insert splays the previous root, which holds the largest key, and the new key becomes the root with the old tree as its left subtree. The result is a chain to the left: 7, 6, 5, 4, 3, 2, 1, of height 6.

Now search for 1. It is at depth 6, so the search makes 7 comparisons, and the splay makes 6 rotations (three zig-zigs). The tree becomes

```
    1
     \
      6
     / \
    4   7
   / \
  2   5
   \
    3
```

of height 4. A search for 3 now finds it at depth 4 and splays it with two zig-zags, 4 rotations, which gives root 3 with left subtree $1(-, 2)$ and right subtree $6(4(-, 5), 7)$. Deleting 3 then removes the root and joins its two subtrees $\{1, 2\}$ and $\{4, 5, 6, 7\}$: the maximum 2 of the left subtree is splayed to its root, and the right subtree hangs below it, so the new root is 2 with left child 1 and right child 6. The in-order sequence is $1, 2, 4, 5, 6, 7$.

The first search was slow: 7 comparisons on 7 keys. But the inserts were cheap (each splayed the root, at cost 0), so the total cost of the 8 operations is small. This is the amortized bound at work.

## Correctness

Splaying keeps the BST property and the in-order sequence. In INSERT, the root $r$ after ACCESS is the floor or the ceiling of $k$ (Lemma 2 of the proof), so the subtree that $z$ takes on each side holds exactly the keys on that side of $k$. In JOIN, the maximum of $L$ has no right child after it is splayed, and all keys of $R$ are larger than it. In SPLIT, after ACCESS the root separates the keys $\le k$ from the keys $> k$ along one link. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | amortized time | worst case |
|---|---|---|
| search (access), floor, ceiling | $O(\log n)$ | $\Theta(n)$ |
| insert, delete | $O(\log n)$ | $\Theta(n)$ |
| split, join | $O(\log n)$ | $\Theta(n)$ |
| minimum, maximum | $O(\log n)$ | $\Theta(n)$ |
| $m$ operations from a tree of $n$ keys | $O((m + n)\log n)$ total | |
| space | $\Theta(n)$ | |

The analysis uses the [potential method](/potential-method/) with weights $w(i) > 0$, sizes $s(x)$ (the total weight in the subtree of $x$), ranks $r(x) = \lg s(x)$ and the potential $\Phi = \sum_x r(x)$. The **Access Lemma** (Sleator and Tarjan, Lemma 1) bounds the amortized number of rotations of a splay of $x$ in a tree with root $t$ by $3(r(t) - r(x)) + 1$; it is proved on the [splaying](/splaying/) page. With unit weights it gives $3 \lg n + 1$ per splay, and the updates add at most $O(\log n)$ potential each. The proof is in [the complexity proof](proofs/complexity.md).

With other weights, the same lemma gives the theorems of Sleator and Tarjan for a sequence of $m$ accesses to $n$ keys, where each item is accessed at least once:

- **Balance (Theorem 1).** $O((m + n) \log n + m)$ total.
- **Static optimality (Theorem 2).** $O(m + \sum_i q(i) \lg(m/q(i)))$, where $q(i)$ is the number of accesses to item $i$. This is the cost of the best static tree up to a constant factor. See the [static optimality theorem](/static-optimality-theorem/).
- **Static finger (Theorem 3).** For each fixed key $f$, $O(n \log n + m + \sum_j \lg(|i_j - f| + 1))$, where $i_j$ is the rank of the $j$-th access.
- **Working set (Theorem 4).** $O(n \log n + m + \sum_j \lg(t(j) + 1))$, where $t(j)$ is the number of distinct items accessed since the last access to the item of access $j$. See the [working set theorem](/working-set-theorem/).

Later results: the **sequential access theorem** (Tarjan 1985) says that accessing all $n$ keys in increasing order costs $O(n)$; the **dynamic finger theorem** (Cole, with Mishra, Schmidt and Siegel, 2000) says that the cost is $O(m + n + \sum_j \lg(|i_j - i_{j-1}| + 1))$.

## Variants

- **Top-down splay trees.** Splay during the search, splitting the path into a left tree and a right tree, then join them. Sleator and Tarjan give this form in Section 4; it needs no parent pointers and is the usual implementation.
- **Semi-splay trees.** Do fewer rotations per step, with the same asymptotic bounds.
- **Splaying only sometimes.** Splay only on every $k$-th access, or only when the path is long. These reduce the writes for read-heavy loads.
- **Augmented splay trees.** Subtree sizes or sums kept after each rotation, as in [augmenting data structures](/augmenting-data-structures/), give rank, select and range sums in $O(\log n)$ amortized time.
- **Link-cut trees.** [Link-cut trees](/link-cut-tree/) of Sleator and Tarjan keep each path of a dynamic forest in a splay tree.

## When to use it

Use a splay tree when the access pattern has locality, such as caches, routing tables that see a few hot destinations, or sequences of nearby keys, and when amortized bounds are enough. It needs no balance fields and is short to code, and it gives split and join for free, which makes it a good base for sequences with cut and paste and for [link-cut trees](/link-cut-tree/). Avoid it for real-time code that needs a bound on each operation, for trees read by many threads at once (each read writes), and for workloads with no locality, where its rotations make it slower than a [red-black tree](/red-black-tree/).

## Pitfalls

- **Not splaying on a miss.** If an unsuccessful search does not splay, an adversary can repeat a deep miss and cost $\Theta(n)$ each time.
- **Using rotate-to-root.** Single rotations to the root instead of the zig-zig rule lose the amortized bound.
- **Expecting worst-case bounds.** One operation can cost $\Theta(n)$, for example the first search for the smallest key after sorted inserts. A server with a deadline per request can miss it.
- **Recursion depth.** A recursive splay or a recursive walk can overflow the stack on a deep tree; the tree can be a chain of depth $n - 1$.
- **Concurrent readers.** Readers change the tree, so a splay tree cannot be shared between threads without a lock, even for searches.
- **Iterators and splaying.** An iterator that holds a node while other operations splay sees the tree change below it; use the in-order successor by parent pointers, or splay each successor.

## Implementations

The Python class follows the main block with bottom-up splaying and parent pointers. It has access, insert, delete, split, join, minimum and floor, a counter of rotations used by the tests, and a check of the BST order and the parent links.

## History

Sleator and Tarjan introduced splay trees in 1985, with the Access Lemma and the balance, static optimality, static finger and working set theorems, and stated the dynamic optimality conjecture. Tarjan proved the sequential access theorem in the same year. Cole, with Mishra, Schmidt and Siegel, proved the dynamic finger theorem in two papers in 2000.

## References
