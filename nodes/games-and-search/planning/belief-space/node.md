---
tag: N0RMN6
kind: concept
slug: belief-space
name: Belief space
aliases:
- belief state
area: games-and-search/planning
level: advanced
summary: The states of planning when the agent cannot see the true state. A belief is the set, or the distribution, of the states that are possible after the actions and observations so far.
prereqs: [state-space, bayes-theorem]
see_also: [pomdp, conformant-planning, contingent-planning, pomdp-planning, point-based-value-iteration, planning-as-model-checking, particle-filter, hidden-markov-model]
sources:
  - paper: doi:10.1016/0022-247X(65)90154-X
    title: K. J. Astrom, Optimal control of Markov processes with incomplete state information, Journal of Mathematical Analysis and Applications 10(1), 1965
    locator: pp. 174 to 205 (the conditional distribution of the state as a sufficient statistic)
  - paper: doi:10.1016/S0004-3702(98)00023-X
    title: Leslie Pack Kaelbling, Michael L. Littman and Anthony R. Cassandra, Planning and acting in partially observable stochastic domains, Artificial Intelligence 101(1-2), 1998
    locator: pp. 99 to 134 (the belief state estimator and the belief MDP)
  - paper: "Blai Bonet and Hector Geffner, Planning with incomplete information as heuristic search in belief space, Proceedings of AIPS 2000"
    locator: pp. 52 to 61 (set beliefs and probabilistic beliefs as the states of a search)
  - paper: doi:10.1613/jair.774
    title: Alessandro Cimatti and Marco Roveri, Conformant planning via symbolic model checking, Journal of Artificial Intelligence Research 13, 2000
    locator: pp. 305 to 338 (sets of states as binary decision diagrams in a search of belief space)
  - book: isbn:9781608459698
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: Section 4.2 (incomplete information), Section 5.5 (belief tracking) and Section 7.4 (belief tracking in POMDPs)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 4 (search with no observations and with partial observations, in the space of belief states)
---

A belief is what an agent knows about the state of the world when it cannot see the state. In the qualitative form, it is the set of the states that are still possible. In the probabilistic form, it is a distribution over the states. Belief space is the set of all beliefs. An action and an observation map a belief to a new belief, and the new belief depends only on the old belief, the action and the observation. So a problem with hidden state becomes a problem with a visible state, the belief, and a planner can search belief space with the methods for full observation. This is the base of [conformant planning](/conformant-planning/), [contingent planning](/contingent-planning/) and [POMDP planning](/pomdp-planning/).

## In plain words

You are in a dark building and do not know which room you are in. You can still write a list of the rooms that you can be in. When you walk, each room on the list is replaced by the rooms that the walk can take you to. When you touch a door, you strike off each room that has no door there. The list is your belief.

A plan for the dark building is a plan for the list. You know the list at each moment, even if you do not know the room. So you can plan as if the list were the place where you are, and the plan works when the list holds only rooms of the goal. If you also know how likely each room is, the list gets a weight for each room, and touching a door changes the weights by Bayes' rule.

## The idea

**Set beliefs.** Take a nondeterministic model: $F(s, a)$ is the set of the possible next states of the action $a$ in the state $s$, and $\Omega(s)$ is the set of observations that the sensor can give in $s$. A belief is a nonempty set $b \subseteq S$. The action $a$ is applicable in $b$ when it is applicable in every state of $b$. The update has two steps.

$$b_a = \bigcup_{s \in b} F(s, a), \qquad b_a^o = \{ s \in b_a : o \in \Omega(s) \}.$$

The first step is the progression, and the second is the filter. With $n$ states there are $2^n - 1$ nonempty set beliefs. A goal is achieved for sure in $b$ when $b \subseteq G$.

**Probabilistic beliefs.** Take a [POMDP](/pomdp/): $P(s' \mid s, a)$ is the transition law and $O(o \mid a, s')$ the observation law. A belief is a distribution $b$ over $S$, and the update is [Bayes' rule](/bayes-theorem/),

$$b_a(s') = \sum_s P(s' \mid s, a) \, b(s), \qquad b_a^o(s') = \frac{O(o \mid a, s') \, b_a(s')}{\sum_{t} O(o \mid a, t) \, b_a(t)}.$$

The derivation is on the [POMDP](/pomdp/) page. The probabilistic beliefs form the simplex $\Delta(S)$, a set of dimension $|S| - 1$ in $\mathbb{R}^{|S|}$. For two states, a belief is one number $b(s_1) \in [0, 1]$.

**The two forms agree on the support.** If the nondeterministic model has $F(s, a) = \{ s' : P(s' \mid s, a) > 0 \}$ and $\Omega(s') = \{ o : O(o \mid a, s') > 0 \}$, then the support of $b_a^o$ is the set update of the support of $b$. So the set belief tells what is possible, and the probabilistic belief adds how likely it is. Planning for a goal that must hold with probability 1 can use the set belief only.

**Belief space is fully observable.** The agent computes its belief from the start belief and the history of actions and observations. So the belief is always known. A plan for a problem with hidden state is a policy on beliefs.

- With no observations, each action maps a belief to one belief. Belief space is then a deterministic [state space](/state-space/), and a conformant plan is a path in it.
- With observations, an action maps a belief to one belief for each observation. A contingent plan is a tree or a graph in belief space, with a branch for each observation.
- With probabilities, the belief moves to $b_a^o$ with the probability $\Pr(o \mid b, a)$. This is the belief MDP of a POMDP, and it has a continuous state space.

**Representations.** An explicit set or vector has up to $|S|$ entries, and $|S|$ is itself exponential in the number of state variables. Planners use compact forms: [binary decision diagrams](/binary-decision-diagram/) for set beliefs, formulas in CNF or DNF, translations that give a classical planner the literals "it is known that $x$", and for probabilities, factored models or samples, as in a [particle filter](/particle-filter/). Belief tracking, the computation of the current belief, is a hard problem by itself when the state has many variables.

## Examples

**A corridor with doors.** Cells $1, 2, 3, 4$; doors at the cells 1 and 3. The action right moves one cell to the right, and stays at 4. The sensor says "door" or "wall". It is correct with probability $4/5$. The start belief is uniform.

| step | belief over the cells 1, 2, 3, 4 |
|---|---|
| start | $(1/4, 1/4, 1/4, 1/4)$ |
| the sensor says door | $(2/5, 1/10, 2/5, 1/10)$ |
| right | $(0, 2/5, 1/10, 1/2)$ |
| the sensor says wall | $(0, 16/37, 1/37, 20/37)$ |

The observation "wall" had probability $37/50$ before it came. With a sensor that is never wrong, the set beliefs are $\{1, 2, 3, 4\}$, then $\{1, 3\}$ after "door", then $\{2, 4\}$ after right and "wall".

**Moving with no sensor.** In the same corridor, with left that stays at 1, the set beliefs after one, two and three moves left are $\{1, 2, 3\}$, $\{1, 2\}$ and $\{1\}$. Three moves locate the agent without any observation. This is a conformant plan for the goal "be at 1".

**The tiger.** In the tiger problem of the [POMDP](/pomdp/) page, the state is the side of the tiger, so the belief is one number, the probability of "left". Each "listen" moves it by Bayes' rule, and opening a door resets it to $1/2$.

**Not a belief.** The true state is not a belief: the agent cannot compute it from what it saw. A belief is also not the same as the set of the states that are reachable from the start. That set ignores the observations, so it is larger than the belief once the agent has seen something.

## Where it is used

- [Conformant planning](/conformant-planning/) searches the deterministic graph of set beliefs from the start belief to a belief inside the goal.
- [Contingent planning](/contingent-planning/) searches the AND-OR graph of set beliefs, with an AND branch for the observations.
- [Planning as model checking](/planning-as-model-checking/) represents set beliefs and their images with binary decision diagrams.
- [POMDP planning](/pomdp-planning/) solves the belief MDP. Its finite-horizon value is piecewise linear and convex over the simplex, and [point-based value iteration](/point-based-value-iteration/) backs it up only at a finite set of beliefs.
- [Execution monitoring](/execution-monitoring/) compares the current belief with what the plan expects.
- [Plan recognition](/plan-recognition/) keeps a belief over the goals of another agent, and updates it with each observed action.
- State estimation in robotics uses the same update. The forward step of a [hidden Markov model](/hidden-markov-model/) and the [particle filter](/particle-filter/) compute probabilistic beliefs.

## References
