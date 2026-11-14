---
title: The Gordon surface of a compatible network contains every curve of the network
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page. The input curves $f_0, \dots, f_n$ have degree $q$, the curves $g_0, \dots, g_m$ have degree $p$, the parameters increase, $n \ge p$, $m \ge q$, the outer parameters $u_0, u_n$ and $v_0, v_m$ are the ends of the knot vectors of the other family, and the network is compatible: $f_i(v_j) = g_j(u_i) = p_{ij}$.

## Lemma 1 (knot insertion)

Inserting a knot into a B-spline curve, by Boehm's rule, gives a new control polygon on the new knot vector that defines the same curve. Inserting a knot into a surface row by row or column by column gives the same surface. This is the theorem on the [Boehm knot insertion](/boehm-knot-insertion/) page, applied to each row or column of the net, since a tensor product surface at fixed $v$ is a curve in $u$ whose control points are the values at $v$ of the column curves. So lines L1, L2 and L7 do not change any curve or surface, and after line L1 every $f_i$ is $f_i(v) = \sum_l M_l(v) F_i[l]$ with the same B-spline basis $M_l$ on $V_c$; likewise $g_j(u) = \sum_k N_k(u) G_j[k]$ on $U_c$.

## Lemma 2 (the interpolation operator)

Let $U_1$ be the averaged knot vector of degree $p$ for the parameters $u_0, \dots, u_n$, with basis $N^1_0, \dots, N^1_n$, and let $A$ be the collocation matrix $A_{ik} = N^1_k(u_i)$. Then $A$ is nonsingular, and the splines

$$\phi_i(u) = \sum_{k=0}^{n} N^1_k(u) (A^{-1})_{ki}, \qquad i = 0, \dots, n,$$

satisfy $\phi_i(u_r) = \delta_{ri}$. For any data $d_0, \dots, d_n$ in a vector space, the spline that line L4 computes with control points $c = A^{-1} d$ is $\sum_i \phi_i(u) d_i$.

*Proof.* With averaged knots each inner knot is the mean of $p$ consecutive parameters, $t_{k+p} = (u_k + \dots + u_{k+p-1})/p$ for $k = 1, \dots, n - p$, so $t_k < u_k < t_{k+p+1}$ for the inner indices, and $u_0$ and $u_n$ are the end knots. These are the conditions of the [Schoenberg-Whitney theorem](/schoenberg-whitney-theorem/), so $A$ is nonsingular. Then $\phi_i(u_r) = \sum_k A_{rk} (A^{-1})_{ki} = \delta_{ri}$. The spline with control points $c$ is $\sum_k N^1_k(u) c_k = \sum_k N^1_k(u) \sum_i (A^{-1})_{ki} d_i = \sum_i \phi_i(u) d_i$. The data may be points, or tuples of control points, since the computation is linear and is done for each entry. $\square$

Let $\psi_0, \dots, \psi_m$ be the splines of Lemma 2 for the parameters $v_j$, degree $q$ and the knots $V_2$, with $\psi_j(v_l) = \delta_{lj}$.

## Lemma 3 (the three surfaces)

The surfaces of lines L4, L5 and L6 are

$$S_1(u, v) = \sum_i \phi_i(u) f_i(v), \qquad S_2(u, v) = \sum_j \psi_j(v) g_j(u), \qquad T(u, v) = \sum_{i, j} \phi_i(u) \psi_j(v) p_{ij}.$$

*Proof.* In line L4 the data for the index $l$ are $F_0[l], \dots, F_n[l]$, so by Lemma 2 the control points of $S_1$ are $P_1[k][l] = \sum_i (A^{-1})_{ki} F_i[l]$. Then

$$S_1(u, v) = \sum_{k, l} N^1_k(u) M_l(v) P_1[k][l] = \sum_i \Bigl(\sum_k N^1_k(u) (A^{-1})_{ki}\Bigr) \Bigl(\sum_l M_l(v) F_i[l]\Bigr) = \sum_i \phi_i(u) f_i(v),$$

using Lemma 1 for the last factor. The proof for $S_2$ is the same with the roles of $u$ and $v$ exchanged. In line L6, the first step gives for each $j$ the spline $\sum_i \phi_i(u) p_{ij}$ in $u$, with control points $R[k][j]$. The second step interpolates, for each $k$, the values $R[k][0], \dots, R[k][m]$ at $v_0, \dots, v_m$, which by Lemma 2 gives control points $P_3[k][l]$ with $\sum_l M^2_l(v) P_3[k][l] = \sum_j \psi_j(v) R[k][j]$. Hence $T(u, v) = \sum_k N^1_k(u) \sum_j \psi_j(v) R[k][j] = \sum_j \psi_j(v) \sum_i \phi_i(u) p_{ij}$. $\square$

## Theorem

If line L3 does not report an incompatible network, the surface $S$ returned in line L8 satisfies $S(u_r, v) = f_r(v)$ for all $r$ and all $v$ in $[v_0, v_m]$, and $S(u, v_s) = g_s(u)$ for all $s$ and all $u$ in $[u_0, u_n]$.

*Proof.* By Lemma 1 the refined nets of line L7 define the same three surfaces on one basis $U \times V$. A tensor product surface depends linearly on its net, so the net $P_1 + P_2 - P_3$ defines $S = S_1 + S_2 - T$. Fix $r$. By Lemma 3 and $\phi_i(u_r) = \delta_{ri}$,

$$S_1(u_r, v) = f_r(v), \qquad S_2(u_r, v) = \sum_j \psi_j(v) g_j(u_r), \qquad T(u_r, v) = \sum_j \psi_j(v) p_{rj}.$$

Line L3 passed, so $g_j(u_r) = p_{rj}$ for every $j$, and the last two terms are equal. Hence $S(u_r, v) = f_r(v)$. For $s$ fixed, $\psi_j(v_s) = \delta_{sj}$ gives $S_2(u, v_s) = g_s(u)$, $S_1(u, v_s) = \sum_i \phi_i(u) f_i(v_s) = \sum_i \phi_i(u) p_{is}$ and $T(u, v_s) = \sum_i \phi_i(u) p_{is}$, so $S(u, v_s) = g_s(u)$. $\square$

## The operator form

The theorem is a case of a general fact about Boolean sums. For surfaces $F$ on the rectangle put $\mathcal{P} F(u, v) = \sum_i \phi_i(u) F(u_i, v)$ and $\mathcal{Q} F(u, v) = \sum_j \psi_j(v) F(u, v_j)$. Both are linear, and both are projectors: $\mathcal{P}\mathcal{P} F = \mathcal{P} F$ because $\phi_i(u_r) = \delta_{ri}$. They commute, $\mathcal{P}\mathcal{Q} F = \mathcal{Q}\mathcal{P} F = \sum_{i, j} \phi_i(u) \psi_j(v) F(u_i, v_j)$, because they act on different variables. The Boolean sum $\mathcal{P} \oplus \mathcal{Q} = \mathcal{P} + \mathcal{Q} - \mathcal{P}\mathcal{Q}$ satisfies

$$I - \mathcal{P} \oplus \mathcal{Q} = (I - \mathcal{P})(I - \mathcal{Q}).$$

For any surface $G$, $(I - \mathcal{P}) G$ vanishes on every line $u = u_r$, since $\mathcal{P} G(u_r, v) = G(u_r, v)$. As $(I - \mathcal{P})$ and $(I - \mathcal{Q})$ commute, the error $F - (\mathcal{P} \oplus \mathcal{Q}) F$ vanishes on every line $u = u_r$ and on every line $v = v_s$. For a compatible network, the surface $S$ of the theorem itself contains the network, so the network comes from some $F$, and $(\mathcal{P} \oplus \mathcal{Q}) F$ uses only the values of $F$ on the network, which are the curves. This is the form in which Gordon stated the result in 1971.

## Rejection

If line L3 reports an incompatible network, then $f_i(v_j) \ne g_j(u_i)$ for some $i, j$, and no surface can contain both curves, since it would take two values at $(u_i, v_j)$. So the report is correct. With exact arithmetic the test in line L3 is exact; with a tolerance, a network that passes is compatible only to that tolerance, and the theorem holds for the network after the curves of one family are moved by at most that amount at the crossings.
