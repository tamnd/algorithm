---
title: What the asynchronous updates of A3C compute
proves: [correctness]
status: full
---

Notation is that of the page. A run is a sequence of events; each event is a *read* (lines L2 to L8 of one worker) or a *write* (line L9 of that worker), and each worker alternates read and write. Let $\theta_k$ be the shared parameters after $k$ writes (the critic $w$ is handled in the same way and we write only $\theta$). For a snapshot $\theta'$ and a segment $\sigma$, let $g(\theta', \sigma)$ be the update $(d\theta, c\, dw)$ of lines L3 to L8. The write of a worker adds $\eta\, g(\theta', \sigma)$, where $\theta'$ is the value read at its last read. We take each write to be atomic in this proof; a write that is split into coordinate updates gives the same sum, because additions to different coordinates, and additions to the same coordinate made as atomic increments, commute.

**Claim 1 (each worker computes an A2C gradient).** For a segment $\sigma = (S_{t_0}, A_{t_0}, R_{t_0+1}, \ldots, S_t)$, $g(\theta', \sigma)$ is the sum over the segment of the n-step advantage actor-critic terms of [A2C](/a2c/), with the return of step $i$ bootstrapped from $V_{w'}(S_t)$ after $t - i$ steps, or from 0 if the episode ended.

*Proof.* Line L5 sets $G$ to the bootstrap value. After the iteration of line L6 for index $i$, $G = \sum_{j=i}^{t-1} \gamma^{j-i} R_{j+1} + \gamma^{t-i} G_{\text{boot}}$, by induction downward from $i = t - 1$: the case $i = t-1$ is $R_t + \gamma G_{\text{boot}}$, and the step from $i + 1$ to $i$ multiplies by $\gamma$ and adds $R_{i+1}$. Lines L7 and L8 add the actor and critic terms with this $G$ and the snapshot $(\theta', w')$. Since a segment stops at the end of an episode, no return crosses into the next episode. These are the terms of lines L6 to L9 of A2C for one copy, summed instead of averaged. $\square$

**Claim 2 (zero delay).** If every read is followed by the write of the same worker before any other event, then $\theta_{k+1} = \theta_k + \eta\, g(\theta_k, \sigma_k)$ for the $k$-th segment $\sigma_k$.

*Proof.* Before the $k$-th read, exactly $k$ writes have happened, so the read copies $\theta_k$. The next event is the write of the same worker, which adds $\eta\, g(\theta_k, \sigma_k)$ to $\theta_k$. $\square$

**Claim 3 (a fully stale round).** If $N$ workers all read and then all write, in any order of the reads and any order of the writes, then the result is $\theta_0 + \eta \sum_{i=1}^{N} g(\theta_0, \sigma_i)$.

*Proof.* No write happens before the last read, so every worker reads $\theta_0$ and computes $g(\theta_0, \sigma_i)$. The $N$ writes add these vectors, and vector addition is commutative and associative, so the order of the writes does not change the sum. This is one synchronous A2C step on the union of the $N$ segments, with the summed gradient. $\square$

**Claim 4 (staleness bound).** Let $\bar g(\theta) = \mathbb{E}[g(\theta, \sigma)]$ be the mean update when the segment is drawn with the policy $\pi_\theta$, and suppose that $\lVert \bar g(\theta) - \bar g(\phi) \rVert \le L \lVert \theta - \phi \rVert$ and that every write has norm at most $\eta M$. If the write number $k + 1$ was read when the shared parameters were $\theta_{k - \tau}$ with $0 \le \tau \le \tau_{\max}$, then

$$\lVert \bar g(\theta_{k-\tau}) - \bar g(\theta_k) \rVert \le L \tau_{\max} \eta M.$$

*Proof.* Between the read and the write, $\tau$ other writes happened, each of norm at most $\eta M$. By the triangle inequality $\lVert \theta_k - \theta_{k-\tau} \rVert \le \tau \eta M \le \tau_{\max} \eta M$, and the Lipschitz bound gives the claim. $\square$

So each write of A3C is $\eta$ times the mean update at the current parameters, plus zero-mean noise, plus a bias of norm at most $L \tau_{\max} \eta^2 M$. For a fixed number of workers this bias is of a higher order in $\eta$ than the step itself, which is the standard form of a perturbed stochastic approximation. No claim is made that the mean update $\bar g$ is the gradient of the discounted return, for the reasons given on the [A2C](/a2c/) page, or that the nonlinear iteration converges. $\blacksquare$
