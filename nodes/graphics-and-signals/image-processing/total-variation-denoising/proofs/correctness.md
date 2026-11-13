---
title: Chambolle's iteration converges to the unique ROF minimizer, and the duality gap bounds the error
proves: [correctness]
status: full
---

All sums run over the $WH$ pixels. For images, $\langle u, v \rangle = \sum u\,v$; for fields $p = (p^1, p^2)$, $\langle p, q \rangle = \sum (p^1 q^1 + p^2 q^2)$, and $|p|$ at a pixel is $\sqrt{(p^1)^2 + (p^2)^2}$. The gradient $\nabla$ and the divergence $\operatorname{div}$ are as on the page: forward differences that are 0 on the last column and row, and

$$(\operatorname{div} p)(x, y) = \big(p^1(x, y)[x < W-1] - p^1(x-1, y)[x > 0]\big) + \big(p^2(x, y)[y < H-1] - p^2(x, y-1)[y > 0]\big),$$

where $[\cdot]$ is 1 if the condition holds and 0 otherwise. $K = \{p : |p| \le 1 \text{ at every pixel}\}$. $E(u) = \frac12\lVert u - f\rVert^2 + \lambda \operatorname{TV}(u)$ and $D(p) = \frac12(\lVert f \rVert^2 - \lVert f - \lambda \operatorname{div} p \rVert^2)$.

**Claim 1 (adjoint, norm and mean).** $\langle \operatorname{div} p, u \rangle = -\langle p, \nabla u \rangle$, $\lVert \operatorname{div} p \rVert^2 \le 8 \lVert p \rVert^2$, and $\sum \operatorname{div} p = 0$.

*Proof.* In one row, $\sum_x u(x)\big(p^1(x)[x < W-1] - p^1(x-1)[x > 0]\big) = \sum_{x < W-1} p^1(x)\big(u(x) - u(x+1)\big) = -\sum_x p^1(x)(\nabla u)^1(x)$, by moving the index in the second sum. The columns are the same. For the norm, each value of $\operatorname{div} p$ is a sum of at most four terms, so its square is at most four times the sum of their squares, and each entry $p^i(x, y)$ is a term of at most two values of $\operatorname{div} p$. So $\lVert \operatorname{div} p \rVert^2 \le 4 \cdot 2 \lVert p \rVert^2$. For the mean, take $u = 1$ in the adjoint identity: $\nabla 1 = 0$. $\square$

So $\sum u = \sum f$ for every output $u = f - \lambda \operatorname{div} p$ of line L6.

**Claim 2 (the iteration stays in $K$).** If $p \in K$, then the field $p'$ of line L5 is in $K$.

*Proof.* At each pixel $|p + \tau g| \le |p| + \tau|g| \le 1 + \tau|g|$. $\square$

**Claim 3 (weak duality).** For every image $v$ and every $p \in K$, $D(p) \le E(v)$.

*Proof.* By Claim 1 and the Cauchy-Schwarz inequality at each pixel, $\langle v, \operatorname{div} p \rangle = -\langle p, \nabla v \rangle \le \sum |p|\,|\nabla v| \le \operatorname{TV}(v)$. So

$$E(v) \ge \tfrac12 \lVert v - f \rVert^2 + \lambda \langle v, \operatorname{div} p \rangle \ge \min_w \Big(\tfrac12 \lVert w - f \rVert^2 + \lambda \langle w, \operatorname{div} p \rangle\Big).$$

The minimum of this quadratic is at $w = f - \lambda \operatorname{div} p$, with value $\lambda\langle f, \operatorname{div} p\rangle - \frac12 \lambda^2 \lVert \operatorname{div} p \rVert^2 = D(p)$. $\square$

**Claim 4 (fixed points are optimal).** Let $p \in K$ be a fixed point of line L5 and $u = f - \lambda \operatorname{div} p$. Then for every image $w$,

$$E(w) \ge E(u) + \tfrac12 \lVert w - u \rVert^2,$$

so $u$ is the unique minimizer $u^\ast$ of $E$, and $D(p) = E(u)$.

*Proof.* Line L3 gives $v = \operatorname{div} p - f/\lambda = -u/\lambda$, so line L4 gives $g = -\nabla u / \lambda$. A fixed point satisfies $p(1 + \tau|g|) = p + \tau g$, that is, $g = |g|\,p$ at each pixel. Where $\nabla u \neq 0$ this gives $p = -\nabla u / |\nabla u|$; in both cases $\langle p, \nabla u \rangle$ is $-|\nabla u|$ at each pixel, and summing, $\langle p, \nabla u \rangle = -\operatorname{TV}(u)$.

Now expand the fidelity around $u$, with $u - f = -\lambda \operatorname{div} p$ and Claim 1:

$$\tfrac12\lVert w - f \rVert^2 - \tfrac12 \lVert u - f \rVert^2 = \langle u - f, w - u \rangle + \tfrac12 \lVert w - u \rVert^2 = \lambda \langle p, \nabla w \rangle - \lambda \langle p, \nabla u \rangle + \tfrac12 \lVert w - u \rVert^2.$$

Here $\lambda \langle p, \nabla w \rangle \ge -\lambda \operatorname{TV}(w)$ because $p \in K$, and $-\lambda\langle p, \nabla u \rangle = \lambda \operatorname{TV}(u)$. Adding $\lambda \operatorname{TV}(w) - \lambda \operatorname{TV}(u)$ to both sides gives the inequality. For $w \neq u$ it is strict, so the minimizer is unique. With $w$ ranging over all images, $E(u) = \min E \ge D(p)$ by Claim 3; and $E(u) = \frac12 \lambda^2 \lVert \operatorname{div} p\rVert^2 + \lambda \operatorname{TV}(u) = \frac12 \lambda^2 \lVert \operatorname{div} p\rVert^2 - \lambda\langle p, \nabla u\rangle = \frac12\lambda^2 \lVert \operatorname{div} p\rVert^2 + \lambda\langle \operatorname{div} p, f - \lambda \operatorname{div} p\rangle = D(p)$. $\square$

**Claim 5 (the gap bounds the error).** For $p \in K$ and $u = f - \lambda \operatorname{div} p$, $\frac12 \lVert u - u^\ast \rVert^2 \le E(u) - E(u^\ast) \le E(u) - D(p)$.

*Proof.* $E$ is the sum of $\frac12 \lVert \cdot - f \rVert^2$ and a convex function, so it is 1-strongly convex (see [strong convexity](/strong-convexity/)), which gives $E(u) \ge E(u^\ast) + \frac12 \lVert u - u^\ast \rVert^2$ at the minimizer $u^\ast$. The second inequality is Claim 3 with $v = u^\ast$. $\square$

**Claim 6 (descent).** Let $F(p) = \lVert \operatorname{div} p - f/\lambda \rVert^2$, let $p \in K$, let $p'$ be the next field of line L5, and $\eta = (p' - p)/\tau$. Then

$$F(p') \le F(p) - \tau (1 - 8\tau) \lVert \eta \rVert^2.$$

*Proof.* With $v = \operatorname{div} p - f/\lambda$ and $g = \nabla v$, Claim 1 gives $\langle \operatorname{div} \eta, v \rangle = -\langle \eta, g \rangle$ and $\lVert \operatorname{div} \eta \rVert^2 \le 8 \lVert \eta \rVert^2$, so

$$F(p') = \lVert v + \tau \operatorname{div} \eta \rVert^2 = F(p) - 2\tau \langle \eta, g \rangle + \tau^2 \lVert \operatorname{div} \eta \rVert^2 \le F(p) - \tau\big(2\langle \eta, g\rangle - 8\tau \lVert \eta \rVert^2\big).$$

From line L5, $p'(1 + \tau |g|) = p + \tau g$, so $\eta = g - |g|\,p'$ at each pixel. Then

$$2\, \eta \cdot g - |\eta|^2 = 2|g|^2 - 2|g|\, p' \cdot g - \big(|g|^2 - 2|g|\, p' \cdot g + |g|^2 |p'|^2\big) = |g|^2 (1 - |p'|^2) \ge 0$$

by Claim 2. So $2\langle \eta, g \rangle \ge \lVert \eta \rVert^2$, and the bound follows. $\square$

**Claim 7 (convergence for $\tau < 1/8$).** For $0 < \tau < 1/8$, the outputs $u^n = f - \lambda \operatorname{div} p^n$ converge to $u^\ast$.

*Proof.* By Claim 6, $F(p^n)$ is nonincreasing and bounded below by 0, so it converges, and since $p^{n+1} - p^n = \tau \eta$, $\lVert p^{n+1} - p^n \rVert^2 \le \tau (F(p^n) - F(p^{n+1}))/(1 - 8\tau) \to 0$. The fields lie in the compact set $K$ (Claim 2). Let $\bar p$ be the limit of a subsequence $p^{n_k}$. The map $T$ of lines L3 to L5 is continuous, so $p^{n_k + 1} = T(p^{n_k}) \to T(\bar p)$; since $p^{n_k + 1} - p^{n_k} \to 0$, $T(\bar p) = \bar p$. By Claim 4, $f - \lambda \operatorname{div} \bar p = u^\ast$. So every limit point of the bounded sequence $u^n$ is $u^\ast$, and $u^n \to u^\ast$. $\square$

The fields $p^n$ themselves need not converge, because the dual problem can have many solutions; only $\operatorname{div} p^n$ does. Chambolle's Theorem 3.1 extends the convergence to $\tau = 1/8$, the default of the implementation; the argument above with $\tau = 1/8$ gives only that $F$ does not increase.

**Cost.** Lines L3 to L6 use a constant number of arithmetic operations and at most one square root per pixel, so one step is $\Theta(WH)$, and a gap check, which evaluates $E$ and $D$, is also $\Theta(WH)$.
