---
title: Free-flight sampling gives the exact law of the distance to collision
proves: [correctness]
status: full
---

We assume exact arithmetic and an exact uniform random number $\xi$ on $(0, 1]$. The particle starts at $x_0$ in region $i_0$ with direction cosine $\mu \ne 0$, and $\Sigma(y) \ge 0$ is the piecewise constant total cross section at the point $y$. Write $\tau(s) = \int_0^s \Sigma(x_0 + \mu s')\, ds'$ for the optical depth after a path length $s$, and let $s_{\text{face}}$ be the path length to the outer face of the slab and $\tau_{\text{face}} = \tau(s_{\text{face}})$.

**Lemma 1 (the physical law).** If the probability of a collision in $[s, s + ds)$, given no collision before $s$, is $\Sigma(x_0 + \mu s)\, ds + o(ds)$, then the probability $G(s)$ of no collision on $[0, s]$ is $e^{-\tau(s)}$.

*Proof.* The hypothesis gives $G(s + ds) = G(s)(1 - \Sigma(x_0 + \mu s)\, ds + o(ds))$, so $G' = -\Sigma G$ at every point where $\Sigma$ is continuous, and $G$ is continuous everywhere. With $G(0) = 1$, the unique solution is $G(s) = e^{-\tau(s)}$. $\square$

**Lemma 2 (the depth).** $T = -\ln \xi$ satisfies $P(T > t) = e^{-t}$ for $t \ge 0$.

*Proof.* $T > t$ holds if and only if $\xi < e^{-t}$. Because $\xi$ is uniform on $(0, 1]$ and $e^{-t} \in (0, 1]$, this has probability $e^{-t}$. $\square$

**Lemma 3 (the loop).** Let $T = -\ln \xi$ and $S^\ast = \inf\{s \ge 0 : \tau(s) \ge T\}$. If $S^\ast < s_{\text{face}}$, FREE-FLIGHT returns a collision at path length $S^\ast$; otherwise it returns escape.

*Proof.* Let $c_0 = 0 < c_1 < \cdots$ be the path lengths at which the particle reaches the faces of the regions it crosses, so the region crossed on $[c_j, c_{j+1}]$ has the constant cross section $\Sigma_j$ and the path length $d_j = c_{j+1} - c_j$. We show by induction on $j$ that when the loop starts its pass $j$, the particle is at path length $c_j$ and the variable $\tau$ holds $T - \tau(c_j)$, and $\tau(c_j) < T$ unless $j = 0$ and $T = 0$. For $j = 0$ this is line L3. In pass $j$, line L6 compares $\Sigma_j d_j = \tau(c_{j+1}) - \tau(c_j)$ with $T - \tau(c_j)$. If $\tau(c_{j+1}) > T$, line L7 returns the point at path length $c_j + (T - \tau(c_j))/\Sigma_j$, where $\tau$ is linear with slope $\Sigma_j > 0$ and equals $T$. This is $S^\ast$, because $\tau < T$ on $[0, c_j]$ by the induction hypothesis and $\tau$ increases strictly on $[c_j, c_{j+1}]$. If $\tau(c_{j+1}) \le T$, lines L8 and L9 set $\tau \leftarrow T - \tau(c_{j+1})$ and move to $c_{j+1}$, which is the hypothesis for $j + 1$, and line L10 returns escape if $c_{j+1} = s_{\text{face}}$. In that case $\tau(s) \le T$ on the whole path, so $S^\ast \ge s_{\text{face}}$ up to the event $\tau(c_{j+1}) = T$ exactly. $\square$

The event $\tau(c_j) = T$ for some face $j$ has probability 0, because $T$ has a density and there are finitely many faces. Up to this event, $S^\ast > s$ if and only if $T > \tau(s)$, because $\tau$ is continuous and does not decrease.

**Theorem.** For $0 \le s < s_{\text{face}}$, the path length $S$ of the returned collision satisfies $P(S > s) = e^{-\tau(s)}$, and the escape probability is $e^{-\tau_{\text{face}}}$. So the sample has the physical law of Lemma 1.

*Proof.* By Lemma 3, $S > s$ (a collision after $s$ or an escape) is the event $S^\ast > s$, which is the event $T > \tau(s)$ up to a null event. By Lemma 2 it has probability $e^{-\tau(s)}$. Escape is the event $T \ge \tau_{\text{face}}$, with probability $e^{-\tau_{\text{face}}}$. $\blacksquare$

**The uniform medium.** If $\Sigma = \Sigma_t > 0$ everywhere, $\tau(s) = \Sigma_t s$ and the collision is at $S = T/\Sigma_t = -\ln(\xi)/\Sigma_t$, which is FREE-FLIGHT-UNIFORM. Its density is $\Sigma_t e^{-\Sigma_t s}$ with mean and standard deviation $1/\Sigma_t$.

**Why one depth is enough.** The memoryless property $P(T > t_0 + t \mid T > t_0) = e^{-t}$ shows that the depth left after a face, $T - \tau(c_j)$ given $T > \tau(c_j)$, has again the exponential law with mean 1 and is independent of the path so far. So drawing a new depth at each face gives the same law, which is the reason why codes may do either.
