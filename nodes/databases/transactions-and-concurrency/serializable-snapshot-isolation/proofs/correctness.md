---
title: Committed transactions under serializable snapshot isolation are one-copy serializable
proves: [correctness]
status: full
---

**Model.** The committed transactions of a run form a multiversion history. $T_i \xrightarrow{rw} T_j$ means that $T_i$ reads a version of an item $x$ and $T_j$ commits a later version of $x$. Two transactions are concurrent if each starts before the other commits. We use the theorem of Fekete et al. (2005):

> If an SI history is not one-copy serializable, its dependency graph has a cycle, and the cycle has consecutive edges $T_1 \xrightarrow{rw} T_2 \xrightarrow{rw} T_3$ with $T_1, T_2$ concurrent and $T_2, T_3$ concurrent, where $T_1 = T_3$ is allowed.

**Lemma 1.** The committed transactions form an SI history.

*Proof.* A read returns the transaction's own write or the newest version committed at or before its start (line L7). A transaction commits only if no version of an item it wrote was committed after its start (line L13). These are the two rules of SI. The extra lines only abort transactions or set flags. $\square$

**Lemma 2.** Let $T_i \xrightarrow{rw} T_j$ with both committed, through item $x$. Then $T_i.out$ and $T_j.in$ are set no later than the later of the two operations $r_i(x)$ and $w_j(x)$.

*Proof.* $T_j$ commits its version after $T_i$ starts, since otherwise $T_i$ would have read that version or a newer one. So the two are concurrent.

- If $w_j(x)$ comes before $r_i(x)$, then at the read either $T_j$ is running with $x$ pending, and line L3 sets the flags, or $T_j$ has committed. In the second case it committed after $T_i.start$, so line L4 puts $T_j$ in $N$, and line L6 sets the flags. Line L6 runs because $T_i$ commits, so line L5 did not abort it.
- If $r_i(x)$ comes first, $T_i$ took an SIREAD lock at line L2. At $w_j(x)$ the lock is still there: $T_i$ did not abort, and line L16 drops it only if $T_i.commit \le$ the start of every running transaction, while $T_j$ is running with $T_j.start < T_i.commit$ (they are concurrent, and $T_i$ committed, so $T_j$ started before $T_i$ committed). So $T_i \in R$ at line L8, and line L10 sets the flags, as line L9 did not abort the committed $T_j$. $\square$

Flags are never cleared, so once set they stay set.

**Theorem.** The committed transactions of every SSI run are one-copy serializable.

*Proof.* By Lemma 1 the history is an SI history. Assume it is not serializable, and take $T_1 \xrightarrow{rw} T_2 \xrightarrow{rw} T_3$ from the theorem of Fekete et al., all committed. Let $e_1$ be the edge into $T_2$ (operations $r_1(x)$ and $w_2(x)$) and $e_2$ the edge out of $T_2$ (operations $r_2(y)$ and $w_3(y)$). Let $o$ be the later of the operations that complete the two edges, in the sense of Lemma 2.

*Case 1: $T_2$ has not committed at $o$.* By Lemma 2, both $T_2.in$ and $T_2.out$ are set before $T_2$ asks to commit. Line L12 aborts $T_2$, a contradiction.

*Case 2: $T_2$ has committed at $o$.* Then $o$ is not an operation of $T_2$. So either $o = r_1(x)$, which completes $e_1$ after $w_2(x)$, or $o = w_3(y)$, which completes $e_2$ after $r_2(y)$.

- If $o = r_1(x)$, the edge $e_2$ was completed earlier, so $T_2.out$ is set. $T_2$ committed a version of $x$ after $T_1.start$, so $T_2 \in N$ at line L4, and line L5 aborts $T_1$. A contradiction.
- If $o = w_3(y)$, the edge $e_1$ was completed earlier, so $T_2.in$ is set. $T_2$ holds an SIREAD lock on $y$ (as in Lemma 2) and has committed after $T_3.start$, so $T_2 \in R$ at line L8, and line L9 aborts $T_3$. A contradiction.

If $T_1 = T_3$ the same argument applies. So no such cycle exists, and the history is serializable. $\square$

**Remark (false positives).** The flags record that $T_2$ has an rw edge in and an rw edge out, but not that $T_3$ reaches $T_1$, and not that the other transactions committed. So SSI may abort a transaction in a serializable history. The node shows the chain $T_1 \xrightarrow{rw} T_2 \xrightarrow{rw} T_3$ with no cycle, where $T_2$ is aborted, and the write skew run in which both transactions abort.
