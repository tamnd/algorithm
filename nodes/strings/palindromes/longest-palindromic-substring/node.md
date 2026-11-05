---
tag: Y8028H
kind: problem
slug: longest-palindromic-substring
name: Longest palindromic substring
aliases:
- longest palindrome substring
- longest palindromic factor
area: strings/palindromes
level: intro
summary: Find a longest contiguous substring of a string that is a palindrome.
model: comparison-model
complexity:
  vars: {n: the length of the string}
  time: {worst: Θ(n)}
  space: {aux: Θ(n)}
prereqs: [palindrome, palindrome-recognition]
see_also: [manacher, palindromic-tree, longest-palindromic-subsequence, palindrome-substring-queries, shortest-palindrome, suffix-tree, longest-common-extension-query, polynomial-rolling-hash]
sources:
  - paper: doi:10.1145/321892.321896
    title: Glenn Manacher, A new linear-time on-line algorithm for finding the smallest initial palindrome of a string, Journal of the ACM 22(3) (1975), 346-351
    locator: the whole paper (the linear-time scan over centers that reuses the mirror radius)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 9, Section 9.2, Finding all maximal palindromes in linear time (pages 197 to 199)
  - paper: doi:10.1016/0304-3975(94)00083-U
    title: Alberto Apostolico, Dany Breslauer and Zvi Galil, Parallel detection of all palindromes in a string, Theoretical Computer Science 141 (1995), 163-173
    locator: the introduction (all maximal palindromes from Manacher's scan) and the parallel algorithm
  - paper: doi:10.4230/LIPIcs.CPM.2022.20
    title: Panagiotis Charalampopoulos, Solon P. Pissis and Jakub Radoszewski, Longest palindromic substring in sublinear time, CPM 2022, LIPIcs 223, 20:1-20:9
    locator: the main theorem (O(n log σ / log n) time on a word RAM for a packed string)
  - url: https://en.wikipedia.org/wiki/Longest_palindromic_substring
    title: Wikipedia, Longest palindromic substring
    locator: the sections on the slow algorithm, Manacher's algorithm and the history of the problem
---

The longest palindromic substring problem asks for a longest contiguous piece of a string that is a [palindrome](/palindrome/). Testing all $\Theta(n^2)$ substrings costs $\Theta(n^3)$ time, expanding around each of the $2n + 1$ centers costs $\Theta(n^2)$ in the worst case, and [Manacher's algorithm](/manacher/) solves the problem in $\Theta(n)$ time. The problem is about substrings, which are contiguous; the [longest palindromic subsequence](/longest-palindromic-subsequence/), where gaps are allowed, is a different problem with a quadratic dynamic program.

## In plain words

You have a long line of letters and you want the longest unbroken stretch of it that reads the same from both ends. Every such stretch has a middle, either on a letter or between two letters. So you can stand at each middle point in turn and step outward on both sides while the two letters match. The longest walk you can make is the answer. That walk is slow when the line has many repeats, because you walk the same ground many times. Manacher's method remembers what it saw on the left side of a long palindrome and uses its mirror image on the right side, so it walks each part of the line a fixed number of times.

## Definition

**Input.** A string $s = s[0..n-1]$ of length $n \ge 0$ over an [alphabet](/alphabet/) $\Sigma$. Indices are 0-based, and $s[i..j]$ includes both ends. Algorithms may only test two symbols for equality, so $\Sigma$ has no order and may be of any size.

**Output.** A pair $(i, \ell)$ such that $s[i..i+\ell-1]$ is a palindrome and no palindromic substring of $s$ is longer than $\ell$. When several longest palindromes exist, any of them is a correct answer; the convention on this page is the leftmost one. For $n = 0$ the answer is the empty string, $\ell = 0$, and for $n \ge 1$ the answer has $\ell \ge 1$, because each single symbol is a palindrome.

**Odd and even palindromes.** Both are allowed. An odd palindrome has a middle symbol and an even one has its center between two symbols. Algorithms that work on centers treat the $n$ symbol centers and the $n + 1$ gap centers, or work on the string with a separator between the symbols, so that both kinds become odd (see [Manacher's algorithm](/manacher/)).

## Variants

- **All maximal palindromes.** For each of the $2n + 1$ centers, the length of the longest palindrome with that center. The longest palindromic substring is the maximum of this list. Manacher's algorithm computes the whole list in $O(n)$ time.
- **Online, for each prefix.** After each symbol, report the longest palindromic suffix, or the longest palindrome in the prefix so far. The [palindromic tree](/palindromic-tree/) does this in $O(1)$ amortized time per symbol for a constant-size alphabet.
- **Longest palindromic prefix.** The longest palindrome that starts at index 0. It is the key step of the [shortest palindrome](/shortest-palindrome/) problem.
- **On substrings.** For many query intervals $[i, j]$, the longest palindrome inside $s[i..j]$: see [palindrome substring queries](/palindrome-substring-queries/).
- **Approximate and gapped.** Palindromes with up to $k$ mismatches, or of the form $u\,g\,u^R$ with a gap $g$: see [gapped palindrome](/gapped-palindrome/). In DNA the symmetry is the reverse complement: see [reverse-complement palindrome](/reverse-complement-palindrome/).

## Examples

The table lists the leftmost longest palindromic substring.

| $s$ | $n$ | longest palindrome | $i$ | $\ell$ |
| --- | --- | --- | --- | --- |
| $\varepsilon$ | 0 | $\varepsilon$ | 0 | 0 |
| `abc` | 3 | `a` | 0 | 1 |
| `babad` | 5 | `bab` (also `aba`) | 0 | 3 |
| `cbbd` | 4 | `bb` | 1 | 2 |
| `abaab` | 5 | `baab` | 1 | 4 |
| `banana` | 6 | `anana` | 1 | 5 |
| `aaaa` | 4 | `aaaa` | 0 | 4 |
| `forgeeksskeegfor` | 16 | `geeksskeeg` | 3 | 10 |
| `abacdfgdcaba` | 12 | `aba` | 0 | 3 |

`abc` has no palindrome longer than 1. In `abaab` the longest palindrome is even and its center is between indices 2 and 3. The last row is a trap: the longest common substring of `abacdfgdcaba` and its reversal `abacdgfdcaba` is `abacd`, which is not a palindrome. A common substring of $s$ and $s^R$ is a palindrome of $s$ only if its two occurrences are mirror images of each other.

## Known algorithms

**Brute force, $\Theta(n^3)$.** Test each of the $n(n+1)/2$ nonempty substrings with the two-pointer scan of [palindrome recognition](/palindrome-recognition/) and keep the longest. It is the reference for testing the others.

**Interval table, $\Theta(n^2)$ time and space.** Let $\mathrm{pal}(i, j)$ be true if $s[i..j]$ is a palindrome. Then $\mathrm{pal}(i, i)$ is true, $\mathrm{pal}(i, i+1)$ is $s[i] = s[i+1]$, and $\mathrm{pal}(i, j) = (s[i] = s[j]) \wedge \mathrm{pal}(i+1, j-1)$ for $j \ge i + 2$. Fill the table by increasing length $j - i$. The table also answers [palindrome substring queries](/palindrome-substring-queries/) in $O(1)$, but Manacher's array does the same in $O(n)$ space.

**Expand around the center, $\Theta(n^2)$ time and $O(1)$ space.** The center $c \in \{0, 1, \ldots, 2n\}$ stands for the symbol $s[(c-1)/2]$ when $c$ is odd and for the gap before $s[c/2]$ when $c$ is even.

```pseudo id=expand
LONGEST-PALINDROME-EXPAND(s)            ▷ s[0 .. n − 1]
L1  best_i ← 0, best_ℓ ← 0
L2  for c ← 0 to 2n − 2 do
L3      i ← ⌊c/2⌋, j ← ⌈c/2⌉
L4      while i ≥ 0 and j < n and s[i] = s[j] do
L5          i ← i − 1, j ← j + 1
L6      if j − i − 1 > best_ℓ then best_i ← i + 1, best_ℓ ← j − i − 1
L7  return (best_i, best_ℓ)
```

The value $c$ is twice the center: for even $c$ the scan starts at the symbol $s[c/2]$ (odd palindromes), and for odd $c$ it starts at the gap between $s[(c-1)/2]$ and $s[(c+1)/2]$ (even palindromes). The two gaps at the ends of $s$ carry only the empty palindrome, so they are skipped. *Correctness.* The palindromes with one center are nested, so the loop of lines L4 and L5 stops at the maximal palindrome $s[i+1..j-1]$ of center $c/2$, and line L6 keeps the longest one. The comparison in line L6 is strict and $c$ grows, so ties go to the smaller center, which is the leftmost palindrome. *Cost.* On $a^n$ the loop makes $n(n+1)/2$ symbol comparisons in all, so the worst case is $\Theta(n^2)$; on a string of length $n \ge 2$ with no palindrome longer than 1, such as `abcabc`, it makes $3n - 3$.

**Manacher's algorithm, $\Theta(n)$.** [Manacher's algorithm](/manacher/) runs the same expansion, but it starts each center at the radius of its mirror center inside the rightmost palindrome found so far, so the right end of the scan only moves right. It computes all $2n + 1$ maximal palindromes in $O(n)$ time and $O(n)$ space with equality tests only. It is the standard solution.

**Suffix tree and extension queries, $\Theta(n)$.** The maximal palindrome at a center is the longest common extension of $s$ read to the right from the center and $s$ read to the left, that is, of a suffix of $s$ and a suffix of $s^R$. With a [suffix tree](/suffix-tree/) of $s\,\$\,s^R$ and [constant-time extension queries](/longest-common-extension-query/), each of the $2n - 1$ centers costs $O(1)$ (Gusfield, Section 9.2). The build is linear for a constant-size or integer alphabet.

**Hashing and binary search, $O(n \log n)$.** If $s[i..j]$ is a palindrome with $j - i \ge 2$, so is $s[i+1..j-1]$. So for each parity, the set of lengths of palindromes in $s$ is downward closed, and binary search on the length works, with a test "is there a palindrome of length $\ell$?" in $O(n)$ by [rolling hashes](/polynomial-rolling-hash/) of $s$ and $s^R$. The answer is correct with high probability. Binary search on the radius at each center gives the same bound.

**Palindromic tree, $\Theta(n)$.** The [palindromic tree](/palindromic-tree/) of $s$ has a node for each distinct palindrome, and the longest node is the answer. The build is $O(n)$ time for a constant-size alphabet, or $O(n \log \sigma)$ with sorted child maps.

**Faster on packed strings.** If $s$ is given packed, $\log n / \log \sigma$ symbols in one word of a [word RAM](/word-ram/), Charalampopoulos, Pissis and Radoszewski (2022) find a longest palindromic substring in $O(n \log \sigma / \log n)$ time, which is sublinear in $n$ for a small alphabet.

**History.** Manacher (1975) gave the linear-time online scan for the smallest initial palindrome of a string. Apostolico, Breslauer and Galil (1995) observed that the same scan finds the maximal palindromes at all centers, and so the longest palindromic substring, in linear time, and they gave parallel algorithms for the problem. Gusfield's 1997 book presents the suffix tree method. Charalampopoulos, Pissis and Radoszewski (2022) gave an algorithm that is sublinear on packed strings.

## Bounds

**Upper bound.** $O(n)$ time and $O(n)$ space with equality tests only, by Manacher's algorithm.

**Lower bound.** In the [comparison model](/comparison-model/) with $|\Sigma| \ge 2$, an algorithm needs at least $\lfloor n/2 \rfloor$ equality tests on $a^n$. *Proof.* From its answer one can tell whether $s$ is a palindrome: $s$ is a palindrome if and only if $\ell = n$. So the algorithm solves [palindrome recognition](/palindrome-recognition/), and the lower bound of that page applies to the same input. $\square$ So $\Theta(n)$ is the exact order of the problem in this model. On a word RAM with packed input the input occupies fewer than $n$ words, and the sublinear algorithm above shows that the comparison bound does not carry over to that model.

## Reductions

- **From palindrome recognition.** As in the lower bound: $s$ is a palindrome if and only if the answer has length $n$.
- **To all maximal palindromes.** The answer is the maximum over the $2n + 1$ centers of the maximal palindrome lengths, read off in $O(n)$ time.
- **To longest common extension.** $2n - 1$ extension queries between $s$ and $s^R$, as in the suffix tree method.
- **Not to the longest common substring of $s$ and $s^R$.** That reduction is wrong without a position check, as the example `abacdfgdcaba` shows. It becomes correct if each candidate common substring $s[i..j]$ must occur in $s^R$ at the mirror position $n - 1 - j$.

## Applications

- **A step of other palindrome problems.** The maximal palindromes give $O(1)$ [palindrome substring queries](/palindrome-substring-queries/), the longest palindromic prefix for the [shortest palindrome](/shortest-palindrome/), and the palindrome tests inside [palindrome partitioning](/palindrome-partitioning/).
- **Biology.** Long [reverse-complement palindromes](/reverse-complement-palindrome/) in DNA can fold into hairpins, and the same center-based algorithms find them after the equality test is replaced by a complement test.
- **Teaching.** The problem shows three standard levels of one task: brute force, a quadratic method that uses the structure, and a linear method that reuses work with an amortized argument.

## References
