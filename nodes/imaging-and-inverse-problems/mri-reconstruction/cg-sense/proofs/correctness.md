---
title: CG-SENSE reaches the weighted least squares solution in at most n^2 steps, and the energy norm of its error does not increase
proves: [correctness]
status: full
---

The setting is that of the algorithm, in exact arithmetic. The image has $N = n^2$ pixels. The encoding operator $E : \mathbb{C}^N \to \mathbb{C}^{cS}$ maps an image to the $S$ samples of each of the $c$ coils, $E x = (M F (s_k x))_k$, where $F$ is the unitary DFT on a Cartesian grid or the nonuniform DFT on a trajectory. $D$ is a diagonal matrix with positive entries, and $D = I$ when no weights are given. Let

$$A = E^H D E, \qquad b = E^H D y.$$

Line L1 computes $b$, line L2 sets $x_0 = 0$, $r_0 = p_0 = b$, and each pass of the loop computes $q_t = A p_t$ (line L5), $\alpha_t = \lVert r_t \rVert^2 / \langle p_t, q_t \rangle$ (line L6), $x_{t+1} = x_t + \alpha_t p_t$ (line L7), $r_{t+1} = r_t - \alpha_t q_t$ (line L8), and $p_{t+1} = r_{t+1} + \beta_t p_t$ with $\beta_t = \lVert r_{t+1} \rVert^2 / \lVert r_t \rVert^2$ (line L9). The inner product is $\langle u, w \rangle = u^H w$.

**Theorem.** Suppose $E$ has full column rank $N$. Then:
1. $A$ is Hermitian positive definite, and $x^\star = A^{-1} b$ is the unique minimizer of $\lVert D^{1/2}(E x - y) \rVert^2$.
2. As long as $r_t \ne 0$, the iterate $x_t$ minimizes $\lVert x - x^\star \rVert_A^2 = (x - x^\star)^H A (x - x^\star)$ over the Krylov subspace $\mathcal{K}_t = \operatorname{span}\{b, Ab, \ldots, A^{t-1} b\}$. Hence $\lVert x_t - x^\star \rVert_A$ does not increase with $t$.
3. Some $t \le N$ has $r_t = 0$, and then $x_t = x^\star$.
4. If $y = E x_{\text{true}}$ (no noise), then $x^\star = x_{\text{true}}$ for every positive $D$.
5. For a Cartesian scan that keeps the rows $\kappa \equiv 0 \pmod R$ and $D = I$, $x^\star$ is the output of [SENSE](/sense/) with $\Psi = I$.

*Proof of 1.* $A^H = E^H D^H E = A$ because $D$ is real and diagonal. For $w \ne 0$, $w^H A w = \lVert D^{1/2} E w \rVert^2 > 0$, because $E w \ne 0$ by full column rank and $D^{1/2}$ is invertible. The objective $\phi(x) = \lVert D^{1/2}(Ex - y) \rVert^2$ has the gradient $2(Ax - b)$ and the Hessian $2A$, which is positive definite, so its only stationary point $x^\star$ is its unique minimizer. $\square$

**Lemma.** As long as $r_0, \ldots, r_{t} \ne 0$: (a) $r_j = b - A x_j$ for $j \le t$; (b) the residuals $r_0, \ldots, r_t$ are mutually orthogonal; (c) the directions $p_0, \ldots, p_t$ are $A$-conjugate, $\langle p_i, A p_j \rangle = 0$ for $i \ne j$; (d) $\operatorname{span}\{r_0, \ldots, r_{t-1}\} = \operatorname{span}\{p_0, \ldots, p_{t-1}\} = \mathcal{K}_t$.

*Proof.* (a) holds for $j = 0$, and line L8 keeps it, since $b - A x_{j+1} = r_j - \alpha_j A p_j$. Part (d) follows by induction from $p_0 = r_0 = b$, $r_{j+1} = r_j - \alpha_j A p_j$ and $p_{j+1} = r_{j+1} + \beta_j p_j$: each step adds at most one power of $A$. For (b) and (c), use induction on $t$. Suppose they hold up to $t$. The choice of $\alpha_t$ and $\langle p_t, A p_t \rangle = \langle r_t, A p_t \rangle$ (since $p_t - r_t$ is a multiple of $p_{t-1}$, which is $A$-conjugate to $p_t$) give $\langle r_t, r_{t+1} \rangle = \lVert r_t \rVert^2 - \alpha_t \langle r_t, A p_t \rangle = 0$. For $j < t$, $\langle r_j, r_{t+1} \rangle = \langle r_j, r_t \rangle - \alpha_t \langle r_j, A p_t \rangle = 0$, because $r_j$ lies in the span of $p_0, \ldots, p_j$, which are $A$-conjugate to $p_t$. So (b) holds up to $t + 1$. For (c), $A p_j \in \operatorname{span}\{r_j, r_{j+1}\}$ by line L8, so $\langle p_{t+1}, A p_j \rangle = \langle r_{t+1}, A p_j \rangle + \beta_t \langle p_t, A p_j \rangle = 0$ for $j < t$. For $j = t$, $A p_t = (r_t - r_{t+1})/\alpha_t$ and $\langle r_{t+1}, A p_t \rangle = -\lVert r_{t+1} \rVert^2/\alpha_t$, while $\beta_t \langle p_t, A p_t \rangle = \beta_t \lVert r_t \rVert^2/\alpha_t = \lVert r_{t+1} \rVert^2/\alpha_t$; the sum is 0. $\square$

*Proof of 2.* By (d), $x_t \in \mathcal{K}_t$. By (a) and (b), $A(x^\star - x_t) = r_t$ is orthogonal to $r_0, \ldots, r_{t-1}$, which span $\mathcal{K}_t$. So for every $z \in \mathcal{K}_t$, $\lVert z - x^\star \rVert_A^2 = \lVert x_t - x^\star \rVert_A^2 + \lVert z - x_t \rVert_A^2 + 2 \operatorname{Re} \langle z - x_t, A(x_t - x^\star) \rangle$, and the last term is 0. Hence $x_t$ is the minimizer over $\mathcal{K}_t$. The subspaces are nested, $\mathcal{K}_t \subseteq \mathcal{K}_{t+1}$, so the minimum does not increase. $\square$

*Proof of 3.* Nonzero mutually orthogonal vectors in $\mathbb{C}^N$ number at most $N$, so by (b) some $r_t$ with $t \le N$ is zero. Then $A x_t = b$ by (a), so $x_t = x^\star$. Line L4 stops the loop there. $\square$

*Proof of 4.* With $y = E x_{\text{true}}$, $\phi(x_{\text{true}}) = 0$, the least possible value, and the minimizer is unique by part 1. $\square$

*Proof of 5.* By the folding lemma on the [SENSE](/sense/) page, the kept rows of coil $k$ are $n^{-1}$ times the DFT of size $m \times n$, $m = n/R$, of the folded image $\sum_p (s_k x)(i + pm, j)$. That DFT is $\sqrt{mn}$ times a unitary map, so $\sum_k \lVert y_k - E_k x \rVert^2 = (m/n) \sum_k \sum_{(i,j)} |a_k(i, j) - (E_{ij} v_{ij})_k|^2$, where $a_k$ are the folded images from the data, $E_{ij}$ the unfolding matrix and $v_{ij}$ the pixel group of $x$. The right side is a sum of independent SENSE objectives, one for each folded pixel, so the two problems have the same minimizers. $\square$

**Remarks.**
- In floating point the residuals lose their orthogonality, and CG does not stop exactly after $N$ steps. The bound $\lVert x_t - x^\star \rVert_A \le 2 \bigl(\frac{\sqrt{\kappa} - 1}{\sqrt{\kappa} + 1}\bigr)^t \lVert x^\star \rVert_A$ with the condition number $\kappa$ of $A$ is the standard rate in exact arithmetic.
- With noise, $x^\star$ is the weighted least squares solution, not the object. Stopping early regularizes; the choice of the stopping index is then a heuristic unless the noise level is known.
- The weights $D$ change the solution when the data are noisy or inconsistent. For noiseless data they change only the speed (part 4).
