---
title: The bully algorithm elects the largest live process, with n² − 1 messages in the worst case
proves: [correctness, termination, complexity]
status: full
---

**Model.** Processes $1, \ldots, n$, all known to all, fully connected. A message sent at time $t$ to a live process arrives at time $t + \delta$; a message to a crashed process is lost. A process handles the messages that arrive at time $t$ before it checks its timers at time $t$. $T_{\mathrm{ok}} = 2\delta$ and $T_{\mathrm{coord}} = 3\delta$. Consider an interval in which no process crashes or recovers, and let $L$ be the set of live processes and $h = \max L$. Let $S \ne \emptyset$ be the processes that run line L1 at time $t_0$ and are not already electing, and $s = \min S$. Suppose no process is electing before $t_0$.

**Claim.** Every process in $L$ ends with $\mathit{coord} = h$. Each process in $L \cap [s, n]$ starts exactly one election and no other process starts one. The run sends exactly $\sum_{u \in L, u \ge s} (n - u)$ ELECTION messages, $|\{(u, v) : u < v,\ u, v \in L,\ u \ge s\}|$ OK messages and $h - 1$ COORDINATOR messages. With $s = 1$ this is $n^2 - 1$ if $L = \{1, \ldots, n\}$, and $n^2 - n - 1$ if $L = \{1, \ldots, n-1\}$.

**Lemma 1 (who starts, and when).** Every $u \in L$ with $u \ge s$ starts an election at $t_0$ or at $t_0 + \delta$, and at no other time before the announcement. No $u < s$ starts.

*Proof.* $s$ sends ELECTION to every $v > s$ at $t_0$, so every live $v > s$ that has not started gets it at $t_0 + \delta$ and starts by line L4. A process starts only by line L1 (only at $t_0$), by line L4 (needs an ELECTION from a smaller process, and only processes $\ge s$ send them), by line L8 (needs a COORDINATOR from a smaller process, and only $h$ sends one, see Lemma 2), or by line L9 (excluded by Lemma 3). A process below $s$ receives no ELECTION. $\square$

**Lemma 2 (only $h$ announces).** Every $u \in L$ with $s \le u < h$ receives an OK before its $T_{\mathrm{ok}}$ runs out, and $h$ runs line L7 at a time $t_h \le t_0 + 3\delta$.

*Proof.* If $u$ starts at time $t_u$, it sends ELECTION to $h$, and $h$ answers at $t_u + \delta$; the OK arrives at $t_u + 2\delta$, before the timer check at that time. So $u$ never runs line L6. Process $h$ starts at $t_h - 2\delta \in \{t_0, t_0 + \delta\}$ by Lemma 1, sends ELECTION only to crashed processes, gets no OK, and runs line L6 and then L7 at $t_h$. $\square$

**Lemma 3 (no restart).** No process runs line L9.

*Proof.* A process $u$ that receives an OK at time $t$ started at $t - 2\delta$, and its ELECTION reached $h$ at $t - \delta \ge t_0$. So $h$ started by $t - \delta$, and $t_h \le t + \delta$ by Lemma 2. The COORDINATOR message reaches $u$ at $t_h + \delta \le t + 2\delta < t + T_{\mathrm{coord}}$. $\square$

**Lemma 4 (no second announcement).** After $t_h$, process $h$ receives no ELECTION.

*Proof.* By Lemma 1 every ELECTION is sent at $t_0$ or $t_0 + \delta$, and arrives by $t_0 + 2\delta \le t_h$. Messages that arrive at $t_h$ are handled before the timer of $h$, while $h$ is still electing. $\square$

**Outputs.** By Lemma 2, $h$ sends COORDINATOR$(h)$ to every $v < h$, and every live $v$ sets $\mathit{coord} = h$ by line L8; no larger process exists to bully $h$. The run ends at $t_h + \delta \le t_0 + 4\delta$.

**Counting.** By Lemmas 1 and 4, each $u \in L$ with $u \ge s$ runs line L2 once and sends $n - u$ ELECTION messages, to live and crashed processes. Each ELECTION from $u$ to a live $v$ gets one OK (line L4). Only $h$ runs line L7, once, with $h - 1$ messages. With $s = 1$:

- if $L = \{1, \ldots, n\}$: $\sum_{u=1}^{n}(n-u) + \binom{n}{2} + (n - 1) = n(n-1) + n - 1 = n^2 - 1$;
- if $L = \{1, \ldots, n - 1\}$: $\sum_{u=1}^{n-1}(n-u) + \binom{n-1}{2} + (n - 2) = \frac{n(n-1)}{2} + \frac{(n-1)(n-2)}{2} + n - 2 = n^2 - n - 1$.

The counts grow as $s$ goes down, so $s = 1$ gives the most messages. If $s = n - 1 = h$, the run sends $1 + (n - 2) = n - 1$ messages.

**Crashes during the election.** If a process crashes after it sent an OK, the processes that wait on it run line L9 and start again, and the lemmas apply to the last election after the last crash or recovery. A recovered process starts an election by line L1, and the same lemmas apply with $S$ the recovered process. So after the last failure event every live process has $\mathit{coord} = \max L$. $\blacksquare$
