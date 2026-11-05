---
tag: Y1B69D
kind: problem
slug: palindrome-edit-distance
name: Palindrome edit distance
aliases:
- minimum insertions to make a palindrome
- distance to the nearest palindrome
area: strings/palindromes
level: core
summary: The fewest edit operations that turn a string into a palindrome.
model: comparison-model
complexity:
  vars: {n: the length of the string}
  time: {worst: O(n^2)}
  space: {aux: O(n)}
prereqs: [palindrome, longest-palindromic-subsequence, edit-distance, interval-dp]
see_also: [shortest-palindrome, longest-common-subsequence, lcs-dynamic-programming, palindrome-recognition, gapped-palindrome, minimum-palindrome-partition]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Chapter 14, Problem 14-2, Longest palindrome subsequence
  - paper: doi:10.1016/S0031-3203(01)00179-0
    title: Alexandre H. L. Porto and Valmir C. Barbosa, Finding approximate palindromes in strings, Pattern Recognition 35(11) (2002), 2581-2591
    locator: the definition of an approximate palindrome by the edit operations of approximate pattern matching, and the O(k^2 n) algorithm for maximal approximate palindromes with up to k errors
  - url: https://leetcode.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/
    title: LeetCode, Problem 1312, Minimum Insertion Steps to Make a String Palindrome
    locator: the problem statement (insert characters anywhere, minimize the number of insertions)
---

The palindrome edit distance of a string $s$ is the least number of edit operations that turn $s$ into a [palindrome](/palindrome/). The answer depends on the operations allowed. With insertions only, with deletions only, or with both, it is $n - \mathrm{LPS}(s)$, where $\mathrm{LPS}(s)$ is the length of the [longest palindromic subsequence](/longest-palindromic-subsequence/). With substitutions only it is the number of mirror pairs that differ. With all three operations of the [edit distance](/edit-distance/) it is given by an $O(n^2)$ [interval dynamic program](/interval-dp/), and it can be smaller than both of the other answers.

## In plain words

You have a word and a set of allowed changes: put in a letter, take out a letter, or change a letter. You want the fewest changes that make the word read the same from both ends. If you may only take letters out, keep the longest set of letters, in their order, that already reads the same from both ends, and take out the rest. If you may only put letters in, give each of those other letters a partner on the opposite side instead. Both cost the same. If you may only change letters, each pair of letters at equal distance from the two ends that do not match costs one change. With all three changes allowed, a mix can be cheaper, and a table over all pieces of the word finds the best mix.

## Definition

**Input.** A string $s = s[0..n-1]$ over an [alphabet](/alphabet/) $\Sigma$, with 0-based indices, and a set of allowed operations, each of cost 1:

- **insertion** of a symbol of $\Sigma$ at any position,
- **deletion** of one symbol,
- **substitution** of one symbol by another symbol of $\Sigma$.

**Output.** The least number $d(s)$ of operations that turn $s$ into a palindrome, odd or even, and, if asked, one such palindrome. Equivalently, $d(s) = \min_{w} \mathrm{dist}(s, w)$ over all palindromes $w$, where $\mathrm{dist}$ is the distance with the allowed operations. Algorithms test symbols for equality only; the inserted and substituted symbols can always be copies of symbols of $s$.

The notations on this page are $I(s)$ for insertions only, $D(s)$ for deletions only, $ID(s)$ for insertions and deletions, $S(s)$ for substitutions only, and $E(s)$ for all three.

## Variants

- **Insertions only, $I(s) = n - \mathrm{LPS}(s)$.** This is the "minimum insertions" problem of programming contests. The [shortest palindrome](/shortest-palindrome/) is the case where insertions are only allowed in front of $s$.
- **Deletions only, $D(s) = n - \mathrm{LPS}(s)$.** The decision version "can $s$ become a palindrome by at most $k$ deletions?" is the same number compared with $k$.
- **Substitutions only, $S(s) = |\{i < \lfloor n/2 \rfloor : s[i] \ne s[n-1-i]\}|$.** The length stays $n$, so the only choice is which symbol of each differing pair to change.
- **All edit operations, $E(s)$.** The interval recurrence below. Weighted costs change only the constants in the recurrence.
- **Approximate palindromes inside a string.** Find the substrings that are within distance $k$ of a palindrome. Porto and Barbosa (2002) define approximate palindromes by edit operations in this way and find the maximal ones with up to $k$ errors in $O(k^2 n)$ time for a fixed alphabet. With substitutions only, this is the $k$-mismatch palindrome problem, see [gapped palindrome](/gapped-palindrome/) for related variants.
- **Partition instead of edit.** Cutting $s$ into palindromes, rather than editing it into one, is [minimum palindrome partition](/minimum-palindrome-partition/).

## Examples

| $s$ | $n$ | $\mathrm{LPS}(s)$ | $I = D = ID$ | $S$ | $E$ |
| --- | --- | --- | --- | --- | --- |
| $\varepsilon$ | 0 | 0 | 0 | 0 | 0 |
| `a` | 1 | 1 | 0 | 0 | 0 |
| `ab` | 2 | 1 | 1 | 1 | 1 |
| `abc` | 3 | 1 | 2 | 1 | 1 |
| `abca` | 4 | 3 | 1 | 1 | 1 |
| `abcd` | 4 | 1 | 3 | 2 | 2 |
| `abab` | 4 | 3 | 1 | 2 | 1 |
| `banana` | 6 | 5 | 1 | 3 | 1 |
| `aababb` | 6 | 3 | 3 | 3 | 2 |

For `banana`, the subsequence `anana` is a palindrome, so one deletion (the `b`) or one insertion (a `b` at the end) is enough, but three mirror pairs differ: (b, a), (a, n), (n, a). For `abcd` substitutions are better: `abba` needs two. For `aababb` a mix is better than each single kind: delete the first `a` to get `ababb`, then change the last `b` to `a` to get `ababa`.

## Known algorithms

**The longest palindromic subsequence, $O(n^2)$.** For the three cases without substitution, compute $\mathrm{LPS}(s)$ with the interval recurrence $L(i, i) = 1$, $L(i, j) = L(i+1, j-1) + 2$ if $s[i] = s[j]$, and $L(i, j) = \max(L(i+1, j), L(i, j-1))$ otherwise, or as the [longest common subsequence](/longest-common-subsequence/) of $s$ and $s^R$ (CLRS, Problem 14-2). Then $I = D = ID = n - \mathrm{LPS}(s)$.

*Proof.* Deletions only: after $k$ deletions the rest is a palindromic subsequence of length $n - k$, so $D(s) = n - \mathrm{LPS}(s)$. Insertions only, upper bound: let $Q$ be a longest palindromic subsequence. Each symbol of $s$ outside $Q$ lies between two consecutive symbols of $Q$, or outside all of them, and inserting its copy at the mirror place keeps the symmetry, so $n - |Q|$ insertions suffice. Lower bound, with insertions and deletions: let $w$ be a palindrome obtained with $k$ operations, and look at the symbols of $s$ that survive into $w$. Those whose mirror symbol in $w$ is also a survivor form a set closed under the mirror map of $w$, so they spell a palindrome, and in $s$ they appear in the same order, so they form a palindromic subsequence of $s$. A survivor whose mirror is an inserted symbol uses up one insertion, and a symbol of $s$ that does not survive uses up one deletion. So at least $n - k$ symbols of $s$ are in that palindromic subsequence, and $k \ge n - \mathrm{LPS}(s)$. $\square$

**Substitutions only, $O(n)$.** Count the mirror pairs that differ, with the scan of [palindrome recognition](/palindrome-recognition/) that does not stop at a mismatch. Each differing pair needs at least one substitution, the pairs are disjoint, and one substitution per pair is enough.

**All three operations, $O(n^2)$ time.** Let $E(i, j)$ be the answer for $s[i..j]$, with $E(i, j) = 0$ for $j \le i$.

```pseudo id=edit
PALINDROME-EDIT-DISTANCE(s)              ▷ s[0 .. n − 1], E(i, j) = 0 for j ≤ i
L1  for ℓ ← 2 to n do                        ▷ the length j − i + 1
L2      for i ← 0 to n − ℓ do
L3          j ← i + ℓ − 1
L4          if s[i] = s[j] then E(i, j) ← E(i + 1, j − 1)
L5          else E(i, j) ← 1 + min(E(i + 1, j), E(i, j − 1), E(i + 1, j − 1))
L6  return E(0, n − 1)
```

The three terms of line L5 are: delete $s[i]$ (or, at the same cost, insert a copy of $s[i]$ after $s[j]$), delete $s[j]$ (or insert a copy of it before $s[i]$), and substitute one of $s[i]$ and $s[j]$ by the other. *Why it is correct (sketch).* Take an optimal edit script into a palindrome $w$. An insertion at an outer end of $w$ that is paired with a symbol of $s$ can be traded for the deletion of that symbol, so one can assume that the outer symbols of $w$ come from $s$ or from insertions paired with $s[i]$ or $s[j]$. Then one of four things happens to the outer pair $s[i]$, $s[j]$: one of them is deleted or paired with an insertion, which gives the first two terms, or they become the two outer symbols of $w$, which costs 0 if they are equal and 1 if not. If $s[i] = s[j]$, keeping both is never worse, because any script for $s[i+1..j]$ or $s[i..j-1]$ yields one for $s[i+1..j-1]$ of no larger cost. The table fills by increasing length, in $O(n^2)$ time; keeping only the last two lengths gives $O(n)$ space.

## Bounds

- **Upper bounds.** $I, D, ID \le n - 1$ for $n \ge 1$, reached by strings of distinct symbols, and $S \le \lfloor n/2 \rfloor$. Also $E \le \min(ID, S)$, and $E$ can be smaller than both, as for `aababb`.
- **Time.** $O(n^2)$ time and $O(n)$ space for each version with a deletion or an insertion, and $\Theta(n)$ for substitutions only. Each version needs $\lfloor n/2 \rfloor$ equality tests on $a^n$, because its answer is 0 if and only if $s$ is a palindrome. The quadratic time is the one of the interval recurrence and of the [LCS dynamic program](/lcs-dynamic-programming/).

## Reductions

- **To the longest palindromic subsequence.** $I = D = ID = n - \mathrm{LPS}(s)$, as proved above.
- **To the longest common subsequence.** $\mathrm{LPS}(s) = \mathrm{LCS}(s, s^R)$: a palindromic subsequence of $s$ is a common subsequence of $s$ and $s^R$, and conversely a longest common subsequence can be chosen to be a palindrome.
- **From palindrome recognition.** Each version is 0 exactly on palindromes.
- **To edit distance.** $E(s) = \min_w \mathrm{dist}(s, w)$ over palindromes $w$, a constrained form of the [edit distance](/edit-distance/) problem.

## Applications

- **Approximate palindromes in biology.** DNA hairpins tolerate a few mismatches and gaps, which is the reason for approximate palindromes with edit operations, as in Porto and Barbosa.
- **Programming tasks.** "Minimum insertions to make a palindrome" and "palindrome after at most $k$ deletions" are standard exercises for interval dynamic programming.

## References
