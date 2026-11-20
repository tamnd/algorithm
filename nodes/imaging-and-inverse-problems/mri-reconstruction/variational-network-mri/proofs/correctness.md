---
title: A variational network stage with derivative activations is a gradient step, and safe steps decrease a known energy
proves: [correctness]
status: full
---

The setting is that of the algorithm. An image $u$ is a vector in $\mathbb{C}^N$ with $N = n_1 n_2$. We use the real inner product $\langle u, v \rangle_{\mathbb{R}} = \operatorname{Re} \sum_p \overline{u(p)} v(p)$, so $\mathbb{C}^N$ is the real space $\mathbb{R}^{2N}$, and gradients are taken in this space. The forward operator is $A u = (M F (c_j u))_{j}$ with the unitary 2D DFT $F$, a 0/1 mask $M$ and coil maps $c_j$ with $\sum_j |c_j(p)|^2 \le 1$ at every pixel (one coil with $c = 1$ if no maps are given). A stage is a pair $(r_t, \mu_t)$ of a function $r_t$ and a number $\mu_t \ge 0$, and the network computes

$$u_0 = A^* f, \qquad u_{t+1} = u_t - r_t(u_t) - \mu_t A^*(A u_t - f), \quad t = 0, \ldots, T-1.$$

A trained network is a list of such stages. Nothing below is about training. It is about what one stage computes and about a special choice of stages for which the answer is known.

## 1. The operators

**Lemma 1.** $\|A\| \le 1$. The function `apply_ah` is the adjoint of `apply_a`. For a filter $(k^{\text{re}}, k^{\text{im}})$, the real image $(K u)(p) = \sum_o k^{\text{re}}_o \operatorname{Re} u(p + o) + k^{\text{im}}_o \operatorname{Im} u(p + o)$ has the adjoint $(K^T z)(q) = \sum_o (k^{\text{re}}_o + i k^{\text{im}}_o) z(q - o)$, that is, $\sum_p (K u)(p) z(p) = \langle u, K^T z \rangle_{\mathbb{R}}$ for every real image $z$.

*Proof.* $\|A u\|^2 = \sum_j \|M F (c_j u)\|^2 \le \sum_j \|c_j u\|^2 = \sum_p \sum_j |c_j(p)|^2 |u(p)|^2 \le \|u\|^2$, because $F$ is unitary and $M$ is a projection. The adjoint of $u \mapsto M F (c_j u)$ is $y \mapsto \bar c_j F^* M y$, and the adjoint of a stack is the sum, which is what `apply_ah` computes. For the filter, $\sum_p z(p) \sum_o k^{\text{re}}_o \operatorname{Re} u(p+o) = \sum_q \operatorname{Re} u(q) \sum_o k^{\text{re}}_o z(q - o)$ with $q = p + o$, and the same holds for the imaginary part. Since $\langle u, a + i b \rangle_{\mathbb{R}} = \sum_q \operatorname{Re} u(q)\, a(q) + \operatorname{Im} u(q)\, b(q)$ for real images $a$ and $b$, the claim follows. $\square$

## 2. A stage is a gradient step when the activations are derivatives

Take filters $K_1, \ldots, K_m$, potentials $\phi_i : \mathbb{R} \to \mathbb{R}$ with continuous derivatives $\phi_i'$, a weight $\lambda \ge 0$, and the energy

$$E(u) = \sum_{i=1}^m \sum_p \phi_i\big((K_i u)(p)\big) + \frac{\lambda}{2} \|A u - f\|^2.$$

**Theorem 2.** $\nabla E(u) = \sum_i K_i^T \phi_i'(K_i u) + \lambda A^*(A u - f)$, with $\phi_i'$ applied pixel by pixel. So if $r_t(u) = \alpha \sum_i K_i^T \phi_i'(K_i u)$ and $\mu_t = \alpha \lambda$, then $u_{t+1} = u_t - \alpha \nabla E(u_t)$.

*Proof.* For a direction $h$, the derivative of $\sum_p \phi_i((K_i u)(p))$ is $\sum_p \phi_i'((K_i u)(p)) (K_i h)(p) = \langle h, K_i^T \phi_i'(K_i u) \rangle_{\mathbb{R}}$ by Lemma 1, because $K_i$ is real linear. The derivative of $\frac12 \|A u - f\|^2$ is $\operatorname{Re} \langle A h, A u - f \rangle = \langle h, A^*(A u - f) \rangle_{\mathbb{R}}$. $\square$

Every continuous activation $\psi$ of one real variable is the derivative of $\phi(z) = \int_0^z \psi(s)\, ds$. So each stage of a trained network of this form is a gradient step on its own energy $E_t$. But $E_t$ changes from stage to stage, and its step is not limited, so the results of Section 3 do not apply to a trained network. This is the reason a trained network has no energy that decreases and no convergence theorem.

The test file checks Theorem 2 with central differences of $E$ for the forward difference filters, the potential $\phi(z) = \sqrt{z^2 + \varepsilon^2}$, two coils and a random mask.

## 3. Safe steps decrease the energy

The forward difference filters are $K_1 u = D_x \operatorname{Re} u$, $K_2 u = D_y \operatorname{Re} u$, $K_3 u = D_x \operatorname{Im} u$ and $K_4 u = D_y \operatorname{Im} u$, where $(D_x a)(i, j) = a(i, j+1) - a(i, j)$ and $(D_y a)(i, j) = a(i+1, j) - a(i, j)$, with periodic indices.

**Lemma 3.** $\|\sum_{i=1}^4 K_i^T K_i\| \le 8$.

*Proof.* By Lemma 1, $K_1^T z = D_x^T z$ and $K_3^T z = i D_x^T z$, and the same for $D_y$. So $\sum_i K_i^T K_i u = L \operatorname{Re} u + i L \operatorname{Im} u$ with $L = D_x^T D_x + D_y^T D_y$. Each difference operator has norm at most 2, because $\|D_x a\| \le \|a(\cdot, \cdot + 1)\| + \|a\| = 2 \|a\|$. So $\|L\| \le 4 + 4 = 8$, and the real and imaginary parts do not mix. $\square$

**Lemma 4.** Let $\phi(z) = \sqrt{z^2 + \varepsilon^2}$ with $\varepsilon > 0$ for all four filters. Then $\nabla E$ is Lipschitz with the constant $L_E = 8/\varepsilon + \lambda$.

*Proof.* $\phi''(z) = \varepsilon^2 (z^2 + \varepsilon^2)^{-3/2} \in (0, 1/\varepsilon]$, so $\phi'$ is Lipschitz with the constant $1/\varepsilon$. Write $\mathcal{K} u = (K_1 u, \ldots, K_4 u)$, so that $\|\mathcal{K}\|^2 = \|\mathcal{K}^T \mathcal{K}\| = \|\sum_i K_i^T K_i\| \le 8$ by Lemma 3. Then the regularizer part of the gradient is $\mathcal{K}^T \phi'(\mathcal{K} u)$, and

$$\|\mathcal{K}^T (\phi'(\mathcal{K} u) - \phi'(\mathcal{K} v))\| \le \|\mathcal{K}\| \cdot \frac1\varepsilon \|\mathcal{K}(u - v)\| \le \frac{8}{\varepsilon} \|u - v\|.$$

The data part $\lambda A^* A$ has norm at most $\lambda$ by Lemma 1. $\square$

**Theorem 5.** With the stages of Theorem 2 for this energy and $0 < \alpha \le 1/L_E$,

$$E(u_{t+1}) \le E(u_t) - \frac{1}{2\alpha} \|u_{t+1} - u_t\|^2$$

for every $t$. So $E(u_t)$ does not increase, and the sum of $\|u_{t+1} - u_t\|^2$ over all stages is at most $2\alpha (E(u_0) - \inf E)$.

*Proof.* For a function with an $L_E$-Lipschitz gradient, $E(u + h) \le E(u) + \langle \nabla E(u), h \rangle_{\mathbb{R}} + \frac{L_E}{2} \|h\|^2$ (the descent lemma, from the integral form of the remainder). With $g = \nabla E(u_t)$ and $h = -\alpha g$, this gives $E(u_{t+1}) \le E(u_t) - \alpha (1 - \alpha L_E / 2) \|g\|^2 \le E(u_t) - \frac{\alpha}{2} \|g\|^2$, and $\frac{\alpha}{2} \|g\|^2 = \frac{1}{2\alpha} \|u_{t+1} - u_t\|^2$. The energy is bounded below by 0, which gives the sum. $\square$

The test file checks the inequality of Theorem 5 at every stage with $\alpha = 1/L_E$. The bound $\alpha \le 1/L_E$ is sufficient, not necessary. With five times this step, the example on the page shows the energy go up, and with twenty times it diverges.

## 4. Two further facts

**Lemma 6 (no regularizer).** If $r_t = 0$ for all $t$, the network is the [Landweber iteration](/landweber-iteration/) $u_{t+1} = u_t - \mu_t A^*(A u_t - f)$ from $u_0 = A^* f$. With one coil, $c = 1$ and $f = M f$ (data only on the mask), $u_0$ fits the data exactly, so $u_t = u_0$ for every $t$.

*Proof.* The first claim is the definition. With one coil, $A A^* = M F F^* M = M$, so $A u_0 - f = M f - f = 0$, the correction is zero, and the iterates do not move. $\square$

So with one coil, data consistency alone never improves on zero filling. All the change from $u_0$ comes from the regularizer.

**Lemma 7 (call counts).** A network of $T$ stages calls each $r_t$ once, $A$ exactly $T$ times and $A^*$ exactly $T + 1$ times.

*Proof.* Line L1 calls $A^*$ once, and each pass of the loop calls $r_t$, $A$ and $A^*$ once each. $\square$
