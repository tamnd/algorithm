---
tag: 8NYTX3
kind: problem
slug: substring-equality-queries
name: Substring equality queries
aliases:
- substring comparison queries
- are two substrings equal
area: strings/string-hashing
level: core
summary: Preprocess a string so that the question whether two of its substrings are equal can be answered in constant time.
model: word-ram
complexity:
  vars: {n: the length of the string, ℓ: the length of the compared substrings}
  time: {build: O(n), query: O(1)}
  space: {extra: O(n)}
prereqs: [polynomial-rolling-hash, polynomial-hash-collision-bound]
see_also: [longest-common-extension-query, lcp-array, suffix-array, dynamic-polynomial-hashing, string-equality-testing, rabin-karp, string-period, palindrome]
sources:
  - url: https://ioinformatics.org/journal/INFOL119.pdf
    title: Jakub Pachocki and Jakub Radoszewski, Where to use and how not to use polynomial string hashing, Olympiads in Informatics 7 (2013), 90-100
    locator: Section 2 (prefix hashes and the hash of a substring in constant time) and Section 3 (problems solved by comparing substrings)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 9.1, The longest common extension problem (constant-time answers with a suffix tree and lowest common ancestors)
  - paper: doi:10.1145/800152.804905
    title: Richard M. Karp, Raymond E. Miller and Arnold L. Rosenberg, Rapid identification of repeated patterns in strings, trees and arrays, Proceedings of the 4th ACM Symposium on Theory of Computing (1972), 125-136
    locator: the naming of all substrings whose length is a power of two, by doubling
---

Substring equality queries ask, for a fixed string $T$ of length $n$, whether $T[i \ldots i+\ell-1] = T[j \ldots j+\ell-1]$ for many triples $(i, j, \ell)$. Without preprocessing a query costs $O(\ell)$ character comparisons. With [prefix hashes](/polynomial-rolling-hash/) it costs $O(1)$ after $O(n)$ preprocessing, and the answer "equal" is wrong with probability at most $(\ell - 1)/p$ for a random base modulo a prime $p$. A [suffix array](/suffix-array/) with an [LCP array](/lcp-array/) and range minimum queries gives the same bounds with no error. The problem is the basic step of many string algorithms that compare substrings by binary search.

## In plain words

You have one long string and many questions of the form: is the piece that starts here the same as the piece of the same length that starts there? Comparing letter by letter takes as long as the pieces are long.

A faster way is to do some work on the string once, at the start. After that work, each question takes a fixed small number of steps. One way stores a running number for each start of the string; the number of any piece then comes from two stored numbers. Equal pieces always give equal numbers, and different pieces almost never do. A second way sorts all the ends of the string and stores how much neighbors agree. It never makes an error, but it is longer to write.

## Definition

**Input.** A string $T = T[0 \ldots n-1]$ over an alphabet $\Sigma$. Indices are 0-based. Characters have integer codes in $\{1, \ldots, \sigma\}$ (the integer alphabet model); the hashing solution needs only $\sigma < p$, and the suffix array solution needs $\sigma \le n^{O(1)}$ for linear preprocessing.

**Query.** A triple $(i, j, \ell)$ with $0 \le i, j$ and $i + \ell \le n$, $j + \ell \le n$. The answer is yes if $T[i + t] = T[j + t]$ for all $0 \le t < \ell$, and no otherwise. For $\ell = 0$ the answer is yes. The two substrings may overlap; for example $(0, 1, n - 1)$ asks whether $T$ has period 1.

**Goal.** Preprocess $T$ in time $P(n)$ and space $S(n)$, then answer each query in time $Q(n)$. The standard target is $P = O(n)$, $S = O(n)$ words and $Q = O(1)$.

**Error model.** A randomized solution is allowed one-sided error: a "yes" may be wrong, a "no" is always right. The error probability is over the random choices of the preprocessing, for a string and a sequence of queries that do not depend on those choices.

## Variants

- **Longest common extension.** Return the largest $\ell$ with $T[i \ldots i+\ell-1] = T[j \ldots j+\ell-1]$: the [longest common extension query](/longest-common-extension-query/). Equality is the test $\mathrm{LCE}(i, j) \ge \ell$.
- **Order queries.** Decide whether $T[i \ldots i+\ell-1]$ is less than, equal to or greater than $T[j \ldots j+\ell-1]$ in lexicographic order. With an LCE value $k$, compare $T[i+k]$ with $T[j+k]$ if $k < \ell$.
- **Two strings.** Compare a substring of $T$ with a substring of another string $U$. Hash both with the same base, or build the structure for $T \# U$ with a separator $\#$.
- **Dynamic strings.** Characters of $T$ change between queries: [dynamic polynomial hashing](/dynamic-polynomial-hashing/) supports updates and queries in $O(\log n)$ time.
- **Special queries.** Is $T[i \ldots j]$ a [palindrome](/palindrome/)? Compare it with the same range of the reversed string. Does $T[i \ldots j]$ have [period](/string-period/) $d$? Ask whether $T[i \ldots j-d] = T[i+d \ldots j]$.

## Examples

Take $T = $ abracadabra ($n = 11$), with the codes a = 1, b = 2, c = 3, d = 4, r = 5.

| query $(i, j, \ell)$ | substrings | answer | LCE$(i, j)$ |
|---|---|---|---|
| (0, 7, 4) | abra, abra | yes | 4 |
| (1, 8, 3) | bra, bra | yes | 3 |
| (0, 3, 1) | a, a | yes | 1 |
| (0, 5, 2) | ab, ad | no | 1 |
| (2, 6, 3) | rac, dab | no | 0 |

**The hash solution.** With $p = 101$ and the base $r = 10$, the prefix hashes $H[k] = h(T[0 \ldots k-1])$ and the powers $W[k] = r^k \bmod p$ are

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $H[k]$ | 0 | 1 | 12 | 24 | 39 | 90 | 93 | 25 | 49 | 88 | 77 | 64 |
| $W[k]$ | 1 | 10 | 100 | 91 | 1 | 10 | 100 | 91 | 1 | 10 | 100 | 91 |

and the hash of $T[i \ldots i+\ell-1]$ is $H[i+\ell] - H[i]\, W[\ell] \bmod p$. For the query (0, 7, 4), the two hashes are $39 - 0 = 39$ and $64 - 25 \cdot 1 = 39$, so the answer is yes. For (2, 6, 3), they are $90 - 12 \cdot 91 \equiv 8$ and $88 - 93 \cdot 91 \equiv 8$. The hashes are equal, but rac and dab differ: the decimal readings 513 and 412 differ by $101$. This is a false yes, caused by the tiny prime and a base that is fixed for the example. Their difference polynomial is $(5-4)t^2 + (1-1)t + (3-2) = t^2 + 1$, so among all 101 bases they collide for exactly 2, the roots $t = 10$ and $t = 91$ of $t^2 + 1$ modulo 101; with $p = 2^{61} - 1$ and a random base, one query errs with probability below $10^{-18}$.

## Known algorithms

- **Direct comparison.** No preprocessing, $O(\ell)$ time per query, no error. Good for few queries or short substrings.
- **Prefix hashes ([polynomial rolling hash](/polynomial-rolling-hash/)).** Store $H[0 \ldots n]$ and $W[0 \ldots n]$ in $O(n)$ time and space, and compare $H[i+\ell] - H[i] W[\ell]$ with $H[j+\ell] - H[j] W[\ell]$ modulo $p$. Query time $O(1)$. A false yes has probability at most $(\ell - 1)/p$ per query, by the [collision bound](/polynomial-hash-collision-bound/). This is the solution of choice in practice because it is short.
- **Naming by doubling (Karp, Miller and Rosenberg).** For each $k \le \lfloor \log_2 n \rfloor$, give each substring of length $2^k$ an integer name, so that equal substrings get equal names; the names for $2^{k+1}$ come from pairs of names for $2^k$. For a query with $2^k \le \ell < 2^{k+1}$, the two substrings are equal if and only if their first $2^k$ characters and their last $2^k$ characters are equal, which is two name comparisons. Preprocessing $O(n \log n)$ time and space, query $O(1)$, no error. The table is often called the dictionary of basic factors, and the same doubling is the core of [prefix doubling](/prefix-doubling/) for suffix arrays.
- **Suffix array, LCP and range minimum.** Build the [suffix array](/suffix-array/) and the [LCP array](/lcp-array/) in $O(n)$ time for an integer alphabet, and a [range minimum query](/range-minimum-query/) structure on the LCP array. Then $\mathrm{LCE}(i, j)$ is the minimum of the LCP values between the ranks of the suffixes $i$ and $j$, in $O(1)$ time, and the answer is $\mathrm{LCE}(i, j) \ge \ell$. Preprocessing $O(n)$, query $O(1)$, no error.
- **Suffix tree and lowest common ancestors.** The depth of the [lowest common ancestor](/lowest-common-ancestor/) of the leaves $i$ and $j$ in the [suffix tree](/suffix-tree/) is $\mathrm{LCE}(i, j)$. Same bounds.

## Bounds

- **Optimality of the standard target.** For $n \ge 2$ and each position $k$, some change of $T[k]$ changes the answer to a query $(k, j, 1)$ with $j \ne k$. So a solution that answers all queries correctly must read every character of $T$ at some time, and $O(n)$ preprocessing with $O(1)$ time per query is optimal up to constant factors.
- **Without preprocessing.** A deterministic algorithm that reads $T$ only at query time must read all $2\ell$ characters of the two substrings in the worst case, when the answer is yes and the substrings do not overlap: if it skips a pair of positions, an adversary changes one of them and the answer becomes no.
- **Error of the hash solution.** For $q$ queries, all fixed before the base is drawn, the probability of any false yes is at most $q(n - 1)/p$ by the union bound. The same bound holds when each query may depend on the answers to the earlier ones, as long as the base and the hash values stay hidden: until the first error, the answers are the true answers, so the queries asked are those of a fixed sequence, and the union bound applies to that sequence. If the hash values or the base are visible, there is no such bound.

## Reductions

- **To longest common extension.** One LCE query answers one equality query.
- **From longest common extension.** By [binary search](/binary-search/) on $\ell$, $O(\log n)$ equality queries give $\mathrm{LCE}(i, j)$, since the answer is yes for all $\ell$ up to the LCE value and no beyond it. With hashing this is the common $O(\log n)$ LCE method; for a correct result every one of the $O(\log n)$ answers must be correct.
- **From string matching.** $P$ occurs in $U$ at $s$ if and only if, in $T = P U$, the query $(0, |P| + s, |P|)$ answers yes. With $O(1)$ queries this gives an $O(|P| + |U|)$ matcher, which is the [Rabin-Karp](/rabin-karp/) idea with prefix hashes.

## Applications

- **Suffix comparison.** Comparing two suffixes in $O(\log n)$ time by binary search on the LCE gives a short $O(n \log^2 n)$ [suffix array construction](/suffix-array-construction/) by any comparison sort.
- **Longest repeated or common substring.** Binary search on the length, then test windows of that length for equal hashes: [longest repeated substring](/longest-repeated-substring/) and [longest common substring](/longest-common-substring/).
- **Palindromes and periods.** Test whether a substring is a [palindrome](/palindrome/) or has a given [period](/string-period/) in $O(1)$ time; with binary search, compute the longest palindrome centered at each position.
- **Rotations.** Compare two rotations of a string with an LCE query on $TT$, which gives the [minimal rotation](/minimal-rotation/) by a linear scan of comparisons.
- **Approximate matching.** The [k-mismatch problem](/k-mismatch-problem/) for one alignment takes $k + 1$ LCE queries, jumping over the matching stretches.

## References
