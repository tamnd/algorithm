---
tag: 31ES8G
kind: problem
slug: circular-pattern-matching
name: Circular pattern matching
aliases:
- cyclic pattern matching
- rotation matching
area: strings/exact-matching
level: advanced
summary: Find occurrences of any rotation of the pattern in the text.
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern}
  time: {worst: Θ(n + m)}
prereqs: [string-matching, word-conjugacy, z-algorithm]
see_also: [word-conjugacy-testing, minimal-rotation, suffix-automaton, knuth-morris-pratt, hamming-string-matching, dictionary-matching, string-period]
sources:
  - paper: doi:10.1186/1748-7188-9-9
    title: Carl Barton, Costas S. Iliopoulos and Solon P. Pissis, Fast algorithms for approximate circular string matching, Algorithms for Molecular Biology 9 (2014), article 9
    locator: Background (the definition of exact circular string matching, the O(n) algorithm with a suffix automaton of xx credited to Lothaire, and the average-case lower bound), Problem 1, and the algorithm ECSMF
  - paper: doi:10.1016/j.jda.2008.09.001
    title: Kimmo Fredriksson and Szymon Grabowski, Average-optimal string matching, Journal of Discrete Algorithms 7(4) (2009), 579-594
    locator: the section "Pattern matching with all circular shifts" (an average-optimal algorithm)
  - paper: doi:10.1007/978-3-540-77891-2_5
    title: Costas S. Iliopoulos and M. Sohel Rahman, Indexing circular patterns, WALCOM 2008, Lecture Notes in Computer Science 4921, 46-57
    locator: the indexing version of the problem
  - paper: doi:10.4230/LIPIcs.ESA.2022.35
    title: Panagiotis Charalampopoulos, Tomasz Kociumaka, Solon P. Pissis, Jakub Radoszewski, Wojciech Rytter, Juliusz Straszyński, Tomasz Waleń and Wiktor Zuba, Approximate circular pattern matching, ESA 2022
    locator: the approximate versions under Hamming and edit distance
---

Circular pattern matching asks for every position of a text $T$ of length $n$ where some rotation of a pattern $P$ of length $m$ occurs, as when $P$ is a circular DNA molecule written from an arbitrary starting point. Every rotation of $P$ is a factor of $PP$, and this reduces the problem to finding, at each text position, the longest prefix and the longest suffix of $P$ that touch it. With the [Z-algorithm](/z-algorithm/) this takes $\Theta(n + m)$ time over a general alphabet, the same as ordinary [string matching](/string-matching/).

## In plain words

Write the word around a circle. You may start reading it at any letter, so a word of length 5 has up to 5 readings: for "abcde" they are abcde, bcdea, cdeab, deabc and eabcd. You want every place in a text where any of these readings appears.

Searching for each reading separately works, but costs one full search per reading. There is a faster way. Any reading is the end part of the word followed by its start part. So, at each place in the text, find how much of the word's end finishes right before it and how much of the word's start begins right at it. If the two lengths add up to the whole word, some reading straddles that place, and simple counting tells you exactly where each such reading starts.

## Definition

**Alphabet.** A general alphabet: the algorithms below only test characters for equality, except the suffix automaton method, which uses an integer alphabet or a dictionary.

**Rotations.** For $0 \le j < m$, the rotation of $P$ by $j$ is $\mathrm{rot}_j(P) = P[j \ldots m-1]\,P[0 \ldots j-1]$. The set $\mathrm{Rot}(P)$ has at most $m$ distinct strings, and exactly $|r|$ of them when $P = r^e$ with $r$ [primitive](/primitive-word/); for instance $\mathrm{Rot}(\text{abab}) = \{\text{abab}, \text{baba}\}$.

**Input.** A text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$. Indices are 0-based.

**Output.** The set $\mathrm{COcc}(P, T) = \{\, i : 0 \le i \le n - m,\ T[i \ldots i+m-1] \in \mathrm{Rot}(P) \,\}$, in increasing order. Each position is reported once, even when several rotations occur there; occurrences may overlap. As on the other pages of this area, if $m = 0$ every position $0, \ldots, n$ is reported, and if $m > n$ nothing is.

**Key fact.** $\mathrm{Rot}(P)$ is exactly the set of factors of length $m$ of $PP$ (for $m \ge 1$): $\mathrm{rot}_j(P) = (PP)[j \ldots j+m-1]$.

## Variants

- **Report the rotation.** Output pairs $(i, j)$, or the smallest $j$ for each $i$. The method below produces, for each position, an interval of valid $j$ per cut point, so the smallest $j$ comes for free.
- **Decision and counting.** Does some rotation occur at all, and how many positions qualify.
- **Conjugacy.** The case $n = m$: are $T$ and $P$ rotations of each other? This is [conjugacy testing](/word-conjugacy-testing/).
- **Circular text.** The text itself is circular; search in $T$ followed by its first $m - 1$ characters.
- **Approximate.** Allow $k$ mismatches or $k$ edits between the window and the best rotation. Barton, Iliopoulos and Pissis give average-case filters, and Charalampopoulos et al. study the worst case.
- **Indexing.** Preprocess $T$ so that circular patterns can be queried fast; Iliopoulos and Rahman treat this version.
- **Many circular patterns.** A dictionary version, in the manner of [dictionary matching](/dictionary-matching/).

## Examples

Take $P$ = abc, so $\mathrm{Rot}(P) = \{$abc, bca, cab$\}$, and $T$ = bcabcaxabcb, with $n = 11$.

| position $i$ | window | rotation |
|---|---|---|
| 0 | bca | $\mathrm{rot}_1$ |
| 1 | cab | $\mathrm{rot}_2$ |
| 2 | abc | $\mathrm{rot}_0$ |
| 3 | bca | $\mathrm{rot}_1$ |
| 7 | abc | $\mathrm{rot}_0$ |

So $\mathrm{COcc}(P, T) = \{0, 1, 2, 3, 7\}$; plain string matching finds only 2 and 7. The windows at 4, 5, 6, 8 (cax, axa, xab, bcb) are not rotations.

More cases: $P$ = aa in $T$ = aaaa gives 0, 1, 2, with a single distinct rotation; $P$ = ba in $T$ = abab gives 0, 1, 2, since ab is a rotation of ba.

## Known algorithms

All bounds are worst case unless stated otherwise.

| method | alphabet | time | extra space |
|---|---|---|---|
| search each rotation with [KMP](/knuth-morris-pratt/) | general | $O(m(n + m))$ | $O(m)$ |
| [Aho-Corasick](/aho-corasick/) on the distinct rotations | integer | $O(m^2 + n)$ | $O(m^2)$ |
| prefix and suffix lengths with the [Z-algorithm](/z-algorithm/) | general | $O(n + m)$ | $O(n + m)$ |
| [suffix automaton](/suffix-automaton/) of $PP$ | integer, $\sigma = O(1)$ | $O(n + m)$ | $O(m)$ |
| Fredriksson and Grabowski | integer | $O(n \log_\sigma m / m)$ average | |

**Prefix and suffix lengths.** For each cut $c$, $0 \le c \le n$, let $\mathrm{LP}[c]$ be the length of the longest prefix of $P$ that starts at $T[c]$, and $\mathrm{LS}[c]$ the length of the longest suffix of $P$ that ends at $T[c-1]$. The first is a [Z-array](/z-algorithm/) of $P \$ T$; the second is the same array for the reversed strings. The rotation $\mathrm{rot}_j(P)$ occurs at $i$ exactly when the suffix of $P$ of length $m - j$ ends just before the cut $c = i + m - j$ and the prefix of length $j$ starts at it. Shorter prefixes and suffixes are implied by longer ones, so the occurrences with cut $c$ are those with $\max(0, m - \mathrm{LS}[c]) \le j \le \min(m - 1, \mathrm{LP}[c])$: an interval of start positions $i = c - m + j$. Marking these $n + 1$ intervals in a difference array and taking prefix sums gives $\mathrm{COcc}(P, T)$ in $O(n + m)$ time. In the example, the cuts 2, 5 and 10 give the intervals $[0, 1]$, $[2, 3]$ and $[7, 7]$.

**Suffix automaton of $PP$.** Run $T$ through the [suffix automaton](/suffix-automaton/) of $PP$ while tracking the length of the longest factor of $PP$ that ends at the current position, as in the [matching statistics](/matching-statistics/) scan. A rotation ends at position $t$ exactly when that length is at least $m$. This is the linear-time solution that Barton, Iliopoulos and Pissis attribute to Lothaire's Applied Combinatorics on Words.

**Average case.** Fredriksson and Grabowski give an algorithm that is optimal on average, and Barton, Iliopoulos and Pissis give a simpler filtering algorithm, ECSMF, that runs in $O(n)$ average time: it cuts $PP$ into fragments, searches for them all at once, and checks the candidates.

## Bounds

**Upper bound.** $O(n + m)$ time over a general alphabet, by the prefix and suffix method.

**Lower bound.** For $P = a^m$, $\mathrm{Rot}(P) = \{P\}$ and the problem is ordinary string matching, where Rivest's [lower bound](/string-matching-lower-bound/) forces $n - m + 1$ text reads in the worst case; reading the pattern adds $m$. So $\Theta(n + m)$ is tight.

**Average case.** Barton, Iliopoulos and Pissis report that the average-case lower bound $\Omega(n \log_\sigma m / m)$ of single-pattern matching, due to Yao, also holds for circular matching, and that Fredriksson and Grabowski reach it.

**Output size.** Up to $n - m + 1$ positions, as for $T = a^n$, $P = a^m$.

## Reductions

- **To string matching with a set of patterns.** $\mathrm{COcc}(P, T)$ is the set of occurrences of the dictionary $\mathrm{Rot}(P)$, which has at most $m$ strings of length $m$, total size $O(m^2)$.
- **To factors of $PP$.** A window of $T$ of length $m$ is a rotation of $P$ exactly when it is a factor of $PP$; any structure that reports the longest factor of $PP$ ending at each text position solves the problem.
- **From conjugacy.** With $n = m$, the problem is [conjugacy testing](/word-conjugacy-testing/), which in turn reduces to ordinary string matching of $T$ in $PP$.
- **Canonical rotations.** $T[i \ldots i+m-1]$ is a rotation of $P$ exactly when both have the same [minimal rotation](/minimal-rotation/). This gives an $O(nm)$ method, or a filter, and it is the basis of indexing circular patterns by a canonical form.

## Applications

- Searching circular genomes, plasmids and other circular DNA sequences, whose linear representation starts at an arbitrary point; this is the motivation in Barton, Iliopoulos and Pissis.
- Detecting that two cyclic sequences, such as necklaces or periodic schedules, are the same up to their starting point.

## References
