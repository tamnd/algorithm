---
title: Angular momentum, linear momentum and affine fields in the APIC transfers
proves: [correctness]
status: full
---

We use the notation of the page, with exact real arithmetic.
Lines L2 and L5 use the same particle positions.
We write the claims for the $u$ faces, with the center $x_f = (x_f, y_f)$ of face $f$; the $v$ faces are the same with the roles of $x$ and $y$ exchanged.
The masses are $m_p > 0$ and $m_f = \sum_p w_{fp} m_p$.

## The bilinear stencil

Fix a particle $p$ whose $u$ weights are not clamped.
Its four faces are $(a_0 + \alpha, b_0 + \beta)$ with $\alpha, \beta \in \{0, 1\}$, at $x_f = x_0 + \alpha\Delta x$ and $y_f = y_0 + \beta\Delta x$, and $x_p = x_0 + s\Delta x$, $y_p = y_0 + t\Delta x$ with $s, t \in [0, 1]$.
The weights are $w_{fp} = X_\alpha Y_\beta$ with $X_0 = 1 - s$, $X_1 = s$, $Y_0 = 1 - t$, $Y_1 = t$.
The gradient of the code is $\nabla w_{fp} = (X'_\alpha Y_\beta, X_\alpha Y'_\beta)$ with $X'_0 = -1/\Delta x$, $X'_1 = 1/\Delta x$, and the same for $Y'$.

**Lemma 1.** For the stencil of $p$:

1. $\sum_f w_{fp} = 1$, $\sum_f w_{fp}(x_f - x_p) = 0$ and $\sum_f w_{fp}(y_f - y_p) = 0$.
2. $D_{xy} = \sum_f w_{fp}(x_f - x_p)(y_f - y_p) = 0$, $D_{xx} = \sum_f w_{fp}(x_f - x_p)^2 = s(1-s)\Delta x^2$ and $D_{yy} = t(1-t)\Delta x^2$.
3. $\sum_f\nabla w_{fp} = 0$, $\sum_f x_f\nabla w_{fp} = (1, 0)$ and $\sum_f y_f\nabla w_{fp} = (0, 1)$.
4. For each face, $w_{fp}\,y_p + \partial_y w_{fp}\,D_{yy} = w_{fp}\,y_f$, and $w_{fp}(y_f - y_p) = D_{yy}\,\partial_y w_{fp}$. The same holds with $x$ in place of $y$.

*Proof.*
Each sum factors into a sum over $\alpha$ and a sum over $\beta$.
In one dimension, $X_0 + X_1 = 1$ and $X_0(-s\Delta x) + X_1(1 - s)\Delta x = 0$, which gives part 1.
For part 2, $D_{xy}$ is the product of the two sums of part 1, so it is 0, and $X_0 s^2\Delta x^2 + X_1(1-s)^2\Delta x^2 = s(1-s)\Delta x^2$.
For part 3, $X'_0 + X'_1 = 0$ and $X'_0 x_0 + X'_1(x_0 + \Delta x) = 1$, while the factor $\sum_\beta Y_\beta = 1$ or $\sum_\beta Y'_\beta = 0$ gives the other parts.
For part 4, take $\beta = 0$: $Y_0 y_p + Y'_0 t(1-t)\Delta x^2 = (1-t)(y_p - t\Delta x) = (1-t)y_0 = Y_0 y_f$.
For $\beta = 1$: $Y_1 y_p + Y'_1 t(1-t)\Delta x^2 = t(y_p + (1-t)\Delta x) = t\,y_f$.
Multiply by $X_\alpha$.
The second identity of part 4 is the first one minus $w_{fp} y_p$. $\square$

For the $u$ faces, no clamping means $y_p \in [\Delta x/2, (n_y - 1/2)\Delta x]$; for the $v$ faces, $x_p \in [\Delta x/2, (n_x - 1/2)\Delta x]$.
Line L6 keeps every particle in this range.
We write $D^u_{p,yy}$ for $D_{yy}$ of the $u$ stencil of $p$ and $D^v_{p,xx}$ for $D_{xx}$ of its $v$ stencil.

## Angular momentum

The particle angular momentum is $L_P = \sum_p m_p(x_p v_p - y_p u_p + c^v_{p,x}D^v_{p,xx} - c^u_{p,y}D^u_{p,yy})$, and the grid angular momentum is $L_G = \sum_{v} m_f x_f v_f - \sum_{u} m_f y_f u_f$.

**Claim 1.** If no weight is clamped, line L2 gives $L_G = L_P$.

*Proof.*
A face with no mass has $w_{fp} = 0$ for every $p$ and adds nothing.
For the others, $m_f u_f = \sum_p w_{fp} m_p (u_p + c^u_p\cdot(x_f - x_p))$, so

$$\sum_u m_f y_f u_f = \sum_p m_p\sum_f w_{fp}\,y_f\left(u_p + c^u_{p,x}(x_f - x_p) + c^u_{p,y}(y_f - y_p)\right).$$

Write $y_f = y_p + (y_f - y_p)$.
By Lemma 1, $\sum_f w_{fp} y_f = y_p$, $\sum_f w_{fp} y_f(x_f - x_p) = D_{xy} + y_p\cdot 0 = 0$ and $\sum_f w_{fp} y_f(y_f - y_p) = D_{yy}$.
So $\sum_u m_f y_f u_f = \sum_p m_p(y_p u_p + c^u_{p,y}D^u_{p,yy})$.
In the same way, $\sum_v m_f x_f v_f = \sum_p m_p(x_p v_p + c^v_{p,x}D^v_{p,xx})$.
The difference is $L_P$. $\square$

**Claim 2.** If no weight is clamped, line L5 gives $L_P = L_G$, with the face masses of line L2.

*Proof.*
After line L5, $u_p = \sum_f w_{fp}u_f$ and $c^u_{p,y} = \sum_f\partial_y w_{fp}\,u_f$.
So by Lemma 1, part 4,

$$\sum_p m_p(y_p u_p + c^u_{p,y}D^u_{p,yy}) = \sum_p m_p\sum_f u_f(w_{fp}y_p + \partial_y w_{fp}D^u_{p,yy}) = \sum_p m_p\sum_f w_{fp}\,y_f u_f = \sum_u m_f y_f u_f.$$

The $v$ part is the same with $x$, and the difference gives $L_P = L_G$. $\square$

## Linear momentum

**Claim 3.** Line L2 gives $\sum_f m_f u_f = \sum_p m_p u_p$, and line L5 gives $\sum_p m_p u_p = \sum_f m_f u_f$.

*Proof.*
$\sum_f m_f u_f = \sum_p m_p(u_p + c^u_p\cdot\sum_f w_{fp}(x_f - x_p)) = \sum_p m_p u_p$ by Lemma 1, part 1.
Line L5 is the PIC transfer for $u_p$, and $\sum_p m_p\sum_f w_{fp}u_f = \sum_f m_f u_f$. $\square$

## Affine fields

**Claim 4.** Let $u(x) = a + b\,x + c\,y$, and let every particle carry $u_p = u(x_p)$ and $c^u_p = (b, c)$. If no weight is clamped, then after lines L2 and L5, $u_p = u(x_p)$ and $c^u_p = (b, c)$ for every particle.

*Proof.*
For every particle, $u_p + c^u_p\cdot(x_f - x_p) = u(x_f)$, so each face with mass gets the weighted mean of equal values, $u_f = u(x_f)$.
A face in the stencil of a particle has $w_{fp} > 0$ and so has mass, or it has $w_{fp} = 0$ and adds nothing to line L5.
Then $\sum_f w_{fp}u(x_f) = a + b x_p + c y_p$ by Lemma 1, part 1.
And $\sum_f\nabla w_{fp}\,u(x_f) = a\cdot 0 + b(1, 0) + c(0, 1) = (b, c)$ by Lemma 1, part 3. $\square$

With the gradients set to 0, the same field is the PIC case, and the energy loss of the PIC proof applies.

## The gradient as B D^-1

**Claim 5.** Let $B = \sum_f w_{fp}u_f(x_f - x_p)$. Then $B_x = D_{xx}\,c^u_{p,x}$ and $B_y = D_{yy}\,c^u_{p,y}$, so $c^u_p = B D^{-1}$ when $D$ is invertible.

*Proof.*
By Lemma 1, part 4, $w_{fp}(y_f - y_p) = D_{yy}\,\partial_y w_{fp}$ for each face, and the same with $x$.
Multiply by $u_f$ and sum over the faces.
$D$ is diagonal by Lemma 1, part 2. $\blacksquare$
