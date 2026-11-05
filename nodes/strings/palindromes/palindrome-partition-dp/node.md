---
tag: 3EX5K9
kind: algorithm
slug: palindrome-partition-dp
name: Palindrome partition dynamic programming
aliases:
- DP for minimum palindrome cuts
- minimum cut palindrome partitioning
area: strings/palindromes
level: core
summary: Tabulates palindrome status of all substrings and computes the minimum cuts in O(n^2) time.
solves: [minimum-palindrome-partition]
model: comparison-model
complexity:
  vars: {n: the length of the string}
  time: {worst: Θ(n^2), best: Θ(n^2)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false, online: true, comparison: true}
prereqs: [minimum-palindrome-partition, interval-dp, dag-dynamic-programming]
see_also: [palindrome-partition-backtracking, palindrome-partitioning, series-links, palindromic-tree, manacher, text-segmentation, optimal-substructure, longest-palindromic-subsequence]
sources:
  - url: https://leetcode.com/problems/palindrome-partitioning-ii/
    title: LeetCode, Problem 132, Palindrome Partitioning II
    locator: the problem statement (return the minimum number of cuts for a palindrome partitioning of s) and its examples
  - paper: doi:10.1016/j.jda.2014.08.001
    title: Gabriele Fici, Travis Gagie, Juha Kärkkäinen and Dominik Kempa, A subquadratic algorithm for minimum palindromic factorization, Journal of Discrete Algorithms 28 (2014), 41-48
    locator: Section 1, Introduction (the problem and earlier work), and the O(n log n) algorithm for a minimum palindromic factorization
  - paper: doi:10.1007/978-3-319-07566-2_16
    title: Tomohiro I, Shiho Sugimoto, Shunsuke Inenaga, Hideo Bannai and Masayuki Takeda, Computing palindromic factorizations and palindromic covers on-line, CPM 2014, Lecture Notes in Computer Science 8486, 150-161
    locator: the on-line computation of a minimum palindromic factorization of each prefix
  - paper: doi:10.1145/322047.322056
    title: Zvi Galil and Joel Seiferas, A linear-time on-line recognition algorithm for Palstar, Journal of the ACM 25(1) (1978), 102-111
    locator: the whole paper (on-line recognition of the concatenations of even palindromes, an early factorization question)
---

Palindrome partition dynamic programming finds the least number of [palindromes](/palindrome/) whose concatenation is a string $s$, and one such partition. It goes over the end positions from left to right. At each end $i$ it finds every palindrome $s[j..i]$ that ends there, with a table of palindromic substrings that it fills in the same loop, and it sets $\mathrm{best}[i+1] = \min_j \mathrm{best}[j] + 1$. The time is $\Theta(n^2)$ and the minimum number of cuts is $\mathrm{best}[n] - 1$. It is the standard solution of the [minimum palindrome partition](/minimum-palindrome-partition/) problem, and the starting point of the faster methods with [series links](/series-links/).

## In plain words

Read the word from left to right. After each new letter, ask: what is the fewest number of palindromes that make up the part read so far? The last piece of such a split is a palindrome that ends at the new letter. So look at each palindrome that ends there, take the best answer for the part before it, and add one. Keep the smallest result. A single letter is always a palindrome, so there is always an answer. To find quickly which pieces that end at the new letter are palindromes, keep a table: a piece is a palindrome if its two end letters match and the piece inside them, which ends one letter earlier, is a palindrome.

## The problem

The input is a string $s = s[0..n-1]$ over an [alphabet](/alphabet/) $\Sigma$, with 0-based indices; $s[j..i]$ includes both ends, and symbols are only tested for equality. The output is the palindromic length $\mathrm{PL}(s)$, the least $k$ such that $s = p_1 p_2 \cdots p_k$ with each $p_t$ a nonempty palindrome, and one such partition. Pieces may be odd or even palindromes. $\mathrm{PL}(\varepsilon) = 0$. Problems that ask for the minimum number of *cuts* want $\mathrm{PL}(s) - 1$ for $n \ge 1$.

## The algorithm

$\mathrm{best}[i]$ is $\mathrm{PL}(s[0..i-1])$, the answer for the prefix of length $i$, and $\mathrm{pal}[j][i]$ is true if $s[j..i]$ is a palindrome; all entries of $\mathrm{pal}$ start as false. $\mathrm{start}[i]$ is the start of the last piece of a best partition of the prefix of length $i$.

```pseudo id=main
PALINDROME-PARTITION-DP(s)                   ▷ s[0 .. n − 1]
L1  best[0] ← 0
L2  for i ← 0 to n − 1 do                    ▷ i is the end of the last piece
L3      best[i + 1] ← ∞
L4      for j ← 0 to i do                    ▷ j is the start of the last piece
L5          if s[j] = s[i] and (i − j < 2 or pal[j + 1][i − 1]) then
L6              pal[j][i] ← true
L7              if best[j] + 1 < best[i + 1] then best[i + 1] ← best[j] + 1, start[i + 1] ← j
L8  i ← n, pieces ← empty list
L9  while i > 0 do put s[start[i] .. i − 1] at the front of pieces, i ← start[i]
L10 return best[n], pieces
```

Line L5 reads column $i - 1$ of the table, which the previous run of the outer loop filled. So one pass fills the table column by column and the answers prefix by prefix.

## Example

Let $s = $ `banana`. The table shows, for each end $i$, the starts $j$ of the palindromes $s[j..i]$, then $\mathrm{best}[i+1]$ and $\mathrm{start}[i+1]$.

| $i$ | $s[i]$ | starts $j$ with $s[j..i]$ a palindrome | $\mathrm{best}[i+1]$ | $\mathrm{start}[i+1]$ |
| --- | --- | --- | --- | --- |
| 0 | b | 0 | 1 | 0 |
| 1 | a | 1 | 2 | 1 |
| 2 | n | 2 | 3 | 2 |
| 3 | a | 1 (`ana`), 3 | 2 | 1 |
| 4 | n | 2 (`nan`), 4 | 3 | 2 |
| 5 | a | 1 (`anana`), 3 (`ana`), 5 | 2 | 1 |

So $\mathrm{PL}(\texttt{banana}) = 2$, and one cut is enough. Lines L8 and L9 follow $\mathrm{start}[6] = 1$ and then $\mathrm{start}[1] = 0$, which gives the pieces `b` and `anana`. At $i = 5$ the start $j = 3$ gives $\mathrm{best}[3] + 1 = 4$ and $j = 5$ gives $\mathrm{best}[5] + 1 = 4$, so the long piece wins. For `abaab` the result is 2 with the pieces `a` and `baab`, while the greedy choice of the longest palindromic prefix, `aba`, leads to 3 pieces. For $a^n$ the result is 1, and for `abcabc` it is 6.

## Correctness

The proof has two parts. First, after the run of the outer loop for $i$, column $i$ of $\mathrm{pal}$ is correct: by induction on $i$, since $s[j..i]$ with $i - j \ge 2$ is a palindrome if and only if $s[j] = s[i]$ and $s[j+1..i-1]$ is a palindrome, and the second test reads column $i - 1$. Second, $\mathrm{best}[i] = \mathrm{PL}(s[0..i-1])$, by induction on $i$. In a best partition of $s[0..i]$ the last piece is a palindrome $s[j..i]$ and the pieces before it form a partition of $s[0..j-1]$, which has at least $\mathrm{PL}(s[0..j-1])$ pieces; conversely, a best partition of $s[0..j-1]$ followed by $s[j..i]$ is a partition with $\mathrm{best}[j] + 1$ pieces. So
$$ \mathrm{PL}(s[0..i]) = \min\{\mathrm{PL}(s[0..j-1]) + 1 : 0 \le j \le i,\ s[j..i] \text{ is a palindrome}\}, $$
which lines L3 to L7 compute; the set is not empty because $j = i$ is in it. The pointers $\mathrm{start}$ record a $j$ that reaches the minimum, so lines L8 and L9 rebuild a partition with $\mathrm{best}[n]$ pieces. The full proof is in the proof file of this page.

## Complexity

**Time.** Line L4 runs $\sum_{i=0}^{n-1} (i + 1) = n(n+1)/2$ times, each in $O(1)$ time, and lines L8 and L9 take $O(n)$. So the time is $\Theta(n^2)$ on every input of length $n$: the loops do not stop early.

**Space.** $\Theta(n^2)$ for the table $\mathrm{pal}$ and $\Theta(n)$ for $\mathrm{best}$ and $\mathrm{start}$. The table can be a matrix of booleans, $n^2/8$ bytes when packed.

- **Linear space.** Expand around each of the $2n - 1$ centers, from left to right, and for each palindrome $s[l..r]$ found, set $\mathrm{best}[r+1] \gets \min(\mathrm{best}[r+1], \mathrm{best}[l] + 1)$. When $s[l..r]$ is found, each palindrome that ends at $l - 1$ has a center to the left of the current one, so $\mathrm{best}[l]$ is already final. This takes $\Theta(n)$ space, and $O(n + N_{\mathrm{occ}}(s))$ time, where $N_{\mathrm{occ}}(s) \le n(n+1)/2$ is the number of palindromic occurrences.
- **Faster methods.** The palindromic suffixes of a prefix form $O(\log n)$ arithmetic progressions of lengths, and [series links](/series-links/) give $O(n \log n)$ time; Borozdin, Kosolobov, Rubinchik and Shur reach $O(n)$. See [minimum palindrome partition](/minimum-palindrome-partition/).

## Properties

- **Online.** $\mathrm{best}[i+1]$ is final as soon as $s[i]$ is read, so the algorithm reports $\mathrm{PL}$ of each prefix one symbol at a time.
- **Ties.** The strict test in line L7 keeps the smallest $j$ among the best ones, which is the longest last piece.
- **Deterministic and not recursive.** Two nested loops and one backward walk.
- **Shortest path.** The recurrence is a shortest path from 0 to $n$ in the DAG on the positions $0, \ldots, n$ with an edge $j \to i + 1$ for each palindrome $s[j..i]$, computed in topological order, as in [DAG dynamic programming](/dag-dynamic-programming/).

## Variants and improvements

- **Interval form.** A common textbook form fills $\mathrm{pal}[i][j]$ by increasing length first, in a separate pass, and then runs the prefix recurrence. It does the same work but is not online.
- **Suffix form.** $\mathrm{best}'[i] = \min\{\mathrm{best}'[j+1] + 1 : s[i..j] \text{ is a palindrome}\}$ over suffixes, filled from $i = n - 1$ down to 0, gives the same value.
- **Counting.** Replace $\min$ and $+1$ by a sum to count the partitions, as on the [palindrome partitioning](/palindrome-partitioning/) page.
- **Weighted pieces.** A cost per piece that depends on its length or its position keeps the same loops; only line L7 changes.
- **Restricted pieces.** For even palindromes only, or for pieces of length at least $\ell$, skip the other starts in line L7, and $\mathrm{best}[n] = \infty$ means that no partition exists.

## When to use it

Use it for strings of up to a few thousand symbols, or when the code must be short. For long strings, use the linear-space variant, which needs only $O(n)$ memory, or the $O(n \log n)$ method with the [palindromic tree](/palindromic-tree/) and series links. If all partitions are needed, not only one with the fewest pieces, use [backtracking](/palindrome-partition-backtracking/).

## Pitfalls

- **Greedy is wrong.** Taking the longest palindromic prefix each time gives 3 pieces on `aaba` and on `abaab`, where 2 are enough.
- **Off by one.** $\mathrm{best}$ has $n + 1$ entries, indexed by prefix length, while $\mathrm{pal}$ is indexed by positions. The number of cuts is $\mathrm{best}[n] - 1$, and 0 for the empty string, not $-1$.
- **Fill order.** $\mathrm{pal}[j+1][i-1]$ must be ready when line L5 reads it. Here it is, because column $i - 1$ is filled before column $i$. A loop that fills a row at a time from the top reads entries that are not yet filled.
- **Even palindromes.** The test $i - j < 2$ handles pieces of length 2; without it, `aa` is missed or the table is read out of range.
- **Memory.** A table of $n^2$ Python booleans takes several bytes per entry; for $n$ near $10^4$, use the linear-space variant.

## Implementations

## History

The prefix recurrence for the fewest palindromic pieces is folklore and is the starting point of the papers that improve it. Fici, Gagie, Kärkkäinen and Kempa (2014) and, at the same time, I, Sugimoto, Inenaga, Bannai and Takeda (2014) gave $O(n \log n)$ algorithms, by grouping the palindromic suffixes of each prefix into $O(\log n)$ series. Earlier, Galil and Seiferas (1978) recognized the concatenations of even palindromes, the language Palstar, online in linear time. The minimum-cut form is a standard programming exercise, such as LeetCode problem 132.

## References
