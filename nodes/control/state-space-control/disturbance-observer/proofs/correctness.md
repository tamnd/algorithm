---
title: The disturbance observer realizes Q(P_n^(-1) y - u), estimates Q d for an exact model, and leaves no offset for a constant disturbance
proves: [correctness]
status: full
---

Let $P_n = N/D$ with real polynomials $N$, $D$, $r = \deg D - \deg N \ge 1$, let $\tau > 0$, let $k \ge \max(r, 1)$ be an integer, and let $q(s) = (\tau s + 1)^k$ and $Q = 1/q$. All transfer functions below are for zero initial conditions.

## Lemma 1: the realization

Let $a(s) = s^n + a_1 s^{n-1} + \dots + a_n$ be monic, let $\beta(s) = \beta_0 s^n + \beta_1 s^{n-1} + \dots + \beta_n$, and let $A_f$ have $-a_1, \dots, -a_n$ in its first column, ones on the superdiagonal and zeros elsewhere, $C_f = [1, 0, \dots, 0]$, $b_i = \beta_i - \beta_0 a_i$. Then $C_f(sI - A_f)^{-1} b + \beta_0 = \beta(s)/a(s)$.

*Proof.* Let $w(s) = [s^{n-1}, s^{n-2}, \dots, 1]/a(s)$. Column 1 of $w(sI - A_f)$ is $s w_1 + \sum_i a_i w_i = a(s)/a(s) = 1$. For $j \ge 2$, column $j$ is $s w_j - w_{j-1} = (s \cdot s^{n-j} - s^{n-j+1})/a(s) = 0$. So $w(sI - A_f) = C_f$, that is, $C_f(sI - A_f)^{-1} = w$ for every $s$ that is not a root of $a$. Then

$$C_f(sI - A_f)^{-1} b + \beta_0 = \frac{\sum_{i=1}^n (\beta_i - \beta_0 a_i) s^{n-i} + \beta_0 a(s)}{a(s)} = \frac{\beta(s)}{a(s)}. \qquad \square$$

## Lemma 2: the filter of lines L1 to L5

If line L1 passes, the realization of line L5 has the transfer function $[D, -N]/(Nq)$ from $[y, u]$ to $\hat d$, its poles are the roots of $N$ and $-1/\tau$, all in the open left half plane, and its direct term from $u$ is 0. If $k < r$ or $N$ has a root with real part $\ge 0$, line L1 raises an error.

*Proof.* Line L2 sets $a = Nq/c$, where $c$ is the leading coefficient of $Nq$, so $a$ is monic of degree $n = \deg N + k$. Line L3 sets $\beta_y = D/c$ and $\beta_u = -N/c$. Since $\deg D = \deg N + r \le n$ and $\deg N = n - k < n$, both fit into $n + 1$ coefficients, and $\beta_u$ has leading coefficient 0. By Lemma 1 the transfer functions are $\beta_y/a = D/(Nq)$ and $\beta_u/a = -N/(Nq)$, and the direct term from $u$ is $\beta_{u,0} = 0$. The poles are the roots of $a$.

Line L1 uses the Routh test. A real polynomial has all roots in the open left half plane if and only if all its coefficients and all entries of the first column of its Routh array are nonzero and of one sign (the Routh-Hurwitz criterion). The implementation returns false as soon as an entry is 0 or of the other sign. This is correct, because a zero entry in the first column occurs only if some root has real part $\ge 0$. $\square$

## Lemma 3: the estimate

If $y = P(u + d)$, then $\hat d = QP_n^{-1}P(u + d) - Qu$. If $P = P_n$, then $\hat d = Qd$ for every input $u$.

*Proof.* By Lemma 2, $\hat d = (D y - N u)/(Nq) = Q(P_n^{-1} y - u)$. Substitute $y$. If $P = P_n$, then $P_n^{-1}P = 1$ and $\hat d = Q(u + d) - Qu = Qd$. $\square$

## Lemma 4: the closed loop

Let $u = u_c - \hat d$. Then

$$y = \frac{P P_n}{P_n + Q(P - P_n)}\bigl(u_c + (1 - Q)d\bigr).$$

*Proof.* By Lemma 3, $\hat d = QP_n^{-1}P(u_c - \hat d + d) - Q(u_c - \hat d)$. Multiply by $P_n$ and collect $\hat d$:

$$\hat d\,\bigl(P_n + Q(P - P_n)\bigr) = Q(P - P_n)u_c + QPd.$$

Let $\Delta = P_n + Q(P - P_n)$. Then

$$u + d = u_c - \hat d + d = \frac{\Delta u_c - Q(P - P_n)u_c + \Delta d - QPd}{\Delta} = \frac{P_n u_c + (1 - Q)P_n d}{\Delta},$$

since $\Delta - QP = P_n - QP_n$. Multiply by $P$. $\square$

## Theorem: no offset for a constant disturbance

Let $P = N_p/D_p$ and let the outer controller be $u_c = C(s)(y_{\mathrm{ref}} - y)$ with $C = N_c/D_c$. Write the transfer function from $d$ to $y$ as a ratio of polynomials. Its denominator is

$$\chi = D_c\bigl(N D_p (q - 1) + N_p D\bigr) + N_c N_p N q,$$

and its numerator is $N_p N D_c (q - 1)$. If all roots of $\chi$ lie in the open left half plane, then for a constant disturbance $d$ the output $y$ converges to its value for $d = 0$.

*Proof.* With $y_{\mathrm{ref}} = 0$, Lemma 4 gives $y = G(-Cy + (1 - Q)d)$ with $G = PP_n/\Delta$, so $y = T_d\, d$ with $T_d = G(1 - Q)/(1 + GC)$. Let $M = N D_p (q - 1) + N_p D$. Then

$$\Delta = \frac{N}{D} + \frac{1}{q}\Bigl(\frac{N_p}{D_p} - \frac{N}{D}\Bigr) = \frac{N D_p q + N_p D - N D_p}{D D_p q} = \frac{M}{D D_p q},$$

so $G = N_p N q/M$, $G(1 - Q) = N_p N (q - 1)/M$ and $GC = N_p N q N_c/(M D_c)$. Hence

$$T_d = \frac{N_p N (q - 1)/M}{(M D_c + N_c N_p N q)/(M D_c)} = \frac{N_p N D_c (q - 1)}{\chi}.$$

Every pole of $T_d$ is a root of $\chi$, so it lies in the open left half plane. For $d(s) = d_0/s$, the function $s\,y(s) = T_d(s) d_0$ has no pole in the closed right half plane, and the final value theorem gives $\lim_{t \to \infty} y(t) = T_d(0) d_0$. Since $q(0) = 1$, the numerator of $T_d$ is 0 at $s = 0$, so the limit is 0. $\square$

With minimal realizations of $P$, $C$ and the filter, $\chi$ is the characteristic polynomial of the closed loop: its degree $\deg D_p + \deg N + k + \deg D_c$ is the total number of states.

## Remarks

- **The example.** For $P = 1/(Js)$, $P_n = 1/(J_n s)$, $k = 1$ and $C = k_p$, $M = s(J\tau s + J_n)$ and $\chi = J\tau s^2 + (J_n + k_p\tau)s + k_p$, which is Hurwitz for all positive parameters. The transfer function from $d$ to $y$ is $\tau s/\chi$, and it is 0 at $s = 0$.
- **Exact arithmetic.** With int and Fraction data, lines L1 to L5 compute in Fraction, so the realization of the tests is exact.
