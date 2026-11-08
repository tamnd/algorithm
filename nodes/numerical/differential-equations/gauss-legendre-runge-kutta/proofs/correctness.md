---
title: The s-stage Gauss method is collocation of order 2s, algebraically stable, A-stable for Re z < 0, and conserves quadratic invariants
proves: [correctness, termination, convergence]
status: full
---

**Setting.** $c_1 < \cdots < c_s$ are the zeros of the shifted Legendre polynomial $\tilde P_s(\tau) = P_s(2\tau - 1)$ in $(0, 1)$, $\ell_j$ is the Lagrange basis polynomial of degree $s - 1$ with $\ell_j(c_i) = \delta_{ij}$, $a_{ij} = \int_0^{c_i}\ell_j$ and $b_j = \int_0^1\ell_j$, exactly as computed at line L1. We assume the stage equations are solved exactly; the effect of the iteration tolerance is discussed at the end. $\langle\cdot,\cdot\rangle$ is an inner product on $\mathbb{R}^d$ (or a Hermitian one on $\mathbb{C}^d$), $\|\cdot\|$ its norm.

**Lemma 1 (simplifying assumptions).** The tableau satisfies

- $B(2s)$: $\sum_ib_ic_i^{k-1} = 1/k$ for $k = 1, \ldots, 2s$;
- $C(s)$: $\sum_ja_{ij}c_j^{k-1} = c_i^k/k$ for $k = 1, \ldots, s$ and all $i$;
- $b_i > 0$ for all $i$.

*Proof.* For a polynomial $p$ of degree $\le s - 1$, $p = \sum_jp(c_j)\ell_j$, so $\int_0^xp = \sum_jp(c_j)\int_0^x\ell_j$. With $x = c_i$ and $p(\tau) = \tau^{k-1}$ this is $C(s)$; with $x = 1$ it is $B(s)$. The quadrature rule $\sum_jb_jg(c_j)$ is thus exact for degree $\le s - 1$. For $g$ of degree $\le 2s - 1$, divide: $g = q\tilde P_s + r$ with $\deg q, \deg r \le s - 1$. Since $\tilde P_s$ is orthogonal on $[0, 1]$ to all polynomials of degree $< s$, $\int_0^1g = \int_0^1r$, and since $\tilde P_s(c_j) = 0$, $\sum_jb_jg(c_j) = \sum_jb_jr(c_j) = \int_0^1r$. This gives $B(2s)$. Finally $b_i = \sum_jb_j\ell_i(c_j)^2 = \int_0^1\ell_i^2 > 0$, because $\ell_i^2$ has degree $2s - 2 \le 2s - 1$. $\square$

**Lemma 2 (algebraic stability).** The symmetric matrix $M$ with $m_{ij} = b_ia_{ij} + b_ja_{ji} - b_ib_j$ is zero.

*Proof.* Let $V$ be the Vandermonde matrix $V_{ik} = c_i^{k-1}$, $k = 1, \ldots, s$; it is nonsingular because the $c_i$ are distinct, so it suffices to show $V^TMV = 0$. Using $C(s)$ and then $B(2s)$ (note $k + l \le 2s$),

$$\sum_{i,j}b_ic_i^{k-1}a_{ij}c_j^{l-1} = \sum_ib_ic_i^{k-1}\frac{c_i^l}{l} = \frac{1}{l(k + l)},$$

the transposed term gives $\frac{1}{k(k+l)}$, and $\sum_ib_ic_i^{k-1}\sum_jb_jc_j^{l-1} = \frac{1}{kl}$. So $(V^TMV)_{kl} = \frac{1}{l(k+l)} + \frac{1}{k(k+l)} - \frac{1}{kl} = \frac{k + l}{kl(k + l)} - \frac{1}{kl} = 0$. $\square$

**Lemma 3 (collocation).** Let $Y_i$ solve the stage equations and $F_j = f(t_0 + c_jh, Y_j)$. The polynomial $u(t_0 + \tau h) = y_0 + h\sum_jF_j\int_0^\tau\ell_j$ of degree $\le s$ satisfies $u(t_0) = y_0$, $u(t_0 + c_ih) = Y_i$, $u'(t_0 + c_ih) = f(t_0 + c_ih, u(t_0 + c_ih))$ for all $i$, and $u(t_0 + h) = y_1$. Conversely, any polynomial of degree $\le s$ with these collocation conditions yields a solution of the stage equations.

*Proof.* $u(t_0 + c_ih) = y_0 + h\sum_ja_{ij}F_j = Y_i$ by the definition of $a_{ij}$ and the stage equations; $u'(t_0 + \tau h) = \sum_jF_j\ell_j(\tau)$, so $u'(t_0 + c_ih) = F_i = f(t_0 + c_ih, Y_i)$; and $u(t_0 + h) = y_0 + h\sum_jb_jF_j = y_1$. Conversely, $u'$ has degree $\le s - 1$ and is therefore the interpolant $\sum_ju'(t_0 + c_jh)\ell_j$; integrating gives the stage equations with $Y_i = u(t_0 + c_ih)$. $\square$

**Theorem 1 (solvability and termination).** If $hL\|A\|_\infty < 1$ (with $\|\cdot\|_\infty$ the maximum row sum and $L$ the Lipschitz constant in the maximum norm), the stage equations have a unique solution, the fixed-point map $Z \mapsto h(A \otimes I)F(Z)$ is a contraction, and for $h$ small enough the simplified Newton iteration at line L6 converges linearly to it. In any case the loop at line L6 runs at most `max_newton` times per step, and the outer loop $N$ times, so the algorithm terminates (raising an error if the iteration has not converged).

*Proof.* For stacked vectors $Z, W$, $\|h(A \otimes I)(F(Z) - F(W))\|_\infty \le h\|A\|_\infty L\|Z - W\|_\infty$, so Banach's fixed-point theorem applies. Simplified Newton is the fixed-point iteration for $Z \mapsto Z + M^{-1}G(Z)$ with $G(Z) = -Z + h(A \otimes I)F(Z)$ and $M = I - hA \otimes J$; its derivative at the solution is $M^{-1}(hA \otimes (\partial_yf - J))$, of norm $O(h)$ times the variation of $\partial_yf$ over the step, which is smaller than 1 for small $h$. $\square$

**Theorem 2 (order $2s$).** Let $f$ be $C^{2s+1}$ in a neighbourhood of the exact solution on $[t_0, T]$. Then the local error satisfies $\|y(t_0 + h) - y_1\| \le Ch^{2s+1}$, and the global error satisfies $\max_n\|y(t_n) - y_n\| \le C'h^{2s}$ for $h \le h_0$.

*Proof.* Let $u$ be the collocation polynomial of Lemma 3 and $\delta(t) = u'(t) - f(t, u(t))$, its defect; $\delta(t_0 + c_ih) = 0$ for all $i$. For $h$ small, $u$ and its derivatives up to order $s + 1$ are bounded independently of $h$, and so are the derivatives of $\delta$ up to order $2s$ (HNW I, Section II.7; this follows from the stage order $s$ estimate $u(t) - y(t) = O(h^{s+1})$ and the bound on derivatives of the interpolant). Let $\Phi(t, \tau, v)$ be the derivative of the flow $y(t; \tau, v)$ with respect to the initial value $v$ at time $\tau$; it is $C^{2s}$. The nonlinear variation-of-constants formula (Alekseev-Gröbner) gives

$$u(t_0 + h) - y(t_0 + h) = \int_{t_0}^{t_0+h}\Phi\big(t_0 + h, \tau, u(\tau)\big)\delta(\tau)\,d\tau.$$

Apply the Gauss quadrature rule of Lemma 1, which is exact for degree $\le 2s - 1$ and so has error $O(h^{2s+1}\max\|g^{(2s)}\|)$ on $[t_0, t_0 + h]$ for a $C^{2s}$ integrand $g$. Here the quadrature sum $h\sum_ib_ig(t_0 + c_ih)$ is zero because $\delta$ vanishes at the nodes, and $g^{(2s)}$ is bounded, so $\|y_1 - y(t_0 + h)\| = \|u(t_0 + h) - y(t_0 + h)\| \le Ch^{2s+1}$. The method is a one-step method whose increment function is Lipschitz in $y$ for $h \le h_0$ (by Theorem 1 and the implicit function theorem), so the standard argument (local errors propagated by the Lipschitz-stable step and summed over $N \le (T - t_0)/h + 1$ steps; HNW I, Section II.3) gives the global bound $C'h^{2s}$. $\square$

**Theorem 3 (energy identity and its consequences).** For any $f$ and stage solution, with $F_i = f(t_0 + c_ih, Y_i)$,

$$\|y_1\|^2 = \|y_0\|^2 + 2h\sum_ib_i\operatorname{Re}\langle Y_i, F_i\rangle.$$

Consequently:

1. (Quadratic invariants.) If $\langle y, f(t, y)\rangle = 0$ for all $t, y$, where $\langle y, z\rangle = y^TQz$ with $Q$ symmetric positive semidefinite, then $y_1^TQy_1 = y_0^TQy_0$. (Positive semidefiniteness is not needed: the identity is purely algebraic and holds for any symmetric $Q$.)
2. (B-stability.) If $\langle f(t, y) - f(t, z), y - z\rangle \le 0$ for all $t, y, z$, then two numerical solutions satisfy $\|y_1 - z_1\| \le \|y_0 - z_0\|$.
3. (A-stability in the open half-plane.) For $y' = \lambda y$ with $z = h\lambda$, $\operatorname{Re}z < 0$, the stage equations are uniquely solvable and $|R(z)| \le 1$.

*Proof.* Expand $y_1 = y_0 + h\sum_ib_iF_i$:

$$\|y_1\|^2 = \|y_0\|^2 + 2h\sum_ib_i\operatorname{Re}\langle y_0, F_i\rangle + h^2\sum_{i,j}b_ib_j\operatorname{Re}\langle F_i, F_j\rangle.$$

Substitute $y_0 = Y_i - h\sum_ja_{ij}F_j$ in the middle sum:

$$2h\sum_ib_i\operatorname{Re}\langle y_0, F_i\rangle = 2h\sum_ib_i\operatorname{Re}\langle Y_i, F_i\rangle - h^2\sum_{i,j}(b_ia_{ij} + b_ja_{ji})\operatorname{Re}\langle F_j, F_i\rangle,$$

where the double sum was symmetrized. Together, $\|y_1\|^2 = \|y_0\|^2 + 2h\sum_ib_i\operatorname{Re}\langle Y_i, F_i\rangle - h^2\sum_{i,j}m_{ij}\operatorname{Re}\langle F_i, F_j\rangle$, and $M = 0$ by Lemma 2. The identity uses only bilinearity and symmetry of $\langle\cdot,\cdot\rangle$, so it holds for any symmetric $Q$.

(1) Each term $\langle Y_i, F_i\rangle = \langle Y_i, f(t_0 + c_ih, Y_i)\rangle$ vanishes.

(2) The differences $y_0 - z_0$, $Y_i - Z_i$, $F_i - G_i$ satisfy the same linear relations as the method itself, so the identity applies to them, and $b_i > 0$ with $\operatorname{Re}\langle Y_i - Z_i, F_i - G_i\rangle \le 0$ gives the claim.

(3) On $\mathbb{C}$ with $\langle u, v\rangle = \bar uv$: if $(I - zA)Y = 0$ for some $Y \ne 0$, then $Y$ is a stage vector for $y_0 = 0$, and the identity gives $|y_1|^2 = 2\operatorname{Re}(z)\sum_ib_i|Y_i|^2 < 0$, impossible. So $I - zA$ is nonsingular, and the identity with $y_0 = 1$, $y_1 = R(z)$ gives $|R(z)|^2 = 1 + 2\operatorname{Re}(z)\sum_ib_i|Y_i|^2 \le 1$. $\blacksquare$

**Remarks.** (i) On the imaginary axis, $R$ is the $(s, s)$ Padé approximation of $e^z$ (Ehle; HW II, Section IV.3), whose denominator $P(-z)$ has no zeros there, and $|R(iy)| = |P(iy)|/|\overline{P(iy)}| = 1$; this part is cited. The tests compare a Gauss step on random $2 \times 2$ linear systems with the Padé formula. (ii) Symplecticity for Hamiltonian systems follows from $M = 0$ (Sanz-Serna 1988; Hairer, Lubich and Wanner 2006, Section VI.4), applying part 1 to the variational equation, whose symplectic form is a quadratic invariant of the augmented system; cited. (iii) In floating point the stage equations are solved to a relative tolerance $\varepsilon$, which perturbs each step by $O(h\varepsilon)$; invariants are then preserved to $O(N\varepsilon)$ over $N$ steps plus rounding, as seen in the harmonic oscillator test.
