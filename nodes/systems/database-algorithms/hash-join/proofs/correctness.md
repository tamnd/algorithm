---
title: Hash join returns the join as a multiset with M + N reads
proves: [correctness, termination, io.worst]
status: full
---

We use the line numbers of the pseudocode. We treat each stored tuple as a distinct occurrence. The join $R \bowtie S$ on $r.a = s.b$ is the multiset with one copy of $r \cdot s$ for each pair of occurrences $(r, s)$ with $r.a = s.b$. Let $h$ be the hash function of the table and $K$ its number of buckets.

**Swapping the roles.** If line L1 swaps $R$ and $S$, the algorithm builds on $S$ and probes with $R$, and it appends $r \cdot s$ in the order of the original relations. The set of matching pairs does not depend on which side is built, so it is enough to prove the claim for a build on $R$.

**Lemma 1 (build).** After line L4, for each value $v$, the tuples $r$ in bucket $h(v) \bmod K$ with $r.a = v$ are exactly the occurrences of $R$ with $r.a = v$, each once.

*Proof.* Line L4 reads each page of $R$ once and inserts each occurrence $r$ once, into bucket $h(r.a) \bmod K$. The table appends to a chain and never replaces an entry. So every occurrence with $r.a = v$ is in bucket $h(v) \bmod K$, once. Every tuple of that bucket that passes the test $r.a = v$ is an occurrence with key $v$. $\square$

**Theorem 1 (correctness).** If line L2 does not fail, HASH-JOIN returns a list whose multiset of elements is $R \bowtie S$.

*Proof.* Lines L6 and L8 meet each occurrence $s$ of $S$ exactly once, because the pages partition $S$. For this $s$, line L8 looks in bucket $h(s.b) \bmod K$ and appends $r \cdot s$ for each tuple $r$ of the bucket with $r.a = s.b$. By Lemma 1 with $v = s.b$, these are exactly the occurrences of $R$ that match $s$, each once. Nothing else is appended. So the number of copies of each tuple $t$ in $out$ is the number of matching pairs $(r, s)$ with $r \cdot s = t$. All loops are finite, so the algorithm stops. $\blacksquare$

**Theorem 2 (I/O count).** If line L2 does not fail, the algorithm does exactly $M + N$ page reads and no page writes other than the output.

*Proof.* Line L4 reads each of the $M$ pages of the build input once and line L7 reads each of the $N$ pages of the probe input once. By the test of line L2, the table takes at most $B - 2$ pages, so together with one input page and one output page it fits in the $B$ buffer pages, and no page of the table is written out. $\blacksquare$

**Expected work.** Let $n_R = p_R M$ and choose $K \ge n_R$ and $h$ from a universal family, so that two different keys share a bucket with probability at most $1/K$. For a tuple $s$, the expected number of tuples of $R$ in its bucket with a key other than $s.b$ is at most $n_R / K \le 1$. The tuples with key $s.b$ are output. Summing over the tuples of $S$, the expected work of line L8 is $O(p_S N + T)$, and line L4 does $O(n_R)$ work, so the expected total is $O(p_R M + p_S N + T)$. $\blacksquare$
