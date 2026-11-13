---
tag: N54CF6
kind: technique
slug: rollout-algorithm
name: Rollout algorithm
aliases:
- rollouts
- Monte Carlo rollouts
area: games-and-search/game-tree-search
level: advanced
summary: Improves a base heuristic policy by simulating it from each candidate move and choosing the best average result.
prereqs: [markov-decision-process, policy-improvement-theorem, greedy-algorithm, monte-carlo-policy-evaluation]
see_also: [monte-carlo-tree-search, uct, policy-iteration, nearest-neighbor-heuristic, traveling-salesman-problem, bellman-equation, rapid-action-value-estimation, hoeffding-inequality]
sources:
  - paper: doi:10.1023/A:1009635226865
    title: "Dimitri P. Bertsekas, John N. Tsitsiklis and Cynara Wu, Rollout algorithms for combinatorial optimization, Journal of Heuristics 3(3) (1997), 245-262"
    locator: Section 2 (the rollout algorithm RH, Eq. 7, Example 1 on a rollout that does not terminate, Definition 1 of a sequentially consistent heuristic, Proposition 1 on cost improvement), the interpretation as one step of policy iteration, Section 4 (Definition 2 of a sequentially improving heuristic, Proposition 2, and the extended, optimized and fortified rollout algorithms), and the machine repair example
  - book: "M. C. Mozer, M. I. Jordan and T. Petsche (eds.), Advances in Neural Information Processing Systems 9 (NIPS 1996), MIT Press, 1997"
    title: "Gerald Tesauro and Gregory R. Galperin, On-line policy improvement using Monte-Carlo search"
    locator: pp. 1068 to 1074 (Monte Carlo rollouts of a backgammon program used to choose its moves online)
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Chapter 8 (planning at decision time, rollout algorithms and Monte Carlo tree search)
---

A rollout algorithm is a technique that turns a base policy, a heuristic that can complete any partial solution or play any position to the end, into a better policy. At each step it tries every candidate action, runs the base policy from the result to the end (a rollout), and takes the action whose rollouts give the best result. With random outcomes, each action gets several simulated rollouts and their mean is used. In terms of dynamic programming and the [Bellman equation](/bellman-equation/), the rollout policy is one step of [policy iteration](/policy-iteration/) from the base policy, computed only at the states that are actually reached. Bertsekas, Tsitsiklis and Wu (1997) analyzed it for combinatorial optimization, and the name comes from the Monte Carlo backgammon work of Tesauro and Galperin.

## In plain words

Suppose you have a simple rule for making decisions, such as "always go to the nearest city not yet visited". It is fast but not very good. To make a better decision now, try each possible next step, and from each one finish the job with your simple rule. See which first step led to the best final result, and take that step. Then repeat the same thing at the next step.

If the world is random, finish each trial several times and take the average. Your new way of deciding is never much worse than your simple rule, and is usually better, because it looks at the real consequences of each step instead of guessing them.

## When it applies

- There is a base policy that can finish any partial solution or play any state to the end, and running it is cheap enough to repeat many times per decision.
- There is a model or simulator, so that you can try an action and see the result without acting in the real world.
- The problem is sequential: a solution is built one decision at a time, as in a tour, a schedule, a game or a finite-horizon [MDP](/markov-decision-process/).
- The decision is made online, at the states that occur, so computing a whole new policy offline is not needed.

## The template

```pseudo id=main
ROLLOUT-STEP(s, π, m)
L1  for each action a available at s
L2    repeat m times: apply a at s, then follow the base policy π to the end, and record the total cost
L3    Q̂(s, a) ← the mean of the m costs
L4  return the action a with the smallest Q̂(s, a)

ROLLOUT(s_0, π, m)
L5  s ← s_0
L6  while s is not terminal: a ← ROLLOUT-STEP(s, π, m); apply a to s
```

For a deterministic problem $m = 1$, and $\hat Q(s, a) = H(s')$, the cost of the solution that the heuristic $H$ builds from the next state $s'$. This is Eq. 7 of Bertsekas, Tsitsiklis and Wu: move to the successor $j$ with the smallest $H(j)$. For rewards instead of costs, line L4 takes the largest mean.

**Why it improves.** If $\hat Q$ is exact, the rollout policy $\pi'$ is greedy with respect to the value of $\pi$, so by the [policy improvement theorem](/policy-improvement-theorem/) its expected cost is at most that of $\pi$ from every state. For deterministic problems, Bertsekas, Tsitsiklis and Wu prove this directly. A heuristic $H$ is *sequentially consistent* if, whenever it builds the path $(i, i_1, \ldots, i_m)$ from $i$, it builds $(i_1, \ldots, i_m)$ from $i_1$. Greedy heuristics with a fixed rule for ties have this property. Then the rollout terminates, and along its path $i_1, i_2, \ldots$ the costs $H(i_1) \ge H(i_2) \ge \cdots$ do not increase (Proposition 1), so its final cost is at most $H(i_1)$. Proposition 2 gives the same result under the weaker condition of a *sequentially improving* heuristic.

**Cost.** If a decision has at most $b$ actions, a rollout costs at most $C$, and a solution has $N$ decisions, the rollout policy costs $O(N b m C)$, a factor $N b m$ more than the base policy.

## Classic examples

- **Backgammon.** Tesauro and Galperin used a backgammon program as the base policy for both players. To choose a move, they simulated many games from each candidate move with dice rolls drawn at random and took the move with the best mean result. With base players that ranged from a random policy to TD-Gammon, they report that the error rate of the base player fell by as much as a factor of 5 or more. The method works online, at the positions of the game being played, and runs in parallel easily.
- **Repair of machines.** Bertsekas, Tsitsiklis and Wu applied rollouts to a two-stage stochastic problem: a shop decides how many spare parts to use on broken machines now, keeping some for later breakdowns. The base policies are simple rules, such as repairing machines in decreasing order of a value. On 5000 random test problems with an average optimal cost of 33.69, the rollouts removed a large part of the gap to the optimum; for example, one heuristic with mean cost 49.00 was improved to 43.06 by the best rollout, a gain of 38.8 percent of the gap (their Table 1). In two rows of that table the plain rollout was worse than its heuristic, which is not sequentially improving there, while the optimized, extended and fortified rollouts were always better.
- **Flat Monte Carlo in games.** Evaluating each move of the root by random playouts, as in early Monte Carlo Go programs, is a rollout algorithm whose base policy is uniformly random. On the page [MCTS](/monte-carlo-tree-search/), such a flat search with 400 playouts chooses the wrong move in a small trap tree, because it estimates the value of the random policy, not the minimax value. MCTS and [UCT](/uct/) fix this by growing a tree and improving the policy inside it as the playouts accumulate.
- **Tours and paths.** A greedy construction such as nearest neighbor for the [traveling salesman problem](/traveling-salesman-problem/) is a natural base policy, as the worked example below shows.

### A worked example

A traveler starts at 0 on a line and must visit the cities $1$, $-2$ and $5$, with no return. The base policy is the [nearest neighbor heuristic](/nearest-neighbor-heuristic/), which goes $0 \to 1 \to -2 \to 5$ with cost $1 + 3 + 7 = 11$. The rollout tries each first city and finishes with nearest neighbor:

| first city | completed by nearest neighbor | cost |
|---|---|---|
| 1 | 1, −2, 5 | 11 |
| −2 | −2, 1, 5 | 9 |
| 5 | 5, 1, −2 | 12 |

It goes to $-2$. From there it compares $1$ then $5$ (cost $3 + 4 = 7$) with $5$ then $1$ (cost $7 + 4 = 11$) and goes to $1$. The rollout tour $0, -2, 1, 5$ costs 9, which is optimal for these cities, against 11 for the base policy. Nearest neighbor is sequentially consistent, so Proposition 1 promises at most 11 before any computation, and the costs along the rollout path are $11, 9, 9$.

## Variations

- **Truncated rollouts.** Run the base policy for a few steps and then add an evaluation of the state reached, which is much cheaper than a run to the end.
- **Multistep lookahead.** Compare sequences of two or more actions, each followed by the base policy, instead of single actions.
- **Repeated rollout.** Use the rollout policy as the base policy of a second rollout. This is two steps of policy iteration, at a cost that multiplies again.
- **Extended, optimized and fortified rollouts.** If the heuristic is not sequentially improving, the plain rollout can be worse than the heuristic. The extended rollout changes the problem so that Proposition 2 applies. The optimized rollout keeps the best of all complete solutions it builds. The fortified rollout keeps the best complete path found so far and leaves it only for a better one. Each is guaranteed to be no worse than the heuristic.
- **Adaptive sampling.** With random outcomes, spend more rollouts on the actions whose means are close to the best, and stop early on clearly bad ones. A bandit rule such as [UCB1](/ucb1/) does this, and doing it at every node of a tree gives UCT.

## Pitfalls

- **A heuristic that is not sequentially consistent.** The rollout can then cycle forever: in Example 1 of Bertsekas, Tsitsiklis and Wu, the heuristic always takes one step around a cycle and then goes to the destination, so the rollout always takes that step and never stops. Use the fortified or optimized version, or check termination.
- **Too few samples.** With $m$ rollouts the error of a mean is of order $1/\sqrt m$ (by the [Hoeffding inequality](/hoeffding-inequality/) for bounded costs). If two actions differ by less than that, the choice is noise and the rollout can be worse than the base policy. Use the same random numbers for all actions when the simulator permits it, so that the differences have less noise.
- **Expecting optimality.** One rollout step improves the base policy but does not make it optimal. A poor base policy gives a poor estimate, as the flat Monte Carlo example shows.
- **Opponent models in games.** In a game, the rollouts assume that both players follow the base policy. The improvement is against that model of the opponent, not against a strong opponent.
- **Cost.** The factor $N b m$ adds up quickly. Truncate the rollouts or prune the actions when time is short.

## References
