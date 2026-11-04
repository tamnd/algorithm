---
title: The leveled LSM tree returns the newest entry of each key
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, with $C_0 \ge 1$ and $T \ge 2$. Number the updates $1, 2, \ldots$ in order. Every entry in the memtable or in a run is a copy of some update of its key, an entry *of age* $t$ if it comes from update $t$. Let $\sigma(k)$ be the state of $k$ in the abstract dictionary: absent if $k$ was never updated or its last update is a delete, and present with value $v$ if its last update is `put(k, v)`.

Define the *sequence* of components as the memtable, then level 1, level 2, and so on. The *found entry* of a key $k$ is its first entry in this sequence, if any. We prove that between operations:

- (M1) every run is sorted with distinct keys and has at most $C_0 T^i$ entries at level $i$, and the memtable has fewer than $C_0$ entries;
- (M2) for every key $k$, if $k$ has entries in two components, the one earlier in the sequence is younger;
- (N) for every key $k$, if $k$ has a found entry, it is the last update of $k$, or $k$ has no found entry and $\sigma(k)$ is absent; and if the found entry is a tombstone, $\sigma(k)$ is absent;
- (M3) the deepest nonempty level has no tombstones.

We prove (N) in the form: for every key $k$ that was ever updated, either its found entry is of the age of its last update, or $k$ has no entry and its last update is a delete.

**Base.** All components are empty and no key was updated.

**GET.** Lines L8 to L11 look at the memtable and then at the levels in order and return the first entry of $k$, which is the found entry. The search inside one run is a binary search inside the block chosen by the fence keys: the block whose first key is the largest fence at most $k$ holds $k$ if any block does, because the run is sorted by (M1). If the found entry is a put of $v$, it is the last update of $k$ by (N), so $\sigma(k)$ is present with value $v$. If it is a tombstone, the last update was a delete, and $\sigma(k)$ is absent. If there is no entry, $\sigma(k)$ is absent by (N). GET ends after at most one step per level.

**UPDATE, line L1.** The new entry of $k$ is the youngest of all entries, and it replaces the older entry of $k$ in the memtable, if any. So $k$ has its found entry in the memtable, of the age of its last update, and (N) holds for $k$. Other keys are not changed. (M2) holds because the memtable is first in the sequence and its entry of $k$ is the youngest. If the memtable now has $C_0$ entries, line L2 calls FLUSH.

**FLUSH.** We prove a loop invariant for lines L4 to L7. At the start of each pass with index $i$:

- (F1) $R$ is a sorted run with distinct keys, and the memtable and the levels $1, \ldots, i - 1$ are empty;
- (F2) for each key, its entry in $R$ is younger than its entries in levels $i, i+1, \ldots$;
- (F3) for each key, if we take the sequence $R$, level $i$, level $i+1$, and so on, the first entry of each key is the found entry it had before FLUSH, or there is no entry and the found entry before was a tombstone that was dropped.

At the first pass, $i = 1$ and $R$ is the memtable in key order, so (F1) to (F3) hold by (M2) and the definition.

*Line L5.* MERGE takes the union of the entries of $R$ and of level $i$; on a key in both, it keeps the one of $R$, which is younger by (F2), and drops the older one, which was not the first entry of the key in the sequence. So the first entry of each key in the sequence (new $R$, level $i + 1$, ...) is the same as in (old $R$, level $i$, level $i + 1$, ...). The result is sorted with distinct keys, as a merge of two sorted runs with equal keys combined. If all levels below $i$ are empty, a tombstone in the result is the only entry of its key in the whole tree, so dropping it changes the first entry of that key from a tombstone to none, which (F3) allows. So (F1) to (F3) hold for the new $R$, with level $i$ now merged into it.

*Line L6.* If $R$ fits, it becomes level $i$. Then the sequence is: empty memtable, empty levels $1..i-1$, level $i = R$, levels $i+1, \ldots$ unchanged. By (F3), the found entry of each key is its old found entry, or none for a dropped tombstone. So (N) holds: an old found entry is of the age of the last update, and a dropped tombstone means the last update was a delete. (M2) holds by (F2) and by (M2) for the deeper levels, which were not touched. (M1) holds: $R$ has at most $C_0 T^i$ entries, and the memtable is empty. For (M3): if all levels below $i$ are empty, $R$ is the deepest nonempty level and has no tombstones, since they were dropped; otherwise the deepest nonempty level is unchanged.

*Line L7.* If $R$ is too big, level $i$ becomes empty, and the loop goes on with $i + 1$. (F1) holds, since level $i$ is now empty and its entries are in $R$. (F2) holds for level $i + 1$ and deeper by (F2) and (M2) before. (F3) holds by the argument of line L5.

**Termination of FLUSH.** Each pass either returns or increases $i$. When the pass at level $i$ starts, $R$ holds at most the entries of the memtable and of the levels $1, \ldots, i-1$, so at most $C_0(1 + T + \cdots + T^{i-1}) = C_0\frac{T^i - 1}{T - 1} < C_0 T^i$ entries, since $T \ge 2$. Once $i$ is past the last nonempty level, level $i$ is empty, the merge adds nothing, and line L6 returns. So the pass at the first empty level returns at the latest, and FLUSH ends after at most one pass per level plus one.

**Range queries.** RANGE reads, in each run, the entries with keys in the range, from the oldest level to the newest and then the memtable, letting newer entries overwrite older ones. So it keeps for each key the found entry, and it returns the keys whose found entry is a put, which by (N) are exactly the present keys in the range.

So every GET and RANGE returns the state of the abstract dictionary, every operation ends, and the invariants hold between operations. $\blacksquare$
