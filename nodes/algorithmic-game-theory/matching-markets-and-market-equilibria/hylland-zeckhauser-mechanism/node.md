---
tag: NMFNPQ
kind: algorithm
slug: hylland-zeckhauser-mechanism
name: Hylland-Zeckhauser mechanism
aliases:
- HZ mechanism
- pseudo-market for assignment
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: advanced
summary: "Assigns probability shares of objects by a competitive equilibrium with equal budgets over cardinal utilities. Approximate equilibria are PPAD-complete; the exact case is open."
solves: [house-allocation-problem]
model: real-ram
complexity:
  vars: {n: the number of agents and of objects, g: the number of grid values for one price, T: the time of one LP solve with at most n^2 variables}
  time: {worst: O(g^n n T)}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 1979
  people: [Aanund Hylland, Richard Zeckhauser]
  note: Hylland and Zeckhauser proposed the pseudo-market in 1979. Its computational complexity was studied from 2020 by Vazirani and Yannakakis and by Chen, Chen, Peng and Yannakakis.
prereqs: [house-allocation-problem, competitive-equilibrium, linear-programming-problem]
see_also: [competitive-equilibrium-from-equal-incomes, fisher-market, probabilistic-serial, random-serial-dictatorship, birkhoff-von-neumann-decomposition, envy-freeness, ppad, approximate-ceei]
sources:
  - paper: doi:10.1086/260757
    title: Aanund Hylland and Richard Zeckhauser, The efficient allocation of individuals to positions, Journal of Political Economy 87(2), 293 to 314 (1979)
    locator: the pseudo-market with equal budgets, the existence of an equilibrium and its Pareto efficiency
  - paper: doi:10.4230/LIPIcs.ITCS.2021.59
    title: Vijay V. Vazirani and Mihalis Yannakakis, Computational complexity of the Hylland-Zeckhauser scheme for one-sided matching markets, 12th Innovations in Theoretical Computer Science Conference (ITCS 2021)
    locator: an instance with only irrational equilibria, membership of the exact problem in FIXP and of the approximate problem in PPAD, and polynomial algorithms for dichotomous and bi-valued utilities
  - paper: arXiv:2107.05746
    title: Thomas Chen, Xi Chen, Binghui Peng and Mihalis Yannakakis, Computational hardness of the Hylland-Zeckhauser scheme, Proceedings of the 2022 ACM-SIAM Symposium on Discrete Algorithms (SODA 2022)
    locator: PPAD-hardness of finding an approximate equilibrium, also for four-valued utilities
---

The Hylland-Zeckhauser mechanism solves the [house allocation problem](/house-allocation-problem/) with cardinal utilities. Each of $n$ agents gets one unit of fake money, and each of $n$ objects gets a price. Agents buy probability shares of objects: each agent buys one unit of shares in total, the best bundle it can afford, and among the best bundles the cheapest one. Prices are set so that every object is sold exactly once. This is a [competitive equilibrium](/competitive-equilibrium/), and the result is a bistochastic matrix that a [Birkhoff-von Neumann decomposition](/birkhoff-von-neumann-decomposition/) turns into a lottery over matchings. Hylland and Zeckhauser (1979) proved that an equilibrium exists and that its allocation is Pareto efficient, and with equal budgets it is also envy-free. No efficient algorithm is known. Finding an approximate equilibrium is PPAD-complete, and the complexity of the exact problem is open. The code on this page is a toy: it tries the prices on a grid.

## In plain words

A school must give $n$ rooms to $n$ students, one each, and it wants to be fair. It gives each student 1 coin of play money. The rooms get prices, and a student can buy a mix of chances, for example half a chance of room A and half of room C. A popular room gets a high price, so a student who wants it a lot pays for a large chance of it, and a student who cares less takes a sure chance of a cheap room. When the prices are right, all chances of every room are sold. Then the school draws the real rooms by lottery from these chances.

## The problem

There are $n$ agents and $n$ objects, one unit of each. Agent $i$ has utility $u_{ij} \ge 0$ for object $j$, and its expected utility for a row of shares $x_i$ is $u_i \cdot x_i = \sum_j u_{ij} x_{ij}$. A price vector $p \ge 0$ and an allocation $x$, an $n$ by $n$ matrix with $x_{ij} \ge 0$, form an HZ equilibrium when:

1. every agent gets one unit, $\sum_j x_{ij} = 1$, and every object is sold once, $\sum_i x_{ij} = 1$;
2. $x_i$ is in the budget set $\{y \ge 0 : \sum_j y_j = 1,\ p \cdot y \le 1\}$ and maximizes $u_i \cdot y$ over it;
3. among those maximizers, $x_i$ has the least cost $p \cdot y$.

Condition 3 is needed for efficiency: without it an agent could pay for shares that give it nothing more, and the money would be wasted. Some object must cost at most 1, or the budget sets are empty.

The prices can be normalized. If the smallest price $m$ is below 1, then $p' = (p - m)/(1 - m)$ gives the same budget sets, since $\sum_j y_j = 1$ turns $p \cdot y \le 1$ into $p' \cdot y \le 1$, and it orders the costs in the same way, so $(p', x)$ is also an equilibrium. If $m = 1$, then every share bought costs exactly 1, all prices are 1, every agent buys only top objects, and $p = 0$ also works. So every equilibrium allocation has prices with smallest entry 0.

## The algorithm

```pseudo id=main
HZ-GRID-SEARCH(u, k, pmax)
L1  for each price vector p with entries in {0, 1/k, 2/k, ..., pmax} and smallest entry 0 do
L2      for each agent i do
L3          U_i ← max { u_i · y : y ≥ 0, Σ_j y_j = 1, p · y ≤ 1 }
L4          C_i ← min { p · y : y ≥ 0, Σ_j y_j = 1, p · y ≤ 1, u_i · y = U_i }
L5      find x ≥ 0 with Σ_j x_ij = 1, u_i · x_i = U_i and p · x_i = C_i for each i, and Σ_i x_ij = 1 for each j
L6      if x exists then return (p, x)
L7  return none
```

This is a toy, not an efficient algorithm. For a fixed price vector, the demand set of agent $i$, the set of rows that satisfy conditions 2 and 3, is the face $\{y \ge 0 : \sum_j y_j = 1,\ u_i \cdot y = U_i,\ p \cdot y = C_i\}$. Lines L3 and L4 find $U_i$ and $C_i$ with two small linear programs, and line L5 checks with one more linear program whether the demand sets can be chosen so that every object is sold once. The hard part of the problem is to find the prices, and the toy just tries every price on a grid, in lexicographic order.

## Example

**Same favourite.** Two agents both have $u = (1, 0)$. With $p = (1, 0)$ each agent can afford all of object 1, so both demand it and the market does not clear. With $p = (2, 0)$ an agent can buy at most half of object 1, so each agent buys $(1/2, 1/2)$, which costs 1, and the market clears. The toy tries $(0, 0)$, $(1/5, 0)$ and so on, and returns $p = (2, 0)$ with the uniform matrix. Every agent gets a fair coin flip.

**Three identical agents.** All three have $u = (3, 2, 0)$. They have the same demand set, which is convex, and the rows of an equilibrium allocation average to $(1/3, 1/3, 1/3)$, so the uniform row is a best bundle. The equilibrium prices are $p = (9/5, 6/5, 0)$. Check: the bundle $(1/3, 1/3, 1/3)$ costs $3/5 + 2/5 = 1$ and has utility $5/3$. The budget set is a polygon whose corners have at most two nonzero entries. The corner that mixes objects 1 and 3 is $(5/9, 0, 4/9)$, with utility $5/3$; the corner that mixes objects 2 and 3 is $(0, 5/6, 1/6)$, also with utility $5/3$; object 3 alone has utility 0; and no mix of objects 1 and 2 alone is affordable. So $U = 5/3$, every best bundle costs 1, and $(1/3, 1/3, 1/3) = \frac35 (5/9, 0, 4/9) + \frac25 (0, 5/6, 1/6)$ is one of them. With the smallest price 0, these are the only equilibrium prices. The uniform row has no zero entry, so it is a best bundle only if the budget constraint is tight there and $(3, 2, 0) = \alpha (1, 1, 1) + \beta p$ with $\beta \ge 0$. If $p_3 = 0$, the third entry gives $\alpha = 0$, so $p$ is proportional to $(3, 2, 0)$, and a cost of 1 for the uniform row gives $p = (9/5, 6/5, 0)$. If $p_1 = 0$ or $p_2 = 0$ instead, then $\alpha > 0$ and the third entry $0 = \alpha + \beta p_3$ is impossible. The toy finds these prices but returns a vertex of the clearing LP, which is not the uniform matrix.

**No conflict.** With $u_1 = (2, 1)$ and $u_2 = (1, 2)$, prices $(0, 0)$ work: each agent buys its favourite for free, and the cheapest-bundle rule plays no role.

## Correctness

The toy returns $(p, x)$ only when line L5 finds $x$. Then $x$ is bistochastic, and each row $x_i$ is in the budget set, has utility $U_i$, the largest possible by line L3, and has cost $C_i$, the least among the bundles with utility $U_i$ by line L4. These are exactly conditions 1 to 3, so every answer is an equilibrium. Conversely, if some equilibrium has its normalized prices on the grid, the toy returns an equilibrium at those prices or at an earlier grid point. If no equilibrium has grid prices, it returns none, even though an equilibrium always exists. The proof file gives the details.

The properties of the equilibrium itself are theorems.

- **Existence.** Hylland and Zeckhauser (1979) proved that an equilibrium exists for all utilities.
- **Pareto efficiency.** The allocation is Pareto efficient among all random assignments (ex ante efficient), by a first welfare theorem argument that uses condition 3.
- **Envy-freeness.** Every bundle $x_k$ costs at most 1, so agent $i$ could afford it, and $x_i$ is a best affordable bundle. So $u_i \cdot x_i \ge u_i \cdot x_k$, which is [envy-freeness](/envy-freeness/) in expected utility.

## Complexity

The toy tries $g^n$ price vectors with $g = k \cdot \text{pmax} + 1$, and for each it solves $2n + 1$ linear programs with at most $n^2$ variables, by an exact simplex method. With $T$ the time of one such solve, the total is $O(g^n n T)$. That is exponential in $n$, and it is the reason the toy is only for $n \le 3$.

No polynomial algorithm is known for the general problem, and none is expected.

- Vazirani and Yannakakis (2021) gave an instance whose only equilibria have irrational prices, so an exact answer cannot be written down in rational numbers. They showed that the exact problem is in FIXP and that finding an approximate equilibrium is in [PPAD](/ppad/). For dichotomous and bi-valued utilities they gave polynomial time algorithms.
- Chen, Chen, Peng and Yannakakis (2022) showed that finding an approximate equilibrium is PPAD-hard, even with an inverse polynomial precision and with four distinct utility values. With the membership above, the approximate problem is PPAD-complete.
- The exact problem is open as of the 2022 paper: it is in FIXP, and FIXP-hardness is not known.

The model is the [real RAM](/real-ram/), since equilibrium prices can be irrational. The toy uses exact rational numbers and therefore only sees rational grid prices.

## Properties

- **Cardinal.** It uses the strength of preferences, not only the order. An agent who cares much more about one object than about the others can buy a larger chance of it, which [probabilistic serial](/probabilistic-serial/) and [random serial dictatorship](/random-serial-dictatorship/) cannot express.
- **Scale free.** If an agent replaces $u_i$ by $a u_i + b$ with $a > 0$, its utility for every unit bundle changes in the same way, so the equilibria do not change.
- **Efficient and fair.** Ex ante Pareto efficient and envy-free, as above.
- **Not strategyproof.** An agent can sometimes gain by reporting false utilities, since its report changes the prices.
- **Money is fake.** The budgets only give each agent equal weight in the market; no real money changes hands.

## Variants and improvements

- **Unequal budgets.** Different budgets give priority to some agents. The envy-freeness argument then holds only among agents with equal budgets.
- **More objects and capacities.** Objects with several copies, and more objects than agents, fit by changing the column sums to the capacities.
- **Fisher markets.** In a linear [Fisher market](/fisher-market/) agents spend money on goods with no unit demand constraint. That market has a convex program and polynomial algorithms. The unit demand constraint $\sum_j x_{ij} = 1$ of HZ breaks this structure, and the problem becomes much harder.
- **CEEI.** [Competitive equilibrium from equal incomes](/competitive-equilibrium-from-equal-incomes/) is the same idea with real goods, and [approximate CEEI](/approximate-ceei/) is the version for indivisible goods used in course allocation.

## When to use it

Use it when agents have cardinal preferences that matter, the market is small or has structure (for example two utility values), and fairness and ex ante efficiency are worth a heavy computation. For large markets, or when only rankings are known, [probabilistic serial](/probabilistic-serial/) or [random serial dictatorship](/random-serial-dictatorship/) are simple and fast. Use the toy on this page only to study small examples.

## Pitfalls

- **Forgetting the cheapest-bundle rule.** Without condition 3 the allocation can waste money on worthless shares and lose Pareto efficiency.
- **Trusting a grid.** A price grid can miss all equilibria, since equilibrium prices can be irrational. A search that finds nothing proves nothing.
- **Floating point.** The demand sets are faces of polytopes, and a small error in $U_i$ or $C_i$ makes the face empty. Compare exactly, or with care.
- **All prices positive.** Normalize so that the smallest price is 0. Without it the same allocation appears at many price vectors, and a search wastes time.
- **Asymmetric answers.** The clearing LP of line L5 returns a vertex, which can be an asymmetric allocation even for identical agents. All such answers are equilibria, but they may look less fair than the symmetric one.

## Implementations

The Python version is a toy and says so. It takes the utility matrix and the grid parameters and returns the first price vector on the grid with a clearing allocation, or None. It uses the shared exact LP helper in Fraction for the demand values and the clearing step, and it has an exact equilibrium checker. The tests check the examples above, the checker on wrong prices, the demand values against a search over the corners of the budget set, and on random instances with 2 agents that every answer is an equilibrium, ex ante Pareto efficient by a linear program over all bistochastic matrices, and envy-free. The 3 agent example is checked at its known prices, because the grid search on 3 objects is too slow for a unit test.

## History

Hylland and Zeckhauser (1979) proposed the pseudo-market for assigning individuals to positions, proved that an equilibrium exists and that its allocation is efficient. It was long seen as the ideal mechanism for one-sided matching with cardinal utilities, but too hard to compute. Vazirani and Yannakakis (2021) started its study in computer science, with irrational equilibria, FIXP and PPAD membership, and algorithms for special utilities. Chen, Chen, Peng and Yannakakis (2022) proved that the approximate problem is PPAD-hard.

## References
