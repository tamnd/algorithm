---
title: NOrec is opaque and aborts only when another transaction commits
proves: [correctness, opacity, progress]
status: full
---

We use the pseudocode of the page (lines L1 to L16) and its model: asynchronous processes, sequentially consistent memory with atomic read, write and compare-and-swap, and one shared word GL, the global sequence lock. "Await GL is even" at L1 and L10 is a spin loop; its result is a value of GL that is even at the moment of the last read of the loop.

**Lemma 1 (the sequence lock).** (a) GL never decreases. (b) GL changes only at a successful CAS at L14, from an even value $s$ to $s + 1$, and at L16, from $s + 1$ to $s + 2$, by the same transaction. (c) A data word is written only at L15, by a transaction whose CAS at L14 succeeded and which has not yet executed L16. So data words change only while GL is odd, and while GL is odd exactly one transaction, the one whose CAS made it odd, writes data words.

*Proof.* GL starts at 0. The only steps that write GL are the CAS at L14 and the write at L16. A CAS at L14 compares GL with the snapshot of the transaction, and a snapshot is always even (it comes from L1 or from L10 through L12). So a successful CAS changes an even $s$ into $s + 1$, and after it no other CAS can succeed until GL is even again. Only the transaction that made GL odd executes L15 and L16, and L16 writes $s + 2$. This gives (a), (b) and (c) by induction on the steps. $\square$

Call a transaction *effective* if its CAS at L14 succeeded. By Lemma 1 the effective transactions $C_1, C_2, \dots$ are totally ordered by their CAS, and $C_k$ changes GL from $2k - 2$ to $2k - 1$ and then to $2k$. Let $S_0$ be the initial memory and $S_k$ the result of applying the write sets of $C_1, \dots, C_k$ in this order. An effective transaction executes no ABORT after L14, so it writes its whole write set unless its process crashes.

**Lemma 2 (memory at an even value).** During any interval in which GL keeps the even value $2k$, the data words equal $S_k$.

*Proof.* When GL reaches $2k$ at L16 of $C_k$ (or at the start, for $k = 0$), $C_k$ has written its whole write set at L15, and no other transaction wrote a data word since $C_{k-1}$ finished (Lemma 1c). So the memory is $S_{k-1}$ updated by the writes of $C_k$, which is $S_k$. While GL stays at $2k$, no data word changes (Lemma 1c). $\square$

**Lemma 3 (the read log).** For each live transaction $T$, after each completed step of BEGIN, READ or VALIDATE: the snapshot $s$ of $T$ is even, GL had the value $s$ at some moment after $T$ began, and each pair $(a, v)$ in the read log of $T$ satisfies $v = S_{s/2}[a]$.

*Proof.* By induction on the steps of $T$.

*Begin (L1).* The snapshot is an even value of GL read after the begin, and the log is empty.

*Validate (L9 to L12).* Let $t$ be the even value returned at L10, at time $t_{10}$, and suppose L12 reads GL $= t$ at time $t_{12}$. By Lemma 1a, GL $= t$ during the whole interval $[t_{10}, t_{12}]$, so by Lemma 2 the memory equals $S_{t/2}$ during the reads of L11. If no read at L11 differs from the log, each logged $v$ equals $S_{t/2}[a]$, and VALIDATE returns $t$, which becomes the snapshot. If some read differs, $T$ aborts, and the claim is about live transactions only. If L12 finds another value, the loop starts again and the log has not changed.

*Read (L3 to L7).* Let $s$ be the snapshot before the read, and let $v$ be loaded at L3 (or at L6) at time $t_3$. The loop at L4 exits only when it reads GL $= s$, at some time $t_4 > t_3$. The snapshot $s$ is a value that GL had at some time $t_0 < t_3$ (by the induction hypothesis, or by the last VALIDATE inside the loop, which ends before L6). By Lemma 1a, GL $= s$ during $[t_0, t_4]$, so the load returned $S_{s/2}[a]$ by Lemma 2. The pairs already in the log satisfy the claim for $s$ by the hypothesis or by the validation. So after L7 every logged pair satisfies the claim. A read that finds $a$ in the write set at L2 adds nothing to the log. $\square$

**Lemma 4 (commit).** If the CAS at L14 of $T$ succeeds, so that $T = C_k$, then each pair $(a, v)$ in the read log of $T$ satisfies $v = S_{k-1}[a]$.

*Proof.* The CAS succeeds with GL $= s$, the snapshot of $T$, and then $k - 1 = s/2$. By Lemma 3 the log agrees with $S_{s/2}$. $\square$

**Theorem 1 (opacity).** Each finite history of NOrec is opaque.

*Proof.* Complete the history: each effective transaction without a commit event is completed as committed (it has passed its last abort point), and each other live or commit-pending transaction is completed as aborted. Give $C_k$ the position $k$. Give each other transaction $T$ the position $s_T/2 + \tfrac12$, where $s_T$ is its last snapshot. Order by position, and break ties between non-effective transactions by the time of their begin.

*Legality.* In this serial order, the effective transactions run in the order $C_1, C_2, \dots$, so the state before $C_k$ is $S_{k-1}$, and the state seen at position $s/2 + \tfrac12$ is $S_{s/2}$. A read that hits the write set (L2) returns the last write of the transaction, as in the serial run. Every other read that returned a value is in the read log, and it is the first access of that word by the transaction, because a word that the transaction has written is found at L2. By Lemma 3, for a non-effective transaction the logged values equal $S_{s_T/2}$. By Lemma 4, for $C_k$ they equal $S_{k-1}$. A read that ended in ABORT returned no value. Effective transactions write exactly their write sets, which is what $S$ applies. So the serial run is legal, and each transaction, aborted or not, reads the values of this run.

*Real-time order.* Let $T$ complete before $U$ begins. If $T = C_k$, then $T$ set GL to $2k$ before it completed, so every snapshot of $U$ is at least $2k$ (Lemma 1a). If $U$ is not effective, its position is at least $k + \tfrac12$. If $U = C_j$, its CAS succeeded on a snapshot of at least $2k$, so $j \ge k + 1$. If $T$ is not effective, its last snapshot $s_T$ is a value that GL had before $T$ completed, so every snapshot of $U$ is at least $s_T$. If $U = C_j$, then $j - 1 \ge s_T / 2$, so $j > s_T/2 + \tfrac12$. If $U$ is not effective, its position is at least that of $T$, and a tie is broken by the begin times, where $T$ comes first. $\blacksquare$

**Theorem 2 (aborts and failed CAS steps).** A transaction $T$ aborts, or its CAS at L14 fails, or its loop at L4 runs again, only if some effective transaction executed its CAS after $T$ took the snapshot in use.

*Proof.* An abort happens only at L11, when a data word differs from its logged value. By Lemma 3 the logged value is $S_{s/2}[a]$, the memory value when GL was $s$; a data word changes only at L15 of an effective transaction (Lemma 1c), and that transaction made its CAS after GL was $s$. A failed CAS at L14 and a new round of the loop at L4 both mean that GL differs from the snapshot $s$, and GL changes only by an effective transaction (Lemma 1b). $\square$

So NOrec cannot livelock: in a run where transactions keep aborting, other transactions keep committing. NOrec is still blocking: if the process of $C_k$ stops while GL is odd, every other transaction waits forever at L1 or L10. $\blacksquare$
