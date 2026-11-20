---
title: The Steger-Warming and van Leer splittings add up to the Euler flux, the van Leer parts are smooth at the sonic points, and the scalar splitting scheme is TVD
proves: [correctness]
status: full
---

**Setting.** The scheme stores cell averages $U_j^n$ on a uniform grid with width $\Delta x$ and steps $U_j^{n+1} = U_j^n - \lambda(F_{j+1/2} - F_{j-1/2})$ with $\lambda = \Delta t/\Delta x$ (line L9). The face flux is $F_{j+1/2} = F^+(U_j) + F^-(U_{j+1})$ (line L6). For the Euler equations, $U = (\rho, \rho u, E)$, $p = (\gamma - 1)(E - \frac12\rho u^2)$, $c = \sqrt{\gamma p/\rho}$, $H = (E + p)/\rho$ and $M = u/c$. The eigenvalues of the Jacobian $A(U) = \partial F/\partial U$ are $\lambda_1 = u - c$, $\lambda_2 = u$, $\lambda_3 = u + c$, with right eigenvectors $r_1 = (1, u - c, H - uc)$, $r_2 = (1, u, \frac12 u^2)$ and $r_3 = (1, u + c, H + uc)$. For a real number $x$, $x^+ = \max(x, 0)$ and $x^- = \min(x, 0)$.

**Lemma 1 (the state in eigenvector coordinates).** $U = w_1 r_1 + w_2 r_2 + w_3 r_3$ with $w_1 = w_3 = \rho/(2\gamma)$ and $w_2 = \rho(\gamma - 1)/\gamma$.

*Proof.* Mass: $2\rho/(2\gamma) + \rho(\gamma - 1)/\gamma = \rho$. Momentum: $\frac{\rho}{2\gamma}\big((u - c) + (u + c)\big) + \frac{\rho(\gamma - 1)}{\gamma}u = \rho u$. Energy: $\frac{\rho}{2\gamma}\cdot 2H + \frac{\rho(\gamma - 1)}{\gamma}\cdot\frac{u^2}{2}$. Here $\rho H = E + p = \frac{\gamma p}{\gamma - 1} + \frac12\rho u^2$, so $\rho H/\gamma = \frac{p}{\gamma - 1} + \frac{\rho u^2}{2\gamma}$. Adding $\frac{(\gamma - 1)\rho u^2}{2\gamma}$ gives $\frac{p}{\gamma - 1} + \frac12\rho u^2 = E$. $\square$

**Lemma 2 (homogeneity).** $F(sU) = sF(U)$ for $s > 0$, and $F(U) = A(U)U$.

*Proof.* Scaling $U$ by $s$ scales $\rho$, $\rho u$, $E$ and $p$ by $s$ and leaves $u$ unchanged. Each flux component, $\rho u$, $\rho u^2 + p$ and $u(E + p)$, is then scaled by $s$. Differentiating $F(sU) = sF(U)$ with respect to $s$ at $s = 1$ gives $A(U)U = F(U)$ (Euler's theorem on homogeneous functions). $\square$

**Theorem 1 (Steger-Warming).** Let $F^\pm(U) = \sum_k \lambda_k^\pm w_k r_k$ (lines L1 and L2). Then $F^+ + F^- = F$, $F^\pm = A^\pm U$ with $A^\pm = R\Lambda^\pm R^{-1}$, the eigenvalues of $A^+$ are $\lambda_k^+ \ge 0$ and those of $A^-$ are $\lambda_k^- \le 0$. If $u \ge c$ then $F^+ = F$ and $F^- = 0$, and if $u \le -c$ then $F^+ = 0$ and $F^- = F$.

*Proof.* By Lemma 1 and $Ar_k = \lambda_k r_k$, $A U = \sum_k \lambda_k w_k r_k$, and by Lemma 2 this is $F(U)$. Since $\lambda_k^+ + \lambda_k^- = \lambda_k$ for each $k$, $F^+ + F^- = \sum_k \lambda_k w_k r_k = F$. The matrix $R\Lambda^\pm R^{-1}$ maps $U = \sum_k w_k r_k$ to $\sum_k \lambda_k^\pm w_k r_k = F^\pm$, and its eigenvalues are the entries of $\Lambda^\pm$. If $u \ge c$, all three $\lambda_k \ge 0$, so $\lambda_k^+ = \lambda_k$ and $\lambda_k^- = 0$, which gives $F^+ = F$ and $F^- = 0$. The case $u \le -c$ is the mirror. $\square$

Written out, $F^\pm = \frac{\rho}{2\gamma}\big(\lambda_1^\pm + 2(\gamma - 1)\lambda_2^\pm + \lambda_3^\pm,\ (u - c)\lambda_1^\pm + 2(\gamma - 1)u\lambda_2^\pm + (u + c)\lambda_3^\pm,\ (H - uc)\lambda_1^\pm + (\gamma - 1)u^2\lambda_2^\pm + (H + uc)\lambda_3^\pm\big)$. The map $x \mapsto x^+$ has a kink at $x = 0$, so $F^\pm$ is continuous but its derivative jumps where $u = \pm c$ or $u = 0$.

**Theorem 2 (van Leer).** For $|M| < 1$ let

$$F^\pm = \pm\frac{\rho c}{4}(M \pm 1)^2\Big(1,\ \frac{(\gamma - 1)u \pm 2c}{\gamma},\ \frac{((\gamma - 1)u \pm 2c)^2}{2(\gamma^2 - 1)}\Big)$$

(lines L4 and L5), and for $|M| \ge 1$ let the parts be as in Theorem 1 (line L3). Then $F^+ + F^- = F$ for every state, and $F^+$ and $F^-$ are continuous with continuous first derivatives across $M = 1$ and $M = -1$.

*Proof.* Write $a = (\gamma - 1)u$, $X = (M + 1)(a + 2c)$ and $Y = (M - 1)(a - 2c)$.

Mass: $\frac{\rho c}{4}\big((M + 1)^2 - (M - 1)^2\big) = \frac{\rho c}{4}\cdot 4M = \rho u$.

Momentum: $\frac{\rho c}{4\gamma}\big((M + 1)^2(a + 2c) - (M - 1)^2(a - 2c)\big)$. The bracket is $a\cdot 4M + 2c\big((M + 1)^2 + (M - 1)^2\big) = 4aM + 4c(M^2 + 1)$. So the sum is $\frac{\rho}{\gamma}\big((\gamma - 1)u^2 + u^2 + c^2\big) = \rho u^2 + \rho c^2/\gamma = \rho u^2 + p$.

Energy: $\frac{\rho c}{8(\gamma^2 - 1)}(X^2 - Y^2)$. Expanding, $X - Y = 2a + 4cM = 2(\gamma + 1)u$ and $X + Y = 2aM + 4c$. So $X^2 - Y^2 = 4(\gamma + 1)u\big((\gamma - 1)uM + 2c\big)$, and the sum is $\frac{\rho c u}{2(\gamma - 1)}\big((\gamma - 1)uM + 2c\big) = \frac{\rho u}{2(\gamma - 1)}\big((\gamma - 1)u^2 + 2c^2\big) = \rho u\big(\tfrac12 u^2 + \tfrac{c^2}{\gamma - 1}\big) = \rho u H = u(E + p)$.

So $F^+ + F^- = F$ for $|M| < 1$, and by Theorem 1 also for $|M| \ge 1$. At $M = 1$, the subsonic $F^-$ is the product of $(M - 1)^2$ and a smooth function of $(\rho, u, c)$, so $F^-$ and its first derivatives are zero there. The supersonic $F^-$ is identically zero, so $F^-$ is $C^1$ across $M = 1$. Then $F^+ = F - F^-$ is $C^1$ there too, because $F$ is smooth. The case $M = -1$ is the mirror, with $(M + 1)^2$ in $F^+$. $\square$

**Theorem 3 (consistency and conservation).** For both splittings, $F_{j+1/2} = F(U)$ when $U_j = U_{j+1} = U$, and on a periodic grid the sums $\sum_j U_j$ are kept. So, by the [Lax-Wendroff theorem](/lax-wendroff-theorem/), a limit that the scheme converges to boundedly in $L^1_{loc}$ is a weak solution.

*Proof.* Consistency is $F^+(U) + F^-(U) = F(U)$, which is Theorems 1 and 2. Conservation: each face flux enters cell $j$ with the factor $-\lambda$ and cell $j + 1$ with $+\lambda$, so the sum over a periodic grid telescopes. $\square$

**Theorem 4 (scalar law: TVD).** Let $f = f^+ + f^-$ with $f^+$ nondecreasing, $f^-$ nonincreasing, both Lipschitz, and let $F_{j+1/2} = f^+(u_j) + f^-(u_{j+1})$. If $\lambda \sup(f^{+\prime} - f^{-\prime}) \le 1$, then the scheme does not increase $\sum_j |u_{j+1} - u_j|$, and it is monotone.

*Proof.* With $\Delta_{j+1/2} = u_{j+1} - u_j$,

$$u_j^{n+1} = u_j - \lambda\big(f^+(u_j) - f^+(u_{j-1})\big) - \lambda\big(f^-(u_{j+1}) - f^-(u_j)\big) = u_j - C_{j-1/2}\Delta_{j-1/2} + D_{j+1/2}\Delta_{j+1/2},$$

where $C_{j-1/2} = \lambda\frac{f^+(u_j) - f^+(u_{j-1})}{\Delta_{j-1/2}} \ge 0$ and $D_{j+1/2} = -\lambda\frac{f^-(u_{j+1}) - f^-(u_j)}{\Delta_{j+1/2}} \ge 0$ (read as 0 when the difference is 0). Then $C_{j+1/2} + D_{j+1/2} = \lambda\frac{(f^+ - f^-)(u_{j+1}) - (f^+ - f^-)(u_j)}{\Delta_{j+1/2}} \le \lambda\sup(f^{+\prime} - f^{-\prime}) \le 1$. By Harten's lemma (Harten 1983), the total variation does not increase. Monotone: the update $H(u_{j-1}, u_j, u_{j+1})$ is nondecreasing in $u_{j-1}$ (since $f^+$ is nondecreasing), in $u_{j+1}$ (since $f^-$ is nonincreasing), and in $u_j$, because $u_j \mapsto u_j - \lambda(f^+ - f^-)(u_j)$ has slope $1 - \lambda(f^{+\prime} - f^{-\prime}) \ge 0$. $\square$

For Burgers' equation the choice $f^+ = (u^+)^2/2$, $f^- = (u^-)^2/2$ has $f^{+\prime} - f^{-\prime} = |u|$, so the condition is $\lambda\max|u| \le 1$. The test runs this case with $\lambda\max|u| = 0.9$ on random data and checks that the total variation does not increase in 40 steps. Monotone schemes converge to the entropy solution (Crandall and Majda 1980).

**Proposition 5 (a contact at rest is not kept).** Let $W_L = (\rho_L, 0, p)$ and $W_R = (\rho_R, 0, p)$ with $\rho_L \ne \rho_R$. The van Leer mass flux at the face is $(\rho_L c_L - \rho_R c_R)/4$ and the Steger-Warming one is $(\rho_L c_L - \rho_R c_R)/(2\gamma)$. Both are nonzero, so the exact steady solution is not a steady solution of the scheme.

*Proof.* At $M = 0$, the van Leer mass parts are $\pm\rho c/4$, and the Steger-Warming parts are $\frac{\rho}{2\gamma}(\lambda_1^\pm + \lambda_3^\pm) = \pm\frac{\rho c}{2\gamma}$. So the face mass flux is the difference of the two $\rho c$ values times $\frac14$ or $\frac{1}{2\gamma}$. With equal pressures, $\rho c = \sqrt{\gamma p \rho}$ is strictly increasing in $\rho$, so $\rho_L c_L \ne \rho_R c_R$. $\square$
