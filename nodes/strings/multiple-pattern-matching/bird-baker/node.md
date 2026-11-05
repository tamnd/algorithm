---
tag: WZE4CC
kind: algorithm
slug: bird-baker
name: Bird-Baker algorithm
aliases:
- Bird's algorithm
- Baker's algorithm
area: strings/multiple-pattern-matching
level: research
summary: Two-dimensional matching that names the pattern rows with Aho-Corasick and then matches the columns of row names with a second string matcher.
solves: [two-dimensional-dictionary-matching]
model: word-ram
complexity:
  vars: {R: the number of text rows, C: the number of text columns, M: the total size of the patterns, d: the number of distinct pattern widths, z: the number of occurrences}
  time: {build: O(M), search: O(d·R·C + z)}
  space: {extra: O(M + C)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1977
  people: [Richard S. Bird, Theodore P. Baker]
  note: Found independently by Bird (1977) and Baker (1978); Baker's version handles a set of patterns and more than two dimensions.
prereqs: [aho-corasick, knuth-morris-pratt, dictionary-matching]
see_also: [multiple-string-matching, karp-rabin-multiple-patterns, dynamic-dictionary-matching, suffix-tree, failure-link, string-matching]
sources:
  - paper: doi:10.1016/0020-0190(77)90017-5
    title: Richard S. Bird, Two dimensional pattern matching, Information Processing Letters 6(5) (1977), 168-170
    locator: the reduction of matching one pattern array to string matching on the columns of row names
  - paper: doi:10.1137/0207043
    title: Theodore P. Baker, A technique for extending rapid exact-match string matching to arrays of more than one dimension, SIAM Journal on Computing 7(4) (1978), 533-541
    locator: the abstract and the method (a fixed set of pattern arrays, the use of Knuth-Morris-Pratt, and the extensions to patterns of different sizes and to more dimensions)
  - url: https://arxiv.org/abs/1302.0072
    title: Shoshana Marcus and Dina Sokol, Dynamic 2D dictionary matching in small space, arXiv 1302.0072 (2013)
    locator: Section 3 (the Bird / Baker algorithm with Aho-Corasick for dictionaries of uniform width, its linear time and space, and Algorithm 1, its dynamic version)
  - paper: doi:10.1137/S0097539792226321
    title: Amihood Amir, Gary Benson and Martin Farach, An alphabet independent approach to two-dimensional pattern matching, SIAM Journal on Computing 23(2) (1994), 313-323
    locator: the abstract (earlier two-dimensional algorithms need an ordered alphabet and run in O(n^2 log m) time; the text scan of the new algorithm runs in O(n^2) time)
---

The Bird-Baker algorithm finds every occurrence of one or more rectangular patterns in a rectangular text by reducing the two-dimensional problem to two one-dimensional ones. It gives each distinct pattern row a name and runs an [Aho-Corasick](/aho-corasick/) automaton along each text row, which writes at each position the name of the pattern row that ends there. A pattern then occurs exactly where its column of row names occurs in a column of the text's names, which a second string matcher finds: [Knuth-Morris-Pratt](/knuth-morris-pratt/) for one pattern, Aho-Corasick for a set of patterns of equal width. The whole search reads each text character once and takes $O(n_1 n_2 + M + z)$ time for patterns of one width, with hashed transitions.

## In plain words

Think of the text as a grid of letters and each pattern as a smaller grid. First give each different pattern row a short name, such as A or B. Then go along each row of the text with a machine that finds all pattern rows at once, and at each place where a pattern row ends, write its name.

Now a pattern of three rows A, B, A sits at some place exactly when, going down one column of names, you see A, B, A one under the other. So the search for a grid becomes a search for a word of names down each column, and that is a normal string search.

The method reads the text one row at a time and keeps only one search state for each column.

## The problem

The text $T$ has $n_1$ rows and $n_2$ columns, and pattern $P_j$, for $j = 0, \ldots, k - 1$, has $m_j$ rows and $w_j$ columns. All rows of one grid have the same length. A pattern occurs at $(r, c)$ if $T[r + i][c + t] = P_j[i][t]$ for all $0 \le i < m_j$ and $0 \le t < w_j$. Output all triples $(r, c, j)$ of occurrences, with $(r, c)$ the top-left corner. Indices are 0-based, and occurrences may overlap. A pattern listed twice is reported once for each index. A pattern with no rows occurs at every $(r, c)$ with $0 \le r \le n_1$ and $0 \le c \le n_2$, and a pattern of $m$ empty rows occurs at every $(r, c)$ with $0 \le r \le n_1 - m$ and $0 \le c \le n_2$. The alphabet is general: symbols are compared for equality and used as keys of hash tables. $M$ is the total number of symbols in the patterns.

## The algorithm

The algorithm is written for the nonempty patterns of one width $w$; patterns of $d$ different widths take one pass each.

```pseudo id=main
BIRD-BAKER(T[0 .. n1-1][0 .. n2-1], P_0, ..., P_{k-1})
L1  output the occurrences of the empty patterns
L2  give each distinct row of the patterns a name; build the Aho-Corasick automaton A_row of these rows
L3  for each pattern P_j, let R_j ← name(P_j[0]) name(P_j[1]) ... name(P_j[m_j − 1])
L4  build the Aho-Corasick automaton A_col of the strings R_j over the alphabet of names
L5  for c ← 0 to n2 − 1 do q[c] ← the root of A_col
L6  for r ← 0 to n1 − 1 do
L7      run A_row on T[r]; L[c] ← the name of the pattern row that ends at (r, c), or ⊥ if none
L8      for c ← w − 1 to n2 − 1 do
L9          q[c] ← the state of A_col after q[c] reads L[c]          ▷ ⊥ leads to the root
L10         output (r − m_j + 1, c − w + 1, j) for each j with R_j ending at q[c]
```

All pattern rows have the same length $w$, so at most one of them ends at a text position, and line L7 writes one name or ⊥. The state of $A_{\mathrm{row}}$ after it reads $T[r][0 \ldots c]$ spells the longest suffix of $T[r][0 \ldots c]$ that is a prefix of a pattern row; a pattern row ends at $(r, c)$ exactly when this state has depth $w$. Line L10 uses the output lists of $A_{\mathrm{col}}$, which include the strings found through [failure links](/failure-link/). For one pattern, $A_{\mathrm{col}}$ is the Knuth-Morris-Pratt automaton of $R_0$.

## Example

Take the text with the rows ababa, babab, ababa, bbaab ($n_1 = 4$, $n_2 = 5$) and the patterns $P_0$ with rows ab, ba and $P_1$ with rows ba, ab, ba, both of width 2. The distinct rows get the names A = ab and B = ba, so $R_0 = $ AB and $R_1 = $ BAB. Line L7 writes these names:

| row $r$ | text row | $L[0]$ | $L[1]$ | $L[2]$ | $L[3]$ | $L[4]$ | output after line L10 |
|---|---|---|---|---|---|---|---|
| 0 | ababa | ⊥ | A | B | A | B | |
| 1 | babab | ⊥ | B | A | B | A | (0, 0, 0), (0, 2, 0) |
| 2 | ababa | ⊥ | A | B | A | B | (0, 1, 1), (1, 1, 0), (0, 3, 1), (1, 3, 0) |
| 3 | bbaab | ⊥ | ⊥ | B | ⊥ | A | |

Read down the columns: column 1 is A B A ⊥, column 2 is B A B B, column 3 is A B A ⊥, and column 4 is B A B A. AB ends in columns 1 and 3 at row 1 and in columns 2 and 4 at row 2, and BAB ends in columns 2 and 4 at row 2. The output is $(0, 0, 0)$, $(0, 1, 1)$, $(0, 2, 0)$, $(0, 3, 1)$, $(1, 1, 0)$ and $(1, 3, 0)$; the occurrences overlap, and $P_0$ is the top part of $P_1$ shifted down by one row.

## Correctness

Three facts give correctness; the full proof is in the proof file below.

- **Row names.** After $A_{\mathrm{row}}$ reads $T[r][0 \ldots c]$, its state spells the longest suffix that is a prefix of a pattern row. If the pattern row $x$ ends at $(r, c)$, then $x$ is such a suffix of length $w$, the largest possible depth, so the state spells $x$; conversely a state of depth $w$ spells a whole row. So $L[c]$ is the name of the row $T[r][c - w + 1 \ldots c]$ if that is a pattern row, and ⊥ otherwise.
- **Reduction.** $P_j$ occurs at $(r_0, c_0)$ if and only if $T[r_0 + i][c_0 \ldots c_0 + w - 1] = P_j[i]$ for each $i < m_j$, that is, if and only if the names in column $c = c_0 + w - 1$ at rows $r_0, \ldots, r_0 + m_j - 1$ spell $R_j$. Different rows have different names, and ⊥ is no name.
- **Columns.** $q[c]$ is the Aho-Corasick state of the column string read so far, so line L10 reports $j$ at row $r$ exactly when $R_j$ ends there, once for each $j$.

## Complexity

- **Preprocessing.** Building the trie of the distinct rows and the trie of the strings $R_j$, with failure links, takes $O(M)$ time with hashed transitions; the strings $R_j$ have total length $\sum_j m_j \le M$.
- **Search.** Along one text row, $A_{\mathrm{row}}$ makes $n_2$ moves and fewer than $n_2$ failure steps in all, since each failure step lowers the depth and each move raises it by at most 1. The same count holds for each column of names with $A_{\mathrm{col}}$. So one width takes $O(n_1 n_2)$ time plus $O(z)$ for the output, and $d$ widths take $O(d\, n_1 n_2 + z)$.
- **Alphabet.** The bounds above are expected bounds with hashed transitions. With balanced search trees for the transitions they gain a factor $O(\log \sigma)$ for the rows and $O(\log k')$ for the names, where $k'$ is the number of distinct rows. Amir, Benson and Farach note that the earlier two-dimensional algorithms need an ordered alphabet, and give a text scan whose time does not depend on the alphabet.
- **Space.** $O(M)$ for the automata, $n_2$ states $q[c]$, and one row of names: $O(M + n_2)$ beyond the text. The text can be read one row at a time.

## Properties

- **Online by rows.** Each text row is read once, and all occurrences whose bottom row is $r$ are reported when row $r$ has been read.
- **Deterministic and exact.** No hashing of rows is needed for correctness; the names are exact.
- **Uniform width needed for a single pass.** With rows of different lengths, several pattern rows can end at one position, and one name per position is no longer enough; one pass per width solves this at a factor $d$.
- **Works with any one-dimensional matcher.** The column step can use any string matcher that runs over a stream of names, which is how the dynamic and the compressed versions below arise.

## Variants and improvements

- **One pattern.** With one pattern, $A_{\mathrm{col}}$ is the [Knuth-Morris-Pratt](/knuth-morris-pratt/) automaton of $R_0$; this is the form in which Bird and Baker present the method.
- **Patterns of uniform height.** Exchange rows and columns: name the pattern columns, and run the second matcher along the rows.
- **More dimensions.** Baker's technique applies the same naming to arrays of three or more dimensions: name the $(d-1)$-dimensional slices, then match along the last dimension.
- **Alphabet-independent scanning.** Amir, Benson and Farach (1994) scan the text in $O(n^2)$ time for an $n \times n$ text, with no dependence on the alphabet, using the periodicity of the pattern instead of an automaton of rows.
- **Dynamic dictionaries.** Marcus and Sokol replace both automata by the dynamic dictionary matching of Sahinalp and Vishkin, which gives insertion and deletion of patterns in time proportional to their size with no slowdown of the search; see [dynamic dictionary matching](/dynamic-dictionary-matching/).
- **Patterns of different shapes.** Square patterns of different sizes, or rectangles of different widths and heights, need other methods, such as two-dimensional suffix trees; see [two-dimensional dictionary matching](/two-dimensional-dictionary-matching/).
- **Hashing.** A randomized alternative fingerprints each pattern row and each window of $w$ text characters with a [rolling hash](/karp-rabin-multiple-patterns/) and then fingerprints the columns of row fingerprints, as in the two-dimensional version of Karp and Rabin.

## When to use it

Use Bird-Baker to find a set of image tiles, board positions or other two-dimensional patterns that all have the same width, in a large grid that should be read once, row by row. It is simple, exact and linear. For patterns of many different widths and heights, the factor $d$ grows, and the methods of [two-dimensional dictionary matching](/two-dimensional-dictionary-matching/) are better.

## Pitfalls

- **Names of distinct rows only.** Two equal pattern rows must get the same name, in the same pattern or in different ones. Otherwise the text, where only one name can be written, never matches the second copy.
- **Rows of different widths in one pass.** Then the row ab and the row b can both end at one text position, and writing one name loses an occurrence. Group the patterns by width.
- **Resetting the column state.** The column automaton must read ⊥ at positions with no pattern row, which sends it to the root. Skipping these positions joins names from rows that are not adjacent.
- **The corner.** The occurrence found at the end of row $r$ and column $c$ has its top-left corner at $(r - m_j + 1, c - w + 1)$; the height $m_j$ differs between patterns of one width.
- **Empty patterns.** Patterns with no rows or no columns never reach the automata; handle them first, as in line L1.

## Implementations

## History

Richard Bird (1977) and Theodore Baker (1978) published the method independently. Both reduce two-dimensional matching to string matching by naming the pattern rows. Baker's paper treats a fixed set of pattern arrays, uses the algorithm of Knuth, Morris and Pratt, and extends the technique to nonrectangular arrays, arrays of different sizes and more than two dimensions. Later work removed the dependence on the alphabet (Amir, Benson and Farach, 1994), handled square patterns of different sizes (Amir and Farach, 1992; Giancarlo, 1995), and made the dictionary dynamic or compressed (Marcus and Sokol, 2013).

## References
