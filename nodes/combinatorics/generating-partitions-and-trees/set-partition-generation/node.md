---
tag: 8CRTRG
kind: algorithm
slug: set-partition-generation
name: Set partition generation (Algorithm H)
aliases:
- Knuth's Algorithm H
- Restricted growth string enumeration
- Next set partition in lexicographic order
area: combinatorics/generating-partitions-and-trees
level: core
summary: Lists all B_n partitions of {1, ..., n} as restricted growth strings in lexicographic order, in constant amortized time for each partition.
solves: [set-partitions]
model: word-ram
complexity:
  vars: {n: the size of the set, N: "the number of set partitions, the Bell number B_n"}
  time: {worst: Θ(N), amortized: Θ(1)}
  space: {extra: Θ(n)}
properties: {in_place: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 2011
  people: [Donald E. Knuth]
  note: Knuth gives Algorithm H, restricted growth strings in lexicographic order, in Section 7.2.1.5 of TAOCP Volume 4A (2011). Successor routines for set partitions are older, such as NEXEQU of Nijenhuis and Wilf (1978).
prereqs: [set-partitions, restricted-growth-string, constant-amortized-time-generation]
see_also: [stirling-numbers, bell-numbers, partition-lattice, integer-partition-generation, composition-generation, lexicographic-successor, ranking-unranking, counting-set-partitions]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.5, Generating all set partitions (Algorithm H, Restricted growth strings in lexicographic order, its analysis, and Gray codes)
  - book: isbn:9780125192606
    title: Albert Nijenhuis and Herbert S. Wilf, Combinatorial Algorithms for Computers and Calculators, second edition, Academic Press, 1978
    locator: Chapter 11, Next equivalence relation on n letters (NEXEQU), and Chapter 12, Random equivalence relation on n letters (RANEQU)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 3, Section 3.2, Set partitions, Bell and Stirling numbers (successor, ranking and unranking of restricted growth functions)
  - paper: doi:10.1016/0001-8708(77)90043-3
    title: Stephen C. Milne, Restricted growth functions and incidence relations of the lattice of partitions of an n-set, Advances in Mathematics 26 (1977), 290-305
    locator: the whole paper
---

This algorithm lists the [partitions of the set](/set-partitions/) $[n] = \{1, \ldots, n\}$ by listing their [restricted growth strings](/restricted-growth-string/) in lexicographic order, from $00 \ldots 0$ (one block) up to $01 \ldots (n-1)$ ($n$ singleton blocks). Each step finds the last entry that can grow, adds $1$ to it, and sets all entries after it to $0$. The scans of all steps add up to $\sum_{i=1}^{n-1} B_i$, which is less than $B_n$, so the whole list takes $\Theta(B_n)$ time, [constant amortized time](/constant-amortized-time-generation/) for each partition. It is Knuth's Algorithm H.

## In plain words

Number the teams in a split by the order in which they first appear, and write each person's team number in a row. The first person is always in team zero, and each person is in a team that already exists or in the next new team. These rows of numbers stand for the splits one to one.

List the rows as a dictionary would. To get the next row, look from the right for the last person who could move to a higher team number: a person can go up to the next new team, but not beyond it. Move that person up by one, and put everyone after them back in team zero. Most steps change only the last person, so the work for each split is small on average.

## The problem

The input is an integer $n \ge 0$. The output is the list of all partitions of $[n]$, each one time. A partition is written as its restricted growth string $a_1 \ldots a_n$: $a_i$ is the block number of $i$, with blocks numbered $0, 1, \ldots$ by their smallest elements. So $a_1 = 0$ and $a_i \le 1 + \max(a_1, \ldots, a_{i-1})$. The order is increasing lexicographic order of the strings. The number of partitions is the Bell number $N = B_n$.

The algorithm keeps the string in an array $a[1 \ldots n]$, and for $j \ge 2$ it keeps $b[j] = 1 + \max(a[1], \ldots, a[j - 1])$, the largest value allowed at position $j$. The visit of line L4 sees the array in place.

## The algorithm

```pseudo id=main
SET-PARTITIONS(n)                           ▷ visit a[1 .. n] in lexicographic order
L1  if n = 0 then visit the empty partition and return
L2  a[1 .. n] ← 0, …, 0, b[2 .. n] ← 1, …, 1  ▷ b[j] = 1 + max(a[1 .. j − 1])
L3  loop
L4      visit a[1 .. n]
L5      j ← n
L6      while j ≥ 2 and a[j] = b[j] do j ← j − 1  ▷ skip entries at their largest value
L7      if j = 1 then return                ▷ a = 0 1 2 … n − 1, the last string
L8      a[j] ← a[j] + 1, c ← max(b[j], a[j] + 1)
L9      for i ← j + 1 to n do a[i] ← 0, b[i] ← c
```

Line L6 finds the last position $j$ whose entry can still grow. Line L8 increases it, and $c$ is the new value of $1 + \max(a[1], \ldots, a[j])$. Line L9 puts the smallest entries, zeros, after position $j$, and since these do not change the maximum, all of them get the bound $c$. The steps follow the plan of Knuth's Algorithm H, which also has a short path for the case $j = n$.

## Example

Take $n = 4$. There are $B_4 = 15$ partitions.

| visit | $a$ | partition | $j$ | runs of L6 | next $a$ |
| --- | --- | --- | --- | --- | --- |
| 0 | $0000$ | $\{1,2,3,4\}$ | $4$ | $0$ | $0001$ |
| 1 | $0001$ | $\{1,2,3\}\{4\}$ | $3$ | $1$ | $0010$ |
| 2 | $0010$ | $\{1,2,4\}\{3\}$ | $4$ | $0$ | $0011$ |
| 3 | $0011$ | $\{1,2\}\{3,4\}$ | $4$ | $0$ | $0012$ |
| 4 | $0012$ | $\{1,2\}\{3\}\{4\}$ | $2$ | $2$ | $0100$ |
| 5 | $0100$ | $\{1,3,4\}\{2\}$ | $4$ | $0$ | $0101$ |
| 6 | $0101$ | $\{1,3\}\{2,4\}$ | $4$ | $0$ | $0102$ |
| 7 | $0102$ | $\{1,3\}\{2\}\{4\}$ | $3$ | $1$ | $0110$ |
| 8 | $0110$ | $\{1,4\}\{2,3\}$ | $4$ | $0$ | $0111$ |
| 9 | $0111$ | $\{1\}\{2,3,4\}$ | $4$ | $0$ | $0112$ |
| 10 | $0112$ | $\{1\}\{2,3\}\{4\}$ | $3$ | $1$ | $0120$ |
| 11 | $0120$ | $\{1,4\}\{2\}\{3\}$ | $4$ | $0$ | $0121$ |
| 12 | $0121$ | $\{1\}\{2,4\}\{3\}$ | $4$ | $0$ | $0122$ |
| 13 | $0122$ | $\{1\}\{2\}\{3,4\}$ | $4$ | $0$ | $0123$ |
| 14 | $0123$ | $\{1\}\{2\}\{3\}\{4\}$ | $1$ | $3$ | stop |

At visit 4, $a = 0012$ has $a_4 = 2 = b_4$ and $a_3 = 1 = b_3$, so the scan stops at $j = 2$. Line L8 makes $a_2 = 1$ and $c = 2$, and line L9 writes $a_3 = a_4 = 0$ with $b_3 = b_4 = 2$. The scans run $8 = B_1 + B_2 + B_3$ times in all.

## Correctness

Let $a$ be an RGS other than the last one. A larger RGS must first differ from $a$ at a position $i$ where $a_i$ is below its bound, because the bound at $i$ depends only on the prefix. The smallest larger RGS uses the last such position $j$, the value $a_j + 1$ there, and then zeros, the smallest entries that are always allowed. Lines L6 to L9 write exactly this string, and they keep $b$ correct, because zeros after position $j$ do not change the running maximum. The first string $0^n$ is the smallest RGS and the last one, $01 \ldots (n-1)$, is the largest and is the only one with every entry at its bound. So the algorithm visits each RGS once, in increasing order. The full proof is in the proof file.

## Complexity

**Each step.** One step costs $O(1)$ plus $O(1)$ for each run of line L6 and for each pass of line L9. Line L9 runs $n - j$ times, which equals the number of runs of line L6 in the same step.

**Total of the scans.** The scan at $a$ runs $s$ or more times exactly when the last $s$ entries of $a$ are each at their bound. Such a string is any RGS of length $n - s$ followed by forced entries, so there are $B_{n-s}$ of them, for $1 \le s \le n - 1$. Hence the total is

$$\sum_{s=1}^{n-1} B_{n-s} = \sum_{i=1}^{n-1} B_i.$$

**Bell numbers double.** For $i \ge 1$, each partition of $[i]$ gives two partitions of $[i + 1]$, one with the block $\{i + 1\}$ and one with $i + 1$ added to the block of $1$. So $B_{i+1} \ge 2 B_i$, and $\sum_{i=1}^{n-1} B_i < 2 B_{n-1} \le B_n$ for $n \ge 2$.

**Total.** The time is $\Theta(B_n)$ for the whole list, so $\Theta(1)$ amortized for each partition. The extra space is the two arrays of $n + 1$ entries.

- **Delay.** The algorithm is CAT but not [loopless](/loopless-generation/). The step from $0\, 0\, 1\, 2 \cdots (n-2)$ to $0\, 1\, 0 \cdots 0$ runs line L6 $n - 2$ times and line L9 $n - 2$ times, so the worst delay is $\Theta(n)$.
- **Lower bound.** Each method must output $B_n$ partitions, so $\Omega(B_n)$ time is necessary, and the algorithm is optimal up to a constant factor.
- **Copies.** If each string is copied, as the Python code does, the total time is $\Theta(n B_n)$.

## Properties

- **In place, no recursion.** The state is the arrays $a$ and $b$.
- **Successor only.** Each step needs only the current string, since $b$ can be computed from $a$ in $O(n)$. So the generation can start at any partition.
- **Block structure.** The strings with a fixed prefix $a_1 \ldots a_i$ form one block of consecutive entries, of size $T(n - i, b)$, the number of completions with $b$ blocks so far. The rank formula on the page of [restricted growth strings](/restricted-growth-string/) follows from this.
- **Number of blocks.** The number of blocks of the current partition is $1 + \max_i a_i = \max(b[n], a[n] + 1)$, available in $O(1)$.
- **Not a Gray code.** One step can move many elements, as in the step from $0012$ to $0100$, which moves elements $2$ and $3$ and $4$.

## Variants and improvements

- **Short path for the last entry.** If $a[n] < b[n]$, the step is $a[n] \leftarrow a[n] + 1$ with no scan. Knuth's Algorithm H tests this case first, and it covers most steps: the strings with $a_n < b_n$ are all but $B_{n-1}$ of them.
- **Exactly $k$ blocks.** Restrict the values to at most $k - 1$ and require that all values up to $k - 1$ appear; a prefix that cannot reach $k$ blocks in the positions left is skipped. This lists the $S(n, k)$ partitions with $k$ blocks, counted by the [Stirling numbers](/stirling-numbers/).
- **Gray codes.** Knuth (Section 7.2.1.5) describes orders of the restricted growth strings in which one entry changes at each step, so one element moves to another block.
- **Insertion order.** Recursion on $n$: from each partition of $[n - 1]$, put $n$ into each block in turn and then into a new block. This is also CAT.
- **Ranking, unranking and sampling.** With the table of completions $T(r, b)$, a uniform random integer below $B_n$ unranks to a uniform random partition in $O(n)$ big integer steps. Nijenhuis and Wilf's RANEQU samples a random partition by a different method.

## When to use it

Use it when you need all partitions of a small set, in a fixed order, with a compact state. The string form is also the right form for search: in graph coloring or clustering by brute force, a search over restricted growth strings visits each grouping of $n$ items once instead of once for each naming of the groups. Since $B_{15} = 1382958545$, a full list is feasible only for $n$ up to about $15$. To count partitions, use the Bell or [Stirling numbers](/stirling-numbers/) instead of a list.

## Pitfalls

- **The bound $c$.** After line L8, the bound for the later positions is $1 + \max(a[1], \ldots, a[j])$ with the new $a[j]$. Writing $b[j]$ or $a[j] + 1$ alone is wrong in one of the two cases: $a[j] + 1$ is too small when $a[j]$ is below the running maximum, and $b[j]$ is too small when $a[j]$ has just reached it.
- **The guard $j \ge 2$.** Position $1$ is fixed at $0$. Without the guard the scan reads $b[1]$, which is not defined.
- **$n = 0$.** There is one partition of the empty set, with no blocks, and the algorithm visits it once.
- **Block numbers.** The strings number blocks by their smallest elements. A labeling with other block numbers, such as $1000$, is not an RGS and is not visited.
- **Shared state.** The visit sees the array that the next step changes. Copy it if you store it.

## Implementations

The Python code yields a tuple copy of each string, and `to_blocks` turns a string into its list of blocks. The function `scan_steps` runs the same steps without visits and returns the number of runs of line L6.

## History

Restricted growth strings as a code for set partitions are old. Milne (1977) used the name restricted growth functions in a study of the partition lattice. Nijenhuis and Wilf gave the successor routine NEXEQU and the sampler RANEQU in 1978. Knuth, in Section 7.2.1.5, gives Algorithm H for restricted growth strings in lexicographic order with its analysis, a variant for a fixed number of blocks, and Gray codes.

## References
