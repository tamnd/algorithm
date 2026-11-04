---
tag: M7WT2F
kind: data-structure
slug: b-plus-tree
name: B+ tree
aliases:
- B+-tree
area: data-structures/external-memory-structures
level: core
summary: B-tree variant that stores all keys in linked leaves, giving fast range scans and high fanout.
implements: [ordered-set]
model: external-memory-model
prereqs: [b-tree, external-memory-model]
see_also: [b-star-tree, external-searching, bulk-loading-b-tree, blink-tree, clustered-index, b-epsilon-tree, log-structured-merge-tree, string-b-tree]
sources:
  - paper: doi:10.1145/356770.356776
    title: "Douglas Comer, The ubiquitous B-tree, ACM Computing Surveys 11(2) (1979)"
    locator: pp. 121 to 137, the sections on the B+-tree and on VSAM
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition
    locator: Chapter 10, Tree-Structured Indexing (the order d, search, insert with copy-up and push-up, delete with redistribution and merge)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 18.1 (the B+-tree as the variant that keeps satellite data in the leaves)
---

A B+ tree is a [B-tree](/b-tree/) in which all keys, with their records, are in the leaves, the internal nodes hold only *separators* that guide the search, and the leaves are linked from left to right. With an order $d \ge 1$, each node other than the root holds $d$ to $2d$ keys or separators. A search, an insertion and a deletion each read one node per level, $O(\log_d n)$ nodes, and a range query that reports $Z$ keys reads $O(\log_d n + Z/d)$ nodes. Because internal nodes hold no records, they have a higher fanout than in a B-tree with records, and the linked leaves make a range scan a sequential read. It is the index structure of most relational databases and of many file systems.

## In plain words

Think of a large dictionary printed on many pages. Every word is on some page, in alphabetical order, and each page ends with "continued on the next page". In front of the pages is a small guide: "words from A to Ca are on pages 1 to 40", and so on. The guide can have its own guide.

To find a word, you read the guide and jump to the right page. To list all the words between two words, you find the first one and then turn the pages. The guide holds only short labels, not the definitions, so one guide page points to very many pages.

When a page gets too full, it is cut into two pages, and a new label goes into the guide. When a page gets too empty, it takes words from a neighbour or joins it.

## The abstract type

A B+ tree implements the [ordered set](/ordered-set/), and the [dictionary](/dictionary/) as a part of it: `search(T, k)`, `insert(T, k)`, `delete(T, k)`, and `range(T, a, b)`, which returns the keys $k$ with $a \le k \le b$ in increasing order. Minimum, maximum, successor and predecessor follow from the leaf chain. On this page the keys are distinct, and a key stands for the key with its record.

## Representation

The tree has an order $d \ge 1$ and a root pointer. There are two kinds of nodes.

- A *leaf* holds sorted keys $key[1 \ldots m]$ and a pointer $next$ to the leaf to its right, or NIL.
- An *internal node* holds sorted separators $key[1 \ldots m]$ and $m + 1$ children $c[0 \ldots m]$. With $key[0] = -\infty$ and $key[m+1] = +\infty$, the child $c[i]$ holds the keys $k$ with $key[i] \le k < key[i+1]$.

The invariants are:

- **(P1)** Each node has at most $2d$ keys or separators, in increasing order.
- **(P2)** The search order of the internal nodes, as above.
- **(P3)** All leaves have the same depth $h$, the height.
- **(P4)** Each node other than the root has at least $d$ keys or separators. An internal root has at least one separator.
- **(P5)** The leaves are linked by $next$ in increasing order of their keys.

A separator is a copy of a key, or a value left from a key that was deleted later. A key can appear once in a leaf and again as a separator. Ramakrishnan and Gehrke use this definition with the order $d$. Real systems often give leaves and internal nodes different capacities, because a leaf entry holds a record or a record id and an internal entry holds only a key and a pointer.

**The disk model.** Each node is one disk block, and the root stays in memory. The cost is the number of nodes read. With 8-byte keys, 8-byte pointers and 8 KB blocks, an internal node holds up to 511 separators and 512 children, since $511 \cdot 8 + 512 \cdot 8 = 8184$ bytes, so the order $d = 255$ fits.

## Operations

The search goes down to the one leaf that can hold $k$. Insertion goes down to that leaf, inserts, and on the way back up splits each node that has $2d + 1$ entries. A split leaf *copies up* the smallest key of its right half, which stays in the leaf. A split internal node *pushes up* its middle separator, which leaves the lower level.

```pseudo id=main
FIND-LEAF(T, k)                            ▷ the only leaf that can hold k
L1  x ← T.root
L2  while x is not a leaf do
L3      i ← the number of separators of x that are ≤ k
L4      x ← x.c[i], DISK-READ(x)
L5  return x

RANGE(T, a, b)                             ▷ the keys k with a ≤ k ≤ b, in order
L6  x ← FIND-LEAF(T, a), out ← an empty list
L7  loop
L8      for each key k of x in order: if k ≥ a then (if k > b then return out), append k to out
L9      if x.next = NIL then return out
L10     x ← x.next, DISK-READ(x)

BPT-INSERT(T, k)                           ▷ k is not in T
L11 r ← INSERT-REC(T.root, k)
L12 if r ≠ NIL then                        ▷ the root split into the old root and z
L13     (s, z) ← r, T.root ← a new internal node with separator s and children (old root, z)

INSERT-REC(x, k)                           ▷ returns NIL, or (separator, new right sibling)
L14 if x is a leaf then
L15     insert k into x.key in order
L16     if x has at most 2d keys then return NIL
L17     z ← a new leaf with the last d + 1 keys of x; x keeps the first d
L18     z.next ← x.next, x.next ← z
L19     return (z.key[1], z)                ▷ copy up: z.key[1] stays in the leaf z
L20 i ← the number of separators of x that are ≤ k, DISK-READ(x.c[i])
L21 r ← INSERT-REC(x.c[i], k)
L22 if r = NIL then return NIL
L23 (s, z) ← r, insert s into x after x.key[i] and z after x.c[i]
L24 if x has at most 2d separators then return NIL
L25 z′ ← a new internal node with the last d separators and the last d + 1 children of x
L26 s′ ← x.key[d + 1]; x keeps the first d separators and the first d + 1 children
L27 return (s′, z′)                        ▷ push up: s′ is no longer in x or in z′
```

**Deletion.** Deletion removes the key from its leaf and, on the way back up, repairs each child that has dropped to $d - 1$ entries. The repair first tries to borrow one entry from a sibling with more than $d$. If both neighbouring siblings have exactly $d$, it merges the child with one of them.

```pseudo id=delete
BPT-DELETE(T, k)
L28 DELETE-REC(T.root, k)
L29 if T.root is internal and has no separator then T.root ← T.root.c[0]

DELETE-REC(x, k)                           ▷ returns true if x now has fewer than d entries
L30 if x is a leaf then remove k from x if it is there, return (x has fewer than d keys)
L31 i ← the number of separators of x that are ≤ k, DISK-READ(x.c[i])
L32 if not DELETE-REC(x.c[i], k) then return false
L33 FIX-CHILD(x, i)
L34 return (x has fewer than d separators)

FIX-CHILD(x, i)                            ▷ x.c[i] has d − 1 entries
L35 let y be a sibling of x.c[i] next to it, one with more than d entries if there is one
L36 if y has more than d entries then move one entry from y to x.c[i] and reset the separator between them
L37 else merge x.c[i] and y into the left one of them, and remove the separator between them and the right one from x
```

In line L36, for leaves, the moved key goes to the near end of $x.c[i]$, and the separator between the two leaves becomes the smallest key of the right one. For internal nodes, the move is a rotation: the separator of $x$ goes down into $x.c[i]$, the near separator of $y$ goes up in its place, and the near child of $y$ moves to $x.c[i]$. In line L37, two leaves are concatenated and the left one takes the $next$ link of the right one. Two internal nodes are concatenated with the separator of $x$ between them, since that separator is still needed to divide their children.

**Costs of one operation.** Each operation reads one node per level, so it makes at most $h$ reads, plus $O(1)$ reads of siblings per level for a deletion. A node is split or merged at most once per level.

## Example

Take $d = 2$, so each node other than the root holds 2 to 4 entries. A leaf is written in square brackets and an internal node in angle brackets, followed by its children. Insert $20, 5, 40, 10, 30, 15, 25, 35, 45, 50, 12$.

| step | the tree after it |
|---|---|
| insert 20, 5, 40, 10 | [5 10 20 40] |
| insert 30 | the leaf has 5 keys: split into [5 10] and [20 30 40], copy 20 up. <20>([5 10] [20 30 40]) |
| insert 15, 25 | <20>([5 10 15] [20 25 30 40]) |
| insert 35 | split [20 25 30 35 40], copy 30 up. <20 30>([5 10 15] [20 25] [30 35 40]) |
| insert 45, 50 | split [30 35 40 45 50], copy 40 up. <20 30 40>([5 10 15] [20 25] [30 35] [40 45 50]) |
| insert 12 | <20 30 40>([5 10 12 15] [20 25] [30 35] [40 45 50]) |

RANGE(12, 35) goes from the root to the leaf [5 10 12 15], skips 5 and 10, and follows the links through [20 25] and [30 35] to [40 45 50], where 40 stops it. The answer is $12, 15, 20, 25, 30, 35$, with one internal read and four leaf reads.

Now delete $40, 45, 50, 5, 25, 12, 30$.

| step | what happens | the tree after it |
|---|---|---|
| delete 40 | the leaf keeps 2 keys; the separator 40 stays | <20 30 40>([5 10 12 15] [20 25] [30 35] [45 50]) |
| delete 45 | [50] is too small, its sibling [30 35] has exactly 2: merge | <20 30>([5 10 12 15] [20 25] [30 35 50]) |
| delete 50 | | <20 30>([5 10 12 15] [20 25] [30 35]) |
| delete 5 | | <20 30>([10 12 15] [20 25] [30 35]) |
| delete 25 | [20] borrows 15 from [10 12 15]; the separator becomes 15 | <15 30>([10 12] [15 20] [30 35]) |
| delete 12 | [10] merges with [15 20]; the separator 15 goes | <30>([10 15 20] [30 35]) |
| delete 30 | [35] borrows 20 from [10 15 20] | <20>([10 15] [20 35]) |

After the deletion of 40, the separator 40 is no longer a key, and the tree is still valid: the separators only have to divide the key ranges.

## Correctness

The invariant (P2) makes FIND-LEAF reach the only leaf whose range can contain $k$, and every leaf to its left holds only smaller keys. With (P5), RANGE then reads exactly the keys of $[a, b]$, in order. A split cuts a node of $2d + 1$ entries into two nodes of at least $d$ entries, and the returned separator divides their key ranges, so the parent keeps (P2). A borrow keeps the in-order sequence of keys and separators. A merge joins two adjacent ranges into one, and has at most $(d - 1) + d = 2d - 1$ keys for leaves and $(d - 1) + 1 + d = 2d$ separators for internal nodes. The tree changes height only at the root, so all leaves stay at one depth. The full proof is below.

## Complexity

**Height.** Let the tree have $n$ keys and height $h \ge 1$. The root has at least 2 children, each other internal node at least $d + 1$, and each leaf at least $d$ keys. So there are at least $2(d+1)^{h-1}$ leaves and

$$n \ \ge\ 2d\,(d+1)^{h-1}, \qquad\text{so}\qquad h \ \le\ 1 + \log_{d+1}\frac{n}{2d}.$$

| operation | node reads | CPU time |
|---|---|---|
| search | $h$ | $O(h \log d)$ with binary search in a node |
| insert | $h$ | $O(h\, d)$ |
| delete | $O(h)$ | $O(h\, d)$ |
| range query with $Z$ answers | at most $h + Z/d + 2$ | $O(h \log d + Z)$ |
| full scan | $h$ plus the number of leaves, at most $n/d + 1$ | $O(n)$ |

The range bound holds because the leaves strictly between the first and the last leaf visited hold only answers, at least $d$ each. The space is $O(n/d)$ nodes, and $O(n)$ words in total, because each node other than the root is at least half full.

**In the external memory model.** With $d = \Theta(B)$, search and updates cost $O(\log_B n)$ I/Os and a range query costs $O(\log_B n + Z/B)$ I/Os. This is optimal for comparison-based [external searching](/external-searching/) and for reporting. For $n = 10^9$ keys with $d = 256$ (512 entries per node), $h \le 1 + \log_{257}(10^9/512) \approx 3.61$, so $h \le 3$.

**Fanout against a B-tree.** In a [B-tree](/b-tree/) that keeps a 100-byte record with each key, an entry of an internal node takes a key, a record and a child pointer, $8 + 100 + 8 = 116$ bytes, so an 8 KB node holds at most 70 keys and has at most 71 children. A B+ internal node of the same size has up to 512 children. The larger fanout gives a smaller height and lets the internal levels fit in memory.

## Variants

- **Leaves that hold record ids.** In a secondary index the leaves hold pointers to records stored elsewhere, and a [clustered index](/clustered-index/) stores the records themselves in the leaves in key order.
- **Prefix B+ tree.** Separators only need to divide two neighbouring leaves, so the shortest prefix that does so is enough. This raises the fanout for string keys. The [string B-tree](/string-b-tree/) takes the idea further.
- **Splitting as in the B\*-tree.** A full node first shifts entries into a sibling, and splits two full nodes into three. See the [B\*-tree](/b-star-tree/).
- **Bulk loading.** Sort the keys, fill the leaves left to right, and build each internal level from the level below. See [bulk loading a B-tree](/bulk-loading-b-tree/).
- **B-link tree.** Each internal node also has a right link, as the leaves do, so that a search can recover from a concurrent split. See [B-link tree](/blink-tree/).
- **Lazy deletion.** Many systems do not merge nodes on deletion and free a node only when it becomes empty. They give up the fill invariant (P4), and with it the space bound, for simpler code and less locking.
- **Write-optimized trees.** The [B^ε-tree](/b-epsilon-tree/) and the [log-structured merge tree](/log-structured-merge-tree/) trade some query cost for much cheaper inserts.

## When to use it

Use a B+ tree for a disk-resident ordered index with a mix of point queries, range queries and updates. It is the default index of database systems: point queries cost a few reads, and the leaf chain makes range queries and full scans sequential. A plain B-tree saves a little space because each key is stored once, but it has a lower fanout when records are large, and range scans must climb back up the tree. When inserts dominate and queries are rare, a [log-structured merge tree](/log-structured-merge-tree/) or a [B^ε-tree](/b-epsilon-tree/) is cheaper.

## Pitfalls

- **Copy up against push up.** A leaf split copies the smallest key of the right leaf up and keeps it in the leaf (line L19). An internal split pushes the middle separator up and removes it from both halves (lines L25 and L26). Removing the key from the leaf loses a record, and keeping the separator in an internal half breaks the count of children.
- **The direction of ties.** With the convention $key[i] \le k < key[i+1]$, a key equal to a separator goes to the right child (line L3 counts separators $\le k$). A search that uses $<$ in one place and $\le$ in another misses keys equal to separators.
- **Updating the separator after a borrow.** When a leaf borrows from its right sibling, the separator between them must become the new smallest key of the right sibling. Keeping the old separator leaves the moved key on the wrong side.
- **The leaf chain on a merge.** When two leaves merge, the left one must take the $next$ link of the right one (line L37). A dangling link makes range scans return deleted leaves.
- **Separators that are not keys.** After deletions, a separator may be a value that is no longer in the tree. Code that answers a search from the internal nodes, without going to a leaf, gives wrong answers.

## Implementations

## History

Comer's survey of 1979 describes the B+-tree, with the VSAM access method of IBM as an example of its use, and explains why it became the usual form in practice: the leaves form a sequential file, and the internal nodes form an index to it. CLRS mentions it as the common variant that keeps all satellite data in the leaves. Ramakrishnan and Gehrke give the version with order $d$, copy-up and push-up that this page uses.

## References
