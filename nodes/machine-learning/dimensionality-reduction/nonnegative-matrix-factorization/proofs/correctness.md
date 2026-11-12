---
title: The multiplicative updates keep the factors nonnegative and never increase the loss
proves: [correctness]
status: full
---

We use the pseudocode and notation of the page. $V$ is a nonnegative $m \times n$ matrix, $W$ is $m \times r$, $H$ is $r \times n$, and $F(W, H) = \frac12 \lVert V - W H \rVert_F^2$ (the factor $\frac12$ does not change the minimizers or the monotonicity). Products and quotients marked $\circ$ and $\oslash$ act entry by entry.

**Lemma 1 (nonnegativity and zero patterns).** If $W$ and $H$ are nonnegative before line L3, then after lines L3 and L4 they are nonnegative, an entry that is 0 stays 0, and an entry that is positive stays positive as long as its numerator is positive.

*Proof.* $W^{\top} V$, $W^{\top} W H$, $V H^{\top}$ and $W H H^{\top}$ are products of nonnegative matrices, so they are nonnegative, and each new entry is the old entry times a nonnegative ratio. When a denominator is 0 the implementation keeps the old entry; this happens only when the matching numerator is also 0, for example $(W^{\top} W H)_{a j} = 0$ with $H_{a j} > 0$ forces column $a$ of $W$ to be 0, and then $(W^{\top} V)_{a j} = 0$. $\square$

**Auxiliary functions.** A function $G(h, h')$ is an auxiliary function for $f(h)$ if $G(h, h') \ge f(h)$ for all $h, h'$ and $G(h, h) = f(h)$. If $h^{t+1}$ minimizes $G(\cdot, h^t)$, then
$$ f(h^{t+1}) \le G(h^{t+1}, h^t) \le G(h^t, h^t) = f(h^t) . $$

**Theorem 1 (the H update does not increase $F$).** For fixed $W$, line L3 does not increase $F(W, H)$.

*Proof.* $F$ is a sum over the columns of $H$, and line L3 acts on each column separately, so fix one column $v$ of $V$ and the matching column $h$ of $H$. Put $f(h) = \frac12 \lVert v - W h \rVert^2$ and $P = W^{\top} W$, which has nonnegative entries. Let $S$ be the set of indices with $h^t_a > 0$; by Lemma 1 the update keeps $h_a = 0$ off $S$, so we work on $S$ only and drop the other coordinates. Then $f$ is quadratic with gradient $\nabla f(h^t) = P h^t - W^{\top} v$ and Hessian $P$, and
$$ f(h) = f(h^t) + (h - h^t)^{\top} \nabla f(h^t) + \tfrac12 (h - h^t)^{\top} P (h - h^t) . $$
Let $K$ be diagonal with $K_{a a} = (P h^t)_a / h^t_a$, and
$$ G(h, h^t) = f(h^t) + (h - h^t)^{\top} \nabla f(h^t) + \tfrac12 (h - h^t)^{\top} K (h - h^t) . $$
Then $G(h^t, h^t) = f(h^t)$, and $G(h, h^t) \ge f(h)$ for all $h$ if $K - P$ is positive semidefinite. To show this, put $M_{a b} = h^t_a (K - P)_{a b} h^t_b$; since $h^t_a > 0$ on $S$, $K - P$ is positive semidefinite exactly when $M$ is. For any vector $\nu$,
$$ \nu^{\top} M \nu = \sum_a (P h^t)_a h^t_a \nu_a^2 - \sum_{a, b} h^t_a P_{a b} h^t_b \nu_a \nu_b = \sum_{a, b} P_{a b} h^t_a h^t_b \bigl(\nu_a^2 - \nu_a \nu_b\bigr) = \tfrac12 \sum_{a, b} P_{a b} h^t_a h^t_b (\nu_a - \nu_b)^2 \ge 0 , $$
where the last step averages the middle sum with itself under the swap $a \leftrightarrow b$, and the sign uses $P_{a b} \ge 0$. If $(P h^t)_a = 0$ for some $a \in S$, then column $a$ of $W$ is 0, the coordinate $h_a$ does not affect $f$, and the update keeps it; we drop it as well. On the rest, $K$ is positive definite, so $G(\cdot, h^t)$ has the unique minimizer
$$ h = h^t - K^{-1} \nabla f(h^t) , \qquad h_a = h^t_a - \frac{h^t_a}{(P h^t)_a} \bigl((P h^t)_a - (W^{\top} v)_a\bigr) = h^t_a \frac{(W^{\top} v)_a}{(W^{\top} W h^t)_a} , $$
which is line L3. The auxiliary function argument gives $f(h^{t+1}) \le f(h^t)$. $\square$

**Theorem 2 (the W update does not increase $F$).** For fixed $H$, line L4 does not increase $F(W, H)$.

*Proof.* $\lVert V - W H \rVert_F = \lVert V^{\top} - H^{\top} W^{\top} \rVert_F$. Apply Theorem 1 with $V^{\top}$ in place of $V$, $H^{\top}$ in place of $W$, and $W^{\top}$ in place of $H$. The update of Theorem 1 becomes $W^{\top} \leftarrow W^{\top} \circ (H V^{\top}) \oslash (H H^{\top} W^{\top})$, which is the transpose of line L4. $\square$

**Corollary.** The sequence of losses recorded after each iteration is nonincreasing and bounded below by 0, so it converges. The loop stops after at most $T$ iterations.

The limit need not be a minimum. Lee and Seung's argument shows monotonicity only; a fixed point with $H_{a j} > 0$ satisfies $(W^{\top} V)_{a j} = (W^{\top} W H)_{a j}$, which is the stationarity condition for that entry, but entries that reach 0 need not satisfy the sign condition of the Karush-Kuhn-Tucker system, and the iteration can approach the boundary slowly. Gonzalez and Zhang (2005) and Lin (2007) discuss this and give modified updates with convergence to stationary points.

**Theorem 3 (the Kullback-Leibler updates).** For $D(V \Vert W H) = \sum_{i j} \bigl(V_{i j} \log \frac{V_{i j}}{(W H)_{i j}} - V_{i j} + (W H)_{i j}\bigr)$, the update $H_{a j} \leftarrow H_{a j} \sum_i W_{i a} V_{i j} / (W H)_{i j} \,/\, \sum_i W_{i a}$ does not increase $D$, and the same holds for the matching $W$ update.

*Proof.* Fix a column $j$ and write $v = V_{\cdot j}$, $h = H_{\cdot j}$. The terms of $D$ that depend on $h$ are $f(h) = \sum_i \bigl(\sum_a W_{i a} h_a - v_i \log \sum_a W_{i a} h_a\bigr)$. With weights $\alpha_{i a} = W_{i a} h^t_a / \sum_b W_{i b} h^t_b$, which sum to 1 over $a$, concavity of the logarithm (Jensen's inequality) gives $\log \sum_a W_{i a} h_a \ge \sum_a \alpha_{i a} \log (W_{i a} h_a / \alpha_{i a})$. So
$$ G(h, h^t) = \sum_i \Bigl(\sum_a W_{i a} h_a - v_i \sum_a \alpha_{i a} \log \frac{W_{i a} h_a}{\alpha_{i a}}\Bigr) $$
satisfies $G(h, h^t) \ge f(h)$, with equality at $h = h^t$. $G$ is separable and convex in each $h_a$; setting $\partial G / \partial h_a = \sum_i W_{i a} - \sum_i v_i \alpha_{i a} / h_a = 0$ gives the update. The $W$ update follows by transposition. $\square$

**Cost.** Line L3 computes $W^{\top} V$ in $\Theta(m n r)$, $W^{\top} W$ in $\Theta(m r^2)$ and $(W^{\top} W) H$ in $\Theta(n r^2)$. Line L4 is symmetric. So one iteration costs $\Theta(m n r + (m + n) r^2)$, and $T$ iterations cost $\Theta(T (m n r + (m + n) r^2))$. If $V$ is sparse with $N$ nonzero entries, $W^{\top} V$ and $V H^{\top}$ cost $\Theta(N r)$ instead of $\Theta(m n r)$. The extra memory is $\Theta((m + n) r + r^2)$ besides the input.
