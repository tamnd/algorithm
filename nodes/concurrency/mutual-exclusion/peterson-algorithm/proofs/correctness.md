---
title: Peterson's algorithm gives mutual exclusion, bypass 1, starvation freedom and FCFS
proves: [correctness]
status: full
---

We use the pseudocode of the page, for processes 0 and 1, with $j = 1 - i$. The shared registers $flag[0]$, $flag[1]$ and $turn$ are atomic, and the memory is sequentially consistent: every run is one sequence of reads and writes, and each read returns the value of the last write before it to the same register. Initially $flag[0] = flag[1] = false$. A process stays in the critical section for a finite number of its own steps, and a run is *fair*: a process that is not in its remainder section takes another step eventually. The doorway is lines L1 and L2, and the waiting loop is lines L3 to L5.

Three facts follow from the code at once.

- **(F1)** Only process $i$ writes $flag[i]$. It is true from the write of L1 to the write of L6, so it is true while $i$ is in its waiting loop or in the critical section, and false while $i$ is in its remainder section.
- **(F2)** Process $i$ writes only the value $j$ to $turn$, and only at L2, once in each entry section.
- **(F3)** Process $i$ leaves the waiting loop only after a read of L4 that returns $flag[j] = false$ or a read of L5 that returns $turn \ne j$, and both reads come after its own write of L2 in that entry section.

**Claim 1 (mutual exclusion).** No run has both processes in the critical section at the same time.

*Proof.* Assume that at time $t$ both processes are in the critical section. In its current entry section, each process $i$ wrote $turn \leftarrow j$ at L2, at a time $w_i < t$. The two times differ, so let $i$ be the process with the later write: $w_j < w_i < t$. By (F2), from $w_i$ to $t$ no write to $turn$ happens, because $i$ does not write $turn$ again before it leaves, and $j$ wrote $turn$ at $w_j$ and does not write it again before it leaves, which is after $t$. So $turn = j$ in the whole interval $[w_i, t]$. Process $j$ wrote $flag[j] \leftarrow true$ at L1 before $w_j < w_i$, and it is in the critical section at $t$, so by (F1) $flag[j] = true$ in the whole interval $[w_i, t]$. By (F3), process $i$ left its loop after a read in $(w_i, t)$ that returned $flag[j] = false$ or $turn \ne j$. Both values are impossible in that interval. This is a contradiction. $\square$

**Claim 2 (bypass 1).** If process $i$ has finished its doorway at time $t_0$ and has not yet entered the critical section, then process $j$ enters the critical section at most once between $t_0$ and the entry of $i$.

*Proof.* Assume that $j$ enters twice after $t_0$ while $i$ waits. Between the two entries, $j$ runs its exit section and a new entry section, and in it $j$ writes $turn \leftarrow i$ at L2, at a time $t_2 > t_0$. From $t_2$ on, only $i$ can write $turn$ by (F2), and $i$ is in its waiting loop, which does not write. So $turn = i$ from $t_2$ until $i$ enters. Also $flag[i] = true$ all that time, by (F1). By (F3), the second entry of $j$ needs a read after $t_2$ that returns $flag[i] = false$ or $turn \ne i$. Neither value occurs. This is a contradiction. $\square$

**Claim 3 (starvation freedom, and so deadlock freedom).** In a fair run, each process that starts its entry section enters the critical section.

*Proof.* The doorway has no loop, so process $i$ finishes it. Assume that $i$ then stays in its waiting loop forever. By fairness, $i$ runs L4, and L5 when it gets there, infinitely often. By Claim 2, $j$ enters the critical section only a finite number of times, so after some time $T$ it does not enter again. After $T$, process $j$ cannot stay in the critical section or in its exit section forever, since both are finite. So after some time $j$ either stays in its remainder section forever or stays in its waiting loop forever.

- If $j$ stays in its remainder section, $flag[j] = false$ from some time on, by (F1). The next read of L4 by $i$ returns false, and $i$ leaves the loop.
- If $j$ stays in its waiting loop, then both processes have done their last write to $turn$, so $turn$ has a fixed value $x$ from some time on. If $x = i$, then $turn \ne j$, and if $i$ reads $flag[j] = true$ at L4, it reads $turn \ne j$ at L5 and leaves the loop. If $x = j$, then $turn \ne i$, and in the same way $j$ leaves its loop, which contradicts the case.

In each case $i$ leaves the loop and enters. $\square$

**Claim 4 (first come, first served).** If process $i$ finishes its doorway before process $j$ starts its doorway, then $j$ does not enter the critical section before $i$ does.

*Proof.* Let $t_0$ be the time when $i$ finishes L2, and assume that $j$ writes L1 after $t_0$ and enters before $i$. Then $j$ writes $turn \leftarrow i$ at L2 at a time $t_2 > t_0$. Until $i$ enters, $i$ does not write $turn$, so $turn = i$ and, by (F1), $flag[i] = true$ from $t_2$ until $i$ enters. By (F3), $j$ needs a read after $t_2$ that returns $flag[i] = false$ or $turn \ne i$ before $i$ enters. This is a contradiction. $\square$

**Cost.** Without contention, the entry section of $i$ makes the writes of L1 and L2 and the read of L4, which returns false, and the exit section makes the write of L6: four shared accesses in all, and the waiting loop runs once. Claims 1 to 4 give the properties on the page. $\blacksquare$
