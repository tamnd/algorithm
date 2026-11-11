---
title: Rollback with the undo log restores the old state
proves: [correctness]
status: full
---

We prove that a rollback with the undo log of the page (lines L1 to L5) restores every word to the value it had before the transaction first wrote it, provided that no other transaction writes those words in the meantime. We prove it for both forms of the log: one entry per word (the first write only) and one entry per write, with the rollback in reverse order.

**Setting.** One transaction writes $W = (a_1, v_1), \dots, (a_t, v_t)$ in order, in place, through the log. Let $A$ be the set of words in $W$. For $a \in A$, let $f(a)$ be the index of the first write to $a$, and let $M_0(a)$ be the value of $a$ just before that write.

**Assumption (isolation of written words).** From the first write of the transaction to a word $a$ until the end of the rollback, no other process writes $a$. An [eager-versioning](/eager-versioning/) STM gets this from a write lock that it takes at or before the first write ([encounter-time locking](/encounter-time-locking/)) and holds until the rollback ends.

**Lemma 1 (first-write-only log).** After the writes $W$, the log holds exactly one entry $(a, M_0(a))$ for each $a \in A$, and no other entry.

*Proof.* The write $(a_i, v_i)$ appends an entry at L2 if and only if $a_i$ is not yet logged (L1), that is, if and only if $i = f(a_i)$. At that moment, L2 reads $a_i$ just before the write at L3, so it saves $M_0(a_i)$ by the definition of $M_0$. Later writes to $a_i$ find it logged and add nothing. $\square$

**Lemma 2 (log with an entry per write).** With an entry at every write, the entries for a word $a$ are, in log order, $(a, M_0(a)), (a, u_1), \dots, (a, u_j)$, where $u_1, \dots, u_j$ are the values the transaction wrote to $a$ before its last write to $a$.

*Proof.* Each write to $a$ saves the value that $a$ holds just before it. The first saves $M_0(a)$. By the assumption, between two writes of the transaction to $a$ no one else writes $a$, so each later write saves the value of the previous write of the transaction. $\square$

**Theorem.** After the rollback (L4), $a = M_0(a)$ for every $a \in A$, and the words outside $A$ are not touched.

*Proof.* The rollback writes only words that appear in the log, which are words of $A$. With the first-write-only log, it writes $M_0(a)$ once for each $a$ (Lemma 1), so the order does not matter. With an entry per write, the rollback in reverse order writes the entries of $a$ from the last to the first, so the last write to $a$ is $(a, M_0(a))$ (Lemma 2), and by the assumption nothing else writes $a$ during the rollback. $\blacksquare$

**Why reverse order.** With an entry per write and forward order, the last value written to $a$ is $u_j$, the value of the transaction's second-to-last write, not $M_0(a)$. The test `test_with_an_entry_per_write_only_the_reverse_order_works` shows $x = 1$ after writes $0 \to 1 \to 2$ and a forward rollback.

**Why the assumption is needed.** Without the write lock, two things go wrong, and the tests show both. A reader can see a value that is later undone (a dirty read). And a rollback can wipe out a committed write: if $T_2$ writes $x = 7$ in place and commits after $T_1$ wrote $x = 1$ with $x = 0$ in its log, the rollback of $T_1$ sets $x = 0$, and the write of $T_2$ is lost.
