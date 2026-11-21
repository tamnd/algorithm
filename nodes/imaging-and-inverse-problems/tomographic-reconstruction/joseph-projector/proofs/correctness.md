---
title: Correctness of Joseph's projector
proves: [correctness]
status: full
---

We use the conventions of the page. The image is $n \times n$ on $[-1, 1]^2$ with $h = 2/n$, and the center of pixel $(i, j)$ is $(x_j, y_i)$ with $x_j = -1 + (j + 1/2)h$ and $y_i = 1 - (i + 1/2)h$. The ray is the line $L = \{(x, y) : x c + y \sigma = s\}$ with $c = \cos\theta$ and $\sigma = \sin\theta$. Its direction is $\omega^\perp = (-\sigma, c)$, and $t$ is the arc length along it. We treat the case $|c| \ge |\sigma|$, which lines L2 to L7 handle. The other case, lines L8 to L10, is the same with the roles of $x$ and $y$ exchanged. We prove three things: the code computes the quadrature sum that the page defines, the error of that sum is $O(h^2)$ for smooth images, and the back projector is the exact adjoint.

**Lemma 1 (the step length, line L3).** Between the horizontal lines $y = y_i$ and $y = y_{i+1}$, the ray has length $h/|c|$.

*Proof.* Along $L$, $dy/dt = c$, and $c \ne 0$ because $|c| \ge |\sigma|$ and $c^2 + \sigma^2 = 1$. So a change of $h$ in $y$ is a change of $h/|c|$ in $t$. $\square$

**Lemma 2 (the interpolation, lines L5 to L7).** Fix a row $i$. Line L5 finds the point $(x, y_i)$ of $L$ on the line $y = y_i$. Put $\phi_i(x) = (1 - t)f_{ij} + t f_{i,j+1}$ with $j$ and $t$ as in line L6, and with $f_{ik} = 0$ for $k < 0$ or $k \ge n$. Then $\phi_i$ is the continuous, piecewise linear function of $x$ that takes the value $f_{ik}$ at $x_k$ for every integer $k$ (with the zero values outside), and line L7 adds $\Delta\,\phi_i(x)$.

*Proof.* $x c + y_i\sigma = s$ gives $x = (s - y_i\sigma)/c$, which is line L5. The coordinate $u = ((x + 1)n - 1)/2$ is an affine function of $x$ with $u = k$ exactly at $x = x_k$, because $x_k + 1 = (2k + 1)/n$. With $j = \lfloor u\rfloor$ and $t = u - j \in [0, 1)$, the point $x$ lies in $[x_j, x_{j+1})$ and $t = (x - x_j)/h$. The linear interpolant of the values at $x_j$ and $x_{j+1}$ is $(1 - t)f_{ij} + t f_{i,j+1}$. Line L7 skips an index outside the image, which is the same as the value 0 there. $\square$

So, with $\Delta = h/|c|$, lines L2 to L7 compute
$$P(\theta, s) = \Delta \sum_{i=0}^{n-1} \phi_i\!\left(\frac{s - y_i\sigma}{c}\right).$$
This is the definition of Joseph's projector on the page. The weight of pixel $(i, j)$ in it is $\Delta(1 - t)$ or $\Delta t$, which is what the function `ray_weights` returns.

**Theorem 1 (second order accuracy).** Let $f$ be twice continuously differentiable on $\mathbb{R}^2$, with $f = 0$ outside $[-1 + h/2, 1 - h/2]^2$. Let $M$ bound $|f_{xx}|$, $|f_{xy}|$ and $|f_{yy}|$. Let $f_{ij} = f(x_j, y_i)$. Then for every $\theta$ and $s$
$$|P(\theta, s) - \mathcal{R}f(\theta, s)| \le \frac{7 h^2 M}{12\,|c|} \le \frac{7\sqrt{2}}{12}\, h^2 M.$$

*Proof.* Write the line integral with $y$ as the parameter. The point of $L$ at height $y$ is $(X(y), y)$ with $X(y) = (s - y\sigma)/c$, and $dt = dy/|c|$ by Lemma 1. Put $g(y) = f(X(y), y)$. Since $f = 0$ for $|y| > 1$,
$$\mathcal{R}f(\theta, s) = \frac{1}{|c|}\int_{-1}^{1} g(y)\,dy.$$
Split the error in two parts.

*Quadrature.* The intervals $[y_i - h/2, y_i + h/2]$ for $i = 0, \ldots, n-1$ partition $[-1, 1]$, and $h\sum_i g(y_i)$ is the midpoint rule on them. On one interval of length $h$, the midpoint rule has error at most $h^3 \max|g''|/24$, so the total error is at most $n h^3 \max|g''|/24 = h^2\max|g''|/12$. With $\tau = \sigma/c$, $X'(y) = -\tau$ and $|\tau| \le 1$, so
$$g'' = \tau^2 f_{xx} - 2\tau f_{xy} + f_{yy}, \qquad |g''| \le 4M.$$
So $\left|\int_{-1}^{1} g\,dy - h\sum_i g(y_i)\right| \le h^2 M/3$.

*Interpolation.* Fix $i$ and put $x = X(y_i)$. If $x_0 \le x \le x_{n-1}$, then $\phi_i(x)$ is the linear interpolant of $f(\cdot, y_i)$ between two neighbors at distance $h$, and the standard bound for linear interpolation gives $|\phi_i(x) - f(x, y_i)| \le h^2 M/8$. If $x < x_0$, then $f(x, y_i) = 0$ because $x < -1 + h/2$, and $\phi_i(x) = t f_{i0}$ with $f_{i0} = f(-1 + h/2, y_i) = 0$ by continuity, so the error is 0. The case $x > x_{n-1}$ is the same. So $\left|h\sum_i \phi_i(X(y_i)) - h\sum_i g(y_i)\right| \le n h \cdot h^2 M/8 = h^2 M/4$.

Add the two parts and divide by $|c|$: the error is at most $(1/3 + 1/4)h^2 M/|c| = 7h^2M/(12|c|)$. Finally $|c| \ge 1/\sqrt{2}$, because $|c| \ge |\sigma|$ and $c^2 + \sigma^2 = 1$. $\square$

The bound is not sharp, but it shows the order: when $n$ doubles, the error falls by about 4. The page gives the measured values for a Gaussian. For a piecewise constant image, such as a disk, the samples jump, and the error is of the order of $h$ near the jumps. That is a property of the image model, not of the code.

**Theorem 2 (matched back projector).** Let $A$ be the matrix whose row for ray $(\theta, s)$ holds the weights of that ray. The back projector of the code, which adds $w\,v$ to pixel $(i, j)$ for each weight $w$ of a ray with value $v$, computes $A^T v$.

*Proof.* The forward projector computes $(Ax)_r = \sum_{(i,j,w)} w\,x_{ij}$ over the weights of ray $r$. The back projector computes $(Bv)_{ij} = \sum_r \sum_{(i,j,w) \text{ of } r} w\,v_r$, with the same weights. So $\langle Ax, v\rangle = \sum_r\sum_{(i,j,w)} w\,x_{ij}\,v_r = \langle x, Bv\rangle$ for all $x$ and $v$, and $B = A^T$. $\square$

**Exact cases.** If $\theta = 0$ and $s = x_j$, then $u = j$ and $t = 0$ in every row, so $P = h\sum_i f_{ij}$: the exact integral of the piecewise constant image along the center line of column $j$. If the image is constant, $f_{ij} = 1$, and the ray meets every row at a point $x$ with $x_0 \le x \le x_{n-1}$, then every $\phi_i = 1$ and $P = nh/|c| = 2/|c|$, which is the length of the chord of the square between $y = -1$ and $y = 1$. The tests check both cases. In the worked example on the page, the samples come from a linear function $F$, and the ray meets every row inside $[x_0, x_{n-1}]$. Linear interpolation and the midpoint rule are both exact for linear functions, so there $P$ is the exact integral of $F$ along the ray between $y = -1$ and $y = 1$.
