---
title: Lagrange-Gauss reduction returns a basis of the same lattice whose vectors reach the two minima, after a logarithmic number of iterations
proves: [correctness, termination, time.worst]
status: full
---

**Setting.** The input is two linearly independent vectors $b_1, b_2 \in \mathbb{Q}^m$. We write $L$ for the lattice they generate, $\langle \cdot, \cdot \rangle$ for the inner product and $N(v) = \langle v, v \rangle$. The nearest integer $\lceil x \rfloor = \lfloor x + 1/2 \rfloor$ satisfies $|x - \lceil x \rfloor| \le 1/2$. We call a pair $(u, v)$ **reduced** if $N(u) \le N(v)$ and $2 |\langle u, v \rangle| \le N(u)$.

**Lemma 1 (the pair stays a basis).** At every moment, $(u, v)$, the current values of the two variables, is a basis of $L$.

*Proof.* At the start $(u, v)$ is $(b_1, b_2)$ or $(b_2, b_1)$. Line L4 replaces $v$ by $v - q u$ with $q \in \mathbb{Z}$, which is the unimodular matrix $\begin{pmatrix} 1 & 0 \\ -q & 1 \end{pmatrix}$ applied to the pair, and lines L1 and L6 apply $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$. Both matrices are integer with determinant $\pm 1$, so the new pair generates the same lattice and is again independent. $\square$

In particular $u \ne 0$ at line L3, so the division is defined.

**Lemma 2 (the output is reduced).** When line L5 returns, $(u, v)$ is reduced.

*Proof.* Let $u$ and $v$ be the values before line L4, and $\mu = \langle u, v \rangle / N(u)$, $q = \lceil \mu \rfloor$. After line L4, $\langle u, v - q u \rangle / N(u) = \mu - q$, which has absolute value at most $1/2$. Line L5 returns only if $N(v - q u) \ge N(u)$. These are the two conditions. $\square$

**Lemma 3 (a reduced pair reaches the minima).** If $(u, v)$ is a reduced basis of $L$, then $N(u) = \lambda_1(L)^2$ and $N(v) = \lambda_2(L)^2$.

*Proof.* Let $w = x u + y v$ with integers $(x, y) \ne (0, 0)$. Then
$$N(w) = x^2 N(u) + 2 x y \langle u, v \rangle + y^2 N(v) \ge x^2 N(u) - |x y| N(u) + y^2 N(v) = (x^2 - |xy| + y^2) N(u) + y^2 (N(v) - N(u)),$$
using $2 |\langle u, v \rangle| \le N(u)$. For integers not both zero, $x^2 - |xy| + y^2 \ge 1$: if $|x| \ge |y|$, then $x^2 - |xy| + y^2 = |x|(|x| - |y|) + y^2$, which is a positive integer unless $x = y = 0$; the other case is symmetric. The last term is at least 0 because $N(v) \ge N(u)$. Hence $N(w) \ge N(u)$, so $u$ is a shortest nonzero vector and $N(u) = \lambda_1^2$.

For $\lambda_2$: a vector $w$ independent of $u$ has $y \ne 0$, so $y^2 (N(v) - N(u)) \ge N(v) - N(u)$, and $N(w) \ge N(u) + N(v) - N(u) = N(v)$. Any two independent lattice vectors include one that is independent of $u$, so the longer of them has squared norm at least $N(v)$; and the pair $(u, v)$ itself reaches $N(v)$. So $N(v) = \lambda_2^2$. $\square$

**Lemma 4 (the norms fall geometrically).** Number the iterations of the loop of line L2 by $k = 1, 2, \ldots, T$, and let $r_k = N(u)$ at the start of iteration $k$. Then $r_1 > r_2 > \cdots > r_T$, and for every iteration $k$ with $2 \le k < T$,
$$r_{k+1} < r_{k-1} / 3.$$

*Proof.* An iteration that does not return ends at line L6 with the new $u$ equal to $v - qu$, and $N(v - qu) < N(u)$ by line L5. So $r_{k+1} < r_k$.

Fix $k$ with $2 \le k < T$, and let $u, v$ be the values at the start of iteration $k$, with $r = N(u) = r_k$ and $s = N(v) = r_{k-1}$, so $s > r$. The vector $u$ was produced by line L4 of iteration $k - 1$ as the reduction of the old $v$ against the old $u$, which is now $v$; by the computation in Lemma 2, $c = \langle u, v \rangle$ satisfies $|c| \le s/2$. Let $q = \lceil c / r \rfloor$ and $t = N(v - q u) = s - 2 q c + q^2 r$. Iteration $k$ does not return, so $t < r$.

- If $q = 0$, then $t = s > r$, a contradiction.
- If $q = 1$, then $c / r \ge 1/2 > 0$, and $t = s - 2c + r \ge s - s + r = r$, a contradiction. The case $q = -1$ is the same with $-c$.

So $|q| \ge 2$. Write $c / r = q + e$ with $|e| \le 1/2$; then $q c = (q^2 + q e) r \ge (q^2 - |q|/2) r$, and
$$t = s - 2 q c + q^2 r \le s - (2 q^2 - |q|) r + q^2 r = s - (q^2 - |q|) r \le s - 2 r.$$
Thus $t < r$ and $t \le s - 2r$. If $r \le s/3$ then $t < r \le s/3$; otherwise $t \le s - 2r < s/3$. In both cases $r_{k+1} = t < s/3 = r_{k-1}/3$. $\square$

**Theorem.** On linearly independent $b_1, b_2 \in \mathbb{Q}^m$, the algorithm terminates after
$$T \le 2 + 2 \log_3 \frac{\min(N(b_1), N(b_2))}{\lambda_1(L)^2}$$
iterations, and returns a basis $(u, v)$ of $L$ with $\|u\| = \lambda_1(L)$, $\|v\| = \lambda_2(L)$ and $|\langle u, v \rangle| \le \|u\|^2 / 2$.

*Proof.* First, termination. The values $r_k$ are squared norms of nonzero lattice vectors (Lemma 1), so $r_k \ge \lambda_1^2 > 0$. If the loop ran for at least $2j + 1$ iterations with $j \ge 1$, Lemma 4 applied to $k = 2, 4, \ldots, 2j$ gives $r_{2j+1} < r_1 / 3^j$. Since also $r_{2j+1} \ge \lambda_1^2$, we get $3^j < r_1 / \lambda_1^2$. So the number of such $j$ is finite and the loop ends. With $j = \lfloor (T - 1)/2 \rfloor$ this reads $T \le 2j + 2 < 2 + 2 \log_3(r_1 / \lambda_1^2)$ when $T \ge 3$, and the bound holds trivially when $T \le 2$. Line L1 makes $r_1 = \min(N(b_1), N(b_2))$.

The output is a basis of $L$ by Lemma 1, reduced by Lemma 2, and reaches the two minima by Lemma 3. $\blacksquare$

**Cost.** Each iteration does three inner products and one vector update, $O(m)$ arithmetic operations. For an integer input with entries of absolute value below $2^\beta$, $\lambda_1 \ge 1$ and $r_1 \le m\, 2^{2\beta}$, so $T = O(\beta + \log m)$. Every vector that appears has squared norm at most $\max(N(b_1), N(b_2)) + r_1 / 4$: the returned $v$ has $N(v) \le N(v_{\text{old}}^*) + N(u)/4$ where $v_{\text{old}}^*$ is the component orthogonal to $u$, and all other vectors are shorter than an earlier one. So all numbers have $O(\beta + \log m)$ binary digits, and with schoolbook multiplication the total is $O(m (\beta + \log m)^3)$ bit operations.
