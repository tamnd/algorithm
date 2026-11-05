---
tag: 6FAFNT
kind: problem
slug: longest-repeated-substring
name: Longest repeated substring
aliases:
- longest repeat
area: strings/suffix-structures
level: core
summary: Find the longest substring that occurs at least twice in a string.
model: word-ram
complexity:
  vars: {n: the length of the string}
  time: {worst: Θ(n)}
prereqs: [suffix-array, lcp-array]
see_also: [lcp-array, maximal-repeats, longest-common-substring, count-distinct-substrings, suffix-tree, kasai-algorithm, shortest-unique-substring, element-distinctness]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Chapter 6 (Context), the section on suffix arrays, with the longest repeated substring client LRS
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 7 (first applications of suffix trees), repeats found as the deepest internal node, and Section 7.14 on suffix arrays
  - paper: doi:10.1145/800152.804905
    title: Richard M. Karp, Raymond E. Miller and Arnold L. Rosenberg, Rapid identification of repeated patterns in strings, trees and arrays, STOC 1972
    locator: pages 125 to 136, the naming method for finding repeated substrings
---

The longest repeated substring problem asks for a longest string that occurs at least twice in a given string $T$, at two different start positions; the two occurrences may overlap. Its length is the maximum of the [LCP array](/lcp-array/), and the string is read from the [suffix array](/suffix-array/) at a rank where the maximum is reached. With a linear suffix array construction this takes $\Theta(n)$ time. In the [suffix tree](/suffix-tree/), the answer is the path label of an internal node of largest string depth.

## In plain words

Look for the longest piece of a text that appears in it two times or more. In "banana", the piece "ana" appears at the second letter and again at the fourth letter. The two copies share a letter, and that is allowed.

A piece that appears twice is the start of two different endings of the text. Sort all endings of the text. Two endings with a long common start are then next to each other in the sorted list. So the longest repeated piece is the longest common start of two neighbors in the list. One pass over the counts of shared first letters finds it.

## Definition

**Input.** A string $T = T[0 \ldots n-1]$ over an ordered alphabet, with 0-based indices.

**Output.** A string $u$ of largest length such that $u = T[i \ldots i + |u| - 1] = T[j \ldots j + |u| - 1]$ for two positions $0 \le i < j \le n - |u|$. The empty string is the answer when all symbols of $T$ are different. Often the output is the length $|u|$ together with the two positions $i$ and $j$.

**The method.** Let $SA$ be the suffix array of $T$ without a sentinel and $LCP[i] = \mathrm{lcp}(T_{SA[i-1]}, T_{SA[i]})$ for $1 \le i < n$. Then

$$|u| = \max_{1 \le i < n} LCP[i] \quad (\text{and } 0 \text{ if } n \le 1),$$

and for an index $i$ that reaches the maximum, $u = T[SA[i] \ldots SA[i] + LCP[i] - 1]$ occurs at $SA[i-1]$ and at $SA[i]$.

*Proof.* Each value $LCP[i]$ is the length of a common prefix of two different suffixes, so it is the length of a repeated substring. Conversely, if $u$ occurs at $i \ne j$, then $u$ is a common prefix of $T_i$ and $T_j$. Let their ranks be $a < b$. By the [LCP-RMQ reduction](/lcp-rmq-reduction/), $|u| \le \mathrm{lcp}(T_i, T_j) = \min LCP[a+1 \ldots b] \le LCP[b]$. So the maximum of the array is at least the length of each repeat. $\square$

## Variants

- **Repeated $k$ times.** The longest substring that occurs at least $k$ times has length $\max_i \min LCP[i+1 \ldots i+k-1]$, the best window of $k - 1$ consecutive values, found with a sliding-window minimum in $O(n)$ time.
- **Non-overlapping.** Require $j \ge i + |u|$. The sorted neighbors are no longer enough. One method tests each length $L$ with a scan of the groups of the suffix array where $LCP \ge L$, keeping the smallest and the largest start position of each group; the test is monotone in $L$, so a binary search over $L$ gives $O(n \log n)$ time.
- **All longest repeats.** Report each distinct string of maximum length: these are the distinct strings at the ranks where the maximum is reached, so they come from one scan.
- **Maximal repeats.** Repeats that cannot be extended to the left or to the right with the same occurrences: see [maximal repeats](/maximal-repeats/).
- **Of several strings.** The longest substring common to two strings is the [longest common substring](/longest-common-substring/). It uses the same scan on the suffix array of the two strings joined by a separator.
- **The opposite problem.** The [shortest unique substring](/shortest-unique-substring/) asks for the shortest substring that occurs only once.

## Examples

| $T$ | longest repeat | positions | at least 3 times | non-overlapping |
|---|---|---|---|---|
| `banana` | `ana` (length 3) | 1 and 3, overlapping | `a` (length 1) | `an`, `na` (length 2) |
| `mississippi` | `issi` (length 4) | 1 and 4, overlapping | `i`, `s` (length 1) | `iss`, `ssi` (length 3) |
| `aaaaa` | `aaaa` (length 4) | 0 and 1 | `aaa` (length 3) | `aa` (length 2) |
| `abababab` | `ababab` (length 6) | 0 and 2 | `abab` (length 4) | `abab` (length 4) |
| `abcd` | empty | none | empty | empty |
| `to be or not to be` | `to be` (length 5) | 0 and 13 | length 1 | `to be` (length 5) |

For `mississippi`, $SA = [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]$ and $LCP = [0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3]$. The maximum is $LCP[3] = 4$, at the adjacent suffixes `issippi` (position 4) and `ississippi` (position 1). For the 3-fold repeat, the best window of two consecutive values is $\min(LCP[1], LCP[2]) = 1$, the three suffixes that start with `i`; no window reaches 2.

## Known algorithms

| method | time | notes |
|---|---|---|
| compare all pairs of positions | $O(n^3)$, or $O(n^2)$ with a [longest common extension](/longest-common-extension-query/) per pair | a check for small inputs |
| dynamic programming on $\mathrm{lcp}(T_i, T_j)$ for $i < j$ | $\Theta(n^2)$ time, $O(n)$ space by rows | $L[i][j] = L[i+1][j+1] + 1$ when $T[i] = T[j]$ |
| binary search on the length, with [Rabin-Karp](/rabin-karp/) hashing | $O(n \log n)$ expected | a repeat of length $L$ implies one of each shorter length |
| suffix array and [LCP array](/lcp-array/) | $O(n)$ after a linear [suffix array construction](/suffix-array-construction/) for an integer alphabet | [Kasai's algorithm](/kasai-algorithm/) gives the LCP array |
| sort the suffixes with a string sort, then compare neighbors | $O(n^2 \log n)$ worst case, fast on natural text | the client of Sedgewick and Wayne |
| [suffix tree](/suffix-tree/) | $O(n)$ for an integer alphabet | the internal node of largest string depth |
| [suffix automaton](/suffix-automaton/) | $O(n \log \sigma)$ | a state $v$ with at least two end positions and largest $len(v)$ |

## Bounds

- **Upper bound.** $O(n)$ time in the [word RAM](/word-ram/) for an integer alphabet of size $n^{O(1)}$, and $O(n \log n)$ for a general ordered alphabet, where the sort of the symbols dominates.
- **Lower bound, general alphabet.** All symbols of $T$ are different if and only if the longest repeat is empty. So [element distinctness](/element-distinctness/) reduces to this problem, and the problem needs $\Omega(n \log n)$ comparisons in the [comparison model](/comparison-model/).
- **Lower bound, integer alphabet.** $\Omega(n)$: an algorithm that does not read some symbol cannot tell a text with a repeat through it from one without.

## Reductions

- **To the maximum of the LCP array.** As in the definition, in $O(n)$ time once the arrays exist.
- **From element distinctness.** As in the bounds.
- **To the longest common substring.** The longest common substring of $X$ and $Y$ is a longest repeat of $X \# Y$ (with a separator $\#$ that occurs in neither) whose two occurrences are on different sides of $\#$.

## Applications

- **Data compression.** Long repeats are what dictionary methods such as [LZ77](/lz77/) exploit. The longest repeat bounds the length of the longest phrase.
- **Biology.** Long repeats in DNA mark duplicated genes and transposons, and they make genome assembly hard: a read shorter than the longest repeat cannot tell its copies apart.
- **Plagiarism and code clone detection.** A long repeat in a file, or across files joined with separators, shows copied text.
- **Teaching.** It is the first application of the suffix array in many textbooks, with the [keyword-in-context search](/keyword-in-context-search/).

## References
