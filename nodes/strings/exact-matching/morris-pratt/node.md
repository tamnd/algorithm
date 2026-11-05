---
tag: SGQC43
kind: algorithm
slug: morris-pratt
name: Morris-Pratt algorithm
aliases:
- MP algorithm
area: strings/exact-matching
level: core
summary: Historical precursor of KMP with a weaker failure rule; linear time.
solves: [string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [prefix-function, string-matching, potential-method]
see_also: [knuth-morris-pratt, naive-string-matching, string-matching-automaton, aho-corasick]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.4, The Knuth-Morris-Pratt algorithm (KMP-MATCHER and COMPUTE-PREFIX-FUNCTION use the prefix function, which is the Morris-Pratt rule)
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node7.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Morris-Pratt algorithm (the table mpNext, at most 2n - 1 comparisons, delay at most m)
  - paper: doi:10.1137/0206024
    title: D. E. Knuth, J. H. Morris and V. R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2) (1977), 323-350
    locator: the historical remarks (the 1970 report of Morris and Pratt) and the comparison of the failure tables
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 2.3 (the shift rule with the values sp, against the stronger sp')
---

The Morris-Pratt algorithm (MP) solves [string matching](/string-matching/) in $\Theta(n + m)$ time by scanning the text once from left to right and, after each mismatch, falling back along the [prefix function](/prefix-function/) of the pattern. It makes at most $2n$ character comparisons in the search, like [Knuth-Morris-Pratt](/knuth-morris-pratt/), but its fall-back rule is weaker: it may compare one text character with several pattern characters that are all equal to the one that just failed, so its delay on one character can reach $m$. Morris and Pratt described it in 1970, and most textbooks present this version under the name KMP.

## In plain words

Read the text one letter at a time, and remember how many letters of the word match the end of what you read. If the next letter fits, the count goes up by one. If the count reaches the length of the word, report a match.

If the next letter does not fit, do not go back in the text. The letters matched so far are a start of the word. Find the longest end of that start which is also a start of the word, and pretend that only this much matched. Try the same text letter again. Repeat until it fits or nothing is left.

The table of "longest end that is also a start" is built once, before the search, in one pass over the word.

## The problem

The input is a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$ over a general alphabet: only equality tests between characters are used. Indices are 0-based. The output is the list of all shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order. Occurrences may overlap. If $m = 0$, all shifts $0, \ldots, n$ are output; if $m > n$, nothing is output. This is the [string matching](/string-matching/) problem.

## The algorithm

$\pi[q]$ is the length of the longest proper [border](/border/) of $P[0 \ldots q]$, the [prefix function](/prefix-function/). The variable $q$ is the number of pattern characters matched so far.

```pseudo id=main
MP-MATCHER(T, P)
L1  n ← |T|, m ← |P|
L2  if m = 0 then output 0, 1, …, n and return
L3  π ← COMPUTE-PREFIX-FUNCTION(P)
L4  q ← 0                                ▷ P[0 .. q − 1] = T[i − q .. i − 1]
L5  for i ← 0 to n − 1 do
L6      while q > 0 and P[q] ≠ T[i] do
L7          q ← π[q − 1]                 ▷ next shorter border
L8      if P[q] = T[i] then q ← q + 1
L9      if q = m then
L10         output i − m + 1
L11         q ← π[m − 1]

COMPUTE-PREFIX-FUNCTION(P)
L12 m ← |P|, π[0] ← 0, k ← 0
L13 for q ← 1 to m − 1 do
L14     while k > 0 and P[k] ≠ P[q] do
L15         k ← π[k − 1]
L16     if P[k] = P[q] then k ← k + 1
L17     π[q] ← k
L18 return π
```

Both parts have the same shape. COMPUTE-PREFIX-FUNCTION is MP-MATCHER run with the pattern against itself, starting at the second character. In the search, lines L6 and L7 walk down the chain of borders of the matched part until the next pattern character equals $T[i]$ or the matched part is empty. Line L8 extends the match by one if it can. After a full match, line L11 keeps the longest border of $P$, so that overlapping occurrences are found. In code, the comparison that ends the loop of line L6 and the test of line L8 are one comparison.

## Example

Search for $P$ = abacabab ($m = 8$) in $T$ = abacabcabacababa ($n = 16$), the example of the [KMP](/knuth-morris-pratt/) page.

| $q$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $P[q]$ | a | b | a | c | a | b | a | b |
| $\pi[q]$ | 0 | 0 | 1 | 0 | 1 | 2 | 3 | 2 |

| $i$ | $T[i]$ | values of $q$ tried | $q$ after L8 | output |
|---|---|---|---|---|
| 0 to 5 | abacab | 0, 1, 2, 3, 4, 5 (one each) | 1 to 6 | |
| 6 | c | 6, 2, 0 | 0 | |
| 7 to 13 | abacaba | 0, 1, ..., 6 (one each) | 1 to 7 | |
| 14 | b | 7 | 8, then $\pi[7] = 2$ | 7 |
| 15 | a | 2 | 3 | |

At $i = 6$, the matched part is abacab and $P[6]$ = a fails against c. MP falls back to the border ab ($q = \pi[5] = 2$) and compares $P[2]$ = a with c, then to the empty border ($q = \pi[1] = 0$) and compares $P[0]$ = a with c. All three pattern characters are a, so the last two comparisons could not succeed. KMP skips them, and makes 16 comparisons on this input instead of 18. Both report the occurrence at shift 7.

## Correctness

The loop of line L5 keeps this [loop invariant](/loop-invariant/): at the start of the iteration for $i$, $q$ is the length of the longest prefix of $P$, shorter than $m$, that is a suffix of $T[0 \ldots i-1]$, and the shifts already output are the occurrences that end before $i$. The chain $q, \pi[q-1], \pi[\pi[q-1]-1], \ldots, 0$ lists exactly the prefixes of $P$ that are suffixes of the text read so far, longest first, by the border-chain lemma of the [prefix function](/prefix-function/). Lines L6 to L8 take the first of them that $T[i]$ extends, which is the longest prefix of $P$ ending at $T[i]$. The full proof is below.

## Complexity

- **Preprocessing.** $O(m)$ time, with at most $2(m - 1)$ comparisons, by the potential argument of the [prefix function](/prefix-function/) page.
- **Search.** Each failed comparison of line L6 is followed by line L7, which decreases $q$ by at least 1, because $\pi[q-1] \le q - 1$. The variable $q$ starts at 0, is never negative, and increases only at line L8, by 1, at most once per text character. So the total number of decreases is at most $n$, and there are at most $n$ failed comparisons in line L6. Line L8 adds at most one comparison per text character, so at most $n$. The search makes at most $2n$ comparisons and runs in $O(n)$ time. This is the [potential method](/potential-method/) with potential $q$.
- **Lower bound.** Each text character is compared at least once, and each pattern character is read in the preprocessing, so the time is $\Omega(n + m)$ on every input, and $\Theta(n + m)$ in the best and the worst case.
- **Space.** $\Theta(m)$ for $\pi$.
- **Delay.** One text character can cost $m$ comparisons. For $P = a^{m-1}b$ and the text $a^{m-1}c$, the last character is compared with $P[m-1]$, $P[m-2]$, ..., $P[0]$. The [KMP](/knuth-morris-pratt/) table reduces the delay to $O(\log m)$.

| claim | value |
|---|---|
| time, worst and best | $\Theta(n + m)$ |
| comparisons in the search | at most $2n$ |
| extra space | $\Theta(m)$ |

## Properties

- **Online.** Each text character is read once, and an occurrence is reported when its last character is read.
- **General alphabet.** Only equality tests are used.
- **Not real time.** The work on one character is up to $m$ comparisons, so the time between two reads is not bounded by a constant.
- **Simple table.** The table is the plain prefix function, which has many other uses, so one table serves several purposes.

## Variants and improvements

- **Knuth-Morris-Pratt.** Skip each border $k$ with $P[k] = P[q]$: the strong failure table. Same total bound, delay $O(\log m)$. See [Knuth-Morris-Pratt](/knuth-morris-pratt/).
- **Automaton.** Precompute the result of the fall-back loop for each state and each character: the [string-matching automaton](/string-matching-automaton/), with exactly one step per text character.
- **Matching through one prefix function.** Compute $\pi$ of $P \# T$ with a separator $\#$ not in the alphabet; the occurrences end where the value equals $m$.
- **Many patterns.** [Aho-Corasick](/aho-corasick/) runs the same fall-back loop on a trie with [failure links](/failure-link/).

## When to use it

Use MP when you need a short, safe linear-time matcher and the delay per character does not matter: it is the version that most libraries and contest codes call KMP. Prefer [KMP](/knuth-morris-pratt/) or the [automaton](/string-matching-automaton/) when each character must be handled in short bounded time, for example in a network filter. For fast average search in natural text, a [Boyer-Moore](/boyer-moore/) variant skips characters and is faster.

## Pitfalls

- **Restart at zero after a match.** Line L11 must set $q \leftarrow \pi[m-1]$, not $q \leftarrow 0$, or overlapping occurrences are lost. The test `test_overlap_after_match` checks abab in abababab.
- **Reading $P[m]$.** Without line L11, the next iteration would compare $P[m]$. Always reduce $q$ right after a full match.
- **Wrong index into $\pi$.** The fall-back from $q$ matched characters is $\pi[q-1]$, not $\pi[q]$. The test `test_prefix_function_against_definition` checks the table against the definition.
- **An infinite loop.** If the while test is `q ≥ 0` with this table, then at $q = 0$ line L7 reads $\pi[-1]$. The test must be `q > 0`.

## Implementations

## History

James H. Morris and Vaughan R. Pratt described the algorithm in 1970 in the technical report "A linear pattern-matching algorithm" (Technical Report 40, University of California, Berkeley). Morris had used the idea in a text editor. Knuth found the method independently and added the stronger table; the joint paper of Knuth, Morris and Pratt appeared in 1977 and describes this history. The name Morris-Pratt for the weaker version is used by Charras and Lecroq and by Crochemore and his coauthors, while CLRS call the same algorithm KMP.

## References
