---
title: "LISTA with the ISTA weights is ISTA, its fixed points are the lasso solutions, and the backpropagation formulas give the gradient of the training loss"
proves: [correctness]
status: full
---

**Setting.** $A \in \mathbb{R}^{m \times n}$, $y \in \mathbb{R}^m$, $\lambda > 0$ and $L \ge \|A\|^2$. The lasso objective is $F(x) = \tfrac12\|Ax - y\|^2 + \lambda\|x\|_1$. Soft thresholding with a vector of thresholds $\theta \ge 0$ is $\operatorname{soft}(v, \theta)_i = \operatorname{sign}(v_i)\max(|v_i| - \theta_i, 0)$. A LISTA layer with weights $(W_e, S, \theta)$ maps $x$ to $\operatorname{soft}(W_e y + S x, \theta)$, and the network starts from $x^0 = 0$ (lines L1 to L5).

What is proved here is a statement about the algorithm around the weights. Nothing is proved about trained weights: for them the page reports measurements only.

**Fact (P).** For $t > 0$, $\operatorname{soft}(v, t\mathbf{1})$ is the proximal operator of $t\|\cdot\|_1$: it is the unique minimizer of $u \mapsto t\|u\|_1 + \tfrac12\|u - v\|^2$. *Proof.* The function is separable and strongly convex, so it has one minimizer, and each coordinate solves $\min_{u_i} t|u_i| + \tfrac12(u_i - v_i)^2$. The optimality condition $0 \in t\,\partial|u_i| + u_i - v_i$ gives $u_i = v_i - t$ if $v_i > t$, $u_i = v_i + t$ if $v_i < -t$, and $u_i = 0$ if $|v_i| \le t$, because then $v_i/t \in [-1, 1] = \partial|0|$. This is the soft threshold.

**Lemma 1 (one layer is one ISTA step).** Let $W_e = A^T/L$, $S = I - A^TA/L$ and $\theta = (\lambda/L)\mathbf{1}$. Then for every $x$,

$$\operatorname{soft}(W_e y + Sx, \theta) = \operatorname{soft}\big(x - \tfrac1L A^T(Ax - y), \tfrac{\lambda}{L}\big),$$

the ISTA step with step $1/L$. *Proof.* $W_e y + Sx = \tfrac1L A^Ty + x - \tfrac1L A^TAx = x - \tfrac1L A^T(Ax - y)$. The thresholds are equal.

**Corollary.** By induction on $k$, the $K$-layer network with these weights in every layer returns the ISTA iterate $x^K$ started at $x^0 = 0$. The base case is $x^0 = 0$ in both; the step is Lemma 1. The test `test_lista_with_ista_weights_is_ista` checks this for $K = 1, \ldots, 11$.

**Lemma 2 (fixed points).** With the weights of Lemma 1, $x$ is a fixed point of the layer if and only if $x$ minimizes $F$. *Proof.* By (P), $x = \operatorname{soft}(v, \lambda/L)$ with $v = x - \tfrac1L A^T(Ax - y)$ holds if and only if $v - x \in (\lambda/L)\,\partial\|x\|_1$, that is $-\tfrac1L A^T(Ax - y) \in \tfrac{\lambda}{L}\partial\|x\|_1$. Multiply by $L$: this is $0 \in A^T(Ax - y) + \lambda\,\partial\|x\|_1 = \partial F(x)$. Since $F$ is convex, $0 \in \partial F(x)$ is the condition for a minimizer.

So with the ISTA weights a deep enough network approaches a lasso solution: ISTA converges for $L \ge \|A\|^2$, with $F(x^K) - F^* \le L\|x^0 - x^*\|^2/(2K)$ (Beck and Teboulle 2009, Theorem 3.1; see [iterative shrinkage-thresholding](/iterative-shrinkage-thresholding/)). LISTA with other weights has no such guarantee in general.

**Lemma 3 (why $S$ and $W_e$ must be coupled).** Take no thresholds ($\theta = 0$) and tied weights. If every $x \in \mathbb{R}^n$ is a fixed point of the layer for the data $y = Ax$, then $S = I - W_eA$. *Proof.* With $\theta = 0$ the layer is the linear map $x \mapsto W_eAx + Sx$. If it fixes every $x$, then $(W_eA + S - I)x = 0$ for all $x$, so $W_eA + S - I = 0$. Chen, Liu, Wang and Yin (2018, Theorem 1) prove the same coupling in the limit, with thresholds, for networks that recover every sparse $x$; this motivates LISTA-CP, which sets $S^k = I - W^kA$ in each layer.

**Lemma 4 (backpropagation).** Let $c^k = W_e^k y + S^k x^{k-1}$ and $x^k = \operatorname{soft}(c^k, \theta^k)$ for $k = 1, \ldots, K$, and let $\ell = \tfrac12\|x^K - x^\star\|^2$ for a target $x^\star$. Suppose $|c^k_i| \ne \theta^k_i$ for all $k$ and $i$. Set $g^K = x^K - x^\star$, and for $k = K, \ldots, 1$ let $a^k_i = 1$ if $|c^k_i| > \theta^k_i$ and $0$ otherwise, $d^k = a^k \odot g^k$ and $g^{k-1} = (S^k)^T d^k$. Then

$$\frac{\partial \ell}{\partial W_e^k} = d^k y^T,\qquad \frac{\partial \ell}{\partial S^k} = d^k (x^{k-1})^T,\qquad \frac{\partial \ell}{\partial \theta^k_i} = -\operatorname{sign}(c^k_i)\, a^k_i\, g^k_i.$$

*Proof.* Under the assumption, each $\operatorname{soft}(\cdot, \cdot)_i$ is differentiable near $(c^k_i, \theta^k_i)$: on the active branch it is $c_i - \operatorname{sign}(c_i)\theta_i$, with derivative 1 in $c_i$ and $-\operatorname{sign}(c_i)$ in $\theta_i$; on the dead branch it is 0 near the point. We show by downward induction that $g^k = \partial\ell/\partial x^k$. For $k = K$ this is the derivative of $\ell$. If it holds for $k$, the chain rule through $x^k = \operatorname{soft}(c^k, \theta^k)$ gives $\partial\ell/\partial c^k = a^k \odot g^k = d^k$, and through $c^k = W_e^k y + S^k x^{k-1}$ it gives $\partial\ell/\partial x^{k-1} = (S^k)^T d^k = g^{k-1}$. The weight $W_e^k$ enters $\ell$ only through $c^k$, linearly with $\partial c^k_i/\partial (W_e^k)_{ij} = y_j$, which gives $d^k y^T$; the same argument gives $d^k (x^{k-1})^T$ for $S^k$, and the threshold formula is the chain rule through the active branch. For tied weights, the gradient is the sum of the $K$ layer gradients, because the tied weight enters each layer once. The set where some $|c^k_i| = \theta^k_i$ has measure zero in the data for fixed weights, and the test checks the formulas against central differences.
