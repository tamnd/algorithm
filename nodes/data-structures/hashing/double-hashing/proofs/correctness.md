---
title: Double hashing keeps its probe invariant and implements a dictionary
proves: [correctness, termination]
status: full
---

Write $p_k(i) = (h_1(k) + i \cdot h_2(k)) \bmod m$, and assume $\gcd(h_2(k), m) = 1$ for each key $k$. A slot is **free** when it is EMPTY or DELETED, and **occupied** when it holds a pair. The map of the table is the set $D$ of the pairs in occupied slots.

**Lemma 1 (the probe sequence is a permutation).** For each key $k$, the values $p_k(0), \ldots, p_k(m-1)$ are the $m$ slots, each exactly once.

*Proof.* Suppose $p_k(i) = p_k(i')$ with $0 \le i < i' \le m - 1$. Then $m$ divides $(i' - i) h_2(k)$. Since $\gcd(h_2(k), m) = 1$, $m$ divides $i' - i$. But $0 < i' - i < m$, a contradiction. So the $m$ values are distinct, and they are $m$ values in $\{0, \ldots, m-1\}$, so they are all the slots. $\square$

**Invariant.**

- **(D1)** If key $k$ is in slot $p_k(t)$, then none of $p_k(0), \ldots, p_k(t-1)$ is EMPTY.
- **(D2)** No key is in two occupied slots.

**Lemma 2 (complete scan).** Assume (D1) and (D2). Follow $p_k(0), p_k(1), \ldots$ and stop at the first EMPTY slot, or after $m$ probes. If $k$ is in the table, the scan meets its slot. If the scan does not meet $k$, then $k$ is not in the table.

*Proof.* If $k$ is in slot $p_k(t)$, then $t \le m - 1$ by Lemma 1, and by (D1) no slot before position $t$ is EMPTY, so the scan reaches position $t$. The second sentence is the contrapositive of the first. $\square$

**Theorem.** Start from a table with all slots EMPTY, and apply any sequence of DH-INSERT, DH-SEARCH and DH-DELETE. Each call ends after at most $m$ passes of its loop. After each call (D1) and (D2) hold, $D$ is the map that the same sequence gives on an abstract dictionary (except that an insert into a table with no free slot and without $k$ reports a full table and changes nothing), and each search returns the value of its key in $D$, or NIL.

*Proof.* **Termination.** Each loop runs with $i = 0, 1, \ldots, m - 1$, and $i$ grows by 1 at each pass, so it stops after at most $m$ passes.

**Base.** In the empty table no slot is occupied, so (D1) and (D2) hold, and $D$ is empty.

**Search.** The loop of lines L13 to L17 is the scan of Lemma 2. Line L16 returns the value of the occupied slot with key $k$, which is the only one by (D2). If the scan ends at EMPTY or after $m$ probes, $k$ is absent by Lemma 2 and NIL is right. No slot changes.

**Delete.** Lines L18 to L21 are the same scan. If they find $k$ in slot $q$, line L21 makes $q$ DELETED, so $D$ loses exactly the pair of $k$. No slot becomes EMPTY, so for each other key the slots before it on its path are still not EMPTY, and (D1) holds. (D2) holds since a pair was only removed. If the scan does not find $k$, then $k$ is absent and nothing changes.

**Insert.** The loop of lines L2 to L10 follows $p_k(0), p_k(1), \ldots$ and stops at the first EMPTY slot or after $m$ probes, so it is the scan of Lemma 2, with a key test on each occupied slot at line L9. If it finds $k$, line L10 changes only the value, so (D1), (D2) and the slots are as before, and $D$ maps $k$ to $v$.

Else $k$ is absent, by Lemma 2. During the scan, $j$ is set at lines L5 or L8 to the first free slot of the path, if the scan meets one. Let $j = p_k(t)$. All the slots $p_k(0), \ldots, p_k(t-1)$ were met before $j$ and were not free, so they are occupied, and in particular not EMPTY. If $j$ is NIL, the scan met no free slot. If it stopped at an EMPTY slot, that slot would have set $j$; so it made $m$ probes, all occupied, and by Lemma 1 every slot is occupied by a key other than $k$. Then line L11 reports a full table and changes nothing, as stated.

Otherwise line L12 puts $(k, v)$ in slot $p_k(t)$. Then (D1) holds for $k$, by the fact above. For each other key, line L12 turned a free slot into an occupied one, and no slot became EMPTY, so (D1) still holds for it. (D2) holds because $k$ was absent. $D$ gains exactly the pair $(k, v)$.

By induction on the number of calls, the claims hold after each call. $\blacksquare$
