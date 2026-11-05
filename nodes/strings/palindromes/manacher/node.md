---
tag: 25Z40B
kind: algorithm
slug: manacher
name: Manacher's algorithm
aliases:
- Manacher algorithm
- palindromic radius algorithm
area: strings/palindromes
level: core
summary: Computes the radius of the longest palindrome centred at every position in linear time.
solves: [longest-palindromic-substring]
model: comparison-model
complexity:
  vars: {n: the length of the string}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false, comparison: true}
history:
  year: 1975
  people: [Glenn Manacher]
  note: Manacher published a linear-time on-line algorithm for the smallest initial palindrome of a string in the Journal of the ACM in 1975.
prereqs: [palindrome, longest-palindromic-substring, amortized-cost]
see_also: [palindromic-tree, z-algorithm, palindrome-substring-queries, count-palindromic-substrings, shortest-palindrome, reverse-complement-palindrome, longest-common-extension-query, palindrome-recognition]
sources:
  - paper: doi:10.1145/321892.321896
    title: Glenn Manacher, A new linear-time on-line algorithm for finding the smallest initial palindrome of a string, Journal of the ACM 22(3) (1975), 346-351
    locator: the whole paper (the scan that starts each center at its mirror value, and the linear bound)
  - paper: doi:10.1016/0304-3975(94)00083-U
    title: Alberto Apostolico, Dany Breslauer and Zvi Galil, Parallel detection of all palindromes in a string, Theoretical Computer Science 141 (1995), 163-173
    locator: the introduction (Manacher's scan gives the maximal palindromes at all centers)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 9, Section 9.2, Finding all maximal palindromes in linear time (pages 197 to 199)
  - url: https://cp-algorithms.com/string/manacher.html
    title: CP-Algorithms, Manacher's algorithm, finding all sub-palindromes in O(N)
    locator: the whole article (the trivial algorithm, the arrays for odd and even palindromes, and the version with separators)
---

Manacher's algorithm computes, for each of the $2n + 1$ centers of a string of length $n$, the length of the longest [palindrome](/palindrome/) with that center, in $\Theta(n)$ time. It is the expand-around-the-center method with one change: inside the rightmost palindrome found so far, a center starts from the value of its mirror center on the left, so no symbol to the left of the right end is compared twice. The output answers the [longest palindromic substring](/longest-palindromic-substring/) problem, counts all palindromic substrings, and tests any substring for being a palindrome in $O(1)$ time. It uses only equality tests between symbols.

## In plain words

Every palindrome has a middle, on a letter or between two letters. The slow method stands at each middle and steps outward while the two letters match. Manacher's method keeps the palindrome that reaches farthest to the right. When a new middle falls inside it, the method looks at the mirror point on the left side of that palindrome, whose answer is already known. Inside the big palindrome the two sides look the same, so the new middle gets at least the same answer, as far as the big palindrome reaches. Only beyond its right end does the method step outward again, and each such step moves the right end. The right end never goes back, so the total work is a fixed amount for each letter.

## The problem

The input is a string $s = s[0..n-1]$ over an [alphabet](/alphabet/) $\Sigma$, with 0-based indices. The algorithm only tests two symbols for equality, so $\Sigma$ needs no order and can be of any size.

To treat odd and even palindromes the same way, the algorithm reads $s$ through the implicit string
$$ T = \#\, s[0]\, \#\, s[1]\, \# \cdots \#\, s[n-1]\, \# $$
of length $m = 2n + 1$, where $\#$ is a separator that is not a symbol of $\Sigma$. So $T[2k+1] = s[k]$ and $T[2k] = \#$. Position $c$ of $T$ is a center of $s$: odd $c$ is the symbol $s[(c-1)/2]$, and even $c$ is the gap before $s[c/2]$ (with the two ends $c = 0$ and $c = 2n$).

The output is the array $P[0..m-1]$, where $P[c]$ is the largest $r \ge 0$ such that $c - r \ge 0$, $c + r \le m - 1$ and $T[c-r..c+r]$ is a palindrome. The correctness proof shows that $P[c]$ is also the length of the longest palindrome of $s$ with center $c$, which is
$$ s\big[\tfrac{c - P[c]}{2} \,..\, \tfrac{c + P[c]}{2} - 1\big], $$
and that for $0 \le i \le j \le n-1$,
$$ s[i..j] \text{ is a palindrome} \iff P[i + j + 1] \ge j - i + 1. $$
Odd palindromes appear at odd $c$ with odd $P[c]$, and even palindromes at even $c$ with even $P[c]$.

## The algorithm

A test $T[x] = T[y]$ is made only for $x$ and $y$ of the same parity. For even $x$ it is true without a comparison (two separators), and for odd $x$ it is the symbol test $s[(x-1)/2] = s[(y-1)/2]$. So $T$ is never built. The variable $r$ is the largest value of $c' + P[c']$ over the centers $c'$ done so far, the rightmost position of $T$ covered by a palindrome found so far, and $c$ is a center that reaches it.

```pseudo id=main
MANACHER(s)                                  ▷ s[0 .. n − 1], T as above
L1  m ← 2n + 1
L2  P[0 .. m − 1] ← all 0
L3  c ← 0, r ← 0
L4  for i ← 0 to m − 1 do
L5      if i < r then P[i] ← min(P[2c − i], r − i)     ▷ mirror center 2c − i
L6      while i − P[i] − 1 ≥ 0 and i + P[i] + 1 < m and T[i − P[i] − 1] = T[i + P[i] + 1] do
L7          P[i] ← P[i] + 1
L8      if i + P[i] > r then c ← i, r ← i + P[i]
L9  return P
```

Line L5 is the only difference from the expand-around-the-center method. Without it, $P[i]$ would start at 0 and the method would take $\Theta(n^2)$ time on $a^n$.

## Example

Let $s = $ `abaabaab`, so $n = 8$ and $m = 17$. The table shows, for each $i$, the mirror center $2c - i$ when $i < r$, the start value of $P[i]$ from line L5, the number of steps of line L7, the final $P[i]$, and $c$ and $r$ after line L8.

| $i$ | $T[i]$ | mirror | start | steps | $P[i]$ | $c$ | $r$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | # | none | 0 | 0 | 0 | 0 | 0 |
| 1 | a | none | 0 | 1 | 1 | 1 | 2 |
| 2 | # | none | 0 | 0 | 0 | 1 | 2 |
| 3 | b | none | 0 | 3 | 3 | 3 | 6 |
| 4 | # | 2 | 0 | 0 | 0 | 3 | 6 |
| 5 | a | 1 | 1 | 0 | 1 | 3 | 6 |
| 6 | # | none | 0 | 6 | 6 | 6 | 12 |
| 7 | a | 5 | 1 | 0 | 1 | 6 | 12 |
| 8 | # | 4 | 0 | 0 | 0 | 6 | 12 |
| 9 | b | 3 | 3 | 4 | 7 | 9 | 16 |
| 10 | # | 8 | 0 | 0 | 0 | 9 | 16 |
| 11 | a | 7 | 1 | 0 | 1 | 9 | 16 |
| 12 | # | 6 | 4 | 0 | 4 | 9 | 16 |
| 13 | a | 5 | 1 | 0 | 1 | 9 | 16 |
| 14 | # | 4 | 0 | 0 | 0 | 9 | 16 |
| 15 | b | 3 | 1 | 0 | 1 | 9 | 16 |
| 16 | # | none | 0 | 0 | 0 | 9 | 16 |

So $P = [0, 1, 0, 3, 0, 1, 6, 1, 0, 7, 0, 1, 4, 1, 0, 1, 0]$. The rows show the three cases of line L5.

- **The mirror palindrome is inside.** At $i = 11$ the mirror 7 has $P = 1 < r - i = 5$, so $P[11] = 1$ and the test of line L6 fails at once.
- **The mirror palindrome reaches past the left end.** At $i = 12$ the mirror 6 has $P = 6 > r - i = 4$, so $P[12] = 4$ and line L6 fails at once; the same holds at $i = 15$.
- **The mirror palindrome ends at the left end.** At $i = 9$ the mirror 3 has $P = 3 = r - i$, so $P[9]$ starts at 3 and line L7 runs 4 more times, which moves $r$ from 12 to 16.

The longest palindrome is at $c = 9$ with $P[9] = 7$: it is $s[1..7] = $ `baabaab`. The even center $c = 6$ gives $s[0..5] = $ `abaaba`. The test of line L6 runs 23 times in all, and 15 of these compare two symbols of $s$.

## Correctness

Let $\rho(c)$ be the true radius of the maximal palindrome of $T$ at $c$. The proof rests on a mirror lemma. Suppose $c < i < r = c + \rho(c)$ and $j = 2c - i$. Then $T[c - \rho(c)..r]$ is a palindrome that contains the windows of radius $\min(\rho(j), r - i)$ around $j$ and around $i$, and these windows are reversals of each other, so $\rho(i) \ge \min(\rho(j), r - i)$. If $\rho(j) \ne r - i$, then equality holds: when $\rho(j) < r - i$, a longer palindrome at $i$ would mirror to a longer one at $j$; when $\rho(j) > r - i$, the symbol after $r$ differs from the symbol before $c - \rho(c)$, and by two mirror steps that symbol equals the symbol at $i - (r - i) - 1$.

The loop invariant of line L4 is: for all $k < i$, $P[k] = \rho(k)$; $r = \max_{k < i} (k + \rho(k))$, or 0 when $i = 0$; and $c + P[c] = r$. By the lemma, line L5 sets $P[i]$ to a radius at which $T[i - P[i]..i + P[i]]$ is a palindrome and $P[i] \le \rho(i)$. The palindromes with one center are nested, so lines L6 and L7 extend $P[i]$ exactly to $\rho(i)$. Line L8 keeps $r$ and $c$. At the end, $P = \rho$.

The link to $s$ comes from the separators. A maximal palindrome of $T$ ends on separators, because two symbol ends could be extended by the two separators next to them. A substring $T[2a..2b]$ with separator ends is a palindrome if and only if $s[a..b-1]$ is one, and $s[a..b-1]$ has $b - a = \rho(c)$ symbols for $c = a + b$. The full proof is in the proof file of this page.

## Complexity

**Time.** At each $i$, the number of runs of line L7 is at most the increase of $r$ in line L8. *Proof.* If $i \ge r$, then $P[i]$ starts at 0, and after $t \ge 1$ steps line L8 sets $r$ to $i + t \ge r + t$. If $i < r$, the lemma shows that line L6 can succeed only when $\rho(j) = r - i$, so $P[i]$ starts at $r - i$, and after $t$ steps line L8 sets $r$ to $r + t$. $r$ starts at 0, never decreases and stays at most $m - 1 = 2n$, so line L7 runs at most $2n$ times in all. Each $i$ has at most one test of line L6 that ends its loop. So line L6 runs at most $2n + m = 4n + 1$ times, and the time is $\Theta(n)$.

- **Symbol comparisons.** Each test of line L6 makes at most one comparison of two symbols of $s$, and the tests between separators make none. So there are at most $4n + 1$ symbol comparisons.
- **Best case.** The loop of line L4 runs $m$ times on every input, so the time is $\Theta(n)$ on every input, including $a^n$ and strings with no palindrome longer than 1.
- **Space.** The array $P$ has $2n + 1$ entries. No copy of $s$ and no array $T$ are needed.

The [palindrome recognition](/palindrome-recognition/) page proves that $\lfloor n/2 \rfloor$ equality tests are necessary to test one string, and the [longest palindromic substring](/longest-palindromic-substring/) page reduces that test to this output. So $\Theta(n)$ is optimal in the [comparison model](/comparison-model/). The analysis is an instance of the [amortized cost](/amortized-cost/) idea: the potential is $r$.

## Properties

- **Equality tests only.** No order on the alphabet and no hashing are needed. A separator that is not a symbol is not needed either, because the parity of the positions tells where the separators are.
- **Deterministic and exact.** There is no probability of error, unlike methods with [rolling hashes](/polynomial-rolling-hash/).
- **Not recursive.** The algorithm is one loop with an inner loop; the stack depth is constant.
- **The output is final for each center only at the end.** $P[i]$ depends on the symbols to the right of $i$, so the array form is not online. The original 1975 algorithm is online in a different sense: after each symbol it reports whether a palindromic prefix has ended there.
- **The same idea as the Z-algorithm.** The [Z-algorithm](/z-algorithm/) keeps the rightmost box that matches a prefix and starts each position from the value at its copy inside the prefix. Manacher's algorithm keeps the rightmost palindrome and starts each center from its mirror.

## Variants and improvements

- **Two arrays, no separators.** Compute $d_1[k]$, the number of odd palindromes centered at $s[k]$, and $d_2[k]$, the number of even palindromes centered in the gap before $s[k]$. These are $d_1[k] = (P[2k+1] + 1)/2$ and $d_2[k] = P[2k]/2$. The CP-Algorithms article gives both forms.
- **Counting palindromic substrings.** The center $c$ holds $\lceil P[c]/2 \rceil$ palindromic occurrences, so the total is $\sum_c \lceil P[c]/2 \rceil$: see [counting palindromic substrings](/count-palindromic-substrings/).
- **Palindrome queries.** With $P$, the test "is $s[i..j]$ a palindrome?" takes $O(1)$ time: see [palindrome substring queries](/palindrome-substring-queries/).
- **Longest palindromic prefix and suffix.** The prefix $s[0..j]$ is a palindrome if and only if $P[j+1] \ge j + 1$. The longest such $j$ gives the [shortest palindrome](/shortest-palindrome/) that has $s$ as a suffix.
- **Other symmetries.** With the test $s[x] = f(s[y])$ for an involution $f$, the same algorithm finds [reverse-complement palindromes](/reverse-complement-palindrome/) in DNA; for the DNA complement, which fixes no symbol, the scan runs over the even centers only.
- **Parallel.** Apostolico, Breslauer and Galil (1995) gave parallel algorithms for all maximal palindromes.
- **Distinct palindromes.** Manacher's array does not tell which palindromes are equal as strings. For distinct palindromes and for online use, the [palindromic tree](/palindromic-tree/) is the tool.

## When to use it

Use Manacher's algorithm when you need the longest palindromic substring, the maximal palindrome at each center, the number of palindromic occurrences, or many palindrome tests on one fixed string. It is short, exact and linear, and it needs only an equality test on symbols. Use the [palindromic tree](/palindromic-tree/) when the string grows by appends and you need answers after each symbol, or when you need the distinct palindromes. Use the expand-around-the-center method only for short strings.

## Pitfalls

- **Forgetting even palindromes.** Running the scan only on symbol centers misses `abba`. The separators, or the second array $d_2$, solve this.
- **A separator that is a symbol.** If $T$ is built as a real string with `#`, the input must not contain `#`. A separate object, or the parity test of this page, avoids the issue.
- **Off-by-one in the start index.** In the separator form the palindrome at $c$ starts at $(c - P[c])/2$ in $s$ and has length $P[c]$, not $2P[c] + 1$.
- **The mirror without the clip.** Line L5 needs the minimum with $r - i$. The mirror value alone can be too large, as at $i = 12$ in the example, where $P[6] = 6$ but $P[12] = 4$.
- **An open or closed $r$.** On this page $r = c + P[c]$ is the last position covered, and line L5 tests $i < r$. Code that stores the first position after the palindrome must shift the tests by one.

## Implementations

## History

Manacher (1975) published the algorithm as a linear-time online method for the smallest initial palindrome of a string, that is, the shortest nonempty prefix that is a palindrome (of even length in the paper). Apostolico, Breslauer and Galil (1995) observed that the same scan finds the maximal palindromes at all centers, and gave parallel versions. Gusfield's 1997 book gives an alternative with suffix trees and longest common extension queries, in Section 9.2.

## References
