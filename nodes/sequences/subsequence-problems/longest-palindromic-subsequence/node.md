---
tag: Q5069X
kind: problem
slug: longest-palindromic-subsequence
name: Longest palindromic subsequence
aliases:
- LPS
area: sequences/subsequence-problems
level: core
summary: Find the longest subsequence of a string that reads the same forwards and backwards.
prereqs: [longest-common-subsequence, palindrome, interval-dp]
see_also: [longest-palindromic-substring, lcs-dynamic-programming, distinct-subsequences, bit-parallel-lcs, hirschberg-lcs, traceback]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 15, Problem 15-2, Longest palindrome subsequence (with the example character and carac)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 6 exercises, the exercise on the longest palindromic subsequence in O(n^2) time
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.4, the LCS table, which gives the length through the string and its reverse
---

The longest palindromic subsequence problem asks for a longest [subsequence](/subsequence/) of a string $S$ of length $n$ that is a [palindrome](/palindrome/), that is, that reads the same from left to right and from right to left. For example, the longest palindromic subsequence of "character" is "carac". An [interval DP](/interval-dp/) over the factors $S[i \ldots j]$ solves it in $\Theta(n^2)$ time, and its length equals $\mathrm{lcs}(S, S^R)$, the [longest common subsequence](/longest-common-subsequence/) of $S$ and its reverse. The length also gives the least number of letters that must be inserted into $S$, or deleted from it, to make a palindrome: $n$ minus the length. The contiguous version is a different problem, the [longest palindromic substring](/longest-palindromic-substring/).

## In plain words

Cross out some letters of a word so that what is left reads the same both ways, and cross out as few as you can. From "character" you can keep "carac".

Look at the first and the last letter. If they are equal, keep both: they can be the two ends of the answer, and the rest of the answer comes from the letters between them. If they are not equal, at least one of them is not in the answer, so try the word without its first letter and the word without its last letter, and keep the better. A table over all pieces of the word, from short to long, gives each answer from shorter pieces.

## Definition

**Input.** A string $S = s_1 \cdots s_n$ over an alphabet $\Sigma$.

**Output.** A palindromic subsequence $P \preceq S$ of maximum length $\mathrm{lps}(S)$, or only this length.

**The recurrence.** Let $p(i, j) = \mathrm{lps}(s_i \cdots s_j)$, with $p(i, i - 1) = 0$ for the empty factor and $p(i, i) = 1$. For $i < j$:

$$p(i, j) = \begin{cases} p(i + 1, j - 1) + 2 & \text{if } s_i = s_j, \\ \max(p(i + 1, j),\ p(i, j - 1)) & \text{if } s_i \ne s_j. \end{cases}$$

*Proof.* Let $i < j$ and let $P$ be a longest palindromic subsequence of $s_i \cdots s_j$, with positions $t_1 < \cdots < t_\ell$.

If $s_i \ne s_j$: $P$ cannot use both $i$ and $j$, since its first and last items are equal (for $\ell \ge 2$; for $\ell \le 1$ there is nothing to show). So it is a palindromic subsequence of $s_{i+1} \cdots s_j$ or of $s_i \cdots s_{j-1}$, and $p(i, j) \le \max(p(i+1, j), p(i, j-1))$. The other direction holds because both factors are inside $s_i \cdots s_j$.

If $s_i = s_j$: for $\ge$, put $s_i$ and $s_j$ around a longest palindromic subsequence of $s_{i+1} \cdots s_{j-1}$. For $\le$, if $\ell \le 1$ the bound $\ell \le 2 \le p(i+1, j-1) + 2$ holds. If $\ell \ge 2$, remove the first and last items of $P$: the middle $P'$ is a palindrome of length $\ell - 2$ with positions strictly between $t_1 \ge i$ and $t_\ell \le j$, so inside $s_{i+1} \cdots s_{j-1}$. Hence $\ell - 2 \le p(i + 1, j - 1)$, and $\ell \le p(i+1, j-1) + 2$. $\square$

```pseudo id=lps
LPS-LENGTH(S[1 .. n])
L1  for i ← n downto 1 do
L2      p[i, i] ← 1; p[i, i − 1] ← 0
L3      for j ← i + 1 to n do
L4          if S[i] = S[j] then p[i, j] ← p[i + 1, j − 1] + 2
L5          else p[i, j] ← max(p[i + 1, j], p[i, j − 1])
L6  return p[1, n]
```

The rows are filled from the bottom, so the cells $(i + 1, \cdot)$ are ready when row $i$ needs them. A [traceback](/traceback/) from $(1, n)$ gives the palindrome: on equal ends, write $s_i$ at the front and $s_j$ at the back and go to $(i + 1, j - 1)$; else go to the neighbour with the same value; at a cell $(i, i)$, put $s_i$ in the middle.

**Through the LCS.** $\mathrm{lps}(S) = \mathrm{lcs}(S, S^R)$.

*Proof.* A palindrome $P \preceq S$ satisfies $P = P^R \preceq S^R$, so it is a common subsequence, and $\mathrm{lps}(S) \le \mathrm{lcs}(S, S^R)$. Conversely, let $Z$ be a common subsequence of $S$ and $S^R$ of length $L$. Its embedding in $S^R$, read in $S$, gives positions $j_1 > j_2 > \cdots > j_L$ with $s_{j_t} = z_t$, and its embedding in $S$ gives $i_1 < \cdots < i_L$ with $s_{i_t} = z_t$. The value $i_t - j_t$ increases with $t$. Let $a$ be the number of $t$ with $i_t < j_t$, $b$ the number with $i_t > j_t$, and $e \le 1$ the number with $i_t = j_t$. The positions $i_1 < \cdots < i_a < j_a < \cdots < j_1$ hold $z_1 \cdots z_a z_a \cdots z_1$, a palindrome of length $2a$, and if $e = 1$ the position $i_{a+1} = j_{a+1}$ lies between $i_a$ and $j_a$ and can be its middle. In the same way the last $b$ indices give a palindrome of length $2b$ (with the middle if $e = 1$). One of the two has length at least $a + b + e = L$. $\square$

A longest common subsequence of $S$ and $S^R$ need not itself be a palindrome; the proof shows how to get one of the same length.

## Variants

- **Fewest insertions to a palindrome.** The least number of letters to insert into $S$ to make it a palindrome is $n - \mathrm{lps}(S)$. Insert the mirror of each letter that is not in a longest palindromic subsequence; conversely, in a palindrome $Q$ of length $n + t$ that contains $S$, pair each position with its mirror; at most $t$ letters of $S$ are paired with an inserted letter, so the others form a palindromic subsequence of $S$ of length at least $n - t$.
- **Fewest deletions.** Deleting the $n - \mathrm{lps}(S)$ letters outside a longest palindromic subsequence is optimal, by definition.
- **$k$-palindromes.** Decide whether $S$ becomes a palindrome after at most $k$ deletions, that is, whether $n - \mathrm{lps}(S) \le k$. Only the cells $(i, j)$ of the table that can be reached with at most $k$ deletions matter, which gives $O(nk)$ time.
- **Counting palindromic subsequences.** The number $C(i, j)$ of non-empty index sets of $s_i \cdots s_j$ that spell a palindrome satisfies $C(i, j) = C(i+1, j) + C(i, j-1) - C(i+1, j-1)$, plus $C(i+1, j-1) + 1$ if $s_i = s_j$. For "character" it is 23. Counting distinct palindromes is the palindromic case of [counting distinct subsequences](/distinct-subsequences/).
- **Substring instead of subsequence.** If the palindrome must be contiguous, the problem is the [longest palindromic substring](/longest-palindromic-substring/), solved in linear time by Manacher's algorithm.

## Examples

| $S$ | lps | one longest palindromic subsequence |
| --- | --- | --- |
| character | 5 | carac |
| BBABCBCAB | 7 | BACBCAB |
| agbdba | 5 | abdba |
| ABCBDAB | 5 | ABCBA |
| abcd | 1 | any one letter |
| aaaa | 4 | aaaa |

The table $p(i, j)$ for $S = $ agbdba (row $i$, column $j$, entries below the diagonal empty):

| $i \backslash j$ | 1 a | 2 g | 3 b | 4 d | 5 b | 6 a |
| --- | --- | --- | --- | --- | --- | --- |
| 1 a | 1 | 1 | 1 | 1 | 3 | 5 |
| 2 g | | 1 | 1 | 1 | 3 | 3 |
| 3 b | | | 1 | 1 | 3 | 3 |
| 4 d | | | | 1 | 1 | 1 |
| 5 b | | | | | 1 | 1 |
| 6 a | | | | | | 1 |

The traceback from $(1, 6)$: a = a, go to $(2, 5)$; g $\ne$ b and $p(3, 5) = 3 \ge p(2, 4) = 1$, go to $(3, 5)$; b = b, go to $(4, 4)$, the middle d. The result is abdba, and agbdba needs $6 - 5 = 1$ insertion (a g after the second b) to become the palindrome agbdbga.

## Known algorithms

- **Interval DP.** LPS-LENGTH fills $\binom{n+1}{2}$ cells in $\Theta(n^2)$ time and space; the length alone needs two rows, so $\Theta(n)$ space.
- **LCS methods on $S$ and $S^R$.** Each [LCS](/longest-common-subsequence/) algorithm applies: the [table](/lcs-dynamic-programming/), [Hirschberg's](/hirschberg-lcs/) linear-space method for the palindrome itself (after the conversion in the proof above), or the [bit-parallel](/bit-parallel-lcs/) method for the length in $O(n^2 / w)$ word operations.
- **Memoized recursion.** The recurrence with memoization computes the same cells top-down.

## Bounds

- **Range.** $\lceil n / \sigma \rceil \le \mathrm{lps}(S) \le n$ for $n \ge 1$, where $\sigma$ is the number of distinct letters: the most frequent letter occurs at least $\lceil n / \sigma \rceil$ times, and its copies form a palindrome. $\mathrm{lps}(S) = n$ exactly when $S$ is a palindrome.
- **Time.** $O(n^2)$ by the DP, and $\Omega(n)$ since each letter must be read.

## Reductions

- **To LCS.** $\mathrm{lps}(S) = \mathrm{lcs}(S, S^R)$, shown above.
- **To interval DP.** The recurrence is an [interval DP](/interval-dp/): each factor depends on factors one or two letters shorter.
- **To shortest common supersequence.** A shortest palindrome that contains $S$ as a subsequence has length $2n - \mathrm{lps}(S)$, by the insertion variant.

## Applications

- **Fewest edits to a palindrome.** The insertion and deletion variants are standard tasks in programming contests and exercises.
- **Teaching interval DP.** It is a common first example of a table indexed by the two ends of a factor.

## References
