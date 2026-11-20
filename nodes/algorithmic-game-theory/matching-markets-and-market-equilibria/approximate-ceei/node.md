---
tag: DWVSMG
kind: algorithm
slug: approximate-ceei
name: Approximate competitive equilibrium from equal incomes
aliases:
- A-CEEI
- Budish course allocation mechanism
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: research
summary: Gives agents slightly unequal budgets so that an approximate equilibrium exists for indivisible goods. It is used for course allocation.
model: real-ram
complexity:
  vars: {n: the number of agents, m: the number of goods, g: the number of grid prices per good, l: the length of the longest preference list}
  time: {worst: "O(g^m n l m)"}
  space: {extra: O(n m)}
properties: {deterministic: true, recursive: false}
history:
  year: 2011
  people: [Eric Budish]
  note: Budish proved that an approximate CEEI exists for any preferences over bundles of indivisible goods. Othman, Sandholm and Budish gave a heuristic price search, and Othman, Papadimitriou and Rubinstein proved that the problem is PPAD-complete.
prereqs: [competitive-equilibrium-from-equal-incomes, indivisible-goods-allocation]
see_also: [envy-freeness-up-to-one-good, maximin-share, combinatorial-auction, kakutani-fixed-point-theorem, ppad, tatonnement, tabu-search, random-serial-dictatorship]
sources:
  - paper: doi:10.1086/664613
    title: "Eric Budish, The combinatorial assignment problem: approximate competitive equilibrium from equal incomes, Journal of Political Economy 119(6), 1061-1103 (2011)"
    locator: the whole paper (the existence theorem for approximate CEEI and the fairness and incentive properties of the mechanism)
  - paper: doi:10.5555/1838206.1838323
    title: "Abraham Othman, Tuomas Sandholm and Eric Budish, Finding approximate competitive equilibria: efficient and fair course allocation, AAMAS 2010, 873-880"
    locator: the whole paper (a tabu search over prices, with demands computed by integer programs)
  - paper: doi:10.1145/2956583
    title: "Abraham Othman, Christos Papadimitriou and Aviad Rubinstein, The complexity of fairness through equilibrium, ACM Transactions on Economics and Computation 4(4), Article 20 (2016)"
    locator: the whole paper (computing the A-CEEI of Budish's theorem is PPAD-complete, and a better approximation is NP-hard)
  - url: https://arxiv.org/abs/1312.6249
    title: "Abraham Othman, Christos Papadimitriou and Aviad Rubinstein, The complexity of fairness through equilibrium, arXiv 1312.6249 (version of EC 2014)"
    locator: "Definition 2 (clearing error), Definition 3 ((alpha, beta)-CEEI), Theorem 1 (Budish's existence theorem), Theorem 2 (PPAD-completeness), Theorem 3 (NP-hardness)"
---

Approximate competitive equilibrium from equal incomes, or A-CEEI, is Budish's answer to a problem of the [competitive equilibrium from equal incomes](/competitive-equilibrium-from-equal-incomes/) (CEEI): with [indivisible goods](/indivisible-goods-allocation/) such as seats in courses, a CEEI often does not exist. A-CEEI changes two things. The budgets are made slightly unequal, all in $[1, 1 + \beta]$ for a small $\beta > 0$, and the market only has to clear approximately: the clearing error $\alpha$, the length of the vector of oversubscribed and unfilled seats, has to be small. Budish proved that for any preferences over bundles, an A-CEEI exists with $\alpha \le \sqrt{\sigma m} / 2$, a bound that does not grow with the number of agents. It is used in practice to assign business school students to courses. Finding it is PPAD-complete, so real systems search for prices heuristically. The implementation on this page is a toy that tries every price vector on a grid.

## In plain words

Every student gets almost the same amount of fake money, but no two students get exactly the same amount. Each course seat gets a price. At these prices, every student takes the best schedule she can pay for. If too many students want a course, its price is too low; if a course with a positive price has empty seats, its price is too high. The goal is prices at which every course is about full. With exactly equal money this can be impossible: if two students want the one seat of a course, either both can pay for it or neither can. Tiny differences in money break these ties, and then prices that almost clear the market always exist.

## The problem

There are $n$ agents and $m$ goods, with $q_j$ identical seats of good $j$. Agent $i$ accepts some bundles of goods, ranked by a strict order, and the empty bundle is always acceptable; $k$ is the largest size of an accepted bundle. Agent $i$ has a budget $b_i$. At prices $p \in \mathbb{R}^m_{\ge 0}$, the *demand* $x_i(p)$ of agent $i$ is her highest ranked bundle with $\sum_{j \in x_i} p_j \le b_i$. The *clearing error* of $p$ is $\alpha = \|z\|_2$ with
$$
z_j = \begin{cases} \#\{i : j \in x_i(p)\} - q_j & \text{if } p_j > 0, \\ \max(\#\{i : j \in x_i(p)\} - q_j, \, 0) & \text{if } p_j = 0, \end{cases}
$$
so empty seats count against a good only if it has a positive price. Prices with $\alpha = 0$ and equal budgets are a CEEI. An *$(\alpha, \beta)$-CEEI* is a vector of budgets in $[1, 1 + \beta]$ with prices whose clearing error is at most $\alpha$, where every agent gets her demand. The task is to find one with small $\alpha$.

## The algorithm

The toy fixes the budgets and searches a grid of prices with step $s$ and largest price $c$.

```pseudo id=main
A-CEEI-GRID(preference lists, seats q, budgets b, step s, cap c)
L1  best ← none
L2  for each p in {0, s, 2s, ..., c}^m, in lexicographic order do
L3      x_i ← the first bundle on the list of agent i that costs at most b_i at p, or the empty bundle
L4      z_j ← (the number of agents with j in x_i) - q_j, raised to 0 if p_j = 0 and it is negative
L5      if best is none or ||z||² < the error of best then best ← (||z||², p, x)
L6  return the square root of the error of best, its prices and its bundles
```

Line L3 computes each agent's demand by walking her list from the top. Line L4 is the clearing error vector, and line L5 keeps the first price vector with the smallest error. All arithmetic is in exact fractions, so the comparisons of line L3 are exact. The implementation also gives the budgets $1, 1 + \beta/n, \ldots, 1 + (n - 1)\beta/n$, which are distinct and lie in $[1, 1 + \beta)$, and Budish's bound $\sqrt{\sigma m}/2$.

Practical solvers do not search a grid. The method of Othman, Sandholm and Budish moves prices in the direction of the clearing error, as in [tatonnement](/tatonnement/), within a [tabu search](/tabu-search/), and computes each student's demand with an integer program.

## Example

**One seat, two agents.** Both agents want the single seat of good 1. With equal budgets $1$, a price of at most $1$ makes both demand it ($z = 1$), and a higher price makes neither demand it ($z = -1$, since the price is positive), so every price has $\alpha = 1$ and there is no CEEI. With budgets $1$ and $11/10$, any price in $(1, 11/10]$ gives the seat to agent 2 alone and $\alpha = 0$. The toy with step $1/20$ returns $p = 21/20$. Here $k = m = 1$, so Budish's bound is $\sqrt{1}/2 = 1/2$; since $z$ is an integer vector, the theorem promises budgets in $[1, 1 + \beta]$ at which some price clears the market exactly.

**Three students and two courses.** Course 1 has one seat and course 2 has three seats. All three students rank $\{1, 2\}$ first, then $\{1\}$, then $\{2\}$.

| budgets | grid step | best prices $(p_1, p_2)$ | bundles of students 1, 2, 3 | $\alpha$ |
|---|---|---|---|---|
| $(1, 1, 1)$ | $1/8$ | any | the same for all three students | $1$ |
| $(1, 11/10, 6/5)$ | $1/40$ | $(9/8, 0)$ | $\{2\}, \{2\}, \{1, 2\}$ | $0$ |

With equal budgets the three students always demand the same bundle, so course 1 is either taken by all three or by none, and the error is at least $1$. With the budgets $(1, 11/10, 6/5)$, the price $9/8$ for course 1 is above the budgets of students 1 and 2 but within the budget of student 3, and course 2 is free. Student 3 buys $\{1, 2\}$, the others buy $\{2\}$, and both courses are exactly full. Here $k = 2$, $m = 2$, $\sigma = 2$, and the bound is $1$.

## Correctness

The proof for the toy is in `proofs/correctness.md`. Every returned bundle is the demand of its agent at the returned prices, the returned $\alpha$ is the smallest clearing error over the grid, and the search ends because the grid is finite. So the output is an $(\alpha, \beta)$-CEEI for the given budgets, and no grid price does better. The toy does not prove Budish's theorem; a grid can miss the prices that the theorem promises when the step is too coarse. The proof also shows the two statements of the example: with equal budgets and one wanted seat no price clears, and with distinct budgets a price between them does.

**Budish's theorem.** For any $\beta > 0$ and any preferences, there are budgets in $[1, 1 + \beta]$ and prices with clearing error at most $\sqrt{\sigma m}/2$, where $\sigma = \min(2k, m)$. Othman, Papadimitriou and Rubinstein restate it with the bound $\sqrt{km/2}$, which is the same as $\sqrt{2km}/2$. The proof is not constructive: it relies on the [Kakutani fixed point theorem](/kakutani-fixed-point-theorem/).

## Complexity

The toy tries $g^m$ price vectors, where $g = c/s + 1$, and for each it reads every preference list, with bundles of up to $m$ goods. That is $O(g^m n l m)$ time and $O(nm)$ extra space, which is exponential in $m$. This is why it is a toy. In general the problem is hard: Othman, Papadimitriou and Rubinstein showed that computing an A-CEEI with the guarantee of Budish's theorem is PPAD-complete, and that it is NP-hard to tell an economy with an exact CEEI from one with no A-CEEI whose error is below a constant times $\sqrt{n + m}$. In the course allocation setting, also each demand query is an optimization over schedules, solved with [mixed integer programming](/mixed-integer-programming/).

## Properties

- **Approximately efficient.** Every agent gets her best affordable bundle, so the loss comes from the clearing error. The error bound does not grow with the number of agents, so in a large market it is small compared with the supply.
- **Approximately fair.** Because the budgets differ by at most $\beta$, Budish shows two fairness criteria: envy is bounded by a single good (a guarantee of the [EF1](/envy-freeness-up-to-one-good/) type), and every agent gets at least her $(n + 1)$-[maximin share](/maximin-share/).
- **Strategyproof in large markets.** An agent who is small compared with the market cannot change the prices, so she can do no better than report her true preferences.
- **Unequal budgets are essential.** With exactly equal budgets, agents with the same preferences always demand the same bundle, as in the example.
- **The bound is close to tight.** Budish shows economies where the error must be of order $\sqrt{km}$.

## Variants and improvements

- **Course Match.** Budish, Cachon, Kessler and Othman built Course Match, a large scale implementation of A-CEEI for course allocation at business schools, on top of a heuristic price search.
- **Divisible goods.** With divisible goods and equal budgets, an exact CEEI exists, and for additive utilities it is the [maximum Nash welfare](/maximum-nash-welfare/) allocation.
- **Other mechanisms.** [Random serial dictatorship](/random-serial-dictatorship/) is simpler and strategyproof but less fair ex post, and [combinatorial auctions](/combinatorial-auction/) use real money instead of equal budgets.

## When to use it

Use A-CEEI when agents with almost equal rights must share indivisible goods with limited seats, preferences over bundles matter (schedules, shifts, slots), and money cannot be used, as in course allocation. Use the toy only to check the definitions on very small instances. For real instances, use a heuristic price search with an exact demand oracle, and accept a small clearing error.

## Pitfalls

- Using equal budgets in line L3 can make the best error stay large, as in the example; the budgets must be distinct.
- Counting the empty seats of a free good as error in line L4 is wrong: a good with price $0$ may have empty seats.
- Using floating point in line L3 makes the test of affordability fail for bundles that cost exactly the budget; the toy uses exact fractions.
- A grid step in line L2 that is coarser than the differences between budgets can miss every price that separates the agents. In the example with three students and budgets $(1, 11/10, 6/5)$, step $1/4$ jumps from $1$ to $5/4$ over the interval $(11/10, 6/5]$, and the best error on the grid is $1$.
- Taking the smallest error in line L5 as the answer of Budish's theorem is wrong: the grid optimum can be larger than the bound $\sqrt{\sigma m}/2$ when the grid is too coarse.

## Implementations

## History

Varian (1974) proposed the competitive equilibrium from equal division as a fair allocation of divisible goods. For indivisible goods, Budish first presented the A-CEEI mechanism in a working paper of 2009 and published it in 2011, with course allocation at business schools as the main application. Othman, Sandholm and Budish built a heuristic solver for real course allocation data in 2010. Othman, Papadimitriou and Rubinstein showed in 2014, in a journal version of 2016, that finding the approximate equilibrium of Budish's theorem is PPAD-complete. The mechanism is in use for assigning business school students to classes.

## References
