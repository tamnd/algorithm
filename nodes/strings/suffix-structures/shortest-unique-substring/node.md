---
tag: AEY8AA
kind: problem
slug: shortest-unique-substring
name: Shortest unique substring
aliases:
- shortest unique substring at each position
area: strings/suffix-structures
level: advanced
summary: For each position, find the shortest substring starting there that occurs only once.
model: word-ram
complexity:
  vars: {n: the length of the string}
  time: {worst: Θ(n)}
prereqs: [suffix-array, lcp-array]
see_also: [longest-repeated-substring, maximal-repeats, matching-statistics, suffix-tree, kasai-algorithm, count-distinct-substrings, element-distinctness, longest-common-substring]
sources:
  - paper: doi:10.1109/icde.2013.6544887
    title: Jian Pei, Wush Chi-Hsuan Wu and Mi-Yen Yeh, On shortest unique substring queries, ICDE 2013
    locator: pages 937 to 948; the query for a shortest unique substring covering a position, with a suffix tree
  - paper: doi:10.1007/978-3-319-04298-5_44
    title: Kazuya Tsuruta, Shunsuke Inenaga, Hideo Bannai and Masayuki Takeda, Shortest unique substrings queries in optimal time, SOFSEM 2014
    locator: the linear-time computation for all positions with the suffix array and the LCP array
  - paper: doi:10.1007/978-3-319-07566-2_18
    title: Atalay Mert İleri, M. Oğuzhan Külekci and Bojian Xu, Shortest unique substring query revisited, CPM 2014
    locator: pages 172 to 181; the linear-time algorithm for all positions, from the minimal unique substring at each start
  - paper: doi:10.1016/j.tcs.2014.11.004
    title: Atalay Mert İleri, M. Oğuzhan Külekci and Bojian Xu, A simple yet time-optimal and linear-space algorithm for shortest unique substring queries, Theoretical Computer Science 562, 2015
    locator: pages 621 to 633; the journal version, with all the shortest unique substrings covering each position
---

A unique substring of a string $T$ is one that occurs in $T$ exactly once. The shortest unique substring problem asks, for each position $i$, for the length of the shortest unique substring that starts at $i$; the related query of Pei, Wu and Yeh (2013) asks for the shortest unique substring that *covers* a position. Both are read from the [suffix array](/suffix-array/) and the [LCP array](/lcp-array/) in $\Theta(n)$ time: the shortest unique substring starting at $i$ is one symbol longer than the longest common prefix of suffix $i$ with its two neighbors in sorted order. It is the counterpart of the [longest repeated substring](/longest-repeated-substring/), and it is used to find unique markers in genomes.

## In plain words

A piece of a text is unique if it appears only once. From each letter, read forward until the piece you have read is unique. The number of letters you needed is the answer at that letter. Near the end of a text, sometimes even the whole rest is not unique, and then there is no answer.

Sort all endings of the text. The ending that starts at a given letter has two neighbors in the sorted list, and they are the endings most like it. If it shares five letters with the closer neighbor, then six letters are enough to make it different from every other ending. So the answer at each letter comes from two numbers next to each other in a table.

## Definition

**Input.** A string $T = T[0 \ldots n-1]$ over an ordered alphabet, with 0-based indices. No sentinel is part of $T$; a suffix array built with a sentinel gives the same answers after the sentinel suffix is removed.

**Output, starting at each position.** For each $i$, $sus[i]$ is the smallest $\ell \ge 1$ such that $i + \ell \le n$ and $T[i \ldots i + \ell - 1]$ occurs exactly once in $T$, or "none" if no such $\ell$ exists. The substring $T[i \ldots i + sus[i] - 1]$ is the *minimal unique substring* at $i$ in the sense that no proper prefix of it is unique.

**Output, covering each position.** For each $q$, the shortest unique substrings $T[i \ldots j]$ with $i \le q \le j$; their length is
$$cover[q] = \min_{i \le q,\ sus[i] \ne \text{none}} \max(sus[i],\ q - i + 1),$$
since every extension of a unique substring to the right is unique.

**The formula.** Let $SA$ be the suffix array, $rank$ its inverse, and $LCP[r] = \mathrm{lcp}(T_{SA[r-1]}, T_{SA[r]})$ for $1 \le r < n$, with $LCP[0] = LCP[n] = 0$. Then with $h = \max(LCP[rank[i]], LCP[rank[i] + 1])$,
$$sus[i] = h + 1 \text{ if } i + h + 1 \le n, \text{ and none otherwise.}$$

*Proof.* A prefix of $T_i$ of length $\ell$ occurs at another position $j$ if and only if $\mathrm{lcp}(T_i, T_j) \ge \ell$. The largest $\mathrm{lcp}$ of $T_i$ with another suffix is reached at a neighbor in sorted order, and it is $h$. So the prefix of length $\ell$ is unique if and only if $\ell > h$, and the shortest is $h + 1$ when $T_i$ is long enough. If $|T_i| = n - i \le h$, then $T_i$ is a prefix of its neighbor and no prefix is unique. $\square$

## Variants

- **Global shortest unique substring.** The minimum of $sus[i]$ over all $i$.
- **Covering a position.** The query of Pei, Wu and Yeh, in the formula above. A position can have several shortest unique substrings covering it; some algorithms report one, others all.
- **Interval queries.** The shortest unique substring that covers a range $[s, t]$, or that lies inside a range.
- **Compressed and run-length encoded inputs.** Algorithms in space bounded by compressed measures, and on run-length encoded strings.
- **Palindromic and other restricted variants.** The shortest unique palindromic substring covering a range, studied for run-length encoded strings.
- **Several strings.** The shortest substring of one string that occurs in no other string of a set: a marker, or a distinguishing substring, computed with a [generalized suffix tree](/generalized-suffix-tree/) or with [matching statistics](/matching-statistics/) ($ms[i] + 1$ against the other strings).

## Examples

Take $T = \texttt{abaababa}$, $n = 8$. Then $SA = [7, 2, 5, 0, 3, 6, 1, 4]$ and $LCP = [0, 1, 1, 3, 3, 0, 2, 2]$, with $LCP[8] = 0$.

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $T[i]$ | a | b | a | a | b | a | b | a |
| $h$ | 3 | 2 | 1 | 3 | 2 | 3 | 2 | 1 |
| $sus[i]$ | 4 | 3 | 2 | 4 | 3 | none | none | none |
| substring | abaa | baa | aa | abab | bab | | | |
| $cover[q]$ | 4 | 3 | 2 | 2 | 3 | 3 | 3 | 4 |

At $i = 0$, suffix $\texttt{abaababa}$ has rank 3, and its neighbors share $\texttt{aba}$ with it, so $sus[0] = 4$, the string $\texttt{abaa}$. At $i = 5$, suffix $\texttt{aba}$ is a prefix of its neighbor $\texttt{abaababa}$, so it has no unique prefix. The global shortest unique substring is $\texttt{aa}$, of length 2. For $q = 4$ there are two shortest covering unique substrings, $\texttt{aab}$ at 2 and $\texttt{bab}$ at 4.

Other cases, checked by script against brute force:

| $T$ | $sus$ | global |
|---|---|---|
| `mississippi` | 1, 5, 4, 3, 5, 4, 3, 2, 2, 2, none | 1 (`m`) |
| `banana` | 1, 4, 3, none, none, none | 1 (`b`) |
| `abab` | 3, 2, none, none | 2 (`ba`) |
| $a^n$ | $n$, then none | $n$ |
| the empty string | the empty array | none |

## Known algorithms

| method | time | notes |
|---|---|---|
| for each $i$ and $\ell$, count the occurrences | $O(n^3)$ or more | an oracle for tests |
| Pei, Wu and Yeh, suffix tree | $O(n)$ per covering query; $O(n^2)$ for all positions | the first algorithm for the covering query |
| suffix array and LCP array, the formula | $\Theta(n)$ for all $sus[i]$ after the arrays | Tsuruta, Inenaga, Bannai and Takeda; İleri, Külekci and Xu |
| covering lengths from $sus$ | $\Theta(n)$ | two sweeps, or a sliding minimum over the starts |
| suffix tree, leaf parents | $\Theta(n)$ | $sus[i]$ is the string depth of the parent of the leaf of $i$, plus one |
| Hu, Pei and Tao | $O(n)$ build, $O(1)$ per covering query | an optimal query structure |

**Covering lengths in linear time.** Each start $i$ with $sus[i] = s$ gives the unique substring $[i, i + s - 1]$, and for $q \ge i + s$ the extension $[i, q]$. So $cover[q]$ is the smaller of two minima: the shortest interval $[i, i + s - 1]$ that contains $q$, and $q - i^* + 1$ for the largest start $i^*$ with $i^* + sus[i^*] - 1 \le q$. The first is a range minimum over intervals, computed by a sweep with a monotone queue; the second is a running maximum. Both take $O(n)$ time.

## Bounds

- **Upper bound.** $\Theta(n)$ in the [word RAM](/word-ram/) for an integer alphabet of size $n^{O(1)}$, by a linear [suffix array construction](/suffix-array-construction/) and [Kasai's algorithm](/kasai-algorithm/).
- **Lower bound.** $\Omega(n)$ to read the input. Over a general ordered alphabet, $sus[i] = 1$ for all $i$ if and only if all symbols are different, so [element distinctness](/element-distinctness/) reduces to the problem and $\Omega(n \log n)$ comparisons are needed in the decision tree model.
- **Output size.** $n$ numbers. Listing all shortest covering substrings for all positions can take more space; İleri, Külekci and Xu give them in $O(n)$ total by intervals.

## Reductions

- **To the LCP array.** As in the formula: two neighbors per suffix.
- **From element distinctness.** As in the bounds.
- **Relation to repeats.** $sus[i] - 1$ is the length of the longest repeated prefix of $T_i$, so $\max_i (sus[i] - 1)$, taken over positions with an answer, is the length of the longest repeated substring.
- **To matching statistics.** A substring that starts at $i$ and occurs in no other string of a set is shortest at length $ms[i] + 1$, where $ms$ are the [matching statistics](/matching-statistics/) of the string against the others.

## Applications

- **Genome markers and primers.** A unique substring identifies a location in a genome; short unique substrings are candidates for PCR primers and probes, and for marking regions of a reference.
- **Read mapping.** A read that contains a unique substring of the reference maps to one place, which helps to resolve repeats.
- **Document search and text analysis.** Pei, Wu and Yeh motivated the covering query with finding the shortest phrase that identifies an event in a log or a sentence in a document.
- **Testing other structures.** The answers are a short check of a suffix array and LCP array implementation, as the brute force is simple.

## References
