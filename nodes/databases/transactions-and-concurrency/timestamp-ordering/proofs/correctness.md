---
title: Basic timestamp ordering accepts conflicting actions only in timestamp order
proves: [correctness]
status: full
---

**Setting.** Each attempt of a transaction has a timestamp, and different attempts have different timestamps (a restart gets a new one). For each item $x$ the scheduler keeps $\mathrm{rts}(x)$, the largest timestamp of an accepted read of $x$, and $\mathrm{wts}(x)$, the timestamp of the last accepted write of $x$; both start at $0$, below every timestamp. The rules are those of the pseudocode:

- a read $r_i(x)$ is rejected if $\mathrm{ts}(T_i) < \mathrm{wts}(x)$ (line L1), and otherwise accepted with $\mathrm{rts}(x) \leftarrow \max(\mathrm{rts}(x), \mathrm{ts}(T_i))$ (line L2);
- a write $w_i(x)$ is rejected if $\mathrm{ts}(T_i) < \mathrm{rts}(x)$ or $\mathrm{ts}(T_i) < \mathrm{wts}(x)$ (line L3), and otherwise accepted with $\mathrm{wts}(x) \leftarrow \mathrm{ts}(T_i)$ (line L4).

A rejected attempt aborts; it may restart as a new attempt with a larger timestamp (line L5).

**Lemma 1 (monotone stamps).** For each item $x$, $\mathrm{rts}(x)$ and $\mathrm{wts}(x)$ never decrease. At any time, $\mathrm{rts}(x)$ is at least the timestamp of every accepted read of $x$ so far, and $\mathrm{wts}(x)$ is at least the timestamp of every accepted write of $x$ so far.

*Proof.* Line L2 sets $\mathrm{rts}(x)$ to a maximum, so it never decreases and is at least each accepted read. Line L4 runs only when the test of line L3 failed, so $\mathrm{ts}(T_i) \ge \mathrm{wts}(x)$, and the new value is at least the old one. By induction, $\mathrm{wts}(x)$ is at least the timestamp of each accepted write. $\square$

**Theorem 1 (accepted conflicts are in timestamp order).** Let $p_i(x)$ and $q_j(x)$ be accepted actions of different attempts $T_i \ne T_j$ that conflict, with $p_i(x)$ accepted first. Then $\mathrm{ts}(T_i) < \mathrm{ts}(T_j)$.

*Proof.* Consider the moment at which $q_j(x)$ is accepted. If $p$ is a write, Lemma 1 gives $\mathrm{wts}(x) \ge \mathrm{ts}(T_i)$, and both rules accept $q_j(x)$ only if $\mathrm{ts}(T_j) \ge \mathrm{wts}(x)$. If $p$ is a read, then $q$ is a write, because the two actions conflict; Lemma 1 gives $\mathrm{rts}(x) \ge \mathrm{ts}(T_i)$, and line L3 accepts the write only if $\mathrm{ts}(T_j) \ge \mathrm{rts}(x)$. In both cases $\mathrm{ts}(T_j) \ge \mathrm{ts}(T_i)$, and the timestamps of different attempts differ, so $\mathrm{ts}(T_i) < \mathrm{ts}(T_j)$. $\square$

**Corollary 2 (serializability).** Let $C$ be the committed projection: the accepted actions of the attempts that commit. Every edge $T_i \to T_j$ of the conflict graph of $C$ has $\mathrm{ts}(T_i) < \mathrm{ts}(T_j)$, so the graph is acyclic and $C$ is conflict equivalent to the serial schedule of the committed attempts in timestamp order.

*Proof.* An edge of the conflict graph of $C$ comes from two conflicting actions of $C$, which are accepted actions, so Theorem 1 applies. Every edge goes from a smaller to a larger timestamp, so a cycle is impossible and the timestamp order is a topological order. By the theorem on [conflict serializability](/conflict-serializability/), $C$ is conflict equivalent to the serial schedule in that order. $\blacksquare$

**Theorem 3 (which schedules are accepted).** Feed a fixed schedule $S$ to the scheduler, with timestamps in the order in which the transactions first appear and no restarts. The scheduler accepts every action of $S$ if and only if every pair of conflicting actions $p_i(x) <_S q_j(x)$ has $\mathrm{ts}(T_i) < \mathrm{ts}(T_j)$.

*Proof.* If every action is accepted, Theorem 1 gives the condition. Conversely, assume the condition, and assume that all actions before some action $q_j(x)$ were accepted. By the condition, every earlier action on $x$ of another transaction that conflicts with $q_j(x)$ has a smaller timestamp than $T_j$. If $q$ is a read, the earlier writes of $x$ conflict with it, so all of them belong to $T_j$ or to older transactions, and $\mathrm{wts}(x) \le \mathrm{ts}(T_j)$: the read is accepted. If $q$ is a write, all earlier reads and writes of $x$ conflict with it or belong to $T_j$, so $\mathrm{rts}(x) \le \mathrm{ts}(T_j)$ and $\mathrm{wts}(x) \le \mathrm{ts}(T_j)$: the write is accepted. By induction, all actions are accepted. $\square$

So, with timestamps given at start, the schedules that basic TO passes unchanged are exactly the schedules whose conflict graph is consistent with the start order. This is a proper subset of the conflict serializable schedules. For example, $r_1(y)\, w_2(x)\, w_1(x)$ is conflict equivalent to the serial schedule $T_2 T_1$, but $T_1$ starts first, so $w_1(x)$ comes after a write of the younger $T_2$ and is rejected.

**What the theorem does not give.** Theorem 1 says nothing about values read from attempts that later abort. In $w_1(x)\, r_2(x)$ with $\mathrm{ts}(T_1) < \mathrm{ts}(T_2)$ both actions are accepted. If a later action of $T_1$ is rejected, $T_1$ aborts, and $T_2$ has read a value that never existed; if $T_2$ has already committed, the schedule is not recoverable. Basic TO therefore needs one more mechanism for recoverability, for example strict TO, which delays a read or write of $x$ until the transaction that wrote $\mathrm{wts}(x)$ has committed or aborted. In strict TO a transaction waits only for an older one, so the waits cannot form a cycle.
