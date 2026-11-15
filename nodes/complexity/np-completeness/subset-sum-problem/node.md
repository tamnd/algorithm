---
tag: PFB9XG
kind: problem
slug: subset-sum-problem
name: Subset sum problem
aliases:
- SSP
- SUBSET-SUM
- subset sum
area: complexity/np-completeness
level: intro
summary: Given positive integers and a target, decide whether some subset sums to the target. NP-complete, but solvable in pseudo-polynomial time.
prereqs: [decision-problem, np-complete, pseudo-polynomial-time]
see_also: [partition-problem, knapsack-problem, subset-sum-fptas, horowitz-sahni-algorithm, counting-subset-sum, weak-np-hardness, k-sum, three-partition]
sources:
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum Press, 1972, pages 85 to 103
    locator: Section 4, the problem KNAPSACK (in Karp's form it is subset sum) and its reduction from EXACT COVER
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 34.5.5, The subset-sum problem (the reduction from 3-CNF-SAT)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 4.2 (pseudo-polynomial algorithms and number problems) and the appendix, problem SP13 (SUBSET SUM)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 8.8, Numerical Problems
  - paper: Richard Bellman, Dynamic Programming, Princeton University Press, 1957
    title: Bellman, the dynamic program over reachable sums
    locator: the knapsack recursion
  - paper: doi:10.1145/321812.321823
    title: Ellis Horowitz and Sartaj Sahni, Computing partitions with applications to the knapsack problem, Journal of the ACM 21(2), 1974
    locator: the main algorithm (two halves of the input)
  - paper: doi:10.1137/0210033
    title: Richard Schroeppel and Adi Shamir, A T = O(2^(n/2)), S = O(2^(n/4)) algorithm for certain NP-complete problems, SIAM Journal on Computing 10(3), 1981
    locator: the main theorem
  - paper: David Pisinger, Linear time algorithms for knapsack problems with bounded weights, Journal of Algorithms 33(1), 1999
    title: Pisinger, subset sum in O(n max a_i) time
    locator: the subset sum algorithm
  - paper: Konstantinos Koiliaris and Chao Xu, A faster pseudopolynomial time algorithm for subset sum, SODA 2017, pages 1062 to 1072
    title: Koiliaris and Xu, deterministic subset sum in O~(sqrt(n) t) time
    locator: the main theorem
  - paper: doi:10.1137/1.9781611974782.69
    title: Karl Bringmann, A near-linear pseudopolynomial time algorithm for subset sum, SODA 2017, pages 1073 to 1084
    locator: the main theorem (randomized O~(n + t) time)
  - paper: doi:10.1145/3450524
    title: Amir Abboud, Karl Bringmann, Danny Hermelin and Dvir Shabtay, SETH-based lower bounds for subset sum and bicriteria path, ACM Transactions on Algorithms 18(1), article 6, 2022 (conference version SODA 2019)
    locator: the main theorem (no t^(1-e) 2^(o(n)) algorithm under SETH)
---

The subset sum problem asks whether some of the given positive integers add up exactly to a given target. It is one of the basic [NP-complete](/np-complete/) number problems: Karp proved it NP-complete in 1972, under the name KNAPSACK. It is also the standard example of a problem that is only weakly hard. A dynamic program decides it in $O(nt)$ time for $n$ numbers and target $t$. This is [pseudo-polynomial time](/pseudo-polynomial-time/), not polynomial time, because the input writes $t$ in binary with only about $\log_2 t$ bits. So the problem is NP-complete and still easy when the numbers are small. The [partition problem](/partition-problem/) is its special case with $t$ equal to half the total.

## In plain words

You have a pile of coins of different values and a price to pay. Can you pay the price exactly with some of the coins, without change?

With a few coins you can try every choice. With 40 coins there are about a million million choices, so this is too slow. A better method keeps a list of all the amounts you can make so far and adds one coin at a time. This is fast when the price is small, because the list never holds more than the price plus one amount. But a price with 40 binary digits is a short number to write down and a huge list to keep. No method is known that is fast in the length of the numbers, and most experts think that none exists.

## Definition

**Instance.** Positive integers $a_1, \ldots, a_n$ and a target $t$, all written in binary.

**Question.** Is there a set $S \subseteq \{1, \ldots, n\}$ with $\sum_{i \in S} a_i = t$?

**Encoding.** The input length is $L = \Theta\big(\sum_i \log_2 (a_i + 1) + \log_2 (t + 1)\big)$ bits. The value of $t$ can be as large as $2^L$. The certificate is the set $S$, and a verifier adds the chosen numbers in time polynomial in $L$, so the problem is in NP.

**Complexity.** The problem is NP-complete under Karp reductions (polynomial-time many-one reductions). Karp (1972) reduced exact cover to it. CLRS give a reduction from [3-SAT](/3-sat/), shown under Reductions. The problem is not [strongly NP-hard](/strong-np-hardness/) unless P = NP, because it has a pseudo-polynomial algorithm. So it is [weakly NP-hard](/weak-np-hardness/).

## Variants

- **Search version.** Output a set $S$, or report that none exists. With the table of the dynamic program, walk back from $t$ to recover $S$ in $O(n)$ extra steps.
- **Optimization version.** Find the largest subset sum that is at most $t$. It has an FPTAS; see [subset sum FPTAS](/subset-sum-fptas/).
- **Partition.** Take $t = \frac{1}{2}\sum_i a_i$. See the [partition problem](/partition-problem/).
- **Knapsack.** Give each item a weight and a value. Subset sum is the case where value equals weight; see the [knapsack problem](/knapsack-problem/) and [knapsack decision](/knapsack-decision/).
- **Integers of both signs.** Ask whether a nonempty subset sums to zero. This is equivalent to the positive form under polynomial-time reductions.
- **Fixed subset size.** Ask for exactly $k$ numbers with the given sum. For fixed $k$ this is the [k-sum](/k-sum/) problem, which is in P; [3SUM](/3sum/) is the case $k = 3$.
- **Counting.** Count the subsets with sum $t$; see [counting subset sum](/counting-subset-sum/).
- **Unary input.** If the numbers are written in [unary](/unary-encoding/), the dynamic program runs in polynomial time in the input length, so the problem is in P.

## Examples

**A yes-instance and some no-instances.** Take $a = (3, 34, 4, 12, 5, 2)$, with total 60. For $t = 9$ the answer is yes, with two solutions: $4 + 5$ and $3 + 4 + 2$. For $t = 13$, $t = 30$ and $t = 59$ the answer is no. Of the $2^6 = 64$ subsets, the sums take 48 distinct values.

**The dynamic program.** Keep the set $R$ of reachable sums. For $a = (2, 3, 7)$ and $t = 10$:

| after the number | reachable sums $R$ |
|---|---|
| (start) | 0 |
| 2 | 0, 2 |
| 3 | 0, 2, 3, 5 |
| 7 | 0, 2, 3, 5, 7, 9, 10, 12 |

The value 10 is in the last row, so the answer is yes ($3 + 7$).

**Why $O(nt)$ is not polynomial.** Take $n = 40$ numbers of 40 bits each, with a 40-bit target. The input is about 1640 bits long. The dynamic program table has $(n + 1) \cdot 2^{40} = 45{,}079{,}976{,}738{,}816$ cells. The meet-in-the-middle method of Horowitz and Sahni lists only $2^{20} = 1{,}048{,}576$ sums for each half of the input, so on this input it is much faster.

## Known algorithms

- **Dynamic programming (Bellman 1957).** $O(nt)$ time on a [word RAM](/word-ram/), or $O(nt / w)$ with bit-parallel shifts of $w$-bit words; see [knapsack dynamic programming](/knapsack-dynamic-programming/).
- **Bounded numbers (Pisinger 1999).** $O(n \cdot \max_i a_i)$ time on a word RAM, which is better than $O(nt)$ when $t$ is much larger than every $a_i$.
- **Deterministic, near $\sqrt{n}\,t$ (Koiliaris and Xu 2017).** $\tilde O(\sqrt{n}\, t)$ time.
- **Randomized, near-linear in $n + t$ (Bringmann 2017).** $\tilde O(n + t)$ time with one-sided error.
- **Meet in the middle (Horowitz and Sahni 1974).** $O(2^{n/2} n)$ time and $O(2^{n/2})$ space, independent of the size of the numbers; see the [Horowitz-Sahni algorithm](/horowitz-sahni-algorithm/).
- **Less space (Schroeppel and Shamir 1981).** $O(2^{n/2})$ time and $O(2^{n/4})$ space; see the [Schroeppel-Shamir algorithm](/schroeppel-shamir-algorithm/).
- **Random instances.** The [Howgrave-Graham and Joux algorithm](/howgrave-graham-joux-algorithm/) and its successors run faster than $2^{n/2}$ on random instances with $t$ and the $a_i$ near $2^n$, under heuristic assumptions. Lattice reduction ([LLL](/lll-algorithm/)) solves many instances whose numbers are much larger than $2^n$.

## Bounds

- **NP-completeness.** NP-complete under Karp reductions (Karp 1972). So there is no polynomial-time algorithm unless P = NP.
- **Conditional on SETH.** For each $\varepsilon > 0$ there is no algorithm in time $t^{1-\varepsilon} 2^{o(n)}$ unless the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) fails (Abboud, Bringmann, Hermelin and Shabtay 2019). So Bringmann's $\tilde O(n + t)$ bound cannot be improved to $t^{1-\varepsilon}$ times a small factor in $n$.
- **Conditional on ETH.** The reduction from 3-SAT below makes a number of integers that is linear in the size of the formula. With the sparsification lemma, it follows that there is no $2^{o(n)}$-time algorithm unless ETH fails. ETH is stated on the page of the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/).
- **Weak hardness.** The $O(nt)$ algorithm shows that the problem is in P when $t$ is bounded by a polynomial in $n$. All NP-hard instances therefore need numbers with many bits.
- **Approximation.** The optimization version has an FPTAS ([subset sum FPTAS](/subset-sum-fptas/)). This does not contradict NP-hardness, because the FPTAS gives an approximate sum, not an exact one.

## Reductions

- **From 3-SAT (Karp reduction, CLRS Section 34.5.5).** Let the formula have variables $x_1, \ldots, x_v$ and clauses $C_1, \ldots, C_c$. Write numbers in base 10 with $v + c$ digits: one digit for each variable, then one for each clause. For each variable $x_i$ make two numbers $v_i$ and $v_i'$. Each has a 1 in the digit of $x_i$. $v_i$ has a 1 in the digit of each clause that contains $x_i$, and $v_i'$ has a 1 in the digit of each clause that contains $\neg x_i$. For each clause make two slack numbers, with 1 and 2 in its digit. The target has 1 in each variable digit and 4 in each clause digit. A clause digit can sum to at most $3 + 1 + 2 = 6$, so no carries occur. The variable digits force one of $v_i, v_i'$ for each $i$, which is a truth assignment. A clause digit reaches 4 only if the clause has 1, 2 or 3 true literals, and then exactly one choice of slack numbers (3 as $1 + 2$, 2, or 1) completes it. So each satisfying assignment gives exactly one subset, and the reduction is parsimonious. The output has $2v + 2c$ numbers of $v + c$ digits, so it takes polynomial time.
**Example of the 3-SAT reduction.** For $\varphi = (x_1 \lor \neg x_2 \lor x_3) \land (\neg x_1 \lor x_2 \lor x_3)$ the digits are $x_1, x_2, x_3, C_1, C_2$:

| number | digits | number | digits |
|---|---|---|---|
| $v_1$ | 10010 | $v_1'$ | 10001 |
| $v_2$ | 01001 | $v_2'$ | 01010 |
| $v_3$ | 00111 | $v_3'$ | 00100 |
| $s_1$ | 00010 | $s_1'$ | 00020 |
| $s_2$ | 00001 | $s_2'$ | 00002 |

The target is 11144. The assignment $x_1 = 1, x_2 = 1, x_3 = 0$ selects $v_1, v_2, v_3', s_1, s_1', s_2, s_2'$, with sum 11144. The formula has 6 satisfying assignments, and exactly 6 subsets sum to 11144.

- **From exact cover (Karp reduction).** Give each element of the universe a digit in base $m + 1$, where $m$ is the number of sets. Each set becomes the number with a 1 in the digits of its elements, and the target has a 1 in every digit. The base is large enough that no carries occur. The same map works for [exact cover by 3-sets](/exact-cover-by-3-sets/).
- **To partition (Karp reduction).** Let $A = \sum_i a_i$. If $t \le A$, add the two numbers $2A - t$ and $A + t$. The new total is $4A$, and a half of it, $2A$, contains exactly one of the two new numbers, so it is $2A - t$ plus a subset with sum $t$ of the old numbers. If $t > A$, output a fixed no-instance. See the [partition problem](/partition-problem/).
- **To knapsack and to scheduling.** Subset sum is the special case of [knapsack decision](/knapsack-decision/) with value equal to weight. Kleinberg and Tardos (Section 8.8) reduce it to [scheduling with release times and deadlines](/scheduling-with-release-times-and-deadlines/).

## Applications

- **Weak NP-hardness proofs.** Subset sum and partition are the usual starting points for proofs that a number problem is NP-hard, for example in scheduling and [bin packing](/bin-packing-np-hardness/).
- **Cryptography.** The [Merkle-Hellman knapsack cryptosystem](/merkle-hellman-knapsack-cryptosystem/) used a hidden easy instance as a trapdoor. Lattice attacks broke it, which shows that worst-case hardness does not give hardness of the instances a system produces.
- **Making change and budgets.** Paying an exact amount with given coins ([coin change](/coin-change-problem/)) and filling a budget or a container exactly with given items are subset sum questions. In practice the amounts are small, and the dynamic program is fast.
- **Fine-grained complexity.** Subset sum with small $t$ is a test case for [conditional lower bounds](/conditional-lower-bound/) based on SETH.

## References
