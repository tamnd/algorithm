---
title: Correctness of homotopy continuation
proves: [correctness, termination, convergence-rate]
status: full
---

This page proves the probability one statement in full for a single polynomial, proves termination of the tracker, and states the local rates. The statement for systems and the guarantee against path jumping are cited.

## Setting

Let $p(x) = x^n + b_1x^{n-1} + \cdots + b_n$ be monic of degree $n \ge 1$, which is what the reference code produces after dividing by $a_0$ and scaling $x$. Let $G(x) = x^n - 1$ and, for $\gamma \in \mathbb{C}$ with $|\gamma| = 1$,
$$H(x, t) = (1 - t)\gamma G(x) + tp(x), \qquad 0 \le t \le 1.$$

## Lemma 1 (finitely many bad directions)

There is a finite set $B$ of angles such that, if $\arg\gamma \notin B$, then for every $t \in [0, 1)$ the polynomial $H(\cdot, t)$ has degree exactly $n$ and $n$ distinct roots.

*Proof.* For $t \in [0, 1)$ put $s = t/(1 - t) \in [0, \infty)$. Then $H(x, t) = (1 - t)(\gamma G(x) + sp(x))$, so $H(\cdot, t)$ and $\gamma G + sp$ have the same roots. Write $w = s/\gamma$, so that $\gamma G + sp = \gamma(G + wp)$.

The leading coefficient of $G + wp$ is $1 + w$, so it vanishes only at $w = -1$, which means $s = -\gamma$. For $s \ge 0$ this requires $\gamma = -1$, which is one bad angle.

For $w \ne -1$, let $\Delta(w)$ be the discriminant of $(G + wp)/(1 + w)$. Its coefficients are rational functions of $w$, so $\Delta$ is a rational function of $w$, and $\Delta(0) \ne 0$ because $G$ has $n$ distinct roots. So $\Delta$ is not identically zero and has finitely many zeros $w_1, \dots, w_M$. A multiple root occurs at some $s \ge 0$ only if $s/\gamma = w_i$ for some $i$. Since $s = 0$ gives $w = 0 \ne w_i$, this means $s > 0$ and $\arg\gamma = -\arg w_i$ modulo $2\pi$. So $B = \{\pi\} \cup \{-\arg w_i\}$ is finite. $\square$

## Theorem 1 (the paths)

If $\arg\gamma \notin B$, there are $n$ continuous functions $x_1(t), \dots, x_n(t)$ on $[0, 1)$, analytic in $t$, with $x_j(0) = e^{2\pi ij/n}$, such that for each $t$ the values $x_1(t), \dots, x_n(t)$ are the $n$ distinct roots of $H(\cdot, t)$. As $t \to 1$, the paths converge, and the multiset of limits is the multiset of roots of $p$. So a root of multiplicity $m$ is the limit of exactly $m$ paths.

*Proof.* At a simple root, $H_x \ne 0$, so by the implicit function theorem each root continues analytically in $t$, and the continuations stay distinct by Lemma 1. Since $[0, 1)$ is connected and the roots never collide or escape to infinity (the degree stays $n$), the $n$ continuations are defined on all of $[0, 1)$. For the limit, the coefficients of $H(\cdot, t)/((1 - t)\gamma + t)$ are continuous in $t$ on $[0, 1]$, and the leading coefficient $(1 - t)\gamma + t$ does not vanish on $[0, 1]$ for $\gamma \ne -1$. The roots of a monic polynomial depend continuously on its coefficients as a multiset, for example by Rouché's theorem on small circles around each root of $p$. So for $t$ near 1, exactly $m$ of the $x_j(t)$ lie in a small disc around a root of multiplicity $m$, and each path has a limit. $\square$

Since $B$ is finite, a $\gamma$ with $\arg\gamma$ uniform on $[0, 2\pi)$ avoids it with probability one. This is the gamma trick.

## Systems (cited)

For a square system $F$ with $\deg F_i = d_i$, $G_i = x_i^{d_i} - 1$ and $\gamma$ outside a finite set of angles, the statement of Sommese and Wampler is as follows. The $D = \prod d_i$ solution paths are smooth and disjoint on $[0, 1)$. Every isolated solution of $F = 0$ of multiplicity $\mu$ is the limit of exactly $\mu$ paths. The remaining paths diverge to infinity or converge to positive-dimensional solution sets. The proof follows the same pattern as Lemma 1: the bad parameter values form a proper algebraic subset of $\mathbb{C}$, which a real ray from 0 misses for all but finitely many directions. The new ingredient is that the start system has no solutions at infinity, which bounds the paths in projective space. We cite it and do not prove it.

## Termination of TRACK

Each pass of the loop L2 either accepts a step, which increases $t$ by $h > 0$, or halves $h$. In the first case the step count increases by one. In the second it also increases, and the return at L7 fires once $h < h_{\min}$. Line L9 returns after $K$ passes, so TRACK makes at most $K$ passes. When $t + h$ would exceed 1, line L3 sets $h = 1 - t$, and the code sets $t$ to exactly 1 in that case, so the loop condition at L2 becomes false. The refinement of the end point is a Newton iteration with an iteration cap, so it terminates as well.

## Local rates

Along a nonsingular path, $x(t)$ is analytic and solves $\dot x = -H_x^{-1}H_t$. The classical Runge-Kutta method has local error $O(h^5)$ on such an equation, which the tests check: the ratio of the errors for $h$ and $h/2$ is about 32. Newton's method on $H(\cdot, t + h)$ converges quadratically from a predicted point close enough to the path, by the standard Newton theorem ([Kantorovich](/kantorovich-theorem/)), with a basin whose radius is proportional to $1/(\|H_x^{-1}\|\,\|H_{xx}\|)$. Near a root of multiplicity $m$, $\|H_x^{-1}\|$ grows without bound as $t \to 1$. The basin shrinks, the step size collapses, and the reference code reports "singular-end". The end point is then accurate to about $u^{1/m}$ in the observed runs.

## What is not proved

The step control of L5 to L7 is a heuristic. A small first correction and fast contraction make path jumping unlikely, but they do not exclude it, and on very ill conditioned problems the observed failures are real. Certified path tracking, which chooses steps by Smale's alpha theory or by interval enclosures, removes this gap and is cited on the page.
