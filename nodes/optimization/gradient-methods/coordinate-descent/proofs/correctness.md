---
title: Randomized coordinate descent converges linearly under the PL condition and at the rate 2 n L_max R_0^2 / k for convex functions
proves: [correctness, convergence-rate]
status: full
---

**Assumptions.** $f : \mathbb{R}^n \to \mathbb{R}$ is differentiable and bounded below, with infimum $f^*$. It has coordinate-wise Lipschitz gradients: for each $i$ there is $L_i > 0$ with

$$\lvert\partial_i f(x + te_i) - \partial_i f(x)\rvert \le L_i\lvert t\rvert \qquad \text{for all } x \in \mathbb{R}^n,\ t \in \mathbb{R}.$$

Let $L_{\max} = \max_i L_i$. The method picks $i_k$ uniformly at random from $\{1, \dots, n\}$, independently of the past, and sets $x_{k+1} = x_k - \frac{1}{L_{i_k}}\partial_{i_k}f(x_k)e_{i_k}$. Write $\delta_k = f(x_k) - f^*$ and $\mathbb{E}_k$ for the expectation over $i_k$ given $x_k$.

**Lemma 1 (descent along one coordinate).** For each $x$ and $i$, with $x^+ = x - \frac{1}{L_i}\partial_i f(x)e_i$,

$$f(x^+) \le f(x) - \frac{1}{2L_i}\big(\partial_i f(x)\big)^2.$$

*Proof.* Let $\phi(t) = f(x + te_i)$. Then $\phi'(t) = \partial_i f(x + te_i)$ is $L_i$-Lipschitz, so $\phi(t) \le \phi(0) + t\phi'(0) + \frac{L_i}{2}t^2$, by the integral form $\phi(t) - \phi(0) - t\phi'(0) = \int_0^t(\phi'(s) - \phi'(0))\,ds$. Put $t = -\phi'(0)/L_i$. $\square$

For a quadratic $f(x) = \frac{1}{2}x^\top Qx - c^\top x$, $L_i = Q_{ii}$, $\phi$ is a parabola, and Lemma 1 holds with equality: the step $1/L_i$ is the exact minimization along the coordinate.

**Lemma 2 (expected decrease).** $\mathbb{E}_k f(x_{k+1}) \le f(x_k) - \frac{1}{2nL_{\max}}\lVert\nabla f(x_k)\rVert^2$. Also $f(x_{k+1}) \le f(x_k)$ for every choice of $i_k$.

*Proof.* Average Lemma 1 over the $n$ choices of $i$ and use $L_i \le L_{\max}$: $\frac{1}{n}\sum_i\frac{1}{2L_i}(\partial_i f)^2 \ge \frac{1}{2nL_{\max}}\sum_i(\partial_i f)^2$. The second claim is Lemma 1 for the chosen $i_k$. $\square$

**Theorem 1 (linear rate).** If $f$ satisfies the [Polyak-Łojasiewicz condition](/polyak-lojasiewicz-condition/) $\frac{1}{2}\lVert\nabla f(x)\rVert^2 \ge \mu(f(x) - f^*)$ for all $x$, with $\mu > 0$ (this holds when $f$ is $\mu$-strongly convex), then

$$\mathbb{E}\,\delta_k \le \Big(1 - \frac{\mu}{nL_{\max}}\Big)^k\delta_0.$$

*Proof.* Lemma 2 and the PL condition give $\mathbb{E}_k\delta_{k+1} \le \delta_k - \frac{\mu}{nL_{\max}}\delta_k$. Take the full expectation (the tower property of [conditional expectation](/conditional-expectation/)) and apply this $k$ times. Note that $\mu \le L_i$ for each $i$, so the factor lies in $[0, 1)$. $\blacksquare$

**Theorem 2 (convex).** Let $f$ be convex with a minimizer, and let the level set $\{x : f(x) \le f(x_0)\}$ have finite radius

$$R_0 = \max_{x:\,f(x) \le f(x_0)}\ \min_{x^* \in X^*}\lVert x - x^*\rVert,$$

where $X^*$ is the set of minimizers. Then for each $k \ge 1$, $\mathbb{E}\,\delta_k \le \dfrac{2nL_{\max}R_0^2}{k}$.

*Proof.* By Lemma 2, $f(x_k) \le f(x_0)$ for every sample path, so $x_k$ lies in the level set. Let $x^*$ be the minimizer closest to $x_k$. By convexity and the Cauchy-Schwarz inequality, $\delta_k \le \langle\nabla f(x_k), x_k - x^*\rangle \le R_0\lVert\nabla f(x_k)\rVert$. With Lemma 2, and $c = 2nL_{\max}R_0^2$,

$$\mathbb{E}_k\delta_{k+1} \le \delta_k - \frac{\delta_k^2}{c}.$$

Let $\varphi_k = \mathbb{E}\,\delta_k$. Take the full expectation and use $\mathbb{E}\,\delta_k^2 \ge \varphi_k^2$ ([Jensen's inequality](/jensens-inequality/)): $\varphi_{k+1} \le \varphi_k - \varphi_k^2/c$. In particular $\varphi_{k+1} \le \varphi_k$. If some $\varphi_j = 0$, then $\varphi_k = 0$ for $k \ge j$ and the claim holds. Otherwise, divide by $\varphi_k\varphi_{k+1} > 0$:

$$\frac{1}{\varphi_{k+1}} - \frac{1}{\varphi_k} \ge \frac{\varphi_k}{c\,\varphi_{k+1}} \ge \frac{1}{c}.$$

Sum from $0$ to $k - 1$: $1/\varphi_k \ge 1/\varphi_0 + k/c \ge k/c$. $\blacksquare$

**Comparison with gradient descent.** If $f$ has an $L_f$-Lipschitz gradient, then $L_i \le L_f$ for each $i$, so $L_{\max} \le L_f$. Under Theorem 1, $n$ steps of the randomized method contract the bound by $(1 - \mu/(nL_{\max}))^n \le e^{-\mu/L_{\max}}$, while one step of gradient descent with the step $1/L_f$ contracts it by $1 - \mu/L_f$. When one partial derivative costs about $1/n$ of a full gradient, the two methods do the same work, and the coordinate method gains when $L_{\max}$ is much smaller than $L_f$.

**Cyclic order.** Lemma 1 holds for each step of any order, so the cyclic method also decreases $f$ monotonically. The proofs above use that $i_k$ is independent of $x_k$, so they do not apply to it. Its known worst-case bounds are weaker (Beck and Tetruashvili 2013), and Sun and Ye (2021) give quadratics on which the cyclic order is slower than the random order by a factor of order $n^2$.

**Nonsmooth terms.** The proofs need a gradient. If $F = f + \sum_i h_i(x_i)$ with each $h_i$ convex, the coordinate step becomes a one-variable prox step, and rates of the same form hold for that composite case (Richtárik and Takáč 2014). If the nonsmooth part couples coordinates, the method can stop at a non-minimizer; the page gives the example $x^2 + y^2 + 2\lvert x - y\rvert$ at $(1, 1)$.
