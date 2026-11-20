---
title: The SVD clutter filter removes the best rank k1 approximation of the Casorati matrix, separates tissue exactly when tissue and blood are orthogonal in space and slow time, and is computed correctly through the real embedding of the Gram matrix
proves: [correctness]
status: full
---

Notation. $S$ is the $M \times N$ complex Casorati matrix (pixels by slow time), with the thin SVD $S = \sum_{j=1}^{N} \sigma_j u_j v_j^H$, $\sigma_1 \ge \dots \ge \sigma_N \ge 0$, orthonormal $u_j \in \mathbb{C}^M$ and orthonormal $v_j \in \mathbb{C}^N$ (if $M < N$, some $\sigma_j$ are zero and the $u_j$ for them are any completion; they do not appear in the results). For $0 \le k_1 \le k_2 \le N$ let $P = \sum_{j = k_1 + 1}^{k_2} v_j v_j^H$ (line L5) and $S_f = S P$ (line L6). The norm is the Frobenius norm.

**Lemma 1 (the filter is a band of singular components).** $S_f = \sum_{j = k_1 + 1}^{k_2} \sigma_j u_j v_j^H$, and $\|S_f\|^2 = \sum_{j = k_1 + 1}^{k_2} \sigma_j^2$.

*Proof.* $S v_l = \sum_j \sigma_j u_j (v_j^H v_l) = \sigma_l u_l$ by orthonormality, so $S P = \sum_{l = k_1+1}^{k_2} \sigma_l u_l v_l^H$. The terms are orthogonal in the Frobenius inner product, since $\operatorname{tr}((u_j v_j^H)^H u_l v_l^H) = (u_j^H u_l)(v_l^H v_j) = \delta_{jl}$, which gives the norm. $\square$

So with $k_2 = N$ the filter removes $S_{k_1} = \sum_{j \le k_1} \sigma_j u_j v_j^H$, and the removed energy is $\|S - S_f\|^2 = \sum_{j \le k_1} \sigma_j^2$.

**Theorem 1 (the removed part is the best rank k1 fit).** For every complex $M \times N$ matrix $R$ of rank at most $k_1$, $\|S - R\|^2 \ge \sum_{j > k_1} \sigma_j^2 = \|S - S_{k_1}\|^2$. This is the theorem of Eckart and Young (1936).

*Proof.* Weyl's inequality for singular values, $\sigma_{i + j - 1}(A + B) \le \sigma_i(A) + \sigma_j(B)$, follows from the Courant-Fischer minimax characterization of $\sigma_i$. Apply it with $A = S - R$, $B = R$ and $j = k_1 + 1$: since $\sigma_{k_1 + 1}(R) = 0$, $\sigma_{i + k_1}(S) \le \sigma_i(S - R)$ for every $i \ge 1$. Squaring and summing over $i$ gives $\|S - R\|^2 = \sum_i \sigma_i(S - R)^2 \ge \sum_{i} \sigma_{i + k_1}(S)^2$. By Lemma 1 the bound is attained by $R = S_{k_1}$. $\square$

So the filter models the tissue as the rank $k_1$ matrix closest to the data, and the blood and noise as the rest. This is a statement about energy. It does not say that the removed part is tissue; Theorem 2 gives a condition under which it is.

**Theorem 2 (exact separation).** Let $S = T + B$ where $T$ has rank $k_1$ and (a) $T^H B = 0$, that is the columns of $T$ and of $B$ are orthogonal in pixel space, and (b) $T B^H = 0$, that is the rows of $T$ and of $B$ are orthogonal in slow time. If the smallest nonzero singular value of $T$ is larger than the largest singular value of $B$, then the filter with $k_2 = N$ returns $S_f = B$.

*Proof.* Let $T = \sum_{j=1}^{k_1} \tau_j a_j x_j^H$ and $B = \sum_l \beta_l b_l y_l^H$ be SVDs. Condition (a) gives $a_j^H b_l = 0$ for all $j, l$ (multiply $T^H B = 0$ by $x_j$ on the left and $y_l$ on the right, after dividing by $\tau_j \beta_l > 0$). Condition (b) gives $x_j^H y_l = 0$ in the same way. So the sets $\{a_j\} \cup \{b_l\}$ and $\{x_j\} \cup \{y_l\}$ are orthonormal, and $S = \sum_j \tau_j a_j x_j^H + \sum_l \beta_l b_l y_l^H$ is an SVD of $S$. Since every $\tau_j$ exceeds every $\beta_l$, the first $k_1$ right singular vectors span the same space as the $x_j$ (if some singular values are equal inside the tissue part or inside the blood part, the choice of basis inside that part does not change the span). So $I - P$ is the orthogonal projector onto the span of the $x_j$, and $S P = S - T(I - P) - B(I - P) = S - T = B$, because $T(I - P) = T$ and $B x_j = 0$ by (b). $\square$

Both conditions are needed. Disjoint supports in space give (a), and Doppler frequencies on disjoint sets of DFT bins of length $N$ give (b). If tissue and blood share pixels and slow time content, the singular vectors mix the two, and part of the blood is removed with the tissue. A Doppler frequency filter would need (b) and a frequency gap; the SVD filter needs (a) and (b) and an energy gap, but no frequency gap: Lemma 3 shows that it does not see frequencies as such.

**Lemma 2 (the real embedding).** For a Hermitian $N \times N$ matrix $C = A + iB$ ($A$ real symmetric, $B$ real antisymmetric), let $E(C) = \begin{pmatrix} A & -B \\ B & A \end{pmatrix}$. Then $E$ is a real algebra homomorphism, $E(C)$ is real symmetric, every eigenvalue $\lambda$ of $C$ is an eigenvalue of $E(C)$ with twice the multiplicity, and for an orthogonal projector $P$ onto an invariant subspace of $C$, $E(P)$ is the orthogonal projector onto the sum of the corresponding eigenspaces of $E(C)$. In particular $\operatorname{Re} P$ and $\operatorname{Im} P$ are the left blocks of that real projector.

*Proof.* Identify $z = p + iq \in \mathbb{C}^N$ with $\hat z = (p, q) \in \mathbb{R}^{2N}$. A direct computation gives $\widehat{C z} = E(C) \hat z$, and $E(C_1 C_2) = E(C_1) E(C_2)$, $E(C^H) = E(C)^T$. If $C z = \lambda z$ with real $\lambda$, then $E(C) \hat z = \lambda \hat z$ and $E(C) \widehat{iz} = \lambda \widehat{iz}$, with $\widehat{iz} = (-q, p)$ orthogonal to $\hat z$. An orthonormal eigenbasis $z_1, \dots, z_N$ of $C$ gives the orthonormal basis $\hat z_j, \widehat{i z_j}$ of $\mathbb{R}^{2N}$ (the real inner product of $\hat z$ and $\hat w$ is $\operatorname{Re}(z^H w)$), so the spectrum of $E(C)$ is that of $C$ with doubled multiplicity. $E(P)$ is real symmetric and idempotent because $P$ is Hermitian and idempotent, and it maps $\hat z_j$ and $\widehat{i z_j}$ to themselves or to 0 as $P$ maps $z_j$. $\square$

The code applies Lemma 2 to $C = S^H S$ (line L2), whose eigenvalues are $\sigma_j^2$ with eigenvectors $v_j$. If $\sigma_{k_1} > \sigma_{k_1 + 1}$ and $\sigma_{k_2} > \sigma_{k_2 + 1}$, the real eigenvectors number $2 k_1 + 1$ to $2 k_2$ of $E(C)$ in descending order span exactly the embedding of the span of $v_{k_1 + 1}, \dots, v_{k_2}$, whatever real basis the eigensolver returns inside a pair. Their real projector is $E(P)$, and line L5 reads $P$ from its left blocks. If a cut falls inside a group of equal singular values, $P$ is not defined by the data; this is a property of the problem, not of the method of computation.

**Lemma 3 (invariances).** Let $\Pi$ be an $M \times M$ unitary matrix (for example a permutation of the pixels times a common phase) and $W$ an $N \times N$ unitary matrix (for example the diagonal matrix $\operatorname{diag}(e^{i \omega t})$, a shift of every Doppler frequency by $\omega$). Then the filter maps $\Pi S W$ to $\Pi S_f W$.

*Proof.* $\Pi S W = \sum_j \sigma_j (\Pi u_j)(W^H v_j)^H$ is an SVD with the same singular values, and the right singular vectors are $W^H v_j$. So $P' = W^H P W$ and $\Pi S W P' = \Pi S P W = \Pi S_f W$. $\square$

So the result depends neither on the order of the pixels nor on a common shift of the Doppler frequencies. A tissue echo that moves fast is removed as long as it is strong and coherent in space, and blood that is slow is kept as long as it is weak and incoherent in space.

**Theorem 3 (cost).** Lines L1 to L8 cost $O(M N^2 + N^3)$ operations in the real-RAM model with an eigensolver that is counted as $O(N^3)$ to working precision, and $O(M N + N^2)$ space.

*Proof.* Line L2 forms $N^2$ inner products of length $M$. Line L3 is an eigenproblem of size $2N$, which a fixed number of Jacobi sweeps or a tridiagonal QR method solves in $O(N^3)$. Line L5 forms $N^2$ entries, each a sum of at most $2N$ products, $O(N^3)$. Line L6 is an $M \times N$ by $N \times N$ product, $O(M N^2)$. Line L7 is $O(M N)$. The matrices $S$, $S_f$, $C$ and $P$ need $O(M N + N^2)$ space. $\square$
