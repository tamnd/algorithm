---
tag: 1S27ZF
kind: algorithm
slug: mccreight-algorithm
name: McCreight's algorithm
aliases:
- McCreight suffix tree construction
area: strings/suffix-structures
level: advanced
summary: Linear-time suffix tree construction inserting suffixes from longest to shortest.
solves: [suffix-tree-construction]
model: word-ram
complexity:
  vars: {n: the length of the text, σ: the size of the alphabet}
  time: {worst: O(n log σ), constant-alphabet: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: false, comparison: false}
prereqs: [suffix-tree, suffix-link]
see_also: [ukkonen-algorithm, weiner-algorithm, suffix-tree-construction, suffix-tree-size-theorem, suffix-trie, implicit-suffix-tree, matching-statistics, generalized-suffix-tree]
sources:
  - paper: doi:10.1145/321941.321946
    title: Edward M. McCreight, A space-economical suffix tree construction algorithm, Journal of the ACM 23(2), 1976
    locator: pages 262 to 272; head and tail of each suffix, the suffix links, the rescan and scan steps, and the linear time bound
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 6, the section on McCreight's suffix tree algorithm
  - paper: doi:10.1007/pl00009177
    title: Robert Giegerich and Stefan Kurtz, From Ukkonen to McCreight and Weiner, a unifying view of linear-time suffix tree construction, Algorithmica 19(3), 1997
    locator: pages 331 to 353; McCreight's algorithm as Ukkonen's algorithm restricted to the complete text
---

McCreight's algorithm builds the [suffix tree](/suffix-tree/) of a string by inserting its suffixes one by one, from the longest to the shortest. Each new suffix branches off the tree at its *head*, the longest prefix it shares with an earlier suffix, and the [suffix link](/suffix-link/) of the previous head leads close to the new head, so the search does not start again at the root. Two kinds of walks, a fast *rescan* that only counts edge lengths and a *scan* that compares symbols, add up to $O(n)$ steps for a constant alphabet. McCreight published it in 1976 as a simpler and more space-economical form of [Weiner's](/weiner-algorithm/) 1973 algorithm, and Ukkonen's online algorithm of 1995 turned out to perform the same steps.

## In plain words

Put the endings of a text into a tree one at a time, from the whole text down to the last letter. Each new ending follows the tree from the top for as long as it matches some ending already there, and then a new branch starts. The matched part is its head.

Searching for each head from the top would be slow. But the head of the next ending is at least the old head minus its first letter. Each inner node of the tree has an arrow to the node for its string without the first letter. Follow that arrow, then go down. The part already known to match is crossed by edge lengths, without reading letters. Only the new part is read letter by letter. In total, the work is in proportion to the length of the text.

## The problem

**Input.** A string $S = S[0 \ldots n-1]$, 0-based, over an alphabet $\Sigma$ whose symbols can be keys of a child map; the code uses hash maps, so it tests symbols for equality only. The algorithm needs the whole string in advance.

**Output.** The suffix tree of $t = S\$$, where the [sentinel](/sentinel-character/) $\$$ occurs nowhere in $S$: a compact trie with one leaf for each of the $n + 1$ suffixes $t_i = t[i \ldots n]$, every inner node except the root with at least two children, and edges labeled by index pairs into $t$. The algorithm also leaves a suffix link at every inner node.

## The algorithm

For $i \ge 1$, the *head* $head_i$ is the longest prefix of $t_i$ that is also a prefix of some $t_j$ with $j < i$, and the *tail* is the rest of $t_i$. Because $\$$ is unique, the tail is never empty, so suffix $i$ gets a leaf below the place of $head_i$, and the tree after step $i$ is the compact trie of $t_0, \ldots, t_i$. Take $head_0$ as the empty string.

**McCreight's lemma.** If $head_{i-1} = x\alpha$ for a symbol $x$ and a string $\alpha$, then $\alpha$ is a prefix of $head_i$. *Reason:* $x\alpha$ is a prefix of some earlier $t_j$, $j < i - 1$, so $\alpha$ is a prefix of $t_{j+1}$, which is earlier than $t_i$, and $\alpha$ is also a prefix of $t_i$.

So step $i$ can start from the place of $\alpha$. If $head_{i-1}$ is an inner node that existed before step $i - 1$, it has a suffix link to $\alpha$. Otherwise $head_{i-1}$ was created in step $i - 1$ and has no link yet; then its parent $p$ has one, and the place of $\alpha$ is reached from $link(p)$ by going down the label $\beta$ of the edge from $p$ to $head_{i-1}$. That walk is the *rescan*: $\alpha$ is known to be in the tree, so it uses only edge lengths and first symbols.

```pseudo id=main
MCCREIGHT(t)                                ▷ t = S$, suffixes t_0 .. t_n
L1  create the root and a leaf for t_0; h ← root          ▷ h = head of the last suffix
L2  for i ← 1 to n do
L3      if h = root then w ← root
L4      else if h has a suffix link then w ← link(h)
L5      else p ← parent(h); β ← label(p → h); if p = root then drop the first symbol of β and v ← root else v ← link(p)
L6          w ← RESCAN(v, β)                ▷ go down by edge lengths; split an edge if β ends inside it
L7          link(h) ← w; if w was just created by a split then head_i ← w and go to L9
L8      head_i ← SCAN(w, t_i)               ▷ compare symbols below w; split at the first mismatch
L9      add a leaf for t_i below head_i
L10     h ← head_i
L11 return the tree
```

**Why a rescan that ends inside an edge gives the head directly.** In that case $head_{i-1} = x\alpha$ was new in step $i - 1$, so it was created by a split: $x\alpha$ is followed in the tree by one symbol $c$ from an earlier suffix and by a different symbol $d$ in $t_{i-1}$. Then $\alpha c$ occurs in an earlier suffix, and $\alpha d$ is a prefix of $t_i$. If $\alpha$ ends inside an edge, the only symbol that follows it in the tree is $c$, so $t_i$ leaves the tree right there, and the new node is $head_i$.

## Example

Take $S = \texttt{aaabaaa}$, $n = 7$, $t = \texttt{aaabaaa\$}$. The table gives, for each step, how the start point $w$ was found, and the head.

| $i$ | $t_i$ | case | start $w$ | $head_i$ | new node |
|---|---|---|---|---|---|
| 0 | `aaabaaa$` | | | empty | |
| 1 | `aabaaa$` | L3, scan from the root | root | `aa` | `aa`, split of the leaf edge of $t_0$ |
| 2 | `abaaa$` | L5, rescan `a` from the root | | `a` | `a`, split inside the edge `aa`; link(`aa`) = `a` |
| 3 | `baaa$` | L5, rescan the empty string | root | empty | link(`a`) = root |
| 4 | `aaa$` | L3, scan from the root | root | `aaa` | `aaa`, split of the edge `abaaa$` below `aa` |
| 5 | `aa$` | L5, rescan `a` from link(`aa`) = `a` | `aa` | `aa` | none; link(`aaa`) = `aa` |
| 6 | `a$` | L4, link(`aa`) | `a` | `a` | none |
| 7 | `$` | L4, link(`a`) | root | empty | none |

In step 2 the rescan of `a` ends inside the edge from the root to `aa`, so the new node `a` is the head and no symbol is compared. In step 5 the head of step 4, `aaa`, is new; its parent `aa` has the link to `a`, and the rescan of the edge label `a` from there ends exactly at the node `aa`; the scan then compares the symbol $\$$ and stops at once. In steps 6 and 7 the old heads have links and the scans also stop at once. The final tree has the root, the three inner nodes `a`, `aa`, `aaa` and eight leaves, 12 nodes, and its leaves in symbol order give the suffix array $[6, 5, 4, 0, 1, 2, 3]$ of $S$. The code checks this trace.

## Correctness

The invariant before step $i$ is: the tree is the compact trie of $t_0, \ldots, t_{i-1}$ with leaves labeled by their start positions, every inner node except possibly $h = head_{i-1}$ has its suffix link, and $h$ is the place of $head_{i-1}$. By McCreight's lemma, lines L3 to L7 reach the place of $\alpha$, a prefix of $head_i$, and they set the link of $h$, which is an inner node whose string without the first symbol is $\alpha$. The scan in line L8 extends from $\alpha$ to the longest prefix of $t_i$ in the tree, which is $head_i$ by definition. Line L9 adds the leaf, so the tree is the compact trie of $t_0, \ldots, t_i$. A node created in step $i$ can only be $head_i$, so all other inner nodes still have links. The proof file gives the details.

## Complexity

**Scan.** Let $|head_i|$ be the string depth of the head. The scan in step $i$ starts at depth at least $|head_{i-1}| - 1$ and compares $|head_i| - |w| + 1$ symbols, so its cost is at most $|head_i| - |head_{i-1}| + 2$. Summed over $i$, this telescopes to at most $|head_n| + 2n = O(n)$.

**Rescan.** Each step of the rescan goes down one node, with $O(1)$ work. Let $nd(x)$ be the node depth of a place $x$, the number of nodes on its path from the root. Going from $h$ to its parent lowers the node depth by one. Following a suffix link from $p$ lowers it by at most one more, because the ancestors of $p$ other than the root have links to distinct ancestors of $link(p)$. So the rescan starts at node depth at least $nd(head_{i-1}) - 2$, and the scan after it only goes down. The number of rescan steps in step $i$ is therefore at most $nd(head_i) - nd(head_{i-1}) + 2$, which sums to $O(n)$.

**Total.** Each step needs a child lookup by its first symbol: $O(1)$ for a constant alphabet or with hashing, and $O(\log \sigma)$ with balanced child maps. The tree has at most $2n + 1$ nodes, by the [size theorem](/suffix-tree-size-theorem/).

| resource | bound |
|---|---|
| time, constant alphabet or hashing | $O(n)$, expected for hashing |
| time, ordered child maps | $O(n \log \sigma)$ |
| symbol comparisons in scans | at most $3n + 1$ |
| space | $O(n)$ words |

## Properties

- **Not online.** Suffix $i$ needs the symbols after position $i$, so the whole text must be known. Before step $n$, the tree is not the suffix tree of any prefix.
- **Equality tests only.** No symbol order is used, except to list children in order afterwards.
- **Iterative.** Only loops; the code uses no recursion.
- **Each step adds one leaf and at most one inner node.** So the node counts follow the [size theorem](/suffix-tree-size-theorem/) directly.

## Variants and improvements

- **Ukkonen's algorithm.** [Ukkonen's](/ukkonen-algorithm/) online algorithm, run on the whole text, creates the same nodes in the same order; Giegerich and Kurtz show the correspondence. Ukkonen's version is online, McCreight's is often a little simpler to analyze.
- **Weiner's algorithm.** [Weiner's](/weiner-algorithm/) algorithm inserts the suffixes from the shortest, using reverse links; McCreight's insertion order needs only forward suffix links and less space.
- **Space reductions.** Kurtz (1999) gives representations of McCreight's tree with about 10 to 20 bytes per symbol, which made suffix trees practical for whole genomes.
- **Generalized suffix trees.** Insert the suffixes of several strings in turn, each with its own end marker.
- **Matching statistics.** The same head, link and rescan steps compute the [matching statistics](/matching-statistics/) of a pattern against the tree of a text.

## When to use it

Use McCreight's algorithm to build a suffix tree of a fixed text in linear time with a short, iterative program. If the text arrives as a stream, use Ukkonen's algorithm. For very large texts, or when memory matters, build the [suffix array](/suffix-array/) and the LCP array and derive the tree, or work with the arrays directly.

## Pitfalls

- **Rescan from the wrong node.** When the parent $p$ of the new head is the root, the first symbol of $\beta$ must be dropped and the rescan starts at the root; when $p$ is not the root, the whole $\beta$ is rescanned from $link(p)$.
- **Comparing symbols in the rescan.** The rescan must only compare lengths and pick children by first symbol; reading all symbols is correct but loses the linear bound.
- **Stale parent pointers after a split.** When an edge is split, the lower node gets the new node as its parent. The rescan of the next step starts from the parent of the head, so a parent pointer that is not updated sends it to the wrong place.
- **Forgetting to set the link of a new head.** The link must be set in the next step, even when the rescan ends at the root.
- **No unique sentinel.** Without it, a suffix can be a prefix of an earlier one; it has no tail and no leaf, and the head definition breaks.

## Implementations

## History

Weiner gave the first linear-time construction in 1973. McCreight's 1976 paper in the Journal of the ACM inserted the suffixes in the opposite order, introduced the suffix links used by later algorithms, and saved space over Weiner's structure. Ukkonen's online algorithm (1995) and the unifying view of Giegerich and Kurtz (1997) showed that the two left-to-right methods are close relatives. Gusfield's 1997 textbook presents all three linear-time constructions.

## References
