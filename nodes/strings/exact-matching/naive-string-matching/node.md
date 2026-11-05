---
tag: NM14X8
kind: algorithm
slug: naive-string-matching
name: Naive string matching
aliases:
- brute-force string matching
area: strings/exact-matching
level: intro
summary: Try every shift and compare; O(nm) worst case.
solves: [string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the alphabet size}
  time: {worst: Θ((n - m + 1) m), average: O(n), best: Θ(n - m + 1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [string-matching, loop-invariant, asymptotic-notation]
see_also: [knuth-morris-pratt, boyer-moore, rabin-karp, z-algorithm, string-matching-lower-bound]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.1, The naive string-matching algorithm
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 1, Section 1.1 (the naive method and its worst case)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 5.3, Substring search (brute-force substring search and its worst case)
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node3.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Brute Force algorithm (expected 2n comparisons on random text)
---

Naive string matching solves the [string matching](/string-matching/) problem by trying each shift of the pattern against the text and comparing character by character. It takes $\Theta((n - m + 1)m)$ time in the worst case, for a text of length $n$ and a pattern of length $m$, and $O(n)$ time on average on a random text. It needs no preprocessing and no extra memory, so it is the baseline that every faster algorithm improves on, and it is still the fastest choice for very short patterns.

## In plain words

Put the word under the start of the text. Compare the letters one by one, from left to right, until two letters differ or the word ends. If the word ends, you found an occurrence. Then move the word one letter to the right and start again from its first letter.

The method forgets everything at each move. If the text and the word are long runs of the same letter, it compares almost every letter of the word at almost every start. On normal text, the first or second letter usually differs, so each start costs very little.

## The problem

The input is a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$ over a general alphabet: the algorithm only tests two characters for equality. Indices are 0-based. The output is the list of all shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order. Occurrences may overlap. If $m = 0$, every shift $0, \ldots, n$ is output, and if $m > n$, nothing is output. This is the [string matching](/string-matching/) problem.

## The algorithm

```pseudo id=main
NAIVE-STRING-MATCHING(T, P)
L1  n ← |T|, m ← |P|
L2  for s ← 0 to n − m do                 ▷ no iteration when m > n
L3      j ← 0
L4      while j < m and T[s + j] = P[j] do
L5          j ← j + 1
L6      if j = m then output s
```

Line L2 tries each shift once, in increasing order. Lines L3 to L5 extend the match at shift $s$ from the left until a mismatch or the end of the pattern. The test $j < m$ comes first, so the loop never reads $P[m]$ or a text character past $T[s + m - 1] \le T[n - 1]$. Line L6 reports the shift when the whole pattern matched.

## Example

Search for $P$ = abab in $T$ = abaababaab, with $n = 10$ and $m = 4$. There are $n - m + 1 = 7$ shifts. The column $j$ is the length of the match when the loop of line L4 stops.

| $s$ | $T[s \ldots s+3]$ | $j$ | comparisons | output |
|---|---|---|---|---|
| 0 | abaa | 3 | 4 | |
| 1 | baab | 0 | 1 | |
| 2 | aaba | 1 | 2 | |
| 3 | abab | 4 | 4 | 3 |
| 4 | baba | 0 | 1 | |
| 5 | abaa | 3 | 4 | |
| 6 | baab | 0 | 1 | |

The output is the single shift 3, after 17 character comparisons. At shift 0 the algorithm learns that $T[0 \ldots 2]$ = aba, but it still compares $T[1]$ and $T[2]$ again at shifts 1 and 2. [Knuth-Morris-Pratt](/knuth-morris-pratt/) uses this lost information.

A worst case: for $T = a^{10}$ and $P = a^4$, each of the 7 shifts compares all 4 characters, so the algorithm makes $7 \cdot 4 = 28$ comparisons. The pattern aaab gives 28 comparisons too and no occurrence.

## Correctness

For a fixed $s$, the loop of line L4 keeps the [loop invariant](/loop-invariant/) $0 \le j \le m$ and $T[s \ldots s+j-1] = P[0 \ldots j-1]$. It stops with $j = m$ exactly when all $m$ characters match, so line L6 outputs $s$ exactly when $s$ is a valid shift. Line L2 tries every candidate shift, in increasing order. The full proof is below.

## Complexity

Count the character comparisons of line L4. Each other step costs $O(1)$ per comparison or per shift.

- **Worst case.** At each of the $n - m + 1$ shifts, the loop makes at most $m$ comparisons, so the time is $O((n - m + 1)m)$. The input $T = a^n$, $P = a^m$ with $m \le n$ makes exactly $m$ comparisons at each shift, so the bound is reached: $\Theta((n - m + 1)m)$. For $m = n/2$ this is $\Theta(n^2)$.
- **Best case.** Each shift makes at least one comparison when $m \ge 1$, so the time is $\Theta(n - m + 1)$. A text with no copy of $P[0]$ reaches it.
- **Average case.** Let the text be uniformly random over $\sigma \ge 2$ letters, and let $P$ be any fixed pattern. At shift $s$, the comparison of $P[j]$ happens only if the $j$ earlier characters matched, which has probability $\sigma^{-j}$, because the text characters are independent. So the expected number of comparisons at one shift is at most $\sum_{j \ge 0} \sigma^{-j} = \sigma / (\sigma - 1) \le 2$, and by [linearity of expectation](/linearity-of-expectation/) the total is at most $2(n - m + 1) = O(n)$.
- **Space.** The algorithm uses the variables $s$ and $j$, so the extra space is $\Theta(1)$ besides the output.

On real text the average is close to this bound, because the first character often differs. On text with long runs, such as DNA with repeats or binary data with many zero bytes, the worst case can appear.

## Properties

- **No preprocessing.** It reads the pattern only during the search, so it works for a pattern used once.
- **General alphabet.** It only tests characters for equality.
- **Not online.** It moves back in the text by up to $m - 1$ characters at each new shift, so a stream needs a buffer of the last $m$ characters.
- **Deterministic and simple.** Its inner loop is the same as the loop of a library `memcmp`, which hardware does fast.

## Variants and improvements

- **Compare from the right.** The same method with right-to-left comparison is the base of [Boyer-Moore](/boyer-moore/). The shift is still 1 here.
- **Not So Naive.** A variant compares $P[1]$ first and uses whether $P[0] = P[1]$ to skip one or two shifts. Its worst case is still $\Theta(nm)$.
- **Filter on the first character.** Use a fast search (for example `memchr`) for $P[0]$ and run the comparison only at those places. Library functions often do this.
- **Use what was matched.** [Morris-Pratt](/morris-pratt/) and [Knuth-Morris-Pratt](/knuth-morris-pratt/) keep the matched prefix and never move back in the text, which gives $O(n + m)$ time.
- **Compare a hash first.** [Rabin-Karp](/rabin-karp/) compares a rolling hash of the window before the characters.

## When to use it

Use it for short patterns, for one search with a pattern that is never used again, and for random-looking text, where its average is about one or two comparisons per shift. Use [Knuth-Morris-Pratt](/knuth-morris-pratt/) or the [two-way algorithm](/two-way-string-matching/) when the input can be adversarial, because the naive method then takes quadratic time. Use [Horspool](/boyer-moore-horspool/) for long patterns over a large alphabet.

## Pitfalls

- **The last shift is missed.** A loop `for s in range(n - m)` stops at $n - m - 1$. The bound of line L2 includes $n - m$. The test `test_last_shift` catches this.
- **Unsigned underflow.** In C, `n - m` with unsigned `size_t` wraps around to a huge value when $m > n$, and the loop reads past the text. Test $m > n$ first. The test `test_edges` has a pattern longer than the text.
- **The order of the tests.** Write `j < m and T[s + j] = P[j]`, not the other way. Otherwise the loop reads $P[m]$ after a full match.
- **The empty pattern.** Decide what the empty pattern returns. This page returns all $n + 1$ shifts, as the definition gives.
- **Copies of slices.** In Python, `t[s:s+m] == p` copies $m$ characters at each shift. The time stays $\Theta(m)$ per shift in the worst case, but even an early mismatch costs $m$, so the average becomes $\Theta(nm)$.

## Implementations

## History

The method is the direct reading of the definition and has no single author. Textbooks present it as the base of the topic: CLRS in Section 32.1, Gusfield in Section 1.1 and Sedgewick and Wayne in Section 5.3. The faster algorithms of 1977, [Knuth-Morris-Pratt](/knuth-morris-pratt/) and [Boyer-Moore](/boyer-moore/), were designed to remove its worst case and to beat its average.

## References
