---
title: The double reflection method gives orthonormal frames that are exact on planes and spheres and symmetric under reversal
proves: [correctness]
status: full
---

We use the notation of the page.
For a nonzero vector $v$, let $H_v a = a - \frac{2}{v \cdot v}(v \cdot a)\,v$.
Line L3 is $r_L = H_{v_1}r_i$, line L4 is $t_L = H_{v_1}t_i$, and line L6 is $r_{i+1} = H_{v_2}r_L$.
If $c_1 = 0$, the implementation sets $v_1 = t_i$.
If $c_2$ is below a small threshold, it stops with an error, so in every completed step $v_1 \ne 0$ and $v_2 \ne 0$.
Write $M_i = H_{v_2}H_{v_1}$ for the map of step $i$.
The tangents $t_i$ are unit vectors and $r_0$ is a unit vector perpendicular to $t_0$.

## Reflections

**Lemma 1.** $H_v$ is linear, orthogonal, symmetric, of determinant $-1$, and $H_v^2 = I$. It fixes every vector perpendicular to $v$, and $H_{\lambda v} = H_v$ for $\lambda \ne 0$.

*Proof.*
$H_v = I - 2\hat v\hat v^{\mathsf T}$ with $\hat v = v/|v|$, which depends only on the line of $v$.
It is symmetric, and $H_v^2 = I - 4\hat v\hat v^{\mathsf T} + 4\hat v(\hat v^{\mathsf T}\hat v)\hat v^{\mathsf T} = I$, so it is orthogonal.
It maps $\hat v$ to $-\hat v$ and fixes the plane $\hat v^\perp$, so its determinant is $-1$. $\square$

**Lemma 2.** If $|a| = |b|$ and $a \ne b$, then $H_{b - a}\,a = b$.

*Proof.*
Let $v = b - a$.
Then $v \cdot v = |a|^2 - 2a\cdot b + |b|^2 = 2(|a|^2 - a \cdot b) = -2\,v \cdot a$.
So $H_v a = a - \frac{2(v \cdot a)}{v \cdot v}v = a + v = b$. $\square$

## Orthonormal frames

**Lemma 3.** $M_i t_i = t_{i+1}$, and $M_i$ is a rotation.

*Proof.*
$t_L = H_{v_1}t_i$ is a unit vector by Lemma 1, and $t_L \ne t_{i+1}$ because $v_2 \ne 0$.
Lemma 2 with $a = t_L$ and $b = t_{i+1}$ gives $H_{v_2}t_L = t_{i+1}$.
$M_i$ is a product of two orthogonal maps of determinant $-1$, so it is orthogonal with determinant $+1$. $\square$

**Lemma 4.** If $x_{i+1} = x_i$, $M_i$ is the smallest rotation that takes $t_i$ to $t_{i+1}$, the rotation about $t_i \times t_{i+1}$ by the angle between the two tangents. In particular $M_i = I$ if $t_{i+1} = t_i$.

*Proof.*
Here $v_1 = t_i$, so $t_L = -t_i$ and $v_2 = t_{i+1} + t_i$, which is not zero.
Both $t_i$ and $t_i + t_{i+1}$ are perpendicular to $k = t_i \times t_{i+1}$, so both reflections fix $k$, and $M_i$ is a rotation about $k$ (or the identity if $k = 0$).
The product of the reflections in two planes that meet at the angle $\beta$ along a line is the rotation about that line by $2\beta$.
The normals $t_i$ and $t_i + t_{i+1}$ make the angle $\theta/2$, where $\theta$ is the angle from $t_i$ to $t_{i+1}$, so the rotation angle is $\theta$, and by Lemma 3 its sense takes $t_i$ to $t_{i+1}$. $\square$

**Theorem 1.** Every frame $(r_i, s_i, t_i)$ of line L8 is a right-handed orthonormal basis.

*Proof.*
By induction on $i$.
For $i = 0$, $r_0 \perp t_0$ are unit vectors and $s_0 = t_0 \times r_0$.
If $r_i \perp t_i$ are unit vectors, then $r_{i+1} = M_ir_i$ and $t_{i+1} = M_it_i$ (Lemma 3) are unit vectors with $r_{i+1}\cdot t_{i+1} = r_i \cdot t_i = 0$, because $M_i$ is orthogonal.
With $s_{i+1} = t_{i+1} \times r_{i+1}$ from line L7, $r_{i+1} \times s_{i+1} = r_{i+1} \times (t_{i+1} \times r_{i+1}) = t_{i+1}(r_{i+1} \cdot r_{i+1}) - r_{i+1}(r_{i+1}\cdot t_{i+1}) = t_{i+1}$, so the basis $(r_{i+1}, s_{i+1}, t_{i+1})$ is orthonormal and right-handed. $\square$

## Exact cases

A unit normal field $r(u) \perp t(u)$ along a regular curve is rotation minimizing if and only if $r'$ is parallel to $t$, which is the equation $r' = -(r \cdot t')\,t$ after the product rule on $r \cdot t = 0$.

**Theorem 2 (plane curves).** If all the points lie in a plane with the unit normal $n$, all the tangents are parallel to that plane, and $r_0 = \cos\alpha\,n + \sin\alpha\,(n \times t_0)$, then $r_i = \cos\alpha\,n + \sin\alpha\,(n \times t_i)$ for every $i$, and this is the rotation minimizing frame at $x_i$.

*Proof.*
The vectors $v_1$ and $v_2$ are parallel to the plane, so $H_{v_1}$ and $H_{v_2}$ fix $n$ by Lemma 1, and so does $M_i$.
A rotation that fixes $n$ commutes with $a \mapsto n \times a$, so $M_i(n \times t_i) = n \times M_it_i = n \times t_{i+1}$ by Lemma 3.
By linearity $r_{i+1} = M_ir_i = \cos\alpha\,n + \sin\alpha\,(n \times t_{i+1})$.
For the continuous field $r(u) = \cos\alpha\,n + \sin\alpha\,(n \times t(u))$, $r' = \sin\alpha\,(n \times t')$, and $t' \perp t$ lies in the plane, so $n \times t'$ is parallel to $t$, and $r$ is rotation minimizing. $\square$

**Theorem 3 (spherical curves).** If all the points lie on a sphere with the center $p$ and the radius $\rho > 0$, each $t_i$ is perpendicular to $x_i - p$, the points are distinct, and $r_0 = (x_0 - p)/\rho$, then $r_i = (x_i - p)/\rho$ for every $i$, and this is the rotation minimizing frame at $x_i$.

*Proof.*
Assume $r_i = (x_i - p)/\rho$.
The vectors $a = x_i - p$ and $b = x_{i+1} - p$ have the length $\rho$ and $b - a = v_1$, so Lemma 2 gives $H_{v_1}a = b$ and $r_L = (x_{i+1} - p)/\rho$.
By Lemma 1, $t_L \cdot r_L = t_i \cdot r_i = 0$, and $t_{i+1}\cdot r_L = 0$ by the assumption on the tangents.
So $v_2 = t_{i+1} - t_L$ is perpendicular to $r_L$, and $H_{v_2}$ fixes $r_L$.
So $r_{i+1} = r_L$.
For the continuous field $r(u) = (x(u) - p)/\rho$ on a curve on the sphere, $r' = x'/\rho$ is parallel to $t$, and $r \perp t$ because $(x - p)\cdot(x - p) = \rho^2$ has the derivative $2(x - p)\cdot x' = 0$. $\square$

**Theorem 4 (straight lines).** If $t_i = t_{i+1}$ and $v_1$ is a positive multiple of $t_i$, then $r_{i+1} = r_i$.

*Proof.*
By Lemma 1, $H_{v_1}t_i = -t_i$, so $v_2 = 2t_{i+1}$ and $H_{v_2} = H_{v_1}$.
So $M_i = H_{v_1}^2 = I$. $\square$

## Symmetry

**Theorem 5.** Run the method on the reversed points $x_N, \dots, x_0$ with the reversed tangents $-t_N, \dots, -t_0$, starting from $r_N$. If the points $x_i$ are distinct, the backward step from $x_{i+1}$ to $x_i$ is $M_i^{-1}$, so the backward run gives $r_N, \dots, r_0$.

*Proof.*
The backward chord is $-v_1$, so its first reflection is $H_{-v_1} = H_{v_1}$ by Lemma 1.
The backward reflected tangent is $H_{v_1}(-t_{i+1}) = -H_{v_1}t_{i+1}$, so the backward second vector is $v_2' = -t_i + H_{v_1}t_{i+1}$.
Since $H_{v_1}^2 = I$, $v_2' = H_{v_1}(t_{i+1} - H_{v_1}t_i) = H_{v_1}v_2$.
For an orthogonal $Q$, $H_{Qv} = QH_vQ^{\mathsf T}$, so $H_{v_2'} = H_{v_1}H_{v_2}H_{v_1}$.
The backward step is $H_{v_2'}H_{v_1} = H_{v_1}H_{v_2}H_{v_1}H_{v_1} = H_{v_1}H_{v_2} = (H_{v_2}H_{v_1})^{-1} = M_i^{-1}$. $\square$

The same argument with the tangents $t_N, \dots, t_0$ not negated gives $v_2' = -H_{v_1}v_2$, which defines the same reflection, so the orientation of the tangents does not matter for the symmetry.

## Accuracy

The order of accuracy is not proved here.
Wang, Jüttler, Zheng and Liu (2008, Theorems 4.4 and 4.5) show that, for a smooth curve with $u_i = u_0 + ih$ and exact tangents, one step has the error $\frac{K}{720}h^5 + O(h^6)$, with $K = 2\kappa_1^2\tau_0 + \kappa_0^2\tau_0^3 + \kappa_1\kappa_0\tau_1 - \kappa_2\kappa_0\tau_0$ in terms of the curvature, the torsion and their derivatives at the start of the step, and that the global error on a fixed interval is $O(h^4)$.
The tests check this rate on a helix against its closed form and on the twisted cubic against a fine Runge-Kutta integration.
