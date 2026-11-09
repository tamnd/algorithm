---
tag: 45NXTX
kind: algorithm
slug: composition-generation
name: Composition generation
aliases:
- Generating compositions
- Next composition in lexicographic order
area: combinatorics/generating-partitions-and-trees
level: core
summary: Lists all 2^(n-1) compositions of n in lexicographic order by a successor rule that is a binary countdown on the cut set, in constant amortized time.
solves: [integer-compositions]
model: word-ram
complexity:
  vars: {n: the integer that is split, N: "the number of compositions, 2^(n-1)"}
  time: {worst: Θ(N), amortized: Θ(1)}
  space: {extra: Θ(n)}
properties: {in_place: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 1978
  people: [Albert Nijenhuis, Herbert S. Wilf]
  note: Nijenhuis and Wilf gave the successor routine NEXCOM for compositions into k parts in their 1978 book. The lexicographic successor on this page is the binary counter on the cut set and has no single inventor.
prereqs: [integer-compositions, constant-amortized-time-generation]
see_also: [binary-counter-increment, binary-reflected-gray-code, power-set-enumeration, lexicographic-combinations, integer-partition-generation, set-partition-generation, lexicographic-successor, loopless-generation]
sources:
  - book: isbn:9780125192606
    title: Albert Nijenhuis and Herbert S. Wilf, Combinatorial Algorithms for Computers and Calculators, second edition, Academic Press, 1978
    locator: Chapter 5, Next composition of n into k parts (NEXCOM), and Chapter 6, Random composition of n into k parts (RANCOM)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Section 1.2, How to count (the bijection between compositions of n and subsets of [n-1])
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1, Generating all n-tuples (binary counting and Gray codes, which act on the cut set)
  - paper: doi:10.1098/rsta.1893.0017
    title: P. A. MacMahon, Memoir on the theory of the compositions of numbers, Philosophical Transactions of the Royal Society of London A 184 (1893), 835-901
    locator: the whole paper
---

This algorithm lists the [compositions](/integer-compositions/) of an integer $n$ in lexicographic order, from $(1, 1, \ldots, 1)$ up to $(n)$. Each step moves one unit from the last part to the part before it, and breaks the rest of the last part into ones. The step is a [binary countdown](/binary-counter-increment/) on the set of cut points, so the whole list of $N = 2^{n-1}$ compositions takes $\Theta(N)$ time, which is [constant amortized time](/constant-amortized-time-generation/) for each composition.

## In plain words

Write each way to split the number as a list of parts in order, and list the splits as a dictionary would. The first split is all ones and the last split is the number itself.

To get the next split, look at the last part. Give one unit of it to the part before it, and then write what is left of the last part as single ones. If the last part was one, nothing is left, and the step is just the move of that one unit. Half of the splits end in a one, so most steps are short, and the work for each split is small on average.

## The problem

The input is an integer $n \ge 0$. The output is the list of all compositions of $n$, each one time, in increasing lexicographic order of the sequences of parts. A composition of $n$ is a sequence of integers $c_1, \ldots, c_m \ge 1$ with sum $n$, and there are $N = 2^{n-1}$ of them for $n \ge 1$ and one, the empty sequence, for $n = 0$.

The algorithm keeps the parts in an array $a[1 \ldots m]$. The visit of line L4 sees the array in place.

**The cut set.** Each composition of $n \ge 1$ is fixed by its partial sums $c_1, c_1 + c_2, \ldots$, a subset of $\{1, \ldots, n - 1\}$. Write this subset as a string of $n - 1$ bits, with bit $i$ equal to $1$ when $i$ is a partial sum. Lexicographic order of compositions is then decreasing order of these bits read as binary numbers, from $11 \ldots 1$ down to $00 \ldots 0$.

## The algorithm

```pseudo id=main
COMPOSITIONS(n)                             ▷ visit a[1 .. m] in lexicographic order
L1  if n = 0 then visit the empty composition and return
L2  m ← n, a[1 .. n] ← 1, …, 1              ▷ the smallest composition
L3  loop
L4      visit a[1 .. m]
L5      if m = 1 then return                ▷ a = (n), the last composition
L6      t ← a[m] − 1                        ▷ units left after one unit moves
L7      m ← m − 1, a[m] ← a[m] + 1          ▷ the last part gives one unit to the part before it
L8      while t > 0 do m ← m + 1, a[m] ← 1, t ← t − 1
```

The successor of $c = (c_1, \ldots, c_m)$ with $m \ge 2$ is $(c_1, \ldots, c_{m-2}, c_{m-1} + 1, 1^{c_m - 1})$. In the cut set, the last part $c_m$ is a final $1$ followed by $c_m - 1$ zeros. Subtracting $1$ from this binary number turns the final $1$ into $0$, which joins one unit to part $m - 1$, and turns the $c_m - 1$ zeros into ones, which are the new parts of size $1$.

## Example

Take $n = 4$. There are $2^3 = 8$ compositions.

| visit | $a$ | cut bits | $t$ | runs of L8 | next $a$ |
| --- | --- | --- | --- | --- | --- |
| 0 | $1, 1, 1, 1$ | $111$ | $0$ | $0$ | $1, 1, 2$ |
| 1 | $1, 1, 2$ | $110$ | $1$ | $1$ | $1, 2, 1$ |
| 2 | $1, 2, 1$ | $101$ | $0$ | $0$ | $1, 3$ |
| 3 | $1, 3$ | $100$ | $2$ | $2$ | $2, 1, 1$ |
| 4 | $2, 1, 1$ | $011$ | $0$ | $0$ | $2, 2$ |
| 5 | $2, 2$ | $010$ | $1$ | $1$ | $3, 1$ |
| 6 | $3, 1$ | $001$ | $0$ | $0$ | $4$ |
| 7 | $4$ | $000$ | | | stop |

The cut bits count down from $7$ to $0$. Line L8 runs $0 + 1 + 0 + 2 + 0 + 1 + 0 = 4$ times in all, which is $2^3 - 4$.

## Correctness

Let $c$ be a composition with $m \ge 2$ parts. A larger composition $d$ of $n$ cannot first differ from $c$ at the last index $m$, because then $d_m$ would exceed what is left of $n$. So it first differs at an index $i \le m - 1$ with $d_i > c_i$. The smallest such $d$ uses the largest $i = m - 1$, the smallest value $c_{m-1} + 1$ there, and the smallest composition of the $c_m - 1$ units that remain, which is all ones. This is what lines L6 to L8 write. The algorithm starts at $(1^n)$, the smallest composition, and stops at $(n)$, the largest. So it visits each composition exactly once, in increasing order. The full proof is in the proof file.

## Complexity

**Each step.** One step costs $O(1)$ plus $O(1)$ for each run of the loop body of line L8. The step from $c$ runs it $c_m - 1$ times.

**Total of line L8.** For $1 \le j \le n - 1$ there are $2^{n-j-1}$ compositions of $n$ with last part $j$, one for each composition of $n - j$. So the total number of runs is

$$\sum_{j=1}^{n-1} (j - 1)\, 2^{n-1-j} = 2^{n-1} - n,$$

by induction on $n$ with $T(n + 1) = 2T(n) + n - 1$. This is less than one run for each composition.

**Total.** The time is $\Theta(2^{n-1})$ for the whole list, so $\Theta(1)$ amortized for each composition. The extra space is the array of $n + 1$ entries.

- **Delay.** The algorithm is CAT but not [loopless](/loopless-generation/). The step from $(1, n - 1)$ to $(2, 1^{n-2})$ runs line L8 $n - 2$ times, so the worst delay is $\Theta(n)$.
- **Lower bound.** Each method must output $2^{n-1}$ compositions, so $\Omega(2^{n-1})$ time is necessary, and the algorithm is optimal up to a constant factor.
- **Copies.** If each composition is copied, as the Python code does, the total time is the total number of parts, $(n + 1)\, 2^{n-2}$ for $n \ge 2$.

## Properties

- **In place, no recursion.** The state is one array and $m$.
- **Successor only.** Each step needs only the current composition, so the generation can start at any composition and stop at any time.
- **Rank.** The rank of $c$ in the list, from $0$, is $2^{n-1} - 1 - b(c)$, where $b(c)$ is the cut bit string read as a binary number. Unranking reads the bits of $2^{n-1} - 1 - r$.
- **Prefix blocks.** The compositions with first part $j$ form one block of $2^{n-j-1}$ consecutive entries for $j < n$, in the order $j = 1, 2, \ldots$.
- **Not a Gray code.** One step can change many parts, as in the step from $(1, 3)$ to $(2, 1, 1)$.

## Variants and improvements

- **Reverse lexicographic order.** Write $c = (c_1, \ldots, c_r, 1^t)$ with $c_r \ge 2$. Its predecessor is $(c_1, \ldots, c_{r-1}, c_r - 1, t + 1)$. This is a binary increment on the cut set, and it is CAT as well: the scan for the trailing ones has total length at most $2^{n-1}$, because at most $2^{n-1-t}$ compositions end with $t$ or more ones.
- **Gray code.** List the cut sets in [binary reflected Gray code](/binary-reflected-gray-code/) order. Each step flips one bit, so it either merges two neighbor parts or splits one part in two. With the composition kept as its cut set, each step takes $O(1)$ worst-case time, so the order is [loopless](/loopless-generation/) in that form.
- **Exactly $k$ parts.** The compositions with $k$ parts match the $(k-1)$-subsets of $\{1, \ldots, n - 1\}$, so [combination generation](/lexicographic-combinations/) lists them, $C(n-1, k-1)$ in all. Nijenhuis and Wilf's NEXCOM lists the weak compositions into $k$ parts, where parts may be $0$.
- **Recursion on the first part.** Choose the first part $j = 1, \ldots, n$ and list the compositions of $n - j$ after it. This gives the same order with depth up to $n$.
- **Random composition.** Choose each of the $n - 1$ cut bits by a fair coin. RANCOM in Nijenhuis and Wilf samples a composition with exactly $k$ parts.
- **Restricted parts.** For parts in a set $A$, recursion on the first part lists only the valid compositions. The counts $c_A(s)$ tell which first parts can be completed, so the recursion has no dead ends.

## When to use it

Use it when you need all compositions of $n$ in lexicographic order, or in any order with a short successor rule. If the only aim is to loop over the cut sets, a plain loop over the integers from $0$ to $2^{n-1} - 1$ is simpler. Use the Gray code when each visit updates a cost that changes little when two neighbor parts merge or a part splits. To count compositions, use the formula $2^{n-1}$ or [counting integer compositions](/counting-integer-compositions/) instead of a list.

## Pitfalls

- **$n = 0$.** There is one composition of $0$, the empty one. A loop over $2^{n-1}$ cut sets gives the wrong answer here, since $2^{-1}$ is not an integer count.
- **Order of the bits.** Bit $1$ of the cut set, the cut after the first unit, is the most significant bit for lexicographic order. With the other bit order, the list is the order of the reversed compositions, not lexicographic order.
- **Array size.** The array needs $n$ entries, for the composition $(1^n)$.
- **Shared state.** The visit sees the array that the next step changes. Copy it if you store it.
- **Growth.** The list doubles with each unit. For $n = 40$ it has more than $5 \times 10^{11}$ entries.

## Implementations

The Python code yields a tuple copy of each composition, so its time is the total number of parts. The function `extra_writes` runs the same steps without visits and returns the number of runs of line L8.

## History

MacMahon studied compositions in a memoir of 1893 and later in his Combinatory Analysis. The correspondence between compositions and subsets of $\{1, \ldots, n - 1\}$ is standard, see Stanley, Section 1.2. Nijenhuis and Wilf gave the routines NEXCOM and RANCOM for compositions into $k$ parts in 1978. Since the lexicographic successor is the binary counter on the cut set, the generators for $n$-tuples and Gray codes in Knuth's Section 7.2.1.1 also apply.

## References
