---
tag: ASK6PS
kind: algorithm
slug: chandy-misra-bryant
name: Chandy-Misra-Bryant algorithm
aliases:
- conservative parallel simulation
- null message protocol
area: distributed/clocks-and-ordering
level: advanced
summary: Conservative parallel simulation. A process runs an event only when no input link can still bring an earlier one. Null messages carry lower bounds on future timestamps, which prevents deadlock.
solves: [parallel-discrete-event-simulation]
model: asynchronous-model
complexity:
  vars: {E: the number of events, e: the number of links, d: the largest number of input links of a process, T: the end time (an integer)}
  time: {worst: O((E + e T) d)}
  space: {extra: O(E + e)}
  messages: {worst: O(E + e T)}
properties: {deterministic: true, recursive: false}
history:
  year: 1979
  people: [K. Mani Chandy, Jayadev Misra, Randal E. Bryant]
  note: Bryant described the method in an MIT report in 1977, and Chandy and Misra published it with null messages and a proof in IEEE Transactions on Software Engineering in 1979.
prereqs: [parallel-discrete-event-simulation, fifo-delivery]
see_also: [parallel-discrete-event-simulation, time-warp, virtual-time, global-virtual-time, deadlock, fifo-delivery, event-driven-simulation]
sources:
  - paper: "K. Mani Chandy and Jayadev Misra, Distributed simulation, a case study in design and verification of distributed programs, IEEE Transactions on Software Engineering SE-5(5), 1979, pages 440 to 452"
    locator: the safe processing rule, null messages, and the proof of absence of deadlock (volume and pages from memory, to be checked)
  - paper: "Randal E. Bryant, Simulation of packet communication architecture computer systems, Technical Report MIT/LCS/TR-188, Massachusetts Institute of Technology, 1977"
    locator: the conservative method with lower bounds sent on the links (report number from memory, to be checked)
  - paper: "K. Mani Chandy and Jayadev Misra, Asynchronous distributed simulation via a sequence of parallel computations, Communications of the ACM 24(4), 1981"
    locator: the variant without null messages, with deadlock detection and recovery (volume from memory, to be checked)
  - paper: "Jayadev Misra, Distributed discrete-event simulation, ACM Computing Surveys 18(1), 1986, pages 39 to 65"
    locator: the model of logical processes, null messages and lookahead (volume and pages from memory, to be checked)
  - book: isbn:9780471183839
    title: Richard M. Fujimoto, Parallel and Distributed Simulation Systems, Wiley, 2000
    locator: the chapter on conservative synchronization (null messages, lookahead, deadlock detection and recovery; ISBN from memory, to be checked)
---

The *Chandy-Misra-Bryant algorithm* is the first conservative method for [parallel discrete event simulation](/parallel-discrete-event-simulation/). Each logical process gets its events over FIFO links, each in timestamp order, so the head of a link is a lower bound on everything that link will still bring. A process runs its earliest event only when every input link has shown a bound above it. To stop processes from waiting for each other forever, a process sends *null messages*, which carry no event, only the promise "nothing I send from now on will have a timestamp below $v$". Randal Bryant (1977) and K. Mani Chandy and Jayadev Misra (1979) found the method independently.

## In plain words

A station in a factory simulation gets parts from several other stations. Each input belt delivers its parts in time order. So when every belt has a part waiting, the earliest of those parts is surely the next one, and the station can work on it. If one belt is empty, the station cannot know what that belt will bring, and it must wait.

If two stations each wait for the other, nothing moves. Null messages fix this. Each station tells its neighbours: "every part I send you from now on will be at time $v$ or later". It knows this because its own next part cannot come before its next input, and handling a part takes at least $L$ time units. Such promises go around the loop, each one $L$ larger than the one before, until they pass the time of a waiting part and set it free.

## The problem

**Model.** As in [parallel discrete event simulation](/parallel-discrete-event-simulation/): logical processes, here called stations, are connected by directed links that are reliable and FIFO (see [FIFO delivery](/fifo-delivery/)), with unbounded delay. Each station sends on each output link events with strictly increasing timestamps. Every station has *lookahead* $L \ge 1$: an event that it schedules has a timestamp at least $L$ above both the event that caused it and the last event it sent. The simulation stops at the integer time $T$.

The implementation here simulates a closed network of FIFO queues: a job that arrives at time $a$ leaves at $\max(a, \mathit{last}) + s$, where $\mathit{last}$ is the previous departure and the service time $s \ge L$ depends only on the job and its visit number.

**Goal.** Each station runs the events sent to it in increasing order of the key (timestamp, source link), which by the theorem on the [PDES page](/parallel-discrete-event-simulation/) gives the result of the sequential simulation; and the run must not stop while an event at time $T$ or earlier is left.

## The algorithm

Each station $i$ keeps a FIFO queue and a bound $\mathit{bound}_j$ for each input link $j$, and the time $\mathit{last}$ of its last departure. $\mathit{bound}_j$ is a lower bound on the timestamp of the next message that link $j$ will deliver.

```pseudo id=main
STEP(i)                                         ▷ run whenever something changes at station i
    loop
L1      h ← the queued message with the least key (ts, source)
L2      if some input link j has an empty queue and (bound_j, j) < (ts(h), source(h)) then leave the loop
        if ts(h) > T then leave the loop
L3      take h off its queue; dep ← max(ts(h), last) + service; last ← dep
L4      if dep ≤ T then send the job on its next link with timestamp dep
L5  v ← min(max(T_in, last) + L, T + 1)         ▷ T_in: the least head or bound over all input links
    for each output link k: if v is above the last null sent on k then send null(v) on k

RECEIVE(i, j, msg)
    if msg is null(v) then
L6      bound_j ← max(bound_j, v)
    else append msg to the queue of link j; bound_j ← ts(msg) + 1
```

Line L2 is the safety test: a link with an empty queue can still bring a message, and its key would be at least $(\mathit{bound}_j, j)$. Line L5 is the promise: a future departure of $i$ is at least $\max(\text{its arrival}, \mathit{last}) + L$, and its arrival is at least $T_{\mathrm{in}}$.

## Example

Three stations with links $0 \to 1$, $1 \to 0$, $0 \to 2$ and $2 \to 0$, lookahead $L = 1$, end time $T = 30$, and one job that starts at station 0. The job goes from station 0 to station 1 and back, again and again; it never goes to station 2.

**Without null messages.** Station 0 runs the job at time 0 and sends it to station 1 for time 1. Station 1 sends it back for time 3. Now station 0 has the job at time 3 in the queue of link 1, but the queue of link 2 is empty with bound 0, and $(0, 2) < (3, 1)$. Line L2 says that station 2 might still send something earlier, so station 0 waits. Station 2 has nothing to do and never sends anything. The run stops with work left: a [deadlock](/deadlock/).

**With null messages.** Station 2 has an empty input with a bound that grows from the nulls of station 0, and it sends back that bound plus $L$. Each exchange of nulls between stations 0 and 2 raises the bound of link 2 at station 0 by about $2L$. When it passes 3, the job at time 3 is safe and runs, and so on. The run ends with the same events as the sequential simulation: 7 arrivals at station 0, at times 0, 3, 10, 13, 20, 23 and 30, and 6 at station 1. It uses 38 null messages.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has three steps.

- **The bounds are true.** By induction over the messages: when station $i$ sends null($v$), every later departure of $i$ is at least $v$, because its arrivals are at least $T_{\mathrm{in}}$ and its service time is at least $L$. So $\mathit{bound}_j$ never exceeds the timestamp of a message that link $j$ will still deliver.
- **Safety.** If line L2 passes, every message that station $i$ will still receive has a larger key than $h$. So each station runs its events in key order, and by the theorem on the [PDES page](/parallel-discrete-event-simulation/) the result is the sequential one.
- **No deadlock.** Suppose the run stops with an event at time at most $T$ left. Let $\tau \le T$ be the least $T_{\mathrm{in}}$ over all stations. Every station has sent nulls of at least $\min(\tau + L, T + 1) > \tau$ on every output, so no empty link has a bound of $\tau$ or less, and the queued event at time $\tau$ passes line L2, a contradiction.

The seeded tests run 40 random strongly connected networks of 2 to 6 stations, with random delays and lookahead 1 to 3, and compare every station's list of events with the sequential simulation. They also run the example above, with and without nulls, and check that without nulls a run either matches the sequential result or stops with a correct prefix.

## Complexity

Each event is one job message and runs in $O(d)$ time for the test of line L2. The nulls on one link carry strictly increasing integers of at most $T + 1$, so there are at most $e(T + 1)$ of them. This gives $O(E + eT)$ messages and $O((E + eT)\,d)$ time. Each station stores its queues and one bound per link.

The bound on nulls is the real cost: with small $L$, the nulls go around a cycle about $T / L$ times, and each takes a message, even when no real event moves.

## Properties

- **Never wrong.** No event is run before an earlier one at the same station, so there are no rollbacks and no saved states.
- **Needs lookahead.** With $L = 0$ the nulls on a cycle do not grow, and the run can deadlock. With small $L$ it makes many nulls.
- **Needs a fixed graph.** Every station must know its input links, since an empty link blocks it.
- **Deterministic result.** The order of the keys fixes the result, whatever the delays.

## Variants and improvements

- **Deadlock detection and recovery (Chandy and Misra 1981).** Send no nulls. When all stations are blocked, which a [termination detection](/termination-detection/) method finds, run the events with the least timestamp in the whole system, which are always safe, and continue.
- **Nulls on demand.** A blocked station asks the station at the end of its empty link for a null, instead of every station sending nulls all the time.
- **Better lookahead.** A station that knows its next service time $s \ge L$ in advance can promise $\max(T_{\mathrm{in}}, \mathit{last}) + s$ instead of adding only $L$, which raises the bounds faster when $s$ is larger than $L$.
- **Window methods.** All stations run the events below the least timestamp plus $L$ and then meet at a barrier (see the [PDES page](/parallel-discrete-event-simulation/)).

## When to use it

Use it when the model has good lookahead, for example a network simulation with link delays of at least a few microseconds, and when saving states for rollback is costly. When lookahead is small or the links between processes change all the time, an optimistic method such as [Time Warp](/time-warp/) is often faster.

## Pitfalls

- **Zero lookahead.** A cycle of stations with $L = 0$ can send nulls with the same value forever. Every cycle must have a positive total lookahead.
- **Ties.** Two events with the same timestamp from different links must be run in a fixed order, here by the number of the link. Without a tie rule, the order of equal times depends on the delays, and the result is no longer the same in every run.
- **Non-FIFO links.** The bounds assume that each link delivers in timestamp order. On a link that reorders, a bound can be wrong and an event can be run too early.
- **Too many nulls.** Sending a null after every step can flood the network; send a null only when its value grows, as line L5 does, or on demand.

## Implementations

## History

Randal E. Bryant described a conservative method with bounds on the links in an MIT report in 1977. K. Mani Chandy and Jayadev Misra published the same idea in IEEE Transactions on Software Engineering in 1979, with null messages and a proof that they prevent deadlock, and in 1981 they gave the variant that detects deadlock and then recovers. Misra's survey of 1986 and Fujimoto's survey of 1990 present it as the basic conservative method.

## References
