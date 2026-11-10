---
tag: R8TGNF
kind: algorithm
slug: lamport-clocks
name: Lamport logical clocks
aliases:
- Lamport timestamps
- scalar logical clocks
area: distributed/clocks-and-ordering
level: intro
summary: Each process keeps a counter, adds 1 at each event, sends it with each message and jumps past a received value, so that a happened-before b implies C(a) < C(b).
solves: [event-ordering]
model: asynchronous-model
complexity:
  vars: {n: the number of processes}
  time: {worst: O(1), best: O(1)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 1978
  people: [Leslie Lamport]
  note: Lamport defined happened-before, the clock rules IR1 and IR2 and the total order in a CACM paper in 1978.
prereqs: [happened-before, asynchronous-model]
see_also: [lamport-clock-condition, total-order, event-ordering, vector-clocks, hybrid-logical-clocks, space-time-diagram, mutual-exclusion-problem, last-writer-wins]
sources:
  - paper: doi:10.1145/359545.359563
    title: Leslie Lamport, Time, clocks, and the ordering of events in a distributed system, Communications of the ACM 21(7), 1978
    locator: pages 558 to 565, sections Logical Clocks (rules IR1 and IR2, the Clock Condition) and Ordering the Events Totally
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 18 (logical time)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 6, Section 6.1 (causality and logical clocks)
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 3, Section 3.3 (scalar time)
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 9, Ordering Guarantees (Lamport timestamps)
---

Lamport logical clocks give each event of a distributed run an integer timestamp $C(e)$, with no physical clock at all. Each process keeps one counter. It adds 1 at each event, puts the counter on each message that it sends, and on a receive it jumps past the value in the message. The result satisfies the [clock condition](/lamport-clock-condition/): if $a$ [happened before](/happened-before/) $b$, then $C(a) < C(b)$. With the process number as a tie-break, the timestamps give a [total order](/total-order/) of all events that agrees with causality.

## In plain words

Each computer keeps a counter that starts at zero. It does not show the time of day. It only counts.

When something happens on a computer, the computer adds one to its counter, and the new value is the label of that event. When the computer sends a message, it writes its counter on the message. When a computer gets a message, it looks at the number on the message. If that number is larger than its own counter, it moves its counter up to that number. Then it adds one, as for any other event.

So a reply always gets a larger label than the question that caused it, even if the two computers count at very different speeds. The labels do not tell you the reverse: a smaller label does not mean that the event came first, or that it had any effect on the other one.

## The problem

There are $n$ processes $p_1, \ldots, p_n$ with unique identifiers. They communicate only by messages over point-to-point channels. The timing is [asynchronous](/asynchronous-model/): there is no bound on message delays or on relative speeds, and there is no common clock. Channels do not need to be FIFO. The algorithm does not use the number of faulty processes $f$, the number of links $m$, the diameter $D$ or a delay bound $\delta$: it is correct for every run, with crashes, with lost messages and with duplicated messages, because each property below is about the events that do happen.

Each process does local events, send events and receive events. The goal is a map $C$ from events to integers with $a \to b \Rightarrow C(a) < C(b)$, where $\to$ is happened-before. This is one form of the [event ordering problem](/event-ordering/).

## The algorithm

Process $p_i$ runs this code. Each call is one event, and the value it returns is the timestamp $C(e)$ of that event.

```pseudo id=main
LAMPORT-CLOCK at process p_i
L1  C_i ← 0

LOCAL-EVENT()
L2  C_i ← C_i + 1                       ▷ IR1: tick before the event
L3  return C_i

SEND(m, p_j)
L4  C_i ← C_i + 1                       ▷ IR1
L5  attach T_m ← C_i to m, send m to p_j  ▷ IR2(a)
L6  return C_i

RECEIVE(m)                              ▷ m carries T_m
L7  C_i ← max(C_i, T_m) + 1             ▷ IR2(b), then IR1
L8  return C_i
```

The total order $\Rightarrow$ compares the pair $(C(e), i)$ of an event $e$ of $p_i$ in lexicographic order. Lamport's paper allows any fixed order of the processes as the tie-break. The index is the usual choice.

## Example

Three processes run seven events. $P_1$ sends a message to $P_2$ (event $a$) and then does a local event $b$. $P_2$ does a local event $c$, receives the message of $a$ (event $d$) and sends a message to $P_3$ (event $e$). $P_3$ does a local event $f$ and receives the message of $e$ (event $g$).

| event | process | kind | rule | $C$ |
|---|---|---|---|---|
| $a$ | $P_1$ | send, $T_m = 1$ | $0 + 1$ | 1 |
| $b$ | $P_1$ | local | $1 + 1$ | 2 |
| $c$ | $P_2$ | local | $0 + 1$ | 1 |
| $d$ | $P_2$ | receive, $T_m = 1$ | $\max(1, 1) + 1$ | 2 |
| $e$ | $P_2$ | send, $T_m = 3$ | $2 + 1$ | 3 |
| $f$ | $P_3$ | local | $0 + 1$ | 1 |
| $g$ | $P_3$ | receive, $T_m = 3$ | $\max(1, 3) + 1$ | 4 |

The chain $a \to d \to e \to g$ gets the timestamps $1 < 2 < 3 < 4$. The total order by $(C, i)$ is $a, c, f, b, d, e, g$.

The converse of the clock condition fails here. $C(b) = 2 < 3 = C(e)$, but $b$ and $e$ are [concurrent](/concurrent-events/): no chain of process steps and messages leads from $b$ to $e$, or from $e$ to $b$. A Lamport timestamp cannot tell $b \parallel e$ apart from $b \to e$.

## Correctness

Each of lines L2, L4 and L7 makes $C_i$ larger by at least 1, so the timestamps on one process strictly increase. A message carries the timestamp of its send (line L5), and line L7 sets the receive timestamp to at least that value plus 1. Every happened-before pair $a \to b$ is joined by a finite chain of these two kinds of steps, so $C(a) < C(b)$ by induction on the length of the chain. Two events of one process never share a timestamp, so the pairs $(C(e), i)$ are all different, and their lexicographic order is a total order that extends $\to$. With exactly 1 per tick, $C(e)$ is also the number of events on a longest causal chain that ends at $e$. The full proofs are below.

## Complexity

- **Time.** Each event costs $O(1)$ integer operations.
- **Space.** Each process stores one integer. Each message carries one integer.
- **Size of the integer.** By the depth result above, $C(e)$ is at most the total number of events $k$ in the run, so a timestamp needs $O(\log k)$ bits. A 64-bit counter is enough in practice.
- **Messages.** The algorithm sends no messages of its own. It only adds one field to the messages of the application.

No timestamp in $\mathbb{R}^k$ with $k < n$ can capture happened-before exactly, in both directions, by the bound of Charron-Bost. So the one-integer cost is possible only because the clock condition asks for one direction. The [vector clocks](/vector-clocks/) page gives the exact version with $n$ integers.

## Properties

- **Safety only.** The clock condition and the total order are safety properties. They hold for each prefix of each run, so they need no liveness assumption.
- **Deterministic.** Given the events of a run, the timestamps are fixed. They do not depend on message delays.
- **Monotone per process.** The clock of a process never goes back while the process keeps its state.
- **Not characterizing.** $C(a) < C(b)$ does not imply $a \to b$, and $C(a) = C(b)$ with $a \ne b$ implies only that $a$ and $b$ are concurrent and on different processes.

## Variants and improvements

- **Any positive increment.** Lamport's rule IR1 asks only that $C_i$ grows between two events, and rule IR2(b) asks only that the receiver sets $C_j$ to a value that is at least its present value and larger than $T_m$. Lines L2, L4 and L7 use the smallest such values.
- **Physical clocks.** The last part of Lamport's paper replaces the counters with physical clocks, which must tick forward and stay close to each other. See [clock synchronization](/clock-synchronization/) and [clock drift](/clock-drift/).
- **[Hybrid logical clocks](/hybrid-logical-clocks/).** Keep the largest physical time seen plus a small counter. The timestamps stay close to physical time and still satisfy the clock condition.
- **[Vector clocks](/vector-clocks/).** One integer per process. They give $a \to b$ if and only if $V(a) < V(b)$.
- **[Matrix clocks](/matrix-clocks/).** An $n \times n$ matrix per process, which also says what each process knows about the others.

## When to use it

Use Lamport clocks when you need a total order of events that never contradicts causality, and one integer per message is all that you can afford. Lamport's own use is [mutual exclusion](/mutual-exclusion-problem/): each process sends a timestamped request to all, and the request with the smallest $(C, i)$ goes first. [Total order broadcast](/total-order-broadcast/) can use the same idea, and [last-writer-wins](/last-writer-wins/) registers often use $(C, i)$ to pick the winning write. Do not use them to detect conflicts or concurrency. Use [vector clocks](/vector-clocks/) or [version vectors](/version-vectors/) for that.

## Pitfalls

- **Reading the converse.** $C(a) < C(b)$ does not mean that $a$ came first or caused $b$. In the example, $C(b) < C(e)$ and $b \parallel e$.
- **Sending the old value.** If a process attaches $C_i$ to the message before line L4 adds 1, the receiver can get the same timestamp as the send, and the clock condition fails.
- **Forgetting the +1 on receive.** The rule $C_i \leftarrow \max(C_i, T_m)$ alone can give a receive the same timestamp as its send.
- **Restart from 0.** A process that crashes and recovers must not reuse old timestamps. Store the clock on disk, or restart above each value that it may have sent.
- **The order is final only later.** A process cannot know from its own timestamp that no other process has an event with a smaller pair $(C, i)$. To act on the total order, it must hear from every process, as Lamport's mutual exclusion algorithm does over FIFO channels.
- **Bias of the tie-break.** Equal timestamps always go to the process with the smaller index. The total order also can differ from real-time order for concurrent events, which Lamport calls anomalous behavior.

## Implementations

## History

Leslie Lamport published the algorithm in 1978 in "Time, clocks, and the ordering of events in a distributed system". The same paper defines happened-before, states the clock condition, builds the total order, uses it for a mutual exclusion algorithm, and then adds physical clocks with a bound on their drift. Fidge and Mattern later extended the single counter to a vector of counters that captures happened-before exactly.

## References
