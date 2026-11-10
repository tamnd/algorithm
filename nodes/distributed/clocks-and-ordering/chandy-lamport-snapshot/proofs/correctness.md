---
title: The Chandy-Lamport algorithm records the global state of a consistent cut with one marker per channel
proves: [correctness]
status: full
---

We use the pseudocode and the model of the page: a strongly connected directed graph, reliable FIFO channels, no failures, and one initiator that calls RECORD. For a process $p$, let $\mathrm{rec}(p)$ be the moment at which $p$ runs line L1. Let $C$ be the cut made of the events of each process before $\mathrm{rec}(p)$. RECORD is an atomic step: lines L1 and L2 run together, with no application event of $p$ in between.

**Lemma 1 (termination).** Every process records exactly once, every channel carries exactly one marker, and every channel recording stops.

*Proof.* Line L3 guards line L4, and the initiator calls RECORD only if it has not recorded, so each process records at most once. Each RECORD sends one marker on each outgoing channel, so each channel carries at most one marker. Now let $p$ record and let $(p, q)$ be a channel. The marker on it arrives, since channels are reliable, and then $q$ records if it has not already. The graph is strongly connected, so every process is reachable from the initiator, and by induction on the length of a path every process records. So every channel carries exactly one marker, and line L5 stops the recording of each channel when its marker arrives. $\square$

**Lemma 2 (the marker separates).** Let $c = (p_i, p_j)$ be a channel. A message $m$ on $c$ arrives before the marker on $c$ if and only if $p_i$ sent $m$ before $\mathrm{rec}(p_i)$.

*Proof.* $p_i$ sends the marker on $c$ in line L2, at $\mathrm{rec}(p_i)$, before any application message that it sends later. FIFO order keeps the arrival order equal to the sending order. $\square$

**Theorem 1 (consistency).** $C$ is a consistent cut.

*Proof.* By Lemma 1 of the page on [consistent cuts](/consistent-cut/), it is enough to show that every receive in $C$ has its send in $C$. Let $p_j$ receive $m$ from $p_i$ before $\mathrm{rec}(p_j)$, and suppose that $p_i$ sent $m$ after $\mathrm{rec}(p_i)$. By Lemma 2 the marker on $(p_i, p_j)$ arrived before $m$. When it arrived, $p_j$ recorded (line L4) if it had not already. So $\mathrm{rec}(p_j)$ is before the receipt of $m$, a contradiction. $\square$

**Theorem 2 (channel states).** For each channel $c = (p_i, p_j)$, the recorded $State(c)$ is the sequence of messages that $p_i$ sent before $\mathrm{rec}(p_i)$ and $p_j$ received after $\mathrm{rec}(p_j)$, in the order sent.

*Proof.* By lines L2, L5 and L6, $State(c)$ holds the messages that arrive on $c$ after $\mathrm{rec}(p_j)$ and before the marker on $c$, in order of arrival. By Lemma 2, "before the marker" is the same as "sent before $\mathrm{rec}(p_i)$". By FIFO order, arrival order is sending order. If $p_j$ records because of the marker on $c$ itself, then $\mathrm{rec}(p_j)$ is the arrival of that marker, the recording of $c$ stops at once, and $State(c)$ is empty; and indeed every message sent before the marker arrived before it, so no message is both sent before $\mathrm{rec}(p_i)$ and received after $\mathrm{rec}(p_j)$. $\square$

**Theorem 3 (the result is a global snapshot).** The recorded local states and channel states form the global state $S^\ast$ of the consistent cut $C$. Hence $S^\ast$ is reachable from the global state at the start of the algorithm, and the global state at its end is reachable from $S^\ast$.

*Proof.* The local state saved in line L1 is the state of $p$ after its events in $C$. By Theorem 2, each channel state is the set of messages sent in $C$ and received outside $C$, which is the channel state of the cut. Theorem 1 says that $C$ is consistent. The reachability claims are the theorem on the page on [global snapshots](/global-snapshot/). $\square$

**Corollary (conservation).** If a quantity, such as the money of a bank, is the same in every reachable global state, then its value in $S^\ast$ equals its true value.

**Messages.** By Lemma 1 the algorithm sends exactly one marker on each of the $e$ channels, so $e$ markers. $\square$

**Why FIFO is needed.** Lemma 2 is the only place that uses FIFO order. Without it, a message sent after $\mathrm{rec}(p_i)$ can overtake the marker and reach $p_j$ before $\mathrm{rec}(p_j)$, which gives a receive in $C$ whose send is outside $C$. The page shows such a run, and the test of the code builds it.
