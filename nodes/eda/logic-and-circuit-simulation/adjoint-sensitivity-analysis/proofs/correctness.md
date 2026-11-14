---
title: One adjoint solve gives the derivative of an output with respect to every parameter
proves: [correctness]
status: full
---

Let a linear resistive circuit have nodes $0, \ldots, n$ with ground $0$, and let its modified nodal analysis system be $M(p)\, x = z(p)$, where $x = (e_1, \ldots, e_n, j_1, \ldots, j_m)$ and $p = (p_1, \ldots, p_P)$ are the parameters of the elements. The stamps are those of the MNA page: a conductance $G$ from $a$ to $b$ adds $G$ at $(a, a)$ and $(b, b)$ and $-G$ at $(a, b)$ and $(b, a)$; a current source $s$ from $a$ to $b$ adds $-s$ to $z_a$ and $s$ to $z_b$; a voltage source with current row $r$ adds $1$ at $(a, r)$ and $(r, a)$, $-1$ at $(b, r)$ and $(r, b)$, and $s$ to $z_r$; a VCCS of gain $g$ from $a$ to $b$ controlled by $e_c - e_d$ adds $g$ at $(a, c)$ and $(b, d)$ and $-g$ at $(a, d)$ and $(b, c)$. Entries in a row or column of ground are dropped, and $x_0 = \lambda_0 = 0$. Let $\varphi = c^{\mathsf T} x$ be an output.

**Lemma 1 (differentiability).** If $M(p_0)$ is nonsingular, then on a neighbourhood of $p_0$ the solution $x(p) = M(p)^{-1} z(p)$ is continuously differentiable, and

$$M\, \frac{\partial x}{\partial p_k} = \frac{\partial z}{\partial p_k} - \frac{\partial M}{\partial p_k}\, x.$$

*Proof.* Every entry of $M$ and $z$ is a polynomial in a conductance, a gain or a source value, or $1/R$ for a resistance $R > 0$, so it is continuously differentiable in $p$. The determinant is continuous, so $M(p)$ stays nonsingular near $p_0$, and the entries of $M^{-1}$ are rational functions of the entries of $M$ with nonzero denominator $\det M$ (Cramer's rule). So $x$ is continuously differentiable. Differentiating the identity $M(p)\, x(p) = z(p)$ with the product rule gives the displayed equation. $\square$

**Theorem 1 (the adjoint identity).** Let $\lambda$ solve $M^{\mathsf T} \lambda = c$. Then for every parameter $p_k$,

$$\frac{\partial \varphi}{\partial p_k} = \lambda^{\mathsf T}\Big(\frac{\partial z}{\partial p_k} - \frac{\partial M}{\partial p_k}\, x\Big).$$

So one solve with $M^{\mathsf T}$ for each output gives the derivative with respect to all parameters.

*Proof.* $\partial \varphi / \partial p_k = c^{\mathsf T} \partial x / \partial p_k = (M^{\mathsf T} \lambda)^{\mathsf T} \partial x / \partial p_k = \lambda^{\mathsf T} M\, \partial x / \partial p_k$, and Lemma 1 replaces $M\, \partial x / \partial p_k$. The vector $\lambda$ does not depend on $k$. $\square$

**Lemma 2 (the table).** With $x_0 = \lambda_0 = 0$, Theorem 1 gives:

1. conductance $G$ from $a$ to $b$: $\partial \varphi / \partial G = -(\lambda_a - \lambda_b)(x_a - x_b)$;
2. resistor $R$ from $a$ to $b$: $\partial \varphi / \partial R = (\lambda_a - \lambda_b)(x_a - x_b)/R^2$;
3. current source $s$ from $a$ to $b$: $\partial \varphi / \partial s = -(\lambda_a - \lambda_b)$;
4. voltage source $s$ with current row $r$: $\partial \varphi / \partial s = \lambda_r$;
5. VCCS of gain $g$ from $a$ to $b$ controlled by $e_c - e_d$: $\partial \varphi / \partial g = -(\lambda_a - \lambda_b)(x_c - x_d)$.

*Proof.* (1) $\partial z / \partial G = 0$, and $\partial M / \partial G$ is the stamp with $G$ replaced by $1$. So $(\partial M / \partial G)\, x$ has $x_a - x_b$ in row $a$ and $-(x_a - x_b)$ in row $b$, and $\lambda^{\mathsf T}$ of it is $(\lambda_a - \lambda_b)(x_a - x_b)$; dropping a ground row or column agrees with $x_0 = \lambda_0 = 0$. (2) $G = 1/R$ and $dG/dR = -1/R^2$, so the chain rule applied to (1) gives the formula. (3) $\partial M / \partial s = 0$ and $\partial z / \partial s$ has $-1$ in row $a$ and $1$ in row $b$, so the product is $-\lambda_a + \lambda_b$. (4) $\partial M / \partial s = 0$ and $\partial z / \partial s$ is the unit vector of row $r$. (5) $\partial z / \partial g = 0$, and $(\partial M / \partial g)\, x$ has $x_c - x_d$ in row $a$ and $-(x_c - x_d)$ in row $b$, so $\lambda^{\mathsf T}$ of it is $(\lambda_a - \lambda_b)(x_c - x_d)$. $\square$

**Lemma 3 (the adjoint network).** $M^{\mathsf T}$ is the MNA matrix of the adjoint network, the same netlist with every independent source set to zero and every VCCS from $a$ to $b$ controlled by $e_c - e_d$ replaced by a VCCS of the same gain from $c$ to $d$ controlled by $e_a - e_b$. The right side $c$ is the excitation of that network by independent sources: $c = u_k$ (the unit vector of node $k$) is a current source of 1 A from ground into node $k$, and $c = u_r$ for the current row $r$ of a voltage source is the value 1 V of that source.

*Proof.* $M$ is the sum of the stamps of the elements, and the transpose of a sum is the sum of the transposes. The stamp of a conductance and the stamp of a voltage source are symmetric matrices. The VCCS stamp has $g$ at $(a, c)$ and $(b, d)$ and $-g$ at $(a, d)$ and $(b, c)$; its transpose has $g$ at $(c, a)$ and $(d, b)$ and $-g$ at $(d, a)$ and $(c, b)$, which is the stamp of a VCCS from $c$ to $d$ controlled by $e_a - e_b$. Independent sources do not enter $M$. A current source of 1 A from ground to node $k$ adds $1$ to row $k$ of the right side, and a voltage source of value 1 V adds $1$ to its own row. $\square$

**Theorem 2 (Tellegen form).** Let $(v, i)$ be the branch voltages and currents of the original circuit, $(\hat v, \hat\imath)$ those of the adjoint network of Lemma 3 written as a circuit on the same graph, and let a parameter change from $p_k$ to $p_k + \delta p_k$ change the original solution by $(\delta v, \delta i)$. Then

$$\sum_b \big(\delta v_b\, \hat\imath_b - \hat v_b\, \delta i_b\big) = 0.$$

*Proof.* The perturbed circuit and the original circuit have the same graph, so $\delta v$ satisfies Kirchhoff's voltage law and $\delta i$ satisfies Kirchhoff's current law, because both laws are linear. The adjoint network has the same graph as well, so $\hat v$ satisfies KVL and $\hat\imath$ satisfies KCL. Tellegen's theorem, which needs only KCL for one vector and KVL for the other on the same graph, gives $\sum_b \delta v_b\, \hat\imath_b = 0$ and $\sum_b \hat v_b\, \delta i_b = 0$. Subtracting gives the claim. $\square$

The terms of this sum for an element that was not changed vanish by the choice of the adjoint element. For a resistor with $i = G v$ and adjoint $\hat\imath = G \hat v$, the term is $\delta v\, G \hat v - \hat v\, G \delta v = 0$. For a changed conductance, $\delta i = G \delta v + \delta G\, v$ to first order, so its term is $-\hat v\, v\, \delta G$, which is the first row of Lemma 2 with $\hat v = \lambda_a - \lambda_b$ and $v = x_a - x_b$. The other rows follow in the same way. This is the form in which Director and Rohrer stated the method; Theorem 1 is the same statement in matrix form.

**Theorem 3 (cost).** For a circuit with $N = n + m$ unknowns, $P$ parameters and $K$ outputs, the algorithm uses one LU factorization of $M$, one solve for $x$ and $K$ solves with $M^{\mathsf T}$, and $O(1)$ further operations per parameter and output.

*Proof.* Lines L2 and L3 run once. For each output, line L4 runs once. If $P_r M = L U$ with a permutation $P_r$, then $M^{\mathsf T} = U^{\mathsf T} L^{\mathsf T} P_r$, so $M^{\mathsf T} \lambda = c$ is solved by a forward substitution with the lower triangular $U^{\mathsf T}$, a back substitution with the upper triangular $L^{\mathsf T}$, and the permutation $P_r^{\mathsf T}$, with no new factorization. Each row of Lemma 2 reads at most four entries of $x$ and $\lambda$ and does a fixed number of arithmetic operations. $\square$

**Theorem 4 (correctness of the algorithm).** If $M$ is nonsingular, ADJOINT-SENSITIVITY returns $\varphi = c^{\mathsf T} x$ and, for every element $k$, $s_k = \partial \varphi / \partial p_k$. If $M$ is singular, the factorization of line L2 fails and the code reports it.

*Proof.* Lines L1 to L3 compute the solution $x$ of the MNA system, since the stamps are those of the MNA page and LU with partial pivoting solves a nonsingular system exactly in exact arithmetic. Line L4 computes $\lambda$ with $M^{\mathsf T} \lambda = c$ by Theorem 3. Line L5 is the definition of $\varphi$. Line L7 evaluates the formula of Lemma 2 for the kind of element $k$, which equals $\partial \varphi / \partial p_k$ by Theorem 1. If $M$ is singular, Gaussian elimination with partial pivoting meets a column with no nonzero pivot candidate, and the factorization raises the error. $\blacksquare$
