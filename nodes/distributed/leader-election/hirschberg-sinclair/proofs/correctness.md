---
title: Hirschberg-Sinclair elects the largest identifier with at most 8n⌈lg n⌉ − 2n election messages
proves: [correctness, termination, complexity]
status: full
---

**Claim.** Run HIRSCHBERG-SINCLAIR on an asynchronous bidirectional ring of $n \ge 2$ processes with distinct identifiers, oriented or not, with reliable channels that need not be FIFO. Let $p_m$ hold the largest identifier and $L = \lceil \lg n \rceil$. Then every run is finite, $p_m$ ends with status *leader*, every other process ends with status *non-leader* and stores $u_m$, and the run sends at most $8nL - 2n$ out and in messages and exactly $n$ leader messages. If each message takes at most one time unit and local steps take no time, $p_m$ is elected by time $2(2^L - 1) + n$. For $n = 1$ the only process sends its two tokens of phase 0 round the loop and is elected.

**Setup.** Write $\mathrm{dist}(i, j) = \min(d, n - d)$ with $d = (j - i) \bmod n$. A *token of $p_i$ in phase $k$* is a copy of $\langle \text{out}, u_i, \cdot \rangle$ or $\langle \text{in}, u_i \rangle$ that descends from one of the two out tokens that $p_i$ sends when it starts phase $k$ (line L2 for $k = 0$, line L11 for $k \ge 1$). Only $p_i$ creates messages with value $u_i$, and lines L4, L5 and L9 each turn one received message into at most one sent message. So each message belongs to exactly one *chain*, which starts at $p_i$ in one direction.

**Lemma 1 (one chain).** Consider an out token that $p_i$ sends in phase $k$ in one direction, with $2^k < n$. Let $q_1, q_2, \ldots$ be the processes in that direction at distance $1, 2, \ldots$. If $u_{q_d} < u_i$ for all $d \le 2^k$, the chain makes $2^k$ out hops and $2^k$ in hops and delivers one in token to $p_i$. Otherwise it makes at most $2^k$ hops and delivers nothing to $p_i$.

*Proof.* The token arrives at $q_d$ with hop count $h = 2^k - d + 1$, by induction on $d$ from line L4. At $q_d$ with $d < 2^k$, so $h > 1$, the token goes on exactly when $u_{q_d} < u_i$ (line L4); otherwise line L7 drops it, since $u_{q_d} \ne u_i$ when $d < n$. At $q_{2^k}$, $h = 1$, and the token turns back when $u_{q_{2^k}} < u_i$ (line L5). The in token then passes $q_{2^k - 1}, \ldots, q_1$, each of which forwards it by line L9, and reaches $p_i$. The port rules "other port" and "same port" make the token move away from $p_i$ and then back, whatever the labels of the ports. $\square$

**Lemma 2 (the winner).** $p_m$ starts phases $0, 1, \ldots, L$, and in phase $L$ an out token of $p_m$ returns to $p_m$, which sets status *leader*.

*Proof.* Every other identifier is smaller than $u_m$. For $k < L$ we have $2^k < n$, so by Lemma 1 both chains of phase $k$ return an in token, and $p_m$ starts phase $k + 1$ by line L11. In phase $L$, $2^L \ge n$. The out token arrives at distance $d$ with $h = 2^L - d + 1 \ge 2$ for each $d \le n - 1$, so line L4 forwards it, and after $n$ hops it is at $p_m$, where line L6 applies. $\square$

**Lemma 3 (nobody else wins).** For $i \ne m$, line L6 never runs at $p_i$.

*Proof.* Line L6 runs at $p_i$ only when an out token with value $u_i$ arrives at $p_i$, which needs a chain of $p_i$ to make $n$ out hops. That chain passes $p_m$ first, and $u_i < u_m$, so line L7 drops it at $p_m$. $\square$

**Lemma 4 (spacing).** If $k \ge 1$ and $p_i$ starts phase $k$, then $2^{k-1} < n$ and $u_i > u_j$ for every $j \ne i$ with $\mathrm{dist}(i, j) \le 2^{k-1}$. Two processes that start phase $k$ are more than $2^{k-1}$ hops apart in both directions, and at most $\lfloor n/(2^{k-1}+1) \rfloor$ processes start phase $k$.

*Proof.* $p_i$ starts phase $k$ only after two in tokens of phase $k - 1$ (line L11). If $2^{k-1} \ge n$, then by Lemma 2 and Lemma 3 no in token of phase $k-1$ exists for $i \ne m$, and $p_m$ has already been elected in a phase $\le k - 1$ and does not reach line L11 in phase $k-1$; so $2^{k-1} < n$. By Lemma 1, both chains of phase $k - 1$ returned, so all processes within $2^{k-1}$ hops on both sides have smaller identifiers. If $p_i$ and $p_j$ both start phase $k$ and were within $2^{k-1}$ hops in one direction, each would be larger than the other. So, going round the ring, consecutive starters are at least $2^{k-1} + 1$ hops apart. With $s$ starters the $s$ gaps add up to $n$, so $s(2^{k-1}+1) \le n$. $\square$

**Messages.** For $k = 0$ each process sends two out tokens and at most two in tokens, at most $4n$ messages. For $1 \le k \le L - 1$, each starter of phase $k$ causes at most $4 \cdot 2^k$ messages by Lemma 1, so phase $k$ has at most

$$4 \cdot 2^k \cdot \frac{n}{2^{k-1} + 1} < 4 \cdot 2^k \cdot \frac{n}{2^{k-1}} = 8n$$

messages. In phase $L$, Lemma 4 gives at most $n/(2^{L-1}+1) < 2$ starters, because $2^{L-1} \ge n/2$; the one starter is $p_m$ by Lemma 2. Its two out tokens make $n$ hops each, and the copy that arrives second is dropped by line L7. No process starts phase $L + 1$ by Lemma 4, since $2^L \ge n$. The total is at most $4n + 8n(L-1) + 2n = 8nL - 2n$. Only $p_m$ sends a leader message (Lemma 3, line L6 runs once by the test on the status), each other process forwards it once on the other port (line L13), and $p_m$ ignores it, so it makes exactly $n$ hops.

**Termination and outputs.** The number of messages is finite by the count above, and each delivery causes at most one send, so the run ends when the last message is delivered. By Lemmas 2 and 3, $p_m$ is the only leader, and each other process receives the announcement once and sets status *non-leader* with leader $u_m$.

**Time.** Every process forwards the tokens of $p_m$ at once (lines L4, L5 and L9 apply because $u_m$ is the largest). So phase $k < L$ of $p_m$ ends at most $2 \cdot 2^k$ time units after it starts, and phase $L$ ends after at most $n$ time units with the election. Adding up, $p_m$ is elected by time $\sum_{k=0}^{L-1} 2^{k+1} + n = 2(2^L - 1) + n$. $\blacksquare$
