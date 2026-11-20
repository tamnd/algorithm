---
title: SUPG is consistent, has a unique solution, and with the optimal tau is exact at the nodes in one dimension
proves: [correctness]
status: full
---

**Setting.** The problem is $-\varepsilon u'' + a u' = f$ on $(0, 1)$ with $u(0) = g_0$ and $u(1) = g_1$, where $\varepsilon > 0$ and $a \ne 0$ are constants. The mesh has the nodes $x_j = jh$, $h = 1/m$, $m \ge 2$, and $V_h$ is the space of continuous piecewise linear functions. $V_{h,0}$ is the subspace of functions that vanish at $0$ and $1$. For $\tau \ge 0$, the SUPG problem is: find $u_h \in V_h$ with $u_h(0) = g_0$, $u_h(1) = g_1$ and

$$B(u_h, v) = L(v) \quad\text{for all } v \in V_{h,0},$$

$$B(w, v) = \varepsilon(w', v') + (a w', v) + \tau\sum_K (-\varepsilon w'' + a w',\ a v')_K, \qquad L(v) = (f, v) + \tau\sum_K (f, a v')_K,$$

where $(\cdot,\cdot)_K$ is the $L^2$ product on the cell $K$ and $(\cdot,\cdot)$ is the product on $(0, 1)$. Lines L3 to L6 of the algorithm compute the matrix of $B$ and the vector of $L$ in the hat basis, cell by cell. The proof of [finite element assembly](/finite-element-assembly/) shows that this gives $B(\phi_s, \phi_r)$ and $L(\phi_r)$ when the quadrature of line L5 is exact, and Boole's rule is exact when $f$ is a polynomial of degree at most 4. Line L7 fixes the two boundary values, so lines L8 and L9 return the solution of the SUPG problem if it exists. We prove four claims.

**Claim 1 (consistency).** If the exact solution $u$ is in $H^2(0, 1)$, then $B(u, v) = L(v)$ for all $v \in V_{h,0}$, so $B(u - u_h, v) = 0$.

*Proof.* Integration by parts on $(0, 1)$, with $v(0) = v(1) = 0$, gives $\varepsilon(u', v') = (-\varepsilon u'', v)$. So $\varepsilon(u', v') + (a u', v) = (-\varepsilon u'' + a u', v) = (f, v)$. On each cell $-\varepsilon u'' + a u' - f = 0$, so $\tau\sum_K(-\varepsilon u'' + a u' - f, a v')_K = 0$. Adding the two identities gives $B(u, v) = L(v)$. Subtract $B(u_h, v) = L(v)$. $\square$

**Claim 2 (the extra diffusion).** For $w, v \in V_h$, $B(w, v) = (\varepsilon + \tau a^2)(w', v') + (a w', v)$. For a constant $f = c$ and an interior hat function $\phi_i$, $1 \le i \le m - 1$, $L(\phi_i) = (c, \phi_i) = ch$.

*Proof.* On each cell $w$ is linear, so $w'' = 0$ there and $(-\varepsilon w'' + a w', a v')_K = a^2(w', v')_K$. Summing over $K$ gives the first identity. For the second, $\tau\sum_K(c, a\phi_i')_K = \tau a c\int_0^1\phi_i'\,dx = \tau a c\,(\phi_i(1) - \phi_i(0)) = 0$, and $(c, \phi_i) = ch$ because the hat function has area $h$. $\square$

**Claim 3 (unique solution).** For every $\tau \ge 0$ the SUPG problem has exactly one solution. If $\varepsilon' = \varepsilon + \tau a^2$ satisfies $\varepsilon' \ge |a|h/2$, the Thomas algorithm of line L8 meets no zero pivot.

*Proof.* Write $u_h = w_g + z$ with $w_g \in V_h$ the function with nodal values $(g_0, 0, \ldots, 0, g_1)$ and $z \in V_{h,0}$. The problem becomes $B(z, v) = L(v) - B(w_g, v)$ for all $v \in V_{h,0}$, a square linear system of size $m - 1$. It has a unique solution if $B(z, z) = 0$ implies $z = 0$ on $V_{h,0}$. By Claim 2, $B(z, z) = \varepsilon'\|z'\|^2 + a\int_0^1 z' z\,dx = \varepsilon'\|z'\|^2 + \tfrac{a}{2}(z(1)^2 - z(0)^2) = \varepsilon'\|z'\|^2$. If this is $0$, then $z' = 0$, so $z$ is constant, and $z(0) = 0$ gives $z = 0$.

For the pivots: by Claim 2, row $i$ of the inner system ($1 \le i \le m - 1$) has the entries

$$\ell = -\frac{\varepsilon'}{h} - \frac{a}{2}, \qquad d = \frac{2\varepsilon'}{h}, \qquad \mu = -\frac{\varepsilon'}{h} + \frac{a}{2}$$

for $U_{i-1}$, $U_i$ and $U_{i+1}$, except that line L7 removes $\ell$ from the first row and $\mu$ from the last. If $\varepsilon' \ge |a|h/2$, both $\ell$ and $\mu$ are $\le 0$, so $|\ell| + |\mu| = 2\varepsilon'/h = d > 0$. The Thomas algorithm uses the pivots $p_1 = d$ and $p_i = d - \ell c'_{i-1}$ for $i \ge 2$, with $c'_i = \mu/p_i$.

- If $\varepsilon' > |a|h/2$, then $\ell < 0$ and $\mu < 0$. We show by induction that $p_i > |\mu|$, so $p_i > 0$ and $|c'_i| < 1$. For $i = 1$, $p_1 = d = |\ell| + |\mu| > |\mu|$. For the step, the hypothesis $|c'_{i-1}| < 1$ and $\ell \ne 0$ give $p_i \ge d - |\ell|\,|c'_{i-1}| > d - |\ell| = |\mu|$.
- If $\varepsilon' = |a|h/2$, one of $\ell$ and $\mu$ is $0$, so the matrix is bidiagonal. If $\mu = 0$, every $c'_i$ is $0$ and every pivot is $d$. If $\ell = 0$, again every pivot is $d - 0 = d$.

In both cases no pivot is zero. $\square$

**Claim 4 (nodal exactness).** Let $\mathrm{Pe} = |a|h/(2\varepsilon)$ and $\tau = \frac{h}{2|a|}\bigl(\coth\mathrm{Pe} - \frac{1}{\mathrm{Pe}}\bigr)$, the value of line L2. If $f = c$ is constant, then $U_j = u(x_j)$ for $j = 0, \ldots, m$, where $u$ is the exact solution.

*Proof.* First, $\varepsilon' = \varepsilon + \tau a^2 = \varepsilon + \frac{|a|h}{2}\coth\mathrm{Pe} - \frac{|a|h}{2\mathrm{Pe}} = \frac{|a|h}{2}\coth\mathrm{Pe}$, because $\frac{|a|h}{2\mathrm{Pe}} = \varepsilon$. Since $\coth$ is odd, this is also $\frac{ah}{2}\coth\frac{ah}{2\varepsilon}$, and $\varepsilon' > |a|h/2$ because $\coth x > 1$ for $x > 0$.

By Claim 2 and the entries in the proof of Claim 3, row $i$ of the system, divided by $h$, reads

$$R_i(U) = -\varepsilon'\,\frac{U_{i+1} - 2U_i + U_{i-1}}{h^2} + a\,\frac{U_{i+1} - U_{i-1}}{2h} = c, \qquad 1 \le i \le m - 1.$$

The exact solution is $u(x) = A + Bx + Ce^{rx}$ with $r = a/\varepsilon$, $B = c/a$, and $A$, $C$ fixed by the boundary values. $R_i$ is linear, so we check each term on the nodal values $U_j = u(x_j)$:

1. For $U_j = 1$: $R_i = 0$.
2. For $U_j = x_j$: the second difference is $0$ and the centered difference is $1$, so $R_i = a$. Times $B = c/a$ this gives $c$.
3. For $U_j = e^{rx_j}$: write $U_{i\pm1} = U_i e^{\pm rh}$. Then $R_i = U_i\bigl(-\varepsilon'\frac{2\cosh(rh) - 2}{h^2} + a\frac{\sinh(rh)}{h}\bigr)$. With $\cosh(rh) - 1 = 2\sinh^2(rh/2)$ and $\sinh(rh) = 2\sinh(rh/2)\cosh(rh/2)$, this is $\frac{2U_i\sinh(rh/2)}{h}\bigl(-\frac{2\varepsilon'}{h}\sinh(rh/2) + a\cosh(rh/2)\bigr)$. It is $0$ because $\varepsilon' = \frac{ah}{2}\coth\frac{rh}{2}$, and $\frac{rh}{2} = \frac{ah}{2\varepsilon}$.

So $R_i(u(x_0), \ldots, u(x_m)) = 0 + c + 0 = c$ for every interior $i$, and the nodal values of $u$ take the right boundary values. By Claim 3 the discrete system has exactly one solution, so it is the vector of nodal values of $u$. $\square$

**Conclusion.** Lines L3 to L6 assemble $B$ and $L$, line L7 imposes the boundary values, and line L8 solves the system without a zero pivot whenever $\varepsilon + \tau a^2 \ge |a|h/2$, which holds for the $\tau$ of line L2. By Claim 3 the returned vector is the unique SUPG solution, by Claim 1 the method is consistent, so the error satisfies Galerkin orthogonality for the form $B$, and by Claim 4 the result is exact at the nodes when $f$ is constant. $\blacksquare$
