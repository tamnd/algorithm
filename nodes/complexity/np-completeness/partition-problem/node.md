---
tag: 2B3896
kind: problem
slug: partition-problem
name: Partition problem
aliases:
- equal-sum partition
- number partitioning
- set partition problem
area: complexity/np-completeness
level: intro
summary: Given positive integers, decide whether they can be split into two groups with equal sums. NP-complete, but only weakly, since a pseudo-polynomial algorithm exists.
prereqs: [subset-sum-problem, np-complete]
see_also: [subset-sum-problem, three-partition, weak-np-hardness, bin-packing-np-hardness, makespan-minimization, knapsack-problem, karps-21-np-complete-problems, scheduling-with-release-times-and-deadlines]
sources:
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum Press, 1972, pages 85 to 103
    locator: Section 4, the problem PARTITION and its reduction from KNAPSACK
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 3.1 (PARTITION is one of the six basic NP-complete problems, proved from 3DM), Section 4.2 (the pseudo-polynomial algorithm) and the appendix, problem SP12
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 34, the problems on subset sum (Section 34.5.5) and the exercises on set partition
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 8.8, Numerical Problems
  - paper: doi:10.1145/321812.321823
    title: Ellis Horowitz and Sartaj Sahni, Computing partitions with applications to the knapsack problem, Journal of the ACM 21(2), 1974
    locator: the main algorithm
  - paper: doi:10.1137/1.9781611974782.69
    title: Karl Bringmann, A near-linear pseudopolynomial time algorithm for subset sum, SODA 2017, pages 1073 to 1084
    locator: the main theorem (randomized O~(n + t) time)
---

The partition problem asks whether a list of positive integers can be split into two parts with equal sums. It is the [subset sum problem](/subset-sum-problem/) with the target equal to half the total. Karp proved it [NP-complete](/np-complete/) in 1972, and Garey and Johnson made it one of their six basic NP-complete problems. Like subset sum, it is only [weakly NP-hard](/weak-np-hardness/): a dynamic program decides it in time $O(nA)$, where $A$ is the total, which is [pseudo-polynomial](/pseudo-polynomial-time/). It is the usual source of NP-hardness for problems with two machines, two bins or two players. Its strongly NP-hard relative is [3-partition](/three-partition/).

## In plain words

Two children want to share a bag of sweets of different sizes, and each wants the same total amount. Can the sweets be split fairly?

If the total is odd, the answer is no at once. Otherwise you need a group of sweets that adds up to exactly half. This is the subset sum question, so the same methods apply. A list of all the amounts you can make so far works well when the sizes are small numbers. When the sizes are long numbers, no fast method is known. Simple rules, such as giving the largest remaining sweet to the child who has less, often get close to a fair split but can miss an exact one.

## Definition

**Instance.** Positive integers $a_1, \ldots, a_n$, written in binary. Let $A = \sum_{i=1}^n a_i$.

**Question.** Is there a set $S \subseteq \{1, \ldots, n\}$ with $\sum_{i \in S} a_i = \sum_{i \notin S} a_i$, that is, $\sum_{i \in S} a_i = A/2$?

**Encoding.** The input length $L$ is the total number of bits of the $a_i$. $A$ can be as large as $2^L$. The set $S$ is a certificate that a verifier checks in time polynomial in $L$, so the problem is in NP.

**Complexity.** The problem is NP-complete under Karp reductions. Karp (1972) reduced KNAPSACK, his form of subset sum, to it, and Garey and Johnson (Section 3.1) reduce [three-dimensional matching](/three-dimensional-matching/) to it. It has a pseudo-polynomial algorithm, so it is not [strongly NP-hard](/strong-np-hardness/) unless P = NP.

## Variants

- **Optimization version.** Minimize $\lvert \sum_{i \in S} a_i - \sum_{i \notin S} a_i \rvert$. This is the same as two-machine [makespan minimization](/makespan-minimization/) with job lengths $a_i$.
- **Search version.** Output $S$. The table of the dynamic program gives $S$ by a walk back from $A/2$.
- **More parts.** Split into $k$ parts with equal sums, for a fixed $k \ge 2$. The dynamic program generalizes and stays pseudo-polynomial for each fixed $k$.
- **Parts of size three.** In [3-partition](/three-partition/), the number of parts grows with $n$ and each part gets three numbers. This version is strongly NP-hard, so it has no pseudo-polynomial algorithm unless P = NP.

## Examples

**A yes-instance.** $a = (8, 7, 6, 5, 4)$ has total 30. The only equal split is $\{4, 5, 6\}$ and $\{7, 8\}$, each with sum 15.

**A no-instance.** $a = (1, 2, 7)$ has total 10. No subset sums to 5, because the subset sums are 0, 1, 2, 3, 7, 8, 9 and 10.

**More than one solution.** $a = (3, 1, 1, 2, 2, 1)$ has total 10 and two different splits: $\{1, 1, 1, 2\} \mid \{2, 3\}$ and $\{1, 1, 3\} \mid \{1, 2, 2\}$.

**Heuristics can miss.** On $(8, 7, 6, 5, 4)$, the greedy rule (take the numbers from the largest, and give each one to the part with the smaller sum) gives sums 17 and 13, a difference of 4. The differencing method of Karmarkar and Karp repeatedly replaces the two largest numbers by their difference: $(8, 7) \to 1$, $(6, 5) \to 1$, $(4, 1) \to 3$, $(3, 1) \to 2$. It ends with a difference of 2. The optimum difference is 0.

**The dynamic program.** For $(8, 7, 6, 5, 4)$ the table of reachable sums up to $A/2 = 15$ has $(n + 1)(A/2 + 1) = 6 \cdot 16 = 96$ cells.

## Known algorithms

- **Dynamic programming.** $O(nA)$ time on a [word RAM](/word-ram/), by the subset sum table up to $A/2$; see [knapsack dynamic programming](/knapsack-dynamic-programming/).
- **Near-linear pseudo-polynomial time (Bringmann 2017).** $\tilde O(n + A)$ randomized time, by the subset sum algorithm with $t = A/2$; see the [subset sum problem](/subset-sum-problem/).
- **Meet in the middle (Horowitz and Sahni 1974).** $O(2^{n/2} n)$ time, independent of the size of the numbers; see the [Horowitz-Sahni algorithm](/horowitz-sahni-algorithm/).
- **Approximation of the optimization version.** The two-machine makespan problem has an FPTAS, so a split within a factor $1 + \varepsilon$ of the best larger part takes time polynomial in $n$ and $1/\varepsilon$; see [FPTAS](/fptas/).

## Bounds

- **NP-completeness.** NP-complete under Karp reductions (Karp 1972). There is no polynomial-time algorithm unless P = NP.
- **Weak hardness.** The $O(nA)$ algorithm puts the problem in P when $A$ is bounded by a polynomial in $n$, and in P for [unary](/unary-encoding/) input. So hard instances need numbers with many bits.
- **No good absolute error.** Deciding whether the best difference is 0 is NP-complete, so no polynomial-time algorithm finds the optimum difference unless P = NP. For the same reason, [bin packing](/bin-packing-np-hardness/) has no polynomial-time approximation with ratio below $3/2$ unless P = NP.

## Reductions

- **From subset sum (Karp reduction).** For an instance $(a_1, \ldots, a_n; t)$ with $A = \sum_i a_i$ and $t \le A$, output $(a_1, \ldots, a_n, 2A - t, A + t)$. The new total is $4A$. The two new numbers sum to $3A$, which is more than $2A$, so each half contains exactly one of them. The half with $2A - t$ needs old numbers with sum $t$. If $t > A$, output a fixed no-instance such as $(1, 2)$. For example, $((2, 3, 7); 10)$ maps to $(2, 3, 7, 14, 22)$, with total 48 and the split $\{2, 22\} \mid \{3, 7, 14\}$. The no-instance $((2, 3, 7); 6)$ maps to $(2, 3, 7, 18, 18)$, which has no equal split.
- **To subset sum (Karp reduction).** If $A$ is odd, output a no-instance; otherwise ask for a subset with sum $A/2$.
- **To bin packing (Karp reduction).** The numbers fit into two bins of size $A/2$ if and only if the answer is yes. See [bin packing NP-hardness](/bin-packing-np-hardness/).
- **To two-machine scheduling (Karp reduction).** Jobs of lengths $a_i$ on two identical machines finish by time $A/2$ if and only if the answer is yes.
- **To scheduling with release times and deadlines (Karp reduction).** Garey and Johnson (Theorem 3.8) reduce partition to one-machine sequencing within intervals, with an extra job that must run at time $A/2$. See [scheduling with release times and deadlines](/scheduling-with-release-times-and-deadlines/).

## Applications

- **NP-hardness proofs.** Two-machine scheduling, two-bin packing, [knapsack](/knapsack-problem/) and many problems with two players or two resources are shown NP-hard by a reduction from partition.
- **Load balancing.** Split work between two equal processors or two workers so that both finish at the same time.
- **Fair division.** Split goods of given values between two people so that each gets half of the total value.

## References
