---
title: Kessels' two-process algorithm gives mutual exclusion, starvation freedom and bypass 1, and the tree gives mutual exclusion and starvation freedom
proves: [correctness]
status: full
---

We use the pseudocode of the page. The registers are atomic and the memory is sequentially consistent. A process stays in the critical section for a finite time, and a process that is not in its remainder section takes another step eventually.

## Part 1: two processes

Take one node and write $b_s$ and $t_s$ for $b[x][s]$ and $t[x][s]$. Process $i \in \{0, 1\}$ plays side $i$, and $j = 1 - i$. Only process $i$ writes $b_i$ and $t_i$. Let

$$T = t_0 \oplus t_1 .$$

Line L4 picks $mine$ so that $mine \oplus o = i$. So the write at L5 makes $T = i$ if $t_j$ still has the value $o$ that $i$ read at L3. In the loop, $t_i = mine$, so the test at L9 lets $i$ leave the loop exactly when $T \ne i$. In short: process $i$ waits while $b_j = true$ and $T = i$, and the last process to write its $t$ is the one that gives way.

**Program counter.** The atomic steps of process $i$ are the write at L2, the read at L3 (with the local step L4), the write at L5, the read at L7, the read at L8 (with the local test L9), and the write at L11. Let $pc_i$ be one of the following:

- $R$: in the remainder section, or about to do L2;
- $3$: about to do L3;
- $5$: about to do L5, with the value $o_i$ that it read at L3;
- $7$ or $8$: in the loop, about to do L7 or L8;
- $C$: in the critical section, or about to do L11.

Then $b_i = true$ exactly when $pc_i \ne R$. Write $Q_i$ for $pc_i \in \{7, 8, C\}$. While $Q_i$ holds, $t_i$ does not change.

**Invariants.** For $i \in \{0, 1\}$ and $j = 1 - i$:

- $A(i)$: if $pc_i = C$ and $Q_j$, then $T = j$.
- $B(i)$: if $pc_i = C$ and $pc_j = 5$, then $o_j = t_i$.
- $D(i)$: if $Q_i$, $pc_j = 5$ and $o_j \ne t_i$, then $T = i$.
- $E(i)$: if $pc_i = 5$ and $pc_j \in \{R, 3, 5\}$, then $o_i = t_j$.

**Lemma 1.** The eight statements $A(i)$, $B(i)$, $D(i)$, $E(i)$ for $i = 0, 1$ hold in every reachable state.

*Proof.* At the start $pc_0 = pc_1 = R$, so no premise holds. We show that each step of a process $i$ keeps all eight true. The step changes only $pc_i$, the local values of $i$, and possibly $b_i$ or $t_i$. A statement whose premise is false after the step holds. A statement whose premise and conclusion do not change holds by the induction. So we look only at the other cases. The states $7$ and $8$ play the same role in all eight statements, so the steps $7 \to 8$ and $8 \to 7$ keep them.

1. *L2, $R \to 3$.* Only $E(j)$ can have a true premise after the step, and it had a true premise before, since $pc_i \in \{R, 3, 5\}$ before and after. Its conclusion $o_j = t_i$ does not change.
2. *L3, $3 \to 5$.* Now $o_i = t_j$, just read. This gives $E(i)$ and $B(j)$, and it makes the premise of $D(j)$ false. For $E(j)$, the premise held before ($pc_i = 3$) and its conclusion does not change.
3. *L5, $5 \to 7$.* Now $t_i \oplus o_i = i$, and $Q_i$ holds.
   - $A(j)$: if $pc_j = C$, then $B(j)$ before the step gives $o_i = t_j$, so after it $T = t_i \oplus t_j = t_i \oplus o_i = i$, which is what $A(j)$ says.
   - $D(i)$: if $pc_j = 5$, then $E(i)$ before the step gives $o_i = t_j$, so after it $T = i$.
   - The premises of $B(j)$, $D(j)$, $E(i)$ and $E(j)$ are false after the step, and so are those of $A(i)$ and $B(i)$.
4. *L7 reads $b_j = false$, $7 \to C$.* Then $pc_j = R$. So the premises of $A(i)$ and $B(i)$ are false. No register changes, and $Q_i$ holds before and after, so $D(i)$ and $A(j)$ keep their values. The premises of $B(j)$, $D(j)$ and $E(j)$ need $pc_i = 5$ or $pc_i \in \{R, 3, 5\}$, so they are false.
5. *L8 reads $t_j$ and the test at L9 succeeds, $8 \to C$.* Then $T \ne i$, so $T = j$ in this state, and no register changes. This gives $A(i)$. For $B(i)$: if $pc_j = 5$ and $o_j \ne t_i$, then $D(i)$ before the step gives $T = i$, which is false. So $o_j = t_i$. The other statements keep their values as in case 4.
6. *L11, $C \to R$.* Only $E(j)$ can have a true premise after the step: $pc_j = 5$. Before the step $pc_i = C$, so $B(i)$ gave $o_j = t_i$, and $t_i$ does not change.

So every step keeps the eight statements. $\square$

**Theorem 1 (mutual exclusion, two processes).** The two processes are never in the critical section at the same time.

*Proof.* If $pc_0 = pc_1 = C$, then $Q_0$ and $Q_1$ hold, so $A(0)$ gives $T = 1$ and $A(1)$ gives $T = 0$. This is not possible. $\square$

**Lemma 2.** Suppose that process $i$ has $Q_i$ from some time on, and that process $j$ does L3 after that time and then L5. From the write of $j$ at L5 on, while $Q_i$ still holds, $j$ does not leave the loop at L6.

*Proof.* While $Q_i$ holds, $t_i$ and $b_i = true$ do not change. So $j$ reads the current $t_i$ at L3, and after its write at L5, $T = t_i \oplus t_j = j$. Only $j$ can change $t_j$, and it does so only at L5 of a later passage. So $T = j$ and $b_i = true$ stay true, and each time $j$ reads them in the loop, it stays in the loop. $\square$

**Theorem 2 (bypass 1 and first come, first served).** Let the doorway be L2 to L5. After process $i$ finishes its doorway, process $j$ enters the critical section at most once before $i$ does. If $j$ starts its entry section after $i$ finished its doorway, $j$ does not enter before $i$.

*Proof.* After its doorway, $Q_i$ holds until $i$ leaves the critical section. A passage of $j$ that starts after that time does L3 after it, so by Lemma 2, $j$ does not enter in that passage before $i$ does. Only the passage of $j$ that was in progress when $i$ finished its doorway can enter first. $\square$

**Theorem 3 (starvation freedom, two processes).** In a fair run, a process that starts its entry section enters the critical section.

*Proof.* Suppose that process $i$ stays in its entry section forever. It finishes its doorway, so from some time on $Q_i$ holds and $i$ is in the loop forever. Look at $j$ after that time.

- If $j$ enters the critical section twice more, then the second of those passages started after $i$ finished its doorway, and Theorem 2 says that this cannot happen.
- So from some time on, $j$ does not enter. If $j$ is then in its remainder section forever, $b_j = false$ forever, and $i$ reads it at L7 and leaves the loop. This is false.
- Otherwise $j$ is in its entry section forever (its critical and exit sections are finite), and by fairness it is in the loop forever too. Then neither $t_0$ nor $t_1$ changes, so $T$ is a constant, and $b_0 = b_1 = true$. Each process reads the other $b$ as true and goes to L8 again and again. One of them has $T \ne$ its own index, and it leaves the loop at L9. This is false.

So $i$ enters. $\square$

Deadlock freedom follows from Theorem 3.

## Part 2: the tree

For $n$ processes, the nodes of a complete binary tree each hold one copy of the two-process algorithm, as on the page. Process $i$ *holds* node $x$ from the moment it leaves the loop at $x$ until its write $b[x][s] \leftarrow false$ at L11. Say that process $i$ holds its own leaf from the start of its entry section until the end of its exit section.

**Lemma 3.** A process runs code of node $x$ only while it holds the child $c$ of $x$ on its path.

*Proof.* Process $i$ starts the code of $x$ at once after it leaves the loop at $c$. In the exit section it writes $b$ from the root down, so it writes $b[x][s] \leftarrow false$ before it releases $c$. For a leaf $c$, the claim holds by the definition. $\square$

**Lemma 4.** For each inner node $x$, at most one process holds $x$ at any time. Also, at each time at most one process runs code on side $s$ of $x$.

*Proof.* By induction on the height of $x$. By Lemma 3 and the induction for the child $c_s(x)$ on side $s$ (or, for a leaf, because only one process starts there), the processes that run code on side $s$ of $x$ do so one at a time. Their passages on side $s$ follow one another, and a new one starts only after the last one wrote $b[x][s] \leftarrow false$, which is the state $R$ of Part 1. The value of $t[x][s]$ stays from one passage to the next, as it does for a single process. So the steps on side $s$ are the steps of one *virtual process* that runs the two-process code again and again. Only the two virtual processes of $x$ access the registers of $x$. So each run of the tree gives a run of the two-process algorithm at $x$, and Theorem 1 says that at most one virtual process, so at most one real process, holds $x$. $\square$

**Theorem 4 (mutual exclusion).** At most one process is in the critical section at any time.

*Proof.* A process in the critical section holds the root. Apply Lemma 4 to the root. $\square$

**Theorem 5 (starvation freedom).** In a fair run, every process that starts its entry section enters the critical section.

*Proof.* We show by induction on the depth of $x$, from the root down, that a process that starts the code of $x$ holds $x$ later and then releases it. Look at the run of the two-process algorithm of the virtual processes at $x$. A virtual process in its entry section is a real process in the loop at $x$, so it takes steps. Its critical section is finite: if $x$ is the root, the process is in the real critical section, which is finite, and then it writes $b[x][s] \leftarrow false$ first; if $x$ has a parent $y$, the process starts the code of $y$ at once, holds $y$ and releases it by the induction, and its next write releases $x$. A virtual process with no passage in progress has $b[x][s] = false$, as a process in its remainder section has. So Theorem 3 applies at $x$. A process that starts its entry section starts the code of its lowest node at once, and by the claim it holds each node of its path in turn, up to the root. $\square$

Deadlock freedom follows from Theorem 5.

**Theorem 6 (no bound on bypass for $n \ge 3$).** Take the doorway to be L2 to L5 at the lowest node of the path. For every $m$ there is a run in which process 0 has finished its doorway and process 2 enters $m$ times before process 0 enters.

*Proof.* For $n \ge 3$ the lowest node $x$ of process 0 has leaves 0 and 1 below it, and the path of process 2 does not go through $x$. Process 0 finishes its doorway at $x$ and then takes no step, and the processes other than 0 and 2 stay in their remainder sections. At every node $y$ on the path of process 2, the $b$ register of the other side is false: if process 0 is below that side, it has written only at $x$, which is below $y$, and else no process of that side has started. So process 2 passes each node at L7 and enters, $m$ times. The run is finite, so it can go on fairly, and then process 0 enters by Theorem 5. For $n = 2$ the tree is one node and Theorem 2 gives bypass 1. $\blacksquare$
