---
tag: T7QYNA
kind: problem
slug: palindrome-partitioning
name: Palindrome partitioning
aliases:
- palindromic factorization
- palindromic decomposition
area: strings/palindromes
level: core
summary: Split a string into contiguous pieces that are all palindromes; list, count or minimise such splits.
model: comparison-model
complexity:
  vars: {n: the length of the string, P: the number of palindromic partitions}
  time: {worst: O(n^2 + n P)}
  space: {aux: O(n^2)}
prereqs: [palindrome, text-segmentation]
see_also: [palindrome-partition-backtracking, minimum-palindrome-partition, palindrome-partition-dp, series-links, palindromic-tree, manacher, enumeration-problem, catalan-numbers]
sources:
  - url: https://leetcode.com/problems/palindrome-partitioning/
    title: LeetCode, Problem 131, Palindrome Partitioning
    locator: the problem statement (return all partitions of s into palindromic substrings)
  - paper: doi:10.1016/j.jda.2014.08.001
    title: Gabriele Fici, Travis Gagie, Juha Kärkkäinen and Dominik Kempa, A subquadratic algorithm for minimum palindromic factorization, Journal of Discrete Algorithms 28 (2014), 41-48
    locator: the introduction (palindromic factorizations and earlier work) and the O(n log n) algorithm for a minimum factorization
  - paper: doi:10.1007/978-3-319-07566-2_16
    title: Tomohiro I, Shiho Sugimoto, Shunsuke Inenaga, Hideo Bannai and Masayuki Takeda, Computing palindromic factorizations and palindromic covers on-line, CPM 2014, Lecture Notes in Computer Science 8486, 150-161
    locator: the definitions of palindromic factorizations, the on-line O(n log n) algorithm, and the palindromic cover
  - paper: doi:10.4230/LIPIcs.CPM.2017.23
    title: Kirill Borozdin, Dmitry Kosolobov, Mikhail Rubinchik and Arseny M. Shur, Palindromic length in linear time, CPM 2017, LIPIcs 78, 23:1-23:12
    locator: the definition of palindromic length and the linear-time on-line algorithm
  - paper: doi:10.4230/LIPIcs.MFCS.2020.81
    title: Mikhail Rubinchik and Arseny M. Shur, Palindromic k-factorization in pure linear time, MFCS 2020, LIPIcs 170, paper 81
    locator: the main theorem (online decision of whether a string is a concatenation of k palindromes in linear time)
  - paper: arxiv:1703.08931
    title: Michał Adamczyk, Mai Alzamel, Panagiotis Charalampopoulos, Costas S. Iliopoulos and Jakub Radoszewski, Palindromic decompositions with gaps and errors, CSR 2017
    locator: the abstract and Section 1 (decompositions with gaps, with errors, and with a minimum length of the palindromes)
---

Palindrome partitioning splits a string into contiguous pieces, each of which is a [palindrome](/palindrome/). A string of length $n \ge 1$ always has at least one such split, into single symbols, and can have up to $2^{n-1}$ of them. Three tasks share the name: list all partitions, count them, or find one with the fewest pieces, the [minimum palindrome partition](/minimum-palindrome-partition/). Listing is done by [backtracking](/palindrome-partition-backtracking/), and counting and minimizing by a [dynamic program](/palindrome-partition-dp/) over prefixes, in $O(n^2)$ time, or in $O(n \log n)$ time with [series links](/series-links/).

## In plain words

Take a word and draw cuts between some of its letters. Each piece between two cuts must read the same from both ends. Single letters always do, so cutting between every pair of letters always works. Often there are other ways, with longer pieces. You may want to see all ways, to know how many there are, or to use as few pieces as you can. All three questions start from the same fact: the first piece is a palindrome that starts at the first letter, and what is left must be cut in the same way.

## Definition

**Input.** A string $s = s[0..n-1]$ over an [alphabet](/alphabet/) $\Sigma$, with 0-based indices. Algorithms test symbols for equality only.

**Palindromic partition.** A sequence of cut positions $0 = c_0 < c_1 < \cdots < c_k = n$ such that each piece $s[c_{t-1}..c_t - 1]$, for $1 \le t \le k$, is a nonempty palindrome. The pieces may be odd or even palindromes. The empty string has exactly one partition, with $k = 0$ pieces.

**Tasks.**

- **Enumeration.** Output every palindromic partition of $s$, each one time. This is an [enumeration problem](/enumeration-problem/); the cost is measured in $n$ and the output size.
- **Counting.** Output the number $P(s)$ of palindromic partitions.
- **Minimization.** Output the least number of pieces, the *palindromic length* $\mathrm{PL}(s)$, and one partition that reaches it. This task has its own page, [minimum palindrome partition](/minimum-palindrome-partition/).

All three rest on one recurrence over the end of the first piece, or equally over the start of the last piece. Let $C(i)$ be the set of $j < i$ such that $s[j..i-1]$ is a palindrome. Then the partitions of the prefix $s[0..i-1]$ are the partitions of some $s[0..j-1]$ with $j \in C(i)$, followed by the piece $s[j..i-1]$.

## Variants

- **Partitions into $k$ pieces.** Decide whether $s$ is a concatenation of exactly $k$ nonempty palindromes. Rubinchik and Shur (2020) decide this online in $O(n)$ time on a word RAM.
- **Maximal palindromes only.** Split $s$ into pieces that are maximal palindromes, or cover $s$ with as few maximal palindromes as possible. I, Sugimoto, Inenaga, Bannai and Takeda (2014) compute a smallest palindromic cover in $O(n)$ time.
- **Restricted pieces.** Only even palindromes, only palindromes of length at least $\ell$, or pieces with gaps and errors, as in the work of Adamczyk, Alzamel, Charalampopoulos, Iliopoulos and Radoszewski.
- **Online.** Report $\mathrm{PL}$ or $P$ for each prefix after each new symbol. The series-link method is online, and Borozdin, Kosolobov, Rubinchik and Shur (2017) compute the palindromic length of each prefix online in linear total time.
- **Word segmentation.** Partitioning into palindromes is the case of [text segmentation](/text-segmentation/) where the dictionary is the set of all palindromes.

## Examples

| $s$ | partitions | $P(s)$ | $\mathrm{PL}(s)$ |
| --- | --- | --- | --- |
| $\varepsilon$ | the empty partition | 1 | 0 |
| `abc` | a, b, c | 1 | 3 |
| `aab` | a, a, b; aa, b | 2 | 2 |
| `abaab` | a, b, a, a, b; a, b, aa, b; a, baab; aba, a, b | 4 | 2 |
| `banana` | b, a, n, a, n, a; b, a, n, ana; b, a, nan, a; b, ana, n, a; b, anana | 5 | 2 |
| `aaaa` | each of the $2^3$ ways to cut | 8 | 1 |
| `racecar` | four partitions, one of them the whole string | 4 | 1 |

`abc` has only the trivial partition, because it has no palindrome longer than 1. For $a^n$ every set of cuts works, so $P(a^n) = 2^{n-1}$ for $n \ge 1$.

## Known algorithms

**Palindrome table.** Precompute which substrings are palindromes: with the interval recurrence $\mathrm{pal}(i, j) = (s[i] = s[j]) \wedge \mathrm{pal}(i+1, j-1)$ in $O(n^2)$ time and space, or with [Manacher's algorithm](/manacher/) in $O(n)$ time, which answers each test in $O(1)$. For each start $i$, list the ends $j$ with $s[i..j]$ a palindrome; the lists have $N_{\mathrm{occ}}(s) \le n(n+1)/2$ entries in all.

**Enumeration by backtracking, $O(n^2 + nP)$.** Extend a partial partition by each palindrome that starts at the current position, from the lists above, and output a partition when the position reaches $n$. Each branch of the search ends in a full partition, so there is no dead end, and the work per output is $O(n)$. The page [palindrome partition backtracking](/palindrome-partition-backtracking/) gives the algorithm with an explicit stack and its proof.

**Counting by dynamic programming, $O(n^2)$.** $P_0 = 1$ and $P_i = \sum_{j \in C(i)} P_j$ for $1 \le i \le n$, so $P(s) = P_n$. The sum over $C(i)$ is over the palindromic suffixes of $s[0..i-1]$, and there can be $\Theta(n)$ of them, which gives $O(n^2)$ time.

**Minimum by dynamic programming, $O(n^2)$.** The same recurrence with $\min$ and $+1$ in place of the sum: see [palindrome partition dynamic programming](/palindrome-partition-dp/).

**Series links, $O(n \log n)$.** The palindromic suffixes of each prefix form $O(\log n)$ arithmetic progressions of lengths. With the [palindromic tree](/palindromic-tree/) and [series links](/series-links/), the sum or the minimum over a whole progression is reused from an earlier position, so each prefix costs $O(\log n)$. This gives both $P(s)$ and $\mathrm{PL}(s)$ in $O(n \log n)$ time and $O(n)$ space (Fici, Gagie, Kärkkäinen and Kempa 2014; I, Sugimoto, Inenaga, Bannai and Takeda 2014). For the minimum, Borozdin et al. (2017) reach linear time.

## Bounds

- **Number of partitions.** $1 \le P(s) \le 2^{n-1}$ for $n \ge 1$. The upper bound counts all sets of cuts. It is reached only by $a^n$: if every set of cuts is valid, then the cut set that leaves the piece $s[i..i+1]$ and cuts everywhere else is valid, so $s[i] = s[i+1]$ for each $i$. The lower bound is reached exactly by the strings with no palindrome of length 2 or 3, such as `abcabc` $\cdots$, because each longer palindrome has one of length 2 or 3 at its center.
- **Enumeration time.** Any algorithm that writes each partition out in full needs $\Omega(nP)$ time on $a^n$, since each partition there covers $n$ symbols. The backtracking bound $O(n^2 + nP)$ matches this up to the additive $O(n^2)$ for the palindrome table.
- **Counting and minimization.** $O(n \log n)$ for counting and $O(n)$ for the minimum, both online. In the comparison model, $\lfloor n/2 \rfloor$ tests are needed on $a^n$, since $\mathrm{PL}(s) = 1$ if and only if $s$ is a palindrome.

## Reductions

- **From palindrome recognition.** $s$ is a palindrome if and only if $\mathrm{PL}(s) = 1$.
- **To palindromic suffixes.** All three tasks need, at each prefix, the set of its palindromic suffixes, which the [palindromic tree](/palindromic-tree/) provides.
- **To shortest paths.** The minimum partition is a shortest path from 0 to $n$ in the [DAG](/dag-dynamic-programming/) on the positions $0, \ldots, n$ with an edge $j \to i$ for each palindrome $s[j..i-1]$; the count is the number of paths.

## Applications

- **Combinatorics on words.** The palindromic length of words, and of the prefixes of infinite words, is a studied measure; the factorization algorithms above compute it.
- **Biology.** Decompositions of DNA into palindromes with gaps and errors model hairpin structures.
- **Programming tasks.** Listing and minimizing palindromic partitions are standard exercises for backtracking and for dynamic programming over prefixes.

## References
