---
tag: 9E7NPE
kind: concept
slug: global-virtual-time
name: Global virtual time
aliases:
- GVT
area: distributed/clocks-and-ordering
level: research
summary: The least timestamp of all unprocessed events and all messages in transit in an optimistic simulation. No rollback goes below it, so work before it is final and its saved state can be freed.
prereqs: [time-warp, consistent-cut]
see_also: [time-warp, lai-yang-snapshot, global-snapshot, virtual-time, consistent-cut, termination-detection, parallel-discrete-event-simulation, chandy-misra-bryant]
sources:
  - paper: "David R. Jefferson, Virtual time, ACM Transactions on Programming Languages and Systems 7(3), 1985, pages 404 to 425"
    locator: the definition of global virtual time, the proof that it never decreases, and fossil collection (volume and pages from memory, to be checked)
  - paper: doi:10.1006/jpdc.1993.1075
    title: Friedemann Mattern, Efficient algorithms for distributed snapshots and global virtual time approximation, Journal of Parallel and Distributed Computing 18(4), 1993
    locator: pages 423 to 434 (the two cuts, message colours and counters, and the GVT approximation)
  - paper: "Behrokh Samadi, Distributed simulation, algorithms and performance analysis, PhD thesis, University of California, Los Angeles, 1985"
    locator: a GVT algorithm with acknowledgements for every message (title from memory, to be checked)
  - book: isbn:9780471183839
    title: Richard M. Fujimoto, Parallel and Distributed Simulation Systems, Wiley, 2000
    locator: the chapter on global virtual time (the transient message problem, the simultaneous reporting problem, Samadi's and Mattern's algorithms; ISBN from memory, to be checked)
---

*Global virtual time* (GVT) is the least timestamp of all the work that an optimistic simulation has not finished: the unprocessed events of every logical process and the messages and antimessages in transit. David Jefferson defined it with [Time Warp](/time-warp/) in 1985. No rollback can go below the GVT, so every event before it is final: its saved states can be freed, a step called *fossil collection*, and its output can be committed. No process can see the GVT directly, so it is estimated by a distributed algorithm that must never return a value above it. Mattern's algorithm of 1993 does this with two cuts and message colours, the method of the [Lai-Yang snapshot](/lai-yang-snapshot/).

## In plain words

In an optimistic simulation every process runs ahead and sometimes has to go back. A process can be sent back by a message with an earlier time, or by work that is still waiting somewhere. So the earliest time of all the waiting work and all the messages on the way is a floor: nothing will ever be undone below it.

The hard part is to measure this floor while everything keeps moving. If you ask each process for its earliest time, a message may be on the way between two processes, seen by neither. And the processes answer at different moments, so a process may send an early message just after it answered. A GVT algorithm must catch both cases, so that its answer is never too high. An answer that is a little too low is safe; it only frees memory a little later.

## The idea

**Definition.** At a real time $\tau$, let $LVT_i(\tau)$, the *local virtual time*, be the least timestamp of the unprocessed events of process $i$, with $\infty$ if there are none. Then
$$\mathrm{GVT}(\tau) = \min\Big(\min_i LVT_i(\tau),\ \min\{\mathrm{ts}(m) : m \text{ in transit at } \tau\}\Big).$$

**GVT never decreases.** Every new event, message or antimessage is made by running or undoing an event of timestamp at least the GVT, and has a timestamp at least as large. So the GVT at a later time is at least the GVT now. The proof is in Lemmas 3 and 4 of the correctness proof of [Time Warp](/time-warp/). As a result, no rollback undoes an event below the GVT of any earlier moment, and fossil collection with any lower bound on the GVT is safe.

**Two problems.** A process cannot read $\tau$ or the channels. An estimate built from reports must solve:

- the *transient message problem*: a message that was sent before its sender reported and received after its receiver reported is seen by neither;
- the *simultaneous reporting problem*: the reports are made at different moments, so a message sent after its sender reported, with a small timestamp, may reach a process that has not reported yet, or may be in transit after all reports.

The second problem is the problem of a [consistent cut](/consistent-cut/). The GVT at an instant is a property of a global state, but the reports form a cut, which must count each message on exactly one side.

**Mattern's algorithm.** The processes are *white* until a first cut and *red* after, as in the [Lai-Yang snapshot](/lai-yang-snapshot/); round $r$ uses colour $r - 1$ as white and $r$ as red. Each process counts the white messages it sends to each other process, and keeps $t_{\min}$, the least timestamp of the red messages it has sent in the round.

```pseudo id=main
SEND(i, m)                                      ▷ process i sends a simulation message m
L2  count[colour(i), i, dst(m)] ← count[colour(i), i, dst(m)] + 1; colour(m) ← colour(i)
L3  tmin_i ← min(tmin_i, ts(m))

ROUND(r)                                        ▷ run by a controller
    send CUT1(r) to every process
    on CUT1(r) at process j:
L1      colour(j) ← r; tmin_j ← ∞; report count[r − 1, j, k] for each k
    when all have reported: for each k, W_k ← Σ_j count[r − 1, j, k]; send CUT2(r, W_k) to k
    on CUT2(r, W_k) at process k:
L4      wait until process k has received W_k messages of colour r − 1
L5      report min(LVT_k, tmin_k)
L6  estimate ← the least of the reports
```

Line L1 resets $t_{\min}$, so at line L5 it holds the least timestamp of the red messages that $k$ sent in this round. Line L4 solves the transient message problem: every white message has arrived before its receiver reports. Line L3 solves the simultaneous reporting problem: a red message that a process sent before it reported is in its own report.

**Theorem 1 (the estimate is a lower bound).** Let $E$ be the estimate of a round, and let $\tau$ be any time after the last report of the round. Then $E \le \mathrm{GVT}(\tau)$.

*Proof.* Let $\rho_k$ be the moment at which process $k$ reports, and $c_k$ the moment at which it runs line L1. Every $c_j$ comes before every $\rho_k$, since CUT2 is sent only after all CUT1 reports. Take any event or message $x$ that is unprocessed or in transit at $\tau$. Follow its ancestors back to an initial event: $x_0, x_1, \dots, x_M = x$, where running $x_{a-1}$ made $x_a$. Timestamps increase along this chain. Let $x_a$ be the first one in the chain that its process $k_a$ has not run before $\rho_{k_a}$; there is one, since $x$ itself is not run at $\tau \ge \rho_{k_M}$.

- If $a = 0$, $x_0$ is an initial event of $k_0$, unprocessed at $\rho_{k_0}$, so the report of $k_0$ is at most $\mathrm{ts}(x_0)$.
- Otherwise, $x_{a-1}$ ran at process $i$ before $\rho_i$ and made $x_a$ then. If $x_a$ is an event of $i$ itself, it is unprocessed at $\rho_i$, so $LVT_i(\rho_i) \le \mathrm{ts}(x_a)$. If $x_a$ is a message sent after $c_i$, it is red, and line L3 gives $t_{\min,i} \le \mathrm{ts}(x_a)$ at $\rho_i$. If it is a message sent before $c_i$, it is white and was counted in $W_{k_a}$, so by line L4 it reached $k_a$ before $\rho_{k_a}$; it is not run before $\rho_{k_a}$, so $LVT_{k_a}(\rho_{k_a}) \le \mathrm{ts}(x_a)$.

In every case some report is at most $\mathrm{ts}(x_a) \le \mathrm{ts}(x)$, so $E \le \mathrm{ts}(x)$. $\square$

**Theorem 2 (the estimate is not stale).** $E$ is at least the GVT at the start of the round.

*Proof.* A report is $LVT_k(\rho_k) \ge \mathrm{GVT}(\rho_k)$, or the timestamp of a message that existed during the round, or $\infty$. Both are at least the GVT at the start of the round, since the GVT never decreases. $\square$

The proofs are for the model of the implementation, in which a message with an early timestamp lowers $LVT$ but rollbacks and antimessages are not simulated. In [Time Warp](/time-warp/), a rollback makes run events unprocessed again. We do not give a full proof for that case here. A sketch: the rollback is caused by a message with a timestamp at most that of the events it undoes, and the argument of Theorem 1 applied to that message gives the same bound; Mattern's paper treats the general case. The seeded tests run 40 systems of 2 to 6 processes for 12 rounds each and check, after every step of the simulation, that no unprocessed or in-transit timestamp is below the best estimate so far, and that each estimate is at least the GVT at the start of its round.

## Examples

**Two processes.** At the start of a round, $LVT_0 = 10$, $LVT_1 = 30$, and a white message $m$ with timestamp 11 is in transit from 0 to 1. The GVT is 10.

1. CUT1 reaches both. Process 0 reports one white message sent to 1; process 1 reports none. Both turn red, with $t_{\min} = \infty$ (L1).
2. Process 0 runs its event at 10 and sends a red message with timestamp 14 to process 1, so $t_{\min,0} = 14$ (L3). Its next event is at 25.
3. CUT2 tells process 1 to wait for one white message (L4). When $m$ arrives, $LVT_1 = 11$, and process 1 reports 11. Process 0 reports $\min(25, 14) = 14$ (L5). The estimate is 11 (L6).

**Why line L4 is needed.** Without it, process 1 would report 30, before $m$ arrives. The estimate would be 14, while $m$, with timestamp 11, is still in transit.

**Why line L3 is needed.** Suppose instead that $m$ had arrived and been run before CUT2, so that $LVT_1 = 30$ again, while the red message of timestamp 14 is still in transit. Without $t_{\min}$, the reports would be 25 and 30, and the estimate 25 would be above a message of timestamp 14. With $t_{\min}$ the estimate is 14, which is correct.

## Where it is used

- **Fossil collection in [Time Warp](/time-warp/).** Saved states and processed events below the GVT are freed, and the memory of the simulation stays bounded.
- **Committing output.** Output of events below the GVT can be printed or written, since they will not be undone.
- **Termination.** The simulation has ended when the GVT is $\infty$ or above the end time.
- **Other algorithms.** Samadi's algorithm (1985) acknowledges every message, so that a message in transit is always counted by its sender until it arrives. Mattern's algorithm needs no acknowledgements.
- **Snapshots.** Mattern's algorithm is a [global snapshot](/global-snapshot/) that keeps only one number, the minimum, instead of all the states.

## References
