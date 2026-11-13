---
tag: 8ZZ2XW
kind: problem
slug: josephus-problem
name: Josephus problem
aliases:
- Josephus permutation
area: games-and-search/puzzles
level: intro
summary: People 1 to n stand in a circle and every k-th one still there is removed. Find the last one left, or the whole order. O(n) by a recurrence; for k = 2 a bit rotation of n.
prereqs: [recurrence-relation, circular-linked-list]
see_also: [order-statistic-tree, fenwick-tree, linked-list, queue, segment-tree]
sources:
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, 2nd edition, Addison-Wesley, 1994
    locator: Section 1.3 (The Josephus Problem, the case of every second person and its closed form) and Section 3.3 (Floor/Ceiling Recurrences, the survivor for every q-th person)
  - paper: doi:10.1017/S0017089500008272
    title: A. M. Odlyzko and H. S. Wilf, Functional iteration and the Josephus problem, Glasgow Mathematical Journal 33(2), 1991, 235 to 240
    locator: the whole paper (the iteration x to ceil(q x / (q - 1)) behind the survivor formula of Concrete Mathematics, Section 3.3)
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, 3rd edition, MIT Press, 2009
    locator: Chapter 14, Problem 14-2 (the Josephus permutation in O(n lg n) time with an order-statistic tree)
---

The Josephus problem puts $n$ people, numbered 1 to $n$, in a circle, and removes every $k$-th person still in the circle until one is left. The *Josephus permutation* is the order of removal, and $J(n, k)$ is the number of the last person left. The survivor follows from the recurrence $J(n, k) = ((J(n-1, k) + k - 1) \bmod n) + 1$ in $O(n)$ time, and for $k = 2$ it is a one-bit [rotation](/bitwise-operations/) of the binary form of $n$ (Graham, Knuth and Patashnik, Section 1.3). The whole order takes $O(n \log n)$ time with an [order-statistic tree](/order-statistic-tree/) or a [Fenwick tree](/fenwick-tree/).

## In plain words

A group of people stand in a ring. You count around the ring, and every time you reach a fixed count, that person leaves the ring. The counting goes on from the next person, around and around, skipping the people who already left. Who is the last person in the ring?

You can play it out with a list in which people are taken away one by one, but that is slow for a large group. A better way works backward: the survivor of a ring of a given size tells you the survivor of a ring with one more person, after you shift the numbers. When every second person leaves, there is a neat trick: write the size of the ring in binary, move the first digit to the end, and read off the survivor.

## Definition

Fix integers $n \ge 1$ and $k \ge 1$. The people are $1, \ldots, n$ in a circle, in this order. Start the count at person 1. Repeat until the circle is empty: count $k$ people around the circle, starting with the current one, remove the $k$-th, and make the next person in the circle the current one.

- **Survivor.** Output $J(n, k)$, the last person removed.
- **Permutation.** Output the order of removal $\pi_1, \ldots, \pi_n$, the $(n, k)$-Josephus permutation, so that $\pi_n = J(n, k)$.
- **Step query.** Output the person removed at step $i$, or the step at which person $p$ is removed.

Write $J_0(n, k) = J(n, k) - 1$ for the 0-indexed survivor. The input size is $O(\log n + \log k)$ bits for the survivor, and the output of the permutation has $n$ numbers.

## Variants

- **Every second person.** $k = 2$, with a closed form; see Examples.
- **A different start, or a reversed direction.** Shift or reflect the numbers: starting the count at person $s$ gives survivor $((J(n, k) + s - 2) \bmod n) + 1$.
- **Several survivors.** The last $t$ people removed, for example the last two in the story of Josephus.
- **Choosing the count.** Given $n$ and a person $p$, find a $k$ with $J(n, k) = p$.
- **Varying counts.** The count changes from step to step; the rank-select structures below still apply, since each step is one select and one delete.

## Examples

**$n = 10$, $k = 2$.** The removal order is $2, 4, 6, 8, 10, 3, 7, 1, 9, 5$, so $J(10, 2) = 5$. In binary $10 = 1010_2$; moving the leading 1 to the end gives $0101_2 = 5$.

**$n = 7$, $k = 3$.** The order is $3, 6, 2, 7, 5, 1, 4$, so $J(7, 3) = 4$.

**The story.** In the version told in Concrete Mathematics, 41 people stand in a circle and every third is removed. The last two removed are 16 and 31, so the places 16 and 31 survive to the end; $J(41, 3) = 31$.

**Small values.**

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $J(n, 2)$ | 1 | 1 | 3 | 1 | 3 | 5 | 7 | 1 | 3 | 5 | 7 | 9 | 11 | 13 | 15 | 1 |
| $J(n, 3)$ | 1 | 2 | 2 | 1 | 4 | 1 | 4 | 7 | 1 | 4 | 7 | 10 | 13 | 2 | 5 | 8 |

Also $J(100, 2) = 73$ and $J(100, 3) = 91$.

**The recurrence.** For $n \ge 2$, $J_0(n, k) = (J_0(n - 1, k) + k) \bmod n$, with $J_0(1, k) = 0$. *Proof.* Number the people $0, \ldots, n - 1$. The first person removed is $(k - 1) \bmod n$. The count then starts at $k \bmod n$, and the game goes on as a game of $n - 1$ people. Renumber the remaining people so that $k \bmod n$ becomes $0$, the next one $1$, and so on around the circle; the person with new number $x$ has old number $(x + k) \bmod n$. The survivor has new number $J_0(n - 1, k)$, so its old number is $(J_0(n - 1, k) + k) \bmod n$. $\square$

**The case $k = 2$.** Write $n = 2^m + l$ with $0 \le l < 2^m$. Then $J(n, 2) = 2l + 1$. *Proof.* For $n = 2j$, the first round removes all even people, and the game goes on with $1, 3, \ldots, 2j - 1$ and the count at 1, a game of $j$ people where person $x$ is old person $2x - 1$; so $J(2j, 2) = 2J(j, 2) - 1$. For $n = 2j + 1$, the first round removes the even people and then person 1, and the game goes on with $3, 5, \ldots, 2j + 1$ from 3; so $J(2j + 1, 2) = 2J(j, 2) + 1$. Now induct on $m$. For $m = 0$, $n = 1$ and $J = 1 = 2 \cdot 0 + 1$. If $n = 2^m + l$ with $m \ge 1$, then $j = \lfloor n / 2 \rfloor = 2^{m-1} + \lfloor l/2 \rfloor$, so by induction $J(j, 2) = 2\lfloor l / 2 \rfloor + 1$. For even $l$, $J(n, 2) = 2(l + 1) - 1 = 2l + 1$. For odd $l$, $J(n, 2) = 2(l - 1 + 1) + 1 = 2l + 1$. $\square$

In binary, $n = 1 b_{m-1} \ldots b_0$ and $2l + 1 = b_{m-1} \ldots b_0 1$: the leading bit moves to the end. So $J(n, 2) = n$ exactly when $n = 2^m - 1$, and applying $J(\cdot, 2)$ again and again to $n$ ends at $2^{v} - 1$, where $v$ is the number of 1 bits of $n$ (Concrete Mathematics, Section 1.3).

## Known algorithms

- **Simulation.** Keep the people in a [circular linked list](/circular-linked-list/) or a [queue](/queue/) and step $k - 1$ times before each removal: $O(nk)$ time and $O(n)$ space, and it gives the whole permutation.
- **The recurrence.** Run $j \leftarrow (j + k) \bmod i$ for $i = 2, \ldots, n$: $O(n)$ arithmetic operations and $O(1)$ space for the survivor.
- **Many removals per round.** When $k \le n$, one pass around the circle removes $\lfloor n/k \rfloor$ people at once. Solve the smaller game of $n - \lfloor n/k \rfloor$ people and map the answer back by adding the number of removed people before it. Each call shrinks $n$ by the factor $1 - 1/k$, so there are $O(k \log n)$ calls, and the recurrence above handles the steps where $k > n$.
- **The ceiling iteration.** For $k \ge 2$ let $D_0 = 1$ and $D_j = \lceil k D_{j-1} / (k - 1) \rceil$. Then $J(n, k) = kn + 1 - D_j$ for the least $j$ with $D_j > (k - 1) n$ (Concrete Mathematics, Section 3.3). The $D_j$ grow by the factor $k/(k-1)$, so this takes $O(k \log n)$ steps; Odlyzko and Wilf (1991) studied this iteration and its growth constant.
- **Bit rotation.** For $k = 2$, $O(1)$ word operations: $J(n, 2) = 2(n - 2^{\lfloor \log_2 n \rfloor}) + 1$, with the [floor of the base 2 logarithm](/floor-log2/) from the bit length.
- **The permutation in $O(n \log n)$.** Keep the people still in the circle in an [order-statistic tree](/order-statistic-tree/), a [Fenwick tree](/fenwick-tree/) of 0 and 1 counts, or a [segment tree](/segment-tree/). If the current person has rank $r$ (from 0) among the $t$ people left, the next removal has rank $(r + k - 1) \bmod t$; select it and delete it in $O(\log n)$ time (CLRS, Problem 14-2). This is independent of $k$, and it also answers the step queries.

## Bounds

- **Survivor.** $O(n)$ time for every $k$, $O(k \log n)$ for small $k$, and $O(1)$ word operations for $k = 2$.
- **Permutation.** $O(n \log n)$ time, and $O(nk)$ by direct simulation, which is better when $k < \log n$; the output alone needs $\Omega(n)$ time.
- **Growth of the ceiling iteration.** For $k \ge 3$ the formula of Section 3.3 depends on the sequence $D_j$. Odlyzko and Wilf (1991) showed that $D_j$ is within $O(1)$ of $c\,(k/(k-1))^j$ for a constant $c$ that depends on $k$.

## Reductions

- **To order statistics.** Each removal is a select by rank followed by a delete in a dynamic set, so any structure with $O(\log n)$ rank select and delete gives the permutation in $O(n \log n)$.
- **To a recurrence.** The survivor is the solution of a first-order [recurrence](/recurrence-relation/) with a modulus, which the methods above evaluate quickly.

## Applications

- **Teaching.** The problem is the standard first example of a recurrence with a closed form found from a table, in Concrete Mathematics, Chapter 1, and of an augmented search tree, in CLRS.
- **Round-robin removal.** Any process that skips a fixed number of items in a ring and removes the next one follows the same rule, and the rank-select structures give the order fast.

## References
