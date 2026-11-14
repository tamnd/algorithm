---
title: The eigendecomposition of the TCC gives the sum of coherent systems, with truncation error set by the tail eigenvalues
proves: [correctness]
status: full
---

**Setting.** Let $f_1, \dots, f_N$ be the band frequencies, $J(s) \ge 0$ the weights of finitely many source points $s$, and $H$ the pupil. The TCC is $T_{ab} = \sum_s J(s) H(f_a + s) \overline{H(f_b + s)}$, and for mask coefficients $M_a = M(f_a)$ the Hopkins image is

$$ I(x) = \sum_{a, b} T_{ab}\, M_a \overline{M_b}\, e^{2\pi i (f_a - f_b) x}. $$

For a point $x$ define the vector $u = u(x) \in \mathbb{C}^N$ by $u_a = \overline{M_a}\, e^{-2\pi i f_a x}$. Write $\|u\|^2 = \sum_a |u_a|^2 = \sum_a |M_a|^2$.

**Lemma 1 (the image is a quadratic form).** $I(x) = u^* T u$.

*Proof.* $u^* T u = \sum_{a, b} \overline{u_a}\, T_{ab}\, u_b = \sum_{a, b} M_a e^{2\pi i f_a x}\, T_{ab}\, \overline{M_b} e^{-2\pi i f_b x}$, which is the Hopkins sum. $\square$

**Lemma 2 (structure of $T$).** Let $h_s \in \mathbb{C}^N$ have entries $h_s(a) = H(f_a + s)$. Then $T = \sum_s J(s)\, h_s h_s^*$. Hence $T$ is Hermitian, positive semidefinite, and of rank at most the number $S$ of source points.

*Proof.* The $(a, b)$ entry of $h_s h_s^*$ is $H(f_a + s)\overline{H(f_b + s)}$, which gives the sum. Each $h_s h_s^*$ is Hermitian, and $c^* h_s h_s^* c = |h_s^* c|^2 \ge 0$, so a sum with weights $J(s) \ge 0$ is Hermitian and positive semidefinite. Each term has rank at most one, and the rank of a sum is at most the sum of the ranks. $\square$

By the spectral theorem for Hermitian matrices, $T = \sum_{j=1}^{N} \lambda_j v_j v_j^*$ with an orthonormal basis $v_1, \dots, v_N$ and real $\lambda_1 \ge \dots \ge \lambda_N$, and $\lambda_N \ge 0$ by Lemma 2. At most $S$ of the $\lambda_j$ are nonzero. For $0 \le K \le N$ let $T_K = \sum_{j \le K} \lambda_j v_j v_j^*$, and define the coherent fields and the truncated image as in lines L7 and L8:

$$ E_j(x) = \sum_a v_j(a)\, M_a\, e^{2\pi i f_a x}, \qquad I_K(x) = \sum_{j \le K} \lambda_j |E_j(x)|^2 . $$

**Lemma 3.** $v_j^* u = \overline{E_j(x)}$, so $u^* v_j v_j^* u = |E_j(x)|^2$.

*Proof.* $v_j^* u = \sum_a \overline{v_j(a)}\, \overline{M_a}\, e^{-2\pi i f_a x} = \overline{\sum_a v_j(a) M_a e^{2\pi i f_a x}}$. Then $u^* v_j v_j^* u = \overline{(v_j^* u)}\,(v_j^* u) = |v_j^* u|^2$. $\square$

**Theorem 1 (SOCS is exact at full rank).** $I(x) = \sum_{j=1}^{N} \lambda_j |E_j(x)|^2$ for every mask and every $x$. In particular $I_K = I$ whenever $K \ge \operatorname{rank} T$, and so whenever $K \ge S$.

*Proof.* By Lemma 1 and the eigendecomposition, $I = \sum_j \lambda_j\, u^* v_j v_j^* u$, and Lemma 3 gives each term. The terms with $j > \operatorname{rank} T$ have $\lambda_j = 0$. $\square$

**Theorem 2 (pointwise error).** For every mask and every $x$,

$$ I(x) - I_K(x) = u^* (T - T_K)\, u = \sum_{j > K} \lambda_j |E_j(x)|^2 \in \big[\, 0,\ \lambda_{K+1} \|u\|^2 \,\big], $$

with $\lambda_{N+1} = 0$. The upper bound is attained: if $M_a = \overline{v_{K+1}(a)}$ for all $a$, then at $x = 0$ the error equals $\lambda_{K+1} \|u\|^2$.

*Proof.* The identity follows from Theorem 1 minus the definition of $I_K$, with Lemma 3. Every term is at least $0$, which gives the lower bound. For the upper bound, $\lambda_j \le \lambda_{K+1}$ for $j > K$, so the sum is at most $\lambda_{K+1} \sum_{j > K} |v_j^* u|^2 \le \lambda_{K+1} \sum_{j} |v_j^* u|^2 = \lambda_{K+1} \|u\|^2$, by Parseval's identity in the orthonormal basis $(v_j)$. For the attaining mask, $u = v_{K+1}$ at $x = 0$, so $|v_j^* u|^2$ is $1$ for $j = K + 1$ and $0$ otherwise, and the error is $\lambda_{K+1} = \lambda_{K+1}\|u\|^2$. $\square$

So the worst error per unit of mask energy is $\lambda_{K+1}$, the spectral norm of $T - T_K$, whose eigenvalues are $\lambda_{K+1}, \dots, \lambda_N$ and $0$.

**Corollary 3 (masks of bounded amplitude).** Let the mask $m$ have period $P$ and $|m(x)| \le 1$, with $M_a = \frac{1}{P}\int_0^P m(y) e^{-2\pi i f_a y}\, dy$ for distinct frequencies $f_a \in \frac{1}{P}\mathbb{Z}$. Then $0 \le I(x) - I_K(x) \le \lambda_{K+1}$ for all $x$. The same holds for a sampled mask with $|m[n]| \le 1$ and the discrete coefficients $M(k) = \frac{1}{N'} \sum_n m[n] e^{-2\pi i k n / N'}$, as long as the band integers $k$ are distinct modulo the number of samples $N'$.

*Proof.* By Parseval's identity for Fourier series, $\sum_{a} |M_a|^2 \le \sum_{f \in \frac1P \mathbb{Z}} |M(f)|^2 = \frac{1}{P} \int_0^P |m|^2 \le 1$. For the sampled mask, the discrete Parseval identity gives $\sum_{k \bmod N'} |M(k)|^2 = \frac{1}{N'} \sum_n |m[n]|^2 \le 1$, and the band uses each residue at most once. Apply Theorem 2. $\square$

**Theorem 4 (the trace norm is the summed error).** Let $e_a$ be the mask with $M_a = 1$ and all other coefficients $0$, a single plane wave. For every $x$,

$$ \sum_{a=1}^{N} \big( I(x) - I_K(x) \big)\Big|_{\text{mask } e_a} = \sum_{j > K} \lambda_j = \operatorname{tr}(T - T_K) = \|T - T_K\|_* . $$

Also, if $u$ is a random vector with $\mathbb{E}[u u^*] = \mathrm{Id}$, then $\mathbb{E}[I - I_K] = \sum_{j > K} \lambda_j$.

*Proof.* For the mask $e_a$, $u$ is $e^{-2\pi i f_a x}$ times the $a$th unit vector, so by Theorem 2 the error is $(T - T_K)_{aa}$; the phase cancels. The sum over $a$ is the trace of $T - T_K$, which is the sum of its eigenvalues $\lambda_{K+1}, \dots, \lambda_N$. These are at least $0$, so the trace equals the trace norm, the sum of the singular values. For the random case, $\mathbb{E}[u^* A u] = \mathbb{E}[\operatorname{tr}(A u u^*)] = \operatorname{tr}(A\, \mathbb{E}[u u^*]) = \operatorname{tr} A$ with $A = T - T_K$. $\square$

**Optimality (cited).** For every matrix $X$ of rank at most $K$, $\|T - X\|_2 \ge \lambda_{K+1}$ and $\|T - X\|_* \ge \sum_{j > K} \lambda_j$, with equality for $X = T_K$. For the spectral and Frobenius norms this is the theorem of Eckart and Young (1936), and Mirsky (1960) extended it to every unitarily invariant norm, which includes the trace norm. Any $K$ coherent systems with weights $\mu_j$ and kernel spectra $w_j$ give the image $u^* X u$ with $X = \sum_{j \le K} \mu_j w_j w_j^*$ of rank at most $K$. So, measured by these two norms of the kernel error, the SOCS truncation is the best choice of $K$ coherent systems. This part is cited, not proved here.

**The eigensolver (lines L2 and L3).** The implementation uses cyclic complex Jacobi rotations. We prove that each rotation zeroes its pivot, preserves the eigenvalues, and lowers the off-diagonal mass; the convergence of the cyclic sweeps is cited from the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/).

*One rotation.* Let $A$ be Hermitian with pivot $A_{pq} = r e^{i\varphi}$, $r > 0$, and write $\alpha = A_{pp}$, $\beta = A_{qq}$, both real. Let $U$ be the identity except on rows and columns $p, q$, where it is $W R$ with $W = \operatorname{diag}(1, e^{-i\varphi})$ and $R = \begin{pmatrix} c & s \\ -s & c \end{pmatrix}$, $c^2 + s^2 = 1$. Then $U$ is unitary, and $A' = U^* A U$ is Hermitian with the same eigenvalues. On the $2 \times 2$ block, $W^* \begin{pmatrix} \alpha & r e^{i\varphi} \\ r e^{-i\varphi} & \beta \end{pmatrix} W = \begin{pmatrix} \alpha & r \\ r & \beta \end{pmatrix}$, and the off-diagonal entry of $R^{\mathsf T} \begin{pmatrix} \alpha & r \\ r & \beta \end{pmatrix} R$ is

$$ (c, -s) \begin{pmatrix} \alpha & r \\ r & \beta \end{pmatrix} \begin{pmatrix} s \\ c \end{pmatrix} = r (c^2 - s^2) + c s (\alpha - \beta). $$

With $t = s/c$ and $\theta = (\beta - \alpha)/(2r)$, this is zero if and only if $t^2 + 2\theta t - 1 = 0$. The roots are $-\theta \pm \sqrt{\theta^2 + 1}$. The value $t = \operatorname{sgn}(\theta)/(|\theta| + \sqrt{\theta^2 + 1})$, with $\operatorname{sgn}(0) = 1$, is one of them: multiply the numerator and the denominator by $\sqrt{\theta^2 + 1} - |\theta|$ to get $t = \operatorname{sgn}(\theta)\big(\sqrt{\theta^2 + 1} - |\theta|\big) = -\theta + \operatorname{sgn}(\theta)\sqrt{\theta^2 + 1}$. It is the root of smaller size, so $|t| \le 1$ and the rotation angle is at most $\pi/4$. Then $c = 1/\sqrt{1 + t^2}$ and $s = t c$ zero the pivot.

*Off-diagonal mass.* Let $\operatorname{off}(A)^2 = \sum_{i \ne k} |A_{ik}|^2$. The Frobenius norm is invariant under $A \mapsto U^* A U$. Entries outside rows and columns $p, q$ do not change. For $k \notin \{p, q\}$, the pair $(A_{pk}, A_{qk})$ is multiplied by the unitary $2 \times 2$ block, so $|A'_{pk}|^2 + |A'_{qk}|^2 = |A_{pk}|^2 + |A_{qk}|^2$, and the same for columns. The $2 \times 2$ block keeps its Frobenius norm, $\alpha^2 + \beta^2 + 2r^2$, and now has a zero off-diagonal, so its diagonal gains $2r^2$. Hence $\operatorname{off}(A')^2 = \operatorname{off}(A)^2 - 2r^2$.

*Output.* After the rotations $U_1, \dots, U_m$, the matrix $V = U_1 \cdots U_m$ is unitary and $A = V^* T V$. Write $A = D + F$ with $D$ diagonal and $F$ the off-diagonal part. Then $T = V D V^* + V F V^*$, and $\|V F V^*\|_2 \le \|F\|_F = \operatorname{off}(A)$. The loop stops when $\operatorname{off}(A) \le \tau \|T\|_F$ for the tolerance $\tau$. By Weyl's inequality, after sorting (line L3) each diagonal value differs from the corresponding eigenvalue of $T$ by at most $\operatorname{off}(A)$. So Theorems 1 to 4 hold for the computed pairs up to an additive error of at most $\operatorname{off}(A) \|u\|^2$ in the image. The tests check $V^* V = \mathrm{Id}$ and $V D V^* = T$ to $10^{-12}$, and the full-rank image against the direct Hopkins sum and Abbe's method to $10^{-11}$.

**Example check.** For the three-point source of the page, Lemma 2 gives $T = \frac13 (h_+ h_+^* + h_0 h_0^* + h_- h_-^*)$ of rank $3$, and the eigenvalues $\frac{13 \pm \sqrt{137}}{6}$ and $\frac23$ sum to $\operatorname{tr} T = 5$. By Theorem 1, three kernels give the exact image, as the table on the page shows.
