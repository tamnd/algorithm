---
title: Dekker's algorithm gives mutual exclusion and starvation freedom, but no bound on bypass
proves: [correctness]
status: full
---

We use the pseudocode of the page, for processes 0 and 1, with $j = 1 - i$. The registers $flag[0]$, $flag[1]$ and $turn$ are atomic, and the memory is sequentially consistent: a run is one sequence of reads and writes, and a read returns the value of the last write before it. Initially both flags are false and $turn \in \{0, 1\}$. A process stays in the critical section for a finite number of its own steps. A run is *fair* if each process that is not in its remainder section takes another step eventually.

Facts from the code:

- **(F1)** Only process $i$ writes $flag[i]$. It writes true at L1 and L6 and false at L4 and L8. Each write of L4 is followed by L5 and then L6, so in each entry section the last write of $flag[i]$ before the entry is a write of true, and $flag[i]$ stays true from that write until L8. In the remainder section $flag[i]$ is false.
- **(F2)** $turn$ is written only at L7, in an exit section, and process $i$ writes only the value $j$ there.
- **(F3)** Process $i$ enters the critical section only directly after a read of L2 that returns $flag[j] = false$.

**Claim 1 (mutual exclusion).** No run has both processes in the critical section at the same time.

*Proof.* Assume that both are in the critical section at time $t$. By (F3), each process $i$ entered after a read of L2 at a time $r_i < t$ that returned $flag[j] = false$, and by (F1) its last write of $flag[i]$ before $r_i$ was a write of true, at a time $w_i < r_i$, after which $flag[i]$ is true until after $t$. Say $r_0 < r_1$. Then $w_0 < r_0 < r_1 < t$, so $flag[0] = true$ at time $r_1$, and the read of process 1 at $r_1$ cannot return false. The case $r_1 < r_0$ is the same with the names exchanged. $\square$

**Claim 2 (starvation freedom).** In a fair run, each process that starts its entry section enters the critical section.

*Proof.* Assume that process $i$ starts its entry section at time $T$ and never enters after that. By fairness, $i$ takes infinitely many steps, all in its entry section.

*Case A: process $j$ enters the critical section after $T$.* It leaves after a finite time and writes $turn \leftarrow i$ at L7, at a time $T_1$. After $T_1$, only $j$ can write $turn$, by (F2), because $i$ does not reach its exit section; and $j$ writes only $i$. So $turn = i$ from $T_1$ on. After $T_1$, process $i$ leaves the loop of L5 if it is in it, since it reads $turn = i \ne j$, and then writes $flag[i] \leftarrow true$ at L6. From then on, at L3 it reads $turn = i \ne j$, so it never runs L4 again. So there is a time $T_2$ after which $flag[i] = true$ forever. Now look at $j$ after $T_2$. An entry of $j$ needs a read of L2 that returns $flag[i] = false$, and such a read happens before $T_2$, so $j$ enters at most once more, directly after a read made before $T_2$. After that, $j$ either stays in its remainder section, with $flag[j] = false$, or runs its entry section: at L2 it reads $flag[i] = true$, at L3 it reads $turn = i$, which is the other process for $j$, so it writes $flag[j] \leftarrow false$ at L4 and waits at L5 for $turn \ne i$ forever. In both cases $flag[j] = false$ from some time on. Process $i$ then reads $flag[j] = false$ at L2 and enters. This is a contradiction.

*Case B: process $j$ does not enter after $T$.* Then from some time on, $j$ is either in its remainder section forever or in its entry section forever (the critical section and the exit section are finite).

- If $j$ is in its remainder section forever from some time on, $flag[j] = false$ from then on. If $i$ is in the loop of L5, it waits for $turn \ne j$. It got there by reading $turn = j$. If $j$ left its critical section after $T$, it wrote $turn \leftarrow i$, so $i$ leaves L5. If not, $j$ was in its remainder section during the whole entry section of $i$, so $flag[j] = false$ at every read of L2 by $i$, and $i$ never reached L5. So $i$ is in the loop of L2 and L3, and it reads $flag[j] = false$ at L2 and enters.
- If $j$ is in its entry section forever, then neither process writes $turn$ again, so $turn$ has a fixed value $x$ from some time on. Let $f = x$ be the *favoured* process and $u$ the other. Process $u$ reads $flag[f]$ at L2 again and again. Each such read returns true, otherwise $u$ enters, which is excluded. So $u$ then reads $turn = f$ at L3, writes $flag[u] \leftarrow false$ at L4, and waits at L5 forever, because $turn = f$. Process $f$ leaves L5 if it is there (it reads $turn = f \ne u$), never runs L4 again, and reads $flag[u] = false$ at L2. So $f$ enters, which is excluded for both $f = i$ and $f = j$.

Each case gives a contradiction, so $i$ enters. $\square$

**Claim 3 (deadlock freedom).** This follows from Claim 2.

**Claim 4 (no bound on bypass).** For each $k$, there is a run in which process 0 has started its entry section, has written $flag[0] \leftarrow true$, and does not enter while process 1 enters $k$ times.

*Proof.* Let $turn = 1$ (process 0 can make this true by one passage alone, since its exit writes $turn \leftarrow 1$). Process 1 writes $flag[1] \leftarrow true$. Process 0 writes $flag[0] \leftarrow true$ at L1, reads $flag[1] = true$ at L2 and $turn = 1$ at L3, and writes $flag[0] \leftarrow false$ at L4. Now process 0 stops for a while; it is still in its entry section. Process 1 reads $flag[0] = false$ at L2, enters, leaves (writing $turn \leftarrow 0$ and $flag[1] \leftarrow false$), starts again, writes $flag[1] \leftarrow true$, reads $flag[0] = false$ and enters again. It can repeat this $k$ times, because $flag[0]$ stays false while process 0 takes no step. The run is a prefix of a fair run, since process 0 can take its steps afterwards, and by Claim 2 it then enters. $\square$

So the algorithm gives mutual exclusion and starvation freedom, but no bound on bypass, even when the count starts after the write of L1. In the run of Claim 4, process 1 starts its entry section after process 0 has written L1 and still enters first, so L1 is not a doorway that gives FCFS order either. $\blacksquare$
