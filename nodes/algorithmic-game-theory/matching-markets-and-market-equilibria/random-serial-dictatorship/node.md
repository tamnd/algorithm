---
tag: K05SWB
kind: algorithm
slug: random-serial-dictatorship
name: Random serial dictatorship
aliases:
- RSD
- random priority
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: "Runs serial dictatorship with a uniformly random order of agents. The lottery is fair, strategyproof and ex post efficient, but its exact probabilities are #P-hard to compute."
solves: [house-allocation-problem]
model: word-ram
complexity:
  vars: {n: the number of agents, m: the number of objects}
  time: {worst: O(m + n^2)}
  space: {extra: O(n + m)}
properties: {deterministic: false, randomized: true, recursive: false}
history:
  year: 1998
  people: [Atila Abdulkadiroglu, Tayfun Sonmez]
  note: Lotteries over priority orders are an old practice. Abdulkadiroglu and Sonmez proved in 1998 that the rule gives the same lottery as the core from random endowments.
prereqs: [serial-dictatorship, random-permutation]
see_also: [probabilistic-serial, top-trading-cycles, house-allocation-problem, fisher-yates-shuffle, truthful-in-expectation, birkhoff-von-neumann-decomposition, school-choice-problem, pareto-optimality]
sources:
  - paper: doi:10.2307/2998580
    title: Atila Abdulkadiroglu and Tayfun Sonmez, Random serial dictatorship and the core from random endowments in house allocation problems, Econometrica 66(3) (1998)
    locator: the main theorem (random serial dictatorship equals the core from random endowments)
  - paper: doi:10.1006/jeth.2000.2710
    title: Anna Bogomolnaia and Herve Moulin, A new solution to the random assignment problem, Journal of Economic Theory 100(2), 295 to 328 (2001)
    locator: the random priority mechanism and the example where it is not ordinally efficient
  - paper: doi:10.1287/moor.2014.0707
    title: Daniela Saban and Jay Sethuraman, The complexity of computing the random priority allocation matrix, Mathematics of Operations Research 40(4), 1005 to 1014 (2015)
    locator: "the #P-completeness of the allocation matrix and the NP-completeness of the positive probability test"
  - paper: doi:10.1016/j.econlet.2013.09.006
    title: Haris Aziz, Felix Brandt and Markus Brill, The computational complexity of random serial dictatorship, Economics Letters 121(3), 341 to 345 (2013)
    locator: "the #P-completeness of the RSD probabilities"
  - paper: doi:10.3982/ECTA8354
    title: Yeon-Koo Che and Fuhito Kojima, Asymptotic equivalence of probabilistic serial and random priority mechanisms, Econometrica 78(5), 1625 to 1672 (2010)
    locator: the main theorem (the two assignments converge as the number of copies grows)
---

Random serial dictatorship solves the [house allocation problem](/house-allocation-problem/) with a lottery. It draws an order of the agents uniformly at random and then runs [serial dictatorship](/serial-dictatorship/) in that order: the first agent takes its favourite object, the next agent takes its favourite object that is left, and so on. Bogomolnaia and Moulin call it random priority. Every outcome is [Pareto optimal](/pareto-optimality/), no agent can gain by a false list whatever the draw, and agents with the same list have the same chances. One draw costs $O(m + n^2)$ time for $n$ agents and $m$ objects. The probability that a given agent gets a given object is #P-complete to compute exactly, and the lottery can be ordinally inefficient: [probabilistic serial](/probabilistic-serial/) can give every agent a lottery that it prefers.

## In plain words

Put the names in a hat and draw them one by one. The first name drawn chooses a room, then the second name chooses among the rooms that are left, and so on.

Before the draw, everybody has the same chance to be early, so the rule is fair in the sense that equal people are treated equally. After the draw, it is plain serial dictatorship, so nobody can gain by lying and nothing is wasted. The weakness is in the chances themselves. Two people who rank the rooms in opposite ways can sometimes both improve their chances by swapping some probability, and random serial dictatorship does not do this swap for them.

## The problem

The input is $n$ agents and $m$ objects, with a strict list of acceptable objects for each agent, best first. The output is one matching drawn at random. The object of interest is the random assignment: the $n$ by $m$ matrix $P$ where $P_{io}$ is the probability that agent $i$ gets object $o$.

## The algorithm

```pseudo id=main
RANDOM-SERIAL-DICTATORSHIP(lists)
L1  π ← a uniformly random order of the agents, by the Fisher-Yates shuffle
L2  for each object o do taken[o] ← false
L3  for each agent i do M[i] ← NIL
L4  for k ← 1 to n do
L5      i ← π(k)
L6      for each object o on the list of i, best first do
L7          if not taken[o] then M[i] ← o;  taken[o] ← true;  stop the loop of line L6
L8  return M
```

Line L1 is the only random step. It uses the [Fisher-Yates shuffle](/fisher-yates-shuffle/), so each of the $n!$ orders has probability $1/n!$. Lines L2 to L8 are serial dictatorship.

## Example

This is the example of Bogomolnaia and Moulin (2001). Agents 1 and 2 rank $a \succ b \succ c \succ d$, and agents 3 and 4 rank $b \succ a \succ d \succ c$. The 24 orders give 12 different matchings. The random assignment is:

| agent | $a$ | $b$ | $c$ | $d$ |
|---|---|---|---|---|
| 1 | 5/12 | 1/12 | 5/12 | 1/12 |
| 2 | 5/12 | 1/12 | 5/12 | 1/12 |
| 3 | 1/12 | 5/12 | 1/12 | 5/12 |
| 4 | 1/12 | 5/12 | 1/12 | 5/12 |

To check the first entry: agents 3 and 4 take $b$ before they take $a$. So agent 1 gets $a$ exactly when it comes before agent 2, unless agents 3 and 4 both come before agent 1, in which case they take $b$ and then $a$. The first event has probability $1/2$, and the bad case (3 and 4 first, in either order, then 1, then 2) has probability $2/24$. So $P_{1a} = 1/2 - 1/12 = 5/12$. Agent 1 gets $b$ only for the orders that start with 2 and 1, which is $2/24 = 1/12$.

Now look at the 1/12 entries. Agent 1 has a chance at $b$ and agent 3 has a chance at $a$, but each of them prefers the object of the other. If they swap these shares, and the same for $c$ and $d$, every agent gets $\{a: 1/2, c: 1/2\}$ or $\{b: 1/2, d: 1/2\}$. This is the [probabilistic serial](/probabilistic-serial/) assignment. Each agent prefers it in the sense of stochastic dominance (defined under Properties), so random serial dictatorship is not ordinally efficient here.

**Edge cases.** With one agent, it takes its top object with probability 1. If three agents accept only $a$, each gets it with probability $1/3$. An agent with an empty list always gets nothing.

## Correctness

Each outcome is the output of serial dictatorship for some order, so it is a matching and it is Pareto optimal. The converse also holds: every Pareto optimal matching is the output of some order (see [serial dictatorship](/serial-dictatorship/)), so the support of the lottery is exactly the set of Pareto optimal matchings.

Strategyproofness holds order by order. For a fixed order, the objects taken before the turn of agent $i$ do not depend on its list, and with its true list it gets its best free object. So for every order, the true list gives $i$ an object at least as good as any false list does. Summing over the orders, for every $k$ the truth gives a probability at least as large of an object among the $k$ best. This is strategyproofness in the sense of stochastic dominance. It implies [truthfulness in expectation](/truthful-in-expectation/) for every utility function that agrees with the true list.

Equal treatment of equals: if agents $i$ and $j$ have the same list, swapping $i$ and $j$ in the order is a bijection of the orders that swaps their objects, so their rows of $P$ are equal. The proof file below gives the details.

## Complexity

- **One draw.** Line L1 costs $O(n)$ time and $n - 1$ random integers. Lines L2 to L8 cost $O(m + n^2)$, as for [serial dictatorship](/serial-dictatorship/): the $k$-th agent reads at most $k$ entries of its list. The extra space is $O(n + m)$.
- **The exact matrix.** Running all $n!$ orders gives $P$ in $O(n! (m + n^2))$ time, which is what the tests do for $n \le 5$. No polynomial method is expected: Saban and Sethuraman (2015) proved that computing the matrix is #P-complete, and that deciding if a given agent gets a given object with positive probability is NP-complete, while the test for probability 1 is polynomial. Aziz, Brandt and Brill (2013) proved #P-completeness of the RSD probabilities in voting and assignment settings.
- **Estimates.** Each entry of $P$ is an average of indicator variables over random orders, so $s$ independent draws estimate all entries within $\varepsilon$ with probability at least $1 - \delta$ when $s \ge \ln(2nm/\delta)/(2\varepsilon^2)$, by the [Hoeffding inequality](/hoeffding-inequality/) and a union bound.

## Properties

- **Ex post efficient.** Every outcome is Pareto optimal.
- **Strategyproof** in the strong sense: it is a lottery over strategyproof deterministic rules, so truth-telling is dominant after the draw, not only on average.
- **Equal treatment of equals** and anonymity: the result does not depend on the names of the agents.
- **Not ordinally efficient.** An assignment $Q$ stochastically dominates $P$ for agent $i$ if, for every $k$, $Q$ gives $i$ at least as much probability of one of its $k$ best objects. In the example, the probabilistic serial matrix dominates the RSD matrix for every agent and is different from it.
- **The core from random endowments.** Abdulkadiroglu and Sonmez (1998) showed that if the $n$ houses are first given to the $n$ agents by a uniform random endowment and the agents then trade by [top trading cycles](/top-trading-cycles/), the lottery over matchings is the same as that of random serial dictatorship. The tests check this on all endowments for $n \le 4$.
- **Bistochastic.** With $n = m$ and complete lists, every agent gets an object and every object is given, so the rows and the columns of $P$ sum to 1.

## Variants and improvements

- **Probabilistic serial.** [Probabilistic serial](/probabilistic-serial/) is ordinally efficient and envy-free, but it is only weakly strategyproof. Bogomolnaia and Moulin (2001) showed that, for $n \ge 4$, no rule has ordinal efficiency, strategyproofness and equal treatment of equals together, so a choice between RSD and PS is necessary.
- **Large markets.** Che and Kojima (2010) showed that when each object has many copies, the RSD and PS assignments get close, so the inefficiency of RSD vanishes in large markets.
- **Copies.** If an object has several copies, an agent takes a copy while one is left. The properties above stay true.
- **Tie-breaking in school choice.** In [school choice](/school-choice-problem/) with coarse priorities, one random order of the students often breaks the ties at all schools. This is the same idea, applied inside another mechanism.
- **Implementing a matrix.** A random assignment matrix of another rule can be turned into a lottery over matchings by the [Birkhoff-von Neumann decomposition](/birkhoff-von-neumann-decomposition/). RSD does not need this step, since it draws the matching directly.

## When to use it

Use it when no priority is accepted as fair and strategyproofness must hold without any doubt: university housing, course seats, public housing and the allocation of slots by a public lottery. It is easy to explain and to audit, since the order can be drawn in public. If the efficiency of the probabilities matters more, and the agents are many or not strategic, consider [probabilistic serial](/probabilistic-serial/).

## Pitfalls

- **Computing the matrix by formula.** A program that must report each agent's probabilities exactly faces a #P-complete problem. Sample, or enumerate the orders for small $n$.
- **A biased order.** Shuffles that sort by random keys with ties, or that swap with a uniform position in the whole array at every step, do not give uniform orders. Use the Fisher-Yates shuffle as in line L1.
- **Believing ex post efficiency is enough.** Each outcome is Pareto optimal, but the lottery as a whole can be dominated, as the example shows.
- **Equal chances are not equal results.** The rule is fair before the draw only. After the draw, the first agent still gets its top choice and the last may get nothing, so the draw must be seen as fair by the agents, for example done in public.

## Implementations

The Python version has three functions. random_serial_dictatorship draws one matching from a given random.Random. rsd_lottery and rsd_probabilities enumerate all $n!$ orders and return the exact lottery and the exact matrix in Fraction. The tests check the example matrix, that the support is exactly the set of Pareto optimal matchings found by brute force, strategyproofness in the sense of stochastic dominance against every possible list (truncations included) for 3 agents and 3 objects, equal treatment, the equality with the core from random endowments, and the sampler frequencies with a fixed seed.

## History

Lotteries over a priority order are an old way to allocate housing and other goods. Abdulkadiroglu and Sonmez (1998) gave the rule its name in the matching literature and proved that it coincides with the core from random endowments. Bogomolnaia and Moulin (2001) called it random priority, showed by the example above that it is not ordinally efficient, and proposed probabilistic serial in its place. Che and Kojima (2010) showed that the two rules agree in large markets. Aziz, Brandt and Brill (2013) and Saban and Sethuraman (2015) proved that the exact probabilities are #P-complete to compute.

## References
