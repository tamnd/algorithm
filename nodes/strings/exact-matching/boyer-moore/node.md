---
tag: GBSH7D
kind: algorithm
slug: boyer-moore
name: Boyer-Moore algorithm
aliases:
- Boyer-Moore string search
area: strings/exact-matching
level: core
summary: Compares the pattern right to left and skips using bad-character and good-suffix shifts; sublinear on average.
solves: [string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the alphabet size}
  time: {worst: Θ(n m), best: Θ(n/m + m + σ), preprocessing: Θ(m + σ)}
  space: {extra: Θ(m + σ)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [bad-character-rule, good-suffix-rule, string-matching]
see_also: [boyer-moore-horspool, quick-search, galil-rule, boyer-moore-comparison-bound, turbo-boyer-moore, apostolico-giancarlo, knuth-morris-pratt, naive-string-matching]
sources:
  - paper: doi:10.1145/359842.359859
    title: R. S. Boyer and J S. Moore, A fast string searching algorithm, Communications of the ACM 20(10) (1977), 762-772
    locator: the algorithm with the tables delta1 and delta2, and its empirical behavior on English text
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 2, Section 2.2 (the Boyer-Moore algorithm with the extended bad character rule and the strong good suffix rule), and Chapter 3, Section 3.2 (Cole's linear worst-case bound), pages 16-34 and 35-69
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node14.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Boyer-Moore algorithm (the C code for bmBc, suffixes and bmGs, O(mn) worst case, 3n comparisons for an aperiodic pattern, best case O(n/m), and the example x = GCAGAGAG)
  - paper: doi:10.1137/S0097539791195543
    title: R. Cole, Tight bounds on the complexity of the Boyer-Moore string matching algorithm, SIAM Journal on Computing 23(5) (1994), 1075-1091
    locator: the upper bound 3n - 3(n - m + 1)/(m + 2) on the comparisons, the lower bound 3n(1 - o(1)), and the simpler 4n bound
---

The Boyer-Moore algorithm solves [string matching](/string-matching/) by placing the pattern under the text, comparing it from right to left, and then shifting it by the larger of two precomputed shifts, the [bad-character](/bad-character-rule/) shift and the [good-suffix](/good-suffix-rule/) shift. On text over a large alphabet many windows fail at the first comparison on a character that is not in the pattern, so the pattern moves by about $m$ and most text characters are never read. Preprocessing takes $\Theta(m + \sigma)$ time; the search can take $\Theta(nm)$ time when the pattern occurs very often, and with the [Galil rule](/galil-rule/) it is linear in the worst case.

## In plain words

Put the word under the start of the text, but compare its letters from the last one backwards. Two facts let you move the word far.

First, the text letter where the comparison failed must, after the move, sit under the same letter of the word. If that letter is nowhere in the word, the word can jump past it completely.

Second, the letters that did match are now known text. After the move, the word must agree with them too, so it can jump to the next place in the word where the same letters appear, with a different letter in front of them.

Take whichever jump is longer. Both jumps depend only on the word and are computed once, before the search.

## The problem

The input is a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$ over an integer alphabet $\{0, \ldots, \sigma - 1\}$, so that a character indexes the last-occurrence table; the implementation uses a hash map, which accepts any characters. Indices are 0-based. The output is the list of all shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order. Occurrences may overlap. If $m = 0$, all shifts $0, \ldots, n$ are output; if $m > n$, nothing is output.

## The algorithm

$\lambda(c)$ is the last position of $c$ in $P$, or $-1$. $\mathrm{gs}[j]$ is the strong good-suffix shift after a mismatch at $j$, and $\mathrm{gs}[0]$ equals the smallest [period](/string-period/) of $P$. $\mathrm{suff}[i]$ is the length of the longest common suffix of $P[0 \ldots i]$ and $P$, computed in $O(m)$ time like a [Z array](/z-algorithm/) of the reversed pattern.

```pseudo id=main
BOYER-MOORE(T, P)
L1  n ← |T|, m ← |P|
L2  if m = 0 then output 0, 1, …, n and return
L3  λ ← LAST-OCCURRENCE(P), gs ← GOOD-SUFFIX(P)
L4  s ← 0
L5  while s ≤ n − m do
L6      j ← m − 1
L7      while j ≥ 0 and P[j] = T[s + j] do     ▷ right to left
L8          j ← j − 1
L9      if j < 0 then
L10         output s
L11         s ← s + gs[0]                      ▷ the period of P
L12     else s ← s + max(gs[j], j − λ(T[s + j]))

LAST-OCCURRENCE(P)
L13 λ(c) ← −1 for every c; for k ← 0 to m − 1 do λ(P[k]) ← k

GOOD-SUFFIX(P)
L14 suff ← SUFFIXES(P)
L15 gs[j] ← m for 0 ≤ j < m; j ← 0
L16 for i ← m − 1 downto 0 do
L17     if suff[i] = i + 1 then                ▷ P[0 .. i] is a border of P
L18         while j < m − 1 − i do
L19             if gs[j] = m then gs[j] ← m − 1 − i
L20             j ← j + 1
L21 for i ← 0 to m − 2 do                      ▷ reoccurrences of suffixes
L22     gs[m − 1 − suff[i]] ← m − 1 − i
L23 return gs
```

Lines L6 to L8 compare the window from right to left. A full match shifts by the period, the smallest shift that agrees with the matched text. A mismatch at $j$ shifts by the larger of the two rules; the bad-character value $j - \lambda(c)$ can be zero or negative, but $\mathrm{gs}[j] \ge 1$ keeps the shift positive. Lines L14 to L23 are the $O(m)$ computation of the strong good-suffix table explained on the page of the [good-suffix rule](/good-suffix-rule/).

## Example

$P$ = gcagagag ($m = 8$) and $T$ = gcatcgcagagagtatacagtacg ($n = 24$), the example of Charras and Lecroq. The tables are $\lambda$(a) = 6, $\lambda$(c) = 1, $\lambda$(g) = 7, $\lambda$(t) = $-1$, and:

| $j$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $P[j]$ | g | c | a | g | a | g | a | g |
| $\mathrm{gs}[j]$ | 7 | 7 | 7 | 2 | 7 | 4 | 7 | 1 |

The search:

| $s$ | window | mismatch at $j$ | $T[s+j]$ | bad character | good suffix | shift | comparisons |
|---|---|---|---|---|---|---|---|
| 0 | gcatcgca | 7 | a | 1 | 1 | 1 | 1 |
| 1 | catcgcag | 5 | c | 4 | 4 | 4 | 3 |
| 5 | gcagagag | match | | | | 7 | 8 |
| 12 | gtatacag | 5 | c | 4 | 4 | 4 | 3 |
| 16 | acagtacg | 6 | c | 5 | 7 | 7 | 2 |

The next shift would be 23, beyond $n - m = 16$, so the search stops. The output is $[5]$, after 17 character comparisons, against 30 for the [naive method](/naive-string-matching/) on the same input. At $s = 16$, the good-suffix rule wins: the matched suffix g does not reoccur in $P$ with a character other than a before it, so only the border g of $P$ helps, and the shift is $m - 1 = 7$.

## Correctness

Each shift is safe: by the [bad-character rule](/bad-character-rule/), every smaller shift than $j - \lambda(c)$ puts a pattern character other than $c$ under the text character $c$, and by the [good-suffix rule](/good-suffix-rule/), every smaller shift than $\mathrm{gs}[j]$ disagrees with the matched text or repeats the failed character. So the larger of the two skips no occurrence. After a full match, every shift smaller than the period disagrees with the matched text. The windows are tested in increasing order, so the output is the sorted list of valid shifts. The full proof is below.

## Complexity

- **Preprocessing.** $\Theta(m + \sigma)$ time and space for $\lambda$ over an integer alphabet, and $\Theta(m)$ for $\mathrm{suff}$ and $\mathrm{gs}$, since in lines L16 to L20 the pointer $j$ only moves right.
- **Worst case, periodic pattern.** $\Theta(nm)$. For $T = a^n$ and $P = a^m$, every window is a full match costing $m$ comparisons, and the shift is the period 1, so the search makes $(n - m + 1)m$ comparisons. The [Galil rule](/galil-rule/) removes this case and gives $O(n + m)$ time.
- **Worst case, non-periodic pattern.** With the strong good-suffix rule, at most $3n$ comparisons when the smallest period of $P$ exceeds $m/2$ (Cole, 1994), and this is tight up to lower-order terms; Knuth had earlier proved a linear bound when $P$ does not occur. See the [comparison bound](/boyer-moore-comparison-bound/).
- **Best case.** If every window fails at its first comparison on a character not in $P$, each window costs one comparison and shifts by $m$, for $\lceil (n - m + 1)/m \rceil$ comparisons. No search can do better on this input with shifts of at most $m$ after one comparison per window, so the best case is $\Theta(n/m)$ plus the preprocessing.
- **In practice.** On natural-language text and moderately long patterns, the mismatches are mostly bad characters that are rare in $P$, and the number of comparisons is a small fraction of $n$, as Boyer and Moore observed on English text.
- **Space.** $\Theta(m + \sigma)$.

| claim | value |
|---|---|
| preprocessing | $\Theta(m + \sigma)$ |
| worst case, all occurrences | $\Theta(nm)$ |
| worst case with the Galil rule | $O(n + m)$ |
| comparisons, non-periodic $P$ | at most $3n$ |
| best case | $\Theta(n/m)$ comparisons |

## Properties

- **Not online.** The algorithm jumps ahead in the text and compares backwards, so it needs random access to the current window; a stream needs a buffer of $m$ characters.
- **Sublinear.** On favorable inputs it reads only a fraction about $1/m$ of the text, which no left-to-right algorithm can do.
- **Integer or hashed alphabet.** The bad-character table is indexed by characters. The good-suffix table uses only equality tests.
- **Deterministic and in place.** It uses $\Theta(m + \sigma)$ extra memory, independent of $n$.

## Variants and improvements

- **Simpler shifts.** [Horspool](/boyer-moore-horspool/) keeps only a bad-character table on the last window character, and [Quick Search](/quick-search/) uses the character after the window. They are shorter and often faster in practice, with the same $\Theta(nm)$ worst case.
- **Linear worst case.** The [Galil rule](/galil-rule/) stops the comparisons at the part known from the previous occurrence; [Turbo Boyer-Moore](/turbo-boyer-moore/) remembers the last matched factor and makes at most $2n$ comparisons; [Apostolico-Giancarlo](/apostolico-giancarlo/) remembers all matched suffixes, also with $2n$.
- **Extended bad character.** Gusfield's version uses the rightmost occurrence to the left of the mismatch, with a larger table.
- **Factor-based shifts.** [Backward DAWG matching](/backward-dawg-matching/) reads the window from the right with a [suffix automaton](/suffix-automaton/) of the reversed pattern and is optimal on average.
- **Many patterns.** Commentz-Walter, [Set Horspool](/set-horspool/) and [Wu-Manber](/wu-manber/) extend the idea to sets of patterns; see [multiple string matching](/multiple-string-matching/).

## When to use it

Use Boyer-Moore or a variant for long patterns over a large alphabet, such as words in natural-language text or byte strings, when the text is in memory. Search tools such as GNU grep use Boyer-Moore-style skipping for fixed strings. For small alphabets such as DNA, the bad-character shifts are short; [backward DAWG matching](/backward-dawg-matching/) or [Shift-Or](/shift-or/) then do better. For streams or when a guaranteed linear bound matters with a simple code, use [KMP](/knuth-morris-pratt/).

## Pitfalls

- **A negative shift.** The bad-character value $j - \lambda(c)$ is negative when the last $c$ is right of the mismatch. Used alone, it moves the pattern back and loops; take the maximum with $\mathrm{gs}[j]$, or with 1. The test `test_random_against_oracle` runs on many such windows.
- **The shift after a match.** Shifting by $m$ after a full match misses overlapping occurrences; the shift is the period, $\mathrm{gs}[0]$. The test `test_edges` searches $a^4$ in $a^{10}$ and expects 7 occurrences.
- **A wrong good-suffix table.** The preprocessing is easy to get wrong, and a historical version in the literature was incorrect. The test `test_tables_against_definition` compares the table with the definition on all small patterns it draws.
- **Quadratic time on periodic input.** Without the Galil rule, $T = a^n$ and $P = a^m$ take $\Theta(nm)$ time; do not use plain Boyer-Moore where an adversary controls the text.
- **A large table.** An array over a 16-bit or Unicode alphabet costs memory and time to initialize for each pattern; use a hash map or a byte-level search.

## Implementations

## History

Robert S. Boyer and J Strother Moore published the algorithm in 1977, in the same year as [Knuth-Morris-Pratt](/knuth-morris-pratt/). Knuth, in the paper with Morris and Pratt, proved that the algorithm makes $O(n)$ comparisons when the pattern does not occur and gave a linear preprocessing for the good-suffix table, which Rytter later corrected. Galil (1979) added the rule that makes the search linear when the pattern occurs, Guibas and Odlyzko improved the constant, and Cole (1994) proved the tight bound of about $3n$ comparisons. Horspool (1980) and Sunday (1990) published the simplified variants that are most used in practice.

## References
