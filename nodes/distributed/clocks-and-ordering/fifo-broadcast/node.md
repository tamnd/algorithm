---
tag: 271TJB
kind: algorithm
slug: fifo-broadcast
name: FIFO broadcast
aliases:
- FIFO multicast
area: distributed/clocks-and-ordering
level: core
summary: Reliable broadcast plus one sequence number per sender. Each receiver delivers the messages of each sender in sending order and buffers those that arrive early.
solves: [fifo-delivery]
model: asynchronous-model
complexity:
  vars: {n: the number of processes, b: the number of buffered messages}
  time: {worst: O(b), best: O(1)}
  space: {extra: O(n + b)}
properties: {deterministic: true, recursive: false}
history:
  year: 1994
  people: [Vassos Hadzilacos, Sam Toueg]
  note: Hadzilacos and Toueg defined FIFO broadcast as reliable broadcast plus FIFO order in their modular account of fault-tolerant broadcasts.
prereqs: [fifo-ordering, broadcast-problem]
see_also: [fifo-delivery, fifo-ordering, causal-broadcast, total-order-broadcast, causal-ordering, sliding-window-protocol, bracha-reliable-broadcast, flooding]
sources:
  - paper: "Vassos Hadzilacos and Sam Toueg, A modular approach to fault-tolerant broadcasts and related problems, Technical Report TR 94-1425, Cornell University, 1994"
    title: Vassos Hadzilacos and Sam Toueg, A modular approach to fault-tolerant broadcasts and related problems, Cornell TR 94-1425, 1994
    locator: the specification of FIFO broadcast and its construction from reliable broadcast
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Section 3.9 (FIFO and causal broadcast)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 8 (broadcast and multicast, ordering properties)
---

FIFO broadcast is reliable broadcast with one more promise: the messages of each sender are delivered in the order in which that sender broadcast them. The usual algorithm adds a sequence number to each message and makes each receiver deliver the messages of each sender in the order of their numbers. Messages of different senders are not ordered against each other. This page is the algorithm. The property is [FIFO ordering](/fifo-ordering/), and the problem it solves is [FIFO delivery](/fifo-delivery/).

## In plain words

Each sender numbers its messages 1, 2, 3 and so on. A receiver keeps a note, for each sender, of the next number it expects. When a message arrives with that number, the receiver shows it and moves the note on. When a message arrives too early, for example number 3 while it expects 2, the receiver keeps it aside. As soon as number 2 arrives, it shows 2 and then 3.

This keeps each sender's messages in order. It says nothing about messages from two different senders. A reply from one person can still appear before the question from another person that it answers. To prevent that, use causal broadcast.

## The problem

There are $n$ processes in the [asynchronous model](/asynchronous-model/), and processes can crash. The algorithm must satisfy:

- **Validity.** If a correct process broadcasts $m$, every correct process eventually delivers $m$.
- **Agreement.** If a correct process delivers $m$, every correct process eventually delivers $m$.
- **Integrity.** Each message is delivered at most once per process, and only if it was broadcast.
- **FIFO order.** If a process broadcasts $m$ before $m'$, no process delivers $m'$ unless it has already delivered $m$.

## The algorithm

Messages travel through a reliable broadcast layer (RB), for example eager [flooding](/flooding/), which may reorder them.

```pseudo id=main
init at p_i
L1  lsn ← 0;  next ← [1, …, 1];  pending ← ∅

FIFO-BROADCAST(m) at p_i
L2  lsn ← lsn + 1
L3  RB-BROADCAST(m, lsn)
L4  FIFO-DELIVER(m);  next[i] ← next[i] + 1

upon RB-DELIVER(m, s) from p_j with j ≠ i
L5  pending ← pending ∪ {(j, s, m)}
L6  while pending has an entry (j, next[j], m') do
L7      remove it;  FIFO-DELIVER(m');  next[j] ← next[j] + 1
```

Only the sender of the new message can have become ready, so line L6 checks only that sender.

## Example

Process $p_1$ broadcasts $a$, $b$ and $c$ with numbers $1$, $2$ and $3$. At $p_2$ they arrive as $c$, $b$, $a$.

| arrival at $p_2$ | $next[1]$ before | action | delivered so far |
|---|---|---|---|
| $c$, number 3 | 1 | buffer | none |
| $b$, number 2 | 1 | buffer | none |
| $a$, number 1 | 1 | deliver $a$, then $b$, then $c$ | $a, b, c$ |

**FIFO order does not give causal order.** Process $p_1$ broadcasts $m_1$. Process $p_2$ delivers $m_1$ and then broadcasts $m_2$, so the broadcast of $m_1$ [happened before](/happened-before/) the broadcast of $m_2$. At $p_3$, $m_2$ arrives first. It is message number 1 of $p_2$, so $p_3$ delivers it at once, and delivers $m_1$ later. All four properties hold, but $p_3$ sees the effect before the cause. [Causal broadcast](/causal-broadcast/) would hold $m_2$ back.

## Correctness

By induction, each process has always delivered exactly the messages of each sender $p_k$ with numbers $1$ up to $next[k] - 1$, in order. This gives FIFO order and integrity. If a correct process delivers the $s$-th message of $p_k$, it delivered the earlier ones too, and each of them came from the reliable broadcast layer or from itself. So reliable agreement brings all of them to every correct process, and there the loop of lines L6 and L7 delivers them in order. Validity follows, because the sender delivers its own message at once. The full proof is below.

## Complexity

Each message carries one integer. With a hash map keyed by sender and number, each arrival costs $O(1)$ expected time, plus $O(1)$ per message that it releases. One arrival can release all $b$ buffered messages, but each message is released once, so the cost per message is $O(1)$ on average. The state is the vector $next$ of $n$ integers plus the buffer of $b$ early messages. The buffer can grow without bound if one early message of a sender is delayed for a long time.

## Properties

- **Deterministic.** The delivery order depends only on the arrival order.
- **No extra messages.** The FIFO layer adds one integer to each message and no messages.
- **Weaker than causal broadcast.** It is the per-sender part of [causal broadcast](/causal-broadcast/). Messages from different senders can be delivered in any order.
- **Not total order.** Two processes can deliver messages of different senders in different orders. [Total order broadcast](/total-order-broadcast/) and FIFO broadcast are incomparable: a total order can still break the order of one sender, unless both are required.

## Variants and improvements

- **FIFO over point-to-point links.** The same sequence numbers make one channel FIFO. Protocols such as the [sliding window protocol](/sliding-window-protocol/) add acknowledgments and retransmission so that the channel is also reliable. See [FIFO delivery](/fifo-delivery/).
- **[Causal broadcast](/causal-broadcast/).** Replaces the sequence number by a vector timestamp, so that a message also waits for the messages of other senders that its sender had seen.
- **FIFO total order broadcast.** Total order broadcast that also respects each sender's order, as needed by state machine replication when one client sends several commands.
- **Uniform FIFO broadcast.** Built the same way on top of uniform reliable broadcast.

## When to use it

Use FIFO broadcast when each sender's messages describe a sequence of changes that only that sender makes, such as updates to data that the sender owns, or a stream of events from one source. It is cheaper than [causal broadcast](/causal-broadcast/), because each message carries one integer and not a vector. When messages from one sender react to messages from another, use causal broadcast instead.

## Pitfalls

- **Assuming causal order.** FIFO broadcast allows a reply to arrive before the question, as in the example. This is the most common mistake.
- **Gaps from crashed senders.** If a sender crashes after only some processes received its message $s$, and no correct process received it, then all later messages of that sender wait forever. Reliable broadcast below prevents this for messages that any correct process received.
- **Restarting a sender.** A process that restarts with $lsn = 0$ reuses numbers, and receivers drop or misorder its new messages. The sender must store $lsn$ or start a new incarnation.
- **Unbounded buffers.** Early messages wait in the buffer. A slow or lost message from one sender holds back all later messages of that sender.

## Implementations

## History

FIFO order on a single channel is as old as computer networks: sequence numbers in link and transport protocols put packets back in order. Vassos Hadzilacos and Sam Toueg gave the modular definitions in 1994: FIFO broadcast is reliable broadcast plus FIFO order, causal broadcast is reliable broadcast plus causal order, and atomic broadcast is reliable broadcast plus total order. Cachin, Guerraoui and Rodrigues present the same hierarchy with algorithms.

## References
