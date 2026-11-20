---
tag: 0Y9DP6
kind: algorithm
slug: dhondt-method
name: "D'Hondt method"
aliases:
- Jefferson method
- greatest divisors method
area: algorithmic-game-theory/social-choice-and-voting
level: intro
summary: Assigns seats one at a time to the party with the largest votes divided by one plus its seats. It favours large parties.
model: word-ram
complexity:
  vars: {n: the number of parties, h: the number of seats}
  time: {worst: O(n + h log n)}
  space: {extra: O(n)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1792
  people: [Thomas Jefferson, Victor D'Hondt]
  note: "Jefferson's method apportioned the US House from the census of 1790 to that of 1830. Victor D'Hondt proposed the same rule for party lists in Belgium in the 1870s and 1880s."
prereqs: [apportionment-problem, priority-queue]
see_also: [apportionment-problem, sainte-lague-method, huntington-hill-method, hamilton-method, balinski-young-theorem, alabama-paradox, binary-heap, single-transferable-vote]
sources:
  - book: isbn:9780815701118
    title: "Michel L. Balinski and H. Peyton Young, Fair Representation: Meeting the Ideal of One Man, One Vote, 2nd edition, Brookings Institution Press, 2001"
    locator: "Chapter 3 (The Methods of Jefferson and Hamilton), Chapter 10 (Staying within the Quota) and Appendix A (The Theory of Apportionment)"
  - paper: "M. L. Balinski and H. P. Young, The quota method of apportionment, American Mathematical Monthly 82(7) (1975), 701-730"
    locator: Jefferson's method is the only divisor method that satisfies lower quota
  - paper: doi:10.1007/978-3-319-13075-0_46
    title: "Zhanpeng Cheng and David Eppstein, Linear-time algorithms for proportional apportionment, Proc. 25th International Symposium on Algorithms and Computation (ISAAC 2014), LNCS 8889, 581-592"
    locator: divisor methods in O(n) time, independent of the number of seats
---

The D'Hondt method apportions $h$ seats among parties or states in proportion to their votes. It gives the seats one at a time, each to the party with the largest quotient of its votes divided by one more than its seats so far. It is the same as Jefferson's method, the divisor method that rounds every quota down. It has none of the paradoxes of [Hamilton's method](/hamilton-method/), and it never gives a party less than its lower quota, but it can give a large party more than its upper quota.

## In plain words

Write each party's vote total at the top of a column. Below it write the total divided by 2, by 3, by 4, and so on. Now give the seats to the largest numbers in the whole table, one seat for each number, until all seats are gone. A party with twice the votes of another gets about twice the seats. Small parties are cut a little: the method rounds down, and the rounding hurts a party with few seats the most.

## The problem

The input is the votes $p_1, \ldots, p_n \ge 0$, integers with sum $P > 0$, and the number of seats $h$. The output is integers $a_i \ge 0$ with $\sum_i a_i = h$. The quota of party $i$ is $q_i = h p_i / P$. See the [apportionment problem](/apportionment-problem/) for the setting and the other methods.

Jefferson's method in divisor form is: find a divisor $\lambda > 0$ such that $\sum_i \lfloor p_i / \lambda \rfloor = h$, and give party $i$ the seats $a_i = \lfloor p_i / \lambda \rfloor$. The D'Hondt rule in highest averages form gives each seat to the party with the largest $p_i/(a_i + 1)$, ties to the smallest index. The two forms give the same apportionments.

## The algorithm

A [priority queue](/priority-queue/) holds one key per party, its next quotient. A [binary heap](/binary-heap/) compares two keys $p_i/d_i$ and $p_j/d_j$ by the integers $p_i d_j$ and $p_j d_i$, with no division.

```pseudo id=main
D'HONDT(p, h)                             ▷ p = (p_1, ..., p_n) votes, h seats
L1  a_i ← 0 for each i
L2  Q ← a max-priority queue of the parties, with keys p_i / 1
L3  repeat h times
L4      i ← extract from Q the largest key, the smallest index among ties
L5      a_i ← a_i + 1
L6      insert i into Q with key p_i / (a_i + 1)
L7  return a
```

Each pass of lines L3 to L6 gives one seat and puts the party back with its next quotient.

## Example

Four parties have 100000, 80000, 30000 and 20000 votes, and $h = 8$ seats are to be filled. The table lists the quotients $p_i / d$; the numbers in bold get the seats, in the order given in brackets.

| divisor | party 1 | party 2 | party 3 | party 4 |
|---|---|---|---|---|
| 1 | **100000** (1) | **80000** (2) | **30000** (6) | 20000 |
| 2 | **50000** (3) | **40000** (4) | 15000 | 10000 |
| 3 | **33333** (5) | **26667** (7) | 10000 | 6667 |
| 4 | **25000** (8) | 20000 | 7500 | 5000 |
| 5 | 20000 | 16000 | 6000 | 4000 |

The result is $(4, 3, 1, 0)$. The quotas are $3.48$, $2.78$, $1.04$ and $0.70$, so party 1 gets its upper quota and party 4 its lower quota 0. [Hamilton's method](/hamilton-method/), the [Sainte-Lague method](/sainte-lague-method/) and the [Huntington-Hill method](/huntington-hill-method/) all give $(3, 3, 1, 1)$. Any divisor $\lambda$ with $20000 < \lambda \le 25000$ gives the same result in divisor form: for $\lambda = 22000$, $\lfloor 100000/22000 \rfloor = 4$, $\lfloor 80000/22000 \rfloor = 3$, $\lfloor 30000/22000 \rfloor = 1$ and $\lfloor 20000/22000 \rfloor = 0$. The ninth seat is a three-way tie at 20000, between parties 1, 2 and 4; the smallest index gives it to party 1.

## Correctness

The [proof](proofs/correctness.md) shows that the keys of the seats, in the order they are given, never increase. Let $\ell$ be the largest key left at the end and $u = \min_i p_i/a_i$ the smallest key that won a seat. Then $\ell \le u$, and every $\lambda$ with $\ell < \lambda \le u$ gives $a_i = \lfloor p_i/\lambda \rfloor$ for every party. So the highest averages rule computes Jefferson's divisor method, and its result is unique when $\ell < u$. The proof also shows lower quota, the least-cost form below, house monotonicity and population monotonicity.

## Complexity

Building the heap takes $O(n)$ time, and each of the $h$ seats costs $O(\log n)$, so the total is $O(n + h \log n)$, with $O(n)$ extra space. A linear scan for the largest key instead of the heap gives $O(n h)$. Cheng and Eppstein (2014) solve every divisor method in $O(n)$ time, independent of $h$: they start from an estimate of $\lambda$ near $P/h$, which leaves only $O(n)$ seats to place, and they place them by [selection](/selection-problem/). The comparisons use products of numbers of $O(\log P + \log h)$ bits.

## Properties

- **Lower quota.** Every party gets at least $\lfloor q_i \rfloor$. Jefferson's method is the only divisor method with this property (Balinski and Young 1975).
- **Upper quota fails.** With votes $(8, 2, 1, 1)$ and $h = 7$, the method gives $(6, 1, 0, 0)$, while the quota of party 1 is $14/3 = 4.67$. There is no tie in this example.
- **House monotone.** One more seat never takes a seat from anyone, so there is no [Alabama paradox](/alabama-paradox/).
- **Population monotone.** If party $i$ gains votes and party $j$ loses votes, $i$ does not lose a seat to $j$, except through a tie.
- **Bias to large parties.** Rounding down favors the parties with many seats. In the example, the largest party gets its upper quota, and the smallest gets nothing.
- **Least cost.** The result minimizes $\sum_i a_i (a_i + 1)/p_i$, because the cost of the next seat of party $i$, $2(a_i + 1)/p_i$, grows with $a_i$, and the method always takes the cheapest next seat.

## Variants and improvements

- **Other divisors.** The [Sainte-Lague method](/sainte-lague-method/) divides by $2a + 1$ and rounds at one half. The [Huntington-Hill method](/huntington-hill-method/) rounds at the geometric mean $\sqrt{a (a + 1)}$. Adams's method rounds up, the mirror of Jefferson's, and favors small parties.
- **Thresholds.** Many laws give no seats to lists below a share of the votes, such as 3 or 5 percent, and run the method on the others.
- **Biproportional apportionment.** Seats are apportioned to parties and to districts at the same time, with one divisor per party and one per district.
- **A quota with a cap.** Balinski and Young's quota method gives seats one at a time like D'Hondt, but only to parties still below their upper quota.

## When to use it

Use the D'Hondt method for party lists when stable majorities matter more than exact proportionality for small parties, or when the law asks for it. It is simple to compute and to check, it has no paradoxes, and it never denies a party its lower quota. If small parties must be treated as fairly as large ones, the [Sainte-Lague method](/sainte-lague-method/) is unbiased. If every party must stay within quota, use [Hamilton's method](/hamilton-method/), at the price of its paradoxes.

## Pitfalls

- **Floating point.** Quotients such as $100000/3$ and $80000/3$ are not exact in floating point, and ties like the three-way tie at 20000 in the example can be decided by rounding errors. Compare $p_i d_j$ with $p_j d_i$.
- **Ties.** The law must say how to break a tie for the last seat. This page gives it to the smallest index; real laws often use the larger vote total or a lot.
- **Divisors from 1.** The divisors are $1, 2, 3, \ldots$. With divisors $2, 3, 4, \ldots$ (the Imperiali method) or $1.4, 3, 5, \ldots$ (a modified Sainte-Lague), the result differs.
- **Zero votes.** A party with no votes has key 0. It can get a seat only if every other key is 0, which needs $P = 0$, an invalid input.

## Implementations

## History

Thomas Jefferson proposed the method for the US House after the census of 1790. After Washington vetoed Hamilton's method in 1792, Congress adopted Jefferson's, and it was used until the census of 1830. Its bias to large states led to its end: after the census of 1830 it gave New York 40 seats, while its quota was about 38.6. Victor D'Hondt, a Belgian lawyer, proposed the same rule for party lists in the 1870s and 1880s, in the highest averages form, and Belgium adopted it. It is now one of the most used rules for party-list elections, for example in Spain and Portugal, and Balinski and Young (1975, 1982) showed that it is the only divisor method that satisfies lower quota.

## References
