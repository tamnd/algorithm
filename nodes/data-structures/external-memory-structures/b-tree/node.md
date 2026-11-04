---
tag: KEZ9RE
kind: data-structure
slug: b-tree
name: B-tree
aliases:
- Definition of B-trees
- B-TREE-INSERT
area: data-structures/external-memory-structures
level: core
summary: Balanced multiway search tree whose nodes hold many keys, designed to minimize disk accesses in large stored datasets.
implements: [dictionary]
model: external-memory-model
prereqs: [binary-search-tree, external-memory-model, asymptotic-notation]
see_also: [b-plus-tree, b-star-tree, external-searching, red-black-correspondence-with-2-3-4-trees, bulk-loading-b-tree, buffer-tree, b-epsilon-tree, cache-oblivious-b-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 18, Section 18.1 (definition and Theorem 18.1, the height bound), Section 18.2 (search, split and insert) and Section 18.3 (deletion)
  - paper: doi:10.1007/BF00288683
    title: "Rudolf Bayer and Edward M. McCreight, Organization and maintenance of large ordered indexes, Acta Informatica 1(3) (1972)"
    locator: pp. 173 to 189
  - paper: doi:10.1145/356770.356776
    title: "Douglas Comer, The ubiquitous B-tree, ACM Computing Surveys 11(2) (1979)"
    locator: pp. 121 to 137
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.4, Multiway trees
---

A B-tree is a balanced search tree in which each node holds many sorted keys and has one more child than keys, and all leaves are at the same depth. With a minimum degree $t \ge 2$, each node other than the root has between $t - 1$ and $2t - 1$ keys, so a tree with $n$ keys has height at most $\log_t \frac{n+1}{2}$. Search, insert and delete each visit one node per level. When one node fills one disk block, so that $t = \Theta(B)$ in the [external memory model](/external-memory-model/), each operation costs $O(\log_B n)$ block transfers, which is optimal for comparison-based [external searching](/external-searching/). It is the standard index of file systems and databases.

## In plain words

A [binary search tree](/binary-search-tree/) chooses between two ways at each node. On a disk, each node you visit can cost a slow read, and a binary tree with a billion keys has about thirty levels.

A B-tree makes each node as big as one disk block. A node holds hundreds of sorted keys, and between two neighbouring keys is a pointer to a child that holds the keys in that gap. So one read chooses among hundreds of ways, and a billion keys fit in three or four levels.

The tree stays balanced in a simple way. A node that gets too full splits into two halves and pushes its middle key up to its parent. A node that gets too empty borrows a key from a neighbour or joins with it. The tree grows and shrinks only at the root, so all leaves stay at the same depth.

## The abstract type

A B-tree implements the [dictionary](/dictionary/) on keys from a total order: `search(T, k)`, `insert(T, k)` and `delete(T, k)`. Because the keys are kept in order, it also gives the operations of an [ordered set](/ordered-set/): minimum, maximum, predecessor, successor and a range query that lists the keys between two bounds. On this page the keys are distinct. A record that goes with a key is stored next to the key, or the key holds a pointer to it.

## Representation

The tree has a minimum degree $t \ge 2$ and a pointer $T.root$. Each node $x$ has a number of keys $x.n$, keys $x.key[1 \ldots x.n]$, a flag $x.leaf$, and, if $x$ is internal, $x.n + 1$ child pointers $x.c[1 \ldots x.n+1]$. The tree satisfies four properties at each node $x$:

- **(B1) Order in a node.** $x.key[1] < x.key[2] < \cdots < x.key[x.n]$, and $x.n \le 2t - 1$.
- **(B2) Search order.** If $k_i$ is any key in the subtree of $x.c[i]$, then $k_1 < x.key[1] < k_2 < x.key[2] < \cdots < x.key[x.n] < k_{x.n+1}$.
- **(B3) Balance.** All leaves have the same depth, the height $h$ of the tree.
- **(B4) Fill.** Each node other than the root has at least $t - 1$ keys. A non-empty tree has at least one key at the root.

A node with $2t - 1$ keys is *full*. The case $t = 2$ allows 2, 3 or 4 children per internal node and is the 2-3-4 tree.

**The disk model.** Each node is stored in one disk block, and DISK-READ and DISK-WRITE move one node between the disk and the memory. The cost of an operation is the number of these calls. The root stays in memory, so it costs no read. Choose $t$ so that a full node fills a block: with keys and pointers of 8 bytes each and blocks of 16 KB, $t = 512$ gives $1023 \cdot 8 + 1024 \cdot 8 = 16376$ bytes per node. In terms of the block size $B$, counted in keys and pointers, $t = \Theta(B)$.

## Operations

The main block holds the search and the insertion. Insertion goes down from the root once. Before it enters a full node, it splits that node, so the parent of a split always has room for the middle key. This is the *top-down* or *proactive* insertion of CLRS.

```pseudo id=main
B-TREE-SEARCH(x, k)                        ▷ returns (node, index), or NIL
L1  i ← 1
L2  while i ≤ x.n and k > x.key[i] do i ← i + 1
L3  if i ≤ x.n and k = x.key[i] then return (x, i)
L4  if x.leaf then return NIL
L5  DISK-READ(x.c[i])
L6  return B-TREE-SEARCH(x.c[i], k)

B-TREE-INSERT(T, k)                        ▷ k is not in T
L7  r ← T.root
L8  if r.n = 2t − 1 then                   ▷ a full root: the tree grows by one level
L9      s ← a new node, s.leaf ← false, s.n ← 0, s.c[1] ← r
L10     T.root ← s
L11     SPLIT-CHILD(s, 1)
L12     r ← s
L13 INSERT-NONFULL(r, k)

SPLIT-CHILD(x, i)                          ▷ x is not full and y = x.c[i] is full
L14 y ← x.c[i], z ← a new node, z.leaf ← y.leaf, z.n ← t − 1
L15 z.key[1 .. t − 1] ← y.key[t + 1 .. 2t − 1]
L16 if not y.leaf then z.c[1 .. t] ← y.c[t + 1 .. 2t]
L17 y.n ← t − 1                            ▷ y keeps key[1 .. t − 1]; y.key[t] goes up
L18 shift x.c[i + 1 .. x.n + 1] and x.key[i .. x.n] one place to the right
L19 x.c[i + 1] ← z, x.key[i] ← y.key[t], x.n ← x.n + 1
L20 DISK-WRITE(y), DISK-WRITE(z), DISK-WRITE(x)

INSERT-NONFULL(x, k)                       ▷ x is not full
L21 i ← x.n
L22 if x.leaf then
L23     while i ≥ 1 and k < x.key[i] do x.key[i + 1] ← x.key[i], i ← i − 1
L24     x.key[i + 1] ← k, x.n ← x.n + 1, DISK-WRITE(x), return
L25 while i ≥ 1 and k < x.key[i] do i ← i − 1
L26 i ← i + 1, DISK-READ(x.c[i])
L27 if x.c[i].n = 2t − 1 then
L28     SPLIT-CHILD(x, i)
L29     if k > x.key[i] then i ← i + 1
L30 INSERT-NONFULL(x.c[i], k)
```

SEARCH scans the keys of a node until it finds the first key that is at least $k$ (line L2). Either that key is $k$, or the search goes down into the gap just left of it. A binary search in the node gives the same index with $O(\log t)$ comparisons instead of $O(t)$. SPLIT-CHILD cuts a full node of $2t - 1$ keys into two nodes of $t - 1$ keys and moves the middle key up into the parent. A split at the root (lines L8 to L12) is the only way the height grows. A new key always goes into a leaf (line L24).

**Deletion.** Deletion also goes down once. Before it enters a child with only $t - 1$ keys, it gives that child a key more, so that a key can later be removed from it without breaking (B4). The call starts at the root.

```pseudo id=delete
B-TREE-DELETE(x, k)                        ▷ x is the root, or x has at least t keys
L31 i ← the least index with k ≤ x.key[i], or x.n + 1 if there is none
L32 if i ≤ x.n and k = x.key[i] then
L33     if x.leaf then remove x.key[i] from x, DISK-WRITE(x), return       ▷ case 1
L34     y ← x.c[i], z ← x.c[i + 1]
L35     if y.n ≥ t then k′ ← the largest key below y, x.key[i] ← k′, B-TREE-DELETE(y, k′)       ▷ case 2a
L36     else if z.n ≥ t then k′ ← the smallest key below z, x.key[i] ← k′, B-TREE-DELETE(z, k′)  ▷ case 2b
L37     else move k and all of z to the end of y, remove z from x, B-TREE-DELETE(y, k)  ▷ case 2c
L38 else if x.leaf then return             ▷ k is not in the tree
L39 else if x.c[i].n = t − 1 then          ▷ case 3: give the child one key more
L40     if a neighbour sibling of x.c[i] has t keys or more then rotate one key from it through x   ▷ case 3a
L41     else merge x.c[i], the key of x between them and a neighbour sibling, and let x.c[i] be the result  ▷ case 3b
L42     B-TREE-DELETE(x.c[i], k)
```

After the call, if the root is internal and has no key left, its only child becomes the new root. This is the only way the height drops. Cases 2a and 2b replace $k$ by its predecessor or its successor, which lies in a leaf, and then delete that key below. In case 3a the key of $x$ between the child and its sibling moves down into the child, and the nearest key of the sibling moves up in its place, with the child pointer at that end of the sibling.

**Other operations.** The minimum is the first key of the leftmost leaf, found by following $c[1]$ from the root, and the maximum is the mirror image. A range query for the keys in $[a, b]$ searches for $a$ and then walks the tree in order until it passes $b$, with the path from the root kept in memory.

## Example

Take $t = 2$, so each node has 1 to 3 keys. Insert $8, 3, 12, 5, 1, 9, 15, 7, 4, 10$ into an empty tree. The table writes a node as its keys in brackets, followed by its children in parentheses.

| step | the tree after it |
|---|---|
| insert 8, 3, 12 | [3 8 12] |
| insert 5 | the root is full: split it. [8]([3 5] [12]) |
| insert 1, 9, 15 | [8]([1 3 5] [9 12 15]) |
| insert 7 | the child [1 3 5] is full: split it. [3 8]([1] [5 7] [9 12 15]) |
| insert 4 | [3 8]([1] [4 5 7] [9 12 15]) |
| insert 10 | the child [9 12 15] is full: split it. [3 8 12]([1] [4 5 7] [9 10] [15]) |

Now delete $12, 3, 8, 9, 4, 7$.

| step | case | the tree after it |
|---|---|---|
| delete 12 | 2a: the left child [9 10] has 2 keys, so 12 becomes its predecessor 10 | [3 8 10]([1] [4 5 7] [9] [15]) |
| delete 3 | 2b: [1] has 1 key and [4 5 7] has 3, so 3 becomes its successor 4 | [4 8 10]([1] [5 7] [9] [15]) |
| delete 8 | 2a: 8 becomes 7 from [5 7] | [4 7 10]([1] [5] [9] [15]) |
| delete 9 | 3b: [9] and both its siblings have 1 key, so [9] merges with 10 and [15] | [4 7]([1] [5] [10 15]) |
| delete 4 | 2c: [1] and [5] have 1 key each, so they merge with 4 into [1 4 5] | [7]([1 5] [10 15]) |
| delete 7 | 2a: 7 becomes 5 from [1 5] | [5]([1] [10 15]) |

The insertion of 5 shows the only way the height grows. In the deletion of 9, the search goes into [9] but first fixes it, because a leaf with $t - 1 = 1$ key cannot lose a key.

## Correctness

Each operation keeps (B1) to (B4). SPLIT-CHILD is called only on a full child of a parent that is not full, so the parent gains a key and stays within $2t - 1$, and the two halves have $t - 1$ keys each. INSERT-NONFULL is called only on nodes that are not full, so the leaf that gets the new key has room. DELETE enters a node only when it is the root or has at least $t$ keys, and it removes at most one key from each node it enters, so no node drops below $t - 1$. Splits, rotations and merges keep the in-order sequence of the keys and the depth of every leaf. The full proof, with the cases of deletion, is below.

## Complexity

**Height.** Let a B-tree with $n \ge 1$ keys have height $h$. The root has at least 1 key and 2 children if $h \ge 1$. Each other node has at least $t - 1$ keys and, if internal, at least $t$ children. So there are at least $2t^{d-1}$ nodes at depth $d$ for $1 \le d \le h$, and

$$n \ \ge\ 1 + (t-1)\sum_{d=1}^{h} 2t^{d-1} \ =\ 1 + 2(t^h - 1) \ =\ 2t^h - 1, \qquad\text{so}\qquad h \le \log_t\frac{n+1}{2}.$$

This is Theorem 18.1 of CLRS. The bound is tight: the tree in which every node has the least number of keys has exactly $2t^h - 1$ keys.

Each operation visits $O(1)$ nodes on each level, so with $h = O(\log_t n)$:

| operation | disk reads and writes | CPU time |
|---|---|---|
| search | at most $h$ reads | $O(t h)$, or $O(h \log t)$ with binary search in a node |
| insert | at most $h + 1$ reads, at most $3h + 4$ writes | $O(t h)$ |
| delete | $O(h)$ reads and writes | $O(t h)$ |
| minimum, maximum | $h$ reads | $O(h)$ |
| range query with $Z$ answers | $O(h + Z/t)$ reads | $O(t h + Z)$ |

The space is $O(n/t)$ nodes of $\Theta(t)$ words each, so $O(n)$ words. Each node other than the root is at least about half full.

**In the external memory model.** With $t = \Theta(B)$, all operations above cost $O(\log_B n)$ I/Os, and the range query costs $O(\log_B n + Z/B)$. The [external memory model](/external-memory-model/) page proves that a comparison-based search needs at least $\log_{B+1}(n+1)$ reads, so the B-tree is optimal for single searches. For $n = 10^9$ and $t = 512$, $\log_{512}\frac{n+1}{2} \approx 3.21$, so $h \le 3$ and a search reads at most 3 nodes besides the root. A balanced binary tree on the same keys has about $\lg n \approx 30$ levels.

**Splits are rare.** In a sequence of $n$ insertions into an empty tree, each split adds one node, or two at the root, so the number of splits is less than the number of nodes. A tree with $p$ nodes has $n \ge 1 + (p - 1)(t - 1)$ keys by (B4), so there are at most $(n - 1)/(t - 1)$ splits in total, which is $O(1/t)$ amortized per insertion.

## Variants

- **B+ tree.** All records are in the leaves, the internal nodes hold only copies of keys to guide the search, and the leaves are linked for fast range scans. This is the form most databases use. See [B+ tree](/b-plus-tree/).
- **B\*-tree.** A full node first shares keys with a sibling, and two full siblings split into three nodes, so nodes stay at least two thirds full. See [B\*-tree](/b-star-tree/).
- **Order instead of minimum degree.** Knuth defines a B-tree of order $m$: each node has at most $m$ children, and each node other than the root and the leaves has at least $\lceil m/2 \rceil$. An order $m = 2t$ gives the trees of this page. An odd $m$ has no $t$, and top-down splitting needs extra care there.
- **Bottom-up insertion.** Bayer and McCreight insert into the leaf first and split overflowing nodes on the way back up, with the path kept on a stack. It splits only when necessary, but it needs the path.
- **2-3-4 trees and red-black trees.** The case $t = 2$ is a 2-3-4 tree, and a [red-black tree](/red-black-tree/) is a binary form of it. See [red-black correspondence with 2-3-4 trees](/red-black-correspondence-with-2-3-4-trees/).
- **Bulk loading.** Building a tree from sorted keys bottom-up, level by level, costs $O(n/B)$ I/Os instead of $O(n \log_B n)$. See [bulk loading a B-tree](/bulk-loading-b-tree/).
- **Concurrent B-trees.** The [B-link tree](/blink-tree/) adds right-sibling pointers so that readers need no locks during a split.
- **Write-optimized trees.** The [buffer tree](/buffer-tree/), the [B^ε-tree](/b-epsilon-tree/) and the [log-structured merge tree](/log-structured-merge-tree/) make updates much cheaper than $\Theta(\log_B n)$ I/Os, at some cost to queries.
- **Cache-oblivious B-tree.** The [cache-oblivious B-tree](/cache-oblivious-b-tree/) has the same $O(\log_B n)$ search cost without knowing $B$.

## When to use it

Use a B-tree, usually as a B+ tree, for an ordered index on data that does not fit in memory: it gives searches, updates and range queries in a few disk reads each, and it keeps good worst-case bounds. In memory, a B-tree with nodes of one or a few cache lines is often faster than a binary tree, because it misses the cache less. If the work is a large batch of updates whose answers can wait, sorting or a [buffer tree](/buffer-tree/) is cheaper: $n$ B-tree insertions cost $\Theta(n \log_B n)$ I/Os, which is far more than the sort bound. For exact-match lookups only, a hash table on disk needs $O(1)$ expected I/Os.

## Pitfalls

- **The two conventions for the size of a node.** CLRS uses the minimum degree $t$ (at most $2t - 1$ keys), Knuth uses the order $m$ (at most $m$ children). Mixing them gives nodes that are off by one, and a "B-tree of order 3" is a 2-3 tree, not a tree with $t = 3$.
- **Splitting too late.** If the insertion goes down to the leaf first and splits only there, a full parent has no room for the middle key. Either split full nodes on the way down (line L27) or keep the path and split upward.
- **The root rules.** The root may have only one key, the height grows only by a root split (line L8), and it drops only when the root loses its last key. Forgetting the second step leaves an empty internal root.
- **Deleting a key from an internal node.** Removing $x.key[i]$ from an internal node leaves two children with one gap between them. Replace it by its predecessor or successor (lines L35 and L36), or merge the two children (line L37).
- **Duplicate keys.** Property (B2) uses $<$. With equal keys, the inequalities must become $\le$ and a search for all copies must look in more than one child. Store a list of records per key instead, or make the keys distinct by adding a record id.
- **Bytes against keys.** The block size $B$ in the bounds counts keys and pointers, not bytes. A 4 KB block with 16-byte keys and 8-byte pointers holds about 170 keys, not 4096.

## Implementations

## History

Rudolf Bayer and Edward McCreight invented the B-tree at the Boeing Scientific Research Laboratories, and published it in Acta Informatica in 1972. Their paper analyses the cost of searches and updates on an index stored on a disk with random access. By 1979, when Comer wrote his survey "The ubiquitous B-tree", B-trees and the B+ tree variant were the standard way to organize indexes in databases and file systems. Comer reports that the authors never explained the letter B. Knuth treats B-trees in Section 6.2.4 of his third volume, and CLRS gives the top-down insertion and deletion of this page in Chapter 18.

## References
