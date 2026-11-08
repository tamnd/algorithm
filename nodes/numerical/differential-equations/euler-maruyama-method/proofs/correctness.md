---
title: The Euler-Maruyama method converges with strong order 1/2 under global Lipschitz conditions
proves: [correctness, termination, convergence]
status: full
---

**Setting.** $\|\cdot\|$ is the Euclidean norm on $\mathbb{R}^d$ and the Frobenius norm on $\mathbb{R}^{d \times m}$. $W$ is an $m$-dimensional Brownian motion on $[t_0, T]$ with its filtration, and $X_0$ is independent of $W$ with $E\|X_0\|^2 < \infty$. First take $a$ and $b$ independent of $t$ (the autonomous case) and globally Lipschitz: $\|a(x) - a(y)\| + \|b(x) - b(y)\| \le K\|x - y\|$. Then $\|a(x)\|^2 + \|b(x)\|^2 \le K_1(1 + \|x\|^2)$ with $K_1 = 2\max(2K^2, \|a(0)\|^2 + \|b(0)\|^2)$. Under these conditions the equation has a unique strong solution with $\sup_{t \le T}E\|X(t)\|^2 < \infty$ (Kloeden and Platen 1992, Section 4.5). We write $h = \max_n(t_{n+1} - t_n)$. Time-dependent coefficients that are Lipschitz in $(t, x)$ reduce to this case by adding $t$ as a component of the state with drift 1 and diffusion 0; Euler-Maruyama treats that component exactly.

**Lemma 1 (the loop).** After iteration $n$ of lines L3 to L8, $t = t_{n+1}$ and $X = X_{n+1} = X_n + a(X_n)\Delta t_n + b(X_n)\Delta W_n$, where $t_m = t_0 + mh$ for $m < N$, $t_N = T$, and $\Delta W_0, \ldots, \Delta W_{N-1}$ are independent with $\Delta W_n \sim N(0, \Delta t_nI_m)$, $\Delta t_n = t_{n+1} - t_n$. The algorithm stops after $N$ iterations.

*Proof.* Induction on $n$, exactly as for Euler's method: line L4 gives $t_{n+1}$, line L5 its distance to $t_n$, line L6 an increment independent of the earlier ones with the stated law, and line L7 the update. The loop of line L3 runs $N$ times. If the increments are taken from a path $W$, $\Delta W_n = W(t_{n+1}) - W(t_n)$, which has the same joint law by the independent increments of Brownian motion. $\square$

**Lemma 2 (continuous extension).** Let $\bar X(s) = X_n$ for $s \in [t_n, t_{n+1})$, and define

$$\tilde X(t) = X_0 + \int_{t_0}^{t}a(\bar X(s))\,ds + \int_{t_0}^{t}b(\bar X(s))\,dW(s).$$

Then $\tilde X(t_n) = X_n$ for every $n$, and $\sup_n E\|X_n\|^2 < \infty$.

*Proof.* On $[t_n, t_{n+1}]$ the integrands are constant, equal to $a(X_n)$ and $b(X_n)$, so the integrals over that interval are $a(X_n)\Delta t_n$ and $b(X_n)\Delta W_n$; summing over the intervals gives $\tilde X(t_n) = X_n$ by Lemma 1. For the moments, $X_n$ is independent of $\Delta W_n$, so $E\|X_{n+1}\|^2 = E\|X_n + a(X_n)\Delta t_n\|^2 + \Delta t_nE\|b(X_n)\|^2 \le (1 + h)E\|X_n\|^2 + (2h + h^2)K_1(1 + E\|X_n\|^2)$, using $\|u + v\|^2 \le (1 + h)\|u\|^2 + (1 + 1/h)\|v\|^2$ with $v = a(X_n)\Delta t_n$, $\Delta t_n \le h \le 1$, and the linear growth bound. A finite number of steps of a linear recurrence keeps the bound finite. $\square$

**Lemma 3 (increments of the exact solution).** Let $B = \sup_{t \le T}E\|X(t)\|^2$. For $t_0 \le r \le s \le T$ with $s - r \le 1$, $E\|X(s) - X(r)\|^2 \le C_1(s - r)$ with $C_1 = 2K_1(1 + B)$.

*Proof.* $X(s) - X(r) = \int_r^sa(X)\,du + \int_r^sb(X)\,dW$. By $\|u + v\|^2 \le 2\|u\|^2 + 2\|v\|^2$, the Cauchy-Schwarz inequality for the first integral and the Itô isometry for the second,

$$E\|X(s) - X(r)\|^2 \le 2(s - r)\int_r^sE\|a(X(u))\|^2du + 2\int_r^sE\|b(X(u))\|^2du \le 2K_1(1 + B)\big((s - r)^2 + (s - r)\big),$$

and $(s - r)^2 \le s - r$. $\square$

**Theorem (strong order 1/2).** For $h \le 1$, $\sup_{t_0 \le t \le T}E\|X(t) - \tilde X(t)\|^2 \le C_2h$ with $C_2 = 4(T - t_0 + 1)K^2C_1(T - t_0)e^{4(T - t_0 + 1)K^2(T - t_0)}$. In particular $\max_n(E\|X(t_n) - X_n\|^2)^{1/2} \le \sqrt{C_2}\,h^{1/2}$.

*Proof.* Let $e(t) = X(t) - \tilde X(t)$ and $z(t) = \sup_{t_0 \le r \le t}E\|e(r)\|^2$, which is finite by Lemma 2 and the moment bound on $X$. Since

$$e(t) = \int_{t_0}^{t}\big(a(X(s)) - a(\bar X(s))\big)ds + \int_{t_0}^{t}\big(b(X(s)) - b(\bar X(s))\big)dW(s),$$

the same three tools as in Lemma 3 give

$$E\|e(t)\|^2 \le 2(T - t_0)K^2\int_{t_0}^{t}E\|X(s) - \bar X(s)\|^2ds + 2K^2\int_{t_0}^{t}E\|X(s) - \bar X(s)\|^2ds.$$

For $s \in [t_n, t_{n+1})$, $X(s) - \bar X(s) = (X(s) - X(t_n)) + e(t_n)$, because $\bar X(s) = X_n = \tilde X(t_n)$. By Lemma 3, $E\|X(s) - \bar X(s)\|^2 \le 2C_1h + 2E\|e(t_n)\|^2 \le 2C_1h + 2z(s)$. Hence, with $c = 2(T - t_0 + 1)K^2$,

$$E\|e(t)\|^2 \le c\Big(2C_1h(T - t_0) + 2\int_{t_0}^{t}z(s)\,ds\Big).$$

The right side increases in $t$, so the same bound holds for $z(t)$. The integral form of the [Gronwall inequality](/gronwall-inequality/) for the nondecreasing function $z$ gives $z(t) \le 2cC_1(T - t_0)h\,e^{2c(t - t_0)}$, which is the claim. At $t = t_n$, $\tilde X(t_n) = X_n$ by Lemma 2. $\square$

**Sharpness.** The exponent $\tfrac12$ cannot be improved in general. For $dX = X\,dW$, $X(0) = 1$, $d = m = 1$, the mean-square error after one step from the exact value is $E\big(X(h) - 1 - \Delta W\big)^2$ with $X(h) = e^{\Delta W - h/2}$; expanding, $X(h) - 1 - \Delta W = \tfrac12(\Delta W^2 - h) + O(h^{3/2})$ in mean square, whose second moment is $\tfrac14E(\Delta W^2 - h)^2 = \tfrac12h^2$. These local errors have mean zero and are uncorrelated across steps to leading order, so after $N = (T - t_0)/h$ steps they add up to a mean-square error of order $Nh^2 = (T - t_0)h$: root mean square order $\tfrac12$, matching the theorem. The term $\tfrac12(\Delta W^2 - h)$ is exactly what the Milstein method adds. $\blacksquare$
