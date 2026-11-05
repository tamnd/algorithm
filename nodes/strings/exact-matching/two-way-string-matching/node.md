---
tag: 5X5RDM
kind: algorithm
slug: two-way-string-matching
name: Two-way algorithm
aliases:
- Crochemore-Perrin algorithm
- Crochemore-Perrin two-way
area: strings/exact-matching
level: advanced
summary: Linear-time, constant-space matching using a critical factorization of the pattern.
solves: [string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern}
  time: {worst: Θ(n + m), best: Θ(n/m + m), preprocessing: Θ(m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [critical-factorization, string-period, string-matching]
see_also: [galil-seiferas, knuth-morris-pratt, boyer-moore, lyndon-word, turbo-boyer-moore, naive-string-matching]
sources:
  - paper: doi:10.1145/116825.116845
    title: M. Crochemore and D. Perrin, Two-way string-matching, Journal of the ACM 38(3) (1991), 650-674
    locator: the two-way scheme on a critical factorization, the computation of the factorization by two maximal suffixes, the memory of the periodic case, and the linear bound with constant extra space
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node26.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Two Way algorithm (the definitions of repetition, local period and critical factorization, the C code maxSuf, maxSufTilde and TW, and the bound of 2n - m text character comparisons)
  - book: isbn:9780195086096
    title: Maxime Crochemore and Wojciech Rytter, Text Algorithms, Oxford University Press, 1994
    locator: the chapter on time-space optimal string matching (the critical factorization theorem and the two-way algorithm)
---

The two-way algorithm of Crochemore and Perrin solves [string matching](/string-matching/) in $O(n + m)$ time with only a constant number of extra variables. It splits the pattern at a [critical factorization](/critical-factorization/) $P = x_\ell x_r$, a cut where the local repetition is as long as the period of the whole pattern; it compares $x_r$ from left to right and, if that part matches, $x_\ell$ from right to left. The cut is found in linear time from two maximal suffixes of the pattern, one for the order of the alphabet and one for the reverse order, so the alphabet must be ordered. The algorithm is used in the C libraries glibc and musl for `strstr` and `memmem`.

## In plain words

Cut the word into a left part and a right part at a well-chosen place. At each position of the text, first check the right part, letter by letter from left to right. If a letter differs, slide the word forward by the number of right-part letters that matched plus one; the special cut guarantees that no copy of the word starts in between. If the whole right part matches, check the left part from right to left. Then slide by the period of the word, or by more when the word has no short period.

The cut is chosen so that, around it, the word looks the same only when shifted by its full period. Finding it needs only a few counters, never a table, so the method uses almost no memory. It also never reads a letter of the text more than about twice.

## The problem

The input is a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$ over a general ordered alphabet: the search tests characters for equality, and the preprocessing compares pattern characters with a total order. Indices are 0-based. The output is every shift $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order. Occurrences may overlap. If $m = 0$, every shift $0, \ldots, n$ is output, and if $m > n$, nothing is output.

## The algorithm

**Critical factorization.** For a cut of $P$ between positions $c - 1$ and $c$, a *repetition* is a nonempty word $w$ such that $w$ and $P[0 \ldots c-1]$ are suffixes of one another, and $w$ and $P[c \ldots m-1]$ are prefixes of one another. The smallest length of a repetition is the *local period* at the cut; it is at most the period $\mathrm{per}(P)$. A cut is *critical* when its local period equals $\mathrm{per}(P)$. The critical factorization theorem (Césari and Vincent) says that every word with $m \ge 2$ has a critical cut among any $\mathrm{per}(P)$ consecutive cuts.

Crochemore and Perrin compute one as follows. Let $z$ be the lexicographically maximal suffix of $P$ for the order $<$, and $\tilde z$ the maximal suffix for the reverse order. The cut before the shorter of the two suffixes, that is, the one that starts later, is critical, and the left part $x_\ell$ is shorter than $\mathrm{per}(P)$. Each maximal suffix and its period come from one pass of the procedure MAXIMAL-SUFFIX below, with $O(1)$ variables and $O(m)$ character comparisons.

**Search.** Let $\ell$ be the last index of $x_\ell$ (so $x_\ell = P[0 \ldots \ell]$, and $\ell = -1$ when $x_\ell$ is empty) and let $p$ be the period of the chosen maximal suffix. If $P[0 \ldots \ell] = P[p \ldots p + \ell]$, then $p = \mathrm{per}(P)$ and the pattern is handled as periodic: after a full scan the shift is $p$, and the next window starts with $m - p$ characters known to match, which are not compared again (the variable $\mathit{mem}$). Otherwise $\mathrm{per}(P) > \max(\ell + 1, m - \ell - 1)$, and the shift after a full scan is $q = \max(\ell + 1, m - \ell - 1) + 1$, a lower bound for the period that needs no memory.

```pseudo id=main
TWO-WAY(T, P)
L1  n ← |T|, m ← |P|
L2  if m = 0 then output 0, 1, …, n and return
L3  (ℓ, p) ← CRITICAL-FACTORIZATION(P)
L4  if P[0 .. ℓ] = P[p .. p + ℓ] then                     ▷ p = per(P)
L5      s ← 0, mem ← −1
L6      while s ≤ n − m do
L7          i ← max(ℓ, mem) + 1
L8          while i < m and P[i] = T[s + i] do i ← i + 1    ▷ right part, left to right
L9          if i ≥ m then
L10             i ← ℓ; while i > mem and P[i] = T[s + i] do i ← i − 1   ▷ left part
L11             if i ≤ mem then output s
L12             s ← s + p, mem ← m − p − 1
L13         else s ← s + i − ℓ, mem ← −1
L14 else
L15     q ← max(ℓ + 1, m − ℓ − 1) + 1, s ← 0
L16     while s ≤ n − m do
L17         i ← ℓ + 1; while i < m and P[i] = T[s + i] do i ← i + 1
L18         if i ≥ m then i ← ℓ; while i ≥ 0 and P[i] = T[s + i] do i ← i − 1; (if i < 0 then output s); s ← s + q
L19         else s ← s + i − ℓ

MAXIMAL-SUFFIX(P, ≺)                                       ▷ returns (ms, period of P[ms + 1 ..])
L20 ms ← −1, j ← 0, k ← 1, per ← 1
L21 while j + k < m do
L22     a ← P[j + k], b ← P[ms + k]
L23     if a ≺ b then j ← j + k, k ← 1, per ← j − ms
L24     else if a = b then (if k ≠ per then k ← k + 1 else j ← j + per, k ← 1)
L25     else ms ← j, j ← ms + 1, k ← 1, per ← 1
L26 return (ms, per)

CRITICAL-FACTORIZATION(P)
L27 (i, p₁) ← MAXIMAL-SUFFIX(P, <), (j, p₂) ← MAXIMAL-SUFFIX(P, >)
L28 if i > j then return (i, p₁) else return (j, p₂)
```

In MAXIMAL-SUFFIX, $P[ms+1 \ldots]$ is the best suffix candidate so far, $P[j+1 \ldots j+k]$ is compared with $P[ms+1 \ldots ms+k]$, and $\mathit{per}$ is the period of the part of the candidate matched so far. A smaller character at line L23 extends the candidate's run with a longer period; a larger one at line L25 makes the suffix at $j + 1$ the new candidate. Lines L23 and L24 increase $j + k$ by 1, and line L25 increases $ms$ and sets $j + k = ms + 2$, so the number of steps is at most about $2m$ and the work is $O(m)$.

## Example

Search for $P$ = gcagagag in $T$ = gcatcgcagagagtatacagtacg, with $n = 24$ and $m = 8$. With a < c < g, the maximal suffix is the whole word (ms $= -1$, period 7). For the reverse order, the maximal suffix is agagag (ms $= 1$, period 2). The later start wins: $\ell = 1$, $x_\ell$ = gc, $x_r$ = agagag, $p = 2$. Since $P[0 \ldots 1]$ = gc differs from $P[2 \ldots 3]$ = ag, the pattern is handled as non-periodic, with $q = \max(2, 6) + 1 = 7$. Its true period is 7, and the local period at the cut, between c and a, is 7 as well.

| $s$ | right part $P[2 \ldots 7]$ against $T$ | left part | comparisons | shift |
|---|---|---|---|---|
| 0 | a = a, t ≠ g at $i = 3$ | | 2 | $3 - 1 = 2$ |
| 2 | g ≠ a at $i = 2$ | | 1 | 1 |
| 3 | c ≠ a at $i = 2$ | | 1 | 1 |
| 4 | g ≠ a at $i = 2$ | | 1 | 1 |
| 5 | agagag matches | c, g match | 8 | 7 |
| 12 | a = a, t ≠ g at $i = 3$ | | 2 | 2 |
| 14 | a = a, t ≠ g at $i = 3$ | | 2 | 2 |
| 16 | a, g = a, g, c ≠ a at $i = 4$ | | 3 | 3 |

The output is 5, after 20 comparisons, within the bound $2n - m = 40$.

A periodic example: $P$ = aabaab in $T$ = abaabaabaabaab. With a < b the maximal suffix is baab, starting at index 2; for the reverse order it is the whole word. The later start wins, so $\ell = 1$, $x_\ell$ = aa, $x_r$ = baab and $p = 3$. Since $P[0 \ldots 1] = P[3 \ldots 4]$ = aa, the pattern is periodic with period 3. The windows at $s = 0$ and $s = 1$ fail at once and shift by 1. At $s = 2$ all 6 characters match; the shift is 3 and $\mathit{mem} = 6 - 3 - 1 = 2$. At $s = 5$ and $s = 8$, the scan starts at $i = 3$, matches $P[3 \ldots 5]$, and the left part needs no comparison because $\ell \le \mathit{mem}$: each window costs 3 comparisons. The output is 2, 5, 8, after 14 comparisons.

## Correctness

The shifts are safe because of the critical cut. If an occurrence started at $s + d$ inside the skipped range, the text characters that the window has matched just right of the cut would also be matched by the shifted pattern, so $d$, and then every $d - t\,\mathrm{per}(P) \ge 1$, would be the length of a repetition at the cut. Since the local period at a critical cut is $\mathrm{per}(P)$, this forces $\mathrm{per}(P)$ to divide $d$, and then the shifted pattern has the same character as $P$ at the mismatch, a contradiction. After a full match of the right part, the same argument shows that the next occurrence is at least $\mathrm{per}(P)$ away, and both $p$ (periodic case) and $q$ (otherwise) are at most $\mathrm{per}(P)$. The memory in the periodic case holds the $m - p$ characters that the previous window matched. The full proof is below.

## Complexity

- **Preprocessing.** Two runs of MAXIMAL-SUFFIX, each with $O(m)$ comparisons, and one comparison of $\ell + 1 < m$ characters at line L4: $\Theta(m)$ time and $O(1)$ extra space.
- **Search.** In the right-part scan, each successful comparison at $s + i$ is followed by a shift of at least $i - \ell$ or by a full scan, so the right scans make at most $n$ comparisons in total; the left scans run only after a full right match, are followed by a shift of at least $\ell + 1$ positions, and cost at most $\ell + 1$ comparisons each. Crochemore and Perrin show that the total is at most $2n - m$ text character comparisons, and the search takes $\Theta(n)$ time in the worst case.
- **Best case.** A mismatch after $r$ comparisons in the right part shifts by $r$, so on most patterns the search reads a constant fraction of the text. When the right part is short, it can be sublinear: for $P = a^7 b$ the cut is $\ell = 6$ and $q = 8$, and on $T = (x^7 b)^{125}$, with $n = 1000$, each window costs 2 comparisons (b, then a mismatch on x) and shifts by 8, for 250 comparisons in total. The best case over all inputs is $\Theta(n/m)$ comparisons.
- **Space.** $O(1)$ extra: the indices $\ell$, $p$, $q$, $s$, $i$, $\mathit{mem}$.

| claim | value |
|---|---|
| preprocessing | $\Theta(m)$ time, $O(1)$ space |
| comparisons in the search | at most $2n - m$ |
| time | $\Theta(n + m)$ |
| extra space | $O(1)$ |

The test `test_comparison_bound` checks the bound $2n - m$ on every binary text of length at most 10 and pattern of length at most 5.

## Properties

- **Constant extra space.** No table depends on $m$, unlike [KMP](/knuth-morris-pratt/) and [Boyer-Moore](/boyer-moore/).
- **Linear worst case.** At most $2n - m$ comparisons, with no quadratic input.
- **Ordered alphabet.** The order is used only in the preprocessing, to find the critical cut. The search tests equality only.
- **Not online.** It reads the left part of a window after its right part, so it needs the current window in memory.

## Variants and improvements

- **A bad-character skip.** The glibc and musl implementations add a shift table on the last character of the window, as in [Horspool](/boyer-moore-horspool/), for long needles. This makes the search sublinear on typical text while keeping the linear worst case.
- **Fewer comparisons.** Breslauer designed a variant with fewer than $2n - m$ comparisons, still in constant space.
- **Other constant-space algorithms.** [Galil-Seiferas](/galil-seiferas/) was the first linear algorithm with $O(1)$ extra space (1983); the two-way algorithm is simpler and faster.
- **Lyndon words.** The maximal suffix of $P$ for an order is the smallest suffix for the reverse order, which is the last factor of the [Lyndon factorization](/lyndon-factorization/) of $P$ for that reverse order; the procedure MAXIMAL-SUFFIX is close to Duval's factorization algorithm.

## When to use it

Use the two-way algorithm when memory per pattern must be constant and the worst case must be linear, for example in a C library `strstr` that must not allocate memory and must resist adversarial input. When a table of size $m$ is affordable, [KMP](/knuth-morris-pratt/) is simpler for streams and [Boyer-Moore](/boyer-moore/) variants are faster on typical text.

## Pitfalls

- **Only one maximal suffix.** The maximal suffix for one order alone does not always give a critical cut. For ba with a < b it is the whole word, the cut is before position 0, and the local period there is 1 while the period is 2; the reverse order gives the critical cut between b and a. The test `test_critical_factorization` checks that the local period at the chosen cut equals the period of the word for all words over three letters up to length 7.
- **The period test.** The test of line L4 must compare $P[0 \ldots \ell]$ with $P[p \ldots p + \ell]$; using $p$ as the period without it gives shifts that are too long when $p$ is only the period of the suffix. The test `test_example` uses gcagagag, whose suffix period 2 differs from its period 7.
- **Forgetting to reset the memory.** After a right-part mismatch, $\mathit{mem}$ must go back to $-1$, or the next window skips characters that were never checked. The test `test_random_against_oracle` catches this.
- **An empty left part.** For $m = 1$ or words such as ab, $\ell = -1$ and the left part is empty; the loops must handle it. The test `test_edges` searches patterns of length 1 to 4.

## Implementations

## History

Crochemore and Perrin published the algorithm in 1991 in the Journal of the ACM, after the constant-space algorithm of [Galil and Seiferas](/galil-seiferas/) (1983) had shown that linear time and constant space are compatible. It rests on the critical factorization theorem of Césari and Vincent (1978), later sharpened by Duval, and on the computation of maximal suffixes. Charras and Lecroq's catalog gave a short C version, and the algorithm entered GNU glibc for `strstr` and `memmem` in 2008, and later musl, because it guarantees linear time without allocating memory.

## References
