---
title: Priority scheduling always runs a ready process of highest priority
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. Process $i$ has arrival $a_i$, burst $b_i > 0$ and priority $\pi_i$, and its key is $\kappa_i = (\pi_i, a_i, i)$ in lexicographic order; a smaller key means a higher priority. Line L1 lists the processes as $P[1], \ldots, P[n]$ in order of $(a_i, i)$. Call a process *ready* at time $\theta$ if $a_i \le \theta$ and it has not finished.

**Claim.** The slices form a valid schedule: they do not overlap, process $i$ runs only after $a_i$, and its slices add up to $b_i$. The CPU is idle only when no process is ready. Moreover:

- *nonpreemptive*: each process runs in one slice, and when a slice starts at time $t$, its process has the least key among the processes ready at $t$;
- *preemptive*: at each time $\theta$ when the CPU runs process $i$, $i$ has the least key among the processes ready at $\theta$.

*Proof.* We show that this invariant holds at each test of line L3:

> **(I)** (a) the slices do not overlap and end by $t$; (b) $H$ holds exactly the processes ready at $t$ that line L5 has admitted, each once, and $P[1..k-1]$ are the admitted ones; (c) $\mathit{left}[i]$ is $b_i$ minus the length of the slices of $i$; (d) before $t$, the CPU was idle only when no process was ready, and the key property of the claim holds for every slice so far.

*Initialization.* With $t = 0$, $k = 1$, $H$ empty and no slices, all parts hold.

*Maintenance.* Line L4 runs only if $H$ is empty; then by (b) no admitted process is ready, and every process not admitted arrives at $a_{P[k]}$ or later, so the CPU is idle on $[t, a_{P[k]})$ with no ready process, as (d) allows. After line L5, $H$ holds exactly the processes ready at $t$, and it is not empty. Line L6 takes the process $i$ of least key among them.

In the nonpreemptive case, line L7 sets $e = t + \mathit{left}[i] = t + b_i$, since $i$ has not run before: a process returns to $H$ at line L9 only in the preemptive case. So $i$ runs in one slice from $t$, with the least key among the ready processes at $t$, and finishes at $e$.

In the preemptive case, line L7 sets $e$ to the earlier of the completion of $i$ and the next arrival $a_{P[k]}$, which is greater than $t$ because line L5 admitted all arrivals up to $t$. On $[t, e)$ no process arrives, so the set of ready processes does not change on $[t, e)$, and $i$ has the least key in it at every moment. If $i$ goes back to $H$ at line L9 and keeps the least key after the next arrivals are admitted, line L6 picks it again and line L8 extends its slice; otherwise the new arrival with a smaller key runs next.

In both cases, line L8 lowers $\mathit{left}[i]$ by the length of the slice and moves $t$ to $e$, which keeps (a) and (c), and line L9 returns $i$ to $H$ exactly when it is still ready at the new $t$, which keeps (b) once line L5 runs again.

*Termination.* In the nonpreemptive case, each pass finishes one process. In the preemptive case, each pass either finishes a process or ends at an arrival time $a_{P[k]}$, after which line L5 admits $P[k]$; so there are at most $n$ passes of each kind, and at most $2n - 1$ slices, since the last pass finishes a process. When $k > n$ and $H$ is empty, every process has been admitted and has finished, and (c) gives that each got exactly $b_i$. $\square$

**Cost.** The sort of line L1 takes $O(n \log n)$ time. There are at most $2n$ passes, and each does $O(1)$ heap operations of $O(\log n)$ time, besides the admissions, which insert each process once. So the time is $O(n \log n)$ and the extra space is $O(n)$.
