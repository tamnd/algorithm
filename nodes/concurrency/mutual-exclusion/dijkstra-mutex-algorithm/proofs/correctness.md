---
title: Dijkstra's algorithm gives mutual exclusion and deadlock freedom, but not starvation freedom
proves: [correctness]
status: full
---

We use the pseudocode of the page. There are $n \ge 2$ processes. At the start $b[i] = c[i] = true$ for all $i$, and $k$ is some process number. The registers are atomic and the memory is sequentially consistent. Each access in the pseudocode is one atomic step; at L5 the process reads $k$ and then reads $b$ of the value that it read. A process stays in the critical section for a finite time, and a process that is not in its remainder section takes another step eventually.

Only process $i$ writes $b[i]$ and $c[i]$. Note these facts about the code:

- (F1) $b[i] = true$ while process $i$ is in its remainder section, and $b[i] = false$ from L1 until L13.
- (F2) $c[i] = true$ while process $i$ is in its remainder section. Process $i$ writes $c[i] \leftarrow false$ only at L8, and after that it writes $c[i]$ again only at L4 (in a later round of the loop) or at L12 (after the critical section).
- (F3) Process $i$ enters the critical section only at L11, after a round of the loop in which it wrote $c[i] \leftarrow false$ at L8 and then read $c[j] = true$ for each $j \ne i$ at L10.

**Theorem 1 (mutual exclusion).** At most one process is in the critical section at any time.

*Proof.* Suppose that processes $i \ne j$ are both in the critical section at time $\tau$. For each of them, take the write $c \leftarrow false$ at L8 in the round in which it entered (F3); call them $w_i$ and $w_j$, and say $w_i$ comes before $w_j$. By (F2), from $w_i$ until $i$ leaves the critical section, which is after $\tau$, process $i$ does not write $c[i]$ again, so $c[i] = false$ in all that time. In the round of $j$ that ends with its entry, $j$ reads $c[i]$ at L10 after $w_j$ and before $\tau$. That read is after $w_i$ and before $\tau$, so it returns false, and $j$ goes back to L2 in that round. This contradicts (F3). $\square$

**Theorem 2 (deadlock freedom).** In a fair run, if some process is in its entry section, then some process enters the critical section later.

*Proof.* Suppose not. Then from some time $t_0$ on no process enters, and some process is in its entry section. The exit section has two writes, so we can choose $t_0$ so that after $t_0$ no process is in its critical or exit section. A process in its remainder section after $t_0$ stays there or starts its entry section, and it never leaves the entry section again. So we can also choose $t_0$ so that, from $t_0$ on, the set $P$ of processes in the entry section does not change. Then $P \ne \emptyset$, every process in $P$ goes around the loop forever, and by (F1), $b[x] = false$ for $x \in P$ and $b[x] = true$ for $x \notin P$, from $t_0$ on.

*Step 1: from some time on, $k \in P$ forever.* Only processes in $P$ write $k$ after $t_0$, and each of them writes its own number. So once $k \in P$, it stays in $P$. Suppose that $k \notin P$ for all time after $t_0$. Take a process $i \in P$. It reads $k \ne i$ at L3 (since $k \notin P$), writes $c[i]$, reads $k$ at L5 and gets a value $x \notin P$, reads $b[x] = true$, and writes $k \leftarrow i \in P$. This is a contradiction.

*Step 2: from some time $t_2$ on, $k$ does not change.* Let $t_1$ be the time after which $k \in P$. A process $i$ writes $k$ at L6 only right after it read $b[x] = true$ at L5 for the value $x$ that it read from $k$. After $t_1$, every read of $k$ returns a value in $P$, and $b[x] = false$ for it. So each read pair at L5 that starts after $t_1$ leads to no write. Only a read pair that started before $t_1$ can lead to a write after $t_1$, and each process has at most one such pair. So there are at most $|P|$ writes of $k$ after $t_1$, and after the last one, $k$ is a constant $k^* \in P$.

*Step 3: process $k^*$ enters.* Take a process $i \in P$ with $i \ne k^*$. It finishes the round that it is in at $t_2$ without entering, by the choice of $t_0$. In each later round it reads $k = k^* \ne i$ at L3 and writes $c[i] \leftarrow true$ at L4, and it never reaches L8 again. So from some time $t_3$ on, $c[i] = true$ for all $i \ne k^*$: for $i \in P$ by this argument, and for $i \notin P$ by (F2). Process $k^*$ reads $k = k^*$ at L3 in each round after $t_2$, so it goes to L8 and scans the $c[j]$. Its first round that starts after $t_3$ reads $c[j] = true$ for all $j \ne k^*$ and enters at L11. This contradicts the choice of $t_0$. $\square$

**Theorem 3 (no starvation freedom).** For $n = 2$ there is a fair run in which process 1 stays in its entry section forever. The same run, with the other processes in their remainder sections, works for every $n \ge 2$.

*Proof.* Let $k = 0$ at the start. Process 0 runs alone into the critical section: $b[0] \leftarrow false$, it reads $k = 0$, $c[0] \leftarrow false$, it reads $c[j] = true$ for all $j \ne 0$, and it enters. Now process 1 starts: $b[1] \leftarrow false$, it reads $k = 0 \ne 1$, writes $c[1] \leftarrow true$, reads $k = 0$ and $b[0] = false$, and does not write $k$. Call this state $S$. Then repeat the following round forever:

1. Process 0 leaves: $c[0] \leftarrow true$, $b[0] \leftarrow true$.
2. Process 0 starts again: $b[0] \leftarrow false$, it reads $k = 0$, writes $c[0] \leftarrow false$, reads $c[1] = true$ (and $c[j] = true$ for the other $j$), and enters.
3. Process 1 does one round of its loop: it reads $k = 0$, writes $c[1] \leftarrow true$, reads $k = 0$ and $b[0] = false$, and does not write $k$.

Process 1 reads $b[0]$ only in step 3, when process 0 is in the critical section and $b[0] = false$. After each round, all registers and both processes are as in $S$, so the round can repeat forever. Both processes take steps in every round, so the run is fair, and process 1 never enters. By symmetry, the run with the roles of 0 and 1 swapped and $k = 1$ shows that process 0 can starve too. $\blacksquare$
