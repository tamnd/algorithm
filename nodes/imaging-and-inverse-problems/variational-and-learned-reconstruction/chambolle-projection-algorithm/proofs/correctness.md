---
title: Chambolle's dual iteration decreases the dual objective for a step of at most 1/8 and its primal iterates converge to the total variation denoised image
proves: [correctness, termination]
status: full
---

**Setting.** Images are vectors in $X = \mathbb{R}^{n_1 \times n_2}$ and fields are pairs $p = (p_1, p_2) \in Y = X \times X$, with $p_{ij} \in \mathbb{R}^2$ and Euclidean length $|p_{ij}|$. The gradient $\nabla : X \to Y$ uses forward differences with a zero difference at the last row and column, and $\operatorname{div} = -\nabla^\top$, so $\langle \nabla u, p\rangle_Y = -\langle u, \operatorname{div}p\rangle_X$. Let $\kappa$ be a bound with $\|\operatorname{div} p\|^2 \le \kappa\|p\|^2$ for all $p$. Let $f \in X$, $\lambda > 0$, $g = f/\lambda$,

$$E(u) = \tfrac12\|u - f\|^2 + \lambda\,\mathrm{TV}(u),\qquad \mathrm{TV}(u) = \sum_{ij}|(\nabla u)_{ij}|,$$

$$P = \{p \in Y : |p_{ij}| \le 1 \text{ for all } i, j\},\qquad K = \{\operatorname{div}p : p \in P\},\qquad F(p) = \|\operatorname{div}p - g\|^2.$$

The step map $T$ of lines L3 to L5 is: $z = \nabla(\operatorname{div}p - g)$ and $(Tp)_{ij} = (p_{ij} + \tau z_{ij})/(1 + \tau|z_{ij}|)$. The algorithm sets $p^0 = 0$, $p^{n+1} = Tp^n$ and $u^n = f - \lambda\operatorname{div}p^n$.

**Lemma 0 (the bound $\kappa = 8$ in two dimensions, $\kappa = 4$ in one).** $(\operatorname{div}p)_{ij} = a - b + c - d$, where $a = p_{1,ij}$, $b = p_{1,i-1,j}$, $c = p_{2,ij}$, $d = p_{2,i,j-1}$ and an entry outside the image or on the last row (for $p_1$) or column (for $p_2$) is replaced by 0. By the Cauchy-Schwarz inequality $(a - b + c - d)^2 \le 4(a^2 + b^2 + c^2 + d^2)$. Each entry of $p$ appears in the sums of at most two pixels, so $\|\operatorname{div}p\|^2 \le 8\|p\|^2$. In one dimension there are two terms per pixel, the factor 4 becomes 2, and $\kappa = 4$. $\square$

**Lemma 1 (dual formula).** For all $u$, $\mathrm{TV}(u) = \max_{p \in P}\langle u, \operatorname{div}p\rangle$, so $\lambda\,\mathrm{TV}(u) = \max_{w \in \lambda K}\langle u, w\rangle$.

*Proof.* For $p \in P$, $\langle u, \operatorname{div}p\rangle = -\langle\nabla u, p\rangle \le \sum_{ij}|(\nabla u)_{ij}|\,|p_{ij}| \le \mathrm{TV}(u)$. Equality holds for $p_{ij} = -(\nabla u)_{ij}/|(\nabla u)_{ij}|$ where $(\nabla u)_{ij} \ne 0$ and $p_{ij} = 0$ elsewhere, and this $p$ is in $P$. $\square$

**Lemma 2 (a certificate of optimality).** Let $w \in \lambda K$ and $u = f - w$ with $\langle u, w\rangle = \lambda\,\mathrm{TV}(u)$. Then for every $v \in X$,

$$E(v) \ge E(u) + \tfrac12\|v - u\|^2.$$

So $u$ is the unique minimizer $u^*$ of $E$.

*Proof.* By Lemma 1, $\lambda\,\mathrm{TV}(v) \ge \langle v, w\rangle$ for every $v$, with equality at $v = u$ by assumption. Since $v - f = (v - u) - w$,

$$E(v) \ge \tfrac12\|v - u\|^2 - \langle v - u, w\rangle + \tfrac12\|w\|^2 + \langle v, w\rangle = \tfrac12\|v - u\|^2 + \tfrac12\|w\|^2 + \langle u, w\rangle = \tfrac12\|v - u\|^2 + E(u). \qquad\square$$

The minimizer $u^*$ exists because $E$ is continuous and $E(u) \to \infty$ as $\|u\| \to \infty$, and it is unique because $E$ is strongly convex. Let $w^* = \pi_{\lambda K}(f)$, which exists because $K$ is the linear image of the compact convex set $P$ and so is compact and convex. The projection inequality gives $\langle f - w^*, w - w^*\rangle \le 0$ for all $w \in \lambda K$, so $\langle f - w^*, w^*\rangle = \max_{w \in \lambda K}\langle f - w^*, w\rangle = \lambda\,\mathrm{TV}(f - w^*)$ by Lemma 1. Lemma 2 then gives $u^* = f - \pi_{\lambda K}(f)$. This is the dual problem: $\lambda\operatorname{div}p^* = \pi_{\lambda K}(f)$ exactly when $p^*$ minimizes $F$ over $P$.

**Lemma 3 (feasibility).** If $p \in P$ then $Tp \in P$, and $p' = Tp$ satisfies $p' = p + \tau\eta$ with $\eta = z - |z|\,p'$ at each pixel.

*Proof.* $|p_{ij} + \tau z_{ij}| \le 1 + \tau|z_{ij}|$, so $|p'_{ij}| \le 1$. Multiply the definition of $p'$ by $1 + \tau|z|$: $p' + \tau|z|p' = p + \tau z$. $\square$

By induction from $p^0 = 0$, every iterate is in $P$. This is the loop invariant of lines L2 to L5.

**Lemma 4 (descent).** Let $p \in P$, $p' = Tp$ and $0 < \tau \le 1/\kappa$. Then

$$F(p') \le F(p) - \tau\Big(\sum_{ij}|z_{ij}|^2\big(1 - |p'_{ij}|^2\big) + (1 - \tau\kappa)\|\eta\|^2\Big) \le F(p).$$

*Proof.* Put $r = \operatorname{div}p - g$, so $z = \nabla r$. Then $\operatorname{div}p' - g = r + \tau\operatorname{div}\eta$ and

$$F(p') = \|r\|^2 + 2\tau\langle \operatorname{div}\eta, r\rangle + \tau^2\|\operatorname{div}\eta\|^2 \le F(p) - 2\tau\langle \eta, z\rangle + \tau^2\kappa\|\eta\|^2,$$

using $\langle\operatorname{div}\eta, r\rangle = -\langle\eta, \nabla r\rangle$. At each pixel $2\eta\cdot z - |\eta|^2 = |z|^2 - |z - \eta|^2 = |z|^2 - |z|^2|p'|^2$, because $z - \eta = |z|p'$. So

$$2\langle\eta, z\rangle - \tau\kappa\|\eta\|^2 = \sum_{ij}|z_{ij}|^2\big(1 - |p'_{ij}|^2\big) + (1 - \tau\kappa)\|\eta\|^2,$$

and both terms are at least 0 by Lemma 3 and $\tau\kappa \le 1$. $\square$

**Lemma 5 (no decrease means a fixed point).** Let $p \in P$ and $0 < \tau \le 1/\kappa$. If $F(Tp) = F(p)$ then $Tp = p$.

*Proof.* By Lemma 4 the bracket is 0, so $|z_{ij}|^2(1 - |p'_{ij}|^2) = 0$ at each pixel. If $z_{ij} = 0$ then $p'_{ij} = p_{ij}$ by the formula. Otherwise $|p'_{ij}| = 1$, so $|p_{ij} + \tau z_{ij}| = 1 + \tau|z_{ij}| \ge |p_{ij}| + \tau|z_{ij}|$. The triangle inequality then holds with equality and $|p_{ij}| = 1$. Equality in the triangle inequality with $z_{ij} \ne 0$ and $p_{ij} \ne 0$ means $p_{ij} = c\,z_{ij}$ with $c > 0$, so $p_{ij} = z_{ij}/|z_{ij}|$. Then $p_{ij} + \tau z_{ij} = (1 + \tau|z_{ij}|)\,z_{ij}/|z_{ij}|$ and $p'_{ij} = z_{ij}/|z_{ij}| = p_{ij}$. $\square$

For $\tau < 1/\kappa$ the term $(1 - \tau\kappa)\|\eta\|^2$ alone gives $\eta = 0$. The argument above is what covers the end point $\tau = 1/\kappa$, which is $\tau = 1/8$ in two dimensions.

**Lemma 6 (a fixed point gives the minimizer).** If $p \in P$ and $Tp = p$, then $u = f - \lambda\operatorname{div}p$ is $u^*$.

*Proof.* $Tp = p$ means $p + \tau z = (1 + \tau|z|)p$ at each pixel, so $z = |z|\,p$. Since $u = -\lambda(\operatorname{div}p - g)$, we have $\nabla u = -\lambda z$, so $-(\nabla u)_{ij} = |(\nabla u)_{ij}|\,p_{ij}$. Where $(\nabla u)_{ij} \ne 0$ this forces $|p_{ij}| = 1$. Hence

$$\langle u, \operatorname{div}p\rangle = -\langle\nabla u, p\rangle = \sum_{ij}|(\nabla u)_{ij}|\,|p_{ij}|^2 = \mathrm{TV}(u).$$

With $w = \lambda\operatorname{div}p \in \lambda K$ and $u = f - w$, Lemma 2 applies. $\square$

**Theorem.** Let $0 < \tau \le 1/\kappa$, so $\tau \le 1/8$ for images and $\tau \le 1/4$ for signals. Then $F(p^n)$ is nonincreasing and $u^n = f - \lambda\operatorname{div}p^n \to u^*$, the minimizer of $E$.

*Proof.* By Lemma 4 the sequence $F(p^n)$ is nonincreasing and at least 0, so it has a limit $m$. The iterates lie in the compact set $P$ (Lemma 3). Let $p^{n_k} \to \bar p$ be any convergent subsequence. The map $T$ is continuous, because its denominator is at least 1. So $p^{n_k + 1} = Tp^{n_k} \to T\bar p$, and by continuity of $F$, $F(T\bar p) = \lim F(p^{n_k+1}) = m = F(\bar p)$. Lemma 5 gives $T\bar p = \bar p$, and Lemma 6 gives $f - \lambda\operatorname{div}\bar p = u^*$. So along every convergent subsequence of $(p^n)$, $u^n \to u^*$. If $u^n$ did not converge to $u^*$, there would be $\varepsilon > 0$ and a subsequence with $\|u^n - u^*\| \ge \varepsilon$; by compactness of $P$ it has a further subsequence on which $p^n$ converges, and on it $u^n \to u^*$, a contradiction. $\square$

**Termination with a certificate.** For $p \in P$ let $D(p) = \tfrac12\|f\|^2 - \tfrac12\|f - \lambda\operatorname{div}p\|^2$. With $w = \lambda\operatorname{div}p$, Lemma 1 gives for every $v$

$$E(v) \ge \tfrac12\|v - f\|^2 + \langle v, w\rangle \ge \min_x\Big(\tfrac12\|x - f\|^2 + \langle x, w\rangle\Big) = \langle f, w\rangle - \tfrac12\|w\|^2 = D(p).$$

So $E(u^*) \ge D(p)$, and by Lemma 2 applied at $u^*$,

$$\tfrac12\|u - u^*\|^2 \le E(u) - E(u^*) \le E(u) - D(p)$$

for every image $u$ and every $p \in P$. The gap $E(u^n) - D(p^n)$ is computable, and it tends to 0: $u^n \to u^*$, $E$ is continuous, and $D(p^n) = \tfrac12\|f\|^2 - \tfrac12\|u^n\|^2 \to \tfrac12\|f\|^2 - \tfrac12\|u^*\|^2 = E(u^*)$, the last equality by strong duality ($\langle u^*, w^*\rangle = \lambda\,\mathrm{TV}(u^*)$ with $u^* = f - w^*$). So the loop with the stop rule "gap at most $\varepsilon$" ends after finitely many steps for every $\varepsilon > 0$, and then $\|u - u^*\|^2 \le 2\varepsilon$.
