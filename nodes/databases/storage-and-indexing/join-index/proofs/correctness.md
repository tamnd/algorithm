---
title: The join index stays equal to the set of matching rid pairs, and its join returns R join S with the stated page count
proves: [correctness, io.worst]
status: full
---

We use the line numbers of the pseudocode. Write $R$ and $S$ for the current relations, as maps from live rids to tuples, and
$$J^\ast = \{\, (i, j) \mid i \in \mathrm{dom}(R),\ j \in \mathrm{dom}(S),\ R[i].a = S[j].b \,\}$$
for the set of matching rid pairs. The representation is correct when the following holds.

**Invariant.** (I1) For every value $v$, $V_R[v] = \{ i \in \mathrm{dom}(R) \mid R[i].a = v \}$ and $V_S[v] = \{ j \in \mathrm{dom}(S) \mid S[j].b = v \}$. (I2) $J_R = J_S = J^\ast$ as sets of pairs. (I3) A rid returned by line L1 is not in use and has never been used.

*Initialization.* With $R$ and $S$ empty, all value indexes and both copies are empty, and $J^\ast$ is empty.

**Lemma 1 (insert).** If the invariant holds before INSERT-R$(r)$, it holds after it. The same holds for INSERT-S by symmetry.

*Proof.* Let $i$ be the new rid and $v = r.a$. By (I3), $i$ is not in $\mathrm{dom}(R)$, and no pair in $J_R$ or $J_S$ has first rid $i$, because by (I2) such a pair would be in $J^\ast$ and so $i$ would be live. Line L1 adds $i$ to $V_R[v]$ only, so (I1) holds for $R$, and $V_S$ does not change. The new set $J^\ast$ is the old one plus the pairs $(i, j)$ with $S[j].b = v$, because no other tuple changed. By (I1) for $S$, these $j$ are exactly the elements of $V_S[v]$, and line L2 adds exactly these pairs to both copies. So (I2) holds. The rid counter moves past $i$, so (I3) holds. $\square$

**Lemma 2 (delete).** If the invariant holds before DELETE-R$(i)$ for a live rid $i$, it holds after it. The same holds for DELETE-S by symmetry.

*Proof.* Let $r = R[i]$. Line L3 removes $i$ from $\mathrm{dom}(R)$ and from $V_R[r.a]$, which is the only set of $V_R$ that holds it by (I1). So (I1) holds. The new set $J^\ast$ is the old one without the pairs whose first rid is $i$. Line L4 visits exactly the pairs of $J_R$ with first rid $i$ and removes each from both copies. Since $J_R = J_S$ before, the same pairs leave both, and (I2) holds. Rids are not reused, so (I3) holds. $\square$

**Theorem 1 (correctness).** After any sequence of operations, JOIN returns a list whose multiset of elements is $R \bowtie S$.

*Proof.* By Lemma 1 and Lemma 2 and induction on the number of operations, the invariant holds before JOIN. So line L5 lists each pair of $J^\ast$ exactly once. Line L6 puts one entry $(j, R[i])$ into $L$ for each pair, line L7 only reorders $L$, and line L8 appends $R[i] \cdot S[j]$ once for each entry. So the output has one copy of $R[i] \cdot S[j]$ for each pair of $J^\ast$, which is one copy for each pair of tuples with $R[i].a = S[j].b$. That is $R \bowtie S$ as a multiset, with each stored tuple counted as a distinct occurrence. $\blacksquare$

**Theorem 2 (page count of JOIN).** Let $P = |J^\ast|$, let $q$ pairs fit on a page, and let $L$ fit in memory. Then JOIN reads exactly $\lceil P/q \rceil + |\pi_R| + |\pi_S|$ pages, where $\pi_R$ is the set of pages of $R$ that hold a tuple with at least one partner and $\pi_S$ the same for $S$. This is at most $\lceil P/q \rceil + M + N$.

*Proof.* Line L5 reads the pairs, stored $q$ to a page in order of $i$: $\lceil P/q \rceil$ reads. In line L6 the rids $i$ come in increasing order, and the page of a rid, $\lfloor i/t \rfloor$, is a nondecreasing function of it. So the pages of $R$ come in nondecreasing order, the test "differs from the last one" succeeds exactly once for each distinct page, and line L6 reads each page of $\pi_R$ once. After line L7, the rids $j$ of $L$ are in nondecreasing order, so by the same argument line L8 reads each page of $\pi_S$ once. A page holds a tuple with a partner exactly when some pair names one of its tuples. The bound follows from $|\pi_R| \le M$ and $|\pi_S| \le N$. $\blacksquare$

**Maintenance cost.** By the proofs of Lemma 1 and Lemma 2, an insertion or deletion of a tuple with $d$ partners changes exactly $d$ pairs in each of the two copies, plus one entry of a value index. $\blacksquare$
