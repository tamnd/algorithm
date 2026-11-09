---
tag: E69C97
kind: algorithm
slug: integer-partition-generation
name: Integer partition generation (Algorithm P)
aliases:
- Knuth's Algorithm P
- Partition generation in reverse lexicographic order
- Next partition of an integer
area: combinatorics/generating-partitions-and-trees
level: core
summary: Lists all partitions of n in reverse lexicographic order with constant amortized work per partition.
solves: [integer-partitions]
model: word-ram
complexity:
  vars: {n: the integer that is partitioned, N: "the number of partitions, p(n)"}
  time: {worst: Θ(N), amortized: Θ(1)}
  space: {extra: Θ(n)}
properties: {in_place: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 1970
  people: [J. K. S. McKay]
  note: McKay published a successor routine for partitions in natural order as Algorithm 371 of the Communications of the ACM in 1970. Knuth's Algorithm P in Section 7.2.1.4 is the tuned form of this method.
prereqs: [integer-partitions, constant-amortized-time-generation]
see_also: [integer-partitions, integer-partition-function, ferrers-diagram, conjugate-partition, composition-generation, set-partition-generation, lexicographic-combinations, next-permutation]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.4, Generating all partitions (Algorithm P, Partitions in reverse lexicographic order, and its analysis)
  - book: isbn:9780125192606
    title: Albert Nijenhuis and Herbert S. Wilf, Combinatorial Algorithms for Computers and Calculators, second edition, Academic Press, 1978
    locator: Chapter 9, Next partition of integer n (NEXPAR)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 3, Section 3.1, Integer partitions
  - paper: doi:10.1145/361953.361980
    title: J. K. S. McKay, Algorithm 371, Partitions in natural order, Communications of the ACM 13(1), 1970, 52
---

This algorithm lists the partitions of an integer $n$ in reverse lexicographic order, from $(n)$ down to $(1, 1, \ldots, 1)$. It keeps the current partition as a non-increasing array and finds the next one by a local change at the last part that is larger than $1$. It solves the [integer partition problem](/integer-partitions/) in $\Theta(p(n))$ total time, so the work for each partition is $O(1)$ amortized, which is [constant amortized time](/constant-amortized-time-generation/). It is Knuth's Algorithm P.

## In plain words

Write each split of the number with its parts from largest to smallest, and list the splits as a dictionary would, but backward: the split with the largest first part comes first. So the list starts with the number itself and ends with all ones.

To get the next split, look at the last part that is bigger than one. Make it one smaller. Take the unit that you removed and all the ones that follow it, and give them out again, as large as the new part allows, from left to right. If the part was a two, the step is short: the two becomes two ones. Most steps are short, so the work for each split is small on average.

## The problem

The input is an integer $n \ge 0$. The output is the list of all partitions of $n$, each one time, in reverse lexicographic order of the non-increasing sequences of parts. This is the [integer partition problem](/integer-partitions/) with a fixed order. The number of partitions is $N = p(n)$, the [partition function](/integer-partition-function/).

The algorithm keeps the parts in an array $a[1 \ldots m]$ with $a[1] \ge \cdots \ge a[m] \ge 1$ and $a[1] + \cdots + a[m] = n$. It also keeps $q$, the index of the last part greater than $1$, or $q = 0$ when all parts are $1$. The visit of line L5 sees the array in place.

## The algorithm

```pseudo id=main
PARTITIONS(n)                               ▷ visit a[1 .. m] in reverse lexicographic order
L1  if n = 0 then visit the empty partition and return
L2  a[1] ← n, m ← 1
L3  if n > 1 then q ← 1 else q ← 0          ▷ q is the index of the last part > 1
L4  loop
L5      visit a[1 .. m]
L6      if q = 0 then return                ▷ a = (1, …, 1), the last partition
L7      if a[q] = 2 then                    ▷ short step: 2 becomes 1 + 1
L8          a[q] ← 1, m ← m + 1, a[m] ← 1, q ← q − 1
L9      else                                ▷ a[q] ≥ 3
L10         x ← a[q] − 1, s ← m − q + 1, a[q] ← x, m ← q
L11         while s > x do m ← m + 1, a[m] ← x, s ← s − x
L12         m ← m + 1, a[m] ← s
L13         if s > 1 then q ← m else q ← m − 1
```

The parts after position $q$ are all $1$. Line L10 takes one unit from $a[q]$ and joins it with the $m - q$ ones that follow, so $s$ units must be placed after position $q$, each part at most $x$. Line L11 places as many parts $x$ as it can while more than $x$ units are left, and line L12 places the rest, a number from $1$ to $x$. Line L13 restores the meaning of $q$. In the branch of line L9, $x \ge 2$, so if the last part is $1$, the part before it is $x$ and is greater than $1$. The steps are those of Knuth's Algorithm P, with explicit names for the variables.

## Example

Take $n = 6$. There are $p(6) = 11$ partitions.

| visit | $a$ | $q$ | branch | runs of L11 | next $a$ |
| --- | --- | --- | --- | --- | --- |
| 0 | $6$ | 1 | L9 | 0 | $5, 1$ |
| 1 | $5, 1$ | 1 | L9 | 0 | $4, 2$ |
| 2 | $4, 2$ | 2 | L7 | 0 | $4, 1, 1$ |
| 3 | $4, 1, 1$ | 1 | L9 | 0 | $3, 3$ |
| 4 | $3, 3$ | 2 | L9 | 0 | $3, 2, 1$ |
| 5 | $3, 2, 1$ | 2 | L7 | 0 | $3, 1, 1, 1$ |
| 6 | $3, 1, 1, 1$ | 1 | L9 | 1 | $2, 2, 2$ |
| 7 | $2, 2, 2$ | 3 | L7 | 0 | $2, 2, 1, 1$ |
| 8 | $2, 2, 1, 1$ | 2 | L7 | 0 | $2, 1, 1, 1, 1$ |
| 9 | $2, 1, 1, 1, 1$ | 1 | L7 | 0 | $1, 1, 1, 1, 1, 1$ |
| 10 | $1, 1, 1, 1, 1, 1$ | 0 | stop | | |

At visit 6, $x = 2$ and $s = 4$: line L11 places one $2$ and leaves $s = 2$, and line L12 places the last $2$. The short branch of line L7 runs $5 = p(4)$ times, the long branch runs $5$ times, and the loop of line L11 runs $1$ time in all.

## Correctness

Let $\lambda = (a_1, \ldots, a_q, 1^r)$ with $a_q \ge 2$ and $r = m - q$. A partition that is smaller than $\lambda$ in lexicographic order must first differ from $\lambda$ at a position $i \le q$, because a partition that agrees with $\lambda$ on $a_1, \ldots, a_q$ must end with $r$ ones. The largest such partition differs at the last possible position $i = q$, takes the largest smaller value $a_q - 1$ there, and ends with the lexicographically largest partition of the remaining $r + 1$ units into parts of at most $a_q - 1$. That largest partition is the greedy one, as many parts $a_q - 1$ as possible and then the rest. This is what lines L7 to L13 write. The first partition $(n)$ is the largest, and the algorithm stops at $(1^n)$, the smallest. So it visits each partition of $n$ exactly once, in decreasing order. The full proof is in the proof file.

## Complexity

**Each step.** One step costs $O(1)$ plus $O(1)$ for each run of the loop body of line L11.

**The short branch.** The branch of line L7 runs when the last part greater than $1$ is a $2$, that is, when $\lambda$ contains a $2$. Removing one $2$ is a bijection from these partitions to the partitions of $n - 2$, so the short branch runs exactly $p(n - 2)$ times. The long branch runs $p(n) - 1 - p(n - 2)$ times.

**The loop of line L11.** Let a long step start from $\lambda = (a_1, \ldots, a_{q-1}, y, 1^r)$ with $y \ge 3$, and let $x = y - 1$. The loop runs $k = \lfloor r / x \rfloor$ times. Map each pair $(\lambda, j)$ with $1 \le j \le k$ to the partition

$$\nu = (a_1, \ldots, a_{q-1}, y, x^j, 1^{r - jx}).$$

In $\nu$, the smallest part greater than $1$ is $x$, it appears exactly $j$ times, and $x + 1 = y$ is also a part. From $\nu$ we get $x$ and $j$ back, and then $\lambda$, by turning the $j$ parts $x$ into ones. So the map is injective, and the total number of runs of line L11 is at most $p(n)$. In fact it equals the number of partitions of $n$ whose smallest part $z > 1$ has $z + 1$ also as a part, since each such partition is the image of a pair. For $n = 50$ this number is $116572$, against $p(50) = 204226$.

**Total.** The time is $\Theta(p(n))$ for the whole list, so $\Theta(1)$ amortized for each partition. The extra space is the array of $n + 1$ entries.

- **Delay.** The algorithm is CAT but not [loopless](/loopless-generation/). The step from $(3, 1^{n-3})$ to $(2^{\lfloor n/2 \rfloor}, 1^{n \bmod 2})$ runs line L11 $\lfloor (n - 3)/2 \rfloor$ times, so the worst delay is $\Theta(n)$.
- **Lower bound.** Each method must output $p(n)$ partitions, so $\Omega(p(n))$ time is necessary. The algorithm is optimal up to a constant factor.
- **Copies.** If each partition is copied, as the Python code does, the total time is $\Theta(\sum_{\lambda \vdash n} \ell(\lambda))$, see [integer partitions](/integer-partitions/).

## Properties

- **In place, no recursion.** The state is one array, $m$ and $q$.
- **Successor only.** Each step needs only the current partition and $q$, and $q$ can be found by a scan from the right. So the generation can start at any partition and stop at any time.
- **Order.** Reverse lexicographic order is also the order in which the [Ferrers diagrams](/ferrers-diagram/) of the partitions are sorted by their first rows, then their second rows, and so on, from the longest.
- **Not a Gray code.** One step can change many parts, as in the step from $(3, 1, 1, 1)$ to $(2, 2, 2)$.

## Variants and improvements

- **Lexicographic order.** The reverse list, from $(1^n)$ up to $(n)$, has a successor rule of the same kind. Zoghbi and Stojmenović (1998) gave fast successor algorithms for both orders.
- **Multiplicity form.** Keep the distinct parts with their multiplicities. A step then changes $O(1)$ pairs in the worst case. Nijenhuis and Wilf's NEXPAR uses this form.
- **Exactly $k$ parts.** Knuth's Algorithm H in the same section lists the partitions of $n$ into exactly $k$ parts.
- **Conjugates.** Listing the [conjugates](/conjugate-partition/) of the output gives the partitions in another order. Bounded parts become bounded length.
- **Gray codes.** Savage (1989) showed that the partitions of $n$ can be listed so that each step moves one unit from one part to another. Such an order has no simple successor rule of this kind.
- **Recursion.** Recursion on the largest part, as in [integer partitions](/integer-partitions/), visits the same list in the same order.

## When to use it

Use it when you need all partitions of $n$ and the order does not matter, or when you need reverse lexicographic order. It is the standard choice: it is short, it needs no recursion and no tables, and it is CAT. For one random partition, unrank a random integer or use a sampler instead of a list. To count the partitions without a list, use [partition counting](/integer-partition-counting/), since the list has $p(n)$ entries.

## Pitfalls

- **The value of $q$.** After the long branch, $q$ is $m$ when the last part $s$ is greater than $1$, and $m - 1$ when it is $1$. Setting $q \leftarrow m$ in both cases breaks the next step.
- **The short branch.** Without line L7, the long branch also works when $a[q] = 2$, but then $x = 1$ and line L11 writes all the ones again. Over the whole list this adds $\sum_{t \ge 1} p(n - 2 - t)$ runs of line L11, one for each $1$ in each partition of $n - 2$. For $n = 50$ that is $770947$ extra runs against $p(50) = 204226$ visits, and the ratio grows with $n$.
- **$n = 0$ and $n = 1$.** There is one partition of $0$, the empty one, and one partition of $1$. Line L3 sets $q = 0$ for $n = 1$, so the loop visits $(1)$ and stops.
- **Array size.** The array needs $n$ entries, for the partition $(1^n)$.
- **Shared state.** The visit sees the array that the next step changes. Copy it if you store it.
- **Growth.** $p(n)$ grows as $e^{\pi \sqrt{2n/3}}$ divided by a polynomial, see the [Hardy-Ramanujan theorem](/hardy-ramanujan-theorem/). A full list for $n = 200$, with $p(200) = 3972999029388$, is out of reach.

## Implementations

The Python code yields a tuple copy of each partition, so its time is the total number of parts. The function `step_counts` runs the same steps without visits and returns the counts of the two branches and of line L11.

## History

McKay published a successor routine for partitions in natural order as Algorithm 371 of the Communications of the ACM (1970). Nijenhuis and Wilf gave the routine NEXPAR in the multiplicity form (1978). Knuth, in Section 7.2.1.4, gives Algorithm P, analyzes the number of times each step runs, and gives Gray codes and Algorithm H for a fixed number of parts.

## References
