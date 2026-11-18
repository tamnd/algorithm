---
title: New transactions after an instant restart read only committed values
proves: [correctness]
status: full
---

**Model.** This is the model of the implementation. Records are items $x$ on pages, each page with a pageLSN. A transaction writes an item with a physical update record that holds the before and the after value, and it holds a lock on each item that it reads or writes until its end record. The buffer obeys the write-ahead rule, a commit record is forced, and the policies are steal and no-force. Rollback of a transaction uses CLRs as in ARIES: the CLR for an update $u$ writes $u.\mathrm{before}$ and has undoNextLSN equal to $u.\mathrm{prevLSN}$. A crash keeps the disk and the stable log, which is a prefix of the log, and loses the rest. There are no checkpoints.

Restart runs lines L1 to L4: analysis builds, for each page $P$, the list $\mathrm{chain}[P]$ of the LSNs of all update and CLR records on $P$ in the stable log, in LSN order, and the set needRedo of these pages; it finds the losers with the head undoNext of each chain; and it gives each loser the lock on every item that its chain still has to undo. Then new transactions run. Every access to a page goes through FIX (lines L5 to L8), and every access to an item takes its lock through LOCK (lines L9 and L10).

The *committed value* of an item $x$ is the after value of the last update on $x$ by a committed transaction, or the initial value if there is none. A transaction is committed when its commit record is in the stable log. Under strict locking this is the value that $x$ has after a full ARIES restart.

**Lemma 1 (redo on demand).** After FIX$(P)$ returns, the buffered page $P$ holds the effect of all update and CLR records on $P$ in the stable log, in LSN order, and, after that, the effect of the records on $P$ written since the restart.

*Proof.* Before the first FIX$(P)$ after the restart, no record on $P$ has been written since the restart, because every write of a page (by a new transaction in WRITE, or by UNDO-STEP in line L12) calls FIX first. The disk version of $P$ with pageLSN $p$ holds the effect of the records on $P$ with LSN at most $p$, by the write-ahead rule and the pageLSN rule of normal work. Lines L6 and L7 apply the records of $\mathrm{chain}[P]$ with LSN above $p$ in LSN order, and $\mathrm{chain}[P]$ holds all records on $P$ of the stable log. Line L8 removes $P$ from needRedo, so later calls do not redo it again, and later records are applied by the action that writes them. $\square$

**Lemma 2 (loser locks).** From the end of line L3 until a loser $L$ ends, every item $x$ that an update on the chain of $L$ changed is locked by $L$. No other transaction writes or reads $x$ before $L$ ends.

*Proof.* Line L3 locks every such item. Under strict locking in normal work, two transactions never hold uncommitted updates on the same item, so line L3 never gives one item to two losers. LOCK, line L9, gives a lock held by a loser to another transaction only after ROLLBACK$(L)$ has run, that is, after the end record of $L$. Locks are released only in line L13 and at commit. $\square$

**Lemma 3 (undo).** When a loser $L$ ends, every update of $L$ in the log is compensated by a CLR, and each item that $L$ changed holds the value it had before the first update of $L$ on it.

*Proof.* The chain from undoNext$[L]$ through prevLSN for updates and undoNextLSN for CLRs visits exactly the updates of $L$ that are not yet compensated, newest first, as in ARIES. Line L11 and line L12 walk this chain and write one CLR per update. Line L12 calls FIX first, so by Lemma 1 the CLR is applied to a page that holds the whole history. By Lemma 2 no other transaction changed the item between the update and its CLR, so writing the before image undoes exactly this update. Applied newest first, the CLRs leave each item at the before value of the oldest update of $L$ on it. $\square$

**Theorem.** In the model, after a crash at any point, and after any number of later crashes, also during the instant phase or the background phase, (a) every read by a new transaction returns the committed value of the item, as it would after a full ARIES restart, and (b) when the background steps are done, every item holds the initial value plus the effect of the committed transactions, old and new.

*Proof.* (a) A new transaction $T$ reads $x$ only after LOCK$(T, x)$ succeeds. If a loser held the lock, line L9 has rolled it back, and by Lemma 3 $x$ holds the value before the loser's updates. If no loser held the lock, then by Lemma 2 no loser changed $x$, or its changes on $x$ are already compensated. Then FIX gives the page with the whole history by Lemma 1, and the last change of $x$ in it is by a committed transaction, by a compensated loser, or by a new transaction that committed before $T$ took the lock. This is the committed value.

(b) Line L14 fixes every page that is left in needRedo, and line L15 runs UNDO-STEP for every loser that is left until it ends. Each step makes progress, so the background phase ends with needRedo empty and no loser. By Lemma 1 and Lemma 3, the state is then the history of the stable log with every loser undone, plus the committed new transactions.

For a later crash, the new stable log is a prefix of the log, with the CLRs and end records written so far. The next analysis finds the CLRs, and the head of each loser skips the updates they compensate. The new transactions that did not commit are new losers of the same kind. So the same argument applies to the new stable log. $\square$

The tests check the theorem by a crash after every prefix of a random workload, by crashes during the instant phase and during background recovery, and by a hand example with the log records of the page.
