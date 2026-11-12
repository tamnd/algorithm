---
tag: QWHW45
kind: model
slug: options-framework
name: Options framework
aliases:
- semi-MDP options
- temporally extended actions
area: machine-learning/reinforcement-learning
level: research
summary: "An option is a policy with a start set and a stop rule. An MDP with options is a semi-MDP, so value iteration and Q-learning work over options, with discounted multi-step models."
prereqs: [markov-decision-process, value-iteration]
see_also: [q-learning, dyna-q, hidden-semi-markov-model, policy-gradient-theorem, actor-critic, potential-based-reward-shaping, successor-representation, model-based-reinforcement-learning]
sources:
  - paper: doi:10.1016/S0004-3702(99)00052-1
    title: "Richard S. Sutton, Doina Precup and Satinder Singh, Between MDPs and semi-MDPs, a framework for temporal abstraction in reinforcement learning, Artificial Intelligence 112(1-2), 1999, pages 181 to 211"
    locator: "Section 2 (options), Theorem 1 (MDP plus options is an SMDP), Section 3 (option models and SMDP planning, the four-rooms gridworld), Section 4 (interrupting options), Section 5 (intra-option learning)"
  - paper: "Pierre-Luc Bacon, Jean Harb and Doina Precup, The option-critic architecture, Proceedings of the Thirty-First AAAI Conference on Artificial Intelligence, 2017, pages 1726 to 1734"
    locator: the intra-option policy gradient theorem and the termination gradient theorem
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: Chapter 11 (semi-Markov decision processes)
  - paper: "Doina Precup, Temporal abstraction in reinforcement learning, PhD thesis, University of Massachusetts Amherst, 2000"
    locator: option models, intra-option learning and their convergence
  - paper: "Thomas G. Dietterich, Hierarchical reinforcement learning with the MAXQ value function decomposition, Journal of Artificial Intelligence Research 13, 2000, pages 227 to 303"
    locator: the MAXQ hierarchy and recursive optimality
  - paper: "Ronald Parr and Stuart Russell, Reinforcement learning with hierarchies of machines, Advances in Neural Information Processing Systems 10, 1998"
    locator: hierarchies of abstract machines (HAMs)
---

The options framework (Sutton, Precup and Singh, 1999) adds *temporally extended actions* to a [Markov decision process](/markov-decision-process/). An option is a closed-loop policy together with the set of states where it may start and a rule that says when it stops: "walk to the door", "pick up the cup". An agent may choose an option instead of a primitive action, and then follows it until it stops. The main theorem says that an MDP with a fixed set of options is a semi-Markov decision process (SMDP) over those options, so planning and learning methods for MDPs, such as [value iteration](/value-iteration/) and [Q-learning](/q-learning/), carry over with one change: each option has a discounted multi-step model in place of a one-step model. Primitive actions are options that last one step, so the framework includes the plain MDP.

## The machine

Fix a finite MDP $(S, A, P, R, \gamma)$ with $\gamma < 1$. A **Markov option** is a triple $o = (I, \pi, \beta)$:

- $I \subseteq S$ is the *initiation set*: the option may start only in a state of $I$.
- $\pi(a \mid s)$ is the option's policy, followed while the option runs.
- $\beta(s) \in [0, 1]$ is the *termination condition*: after each step, in the new state $s$, the option stops with probability $\beta(s)$.

A primitive action $a$ is the option with $I = \{s : a \text{ is allowed in } s\}$, $\pi(a \mid s) = 1$ and $\beta \equiv 1$. A *semi-Markov option* may let $\pi$ and $\beta$ depend on the whole history since the option started, for example to stop after a fixed number of steps.

A policy over options $\mu(o \mid s)$ picks an option in the current state; the option runs until it stops at some state $s'$ after $k$ steps; $\mu$ picks again in $s'$. The **model of option $o$** at a start state $s \in I$ is

$$R_o(s) = \mathbb{E}\big[r_1 + \gamma r_2 + \cdots + \gamma^{k-1} r_k\big], \qquad P_o(s' \mid s) = \sum_{j \ge 1} \gamma^j \Pr(k = j, s_k = s'),$$

where $k$ is the random duration. The discount is folded into $P_o$, so $\sum_{s'} P_o(s' \mid s) = \mathbb{E}[\gamma^k] < 1$. With these models, the Bellman optimality equation over a set of options $O$ is

$$V^*_O(s) = \max_{o \in O,\ s \in I_o} \Big[R_o(s) + \sum_{s'} P_o(s' \mid s)\, V^*_O(s')\Big].$$

For a Markov option, both parts of the model are fixed points of linear equations over the states where the option continues, so one linear solve computes them:

```pseudo id=model
OPTION-MODEL(o = (I, π, β), P, R, γ)
M1  for each start state s and each step, draw a ~ π(· | s) and s′ ~ P(· | s, a)
M2  R_o(s) = Σ_a π(a | s) [R(s, a) + γ Σ_s′ P(s′ | s, a) (1 − β(s′)) R_o(s′)]
M3  P_o(x | s) = Σ_a π(a | s) γ Σ_s′ P(s′ | s, a) [(1 − β(s′)) P_o(x | s′)
M4                                                  + β(s′) [s′ = x]]
M5  solve the linear equations M2 to M4 for R_o and P_o
```

SMDP value iteration then backs up over options:

```pseudo id=main
SMDP-VALUE-ITERATION(S, O, models R_o and P_o, ε)
L1  V ← 0
L2  repeat
L3      V′(s) ← max over o with s ∈ I_o of R_o(s) + Σ_x P_o(x | s) V(x), for each s
L4      δ ← max_s |V′(s) − V(s)|;  V ← V′
L5  until δ < ε
L6  return V, and in each s an option that attains the max of L3
```

The map in line L3 is a contraction in the max norm with factor $\max_{o, s} \mathbb{E}_s[\gamma^k] \le \gamma$, so the loop converges to $V^*_O$.

## What it counts

- **Planning:** sweeps of line L3 until the error is below $\varepsilon$. With long options the factor $\mathbb{E}[\gamma^k]$ is smaller than $\gamma$, and the value moves many cells in one sweep.
- **Learning:** samples (steps in the environment) to learn $V^*_O$ or $Q^*_O$. SMDP Q-learning updates $Q(s, o) \leftarrow Q(s, o) + \alpha\big[r + \gamma r_2 + \cdots + \gamma^{k-1} r_k + \gamma^k \max_{o'} Q(s', o') - Q(s, o)\big]$ once per option execution. Intra-option methods update every option consistent with each primitive step.
- **Quality:** the loss $V^* - V^*_O$ from using only the options in $O$.

**Example.** The implementation uses its own four-rooms grid: a $9 \times 9$ map with walls, four rooms of $3 \times 3$ cells, and four one-cell hallways, 40 cells in all. Each move goes in the intended direction with probability $2/3$ and in each other direction with probability $1/9$; a move into a wall stays. Entering the goal cell (in the bottom-right room) pays 1 and ends the episode; $\gamma = 0.9$. The eight hallway options lead from inside a room to one of its two hallways along a shortest path, and stop as soon as the agent leaves the room's interior. The results:

| options in $O$ | all 39 values nonzero after | max error after 10 sweeps | $V$ at the far corner |
|---|---|---|---|
| 4 primitives | 11 sweeps | 0.180 | 0.1556 |
| 4 primitives and 8 hallway options | 3 sweeps | 0.031 | 0.1556 |
| 8 hallway options only | | | 0.0512 |

With the primitives included, the fixed point equals the $V^*$ of plain value iteration to within $10^{-9}$ in every state, but the value spreads from the goal in fewer sweeps. With hallway options only, the agent can reach the goal's room but has no option that walks to the goal, so it gets there only by accident, and $V^*_O$ is well below $V^*$.

## Relation to other models

- **MDP.** With $O = A$ (one-step options), the model is the MDP, and line L3 is the Bellman optimality backup of [value iteration](/value-iteration/).
- **SMDP.** Theorem 1 of Sutton, Precup and Singh: an MDP with a set of options, where each option runs to termination, is an SMDP whose actions are the options, with $R_o$ and $P_o$ as its model. SMDPs (Puterman, Chapter 11) allow random holding times between decisions.
- **Hidden semi-Markov models.** A [hidden semi-Markov model](/hidden-semi-markov-model/) has explicit durations in each hidden state; an option's duration is instead set by its termination rule and the dynamics.
- **Other hierarchies.** Hierarchies of abstract machines (Parr and Russell, 1998) restrict the policy by finite machines; MAXQ (Dietterich, 2000) decomposes the value function along a task hierarchy and aims at recursive optimality. Feudal methods give goals to lower levels. Options are the simplest of these: they only add actions.
- **Policy gradients.** The option-critic architecture (Bacon, Harb and Precup, 2017) learns the option policies and termination functions together with the policy over options, by the intra-option policy gradient theorem and the termination gradient theorem, two analogues of the [policy gradient theorem](/policy-gradient-theorem/) for [actor-critic](/actor-critic/) learning.
- **Models for planning.** Option models are multi-step models for [Dyna](/dyna-q/)-style and [model-based](/model-based-reinforcement-learning/) planning. The [successor representation](/successor-representation/) is a related multi-step quantity that is used to find options.

## Known results in the model

- **Options form an SMDP** (Sutton, Precup and Singh, 1999, Theorem 1). So SMDP value iteration, SMDP policy iteration and SMDP Q-learning apply, with the usual convergence results for SMDPs.
- **Adding options to the primitives keeps the optimum.** If $A \subseteq O$ (every primitive action is available as an option), then $V^*_O = V^*$. If $O$ does not include the primitives, $V^*_O \le V^*$, with strict inequality in general, as the hallway-only row of the example shows.
- **Interruption.** Running each option until it ends can be improved: stopping an option $o$ early whenever some option has a higher value $Q_\mu(s, o') > Q_\mu(s, o)$ gives a policy that is at least as good as $\mu$ in every state (Sutton, Precup and Singh, Section 4).
- **Intra-option learning.** For Markov options, one primitive transition is a valid sample for every option whose policy would have chosen that action. Intra-option Q-learning uses each step to update all such options, and converges to $Q^*_O$ under the usual step size and exploration conditions (Section 5 of the paper; Precup, 2000).
- **Finding good options** is open in general. Methods use bottleneck states, graph cuts, eigenvectors of the transition graph (eigenoptions), the successor representation, or gradient methods such as option-critic. Badly chosen options can slow learning, because they add choices without shortening the search.

## References
