---
tag: RFB4V2
kind: algorithm
slug: boyer-moore-horspool
name: Boyer-Moore-Horspool algorithm
aliases:
- Horspool algorithm
- BMH
area: strings/exact-matching
level: core
summary: Simplified Boyer-Moore using only the bad-character rule on the last text character of the window.
solves: [string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the alphabet size}
  time: {worst: Θ(n m), best: Θ(n/m + m + σ), preprocessing: Θ(m + σ)}
  space: {extra: Θ(σ)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [bad-character-rule, string-matching, naive-string-matching]
see_also: [boyer-moore, quick-search, set-horspool, wu-manber, shift-or, backward-dawg-matching]
sources:
  - paper: doi:10.1002/spe.4380100608
    title: R. N. Horspool, Practical fast searching in strings, Software, Practice and Experience 10(6) (1980), 501-506
    locator: the simplified Boyer-Moore algorithm that keeps only the table of the first rule and indexes it by the text character aligned with the last pattern character
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node18.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Horspool algorithm (preprocessing in O(m + σ), worst case O(mn), the example with x = GCAGAGAG)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 2, String matching, the suffix-based approach (the Horspool algorithm and its practical performance)
---

The Boyer-Moore-Horspool algorithm solves [string matching](/string-matching/) by testing each window of the text and then shifting the pattern by a [bad-character](/bad-character-rule/) shift computed from one character only: the text character under the last pattern position. Its table has one entry per character and is built in $\Theta(m + \sigma)$ time. It drops the [good-suffix rule](/good-suffix-rule/) of [Boyer-Moore](/boyer-moore/), so its worst case is $\Theta(nm)$, but on natural text and large alphabets it is as fast or faster, and it is one of the most used exact matchers in practice.

## In plain words

Look at the window of text under the word. Check whether it equals the word, in any order you like. Then, whatever happened, look at the last text letter of the window and ask where that letter appears in the word, not counting the word's last letter. Slide the word so that the rightmost such copy comes under it. If the letter does not appear, slide the whole word past it.

The jump only depends on one text letter, so a table with one entry per letter holds all jumps. With many different letters and a long word, most jumps are almost the full length of the word.

## The problem

The input is a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$ over an integer alphabet $\{0, \ldots, \sigma - 1\}$, so a character indexes the shift table; the implementation uses a hash map and accepts any characters. Indices are 0-based. The output is the list of all shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order. Occurrences may overlap. If $m = 0$, all shifts $0, \ldots, n$ are output; if $m > n$, nothing is output.

## The algorithm

The shift of a character $c$ is the distance from its rightmost occurrence in $P[0 \ldots m-2]$ to the last position $m - 1$, or $m$ if $c$ does not occur there:

$$\mathrm{shift}[c] = \min\big(\{m\} \cup \{\, m - 1 - k : 0 \le k \le m - 2,\ P[k] = c \,\}\big).$$

```pseudo id=main
HORSPOOL(T, P)
L1  n ← |T|, m ← |P|
L2  if m = 0 then output 0, 1, …, n and return
L3  shift[c] ← m for every character c
L4  for k ← 0 to m − 2 do shift[P[k]] ← m − 1 − k
L5  s ← 0
L6  while s ≤ n − m do
L7      j ← m − 1
L8      while j ≥ 0 and P[j] = T[s + j] do j ← j − 1
L9      if j < 0 then output s
L10     s ← s + shift[T[s + m − 1]]
```

Line L4 runs left to right, so a later occurrence overwrites an earlier one and the table keeps the rightmost. It stops at $m - 2$: the last pattern character is excluded, so every shift is at least 1. Lines L7 and L8 compare the window from right to left; Horspool's paper and many libraries compare the last character first and then the rest in any order, which does not change the shifts. Line L10 shifts by the table entry of the last window character, whether the window matched or not.

## Example

$P$ = gcagagag ($m = 8$) and $T$ = gcatcgcagagagtatacagtacg ($n = 24$), the example of Charras and Lecroq. The shift table is shift[a] = 1, shift[c] = 6, shift[g] = 2 and shift[t] = 8.

| $s$ | window | result | comparisons | $T[s + 7]$ | shift |
|---|---|---|---|---|---|
| 0 | gcatcgca | mismatch at 7 | 1 | a | 1 |
| 1 | catcgcag | mismatch at 5 | 3 | g | 2 |
| 3 | tcgcagag | mismatch at 3 | 5 | g | 2 |
| 5 | gcagagag | match | 8 | g | 2 |
| 7 | agagagta | mismatch at 7 | 1 | a | 1 |
| 8 | gagagtat | mismatch at 7 | 1 | t | 8 |
| 16 | acagtacg | mismatch at 6 | 2 | g | 2 |

The next shift is 18 > 16, so the search stops with the output $[5]$, after 21 comparisons in this right-to-left order. At $s = 8$, the last window character t does not occur in $P$, and the pattern jumps by its full length. At $s = 1$, [Boyer-Moore](/boyer-moore/) shifts by 4 because it uses the mismatched character c, while Horspool uses the last character g and shifts by 2.

## Correctness

After testing the window at $s$, let $c = T[s + m - 1]$. A valid shift $s + d$ with $1 \le d \le m - 1$ puts $P[m - 1 - d]$ under this text character, so $P[m - 1 - d] = c$ with $0 \le m - 1 - d \le m - 2$, which means $d \ge \mathrm{shift}[c]$. So no valid shift lies strictly between $s$ and $s + \mathrm{shift}[c]$, and the shift is at least 1, so the search visits all candidate windows in increasing order. The full proof is below.

## Complexity

- **Preprocessing.** $\Theta(m + \sigma)$ time for the table over an integer alphabet, and $\Theta(\sigma)$ space; with a hash map, $O(m)$ expected time and space.
- **Worst case.** $\Theta(nm)$. For $T = a^n$ and $P = b\,a^{m-1}$, each window compares $m$ characters and fails on the first, and $\mathrm{shift}[a] = 1$, so the search makes $(n - m + 1)m$ comparisons without finding anything. $P = a^m$ gives the same with every window a match.
- **Best case.** If the last window character never occurs in $P[0 \ldots m-2]$ and the first comparison fails, each window costs 1 comparison and shifts by $m$, about $n/m$ comparisons in total; since a shift is at most $m$, at least $\lfloor (n - m)/m \rfloor + 1$ windows are tested on every input, so the best case is $\Theta(n/m)$ plus the preprocessing.
- **Average.** On random text, each window costs $O(1)$ expected comparisons for $\sigma \ge 2$, as for the [naive method](/naive-string-matching/), and the expected shift grows with $m$ and $\sigma$ up to $m$, so the time in practice is close to $n$ divided by the average shift.

| claim | value |
|---|---|
| preprocessing | $\Theta(m + \sigma)$ |
| worst case | $\Theta(nm)$ |
| best case | $\Theta(n/m)$ comparisons |
| extra space | $\Theta(\sigma)$ |

## Properties

- **Not online.** It jumps ahead in the text, so it needs the current window in memory.
- **Sublinear on favorable input.** It can skip most of the text without reading it.
- **One table, one lookup.** The shift does not depend on where the mismatch happened, so the inner comparison loop can be any fast equality test, such as `memcmp`.
- **Integer alphabet.** The table is indexed by characters; for large alphabets, use a hash map or work on bytes.

## Variants and improvements

- **Quick Search.** Sunday's [Quick Search](/quick-search/) uses the character after the window, $T[s + m]$, with a table over all of $P$, and can shift by $m + 1$.
- **Boyer-Moore.** [Boyer-Moore](/boyer-moore/) adds the [good-suffix rule](/good-suffix-rule/) and uses the mismatched character; more preprocessing, fewer comparisons on periodic patterns.
- **Two characters.** Using the pair $T[s + m - 2 \ldots s + m - 1]$ as the index (a table of size $\sigma^2$) gives longer shifts on small alphabets such as DNA.
- **Many patterns.** [Set Horspool](/set-horspool/) uses a trie of reversed patterns with the same shift idea, and [Wu-Manber](/wu-manber/) uses blocks of characters.
- **Guaranteed linear time.** For adversarial input, run [KMP](/knuth-morris-pratt/) or the [two-way algorithm](/two-way-string-matching/) instead.

## When to use it

Use Horspool when you want a short and fast matcher for one pattern in text held in memory, with a moderate or large alphabet and patterns of a few characters or more: English text, source code, byte strings. It is the usual choice of library `memmem`-style functions that do not need worst-case guarantees. For tiny alphabets, prefer [backward DAWG matching](/backward-dawg-matching/) or [Shift-Or](/shift-or/); for adversarial input, an algorithm with a linear worst case.

## Pitfalls

- **Including the last character.** If line L4 runs up to $m - 1$, the last pattern character gets the shift 0, and the search loops forever on a window that ends with that character. The test `test_last_character_excluded` checks that $P$ = ab has no entry for b.
- **Using the mismatched character.** The shift must be indexed by $T[s + m - 1]$, not by the character where the comparison failed; with the latter, the table needs the formula of the [bad-character rule](/bad-character-rule/) and can skip occurrences.
- **Not shifting after a match.** The shift of line L10 applies after a match too; shifting by $m$ there loses overlapping occurrences. The test `test_edges` searches $a^4$ in $a^{10}$.
- **Quadratic input.** Repetitive text such as long runs of one byte makes it slow; do not use it where an adversary controls the text.

## Implementations

## History

R. Nigel Horspool published the algorithm in 1980 in "Practical fast searching in strings", observing that the bad-character table of [Boyer-Moore](/boyer-moore/), indexed by the last character of the window, gives most of the speed of the full algorithm with much less code. Sunday's Quick Search (1990) and many later variants, studied in detail by Navarro and Raffinot and by Charras and Lecroq, refine the same idea.

## References
