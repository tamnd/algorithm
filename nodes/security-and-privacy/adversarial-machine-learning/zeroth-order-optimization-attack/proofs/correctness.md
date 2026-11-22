---
title: The ZOO attack estimates the right derivatives, counts its queries and returns only valid adversarial inputs
proves: [correctness]
status: full
---

Let the model return probabilities $p(u) = \operatorname{softmax}(z(u))$ for an input $u$, let $x \in [0,1]^d$ have label $y$, and let $\ell(u) = \max(\ln p_y(u) - \max_{i \ne y} \ln p_i(u), -\kappa)$ be the loss of `log_margin`. The objective of line L4 is $F(u) = \lVert u - x \rVert_2^2 + c\, \ell(u)$.

**Lemma 1 (the log margin is the logit margin).** If no probability is below the floor $10^{-300}$, then $\ell(u) = \max(z_y(u) - \max_{i \ne y} z_i(u), -\kappa)$.

*Proof.* With $s = \ln \sum_k e^{z_k}$, every $\ln p_i = z_i - s$. The common term $s$ cancels in $\ln p_y - \ln p_i$, and the maximum over $i \ne y$ of $z_i - s$ is $\max_{i\ne y} z_i - s$. $\square$

So the attack minimizes the same loss as the C&W attack, but it sees only the scores, never the logits or the gradients. The label from the scores is the label from the logits, because softmax keeps the order of the entries.

**Lemma 2 (the symmetric difference).** Let $e_i$ be the unit vector of coordinate $i$, and let $\phi(s) = F(u + s e_i)$ be three times differentiable on $[-h, h]$ with $|\phi'''| \le M$ there. Then the estimate $g = (\phi(h) - \phi(-h)) / (2h)$ of `coordinate_estimate` satisfies $|g - \partial_i F(u)| \le M h^2 / 6$.

*Proof.* By Taylor's theorem with the Lagrange remainder, $\phi(\pm h) = \phi(0) \pm h \phi'(0) + \tfrac12 h^2 \phi''(0) \pm \tfrac16 h^3 \phi'''(\xi_\pm)$ for some $\xi_\pm$ in $[-h, h]$. Subtracting, $\phi(h) - \phi(-h) = 2h\phi'(0) + \tfrac16 h^3 (\phi'''(\xi_+) + \phi'''(\xi_-))$. Divide by $2h$; the error is at most $\tfrac1{12} h^2 \cdot 2M$. $\square$

The function $F$ has kinks where the maximum of $\ell$ changes its active term, so Lemma 2 does not hold at points within $h$ of a kink. There the estimate is a mean of two one-sided slopes. Floating point adds an error of about $\varepsilon_{\text{mach}} |F| / h$, which is why $h$ is not taken much smaller than $10^{-4}$.

**Theorem 1 (the output).** For $T$ steps, the attack makes exactly $3T$ queries. Every iterate lies in $[0,1]^d$. If it returns a point $u^\star$ (not `None`), then $u^\star \in [0,1]^d$, the label of $u^\star$ is not $y$, and $u^\star$ is the closest to $x$ of all the iterates whose label is not $y$. Hence $\lVert u^\star - x \rVert_2 \ge d^\star(x) = \inf\{\lVert v - x \rVert_2 : v \in [0,1]^d \text{ with a label other than } y\}$, the true minimum adversarial distance in the box.

*Proof.* Each step makes two queries in line L4 and one in line L7, and adds $3$ to the count. Line L1 starts at $x \in [0,1]^d$, and line L6 changes one coordinate and clips it to $[0,1]$, so every iterate stays in the box. After line L6, line L7 queries the new iterate and records it only when its label is not $y$ and its distance is strictly smaller than the best so far. Only such points are ever stored and returned in line L8. A stored point is in the set over which $d^\star(x)$ is the infimum. $\blacksquare$

**What is not claimed.** The attack uses a fixed $c$ and one random coordinate a step. It has no proof of convergence to a minimum of $F$, and a run can end with `None` even when an adversarial input is near. In the seeded tests on binary linear models, 300 steps gave a distance at most about $1.62$ times the closed-form minimum (a measurement, not a theorem).
