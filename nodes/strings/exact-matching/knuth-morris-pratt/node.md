---
tag: F0V6W1
kind: algorithm
slug: knuth-morris-pratt
name: Knuth-Morris-Pratt algorithm
aliases:
- KMP
- Knuth-Morris-Pratt string search
area: strings/exact-matching
level: core
summary: Linear-time matching using the prefix function; the text pointer never moves backward.
solves: [string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [prefix-function, string-matching, border, potential-method]
see_also: [morris-pratt, naive-string-matching, string-matching-automaton, z-algorithm, aho-corasick, boyer-moore]
sources:
  - paper: doi:10.1137/0206024
    title: D. E. Knuth, J. H. Morris and V. R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2) (1977), 323-350
    locator: the algorithm with the next table, its analysis (the linear bound and the delay bound with the golden ratio), and the historical remarks
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.4, The Knuth-Morris-Pratt algorithm
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 2.3, The Knuth-Morris-Pratt algorithm (the values sp and sp'), and Section 2.4, Real-time string matching
  - url: https://cp-algorithms.com/string/prefix-function.html
    title: CP-Algorithms, Prefix function. Knuth-Morris-Pratt algorithm
    locator: the section on the search for a substring
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node8.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Knuth-Morris-Pratt algorithm (the table kmpNext and the delay bound)
---

The Knuth-Morris-Pratt algorithm (KMP) solves [string matching](/string-matching/) in $\Theta(n + m)$ time for a text of length $n$ and a pattern of length $m$, with at most $2n$ character comparisons in the search. It reads the text once from left to right and never moves back. After a mismatch it uses a table computed from the [prefix function](/prefix-function/) of the pattern to keep the longest part of the match that can still lead to an occurrence. It was the first linear-time algorithm for the problem on a general alphabet, and its failure function is the base of [Aho-Corasick](/aho-corasick/) and many other string algorithms.

## In plain words

Read the text one letter at a time, and keep track of how much of the word you have matched so far. When the next letter fits, the match grows by one. When the whole word fits, report it.

When a letter does not fit, the naive method would go back in the text. KMP does not. The matched part is a known piece of the word. Before the search, KMP has worked out, for each such piece, the longest end of it that is also a start of the word. That end is the best match you can keep, so KMP falls back to it and tries the same text letter again. It also skips fall-backs that would compare the text letter with the same pattern letter that just failed.

## The problem

The input is a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$ over a general alphabet: only equality tests between characters are used. Indices are 0-based. The output is the list of all shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order. Occurrences may overlap. If $m = 0$, all shifts $0, \ldots, n$ are output; if $m > n$, nothing is output. This is the [string matching](/string-matching/) problem.

## The algorithm

Let $\pi$ be the [prefix function](/prefix-function/) of $P$: $\pi[q]$ is the length of the longest proper border of $P[0 \ldots q]$. KMP uses the *strong failure table* $\mathrm{nxt}[0 \ldots m]$:

- for $0 \le q < m$, $\mathrm{nxt}[q]$ is the largest $k < q$ such that $P[0 \ldots k-1]$ is a border of $P[0 \ldots q-1]$ and $P[k] \ne P[q]$, or $-1$ if no such $k$ exists;
- $\mathrm{nxt}[m] = \pi[m-1]$, the length of the longest proper border of $P$.

The variable $q$ is the number of pattern characters matched so far; the value $-1$ means "no match is possible, move to the next text character".

```pseudo id=main
KMP-MATCHER(T, P)
L1  n ← |T|, m ← |P|
L2  if m = 0 then output 0, 1, …, n and return
L3  nxt ← COMPUTE-NEXT(P)
L4  q ← 0                                ▷ P[0 .. q − 1] = T[i − q .. i − 1]
L5  for i ← 0 to n − 1 do
L6      while q ≥ 0 and P[q] ≠ T[i] do
L7          q ← nxt[q]                   ▷ fall back to a shorter border
L8      q ← q + 1
L9      if q = m then
L10         output i − m + 1
L11         q ← nxt[m]                   ▷ keep the longest border of P

COMPUTE-NEXT(P)                          ▷ m ≥ 1
L12 π ← COMPUTE-PREFIX-FUNCTION(P)
L13 nxt[0] ← −1
L14 for q ← 1 to m − 1 do
L15     k ← π[q − 1]                     ▷ longest proper border of P[0 .. q − 1]
L16     if P[k] = P[q] then nxt[q] ← nxt[k] else nxt[q] ← k
L17 nxt[m] ← π[m − 1]
L18 return nxt
```

The search loop of lines L5 to L11 handles one text character per iteration. Line L6 compares $T[i]$ with the next pattern character. On a mismatch, line L7 moves to a shorter border of the matched part, and the test repeats with the same $T[i]$. When $q$ reaches $-1$, no border can be extended, and line L8 makes $q = 0$. After a full match, line L11 keeps the longest border of $P$, so overlapping occurrences are found.

COMPUTE-NEXT derives the strong table from $\pi$, which COMPUTE-PREFIX-FUNCTION builds in $O(m)$ time as shown on the [prefix function](/prefix-function/) page. The borders of $P[0 \ldots q-1]$ are $k = \pi[q-1]$ and the borders of $P[0 \ldots k-1]$. If $P[k] \ne P[q]$, the longest border already qualifies. If $P[k] = P[q]$, that border is useless after a mismatch at $P[q]$, and the best qualifying border is the one for $k$, which is $\mathrm{nxt}[k]$, because the character to avoid is the same.

## Example

Search for $P$ = abacabab ($m = 8$) in $T$ = abacabcabacababa ($n = 16$).

| $q$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $P[q]$ | a | b | a | c | a | b | a | b | |
| $\pi[q]$ | 0 | 0 | 1 | 0 | 1 | 2 | 3 | 2 | |
| $\mathrm{nxt}[q]$ | $-1$ | 0 | $-1$ | 1 | $-1$ | 0 | $-1$ | 3 | 2 |

For example $\mathrm{nxt}[6] = -1$: the borders of abacab are ab and the empty string, and both are followed by a, which is $P[6]$ itself, so no border helps after a mismatch at $P[6]$.

The trace lists the values that $q$ takes in the loop of line L6 for each text character.

| $i$ | $T[i]$ | values of $q$ at line L6 | $q$ after L8 | output |
|---|---|---|---|---|
| 0 to 5 | abacab | 0, 1, 2, 3, 4, 5 (one each) | 1 to 6 | |
| 6 | c | 6, then $-1$ | 0 | |
| 7 to 13 | abacaba | 0, 1, ..., 6 (one each) | 1 to 7 | |
| 14 | b | 7 | 8, then $\mathrm{nxt}[8] = 2$ | 7 |
| 15 | a | 2 | 3 | |

At $i = 6$, the comparison of $P[6]$ = a with c fails, and $\mathrm{nxt}[6] = -1$ ends the loop at once. The weaker table of [Morris-Pratt](/morris-pratt/) would try $q = \pi[5] = 2$ and $q = \pi[1] = 0$ first, comparing a with c twice more. The search makes 16 comparisons here, against 18 for Morris-Pratt, and reports the single occurrence at shift 7.

## Correctness

The search loop keeps this [loop invariant](/loop-invariant/): at the start of the iteration for $i$, $0 \le q < m$, and $q$ is the length of the longest prefix of $P$ shorter than $m$ that is a suffix of $T[0 \ldots i-1]$; and the shifts already output are exactly the occurrences that end before position $i$. Each fall-back of line L7 skips only borders that cannot be extended by $T[i]$, by the definition of $\mathrm{nxt}$ and the chain of borders of the prefix function. So after line L8, $q$ is the length of the longest prefix of $P$ that is a suffix of $T[0 \ldots i]$, and an occurrence ends at $i$ exactly when $q = m$. The full proof is below.

## Complexity

- **Preprocessing.** COMPUTE-PREFIX-FUNCTION takes $O(m)$ time with at most $2(m - 1)$ comparisons, as shown on the [prefix function](/prefix-function/) page. Lines L13 to L17 take $O(m)$ more.
- **Search, at most $2n$ comparisons.** Each comparison of line L6 either succeeds, which happens at most once per text character, so at most $n$ times, or fails. Each failure runs line L7, which decreases $q$ by at least 1, because $\mathrm{nxt}[q] < q$. The variable $q$ starts at 0, ends at a value of at least 0, and grows only at line L8, by 1, exactly $n$ times in all. So its total decrease is at most $n$, and there are at most $n$ failures. This is a [potential](/potential-method/) argument with potential $q$. The search makes at most $2n$ comparisons and runs in $O(n)$ time.
- **Lower bound.** Each text character is read at line L6 at least once, and the preprocessing reads the whole pattern, so the time is $\Omega(n + m)$ on every input. Hence $\Theta(n + m)$ in the best and in the worst case.
- **Space.** The tables $\pi$ and $\mathrm{nxt}$ take $\Theta(m)$ words. The text is not stored: the algorithm only needs $T[i]$.
- **Delay.** The number of comparisons spent on one text character is not bounded by a constant. With the strong table, Knuth, Morris and Pratt proved that it is $O(\log m)$, with the golden ratio as the base of the logarithm. Over two letters it is at most 2, because after a mismatch the strong table never offers the same letter again. With the weak table of Morris-Pratt, the delay can be $m$, for example for $P = a^{m-1}b$ and a text with $a^{m-1}$ followed by a third letter.

| claim | value |
|---|---|
| time, worst and best | $\Theta(n + m)$ |
| comparisons in the search | at most $2n$ |
| extra space | $\Theta(m)$ |

## Properties

- **Online.** The output at position $i$ depends only on $T[0 \ldots i]$, and each character is read once, so KMP works on a stream with no buffer.
- **General alphabet.** It only tests equality, so it works on any type with equality, and its time does not depend on the alphabet size.
- **Deterministic and exact.** No hashing and no probability.
- **Not sublinear.** It reads every text character. Algorithms such as [Boyer-Moore](/boyer-moore/) can skip characters on average.

## Variants and improvements

- **Morris-Pratt.** Use $\pi$ itself as the failure table. Same $O(n + m)$ time and $2n$ bound, but a larger delay. See [Morris-Pratt](/morris-pratt/).
- **The automaton.** Unfold the failure transitions into a full transition table, one entry per state and character. Then each text character costs exactly one step: the [string-matching automaton](/string-matching-automaton/), built in $O(m\sigma)$ time.
- **Real time.** Galil (1981) turned the method into a real-time algorithm, with $O(1)$ time per text character in the worst case.
- **Matching through the prefix function only.** Compute $\pi$ of $P \# T$, with a separator $\#$ not in the alphabet, and report each $j$ with $\pi[j] = m$. Simple, but it uses $O(n + m)$ memory.
- **Many patterns.** [Aho-Corasick](/aho-corasick/) generalizes the failure function to a [trie](/trie/) of patterns.
- **Fewer comparisons.** Simon's and Colussi's refinements, and the Galil-Giancarlo algorithm, lower the number of comparisons below $2n$ while keeping a left-to-right style.

## When to use it

Use KMP when the worst case matters, when the text is a stream that cannot be read twice, or when the alphabet is large or not even ordered. For one search in normal text with a long pattern, [Horspool](/boyer-moore-horspool/) or [Boyer-Moore](/boyer-moore/) is often several times faster because it skips characters. For many searches in one fixed text, index the text with a [suffix array](/suffix-array/). For constant extra space with a linear bound, use the [two-way algorithm](/two-way-string-matching/).

## Pitfalls

- **Restart from zero after a match.** Setting $q \leftarrow 0$ instead of $q \leftarrow \mathrm{nxt}[m]$ in line L11 misses overlapping occurrences: abab in abababab is then found at 0 and 4 but not at 2. The test `test_overlap_after_match` catches this.
- **Advancing the text on a mismatch.** After line L7 the same $T[i]$ must be compared again. Code that moves to $T[i+1]$ after a fall-back misses occurrences. The random test `test_random_against_oracle` catches this.
- **Off by one in the table.** The value $\pi[q]$ is for the prefix of length $q + 1$. Using $\pi[q]$ where $\pi[q-1]$ is needed (line L15) shifts every fall-back. The test `test_tables_against_definition` compares both tables with a brute-force definition.
- **The strong table at $q = m$.** $P[m]$ does not exist, so $\mathrm{nxt}[m]$ must be $\pi[m-1]$, not computed by line L16.
- **Counting the whole prefix as a border.** If $\pi[q]$ could be $q + 1$, line L7 would not decrease $q$ and the loop would never end.

## Implementations

## History

James H. Morris found the method while writing a text editor, and with Vaughan Pratt described it in a 1970 Berkeley technical report; this version is now called [Morris-Pratt](/morris-pratt/). Donald Knuth reached the same algorithm independently from Stephen Cook's theorem that two-way deterministic pushdown automata can be simulated in linear time, and added the strong failure table and the analysis of the delay. The three authors published the joint paper in the SIAM Journal on Computing in 1977, with an account of this history at its end. The same year Boyer and Moore published their right-to-left algorithm.

## References
