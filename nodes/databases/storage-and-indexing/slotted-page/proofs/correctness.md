---
title: The slotted page keeps its layout invariant, keeps record ids stable, and rejects a record only when it cannot fit
proves: [correctness]
status: full
---

We use the notation of the page. The page has $p$ bytes, a header of 4 bytes, $n$ slot entries of 4 bytes, and the free end $e$. A live slot $s$ has offset $o_s > 0$ and length $\ell_s$; a free slot holds $(0, 0)$. Let $S$ be the set of live slots, $G = e - 4 - 4n$ the gap and $F = p - 4 - 4n - \sum_{s \in S} \ell_s$ the total free space. The invariant is:

1. $4 + 4n \le e \le p$.
2. For $s \in S$, $e \le o_s$ and $o_s + \ell_s \le p$, and the intervals $[o_s, o_s + \ell_s)$ for $s \in S$ are pairwise disjoint.
3. $n = 0$ or $n - 1 \in S$.
4. For $s \in S$, the bytes at $[o_s, o_s + \ell_s)$ are the record last stored in slot $s$.

Let $M$ be the abstract map from slots to records. We also claim:

5. $S$ is the domain of $M$, and for $s \in S$, `get(s)` returns $M(s)$.

**Lemma 1.** If the invariant holds, then $G \le F$, and $G = F$ when the live records fill $[e, p)$ with no holes.

*Proof.* By part 2 the live intervals are disjoint subsets of $[e, p)$, so $\sum_{s \in S} \ell_s \le p - e$, which gives $F = p - 4 - 4n - \sum \ell_s \ge e - 4 - 4n = G$. Equality holds exactly when the intervals cover $[e, p)$. $\square$

**Lemma 2 (COMPACT).** If the invariant holds before COMPACT, it holds after it, $M$ does not change, $S$ and $n$ do not change, and afterwards $G = F$.

*Proof.* Let $s_1, \ldots, s_k$ be the live slots in the order of line L13, so $o_{s_1} \ge o_{s_2} \ge \cdots \ge o_{s_k}$. Two offsets can be equal only if one of the records has length 0; such a record occupies no byte, and the argument below holds for any order among equal offsets. Let $e'_0 = p$ and $e'_i = e'_{i-1} - \ell_{s_i}$, the value of $e'$ after the $i$-th pass of the loop.

First, $e'_i \ge o_{s_i}$ for each $i$. The records $s_1, \ldots, s_{i-1}$ have offsets above $o_{s_i}$, and by disjointness their intervals lie in $[o_{s_i} + \ell_{s_i}, p)$. So $\sum_{j < i} \ell_{s_j} \le p - o_{s_i} - \ell_{s_i}$, and $e'_i = p - \sum_{j \le i} \ell_{s_j} \ge o_{s_i}$.

Second, the move at line L17 of record $s_i$ writes $[e'_i, e'_{i-1})$. The records not moved yet, $s_{i+1}, \ldots, s_k$, lie below $o_{s_i} \le e'_i$, so the write does not touch them. The records moved before lie in $[e'_{i-1}, p)$, which is also not touched. The source $[o_{s_i}, o_{s_i} + \ell_{s_i})$ may overlap the target, but a memory move copies the bytes as they were before the move (the implementation copies the source slice first). So after the pass, slot $s_i$ points to its own bytes, and the other moved records keep theirs. This gives part 4 after the loop.

After the loop the live records are the intervals $[e'_i, e'_{i-1})$, which are disjoint and cover $[e'_k, p)$, and line L19 sets $e = e'_k$. This gives part 2 and, by Lemma 1, $G = F$. Since $F \ge 0$, we have $e \ge 4 + 4n$, which is part 1. The directory length $n$ and the set $S$ do not change, which gives part 3 and part 5. $\square$

**Lemma 3 (INSERT).** If the invariant holds before INSERT$(r)$ and $need \le F$, then INSERT returns a slot $s \notin S$, after it $M' = M \cup \{s \mapsto r\}$, and the invariant holds. If $need > F$, INSERT fails and changes nothing.

*Proof.* Line L1 picks $s$, the least free slot or $n$, so $s \notin S$. Line L2 sets $need = |r| + 4[s = n]$. If $need > F$, the test at line L4 fails before any write; note that $need > F \ge G$, so line L3 is true and line L4 is reached. Otherwise, after lines L3 to L5, $G \ge need$: either $G \ge need$ already, or COMPACT ran, which by Lemma 2 keeps the invariant and $M$ and makes $G = F \ge need$.

Line L6 writes $r$ at $[e - |r|, e)$ and lowers $e$ by $|r|$. Since $G \ge need \ge |r|$, the new interval lies above $4 + 4n$, so it overlaps no slot entry, and it lies below every live record, so it is disjoint from them. If $s = n$, line L7 grows the directory to $n + 1$ entries, whose end $4 + 4(n + 1)$ is at most the new $e$ because $G \ge |r| + 4$. Line L8 sets slot $s$. So part 1 holds, part 2 holds since the new interval is disjoint from the others, and part 3 holds since slot $n - 1$ is either the old last live slot or $s$ itself. Part 4 holds for $s$ by the write at line L6 and for the other slots because their bytes and entries did not change. $\square$

**Lemma 4 (DELETE).** If the invariant holds and $s \in S$, after DELETE$(s)$ the invariant holds and $M' = M$ without $s$.

*Proof.* Line L10 marks $s$ free, which removes it from $S$. Removing an interval keeps part 2 and part 4, and $e$ does not change. Lines L11 and L12 lower $n$ until slot $n - 1$ is live or $n = 0$, which gives part 3; only free entries are dropped, so $S$ loses nothing more, and a smaller $n$ keeps part 1. $\square$

**Lemma 5 (UPDATE).** If the invariant holds and $s \in S$, then UPDATE$(s, r)$ either sets $M(s) = r$ with the same slot $s$ and keeps the invariant, or fails without a change. It fails if and only if $|r| - \ell_s > F$.

*Proof.* If $|r| \le \ell_s$, the record is written over the start of its own interval, and the new interval $[o_s, o_s + |r|)$ is contained in the old one, so the invariant holds. Otherwise, the record grows by $d = |r| - \ell_s > 0$. If $d > F$, UPDATE fails before any write. If not, and $|r| \le G$, the record is written at the free end as in Lemma 3 (no new slot entry is needed, and the old interval simply becomes a hole). If $|r| > G$, slot $s$ is marked free for the moment, so the total free space becomes $F + \ell_s \ge |r|$, and COMPACT makes $G = F + \ell_s \ge |r|$ by Lemma 2, without touching $n$. The record is then written at the free end and slot $s$ points to it. In both cases only slot $s$ changes, and part 3 holds because $n$ did not change and $s$ is live again. $\square$

**Theorem.** Starting from the empty page, after any sequence of operations the invariant holds, `get` returns the abstract map $M$, a slot returned by INSERT names the same record until it is deleted (whatever compactions and updates of other slots happen in between), and INSERT fails if and only if $|r| + 4[\text{no slot is free}] > F$.

*Proof.* The empty page has $n = 0$ and $e = p$, so the invariant holds with $M = \emptyset$. Each operation keeps it and changes $M$ as its abstract specification says, by Lemmas 2 to 5. A slot $s$ leaves $S$ only at line L10, which runs only on DELETE$(s)$, and no lemma changes the record of a slot other than the one the operation names. The failure condition is Lemma 3, with $need$ written out. $\square$

**Running time.** Line L1 scans at most $n$ entries. COMPACT sorts at most $n$ live slots and moves at most $p - e' \le p$ bytes. Lines L11 and L12 remove each slot entry at most once after it was added, and each entry was added by one INSERT, so over a sequence of operations their total work is at most the number of inserts, which gives $O(1)$ amortized time per DELETE.
