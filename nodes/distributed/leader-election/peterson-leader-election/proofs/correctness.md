---
title: Peterson's algorithm elects one leader with at most 2n⌊lg n⌋ + n election messages
proves: [correctness, termination, complexity]
status: full
---

**Claim.** Run PETERSON-LEADER on an asynchronous unidirectional ring of $n \ge 1$ processes with distinct identifiers and reliable FIFO channels. Then every run is finite, exactly one process $\ell$ ends with status *leader*, its $\mathit{tid}$ is the largest identifier, every other process ends with status *non-leader* and stores $u_\ell$, and the run sends exactly $2nR + n$ val messages and $n$ leader messages, where $R \le \lfloor \lg n \rfloor$ is the number of phases with at least two active processes.

**Setup.** Phase $r$ of an active process starts when it sends a value by line L2 ($r = 1$) or line L10, and ends when it runs line L6, L10 or L11. Let $A_r$ be the set of processes that start phase $r$, in ring order $a_1, \ldots, a_k$ with $k = |A_r|$, indices of $a$ modulo $k$, and let $t_j$ be the value that $a_j$ sends at the start of phase $r$, its $\mathit{tid}$ in phase $r$. We prove by induction on $r$ the statement $S(r)$: the values $t_1, \ldots, t_k$ are distinct identifiers, every process outside $A_r$ is a relay, and each $a_j$ receives in phase $r$ first $t_{j-1}$ and then, if $k \ge 2$, $t_{j-2}$.

**Lemma 1.** $S(1)$ holds, and if $S(r)$ holds with $k \ge 2$, then $A_{r+1}$ is the set of $a_j$ such that $t_{j-1} > \max(t_{j-2}, t_j)$, the value of such $a_j$ in phase $r+1$ is $t_{j-1}$, and $S(r+1)$ holds.

*Proof.* Consider phase $r$ with $k$ active processes, distinct values, and relays elsewhere. The relays between $a_{j-1}$ and $a_j$ forward everything (line L4). Process $a_{j-1}$ sends exactly two values in phase $r$ toward $a_j$: first $t_{j-1}$ (line L2 or L10 at the start), then the first value it receives (line L7). Before phase $r$, every message that $a_{j-1}$ sent in phase $r - 1$ was sent before $t_{j-1}$, and on the FIFO path it reaches $a_j$ earlier, where it belongs to phase $r - 1$ of $a_j$ by $S(r-1)$. So the first value $a_j$ receives in phase $r$ is $t_{j-1}$. If $k \ge 2$, $t_{j-1} \ne t_j$ by distinctness, so $a_j$ runs line L7, and the next value it receives is the value that $a_{j-1}$ forwards by line L7, namely the first value $a_{j-1}$ received, which is $t_{j-2}$ by the same argument applied to $a_{j-1}$. Line L9 at $a_j$ then tests $t_{j-1} > \max(t_j, t_{j-2})$. If it holds, $a_j$ sets $\mathit{tid} = t_{j-1}$ and starts phase $r + 1$; otherwise it becomes a relay for good. The new values are $t_{j-1}$ for distinct $j$, so they are distinct identifiers. The statement about what is received in phase $r + 1$ follows by the same FIFO argument, now with the relays of $A_{r} \setminus A_{r+1}$ added. $S(1)$ is the case with $A_1$ all processes, $t_j$ the own identifiers and no earlier phase. $\square$

**Lemma 2 (survivors).** If $k \ge 2$, then $1 \le |A_{r+1}| \le \lfloor k/2 \rfloor$, and the largest value of phase $r$ is a value of phase $r + 1$.

*Proof.* For $k = 2$ the test is $t_{j-1} > t_j$, which holds for exactly one $j$. For $k \ge 3$, let $t_{i}$ be the largest value; then $a_{i+1}$ survives with $t_i$. If $a_j$ and $a_{j+1}$ both survived, then $t_{j-1} > t_j$ and $t_j > t_{j-1}$, which is impossible. So no two cyclically consecutive processes of $A_r$ survive, and at most $\lfloor k/2 \rfloor$ survive. $\square$

**Lemma 3 (the end).** Let $k = |A_r|$. If $k \ge 2$, no process runs line L6 in phase $r$. If $k = 1$, the only active process runs line L6 and becomes the leader.

*Proof.* If $k \ge 2$, the first value of $a_j$ is $t_{j-1} \ne t_j$ (Lemma 1). If $k = 1$, the first value is the own value $t_1$, which went round the ring through relays. $\square$

**Outputs.** By Lemma 2, $|A_r|$ is at least $1$ in each phase and at least halves while it is at least $2$, so for some $r$ we have $|A_r| = 1$, after $R$ phases with at least two active processes, where $n / 2^R \ge 1$, that is $R \le \lfloor \lg n \rfloor$. By Lemma 3 exactly one process $\ell$ runs line L6, and by Lemma 2 its value is the largest identifier. It sends $\langle \text{leader}, u_\ell \rangle$. Every other process forwards it once and sets status *non-leader* (line L13), and $\ell$ drops it, so it makes exactly $n$ hops.

**Counting.** In phase $r$ with $k \ge 2$, the value $t_{j-1}$ goes from $a_{j-1}$ to $a_j$, and the forwarded value goes from $a_{j-1}$ to $a_j$, so each gap of the ring between consecutive active processes is crossed by exactly two values. The gaps add up to $n$, so the phase sends exactly $2n$ val messages. In the last phase the one value goes once round the ring: $n$ messages. So there are $2nR + n \le 2n \lfloor \lg n \rfloor + n$ val messages.

**Termination.** The number of messages is finite, each delivery causes at most one send, and no process waits for a message that is not sent (each active process of phase $r$ receives its two values by Lemma 1). So the run ends with the outputs above. $\blacksquare$
