---
title: Undo/redo recovery leaves every item with its last committed value
proves: [correctness]
status: full
---

**Model.** Each item $X$ is a page with one value and a pageLSN. The schedule is strict: after a transaction $T$ writes $X$, no other transaction writes $X$ until $T$ ends, by its commit (line L5) or by its rollback (lines L6 and L7, one step). The buffer manager may call OUTPUT (lines L3 and L4) on any dirty item at any time, also during recovery. A commit is reported only after its commit record is stable (line L5). Lines L8, L9 and L10 are three separate steps, and other steps can run between them; line L9 is one step. A crash keeps the disk and the stable log $R$ and loses the buffer, the log tail and the lists of updates. The log only grows at its end, so $R$ is always a prefix of the log that the run appended.

For an item $X$, the *target* $\tau(X)$ is the after image of the newest update on $X$ in $R$ by a transaction with a commit record in $R$, or the initial value of $X$ if there is no such update. Write $C^*$ for the set of transactions with a commit record in $R$.

**Lemma 1 (order).** Among the transactions that write $X$ and commit, the order of their updates on $X$ in the log is the order of their commits.

*Proof.* If $T_1$ writes $X$ before $T_2$ does, strictness puts the end of $T_1$ between the two writes, and $T_2$ commits after its own write. $\square$

So $\tau(X)$ is the value of $X$ after the committed transactions run one after the other in commit order, which is what the [crash recovery problem](/crash-recovery/) asks for.

**Lemma 2 (current value).** In normal processing, the current value of $X$ (the buffer copy if $X$ is dirty, else the disk copy) is the newest after image of the active transaction that has written $X$, if there is one; otherwise it is the after image of the newest update on $X$ by a transaction that has committed, or the initial value.

*Proof.* By induction on the steps, starting from a state where every item holds its last committed value (the initial state, or the end of a recovery by the Theorem below). Line L2 sets the value to the new after image, and by strictness the writer is the only active writer of $X$. A commit makes the active writer's last after image the newest committed one. Line L6 puts back, newest first, the before images of the aborting transaction; the oldest of them was the current value just before that transaction first wrote $X$, which by the induction and strictness was the last committed value, and no commit on $X$ happened in between. Lines L3 and L4 copy the value from the buffer to the disk and do not change it. $\square$

**Lemma 3 (UR1).** At every time, if the disk copy of $X$ holds an effect of an update record $u$, then $u$ is in $R$.

*Proof.* Every change to the buffer copy of $X$ sets its pageLSN to the LSN of the record it applies (lines L2 and L17, L19), or keeps a pageLSN at least as large (line L6). So the pageLSN is at least the LSN of every record whose effect the copy holds. Line L3 makes the log stable up to that pageLSN before line L4 writes the copy. $\square$

**Lemma 4 (passes).** Let $s$ and $L$ come from line L11 and $U$ from line L12. The undo pass reads every record with LSN at least $s$ and every update of a transaction in $L$. When the redo pass starts, $C \cap U = C^* \cap U$, and every update with LSN larger than $s$ is by a transaction in $U$.

*Proof.* Line L14 stops only below $s$ and only when the pass has read the start record of each transaction in $L$. Those start records are in $R$, since line L8 made the log stable up to the checkpoint start, and each one comes before all updates of its transaction. A transaction in $U$ was active at the checkpoint start or started after it, so its commit record, if any, has LSN larger than $s$, and line L15 has read it. A transaction that writes after the checkpoint start is active then, so it is in $L$ or its start record is after $s$. When there is no checkpoint, $s = 0$, the pass reads all of $R$, and $U$ holds every transaction. $\square$

Lines L15 to L17 meet the commit record of a transaction before its updates, because the pass goes backwards. So line L17 undoes exactly the updates in the pass by transactions in $U \setminus C^*$, newest first, and line L19 redoes exactly the updates after $s$ by transactions in $C^*$, oldest first.

**Theorem.** When RECOVER ends, after any number of crashes in normal processing or in earlier runs of RECOVER, every item $X$ holds $\tau(X)$ on disk and is clean.

*Proof.* A run of RECOVER appends nothing before line L21, so all runs that crash before line L21 ends see the same $R$. Each run computes the value it gives to $X$ from $R$ alone, and only for the items that lines L17 and L19 touch; it writes the others never. So a crashed run changes only touched items, and the last run writes all touched items again (line L20, or an OUTPUT after the last change). The records that line L21 adds are abort records, which no line of RECOVER reads. So it is enough to show that one full run gives $\tau(X)$, from the disk that the crash left. Fix $X$. There are three cases.

Case A: some update on $X$ after $s$ is by a transaction in $C^*$. Line L19 runs after all of line L17, and its last change to $X$ is the newest such update. By Lemma 4 every update of a transaction in $C^*$ after $s$ is redone, and an update on $X$ by $C^*$ before $s$ is older. So $X$ gets $\tau(X)$.

Case B: no update on $X$ after $s$ is by $C^*$, but some update on $X$ in the undo pass is by a transaction in $U \setminus C^*$. Line L19 does not touch $X$. Line L17 undoes these updates newest first, so $X$ ends with the before image $v$ of the oldest one, $e$, by transaction $T_e$. No earlier update of $T_e$ on $X$ exists (it would be older than $e$ and also undone), so $e$ is the first write of $T_e$ to $X$, and by Lemma 2 and strictness, $v$ is the after image of the newest committed update on $X$ before $e$, or the initial value. This is $\tau(X)$ unless some update $c$ on $X$ by $C^*$ has LSN larger than $e$. Suppose there is one. In case B, $c$ is before $s$. By strictness $T_e$ ended before $c$, and it did not commit (its commit would be in $R$ after $s$, by Lemma 4). So $T_e$ ended before $c$ by a rollback, or by a crash and a recovery that undid it, and in both cases before the checkpoint start. Then $T_e$ is not in $L$ and did not start after $s$, so $T_e \notin U$, a contradiction.

Case C: neither. Recovery does not touch $X$, so $X$ keeps its disk copy. If $s = 0$, $U$ holds every transaction, so no update on $X$ is in $R$, by Lemma 3 the disk copy is the initial value, and $\tau(X)$ is the initial value. If $s > 0$, by Lemma 4 every update on $X$ after $s$ is by $U$, and in case C there is none, by $C^*$ or by $U \setminus C^*$. Let $t$ be the time of line L9. At $t$ the disk copy of $X$ equals its current value. If an active transaction $T$ had written $X$ at $t$, then $T$ was active at the checkpoint start, so $T \in L \subseteq U$, and $T$ is not in $U \setminus C^*$, so $T$ committed later with no further write to $X$; its last write is the newest update on $X$ in $R$ and is $\tau(X)$, and by Lemma 2 it is the current value at $t$. If no active transaction had written $X$, Lemma 2 gives the last committed value at $t$, and no later update on $X$ exists, so this is $\tau(X)$. After $t$ the disk copy changes only by line L4 on a dirty copy, and a copy becomes dirty only by an update on $X$, which does not exist after $t$.

In all cases line L20 writes the touched items, so at the end every item is clean and holds $\tau(X)$. $\square$

**Corollary (cost).** One run of RECOVER reads each record from the end of $R$ back to the oldest start record of a transaction in $L$ (or to the checkpoint start, if that is older) once, then the records after $s$ once more. Each touched item is written at least once and at most once per OUTPUT. Without a checkpoint, both passes read all of $R$.

**Remark (order of the passes).** The proof of case A uses that line L19 runs after line L17. If redo ran first, case A would fail when a transaction that aborted in normal processing wrote $X$ before a committed transaction did: its undo would come last and put back its old before image. The test file builds this case. A system that logs each rollback step and redoes it, as ARIES does with compensation log records, avoids the problem in a different way; this proof does not cover that variant. This model does not log rollbacks, which is why it undoes aborted transactions in recovery.
