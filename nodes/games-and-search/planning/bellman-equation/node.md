---
tag: Y80W1T
kind: definition
slug: bellman-equation
name: Bellman equation
area: games-and-search/planning
level: core
summary: "The fixed point equation V(s) = min over a of c(s, a) + sum of P(s' | s, a) V(s'), with V = 0 on goals, and its finite horizon form V_k = T V_(k-1), as used in planning."
prereqs: [markov-decision-process, principle-of-optimality]
see_also: [bellman-optimality-equation, bellman-expectation-equation, bellman-contraction, value-iteration, policy-iteration, stochastic-shortest-path, real-time-dynamic-programming, pomdp-planning]
sources:
  - book: isbn:9780486428093
    title: Richard Bellman, Dynamic Programming, Princeton University Press, 1957 (Dover reprint, 2003)
    locator: Chapter III (the principle of optimality and the functional equations of multistage decision processes)
  - paper: "Richard Bellman, On a routing problem, Quarterly of Applied Mathematics 16(1), 1958"
    title: Bellman 1958, On a routing problem
    locator: pp. 87 to 90 (the functional equation of the deterministic shortest path problem)
  - paper: doi:10.1287/moor.16.3.580
    title: "Dimitri P. Bertsekas and John N. Tsitsiklis, An analysis of stochastic shortest path problems, Mathematics of Operations Research 16(3), 1991"
    locator: pp. 580 to 595 (the total cost Bellman equation, proper policies, and when its solution is unique)
  - book: isbn:9781886529106
    title: Dimitri P. Bertsekas and John N. Tsitsiklis, Neuro-Dynamic Programming, Athena Scientific, 1996
    locator: Chapter 2 (stochastic shortest path problems and discounted problems as a special case)
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: Chapter 4 (finite horizon problems and backward induction) and Chapter 7 (the expected total reward criterion)
  - book: isbn:9781608458868
    title: Mausam and Andrey Kolobov, Planning with Markov Decision Processes, An AI Perspective, Morgan and Claypool, 2012
    locator: Chapter 2 (MDPs, the stochastic shortest path model and its Bellman equation)
  - book: isbn:9781608459698
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: Section 6.1 (goal, shortest path and discounted models) and Section 6.2 (dynamic programming algorithms)
---

The Bellman equation is the fixed point equation that the optimal cost to go of a sequential decision problem must satisfy: the cost of a state is the best, over the actions, of the cost of one step plus the expected cost of the next state. Planning uses two forms of it. The *total cost form*, with no discount and with goal states that cost nothing, is the equation of the [stochastic shortest path problem](/stochastic-shortest-path/). The *finite horizon form* is a recurrence over the number of steps to go and is solved by one backward pass. Both come from the [principle of optimality](/principle-of-optimality/). The discounted forms, with rewards and a [discount factor](/discount-factor/), are on the machine learning pages [Bellman optimality equation](/bellman-optimality-equation/) and [Bellman expectation equation](/bellman-expectation-equation/), and this page does not repeat them.

## Definition

### The model

Take a [Markov decision process](/markov-decision-process/) in cost form, with:

- a finite set of states $S$ and a set of goal states $G \subseteq S$,
- for each state $s \notin G$, a finite nonempty set of actions $A(s)$,
- a cost $c(s, a) \in \mathbb{R}$ for each action,
- a transition law $P(s' \mid s, a) \ge 0$, with $\sum_{s'} P(s' \mid s, a) = 1$.

A goal state is absorbing and free: once the process enters $G$ it stays there and pays nothing more. A [policy](/policy/) $\pi$ is a rule that picks an action; a *stationary* policy is a map $\mu : S \setminus G \to A$ with $\mu(s) \in A(s)$.

For a function $V : S \setminus G \to \mathbb{R}$, extend it by $V(s) = 0$ for $s \in G$ and define the *Q-value* and the *Bellman operator*

$$Q_V(s, a) = c(s, a) + \sum_{s' \in S} P(s' \mid s, a) \, V(s'), \qquad (T V)(s) = \min_{a \in A(s)} Q_V(s, a).$$

For a stationary policy $\mu$, the operator of the policy is $(T_\mu V)(s) = Q_V(s, \mu(s))$. The one step computation of $(TV)(s)$ at a single state is a *Bellman backup*. Its cost is $O(|A(s)| \cdot |S|)$ with a dense transition table, so one full application of $T$ costs $O(|S|^2 |A|)$.

### The total cost form

The cost of a policy $\pi$ from $s$ is the expected total cost $V_\pi(s) = \mathbb{E}_\pi[\sum_{t \ge 0} c(s_t, a_t) \mid s_0 = s]$, where the sum stops at the first goal state, and $V^*(s) = \inf_\pi V_\pi(s)$ is the optimal cost. The **Bellman equation** in total cost form is

$$V(s) = 0 \ \ (s \in G), \qquad V(s) = \min_{a \in A(s)} \Bigl[ c(s, a) + \sum_{s'} P(s' \mid s, a) \, V(s') \Bigr] \ \ (s \notin G), \tag{1}$$

that is, $V = T V$. The **Bellman equation of a policy** $\mu$ is $V = T_\mu V$, a linear system $V = c_\mu + P_\mu V$ over the non-goal states. Here $c_\mu(s) = c(s, \mu(s))$, and $P_\mu$ is the matrix of transitions between non-goal states under $\mu$.

Equation (1) is a condition, not a definition of $V^*$. Whether $V^*$ solves it, and whether it is the only solution, depends on the problem. A stationary policy $\mu$ is *proper* when, from every state, it reaches $G$ with probability 1. Bertsekas and Tsitsiklis (1991) proved that if at least one proper policy exists and every improper policy has infinite cost from some state, then $V^*$ is finite, it is the unique solution of (1), and a policy is optimal exactly when it is greedy for $V^*$. The statement and its proof are on [stochastic shortest path](/stochastic-shortest-path/). Without these assumptions, (1) can have many solutions or none; the non-examples below show both.

### The finite horizon form

Fix a horizon $H \ge 0$ and a terminal cost $h : S \setminus G \to \mathbb{R}$, paid at the state reached after $H$ steps if it is not a goal. Let $V_k(s)$ be the optimal expected cost when $k$ steps remain. The **finite horizon Bellman equation** is the recurrence

$$V_0 = h, \qquad V_k(s) = \min_{a \in A(s)} \Bigl[ c(s, a) + \sum_{s'} P(s' \mid s, a) \, V_{k-1}(s') \Bigr] \quad (1 \le k \le H), \tag{2}$$

that is, $V_k = T V_{k-1} = T^k h$. It has exactly one solution, computed by *backward induction* from $k = 0$ up to $k = H$ in $H$ applications of $T$, for a total of $O(H \, |S|^2 |A|)$ time. An optimal policy takes, when $k$ steps remain, an action $\mu_k(s)$ that attains the minimum in (2). This policy is Markov, because it depends only on the state and the number of steps to go, but in general it is not stationary.

**Claim.** For every $k \le H$ and every state $s$, $V_k(s)$ is the least expected cost of $k$ steps plus the terminal cost, over all policies, including those that use the full history and randomize, and the policy $(\mu_k, \mu_{k-1}, \ldots, \mu_1)$ attains it.

**Proof.** By induction on $k$. For $k = 0$ no action is taken and the cost is $h(s)$ for every policy. Let $k \ge 1$ and let $\pi$ be any policy. Its first action is $a$ with probability $\pi(a \mid s)$. After the first step, with history $(s, a, s')$, the rest of $\pi$ is a policy for $k - 1$ steps from $s'$, so by the induction hypothesis its expected cost is at least $V_{k-1}(s')$, with $V_{k-1} = 0$ on $G$. Hence the cost of $\pi$ is at least $\sum_a \pi(a \mid s) \, [c(s, a) + \sum_{s'} P(s' \mid s, a) V_{k-1}(s')]$. This is an average of the terms of the minimum in (2), so it is at least $V_k(s)$. The policy that plays $\mu_k(s)$ first and then $(\mu_{k-1}, \ldots, \mu_1)$ makes each inequality an equality: by the induction hypothesis its rest costs exactly $V_{k-1}(s')$, and $\mu_k(s)$ attains the minimum. $\square$

The total cost form is the limit of the finite horizon form with $h = 0$: $V^* = \lim_{k \to \infty} T^k 0$ under the assumptions of Bertsekas and Tsitsiklis, and this limit is [value iteration](/value-iteration/).

## Examples and non-examples

### Example: a two state problem

Take non-goal states $A$ and $B$ and one goal $G$, with four actions:

| state | action | cost | outcomes |
|---|---|---|---|
| $A$ | safe | 4 | $G$ |
| $A$ | risky | 1 | $G$ with probability $1/2$, $B$ with probability $1/2$ |
| $B$ | back | 1 | $A$ |
| $B$ | jump | 2 | $G$ with probability $1/3$, $B$ with probability $2/3$ |

There are four stationary policies, and all of them are proper. The cost of each one is the solution of its linear system $V = c_\mu + P_\mu V$. For example, for (risky, back) the system is $V(A) = 1 + \tfrac12 V(B)$ and $V(B) = 1 + V(A)$, so $V(A) = 3$ and $V(B) = 4$. For jump, $V(B) = 2 + \tfrac23 V(B)$ gives $V(B) = 6$.

| policy at $A$, $B$ | $V(A)$ | $V(B)$ |
|---|---|---|
| safe, back | 4 | 5 |
| safe, jump | 4 | 6 |
| risky, back | 3 | 4 |
| risky, jump | 4 | 6 |

The policy (risky, back) is best at both states, so $V^* = (3, 4)$. It satisfies (1): at $A$ the two Q-values are $4$ and $1 + \tfrac12 \cdot 4 = 3$, and at $B$ they are $1 + 3 = 4$ and $2 + \tfrac23 \cdot 4 = \tfrac{14}{3}$. The minima are 3 and 4, and the greedy actions are risky and back. The cost $(4, 5)$ of (safe, back) satisfies its own policy equation but not (1): one backup at $A$ gives $\min(4, 1 + \tfrac52) = \tfrac72 < 4$. This is the improvement step of [policy iteration](/policy-iteration/).

Repeated backups from $V = 0$ give $(1, 1)$, $(\tfrac32, 2)$, $(2, \tfrac52)$, $(\tfrac94, 3)$, $(\tfrac52, \tfrac{13}4)$, and after 8 sweeps $(\tfrac{45}{16}, \tfrac{15}{4})$. The values rise toward $(3, 4)$ and never pass it. They do not reach it in a finite number of steps.

### Example: a deadline makes the policy depend on time

Use the same model with a finite horizon and a terminal cost $h = 10$ at $A$ and at $B$: a state that is not a goal after $H$ steps pays 10. Backward induction (2) gives:

| steps to go $k$ | $V_k(A)$ | $V_k(B)$ | action at $A$ | action at $B$ |
|---|---|---|---|---|
| 0 | 10 | 10 | | |
| 1 | 4 | $\tfrac{26}{3}$ | safe | jump |
| 2 | 4 | 5 | safe | back |
| 3 | $\tfrac72$ | 5 | risky | back |
| 4 | $\tfrac72$ | $\tfrac92$ | risky | back |
| 5 | $\tfrac{13}{4}$ | $\tfrac92$ | risky | back |
| 6 | $\tfrac{13}{4}$ | $\tfrac{17}{4}$ | risky | back |

With one step left, the risky action at $A$ costs $1 + \tfrac12 \cdot 10 = 6$, more than the safe 4, and at $B$ the jump costs $2 + \tfrac23 \cdot 10 = \tfrac{26}{3}$, less than $1 + 10$. With three or more steps left, the policy is the stationary optimum of the total cost problem. The values fall toward $(3, 4)$ from above. The action in a state depends on the time left, so no stationary policy is optimal for this finite horizon problem.

### Example: deterministic shortest paths

If each action has one outcome with probability 1, the action is an edge $s \to s'$ of length $c(s, a)$, and (1) reads $d(s) = \min_{(s, s')} [c(s, s') + d(s')]$ with $d = 0$ on $G$. These are Bellman's equations for the [shortest path](/shortest-path/) distances to $G$ (Bellman 1958). Applying $T$ repeatedly from $d = \infty$ is the [Bellman-Ford algorithm](/bellman-ford/) on the reversed graph. When the graph is acyclic, one pass in reverse topological order solves them, as in [shortest paths in a DAG](/dag-shortest-paths/).

### Example: the discounted problem is a special case

A discounted problem with costs $c$, transitions $P$ and a discount factor $\gamma \in [0, 1)$ becomes a total cost problem with one new goal $g$. Each action keeps its cost and moves to $g$ with probability $1 - \gamma$, and otherwise moves by $P$. The probability that the process is still running after $t$ steps is $\gamma^t$, so the expected total cost of a policy is its discounted cost. Every policy is proper, and (1) for the new problem is the discounted optimality equation in cost form.

### Non-example: an improper loop that costs nothing

Add to the first example an action wait at $B$, of cost 0, that stays at $B$. The policy (risky, wait) is improper: from $B$ it never reaches $G$. Now (1) at $B$ is $V(B) = \min(1 + V(A), 2 + \tfrac23 V(B), V(B))$. With $V(A) = \min(4, 1 + \tfrac12 x)$, the pair $(V(A), V(B)) = (\min(4, 1 + \tfrac{x}{2}), x)$ is a solution for every real $x \le 4$: $(3, 4)$, $(1, 0)$ and $(-4, -10)$ all satisfy (1). The equation no longer picks out one function. The true optimal total cost is $(1, 0)$, reached by waiting forever. That policy never reaches the goal, so the total cost criterion is not the right model here. For problems with nonnegative costs, $V^*$ is the smallest nonnegative solution of (1) (Puterman, Chapter 7), and $(1, 0)$ is that solution.

### Non-example: an improper loop with negative cost

Replace the wait action by a loop at $B$ of cost $-1$. The policy that loops forever has cost $-\infty$, and (1) at $B$ would need $V(B) \le -1 + V(B)$. No real function solves the equation.

### Non-example: a dead end

Add a state $D$ whose only action costs 1 and stays at $D$, and give $A$ a shortcut of cost 0 that goes to $G$ or to $D$ with probability $\tfrac12$ each. No policy is proper from $D$, so $V^*(D) = +\infty$, and (1) at $D$ reads $V(D) = 1 + V(D)$, which no real number solves. Value iteration adds 1 to $V(D)$ at each sweep, and the shortcut at $A$ looks better than it is for many sweeps. Kolobov, Mausam and Weld (2012) study such *dead ends*; see [stochastic shortest path](/stochastic-shortest-path/).

## Related definitions

- **[Principle of optimality](/principle-of-optimality/).** The tails of an optimal policy are optimal. The proof of the finite horizon claim above is that principle in the stochastic case.
- **[Bellman optimality equation](/bellman-optimality-equation/) and [Bellman expectation equation](/bellman-expectation-equation/).** The discounted forms, with rewards to maximize. Because $\gamma < 1$, the operator is a contraction ([Bellman contraction](/bellman-contraction/)), and the solution is unique with no assumption on policies. The total cost form needs the proper policy assumption instead.
- **[Value iteration](/value-iteration/), [policy iteration](/policy-iteration/) and [policy evaluation](/policy-evaluation/).** The standard ways to solve (1) and its policy form. [Real-time dynamic programming](/real-time-dynamic-programming/) applies the backup only at states that a greedy simulation visits.
- **[Stochastic shortest path](/stochastic-shortest-path/) and [MDP planning](/mdp-planning/).** The problems whose optimal costs (1) characterizes.
- **[Action-value function](/action-value-function/).** The function $Q_{V^*}$; an optimal action in $s$ is one that minimizes it.
- **The belief form.** In a [POMDP](/pomdp/), the same equations hold over beliefs instead of states, with an expectation over observations; see [POMDP planning](/pomdp-planning/).

## References
