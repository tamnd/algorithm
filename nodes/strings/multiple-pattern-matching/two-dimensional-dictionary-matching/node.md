---
tag: BRJ52T
kind: problem
slug: two-dimensional-dictionary-matching
name: Two-dimensional dictionary matching
aliases:
- 2D multiple pattern matching
area: strings/multiple-pattern-matching
level: research
summary: Find all occurrences of a set of rectangular 2D patterns in a 2D text.
model: word-ram
complexity:
  vars: {R: the number of text rows, C: the number of text columns, M: the total size of the patterns, z: the number of occurrences}
  time: {build: O(M), search: O(R·C + z)}
  space: {extra: O(M + C)}
prereqs: [dictionary-matching, multiple-string-matching]
see_also: [bird-baker, dynamic-dictionary-matching, aho-corasick, knuth-morris-pratt, suffix-tree, karp-rabin-multiple-patterns, compressed-suffix-tree]
sources:
  - paper: doi:10.1137/0207043
    title: Theodore P. Baker, A technique for extending rapid exact-match string matching to arrays of more than one dimension, SIAM Journal on Computing 7(4) (1978), 533-541
    locator: the abstract and the method (a fixed set of pattern arrays matched on-line in linear time by reduction to string matching, with extensions to arrays of different sizes, nonrectangular arrays and more dimensions)
  - paper: doi:10.1137/S0097539792231982
    title: Raffaele Giancarlo, A generalization of the suffix tree to square matrices, with applications, SIAM Journal on Computing 24(3) (1995), 520-562
    locator: the abstract (the Lsuffix tree, and the bounds for two-dimensional dictionary matching of square patterns of different sizes)
  - paper: doi:10.1137/S0097539792226321
    title: Amihood Amir, Gary Benson and Martin Farach, An alphabet independent approach to two-dimensional pattern matching, SIAM Journal on Computing 23(2) (1994), 313-323
    locator: the abstract (the dependence of earlier algorithms on an ordered alphabet, and the O(n^2) text scan)
  - paper: doi:10.1006/inco.1995.1030
    title: Ramana M. Idury and Alejandro A. Schäffer, Multiple matching of rectangular patterns, Information and Computation 117(1) (1995), 78-90
    locator: the dictionary matching of rectangular patterns of different sizes
  - url: https://arxiv.org/abs/1302.0072
    title: Shoshana Marcus and Dina Sokol, Dynamic 2D dictionary matching in small space, arXiv 1302.0072 (2013)
    locator: Section 1 (related work on two-dimensional dictionary matching and the problem definition for patterns of uniform width) and Section 3 (the Bird / Baker algorithm and its dynamic version)
---

Two-dimensional dictionary matching finds every occurrence of a set of matrix patterns in a matrix text: each pattern is a rectangle of symbols, and it occurs where it equals a block of the text. For patterns that all have the same width, the [Bird-Baker](/bird-baker/) method solves it in time linear in the text, the patterns and the output, by naming the pattern rows with [Aho-Corasick](/aho-corasick/) and then matching columns of names. Patterns of many shapes are harder, because the occurrences of a small square and of a larger square at one corner do not form a sequence of rows of one length. Research on the problem has studied square patterns of different sizes, independence of the alphabet, small space and dictionaries that change.

## In plain words

You have a big picture made of small cells, and a list of small pictures. You want to find every place where a small picture appears, cell for cell, inside the big one. A program that recognizes known icons in a screenshot, or known shapes in a game board, does this.

One small picture at a time is easy to describe but slow when the list is long. The goal is to look at each cell of the big picture only a few times, whatever the number of small pictures. When all small pictures have the same width, a neat trick works: name each row of each small picture, write these names into the big picture, and then search down the columns for each small picture's list of row names. Small pictures of many sizes need more complex tools.

## Definition

**Input.** A text $T$ with $R$ rows and $C$ columns, and patterns $P_0, \ldots, P_{k-1}$, where $P_j$ has $m_j$ rows and $w_j$ columns. All rows of one matrix have the same length. $M = \sum_j m_j w_j$ is the total size of the patterns. Symbols come from an alphabet $\Sigma$; the model is either an ordered alphabet, with comparisons, or a general alphabet with hashing.

**Output.** All triples $(r, c, j)$ such that $T[r + i][c + t] = P_j[i][t]$ for all $0 \le i < m_j$ and $0 \le t < w_j$, so that $(r, c)$ is the top-left corner of the occurrence.

**Conventions.** Indices are 0-based, and occurrences may overlap. A pattern listed twice is reported once for each index. A pattern with no rows occurs at every $(r, c)$ with $0 \le r \le R$ and $0 \le c \le C$, and a pattern of $m$ empty rows at every $(r, c)$ with $0 \le r \le R - m$ and $0 \le c \le C$.

**Costs.** The dictionary may be preprocessed once in time and space that depend on $M$ and $k$, and then texts are searched. The target is $O(M)$ preprocessing and $O(RC + z)$ search, where $z$ is the number of occurrences.

## Variants

- **Uniform width or uniform height.** All patterns have the same number of columns, or the same number of rows. This is the case of Bird-Baker and of the dynamic algorithm of Marcus and Sokol.
- **Square patterns of different sizes.** Pattern $j$ is an $m_j \times m_j$ square. The Lsuffix tree of Giancarlo and earlier work of Amir and Farach treat this case.
- **Rectangles of arbitrary sizes.** The most general case, treated by Idury and Schäffer.
- **Dynamic dictionaries.** Patterns are inserted and deleted, as in [dynamic dictionary matching](/dynamic-dictionary-matching/).
- **Small space.** The structure must take space close to that of a compressed dictionary, as in the work of Neuburger and Sokol and of Marcus and Sokol.
- **Other shapes and dimensions.** Baker extends his technique to nonrectangular patterns and to arrays of more than two dimensions.

## Examples

The text has the 4 rows abaab, babba, abaab and aabab. The dictionary has five patterns, of three widths:

| $j$ | rows of $P_j$ | size | occurrences $(r, c)$ |
|---|---|---|---|
| 0 | ab, ba | $2 \times 2$ | (0, 0), (0, 3), (1, 1) |
| 1 | aba | $1 \times 3$ | (0, 0), (2, 0), (3, 1) |
| 2 | a, b, a | $3 \times 1$ | (0, 0), (0, 2), (0, 3), (1, 1) |
| 3 | ba, ab | $2 \times 2$ | (0, 1), (1, 0), (1, 3), (2, 1) |
| 4 | ab, ba | $2 \times 2$ | (0, 0), (0, 3), (1, 1) |

There are $z = 17$ occurrences. They overlap: $P_0$ at $(0, 0)$ and $P_3$ at $(0, 1)$ share the cells $(0, 1)$ and $(1, 1)$. $P_4$ equals $P_0$ and is reported under its own index. The patterns 0, 3 and 4 have width 2, so one Bird-Baker pass with the row names ab and ba finds them; the patterns 1 and 2 need one pass each, for the widths 3 and 1.

## Known algorithms

- **Naive search.** Compare each pattern at each corner: $O(RC \cdot M)$ time in the worst case, no preprocessing.
- **Bird-Baker.** For patterns of one width, name the distinct pattern rows, run an Aho-Corasick automaton of the rows along each text row, and run a second Aho-Corasick automaton of the columns of names down each text column. Preprocessing $O(M)$ and search $O(RC + z)$ with hashed transitions; for $d$ distinct widths, one pass each, $O(d \cdot RC + z)$. See [Bird-Baker](/bird-baker/).
- **Fingerprints.** For each distinct pattern shape, keep a [hash table](/hash-table/) of the fingerprints of the patterns of that shape, and compute the fingerprint of every text block of that shape with a rolling hash along the rows and then along the columns, as in [Karp-Rabin for many patterns](/karp-rabin-multiple-patterns/). Expected $O(s \cdot RC + M + z)$ time for $s$ distinct shapes, with a small chance of false matches unless each match is verified.
- **Square patterns: the Lsuffix tree (Giancarlo).** Read each square as a sequence of L-shaped pieces, so that the $i \times i$ top-left squares of a matrix are the prefixes of one string, and build a suffix tree of these strings. For square patterns of sizes $m_j$, with $t = \sum_j m_j^2$ and $\bar{t} = \sum_j m_j$, preprocessing takes $O(t \log |\Sigma| + \bar{t} \log \bar{t})$ time and $O(t)$ space, and an $n \times n$ text is searched in $O(n^2 (\log |\Sigma| + \log \bar{t}) + z)$ time, on an ordered alphabet.
- **Rectangles of different sizes (Idury and Schäffer).** An algorithm for rectangular patterns of arbitrary sizes, which also allows changes to the dictionary; Marcus and Sokol note that it uses linear working space and more than linear time.
- **Small space (Neuburger and Sokol; Marcus and Sokol).** Succinct static algorithms for patterns of one size with no slowdown, and a dynamic algorithm for patterns of uniform width whose only slowdown is the time $\tau \le \log^2 \ell$ of a query to a compressed self-index of the dictionary.
- **Dynamic square patterns.** The algorithms of Amir, Farach, Idury, La Poutré and Schäffer, of Choi and Lam, and the dynamic form of the Lsuffix tree, which Marcus and Sokol summarize as having an $O(\log \ell)$ or $O(\log^2 \ell)$ slowdown.

## Bounds

- **Search.** In the worst case, a search needs $\Omega(RC + z)$ time: the output has $z$ triples, and with a $1 \times 1$ pattern every text cell must be read, since changing an unread cell changes the output. Bird-Baker meets this bound for patterns of one width, with hashed transitions.
- **Preprocessing.** $\Omega(M)$, since each pattern symbol must be read.
- **Alphabet.** Algorithms that branch on symbols in a trie or a suffix tree pay $O(\log |\Sigma|)$ per step with an ordered alphabet. For a single pattern, Amir, Benson and Farach give an $O(n^2)$ text scan for an $n \times n$ text that needs only equality tests between symbols, while their preprocessing still uses the order.
- **Many shapes.** The bounds cited above for squares of different sizes have a logarithmic factor in the dictionary size on the text scan, and a factor $d$ or $s$ appears in the simple methods for $d$ widths or $s$ shapes.

## Reductions

- **From one-dimensional dictionary matching.** A one-dimensional dictionary is a set of $1 \times w_j$ patterns in a $1 \times n$ text.
- **To one-dimensional dictionary matching.** For patterns of one width, naming the rows reduces the problem to two one-dimensional dictionary problems, one on the text rows and one on the columns of names. Baker phrases this as a reduction to string matching.
- **To one-dimensional dynamic dictionary matching.** Under the same reduction, a dynamic one-dimensional structure for both steps gives a dynamic two-dimensional one; Marcus and Sokol use the algorithm of Sahinalp and Vishkin this way.
- **Squares to strings.** Giancarlo's L-shaped reading turns each square into a string whose prefixes are its top-left squares, so a suffix tree over these strings handles squares of all sizes at once.

## Applications

- **Image recognition.** Finding known small images inside a large image; Marcus and Sokol name image identification software as a direct application.
- **Image processing and visual databases.** Giancarlo motivates his structure by problems of low-level image processing and visual databases.
- **Board games and edge detection.** Baker names edge detection and board games among the uses of his technique.

## References
