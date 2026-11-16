---
title: A Stewart-Trinkle step obeys the discrete contact laws and does not add energy
proves: [correctness]
status: full
---

We use the notation of the page. The system has the mass matrix $M$, symmetric and positive definite, and the contacts $i = 1, \ldots, c$ with $\phi_i \le \varepsilon$ are active. Contact $i$ has the normal row $n_i$, the $k$ friction edge directions $d_{i1}, \ldots, d_{ik}$, the impulses $c_{n,i}$ and $\beta_{i1}, \ldots, \beta_{ik}$, and the slack $\lambda_i$. $N$ and $D$ have these as columns, $E$ is the block diagonal matrix with one column of ones of length $k$ per contact, and $U = \mathrm{diag}(\mu_i)$. Let $v^* = v + h M^{-1} f$ and, for a vector $z = (c_n, \beta, \lambda)$,
$$P = N c_n + D \beta, \qquad v^+ = v^* + M^{-1} P .$$
The LCP of line L7 asks for $z \ge 0$ with $w = A z + b \ge 0$ and $z^T w = 0$, with $A$ and $b$ from lines L4 to L6.

**Lemma 1 (the parts of $w$).** For every $z$,
$$w_{c_n} = N^T v^+ + \phi / h, \qquad w_\beta = D^T v^+ + E \lambda, \qquad w_\lambda = U c_n - E^T \beta .$$

*Proof.* By lines L4 and L6, $w_{c_n} = N^T M^{-1} N c_n + N^T M^{-1} D \beta + N^T v^* + \phi/h = N^T (v^* + M^{-1} P) + \phi/h$. In the same way, $w_\beta = D^T M^{-1} P + E \lambda + D^T v^* = D^T v^+ + E\lambda$. The last row is line L5. $\square$

**Theorem 1 (discrete contact laws).** Let $z$ solve the LCP. Then for each active contact $i$:

1. (no penetration to first order) $\phi_i + h\, n_i^T v^+ \ge 0$, and $c_{n,i} > 0$ only if $\phi_i + h\, n_i^T v^+ = 0$;
2. (friction cone) $\beta_i \ge 0$ and $\sum_j \beta_{ij} \le \mu_i c_{n,i}$, so the contact impulse lies in the linearized friction cone;
3. (maximal dissipation) $\beta_i$ minimizes the power $\sum_j \beta'_j\, d_{ij}^T v^+$ over all $\beta' \ge 0$ with $\sum_j \beta'_j \le \mu_i c_{n,i}$;
4. (slip) if $d_{ij}^T v^+ < 0$ for some $j$, then $\sum_j \beta_{ij} = \mu_i c_{n,i}$ and $\lambda_i = \max_j (-d_{ij}^T v^+)$.

*Proof.* Part 1 is $w_{c_n} \ge 0$ and $c_n^T w_{c_n} = 0$ with Lemma 1, multiplied by $h > 0$. Part 2 is $\beta \ge 0$ and $w_\lambda \ge 0$.

For part 3, fix $i$ and write $s_j = d_{ij}^T v^+$. The problem in part 3 is a linear program in $\beta'$. Its KKT conditions, with the multiplier $\lambda_i$ of the constraint $\sum_j \beta'_j \le \mu_i c_{n,i}$, are
$$s_j + \lambda_i \ge 0, \quad \beta'_j \ge 0, \quad \beta'_j (s_j + \lambda_i) = 0, \quad \lambda_i \ge 0, \quad \lambda_i \big(\mu_i c_{n,i} - \textstyle\sum_j \beta'_j\big) = 0 .$$
By Lemma 1, these are exactly the rows of $w_\beta \ge 0$ and $w_\lambda \ge 0$ for contact $i$, with their complementarity. For a linear program the KKT conditions are sufficient for optimality, so $\beta_i$ is a minimizer.

For part 4, the first condition gives $\lambda_i \ge -s_j > 0$, and then the last condition gives $\sum_j \beta_{ij} = \mu_i c_{n,i}$. If $c_{n,i} > 0$, some $\beta_{ij} > 0$, and for it $\lambda_i = -s_j$; with $\lambda_i \ge -s_{j'}$ for all $j'$ this is the maximum. If $c_{n,i} = 0$, all $\beta_{ij} = 0$, and $\lambda_i$ can be any value at least $\max_j(-s_j)$; the claim about $\lambda_i$ holds only up to this case. $\square$

**Theorem 2 (no energy from the contacts).** Let $z$ solve the LCP and assume that $\phi_i \ge 0$ for every active contact. Then $\tfrac12 (v^+)^T M v^+ \le \tfrac12 (v^*)^T M v^*$.

*Proof.* From $v^* = v^+ - M^{-1} P$,
$$\tfrac12 (v^*)^T M v^* = \tfrac12 (v^+)^T M v^+ - P^T v^+ + \tfrac12 P^T M^{-1} P .$$
The last term is at least 0, so it is enough to show $P^T v^+ \le 0$. Now $P^T v^+ = c_n^T N^T v^+ + \beta^T D^T v^+$. By Theorem 1, part 1, $c_{n,i}\, n_i^T v^+ = -c_{n,i} \phi_i / h \le 0$. By the complementarity of $\beta$ and $w_\beta$ and of $\lambda$ and $w_\lambda$,
$$\beta_i^T D_i^T v^+ = -\lambda_i \textstyle\sum_j \beta_{ij} = -\lambda_i \mu_i c_{n,i} \le 0 .$$
The sum of these terms is $P^T v^+ \le 0$. $\square$

The assumption $\phi_i \ge 0$ is necessary. If a contact has $\phi_i < 0$ at the start of the step, the term $\phi_i / h$ asks for a separating velocity, and the normal impulse then does positive work. This is the price of the gap term in line L6: it removes the drift into the ground but it can add energy.

**Lemma 2 (Lemke's method ends).** With the lexicographic ratio test of line L18, Lemke's method of lines L11 to L20 stops after a finite number of pivots, either with $z_0$ leaving the basis or on a ray.

*Proof.* If $b \ge 0$, line L11 returns $z = 0$, which solves the LCP. Otherwise the tableau of line L12 holds $w - A z - e z_0 = b$. After the pivot of line L13, $z_0 = -\min_i b_i > 0$ and every basic variable is at least 0. Every later basis is almost complementary: it contains $z_0$ and, for every index but one, exactly one of $w_i$ and $z_i$. The lexicographic ratio test keeps every row of the matrix $(\text{right side}, B^{-1})$ lexicographically positive, and with it the leaving row of each pivot is unique (Cottle, Pang and Stone, Chapter 4). An almost complementary basis therefore has at most two neighbours on the path: the two pivots in which one member of the missing pair enters. The path enters through one and leaves through the other. The start has only one neighbour on the path, because the other direction from it is the primary ray. Suppose that a basis repeats, and take the first one that does. It is not the start, so it would have three different neighbours on the path: the one before its first visit, the one after it, and the one before its second visit. This is not possible, so no basis repeats. There are at most $m\, 2^{m-1}$ almost complementary bases, so the path is finite. It stops when line L19 finds no positive entry in the entering column, which is a ray, or when $z_0$ leaves at line L16. $\square$

**Lemma 3 (the output solves the LCP).** If $z_0$ leaves at line L16, the vector $z$ of line L20 solves the LCP.

*Proof.* After $z_0$ leaves, $z_0 = 0$ and the basis is complementary: for each $i$ exactly one of $w_i$ and $z_i$ is basic, and the nonbasic one is 0. All basic values are at least 0, because every pivot of the method keeps the right side nonnegative. So $z \ge 0$, $w = A z + b \ge 0$ and $z_i w_i = 0$ for every $i$. $\square$

**Existence.** Lemke's method can end on a ray, and then it gives no solution. For the velocity form of the step, where $b$ has no term $\phi/h$, Anitescu and Potra (1997) proved that the LCP always has a solution and that Lemke's method finds it. With the gap term of line L6, Trinkle, Berard and Pang (2005) describe the LCP as nearly always solvable, not always. The implementation raises an error on a ray.

**Line L9.** The new configuration is $q^+ = q + h v^+$, a semi-implicit Euler step: the position update uses the new velocity. For a body that moves in a plane with $q = (x, y, \theta)$ this is exact for the coordinates. For a body in space, $q^+$ must be formed with the exponential map of the rotation; see the pitfalls on the page.

**Cost.** Lines L2 to L6 cost $O(n^3 + n^2 m + n m^2)$ for $n$ velocities and $m$ unknowns, with a Cholesky factor of $M$. Each pivot of Lemke's method updates a tableau of $m$ rows and $2m + 2$ columns in $\Theta(m^2)$ operations. By the proof of Lemma 2, the number of pivots is at most $m\, 2^{m-1} + 1$. Murty (1978) gave LCPs on which Lemke's method needs a number of pivots exponential in $m$.
