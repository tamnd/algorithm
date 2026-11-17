---
title: ARIES restart leaves exactly the surviving writes of committed transactions
proves: [correctness]
status: full
---

**Model.** A page holds records and a pageLSN. Locking is strict at the level of records, so between a write of a record by $T$ and the end of $T$ (its commit, or the end of its rollback) no other transaction writes that record. The buffer obeys the WAL rule: a page with pageLSN $n$ is written to disk only after the log is stable up to $n$. A commit is reported only after its commit record is stable. The master record names a begin_checkpoint record only after its end_checkpoint record is stable, and the copies in that end record are the exact ATT and DPT at the time the end record was appended. A crash keeps the disk, the stable log and the master record, and loses the rest. Every log record of a transaction except the first holds the transaction's previous LSN as its prevLSN.

For a transaction $T$ and a log prefix, define the *chain* of $T$: start at the newest update, CLR or abort record of $T$, and step from an update or abort record to its prevLSN and from a CLR to its undoNextLSN, until LSN 0. An update is *compensated* if a CLR in the prefix names it as undone.

**Lemma 1 (chain).** In every log prefix, the updates on the chain of $T$ are exactly the uncompensated updates of $T$, in decreasing LSN order, and the CLRs of $T$ each compensate a distinct update.

*Proof.* By induction on the records of $T$. An update record $u$ with prevLSN $p$ puts $u$ in front of the chain that starts at $p$: the claim holds. An abort record does not change the set of updates on the chain. Line L19 appends a CLR $c$ for the update $r$ at the head of the chain (the ATT's undoNext is the head, by the induction and by lines L20 and L21). It sets undoNextLSN to $r$.prevLSN, so the new chain is the old chain without $r$, and $r$ is now compensated. Since $r$ was on the chain, no earlier CLR compensates it. A CLR met at the head (line L21) is skipped to its undoNextLSN, which is the chain that it left. $\square$

**Lemma 2 (page).** At every time, a page version in the buffer or on disk with pageLSN $n$ holds, for each of its records, the value written by the newest update or CLR on that record with LSN at most $n$, or its initial value if there is none.

*Proof.* Normal processing sets the pageLSN to the LSN of each change it applies, and the LSNs increase. Redo applies a record $r$ only if pageLSN $< r$.lsn (line L11) and then sets pageLSN to $r$.lsn. If redo applies the records of a page in increasing LSN order starting from a version that satisfies the claim, each version it makes satisfies it, provided it skips no record on the page with LSN between the old pageLSN and the new one. Lemma 3 gives this. $\square$

**Lemma 3 (analysis).** After analysis, for every page $P$ and every update or CLR $r$ on $P$ in the stable log with $r$.lsn larger than the pageLSN of $P$ on disk, $P$ is in the DPT and DPT$[P] \le r$.lsn.

*Proof.* Let $D$ be the disk version of $P$ at the crash. Case 1: $r$ is after the begin_checkpoint named by the master record. Either $P$ entered the table from the checkpoint copy with a recLSN, or line L4 adds it at its first record after the end_checkpoint. If $P$ is in the copy, its recLSN is at most the LSN of the first change since the last write of $P$ before the end record; if that write is before $r$, the recLSN is at most $r$.lsn. If $P$ was written after the end_checkpoint and after $r$, then $D$ holds $r$ by the WAL order and pageLSN$(D) \ge r$.lsn, against the assumption. Case 2: $r$ is before the begin_checkpoint. Then $D$ lacks $r$, so $P$ was not written between $r$ and the crash. So at the end_checkpoint, $P$ was dirty with a change at or before $r$, and the exact DPT copy holds $P$ with recLSN $\le r$.lsn. Analysis does not remove pages from the DPT. $\square$

By Lemma 3, redo starts at a LSN no larger than any record missing from any disk page, and line L10 skips only records that the disk version already holds (if DPT$[P] > r$.lsn, the page was written after $r$, so pageLSN$(D) \ge r$.lsn). Pages written to disk during redo leave the live DPT, but line L10 uses the table as analysis left it, so this skips nothing. Hence, by Lemma 2, at the end of redo every page holds the effect of the whole stable log, in LSN order. This is *repeating history*.

**Lemma 4 (losers).** After line L7 the ATT holds exactly the transactions with a record in the stable log, no end record, and no commit record, each with undoNext equal to the head of its chain.

*Proof.* A transaction with a record before the checkpoint and none after it is in the checkpoint copy with its exact lastLSN and undoNext (it was active there) unless it had ended. Lines L3 and L5 then follow each later record: an update makes it the head, a CLR moves the head to the CLR's undoNextLSN, an end removes it. Line L7 ends the committed ones. $\square$

**Theorem.** After a RESTART that runs to the end, after any number of earlier crashes, also crashes during earlier restarts, every record holds the value of the newest uncompensated update by a transaction whose commit record is stable, or its initial value. The stable log holds at most one CLR per update.

*Proof.* After redo, the state is the effect of the stable log in order. Take a record $x$. Strictness gives: the writes to $x$ in log order form groups, one per transaction, and a group of $T$ is not interleaved with writes of another transaction to $x$ while $T$ is active. Each CLR on $x$ restores the before image of an update of the same transaction, so after a rollback (complete or partial) of the updates of $T$ on $x$ in reverse order, $x$ holds what it held before them.

The undo pass picks the loser with the largest undoNext (line L14) and undoes its head (line L15). By Lemma 4 and Lemma 1, the heads are exactly the uncompensated updates of losers, and the global order of undo is decreasing LSN. For a record $x$, the newest uncompensated write of a loser to $x$ is undone first, then the older ones, and its before image is the value that $x$ held before the loser's first uncompensated write, which by strictness was written by a winner or was the initial value, or was itself restored by an earlier CLR. So after undo, $x$ holds the newest uncompensated update of a winner. Winners' writes that a partial rollback removed are compensated, so they do not count, as the problem asks.

A crash during RESTART leaves a stable log that is a prefix of the log of the run. Redo is restartable by Lemma 2, since it only applies records that pages lack. Each CLR that reached the stable log has, by Lemma 1, moved the chain head past its update, so the next restart does not undo that update again and appends no second CLR for it. The end records written by line L7 or line L22 are idempotent: a second one for the same transaction is never written, because analysis removes a transaction at its first end record. $\square$

**Corollary (bounded log).** Over any sequence of crashes during recovery, the log holds at most one CLR for each update of a loser, and at most one end record for each transaction. So the log growth caused by recovery is linear in the size of the stable log at the first crash.
