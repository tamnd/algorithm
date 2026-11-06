---
title: Correctness of the MOV reduction
proves: [correctness, termination]
status: full
---

Let $p \equiv 3 \pmod 4$ be prime, $E : y^2 = x^3 + x$ over $\mathbb{F}_p$, $\mathbb{F}_{p^2} = \mathbb{F}_p(i)$ with $i^2 = -1$, and $\psi(x, y) = (-x, iy)$. Let $P \in E(\mathbb{F}_p)$ have odd order $n$ and $Q \in E(\mathbb{F}_p)$. For termination we treat the choices of line L4 as independent. We use the following standard facts about the Tate pairing, for an elliptic curve over a finite field $\mathbb{F}$ and $m$ with $\mu_m \subseteq \mathbb{F}^*$ (Galbraith, Theorem 26.3.3 and Section 26.3.1, and Frey and Rück for non-degeneracy).

- **(T1)** The reduced pairing $\hat t_m : E(\mathbb{F})[m] \times E(\mathbb{F})/mE(\mathbb{F}) \to \mu_m$ is bilinear.
- **(T2)** It is non-degenerate: if $S \in E(\mathbb{F})[m]$ and $\hat t_m(S, R) = 1$ for all $R \in E(\mathbb{F})$, then $S = O$.
- **(T3)** If $m \mid N$ and both $\mu_m, \mu_N \subseteq \mathbb{F}^*$, then $\hat t_m(S, R) = \hat t_N(S, R)$ for $S \in E(\mathbb{F})[m]$ (Galbraith, Exercise 26.3.8).
- **(T4)** For $T_0 \in E(\mathbb{F}_p)$ of order $m$ with $m \mid p + 1$ and $R \in E(\mathbb{F}_{p^2}) \setminus E(\mathbb{F}_p)$, the reduced pairing over $\mathbb{F} = \mathbb{F}_{p^2}$ equals $f_{m, T_0}(R)^{(p^2 - 1)/m}$, where $f_{m, T_0}$ is any function over $\mathbb{F}_p$ with divisor $m(T_0) - m(O)$ (Galbraith, Lemma 26.3.11, whose argument works for any $m$ prime to $p$ as noted there after Granger, Hess, Oyono, Thériault and Vercauteren).
- **(T5)** Miller's construction: if $f_k$ has divisor $k(T_0) - (kT_0) - (k - 1)(O)$, then $f_{2k} = f_k^2 \, \ell_{kT_0, kT_0} / v_{2kT_0}$ and $f_{k + 1} = f_k \, \ell_{kT_0, T_0} / v_{(k + 1)T_0}$, where $\ell$ is the line through the two points and $v_S = x - x_S$ is the vertical line through $S$, with $v_O = 1$; if $kT_0 = -T_0$, the line $\ell_{kT_0, T_0}$ is $v_{T_0}$ itself. Then $f_m$ has divisor $m(T_0) - m(O)$.

**Lemma 1 (the group).** $\#E(\mathbb{F}_p) = p + 1$, $E(\mathbb{F}_p)$ is cyclic, and $E(\mathbb{F}_p)[2] = \{O, (0, 0)\}$.

*Proof.* Since $p \equiv 3 \pmod 4$, $-1$ is not a square modulo $p$, so $x^2 + 1$ has no root and $x^3 + x = 0$ only for $x = 0$. The map $x \mapsto -x$ sends $x^3 + x$ to $-(x^3 + x)$, so for each pair $\{x, -x\}$ with $x \ne 0$ exactly one of the two values is a nonzero square, giving two points. The $(p - 1)/2$ pairs give $p - 1$ points, and with $(0, 0)$ and $O$ there are $p + 1$. The $2$-torsion consists of $O$ and the points with $y = 0$, which is only $(0, 0)$. Write $E(\mathbb{F}_p) \cong \mathbb{Z}/n_1 \times \mathbb{Z}/n_2$ with $n_1 \mid n_2$. If $n_1 > 1$, a prime $r \mid n_1$ would give $E[r] \subseteq E(\mathbb{F}_p)$, and the Weil pairing then puts $\mu_r$ in $\mathbb{F}_p$, so $r \mid p - 1$; also $r \mid p + 1$, so $r = 2$, but $E(\mathbb{F}_p)[2]$ has only two elements. So $n_1 = 1$. $\square$

**Lemma 2 (membership).** Line L1 returns NONE exactly when $Q \notin \langle P \rangle$, and line L2 is correct.

*Proof.* A cyclic group has exactly one subgroup of each order dividing its order, and $\{S : nS = O\}$ is the subgroup of order $n$, so it equals $\langle P \rangle$. If $Q = O$ then $x = 0$. $\square$

From now on $Q = x^* P$ with $0 < x^* < n$, so $n \ge 3$, and $d = \operatorname{ord}(Q)$ divides $n$ and is odd.

**Lemma 3 (the helper point).** The point $R = \psi(R_0)$ of line L4 lies on $E$, is not in $E(\mathbb{F}_p)$, and every line value in TATE is a nonzero element of $\mathbb{F}_{p^2}$, while every vertical line value $x_R - x_S$ with $S \in E(\mathbb{F}_p)$ lies in $\mathbb{F}_p^*$.

*Proof.* $(iy_0)^2 = -y_0^2 = -(x_0^3 + x_0) = (-x_0)^3 + (-x_0)$, so $R \in E(\mathbb{F}_{p^2})$, and $iy_0 \notin \mathbb{F}_p$ since $y_0 \ne 0$. For $T \in E(\mathbb{F}_p)$ and a slope $\lambda \in \mathbb{F}_p$, $\ell(R) = iy_0 - y_T - \lambda(-x_0 - x_T)$ has imaginary part $y_0 \ne 0$. If $x_R = x_S$ for $S = (x_S, y_S) \in E(\mathbb{F}_p)$, then $y_S^2 = x_S^3 + x_S = (iy_0)^2 = -y_0^2$, which forces $-1$ to be a square or $y_0 = 0$; neither holds, so $x_R - x_S \in \mathbb{F}_p^*$. $\square$

**Lemma 4 (TATE).** For $T_0 \in E(\mathbb{F}_p)$ of odd order $m \ge 3$ with $m \mid p + 1$, and $R$ as in line L4, TATE$(T_0, R, m) = \hat t_m(T_0, R)$, the reduced pairing over $\mathbb{F}_{p^2}$.

*Proof.* After processing the binary prefix $k$ of $m$, the loop of lines L10 to L12 keeps $T = kT_0$ and $f = c_k f_k(R)$ for a constant $c_k \in \mathbb{F}_p^*$, with $f_k$ as in (T5). Initially $k = 1$, $f_1 = 1$. A doubling at line L11 multiplies by $\ell_{T,T}(R)$ and omits $v_{2T}(R)^{-1}$, and an addition at line L12 multiplies by $\ell_{T, T_0}(R)$ and omits $v_{T + T_0}(R)^{-1}$. By Lemma 3 every omitted factor lies in $\mathbb{F}_p^*$. Every prefix $k$ before the last step satisfies $1 \le k < m$, so $kT_0 \ne O$; since $m$ is odd, $kT_0$ is not $(0, 0)$, so the tangent at $T$ is not vertical and $2T \ne O$. An addition at an intermediate step has $T = kT_0$ with $2 \le k < m - 1$, so $T \ne \pm T_0$ and the chord has a slope. The only vertical chord is at the last step, where $k = m - 1$ and $T = -T_0$; by (T5) its line is $v_{T_0}$, also in $\mathbb{F}_p^*$ at $R$, and line L12 omits it. So before line L13, $f = c \, f_m(R)$ with $c \in \mathbb{F}_p^*$ and $f_m$ of divisor $m(T_0) - m(O)$. The exponent $(p^2 - 1)/m = (p - 1)(p + 1)/m$ is a multiple of $p - 1$, so $c^{(p^2 - 1)/m} = 1$, and by (T4) the result is $\hat t_m(T_0, R)$. $\square$

**Lemma 5 (soundness).** If line L5 accepts, then lines L6 to L8 return $x^*$.

*Proof.* Since $n \mid p + 1 \mid p^2 - 1$, $\mu_n \subseteq \mathbb{F}_{p^2}^*$, and similarly for $d$. By Lemma 4 and (T3), $\beta = \hat t_d(Q, R) = \hat t_n(Q, R)$, and by (T1), $\hat t_n(x^* P, R) = \hat t_n(P, R)^{x^*} = \alpha^{x^*}$. Line L5 accepts only if $\alpha^{n/r} \ne 1$ for every prime $r \mid n$; since $\alpha^n = 1$, $\alpha$ has order exactly $n$. The equation $\alpha^x = \beta$ then has the unique solution $x^*$ in $[0, n)$, which baby-step giant-step finds. $\square$

**Lemma 6 (each trial succeeds with positive probability).** Let $\chi(R_0) = \hat t_n(P, \psi(R_0))$ for $R_0 \in E(\mathbb{F}_p)$. Then $\chi$ is a homomorphism from $E(\mathbb{F}_p)$ onto $\mu_n$, and one trial of lines L4 and L5 accepts with probability at least $\varphi(n)/n$.

*Proof.* $\psi$ is a homomorphism, since it is an isomorphism of curves over $\mathbb{F}_{p^2}$ fixing $O$ (it maps $y^2 = x^3 + x$ to itself), so $\chi$ is a homomorphism by (T1). Let $\pi$ be the $p$-power Frobenius on $E(\mathbb{F}_{p^2})$, so $\pi^2 = 1$ there. A point $(x, y)$ satisfies $\pi(x, y) = -(x, y)$ exactly when $x \in \mathbb{F}_p$ and $y^p = -y$, that is $y \in i \mathbb{F}_p$; writing $y = iy_1$, the equation gives $y_1^2 = (-x)^3 + (-x)$, so $\ker(\pi + 1) = \psi(E(\mathbb{F}_p))$, and $\ker(\pi - 1) = E(\mathbb{F}_p)$.

For $S \in E(\mathbb{F}_p)$, $\hat t_n(P, S) = 1$: computing the pairing with a divisor equivalent to $(S) - (O)$ defined over $\mathbb{F}_p$, the value before the final exponentiation lies in $\mathbb{F}_p^*$, and the exponent $(p^2 - 1)/n$ is a multiple of $p - 1$. Now let $S \in E(\mathbb{F}_{p^2})$ be arbitrary and let $u$ be an integer with $2u \equiv 1 \pmod n$, which exists because $n$ is odd. Then $S - 2uS = (1 - 2u)S \in nE(\mathbb{F}_{p^2})$, and $2uS = u(S + \pi S) + u(S - \pi S)$ with $u(S + \pi S) \in \ker(\pi - 1)$ and $u(S - \pi S) \in \ker(\pi + 1)$. Since $\hat t_n(P, \cdot)$ is a homomorphism that is trivial on $nE(\mathbb{F}_{p^2})$ and on $E(\mathbb{F}_p)$, $\hat t_n(P, S) = \hat t_n(P, u(S - \pi S))$, which lies in $\chi(E(\mathbb{F}_p))$. So the image of $\chi$ equals the image of $\hat t_n(P, \cdot)$ on all of $E(\mathbb{F}_{p^2})$.

If that image were a proper subgroup of the cyclic group $\mu_n$, it would lie in $\mu_{n/r}$ for some prime $r \mid n$, and then $\hat t_n((n/r)P, S) = \hat t_n(P, S)^{n/r} = 1$ for every $S$, so $(n/r)P = O$ by (T2), contradicting $\operatorname{ord}(P) = n$. So $\chi$ is onto $\mu_n$, and its kernel $K$ has $(p + 1)/n$ elements.

Line L4 draws $R_0$ uniformly from $E(\mathbb{F}_p) \setminus \{O, (0, 0)\}$: $x_0$ is uniform, the draw is kept when $x_0^3 + x_0$ is a nonzero square, and the sign of $y_0$ is uniform, so every affine point with $y_0 \ne 0$ has the same probability. Both excluded points lie in $K$: $\chi(O) = 1$, and $\chi((0, 0))$ has order dividing $2$ and $n$, so it is $1$. Each element of $\mu_n$ of order exactly $n$ has $|K|$ preimages, none excluded, so the probability of acceptance is $\varphi(n)|K| / (p - 1) \ge \varphi(n)|K| / (p + 1) = \varphi(n)/n$. $\square$

**Termination.** The loop of lines L4 to L8 ends at the first accepted trial. Trials are independent, and by Lemma 6 each accepts with probability at least $\varphi(n)/n > 0$, so the loop ends with probability $1$ after an expected at most $n/\varphi(n)$ trials. The inner loops are finite: drawing $R_0$ succeeds with probability about $1/2$ per attempt, TATE runs $\lfloor \log_2 m \rfloor$ iterations, and baby-step giant-step runs $O(\sqrt n)$ steps.

**Conclusion.** By Lemma 2 the algorithm returns NONE exactly when $Q \notin \langle P \rangle$ and returns $0$ for $Q = O$; otherwise, by Lemmas 5 and 6, it returns $x^*$ with probability $1$. $\blacksquare$
