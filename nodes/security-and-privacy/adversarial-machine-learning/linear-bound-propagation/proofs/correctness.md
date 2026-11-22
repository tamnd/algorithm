---
title: Linear bound propagation gives sound lower bounds, and they are exact when every unit is stable
proves: [correctness]
status: full
---

The network has layers $(W_1, b_1), \dots, (W_K, b_K)$, pre-activations $z_j = W_j a_{j-1} + b_j$, activations $a_j = \mathrm{relu}(z_j)$ for $j < K$, and $a_0 = x$. The box is $B = \{x : l \le x \le u\}$. Inequalities between vectors hold in each coordinate, and arithmetic is exact.

**Lemma 1 (the two lines).** Let $l \le u$ and let RELAX$(l, u) = (s^+, t^+, s^-, t^-)$. For every $z \in [l, u]$,
$$s^- z + t^- \le \max(z, 0) \le s^+ z + t^+.$$

*Proof.* If $u \le 0$, then $\max(z, 0) = 0$ on $[l, u]$ and both lines are $0$. If $l \ge 0$, then $\max(z, 0) = z$ and both lines are $z$. Otherwise $l < 0 < u$. The upper line $g(z) = u(z - l)/(u - l)$ is the chord through $(l, 0)$ and $(u, u)$. The ReLU is convex, so on $[l, u]$ it lies below its chord between the two ends. The lower line is $\alpha z$ with $\alpha \in \{0, 1\}$. For $z \ge 0$, $\alpha z \le z = \max(z, 0)$ since $\alpha \le 1$, and for $z < 0$, $\alpha z \le 0 = \max(z, 0)$ since $\alpha \ge 0$. The same argument works for any $\alpha \in [0, 1]$. $\square$

**Lemma 2 (minimum of a linear function over a box).** For a row vector $g$ and a number $c$, $\min_{x \in B} (g x + c) = c + \sum_t g_t \cdot (l_t \text{ if } g_t \ge 0 \text{ else } u_t)$.

*Proof.* The sum $\sum_t g_t x_t$ has one term per coordinate, and the coordinates range independently over $[l_t, u_t]$. A term with $g_t \ge 0$ is smallest at $x_t = l_t$, and a term with $g_t < 0$ is smallest at $x_t = u_t$. The point that makes every term smallest is in $B$, so it attains the minimum. $\square$

**Theorem 1 (soundness of one backward pass).** Suppose that for every $j < k$ and every $x \in B$, $l_j \le z_j(x) \le u_j$. Then LBP-BACKWARD$(k, \Lambda)$ returns $m$ with $m \le \Lambda z_k(x)$ for every $x \in B$.

*Proof.* Fix $x \in B$ and one row $r$. We show the invariant: at the top of round $j$ of line L2, $\Lambda_r z_k(x) \ge A_r z_j(x) + c_r$, and after line L10 of round $j$, $\Lambda_r z_k(x) \ge A_r a_{j-1}(x) + c_r$.

At the start ($j = k$), line L1 gives $A = \Lambda$ and $c = 0$, so the invariant is an equality. Lines L3 and L4 replace $A$ by $A W_j$ and $c$ by $c + A b_j$. Since $z_j = W_j a_{j-1} + b_j$, the value $A z_j + c$ equals $(A W_j) a_{j-1} + (c + A b_j)$, so the inequality carries over to the form in $a_{j-1}$. If $j = 1$, this is the form in $a_0 = x$, and the loop ends.

If $j > 1$, then $a_{j-1} = \mathrm{relu}(z_{j-1})$ and by hypothesis $z_{j-1}(x) \in [l_{j-1}, u_{j-1}]$. Lines L6 to L10 treat one unit $i$ at a time, and each step changes only column $i$ of $A$ and the constant $c$. Let $(s^+, t^+, s^-, t^-)$ be the lines of unit $i$. If $A_{ri} \ge 0$, Lemma 1 gives $A_{ri}\, a_{j-1,i} \ge A_{ri}(s^- z_{j-1,i} + t^-)$, which is line L9. If $A_{ri} < 0$, multiplying the upper line by a negative number gives $A_{ri}\, a_{j-1,i} \ge A_{ri}(s^+ z_{j-1,i} + t^+)$, which is line L10. In both cases the right side is no larger, so the inequality still holds after the step. After all units, column $i$ multiplies $z_{j-1,i}$ for every $i$, which is the invariant at the top of round $j - 1$.

When the loop ends, $\Lambda_r z_k(x) \ge A_r x + c_r$ for every $x \in B$. Line L11 computes $\min_{x \in B}(A_r x + c_r)$ by Lemma 2, which is at most $A_r x + c_r$ for each $x$. So $m_r \le \Lambda_r z_k(x)$. $\square$

**Theorem 2 (soundness of LBP and of the certificate).** LBP$(l, u, \Lambda)$ returns $m$ with $m \le \Lambda z_K(x)$ for every $x \in B$. If $\Lambda$ has the rows $e_y - e_j$ for $j \ne y$, the box is $B_\infty(x_0, \epsilon) \cap [0,1]^d$, and every entry of $m$ is positive, then $y$ is the only argmax of $z_K(x)$ for every $x$ in the box.

*Proof.* By induction on $k$ in line L13. Assume that the bounds of the layers $1, \dots, k - 1$ are sound (for $k = 1$ there is nothing to assume). Theorem 1 with $\Lambda = I$ gives $l_k \le z_k(x)$, and with $\Lambda = -I$ it gives $-z_k(x) \ge$ LBP-BACKWARD$(k, -I)$, that is $z_k(x) \le u_k$. So the bounds of layer $k$ are sound. After the loop, the hypothesis of Theorem 1 holds for $k = K$, and line L15 gives the claim. For the certificate, $(e_y - e_j) z_K(x) = z_y(x) - z_j(x) \ge m_j > 0$ for every $j \ne y$. $\square$

**Theorem 3 (exact on stable networks).** If $K = 2$ and every unit of the hidden layer has $u_{1,i} \le 0$ or $l_{1,i} \ge 0$, then $m_r = \min_{x \in B} \Lambda_r z_2(x)$.

*Proof.* For $K = 2$, the bounds of line L14 for $k = 1$ come from one affine layer with no ReLU, so they are the exact minimum and maximum of each $z_{1,i}$ over $B$ by Lemma 2. If $u_{1,i} \le 0$, then $a_{1,i} = 0$ on $B$ and both lines are $0$; if $l_{1,i} \ge 0$, then $a_{1,i} = z_{1,i}$ and both lines are the identity. So every step of lines L9 and L10 is an equality for every $x \in B$, and the loop ends with $\Lambda_r z_2(x) = A_r x + c_r$ on $B$. Line L11 is the exact minimum by Lemma 2. $\blacksquare$
