---
tag: Z996JP
kind: problem
slug: periodicity-detection
name: Periodicity detection
aliases:
- period computation
- computing all periods
area: strings/string-combinatorics
level: core
summary: Compute the smallest period or all periods of a string.
model: comparison-model
complexity:
  vars: {n: the length of the string}
  time: {worst: Θ(n)}
  space: {aux: Θ(n)}
prereqs: [string-period, prefix-function]
see_also: [z-algorithm, knuth-morris-pratt, primitive-root-of-a-word, string-compression-by-period, fine-and-wilf-theorem, critical-factorization, two-way-string-matching, border]
sources:
  - paper: doi:10.1137/0206024
    title: Donald E. Knuth, James H. Morris and Vaughan R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2), 1977, 323-350
    locator: the failure function, computed in linear time, and its relation to the periods of the pattern
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings, Cambridge University Press, 2007
    locator: Chapter 1, Tools (periods and borders, the border table and its linear-time computation)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 1, Exact matching (the Z values and their linear-time computation) and Chapter 2 (the failure function of Knuth-Morris-Pratt)
  - paper: doi:10.1090/S0002-9939-1965-0174934-9
    title: N. J. Fine and H. S. Wilf, Uniqueness theorems for periodic functions, Proceedings of the American Mathematical Society 16(1), 1965, 109-114
    locator: the periodicity theorem used to show that the small periods are the multiples of the smallest one
---

Periodicity detection asks for the smallest [period](/string-period/) of a string, or for the list of all its periods. A period $p$ of $s$ is a shift with $s[i] = s[i+p]$ wherever both sides exist, and periods correspond one to one to [borders](/border/), so the [prefix function](/prefix-function/) of Knuth, Morris and Pratt gives the smallest period in $O(n)$ time and lists all periods by following its border chain. The [Z-algorithm](/z-algorithm/) gives the same list in a different way: $p < n$ is a period exactly when $z[p] = n - p$.

## In plain words

Picture a strip of letters and a copy of it on a clear sheet laid on top. Slide the copy to the right step by step. A slide is a period when every letter of the copy that still lies over the strip matches the letter under it. The smallest working slide tells how often the strip repeats itself, and the strip is built from copies of its first few letters. Sliding and checking every time is slow. The fast methods do one pass over the strip and record, for each spot, how much of the start of the strip ends there. From that record every working slide can be read off at once.

## Definition

**Input.** A string $s = s[0..n-1]$ with $n \ge 1$ over an [alphabet](/alphabet/) $\Sigma$. Algorithms test letters only for equality, so $\Sigma$ needs no order and may be of any size. Indices are 0-based, and $s[i..j]$ includes both ends.

**Output.** Either the smallest period $\mathrm{per}(s)$, or the set $P(s) = \{ p : 1 \le p \le n,\ s[i] = s[i+p] \text{ for } 0 \le i < n - p \}$ in increasing order. The length $n$ always belongs to $P(s)$.

**Duality with borders.** $p \in P(s)$ if and only if $s[0..n-p-1] = s[p..n-1]$, that is, if $s$ has a border of length $n - p$. So $\mathrm{per}(s) = n - |\mathrm{Border}(s)|$, and listing the borders lists the periods.

## Variants

- **Smallest period of every prefix.** The prefix function gives $\mathrm{per}(s[0..i]) = i + 1 - \pi[i]$ for all $i$ in one pass.
- **Test one shift.** Decide whether a given $p$ is a period: $n - p$ comparisons and constant space.
- **Periods of factors.** Answer many queries "what is the smallest period of $s[i..j]$" after preprocessing; this is one of the internal queries on strings.
- **Approximate periods.** Find shifts $p$ with at most $k$ mismatches $s[i] \ne s[i+p]$, or a word $u$ such that $s$ is close to a prefix of $u^\infty$ in Hamming or edit distance.
- **Quasi-periods.** Find a shortest cover, a word whose occurrences cover every position of $s$, or a [seed](/seed/); these generalize periods to overlapping or partial copies.
- **Local periods.** For each cut of $s$, the length of the shortest square centered there; the [critical factorization](/critical-factorization/) theorem says that the largest local period equals $\mathrm{per}(s)$.

## Examples

| $s$ | $n$ | prefix function $\pi$ | Z-array | periods | $\mathrm{per}(s)$ |
| --- | --- | --- | --- | --- | --- |
| `abcd` | 4 | 0, 0, 0, 0 | 4, 0, 0, 0 | 4 | 4 |
| `aaaaa` | 5 | 0, 1, 2, 3, 4 | 5, 4, 3, 2, 1 | 1, 2, 3, 4, 5 | 1 |
| `abacaba` | 7 | 0, 0, 1, 0, 1, 2, 3 | 7, 0, 1, 0, 3, 0, 1 | 4, 6, 7 | 4 |
| `aabaabaa` | 8 | 0, 1, 0, 1, 2, 3, 4, 5 | 8, 1, 0, 5, 1, 0, 2, 1 | 3, 6, 7, 8 | 3 |
| `abcabcab` | 8 | 0, 0, 0, 1, 2, 3, 4, 5 | 8, 0, 0, 5, 0, 0, 2, 0 | 3, 6, 8 | 3 |
| `abaababaab` | 10 | 0, 0, 1, 1, 2, 3, 2, 3, 4, 5 | 10, 0, 1, 3, 0, 5, 0, 1, 2, 0 | 5, 8, 10 | 5 |

For `aabaabaa`, the border chain from $\pi[7] = 5$ is $5, \pi[4] = 2, \pi[1] = 1, \pi[0] = 0$, which gives the periods $8 - 5 = 3$, $8 - 2 = 6$, $8 - 1 = 7$ and $8$. The Z-array gives the same set: $z[3] = 5 = 8 - 3$, $z[6] = 2 = 8 - 6$ and $z[7] = 1 = 8 - 7$, while for example $z[1] = 1 \ne 7$. The periods 3 and 7 show that a period need not be a multiple of the smallest one when it exceeds $n - \mathrm{per}(s)$.

## Known algorithms

**Check every shift, $O(n^2)$.** For $p = 1, 2, \ldots$ compare $s[i]$ with $s[i+p]$ for all $i < n - p$, stopping at the first mismatch; the first $p$ that passes is $\mathrm{per}(s)$. On $a^{n-1}b$ every shift fails only at the last comparison, so the cost is about $n^2/2$.

**Prefix function, $O(n)$.** Compute $\pi$ in $O(n)$ time as in [Knuth-Morris-Pratt](/knuth-morris-pratt/). Then $\mathrm{per}(s) = n - \pi[n-1]$, and the border chain lists all periods in increasing order:

```pseudo id=all-periods
ALL-PERIODS(s)                ▷ s[0 .. n − 1], n ≥ 1
L1  π ← PREFIX-FUNCTION(s)
L2  b ← π[n − 1], P ← empty list
L3  loop
L4      append n − b to P
L5      if b = 0 then return P
L6      b ← π[b − 1]
```

The chain visits every border, longest first, because the longest proper border of a border of $s$ is the next border of $s$; see the [prefix function](/prefix-function/) page. The output can have $n$ entries, as for $a^n$, so listing is $\Theta(n)$ in the worst case.

**Z-algorithm, $O(n)$.** Compute $z[p]$, the length of the longest common prefix of $s$ and $s[p..n-1]$, for all $p$ with the [Z-algorithm](/z-algorithm/). Then $p < n$ is a period if and only if $z[p] = n - p$, that is, if the suffix at $p$ is a prefix of $s$.

**Compact output: $O(\log n)$ progressions.** The set of periods, though it can have $\Theta(n)$ elements, is a union of $O(\log n)$ arithmetic progressions. *Proof.* First, the periods $q \le n/2$ of $s$ are exactly the multiples of $\mathrm{per}(s)$ up to $n/2$: such a $q$ satisfies $\mathrm{per}(s) + q \le n$, so by the [Fine and Wilf theorem](/fine-and-wilf-theorem/) $\gcd(\mathrm{per}(s), q)$ is a period, and minimality forces $\mathrm{per}(s) \mid q$; conversely multiples of a period are periods. In terms of borders, the borders of $s$ of length at least $n/2$ form one progression. Next, let $w$ be the longest border of $s$ of length less than $n/2$. A border of $s$ shorter than $|w|$ is a prefix and a suffix of $w$, so it is a border of $w$, and conversely a border of a border is a border. So the remaining borders of $s$ are $w$ and the borders of $w$, and the same argument applies to $w$, whose length is less than half of $n$. After at most $\log_2 n + 1$ halvings no border is left, so there are $O(\log n)$ progressions. $\square$

**History.** Morris and Pratt (1970) and Knuth (independently) introduced the failure function, and the 1977 paper of Knuth, Morris and Pratt relates it to the periods of the pattern. The Z-values were popularized as a basic tool by Gusfield (1997). The periodicity theorem of Fine and Wilf (1965) gives the structure of the set of periods.

## Bounds

**Upper bound.** $O(n)$ time with equality tests, by either method above; $O(n)$ extra space for the table.

**Lower bound.** At least $\lceil n/2 \rceil$ comparisons in the worst case for $n \ge 2$ and an alphabet with two letters. *Proof.* On $s = a^n$ the smallest period is 1. If some index $j$ takes part in no comparison, change $s[j]$ to $b$: the comparisons give the same results and the algorithm still answers 1, but $s[j] \ne s[j \pm 1]$ now, so 1 is no longer a period. So every index takes part in some comparison, and each comparison involves two indices. $\square$

## Reductions

- **Primitive root.** The [primitive root](/primitive-root-of-a-word/) of $s$ has length $\mathrm{per}(s)$ if $\mathrm{per}(s)$ divides $n$ and length $n$ otherwise, so it reduces to computing the smallest period.
- **Compression by the period.** [Compressing a string by its period](/string-compression-by-period/) stores $s[0..\mathrm{per}(s)-1]$ and $n$.
- **To longest common prefixes.** $p$ is a period if and only if the suffix $s[p..n-1]$ is a prefix of $s$, so one longest-common-prefix value per suffix, the Z-array, decides every shift.
- **Borders.** All borders and all periods are the same problem under the map $p \mapsto n - p$.

## Applications

- **Pattern matching.** The shifts of [Knuth-Morris-Pratt](/knuth-morris-pratt/) are periods of pattern prefixes, and [two-way matching](/two-way-string-matching/) needs the period of the pattern after a critical factorization.
- **Repetitions.** Computing runs and squares uses the periods of factors; see [maximal repetition](/maximal-repetition/).
- **Data compression.** A string of small period is stored as one period and a length.
- **Combinatorics on words.** Tests of conjectures on periods, [primitive words](/primitive-word/) and the [Fine and Wilf theorem](/fine-and-wilf-theorem/) start from the list of all periods.

## References
