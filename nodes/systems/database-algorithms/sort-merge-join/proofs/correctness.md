---
title: Sort-merge join returns the join as a multiset, and its cost is 3(M + N) when the runs fit
proves: [correctness, termination, io.best]
status: full
---

We use the line numbers of the pseudocode. We treat each stored tuple as a distinct occurrence. The join $R \bowtie S$ on $r.a = s.b$ is the multiset with one copy of $r \cdot s$ for each pair of occurrences with $r.a = s.b$, a *matching pair*. The keys come from a total order.

**Lemma 1 (sorted streams).** Lines L1 to L3 stop, and line L4 gives two streams: $\rho = (\rho_1, \ldots, \rho_m)$, the occurrences of $R$ in non-decreasing order of $a$, and $\sigma = (\sigma_1, \ldots, \sigma_n)$, the occurrences of $S$ in non-decreasing order of $b$.

*Proof.* Line L1 writes each occurrence into exactly one run and sorts each run. A merge pass replaces groups of runs by their merge, which is a sorted run of the same occurrences, as on the page [external merge sort](/external-merge-sort/). Line L3 works on the input with more runs, and by the test of line L2 that input has two or more runs. With fan-in $B - 1 \ge 2$, the pass lowers its number of runs by at least one, so the loop of line L2 stops. The merge of line L4 of all remaining runs of $R$ is a sorted stream of all occurrences of $R$, and the same holds for $S$. $\square$

Let $i$ and $j$ be the positions of the cursors, so $r = \rho_i$ and $s = \sigma_j$. Let $P = \{\rho_1, \ldots, \rho_{i-1}\}$ and $Q = \{\sigma_1, \ldots, \sigma_{j-1}\}$ be the occurrences that the cursors have passed. For a key $v$, let $\rho(v)$ and $\sigma(v)$ be the occurrences with key $v$. Because the streams are sorted, each of them is a contiguous block of its stream.

**Invariant.** At each test of line L5:

- (I1) $out$ holds exactly one copy of $r' \cdot s'$ for each matching pair $(r', s')$ with $r' \in P$ and $s' \in Q$, and nothing else;
- (I2) for each matching pair $(r', s')$, $r' \in P$ if and only if $s' \in Q$.

*Initialization.* At the start $P$ and $Q$ are empty and $out$ is empty, so both parts hold.

*Maintenance, line L6.* Here $\rho_i.a < \sigma_j.b$. Suppose $\rho_i$ had a match $s'$. If $s' \in Q$, then by (I2) $\rho_i \in P$, which is false. If $s' \notin Q$, then $s'$ is at position $j$ or later, so its key is at least $\sigma_j.b > \rho_i.a$, which is not a match. So $\rho_i$ has no match. Line L6 adds $\rho_i$ to $P$ and changes nothing else. No matching pair contains $\rho_i$, so (I1) and (I2) still hold.

*Maintenance, line L7.* The same argument with the roles of $R$ and $S$ swapped.

*Maintenance, lines L8 to L10.* Here $\rho_i.a = \sigma_j.b = v$. No occurrence of $\rho(v)$ is in $P$: if $r' \in P$ had key $v$, then $(r', \sigma_j)$ would be a matching pair with $r' \in P$ and $\sigma_j \notin Q$, against (I2). In the same way, no occurrence of $\sigma(v)$ is in $Q$. Because the blocks are contiguous, $\rho(v)$ starts at position $i$ and $\sigma(v)$ starts at position $j$, and line L9 sets $G_R = \rho(v)$ and $G_S = \sigma(v)$. The cursors move past both blocks, so $P$ becomes $P \cup \rho(v)$ and $Q$ becomes $Q \cup \sigma(v)$. The matching pairs that are new in $P \times Q$ are exactly those with a member in $\rho(v)$ or in $\sigma(v)$, and these are exactly the pairs of $\rho(v) \times \sigma(v)$, because a match of a tuple with key $v$ has key $v$. Line L10 appends each of them once, so (I1) holds. For (I2), the pairs with key $v$ now have both members inside, and the other pairs did not change.

**Termination.** Each iteration of the loop of line L5 moves $i$ or $j$ forward by at least one, so the loop runs at most $m + n$ times.

**Theorem 1 (correctness).** SORT-MERGE-JOIN returns a list whose multiset of elements is $R \bowtie S$.

*Proof.* When the loop stops, one stream is used up. Say it is $\rho$, so $P$ is all of $R$. For each matching pair $(r', s')$, $r' \in P$, so $s' \in Q$ by (I2). By (I1), $out$ holds each matching pair exactly once and nothing else. If $\sigma$ is used up, the argument is the same with $Q$. $\blacksquare$

**Theorem 2 (cost with combined passes).** Assume that every page is full, that $\lceil M/B \rceil + \lceil N/B \rceil \le B - 2$, and that every block $\sigma(v)$ that meets a block $\rho(v)$ of two or more pages fits in the free frames. Then the algorithm does exactly $3(M + N)$ page I/Os, without the writes of the output. The second assumption holds when $B(B - 4) \ge M + N$.

*Proof.* Line L1 reads each page once and writes each page once, which is $2M + 2N$ I/Os, and makes $\lceil M/B \rceil + \lceil N/B \rceil$ runs. By assumption these fit in $B - 2$ frames, so line L2 does no pass. Line L4 reads each page of each run once while the merge phase consumes it, and by the third assumption no block is read twice, which is $M + N$ reads. The total is $3(M + N)$. For the last claim, $\lceil x \rceil < x + 1$, so $\lceil M/B \rceil + \lceil N/B \rceil < (M + N)/B + 2 \le (B - 4) + 2 = B - 2$ when $B(B - 4) \ge M + N$. $\blacksquare$
