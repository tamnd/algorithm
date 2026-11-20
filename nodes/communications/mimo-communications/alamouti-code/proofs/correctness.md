---
title: "The Alamouti combiner decouples the two symbols, its decisions are maximum likelihood, and the diversity order is 2m"
proves: [correctness]
status: full
---

The model has two transmit antennas and $m$ receive antennas. Receive antenna $i$ sees, in the two slots of one block,

$$y_{i1} = h_{i1} s_1 + h_{i2} s_2 + w_{i1}, \qquad y_{i2} = -h_{i1} s_2^* + h_{i2} s_1^* + w_{i2},$$

where the gains $h_{ik}$ are known to the receiver and stay fixed over the block, and the $2m$ noise samples are independent $\mathcal{CN}(0, N_0)$. The symbols $s_1, s_2$ are independent and uniform on a finite set $\mathcal{A}$. Write $g = \sum_i (|h_{i1}|^2 + |h_{i2}|^2)$ and assume $g > 0$.

**Lemma 1 (the equivalent channel).** Let $\tilde y_i = (y_{i1}, y_{i2}^*)^T$ and $\tilde w_i = (w_{i1}, w_{i2}^*)^T$. Then $\tilde y_i = G_i s + \tilde w_i$ with $s = (s_1, s_2)^T$ and

$$G_i = \begin{pmatrix} h_{i1} & h_{i2} \\ h_{i2}^* & -h_{i1}^* \end{pmatrix}.$$

Stack the $m$ blocks into $\tilde y = G s + \tilde w$, with $G$ of size $2m \times 2$. Then $G^H G = g I_2$, and $\tilde w \sim \mathcal{CN}(0, N_0 I_{2m})$.

*Proof.* The first row is the first slot as it is. The conjugate of the second slot is $y_{i2}^* = -h_{i1}^* s_2 + h_{i2}^* s_1 + w_{i2}^*$, which is the second row. For each $i$, the two columns of $G_i$ are $c_1 = (h_{i1}, h_{i2}^*)^T$ and $c_2 = (h_{i2}, -h_{i1}^*)^T$. Then $c_1^H c_1 = c_2^H c_2 = |h_{i1}|^2 + |h_{i2}|^2$ and $c_1^H c_2 = h_{i1}^* h_{i2} - h_{i2} h_{i1}^* = 0$. Summing over $i$ gives $G^H G = g I_2$. If $w \sim \mathcal{CN}(0, N_0)$, then $w^*$ has the same law, because the law is invariant under conjugation (the real and imaginary parts are independent with equal variance). Conjugation of one sample does not change the independence of the samples. $\square$

**Lemma 2 (the combiner).** The lines L4 and L5 compute $(z_1, z_2)^T = G^H \tilde y$. So $z_k = g s_k + n_k$, where $n_1, n_2$ are independent $\mathcal{CN}(0, g N_0)$.

*Proof.* The first row of $G_i^H$ is $(h_{i1}^*, h_{i2})$ and the second row is $(h_{i2}^*, -h_{i1})$. Applied to $\tilde y_i$, they give $h_{i1}^* y_{i1} + h_{i2} y_{i2}^*$ and $h_{i2}^* y_{i1} - h_{i1} y_{i2}^*$, which are the terms of lines L4 and L5. So $G^H \tilde y = G^H G s + G^H \tilde w = g s + n$ by Lemma 1. The vector $n = G^H \tilde w$ is circularly symmetric Gaussian with covariance $G^H (N_0 I) G = g N_0 I_2$. A circularly symmetric Gaussian vector with a diagonal covariance has independent entries. $\square$

**Theorem 1 (maximum likelihood).** For every received block, the pair returned by line L7 minimizes $\|\tilde y - G s\|^2$ over $s \in \mathcal{A}^2$. So it is a maximum likelihood decision of $(s_1, s_2)$.

*Proof.* The likelihood of $s$ is proportional to $\exp(-\|\tilde y - G s\|^2 / N_0)$, by Lemma 1. Expand the norm and use $G^H G = g I$ and $G^H \tilde y = z$:

$$\|\tilde y - G s\|^2 = \|\tilde y\|^2 - 2\,\mathrm{Re}(s^H z) + g \|s\|^2 = \|\tilde y\|^2 - \frac{\|z\|^2}{g} + g \sum_{k=1}^{2} \left| s_k - \frac{z_k}{g} \right|^2.$$

The first two terms do not depend on $s$. The last sum has one term for $s_1$ and one term for $s_2$, and $s$ ranges over the full product $\mathcal{A} \times \mathcal{A}$. So the minimum is reached when each $s_k$ is a point of $\mathcal{A}$ nearest to $z_k / g$, which is what lines L6 and L7 compute. Ties happen only on the boundaries between decision regions, a set of probability zero. $\blacksquare$

**Theorem 2 (diversity order $2m$).** Let the $2m$ gains be i.i.d. $\mathcal{CN}(0, 1)$, and let each antenna send with amplitude $\sqrt{E_s/2}$, so that the total transmit energy per slot is $E_s$ on average for unit-energy symbols. Let $\bar\gamma = E_s/N_0$. Then the pairwise error probability between two symbols $a \ne b$ in $\mathcal{A}$ satisfies

$$P(a \to b) \le \left(1 + \frac{\bar\gamma\,|a - b|^2}{8}\right)^{-2m},$$

and the symbol error probability falls as $\bar\gamma^{-2m}$ at high SNR.

*Proof.* With the amplitude included in the gains, $g = (E_s/2) \sum_i (|h_{i1}|^2 + |h_{i2}|^2)$. By Lemma 2 the decision on $s_k$ is a scalar decision in the channel $z_k / g = s_k + n_k / g$, with noise variance $N_0 / g$. Given the channel, the probability that $b$ is nearer than $a$ to $z_k / g$ when $a$ was sent is $Q\big(\sqrt{g |a - b|^2 / (2 N_0)}\big)$. The bound $Q(x) \le \exp(-x^2/2)$ for $x \ge 0$ gives at most $\exp(-g |a - b|^2 / (4 N_0))$. The variable $\sum_i (|h_{i1}|^2 + |h_{i2}|^2)$ is a sum of $2m$ independent exponential variables of mean 1, and $\mathbb{E}\, e^{-t X} = 1/(1 + t)$ for $X \sim \mathrm{Exp}(1)$ and $t \ge 0$. So the average is

$$\mathbb{E} \exp\!\left(-\frac{\bar\gamma |a - b|^2}{8} \sum_i (|h_{i1}|^2 + |h_{i2}|^2)\right) = \left(1 + \frac{\bar\gamma |a - b|^2}{8}\right)^{-2m}.$$

The union bound over the $|\mathcal{A}| - 1$ wrong symbols gives a symbol error probability at most a constant times $\bar\gamma^{-2m}$. For the lower bound, the error event contains the event that the sum of the $2m$ exponential variables is below $1/\bar\gamma$; this event has a probability of order $\bar\gamma^{-2m}$, and on it the conditional error probability stays above a positive constant. So the exponent is exactly $2m$. $\square$

**Cost.** Line L3 and lines L4 and L5 each do $\Theta(m)$ complex operations. Lines L6 and L7 do two divisions and two nearest-point searches; the search is $\Theta(|\mathcal{A}|)$ by brute force and $\Theta(1)$ with a slicer for PAM, square QAM or PSK.
