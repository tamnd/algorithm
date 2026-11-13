---
tag: 4D16F2
kind: problem
slug: stochastic-shortest-path
name: Stochastic shortest path problem
aliases:
- Stochastic shortest paths
- stochastic shortest path problem
area: games-and-search/planning
level: core
summary: Find a policy that reaches a goal with probability 1 at the least expected total cost, in an MDP with no discount. Under the proper policy assumption the Bellman equation has a unique solution.
prereqs: [markov-decision-process, bellman-equation, shortest-path]
see_also: [real-time-dynamic-programming, value-iteration, policy-iteration, linear-programming-for-mdps, mdp-planning, dijkstra, bellman-ford, stochastic-game]
sources:
  - paper: doi:10.1287/moor.16.3.580
    title: "Dimitri P. Bertsekas and John N. Tsitsiklis, An analysis of stochastic shortest path problems, Mathematics of Operations Research 16(3), 1991"
    locator: pp. 580 to 595 (proper policies, the two assumptions, uniqueness of the solution of the Bellman equation and convergence of value iteration and policy iteration)
  - book: isbn:9781886529106
    title: Dimitri P. Bertsekas and John N. Tsitsiklis, Neuro-Dynamic Programming, Athena Scientific, 1996
    locator: Chapter 2 (stochastic shortest path problems, the case where all policies are proper, and the contraction of T over n stages)
  - paper: url:https://arxiv.org/abs/1210.4875
    title: "Andrey Kolobov, Mausam and Daniel S. Weld, A theory of goal-oriented MDPs with dead ends, UAI 2012"
    locator: pp. 438 to 447 (dead ends, the classes fSSPUDE with a finite penalty and iSSPUDE with an infinite penalty)
  - book: isbn:9781608458868
    title: Mausam and Andrey Kolobov, Planning with Markov Decision Processes, An AI Perspective, Morgan and Claypool, 2012
    locator: Chapter 2 (the SSP model), Chapter 3 (value iteration, policy iteration and linear programming) and Chapter 4 (heuristic search from an initial state)
  - book: isbn:9781608459698
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: Section 6.1 (goal, shortest path and discounted models), Section 6.2 (dynamic programming) and Section 6.3 (heuristic search)
---

The stochastic shortest path problem (SSP) asks for a policy that takes a system to a goal state at the least expected total cost, when each action has a cost and a random outcome. It is the [Markov decision process](/markov-decision-process/) model of planning with uncertain action effects: there is no discount, and the process stops at the goal. Bertsekas and Tsitsiklis (1991) gave the theory: if some policy reaches the goal with probability 1 and every policy that does not has infinite cost, then the optimal cost is the unique solution of the [Bellman equation](/bellman-equation/), and [value iteration](/value-iteration/) finds it from any start. When each action has one outcome, the problem is the ordinary [shortest path](/shortest-path/) problem. The abbreviation SSP is also used for the subset-sum problem in complexity theory; on this page it means only the stochastic shortest path problem.

## In plain words

A robot must get to a dock. Each move costs something, and a move does not always do what the robot wants: a sail can stall, a wheel can slip. The robot cannot pick one fixed path, because it does not know where each move will leave it. It needs a rule that says what to do in every place it can end up.

The best rule is the one with the smallest average total cost until the robot is at the dock. The question makes sense only if the robot can reach the dock for sure. If some place has no way out, every rule has an infinite cost there, and the problem must be changed, for example by a fixed charge for giving up.

## Definition

**Input.** An SSP is a tuple $(S, G, A, c, P)$, with:

- a finite set of states $S$ and a nonempty set of goal states $G \subseteq S$,
- for each $s \notin G$, a finite nonempty set of actions $A(s)$,
- a cost $c(s, a) \in \mathbb{R}$ for each $s \notin G$ and $a \in A(s)$,
- transition probabilities $P(s' \mid s, a)$, with $\sum_{s'} P(s' \mid s, a) = 1$.

Goal states are absorbing and cost nothing. Often an initial state $s_0$ is also given; then only the states that a policy can reach from $s_0$ matter. We write $n = |S \setminus G|$.

**Output.** A [policy](/policy/) that attains the optimal cost $V^*(s) = \inf_\pi \mathbb{E}_\pi[\sum_{t \ge 0} c(s_t, a_t) \mid s_0 = s]$, where the sum stops when $s_t \in G$. Usually the answer is a stationary policy $\mu : S \setminus G \to A$, with its cost $V^*$.

**Cost model.** The input size is the number of nonzero entries of $P$ plus $|S| + |A|$. The unit of work is the [Bellman backup](/bellman-equation/) at one state, which costs $O(|A(s)| \cdot |S|)$; one sweep over all states costs $O(|S|^2 |A|)$. The horizon is infinite and the criterion is total cost, with no discount.

### Proper policies and the two assumptions

A stationary policy $\mu$ is **proper** if, from every state, it reaches $G$ with probability 1. In a finite Markov chain this holds exactly when $G$ can be reached from every state along transitions of positive probability. A policy that is not proper is **improper**.

- **(A1)** At least one proper policy exists.
- **(A2)** For every improper policy $\mu$, the cost $V_\mu(s)$ is $+\infty$ for at least one state $s$.

If every cost is positive, (A2) holds automatically: an improper policy stays out of $G$ forever with positive probability from some state, and it pays at least $\min c > 0$ at each step. This is the usual case in planning, where only (A1) can fail.

**Theorem (Bertsekas and Tsitsiklis 1991).** Under (A1) and (A2):

1. $V^*$ is finite, and it is the unique solution of the Bellman equation $V = TV$, where $(TV)(s) = \min_{a} [c(s, a) + \sum_{s'} P(s' \mid s, a) V(s')]$ and $V = 0$ on $G$.
2. For every starting function $V_0$, the sequence $T^k V_0$ converges to $V^*$.
3. A stationary policy is optimal if and only if it attains the minimum in $TV^*$ at every state, and every optimal stationary policy is proper.
4. Policy iteration that starts from a proper policy produces only proper policies and stops with an optimal one.

### A proof when every policy is proper

The full theorem needs a careful argument for improper policies, given in the 1991 paper. The case where every policy is proper has a short proof, and it shows where the assumptions enter.

**Lemma 1.** Every stationary policy is proper if and only if the layers $L_0 = G$ and $L_{k+1} = L_k \cup \{ s : \text{every } a \in A(s) \text{ has } P(L_k \mid s, a) > 0 \}$ reach all of $S$. Then, for every policy, including those that use the history, and every start, $\Pr[s_n \notin G] \le \rho = 1 - p^n < 1$, where $p$ is the smallest positive transition probability.

*Proof.* If the layers stop at $L \ne S$, each state $s \notin L$ has an action $a_s$ with no positive transition into $L$. The stationary policy that plays $a_s$ outside $L$ never leaves $S \setminus L$, so it is improper. If the layers reach $S$, they do so in at most $n$ steps. From a state of layer $k$, whatever action is taken, the next state is in layer $k - 1$ with probability at least $p$. So $G$ is reached within $k \le n$ steps with probability at least $p^n$. $\square$

**Lemma 2.** Under the conclusion of Lemma 1, $\| T^n V - T^n W \|_\infty \le \rho \, \| V - W \|_\infty$ for all $V, W$.

*Proof.* By the finite horizon form of the Bellman equation, $(T^n V)(s)$ is the least expected cost of $n$ steps plus the terminal cost $V(s_n)$, over all policies. For a fixed policy, the two objectives with terminal costs $V$ and $W$ differ by $\mathbb{E}[V(s_n) - W(s_n)]$. Because $V = W = 0$ on $G$, this is at most $\Pr[s_n \notin G] \, \|V - W\|_\infty \le \rho \|V - W\|_\infty$ in absolute value. Two minima over the same set of functions that differ pointwise by at most $\delta$ differ by at most $\delta$. $\square$

*Proof of 1 to 3 in this case.* By Lemma 2 and the [Banach fixed point theorem](/banach-fixed-point-theorem/), $T^n$ has a unique fixed point $\bar V$, and $T^{kn} V_0 \to \bar V$ for every $V_0$. Since $T^n(T \bar V) = T(T^n \bar V) = T \bar V$, the function $T \bar V$ is also a fixed point of $T^n$, so $T \bar V = \bar V$, and every fixed point of $T$ is one of $T^n$, so it is $\bar V$. Convergence of the full sequence follows from $T^{kn + j} V_0 = T^{kn}(T^j V_0)$ for $j < n$. Let $\mu$ attain the minimum in $T \bar V$. The operator $T_\mu$ of a single policy satisfies Lemma 2 as well, so its unique fixed point is the cost $V_\mu$, and $T_\mu \bar V = T \bar V = \bar V$ gives $V_\mu = \bar V$. For any policy $\pi$, its cost is the cost of its first $kn$ steps plus the cost after them. The first part is at least $(T^{kn} \bar V)(s) - \rho^k \|\bar V\|_\infty = \bar V(s) - \rho^k \|\bar V\|_\infty$. The second part is at most $\max |c| \cdot n \sum_{j \ge k} \rho^j$ in absolute value. Both error terms go to 0, so $V_\pi \ge \bar V = V_\mu$. Hence $V^* = \bar V$ and $\mu$ is optimal. $\square$

## Variants

- **Positive costs.** Many planning texts assume $c(s, a) > 0$ for all actions. Then (A2) holds, and the problem is well posed exactly when (A1) holds from the states that matter.
- **SSP from an initial state.** With a start $s_0$, a solution is a partial policy that is defined on all states it reaches from $s_0$. Heuristic search methods such as [real-time dynamic programming](/real-time-dynamic-programming/), LRTDP and LAO* solve this form and can leave most of $S$ untouched.
- **Dead ends.** A state from which no policy reaches $G$ with probability 1 is a dead end, and (A1) fails. Kolobov, Mausam and Weld (2012) define two repairs. In fSSPUDE, a finite penalty $D$ is paid to give up and stop, which is the same as an action of cost $D$ to the goal from every state. In iSSPUDE the penalty is infinite: first maximize the probability of reaching $G$ (the MAXPROB problem), then minimize the cost among the policies that attain that probability.
- **Finite horizon.** A deadline of $H$ steps gives the finite horizon form of the Bellman equation, with a policy that depends on the time to go. It is an SSP over the states $S \times \{0, \ldots, H\}$.
- **Discounted problems.** A discounted MDP is the special case in which each action moves to the goal with probability $1 - \gamma$, so every policy is proper (see [Bellman equation](/bellman-equation/)).
- **Partial observability.** When the state is not observed, the same total cost criterion over beliefs gives goal POMDPs; see [POMDP planning](/pomdp-planning/).
- **Two players.** When a second agent picks some of the actions, the model is a [stochastic game](/stochastic-game/) and the solution concept changes; SSP has one controller.

## Examples

### A boat and a dock

The states are the distances $1, 2, 3$ to a dock, which is the goal $0$. Rowing costs 2 and always moves one step closer. Sailing costs 1: from 2 or 3 it moves one step closer with probability $\tfrac23$ and stalls with probability $\tfrac13$; from 1 the wind is fickle, and it reaches the dock or blows the boat back to 2 with probability $\tfrac12$ each.

All eight stationary policies are proper, and solving the linear system of each with exact fractions gives its cost. Two of them:

| policy at 1, 2, 3 | $V(1)$ | $V(2)$ | $V(3)$ |
|---|---|---|---|
| row, sail, sail | 2 | $\tfrac72$ | 5 |
| row, row, row | 2 | 4 | 6 |
| sail, sail, sail | $\tfrac72$ | 5 | $\tfrac{13}{2}$ |

The policy (row, sail, sail) is best at every state, so $V^* = (2, \tfrac72, 5)$. Sailing from 2 costs $1 + \tfrac23 \cdot 2 + \tfrac13 \cdot \tfrac72 = \tfrac72$, against $2 + 2 = 4$ for rowing; sailing from 1 costs $1 + \tfrac12 \cdot \tfrac72 = \tfrac{11}{4}$, against 2 for rowing.

Value iteration from $V_0 = 0$ gives $(1, 1, 1)$, $(\tfrac32, 2, 2)$, $(2, \tfrac83, 3)$, $(2, \tfrac{29}{9}, \tfrac{34}{9})$ and $(2, \tfrac{92}{27}, \tfrac{119}{27})$ in the first five sweeps. From $V_0 = 100$ it gives $(2, 101, 101)$, $(2, 4, 102)$ and $(2, \tfrac{11}{3}, 6)$ in the first three. In floating point, the largest change in a sweep falls below $10^{-9}$ after 26 sweeps in the first run and 25 in the second, and both end within $10^{-8}$ of $V^*$. The greedy policy is already optimal after the second sweep from 0.

### An improper policy that costs too much

Give each state an action anchor that costs 1 and stays in place. A policy that anchors anywhere is improper, but it has infinite cost there, so (A2) holds. Nothing changes: $V^*$ is still $(2, \tfrac72, 5)$, and value iteration still converges to it.

### An improper policy that costs nothing

Instead give state 2 an action drift of cost 0 that stays at 2. Now (A2) fails. Value iteration from 0 converges to $(1, 0, \tfrac32)$: drifting at 2 forever costs nothing, and the boat never docks. From 100 it converges to $(2, \tfrac72, 5)$. Both are solutions of the Bellman equation, so the solution is not unique, and the start decides which one value iteration finds.

### A dead end

Give state 3 a shortcut over the rocks that costs 1, reaches the dock with probability $\tfrac34$, and wrecks the boat with probability $\tfrac14$. The wreck $W$ has one action, of cost 1, that stays at $W$. No policy is proper from $W$, so (A1) fails and $V^*(W) = \infty$. Value iteration from 0 raises $V(W)$ by 1 at each sweep and never converges. For the first 15 sweeps the greedy action at 3 is the shortcut, because $1 + \tfrac14 V(W)$ is still small. From sweep 16 on it is sail. With the fSSPUDE repair and a give-up penalty $D$, the shortcut costs $1 + \tfrac{D}{4}$ against 5 for sailing. For $D = 8$ the optimal policy takes the shortcut, with $V^*(3) = 3$. For $D = 20$ it sails, with $V^*(3) = 5$.

## Known algorithms

| method | what it needs | what it returns |
|---|---|---|
| [Value iteration](/value-iteration/) | (A1), (A2) | converges to $V^*$ from any start; stop on a small residual |
| [Policy iteration](/policy-iteration/) | (A1), (A2), a proper first policy | an optimal policy in a finite number of steps |
| [Linear programming](/linear-programming-for-mdps/) | (A1), (A2) | $V^*$ as the optimum of maximize $\sum_s V(s)$ subject to $V(s) \le c(s, a) + \sum_{s'} P(s' \mid s, a) V(s')$ |
| [Real-time dynamic programming](/real-time-dynamic-programming/) | an initial state, an admissible start, positive costs | $V^*$ on the states that the optimal policy reaches |
| LRTDP (Bonet and Geffner 2003) | as RTDP | the same, with a labeling rule that detects convergence |
| LAO* (Hansen and Zilberstein 2001) | an initial state, an admissible heuristic | an optimal partial policy found by heuristic search over the AND-OR graph |
| [Dijkstra's algorithm](/dijkstra/) | one outcome per action, $c \ge 0$ | exact distances in $O(m + n \log n)$ |

The [MDP planning](/mdp-planning/) page lists the same methods for the discounted problem.

## Bounds

- One sweep of value iteration costs $O(|S|^2 |A|)$ time with a dense table, and $O(|S| + \text{nonzeros of } P)$ with a sparse one.
- When every policy is proper, value iteration converges geometrically: by Lemma 2, $n$ sweeps shrink the error by the factor $\rho = 1 - p^n$. This factor can be very close to 1, and then convergence is slow. The bound is a worst case bound, not a prediction for a given problem.
- Under (A1) and (A2) the optimal cost is the optimum of a linear program with $|S|$ variables and one constraint per state and action, so it can be computed in time polynomial in the input size. Methods for MDPs that use linear programs are on [linear programming for MDPs](/linear-programming-for-mdps/).
- Checking (A1) is a graph problem. The set of states from which some policy reaches $G$ with probability 1 is the greatest set $W$ such that from each state of $W$ the goal can be reached with actions whose outcomes all stay in $W$. A nested fixed point computation finds it in polynomial time. The test that every policy is proper is the layer construction of Lemma 1.

## Reductions

- **Deterministic SSP is the shortest path problem.** With one outcome per action, a policy is a choice of one out-edge per state, and its cost is the length of the path to $G$. With nonnegative costs, [Dijkstra's algorithm](/dijkstra/) on the reversed graph solves it. With negative costs and no negative cycle, [Bellman-Ford](/bellman-ford/) does. A cycle of positive cost is an improper policy of infinite cost, as (A2) wants; a [negative cycle](/negative-cycle/) is an improper policy of cost $-\infty$, and (A2) fails.
- **Discounted MDP to SSP.** Add a goal and move to it with probability $1 - \gamma$ from each action. The total cost of the new problem is the discounted cost of the old one.
- **Finite horizon to SSP.** Take the product of the states with the time to go.
- **SSP is a special case of [MDP planning](/mdp-planning/)** with the total cost criterion and absorbing goals.

## Applications

- **Probabilistic planning.** Planners for probabilistic PDDL domains model the task as an SSP from an initial state and solve it with heuristic search (RTDP, LRTDP, LAO*), or replan on a determinization ([replanning](/replanning/)).
- **Robot navigation under slip.** Grid worlds with noisy moves and a target cell are the standard small SSPs; the boat above is one.
- **Goal POMDPs.** The belief MDP of a POMDP with a goal is an SSP over beliefs, with the same assumptions ([belief space](/belief-space/)).
- **Routing with random moves.** The 1991 paper states the problem in this form: at each node of a graph, choose a probability distribution over the successor nodes, so as to reach a destination node at the least expected cost.

## References
