---
title: The REINFORCE update is an unbiased estimate of the policy gradient
proves: [correctness]
status: full
---

Notation is that of the page. An episode is $\tau = (S_0, A_0, R_1, S_1, \ldots, S_{T-1}, A_{T-1}, R_T)$, the score is $\psi_t = \nabla_\theta \log \pi_\theta(A_t \mid S_t)$, and $g = \sum_{t=0}^{T-1} \gamma^t (G_t - b(S_t)) \psi_t$ is the vector of lines L3 to L7. We assume that $S$ and $A$ are finite, that $\pi_\theta(a \mid s) > 0$ for all $s, a$, that $\pi_\theta(a \mid s)$ is differentiable in $\theta$, and that the reward $R_{t+1}$ has a distribution that depends only on $(S_t, A_t)$, with $|R_{t+1}| \le R_{\max}$. The baseline $b$ is a fixed function of the state during the episode. Let $\mathcal{H}_t$ be the history up to and including $S_t$, together with the event $\{T > t\}$ that the episode is still running at step $t$.

**Lemma 1 (the score has mean zero).** On the event $\{T > t\}$, $\mathbb{E}[\psi_t \mid \mathcal{H}_t] = 0$.

*Proof.* Given $\mathcal{H}_t$, the action $A_t$ has the distribution $\pi_\theta(\cdot \mid S_t)$, so

$$\mathbb{E}[\psi_t \mid \mathcal{H}_t] = \sum_a \pi_\theta(a \mid S_t) \frac{\nabla_\theta \pi_\theta(a \mid S_t)}{\pi_\theta(a \mid S_t)} = \nabla_\theta \sum_a \pi_\theta(a \mid S_t) = \nabla_\theta 1 = 0. \qquad \square$$

**Theorem 1 (finite horizon).** Cut every episode at the horizon $H$, so $T \le H$, and let $J_H(\theta) = \mathbb{E}\big[\sum_{t=0}^{T-1} \gamma^t R_{t+1}\big]$. Then $\mathbb{E}[g] = \nabla J_H(\theta)$ for every baseline $b$.

*Proof.* Step 1 (likelihood ratio). Condition on the rewards being replaced by their means: since the reward distribution does not depend on $\theta$, we may first average over rewards and work with the finite set of state and action sequences $\sigma = (S_0, A_0, \ldots, S_{T-1}, A_{T-1})$. The probability of $\sigma$ is

$$p_\theta(\sigma) = \mu(S_0) \prod_{t=0}^{T-1} \pi_\theta(A_t \mid S_t) \prod_{t=0}^{T-2} P(S_{t+1} \mid S_t, A_t) \cdot e(\sigma),$$

where $e(\sigma)$ is the probability that the episode ends after $A_{T-1}$ (1 if $T = H$). Only the factors $\pi_\theta$ depend on $\theta$. Let $\bar R(\sigma) = \sum_t \gamma^t r(S_t, A_t)$ with $r(s, a) = \mathbb{E}[R_{t+1} \mid S_t = s, A_t = a]$. The sum $J_H = \sum_\sigma p_\theta(\sigma) \bar R(\sigma)$ is finite, so we may differentiate term by term. If $p_\theta(\sigma) > 0$ then $\nabla p_\theta(\sigma) = p_\theta(\sigma) \sum_t \psi_t$. If $p_\theta(\sigma) = 0$, a factor that does not depend on $\theta$ is zero, so $\nabla p_\theta(\sigma) = 0$. Hence

$$\nabla J_H = \mathbb{E}\Big[\Big(\sum_{k=0}^{T-1} \gamma^k R_{k+1}\Big) \Big(\sum_{t=0}^{T-1} \psi_t\Big)\Big],$$

where we put back the sampled rewards, whose conditional mean given $\sigma$ is $r(S_k, A_k)$ and does not change the expectation.

Step 2 (causality). Write the product as $\sum_{t} \sum_{k} \gamma^k R_{k+1} \psi_t \mathbf{1}[T > t]\mathbf{1}[T > k]$. Take a pair with $k < t$. The factor $\gamma^k R_{k+1} \mathbf{1}[T > k] \mathbf{1}[T > t]$ is determined by $\mathcal{H}_t$, so by Lemma 1

$$\mathbb{E}\big[\gamma^k R_{k+1} \mathbf{1}[T > k] \mathbf{1}[T > t] \psi_t\big] = \mathbb{E}\big[\gamma^k R_{k+1} \mathbf{1}[T > k] \mathbf{1}[T > t]\, \mathbb{E}[\psi_t \mid \mathcal{H}_t]\big] = 0.$$

The terms with $k \ge t$ give $\sum_{k \ge t} \gamma^k R_{k+1} = \gamma^t G_t$. Hence $\nabla J_H = \mathbb{E}\big[\sum_{t=0}^{T-1} \gamma^t G_t \psi_t\big]$.

Step 3 (baseline). For each $t$, $\gamma^t b(S_t) \mathbf{1}[T > t]$ is determined by $\mathcal{H}_t$, so the same argument gives $\mathbb{E}[\gamma^t b(S_t) \mathbf{1}[T > t] \psi_t] = 0$. Subtracting these terms gives $\mathbb{E}[g] = \nabla J_H$. All the expectations are finite sums, so every step is exact. $\square$

**Theorem 2 (no cut).** Let $\gamma < 1$, $\lVert \psi_t \rVert \le \Psi$ and $|b| \le B$. Then $J$ is differentiable and $\mathbb{E}[g] = \nabla J(\theta)$.

*Proof.* Run the episode without a cut, and let $g_H$ be the vector that lines L3 to L7 compute from its first $H$ steps (the episode cut at $H$). Since the first $H$ steps have the law of the cut episode, Theorem 1 gives $\mathbb{E}[g_H] = \nabla J_H$. The returns satisfy $|G_t| \le R_{\max} / (1 - \gamma)$, and the returns of the cut episode differ from those of the full episode by at most $\gamma^{H - t} R_{\max} / (1 - \gamma)$. So

$$\lVert g - g_H \rVert \le \sum_{t < H} \gamma^t \gamma^{H-t} \frac{R_{\max}}{1-\gamma} \Psi + \sum_{t \ge H} \gamma^t \Big(\frac{R_{\max}}{1-\gamma} + B\Big) \Psi \le \gamma^H \Psi \Big(\frac{H R_{\max}}{1-\gamma} + \frac{R_{\max}/(1-\gamma) + B}{1-\gamma}\Big) =: \epsilon_H.$$

The bound $\epsilon_H$ does not depend on $\theta$ and tends to 0. Hence $\lVert \nabla J_H - \mathbb{E}[g] \rVert \le \epsilon_H$ for all $\theta$, and also $|J - J_H| \le \gamma^H R_{\max}/(1-\gamma)$. So $J_H \to J$ and $\nabla J_H \to \mathbb{E}[g]$ uniformly in $\theta$. A uniform limit of gradients of functions that converge pointwise is the gradient of the limit: for any $\theta$ and direction $u$, $J_H(\theta + u) - J_H(\theta) = \int_0^1 \nabla J_H(\theta + s u) \cdot u \, ds$, and both sides converge, so $J(\theta + u) - J(\theta) = \int_0^1 m(\theta + s u) \cdot u \, ds$ with $m = \mathbb{E}[g]$ as a function of $\theta$. The function $m$ is continuous as a uniform limit of continuous functions, so $J$ is differentiable with $\nabla J = m$. $\square$

**Corollary (the learned baseline).** Line L9 changes $b$ only after line L8. So during the episode that produces $g$, $b$ is a fixed function determined by earlier episodes, which are independent of the current one given $\theta$. Conditioning on the earlier episodes and applying Theorem 1 or Theorem 2 gives $\mathbb{E}[g \mid \text{past}] = \nabla J(\theta)$. $\blacksquare$
