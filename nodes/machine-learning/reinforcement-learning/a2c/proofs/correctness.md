---
title: The n-step advantage of A2C and the mean direction of its update
proves: [correctness]
status: full
---

Notation is that of the page. Fix $\theta$ and $w$ during one round, and write $\pi = \pi_\theta$, $V = V^\pi$, $Q = Q^\pi$, $e = V_w - V$, with all values 0 at the end of an episode. Rewards satisfy $\mathbb{E}[R_{t+1} \mid S_t = s, A_t = a] = r(s, a)$ and $Q(s, a) = r(s, a) + \gamma \sum_{s'} P(s' \mid s, a) V(s')$. Fix one copy and drop the index $i$. For a position $t$ in the segment, let $m = n - t$ be the number of steps to the end of the segment, and let $E_t$ be the event that the episode does not end in steps $t, \ldots, n - 1$.

**Claim 1 (the n-step target).** $\mathbb{E}[\hat G_t \mid S_t = s, A_t = a] = Q(s, a) + \gamma^m \mathbb{E}[\mathbf{1}_{E_t}\, e(S_n) \mid S_t = s, A_t = a]$. In particular, if $V_w = V$ then $\mathbb{E}[\hat G_t \mid S_t, A_t] = Q(S_t, A_t)$ and $\mathbb{E}[\hat A_t \mid S_t, A_t] = A^\pi(S_t, A_t)$.

*Proof.* By induction on $m$. Lines L5 and L6 give $\hat G_{n} = V_w(S_n)$ and $\hat G_t = R_{t+1} + \gamma (1 - D_{t+1}) \hat G_{t+1}$.

Base $m = 1$: $\hat G_{n-1} = R_n + \gamma(1 - D_n) V_w(S_n)$. Given $(S_{n-1}, A_{n-1}) = (s, a)$, the episode continues to $s'$ with probability $P(s' \mid s, a)$, so $\mathbb{E}[\hat G_{n-1} \mid s, a] = r(s, a) + \gamma \sum_{s'} P(s' \mid s, a) (V(s') + e(s')) = Q(s, a) + \gamma \mathbb{E}[\mathbf{1}_{E_{n-1}} e(S_n) \mid s, a]$.

Step: suppose the claim holds for $t + 1$ (that is, for $m - 1$). Given $(S_t, A_t) = (s, a)$ and that the episode continues to $S_{t+1} = s'$, the next action has the law $\pi(\cdot \mid s')$ because the whole segment uses the same $\theta$ (line L3). So, by the Markov property and the hypothesis,

$$\mathbb{E}[\hat G_{t+1} \mid S_{t+1} = s'] = \sum_{a'} \pi(a' \mid s') Q(s', a') + \gamma^{m-1} \mathbb{E}[\mathbf{1}_{E_{t+1}} e(S_n) \mid S_{t+1} = s'] = V(s') + \gamma^{m-1} \mathbb{E}[\mathbf{1}_{E_{t+1}} e(S_n) \mid S_{t+1} = s'].$$

Hence

$$\mathbb{E}[\hat G_t \mid s, a] = r(s, a) + \gamma \sum_{s'} P(s' \mid s, a) \Big(V(s') + \gamma^{m-1} \mathbb{E}[\mathbf{1}_{E_{t+1}} e(S_n) \mid S_{t+1} = s']\Big) = Q(s, a) + \gamma^m \mathbb{E}[\mathbf{1}_{E_t} e(S_n) \mid s, a],$$

since $E_t$ is the event that the episode continues at step $t$ and then $E_{t+1}$ holds. When $e = 0$ the second term is zero. $V_w(S_t)$ is fixed given $S_t$, so $\mathbb{E}[\hat A_t \mid S_t, A_t] = Q(S_t, A_t) - V(S_t) = A^\pi(S_t, A_t)$. $\square$

Since $|\mathbb{E}[\mathbf{1}_{E_t} e(S_n) \mid s, a]| \le \max_{s'} |e(s')|$, the bias is at most $\gamma^m \max |e|$.

**Claim 2 (the mean direction).** Let $\beta = 0$ and $V_w = V$. Let $\rho$ be the distribution of a state drawn uniformly from the $N n$ states of the batch. Then $\mathbb{E}[g_\theta] = \sum_s \rho(s) \sum_a \nabla_\theta \pi(a \mid s) A^\pi(s, a)$, and this equals $\sum_s \rho(s) \sum_a \nabla_\theta \pi(a \mid s) Q^\pi(s, a)$.

*Proof.* $g_\theta$ is the average of $Nn$ terms $\hat A^i_t \nabla_\theta \log \pi(A^i_t \mid S^i_t)$. Condition each term on $(S^i_t, A^i_t)$. Given $S^i_t = s$, $A^i_t$ has the law $\pi(\cdot \mid s)$, and by Claim 1 the conditional mean of $\hat A^i_t$ given $(s, a)$ is $A^\pi(s, a)$. So the mean of one term given $S^i_t = s$ is $\sum_a \pi(a \mid s) A^\pi(s, a) \nabla \log \pi(a \mid s) = \sum_a \nabla \pi(a \mid s) A^\pi(s, a)$. Averaging over the terms gives the weight $\rho(s)$. Finally $\sum_a \nabla \pi(a \mid s) V(s) = V(s) \nabla \sum_a \pi(a \mid s) = 0$, so $A^\pi$ may be replaced by $Q^\pi$. $\square$

By the [policy gradient theorem](/policy-gradient-theorem/), $\nabla J = \sum_s d(s) \sum_a \nabla \pi(a \mid s) Q^\pi(s, a)$ with the discounted visitation $d$. So the mean A2C direction is the gradient exactly when $\rho$ is proportional to $d$, for example for $\gamma = 1$ with copies sampled from their episode starts, and it is a reweighted version otherwise.

**Claim 3 (one step on the batch surrogate).** Let $L(\theta', w') = \frac{1}{Nn} \sum_{i,t} \big[\hat A^i_t \log \pi_{\theta'}(A^i_t \mid S^i_t) + \beta H(\pi_{\theta'}(\cdot \mid S^i_t)) - \frac{c}{2} (\hat G^i_t - V_{w'}(S^i_t))^2\big]$ with $\hat A$ and $\hat G$ held fixed. Then line L10 is $(\theta, w) \leftarrow (\theta, w) + \eta \nabla L(\theta, w)$, with the critic part taken as a semi-gradient through $V_{w'}(S^i_t)$ only.

*Proof.* The gradient of $\hat A \log \pi_{\theta'}$ in $\theta'$ is $\hat A \nabla \log \pi_{\theta'}$, the gradient of the entropy term is $\beta \nabla H$, and the gradient of $-\frac{c}{2}(\hat G - V_{w'})^2$ in $w'$ with $\hat G$ fixed is $c (\hat G - V_{w'}) \nabla V_{w'}$. Averaging and evaluating at $(\theta, w)$ gives $g_\theta$ of line L8 and $c\, g_w$ of line L9, and line L10 adds $\eta$ times them. All terms use the same $(\theta, w)$, because lines L3 and L4 sample with it and nothing changes before line L10. $\blacksquare$
