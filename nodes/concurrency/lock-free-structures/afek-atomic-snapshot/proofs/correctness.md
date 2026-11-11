---
title: The Afek et al. snapshot is linearizable, and each operation takes at most 2n² reads and one write
proves: [correctness]
status: full
---

We use the pseudocode of the page, with processes $0, \ldots, n-1$. Register $R[j]$ holds a triple $(val, seq, view)$ and only process $j$ writes it. Every read and every write of a register is atomic. Process $j$ numbers its updates $1, 2, 3, \ldots$ and writes the number of the update in the $seq$ field, so the values of $R[j].seq$ grow by one at each write of $R[j]$ and never repeat. The initial value of $R[j]$ has $seq = 0$ and the initial vector as its view.

The object state at time $t$ is the vector of the $val$ fields of $R[0], \ldots, R[n-1]$ at time $t$. A *direct scan* is one that returns in line L8. A *borrowed scan* is one that returns in line L11.

**Lemma 1 (no write between equal reads).** If a process reads $R[j]$ twice and gets the same $seq$ both times, no write of $R[j]$ happened between the two reads.

*Proof.* Every write of $R[j]$ stores a $seq$ larger than all earlier ones. So after a write between the two reads, the second read would get a larger $seq$ than the first. $\square$

**Lemma 2 (a direct scan sees one instant).** Let a scan $S$ return in line L8 after collects $a$ (line L5) and $b$ (line L6). Let $t$ be any time after the last read of $a$ and before the first read of $b$. Then at time $t$, for every $j$, $R[j] = b[j]$.

*Proof.* For each $j$, the read of $R[j]$ in $a$ is before $t$ and the read of $R[j]$ in $b$ is after $t$. Line L7 says that the two reads got the same $seq$. By Lemma 1 no write of $R[j]$ happened between them, so $R[j]$ held the same triple during the whole interval, and that triple is $b[j]$. $\square$

**Lemma 3 (a borrowed view comes from a scan inside this scan).** Let a scan $S$ return $b[j].view$ in line L11. Then this view is the result of an embedded scan $S'$ (line L1 of an update of process $j$) that started after $S$ started and ended before $S$ ended.

*Proof.* Line L11 runs only if $moved[j]$ is already true, so $R[j]$ changed between the two collects of an earlier iteration $k_1$ of $S$, and again in the current iteration $k_2$. In iteration $k_1$, let the collects give $seq$ values $s_0 \ne s_1$ for $R[j]$. The write of $s_1$ happened after the read that gave $s_0$, so after $S$ started. In iteration $k_2$, the first read of $R[j]$ comes after the read that gave $s_1$, so it gives some $s' \ge s_1$, and the second read gives $s_2 \ne s'$, so $s_2 > s' \ge s_1$. Let $U$ be the update of process $j$ with number $s_2$. Process $j$ runs its updates one at a time, so $U$ started after update number $s_1$ ended, which is after its write, which is after $S$ started. The embedded scan $S'$ of $U$ runs in line L1, inside $U$, before the write of $U$. That write happened before $S$ read $s_2$, which is before $S$ ends. So $S'$ runs inside the interval of $S$, and $U$ wrote the result of $S'$ as its view. $\square$

**Theorem 1 (linearizability).** Linearize each update at its write (line L2). For each scan $S$ choose a time $\tau(S)$ as follows. If $S$ is direct, $\tau(S)$ is a time $t$ as in Lemma 2. If $S$ is borrowed from $S'$ as in Lemma 3, $\tau(S) = \tau(S')$. Then $\tau(S)$ is inside the interval of $S$, and $S$ returns the object state at time $\tau(S)$. Order all operations by their linearization times, scans after updates at the same time. This order respects real time and is legal for the sequential snapshot object, so every history is linearizable.

*Proof.* We show the two claims about $\tau(S)$ by strong induction on the end time of the scan. A direct scan returns the $val$ fields of $b$, which by Lemma 2 are the object state at $\tau(S)$, and $\tau(S)$ is between two of its own reads. A borrowed scan $S$ returns the result of $S'$, which ends before $S$ ends, so the claims hold for $S'$ by induction: $S'$ returns the state at $\tau(S')$, inside the interval of $S'$, which is inside the interval of $S$ by Lemma 3. So $\tau(S) = \tau(S')$ is inside the interval of $S$ and $S$ returns the state at that time. (The embedded scans are scans like the others, so the induction covers them too.)

Every linearization time is inside the interval of its operation, so the order respects real time. In the order, the object state after the updates placed before a time $t$ is the vector of the values written by the last write of each register before $t$, which is the vector of $val$ fields at time $t$. So each scan returns exactly what the sequential object returns at its place in the order. An update that has not written yet is left out, and one that has written is placed at its write, which is a legal treatment of pending operations. $\square$

**Theorem 2 (wait-freedom and the step bound).** A scan does at most $n$ iterations of the loop of line L4, so at most $2n^2$ register reads. An update does at most $2n^2$ reads and one write.

*Proof.* Let $S$ be a scan by process $p$ (a scan operation of $p$, or the embedded scan of an update of $p$). While $S$ runs, $p$ does nothing else; in particular it does not write $R[p]$, because the write of an update comes after its embedded scan. So the two collects of an iteration always agree on $R[p]$, and $moved[p]$ stays false.

Consider an iteration that does not return. Line L7 found some $j$ whose $seq$ changed, and line L10 found $moved[j]$ false for each such $j$ (or it would have returned), so line L12 sets at least one entry of $moved$ from false to true. Only the $n - 1$ entries other than $moved[p]$ can become true. So after at most $n - 1$ iterations that do not return, every $j \ne p$ is marked. In the next iteration, either no $seq$ changed and line L8 returns, or some $j \ne p$ changed, $moved[j]$ is true, and line L11 returns. So $S$ ends within $n$ iterations. Each iteration reads $2n$ registers in lines L5 and L6, so $S$ does at most $2n \cdot n = 2n^2$ reads. An update is one scan and one write. $\square$

**Remarks.** The bound does not depend on the speed of the other processes, so the object is wait-free. The proof uses the fact that $seq$ values never repeat; this is why the registers are unbounded. Afek et al. also give a version with bounded registers, which replaces the sequence numbers by handshake bits and a toggle bit; its proof is different and is not given here.
