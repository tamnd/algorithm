---
title: Adaptive merging answers every range query exactly and moves each entry at most once
proves: [correctness]
status: full
---

We use the notation of the page and the code. The column has $N$ entries $(k, r)$, where $k$ is the key and $r$ the row id, so the entries are distinct even if keys are equal. A query $[lo, hi)$ asks for all entries with $lo \le k < hi$, in key order. The state after the first query is a list of runs $R_1, \dots, R_m$, the final partition $F$, and the covered set $C$, a union of disjoint half-open key ranges.

**Invariant.** After each query:

- (P) Every entry of the column is in exactly one of $F, R_1, \dots, R_m$.
- (S) $F$ and every $R_i$ are sorted by $(k, r)$.
- (C) An entry is in $F$ if and only if its key is in $C$.

**Lemma 1 (run generation, L1 to L3).** After the runs are made, (P), (S) and (C) hold with $F$ and $C$ empty.

*Proof.* The chunks of the column at the offsets $0, s, 2s, \dots$ are disjoint and cover the column, and each is sorted at L3. $\square$

**Lemma 2 (gaps, L4).** `gaps(lo, hi)` returns disjoint ranges whose union is $[lo, hi) \setminus C$.

*Proof.* The covered ranges are sorted and disjoint. The loop keeps a point $a$ such that every point of $[lo, a)$ is either covered or in a gap already returned, and no point in a returned gap is covered. A covered range $[c, d)$ that starts after $a$ gives the gap $[a, c)$, and then $a$ moves to $d$. A range that ends at or before $a$ is skipped. The loop stops when the next range starts at or after $hi$, and the last gap is $[a, hi)$ if $a < hi$. $\square$

**Lemma 3 (extraction, L5 to L7).** For a gap $[a, b)$ and a sorted run $R$, `bisect_left(R, (a,))` and `bisect_left(R, (b,))` give the indices $i \le j$ such that $R[i..j-1]$ is exactly the set of entries of $R$ with a key in $[a, b)$.

*Proof.* The tuple $(a,)$ is smaller than every $(a, r)$ and larger than every $(k, r)$ with $k < a$. So $i$ is the first index with a key $\ge a$, and likewise $j$ is the first index with a key $\ge b$. As $R$ is sorted, the keys in $[a, b)$ are exactly at $i, \dots, j - 1$. Removing a contiguous slice keeps $R$ sorted. $\square$

**Lemma 4 (merge and insert, L8 and L9).** After L9 for a gap $[a, b)$, the invariant holds with $C$ replaced by $C \cup [a, b)$.

*Proof.* By (C) and since $[a, b)$ is disjoint from $C$ (Lemma 2), no entry with a key in $[a, b)$ is in $F$; by (P) all of them are in the runs, and by Lemma 3 the pieces hold exactly these entries, each once. The merge of sorted pieces is sorted. Every key in $F$ is in $C$, so it is either $< a$ or $\ge b$. So $p$, the first index of $F$ with a key $\ge a$, has all keys $< a$ before it and all keys $\ge b$ from it on, and putting the merged list at $p$ keeps $F$ sorted, which is (S). The entries move from the runs to $F$ and no entry is copied, which is (P). Now $F$ holds exactly the entries with a key in $C \cup [a, b)$, which is (C). $\square$

**Theorem 1 (exact answers).** `range_query(lo, hi)` returns exactly the entries with $lo \le k < hi$, in order, and keeps the invariant.

*Proof.* By Lemmas 2 and 4, applied to each gap in turn, after the loop $F$ holds exactly the entries with a key in $C \cup [lo, hi)$, and L10 records this union as the new $C$. Removing empty runs changes nothing. As $[lo, hi) \subseteq C$, all entries with a key in $[lo, hi)$ are in $F$, which is sorted, so the slice between the first key $\ge lo$ and the first key $\ge hi$ at L11 is the answer, in order. $\square$

**Theorem 2 (each entry moves once).** Over any sequence of queries, each entry is sorted once at run generation and moved from a run to $F$ at most once. So the total number of moved entries is at most $N$, and a query whose range is already in $C$ moves nothing and makes no search in the runs.

*Proof.* Entries only leave runs (L7) and only enter $F$ (L9), and no step moves an entry out of $F$. A covered range has no gaps (Lemma 2), so the loop of L4 does not run. $\square$

**Cost of one query.** With $g$ gaps and $m \le \lceil N / s \rceil$ runs, the query makes $2 g m$ binary searches, each $O(\log s)$, merges the $t$ new entries in $O(t \log m)$ with a heap, and answers in $O(\log N + |answer|)$ from $F$. Putting the block into a Python list costs $O(|F|)$ for the shift; in a B-tree, as in the paper, it costs $O(t + \log N)$ per gap.

The tests check the answers of random queries with many equal keys against a full scan, run the invariant check after each query, check that the moved count equals $|F|$ and is at most $N$, check that a query over the whole key domain empties the runs, and check `gaps` against a brute force over small integer domains.
