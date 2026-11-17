---
title: The box encoding is a bijection with DECODE as its inverse, it does not change under axis scaling and shifting, and it maps one-coordinate errors to IoU in closed form
proves: [correctness]
status: full
---

Let $\mathcal{B}$ be the set of boxes $(x_1, y_1, x_2, y_2)$ with $x_1 < x_2$ and $y_1 < y_2$. The center form $c(b) = (x, y, w, h)$ with $w = x_2 - x_1$, $h = y_2 - y_1$, $x = x_1 + w/2$, $y = y_1 + h/2$ is a bijection from $\mathcal{B}$ onto $\mathbb{R}^2 \times (0, \infty)^2$, with inverse $(x, y, w, h) \mapsto (x - w/2, y - h/2, x + w/2, y + h/2)$: the inverse gives $x_1 = x - w/2$ and $x_2 - x_1 = w > 0$, and the center form of that box is $(x, y, w, h)$ again.

Fix a reference box $a$ with center form $(x_a, y_a, w_a, h_a)$, $w_a, h_a > 0$.

**Claim 1 (inverse maps).** For every $g \in \mathcal{B}$, DECODE(a, ENCODE(a, g)) = g. For every $t \in \mathbb{R}^4$, DECODE(a, t) is in $\mathcal{B}$ and ENCODE(a, DECODE(a, t)) = t.

*Proof.* Let $(x, y, w, h) = c(g)$ and let $t$ be the output of line L3. Line L5 gives $x_a + t_x w_a = x_a + (x - x_a) = x$, and the same for $y$. Line L6 gives $w_a \exp(\log(w / w_a)) = w$, since $w / w_a > 0$, and the same for $h$. Line L7 is the inverse of the center form, so the result is $g$. For the second part, lines L5 and L6 give $w = w_a e^{t_w} > 0$ and $h = h_a e^{t_h} > 0$, so the box of line L7 is in $\mathcal{B}$ with center form $(x_a + t_x w_a, y_a + t_y h_a, w_a e^{t_w}, h_a e^{t_h})$. Line L3 applied to it gives $((t_x w_a)/w_a, (t_y h_a)/h_a, \log e^{t_w}, \log e^{t_h}) = t$. $\square$

So ENCODE(a, ·) is a bijection from $\mathcal{B}$ onto $\mathbb{R}^4$, and the network output needs no constraint to decode to a valid box.

**Claim 2 (invariance).** Let $m(p) = (s_x p_x + b_x, s_y p_y + b_y)$ with $s_x, s_y > 0$, applied to the two corners of a box. Then ENCODE(m(a), m(g)) = ENCODE(a, g).

*Proof.* Since $s_x > 0$, $m$ keeps $x_1 < x_2$, and the image box has width $s_x w$ and center $s_x x + b_x$; the same holds for $y$ with $s_y$. So $t_x$ becomes $(s_x x + b_x - s_x x_a - b_x)/(s_x w_a) = (x - x_a)/w_a$, and $t_w$ becomes $\log(s_x w / (s_x w_a)) = \log(w / w_a)$. The $y$ terms are the same. $\square$

**Claim 3 (IoU after one error).** Let $g \in \mathcal{B}$ with center form $(x, y, w, h)$, and decode with $g$ itself as the reference.

1. If $t = (e, 0, 0, 0)$ with $|e| \le 1$, the decoded box has IoU $(1 - |e|)/(1 + |e|)$ with $g$.
2. If $t = (0, 0, e, 0)$ for any real $e$, the decoded box has IoU $e^{-|e|}$ with $g$.

*Proof.* (1) The decoded box is $g$ shifted by $d = |e| w \le w$ along $x$. The two boxes share the $y$ range of length $h$, and their $x$ ranges overlap in a length $w - d \ge 0$. So the intersection is $(w - d)h$ and the union is $2wh - (w - d)h = (w + d)h$, and the IoU is $(w - d)/(w + d) = (1 - |e|)/(1 + |e|)$. (2) The decoded box has the same center and height and width $w e^{e}$. The two boxes are nested, so the IoU is the smaller area over the larger one, $\min(1, e^{e}) / \max(1, e^{e}) = e^{-|e|}$. $\square$

**Claim 4 (smooth L1).** The function $f(z) = 0.5 z^2$ for $|z| < 1$ and $|z| - 0.5$ otherwise is continuously differentiable with $f'(z) = z$ for $|z| < 1$ and $f'(z) = \operatorname{sign}(z)$ for $|z| \ge 1$, and $|f'(z)| \le 1$.

*Proof.* On each open piece $f$ is a polynomial with the stated derivative. At $z = 1$ both pieces give $f(1) = 0.5$, and both one-sided derivatives are $1$; at $z = -1$ both give $0.5$ and $-1$. So $f$ is differentiable everywhere, and $f'$ is continuous. The bound follows from the formula. $\square$

**Claim 5 (ridge fit).** For $\lambda > 0$, line L8 has exactly one solution, and it is the unique minimizer of $\|T - \Phi W\|^2 + \lambda \|W\|^2$.

*Proof.* For $v \ne 0$, $v^{\mathsf T}(\Phi^{\mathsf T}\Phi + \lambda I)v = \|\Phi v\|^2 + \lambda \|v\|^2 > 0$, so the matrix is positive definite and invertible. The objective is a strictly convex quadratic with gradient $2(\Phi^{\mathsf T}\Phi + \lambda I)W - 2\Phi^{\mathsf T}T$, which is zero exactly at the $W$ of line L8. $\square$

The code solves the system of line L8 by Gaussian elimination with partial pivoting, which gives the exact solution in exact arithmetic for a nonsingular matrix.
