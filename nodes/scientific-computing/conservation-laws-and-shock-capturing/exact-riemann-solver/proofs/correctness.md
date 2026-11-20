---
title: The exact Riemann solver finds the unique star pressure and samples the exact solution
proves: [correctness]
status: full
---

**Setting.** The data are $W_L = (\rho_L, u_L, p_L)$ and $W_R = (\rho_R, u_R, p_R)$ with positive densities and pressures, $\gamma > 1$, $c_K = \sqrt{\gamma p_K/\rho_K}$ and $z = (\gamma - 1)/(2\gamma)$. The solution of the Riemann problem for the Euler equations of an ideal gas is self-similar and has three waves: a left wave (shock or rarefaction), a contact discontinuity, and a right wave. Pressure and velocity are continuous across the contact, so the two star states between the outer waves share $p^*$ and $u^*$ and differ only in density (LeVeque 2002, Section 14.11; Toro 2009, Section 4.1). For $K \in \{L, R\}$ let

$$f_K(p) = \begin{cases} (p - p_K)\sqrt{\dfrac{A_K}{p + B_K}}, & p > p_K, \\[2mm] \dfrac{2c_K}{\gamma - 1}\Big(\big(\tfrac{p}{p_K}\big)^{z} - 1\Big), & p \le p_K, \end{cases} \qquad A_K = \frac{2}{(\gamma + 1)\rho_K}, \quad B_K = \frac{\gamma - 1}{\gamma + 1}p_K,$$

and $f(p) = f_L(p) + f_R(p) + u_R - u_L$. Lines L4 and L5 compute $f$ and $f'$ with these formulas.

**Lemma 1 (wave relations).** A left wave connects $W_L$ to a star state with pressure $p$ and velocity $u$ exactly when $u = u_L - f_L(p)$. A right wave connects a star state $(p, u)$ to $W_R$ exactly when $u = u_R + f_R(p)$.

*Proof.* Take the left side; the right side is the mirror image $x \to -x$, $u \to -u$. If $p \le p_L$ the wave is a rarefaction. Across it the entropy is constant, so $p/\rho^\gamma$ is constant and $c/c_L = (p/p_L)^z$, and the Riemann invariant $u + 2c/(\gamma - 1)$ of the 1-family is constant (LeVeque 2002, Section 14.10). So $u = u_L + \frac{2}{\gamma - 1}(c_L - c) = u_L - f_L(p)$.

If $p > p_L$ the wave is a shock with speed $S$. Let $Q = \rho_L(u_L - S) = \rho(u - S)$ be the mass flux through it, from the first Rankine-Hugoniot condition. The second condition gives $Q^2 = (p - p_L)/(1/\rho_L - 1/\rho)$, and the third gives the Hugoniot density ratio $\rho/\rho_L = (r + g)/(g r + 1)$ with $r = p/p_L$ and $g = (\gamma - 1)/(\gamma + 1)$ (Toro 2009, Sections 3.1.3 and 4.2.1). Then $1/\rho_L - 1/\rho = (1 - g)(r - 1)/(\rho_L(r + g))$, and since $1 - g = 2/(\gamma + 1)$,

$$Q^2 = \frac{\rho_L p_L(r + g)}{1 - g} = \frac{\gamma + 1}{2}\rho_L(p + B_L) = \frac{p + B_L}{A_L}.$$

Since $u_L - S = Q/\rho_L$ and $u - S = Q/\rho$, with $Q > 0$ for a left shock, $u - u_L = -Q(1/\rho_L - 1/\rho) = -(p - p_L)/Q$. So $u = u_L - (p - p_L)\sqrt{A_L/(p + B_L)} = u_L - f_L(p)$. $\square$

Subtracting the two relations of Lemma 1 gives $f(p^*) = 0$, and adding them gives $u^* = \frac12(u_L + u_R) + \frac12(f_R(p^*) - f_L(p^*))$, which is line L9.

**Lemma 2 (shape of $f$).** On $(0, \infty)$ each $f_K$ is $C^1$, strictly increasing and concave. So $f$ is too.

*Proof.* On the rarefaction branch $f_K'(p) = \frac{1}{\rho_K c_K}(p/p_K)^{-(\gamma + 1)/(2\gamma)}$, which is positive and decreasing. On the shock branch, with $q = \sqrt{A_K/(p + B_K)}$,

$$f_K'(p) = q\Big(1 - \frac{p - p_K}{2(p + B_K)}\Big), \qquad f_K''(p) = -\sqrt{A_K}\,(p + B_K)^{-5/2}\Big(\frac{p}{4} + B_K + \frac{3p_K}{4}\Big).$$

The bracket in $f_K'$ is positive because $p - p_K < 2(p + B_K)$, and $f_K'' < 0$. At $p = p_K$ the shock branch gives $f_K'(p_K) = \sqrt{A_K/(p_K + B_K)} = \sqrt{1/(\gamma\rho_K p_K)} = 1/(\rho_K c_K)$, the same value as the rarefaction branch, and both branches give $f_K(p_K) = 0$. So $f_K'$ is continuous, positive, and decreasing on each branch, hence decreasing on $(0, \infty)$. $\square$

**Lemma 3 (existence and the vacuum test).** $f$ has a positive root exactly when $\frac{2}{\gamma - 1}(c_L + c_R) > u_R - u_L$, and then the root is unique.

*Proof.* As $p \to 0^+$ both sides are on the rarefaction branch and $f(p) \to u_R - u_L - \frac{2}{\gamma - 1}(c_L + c_R)$. As $p \to \infty$ both sides are on the shock branch, where $f_K(p)$ grows like $\sqrt{p}$, so $f(p) \to \infty$. By Lemma 2, $f$ is continuous and strictly increasing, so it has a positive root if and only if its limit at $0^+$ is negative, and the root is unique. $\square$

So line L1 reports a vacuum exactly when no star pressure exists. The guess of line L2 is the exact root when both waves are rarefactions, because then $f(p) = \frac{2}{\gamma - 1}\big(c_L((p/p_L)^z - 1) + c_R((p/p_R)^z - 1)\big) + u_R - u_L$ is linear in $p^z$. It is positive by the test of line L1.

**Theorem (Newton iteration).** Let $p^*$ be the root and $\varepsilon = \mathrm{tol}\cdot\min(p_L, p_R)$, and assume $p^* \ge \varepsilon$. From any $p_0 > 0$, the iterates of lines L3 to L8 satisfy $0 < p_1 \le p^*$, then increase monotonically to $p^*$, and the convergence is quadratic.

*Proof.* Concavity gives $f(q) \le f(p) + f'(p)(q - p)$ for all $p, q > 0$. With $q = p - f(p)/f'(p)$ the right side is $0$, so $f(q) \le 0$ and $q \le p^*$ by Lemma 2, whenever $q > 0$. If $q \le 0$, line L6 replaces it by $\varepsilon \le p^*$. So every iterate after the first lies in $(0, p^*]$. For such an iterate $f(p) \le 0$ and $f'(p) > 0$, so the next iterate is at least $p$, and it is positive and at most $p^*$ by the first argument, so line L6 never fires again. The sequence is nondecreasing and bounded by $p^*$, so it has a limit $\ell \le p^*$. On $[p_1, p^*]$ the derivative $f'$ is continuous with minimum $f'(p^*) > 0$, so passing to the limit in $p_{k+1} = p_k - f(p_k)/f'(p_k)$ gives $f(\ell) = 0$ and $\ell = p^*$. The derivative $f'$ has bounded one-sided derivatives on $[p_1, p^*]$, so it is Lipschitz there with some constant $M$, and the usual Newton estimate gives $p^* - p_{k+1} \le \frac{M}{2f'(p^*)}(p^* - p_k)^2$. $\square$

*Stopping test.* Write $e_k = p^* - p_k$ and $C = M/(2f'(p^*))$. Once $Ce_k \le \frac12$, we have $e_k = (p_{k+1} - p_k) + e_{k+1} \le (p_{k+1} - p_k) + \frac12e_k$, so $e_k \le 2(p_{k+1} - p_k)$ and $e_{k+1} \le 4C(p_{k+1} - p_k)^2$. So when line L8 stops on a relative change below tol, the relative error of the returned pressure is of order $\mathrm{tol}^2$ times a constant of the problem. Because the iterates increase, the loop ends after finitely many steps; the code raises an error if maxit steps are not enough.

**Star densities and wave speeds (lines L10 and L11).** On a shock side, $\rho^*_K$ is the Hugoniot density ratio of Lemma 1 times $\rho_K$, and the shock speed follows from $Q$: $S_L = u_L - Q/\rho_L = u_L - c_L\sqrt{\frac{\gamma + 1}{2\gamma}\frac{p^*}{p_L} + z}$, and the mirror formula with a plus sign on the right. On a rarefaction side, $\rho^*_K = \rho_K(p^*/p_K)^{1/\gamma}$ by isentropy, the head moves at $u_K \mp c_K$ and the tail at $u^* \mp c^*_K$ with $c^*_K = c_K(p^*/p_K)^z$. The waves are ordered: the left wave lies at $\xi < u^*$ and the right wave at $\xi > u^*$ (Toro 2009, Section 4.4).

**Sampling (lines L12 to L15).** Take $\xi \le u^*$, the left side; the right side is the mirror image. Outside the left wave the solution is $W_L$ (line L13). Between the tail of the wave and the contact it is the left star state (line L14). Inside a left fan, the characteristic through the origin gives $u - c = \xi$, the Riemann invariant gives $u + \frac{2c}{\gamma - 1} = u_L + \frac{2c_L}{\gamma - 1}$, and the isentropic relation gives $\rho \propto c^{2/(\gamma - 1)}$ and $p \propto c^{2\gamma/(\gamma - 1)}$. Solving the two linear equations,

$$\frac{c}{c_L} = w = \frac{2}{\gamma + 1} + \frac{\gamma - 1}{(\gamma + 1)c_L}(u_L - \xi), \qquad u = \frac{2}{\gamma + 1}\Big(c_L + \frac{\gamma - 1}{2}u_L + \xi\Big),$$

$\rho = \rho_Lw^{2/(\gamma - 1)}$ and $p = p_Lw^{2\gamma/(\gamma - 1)}$, which is line L15. At the head $\xi = u_L - c_L$ this gives $w = 1$, and at the tail it gives the star state, so the sampled solution is continuous across the fan. $\blacksquare$

**What the tests check independently.** The Rankine-Hugoniot conditions $S(U^* - U_K) = F(U^*) - F(U_K)$ across every computed shock, the isentropic relation and the Riemann invariant at eleven points of the Sod fan, the root against 200 steps of bisection on $f$ for 200 random data sets, and the integral form of the conservation law on $[-4, 4]$ at $t = 1$.
