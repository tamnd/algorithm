---
title: Quantum phase estimation is within 2^-n of phi with probability at least 1 - delta
proves: [correctness]
status: full
---

We write $T = 2^t$, $e(x) = e^{2\pi i x}$, and $d_\circ(a, c) = \min_{z \in \mathbb{Z}} |a - c - z|$. Register A is qubits $0$ to $t - 1$, with qubit $j$ holding bit $x_j$ of $x = \sum_j x_j 2^j$, and register B holds $|u\rangle$ with $U|u\rangle = e(\varphi)|u\rangle$, $\varphi \in [0, 1)$. We use that the QFT circuit computes $F_T|x\rangle = T^{-1/2}\sum_m e(xm/T)|m\rangle$ (proved on the [quantum Fourier transform](/quantum-fourier-transform/) page), so its inverse computes $F_T^\dagger |x\rangle = T^{-1/2} \sum_m e(-xm/T)|m\rangle$.

**Lemma 1 (after line L3).** The state after line L3 is $T^{-1/2} \sum_{x} e(x\varphi)|x\rangle \otimes |u\rangle$.

*Proof.* Line L2 gives $T^{-1/2} \sum_x |x\rangle|u\rangle$. On $|x\rangle|u\rangle$ the gate $\mathrm{c}U^{2^j}$ with control qubit $j$ applies $U^{2^j x_j}$ to register B. All $t$ gates together apply $U^{\sum_j x_j 2^j} = U^x$, and $U^x |u\rangle = e(x\varphi)|u\rangle$. By linearity the claim follows. $\square$

**Lemma 2 (distribution).** Line L5 gives $m$ with probability $P(m) = |\alpha_m|^2$, where for $\Delta = \varphi - m/T$
$$\alpha_m = \frac{1}{T}\sum_{x=0}^{T-1} e(x\Delta), \qquad P(m) = \frac{\sin^2(\pi T\Delta)}{T^2\sin^2(\pi\Delta)} \text{ if } \Delta \notin \mathbb{Z}, \qquad P(m) = 1 \text{ if } \Delta \in \mathbb{Z}.$$
$P(m)$ depends only on $\Delta \bmod 1$. If $T\varphi$ is an integer, $m = T\varphi$ with probability $1$.

*Proof.* By Lemma 1 and the formula for $F_T^\dagger$, register A after line L4 is $\sum_m \alpha_m |m\rangle$ with $\alpha_m = T^{-1} \sum_x e(x\varphi) e(-xm/T)$, and register B is still $|u\rangle$ in a product state. If $\Delta \in \mathbb{Z}$, every term is $1$. Otherwise the geometric sum is $(1 - e(T\Delta))/(T(1 - e(\Delta)))$, and $|1 - e(y)| = 2|\sin(\pi y)|$. Both $\sin^2(\pi T\Delta)$ and $\sin^2(\pi\Delta)$ have period $1$ in $\Delta$, since $T$ is an integer. If $T\varphi = a$ is an integer, then $\Delta \in \mathbb{Z}$ exactly for $m = a$, so $P(a) = 1$. $\square$

**Lemma 3 (the nearest value).** Let $m$ be the outcome with $d_\circ(m/T, \varphi) \le 1/(2T)$. Then $P(m) \ge 4/\pi^2$.

*Proof.* Choose the representative $\Delta \in [-1/(2T), 1/(2T)]$. If $\Delta = 0$, $P(m) = 1$. Otherwise $\sin(\pi y) \ge 2y$ for $y \in [0, 1/2]$, by concavity of the sine on $[0, \pi/2]$, so $\sin^2(\pi T\Delta) \ge 4T^2\Delta^2$. Also $\sin^2(\pi\Delta) \le \pi^2\Delta^2$. So $P(m) \ge 4T^2\Delta^2/(T^2\pi^2\Delta^2) = 4/\pi^2$. $\square$

**Lemma 4 (the two nearest values).** Let $c = \lfloor T\varphi \rfloor$. Then $P(c) + P(c + 1 \bmod T) \ge 8/\pi^2$. So $d_\circ(m/T, \varphi) < 1/T$ with probability at least $8/\pi^2$.

*Proof.* Let $\beta = T\varphi - c \in [0, 1)$. If $\beta = 0$, $P(c) = 1$. Otherwise the two outcomes have $T\Delta = \beta$ and $T\Delta = \beta - 1$, so $\sin^2(\pi T\Delta) = \sin^2(\pi\beta)$ for both. With $\sin y \le y$ for $y \ge 0$,
$$P(c) + P(c+1) = \frac{\sin^2(\pi\beta)}{T^2}\Big(\frac{1}{\sin^2(\pi\beta/T)} + \frac{1}{\sin^2(\pi(1-\beta)/T)}\Big) \ge \frac{g(\beta)}{\pi^2}, \qquad g(\beta) = \sin^2(\pi\beta)\Big(\frac{1}{\beta^2} + \frac{1}{(1-\beta)^2}\Big).$$
We show $g(\beta) \ge 8$. Since $g(\beta) = g(1 - \beta)$, write $\beta = (1 - w)/2$ with $w \in [0, 1)$. Then $\beta(1-\beta) = (1 - w^2)/4$, $\beta^2 + (1-\beta)^2 = (1 + w^2)/2$ and $\sin(\pi\beta) = \cos(\pi w/2)$, so
$$g(\beta) = \frac{8\cos^2(\pi w/2)(1 + w^2)}{(1 - w^2)^2},$$
and we need $\cos^2(\pi w/2)(1 + w^2) \ge (1 - w^2)^2$. The product formula $\cos(\pi w/2) = \prod_{k \ge 1}(1 - w^2/(2k-1)^2)$ and the inequality $\prod_k (1 - a_k) \ge 1 - \sum_k a_k$ for $a_k \in [0, 1]$ give
$$\cos(\pi w/2) \ge (1 - w^2)(1 - \gamma w^2), \qquad \gamma = \sum_{k \ge 2} \frac{1}{(2k-1)^2} = \frac{\pi^2}{8} - 1 \approx 0.234.$$
Both factors are positive, so it is enough that $(1 - \gamma z)^2(1 + z) \ge 1$ for $z = w^2 \in [0, 1)$. Expand: $(1 - \gamma z)^2(1 + z) = 1 + z\big((1 - 2\gamma) + (\gamma^2 - 2\gamma)z + \gamma^2 z^2\big)$. Since $\gamma^2 - 2\gamma < 0$ and $z < 1$, the bracket is at least $1 - 4\gamma + \gamma^2 = 5 - \pi^2/2 + \gamma^2 > 0$, because $\pi^2/2 < 4.94$. So $g(\beta) \ge 8$, with equality at $\beta = 1/2$. $\square$

**Lemma 5 (the tail).** Let $c = \lfloor T\varphi \rfloor$, and write each outcome as $m = c + l \bmod T$ with $-T/2 < l \le T/2$. For an integer $e \ge 2$, the probability that $|l| > e$ is at most $1/(2(e - 1))$.

*Proof.* Let $\beta = T\varphi - c \in [0, 1)$. Then $\Delta \equiv (\beta - l)/T \pmod 1$, and the representative $y = (\beta - l)/T$ lies in $[-1/2, 1/2)$, because $-T/2 < l \le T/2$. By Lemma 2, $|\alpha_m| \le 2/(T|1 - e(y)|)$, and $|1 - e(y)| = 2|\sin(\pi y)| \ge 4|y|$ for $|y| \le 1/2$. So $|\alpha_m| \le 1/(2|\beta - l|)$. For $l \ge e + 1$, $l - \beta > l - 1 \ge e$. For $l \le -(e + 1)$, $|l - \beta| \ge |l|$. Hence
$$\Pr[|l| > e] \le \frac{1}{4}\Big(\sum_{l \ge e+1} \frac{1}{(l-1)^2} + \sum_{l \ge e+1} \frac{1}{l^2}\Big) \le \frac{1}{2}\sum_{l \ge e} \frac{1}{l^2} \le \frac{1}{2}\int_{e-1}^{\infty} \frac{dx}{x^2} = \frac{1}{2(e-1)}.$$
The last step uses $1/l^2 \le \int_{l-1}^{l} dx/x^2$. $\square$

**Theorem.** Let $n \ge 1$, $\delta \in (0, 1)$ and $t = n + \lceil \log_2(2 + 1/(2\delta)) \rceil$. Then PHASE-ESTIMATION returns $\tilde\varphi = m/T$ with $d_\circ(\tilde\varphi, \varphi) < 2^{-n}$ with probability at least $1 - \delta$.

*Proof.* Let $e = 2^{t-n} - 1$. Since $2 + 1/(2\delta) > 2$, $t - n \ge 2$ and $e \ge 3$. Write $m = c + l \bmod T$ as in Lemma 5. If $|l| \le e$, then $d_\circ(m/T, \varphi) \le |l - \beta|/T$, and $|l - \beta| < e + 1$: for $l \ge 0$ both $l$ and $\beta$ are less than $e + 1$, and for $l < 0$, $|l - \beta| = |l| + \beta < e + 1$. So $d_\circ(m/T, \varphi) < (e + 1)/T = 2^{-n}$. By Lemma 5 the failure probability is at most $1/(2(e-1)) = 1/(2(2^{t-n} - 2))$. By the choice of $t$, $2^{t-n} \ge 2 + 1/(2\delta)$, so $2(2^{t-n} - 2) \ge 1/\delta$ and the failure probability is at most $\delta$. $\blacksquare$

**Lemma 6 (superposition input).** If register B starts in $\sum_k c_k |u_k\rangle$ with orthonormal eigenvectors $|u_k\rangle$ of phases $\varphi_k$, then $\Pr[m] = \sum_k |c_k|^2 P_{\varphi_k}(m)$, where $P_\varphi$ is the distribution of Lemma 2.

*Proof.* By linearity and Lemma 2, the state before line L5 is $\sum_k c_k \big(\sum_m \alpha_m(\varphi_k)|m\rangle\big) \otimes |u_k\rangle$. The probability of $m$ is the squared norm of $\sum_k c_k \alpha_m(\varphi_k)|u_k\rangle$, which is $\sum_k |c_k|^2 |\alpha_m(\varphi_k)|^2$ because the $|u_k\rangle$ are orthonormal. $\square$

**The cost.** Line L3 calls $\mathrm{c}U^{2^j}$ once for each $j < t$. If each call is made of $2^j$ uses of $\mathrm{c}U$, the total is $\sum_{j<t} 2^j = 2^t - 1$.
