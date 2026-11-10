---
tag: G3HNQ1
kind: algorithm
slug: random-assignment-max-3-sat
name: Randomized 8/7-approximation for MAX-3-CNF
aliases:
- random assignment for MAX-3SAT
- 7/8-approximation for MAX-3SAT
- uniform random assignment for MAX-E3-SAT
area: approximation/lp-rounding
level: core
summary: Sets each variable true or false uniformly at random, so each clause is satisfied with probability 7/8 and the expected number of satisfied clauses is at least 7/8 of the optimum.
solves: [max-sat]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of clauses}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: false, recursive: false, online: false}
history:
  year: 1974
  people: [David S. Johnson]
  note: Johnson (1974) gave the deterministic form, which satisfies at least 1 − 2^(−k) of the clauses when each has at least k literals; the random assignment is the probabilistic view of it.
prereqs: [max-sat, 3-sat, linearity-of-expectation, indicator-random-variable]
see_also: [method-of-conditional-expectations, max-3sat-inapproximability, max-sat-lp-rounding, randomized-approximation-algorithm, probabilistic-method, weighted-max-sat, max-2-sat, maximum-cut]
sources:
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 35, Section 35.4 (a randomized approximation algorithm for MAX-3-CNF satisfiability)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 5, Section 5.1 (simple algorithms for MAX SAT and MAX CUT) and Section 5.2 (derandomization)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 6 (the probabilistic method, the expectation argument for satisfiability)
  - paper: "David S. Johnson, Approximation algorithms for combinatorial problems, Journal of Computer and System Sciences 9, 1974"
    locator: pages 256 to 278 (the MAX-SAT algorithm with ratio 1 − 2^(−k))
  - paper: doi:10.1145/502090.502098
    title: Johan Håstad, Some optimal inapproximability results, Journal of the ACM 48(4), 2001
    locator: pages 798 to 859 (7/8 + ε hardness for MAX-E3-SAT)
---

The random assignment algorithm for MAX-3-CNF sets each variable to true or false by a fair coin, independently. When each clause has exactly three literals on three different variables, each clause is false only when all three literals are false, which has probability $1/8$. So the expected number of satisfied clauses is $7m/8$, which is at least $7/8$ of the optimum. In the convention ALG $\ge \alpha \cdot$ OPT for maximization, the ratio is $\alpha = 7/8$ in expectation; CLRS writes the same bound as a randomized $8/7$-approximation. By the [method of conditional expectations](/method-of-conditional-expectations/) it becomes a deterministic algorithm with the same bound, and by [Håstad's theorem](/max-3sat-inapproximability/) no polynomial-time algorithm does better than $7/8 + \varepsilon$ unless P = NP.

## In plain words

A formula is a list of rules, and each rule names three different switches and says which way each one should be. A rule is met when at least one of its three switches is set its way. You want to meet as many rules as you can.

Flip a fair coin for each switch. A rule fails only when all three of its switches go the wrong way, and that happens in one case out of eight. So, on average, seven rules in eight are met. No setting can meet more than all of them, so the average result is at least seven eighths of the best. Choosing the switches one at a time, each time the way that keeps the average high, gives a fixed setting that is never below this average.

## The problem

The input is a CNF formula with variables $x_1, \ldots, x_n$ and clauses $C_1, \ldots, C_m$, where each clause is an OR of exactly three literals on three different variables. This is MAX-3-CNF, also called MAX-E3-SAT. The output is an assignment $a \in \{0, 1\}^n$, and the goal is to make the number $s(a)$ of satisfied clauses large. It is the case of [MAX-SAT](/max-sat/) with clause length 3, and it is NP-hard because [3-SAT](/3-sat/) is. The analysis compares with the upper bound $\text{OPT} \le m$.

## The algorithm

```pseudo id=main
RANDOM-ASSIGNMENT(x_1, ..., x_n, C_1, ..., C_m)
L1  for i ← 1 to n do
L2      a_i ← 1 with probability 1/2, else 0, independently
L3  s ← the number of clauses satisfied by a
L4  return (a, s)
```

The algorithm does not read the clauses to pick $a$; line L3 only counts. No LP is solved. It uses $n$ random coins and one pass over the clauses.

## Example

Take $n = 4$ and the six clauses

$$(x_1 \lor x_2 \lor \lnot x_3), (\lnot x_1 \lor x_3 \lor x_4), (\lnot x_2 \lor \lnot x_3 \lor \lnot x_4), (x_1 \lor \lnot x_2 \lor x_4), (\lnot x_1 \lor \lnot x_2 \lor x_3), (x_2 \lor x_3 \lor x_4).$$

Of the 16 assignments, 2 satisfy 4 clauses, 8 satisfy 5 and 6 satisfy all 6. So the formula is satisfiable, OPT $= 6$, and the random assignment satisfies $(2 \cdot 4 + 8 \cdot 5 + 6 \cdot 6)/16 = 21/4 = 7 \cdot 6/8$ clauses on average. It finds a satisfying assignment with probability $6/16$.

The derandomized form fixes the variables in order and keeps the conditional expectation $E$ of the number of satisfied clauses, with the free variables still fair coins.

| step | $E$ if true | $E$ if false | choice |
|---|---|---|---|
| $x_1$ | 21/4 | 21/4 | true (tie) |
| $x_2$ | 5 | 11/2 | false |
| $x_3$ | 6 | 5 | true |
| $x_4$ | 6 | 6 | true (tie) |

The result $(1, 0, 1, 1)$ satisfies all 6 clauses. The method promises only $E \ge 21/4$, so at least 6 since the count is an integer.

**A tight formula.** The 8 clauses on $x_1, x_2, x_3$ with all 8 sign patterns have OPT $= 7$: each assignment falsifies exactly the clause whose literals are all false under it. Here every assignment satisfies $7m/8$ clauses, so the bound $7m/8$ cannot be raised as a fraction of $m$.

## Correctness

**Theorem.** If each clause has exactly three literals on three different variables, then $\mathbb{E}[s] = 7m/8 \ge \tfrac78 \text{OPT}$.

Let $Y_j$ be the [indicator](/indicator-random-variable/) of the event that $C_j$ is satisfied. The clause is false exactly when each of its three literals is false. The three literals are on different variables, so these events are independent, each with probability $1/2$, and $\Pr[Y_j = 0] = 1/8$. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[s] = \sum_j \mathbb{E}[Y_j] = 7m/8$, and $\text{OPT} \le m$. The full proof, with the derandomized form, is in the proof file below.

**Consequences.** Since $\mathbb{E}[s] = 7m/8$, some assignment satisfies at least $7m/8$ clauses. So every exact 3-CNF formula with at most 7 clauses is satisfiable. This is a first example of the [probabilistic method](/probabilistic-method/).

**Tightness.** For the algorithm, each satisfiable formula, such as the example, has $\mathbb{E}[s] = 7m/8$ and OPT $= m$, so the ratio $7/8$ is exact. The formula with all 8 sign patterns has OPT $= 7m/8$, so no algorithm can promise more than $7m/8$ satisfied clauses as a fraction of $m$. For the problem, Håstad (2001) showed that for each $\varepsilon > 0$ it is NP-hard to tell satisfiable exact 3-CNF formulas from those where at most a $7/8 + \varepsilon$ fraction of the clauses can be satisfied. So $7/8$ is the best ratio in polynomial time unless P = NP, even on satisfiable inputs.

## Complexity

- **Time.** Lines L1 and L2 take $\Theta(n)$ time with $n$ coin flips, and line L3 reads $3m$ literals, so the time is $\Theta(n + m)$ in the worst case. The derandomized form computes $2n$ conditional expectations, each in $O(m)$ time, so $O(n m)$ time; with a list of the clauses of each variable it updates only the clauses that change, in $O(n + m)$ total time.
- **Space.** $\Theta(n)$ for the assignment, besides the input.

## Properties

- **Randomized, ratio in expectation.** The bound holds for $\mathbb{E}[s]$. See [randomized approximation algorithms](/randomized-approximation-algorithm/) for the forms with high probability.
- **Oblivious.** The assignment does not depend on the formula. The same coins give $7/8$ in expectation for every exact 3-CNF formula on these variables at once.
- **Three-wise independence is enough.** The proof uses only that the three variables of each clause are independent. A [3-wise independent](/k-wise-independence/) family of assignments of polynomial size has the same expectation, so trying all of them is a second deterministic algorithm. Pairwise independence is not enough: with $x_3 = x_1 \oplus x_2$, the clause $x_1 \lor x_2 \lor x_3$ is false with probability $1/4$.
- **Longer clauses.** A clause with $k$ literals on $k$ different variables is satisfied with probability $1 - 2^{-k}$. So for clauses of length at least $k$, the ratio is $1 - 2^{-k}$, and for general MAX-SAT it is $1/2$.

## Variants and improvements

- **Derandomization.** Fix $x_1, x_2, \ldots$ in turn to the value with the larger conditional expectation; each conditional expectation is a sum of terms $1$ or $1 - 2^{-k}$ over the clauses, with $k$ the number of free literals. This is the [method of conditional expectations](/method-of-conditional-expectations/), which has a worked trace for this problem. Johnson (1974) gave this algorithm, in a greedy form with weights $2^{-k}$, before the probabilistic view was common.
- **Clauses of mixed length.** For clauses of length 1 or 2, the random assignment gives only $1/2$ or $3/4$ per clause. [LP rounding for MAX-SAT](/max-sat-lp-rounding/) handles short clauses better, and the better of the two methods gives $3/4$ for general MAX-SAT.
- **Up to three literals.** Karloff and Zwick (1997) used semidefinite programming to get $7/8$ for MAX-3-SAT with clauses of at most three literals, where the random assignment gives only $1/2$ on unit clauses. The proof of the ratio for all instances was completed with computer help by Zwick (2002).
- **Weights.** With clause weights, the expected satisfied weight is $\tfrac78$ of the total weight, and the same proof applies; see [weighted MAX-SAT](/weighted-max-sat/).

## When to use it

Use it as a baseline for MAX-3-SAT and for exact $k$-CNF formulas, where it is optimal in polynomial time. Use the derandomized form when you need a guarantee for each run, or a local search started from its output for better results in practice. For formulas with short clauses, use the LP-based method or the SDP of Karloff and Zwick.

## Pitfalls

- **Repeated variables.** The bound needs three different variables per clause. The clause $x_1 \lor x_1 \lor x_2$ is satisfied with probability only $3/4$, and $x_1 \lor \lnot x_1 \lor x_2$ always. For such inputs, compute the probability of each clause from its set of distinct literals.
- **The wrong ratio convention.** CLRS calls this an $8/7$-approximation, with the ratio at least 1. In the convention ALG $\ge \alpha \cdot$ OPT the same bound is $\alpha = 7/8$. Do not mix the two in one argument.
- **Expectation is not a guarantee.** One run can satisfy fewer than $7m/8$ clauses. The probability that a run reaches $7m/8$ is at least $1/(m + 1)$, so the expected number of runs until one does is at most $m + 1$; or use the derandomized form.
- **Exact arithmetic in the derandomization.** The conditional expectations are multiples of $1/8$. Compute them as integers scaled by 8, or as fractions. With floating point, a near tie can go the wrong way.

## Implementations

The Python code gives the random assignment, the exact conditional expectation for any partial assignment, and the derandomized algorithm. It takes clauses as lists of DIMACS literals, where $+i$ is $x_i$ and $-i$ is $\lnot x_i$.

## History

Johnson (1974) gave a deterministic algorithm for MAX-SAT that satisfies at least $1 - 2^{-k}$ of the clauses when each clause has at least $k$ literals. It was later read as the derandomization, by conditional expectations, of the random assignment. Håstad (2001) proved, with the PCP theorem and long codes, that the ratio $7/8$ is optimal for MAX-E3-SAT unless P = NP. CLRS presents the random assignment as the first example of a randomized approximation algorithm.

## References
