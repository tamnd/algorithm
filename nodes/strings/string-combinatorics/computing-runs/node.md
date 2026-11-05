---
tag: 7JC3F4
kind: problem
slug: computing-runs
name: Computing runs
aliases:
- runs computation
- maximal repetitions finding
area: strings/string-combinatorics
level: advanced
summary: List all runs of a string together with their periods and positions.
prereqs: [maximal-repetition, string-period]
see_also: [runs-theorem, lyndon-based-runs-computation, main-lorentz-algorithm, lyndon-array, lempel-ziv-factorization, counting-distinct-squares, square-free-word, longest-common-extension-query]
sources:
  - paper: doi:10.1109/sffcs.1999.814634
    title: Roman Kolpakov and Gregory Kucherov, Finding maximal repetitions in a word in linear time, 40th Annual Symposium on Foundations of Computer Science (FOCS 1999), 596-604
    locator: the linear bound on the number of runs and the linear-time algorithm from the Lempel-Ziv factorization over an integer alphabet
  - paper: doi:10.1137/15M1011032
    title: Hideo Bannai, Tomohiro I, Shunsuke Inenaga, Yuto Nakashima, Masayuki Takeda and Kazuya Tsuruta, The "Runs" Theorem, SIAM Journal on Computing 46(5), 2017, 1501-1514
    locator: the bound of n runs and the simple linear-time algorithm from Lyndon arrays for two orders and longest common extensions
  - paper: doi:10.1016/0020-0190(81)90024-7
    title: Maxime Crochemore, An optimal algorithm for computing the repetitions in a word, Information Processing Letters 12(5), 1981, 244-250
    locator: all maximal repetitions in O(n log n) time by refining partitions, and the O(n log n) bound on primitively rooted squares
  - paper: doi:10.1016/0196-6774(84)90021-x
    title: Michael G. Main and Richard J. Lorentz, An O(n log n) algorithm for finding all repetitions in a string, Journal of Algorithms 5(3), 1984, 422-432
    locator: the divide and conquer algorithm for all repetitions and the lower bound for algorithms that only test letters for equality
  - url: "https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2021.63"
    title: Jonas Ellert and Johannes Fischer, Linear time runs over general ordered alphabets, ICALP 2021, LIPIcs 198, 63:1-63:16
    locator: the linear-time computation of all runs when letters can only be compared, through the Lyndon array
  - paper: doi:10.1007/978-3-319-46049-9_3
    title: Maxime Crochemore, Costas S. Iliopoulos, Tomasz Kociumaka, Ritu Kundu, Solon P. Pissis, Jakub Radoszewski, Wojciech Rytter and Tomasz Waleń, Near-optimal computation of runs over general alphabet via non-crossing LCE queries, SPIRE 2016, Lecture Notes in Computer Science 9954, 22-34
    locator: runs over a general ordered alphabet in O(n α(n)) time
  - paper: doi:10.1016/j.ipl.2015.11.016
    title: Dmitry Kosolobov, Computing runs on a general alphabet, Information Processing Letters 116(3), 2016, 241-244
    locator: the first o(n log n) algorithm for runs over a general ordered alphabet
---

Computing runs is the problem of listing all [maximal repetitions](/maximal-repetition/) of a string: every maximal factor whose smallest period $p$ fits at least twice into it, together with its start, end and period. A string of length $n$ has fewer than $n$ runs by the [runs theorem](/runs-theorem/), so the output is linear, and the problem can be solved in $O(n)$ time over integer alphabets and over general ordered alphabets. Since runs hold all squares and higher repetitions, this one listing answers many questions about periodicity: testing square-freeness, counting distinct squares, or finding the largest exponent of a repetition.

## In plain words

Look for the places where a string repeats itself: a block written twice or more in a row, maybe with a broken copy at the end, like `abcabcab`. Make each such place as long as it can be while it keeps repeating the same block, and use the shortest block that works. Each of these stretches is a run. The task is to write down every run: where it starts, where it ends, and how long its block is. A string never has more runs than letters, so the list is short, even when the string has very many repeated pieces.

## Definition

The input is a string $s = s[0..n-1]$ over an [alphabet](/alphabet/) $\Sigma$. Indices are 0-based. Depending on the model, $\Sigma$ is an integer alphabet $\{0, \ldots, n^{O(1)}\}$, a general ordered alphabet (letters can only be compared), or a general unordered alphabet (letters can only be tested for equality).

A run is a triple $(i, j, p)$ with $0 \le i \le j < n$ such that $p$ is the smallest [period](/string-period/) of $s[i..j]$, $j - i + 1 \ge 2p$, and the period $p$ does not extend: $i = 0$ or $s[i-1] \ne s[i-1+p]$, and $j = n - 1$ or $s[j+1] \ne s[j+1-p]$. Its exponent is $(j - i + 1)/p$.

**Output.** The set $\mathrm{Runs}(s)$ of all runs, as a list of triples in any order.

## Variants

- **All primitively rooted squares.** List every occurrence $s[i..i+2p-1]$ of a square $uu$ with $u$ [primitive](/primitive-word/). Each lies in exactly one run, and a run $(i, j, p)$ holds $j - i + 2 - 2p$ of them, so they come from the runs in time proportional to their number, which is $O(n \log n)$ and can be that large.
- **All repetitions.** Listing every square occurrence, including non-primitive roots, has output size up to $\Theta(n^2)$, as in $a^n$.
- **Leftmost occurrences.** Main (1989) reports the leftmost occurrence of each distinct run, or each distinct repetition type, from the Lempel-Ziv factorization.
- **Testing square-freeness.** Decide whether there is at least one run, the decision version.
- **Distinct squares.** Count or list the distinct square factors; see [counting distinct squares](/counting-distinct-squares/).
- **Runs of large exponent.** Report only the runs of exponent at least $e$, for example the cubes, or the run of largest exponent (the local critical exponent of a finite word).
- **Gapped and approximate repeats.** Allow a gap between the two copies, or mismatches between them; these are separate problems with their own algorithms.

## Examples

| $s$ | $n$ | runs $(i, j, p)$ |
|---|---|---|
| `aabaabaa` | 8 | $(0, 7, 3)$, $(0, 1, 1)$, $(3, 4, 1)$, $(6, 7, 1)$ |
| `mississippi` | 11 | $(1, 7, 3)$, $(2, 3, 1)$, $(5, 6, 1)$, $(8, 9, 1)$ |
| `banana` | 6 | $(1, 5, 2)$ |
| `abcacb` | 6 | none: the string is square-free |
| $a^n$ | $n \ge 2$ | $(0, n-1, 1)$ only |

- The string $a^n$ has one run but $\Theta(n^2)$ square occurrences, which is why the runs are the useful output.
- The [Fibonacci word](/fibonacci-word/) $f_6 = $ `abaababaabaababaababa`, of length 21, has 13 runs, among them $(0, 5, 3)$, $(0, 10, 5)$, $(0, 18, 8)$ and $(2, 3, 1)$. In general $f_k$ has $2|f_{k-2}| - 3$ runs for $k \ge 3$.

## Known algorithms

- **Quadratic method.** For each $p$ from 1 to $n/2$, scan the positions $t$ with $s[t] = s[t + p]$; each maximal interval of such positions with length at least $p$ gives a maximal factor of period $p$ and length at least $2p$. Keep it if no proper divisor of $p$ is also a period of it (by the [Fine and Wilf theorem](/fine-and-wilf-theorem/), a smaller period would divide $p$). This takes $O(n^2)$ time and is a good test oracle.
- **Crochemore (1981).** Refining the partitions of positions by equal factors of length $1, 2, 3, \ldots$ finds all maximal repetitions in $O(n \log n)$ time; this is optimal for listing all primitively rooted square occurrences.
- **Main and Lorentz (1984).** A [divide and conquer](/main-lorentz-algorithm/) that finds the repetitions crossing the middle with Z-function computations, in $O(n \log n)$ time; it works with equality tests only.
- **Kolpakov and Kucherov (1999).** Compute the [Lempel-Ziv factorization](/lempel-ziv-factorization/) with a suffix tree, then find the runs that cross a phrase boundary with the method of Main and extend the others from their earlier copies. This gives $O(n)$ time over an integer alphabet, and proved that the number of runs is $O(n)$.
- **Lyndon roots (Bannai et al., 2017).** For each of the two orders $a < b$ and $b < a$, compute the [Lyndon array](/lyndon-array/), and for each $i$ take the longest Lyndon word $s[i..e]$ starting at $i$ as a candidate root; [longest common extensions](/longest-common-extension-query/) on both sides decide in $O(1)$ time whether it is the root of a run. This takes $O(n)$ time; see [Lyndon-based runs computation](/lyndon-based-runs-computation/).
- **General ordered alphabets.** Kosolobov showed how to do it in $O(n \log^{2/3} n)$ time, Crochemore et al. (2016) in $O(n \alpha(n))$ time, and Ellert and Fischer (2021) in $O(n)$ time, using only comparisons of letters.

## Bounds

- **Output.** $|\mathrm{Runs}(s)| < n$, and the sum of the exponents of the runs is at most $3n$ (Bannai et al.). Fischer, Holub, I and Lewenstein improved the first bound to $22n/23$. The best known families have about $0.9445n$ runs, so the largest constant is between these values.
- **Time.** $\Omega(n)$, to read the input, which the algorithms above meet for integer and for general ordered alphabets.
- **Equality tests only.** Main and Lorentz proved that deciding whether a string has a square needs $\Omega(n \log n)$ equality tests on a general unordered alphabet, and their algorithm meets this bound. The order on letters is what allows linear time.

## Reductions

- **To Lyndon arrays and LCE queries.** Every run with period $p$ contains a Lyndon root of length $p$ for one of the two orders, and that root is the longest Lyndon word starting at its position. So the runs are among $2n$ candidates, each checked with two longest common extension queries.
- **From square-freeness.** A string is square-free if and only if it has no run, so any algorithm for runs decides square-freeness, and the equality-test lower bound of Main and Lorentz carries over to runs.
- **To Lempel-Ziv.** Every run that does not cross a phrase boundary of the LZ factorization has an earlier copy, which gives the Kolpakov-Kucherov reduction.
- **To distinct squares and critical exponents.** The distinct squares, the cubes, and the maximal exponent of $s$ are read from the list of runs in linear time.

## Applications

- **Tandem repeats in DNA.** Microsatellites and other tandem repeats are runs, or approximate runs, of short periods in genomic sequences.
- **Compression and indexing.** Runs bound the number of distinct squares and appear in the analysis of [Lempel-Ziv](/lempel-ziv-factorization/) parsing and of compressed indexes.
- **Combinatorics on words.** Computing the runs of long [square-free](/square-free-word/) or repetition-avoiding words checks constructions and measures exponents, and searches for run-rich strings use fast runs algorithms.
- **Periodicity questions.** Finding the shortest period of every factor, primitively rooted squares, or the repetitions with largest exponent.

## References
