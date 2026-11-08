---
tag: S069GX
kind: theorem
slug: butcher-order-conditions
name: Butcher order conditions
aliases:
- order conditions for Runge-Kutta methods
- Butcher's order theorem
- rooted tree order conditions
area: numerical/differential-equations
level: advanced
summary: A Runge-Kutta method with c = A1 has order p if and only if b^T Φ(t) = 1/γ(t) for every rooted tree t with at most p vertices.
prereqs: [butcher-tableau, order-of-accuracy]
see_also: [runge-kutta-methods, classical-runge-kutta-4, local-truncation-error, gauss-legendre-runge-kutta, embedded-runge-kutta-pairs, cash-karp-method, dormand-prince-method, collocation-method]
sources:
  - paper: doi:10.1017/S1446788700027932
    title: "J. C. Butcher, Coefficients for the study of Runge-Kutta integration processes, Journal of the Australian Mathematical Society 3 (1963) 185-201"
    locator: the order conditions indexed by rooted trees, with the functions γ and the elementary weights
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.2 (rooted trees, elementary differentials, Taylor expansion of exact and numerical solution, the order conditions and their independence), Section II.5 (the order barriers for explicit methods) and Section II.7 (simplifying assumptions)
  - book: isbn:9783540306634
    title: Ernst Hairer, Christian Lubich and Gerhard Wanner, Geometric Numerical Integration, second edition, Springer, 2006
    locator: Section III.1 (B-series, the composition lemma for h f(B(a, y)), and the order conditions of Runge-Kutta methods)
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 3 (Runge-Kutta methods; trees, elementary differentials, order conditions and order barriers)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 3 (Runge-Kutta methods, the order conditions for explicit methods of low order)
---

## Statement

**Setting.** An $s$-stage [Runge-Kutta method](/runge-kutta-methods/) with [Butcher tableau](/butcher-tableau/) $(A, b, c)$ is applied to the autonomous system $y' = f(y)$, $y \in \mathbb{R}^d$, $y(t_0) = y_0$. One step of size $h$ is
$$Y_i = y_0 + h\sum_{j=1}^sa_{ij}f(Y_j), \quad i = 1, \dots, s, \qquad y_1 = y_0 + h\sum_{i=1}^sb_if(Y_i).$$
For an implicit method, $Y_i$ is the solution that tends to $y_0$ as $h \to 0$. The method has **order $p$** if, for every $f$ that is $C^{p+1}$ near $y_0$, the local error satisfies $y(t_0 + h) - y_1 = O(h^{p+1})$ as $h \to 0$.

**Trees.** A rooted tree is either the single vertex $\bullet$, or $t = [t_1, \dots, t_m]$, a new root joined to the roots of the trees $t_1, \dots, t_m$ (an unordered list, repeats allowed). The set of all rooted trees is $T$. For $t \in T$:

- the order $|t|$ is the number of vertices: $|\bullet| = 1$ and $|t| = 1 + \sum_l|t_l|$;
- the density is $\gamma(\bullet) = 1$ and $\gamma(t) = |t|\prod_l\gamma(t_l)$;
- the symmetry is $\sigma(\bullet) = 1$ and $\sigma(t) = \prod_l\sigma(t_l)\cdot\prod_k\mu_k!$, where $\mu_k$ are the multiplicities of the distinct trees among $t_1, \dots, t_m$;
- the elementary differential is $F(\bullet)(y) = f(y)$ and $F(t)(y) = f^{(m)}(y)[F(t_1)(y), \dots, F(t_m)(y)]$;
- the elementary weights are $\Phi_i(\bullet) = 1$ and $\Phi_i(t) = \prod_{l=1}^m\big(\sum_ja_{ij}\Phi_j(t_l)\big)$ for $i = 1, \dots, s$.

**Theorem (Butcher 1963).** The method has order $p$ if and only if
$$\sum_{i=1}^sb_i\Phi_i(t) = \frac1{\gamma(t)} \quad\text{for every } t \in T \text{ with } |t| \le p. \tag{1}$$
Moreover, if $f$ is $C^{p+1}$, then
$$y(t_0 + h) - y_1 = \sum_{|t| \le p}\frac{h^{|t|}}{\sigma(t)}\Big(\frac1{\gamma(t)} - b^T\Phi(t)\Big)F(t)(y_0) + O(h^{p+1}). \tag{2}$$

**Non-autonomous problems.** If $c_i = \sum_ja_{ij}$ for all $i$, the same conditions (1) are necessary and sufficient for order $p$ on $y' = f(t, y)$ with stages at $t_0 + c_ih$.

With $c = A\mathbf 1$ the conditions up to order 4 read:

| $\lvert t\rvert$ | tree | condition (1) | $F(t)$ | $\sigma(t)$ |
|---|---|---|---|---|
| 1 | $\bullet$ | $\sum_ib_i = 1$ | $f$ | 1 |
| 2 | $[\bullet]$ | $\sum_ib_ic_i = \tfrac12$ | $f'f$ | 1 |
| 3 | $[\bullet, \bullet]$ | $\sum_ib_ic_i^2 = \tfrac13$ | $f''(f, f)$ | 2 |
| 3 | $[[\bullet]]$ | $\sum_{ij}b_ia_{ij}c_j = \tfrac16$ | $f'f'f$ | 1 |
| 4 | $[\bullet, \bullet, \bullet]$ | $\sum_ib_ic_i^3 = \tfrac14$ | $f'''(f, f, f)$ | 6 |
| 4 | $[\bullet, [\bullet]]$ | $\sum_{ij}b_ic_ia_{ij}c_j = \tfrac18$ | $f''(f, f'f)$ | 1 |
| 4 | $[[\bullet, \bullet]]$ | $\sum_{ij}b_ia_{ij}c_j^2 = \tfrac1{12}$ | $f'f''(f, f)$ | 2 |
| 4 | $[[[\bullet]]]$ | $\sum_{ijk}b_ia_{ij}a_{jk}c_k = \tfrac1{24}$ | $f'f'f'f$ | 1 |

## In plain words

Expand the exact solution and one step of the method in powers of the step size $h$. Each power of $h$ is a sum of terms built from $f$ and its derivatives, such as $f'f$ or $f''(f, f)$. Each such term has the shape of a tree: a derivative of $f$ is a vertex, and the functions it acts on are its children. The exact solution has a fixed coefficient $1/\gamma(t)$ for each tree. The method has a coefficient that is a polynomial in its tableau entries. The method is accurate to order $p$ exactly when the two coefficients agree for every tree with at most $p$ vertices. The terms for different trees cannot cancel each other in general, so no condition can be skipped.

## Proof

All expansions below are Taylor expansions in $h$ up to $h^p$, with a remainder $O(h^{p+1})$. They are valid because $f$ is $C^{p+1}$, so $y(t_0 + h)$ and the stages are $C^{p+1}$ functions of $h$ near $h = 0$ (for implicit stages by the implicit function theorem). For a map $a: T \to \mathbb{R}$ write
$$B_h(a) = \sum_{|t| \le p}\frac{h^{|t|}}{\sigma(t)}a(t)F(t)(y_0),$$
and define $a': T \to \mathbb{R}$ by $a'(\bullet) = 1$ and $a'([t_1, \dots, t_m]) = \prod_la(t_l)$.

**Lemma 1 (composition).** If $Y(h) = y_0 + B_h(a) + O(h^{p+1})$, then $hf(Y(h)) = B_h(a') + O(h^{p+1})$.

*Proof.* Write $\delta = Y - y_0$. Taylor's theorem gives $hf(y_0 + \delta) = h\sum_{m \le p}\frac1{m!}f^{(m)}(y_0)[\delta, \dots, \delta] + O(h^{p+1})$, because $\delta = O(h)$. Insert $\delta = B_h(a)$ and expand by multilinearity. The term for an ordered list $(t_1, \dots, t_m)$ is
$$\frac{h^{1 + \sum|t_l|}}{m!}\prod_l\frac{a(t_l)}{\sigma(t_l)}\,f^{(m)}(y_0)[F(t_1), \dots, F(t_m)].$$
The value of $f^{(m)}$ is symmetric in its arguments, so all orderings of the same multiset give the same term. That term is $h^{|u|}\,\prod_la(t_l)\,F(u)(y_0)$ times a factor, with $u = [t_1, \dots, t_m]$. A multiset with multiplicities $\mu_k$ has $m!/\prod_k\mu_k!$ orderings. So the total coefficient is $\frac1{m!}\cdot\frac{m!}{\prod_k\mu_k!}\cdot\frac1{\prod_l\sigma(t_l)} = \frac1{\sigma(u)}$. The constant term $hf(y_0)$ is the tree $\bullet$ with $a'(\bullet) = 1$. Terms with $|u| > p$ go into the remainder. $\square$

**Lemma 2 (uniqueness of expansions).** Let $g$ be $C^{p+1}$, and let $Z(h)$ and $W(h)$ be $C^{p+1}$ functions with $Z(0) = W(0) = y_0$.

- (a) If $hZ'(h) = hg(Z(h)) + O(h^{p+1})$ and the same holds for $W$, then $Z - W = O(h^{p+1})$.
- (b) If $Z = y_0 + hMg(Z) + O(h^{p+1})$ and $W = y_0 + hMg(W) + O(h^{p+1})$ for a fixed linear map $M$ (acting on stacked stage vectors), then $Z - W = O(h^{p+1})$.

*Proof.* (a) Let $D = Z - W = \sum_{q=1}^pd_qh^q + O(h^{p+1})$. The coefficient of $h^q$ in $h(g(Z) - g(W))$ depends only on $d_1, \dots, d_{q-1}$ and is zero if they are all zero, because of the factor $h$. The equation gives $qd_q$ equal to that coefficient. By induction, $d_q = 0$ for all $q \le p$. (b) $g$ is Lipschitz near $y_0$ with some constant $L$, so $\|Z - W\| \le h\|M\|L\|Z - W\| + O(h^{p+1})$. For $h\|M\|L \le \tfrac12$ this gives $\|Z - W\| = O(h^{p+1})$. $\square$

**Step 1 (exact solution).** Let $e(t) = 1/\gamma(t)$ and $E(h) = y_0 + B_h(e)$. From $\gamma([t_1, \dots, t_m]) = |t|\prod\gamma(t_l)$ we get $e'(t) = \prod_le(t_l) = |t|e(t)$. By Lemma 1, $hf(E) = B_h(e') + O(h^{p+1}) = \sum\frac{|t|h^{|t|}}{\sigma(t)}e(t)F(t)(y_0) + O(h^{p+1}) = hE'(h) + O(h^{p+1})$. The exact solution satisfies $hy'(t_0 + h) = hf(y(t_0 + h))$. By Lemma 2(a), $y(t_0 + h) = y_0 + B_h(e) + O(h^{p+1})$.

**Step 2 (stages).** Define $\Psi_i: T \to \mathbb{R}$ by $\Psi_i(t) = \sum_ja_{ij}\Phi_j(t)$. By the definition of the elementary weights, $\Phi_j = \Psi_j'$. Let $\tilde Y_i = y_0 + B_h(\Psi_i)$. By Lemma 1, $\tilde Y_i = y_0 + h\sum_ja_{ij}f(\tilde Y_j) + O(h^{p+1})$, so the $\tilde Y_i$ satisfy the stage equations up to $O(h^{p+1})$. By Lemma 2(b), $Y_i = \tilde Y_i + O(h^{p+1})$, and so $hf(Y_i) = B_h(\Phi_i) + O(h^{p+1})$. Hence $y_1 = y_0 + B_h(b^T\Phi) + O(h^{p+1})$.

**Step 3 (sufficiency).** Subtracting Step 2 from Step 1 gives (2). If (1) holds, every term in (2) is zero, and the local error is $O(h^{p+1})$.

**Step 4 (independence of the elementary differentials).** Fix a tree $t$ with $q$ vertices, labelled $1, \dots, q$ with the root labelled 1. For a vertex $i$, let $t_i$ be the subtree of $t$ rooted at $i$. Define the polynomial vector field $f: \mathbb{R}^q \to \mathbb{R}^q$ by $f_i(y) = \prod_{j \text{ child of } i}y_j$, so $f_i = 1$ when $i$ is a leaf. *Claim:* for every tree $u$, $F(u)(0)_i$ is a nonnegative integer, and it is positive if and only if $u$ is isomorphic to $t_i$.

Proof by induction on $|u|$. For $u = \bullet$, $F(u)(0)_i = f_i(0)$, which is 1 if $i$ is a leaf and 0 otherwise. For $u = [u_1, \dots, u_m]$,
$$F(u)(0)_i = \sum_{j_1, \dots, j_m}\frac{\partial^mf_i}{\partial y_{j_1}\cdots\partial y_{j_m}}(0)\prod_lF(u_l)(0)_{j_l}.$$
Since $f_i$ is a product of distinct variables, the derivative at 0 is 1 if $(j_1, \dots, j_m)$ is an ordering of the children of $i$ (which needs $m$ to equal their number), and 0 otherwise. So $F(u)(0)_i$ is a sum over the bijections $\pi$ from $\{1, \dots, m\}$ to the children of $i$ of $\prod_lF(u_l)(0)_{\pi(l)}$. By induction each term is a nonnegative integer, and it is positive exactly when $u_l \cong t_{\pi(l)}$ for every $l$. Such a $\pi$ exists if and only if $u \cong t_i$. $\square$

**Step 5 (necessity).** Suppose the method has order $p$, but (1) fails for a tree $t$ with $|t| = q \le p$. Take $f$ from Step 4 and $y_0 = 0$. The function $f$ is a polynomial, so the local error is a $C^{p+1}$ function of $h$, and by assumption it is $O(h^{p+1})$. So all its Taylor coefficients of order $q \le p$ vanish. By (2), the coefficient of $h^q$ in component 1 is
$$\sum_{|u| = q}\frac1{\sigma(u)}\Big(\frac1{\gamma(u)} - b^T\Phi(u)\Big)F(u)(0)_1.$$
By Step 4 only $u = t$ contributes, and $F(t)(0)_1 > 0$. So the coefficient is not zero, which is a contradiction. $\square$

**Non-autonomous problems.** Write $z = (\tau, y)$ and $g(z) = (1, f(\tau, y))$. The method applied to $z' = g(z)$ gives stage times $t_0 + h\sum_ja_{ij} = t_0 + c_ih$, exactly the stages of the method applied to $y' = f(t, y)$. If $f$ is $C^{p+1}$, so is $g$. So (1) is sufficient. It is also necessary, because autonomous problems are a special case. $\square$

## Consequences

- **Number of conditions.** The numbers of rooted trees with $q = 1, \dots, 10$ vertices are 1, 1, 2, 4, 9, 20, 48, 115, 286, 719. So order $p = 1, \dots, 10$ needs 1, 2, 4, 8, 17, 37, 85, 200, 486, 1205 conditions. These counts were checked by generating the trees.
- **The classical method.** The [classical Runge-Kutta method](/classical-runge-kutta-4/) satisfies the eight conditions in the table exactly, checked with `Fraction`. It fails all nine conditions of order 5. For example, $\sum b_ic_i^4 = \tfrac5{24} \ne \tfrac15$ and $\sum b_ia_{ij}a_{jk}a_{kl}c_l = 0 \ne \tfrac1{120}$. So its order is exactly 4.
- **Stability function.** For the tall trees $[\dots[\bullet]\dots]$ with $q$ vertices, (1) reads $b^TA^{q-1}\mathbf 1 = 1/q!$. The stability function is $R(z) = 1 + \sum_{q \ge 1}z^qb^TA^{q-1}\mathbf 1$ (a finite sum for explicit methods), so order $p$ gives $R(z) = e^z + O(z^{p+1})$.
- **First barrier for explicit methods.** For an explicit method, $A$ is strictly lower triangular, so $A^s = 0$ and $b^TA^{q-1}\mathbf 1 = 0$ for $q > s$. The condition $b^TA^{p-1}\mathbf 1 = 1/p! \ne 0$ then needs $p \le s$. Butcher proved stronger barriers: order 5 needs 6 stages, order 6 needs 7, order 7 needs 9, and order 8 needs 11. Those proofs are not given here.
- **Design of methods and pairs.** The conditions are polynomial equations in the tableau. For [embedded pairs](/embedded-runge-kutta-pairs/) the conditions are imposed on both $b$ and $\hat b$ with the same $A$. The tests for the [Cash-Karp pair](/cash-karp-method/) check all 37 conditions up to order 6 in exact arithmetic.
- **Simplifying assumptions.** Butcher's conditions $B(p)$: $\sum b_ic_i^{k-1} = 1/k$ for $k \le p$, $C(\eta)$: $\sum_ja_{ij}c_j^{k-1} = c_i^k/k$ for $k \le \eta$, and $D(\zeta)$ reduce the number of independent conditions. If $B(p)$, $C(\eta)$ and $D(\zeta)$ hold with $p \le \eta + \zeta + 1$ and $p \le 2\eta + 2$, the method has order $p$ (HNW I, Section II.7). This gives order $2s$ for the [Gauss methods](/gauss-legendre-runge-kutta/) and explains the order of [collocation methods](/collocation-method/).

## Tightness

- **No condition can be dropped.** Step 4 shows that for each tree there is a polynomial system on which only that condition matters at its order. So (1) is a minimal set of conditions for systems of equations.
- **The hypothesis $c = A\mathbf 1$ matters.** Heun's method with $c_2$ changed from 1 to 0 has the same $A$ and $b$, so it still has order 2 on autonomous problems. On $y' = t$ it gives $y_1 = y_0 + ht_0$, while the exact value is $y_0 + ht_0 + h^2/2$. The local error is $h^2/2$ (0.005 at $h = 0.1$ and 0.00125 at $h = 0.05$), so the order is only 1.
- **Smoothness.** Order $p$ is a statement about $f \in C^{p+1}$. For less smooth $f$, the observed order can be lower, and the expansion (2) does not exist.

## History

Kutta (1901) found the eight conditions for order 4 by direct expansion and gave the classical method. Expansions of this kind grow quickly with the order, and errors in early fifth order methods were corrected later by Nyström (1925). Merson (1957) used rooted trees to organize the expansion. Butcher (1963) gave the general theory with the density $\gamma$ and the elementary weights, which is the theorem above. In 1972 he gave an algebraic theory of these series. Hairer and Wanner (1974) named the resulting group the Butcher group and introduced the term B-series. Cayley (1857) had counted rooted trees in another context.

## References
