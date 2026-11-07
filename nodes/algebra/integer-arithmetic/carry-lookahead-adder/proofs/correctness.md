---
title: The carry-lookahead adder computes the sum of its inputs
proves: [correctness, termination]
status: full
---

Let $n \ge 1$, $r \ge 2$, and let $a_i, b_i, c_0 \in \{0, 1\}$. Define the true carries by $c^{\ast}_0 = c_0$ and $c^{\ast}_{i+1} = g_i \vee (p_i \wedge c^{\ast}_i)$ with $g_i = a_i \wedge b_i$ and $p_i = a_i \oplus b_i$ (line L1). Then $a_i + b_i + c^{\ast}_i = (a_i \oplus b_i \oplus c^{\ast}_i) + 2 c^{\ast}_{i+1}$ for each $i$: if $p_i = 1$ the left side is $1 + c^{\ast}_i$, and if $p_i = 0$ it is $2g_i + c^{\ast}_i$. Multiplying by $2^i$ and summing gives

$$a + b + c_0 = \sum_{i=0}^{n-1} (p_i \oplus c^{\ast}_i)\, 2^i + c^{\ast}_n\, 2^n ,$$

so it suffices to show that leaf $i$ receives the carry-in $c^{\ast}_i$ and that line L10 gives $c^{\ast}_n$.

**Termination.** Each pass of the loop L3 to L6 replaces a level of $t \ge 1$ nodes by $\lceil t / r \rceil$ nodes. If $t \ge 2$ this is less than $t$, and if $t = 1$ the pass makes one group, and the loop stops. So the loop runs $h = \max(1, \lceil \log_r n \rceil)$ times. The downward pass visits each of the finitely many nodes once.

**Notation.** Each node $v$ covers an interval of positions $[\ell_v, u_v]$: a leaf $i$ covers $[i, i]$, and a group covers the union of the intervals of its children, which are consecutive and listed from low to high, because line L4 cuts each level into runs of consecutive nodes and the leaves are in order.

**Lemma 1 (unrolling).** Let $(x_0, y_0), \ldots, (x_{m-1}, y_{m-1})$ and bits $d_0, \ldots, d_m$ satisfy $d_{j+1} = x_j \vee (y_j \wedge d_j)$ for $0 \le j < m$. Then for each $k$ with $1 \le k \le m$,

$$d_k = x_{k-1} \vee y_{k-1} x_{k-2} \vee \cdots \vee y_{k-1} \cdots y_1 x_0 \vee y_{k-1} \cdots y_0\, d_0 .$$

*Proof.* By induction on $k$. For $k = 1$ it is the hypothesis. If it holds for $k$, then $d_{k+1} = x_k \vee y_k d_k$; substituting the formula for $d_k$ and distributing $y_k$ over the OR gives the formula for $k + 1$. $\square$

**Lemma 2 (upward invariant).** For each node $v$ that has signals $(G_v, P_v)$ (a leaf, or a group built in line L5), $c^{\ast}_{u_v + 1} = G_v \vee (P_v \wedge c^{\ast}_{\ell_v})$.

*Proof.* By induction on the level. For a leaf $i$, $(G_v, P_v) = (g_i, p_i)$ and the claim is the definition of $c^{\ast}_{i+1}$. For a group with one child, the signals are the child's and the interval is the same. For a group $v$ with children $w_0, \ldots, w_{m-1}$, $m \ge 2$, set $x_j = G_{w_j}$, $y_j = P_{w_j}$ and $d_j = c^{\ast}_{\ell_{w_j}}$ for $j < m$, and $d_m = c^{\ast}_{u_v + 1}$. Since the intervals are consecutive, $u_{w_j} + 1 = \ell_{w_{j+1}}$, so the induction hypothesis for the children says $d_{j+1} = x_j \vee y_j d_j$. Lemma 1 with $k = m$ gives $d_m = G_v \vee P_v d_0$ where $G_v$ and $P_v$ are exactly the formulas of line L5, and $d_0 = c^{\ast}_{\ell_v}$. $\square$

**Lemma 3 (downward invariant).** Each node $v$ receives the carry-in $c^{\ast}_{\ell_v}$.

*Proof.* By induction from the root down. The root covers $[0, n-1]$ and receives $c_0 = c^{\ast}_0$ in line L7. Let $v$ be a group with carry-in $c^{\ast}_{\ell_v}$ and children $w_0, \ldots, w_{m-1}$, and define $x_j, y_j, d_j$ as in the proof of Lemma 2, where now each child has signals by Lemma 2 (children of any group are leaves or groups built in line L5, since only the root skips line L5). Child $w_0$ receives $c^{\ast}_{\ell_v} = d_0$, and $\ell_{w_0} = \ell_v$. For $1 \le k < m$, line L9 gives child $w_k$ the value of the formula of Lemma 1 with $d_0 = c^{\ast}_{\ell_v}$, which equals $d_k = c^{\ast}_{\ell_{w_k}}$. $\square$

**Theorem.** CLA-ADD returns the sum bits and the carry out of $a + b + c_0$.

*Proof.* By Lemma 3, leaf $i$ receives $c^{\ast}_i$, so line L11 sets $s_i = p_i \oplus c^{\ast}_i$. Line L10 applies the formula of Lemma 1 with $k = m$ to the root's children and $d_0 = c_0$; by Lemma 2 for the children it equals $d_m = c^{\ast}_{u + 1}$ with $u = n - 1$, so it is $c^{\ast}_n$. By the identity at the start, the outputs represent $a + b + c_0$. $\blacksquare$
