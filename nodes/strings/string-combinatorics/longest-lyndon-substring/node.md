---
tag: 9R4DF2
kind: problem
slug: longest-lyndon-substring
name: Longest Lyndon substring
aliases:
- longest Lyndon subword
area: strings/string-combinatorics
level: advanced
summary: Find the longest substring of a string that is a Lyndon word.
prereqs: [lyndon-word, lyndon-factorization]
see_also: [duval-algorithm, lyndon-schutzenberger-theorem, lyndon-array, minimal-rotation, runs-theorem, lexicographic-order, longest-palindromic-substring, longest-repeated-substring]
sources:
  - url: "https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CPM.2018.19"
    title: Yuki Urabe, Yuto Nakashima, Shunsuke Inenaga, Hideo Bannai and Masayuki Takeda, Longest Lyndon substring after edit, 29th Annual Symposium on Combinatorial Pattern Matching (CPM 2018), LIPIcs 105, 19:1-19:10
    locator: the definition of LLS(T), its computation from the Lyndon factorization, and the O(log n) time answer after a single character edit with O(n) preprocessing
  - paper: doi:10.1016/0196-6774(83)90017-2
    title: Jean-Pierre Duval, Factorizing words over an ordered alphabet, Journal of Algorithms 4(4), 1983, 363-381
    locator: the linear-time computation of the Lyndon factorization over an ordered alphabet
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 5, Lyndon words (D. Perrin), Section 5.1, the factorization theorem and the first factor as the longest Lyndon prefix
  - paper: doi:10.1007/s00453-023-01125-z
    title: Hideo Bannai, Tomohiro I, Tomasz Kociumaka, Dominik Köppl and Simon J. Puglisi, Computing longest Lyndon subsequences and longest common Lyndon subsequences, Algorithmica 86(3), 2024, 735-756
    locator: the longest Lyndon subsequence in O(n^3) time and O(n) space, and the longest common Lyndon subsequence of two strings
  - paper: doi:10.3390/a13110294
    title: Frantisek Franek and Michael Liut, Computing maximal Lyndon substrings of a string, Algorithms 13(11), 2020, 294
    locator: the right-maximal Lyndon substrings, the Lyndon array, and algorithms to compute them
---

The longest Lyndon substring problem asks for a longest factor of a string that is a [Lyndon word](/lyndon-word/), a word strictly smaller than all its proper rotations. The answer can be read off the [Lyndon factorization](/lyndon-factorization/): the longest Lyndon substrings are exactly the longest factors of that factorization. So [Duval's algorithm](/duval-algorithm/) solves the problem in $O(n)$ time and $O(1)$ extra space over any ordered alphabet.

## In plain words

Order words as in a dictionary. A Lyndon word is one that comes strictly before every word obtained by cutting it in two and swapping the halves, such as "aab" or "abac". Given a text, we want its longest stretch of consecutive letters that has this property. Every text splits in a unique way into Lyndon pieces that never increase from left to right, and the answer is simply the longest of those pieces. A single left to right pass that finds the pieces therefore also finds the answer.

## Definition

Let $\Sigma$ be a totally ordered [alphabet](/alphabet/); only comparisons of letters are used. Indices are 0-based, and $s = s[0..n-1]$ with $n \ge 1$. Words are compared in [lexicographic order](/lexicographic-order/), and a word $u \ne \varepsilon$ is a Lyndon word if $u < v$ for each proper nonempty suffix $v$ of $u$.

**Input.** A string $s \in \Sigma^n$.

**Output.** A pair $(i, j)$ with $0 \le i < j \le n$ such that $s[i..j-1]$ is a Lyndon word and $j - i$ is as large as possible. The length $j - i$ is written $\mathrm{LLS}(s)$.

Each single letter is a Lyndon word, so $\mathrm{LLS}(s) \ge 1$.

## Variants

- **All longest occurrences.** List every pair $(i, j)$ that attains $\mathrm{LLS}(s)$.
- **Longest Lyndon substring starting at each position.** For each $i$, the length $\lambda[i]$ of the longest Lyndon word that starts at $i$. This is the [Lyndon array](/lyndon-array/), and $\mathrm{LLS}(s) = \max_i \lambda[i]$.
- **After an edit.** Preprocess $s$, then answer $\mathrm{LLS}(s')$ for a string $s'$ obtained from $s$ by changing, inserting or deleting one letter, or by replacing a block.
- **Longest Lyndon subsequence.** Letters need not be consecutive. This is a different and harder problem, solved in $O(n^3)$ time by Bannai, I, Kociumaka, Köppl and Puglisi.
- **Other orders.** The answer depends on the order of $\Sigma$. The [runs theorem](/runs-theorem/) uses Lyndon words for an order and for its reverse together.

## Examples

Over $a < b < c < d$, and for `mississippi` over the usual order of letters $i < m < p < s$:

| $s$ | Lyndon factorization | Longest Lyndon substrings | $\mathrm{LLS}$ |
|---|---|---|---|
| `banana` | `b` $\cdot$ `an` $\cdot$ `an` $\cdot$ `a` | `an` at the indices 1 and 3 | 2 |
| `mississippi` | `m` $\cdot$ `iss` $\cdot$ `iss` $\cdot$ `ipp` $\cdot$ `i` | `iss` at 1 and 4, `ipp` at 7 | 3 |
| `abcabacab` | `abc` $\cdot$ `abac` $\cdot$ `ab` | `abac` at 3 | 4 |
| `bbababaab` | `b` $\cdot$ `b` $\cdot$ `ab` $\cdot$ `ab` $\cdot$ `aab` | `aab` at 6 | 3 |
| `dbcabcab` | `d` $\cdot$ `bc` $\cdot$ `abc` $\cdot$ `ab` | `abc` at 3 | 3 |
| `aabab` | `aabab` | the whole string | 5 |
| `cba` | `c` $\cdot$ `b` $\cdot$ `a` | each letter | 1 |

In `abcabacab`, the factor `bcab` is not Lyndon, since its suffix `ab` is smaller, and no factor of length 5 is Lyndon; `abac` is the answer. In `cba`, every factor of length 2 starts with a larger letter than it ends with, so only single letters are Lyndon.

## Known algorithms

- **Brute force.** Test each of the $n(n+1)/2$ factors for the Lyndon property in linear time, for $O(n^3)$ time; testing all factors that start at $i$ together, by the Lyndon factorization of $s[i..n-1]$, gives $O(n^2)$.
- **From the Lyndon factorization.** Let $s = \ell_1 \ell_2 \cdots \ell_k$ with Lyndon words $\ell_1 \ge \cdots \ge \ell_k$. Then $\mathrm{LLS}(s) = \max_t |\ell_t|$, and the longest Lyndon substrings are exactly the factors $\ell_t$ of maximal length. *Proof.* Fix $i$, and let $\ell_t$ be the factor that contains the index $i$, so that $s[i..n-1] = x\,\ell_{t+1} \cdots \ell_k$, where $x$ is a nonempty suffix of $\ell_t$. Let $x = x_1 \cdots x_r$ be the Lyndon factorization of $x$. Its last factor $x_r$ is a nonempty suffix of the Lyndon word $\ell_t$, so $x_r \ge \ell_t \ge \ell_{t+1}$. So $x_1, \ldots, x_r, \ell_{t+1}, \ldots, \ell_k$ is a nonincreasing factorization of $s[i..n-1]$ into Lyndon words, and by the uniqueness in the [Chen-Fox-Lyndon theorem](/lyndon-schutzenberger-theorem/) it is the Lyndon factorization. The first factor of a Lyndon factorization is the longest Lyndon prefix, so the longest Lyndon word that starts at $i$ is $x_1$. It has length at most $|x| \le |\ell_t|$, with equality only if $x_1 = x = \ell_t$, that is, only if $i$ is the start of $\ell_t$. $\square$ [Duval's algorithm](/duval-algorithm/) finds the factorization, and therefore the answer, in $O(n)$ time with $O(1)$ extra space, using at most $2n - 1$ letter comparisons.
- **From the Lyndon array.** The [Lyndon array](/lyndon-array/) $\lambda$ can be built in $O(n)$ time from the inverse suffix array and next-smaller values, or over a general ordered alphabet by the method of Ellert and Fischer; its maximum is $\mathrm{LLS}(s)$. This is more work than Duval's algorithm, but it also gives the answer for every suffix $s[i..n-1]$.
- **After an edit.** Urabe, Nakashima, Inenaga, Bannai and Takeda (2018) answer $\mathrm{LLS}(s')$ for a single character edit in $O(\log n)$ time after $O(n)$ preprocessing, and for the replacement of a block by a string of length $l$ in $O(l \log \sigma + \log n)$ time.

## Bounds

- **Range.** $1 \le \mathrm{LLS}(s) \le n$. The upper bound holds exactly when $s$ is a Lyndon word. The lower bound holds exactly when $s[0] \ge s[1] \ge \cdots \ge s[n-1]$: if $s[i] < s[i+1]$ for some $i$, then $s[i]s[i+1]$ is a Lyndon word of length 2, and otherwise every factor of length at least 2 has a first letter at least its last letter and is not Lyndon, since a Lyndon word of length at least 2 is smaller than its last letter.
- **Time.** $\Theta(n)$. An algorithm that skips the letter $s[i]$ of a nonincreasing string cannot tell it from the string with $s[i]$ replaced by a larger letter, which may create a factor of length 2 that is Lyndon. Duval's algorithm meets the bound with $O(1)$ extra space, over a general ordered alphabet.
- **Number of answers.** The longest Lyndon substrings are factors of the Lyndon factorization, so there are at most $n / \mathrm{LLS}(s)$ of them, and they do not overlap.

## Reductions

- **To the Lyndon factorization,** as shown above, in $O(n)$ extra time.
- **From the minimal rotation.** For a [primitive word](/primitive-word/) $w$ of length $m$, $\mathrm{LLS}(ww) = m$, and the longest Lyndon substrings of $ww$ are the occurrences of the least rotation of $w$. *Proof.* A factor of $ww$ has the period $m$, and a Lyndon word has no period smaller than its length, since it is unbordered; so no Lyndon factor is longer than $m$. A Lyndon factor of length $m$ is a rotation of $w$ that is Lyndon, and the least rotation of a primitive word is its unique Lyndon rotation, which occurs in $ww$. $\square$ So the [minimal rotation](/minimal-rotation/) problem for primitive words reduces to the longest Lyndon substring of a string of length $2m$.
- **To the Lyndon array.** $\mathrm{LLS}(s)$ is the maximum of the Lyndon array.

## Applications

- **Runs and repetitions.** In the Lyndon-based proof of the [runs theorem](/runs-theorem/), each run gets a Lyndon root that is the longest Lyndon word starting at its position, for one of two opposite orders; these are the entries of the Lyndon array, whose maximum is $\mathrm{LLS}$.
- **Bijective transforms and sorting.** The factors of the Lyndon factorization, and the longest one in particular, are the blocks of the bijective Burrows-Wheeler transform and of suffix sorting algorithms that start from Lyndon factors.

## References
