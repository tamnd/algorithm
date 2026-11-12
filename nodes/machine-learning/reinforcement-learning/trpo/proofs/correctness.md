---
title: The surrogate matches the return to first order and bounds it from below
proves: [correctness]
status: full
---

Notation is that of the page. The MDP has discount $\gamma < 1$ and bounded rewards; an episode that ends moves to an absorbing state with reward 0 and value 0. For a policy $\pi$, $V^\pi$, $Q^\pi$ and $A^\pi = Q^\pi - V^\pi$ are its value functions, $\eta(\pi) = \mathbb{E}[V^\pi(S_0)]$, and $\rho_\pi(s) = \sum_t \gamma^t \Pr_\pi(S_t = s)$. For two policies, write $\bar A(s) = \sum_a \tilde\pi(a \mid s) A^\pi(s, a)$; note $\sum_a \pi(a \mid s) A^\pi(s, a) = 0$.

**Lemma 1 (Kakade and Langford).** $\eta(\tilde\pi) = \eta(\pi) + \mathbb{E}_{\tilde\pi}\left[\sum_t \gamma^t A^\pi(S_t, A_t)\right] = \eta(\pi) + \sum_t \gamma^t \mathbb{E}_{S_t \sim \tilde\pi}[\bar A(S_t)]$, where the trajectory is drawn from $\tilde\pi$.

*Proof.* $A^\pi(s, a) = \mathbb{E}[R_{t+1} + \gamma V^\pi(S_{t+1}) - V^\pi(S_t) \mid S_t = s, A_t = a]$ for any policy that chose $a$ in $s$, because the expectation depends only on $(s, a)$ and the transition law. Hence $\mathbb{E}_{\tilde\pi}[\sum_{t<H} \gamma^t A^\pi(S_t, A_t)] = \mathbb{E}_{\tilde\pi}[\sum_{t<H} \gamma^t R_{t+1}] + \mathbb{E}_{\tilde\pi}[\gamma^H V^\pi(S_H)] - \mathbb{E}[V^\pi(S_0)]$ by telescoping. As $H \to \infty$, the middle term goes to 0 because $V^\pi$ is bounded, the first goes to $\eta(\tilde\pi)$, and the last is $\eta(\pi)$ because $S_0$ has the same law under both policies. Conditioning on $S_t$ turns $A^\pi(S_t, A_t)$ into $\bar A(S_t)$. $\square$

By the same conditioning, $L_\pi(\tilde\pi) = \eta(\pi) + \sum_t \gamma^t \mathbb{E}_{S_t \sim \pi}[\bar A(S_t)]$: the local approximation uses the state law of $\pi$ in place of that of $\tilde\pi$.

**Claim 1 (first-order match).** $L_{\pi_{\text{old}}}(\pi_{\text{old}}) = \eta(\pi_{\text{old}})$, and $\nabla_\theta L_{\pi_{\text{old}}}(\pi_\theta) = \nabla_\theta \eta(\pi_\theta)$ at $\theta = \theta_{\text{old}}$. The sample gradient of line L4 with exact advantages has expectation $\nabla_\theta \eta$.

*Proof.* For $\tilde\pi = \pi_{\text{old}}$, $\bar A = 0$, so $L = \eta$. Next, $\nabla_\theta L_{\pi_{\text{old}}}(\pi_\theta) = \sum_s \rho_{\text{old}}(s) \sum_a \nabla_\theta \pi_\theta(a \mid s) A^{\text{old}}(s, a)$. At $\theta_{\text{old}}$, since $\sum_a \nabla_\theta \pi_\theta(a \mid s) = 0$, this equals $\sum_s \rho_{\text{old}}(s) \sum_a \nabla_\theta \pi_\theta(a \mid s) Q^{\text{old}}(s, a)$, which is $\nabla_\theta \eta$ by the policy gradient theorem. For line L4, $\mathbb{E}[\sum_t \gamma^t A^{\text{old}}(S_t, A_t) \nabla \log \pi(A_t \mid S_t)] = \sum_t \gamma^t \sum_s \Pr(S_t = s) \sum_a \pi(a \mid s) \nabla \log \pi(a \mid s) A^{\text{old}}(s, a)$, and $\pi \nabla \log \pi = \nabla \pi$; summing over $t$ gives the formula above. The weight $1/N$ averages $N$ independent episodes. $\square$

**Lemma 2 (coupling).** Let $\alpha = \max_s D_{\mathrm{TV}}(\pi(\cdot \mid s), \tilde\pi(\cdot \mid s))$ and $\epsilon = \max_{s,a} |A^\pi(s, a)|$. Then $|\bar A(s)| \le 2\alpha\epsilon$ for every $s$, and $|\mathbb{E}_{S_t \sim \tilde\pi}[\bar A(S_t)] - \mathbb{E}_{S_t \sim \pi}[\bar A(S_t)]| \le 4\alpha\epsilon(1 - (1 - \alpha)^t)$.

*Proof.* For each $s$ there is a coupling $(a, \tilde a)$ with marginals $\pi(\cdot \mid s)$ and $\tilde\pi(\cdot \mid s)$ and $\Pr(a \ne \tilde a) = D_{\mathrm{TV}} \le \alpha$ (the maximal coupling). Then $\bar A(s) = \mathbb{E}[A^\pi(s, \tilde a)] - \mathbb{E}[A^\pi(s, a)] = \mathbb{E}[(A^\pi(s, \tilde a) - A^\pi(s, a)) [a \ne \tilde a]]$, so $|\bar A(s)| \le 2\epsilon\alpha$. Now run two trajectories together from the same start state: while they are in the same state, draw the two actions from the maximal coupling, and if the actions agree, draw one common next state; after the first disagreement, continue them independently. Each trajectory has the correct law. Let $E_t$ be the event that they agreed at all steps before $t$; then $\Pr(E_t) \ge (1 - \alpha)^t$ by induction, and on $E_t$ the two states at time $t$ are equal. So the difference of expectations is $\mathbb{E}[(\bar A(\tilde S_t) - \bar A(S_t)) [\text{not } E_t]]$, at most $2 \cdot 2\alpha\epsilon \cdot (1 - (1 - \alpha)^t)$ in absolute value. $\square$

**Claim 2 (Theorem 1 of the paper).** $\eta(\tilde\pi) \ge L_\pi(\tilde\pi) - \frac{4\epsilon\gamma}{(1-\gamma)^2}\alpha^2$, and the same bound holds with $\alpha^2$ replaced by $D^{\max}_{\mathrm{KL}}(\pi, \tilde\pi) = \max_s D_{\mathrm{KL}}(\pi(\cdot \mid s) \,\|\, \tilde\pi(\cdot \mid s))$.

*Proof.* By Lemma 1 and the remark after it, $|\eta(\tilde\pi) - L_\pi(\tilde\pi)| \le \sum_t \gamma^t \cdot 4\alpha\epsilon(1 - (1-\alpha)^t) = 4\alpha\epsilon\left(\frac{1}{1-\gamma} - \frac{1}{1 - \gamma(1-\alpha)}\right) = \frac{4\alpha^2\epsilon\gamma}{(1-\gamma)(1-\gamma+\gamma\alpha)} \le \frac{4\epsilon\gamma}{(1-\gamma)^2}\alpha^2$. For the KL form, Pinsker's inequality gives $D_{\mathrm{TV}}^2 \le \tfrac12 D_{\mathrm{KL}} \le D_{\mathrm{KL}}$ in every state, so $\alpha^2 \le D^{\max}_{\mathrm{KL}}$. $\square$

**Claim 3 (minorize-maximize).** Let $C = 4\epsilon\gamma/(1-\gamma)^2$ and $M_i(\pi) = L_{\pi_i}(\pi) - C D^{\max}_{\mathrm{KL}}(\pi_i, \pi)$. If $\pi_{i+1}$ maximizes $M_i$, then $\eta(\pi_{i+1}) \ge \eta(\pi_i)$.

*Proof.* By Claim 2, $\eta(\pi_{i+1}) \ge M_i(\pi_{i+1})$. By Claim 1 and $D_{\mathrm{KL}}(\pi_i, \pi_i) = 0$, $M_i(\pi_i) = \eta(\pi_i)$. Since $\pi_{i+1}$ maximizes $M_i$, $M_i(\pi_{i+1}) \ge M_i(\pi_i)$. $\square$

**Claim 4 (the step of lines L5 to L9).** In exact arithmetic, $k$ iterations of conjugate gradients solve $(\hat F + \epsilon I) x = g$ for a positive definite system of size $k$. The quadratic model $\tfrac12 (\beta x)^\top \hat F (\beta x)$ of the mean KL divergence then equals $\delta$. The parameters returned by lines L7 to L9 either equal $\theta_{\text{old}}$ or satisfy $\bar D_{\mathrm{KL}}(\theta_{\text{old}}, \theta) \le \delta$ and $L(\theta) > L(\theta_{\text{old}})$ on the batch.

*Proof.* The first sentence is the finite termination of conjugate gradients for symmetric positive definite matrices (Nocedal and Wright, Chapter 5). The second follows from $\beta^2 = 2\delta / x^\top \hat F x$. The third holds because line L9 runs only when the test of line L8 passes. $\hat F$ is the Hessian of the mean KL divergence at $\theta_{\text{old}}$: for each state, the Hessian of $D_{\mathrm{KL}}(\pi_{\text{old}} \,\|\, \pi_\theta)$ at $\theta_{\text{old}}$ is $-\sum_a \pi \nabla^2 \log \pi = \sum_a \pi \,\nabla \log \pi \,\nabla \log \pi^\top - \sum_a \nabla^2 \pi$, and $\sum_a \nabla^2 \pi = \nabla^2 1 = 0$. $\square$

Claims 1 to 3 justify maximizing the surrogate near the old policy, and Claim 4 shows what the practical step guarantees: it is a natural gradient step of KL size $\delta$ in the quadratic model, and the line search enforces the real constraint and a sampled improvement. $\blacksquare$
