---
tag: KM91EN
kind: problem
slug: minimal-rotation
name: Minimal rotation
aliases:
- least rotation
- canonical rotation
- minimum cyclic shift
area: strings/string-combinatorics
level: core
summary: Find the lexicographically smallest rotation of a word.
model: comparison-model
complexity:
  vars: {n: the length of the word}
  time: {worst: Θ(n)}
  space: {aux: Θ(1)}
prereqs: [word-conjugacy, lexicographic-order]
see_also: [booth-algorithm, shiloach-least-rotation, duval-algorithm, necklace, lyndon-word, word-conjugacy-testing, circular-pattern-matching, circular-suffix-array]
sources:
  - paper: doi:10.1016/0020-0190(80)90149-0
    title: Kellogg S. Booth, Lexicographically least circular substrings, Information Processing Letters 10(4-5), 1980, 240-242
    locator: the whole paper (a linear-time algorithm based on the failure function of Knuth, Morris and Pratt)
  - paper: doi:10.1016/0196-6774(81)90013-4
    title: Yossi Shiloach, Fast canonization of circular strings, Journal of Algorithms 2(2), 1981, 107-121
    locator: the main algorithm (all least starting points with at most n + ⌈d/2⌉ comparisons and constant extra space)
  - paper: doi:10.1016/0196-6774(83)90017-2
    title: Jean-Pierre Duval, Factorizing words over an ordered alphabet, Journal of Algorithms 4(4), 1983, 363-381
    locator: the factorization algorithm and its application to the least circular shift
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1, Generating all n-tuples (necklaces as least rotations, and the exercises on testing for the least rotation)
---

The minimal rotation problem asks for the lexicographically smallest word among the $n$ rotations of a word of length $n$, together with a starting index where it begins. The answer is a canonical name for the word read around a circle: two words are rotations of each other exactly when their least rotations are equal. Comparing all rotations costs $\Theta(n^2)$ letter comparisons in the worst case, while [Booth's algorithm](/booth-algorithm/), [Shiloach's algorithm](/shiloach-least-rotation/) and [Duval's factorization](/duval-algorithm/) of the doubled word all take $O(n)$ time.

## In plain words

Write a word around a circle, like beads on a ring. You can start reading at any bead and go once around, and each starting bead gives a different-looking word. The task is to find the starting bead that gives the word that would come first in a dictionary. That word is a fair name for the ring, because it does not depend on where the ring was cut. Trying every start and comparing whole words is slow on long rings. The fast methods compare two candidate starts letter by letter, and when one loses, they throw out a whole stretch of starts at once, so each bead is passed over only a few times.

## Definition

**Input.** A word $s = s[0..n-1]$ with $n \ge 1$ over an [alphabet](/alphabet/) $\Sigma$ with a total order. Algorithms access letters only by three-way comparisons $s[i] < s[j]$, $s[i] = s[j]$ or $s[i] > s[j]$, so the alphabet may be of any size. Indices are 0-based.

**Rotations.** $\mathrm{rot}_i(s) = s[i..n-1]\,s[0..i-1]$ for $0 \le i \le n - 1$, so $\mathrm{rot}_i(s)[t] = s[(i + t) \bmod n]$; these are the [conjugates](/word-conjugacy/) of $s$.

**Output.** The least index $i^\ast$ such that $\mathrm{rot}_{i^\ast}(s) \le \mathrm{rot}_j(s)$ for all $j$, in [lexicographic order](/lexicographic-order/). The least rotation itself is $\mathrm{rot}_{i^\ast}(s)$.

**All minimal starts.** If $d$ is the length of the primitive root of $s$, the indices $j$ with $\mathrm{rot}_j(s) = \mathrm{rot}_{i^\ast}(s)$ are exactly $i^\ast, i^\ast + d, i^\ast + 2d, \ldots$, by the class-size fact on the [conjugacy](/word-conjugacy/) page. So $i^\ast < d$, and $i^\ast$ and $d$ together give all minimal starts.

## Variants

- **All least starting points.** Report every index where the least rotation begins; by the fact above this adds only the computation of $d$. Shiloach's algorithm returns them directly.
- **Maximal rotation.** The same problem with the order of $\Sigma$ reversed.
- **Canonical form of a bracelet.** The least word among the rotations of $s$ and of its reversal: two minimal-rotation computations and one comparison. See [bracelet](/bracelet/).
- **Necklace and Lyndon tests.** Decide whether $s$ itself is its least rotation (a [necklace](/necklace/) in the word sense), or the unique least one (a [Lyndon word](/lyndon-word/)).
- **Rotations of substrings.** Many queries, each asking for the least rotation of a factor $s[i..j]$, answered by data structures built on the whole word.
- **Least suffix and least rotation of every prefix.** Related online problems where the word grows one letter at a time.

## Examples

| $s$ | $n$ | least rotation | $i^\ast$ |
| --- | --- | --- | --- |
| `bca` | 3 | `abc` | 2 |
| `abaab` | 5 | `aabab` | 2 |
| `abab` | 4 | `abab` | 0 |
| `baabaa` | 6 | `aabaab` | 1 |
| `alfalfa` | 7 | `aalfalf` | 6 |
| `cabbage` | 7 | `abbagec` | 1 |
| `bbaaccaadd` | 10 | `aaccaaddbb` | 2 |
| `mississippi` | 11 | `imississipp` | 10 |
| `aaaa` | 4 | `aaaa` | 0 |

In `baabaa` the least rotation starts at both 1 and 4, since the primitive root has length $d = 3$; the answer is the smaller index. In `bbaaccaadd` the runs `aa` at positions 2 and 6 tie for two letters, and the third letter decides: `c` after the first, `d` after the second. A method that looks only at the first few letters picks the wrong start on such inputs.

## Known algorithms

**All rotations, $\Theta(n^2)$.** Compare the $n$ rotations in turn, keeping the least. Each comparison of two rotations costs up to $n$ letter comparisons, so the worst case, reached on $a^n$, is about $n^2$. It is the reference for testing the others.

**Sorting the rotations.** A [suffix array](/suffix-array/) of $ss$, or a [circular suffix array](/circular-suffix-array/) of $s$, lists the rotations in order, so its first entry with index below $n$ gives a least rotation. This costs $O(n)$ for an integer alphabet, more than needed, but the array answers many other questions at the same time.

**Booth's algorithm, $O(n)$.** Booth (1980) runs the failure function of [Knuth-Morris-Pratt](/knuth-morris-pratt/) over $ss$ and moves the candidate start each time a smaller letter appears; see [Booth's algorithm](/booth-algorithm/). It uses $\Theta(n)$ extra space for the failure table and at most about $3n$ comparisons.

**Shiloach's algorithm, $O(n)$ and $O(1)$ space.** Keep two candidate starts and compare their rotations letter by letter. When they first differ after $k$ equal letters, the larger candidate and the $k$ starts after it cannot be least, so they are discarded together. Shiloach (1981) refined this to at most $n + \lceil d/2 \rceil$ comparisons with constant extra space; see [Shiloach's least rotation](/shiloach-least-rotation/), which also gives the simple two-pointer form with a full proof.

**Lyndon factorization of $ss$, $O(n)$ and $O(1)$ space.** Run [Duval's algorithm](/duval-algorithm/) on $t = ss$. The least rotation starts at the first index of the last block of equal [Lyndon](/lyndon-word/) factors that begins before position $n$:

```pseudo id=duval-ss
LEAST-ROTATION-BY-DUVAL(s)          ▷ s[0 .. n − 1], t = ss
L1  i ← 0, ans ← 0
L2  while i < n do
L3      ans ← i, j ← i + 1, k ← i
L4      while j < 2n and t[k] ≤ t[j] do
L5          if t[k] < t[j] then k ← i else k ← k + 1
L6          j ← j + 1
L7      while i ≤ k do i ← i + j − k
L8  return ans
```

*Why it works.* A rotation $\mathrm{rot}_i(s)$ is the prefix of length $n$ of the suffix $t[i..2n-1]$, and if two such prefixes differ, the suffixes compare the same way, so a least suffix of $t$ among those starting before $n$ starts a least rotation. Duval (1983) shows that this least suffix starts at a boundary of the Lyndon factorization of $t$, at the first copy of the last block of equal factors that begins before $n$. Line L7 jumps over a whole block of equal factors, so $ans$ holds the first index of the block, which is the least minimal start.

**History.** Booth (1980) gave the first linear-time solution, and Shiloach (1981) reduced the comparison count to $n + \lceil d/2 \rceil$ with constant space. Duval (1983) derived the problem from the Lyndon factorization, in linear time with constant space. The two-pointer elimination form became the standard in programming practice.

## Bounds

**Upper bound.** $O(n)$ time and $O(1)$ extra space, by Shiloach's algorithm or Duval's.

**Lower bound.** In the comparison model, at least $\lceil (n-1)/2 \rceil$ comparisons are needed in the worst case, for an alphabet with at least two letters $a < b$. *Proof.* Run an algorithm on $s = b^n$; it must answer 0. Suppose some index $j \ge 1$ takes part in no comparison. Change $s[j]$ to $a$: every comparison gives the same result as before, so the algorithm again answers 0, but now $\mathrm{rot}_j(s)$ starts with $a$ and is the unique least rotation, so the answer should be $j$. So each of the $n - 1$ indices $1, \ldots, n-1$ takes part in a comparison, and each comparison involves at most two indices. $\square$ Together with the upper bound, $\Theta(n)$ is the exact order.

## Reductions

- **Conjugacy testing to minimal rotation.** $u$ and $v$ of equal length are conjugate if and only if their least rotations are equal, so [conjugacy testing](/word-conjugacy-testing/) costs two minimal rotations and one comparison of words.
- **Necklace test.** $s$ is a necklace in the word sense if and only if $i^\ast = 0$, and a Lyndon word if moreover $d = n$.
- **Minimal rotation to Lyndon factorization.** As in the Duval method above.
- **Minimal rotation to suffix sorting.** As in the suffix array method above, via the doubled word $ss$.

## Applications

- **Canonical forms of circular data.** Cyclic molecules, closed polygonal shapes coded by edge directions (chain codes), and circular DNA such as plasmids are stored by their least rotation, so equal objects get equal keys for hashing and sorting.
- **Necklace and Lyndon word algorithms.** Generation and ranking of [necklaces](/necklace/) need the test "is this word its least rotation".
- **Circular string matching.** [Circular pattern matching](/circular-pattern-matching/) searches for all rotations of a pattern; a canonical rotation reduces some versions to ordinary matching.
- **Graph canonization.** A cycle labeled by letters, or a planar map around a vertex, is put in canonical form by its least rotation.

## References
