---
tag: VY2D6A
kind: algorithm
slug: probabilistic-serial
name: Probabilistic serial
aliases:
- eating algorithm
- Bogomolnaia-Moulin mechanism
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: Agents eat their favourite remaining objects at equal speed, and the amounts eaten are the assignment probabilities. It is ordinally efficient and envy-free but not strategyproof.
solves: [house-allocation-problem]
model: word-ram
complexity:
  vars: {n: the number of agents, m: the number of objects}
  time: {worst: O(m (n + m))}
  space: {extra: O(n m)}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 2001
  people: [Anna Bogomolnaia, Herve Moulin]
  note: Bogomolnaia and Moulin defined ordinal efficiency and the eating algorithm in 2001. Katta and Sethuraman extended it to preferences with ties in 2006.
prereqs: [house-allocation-problem, random-serial-dictatorship]
see_also: [random-serial-dictatorship, serial-dictatorship, birkhoff-von-neumann-decomposition, envy-freeness, hylland-zeckhauser-mechanism, pareto-optimality, truthful-in-expectation, school-choice-problem]
sources:
  - paper: doi:10.1006/jeth.2000.2710
    title: Anna Bogomolnaia and Herve Moulin, A new solution to the random assignment problem, Journal of Economic Theory 100(2), 295 to 328 (2001)
    locator: the definitions of ordinal efficiency and of the simultaneous eating algorithms, the probabilistic serial mechanism and the impossibility result
  - paper: doi:10.1016/j.jet.2005.05.001
    title: Akshay-Kumar Katta and Jay Sethuraman, A solution to the random assignment problem on the full preference domain, Journal of Economic Theory 131(1), 231 to 250 (2006)
    locator: the extension of probabilistic serial to preferences with ties
  - paper: doi:10.3982/ECTA8354
    title: Yeon-Koo Che and Fuhito Kojima, Asymptotic equivalence of probabilistic serial and random priority mechanisms, Econometrica 78(5), 1625 to 1672 (2010)
    locator: the main theorem (the two assignments converge as the number of copies grows)
---

Probabilistic serial solves the [house allocation problem](/house-allocation-problem/) with a random assignment instead of a single matching. Think of each object as one unit of a divisible good, the probability of getting it. All agents start at time 0 and eat at the same speed. Each agent eats from its favourite object that is not used up, and moves to the next one on its list when that object runs out. At time 1 the amount of object $o$ that agent $i$ has eaten is the probability that $i$ gets $o$. Bogomolnaia and Moulin (2001) proved that the result is ordinally efficient and envy-free in the sense of stochastic dominance, which [random serial dictatorship](/random-serial-dictatorship/) is not. The price is incentives: an agent can sometimes gain in expected utility by a false list. With exact rational arithmetic the algorithm takes $O(m(n + m))$ time for $n$ agents and $m$ objects.

## In plain words

Imagine each room as a cake. A bell rings, and everybody starts to eat from the cake of the room they like most, all at the same speed. When a cake is finished, the people who were eating it move to the best cake that is still there. After one unit of time the bell rings again. The share of a cake you ate is your chance to get that room.

Nobody envies another person's plate, because at every moment you were eating the best cake left. And no trade of chances can make everybody happier. The catch is that a person can sometimes gain by pretending to like a contested room less and eating an uncontested one first.

## The problem

The input is $n$ agents and $m$ objects, each agent with a strict list of the objects it accepts, best first. The output is a random assignment: an $n$ by $m$ matrix $P \ge 0$ with row sums at most 1 and column sums at most 1, where $P_{io}$ is the probability that agent $i$ gets object $o$, and $P_{io} = 0$ if $i$ does not accept $o$. When $n = m$ and the lists are complete, $P$ is bistochastic, and the [Birkhoff-von Neumann decomposition](/birkhoff-von-neumann-decomposition/) turns it into a lottery over matchings.

For agent $i$, a row $p$ stochastically dominates a row $q$ if, for every $k$, $p$ gives at least as much probability as $q$ to the set of the $k$ best objects of $i$. The assignment $P$ is ordinally efficient if no other random assignment gives every agent a row that dominates its row in $P$, and a different row to at least one agent.

## The algorithm

```pseudo id=main
PROBABILISTIC-SERIAL(lists)
L1  for each object o do left[o] ← 1
L2  for each agent i and object o do P[i][o] ← 0
L3  t ← 0
L4  while t < 1 do
L5      for each agent i do top[i] ← the first object on the list of i with left > 0, or NIL
L6      if every top[i] is NIL then stop the loop of line L4
L7      for each object o do eaters[o] ← the number of agents i with top[i] = o
L8      δ ← min(1 - t, min of left[o] / eaters[o] over the objects o with eaters[o] > 0)
L9      for each agent i with top[i] ≠ NIL do P[i][top[i]] ← P[i][top[i]] + δ;  left[top[i]] ← left[top[i]] - δ
L10     t ← t + δ
L11 return P
```

The algorithm jumps from event to event. Between two events no agent changes its object, so each object $o$ shrinks at rate eaters[o], and line L8 finds the time until the first object runs out or the clock reaches 1. All numbers are rationals, and the implementation computes them exactly.

## Example

Agent 1 ranks $a \succ b \succ c$, agent 2 ranks $a \succ c \succ b$, and agent 3 ranks $b \succ a \succ c$.

| interval | agent 1 eats | agent 2 eats | agent 3 eats | event at the end |
|---|---|---|---|---|
| $[0, 1/2]$ | $a$ | $a$ | $b$ | $a$ is used up: two eaters, $1/2$ each |
| $[1/2, 3/4]$ | $b$ | $c$ | $b$ | $b$ is used up: $1/2$ was left, two eaters |
| $[3/4, 1]$ | $c$ | $c$ | $c$ | $c$ is used up and $t = 1$ |

The result is

| agent | $a$ | $b$ | $c$ |
|---|---|---|---|
| 1 | 1/2 | 1/4 | 1/4 |
| 2 | 1/2 | 0 | 1/2 |
| 3 | 0 | 3/4 | 1/4 |

Agent 3 eats $b$ for the whole interval $[0, 3/4]$ and $c$ after that. Agent 1 does not envy agent 3: under the list of agent 1, its own row gives $1/2$ to $\{a\}$ against $0$, $3/4$ to $\{a, b\}$ against $3/4$, and $1$ to everything against $1$.

In the example of Bogomolnaia and Moulin, where agents 1 and 2 rank $a \succ b \succ c \succ d$ and agents 3 and 4 rank $b \succ a \succ d \succ c$, probabilistic serial gives agents 1 and 2 half of $a$ and half of $c$, and agents 3 and 4 half of $b$ and half of $d$. [Random serial dictatorship](/random-serial-dictatorship/) gives agent 1 the row $(5/12, 1/12, 5/12, 1/12)$, which is dominated.

**A manipulation.** Let agents 1 and 2 rank $a \succ b \succ c$ and agent 3 rank $b \succ c \succ a$. With the truth, agent 1 gets $(1/2, 1/6, 1/3)$ for $(a, b, c)$. If agent 1 reports $b \succ a \succ c$, it eats $b$ together with agent 3 first and gets $(1/4, 1/2, 1/4)$. With utilities $3$, $2.9$ and $0$, the lie raises its expected utility from about $1.98$ to $2.2$. The false row does not dominate the true one (it gives less probability to $\{a\}$), which is the weak form of strategyproofness that probabilistic serial has.

**Edge cases.** If three agents accept only $a$, each gets $1/3$ of it. With more objects than agents, eating stops at time 1, and objects can stay partly uneaten. An agent whose list runs out stops eating, and its row sums to less than 1.

## Correctness

The output is a random assignment: each object starts with one unit and line L8 never lets left[o] go below 0, so the column sums are at most 1; each agent eats for at most one unit of time, so the row sums are at most 1. Agents eat only acceptable objects.

**Envy-freeness.** Fix agents $i$ and $j$ and the set $B_k$ of the $k$ best objects of $i$. While some object of $B_k$ is left, agent $i$ eats from $B_k$. So until the last object of $B_k$ is used up, at time $t_k$, agent $i$ eats from $B_k$ at speed 1 and agent $j$ eats from it at speed at most 1, and after $t_k$ nobody eats from $B_k$. Hence $i$ has at least as much of $B_k$ as $j$, for every $k$.

**Ordinal efficiency.** Suppose an assignment $Q$ gives every agent a row that dominates its row in $P$. Go through the objects in the order in which they are used up. The agents who eat an object $o$ at the moment it runs out have eaten only objects they like at least as much as $o$, and all of these are used up by then, so their whole eating time went into this top set. Domination forces each of them to get at least as much of $o$ in $Q$ as in $P$, given that $Q$ and $P$ agree on the objects used up earlier. Since $P$ gives out all of $o$, $Q$ must agree with $P$ on $o$. At the end, the same argument for the objects still left at time 1 shows $Q = P$. The proof file below gives the details. Bogomolnaia and Moulin also characterize ordinal efficiency by the absence of a cycle in a relation on the objects.

**Weak strategyproofness.** No false list gives a row that dominates the true row unless the two rows give the same probability to each top set. Bogomolnaia and Moulin also proved that, for $n \ge 4$, no rule has ordinal efficiency, strategyproofness in the sense of stochastic dominance and equal treatment of equals together, so the gap cannot be closed.

## Complexity

The model is the [word RAM](/word-ram/) with exact rational arithmetic; each event involves fractions whose sizes grow with the number of events.

- **Events.** Each pass of the loop of line L4 except the last uses up at least one object, the one that gives the minimum in line L8. So there are at most $m + 1$ passes.
- **Work per pass.** Lines L7 to L10 cost $O(n + m)$. For line L5, each agent keeps a pointer into its list that only moves forward, because a used-up object never comes back. The pointer moves cost $O(nm)$ in total over all passes.
- **Total.** $O(m(n + m) + nm) = O(m(n + m))$ arithmetic operations, and $O(nm)$ space for the matrix. The output itself has $nm$ entries.

## Properties

- **Ordinally efficient**, so also ex post efficient: the matrix can be written as a lottery over Pareto optimal matchings.
- **Envy-free** in the sense of stochastic dominance, which implies equal treatment of equals.
- **Weakly strategyproof** but not strategyproof: a false list never gives a dominating row, but it can raise the expected utility, as the manipulation above shows.
- **Every ordinally efficient assignment is an eating outcome.** Bogomolnaia and Moulin showed that, with complete lists and $n = m$, the ordinally efficient assignments are exactly the outcomes of simultaneous eating algorithms with some eating speeds that may vary over time. Probabilistic serial is the case of equal constant speeds.
- **Large markets.** Che and Kojima (2010) showed that, as each object gets more and more copies, the probabilistic serial and random serial dictatorship assignments converge to each other.

## Variants and improvements

- **Ties.** Katta and Sethuraman (2006) extended the rule to preferences with indifferences. The eating step then becomes a sequence of parametric flow problems, because an agent indifferent between several objects may eat from any of them.
- **Copies and quotas.** If object $o$ has $q_o$ copies, start with left[o] $= q_o$. In school choice, a student eats seats at its preferred schools.
- **Unequal speeds.** Eating at speed $w_i$ gives a weighted version, with envy-freeness replaced by a weighted condition.
- **Implementing the lottery.** For $n = m$ with complete lists, the [Birkhoff-von Neumann decomposition](/birkhoff-von-neumann-decomposition/) writes $P$ as a convex combination of at most $(n - 1)^2 + 1$ permutation matrices, and drawing one of them gives a matching with the right marginals.
- **Cardinal utilities.** With utilities instead of lists, the [Hylland-Zeckhauser mechanism](/hylland-zeckhauser-mechanism/) gives an ex ante efficient assignment by prices, at a much higher computational cost.

## When to use it

Use it when objects are assigned by lottery, ordinal efficiency and fairness matter, and the agents have little room or skill for strategy: course seats, school places, tasks among workers, or the assignment of offices. In small markets with strategic agents, [random serial dictatorship](/random-serial-dictatorship/) is safer because it is fully strategyproof. In large markets the two rules give almost the same result.

## Pitfalls

- **Floating point.** Event times are differences and quotients of earlier ones. Floats can leave a tiny positive amount of an object that should be used up, and then an agent eats a crumb of it in an extra event. Use exact fractions, or compare with a tolerance and round at the end.
- **Recomputing top choices from the start of each list.** Without pointers, line L5 costs $O(nm)$ per pass and the total becomes $O(nm^2)$.
- **Reporting the matrix as the result.** The agents get objects, not probabilities. A lottery that implements the matrix is needed, and for incomplete lists or $n \ne m$ the decomposition works on a sub-bistochastic matrix padded with dummy agents or objects.
- **Selling it as strategyproof.** It is not. Agents with good information about others can gain by misreporting in small markets.

## Implementations

The Python version takes the lists as lists of object indices, best first, and returns the matrix of Fractions. The tests check the two examples above, the manipulation, and on random instances (complete and incomplete lists) the row and column sums, envy-freeness in the sense of stochastic dominance, and ordinal efficiency by an exact linear program with agtlp: maximize the total of the top-set probabilities over all assignments that dominate the result, and check that the maximum equals the value of the result. The same program shows that the random serial dictatorship matrix of the Bogomolnaia and Moulin example is dominated. An exhaustive test over all profiles and all false lists (truncations included) for 3 agents and 3 objects checks weak strategyproofness.

## History

Bogomolnaia and Moulin (2001) introduced ordinal efficiency, showed with their four-agent example that random priority (random serial dictatorship) is not ordinally efficient, and defined the probabilistic serial mechanism with its family of simultaneous eating algorithms. Katta and Sethuraman (2006) extended it to the full preference domain with ties. Che and Kojima (2010) proved that it and random priority become equivalent in large markets, which explains why the simpler random priority works well in practice.

## References
