---
title: In a one-link round model, BBR's estimates never overshoot, and with exact estimates the gain cycle keeps the queue below a quarter of the BDP
proves: [correctness]
status: full
---

BBR is a heuristic, and these results are about a model, not about BBR on real networks. They show what the parts of the algorithm do when the model holds.

**The model.** One flow uses one link with capacity $c > 0$ packets per second, propagation round-trip time $d > 0$ and a queue $q \ge 0$ packets. Time goes in rounds. A round that starts with queue $q$ lasts $T = d + q/c$. The flow sends at rate $r = \min(\text{pacing\_rate}, \max(\text{cwnd} - q, 0)/d)$, so $rT$ packets arrive. The link serves $s = \min(q + rT, cT)$ packets, the queue becomes $q + rT - s$, and the round gives the samples $\text{rate} = s/T$ and $\text{RTT} = T$. The sender then runs lines L1 to L9 once.

**Lemma 1 (the samples are bounded by the path).** Every rate sample is at most $c$, and every RTT sample is at least $d$ for the $d$ of its round.

*Proof.* $s \le cT$ gives $s/T \le c$. $T = d + q/c \ge d$. $\square$

**Lemma 2 (the estimates never overshoot).** After the first round, $\text{BtlBw} \le c$. If the initial RTprop is at least $d$ and $d$ never goes up, then $\text{RTprop} \ge d$ for the current $d$ at all times.

*Proof.* Line L1 sets BtlBw to the maximum of the last 10 rate samples, and each is at most $c$ by Lemma 1. RTprop is either its initial value or an RTT sample, because line L2 only ever sets it to a sample. A sample is at least the $d$ of its round by Lemma 1, and that $d$ is at least the current one, since $d$ never goes up. $\square$

So BtlBw can only be too small, and RTprop can be too small only after the path got longer. Theorem 2 shows how BBR repairs that case.

**Lemma 3 (the gains).** The STARTUP gain $2/\ln 2$ and the DRAIN gain $\ln 2/2$ multiply to 1. The mean of the PROBE_BW pacing gains $1.25, 0.75, 1, 1, 1, 1, 1, 1$ is 1.

*Proof.* $(2/\ln 2)(\ln 2/2) = 1$, and $1.25 + 0.75 + 6 = 8$. $\square$

**Theorem 1 (the steady cycle).** Let the flow be in PROBE_BW with $\text{BtlBw} = c$ and $\text{RTprop} = d$, so $\text{cwnd} = 2cd$, and let $q = 0$ at the start of the round with gain 1.25. Then over the next 8 rounds:

1. The round with gain 1.25 ends with $q = cd/4$.
2. The round with gain 0.75 lasts $1.25d$, delivers at rate $0.95c$, and ends with $q = 0$.
3. The six rounds with gain 1 each last $d$, deliver at rate $c$, and end with $q = 0$.
4. The cycle delivers $\frac{8.1875}{8.25}\,c > 0.99\,c$ on average, the queue is never above $cd/4$, and BtlBw stays $c$ and RTprop stays $d$.

*Proof.* (1) $T = d$ and $r = \min(1.25c, 2cd/d) = 1.25c$. So $1.25cd$ packets arrive, $s = \min(1.25cd, cd) = cd$, and $q = cd/4$.

(2) $T = d + (cd/4)/c = 1.25d$ and $r = \min(0.75c, (2cd - cd/4)/d) = 0.75c$. So $0.9375cd$ packets arrive, $s = \min(cd/4 + 0.9375cd, 1.25cd) = 1.1875cd$, and the queue becomes 0. The rate sample is $1.1875cd/(1.25d) = 0.95c$.

(3) $q = 0$, so $T = d$, $r = \min(c, 2c) = c$, $s = cd$ and $q$ stays 0.

(4) The cycle lasts $d + 1.25d + 6d = 8.25d$ and delivers $cd + 1.1875cd + 6cd = 8.1875cd$. The window of the max filter is 10 rounds, longer than the cycle, so it always holds a sample equal to $c$ from a round with gain 1, and Lemma 1 bounds the others by $c$. The rounds with gain 1 have $\text{RTT} = d \le \text{RTprop}$, so line L2 refreshes RTprop with $d$. $\blacksquare$

**Theorem 2 (PROBE_RTT after a route change).** Let the flow be in the cycle of Theorem 1, and let $d$ grow to $d' > d$ at time $t_0$. Then line L2 does not refresh RTprop until it expires, so the flow enters PROBE_RTT within $10$ s plus one round after the last refresh before $t_0$, and the first RTT sample after the expiry is at least $d'$, so the new RTprop is at least $d'$.

*Proof.* After $t_0$ every RTT sample is at least $d' > d = \text{RTprop}$ by Lemma 1, so the test $\text{RTT} \le \text{RTprop}$ in line L2 fails. The last refresh was at most one cycle before $t_0$. The first round that ends more than $10$ s after it has an expired stamp, so line L2 takes its sample, which is at least $d'$, and line L6 enters PROBE_RTT. $\blacksquare$

These results do not show that BBR converges from every start, that several BBR flows share a link fairly, or that BBR is fair to loss-based flows. With several flows, each rate sample depends on the others, and the max filter can keep an estimate above the fair share.
