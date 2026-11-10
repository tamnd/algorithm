---
title: With null messages and lookahead at least 1, every station runs its events in key order and the run does not stop before time T
proves: [correctness]
status: full
---

We use the model and the pseudocode of the page: FIFO links, integer timestamps, lookahead $L \ge 1$, end time $T$, and stations that are deterministic. An arrival at station $i$ has the key $(\mathrm{ts}, \text{source}, \text{job})$. The start jobs sit on a special input link $-1$ with bound $\infty$. For station $i$, let
$$T_{\mathrm{in}}(i) = \min_j \begin{cases} \mathrm{ts}(\text{head of queue } j) & \text{if queue } j \text{ is not empty,} \\ \mathit{bound}_j & \text{otherwise.} \end{cases}$$

**Lemma 1 (each link is in timestamp order).** The jobs that station $i$ sends on one link have strictly increasing timestamps.

*Proof.* Successive departures of $i$ are $\mathit{dep}' = \max(a, \mathit{dep}) + s > \mathit{dep}$, since $s \ge L \ge 1$. $\square$

**Lemma 2 (the bounds are true).** At every moment, for every station $i$ and input link $j$: (a) every job on link $j$ that $i$ has not yet received has timestamp at least $\mathit{bound}_j$; (b) every arrival that $i$ has not yet run, queued or not yet received, has timestamp at least $T_{\mathrm{in}}(i)$; (c) when $i$ sends null($v$) on a link, every job that $i$ sends later on that link has timestamp at least $v$.

*Proof.* By induction over the steps of the run. Part (b) follows from (a) at the same moment: queued jobs on link $j$ are at least the head by Lemma 1, and jobs not yet received on link $j$ come after the queued ones by FIFO order, so they are larger still if the queue is not empty, and at least $\mathit{bound}_j$ by (a) if it is empty.

For (c), let $i$ send null($v$) with $v = \min(\max(T_{\mathrm{in}}(i), \mathit{last}) + L,\ T + 1)$. A later departure of $i$ serves some arrival $a$ that $i$ has not yet run, so $\mathrm{ts}(a) \ge T_{\mathrm{in}}(i)$ by (b), and it leaves at $\max(\mathrm{ts}(a), \mathit{last}') + s$ with $\mathit{last}' \ge \mathit{last}$ and $s \ge L$. So it is at least $\max(T_{\mathrm{in}}(i), \mathit{last}) + L \ge v$.

For (a): the bound changes only at line L6 and in the job branch of RECEIVE. At line L6, the new bound is the old bound or $v$; jobs received later on the link were sent after the null, by FIFO order, so they are at least $v$ by (c). In the job branch, the new bound is $\mathrm{ts} + 1$; later jobs on the link are larger than $\mathrm{ts}$ by Lemma 1, and timestamps are integers. $\square$

**Theorem 1 (safety).** Each station runs its arrivals in increasing order of key.

*Proof.* Let line L3 run $h$, after line L2 passed. Take any arrival $x$ that $i$ has not yet run. If $x$ is queued on a link with a non-empty queue, its key is at least the head of that queue by Lemma 1, and the head is at least $h$ by line L1. If $x$ is on a link $j$ whose queue is empty, then $\mathrm{ts}(x) \ge \mathit{bound}_j$ by Lemma 2(a), and line L2 passed, so $(\mathit{bound}_j, j) \ge (\mathrm{ts}(h), \mathrm{source}(h))$. Equality would mean $j = \mathrm{source}(h)$, whose queue holds $h$; so the inequality is strict on these two entries, and $x$ has a larger key than $h$. If $x$ is queued on the link of $h$, it comes after $h$ and is larger by Lemma 1. So $h$ has the least key of all arrivals that $i$ will ever still run. $\square$

By Theorem 1 and the theorem of the page on [parallel discrete event simulation](/parallel-discrete-event-simulation/), the events that the stations run, and their states, are those of the sequential simulation, as far as the run goes.

**Lemma 3 (the run comes to rest).** The run sends finitely many messages.

*Proof.* Each job leaves a station at a time larger than its arrival time, and it is sent only if the departure is at most $T$, so each of the finitely many jobs makes finitely many visits. Nulls on one link have strictly increasing integer values, by the test of line L5, and at most $T + 1$, so there are finitely many. $\square$

**Theorem 2 (no deadlock).** When the run comes to rest, with no message in transit and no station able to run or send, every arrival with timestamp at most $T$ has been run.

*Proof.* At rest, each station $i$ ran STEP and sent nothing, so for each output link $k$ the last null that $i$ sent on $k$ has a value of at least $v_i = \min(\max(T_{\mathrm{in}}(i), \mathit{last}_i) + L,\ T + 1)$. That null was delivered. If no job came after it on the link, the bound at the other end is at least its value by line L6. If a job came after it, the bound is that job's timestamp plus one, and the job's timestamp is at least the null value by Lemma 2(c). So the bound of link $i \to k$ at $k$ is at least $v_i$.

Let $\tau$ be the least $T_{\mathrm{in}}$ over all stations, and suppose that $\tau \le T$. Then $v_i \ge \min(\tau + L, T + 1) > \tau$ for every $i$, so every empty input link of every station has a bound larger than $\tau$. Let station $i$ have $T_{\mathrm{in}}(i) = \tau$. The value $\tau$ is not the bound of an empty link, so it is the timestamp of a queued head, and the queued message $h$ with the least key has $\mathrm{ts}(h) = \tau \le T$. Every empty link $j$ has $\mathit{bound}_j > \tau = \mathrm{ts}(h)$, so line L2 passes, and station $i$ can run $h$, which contradicts rest. So $\tau > T$, and by Lemma 2(b) no arrival at time $T$ or earlier is left. $\square$

**Remark (the role of $L \ge 1$).** With $L = 0$, the value $v_i$ can equal $\tau$, the strict inequality in Theorem 2 fails, and the example of the page with $L = 0$ deadlocks even with null messages; a test checks this.
