---
tag: HSXH10
kind: algorithm
slug: bully-algorithm
name: Bully algorithm
aliases:
- Garcia-Molina's bully algorithm
area: distributed/leader-election
level: core
summary: Election with crash failures in a synchronous system. A process that sees the coordinator fail asks all higher processes; the highest live process wins. Θ(n²) messages in the worst case.
model: synchronous-model
complexity:
  vars: {n: the number of processes}
  time: {worst: O(1)}
  messages: {worst: O(n^2), best: O(n)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 1982
  people: [Hector Garcia-Molina]
  note: Defined the election problem with crash failures and gave the bully and invitation algorithms.
prereqs: [synchronous-model, message-complexity, explicit-leader-election]
see_also: [invitation-algorithm, omega-failure-detector, raft, complete-network-leader-election, ring-leader-election, floodmax, consensus-problem, asynchronous-model]
sources:
  - paper: doi:10.1109/TC.1982.1675885
    title: Hector Garcia-Molina, Elections in a Distributed Computing System, IEEE Transactions on Computers C-31(1), 1982
    locator: pages 48 to 59 (the election assertions, the synchronous assumptions, and the Bully Algorithm)
---

The bully algorithm elects a coordinator among $n$ processes that can crash, in a system where every message arrives within a known time and every process answers within a known time. When a process sees that the coordinator has failed, it sends an election message to every process with a larger identifier. If none answers in time, it takes over and tells the processes with smaller identifiers. If a larger process answers, that process takes over the election. The live process with the largest identifier always wins, which is why the algorithm is called the bully. Garcia-Molina gave it in 1982. It sends $\Theta(n^2)$ messages in the worst case.

## In plain words

A team needs one boss. Everyone has a different rank, and everyone knows everyone else's rank. People can leave suddenly, but a message always arrives within a known time, so silence means the other person is gone.

When someone notices that the boss is gone, they ask everyone with a higher rank: "Are you there?" Anyone higher who is there answers "Yes, I'll take it from here" and starts the same thing with the people above them. If nobody higher answers in time, the person who asked becomes the boss and tells everyone below them.

So the highest-ranked person who is still there always ends up as the boss. If a higher person comes back later, they take over again.

## The problem

There are $n$ processes with distinct identifiers $1, \ldots, n$, and every process knows all identifiers. Every pair of processes can exchange messages. The system is [synchronous](/synchronous-model/) in the sense of Garcia-Molina: messages are not lost and arrive within a known time $\delta$, and a live process handles a message within a known time. Processes fail by crashing. A crashed process may later recover; it then knows that it has crashed and starts again from a fixed state. Each process $p$ has a variable $\mathit{coord}_p$.

The goal, after the last crash or recovery, is that every live process has $\mathit{coord}_p$ equal to the same live process, and in the bully algorithm this is the live process with the largest identifier. While crashes go on, no algorithm can stop the leader from changing.

## The algorithm

The algorithm uses three kinds of message: ELECTION, OK and COORDINATOR. It uses two timers: $T_{\mathrm{ok}} = 2\delta$, the time for a round trip, and $T_{\mathrm{coord}}$, long enough for an election started above to end.

```pseudo id=main
BULLY(u)                                      ▷ the code of process u
L1  on noticing that coord has crashed, or on recovery: START-ELECTION
L2  START-ELECTION: electing ← true; send ELECTION to every process v > u
L3      start the timer T_ok
L4  on ELECTION from v < u: send OK to v; if not electing then START-ELECTION
L5  on OK: stop T_ok; start the timer T_coord          ▷ a larger process is alive
L6  on timeout of T_ok: BECOME-COORDINATOR             ▷ no larger process answered
L7  BECOME-COORDINATOR: coord ← u; electing ← false; send COORDINATOR(u) to every v < u
L8  on COORDINATOR(w): if w < u then START-ELECTION    ▷ bully the smaller one
        else coord ← w; electing ← false; stop all timers
L9  on timeout of T_coord: START-ELECTION              ▷ the larger process crashed too
```

The process with the largest identifier sends no ELECTION messages, waits $T_{\mathrm{ok}}$, and then becomes the coordinator. A process that crashes and recovers starts an election at once (line L1), so a large process that comes back takes over. This is the bully step.

**The original form.** In Garcia-Molina's paper the winner first sends a *halt* message to the processes below it and then a message that names the new coordinator, so that the processes also agree on the state of the task they run. The page uses the shorter three-message form found in most textbooks. The two forms elect the same process and have the same order of messages.

## Example

Take $n = 5$. Process 5 is the coordinator and crashes. At step 1, process 2 notices.

| step | event | messages |
|---|---|---|
| 1 | 2 sends ELECTION to 3, 4, 5 | 3 |
| 2 | 3 and 4 answer OK to 2; 3 sends ELECTION to 4, 5; 4 sends ELECTION to 5 | 2 + 3 |
| 3 | 4 answers OK to 3; 2 has an OK and waits | 1 |
| 4 | 4 has no answer from 5 and becomes the coordinator; it sends COORDINATOR to 1, 2, 3 | 3 |

The run sends $6$ ELECTION, $3$ OK and $3$ COORDINATOR messages, $12$ in total. Process 1 does not take part in the election, but it learns the result. If process 5 recovers later, it starts an election, gets no answer, and sends COORDINATOR to 1, 2, 3 and 4.

## Correctness

The proof assumes that no process crashes or recovers during the election that is analysed. Let $h$ be the live process with the largest identifier.

- **The winner is $h$.** A process $u < h$ that starts an election sends ELECTION to $h$, and $h$ answers OK within $2\delta$, so $u$ never runs line L6. Process $h$ starts an election when it gets that message (line L4). It sends ELECTION only to crashed processes, gets no OK, and runs line L7. So $h$ is the only process that sends COORDINATOR.
- **Everyone learns it.** $h$ sends COORDINATOR to every process below it, and each live one sets $\mathit{coord} = h$ by line L8. A process that started an election and got an OK waits on $T_{\mathrm{coord}}$. Its ELECTION reached $h$ one hop after it was sent, so $h$ announces at most $\delta$ after the OK arrives, and the COORDINATOR message arrives within $2\delta$ of the OK. So $T_{\mathrm{coord}} = 3\delta$ is safe.
- **Crashes during the election.** If a process that answered OK crashes, the timer of line L9 runs out and the election starts again. Each new crash or recovery can start a new election, but when they stop, the argument above applies to the last election.

The [proof of correctness](proofs/correctness/) also derives the exact message counts.

## Complexity

Count the ELECTION, OK and COORDINATOR messages of one election in which no process crashes or recovers. Suppose all processes that notice the failure start at the same step, and let $s$ be the smallest of them. Then every process $u \ge s$ starts exactly once: either it notices, or it gets ELECTION from $s$ at the next step. No process below $s$ starts. So:

- each live $u \ge s$ sends one ELECTION to each $v > u$, live or not;
- each live $v$ answers OK to each ELECTION from a live $u < v$;
- $h$ sends COORDINATOR to each $v < h$.

**Worst case.** The count is largest when $s = 1$, the process with the smallest identifier. If all $n$ processes are live, for example when the system starts:

$$\underbrace{\sum_{u=1}^{n} (n - u)}_{\text{ELECTION}} + \underbrace{\binom{n}{2}}_{\text{OK}} + \underbrace{(n-1)}_{\text{COORDINATOR}} = \frac{n(n-1)}{2} + \frac{n(n-1)}{2} + n - 1 = n^2 - 1.$$

If the old coordinator $n$ has crashed and the other $n - 1$ processes are live, process $u$ still sends $n - u$ ELECTION messages, but only $\binom{n-1}{2}$ OK messages come back and $h = n - 1$ sends $n - 2$ COORDINATOR messages:

$$\frac{n(n-1)}{2} + \frac{(n-1)(n-2)}{2} + (n - 2) = n^2 - n - 1.$$

Both are $\Theta(n^2)$.

**Best case.** If process $n - 1$ notices that $n$ has crashed, it sends one ELECTION message, gets no answer, and sends $n - 2$ COORDINATOR messages: $n - 1$ messages in all.

**Time.** With all starters at the same step, $h$ starts at most $\delta$ later and becomes coordinator $2\delta$ after that, so the election ends within $4\delta$ of the first notice. Each crash during the election adds at most one timeout.

**Late starters.** If a process notices the failure after $h$ has already announced, its ELECTION reaches $h$ again and $h$ runs a second election and a second announcement. The count above is for one wave; the tests show a case with a second wave.

## Properties

- **Deterministic.**
- **Needs a reliable failure detector.** The timeouts are correct only because the system is synchronous. With a wrong timeout, two processes can both become coordinator.
- **The leader is the live process with the largest identifier**, and it changes back when a larger process recovers.
- **Every process knows all identifiers** and can send to each of them directly.
- **Not partition tolerant.** If the network splits, each part elects its own coordinator. The [invitation algorithm](/invitation-algorithm/) handles this case.

## Variants and improvements

- **The invitation algorithm.** For [asynchronous](/asynchronous-model/) systems with partitions, Garcia-Molina gave the [invitation algorithm](/invitation-algorithm/), which only promises groups whose members agree.
- **Fewer messages.** A process can send ELECTION to the larger processes one at a time from the top, and stop at the first answer. The worst case then becomes $O(n)$ messages but the time grows to $O(n\delta)$.
- **No bully on recovery.** A recovering process can accept the current coordinator if it is live. This avoids a change of leader each time a large process comes back.
- **Modern systems.** Systems that must stay safe without synchrony use [Raft](/raft/) style terms and majorities, or an [Omega failure detector](/omega-failure-detector/) together with [consensus](/consensus-problem/).

## When to use it

Use it in a small, fully connected group where message delays and processing times have a known bound and a crash can be detected by a timeout. It is simple and makes the most capable process the leader. Do not use it where the network can split or delays have no bound, because then it can elect two leaders.

## Pitfalls

- **Timeouts that are too short.** A slow but live process looks crashed, and two coordinators act at the same time.
- **Forgetting to restart.** A process that got an OK must restart the election if no COORDINATOR arrives (line L9); otherwise a crash of the answering process leaves it without a leader for ever.
- **Counting only the messages to live processes.** The ELECTION messages to crashed processes are sent too. The count $n^2 - n - 1$ includes them.
- **Assuming one wave.** Processes that notice the failure at different times can cause more than one announcement.

## Implementations

## History

Garcia-Molina studied elections in 1982, in the IEEE Transactions on Computers. He stated the problem with assertions about the states of the processes, gave the bully algorithm for systems with time bounds and crash failures, and gave the invitation algorithm for systems where the network can split. The bully algorithm became a standard example in textbooks on distributed systems.

## References
