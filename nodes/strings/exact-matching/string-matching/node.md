---
tag: 71WJZT
kind: problem
slug: string-matching
name: String matching (exact pattern matching)
aliases:
- exact string matching
- substring search
- pattern matching
area: strings/exact-matching
level: intro
summary: Find all occurrences of a pattern P in a text T.
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern}
  time: {worst: Θ(n + m)}
prereqs: [alphabet, asymptotic-notation]
see_also: [naive-string-matching, knuth-morris-pratt, boyer-moore, rabin-karp, string-matching-lower-bound, dictionary-matching, approximate-string-matching, suffix-array]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 32, String Matching (the introduction defines valid shifts; Sections 32.1 to 32.4 give the naive, Rabin-Karp, automaton and KMP algorithms)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapters 1 to 4 (exact matching, pages 5 to 86)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 2, Single string matching (prefix-based, suffix-based and factor-based approaches, and the experimental map)
  - paper: doi:10.1137/0206048
    title: R. L. Rivest, On the worst-case behavior of string-searching algorithms, SIAM Journal on Computing 6(4) (1977), 669-674
    locator: the main theorem (the lower bound of n - m + 1 character reads)
  - paper: doi:10.1137/0208029
    title: A. C. Yao, The complexity of pattern matching for a random string, SIAM Journal on Computing 8(3) (1979), 368-387
    locator: the main theorem (the average number of characters examined on a random text)
  - paper: doi:10.1137/0206024
    title: D. E. Knuth, J. H. Morris and V. R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2) (1977), 323-350
    locator: the linear-time algorithm and the historical remarks at the end of the paper
---

String matching is the problem of finding every position where a pattern string $P$ of length $m$ occurs as a contiguous block of a text string $T$ of length $n$. It is solved in $\Theta(n + m)$ time in the worst case on the [word RAM](/word-ram/), for example by [Knuth-Morris-Pratt](/knuth-morris-pratt/), and no algorithm can do better in the worst case, because it must read almost all of the text. It is the search function of every text editor and of tools such as `grep`, and many harder string problems reduce to it.

## In plain words

You have a long text and a short word. You want to know every place where the word appears in the text, letter for letter. The answer is a list of starting positions.

Two places may overlap. In the text "aaaaa", the word "aaa" starts at the first, the second and the third letter, and all three count.

The obvious method puts the word at each start, compares letter by letter, and moves one step to the right. It can be slow when the text and the word repeat the same letters. Faster methods learn from the comparisons that they already made. They never look back in the text, or they jump forward by more than one step.

## Definition

**Alphabet.** An [alphabet](/alphabet/) $\Sigma$ is a set of characters. Write $\sigma = |\Sigma|$ when it is finite. The algorithms of this area use one of three models of the alphabet:

- a *general* alphabet: the algorithm may only test two characters for equality;
- a *general ordered* alphabet: the algorithm may also test $a < b$ in a total order;
- an *integer* alphabet $\Sigma = \{0, 1, \ldots, \sigma - 1\}$: a character may also index an array, so a table of size $\sigma$ costs $\Theta(\sigma)$ time and space. A *constant-size* alphabet is an integer alphabet with $\sigma = O(1)$.

**Input.** A text $T = T[0 \ldots n-1] \in \Sigma^n$ and a pattern $P = P[0 \ldots m-1] \in \Sigma^m$, with $n, m \ge 0$. Indices are 0-based on all pages of this area.

**Output.** The set of *valid shifts*

$$\mathrm{Occ}(P, T) = \{\, s \in \mathbb{Z} : 0 \le s \le n - m \text{ and } T[s + j] = P[j] \text{ for each } 0 \le j < m \,\}.$$

A shift $s$ in this set is an *occurrence* of $P$ at position $s$. The output is usually listed in increasing order.

**Conventions.**

- Occurrences may overlap: both $s$ and $s + 1$ may be valid shifts.
- If $m > n$, there is no valid shift and the output is empty.
- If $m = 0$, the condition on $j$ is empty, so every $s$ with $0 \le s \le n$ is valid, and the output has $n + 1$ elements. Library functions differ here: some return position 0 only. The implementations on the pages of this area return all $n + 1$ positions.

## Variants

- **Decision.** Does $P$ occur in $T$ at all? This is the problem of the [lower bound](/string-matching-lower-bound/).
- **First occurrence.** Return the least valid shift, or report that none exists. A library `find` or `indexOf` solves this.
- **Counting.** Return $|\mathrm{Occ}(P, T)|$. All linear-time algorithms below also count in linear time.
- **Non-overlapping occurrences.** Return a greedy set of occurrences that do not overlap, as a "replace all" function needs. Scan the sorted valid shifts and keep a shift when it is at least $m$ after the last kept one.
- **Online or streaming.** The text arrives one character at a time, and the algorithm must report an occurrence as soon as its last character arrives. [Knuth-Morris-Pratt](/knuth-morris-pratt/), the [string-matching automaton](/string-matching-automaton/) and [Shift-Or](/shift-or/) work in this way. A *real-time* algorithm also spends $O(1)$ time on each character.
- **Indexing.** The text is fixed and many patterns come later. Build a [suffix tree](/suffix-tree/) or a [suffix array](/suffix-array/) of $T$ once, then answer each pattern in time that depends on $m$ and the number of occurrences, not on $n$.
- **Many patterns.** Find all occurrences of each pattern of a set. This is [dictionary matching](/dictionary-matching/), solved by [Aho-Corasick](/aho-corasick/).
- **Approximate.** Allow some mismatches or edits. See [approximate string matching](/approximate-string-matching/) and [Hamming string matching](/hamming-string-matching/).
- **Generalized equality.** Match up to a rotation ([circular pattern matching](/circular-pattern-matching/)), up to a renaming of symbols ([parameterized matching](/parameterized-pattern-matching/)), or up to the relative order of the values ([order-preserving matching](/order-preserving-matching/)).
- **Compressed text.** Search a text given in compressed form without full decompression: [pattern matching in compressed text](/pattern-matching-in-compressed-text/).

## Examples

| text $T$ | pattern $P$ | $\mathrm{Occ}(P, T)$ | note |
|---|---|---|---|
| abracadabra | abra | 0, 7 | two separate occurrences |
| abaababaab | aba | 0, 3, 5 | the occurrences at 3 and 5 overlap |
| aaaaa | aaa | 0, 1, 2 | the maximum $n - m + 1$ occurrences |
| abc | (empty) | 0, 1, 2, 3 | $n + 1$ occurrences of the empty pattern |
| ab | abc | none | $m > n$ |
| abcabc | cab | 2 | |

**Non-example.** "aba" is not an occurrence of "aa" in "aba". The letters a, a appear in "aba" as a *subsequence*, but string matching asks for a contiguous block. Subsequence search is a different problem, solved by one greedy scan.

The output can have $\Theta(n)$ elements: for $T = a^n$ and $P = a^m$ with $m \le n$, every shift from $0$ to $n - m$ is valid. So an algorithm that lists all occurrences cannot be faster than the size of its output.

## Known algorithms

All bounds are worst-case bounds, except where they say "average". The extra space does not count the input or the output.

| algorithm | alphabet | preprocessing | search | extra space |
|---|---|---|---|---|
| [naive](/naive-string-matching/) | general | none | $O((n - m + 1)m)$ | $O(1)$ |
| [Morris-Pratt](/morris-pratt/), [Knuth-Morris-Pratt](/knuth-morris-pratt/) | general | $O(m)$ | $O(n)$ | $O(m)$ |
| [Z-algorithm](/z-algorithm/) on $P \$ T$ | general | | $O(n + m)$ total | $O(n + m)$ |
| [string-matching automaton](/string-matching-automaton/) | integer | $O(m\sigma)$ | $O(n)$, one step per character | $O(m\sigma)$ |
| [Rabin-Karp](/rabin-karp/) | integer | $O(m)$ | $O(n + m)$ expected | $O(1)$ |
| [Shift-Or](/shift-or/) | integer | $O(\sigma + m)$ | $O(n \lceil m / w \rceil)$ | $O(\sigma \lceil m / w \rceil)$ |
| [Boyer-Moore](/boyer-moore/) | integer | $O(m + \sigma)$ | $O(nm)$; $O(n)$ with the [Galil rule](/galil-rule/) | $O(m + \sigma)$ |
| [Horspool](/boyer-moore-horspool/), [Quick Search](/quick-search/) | integer | $O(m + \sigma)$ | $O(nm)$; fast on average | $O(\sigma)$ |
| [Turbo-BM](/turbo-boyer-moore/), [Apostolico-Giancarlo](/apostolico-giancarlo/) | integer | $O(m + \sigma)$ | $O(n)$ | $O(m + \sigma)$ |
| [backward DAWG matching](/backward-dawg-matching/) | integer | $O(m\sigma)$ | $O(nm)$; $O((n / m)\log_\sigma m)$ average | $O(m\sigma)$ |
| [two-way](/two-way-string-matching/) | general ordered | $O(m)$ | $O(n)$ | $O(1)$ |
| [Galil-Seiferas](/galil-seiferas/) | general | $O(m)$ | $O(n)$ | $O(1)$ |

Here $w$ is the word size of the word RAM, and the average is over a uniformly random text.

## Bounds

**Upper bound.** Knuth-Morris-Pratt runs in $O(n + m)$ time on a general alphabet, with at most $2n$ character comparisons in its search phase. The two-way and Galil-Seiferas algorithms reach $O(n + m)$ time with $O(1)$ extra words of memory.

**Lower bound, worst case.** Rivest (1977) proved that for each pattern with $m \ge 1$ over an alphabet with at least two letters, each deterministic algorithm reads at least $n - m + 1$ characters of the text on some text of length $n$, even to decide whether $P$ occurs. Together with the $m$ reads of the pattern, this gives $\Omega(n + m)$ time, so $\Theta(n + m)$ is tight. The proof is on the page [string matching lower bound](/string-matching-lower-bound/).

**Lower bound, average case.** Yao (1979) proved that on a uniformly random text over $\sigma \ge 2$ letters, for almost all patterns, each algorithm reads $\Omega((n / m)\log_\sigma m)$ characters on average, and that this is reachable. [Backward DAWG matching](/backward-dawg-matching/) reaches it. So the best average is sublinear when $m$ grows.

**Output size.** Listing all occurrences takes $\Omega(|\mathrm{Occ}(P, T)|)$ time, which is $\Theta(n)$ in the worst case. In the indexing variant, after the preprocessing of $T$, a query takes $O(m + |\mathrm{Occ}(P, T)|)$ time with a suffix tree over a constant-size alphabet.

## Reductions

- **To the prefix function.** Compute the [prefix function](/prefix-function/) of $P \# T$, where $\#$ is a character not in $\Sigma$. Then $s$ is a valid shift exactly when the value at index $m + s + m$ equals $m$. The cost is $O(n + m)$.
- **To the Z-array.** Compute the [Z-array](/z-algorithm/) of $P \# T$. Then $s$ is a valid shift exactly when $Z[m + 1 + s] = m$. The cost is $O(n + m)$.
- **To polynomial multiplication.** Over the integers, $\sum_j (T[s + j] - P[j])^2 = 0$ exactly when $s$ is valid. Expand the square: each of the three sums is a convolution, so all $n - m + 1$ sums take $O(n \log n)$ time with the [fast Fourier transform](/fast-fourier-transform/). This is slower than KMP for exact matching, but it extends to patterns with wildcards.
- **Conjugacy reduces to string matching.** Two strings $u$ and $v$ of the same length are rotations of each other exactly when $u$ occurs in $vv$. See [conjugacy testing](/word-conjugacy-testing/).

## Applications

- The "find" command of editors and the `strstr`, `str.find` and `indexOf` functions of standard libraries.
- Searching files with `grep` when the expression is a fixed string.
- Searching DNA and protein sequences for a known motif.
- Signature search in antivirus and network intrusion detection, usually with many patterns at once.
- As a step in other algorithms: [conjugacy testing](/word-conjugacy-testing/), the [period](/string-period/) of a string, and the filters of [approximate matching](/approximate-string-matching/).

## References
