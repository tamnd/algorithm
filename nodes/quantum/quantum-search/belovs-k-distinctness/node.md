---
tag: KK9NWR
kind: algorithm
slug: belovs-k-distinctness
name: Belovs k-distinctness algorithm
aliases:
- Belovs quantum k-distinctness
area: quantum/quantum-search
level: research
summary: A learning-graph algorithm for k-distinctness with O(N^(1 - 2^(k-2)/(2^k - 1))) queries and bounded error. It beats Ambainis's O(N^(k/(k+1))) for k of 3 or more and is optimal.
solves: [k-distinctness]
model: quantum-query-model
complexity:
  vars: {N: the number of input values, k: the number of equal values to find, M: the size of the value alphabet}
  queries: {worst: O(N^(1 - 2^(k-2)/(2^k - 1)))}
properties: {deterministic: false, exact: false, oracle: bit}
history:
  year: 2012
  people: [Aleksandrs Belovs]
  note: First posted as arXiv:1205.1534 in May 2012 and presented at FOCS 2012. A matching lower bound followed in a 2026 preprint by the same author.
prereqs: [k-distinctness, ambainis-element-distinctness, quantum-adversary-method, quantum-query-complexity]
see_also: [quantum-query-model, semidefinite-programming, polynomial-method, quantum-walk-search, element-distinctness, triangle-finding, brassard-hoyer-tapp-collision, quantum-random-access-memory]
sources:
  - paper: doi:10.1109/FOCS.2012.18
    title: "Aleksandrs Belovs, Learning-graph-based quantum algorithm for k-distinctness, Proceedings of the 53rd IEEE FOCS, 2012, pages 207-216"
    locator: with the numbering of arXiv:1205.1534, Definition 1 and Theorem 2 (the dual adversary bound), Definitions 3 and 4 (learning graphs and flows), Tables 1 and 2, Theorem 7 (graph collision), Theorem 8 and Sections 5 and 6 (the construction, its cost (12), the flaw of Section 5.3 and the fault-tolerant version with Lemma 9), Footnote 8
  - paper: doi:10.1145/2213977.2213985
    title: "Aleksandrs Belovs, Span programs for functions with constant-sized 1-certificates, Proceedings of the 44th ACM STOC, 2012, pages 77-84"
    locator: the whole paper (the first learning graphs, and triangle finding with O(n^(35/27)) queries)
  - paper: doi:10.1137/1.9781611973082.44
    title: "Ben W. Reichardt, Reflections for quantum query algorithms, Proceedings of the 22nd ACM-SIAM SODA, 2011, pages 560-569"
    locator: the main theorem (the dual adversary bound is the bounded-error query complexity of a function up to a constant factor)
  - paper: doi:10.1109/FOCS.2011.75
    title: "Troy Lee, Rajat Mittal, Ben W. Reichardt, Robert Špalek and Mario Szegedy, Quantum query complexity of state conversion, Proceedings of the 52nd IEEE FOCS, 2011, pages 344-353"
    locator: the main theorem (the same result for partial functions, with a simpler algorithm)
  - paper: doi:10.1137/S0097539705447311
    title: "Andris Ambainis, Quantum walk algorithm for element distinctness, SIAM Journal on Computing 37(1), 2007, pages 210-239"
    locator: with the numbering of arXiv:quant-ph/0311001, Theorem 3 (O(N^(k/(k+1))) queries), the algorithm that Table 1 of Belovs's paper expresses as a learning graph
  - paper: doi:10.1007/978-3-642-39206-1_10
    title: "Aleksandrs Belovs, Andrew M. Childs, Stacey Jeffery, Robin Kothari and Frédéric Magniez, Time-efficient quantum walks for 3-distinctness, Proceedings of ICALP 2013, LNCS 7965, pages 105-122"
    locator: the main result (3-distinctness in time close to the query bound O(N^(5/7)))
  - paper: doi:10.1145/3564246.3585158
    title: "Stacey Jeffery and Sebastian Zur, Multidimensional quantum walks, Proceedings of the 55th ACM STOC, 2023, pages 1125-1130"
    locator: the application to k-distinctness (time close to Belovs's query bound for every constant k)
  - paper: arxiv:2604.05133
    title: "Aleksandrs Belovs, Tight quantum lower bound for k-distinctness, arXiv:2604.05133, version 2, 2026"
    locator: Theorem 1.1 (the matching lower bound, for k = O(1) and an alphabet of size Omega(N^2)); a preprint
---

Belovs's algorithm solves [k-distinctness](/k-distinctness/): given $N$ values through a [quantum oracle](/quantum-oracle/), decide whether $k$ of them are equal. It uses $O(N^{1 - 2^{k-2}/(2^k - 1)})$ queries in the [quantum query model](/quantum-query-model/), with bounded error, for every constant $k$. For $k = 2$ this is $N^{2/3}$, the bound of [Ambainis](/ambainis-element-distinctness/); for $k = 3$ it is $N^{5/7}$ in place of $N^{3/4}$, and for $k = 4$ it is $N^{11/15}$ in place of $N^{4/5}$. A 2026 preprint by Belovs proves a matching lower bound, so for alphabets of size $\Omega(N^2)$ the exponent is the [quantum query complexity](/quantum-query-complexity/) of the problem. This page is the algorithm; the problem and all its bounds are on [k-distinctness](/k-distinctness/). The algorithm is not a circuit that one writes down step by step: it is a feasible solution of the dual [adversary bound](/quantum-adversary-method/), a [semidefinite program](/semidefinite-programming/), built from a *learning graph*, and a general theorem turns this solution into a query algorithm. It bounds queries only, not time.

## In plain words

Ambainis's method keeps one bag of positions and waits until the bag holds all the equal values. For three or more equal values, Belovs found a better plan with a row of bags. The first bag shows all its values. The second bag shows a value only if the same value is in the first bag, and it hides the others. Each later bag shows only the values that match a shown value of the bag before it. The equal values go into the bags one at a time, one value per bag. Because most values stay hidden, a bag can be large and still cost little. The plan is not a program that runs step by step. It is a solution of a large system of matrix conditions, and a general theorem turns any such solution into a quantum program that asks a matching number of questions.

## The problem

The input is $x = (x_1, \ldots, x_N)$ with $x_i \in [M]$, given by the bit oracle $O_x|i\rangle|b\rangle = |i\rangle|b \oplus x_i\rangle$ on a register of $\lceil \lg M \rceil$ bits. The phase form is equivalent, with one query, by [phase kickback](/phase-kickback/). The output is "yes" if there are $k$ distinct indices with equal values, a *$k$-collision*, and "no" otherwise. The cost is the number of oracle calls, with bounded error: the answer is correct with probability at least $2/3$ on every input. The construction below assumes that a positive input has exactly one $k$-collision $\{a_1, \ldots, a_k\}$, with $a_1 < \cdots < a_k$; Variants explains how to remove this promise.

**The dual adversary bound.** For a function $f$, find positive semidefinite matrices $X_1, \ldots, X_N$, indexed by the inputs, with
$$\sum_{j:\, x_j \ne y_j} X_j[x, y] = 1 \quad \text{whenever } f(x) \ne f(y),$$
and make the objective $\max_z \sum_j X_j[z, z]$ small. By Theorem 2 of Belovs's paper, from Reichardt (SODA 2011) and Lee, Mittal, Reichardt, Špalek and Szegedy (FOCS 2011), the optimal value is the bounded-error quantum query complexity of $f$ up to a constant factor, and every feasible solution gives an algorithm with that many queries.

**Learning graphs.** A learning graph builds such a solution from a flow. Its vertices are sets of indices that the algorithm "knows", and an arc loads one more index $j$. For a positive input $x$ one sends a unit flow from the empty set to sets that contain a certificate of $x$, here the $k$-collision. Each arc has a weight $w$, and it adds to $X_j$ a block with the entries $q/w$, $q$ and $qw$ for the pairs (positive, positive), (positive, negative) and (negative, negative) inputs that agree on the loaded set, where $q$ is the flow on the arc. The block is a rank-one matrix $q\psi\psi^*$, so it is positive semidefinite. Belovs's new idea is a set with *covered* elements: the vertex stores only part of the information about some of its values.

## The algorithm

Let $r_1, \ldots, r_{k-1}$ be the sizes of $k - 1$ disjoint sets $S_1, \ldots, S_{k-1}$, and let the internal randomness be a choice of these sets with no element of the $k$-collision. An element of $S_1$ always shows its value. For $s > 1$, an element of $S_s$ shows its value only if this value is among the shown values of $S_{s-1}$; otherwise it is *covered* and shows only $\star$.

```pseudo id=main
BELOVS-K-DISTINCTNESS(O_x, N, k)   ▷ promise: at most one k-collision
L1  ρ_1 ← 1 - 2^(k-2) / (2^k - 1)
L2  for s = 2 to k - 1: ρ_s ← (1 + ρ_(s-1)) / 2
L3  r_s ← N^(ρ_s) for s = 1, ..., k - 1
L4  stages I.1 to I.(k-1): load disjoint sets S_1, ..., S_(k-1) with |S_s| = r_s; for s > 1 an element of S_s is uncovered only if its value is a shown value of S_(s-1)
L5  stages II.1 to II.k: add a_s to S_s for s < k, then load a_k
L6  arc weights: 1 on stage I.1; w_0 = (N^(s-1) / (r_1 ... r_(s-1)))^(1/2) and w_1 = 1 / w_0 on stage I.s; (N^s / (r_1 ... r_(s-1)))^(-1/2) on stage II.s
L7  X_j ← the sum of the blocks of all arcs that load j
L8  run the algorithm of Theorem 2 for the feasible solution X_1, ..., X_N   ▷ O(objective) queries
L9  return its answer: "yes" if x has a k-collision
```

On stage I.s with $s > 1$ the weight depends on the loaded value: $w_0$ is used when the new element stays covered and $w_1$ when it is uncovered (blocks (11) of the paper). For $k = 2$ there are no covered elements, and the learning graph is Table 1 of the paper, which is Ambainis's algorithm with $r = r_1$.

## Example

Take $k = 3$, $N = 11$ and $x = (3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5)$, indexed from 0, with the 3-collision $\{4, 8, 10\}$ of the value 5. Let the randomness be $S_1 = \{0, 1, 2\}$ and $S_2 = \{3, 5, 9\}$.

1. Stage I.1 loads $S_1$. All its values show: $3, 1, 4$.
2. Stage I.2 loads $S_2$. Index 3 has the value 1, which shows in $S_1$, so it shows. Index 5 has the value 9, which does not, so it is covered. Index 9 has the value 3, which shows in $S_1$. The shown values of $S_2$ are $1, 3$; two of its three elements are uncovered.
3. Stage II.1 adds $a_1 = 4$ (value 5) to $S_1$. Stage II.2 adds $a_2 = 8$ to $S_2$; its value 5 now shows in $S_1$, so it shows. Stage II.3 loads $a_3 = 10$.

The final vertex shows the value 5 three times, which is a certificate. The vertex never needs to store the value 9 of index 5, and on long inputs most elements of $S_2$ are covered in this way, which makes $S_2$ cheap.

With $r_s = N^{\rho_s}$, every term of the cost (12) of the paper is exactly $N^{\rho_1}$:

| $k$ | $\rho_1, \ldots, \rho_{k-1}$ | Belovs exponent | Ambainis exponent $k/(k+1)$ |
|---|---|---|---|
| 2 | $2/3$ | $2/3$ | $2/3$ |
| 3 | $5/7, 6/7$ | $5/7 \approx 0.714$ | $0.75$ |
| 4 | $11/15, 13/15, 14/15$ | $11/15 \approx 0.733$ | $0.8$ |
| 5 | $23/31, 27/31, 29/31, 30/31$ | $23/31 \approx 0.742$ | $0.833$ |

The Belovs exponent tends to $3/4$, while Ambainis's tends to 1. At $N = 2^{40}$ and $k = 3$, the objective (12) is $3N^{5/7} \approx 1.20 \cdot 10^9$ against $N^{3/4} + N^{3/4} \approx 2.15 \cdot 10^9$ for Table 1; constant factors are not part of either number.

The Python file does not simulate the quantum algorithm, because Theorem 2 gives it only through the dual solution. The tests cover the classical parts. They check the exponents for $k$ from 2 to 11 in exact fractions: every term of (12) has the exponent $\rho_1$, $\rho_1 = 3/4 - 1/(4(2^k - 1))$, and $\rho_1 < k/(k+1)$ for $k \ge 3$. They check that the weights of L6 make the positive and the negative cost of each stage equal. With seed 2026, they run the loading of L4 and L5 on 300 random inputs and compare each covered or uncovered mark with a direct definition (an element of $S_s$ shows its value if and only if the value occurs in each of $S_1, \ldots, S_{s-1}$); the final vertex always holds the $k$-collision. For $k = 2$ they build the matrices $X_j$ of the learning graph on all 24 negative and 144 positive inputs with $N = M = 4$ and $r = 1, 2$, and check the constraint of the dual adversary bound exactly on all 3456 pairs, and on 300 sampled pairs for $N = M = 6$ (seed 11); the objective is $7 = r + \sqrt{N} + N/\sqrt{r}$ for $N = 4$, $r = 1$. Last, they check that the closed-form objective for $k = 2$ is minimized near $r = (N/2)^{2/3}$ with a value between $1.85N^{2/3}$ and $2.35N^{2/3}$ for $N = 10^3, 10^4, 10^5$.

## Correctness

Two things must hold. First, the matrices must be feasible: the sum $\sum_{j: x_j \ne y_j} X_j[x, y]$ must be 1 for every positive $x$ and negative $y$. Second, the objective must be $O(N^{\rho_1})$. Then Theorem 2 gives a bounded-error algorithm with $O(N^{\rho_1})$ queries.

For $k = 2$, feasibility follows from the flow. Fix the randomness $R$. Along the path that loads $R$ and then $a_1, a_2$, the inputs $x$ and $y$ agree on the empty set but not on the last set, since $y$ has no equal pair. So exactly one arc on the path is the first one where they stop agreeing, and it loads some $j$ with $x_j \ne y_j$. That arc gives $q$, the others give 0, and the $\binom{N-2}{r}$ paths with flow $q = 1/\binom{N-2}{r}$ give 1 in total. The proof page gives the details.

For $k \ge 3$, the learning graph of Table 2 is *not* feasible, as Section 5.3 of the paper shows. A *fault* is an element $b \in S_i$, $i > 1$, with $y_b = x_{a_1}$: it is covered on $y$ until $a_1$ is loaded, and then it suddenly shows its value. So $y$ can agree with $x$ on the whole first part of a path and then disagree on an arc that loads an element where $x$ and $y$ are equal, which gives a sum of 0. A negative input has at most $k - 1$ such faults. Section 6 splits each $S_i$ into parts labeled by subsets and uses inclusion and exclusion to make the sum exactly 1 for any set of at most $k - 1$ faults (Lemma 9). The split changes the cost only by a factor that depends on $k$.

The objective of the learning graph is (12): $O(r_1 + r_2\sqrt{r_1/N} + \cdots + r_{k-1}\sqrt{r_1 \cdots r_{k-2}/N^{k-2}} + \sqrt{N^k/(r_1 \cdots r_{k-1})})$. The recursion of L2 makes the first $k - 1$ terms equal, and the value of $\rho_1$ in L1 makes the last one equal to them, so the sum is $O(N^{\rho_1})$; the proof page shows the computation.

## Complexity

- **Queries:** $O(N^{1 - 2^{k-2}/(2^k - 1)}) = O(N^{3/4 - 1/(4(2^k - 1))})$ with bounded error, for constant $k$. The constant factor grows quickly with $k$, because the fault-tolerant construction splits each set into many parts.
- **Time:** not given. Theorem 2 turns a dual solution into an algorithm whose gates other than queries can be very costly. A query bound is not a time bound. Time-efficient versions need new ideas and a [quantum random access memory](/quantum-random-access-memory/); see Variants.
- **Space:** not given by the construction.

## Properties

- **Query model:** bit oracle, or phase oracle by phase kickback.
- **Error:** bounded error, not exact and not zero-error. The paper does not claim one-sided error.
- **Optimal:** for constant $k$ and an alphabet of size $\Omega(N^2)$, by Theorem 1.1 of Belovs's 2026 preprint.
- **Nonconstructive in time:** the algorithm exists through the dual adversary bound; the paper gives the dual solution, not a circuit.

## Variants and improvements

- **Removing the promise.** Run the algorithm on random subsets $T_i$ of sizes $(2k/(2k+1))^i N$. If $x$ has a $k$-collision, some $T_i$ holds exactly one with probability at least $1/2$, and the costs form a geometric series. Footnote 8 of the paper notes that $O(N)$ pairs of equal values are enough for the analysis.
- **Ambainis's algorithm as a learning graph.** Table 1 loads one set of size $r$ and then the $k$-collision, with cost $O(r + \sqrt{N^k/r^{k-1}})$, which gives $O(N^{k/(k+1)})$. It is time-efficient, which Belovs's algorithm is not known to be.
- **Graph collision.** With the same ideas, Theorem 7 solves graph collision on a graph $G$ with $O(\sqrt{n}\,\alpha(G)^{1/6})$ queries, where $\alpha(G)$ is the independence number. Graph collision is a subroutine of [triangle finding](/triangle-finding/).
- **Learning graphs.** Belovs introduced them at STOC 2012 and gave [triangle finding](/triangle-finding/) with $O(n^{35/27})$ queries there.
- **Time.** Belovs, Childs, Jeffery, Kothari and Magniez (ICALP 2013) solved 3-distinctness in time close to $N^{5/7}$ with quantum walks. Jeffery and Zur (STOC 2023) reached time close to Belovs's query bound for every constant $k$ with multidimensional quantum walks.

## When to use it

Use it as the query bound for $k$-distinctness with $k \ge 3$, and as a model for learning-graph or adversary-bound constructions. To run a program, use [Ambainis's quantum walk](/ambainis-element-distinctness/), which has a known time bound, or the time-efficient walks of Variants. For $k = 2$ the two bounds are the same. For collisions in a two-to-one function, use [Brassard-Høyer-Tapp](/brassard-hoyer-tapp-collision/) instead.

## Pitfalls

- The bound $O(N^{k/(k+1)})$ is Ambainis's, not Belovs's. Belovs's exponent is $1 - 2^{k-2}/(2^k - 1)$, which is smaller for $k \ge 3$.
- The learning graph of Table 2 alone is not feasible for $k \ge 3$; the fault-tolerant version of Section 6 is needed.
- The sizes $r_1 + \cdots + r_{k-1}$ must be smaller than $N$. This holds for large $N$, since $\rho_{k-1} = 1 - 1/(2^k - 1) < 1$, but not for small $N$ with large $k$.
- Grover search alone gives only $O(N^{3/4})$ for element distinctness (Buhrman et al.); the quantum walk or the learning graph is needed for $N^{2/3}$.
- The lower bounds of the [polynomial method](/polynomial-method/) before 2026 were not tight for $k \ge 3$: they were $\tilde{\Omega}(N^{3/4 - 1/(2k)})$ and $\Omega(N^{3/4 - 1/(4k)})$. The matching bound is the 2026 preprint.

## Implementations

## History

Ambainis's quantum walk of 2003 gave $O(N^{k/(k+1)})$ queries, and for almost ten years nothing better was known for $k \ge 3$. In 2011 Reichardt, and Lee, Mittal, Reichardt, Špalek and Szegedy, proved that the dual adversary bound is the quantum query complexity up to a constant factor. Belovs then introduced learning graphs as a way to build dual solutions (STOC 2012) and improved triangle finding. In May 2012 he posted the $k$-distinctness algorithm, with covered elements, value-dependent weights and fault tolerance, and presented it at FOCS 2012. The question of a time-efficient version, asked at the end of the paper, was answered for $k = 3$ in 2013 and for every constant $k$ by Jeffery and Zur in 2023. In 2026 Belovs proved that the exponent is optimal.

## References
