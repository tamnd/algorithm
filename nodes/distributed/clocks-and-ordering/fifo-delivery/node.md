---
tag: M55EWN
kind: problem
slug: fifo-delivery
name: FIFO delivery
area: distributed/clocks-and-ordering
level: core
summary: Deliver the messages of each sender in the order that sender sent them, either to all processes as a broadcast, or over one channel that may lose or reorder packets.
prereqs: [fifo-ordering, broadcast-problem, asynchronous-model]
see_also: [fifo-broadcast, fifo-ordering, causal-order-delivery, sliding-window-protocol, alternating-bit-protocol, go-back-n, selective-repeat, total-order-broadcast]
sources:
  - paper: "Vassos Hadzilacos and Sam Toueg, A modular approach to fault-tolerant broadcasts and related problems, Technical Report TR 94-1425, Cornell University, 1994"
    title: Vassos Hadzilacos and Sam Toueg, A modular approach to fault-tolerant broadcasts and related problems
    locator: the specification of FIFO broadcast and its construction from reliable broadcast
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 3, Section 3.9 (FIFO-order reliable broadcast)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 8 (broadcast services with ordering guarantees)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 22 (data link protocols, including protocols that use sequence numbers and the impossibility results for bounded headers and for crashes)
---

FIFO delivery is the problem of providing [FIFO ordering](/fifo-ordering/): the messages of each sender must be delivered in the order that sender sent them. It has two common forms. In the broadcast form, every process sends to all, and the usual reliability properties of broadcast also hold. In the channel form, one sender and one receiver share a link that may lose, duplicate or reorder packets, which is the data link problem. Both are solved with sequence numbers. The broadcast form is solved by [FIFO broadcast](/fifo-broadcast/), and the channel form by protocols such as the [sliding window protocol](/sliding-window-protocol/).

## In plain words

A sender writes several messages one after another. On the way they can be delayed by different amounts, so they can arrive in a different order. Some can be lost and must be sent again.

The receiver must hand them to the application in the order they were written, with no gaps and no copies. Messages from different senders need not be in any particular order with each other.

The usual solution numbers the messages of each sender $1, 2, 3$, and so on. The receiver keeps, for each sender, the next number it expects. It hands over a message only when its number is the next one, and keeps early arrivals until the gap is filled. On a lossy link, the sender also sends a message again until the receiver acknowledges it.

## Definition

**Broadcast form.** $n$ processes, any of which may crash, communicate over reliable channels in the [asynchronous model](/asynchronous-model/). Processes call $\text{fifo-broadcast}(m)$, and the service raises $\text{fifo-deliver}(m)$. The service must satisfy:

- **Validity, no duplication, no creation and agreement**, as for reliable broadcast in the [broadcast problem](/broadcast-problem/);
- **FIFO order.** If a process broadcasts $m$ before $m'$, then any process that delivers $m'$ has already delivered $m$.

**Channel form.** A sender process $p$ and a receiver process $q$ are joined by a physical channel that may lose, duplicate and reorder packets, but that delivers a packet sent again and again eventually, if $p$ keeps sending it. Packets may also flow from $q$ back to $p$. The protocol must implement a channel whose received messages are exactly the sent messages, each once, in the order sent. Lynch treats this as the data link problem.

## Variants

- **Without reliability.** Only FIFO order is required, so a lost message may block or be skipped. Some definitions allow gaps, so that the delivered messages form a subsequence of the sent ones.
- **Uniform FIFO broadcast.** Agreement holds for all processes that deliver, including those that crash later.
- **FIFO channels with bounded headers.** The packet headers may take only a fixed number of values, as in the [alternating bit protocol](/alternating-bit-protocol/). This is possible when the physical channel does not reorder packets.
- **Stronger orders.** [Causal order delivery](/causal-order-delivery/) adds local order across senders, and [total order broadcast](/total-order-broadcast/) adds one common order.

## Examples

**Reordering repaired.** A sender broadcasts messages numbered $1, 2, 3$, and a receiver gets them as $3, 2, 1$. The receiver expects $1$, so it holds $3$ and $2$. When $1$ arrives, it delivers $1$ and then the held messages $2$ and $3$. The tests of [FIFO broadcast](/fifo-broadcast/) run this case.

**Allowed reordering across senders.** $p_1$ broadcasts $m_1$. $p_2$ delivers $m_1$ and then broadcasts $m_2$. $p_3$ receives $m_2$ first. FIFO delivery lets $p_3$ deliver $m_2$ at once, because $m_2$ is the first message of $p_2$. This breaks causal order, and the tests of FIFO broadcast check it.

**A lossy channel.** With [go-back-N](/go-back-n/) and a window of 3, the sender sends packets $1, 2, 3$, and packet $2$ is lost. The receiver accepts $1$, discards $3$ because it expects $2$, and acknowledges $1$ again. After a timeout the sender sends $2$ and $3$ again. [Selective repeat](/selective-repeat/) would keep $3$ in a buffer and send only $2$ again.

## Known algorithms

| algorithm | form | idea |
|---|---|---|
| [FIFO broadcast](/fifo-broadcast/) | broadcast | reliable broadcast plus a sequence number per sender, and a hold-back buffer at each receiver |
| [Alternating bit protocol](/alternating-bit-protocol/) | channel without reordering | one bit of sequence number, resent until acknowledged |
| [Stop-and-wait](/stop-and-wait/) | channel | one packet in flight at a time |
| [Sliding window protocol](/sliding-window-protocol/) | channel | up to $w$ unacknowledged packets with sequence numbers |
| [Go-back-N](/go-back-n/) | channel | the receiver accepts only in order, and the sender resends the whole window after a loss |
| [Selective repeat](/selective-repeat/) | channel | the receiver buffers out-of-order packets, and the sender resends only lost ones |

## Bounds

- **Solvable with crashes.** FIFO broadcast can be built in the asynchronous model with any number of crash failures. The correctness proof on the [FIFO broadcast](/fifo-broadcast/) page covers runs with crashes.
- **Waiting is needed.** If a later message of a sender arrives first and does not carry the earlier one, the receiver must hold it. Since the earlier message can be delayed for any finite time, the delivery of the later one can be too. This is a short argument, not a cited theorem.
- **Counters.** In the broadcast form, each receiver keeps one counter per sender, so the state is $n$ counters. The counters grow without bound as the run goes on.
- **Bounded headers.** Lynch, Chapter 22, presents impossibility results for the channel form: with bounded headers, FIFO delivery cannot be implemented over physical channels that may reorder packets, and reliable delivery cannot be implemented when processes may crash and lose their state. These results are cited here, not proved.

## Reductions

- **From reliable broadcast.** FIFO broadcast is reliable broadcast plus a sequence number per sender, as in [FIFO broadcast](/fifo-broadcast/).
- **To causal broadcast.** FIFO broadcast in which each message carries the messages that its sender delivered since its last broadcast gives causal broadcast. See [causal order delivery](/causal-order-delivery/).
- **From FIFO channels.** Over FIFO channels, reliable broadcast that relays each message in the order of delivery does not by itself give FIFO broadcast, since a message and a later one of the same sender can reach a process through different relays. A sequence number per sender is still needed.

## Applications

- **Reliable byte streams.** TCP numbers bytes and delivers them in order, which solves the channel form.
- **Snapshots and mutual exclusion.** The [Chandy-Lamport snapshot](/chandy-lamport-snapshot/) and Lamport's 1978 mutual exclusion algorithm assume FIFO channels.
- **Replication from one leader.** When one primary sends all updates, FIFO delivery from it applies them in the same order at every backup.
- **Message queues.** Many queues guarantee order per producer or per partition, which is FIFO delivery per sender.

## References
