---
title: Cyclon keeps valid caches, reverses the link with its partner, removes the oldest entry, and joins without changing other out-degrees
proves: [correctness]
status: full
---

**Setting.** Every node runs CYCLON-SHUFFLE (lines L1 to L9) once per cycle, and the partner $Q$ merges with lines L7 to L9 with the roles exchanged. Each shuffle is atomic. A crashed node takes no steps and does not answer. Joins run as described on the page.

**Claim.**

1. *Valid caches.* At all times, the cache of every node $P$ holds at most $c$ entries, with distinct addresses, none equal to $P$.
2. *The partner keeps its size.* In a shuffle in which $Q$ answers, the cache of $Q$ has at least as many entries after the shuffle as before.
3. *Link reversal.* In a shuffle in which $Q$ answers and the cache of $Q$ did not hold $P$, after the shuffle the cache of $P$ does not hold $Q$ and the cache of $Q$ holds $(P, 0)$.
4. *The oldest entry goes.* After a shuffle of $P$, the cache of $P$ does not hold the entry that had the highest age after line L1. In particular, if that entry points to a crashed node, it is removed.
5. *No fresh entry of a crashed node.* An entry $(d, 0)$ is created only by $d$ itself, in line L4. So after $d$ crashes, no new entry about $d$ is created, and every entry about $d$ is a moved or copied old entry.
6. *Join.* A join leaves the cache size of every old node unchanged, and gives the new node $P$ an in-degree equal to the size of its cache.

**Proof of 1.** By induction over shuffles and joins. Initially the property holds. In a shuffle, $P$ only removes entries (L3) or adds entries of $R$ that pass line L7, so no entry for $P$ and no duplicate address enters. An entry is added only into an empty slot (L8), so the size stays at most $c$, or in place of an entry of $S$ (L9), which keeps the size. Two entries of $R$ have distinct addresses, because $R$ is a subset of the valid cache of $Q$, so adding several of them creates no duplicate. The same holds for $Q$, whose received set $S \cup \{(P, 0)\}$ has distinct addresses: $S$ is a subset of the cache of $P$, which does not hold $P$. In a join, the node $A$ at the end of a walk replaces one entry by $(P, 0)$ only if it does not hold $P$, and $P$ adds the replaced entry only if it is not $P$ and not held yet. $\square$

**Proof of 2.** $Q$ removes nothing except in line L9, and there it adds one entry for each entry of $R$ that it removes. Line L8 only adds. So the size of the cache of $Q$ never falls. $\square$

**Proof of 3.** Line L3 removes $Q$ from the cache of $P$. Afterwards, $P$ only adds entries of $R$, and $R$ does not contain $Q$, because the cache of $Q$ does not hold $Q$ (claim 1). So $P$ does not hold $Q$ after the shuffle. $Q$ receives $(P, 0)$. It does not discard it in line L7, because $(P, 0)$ does not point to $Q$ and $Q$ did not hold $P$. It puts it into an empty slot, or in place of an entry of $R$. There are enough entries of $R$ for all entries that pass line L7 if the cache of $Q$ is full: $|R| = \min(l, |\mathrm{cache}(Q)|)$ and the received set has at most $l$ entries, so if $|R| = l$ every received entry finds a place, and if $|R| < l$ the cache of $Q$ had fewer than $l \le c$ entries and has empty slots for the rest. So $Q$ holds $(P, 0)$ after the shuffle. $\square$

**Proof of 4.** Line L2 chooses as $Q$ the entry with the highest age, and line L3 removes it. Afterwards $P$ only adds entries of $R$, which never contains $Q$ (claim 1 for the cache of $Q$), or nothing at all if $Q$ does not answer (line L5). $\square$

**Proof of 5.** The only line that creates an entry with age 0 is L4, and it creates $(P, 0)$ for the node $P$ that runs the shuffle. A join creates $(P, 0)$ for the joining node $P$. Every other step moves or copies existing entries with their ages, or increases ages. A crashed node runs no shuffle and no join. $\square$

**Proof of 6.** At the end of each walk, $A$ replaces one entry by one entry, so its size does not change, or it does nothing. No other old node changes its cache. Each entry $(P, 0)$ that is placed at some $A$ is matched by exactly one entry that $P$ adds to its cache, and the steps that skip one of the two skip both. So the number of caches that hold $P$ equals the size of the cache of $P$. $\square$

**What is not proved.** The claims do not bound the in-degree variance, the clustering coefficient, or the time to remove all dead entries. Copies of an entry can appear, because $P$ keeps the entries of $S$ that it did not replace in line L9, so the number of entries that point to a crashed node can grow for a while before it falls. These quantities are measured on the page.
