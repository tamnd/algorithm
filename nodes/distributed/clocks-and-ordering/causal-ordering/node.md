---
tag: 6BRBAP
kind: concept
slug: causal-ordering
name: Causal ordering
aliases:
- causal order
area: distributed/clocks-and-ordering
level: core
summary: The property that a message is delivered only after every message whose sending happened before its own sending. It implies FIFO order and is independent of total order.
prereqs: [happened-before, fifo-ordering]
see_also: [causal-order-delivery, causal-broadcast, fifo-ordering, happened-before, total-order-broadcast, causal-consistency, vector-clocks, matrix-clocks]
sources:
  - paper: doi:10.1145/128738.128742
    title: Kenneth Birman, André Schiper and Pat Stephenson, Lightweight causal and atomic group multicast, ACM Transactions on Computer Systems 9(3), 1991
    locator: pages 272 to 314 (the causal delivery order for multicasts)
  - paper: "Vassos Hadzilacos and Sam Toueg, A modular approach to fault-tolerant broadcasts and related problems, Technical Report TR 94-1425, Cornell University, 1994"
    title: Vassos Hadzilacos and Sam Toueg, A modular approach to fault-tolerant broadcasts and related problems
    locator: the definitions of FIFO order, local order and causal order for broadcasts
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 3, Section 3.9 (causal broadcast and the causal order property)
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 6 (message ordering paradigms, and the causal order for point-to-point messages)
  - paper: doi:10.1016/0020-0190(91)90008-6
    title: Michel Raynal, André Schiper and Sam Toueg, The causal ordering abstraction and a simple way to implement it, Information Processing Letters 39(6), 1991
    locator: the definition of causal ordering for point-to-point messages
---

Causal ordering is a property of message delivery: if the sending of a message $m$ [happened before](/happened-before/) the sending of a message $m'$, then no process delivers $m'$ before it has delivered $m$. Effects never arrive before their causes. The property is stronger than [FIFO ordering](/fifo-ordering/), which asks this only for messages of one sender, and it is independent of total order. This page is about the property. The task of providing it is [causal order delivery](/causal-order-delivery/), and [causal broadcast](/causal-broadcast/) is an algorithm that solves it.

## In plain words

Alice posts a question to a group. Bob reads it and posts an answer. Carol should never see the answer before the question, because the answer depends on it. Causal ordering is the rule that says so.

The rule is about cause and effect, not about time. If two people post at about the same moment without seeing each other's post, nobody has to see them in the same order. If one person posts twice, the second post may depend on the first, so the rule keeps them in order too.

A network does not give this by itself. Bob's answer may take a fast path to Carol and Alice's question a slow one. So each receiver may have to wait and hold a message back until its causes have arrived.

## The idea

**The order on messages.** A run consists of broadcast events and delivery events. Happened-before is defined on these events as usual, with an edge from the broadcast of a message to each of its deliveries. For messages $m \ne m'$, write $m \to m'$ if the broadcast of $m$ happened before the broadcast of $m'$. There are two direct ways for this to happen:

- **FIFO pair.** The same process broadcasts $m$ and then $m'$.
- **Local order pair.** A process delivers $m$ and then broadcasts $m'$.

**Causal order.** For all messages with $m \to m'$: if a process delivers $m'$, it has already delivered $m$.

**FIFO order** is the same condition for FIFO pairs only, and **local order** is the same condition for local order pairs only.

**Proposition.** Causal order holds if and only if FIFO order and local order both hold.

*Proof.* Causal order implies the other two, because their pairs are causal pairs. For the converse, take $m \to m'$ and a path of happened-before edges from the broadcast of $m$ to the broadcast of $m'$. List the broadcast events on the path in order: $m = x_0, x_1, \ldots, x_k = m'$. Between the broadcast of $x_i$ at process $p$ and the broadcast of $x_{i+1}$, the path cannot cross to another process without a message edge, and a message edge starts at a broadcast. So the path either stays on $p$, which makes $(x_i, x_{i+1})$ a FIFO pair, or takes the edge from the broadcast of $x_i$ to its delivery at some $q$ and then stays on $q$ up to the broadcast of $x_{i+1}$, which makes it a local order pair. Now suppose a process $r$ delivers $m' = x_k$. By FIFO order or local order, $r$ delivered $x_{k-1}$ before it. Repeating the argument, $r$ delivered $x_{k-2}$ before $x_{k-1}$, and so on down to $x_0 = m$. $\square$

Hadzilacos and Toueg state causal order as FIFO order together with local order. It shows where FIFO order falls short: it misses the local order pairs, where one process passes a cause on to another.

**How the orders relate.**

- Causal order implies FIFO order, by the proposition.
- FIFO order does not imply causal order: the first example below has FIFO order but not causal order.
- Causal order and total order are independent. The second example has a total order that is not causal, and the third a causal order that is not total.
- *Causal total order* asks for both, and [total order broadcast](/total-order-broadcast/) often includes it.

**Point-to-point messages.** For messages sent to single receivers, the condition reads: if the send of $m$ happened before the send of $m'$, and both go to the same process, then that process receives $m$ first. FIFO channels are the special case of one sender. Raynal, Schiper and Toueg studied this form, and Kshemkalyani and Singhal place it in a hierarchy between FIFO channels and synchronous order.

**Not to be confused with.**

- **[Happened-before](/happened-before/).** Some authors call the relation $\to$ itself the causal order of events. Here, causal ordering is a property of message delivery that uses that relation.
- **[Causal consistency](/causal-consistency/).** A guarantee for reads and writes on shared data: reads respect the causal order of writes. Causal order delivery of the updates is one way to implement it.
- **[Causal broadcast](/causal-broadcast/)** and **[causal order delivery](/causal-order-delivery/).** The algorithm and the problem, as stated above.

## Examples

Each example has three processes. $B(m)$ is a broadcast and $D(m)$ a delivery. A script checked each of the claims below from the event lists.

**FIFO but not causal.** $P_1$: $B(m_1)$, $D(m_1)$, $D(m_2)$. $P_2$: $D(m_1)$, $B(m_2)$, $D(m_2)$. $P_3$: $D(m_2)$, $D(m_1)$. Here $m_1 \to m_2$ is a local order pair. $P_3$ delivers the answer $m_2$ before the question $m_1$. The two messages have different senders, so FIFO order holds.

**Total but not causal.** $P_1$ broadcasts $m_1$ and then $m_2$, and all three processes deliver $m_2$ and then $m_1$. All processes agree on the order, but it reverses a FIFO pair, so neither FIFO order nor causal order holds.

**Causal but not total.** $P_1$: $B(m_1)$, $D(m_1)$, $D(m_2)$. $P_2$: $B(m_2)$, $D(m_2)$, $D(m_1)$. $P_3$: $D(m_1)$, $D(m_2)$. The two messages are concurrent, so causal order holds in any order. $P_1$ and $P_2$ deliver them in different orders, so the order is not total.

**The running example.** In the run of this area, $P_1$ sends from $a$ to $P_2$, and $P_2$ later sends from $e$ to $P_3$. The send at $a$ happened before the send at $e$, but the two messages go to different processes. So point-to-point causal order places no constraint on this run, while for a broadcast of both messages $P_3$ would have to deliver the first one first.

## Where it is used

- **Group communication.** Isis offered causal multicast through the CBCAST protocol of Birman, Schiper and Stephenson, which [causal broadcast](/causal-broadcast/) describes.
- **Replicated data.** [Operation-based CRDTs](/op-based-crdt/) often assume causal delivery, so that an operation is applied only after the operations it depends on, such as the insert before a delete of the same element.
- **[Causal consistency](/causal-consistency/).** Stores that offer causal consistency deliver or make visible updates in causal order.
- **Chat and social feeds.** A reply is shown only after the post it answers.
- **Implementation.** [Vector clocks](/vector-clocks/) suffice to test the condition for broadcasts, and [matrix clocks](/matrix-clocks/) or lists of dependencies are used for point-to-point messages.

## References
