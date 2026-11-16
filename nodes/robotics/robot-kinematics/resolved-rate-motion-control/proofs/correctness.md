---
title: RESOLVED-RATE gives least norm joint rates and bounded tracking error
proves: [correctness]
status: full
---

We use the notation of the page.
The task map is $f : \mathbb{R}^n \to \mathbb{R}^m$ with $m \le n$, of class $C^2$, with the Jacobian $J(q) = Df(q)$.
All vector norms are Euclidean, and the norm of a matrix is the induced norm, its largest singular value.
The proof is in exact arithmetic, in the real RAM.

Lines L4 to L8 of RESOLVED-RATE compute, for $j = 0, \dots, N - 1$ and $t_j = j\Delta t$,

$$e_j = x_d(t_j) - f(q_j), \qquad v_j = \dot x_d(t_j) + Ke_j, \qquad q_{j+1} = q_j + \Delta t\, J(q_j)^{+} v_j.$$

## The step

**Lemma 1.** Let $J$ be an $m \times n$ matrix of rank $m$, and let $J^{+} = J^{\mathsf T}(JJ^{\mathsf T})^{-1}$.
For every $v \in \mathbb{R}^m$:

1. $J(J^{+}v) = v$;
2. every $u$ with $Ju = v$ satisfies $|u|^2 = |J^{+}v|^2 + |u - J^{+}v|^2$, so $J^{+}v$ is the unique solution of least norm;
3. $|J^{+}v| \le |v| / \sigma_m$, where $\sigma_m > 0$ is the smallest singular value of $J$.

*Proof.*
Since $J$ has rank $m$, the $m \times m$ matrix $JJ^{\mathsf T}$ is positive definite, hence invertible, and $JJ^{+}v = JJ^{\mathsf T}(JJ^{\mathsf T})^{-1}v = v$.
If $Ju = v$, then $J(u - J^{+}v) = 0$.
The vector $J^{+}v = J^{\mathsf T}y$ with $y = (JJ^{\mathsf T})^{-1}v$ lies in $\operatorname{range}(J^{\mathsf T})$, and $(J^{\mathsf T}y)^{\mathsf T}(u - J^{+}v) = y^{\mathsf T}J(u - J^{+}v) = 0$.
So $u = J^{+}v + (u - J^{+}v)$ is a sum of two orthogonal vectors, which gives item 2; equality $|u| = |J^{+}v|$ holds only for $u = J^{+}v$.
For item 3, write $J = U\Sigma V^{\mathsf T}$ with orthogonal $U$ and $V$ and $\Sigma = (\operatorname{diag}(\sigma_1, \dots, \sigma_m)\ 0)$.
Then $JJ^{\mathsf T} = U\operatorname{diag}(\sigma_i^2)U^{\mathsf T}$, and $J^{+} = V\Sigma^{\mathsf T}\operatorname{diag}(\sigma_i^{-2})U^{\mathsf T}$, whose singular values are $1/\sigma_i$.
The largest is $1/\sigma_m$.
$\square$

So line L7 computes the least norm joint velocity that produces the task velocity $v$ exactly, as the page claims.

## Continuous time

**Proposition 2.** Let $q(t)$ be a $C^1$ solution of $\dot q = J(q)^{+}\big(\dot x_d(t) + Ke(t)\big)$ on $[0, T]$, with $e = x_d - f(q)$ and $J(q(t))$ of rank $m$ for all $t$.
Then $\dot e = -Ke$, so $e(t) = e^{-Kt}e(0)$.
If $K$ is symmetric and positive semidefinite with smallest eigenvalue $\lambda \ge 0$, then $|e(t)| \le e^{-\lambda t}|e(0)|$.

*Proof.*
By the chain rule and Lemma 1, $\dot e = \dot x_d - J(q)\dot q = \dot x_d - (\dot x_d + Ke) = -Ke$.
This linear equation with constant coefficients has the unique solution $e^{-Kt}e(0)$.
For the bound, $\frac{d}{dt}|e|^2 = -2e^{\mathsf T}Ke \le -2\lambda|e|^2$, so $|e(t)|^2 e^{2\lambda t}$ does not increase.
$\square$

For $K = 0$ the error stays equal to $e(0)$: the open-loop law tracks the path exactly from an exact start, and keeps any start error.

## One discrete step

Make these assumptions.

- (A1) $x_d$ is $C^2$ on $[0, T]$, with $|\dot x_d(t)| \le V$ and $|\ddot x_d(t)| \le A$.
- (A2) $\Omega \subset \mathbb{R}^n$ is a set on which $\sigma_m(J(q)) \ge \sigma_0 > 0$, and $H \ge 0$ is a constant such that $|f(q + \delta) - f(q) - J(q)\delta| \le \tfrac{H}{2}|\delta|^2$ whenever the segment from $q$ to $q + \delta$ lies in $\Omega$. (Such an $H$ exists when $\Omega$ is compact and convex, by Taylor's theorem with the bound of the second derivative of $f$.)
- (A3) The iterates $q_0, \dots, q_N$ and the segments between consecutive iterates lie in $\Omega$, and $N\Delta t \le T$.

**Lemma 3.** Under (A1) to (A3), for every $j < N$,

$$e_{j+1} = (I - \Delta t K)\,e_j + r_j, \qquad |r_j| \le \tfrac12\big(A\Delta t^2 + H|\delta_j|^2\big), \qquad |\delta_j| \le \frac{\Delta t\,|v_j|}{\sigma_0},$$

where $\delta_j = q_{j+1} - q_j = \Delta t\,J(q_j)^{+}v_j$.

*Proof.*
By Taylor's theorem with remainder, $x_d(t_{j+1}) = x_d(t_j) + \Delta t\,\dot x_d(t_j) + r'_j$ with $|r'_j| \le A\Delta t^2/2$.
By (A2) and (A3), $f(q_{j+1}) = f(q_j) + J(q_j)\delta_j + r''_j$ with $|r''_j| \le H|\delta_j|^2/2$.
By Lemma 1, $J(q_j)\delta_j = \Delta t\,v_j = \Delta t\,\dot x_d(t_j) + \Delta t\,Ke_j$.
Subtracting,

$$e_{j+1} = e_j + \Delta t\,\dot x_d(t_j) - \Delta t\,\dot x_d(t_j) - \Delta t\,Ke_j + r'_j - r''_j = (I - \Delta tK)e_j + r_j,$$

with $r_j = r'_j - r''_j$.
The bound on $|\delta_j|$ is item 3 of Lemma 1 with $\sigma_m(J(q_j)) \ge \sigma_0$.
$\square$

## The open-loop bound

**Theorem 4.** Under (A1) to (A3) with $K = 0$, let $c_0 = \tfrac12(A + H V^2/\sigma_0^2)$.
Then $|e_j| \le |e_0| + c_0\, t_j\, \Delta t$ for $j = 0, \dots, N$.

*Proof.*
With $K = 0$, $v_j = \dot x_d(t_j)$, so $|\delta_j| \le \Delta t V/\sigma_0$ and $|r_j| \le c_0\Delta t^2$ by Lemma 3.
Then $|e_{j+1}| \le |e_j| + c_0\Delta t^2$, and by induction $|e_j| \le |e_0| + j\,c_0\Delta t^2 = |e_0| + c_0 t_j \Delta t$.
$\square$

So, from an exact start, the open-loop error at a fixed time $t$ is $O(\Delta t)$: halving the step halves the bound, as in the example on the page.

## The closed-loop bound

**Theorem 5.** Under (A1) to (A3) with $K = \kappa I$ and $\kappa > 0$, fix a number $E > |e_0|$, and let

$$\rho = \frac{V + \kappa E}{\sigma_0}, \qquad c = \tfrac12\big(A + H\rho^2\big).$$

If $0 < \kappa\Delta t \le 1$ and $c\,\Delta t / \kappa \le E - |e_0|$, then for $j = 0, \dots, N$,

$$|e_j| \le B_j := (1 - \kappa\Delta t)^j\,|e_0| + \frac{c\,\Delta t}{\kappa}\Big(1 - (1 - \kappa\Delta t)^j\Big) \le E.$$

In particular $|e_N| \le (1 - \kappa\Delta t)^N|e_0| + c\,\Delta t/\kappa$.

*Proof.*
The constants $\rho$ and $c$ depend on $E$, $V$, $A$, $H$, $\sigma_0$ and $\kappa$, but not on $\Delta t$ or on the iterates, so the conditions on $\Delta t$ can be met by taking $\Delta t$ small; there is no circular argument.

First, $B_j \le E$ for every $j$.
With $a = (1 - \kappa\Delta t)^j \in [0, 1]$, $B_j = a|e_0| + (1 - a)\,c\Delta t/\kappa$ is a convex combination of $|e_0| < E$ and $c\Delta t/\kappa \le E - |e_0| \le E$.

Now induct on $j$.
For $j = 0$, $B_0 = |e_0|$.
Suppose $|e_j| \le B_j$.
Then $|e_j| \le E$, so $|v_j| \le V + \kappa E$, $|\delta_j| \le \rho\Delta t$ and $|r_j| \le c\Delta t^2$ by Lemma 3.
Since $0 < \kappa\Delta t \le 1$, the matrix $I - \Delta tK = (1 - \kappa\Delta t)I$ has norm $1 - \kappa\Delta t$, so

$$|e_{j+1}| \le (1 - \kappa\Delta t)B_j + c\Delta t^2 = (1 - \kappa\Delta t)^{j+1}|e_0| + \frac{c\Delta t}{\kappa}\Big((1 - \kappa\Delta t) - (1 - \kappa\Delta t)^{j+1} + \kappa\Delta t\Big) = B_{j+1}.$$

$\square$

**Remark.** For a symmetric positive definite $K$ with eigenvalues in $[\lambda, \Lambda]$ and $\Lambda\Delta t \le 1$, the same proof works with $\|I - \Delta tK\| = 1 - \lambda\Delta t$, with $\kappa$ replaced by $\lambda$ in the rate and in the final term, and by $\Lambda$ in $\rho$.

So the closed-loop error forgets the start error at the geometric rate $1 - \kappa\Delta t$ and then stays within $c\Delta t/\kappa$ of the path for all $j \le N$, a bound that does not grow with the length of the run.
Both theorems need (A3): the iterates must stay where $J$ is well conditioned.
Near a kinematic singularity $\sigma_0 \to 0$, and $\rho$, $c$ and the bounds blow up, which is the failure described on the page.
