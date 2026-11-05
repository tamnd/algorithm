---
tag: 05ED1E
kind: algorithm
slug: turbo-boyer-moore
name: Turbo-BM algorithm
aliases:
- Turbo Boyer-Moore
area: strings/exact-matching
level: advanced
summary: Boyer-Moore variant that remembers the matched segment to avoid rescanning, giving at most 2n comparisons.
solves: [string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the alphabet size}
  time: {worst: O(n + m + σ), best: Θ(n/m + m + σ), preprocessing: Θ(m + σ)}
  space: {extra: Θ(m + σ)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [boyer-moore, good-suffix-rule, bad-character-rule, string-period]
see_also: [galil-rule, apostolico-giancarlo, boyer-moore-comparison-bound, backward-dawg-matching, knuth-morris-pratt, two-way-string-matching]
sources:
  - paper: doi:10.1007/BF01185427
    title: M. Crochemore, A. Czumaj, L. Gasieniec, S. Jarominek, T. Lecroq, W. Plandowski and W. Rytter, Speeding up two string-matching algorithms, Algorithmica 12(4-5) (1994), 247-267
    locator: the Turbo-BM algorithm, its memory and turbo shift, and the bound of 2n comparisons
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node15.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Turbo-BM algorithm (description of the memory, the turbo shift and the extra rule with u + 1, the C code TBM, the bound of 2n comparisons, and the example x = GCAGAGAG)
  - book: isbn:9780195086096
    title: Maxime Crochemore and Wojciech Rytter, Text Algorithms, Oxford University Press, 1994
    locator: the chapter on the Boyer-Moore algorithm and its variants (Turbo_BM)
---

The Turbo-BM algorithm solves [string matching](/string-matching/) like [Boyer-Moore](/boyer-moore/), comparing the pattern from right to left and shifting by the [good-suffix](/good-suffix-rule/) and [bad-character](/bad-character-rule/) rules, but it also remembers the text factor that matched a suffix of the pattern in the previous window. It jumps over that factor instead of comparing it again, and it can make a third kind of shift, the turbo shift, when the current match is shorter than the remembered one. With only a constant amount of extra memory over Boyer-Moore, the search makes at most $2n$ character comparisons on a text of length $n$, so its worst case is linear while it keeps the long shifts of Boyer-Moore.

## In plain words

Boyer-Moore compares the word with the text from the right end and then slides it. After a slide, part of the text it just read may again sit under the word. Plain Boyer-Moore forgets this and reads that part again, which costs a lot on texts like aaaa...

Turbo-BM remembers one piece: the stretch of text that matched the end of the word just before the last slide. When the new comparison reaches that stretch, it skips over it, because the answer is already known.

The memory also gives a new reason to slide. If this time fewer letters matched than last time, the two different letters found at the two mismatches cannot both fit under the same copy of the word, so the word can move at least the difference. The algorithm takes the longest of the three slides.

## The problem

The input is a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$ over an integer alphabet $\{0, \ldots, \sigma - 1\}$: the bad-character table is indexed by characters. The implementation uses a dictionary instead, which works for any hashable characters. Indices are 0-based. The output is every shift $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order. Occurrences may overlap. If $m = 0$, every shift $0, \ldots, n$ is output, and if $m > n$, nothing is output.

## The algorithm

The two tables are those of Boyer-Moore. $\mathrm{gs}[i]$, for $0 \le i < m$, is the strong good-suffix shift: the smallest $d \ge 1$ such that $P[k - d] = P[k]$ for all $k$ with $i < k < m$ and $k \ge d$, and $i - d < 0$ or $P[i - d] \ne P[i]$. In particular $\mathrm{gs}[0]$ is the smallest period of $P$. $\lambda(c)$ is the last position of $c$ in $P[0 \ldots m-2]$, or $-1$, as in [Horspool](/boyer-moore-horspool/).

The variable $u$ is the memory: the length of the text factor known to match the pattern, from the previous window. After a good-suffix shift by $\mathit{shift}$, that factor lies at window positions $m - \mathit{shift} - u$ to $m - \mathit{shift} - 1$ of the new window. The variable $v$ is the length of the suffix matched in the current window.

```pseudo id=main
TURBO-BOYER-MOORE(T, P)
L1  n ← |T|, m ← |P|
L2  if m = 0 then output 0, 1, …, n and return
L3  gs ← GOOD-SUFFIX(P), λ ← last occurrences in P[0 .. m − 2]
L4  s ← 0, u ← 0, shift ← m
L5  while s ≤ n − m do
L6      i ← m − 1
L7      while i ≥ 0 and P[i] = T[s + i] do               ▷ right to left
L8          i ← i − 1; if u ≠ 0 and i = m − 1 − shift then i ← i − u   ▷ jump over the memory
L9      if i < 0 then
L10         output s; shift ← gs[0]
L11         u ← m − shift
        else
L12         v ← m − 1 − i
L13         turbo ← u − v
L14         bc ← i − λ(T[s + i])
L15         shift ← max(turbo, bc, gs[i])
L16         if shift = gs[i] then
L17             u ← min(m − shift, v)                    ▷ remember the matched part
            else
L18             u ← 0
L19     s ← s + shift
```

Line L8 is the only change in the comparison loop: when the scan reaches the right end of the remembered factor, it skips the $u$ positions of the factor. Lines L12 to L15 compute the three candidate shifts. The memory is kept only after a good-suffix shift (line L17) or a full match (line L11), because only then is the position of the matched factor in the new window known. A bad-character or turbo shift clears it (line L18).

The table GOOD-SUFFIX is computed in $\Theta(m)$ time exactly as on the page of [Boyer-Moore](/boyer-moore/), from the array of longest common suffixes.

## Example

Search for $P$ = gcagagag in $T$ = gcatcgcagagagtatacagtacg, with $n = 24$ and $m = 8$, the example of Charras and Lecroq. The tables are $\mathrm{gs}$ = 7 7 7 2 7 4 7 1 for $i = 0, \ldots, 7$, and $\lambda$(a) = 6, $\lambda$(c) = 1, $\lambda$(g) = 5, $\lambda$(t) = $-1$.

| $s$ | memory $u$ at start | result | comparisons | turbo | bc | gs | shift | new $u$ |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | mismatch at $i = 7$, $v = 0$ | 1 | 0 | 1 | 1 | 1 | 0 |
| 1 | 0 | mismatch at $i = 5$, $v = 2$ | 3 | $-2$ | 4 | 4 | 4 | 2 |
| 5 | 2 | match, jump over positions 2 and 3 | 6 | | | | 7 | 1 |
| 12 | 1 | mismatch at $i = 5$, $v = 2$ | 3 | $-1$ | 4 | 4 | 4 | 2 |
| 16 | 2 | mismatch at $i = 6$, $v = 1$ | 2 | 1 | 5 | 7 | 7 | 1 |

The output is the single shift 5, after 15 comparisons. Boyer-Moore with the same tables makes 17 on this input: at $s = 5$ it compares all 8 characters, while Turbo-BM knows from the window at $s = 1$ that $T[7 \ldots 8]$ = ag, which now sits under $P[2 \ldots 3]$, and skips it.

A periodic example: $P$ = aabaab in $T$ = abaabaabaabaab. The windows at $s = 0$ and $s = 1$ fail at once and shift by 1. The window at $s = 2$ is a full match with 6 comparisons; the shift is the period $\mathrm{gs}[0] = 3$ and the memory is $u = 3$. At $s = 5$ and $s = 8$, the scan compares $P[5], P[4], P[3]$, jumps over $P[0 \ldots 2]$, and reports a match with 3 comparisons. The output is 2, 5, 8 with 14 comparisons, while plain Boyer-Moore makes 20.

## Correctness

The algorithm outputs only shifts it has checked, provided the skipped positions really match: after a good-suffix shift by $d$ from a window whose suffix of length $v' \ge u$ matched, the last $u$ text characters of that window lie under $P[m - d - u \ldots m - d - 1]$, and the good-suffix condition says these equal $P[m-u \ldots m-1]$, which is the text there. The bad-character and good-suffix shifts are safe as in Boyer-Moore. The turbo shift is safe because, when $v < u$, the remembered factor $w$ is a suffix of $P$ that ends with $b$ followed by the current matched suffix, while the text has $a \ne b$ at the mismatch; a shift $d < u - v$ would place a copy of $w$ over the mismatch, and the alignment with the memory shows that $w$ has period $d$, which forces $a = b$. Every shift is at least 1, so the loop stops. The full proof is below.

## Complexity

- **Preprocessing.** $\Theta(m + \sigma)$ time and space, the same tables as Boyer-Moore; with a dictionary for $\lambda$, $\Theta(m)$ expected.
- **Worst case.** Crochemore et al. prove that Turbo-BM makes at most $2n$ text character comparisons, so the search takes $O(n)$ time in the worst case, against $\Theta(nm)$ for plain Boyer-Moore with all occurrences. The input $T = a^n$, $P = a^m$ costs Boyer-Moore $(n - m + 1)m$ comparisons; Turbo-BM makes $m$ comparisons at the first window and then 1 per window, about $n$ in total, because the memory covers the other $m - 1$ positions.
- **Best case.** As in Boyer-Moore, if each window fails at once on a character not in $P$, there is one comparison per window and the shift is $m$: $\Theta(n/m)$ comparisons.
- **Space.** $\Theta(m + \sigma)$, plus the two integers $u$ and $\mathit{shift}$.

| claim | value |
|---|---|
| preprocessing | $\Theta(m + \sigma)$ |
| comparisons, worst case | at most $2n$ |
| search time, worst case | $O(n)$ |
| best case | $\Theta(n/m)$ comparisons |
| extra memory over Boyer-Moore | $O(1)$ |

The input $a^{1000}$ with $P = a^{10}$ takes exactly 1000 comparisons. The test `test_exhaustive_binary` checks the bound of $2n$ comparisons on all binary texts of length at most 8 and patterns of length at most 4, and `test_random_against_oracle` checks it on random inputs.

## Properties

- **Linear and sublinear.** It keeps the $\Theta(n/m)$ best case of Boyer-Moore and adds a linear worst case, without the extra table of [Apostolico-Giancarlo](/apostolico-giancarlo/).
- **Constant extra memory.** Only $u$ and the last shift are kept between windows.
- **Not online.** Like Boyer-Moore, it needs random access to the current window of $m$ characters.
- **Integer alphabet.** The bad-character table is indexed by characters; the good-suffix table and the memory use only equality tests.

## Variants and improvements

- **A longer shift after a bad-character shift.** The code of Charras and Lecroq adds one more rule: when the bad-character shift beats both the good-suffix and the turbo shift, the shift is raised to at least $u + 1$. This page leaves the rule out, since it rarely lengthens a shift and its safety needs a longer case analysis; the search is correct without it and the tests check the $2n$ bound for this version.
- **No bad-character table.** A version with only the good-suffix and turbo shifts uses $\Theta(m)$ space for any alphabet with equality tests.
- **Remember all matched suffixes.** [Apostolico-Giancarlo](/apostolico-giancarlo/) stores, for every text position, the length of the suffix matched there, and skips any of them. It makes at most $1.5n$ comparisons in a refined analysis, but needs $\Theta(m)$ extra memory for the skips.
- **Galil's rule.** The [Galil rule](/galil-rule/) uses the period of $P$ after a full match only; it gives a linear bound for the version that reports all occurrences, but not the turbo shift.
- **Turbo for factor automata.** The same paper applies the memory idea to [backward DAWG matching](/backward-dawg-matching/), giving Turbo-RF, which is linear in the worst case and optimal on average.

## When to use it

Use Turbo-BM where Boyer-Moore is the right choice, long patterns over a large alphabet, but the input may be adversarial or very repetitive, such as logs, DNA with repeats, or binary data. The change from Boyer-Moore is a few lines and two integers. If only one occurrence is wanted, or the input is not adversarial, plain Boyer-Moore or [Horspool](/boyer-moore-horspool/) is simpler. For a stream, use [KMP](/knuth-morris-pratt/); for constant extra space over a general ordered alphabet, use the [two-way algorithm](/two-way-string-matching/).

## Pitfalls

- **Keeping the memory after the wrong shift.** The memory is only valid after a good-suffix shift or a full match. If it is kept after a bad-character or turbo shift, the scan skips positions that were never checked and reports false matches. The test `test_random_against_oracle` catches this on random binary texts.
- **The jump test with the old shift.** Line L8 compares $i$ with $m - 1 - \mathit{shift}$ for the shift that brought the pattern to this window. Updating $\mathit{shift}$ before the scan breaks the jump. The test `test_example` checks the count of 15 comparisons, which depends on the jump.
- **The memory after a match.** After a full match the memory is $m - \mathrm{gs}[0]$, the overlap of two occurrences one period apart. Setting it to 0 is correct but loses the linear bound on periodic input; the test `test_periodic_input_is_linear` searches $a^{10}$ in $a^{1000}$ and checks at most $2n$ comparisons.
- **A negative turbo or bad-character value.** Both can be negative; the maximum with $\mathrm{gs}[i] \ge 1$ keeps the shift positive. The test `test_edges` runs patterns longer than the text and the empty pattern.

## Implementations

## History

Turbo-BM was presented by Crochemore, Czumaj, Gasieniec, Jarominek, Lecroq, Plandowski and Rytter, first in French in 1991 ("Deux méthodes pour accélérer l'algorithme de Boyer-Moore", in the proceedings of the second Journées franco-belges on automata theory, Rouen) and then in the journal paper "Speeding up two string-matching algorithms" in Algorithmica in 1994. The second method of that paper is Turbo-RF, the same memory applied to the reverse factor algorithm. Earlier ways to make Boyer-Moore linear were Galil's rule of 1979, which uses the period of the pattern after a full match, and the 1986 algorithm of Apostolico and Giancarlo, which keeps a table of size $m$; Turbo-BM needs only a constant amount of extra memory. Charras and Lecroq's catalog of exact string-matching algorithms made the C code and the example above widely known.

## References
