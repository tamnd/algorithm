---
title: The inverse compositional step solves the linearized problem, stays in the warp group, fixes an exact alignment, and converges superlinearly near a zero-residual solution
proves: [correctness]
status: full
---

Notation as on the page: $\Omega$ is the set of $m$ template pixels, $S(x)$ is the $1 \times n$ steepest descent image of line L3, $H = \sum_x S(x)^{\mathsf T} S(x)$, and $e(x) = I(W(x; p)) - T(x)$. We work with the affine warp, $W(x; p) \leftrightarrow A(p)$, and write $D(p) = A(p) - \mathrm{Id}$, which is the $3 \times 3$ matrix with the entries of $p$ in its first two rows and zeros in its last row. The map $p \mapsto D(p)$ is linear and one to one, so $|p|$ and $\|D(p)\|$ are equivalent norms: there are constants $c_1, c_2 > 0$ with $c_1 |p| \le \|D(p)\| \le c_2 |p|$.

## Claim 1: the step solves the linearized problem

The step asks for the small warp $\Delta p$ of the template that best matches the current warped image:

$$
\psi(\Delta p) = \sum_{x \in \Omega} \big( T(W(x; \Delta p)) - I(W(x; p)) \big)^2 .
$$

Since $W(x; 0) = x$, the chain rule gives $T(W(x; \Delta p)) = T(x) + \nabla T(x)^{\mathsf T} \frac{\partial W}{\partial p}(x; 0)\, \Delta p + o(|\Delta p|) = T(x) + S(x) \Delta p + o(|\Delta p|)$. Dropping the remainder gives

$$
\phi(\Delta p) = \sum_x \big( S(x) \Delta p - e(x) \big)^2 = \Delta p^{\mathsf T} H \Delta p - 2 g^{\mathsf T} \Delta p + \sum_x e(x)^2, \qquad g = \sum_x S(x)^{\mathsf T} e(x),
$$

which is line L7. For any $\Delta p$ and $h$, $\phi(\Delta p + h) - \phi(\Delta p) = 2 h^{\mathsf T} (H \Delta p - g) + h^{\mathsf T} H h$, and $h^{\mathsf T} H h = \sum_x (S(x) h)^2 \ge 0$. So every solution of $H \Delta p = g$ minimizes $\phi$, and at a minimizer the gradient $2(H \Delta p - g)$ vanishes. If the $n$ functions $x \mapsto S_i(x)$ on $\Omega$ are linearly independent, then $S(x) h = 0$ for all $x$ forces $h = 0$, so $h^{\mathsf T} H h > 0$ for $h \ne 0$: $H$ is positive definite, and $\Delta p = H^{-1} g$ of line L8 is the unique minimizer. $H$ depends only on $T$ and $\Omega$, so lines L1 to L4 can compute it once. $\square$

## Claim 2: the update stays in the family

$A(\Delta p)$ has last row $(0, 0, 1)$ and is invertible when $\det \begin{pmatrix} 1 + \Delta p_1 & \Delta p_3 \\ \Delta p_2 & 1 + \Delta p_4 \end{pmatrix} \ne 0$, which holds for $|\Delta p|$ small. The inverse of a matrix with last row $(0, 0, 1)$ has last row $(0, 0, 1)$, and so does a product of two such matrices. So $A(p) A(\Delta p)^{-1} = A(p')$ for exactly one $p'$, read from its first two rows. The action of a product of homogeneous matrices on $(u, v, 1)$ is the composition of the actions, so $W(\cdot; p') = W(\cdot; p) \circ W(\cdot; \Delta p)^{-1}$. $\square$

## Claim 3: an exact alignment is a fixed point

If $I(W(x; p^*)) = T(x)$ for every $x \in \Omega$, then at $p = p^*$ line L6 gives $e = 0$, line L7 gives $g = 0$, and line L8 gives $\Delta p = 0$. Then $A(p^*) A(0)^{-1} = A(p^*)$, so $p^*$ does not change, and line L10 stops. $\square$

## Claim 4: local superlinear convergence

**Hypotheses.** $T$ is continuously differentiable on the plane; $H$ is positive definite; and there is an open set $U \supset \Omega$ with $I(W(y; p^*)) = T(y)$ for all $y \in U$. (On sampled images this holds only approximately; the claim describes the smooth model.)

**Error coordinates.** For $p$ near $p^*$, define $\delta$ by $A(p) = A(p^*) A(\delta)$, that is $A(\delta) = A(p^*)^{-1} A(p)$. This is affine with last row $(0, 0, 1)$, so $\delta$ exists, it depends continuously on $p$, and $\delta = 0$ exactly when $p = p^*$. The warp error is $|\delta|$.

**The residual.** $W(x; p) = W(W(x; \delta); p^*)$. For $\delta$ small, $W(x; \delta) \in U$ for every $x \in \Omega$ ($\Omega$ is finite and $U$ is open), so

$$
e(x) = I(W(W(x; \delta); p^*)) - T(x) = T(W(x; \delta)) - T(x) = S(x) \delta + r(x), \qquad |r(x)| = o(|\delta|),
$$

by the chain rule at $\delta = 0$ (as in Claim 1).

**The step.** By line L8, $\Delta p = H^{-1} \sum_x S(x)^{\mathsf T} (S(x) \delta + r(x)) = \delta + H^{-1} \sum_x S(x)^{\mathsf T} r(x)$. So $\Delta p = \delta + \rho$ with $|\rho| = o(|\delta|)$. In particular $|\Delta p| \le 2 |\delta|$ for $\delta$ small.

**The new error.** The new warp is $A(p') = A(p) A(\Delta p)^{-1} = A(p^*) A(\delta) A(\Delta p)^{-1}$, so the new error $\delta'$ has $A(\delta') = A(\delta) A(\Delta p)^{-1}$. Write $D = D(\delta)$ and $E = D(\Delta p)$. For $\|E\| \le 1/2$ the Neumann series gives $(\mathrm{Id} + E)^{-1} = \mathrm{Id} - E + R_1$ with $\|R_1\| \le \sum_{j \ge 2} \|E\|^j \le 2 \|E\|^2$. Then

$$
A(\delta') = (\mathrm{Id} + D)(\mathrm{Id} - E + R_1) = \mathrm{Id} + (D - E) + R_2, \qquad \|R_2\| \le \|D\| \|E\| + (1 + \|D\|) 2 \|E\|^2 .
$$

So $D(\delta') = D(\delta - \Delta p) + R_2 = -D(\rho) + R_2$. With $\|D\| \le c_2 |\delta|$ and $\|E\| \le 2 c_2 |\delta|$, $\|R_2\| = O(|\delta|^2)$, and $\|D(\rho)\| \le c_2 |\rho| = o(|\delta|)$. By the norm equivalence, $|\delta'| \le c_1^{-1} \|D(\delta')\| = o(|\delta|)$.

**Conclusion.** There is $\varepsilon > 0$ such that $|\delta| \le \varepsilon$ implies $|\delta'| \le \frac{1}{2} |\delta|$, and all the conditions used above hold. By induction, a start with $|\delta_0| \le \varepsilon$ gives $|\delta_j| \le 2^{-j} |\delta_0| \to 0$, so $p_j \to p^*$ by the continuity of $\delta \mapsto A(p^*) A(\delta)$. Since $|\delta_{j+1}| = o(|\delta_j|)$ and $\delta_j \to 0$, the ratio $|\delta_{j+1}| / |\delta_j|$ tends to 0: the convergence is superlinear. $\square$

## What is not claimed

The claims say nothing about starts far from $p^*$, where the iteration can converge to another stationary point or leave the image. The cost $E(p)$ is not proved to decrease at every step: the step minimizes a linearization at the template, not the true cost, and the plain algorithm has no test before it accepts a step. The first-order equivalence of Baker and Matthews with the forwards additive and forwards compositional updates is their result; Claim 4 uses a similar first-order expansion, but it is a separate statement about the inverse compositional iteration alone.
