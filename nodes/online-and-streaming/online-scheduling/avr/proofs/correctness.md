---
title: AVR computes its speed profile and meets every deadline
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The jobs are $(r_j, w_j, d_j)$ with $w_j > 0$ and $r_j < d_j$, and $\delta_j = w_j / (d_j - r_j)$. The AVR speed is $s(t) = \sum_{j : r_j \le t < d_j} \delta_j$.

## Part 1. The sweep outputs the AVR speed profile

Let $e_1 \le e_2 \le \dots \le e_{2n}$ be the sorted event times. On an open interval between two consecutive distinct event times, no window opens or closes, so $s(t)$ is constant there.

**Invariant.** When the loop of line L4 reaches the first event with time $t$, the variable $s$ equals $\sum_j \delta_j$ over the jobs with $r_j < t$ and $d_j \ge t$, that is, over the windows that contain the open interval just before $t$.

At the first event, no event was processed and $s = 0$, so the invariant holds. Suppose that it holds at time $t$, and let $t'$ be the next distinct event time. Line L6 processes all the events at time $t$: it adds $\delta_j$ for each window that opens at $t$ and subtracts $\delta_j$ for each window that closes at $t$. After that, $s$ is the sum over the windows with $r_j \le t$ and $d_j > t$. These are exactly the windows that contain $(t, t')$, since no event lies strictly between $t$ and $t'$. So when the loop reaches $t'$, the invariant holds, and line L5 outputs the piece $[t, t')$ with the speed $s$, which is $s(\tau)$ for all $\tau \in [t, t')$. Pieces with speed 0 are not output; on them no window is open.

**Termination.** The loop of line L4 visits each of the $2n$ events once, and each step does a constant amount of work. So it stops after $2n$ steps. $\square$

## Part 2. EDF at the AVR speeds meets every deadline

**Step 1. A feasible schedule exists at these speeds.** Consider the schedule $S^*$ that, at each time $t$, gives each job $j$ with $r_j \le t < d_j$ the rate $\delta_j$. The total rate is $s(t)$, so $S^*$ uses exactly the AVR speed. Job $j$ gets $\delta_j (d_j - r_j) = w_j$ units of work inside its window. So $S^*$ is feasible. It shares the processor among several jobs; this is the limit of fast switching and is a valid preemptive schedule in this model.

**Step 2. Change of the time scale.** Let $W(t) = \int_0^t s(\tau) \, d\tau$, the work that the processor can do by time $t$. It is continuous and does not decrease. A schedule at the speeds $s(t)$ is the same as a schedule at speed 1 in the work scale $x = W(t)$, where job $j$ has release $W(r_j)$ and deadline $W(d_j)$. A job meets its deadline in time if and only if it meets it in the work scale. On the times where $s = 0$, no schedule does any work, so nothing is lost.

**Step 3. EDF is optimal for feasibility.** In the work scale, the problem is preemptive scheduling on one machine of speed 1 with releases and deadlines. EDF meets all deadlines whenever some schedule does ([EDF optimality](/edf-optimality/)). We recall the exchange: if a schedule runs a job $k$ at a point where a released job $j$ with $d_j < d_k$ is unfinished, swap a small amount of work of $k$ there with the same amount of work of $j$ later, before $C_j \le d_j \le d_k$. Both jobs still meet their deadlines. Repeating this turns any feasible schedule into the EDF schedule.

Step 1 gives a feasible schedule at the AVR speeds, so by Steps 2 and 3, EDF at the AVR speeds meets all deadlines. EDF changes the job only at a release or a completion, so it makes at most $2n$ decisions, and with the pieces of Part 1 it ends after finitely many steps. $\square$
