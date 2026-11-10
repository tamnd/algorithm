---
tag: TE21R0
kind: algorithm
slug: max-sat-lp-rounding
name: Goemans-Williamson MAX-SAT rounding
aliases:
- 3/4-approximation for MAX-SAT
- LP rounding for MAX-SAT
- better of two for MAX-SAT
area: approximation/lp-rounding
level: advanced
summary: Round the MAX-SAT LP with probabilities equal to its values for a 1 − 1/e ratio, and take the better of this and a fair random assignment for a 3/4 ratio.
solves: [weighted-max-sat, max-sat]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of clauses, s: the total clause length}
  time: {worst: poly(n + m)}
  space: {extra: Θ(n + m + s)}
properties: {deterministic: false, recursive: false, online: false}
history:
  year: 1994
  people: [Michel X. Goemans, David P. Williamson]
  note: Goemans and Williamson (1994) gave the 1 − 1/e LP rounding and the 3/4 bound for the better of LP rounding and a random assignment.
prereqs: [weighted-max-sat, lp-relaxation, randomized-rounding, random-assignment-max-3-sat, linearity-of-expectation]
see_also: [max-sat, method-of-conditional-expectations, randomized-approximation-algorithm, integrality-gap, max-2-sat, max-3sat-inapproximability, linear-programming-rounding, semidefinite-programming]
sources:
  - paper: doi:10.1137/S0895480192243516
    title: Michel X. Goemans and David P. Williamson, New 3/4-approximation algorithms for the maximum satisfiability problem, SIAM Journal on Discrete Mathematics 7(4), 1994
    locator: pages 656 to 666
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 5, Section 5.4 (randomized rounding for MAX SAT) and Section 5.5 (choosing the better of two solutions)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 16 (maximum satisfiability)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 6 (the probabilistic method, with the derandomization by conditional expectations)
---

The Goemans-Williamson rounding for [weighted MAX-SAT](/weighted-max-sat/) solves an LP relaxation, sets each variable $x_i$ true with probability equal to its LP value $y_i$, and keeps the better of this assignment and a fair random assignment. LP rounding alone satisfies a clause of length $k$ with probability at least $1 - (1 - 1/k)^k \ge 1 - 1/e$ times its LP value, which is good for short clauses. The [fair random assignment](/random-assignment-max-3-sat/) is good for long clauses. Together they give at least $\tfrac34 \cdot \text{LP}^* \ge \tfrac34 \cdot \text{OPT}$ in expectation, in the convention ALG $\ge \alpha \cdot$ OPT. The LP has [integrality gap](/integrality-gap/) $3/4$, so no analysis against it gives more. With the [method of conditional expectations](/method-of-conditional-expectations/) both roundings become deterministic.

## In plain words

A formula is a list of weighted rules, and each rule asks that at least one of a few switches be set its way. You want the met rules to weigh as much as possible. First solve an easier problem where each switch may be partly on, and each rule may be partly met. Then turn each switch on with a chance equal to how much it is on in that answer.

This is good for short rules, but a long rule can lose about a third. A fair coin for each switch is bad for short rules and good for long ones. Run both and keep the better result. For each rule length, the two chances together are at least one and a half times what the easy answer says, so the better one gets at least three quarters of the best.

## The problem

The input is a CNF formula with variables $x_1, \ldots, x_n$ and clauses $C_1, \ldots, C_m$ with weights $w_j \ge 0$. Each clause is an OR of literals on different variables; let $P_j$ and $N_j$ be the sets of variables that appear in $C_j$ without and with negation, and $k_j = |P_j| + |N_j|$. The goal is an assignment of large satisfied weight $W(a) = \sum_{j : a \text{ satisfies } C_j} w_j$. The LP relaxation is

$$\text{LP}^* = \max \sum_{j=1}^m w_j z_j \quad \text{subject to} \quad \sum_{i \in P_j} y_i + \sum_{i \in N_j} (1 - y_i) \ge z_j \text{ for each } j, \qquad 0 \le y_i \le 1, \quad 0 \le z_j \le 1.$$

An assignment with $y_i = a_i$ and $z_j = 1$ for each satisfied clause is feasible, so $\text{OPT} \le \text{LP}^*$; this is the upper bound of the analysis.

## The algorithm

```pseudo id=main
GW-MAX-SAT(x_1, ..., x_n, C_1, ..., C_m, w)
L1  (y, z) ← an optimal solution of the MAX-SAT LP       ▷ ellipsoid or interior point method
L2  for i ← 1 to n: a_i ← 1 with probability y_i, independently
L3  for i ← 1 to n: b_i ← 1 with probability 1/2, independently
L4  if W(a) ≥ W(b) then return a else return b
```

Line L1 solves an LP with $n + m$ variables and $m$ constraints besides the bounds, of polynomial size, so no separation oracle is needed. Line L2 is [randomized rounding](/randomized-rounding/), and line L3 is the random assignment. The deterministic form replaces lines L2 and L3 by their derandomizations and keeps line L4.

## Example

Take three variables and five clauses of lengths 1, 2 and 3.

| clause | weight | $z_j$ | $\Pr[\text{sat}]$ under $y$ | $\Pr[\text{sat}]$ under $1/2$ |
|---|---|---|---|---|
| $\lnot x_2$ | 2 | 2/3 | 2/3 | 1/2 |
| $\lnot x_1 \lor \lnot x_2$ | 4 | 1 | 7/9 | 3/4 |
| $\lnot x_1 \lor x_3$ | 1 | 1 | 7/9 | 3/4 |
| $x_1 \lor x_2$ | 2 | 1 | 7/9 | 3/4 |
| $\lnot x_1 \lor x_2 \lor \lnot x_3$ | 2 | 1 | 19/27 | 7/8 |

An optimal LP solution is $y = (2/3, 1/3, 2/3)$ with the values $z_j$ of the table, so $\text{LP}^* = 4/3 + 9 = 31/3$. The best assignment is $(1, 0, 0)$, which misses only the clause $\lnot x_1 \lor x_3$, so OPT $= 10$.

- LP rounding gives the expected weight $221/27 \approx 8.19$, and the random assignment gives $8$. Their average, $437/54 \approx 8.09$, is at least $\tfrac34 \cdot \tfrac{31}{3} = 7.75$, as the theorem says.
- The randomized algorithm, which keeps the better of the two, has the exact expected weight $1949/216 \approx 9.02$, over all $8 \cdot 8$ pairs of outcomes.
- Both derandomized roundings, with the variables fixed in the order $x_1, x_2, x_3$, reach the assignment $(0, 1, 1)$ of weight 9, so the deterministic form returns weight 9, a ratio of $0.9$ against OPT.

## Correctness

**Theorem (Goemans and Williamson 1994).** Let $(y, z)$ be an optimal LP solution. Then LP rounding gives $\mathbb{E}[W(a)] \ge \sum_j \beta_{k_j} w_j z_j \ge (1 - 1/e) \cdot \text{LP}^*$ with $\beta_k = 1 - (1 - 1/k)^k$, and GW-MAX-SAT gives $\mathbb{E}[\max(W(a), W(b))] \ge \tfrac12 (\mathbb{E}[W(a)] + \mathbb{E}[W(b)]) \ge \tfrac34 \cdot \text{LP}^* \ge \tfrac34 \cdot \text{OPT}$.

A clause of length $k$ is false under $a$ with probability $\prod_{i \in P_j} (1 - y_i) \prod_{i \in N_j} y_i$. By the inequality of arithmetic and geometric means and the LP constraint, this is at most $(1 - z_j/k)^k$. The function $1 - (1 - z/k)^k$ is concave on $[0, 1]$ and is 0 at $z = 0$, so it is at least $\beta_k z$. For the average, the random assignment satisfies the clause with probability $1 - 2^{-k} \ge (1 - 2^{-k}) z_j$, and $\tfrac12 (\beta_k + 1 - 2^{-k}) \ge 3/4$ for every $k \ge 1$: it is $3/4$ for $k = 1$ and for $k = 2$, and above $\tfrac12 (0.632 + 0.875) > 3/4$ for $k \ge 3$. The full proof is in the proof file below.

**Tightness.** The four clauses $x_1 \lor x_2$, $x_1 \lor \lnot x_2$, $\lnot x_1 \lor x_2$ and $\lnot x_1 \lor \lnot x_2$ with unit weights have OPT $= 3$, since each assignment falsifies one of them, while $y = (1/2, 1/2)$ and $z = 1$ give $\text{LP}^* = 4$. So the integrality gap of this LP is at most $3/4$, and the bound $3/4$ against $\text{LP}^*$ is tight. For LP rounding alone, the bound $\beta_k$ per clause is tight as $k$ grows, so its ratio against $\text{LP}^*$ cannot be better than $1 - 1/e$ in general. For the problem, MAX-SAT contains MAX-E3-SAT, which is NP-hard to approximate within $7/8 + \varepsilon$ by [Håstad's theorem](/max-3sat-inapproximability/).

## Complexity

- **Time.** The LP has $n + m$ variables, $m$ constraints with $s$ nonzero coefficients in all, and the bounds. The [ellipsoid method](/ellipsoid-method/) or an [interior point method](/interior-point-method/) solves it in time polynomial in $n + m$ and the bit size of the weights. Lines L2 to L4 take $\Theta(n + s)$ time. The derandomized form computes $2n$ conditional expectations, each in $O(s)$ time, for $O(n s)$ in total. The total is poly$(n + m)$.
- **Space.** $\Theta(n + m + s)$ for the formula and the LP solution, besides the LP solver.

## Properties

- **Randomized, ratio in expectation.** The bound $3/4$ holds for the expected weight. The deterministic form gives at least $\tfrac34 \cdot \text{LP}^*$ for each input; see [randomized approximation algorithms](/randomized-approximation-algorithm/).
- **Per-clause bounds.** Each clause gets its own guarantee, $\beta_k z_j$ under LP rounding and $1 - 2^{-k}$ under the fair coins. This is why the average works: the two methods are good on different clause lengths.
- **One LP for both bounds.** Both expected weights are compared with the same $\text{LP}^*$, so each run also certifies its own ratio against $\text{LP}^*$.

## Variants and improvements

- **A single nonlinear rounding.** Goemans and Williamson also gave roundings that set $x_i$ true with probability $f(y_i)$ for a function $f$ other than the identity, and reach $3/4$ with one run. The linear choice $f(y) = \tfrac14 + \tfrac12 y$ works too: since $1 - f(y) = f(1 - y)$, a clause of length $k$ is false with probability at most $(\tfrac34 - \tfrac{z_j}{2k})^k$, and this gives at least $\tfrac34 z_j$ for each $k$.
- **Mixing.** Using LP rounding with probability $1/2$ and fair coins with probability $1/2$ gives the same $3/4$ in expectation, since the expected weight is the average of the two.
- **Earlier and better ratios.** Yannakakis (1994) gave a different $3/4$-approximation, using network flow. Semidefinite programming gives more: Goemans and Williamson (1995) reached about $0.758$ for MAX-SAT, and later work by Feige and Goemans, Karloff and Zwick, and Avidor, Berkovitch and Zwick raised it to about $0.797$. For [MAX-2-SAT](/max-2-sat/), [semidefinite programming](/semidefinite-programming/) gives about $0.940$.
- **Biased coins.** After a simple preprocessing of the unit clauses, a coin with bias $p = (\sqrt{5} - 1)/2 \approx 0.618$ toward the heavier unit clause of each variable gives ratio $0.618$ without an LP (Lieberherr and Specker 1981).

## When to use it

Use it when the formula has many short clauses and the weights matter, and an LP solver is at hand. For exact 3-CNF or longer clauses, the random assignment alone is as good. In practice, run the deterministic form and then a local search from its output; the LP value certifies how far from optimal the result can be.

## Pitfalls

- **Repeated or complementary literals.** The bound $\beta_k$ assumes $k$ different variables in the clause. Merge repeated literals first, and remove a clause with $x$ and $\lnot x$, which every assignment satisfies.
- **Expecting $3/4$ from one method.** Neither rounding alone has ratio $3/4$: LP rounding loses on long clauses, down to $1 - 1/e \approx 0.632$, and fair coins lose on unit clauses, down to $1/2$.
- **Looking for a better rounding of this LP.** The gap instance shows that a bound above $3/4$ needs a stronger relaxation, such as the SDP, not a better rounding of this LP.
- **Floating-point probabilities.** The derandomization compares conditional expectations that can be equal. Use exact fractions for small inputs. With floating point, a near tie can go the wrong way, and the loss at that step is at most the size of the error.

## Implementations

The Python code solves the LP with a small exact simplex method in rational arithmetic, computes the expected weight under any product distribution exactly, and gives both the randomized algorithm and the deterministic form that takes the better of the two derandomized roundings.

## History

Johnson (1974) gave the first approximation for MAX-SAT, with ratio $1/2$, and Lieberherr and Specker (1981) gave $0.618$. Yannakakis (1994) gave the first $3/4$-approximation, by network flow and probabilistic arguments. Goemans and Williamson (1994) gave the simpler LP rounding with ratio $1 - 1/e$ and the $3/4$ bound for the better of two. A year later, their semidefinite programming method for maximum cut also improved MAX-SAT, and it opened the line of SDP-based work.

## References
