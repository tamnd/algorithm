---
title: The chained hash table keeps its invariant and implements a dictionary
proves: [correctness]
status: full
---

We write $b_m(k) = h(k) \bmod m$ for the bucket of key $k$ in a table of $m$ buckets, and $D(T)$ for the set of pairs that the lists of $T$ hold. The invariant is the one of the page:

- **(H1)** each pair $(k, v)$ of $D(T)$ is in the list $B[b_m(k)]$;
- **(H2)** no key occurs in two pairs of $D(T)$;
- **(H3)** $n$ is the total length of the lists;
- **(H4)** $n \le m$.

**Theorem.** Start from an empty table with $m \ge 1$ buckets, and apply any sequence of HASH-INSERT, HASH-SEARCH and HASH-DELETE. Then after each operation (H1) to (H4) hold, and $D(T)$ is the map that the same sequence gives on an abstract dictionary. Each search returns the value of its key in that map, or NIL.

*Proof.* The empty table has no pair and $n = 0 \le m$, so (H1) to (H4) hold, and $D(T)$ is the empty map. We show that each operation keeps the invariant and changes $D(T)$ as the dictionary operation does. Fix an operation on key $k$, and let $i = b_m(k)$ be the index that line L1, L7 or L11 computes.

**Step 1 (the scan is complete).** Assume (H1). If some pair of $D(T)$ has key $k$, then by (H1) this pair is in $B[i]$. So a scan of $B[i]$ alone finds each pair with key $k$, and if the scan finds none, then $k$ is not a key of $D(T)$.

**Step 2 (search).** Lines L8 and L9 scan $B[i]$ and return the value of the first pair with key $k$. By Step 1 and (H2), this is the only pair with key $k$ in the table, so the value is $D(T)(k)$. If there is no such pair in $B[i]$, then by Step 1 $k$ is not a key, and line L10 returns NIL. Search changes no field, so the invariant holds after it.

**Step 3 (insert of a present key).** If the scan of lines L2 and L3 finds a pair $(k, v')$, line L3 replaces $v'$ by $v$ and returns. No pair moves, no key changes, and $n$ and $m$ do not change, so (H1) to (H4) hold. By (H2), this was the only pair with key $k$, so $D(T)$ is now the old map with $k$ mapped to $v$, as the dictionary asks.

**Step 4 (insert of a new key).** If the scan finds no pair with key $k$, then by Step 1 $k$ is not a key. Line L4 appends $(k, v)$ to $B[i] = B[b_m(k)]$, which keeps (H1). Since $k$ was not a key, (H2) holds. Line L5 adds 1 to $n$ and the lists grow by one pair, so (H3) holds. Before the operation $n \le m$, so now $n \le m + 1$. If $n \le m$, line L6 does nothing and (H4) holds. Else $n = m + 1$, and line L6 calls RESIZE$(T, 2m)$. By Step 6 below, RESIZE keeps (H1) to (H3) for the new size and does not change $D(T)$, and after it $n = m + 1 \le 2m$ since $m \ge 1$. So (H4) holds. The map is now the old map plus $(k, v)$.

**Step 5 (delete).** Lines L12 and L13 scan $B[i]$. If they find a pair with key $k$, they remove it and subtract 1 from $n$. By Step 1 and (H2), this was the only pair with key $k$, so $D(T)$ is now the old map without $k$. The other pairs do not move, so (H1) and (H2) hold, (H3) holds because both sides drop by 1, and (H4) holds because $n$ decreased and $m$ did not change. If they find no pair, $k$ is not a key, nothing changes, and the map is the old map without $k$, as the dictionary asks.

**Step 6 (resize).** Assume (H2) and (H3) for the old table, and let $m' \ge 1$. Line L14 makes $m'$ empty lists. The loop of lines L15 and L16 visits each pair of each old list exactly once and appends it to $B'[b_{m'}(k)]$. So after the loop, the new lists hold exactly the pairs of $D(T)$, each one once, and each pair $(k, v)$ is in $B'[b_{m'}(k)]$. Line L17 makes $B'$ and $m'$ the fields of $T$. Hence (H1) holds for the new size, $D(T)$ is the same set of pairs, so (H2) holds, and the total length of the lists is the old total, which is $n$, so (H3) holds.

By induction on the number of operations, using Steps 2 to 5, the invariant holds after each operation and $D(T)$ follows the abstract dictionary. $\blacksquare$
