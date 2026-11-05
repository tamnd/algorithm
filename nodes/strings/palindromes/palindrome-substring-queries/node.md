---
tag: RKFCXX
kind: problem
slug: palindrome-substring-queries
name: Palindrome substring queries
aliases:
- palindrome range queries
area: strings/palindromes
level: advanced
summary: Preprocess a string to answer whether any given substring is a palindrome quickly.
model: comparison-model
complexity:
  vars: {n: the length of the string, q: the number of queries}
  time: {worst: Θ(n + q)}
  space: {aux: Θ(n)}
prereqs: [palindrome, manacher, palindrome-recognition]
see_also: [longest-palindromic-substring, count-palindromic-substrings, palindromic-tree, polynomial-rolling-hash, fenwick-tree, lowest-common-ancestor, suffix-tree, range-minimum-query]
sources:
  - paper: doi:10.1145/321892.321896
    title: Glenn Manacher, A new linear-time on-line algorithm for finding the smallest initial palindrome of a string, Journal of the ACM 22(3) (1975), 346-351
    locator: the whole paper (the linear scan that gives the maximal palindrome at each center)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 9, Section 9.2, Finding all maximal palindromes in linear time (longest common extension queries on a string and its reverse)
  - paper: doi:10.1147/rd.312.0249
    title: Richard M. Karp and Michael O. Rabin, Efficient randomized pattern-matching algorithms, IBM Journal of Research and Development 31(2) (1987), 249-260
    locator: the fingerprint method (polynomial hashes of substrings compared in constant time with a small error probability)
  - paper: doi:10.1007/978-3-319-67428-5_25
    title: Mikhail Rubinchik and Arseny M. Shur, Counting palindromes in substrings, SPIRE 2017, Lecture Notes in Computer Science 10508, 290-303
    locator: the main result (the number of distinct palindromes in a query substring)
---

Palindrome substring queries ask, many times, whether a substring $s[i..j]$ of a fixed string $s$ is a [palindrome](/palindrome/). Testing each query with the two-pointer scan costs $\Theta(j - i)$. After one run of [Manacher's algorithm](/manacher/) in $\Theta(n)$ time, each query is answered in $O(1)$ time by one comparison: $s[i..j]$ is a palindrome if and only if the radius at its center is at least its length. Hashes, longest common extensions and harder questions about the palindromes inside $s[i..j]$ are the variants.

## In plain words

You have one long word and you will get many questions of the form "does the piece from here to there read the same from both ends?". Checking each piece letter by letter is slow when the pieces are long. Instead, first find, for each middle point of the word, how far a palindrome reaches around it. A piece is a palindrome exactly when the palindrome around its middle reaches at least as far as the piece. So after one pass over the word, each question takes one look in a table.

## Definition

**Input.** A string $s = s[0..n-1]$ over an [alphabet](/alphabet/) $\Sigma$, with 0-based indices, and then $q$ queries $(i, j)$ with $0 \le i \le j \le n - 1$; $s[i..j]$ includes both ends. The comparison-based methods test symbols for equality only; the hashing methods treat symbols as integers.

**Output.** For each query, whether $s[i..j]$ is a palindrome. The length $j - i + 1$ may be odd or even.

**Cost.** Preprocessing time and space, and time per query. The queries may come online, after the preprocessing, or offline, all known in advance.

## Variants

- **Updates.** The string changes by point substitutions between queries. Keep the forward and the backward [polynomial hash](/polynomial-rolling-hash/) of $s$ in two [Fenwick trees](/fenwick-tree/): an update and a query take $O(\log n)$ time, and the answer is correct with high probability.
- **Longest palindrome inside $s[i..j]$.** Report the longest palindromic substring of $s[i..j]$. The maximal palindromes of $s$ are not enough, because a palindrome of $s[i..j]$ that touches an end of the query can be cut off; this needs more involved structures.
- **Counting inside $s[i..j]$.** Report the number of distinct palindromes that occur in $s[i..j]$. Rubinchik and Shur (2017) give a data structure for this question; see [counting palindromic substrings](/count-palindromic-substrings/).
- **Gapped and approximate queries.** Is $s[i..j]$ a palindrome with up to $k$ mismatches, or a palindrome with a gap in the middle? See [gapped palindrome](/gapped-palindrome/).
- **Reverse complement.** For DNA, the same queries with the reverse complement in place of the reverse; see [reverse-complement palindrome](/reverse-complement-palindrome/).

## Examples

Let $s = $ `abaab`. Manacher's array on $\#a\#b\#a\#a\#b\#$ is $P = [0, 1, 0, 3, 0, 1, 4, 1, 0, 1, 0]$, where $P[c]$ is the length in $s$ of the longest palindrome with center $c$. The center of $s[i..j]$ is $c = i + j + 1$.

| query $(i, j)$ | $s[i..j]$ | $c$ | $P[c]$ | $P[c] \ge j - i + 1$ | palindrome |
| --- | --- | --- | --- | --- | --- |
| $(2, 2)$ | `a` | 5 | 1 | $1 \ge 1$ | yes |
| $(0, 2)$ | `aba` | 3 | 3 | $3 \ge 3$ | yes |
| $(2, 3)$ | `aa` | 6 | 4 | $4 \ge 2$ | yes |
| $(1, 4)$ | `baab` | 6 | 4 | $4 \ge 4$ | yes |
| $(3, 4)$ | `ab` | 8 | 0 | $0 \ge 2$ fails | no |
| $(0, 3)$ | `abaa` | 4 | 0 | $0 \ge 4$ fails | no |
| $(0, 4)$ | `abaab` | 5 | 1 | $1 \ge 5$ fails | no |

The queries $(2, 3)$ and $(1, 4)$ share the center 6 between the two `a`: both are even palindromes, nested around it.

## Known algorithms

**Scan per query, $O(1)$ preprocessing.** Test $s[i..j]$ with the two-pointer scan of [palindrome recognition](/palindrome-recognition/): $\lfloor (j - i + 1)/2 \rfloor$ comparisons, $\Theta(nq)$ in the worst case.

**Interval table, $\Theta(n^2)$ preprocessing.** Fill $\mathrm{pal}(i, j) = (s[i] = s[j]) \wedge \mathrm{pal}(i+1, j-1)$ for all pairs by increasing length. Each query is one lookup, but the space is $\Theta(n^2)$.

**Manacher's array, $\Theta(n)$ preprocessing, $O(1)$ per query.** Compute $P[0..2n]$ with [Manacher's algorithm](/manacher/). The palindromes with center $c$ are nested, and their lengths are $P[c], P[c] - 2, \ldots$, all of the parity of $P[c]$, which is the parity of $c$. A substring $s[i..j]$ has center $c = i + j + 1$ and length $j - i + 1$, of the same parity, so:

```pseudo id=query
IS-PALINDROME(P, i, j)              ▷ P from MANACHER(s), 0 ≤ i ≤ j ≤ n − 1
L1  c ← i + j + 1                   ▷ the center of s[i .. j] on # s[0] # ... # s[n − 1] #
L2  return P[c] ≥ j − i + 1
```

*Correctness.* If $P[c] \ge j - i + 1$, then $s[i..j]$ is the palindrome of length $j - i + 1$ in the nested family at $c$, since both lengths have the same parity. If $s[i..j]$ is a palindrome with center $c$, then $P[c]$, the longest one there, is at least as long. *Cost.* $\Theta(n)$ time and space before the queries, and two operations per query, so $\Theta(n + q)$ in all.

**Longest common extensions, $O(n)$ preprocessing, $O(1)$ per query.** $s[i..j]$ is a palindrome if and only if the longest common prefix of the suffix $s[i..n-1]$ and the suffix of $s^R$ that starts at the image $n - 1 - j$ of position $j$ is at least $j - i + 1$. With a [suffix tree](/suffix-tree/) of $s\,\#\,s^R$ and constant-time [lowest common ancestor](/lowest-common-ancestor/) queries, or a suffix array with [range minimum queries](/range-minimum-query/), each extension query takes $O(1)$ time. Gusfield uses these queries to find all maximal palindromes; for a single test it is heavier than Manacher's array, but the same structure also answers queries with $k$ mismatches in $O(k)$ extension queries.

**Rolling hashes, $O(n)$ preprocessing, $O(1)$ per query.** Store the prefix hashes $H$ of $s$ and $H^R$ of $s^R$ in the style of Karp and Rabin, and compare the hash of $s[i..j]$ with the hash of $s^R[n-1-j..n-1-i]$. A modulus chosen at random makes a wrong "yes" unlikely; a "no" is always right. This is the method that extends to updates.

**History.** Manacher (1975) found the palindromic prefixes of a string online in linear time, and his scan, read as an array of radii for all centers, became the standard way to answer palindrome queries. Gusfield's textbook (1997) presents the maximal palindromes through longest common extension queries on $s$ and $s^R$. Karp and Rabin (1987) introduced the fingerprints that give the hashing method. Queries about all palindromes inside a substring are more recent, for example the distinct count of Rubinchik and Shur (2017).

## Bounds

- **Upper bound.** $\Theta(n)$ preprocessing and $O(1)$ per query, in the comparison model, by Manacher's array.
- **Preprocessing.** The query $(0, n-1)$ alone is [palindrome recognition](/palindrome-recognition/), so $\lfloor n/2 \rfloor$ comparisons are needed on $a^n$, in the preprocessing and the queries together.
- **Per query.** $O(1)$ is optimal, since the query must at least be read.
- **Space.** $2n + 1$ integers for $P$. A structure that answers all queries without reading $s$ again must store at least $n - 1$ binary digits, because the answers to the queries $(i, i+1)$ can be any pattern of equal and unequal neighbors.

## Reductions

- **To Manacher's array.** Each query is one comparison with one entry of $P$.
- **To longest common extensions.** A palindrome query is one extension query between $s$ and $s^R$.
- **From palindrome recognition.** The query $(0, n - 1)$ is the recognition of $s$.
- **To counting.** The [occurrence count](/count-palindromic-substrings/) is the number of queries $(i, j)$ with the answer yes, computed without asking them one by one.

## Applications

- **Dynamic programs over substrings.** [Palindrome partition dynamic programming](/palindrome-partition-dp/) and [backtracking](/palindrome-partition-backtracking/) ask "is $s[j..i]$ a palindrome?" for many pairs; Manacher's array answers these in $O(1)$ each in $O(n)$ space, in place of the $\Theta(n^2)$ table.
- **Biology.** Testing candidate hairpin regions of DNA for reverse-complement palindromes.
- **Programming tasks.** Many queries on substrings are standard exercises for Manacher's algorithm and for rolling hashes with Fenwick trees.

## References
