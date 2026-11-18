---
title: Primary copy locking gives one-copy serializable histories in commit order
proves: [correctness, messages]
status: full
---

We use the line numbers of the pseudocode on the page. The model is the model of the page and of the code.

**The model.** Each item $x$ has copies at a fixed set of sites, and one of them is the primary copy, at the site $P(x)$. Only $P(x)$ keeps locks for $x$, with S and X modes, and two locks of different transactions on $x$ conflict unless both are S. Channels between two sites are first in, first out, and messages are not lost. A site can fail by stopping. It then stays down, it loses its lock table, and a message to it comes back as "no response". A transaction that holds or waits for a lock at a failed site and has not reached line L7 aborts. For each item, at least one site with a copy stays up. A transaction reads an item at most once and does not read an item after it writes it. The history over copies records $r_T[x_A]$ when site $A$ returns a value and $w_T[x_A]$ when site $A$ installs a value. The 1SR definition is that of Bernstein, Hadzilacos and Goodman (1987), Section 8.3, as on the page [one-copy serializability](/one-copy-serializability/).

Let $\gamma_T$ be the moment of line L7 for a committed transaction $T$, and let $\mathcal{C}$ be the set of committed transactions, with the initial transaction $T_0$ first.

**Lemma 1 (lock intervals).** If $T \in \mathcal{C}$ gets a lock on $x$ at time $g$, and $P(x)$ releases it at time $\rho$ (or $P(x)$ fails at time $\rho$), then $g < \gamma_T < \rho$. For two committed transactions with conflicting locks on $x$, the intervals $[g, \rho]$ are disjoint, and their order is the order of the $\gamma$ values.

*Proof.* Line L7 runs only after the last operation of $T$ got its lock, and line L10 sends the release after line L7, so $g < \gamma_T < \rho$. Conflicting locks are never held together at $P(x)$, so two such intervals cannot overlap while $P(x)$ is up. After $P(x)$ fails, no lock on $x$ is granted again, so no interval starts after a failure. Each $\gamma$ is inside its own interval, so the intervals and the $\gamma$ values are in the same order. $\square$

**Lemma 2 (installs inside the X interval).** Let $U \in \mathcal{C}$ write $x$, with X interval $[g_U, \rho_U]$, and let $\rho_U$ be a release, not a failure of $P(x)$. Then every copy of $x$ at a site that is up when the install arrives installs the value of $U$ at a time in $(\gamma_U, \rho_U]$, and the primary copy installs it at $\rho_U$. If $\rho_U$ is a failure of $P(x)$, the copies at up sites still install the value of $U$ after $\gamma_U$, and no transaction gets a lock on $x$ after $\rho_U$.

*Proof.* Line L8 sends the installs after $\gamma_U$. Line L9 waits for an acknowledgment or "no response" from each copy that is not the primary, so each of these installs happens before line L10 sends the release, and so before $\rho_U$. The primary copy installs the value in the same step in which $P(x)$ handles the release (line L10). If $P(x)$ fails first, $U$ goes on with lines L8 to L10, because it has passed line L7, and $P(x)$ grants no lock after it fails. $\square$

So if some transaction gets a lock on $x$ after the X interval of $U$, that interval ended with a release, and all installs of $U$ at up sites happened before it.

**Lemma 3 (one order of installs).** For each copy $x_A$, the committed writes of $x$ are installed on $x_A$ in the order of their $\gamma$ values.

*Proof.* Take two committed writers $U$ and $V$ of $x$ with $\gamma_U < \gamma_V$. By Lemma 1, the X interval of $U$ ends before $V$ gets its X lock, so by the note after Lemma 2 it ended with a release, and $U$ installs on $x_A$ before $\rho_U$. $V$ installs after $\gamma_V > g_V > \rho_U$. $\square$

**Theorem 1 (one-copy serializability).** Every history of the protocol is one-copy serializable, with the serial order of the $\gamma$ values.

*Proof.* Let $T \in \mathcal{C}$ read $x$, with the S lock interval $[g_T, \rho_T]$, at the copy $x_A$ at time $t$ with $g_T < t < \gamma_T$. Line L4 reads the local copy, or the primary copy if there is no local copy or its site is down; a read at a down site returns nothing, so $A$ is up at $t$. Let $U$ be the writer of $x$ with the largest $\gamma_U < \gamma_T$, or $T_0$.

Every committed writer $V$ of $x$ has an X interval that is disjoint from $[g_T, \rho_T]$ by Lemma 1. If $\gamma_V < \gamma_T$, the interval of $V$ ends before $g_T$, so by the note after Lemma 2 its install on $x_A$ happens before $g_T < t$, because $A$ is up at $t$ and so was up before. If $\gamma_V > \gamma_T$, the interval of $V$ starts after $\rho_T > t$, so its install on $x_A$ happens after $t$. So the writes installed on $x_A$ before $t$ are exactly those of the writers with $\gamma_V < \gamma_T$, and by Lemma 3 the last of them is the write of $U$. So $T$ reads $x$ from $U$ in the history. In the serial order of the $\gamma$ values, $T$ also reads $x$ from $U$, the last writer of $x$ before $T$; $T$ does not read its own write. Each read of $T$ in one history is one read of $T$ in the other, so the reads-from relations are equal.

For the final writes, let $W$ be the writer of $x$ with the largest $\gamma$. At least one site with a copy $x_A$ of $x$ stays up, so by Lemma 2 $x_A$ installs the value of $W$, and by Lemma 3 no committed write is installed on $x_A$ after it. So $w_W[x_A]$ is the final write of $x_A$. $\blacksquare$

**Where each part is used.** The proof uses two facts at the primary: the X lock covers the installs at all copies (Lemma 2), and the S lock covers the read (Theorem 1). If the primary releases the X lock when the installs are sent instead of when they are acknowledged, Lemma 2 fails. The test file finds such a history: $T_3$ writes $x$, the primary $A$ installs and releases, $T_2$ locks $x$ at $A$ and reads its local copy $x_C$ before the install of $T_3$ arrives there. $T_2$ reads $x$ from $T_0$ although $T_3$ committed before it, and the history has no one-copy serial order.

**Theorem 2 (messages).** Count only messages between different sites. Let the home site of $T$ hold no copy and let the items of $T$ have different primary sites. A read costs 2 messages, a write of an item with $n$ copies costs $2 + 2(n - 1) = 2n$ messages, and the release costs one message per primary site. So $T$ with $r$ reads and $w$ writes on items with at most $n$ copies sends at most $3r + w(2n + 1)$ messages.

*Proof.* A read sends a lock request to the primary, and the grant carries the value of the primary copy (lines L3 and L4): 2 messages. A write sends a lock request and gets a grant (line L6), and at commit one install and one acknowledgment per copy other than the primary (lines L8 and L9). Line L10 sends one release to each primary site. A read of a local copy that is not the primary costs the same 2 messages for the lock and none for the read. $\blacksquare$
