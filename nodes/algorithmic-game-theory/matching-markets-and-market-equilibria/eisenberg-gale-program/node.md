---
tag: R0QFZC
kind: algorithm
slug: eisenberg-gale-program
name: Eisenberg-Gale convex program
aliases:
- Eisenberg-Gale program
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: Finds equilibrium allocations of a linear Fisher market by maximizing the budget-weighted sum of log utilities. Its dual variables are prices.
model: real-ram
complexity:
  vars: {n: the number of buyers, m: the number of goods, T: the number of rounds of mirror ascent}
  time: {worst: "O(T (n + m) n^2 m^2)"}
  space: {extra: O(n m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1959
  people: [Edmund Eisenberg, David Gale]
  note: Eisenberg and Gale (1959) found the program for the pari-mutuel market, a Fisher market with linear utilities; Eisenberg (1961) extended it to homogeneous utilities.
prereqs: [fisher-market, kkt-conditions, convex-optimization-problem]
see_also: [dpsv-algorithm, orlin-fisher-market-algorithm, proportional-response-dynamics, mirror-descent, maximum-nash-welfare, competitive-equilibrium-from-equal-incomes, proportional-fairness, nash-bargaining-solution]
sources:
  - paper: doi:10.1214/aoms/1177706369
    title: "Edmund Eisenberg and David Gale, Consensus of subjective probabilities: the pari-mutuel method, Annals of Mathematical Statistics 30(1), 165-168 (1959)"
    locator: the whole paper (the convex program whose solution gives the equilibrium odds of a pari-mutuel market)
  - paper: doi:10.1287/mnsc.7.4.337
    title: "Edmund Eisenberg, Aggregation of utility functions, Management Science 7(4), 337-350 (1961)"
    locator: the whole paper (the program for utilities that are homogeneous of degree one)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 5, Vijay V. Vazirani, Combinatorial algorithms for market equilibria (the program and its KKT conditions), and Chapter 6, Bruno Codenotti and Kasturi Varadarajan, Computation of market equilibria by convex programming
  - paper: doi:10.1145/1411509.1411512
    title: "Nikhil R. Devanur, Christos H. Papadimitriou, Amin Saberi and Vijay V. Vazirani, Market equilibrium via a primal-dual algorithm for a convex program, Journal of the ACM 55(5), Article 22 (2008)"
    locator: the whole paper (a combinatorial algorithm for the program, guided by its KKT conditions)
  - paper: doi:10.1007/s10107-006-0065-5
    title: "Yinyu Ye, A path to the Arrow-Debreu competitive market equilibrium, Mathematical Programming 111(1), 315-348 (2008)"
    locator: the whole paper (interior point algorithms for the Fisher and exchange models)
---

The Eisenberg-Gale program is a [convex optimization problem](/convex-optimization-problem/) whose optimal solutions are exactly the equilibrium allocations of a [Fisher market](/fisher-market/) with linear utilities. It maximizes the sum over buyers of the budget times the logarithm of the utility, subject only to the supply of each good. The Lagrange multipliers of the supply constraints are the equilibrium prices. So a market equilibrium, defined by the selfish choices of buyers at given prices, is also the optimum of one global objective, and anything that solves convex programs computes it: the ellipsoid method, interior point methods (Ye 2008), first-order methods, and the combinatorial [DPSV algorithm](/dpsv-algorithm/) and [Orlin's algorithm](/orlin-fisher-market-algorithm/), which are guided by its optimality conditions. With equal budgets the objective is the Nash social welfare, which links Fisher markets to [maximum Nash welfare](/maximum-nash-welfare/), [CEEI](/competitive-equilibrium-from-equal-incomes/) and [proportional fairness](/proportional-fairness/).

## In plain words

Each buyer brings money and likes some goods more than others. Instead of searching for prices, give the goods out so that a single score is as high as possible. The score adds up, for each buyer, her money times the logarithm of how happy she is. The logarithm means that taking from a happy buyer to help an unhappy one often raises the score, and the money weights give richer buyers more say. The best split of the goods is exactly what the buyers would choose if the right prices were posted. Those prices can be read off the best split: a good costs what the buyer who wants it most is willing to pay per unit at that split.

## The problem

There are $n$ buyers and $m$ goods, with one unit of each good. Buyer $i$ has a budget $e_i > 0$ and a linear utility $U_i(x_i) = \sum_j u_{ij} x_{ij}$ with $u_{ij} \ge 0$. Every buyer likes some good and every good is liked by some buyer. The *Eisenberg-Gale program* is

$$
\max \; \sum_i e_i \log \sum_j u_{ij} x_{ij} \quad \text{subject to} \quad \sum_i x_{ij} \le 1 \text{ for every good } j, \qquad x \ge 0 .
$$

With a multiplier $p_j \ge 0$ for the supply of good $j$, the [KKT conditions](/kkt-conditions/) are

1. $p_j > 0 \implies \sum_i x_{ij} = 1$;
2. $e_i u_{ij} / U_i \le p_j$ for all $i, j$, that is, $u_{ij} / p_j \le U_i / e_i$;
3. $x_{ij} > 0 \implies e_i u_{ij} / U_i = p_j$.

Condition 2 says that no good gives buyer $i$ more utility per unit of money (bang per buck) than $U_i / e_i$, and condition 3 says that she buys only goods that reach it. Multiplying condition 3 by $x_{ij}$ and summing over $j$ gives $\sum_j p_j x_{ij} = e_i$: she spends exactly her budget. These are the equilibrium conditions of the Fisher market. The task is to find the prices $p$ and an optimal allocation $x$, exactly.

## The algorithm

The implementation solves the program by mirror ascent with the entropy on each good ([mirror descent](/mirror-descent/) for a maximization, also called exponentiated gradient), in floating point, and then rounds to an exact answer that it certifies with a maximum flow in exact arithmetic. Here $f(x)$ is the objective, $g = \nabla f$, and $\mathrm{KL}(y \| x) = \sum_{ij} y_{ij} \log(y_{ij} / x_{ij})$.

```pseudo id=main
EISENBERG-GALE(utilities u, budgets e)
L1  x_ij ← 1 / (number of buyers who like j) for every edge u_ij > 0, else 0
L2  η ← 1
L3  for round = 1, 2, ... do
L4      g_ij ← e_i u_ij / U_i(x) for every edge
L5      y_ij ← x_ij exp(η g_ij) / Σ_k x_kj exp(η g_kj) for every edge (normalized per good)
L6      if f(y) < f(x) + g·(y - x) - KL(y ‖ x) / η then η ← η / 2 and go to L5
L7      x ← y;  η ← 2η
L8      every 5 rounds: for δ = 10^-2, ..., 10^-14: S ← {x_ij > δ}; p ← the prices that S forces;
            if p passes the exact max-flow check, return p and the flow allocation
```

Line L5 is the closed-form maximizer of $g \cdot y - \mathrm{KL}(y \| x)/\eta$ over allocations that give out each good completely. Line L6 is a backtracking test: it accepts the step only if the program's objective is at least the model that the step maximized, which makes $f$ increase in every round.

Line L8 rounds. A guessed support $S$ forces the prices: on each connected part of $S$, every buyer gets the same bang per buck on all her edges, which fixes the ratios of the prices, and the prices of the part add up to the budgets of its buyers. The check then computes, in `Fraction`, the maximum bang per buck $\alpha_i = \max_j u_{ij} / p_j$ of each buyer and a maximum flow in the network source $\to$ good $j$ (capacity $p_j$) $\to$ buyer $i$ (only if $u_{ij} / p_j = \alpha_i$) $\to$ sink (capacity $e_i$). The prices are accepted if they sum to $\sum_i e_i$ and the flow has value $\sum_i e_i$; then $x_{ij}$ is the flow from $j$ to $i$ divided by $p_j$.

## Example

Three buyers and two goods: $u_1 = (2, 1)$, $u_2 = (1, 2)$, $u_3 = (1, 1)$, budgets $e = (1, 1, 2)$. Line L1 gives every buyer $1/3$ of each good. In the table, buyer 3 holds the same amount of both goods at every round, $f$ is the objective, and the last column is the KKT estimate $\max_i e_i u_{i1} / U_i$ of $p_1$ (by symmetry, $p_2$ has the same estimate).

| round | $\eta$ used | buyer 1 $(x_{11}, x_{12})$ | buyer 3, each good | $f$ | estimate of $p_1$ |
|---|---|---|---|---|---|
| 0 | | $(0.3333, 0.3333)$ | $0.3333$ | $-0.81093$ | |
| 1 | 0.5 | $(0.3072, 0.1863)$ | $0.5065$ | $-0.41874$ | $2.4978$ |
| 2 | 1 | $(0.4649, 0.0809)$ | $0.4542$ | $-0.17082$ | $2.2017$ |
| 3 | 1 | $(0.4375, 0.0283)$ | $0.5342$ | $-0.07106$ | $2.2140$ |
| 4 | 0.5 | $(0.4840, 0.0180)$ | $0.4980$ | $-0.03621$ | $2.0285$ |
| 5 | 1 | $(0.4947, 0.0067)$ | $0.4987$ | $-0.01337$ | $2.0080$ |

At round 5, line L8 with $\delta = 10^{-2}$ drops the edge $(1, 2)$ and keeps $S = \{(1, 1), (2, 2), (3, 1), (3, 2)\}$. $S$ is connected; the bang per buck conditions give $p_1 = p_2$ (from buyer 3), and the prices add up to the total budget $4$, so $p = (2, 2)$. At these prices, buyer 1 spends $1$ on good 1, buyer 2 spends $1$ on good 2, and buyer 3, who is indifferent, spends $1$ on each good. The flow saturates, so the answer is certified: $x_1 = (1/2, 0)$, $x_2 = (0, 1/2)$, $x_3 = (1/2, 1/2)$, all utilities are $1$, and the optimal value is $0$. The ascent itself would need many more rounds to reach this point in floating point.

## Correctness

The proof is in `proofs/correctness.md`. It shows:

1. **The program solves the market.** An allocation is optimal if and only if, with some prices, it is a Fisher market equilibrium, and the prices are then the KKT multipliers. Because $\log$ is strictly concave, the optimal utilities $U_i$ are unique, and so are the prices $p_j = \max_i e_i u_{ij} / U_i$. The allocation need not be unique.
2. **Each round improves the objective.** Line L6 can always be met by a small enough $\eta$, and when it holds, $f(y) \ge f(x)$, because $y$ maximizes the model that line L6 compares with.
3. **The output is exact.** Whatever line L8 guesses, it returns only prices that pass the max-flow check, and passing it means each buyer spends her whole budget on goods of maximum bang per buck and every good is sold. By point 1 the returned $x$ is optimal.
4. **It terminates.** The iterates converge to an optimal allocation $\bar{x}$; once they are close, a threshold between their distance to $\bar{x}$ and the smallest positive entry of $\bar{x}$ recovers the support of $\bar{x}$, which forces the equilibrium prices. This needs the smallest positive entry of $\bar{x}$ to be above about $2 \cdot 10^{-14}$, and the implementation stops with an error otherwise.

## Complexity

A round of lines L4 to L7 costs $O(nm)$ arithmetic operations per backtracking step, and the number of backtracking steps per round is $O(1)$ on average because $\eta$ doubles after each accepted step. Mirror ascent has $f^* - f(x^T) \le \mathrm{KL}(x^* \| x^0) / (\eta_{\min} T)$, where $\eta_{\min}$ is the smallest step accepted, and $\mathrm{KL}(x^* \| x^0) \le m \log n$. This bounds the objective, not the number of rounds until the support is found, which depends on how small the positive entries of the optimum are. Each check of line L8 runs Edmonds-Karp on $n + m + 2$ nodes and up to $nm + n + m$ arcs, $O((n + m) n^2 m^2)$ exact operations on rationals. Line L8 runs every 5 rounds with a fixed number of thresholds, so $T$ rounds take $O(Tnm)$ time for the mirror steps and $O(T (n + m) n^2 m^2)$ time for the checks.

For guaranteed bounds, the program can be solved exactly in polynomial time by the ellipsoid method or by interior point methods, because its optimum is rational with polynomial bit length. The [DPSV algorithm](/dpsv-algorithm/) solves it combinatorially with polynomially many max-flow computations, and [Orlin's algorithm](/orlin-fisher-market-algorithm/) in strongly polynomial time.

## Properties

- **Equilibrium as an optimum.** The market equilibrium maximizes a global objective. Existence of the equilibrium follows at once: the feasible set is compact and has points where every $U_i > 0$.
- **Unique prices and utilities**, possibly many allocations. In the example the allocation is unique. With two identical buyers who both buy two goods, they can swap amounts of the two goods at the price ratio without changing their utilities, so the allocation is not unique.
- **Pareto optimal** and, with equal budgets, envy-free: it is the [CEEI](/competitive-equilibrium-from-equal-incomes/) allocation and the maximum Nash welfare allocation of divisible goods.
- **Rational.** For rational $u$ and $e$, the prices and some optimal allocation are rational, because they solve a linear system once the support is known.
- **Beyond linear utilities.** The same program, with $U_i$ replaced by any concave utility that is homogeneous of degree one (for example CES or Leontief), still captures the Fisher equilibrium (Eisenberg 1961).

## Variants and improvements

- **Homogeneous utilities.** Eisenberg (1961) proved the program for all concave, homogeneous of degree one utilities. For utilities that are not homogeneous, such as additively separable concave ones, no such program is known in general, and SPLC Fisher markets are PPAD-hard; see [PPAD-hardness of market equilibria](/ppad-hardness-of-arrow-debreu/).
- **Shmyrev's program.** A different convex program in the bids $b_{ij}$ (money spent) has the same equilibria for linear utilities; mirror descent on it is [proportional response dynamics](/proportional-response-dynamics/).
- **Combinatorial algorithms.** The [DPSV algorithm](/dpsv-algorithm/) raises prices while keeping KKT conditions 2 and 3 for the current equality graph, and [Orlin's algorithm](/orlin-fisher-market-algorithm/) adds scaling to make the bound strongly polynomial.
- **Nash bargaining.** With equal budgets the objective is the logarithm of the Nash product; see the [Nash bargaining solution](/nash-bargaining-solution/) and [proportional fairness](/proportional-fairness/), where Kelly used the same objective for bandwidth.

## When to use it

Use the program to prove facts about Fisher markets (existence, uniqueness of prices, efficiency) and to compute equilibria with an off-the-shelf convex solver when an approximate answer is enough. Use the rounding and max-flow check of line L8 when an exact answer is needed and the market is small. For large linear markets with exact answers, use a combinatorial algorithm; for distributed settings, use [proportional response dynamics](/proportional-response-dynamics/).

## Pitfalls

- Skipping the exact check of line L8 and returning the rounded support or the float prices can give a wrong answer: a threshold that is too large drops a needed edge and splits a part of $S$, and the prices it forces are then off.
- A fixed step in line L5 without the test of line L6 can fail: the gradient $e_i u_{ij} / U_i$ is huge when $U_i$ is small, and a large step can move almost all of every good away from a buyer, so that the objective falls.
- A zero start on an edge in line L1 stays zero forever, because line L5 is multiplicative. Every edge with $u_{ij} > 0$ must start positive.
- If some good is liked by no buyer, its supply constraint has multiplier $0$ and the good is left unsold; the reading of multipliers as positive prices assumes every good is liked.
- Reading prices from the dual is only right for an optimal $x$. At a non-optimal point, the estimates $\max_i e_i u_{ij} / U_i$ need not add up to the total budget.

## Implementations

## History

Eisenberg and Gale (1959) studied the pari-mutuel method of betting, in which bettors with budgets and subjective probabilities place bets on horses and the odds are set by the money bet. They showed that the equilibrium odds come from maximizing $\sum_i e_i \log U_i$, which gives the existence and uniqueness of the equilibrium odds. Eisenberg (1961) extended the program to homogeneous utilities. Computer science took it up in the 2000s: Devanur, Papadimitriou, Saberi and Vazirani (journal version 2008) gave a combinatorial primal-dual algorithm guided by its KKT conditions, Ye (2008) gave interior point algorithms, and Orlin (2010) gave a strongly polynomial algorithm. Later work on fair division uses the same objective as the maximum Nash welfare rule.

## References
