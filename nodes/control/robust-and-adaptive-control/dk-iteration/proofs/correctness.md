---
title: The K-step and D-step of D-K iteration each lower the scaled bound, up to the back off
proves: [correctness]
status: full
---

Notation is that of the page. The plant is in the normalized form of the two-Riccati page. The uncertainty block uses the first $n_z$ outputs $z_1$ and the first $n_w$ inputs $w_1$, and the rows of $D_{12}$ for $z_1$ and the columns of $D_{21}$ for $w_1$ are zero. For $d > 0$ put $D_z = \mathrm{diag}(d I_{n_z}, I)$ and $D_w = \mathrm{diag}(d I_{n_w}, I)$, and $J(K, d) = \|D_z\,\mathcal{F}_l(P, K)\,D_w^{-1}\|_\infty$. Two results are cited: the two-Riccati theorem (Doyle, Glover, Khargonekar and Francis 1989), with the bisection proof of its page, and the convexity theorem of Sezginer and Overton (1990).

## Claim 1: scaling the plant scales the closed loop

*Let $P_d$ have $C_1^d = D_z C_1$, $D_{12}^d = D_z D_{12}$, $B_1^d = B_1 D_w^{-1}$ and $D_{21}^d = D_{21} D_w^{-1}$, with $A$, $B_2$ and $C_2$ unchanged. Then for every controller $K$, $\mathcal{F}_l(P_d, K) = D_z\,\mathcal{F}_l(P, K)\,D_w^{-1}$. If $P$ is normalized, so is $P_d$.*

*Proof.* The closed loop of $P$ with $K = (A_K, B_K, C_K, D_K)$ has

$$A_{\rm cl} = \begin{bmatrix} A + B_2 D_K C_2 & B_2 C_K \\ B_K C_2 & A_K \end{bmatrix}, \quad B_{\rm cl} = \begin{bmatrix} B_1 + B_2 D_K D_{21} \\ B_K D_{21} \end{bmatrix}, \quad C_{\rm cl} = [C_1 + D_{12} D_K C_2 \ \ D_{12} C_K], \quad D_{\rm cl} = D_{12} D_K D_{21}.$$

$A_{\rm cl}$ uses only $A$, $B_2$, $C_2$ and $K$, so it does not change. Every term of $B_{\rm cl}$ and $D_{\rm cl}$ ends in $B_1$ or $D_{21}$, so in $P_d$ it is multiplied by $D_w^{-1}$ on the right. Every term of $C_{\rm cl}$ and $D_{\rm cl}$ starts with $C_1$ or $D_{12}$, so it is multiplied by $D_z$ on the left. Hence the transfer function $C_{\rm cl}(sI - A_{\rm cl})^{-1} B_{\rm cl} + D_{\rm cl}$ becomes $D_z(\cdot)D_w^{-1}$.

For the normal form: $D_{12}^{dT} D_{12}^d = D_{12}^T D_z^2 D_{12} = D_{12}^T D_{12}$, because the rows of $D_{12}$ that $D_z$ scales are zero. In the same way $D_{12}^{dT} C_1^d = D_{12}^T C_1 = 0$, $D_{21}^d D_{21}^{dT} = D_{21} D_{21}^T$ and $B_1^d D_{21}^{dT} = B_1 D_w^{-2} D_{21}^T = B_1 D_{21}^T = 0$, since the columns of $D_{21}$ that $D_w$ scales are zero. The stabilizability and detectability assumptions with $B_2$ and $C_2$ do not change. For $(A, B_1^d)$ and $(C_1^d, A)$, the scaling by an invertible matrix changes neither the controllable nor the observable subspace. $\square$

So the K-step at scale $d$ solves $\min_K J(K, d)$, up to the bisection and the back off: with $\gamma_d = \gamma_{\rm opt}(P_d)$, every stabilizing $K$ has $J(K, d) \ge \gamma_d$, and the central controller at level $\gamma$ with $\gamma > \gamma_d$ has $J(K, d) < \gamma$.

## Claim 2: the D-step function is convex in log d

*For any finite set of complex matrices $M_1, \ldots, M_f$ of size $p \times m$, the function $\phi(t) = \max_i \bar\sigma(D_z(e^t) M_i D_w(e^t)^{-1})$ is convex on $\mathbb{R}$.*

*Proof.* Embed $M_i$ in the square matrix $N_i = \begin{bmatrix} 0 & M_i \\ 0 & 0 \end{bmatrix}$ of size $p + m$, and let $E = \mathrm{diag}(E_z, E_w)$ with $E_z = \mathrm{diag}(I_{n_z}, 0)$ and $E_w = \mathrm{diag}(I_{n_w}, 0)$. Then $e^{tE} N_i e^{-tE} = \begin{bmatrix} 0 & D_z M_i D_w^{-1} \\ 0 & 0 \end{bmatrix}$, which has the same largest singular value as $D_z M_i D_w^{-1}$. The matrices $tE$ for $t \in \mathbb{R}$ are diagonal, so they commute and form a convex set. By the theorem of Sezginer and Overton (1990), $t \mapsto \bar\sigma(e^{tE} N_i e^{-tE})$ is convex. The pointwise maximum of finitely many convex functions is convex. $\square$

## Claim 3: golden section search finds the minimum of a convex function

*Let $\phi$ be convex and continuous on $[a, b]$. Golden section search keeps an interval that contains a minimizer of $\phi$ on $[a, b]$, and the interval shrinks by the factor $r = (\sqrt5 - 1)/2$ at each step.*

*Proof.* Let $a < x_1 < x_2 < b$ be the two inner points, and let $\phi(x_1) \le \phi(x_2)$. Take any $x \in (x_2, b]$ and write $x_2 = \lambda x_1 + (1 - \lambda) x$ with $\lambda \in (0, 1)$. Convexity gives $\phi(x_2) \le \lambda \phi(x_1) + (1 - \lambda) \phi(x)$. If $\phi(x) < \phi(x_2)$, the right side is below $\lambda \phi(x_2) + (1 - \lambda) \phi(x_2) = \phi(x_2)$, which is impossible. So $\phi(x) \ge \phi(x_2) \ge \phi(x_1)$ for every $x > x_2$, and a minimizer on $[a, b]$ lies in $[a, x_2]$, which the code keeps. The other case is symmetric. The choice $x_1 = b - r(b - a)$, $x_2 = a + r(b - a)$ with $r^2 = 1 - r$ makes the kept inner point one of the new inner points, so the new interval has length $r(b - a)$. $\square$

If the minimizer of $\phi$ on $\mathbb{R}$ lies outside $[-8, 8]$, the search returns the best point of the interval, near an end. The page lists this as a pitfall.

## Claim 4: descent up to the back off

*Use the true norm in place of the grid maximum, and exact arithmetic. Let pass $k$ end with $(K_k, d_k)$ and $v_k = J(K_k, d_k) = \min_d J(K_k, d)$. Let the next K-step use the level $\gamma = (1 + \delta)\,h$ with $\gamma_{d_k} \le h \le (1 + \epsilon)\,\gamma_{d_k}$ from the bisection. Then $\gamma_{d_k} \le v_k$ and $v_{k+1} < (1 + \delta)(1 + \epsilon)\,v_k$.*

*Proof.* $K_k$ stabilizes the plant, so by Claim 1 it is one candidate for $\min_K J(K, d_k)$, and $\gamma_{d_k} \le J(K_k, d_k) = v_k$. The central controller $K_{k+1}$ at level $\gamma > \gamma_{d_k}$ has $J(K_{k+1}, d_k) < \gamma \le (1 + \delta)(1 + \epsilon)\,\gamma_{d_k}$. The D-step minimizes $J(K_{k+1}, \cdot)$, so $v_{k+1} \le J(K_{k+1}, d_k)$. Put the three bounds together. $\square$

With $\delta = \epsilon = 0$ in the limit, the sequence $v_k$ is nonincreasing and bounded below by 0, so it converges. Nothing in the proof says that the limit is the minimum of $J$ over $(K, d)$; a point where neither step improves can be a local optimum of a nonconvex function.

## Claim 5: the K-step optimum of the example at d = sqrt 2 is 3

*For the example plant with $d = \sqrt 2$, $\gamma_{\rm opt}(P_d) = 3$.*

*Proof.* The scaled plant has $B_1^d = [1/\sqrt 2, 1, 0]$ and $C_1^d = [1/\sqrt 2; 1; 0]$, so $B_1^d B_1^{dT} = C_1^{dT} C_1^d = 3/2$, and $B_2 = C_2 = 1$, $A = 1$. Both Riccati equations are $(1.5\,\gamma^{-2} - 1) X^2 + 2X + 1.5 = 0$, so $Y = X$. For $\gamma^2 > 1.5$ put $c = 1 - 1.5\,\gamma^{-2} > 0$. The stabilizing root is $X = (1 + \sqrt{1 + 1.5c})/c > 0$, since then $A + RX = 1 - cX = -\sqrt{1 + 1.5c} < 0$. The coupling condition is $X^2 < \gamma^2$, that is $X < \gamma$. Now $X(\gamma)$ decreases as $\gamma$ grows, because $c$ grows and $X$ is decreasing in $c$, while $\gamma$ grows. At $\gamma = 3$: $c = 5/6$ and $X = (1 + \sqrt{2.25}) \cdot 6/5 = 3$, so $X = \gamma$. So the conditions hold exactly for $\gamma > 3$. For $\gamma^2 \le 1.5$ the first condition fails, since then the Riccati equation has no stabilizing solution with $X \ge 0$: with $c \le 0$ the closed loop $1 - cX \ge 1$ for $X \ge 0$. $\square$

## What the tests check

- Claim 1 numerically: the frequency response of the scaled loop equals $D_z M D_w^{-1}$ entry by entry at three frequencies and three values of $d$, and the scaled plant keeps $D_{12}^T C_1 = 0$ and $B_1 D_{21}^T = 0$.
- Claim 5: the bisection gives $\gamma_{\rm opt}(P_{\sqrt 2}) = 3$ within $10^{-8}$, and $\gamma_{\rm opt}(P_d) = \gamma_{\rm opt}(P_{2/d}) > 3$ for three other values of $d$.
- Claims 2 and 3 against brute force: for two plants, the golden section result is at least as good as each of 31 values of $\log d$ in $[-3, 3]$, and the sampled function satisfies the midpoint convexity inequality.
- Claim 4: along the iteration for two plants, $\gamma_{d_k} \le v_k$ and $v_{k+1} \le 1.02\,v_k$ (with a relative slack of $10^{-3}$ for the grid), and each $v_k$ lies between the K-step optimum and $1.02$ times it.
- The final controller gives a Hurwitz closed loop, and its scaled bound is at most the unscaled peak of the plain H-infinity controller.
- The example values on the page: $d = \sqrt 2$, the first K-step optimum $3.06155$ and the last one $3$.
