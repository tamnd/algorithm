---
tag: Y3V5CE
kind: algorithm
slug: causal-broadcast
name: Causal broadcast
aliases:
- Birman-Schiper-Stephenson broadcast
- BSS causal broadcast
area: distributed/clocks-and-ordering
level: core
summary: Reliable broadcast plus vector timestamps. A receiver buffers each message until it has delivered every message that the sender had delivered, so causes are delivered before effects.
solves: [causal-order-delivery]
model: asynchronous-model
complexity:
  vars: {n: the number of processes, b: the number of buffered messages}
  time: {worst: O(n b^2)}
  space: {extra: O(n b)}
properties: {deterministic: true, recursive: false}
history:
  year: 1991
  people: [Kenneth Birman, André Schiper, Pat Stephenson]
  note: Birman, Schiper and Stephenson described the vector-timestamp delivery rule for causal multicast in ACM TOCS in 1991.
prereqs: [vector-clocks, causal-ordering, broadcast-problem]
see_also: [fifo-broadcast, causal-order-delivery, causal-ordering, total-order-broadcast, vector-clocks, causal-consistency, op-based-crdt, bracha-reliable-broadcast]
sources:
  - paper: doi:10.1145/128738.128742
    title: Kenneth Birman, André Schiper and Pat Stephenson, Lightweight causal and atomic group multicast, ACM Transactions on Computer Systems 9(3), 1991
    locator: pages 272 to 314, the CBCAST protocol and its vector timestamp delivery rule
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Section 3.9 (causal broadcast, the no-waiting and the waiting algorithms)
  - paper: "Vassos Hadzilacos and Sam Toueg, A modular approach to fault-tolerant broadcasts and related problems, Technical Report TR 94-1425, Cornell University, 1994"
    title: Vassos Hadzilacos and Sam Toueg, A modular approach to fault-tolerant broadcasts and related problems, Cornell TR 94-1425, 1994
    locator: the specification of causal broadcast and its construction from reliable broadcast
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 6, Section 6.5 (causal order)
---

Causal broadcast delivers broadcast messages so that a message is never delivered before a message that could have caused it. The algorithm of Birman, Schiper and Stephenson puts a [vector timestamp](/vector-clocks/) on each message and runs on top of a reliable broadcast. A receiver holds back a message until it has delivered every message that the sender had delivered when it sent it. This page is the algorithm. The property it gives is [causal ordering](/causal-ordering/), and the problem it solves is [causal order delivery](/causal-order-delivery/), which also has a point-to-point version.

## In plain words

In a group chat, Alice asks a question and Bob answers it. Carol must never see Bob's answer before Alice's question, even if the network delivers them in the wrong order.

Every process counts how many messages it has shown from each sender. A new message carries the sender's counts, with its own count raised by one. When a message arrives, the receiver asks two questions. Is this the next message from that sender? Have I shown everything that the sender had shown when it wrote this? If both answers are yes, the receiver shows the message and updates its counts. If not, it keeps the message in a waiting room and checks again each time something new is shown.

Messages that do not depend on each other are not held back; they can appear in any order.

## The problem

There are $n$ processes in the [asynchronous model](/asynchronous-model/), and processes can crash. Each process can broadcast messages, and must deliver them so that:

- **Validity.** If a correct process broadcasts $m$, every correct process eventually delivers $m$.
- **Agreement.** If a correct process delivers $m$, every correct process eventually delivers $m$.
- **Integrity.** Each message is delivered at most once per process, and only if it was broadcast.
- **Causal order.** If the broadcast of $m$ [happened before](/happened-before/) the broadcast of $m'$, no process delivers $m'$ before $m$.

The first three properties are those of reliable broadcast. Causal order is stronger than the per-sender order of [FIFO broadcast](/fifo-broadcast/), and it does not give one order to all processes, as [total order broadcast](/total-order-broadcast/) does.

## The algorithm

Each process $p_i$ keeps a vector $VC$ in which $VC[k]$ counts the messages from $p_k$ that $p_i$ has delivered. Messages travel through a reliable broadcast layer (RB).

```pseudo id=main
init at p_i
L1  VC ← [0, …, 0];  pending ← ∅

CO-BROADCAST(m) at p_i
L2  VT ← VC;  VT[i] ← VT[i] + 1
L3  RB-BROADCAST(m, VT)
L4  CO-DELIVER(m);  VC[i] ← VC[i] + 1

upon RB-DELIVER(m, VT) from p_j with j ≠ i
L5  pending ← pending ∪ {(m, VT, j)}
L6  while some (m', VT', k) in pending has VT'[k] = VC[k] + 1 and VT'[x] ≤ VC[x] for all x ≠ k do
L7      remove it from pending;  CO-DELIVER(m');  VC[k] ← VC[k] + 1
```

Line L6 states the delivery rule. The first clause says that $m'$ is the next message from $p_k$, which gives FIFO order per sender. The second clause says that the receiver has delivered every message from other senders that $p_k$ had delivered before it broadcast $m'$.

## Example

Process $p_1$ broadcasts $m_1$ with $VT = (1, 0, 0)$. Process $p_2$ delivers $m_1$, so $VC_2 = (1, 0, 0)$, and then broadcasts the reply $m_2$ with $VT = (1, 1, 0)$. So $m_1 \to m_2$. The network is slow on the link from $p_1$ to $p_3$.

| step at $p_3$ | $VC_3$ before | test of line L6 | action |
|---|---|---|---|
| receive $m_2$, $VT = (1, 1, 0)$ from $p_2$ | $(0, 0, 0)$ | $VT[2] = 1 = 0 + 1$, but $VT[1] = 1 > 0$ | buffer $m_2$ |
| receive $m_1$, $VT = (1, 0, 0)$ from $p_1$ | $(0, 0, 0)$ | $VT[1] = 1 = 0 + 1$ | deliver $m_1$ |
| loop again | $(1, 0, 0)$ | for $m_2$: $VT[2] = 1$, $VT[1] = 1 \le 1$ | deliver $m_2$ |

At the end, $VC_3 = (1, 1, 0)$. If instead $p_1$ and $p_2$ broadcast $a = (1,0,0)$ and $b = (0,1,0)$ without delivering each other's message, $p_3$ delivers each one as soon as it arrives, in either order.

## Correctness

The entry $VC[k]$ counts the deliveries from $p_k$, and these are always the first $VC[k]$ messages of $p_k$, because the first clause admits only the next one. So $VT(m)[k]$ says how many messages of $p_k$ the sender of $m$ had delivered. If $m \to m'$, either $m$ is an earlier message of the same sender, and the first clause makes the receiver deliver it first, or the sender of $m'$ had delivered $m$, and the second clause makes the receiver deliver it first. Chains follow by induction.

For liveness, once a correct receiver has delivered all the causal predecessors of a buffered message, both clauses hold, and the loop of line L6 delivers it. Reliable broadcast makes every correct process receive a message and all its predecessors, so agreement and validity carry over from the layer below. The full proof is below.

## Complexity

Each message carries $n$ integers. One test of line L6 takes $O(n)$ time. With $b$ buffered messages, a scan of the buffer takes $O(n b)$, and one arrival can release a chain of up to $b$ messages, so the simple loop takes $O(n b^2)$ time in the worst case. Indexing the buffer by sender and sequence number reduces the work per released message. The buffer holds $O(n b)$ integers. In a run where messages arrive in causal order, nothing waits, and each message costs $O(n)$.

## Properties

- **Deterministic.** The delivery order depends only on the arrival order.
- **No extra messages.** The causal layer adds no messages; it adds $n$ integers to each message and a delay at the receiver.
- **Concurrent messages are not delayed.** Two messages that are not causally related can be delivered in different orders at different processes.
- **Built on reliable broadcast.** With a uniform reliable broadcast below, the same rule gives uniform causal broadcast.

## Variants and improvements

- **No-waiting causal broadcast.** Each message carries the list of all messages in its causal past, and a receiver delivers that past first. No buffer is needed, but messages grow without bound unless the past is pruned. Cachin, Guerraoui and Rodrigues describe both forms.
- **Point-to-point causal order.** For unicast messages, vectors are not enough, and algorithms such as Raynal, Schiper and Toueg keep an $n \times n$ matrix. See [causal order delivery](/causal-order-delivery/).
- **Smaller timestamps.** Kshemkalyani and Singhal give an algorithm that sends only the necessary dependency information.
- **[FIFO broadcast](/fifo-broadcast/).** Keeping only the first clause of line L6 gives FIFO order, with one sequence number per message.
- **Total order.** Causal broadcast does not make all processes deliver in one order. That needs [total order broadcast](/total-order-broadcast/), which is as hard as consensus.

## When to use it

Use causal broadcast when replies must follow questions, and updates must follow the updates they build on: group chat, collaborative editing, and replicated data with [causal consistency](/causal-consistency/). [Operation-based CRDTs](/op-based-crdt/) often assume causal delivery of operations. It needs no agreement between processes, so it stays available during partitions, unlike total order broadcast. If messages from different senders never depend on each other, [FIFO broadcast](/fifo-broadcast/) is cheaper.

## Pitfalls

- **Messages that never arrive.** If a message is lost for good, every later message that depends on it waits forever. The rule needs reliable broadcast below it, not just best-effort sends.
- **Delivering own messages through the network.** The sender must deliver its own message at once (line L4), or must not count it twice when it comes back.
- **Changing membership.** The vector has one entry per process. Adding or removing processes needs a view change protocol, such as the one in the Isis system.
- **Hidden channels.** Causal order covers only causality through the broadcast messages. If processes also talk through a database or a phone call, those dependencies are invisible.

## Implementations

## History

Kenneth Birman and his colleagues built causal multicast, called CBCAST, into the Isis toolkit in the 1980s. Birman, André Schiper and Pat Stephenson published the vector timestamp version in ACM Transactions on Computer Systems in 1991. Schiper, Eggli and Sandoz had given an algorithm for point-to-point causal order in 1989, and Raynal, Schiper and Toueg gave the matrix algorithm in 1991. Hadzilacos and Toueg gave the modular specification of causal broadcast as reliable broadcast plus causal order in 1994.

## References
