---
title: The NTP offset is within half the round trip delay, and no rule on the same timestamps does better
proves: [correctness]
status: full
---

We use the pseudocode of the page. Over one exchange the clocks do not drift, so the server clock B reads $\theta_0$ more than the client clock A at every moment. The request takes real time $a \ge 0$ and the reply takes $b \ge 0$. The server reads $T_2$ on arrival and $T_3$ when it sends the reply, $h = T_3 - T_2 \ge 0$ later.

**Lemma 1 (the timestamps).** $T_2 - T_1 = \theta_0 + a$ and $T_3 - T_4 = \theta_0 - b$.

*Proof.* The request leaves when A reads $T_1$; at that moment B reads $T_1 + \theta_0$. The request arrives $a$ later, when B reads $T_2 = T_1 + \theta_0 + a$. The reply leaves when B reads $T_3$, so A reads $T_3 - \theta_0$ at that moment, and the reply arrives $b$ later, when A reads $T_4 = T_3 - \theta_0 + b$. $\square$

**Theorem 1 (offset and delay).** Line L1 gives $\theta = \theta_0 + (a - b)/2$, line L2 gives $\delta = a + b$, and $|\theta - \theta_0| \le \delta/2$.

*Proof.* By Lemma 1, $(T_2 - T_1) + (T_3 - T_4) = 2\theta_0 + a - b$, so $\theta = \theta_0 + (a - b)/2$. Also $(T_4 - T_1) - (T_3 - T_2) = (T_2 - T_1) - (T_3 - T_4) = (\theta_0 + a) - (\theta_0 - b) = a + b$. Since $a, b \ge 0$, $|a - b| \le a + b$, so $|\theta - \theta_0| = |a - b|/2 \le (a+b)/2 = \delta/2$. $\square$

The server hold time $h$ does not appear in either result, so a slow server does not make the estimate worse. If $a = b$, $\theta = \theta_0$ exactly.

**Theorem 2 (the bound is optimal).** Let a rule compute an estimate from $T_1, T_2, T_3, T_4$ only, and let it be correct within $e$ for every $\theta_0$ and every $a, b \ge 0$. Then $e \ge \delta/2$.

*Proof.* Fix one run with $\theta_0, a, b$, and let $\delta = a + b$. For a real $s$ with $-b \le s \le a$, consider the run with offset $\theta_0' = \theta_0 + s$, request delay $a' = a - s \ge 0$ and reply delay $b' = b + s \ge 0$, with the same $T_1$ and $h$. By Lemma 1, $T_2' = T_1 + \theta_0' + a' = T_1 + \theta_0 + a = T_2$, so $T_3' = T_3$, and $T_4' = T_3 - \theta_0' + b' = T_3 - \theta_0 + b = T_4$. So the rule sees the same four values and outputs the same estimate $E$ in both runs. The value $s = a$ gives the offset $\theta_0 + a$ and the value $s = -b$ gives $\theta_0 - b$. These two offsets differ by $a + b = \delta$, and $E$ is within $e$ of both, so $2e \ge \delta$. $\square$

**Corollary (the clock filter).** Among the samples in the register, the one with the least $\delta$ has the smallest bound $\delta/2$ by Theorem 1. With drift, older samples also gain error at up to PHI per second, which RFC 5905 adds as dispersion; the code leaves this term out, since its samples are close in time.

**Theorem 3 (selection and combine).** Suppose that the true offset $\theta^\star$ of UTC lies in $[\theta_B - \lambda_B, \theta_B + \lambda_B]$ for every truechimer B, and that SELECT returns $[l, u]$ with $l \le \theta^\star \le u$. Then the combined offset of line L7 satisfies $l \le \Theta \le u$, so $|\Theta - \theta^\star| \le u - l$.

*Proof.* Every survivor of lines L5 and L6 has $\theta_B \in [l, u]$, since line L5 keeps only such servers and line L6 only removes servers. The weights $1/\lambda_B$ are positive, so $\Theta$ is a convex combination of values in $[l, u]$ and lies in $[l, u]$. Both $\Theta$ and $\theta^\star$ lie in $[l, u]$. $\square$

When fewer than half of the servers are falsetickers, SELECT stops at a value of $f$ that is at most their number and returns an interval that holds $\theta^\star$, by the proof on the page on [Marzullo's algorithm](/marzullo-algorithm/). The seeded test of the code checks the whole chain: on 60 runs with five truechimers, some with asymmetric paths, and one falseticker 0.5 s off, the falseticker is always removed, and the combined offset is always within the largest root distance of a truechimer.

**Messages.** Each exchange sends one request and one reply, so polling $m$ servers sends $2m$ messages. $\square$
