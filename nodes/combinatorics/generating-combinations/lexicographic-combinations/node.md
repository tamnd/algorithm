---
tag: JMPMV6
kind: algorithm
slug: lexicographic-combinations
name: Lexicographic generation of combinations (Knuth Algorithm L)
aliases:
- Algorithm L
- next combination in lexicographic order
- lexicographic successor of a combination
area: combinatorics/generating-combinations
level: intro
summary: Repeatedly advance an index array to the lexicographically next k-subset.
solves: [k-subset-enumeration]
model: word-ram
complexity:
  vars: {n: the size of the ground set, k: the size of each subset, N: the number of k-subsets}
  time: {worst: Θ(N*n/(n-k+1)), amortized: Θ(n/(n-k+1))}
  space: {extra: Θ(1)}
properties: {in_place: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 1963
  people: [C. J. Mifsud]
  note: An early published version is Algorithm 154 of the Communications of the ACM, 1963.
prereqs: [k-subset-enumeration, lexicographic-order]
see_also: [k-subset-enumeration, colexicographic-order, recursive-combination-generation, next-permutation, combinatorial-ranking-and-unranking, hockey-stick-identity, lexicographic-successor, cool-lex-order]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.3, Generating all combinations (Algorithm L, Lexicographic combinations, its running time analysis, and Algorithm T)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 2, Section 2.3, k-element subsets (lexicographic ordering, the successor algorithm)
  - book: isbn:9780125192606
    title: Albert Nijenhuis and Herbert S. Wilf, Combinatorial Algorithms for Computers and Calculators, second edition, Academic Press, 1978
    locator: Chapter 3, Next k-subset of an n-set
  - paper: doi:10.1145/366274.366309
    title: C. J. Mifsud, Algorithm 154, Combination in lexicographical order, Communications of the ACM 6(3), 1963, 103
---

This algorithm lists the $k$-subsets of $[n] = \{1, \ldots, n\}$ in lexicographic order. It keeps the current subset as an increasing array $a_1 < a_2 < \cdots < a_k$. To get the next subset, it finds the rightmost entry that can still grow, adds $1$ to it, and resets the entries to its right to the smallest values that follow it. It solves [k-subset enumeration](/k-subset-enumeration/) with $\Theta(n/(n-k+1))$ amortized time for each subset, which is less than $1$ step of the scan on average when $k \le n/2$.

## In plain words

Write each team of $k$ players as a sorted list of player numbers. Sort all these lists as a dictionary sorts words. The first list is $1, 2, \ldots, k$ and the last is $n - k + 1, \ldots, n$.

To find the next list, look at the last number. If it can grow by one, make it grow, and you are done. If it is already as large as it can be, look one place to the left, and so on. When you find a number that can grow, add one to it, and then fill the places to its right with the next numbers in a row. For $n = 5$ and $k = 3$, the list after $1, 4, 5$ is $2, 3, 4$.

## The problem

Given $0 \le k \le n$, visit each $k$-subset of $[n]$ once, in lexicographic order of the sorted lists. The current subset is an array $a[1 \ldots k]$ with $a[1] < \cdots < a[k]$ that the algorithm changes in place. If $k > n$ there is nothing to visit. This is [k-subset enumeration](/k-subset-enumeration/) with a fixed order.

In an increasing list over $[n]$, the entry $a[i]$ is at most $n - k + i$, because $k - i$ larger entries must follow it. The entry is *at its maximum* when $a[i] = n - k + i$.

## The algorithm

```pseudo id=main
LEX-COMBINATIONS(n, k)                     ▷ visit a[1] < … < a[k] over [n]
L1  if k > n then return
L2  a[j] ← j for 1 ≤ j ≤ k
L3  loop
L4      visit a[1 .. k]
L5      i ← k
L6      while i ≥ 1 and a[i] = n − k + i do i ← i − 1
L7      if i = 0 then return               ▷ a = (n − k + 1, …, n), the last subset
L8      a[i] ← a[i] + 1
L9      for j ← i + 1 to k do a[j] ← a[j − 1] + 1
```

Line L6 finds the rightmost entry that is not at its maximum. Line L8 adds one to it, and line L9 makes the tail as small as it can be. For $k = 0$ the algorithm visits the empty set once: line L6 does not run and line L7 returns.

## Example

Take $n = 5$ and $k = 3$. The maxima are $a[1] \le 3$, $a[2] \le 4$ and $a[3] \le 5$.

| visit | $a$ | $i$ after L6 | steps of L6 | next $a$ |
| --- | --- | --- | --- | --- |
| 0 | $1, 2, 3$ | 3 | 0 | $1, 2, 4$ |
| 1 | $1, 2, 4$ | 3 | 0 | $1, 2, 5$ |
| 2 | $1, 2, 5$ | 2 | 1 | $1, 3, 4$ |
| 3 | $1, 3, 4$ | 3 | 0 | $1, 3, 5$ |
| 4 | $1, 3, 5$ | 2 | 1 | $1, 4, 5$ |
| 5 | $1, 4, 5$ | 1 | 2 | $2, 3, 4$ |
| 6 | $2, 3, 4$ | 3 | 0 | $2, 3, 5$ |
| 7 | $2, 3, 5$ | 2 | 1 | $2, 4, 5$ |
| 8 | $2, 4, 5$ | 1 | 2 | $3, 4, 5$ |
| 9 | $3, 4, 5$ | 0 | 3 | stop |

The scan of line L6 takes $10$ steps in total, which is $C(5, 2)$. Line L9 writes $7$ entries in total, which is $C(5, 2) - 3$.

## Correctness

Let $i$ be the largest index with $a[i] < n - k + i$. Each entry to the right of $a[i]$ is at its maximum, so no list that agrees with $a$ before position $i$ and differs later can be larger. The next list therefore changes position $i$, and the smallest choice there is $a[i] + 1$, followed by the smallest increasing tail. This is what lines L8 and L9 write. If no such $i$ exists, $a$ is the largest list and line L7 stops. The start of line L2 is the smallest list. So the algorithm visits all $k$-subsets in increasing lexicographic order, each once. The full proof is in the proof file.

## Complexity

**The scan.** Line L6 steps over the trailing entries that are at their maximum. The lists whose last $d$ entries are at their maximum are the lists that end with $n - d + 1, \ldots, n$, and there are $C(n - d, k - d)$ of them. So the total number of steps of line L6, over all $N = C(n, k)$ visits, is

$$\sum_{d=1}^{k} C(n - d, k - d) = C(n, k - 1),$$

by the [hockey stick identity](/hockey-stick-identity/). Line L9 writes as many entries as line L6 took steps, except in the last call, so it writes $C(n, k - 1) - k$ entries in total.

**The total time.** The time is $\Theta(N + C(n, k-1))$. Since $C(n, k-1) = N \cdot k/(n - k + 1)$, this is $\Theta(N \cdot n/(n - k + 1))$ for $n \ge 1$, or $\Theta(n/(n-k+1))$ amortized for each subset.

- For $k \le n/2$ the ratio $k/(n-k+1)$ is less than $1$, so the algorithm is CAT, see [constant amortized time generation](/constant-amortized-time-generation/).
- For $k$ close to $n$ it is not. With $k = n - 1$ there are $n$ subsets and $C(n, n-2) = n(n-1)/2$ scan steps, about $n/2$ steps for each subset.
- The delay is $\Theta(k)$ in the worst case, at the step from $1, n-k+2, \ldots, n$ to $2, 3, \ldots, k+1$.

**Space.** The array and two indices. No extra space beyond $O(1)$.

These counts match Knuth's analysis of his Algorithm L in Section 7.2.1.3, where the reset step runs about $t/(s+1)$ times for each visit, with $t = k$ and $s = n - k$.

## Properties

- **In place, no recursion.** The algorithm changes one array of $k$ entries.
- **Successor only.** Each step needs only the current list, so the generation can start from any $k$-subset and can stop at any time.
- **Lexicographic order.** The rank of a list in this order has a closed form, see [ranking and unranking combinations](/combinatorial-ranking-and-unranking/).
- **Not a Gray code.** One step can change all $k$ entries, for example from $1, 4, 5$ to $2, 3, 4$.

## Variants and improvements

- **Knuth's Algorithm L.** Knuth keeps the subset as $c_k > \cdots > c_1$ over $\{0, \ldots, n-1\}$ with sentinels $c_{k+1} = n$ and $c_{k+2} = 0$. The scan starts at $c_1$: while $c_j + 1 = c_{j+1}$ it sets $c_j \leftarrow j - 1$ and moves on. Then it adds $1$ to $c_j$. This lists the strings $c_k \cdots c_1$ in lexicographic order, which is [colexicographic order](/colexicographic-order/) of the sets: $210, 310, 320, 321, 410, \ldots$. Replace each element $x$ by $n + 1 - x$ and read the list backward to go from one order to the other.
- **Knuth's Algorithm T.** A tuned form of Algorithm L that predicts the next index $j$ from the last step. It does not set $c_j \leftarrow j - 1$ when $c_j$ already has that value, so it is fast also for $k$ close to $n$.
- **Complements.** For $k > n/2$, list the $(n - k)$-subsets in a bit vector and read the zeros as the $k$-subset. The order changes, but each step changes $O(1)$ bits on average.
- **Bit strings.** On machine words, [Gosper's hack](/gospers-hack/) gives the colexicographic successor in $O(1)$ word operations.
- **Recursion.** The [recursive generator](/recursive-combination-generation/) visits the same list in the same order.
- **Permutations.** The same idea, "find the rightmost place that can grow", gives [next permutation](/next-permutation/).

## When to use it

Use it when you need the $k$-subsets in sorted order, when you need a simple successor function, or when the loop must stop and continue later from a saved subset. It is the standard choice for $k \le n/2$. If you need one change for each step, use a [revolving door](/ehrlich-loopless-combinations/) or [cool-lex](/cool-lex-order/) order.

## Pitfalls

- **The bound of each entry.** The maximum of $a[i]$ is $n - k + i$, not $n$. A test against $n$ in line L6 makes lists with repeated or out-of-range entries.
- **The index out of range.** Test $i \ge 1$ before $a[i]$ in line L6, or keep a sentinel $a[0]$ smaller than each test value.
- **$k > n$ and $k = 0$.** For $k > n$ there is no subset, so do not visit $1, \ldots, k$. For $k = 0$ there is one subset, the empty set.
- **Shared state.** The visit sees the array that the next step changes. Copy it if you store it.
- **Large $k$.** For $k$ close to $n$ the scan is long. Use complements or Algorithm T.

## Implementations

## History

The lexicographic successor of a combination is a standard routine. An early published version is Algorithm 154 of the Communications of the ACM, by C. J. Mifsud (1963). Nijenhuis and Wilf give a version in their chapter on the next $k$-subset. Knuth, in Section 7.2.1.3, gives Algorithm L in the colexicographic form, analyzes its running time, and improves it to Algorithm T.

## References
