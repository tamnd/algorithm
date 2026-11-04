---
tag: WSA7VT
kind: data-structure
slug: sparse-suffix-tree
name: Sparse suffix tree
area: data-structures/string-structures
level: research
summary: Suffix tree built only for a sampled subset of suffixes, trading query time for space.
implements: [full-text-index]
model: word-ram
complexity:
  vars: {n: the length of the text, b: the number of chosen suffixes, m: the length of the pattern, z: the number of chosen positions reported}
  time: {worst: O(m + z)}
  space: {extra: O(b)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [suffix-tree, suffix-array, lcp-array]
see_also: [suffix-tree, suffix-tree-from-suffix-array, suffix-array, succinct-data-structures, compressed-suffix-array, inverted-index, full-text-index, position-heap]
sources:
  - paper: Juha Kärkkäinen and Esko Ukkonen, Sparse suffix trees, Computing and Combinatorics (COCOON 1996), LNCS 1090, doi:10.1007/3-540-61332-3_155
    locator: pages 219 to 230, the suffix tree of evenly spaced suffixes, its construction in linear time and O(n/k) space, and pattern search with it
  - paper: Arne Andersson, N. Jesper Larsson and Kurt Swanson, Suffix trees on words, Algorithmica 23(3), 1999, doi:10.1007/PL00009260
    locator: pages 246 to 260, the word suffix tree, a sparse suffix tree of the suffixes that start at word boundaries, built in space proportional to the number of words
  - paper: Paweł Gawrychowski and Tomasz Kociumaka, Sparse suffix tree construction in optimal time and space, Proceedings of the 28th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 2017), doi:10.1137/1.9781611974782.27
    locator: pages 425 to 439, construction of the sparse suffix tree of an arbitrary set of b suffixes in O(n) time and O(b) working space, with a randomized algorithm
---

A sparse suffix tree is the [suffix tree](/suffix-tree/) of a chosen subset of the suffixes of a text: the compacted trie of the $b$ suffixes that start at a given set of positions, for example every $k$-th position or the start of every word. It has at most $2b$ nodes instead of about $2n$, so it takes $O(b)$ words besides the text. A pattern that starts at a chosen position is found in $O(m + z)$ time, as in a full suffix tree; finding the other occurrences costs more, which is the price for the space.

## In plain words

A suffix tree indexes all $n$ suffixes of a text, and for a long text its node count, about two nodes per symbol, is the main cost. Often we do not need every suffix. In a text of words, a search usually starts at the start of a word. In other cases a sample of the suffixes is enough, and the rest can be recovered with more work.

A sparse suffix tree keeps only the chosen suffixes. It looks exactly like a suffix tree, just with fewer leaves, and searches in it work the same way. If every $k$-th suffix is kept, an occurrence at any position is found by also trying the pattern with its first $1, 2, \ldots, k - 1$ symbols cut off, and checking the cut symbols in the text.

## The abstract type

The sparse suffix tree implements a [full-text index](/full-text-index/) restricted to the chosen positions: given a pattern $P$, report the chosen positions $i$ where $P$ occurs. With evenly spaced positions and $m \ge k$, it also reports all occurrences. Like a suffix tree, it supports the other queries of a compacted trie, such as the longest common prefix of two chosen suffixes, through its node depths.

## Representation

Append an end marker $\$$ to the text, so that no chosen suffix is a prefix of another and each one ends at a leaf. The tree has one leaf per chosen position, and each internal node other than the root has at least two children. Each edge is labeled by an interval $[s, e)$ of the text, and each node $x$ stores its string depth $depth(x)$ and a chosen position $rep(x)$ in its subtree, so that $T[rep(x) \ldots rep(x) + depth(x) - 1]$ is the string of $x$.

**Invariant.** (P1) The leaves are exactly the chosen positions, and the leaf of $i$ spells $T[i \ldots] \$$. (P2) Each internal node other than the root has at least two children, whose edges start with distinct symbols. (P3) The string of each node is the concatenation of the edge labels from the root. With (P1) and (P2), there are at most $2b - 1$ nodes besides the root.

## Operations

```pseudo id=main
BUILD(T, chosen positions)
L1  sort the chosen suffixes; for neighbors in this order, compute their lcp h
L2  for each suffix s in order: pop the stack while the depth of its top is greater than h
L3      if the last node popped hangs below depth h: split its edge with a new node at depth h
L4      attach the leaf of s below the top of the stack, and push it

SEARCH(P)                                    ▷ chosen positions where P occurs
L5  walk from the root along P, comparing P with the edge labels; if a symbol differs, return ∅
L6  return the leaves below the point where P ends

SEARCH-ALL(P, k)                             ▷ chosen positions 0, k, 2k, …;  m ≥ k
L7  for r ← 0 to k − 1:  for each j in SEARCH(P[r …]):
L8      if j ≥ r and T[j − r … j − 1] = P[0 … r − 1]:  report j − r
```

Lines L1 to L4 are the stack construction of a suffix tree from a suffix array and its LCP array, as in [suffix tree from suffix array](/suffix-tree-from-suffix-array/), applied to the chosen suffixes only. In SEARCH-ALL, an occurrence at $i$ is found from the next chosen position $j = i + r$ with $0 \le r < k$: since $m \ge k > r$, the rest $P[r \ldots]$ is nonempty and starts at $j$, and the cut symbols are checked in the text.

## Example

Take $T = $ abracadabra and the positions $0, 3, 6, 9$, every third one. The chosen suffixes, in sorted order, are abracadabra$ (0), acadabra$ (3), dabra$ (6) and ra$ (9). The first two share the prefix a, so the tree is:

| node | edge label | children |
|---|---|---|
| root | | a, dabra$ (6), ra$ (9) |
| a | a | bracadabra$ (0), cadabra$ (3) |

It has 6 nodes; the full suffix tree of abracadabra$ has 12 leaves. SEARCH(a) ends at node a and returns the chosen positions 0 and 3. SEARCH-ALL(abra, 3) runs three searches. For $r = 0$, abra matches at 0. For $r = 1$, bra matches no chosen suffix. For $r = 2$, ra matches at 9, and the cut symbols $T[7 \ldots 8] = $ ab equal $P[0 \ldots 1]$, so 7 is reported. The answer is $\{0, 7\}$, the two occurrences of abra.

## Correctness

The construction is the one for full suffix trees applied to a sorted list of suffixes with the lcp of neighbors, and nothing in it needs the list to contain all suffixes; it gives (P1) to (P3). SEARCH reports the leaves below the locus of $P$, which are the chosen suffixes with prefix $P$. SEARCH-ALL finds each occurrence from the nearest chosen position at or after it. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

A search compares at most $m$ symbols on the way down and then visits the subtree of the locus; since internal nodes have at least two children, the subtree has fewer than $2z$ nodes for $z$ leaves, so SEARCH takes $O(m + z)$ time. SEARCH-ALL makes $k$ searches, and each candidate it receives is checked with at most $k - 1$ comparisons, so it takes $O(km + ck)$ time, where $c$ is the number of candidates; $c$ can exceed the number of occurrences.

The tree takes $O(b)$ words besides the text. Building it from the sorted chosen suffixes and their lcp values takes $O(b)$ time. Sorting the chosen suffixes is the hard part: comparing them directly takes up to $O(n b \log b)$ time, and building the full suffix array first needs $\Theta(n)$ space, which defeats the purpose. Kärkkäinen and Ukkonen (1996) build the tree of evenly spaced suffixes in $O(n)$ time and $O(n/k)$ space. For an arbitrary set of $b$ positions, Gawrychowski and Kociumaka (2017) give a randomized construction in $O(n)$ time and $O(b)$ working space.

## Variants

- **Evenly spaced suffixes.** Every $k$-th suffix, the case of Kärkkäinen and Ukkonen; the parameter $k$ trades space $O(n/k)$ against search time.
- **Word suffix trees.** The chosen positions are the starts of words. Andersson, Larsson and Swanson (1999) build this tree in space proportional to the number of words, which suits indexes over natural-language text, where queries start at word boundaries.
- **Sparse suffix arrays.** The sorted list of chosen suffixes, with their lcp values, gives the same search in $O(m \log b + z)$ time with less space per suffix; see the [suffix array](/suffix-array/).
- **Sampling in compressed indexes.** [Compressed suffix arrays](/compressed-suffix-array/) also keep a sample of the suffix positions, but for a different purpose: to recover the position of a match, not to search.

## When to use it

Use a sparse suffix tree when the queries only need occurrences at known positions, such as word starts, or when memory for a full suffix tree is not available and a slower search is acceptable. If queries are whole words, an [inverted index](/inverted-index/) is simpler. If all occurrences are needed and memory is tight, a compressed index such as the FM-index is usually the better trade-off.

## Pitfalls

- **Short patterns.** SEARCH-ALL with spacing $k$ misses occurrences of patterns shorter than $k$ that lie between two chosen positions. These need a separate method, such as a scan of the text or a small index of short strings.
- **End marker.** Without it, a chosen suffix that is a prefix of another chosen suffix ends inside an edge and has no leaf.
- **Construction space.** Building the full suffix tree or suffix array and then pruning it is correct, but it needs the $\Theta(n)$ space that the sparse tree was meant to avoid.
- **Unchecked candidates.** In SEARCH-ALL, a match of $P[r \ldots]$ at $j$ is only a candidate; the $r$ symbols before $j$ must be checked.

## Implementations

The Python class sorts the chosen suffixes, computes the lcp of neighbors by direct comparison, and builds the tree with the stack scan; nodes store edge intervals, the string depth and a representative position. SEARCH walks the edges and collects the leaves with an explicit stack, and SEARCH-ALL implements the evenly spaced case. check_invariant verifies (P1) to (P3) and the node bound. The tests replay the example, check the full set of positions against a scan, and compare 600 random texts and samples with a direct search.

## History

Kärkkäinen and Ukkonen (1996) introduced sparse suffix trees for evenly spaced suffixes, with a linear-time construction in sublinear space. Andersson, Larsson and Swanson (1999) studied the word suffix tree for suffixes at word boundaries. The construction for an arbitrary set of positions in small space was studied in several later papers, and Gawrychowski and Kociumaka (2017) reached $O(n)$ time and $O(b)$ space.

## References
