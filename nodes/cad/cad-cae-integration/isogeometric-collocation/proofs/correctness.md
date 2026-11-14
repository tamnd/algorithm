---
title: Collocation at the Greville abscissae has a unique solution and is exact on the spline space
proves: [correctness]
status: full
---

We use the notation of the page. The degree is $p \ge 2$. The knot vector $\xi = (\xi_1, \ldots, \xi_{n+p+1})$ is open on $[a, b]$, so $\xi_1 = \cdots = \xi_{p+1} = a$ and $\xi_{n+1} = \cdots = \xi_{n+p+1} = b$, and each interior knot value has multiplicity at most $p - 1$. $N_{j,d}$ is the B-spline of degree $d$ with the knots $\xi_j, \ldots, \xi_{j+d+1}$, taken right-continuous, with the value at $b$ taken as the limit from the left. A spline value at a knot where it jumps is the limit from the right, as in line L5.

**Fact 1 (knot runs).** (a) For $3 \le k \le n$, the $p$ knots $\xi_k, \ldots, \xi_{k+p-1}$ are not all equal. (b) For $1 \le i \le n - 1$, the $p + 1$ knots $\xi_{i+1}, \ldots, \xi_{i+p+1}$ are not all equal.

*Proof.* The value $a$ occurs exactly at $\xi_1, \ldots, \xi_{p+1}$, the value $b$ exactly at $\xi_{n+1}, \ldots, \xi_{n+p+1}$, and an interior value at most $p - 1$ times. (a) A run that starts at $\xi_k$ with $k \ge 3$ holds at most the $p - 1$ copies $\xi_3, \ldots, \xi_{p+1}$ of $a$. A run that ends at $\xi_{k+p-1}$ with $k \le n$ ends at $\xi_{n+p-1}$ or earlier, so it holds at most the $p - 1$ copies $\xi_{n+1}, \ldots, \xi_{n+p-1}$ of $b$. An interior value gives at most $p - 1$ equal knots. So no $p$ of these knots are equal. (b) A run that starts at $\xi_2$ or later holds at most $p$ copies of $a$, one that ends at $\xi_{n+p}$ or earlier holds at most $p$ copies of $b$, and an interior value gives at most $p - 1$. So no $p + 1$ of these knots are equal. $\square$

**Lemma 1 (the Greville points).** $\tau_1 = a$, $\tau_n = b$, $\tau_1 < \tau_2 < \cdots < \tau_n$, and for $2 \le i \le n - 1$ the point $\tau_i$ lies strictly between $\xi_{i+1}$ and $\xi_{i+p}$.

*Proof.* $\tau_1$ is the mean of $\xi_2, \ldots, \xi_{p+1}$, which all equal $a$, and $\tau_n$ is the mean of $\xi_{n+1}, \ldots, \xi_{n+p}$, which all equal $b$. Next, $\tau_{i+1} - \tau_i = (\xi_{i+p+1} - \xi_{i+1}) / p \ge 0$, and it is zero only if the $p + 1$ knots $\xi_{i+1}, \ldots, \xi_{i+p+1}$ are equal, which Fact 1(b) excludes for $1 \le i \le n - 1$. For the last claim, $\tau_i$ is the mean of the $p$ knots $\xi_{i+1}, \ldots, \xi_{i+p}$, and with $k = i + 1 \in \{3, \ldots, n\}$ Fact 1(a) says they are not all equal. A mean of numbers that are not all equal lies strictly between their least and their largest value, here $\xi_{i+1}$ and $\xi_{i+p}$. $\square$

**Lemma 2 (the space of second derivatives).** For each $u \in S_p(\xi)$, the second derivative $u''$ (right limits at the knots) lies in $V = \operatorname{span}\{M_k : 3 \le k \le n\}$ with $M_k = N_{k,p-2}$. The $n - 2$ functions $M_k$ are linearly independent on $[a, b)$.

*Proof.* The derivative formula for B-splines (de Boor, Chapter X) gives

$$ N_{j,d}' = \frac{d}{\xi_{j+d} - \xi_j} N_{j,d-1} - \frac{d}{\xi_{j+d+1} - \xi_{j+1}} N_{j+1,d-1}, $$

on each knot span, with a term dropped when its denominator is zero. Applied twice, it writes $u''$ for $u = \sum_{j=1}^{n} c_j N_{j,p}$ as a combination of $N_{k,p-2}$ for $1 \le k \le n + 2$. The function $N_{k,p-2}$ has the $p$ knots $\xi_k, \ldots, \xi_{k+p-1}$. For $k = 1, 2$ these knots all equal $a$, and for $k = n + 1, n + 2$ they all equal $b$, so these four functions are zero. That leaves $3 \le k \le n$. For these $k$ the knots of $M_k$ are not all equal by Fact 1(a), so $M_k$ is a non-zero B-spline. The knot sequence $\xi_3, \ldots, \xi_{n+p-1}$ of the $M_k$ has no value of multiplicity more than $p - 1 = (p - 2) + 1$, so by the Curry-Schoenberg theorem the $M_k$ are a basis of the splines of degree $p - 2$ on it, and in particular they are linearly independent. $\square$

**Theorem.** Under the precondition above, the $n \times n$ matrix of lines L3 to L7 is non-singular. If the exact solution $u$ of $-u'' = f$, $u(a) = g_a$, $u(b) = g_b$ lies in $S_p(\xi)$, then IGA-COLLOCATION returns its coefficients.

*Proof.* A square matrix is non-singular if its kernel is zero. So let $c$ satisfy the homogeneous system, and let $v = \sum_j c_j N_{j,p}$. Then $v(a) = 0$ (line L3), $v(b) = 0$ (line L7), and $v''(\tau_i) = 0$ for $2 \le i \le n - 1$ (line L5).

By Lemma 2, $v'' = \sum_{k=3}^{n} d_k M_k$ for some numbers $d_k$. Re-index the interior rows by $k = i + 1$: row $i$ asks the element $v''$ of $V$ to vanish at $x_k = \tau_{k-1}$, for $k = 3, \ldots, n$. By Lemma 1 these $n - 2$ points are strictly increasing, and $x_k = \tau_{k-1}$ lies strictly between $\xi_k$ and $\xi_{k+p-1}$, the first and the last knot of $M_k$. A B-spline is positive on the open interval between its first and its last knot, so $M_k(x_k) > 0$ for each $k$. This is the condition of the Schoenberg-Whitney theorem (de Boor, Chapter XIII): interpolation in $V$ at the points $x_3 < \cdots < x_n$ has a unique solution. The zero spline interpolates zero data, so $v'' = 0$, that is, all $d_k = 0$.

So $v'' = 0$ on each knot span, and $v'$ is constant on each span. The interior knots have multiplicity at most $p - 1$, so $v$ is $C^1$ on $[a, b]$ and $v'$ is continuous. A continuous function that is constant on each span of a partition is constant. So $v$ is a polynomial of degree at most 1, and $v(a) = v(b) = 0$ gives $v = 0$. The B-splines $N_{j,p}$ are linearly independent, so $c = 0$. The kernel is zero, and the matrix is non-singular.

For the second claim, let $u = \sum_j u_j N_{j,p} \in S_p(\xi)$ be the exact solution. Then $u(a) = g_a$ and $u(b) = g_b$, and $-u''(\tau_i) = f(\tau_i)$ for every interior $i$, so the vector $(u_j)$ solves the system of lines L3 to L7. By the first part this system has exactly one solution, and line L8 returns it. So the method returns $u$. $\blacksquare$

**The precondition is needed.** Let $p = 2$ and $\xi = (0, 0, 0, \tfrac12, \tfrac12, 1, 1, 1)$, with the interior knot of multiplicity $p = 2$. Then $n = 5$, $\tau = (0, \tfrac14, \tfrac12, \tfrac34, 1)$, and $S_2$ holds $v(x) = \min(x, 1 - x)$, which is $C^0$ at $\tfrac12$. It has $v'' = 0$ on both spans and $v(0) = v(1) = 0$. So $v \ne 0$ is in the kernel, and the matrix is singular. In the proof, the step from $v'' = 0$ to "$v$ is linear" fails because $v'$ jumps.

**What is not proved here.** The theorem gives existence, uniqueness and exactness on $S_p$. It gives no error bound for a solution outside $S_p$. The orders $h^p$ (even $p$) and $h^{p-1}$ (odd $p$) in $L^2$ and $H^1$, and $h^{p-1}$ in $H^2$, are cited from Auricchio and coauthors (2010) and Montardini, Sangalli and Tamellini (2017), and the table on the page measures them on one problem.
