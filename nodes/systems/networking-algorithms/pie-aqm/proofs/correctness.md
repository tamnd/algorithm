---
title: PIE keeps a valid probability, honours the burst allowance and has integral action
proves: [correctness]
status: full
---

We use the pseudocode of the page. Write $T$ for $T_{update}$, $B$ for MAX_BURST, and $P_k$ and $q_k$ for the values of $drop\_prob$ and $qdelay$ just after the $k$-th call of UPDATE, with $P_0 = 0$ and $q_0 = 0$ at the start. The calls of UPDATE happen at times $u_1 < u_2 < \cdots$ with $u_{k+1} = u_k + T$.

**Lemma 1 (a valid probability).** $0 \le drop\_prob \le 1$ at all times.

*Proof.* It holds at the start. Only lines L8, L9 and L10 change $drop\_prob$, and they run in this order in each UPDATE. Line L10 maps any real number into $[0, 1]$. So after each UPDATE the value is in $[0, 1]$, and ENQUEUE does not change it. $\square$

So line L4 is a valid coin, and a packet that reaches line L4 is dropped with probability exactly $drop\_prob$, independent of the past when the coins are independent.

**Lemma 2 (the burst allowance).** Suppose that line L1 sets $burst\_allowance = B$ at time $t_0$. Then no packet that arrives in the time interval $[t_0, t_0 + B - T)$ is dropped.

*Proof.* A packet is dropped only at line L4, and it reaches line L4 only if $burst\_allowance = 0$ at line L2. Between resets, $burst\_allowance$ changes only at line L11, where it falls by $T$ (and stops at 0). Line L1 can only raise it. The calls of UPDATE after $t_0$ are at $u_j, u_{j+1}, \dots$ with $u_j \ge t_0$ and $u_j < t_0 + T$, since the gap between calls is $T$. After the calls $u_j, \dots, u_{j+m-1}$, the allowance is at least $B - mT$. It can reach 0 only after at least $m = \lceil B/T \rceil$ calls since $t_0$, so not before $u_{j+m-1} \ge u_j + (B/T - 1)T \ge t_0 + B - T$. Every packet that arrives before that time finds a positive allowance at line L2 and is accepted. $\square$

With $B = 150$ ms and $T = 15$ ms, this gives at least 135 ms of arrivals with no drop, and at most 150 ms, since the 10th call of UPDATE after the reset comes before $t_0 + B$.

**Lemma 3 (short queues are never cut).** A packet that arrives when the queue holds at most $2 \cdot$MEAN_PKTSIZE bytes is accepted.

*Proof.* Such a packet is accepted at line L2 or, if it gets past line L2, at line L3, which tests exactly this condition. $\square$

**Lemma 4 (integral action).** Let $a < b$ be update indices such that for every $k$ with $a < k \le b$ we have $P_{k-1} \ge 0.1$, the condition of line L9 is false, and line L10 does not change the value. Then

$$P_b - P_a = \alpha \sum_{k=a+1}^{b} (q_k - q_{ref}) + \beta\,(q_b - q_a).$$

*Proof.* At the $k$-th UPDATE, line L11 of the call before set $qdelay\_old = q_{k-1}$, and line L5 gives $q_k$. Line L6 gives $p = \alpha(q_k - q_{ref}) + \beta(q_k - q_{k-1})$. Since $P_{k-1} \ge 0.1$, none of the conditions of line L7 holds, so $p$ is not changed. By the assumptions, lines L9 and L10 do not change $drop\_prob$, so $P_k = P_{k-1} + \alpha(q_k - q_{ref}) + \beta(q_k - q_{k-1})$. Add these equations for $k = a+1, \dots, b$. The terms $\beta(q_k - q_{k-1})$ telescope to $\beta(q_b - q_a)$. $\square$

**Corollary 5 (the mean delay sample is the target).** Under the assumptions of Lemma 4, let $K = b - a$ and let $0 \le q_k \le Q$ for all $a \le k \le b$. Then

$$\left| \frac{1}{K} \sum_{k=a+1}^{b} q_k - q_{ref} \right| \le \frac{1 + \beta Q}{\alpha K}.$$

*Proof.* By Lemma 1, $|P_b - P_a| \le 1$. Also $|q_b - q_a| \le Q$. Solve the identity of Lemma 4 for the sum and divide by $\alpha K$. $\square$

So over a long run in which the probability stays in $[0.1, 1)$ and the queue never empties for two updates in a row, the mean delay sample tends to $q_{ref}$ as the run grows, for any arrival process. This is the property of the integral part of a PI controller: a steady state is possible only where the mean error is zero. The corollary says nothing about the size of the swings around the mean; that depends on the response of the senders, and the choice of $\alpha$ and $\beta$ by Pan and others rests on a linear model of TCP flows.

For a smaller probability, the same argument holds with each term divided by the divisor $d_k$ that line L7 uses at step $k$. The sum then weights the error of step $k$ by $1/d_k$, so the steps are small while the probability is small, and the integral action is slower.

**Theorem.** PIE always drops with a valid probability (Lemma 1), never drops during the 135 ms after a burst allowance is granted (Lemma 2), never drops when the queue holds at most two mean packets (Lemma 3), and, whenever its probability settles in $[0.1, 1)$, holds the mean sampled delay at $q_{ref}$ with an error that falls like $1/K$ in the number of updates (Lemma 4 and Corollary 5). $\blacksquare$
