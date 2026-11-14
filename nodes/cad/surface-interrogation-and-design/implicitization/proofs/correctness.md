---
title: The Sylvester resultant of X - xW and Y - yW vanishes exactly on the closure of a rational curve, has total degree at most d, and is recovered exactly by interpolation
proves: [correctness]
status: full
---

Let $X, Y, W$ be polynomials in $t$ with coefficients in $\mathbb{Q}$, not all of degree below $d$, where $d = \max(\deg X, \deg Y, \deg W) \ge 1$, and with $W \ne 0$. The curve is $C = \{(X(t) / W(t), Y(t) / W(t)) : t \in \mathbb{C}, W(t) \ne 0\}$. Write $X_d, Y_d, W_d$ for the coefficients of $t^d$. For a point $(x, y) \in \mathbb{C}^2$ put

$$A_x(t) = X(t) - x W(t), \qquad B_y(t) = Y(t) - y W(t),$$

both read as polynomials of formal degree $d$, with leading coefficients $X_d - x W_d$ and $Y_d - y W_d$, and let $R(x, y) = \det S(A_x, B_y)$ be the determinant of their $2d \times 2d$ Sylvester matrix, the matrix of lines L3 and L4. Call $t_0 \in \mathbb{C}$ a *base point* if $X(t_0) = Y(t_0) = W(t_0) = 0$, and call the point $p_\infty = (X_d / W_d, Y_d / W_d)$, defined when $W_d \ne 0$, the point of the curve at $t = \infty$.

**Lemma (the Sylvester criterion with formal degrees).** For polynomials $A, B$ of formal degree $d$, $\det S(A, B) = 0$ exactly when $A$ and $B$ have a common root in $\mathbb{C}$ or both formal leading coefficients are $0$.

*Proof.* The rows of $S(A, B)$ are the coefficient vectors of $t^i A$ and $t^i B$ for $0 \le i < d$, in the basis $t^{2d - 1}, \dots, 1$. So $\det S = 0$ exactly when there are polynomials $P, Q$ of degree less than $d$, not both zero, with $P A + Q B = 0$.

If both leading coefficients are $0$, the first column of $S$ is zero and $\det S = 0$. If $A$ and $B$ have a common root $t_0$, write $A = (t - t_0) A_1$ and $B = (t - t_0) B_1$ with $\deg A_1, \deg B_1 < d$; then $P = B_1$, $Q = -A_1$ give $P A + Q B = 0$, and they are not both zero unless $A = B = 0$, in which case $S = 0$ anyway.

Conversely, let $P A + Q B = 0$ with $P, Q$ not both zero, and say the leading coefficient of $A$ is not $0$, so $\deg A = d$. If $Q = 0$ then $P A = 0$, so $P = 0$, which is excluded. So $Q \ne 0$ and $A$ divides $Q B$. If $A$ and $B$ had no common root, $A$ would divide $Q$, which is impossible since $0 \le \deg Q < d = \deg A$. The case of a nonzero leading coefficient of $B$ is the same. $\square$

**Claim 1 (the curve and only the curve).** Assume there is no base point. Then $R(x, y) = 0$ exactly when $(x, y) \in C$ or $(x, y) = p_\infty$.

*Proof.* If $(x, y) = (X(t_0) / W(t_0), Y(t_0) / W(t_0))$, then $A_x(t_0) = B_y(t_0) = 0$, so $R = 0$ by the lemma. If $(x, y) = p_\infty$, both leading coefficients are $0$, so $R = 0$. Conversely, let $R(x, y) = 0$. By the lemma, either both leading coefficients are $0$, so $X_d = x W_d$ and $Y_d = y W_d$, which forces $W_d \ne 0$ (otherwise $X_d = Y_d = W_d = 0$, against the choice of $d$) and then $(x, y) = p_\infty$; or $A_x$ and $B_y$ have a common root $t_0$. In the second case, if $W(t_0) = 0$, then $X(t_0) = A_x(t_0) = 0$ and $Y(t_0) = 0$, a base point, which is excluded. So $W(t_0) \ne 0$, and $x = X(t_0) / W(t_0)$, $y = Y(t_0) / W(t_0)$. $\square$

The point $p_\infty$ is the limit of the curve as $t \to \infty$, so the zero set of $R$ is the image of the whole projective line, the closure of $C$.

**Claim 2 (degree in each variable).** $R$ is a polynomial of degree at most $d$ in $x$ and at most $d$ in $y$, and lines L2 to L5 return it exactly.

*Proof.* The first $d$ rows of $S(A_x, B_y)$ have entries linear in $x$ and free of $y$, and the last $d$ rows have entries linear in $y$ and free of $x$. Expanding the determinant as a sum over permutations, each term is a product of $d$ entries of the first kind and $d$ of the second, so it has degree at most $d$ in $x$ and in $y$.

Lines L3 and L4 compute $R(x_i, y_j)$ exactly in rational arithmetic, at the $(d + 1)^2$ points of the grid $\{0, \dots, d\}^2$. Two polynomials of degree at most $d$ in each variable that agree on the grid are equal: their difference, for each fixed $x_i$, is a polynomial in $y$ of degree at most $d$ with $d + 1$ roots, so it is zero; hence each of its coefficients, a polynomial in $x$ of degree at most $d$, vanishes at the $d + 1$ values $x_i$ and is zero. Line L5 interpolates first in $y$ for each $x_i$, then in $x$ for each power of $y$, by solving Vandermonde systems with distinct nodes, which have unique solutions. So it returns $R$. Line L6 only multiplies by a nonzero rational number. $\square$

**Claim 3 (total degree).** $R$ has total degree at most $d$.

*Proof.* Fix a point $(x_0, y_0)$ and a direction $(p, q)$ with $p \ne 0$, and restrict $R$ to the line $(x_0 + s p, y_0 + s q)$. There $A = A_{x_0} - s p W$ and $B = B_{y_0} - s q W$. Put $E = q A - p B = q A_{x_0} - p B_{y_0}$, which does not depend on $s$. Replacing each row $t^i B$ of the Sylvester matrix by $t^i E = q \, t^i A - p \, t^i B$ adds a multiple of the row $t^i A$ and multiplies the row by $-p$, so $\det S(A, E) = (-p)^d \det S(A, B)$. Now $\det S(A, E)$ is a sum of products of $d$ entries from the rows of $A$, each of degree at most $1$ in $s$, and $d$ entries from the rows of $E$, free of $s$, so it has degree at most $d$ in $s$. Hence $s \mapsto R(x_0 + s p, y_0 + s q)$ has degree at most $d$.

If $R$ had total degree $D > d$, let $R_D$ be its homogeneous part of degree $D$. The coefficient of $s^D$ in $R(x_0 + s p, y_0 + s q)$ is $R_D(p, q)$, so $R_D(p, q) = 0$ for all $p \ne 0$ and all $q$. A polynomial that vanishes on the dense set $\{p \ne 0\}$ is zero, a contradiction. $\square$

**Claim 4 (not identically zero).** With no base point, $R$ is not the zero polynomial.

*Proof.* Since $W \ne 0$, there is at most one $x_0$ with $X = x_0 W$. Choose any other $x_0$, so $A_{x_0} \ne 0$. By Claim 1, the zeros of $R$ on the line $x = x_0$ are the points $(x_0, Y(t_0) / W(t_0))$ for the roots $t_0$ of $A_{x_0}$ with $W(t_0) \ne 0$, at most $d$ of them, and possibly $p_\infty$. So $R(x_0, \cdot)$ has at most $d + 1$ zeros, and choosing $y_0$ outside them gives $R(x_0, y_0) \ne 0$. $\square$

With a base point $t_0$, every $A_x$ and $B_y$ has the root $t_0$, so $R$ is the zero polynomial: dividing $X$, $Y$ and $W$ by their greatest common divisor first is necessary.

So for a curve without base points, line L6 returns a nonzero polynomial of total degree at most $d$ whose complex zero set is exactly the closure of the curve. That $R$ is a power $G^k$ of an irreducible polynomial $G$, where $k$ is the number of parameter values that map to a general point of the curve, is the classical refinement of Claim 1; it is cited from Sederberg, Anderson and Goldman (1984), not proved here. $\blacksquare$
