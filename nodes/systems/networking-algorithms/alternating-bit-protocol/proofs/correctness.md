---
title: The alternating bit protocol is correct over a FIFO channel that loses and duplicates
proves: [correctness]
status: full
---

**Model.** Each channel is a queue. The sender appends to the data queue $D$, and the receiver takes packets from its head. The receiver appends to the ACK queue $A$, and the sender takes packets from its head. At any time, the channel may delete a packet from its queue (a loss) or replace a packet $x$ by two adjacent copies $x\,x$ (a duplication). It never changes the order of packets, and it never makes up a packet. The timer may expire at any time.

**Ghost labels.** For the proof only, we attach to each packet an integer label that the protocol never reads. A DATA packet that the sender sends while its index is $i$ gets the label $i$. An ACK that the receiver sends in answer to a DATA packet with label $j$ gets the label $j$. A copy has the label of its original. We write $r$ for the number of messages that the receiver has delivered. Two facts follow from lines L1, L7, L8 and L10 at once: $b = i \bmod 2$ and $e = r \bmod 2$. A packet with label $j$ carries the bit $j \bmod 2$, and a DATA packet with label $j$ carries $M[j]$.

**Lemma.** In each reachable state:

- **(I1)** $r \in \{i, i+1\}$;
- **(I2)** the labels in $D$, from head to tail, are non-decreasing and lie in $\{i-1, i\}$, and if $r = i + 1$, they are all equal to $i$;
- **(I3)** the labels in $A$, from head to tail, are non-decreasing and lie in $\{i-1, i\}$, and if $r = i$, they are all equal to $i - 1$.

*Proof.* At the start, $i = r = 0$ and both queues are empty. A loss or a duplication keeps a sequence non-decreasing and adds no new label, so it keeps (I1) to (I3). The other steps are these.

*The sender sends* DATA with label $i$ (line L3). The labels in $D$ are at most $i$, so $D$ stays non-decreasing. If $r = i + 1$, all labels in $D$ were $i$, and the new one is $i$ too.

*The receiver takes* the head of $D$, with label $j$. By (I2), $j \in \{i-1, i\}$. There are three cases.

1. $r = i$ and $j = i$. The bit is $i \bmod 2 = e$, so line L10 delivers $M[i] = M[r]$, and $r$ becomes $i + 1$. The ACK gets the label $i$. Before the step, all labels in $A$ were $i - 1$ by (I3), so $A$ stays non-decreasing. (I2) now needs all labels in $D$ to be $i$: the head had the label $i$, and the rest of $D$ is at least $i$ and at most $i$.
2. $r = i$ and $j = i - 1$. The bit differs from $e$, so nothing is delivered. The ACK gets the label $i - 1$, and all labels in $A$ were $i - 1$.
3. $r = i + 1$. By (I2), $j = i$. The bit $i \bmod 2$ differs from $e = (i+1) \bmod 2$, so nothing is delivered. The ACK gets the label $i$, which is at least each label in $A$.

The case $r = i + 1$ and $j = i - 1$ is not possible by (I2).

*The sender takes* the head of $A$, with label $j \in \{i-1, i\}$.

1. $j = i$. Its bit is $b$, so lines L4, L6 and L7 run, and $i$ becomes $i + 1$. Because $A$ held the label $i$, (I3) excludes $r = i$, so $r = i + 1$ by (I1). After the step, $r$ equals the new $i$, so (I1) holds. By (I2), all labels in $D$ were the old $i$, which is the new $i - 1$, so (I2) holds. The rest of $A$ is at least the old $i$ and at most the old $i$, so all its labels are the new $i - 1$, as (I3) needs when $r = i$.
2. $j = i - 1$. Its bit differs from $b$, and line L5 ignores it. Nothing changes except that $A$ loses its head.

*A timeout* leads to line L3, which is the first step above. $\square$

**Theorem (safety).** The receiver delivers $M[0], M[1], M[2], \ldots$ in this order, and each message at most once.

*Proof.* The proof of the lemma shows that a delivery happens only in case 1 of the receiver step, and that it delivers $M[r]$ and then adds 1 to $r$. $\square$

**Theorem (completion and liveness).** When the sender stops with $i = m$, all $m$ messages were delivered. If both channels are fair (a packet that is sent infinitely often is received infinitely often), and each timer expires after a finite time, the sender reaches $i = m$.

*Proof.* By (I1), $r \ge i$, so $i = m$ gives $r = m$. For liveness, assume that the sender stays at index $i \lt m$ forever. Then it sends DATA with label $i$ infinitely often. The receiver receives it infinitely often, so after the first receipt $r = i + 1$, and from then on each DATA packet that it receives has the label $i$ by (I2). Each one makes an ACK with label $i$ and bit $b$, so the sender receives such an ACK, which is a contradiction. $\blacksquare$

**Where FIFO is used.** The receiver step uses that the head of $D$ has the smallest label in $D$. If the channel can reorder, a DATA packet with label $i - 1$ can arrive after $r$ has reached $i + 1$. Its bit equals $e$, because $i - 1$ and $i + 1$ have the same parity, so the receiver delivers $M[i-1]$ a second time. The page gives such a run.
