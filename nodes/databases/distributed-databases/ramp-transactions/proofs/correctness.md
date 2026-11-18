---
title: RAMP-Fast and RAMP-Small reads are read atomic and never wait
proves: [correctness, messages]
status: full
---

We use the line numbers of the pseudocode on the page. The model is the model of the page and of the code: each item has one copy on one partition, clients send messages to partitions and partitions answer, messages arrive in any order and are not lost, and a writer client can crash at any moment and then sends nothing more. Timestamps are pairs (sequence number, client id), so two write transactions never have the same timestamp. The initial version of every item has the timestamp $\bot$, smaller than all others, and belongs to no write transaction.

We say that a write transaction $T$ with timestamp $t$ is *committed* when its client has passed line L3, that is, when it starts to send COMMIT messages. A version of $x$ with timestamp $t$ is a *sibling* of a version of $y$ with timestamp $t$: both come from the same transaction.

**Lemma 1 (siblings are present).** If some partition has $\mathrm{lastCommit}[x] = t \ne \bot$, or has ever had it, then $T$ is committed and every version that $T$ writes is in the set of versions of its partition.

*Proof.* A partition changes $\mathrm{lastCommit}[x]$ only at line L10, when a COMMIT$(x, t)$ arrives. The client sends COMMIT only at line L4, after line L3 saw a PREPARED answer for each item of $T$. A partition sends PREPARED only after line L9 has added the version. Versions are never removed (the code keeps them all). $\square$

**Lemma 2 (every request is answered at once).** Each GET of line L5 or L7, and each second round GET of RAMP-S, finds the version it asks for, so the partition answers in the same step.

*Proof.* A GET of line L5 asks for $\mathrm{lastCommit}[x]$, which is $\bot$ (always present) or a version that line L9 added before. In RAMP-F, line L7 asks for $x$ at a timestamp $t = v_{\mathrm{latest}}[x]$. This $t$ came from a version of some item $z$ that the reader got at line L5 from $\mathrm{lastCommit}[z]$, and the metadata of that version names $x$, so $T$ wrote $x$. By Lemma 1 the version of $x$ at $t$ is present. In RAMP-S, the partition of $x$ looks for the largest timestamp of the set $S$ of first round timestamps that it has for $x$. The timestamp that the reader got for $x$ itself is in $S$ and the partition has it, so the largest one exists. $\square$

**Theorem 1 (RAMP-F is read atomic).** Let a RAMP-F read of the items $I$ return the version of $x$ with timestamp $f[x]$ for each $x \in I$. If $f[x] = t \ne \bot$ and the transaction $T$ with timestamp $t$ also writes $y \in I$, then $f[y] \ge t$. Also $T$ is committed.

*Proof.* Let $r[x]$ be the timestamp that line L5 returned for $x$. After line L7, $f[x] = \max(r[x], v_{\mathrm{latest}}[x])$, where $v_{\mathrm{latest}}[x]$ is the largest $r[z]$ over the items $z \in I$ whose first round version names $x$ in its metadata ($\bot$ if there is none). The metadata of the version of $z$ at $t$ is the set of the other items of $T$.

*Case 1:* $f[x] = r[x] = t$. The first round version of $x$ has the metadata of $T$, which contains $y$. So line L6 gives $v_{\mathrm{latest}}[y] \ge t$ and $f[y] \ge t$.

*Case 2:* $f[x] = v_{\mathrm{latest}}[x] = t > r[x]$. Then $t = r[z]$ for an item $z \in I$ that $T$ wrote. If $z = y$, then $f[y] \ge r[y] = t$. If $z \ne y$, the metadata of the version of $z$ at $t$ contains $y$, so $v_{\mathrm{latest}}[y] \ge t$ and $f[y] \ge t$.

In both cases $t$ equals $r[z]$ for some $z$, and $r[z]$ was a value of $\mathrm{lastCommit}[z]$, so $T$ is committed by Lemma 1. $\blacksquare$

A read has a *fractured read* in the sense of Bailis et al. (2014, Section 3.1) if it returns a version of $x$ written by $T$ and a version of $y$ with a timestamp smaller than that of the version of $y$ that $T$ wrote. Theorem 1 says that this never happens, and that a read never returns a version of a transaction that is not committed. This is read atomic isolation. A writer that crashed before line L3 is never committed, and its prepared versions are never returned, because no $\mathrm{lastCommit}$ and no metadata of a committed version points to them.

**Theorem 2 (RAMP-S is read atomic).** The same statement holds for RAMP-S.

*Proof.* Let $S$ be the set of the first round timestamps, which are values of $\mathrm{lastCommit}$. The second round returns for $x$ the largest $t' \in S$ such that the partition of $x$ has a version of $x$ at $t'$, so $f[x] \in S$. Let $f[x] = t \ne \bot$ and let $T$ also write $y \in I$. Since $t \in S$, $t$ was a value of $\mathrm{lastCommit}$ at some partition, and by Lemma 1 the version of $y$ at $t$ is present at the partition of $y$. So $t$ is a candidate for $y$, and $f[y] \ge t$. Also $T$ is committed by Lemma 1. $\blacksquare$

**Theorem 3 (no waiting, rounds and messages).** Every operation finishes, whatever the other clients do and even if writers crash. Let a write have $w$ items and a read $r$ items, all on different partitions as in the code, which sends one message per item.

1. A write takes 2 round trips and $4w$ messages.
2. A RAMP-F read takes 1 or 2 round trips and $2r$ to $4r$ messages. It takes 1 round trip if, for each version that the first round returns, its transaction had committed at each of its other items $y \in I$ before the first round GET of $y$ was served. In particular, it takes 1 round trip when no write runs at the same time as the read.
3. A RAMP-S read always takes 2 round trips and $4r$ messages.

*Proof.* A partition handles each message with local work only (lines L9 to L11, and Lemma 2), and answers in the same step. A client waits only for answers from partitions to its own requests, never for another client. Since messages are not lost, each request is answered. A writer sends $w$ PREPARE messages and gets $w$ answers (line L2), then $w$ COMMIT messages and $w$ answers (line L4). A reader sends $r$ GET messages and gets $r$ answers (line L5). RAMP-F sends at most $r$ more GET messages at line L7; RAMP-S always sends $r$ more.

For the condition in part 2: if line L6 gives $v_{\mathrm{latest}}[x] = t$, then $t$ came from a first round version of an item $z \ne x$ written by the transaction $T$ with timestamp $t$, and $T$ also wrote $x$. By the condition, $T$ had committed at $x$ before the first round GET of $x$ was served. Line L10 never makes $\mathrm{lastCommit}[x]$ smaller, so $r[x] \ge t$ and line L7 does not ask for $x$. $\blacksquare$

**One round is not enough.** A reader that returns the first round values (the "naive" mode of the code) is not read atomic. Let $T_1$ write $x$ and $y$, and let the COMMIT of $T_1$ reach the partition of $x$ but not yet the partition of $y$. A reader of $x$ and $y$ then gets $x$ from $T_1$ and the initial version of $y$. The test file builds this case. RAMP-F sees $y$ in the metadata of $x$ and fetches $y$ at the timestamp of $T_1$ in a second round; RAMP-S fetches it because the timestamp of $T_1$ is in $S$.
