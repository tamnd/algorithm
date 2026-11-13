---
tag: J05MEA
kind: problem
slug: pomdp-planning
name: POMDP planning
area: games-and-search/planning
level: advanced
summary: Given a POMDP model and a start belief, compute a policy over beliefs, or the next action, that maximizes the expected total reward. Exact planning is hard, so solvers approximate or plan online.
prereqs: [pomdp, belief-space, mdp-planning]
see_also: [point-based-value-iteration, real-time-dynamic-programming, conformant-planning, contingent-planning, stochastic-shortest-path, monte-carlo-tree-search, expectiminimax, pspace]
sources:
  - paper: "Edward J. Sondik, The optimal control of partially observable Markov processes, PhD thesis, Stanford University, 1971"
    locator: the whole thesis (the finite-horizon value as a maximum of linear functions of the belief)
  - paper: doi:10.1287/opre.21.5.1071
    title: Richard D. Smallwood and Edward J. Sondik, The optimal control of partially observable Markov processes over a finite horizon, Operations Research 21(5), 1973
    locator: pp. 1071 to 1088 (the piecewise linear convex value and the exact algorithm)
  - paper: doi:10.1287/mnsc.28.1.1
    title: "George E. Monahan, A survey of partially observable Markov decision processes: theory, models, and algorithms, Management Science 28(1), 1982"
    locator: pp. 1 to 16 (the enumeration algorithm)
  - paper: doi:10.1016/S0004-3702(98)00023-X
    title: Leslie Pack Kaelbling, Michael L. Littman and Anthony R. Cassandra, Planning and acting in partially observable stochastic domains, Artificial Intelligence 101(1-2), 1998
    locator: pp. 99 to 134 (the belief MDP, policy trees, the witness algorithm and the tiger problem)
  - paper: "Anthony R. Cassandra, Michael L. Littman and Nevin L. Zhang, Incremental pruning: a simple, fast, exact method for partially observable Markov decision processes, Proceedings of UAI 1997"
    locator: pp. 54 to 61 (pruning after each sum over the observations)
  - paper: doi:10.1287/moor.12.3.441
    title: Christos H. Papadimitriou and John N. Tsitsiklis, The complexity of Markov decision processes, Mathematics of Operations Research 12(3), 1987
    locator: pp. 441 to 450 (PSPACE-completeness of the finite-horizon problem)
  - paper: doi:10.1016/S0004-3702(02)00378-8
    title: Omid Madani, Steve Hanks and Anne Condon, On the undecidability of probabilistic planning and related stochastic optimization problems, Artificial Intelligence 147(1-2), 2003
    locator: the main undecidability results for infinite and indefinite horizons
  - paper: "Jussi Rintanen, Complexity of planning with partial observability, Proceedings of ICAPS 2004"
    locator: pp. 345 to 354 (EXPSPACE-completeness of conformant planning and 2-EXPTIME-completeness of planning with partial observability, for compact models)
  - book: isbn:9781608459698
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: Chapter 7 (POMDP planning, with Section 7.2 on exact offline algorithms and Section 7.3 on approximate and online algorithms)
---

POMDP planning is the problem of choosing actions when the effects of actions are random and the state is seen only through noisy observations. The input is a [POMDP](/pomdp/) model and a start [belief](/belief-space/). The output is a policy that maps beliefs to actions, or, in online planning, a good action for the current belief. The belief is a sufficient statistic, so the problem is [MDP planning](/mdp-planning/) on the belief MDP, whose states are the points of a simplex. For a finite horizon the optimal value is the maximum of a finite set of linear functions of the belief (Smallwood and Sondik 1973). Exact planning is PSPACE-complete for a polynomial horizon and undecidable for some questions about an infinite horizon, so practical solvers use point-based approximations or search from the current belief.

## In plain words

A robot must act, but its sensors are noisy, so it never knows exactly where it is. It keeps a list of the places it can be, with a weight on each place, and it updates the list after each move and each reading. A plan must say what to do for each list the robot can have, not for each place.

The best plan balances two needs. Some actions earn a reward now. Other actions earn nothing but make the readings better, so that later actions are safer. Planning must pay for information when information is worth its cost. The number of lists is not finite, so the planner cannot write a table of all of them. It either finds a small set of plans that covers all lists, or it plans again from the current list at each step.

## Definition

A POMDP is a tuple $(S, A, \Omega, P, O, R, \gamma)$ with finite sets of states, actions and observations, a transition law $P(s' \mid s, a)$, an observation law $O(o \mid a, s')$, a reward $R(s, a)$ and a discount $0 \le \gamma \le 1$. The model is defined on the [POMDP](/pomdp/) page, with the belief update $b \mapsto b^{a,o}$ and the probability $\Pr(o \mid b, a)$.

**Finite horizon.** Given $b_0$ and $H$, find a policy, which picks $a_t$ from $b_t$ and the number of steps to go, that maximizes $\mathbb{E}\left[\sum_{t=0}^{H-1} \gamma^t R(s_t, a_t)\right]$. The optimal value satisfies $V_0 = 0$ and

$$V_k(b) = \max_{a \in A} \left[ \sum_s b(s) R(s, a) + \gamma \sum_{o \in \Omega} \Pr(o \mid b, a) \, V_{k-1}(b^{a,o}) \right].$$

**Infinite horizon.** With $\gamma < 1$, find a stationary policy $\pi : \Delta(S) \to A$ that maximizes the expected discounted reward. $V^*$ is the unique bounded solution of the same equation without the index $k$.

**Decision version.** Given the model, $b_0$, $H$ and a threshold $\theta$, is there a policy whose expected reward is at least $\theta$? This is the form used in the complexity results.

A deterministic policy for horizon $H$ from $b_0$ is a policy tree: a root action, and below it one subtree of depth $H - 1$ for each observation. Each tree $p$ has a value vector $\alpha_p \in \mathbb{R}^S$, and the value of $p$ at $b$ is $\alpha_p \cdot b$. So

$$V_H(b) = \max_{p} \alpha_p \cdot b,$$

and $V_H$ is piecewise linear and convex. A set $\Gamma$ of vectors represents $V_H$ when the maximum over $\Gamma$ equals $V_H$ everywhere. A vector is *useful* if it is the unique maximum at some belief. Pruning removes the vectors that are not useful.

## Variants

- **Offline and online.** An offline planner computes a policy for all beliefs, or for the beliefs reachable from $b_0$, before it acts. An online planner searches the tree of beliefs from the current belief and picks one action at each step.
- **Goal POMDPs.** Actions have positive costs and the aim is to reach a set of goal states at the least expected cost, with no discount. This is a [stochastic shortest path problem](/stochastic-shortest-path/) on beliefs, in which a belief is a goal when all its mass is on goal states.
- **Qualitative planning.** If only the goal with probability 1 matters, the probabilities can be dropped, and the beliefs become sets. With no observations this is [conformant planning](/conformant-planning/), and with observations it is [contingent planning](/contingent-planning/).
- **Bounded policies.** The policy is a finite-state controller with a fixed number of nodes. The planner searches over the controllers of that size.
- **Factored POMDPs.** States, actions and observations are given by variables, and the model by a dynamic Bayesian network. The number of states is then exponential in the size of the input.

## Examples

**The tiger problem** (Kaelbling, Littman and Cassandra 1998), with no discount. The model and the first values are on the [POMDP](/pomdp/) page. The table counts the vectors at the horizon $H$. Enumeration makes $|A| \, |\Gamma_{H-1}|^{|\Omega|}$ vectors from the set of the step before. The pruned set keeps the useful vectors only. Pruning after each step starts each step from the pruned set.

| $H$ | $V_H(1/2)$ | vectors from full enumeration | useful vectors | vectors made when each step is pruned |
|---|---|---|---|---|
| 1 | $-1$ | 3 | 3 | 3 |
| 2 | $-2$ | 27 | 5 | 27 |
| 3 | $68/25$ | 2187 | 7 | 75 |
| 4 | $1937/800$ | 14348907 | 5 | 147 |

The full enumeration grows as $3^{(2^H - 1)}$. With pruning after each step, the sets stay small: 3, 5, 7, 5 and then 9 useful vectors at $H = 5$. Pointwise dominance alone keeps 9 of the 2187 vectors at $H = 3$. Two of them are not useful: no single vector is above them everywhere, but the maximum of the other vectors is at least as high on the whole interval. With two states, a belief is one number $p$, each vector is a line over $[0, 1]$, and the useful vectors are the pieces of the upper envelope.

At $H = 2$ and $H = 3$, every useful plan starts with listen. At $H = 4$, the two end pieces start by opening a door: when the planner is almost sure where the tiger is, it opens the other door at once and has three steps left after the reset.

**Online search.** The tree of beliefs from $b_0$ has $(|A| \, |\Omega|)^H$ paths of length $H$. For the tiger, search to depth 4 visits at most $6^4 = 1296$ leaves and gives $V_4(1/2) = 1937/800$, with no vectors at all.

## Known algorithms

- **Search in the tree of beliefs.** Expand actions and observations from $b_0$ to depth $H$, with the backup of the equation above at each node. This is an expectimax tree, like the chance nodes of [expectiminimax](/expectiminimax/). It is exact for horizon $H$ and costs $O((|A||\Omega|)^H |S|^2)$.
- **Exact value iteration with vectors.** Enumeration (Monahan 1982) builds all the vectors of $\Gamma_H$ from $\Gamma_{H-1}$, then prunes them with one linear program for each vector. The witness algorithm (Kaelbling, Littman and Cassandra 1998) and incremental pruning (Cassandra, Littman and Zhang 1997) avoid building most of the useless vectors. Incremental pruning prunes after each sum over one observation.
- **Point-based methods.** [Point-based value iteration](/point-based-value-iteration/) keeps one vector for each belief of a finite set and backs up only at these beliefs. Its value is a lower bound. HSVI and SARSOP choose the beliefs by search from $b_0$ with an upper and a lower bound.
- **Heuristic search over beliefs.** [Real-time dynamic programming](/real-time-dynamic-programming/) can run on beliefs, with a table for the beliefs that the trials see, for goal POMDPs.
- **Monte Carlo planning.** Sample states from the belief and run [Monte Carlo tree search](/monte-carlo-tree-search/) over histories of actions and observations, as in POMCP. This needs only a simulator of the model.
- **Policy search.** Improve a finite-state controller by policy iteration over controllers, or by gradient methods.

## Bounds

- **Finite horizon.** The decision version is PSPACE-complete when $H$ is bounded by a polynomial in the size of the input (Papadimitriou and Tsitsiklis 1987). The same question for an MDP is P-complete. So partial observation makes planning much harder, unless P equals [PSPACE](/pspace/).
- **Infinite horizon.** Madani, Hanks and Condon (2003) prove that several questions are undecidable for infinite and indefinite horizons, such as whether a policy reaches the goal with a probability above a given threshold. So there is no exact algorithm for the general infinite-horizon problem.
- **Size of the value.** With no pruning, $|\Gamma_H| = |A| \, |\Gamma_{H-1}|^{|\Omega|}$, which is doubly exponential in $H$. The useful set can also grow exponentially, so no exact algorithm has a polynomial bound in the output size of all instances.
- **Online search.** The belief tree to depth $H$ has $(|A||\Omega|)^H$ leaves, which is exponential in $H$ but independent of the number of beliefs.
- **Approximation.** A point-based solution with beliefs that are within $\delta$ of every reachable belief is within $O(\delta / (1-\gamma)^2)$ of the optimal value. The exact constant is on the [point-based value iteration](/point-based-value-iteration/) page.

## Reductions

- **To the belief MDP.** A POMDP is an MDP on $\Delta(S)$. Every MDP method applies in principle, but the state space is continuous.
- **From MDP planning.** An MDP is a POMDP in which the observation is the state. Then each reachable belief is a point mass.
- **From qualitative planning.** Conformant and contingent planning with a goal for sure are the special case where only the support of the belief matters. Their complexity results, EXPSPACE for conformant and 2-EXPTIME for contingent planning with compact models (Rintanen 2004), are lower bounds for factored POMDPs with a goal for sure.
- **To an SSP.** A goal POMDP is a [stochastic shortest path problem](/stochastic-shortest-path/) on beliefs, and a discounted POMDP becomes a goal POMDP by the usual reduction with a stop probability $1 - \gamma$ in each step.

## Applications

- Robot navigation and localization with noisy sensors, where the belief is over the poses of the robot.
- Dialogue systems, where the state is the hidden intent of the user and each question costs something.
- Medical diagnosis and treatment, where tests give information at a cost and treatments act on a hidden state.
- Maintenance and inspection, the first application of the model in operations research.
- Search for a hidden target, and the guidance of sensors.

## References
