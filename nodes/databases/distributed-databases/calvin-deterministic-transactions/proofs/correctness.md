---
title: Every Calvin replica executes the input log as if the transactions ran one at a time in log order
proves: [correctness, messages]
status: full
---

We use the line numbers of the pseudocode on the page. The model is the model of the page and of the toy code. Each replica has one scheduler for each partition, and each item lives on one partition. A transaction $T$ declares its read set $R(T)$ and write set $W(T)$, and its logic is a deterministic function of the values of $R(T)$; it returns new values for some items of $W(T)$, or an abort. Messages inside a replica arrive in any order and are not lost while the replica is up. The input log, the batch of each sequencer for each epoch, is the same for every replica (in Calvin, Paxos agrees on it; the proof takes it as given).

The *global order* is the order of the log: epoch by epoch, and inside an epoch the batch of sequencer 1, then the batch of sequencer 2, and so on, each batch in its own order. Write it $T_1, T_2, \dots$. The *active participants* of $T$ are the partitions that hold an item of $W(T)$ (of $R(T)$ if $W(T)$ is empty). The *serial execution* runs $T_1, T_2, \dots$ one at a time on the initial state.

**Lemma 1 (the same order everywhere).** At every scheduler, line L4 handles the transactions that touch its partition in the global order.

*Proof.* Line L3 starts epoch $e$ only when the batch of every sequencer for $e$ has arrived, and it takes the batches in sequencer order. It finishes epoch $e$ before it starts $e + 1$. Messages can arrive in any order, but the batches are buffered until line L3 uses them. $\square$

**Lemma 2 (the lock queues).** At each item $k$, the lock queue holds the transactions that access $k$ in the global order. An entry of $T_i$ is granted only when every earlier entry that conflicts with it (one of the two is an X lock) has left the queue.

*Proof.* Line L4 adds all locks of a transaction at once, in the order of Lemma 1. Line L5 grants an entry only if every entry in front of it is compatible with it. An entry leaves the queue only when its transaction releases its locks at that partition. $\square$

**Lemma 3 (progress).** If the replica stays up, every transaction finishes at every partition it touches, and no transaction waits for a later one.

*Proof.* By induction on $i$. Suppose $T_1, \dots, T_{i-1}$ finish everywhere. At each partition $q$ of $T_i$, every entry in front of the entries of $T_i$ belongs to an earlier transaction (Lemma 2), so it leaves the queue, and $T_i$ gets all its local locks. Entries behind it never block it. So every partition of $T_i$ reaches line L6 and sends its local reads to the active participants (line L7). A partition that is not an active participant releases at once (line L8). Each active participant gets the reads of every partition of $R(T_i)$, since messages are not lost, and finishes at lines L9 to L11. $\square$

Lemma 3 shows that the toy has no deadlock: every wait is for an earlier transaction in the global order, so the waits cannot form a cycle.

**Theorem 1 (serial equivalence).** At every replica that stays up, each transaction $T_i$ reads the same values as in the serial execution, makes the same decision (commit with the same writes, or abort), and the final state equals the final state of the serial execution.

*Proof.* By induction on $i$ we show that when a partition $q$ reads an item $k \in R(T_i)$ at line L6, the value of $k$ is its value after $T_1, \dots, T_{i-1}$ in the serial execution, and that $T_i$ writes the same values as in the serial execution.

Let $T_j$ with $j < i$ write $k$. Its X entry on $k$ is in front of the entry of $T_i$ and conflicts with it, so by Lemma 2 $T_i$ reads $k$ only after $T_j$ has released its lock at $q$. The partition $q$ holds $k \in W(T_j)$, so it is an active participant of $T_j$, and it releases the lock only after line L11 has stored the writes of $T_j$. Let $T_m$ with $m > i$ write $k$. Its X entry is behind the entry of $T_i$, so it is granted only after $T_i$ releases its lock at $q$, and $q$ does this after line L6 (at line L8 or after line L11). So when $T_i$ reads $k$, every earlier writer of $k$ has stored its value and no later writer has. The writers of $k$ also store their values in the global order, by the same argument. By the induction hypothesis each earlier writer stored its serial value, so $T_i$ reads the serial value of $k$.

Each active participant of $T_i$ runs the logic (line L10) on the values from every partition of $R(T_i)$, that is, on the serial values of all of $R(T_i)$. The logic is deterministic, so each of them computes the serial decision and the serial writes, and each stores the writes to its own items (line L11). This finishes the induction. By Lemma 3 every transaction finishes, and the last writer of each item in the global order stores the last value, as in the serial execution. $\blacksquare$

**Consequences.** Two replicas that apply the same log reach the same state, with no message between them; this is why Calvin needs no [two-phase commit](/two-phase-commit/). An abort caused by the logic is decided by every active participant from the same values, so no vote is needed. A replica that crashed is rebuilt by running the log again from the initial state (or from a checkpoint taken at a point of the global order). The rebuilt replica satisfies Theorem 1, so it reaches the same state as the others. A replica that is down does not stop the others, because no step of one replica waits for a message from another replica.

**OLLP.** A dependent transaction runs first a reconnaissance read with no locks, and declares the read and write sets that this read predicts. Its logic reads the items that the prediction used again, and returns RESTART if they changed. RESTART is a deterministic decision with no writes, so Theorem 1 holds for the log that contains the failed attempt, and every replica decides the same restart. The client then sends a new attempt, which is a new transaction in a later position of the log.

**Theorem 2 (messages).** In each replica, a transaction sends $\sum_{s} |A(T) \setminus \{s\}|$ messages in phase 3, over the partitions $s$ of $R(T)$, where $A(T)$ is the set of active participants. If $T$ touches $p$ partitions, this is at most $p(p - 1)$. There is no commit message. Each sequencer sends one batch message per epoch to each scheduler of each replica.

*Proof.* Each partition of $R(T)$ sends one message at line L7 to each active participant other than itself, and nothing else is sent for $T$. With $a = |R(T)|$ partitions of reads, $b = |A(T)|$ active participants and $c$ partitions in both sets, the count is $ab - c$ and $a + b - c \le p$. For a fixed $c$ the product is largest when $a = b = (p + c)/2$, which gives $(p + c)^2/4 - c$. This grows with $c$ for $p + c \ge 2$, so the largest value is at $c = p$, that is, $p^2 - p$. $\blacksquare$
