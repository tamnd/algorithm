---
title: The projection of implicit skinning keeps the bind pose and rigid motions, reduces the field error, and keeps converged vertices outside the bones of the toy
proves: [correctness]
status: full
---

We use the notation of the page.
The arithmetic is exact, the weights of each vertex are nonnegative with the sum 1, and each $C_j$ is rigid.
The field in the pose is $f_C(x) = \max_j f_j(C_j^{-1} x)$, and the rest field is $f_I$.
These are properties of the method with given fields; how well an HRBF field fits a mesh is a separate question.

## Bind pose and rigid motions

**Lemma 1.** In the bind pose, with all $C_j = I$, the output is the rest mesh.

*Proof.*
Line L2 gives $v_i$, because the weights sum to 1.
Then $f_I(v_i) = \mathrm{iso}_i$ by line L1, so line L8 stops each projection at once.
In the relaxation of the toy, the target of vertex $i$ is $a + s_i (b - a)$ with the rest neighbors $a, b$ and $s_i = (v_i - a)\cdot(b - a) / \lvert b - a \rvert^2$, and the move is $\rho\, ((\text{target} - v_i)\cdot(b - a))\,(b - a)/\lvert b - a \rvert^2$.
Here $(\text{target} - v_i)\cdot(b - a) = s_i \lvert b - a \rvert^2 - (v_i - a)\cdot(b - a) = 0$, so the vertex does not move, and the new projection stops at once. $\square$

**Lemma 2.** If all $C_j = G$ for one rigid motion $G$, the output is $G v_i$ for every vertex.

*Proof.*
Line L2 gives $G v_i$.
$f_C(G x) = \max_j f_j(G^{-1} G x) = f_I(x)$, so $f_C(G v_i) = \mathrm{iso}_i$ and the projection stops at once.
A rigid motion keeps dot products of differences, so the chord parameter of $G v_i$ between $G a$ and $G b$ is $s_i$, and the relaxation does not move it, as in Lemma 1. $\square$

## The projection step

**Lemma 3.** Let $f$ be twice continuously differentiable near $x$, with $g = \nabla f(x) \ne 0$ and $e = \mathrm{iso} - f(x)$.
After the step $x' = x + \sigma e\, g / \lvert g \rvert^2$, the new error is $\mathrm{iso} - f(x') = (1 - \sigma) e + O(e^2)$.

*Proof.*
By Taylor's theorem, $f(x') = f(x) + g \cdot (x' - x) + O(\lvert x' - x \rvert^2) = f(x) + \sigma e + O(e^2)$, since $\lvert x' - x \rvert = \sigma \lvert e \rvert / \lvert g \rvert$. $\square$

So for $0 < \sigma \le 1$ and a start close enough to the level set, where $\lvert \nabla f \rvert$ stays away from 0, the error shrinks by about the factor $1 - \sigma$ per step and the projection converges linearly; $\sigma = 1$ is Newton's method along the gradient.
The cap on the step length of the toy only shortens steps, and a shorter step along $g$ still lowers the error to first order when $e \ne 0$.

## The toy fields

The toy field of one bone is $\phi(d) = t(d / 2r)$ with $t(u) = 1 - 3u^2 + 2u^3$ on $[0, 1]$ and $0$ beyond, where $d$ is the distance to the segment.
$t'(u) = -6u(1 - u) < 0$ on $(0, 1)$, so $\phi$ is strictly decreasing on $(0, 2r)$, with $\phi(0) = 1$, $\phi(r) = t(1/2) = 1/2$ and $\phi(2r) = 0$.

**Lemma 4.** For one bone, a projection that starts at a point $x$ with $0 < d(x) < 2r$, keeps $d > 0$ at every step and converges, ends at $p + \hat u\, d^*$, where $p$ is the nearest point of the segment to $x$, $\hat u = (x - p)/\lvert x - p \rvert$, and $d^*$ is the unique distance with $\phi(d^*) = \mathrm{iso}$.

*Proof.*
The gradient of the distance is $\hat u$, so $\nabla f = \phi'(d)\, \hat u$ and every step moves the point along the line from $p$ through $x$.
Every point $p + \hat u\, d$ with $d > 0$ has the nearest point $p$ on the segment, because $\hat u$ is normal to the segment at an inner point $p$, and points away from the segment at an end point $p$; so the direction stays $\hat u$, the point stays of the form $p + \hat u\, d$, and the field is $\phi(d)$.
A converged point has $\phi(d) = \mathrm{iso}$, and $\phi$ is strictly decreasing, so $d = d^*$. $\square$

**Lemma 5.** In the toy, a vertex that converges to the value $\mathrm{iso}_i = 0.5$ has the distance at least $r$ from every bone.

*Proof.*
$f_C(v) = 0.5$ is the maximum of the bone fields, so every bone field at $v$ is at most $0.5$.
A bone field at the distance $d < r$ is $\phi(d) > \phi(r) = 0.5$, because $\phi$ is strictly decreasing. $\square$

## The contact rule

Where two bone fields of the toy are equal, the union $\max$ switches from one to the other, and its gradient jumps from $\phi'(d_0)\, \hat u_0$ to $\phi'(d_1)\, \hat u_1$.
On the inside of a bend the two directions $\hat u_0$ and $\hat u_1$ point away from different bones, and the angle between them grows with the bend, so line L9 stops a vertex that crosses that line.
This is a heuristic rule: the angle $\alpha_{\max}$ is a tuning value, and a vertex that stops is not at its iso value.
