---
tag: DXW2GN
kind: algorithm
slug: natural-policy-gradient
name: Natural policy gradient
aliases:
- NPG
- Kakade's natural policy gradient
area: machine-learning/reinforcement-learning
level: advanced
summary: "Policy gradient ascent along F^-1 grad J, where F is the Fisher matrix of the policy averaged over visited states; for a softmax policy the step is the compatible critic's weights."
solves: [rl-control]
model: real-ram
complexity:
  vars: {K: the number of iterations, N: the number of episodes per iteration, T: the maximum episode length, A: the number of actions, m: the number of policy parameters}
  time: {worst: "O(K (N T (A m + m^2) + m^3))"}
  space: {extra: "O(m^2 + T)"}
properties: {deterministic: false, online: false, exact: false, recursive: false}
history:
  year: 2001
  people: [Sham M. Kakade]
  note: "Kakade defined the natural policy gradient with the Fisher matrix of the policy averaged over the stationary state distribution, and showed that it equals the weights of the compatible critic and moves toward the greedy policy."
prereqs: [policy-gradient-theorem, natural-gradient-descent, fisher-information-matrix]
see_also: [trpo, ppo, actor-critic, reinforce, policy-iteration, mirror-descent, advantage-function, policy-improvement-theorem]
sources:
  - paper: "Sham Kakade, A natural policy gradient, Advances in Neural Information Processing Systems 14, 2001, pages 1531 to 1538"
    locator: Equations (2) to (4) (the Fisher matrix F_s, its average over states, and the natural gradient), Section 3.1 Theorem 1 (compatible function approximation), Section 3.2 Theorems 2 and 3 (greedy policy improvement), Section 5 (the linear quadratic and Tetris experiments)
  - paper: doi:10.1016/j.neucom.2007.11.026
    title: "Jan Peters and Stefan Schaal, Natural actor-critic, Neurocomputing 71(7-9), 2008, pages 1180 to 1190"
    locator: the natural actor-critic algorithm, which estimates the natural gradient as the weights of a compatible critic
  - paper: "J. Andrew Bagnell and Jeff Schneider, Covariant policy search, Proceedings of the 18th International Joint Conference on Artificial Intelligence, 2003, pages 1019 to 1024"
    locator: the metric on trajectory distributions and its relation to Kakade's Fisher matrix
  - paper: "Alekh Agarwal, Sham M. Kakade, Jason D. Lee and Gaurav Mahajan, On the theory of policy gradient methods, optimality, approximation, and distribution shift, Journal of Machine Learning Research 22(98), 2021, pages 1 to 76"
    locator: the section on the natural policy gradient for the softmax parameterization (the multiplicative update and the O(1/T) rate without dependence on the size of the MDP)
  - paper: doi:10.1162/089976698300017746
    title: "Shun-ichi Amari, Natural gradient works efficiently in learning, Neural Computation 10(2), 1998, pages 251 to 276"
    locator: the natural gradient as steepest ascent in the Fisher metric
---

The natural policy gradient (NPG) of Kakade (2001) is [natural gradient](/natural-gradient-descent/) ascent on the expected return of a policy. It replaces the plain policy gradient $\nabla J(\theta)$ by $F(\theta)^{-1} \nabla J(\theta)$, where

$$F(\theta) = \sum_s d^{\pi}(s) \sum_a \pi_\theta(a \mid s)\, \nabla_\theta \log \pi_\theta(a \mid s)\, \nabla_\theta \log \pi_\theta(a \mid s)^\top$$

is the [Fisher information matrix](/fisher-information-matrix/) of the action distribution, averaged over the states that the policy visits. The step then depends on how the policy changes, not on how it is parameterized. Three facts make it central to policy optimization. First, $F^{-1} \nabla J$ is exactly the weight vector of the best *compatible* critic, so an actor-critic can read it off a linear regression. Second, for the tabular softmax policy, the natural gradient is the [advantage](/advantage-function/) $A^\pi(s, a)$ itself, so a step multiplies the policy by $e^{\eta A^\pi}$ in every state, a soft form of [policy iteration](/policy-iteration/) that never makes the policy worse. Third, with exact advantages this update converges at the rate $O(1/T)$ with no dependence on the number of states (Agarwal et al., 2021). [TRPO](/trpo/) and [PPO](/ppo/) are practical descendants.

## In plain words

A policy gradient method turns knobs that control the policy. The plain gradient says how much each knob changes the expected reward, but knobs differ: one knob may change the behaviour a lot, another hardly at all, and some knobs matter only in situations the agent rarely meets. The natural gradient measures each step by how much the behaviour actually changes, averaged over the situations the agent meets. It then picks the step that gains the most reward for a fixed amount of behaviour change. For a simple table of preferences, this step is: in every situation, prefer each action in proportion to how much better than average it is. That is a gentle version of "switch to the best action", and it never makes things worse.

## The problem

The setting is [reinforcement learning control](/rl-control/) in a [Markov decision process](/markov-decision-process/) with a differentiable stochastic policy $\pi_\theta$, $\theta \in \mathbb{R}^m$. The objective is $J(\theta) = \sum_s \mu(s) V^{\pi_\theta}(s)$, the discounted return from the start distribution $\mu$, or the average reward in Kakade's original setting. By the [policy gradient theorem](/policy-gradient-theorem/), $\nabla J = \sum_s d^\pi(s) \sum_a \nabla \pi_\theta(a \mid s) Q^\pi(s, a)$, where $d^\pi(s) = \sum_t \gamma^t \Pr(S_t = s)$ is the discounted visitation (the stationary distribution in the average reward setting). The task is to find the steepest ascent direction of $J$ when the length of a step is measured by the expected change of the action distribution, $\tfrac12 \delta\theta^\top F(\theta)\, \delta\theta$, which is the second-order term of the average KL divergence between $\pi_\theta$ and $\pi_{\theta + \delta\theta}$.

## The algorithm

The sampled version estimates $\nabla J$ and $F$ from the same episodes, with the same weights $\gamma^t$, so that both use the visitation $d^\pi$. Notation: $\psi_t = \nabla_\theta \log \pi_\theta(A_t \mid S_t)$ is the score, $G_t$ the return from step $t$, $b$ a baseline fitted on earlier episodes, $\epsilon$ a small damping constant and $\eta$ the step size.

```pseudo id=main
NATURAL-POLICY-GRADIENT(π_θ, γ, η, ε, N)
L1  for k ← 1 to K do
L2      run π_θ for N episodes
L3      Â_t ← G_t − b(S_t) for every step t of every episode
L4      ĝ ← (1/N) Σ_episodes Σ_t γ^t Â_t ψ_t
L5      F̂ ← (1/N) Σ_episodes Σ_t γ^t ψ_t ψ_tᵀ
L6      solve (F̂ + εI) x = ĝ
L7      θ ← θ + η x
```

Line L4 is the [REINFORCE](/reinforce/) estimate of $\nabla J$ with a baseline. Line L5 estimates $F$; it needs no rewards. Line L6 can use [conjugate gradients](/conjugate-gradient-method/) with products $F v$, without forming $F$, as in [TRPO](/trpo/). The damping $\epsilon$ keeps the system solvable when $F$ is singular, which happens for the tabular softmax because adding a constant to all preferences of a state does not change the policy; Kakade added such a small multiple of the identity in his experiments. A natural actor-critic replaces lines L3 to L6 by a regression: fit a linear critic $w^\top \psi(s, a)$ to the advantages, and use $x = w$ (Theorem 1 of Kakade, below).

**The tabular softmax case.** For $\pi_\theta(a \mid s) \propto e^{\theta_{s,a}}$, the Fisher matrix is block diagonal with block $d^\pi(s)(\mathrm{diag}(\pi_s) - \pi_s \pi_s^\top)$ for state $s$, and the gradient block is $d^\pi(s)(\mathrm{diag}(\pi_s) - \pi_s\pi_s^\top) A^\pi(s, \cdot)$. So the solutions of $F x = \nabla J$ are $x_{s,a} = A^\pi(s, a) + c_s$, and the exact NPG step is the multiplicative update

$$\pi_{k+1}(a \mid s) \propto \pi_k(a \mid s)\, e^{\eta A^{\pi_k}(s, a)}.$$

The visitation $d^\pi(s)$ cancels: a state that the policy rarely visits gets the same step as a frequent one. With the visitation normalized to sum to 1, as in Agarwal et al., the same step reads $\eta / (1 - \gamma)$ times the advantage.

## Example

Take the two-state MDP of the [policy gradient theorem](/policy-gradient-theorem/) page with $\gamma = \tfrac12$, start state 0 and the uniform tabular softmax policy. There $d^\pi = (\tfrac{32}{27}, \tfrac{8}{27})$, and the Fisher blocks are $d^\pi(s) \begin{pmatrix} 1/4 & -1/4 \\ -1/4 & 1/4 \end{pmatrix}$, that is $\pm\tfrac{8}{27}$ and $\pm\tfrac{2}{27}$. The plain gradient is $(\tfrac{184}{729}, -\tfrac{184}{729})$ in state 0 and $(-\tfrac{148}{729}, \tfrac{148}{729})$ in state 1. The natural gradient is the advantage plus a constant per state: $A^\pi(0, \cdot) = (\tfrac{23}{54}, -\tfrac{23}{54})$ and $A^\pi(1, \cdot) = (-\tfrac{37}{27}, \tfrac{37}{27})$. State 1 is visited four times less than state 0, so the plain gradient barely moves it, while the natural gradient gives it a step of $\tfrac{37}{27} \approx 1.37$.

Exact ascent with step size 1 from $\theta = 0$ ($V^*(0) = \tfrac{11}{6} \approx 1.8333$):

| iteration | 0 | 1 | 2 | 3 | 5 | 10 |
|---|---|---|---|---|---|---|
| natural gradient, $V(0)$ | 1.0370 | 1.5381 | 1.6716 | 1.7417 | 1.8079 | 1.8326 |
| natural gradient, $\pi(1 \mid 1)$ | 0.500 | 0.939 | 0.995 | 1.000 | 1.000 | 1.000 |
| plain gradient, $V(0)$ | 1.0370 | 1.2382 | 1.3958 | 1.5040 | 1.6233 | 1.7275 |
| plain gradient, $\pi(1 \mid 1)$ | 0.500 | 0.600 | 0.679 | 0.737 | 0.809 | 0.889 |

## Correctness

The correctness proof proves the first three facts; the fourth is the published theorem of Agarwal et al.

1. **Compatible function approximation (Kakade, Theorem 1).** Let $w^*$ minimize $\epsilon(w) = \sum_s d^\pi(s) \sum_a \pi(a \mid s) (w^\top \psi(s, a) - Q^\pi(s, a))^2$. Then $F w^* = \nabla J$, so $w^*$ is a natural gradient. The fitted critic $f(s, a) = w^{*\top} \psi(s, a)$ is the projection of the advantage onto the span of the scores.
2. **Tabular softmax.** The natural gradient is $A^\pi(s, a) + c_s$, and the exact step is $\pi'(a \mid s) \propto \pi(a \mid s) e^{\eta A^\pi(s, a)}$ in every state with $d^\pi(s) > 0$.
3. **Monotone improvement.** That step satisfies $\sum_a \pi'(a \mid s) A^\pi(s, a) \ge 0$ in every state, so $V^{\pi'} \ge V^\pi$ in every state by the [policy improvement theorem](/policy-improvement-theorem/), for every $\eta > 0$. As $\eta \to \infty$, $\pi'$ becomes greedy with respect to $A^\pi$ and the step becomes a [policy iteration](/policy-iteration/) step (Kakade's Theorem 2 states this for exponential family policies in general).
4. **Rate (Agarwal et al., 2021).** For the tabular softmax, rewards in $[0, 1]$, $\theta_0 = 0$ and the step $\theta \leftarrow \theta + \frac{\eta}{1-\gamma} A^{\pi_k}$, the iterates satisfy $V^*(\rho) - V^{\pi_T}(\rho) \le \frac{\log |A|}{\eta T} + \frac{1}{(1-\gamma)^2 T}$ for every start distribution $\rho$. The bound does not depend on the number of states or on how well $\mu$ covers them.

Invariance under a change of parameters, $\theta = B\xi$ with $B$ invertible, is the general property of the [natural gradient](/natural-gradient-descent/): the first-order change of $\log \pi$ is the same in both parameterizations.

## Complexity

With $N$ episodes of length at most $T$ and $m$ parameters, line L4 costs $O(N T (A m))$ for the scores of a linear softmax, line L5 costs $O(N T m^2)$, and line L6 costs $O(m^3)$ by elimination. So $K$ iterations cost $O(K(N T (A m + m^2) + m^3))$ in the worst case, and the matrix takes $O(m^2)$ memory. With conjugate gradients and Fisher-vector products, as in [TRPO](/trpo/), the cost of line L6 drops to a few passes over the batch per CG iteration and the memory to $O(m)$, which is what makes the method usable for networks. The exact tabular version with a known model needs one linear solve of size $|S|$ for $V^\pi$, $O(|S|^3)$, per iteration.

## Properties

- **Parameterization invariant** (to first order), unlike the plain gradient.
- **Visitation independent** for the tabular softmax: rarely visited states still get full steps.
- **Policy improvement in the tabular case** for any step size, with exact advantages.
- **On-policy and sample-based.** The sampled version needs fresh episodes per iteration.
- **Randomized.** Episodes are sampled.

## Variants and improvements

- **Natural actor-critic.** Estimate the natural gradient as the weights of a compatible linear critic (Peters and Schaal, 2008; Bhatnagar et al., 2009).
- **TRPO.** Choose the step length so that the average KL divergence stays below a bound, solve with conjugate gradients and check the step with a line search ([TRPO](/trpo/)).
- **ACKTR and K-FAC.** Approximate $F$ by Kronecker factors per layer.
- **PPO.** Replace the second-order constraint by a clipped first-order objective ([PPO](/ppo/)).
- **Policy mirror descent.** The multiplicative update is [mirror descent](/mirror-descent/) with the KL divergence in each state; with entropy regularization it converges linearly ([maximum entropy RL](/maximum-entropy-rl/)).

## When to use it

Use the natural gradient when plain policy gradients are slow because the parameterization is badly scaled, for example when some states are rarely visited or when the policy is close to deterministic in some states. For small parameter counts, form and solve $F$ directly; for networks, use the conjugate gradient form inside [TRPO](/trpo/), or use [PPO](/ppo/), which is simpler and usually as good. With a known tabular model, the multiplicative update is a smooth alternative to [policy iteration](/policy-iteration/) with a convergence rate that does not depend on the number of states.

## Pitfalls

- **Inconsistent weights.** $\hat g$ and $\hat F$ must use the same state weighting; using $\gamma^t$ in one and not in the other gives a direction that is neither natural nor plain.
- **Singular Fisher matrix.** Tabular softmax and overparameterized networks give singular $F$; add damping or use the pseudo-inverse.
- **Noisy Fisher estimates.** A sampled $\hat F$ with few episodes can be badly conditioned, and its inverse amplifies noise; use more samples, damping, or CG with few iterations.
- **Step size.** The natural gradient has the scale of the advantages, so a fixed $\eta$ can make huge policy changes when advantages are large; TRPO normalizes the step by its KL divergence.
- **Average reward and discount.** Kakade's paper uses the stationary distribution of the average reward setting; with discounting, use the discounted visitation.

## Implementations

## History

Amari (1998) introduced the natural gradient for statistical learning. Kakade (2001) carried it to policies: he defined the Fisher matrix averaged over the stationary state distribution, proved that the natural gradient equals the weights of the compatible critic of Sutton et al. and Konda and Tsitsiklis, showed that for exponential family policies a long natural step chooses the greedy action, and tested it on a linear quadratic regulator and Tetris, where it learned much faster than the plain gradient. Bagnell and Schneider (2003) derived a related metric from trajectory distributions. Peters and Schaal turned the idea into the natural actor-critic, and Schulman et al. (2015) built [TRPO](/trpo/) on it. Agarwal, Kakade, Lee and Mahajan (2019 preprint, JMLR 2021) proved global convergence rates for the tabular case.

## References
