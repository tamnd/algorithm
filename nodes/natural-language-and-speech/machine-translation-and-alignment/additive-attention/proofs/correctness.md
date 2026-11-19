---
title: Additive attention returns a convex combination of the encoder states, and its gradients are as stated
proves: [correctness]
status: full
---

Fix the decoder state $s \in \mathbb{R}^{d_s}$, the encoder states $h_1, \ldots, h_J \in \mathbb{R}^{d_h}$ with $J \ge 1$, the parameters $W \in \mathbb{R}^{a \times d_s}$, $U \in \mathbb{R}^{a \times d_h}$ and $v \in \mathbb{R}^a$, and a mask $M \subseteq \{1, \ldots, J\}$ of the kept positions, not empty. The definition of Bahdanau et al. (2015) is

$$e_j = v^\top \tanh(W s + U h_j), \qquad \alpha_j = \frac{\exp(e_j)}{\sum_{k \in M} \exp(e_k)} \ (j \in M), \qquad \alpha_j = 0 \ (j \notin M), \qquad c = \sum_j \alpha_j h_j.$$

**Lemma 1 (the stable softmax).** For any real $m$, $\exp(e_j - m) / \sum_{k \in M} \exp(e_k - m) = \alpha_j$ for $j \in M$. With $m = \max_{k \in M} e_k$, every exponent is at most 0 and the denominator is at least 1.

*Proof.* Multiply the numerator and the denominator by $e^{m}$. With $m$ the maximum, each $e_j - m \le 0$, and the term of a maximizing $k$ is $e^0 = 1$, so the sum of non-negative terms is at least 1. Positions outside $M$ have the score $-\infty$, and $\exp(-\infty) = 0$, so they add nothing and get the weight 0. $\square$

So line L6 computes $\alpha$ without overflow, and the division never divides by a number below 1.

**Theorem 1 (the output).** Lines L1 to L8 return $c$ and $\alpha$ of the definition, with $\alpha_j \ge 0$, $\sum_j \alpha_j = 1$ and $\alpha_j = 0$ for $j \notin M$. Hence $c$ lies in the convex hull of $\{h_j : j \in M\}$. Moreover $|e_j| \le \|v\|_1$ for every $j$, so the weights satisfy $\alpha_j \ge e^{-2\|v\|_1} / |M|$ for $j \in M$.

*Proof.* Line L1 computes $q = W s$ once, and lines L3 and L4 compute $e_j = v^\top \tanh(q + U h_j)$, which is the definition because $W s + U h_j = q + U h_j$. Line L5 sets the score of a masked position to $-\infty$. By Lemma 1, line L6 gives the weights of the definition. They are non-negative and sum to 1 because the numerators are the terms of the denominator. Line L7 forms $c$. A combination with non-negative weights that sum to 1 is a convex combination.

Each coordinate of $\tanh$ is in $(-1, 1)$, so $|e_j| \le \sum_t |v_t| = \|v\|_1$. For $j \in M$, $\exp(e_j) \ge e^{-\|v\|_1}$ and each term of the denominator is at most $e^{\|v\|_1}$, which gives the bound on $\alpha_j$. $\square$

The bound says that additive attention cannot put all of its weight on one position unless $\|v\|$ is large: the score is bounded by the size of $v$, not by the size of $s$ and $h_j$. A dot-product score has no such bound.

**Theorem 2 (the gradients).** Let $L = g^\top c$ for a fixed $g \in \mathbb{R}^{d_h}$, and write $z_j = W s + U h_j$, $u_j = \tanh(z_j)$ and $\gamma_j = g^\top h_j$. Then, with $\bar\gamma = \sum_k \alpha_k \gamma_k$, $\delta_j = \alpha_j (\gamma_j - \bar\gamma)$ and $r_j = \delta_j \, (v \odot (1 - u_j \odot u_j))$,

$$\frac{\partial L}{\partial v} = \sum_j \delta_j u_j, \quad \frac{\partial L}{\partial W} = \Bigl(\sum_j r_j\Bigr) s^\top, \quad \frac{\partial L}{\partial s} = W^\top \sum_j r_j, \quad \frac{\partial L}{\partial U} = \sum_j r_j h_j^\top, \quad \frac{\partial L}{\partial h_j} = \alpha_j g + U^\top r_j,$$

where $\delta_j = 0$ and $r_j = 0$ for a masked $j$.

*Proof.* By the chain rule. $L = \sum_j \alpha_j \gamma_j$, so $\partial L / \partial \alpha_j = \gamma_j$, and $h_j$ also enters directly with $\partial L / \partial h_j = \alpha_j g$ from this term. The softmax has $\partial \alpha_k / \partial e_j = \alpha_k ([k = j] - \alpha_j)$ for $j, k \in M$, so $\partial L / \partial e_j = \sum_k \gamma_k \alpha_k ([k = j] - \alpha_j) = \alpha_j \gamma_j - \alpha_j \bar\gamma = \delta_j$. A masked score is the constant $-\infty$ and does not depend on the parameters, so it gives no term. From $e_j = v^\top u_j$: $\partial e_j / \partial v = u_j$ and $\partial e_j / \partial z_j = v \odot (1 - u_j \odot u_j)$, because $\tanh' = 1 - \tanh^2$. So $\partial L / \partial z_j = r_j$. Finally $z_j$ is linear: $\partial z_j / \partial W$ gives $r_j s^\top$, $\partial z_j / \partial s$ gives $W^\top r_j$, $\partial z_j / \partial U$ gives $r_j h_j^\top$ and $\partial z_j / \partial h_j$ gives $U^\top r_j$. Summing over $j$ gives the formulas. $\square$

The tests compare these gradients with central finite differences.

**Remark (complexity).** Line L1 costs $O(a d_s)$, line L3 costs $O(a d_h)$ per position, line L4 costs $O(a)$ per position, and lines L6 and L7 cost $O(J + J d_h)$. One decoder step therefore costs $O(a d_s + J a d_h + J d_h)$. The keys $U h_j$ do not depend on the decoder step, so over $I$ decoder steps they are computed once, and the total is $O(J a d_h + I (a d_s + J a + J d_h))$.
