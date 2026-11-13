---
tag: JA1FVX
kind: problem
slug: contingent-planning
name: Contingent planning
aliases:
- conditional planning
- planning with sensing
area: games-and-search/planning
level: advanced
summary: Find a plan whose actions branch on observations, so that it reaches the goal from every possible initial state and for every outcome. It is an AND-OR search over set beliefs.
prereqs: [belief-space, conformant-planning]
see_also: [pomdp-planning, planning-as-model-checking, execution-monitoring, replanning, games-on-graphs, proof-number-search, exptime, binary-decision-diagram]
sources:
  - paper: "Alberto Martelli and Ugo Montanari, Additive AND/OR graphs, Proceedings of IJCAI 1973"
    locator: pp. 1 to 11 (heuristic search for solution graphs of AND/OR graphs)
  - paper: "Blai Bonet and Hector Geffner, Planning with incomplete information as heuristic search in belief space, Proceedings of AIPS 2000"
    locator: pp. 52 to 61 (contingent planning with sensing as search over beliefs)
  - paper: "Jussi Rintanen, Complexity of planning with partial observability, Proceedings of ICAPS 2004"
    locator: pp. 345 to 354 (2-EXPTIME-completeness with partial observability, EXPTIME with full observability and EXPSPACE with none)
  - book: isbn:9781608459698
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: Chapter 5 (planning with sensing, with Section 5.5 on belief tracking and Section 5.6 on strong and strong cyclic plans)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 17 (planning in nondeterministic domains, with Section 17.4 on partial observability)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 4 (AND-OR search for nondeterministic actions and search with partial observations)
---

Contingent planning asks for a plan that may react to what the agent senses. The initial state is only known to be in a set, the actions can have several outcomes, and after each action the agent gets an observation. A contingent plan is a tree, or a policy on [beliefs](/belief-space/), whose branches are labeled with observations, and it must reach the goal on every branch that can happen. The belief after an action and an observation is known to the agent, so the problem is a search in an AND-OR graph: the planner chooses the action (an OR node), and nature chooses the observation (an AND node). Contingent planning includes [conformant planning](/conformant-planning/), the case with no useful observations, and fully observable nondeterministic planning, the case where the observation is the state. For compact models it is 2-EXPTIME-complete.

## In plain words

A doctor does not know which illness a patient has. She does not have to fix the whole treatment in advance. She can order a test, look at the result, and then choose. A plan for her is a tree of choices: do this test, and if the result is positive do that, and if it is negative do something else.

Such a plan must work for every result that can come. The planner picks the next action, and the world picks the result. The plan is good if the planner wins against every choice of the world. Tests help because they split the set of possible cases into smaller sets, and each smaller set is easier to handle. Some problems have no plan at all without a test.

## Definition

A contingent planning problem is a tuple $(S, I, G, A, F, \Omega, \text{obs})$. The parts $S$, $I$, $G$, $A$ and $F$ are as in [conformant planning](/conformant-planning/): states, initial states, goal states, actions and the nondeterministic transition function. $\Omega$ is a finite set of observations, and $\text{obs}(s', a) \in \Omega$ is the observation that the agent gets when the action $a$ has led to the state $s'$. A model with nondeterministic sensing gives a set of observations in place of one.

For a belief $b \subseteq S$ and an action $a$ applicable in every state of $b$, the successor beliefs are

$$b_a^o = \{ s' \in b_a : \text{obs}(s', a) = o \}, \qquad b_a = \bigcup_{s \in b} F(s, a),$$

one for each observation $o$ with $b_a^o \ne \emptyset$.

A **contingent plan** for a belief $b$ is either the empty plan, if $b \subseteq G$, or an action $a$ applicable in $b$ together with a contingent plan for each nonempty $b_a^o$. This definition gives finite trees, which reach the goal in a bounded number of steps on every branch. A plan can also be given as a partial policy $\pi$ from beliefs to actions. The **decision problem** asks whether a plan exists for $I$. The **optimization problem** asks for a plan of least worst-case depth, or of least expected cost under a prior.

Let $d(b) = 0$ if $b \subseteq G$, and otherwise

$$d(b) = \min_{a \text{ applicable in } b} \Big( 1 + \max_{o} d(b_a^o) \Big),$$

with the minimum of an empty set equal to $\infty$. The least solution of this equation over the finite set of beliefs is the least worst-case depth of a plan, and a plan exists exactly when $d(I) < \infty$.

## Variants

- **Full observability.** $\text{obs}(s', a) = s'$. Every reachable belief is a single state, and the problem is fully observable nondeterministic planning (FOND).
- **Strong and strong cyclic plans.** A strong plan reaches the goal in a bounded number of steps on every branch, as above. A strong cyclic plan may loop, and must reach the goal under the assumption that each outcome of a repeated action happens in the end. This is the fairness condition of [planning as model checking](/planning-as-model-checking/).
- **Sensing actions.** Some models have actions that only sense and do not change the state, and other actions that give no information. The definition above covers both, through $\text{obs}$.
- **Probabilistic contingent planning.** With probabilities on the initial state, the outcomes and the observations, the problem is [POMDP planning](/pomdp-planning/), for example with a goal that must hold with probability at least $\theta$.
- **Bounded plans.** Plans of depth at most $k$, or with at most $k$ branch points.

## Examples

**A coin.** A coin shows heads or tails, and the goal is heads. The action look tells the side and does not change it. The action turn turns the coin over and gives no information. No conformant plan exists, because turn maps the belief $\{H, T\}$ to itself. The contingent plan is

$$\text{look}; \ \text{if } T \text{ then turn},$$

of worst-case depth 2. The AND-OR graph has two beliefs that are not goals, $\{H, T\}$ and $\{T\}$.

**A key in three boxes.** A key is in box 1, 2 or 3. The action take($i$) takes the key if it is in box $i$, and after each take the hand feels whether it holds the key. The plan of least depth is: take(1); if empty, take(2); if empty, take(3). Its worst-case depth is 3, the same as the conformant plan take(1), take(2), take(3). The contingent plan stops as soon as it has the key, so with a uniform prior its expected length is $(1 + 2 + 3)/3 = 2$, against 3 for the conformant plan.

**A trap.** A trap is behind door 1 or door 2, and opening the door with the trap is not allowed. With no sensor there is no plan. With a sensor, the plan is: look; if the trap is at 1, open 2, else open 1.

**Sensing never hurts.** Every conformant plan is a contingent plan that ignores the observations. So the least worst-case depth with sensing is at most the length of a shortest conformant plan. The implementation checks this on random problems, and checks that with one observation the two are equal.

## Known algorithms

- **AND-OR search with a fixed point.** Build the AND-OR graph of the beliefs that are reachable from $I$, and compute the least solution $d$ of the equation of the definition by rounds of updates from $\infty$. Then read a plan off $d$. The implementation does this, and it finds a plan of least worst-case depth.
- **Depth-first AND-OR search.** Search the tree of the equation with a depth limit, and increase the limit. A belief that repeats on the current path is a failure for strong plans.
- **Heuristic AND-OR search.** AO* and its relatives (Martelli and Montanari 1973) expand a best partial solution graph under an admissible heuristic. Bonet and Geffner (2000) apply heuristic search to beliefs with sensing.
- **Symbolic search.** Planners based on [binary decision diagrams](/binary-decision-diagram/) compute the beliefs from which a plan exists by backward fixed points, as in [planning as model checking](/planning-as-model-checking/).
- **Compilation.** A contingent problem can be translated into a fully observable nondeterministic problem whose states are sets of known literals, and then solved by a FOND planner. Online methods translate into classical problems with sampled outcomes of the sensors, and plan again when an observation is not the one that was assumed, as in [replanning](/replanning/).
- **Contingent-FF.** It extends the relaxed planning heuristic of FF to beliefs that are kept implicit as action sequences, and searches the AND-OR graph forward.

## Bounds

- **Explicit states.** There are at most $2^{|S|} - 1$ beliefs. The AND-OR graph has at most $|A|$ AND nodes below each belief, each with at most $|\Omega|$ branches. The fixed point needs at most as many rounds as there are beliefs, so the time is polynomial in the size of the graph, and exponential in $|S|$ in the worst case.
- **Size of a plan.** A plan tree can be exponentially larger than the graph, because the same belief can occur on many branches. A plan as a policy on beliefs has at most one entry for each belief.
- **Compact models.** For problems given by state variables, plan existence is 2-EXPTIME-complete with partial observability, EXPTIME-complete with full observability, and EXPSPACE-complete with no observability (Rintanen 2004). So, unless these classes are equal, partial observability is harder than both extremes, because the planner must reason about sets of states and also branch on them.
- **Worst-case depth.** For strong plans, $d(I) \le$ the number of beliefs, because a plan of least depth never repeats a belief on a branch.

## Reductions

- **From conformant planning.** Take one observation for all states. Then each action has one successor belief, the AND nodes have one branch, and a contingent plan is a sequence.
- **From FOND planning.** Take the state as the observation. Then the beliefs are single states.
- **To a game.** A contingent problem is a two-player reachability game on the AND-OR graph of beliefs: the planner moves at OR nodes, nature at AND nodes, and a plan is a winning strategy. The fixed point of the definition is the attractor of the goal beliefs, as in [games on graphs](/games-on-graphs/).
- **To POMDP planning.** With any probabilities of full support, a contingent plan is a POMDP policy that reaches the goal with probability 1 in a bounded number of steps. The [POMDP](/pomdp-planning/) form adds costs and probabilities.
- **To classical planning, online.** Fixing the observations that the agent expects gives a classical problem. Solving it and replanning when the expectation fails gives a complete method for many domains, though not for all.

## Applications

- Robots with sensors that act in partly known places, such as a robot that checks whether a door is open before it plans its route.
- Diagnosis and repair, where tests are actions and their results are observations.
- Composition of web services and business processes whose answers are not known in advance.
- Testing of reactive systems, where a test case is a strategy that reacts to the outputs of the system under test.
- Games against nature in puzzles with hidden information, such as Wumpus-like worlds.

## References
