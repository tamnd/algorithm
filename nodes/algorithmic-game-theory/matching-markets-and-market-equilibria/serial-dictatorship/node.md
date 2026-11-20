---
tag: RKCZD9
kind: algorithm
slug: serial-dictatorship
name: Serial dictatorship
aliases:
- priority mechanism
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: intro
summary: Agents pick their favourite remaining object in a fixed order. The result is Pareto optimal, no agent gains by lying, and every Pareto optimal matching comes from some order.
solves: [house-allocation-problem]
model: word-ram
complexity:
  vars: {n: the number of agents, m: the number of objects}
  time: {worst: O(m + n^2)}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1998
  people: [Atila Abdulkadiroglu, Tayfun Sonmez, Lars-Gunnar Svensson]
  note: Priority by seniority is an old practice. Abdulkadiroglu and Sonmez showed in 1998 that every Pareto optimal matching comes from some order, and Svensson characterized the rule in 1999.
prereqs: [house-allocation-problem]
see_also: [random-serial-dictatorship, probabilistic-serial, top-trading-cycles, pareto-optimality, dominant-strategy-incentive-compatibility, school-choice-problem, gale-shapley]
sources:
  - book: isbn:9789814425247
    title: David F. Manlove, Algorithmics of Matching Under Preferences, World Scientific (2013)
    locator: Chapter 6, Pareto optimal matchings, Section 6.2 (house allocation)
  - paper: doi:10.2307/2998580
    title: Atila Abdulkadiroglu and Tayfun Sonmez, Random serial dictatorship and the core from random endowments in house allocation problems, Econometrica 66(3) (1998)
    locator: the lemma that every Pareto efficient matching is the outcome of a serial dictatorship
  - paper: doi:10.1007/s003550050160
    title: Lars-Gunnar Svensson, Strategy-proof allocation of indivisible goods, Social Choice and Welfare 16, 557 to 567 (1999)
    locator: the main theorem (strategyproof, nonbossy and neutral rules are serial dictatorships)
  - paper: doi:10.1007/978-3-540-30551-4_3
    title: David J. Abraham, Katarina Cechlarova, David F. Manlove and Kurt Mehlhorn, Pareto optimality in house allocation problems, ISAAC 2004, LNCS 3341, 3 to 15
    locator: Pareto optimal matchings with incomplete lists and their sizes
---

Serial dictatorship solves the [house allocation problem](/house-allocation-problem/) by a fixed order of the agents: the first agent takes its favourite object, the second takes its favourite among the objects that are left, and so on. Each agent in turn is a dictator over what remains. The result is a [Pareto optimal](/pareto-optimality/) matching, and no agent can get a better object by reporting a false list, so truth-telling is a [dominant strategy](/dominant-strategy-incentive-compatibility/). It runs in $O(m + n^2)$ time for $n$ agents and $m$ objects. The rule is not fair: the first agent always gets its first choice. The fair version draws the order at random, which is [random serial dictatorship](/random-serial-dictatorship/).

## In plain words

The people line up. The first person takes the room they like best. The second person takes the best room that is still free, and so on to the end of the line. A person who finds no acceptable room free gets nothing.

Nobody can do better by lying, because your turn and the rooms left at your turn do not depend on what you say. The answer is never wasteful: to make someone happier you would have to take a room from a person earlier in the line, who would then be unhappier. But the line decides everything, so the first person in line has a large advantage.

## The problem

The input is $n$ agents and $m$ objects. Agent $i$ has a strict list of the objects it accepts, best first, and it prefers any listed object to nothing. An order $\pi$ of the agents is also given. The output is a matching: each agent gets at most one acceptable object, and no object goes to two agents.

## The algorithm

```pseudo id=main
SERIAL-DICTATORSHIP(lists, π)
L1  for each object o do taken[o] ← false
L2  for each agent i do M[i] ← NIL
L3  for k ← 1 to n do
L4      i ← π(k)
L5      for each object o on the list of i, best first do
L6          if not taken[o] then M[i] ← o;  taken[o] ← true;  stop the loop of line L5
L7  return M
```

Line L5 scans the list of agent $i$ from the top and line L6 stops at the first free object. An agent whose list runs out stays unmatched. Nothing else in the algorithm depends on the list of agent $i$, which is the key to its incentive property.

## Example

This is the example of Bogomolnaia and Moulin (2001). Agents 1 and 2 rank $a \succ b \succ c \succ d$, and agents 3 and 4 rank $b \succ a \succ d \succ c$. With the order 1, 2, 3, 4:

| step | agent | free objects before the step | list | takes |
|---|---|---|---|---|
| 1 | 1 | $a, b, c, d$ | $a, b, c, d$ | $a$ |
| 2 | 2 | $b, c, d$ | $a, b, c, d$ | $b$ (after skipping $a$) |
| 3 | 3 | $c, d$ | $b, a, d, c$ | $d$ (after skipping $b$ and $a$) |
| 4 | 4 | $c$ | $b, a, d, c$ | $c$ (after skipping three) |

The matching gives $a, b, d, c$ to agents 1 to 4. Agent 4 reads 4 entries, the most possible for the fourth agent. With the order 1, 3, 2, 4 the result is $a, c, b, d$, and with the order 4, 3, 1, 2 it is $c, d, a, b$. Over all $4! = 24$ orders, serial dictatorship gives 12 different matchings, and a brute force check over all 209 matchings of this instance shows that these 12 are exactly the Pareto optimal ones.

**Edge cases.** With no agents the result is empty. An agent with an empty list gets nothing. If three agents accept only $a$, the first of them in the order gets it and the others get nothing.

## Correctness

The output is a matching, because line L6 gives an agent only a free object and marks it taken. It is Pareto optimal: if a matching $M'$ were at least as good as $M$ for everybody and better for someone, take the first agent $i$ in the order with $M'(i) \ne M(i)$. With strict lists, $M'(i)$ is an object that $i$ ranks above $M(i)$, and it was not free at the turn of $i$, so an earlier agent $j$ holds it in $M$. But $M'(j) = M(j)$ by the choice of $i$, so $M'$ gives the object to both $i$ and $j$, which is impossible.

It is strategyproof: the objects taken before the turn of $i$ depend only on the lists of earlier agents, and with its true list agent $i$ gets its best free object. A false list can only give a free object that $i$ likes less, or nothing.

Every Pareto optimal matching $M$ is the output for some order. In any such $M$, some agent gets its first choice among all objects: otherwise each agent points to the holder of an object it prefers, and either some agent points to an unassigned object, or the pointers contain a cycle along which the agents can trade, and in both cases $M$ is not Pareto optimal. Put that agent first, remove it and its object, and repeat on the rest, where $M$ stays Pareto optimal. The full proofs are in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/); objects are indices, and a test of $\text{taken}[o]$ costs $O(1)$.

- **Initialization.** Lines L1 and L2 cost $O(m + n)$.
- **Scans.** Before the turn of the $k$-th agent, exactly the objects of the earlier agents are taken, at most $k - 1$ of them. So line L5 reads at most $k$ entries of the list before it stops or the list ends. The total over all agents is at most $1 + 2 + \dots + n = n(n + 1)/2$.
- **Total.** $O(m + n^2)$ time and $O(m)$ extra space for the array $\text{taken}$, besides the input and output. When $n \le m$ and the lists are complete, the input has $nm$ entries, so the algorithm does not even read all of it.

## Properties

- **Pareto optimal**, and every Pareto optimal matching arises from some order (Abdulkadiroglu and Sonmez 1998; the proof below also covers incomplete lists).
- **Strategyproof.** Truth-telling is a dominant strategy for every agent.
- **Nonbossy and neutral.** An agent cannot change the objects of others without changing its own, and renaming the objects renames the result. Svensson (1999) proved that a deterministic rule with these two properties and strategyproofness is a serial dictatorship.
- **Not fair.** Two agents with the same list get very different objects, depending only on the order.
- **Not of maximum size.** A Pareto optimal matching can be about half as large as a largest one. If agent 1 accepts $a$ and $b$ and agent 2 accepts only $a$, the order 1, 2 gives one pair and the order 2, 1 gives two.

## Variants and improvements

- **Random order.** [Random serial dictatorship](/random-serial-dictatorship/) draws the order uniformly at random. It treats equal agents equally and stays strategyproof.
- **Ties.** With indifference, an agent cannot just take one object of its top tie class, because the choice inside the tie class can hurt agents later in the order. The fix keeps the choice open: each agent in turn only promises to take one of its best objects that can still be given to it together with the promises of earlier agents, and a bipartite matching at the end fixes the objects. Manlove (2013, Section 6.2.2) treats this case.
- **Copies.** If an object has several copies, an agent takes a copy while one is left; the analysis is the same.
- **Owners.** When agents own the objects at the start, an order of the agents would violate individual rationality. [Top trading cycles](/top-trading-cycles/) is the right rule then.
- **Size.** To get a largest Pareto optimal matching, Abraham, Cechlarova, Manlove and Mehlhorn (2004) start from a maximum matching and improve it, in $O(n^{1/2} |E|)$ time for $|E|$ acceptable pairs.

## When to use it

Use it when a natural priority exists and is accepted as fair: seniority for offices, the time of application for housing, or a lottery number drawn in public. It is simple to explain and to check, and no agent needs to think about strategy. When no priority is accepted, draw it at random, or use [probabilistic serial](/probabilistic-serial/) if ordinal efficiency matters more than full strategyproofness.

## Pitfalls

- **An order that depends on the reports.** The order must be fixed before the lists are read. If, for example, agents who rank popular objects first are moved back in the line, an agent can gain a better place by a false list, and strategyproofness is lost.
- **Breaking ties arbitrarily.** With indifferences, a fixed tie-break inside serial dictatorship can give a matching that is not Pareto optimal. Use the version for ties.
- **Calling it fair because it is efficient.** Efficiency and strategyproofness say nothing about equal treatment; the order decides who wins.
- **Expecting a large matching.** Pareto optimality does not mean that as many agents as possible get an object.

## Implementations

The Python version takes the lists as lists of object indices, best first, and an optional order of the agents, and it returns the object of each agent, with $-1$ for an agent that gets nothing. The tests compare the set of outcomes over all orders with the set of Pareto optimal matchings found by brute force, and check strategyproofness over all false lists, truncated lists included.

## History

Allocation by a priority order, for example by seniority or by the date of application, is an old practice. In the matching literature, Abdulkadiroglu and Sonmez (1998) showed that the Pareto optimal matchings are exactly the outcomes of serial dictatorships, and that a random order gives the same lottery as the core from random endowments. Svensson (1999) characterized serial dictatorship as the only strategyproof, nonbossy and neutral rule. Abraham, Cechlarova, Manlove and Mehlhorn (2004) studied the sizes of Pareto optimal matchings with incomplete lists, and Manlove (2013) gives the algorithmic account.

## References
