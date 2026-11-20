---
title: CADIS is unbiased, and its exact-importance limit has zero variance
proves: [correctness]
status: full
---

We assume exact arithmetic and exact independent uniform random numbers. The slab, the cells, the cross sections and the lines L1 to L13 are those of the page. We write $\sigma_{\max} = \max_i \sigma_{d,i}$ and assume $c < 1$; the case $c = 1$ in a finite slab is the same, with the bound on the track length of Lemma 1 replaced by the one for a finite slab.

**The analog value function.** For a particle of unit weight that is about to start a flight at the point $x$ with the direction $\mu$, let $V(x, \mu)$ be the expected track-length score $\sum_i \sigma_{d,i} \cdot$ (track length in cell $i$) of the analog game, summed over the whole future of the particle. The [importance](/adjoint-importance-function/) page shows that $V$ is the adjoint flux; here we only need its definition as an expectation. In the analog game the expected number of collisions is at most $1/(1 - c)$ and each flight has the mean length $1/\Sigma_t$, so
$$0 \le V(x, \mu) \le V_{\max} = \frac{\sigma_{\max}}{\Sigma_t (1 - c)}.$$
By the analog page, the analog game is unbiased, so the exact response per source particle is
$$R = \sum_i q_i h \cdot \frac{1}{h} \int_{\text{cell } i} \frac{1}{2} \int_{-1}^{1} V(x, \mu)\, d\mu\, dx. \qquad (1)$$

**Lemma 1 (first event).** Let a particle of unit weight start a flight at $(x, \mu)$ in cell $i$, and let $s$ and $d$ be as in line L9. Then
$$V(x, \mu) = E\big[\sigma_{d,i} \min(s, d)\big] + P(s \ge d)\, V(e, \mu) + E\Big[\mathbf{1}[s < d]\; c \cdot \frac{1}{2} \int_{-1}^{1} V(x + \mu s, \mu')\, d\mu'\Big],$$
where $e$ is the edge of the cell and $V(e, \mu) = 0$ if the particle leaves the slab there.

*Proof.* Condition on the first flight. The track length in cell $i$ during the flight is $\min(s, d)$. If $s \ge d$, the particle is at the edge with the direction $\mu$, and because the exponential law has no memory, the rest of its path has the law of a new flight from $(e, \mu)$. If $s < d$, the particle collides at $x + \mu s$, survives with probability $c$, and starts a new flight with a direction uniform on $[-1, 1]$. Taking expectations gives the three terms. $\square$

**Lemma 2 (one event of CADIS keeps the value).** Let a particle of weight $w$ start a flight at $(x, \mu)$ in cell $i$ in CADIS-RUN. Let $\Delta$ be the score that line L10 adds during this flight, and let $B'$ be the set of particles (none, one, or several copies) that exist after lines L10 to L12. Then
$$E\Big[\Delta + \sum_{(x', \mu', w') \in B'} w' V(x', \mu')\Big] = w V(x, \mu).$$

*Proof.* The flight of line L9 has the analog law, so $E[\Delta] = w E[\sigma_{d,i} \min(s, d)]$, the first term of Lemma 1 times $w$. Consider the window check of lines L11 and L12 for a particle of weight $u$ at a point $y$ with direction $\nu$ in a cell $j$. If line L11 acts, it leaves $k \ge 1$ particles of weight $u/k$ at $(y, \nu)$, so $\sum w' V = u V(y, \nu)$. If line L12 acts, it leaves one particle of weight $\bar w_j$ with probability $u/\bar w_j$ and none otherwise, so $E[\sum w' V] = (u/\bar w_j)\, \bar w_j\, V(y, \nu) = u V(y, \nu)$. Otherwise the particle is unchanged. So the window check keeps $E[\sum w' V]$ in every case.

If $s \ge d$ and the particle stays in the slab, it reaches $(e, \mu)$ with weight $w$, and after the check the expected value is $w V(e, \mu)$. If it leaves, nothing remains and $V(e, \mu) = 0$. If $s < d$, implicit capture gives the weight $cw$ and line L10 samples $\mu'$ uniform on $[-1, 1]$ before the check, so the expected value after the check is $cw \cdot \frac{1}{2}\int V(x + \mu s, \mu')\, d\mu'$. Adding the three cases gives $w$ times the right side of Lemma 1, which is $w V(x, \mu)$. $\square$

The order matters here: the new direction is drawn before the check, so every copy has an independent future with the law of a scattered particle. If the copies kept the old direction, the expected value after the collision would be $cw\, V(x + \mu s, \mu)$, and Lemma 2 would fail.

**Theorem 1 (unbiasedness).** Assume $\phi^+_i > 0$ in every cell with $q_i > 0$, $1 < c_u$, $k_{\max} \ge 1$, and that the expected number of flights $T$ of one history (with all its copies) is finite. Then $E[S] = R$, the exact response of (1), whatever the values of $\phi^+$ are.

*Proof.* Number the flights of one history in the order in which CADIS-RUN does them, $t = 1, 2, \ldots, T$. After step $t$, let $S_t$ be the score so far and $B_t$ the set of particles that wait, including the one in flight, each with its weight and its state at the start of its next flight. Let
$$\Phi_t = S_t + \sum_{(x, \mu, w) \in B_t} w V(x, \mu).$$
Step $t + 1$ does one flight of one particle of $B_t$ and leaves the others alone, so Lemma 2 gives $E[\Phi_{t+1} \mid \mathcal{F}_t] = \Phi_t$, where $\mathcal{F}_t$ is the history up to step $t$. So $\Phi_t$ is a martingale up to the stopping time $T$, at which the bank is empty and $\Phi_T = S$.

The increments are bounded in conditional mean. A weight grows only at line L12, to a target $\bar w_j$, and at birth it is a target as well, so every weight is at most $W = \max_j \bar w_j$, which is finite because $\phi^+ > 0$ where it is used. One step adds at most $W \sigma_{\max} \min(s, d)$ to the score, with conditional mean at most $W\sigma_{\max}/\Sigma_t$, and changes the bank by at most $k_{\max} + 1$ particles, each with $w V \le W V_{\max}$. So $E[|\Phi_{t+1} - \Phi_t| \mid \mathcal{F}_t] \le W\sigma_{\max}/\Sigma_t + (k_{\max} + 2) W V_{\max}$. With $E[T] < \infty$, the optional stopping theorem in its form for bounded conditional increments gives $E[S] = E[\Phi_T] = E[\Phi_0]$.

At the start, line L7 picks cell $i$ with probability $p_i = q_i \phi^+_i h/\hat R$, which is positive where $q_i > 0$, gives the weight $\bar w_i = \hat R/\phi^+_i = q_i h/p_i$, and draws $(x, \mu)$ uniform in the cell and in direction. So
$$E[\Phi_0] = \sum_{i : q_i > 0} p_i \cdot \frac{q_i h}{p_i} \cdot \frac{1}{h}\int_{\text{cell } i} \frac{1}{2}\int_{-1}^{1} V(x, \mu)\, d\mu\, dx = R$$
by (1). The values $\phi^+_i$ cancel, which is why the quality of the adjoint does not enter the mean. $\square$

**Theorem 2 (zero variance with the exact importance, discrete form).** Consider a particle that moves on the states $1, \ldots, m$. From state $i$ it moves to state $j$ with probability $P_{ij} \ge 0$, or it ends with probability $e_i = 1 - \sum_j P_{ij} \ge 0$ and then scores $g_i \ge 0$. Assume the walk ends with probability 1 from every state. Let $v_i$ be the expected score from state $i$, so that
$$v_i = e_i g_i + \sum_j P_{ij} v_j, \qquad (2)$$
let $q$ be the start distribution and $R = \sum_i q_i v_i > 0$. Define the biased game on the states with $v_i > 0$: start in $i$ with probability $\hat q_i = q_i v_i/R$ and weight $R/v_i$; from $i$ move to $j$ with probability $\hat P_{ij} = P_{ij} v_j/v_i$ and multiply the weight by $P_{ij}/\hat P_{ij}$; end with probability $\hat e_i = e_i g_i/v_i$ and score the weight times $e_i g_i/\hat e_i$. Then every history of the biased game scores exactly $R$.

*Proof.* The biased probabilities are a distribution: $\sum_i \hat q_i = 1$ by the definition of $R$, and $\sum_j \hat P_{ij} + \hat e_i = (\sum_j P_{ij} v_j + e_i g_i)/v_i = 1$ by (2). A state with $v_j = 0$ has $\hat P_{ij} = 0$, so the biased walk never enters it. The weight starts at $w_0 = q_i/\hat q_i = R/v_{i_0}$. If $w_k = R/v_{i_k}$, a move to $j$ gives $w_{k+1} = w_k P_{ij}/\hat P_{ij} = w_k v_{i_k}/v_j = R/v_j$. So by induction the weight in state $i$ is always $R/v_i$, and the score at the end in state $i$ is $(R/v_i) \cdot e_i g_i/\hat e_i = (R/v_i) \cdot v_i = R$.

The biased walk ends with probability 1. The probability that it is still running after $n$ steps from state $i$ is $\sum_j (P^n)_{ij} v_j / v_i$, and $\sum_j (P^n)_{ij} v_j$ is the expected score of the analog walks from $i$ that last more than $n$ steps. Since the analog walk ends with probability 1 and $v$ is bounded, this tends to 0 by dominated convergence. $\square$

**How CADIS relates to Theorem 2.** The weight of the zero variance game in state $i$ is $R/v_i$, the importance in the denominator. CADIS uses the same value $\hat R/\phi^+_i$ for the birth weight and the window target, and lines L3 and L4 are exactly the biased start of Theorem 2 with $v$ replaced by $\phi^+$. CADIS does not change the flight and scattering laws; it uses splitting and roulette to keep each weight near the target, which makes the expected number of particles in a cell follow the importance, as the biased transitions $\hat P$ do. This link is a heuristic. Theorem 1 holds in all cases, and the variance reduction of a real run is a measurement.
