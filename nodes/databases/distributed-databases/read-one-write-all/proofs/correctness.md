---
title: The available copies form of read-one write-all gives one-copy serializable histories
proves: [correctness, messages]
status: full
---

We use the line numbers of the pseudocode on the page. This proof is for the simplified model of the page, which is also the model of the code. It follows the argument of Bernstein, Hadzilacos and Goodman (1987), Section 8.6, in a shorter form.

**The model.** Each item $x$ has copies $x_A$ at a fixed set of sites. Sites fail by stopping. A failed site loses its lock table and its queued requests, and it keeps the values of its copies. A request to a failed site comes back as "no response", and only a failed site gives that answer. A site that recovers starts a new epoch, marks all its copies unreadable and refuses reads on them. A write to an unreadable copy is allowed, and a copy becomes readable when a committed write is installed on it. Each site runs strict two-phase locking on its own copies: a read holds an S lock on the copy and a write holds an X lock, both until the end of the transaction, and two locks of different transactions on one copy conflict unless both are S. A write is staged at the site when its lock is granted and installed at commit. The validations of lines L11 to L14 and the commit of line L15 are one atomic step. This step stands for an atomic commitment protocol. A transaction reads an item at most once and does not read an item after it writes it. The copier of a recovered copy is an ordinary transaction that reads $x$ and writes the value to all copies of $x$, so it is part of the history like every other transaction.

The physical history $H$ is the sequence of copy actions in the order of the grants: $r_T[x_A]$ when $T$ gets the S lock on $x_A$, $w_T[x_A]$ when $T$ gets the X lock, and then $c_T$ or $a_T$. For a committed transaction $T$, let $\gamma_T$ be the moment of its commit step. Let $\mathcal{C}$ be the set of committed transactions, with the initial transaction $T_0$ that wrote every copy before the start.

**Definition (one-copy serializability).** $H$ is one-copy serializable if there is a serial order $S$ of $\mathcal{C}$, run on a database with one copy of each item, such that (a) $T$ reads $x$ from $U$ in $H$ (that is, $r_T[x_A]$ reads from $w_U[x_A]$ for some copy) exactly when $T$ reads $x$ from $U$ in $S$, and (b) for each item $x$, if $W$ writes $x$ last in $S$, then $w_W[x_A]$ is the last committed write on $x_A$ in $H$ for some copy $x_A$.

**Lemma 1 (held locks survive).** Let $T \in \mathcal{C}$ hold a lock on $x_A$ that it got at time $t$. Then site $A$ did not fail in the interval $[t, \gamma_T]$, and $T$ holds the lock during the whole interval.

*Proof.* At time $t$, $T$ records the epoch of $A$ (line L4 or L8). Line L14 runs at $\gamma_T$ and finds $A$ up and in the same epoch, or $T$ would abort. A failure of $A$ in $[t, \gamma_T]$ would put $A$ down, and a recovery after it would change the epoch, so there was no failure. Only a failure, the commit or an abort removes a lock, so $T$ holds it until $\gamma_T$. $\square$

**Lemma 2 (a committed write reaches every live copy).** Let $T \in \mathcal{C}$ write $x$. At the moment $\gamma_T$, every copy $x_A$ at a site that is up holds an X lock of $T$, and line L15 installs the write of $T$ on it. At least one such copy exists.

*Proof.* Line L7 sends a request to every copy of $x$, and line L8 waits for each answer. Take a copy $x_A$ at a site that is up at $\gamma_T$. If $A$ answered "no response", line L10 recorded $x_A$ as missed, and line L12 would abort $T$ because $A$ is up. So $A$ granted the lock, and by Lemma 1 $T$ still holds it at $\gamma_T$. Line L15 installs the staged value. Line L9 aborts $T$ if no copy granted, so some copy granted, and by Lemma 1 its site is up at $\gamma_T$. $\square$

For a time $t$ and an item $x$, let $\mathrm{last}(x, t)$ be the transaction of $\mathcal{C}$ that writes $x$ and has the largest $\gamma$ before $t$, or $T_0$ if there is none.

**Lemma 3 (readable copies are current).** At every time $t$ between two steps, every readable copy $x_A$ at a site that is up holds the value installed by $\mathrm{last}(x, t)$.

*Proof.* By induction on the steps. At the start, every copy holds the value of $T_0$. Only four kinds of step change a copy, its readability or $\mathrm{last}(x, t)$. A failure makes a site down, and a recovery makes all its copies unreadable, so neither step can break the claim. An abort installs nothing. A commit of a transaction $T$ that writes $x$ makes $T = \mathrm{last}(x, t)$ after the step, and by Lemma 2 it installs its value on every copy of $x$ at an up site. A commit of a transaction that does not write $x$ changes neither the copies of $x$ nor $\mathrm{last}(x, t)$. $\square$

**Lemma 4 (one order of grants).** If $U, V \in \mathcal{C}$ both write $x_A$, the order of $w_U[x_A]$ and $w_V[x_A]$ in $H$ is the order of $\gamma_U$ and $\gamma_V$. If $T \in \mathcal{C}$ reads $x_A$ at time $t$, then no transaction of $\mathcal{C}$ other than $T$ holds an X lock on $x_A$ at time $t$ or commits a write on $x_A$ in $[t, \gamma_T]$.

*Proof.* By Lemma 1, a committed transaction holds its lock on $x_A$ from the grant to its commit, with no failure of $A$ in between, so the lock table of $A$ is not cleared in that interval. Two X locks conflict, so the intervals of $U$ and $V$ are disjoint, and the one that is granted first commits first. The S lock of $T$ conflicts with an X lock, so the interval $[t, \gamma_T]$ of $T$ is disjoint from the X interval of every other committed writer of $x_A$. $\square$

So in $H$, the write that $r_T[x_A]$ reads from (the last committed write on $x_A$ before it) is the last write installed on $x_A$ before time $t$.

**Theorem 1 (one-copy serializability).** Every history of the protocol is one-copy serializable, with $S$ the order of the commit moments $\gamma$.

*Proof.* Let $T \in \mathcal{C}$ read $x$ at copy $x_A$ at time $t$, and let $U = \mathrm{last}(x, t)$. The copy is readable and its site is up, because the site granted the read, so by Lemma 3 and the note after Lemma 4, $T$ reads $x$ from $U$ in $H$. We show that $U$ is also the last writer of $x$ before $T$ in $S$. First, $\gamma_U < t < \gamma_T$. Suppose that some $V \in \mathcal{C}$, $V \neq T$, writes $x$ and has $t < \gamma_V < \gamma_T$. By Lemma 1, $A$ is up at $\gamma_V$, so by Lemma 2 $V$ holds an X lock on $x_A$ at $\gamma_V$. By Lemma 1, $T$ holds its S lock on $x_A$ at the same moment. The two locks conflict, which is impossible. No writer of $x$ has $\gamma$ between $\gamma_U$ and $t$, by the choice of $U$. A transaction does not read an item after it writes it, so $T$ does not read its own write. So $T$ reads $x$ from $U$ in $S$, and condition (a) holds in this direction. Each read of $T$ in $S$ is one read of $T$ in $H$, so condition (a) holds in both directions.

For condition (b), let $W$ be the last writer of $x$ in $S$, so $W$ has the largest $\gamma$ among the writers of $x$. By Lemma 2, some copy $x_A$ gets the write of $W$ at $\gamma_W$. No committed transaction writes $x_A$ after it, because by Lemma 4 such a write would come with a later commit. So $w_W[x_A]$ is the last committed write on $x_A$ in $H$. $\blacksquare$

**Plain ROWA.** Plain ROWA aborts at line L9 if any copy did not answer, so no transaction has missed copies. The proof above holds without change. With no failures at all, lines L11 to L14 never abort, and the proof shows that strict two-phase locking at the copies, with one read and all writes, is enough.

**Where each part is used.** The examples on the page show that no part can be left out. Without line L12, the history $r_1[x_A]\, r_2[y_C]\, w_1[y_D]\, w_2[x_B]\, c_1\, c_2$ commits after $A$ and $C$ fail; the copy level history is conflict serializable, but each transaction reads the item that the other one writes, before the write, so no serial one-copy order exists. Lemma 2 fails there, because $C$ is down and $D$ is up. A copier that writes only the recovered copy breaks Lemma 2 for itself: a reader that holds an S lock on another copy does not block the copier. The history $r_{1000}[x_B]\, r_3[x_B]\, w_{1000}[x_A]\, c_{1000}\, w_3[x_B]\, w_3[x_A]\, c_3$ from the test file is then possible, and it has no one-copy order.

**Theorem 2 (messages).** Let $n$ be the largest number of copies of an item. A transaction with $r$ reads and $w$ writes sends at most $2(r + w)n$ messages for its reads and writes. If every item has exactly $n$ copies and every read succeeds at the first copy it tries, it sends exactly $2r + 2wn$.

*Proof.* A read sends one request and gets one answer per copy it tries (lines L3 and L4), and it tries at most $n$ copies. A write sends one request to each copy and gets one answer (a grant or "no response") for each, at most $2n$ messages (lines L7 and L8). A write to $x$ always sends to every copy of $x$, so with $n$ copies of each item and one try per read the count is exactly $2r + 2wn$. The messages of the atomic commitment protocol of line L15 are not counted. $\blacksquare$
