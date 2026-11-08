---
title: Levin's method integrates the collocated operator exactly, is exact on its image, and for linear phase has error at most the interpolation error and O(omega^(-2))
proves: [correctness]
status: full
---

Let $a \ne b$ be finite, $\omega \ne 0$ real, $g \in C^1[a, b]$ real, $f$ continuous on $[a, b]$ (complex values allowed), and

$$I = \int_a^b f(x)\, e^{i\omega g(x)}\,dx, \qquad \mathcal{L}[p] = p' + i\omega g' p .$$

Let $c = (a + b)/2$, $r = (b - a)/2$, $x(t) = c + r t$, $t_j = \cos(\pi j / n)$ and $x_j = x(t_j)$ for $j = 0, \ldots, n$, so $x_0 = b$ and $x_n = a$. Write $\mathbb{P}_n$ for the polynomials of degree at most $n$ and $T_k$ for the Chebyshev polynomials. Lines refer to the pseudocode LEVIN.

**Lemma 1 (the exact identity, proved).** For every $p \in C^1[a, b]$,

$$\int_a^b \mathcal{L}[p](x)\, e^{i\omega g(x)}\,dx = p(b)\, e^{i\omega g(b)} - p(a)\, e^{i\omega g(a)} .$$

*Proof.* $\frac{d}{dx}\big(p\, e^{i\omega g}\big) = (p' + i\omega g' p)\, e^{i\omega g} = \mathcal{L}[p]\, e^{i\omega g}$; apply the fundamental theorem of calculus. This holds for either orientation of $[a, b]$. $\square$

**Lemma 2 (what the lines compute).** Let $p(x) = \sum_{k=0}^{n} c_k T_k\big((x - c)/r\big)$. Then row $j$ of the matrix of line L4 applied to $(c_k)$ equals $\mathcal{L}[p](x_j)$, line L7 returns $p(b)$ and $p(a)$, and if the matrix $A$ is nonsingular, line L6 finds the unique $p \in \mathbb{P}_n$ with

$$\mathcal{L}[p](x_j) = f(x_j), \qquad j = 0, \ldots, n,$$

and line L8 returns $Q = p(b) e^{i\omega g(b)} - p(a) e^{i\omega g(a)}$.

*Proof.* By the chain rule $\frac{d}{dx} T_k((x - c)/r) = T_k'(t)/r$, so $\sum_k c_k \big(T_k'(t_j)/r + i\omega g'(x_j) T_k(t_j)\big) = p'(x_j) + i\omega g'(x_j) p(x_j)$. The recurrences of the implementation give $T_k$ and $T_k'$ exactly in exact arithmetic ($T_{k+1} = 2tT_k - T_{k-1}$, and its derivative). $T_k(1) = 1$ and $T_k(-1) = (-1)^k$ give line L7. The $T_k$, $k \le n$, form a basis of $\mathbb{P}_n$, so solutions $c$ of $Ac = F$ correspond one to one with such $p$. $\square$

**Theorem 1 (error identity, proved).** If $A$ is nonsingular and $p$ is the collocation polynomial of Lemma 2, then

$$I - Q = \int_a^b \big(f - \mathcal{L}[p]\big)\, e^{i\omega g}\,dx ,$$

where the residual $f - \mathcal{L}[p]$ vanishes at all $n + 1$ nodes, including $a$ and $b$.

*Proof.* Subtract Lemma 1 for this $p$ from the definition of $I$. $\square$

**Theorem 2 (exactness, proved).** If $f = \mathcal{L}[q]$ for some $q \in \mathbb{P}_n$ and $A$ is nonsingular, then $Q = I$.

*Proof.* $q$ satisfies the $n + 1$ collocation conditions, so by uniqueness $p = q$, and the residual in Theorem 1 is identically 0. $\square$

**Lemma 3 (solvability for large frequency, proved).** If $g'(x_j) \ne 0$ for all $j$, then $A$ is nonsingular for all $|\omega|$ large enough.

*Proof.* $A = i\omega\big(GV + \frac{1}{i\omega r} V'\big)$ with $G = \operatorname{diag}(g'(x_j))$, $V = (T_k(t_j))$ and $V' = (T_k'(t_j))$. $V$ is nonsingular, since a polynomial in $\mathbb{P}_n$ vanishing at $n + 1$ distinct points is 0, and $G$ is nonsingular by hypothesis. The determinant of $GV + sV'$ is a polynomial in $s$ that is nonzero at $s = 0$, so it has finitely many roots, and $\det A \ne 0$ once $1/|\omega r|$ is smaller than the smallest of their moduli. $\square$

**Theorem 3 (linear phase, proved).** Let $g(x) = \kappa x + \gamma$ with $\kappa \ne 0$, and let $\Pi_n f \in \mathbb{P}_n$ interpolate $f$ at $x_0, \ldots, x_n$. Then $A$ is nonsingular, $\mathcal{L}[p] = \Pi_n f$, and with $e_n = f - \Pi_n f$,

$$|I - Q| \le |b - a|\, \|e_n\|_\infty, \qquad\text{and if } f \in C^2[a, b], \qquad |I - Q| \le \frac{|e_n'(a)| + |e_n'(b)| + \int_a^b |e_n''|}{(\kappa\omega)^2} .$$

*Proof.* Here $\mathcal{L}[p] = p' + i\kappa\omega p$ maps $\mathbb{P}_n$ into itself. In the basis $1, x, \ldots, x^n$ its matrix is upper triangular with diagonal entries $i\kappa\omega \ne 0$, so $\mathcal{L}$ is a bijection of $\mathbb{P}_n$. If $Ac = 0$, then $\mathcal{L}[p] \in \mathbb{P}_n$ vanishes at $n + 1$ distinct nodes, so $\mathcal{L}[p] = 0$ and $p = 0$, $c = 0$: $A$ is nonsingular. The collocation conditions say that $\mathcal{L}[p] \in \mathbb{P}_n$ agrees with $f$ at the $n + 1$ nodes, so $\mathcal{L}[p] = \Pi_n f$, and Theorem 1 gives $I - Q = \int_a^b e_n\, e^{i\omega g}$. The first bound follows from $|e^{i\omega g}| = 1$. For the second, write $e^{i\omega g} = \frac{1}{i\kappa\omega}\frac{d}{dx} e^{i\omega g}$ and integrate by parts twice. The first boundary term is $[e_n e^{i\omega g}]_a^b / (i\kappa\omega) = 0$, because $a$ and $b$ are nodes, so

$$\int_a^b e_n e^{i\omega g} = -\frac{1}{i\kappa\omega}\int_a^b e_n' e^{i\omega g} = -\frac{1}{(i\kappa\omega)^2}\Big( \big[e_n' e^{i\omega g}\big]_a^b - \int_a^b e_n'' e^{i\omega g} \Big),$$

and the triangle inequality gives the bound. $\square$

So for linear phase the error is at most the smaller of a term that does not grow with $\omega$ and decays with $n$ as fast as Chebyshev interpolation converges (geometrically for $f$ analytic on a neighbourhood of $[a, b]$; Trefethen 2019, Theorem 8.2, cited), and a term $O(\omega^{-2})$ for fixed $n$. The implementation in this case coincides with a Filon-type rule on the Chebyshev-Lobatto nodes whose moments are never formed.

**General phase (cited, asymptotic).** For $g' \ne 0$ on $[a, b]$ and fixed $n$, the error of Levin collocation with both end points among the nodes is $O(\omega^{-2})$ as $\omega \to \infty$ (Levin 1997; Olver 2006, where collocating $f$ and its first $s - 1$ derivatives at the end points gives $O(\omega^{-s-1})$, under a regularity condition on the basis that holds for polynomials when $g' \ne 0$). If $g'$ vanishes in $[a, b]$, the differential equation $\mathcal{L}[p] = f$ has no solution that is free of oscillation near the stationary point, and neither the rate nor Lemma 3 applies; the test file shows an error of the size of $I$ itself in that case.

**Floating point.** Line L6 uses Gaussian elimination with partial pivoting, which is backward stable in practice (Higham 2002, Chapter 9), so the computed $c$ is accurate when $A$ is well conditioned. As $\omega r \to 0$, $A$ tends to $V'/r$, whose column for $T_0$ is zero, so the condition number grows without bound and the coefficients of $p$ grow while $Q$ stays bounded; the subtraction in line L8 then cancels. The measured errors on $\int_0^1 e^x e^{i\omega x}\,dx$ with $n = 10$ are $6.9 \times 10^{-8}$, $4.7 \times 10^{-4}$ and $9.7$ for $\omega = 10^{-2}, 10^{-4}, 10^{-6}$. For $|\omega(b - a)|$ of order 1 or less a nonoscillatory rule should be used instead.

**Termination and cost.** Lines L2 to L5 run $n + 1$ times, with one evaluation of $f$ and one of $g'$ each and $O(n)$ work for the Chebyshev values; line L8 evaluates $g$ twice. Filling $A$ costs $O(n^2)$, line L6 costs $O(n^3)$ arithmetic and $O(n^2)$ memory, and there is no iteration, so the method always terminates; it raises an error only if a pivot is exactly zero. $\blacksquare$
