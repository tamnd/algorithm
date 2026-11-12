---
title: The leaky bucket queue accepts the same packets as a leaky bucket meter of size K, and sends them at rate r with delay at most K/r
proves: [correctness]
status: full
---

**Setup.** The queue has rate $r > 0$ and capacity $K \ge 1$ packets, counted with the packet that is being sent. Packets arrive at times $t_1 \le t_2 \le \cdots$ with sizes $L_k > 0$, and a packet of size $L$ takes $L/r$ seconds to send. When several events share a time, the departures at that time happen first, then the arrivals in index order; this is what line L1 does by calling DRAIN before the test. Let $A$ be the set of accepted packets. For $k \in A$ let $d_k$ be its departure time, and for each packet $k$ let $p(k)$ be the last accepted packet before $k$, if there is one.

**Theorem 1 (departure times).** For each $k \in A$,

$$d_k = \max(t_k, d_{p(k)}) + L_k / r,$$

with $d_{p(k)} = -\infty$ when $k$ is the first accepted packet. In particular the packets leave in FIFO order, and the link is never idle while a packet waits.

*Proof.* Consider the moment after line L1 at the arrival of $k$. DRAIN has sent every packet whose departure time is at most $t_k$, and no other.

1. If the FIFO is empty, then $p(k)$ (if it exists) has left, so $d_{p(k)} \le t_k$. Line L3 sets the departure of $k$ to $t_k + L_k/r = \max(t_k, d_{p(k)}) + L_k/r$.
2. If the FIFO is not empty, its last packet is $p(k)$, because the FIFO keeps the accepted packets in order of arrival. The head of the FIFO has a departure time greater than $t_k$, and $p(k)$ leaves no earlier than the head, so $d_{p(k)} > t_k$. Packet $k$ joins at the tail. It becomes the head when $p(k)$ leaves, and line L8 then sets its departure to $d_{p(k)} + L_k/r = \max(t_k, d_{p(k)}) + L_k/r$.

In both cases each packet starts to send at the departure of the one before it or at its own arrival, whichever is later, so the link is busy whenever a packet waits. $\square$

From here on all packets have size 1, so each one takes $1/r$ seconds.

**Lemma 2 (packets in the system).** Let $D_k = \max(0, d_{p(k)} - t_k)$ (and $D_k = 0$ if no packet was accepted before $k$). After line L1 at the arrival of $k$, the FIFO holds exactly $\lceil r D_k \rceil$ packets.

*Proof.* If $D_k = 0$, every accepted packet has left by Theorem 1, and the FIFO is empty. Else the link is busy at $t_k$. Let $s \le t_k$ be the start of the busy period that holds $t_k$: the last time before $t_k$ at which the FIFO went from empty to not empty. By Theorem 1, within a busy period each departure is $1/r$ after the one before it, so the departures of this busy period are $s + 1/r, s + 2/r, \ldots, d_{p(k)}$. The FIFO holds the accepted packets whose departure is greater than $t_k$. These are the times $d_{p(k)} - m/r$ with integer $m \ge 0$ and $d_{p(k)} - m/r > t_k$, because each such time is greater than $s$ and is therefore one of the departures of the busy period. Their number is the number of integers $m \ge 0$ with $m < r D_k$, which is $\lceil r D_k \rceil$. $\square$

**Theorem 3 (same decisions as the meter).** Run a [leaky bucket meter](/leaky-bucket-meter/) with leak rate $r$ and size $b = K$, empty at the start, on the same unit packets, and let $X_k$ be its level after its leak line at packet $k$. Then $X_k = r D_k$ for each $k$, and packet $k$ is accepted by the queue if and only if the meter passes it.

*Proof.* We show $X_k = r D_k$ by induction on $k$, and the decisions at each step. For $k = 1$ both are 0. Assume $X_k = r D_k$.

*Decisions.* The queue drops $k$ when the FIFO holds $K$ or more packets, so by Lemma 2 it accepts $k$ exactly when $\lceil r D_k \rceil \le K - 1$. Since $K - 1$ is an integer, this holds exactly when $r D_k \le K - 1$, that is when $X_k + 1 \le K$, which is the meter test with $L = 1$ and $b = K$.

*Step.* If $k$ is accepted, the meter level after $k$ is $X_k + 1 = r D_k + 1 = r(d_k - t_k)$ by Theorem 1, since $d_k - t_k = D_k + 1/r$. Then $p(k+1) = k$, and $X_{k+1} = \max(0, r(d_k - t_k) - r(t_{k+1} - t_k)) = r \max(0, d_k - t_{k+1}) = r D_{k+1}$. If $k$ is dropped, the level after $k$ is $X_k = r \max(0, d_{p(k)} - t_k)$ and $p(k+1) = p(k)$, so the same computation gives $X_{k+1} = r\max(0, d_{p(k)} - t_{k+1}) = r D_{k+1}$. $\square$

**Corollary 4 (delay).** Each accepted unit packet waits $d_k - t_k = (X_k + 1)/r \le K/r$ seconds, with equality when it finds $K - 1$ packets ahead of it with the head just starting.

*Proof.* By Theorem 1, $d_k - t_k = D_k + 1/r = (X_k + 1)/r$ by Theorem 3, and an accepted packet has $X_k + 1 \le K$. $\square$

**Theorem 5 (the output is smooth).** For accepted packets $i$ before $j$ (any sizes), the packets accepted after $i$ and up to $j$ have total size at most $r(d_j - d_i)$. So in any interval of length $\tau$ the packets that leave have total size at most $r\tau + \max_k L_k$; for unit packets, at most $r\tau + 1$ packets.

*Proof.* By Theorem 1, $d_k \ge d_{p(k)} + L_k/r$ for each accepted $k$ after the first. Adding these from the packet after $i$ up to $j$ gives $d_j - d_i \ge \sum L_k / r$. In an interval of length $\tau$, let $i$ and $j$ be the first and the last packets that leave in it. The packets after $i$ add up to at most $r(d_j - d_i) \le r\tau$, and packet $i$ adds at most $\max_k L_k$. $\blacksquare$

So the queue and the meter accept the same unit packets, and differ in what they do with them: the meter forwards each accepted packet at its arrival, in bursts of up to $K$, while the queue holds it for up to $K/r$ seconds and forwards one packet each $1/r$ seconds.
