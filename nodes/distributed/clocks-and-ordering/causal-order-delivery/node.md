---
tag: 8W013Z
kind: problem
slug: causal-order-delivery
name: Causal order delivery
aliases:
- causal multicast
area: distributed/clocks-and-ordering
level: core
summary: Deliver messages so that no message is delivered before a message whose sending happened before its own. Stated for broadcasts, for multicast groups and for point-to-point messages.
prereqs: [causal-ordering, broadcast-problem, asynchronous-model]
see_also: [causal-broadcast, causal-ordering, fifo-delivery, total-order-broadcast, matrix-clocks, vector-clocks, causal-consistency, op-based-crdt]
sources:
  - paper: doi:10.1145/128738.128742
    title: Kenneth Birman, André Schiper and Pat Stephenson, Lightweight causal and atomic group multicast, ACM Transactions on Computer Systems 9(3), 1991
    locator: pages 272 to 314 (the CBCAST protocol with vector timestamps)
  - paper: doi:10.1007/3-540-51687-5_45
    title: André Schiper, Jorge Eggli and Alain Sandoz, A new algorithm to implement causal ordering, Distributed Algorithms (WDAG 1989), LNCS 392, Springer, 1989
    locator: the algorithm for point-to-point messages
  - paper: doi:10.1016/0020-0190(91)90008-6
    title: Michel Raynal, André Schiper and Sam Toueg, The causal ordering abstraction and a simple way to implement it, Information Processing Letters 39(6), 1991
    locator: the definition and the algorithm with a matrix of counters on each message
  - paper: "Vassos Hadzilacos and Sam Toueg, A modular approach to fault-tolerant broadcasts and related problems, Technical Report TR 94-1425, Cornell University, 1994"
    title: Vassos Hadzilacos and Sam Toueg, A modular approach to fault-tolerant broadcasts and related problems
    locator: causal broadcast, its specification and its reductions to reliable and FIFO broadcast
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 3, Section 3.9 (causal broadcast, with a waiting and a no-waiting algorithm)
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 6 (causal order, the RST and SES algorithms, and an algorithm that sends only necessary dependency information)
---

Causal order delivery is the problem of delivering messages so that [causal ordering](/causal-ordering/) holds: if the sending of $m$ happened before the sending of $m'$, then no process delivers $m'$ before $m$. The network may delay messages in any way, so a process may receive an effect before its cause, and must then either wait or obtain the cause in some other way. For broadcasts the problem is usually stated together with the guarantees of reliable broadcast, and it can be solved in the [asynchronous model](/asynchronous-model/) with crashes, unlike total order broadcast. [Causal broadcast](/causal-broadcast/) is the standard algorithm.

## In plain words

Computers send each other messages over a network that can be slow on some paths and fast on others. A message that answers another message can arrive before the message it answers.

The task is to hand messages to the application in an order where every answer comes after what it answers, and more generally after everything its sender had seen or sent before. Messages that do not depend on each other may be handed over in any order.

Each computer must solve this with local information only. It usually tags every message with a small summary of what the sender had seen. A receiver then holds a message back until it has handed over everything that the summary mentions.

## Definition

**Model.** $n$ processes, any of which may crash, communicate over reliable channels in the [asynchronous model](/asynchronous-model/). A message $m'$ *causally follows* $m$, written $m \to m'$, if the broadcast or send of $m$ [happened before](/happened-before/) the broadcast or send of $m'$.

**Broadcast version.** Processes call $\text{co-broadcast}(m)$, and the service raises $\text{co-deliver}(m)$ at processes. The service must satisfy the properties of reliable broadcast, as in the [broadcast problem](/broadcast-problem/):

- **Validity.** If a correct process broadcasts $m$, it eventually delivers $m$.
- **No duplication and no creation.** Each process delivers each message at most once, and only if some process broadcast it.
- **Agreement.** If a correct process delivers $m$, every correct process eventually delivers $m$.

and also:

- **Causal order.** If $m \to m'$ and a process delivers $m'$, that process has already delivered $m$.

**Point-to-point version.** Processes send messages to single destinations. If $m \to m'$ and both are sent to the same process $q$, then $q$ delivers $m$ before $m'$. Liveness asks that every message sent between correct processes is delivered.

## Variants

- **Uniform causal broadcast.** Agreement holds for all processes that deliver, including those that crash later.
- **Multicast to groups.** Each message goes to one group, and groups may overlap. Causal order is required at every process that receives both messages.
- **Causal order without reliability.** Only the safety property is required, which allows a lost cause to block its effects forever.
- **Causal total order.** Add the condition that all processes deliver in the same order. This contains total order broadcast and so needs consensus.
- **Point-to-point causal order.** The version above, with FIFO channels as the special case of one sender.

## Examples

**Overtaking.** $p_1$ broadcasts $m_1$. $p_2$ delivers $m_1$ and then broadcasts $m_2$, so $m_1 \to m_2$. The link from $p_1$ to $p_3$ is slow, and $p_3$ receives $m_2$ first. FIFO order allows $p_3$ to deliver $m_2$ at once, because the senders differ. Causal order forbids it. With vector timestamps, $m_1$ carries $(1,0,0)$ and $m_2$ carries $(1,1,0)$. $p_3$ has delivered nothing, so entry 1 shows a missing cause, and $p_3$ holds $m_2$ until $m_1$ arrives. The tests of [causal broadcast](/causal-broadcast/) run this case.

**No constraint.** If $p_1$ and $p_2$ broadcast $m_1$ and $m_2$ without delivering each other's message, the messages are concurrent and every process may deliver them in either order.

**Point to point.** $p_1$ sends $m_1$ to $p_3$ and then sends $m$ to $p_2$. $p_2$ receives $m$ and sends $m_2$ to $p_3$. Then $m_1 \to m_2$ through $m$, both go to $p_3$, and $p_3$ must deliver $m_1$ first. A FIFO channel does not help, since $m_1$ and $m_2$ come over different channels.

## Known algorithms

| algorithm | messages | tag on each message | idea |
|---|---|---|---|
| [Causal broadcast](/causal-broadcast/) (Birman, Schiper and Stephenson) | broadcast | $n$ integers | deliver when the vector of delivered counts covers the message vector, except one more from the sender |
| No-waiting causal broadcast (Cachin, Guerraoui and Rodrigues) | broadcast | the messages of the causal past | deliver the carried past first, then the message, so no process waits |
| Raynal, Schiper and Toueg | point-to-point | $n \times n$ integers | a [matrix](/matrix-clocks/) of sent counts; deliver when every message to this process that is known to be sent has been delivered |
| Schiper, Eggli and Sandoz | point-to-point | up to $n - 1$ pairs (destination, vector) and a vector | each message carries, per destination, the latest vector it must wait for |
| Kshemkalyani and Singhal | point-to-point | only dependency information that may still be needed | prunes the information of the matrix and SES approaches |

A vector of $n$ integers suffices for broadcasts because each process delivers every message, so the delivered counts per sender describe its whole past. Point-to-point algorithms need more, because a process must know which messages were sent to it, not only how many messages each process sent.

## Bounds

- **Solvable with crashes.** Causal broadcast can be built in the asynchronous model with any number of crash failures. The correctness proof of [causal broadcast](/causal-broadcast/) covers runs with crashes. This differs from [total order broadcast](/total-order-broadcast/), which is equivalent to consensus and so cannot be solved deterministically in this model when a crash can occur.
- **Either wait or carry the past.** In the overtaking example, $p_3$ cannot deliver $m_2$ when it arrives unless it can deliver $m_1$ first. If $m_2$ does not carry $m_1$, $p_3$ must wait, and since $m_1$ can be delayed for any finite time, so can $m_2$. This is a short argument from the example, not a cited theorem.
- **Tag size.** This page proves no lower bound on the size of tags. The bound of $n$ entries by Charron-Bost, proved on [Lamport's clock condition](/lamport-clock-condition/), is about timestamps that capture happened-before exactly, which is more than causal delivery needs. It does not transfer directly.
- **Work.** The vector algorithm does $O(n)$ work per test of a buffered message. Its other costs are on the [causal broadcast](/causal-broadcast/) page.

## Reductions

- **From reliable broadcast.** Causal broadcast is reliable broadcast plus vector timestamps and a hold-back buffer, as in [causal broadcast](/causal-broadcast/).
- **From FIFO broadcast.** Causal order is FIFO order plus local order (proved on [causal ordering](/causal-ordering/)). So FIFO broadcast in which each message carries the messages its sender delivered since its last broadcast gives causal broadcast. [FIFO delivery](/fifo-delivery/) is the weaker problem.
- **To causal consistency.** Delivering updates in causal order to replicas gives [causal consistency](/causal-consistency/) for reads at each replica.
- **With total order.** Adding the same delivery order at all processes gives causal total order broadcast, which needs consensus.

## Applications

- **Group communication systems.** Isis provided causal multicast with CBCAST.
- **[Operation-based CRDTs](/op-based-crdt/).** Many need causal delivery of operations, so that, for example, a remove is applied after the add it removes.
- **Collaborative editing and chat.** Replies, edits and acknowledgments are shown after what they refer to.
- **Distributed debugging and monitoring.** Observers that receive events in causal order see a consistent picture of the run.

## References
