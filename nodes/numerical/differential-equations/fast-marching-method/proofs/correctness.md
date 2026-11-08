---
title: Fast marching returns the unique solution of the upwind discrete eikonal equations
proves: [correctness, termination]
status: full
---

**Setting.** $G$ is the set of grid points with $s < \infty$; neighbours are the up to four axis neighbours inside $G$. $S \subseteq G$ is the nonempty source set. For a point $x \notin S$ write $c_x = s_xh > 0$. For values $T$ on $G$ (with $\infty$ allowed) let $a_x(T)$ and $b_x(T)$ be the smaller of the two horizontal and the two vertical neighbour values, with $\infty$ for missing neighbours. The discrete problem is

$$T_x = 0 \ (x \in S), \qquad T_x = U(c_x, a_x(T), b_x(T)) \ (x \notin S), \tag{D}$$

where, with $\varphi_{a,b}(t) = (t - a)_+^2 + (t - b)_+^2$ and $(r)_+ = \max(r, 0)$, $U(c, a, b)$ is the unique $t > \min(a, b)$ with $\varphi_{a,b}(t) = c^2$, and $U(c, \infty, \infty) = \infty$. If $\min(a, b) < \infty$, $\varphi_{a,b}$ is continuous, zero at $\min(a, b)$, and strictly increasing to $\infty$ on $[\min(a, b), \infty)$, so $U$ is well defined. Solving the quadratic gives the closed form used at line L8: $U = a + c$ if $b - a \ge c$ (with $a \le b$), and $\tfrac12(a + b + \sqrt{2c^2 - (b - a)^2})$ otherwise.

**Lemma 1 (properties of $U$).** Let $c > 0$ and $\min(a, b) < \infty$.

1. Monotone: if $a' \le a$ and $b' \le b$, then $U(c, a', b') \le U(c, a, b)$.
2. Causal: $U(c, a, b) \ge \min(a, b) + c/\sqrt2$.
3. Upwind: if $b \ge U(c, a, b)$, then $U(c, a, b') = U(c, a, b)$ for every $b' \ge U(c, a, b)$, including $b' = \infty$. The same holds with the roles of $a$ and $b$ exchanged.
4. Shift: $U(c, a + D, b + D) = U(c, a, b) + D$ for real $D$.
5. Strictness: if $t = U(c, a, b)$, $a < t$ and $a < a'$, $b \le b'$, then $U(c, a', b') > t$.

*Proof.* (1) $\varphi_{a',b'} \ge \varphi_{a,b}$ pointwise, so at $u = U(c, a, b)$ we have $\varphi_{a',b'}(u) \ge c^2$, and since $\varphi_{a',b'}$ is increasing past $\min(a', b') \le \min(a, b) < u$, its root is at most $u$. (2) At $t = \min(a, b) + c/\sqrt2$ each term of $\varphi$ is at most $c^2/2$, so $\varphi(t) \le c^2$ and the root is at least $t$. (3) If $t = U(c, a, b) \le b$ then $(t - b)_+ = 0 = (t - b')_+$ for $b' \ge t$, so $\varphi_{a,b'}(t) = \varphi_{a,b}(t) = c^2$, and $t > \min(a, b) \ge a \ge \min(a, b')$ (if $t \le a$ as well, $\varphi(t) = 0 \ne c^2$, so $t > a$). By uniqueness of the root, $U(c, a, b') = t$. (4) $\varphi_{a+D,b+D}(t + D) = \varphi_{a,b}(t)$. (5) Since $a < t$, $(t - a)_+ = t - a > (t - a')_+$, and $(t - b)_+ \ge (t - b')_+$, so $\varphi_{a',b'}(t) < c^2$. If $\min(a', b') \ge t$ then $U(c, a', b') > \min(a', b') \ge t$; otherwise $\varphi_{a',b'}$ is increasing past its start below $t$ and its root lies above $t$. $\square$

**Lemma 2 (invariants).** Throughout the run:

- (I1) For every point $y \notin S$ that is not Known, $T_y = U(c_y, a^K_y, b^K_y)$, where $a^K_y, b^K_y$ are the minima over Known neighbours only ($\infty$ if none, and then $T_y = \infty$).
- (I2) Points are made Known in nondecreasing order of $T$, and a Known value never changes.
- (I3) When a point $x$ is popped and accepted with key $\tau$, every heap entry and every non-Known $T_y$ is at least $\tau$.

*Proof.* Values of Known points are never written: line L7 skips Known points and lines L2 and L9 are the only writes. Initially no point is Known and every non-source has $T = \infty = U(c, \infty, \infty)$, so (I1) holds. Making $x$ Known changes $a^K_y$ or $b^K_y$ only for neighbours $y$ of $x$, and those are exactly the points updated at lines L7 to L9. For such $y$, the new $U$ over Known neighbours is at most the old one by Lemma 1(1), since a minimum over a larger set is no larger. Line L9 stores the new $U$ whenever it is smaller and otherwise the stored value equals it already, so (I1) is preserved.

For (I2) and (I3), use induction over pops. Every non-Known point with finite value has a heap entry with key equal to its current value (each write at L2 or L9 pushes one). When $(\tau, x)$ is popped and accepted, $\tau = T_x$ (line L5) and $\tau$ is the smallest key in the heap, so all non-Known values are $\ge \tau$: that is (I3). Now consider a neighbour $y$ whose value is recomputed after $x$ becomes Known. Before, $T_y = U(c_y, a, b) \ge \tau$ by (I3) and (I1). After, one of $a, b$, say $a$, is replaced by $\min(a, \tau)$ and the other is unchanged. If $a \le \tau$ nothing changes. Otherwise let $u = U(c_y, \tau, b)$ and suppose $u < \tau$. Then $(u - a)_+ = 0 = (u - \tau)_+$, so $\varphi_{a,b}(u) = \varphi_{\tau,b}(u) = c_y^2$, and since $u > \min(\tau, b)$ while $u < \tau$, we get $\min(\tau, b) = b < u$. So $u > \min(a, b)$, and by uniqueness $U(c_y, a, b) = u < \tau$, a contradiction. Hence every new value and every new key is $\ge \tau$. Together with (I3) this means all later pops have keys $\ge \tau$, which is (I2). $\square$

**Theorem.** Let $R \subseteq G$ be the set of points joined to $S$ by a path of neighbours in $G$. FAST-MARCHING terminates after at most $|S| + 4|G|$ heap pushes. On return, $T$ is finite exactly on $R$, and $T$ is the unique solution of (D) that is finite on $R$. Every solution of (D) is infinite outside $R$, so (D) has exactly one solution.

*Proof.* **Termination.** A point is accepted at most once (line L5 rejects Known points), each acceptance causes at most 4 pushes, and sources cause $|S|$ pushes, so the heap receives at most $|S| + 4|G|$ entries and the loop pops each once.

**Reachability.** Sources are accepted (each has key 0 and nothing smaller exists). If $x$ is accepted and $y \in G$ is a neighbour, then after $x$ is accepted $T_y \le U(c_y, T_x, \infty) < \infty$ unless $y$ is already Known, so $y$ has a heap entry and is accepted later. By induction along paths, every point of $R$ is accepted with a finite value. Points outside $R$ never get a Known neighbour, so they keep $T = \infty$.

**The output solves (D).** Take $x \in R \setminus S$, accepted with value $t = T_x$. By (I1) at acceptance, $t = U(c_x, a^K, b^K)$ over the neighbours Known at that time. Every other neighbour is accepted later, with value $\ge t$ by (I2), or never, with value $\infty$. By Lemma 1(3), applied once per direction, replacing $a^K, b^K$ by the minima over all neighbours does not change $U$: in each direction the new minimum is either the old one or a value $\ge t$ that replaces $\infty$. So $T_x = U(c_x, a_x(T), b_x(T))$. For $x \notin R$ all neighbours are outside $R$ or obstacles, so $a_x(T) = b_x(T) = \infty$ and $T_x = \infty = U$. Sources have $T = 0$.

**Solutions are infinite outside $R$.** Let $T'$ solve (D) and suppose some point of a connected component $C$ of $G \setminus R$ has a finite value. Pick $x \in C$ with the smallest finite $T'_x$. All its neighbours lie in $C$ or are missing, so $\min(a_x, b_x) \ge T'_x$, while (D) and Lemma 1(2) give $T'_x > \min(a_x, b_x)$, a contradiction.

**Uniqueness on $R$.** Let $T$ and $T'$ be two solutions of (D), both finite on $R$. Suppose $D = \max_{x \in R}(T_x - T'_x) > 0$. Among the points $x$ with $T_x - T'_x = D$ choose one with the smallest $T_x$; it is not a source since sources have difference 0. Write $a = a_x(T)$, $b = b_x(T)$, $a' = a_x(T')$, $b' = b_x(T')$. For every point $y$, $T_y \le T'_y + D$ (outside $R$ both are $\infty$), so $a \le a' + D$ and $b \le b' + D$. If $a < T_x$ and $a < a' + D$, Lemma 1(5) and (4) give $T'_x + D = U(c_x, a' + D, b' + D) > U(c_x, a, b) = T_x$, contradicting $T_x - T'_x = D$; the same holds for $b$. So for each direction whose minimum is below $T_x$ (at least one is, by Lemma 1(2)), say $a < T_x$, we have $a = a' + D$. Let $z$ be a neighbour attaining $a' = T'_z$. Then $a \le T_z \le T'_z + D = a$, so $T_z = a < T_x$ and $T_z - T'_z = D$. Thus $z$ is a maximizer with a smaller value of $T$ than $x$, contradicting the choice of $x$ (if $z$ is a source, $T_z - T'_z = 0 < D$, also a contradiction). Hence $T \le T'$ on $R$, and by symmetry $T = T'$. $\blacksquare$

**Remarks.** (i) The output does not depend on how the heap breaks ties, since it equals the unique solution of (D). (ii) The same solution is the fixed point reached by the fast sweeping method, which is how the tests check the implementation. (iii) Convergence of the solution of (D) to the viscosity solution of $|\nabla T| = s$ as $h \to 0$ is not proved here; it follows from the Barles and Souganidis theorem for monotone, stable and consistent schemes (Rouy and Tourin 1992). The rate $O(h)$ for smooth solutions and $O(h\log(1/h))$ near point sources is observed in the Example of the main page, not proved.
