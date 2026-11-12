---
tag: D4EFKC
kind: algorithm
slug: deferrable-server
name: Deferrable server
area: systems/scheduling
level: research
summary: "A periodic task with budget Cs and period Ts that serves aperiodic requests at a fixed priority. It keeps unused budget until the next period, so it can hit lower tasks twice in a row."
solves: [real-time-scheduling]
model: word-ram
complexity:
  vars: {n: the number of periodic tasks, k: the number of aperiodic requests, h: the number of simulated time units}
  time: {worst: O((n + k) h)}
  space: {extra: O(n + k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1987
  people: [John P. Lehoczky, Lui Sha, Jay K. Strosnider]
  note: Lehoczky, Sha and Strosnider proposed the deferrable server at RTSS 1987; Strosnider, Lehoczky and Sha gave the full analysis in IEEE Transactions on Computers in 1995.
prereqs: [fixed-priority-scheduling, response-time-analysis, sporadic-task-model]
see_also: [sporadic-server, constant-bandwidth-server, rate-monotonic-scheduling, liu-layland-utilization-bound, response-time-analysis, fixed-priority-scheduling, real-time-scheduling, periodic-task-model]
sources:
  - paper: doi:10.1109/12.368008
    title: "Jay K. Strosnider, John P. Lehoczky and Lui Sha, The deferrable server algorithm for enhanced aperiodic responsiveness in hard real-time environments, IEEE Transactions on Computers 44(1) (1995), 73-91"
    locator: the deferrable server rules, the worst case of two back-to-back budgets and the utilization bound under rate monotonic priorities
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 5 (fixed-priority servers), the polling server and the deferrable server
  - book: isbn:9780130996510
    title: Jane W. S. Liu, Real-Time Systems, Prentice Hall, 2000
    locator: Chapter 7 (scheduling aperiodic and sporadic jobs in priority-driven systems), the deferrable server
---

A deferrable server is a periodic task that does no work of its own: it runs aperiodic requests at a fixed priority, for at most a budget of $C_s$ time units in each period $T_s$. Unlike a polling server, it keeps its budget while no request waits and spends it at once when a request comes, so the response time of aperiodic work is short. The cost is that it can take two full budgets back to back, at the end of one period and the start of the next. So a lower task sees more interference than from a periodic task $(C_s, T_s)$. Lehoczky, Sha and Strosnider proposed it in 1987.

## In plain words

A help desk has one worker, and the worker also has regular jobs to do on a fixed plan. The desk gets a fixed amount of the worker's time each hour, for example ten minutes. If nobody comes, the ten minutes stay saved until someone comes, and they are not lost. At the start of each hour the desk gets a fresh ten minutes, and saved time does not carry over.

Visitors are served fast, because the saved time is ready when they come. But a visitor at 9:50 can use ten minutes up to 10:00, and then ten fresh minutes up to 10:10. So the regular jobs can lose twenty minutes in a row, not ten. The plan for the regular jobs must allow for this.

## The problem

One processor runs periodic tasks $\tau_i = (C_i, T_i, D_i)$ with $D_i \le T_i$ under preemptive [fixed priorities](/fixed-priority-scheduling/), and the hard tasks must meet all deadlines. Aperiodic requests also arrive, at unknown times and with unknown demands. They have no hard deadlines, and the goal is to serve them soon. Running them in the background, at the lowest priority, is safe but slow. Running them at a high priority is fast but can make the hard tasks miss. A server is a task that runs aperiodic work at a set priority $P_s$ under a budget rule, so that its worst effect on the hard tasks is known and can go into a [schedulability test](/response-time-analysis/).

## The algorithm

The server has a priority $P_s$, a capacity $C_s$ and a period $T_s$, with $C_s \le T_s$. The budget $c$ is the time it may still run in the current period. Requests wait in a first-come, first-served queue $Q$. Time is cut into units.

```pseudo id=main
DEFERRABLE-SERVER(tasks, Ps, Cs, Ts)
L1  for t ← 0, 1, 2, ... do
L2      if t is a multiple of Ts then c ← Cs                ▷ new budget; the old one is lost
L3      release the periodic jobs due at t; put the requests that arrive at t at the end of Q
L4      the server is ready at priority Ps if Q is not empty and c > 0
L5      run the ready entity of highest priority for one unit
L6      if the server ran then c ← c − 1 and the head of Q gets one unit; remove it from Q when done
```

Line L4 is the difference from a polling server. A polling server is ready only at the start of its period and gives up its budget when $Q$ is empty then. A deferrable server is ready at any time in the period while $c > 0$. Line L2 is the difference from a [sporadic server](/sporadic-server/): the budget comes back at fixed times, whatever the server did.

## Example

A server with $C_s = 2$, $T_s = 5$ has the top priority. A hard task $\tau_1$ with $C_1 = 2$ and $D_1 = 5$ is released at time 3. An aperiodic request of 4 units arrives at time 3. This case is a test of the implementation.

| slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| budget $c$ at the start | 2 | 2 | 2 | 2 | 1 | 2 | 1 | 0 | 0 |
| runs | idle | idle | idle | server | server | server | server | $\tau_1$ | $\tau_1$ |

The server saves its budget through slots 0 to 2, spends it in slots 3 and 4, gets a new budget at time 5 from line L2, and spends it in slots 5 and 6. $\tau_1$ ends at 9, so its response time is 6 and it misses its deadline at 8. A periodic task $(2, 5)$ in the place of the server could take at most 2 of the slots 3 to 7, and $\tau_1$ would end by 7. Without the request, $\tau_1$ ends at 5.

## Correctness

The aperiodic work does not have deadlines, so correctness is about the hard tasks. Each budget given at line L2 can be used only before the next multiple of $T_s$. With this fact, a case analysis over where a window of length $w$ starts gives the bound

$$E(w) \le C_s + \left\lceil \frac{w - C_s}{T_s} \right\rceil C_s$$

on the time the server runs in any window of length $w$, at any priority. The bound is reached by the double hit of the example. So the server acts on lower tasks as a periodic task $(C_s, T_s)$ with a release jitter of $T_s - C_s$. Put this term in the [response-time recurrence](/response-time-analysis/):

$$R_i = C_i + \sum_{j \in hp(i)} \left\lceil \frac{R_i}{T_j} \right\rceil C_j + C_s + \left\lceil \frac{R_i - C_s}{T_s} \right\rceil C_s .$$

If $R_i \le D_i$ for each task below $P_s$, and the usual test holds for the tasks above it, no hard job misses. The proof is the standard busy-window argument with the window bound in the place of $\lceil R/T_s \rceil C_s$. The test is sufficient, not exact. The full proof is in the proofs folder.

## Complexity

- **Simulation.** Each time unit scans the $n$ tasks to release jobs and pick the highest priority, and scans the $k$ requests for arrivals, so a run of $h$ units takes $O((n + k) h)$ time. The extra space is $O(n + k)$ for the remaining work and the queue.
- **In a kernel.** The server needs a budget counter, a timer for the next multiple of $T_s$, and a timer that fires when $c$ reaches 0. Each event costs $O(1)$ on top of the ready queue.
- **Analysis.** One extra term per task in the response-time recurrence, so the test costs the same as without the server.

## Properties

- **Bandwidth preserving.** The budget is not lost while no request waits, unlike in a polling server, so a request that comes late in a period is served at once.
- **Fixed replenishment times.** The budget is reset at $0, T_s, 2T_s, \ldots$, whatever the server did. This makes the server simple, and it also causes the double hit.
- **Worse than a periodic task.** The server can run $2C_s$ units in a window of length $2C_s$, so a task set that is schedulable with a periodic task $(C_s, T_s)$ may not be schedulable with a deferrable server of the same parameters.
- **Utilization bound.** With [rate monotonic](/rate-monotonic-scheduling/) priorities and the server at the top priority, Strosnider, Lehoczky and Sha showed that the hard tasks are schedulable if $U_p \le n[((U_s + 2)/(2U_s + 1))^{1/n} - 1]$, where $U_s = C_s/T_s$. As $n$ grows, this tends to $\ln((U_s + 2)/(2U_s + 1))$. With $U_s = 0$ it is the [Liu and Layland bound](/liu-layland-utilization-bound/) $\ln 2$.

## Variants and improvements

- **Polling server.** The same budget and period, but the budget is lost if $Q$ is empty at the start of the period. It acts exactly as a periodic task, at the cost of a longer aperiodic response.
- **Sporadic server.** It gives back each piece of budget one period after that piece started to be used, not at fixed times. It keeps the fast response of the deferrable server and acts on lower tasks as a periodic task. See [sporadic server](/sporadic-server/).
- **Priority exchange.** The server trades its unused budget for time at lower priority levels with the periodic tasks, so the budget is kept but moves down in priority.
- **Servers under EDF.** With [earliest deadline first](/earliest-deadline-first/), a dynamic deferrable server gives its jobs deadlines at the end of the current server period. The [constant bandwidth server](/constant-bandwidth-server/) is the common choice under EDF.

## When to use it

Use it when aperiodic events need a fast response, the system uses fixed priorities, and you can afford the larger interference term in the analysis, for example when $C_s$ is small compared with $T_s$. It is simpler to build than a sporadic server: one counter and one periodic timer. If the double hit makes the hard tasks fail the test, use a sporadic server with the same $C_s$ and $T_s$, or make $C_s$ smaller.

## Pitfalls

- **Analysing it as a periodic task.** The term $\lceil R/T_s \rceil C_s$ is too small. The example shows a task that passes the test with this term and misses its deadline. Use the jitter term above.
- **Carrying the budget over.** Line L2 sets $c$ to $C_s$; it does not add $C_s$. If unused budget accumulates over periods, the server can run for many budgets in a row and no bound holds.
- **Spending budget with no work.** Line L4 needs both a waiting request and $c > 0$, and line L6 lowers $c$ only when the server runs. If the budget falls while the server is preempted or idle, the server becomes a polling server.
- **Wrong time for the reset.** The resets at line L2 must be on a fixed grid. If the server resets one period after its first use instead, it is a different server, and the proof does not apply as written.

## Implementations

## History

Lehoczky, Sha and Strosnider presented the deferrable server at the IEEE Real-Time Systems Symposium in 1987, as a way to serve aperiodic events faster than polling while keeping the periodic tasks safe. Strosnider, Lehoczky and Sha published the full analysis in IEEE Transactions on Computers in 1995, with the utilization bound for rate monotonic priorities. Sprunt, Sha and Lehoczky designed the sporadic server in 1989 to remove the double hit.

## References
