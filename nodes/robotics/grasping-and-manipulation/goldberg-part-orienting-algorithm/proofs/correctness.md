---
title: Goldberg's algorithm finds a shortest squeeze plan that orients a polygonal part up to the symmetry of its squeeze function
proves: [correctness]
status: full
---

We use the notation of the page. The squeeze function $s : \mathbb{R} \to \mathbb{R}$ is a nondecreasing step function. Its steps are $[e_j, e_{j+1})$, closed on the left and open on the right, and step $j$ maps to the stable orientation $m_j$ with $e_j < m_j < e_{j+1}$. The indices run over all integers. $T$ is the smallest period of $s$, so $s(\theta + T) = s(\theta) + T$ for all $\theta$, and there are $r$ steps in one period: $e_{j+r} = e_j + T$ and $m_{j+r} = m_j + T$. A squeeze with the gripper at the world angle $\alpha$ maps the world orientation $\varphi$ of the part to $\alpha + s(\varphi - \alpha)$. An arc of length $L$ is a set $[a, a + L)$ taken modulo $T$; when $L \ge T$ it is the whole circle $\mathbb{R}/T\mathbb{Z}$. A set $X$ of orientations is *collapsible in $i$ squeezes* if some plan $(\alpha_1, \ldots, \alpha_i)$ maps all of $X$ to one orientation modulo $T$.

The lengths of the algorithm are $L_1 = \max_j (e_{j+1} - e_j)$, the widest step, and, while $L_i < T$,

$$L_{i+1} = \max\{\, e_{q+1} - e_p \;:\; p \le q,\ m_q - m_p < L_i \,\}.$$

Line L6 of the page computes this maximum, and the pair $(p, q)$ that attains it gives the s-interval $\Theta_{i+1} = [e_p, e_{q+1})$ with the s-image $[m_p, m_q]$.

**Lemma 1 (aliasing).** For every plan $\rho$ and every $\varphi$, $\rho(\varphi + T) = \rho(\varphi) + T$. So no plan maps $\varphi$ and $\varphi + T$ to the same orientation, and the best that a plan can do is to fix the orientation modulo $T$.

*Proof.* For one squeeze, $\alpha + s(\varphi + T - \alpha) = \alpha + s(\varphi - \alpha) + T$ by the period of $s$. A plan is a composition of squeezes, and each one commutes with the shift by $T$. $\square$

**Lemma 2 (characterization).** Let $i \ge 1$ and assume $L_{i-1} < T$ when $i \ge 2$. A set $X$ of orientations is collapsible in $i$ squeezes if and only if $X$ lies in an arc of length $L_i$.

*Proof.* By induction on $i$.

Case $i = 1$. Let $j$ be a widest step. If $X \subseteq [a, a + L_1)$ modulo $T$, squeeze at $\alpha = a - e_j$. Then $\varphi - \alpha$ is in $[e_j, e_{j+1})$ modulo $T$ for each $\varphi \in X$, so each $\varphi$ goes to $\alpha + m_j$ modulo $T$. Conversely, let one squeeze at $\alpha$ map $X$ to one orientation modulo $T$. The $r$ minima $m_0, \ldots, m_{r-1}$ of one period are different modulo $T$, so different steps of one period map to different orientations. So all $\varphi - \alpha$ with $\varphi \in X$ lie in one step modulo $T$, and $X$ lies in an arc of length $e_{j+1} - e_j \le L_1$, so also in an arc of length $L_1$.

Case $i + 1$, with $L_i < T$. First the "if" part. Let $L_{i+1} = e_{q+1} - e_p$ with $m_q - m_p < L_i$, and let $X$ lie in the arc $[a, a + L_{i+1})$. Squeeze at $\alpha = a - e_p$. Each $\varphi - \alpha$ is in $[e_p, e_{q+1})$ modulo $T$, which is the union of the steps $p$ to $q$. (When $L_{i+1} \ge T$ this union covers the circle, so the claim holds for every $X$.) So the image of $X$ is in $\{\alpha + m_p, \ldots, \alpha + m_q\}$ modulo $T$. This set lies in the closed arc from $\alpha + m_p$ to $\alpha + m_q$, of length $m_q - m_p < L_i$, so it lies in the arc $[\alpha + m_p, \alpha + m_p + L_i)$. By the induction hypothesis, the image is collapsible in $i$ squeezes, so $X$ is collapsible in $i + 1$.

Now the "only if" part. Let $(\alpha_1, \ldots, \alpha_{i+1})$ collapse $X \neq \emptyset$, and let $Y$ be the image of $X$ after the first squeeze. Then $Y$ is collapsible in $i$ squeezes, so by the induction hypothesis $Y$ lies in an arc $A$ of length $L_i < T$. Lift $A$ to the real interval $[c, c + L_i)$. The indices $j$ with $\alpha_1 + m_j \in [c, c + L_i)$ form a run $p, p+1, \ldots, q$ of consecutive integers, because $m_j$ increases with $j$, and $m_q - m_p < L_i$. Each point of $Y$ is $\alpha_1 + m_j$ modulo $T$ for such a $j$. A point $\varphi \in X$ goes to $\alpha_1 + m_j$ only if $\varphi - \alpha_1$ is in step $j$ modulo $T$. So $X - \alpha_1$ lies in the union of the steps $p$ to $q$ modulo $T$, which is the arc $[e_p, e_{q+1})$. Its length is $e_{q+1} - e_p \le L_{i+1}$ by the definition of $L_{i+1}$. So $X$ lies in an arc of length $L_{i+1}$. $\square$

**Lemma 3 (progress).** If $0 < L_i < T$, then $L_{i+1} > L_i$.

*Proof.* Let $h = L_i$ and $g(\theta) = s(\theta + h) - s(\theta) - h$. The function $g$ has period $T$ and is a bounded step function on $[0, T]$, so it is integrable. With the substitution $\theta \mapsto \theta - h$ and the period of $s$,

$$\int_0^T s(\theta + h)\, d\theta = \int_h^T s(\theta)\, d\theta + \int_0^h \bigl(s(\theta) + T\bigr)\, d\theta = \int_0^T s(\theta)\, d\theta + hT,$$

so $\int_0^T g(\theta)\, d\theta = hT - hT = 0$. This is the integral argument of Goldberg (1993, Section 6).

Suppose $g \ge 0$ almost everywhere. Then $g = 0$ almost everywhere, so $s(\theta + h) = s(\theta) + h$ for all $\theta$ outside a set $N$ of measure zero. Both sides are continuous from the right. For any $\theta$, take $\theta_n \downarrow \theta$ with $\theta_n \notin N$ and pass to the limit: the identity holds for every $\theta$. Then $h$ is a period of $s$ with $0 < h < T$, which contradicts the choice of $T$ as the smallest period.

So $g < 0$ on a set of positive measure. The breakpoints $e_j$ form a discrete set, so we can pick $\theta$ in this set such that neither $\theta$ nor $\theta + h$ is a breakpoint. Let $p$ be the step of $\theta$ and $q$ the step of $\theta + h$; then $q \ge p$, and $m_q - m_p = s(\theta + h) - s(\theta) < h$. Because $\theta$ and $\theta + h$ are not breakpoints, $e_p < \theta$ and $\theta + h < e_{q+1}$. So the pair $(p, q)$ is allowed in the definition of $L_{i+1}$, and $L_{i+1} \ge e_{q+1} - e_p > h = L_i$. $\square$

**Lemma 4 (termination).** The loop of lines L5 to L7 stops after at most $r^2$ rounds, with $L_k = T$.

*Proof.* In the definition of $L_{i+1}$, the condition $m_q - m_p < L_i < T = m_{p+r} - m_p$ gives $q \le p + r - 1$. So $L_{i+1} = e_{q+1} - e_p$ with $0 \le q - p \le r - 1$, and $L_{i+1} \le e_{p+r} - e_p = T$. By the period, the value depends only on $p$ modulo $r$ and on $q - p$, so every $L_i$ is one of at most $r^2$ numbers in $(0, T]$. By Lemma 3, the $L_i$ increase strictly while $L_i < T$. A strictly increasing sequence in a set of at most $r^2$ numbers has at most $r^2$ terms, so some $L_k$ is not less than $T$, and then $L_k = T$. $\square$

The bound $r^2$ is only what this short proof gives. Goldberg (1993) proves $O(n^2)$ and Chen and Ierardi (1995) prove $O(n)$ squeezes, where $n$ is the number of vertices of the convex hull and $r \le n$.

**Theorem (correctness and optimality).** Let $k$ be the first index with $L_k = T$. The plan $(\alpha_1, \ldots, \alpha_k)$ of lines L8 to L11 maps every initial orientation to $\alpha_k + m_{p_1}$ modulo $T$, where $\Theta_1 = [e_{p_1}, e_{p_1 + 1})$. No plan with fewer than $k$ squeezes maps every initial orientation to one orientation modulo $T$.

*Proof.* Optimality first. The set of all orientations lies in an arc of length $L$ only when $L \ge T$, because an arc of length less than $T$ misses a point of the circle. By Lemma 2, the whole circle is collapsible in $i$ squeezes only if $L_i \ge T$. For $i < k$ we have $L_i < T$, so no plan of $i < k$ squeezes works.

Now the plan. Write $(p_\ell, q_\ell)$ for the pair of level $\ell$, so that $\Theta_\ell = [e_{p_\ell}, e_{q_\ell + 1})$ and its s-image is $[m_{p_\ell}, m_{q_\ell}]$. We show by induction on $t = 1, \ldots, k$ that after squeeze $t$ the world orientation $\varphi_t$ satisfies $\varphi_t - \alpha_t \equiv m_j \pmod T$ for some $j$ with $p_\ell \le j \le q_\ell$, where $\ell = k - t + 1$.

For $t = 1$, $\alpha_1 = 0$ and $\Theta_k$ has length $T$, so every $\varphi$ has $\varphi - \alpha_1$ in $\Theta_k$ modulo $T$. The squeeze sends it to $m_j$ with $p_k \le j \le q_k$.

For the step from $t$ to $t + 1$, let $(p, q)$ be the pair of level $\ell = k - t + 1$ and $[a, b) = \Theta_{\ell - 1}$. Line L11 sets $\alpha_{t+1} = \alpha_t + m_p - a - \sigma/2$ with the slack $\sigma = (b - a) - (m_q - m_p)$, and $\sigma > 0$ because $m_q - m_p < L_{\ell - 1} = b - a$. By the induction hypothesis, $\varphi_t - \alpha_{t+1} \equiv m_j - m_p + a + \sigma/2$, with $0 \le m_j - m_p \le m_q - m_p$. So $\varphi_t - \alpha_{t+1}$ lies in $[a + \sigma/2,\ b - \sigma/2]$ modulo $T$, inside $\Theta_{\ell - 1}$, and the squeeze sends it to some $m_{j'}$ with $p_{\ell-1} \le j' \le q_{\ell-1}$. This is the claim for $t + 1$.

At $t = k$ the level is $\ell = 1$, where $p_1 = q_1$. So every initial orientation ends at $\alpha_k + m_{p_1}$ modulo $T$. By Lemma 1, this is the most that any plan can achieve. $\square$

**Remark (margin).** The proof shows more. If the gripper turn between squeezes $t$ and $t + 1$ errs by less than $\sigma/2$ of level $k - t + 1$, the orientation still lands strictly inside $\Theta_{k-t}$, and the plan still works. Goldberg (1993, Section 4.1) uses the same half slack $\epsilon_j$ for this reason.
