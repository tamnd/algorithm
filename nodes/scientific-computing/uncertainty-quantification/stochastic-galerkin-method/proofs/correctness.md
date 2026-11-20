---
title: The stochastic Galerkin system is the Galerkin projection, has a unique solution, and gives the best approximation in the energy norm
proves: [correctness, termination]
status: full
---

We assume exact arithmetic. The inputs $\xi_1, \ldots, \xi_d$ are independent and uniform on $[-1, 1]$, with $\xi_0 = 1$. The matrices $A_0, \ldots, A_d$ are real, symmetric and of size $n$, and $A(\xi) = \sum_{k=0}^{d} \xi_k A_k$ is positive definite for every $\xi \in [-1, 1]^d$. The basis $\Psi_\alpha$, $\alpha \in \Lambda$, is orthonormal: $\mathbb{E}[\Psi_\alpha \Psi_\beta] = \delta_{\alpha\beta}$, with $\Psi_0 = 1$. Let $V_p$ be the set of functions $v_p(\xi) = \sum_{\alpha \in \Lambda} v_\alpha \Psi_\alpha(\xi)$ with $v_\alpha \in \mathbb{R}^n$, and identify $v_p$ with the stacked vector $v = (v_\alpha)_{\alpha \in \Lambda}$. Then $K = \sum_k G_k \otimes A_k$ with $G_k[\beta, \alpha] = \mathbb{E}[\xi_k \Psi_\beta \Psi_\alpha]$, and $F = e_0 \otimes f$.

**Lemma 1 (the block system is the Galerkin projection).** A vector $c$ solves $K c = F$ if and only if $u_p = \sum_\alpha c_\alpha \Psi_\alpha$ satisfies $\mathbb{E}[(A(\xi) u_p(\xi) - f)\, \Psi_\beta(\xi)] = 0$ for every $\beta \in \Lambda$.

*Proof.* By linearity of expectation, $\mathbb{E}[A(\xi) u_p \Psi_\beta] = \sum_\alpha \sum_k \mathbb{E}[\xi_k \Psi_\beta \Psi_\alpha] A_k c_\alpha = (K c)_\beta$, the block row $\beta$ of $K c$. Also $\mathbb{E}[f \Psi_\beta] = \mathbb{E}[\Psi_0 \Psi_\beta] f$, which is $f$ for $\beta = 0$ and $0$ otherwise, so it is the block $F_\beta$. $\square$

**Lemma 2 (the energy identity).** For every $v$, $v^{\mathsf T} K v = \mathbb{E}[v_p(\xi)^{\mathsf T} A(\xi)\, v_p(\xi)]$, and $v^{\mathsf T} (I_P \otimes A_0)\, v = \mathbb{E}[v_p^{\mathsf T} A_0 v_p]$. In particular $K$ is symmetric positive definite, so $K c = F$ has exactly one solution and line L5 terminates with it.

*Proof.* Expand: $v^{\mathsf T} K v = \sum_{\alpha, \beta} \sum_k \mathbb{E}[\xi_k \Psi_\beta \Psi_\alpha]\, v_\beta^{\mathsf T} A_k v_\alpha = \mathbb{E}[\sum_k \xi_k\, v_p^{\mathsf T} A_k v_p] = \mathbb{E}[v_p^{\mathsf T} A(\xi) v_p]$. The second identity is the case where only $A_0$ appears, together with $\mathbb{E}[\Psi_\alpha \Psi_\beta] = \delta_{\alpha\beta}$. $K$ is symmetric because each $G_k$ and each $A_k$ is symmetric. If $v \ne 0$, then $v_p$ is a nonzero polynomial, so it is nonzero on a set of positive probability, and there $v_p^{\mathsf T} A(\xi) v_p > 0$; hence $v^{\mathsf T} K v > 0$. A positive definite matrix is nonsingular, and Gaussian elimination with partial pivoting on a nonsingular matrix finds a nonzero pivot in each of its finitely many steps. $\square$

**Lemma 3 (spectral equivalence).** If $(1 - \tau) A_0 \preceq A(\xi) \preceq (1 + \tau) A_0$ for every $\xi$ in the box, with $0 \le \tau < 1$, then $(1 - \tau)(I_P \otimes A_0) \preceq K \preceq (1 + \tau)(I_P \otimes A_0)$.

*Proof.* For every $\xi$, $(1 - \tau)\, v_p^{\mathsf T} A_0 v_p \le v_p^{\mathsf T} A(\xi) v_p \le (1 + \tau)\, v_p^{\mathsf T} A_0 v_p$. Take the expectation and use both identities of Lemma 2. $\square$

So the eigenvalues of $(I_P \otimes A_0)^{-1} K$ lie in $[1 - \tau, 1 + \tau]$, for every $p$ and $n$.

**Lemma 4 (best approximation in the energy norm).** Let $u(\xi) = A(\xi)^{-1} f$ be the exact solution and $\|w\|_E^2 = \mathbb{E}[w^{\mathsf T} A(\xi) w]$. Then $\|u - u_p\|_E = \min_{v_p \in V_p} \|u - v_p\|_E$.

*Proof.* The form $a(w, z) = \mathbb{E}[w^{\mathsf T} A(\xi) z]$ is an inner product on square integrable vector functions, because $A(\xi)$ is symmetric positive definite and bounded on the box. The exact solution satisfies $A(\xi) u(\xi) - f = 0$ for every $\xi$, so $a(u, v_p) = \mathbb{E}[f^{\mathsf T} v_p]$ for every $v_p \in V_p$. By Lemma 1, $a(u_p, v_p) = \mathbb{E}[f^{\mathsf T} v_p]$ as well. Subtract: $a(u - u_p, v_p) = 0$ for all $v_p \in V_p$, so $u_p$ is the $a$-orthogonal projection of $u$ onto $V_p$. For any $v_p$, $\|u - v_p\|_E^2 = \|u - u_p\|_E^2 + \|u_p - v_p\|_E^2 \ge \|u - u_p\|_E^2$ by the Pythagorean identity. $\square$

Under the hypothesis of Lemma 3, $\|w\|_E^2$ lies between $(1 - \tau)$ and $(1 + \tau)$ times $\mathbb{E}[w^{\mathsf T} A_0 w]$, so in that norm the error is at most $\sqrt{(1 + \tau)/(1 - \tau)}$ times the best error.

**Lemma 5 (one input is Gauss projection).** Let $d = 1$, and let $x_0, \ldots, x_p$ and $w_0, \ldots, w_p$ be the nodes and weights of the $(p+1)$ point Gauss-Legendre rule for the uniform law on $[-1, 1]$, so that $\sum_j w_j = 1$. Then $c_\alpha = \sum_j w_j\, \psi_\alpha(x_j)\, A(x_j)^{-1} f$ for $\alpha = 0, \ldots, p$.

*Proof.* Let $J = G_1$, the $(p+1) \times (p+1)$ matrix with $J[a, b] = \mathbb{E}[\xi \psi_a \psi_b]$. Let $Q[a, j] = \sqrt{w_j}\, \psi_a(x_j)$. The Gauss rule is exact for polynomials of degree $2p + 1$, so $\sum_j w_j \psi_a(x_j) \psi_b(x_j) = \delta_{ab}$, that is $Q Q^{\mathsf T} = I$; as $Q$ is square, $Q$ is orthogonal. The three term recurrence gives $\xi \psi_a = \sum_{b \le p} J[a, b] \psi_b$ for $a < p$, and $\xi \psi_p = \sum_{b \le p} J[p, b] \psi_b + b_{p+1} \psi_{p+1}$. The nodes are the zeros of $\psi_{p+1}$, so at every node $x_j \psi_a(x_j) = \sum_b J[a, b] \psi_b(x_j)$ for all $a$, which is $J Q = Q D$ with $D = \mathrm{diag}(x_j)$. Hence $J = Q D Q^{\mathsf T}$ and

$$K = I \otimes A_0 + J \otimes A_1 = (Q \otimes I)\, \big(I \otimes A_0 + D \otimes A_1\big)\, (Q^{\mathsf T} \otimes I).$$

The middle factor is block diagonal with blocks $A(x_j)$. So $c = (Q \otimes I)\, \mathrm{blockdiag}(A(x_j)^{-1})\, (Q^{\mathsf T} \otimes I)(e_0 \otimes f)$. The vector $Q^{\mathsf T} e_0$ has entries $\sqrt{w_j}\, \psi_0(x_j) = \sqrt{w_j}$. Therefore $c_a = \sum_j \sqrt{w_j} \psi_a(x_j)\, A(x_j)^{-1} \sqrt{w_j} f$, which is the claim. $\square$

**Theorem.** Under the assumptions above, the algorithm terminates, returns the unique coefficients of the Galerkin projection of $u$ onto $V_p$, and these give the best approximation of $u$ in $V_p$ in the energy norm. The returned mean is $\mathbb{E}[u_p]$ and the returned variances are those of the components of $u_p$.

*Proof.* Lines L1 to L4 are finite loops. Termination and uniqueness are Lemma 2, the projection property is Lemma 1, and the optimality is Lemma 4. For the moments, $\mathbb{E}[u_p] = \sum_\alpha c_\alpha \mathbb{E}[\Psi_\alpha \Psi_0] = c_0$, and $\mathbb{E}[(u_p)_i^2] = \sum_\alpha (c_\alpha)_i^2$ by orthonormality, so the variance of $(u_p)_i$ is $\sum_{\alpha \ne 0} (c_\alpha)_i^2$, which is line L6. $\blacksquare$
