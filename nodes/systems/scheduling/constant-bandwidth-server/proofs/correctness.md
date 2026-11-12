---
title: Under EDF, constant bandwidth servers with total bandwidth at most 1 never make a hard task miss
proves: [correctness]
status: full
---

**Setting.** Time is cut into unit slots on one processor. Hard tasks $\tau_i = (C_i, T_i)$ release jobs with a deadline one period after the release. Each constant bandwidth server has a budget $Q$, a period $T$ and the bandwidth $U = Q / T$, and serves its own soft jobs first come, first served, with any arrival times and any demands. A server has a budget $c$ and a deadline $d$, both 0 at the start. When a soft job arrives at time $a$ and finds the queue of its server empty (line L3), the server checks $c \ge (d - a)U$ (line L4). If this is true, it sets $d \leftarrow a + T$ and $c \leftarrow Q$ (line L5, a *new* event); if not, it keeps $c$ and $d$. Line L7 takes one unit of $c$ for each slot the server runs, and line L8 sets $c \leftarrow Q$ and $d \leftarrow d + T$ when $c$ reaches 0 (a *recharge*). Line L6 runs the ready entity with the earliest deadline; a server is ready when its queue is not empty, and its deadline is $d$. Let $W(x, y)$ be the number of slots in $[x, y)$ in which a given server runs.

**Lemma 1 (deadlines never decrease).** At all times $0 \le c \le Q$, and no event makes $d$ smaller.

*Proof.* Line L7 takes a unit only from $c > 0$, and line L8 refills $c$ in the same slot in which it reaches 0. The other lines set $c$ to $Q$ or keep it. A recharge adds $T$ to $d$. A new event at $a$ happens only if $c \ge (d - a)U$. If $d - a > T$, then $(d - a)U > TU = Q \ge c$, so no new event happens. So at a new event $d \le a + T$, and the new deadline $a + T$ is not smaller. $\square$

**Lemma 2 (budget invariant).** Let an arrival at time $r$ find the queue of a server empty. From the end of the arrival step at $r$ onwards, at every point of the run,

$$\Phi = W(r, \cdot) + c - (d - r)U \le 0 .$$

*Proof.* At $r$, if line L5 makes a new event, then $W = 0$, $c = Q$ and $d - r = T$, so $\Phi = 0$. Otherwise $c < (d - r)U$ and $W = 0$, so $\Phi < 0$. Each later step keeps $\Phi \le 0$:

- Line L7 adds 1 to $W$ and takes 1 from $c$, so $\Phi$ does not change.
- A recharge adds $Q$ to $c$ and $T$ to $d$, and $Q - TU = 0$, so $\Phi$ does not change.
- An arrival that finds the queue busy, or that finds it empty and keeps $c$ and $d$, changes nothing.
- A new event at a later time $a$. Just before it, $\Phi \le 0$ gives $W(r, a) + c \le (d - r)U$, and the test of line L4 gives $c \ge (d - a)U$. Subtracting, $W(r, a) \le (a - r)U$. After it, $\Phi = W(r, a) + Q - (a + T - r)U = W(r, a) - (a - r)U \le 0$. $\square$

With $r$ the first arrival, Lemma 2 gives the invariant $W(0, t) + c \le dU$ that the implementation checks after each slot.

**Lemma 3 (server demand).** Let $t_1 < t_2$. Assume that if $t_1 > 0$, the server in slot $t_1 - 1$ is not ready or is ready with a deadline above $t_2$, and that in each slot of $[t_1, t_2)$ in which the server runs, its deadline is at most $t_2$. Then $W(t_1, t_2) \le (t_2 - t_1)U$.

*Proof.* If the server was ready in slot $t_1 - 1$ with a deadline above $t_2$, then its queue stays non-empty until the server serves it, so no new event can happen before it runs, and by Lemma 1 its deadline stays above $t_2$. So it does not run in $[t_1, t_2)$, and $W = 0$. Otherwise its queue is empty at $t_1$, and the server runs again only after an arrival at some time $r \ge t_1$ that finds the queue empty, so $W(t_1, r) = 0$. If the server does not run in $[r, t_2)$, we are done. Else let $e$ be the last slot of $[t_1, t_2)$ in which it runs, and let $d_e \le t_2$ be its deadline in that slot. Apply Lemma 2 just after line L7 of slot $e$ and before line L8 can change $d$:

$$W(t_1, t_2) = W(r, e + 1) \le (d_e - r)U - c \le (t_2 - t_1)U,$$

as $c \ge 0$, $d_e \le t_2$ and $r \ge t_1$. $\square$

**Theorem (isolation).** If $\sum_i C_i / T_i + \sum_S U_S \le 1$, no hard job misses its deadline, whatever the soft jobs do.

*Proof.* Assume that a hard job misses, and let $J$ be a hard job that misses with the earliest deadline $t_2$, so no hard job is late before $t_2$. Then $J$ is ready in slot $t_2 - 1$, so line L6 runs an entity with deadline at most $t_2$ there. Let $t_1 < t_2$ be the smallest time such that each slot of $[t_1, t_2)$ runs an entity whose deadline is at most $t_2$. If $t_1 > 0$, slot $t_1 - 1$ is idle or runs an entity with deadline above $t_2$. As line L6 picks the earliest deadline, every entity that is ready in slot $t_1 - 1$ has a deadline above $t_2$.

*Hard work.* A hard job that runs in $[t_1, t_2)$ has a deadline at most $t_2$. If it was released before $t_1$, it was ready in slot $t_1 - 1$ with a deadline at most $t_2$, which is false. So it is released at or after $t_1$, and $\tau_i$ has at most $\lfloor (t_2 - t_1)/T_i \rfloor$ such jobs, with total work at most $(t_2 - t_1) C_i / T_i$.

*Server work.* Each server meets the assumptions of Lemma 3 for $t_1$ and $t_2$, so it runs in at most $(t_2 - t_1)U_S$ slots of $[t_1, t_2)$.

All $t_2 - t_1$ slots of $[t_1, t_2)$ run hard jobs or servers, and $J$, which is one of the hard jobs counted, still has work left at $t_2$. So

$$t_2 - t_1 < (t_2 - t_1)\Big(\sum_i \frac{C_i}{T_i} + \sum_S U_S\Big) \le t_2 - t_1,$$

which is false. $\blacksquare$

**Remark.** The theorem does not use the behaviour of the soft jobs, so a server that is overloaded only delays its own jobs. The condition is the EDF utilization test for the hard tasks together with periodic tasks $(Q, T)$ in the place of the servers. Abeni and Buttazzo also show that a hard task $(C, T)$ served by its own server with $Q \ge C$ and period $T$ meets all its deadlines; the implementation tests this case.
