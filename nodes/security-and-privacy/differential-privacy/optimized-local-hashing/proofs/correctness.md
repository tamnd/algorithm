---
title: Optimized local hashing is epsilon-LDP, its estimate is unbiased, and g = e^epsilon + 1 minimizes the variance
proves: [correctness]
status: full
---

Let the domain be $\{0, \ldots, d - 1\}$, let $g \ge 2$, and let $\mathcal H = \{H_s : s \in \mathcal S\}$ be a finite family of functions from the domain to $\{0, \ldots, g - 1\}$ with the collision property

$$\Pr_s[H_s(u) = H_s(v)] = \frac1g \qquad \text{for all } u \ne v, \tag{1}$$

where $s$ is uniform on $\mathcal S$. The family of all functions has property (1), because the digits of a uniform seed in base $g$ are independent and uniform. Write $e = e^{\varepsilon} \ge 1$ (rational), $p = e/(e + g - 1)$ and $q = 1/g$. Let $R(v)$ be the report of line L1 to line L5 on the value $v$.

**Lemma 1 (the pmf of one report).** For every seed $s$ and every $y$,

$$\Pr[R(v) = (s, y)] = \frac{1}{|\mathcal S|} \cdot \begin{cases} p & \text{if } y = H_s(v), \\ (1 - p)/(g - 1) & \text{otherwise.}\end{cases}$$

*Proof.* Line L1 picks $s$ uniformly, and line L2 sets $x = H_s(v)$. Line L3 compares a uniform integer below the denominator of $p$ with its numerator, so it keeps $x$ (line L4) with probability $p$ exactly. Otherwise line L5 draws $r$ uniform on $\{0, \ldots, g - 2\}$ and maps it to $r$ or $r + 1$. This map is a bijection onto the $g - 1$ values other than $x$, so each of them has probability $(1 - p)/(g - 1)$. $\square$

**Theorem 1 (privacy).** $R$ is $\varepsilon$-LDP. If some seed has $H_s(u) \ne H_s(v)$, no smaller $\varepsilon$ holds for the pair $u, v$.

*Proof.* By Lemma 1, the ratio $\Pr[R(u) = (s, y)]/\Pr[R(v) = (s, y)]$ is one of $1$, $p(g - 1)/(1 - p)$ and its inverse. Since $1 - p = (g - 1)/(e + g - 1)$, we get $p(g - 1)/(1 - p) = e$. So the ratio is at most $e^{\varepsilon}$, and it equals $e^{\varepsilon}$ at $(s, H_s(u))$ for a seed with $H_s(u) \ne H_s(v)$. $\square$

**Lemma 2 (the support probability).** Fix a value $v$, and let $I_u = [H_s(v) = y]$ for the report $(s, y) = R(u)$. Then $\Pr[I_u = 1] = p$ if $u = v$, and $\Pr[I_u = 1] = q = 1/g$ if $u \ne v$.

*Proof.* If $u = v$, then $I_u = 1$ exactly when line L4 runs, which has probability $p$. If $u \ne v$, condition on $s$. When $H_s(u) = H_s(v)$, the probability of $y = H_s(v)$ is $p$. When $H_s(u) \ne H_s(v)$, it is $(1 - p)/(g - 1)$. By (1),

$$\Pr[I_u = 1] = \frac{p}{g} + \left(1 - \frac1g\right)\frac{1 - p}{g - 1} = \frac{p}{g} + \frac{1 - p}{g} = \frac1g. \qquad \square$$

**Theorem 2 (unbiased estimate).** Let $n$ clients send one independent report each, and let $n_v$ of them hold $v$. If $e > 1$, the estimate $\tilde c(v)$ of line L7 has $\mathbb E[\tilde c(v)] = n_v$ and

$$\mathrm{Var}[\tilde c(v)] = \frac{n_v\,p(1 - p) + (n - n_v)\,q(1 - q)}{(p - q)^2}.$$

*Proof.* Line L6 computes $C(v) = \sum_u I_u$, a sum of $n$ independent indicators. By Lemma 2, $\mathbb E[C(v)] = n_v p + (n - n_v) q = n_v(p - q) + nq$. Since $e > 1$, $p > q$. Line L7 is $\tilde c(v) = (C(v) - nq)/(p - q)$, so its mean is $n_v$. The variance of $C(v)$ is the sum of the variances $p(1 - p)$ and $q(1 - q)$ of the indicators, and the affine map divides it by $(p - q)^2$. $\square$

When $n_v$ is small against $n$, the variance is close to $\mathrm{Var}^* = n q(1 - q)/(p - q)^2$, the quantity that Wang, Blocki, Li and Jha minimize.

**Theorem 3 (the best range).** As a function of a real $g > 1$, $\mathrm{Var}^*$ is minimized at $g = e + 1$, where $\mathrm{Var}^* = n \cdot 4e/(e - 1)^2$. Over the integers $g \ge 2$, with $t = \lfloor e \rfloor$, the minimum is at $g = t + 2$ if $e^2 > t(t + 1)$ and at $g = t + 1$ otherwise.

*Proof.* Let $t = g - 1 > 0$. Then $p - q = \frac{e}{e + t} - \frac{1}{t + 1} = \frac{(e - 1)t}{(e + t)(t + 1)}$ and $q(1 - q) = \frac{t}{(t + 1)^2}$. So

$$\frac{\mathrm{Var}^*}{n} = \frac{t}{(t + 1)^2} \cdot \frac{(e + t)^2 (t + 1)^2}{(e - 1)^2 t^2} = \frac{(e + t)^2}{(e - 1)^2\,t} = \frac{1}{(e - 1)^2}\left(\frac{e^2}{t} + 2e + t\right).$$

The function $\phi(t) = e^2/t + t$ is strictly convex on $t > 0$, with $\phi'(t) = 1 - e^2/t^2$, which is zero at $t = e$. So the real minimum is at $g = e + 1$, and its value is $(2e)^2/((e - 1)^2 e) = 4e/(e - 1)^2$.

Over the integers, convexity puts the minimum at $t = \lfloor e \rfloor$ or $t = \lfloor e \rfloor + 1$. With $t_0 = \lfloor e \rfloor \ge 1$, $\phi(t_0) - \phi(t_0 + 1) = e^2/(t_0(t_0 + 1)) - 1$, which is positive exactly when $e^2 > t_0(t_0 + 1)$. $\square$

Theorem 1 gives the privacy of each client, Theorem 2 gives the correctness of the collector, and Theorem 3 justifies the choice of $g$ in the code. Property (1) holds exactly for the family of all functions used in the code; a family with only approximate collisions gives a small bias in Theorem 2. $\blacksquare$
