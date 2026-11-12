---
tag: SSS4DF
kind: definition
slug: policy
name: Policy
aliases:
- stochastic policy
- deterministic policy
- stationary policy
- Markov policy
area: machine-learning/reinforcement-learning
level: intro
summary: The rule by which an agent in an MDP picks its actions, as a map from states or histories to actions or to distributions over actions.
prereqs: [markov-decision-process]
see_also: [state-value-function, action-value-function, stationary-distribution, epsilon-greedy, policy-iteration, policy-gradient-theorem]
sources:
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: "Section 2.1 (decision rules and the policy classes HR, HD, MR, MD, SR, SD), Section 5.5 (Markov policies give the same state-action frequencies), Theorem 6.2.10"
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: "Section 3.5 (policies and value functions)"
  - book: isbn:9781608454921
    title: Csaba Szepesvári, Algorithms for Reinforcement Learning, Morgan and Claypool, 2010
    locator: "Chapter 2 (Markov decision processes, policies and value functions)"
---

A policy is the rule by which an agent in a [Markov decision process](/markov-decision-process/) picks its actions. In general it maps the history of the process to a probability distribution over the allowed actions. The common special cases are deterministic (one action), Markov (only the current state counts) and stationary (the same rule at each step). A policy together with an initial state distribution fixes the law of the whole trajectory, and so its [value](/state-value-function/).

## Definition

Let $(S, A, P, R, \gamma)$ be a finite MDP with allowed action sets $A(s)$, and let $\Delta(X)$ be the set of probability distributions on a finite set $X$. A *history* at time $t$ is $h_t = (s_0, a_0, s_1, a_1, \ldots, s_t)$.

- A *decision rule* at time $t$ is a map $d_t$ from histories $h_t$ to $\Delta(A(s_t))$. We write $d_t(a \mid h_t)$ for the probability of action $a$.
- A *policy* is a sequence $\pi = (d_0, d_1, d_2, \ldots)$ of decision rules. At time $t$ the agent draws $A_t \sim d_t(\cdot \mid H_t)$.

The policy classes of Puterman (Section 2.1) come from three restrictions:

| restriction | meaning |
|---|---|
| Markov | $d_t(\cdot \mid h_t)$ depends on $h_t$ only through the current state $s_t$ |
| stationary | Markov, and $d_t = d_0$ for every $t$ |
| deterministic | each $d_t(\cdot \mid h_t)$ puts probability 1 on one action |

This gives the classes history dependent randomized (HR), history dependent deterministic (HD), Markov randomized (MR), Markov deterministic (MD), stationary randomized (SR) and stationary deterministic (SD), with $\mathrm{SD} \subseteq \mathrm{SR} \subseteq \mathrm{MR} \subseteq \mathrm{HR}$ and $\mathrm{SD} \subseteq \mathrm{MD} \subseteq \mathrm{HD} \subseteq \mathrm{HR}$. In reinforcement learning, "a policy" without more words usually means a stationary randomized policy $\pi(a \mid s)$, and a deterministic stationary policy is written as a function $\pi : S \to A$.

**The induced process.** A stationary policy $\pi$ turns the MDP into a [Markov chain](/markov-chain/) with the matrix and the reward vector

$$P^\pi(s, s') = \sum_{a} \pi(a \mid s)\, P(s' \mid s, a), \qquad R^\pi(s) = \sum_a \pi(a \mid s)\, R(s, a).$$

From an initial distribution $\mu$ (a row vector), the law of $S_t$ is $\mu (P^\pi)^t$. The *discounted state occupancy* is

$$d^\pi_\mu(s) = (1 - \gamma) \sum_{t=0}^{\infty} \gamma^t \Pr\nolimits^\pi_\mu(S_t = s), \qquad d^\pi_\mu = (1-\gamma)\, \mu\, (I - \gamma P^\pi)^{-1}.$$

It is a probability distribution, because the weights $(1-\gamma)\gamma^t$ add up to 1. The expected value of the policy from $\mu$ is then

$$\sum_s \mu(s) V^\pi(s) = \frac{1}{1-\gamma} \sum_s d^\pi_\mu(s)\, R^\pi(s).$$

The proof is one line: $V^\pi = (I - \gamma P^\pi)^{-1} R^\pi$ by the [Bellman expectation equation](/bellman-expectation-equation/), so $\mu V^\pi = \mu (I - \gamma P^\pi)^{-1} R^\pi = d^\pi_\mu R^\pi / (1 - \gamma)$. For the average reward criterion the occupancy is replaced by the [stationary distribution](/stationary-distribution/) of $P^\pi$.

**Markov policies are enough for the marginals.** For each policy $\pi$, even a history dependent one, and each $\mu$, there is a Markov randomized policy $\pi'$ with $\Pr^{\pi'}_\mu(S_t = s, A_t = a) = \Pr^\pi_\mu(S_t = s, A_t = a)$ for every $t$, $s$ and $a$ (Puterman, Section 5.5). Take $\pi'_t(a \mid s) = \Pr^\pi_\mu(S_t = s, A_t = a) / \Pr^\pi_\mu(S_t = s)$ when the denominator is positive, and any distribution when it is 0. By induction on $t$: the laws of $S_0$ agree because both are $\mu$. If the joint laws of $(S_t, A_t)$ agree, then the laws of $S_{t+1}$ agree, because by the Markov property $\Pr(S_{t+1} = s') = \sum_{s, a} \Pr(S_t = s, A_t = a) P(s' \mid s, a)$ for any policy. Then the joint laws at $t+1$ agree by the choice of $\pi'_{t+1}$. $\blacksquare$ Since the expected rewards depend only on these marginals, $\pi$ and $\pi'$ have the same value under all three criteria. Theorem 6.2.10 of Puterman goes further for the discounted criterion: one deterministic stationary policy is optimal ([MDP](/markov-decision-process/)).

## Examples and non-examples

Take the two-state example of the [MDP page](/markov-decision-process/): in $s_1$, *stay* gives reward 1 and stays, *switch* gives 0 and moves to $s_2$ with probability 1/2; in $s_2$, *stay* gives 2 and stays with probability 3/4, *switch* gives 3 and moves to $s_1$; $\gamma = 9/10$.

- **Deterministic stationary.** $\pi(s_1) = $ switch, $\pi(s_2) = $ stay. This is the optimal policy, with values $360/31$ and $440/31$. Its chain is $P^\pi = \begin{pmatrix} 1/2 & 1/2 \\ 1/4 & 3/4 \end{pmatrix}$. From $s_1$ the law of $S_1$ is $(1/2, 1/2)$ and the law of $S_2$ is $(3/8, 5/8)$. The discounted occupancy from $s_1$ is $(13/31, 18/31)$, and indeed $\frac{1}{1-\gamma}(13/31 \cdot 0 + 18/31 \cdot 2) = 360/31 = V^\pi(s_1)$. The stationary distribution is $(1/3, 2/3)$, so the average reward is $2/3 \cdot 2 = 4/3$.
- **Stochastic stationary.** $\pi(\cdot \mid s) = (1/2, 1/2)$ in both states. Its chain is $\begin{pmatrix} 3/4 & 1/4 \\ 5/8 & 3/8 \end{pmatrix}$. An [epsilon-greedy](/epsilon-greedy/) policy and the softmax policies of the [policy gradient](/policy-gradient-theorem/) methods are stochastic stationary policies.
- **Markov, not stationary.** The optimal policy for the horizon 3 problem of the same MDP with no discount plays stay in $s_2$ at steps 0 and 1 and switch at step 2. Each finite horizon problem has such an optimal deterministic Markov policy, and it is often not stationary.
- **History dependent.** "In $s_1$, switch if the last reward was 0, else stay" looks at the past reward, so it is not Markov. By the result above it has the same value as some Markov randomized policy.
- **Non-example: looks ahead.** "Pick the action that leads to $s_2$ in this step" uses the random outcome of the step before it happens. A decision rule may use only $h_t$, so this is not a policy.
- **Non-example: unseen state.** In a [POMDP](/pomdp/) the agent does not see the state, so a map from states to actions is not a policy that the agent can run. The policies there are maps from observation histories, or from beliefs.
- **Non-example: not allowed.** A rule that picks an action outside $A(s)$ in some state $s$ is not a policy of that MDP.

## Related definitions

- [Markov decision process](/markov-decision-process/): the model that a policy acts in.
- [State value function](/state-value-function/) and [action value function](/action-value-function/): the expected return of a policy.
- [Advantage function](/advantage-function/): how much better one action is than the policy's own choice.
- [Policy evaluation](/policy-evaluation/) computes $V^\pi$; [policy iteration](/policy-iteration/) improves a policy step by step.
- [Stationary distribution](/stationary-distribution/): the long-run law of the chain $P^\pi$.
- [Options framework](/options-framework/): policies that act over several steps.

## References
