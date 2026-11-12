---
title: The Kronecker identities behind K-FAC, the form of a Fisher block, and the damped step
proves: [correctness]
status: full
---

**Setting.** Layer $l$ computes $s = W\bar{a}$ with $W \in \mathbb{R}^{d_o \times d_a}$ and $\bar{a} \in \mathbb{R}^{d_a}$ its input with a $1$ appended. For a target $y$, $g = \partial\log p(y \mid x)/\partial s \in \mathbb{R}^{d_o}$ up to sign, so $\nabla_W\log p = g\bar{a}^\top$. The operator $\operatorname{vec}$ stacks columns: entry $(i, j)$ of an $n \times m$ matrix $X$ is entry $(j-1)n + i$ of $\operatorname{vec}(X)$. The Kronecker product $A \otimes B$ is the block matrix whose block $(j, k)$ is $A_{jk}B$.

**Lemma 1.** $\operatorname{vec}(uv^\top) = v \otimes u$. In particular $\operatorname{vec}(\nabla_W\log p) = \bar{a} \otimes g$.

*Proof.* Column $j$ of $uv^\top$ is $v_ju$, and block $j$ of $v \otimes u$ is $v_ju$. $\square$

**Lemma 2 (vec identity).** For $A \in \mathbb{R}^{m \times m}$, $G \in \mathbb{R}^{n \times n}$ and $X \in \mathbb{R}^{n \times m}$, $(A \otimes G)\operatorname{vec}(X) = \operatorname{vec}(GXA^\top)$.

*Proof.* Block $j$ of the left side is $\sum_k A_{jk}Gx_k$, where $x_k$ is column $k$ of $X$. Column $j$ of $GXA^\top$ is $G\sum_k x_k(A^\top)_{kj} = \sum_k A_{jk}Gx_k$. $\square$

**Lemma 3 (mixed product and inverse).** $(A \otimes G)(B \otimes H) = AB \otimes GH$ when the sizes match, and if $A$ and $G$ are invertible, $(A \otimes G)^{-1} = A^{-1} \otimes G^{-1}$.

*Proof.* Block $(j, k)$ of the product is $\sum_i A_{ji}G\,B_{ik}H = (AB)_{jk}\,GH$. With $B = A^{-1}$ and $H = G^{-1}$ the product is $I \otimes I = I$. $\square$

**Claim 1 (one example).** For one input $x$ and one target $y$, the outer product of the vectorized gradient is $\operatorname{vec}(\nabla_W)\operatorname{vec}(\nabla_W)^\top = \bar{a}\bar{a}^\top \otimes gg^\top$. For a fixed input, the Fisher block of $W$, $F_W = \mathbb{E}_{y \sim p(\cdot \mid x)}[\operatorname{vec}(\nabla_W)\operatorname{vec}(\nabla_W)^\top]$, equals $\bar{a}\bar{a}^\top \otimes \mathbb{E}_y[gg^\top]$ exactly.

*Proof.* By Lemma 1 and the mixed product, $(\bar{a} \otimes g)(\bar{a} \otimes g)^\top = (\bar{a} \otimes g)(\bar{a}^\top \otimes g^\top) = \bar{a}\bar{a}^\top \otimes gg^\top$. For a fixed $x$, $\bar{a}$ does not depend on $y$, and the Kronecker product is linear in its second factor. $\square$

Over a data distribution, $F_W = \mathbb{E}_x\bigl[\bar{a}\bar{a}^\top \otimes \mathbb{E}_y[gg^\top]\bigr]$. K-FAC replaces it by $\bar{A} \otimes G$ with $\bar{A} = \mathbb{E}[\bar{a}\bar{a}^\top]$ and $G = \mathbb{E}[gg^\top]$. The two are equal when $\bar{a}\bar{a}^\top$ and $gg^\top$ are uncorrelated, in particular when they are independent; in general this is an approximation, and the paper measures its quality empirically.

**Claim 2 (output layer).** For a softmax output with probabilities $p$ and $g = p - e_y$, $\mathbb{E}_{y \sim p}[gg^\top] = \operatorname{diag}(p) - pp^\top$.

*Proof.* $\sum_y p_y(p - e_y)(p - e_y)^\top = pp^\top\sum_y p_y - p\sum_y p_ye_y^\top - \sum_y p_ye_yp^\top + \sum_y p_ye_ye_y^\top = pp^\top - pp^\top - pp^\top + \operatorname{diag}(p)$. $\square$

This is why the targets for $G$ must be sampled from the model: with the training labels in place of $y \sim p$ the result is the empirical Fisher, a different matrix.

**Claim 3 (the step).** Let $\bar{A}$ and $G$ be positive semidefinite, $\gamma > 0$, $\pi > 0$, $\bar{A}_\gamma = \bar{A} + \pi\gamma I$ and $G_\gamma = G + (\gamma/\pi)I$. Then $\bar{A}_\gamma \otimes G_\gamma$ is positive definite, and $\Delta = -G_\gamma^{-1}\nabla_W h\,\bar{A}_\gamma^{-1}$ satisfies $\operatorname{vec}(\Delta) = -(\bar{A}_\gamma \otimes G_\gamma)^{-1}\operatorname{vec}(\nabla_W h)$. Unless $\nabla_W h = 0$, $\langle\nabla_W h, \Delta\rangle < 0$.

*Proof.* $\bar{A}_\gamma$ and $G_\gamma$ are symmetric positive definite. The eigenvalues of a Kronecker product are the products of eigenvalues of the factors, all positive here, so $\bar{A}_\gamma \otimes G_\gamma$ is positive definite. By Lemma 3 its inverse is $\bar{A}_\gamma^{-1} \otimes G_\gamma^{-1}$, and by Lemma 2 with $A = \bar{A}_\gamma^{-1}$ (symmetric) and $G = G_\gamma^{-1}$, applying it to $\operatorname{vec}(\nabla_W h)$ gives $\operatorname{vec}(G_\gamma^{-1}\nabla_W h\,\bar{A}_\gamma^{-1})$. Finally $\langle\nabla_W h, \Delta\rangle = -v^\top M^{-1}v < 0$ for $v = \operatorname{vec}(\nabla_W h) \ne 0$ and $M$ positive definite. $\square$

The cost is two solves of size $d_a$ and $d_o$, $O(d_a^3 + d_o^3)$, instead of one solve of size $d_ad_o$, $O(d_a^3d_o^3)$.

**Claim 4 (choice of $\pi$).** $\bar{A}_\gamma \otimes G_\gamma = \bar{A} \otimes G + \gamma\bigl(\pi\,I \otimes G + \pi^{-1}\bar{A} \otimes I\bigr) + \gamma^2 I$. The extra term $\gamma(\pi I \otimes G + \pi^{-1}\bar{A} \otimes I)$, compared with plain Tikhonov damping $\bar{A} \otimes G + \gamma^2I$, has the smallest trace norm when $\pi = \sqrt{(\operatorname{tr}\bar{A}/d_a)/(\operatorname{tr}G/d_o)}$.

*Proof.* The expansion is the mixed product applied to each pair of terms. The extra term is positive semidefinite, so its trace norm is its trace. With $\operatorname{tr}(I_{d_a} \otimes G) = d_a\operatorname{tr}G$ and $\operatorname{tr}(\bar{A} \otimes I_{d_o}) = d_o\operatorname{tr}\bar{A}$, the trace is $\gamma(\pi d_a\operatorname{tr}G + \pi^{-1}d_o\operatorname{tr}\bar{A})$, a convex function of $\pi > 0$ with derivative zero at $\pi^2 = d_o\operatorname{tr}\bar{A}/(d_a\operatorname{tr}G)$. $\square$

**Claim 5 (step length).** For a direction $\Delta$ with $\langle\nabla h, \Delta\rangle < 0$ and the damped quadratic model $M(\delta) = \langle\nabla h, \delta\rangle + \tfrac12\delta^\top(F + (\lambda + \eta)I)\delta$, with $F$ the exact Fisher, the minimizer of $M(\alpha\Delta)$ over $\alpha$ is $\alpha^* = -\langle\nabla h, \Delta\rangle/(\Delta^\top F\Delta + (\lambda + \eta)\lVert\Delta\rVert^2) > 0$, and $M(\alpha^*\Delta) = \tfrac12\alpha^*\langle\nabla h, \Delta\rangle < 0$.

*Proof.* $M(\alpha\Delta)$ is a quadratic in $\alpha$ with positive leading coefficient $\tfrac12(\Delta^\top F\Delta + (\lambda + \eta)\lVert\Delta\rVert^2)$; set its derivative to zero and substitute. $\square$
