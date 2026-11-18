---
tag: AJZDXP
kind: data-structure
slug: prefix-b-tree
name: Prefix B-tree
aliases:
- simple prefix B-tree
- suffix truncation
area: databases/storage-and-indexing
level: advanced
summary: "A B+ tree on string keys whose separators are shortest separators, chosen inside a split interval, and whose nodes store keys without the prefix that their fences share."
model: external-memory-model
complexity:
  vars: {n: the number of keys, f: the number of separators that fit in an inner page, L: the length of the longest key in characters, d: the half width of the split interval}
  time: {worst: "O(L log n)", average: "O(L log n)", best: "O(L log n)"}
  space: {extra: "O(n L)"}
  io:
    worst: "O(log_f n)"
    average: "O(log_f n)"
    best: "O(log_f n)"
properties: {deterministic: true, exact: true, external: true, online: true, in_place: false, recursive: false}
history:
  year: 1977
  people: [Rudolf Bayer, Karl Unterauer]
  note: "Bayer and Unterauer described the simple prefix B-tree and the prefix B-tree in TODS in 1977, after an IBM research report of 1976."
prereqs: [b-plus-tree, external-memory-model]
see_also: [front-coding, b-tree, trie, adaptive-radix-tree, bulk-loading-b-tree, dense-and-sparse-index, clustered-index, generalized-search-tree]
sources:
  - paper: doi:10.1145/320521.320530
    title: "Rudolf Bayer and Karl Unterauer, Prefix B-trees, ACM Transactions on Database Systems 2(1) (1977)"
    locator: pp. 11 to 26, the simple prefix B-tree (shortest separators in the index part, the split interval) and the prefix B-tree (prefixes that are not stored but rebuilt during the search)
  - paper: doi:10.1561/1900000028
    title: "Goetz Graefe, Modern B-tree techniques, Foundations and Trends in Databases 3(4) (2011)"
    locator: pp. 203 to 402, the sections on compression of keys in B-tree nodes (prefix truncation, shortened separator keys, fence keys); section level only
---

A prefix B-tree is a [B+ tree](/b-plus-tree/) on string keys that stores less of each key in its inner nodes and in its leaves. Two ideas from Bayer and Unterauer (1977) make it work: a separator in an inner node only has to tell two neighboring subtrees apart, so the shortest string that does this is enough; and all keys between two separators share the prefix of those separators, so a node does not need to store it. Shorter entries give more entries per page, a larger fan-out and a lower tree. [Front coding](/front-coding/) also removes shared prefixes, but it does so in a sorted list that must be decoded from the start of a block, while the prefix B-tree gets the prefix of a node from its two bounding separators during the search.

## In plain words

Think of the guide words at the top of a phone book page. The page holds names from "Smart" to "Smith". To send a reader to the right page you do not need the full names. "Smi" is enough to tell "Smart" apart from "Smith", because any name that comes after "Smart" and starts with "Smi" or later belongs to the next page.

Inside a page, every name between the guide words starts with "Sm". So the page can store "art" and "it" and add "Sm" back when it needs the whole name.

The tree does both. Its signposts are as short as they can be, and when a page splits, it looks at a few split points near the middle and takes the one with the shortest signpost.

## The abstract type

An ordered set of strings under the usual lexicographic order, with:

- `contains(T, k)`: is $k$ in $T$?
- `insert(T, k)`: add $k$.
- `range(T, lo, hi)`: the keys $k$ with $lo \le k \le hi$, in order.

Deletes work as in a B+ tree. A separator does not need to change when a key is deleted, because it still separates the two subtrees.

## Representation

The tree is a B+ tree: all keys are in the leaves, and every leaf is at the same depth. An inner node with children $c_0, \ldots, c_m$ holds separators $s_1 < \cdots < s_m$. This page uses the convention that every key in $c_{i-1}$ is less than $s_i$ and every key in $c_i$ is at least $s_i$.

- **Fences.** Each node $v$ has two *fences*, $low(v)$ and $high(v)$: the separators to the left and to the right of its pointer in its parent, or the fences of the parent at the ends. The root has the open interval. The invariant is that every key $k$ in the subtree of $v$ satisfies $low(v) \le k < high(v)$.
- **Shortest separators.** When a leaf splits between its keys $a < b$, the separator is the shortest string $s$ with $a < s \le b$. Bayer and Unterauer call a tree with only this change a *simple prefix B-tree*.
- **Split interval.** A split may take any split point within $d$ positions of the middle. The node takes the point whose separator is shortest. With $d = 0$ the split is the usual one at the middle.
- **Stored prefix.** Let $p(v)$ be the longest common prefix of $low(v)$ and $high(v)$ (empty if a fence is open). Every key in the subtree of $v$ starts with $p(v)$, so $v$ stores each key or separator without it. The paper calls the full design, with these prefixes rebuilt during the search, a *prefix B-tree*.

The capacity of a page is counted in bytes in a real system. The code on this page counts entries to keep the logic short; the savings show up as fewer characters stored.

## Operations

```pseudo id=main
SHORTEST-SEPARATOR(a, b)            ▷ a < b; the shortest s with a < s ≤ b
L1  i ← 0
L2  while i < |a| and a[i] = b[i] do i ← i + 1
L3  return the first i + 1 characters of b

SEARCH(T, k)
L4  v ← the root of T
L5  while v is not a leaf do
L6      j ← the number of stored separators of v that are ≤ k without p(v)
L7      v ← child j of v
L8  return whether k without p(v) is a stored key of v

SPLIT-LEAF(v)                       ▷ v has keys k_0 < ... < k_(n-1), one too many
L9  c ← ⌊(n + 1) / 2⌋
L10 j ← the index in [c - d, c + d] with the shortest SHORTEST-SEPARATOR(k_(j-1), k_j), ties to the one nearest c
L11 s ← SHORTEST-SEPARATOR(k_(j-1), k_j)
L12 left ← k_0 .. k_(j-1); right ← k_j .. k_(n-1)
L13 insert s and a pointer to right into the parent of v, just after the pointer to v
L14 store the keys of left and right without the prefixes of their new fences
```

Line L3 is well defined. If $a$ is a prefix of $b$, the loop stops at $i = |a| < |b|$. Otherwise it stops at the first position where $a$ and $b$ differ, and there $a[i] < b[i]$.

Line L6 strips $p(v)$ from $k$. This is safe because the search only enters $v$ when $low(v) \le k < high(v)$, and then $k$ starts with $p(v)$.

`insert` finds the leaf with SEARCH, adds the key, and calls SPLIT-LEAF when the leaf overflows. An inner node that overflows moves one of its separators up to its parent, again chosen within $d$ positions of the middle so that the shortest one moves up. A full root splits into a new root with one separator. `range` walks the leaves whose fence interval meets $[lo, hi]$.

## Example

Insert ten names in this order into a tree with at most 4 entries per node and a split interval with $d = 1$: Smith, Smithers, Smithson, Smythe, Smyth, Snow, Sato, Sanders, Smit, Smart. In the trace, a leaf is written as [prefix | stored keys].

1. The fifth insert overflows the leaf Smith, Smithers, Smithson, Smyth, Smythe. Here $c = 3$, and the three candidates are $j = 2$ with separator "Smiths", $j = 3$ with "Smy", and $j = 4$ with "Smythe". The shortest is "Smy". The root becomes {Smy}, and the leaves are [ | Smith Smithers Smithson] and [ | Smyth Smythe].
2. Snow and Sato go into the two leaves. Sanders then overflows the left leaf Sanders, Sato, Smith, Smithers, Smithson. The candidates are "Sm" ($j = 2$, between Sato and Smith), "Smithe" ($j = 3$) and "Smiths" ($j = 4$), so the split takes "Sm" and leaves two keys on the left.
3. The middle leaf now has the fences "Sm" and "Smy", which share the prefix "Sm", so it stores [Sm | ith ithers ithson]. Smit goes into it. Smart then overflows it with the keys Smart, Smit, Smith, Smithers, Smithson. The candidates are "Smith" ($j = 2$, between Smit and Smith), "Smithe" ($j = 3$) and "Smiths" ($j = 4$). The split takes "Smith", and the new leaf with the fences "Sm" and "Smith" stores [Sm | art it]. The shorter separator "Smi", between Smart and Smit, is at $j = 1$, outside the split interval, so it is not a choice.

The final tree from the code is:

| node | fences | stored prefix | stored entries |
|---|---|---|---|
| root | open | none | Sm, Smith, Smy |
| leaf 1 | open to Sm | none | Sanders, Sato |
| leaf 2 | Sm to Smith | Sm | art, it |
| leaf 3 | Smith to Smy | Sm | ith, ithers, ithson |
| leaf 4 | Smy to open | none | Smyth, Smythe, Snow |

The separators take 10 characters. With $d = 0$ the same inserts give the separators Smi, Smithe and Smy, 12 characters, and two leaves store the prefixes "Smi" and "Sm". On a larger run, 200 random keys of the form "customer-" followed by up to 5 letters (seed 7, at most 4 entries per node) give 143 distinct keys. The inner nodes then store 183 characters of separators instead of 525 characters for the same separators written in full, and 244 instead of 565 with $d = 0$.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md). They rest on three facts.

- **Shortest separator.** For $a < b$, the string $s$ of L3 satisfies $a < s \le b$, and no shorter string does. Let $t$ have $|t| \le i$ and $t \le b$. If $t$ is a prefix of $b$, it is a prefix of $a$ too, because the first $i$ characters agree, so $t \le a$. Otherwise $t$ first differs from $b$ at a position $j < i$ with $t[j] < b[j] = a[j]$, so $t < a$.
- **Prefix of an interval.** If $low \le k < high$ and $p$ is the longest common prefix of $low$ and $high$, then $k$ starts with $p$. So stripping $p$ loses nothing, and the order of the stored suffixes in $v$ is the order of the full keys.
- **Fence invariant.** Every insert and split keeps $low(v) \le k < high(v)$ for every key in the subtree of $v$. Then SEARCH visits the only leaf that can hold $k$, exactly as in a B+ tree.

## Complexity

Costs are in the page I/O model: one node is one page, and a page read is one I/O. In the [external memory model](/external-memory-model/), the memory holds M/B blocks; this page counts page reads only and does not use a buffer size.

- **Search** reads one page per level, $O(\log_f n)$ pages, where $f$ is the number of separators that fit in an inner page. In memory it does a binary search per node with $O(L)$ characters per comparison, $O(L \log n)$ in all, plus $O(L)$ per level to strip and add back the prefix.
- **Insert** costs one search, plus a split at each level in the worst case. The split interval adds $O(d L)$ work per split to compare the candidate separators.
- **Space** is at most that of the plain B+ tree on the same keys, and usually much less in the inner levels.
- **Fan-out.** If separators shrink from an average of $L$ to $\ell$ characters and a pointer takes $q$ bytes, the fan-out grows by about $(L + q) / (\ell + q)$. The height is $\lceil \log_f n \rceil$ and drops by one level only when $f$ grows enough; the gain in height is a measured effect that depends on the keys, not a guarantee.

## Variants

- **Simple prefix B-tree.** Shortest separators and the split interval, but every key stored in full. Most of the gain is in the inner levels.
- **Prefix truncation in leaves.** Many systems store the prefix shared by the fences of a leaf once and remove it from every key of the leaf, as on this page. Graefe (2011) describes this with fence keys kept in each node.
- **Front coding inside a page.** Each key stores only how many characters it shares with the key before it, as in [front coding](/front-coding/). This compresses more but needs a sequential decode, so binary search in the page becomes harder.
- **Normalized keys.** Multi-column keys are first mapped to one byte string whose order is the order of the columns, so that the string methods of this page apply to any key type.
- **Tries.** A [trie](/trie/) or an [adaptive radix tree](/adaptive-radix-tree/) stores each shared prefix once for all keys, not once per node, and has no separators at all, at the cost of a less regular page layout.

## When to use it

Use it for B+ trees on long string keys that share prefixes, such as URLs, file paths, names and composite keys. Most disk-based database systems use some of these ideas in their B-tree code. For short fixed-size integer keys the gain is small, because a separator cannot be shorter than one byte of difference.

## Pitfalls

- **Wrong separator convention.** The shortest separator must respect the rule used by the search. With "left < s ≤ right", the separator is a prefix of the first key on the right. A search that treats an equal key as belonging to the left goes wrong.
- **Choosing a separator from a deleted key.** A separator does not need to be a key of the tree. Code that assumes it is, for example to find "the key equal to the separator", breaks after deletes.
- **Prefixes after a split.** A split changes the fences of the two new nodes, so their prefixes can change. Every stored key must be stored again with the new prefix, as L14 does.
- **Too wide a split interval.** A large $d$ gives very uneven splits and lowers the fill of the pages. Keep $d$ small against the number of entries in a node.
- **Fan-out in entries.** If the page capacity is a count of entries, short separators save nothing. The gain comes only when a page holds as many entries as fit in its bytes.

## Implementations

## History

Rudolf Bayer and Karl Unterauer at the Technical University of Munich published "Prefix B-trees" in ACM Transactions on Database Systems in March 1977, after an IBM research report of 1976. They described the simple prefix B-tree, with short separators in the index part, and the prefix B-tree, in which the prefixes are not stored but rebuilt as the tree is searched. Graefe's survey of 2011 describes how these ideas, together with fence keys and normalized keys, are used in current B-tree code.

## References
