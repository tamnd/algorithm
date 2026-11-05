---
tag: ZFZK7Q
kind: problem
slug: matching-statistics
name: Matching statistics
aliases:
- matching statistics computation
area: strings/suffix-structures
level: advanced
summary: For each position of a pattern, the length of the longest substring starting there that also occurs in the text.
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the alphabet size}
  time: {worst: O((n + m) log σ), constant-alphabet: Θ(n + m)}
prereqs: [suffix-tree, suffix-link]
see_also: [suffix-automaton, longest-common-substring, approximate-string-matching, r-index, fm-index, generalized-suffix-tree, lempel-ziv-factorization, shortest-unique-substring]
sources:
  - paper: doi:10.1007/BF01185431
    title: William I. Chang and Eugene L. Lawler, Sublinear approximate string matching and biological applications, Algorithmica 12(4-5), 1994
    locator: pages 327 to 344; the definition of matching statistics and their computation in O(m) time with the suffix tree of the text and its suffix links
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 7 (first applications of suffix trees), the section on matching statistics and their computation with suffix links
---

The matching statistics of a pattern $P$ against a text $T$ give, for each position $i$ of $P$, the length $ms[i]$ of the longest prefix of $P[i \ldots m-1]$ that occurs somewhere in $T$. Chang and Lawler defined them in 1994 for sublinear approximate matching, and computed all $m$ values in $O(m)$ time with the [suffix tree](/suffix-tree/) of $T$ and its [suffix links](/suffix-link/). Matching statistics give the [longest common substring](/longest-common-substring/), the maximal exact matches used to seed DNA alignment, and distances between sequences.

## In plain words

Put a finger on each letter of a pattern. From that letter, read forward as far as you can while the piece you have read still appears somewhere in a fixed text. The number of letters you could read is the matching statistic at that letter.

Moving the finger one letter to the right can lose at most one letter of the match: the piece that started one letter earlier, minus its first letter, still appears in the text. A good method uses this. It never reads the same part of the pattern again from the start, so the total work is about the length of the pattern, after one pass to prepare the text.

## Definition

**Input.** A text $T = T[0 \ldots n-1]$ and a pattern $P = P[0 \ldots m-1]$ over an ordered alphabet of size $\sigma$, with 0-based indices. No sentinel is part of the definition; algorithms that build a suffix tree append one to $T$ only.

**Output.** The array $ms[0 \ldots m-1]$ with

$$ms[i] = \max\{\ell \ge 0 : P[i \ldots i + \ell - 1] \text{ is a substring of } T\}.$$

The empty string is a substring of every text, so $ms[i] \ge 0$, and $ms[i] \le m - i$. Often each value comes with a position $p[i]$ of $T$ where $P[i \ldots i + ms[i] - 1]$ occurs.

**Key property.** $ms[i+1] \ge ms[i] - 1$, because each substring of a substring of $T$ is a substring of $T$. So the right ends $i + ms[i]$ never decrease.

## Variants

- **Ending at each position.** $\ell[j]$ is the length of the longest suffix of $P[0 \ldots j]$ that occurs in $T$. It is the natural output of a left-to-right scan of $P$ through the [suffix automaton](/suffix-automaton/) of $T$, and $\ell$ for $P$ and $T$ is $ms$ for the reversed strings, read backwards.
- **With positions or counts.** Report, with each $ms[i]$, one occurrence in $T$, or the number of occurrences, read from the locus in the suffix tree.
- **Against a collection.** $T$ is a set of documents or genomes joined with separators, as in a [generalized suffix tree](/generalized-suffix-tree/); one may also ask for the document of each match.
- **Maximal exact matches (MEMs).** Nonempty substrings $P[i \ldots i + \ell - 1]$ that occur in $T$ but stop occurring when extended by one symbol of $P$ to the left or to the right. These are exactly the pairs $(i, ms[i])$ with $ms[i] > 0$ and $i = 0$ or $ms[i-1] \le ms[i]$, so they come from one scan of the matching statistics.
- **Compressed indexes.** With an [FM-index](/fm-index/) or an [r-index](/r-index/) of $T$ in place of the suffix tree, using backward steps on the reversed problem, or, for the r-index, a structure of thresholds (MONI, by Rossi, Oliva, Langmead, Gagie and Boucher, 2022).

## Examples

Take $T = \texttt{abaababa}$ ($n = 8$) and $P = \texttt{babbaab}$ ($m = 7$).

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $P[i]$ | b | a | b | b | a | a | b |
| $ms[i]$ | 3 | 2 | 1 | 4 | 3 | 2 | 1 |
| longest match | bab | ab | b | baab | aab | ab | b |
| $\ell[i]$, ending at $i$ | 1 | 2 | 3 | 1 | 2 | 3 | 4 |

At $i = 0$, $\texttt{bab}$ occurs in $T$ at position 4, but $\texttt{babb}$ does not occur, since $T$ has no $\texttt{bb}$. At $i = 3$ the value rises from 1 to 4: $\texttt{baab}$ occurs at position 1 and reaches the end of $P$. The right ends $i + ms[i]$ are $3, 3, 3, 7, 7, 7, 7$, a nondecreasing sequence.

Other small cases, checked by script:

| $T$ | $P$ | $ms$ |
|---|---|---|
| `banana` | `ananas` | 5, 4, 3, 2, 1, 0 |
| `mississippi` | `sissippis` | 8, 7, 6, 5, 4, 3, 2, 2, 1 |
| `abracadabra` | `cadabrac` | 7, 6, 5, 5, 4, 3, 2, 1 |
| any $T$ | the empty string | the empty array |
| the empty string | any $P$ | all 0 |

## Known algorithms

| method | time | notes |
|---|---|---|
| check each $i$ and each length with a substring search | $O(m^2 n)$ | an oracle for tests |
| for each $i$, walk down the suffix tree of $T$ from the root | $O(m^2)$ worst case after the $O(n)$ tree | each walk restarts at the root |
| Chang and Lawler, suffix tree with suffix links | $O(n + m)$ for a constant alphabet, $O((n + m) \log \sigma)$ in general | after a mismatch, follow the suffix link and skip down with skip/count |
| [suffix automaton](/suffix-automaton/) of $T$, scan of the reversed problem or of $\ell$ | $O((n + m) \log \sigma)$ | on a mismatch, follow the suffix link and set the length to $len$ of the new state |
| [FM-index](/fm-index/) with backward search on $P$ reversed | $O(m)$ rank steps plus the cost of the shortenings | small space; shortening needs a parent operation or a re-search |
| r-index with thresholds | $O(m)$ steps in $O(r)$ words, $r$ the number of BWT runs | for highly repetitive collections |

**Chang and Lawler.** Keep a locus $(v, d)$ in the suffix tree of $T$ that spells $P[i \ldots i + ms[i] - 1]$. To compute $ms[i]$, extend the locus with $P[i + ms[i]]$, $P[i + ms[i] + 1], \ldots$ while the tree has the edge, and record the length. To go from $i$ to $i + 1$, drop the first symbol: go to the parent's suffix link, then walk down the remaining $ms[i] - 1$ symbols with skip/count, comparing only the first symbol of each edge. The forward extensions add up to at most $m$, since $i + ms[i]$ never decreases; the node depth argument of [Ukkonen's](/ukkonen-algorithm/) and [McCreight's](/mccreight-algorithm/) algorithms bounds the skip/count steps by $O(m)$ in total.

## Bounds

- **Upper bound.** $O(n + m)$ for a constant alphabet, $O((n + m) \log \sigma)$ for a general ordered alphabet, and $O(n + m)$ for an integer alphabet of size $n^{O(1)}$ with a suffix tree whose children are found in $O(1)$ time, for example with perfect hashing (expected construction time).
- **Lower bound.** $\Omega(n + m)$: an algorithm that does not read some symbol of $P$ cannot tell its value, and $ms$ can depend on each symbol of $T$ (take $P = T$ with one symbol changed).

## Reductions

- **Longest common substring.** The longest common substring of $T$ and $P$ has length $\max_i ms[i]$, found at an $i$ that reaches the maximum. With a suffix tree of $T$ only, this gives $O(n)$ space, not $O(n + m)$.
- **String matching.** $P$ occurs in $T$ if and only if $ms[0] = m$.
- **Relative Lempel-Ziv parsing.** The greedy parse of $P$ into the longest phrases that occur in a reference $T$ takes phrase lengths $ms[i]$ at the phrase starts $i$ (or one literal symbol when $ms[i] = 0$), so it follows from the matching statistics in $O(m)$ time.
- **To the ending variant.** $ms$ for $(T, P)$ is the reversal of $\ell$ for the reversed strings, as stated in Variants.

## Applications

- **Approximate matching.** Chang and Lawler's filter cuts $P$ (or $T$) into pieces and uses matching statistics to skip text regions that cannot hold a match with $k$ differences, which gives sublinear expected time on random text.
- **Sequence comparison.** The average of $ms[i]$ over $i$, the average common substring, measures the similarity of two genomes without alignment.
- **Read alignment and pangenomes.** Maximal exact matches between a read and a reference seed alignment tools; with an r-index the reference can be a large collection of similar genomes.
- **Compression against a reference.** Relative Lempel-Ziv and similar schemes store a genome as phrases copied from a reference.

## References
