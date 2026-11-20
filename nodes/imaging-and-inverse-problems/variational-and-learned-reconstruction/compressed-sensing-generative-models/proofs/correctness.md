---
title: "Under the set-restricted eigenvalue condition, any near minimizer of the CSGM loss is close to the signal, and the gradient steps use the exact gradient"
proves: [correctness]
status: partial
---

**Setting.** $A \in \mathbb{R}^{m \times n}$, a generator $G : \mathbb{R}^k \to \mathbb{R}^n$, a radius $r > 0$ and the set $S = G(B^k(r))$, where $B^k(r)$ is the ball of radius $r$ in $\mathbb{R}^k$. The data are $y = Ax^* + \eta$ for an unknown signal $x^* \in \mathbb{R}^n$ and noise $\eta$. The signal need not lie in $S$.

The status is partial: the deterministic error bound and the gradient are proved here; the statement that Gaussian matrices satisfy the condition with high probability is cited from Bora, Jalal, Price and Dimakis (2017, Lemmas 4.1 and 4.2), not proved. Nothing here says that gradient descent finds a near minimizer: the loss is not convex in $z$, and the tests show a start that ends at a spurious stationary point.

**Definition (S-REC).** For $\gamma > 0$ and $\delta \ge 0$, the matrix $A$ satisfies $\text{S-REC}(S, \gamma, \delta)$ if $\|A(x_1 - x_2)\| \ge \gamma\|x_1 - x_2\| - \delta$ for all $x_1, x_2 \in S$.

**Theorem (deterministic part of Bora et al., Lemma 4.3).** Suppose $A$ satisfies $\text{S-REC}(S, \gamma, \delta)$. Let $\bar x \in S$ be a point of $S$ closest to $x^*$ (or any point of $S$), and suppose $\|A(x^* - \bar x)\| \le 2\|x^* - \bar x\|$. If $\hat x \in S$ satisfies $\|y - A\hat x\| \le \|y - A\bar x\| + \varepsilon$, which holds in particular when $\|y - A\hat x\| \le \min_{x \in S}\|y - Ax\| + \varepsilon$, then

$$\|\hat x - x^*\| \le \Big(\frac4\gamma + 1\Big)\|x^* - \bar x\| + \frac1\gamma\big(2\|\eta\| + \varepsilon + \delta\big).$$

*Proof.* Both $\hat x$ and $\bar x$ lie in $S$, so S-REC gives $\gamma\|\hat x - \bar x\| \le \|A(\hat x - \bar x)\| + \delta$. By the triangle inequality and the assumption on $\hat x$,

$$\|A(\hat x - \bar x)\| \le \|A\hat x - y\| + \|y - A\bar x\| \le 2\|y - A\bar x\| + \varepsilon.$$

Since $y - A\bar x = A(x^* - \bar x) + \eta$, the assumption on $\bar x$ gives $\|y - A\bar x\| \le 2\|x^* - \bar x\| + \|\eta\|$. Together,

$$\gamma\|\hat x - \bar x\| \le 4\|x^* - \bar x\| + 2\|\eta\| + \varepsilon + \delta.$$

Finally $\|\hat x - x^*\| \le \|\hat x - \bar x\| + \|\bar x - x^*\|$, and dividing the last display by $\gamma$ gives the claim.

**The probabilistic part (cited).** Let $A$ have independent $N(0, 1/m)$ entries. For one fixed vector $v$, $m\|Av\|^2/\|v\|^2$ has the chi-square law with $m$ degrees of freedom, so $\|Av\| \le 2\|v\|$ fails with probability $e^{-\Omega(m)}$; apply this to $v = x^* - \bar x$, which does not depend on $A$. Bora et al. (Lemma 4.1) prove: if $G$ is $L$-Lipschitz and $m = \Omega\big((k/\alpha^2)\log(Lr/\delta)\big)$, then $A$ satisfies $\text{S-REC}(G(B^k(r)), 1 - \alpha, \delta)$ with probability $1 - e^{-\Omega(\alpha^2 m)}$. With $\alpha$ fixed, this and the theorem give their Theorem 1.2: with $m = O(k\log(Lr/\delta))$, with probability $1 - e^{-\Omega(m)}$, the error is at most a constant times $\min_{\|z\| \le r}\|G(z) - x^*\| + \|\eta\| + \varepsilon + \delta$; the paper states the constants $6$, $3$, $2$ and $2$ for a suitable $\alpha$. Lemma 4.2 of the paper gives the same for a $d$-layer ReLU network with $m = \Omega\big((1/\alpha^2) k d\log n\big)$ and $\delta = 0$.

**The gradient.** Let $f(z) = \|AG(z) - y\|^2 + \lambda\|z\|^2$ and let $G$ be differentiable with Jacobian $J_G(z) \in \mathbb{R}^{n \times k}$. Then

$$\nabla f(z) = 2J_G(z)^TA^T\big(AG(z) - y\big) + 2\lambda z.$$

*Proof.* The differential of $z \mapsto \|AG(z) - y\|^2$ in a direction $u$ is $2\langle AG(z) - y, AJ_G(z)u\rangle = \langle 2J_G(z)^TA^T(AG(z) - y), u\rangle$, and that of $\lambda\|z\|^2$ is $\langle 2\lambda z, u\rangle$. For $G(z) = \tanh(Wz + b)$, entry by entry, $J_G(z) = \operatorname{diag}(1 - G(z)^2)\,W$, so $J_G(z)^Tv = W^T\big(v \odot (1 - G(z)^2)\big)$; this is the vector-Jacobian product in the implementation, and the tests check it against central differences. Lines L5 and L6 are therefore exact gradient steps on $f$, and line L7 keeps the start with the lowest final loss.

**The one-measurement example.** For $G(z) = (\tanh z, \tanh 2z)$ and $A = (1\ \ 1)$, the map $z \mapsto AG(z) = \tanh z + \tanh 2z$ has the derivative $(1 - \tanh^2 z) + 2(1 - \tanh^2 2z) > 0$, so it is strictly increasing and every $y$ in its range has exactly one code. Hence the minimizer of the noiseless loss is unique and equals the true code, although $m = 1 < n = 2$. For $A = (1\ \ {-1})$ the map $\tanh z - \tanh 2z$ is not monotone on $z > 0$ (it is 0 at $z = 0$, negative in between and tends to 0 as $z \to \infty$), so two codes fit $y = -0.2$ exactly. Here $S$-REC fails for every $\gamma > 0$ and $\delta$ small: two different points of the range have the same measurement.
