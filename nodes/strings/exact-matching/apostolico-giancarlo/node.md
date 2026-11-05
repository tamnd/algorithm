---
tag: 7XHZHF
kind: algorithm
slug: apostolico-giancarlo
name: Apostolico-Giancarlo algorithm
aliases:
- Apostolico-Giancarlo Boyer-Moore
area: strings/exact-matching
level: advanced
summary: Boyer-Moore variant that records previous match information to bound the total comparisons linearly.
solves: [string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the alphabet size}
  time: {worst: O(n + m + σ), best: Θ(n/m + m + σ), preprocessing: Θ(m + σ)}
  space: {extra: Θ(m + σ)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [boyer-moore, good-suffix-rule, bad-character-rule, z-algorithm]
see_also: [turbo-boyer-moore, galil-rule, boyer-moore-comparison-bound, knuth-morris-pratt, backward-dawg-matching]
sources:
  - paper: doi:10.1137/0215007
    title: A. Apostolico and R. Giancarlo, The Boyer-Moore-Galil string searching strategies revisited, SIAM Journal on Computing 15(1) (1986), 98-105
    locator: the algorithm with the table of matched suffix lengths and the bound of 2n comparisons
  - paper: doi:10.1016/S0020-0190(97)00107-5
    title: M. Crochemore and T. Lecroq, Tight bounds on the complexity of the Apostolico-Giancarlo algorithm, Information Processing Letters 63(4) (1997), 195-203
    locator: the tight upper bound of 3n/2 text character comparisons and the family of inputs that reaches it
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node16.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Apostolico-Giancarlo algorithm (the four cases, the tables skip and suff, and the C code AG)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 3, Section 3.1 (the Apostolico-Giancarlo variant of Boyer-Moore and its linear bound)
---

The Apostolico-Giancarlo algorithm solves [string matching](/string-matching/) like [Boyer-Moore](/boyer-moore/), comparing the pattern with each window from right to left and shifting by the [good-suffix](/good-suffix-rule/) and [bad-character](/bad-character-rule/) rules, but it records, for each text position where a window ended, how long a suffix of the pattern matched there. When a later window reaches such a position, it compares the recorded length with a table of the pattern and decides in constant time whether to jump over the recorded part, to report a mismatch, or to report an occurrence. Each text character is then compared successfully at most once, so the search makes at most $2n$ comparisons, and Crochemore and Lecroq showed the tight bound $1.5n$.

## In plain words

Boyer-Moore compares the word with the text from its last letter backwards, then slides. It forgets what it read, so on repetitive text it reads the same letters again and again.

This method keeps a note at each text position where a comparison started: "here, the last 5 letters of the word matched". When a later attempt arrives at a noted position, it does not read those letters again. It knows, from a table made once for the word, how far back the word matches its own end at this place. Comparing the two lengths tells it at once whether the noted letters all match, or where the first difference must be. Then it continues past them, or stops.

So every letter of the text is matched at most once, and the work stays proportional to the length of the text.

## The problem

The input is a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$ over an integer alphabet $\{0, \ldots, \sigma - 1\}$, since the bad-character table is indexed by characters; the implementation uses a dictionary, which works for any hashable characters. Indices are 0-based. The output is every shift $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order. Occurrences may overlap. If $m = 0$, every shift $0, \ldots, n$ is output, and if $m > n$, nothing is output.

## The algorithm

The pattern tables are those of Boyer-Moore. $\mathrm{suff}[i]$, for $0 \le i < m$, is the length of the longest common suffix of $P[0 \ldots i]$ and $P$; it is the [Z-array](/z-algorithm/) of the reversed pattern, read backwards. $\mathrm{gs}[i]$ is the strong good-suffix shift, computed from $\mathrm{suff}$, and $\mathrm{gs}[0]$ is the smallest period of $P$. $\lambda(c)$ is the last position of $c$ in $P$, or $-1$.

The text table is $\mathrm{skip}[t]$: after the window that ends at position $t$ has been tested, $\mathrm{skip}[t]$ is the length of the longest suffix of $P$ that ends at $T[t]$ (it is $m$ for an occurrence). Positions never used as a window end hold 0. Only the $m$ positions of the current window are ever read, so $\mathrm{skip}$ is stored in an array of size $m$ indexed by $t \bmod m$, and the entries that leave the window are cleared at each shift.

During the right-to-left scan at window $s$, suppose the scan is at pattern position $i$, the text matches $P[i+1 \ldots m-1]$ so far, and $k = \mathrm{skip}[s + i] > 0$, $h = \mathrm{suff}[i]$. The text has a suffix of $P$ of length exactly $k$ ending at $s + i$, and $P[0 \ldots i]$ has one of length exactly $h$. Four cases follow.

- $k > h$ and $h = i + 1$: the text matches the whole prefix $P[0 \ldots i]$, so the window is an occurrence.
- $k > h$ and $h \le i$: the text matches $P[i-h+1 \ldots i]$, and the mismatch is at $i - h$, where the text has $P[m-1-h] \ne P[i-h]$.
- $k < h$: the text matches $P[i-k+1 \ldots i]$, and the mismatch is at $i - k$, where $P$ has $P[m-1-k]$ but the text does not.
- $k = h$: the text matches $P[i-k+1 \ldots i]$, and nothing is known about position $i - k$, so the scan jumps there and goes on.

```pseudo id=main
APOSTOLICO-GIANCARLO(T, P)
L1  n ← |T|, m ← |P|
L2  if m = 0 then output 0, 1, …, n and return
L3  suff ← SUFFIXES(P), gs ← GOOD-SUFFIX(P), λ ← LAST-OCCURRENCE(P)
L4  skip[t] ← 0 for all t; s ← 0
L5  while s ≤ n − m do
L6      i ← m − 1
L7      while i ≥ 0 do
L8          k ← skip[s + i], h ← suff[i]
L9          if k > 0 then
L10             if k > h then (if h = i + 1 then i ← −1 else i ← i − h); exit the loop
L11             i ← i − k; if k < h then exit the loop          ▷ k = h: jump and go on
L12         else if P[i] = T[s + i] then i ← i − 1 else exit the loop
L13     if i < 0 then output s; skip[s + m − 1] ← m; shift ← gs[0]
L14     else skip[s + m − 1] ← m − 1 − i; shift ← max(gs[i], i − λ(T[s + i]))
L15     skip[t] ← 0 for s ≤ t < s + min(shift, m)              ▷ positions leaving the window
L16     s ← s + shift
```

When the loop of line L7 ends with $i \ge 0$, position $i$ is a mismatch, either compared at line L12 or deduced at lines L10 and L11, and the text matches $P[i+1 \ldots m-1]$. So line L14 stores the exact length of the matched suffix, and the shift is the Boyer-Moore shift for a mismatch at $i$ on the text character $T[s+i]$.

## Example

Search for $P$ = gcagagag in $T$ = gcatcgcagagagtatacagtacg, with $n = 24$ and $m = 8$, the example used on the pages of Boyer-Moore and Turbo-BM. The tables are $\mathrm{suff}$ = 1 0 0 2 0 4 0 8 and $\mathrm{gs}$ = 7 7 7 2 7 4 7 1, for $i = 0, \ldots, 7$, and $\lambda$(a) = 6, $\lambda$(c) = 1, $\lambda$(g) = 7.

| $s$ | scan | comparisons | stored | shift |
|---|---|---|---|---|
| 0 | mismatch at $i = 7$ | 1 | $\mathrm{skip}[7] = 0$ | $\max(1, 1) = 1$ |
| 1 | match $i = 7, 6$, mismatch at $i = 5$ | 3 | $\mathrm{skip}[8] = 2$ | $\max(4, 4) = 4$ |
| 5 | match $i = 7, 6, 5, 4$; at $i = 3$, $k = \mathrm{skip}[8] = 2 = h$, jump to $i = 1$; match $i = 1, 0$ | 6 | $\mathrm{skip}[12] = 8$ | $\mathrm{gs}[0] = 7$ |
| 12 | match $i = 7, 6$, mismatch at $i = 5$ | 3 | $\mathrm{skip}[19] = 2$ | $\max(4, 4) = 4$ |
| 16 | match $i = 7$, mismatch at $i = 6$ | 2 | $\mathrm{skip}[23] = 1$ | $\max(7, 5) = 7$ |

The output is the single shift 5, after 15 comparisons, against 17 for Boyer-Moore. At $s = 5$ the note left by the window at $s = 1$ says that $T[7 \ldots 8]$ = ag is a suffix of $P$ of length exactly 2, and $\mathrm{suff}[3] = 2$ says the same of $P[2 \ldots 3]$, so the scan jumps over both characters.

A periodic example: $P$ = aabaab in $T$ = abaabaabaabaab, with $\mathrm{suff}$ = 0 0 3 0 0 6. The window at $s = 2$ is an occurrence after 6 comparisons, and $\mathrm{skip}[7] = 6$. At $s = 5$ the scan matches $P[5], P[4], P[3]$ and reaches $i = 2$, text position 7, with $k = 6 > h = \mathrm{suff}[2] = 3 = i + 1$: an occurrence, found with 3 comparisons. The same happens at $s = 8$. The output is 2, 5, 8 with 14 comparisons.

## Correctness

The key fact is that $\mathrm{skip}$ stores exact lengths: when a window is tested, the loop of line L7 keeps the invariant that the text matches $P[i+1 \ldots m-1]$, and it stops at the first position where it does not. The four cases each follow from comparing two exact suffix lengths ending at the same place: if a text factor and the prefix $P[0 \ldots i]$ both end with a suffix of $P$, the shorter of the two lengths is the length of their common part, and if the lengths differ, the next characters differ. The shifts are those of Boyer-Moore, which skip no occurrence. The full proof is below.

## Complexity

- **Preprocessing.** $\Theta(m + \sigma)$ time and space for the three pattern tables, as for Boyer-Moore.
- **Comparisons.** A comparison at line L12 that succeeds is at a text position not covered by any note. After the window, that position lies inside the factor recorded at the window end, and later scans jump over it or stop before it. So each text position is matched successfully at most once, and there is at most one failed comparison per window. Since there are at most $n - m + 1$ windows, the search makes fewer than $2n$ comparisons, the bound of Apostolico and Giancarlo. Crochemore and Lecroq refined the analysis to at most $1.5n$ comparisons and gave a family of inputs that reaches this bound.
- **Time.** Each step of the inner loop either makes a comparison or uses a note; the cases of line L10 and the case $k < h$ end the scan, so only the jumps with $k = h$ can repeat within a window, and Apostolico and Giancarlo show that the total work of the search is $O(n)$. Clearing at line L15 costs $\min(\mathit{shift}, m)$ per window, $O(n)$ in total. The search is $O(n)$ in the worst case, including the version that reports all occurrences.
- **Best case.** $\Theta(n/m)$ comparisons, as for Boyer-Moore, when each window fails at once on a character not in $P$.
- **Space.** $\Theta(m + \sigma)$: the pattern tables and $m$ entries of $\mathrm{skip}$.

| claim | value |
|---|---|
| preprocessing | $\Theta(m + \sigma)$ |
| comparisons, original bound | at most $2n$ |
| comparisons, tight bound | at most $1.5n$ |
| search time, worst case | $O(n)$ |
| best case | $\Theta(n/m)$ comparisons |

The tests `test_exhaustive_binary` and `test_random_against_oracle` check the bound of $1.5n$ comparisons on every input they run; the input $T = a^{1000}$, $P = a^{10}$ takes exactly 1000 comparisons, since each new window needs one comparison and then finds the note of the previous occurrence.

## Properties

- **Linear with all occurrences.** Unlike plain Boyer-Moore, it stays linear when the pattern occurs many times, without the special case of the [Galil rule](/galil-rule/).
- **Sublinear on average.** It keeps the long shifts of Boyer-Moore, so it reads about $n/m$ characters on favorable text.
- **Not online.** It needs random access to the current window.
- **Integer alphabet.** Only the bad-character table depends on the alphabet; without it, equality tests suffice.

## Variants and improvements

- **Turbo-BM.** [Turbo-BM](/turbo-boyer-moore/) remembers only the last matched factor, with two integers instead of the table $\mathrm{skip}$, and makes at most $2n$ comparisons.
- **A size-$n$ skip table.** The original description keeps $\mathrm{skip}$ for every text position. Indexing by $t \bmod m$ keeps the memory at $\Theta(m)$; the C code of Charras and Lecroq instead copies the table by $\mathit{shift}$ entries at each window, which costs $\Theta(m)$ per window.
- **Fewer comparisons.** Crochemore and Lecroq give a slightly improved version in the same paper, and Crochemore, Hancart and Lecroq later gave a presentation that avoids the extra preprocessing, with the same $1.5n$ bound (Journal of Discrete Algorithms, 2003).
- **Galil's rule.** The [Galil rule](/galil-rule/) gives linear time after occurrences only; the bound for the version without occurrences is [Cole's 3n](/boyer-moore-comparison-bound/).

## When to use it

Use Apostolico-Giancarlo when Boyer-Moore's average speed is wanted with a guaranteed linear bound, for example on long patterns that may occur many times or on repetitive text. When memory per pattern matters more than the constant in the bound, [Turbo-BM](/turbo-boyer-moore/) is simpler. For a stream or a small alphabet, use [KMP](/knuth-morris-pratt/) or [backward DAWG matching](/backward-dawg-matching/).

## Pitfalls

- **Using a note that is not exact.** The four cases need $\mathrm{skip}$ to be the exact length of the matched suffix, not a lower bound; storing $m - 1 - i$ with $i$ from a deduced mismatch is exact, but storing a partial value from a scan cut short is not. The test `test_random_against_oracle` compares the output with the naive search.
- **Stale notes.** With an array indexed by $t \bmod m$, an entry from a position that left the window must be cleared before a new position with the same residue is read. Forgetting line L15 gives wrong jumps. The test `test_exhaustive_binary` covers every binary text up to length 8.
- **Off by one in the occurrence case.** The occurrence case needs $h = i + 1$, the whole prefix $P[0 \ldots i]$; with $h = i$ the scan reports windows that differ at position 0. The test `test_edges` searches baaa in $a^{10}$ and expects nothing.
- **A wrong suffix table.** The table $\mathrm{suff}$ is used twice, for the good-suffix shift and for the cases. The test `test_tables` checks it on gcagagag.

## Implementations

## History

Apostolico and Giancarlo presented the algorithm in 1986 in "The Boyer-Moore-Galil string searching strategies revisited", as a way to make Boyer-Moore linear with all occurrences and a simple analysis, after the periodicity rule of Galil (1979). They proved a bound of $2n$ comparisons. Crochemore and Lecroq proved the tight bound $1.5n$ in 1997, after a 1996 report at the University of Rouen, and Charras and Lecroq's catalog of exact string-matching algorithms gave the C code that most later implementations follow. Gusfield's textbook presents the algorithm in Chapter 3 as the linear-time version of Boyer-Moore.

## References
