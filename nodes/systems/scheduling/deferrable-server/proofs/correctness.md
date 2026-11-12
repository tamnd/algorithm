---
title: The deferrable server takes at most Cs + ceil((w - Cs)/Ts) Cs of any window of length w
proves: [correctness]
status: full
---

**Setting.** Time is cut into unit slots. One processor runs periodic tasks $\tau_j = (C_j, T_j, D_j)$ with $D_j \le T_j$ and distinct fixed priorities, and one deferrable server with capacity $C_s$, period $T_s$, $1 \le C_s \le T_s$, and a fixed priority $P_s$. Line L2 sets the budget $c$ to $C_s$ at each multiple of $T_s$. Line L4 makes the server ready only when it has a request and $c > 0$, and line L6 lowers $c$ by 1 for each slot that the server runs. Let $E(t, t + w)$ be the number of slots in $[t, t + w)$ in which the server runs.

**Lemma 1 (window bound).** For all $t \ge 0$ and $w \ge 1$,

$$E(t, t + w) \le I_s(w) = C_s + \left\lceil \frac{w - C_s}{T_s} \right\rceil C_s .$$

*Proof.* Cut time into the server periods $P_k = [kT_s, (k+1)T_s)$. The budget that line L2 gives at $kT_s$ can only be used in $P_k$, since line L2 resets it at $(k+1)T_s$, so the server runs in at most $C_s$ slots of each $P_k$. It also runs in at most as many slots of a piece of the window as the piece is long. Let $x = (-t) \bmod T_s$ be the length of the part of the window before the first multiple of $T_s$, and let $q = \lceil (w - x)/T_s \rceil$ be the number of periods that start inside the window. If $q = 0$, the window lies inside one period and $E \le \min(w, C_s) \le I_s(w)$, as the ceiling is at least 0 when $w \ge C_s$ and $E \le w$ otherwise. Let $q \ge 1$, and let $y = w - x - (q - 1)T_s \in (0, T_s]$ be the length of the part in the last period. Then

$$E \le \min(x, C_s) + (q - 1) C_s + \min(y, C_s).$$

*Case $x \ge C_s$.* Then $E \le C_s + q C_s$, and $q \le \lceil (w - C_s)/T_s \rceil$ because $x \ge C_s$.

*Case $x < C_s$ and $x + y > C_s$.* Then $w - C_s = (q - 1)T_s + (x + y - C_s) > (q - 1)T_s$, so $\lceil (w - C_s)/T_s \rceil \ge q$ and $I_s(w) \ge C_s + q C_s > x + (q - 1)C_s + C_s \ge E$.

*Case $x + y \le C_s$.* Then $E \le x + (q - 1)C_s + y \le q C_s$. Also $w - C_s = (q - 1)T_s - (C_s - x - y) \ge (q - 1)T_s - C_s > (q - 2)T_s$, as $C_s \le T_s$ and $x + y > 0$. So $\lceil (w - C_s)/T_s \rceil \ge q - 1$ and $I_s(w) \ge q C_s \ge E$. $\square$

**The bound is reached.** Let the server have the top priority and a full budget, and let a long request arrive at $T_s - C_s$. The server runs in $[T_s - C_s, T_s)$, gets a new budget at $T_s$, and runs in $[T_s, T_s + C_s)$. So $E(T_s - C_s, T_s + C_s) = 2C_s = I_s(2C_s)$. A periodic task with the same $C_s$ and $T_s$ can never take $2C_s$ slots of a window of length $2C_s < T_s + C_s$. This is the double hit.

**Theorem (response time of lower tasks).** Let $\tau_i$ have a priority below $P_s$, and let $R_i$ be the least positive solution of

$$R = C_i + \sum_{j \in hp(i)} \left\lceil \frac{R}{T_j} \right\rceil C_j + I_s(R),$$

where $hp(i)$ is the set of periodic tasks of higher priority. If $R_i \le D_i$, each job of $\tau_i$ ends within $R_i$ of its release. For a task above $P_s$, the same holds with the server term left out.

*Proof.* By induction on the jobs of $\tau_i$ in order of release. Let job $J$ be released at $r$ and end at $f$, and assume that every earlier job of $\tau_i$ ended by its deadline, so by $r$, since $D_i \le T_i$. Call a slot *high* if it runs the server or a job of a task in $hp(i)$. Let $t_0 \le r$ be the smallest time such that each slot of $[t_0, r)$ is high. If $t_0 > 0$, the slot $t_0 - 1$ is not high, so it is idle or runs a job of priority at most that of $\tau_i$; then no job of a task in $hp(i)$ was pending at $t_0 - 1$, as it would have run. So each job of $hp(i)$ that runs in $[t_0, f)$ was released at or after $t_0$.

Assume that $f > t_0 + R_i$. In $[r, t_0 + R_i)$, $J$ is pending, so each slot runs $J$ or high work, and each slot of $[t_0, r)$ is high. So all $R_i$ slots of $[t_0, t_0 + R_i)$ run $J$ or high work. $J$ runs in fewer than $C_i$ of them, as it is not done. A task $\tau_j$ of $hp(i)$ releases at most $\lceil R_i / T_j \rceil$ jobs in $[t_0, t_0 + R_i)$, each of cost at most $C_j$. The server runs in at most $I_s(R_i)$ of them by Lemma 1. So the number of slots is less than $C_i + \sum_{j} \lceil R_i/T_j \rceil C_j + I_s(R_i) = R_i$, which is false. Hence $f \le t_0 + R_i \le r + R_i \le r + D_i$. $\blacksquare$

**Remark.** $I_s(w) = \lceil (w + T_s - C_s)/T_s \rceil C_s$, so the server acts on lower tasks as a periodic task $(C_s, T_s)$ with a release jitter of $T_s - C_s$. The test of the theorem is sufficient, not exact.
