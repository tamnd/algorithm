---
title: AWE computes the moments of the transfer function, its model matches the first 2q of them and is the unique such model, q = n gives the exact function, and stability is not guaranteed
proves: [the moment recurrence, matching of 2q moments, uniqueness of the Padé model, exactness for q = n, the residue formula and the step response, the first moment is minus the Elmore delay, an unstable model of a stable circuit, running time]
status: full
---

**Setting.** A linear circuit has the nodal equations $(G + sC) x(s) = b \, u(s)$ in the Laplace domain, where $G$ and $C$ are real $n \times n$ matrices, $G$ is invertible, $b$ is the input vector and $u$ the input. The output is $y = l^T x$. So the transfer function is
$$ H(s) = l^T (G + sC)^{-1} b. $$
Write $A = -G^{-1} C$ and $r = G^{-1} b$. All arithmetic in lines L1 to L5 is exact (rational numbers); lines L6 and L7 use floating point.

**Theorem 1 (moments).** For $|s| < 1 / \rho(A)$, where $\rho$ is the spectral radius ($|s|$ unrestricted if $\rho(A) = 0$),
$$ H(s) = \sum_{k \ge 0} m_k s^k, \qquad m_k = l^T A^k r, $$
and lines L1 to L3 compute $m_0, \ldots, m_{2q-1}$.

*Proof.* $G + sC = G (I - sA)$, so $(G + sC)^{-1} = (I - sA)^{-1} G^{-1}$. For $|s| \rho(A) < 1$ the Neumann series $(I - sA)^{-1} = \sum_k s^k A^k$ converges, which gives the expansion. Line L1 sets $x_0 = r$, and line L2 sets $x_k = G^{-1}(-C x_{k-1}) = A x_{k-1}$, so $x_k = A^k r$ by induction, and line L3 gives $m_k = l^T x_k$. $\square$

**Theorem 2 (matching of 2q moments).** Suppose the $q \times q$ Hankel matrix $M_q$ with entries $m_{k-j}$ ($k = q, \ldots, 2q-1$, $j = 1, \ldots, q$) is invertible. Let $b_0 = 1$, let $b_1, \ldots, b_q$ solve line L4 and let $a_0, \ldots, a_{q-1}$ be given by line L5. With $Q(s) = \sum_{j=0}^q b_j s^j$ and $P(s) = \sum_{k=0}^{q-1} a_k s^k$,
$$ Q(s) H(s) - P(s) = O(s^{2q}), \qquad H(s) - \frac{P(s)}{Q(s)} = O(s^{2q}). $$
So the Taylor coefficients of $P/Q$ at 0 are $m_0, \ldots, m_{2q-1}$.

*Proof.* The coefficient of $s^k$ in $Q(s) H(s)$ is $c_k = \sum_{j=0}^{\min(k, q)} b_j m_{k-j}$. For $k \le q - 1$, $c_k = a_k$ by line L5. For $q \le k \le 2q - 1$, $c_k = m_k + \sum_{j=1}^q b_j m_{k-j} = 0$ by line L4. So $QH - P$ has no terms of degree below $2q$. Since $Q(0) = 1$, $1/Q$ is a power series, and $H - P/Q = (QH - P)/Q = O(s^{2q})$. $\square$

**Theorem 3 (uniqueness).** Under the hypothesis of Theorem 2, if $P'$ and $Q'$ are polynomials with $\deg P' \le q - 1$, $\deg Q' \le q$, $Q'(0) = 1$ and $H - P'/Q' = O(s^{2q})$, then $P' = P$ and $Q' = Q$.

*Proof.* $Q' H - P' = Q' (H - P'/Q') = O(s^{2q})$. Since $\deg P' \le q - 1$, the coefficients of $s^q, \ldots, s^{2q-1}$ in $Q' H$ are 0, which says that the coefficients $b'_1, \ldots, b'_q$ of $Q'$ solve the system of line L4. As $M_q$ is invertible, $Q' = Q$. Then $P'$ is the part of degree below $q$ of $Q H$, which is $P$. $\square$

**Theorem 4 (q = n is exact).** Let $D(s) = \det(G + sC)$ and suppose that line L4 succeeds for $q = n$. Then $Q = D / D(0)$, and $P / Q = H$ as rational functions.

*Proof.* By Cramer's rule, $x_i(s) = D_i(s) / D(s)$, where $D_i$ is the determinant of $G + sC$ with column $i$ replaced by $b$. Each term of $D$ is a product of $n$ entries of degree at most 1 in $s$, so $\deg D \le n$, and each term of $D_i$ has one constant factor from $b$, so $\deg D_i \le n - 1$. Hence $H = N / D$ with $N = \sum_i l_i D_i$ and $\deg N \le n - 1$. Also $D(0) = \det G \ne 0$. The pair $P' = N / D(0)$, $Q' = D / D(0)$ meets the conditions of Theorem 3 with $q = n$, since $H - P'/Q' = 0$. So $Q = Q'$ and $P = P'$. $\square$

If $M_q$ is singular, line L4 has no unique solution, and the implementation raises an error. This happens, for example, for $q = 2$ on a circuit with one capacitor, whose moments $m_k = (-\tau)^k$ give $m_1^2 - m_0 m_2 = 0$.

**Theorem 5 (residues and step response).** Suppose $b_q \ne 0$ and the roots $p_1, \ldots, p_q$ of $Q$ are simple. Then
$$ \frac{P(s)}{Q(s)} = \sum_{i=1}^q \frac{k_i}{s - p_i}, \qquad k_i = \frac{P(p_i)}{Q'(p_i)}, $$
and the inverse Laplace transform of $P(s) / (s Q(s))$, the response of the model to a unit step, is
$$ y(t) = m_0 + \sum_{i=1}^q \frac{k_i}{p_i} e^{p_i t} \quad (t \ge 0), \qquad y(0) = 0. $$

*Proof.* $\deg P < \deg Q$ and the roots are simple, so the partial fraction decomposition has the stated form, with $k_i = \lim_{s \to p_i} (s - p_i) P(s) / Q(s) = P(p_i) / Q'(p_i)$, since $Q(p_i) = 0$ and $Q'(p_i) \ne 0$. No root is 0 because $Q(0) = 1$. Then
$$ \frac{k_i}{s (s - p_i)} = \frac{k_i}{p_i} \left( \frac{1}{s - p_i} - \frac{1}{s} \right), $$
whose inverse transform is $(k_i / p_i)(e^{p_i t} - 1)$. Summing over $i$ gives $y(t) = \sum_i (k_i/p_i) e^{p_i t} - \sum_i k_i / p_i$. At $s = 0$ the decomposition gives $P(0)/Q(0) = -\sum_i k_i / p_i$, and $P(0)/Q(0) = a_0 = m_0$. So the constant is $m_0$, and $y(0) = m_0 + \sum_i k_i / p_i = 0$. $\square$

Lines L6 and L7 compute the roots and the residues in floating point by an iteration, so the poles and residues of the implementation are approximations of these exact values. The coefficients of $P$ and $Q$ are exact.

**Theorem 6 (the first moment is minus the Elmore delay).** For an RC tree driven at its root through the resistor $R_{\text{root}}$ by a source of value 1, with a capacitor $C_k$ from node $k$ to ground, and output at node $i$ ($l = e_i$), $m_0 = 1$ and $-m_1 = \sum_k R_{ik} C_k$, the [Elmore delay](/elmore-delay/), where $R_{ik}$ is the resistance of the common part of the paths from the source to $i$ and to $k$.

*Proof.* At $s = 0$ no current flows in the capacitors, so no current flows in the resistors, and every node has voltage 1: $r = G^{-1} b = \mathbf 1$, and $m_0 = 1$. Then $m_1 = e_i^T G^{-1}(-C \mathbf 1) = -\sum_k (G^{-1})_{ik} C_k$. Here $(G^{-1})_{ik}$ is the voltage at node $i$ when the source is set to 0 and a unit current is injected at node $k$. That current flows to ground along the unique path from $k$ to the source, so the voltage at a node on that path is the resistance between the node and the source, and every node off the path has the voltage of the node where its path to the source meets the path from $k$. The voltage at $i$ is therefore the resistance of the common part of the two paths, $R_{ik}$. $\square$

**Proposition 7 (stability is not guaranteed).** There is an RC tree, whose poles all lie in the open left half-plane, for which the AWE model with $q = 2$ has a pole in the right half-plane.

*Proof.* Take the ladder with $R = (1, 1, 1)$ and $C = (1, 2, 1)$ and the output at the middle node. Exact computation by lines L1 to L3 gives $m = (1, -7, 48, -330)$. Line L4 solves $-7 b_1 + b_2 = -48$ and $48 b_1 - 7 b_2 = 330$, so $b_1 = 6$ and $b_2 = -6$, and $Q(s) = 1 + 6s - 6s^2$. Its roots are $(6 \pm \sqrt{60})/12$, and $(6 + \sqrt{60})/12 > 0$. The circuit itself has $\det(G + sC) / \det G = 1 + 8s + 8s^2 + 2s^3$. All its coefficients are positive and $8 \cdot 8 > 2 \cdot 1$, so by the Routh-Hurwitz condition for degree 3 all its roots have negative real parts. $\square$

The function `is_stable` of the implementation decides with the Routh test in exact arithmetic whether all roots of $Q$ lie in the open left half-plane. Its correctness is the Routh-Hurwitz theorem, which is not proved here.

**Theorem 8 (running time).** With dense matrices of order $n$, lines L1 to L3 take $\Theta(n^3 + q n^2)$ arithmetic operations: one LU factorization of $G$ and $2q$ triangular solves and products with $C$. Lines L4 and L5 take $\Theta(q^3)$ and $\Theta(q^2)$. Each iteration of the root finder in line L6 takes $\Theta(q^2)$, and line L7 takes $\Theta(q^2)$.

*Proof.* The LU factorization of a dense $n \times n$ matrix takes $\Theta(n^3)$ operations, each pair of triangular solves $\Theta(n^2)$, and each product $C x$ and each inner product $l^T x$ at most $\Theta(n^2)$. The Hankel system is a dense $q \times q$ system. Line L5 sums at most $q$ products for each of $q$ coefficients. One Durand-Kerner sweep evaluates $Q$ and a product of $q - 1$ differences at each of $q$ points. Line L7 evaluates two polynomials of degree below $q$ at $q$ points. $\square$

No bound on the number of iterations of the root finder is proved here. For an RC tree, $G$ is sparse and the moments take $\Theta(n)$ operations each by two passes over the tree, as for the Elmore delay.

$\blacksquare$
