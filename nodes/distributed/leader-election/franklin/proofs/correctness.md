---
title: Franklin's algorithm elects the largest identifier with at most 2n⌊lg n⌋ + 2n messages
proves: [correctness, termination, complexity]
status: full
---

**Claim.** Run FRANKLIN on an asynchronous bidirectional ring of $n \ge 1$ processes with distinct identifiers and reliable FIFO channels, oriented or not. Then every run is finite, the process with the largest identifier $u_{\max}$ ends with status *leader*, every other process ends with status *non-leader* and stores $u_{\max}$, and the run sends exactly $2nR + 2n$ val messages and $n$ leader messages, where $R \le \lfloor \lg n \rfloor$ is the number of rounds with at least two candidates.

**Setup.** Round $r$ of a candidate starts when it sends its value on both ports (line L2 or L8). Let $C_r$ be the set of processes that start round $r$, in ring order $c_1, \ldots, c_k$, indices modulo $k$. For each $j$, call the sequence of processes strictly between $c_j$ and $c_{j+1}$ in the direction from $c_j$ to $c_{j+1}$ the *gap* $G_j$. All processes in gaps of round $r$ are passive.

**Lemma 1 (one round).** Suppose all processes outside $C_r$ are passive when round $r$ starts at each $c_j$, and that every val message of an earlier round is consumed by the candidate it is meant for. Then the first value that $c_j$ takes from the queue of the port toward $c_{j+1}$ in round $r$ is $u(c_{j+1})$, and the first value from the other port is $u(c_{j-1})$.

*Proof.* Passive processes in $G_j$ forward each val message to their other port (line L3), so a message that $c_{j+1}$ sends toward $c_j$ travels through $G_j$ and arrives at $c_j$ on the port toward $c_{j+1}$. A process that became passive in round $r - 1$ forwarded its stored values (line L10) in the same direction, so no message is lost. The channels on this path are FIFO, and every message that $c_{j+1}$ sent toward $c_j$ before round $r$ was consumed in an earlier round by the hypothesis. So the first message of round $r$ in that queue is $\langle \text{val}, u(c_{j+1}) \rangle$. The other port is symmetric. If $k = 1$, both neighbours are $c_1$ itself and the gap is the rest of the ring. $\square$

**Lemma 2 (survivors).** If $k \ge 2$, then $C_{r+1}$ is the set of $c_j$ with $u(c_j) > \max(u(c_{j-1}), u(c_{j+1}))$, it contains the process with the largest identifier in $C_r$, and $1 \le |C_{r+1}| \le \lfloor k/2 \rfloor$. If $k = 1$, $c_1$ runs line L6.

*Proof.* By Lemma 1, line L5 gives $\{a, b\} = \{u(c_{j-1}), u(c_{j+1})\}$. If $k \ge 2$ neither equals $u(c_j)$, so line L6 does not apply and line L7 decides by the stated test; the case $k = 2$ has $c_{j-1} = c_{j+1}$. The largest identifier of $C_r$ passes the test. If $c_j$ and $c_{j+1}$ both passed, each would be larger than the other, so no two cyclically adjacent candidates pass, and at most $\lfloor k/2 \rfloor$ do. If $k = 1$, $a = u(c_1)$ and line L6 applies. Each candidate that fails becomes passive (line L9), and the hypotheses of Lemma 1 hold for round $r + 1$ because each candidate consumes exactly one value from each port in round $r$. $\square$

**Outputs.** $C_1$ is the set of all processes. By Lemma 2 the number of candidates at least halves in each round with at least two candidates and the largest identifier stays, so after $R \le \lfloor \lg n \rfloor$ such rounds the only candidate is the process with $u_{\max}$, which becomes the leader by Lemma 2. No other process runs line L6, because a candidate of a round with $k \ge 2$ never takes its own value from a queue. The leader message goes round the ring once: each other process sets status *non-leader* and forwards it (line L12), and the leader ignores it.

**Counting.** In a round with $k \ge 2$, the value that $c_j$ sends toward $c_{j+1}$ crosses each link of the path from $c_j$ to $c_{j+1}$ once, and the value that $c_{j+1}$ sends toward $c_j$ crosses each link of the same path once in the other direction. The paths for $j = 1, \ldots, k$ cover each of the $n$ links once, so the round sends exactly $2n$ val messages. A forward by line L10 is one of these crossings, delayed, and not an extra message. In the last round both values of the leader go round the ring: $2n$ messages. So there are $2nR + 2n \le 2n\lfloor \lg n \rfloor + 2n$ val messages and $n$ leader messages.

**Termination.** The number of messages is finite, each delivery causes a bounded number of sends, and each candidate receives the two values it waits for by Lemma 1. So the run ends with the outputs above. $\blacksquare$
