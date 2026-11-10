---
tag: 2KYK32
kind: theorem
slug: bin-packing-np-hardness
name: Bin packing is strongly NP-hard
aliases:
- strong NP-hardness of bin packing
- 3/2 hardness of bin packing
area: approximation/covering-and-packing
level: core
summary: Bin packing stays NP-hard even with numbers bounded by a polynomial, via 3-partition.
prereqs: [bin-packing, partition-problem, three-partition, strong-np-hardness, polynomial-time-reduction]
see_also: [bin-packing-inapproximability, first-fit-decreasing, bin-packing-aptas, no-fptas-for-strongly-np-hard-problems, pseudo-polynomial-time, gap-problem]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Section 4.2 (strong NP-completeness and 3-PARTITION), Appendix A4.1 problem SR1 (Bin packing), A3.2 problem SP12 (Partition) and SP15 (3-Partition)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 9 (the 3/2 hardness from partition)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 3.3 (bin packing, the reduction from partition)
  - paper: doi:10.1137/0204035
    title: "M. R. Garey and D. S. Johnson, Complexity results for multiprocessor scheduling under resource constraints, SIAM Journal on Computing 4(4), 1975"
    locator: the strong NP-completeness of 3-PARTITION
---

The decision version of [bin packing](/bin-packing/) is NP-complete, and it stays NP-complete when all numbers are bounded by a polynomial in the input length, so it is [strongly NP-hard](/strong-np-hardness/). A reduction from [partition](/partition-problem/) also shows that no polynomial-time algorithm uses fewer than $\frac32 \mathrm{OPT}$ bins on every input unless P = NP. The bound $\frac32$ is tight, because [first fit decreasing](/first-fit-decreasing/) always uses at most $\frac32 \mathrm{OPT}$ bins.

## Statement

Notation is as on [bin packing](/bin-packing/): $n$ items with sizes $s_i \in (0, 1]$, capacity 1, and $\mathrm{OPT}$ the least number of bins. In the decision version BIN PACKING, the input is a capacity $C$, integer sizes $a_1, \ldots, a_n$ with $1 \le a_i \le C$ and an integer $k$, and the question is whether the items fit into $k$ bins of capacity $C$.

**Theorem.**

1. BIN PACKING is NP-complete.
2. BIN PACKING is NP-complete in the strong sense: there is a polynomial $p$ such that it stays NP-complete on the instances with $C \le p(n)$.
3. Let $\rho < \frac32$. If a polynomial-time algorithm $A$ satisfies $A(L) \le \rho \cdot \mathrm{OPT}(L)$ for every list $L$, then P = NP.

## In plain words

Suppose you could always tell, fast, whether a set of objects fits into two boxes. Then you could also tell whether a set of numbers can be split into two halves with equal sums, which is a famous hard question. So the box question is hard too, already for two boxes.

This has a strong effect on fast approximate methods. If a method could always come within less than one and a half times the best, then on the inputs where two boxes are enough it would have to use two boxes, because three is already too many. So it would answer the hard question. A second reduction, from splitting numbers into groups of three, shows that the problem stays hard even when all the numbers are small.

## Proof

*Membership in NP.* A certificate is the map from items to bins. Checking that each of the $k$ loads is at most $C$ takes $O(n + k)$ additions, and $k \le n$ can be assumed, because $n$ bins always suffice.

*Part 1 and part 3, from PARTITION.* An instance of [partition](/partition-problem/) is a list of positive integers $a_1, \ldots, a_n$, and the question is whether some subset has sum exactly half of the total. If the total is odd, the answer is no. Otherwise let the total be $2B$. If some $a_i > B$, the answer is no as well. In the remaining case, map the instance to the bin packing list with capacity $C = B$ and sizes $a_1, \ldots, a_n$ (so $s_i = a_i / B \le 1$), and $k = 2$. This map takes polynomial time. The total size is $S = 2$.

- If a subset $T$ has sum $B$, then $T$ and its complement are two bins with load exactly $B$. So $\mathrm{OPT} \le 2$.
- If two bins suffice, their loads are at most $B$ and add to $2B$, so each load is exactly $B$, and the items of one bin form a subset with sum $B$.

Since $S = 2$, the size bound gives $\mathrm{OPT} \ge 2$. So the partition instance is a yes-instance if and only if $\mathrm{OPT} = 2$, and it is a no-instance if and only if $\mathrm{OPT} \ge 3$. PARTITION is NP-complete (Karp 1972), so BIN PACKING is NP-complete. This proves part 1.

For part 3, run $A$ on the list. On a yes-instance, $A \le \rho \cdot 2 < 3$, and $A$ is an integer, so $A = 2$. On a no-instance, $A \ge \mathrm{OPT} \ge 3$. So the test "$A \le 2$" decides PARTITION in polynomial time, and P = NP.

*Part 2, from 3-PARTITION.* An instance of [3-partition](/three-partition/) is a bound $B$ and $3m$ positive integers $a_1, \ldots, a_{3m}$ with $B/4 < a_i < B/2$ for each $i$ and $\sum_i a_i = mB$. The question is whether the integers split into $m$ groups that each have sum exactly $B$. Garey and Johnson (1975) proved that 3-PARTITION is NP-complete in the strong sense: it stays NP-complete when $B \le q(m)$ for a polynomial $q$.

Map the instance to BIN PACKING with $C = B$, the same sizes, and $k = m$. The numbers do not change, so an instance with $B \le q(m)$ maps to an instance with $C \le q(n)$, where $n = 3m$.

- If the groups exist, each group is a bin with load exactly $B$.
- If $m$ bins suffice, the loads are at most $B$ and add to $mB$, so each load is exactly $B$. A bin with at most two items has load less than $2 \cdot B/2 = B$, and a bin with at least four items has load more than $4 \cdot B/4 = B$. So each bin has exactly three items, and the bins are the groups.

So BIN PACKING restricted to $C \le q(n)$ is NP-complete, which is part 2. $\blacksquare$

## Consequences

- **No pseudo-polynomial algorithm.** Unless P = NP, no algorithm solves BIN PACKING in time polynomial in $n$ and $C$. Such an algorithm would solve the instances of part 2 in polynomial time. Compare [knapsack](/knapsack-problem/) and [subset sum](/subset-sum-problem/), which have [pseudo-polynomial](/pseudo-polynomial-time/) algorithms.
- **No absolute PTAS and no FPTAS.** Part 3 rules out an absolute [PTAS](/ptas/). It also follows from the general result on [strongly NP-hard problems](/no-fptas-for-strongly-np-hard-problems/), since $\mathrm{OPT} \le n$.
- **The asymptotic ratio is the right measure.** The argument of part 3 uses instances with $\mathrm{OPT} = 2$. It says nothing about $\mathrm{ALG} \le \rho \cdot \mathrm{OPT} + c$ for a constant $c \ge 1$. In fact, the [asymptotic scheme](/bin-packing-aptas/) gives $(1 + \varepsilon)\mathrm{OPT} + 1$ for each $\varepsilon > 0$, and [Karmarkar and Karp](/karmarkar-karp-bin-packing/) give $\mathrm{OPT} + O(\log^2 \mathrm{OPT})$.
- **A gap problem.** The reduction of part 3 shows that the [gap problem](/gap-problem/) "is $\mathrm{OPT} = 2$ or is $\mathrm{OPT} \ge 3$?" is NP-hard. More gap results are on [bin packing inapproximability](/bin-packing-inapproximability/).

## Tightness

The constant $\frac32$ in part 3 cannot be raised. [First fit decreasing](/first-fit-decreasing/) satisfies $\mathrm{FFD} \le \frac32 \mathrm{OPT}$ on every list, with a short proof on its page. The bound of part 3 is reached by first fit decreasing on a partition instance: with capacity 8, the sizes $(4, 3, 3, 2, 2, 2)$ split as $\{4, 2, 2\}$ and $\{3, 3, 2\}$, so $\mathrm{OPT} = 2$, but first fit decreasing packs $[4\ 3]$, $[3\ 2\ 2]$, $[2]$ and uses 3 bins.

Part 2 needs the numbers of 3-PARTITION in the window $(B/4, B/2)$ only to force three items in each bin. Part 1 needs only two bins, so BIN PACKING is NP-complete already for $k = 2$. For each fixed $C$ the problem is polynomial: there are at most $C$ distinct sizes, so a dynamic program over the vector of counts of each size has at most $(n+1)^C$ states, and each state tries the at most $(n+1)^C$ ways to fill one bin. This is the high multiplicity view of the [cutting stock problem](/cutting-stock-problem/).

## History

Bin packing is problem SR1 in the list of Garey and Johnson (1979), where its strong NP-completeness is shown by the reduction from 3-PARTITION. Garey and Johnson (1975) introduced 3-PARTITION and proved it strongly NP-complete. PARTITION is one of the 21 problems of [Karp (1972)](/karps-21-np-complete-problems/). The $\frac32$ consequence for approximation is the standard textbook argument, given for example by Vazirani (Chapter 9) and by Williamson and Shmoys (Section 3.3).

## References
