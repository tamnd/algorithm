---
title: Linial's colour reduction is proper, reaches O(Delta^2) colours in log* N + O(1) rounds, and ends with Delta + 1 colours
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $G = (V, E)$ is a simple graph with maximum degree at most $\Delta \ge 1$. A family $S_0, \dots, S_{m-1}$ of subsets of a ground set $U$ is $\Delta$-cover-free if $S_x \not\subseteq S_{y_1} \cup \dots \cup S_{y_\Delta}$ for every $x$ and all indices $y_1, \dots, y_\Delta$ different from $x$. $\lg$ is $\log_2$.

**Lemma 1 (one round).** Let $c$ be a proper colouring of $G$ with colours in $[0, m)$, and let $S_0, \dots, S_{m-1} \subseteq U$ be $\Delta$-cover-free with $U$ totally ordered. Let $c'(v)$ be the least element of $S_{c(v)} \setminus \bigcup_{u \in N(v)} S_{c(u)}$. Then $c'$ is well defined and is a proper colouring with colours in $U$.

*Proof.* The node $v$ has at most $\Delta$ neighbours, and their colours differ from $c(v)$ because $c$ is proper. By the cover-free property, the set $S_{c(v)} \setminus \bigcup_{u \in N(v)} S_{c(u)}$ is not empty, so $c'(v)$ exists. Let $\{u, v\} \in E$. Then $c'(v) \in S_{c(v)}$, and $c'(u) \notin S_{c(v)}$ because $v$ is a neighbour of $u$. So $c'(u) \ne c'(v)$. $\square$

**Lemma 2 (polynomial family).** Let $q$ be a prime, $d \ge 1$, $q^{d+1} \ge m$ and $q > \Delta d$. For $x \in [0, m)$, let $p_x(a) = \sum_{j=0}^{d} x_j a^j$ over $\mathrm{GF}(q)$, where $x_j$ is digit $j$ of $x$ in base $q$, and let $S_x = \{(a, p_x(a)) : a \in \mathrm{GF}(q)\}$. Then the family is $\Delta$-cover-free in $U = \mathrm{GF}(q)^2$, which has $q^2$ elements.

*Proof.* Since $x < q^{d+1}$, $x$ has at most $d + 1$ digits, and different $x$ give different polynomials. For $x \ne y$, the polynomial $p_x - p_y$ is not zero and has degree at most $d$, so it has at most $d$ roots, and $|S_x \cap S_y| \le d$. Then $\Delta$ sets other than $S_x$ meet $S_x$ in at most $\Delta d < q = |S_x|$ points, so they do not cover $S_x$. $\square$

**Lemma 3 (existence of a family with $O(\Delta^2 \log m)$ points).** For $m \ge 2$, a $\Delta$-cover-free family of $m$ subsets of $[0, k)$ exists with $k = \lfloor e (\Delta + 1)^2 \ln m \rfloor + 1$.

*Proof.* Put each $j \in [0, k)$ into each $S_x$ independently with probability $p = 1/(\Delta + 1)$. Fix $x$ and a set $Y$ of $\Delta$ indices other than $x$. A fixed $j$ lies in $S_x$ and in no $S_y$ with $y \in Y$ with probability $p(1 - p)^{\Delta} \ge p / e$, because $(1 - 1/(\Delta + 1))^{\Delta} \ge 1/e$. The $k$ points are independent, so $\Pr[S_x \subseteq \bigcup_{y \in Y} S_y] \le (1 - p/e)^k < e^{-k p / e}$. There are at most $m \cdot m^{\Delta} = m^{\Delta + 1}$ choices of $x$ and $Y$. By the [union bound](/union-bound/), the family fails with probability less than $m^{\Delta + 1} e^{-k/(e(\Delta + 1))}$, which is at most 1 when $k \ge e (\Delta + 1)^2 \ln m$. So some family is cover-free. $\square$

**Lemma 4 (bounds on one step of the schedule).** In a step the algorithm uses the pair $(q, d)$ with $q$ prime, $q > \Delta d$ and $q^{d+1} \ge m$ that has the least $q$, and it makes the step only when $q^2 < m$. So the new number of colours $m' = q^2$ is at most $q_0^2$ for any other pair $(q_0, d_0)$ with these properties. Two such pairs:

- (a) If $m \ge 3$, take $d_0 = \lceil \lg m \rceil - 1 \ge 1$ and $q_0$ the least prime above $\Delta d_0$. By Bertrand's postulate $q_0 \le 2 \Delta d_0$, and $q_0^{d_0 + 1} \ge 2^{\lceil \lg m \rceil} \ge m$. So $m' \le 4 \Delta^2 (\lg m)^2$.
- (b) If $m \le (c \Delta)^{c+1}$ for an integer $c \ge 1$, take $d_0 = c$ and $q_0$ the least prime above $c \Delta$. Then $q_0^{c+1} > (c\Delta)^{c+1} \ge m$ and $q_0 \le 2c\Delta$, so $m' \le 4 c^2 \Delta^2$.

**Theorem 1 (correctness and termination).** The algorithm stops and returns a proper colouring with colours in $\{0, \dots, \Delta\}$.

*Proof.* The identifiers are a proper colouring with colours in $[0, N)$. Each step of the loop is the round of Lemma 1 with the family of Lemma 2, so the colouring stays proper, and its colours lie in $[0, q^2)$ with the encoding $(a, y) \mapsto aq + y$. The loop runs only while $q^2 < m$, so $m$ drops by at least 1 per step and the loop stops. In the final rounds, the nodes of colour $x$ are pairwise non-adjacent, so they change at the same time without conflict. Each has at most $\Delta$ neighbours, so a colour in $\{0, \dots, \Delta\}$ is free; the colouring stays proper and the colour $x$ disappears. After $x = m - 1, \dots, \Delta + 1$, only the colours $0, \dots, \Delta$ remain. $\square$

**Theorem 2 (rounds).** Let $p$ be the least prime with $p > 2\Delta$. The loop runs $\log^* N + O(1)$ times, with an absolute constant in the $O(1)$, and ends with at most $\max(p^2, 216)$ colours. By Bertrand's postulate $p < 4\Delta$, so this is $O(\Delta^2)$. The final rounds take fewer than $\max(p^2, 216)$ more rounds.

*Proof.* Let $\ell_t = \lg m_t$ and $A = 2 + 2 \lg \Delta$. By Lemma 4(a), every step with $m_t \ge 3$ gives $\ell_{t+1} \le A + 2 \lg \ell_t$.

*Phase 1: while $\lg \ell_t \ge A$ and $\ell_t > 24$.* Then $\ell_{t+1} \le 3 \lg \ell_t$. With $\operatorname{tower}(0) = 1$ and $\operatorname{tower}(k+1) = 2^{\operatorname{tower}(k)}$: if $k \ge 3$ and $x \le 6 \operatorname{tower}(k)$, then $3 \lg x \le 3 \lg 6 + 3 \operatorname{tower}(k - 1) \le 6 \operatorname{tower}(k - 1)$, because $3 \lg 6 < 8 \le 3 \operatorname{tower}(k-1)$ when $\operatorname{tower}(k - 1) \ge 4$. Let $K = \log^* N$, so $\ell_0 = \lg N \le \operatorname{tower}(K - 1)$. Each step of Phase 1 lowers the level $k$ by one, so after at most $K$ steps either $\ell_t \le 6 \operatorname{tower}(2) = 24$ or Phase 1 has ended. So Phase 1 has at most $\log^* N$ steps.

*Phase 2: one step.* Now $\ell_t \le \max(2^A, 24)$, so $\lg \ell_t \le \max(A, 5)$ and $\ell_{t+1} \le A + 2\max(A, 5) \le 3A + 10$. So $m_{t+1} \le 2^{3A + 10} = 2^{16} \Delta^6$.

*Phase 3: one step.* Since $2^{16} \Delta^6 \le (6\Delta)^7$, Lemma 4(b) with $c = 6$ gives $m \le 144 \Delta^2$ after one more step.

*Phase 4.* If $\Delta \ge 18$, then $144 \Delta^2 \le 8 \Delta^3 < (2\Delta + 1)^3$. When $m \le (2\Delta + 1)^3$, the pair $(p, 2)$ is valid, and every valid pair with $d \ge 2$ has a prime $q > 2\Delta$, so $q \ge p$. A pair with $d = 1$ has $q^2 \ge m$. So the next step, if any, gives exactly $p^2$, and from $m = p^2$ no step improves, since every candidate has $q \ge p$. So Phase 4 has at most 1 step. If $\Delta < 18$, then $m \le 144 \cdot 17^2$ and $m$ drops by at least 1 per step, so Phase 4 has an absolute constant number of steps.

*The final count.* Suppose the loop stops at $m$. If $m \le (2\Delta + 1)^3$, the argument of Phase 4 shows $m \le p^2$. If $m > (2\Delta + 1)^3 \ge 27$, let $x = \lceil m^{1/3} \rceil \ge 4$. If also $m > 216$, then $x \ge 7$; Bertrand's postulate gives a prime $q$ with $x \le q \le 2x - 1$, the pair $(q, 2)$ is valid because $q > 2\Delta$ and $q^3 \ge m$, and $q^2 \le (2x - 1)^2 < (x - 1)^3 < m$, so the loop does not stop. Hence $m \le \max(p^2, 216)$. The last phase removes one class per round. $\blacksquare$
