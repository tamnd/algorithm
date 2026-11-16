---
title: PBVS makes the pose error decay exponentially and stops at the estimated goal
proves: [correctness]
status: full
---

Write $E = T_{c^*t}T_{ct}^{-1}$ for the pose of the current camera frame in the desired camera frame, with rotation $R$ and translation $t$, and $\theta u = \log R$ with $\theta \in [0, \pi]$. The camera moves with the body twist $V = (\omega, v)$ in the camera frame, and the target is fixed.

**Lemma 1 (error kinematics).** $\dot E = E[V]$, that is, $\dot R = R[\omega]$ and $\dot t = Rv$.

*Proof.* $T_{ct}^{-1} = T_{tc} = T_{tw}T_{wc}$, where $T_{tw}$ is constant because the target is fixed. So $E = T_{c^*t}T_{tw}T_{wc}$ is a constant pose times $T_{wc}$, and $\dot T_{wc} = T_{wc}[V]$ for a body twist. Hence $\dot E = E[V]$. Writing out the blocks of $E[V]$ gives the two formulas. $\square$

**Theorem 1 (exponential decay with an exact estimate).** Let the estimate be exact and let $\theta(0) < \pi$. Under $v = -\lambda R^T t$ and $\omega = -\lambda\theta u$, the solution is $t(\tau) = e^{-\lambda\tau}t(0)$, $u(\tau) = u(0)$ and $\theta(\tau) = e^{-\lambda\tau}\theta(0)$ for all $\tau \ge 0$. In particular the camera center moves on the straight segment from $t(0)$ to the goal.

*Proof.* By Lemma 1, $\dot t = Rv = -\lambda RR^T t = -\lambda t$, which gives the formula for $t$. For the rotation, let $\phi(\tau) = e^{-\lambda\tau}\theta(0)$ and $\tilde R(\tau) = \exp(\phi(\tau)[u(0)])$. Since $\phi(\tau) \in [0, \pi)$, $\log\tilde R = \phi u(0)$. Because $\tilde R$ commutes with $[u(0)]$, $\dot{\tilde R} = \dot\phi\,\tilde R[u(0)] = \tilde R[-\lambda\phi u(0)] = \tilde R[-\lambda\log\tilde R]$. So $\tilde R$ solves $\dot R = R[-\lambda\log R]$ with the same initial value as $R$. The right side is a smooth function of $R$ on the set $\theta < \pi$, which $\tilde R$ never leaves, so the solution is unique there and $R = \tilde R$. $\square$

If $\theta(0) = \pi$, the logarithm chooses one of the two axes, and after the first instant $\theta < \pi$ and the theorem applies. So with an exact estimate the goal is reached from every start, with no local minima, as long as the pose can be estimated along the way.

**Proposition 2 (sampled rotation).** If the twist is held constant for each sample time $h$ with $\lambda h < 1$, then $\theta_k = (1 - \lambda h)^k\theta_0$ and $u_k = u_0$ exactly, for $\theta_0 < \pi$.

*Proof.* With $\omega$ constant on the step, $R_{k+1} = R_k\exp(-\lambda h\theta_k[u_k])$. If $R_k = \exp(\theta_k[u_0])$, the two exponentials have the same axis and add: $R_{k+1} = \exp((1 - \lambda h)\theta_k[u_0])$, and $(1 - \lambda h)\theta_k \in [0, \pi)$, so the logarithm returns this angle and axis. Induction on $k$ gives the claim. $\square$

The translation of the sampled loop is not exactly geometric, because $v$ is held in the rotating camera frame during the step; its distance from the straight segment is $O(h)$.

**Theorem 3 (biased estimate).** Let the estimator return $T_{ct}B$ for a fixed pose $B$ instead of $T_{ct}$, and let the estimated rotation error start below $\pi$. Then the true pose of the target in the camera frame tends to $T_{c^*t}B^{-1}$, and the true error pose tends to $T_{c^*t}BT_{c^*t}^{-1}$, which is the identity only if $B = I$.

*Proof.* The law uses $\hat E = T_{c^*t}(T_{ct}B)^{-1} = T_{c^*t}B^{-1}T_{tw}T_{wc}$. This is again a constant pose times $T_{wc}$, so Lemma 1 holds for $\hat E$, and the law is the law of Theorem 1 written for $\hat E$. So $\hat E \to I$ exponentially, which means $T_{ct}B \to T_{c^*t}$, that is $T_{ct} \to T_{c^*t}B^{-1}$. The true error is $E = T_{c^*t}T_{ct}^{-1} \to T_{c^*t}BT_{c^*t}^{-1}$. $\blacksquare$

The theorems say nothing about the image: the target can leave the field of view on the way, and then the pose estimate, which the proofs assume, is lost.
