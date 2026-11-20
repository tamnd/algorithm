---
title: Invariants of the Pipe-Menon density compensation iteration
proves: [correctness]
status: full
---

The setting is that of the algorithm. There are $m$ sample positions $k_1, \ldots, k_m$, and a kernel $C(r) \ge 0$ with $C(0) > 0$ and $C(r) = 0$ for $r \ge W/2$. The matrix $C$ has the entries $C_{ij} = C(|k_i - k_j|)$, so it is symmetric, nonnegative, and has the diagonal $C(0)$. The iteration is $w^{(0)} = \mathbf{1}$ (line L2) and

$$w^{(t+1)}_i = \frac{w^{(t)}_i}{d^{(t)}_i}, \qquad d^{(t)} = C w^{(t)} \quad \text{(lines L4 and L5)}.$$

Line L1 only stores the nonzero entries of each row of $C$, so line L4 computes $C w$ exactly.

This page does not claim that the iteration converges. Pipe and Menon give no convergence proof, and examples exist where the system $C w = \mathbf{1}$ has no positive solution. The statements below are what holds for every input.

**Theorem 1 (the iterates are well defined and positive).** For every $t \ge 0$ and every $i$, $w^{(t)}_i > 0$ and $d^{(t)}_i \ge C(0)\, w^{(t)}_i > 0$. For $t \ge 1$, also $w^{(t)}_i \le 1/C(0)$.

*Proof.* By induction on $t$. The start $w^{(0)} = \mathbf{1}$ is positive. If $w^{(t)} > 0$, every term $C_{ij} w^{(t)}_j$ is nonnegative, and the diagonal term is $C(0) w^{(t)}_i > 0$. So $d^{(t)}_i \ge C(0) w^{(t)}_i > 0$, line L5 does not divide by zero, and $w^{(t+1)}_i = w^{(t)}_i / d^{(t)}_i > 0$. The same inequality gives $w^{(t+1)}_i \le w^{(t)}_i / (C(0) w^{(t)}_i) = 1/C(0)$. $\square$

**Theorem 2 (fixed points).** A vector $w$ with positive entries satisfies $w_i = w_i / (C w)_i$ for all $i$ if and only if $C w = \mathbf{1}$.

*Proof.* Since $w_i > 0$, the equation $w_i = w_i / (C w)_i$ holds if and only if $(C w)_i = 1$. $\square$

So if the iterates converge to a positive limit, line L5 is continuous there and the limit solves $C w = \mathbf{1}$: the weighted samples, convolved with the kernel, give the value 1 at every sample. If $C w = \mathbf{1}$ has no positive solution, the iterates cannot converge to a positive vector.

**Theorem 3 (scale of the kernel).** Let $c > 0$, and let $\tilde w^{(t)}$ be the iterates for the kernel $c\, C$. Then $\tilde w^{(t)} = w^{(t)}/c$ for every $t \ge 1$.

*Proof.* For $t = 1$: $\tilde w^{(1)}_i = 1 / (c\, (C \mathbf{1})_i) = w^{(1)}_i / c$. If $\tilde w^{(t)} = w^{(t)}/c$, then $\tilde d^{(t)} = c\, C\, w^{(t)}/c = d^{(t)}$, so $\tilde w^{(t+1)}_i = (w^{(t)}_i / c) / d^{(t)}_i = w^{(t+1)}_i / c$. $\square$

The weights therefore carry the unit of the inverse kernel. A reconstruction that grids with the kernel $C$ must use weights from the same $C$, or rescale them.

**Theorem 4 (repeated samples).** If $k_a = k_b$, then $w^{(t)}_a = w^{(t)}_b$ for every $t$.

*Proof.* The rows $a$ and $b$ of $C$ are equal, because $C_{aj} = C(|k_a - k_j|) = C(|k_b - k_j|) = C_{bj}$. By induction, if $w^{(t)}_a = w^{(t)}_b$, then $d^{(t)}_a = d^{(t)}_b$, so $w^{(t+1)}_a = w^{(t+1)}_b$. The start $w^{(0)} = \mathbf{1}$ has equal entries. $\square$

Moreover, the columns $a$ and $b$ of $C$ are equal too, so $C w$ depends on $w_a$ and $w_b$ only through $w_a + w_b$. If $C w = \mathbf{1}$ has a positive solution, the two copies share the weight that one sample at that place would get in the system without the repeat, provided that system has a unique solution. $\blacksquare$

**Remarks.**

- Theorems 1 to 4 hold for every positive starting vector in place of $\mathbf{1}$, except that Theorem 4 needs equal starting values on the repeated samples.
- The fixed points solve $\operatorname{diag}(w)\, C w = w$, a diagonal scaling equation. This page gives no convergence theorem for the iteration. In the tests, the iterates matched the direct solution of $C w = \mathbf{1}$ when that solution was positive.
