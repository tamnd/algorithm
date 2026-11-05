---
tag: B8YJN8
kind: algorithm
slug: lyndon-based-runs-computation
name: Lyndon-based runs computation
aliases:
- Bannai et al. runs algorithm
- Lyndon roots runs algorithm
area: strings/string-combinatorics
level: research
summary: Computes all runs in linear time from Lyndon roots and longest common extensions.
solves: [computing-runs]
model: word-ram
complexity:
  vars: {n: the length of the string}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [runs-theorem, lyndon-array, longest-common-extension-query]
see_also: [computing-runs, maximal-repetition, main-lorentz-algorithm, lyndon-word, fine-and-wilf-theorem, suffix-array, kasai-algorithm, range-minimum-query]
sources:
  - paper: doi:10.1137/15m1011032
    title: Hideo Bannai, Tomohiro I, Shunsuke Inenaga, Yuto Nakashima, Masayuki Takeda and Kazuya Tsuruta, The "Runs" Theorem, SIAM Journal on Computing 46(5), 2017, 1501-1514
    locator: the Lyndon roots of a run under one of two opposite orders, the lemma that a Lyndon root is the longest Lyndon word starting at its position, and the linear-time algorithm that extends each Lyndon array entry with longest common extension queries
  - paper: doi:10.1109/sffcs.1999.814634
    title: Roman Kolpakov and Gregory Kucherov, Finding maximal repetitions in a word in linear time, 40th Annual Symposium on Foundations of Computer Science (FOCS 1999), 596-604
    locator: the first linear-time algorithm for all runs over a constant alphabet, from the Lempel-Ziv factorization and Main-Lorentz extension functions
  - paper: doi:10.1007/978-3-319-46049-9_3
    title: Maxime Crochemore, Costas S. Iliopoulos, Tomasz Kociumaka, Ritu Kundu, Solon P. Pissis, Jakub Radoszewski, Wojciech Rytter and Tomasz Waleń, Near-optimal computation of runs over general alphabet via non-crossing LCE queries, String Processing and Information Retrieval (SPIRE 2016), Lecture Notes in Computer Science 9954, 22-34
    locator: the Lyndon-based scheme over a general ordered alphabet, with the observation that the LCE queries it asks do not cross, answered in O(n·α(n)) total time
  - paper: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2021.63
    title: Jonas Ellert and Johannes Fischer, Linear Time Runs over General Ordered Alphabets, 48th International Colloquium on Automata, Languages, and Programming (ICALP 2021), LIPIcs 198, 63:1-63:16
    locator: the Lyndon array and the extensions computed in O(n) time with only letter comparisons
---

The Lyndon-based runs computation lists all [runs](/maximal-repetition/) of a string of length $n$ in $O(n)$ time. Every run has a root that is a [Lyndon word](/lyndon-word/) for one of two opposite letter orders, and that root is exactly the longest Lyndon word starting at its position. So it suffices to take each entry of the two [Lyndon arrays](/lyndon-array/), extend it to the left and right with [longest common extension queries](/longest-common-extension-query/), and keep the extensions of length at least twice the period. The method comes from the proof of the [runs theorem](/runs-theorem/) by Bannai et al., and it is much simpler than the earlier linear-time algorithm of Kolpakov and Kucherov.

## In plain words

A run is a stretch of text that repeats a short block at least twice and cannot be stretched further. Rotate that block to its alphabetically smallest form; this rotated block is a Lyndon word, and it really occurs inside the run. At that place, the longest Lyndon word that starts there is exactly the block, provided the alphabet order is chosen by how the run ends, which is why two orders are tried. So the algorithm looks at every position, takes the longest Lyndon word starting there as a guessed block, and measures how far the text keeps repeating that block to the left and to the right. If the repetition covers at least two blocks, it is a run. Every guess is cheap, and every run is found.

## The problem

The input is a string $s = s[0..n-1]$ over a totally ordered [alphabet](/alphabet/); for the linear time bound the letters are integers in $\{0, \ldots, n^{O(1)}\}$. Indices are 0-based. A run is a triple $(i, j, p)$ with $0 \le i \le j < n$ such that $p$ is the smallest [period](/string-period/) of $s[i..j]$, $j - i + 1 \ge 2p$, and the period $p$ does not extend: $i = 0$ or $s[i-1] \ne s[i-1+p]$, and $j = n - 1$ or $s[j+1] \ne s[j+1-p]$. The output is the set of all runs, which has fewer than $n$ elements by the runs theorem. This is the problem of [computing runs](/computing-runs/).

## The algorithm

Let $<_0$ be the order on letters and $<_1$ its reverse. Each order is extended to words lexicographically, with a proper prefix smaller than the longer word. $\lambda_\ell[i]$ is the length of the longest prefix of $s[i..n-1]$ that is a Lyndon word for $<_\ell$. $\mathrm{LCP}(i, j)$ is the length of the longest common prefix of $s[i..n-1]$ and $s[j..n-1]$, and $\mathrm{LCS}(i, j)$ that of the longest common suffix of $s[0..i-1]$ and $s[0..j-1]$.

```pseudo id=main
RUNS(s)                                          ▷ s[0 .. n − 1]
L1  R ← empty set; build LCP queries on s and LCS queries on s (via its reversal)
L2  for ℓ ← 0 to 1 do
L3      λ ← LYNDON-ARRAY(s, <ℓ)
L4      for i ← 0 to n − 1 do
L5          p ← λ[i], j ← i + p
L6          l ← i − LCS(i, j)                     ▷ LCS(0, j) = 0
L7          r ← j + LCP(i, j)                     ▷ LCP(i, n) = 0
L8          if r − l ≥ 2p then add (l, r − 1, p) to R
L9  return R
```

Line L3 uses the fact that $\lambda_\ell[i] = j - i$, where $j$ is the first index after $i$ whose suffix is smaller than the suffix at $i$ for $<_\ell$, or $n$. With a [suffix array](/suffix-array/) for $<_\ell$ these next smaller suffixes are found by one scan from right to left with a [monotonic stack](/monotonic-stack/). The queries of lines L6 and L7 are [range minimum queries](/range-minimum-query/) on the LCP array, built by the [Kasai algorithm](/kasai-algorithm/), of $s$ and of its reversal. Lines L6 and L7 stretch the factor $s[i..j-1]$ with the period $p$ as far as it goes; line L8 keeps it if it has at least two periods.

## Example

Let $s = $ `aabaabaa`, $n = 8$, with $a <_0 b$ and $b <_1 a$. Each cell gives $\lambda_\ell[i]$ and the interval $[l, r)$ of lines L6 and L7; a star marks $r - l \ge 2\lambda_\ell[i]$.

| $i$ | $s[i]$ | $\lambda_0[i]$ | $[l, r)$ for $<_0$ | $\lambda_1[i]$ | $[l, r)$ for $<_1$ |
|---|---|---|---|---|---|
| 0 | `a` | 3 (`aab`) | $[0, 8)$ * | 1 | $[0, 2)$ * |
| 1 | `a` | 2 (`ab`) | $[1, 4)$ | 1 | $[0, 2)$ * |
| 2 | `b` | 1 | $[2, 3)$ | 3 (`baa`) | $[0, 8)$ * |
| 3 | `a` | 3 (`aab`) | $[0, 8)$ * | 1 | $[3, 5)$ * |
| 4 | `a` | 2 (`ab`) | $[4, 7)$ | 1 | $[3, 5)$ * |
| 5 | `b` | 1 | $[5, 6)$ | 3 (`baa`) | $[0, 8)$ * |
| 6 | `a` | 1 | $[6, 8)$ * | 1 | $[6, 8)$ * |
| 7 | `a` | 1 | $[6, 8)$ * | 1 | $[6, 8)$ * |

For $i = 1$ and $<_0$, $p = 2$ and $j = 3$: the letters before them, $s[0] = $ `a` and $s[2] = $ `b`, differ, so $l = 1$; $s[1..]$ = `abaabaa` and $s[3..]$ = `aabaa` share one letter, so $r = 4$, and $[1, 4)$ is too short for period 2. For $i = 0$ and $<_0$, `aab` repeats over the whole word, so $[0, 8)$ with $p = 3$ is reported. After removing duplicates, $R = \{(0, 1, 1), (0, 7, 3), (3, 4, 1), (6, 7, 1)\}$: the runs `aa` three times and `aabaabaa` with period 3. The run $(0, 1, 1)$ is found only with $<_1$, because it is followed by `b` and $b <_1 a$; with $<_0$, the Lyndon word at 0 is `aab`, longer than its root `a`.

## Correctness

Two facts carry the proof, given in full in the proof file.

- **Each reported triple is a run.** Lines L6 and L7 return the maximal interval $[l, r)$ around $[i, i + p)$ with the period $p$, so $s[l..r-1]$ cannot be extended. If its smallest period were some $q < p$, then since $r - l \ge 2p \ge p + q$, the [Fine and Wilf theorem](/fine-and-wilf-theorem/) would make $\gcd(p, q)$ a period, and the Lyndon word $s[i..i+p-1]$ would be a proper power. Lyndon words are primitive, so $p$ is the smallest period.
- **Each run is reported.** Let $[l, r)$ be a run with period $p$. If $r < n$, choose $\ell$ with $s[r] <_\ell s[r-p]$; if $r = n$, either order works. The $p$ factors of length $p$ starting in $[l, l + p)$ are the rotations of a primitive word, and the least of them for $<_\ell$ is a Lyndon word, starting at some $c$. A longer Lyndon word starting at $c$ is impossible: if it ends inside the run, it has the period $p$ and so a border; if it ends after $r$, its suffix starting at $c + p$ is smaller, because of the letter $s[r]$. So $\lambda_\ell[c] = p$, and the extension at $c$ gives exactly $[l, r)$.

## Complexity

- **Time.** On an integer alphabet, the suffix arrays of $s$ under both orders and of its reversal take $O(n)$ time with a linear suffix sorting algorithm, and the LCP arrays $O(n)$ with the Kasai algorithm. A range minimum structure on an LCP array answers each query in $O(1)$ after $O(n)$ preprocessing. The two Lyndon arrays take $O(n)$ with the stack, and lines L4 to L8 run $2n$ times in $O(1)$ each. Removing duplicates among the at most $2n$ candidates takes $O(n)$ with a radix sort. So the time is $\Theta(n)$ on every input.
- **Space.** The arrays and the range minimum structures take $\Theta(n)$ words.
- **Output.** There are fewer than $n$ runs, and their exponents sum to at most $3n$, by the runs theorem. The argument above maps each run to a Lyndon root starting after its first position, which is the core of the proof of that theorem.

## Properties

- **Deterministic and offline.** The suffix arrays need the whole string.
- **Order-based.** The algorithm compares letters by order, not only for equality. The output does not depend on the order chosen, since the two orders are used symmetrically.
- **Simple building blocks.** Apart from the suffix array and range minima, it is two loops and one stack, with no Lempel-Ziv factorization.
- **Every run is found at its Lyndon roots.** Each run with $r - l \ge 3p$ is found several times; the duplicates are harmless.

## Variants and improvements

- **General ordered alphabets.** With only letter comparisons, suffix sorting costs $\Theta(n \log n)$. Crochemore, Iliopoulos, Kociumaka, Kundu, Pissis, Radoszewski, Rytter and Waleń noted that the LCE queries of the algorithm can be answered in $O(n \alpha(n))$ total time, and Ellert and Fischer gave an $O(n)$-time algorithm that computes the Lyndon array and the extensions with comparisons only.
- **Simpler preprocessing.** Prefix doubling for the suffix array and a sparse table for range minima give $O(n \log n)$ time with very short code, which is often enough in practice.
- **Squares and repetitions.** From the runs, all primitively rooted squares, the [distinct squares](/counting-distinct-squares/) and the maximal exponent follow in linear time.
- **Without both orders.** Using only $<_0$ can miss a run whose next letter is larger in $<_0$ than the letter one period earlier, as the run `aa` at 0 in the example. Both orders are needed for completeness.

## When to use it

Use it to compute all runs of a string over an integer alphabet in linear time, or as the basis of a square or repetition finder. It is shorter than the Kolpakov-Kucherov algorithm and needs no Lempel-Ziv factorization. If only equality tests on letters are available, use the $O(n \log n)$ [Main-Lorentz algorithm](/main-lorentz-algorithm/).

## Pitfalls

- **The order on the end of the string.** The Lyndon array and the next smaller suffixes must treat a proper prefix as smaller under both orders; reversing the order of letters does not reverse the role of the end. Negating letter codes while keeping a sentinel $-1$ for the end breaks this.
- **Only one order.** Using a single order misses runs, as in the example.
- **The left extension.** $\mathrm{LCS}(i, j)$ compares the texts before $i$ and before $j = i + p$, not after; with a reversed string, the positions $i$ and $j$ become $n - i$ and $n - j$.
- **Duplicates.** The same run is found from several positions and both orders, so the output must be deduplicated.
- **Out of range.** For $j = n$ the right extension is 0; for $i = 0$ the left extension is 0.

## Implementations

## History

Kolpakov and Kucherov gave the first linear-time algorithm for all runs in 1999, over a constant alphabet, from the Lempel-Ziv factorization; they conjectured that there are fewer than $n$ runs. Bannai, I, Inenaga, Nakashima, Takeda and Tsuruta proved that conjecture with Lyndon roots, in a paper presented at SODA 2015 and published in the SIAM Journal on Computing in 2017, and the same idea gave this simple linear-time algorithm over integer alphabets. Crochemore et al. adapted it to general ordered alphabets in 2016 with $O(n \alpha(n))$ time, and Ellert and Fischer reached $O(n)$ time over general ordered alphabets in 2021.

## References
