---
title: Round robin gives each ready process a quantum in FIFO turn, with bounded waits between turns
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. Process $i$ has arrival $a_i \ge 0$ and burst $b_i > 0$, the quantum is $q > 0$, and the dispatch cost is $s \ge 0$. Line L1 lists the processes as $P[1], \ldots, P[n]$ in order of $(a_i, i)$.

**Claim 1 (a valid, work-conserving schedule).** The slices that line L8 records do not overlap, each process $i$ runs only at times $\ge a_i$, it gets exactly $b_i$ units of CPU time in slices of length at most $q$, and $C_i$ is the end of its last slice. The CPU is neither running a process nor dispatching one at time $\theta$ only if every process with $a_i \le \theta$ has finished by $\theta$.

*Proof.* We show that this invariant holds at each test of line L3:

> **(I)** (a) the recorded slices do not overlap and all end by $t$; (b) every process in $R$ has arrived by $t$, has $\mathit{left} > 0$, and occurs in $R$ once; (c) the processes $P[1], \ldots, P[k-1]$ are exactly those with $a_i \le t$, and each of them is in $R$ or has finished; (d) for each $i$, $b_i - \mathit{left}[i]$ is the total length of its slices; (e) before $t$, the CPU was idle only at times when every arrived process had finished.

*Initialization.* With $t = 0$, $k = 1$, $R$ empty, no slices and $\mathit{left} = b$, parts (a), (b), (d) and (e) hold at once. Part (c) holds after the first call of line L5, which admits all processes with $a_i \le 0$; we check (c) in the maintenance step in this form: at the test of line L3, $P[1..k-1]$ are exactly the processes with $a_i \le t$, except that processes with $a_i = t$ may wait for line L5.

*Maintenance.* Line L4 runs only if $R$ is empty. By (b) and (c), every arrived process has then finished, and every process not yet admitted has $a_i \ge a_{P[k]}$, so the jump to $a_{P[k]}$ skips only idle time allowed by (e). Line L5 admits the processes with $a_i \le t$ in arrival order, and now $R$ is not empty. Line L6 takes the head $i$. Line L7 adds the dispatch time, during which the CPU is busy with the switch. Line L8 sets $d = \min(q, \mathit{left}[i]) > 0$ and records the slice $[t, t + d)$, which starts at or after every earlier slice end by (a), and at or after $a_i$ by (b). Line L9 advances $t$ and lowers $\mathit{left}[i]$ by $d$, which keeps (d). Line L10 admits the processes that arrived during the slice, so (c) holds for the new $t$. Line L11 puts $i$ back at the tail if it has work left, which keeps (b) since $i$ had been removed at line L6, and otherwise sets $C_i = t$, the end of its last slice.

*Termination.* Each pass of the loop removes one process at line L6. Process $i$ is dispatched at most $\lceil b_i / q \rceil$ times, because each of its slices except the last gives it a full quantum. So the loop runs at most $\sum_i \lceil b_i / q \rceil$ times, and it stops when all processes are admitted and $R$ is empty, that is, when every process has finished. $\square$

**Claim 2 (the wait between turns).** Suppose process $i$ joins the tail of $R$ at time $t_0$, at line L5, L10 or L11, and at that moment $m - 1$ processes are ahead of it in $R$. Then $i$ starts its next slice by time $t_0 + (m - 1)(q + s) + s$. In particular, if $n$ processes are present from time 0 and $s = 0$, each one waits at most $(n - 1)q$ between two consecutive slices, and also before its first slice.

*Proof.* $R$ is a FIFO queue, and processes that join after $t_0$ go behind $i$. So before $i$ is dispatched again, exactly the $m - 1$ processes ahead of it are dispatched, once each. The CPU does not idle while $R$ is not empty (line L4 runs only on an empty queue), and each of these dispatches costs at most $s$ for the switch and at most $q$ for the slice. After them, $i$ is at the head, and its own dispatch costs at most $s$ more. With all $n$ processes present at time 0, at most $n - 1$ others are ever in $R$ with $i$. $\square$

**Claim 3 (the limits in $q$).** (i) If $q \ge \max_i b_i$, every slice is a whole burst, each process runs once, in the order in which it reached the head of $R$, which is the order of $(a_i, i)$; so round robin is [FCFS](/fcfs-scheduling/). (ii) Let all $n$ processes arrive at time 0, let $s = 0$, and let $C^{\mathrm{PS}}_j = \sum_{i} \min(b_i, b_j)$ be the completion time of $j$ under processor sharing. Then $|C_j - C^{\mathrm{PS}}_j| < (n - 1) q$ for each $j$, so $C_j \to C^{\mathrm{PS}}_j$ as $q \to 0$.

*Proof.* (i) If every slice is a whole burst, no process returns to $R$ at line L11, so the processes leave $R$ in the order in which they joined it, which is the order of line L1.

(ii) With all processes present and $s = 0$, the dispatches form rounds: in round $r$, each process with work left runs once, in index order, and receives $\min(q, \text{its remaining work})$. Process $j$ finishes in round $r = \lceil b_j / q \rceil$, so $(r - 1) q < b_j \le r q$. At the moment $C_j$, a process $i$ has received
$\min(b_i, (r - 1) q)$ plus, if $i$ comes before $j$ in the round and is still alive in it, $\min(q, b_i - (r - 1) q)$. We compare this with $\min(b_i, b_j)$, its share in $C^{\mathrm{PS}}_j$.

- For $i = j$, both are $b_j$.
- If $b_i \le (r - 1) q$, both are $b_i$.
- If $b_i \ge b_j$, the round-robin share is $(r - 1)q$ or $\min(b_i, rq)$, and the share under processor sharing is $b_j \in ((r - 1)q, rq]$, so they differ by less than $q$.
- If $(r - 1)q < b_i < b_j$, process $i$ also finishes in round $r$; its round-robin share is $b_i$ if it comes before $j$ and $(r - 1)q$ otherwise, so the two differ by less than $q$.

$C_j$ is the sum of the round-robin shares and $C^{\mathrm{PS}}_j$ is the sum of the shares under processor sharing, and only the $n - 1$ processes $i \ne j$ contribute a difference, each less than $q$ in absolute value. $\square$

**Cost.** Line L1 sorts in $O(n \log n)$ time. Each pass of the loop does $O(1)$ queue work apart from admissions, and each process is admitted once. With Claim 1, the time is $O(n \log n + \sum_i \lceil b_i / q \rceil)$, and the extra space is $O(n)$ for the queue and the remaining work, plus the slices if they are recorded.
