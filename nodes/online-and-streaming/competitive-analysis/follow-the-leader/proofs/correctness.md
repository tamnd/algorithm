---
title: Be the leader, the linear regret of follow the leader, its O(log T) regret for squared loss, and the bound εRAT + D/ε of follow the perturbed leader
proves: [be-the-leader, lower-bound, squared-loss-regret, ftpl-regret]
status: full
---

Let $K$ be a set of actions and $\ell_1, \ldots, \ell_T$ loss functions on $K$, fixed in advance (an oblivious adversary). Write $L_t(x) = \sum_{s \le t} \ell_s(x)$, with $L_0 = 0$. Follow the leader plays $x_t \in \arg\min_{x \in K} L_{t-1}(x)$, with a fixed rule for ties; for experts, line L3 is this rule with the least index on ties. We assume that each minimum exists.

**Lemma 1 (be the leader).** $\sum_{t=1}^{T} \ell_t(x_{t+1}) \le \min_{x \in K} L_T(x) = L_T(x_{T+1})$.

*Proof.* By induction on $T$. For $T = 0$ both sides are $0$. Suppose $\sum_{t=1}^{T-1} \ell_t(x_{t+1}) \le L_{T-1}(x_T)$. Since $x_T$ minimizes $L_{T-1}$, $L_{T-1}(x_T) \le L_{T-1}(x_{T+1})$. Add $\ell_T(x_{T+1})$ to both sides: $\sum_{t=1}^{T} \ell_t(x_{t+1}) \le L_{T-1}(x_{T+1}) + \ell_T(x_{T+1}) = L_T(x_{T+1})$, and $x_{T+1}$ minimizes $L_T$. $\square$

**Corollary 1.** The regret of follow the leader is at most $\sum_{t=1}^{T} \bigl(\ell_t(x_t) - \ell_t(x_{t+1})\bigr)$.

*Proof.* Subtract the inequality of Lemma 1 from $\sum_t \ell_t(x_t)$. $\square$

**Theorem 1 (FTL has linear regret).** For two experts and the losses $\ell_1 = (1/2, 0)$, then $(0, 1)$ in the even rounds and $(1, 0)$ in the odd rounds $t \ge 3$, FTL pays $T - 1/2$, and its regret is at least $T/2 - 1$.

*Proof.* After round 1 the totals are $(1/2, 0)$. We claim that after each even round $t$ they are $(1/2 + (t-2)/2,\ t/2)$ and after each odd round $t \ge 3$ they are $(1/2 + (t-1)/2,\ (t-1)/2)$. Both claims follow by induction: an even round adds $(0, 1)$ and an odd round adds $(1, 0)$. So before an even round expert 2 has the smaller total and FTL picks it, and it pays $1$; before an odd round $t \ge 3$ expert 1 has total $1/2 + (t-3)/2 < (t-1)/2$, FTL picks it, and it pays $1$. In round 1 the totals tie at $0$ and FTL pays $1/2$. So FTL pays $T - 1/2$. Expert 2 pays $\lfloor T/2 \rfloor \le T/2$, so the regret is at least $T - 1/2 - T/2 \ge T/2 - 1$. $\square$

**Theorem 2 (FTL for squared loss).** Let $K = [0, 1]$, $\ell_t(x) = (x - z_t)^2$ with $z_t \in [0, 1]$, and $x_1 \in [0, 1]$. Then FTL plays $x_{t+1} = \frac1t \sum_{s \le t} z_s$, and its regret is at most $2 H_T \le 2(1 + \ln T)$.

*Proof.* $L_t$ is a quadratic with its minimum at the mean of $z_1, \ldots, z_t$, which lies in $[0, 1]$. For $t \ge 2$, $x_{t+1} = \frac{(t-1)x_t + z_t}{t}$, so $x_{t+1} - z_t = \frac{t-1}{t}(x_t - z_t)$, and

$$\ell_t(x_t) - \ell_t(x_{t+1}) = (x_t - z_t)^2\left(1 - \frac{(t-1)^2}{t^2}\right) = (x_t - z_t)^2 \frac{2t - 1}{t^2} \le \frac{2}{t}.$$

For $t = 1$, $x_2 = z_1$, and the difference is $(x_1 - z_1)^2 \le 1 \le 2$. Corollary 1 gives regret at most $\sum_{t=1}^{T} 2/t = 2H_T$, and $H_T \le 1 + \ln T$. $\square$

## Follow the perturbed leader

Let $\mathcal{D} \subset \mathbb{R}^d$ be a finite set of decisions and let the losses be linear, $\ell_t(x) = x \cdot s_t$ with $s_t \in \mathbb{R}^d$. Let $M(v) \in \arg\min_{x \in \mathcal{D}} x \cdot v$ with a fixed tie rule, and constants $D \ge \|x - x'\|_1$ for all $x, x' \in \mathcal{D}$, $R \ge |x \cdot s_t|$ for all $x$ and $t$, and $A \ge \|s_t\|_1$ for all $t$. FTPL with parameter $\varepsilon > 0$ plays $M(s_{1:t-1} + p_t)$, where $s_{1:t} = s_1 + \cdots + s_t$ and $p_t$ is uniform on the cube $[0, 1/\varepsilon]^d$.

(For experts, $\mathcal{D}$ is the set of unit vectors, $D = 2$, $R = 1$ and $A = n$. Adding $p$ to the losses, or subtracting it as the implementation does, gives the same distribution up to a shift of the cube, and the proof is the same.)

**Lemma 2 (perturbed be the leader).** For every fixed $p \in [0, 1/\varepsilon]^d$, $\sum_{t=1}^{T} M(s_{1:t} + p) \cdot s_t \le M(s_{1:T}) \cdot s_{1:T} + D/\varepsilon$.

*Proof.* Apply Lemma 1 to the losses $s_0 = p, s_1, \ldots, s_T$, where the leader after round $t$ is $M(p + s_{1:t})$:

$$\sum_{t=0}^{T} M(p + s_{1:t}) \cdot s_t \le M(p + s_{1:T}) \cdot (p + s_{1:T}) \le M(s_{1:T}) \cdot (p + s_{1:T}).$$

Move the term $t = 0$ to the right: $\sum_{t=1}^{T} M(p + s_{1:t}) \cdot s_t \le M(s_{1:T}) \cdot s_{1:T} + (M(s_{1:T}) - M(p)) \cdot p$. The last term is at most $\|M(s_{1:T}) - M(p)\|_1 \|p\|_\infty \le D/\varepsilon$. $\square$

**Lemma 3 (overlap of cubes).** Let $C = [0, 1/\varepsilon]^d$ and $v \in \mathbb{R}^d$. The cubes $C$ and $v + C$ share at least a fraction $1 - \varepsilon\|v\|_1$ of their volume.

*Proof.* The intersection is a box with side $(1/\varepsilon - |v_j|)^+$ in coordinate $j$, so the shared fraction is $\prod_j (1 - \varepsilon|v_j|)^+ \ge 1 - \varepsilon \sum_j |v_j|$, by the inequality $\prod_j (1 - a_j) \ge 1 - \sum_j a_j$ for $a_j \in [0, 1]$ (and trivially if some $a_j > 1$). $\square$

**Theorem 3 (Kalai and Vempala).** Let the losses be nonnegative, $0 \le x \cdot s_t \le R$ for all $x \in \mathcal{D}$ and all $t$. Against an oblivious adversary, $\mathbb{E}[\sum_t M(s_{1:t-1} + p_t) \cdot s_t] \le \min_{x \in \mathcal{D}} x \cdot s_{1:T} + \varepsilon R A T + D/\varepsilon$.

*Proof.* Fix $t$. The point $s_{1:t-1} + p_t$ is uniform on the cube $s_{1:t-1} + C$, and the point $s_{1:t} + p_t$ is uniform on $s_{1:t-1} + (s_t + C)$. By Lemma 3, there is a coupling of the two points under which they are equal except on an event of probability at most $\varepsilon\|s_t\|_1 \le \varepsilon A$. On that event the first loss $M(\cdot) \cdot s_t$ is at most $R$ and the second is at least $0$, so

$$\mathbb{E}[M(s_{1:t-1} + p_t) \cdot s_t] \le \mathbb{E}[M(s_{1:t} + p_t) \cdot s_t] + \varepsilon R A.$$

Sum over $t$. Each $p_t$ has the law of one fixed $p$, so by linearity $\sum_t \mathbb{E}[M(s_{1:t} + p_t) \cdot s_t] = \mathbb{E}[\sum_t M(s_{1:t} + p) \cdot s_t]$, which Lemma 2 bounds by $\min_x x \cdot s_{1:T} + D/\varepsilon$. $\blacksquare$

**Corollary 2 (experts).** For $n$ experts with losses in $[0, 1]$, the expected regret of FTPL is at most $\varepsilon n T + 2/\varepsilon$, which is $2\sqrt{2nT}$ for $\varepsilon = \sqrt{2/(nT)}$.
