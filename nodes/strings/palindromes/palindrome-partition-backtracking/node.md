---
tag: 8C52F0
kind: algorithm
slug: palindrome-partition-backtracking
name: Palindrome partition by backtracking
aliases:
- backtracking palindrome partitioning
area: strings/palindromes
level: core
summary: Recursively tries each palindromic prefix and enumerates all partitions.
solves: [palindrome-partitioning]
model: comparison-model
complexity:
  vars: {n: the length of the string, P: the number of palindromic partitions}
  time: {worst: Θ(n^2 + n P), best: Θ(n^2 + n P)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false, online: false, comparison: true}
prereqs: [palindrome-partitioning, generic-backtracking-algorithm, interval-dp]
see_also: [palindrome-partition-dp, minimum-palindrome-partition, state-space-tree, chronological-backtracking, power-set-enumeration, manacher, text-segmentation]
sources:
  - url: https://leetcode.com/problems/palindrome-partitioning/
    title: LeetCode, Problem 131, Palindrome Partitioning
    locator: the problem statement (return all partitions of s into palindromic substrings) and its examples
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms, Part 2
    locator: Section 7.2.2, Backtrack programming (the basic backtrack algorithm and its explicit-stack form)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 14, Problem 14-2, Longest palindrome subsequence (the interval table of palindromic substrings)
---

Palindrome partition by backtracking lists every way to cut a string into [palindromes](/palindrome/). It first builds a table of which substrings are palindromes, then runs a depth-first search that, at each position, tries every palindrome that starts there and goes on from its end. Every branch of the search ends in a full partition, so the time is $\Theta(n^2 + nP)$ for $P$ partitions, which is optimal for an algorithm that writes each partition out. This version keeps the search on an explicit stack, so its depth does not depend on the call stack of the language.

## In plain words

Stand at the start of the word. Look at every piece that starts here and reads the same from both ends; a single letter always does. Take the shortest such piece first, step to the end of it, and do the same thing from there. When you reach the end of the word, write down the pieces you took. Then go back one step and take the next longer piece at that point instead. When there is no longer piece, go back one more step. To avoid testing the same piece again and again, first make a table that says, for each start, where the palindromes from that start end. Since a single letter is always possible, no path is a dead end.

## The problem

The input is a string $s = s[0..n-1]$ over an [alphabet](/alphabet/) $\Sigma$, with 0-based indices; symbols are only tested for equality. The output is every partition of $s$ into nonempty palindromic pieces, each one time, as defined on the [palindrome partitioning](/palindrome-partitioning/) page. Pieces may be odd or even palindromes. The empty string has one partition, with no pieces.

## The algorithm

Lines L1 to L4 fill the table $\mathrm{pal}[i][j]$ (true if $s[i..j]$ is a palindrome) by the interval recurrence, row $i$ from $n - 1$ down to 0, so that $\mathrm{pal}[i+1][j-1]$ is ready when it is read. They also build, for each start $i$, the list $\mathit{ends}[i]$ of the ends $j$ of the palindromes $s[i..j]$, in increasing order. Lines L5 to L11 are the search. A frame $(i, k)$ on the stack means: the pieces on $\mathit{path}$ cover $s[0..i-1]$, and the next piece to try at position $i$ is the one that ends at $\mathit{ends}[i][k]$.

```pseudo id=main
PALINDROME-PARTITIONS(s)                       ▷ s[0 .. n − 1]
L1  for i ← n − 1 downto 0 do
L2      for j ← i to n − 1 do
L3          pal[i][j] ← (s[i] = s[j]) and (j − i < 2 or pal[i + 1][j − 1])
L4          if pal[i][j] then append j to ends[i]
L5  path ← empty list, S ← stack with the frame (0, 0)
L6  while S is not empty do
L7      (i, k) ← top of S
L8      if i = n then output path, pop S, and if i > 0 remove the last piece of path
L9      else if k = |ends[i]| then pop S, and if i > 0 remove the last piece of path
L10     else set the top of S to (i, k + 1), j ← ends[i][k]
L11         append s[i .. j] to path, push (j + 1, 0) onto S
```

Line L8 is a leaf of the search: a full partition. Line L9 is the end of the choices at position $i$: the search goes back, and the piece that led to position $i$ is removed. Lines L10 and L11 take the next choice and go one level deeper. The stack holds at most $n + 1$ frames, one per piece plus the root.

## Example

Let $s = $ `abaab`. The table gives $\mathit{ends} = [[0, 2], [1, 4], [2, 3], [3], [4]]$: from position 0 the palindromes `a` and `aba`, from 1 `b` and `baab`, from 2 `a` and `aa`, and only single symbols from 3 and 4. The search tree, with the pieces on its edges, is:

| depth 1 | depth 2 | depth 3 | depth 4 | depth 5 | output |
| --- | --- | --- | --- | --- | --- |
| a | b | a | a | b | a, b, a, a, b |
| a | b | aa | b | | a, b, aa, b |
| a | baab | | | | a, baab |
| aba | a | b | | | aba, a, b |

The outputs come in this order, because each list $\mathit{ends}[i]$ is increasing: the first one is the split into single symbols, and the last one starts with the longest first piece. So $P = 4$. For `abcabc` each list has one entry and the search finds only the split into single symbols. For $a^n$ every list $\mathit{ends}[i]$ is $[i, i+1, \ldots, n-1]$, and the search outputs all $2^{n-1}$ sets of cuts.

## Correctness

The table is correct by induction on $j - i$: a substring of length 1 or 2 is a palindrome exactly when its end symbols are equal, and a longer one exactly when its end symbols are equal and its inner part is a palindrome. The search simulates the recursive procedure "output $\mathit{path}$ followed by each partition of $s[i..n-1]$". By strong induction on $n - i$, processing a frame $(i, 0)$ outputs, in order, $\mathit{path}$ followed by each partition of $s[i..n-1]$ exactly one time, and then removes the frame and restores $\mathit{path}$. The case $i = n$ is line L8. For $i < n$, each partition of $s[i..n-1]$ has exactly one first piece $s[i..j]$ with $j \in \mathit{ends}[i]$, and lines L10 and L11 try each such $j$ one time. The full proof is in the proof file of this page.

## Complexity

**Table.** Lines L1 to L4 take $\Theta(n^2)$ time and $\Theta(n^2)$ space; the lists have $N_{\mathrm{occ}}(s) \le n(n+1)/2$ entries in all.

**Search.** Each run of line L11 pushes a frame for a partial partition, a list of palindromic pieces that covers a prefix of $s$, and each partial partition is pushed one time. Each partial partition extends to at least one full partition, by single symbols, so each is a prefix of some output. An output with $t \le n$ pieces has $t$ nonempty prefixes as partial partitions, so there are at most $nP$ pushes in all. Each frame is popped one time, and its $k$ steps through $\mathit{ends}[i]$ are the pushes of its children. Line L8 copies a partition of total length $n$. So the search takes $\Theta(nP)$ time when the copy of an output costs $\Theta(n)$, and $\Theta(n^2 + nP)$ in all.

- **On $a^n$.** There are $P = 2^{n-1}$ partitions and $2^n$ pushes, counting the root, and the time is $\Theta(n 2^n)$.
- **On a string with no palindrome longer than 1.** $P = 1$ and the search is $\Theta(n)$; the table dominates with $\Theta(n^2)$.
- **Space.** $\Theta(n^2)$ for the table, $O(n)$ for the stack and the path. Without the table, the lists can be built from [Manacher's algorithm](/manacher/) in $O(n + N_{\mathrm{occ}})$ space.

The bound $\Omega(nP)$ holds for any algorithm that writes out each partition on $a^n$, since each partition there has total length $n$.

## Properties

- **Output-sensitive.** No branch of the search fails, because a single symbol is always a palindrome. This is the main difference from a generic [backtracking](/generic-backtracking-algorithm/) search, where branches can end without output.
- **Order.** The partitions come in increasing lexicographic order of their sequences of piece lengths.
- **Not recursive.** The explicit stack replaces the recursion of the textbook version, so long inputs do not overflow the call stack.
- **Lazy.** The output can be produced one partition at a time, and the search can stop after any number of outputs.

## Variants and improvements

- **Recursive form.** `SOLVE(i)`: if $i = n$, output $\mathit{path}$; else for each $j \in \mathit{ends}[i]$, push $s[i..j]$, call `SOLVE(j + 1)`, pop. This is the usual form in textbooks and contest code; the stack form above is the same search.
- **Test on the fly.** Without the table, test each candidate piece with the two-pointer scan when the search reaches its start. Each node of the search then costs up to $O(n^2)$ instead of the length of its list, and the same substring is tested again each time the search comes back to its start.
- **Counting only.** The number $P$ follows from the recurrence $P_i = \sum_{j \in \mathit{ends}[i]} P_{j+1}$, $P_n = 1$, in $O(n^2)$ time, without listing; see [palindrome partitioning](/palindrome-partitioning/).
- **Fewest pieces.** To find one partition with the fewest pieces, do not search; use the [dynamic program](/palindrome-partition-dp/).
- **Restricted pieces.** For pieces of length at least $\ell$, or only even pieces, filter the lists. Dead ends become possible, and memoizing which positions can reach the end restores the output-sensitive bound.

## When to use it

Use this algorithm when all partitions are needed, for example to show them or to check a property of each one. It is fast when $P$ is small. When only the number of partitions or the best partition is needed, use the dynamic programs, because $P$ can be $2^{n-1}$.

## Pitfalls

- **Forgetting even palindromes.** The table must cover the pieces of even length, such as `aa` and `baab` in the example. The test $j - i < 2$ in line L3 handles length 2.
- **Wrong fill order.** Row $i$ reads row $i + 1$, so the rows must be filled from $n - 1$ down to 0.
- **Sharing the path.** An output must be a copy of $\mathit{path}$, because the path changes after the output.
- **Recursion depth.** A recursive version has depth up to $n$; in Python, $n$ above about 1000 exceeds the default limit.
- **The empty string.** It has one partition, the empty one, not zero partitions.

## Implementations

## History

Enumeration of all palindromic partitions is a standard backtracking exercise in programming contests and interview collections, such as LeetCode problem 131. The technique is the classical depth-first backtracking that Knuth describes in Section 7.2.2 of Volume 4B of The Art of Computer Programming, applied with a table of palindromic substrings computed by the interval recurrence.

## References
