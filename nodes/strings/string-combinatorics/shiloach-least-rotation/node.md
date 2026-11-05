---
tag: WKJHV4
kind: algorithm
slug: shiloach-least-rotation
name: Shiloach's least rotation algorithm
aliases:
- Shiloach canonization of circular strings
area: strings/string-combinatorics
level: advanced
summary: Canonizes a circular string by repeatedly eliminating non-minimal candidate rotations.
solves: [minimal-rotation, word-conjugacy-testing]
model: comparison-model
complexity:
  vars: {n: the length of the word}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: false, in_place: true, comparison: true}
prereqs: [minimal-rotation, lexicographic-order]
see_also: [booth-algorithm, duval-algorithm, word-conjugacy-testing, necklace, lyndon-word, circular-pattern-matching, primitive-root-of-a-word, loop-invariant]
sources:
  - paper: doi:10.1016/0196-6774(81)90013-4
    title: Yossi Shiloach, Fast canonization of circular strings, Journal of Algorithms 2(2), 1981, 107-121
    locator: the elimination of candidate starting points by comparing two candidates, and the bound of n + ⌈d/2⌉ comparisons with constant extra space
  - paper: doi:10.1016/0020-0190(80)90149-0
    title: Kellogg S. Booth, Lexicographically least circular substrings, Information Processing Letters 10(4-5), 1980, 240-242
    locator: the whole paper (the problem of the least circular substring and the earlier linear-time solution with linear space)
  - paper: doi:10.1016/0196-6774(83)90017-2
    title: Jean-Pierre Duval, Factorizing words over an ordered alphabet, Journal of Algorithms 4(4), 1983, 363-381
    locator: the computation of the least conjugate of a word from the Lyndon factorization, the other constant-space method
---

Shiloach's algorithm finds the least rotation of a word $s$ of length $n$, the index $i$ where the lexicographically smallest of the words $s[i..n-1]\,s[0..i-1]$ begins. It keeps two candidate starting points and compares their rotations letter by letter; at the first difference, the losing candidate and every start in the block of equal letters after it are discarded at once. The method uses fewer than $3n$ letter comparisons and constant extra space in the [comparison model](/comparison-model/), and Shiloach's refined version needs at most $n + \lceil d/2 \rceil$ comparisons. The least rotation is a canonical form of the word read around a circle, so the algorithm also decides whether two words are rotations of each other.

## In plain words

Write a word on a ring. You want the place to cut the ring so that the letters, read from the cut, come first in dictionary order.

Pick two places to cut and read both rings letter by letter. As long as the letters agree, keep reading. When they first differ, the cut that shows the larger letter loses. It is not the only loser: if you had cut one, two or more steps further along on the losing side, you would have been beaten at the same spot by the other side shifted by the same amount. So a whole stretch of cuts is thrown out after one race. The winner stays, and a new challenger comes from the cuts not yet thrown out. Each race throws out at least as many cuts as it read letters, so the total work is small.

## The problem

The input is a word $s = s[0..n-1]$ with $n \ge 1$ over an alphabet with a total order; the algorithm uses only comparisons of letters, equality and less-than. Indices are 0-based and all index arithmetic is modulo $n$. The rotation at $i$ is $\mathrm{rot}_i(s) = s[i..n-1]\,s[0..i-1]$. The output is the smallest $i$ such that $\mathrm{rot}_i(s) \le \mathrm{rot}_j(s)$ in [lexicographic order](/lexicographic-order/) for all $j$. This is the [minimal rotation](/minimal-rotation/) problem.

All least starting points form the progression $i, i + d, i + 2d, \ldots$ below $n$, where $d$ is the length of the [primitive root](/primitive-root-of-a-word/) of $s$, so the smallest one determines the others.

## The algorithm

Call an index $j$ a *loser* if $\mathrm{rot}_j(s)$ is not the least rotation. The variable $g$ is the current best candidate and $h$ the next challenger; every index below $h$ other than $g$ is a loser.

```pseudo id=main
LEAST-ROTATION(s[0 .. n − 1])        ▷ n ≥ 1, indices modulo n
L1  g ← 0; h ← 1
L2  while h < n do
L3      k ← 0
L4      while k < n and s[g + k] = s[h + k] do
L5          k ← k + 1
L6      if k = n then return g            ▷ rot_g = rot_h, s is periodic
L7      if s[g + k] < s[h + k] then
L8          h ← h + k + 1                 ▷ h, h + 1, ..., h + k lose
L9      else
L10         g ← max(h, g + k + 1)         ▷ g, g + 1, ..., g + k lose
L11         h ← g + 1
L12 return g
```

**The elimination rule.** Suppose $\mathrm{rot}_g$ and $\mathrm{rot}_h$ agree on their first $k$ letters and $s[g + k] < s[h + k]$. For $0 \le t \le k$, the rotations $\mathrm{rot}_{g+t}$ and $\mathrm{rot}_{h+t}$ agree on their first $k - t$ letters and then show $s[g + k]$ and $s[h + k]$, so $\mathrm{rot}_{g+t} < \mathrm{rot}_{h+t}$ and $h + t$ is a loser. This is why line L8 skips $k + 1$ challengers at once, and line L10 does the same for the other side.

## Example

Run LEAST-ROTATION on $s = $ `bbaaccaadd`, $n = 10$. Each row is one pass of the loop of line L2; $k$ is the number of equal letters found by lines L4 and L5, and the comparisons of the row are $k + 1$.

| $g$ | $h$ | $k$ | first difference $s[g+k]$, $s[h+k]$ | action | discarded |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | `b` > `a` | L10, L11: $g = 2$, $h = 3$ | 0, 1 |
| 2 | 3 | 1 | `a` < `c` | L8: $h = 5$ | 3, 4 |
| 2 | 5 | 0 | `a` < `c` | L8: $h = 6$ | 5 |
| 2 | 6 | 2 | `c` < `d` | L8: $h = 9$ | 6, 7, 8 |
| 2 | 9 | 0 | `a` < `d` | L8: $h = 10$ | 9 |

The loop stops with $h = 10$ and returns $g = 2$: the least rotation is `aaccaaddbb`. The run used $2 + 2 + 1 + 3 + 1 = 9$ comparisons. In the fourth row the candidate 6 is beaten after two equal letters (`aa`), and with it the starts 7 and 8.

For $s = $ `acabacab` the run reaches $g = 2$, $h = 6$, finds all $8$ letters equal, and returns 2 at line L6; the least rotation `abacabac` also starts at $6 = 2 + 4$, where 4 is the length of the primitive root `acab`.

## Correctness

The loop of line L2 keeps this [loop invariant](/loop-invariant/): $0 \le g < h$, $g < n$, and every index $j < \min(h, n)$ with $j \ne g$ is a loser. Line L1 makes it true. In a pass that finds a difference after $k$ equal letters, the elimination rule shows that line L8 discards only losers, and that line L10 discards $g, \ldots, g + k$, which together with the earlier losers leaves no candidate below $\max(h, g + k + 1)$ except possibly $h$; so the new $g$ is that value. When the loop ends with $h \ge n$, only $g$ can be a least start. When line L6 finds $\mathrm{rot}_g = \mathrm{rot}_h$, the word is invariant under rotation by $h - g$, and a least start at $h$ or beyond would give a least start in the gap between $g$ and $h$, which holds only losers; so $g$ is the answer. The full proof is in the correctness proof below.

## Complexity

- **Comparisons.** Count a three-way comparison of two letters as one. Let $\Phi = g + h$. A pass that stops at a difference after $k$ equal letters uses $k + 1$ comparisons and increases $\Phi$ by at least $k + 1$: line L8 adds exactly $k + 1$, and line L10 adds at least $k + 2$. $\Phi$ starts at 1, and at the end $g \le n - 1$ and $h \le 2n - 1$, so these passes use at most $3n - 3$ comparisons. A pass that reaches line L6 uses $n$ comparisons and ends the run, and before it $\Phi \le 2n - 3$. So the total is less than $3n$ comparisons, and the time is $\Theta(n)$.
- **Worst case.** The words $a^{n-3}baa$ need $3n - 6$ comparisons for $n \ge 4$; this is the maximum over all binary words of each length $4 \le n \le 16$, by exhaustive search.
- **Best case.** At least $n - 1$ comparisons on every word: a pass with $k + 1$ comparisons discards at most $k + 1$ new starts, and $n - 1$ starts must be discarded unless line L6 ends the run after $n$ comparisons. The word $a\,b^{n-1}$ meets this bound.
- **Space.** Three integers besides the input, so $\Theta(1)$ extra space.

## Properties

- **Constant space.** Unlike [Booth's algorithm](/booth-algorithm/), it builds no failure function and does not double the word; indices are taken modulo $n$.
- **Comparison-based.** It needs only equality and order tests on letters, so it works for any totally ordered alphabet.
- **Deterministic and iterative.** No recursion and no random choices.
- **Smallest start.** It returns the smallest index of the least rotation; for a periodic word the other least starts follow by adding the length of the primitive root.

## Variants and improvements

- **Shiloach's refinement.** Shiloach (1981) keeps finer information about the two candidates and reaches at most $n + \lceil d/2 \rceil$ comparisons, where $d$ is the length of the primitive root, still in constant space.
- **Greatest rotation.** Reverse the test of line L7 to find the lexicographically greatest rotation.
- **All least starts.** Compute $d$ with the [prefix function](/prefix-function/) in $O(n)$ time, or let line L6 return $h - g$ as a period, and list $g, g + d, \ldots$.
- **Duval's method.** The least rotation also follows from the Lyndon factorization of $ss$ computed by [Duval's algorithm](/duval-algorithm/), again in linear time and constant space.
- **Conjugacy test.** Two words of equal length are rotations of each other if and only if their least rotations are equal, which gives a constant-space [conjugacy test](/word-conjugacy-testing/).

## When to use it

Use it to put cyclic words in a canonical form: to deduplicate circular DNA sequences or polygon chain codes, to group words into [necklaces](/necklace/), or to compare two cyclic lists without extra memory. It is the shortest correct linear-time code for the problem. When the least rotations of all rotations of many strings are needed, or when suffix structures are built anyway, a [circular suffix array](/circular-suffix-array/) is the better tool.

## Pitfalls

- **Advancing only by one.** Setting $h \leftarrow h + 1$ in line L8 is still correct but takes $n(n-1)/2$ comparisons on $a^{n-1}b$, and setting $g \leftarrow h$ in line L10 takes $n(n-1)/2$ comparisons on $b^{n-1}a$. The skip over the $k$ equal letters is what makes the algorithm linear.
- **Dropping the max in line L10.** With $g \leftarrow g + k + 1$ alone, $g$ can land on a start between the old $g$ and $h$ that was already discarded. The result is still correct, but such starts are examined again and the bound of $3n$ comparisons fails: on $(ab)^5ba$, of length 12, the run takes 41 comparisons instead of 12.
- **Missing the periodic case.** Without the bound $k < n$ in line L4 the inner loop never stops on a word such as `abab`, where two rotations are equal.
- **Wrapping indices.** The letters must be read at $(g + k) \bmod n$; reading past the end of $s$ without the modulus compares wrong letters or fails.

## Implementations

## History

Booth (1980) gave the first linear-time algorithm for the least rotation, using a failure function and linear extra space. Shiloach (1981), in a paper on the canonization of circular strings, showed how to compare two candidate starts and discard many candidates at once, using constant extra space and at most $n + \lceil d/2 \rceil$ comparisons; he had earlier given a constant-space test for the equality of two circular lists (1979). Duval (1983) obtained another constant-space method from the Lyndon factorization. The simple two-candidate form shown here, with the skip of $k + 1$ positions, is the version that became common in textbooks and programming contests.

## References
