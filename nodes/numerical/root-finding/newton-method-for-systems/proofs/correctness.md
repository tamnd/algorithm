---
title: Newton's method for systems ends, and converges quadratically near a root with nonsingular Lipschitz Jacobian
proves: [correctness, termination, local-convergence]
status: full
---

We write $x_k$ for the value of $x$ at the start of pass $k + 1$ of the loop of lines L2 to L11, so $x_0$ is the input, $e_k = x_k - x^*$ and $s_k = x_{k+1} - x_k$. Norms are a fixed vector norm and the induced matrix norm. The arithmetic is exact, except in Claim 1, which holds in any arithmetic.

## Claim 1: termination and the meaning of the flags

Each pass of the loop of line L2 either returns or increases $k$, and $k$ is bounded by $k_{\max}$, so the program ends after at most $k_{\max}$ passes and at most $k_{\max}$ evaluations of $F$ and of $J$. The flag "root" is returned only by line L4, when every component of the computed $F(x)$ is $0$. The flag "converged" is returned only by line L10, so the returned point satisfies $\|s\| \le \delta_a + \delta_r\|x_{\text{new}}\|$. The flag "singular" is returned only when elimination with partial pivoting meets a zero pivot. In exact arithmetic that happens exactly when $J(x)$ is singular: partial pivoting chooses a nonzero pivot in column $c$ whenever one exists, and if none exists, the first $c + 1$ columns of the reduced matrix are linearly dependent, so $J(x)$ is singular.

## Claim 2: two lemmas

**Lemma A (Taylor bound).** If $J$ is Lipschitz with constant $\gamma$ on a convex set $D$ and $x, y \in D$, then
$$\|F(y) - F(x) - J(x)(y - x)\| \le \frac{\gamma}{2}\|y - x\|^2.$$
*Proof.* By the fundamental theorem of calculus along the segment, $F(y) - F(x) - J(x)(y - x) = \int_0^1 (J(x + t(y - x)) - J(x))(y - x)\,dt$. The integrand has norm at most $\gamma t \|y - x\|^2$, and $\int_0^1 t\,dt = 1/2$.

**Lemma B (perturbation of the inverse).** If $A$ is nonsingular, $\|A^{-1}\| \le \beta$ and $\|A^{-1}(B - A)\| \le 1/2$, then $B$ is nonsingular and $\|B^{-1}\| \le 2\beta$.
*Proof.* Write $B = A(I - E)$ with $E = A^{-1}(A - B)$, $\|E\| \le 1/2$. The Neumann series $\sum_j E^j$ converges to $(I - E)^{-1}$ with norm at most $1/(1 - \|E\|) \le 2$. So $B^{-1} = (I - E)^{-1}A^{-1}$ has norm at most $2\beta$.

## Claim 3: local quadratic convergence

**Hypotheses.** $F$ is continuously differentiable on an open convex set containing $B = \{x : \|x - x^*\| \le r\}$, $F(x^*) = 0$, $J(x^*)$ is nonsingular with $\|J(x^*)^{-1}\| \le \beta$, and $\|J(x) - J(y)\| \le \gamma\|x - y\|$ on $B$. Let $\varepsilon = \min(r, 1/(2\beta\gamma))$ and $\|e_0\| \le \varepsilon$.

**Conclusion.** Every $J(x_k)$ is nonsingular, so the program never returns "singular", and $\|e_{k+1}\| \le \beta\gamma\|e_k\|^2 \le \frac12\|e_k\|$ for all $k$.

*Proof by induction on $k$.* Suppose $\|e_k\| \le \varepsilon$, which holds for $k = 0$. Then $x_k \in B$ and
$$\|J(x^*)^{-1}(J(x_k) - J(x^*))\| \le \beta\gamma\|e_k\| \le \tfrac12,$$
so by Lemma B, $J(x_k)$ is nonsingular and $\|J(x_k)^{-1}\| \le 2\beta$. The step is $s_k = -J(x_k)^{-1}F(x_k)$, so
$$e_{k+1} = e_k - J(x_k)^{-1}F(x_k) = J(x_k)^{-1}\bigl(F(x^*) - F(x_k) - J(x_k)(x^* - x_k)\bigr),$$
using $F(x^*) = 0$. Lemma A with $x = x_k$, $y = x^*$ bounds the bracket by $\frac{\gamma}{2}\|e_k\|^2$, so
$$\|e_{k+1}\| \le 2\beta \cdot \frac{\gamma}{2}\|e_k\|^2 = \beta\gamma\|e_k\|^2 \le \beta\gamma\varepsilon\|e_k\| \le \tfrac12\|e_k\|.$$
In particular $\|e_{k+1}\| \le \varepsilon$, which completes the induction. If the program stops at line L4, then $F(x_k) = 0$, and since $J$ is nonsingular on the ball, $x_k = x^*$ by the uniqueness below. Otherwise the iterates converge to $x^*$ with order 2, and $\beta\gamma\|e_k\| \le (\beta\gamma\|e_0\|)^{2^k}$ by induction.

**Uniqueness in the ball.** If $y \in B$ with $\|y - x^*\| \le \varepsilon$ and $F(y) = 0$, then Lemma A with $x = x^*$ gives $\|J(x^*)(y - x^*)\| \le \frac{\gamma}{2}\|y - x^*\|^2$, so $\|y - x^*\| \le \beta\frac{\gamma}{2}\|y - x^*\|^2 \le \frac14\|y - x^*\|$, hence $y = x^*$.

## Claim 4: the step estimates the error

Under the hypotheses of Claim 3, $\|e_{k+1}\| \le \frac12\|e_k\|$, so $\|s_k\| = \|e_{k+1} - e_k\|$ lies between $\frac12\|e_k\|$ and $\frac32\|e_k\|$. Hence $\|e_{k+1}\| \le \beta\gamma\|e_k\|^2 \le 4\beta\gamma\|s_k\|^2$: when line L10 accepts the step $s_k$, the error of the returned point $x_{k+1}$ is at most $4\beta\gamma\|s_k\|^2$. This is a statement in exact arithmetic; in floating point the error also has the limiting part discussed on the main page.

## What is not proved

Nothing is claimed for starts outside the ball of Claim 3; the Kantorovich theorem gives a different, checkable sufficient condition. The constant $1/\sqrt 2$ in the example and the 44 passes on the Freudenstein-Roth problem are observations from runs.
