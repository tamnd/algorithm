---
title: Jacobi rotations reduce the off-diagonal norm and converge to the eigenvalues
proves: [correctness, termination]
status: full
---

Notation of the page: $A = A^T \in \mathbb{R}^{n \times n}$, $\operatorname{off}(A)^2 = \sum_{i \ne j} a_{ij}^2$, $\|\cdot\|_F$ the Frobenius norm, and $J = J(p, q, \theta)$ the rotation equal to the identity except $J_{pp} = J_{qq} = c$, $J_{pq} = s$, $J_{qp} = -s$, with $c = \cos\theta$, $s = \sin\theta$. One rotation step is $B = J^T A J$. Exact arithmetic unless stated.

**Lemma 1 (the rotation zeroes $a_{pq}$).** Let $a_{pq} \ne 0$, $\tau = (a_{qq} - a_{pp}) / (2 a_{pq})$, let $t$ be the root of smaller modulus of $t^2 + 2\tau t - 1 = 0$, that is $t = \operatorname{sign}(\tau) / (|\tau| + \sqrt{1 + \tau^2})$ with $\operatorname{sign}(0) = 1$, and $c = 1/\sqrt{1 + t^2}$, $s = t c$. Then $b_{pq} = b_{qp} = 0$, $b_{pp} = a_{pp} - t a_{pq}$, $b_{qq} = a_{qq} + t a_{pq}$, and $|\theta| \le \pi/4$.

*Proof.* Only rows and columns $p$ and $q$ change. The $2 \times 2$ block is
$$\begin{pmatrix} b_{pp} & b_{pq} \\ b_{qp} & b_{qq} \end{pmatrix} = \begin{pmatrix} c & -s \\ s & c \end{pmatrix} \begin{pmatrix} a_{pp} & a_{pq} \\ a_{pq} & a_{qq} \end{pmatrix} \begin{pmatrix} c & s \\ -s & c \end{pmatrix},$$
so $b_{pq} = a_{pq}(c^2 - s^2) + cs(a_{pp} - a_{qq})$. With $t = s/c$, $b_{pq} = 0$ if and only if $a_{pq}(1 - t^2) + t(a_{pp} - a_{qq}) = 0$, that is $t^2 + 2\tau t - 1 = 0$. The two roots have product $-1$, so the smaller one has $|t| \le 1$ and $|\theta| = |\arctan t| \le \pi/4$. Next, $b_{pp} = c^2 a_{pp} - 2cs\,a_{pq} + s^2 a_{qq}$; with $s^2 (a_{qq} - a_{pp}) = 2 s^2 \tau a_{pq}$ and $2\tau t = 1 - t^2$, this is $a_{pp} + c^2 a_{pq}(t(1 - t^2) - 2t) = a_{pp} - t a_{pq}$, since $c^2(1 + t^2) = 1$. The formula for $b_{qq}$ follows from the invariance of the trace of the block. $\square$

**Lemma 2 (the off-diagonal norm drops by $2 a_{pq}^2$).** $\operatorname{off}(B)^2 = \operatorname{off}(A)^2 - 2 a_{pq}^2$.

*Proof.* $\|B\|_F = \|A\|_F$ since $J$ is orthogonal. For $r \ne p, q$ the pair $(b_{rp}, b_{rq})$ is a rotation of $(a_{rp}, a_{rq})$, so $b_{rp}^2 + b_{rq}^2 = a_{rp}^2 + a_{rq}^2$, and entries outside rows and columns $p, q$ do not change. So the only change of the off-diagonal sum is in the $(p, q)$ block: the Frobenius norm of the $2 \times 2$ block is kept, and its off-diagonal part goes from $2 a_{pq}^2$ to $0$. So $\sum_i b_{ii}^2 = \sum_i a_{ii}^2 + 2 a_{pq}^2$, and the claim follows from $\operatorname{off}^2 = \|\cdot\|_F^2 - \sum_i (\cdot)_{ii}^2$. $\square$

**Theorem 1 (classical Jacobi converges linearly).** If each step rotates on an entry of largest modulus, then $\operatorname{off}(B)^2 \le (1 - 1/N) \operatorname{off}(A)^2$ with $N = n(n-1)/2$. So after $k$ steps $\operatorname{off}(A^{(k)}) \le (1 - 1/N)^{k/2} \operatorname{off}(A)$.

*Proof.* $\operatorname{off}(A)^2 = 2 \sum_{p < q} a_{pq}^2 \le 2N \max_{p<q} a_{pq}^2$, so $2 a_{pq}^2 \ge \operatorname{off}(A)^2 / N$ for the largest entry; apply Lemma 2. $\square$

**Theorem 2 (the diagonal converges to the eigenvalues).** Let $A^{(k)} = V_k^T A V_k$ with $V_k$ orthogonal (the product of the rotations), and let $\operatorname{off}(A^{(k)}) \to 0$. Then, with the eigenvalues $\lambda_1 \ge \dots \ge \lambda_n$ of $A$ and the sorted diagonal $d^{(k)}_{[1]} \ge \dots \ge d^{(k)}_{[n]}$,
$$\max_i |d^{(k)}_{[i]} - \lambda_i| \le \operatorname{off}(A^{(k)}),$$
and the columns of $V_k$ have residuals $\|A v^{(k)}_i - a^{(k)}_{ii} v^{(k)}_i\|_2 \le \operatorname{off}(A^{(k)})$.

*Proof.* $A^{(k)} = D_k + E_k$ with $D_k$ its diagonal and $E_k$ symmetric with $\|E_k\|_2 \le \|E_k\|_F = \operatorname{off}(A^{(k)})$. By [Weyl's inequality](/weyls-inequality/), the sorted eigenvalues of $A^{(k)}$, which are those of $A$, differ from the sorted eigenvalues of $D_k$, its diagonal entries, by at most $\|E_k\|_2$. For the residual, $A V_k = V_k A^{(k)}$, so $A v_i^{(k)} - a^{(k)}_{ii} v_i^{(k)} = V_k E_k e_i$, whose norm is the norm of column $i$ of $E_k$. $\square$

**Theorem 3 (cyclic Jacobi converges, and fast).** For the cyclic-by-row order with $|\theta| \le \pi/4$ (Lemma 1), $\operatorname{off}(A^{(k)}) \to 0$ (Forsythe and Henrici 1960). If the eigenvalues are distinct with minimum gap $\delta$, the convergence is ultimately quadratic per sweep: once $\operatorname{off}$ is small compared with $\delta$, one sweep maps $\operatorname{off}$ to at most a constant times $\operatorname{off}^2 / \delta$ (Henrici 1958; Wilkinson 1962), and Schönhage (1964) extended quadratic convergence to multiple eigenvalues. These are cited results; the proofs are long and not repeated here. The test file measures the ratio $\operatorname{off}_{k+1} / \operatorname{off}_k^2$ and finds it bounded.

**Termination of the implementation.** The sweep loop of line L2 runs at most `max_sweeps` times. With the threshold test of line L4, a sweep that performs no rotation ends the loop (line L7). Under Theorem 3 every off-diagonal entry tends to zero, while for a matrix with $\operatorname{off}(A^{(k)})$ small the diagonal entries approach the eigenvalues. If no eigenvalue is zero, $\sqrt{|a_{pp} a_{qq}|}$ stays bounded away from zero, so every entry eventually falls below its threshold and the sweep loop stops. If some eigenvalues are zero, the entries still go to zero; in floating point they reach exact zero or underflow, and the bound `max_sweeps` guarantees a stop in every case.

**Correctness at the stop.** When the loop stops at line L7, every off-diagonal entry satisfies $|a_{pq}| \le \mathrm{tol} \sqrt{|a_{pp} a_{qq}|}$, so $\operatorname{off}(A^{(k)}) \le \mathrm{tol} \, \sqrt{\sum_{p \ne q} |a_{pp} a_{qq}|} \le \mathrm{tol} \, n \max_i |a_{ii}| \le \mathrm{tol} \, n \|A\|_2$, and Theorem 2 gives the error of the returned eigenvalues and the residuals of the returned vectors.

**Floating point.** Each rotation is computed in floating point as $\hat B = J^T (A + E) J$ with $\|E\|_F \le c\, n u \|A\|_F$ and $J$ exactly orthogonal, up to a small error in $\hat V$ (Wilkinson 1965, Chapter 3 and Chapter 5). A full run of $s$ sweeps is therefore normwise backward stable with an error of order $s n^3 u \|A\|_F$ in this crude bound, and the observed error is of order $u \|A\|$. For a positive definite $A = D H D$ with $D$ diagonal and $H$ with unit diagonal, Demmel and Veselić (1992) proved that the computed eigenvalues have relative errors of order $u \max_k \kappa(H_k)$, where $H_k$ is the scaled form of the iterate $A^{(k)}$; they observed that $\max_k \kappa(H_k)$ is not much larger than $\kappa(H)$. This is a stronger result than any normwise bound when $D$ is strongly graded.
