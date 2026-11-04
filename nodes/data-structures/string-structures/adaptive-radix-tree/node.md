---
tag: 1RJXRZ
kind: data-structure
slug: adaptive-radix-tree
name: Adaptive radix tree
aliases:
- ART
area: data-structures/string-structures
level: advanced
summary: Radix tree whose inner nodes switch between a few array layouts depending on the number of children.
implements: [string-symbol-table]
model: word-ram
complexity:
  vars: {m: the length of the key in bytes, n: the number of keys}
  time: {worst: O(m)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [radix-tree, trie]
see_also: [radix-tree, trie, hash-table, b-tree, burst-trie, hat-trie, double-array-trie, longest-prefix-match]
sources:
  - paper: Viktor Leis, Alfons Kemper and Thomas Neumann, The adaptive radix tree, ARTful indexing for main-memory databases, Proceedings of the 29th IEEE International Conference on Data Engineering (ICDE 2013), doi:10.1109/ICDE.2013.6544812
    locator: pages 38 to 49, Section III (the four node types, lazy expansion and path compression, search, insert and delete) and Section IV (binary-comparable keys)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.3 (Digital searching), tries with nodes as tables and Patricia
  - paper: Viktor Leis, Florian Scheibner, Alfons Kemper and Thomas Neumann, The ART of practical synchronization, Proceedings of the 12th International Workshop on Data Management on New Hardware (DaMoN 2016), doi:10.1145/2933349.2933352
    locator: the whole paper, optimistic lock coupling and the read-optimized write exclusion protocol applied to ART
---

An adaptive radix tree (ART) is a [radix tree](/radix-tree/) over byte strings in which each inner node picks one of four layouts by its number of children: Node4 and Node16 store up to 4 or 16 key bytes in a sorted array next to an array of child pointers, Node48 stores an index of 256 bytes into 48 child slots, and Node256 is a plain array of 256 child pointers. A node grows into the next layout when it is full and shrinks when it has few children left, so its size follows its fan-out, while a lookup still costs $O(1)$ per byte of the key. With path compression for chains of one-child nodes and lazy expansion, where a leaf holds its whole key, the tree has fewer inner nodes than keys. Leis, Kemper and Neumann (2013) designed it as an in-memory index for database systems, where it is as fast as a hash table for lookups and keeps the keys in order.

## In plain words

A trie looks at a key one byte at a time and has a branch for each possible next byte. If each node keeps a table with all 256 possible branches, lookups are fast but most of the table is empty, and memory runs out. A short list per node saves memory but is slow in big nodes.

ART chooses per node. A node with at most 4 branches keeps a tiny list. A node with up to 16 keeps a list that a processor can scan in one instruction. Up to 48, it keeps a 256-entry table of small numbers that point into 48 slots. Above that, it keeps the full table. When a node fills up it moves into the next bigger form, and after deletions it moves back. Long stretches with no branching are stored once in the node, not as a chain of nodes.

## The abstract type

ART implements an ordered [string symbol table](/string-symbol-table/) whose keys are byte strings: get, put, delete, ordered iteration, range scans and prefix queries. Keys of other types are first mapped to *binary-comparable* byte strings, whose byte order is the order of the keys; for example, an unsigned integer is written in big-endian byte order (Leis et al., Section IV).

## Representation

Keys are byte strings, and each key is followed by a terminator byte 0 that occurs in no key, so that no stored key is a prefix of another. (The paper assumes prefix-free keys, which null-terminated strings are.)

- A *leaf* stores the whole key and its value.
- An *inner node* $x$ stores a byte string $x.prefix$, the compressed path, and its children, each labeled by a distinct byte. The layout $x.kind$ is one of:

| layout | children | how a child is found | size on a 64-bit machine (pointers 8 bytes) |
|---|---|---|---|
| Node4 | 2 to 4 | sorted array of 4 key bytes, parallel array of 4 pointers | 4 + 32 bytes |
| Node16 | 4 to 16 | sorted array of 16 key bytes, parallel array of 16 pointers | 16 + 128 bytes |
| Node48 | 13 to 48 | array of 256 slot numbers, array of 48 pointers | 256 + 384 bytes |
| Node256 | 37 to 256 | array of 256 pointers | 2048 bytes |

The ranges of the child counts reflect the grow and shrink rule used here: a node grows when a child is added to a full node, and shrinks to the next smaller layout when its count falls to 3, 12 or 36. The gap between the two thresholds stops a node from switching layouts back and forth.

The string of a node is the concatenation, along the path from the root, of the prefixes of the inner nodes and the bytes of the edges. **Invariant.**

- **(A1) Paths.** For each leaf, its key starts with the string of the path from the root to the leaf.
- **(A2) Branching.** Every inner node has at least 2 children, with distinct bytes, and its child count is in the range of its layout. In Node4 and Node16, the key bytes are sorted.
- **(A3) Count.** The number of leaves is the number of keys.

## Operations

```pseudo id=main
ART-GET(T, k)                     ▷ k already ends with the terminator
L1  x ← T.root; d ← 0; while x is an inner node:
L2      if k[d .. d + |x.prefix| − 1] ≠ x.prefix then return NIL
L3      d ← d + |x.prefix|
L4      x ← FIND-CHILD(x, k[d]); d ← d + 1
L5  if x ≠ NIL and x.key = k then return x.val
L6  return NIL

ART-PUT(T, k, v)
L7  if T.root = NIL then T.root ← LEAF(k, v); return
    x ← T.root; d ← 0; loop:
L8      if x is a leaf: if x.key = k then x.val ← v; return
L9          p ← the length of the common prefix of x.key[d ..] and k[d ..]
L10         replace x by a new Node4 with prefix k[d .. d+p−1] and children x (byte x.key[d+p]) and LEAF(k, v) (byte k[d+p]); return
L11     m ← the length of the common prefix of x.prefix and k[d ..]
L12     if m < |x.prefix| then replace x by a new Node4 with prefix x.prefix[0 .. m−1] and children x (byte x.prefix[m], keeping x.prefix[m+1 ..]) and LEAF(k, v) (byte k[d+m]); return
L13     d ← d + |x.prefix|; c ← FIND-CHILD(x, k[d])
L14     if c = NIL:
L15         if x is full then replace x by a copy in the next larger layout
L16         ADD-CHILD(x, k[d], LEAF(k, v)); return
L17     x ← c; d ← d + 1

ART-DELETE(T, k)
L18 walk down as in ART-GET, recording the path of (node, byte) pairs
L19 if the leaf reached does not have key k then return
L20 remove the leaf from its parent q
L21 if q has one child left then replace q by that child, putting q.prefix and the child's byte in front of the child's prefix if it is an inner node
L22 else if q has reached its shrink threshold then replace q by a copy in the next smaller layout
```

**Find a child.** In Node4 and Node16, compare the byte with the sorted key bytes; a real implementation compares all 16 bytes of a Node16 at once with SIMD instructions. In Node48, read the slot number at index $b$ and then the pointer. In Node256, read the pointer at index $b$. Each is $O(1)$.

**Lazy expansion and path compression.** A new key that differs from an existing leaf at some depth is put in a new Node4 at the first byte where they differ (lines L9 and L10), and the common bytes become the prefix of that Node4. So no chain of one-child nodes is ever built, and a leaf hangs as high as possible. Line L12 handles a key that leaves the compressed path of a node in the middle: the node is split at the mismatch.

## Example

Insert tree, trie, tries, trip, trot, try (values 0 to 5), each with its terminator 0.

- After tree, the root is a leaf.
- trie differs from tree at byte 2 ("e" against "i"), so the root becomes a Node4 with prefix "tr" and children "e" (tree) and "i" (trie).
- tries goes to the child "i", a leaf with key trie, at depth 3. The two keys agree on "e" and then differ (0 against "s"), so the leaf is replaced by a Node4 with prefix "e" and children 0 (trie) and "s" (tries) (lines L9 and L10).
- trip reaches that Node4 at depth 3, and its prefix "e" does not match "p" at the first byte. Line L12 splits the node: a new Node4 with an empty prefix takes its place, with children "e" (the old node, whose prefix is now empty) and "p" (trip).
- trot and try add the children "o" and "y" to the root.

The result has 3 inner nodes, all Node4: the root with prefix "tr" and children e, i, o, y; the node of "tri" with children e and p; and the node of "trie" with children 0 and s. A lookup of "trie" checks the prefix "tr", takes "i", then "e", then the terminator, and compares the key at the leaf.

Insert trunk: the root has 4 children, so it grows into a Node16 with 5. Deleting trunk leaves the Node16 with 4 children, above the shrink threshold 3; deleting trot then brings it to 3, and it shrinks back to a Node4.

## Correctness

The invariant makes a search exact. By (A1) and the terminator, the leaf of a key $k$ is the only leaf whose path string is a prefix of $k$ and whose key is $k$, and the walk of lines L1 to L4 follows that path, since at each inner node the compressed prefix and the next byte of $k$ fix the child. Line L5 compares the full key, which makes the result correct even though inner nodes on the path are not checked against the deleted bytes. Insertions split nodes exactly at the first byte where the new key leaves the existing paths, and deletions merge a one-child node into its child, which keeps (A1) and (A2). Changing a layout does not change the children or their bytes. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Time.** Each step of a lookup reads one compressed prefix and finds one child in $O(1)$ time, so get, put and delete take $O(m)$ time for a key of $m$ bytes, independent of $n$. A layout change copies at most 256 children, which is $O(1)$. The height is at most $m + 1$ and is usually much smaller, since path compression removes the levels where no branching happens.

**Space.** Every inner node has at least 2 children by (A2), so there are fewer inner nodes than leaves, and $\Theta(n)$ nodes in all. Each layout stores its children at a constant cost per child, apart from the fixed parts of Node48 and Node256, which are only used with at least 13 and 37 children. So the space of the inner nodes is $O(1)$ words per key, and Leis et al. give a bound on the bytes per key that does not depend on the keys. The leaves store the keys, which is $O(N)$ bytes for total key length $N$; with values that are pointers to records holding the keys, the leaves need no copy.

**In practice.** Leis et al. report that ART answers lookups faster than the in-memory search trees they tested and about as fast as hash tables, with good cache behaviour because the top levels of the tree stay in cache.

## Variants

- **Optimistic path compression.** Store only the length of the compressed path and its first few bytes in the node, skip the rest during the search, and check the full key at the leaf. This keeps nodes of a fixed size. The paper also describes a hybrid that stores up to 8 bytes and switches to the optimistic mode for longer paths.
- **Multi-value leaves and single-value leaves.** A leaf can be a pointer to a record instead of a node, with a tag bit in the child pointer telling leaves from inner nodes.
- **Concurrent ART.** Leis et al. (2016) make ART concurrent with optimistic lock coupling, in which readers take no locks and check version counters, and with the ROWEX protocol, in which readers never wait.
- **Other adaptive tries.** [Burst tries](/burst-trie/) and [HAT-tries](/hat-trie/) adapt by switching subtrees to containers of strings; [double-array tries](/double-array-trie/) pack all nodes into two integer arrays for static sets.

## When to use it

Use ART as a main-memory index for keys of fixed or variable length when both point lookups and ordered scans or range queries are needed, for example the primary index of an in-memory database. For point lookups only, a [hash table](/hash-table/) is simpler. For data on disk, a [B-tree](/b-tree/) fits the block structure better.

## Pitfalls

- **Keys that are prefixes of others.** ART as described needs prefix-free keys. Append a terminator that no key contains, or store a value at the inner node where a key ends.
- **Byte order of keys.** Integers in little-endian order, signed integers in two's complement, and floats do not sort correctly as bytes. Convert keys to a binary-comparable form: big-endian, with the sign bit flipped for signed integers.
- **Checking the key at the leaf.** With optimistic path compression or lazy expansion, a search can reach a leaf for a different key. Always compare the full key at the end.
- **Layout thrashing.** If a node grows at 5 children and shrinks at 4, alternating inserts and deletes copy the node each time. Shrink well below the grow point.
- **Merging after delete.** When a node keeps one child, merge it with the child and put its prefix and the child's byte in front of the child's prefix; forgetting the byte corrupts the path.

## Implementations

The Python class uses one node class with a layout field, sorted lists for Node4 and Node16, a 256-entry index for Node48 and a 256-slot list for Node256. It stores full prefixes in inner nodes and full keys in leaves, appends the byte 0 to each key, and shrinks nodes at 3, 12 and 36 children. All walks are loops. The tests replay the example of this page, fill a Node256 and empty it again, and compare random operations against a dictionary.

## History

Tries with nodes stored as arrays or as lists go back to the work on digital search in the late 1950s and 1960s, and Knuth (Section 6.3) discusses the choice between the two. Leis, Kemper and Neumann introduced the adaptive radix tree in 2013 for the HyPer main-memory database system, combining nodes of several sizes with path compression and lazy expansion. In 2016 Leis and others added synchronization protocols for concurrent use.

## References
