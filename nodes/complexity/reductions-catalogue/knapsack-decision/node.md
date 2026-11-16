---
tag: 9GWD0R
kind: problem
slug: knapsack-decision
name: 0-1 knapsack decision problem
aliases:
- knapsack feasibility
- 0-1 knapsack decision
area: complexity/reductions-catalogue
level: core
summary: Given items with weights and values, a capacity W and a target V, decide whether some items fit in W with total value at least V. NP-complete, but only weakly.
prereqs: [knapsack-problem, subset-sum-problem, np-complete]
see_also: [knapsack-dynamic-programming, knapsack-fptas, weak-np-hardness, pseudo-polynomial-time, partition-problem, horowitz-sahni-algorithm, zero-one-equations, karps-21-np-complete-problems]
sources:
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum Press, 1972, pages 85 to 103
    locator: Section 4, problem 18 (KNAPSACK, in the form sum of a_j x_j = b) and its reduction from EXACT COVER
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A6, problem MP9 (0-1 knapsack), and Section 4.2 (pseudo-polynomial algorithms and number problems)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 34.5.5 (the subset-sum problem)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms, McGraw-Hill, 2006
    locator: Section 8.3, the reduction from ZOE to SUBSET SUM, and Section 6.4 (knapsack by dynamic programming)
---

The 0-1 knapsack decision problem gives $n$ items, each with a weight and a value, a capacity $W$ and a target $V$, and asks whether some set of items has total weight at most $W$ and total value at least $V$. It is the decision form of the [knapsack problem](/knapsack-problem/). It is [NP-complete](/np-complete/), by a one-line reduction from the [subset sum problem](/subset-sum-problem/), and it was on Karp's 1972 list in the subset sum form. But it is only [weakly NP-hard](/weak-np-hardness/): [dynamic programming](/knapsack-dynamic-programming/) solves it in time polynomial in $n$ and $W$, which is [pseudo-polynomial](/pseudo-polynomial-time/), and the optimization form has an [FPTAS](/knapsack-fptas/).

## In plain words

A hiker has a bag that can carry a limited weight and a pile of things, each with a weight and a usefulness. The question is whether the hiker can pack things that fit and are useful enough in total.

Checking a proposed packing is easy. Finding one is hard in the worst case, because the question can express a pure number puzzle: if each thing is as useful as it is heavy, the hiker must find things whose weights add up exactly to the limit.

The difficulty depends on the size of the numbers. When the weights are small numbers, a table of all reachable weights answers quickly. Hard instances need very large numbers.

## Definition

**Instance.** Positive integers $w_1, \ldots, w_n$ (weights) and $v_1, \ldots, v_n$ (values), a capacity $W$ and a target $V$.

**Question.** Is there a set $S \subseteq \{1, \ldots, n\}$ with $\sum_{i \in S} w_i \le W$ and $\sum_{i \in S} v_i \ge V$?

**Encoding.** All numbers are written in binary, so the input length is about $\sum_i (\log w_i + \log v_i) + \log W + \log V$. The certificate is the set $S$, and the verifier adds two sums of at most $n$ numbers and compares them, in polynomial time on the [multitape Turing machine](/multitape-turing-machine/). So the problem is in NP.

**Complexity.** NP-complete under Karp (polynomial-time many-one) reductions, from subset sum (Garey and Johnson problem MP9). It is NP-complete only in the weak sense: with unary numbers, it is in P.

## Variants

- **Optimization.** Find the largest value with weight at most $W$; see [knapsack problem](/knapsack-problem/). Binary search on $V$ reduces it to the decision form with $O(\log \sum_i v_i)$ calls.
- **Subset sum.** The case $v_i = w_i$ and $V = W$: is there a set with weight exactly $W$? This is Karp's KNAPSACK, $\sum_j a_j x_j = b$ with $x_j \in \{0, 1\}$. See [subset sum problem](/subset-sum-problem/).
- **Partition.** Subset sum with $W$ equal to half the total weight; see [partition problem](/partition-problem/).
- **Unbounded knapsack.** Each item may be taken any number of times. It is also NP-complete and also has a pseudo-polynomial algorithm.
- **Several constraints.** With two or more weight constraints (the multidimensional knapsack), the problem becomes strongly NP-hard when the number of constraints is part of the input; see [zero-one equations](/zero-one-equations/) for the case of many equality constraints.

## Examples

**A small instance.** Take the items $(w, v) = (2, 3), (3, 4), (4, 5), (5, 6)$ and $W = 5$.

- With $V = 7$ the answer is yes: items 1 and 2 have weight $5$ and value $7$.
- With $V = 8$ the answer is no. A script checked all 16 sets; the best value within weight 5 is 7.
- The dynamic program over capacities $c = 0, 1, \ldots, 5$ gives the best values $0, 0, 3, 4, 5, 7$, so the last entry, 7, answers both questions.

**The reduction from subset sum.** Take the numbers $3, 5, 8, 9$ and the target $t = 14$. The only subset with sum 14 is $\{5, 9\}$. The reduction makes four items with $w_i = v_i$ equal to the numbers and $W = V = 14$. The script listed the sets that meet both bounds, and the only one is again $\{5, 9\}$: forward, the subset is a packing of weight $14 \le W$ and value $14 \ge V$; backward, the packing has weight at most 14 and value at least 14, and these are the same sum, so it is exactly 14. On 500 random instances with up to 7 numbers, the two answers agreed (179 yes-instances and 321 no-instances).

## Known algorithms

- **Dynamic programming by weight.** $O(nW)$ time, which is pseudo-polynomial; see [knapsack dynamic programming](/knapsack-dynamic-programming/). A second table indexed by value gives $O(nV)$.
- **Meet in the middle.** The [Horowitz-Sahni algorithm](/horowitz-sahni-algorithm/) runs in $O(2^{n/2} n)$ time, and the [Schroeppel-Shamir algorithm](/schroeppel-shamir-algorithm/) uses less space.
- **Approximation.** For the optimization form, the [knapsack FPTAS](/knapsack-fptas/) finds a set of value at least $(1 - \varepsilon)$ times the optimum in time polynomial in $n$ and $1/\varepsilon$.
- **Branch and bound.** Practical solvers use bounds from the fractional knapsack, which greedy by value per weight solves exactly.

## Bounds

- **NP-completeness.** No algorithm runs in time polynomial in $n$ and $\log W$ unless P = NP.
- **Weak hardness.** Since the $O(nW)$ algorithm exists, the problem is not strongly NP-complete unless P = NP. So hard instances need both $W$ and $V$ to be larger than every polynomial in $n$.
- **Exponential time.** No algorithm for subset sum with time $O(2^{(1/2 - \varepsilon) n})$ for a constant $\varepsilon > 0$ is known; meet in the middle is still the best general bound.

## Reductions

**From subset sum (Karp reduction).** An instance of subset sum is a list $a_1, \ldots, a_n$ of positive integers and a target $t$.

- *Map.* Make one item per number with $w_i = v_i = a_i$, and set $W = V = t$.
- *Cost.* The map copies the numbers, in linear time.
- *If some subset sums to $t$, then the knapsack instance is a yes-instance.* Take that subset $S$. Its weight is $t \le W$ and its value is $t \ge V$.
- *If the knapsack instance is a yes-instance, then some subset sums to $t$.* Take any set $S$ with weight at most $W$ and value at least $V$. Both are the same number $\sum_{i \in S} a_i$, so $t \le \sum_{i \in S} a_i \le t$, and $S$ sums to $t$.

Subset sum itself is NP-complete by Karp's reduction from exact cover (see [Karp's reduction tree](/karp-21-np-complete/)), by the reduction from vertex cover in Cormen, Leiserson, Rivest and Stein, or by the chain through [zero-one equations](/zero-one-equations/) in Dasgupta, Papadimitriou and Vazirani. All these reductions make numbers with a number of digits that grows with the input, which is why the hardness is only weak.

**To scheduling.** Karp reduced KNAPSACK to SEQUENCING with deadlines and penalties, and to PARTITION; both reductions are on [Karp's reduction tree](/karp-21-np-complete/).

## Applications

- **Hardness of resource allocation.** Budgeted selection, cargo loading and capital budgeting contain knapsack, so their exact versions are NP-hard.
- **A source of weak hardness.** Reductions from knapsack or subset sum show weak NP-hardness of scheduling problems with two machines or one machine with weights.
- **Cryptography.** Early public-key schemes, such as the Merkle-Hellman knapsack system, were based on subset sum. They were broken with lattice reduction such as the [LLL algorithm](/lll-algorithm/), which shows that NP-hardness in the worst case does not give hardness on the instances a scheme uses.

## References
