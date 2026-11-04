---
title: The Swiss table keeps its invariant, and each find gives the right answer
proves: [correctness, termination]
status: full
---

We use the notation of the page: $G$ groups of $W$ slots, $G$ a power of two, $m = GW$, and for a key $k$ the probe sequence $g_i(k) = (h_1(k) + i(i+1)/2) \bmod G$. A slot is *full* when its control byte is in $\{0, \ldots, 127\}$, and *free* when it is EMPTY or DELETED. For a full slot $s$, $\text{grp}(s) = \lfloor s / W \rfloor$. The invariant is:

> **(S1)** A slot is full exactly when its control byte is in $\{0, \ldots, 127\}$, and then the byte is $h_2(\text{key}[s])$. No key is in two full slots. $n$ and $d$ are the numbers of full and of DELETED slots.
>
> **(S2)** For each full slot $s$ with key $k$, let $j$ be the least index with $g_j(k) = \text{grp}(s)$. Then none of the groups $g_0(k), \ldots, g_{j-1}(k)$ holds an EMPTY slot.
>
> **(S3)** $n + d \le \text{MaxFill}(m) \le m - 1$.

**Lemma 1 (coverage).** For each key $k$, the groups $g_0(k), \ldots, g_{G-1}(k)$ are all $G$ groups, each once. So the least index $j$ in (S2) exists and is less than $G$.

*Proof.* This is Lemma 1 of the quadratic probing proof, with $G = 2^p$ in place of $m$: the triangular numbers $i(i+1)/2$ for $0 \le i < 2^p$ are distinct modulo $2^p$. $\square$

**Lemma 2 (the variable $g$).** In SWISS-FIND and in lines L10 to L12 of SWISS-INSERT, the group $g$ in the iteration with counter $i$ is $g_i(k)$.

*Proof.* By induction on $i$. For $i = 0$, $g = h_1 \bmod G = g_0(k)$. Line L6 or L12 adds $i + 1$ to $g$ after it adds 1 to $i$, and $i(i+1)/2 + (i + 1) = (i+1)(i+2)/2$. $\square$

**Lemma 3 (find).** If (S1) to (S3) hold, SWISS-FIND$(T, k)$ returns the slot of $k$ if $k$ is in $T$, and NIL otherwise, and it looks at fewer than $G + 1$ groups. It changes nothing.

*Proof.* Line L4 returns a slot $s$ only if $\text{key}[s] = k$ and its byte is $h_2(k)$, which is a full slot by (S1), so a returned slot holds $k$. If $k$ is not in $T$, line L4 never returns, and the find returns NIL at line L5 or does not end. By (S3) some slot is EMPTY, so some group has an EMPTY slot. By Lemmas 1 and 2, iteration $i < G$ reaches that group, and line L5 returns there. So the find ends within $G$ iterations.

Now let $k$ be in the full slot $s$, and let $j$ be as in (S2). For $i < j$, the group $g_i(k)$ is not $\text{grp}(s)$, and $k$ is in no other slot by (S1), so line L4 does not return. By (S2) the group has no EMPTY slot, so line L5 does not return. In iteration $j$, the slot $s$ is in group $g_j(k)$ and its byte is $h_2(k)$ by (S1), so $s \in M$ and line L4 returns $s$. As $j < G$, at most $G$ groups are read. $\square$

**Lemma 4 (an EMPTY group stays EMPTY).** Say that a group is *open* when it holds an EMPTY slot. Between two rebuilds, a group that is not open never becomes open.

*Proof.* Only two lines write EMPTY: line L22, in a rebuild, and line L18. Line L18 writes EMPTY into a slot of a group that is open at that time. So no line makes a group open that was not open before. $\square$

**Lemma 5 (insert).** If (S1) to (S3) hold, then after SWISS-INSERT$(T, k, v)$ they hold again, $D(k) = v$, and the other pairs do not change.

*Proof.* By Lemma 3, line L7 finds the slot of $k$ if it is present, and line L8 then changes only its value, which keeps (S1) to (S3).

Otherwise $k$ is not in $T$. If line L9 calls REBUILD, assume for now that REBUILD gives a table with the same pairs in which (S1) to (S3) hold and $n + d + 1 \le \text{MaxFill}(m)$ (Lemma 7). So at line L10, $n + d + 1 \le \text{MaxFill}(m) \le m - 1$, and as $n + d < m$ some slot is free. By Lemmas 1 and 2, the loop of lines L11 and L12 ends at the first group $g_j(k)$ with a free slot, after $j < G$ steps. Line L13 takes a free slot $s$ of that group, line L14 updates $d$ if $s$ was DELETED, and line L15 makes $s$ full with byte $h_2(k)$ and adds 1 to $n$.

(S1) holds: $k$ was not present, so it is now in one slot, and the counts are right. (S3) holds: $n + d$ grows by 1 if $s$ was EMPTY and stays the same if $s$ was DELETED, and before the insert $n + d + 1 \le \text{MaxFill}(m)$. (S2) for $k$: the least index with $g_i(k) = \text{grp}(s)$ is $j$, because the groups $g_0(k), \ldots, g_{G-1}(k)$ are distinct. The groups $g_0(k), \ldots, g_{j-1}(k)$ had no free slot, so no EMPTY slot, and line L15 does not change them. (S2) for the other keys: they do not move, and the only change is that a free slot becomes full, which does not add an EMPTY slot to any group. $\square$

**Lemma 6 (erase).** If (S1) to (S3) hold, then after SWISS-ERASE$(T, k)$ they hold again, $k$ is not in $T$, and the other pairs do not change. The result is true exactly when $k$ was in $T$.

*Proof.* By Lemma 3, line L16 finds the slot $s$ of $k$, or NIL, and then line L17 returns false and nothing changes. Otherwise lines L18 to L20 make $s$ free and lower $n$ by 1, so $k$ is no longer in $T$, and (S1) holds with the new counts. $n + d$ does not grow, so (S3) holds.

For (S2), take another key $k'$ at a full slot $s'$, with its index $j'$. If line L19 runs, no slot becomes EMPTY, so (S2) for $k'$ still holds. If line L18 runs, the group $a = \text{grp}(s)$ was open before the erase. If $a$ were one of $g_0(k'), \ldots, g_{j'-1}(k')$, the old (S2) for $k'$ would say that $a$ is not open, which is false. So $a$ is not among these groups, and they do not change. (S2) for $k'$ holds. $\square$

**Lemma 7 (rebuild).** REBUILD makes a table with the same pairs in which (S1) to (S3) hold, $d = 0$, and $n + 1 \le \text{MaxFill}(m)/2$, where $m$ is the new number of slots. It ends.

*Proof.* Line L21 doubles $G'$ until $2(n + 1) \le \text{MaxFill}(G'W)$. This ends, because $\text{MaxFill}(G'W) \ge 7G'W/8 - 1$ grows without a bound. The new table has all slots EMPTY, so (S1) to (S3) hold with no pairs. Line L22 puts the old pairs in one at a time by lines L10 to L15. They are distinct keys, so each one is not yet present, and before each put $n + d + 1 \le n_{\text{old}} \le \text{MaxFill}/2 - 1$, so the argument of Lemma 5 applies to each put and keeps (S1) to (S3). At the end the table holds the old pairs, $d = 0$, and $n + 1 \le \text{MaxFill}(m)/2$. $\square$

**Theorem.** Start from a table of EMPTY slots and apply SWISS-INSERT, SWISS-ERASE and SWISS-FIND in any order. Then (S1) to (S3) hold after each operation, the pairs in the table are the map $D$ given by the operations, and each find returns the slot of its key or NIL as it should. Each operation ends.

*Proof.* The EMPTY table has $n = d = 0$ and no full slots, so (S1) to (S3) hold, and $D$ is empty. Lemmas 5 and 6 keep the invariant and change the pairs as the dictionary asks, and Lemma 3 gives the answer of each find. By induction on the number of operations, the claim holds after each one. Each find reads at most $G$ groups, each insert or erase runs one find, at most $G$ steps of lines L11 and L12, and at most one rebuild, and the rebuild ends by Lemma 7. $\blacksquare$

**Remark.** Lemma 4 is not used in the proofs above, but it explains line L18: an open group was open at each moment since the last rebuild, so no find for a present key has ever moved past it, and a slot there can be made EMPTY. Abseil's rule (count the slots that are not EMPTY next to the erased slot, and write EMPTY if the count is less than $W$) is the same idea for unaligned windows of $W$ slots: if no window of $W$ slots without an EMPTY slot covers the erased slot, no probe has moved past it.
