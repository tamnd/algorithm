---
title: Correctness of Brent's cycle detection algorithm
proves: [correctness]
status: full
---

Let $x_0$ be the start value, $x_{i+1} = f(x_i)$, and let $\mu \ge 0$ and $\lambda \ge 1$ be the tail length and the cycle length. We use one fact about eventually periodic sequences.

**Fact.** For $0 \le i < j$, $x_i = x_j$ exactly when $i \ge \mu$ and $\lambda$ divides $j - i$.

*Proof of the fact.* By the definition of $\mu$ and $\lambda$, $x_{\mu + \lambda} = x_\mu$, so $x_{i + \lambda} = x_i$ for all $i \ge \mu$ by applying $f$ repeatedly, and then $x_i = x_j$ when $i \ge \mu$ and $\lambda \mid j - i$. Conversely, let $x_i = x_j$ with $i < j$. Then $x_i$ appears again, so $i \ge \mu$ by the minimality of $\mu$. Write $j - i = q\lambda + r$ with $0 \le r < \lambda$. Since $i \ge \mu$, $x_i = x_{i + q\lambda}$, so $x_{i + q\lambda} = x_{i + q\lambda + r}$. Suppose $r > 0$. Let $s \ge 0$ be such that $m = i + q\lambda + s$ satisfies $m \equiv \mu \pmod{\lambda}$. Applying $f$ $s$ times gives $x_m = x_{m + r}$. Since $m \ge \mu$ and $\lambda$ divides $m - \mu$, $x_m = x_\mu$ and $x_{m + r} = x_{\mu + r}$. So $x_\mu = x_{\mu + r}$ with $0 < r < \lambda$, which contradicts the minimality of $\lambda$. So $r = 0$. $\square$

**The first part (lines L1 to L6).** Number the rounds $k = 0, 1, 2, \ldots$, where round $k$ is the time during which $\text{power} = 2^k$. We claim that during round $k$, at each test of line L3, $t = x_{2^k - 1}$, $h = x_{2^k - 1 + \text{lam}}$ with $1 \le \text{lam} \le 2^k$, where lam is the counter of the pseudocode.

At the first test, after lines L1 and L2, $k = 0$, $t = x_0 = x_{2^0 - 1}$, $h = x_1$ and $\text{lam} = 1$, so the claim holds. Suppose that it holds at a test in round $k$ and the test finds $t \ne h$. If $\text{lam} < 2^k$, line L6 moves $h$ one step and adds 1 to lam, so the claim holds in round $k$ with $\text{lam} + 1 \le 2^k$. If $\text{lam} = 2^k$, then $h = x_{2^{k+1} - 1}$; line L5 sets $t \leftarrow h = x_{2^{k+1} - 1}$, $\text{power} \leftarrow 2^{k+1}$ and $\text{lam} \leftarrow 0$, and line L6 sets $h = x_{2^{k+1}}$ and $\text{lam} = 1$. The claim holds in round $k + 1$.

By the fact, the test of line L3 in round $k$ finds $t = h$ exactly when $2^k - 1 \ge \mu$ and $\lambda$ divides lam. Let $K$ be the least $k$ with $2^k - 1 \ge \mu$ and $2^k \ge \lambda$. In a round $k < K$, either $2^k - 1 < \mu$, and no test succeeds, or $2^k < \lambda$, and no lam in $1, \ldots, 2^k$ is a multiple of $\lambda$, so again no test succeeds. Each such round runs to $\text{lam} = 2^k$ and passes to round $k + 1$. In round $K$, lam takes the values $1, 2, \ldots$ and the first multiple of $\lambda$ is $\lambda$ itself, which is at most $2^K$. So the loop stops in round $K$ with $\text{lam} = \lambda$. In particular the loop terminates.

**The second part (lines L7 to L10).** After lines L7 and L8, $t = x_0$ and $h = x_\lambda$. Each pass of line L10 moves both one step and adds 1 to $\mu$'s counter, so before the test with counter value $m$, $t = x_m$ and $h = x_{m + \lambda}$. By the fact, $x_m = x_{m + \lambda}$ exactly when $m \ge \mu$. So the loop stops at the first $m$ with $m \ge \mu$, which is $m = \mu$. Line L11 returns $(\lambda, \mu)$.

**Evaluation count.** Lines L2 and L6 evaluate $f$ once each time. At the end of the first part $h = x_{2^K - 1 + \lambda}$, and $h$ has moved one step per evaluation from $x_0$, so the first part uses $2^K - 1 + \lambda$ evaluations. By the minimality of $K$, either $K = 0$ or $2^{K-1} < \max(\mu + 1, \lambda)$, so $2^K < 2\max(\mu + 1, \lambda)$ in both cases, since $\max(\mu + 1, \lambda) \ge 1$. The second part uses $\lambda$ evaluations in line L8 and $2\mu$ in line L10. The total is less than $2\max(\mu + 1, \lambda) + 2\lambda + 2\mu$. $\blacksquare$
