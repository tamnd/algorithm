---
tag: MSDFTD
kind: concept
slug: fifo-ordering
name: FIFO ordering
aliases:
- FIFO order
- per-sender order
area: distributed/clocks-and-ordering
level: intro
summary: The property that messages from one sender are delivered in the order they were sent. It says nothing about messages from different senders, so it is weaker than causal order.
prereqs: [happened-before]
see_also: [fifo-delivery, fifo-broadcast, causal-ordering, sliding-window-protocol, total-order-broadcast, lamport-clocks, chandy-lamport-snapshot, happened-before]
sources:
  - paper: "Vassos Hadzilacos and Sam Toueg, A modular approach to fault-tolerant broadcasts and related problems, Technical Report TR 94-1425, Cornell University, 1994"
    title: Vassos Hadzilacos and Sam Toueg, A modular approach to fault-tolerant broadcasts and related problems
    locator: the definition of FIFO order and FIFO broadcast
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 3, Section 3.9 (FIFO order and causal order for broadcasts)
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 6 (message ordering paradigms, FIFO executions)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 22 (data link protocols that give FIFO delivery over channels that may reorder or lose messages)
  - paper: doi:10.1145/359545.359563
    title: Leslie Lamport, Time, clocks, and the ordering of events in a distributed system, Communications of the ACM 21(7), 1978
    locator: pages 558 to 565, section Ordering the Events Totally (the assumption that messages from one process to another are received in the order sent)
---

FIFO ordering is a property of message delivery: if a process sends $m$ before $m'$, then no process delivers $m'$ before it has delivered $m$. The order is per sender. Messages from different senders may be delivered in any order, even when one caused the other, so FIFO ordering is weaker than [causal ordering](/causal-ordering/). This page is about the property. The task of providing it is [FIFO delivery](/fifo-delivery/), and [FIFO broadcast](/fifo-broadcast/) is an algorithm that solves it for broadcasts.

## In plain words

FIFO means first in, first out. If one person sends two letters, the receiver opens them in the order they were written. That is the whole rule.

The rule does not compare letters from different people. If Alice writes to Bob and Carol, and Bob then replies to Carol, Carol may read Bob's reply before Alice's letter. FIFO ordering allows that, because the two letters have different senders.

Networks often do not keep order by themselves: packets take different routes, and lost packets are sent again. A receiver can restore FIFO order with a sequence number per sender. It holds back any message that arrives before an earlier one from the same sender.

## The idea

**Definition for broadcasts.** For messages $m \ne m'$ with the same sender $p$, if $p$ broadcasts $m$ before $m'$, then any process that delivers $m'$ has already delivered $m$.

**Definition for channels.** A channel from $p$ to $q$ is FIFO if $q$ receives the messages that $p$ sends to $q$ in the order that $p$ sent them. With loss allowed, the received messages form a subsequence of the sent ones. A FIFO channel gives FIFO order for one pair of processes, and FIFO order for broadcasts asks for it at every receiver.

**What it does and does not say.**

- It is a safety property. It does not require any message to be delivered, so it is usually combined with a reliability property, such as in reliable broadcast or a reliable channel.
- A process that misses $m$ must also never deliver $m'$, or must wait for $m$. So with loss, FIFO order makes later messages wait for retransmission. This is the head-of-line blocking of TCP.
- It orders messages by the local order of their sends at one process. In terms of [happened-before](/happened-before/), it keeps the pairs of sends that are ordered by local order alone, and it may break pairs that are linked through other processes.

**Relation to other orders.** Causal order is FIFO order plus local order: if a process delivers $m$ and then broadcasts $m'$, everyone delivers $m$ first. The proof is on the [causal ordering](/causal-ordering/) page. So causal order implies FIFO order, and the converse fails. FIFO order and total order are independent: a total order may reverse two messages of one sender, and FIFO order lets two processes deliver messages of different senders in different orders.

**Three terms.** FIFO ordering is the property. [FIFO delivery](/fifo-delivery/) is the problem of providing it, for broadcasts or for a channel. [FIFO broadcast](/fifo-broadcast/) is the algorithm that adds a sequence number per sender to reliable broadcast.

## Examples

Each example has three processes. $B(m)$ is a broadcast and $D(m)$ a delivery. A script checked each claim below from the event lists.

**FIFO order broken.** $P_1$: $B(m_1)$, $B(m_2)$, $D(m_1)$, $D(m_2)$. $P_2$: $D(m_2)$, $D(m_1)$. $P_3$: $D(m_1)$, $D(m_2)$. $P_2$ delivers the second message of $P_1$ first.

**FIFO but not causal.** $P_1$: $B(m_1)$, $D(m_1)$, $D(m_2)$. $P_2$: $D(m_1)$, $B(m_2)$, $D(m_2)$. $P_3$: $D(m_2)$, $D(m_1)$. The messages have different senders, so FIFO order holds. But $P_2$ sent $m_2$ after it delivered $m_1$, and $P_3$ delivers them in the other order, so causal order fails.

**Sequence numbers.** $P_1$ numbers its broadcasts $1, 2, 3$. If $P_2$ receives them as $3, 2, 1$, it holds $3$ and $2$, delivers $1$ when it arrives, and then delivers $2$ and $3$. The tests of [FIFO broadcast](/fifo-broadcast/) run this case.

## Where it is used

- **Reliable byte streams.** TCP delivers bytes in the order sent by numbering them. The [sliding window protocol](/sliding-window-protocol/), [go-back-N](/go-back-n/) and [selective repeat](/selective-repeat/) give FIFO delivery over channels that lose and reorder packets.
- **Algorithms that assume FIFO channels.** Lamport's mutual exclusion algorithm of 1978 assumes it. The [Chandy-Lamport snapshot](/chandy-lamport-snapshot/) needs it, so that the marker separates messages sent before the snapshot from those sent after. The [Lai-Yang snapshot](/lai-yang-snapshot/) works without it.
- **Replication of a log from one leader.** When one process sends all updates, FIFO order from that process is enough to apply them in the same order everywhere, which is why primary-backup schemes often need nothing stronger.
- **Building stronger orders.** Causal broadcast can be built from FIFO broadcast by adding local order, and total order broadcast with a fixed sequencer uses FIFO channels from the sequencer.

## References
