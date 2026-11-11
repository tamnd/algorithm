---
title: The anchor scheme of this page never frees a node that a process can still use, and keeps at most n R retired nodes unfreed
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes on a sequentially consistent shared memory with reads, writes, compare-and-swap and a compare-and-swap on two adjacent words. We prove the version on the page: a Michael and Scott queue whose nodes carry sequence numbers, with anchors that are sequence numbers, and a Treiber stack whose anchors are node addresses. Process $t$ has one shared word $ANCHOR[t]$ and a private list of retired nodes; $K \ge 1$ and $R > n (K + 1)$. The client follows four rules.

1. **Sequence numbers.** The queue keeps the pairs $(head, hseq)$ and $(tail, tseq)$, each in one double-width word, and changes them only with a double-width CAS that moves the pointer one node forward and adds 1 to the number. A new node gets the number $ts + 1$, where $(tl, ts)$ is the tail pair it links after. So along the queue the numbers grow by 1 per node, and $hseq$ is the number of the head node.
2. **Anchored access.** On the queue, a process reads a field of a node with number $s$ only while its anchor $a$ satisfies $a \le s \le a + K$, and only if, at a time after it wrote $a$, the queue held the node with number $a$, that is, $hseq \le a$. It gets this at L1 by the check that the head or tail pair did not change, and at L6 by the check of $hseq$. On the stack, a process reads a field of a node $x$ only while its anchor names $x$, and only if $top = x$ at a read after it wrote the anchor.
3. **Retire after removal.** A node is retired once, by the process whose CAS removed it, with its number on the queue.
4. **Free only in the scan.** A node is freed only at L10.

**Lemma 1 (removal in order).** On the queue, the node with number $s$ is removed by the CAS that moves $hseq$ from $s$ to $s + 1$. So at any time the removed nodes are exactly those with numbers below $hseq$, and two retired nodes that are not yet freed have different numbers.

*Proof.* By rule 1, the head CAS moves from the node with number $s$ to its successor, with number $s + 1$, and it is the only step that removes a node. $hseq$ only grows, so each number is removed once. A number is given to one node in the queue at a time, because a node is linked only after the current tail, so two nodes that were in the queue at any time have different numbers, as long as $hseq$ has not wrapped around, which a counter of 64 bits does not do in practice. $\square$

**Lemma 2 (a guarded node is retired after the anchor).** Let process $p$ access a queue node $x$ with number $s_x$ under anchor $a$ (rule 2). Then $x$ was retired after $p$ wrote $a$.

*Proof.* By rule 2, at a time $T$ after the write of $a$, $hseq \le a \le s_x$. By Lemma 1, $x$ was not removed at $T$, so by rule 3 it was retired after $T$. $\square$

**Theorem 1 (safety).** No process accesses a node after it is freed.

*Proof.* Let $p$ access a node $x$ under anchor $a$, and suppose some process $r$ frees $x$ at L10 before the access. The scan of $r$ started after $x$ was retired, so by Lemma 2 after $p$ wrote $a$. Its read of $ANCHOR[p]$ at L8 came before the free, so before the access. Between the write of $a$ and the access, $p$ did not change its anchor: it changes the anchor only at L1, at L5, or at the end, and after each change it accesses only nodes guarded by the new anchor. So L8 returned $a$, and since $a \le s_x \le a + K$, L9 keeps $x$, a contradiction. On the stack, the same argument holds with the anchor naming $x$ and $top = x$ after the write, as for [hazard pointers](/hazard-pointers/): $x$ was not removed at that read, so its retire and the scan come after the write. $\square$

**Theorem 2 (no double free).** Each node is freed at most once.

*Proof.* By rule 3, a node enters one private list once, and L10 removes it from the list when it frees it. $\square$

**Theorem 3 (bounded garbage).** At every time, at most $n R$ retired nodes are unfreed, even if some processes stop for good.

*Proof.* On the queue, an anchor $a$ guards the numbers $a$ to $a + K$, and by Lemma 1 at most one unfreed retired node has each number, so it keeps at most $K + 1$ nodes. On the stack, an anchor keeps at most one node. So a scan keeps at most $n (K + 1) < R$ nodes in the list of the scanner. A list grows by one node per retire and scans when it reaches $R$, so it never holds more than $R$ nodes. There are $n$ lists. $\square$

**Theorem 4 (cost).** A traversal of $L$ nodes makes $\lceil L / K \rceil$ anchor writes and as many checks, plus the reads of the nodes. A scan reads $n$ anchors and frees at least $R - n (K + 1)$ nodes, so with $R = 2 n (K + 1)$ its shared cost per retired node is $O(1)$ amortized. A traversal restarts only when the head passed its anchor, which needs a dequeue by another process, so the method keeps the queue lock free.

*Proof.* The anchor is written at L1 and then once every $K$ hops at L5, each followed by one check. The rest follows from Theorem 3 and from the code of L8 to L10. $\square$

Theorems 1 to 4 give the correctness of the method. $\blacksquare$
