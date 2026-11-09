---
title: Kelley's method keeps certified bounds L <= f* <= U and stops after at most (1 + G D sqrt(n)/eps)^n oracle calls
proves: [correctness, termination, iteration-bound]
status: full
---

The problem is $\min f(x)$ over the box $X = \{x \in \mathbb{R}^n : l \le x \le u\}$. At step $j = 0, 1, \ldots$ the method calls the oracle at $x_j \in X$, which returns $f(x_j)$ and some $g_j \in \partial f(x_j)$. It sets $U_j = \min_{i \le j} f(x_i)$, and it lets $(x_{j+1}, L_j)$ be a minimizer of $t$ over $\{(x, t) : x \in X,\ t \ge f(x_i) + g_i^\top(x - x_i) \text{ for } i \le j\}$. It stops at the first $j$ with $U_j - L_j \le \varepsilon$. We assume:

- (A1) $f: \mathbb{R}^n \to \mathbb{R}$ is convex, and $x_0 \in X$;
- (A2) each subgradient the oracle returns has $\|g_j\| \le G$ (Euclidean norm);
- (A3) each side of the box is at most $D$: $u_i - l_i \le D$.

Write $m_j(x) = \max_{i \le j}\big(f(x_i) + g_i^\top(x - x_i)\big)$ for the model after step $j$, and $f^* = \min_X f$, which exists because $f$ is continuous and $X$ is compact.

**Lemma 1 (the linear program has a solution).** For each $j$, the linear program of line L6 has an optimal solution, and $L_j = \min_X m_j$.

*Proof.* The function $m_j$ is a maximum of finitely many affine functions, so it is continuous, and on the compact set $X$ it attains its minimum. A point $(x, t)$ is feasible exactly when $x \in X$ and $t \ge m_j(x)$, so the least $t$ is $\min_X m_j$. $\square$

**Lemma 2 (certified bounds).** For each $j$, $L_j \le f^* \le U_j$. Also $L_j$ does not decrease and $U_j$ does not increase with $j$.

*Proof.* By the subgradient inequality, $f(x) \ge f(x_i) + g_i^\top(x - x_i)$ for all $x$ and $i$, so $m_j \le f$ everywhere, and $L_j = \min_X m_j \le \min_X f = f^*$. Each $x_i$ lies in $X$, so $U_j$ is a value of $f$ on $X$, and $f^* \le U_j$. The model $m_{j+1}$ is the maximum of $m_j$ and one more affine function, so $m_{j+1} \ge m_j$ and $L_{j+1} \ge L_j$. $U_{j+1} \le U_j$ by its definition as a running minimum. $\square$

So when the method stops, the point $x_{\text{best}}$ with $f(x_{\text{best}}) = U_j$ satisfies $f(x_{\text{best}}) - f^* \le U_j - L_j \le \varepsilon$.

**Lemma 3 (new points are far from old ones).** For all $i \le j$,

$$U_j - L_j \le f(x_i) - L_j \le -g_i^\top(x_{j+1} - x_i) \le G\,\|x_{j+1} - x_i\|.$$

*Proof.* The first inequality holds because $U_j \le f(x_i)$. The point $(x_{j+1}, L_j)$ satisfies the cut of step $i$: $L_j \ge f(x_i) + g_i^\top(x_{j+1} - x_i)$. The last inequality is the Cauchy-Schwarz inequality with (A2). $\square$

**Theorem 1 (iteration bound).** Let $\varepsilon > 0$ and $N = \big(1 + GD\sqrt{n}/\varepsilon\big)^n$. The method stops at some $j \le N - 2$, so it makes at most $N - 1$ oracle calls.

*Proof.* Suppose the method has not stopped at steps $0, \ldots, k$, so $U_j - L_j > \varepsilon$ for each $j \le k$. By Lemma 3, $\|x_{j+1} - x_i\| > \varepsilon/G$ for all $i \le j \le k$. So the $k + 2$ points $x_0, \ldots, x_{k+1}$ of $X$ have pairwise Euclidean distances greater than $\delta = \varepsilon/G$. Then their pairwise distances in the maximum norm are greater than $\delta/\sqrt{n}$, so the open cubes of side $\delta/\sqrt{n}$ centered at them do not meet. These cubes lie in the box $X$ enlarged by $\delta/(2\sqrt{n})$ on each side, whose volume is at most $(D + \delta/\sqrt{n})^n$. Comparing volumes,

$$k + 2 \le \frac{(D + \delta/\sqrt{n})^n}{(\delta/\sqrt{n})^n} = \Big(1 + \frac{GD\sqrt{n}}{\varepsilon}\Big)^n = N.$$

So the method cannot run past step $N - 2$ without stopping. $\square$

**Theorem 2 (finite termination for polyhedral functions).** Let $f(x) = \max_{1 \le p \le P}(a_p^\top x + b_p)$, and let the oracle return $g_j = a_p$ for a piece $p$ with $f(x_j) = a_p^\top x_j + b_p$. With $\varepsilon = 0$, the method stops after at most $P + 1$ oracle calls, with $U_j = L_j = f^*$.

*Proof.* The cut of step $i$ is the affine function $a_p^\top x + b_p$ itself. Suppose the method has not stopped at step $j$, and let $p$ be the piece returned at $x_{j+1}$. If the cut of $p$ is already in the model, then $f(x_{j+1}) = a_p^\top x_{j+1} + b_p \le m_j(x_{j+1}) = L_j$, so $U_{j+1} \le L_j \le L_{j+1}$, and with Lemma 2 the method stops at step $j + 1$ with $U = L = f^*$. Otherwise step $j + 1$ adds a new piece. At most $P$ steps add a new piece, so the method stops after at most $P + 1$ oracle calls. $\blacksquare$
