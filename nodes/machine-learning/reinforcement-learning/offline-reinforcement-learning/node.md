---
tag: N9RY82
kind: problem
slug: offline-reinforcement-learning
name: Offline reinforcement learning
aliases:
- batch reinforcement learning
- offline RL
area: machine-learning/reinforcement-learning
level: advanced
summary: "Learn a good policy for an unknown MDP from a fixed dataset of transitions, with no further interaction; the core difficulty is the shift between the data and the learned policy."
prereqs: [markov-decision-process, rl-control]
see_also: [conservative-q-learning, fitted-q-iteration, off-policy-evaluation, importance-sampling-off-policy, imitation-learning, deadly-triad, experience-replay]
sources:
  - paper: "Sergey Levine, Aviral Kumar, George Tucker and Justin Fu, Offline reinforcement learning, tutorial, review, and perspectives on open problems, arXiv:2005.01643, 2020"
    locator: Section 2 (problem statement and why offline RL is hard), Section 4 (policy constraints, uncertainty and conservative methods), Section 5 (model-based offline RL)
  - paper: doi:10.1007/978-3-642-27645-3_2
    title: "Sascha Lange, Thomas Gabel and Martin Riedmiller, Batch reinforcement learning, in Marco Wiering and Martijn van Otterlo (editors), Reinforcement Learning, State-of-the-Art, Springer, 2012, pages 45 to 73"
    locator: the definition of the batch problem and the fitted Q-iteration family
  - paper: "Scott Fujimoto, David Meger and Doina Precup, Off-policy deep reinforcement learning without exploration, Proceedings of the 36th International Conference on Machine Learning (ICML), PMLR 97, 2019, pages 2052 to 2062"
    locator: extrapolation error, and batch-constrained Q-learning (BCQ)
  - paper: "Aviral Kumar, Aurick Zhou, George Tucker and Sergey Levine, Conservative Q-learning for offline reinforcement learning, NeurIPS 2020, arXiv:2006.04779"
    locator: the conservative value family and its lower-bound theorems
  - paper: "Ying Jin, Zhuoran Yang and Zhaoran Wang, Is pessimism provably efficient for offline RL?, Proceedings of the 38th International Conference on Machine Learning (ICML), PMLR 139, 2021"
    locator: pessimistic value iteration and its suboptimality bound under coverage of the optimal policy
  - paper: "Paria Rashidinejad, Banghua Zhu, Cong Ma, Jiantao Jiao and Stuart Russell, Bridging offline reinforcement learning and imitation learning, a tale of pessimism, Advances in Neural Information Processing Systems 34 (NeurIPS 2021)"
    locator: single-policy concentrability, and the matching upper and lower bounds in the tabular case
---

Offline reinforcement learning, also called batch reinforcement learning, is the [control problem](/rl-control/) of reinforcement learning with one change: the agent gets a fixed dataset of transitions and cannot act in the environment to get more. The data was collected earlier by some behavior policy, possibly a mix of people, programs and older agents. The goal is still a policy with high expected return. The problem matters wherever trying things is costly or unsafe, such as in medicine, robotics and recommender systems, and where large logs already exist.

## In plain words

You get a large record of what others did and what happened next. You must use it to find a good way to act, and you cannot test your ideas before you use them.

The record can show that some choices worked and others did not. It cannot show what would have happened after a choice that nobody made. A method that guesses too boldly about such choices will pick them, because the guess looks good, and then fail. So offline methods must stay close to what the record supports, while still doing better than the people who made the record when the record shows how.

## Definition

**Input.** A finite discount $\gamma \in [0, 1)$ (or a horizon $H$), and a dataset $D = \{(s_i, a_i, r_i, s'_i)\}_{i=1}^N$ of transitions of an unknown [Markov decision process](/markov-decision-process/) $M = (S, A, P, R, \gamma)$. In the standard model, the pairs $(s_i, a_i)$ come from a data distribution $d_\beta$, often the state-action distribution of a behavior policy $\pi_\beta$, and $r_i$ and $s'_i$ are drawn from $R(s_i, a_i)$ and $P(\cdot \mid s_i, a_i)$. The algorithm may not query $M$.

**Output.** A policy $\hat\pi$.

**Goal.** Small suboptimality $J(\pi^\star) - J(\hat\pi)$, or, more modestly, $J(\pi) - J(\hat\pi)$ small for the best policy $\pi$ that the data covers, where $J(\pi) = \mathbb{E}\big[\sum_t \gamma^t r_t\big]$ from a start distribution $\rho$.

**Coverage.** Guarantees depend on how well $d_\beta$ covers the state-action distribution $d^\pi$ of the policies of interest. The *concentrability* of $\pi$ is $C^\pi = \max_{s, a} d^\pi(s, a) / d_\beta(s, a)$. Older results need $C^\pi$ bounded for every policy $\pi$ (all-policy coverage); newer pessimistic methods need it only for one good policy (single-policy coverage).

## Variants

- **Horizon.** Discounted infinite horizon, or finite horizon $H$ with episodes in the data.
- **Data source.** Expert data (then [imitation learning](/imitation-learning/) applies), random data, mixed or replay data.
- **Offline policy evaluation.** Estimate $J(\pi)$ for a given $\pi$ from $D$, without the control step: [off-policy evaluation](/off-policy-evaluation/).
- **Offline-to-online.** Pretrain offline, then fine-tune with a small online budget.
- **Function class.** Tabular, linear, or general classes with realizability and completeness assumptions.

## Examples

**No coverage, no guarantee.** Two one-state problems with two actions: in both, action 1 pays 0, and action 2 pays $+1$ in $M_1$ and $-1$ in $M_2$. Let $D$ contain only action 1. The data has the same distribution under $M_1$ and $M_2$, so every algorithm outputs the same (random) policy $\hat\pi$ on both. If $\hat\pi$ plays action 2 with probability $p$, the suboptimality is $1 - p$ on $M_1$ and $p$ on $M_2$, and the larger of the two is at least $\tfrac12$. With $p = 0$ (stay with the data) the loss on $M_2$ is 0, and on $M_1$ it is 1, the cost of a policy that the data could never have justified.

**The corridor.** On the [conservative Q-learning](/conservative-q-learning/) page, a 4-state corridor has data on "right" and "stay" but none on "left". Tabular [fitted Q-iteration](/fitted-q-iteration/) leaves "left" at its initial value 0, which is above its true value, so its greedy policy goes left forever, with value $-10$. CQL drives the value of "left" down and returns the optimal policy, with value $-3.439$ from state 0.

## Known algorithms

The methods fall into three families (Levine and others, 2020), plus a few that do not fit them.

| family | idea | examples |
|---|---|---|
| policy constraints | keep $\hat\pi$ close to $\pi_\beta$ (support, KL or behavior cloning term) | BCQ (Fujimoto, Meger and Precup, 2019), BEAR, BRAC, TD3+BC |
| pessimistic values | lower the values of poorly covered actions | [CQL](/conservative-q-learning/), ensemble and uncertainty penalties, pessimistic value iteration |
| pessimistic models | learn a model, penalize its uncertainty, plan in it | MOPO, MOReL, COMBO |

Others: [fitted Q-iteration](/fitted-q-iteration/) and neural fitted Q-iteration, the original batch methods without any pessimism (Lange, Gabel and Riedmiller, 2012); in-sample methods such as implicit Q-learning, which never evaluate actions outside the data; filtered and weighted [imitation learning](/imitation-learning/) (advantage-weighted regression); and return-conditioned sequence models such as the decision transformer.

## Bounds

- **Without coverage, nothing.** The two-MDP example above gives a worst-case suboptimality of at least $\tfrac12$ (times the reward range) for every algorithm when the data misses an action that could be the best one. So every guarantee needs a coverage assumption.
- **Pessimism with single-policy coverage.** Pessimistic value iteration (Jin, Yang and Wang, 2021) bounds the suboptimality with respect to any policy $\pi$ by a sum of uncertainty terms along the trajectories of $\pi$, so it needs only $\pi$ to be covered. In the tabular case, Rashidinejad and others (2021) show that the suboptimality of a pessimistic method against $\pi^\star$ shrinks like $\sqrt{S C^{\pi^\star} / N}$, times a polynomial in the effective horizon and up to logarithmic factors, and that this rate is optimal for the worst case.
- **Function approximation is harder.** With linear function approximation, realizability of the values of every policy and good coverage of the features are not enough in general: some problems need a number of samples that is exponential in the horizon (Wang, Foster and Kakade, 2021).

## Reductions

- **To planning.** With all pairs covered, build the empirical MDP from $D$ and solve it with [value iteration](/value-iteration/). This is certainty equivalence; tabular fitted Q-iteration computes it.
- **From imitation learning.** If $D$ comes from an expert, behavior cloning is an offline method that needs no rewards; offline RL is the setting where the data may be worse than the goal.
- **To off-policy evaluation.** Any offline evaluation method gives a slow control method: evaluate a set of candidate policies and pick the best. Errors in [importance sampling](/importance-sampling-off-policy/) estimates then decide the choice.
- **From online RL.** An online algorithm whose [replay buffer](/experience-replay/) is filled once and never refreshed is an offline algorithm, and usually a poor one, because of the [deadly triad](/deadly-triad/).

## Applications

Treatment policies from hospital records, robot grasping from logged attempts, dialogue and recommendation policies from user logs, and control of industrial plants and data center cooling, where online exploration is unsafe or slow. D4RL and RL Unplugged are standard benchmarks.

## References
