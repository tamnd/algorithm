---
tag: EZGPK7
kind: data-structure
slug: string-b-tree
name: String B-tree
aliases:
- Ferragina-Grossi B-tree
- String B-tree of Ferragina and Grossi
area: data-structures/string-structures
level: advanced
summary: External-memory search tree for strings that uses longest-common-prefix information to achieve optimal I/O.
implements: [string-symbol-table]
model: external-memory-model
complexity:
  vars: {p: the length of the pattern, K: the number of strings, B: the number of symbols or words in a disk page}
  time: {worst: O(p/B + log_B K)}
  space: {extra: O(K/B)}
properties: {persistent: false, concurrent: false, external: true}
prereqs: [b-tree, radix-tree, external-memory-model]
see_also: [b-plus-tree, radix-tree, suffix-array, full-text-index, cache-oblivious-model, string-sorting, trie, substring-queries]
sources:
  - paper: Paolo Ferragina and Roberto Grossi, The String B-tree, a new data structure for string search in external memory and its applications, Journal of the ACM 46(2), 1999, doi:10.1145/301970.301973
    locator: pages 236 to 280, the B-tree of string pointers with a Patricia trie in each node, blind search, the lcp passed between levels, and the bounds for prefix and substring search, insertion and deletion
  - paper: Michael A. Bender, Martin Farach-Colton and Bradley C. Kuszmaul, Cache-oblivious string B-trees, PODS 2006, doi:10.1145/1142351.1142385
    locator: pages 233 to 242, a cache-oblivious structure with the same goals and the comparison with the String B-tree
---

The String B-tree of Ferragina and Grossi is a B-tree for strings in external memory. The strings stay on disk, and the tree stores only pointers to them; each node holds the Patricia trie of its keys, the *blind trie*, which fits in one page because it stores branching positions and symbols but no string content. A search for a pattern $P$ of length $p$ among $K$ strings reads $O(p/B + \log_B K)$ pages: one page per level for the node, plus pages of the strings, but the symbols of $P$ that were already matched at one level are not read again at the next. Used on the suffixes of a text, it is an external-memory [full-text index](/full-text-index/) that supports updates.

## In plain words

A plain B-tree of strings needs whole string comparisons in every node, and a long string can fill many disk pages. Searching would then cost the length of the pattern at every level of the tree.

The String B-tree fixes two things. Inside a node, it does not compare the pattern with every key. It walks a small trie of the keys, looking only at the letters where the keys differ, and picks one key. One real comparison with that key, reading the string from disk, then tells where the pattern fits among all the keys of the node.

Across levels, it remembers how many letters of the pattern already matched. The next level starts its comparison there. So the pattern is read about once in total, plus one extra letter per level.

## The abstract type

The String B-tree implements an ordered [string symbol table](/string-symbol-table/) for strings stored outside the tree: insert and delete strings, test membership, find the rank of a string in sorted order, and report the strings with a given prefix. When the strings are the suffixes of a text, prefix search becomes substring search, as in a [suffix array](/suffix-array/).

## Representation

The form used here is a B+-tree with fan-out between $b/2$ and $b$, where $b = \Theta(B)$:

- A leaf holds the pointers to up to $b$ strings, in sorted order.
- An internal node holds, for each child, the pointers to the smallest and the largest string below the child, and the number of strings below it. Its keys are these $2c$ pointers, for $c$ children.
- Each node stores the blind trie of its keys: the Patricia trie of the key strings with, at each branching node, its depth and the branching symbols, and the keys as leaves. Here it is kept in array form: for adjacent keys $k_{j-1}$ and $k_j$, the length $adj[j]$ of their longest common prefix and the two symbols $lc[j]$ and $rc[j]$ at that position. The trie is the Cartesian tree of the $adj$ array.

**Invariant.**

- **(S1) B-tree.** All leaves have the same depth, and the sizes are within the bounds above, except at the root.
- **(S2) Order.** The keys of each node are in increasing order of their strings, and the leaves, read from left to right, hold all strings in increasing order.
- **(S3) Boundaries.** The keys of an internal node are the first and the last string of each child, in order.
- **(S4) Tries.** The blind trie of each node is the Patricia trie of its keys.

## Operations

```pseudo id=main
LOCATE(x, P, λ)                    ▷ λ ≤ the longest lcp of P with a key of x
L1  blind search: start with all keys of x; while more than one key: d ← the smallest adj in the range; split the range at the positions with adj = d
L2      keep the part whose branching symbol is P[d], or the first part if none matches or P has no symbol d
L3  s ← the key found; ℓ ← λ; read s from position λ while it agrees with P: ℓ ← lcp(P, s)
L4  for each key k of x: decide k ≤ P from lcp(s, k), ℓ, P[ℓ] and the branching symbols; return the number r of keys ≤ P and the lcp of P with each key

RANK(P)                            ▷ the number of strings ≤ P
    x ← root; λ ← 0; rank ← 0
    repeat: (r, lcps) ← LOCATE(x, P, λ)
L5      if x is a leaf then return rank + r
        i ← ⌊r/2⌋; rank ← rank + the counts of children 0 … i−1; if r is even then return rank
L6      λ ← max(lcps of the first and last key of child i); x ← child i

PREFIX-RANGE(P)
L7  return [the number of strings < P, RANK(P · ⊤)), where ⊤ is above every symbol

INSERT(w)
L8  descend as in RANK, into the child whose range contains w or ends just before it, recording the path
L9  insert w into the leaf at its rank; rebuild the leaf's blind trie
L10 for each node of the path, bottom up: update the count, split the child if it has more than b entries, recompute the boundary keys and the blind trie
L11 if the root has more than b entries, split it and make a new root
```

**Blind search (L1, L2).** The blind search follows the symbols of $P$ at the branching depths of the trie without checking the symbols in between, so it reads no string. Its result $s$ is a key with the longest common prefix with $P$ among all keys of the node, even though it may differ from $P$ early on.

**One comparison (L3, L4).** The only disk access for strings is the comparison of $P$ with $s$. With $\ell = lcp(P, s)$ known, the place of $P$ among all keys follows from the trie alone: a key $k$ with $lcp(s, k) < \ell$ is on the same side of $P$ as of $s$; one with $lcp(s, k) > \ell$ is on the side given by $P[\ell]$ against $s[\ell]$; one with $lcp(s, k) = \ell$ is decided by $P[\ell]$ against the branching symbol of $k$ at depth $\ell$, which the trie stores.

**The lcp passed down (L6).** If $P$ falls inside the range of child $i$, its neighbors among the keys of $x$ are the first and last string of that child, and these are keys of the child too, by (S3). So the child's best key has a common prefix with $P$ at least as long as $\lambda$, the larger of the two, and its comparison starts there. This is what makes the symbol reads add up to $p$ plus one per level, instead of $p$ per level.

**Deletion.** Ferragina and Grossi also delete strings, with the usual B-tree merges and borrowing and with the boundary keys and tries updated along the path; the implementation here does not.

## Example

Twelve strings with $b = 4$, inserted in sorted order: abaa, abab, abba, abbb, abc, bab, baba, bb, bbaa, bbab, c, caa. The tree has height 3:

| node | keys (as strings) | adj | children counts |
|---|---|---|---|
| root | abaa, abbb, abc, caa | 0, 2, 2, 0 | 4, 8 |
| left internal | abaa, abab, abba, abbb | 0, 3, 2, 3 | 2, 2 |
| right internal | abc, bab, baba, bb, bbaa, caa | 0, 0, 3, 1, 2, 0 | 2, 2, 4 |
| leaves | abaa abab; abba abbb; abc bab; baba bb; bbaa bbab c caa | | |

$RANK($bbab$)$:

1. **Root.** The blind search splits at depth 0 into {abaa, abbb, abc} (symbol a) and {caa} (symbol c). $P[0] = $ b matches neither, so it keeps the first part, splits it at depth 2 into a, b, c, and keeps abaa for $P[2] = $ a. The comparison reads one symbol: $\ell = 0$. From the trie, abaa, abbb and abc are below $P$ and caa is above, so $r = 3$: $P$ is inside child 1, with rank so far 4 and $\lambda = \max(lcp($bbab, abc$), lcp($bbab, caa$)) = 0$.
2. **Right internal node.** The blind search keeps the b part {bab, baba, bb, bbaa}, then for $P[1] = $ b the part {bb, bbaa}, then for $P[2] = $ a the key bbaa. The comparison reads b, b, a and the mismatch b against a: $\ell = 3$, 4 symbols. The keys up to bbaa are $\le P$, so $r = 5$, child 2, rank so far $4 + 2 + 2 = 8$, and $\lambda = lcp($bbab, bbaa$) = 3$.
3. **Leaf.** The blind search finds bbab, and the comparison starts at position 3 and reads one symbol: $\ell = 4$, equal. Two keys are $\le P$, so the rank is 10.

The search read 6 symbols of stored strings in 3 nodes, within the bound $p + h = 4 + 3$. Without the passed lcp, the leaf would have read bbab again from the start.

## Correctness

Three facts make the operations correct. Blind search returns a key with the longest common prefix with $P$ among the keys of the node. Given that key and its lcp with $P$, the trie decides the order of $P$ against each key. And the larger of the lcps of $P$ with the two boundary keys of a child is a valid starting point for the comparison in the child. With these, RANK descends exactly into the child that contains the place of $P$ and adds the counts of the children to its left. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let the height be $h = O(\log_B K)$ for fan-out $\Theta(B)$.

- **Search.** Each level reads one node, one page, and the symbols of one string from position $\lambda$ to the first mismatch. The lcp $\ell$ never decreases from level to level, and each level reads $\ell - \lambda + 1$ symbols, so the total is at most $p + h$ symbols, in $O(p/B + h)$ pages when strings are stored contiguously. Ferragina and Grossi prove $O(p/B + \log_B K)$ I/Os for a prefix search, plus $O(occ/B)$ to report $occ$ results.
- **Insertion.** The descent costs the same as a search for the new string of length $m$. The updates along the path touch $O(1)$ nodes per level, and the blind tries are rebuilt in memory, without reading strings, except for the lcps of the new string with its neighbors, which the search computed. The paper proves $O(m/B + \log_B K)$ I/Os.
- **Inside a node.** The blind search and the rank computation are CPU work on one page, $O(B)$ time in the array form here.
- **Space.** $O(K/B)$ pages for the tree, plus the strings themselves.

For substring search on a text of length $N$, the paper indexes the $N$ suffixes and obtains $O((p + occ)/B + \log_B N)$ I/Os per query.

## Variants

- **Patricia tries as trees.** The original stores each node's blind trie as an explicit compacted trie, with the leaves in order, and updates it in place on insertion. The array form here encodes the same information.
- **Suffixes of a dynamic text.** Storing pointers to all suffixes gives a substring index that supports inserting and deleting whole texts, one of the main applications in the paper.
- **Cache-oblivious string B-trees.** Bender, Farach-Colton and Kuszmaul give a structure with similar search bounds that does not need to know $B$, built from cache-oblivious layouts and a compressed representation of the keys.

## When to use it

Use a String B-tree when a large dynamic set of long strings, or of the suffixes of a large text collection, lives on disk and must answer prefix or substring queries with few I/Os. For a static collection, a [suffix array](/suffix-array/) on disk with an lcp-aware binary search is simpler. In memory, a [trie](/trie/), a [radix tree](/radix-tree/) or a sorted array is usually enough.

## Pitfalls

- **Trusting the blind search.** The key found by the blind search can differ from $P$ before the first branching depth. It must be compared with $P$; only then is the order of $P$ against the keys known.
- **Passing the wrong lcp.** The value passed to a child must be a lower bound on the lcp of $P$ with the child's best key. The lcp with the parent's best key is only safe because the boundary keys of the child are its neighbors and are keys of the child; storing separators that are not keys of the child breaks this.
- **Prefixes and equal strings.** A key that is a proper prefix of another, or equal to $P$, needs an end symbol below all symbols, and the prefix range needs one above all symbols. Both must be reserved.
- **Stale tries.** After an insertion or a split, the boundary keys of every node on the path change, and so do their tries. Forgetting to update one gives wrong ranks later, not wrong structure.

## Implementations

The Python class keeps the strings in a list and builds a B+-tree of their indexes with fan-out $b$. Each node keeps the arrays $adj$, $lc$ and $rc$ of its blind trie. LOCATE runs the blind search on these arrays, compares with one string from the passed lcp, and ranks the pattern among the keys; RANK, prefix ranges, membership and insertion follow the pseudocode. A counter of symbols read checks the bound $p + h$. The tests replay the example and compare 500 random sets against a sorted list, also checking the bound on every search.

## History

Ferragina and Grossi presented the String B-tree at STOC 1995 and in the Journal of the ACM in 1999, as the first external-memory structure with optimal search bounds for strings of unbounded length. Bender, Farach-Colton and Kuszmaul gave a cache-oblivious version in 2006.

## References
