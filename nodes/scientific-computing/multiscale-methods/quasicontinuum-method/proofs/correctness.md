---
title: The energy of the quasicontinuum chain, its exact limit, the patch test and the Newton iteration
proves: [correctness]
status: full
---

We use the chain of the page. Atoms $0, \dots, N - 1$ have reference sites $X_i = i a$. The bonds are $(i, i+1)$ and $(i, i+2)$, with a pair potential $\varphi$ that is twice continuously differentiable on $(0, \infty)$ and a scale factor $s_b$ per bond. The repatoms $R = \{r_0 < r_1 < \dots < r_{n-1}\}$ contain $0$ and $N - 1$, the nonlocal set $A \subset R$ contains $0$ and $N - 1$, and every bond with $s_b \ne 1$ has both ends in $A$. The interpolation is $y = T z$ (line L1), the elements are $e_k = (r_k, r_{k+1})$ with $n_k = r_{k+1} - r_k$ and $F_k = (z_{k+1} - z_k) / (n_k a)$, and $W(F) = \varphi(F a) + \varphi(2 F a)$. We assume exact arithmetic.

**Definition (atom energies).** For a nonlocal atom $i$, $\varepsilon_i = \frac12 \sum_{b \ni i} s_b \varphi(\ell_b)$, where $\ell_b = y_j - y_i$ is the length of the bond $b = (i, j)$ at $y = T z$. For a local atom $i$ strictly inside the element $e_k$, $\varepsilon_i = W(F_k)$. For a local repatom $r_k$, $\varepsilon_i = \frac12 (W(F_{k-1}) + W(F_k))$; it has two elements because the ends are nonlocal.

**Lemma 1 (the weights).** With $c_b$ and $w_k$ of line L2, $\sum_i \varepsilon_i = \sum_b c_b s_b \varphi(\ell_b) + \sum_k w_k W(F_k) = E_{\mathrm{QCE}}(z)$.

*Proof.* Split the sum over atoms into nonlocal and local atoms. The nonlocal part is $\sum_{i \in A} \frac12 \sum_{b \ni i} s_b \varphi(\ell_b)$. Exchange the two sums: the bond $b$ appears once for each of its ends in $A$, with the factor $\frac12$, so its weight is $\frac12 \#(b \cap A) = c_b$. In the local part, the term $W(F_k)$ comes from the $n_k - 1$ atoms strictly inside $e_k$, each with weight $1$, and from each end of $e_k$ that is a local repatom, with weight $\frac12$. Each end of $e_k$ is in $A$ or is a local repatom, so the weight is $n_k - 1 + \frac12 (2 - \#(e_k \cap A)) = n_k - \frac12 \#(e_k \cap A) = w_k$. $\square$

**Lemma 2 (the exact limit).** If $R = A = \{0, \dots, N - 1\}$, then $T = I$ and $E_{\mathrm{QCE}}(z) = E(z)$ for all $z$.

*Proof.* Every atom is a repatom, so line L1 gives $y_i = z_i$. Both ends of every bond are in $A$, so $c_b = 1$. Every element has $n_k = 1$ and two ends in $A$, so $w_k = 1 - 1 = 0$. Then $E_{\mathrm{QCE}}(z) = \sum_b s_b \varphi(z_j - z_i) = E(z)$. $\square$

So the iteration of lines L3 to L9 is Newton's method on the full energy in this case, and QC can be refined to full atomistics.

**Lemma 3 (the patch test for the force-based form).** Let $s_b = 1$ for all bonds and let $z_k = F a r_k$ for some $F > 0$, so that $y = F X$. Then the QCF residual is zero at every repatom $r_k$ with $2 \le r_k \le N - 3$.

*Proof.* For a nonlocal repatom $i$ with $2 \le i \le N - 3$, the atoms $i \pm 1$ and $i \pm 2$ exist. At $y = F X$ the bonds to $i + 1$ and $i - 1$ have the same length $F a$, and their forces on $i$ are $\varphi'(F a)$ and $-\varphi'(F a)$; the same holds for $i \pm 2$ with $\varphi'(2 F a)$. So the atomistic force on $i$ is zero. For a local repatom $r_k$, the local energy $\sum_m n_m W(F_m)$ has the derivative $-n_k W'(F_k) / (n_k a) + n_{k-1} W'(F_{k-1}) / (n_{k-1} a) = (W'(F_{k-1}) - W'(F_k)) / a$ with respect to $z_k$, and $F_{k-1} = F_k = F$, so it is zero. $\square$

**Lemma 4 (ghost forces of the energy-based form).** Let all atoms be repatoms, let the nonlocal atoms be $i \le p$ and the local atoms $p + 1 \le i \le q$ inside a long chain, with $s_b = 1$ and $y = F X$. Then the force $f_k = -\partial E_{\mathrm{QCE}} / \partial y_k$ is $-\frac12 \varphi'(2 F a)$ at $k = p - 1$, $\frac12 \varphi'(2 F a)$ at $k = p$ and $k = p + 1$, $-\frac12 \varphi'(2 F a)$ at $k = p + 2$, and zero at other atoms at a distance of more than two from both interfaces.

*Proof.* Shift the indices so that $p = 0$. With $n_k = 1$, the element $(i, i + 1)$ contributes $w_i (\varphi(\ell) + \varphi(2 \ell))$ with $\ell = y_{i+1} - y_i$. The coefficient of $\varphi(y_{i+1} - y_i)$ is $c_{(i,i+1)} + w_i$, which is $1 + 0$ for $i \le -1$, $\frac12 + \frac12$ for $i = 0$, and $0 + 1$ for $i \ge 1$. So the nearest neighbor terms are those of $E$, and their forces cancel at $y = F X$ as in Lemma 3. The other terms are $\sum_i c_i \varphi(y_{i+2} - y_i)$ with $c_i = c_{(i, i+2)}$ equal to $1$ for $i \le -2$, $\frac12$ for $i \in \{-1, 0\}$ and $0$ for $i \ge 1$, and $\sum_i w_i \varphi(2 (y_{i+1} - y_i))$. At $y = F X$ each argument is $2 F a$. The derivative of the first sum with respect to $y_k$ is $(c_{k-2} - c_k) \varphi'(2 F a)$, and that of the second is $2 (w_{k-1} - w_k) \varphi'(2 F a)$. So $f_k = \varphi'(2 F a) (c_k - c_{k-2} + 2 w_k - 2 w_{k-1})$. Insert the values: $k = -1$ gives $\frac12 - 1 + 0 - 0 = -\frac12$; $k = 0$ gives $\frac12 - 1 + 1 - 0 = \frac12$; $k = 1$ gives $0 - \frac12 + 2 - 1 = \frac12$; $k = 2$ gives $0 - \frac12 + 2 - 2 = -\frac12$; $k \le -2$ gives $1 - 1 + 0 - 0 = 0$; $k \ge 3$ gives $0 - 0 + 2 - 2 = 0$. $\square$

Lemma 4 shows that QCE fails the patch test whenever $\varphi'(2 F a) \ne 0$, and with nearest neighbors only the second neighbor terms are absent, so the forces are zero.

**Lemma 5 (the Newton iteration).** Let $G(z)$ be the gradient of $E_{\mathrm{QCE}}$ (or the QCF residual) restricted to the free repatoms, with the fixed repatoms held at their values. Lines L5 and L6 compute $G$ and its Jacobian $K$ exactly. If $G(z^*) = 0$, $K(z^*)$ is nonsingular and $K$ is Lipschitz near $z^*$, then for a start close enough to $z^*$ the iterates of lines L4 to L8 converge to $z^*$ quadratically, and a returned $z$ satisfies $\max |G(z)| < \mathrm{tol}$.

*Proof.* The energy is a sum of terms $\varphi(\ell)$ with $\ell$ linear in $z$ (through $T$), and of terms $W(F_k)$ with $F_k$ linear in $z$. By the chain rule, the gradient of $c\, \varphi(\ell)$ is $c\, \varphi'(\ell)\, \nabla_z \ell$, and its Hessian is $c\, \varphi''(\ell)\, \nabla_z \ell\, \nabla_z \ell^{\mathsf T}$, because $\ell$ is linear in $z$. For a bond $(i, j)$, $\nabla_z \ell = T^{\mathsf T}(e_j - e_i)$, which is what line L5 adds for the bonds and line L6 for their Hessians; the elements are the same with $\nabla_z F_k = (e_{k+1} - e_k) / (n_k a)$. For QCF the residual rows are the same expressions restricted to the rows of the nonlocal or local repatoms, so $K$ is again the exact Jacobian. Lines L7 and L8 are then the Newton step $z \leftarrow z - K^{-1} G$ on the free variables, and the local quadratic convergence is the standard theorem for Newton's method under the stated hypotheses. The loop returns only when the test of line L9 holds. $\square$

**Theorem.** The procedure returns a stationary point of $E_{\mathrm{QCE}}$ (or a zero of the QCF residual) on the free repatoms whenever its Newton iteration converges. That point is the exact atomistic equilibrium when every atom is a nonlocal repatom. For uniform deformations, QCF reproduces the exact zero forces, and QCE has the ghost forces of Lemma 4 when second neighbor bonds are present.

*Proof.* Lemma 5 gives the first claim, Lemma 2 the second, and Lemmas 3 and 4 the third. $\blacksquare$
