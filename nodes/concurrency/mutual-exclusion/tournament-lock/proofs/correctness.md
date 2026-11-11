---
title: The tournament lock with Peterson nodes gives mutual exclusion and starvation freedom, but no bound on bypass
proves: [correctness]
status: full
---

We use the pseudocode of the page. The tree is a complete binary tree with $size \ge n$ leaves, and process $i$ starts at leaf $i$. At each inner node $x$ there is a copy of Peterson's two-process lock with registers $flag[x][0]$, $flag[x][1]$ and $turn[x]$. A process that comes to $x$ from its child on side $s$ runs the code of Peterson's lock for side $s$ at $x$ (lines L2 to L6 there, and L8 for $x$ in the exit section). The registers are atomic and the memory is sequentially consistent. A process stays in the critical section for a finite time, and a process that is not in its remainder section takes another step eventually. We use the results of the proof for [Peterson's algorithm](/peterson-algorithm/): mutual exclusion, and starvation freedom when the critical section is finite.

**Terms.** Process $i$ *holds* node $x$ from the moment it leaves the loop L4 to L6 at $x$ until its write $flag[x][s] \leftarrow false$ at L8. For a leaf, say that process $i$ holds it from the start of its entry section until the end of its exit section. The *subtree on side $s$* of $x$ is the subtree of the child $c_s(x)$ of $x$ on side $s$.

**Lemma 1 (order of steps).** A process runs code of node $x$ only while it holds the child $c$ of $x$ on its path.

*Proof.* Process $i$ starts the code of $x$ at once after it leaves the loop at $c$, so it holds $c$ then. In the exit section it writes the flags from the root down to its leaf, so it writes $flag[x][s] \leftarrow false$ before it writes its flag at $c$, and it still holds $c$ during that write. For a leaf $c$ the claim holds by the definition of holding a leaf. $\square$

**Lemma 2 (mutual exclusion at each node).** For each inner node $x$, at most one process holds $x$ at any time.

*Proof.* By induction on the height of $x$. Assume that the claim holds for the children of $x$; for a child that is a leaf, at most one process holds it, since only process $i$ starts at leaf $i$. Fix a side $s$. The processes that run code of $x$ on side $s$ all come through the child $c_s(x)$, and by Lemma 1 each one does so only while it holds $c_s(x)$. By the induction, the times in which different processes hold $c_s(x)$ do not overlap. So the steps on side $s$ at $x$, in time order, are the steps of one passage of the Peterson code by one process, then one passage by another process, and so on, with no overlap. A new passage on side $s$ starts only after the last one wrote $flag[x][s] \leftarrow false$. Call this sequence of passages the *virtual process* of side $s$.

The two virtual processes of $x$ run Peterson's two-process code on the registers of $x$, and only they access those registers. Each run of the tree gives a run of Peterson's algorithm for the two virtual processes, in which the critical section of side $s$ is the time in which some process of side $s$ holds $x$. By the mutual exclusion of Peterson's algorithm, at most one virtual process, and so at most one process, holds $x$ at any time. $\square$

**Theorem 1 (mutual exclusion).** At most one process is in the critical section at any time.

*Proof.* A process in the critical section holds the root, so this is Lemma 2 for the root. $\square$

**Lemma 3.** In a fair run, every process that starts the code of an inner node $x$ (writes $flag[x][s] \leftarrow true$) later holds $x$ and then releases it.

*Proof.* By induction on the depth of $x$, from the root down. Look at the run of Peterson's algorithm of the two virtual processes at $x$, as in Lemma 2. A virtual process that is in its entry section is a real process in the loop at $x$, so it takes steps. Its critical section is finite: if $x$ is the root, the process enters the critical section, which is finite, and then writes $flag[x][s] \leftarrow false$ first in its exit section; if $x$ has a parent $y$, the process starts the code of $y$ at once, by the induction it holds $y$ and releases it, and its next write releases $x$. A virtual process with no passage in progress has its flag false, as a process in its remainder section has. So Peterson's starvation freedom applies: each passage of a virtual process gets into its critical section, that is, the process holds $x$, and then releases it. $\square$

**Theorem 2 (starvation freedom).** In a fair run, every process that starts its entry section enters the critical section.

*Proof.* The process starts the code of the lowest node on its path at once. By Lemma 3, applied up the path, it holds each node in turn, and when it holds the root it is in the critical section. $\square$

Deadlock freedom follows from Theorem 2.

**Theorem 3 (no bound on bypass for $n \ge 3$).** Take the doorway to be L2 and L3 at the lowest node of the path. For every $m$ there is a run in which process 0 has finished its doorway and the others enter $m$ times before it enters. So the lock is not first come, first served.

*Proof.* Let $n \ge 3$, so the tree has at least two levels. The lowest node $x$ of process 0 has leaves 0 and 1 below it, so the path of process 2 does not go through $x$. Process 0 writes $flag[x][0] \leftarrow true$ and $turn[x] \leftarrow 1$ and then takes no step. All other processes except 2 stay in their remainder sections. Process 2 then makes $m$ passages alone. At each node $y$ on its path, the flag of the other side is false: if process 0 is in the subtree of that side, it has only written a flag at $x$, which is below $y$; otherwise no process of that side has started. So process 2 passes each node without waiting and enters. Process 2 starts each passage after process 0 finished its doorway. The run is finite, so it can go on fairly, and then process 0 enters, by Theorem 2. For $n = 2$ the tree has one node and the lock is Peterson's algorithm, with bypass 1. $\blacksquare$
