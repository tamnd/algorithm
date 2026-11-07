---
title: Algorithm D computes the exact quotient and remainder
proves: [correctness, termination]
status: full
---

Let $\beta \ge 2$, $n \ge 2$ and $m \ge 0$. Let $U = \sum_{i < m+n} u_i\beta^i$ and $V = \sum_{i<n} v_i\beta^i$ with digits in $[0, \beta - 1]$ and $v_{n-1} \ne 0$.

**Theorem.** LONG-DIV$(u, v)$ terminates and returns the digits of $Q = \lfloor U/V \rfloor$ and of $R = U - QV$, with $0 \le R < V$.

The proof has four parts: the normalization, two facts about the trial digit, the step invariant, and the end.

**1. Normalization.** Let $t = v_{n-1}$ and $d = \lfloor \beta / (t + 1) \rfloor \ge 1$. Then $dV$ has $n$ digits and its top digit is at least $\lfloor \beta/2 \rfloor$.

*Proof.* $dV < d(t + 1)\beta^{n-1} \le \beta^n$, so $dV$ has at most $n$ digits, and its top digit is $\lfloor dV / \beta^{n-1} \rfloor \ge dt$. If $t + 1 > \beta / 2$, then $d = 1$ and $dt = t \ge \lfloor \beta/2 \rfloor$. Otherwise $t + 1 \le \beta/2$. Since $d > \beta/(t+1) - 1$, we get $dt > t\beta/(t+1) - t$, and $t\beta/(t+1) - t \ge \beta/2 - 1$ is equivalent to $\beta(t - 1)/(2(t + 1)) \ge t - 1$, which holds for $t = 1$ and, for $t \ge 2$, is $\beta \ge 2(t + 1)$. So the integer $dt$ is larger than $\beta/2 - 1$, hence $dt \ge \lfloor \beta/2 \rfloor$. $\square$

Line L1 replaces $U$ and $V$ by $dU$ (with $m + n + 1$ digits, the top one possibly 0) and $dV$. Since $dU = Q \cdot dV + dR$ with $0 \le dR < dV$, the quotient is unchanged and the new remainder is $dR$. From now on, $U$ and $V$ denote the normalized values, with $v_{n-1} \ge \lfloor \beta/2 \rfloor$.

**2. The trial digit.** Let $W = \sum_{i=0}^{n} w_i\beta^i$ be a number of $n + 1$ digits with $0 \le W < \beta V$, and let $q = \lfloor W/V \rfloor$, so $0 \le q \le \beta - 1$. Let $\hat{q}_0 = \lfloor (w_n\beta + w_{n-1})/v_{n-1} \rfloor$ and $\hat{q} = \min(\hat{q}_0, \beta - 1)$.

*(A) $\hat{q} \ge q$.* If $\hat{q} = \beta - 1$ this holds, since $q \le \beta - 1$. Otherwise $\hat{q} v_{n-1} \ge w_n\beta + w_{n-1} - v_{n-1} + 1$, and

$$W - \hat{q}V \le W - \hat{q}v_{n-1}\beta^{n-1} \le w_n\beta^n + w_{n-1}\beta^{n-1} + (\beta^{n-1} - 1) - (w_n\beta + w_{n-1} - v_{n-1} + 1)\beta^{n-1} = v_{n-1}\beta^{n-1} - 1 < V ,$$

so $W/V < \hat{q} + 1$ and $q \le \hat{q}$. Since $\hat{q}_0 \ge \hat{q}$, also $\hat{q}_0 \ge q$.

*(B) If $v_{n-1} \ge \lfloor \beta/2 \rfloor$, then $\hat{q} \le q + 2$.* If $V = \beta^{n-1}$, then $q = \lfloor W / \beta^{n-1} \rfloor = w_n\beta + w_{n-1} = \hat{q}_0$, and $q \le \beta - 1$ gives $\hat{q} = q$. Otherwise $V > \beta^{n-1}$. Suppose $\hat{q} \ge q + 3$. Then $\hat{q} \le \hat{q}_0 \le (w_n\beta^n + w_{n-1}\beta^{n-1})/(v_{n-1}\beta^{n-1}) \le W/(v_{n-1}\beta^{n-1}) < W/(V - \beta^{n-1})$, using $V < (v_{n-1} + 1)\beta^{n-1}$. Also $q > W/V - 1$. So

$$3 \le \hat{q} - q < \frac{W}{V - \beta^{n-1}} - \frac{W}{V} + 1 = \frac{W}{V} \cdot \frac{\beta^{n-1}}{V - \beta^{n-1}} + 1 ,$$

and $W/V > 2(V - \beta^{n-1})/\beta^{n-1} \ge 2(v_{n-1} - 1)$. Hence $q \ge 2(v_{n-1} - 1)$, and $\beta - 1 \ge \hat{q} \ge q + 3 \ge 2v_{n-1} + 1$, so $v_{n-1} \le \beta/2 - 1 < \lfloor \beta/2 \rfloor$, a contradiction. $\square$

**3. One step.** Fix $j$ and let $W$ be the window $u_j, \ldots, u_{j+n}$ before step $j$, with $0 \le W < \beta V$ (this is shown in part 4). Then step $j$ sets $q_j = q = \lfloor W/V \rfloor$ and leaves the window equal to $W - qV \in [0, V)$.

*Line L3* sets $\hat{q} = \hat{q}_0$ and $\hat{r} = w_n\beta + w_{n-1} - \hat{q}v_{n-1}$, so $0 \le \hat{r} < v_{n-1}$. Each round of line L4 lowers $\hat{q}$ by 1 and raises $\hat{r}$ by $v_{n-1}$, so the relation $\hat{q}v_{n-1} + \hat{r} = w_n\beta + w_{n-1}$ is kept.

*Line L4 keeps $\hat{q} \ge q$.* A round runs only if $\hat{q} \ge \beta$, and then $\hat{q} - 1 \ge \beta - 1 \ge q$; or if $\hat{q}v_{n-2} > \hat{r}\beta + w_{n-2}$. In the second case, adding $\hat{q}v_{n-1}\beta = (w_n\beta + w_{n-1} - \hat{r})\beta$ to both sides gives $\hat{q}(v_{n-1}\beta + v_{n-2}) > w_n\beta^2 + w_{n-1}\beta + w_{n-2}$, so $\hat{q}(v_{n-1}\beta + v_{n-2}) \ge w_n\beta^2 + w_{n-1}\beta + w_{n-2} + 1$, and

$$\hat{q}V \ge \hat{q}(v_{n-1}\beta + v_{n-2})\beta^{n-2} \ge (w_n\beta^2 + w_{n-1}\beta + w_{n-2} + 1)\beta^{n-2} > W .$$

So $q < \hat{q}$ and $\hat{q} - 1 \ge q$. With (A) at the start, $\hat{q} \ge q$ holds throughout.

*Line L4 terminates.* $\hat{q}$ decreases by 1 in each round and stays $\ge q \ge 0$, so there are at most $\hat{q}_0 - q$ rounds. With the normalization, $\hat{q}_0 \le (v_{n-1}\beta + \beta - 1)/v_{n-1} < \beta + 2$ (using $w_n \le v_{n-1}$, which follows from $W < \beta V < (v_{n-1} + 1)\beta^n$), and (B) gives $q \ge \min(\hat{q}_0, \beta - 1) - 2$, so the number of rounds is at most 4.

*After line L4, $\hat{q} \le q + 1$ and $\hat{q} < \beta$.* When the loop stops, either $\hat{r} \ge \beta$ or ($\hat{q} < \beta$ and $\hat{q}v_{n-2} \le \hat{r}\beta + w_{n-2}$). In the first case, $\hat{q} < \beta$ as well: if $\hat{q} \ge \beta$, then $\hat{r} = w_n\beta + w_{n-1} - \hat{q}v_{n-1} \le v_{n-1}\beta + \beta - 1 - \beta v_{n-1} < \beta$. And then $\hat{q}v_{n-2} \le (\beta - 1)^2 < \beta^2 \le \hat{r}\beta + w_{n-2}$. So in both cases $\hat{q} < \beta$ and $\hat{q}v_{n-2} \le \hat{r}\beta + w_{n-2}$, which as above gives $\hat{q}(v_{n-1}\beta + v_{n-2}) \le w_n\beta^2 + w_{n-1}\beta + w_{n-2}$. Write $V = (v_{n-1}\beta + v_{n-2})\beta^{n-2} + V_0$ with $0 \le V_0 < \beta^{n-2}$. Then

$$W - \hat{q}V \ge (w_n\beta^2 + w_{n-1}\beta + w_{n-2})\beta^{n-2} - \hat{q}(v_{n-1}\beta + v_{n-2})\beta^{n-2} - \hat{q}V_0 \ge -\hat{q}V_0 > -\beta \cdot \beta^{n-2} \ge -V ,$$

so $W - (\hat{q} - 1)V > 0$, which gives $q \ge \hat{q} - 1$.

*Lines L5 to L7.* Line L5 computes $W - \hat{q}V$ in $n + 1$ digits with a borrow. If $\hat{q} = q$, then $W - \hat{q}V \in [0, V)$ is not negative, line L6 does nothing, and $q_j = q$. If $\hat{q} = q + 1$, then $W - \hat{q}V = (W - qV) - V \in [-V, 0)$ is negative; the digits hold $W - \hat{q}V + \beta^{n+1}$ with a borrow out, and line L6 adds $V$ and drops the carry, which leaves $W - qV$, and sets $q_j = \hat{q} - 1 = q$. In both cases the window ends as $W - qV \in [0, V)$, and $q_j = q \in [0, \beta - 1]$ is a digit.

**4. The loop invariant and the end.** Let $U^{(j)}$ be the number held in $u_0, \ldots, u_{m+n}$ before step $j$, for $j = m, m-1, \ldots, 0$, and $U^{(-1)}$ the number after step 0. The invariant before step $j$ is

$$U = \Big( \sum_{i > j} q_i \beta^i \Big) V + U^{(j)}, \qquad 0 \le U^{(j)} < \beta^{j+1} V .$$

Before step $m$, $U^{(m)} = U$ and no quotient digit is set. The unnormalized dividend is below $\beta^{m+n}$, so $U < d\beta^{m+n}$, and the unnormalized divisor is at least $\beta^{n-1}$, so $\beta^{m+1}V \ge \beta^{m+1} d\beta^{n-1} = d\beta^{m+n}$. Hence $U^{(m)} < \beta^{m+1}V$. The digits of $U^{(j)}$ below position $j$ are not touched by step $j$, and $U^{(j)} < \beta^{j+1}V$ means that the window $W = \lfloor U^{(j)}/\beta^j \rfloor$ satisfies $W < \beta V$. Step $j$ replaces $W$ by $W - q_jV$ with $q_j = \lfloor W/V \rfloor$ (part 3), so $U^{(j-1)} = U^{(j)} - q_j\beta^jV$ and $0 \le U^{(j-1)} < \beta^j V$, since $U^{(j-1)} = (W - q_jV)\beta^j + (U^{(j)} \bmod \beta^j) \le (V - 1)\beta^j + \beta^j - 1 < \beta^j V$. This is the invariant for $j - 1$.

After step 0, $U = (\sum_{i \ge 0} q_i\beta^i)V + U^{(-1)}$ with $0 \le U^{(-1)} < V$, so $\sum_i q_i\beta^i = \lfloor U/V \rfloor = Q$ and $U^{(-1)}$ is the normalized remainder $dR$. Since $U^{(-1)} < V < \beta^n$, it lies in $u_0, \ldots, u_{n-1}$. It is divisible by $d$, so the short division of line L8 is exact and returns $R$. The loop of line L2 has $m + 1$ steps and each step terminates (part 3), so the algorithm terminates. $\blacksquare$
