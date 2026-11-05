---
tag: YEMC7E
kind: problem
slug: longest-common-substring
name: Longest common substring
aliases:
- longest common factor
area: strings/suffix-structures
level: core
summary: Find the longest substring common to two or more strings.
model: word-ram
complexity:
  vars: {n: the total length of the strings}
  time: {worst: Θ(n)}
prereqs: [suffix-array, lcp-array]
see_also: [generalized-suffix-tree, longest-repeated-substring, longest-common-subsequence, matching-statistics, suffix-automaton, generalized-suffix-automaton, lcs-dynamic-programming]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 7.4 (longest common substring of two strings) and Section 7.6 (common substrings of more than two strings), with the generalized suffix tree of Section 6.4
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design, Cambridge University Press, 2015
    locator: Chapter 8 (Classical indexes), applications of the generalized suffix tree and suffix array
  - url: https://cp-algorithms.com/string/suffix-automaton.html
    title: cp-algorithms, Suffix Automaton
    locator: sections Longest common substring of two strings and Largest common substring of multiple strings
---

The longest common substring problem asks for a longest string that occurs as a contiguous substring of each of two given strings $X$ and $Y$, or of at least $k$ of $m$ given strings. For two strings of total length $n$, it is solved in $\Theta(n)$ time with a [generalized suffix tree](/generalized-suffix-tree/), or with the [suffix array](/suffix-array/) and [LCP array](/lcp-array/) of $X \# Y$, where $\#$ is a separator that occurs in neither string. It is a different problem from the [longest common subsequence](/longest-common-subsequence/), whose common part need not be contiguous, and which has no known algorithm in time $O(n^{2-\varepsilon})$.

## In plain words

You have two texts and want the longest piece of consecutive letters that appears in both. For "banana" and "cabana" it is "bana".

The trick is to glue the two texts together with a special mark between them that appears nowhere else, and sort all endings of the glued text. A piece that occurs in both texts is the start of an ending from the first text and of an ending from the second text. In the sorted list, the endings with the longest common start sit next to each other. So walk through the list and look only at neighbors that come from different texts. The longest shared start among those pairs is the answer. The special mark stops a shared start from running from one text into the other.

## Definition

**Input.** Strings $X = X[0 \ldots n_1-1]$ and $Y = Y[0 \ldots n_2-1]$ over an ordered alphabet $\Sigma$, with 0-based indices.

**Output.** A string $u$ of largest length with $u = X[i \ldots i+|u|-1] = Y[j \ldots j+|u|-1]$ for some $i$ and $j$, often given as the triple $(|u|, i, j)$. The empty string is the answer when $X$ and $Y$ have no symbol in common.

**The suffix array method.** Let $\# \notin \Sigma$ and $Z = X \# Y$, of length $N = n_1 + n_2 + 1$, with suffix array $SA$ and LCP array $LCP$ (no sentinel). Call a position $p$ of $Z$ an $X$-position if $p < n_1$ and a $Y$-position if $p > n_1$. Then

$$|u| = \max \{\, LCP[i] : 1 \le i < N,\ SA[i-1] \text{ and } SA[i] \text{ are one } X\text{-position and one } Y\text{-position} \,\}$$

(and 0 if there is no such $i$).

*Proof.* Because $\#$ occurs once, a common prefix of two suffixes that start at different positions cannot contain $\#$: in the two suffixes, $\#$ would be at different offsets. So the common prefix of a suffix that starts at an $X$-position and one that starts at a $Y$-position lies inside $X$ and inside $Y$, and each candidate value is the length of a common substring. Conversely, let a nonempty $u$ occur at $X$-position $i$ and at $Y$-position $n_1 + 1 + j$, and let the ranks of these two suffixes be $a < b$ (in some order of the sides). By the [LCP-RMQ reduction](/lcp-rmq-reduction/), $\min LCP[a+1 \ldots b] = \mathrm{lcp}(Z_{SA[a]}, Z_{SA[b]}) \ge |u| \ge 1$. The suffix $Z_{n_1}$ starts with $\#$, and no other suffix does, so its LCP with each neighbor is 0. Hence its rank is not in $[a, b]$, and each rank from $a$ to $b$ holds an $X$-position or a $Y$-position. The first and the last are on different sides, so some $c$ with $a < c \le b$ has $SA[c-1]$ and $SA[c]$ on different sides, and $LCP[c] \ge \min LCP[a+1 \ldots b] \ge |u|$. So the maximum is at least $|u|$. $\square$

For $m$ strings $S_1, \ldots, S_m$ and a number $2 \le k \le m$, the general problem asks for a longest string that occurs in at least $k$ of them. On the suffix array of $S_1 \#_1 S_2 \#_2 \cdots S_m \#_m$ with distinct separators, it is the largest value of $\min LCP[l+1 \ldots r]$ over the windows $[l, r]$ of ranks whose suffixes start in at least $k$ different strings.

## Variants

- **Two strings, decision.** Is there a common substring of length at least $L$? This is monotone in $L$, which allows a binary search with hashing.
- **$k$ of $m$ strings.** As above. Gusfield (Section 7.6) solves it for all $k$ at once in $O(n)$ time with a generalized suffix tree and a count of the distinct strings below each node.
- **All common substrings of a given length**, or all maximal common substrings.
- **Matching statistics.** For each position of $Y$, the longest prefix of $Y[j \ldots]$ that occurs in $X$; the maximum is the longest common substring. See [matching statistics](/matching-statistics/).
- **With mismatches.** The longest common substring with up to $k$ mismatches, a harder problem with its own algorithms.
- **Longest common subsequence.** Not contiguous: see [longest common subsequence](/longest-common-subsequence/).

## Examples

| $X$ | $Y$ | longest common substring | length |
|---|---|---|---|
| `banana` | `cabana` | `bana` | 4 |
| `xabxac` | `abcabxabcd` | `abxa` | 4 |
| `abab` | `baba` | `aba` and `bab` | 3 |
| `GATTACA` | `TACTAG` | `TAC` | 3 |
| `aaaa` | `aa` | `aa` | 2 |
| `abc` | `def` | empty | 0 |

The suffix array of $Z = \texttt{banana\#cabana}$ (with $\#$ before the letters) shows the method. The side is $X$ for positions 0 to 5 and $Y$ for 7 to 12.

| rank | $SA$ | side | $LCP$ | suffix | different sides? |
|---|---|---|---|---|---|
| 0 | 6 | # | 0 | #cabana | |
| 1 | 12 | Y | 0 | a | |
| 2 | 5 | X | 1 | a#cabana | yes, 1 |
| 3 | 8 | Y | 1 | abana | yes, 1 |
| 4 | 10 | Y | 1 | ana | |
| 5 | 3 | X | 3 | ana#cabana | yes, 3 |
| 6 | 1 | X | 3 | anana#cabana | |
| 7 | 9 | Y | 0 | bana | |
| 8 | 0 | X | 4 | banana#cabana | yes, 4 |
| 9 | 7 | Y | 0 | cabana | |
| 10 | 11 | Y | 0 | na | |
| 11 | 4 | X | 2 | na#cabana | yes, 2 |
| 12 | 2 | X | 2 | nana#cabana | |

The best pair is at rank 8: `bana` at position 0 of $X$ and at position $9 - 7 = 2$ of $Y$. The pair at ranks 5 and 6 has the value 3 but both suffixes come from $X$, so it is a repeat of $X$, not a common substring.

## Known algorithms

| method | time | space | notes |
|---|---|---|---|
| dynamic programming, $L[i][j] = L[i-1][j-1] + 1$ if $X[i-1] = Y[j-1]$, else 0 | $\Theta(n_1 n_2)$ | $O(\min(n_1, n_2))$ by rows | the textbook method, like [LCS dynamic programming](/lcs-dynamic-programming/) but with a reset to 0 |
| binary search on the length, with [Rabin-Karp](/rabin-karp/) hashing of all substrings of the tested length | $O(n \log n)$ expected | $O(n)$ | a hash collision gives a false answer unless it is checked |
| suffix array and LCP array of $X \# Y$ | $O(n)$ for an integer alphabet, after a linear [suffix array construction](/suffix-array-construction/) | $O(n)$ | the method above |
| [generalized suffix tree](/generalized-suffix-tree/) | $O(n)$ for an integer alphabet | $O(n)$ | the deepest internal node with leaves from both strings (Gusfield, Section 7.4) |
| [suffix automaton](/suffix-automaton/) of $X$, then a scan of $Y$ | $O(n \log \sigma)$ | $O(n_1)$ | keeps the longest suffix of $Y[0 \ldots j]$ that occurs in $X$ |
| $k$ of $m$ strings: suffix array with a sliding window over the ranks | $O(n)$ with a monotone queue for the window minimum | $O(n)$ | the window must hold suffixes from $k$ different strings |

## Bounds

- **Upper bound.** $O(n)$ time in the [word RAM](/word-ram/) for an integer alphabet of size $n^{O(1)}$, for two strings and for the $k$ of $m$ version.
- **Lower bound for a general ordered alphabet.** $X$ and $Y$ have a common substring of length at least 1 if and only if they share a symbol. So set disjointness, which needs $\Omega(n \log n)$ comparisons, reduces to the problem in $O(n)$ time, and the $O(n \log n)$ bound with a comparison sort is optimal in the [comparison model](/comparison-model/).
- **Lower bound for an integer alphabet.** $\Omega(n)$, since each symbol must be read.
- **History of the linear bound.** Gusfield (Section 7.4) reports that Knuth had conjectured that no linear-time algorithm exists for two strings, and that the suffix tree gives one.

## Reductions

- **To a longest repeat.** The answer is a longest repeat of $X \# Y$ with one occurrence on each side of $\#$; compare the [longest repeated substring](/longest-repeated-substring/), which is the same scan without the side test.
- **To matching statistics.** The maximum of the [matching statistics](/matching-statistics/) of $Y$ against $X$.
- **From set disjointness.** As in the bounds.

## Applications

- **Plagiarism and clone detection.** The longest shared passage of two documents or two source files.
- **Biology.** Long exact matches between two genomes are the anchors of whole-genome alignment, and a long common substring with a known vector sequence shows contamination of a DNA sample (Gusfield, Section 7.5).
- **Diff tools.** Some diff and file-sync algorithms anchor on the longest common substring and recurse on the two sides.
- **Data compression.** Finding the longest match of the coming text in a dictionary or in past data, as in the matching statistics.

## References
