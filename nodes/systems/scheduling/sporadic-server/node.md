---
tag: NBTSC8
kind: algorithm
slug: sporadic-server
name: Sporadic server
area: systems/scheduling
level: research
summary: "A fixed-priority aperiodic server that gives back each used piece of its budget one period after that use began. It serves requests fast and acts on lower tasks like a periodic task."
solves: [real-time-scheduling]
model: word-ram
complexity:
  vars: {n: the number of periodic tasks, k: the number of aperiodic requests, h: the number of simulated time units}
  time: {worst: O((n + k) h)}
  space: {extra: O(n + k + h)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1989
  people: [Brinkley Sprunt, Lui Sha, John P. Lehoczky]
  note: Sprunt, Sha and Lehoczky defined the sporadic server in Real-Time Systems in 1989, to keep the fast response of the deferrable server without its double hit; POSIX later added it as SCHED_SPORADIC.
prereqs: [deferrable-server]
see_also: [deferrable-server, constant-bandwidth-server, fixed-priority-scheduling, response-time-analysis, sporadic-task-model, rate-monotonic-scheduling, real-time-scheduling]
sources:
  - paper: doi:10.1007/BF02341920
    title: "Brinkley Sprunt, Lui Sha and John P. Lehoczky, Aperiodic task scheduling for hard-real-time systems, Real-Time Systems 1(1) (1989), 27-60"
    locator: the sporadic server algorithm, its replenishment rules and the proof that it can be analysed as a periodic task
  - paper: doi:10.1109/RTAS.2010.34
    title: "Mark Stanovich, Theodore P. Baker, An-I Wang and Michael González Harbour, Defects of the POSIX sporadic server and how to correct them, IEEE Real-Time and Embedded Technology and Applications Symposium (2010), 35-45"
    locator: the defects of the POSIX replenishment rules and the corrected rules
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 5 (fixed-priority servers), the sporadic server and its replenishment rules
  - book: isbn:9780130996510
    title: Jane W. S. Liu, Real-Time Systems, Prentice Hall, 2000
    locator: Chapter 7 (scheduling aperiodic and sporadic jobs in priority-driven systems), sporadic servers
---

A sporadic server serves aperiodic requests at a fixed priority with a budget of $C_s$ time units, like a [deferrable server](/deferrable-server/), but it does not get its budget back at fixed times. Each piece of budget that it uses comes back one period $T_s$ after the time at which the server became active for that use. So the server can never use more than $C_s$ in any window of length $T_s$, and a lower task can treat it exactly as a periodic task $(C_s, T_s)$ in its [response-time test](/response-time-analysis/). Sprunt, Sha and Lehoczky defined it in 1989.

## In plain words

A help desk may use ten minutes of the worker's time in any hour. Each time the desk uses some minutes, it writes a note: "these minutes come back one hour after this visit started". It does not get a full fresh ten minutes at every full hour.

So the desk can still help a visitor at once if it has minutes left. But it can never use more than ten minutes in any hour, wherever that hour starts. The regular jobs of the worker see the desk as one more regular job of ten minutes every hour, and the plan for them stays simple.

## The problem

One processor runs [periodic](/periodic-task-model/) tasks $\tau_i = (C_i, T_i, D_i)$ with $D_i \le T_i$ under preemptive [fixed priorities](/fixed-priority-scheduling/), and they must meet all deadlines. Aperiodic requests arrive at unknown times with unknown demands and should be served soon. A [deferrable server](/deferrable-server/) gives a fast response, but its budget is reset at fixed times, so it can run $2C_s$ units in a row and the hard tasks must allow for that. The goal is a server with the same fast response that interferes with lower tasks no more than a periodic task $(C_s, T_s)$, so that the hard tasks are analysed as if the server were an ordinary task.

## The algorithm

The server has a priority $P_s$, a capacity $C_s$ and a period $T_s$, with $C_s \le T_s$, and starts with $c = C_s$. The server is *active* while the running job has a priority of at least $P_s$, and *idle* otherwise. A replenishment is a pair (time, amount). FINALIZE schedules the amount $used$ at time $RT$, if the server is armed and $used > 0$, and then disarms it.

```pseudo id=main
SPORADIC-SERVER(tasks, Ps, Cs, Ts)
L1  for t ← 0, 1, 2, ... do c ← c + the replenishments due at t
L2      release the periodic jobs due at t; put the requests that arrive at t at the end of Q
L3      the server is ready at priority Ps if Q is not empty and c > 0
L4      run the ready entity of highest priority for one unit
L5      if the server was active and the running priority is now below Ps then FINALIZE
L6      if the server is active, not armed and c > 0 then arm it: RT ← t + Ts; used ← 0
L7      if the server ran then c ← c − 1; used ← used + 1; the head of Q gets one unit
L8          if c = 0 then FINALIZE
```

Line L6 sets the replenishment time when the priority level $P_s$ becomes busy and the server has budget. Lines L5 and L8 fix the amount: what the server used since then, given back at $RT$. Budget that is not used is kept, so the server keeps the fast response of the deferrable server.

## Example

The same case as on the [deferrable server](/deferrable-server/) page: the server has $C_s = 2$, $T_s = 5$ and the top priority, a hard task $\tau_1$ with $C_1 = 2$ and $D_1 = 5$ is released at time 3, and a request of 4 units arrives at time 3.

| slot | 0 to 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| budget $c$ at the start | 2 | 2 | 1 | 0 | 0 | 0 | 2 | 1 | 0 |
| sporadic server runs | idle | server | server | $\tau_1$ | $\tau_1$ | idle | server | server | idle |
| deferrable server runs | idle | server | server | server | server | $\tau_1$ | $\tau_1$ | idle | idle |

The sporadic server arms at 3 with $RT = 8$, uses 2 units, and reaches $c = 0$, so line L8 schedules the replenishment $(8, 2)$. It cannot run again before 8, so $\tau_1$ ends at 7 and meets its deadline. The request ends at 10 instead of 7. The deferrable server gets a new budget at 5 and makes $\tau_1$ end at 9, a miss.

With small requests, the replenishments split up. With the same server and requests of 1 unit at time 1 and 3 units at time 3, the server runs in slots 1, 3, 6 and 8, and the replenishments are $(6, 1)$, $(8, 1)$, $(11, 1)$ and $(13, 1)$: each unit comes back 5 units after the slot in which it was used.

## Correctness

The aperiodic requests have no deadlines, so correctness is about the hard tasks. Count the capacity as $C_s$ tokens. A run of the server from an arming time $t_A$ to a FINALIZE uses distinct tokens, and they all come back at $t_A + T_s$. For a window $[t, t + T_s)$, either no run is in progress at $t$, and each token is used at most once in the window, or a run that started at $t_A < t$ has used $b$ tokens before $t$. Then at most $C_s - b$ tokens are free for $[t, t_A + T_s)$, and the rest of the window has length $b$. In both cases the server runs at most $C_s$ units in the window. So in any window of length $w$ it runs at most $\lceil w / T_s \rceil C_s$ units, which is the term of a periodic task. With this term, the standard busy-window argument proves the test

$$R_i = C_i + \sum_{j \in hp(i)} \left\lceil \frac{R_i}{T_j} \right\rceil C_j + \left\lceil \frac{R_i}{T_s} \right\rceil C_s \le D_i,$$

which is sufficient, not exact. The proofs folder has the full proof for a server at the top priority. For other priorities, Sprunt, Sha and Lehoczky show the same result, and the tests check it at random priorities.

## Complexity

- **Simulation.** Each time unit scans the $n$ tasks and the $k$ requests, and the replenishments are kept in a map from time to amount, so a run of $h$ units takes $O((n + k) h)$ time. The extra space is $O(n + k + h)$, as up to $O(h)$ replenishments can wait.
- **In a kernel.** A list of pending replenishments in time order, and two timers: one for the next replenishment and one for $c = 0$. With $C_s$ in integer units, at most $C_s$ replenishments are pending, since each holds at least one unit.
- **Analysis.** The server is one more periodic task in the test, so the test costs nothing extra.

## Properties

- **No double hit.** In any window of length $T_s$ the server runs at most $C_s$ units, so it is no worse than a periodic task for the tasks below it.
- **Bandwidth preserving.** Unused budget is kept, so a request is served at once if budget is left, as with a deferrable server.
- **Utilization.** Since the server is a periodic task for the analysis, the [Liu and Layland bound](/liu-layland-utilization-bound/) and [rate monotonic](/rate-monotonic-scheduling/) theory apply with $U_s = C_s / T_s$ as one more task.
- **Fragmentation.** Small requests split the budget into many small replenishments. This costs timer events but does not lower the guarantee.

## Variants and improvements

- **POSIX SCHED_SPORADIC.** POSIX gives a thread a normal priority, a low priority for when its budget is spent, a budget, a period and a maximum number of pending replenishments. Stanovich, Baker, Wang and González Harbour showed in 2010 that the standard rules can let the server use more than its budget, and gave corrected rules.
- **Priority exchange and slack stealing.** Other fixed-priority servers trade budget with the periodic tasks or compute the slack at run time. They can give better aperiodic response, at a higher cost.
- **Under EDF.** The dynamic sporadic server gives the budget a deadline at the replenishment time. The [constant bandwidth server](/constant-bandwidth-server/) is the common choice for EDF.
- **Sporadic tasks.** A [sporadic task](/sporadic-task-model/) with a known minimum gap can run in its own sporadic server, which enforces the gap if the task breaks it.

## When to use it

Use it in a fixed-priority system when aperiodic or overrunning work needs a fast response and the hard tasks need a simple, safe analysis. It is the standard server for fixed priorities when the double hit of a [deferrable server](/deferrable-server/) is too costly. If simplicity matters more than the extra margin, a deferrable server with a smaller budget can be enough.

## Pitfalls

- **Arming at the wrong time.** Line L6 must set $RT$ when the level $P_s$ becomes busy and the server has budget. Setting it when a request arrives, or when the server is idle, lets the budget come back too early.
- **Giving back the full capacity.** Lines L5 and L8 must schedule only the amount used since the arming, not $C_s$. A full refill turns the server into a deferrable server with a moving period, and the window bound fails.
- **Forgetting to finalize at zero budget.** If line L8 is missing, a run that ends with $c = 0$ and goes on after a replenishment is counted as one run, and its replenishment time is too early.
- **Trusting the POSIX rules as written.** Implementations that follow the standard literally can overrun the budget. Use the corrected rules.

## Implementations

## History

Sprunt, Sha and Lehoczky published the sporadic server in the first volume of the journal Real-Time Systems in 1989, after the deferrable server and priority exchange servers of Lehoczky, Sha and Strosnider. It was the first server that keeps its budget and still acts like a periodic task. POSIX added the SCHED_SPORADIC policy in its real-time extensions, and Stanovich, Baker, Wang and González Harbour found and corrected defects in those rules in 2010.

## References
