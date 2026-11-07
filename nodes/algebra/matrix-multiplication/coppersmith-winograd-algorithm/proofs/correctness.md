---
title: The q + 2 approximate products compute the Coppersmith-Winograd bilinear map
proves: [correctness, termination]
status: full
---

Let $R$ be a ring with subtraction: an additive abelian group with an associative multiplication that distributes over addition on both sides. Commutativity of $R$ is not used. Let ε be an indeterminate that commutes with every element of $R$, and work in the polynomial ring $R[\varepsilon]$. In every product the $x$ factor is on the left and the $y$ factor on the right.

Fix $q \ge 0$ and $x, y \in R^{q+2}$, indexed from $0$ to $q + 1$. The target is
$$\varphi_0 = \sum_{i=1}^{q} x_i y_i + x_0 y_{q+1} + x_{q+1} y_0, \qquad \varphi_i = x_0 y_i + x_i y_0 \ (1 \le i \le q), \qquad \varphi_{q+1} = x_0 y_0.$$

## The products

By distributivity, and since ε commutes with $R$,
$$\begin{aligned}
P_i &= (x_0 + \varepsilon x_i)(y_0 + \varepsilon y_i) = x_0 y_0 + \varepsilon (x_0 y_i + x_i y_0) + \varepsilon^2 x_i y_i \qquad (1 \le i \le q), \\
P_{q+1} &= (x_0 + \varepsilon^2 X)(y_0 + \varepsilon^2 Y) = x_0 y_0 + \varepsilon^2 (x_0 Y + X y_0) + \varepsilon^4 X Y, \\
P_{q+2} &= (x_0 + \varepsilon^3 x_{q+1})(y_0 + \varepsilon^3 y_{q+1}) = x_0 y_0 + \varepsilon^3 (x_0 y_{q+1} + x_{q+1} y_0) + \varepsilon^6 x_{q+1} y_{q+1},
\end{aligned}$$
where $X = \sum_{i=1}^q x_i$ and $Y = \sum_{i=1}^q y_i$ as in line L2. Also $x_0 Y + X y_0 = \sum_{i=1}^q (x_0 y_i + x_i y_0)$ by distributivity.

## The outputs

Write $[\varepsilon^k] f$ for the coefficient of $\varepsilon^k$ in $f \in R[\varepsilon]$.

**Output 0 (line L5).** $c_0 = \varepsilon \sum_{i} P_i - P_{q+1} + P_{q+2} - q \varepsilon P_{q+2}$. Its coefficients up to $\varepsilon^3$ are:

- $[\varepsilon^0]$: $0 - x_0 y_0 + x_0 y_0 - 0 = 0$;
- $[\varepsilon^1]$: $q\, x_0 y_0 - 0 + 0 - q\, x_0 y_0 = 0$;
- $[\varepsilon^2]$: $\sum_i (x_0 y_i + x_i y_0) - (x_0 Y + X y_0) + 0 - 0 = 0$;
- $[\varepsilon^3]$: $\sum_i x_i y_i - 0 + (x_0 y_{q+1} + x_{q+1} y_0) - q\, [\varepsilon^2] P_{q+2} = \varphi_0$, since $[\varepsilon^2] P_{q+2} = 0$.

**Outputs 1 to q (line L6).** $P_i - P_{q+1} = \varepsilon (x_0 y_i + x_i y_0) + \varepsilon^2 (x_i y_i - x_0 Y - X y_0) - \varepsilon^4 X Y$ has zero constant term, so $c_i = \varepsilon^2 (P_i - P_{q+1})$ has $[\varepsilon^0] c_i = [\varepsilon^1] c_i = [\varepsilon^2] c_i = 0$ and $[\varepsilon^3] c_i = x_0 y_i + x_i y_0 = \varphi_i$.

**Output q + 1 (line L7).** $c_{q+1} = \varepsilon^3 P_{q+2}$, so its coefficients below $\varepsilon^3$ are $0$ and $[\varepsilon^3] c_{q+1} = [\varepsilon^0] P_{q+2} = x_0 y_0 = \varphi_{q+1}$.

So line L8 returns $(\varphi_0, \ldots, \varphi_{q+1})$. The case $q = 0$ is included: the sums over $i$ are empty, $X = Y = 0$, and the same computation applies.

The computation also shows that $c_k = \varepsilon^3 \varphi_k + O(\varepsilon^4)$ for every $k$. In trilinear form, with $Z = \sum_{i=1}^q z_i$, this is
$$\sum_{i=1}^{q} \varepsilon (x_0 + \varepsilon x_i)(y_0 + \varepsilon y_i)(z_0 + \varepsilon z_i) - (x_0 + \varepsilon^2 X)(y_0 + \varepsilon^2 Y)(z_0 + \varepsilon^2 Z) + (1 - q\varepsilon)(x_0 + \varepsilon^3 x_{q+1})(y_0 + \varepsilon^3 y_{q+1})(z_0 + \varepsilon^3 z_{q+1}) = \varepsilon^3 T_q + O(\varepsilon^4),$$
because the coefficient of $z_k$ on the left is $c_k$, up to the term $-q\varepsilon^4 P_{q+2} z_{q+1}$, which is $O(\varepsilon^4)$. Hence $\underline{R}(T_q) \le q + 2$ with error degree $3$.

## The exact version by interpolation

Let $\tilde c_k$ be $c_k$ as written in lines L5 to L7, a polynomial in ε. Each $P_r$ has degree at most $6$ and each multiplier in L5 to L7 has degree at most $3$, so $\tilde c_k$ has degree at most $9$, and by the above its coefficients of $\varepsilon^0, \varepsilon^1, \varepsilon^2$ are zero. So $f_k(\varepsilon) = \tilde c_k(\varepsilon) / \varepsilon^3$ is a polynomial of degree at most $6$ with $f_k(0) = \varphi_k$. Over $\mathbb{Q}$, or over a field with at least $8$ elements, the values of $f_k$ at the $7$ distinct nonzero points $1, \ldots, 7$ determine $f_k$, and Lagrange interpolation gives
$$\varphi_k = f_k(0) = \sum_{t=1}^{7} f_k(t) \prod_{s \ne t} \frac{-s}{t - s}.$$
Each $f_k(t)$ is computed from the $q + 2$ products at $\varepsilon = t$, divided by $t^3$, so the exact version uses $7(q + 2)$ products and divides only by the nonzero constants $t^3$ and $t - s$. The implementation requires a prime modulus larger than $7$, so that $1, \ldots, 7$ are distinct and nonzero.

## Termination

Lines L1 and L6 are loops over $i = 1, \ldots, q$, and every other line is a single step. Each step is a finite operation on polynomials of degree at most $9$ in ε. So the algorithm stops after $O(q)$ steps. The interpolation version makes $7$ such runs and a fixed number of further operations per output.
