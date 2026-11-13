---
tag: Y0RPP5
kind: problem
slug: plan-recognition
name: Plan recognition
aliases:
- goal recognition
area: games-and-search/planning
level: advanced
summary: Infer the goal or the plan of an agent from some of its actions. Plan recognition as planning ranks the goals by the costs of plans that do and do not fit the observations.
prereqs: [classical-planning, bayes-theorem]
see_also: [inverse-reinforcement-learning, bayesian-inference, hidden-markov-model, execution-monitoring, probabilistic-context-free-grammar, hierarchical-task-network, dijkstra, particle-filter]
sources:
  - paper: doi:10.1016/0004-3702(78)90012-7
    title: C. F. Schmidt, N. S. Sridharan and J. L. Goodson, The plan recognition problem, an intersection of psychology and artificial intelligence, Artificial Intelligence 11(1-2), 1978
    locator: pp. 45 to 83 (the problem of inferring plans from observed actions)
  - paper: "Henry A. Kautz and James F. Allen, Generalized plan recognition, Proceedings of AAAI 1986"
    locator: pp. 32 to 37 (recognition over a hierarchy of plans by minimal covering explanations)
  - paper: doi:10.1016/0004-3702(93)90060-O
    title: Eugene Charniak and Robert P. Goldman, A Bayesian model of plan recognition, Artificial Intelligence 64(1), 1993
    locator: pp. 53 to 79 (plan recognition as inference in Bayesian networks built from a plan library)
  - paper: "Miquel Ramirez and Hector Geffner, Plan recognition as planning, Proceedings of IJCAI 2009"
    locator: pp. 1778 to 1783 (the goals with an optimal plan that embeds the observations, found with classical planners)
  - paper: doi:10.1609/aaai.v24i1.7745
    title: Miquel Ramirez and Hector Geffner, Probabilistic plan recognition using off-the-shelf classical planners, Proceedings of AAAI 2010
    locator: pp. 1121 to 1126 (the likelihood from the cost difference, and the posterior over goals)
  - paper: doi:10.1016/j.cognition.2009.07.005
    title: Chris L. Baker, Rebecca Saxe and Joshua B. Tenenbaum, Action understanding as inverse planning, Cognition 113(3), 2009
    locator: pp. 329 to 349 (Bayesian inverse planning with rational agents, compared with human judgments)
  - book: isbn:9781608459698
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: Section 4.3 (plan and goal recognition), p. 57
---

Plan recognition is the problem of inferring what an agent is trying to do from what it is seen to do. The observer sees some of the actions of the agent, often not all of them, and has a set of possible goals or a library of plans. It must say which goals or plans explain the actions, or how probable each one is. Early systems matched the actions against a hierarchy of plans (Kautz and Allen 1986) or built [Bayesian networks](/bayesian-network/) from a plan library (Charniak and Goldman 1993). **Plan recognition as planning** (Ramírez and Geffner 2009, 2010) uses a planning model in place of a library: a goal is likely when its best plans that fit the observations are about as cheap as its best plans that do not. The inverse view, planning run backward from behavior to goals, is also the idea of [inverse reinforcement learning](/inverse-reinforcement-learning/).

## In plain words

You see a person walk out of a house and turn left. Is she going to the shop, the bus stop or the park? If the shop is to the left, turning left is what a person who wants the shop would do. If the park is to the right, turning left is a strange way to go there. So the shop becomes more likely and the park less likely.

Plan recognition makes this exact. For each possible goal, it asks two questions. How long is the best route to this goal that includes what I saw? How long is the best route that does not? If both are equal, what I saw tells me nothing against this goal. If the route that includes it is much longer, the goal is unlikely. Then it combines this with how likely each goal was before.

## Definition

A **plan recognition problem** is a tuple $(D, s_0, \mathcal{G}, O, P)$:

- $D$ is a planning domain with states, actions and action costs, for example a [STRIPS](/strips/) domain, and $s_0$ is the initial state.
- $\mathcal{G}$ is a finite set of possible goals.
- $O = o_1, \ldots, o_m$ is the sequence of observed actions.
- $P$ is a prior over the goals.

A plan $\pi$ **embeds** $O$ if the actions of $O$ appear in $\pi$ in that order, possibly with other actions between them. For a goal $G$, let $c(G, O)$ be the least cost of a plan for $G$ that embeds $O$, and $c(G, \bar O)$ the least cost of a plan for $G$ that does not, with $\infty$ if there is none.

- **Goal recognition (Ramírez and Geffner 2009).** Output the set of goals $G$ with $c(G, O) = c(G)$, where $c(G)$ is the cost of an optimal plan for $G$. These are the goals for which some optimal plan fits the observations.
- **Probabilistic goal recognition (Ramírez and Geffner 2010).** Output the posterior $P(G \mid O) = \alpha\, P(O \mid G)\, P(G)$ with the likelihood

$$P(O \mid G) = \frac{1}{1 + e^{-\beta \Delta(G, O)}}, \qquad \Delta(G, O) = c(G, \bar O) - c(G, O).$$

The parameter $\beta > 0$ says how close to optimal the agent acts. The formula is what one gets if the agent chooses a plan with probability proportional to $e^{-\beta \cdot \mathrm{cost}}$, and each of the two classes of plans, those that embed $O$ and those that do not, is represented by its cheapest plan.

- **Plan recognition** asks for the plan itself, or a distribution over plans, and not only the goal.

## Variants

- **Keyhole and intended recognition.** In keyhole recognition, the agent does not know or care that it is watched. In intended recognition, the agent acts so as to be understood, as in dialogue. In adversarial recognition, the agent tries to hide its goal.
- **Library-based recognition.** The possible plans come from a hierarchy or a grammar, as in [hierarchical task networks](/hierarchical-task-network/) or a [probabilistic context-free grammar](/probabilistic-context-free-grammar/), and recognition is parsing of the observed actions.
- **Observations of states.** The observer sees facts, or noisy sensor readings, and not actions. The problem then contains state estimation, as in a [hidden Markov model](/hidden-markov-model/) or a [particle filter](/particle-filter/).
- **Online recognition.** The observations arrive one at a time, and the posterior is updated after each one.
- **Full Boltzmann model.** Use the sum over all plans in place of the two cheapest plans. This is exact for the model of a noisy rational agent, and it is the likelihood of [Bayesian inverse planning](/bayesian-inference/) (Baker, Saxe and Tenenbaum 2009).
- **Goal recognition design.** Change the environment so that every agent shows its goal early, for example by blocking some paths.

## Examples

**A 3 by 3 grid.** The agent starts at $(0, 1)$, the middle of the left column. Its goal is $A = (2, 2)$, $B = (2, 0)$ or $C = (0, 2)$, with a uniform prior. Each move costs 1, and $e^{-\beta} = 1/2$.

The observer sees one move east, from $(0, 1)$ to $(1, 1)$.

| Goal | $c(G, O)$ | $c(G, \bar O)$ | $P(O \mid G)$ | $P(G \mid O)$ |
|---|---|---|---|---|
| $A$ | 3 | 3 | 1/2 | 5/12 |
| $B$ | 3 | 3 | 1/2 | 5/12 |
| $C$ | 3 | 1 | 1/5 | 1/6 |

For $C$, the best plan is one move north, and a plan that moves east first needs 3 moves, so $P(O \mid C) = 2^{-3} / (2^{-3} + 2^{-1}) = 1/5$. The goals with an optimal plan that fits $O$ are $A$ and $B$.

Then the observer also sees a move north, from $(1, 1)$ to $(1, 2)$. Now $c(B, O) = 5$ against $c(B, \bar O) = 3$, and the posterior is $A: 5/9$, $B: 2/9$, $C: 2/9$. Only $A$ still has an optimal plan that fits $O$.

With the full Boltzmann model over the plans of at most 6 moves, the first observation gives $A: 5/13$, $B: 5/13$, $C: 3/13$. The order of the goals is the same, but the numbers differ, because many plans that are not optimal also count.

The implementation computes $c(G, O)$ and $c(G, \bar O)$ with [Dijkstra's algorithm](/dijkstra/) in the product of the domain with the number of observations matched so far, and checks them, the posteriors and the full Boltzmann posteriors against an enumeration of all plans up to a length, in exact fractions.

## Known algorithms

- **Plan recognition as planning.** For each goal, compute $c(G, O)$ and $c(G, \bar O)$ with two calls to a planner, then apply the formula. Ramírez and Geffner compile the observations into the domain: a new fact for each observation, which an action can make true only when it is the observed action and the fact of the previous observation holds. A plan embeds $O$ exactly when it makes the last fact true. Any classical planner can then be used, optimal or not.
- **Product search.** With explicit states, search in the product of the states with the index $j \in \{0, \ldots, m\}$ of the observations matched so far. Matching each observation as early as possible is enough to decide whether $O$ embeds in a plan.
- **Covering explanations.** Kautz and Allen find the smallest sets of top-level plans in a hierarchy whose decompositions explain all the observed actions.
- **Bayesian networks from libraries.** Charniak and Goldman build a [Bayesian network](/bayesian-network/) of plans, actions and objects as the observations arrive, and compute posteriors over plans by inference in the network.
- **Grammar parsing.** With plans as a probabilistic grammar, the posterior over plans is computed by chart parsing, as in the [Earley parser](/earley-parser/) or the [CYK algorithm](/cyk-algorithm/).
- **Dynamic programming over plans.** For the full Boltzmann model on an explicit domain, sum the weights of all plans by dynamic programming over (state, observations matched, steps), as in the [forward algorithm](/forward-algorithm/) of hidden Markov models.

## Bounds

- **Explicit states.** With $n$ states, $e$ transitions and $m$ observations, the product has $n(m + 1)$ nodes and $e(m + 1)$ edges, so each cost is one shortest path search in $O(e (m + 1) \log(n (m + 1)))$ time, and a posterior over $k$ goals needs $2k$ searches.
- **Compact models.** For STRIPS domains, deciding whether a goal has a plan that embeds $O$ is PSPACE-complete. It is in PSPACE through the compilation, and it is hard because with no observations it is [plan existence](/strips-plan-existence-pspace-complete/). Computing $c(G, O)$ exactly is as hard as [optimal planning](/optimal-planning/), which is why Ramírez and Geffner also use satisficing planners, at the price of approximate costs.
- **Approximation.** The two-plan formula ignores all plans except the cheapest in each class. It can rank goals differently from the full Boltzmann model when one goal has many cheap plans and another has few.

## Reductions

- **To classical planning.** By the compilation of the observations into the domain, $c(G, O)$ and $c(G, \bar O)$ are optimal costs of classical planning problems.
- **To inverse reinforcement learning.** If the goal is replaced by an unknown reward function, and the agent is an MDP policy, recognition becomes [inverse reinforcement learning](/inverse-reinforcement-learning/).
- **To Bayesian inference.** With a prior over goals and a model of how the agent picks plans, recognition is [Bayesian inference](/bayesian-inference/) of a hidden variable from observations, by [Bayes' theorem](/bayes-theorem/).
- **From parsing.** Recognition over a plan grammar with all actions observed is parsing of the observed string.

## Applications

- Assistants and dialogue systems that infer what a user wants and help or answer before the request is complete.
- Intrusion detection, where an attack is a plan and the observations are system events.
- Games, where non-player characters infer the goal of the player and respond to it.
- Driver assistance and human-robot cooperation, where the robot predicts the goal of a person and plans around it.
- Models of human understanding of actions in cognitive science, as in Bayesian inverse planning.
- Monitoring of agents that act for us, together with [execution monitoring](/execution-monitoring/) of our own plans.

## References
