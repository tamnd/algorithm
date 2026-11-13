---
title: The first and second order product formulas have errors at most t^2 alpha_1/(2r) and t^3 beta_2/r^2
proves: [correctness]
status: full
---

We use the pseudocode of the page. $H = H_1 + \cdots + H_L$ with Hermitian $H_j = c_j P_j$, $T_{j+1} = H_{j+1} + \cdots + H_L$, and $\|\cdot\|$ is the spectral norm. $U(s) = e^{-iHs}$ and $\delta = t/r$ (line L1).

**What the list computes.** Lines L3 to L9 append, for each of the $r$ steps, the factors of one step in the order they act. For order 1 the step is $S_1(\delta) = e^{-iH_L\delta} \cdots e^{-iH_1\delta}$ (the first factor on the right). For order 2 lines L7, L8 and L9 give
$$S_2(\delta) = e^{-iH_1\delta/2} \cdots e^{-iH_{L-1}\delta/2} \, e^{-iH_L\delta} \, e^{-iH_{L-1}\delta/2} \cdots e^{-iH_1\delta/2}.$$
Line L10 only joins neighbors $e^{-i\theta P}$ and $e^{-i\theta' P}$ with the same string, and $e^{-i\theta P}e^{-i\theta' P} = e^{-i(\theta + \theta')P}$ because the two matrices commute. So the circuit is $S(\delta)^r$ with $S = S_1$ or $S = S_2$.

**Lemma 1 (errors add).** For unitaries $U_1, U_2, W_1, W_2$, $\|U_1U_2 - W_1W_2\| \le \|U_1 - W_1\| + \|U_2 - W_2\|$. Hence $\|S^r - U^r\| \le r\|S - U\|$ for unitaries $S$ and $U$.

*Proof.* $U_1U_2 - W_1W_2 = U_1(U_2 - W_2) + (U_1 - W_1)W_2$, and unitaries have norm 1. The second claim follows by induction on $r$, with $U_1 = S$, $U_2 = S^{r-1}$, $W_1 = U$, $W_2 = U^{r-1}$. $\square$

**Lemma 2 (Duhamel).** Let $S(s)$ be a differentiable family of unitaries with $S(0) = I$ and $S'(s) = -iG(s)S(s)$ for Hermitian $G(s)$. Then
$$\|S(\delta) - U(\delta)\| \le \int_0^\delta \|G(s) - H\|\,ds.$$

*Proof.* $\frac{d}{ds}\big(U(\delta - s)S(s)\big) = U(\delta - s)(iH)S(s) + U(\delta - s)(-iG(s))S(s) = -i\,U(\delta - s)(G(s) - H)S(s)$. Integrating from $0$ to $\delta$ gives $S(\delta) - U(\delta) = -i\int_0^\delta U(\delta - s)(G(s) - H)S(s)\,ds$. The outer factors are unitary. $\square$

**Lemma 3 (conjugation).** For Hermitian $A$ and any matrix $B$, let $f(s) = e^{-iAs}Be^{iAs}$. Then $f(0) = B$, $f'(0) = -i[A, B]$, and
$$\|f(s) - B\| \le |s|\,\|[A, B]\|, \qquad \|f(s) - B + is[A, B]\| \le \frac{s^2}{2}\|[A, [A, B]]\|.$$

*Proof.* $f'(u) = -ie^{-iAu}[A, B]e^{iAu}$ and $f''(u) = -e^{-iAu}[A, [A, B]]e^{iAu}$, and conjugation by a unitary keeps the norm. The first bound is $\|\int_0^s f'(u)\,du\|$, and the second is Taylor's formula with the integral remainder $\int_0^s (s - u) f''(u)\,du$. $\square$

**Two terms, first order.** Let $A$ and $B$ be Hermitian and $S(s) = e^{-iAs}e^{-iBs}$. Then $S'(s) = -i(A + e^{-iAs}Be^{iAs})S(s)$, so $G(s) - (A + B) = e^{-iAs}Be^{iAs} - B$, which has norm at most $s\|[A, B]\|$ by Lemma 3. Lemma 2 gives $\|S(\delta) - e^{-i(A+B)\delta}\| \le (\delta^2/2)\|[A, B]\|$. The order $e^{-iBs}e^{-iAs}$ gives the same bound with $\|[B, A]\| = \|[A, B]\|$.

**Two terms, second order.** Let $S(s) = e^{-iAs/2}e^{-iBs}e^{-iAs/2}$. The product rule gives $S'(s) = -iG(s)S(s)$ with
$$G(s) = \frac{A}{2} + e^{-iAs/2}Be^{iAs/2} + S(s)\frac{A}{2}S(s)^{-1} = e^{-iAs/2}\Big(\frac{A}{2} + B + e^{-iBs}\frac{A}{2}e^{iBs}\Big)e^{iAs/2},$$
since $e^{-iAs/2}$ commutes with $A$. Conjugating by $e^{iAs/2}$, which keeps the norm,
$$\|G(s) - (A + B)\| = \Big\| \tfrac12\big(e^{-iBs}Ae^{iBs} - A\big) - \big(e^{iAs/2}Be^{-iAs/2} - B\big) \Big\|.$$
By Lemma 3, $e^{-iBs}Ae^{iBs} = A - is[B, A] + R_1$ with $\|R_1\| \le (s^2/2)\|[B, [B, A]]\|$, and $e^{iAs/2}Be^{-iAs/2} = B + (is/2)[A, B] + R_2$ with $\|R_2\| \le (s^2/8)\|[A, [A, B]]\|$ (Lemma 3 with $-A/2$ in place of $A$). The terms of first order in $s$ are $-\tfrac{is}{2}[B, A] - \tfrac{is}{2}[A, B] = 0$. So
$$\|G(s) - (A + B)\| \le \frac{s^2}{4}\|[B, [B, A]]\| + \frac{s^2}{8}\|[A, [A, B]]\|,$$
and Lemma 2 gives
$$\|S(\delta) - e^{-i(A+B)\delta}\| \le \delta^3\Big(\frac{\|[B, [B, A]]\|}{12} + \frac{\|[A, [A, B]]\|}{24}\Big).$$

**Many terms.** By induction on $L$; one term has no error. For the first order step, $S_1(\delta)$ for $H_1, \ldots, H_L$ is $S_1'(\delta)\,e^{-iH_1\delta}$, where $S_1'$ is the step for $H_2, \ldots, H_L$. By Lemma 1,
$$\|S_1(\delta) - U(\delta)\| \le \|S_1'(\delta) - e^{-iT_2\delta}\| + \|e^{-iT_2\delta}e^{-iH_1\delta} - e^{-i(H_1 + T_2)\delta}\|,$$
and the two-term bound with $A = H_1$, $B = T_2$ gives $(\delta^2/2)\|[H_1, T_2]\|$ for the second part. The induction hypothesis bounds the first part by $(\delta^2/2)\sum_{j \ge 2}\|[H_j, T_{j+1}]\|$. So one step has error at most $\delta^2\alpha_1/2$. For the second order step, $S_2(\delta) = e^{-iH_1\delta/2}S_2'(\delta)e^{-iH_1\delta/2}$ with $S_2'$ the symmetric step for $H_2, \ldots, H_L$, and in the same way
$$\|S_2(\delta) - U(\delta)\| \le \|S_2'(\delta) - e^{-iT_2\delta}\| + \|e^{-iH_1\delta/2}e^{-iT_2\delta}e^{-iH_1\delta/2} - e^{-i(H_1 + T_2)\delta}\|.$$
The second part is the two-term bound with $A = H_1$ and $B = T_2$, and the sum over the induction is $\delta^3\beta_2$.

**Conclusion.** By Lemma 1, $\|S_1(t/r)^r - e^{-iHt}\| \le r(t/r)^2\alpha_1/2 = t^2\alpha_1/(2r)$ and $\|S_2(t/r)^r - e^{-iHt}\| \le r(t/r)^3\beta_2 = t^3\beta_2/r^2$. With $r = \lceil t^2\alpha_1/(2\epsilon)\rceil$ or $r = \lceil t^{3/2}(\beta_2/\epsilon)^{1/2}\rceil$, the error is at most $\epsilon$. If all terms commute, every commutator is zero and the circuit equals $e^{-iHt}$ exactly. $\blacksquare$
