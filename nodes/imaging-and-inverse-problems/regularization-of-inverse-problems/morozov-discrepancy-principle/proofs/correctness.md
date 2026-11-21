---
title: The discrepancy equation has one root, the safeguarded Newton search finds it, and the chosen Tikhonov solution converges
proves: [correctness, termination]
status: full
---

**Setting.** $A$ is a real $m \times n$ matrix with thin SVD $A = \sum_{i} s_i u_i v_i^T$, where $s_1 \ge \dots \ge s_r > 0$ are the positive singular values. The data are $y \in \mathbb{R}^m$, the noise level is $\delta > 0$ and $\tau \ge 1$ is fixed. For $\alpha > 0$ the Tikhonov solution is $x_\alpha = (A^TA + \alpha I)^{-1}A^Ty$. Line L1 computes $b_i = \langle u_i, y\rangle$ for $i \le r$ and $p^2 = \lVert y\rVert^2 - \sum_i b_i^2$, which is the squared norm of the part of $y$ outside the range of $A$, because $u_1, \dots, u_r$ is an orthonormal basis of the range.

**Claim 1 (the residual as a function of alpha).** For $\alpha > 0$,

$$x_\alpha = \sum_{i=1}^r \frac{s_i b_i}{s_i^2 + \alpha} v_i, \qquad \rho(\alpha) := \lVert Ax_\alpha - y\rVert^2 = \sum_{i=1}^r \Big(\frac{\alpha}{s_i^2 + \alpha}\Big)^2 b_i^2 + p^2.$$

The function $\rho$ is continuous and nondecreasing on $(0, \infty)$, with $\rho(\alpha) \to p^2$ as $\alpha \to 0$ and $\rho(\alpha) \to \lVert y\rVert^2$ as $\alpha \to \infty$. If some $b_i \ne 0$, it is strictly increasing.

*Proof.* In the basis $v_i$ the normal equations $(A^TA + \alpha I)x = A^Ty$ are diagonal: the coefficient of $v_i$ satisfies $(s_i^2 + \alpha)\xi_i = s_i b_i$ for $i \le r$, and $\alpha \xi = 0$ on the null space of $A$. This gives $x_\alpha$. Then $Ax_\alpha - y = \sum_{i \le r} (s_i^2/(s_i^2 + \alpha) - 1) b_i u_i - P^\perp y$, where $P^\perp y$ is orthogonal to every $u_i$ and has norm $p$. Since $s_i^2/(s_i^2+\alpha) - 1 = -\alpha/(s_i^2 + \alpha)$, Pythagoras gives $\rho$. Each factor $g_i(\alpha) = \alpha/(s_i^2 + \alpha)$ is continuous and strictly increasing, with $g_i' = s_i^2/(s_i^2+\alpha)^2 > 0$, from $0$ at $\alpha \to 0$ to $1$ at $\alpha \to \infty$. The limits follow from $\sum_i b_i^2 + p^2 = \lVert y\rVert^2$. $\square$

With $t = \log\alpha$ let $F(t) = \rho(e^t) - \tau^2\delta^2$ (line L4). By the chain rule, with $\alpha = e^t$,

$$F'(t) = \alpha\rho'(\alpha) = 2\sum_{i=1}^r \frac{\alpha^2 s_i^2 b_i^2}{(s_i^2 + \alpha)^3}.$$

**Claim 2 (the special cases of lines L2 and L3).** If $p \ge \tau\delta$, no $\alpha > 0$ has $\lVert Ax_\alpha - y\rVert \le \tau\delta$ unless $p = \tau\delta$ and all $b_i = 0$, and then no $\alpha$ is singled out. If $\lVert y\rVert \le \tau\delta$, the vector $x = 0$ already has residual $\lVert y\rVert \le \tau\delta$. If $y = Ax^\dagger + e$ with $\lVert e\rVert \le \delta$ and $\tau > 1$, line L2 never fails.

*Proof.* By Claim 1, $\rho(\alpha) \ge p^2$, with equality only if all $b_i = 0$. The case $\lVert y\rVert \le \tau\delta$ is clear. Under the noise model $Ax^\dagger$ lies in the range of $A$, so $P^\perp y = P^\perp e$ and $p \le \lVert e\rVert \le \delta < \tau\delta$. $\square$

From here on assume $p < \tau\delta < \lVert y\rVert$. Then $\sum_i b_i^2 = \lVert y\rVert^2 - p^2 > 0$, so $F$ is strictly increasing and, by Claim 1 and the intermediate value theorem, has exactly one root $t^\ast$. The value $\alpha^\ast = e^{t^\ast}$ is the unique solution of $\lVert Ax_\alpha - y\rVert = \tau\delta$.

**Claim 3 (the starting bracket of lines L5 and L6).** $F(\mathrm{lo}) < 0 < F(\mathrm{hi})$.

*Proof.* Upper end. Let $q = (1 + \tau\delta/\lVert y\rVert)/2$. Then $\tau\delta/\lVert y\rVert < q < 1$. Line L5 sets $\alpha_{hi} = s_1^2 q/(1-q)$, so $\alpha_{hi}/(s_1^2 + \alpha_{hi}) = q$. For every $i$, $s_i \le s_1$ gives $\alpha_{hi}/(s_i^2 + \alpha_{hi}) \ge q$, and $q < 1$ gives $p^2 \ge q^2p^2$. So $\rho(\alpha_{hi}) \ge q^2(\sum_i b_i^2 + p^2) = q^2\lVert y\rVert^2 > \tau^2\delta^2$.

Lower end. Line L6 sets $\alpha_{lo} = s_r^2 \sqrt{(\tau^2\delta^2 - p^2)/2}/\lVert y\rVert$. For every $i$, $\alpha/(s_i^2 + \alpha) \le \alpha/s_r^2$, so $\rho(\alpha_{lo}) \le (\alpha_{lo}/s_r^2)^2 \sum_i b_i^2 + p^2 \le (\tau^2\delta^2 - p^2)/2 + p^2 < \tau^2\delta^2$, because $p^2 < \tau^2\delta^2$. $\square$

**Claim 4 (loop invariant).** At the start of each pass of the loop L7 to L11, $F(\mathrm{lo}) \le 0 < F(\mathrm{hi})$ and $t^\ast \in [\mathrm{lo}, \mathrm{hi}]$.

*Proof.* It holds at the start by Claim 3. Line L10 always gives a point $t$ with $\mathrm{lo} < t < \mathrm{hi}$: the Newton point is kept only if it is inside the open bracket, and the midpoint is inside. Line L11 replaces $\mathrm{hi}$ by $t$ if $F(t) > 0$ and $\mathrm{lo}$ by $t$ otherwise, so the signs stay. Since $F$ is increasing, $F(\mathrm{lo}) \le 0 = F(t^\ast) < F(\mathrm{hi})$ puts $t^\ast$ in $[\mathrm{lo}, \mathrm{hi}]$. $\square$

**Claim 5 (termination).** Let $W$ be the width of the starting bracket. The loop makes at most $2\lceil \log_2(W/\varepsilon)\rceil$ passes.

*Proof.* Every pass replaces one end by a point inside the bracket, so the width never grows. On even passes line L10 takes the midpoint, so the width at least halves. After $2j$ passes the width is at most $W/2^j$, and the test of line L9 stops the loop once the width is at most $\varepsilon$, which happens for $j = \lceil\log_2(W/\varepsilon)\rceil$. $\square$

**Claim 6 (accuracy).** On exit, $c$ is an end of the bracket and $|\lVert Ax_\alpha - y\rVert^2 - \tau^2\delta^2| \le \frac{8}{27}\lVert y\rVert^2\varepsilon$ for $\alpha = e^c$. The returned $x$ is $x_\alpha$.

*Proof.* Write $w_i = \alpha/(s_i^2 + \alpha) \in (0,1)$. Then $\alpha^2 s_i^2/(s_i^2+\alpha)^3 = w_i^2(1 - w_i) \le 4/27$, the maximum of $w^2(1-w)$ on $[0,1]$, at $w = 2/3$. So $0 \le F'(t) \le \frac{8}{27}\sum_i b_i^2 \le \frac{8}{27}\lVert y\rVert^2$ for every $t$. Line L9 exits in one of two cases. If $\mathrm{hi} - \mathrm{lo} \le \varepsilon$, then $|c - t^\ast| \le \varepsilon$ by Claim 4, and the mean value theorem gives $|F(c)| = |F(c) - F(t^\ast)| \le \frac{8}{27}\lVert y\rVert^2\varepsilon$. Otherwise $|F(c)| \le \varepsilon F'(c) \le \frac{8}{27}\lVert y\rVert^2\varepsilon$. In both cases $|F(c)|$ is the stated quantity. Line L13 evaluates the formula of Claim 1. $\square$

So the algorithm is correct: it returns FAIL exactly when the target is out of reach, the zero solution when the data are within $\tau\delta$ of zero, and otherwise the Tikhonov solution for an $\alpha$ that solves the discrepancy equation to the stated accuracy, after a bounded number of steps.

**Theorem (the discrepancy principle gives a convergent regularization method).** Let $A$ be a bounded linear operator between Hilbert spaces, $y = Ax^\dagger$ with $x^\dagger$ the minimum norm solution, $\lVert y^\delta - y\rVert \le \delta$ and $\tau \ge 1$. Let $\alpha = \alpha(\delta, y^\delta)$ satisfy $\lVert Ax_\alpha^\delta - y^\delta\rVert = \tau\delta$, where $x^\delta_\alpha$ is the Tikhonov solution for the data $y^\delta$. Then:

1. $\lVert x_\alpha^\delta\rVert \le \lVert x^\dagger\rVert$ and $\lVert Ax_\alpha^\delta - y\rVert \le (1 + \tau)\delta$;
2. $x^\delta_\alpha \to x^\dagger$ as $\delta \to 0$;
3. if $x^\dagger = A^\ast w$, then $\lVert x_\alpha^\delta - x^\dagger\rVert \le \sqrt{2(1 + \tau)\lVert w\rVert\,\delta}$.

*Proof.* 1. The Tikhonov solution minimizes $J(x) = \lVert Ax - y^\delta\rVert^2 + \alpha\lVert x\rVert^2$, so $J(x_\alpha^\delta) \le J(x^\dagger) = \lVert y - y^\delta\rVert^2 + \alpha\lVert x^\dagger\rVert^2 \le \delta^2 + \alpha\lVert x^\dagger\rVert^2$. The left side is $\tau^2\delta^2 + \alpha\lVert x_\alpha^\delta\rVert^2$. Since $\tau \ge 1$, $\alpha\lVert x_\alpha^\delta\rVert^2 \le \alpha\lVert x^\dagger\rVert^2 - (\tau^2 - 1)\delta^2 \le \alpha\lVert x^\dagger\rVert^2$. The second bound is the triangle inequality: $\lVert Ax_\alpha^\delta - y\rVert \le \lVert Ax_\alpha^\delta - y^\delta\rVert + \lVert y^\delta - y\rVert$.

2. By part 1, for every $\delta$,
$$\lVert x_\alpha^\delta - x^\dagger\rVert^2 = \lVert x_\alpha^\delta\rVert^2 - 2\langle x_\alpha^\delta, x^\dagger\rangle + \lVert x^\dagger\rVert^2 \le 2\langle x^\dagger - x_\alpha^\delta, x^\dagger\rangle. \tag{$\ast$}$$
Take $\delta_k \to 0$ and write $x_k$ for the chosen solutions. They are bounded by $\lVert x^\dagger\rVert$, so every subsequence has a further subsequence that converges weakly to some $\bar x$. Since $A$ is bounded, $Ax_k \rightharpoonup A\bar x$, and $Ax_k \to y$ by part 1, so $A\bar x = y$. The norm is weakly lower semicontinuous, so $\lVert\bar x\rVert \le \lVert x^\dagger\rVert$. The minimum norm solution is unique, so $\bar x = x^\dagger$. Then the right side of $(\ast)$ tends to $0$ along that subsequence. Every subsequence has a further subsequence along which $x_k \to x^\dagger$, so the whole sequence converges.

3. In $(\ast)$, $\langle x^\dagger - x_\alpha^\delta, A^\ast w\rangle = \langle Ax^\dagger - Ax_\alpha^\delta, w\rangle \le (1 + \tau)\delta\lVert w\rVert$ by part 1. $\blacksquare$
