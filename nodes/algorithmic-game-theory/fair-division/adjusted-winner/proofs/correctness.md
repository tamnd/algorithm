---
title: Adjusted winner is equitable, Pareto optimal and envy-free, with at most one split good
proves: [correctness]
status: full
---

**Setting.** There are $m$ goods and two agents. The points $p_A(g), p_B(g)$ are nonnegative, and $\sum_g p_A(g) = \sum_g p_B(g) = 100$. A share vector gives agent $A$ the share $s_g \in [0, 1]$ of good $g$ and agent $B$ the share $1 - s_g$. We write $U_A(s) = \sum_g p_A(g) s_g$ and $U_B(s) = \sum_g p_B(g)(1 - s_g)$, so $U_A(s) + U_A(1 - s) = 100$, where $1 - s$ is the share of $B$. We refer to the lines L1 to L9 of the page. After line L4, $W$ is the agent with more points and $L$ the other, and $x_g$ is the share of $W$ in good $g$. The running totals $T_W, T_L$ always equal the points of $W$ and $L$ for their current shares.

**Lemma 1 (the goods of each agent after line L1).** Every good $g$ held by $W$ after line L1 has $p_W(g) \ge p_L(g)$, and every good held by $L$ has $p_L(g) \ge p_W(g)$. A good held by $W$ with $p_W(g) = 0$ has $p_L(g) = 0$.

*Proof.* Line L1 gives $g$ to the agent with more points on it, and ties to $A$. So the holder has at least as many points as the other agent. If the holder has 0 points, so does the other agent. $\square$

So the goods left out of $G$ in line L5 are worth 0 to both agents, and every ratio $p_W(g)/p_L(g)$ of a good of $G$ is at least 1.

**Lemma 2 (the loop ends with equal points at a good with $p_L > 0$).** Suppose line L3 does not return, so $T_W > T_L$ when the loop of line L6 starts. Then the loop reaches a good $g$ with $p_L(g) > 0$ at which either line L7 makes $T_W = T_L$ or line L8 runs, and in both cases $T_W = T_L$ after that good, and the loop stops. Before that good, $T_W > T_L$ holds after each move.

*Proof.* A move of line L7 is made only if $T_W - p_W(g) \ge T_L + p_L(g)$, so it keeps $T_W \ge T_L$; if it gives equality, the loop stops. If line L7 does not apply, then $T_W - T_L < p_W(g) + p_L(g)$, and since $T_W > T_L$, the share $\alpha = (T_W - T_L)/(p_W(g) + p_L(g))$ lies strictly between 0 and 1. After the move, $T_W - \alpha p_W(g) = T_L + \alpha p_L(g)$, so the totals are equal.

Suppose that the loop moves every good of $G$ with $p_L(g) > 0$ whole and still has $T_W > T_L$. By Lemma 1, $L$ now holds all goods with $p_L(g) > 0$, so $T_L = 100 \ge T_W$, a contradiction. So the loop stops at the latest at the last good of $G$ with $p_L(g) > 0$. The goods with $p_L(g) = 0$ come after all others in the order of line L5, so the loop stops before it reaches them. $\square$

**Theorem 1 (equitable, with at most one split good).** The output has $U_A = U_B$, and at most one good has a share strictly between 0 and 1.

*Proof.* If line L3 returns, the totals are equal and no good is split. Otherwise Lemma 2 gives $T_W = T_L$ at the end. Line L1 gives whole goods, line L7 moves whole goods, and line L8 runs at most once, because the loop stops after it. So at most one good is split. $\square$

**Theorem 2 (Pareto optimal).** No share vector $s'$ has $U_A(s') \ge U_A(s)$ and $U_B(s') \ge U_B(s)$ with one of the two strict, where $s$ is the output.

*Proof.* Let $r = 1$ if line L3 returns. Otherwise let $r = p_W(g^*)/p_L(g^*)$ for the good $g^*$ at which the loop stops; by Lemma 2, $p_L(g^*) > 0$, so $r$ is finite, and $r \ge 1$ by Lemma 1. (If line L3 returns, take $W = A$ and $L = B$.) We claim that at the end

- every good with $x_g > 0$ has $p_W(g) \ge r\, p_L(g)$, and
- every good with $x_g < 1$ has $p_W(g) \le r\, p_L(g)$.

A good with $x_g > 0$ is a good of $W$ after line L1 that was not moved whole. It is either $g^*$, with $p_W = r p_L$; or a good of $G$ after $g^*$ in the order, with ratio at least $r$; or a good outside $G$, with $p_W = p_L = 0$. A good with $x_g < 1$ is either a good of $L$ after line L1, which has $p_W(g) \le p_L(g) \le r\, p_L(g)$ by Lemma 1 and $r \ge 1$; or a good of $G$ that was moved in whole or in part, which comes no later than $g^*$ and has ratio at most $r$. If line L3 returns, the same holds with $r = 1$ by Lemma 1 alone.

Now let $\Phi(y) = U_W(y) + r\, U_L(y) = \sum_g \big(p_W(g)\, y_g + r\, p_L(g)(1 - y_g)\big)$, where $y_g$ is the share of $W$. Each term is linear in $y_g$, with slope $p_W(g) - r\, p_L(g)$. By the claim, $x_g = 1$ when the slope is positive, unless $g$ is split, and the split good $g^*$ has slope 0; and $x_g = 0$ when the slope is negative. So $x$ maximizes every term and $\Phi(x) \ge \Phi(y)$ for every $y$. If $y$ were at least as good as $x$ for both agents and better for one, then $\Phi(y) > \Phi(x)$ because $r > 0$, a contradiction. $\square$

**Theorem 3 (envy-free).** Each agent values its own share at least as much as the share of the other agent.

*Proof.* Let $T = U_A(s) = U_B(s)$ by Theorem 1. Agent $A$ values the share of $B$ at $100 - T$, and agent $B$ values the share of $A$ at $100 - T$. If $T < 50$, the swapped vector $s' = 1 - s$ gives each agent $100 - T > T$, which contradicts Theorem 2. So $T \ge 50 \ge 100 - T$. $\square$

**Corollary (the value is unique).** All equitable Pareto optimal share vectors give the same number of points $T$. If two of them gave $T_1 < T_2$, the second would give both agents more than the first, so the first would not be Pareto optimal. Hence the output of the procedure is the equitable point of the Pareto frontier.

**Running time.** Lines L1 to L4 take $O(m)$ operations, the sort of line L5 takes $O(m \log m)$, and the loop takes $O(m)$, because each good is visited at most once. $\blacksquare$
