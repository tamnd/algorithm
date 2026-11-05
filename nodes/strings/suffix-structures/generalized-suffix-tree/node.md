---
tag: 4HGXBV
kind: data-structure
slug: generalized-suffix-tree
name: Generalized suffix tree
aliases:
- suffix tree of a set of strings
area: strings/suffix-structures
level: core
summary: A suffix tree over a set of strings, used for multi-string problems such as longest common substring.
model: word-ram
complexity:
  vars: {N: the total length of the strings plus the number of strings, m: the number of strings, q: the length of the pattern, k: the number of occurrences}
  time: {worst: O(N)}
  space: {extra: Θ(N)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [suffix-tree, suffix-array, lcp-array]
see_also: [longest-common-substring, generalized-suffix-automaton, suffix-tree-from-suffix-array, document-listing, ukkonen-algorithm, matching-statistics, sentinel-character, lowest-common-ancestor]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 6.4 (generalized suffix tree for a set of strings), Section 7.4 (longest common substring of two strings) and Section 7.6 (common substrings of more than two strings)
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design, Cambridge University Press, 2015
    locator: Chapter 8 (Classical indexes), the generalized suffix tree and the suffix tree built from the suffix array and the LCP array
  - paper: doi:10.1007/3-540-48194-X_17
    title: Toru Kasai, Gunho Lee, Hiroki Arimura, Setsuo Arikawa and Kunsoo Park, Linear-time longest-common-prefix computation in suffix arrays and its applications, CPM 2001, LNCS 2089
    locator: pages 181 to 192, the bottom-up traversal of the suffix tree with the suffix array and the LCP array
---

A generalized suffix tree of strings $S_0, \ldots, S_{m-1}$ is the [suffix tree](/suffix-tree/) of all their suffixes together: each leaf is one suffix of one string and is labeled with the string and the offset. It is the suffix tree of $S_0 \$_0 S_1 \$_1 \cdots S_{m-1} \$_{m-1}$, with distinct [separators](/sentinel-character/), where each leaf edge is cut after its first separator. It has $\Theta(N)$ nodes for a total length $N$ and is built in $O(N)$ time for an integer alphabet. It answers questions about many strings at once, such as the [longest common substring](/longest-common-substring/) and which strings contain a pattern.

## In plain words

A suffix tree of one word is a tree of all its endings, where shared starts are stored once. For many words, put all the endings of all the words in one tree, and write on each leaf which word and which position it comes from.

Now a pattern search walks down from the root once and finds the pattern in every word at the same time. A branch point whose leaves come from all the words spells a piece that every word contains, and the deepest such point is their longest common piece.

To build it, join the words with a different end mark after each word, sort all endings of the joined text, and build the tree from the sorted list with a stack. Each end mark stops a leaf so that it never runs into the next word.

## The abstract type

The structure is static. It is built from the list of strings and supports:

- `find(P)`: all pairs $(k, j)$ with $S_k[j \ldots j+|P|-1] = P$, for a nonempty pattern $P$;
- `strings_containing(P)`: the ids $k$ of the strings that contain $P$, the [document listing](/document-listing/) query;
- `longest_common_substring(k)`: a longest string that occurs in at least $k$ of the $m$ strings;
- a walk of the nodes, each with its string depth and its leaves, which many other questions use, such as the [matching statistics](/matching-statistics/) and all-pairs suffix-prefix overlaps.

## Representation

The strings are over a general ordered alphabet; the symbols are only compared, and the build maps them to integer codes in their order. Positions are 0-based. The separators $\$_0 < \$_1 < \cdots < \$_{m-1}$ are $m$ new symbols, smaller than all letters, and each one occurs once. Let

$$Z = S_0 \$_0 S_1 \$_1 \cdots S_{m-1} \$_{m-1}, \qquad |Z| = N = m + \sum_k |S_k|.$$

For a position $p$ of $Z$ that holds a letter, the *terminated suffix* $X_p$ runs from $p$ to the first separator after it. The tree is the compacted trie of these $N - m$ strings. Because each ends with a separator that occurs nowhere else, none is a prefix of another, so each one ends at its own leaf.

Each node $v$ stores its string depth $d(v)$, the length of its path label, and one position $pos(v)$ of $Z$ where the path label starts. The edge into $v$ from its parent $u$ is $Z[pos(v) + d(u) \ldots pos(v) + d(v) - 1]$, two integers in place of a copy of the string. The children are in a map keyed by the first symbol of the edge. A leaf stores its label $(k, j)$.

**Invariant.** The root has depth 0. Each internal node other than the root has at least two children, with different first symbols. For each edge $u \to v$, $d(v) > d(u)$, and the path label of $v$ starts with the path label of $u$. There are $N - m$ leaves, one for each nonempty suffix $S_k[j \ldots]$, and the path label of that leaf is $S_k[j \ldots] \$_k$.

The path labels of the internal nodes are exactly the *right-branching* substrings: the strings $u$ that are followed by two different symbols in the strings, where the end of $S_k$ counts as the symbol $\$_k$.

## Operations

```pseudo id=main
GST-BUILD(S_0, .., S_{m−1})              ▷ N = |Z|; positions are 0-based
L1  Z ← S_0 $_0 S_1 $_1 ⋯ S_{m−1} $_{m−1}; SA, LCP ← suffix array and LCP array of Z
L2  root ← node of depth 0; stack ← [root]
L3  for i ← m to N − 1 do                 ▷ ranks 0 .. m − 1 hold the suffixes that start with a separator
L4      p ← SA[i]; h ← LCP[i]
L5      while depth(top) > h do last ← pop
L6      if depth(top) < h then             ▷ the branch point lies inside the edge to last
L7          v ← new node of depth h; move last below v
L8          put v below top in the place of last; push v
L9      leaf ← new leaf of depth e − p + 1, labeled (k, p − start of S_k), where S_k holds p and ends before e
L10     put leaf below top; push leaf
```

**Build.** Line L1 sorts the suffixes of $Z$. The separators are the smallest symbols, so ranks $0$ to $m - 1$ hold the suffixes that start with one, and the loop skips them. The remaining suffixes sort as their terminated suffixes, and their LCP values never reach a separator, because a separator occurs once. The loop then builds the compacted trie of a sorted list of strings, as in the [suffix tree from a suffix array](/suffix-tree-from-suffix-array/): the stack holds the path to the last leaf; the new leaf branches off this path at depth $h = LCP[i]$; line L5 climbs to that depth, and lines L7 and L8 split an edge when no node is there yet.

**Find.** Walk down from the root and compare $P$ with the edge labels, reading them from $Z$. If the walk ends inside or at the end of an edge to $v$, the occurrences are the leaf labels below $v$. The cost is $O(q)$ for the walk with hashed children, plus $O(k)$ for the $k$ leaves below.

**Longest common substring of $k$ strings.** For each node, find the set of string ids of the leaves below it, bottom-up. The deepest internal node whose set has at least $k$ ids spells the answer. For a leaf, the depth without its separator counts. The implementation keeps each set as a machine-integer mask, which costs $O(N \lceil m / w \rceil)$ time on words of $w$ binary digits. The method of Gusfield (Section 7.6), based on lowest common ancestors, finds the number of distinct ids at every node in $O(N)$ time.

## Example

The strings are $S_0 = \texttt{xabxa}$ and $S_1 = \texttt{babxba}$, so $Z = \texttt{xabxa\$}_0\texttt{babxba\$}_1$ and $N = 13$. The ranks 0 and 1 hold the separator suffixes $\$_0 \cdots$ and $\$_1$. The table lists the other ranks with the terminated suffixes.

| rank | $SA$ | $LCP$ | terminated suffix | leaf label |
|---|---|---|---|---|
| 2 | 4 | 0 | a\$0 | (0, 4) |
| 3 | 11 | 1 | a\$1 | (1, 5) |
| 4 | 1 | 1 | abxa\$0 | (0, 1) |
| 5 | 7 | 3 | abxba\$1 | (1, 1) |
| 6 | 10 | 0 | ba\$1 | (1, 4) |
| 7 | 6 | 2 | babxba\$1 | (1, 0) |
| 8 | 2 | 1 | bxa\$0 | (0, 2) |
| 9 | 8 | 2 | bxba\$1 | (1, 2) |
| 10 | 3 | 0 | xa\$0 | (0, 3) |
| 11 | 0 | 2 | xabxa\$0 | (0, 0) |
| 12 | 9 | 1 | xba\$1 | (1, 3) |

At rank 3, $h = 1$: the stack is [root, leaf (0, 4)], line L5 pops the leaf, and lines L7 and L8 put a node `a` of depth 1 between the root and that leaf. At rank 5, $h = 3$ splits the edge to leaf (0, 1) with a node `abx`. At rank 6, $h = 0$ pops back to the root. The result has 11 leaves and 8 internal nodes with the root:

| internal node | depth | children (edge labels) | string ids below |
|---|---|---|---|
| root | 0 | a, b, x | 0, 1 |
| a | 1 | \$0, \$1, bx | 0, 1 |
| abx | 3 | a\$0, ba\$1 | 0, 1 |
| b | 1 | a, x | 0, 1 |
| ba | 2 | \$1, bxba\$1 | 1 |
| bx | 2 | a\$0, ba\$1 | 0, 1 |
| x | 1 | a, ba\$1 | 0, 1 |
| xa | 2 | \$0, bxa\$0 | 0 |

The deepest node with both ids is `abx`, depth 3, so the longest common substring is `abx`. The node `ba` has only id 1: `ba` occurs twice in $S_1$ but not in $S_0$. `find("bx")` walks root, `b`, `bx` and returns $(0, 2)$ and $(1, 2)$. The leaf $(0, 4)$ hangs from `a` with the edge $\$_0$: the suffix `a` of $S_0$ ends at a node, which only the separator makes into a leaf.

## Correctness

Two facts carry the proof. First, the suffixes of $Z$ that start with letters sort as their terminated suffixes, and their adjacent LCP values are those of the terminated suffixes, because the unique separators stop each common prefix. Second, the stack loop builds the compacted trie of any sorted, prefix-free list of strings from the LCP values of adjacent strings: the new string branches off the path to the previous one at exactly the depth $h$, and the stack is that path. So the result is the compacted trie of the terminated suffixes, which is the generalized suffix tree. A pattern without separators occurs at $(k, j)$ exactly when it is a prefix of the terminated suffix at that place, so the leaves below its locus are its occurrences. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The costs are in the [word RAM](/word-ram/), with positions in a word and children in hash maps.

| operation | time | space |
|---|---|---|
| build, given $SA$ and $LCP$ of $Z$ | $O(N)$ | $\Theta(N)$ words |
| build from the strings | $O(N)$ for an integer alphabet, $O(N \log N)$ comparisons for a general ordered alphabet | $\Theta(N)$ words |
| `find(P)` | $O(q + k)$ | $O(1)$ more |
| `strings_containing(P)` | $O(q + k)$ with a scan of the leaves, $O(q)$ plus the output with a [document listing](/document-listing/) structure | |
| `longest_common_substring(k)` | $O(N)$ with Gusfield's method | $O(N)$ |

The loop pushes at most two nodes in each round, so it has at most $2(N - m)$ pops in total. The tree has $N - m$ leaves and fewer than $N - m$ internal nodes other than the root. The implementation builds the suffix array by prefix doubling with library sorts, which takes $O(N \log^2 N)$ time; a linear [suffix array construction](/suffix-array-construction/) such as [SA-IS](/sa-is/) and [Kasai's algorithm](/kasai-algorithm/) give the linear bound.

## Variants

- **One leaf for equal suffixes.** Gusfield builds the tree with [Ukkonen's algorithm](/ukkonen-algorithm/), one string after the other, with one end mark for all strings. A suffix that occurs in several strings is then one leaf with a list of labels. The tree has fewer leaves, and the separators are not stored in the labels.
- **Online, one string at a time.** Ukkonen's algorithm extends the tree with each new string, so the set can grow.
- **Suffix array form.** The generalized [suffix array](/suffix-array/) and LCP array of $Z$, with an array of string ids, answer most of the same questions with less memory, by scans of the LCP array; the [longest common substring](/longest-common-substring/) page uses this form.
- **Generalized suffix automaton.** The [generalized suffix automaton](/generalized-suffix-automaton/) of the set is the automaton form; its suffix-link tree is closely related to the generalized suffix tree of the reversed strings.
- **Color set size.** The number of distinct string ids below every node, which Gusfield computes in linear time with [lowest common ancestor](/lowest-common-ancestor/) queries between leaves of the same string that are adjacent in leaf order.

## When to use it

Use it when a question involves several strings and their common or distinct parts: the longest substring common to $k$ of $m$ strings, the strings that contain a pattern, all exact matches between a set of short reads and a reference, or the overlaps of the suffixes of one read with the prefixes of another in genome assembly. For one string, use a plain [suffix tree](/suffix-tree/). When memory matters, the generalized suffix array with the LCP array does most of the same jobs in two words per symbol, several times less than a pointer-based suffix tree.

## Pitfalls

- **One shared end mark without care.** With the same separator after each string, two suffixes from different strings can share a common prefix that runs through the separator and into the next string, and the tree then has false paths. Use distinct separators, or cut each label at the first separator.
- **Separators in the alphabet.** The separators must not occur in any string. With byte strings, there are not enough unused bytes for many strings; use integer codes as the implementation does.
- **Counting leaves for $k$ strings.** A node with $k$ leaves below it need not have $k$ distinct strings below it, as the node `ba` above shows with two leaves from $S_1$. Count distinct ids.
- **Leaf depth includes the separator.** The path label of a leaf ends with its separator. When a leaf is the answer to a question about substrings, subtract 1 from its depth.
- **Empty strings.** An empty $S_k$ adds a separator but no leaf.

## Implementations

The Python class builds the suffix array and the LCP array of $Z$ with integer codes, and then the tree with an explicit stack; the walks in `find` and `longest_common_substring` are iterative. Node data are in parallel lists, and children in a dictionary for each node.

## History

Gusfield's 1997 book made the generalized suffix tree a standard tool, with the longest common substring and the common substrings of $k$ strings among its first applications. The method that counts the distinct strings below each node in linear time is due to Hui in 1992, under the name color set size. The construction from the suffix array and the LCP array follows the bottom-up traversal of Kasai and coauthors in 2001 and the enhanced suffix array of Abouelhoda, Kurtz and Ohlebusch in 2004.

## References
