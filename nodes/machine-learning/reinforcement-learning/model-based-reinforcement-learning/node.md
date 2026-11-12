---
tag: 1JFJ2J
kind: concept
slug: model-based-reinforcement-learning
name: Model-based reinforcement learning
aliases:
- model-based RL
area: machine-learning/reinforcement-learning
level: core
summary: "Learn the transition probabilities and rewards from experience, then plan on the learned model. Errors in the model limit the quality of the plan."
prereqs: [markov-decision-process, value-iteration]
see_also: [dyna-q, prioritized-sweeping, muzero, mdp-planning, rl-control, exploration-exploitation-tradeoff, q-learning, offline-reinforcement-learning]
sources:
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Chapter 8 (Section 8.1 on models and planning, Sections 8.2 and 8.3 on Dyna and model errors)
  - paper: doi:10.1023/A:1017984413808
    title: "Michael Kearns and Satinder Singh, Near-optimal reinforcement learning in polynomial time, Machine Learning 49(2-3), 2002, pages 209 to 232"
    locator: the E3 algorithm, known and unknown states, and the simulation lemma
  - paper: "Ronen I. Brafman and Moshe Tennenholtz, R-max, a general polynomial time algorithm for near-optimal reinforcement learning, Journal of Machine Learning Research 3, 2002, pages 213 to 231"
    locator: the R-max algorithm, its optimistic model of unknown pairs, and the polynomial bound
---

Model-based reinforcement learning learns an estimate of the transition probabilities and expected rewards of a [Markov decision process](/markov-decision-process/) from experience, and then plans on that estimate, for example with [value iteration](/value-iteration/). A model can be reused for many planning steps without new trials, so it usually needs far fewer real transitions than model-free methods, but the errors of the model limit the quality of the plan.

## In plain words

An agent that learns by trial and error can do one of two things with what it sees. It can change its opinion of its actions directly. Or it can first learn how the world works, which actions lead where and what they pay, and then work out good actions by thinking ahead with that learned picture. The second way is model-based learning.

The learned picture can be used again and again without new trials, so a model-based agent usually needs far fewer real trials. The risk is that the picture is wrong. A plan made with a wrong picture can be bad, and the agent may be very sure of it. So a model-based agent must also decide where to look to make its picture better.

## The idea

A model of a Markov decision process is an estimate $\hat P(s' \mid s, a)$ of the transition probabilities and $\hat R(s, a)$ of the expected rewards. Model-based reinforcement learning splits [the control problem](/rl-control/) into two parts: learning the model from transitions, which is a statistics problem, and solving the model, which is the [MDP planning problem](/mdp-planning/). Model-free methods such as [Q-learning](/q-learning/) skip the model and learn values or policies directly.

**Certainty equivalence.** The simplest plan is to act as if the estimate were the truth. In a tabular MDP, the maximum-likelihood model counts: with $N(s, a)$ visits to $(s, a)$, $N(s, a, s')$ of them leading to $s'$, and a reward sum $\Sigma(s, a)$,

$$\hat P(s' \mid s, a) = \frac{N(s, a, s')}{N(s, a)}, \qquad \hat R(s, a) = \frac{\Sigma(s, a)}{N(s, a)}.$$

The agent solves $(\hat P, \hat R, \gamma)$ with [value iteration](/value-iteration/) or [policy iteration](/policy-iteration/) and acts greedily with respect to the result. The implementation does this with ε-greedy exploration and a new plan every $K$ steps:

```pseudo id=main
CERTAINTY-EQUIVALENCE(environment, γ, ε, K, number of steps)
L1  N(s, a, s′) ← 0, N(s, a) ← 0, Σ(s, a) ← 0 for all s, a, s′; π ← greedy for the empty model
L2  for t ← 1 to the number of steps do
L3      A ← π(S) with probability 1 − ε, else a uniformly random action
L4      take A in S; observe the reward R and the next state S′
L5      N(S, A, S′) ← N(S, A, S′) + 1; N(S, A) ← N(S, A) + 1; Σ(S, A) ← Σ(S, A) + R
L6      if t is a multiple of K or the last step then
L7          P̂ ← N(s, a, s′)/N(s, a); R̂ ← Σ(s, a)/N(s, a)      ▷ a pair with no data is a self-loop with reward r_unknown
L8          V̂, π ← value iteration on (P̂, R̂, γ), and the greedy policy for V̂
L9      S ← S′
L10 return (P̂, R̂), π, V̂
```

**How wrong the plan can be.** The simulation lemma of Kearns and Singh bounds the effect of model errors. Let $\varepsilon_P = \max_{s, a}\sum_{s'}|\hat P(s' \mid s, a) - P(s' \mid s, a)|$, let $\varepsilon_R = \max_{s, a}|\hat R(s, a) - R(s, a)|$, and let $R_{\max} = \max_{s, a}|R(s, a)|$. For every stationary policy $\pi$,

$$\lVert \hat V^\pi - V^\pi \rVert_\infty \le \delta = \frac{1}{1 - \gamma}\Big(\varepsilon_R + \frac{\gamma\,\varepsilon_P R_{\max}}{1 - \gamma}\Big).$$

The proof is one line: $\hat V^\pi - V^\pi = (I - \gamma\hat P_\pi)^{-1}[(\hat R_\pi - R_\pi) + \gamma(\hat P_\pi - P_\pi)V^\pi]$, the inverse has norm at most $1/(1 - \gamma)$, and $\lVert V^\pi \rVert_\infty \le R_{\max}/(1 - \gamma)$. If $\hat\pi$ is optimal for the model and $\pi^*$ for the true MDP, then $V^{\hat\pi} \ge \hat V^{\hat\pi} - \delta \ge \hat V^{\pi^*} - \delta \ge V^* - 2\delta$. So the plan loses at most $2\delta$. The factor $1/(1-\gamma)^2$ in front of $\varepsilon_P$ says that the plan is very sensitive to transition errors when the horizon is long.

**Model bias.** The bound is small only where the model is accurate. Where the agent has little data, the model can be far off, and the planner will find and use these errors, for example a transition that looks like a shortcut but does not exist. This is called model bias. A certainty-equivalence agent with too little exploration can stay with a bad policy forever, because it never visits the states that would show that the model is wrong.

**Exploration with a model.** Two classic algorithms give polynomial bounds on the number of steps that are not near-optimal.

- **E3** (Kearns and Singh 2002) calls a state known when all its actions have enough samples. It plans on the known part of the model. If that plan is good enough, it exploits. Otherwise it plans a path to an unknown state and explores there.
- **R-max** (Brafman and Tennenholtz 2002) is simpler. It treats every pair with fewer than $m$ samples as a jump to a fictional state that pays the largest reward $R_{\max}$ forever, and it always acts greedily on this optimistic model. The plan then goes to unknown pairs by itself, or it is near-optimal. The implementation has the same option: with $r_{\text{unknown}} = R_{\max}$ an untried pair is a self-loop that pays $R_{\max}$.

The [exploration and exploitation trade-off](/exploration-exploitation-tradeoff/) page covers the general problem.

## Examples

- **Dyna.** [Dyna-Q](/dyna-q/) learns a table model of a deterministic environment and plans with it by replaying Q-learning updates. [Prioritized sweeping](/prioritized-sweeping/) plans on a count model, in the order of the Bellman errors.
- **Convergence of the count model.** The tests run the implementation on random MDPs with full support and noisy rewards. With random actions, after 600 steps on at most 3 states, the loss of the learned policy is always within $2\delta$ of the optimum, with $\delta$ from the measured errors. On 10 MDPs with 4 states and 2 actions, with $\varepsilon = 0.5$ and 40000 steps, the row errors of $\hat P$ fall below $0.1$, the reward errors below $0.05$, and the learned policy is exactly optimal.
- **The simulation lemma.** The tests also draw 500 random pairs of true and wrong models and random policies, and check the bound $\lVert \hat V^\pi - V^\pi \rVert_\infty \le \delta$ and the loss of at most $2\delta$ for the plan.
- **Learned models with planning by search.** [MuZero](/muzero/) learns a model of rewards, values and policies in a latent space and plans with Monte Carlo tree search. It does not try to predict the next observation.

## Where it is used

Model-based methods are used when real experience is expensive and computation is cheap, as in robotics, control of physical systems, and settings where a simulator must be learned from logs. Known models are used in board games, where the rules give the model exactly and search does the planning. Model-based offline methods fit a model to a fixed dataset and plan with a penalty for uncertainty, which is one approach to [offline reinforcement learning](/offline-reinforcement-learning/). In theory, the tabular algorithms E3 and R-max were among the first with sample complexity bounds that are polynomial in the number of states and actions, the horizon and the accuracy.

With function approximation, model errors grow when the planner looks many steps ahead, because each predicted state is used as the input of the next prediction. Practical methods therefore plan over short horizons, use ensembles of models to estimate their uncertainty, or learn only the parts of the model that planning needs, as MuZero does.

## References
