---
tag: PTQRP5
kind: algorithm
slug: booth-algorithm
name: Booth's algorithm
aliases:
- Booth least rotation algorithm
area: strings/string-combinatorics
level: core
summary: Finds the least rotation of a word in linear time using a failure function.
solves: [minimal-rotation, word-conjugacy-testing]
model: comparison-model
complexity:
  vars: {n: the length of the word}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [minimal-rotation, prefix-function, border, lexicographic-order]
see_also: [shiloach-least-rotation, duval-algorithm, lyndon-word, necklace, word-conjugacy, knuth-morris-pratt, circular-pattern-matching, circular-suffix-array]
sources:
  - paper: doi:10.1016/0020-0190(80)90149-0
    title: Kellogg S. Booth, Lexicographically least circular substrings, Information Processing Letters 10(4-5), 1980, 240-242
    locator: the whole paper (the failure function of the doubled string relative to the current candidate, and the linear bound)
  - paper: doi:10.1016/0196-6774(83)90017-2
    title: Jean-Pierre Duval, Factorizing words over an ordered alphabet, Journal of Algorithms 4(4), 1983, 363-381
    locator: the computation of the least conjugate of a word from the Lyndon factorization of the doubled word
  - paper: "Yossi Shiloach, Fast canonization of circular strings, Journal of Algorithms 2(2), 1981, 107-121"
    title: Yossi Shiloach, Fast canonization of circular strings
    locator: the problem of the least rotation and an algorithm with a smaller number of comparisons
  - paper: doi:10.1137/0206024
    title: Donald E. Knuth, James H. Morris and Vaughan R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2), 1977, 323-350
    locator: the failure function and the amortized argument for its linear computation
---

Booth's algorithm finds the lexicographically least rotation of a word $s$ of length $n$: the index $k$ such that $s[k..n-1]\,s[0..k-1]$ is smallest among the $n$ rotations. It scans the doubled word $ss$ once, from left to right, and computes the [prefix function](/prefix-function/) of the part that starts at the current best candidate $k$; a mismatch with a smaller letter moves the candidate forward. It uses $\Theta(n)$ time and $\Theta(n)$ extra space in the [comparison model](/comparison-model/). The least rotation is a canonical form of a cyclic word, so the algorithm also tests whether two words are conjugate.

## In plain words

Write the word on a ring. You want the place to cut the ring so that the letters, read from the cut, come first in dictionary order. Write the word twice in a row, so that each cut becomes a window of the doubled word.

Read the doubled word from the left. Keep one best cut so far. While you read, the text after the best cut is a prefix of the best rotation. Each repeat of the start of that text inside it is a rival cut. A rival survives as long as its letters equal those of the best cut. When a new letter differs, the rival either loses (its letter is larger) or wins and becomes the new best cut. The repeats are tracked with the same table that KMP uses, so each letter costs a constant amount of work on average.

## The problem

The input is a word $s = s[0..n-1]$ over an ordered [alphabet](/alphabet/), with $n \ge 1$; only comparisons $<$, $=$ between letters are used. Indices are 0-based. For $0 \le q < n$, the rotation by $q$ is $R(q) = s[q..n-1]\,s[0..q-1]$. The output is the least $k$ with $R(k) \le R(q)$ for each $q$, in [lexicographic order](/lexicographic-order/). This is the [minimal rotation](/minimal-rotation/) problem. For $n = 0$ the implementation returns 0.

## The algorithm

Let $t = ss$, of length $2n$. For $q \ge 0$ write $R(q) = t'[q..q+n-1]$ where $t' = sss\cdots$; then $R(q) = R(q \bmod n)$. The algorithm keeps a candidate $k$ and the word $x = t[k..j-1]$ read since $k$. The array entry $f[r]$ is the length of the longest proper [border](/border/) of $x[0..r]$, minus one, so $-1$ means "no nonempty border". This is the prefix function of $x$, shifted by one.

```pseudo id=main
LEAST-ROTATION(s)                          ▷ s[0 .. n − 1], n ≥ 1
L1  t ← s · s, f[0 .. 2n − 1] ← −1, k ← 0
L2  for j ← 1 to 2n − 1 do
L3      c ← t[j], i ← f[j − k − 1]          ▷ i + 1 = longest border of x = t[k .. j − 1]
L4      while i ≠ −1 and c ≠ t[k + i + 1] do
L5          if c < t[k + i + 1] then k ← j − i − 1
L6          i ← f[i]
L7      if i = −1 and c ≠ t[k] then
L8          if c < t[k] then k ← j
L9          f[j − k] ← −1
L10     else f[j − k] ← i + 1
L11 return k
```

Line L3 takes the longest border $b = x[0..i]$ of $x$. Its second occurrence starts at $j - i - 1$, a rival candidate whose first $i + 1$ letters equal those of the candidate $k$. Line L4 compares the next letter $c$ of the rival with the next letter $x[i+1]$ of the candidate. If they differ and $c$ is smaller, the rival is the better rotation, and line L5 moves $k$ to it. Then $x$ becomes $b$, which is a prefix of the old $x$, so the table $f[0..i]$ is still right for it. In both cases line L6 moves to the next shorter border, the next rival. When the loop stops, either a rival matched $c$, and line L10 records the border $bc$ of $xc$, or no rival is left. In the second case line L7 compares $c$ with the first letter of the candidate: the position $j$ is itself a rival of length 1. If $c$ is smaller, line L8 restarts the candidate at $j$.

## Example

Let $s = $ `cabaab`, $n = 6$, so $t = $ `cabaabcabaab`. The column $x$ is $t[k..j]$ after the step, and "border" is $f[j-k] + 1$, the length of its longest border.

| $j$ | $t[j]$ | $k$ before | what happens | $k$ after | $x$ | border |
|---|---|---|---|---|---|---|
| 1 | a | 0 | no border; `a` $<$ `c`, line L8 | 1 | a | 0 |
| 2 | b | 1 | `b` $>$ `a`, line L9 | 1 | ab | 0 |
| 3 | a | 1 | `a` $=$ `a`, line L10 | 1 | aba | 1 |
| 4 | a | 1 | border `a`: `a` $<$ `b`, line L5 moves $k$ to $4 - 0 - 1 = 3$; then `a` $=$ `a` | 3 | aa | 1 |
| 5 | b | 3 | border `a`: `b` $>$ `a`; then `b` $>$ `a` at line L7 | 3 | aab | 0 |
| 6 | c | 3 | `c` $>$ `a` | 3 | aabc | 0 |
| 7 | a | 3 | `a` $=$ `a` | 3 | aabca | 1 |
| 8 | b | 3 | border `a`: `b` $>$ `a`; then `b` $>$ `a` | 3 | aabcab | 0 |
| 9 | a | 3 | `a` $=$ `a` | 3 | aabcaba | 1 |
| 10 | a | 3 | border `a`: `a` $=$ `a` | 3 | aabcabaa | 2 |
| 11 | b | 3 | border `aa`: `b` $=$ `b` | 3 | aabcabaab | 3 |

The output is $k = 3$, and $R(3) = $ `aabcab`. The six rotations are `cabaab`, `abaabc`, `baabca`, `aabcab`, `abcaba` and `bcabaa`, and `aabcab` is the least. At $j = 4$ the rival at index 3 beats the candidate at index 1, because `aa` $<$ `ab`. The rivals at indices 9 and 10 survive to the end; they are the repeats of the start of $R(3)$ in the second copy.

## Correctness

The proof uses this [loop invariant](/loop-invariant/) at the start of the iteration for $j$, with $x = t[k..j-1]$ nonempty: the table $f[0..|x|-1]$ is the shifted prefix function of $x$; and each index $q < j$ other than $k$ either has $R(q) \ge R(k)$, or has $q > k$ with $t[q..j-1]$ a border of $x$ (a rival not yet decided). A mismatch inside the loop decides one rival, and a move of $k$ happens only to a strictly smaller rotation, so the decided facts carry over by transitivity. At $j = 2n$, each undecided rival $q < n$ has $t[q..2n-1]$, of length more than $n$, as a prefix of $x$, so $R(q) = R(k)$. The full proof, with the argument that the output is the least index and lies in $[0, n)$, is in the proof file.

## Complexity

- **Comparisons.** Let $\beta_j = f[j-k-1] + 1$ be the length of the longest border of $x$ at the start of the iteration $j$, with $\beta_1 = 0$. Each pass of the loop of line L4 replaces $i$ by $f[i] < i$, so after $B_j$ passes the final $i$ is at most $\beta_j - 1 - B_j$. Line L10 then sets the border of the new $x$ to $i + 2 \le \beta_j - B_j + 1$, and line L9 sets it to 0. So $\beta_{j+1} \le \beta_j + 1 - B_j$, and summing over $j = 1, \ldots, 2n-1$ gives $\sum_j B_j \le 2n - 1 + \beta_1 - \beta_{2n} \le 2n - 1$. Each pass costs two letter comparisons, and each iteration has at most two more (the failed test of line L4, or the tests of lines L7 and L8). The total is at most $4(2n - 1) = 8n - 4$ comparisons. Over all binary words of length $n$ for $2 \le n \le 12$, the largest count is $6n - 7$.
- **Time.** Each comparison and each line costs $O(1)$, so the time is $\Theta(n)$ in the worst case. The loop of line L2 runs $2n - 1$ times on every input, so the best case is also $\Theta(n)$.
- **Space.** The table $f$ and the word $t$ take $\Theta(n)$ cells. The word $t$ need not be stored: use $s[q \bmod n]$ for $t[q]$.

## Properties

- **Ordered alphabet only.** The algorithm compares letters; it does not index tables by letters, so it works for any total order.
- **Least index.** On a periodic word such as `abab`, several indices give the least rotation. The algorithm returns the smallest one, 0 for `abab`, because $k$ moves only to a strictly smaller rotation.
- **Deterministic and not online.** The output depends on the whole word; a new last letter can change the answer completely.

## Variants and improvements

- **Duval's method.** The least rotation of $s$ starts at the start of the last [Lyndon factor](/lyndon-factorization/) of $ss$ that begins in the first copy, so a run of [Duval's algorithm](/duval-algorithm/) on $ss$ gives a least rotation in $O(n)$ time and $O(1)$ extra space. It is not always the least index: on `abab` the factors of $ss$ are `ab` four times, and the method returns 2.
- **The two-pointer method.** Keep two candidates $i < j$ and the length $\ell$ of their common prefix; on a mismatch, the losing candidate jumps past the compared part. It also runs in $O(n)$ time with $O(1)$ extra space. See [minimal rotation](/minimal-rotation/).
- **[Shiloach's algorithm](/shiloach-least-rotation/).** A linear algorithm with a smaller constant in the number of comparisons.
- **Conjugacy test.** Words $u$ and $v$ of the same length are [conjugate](/word-conjugacy/) if and only if their least rotations are equal, so two runs of Booth's algorithm and one comparison answer [word conjugacy testing](/word-conjugacy-testing/).
- **Least rotation for all rotations.** The [circular suffix array](/circular-suffix-array/) sorts all rotations, and its first entry is the least one, at a higher cost.

## When to use it

Use Booth's algorithm to put a cyclic word in canonical form, for example to deduplicate necklaces, to compare cyclic chemical or polygon codes, or to hash a cyclic sequence. It is short and its bound is a worst case. If memory matters, Duval's method and the two-pointer method need only $O(1)$ extra cells. If you need the order of all rotations, build a circular suffix array instead.

## Pitfalls

- **Wrong comparison direction.** Lines L5 and L8 must move $k$ when the new letter $c$ is smaller. With $c > t[k+i+1]$ and $c > t[k]$ the result is wrong: on `ba` it is 0 instead of 1.
- **Index of the new table entry.** Lines L9 and L10 write $f[j - k]$ with the value of $k$ after the move. Writing $f[j - k_{\text{old}}]$ corrupts the table of the new candidate.
- **Single copy.** Running $j$ only to $n - 1$ misses rivals whose comparison wraps around the end of $s$; on `ab` the scan of one copy is fine, but on `aba` it returns 0 instead of 2.

## Implementations

## History

Kellogg S. Booth published the algorithm in 1980 in Information Processing Letters, as a way to compute a canonical form of circular strings in linear time with a modified failure function. Shiloach gave another linear algorithm in 1981, and Duval's 1983 algorithm for the Lyndon factorization gives a third method with constant extra space.

## References
