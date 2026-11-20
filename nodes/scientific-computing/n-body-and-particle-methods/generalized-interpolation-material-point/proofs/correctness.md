---
title: The GIMP weights form a partition of unity, their gradients are continuous in the point position, and tiling domains under a uniform stress give no interior force
proves: [correctness]
status: full
---

We work in 1D with the hats $N_i(x) = \max(0, 1 - |x - x_i| / \Delta x)$, $x_i = i \Delta x$, and exact arithmetic. A point $p$ has the domain $[a_p, b_p] = [x_p - l_p, x_p + l_p]$ with $l_p > 0$, and

$$S_{ip} = \frac{1}{2 l_p} \int_{a_p}^{b_p} N_i(x)\, dx, \qquad S_{ip}' = \frac{N_i(b_p) - N_i(a_p)}{2 l_p}.$$

Line L2 visits every node whose hat is not zero on an open part of the domain, and the other nodes have $S_{ip} = S_{ip}' = 0$, so sums over the visited nodes equal sums over all nodes. We use two facts of the hats: for every $x$, $\sum_i N_i(x) = 1$ and $\sum_i N_i(x)\, x_i = x$ (on the cell $[x_j, x_{j+1}]$ only $N_j$ and $N_{j+1}$ are not zero, and they are $1 - w$ and $w$ with $x = x_j + w \Delta x$).

**Claim 1 (partition of unity).** $\sum_i S_{ip} = 1$, $\sum_i S_{ip}\, x_i = x_p$ and $\sum_i S_{ip}' = 0$.

*Proof.* Only finitely many terms are not zero, so the sum and the integral commute: $\sum_i S_{ip} = \frac{1}{2 l_p} \int_{a_p}^{b_p} \sum_i N_i(x)\, dx = \frac{1}{2 l_p} (b_p - a_p) = 1$. In the same way $\sum_i S_{ip} x_i = \frac{1}{2 l_p} \int_{a_p}^{b_p} x\, dx = \frac{a_p + b_p}{2} = x_p$. Finally $\sum_i S_{ip}' = (\sum_i N_i(b_p) - \sum_i N_i(a_p)) / (2 l_p) = (1 - 1)/(2 l_p) = 0$. $\square$

With Claim 1 in place of the partition of unity of the hats, the proofs of Claims 1, 2 and 3 on the [MPM page](../../material-point-method/proofs/correctness.md) go through word for word: the transfer in line L5 puts all mass and momentum on the grid, the step conserves momentum when no node is fixed (since $\sum_i f_i = -\sum_p V_p \sigma_p \sum_i S_{ip}' = 0$), and a rigid translation with zero stress is reproduced exactly (each point moves by $h \sum_i S_{ip} u = h u$ and has $\dot\varepsilon_p = u \sum_i S_{ip}' = 0$). These need the same assumption as there, that every node with $S_{ip} \ne 0$ or $S_{ip}' \ne 0$ for some point has a positive mass.

**Claim 2 (the gradient).** For fixed $l_p$, $S_{ip}$ is a continuously differentiable function of $x_p$ with derivative $S_{ip}'$, and for all $x$, $y$,
$$|S_{ip}'(x) - S_{ip}'(y)| \le \frac{|x - y|}{l_p \Delta x}.$$

*Proof.* $N_i$ is continuous, so by the fundamental theorem of calculus $\frac{d}{dx_p} \int_{x_p - l_p}^{x_p + l_p} N_i = N_i(x_p + l_p) - N_i(x_p - l_p)$, and dividing by $2 l_p$ gives $S_{ip}'$. This is continuous in $x_p$ because $N_i$ is. $N_i$ is Lipschitz with constant $1/\Delta x$, so each of the two terms changes by at most $|x - y| / \Delta x$, and $|S_{ip}'(x) - S_{ip}'(y)| \le 2 |x - y| / (2 l_p \Delta x)$. $\square$

So the internal force $f_i = -\sum_p V_p \sigma_p S_{ip}'$ is a continuous function of the positions, and it cannot jump when a point crosses a node or a cell boundary. For the hats themselves ($l_p \to 0$), $N_i'$ jumps by $1/\Delta x$ at each node, which is the cell crossing jump of MPM.

**Claim 3 (no interior force for tiling domains).** Let the domains of points $1, \ldots, n$ tile $[a, b]$, that is $a_1 = a$, $b_k = a_{k+1}$ for $k < n$ and $b_n = b$; let $V_p = b_p - a_p = 2 l_p$, and let every point have the stress $\sigma$. Then for every node $i$,
$$f_i = \sigma \bigl(N_i(a) - N_i(b)\bigr).$$

*Proof.* $V_p S_{ip}' = N_i(b_p) - N_i(a_p)$, so
$$f_i = -\sigma \sum_{p=1}^{n} \bigl(N_i(b_p) - N_i(a_p)\bigr) = -\sigma \bigl(N_i(b_n) - N_i(a_1)\bigr),$$
since the sum telescopes by $b_k = a_{k+1}$. $\square$

$N_i(a) = 0$ and $N_i(b) = 0$ for every node with $|x_i - a| \ge \Delta x$ and $|x_i - b| \ge \Delta x$, so these nodes get no force, whatever the sizes and positions of the points. The forces at the remaining nodes are the traction $+\sigma$ at the left end and $-\sigma$ at the right end, spread over the nodes by the hats; in the example of the page, $a = 0$ and $b = 4.8$ give $f = (1, 0, 0, 0, -0.2, -0.8, 0)$.

**Claim 4 (the MPM limit).** If $x_p$ is not a node, then $S_{ip} \to N_i(x_p)$ and $S_{ip}' \to N_i'(x_p)$ as $l_p \to 0$.

*Proof.* $S_{ip}$ is the mean of a continuous function over an interval that shrinks to $x_p$, so it tends to $N_i(x_p)$. For $l_p$ smaller than the distance from $x_p$ to the nearest node, $N_i$ is linear on $[a_p, b_p]$, so $S_{ip}' = (N_i(b_p) - N_i(a_p)) / (b_p - a_p) = N_i'(x_p)$ exactly. $\blacksquare$
