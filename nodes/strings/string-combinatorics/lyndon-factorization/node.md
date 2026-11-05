---
tag: ZAAVT6
kind: problem
slug: lyndon-factorization
name: Lyndon factorization
aliases:
- Lyndon decomposition
area: strings/string-combinatorics
level: core
summary: Factor a word into a nonincreasing sequence of Lyndon words.
prereqs: [lyndon-schutzenberger-theorem, lyndon-word]
see_also: [duval-algorithm, lyndon-array, longest-lyndon-substring, minimal-rotation, suffix-array, bijective-burrows-wheeler-transform, lyndon-based-runs-computation, witt-formula]
sources:
  - paper: doi:10.1016/0196-6774(83)90017-2
    title: Jean-Pierre Duval, Factorizing words over an ordered alphabet, Journal of Algorithms 4(4), 1983, 363-381
    locator: the problem, the linear-time algorithm with constant extra space, and the least conjugate
  - paper: doi:10.2307/1970044
    title: Kuo-Tsai Chen, Ralph H. Fox and Roger C. Lyndon, Free differential calculus IV. The quotient groups of the lower central series, Annals of Mathematics 68(1), 1958, 81-95
    locator: the existence and uniqueness of the factorization
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 5, Lyndon words (D. Perrin), Section 5.1
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1, Generating all n-tuples (prime strings and factorization into primes)
  - paper: doi:10.1137/15M1011032
    title: Hideo Bannai, Tomohiro I, Shunsuke Inenaga, Yuto Nakashima, Masayuki Takeda and Kazuya Tsuruta, The "Runs" Theorem, SIAM Journal on Computing 46(5), 2017, 1501-1514
    locator: the Lyndon roots of runs and the computation of the longest Lyndon word at each index for two orders
---

The Lyndon factorization problem asks for the unique way to cut a word $s$ into [Lyndon words](/lyndon-word/) $\ell_1, \ell_2, \ldots, \ell_k$ with $\ell_1 \ge \ell_2 \ge \cdots \ge \ell_k$ in lexicographic order, as in `banana` $=$ `b` $\cdot$ `an` $\cdot$ `an` $\cdot$ `a`. The factorization exists and is unique by the [Chen-Fox-Lyndon theorem](/lyndon-schutzenberger-theorem/). [Duval's algorithm](/duval-algorithm/) computes it in linear time with constant extra space, and the factorization gives the least suffix, a least rotation, the bijective Burrows-Wheeler transform and a starting point for the computation of runs.

## In plain words

A Lyndon word is a word that comes strictly first in dictionary order among all its rotations, such as `aab` or `abac`. Any word can be cut into Lyndon words that never get larger from left to right, and there is only one way to do it. The task is to find the cut points. The last piece is always the smallest ending of the word, and the first piece is the longest beginning that is a Lyndon word. A simple scan from left to right finds all the cuts in time proportional to the length of the word.

## Definition

**Input.** A word $s = s[0..n-1]$ over a totally ordered [alphabet](/alphabet/), with $n \ge 0$. Only comparisons of letters are needed. Indices are 0-based. Words are compared in [lexicographic order](/lexicographic-order/), where a proper prefix is smaller.

**Output.** The start indices $0 = b_1 < b_2 < \cdots < b_k < n$ such that, with $b_{k+1} = n$, each factor $\ell_r = s[b_r..b_{r+1}-1]$ is a Lyndon word and $\ell_1 \ge \ell_2 \ge \cdots \ge \ell_k$. For $n = 0$ the output is empty. An equivalent output is the list of factors, or the grouped form $s = m_1^{e_1} \cdots m_t^{e_t}$ with $m_1 > \cdots > m_t$.

**Characterizations.** For $n \ge 1$ the output is determined by each of these rules, proved on the [theorem](/lyndon-schutzenberger-theorem/) page and on the [Duval's algorithm](/duval-algorithm/) page:

1. $\ell_1$ is the longest prefix of $s$ that is a Lyndon word, and $\ell_2 \cdots \ell_k$ is the factorization of the rest.
2. $\ell_k$ is the lexicographically least nonempty suffix of $s$.
3. The start indices are the indices $i$ whose suffix $s[i..n-1]$ is smaller than every suffix $s[j..n-1]$ with $j < i$, that is, the left-to-right minima of the inverse [suffix array](/suffix-array/).

*Proof of 3.* First, an index $i$ inside a factor $\ell_r$, after its start, is not a minimum. Write $s[i..] = \ell_r' \ell_{r+1} \cdots \ell_k$ with $\ell_r'$ a proper suffix of $\ell_r$. Then $\ell_r' > \ell_r$, and $\ell_r'$ is not a prefix of $\ell_r$, so the two first differ inside $\ell_r'$ with the larger letter in $\ell_r'$; hence $s[i..] > s[b_r..]$ with $b_r < i$. Next, let $C(r)$ say that $s[j..] > s[b_r..]$ for every $j < b_r$; we prove $C(r)$ for $r = k + 1, k, \ldots, 1$, with $b_{k+1} = n$. $C(k+1)$ holds because every nonempty suffix is larger than the empty one. Assume $C(r+1)$ and let $j < b_r$. The prefix $P = \ell_1 \cdots \ell_r$ has the factorization $\ell_1, \ldots, \ell_r$, so by characterization 2 its least suffix is $\ell_r$, and $y = s[j..b_{r+1}-1]$ satisfies $y > \ell_r$. If $\ell_r$ is not a prefix of $y$, then $y$ is not a proper prefix of $\ell_r$ either (it would be smaller), so $y$ and $\ell_r$ first differ inside both, and $s[j..] > s[b_r..]$. If $y = \ell_r y'$ with $y'$ nonempty, then $s[j..] = \ell_r\,s[j'..]$ and $s[b_r..] = \ell_r\,s[b_{r+1}..]$ with $j' = j + |\ell_r| < b_{r+1}$, and $C(r+1)$ gives $s[j'..] > s[b_{r+1}..]$. So $C(r)$ holds, and each start $b_r$ is a left-to-right minimum. $\square$

## Variants

- **Least suffix.** Output only $\ell_k$, the least nonempty suffix. Duval's algorithm finds it in linear time and constant space.
- **Least rotation.** A least rotation of $s$ starts at the start of the last Lyndon factor of $ss$ that begins below $|s|$; this is the [minimal rotation](/minimal-rotation/) problem.
- **All suffixes: the Lyndon array.** For each index $i$, the length of the longest Lyndon word that starts at $i$ is the length of the first factor of the factorization of $s[i..n-1]$. The array of these lengths is the [Lyndon array](/lyndon-array/), computable in linear time on an integer alphabet.
- **Both orders.** The factorizations for an order and for its reverse are used together in the computation of runs, because each run has a Lyndon root for one of the two orders; see [Lyndon-based runs computation](/lyndon-based-runs-computation/).
- **Longest Lyndon factor.** The longest Lyndon factor of $s$ is a longest factor of the factorization; see [longest Lyndon substring](/longest-lyndon-substring/).

## Examples

All 16 binary words of length 4, with $a < b$:

| $s$ | factorization | $s$ | factorization |
|---|---|---|---|
| `aaaa` | `a` $\cdot$ `a` $\cdot$ `a` $\cdot$ `a` | `baaa` | `b` $\cdot$ `a` $\cdot$ `a` $\cdot$ `a` |
| `aaab` | `aaab` | `baab` | `b` $\cdot$ `aab` |
| `aaba` | `aab` $\cdot$ `a` | `baba` | `b` $\cdot$ `ab` $\cdot$ `a` |
| `aabb` | `aabb` | `babb` | `b` $\cdot$ `abb` |
| `abaa` | `ab` $\cdot$ `a` $\cdot$ `a` | `bbaa` | `b` $\cdot$ `b` $\cdot$ `a` $\cdot$ `a` |
| `abab` | `ab` $\cdot$ `ab` | `bbab` | `b` $\cdot$ `b` $\cdot$ `ab` |
| `abba` | `abb` $\cdot$ `a` | `bbba` | `b` $\cdot$ `b` $\cdot$ `b` $\cdot$ `a` |
| `abbb` | `abbb` | `bbbb` | `b` $\cdot$ `b` $\cdot$ `b` $\cdot$ `b` |

The three words with one factor, `aaab`, `aabb` and `abbb`, are the binary Lyndon words of length 4. The five words with four factors are the nonincreasing words $b^i a^{4-i}$. Over three letters, `abcabacab` $=$ `abc` $\cdot$ `abac` $\cdot$ `ab`, and the suffix `ab` is its least suffix.

**The suffix array view.** For $s = $ `banana`, the suffixes in sorted order start at 5, 3, 1, 0, 4, 2, so the inverse suffix array is $[3, 2, 5, 1, 4, 0]$. Its left-to-right minima are at the indices 0, 1, 3 and 5, the starts of `b`, `an`, `an` and `a`.

**The number of factors.** A word of length $n$ has between 1 and $n$ factors. It has $n$ factors exactly when its letters are nonincreasing. For a uniformly random word, the mean number of factors is $\sum_{N=1}^{n} c(N)\,\sigma^{-N}$, where $c(N) = \sum_{m \mid N} L_\sigma(m)$ and $L_\sigma(m)$ is the number of Lyndon words of length $m$. *Proof.* Mark each factor by a variable $u$; the theorem gives $\prod_m (1 - u z^m)^{-L_\sigma(m)}$ as the generating function of words by length and number of factors. Differentiate at $u = 1$: the total number of factors over $\Sigma^n$ is $[z^n]\,\frac{1}{1 - \sigma z} \sum_m L_\sigma(m) \frac{z^m}{1 - z^m} = \sum_{N \le n} c(N)\,\sigma^{n-N}$. $\square$ Since $N L_\sigma(N) = \sigma^N - O(\sigma^{N/2})$ by the [Witt formula](/witt-formula/), the mean is $\ln n + O(1)$. The exact means are $21/8$ for binary words of length 4, $217/64$ for length 8, $32279/8192 \approx 3.94$ for length 14, and $64/27$ for ternary words of length 4.

## Known algorithms

| algorithm | time | extra space | idea |
|---|---|---|---|
| greedy with a Lyndon test | $O(n^3)$ | $O(1)$ | repeat: take the longest Lyndon prefix (characterization 1), testing each candidate prefix in linear time |
| merging | $O(n^2)$ | $O(n)$ | start from the letters; each pass compares all adjacent factors in $O(n)$ time and merges a pair $\ell_i < \ell_{i+1}$, as in the existence proof |
| [Duval's algorithm](/duval-algorithm/) | $\Theta(n)$ | $O(1)$ | keep a prefix of a power of a Lyndon word; at most $2n - 1$ comparisons |
| [suffix array](/suffix-array/) | $O(n)$ on an integer alphabet | $O(n)$ | left-to-right minima of the inverse suffix array (characterization 3) |

Duval's algorithm is the standard choice. The suffix array route is useful when the suffix array is built anyway, and it extends to the [Lyndon array](/lyndon-array/).

## Bounds

- **Time.** $\Theta(n)$. The upper bound is Duval's algorithm. For the lower bound, every correct algorithm must read every letter: in $a^n$ over $\{a, b\}$, changing the letter at an index $i \ge 1$ to $b$ gives $a^i b a^{n-i-1}$, whose first factor $a^i b$ is longer than `a`.
- **Comparisons.** At most $2n - 1$ three-way letter comparisons by Duval's algorithm, and at least $n - 1$ for any algorithm on $a^n$, by the argument above.
- **Space.** $O(1)$ extra cells besides the input and the output, by Duval's algorithm.
- **Output size.** Between 1 and $n$ factors; the mean is $\ln n + O(1)$ over uniform random words, as shown in the examples.

## Reductions

- **To suffix sorting.** By characterization 3, the factorization is read from the inverse suffix array in $O(n)$ time. So any suffix sorting method solves the problem.
- **Least suffix and least rotation.** The least suffix is the last factor, and a least rotation of $s$ comes from the factorization of $ss$. So both problems reduce to this one in linear time.
- **Counting.** The theorem behind the problem is a bijection between words and multisets of Lyndon words. Over an alphabet of $q$ letters, $q$ a prime power, the Lyndon words of length $m$ are as many as the monic irreducible polynomials of degree $m$ over $\mathbb{F}_q$, so the number of factors of a random word has the same distribution as the number of irreducible factors, with multiplicity, of a random monic polynomial of degree $n$.

## Applications

- **Canonical forms of cyclic words.** The least rotation, through the factorization of $ss$, gives a canonical representative of a [necklace](/necklace/).
- **[Bijective Burrows-Wheeler transform](/bijective-burrows-wheeler-transform/).** It factors the text into Lyndon words and sorts the rotations of all factors together, which makes the transform a bijection without an end marker.
- **Runs and repetitions.** The longest Lyndon word starting at each index, for both orders, gives the Lyndon roots of all runs; see [Lyndon-based runs computation](/lyndon-based-runs-computation/).
- **String matching.** The maximal suffix computation, a variant of the same scan, gives a [critical factorization](/critical-factorization/) for [two-way string matching](/two-way-string-matching/).
- **Algebra.** The Lyndon words index a basis of the free Lie algebra, and the factorization expresses each word in the corresponding basis of the free associative algebra; this was the original motivation of Chen, Fox and Lyndon.

## References
