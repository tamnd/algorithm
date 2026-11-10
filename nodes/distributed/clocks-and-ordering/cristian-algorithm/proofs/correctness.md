---
title: The estimate of Cristian's algorithm is within h minus the minimum delay of the server clock
proves: [correctness]
status: full
---

We use the pseudocode of the page and its model. The server clock $S$ is correct, so $S(t) = t$. The client clock $C$ is $\rho$-bounded with $0 \le \rho < 1$: for all real times $a \le b$, $(1-\rho)(b-a) \le C(b) - C(a) \le (1+\rho)(b-a)$. Each one-way delay is at least $d_{\min}$.

Fix one attempt. Let $s$ be the real time of line L1 (the request leaves), $r$ the real time at which the server reads its clock, and $t$ the real time of line L2 (the reply arrives). Then $T_0 = C(s)$, $T = r$ and $T_1 = C(t)$. Let $\tau = t - s$ be the real round trip time, and let $h = (T_1 - T_0)/(2(1-\rho))$ as in line L3.

**Lemma 1.** $\tau \le 2h$.

*Proof.* By the drift bound, $T_1 - T_0 = C(t) - C(s) \ge (1-\rho)(t - s) = (1-\rho)\tau$. Divide by $1 - \rho > 0$: $\tau \le (T_1 - T_0)/(1-\rho) = 2h$. $\square$

**Lemma 2.** $d_{\min} \le t - r \le \tau - d_{\min}$.

*Proof.* The request leaves at $s$ and reaches the server no earlier than $s + d_{\min}$. The server reads its clock after the request arrives, so $r \ge s + d_{\min}$. The reply leaves after the reading and takes at least $d_{\min}$, so $t \ge r + d_{\min}$. The second fact gives $t - r \ge d_{\min}$. The first gives $t - r \le t - s - d_{\min} = \tau - d_{\min}$. $\square$

**Theorem.** The estimate $E = T + h$ of line L4 satisfies $|E - S(t)| \le h - d_{\min}$.

*Proof.* $E - S(t) = r + h - t = h - (t - r)$. By Lemma 2, $h - (\tau - d_{\min}) \le E - S(t) \le h - d_{\min}$. By Lemma 1, $\tau \le 2h$, so $h - \tau + d_{\min} \ge h - 2h + d_{\min} = -(h - d_{\min})$. Both sides together give $|E - S(t)| \le h - d_{\min}$. $\square$

In particular $h \ge d_{\min}$ always holds, since $2h \ge \tau \ge 2 d_{\min}$ by Lemmas 1 and 2.

**Tightness.** Let $\rho = 0$, let the request take exactly $d_{\min}$, and let the server read its clock and reply at once, with a reply delay of $x \ge d_{\min}$. Then $\tau = d_{\min} + x = 2h$ and $t - r = x = \tau - d_{\min}$, so $E - S(t) = h - \tau + d_{\min} = -(h - d_{\min})$. The mirror case, with a reply delay of exactly $d_{\min}$, gives $+(h - d_{\min})$. So no better bound holds for the estimate $T + h$, and the client cannot tell these two runs apart from a run with symmetric delays, since all three give the same $T_0$, $T$ and $T_1$ up to its own offset.

**The retry rule.** Line L6 accepts an attempt only when $T_1 - T_0 \le 2U(1-\rho)$, that is when $h \le U$. By the theorem, an accepted reading has error at most $U - d_{\min}$. If each attempt is accepted with probability $p > 0$, independently, then $k$ attempts all fail with probability $(1-p)^k$, which tends to 0, and the expected number of attempts is $\sum_{k \ge 1} k p (1-p)^{k-1} = 1/p$.

**Setting the clock.** Line L6 sets $C$ to $E$ at real time $t$, so right after the attempt the client clock is within $U - d_{\min}$ of $S$. Afterwards the error grows by at most $\rho$ per second of real time, by the drift bound (see the page on clock drift). $\square$
