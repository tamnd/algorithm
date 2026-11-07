---
title: Correctness of the interval Newton method
proves: [correctness, termination, convergence-rate]
status: full
---

Throughout, $f$ is continuously differentiable on $X_0 = [a, b]$. $F$ and $F'$ are inclusion functions: for every interval $X \subseteq X_0$, $\{f(x) : x \in X\} \subseteq F(X)$ and $\{f'(x) : x \in X\} \subseteq F'(X)$. For a point $m$, $F([m, m])$ contains $f(m)$. The width of $X = [\underline{x}, \overline{x}]$ is $w(X) = \overline{x} - \underline{x}$.

## Outward rounding gives inclusion functions

Each interval operation in the reference code first computes its endpoints in round to nearest, which is within half an ulp of the exact value. It then moves the lower endpoint one float down and the upper one float up. So the computed interval contains the exact interval result of the operation applied to the computed operands. By induction over the expression that defines $f$, this is the fundamental theorem of interval arithmetic: the computed $F(X)$ contains the range of $f$ on $X$. For iexp, this requires that math.exp is accurate to within one ulp. That is an assumption about the C library, not a consequence of IEEE 754. The same widening applies to the Newton operator: the computed $N(X)$ contains the exact set $\{m - y/z : y \in F([m, m]),\ z \in F'(X)\}$.

## Lemma 1 (no zero is lost)

If $x^* \in X$ and $f(x^*) = 0$, then $x^*$ lies in the set $N(X)$ computed at L5. If extended division is used, it lies in one of the pieces, and if $0 \in F([m, m])$ and $0 \in F'(X)$, it lies in $X$, which L5 returns unchanged.

*Proof.* By the mean value theorem there is $\xi$ between $m$ and $x^*$, hence in $X$, with $0 = f(m) + f'(\xi)(x^* - m)$. If $f'(\xi) \ne 0$, then $x^* = m - f(m)/f'(\xi)$ with $f(m) \in F([m, m])$ and $f'(\xi) \in F'(X)$, so $x^* \in N(X)$.

When $0 \in F'(X)$ but $0 \notin F([m, m])$, the set of quotients $\{y/z : y \in F([m, m]),\ z \in F'(X) \setminus \{0\}\}$ is contained in the half-lines that the code forms. For $y \ge u > 0$: $z \in (0, d]$ gives $y/z \ge u/d$, and $z \in [c, 0)$ gives $y/z \le u/c$. The case $y \le v < 0$ is symmetric. $N(X)$ is $m$ minus these half-lines, and $f'(\xi) \ne 0$ in this case, because $f'(\xi) = 0$ would force $f(m) = 0 \in F([m, m])$.

If $f'(\xi) = 0$, then $f(m) = 0$, so $0 \in F([m, m])$. If moreover $0 \in F'(X)$, the code keeps $X$ whole. If $0 \notin F'(X)$, then $f'(\xi) = 0$ is impossible. $\square$

Line L4 discards $X$ only when $0 \notin F(X)$, which implies that $f$ has no zero in $X$. Bisection at L10 covers $X$ by two halves. So, by induction over the iterations, the union of the stack and the boxes in found always contains every zero of $f$ in $X_0$. The merging at L12 only replaces boxes by their hulls or by verified sub-boxes, which by Lemma 2 contain the same zero. At the cap, the remaining stack is returned as well. This proves the claim that no zero in $[a, b]$ is missed.

## Lemma 2 (existence and uniqueness)

If $0 \notin F'(X)$ and $N(X) \subseteq X$, then $f$ has exactly one zero in $X$, and it lies in $N(X)$.

*Proof.* $f'$ has constant sign on $X$, so $f$ is strictly monotone on $X$ and has at most one zero there. For existence, assume without loss of generality that $F'(X) = [c, d]$ with $c > 0$; otherwise replace $f$ by $-f$. If $f(m) = 0$ we are done. Suppose $f(m) > 0$. The lower endpoint of $N(X)$ is at most $m - f(m)/c$, and it is at least $\underline{x}$ because $N(X) \subseteq X$. So $m - \underline{x} \ge f(m)/c$. By the mean value theorem, for some $\xi \in X$,
$$f(\underline{x}) = f(m) - f'(\xi)(m - \underline{x}) \le f(m) - c\,\frac{f(m)}{c} = 0.$$
So $f$ changes sign on $[\underline{x}, m]$ and has a zero there by the intermediate value theorem. The case $f(m) < 0$ uses the upper endpoint in the same way. Lemma 1 places the zero in $N(X)$. $\square$

Since the computed $N(X)$ contains the exact operator set, a computed inclusion $N(X) \subseteq X$ implies the exact one, so the conclusion is rigorous in floating point. The inflation in L12 applies Lemma 2 to a slightly larger box $Z$. The verified box is then $N(Z) \cap Z$, which contains the unique zero of $Z$, and hence any zero in the original hull.

## Theorem 1 (quadratic convergence of the width)

Suppose $0 \notin F'(X)$, with $|z| \ge \mu > 0$ for all $z \in F'(X)$, and that $F'$ satisfies $w(F'(Y)) \le L\,w(Y)$ for $Y \subseteq X$. If $X$ contains the zero $x^*$, then
$$w(N(X)) \le \frac{L\,\sup_{x \in X}|f'(x)|}{2\mu^2}\,w(X)^2 + w(F([m, m]))/\mu,$$
and the last term is a rounding term of a few ulps of $f(m)$ divided by $\mu$.

*Proof.* With exact $f(m)$, $N(X) = m - f(m)\cdot[1/d, 1/c]$ for $F'(X) = [c, d]$ with $0 < \mu \le c$. Its width is $|f(m)|(1/c - 1/d) = |f(m)|(d - c)/(cd) \le |f(m)|\,L\,w(X)/\mu^2$. Since $f(x^*) = 0$, $|f(m)| \le \sup|f'|\,|m - x^*| \le \sup|f'|\,w(X)/2$. A wider $F([m, m])$ adds at most $w(F([m, m]))/\mu$. The case $d < 0$ is symmetric. $\square$

So, in exact arithmetic, the widths of a verified box satisfy $w_{k+1} \le C w_k^2$, which is order $q = 2$. In floating point the widths decrease in this way until the rounding term dominates, at a few ulps. Then L7 sees no shrinking and outputs the box. The test checks $w_{k+1} < 0.1\,w_k^2$ on $x^2 - 2$.

## Termination

Each pass of the loop L2 removes one box from the stack, and then does one of four things. It discards the box. It outputs a box. It pushes one box at most half as wide (L9), or one strictly narrower verified box (L7). Or it pushes pieces of which each is either at most half as wide or one of two bisection halves (L10). Bisection is skipped only when the midpoint is not strictly inside the box, and such a box counts as small, so it is output at L8. A box of width below $\delta\max(1, |x|)$ is output too. Verified boxes are pushed only while their width strictly decreases, and a float interval has finitely many floats. So every chain of descendants is finite, and the stack empties. Independently of this argument, L11 stops the loop after $K$ iterations, so the run always terminates. The merge at L12 runs at most 8 Newton tests per merged box.
