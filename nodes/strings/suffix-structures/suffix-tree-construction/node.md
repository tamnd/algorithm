---
tag: QNKKR5
kind: problem
slug: suffix-tree-construction
name: Suffix tree construction
aliases:
- building suffix trees
area: strings/suffix-structures
level: core
summary: Build the suffix tree of a string in time linear in its length.
prereqs: [suffix-tree]
see_also: [ukkonen-algorithm, mccreight-algorithm, weiner-algorithm, suffix-tree-from-suffix-array, suffix-array-construction, suffix-link, suffix-tree-size-theorem, sparse-suffix-tree]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 6, Linear-time construction of suffix trees (Ukkonen, Weiner and McCreight, and the dependence on the alphabet)
  - paper: doi:10.1109/SFCS.1997.646102
    title: Martin Farach, Optimal suffix tree construction with large alphabets, FOCS 1997
    locator: pages 137 to 143; linear time for an integer alphabet by recursion on odd and even suffixes
  - paper: doi:10.1145/355541.355547
    title: Martin Farach-Colton, Paolo Ferragina and S. Muthukrishnan, On the sorting-complexity of suffix tree construction, Journal of the ACM 47(6), 2000
    locator: pages 987 to 1011; suffix tree construction has the complexity of sorting, in the RAM, external memory and other models
  - paper: doi:10.1007/pl00009177
    title: Robert Giegerich and Stefan Kurtz, From Ukkonen to McCreight and Weiner, a unifying view of linear-time suffix tree construction, Algorithmica 19(3), 1997
    locator: pages 331 to 353
  - paper: doi:10.1002/(sici)1097-024x(199911)29:13<1149::aid-spe274>3.0.co;2-o
    title: Stefan Kurtz, Reducing the space requirement of suffix trees, Software Practice and Experience 29(13), 1999
    locator: pages 1149 to 1179
---

Suffix tree construction is the problem of building the [suffix tree](/suffix-tree/) of a string: the compact trie of all its suffixes, with edge labels stored as index pairs. The tree has $O(n)$ nodes for a string of length $n$, by the [suffix tree size theorem](/suffix-tree-size-theorem/), so linear time is the goal. Weiner (1973), McCreight (1976) and Ukkonen (1995) reach $O(n)$ time for a constant alphabet with [suffix links](/suffix-link/); Farach (1997) reaches $O(n)$ for an integer alphabet. Over a general ordered alphabet, with the children in sorted order, the problem needs $\Theta(n \log n)$ comparisons, as sorting does.

## In plain words

The task is to build the tree of all endings of a text, the tree where each branch point is a place where endings go different ways. Inserting the endings one by one, each from the top of the tree, is easy but slow: each insert can read almost the whole text again.

The fast methods avoid reading the same letters twice. After they put in one ending, they jump straight to the place for the next ending by an arrow stored in the tree. The arrows and some careful counting make the total work grow only in step with the length of the text.

## Definition

**Input.** A string $S = S[0 \ldots n-1]$, $n \ge 0$, 0-based, over an alphabet $\Sigma$. The models are:

- **constant alphabet:** $|\Sigma| = O(1)$, and each node can keep an array of $|\Sigma|$ children;
- **integer alphabet:** $\Sigma \subseteq \{0, \ldots, n^c\}$ for a constant $c$, so symbols can be sorted by [radix sort](/radix-sort/) in $O(n)$ time;
- **general ordered alphabet:** symbols are only compared, at unit cost.

**Output.** The suffix tree of $T = S\$$, where the [sentinel](/sentinel-character/) $\$$ does not occur in $S$: a rooted tree with $n + 1$ leaves, one for each suffix $T_i = T[i \ldots n]$, labeled $i$; each edge labeled by a pair $(a, b)$ that stands for $T[a \ldots b - 1]$, nonempty; the labels of the child edges of a node start with distinct symbols; each inner node other than the root has at least two children; and the path from the root to leaf $i$ spells $T_i$. The tree is unique up to the choice of index pairs for equal labels and the order of children. When the output must have the children of each node sorted by first symbol, say so: it is the *ordered* suffix tree.

Most algorithms also output the string depth of each node and a [suffix link](/suffix-link/) for each inner node, because users of the tree need them.

## Variants

- **Online construction.** Read $S$ one symbol at a time, and keep the tree of the prefix read so far. Ukkonen's algorithm does this, with the implicit tree, in which some suffixes end inside edges or at inner nodes.
- **Construction from the suffix array.** Given $SA$ and the LCP array, build the tree by one left-to-right scan with a stack. See [suffix tree from suffix array](/suffix-tree-from-suffix-array/).
- **Generalized suffix tree.** Build the tree of the suffixes of a set of strings, each ending with its own marker. See the [generalized suffix tree](/generalized-suffix-tree/).
- **Sparse suffix tree.** Only the suffixes that start at $b$ given positions, in $O(b)$ space if possible. See the [sparse suffix tree](/sparse-suffix-tree/).
- **Compressed and external-memory construction.** Build a compressed suffix tree in space close to the compressed text, or build a tree larger than the main memory with few block transfers.

## Examples

| $S$ | leaves | inner nodes (root first) | nodes |
|---|---|---|---|
| (the empty string) | 1 | root | 2 |
| banana | 7 | root, a, na, ana | 11 |
| abab | 5 | root, b, ab | 8 |
| aaaa | 5 | root, a, aa, aaa | 9 |
| abcd | 5 | root | 6 |

The table lists the right-branching substrings of $S\$$, which are the inner nodes. For $\texttt{aaaa}$, each $\texttt{a}^k$ with $1 \le k \le 3$ is followed by $\texttt{a}$ and by $\$$, and the tree reaches the upper bound $2n + 1$. For $\texttt{abcd}$ the root has 5 leaf children, the lower bound $n + 2$.

**The naive build is quadratic.** Inserting $T_0, T_1, \ldots$ each from the root reads, for $S = \texttt{a}^n$, about $n - i$ symbols to place $T_i$, about $n^2/2$ symbols in all. For random text over a fixed alphabet, the inserts read about $\log n$ symbols each on average, so the naive build takes $O(n \log n)$ expected time.

## Known algorithms

| algorithm | time | alphabet | order of the suffixes | notes |
|---|---|---|---|---|
| naive insertion | $O(n^2)$ worst | any | $T_0, T_1, \ldots$ | the test oracle |
| [Weiner](/weiner-algorithm/), 1973 | $O(n)$ | constant | from the shortest | uses reverse suffix links |
| [McCreight](/mccreight-algorithm/), 1976 | $O(n)$ | constant | from the longest | suffix links, rescan and scan |
| [Ukkonen](/ukkonen-algorithm/), 1995 | $O(n)$ | constant | online, by prefixes | suffix links, open leaf edges |
| Farach, 1997 | $O(n)$ | integer | odd and even suffixes | recursion on pairs, then a merge |
| from $SA$ and LCP | $O(n)$ after $SA$ | integer | by $SA$ | with [SA-IS](/sa-is/) and [Kasai](/lcp-array-construction/) |

With ordered child maps, as balanced trees or sorted lists, Weiner, McCreight and Ukkonen run in $O(n \log |\Sigma|)$ time; with hash tables, in $O(n)$ expected time for any alphabet, but the children are not sorted. Giegerich and Kurtz show that the three classic algorithms are closely related. In practice, building the suffix array with SA-IS and then the tree from the arrays is often the fastest route for large texts, and Kurtz's 1999 implementation techniques reduce the space of the tree to about 10 bytes for each text symbol on typical inputs.

## Bounds

- **Upper bound, constant or integer alphabet.** $O(n)$ time, by the algorithms above. This is optimal, since the output has $\Theta(n)$ size.
- **Upper bound, general ordered alphabet.** $O(n \log n)$: sort the symbols, replace them by ranks in $\{0, \ldots, n-1\}$, and run Farach's algorithm, or run McCreight or Ukkonen with balanced child maps in $O(n \log \min(n, |\Sigma|))$.
- **Lower bound, ordered tree.** $\Omega(n \log n)$ comparisons in the [comparison model](/comparison-model/). If the symbols of $S$ are pairwise distinct, the root of the ordered tree has $n + 1$ leaf children in the order of the first symbols, so the tree sorts the symbols, and [sorting](/sorting-problem/) needs $\lceil \lg n! \rceil$ comparisons.
- **Sorting complexity in all models.** Farach-Colton, Ferragina and Muthukrishnan show that the problem has the same complexity as sorting the symbols, in the RAM, in external memory, and in other models.

## Reductions

- **Suffix sorting reduces to it.** A depth-first walk of the ordered tree, children by first symbol with $\$$ first, lists the leaves in [suffix array](/suffix-array/) order in $O(n)$ time.
- **It reduces to suffix sorting.** From $SA$ and the LCP array, a stack-based scan builds the tree in $O(n)$ time, so suffix tree construction and [suffix array construction](/suffix-array-construction/) have the same complexity up to $O(n)$ extra time.
- **Sorting reduces to it.** As in the lower bound: $n$ distinct keys, written as a string, are sorted by the order of the root's children.
- **Suffix automaton.** The [suffix automaton](/suffix-automaton/) of the reversed string, built online, has as its suffix-link tree the suffix tree of $S$; this gives another linear-time construction for a constant alphabet.

## Applications

- **Exact pattern matching** in $O(m)$ time for a constant alphabet, and reporting in $O(m + occ)$; see the [suffix tree](/suffix-tree/).
- **Repeats and unique substrings.** The [longest repeated substring](/longest-repeated-substring/), [maximal repeats](/maximal-repeats/) and [shortest unique substrings](/shortest-unique-substring/) come from one walk over the tree.
- **Common substrings.** The longest common substring of two strings, via the generalized tree; see [longest common substring via suffix tree](/lcs-via-suffix-tree/).
- **Matching statistics and approximate matching.** [Matching statistics](/matching-statistics/) with suffix links, and seeds for approximate matching in bioinformatics.
- **Data compression.** [Lempel-Ziv factorization](/lempel-ziv-factorization/) can be computed in linear time with a suffix tree.

## References
