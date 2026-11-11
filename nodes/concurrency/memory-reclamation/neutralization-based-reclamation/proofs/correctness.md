---
title: NBR never frees a node that a process can still access, frees each node once, and keeps at most n R retired nodes unfreed even if processes stop
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes on a sequentially consistent shared memory. Process $q$ owns $K$ reservation words $res[q][0..K-1]$, a local flag $restartable_q$ and a local retire list. We use the lines L1 to L8 of the page. Each attempt of an operation has a read phase, from L2 to L4, and a write phase, from L4 to the start of the next attempt or the end of the operation. A signal sent to $q$ at L6 stays pending until $q$ handles it. The client follows these rules.

1. **Reachability.** In a read phase, a process accesses a node $x$ only if $x$ was reachable from a root at the read that returned it. The stack reads from the root; the dequeue reads the head again before it uses $head.next$.
2. **Phases.** A read phase does not write to shared nodes and does not allocate, except for the own new node that is not yet published, so it can restart at any step. A write phase accesses only the nodes that its L3 put in the reservations, and the static roots.
3. **Retire after unlink.** RETIRE($x$) is called once per allocation of $x$, after the step that removed the last link to $x$, and a retired node is not linked again before it is freed.
4. **Prompt handling (Assumption 4 of the paper).** A process handles a pending signal before its next shared step. If it is restartable at that moment, it drops every local reference and starts a new attempt at L1. Otherwise it goes on.

The flag $restartable_q$ changes only between two steps of $q$: it becomes true at L2 after the clear of the old reservations, and false at L4 after the last reservation write at L3.

**Lemma 1 (no step, no phase change).** If $q$ takes no step in an interval, then $restartable_q$ and $res[q]$ do not change in it.

*Proof.* Only $q$ writes $res[q]$ and $restartable_q$. The writes to $res[q]$ are steps of $q$. The flag changes at L2 and L4, which run only after a step of $q$ returns, so between two steps of $q$ at most one local stretch runs, and it runs right after the earlier step. $\square$

**Lemma 2 (a non-restartable process is reserved).** If $q$ is not restartable at a time $t$ and is inside the write phase of an attempt, then every node that this write phase accesses was written to $res[q]$ at L3 before $t$, and stays there until the next L1 of $q$.

*Proof.* The write phase starts at L4, which runs after all writes of L3 of the same attempt. By rule 2 the write phase uses only those nodes. The words $res[q]$ change again only at L1 of the next attempt and at L3. $\square$

**Theorem 1 (safety).** If process $p$ frees $x$ at L8 at time $t_f$, then no process accesses this incarnation of $x$ after $t_f$.

*Proof.* Process $p$ retired $x$ at L5 after the unlink of $x$ (rule 3), then sent a signal to every other process at L6, then read all reservations at L7, and freed $x$ because no reservation named it. Let $q \ne p$ access $x$ at a step at time $t > t_f$. Let $t_s$ be the time of the signal from $p$ to $q$ in that scan, so $t_s < t_f < t$. The signal is pending from $t_s$, so by rule 4, $q$ handles it at its first step after $t_s$, and this is at or before $t$. Let $t_h$ be the time of that handling. Process $q$ takes no step in $(t_s, t_h)$, so by Lemma 1 its flag and its reservations at $t_h$ are the same as at $t_s$. There are three cases.

(a) $q$ is restartable at $t_h$. Then $q$ drops all references and starts a new attempt after $t_h$. Its reads in the new attempt are after $t_s$, so after the unlink of $x$, and by rules 1 and 3 none of them returns $x$. So $q$ has no way to reach $x$ at $t$.

(b) $q$ is not restartable at $t_h$, and the step at $t$ is in the write phase that $q$ is in at $t_h$. By Lemma 1, $q$ was in this write phase at $t_s$, so by Lemma 2, $x$ was in $res[q]$ before $t_s$ and stays there until the next L1 of $q$, which comes after $t$. The read of $res[q]$ by $p$ at L7 is between $t_s$ and $t_f < t$, so it sees $x$, and $p$ does not free $x$. This is a contradiction.

(c) The step at $t$ is in an attempt or operation of $q$ that starts after $t_h$. Its reads are after $t_s$ and after the unlink, so by rule 1 they do not return $x$, and by rule 2 its write phase uses only nodes that those reads returned.

So $q$ does not access $x$ after $t_f$. Process $p$ itself accesses only reserved nodes or nodes from new reads after the unlink, by the same argument with $t_h = t_s$. $\square$

**Theorem 2 (no double free).** Each incarnation of a node is freed at most once.

*Proof.* By rule 3, RETIRE($x$) puts $x$ in one retire list once. A scan frees a node only when it removes it from the list of its owner, and the scans of one process do not overlap. $\square$

**Theorem 3 (bound).** Let $R > n K$. At every time, each retire list holds at most $R$ nodes. So at most $n R$ retired nodes are unfreed, even if any number of processes stop at any point.

*Proof.* A list grows only by one node at L5. When it reaches $R$ nodes, the same RETIRE scans it, and L8 keeps only nodes that a reservation names. There are at most $n K$ reservation words, so at most $n K < R$ nodes stay. A process that stops at any step leaves its list at most $R$ long. A stopped process holds back no node in the list of another process, except the at most $K$ nodes in its own reservations, which are part of the $n K$ that a scan keeps. $\square$

If $R \le n K$, the same argument gives at most $n K + 1$ nodes per list, but then a scan may free nothing, so every retire sends signals.

**Theorem 4 (cost).** A read in the read phase costs no extra step. L1 and L3 cost at most $K$ writes each per attempt. A scan costs $n - 1$ signals, $n K$ reads and one free per freed node, and with $R \ge 2 n K$ it frees at least $R - n K \ge n K$ nodes, so the cost of a scan is $O(1)$ steps per freed node. A process restarts only when another process scans, and each scan follows a successful unlink, so the restarts do not stop the system from making progress. $\square$

Theorems 1 to 4 give the correctness of the method. $\blacksquare$
