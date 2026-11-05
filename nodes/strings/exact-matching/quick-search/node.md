---
tag: GYWS8F
kind: algorithm
slug: quick-search
name: Quick Search algorithm
aliases:
- Sunday algorithm
area: strings/exact-matching
level: core
summary: Boyer-Moore variant that uses the character just after the window for the shift.
solves: [string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the alphabet size}
  time: {worst: Θ(n m), best: Θ(n/m + m + σ), preprocessing: Θ(m + σ)}
  space: {extra: Θ(σ)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [bad-character-rule, string-matching, naive-string-matching]
see_also: [boyer-moore-horspool, boyer-moore, shift-or, backward-dawg-matching]
sources:
  - paper: doi:10.1145/79173.79184
    title: D. M. Sunday, A very fast substring search algorithm, Communications of the ACM 33(8) (1990), 132-142
    locator: the Quick Search algorithm (the shift table indexed by the character following the window), and the Maximal Shift and Optimal Mismatch variants
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node19.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Quick Search algorithm (the table qsBc, preprocessing in O(m + σ), worst case O(mn), the example with x = GCAGAGAG)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 2, String matching, the suffix-based approach (Horspool-type shifts and their variants)
---

The Quick Search algorithm, published by Daniel Sunday in 1990, solves [string matching](/string-matching/) by testing each window and then shifting by a [bad-character](/bad-character-rule/) shift indexed by the text character just after the window. That character must be covered by the next possible occurrence, so the shift can be $m + 1$, one more than in [Horspool](/boyer-moore-horspool/), and the table may include the last pattern character. The worst case is $\Theta(nm)$, but the code is tiny and fast on large alphabets and short patterns.

## In plain words

Test the window of text under the word, comparing letters in any order. Then look at the text letter just after the window. Any next match must cover that letter, so find the rightmost copy of it in the word and slide the word to put that copy under it. If the letter is not in the word, the word can jump completely past it, one letter more than its own length.

As in Horspool's method, the jump depends on one text letter only, so a table with one entry per letter holds all jumps.

## The problem

The input is a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$ over an integer alphabet $\{0, \ldots, \sigma - 1\}$, so a character indexes the shift table; the implementation uses a hash map and accepts any characters. Indices are 0-based. The output is the list of all shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order. Occurrences may overlap. If $m = 0$, all shifts $0, \ldots, n$ are output; if $m > n$, nothing is output.

## The algorithm

$$\mathrm{qs}[c] = \min\big(\{m + 1\} \cup \{\, m - k : 0 \le k \le m - 1,\ P[k] = c \,\}\big),$$

the distance from the rightmost $c$ in $P$ to the position just after the pattern.

```pseudo id=main
QUICK-SEARCH(T, P)
L1  n ← |T|, m ← |P|
L2  if m = 0 then output 0, 1, …, n and return
L3  qs[c] ← m + 1 for every character c
L4  for k ← 0 to m − 1 do qs[P[k]] ← m − k
L5  s ← 0
L6  while s ≤ n − m do
L7      j ← 0
L8      while j < m and P[j] = T[s + j] do j ← j + 1
L9      if j = m then output s
L10     if s + m = n then stop               ▷ no character after the last window
L11     s ← s + qs[T[s + m]]
```

Line L4 keeps the rightmost occurrence of each character, since later positions overwrite earlier ones. Lines L7 and L8 compare from left to right, as in Sunday's Quick Search; since the shift does not depend on the comparisons, any order works, and Sunday's other two variants choose the order by character frequency or by shift length. Line L10 handles the last window, after which no text character exists.

## Example

$P$ = gcagagag ($m = 8$) and $T$ = gcatcgcagagagtatacagtacg ($n = 24$), the example of Charras and Lecroq. The table is qs[a] = 2, qs[c] = 7, qs[g] = 1 and qs[t] = 9.

| $s$ | window | result | comparisons | $T[s + 8]$ | shift |
|---|---|---|---|---|---|
| 0 | gcatcgca | mismatch at 3 | 4 | g | 1 |
| 1 | catcgcag | mismatch at 0 | 1 | a | 2 |
| 3 | tcgcagag | mismatch at 0 | 1 | a | 2 |
| 5 | gcagagag | match | 8 | t | 9 |
| 14 | atacagta | mismatch at 0 | 1 | c | 7 |

The next shift is 21 > 16, so the search stops. The output is $[5]$, after 15 comparisons, against 21 for [Horspool](/boyer-moore-horspool/) and 17 for [Boyer-Moore](/boyer-moore/) on the same input. After the match at $s = 5$, the character after the window is t, which is not in $P$, so the pattern jumps by $m + 1 = 9$.

## Correctness

After testing the window at $s < n - m$, let $c = T[s + m]$. Every shift $s + d$ with $1 \le d \le m$ covers the text position $s + m$ with the pattern position $m - d$, so a valid shift needs $P[m - d] = c$, that is $d \ge \mathrm{qs}[c]$. So no valid shift is skipped, every shift is at least 1, and the windows are tested in increasing order. The full proof is below.

## Complexity

- **Preprocessing.** $\Theta(m + \sigma)$ time over an integer alphabet, $\Theta(\sigma)$ space.
- **Worst case.** $\Theta(nm)$: for $T = a^n$ and $P = a^m$, every window costs $m$ comparisons and $\mathrm{qs}[a] = 1$. For no occurrence, $P = a^{m-1}b$ and $T = a^n$ cost $m$ comparisons per window, with shift $\mathrm{qs}[a] = 2$, so about $nm/2$ comparisons.
- **Best case.** If the first comparison of each window fails and the next character is not in $P$, each window costs one comparison and the shift is $m + 1$, for about $n/(m+1)$ comparisons; at least $\lfloor (n-m)/(m+1) \rfloor + 1$ windows are tested on every input, so the best case is $\Theta(n/m)$ plus the preprocessing.
- **Space.** $\Theta(\sigma)$ for the table.

| claim | value |
|---|---|
| preprocessing | $\Theta(m + \sigma)$ |
| worst case | $\Theta(nm)$ |
| best case | $\Theta(n/m)$ comparisons |
| largest shift | $m + 1$ |

## Properties

- **Not online.** It looks one character beyond the window and jumps ahead.
- **Any comparison order.** The shift depends only on $T[s + m]$, so the window test can be a `memcmp` or a comparison in an order chosen for the data.
- **Integer alphabet.** The table is indexed by characters.
- **Very short code.** One table, one loop; this is the main reason for its popularity.

## Variants and improvements

- **Maximal Shift and Optimal Mismatch.** Sunday's two other algorithms, in the same paper, compare the pattern characters in an order chosen to maximize the shift or to test the rarest characters first.
- **Horspool.** [Horspool](/boyer-moore-horspool/) uses the last character of the window instead; its shifts are at most $m$, but it does not read past the window.
- **Two-character shifts.** Using the pair $T[s+m \ldots s+m+1]$ gives longer shifts on small alphabets, as in the Berry-Ravindran variant.
- **Bit-parallel and factor methods.** For small alphabets, [Shift-Or](/shift-or/) and [backward DAWG matching](/backward-dawg-matching/) are usually faster.

## When to use it

Use Quick Search for short patterns over a large alphabet when the text is in memory and the input is not adversarial: it is among the simplest fast matchers. Avoid it for highly repetitive text or tiny alphabets, where its shifts are short, and where a guaranteed linear bound is required.

## Pitfalls

- **Reading past the text.** The character $T[s + m]$ does not exist for the last window $s = n - m$. Line L10 stops there; without it, an implementation reads $T[n]$. The test `test_window_at_the_end` has an occurrence in the last window.
- **The default shift.** A character absent from $P$ shifts by $m + 1$, not $m$; using $m$ is safe but loses the advantage.
- **Excluding the last pattern character.** Unlike Horspool, the table must include $P[m-1]$, which gets the shift 1. Copying the Horspool loop up to $m - 2$ gives wrong shifts that skip occurrences. The test `test_random_against_oracle` catches this.
- **Shift after a match.** The table shift also applies after a match, which keeps overlapping occurrences. The test `test_edges` searches $a^4$ in $a^{10}$.

## Implementations

## History

Daniel M. Sunday described Quick Search, together with the Maximal Shift and Optimal Mismatch algorithms, in "A very fast substring search algorithm" in Communications of the ACM in 1990. It became a standard in surveys of exact string matching, such as the handbook of Charras and Lecroq, as one of the fastest simple algorithms in practice.

## References
