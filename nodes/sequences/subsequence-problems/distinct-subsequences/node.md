---
tag: DVAPVH
kind: problem
slug: distinct-subsequences
name: Counting distinct subsequences
aliases:
- number of distinct subsequences
area: sequences/subsequence-problems
level: core
summary: Count the distinct subsequences of a string, not counting repeated index choices that yield equal strings.
prereqs: [subsequence, count-subsequence-occurrences, subsequence-checking]
see_also: [subsequence-automaton, count-distinct-substrings, fibonacci-numbers, tabulation, longest-common-subsequence]
sources:
  - paper: "Cees Elzinga, Sven Rahmann and Hui Wang, Algorithms for subsequence combinatorics, Theoretical Computer Science 409(3), 2008, 394-404"
    locator: the linear-time count of the distinct subsequences of one string and the count of the distinct common subsequences of two strings
  - paper: "Abraham Flaxman, Aram W. Harrow and Gregory B. Sorkin, Strings with maximally many distinct subsequences and substrings, Electronic Journal of Combinatorics 11(1), 2004, R8"
    locator: the strings of a given length and alphabet with the most distinct subsequences
  - book: "M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997"
    locator: Chapter 6, Subwords (the set of subwords of a word and the leftmost and rightmost occurrences)
---

This problem asks for the number of different strings that are [subsequences](/subsequence/) of a string $T$ of length $n$, the empty string included. A string of $n$ distinct letters has $2^n$ of them, but repeated letters make many index sets give the same string: ABCBDAB has $2^7 = 128$ index sets but only 102 distinct subsequences. A one-pass recurrence, $D_i = 2D_{i-1} - D_{p-1}$ where $p$ is the previous position of the same letter, counts them in $O(n)$ arithmetic operations. It is the distinct-string counterpart of [counting the occurrences](/count-subsequence-occurrences/) of one pattern.

## In plain words

Take the word "aba". You can pick letters in eight ways (each letter in or out), but "a" comes out twice, from the first a and from the last a. So there are only seven different results: the empty word, a, b, ab, ba, aa and aba.

Read the word from left to right and keep the number of different results so far. A new letter doubles the number, because each old result can stay as it is or get the new letter at its end. But some of the results with the new letter at the end were already there, made with the earlier copy of the same letter. Subtract those, and the count is right.

## Definition

**Input.** A string $T = t_1 \cdots t_n$ over an alphabet $\Sigma$ of size $\sigma$.

**Output.** $D(T) = |\mathrm{Sub}(T)|$, where $\mathrm{Sub}(T) = \{Z : Z \preceq T\}$ is the set of distinct subsequences, the empty string $\varepsilon$ included. (Subtract 1 to exclude it.)

**The recurrence.** Let $D_i = D(t_1 \cdots t_i)$, and for $i \ge 1$ let $p(i)$ be the largest $p < i$ with $t_p = t_i$, if there is one. Then $D_0 = 1$ and

$$D_i = \begin{cases} 2 D_{i-1} & \text{if } t_i \text{ did not occur before}, \\ 2 D_{i-1} - D_{p(i) - 1} & \text{otherwise}. \end{cases}$$

*Proof.* Write $T_i = t_1 \cdots t_i$ and $c = t_i$. A subsequence of $T_i$ either has an embedding that does not use position $i$, so it is in $\mathrm{Sub}(T_{i-1})$, or it is $Zc$ with $Z \in \mathrm{Sub}(T_{i-1})$. So

$$\mathrm{Sub}(T_i) = \mathrm{Sub}(T_{i-1}) \cup \{Zc : Z \in \mathrm{Sub}(T_{i-1})\}.$$

The second set has $D_{i-1}$ elements, because $Z \mapsto Zc$ is one-to-one. We count the strings in both sets: the strings $Zc$ that are also subsequences of $T_{i-1}$.

*Claim.* $Zc \preceq T_{i-1}$ if and only if $c$ occurs in $T_{i-1}$ and $Z \preceq T_{p(i)-1}$.

If $Z \preceq T_{p(i)-1}$, append the index $p(i)$, which holds $c$, to an embedding of $Z$; this embeds $Zc$ in $T_{i-1}$. Conversely, let $Zc \preceq T_{i-1}$ with an embedding whose last index $q$ holds $c$. Then $q \le i - 1$ and $t_q = c$, so $q \le p(i)$ by the choice of $p(i)$ as the last such index. The other indices are below $q$, so $Z \preceq T_{q-1}$, and $T_{q-1}$ is a prefix of $T_{p(i)-1}$, so $Z \preceq T_{p(i)-1}$.

So the overlap has $D_{p(i)-1}$ elements if $c$ occurred before, and none otherwise. Inclusion and exclusion give $D_i = D_{i-1} + D_{i-1} - D_{p(i)-1}$, or $2D_{i-1}$. $\square$

```pseudo id=distinct
COUNT-DISTINCT-SUBSEQUENCES(T[1 .. n])
L1  D[0] ← 1; last[c] ← 0 for each letter c
L2  for i ← 1 to n do
L3      D[i] ← 2 · D[i − 1]
L4      if last[T[i]] > 0 then D[i] ← D[i] − D[last[T[i]] − 1]
L5      last[T[i]] ← i
L6  return D[n]
```

**Form by last letters.** An equal method keeps, for each letter $c$, the number $E[c]$ of distinct non-empty subsequences that end with $c$. On reading $c$, set $E[c] \gets 1 + \sum_{d \in \Sigma} E[d]$: the new strings that end with $c$ are $c$ itself and each old non-empty string followed by $c$, and they include all old strings that end with $c$. With a running total of the $E$ values, each step is $O(1)$. At the end, $D(T) = 1 + \sum_d E[d]$.

## Variants

- **Modulo a prime.** The count can be as large as $2^n$, so tasks ask for it modulo a number. Line L4 then subtracts modulo the number.
- **Fixed length.** Count the distinct subsequences of length $k$: keep $D_i^{(k)}$ for each $k$, with the same recurrence on each length, in $O(nk)$ operations.
- **Distinct common subsequences.** Count the distinct strings that are subsequences of both $X$ and $Y$. Elzinga, Rahmann and Wang give a table over pairs of prefixes, in $O(nm)$ operations.
- **Distinct palindromic subsequences.** Count the distinct palindromes among the subsequences, with an [interval DP](/interval-dp/).
- **The $k$-th subsequence.** List the distinct subsequences in lexicographic order and find the $k$-th one, with counts from a [subsequence automaton](/subsequence-automaton/), whose paths from the start state are exactly the distinct subsequences.
- **Substrings instead.** The number of distinct substrings is a different problem, solved with suffix structures: [count distinct substrings](/count-distinct-substrings/).

## Examples

The row $D_0, \ldots, D_n$ for some strings:

| $T$ | $D_0, D_1, \ldots, D_n$ | $D(T)$ |
| --- | --- | --- |
| abc | 1, 2, 4, 8 | 8 |
| aaa | 1, 2, 3, 4 | 4 |
| aba | 1, 2, 4, 7 | 7 |
| banana | 1, 2, 4, 8, 14, 24, 40 | 40 |
| ABCBDAB | 1, 2, 4, 8, 14, 28, 55, 102 | 102 |

For ABCBDAB at $i = 4$: the letter B occurred last at $p = 2$, so $D_4 = 2 \cdot 8 - D_1 = 16 - 2 = 14$. At $i = 7$: B occurred last at $p = 4$, so $D_7 = 2 \cdot 55 - D_3 = 110 - 8 = 102$.

**The most subsequences.** For binary strings of length $n$, an exhaustive search for $n \le 12$ gives the maximum of $D$ as $F_{n+3} - 1$, where $F_k$ are the [Fibonacci numbers](/fibonacci-numbers/), reached by the alternating string abab...:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\max D$ | 2 | 4 | 7 | 12 | 20 | 33 | 54 | 88 | 143 | 232 |

For the alternating string the value is exactly $F_{n+3} - 1$ for each $n$: for $i \ge 3$, $p(i) = i - 2$, so $D_i = 2D_{i-1} - D_{i-3}$, and $F_{i+3} - 1$ satisfies the same equation, since $2(F_{i+2} - 1) - (F_i - 1) = F_{i+2} + F_{i+1} - 1 = F_{i+3} - 1$; the first values $D_0, D_1, D_2 = 1, 2, 4$ agree with $F_3 - 1, F_4 - 1, F_5 - 1$. Flaxman, Harrow and Sorkin describe the maximizing strings for all alphabet sizes.

## Known algorithms

- **The recurrence.** COUNT-DISTINCT-SUBSEQUENCES uses $O(n)$ additions and subtractions and $O(n + \sigma)$ space; the form by last letters uses $O(\sigma)$ space. With exact integers of up to $n + 1$ bits, the bit cost is $O(n^2 / w)$ word operations on a $w$-bit machine.
- **Subsequence automaton.** The number of paths from the start state of the [subsequence automaton](/subsequence-automaton/) of $T$ is $D(T)$; it can be counted backward over the states in $O(n \sigma)$ time.
- **Brute force.** Listing the $2^n$ index sets and keeping a set of strings takes exponential time and space. It is useful only to test the fast method.

## Bounds

- **Range.** $n + 1 \le D(T) \le 2^n$ for $n \ge 0$. The lower bound is reached by $a^n$ (the subsequences are $a^0, \ldots, a^n$); the upper bound by strings with $n$ distinct letters, and only by them.
- **Work.** $\Theta(n)$ arithmetic operations, which is optimal, since each letter of $T$ must be read.

## Reductions

- **To occurrence counting.** $\binom{n}{k}$ index sets of size $k$ are split among the distinct subsequences of length $k$, so $\sum_{Z} \binom{T}{Z} = 2^n$, summed over the distinct subsequences $Z$, where $\binom{T}{Z}$ is the [number of occurrences](/count-subsequence-occurrences/).
- **Path counting.** $D(T)$ is the number of paths from the start in the DAG of the subsequence automaton, a standard [tabulation](/tabulation/) on a DAG.

## Applications

- **Sequence analysis.** In the social sciences, sequences of states (jobs, family events) are compared by the number of distinct subsequences they share, which Elzinga and coauthors use as a similarity measure.
- **Contest problems.** The recurrence is the standard solution of "distinct subsequences" tasks, usually modulo $10^9 + 7$.

## References
