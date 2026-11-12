---
title: In the fluid model, the Vegas Diff is the backlog of the flow, and every fixed point fills the link with a queue of n alpha to n beta packets
proves: [correctness]
status: full
---

**The model.** One link serves $c > 0$ packets per time unit. Flows $1, \ldots, n$ have propagation round-trip times $d_i > 0$ and windows $w_i \ge 2$ packets. The queueing delay $q \ge 0$ is $0$ if $\sum_i w_i / d_i \le c$, and otherwise it is the unique $q > 0$ with $\sum_i w_i/(d_i + q) = c$. It is unique because the sum falls strictly in $q$ and goes to $0$. Flow $i$ sends at rate $x_i = w_i/(d_i + q)$. In each round every flow measures $\text{RTT}_i = d_i + q$ and runs lines L2 to L8 once, with $0 < \alpha \le \beta$.

**Lemma 1 (no overload).** $\sum_i x_i \le c$, with equality when $q > 0$.

*Proof.* If $q = 0$ then $\sum_i x_i = \sum_i w_i/d_i \le c$. If $q > 0$, equality is the definition of $q$. $\square$

**Lemma 2 (Diff is the backlog).** If $\text{BaseRTT}_i = d_i$, then line L5 gives

$$\text{Diff}_i = \left(\frac{w_i}{d_i} - \frac{w_i}{d_i + q}\right) d_i = \frac{w_i\, q}{d_i + q} = x_i\, q.$$

The FIFO queue holds $c q$ packets in total (when $q > 0$, a packet waits $q$ while the link serves $c$ per time unit), and flow $i$ has the share $x_i / c$ of the arrivals, so it has $x_i q$ packets in the queue. So $\text{Diff}_i$ is the number of packets of flow $i$ in the queue.

*Proof.* The first equality is line L5 with lines L3 and L4. The rest is algebra with $x_i = w_i/(d_i + q)$. $\square$

**Lemma 3 (BaseRTT).** After the first round, $\text{BaseRTT}_i = \min$ of the measured round-trip times, so $\text{BaseRTT}_i \ge d_i$. It is $d_i$ once flow $i$ has seen a round with $q = 0$.

*Proof.* Line L2 keeps the minimum of the values $d_i + q \ge d_i$. $\square$

**Theorem 1 (the fixed points).** Let $\text{BaseRTT}_i = d_i$ for all $i$. The windows do not change in a round if and only if, for every $i$, either $\alpha \le x_i q \le \beta$, or $w_i = 2$ and $x_i q > \beta$. At such a fixed point:

1. $q > 0$, so the link is fully used: $\sum_i x_i = c$.
2. If no window is at the floor 2 with $x_i q > \beta$, the queue holds between $n\alpha$ and $n\beta$ packets: $n\alpha \le cq \le n\beta$.
3. Any two flows $i$ and $j$ with $\alpha \le x q \le \beta$ have $\alpha/\beta \le x_i/x_j \le \beta/\alpha$. If $\alpha = \beta$, all such flows have the same rate $\alpha/q$, whatever their round-trip times.

*Proof.* By Lemma 2, line L6 adds 1 exactly when $x_i q < \alpha$, and line L7 takes 1 away exactly when $x_i q > \beta$ and $w_i > 2$. That gives the first claim.

(1) If $q = 0$ then $x_i q = 0 < \alpha$ for every $i$, so line L6 raises every window, and this is not a fixed point. So $q > 0$, and Lemma 1 gives $\sum_i x_i = c$.

(2) Sum $\alpha \le x_i q \le \beta$ over $i$, and use $\sum_i x_i q = c q$ from (1).

(3) From $\alpha \le x_i q \le \beta$ and $\alpha \le x_j q \le \beta$, divide the two bounds. With $\alpha = \beta$ both rates equal $\alpha/q$. $\blacksquare$

**Theorem 2 (a utility view).** Let $\alpha = \beta$, all BaseRTT exact, and no window at the floor. Then the fixed-point rates are the unique solution of

$$\max_{x \ge 0} \sum_{i=1}^{n} \alpha \log x_i \quad\text{subject to}\quad \sum_i x_i \le c,$$

and $q$ is the Lagrange multiplier of the capacity constraint.

*Proof.* The objective is strictly concave and the constraint is linear, so the KKT conditions are necessary and sufficient, and the maximizer is unique. They are: $\alpha / x_i = \lambda$ for all $i$, $\lambda \ge 0$, and $\lambda(c - \sum_i x_i) = 0$. Theorem 1 gives $x_i q = \alpha$ and $\sum_i x_i = c$, so $\lambda = q$ satisfies all of them. $\blacksquare$

This is the single-link case of the result of Low, Peterson and Wang: queueing delay plays the role of the price, and Vegas reaches a weighted proportionally fair allocation.

**Theorem 3 (no fixed point at an empty link).** From any windows with $q = 0$, every window grows by 1 per round until $q > 0$, which takes at most $\lceil c \max_i d_i \rceil$ rounds.

*Proof.* While $q = 0$ each measured round-trip time is $d_i$, so $\text{Diff}_i = 0 < \alpha$ and line L6 runs for each flow. After $r$ rounds, $\sum_i w_i/d_i \ge r/\max_i d_i$, which is above $c$ once $r > c \max_i d_i$. $\blacksquare$

These results describe the fixed points and do not prove that the windows reach one from every start. A wrong BaseRTT breaks Lemma 2: a flow that starts while a queue is present measures $\text{BaseRTT}_i = d_i + q_0$ with $q_0 > 0$, and then $\text{Diff}_i$ is smaller than its backlog.
