---
tag: HRAZCB
kind: algorithm
slug: lai-yang-snapshot
name: Lai-Yang snapshot algorithm
aliases:
- Lai-Yang algorithm
- colouring snapshot
area: distributed/clocks-and-ordering
level: advanced
summary: A snapshot for non-FIFO channels. Messages carry the sender's colour, white before recording and red after. A red message makes a white receiver record first.
solves: [global-snapshot]
model: asynchronous-model
complexity:
  vars: {e: the number of channels, W: the number of white messages}
  time: {worst: O(e + W)}
  space: {extra: O(e + W)}
  messages: {worst: e}
properties: {deterministic: true, recursive: false}
history:
  year: 1987
  people: [Ten H. Lai, Tao H. Yang]
  note: Lai and Yang published the colouring algorithm for non-FIFO channels in Information Processing Letters in 1987.
prereqs: [chandy-lamport-snapshot]
see_also: [chandy-lamport-snapshot, global-snapshot, consistent-cut, global-virtual-time, fifo-delivery, termination-detection, checkpointing]
sources:
  - paper: doi:10.1016/0020-0190(87)90125-6
    title: Ten H. Lai and Tao H. Yang, On distributed snapshots, Information Processing Letters 25(3), 1987
    locator: pages 153 to 158 (the colouring rules and the channel state as a difference of histories)
  - paper: doi:10.1006/jpdc.1993.1075
    title: Friedemann Mattern, Efficient algorithms for distributed snapshots and global virtual time approximation, Journal of Parallel and Distributed Computing 18(4), 1993
    locator: pages 423 to 434 (colours with message counters instead of histories, and the use for global virtual time)
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 4 (snapshot algorithms for non-FIFO channels, Lai-Yang and Mattern)
---

The *Lai-Yang snapshot algorithm* records a [global snapshot](/global-snapshot/) when channels may deliver messages out of order. Each process is *white* until it records its state and *red* after. Every message carries the colour of its sender at the time of sending, and a white process that receives a red message records its state before it takes the message. The state of a channel is the set of white messages sent on it minus the white messages received on it before the receiver recorded. Lai and Yang published it in 1987; it needs no FIFO order and no markers on the channels.

## In plain words

In the Chandy-Lamport method, a marker on each channel separates the messages sent before a snapshot from those sent after. If a later message can overtake the marker, the separation fails. Lai and Yang put the separation into every message instead.

Each process starts white. When it takes its snapshot it turns red, and from then on every message it sends is red. If a white process gets a red message, it knows that the sender already took its snapshot, so it takes its own snapshot first, and only then reads the message. Each process also keeps a list of the white messages it sent and received. A white message that was sent but not received before the receiver's snapshot was on its way: it belongs to the channel.

## The problem

**Model.** A strongly connected graph of $n$ processes and $e$ channels. Channels are reliable but not FIFO: a message may overtake any other. Delays are unbounded, as in the [asynchronous model](/asynchronous-model/). Processes do not fail. One process starts the snapshot.

**Goal.** As for every [global snapshot](/global-snapshot/): local states and channel states that form the global state of a [consistent cut](/consistent-cut/), recorded without stopping the application. The algorithm may add one bit to each application message.

## The algorithm

```pseudo id=main
SEND(p, q, m)                                   ▷ p sends application message m to q
L1  colour(m) ← colour(p)
L2  if colour(p) = white then add m to WhiteSent(p, q)
    send m to q

RECORD(p)                                       ▷ the initiator, or the rule of L4
L3  save the local state of p; colour(p) ← red
    for each outgoing channel (p, q): send a red message with no content

RECEIVE(p, q, m)                                ▷ m arrives at p from q
L4  if colour(m) = red and colour(p) = white then RECORD(p)
    deliver m to the application
L5  if colour(m) = white and colour(p) = white then add m to WhiteRecd(q, p)

CHANNEL-STATE(q, p)                             ▷ computed by a collector
L6  return WhiteSent(q, p) − WhiteRecd(q, p) as saved when p recorded
```

Every process sends its local state, its WhiteSent sets and its WhiteRecd sets to a collector, which computes line L6 for each channel.

**The red messages of line L3.** A process records only when it gets a red message. Lai and Yang assume that each process, after it turns red, eventually sends a message on each channel, so that all processes record. The version here sends a red message with no content on each outgoing channel at once, which makes this true for any application; in the bank it is a transfer of 0. These are the only control messages.

## Example

**The run of the Chandy-Lamport page.** Branch $p_0$ holds 100, $p_1$ holds 50. Messages with money take 4 time units, messages without money take 1.

| time | event | record |
|---|---|---|
| 1 | $p_1$, white, sends a white 30 to $p_0$ (L1, L2) | WhiteSent$(1,0) = \{30\}$ |
| 2 | $p_0$ records 100 and turns red (L3); it sends a red 0 to $p_1$ | $LS_0 = 100$ |
| 3 | the red 0 reaches white $p_1$: $p_1$ records 20 first (L4) | $LS_1 = 20$, WhiteRecd$(0,1) = \{\}$ |
| 4 | the red 0 of $p_1$ reaches $p_0$, which is red already | |
| 5 | the white 30 reaches $p_0$, which is red, so L5 does not add it | WhiteRecd$(1,0) = \{\}$ |

Line L6 gives the state of channel $(1, 0)$ as $\{30\} - \{\} = \{30\}$. The record holds $100 + 20 + 30 = 150$.

**Overtaking is harmless.** Both branches hold 100. Messages with money take 1, messages without money take 5, and messages may overtake. $p_0$ records 100 at time 0 and sends a red 0; at time 0.5 it sends 10, which is red, since $p_0$ is red. The 10 overtakes the red 0 and arrives at time 1.5. Because it is red, $p_1$ records 100 first and only then adds the 10. The record holds $100 + 100 = 200$ and is consistent. The same run breaks the [Chandy-Lamport algorithm](/chandy-lamport-snapshot/), which records 110 for $p_1$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Let $C$ be the cut of the events that each process runs before it records. By line L1, a message is red exactly when its sender sent it after recording.

- **Consistency.** Suppose $p_j$ receives $m$ before it records, and $p_i$ sent $m$ after recording. Then $m$ is red, and line L4 makes $p_j$ record before it takes $m$, a contradiction. So every receive in $C$ has its send in $C$.
- **Every process records.** A process that records sends a red message on every outgoing channel, so its neighbours record when it arrives, and so on along every path.
- **Channel states.** WhiteSent$(q, p)$ is the set of messages that $q$ sent to $p$ in $C$. The saved WhiteRecd$(q, p)$ is the set of those messages that $p$ received in $C$, since only white messages are sent in $C$. Their difference is the set sent in $C$ and not received in $C$, which is the channel state of the cut.

No step uses FIFO order. The seeded tests run 60 banks of 2 to 5 branches on channels with random delays, and check that the cut is consistent, that the channel states equal the messages in transit across the cut, and that the money adds up.

## Complexity

Each application message carries one extra bit. The version here sends one red message per channel, $e$ in all; with the assumption of Lai and Yang it sends none. Each process stores the white messages it sends and receives, $O(W)$ in all for $W$ white messages, and the collector computes the differences in $O(e + W)$ time with hashing. The histories are the main cost: they hold every white message since the start of the computation, or since the last snapshot.

## Properties

- **Works on non-FIFO channels.** The colour travels with each message, so overtaking cannot hide which side of the cut a send is on.
- **Few control messages.** None in the original, one per channel here.
- **Piggybacking.** One bit per message, or a snapshot number for repeated snapshots.
- **Channel states are computed, not observed.** No process watches a channel; a collector takes a difference of sets.

## Variants and improvements

- **Counters instead of histories (Mattern 1993).** Each process counts the white messages it sends on each channel. The receiver learns the count and waits until it has received that many white messages; the white messages that arrive after it turned red are the channel state. This replaces the histories with counters.
- **Repeated snapshots.** Use the snapshot number as the colour, so that snapshot $k$ is "red" for the messages sent after recording number $k$.
- **Global virtual time.** Mattern's colouring computes the [global virtual time](/global-virtual-time/) of an optimistic simulation: the minimum over the processes and the white messages in transit.
- **FIFO channels.** With FIFO order, the [Chandy-Lamport algorithm](/chandy-lamport-snapshot/) needs no piggybacking and no histories.

## When to use it

Use it when messages can be reordered, for example with several connections or paths between two processes, with a message broker, or with datagrams over a reliable layer that does not keep order. Use the counter variant when message histories would be too large.

## Pitfalls

- **Processes that never get a red message.** If a process only receives white messages, it never records. Send a red message on each channel, as here, or make sure that the application does.
- **Histories that grow forever.** Without a bound on the time between snapshots, WhiteSent and WhiteRecd grow without limit. Clear them after each snapshot, or use counters.
- **Recording after the message.** Line L4 must run before the message changes the local state. If the process applies a red message and then records, the receive is in the cut and its send is not.
- **Content-free messages in the state.** The red messages of line L3 are sent after recording, so they are never white and never part of a channel state. Messages with no content that are white must still be counted, or left out on both sides of line L6.

## Implementations

## History

Ten H. Lai and Tao H. Yang published the algorithm in Information Processing Letters in 1987 under the title On distributed snapshots. It removed the FIFO assumption of Chandy and Lamport (1985) by moving the cut information from markers into the messages. Friedemann Mattern (1993) replaced the histories with message counters and applied the colouring idea to global virtual time in optimistic simulation.

## References
