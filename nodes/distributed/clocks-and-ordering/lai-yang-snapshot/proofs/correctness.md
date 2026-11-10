---
title: The Lai-Yang colouring records the global state of a consistent cut on non-FIFO channels
proves: [correctness]
status: full
---

We use the pseudocode and the model of the page: a strongly connected graph, reliable channels with no FIFO order, no failures, and one initiator that calls RECORD. For a process $p$, let $\mathrm{rec}(p)$ be the moment at which $p$ runs line L3. RECORD is an atomic step. Let $C$ be the cut made of the events of each process before $\mathrm{rec}(p)$. We count as events of the cut only the application events; the red messages without content of line L3 carry no state.

**Lemma 1 (colours).** A message $m$ sent by $p_i$ is white if and only if $p_i$ sent it before $\mathrm{rec}(p_i)$, that is, if its send is in $C$.

*Proof.* Line L1 gives $m$ the colour of $p_i$ at the send. $p_i$ is white before $\mathrm{rec}(p_i)$ and red from then on, since line L3 is the only line that changes a colour and it runs once per process (line L4 guards it, and the initiator records once). $\square$

**Lemma 2 (every process records).** Every process eventually records.

*Proof.* The initiator records. When a process $p$ records, it sends a red message on every outgoing channel $(p, q)$. That message arrives, since channels are reliable, and by line L4 $q$ records before it takes it, if it has not already. The graph is strongly connected, so by induction on the length of a path from the initiator, every process records. $\square$

**Theorem 1 (consistency).** $C$ is a consistent cut.

*Proof.* By Lemma 1 of the page on [consistent cuts](/consistent-cut/), it is enough to show that every receive in $C$ has its send in $C$. Let $p_j$ receive $m$ from $p_i$ before $\mathrm{rec}(p_j)$, and suppose that the send of $m$ is not in $C$. By Lemma 1, $m$ is red. When $m$ arrived, $p_j$ was white, since the receive is before $\mathrm{rec}(p_j)$. So line L4 ran RECORD before $p_j$ took $m$, and the receive is after $\mathrm{rec}(p_j)$, a contradiction. $\square$

**Theorem 2 (channel states).** For each channel $(q, p)$, line L6 returns exactly the set of messages that $q$ sent to $p$ in $C$ and that $p$ did not receive in $C$.

*Proof.* By line L2 and Lemma 1, WhiteSent$(q, p)$ is the set of messages that $q$ sent to $p$ in $C$. By line L5, the saved WhiteRecd$(q, p)$ is the set of white messages from $q$ that $p$ received while white, that is in $C$. Every message that $p$ receives from $q$ in $C$ was sent in $C$ by Theorem 1, so it is white. So the saved WhiteRecd$(q, p)$ is the set of messages from $q$ received in $C$, all of which are in WhiteSent$(q, p)$. The difference is the set of messages sent in $C$ and not received in $C$. $\square$

**Theorem 3 (the result is a global snapshot).** The saved local states and the channel states of line L6 form the global state $S^\ast$ of the consistent cut $C$. So $S^\ast$ is reachable from the state at the start, and the state at the end is reachable from $S^\ast$.

*Proof.* Line L3 saves the state of each process after its events in $C$. Theorem 2 gives the channel states of $C$, and Theorem 1 says that $C$ is consistent. The reachability claims are the theorem on the page on [global snapshots](/global-snapshot/). $\square$

**No FIFO order is used.** The proofs use only the colour on each message. A red message may overtake a white one on the same channel, as in the second example of the page: the white one then arrives at a red receiver, line L5 does not add it, and line L6 counts it in the channel. A white message may overtake a red one: it then arrives either at a white receiver, which adds it, or at a red one, and in both cases Theorem 2 still holds.

**Control messages.** Each process sends one red message without content on each outgoing channel, so $e$ such messages in all. $\square$
