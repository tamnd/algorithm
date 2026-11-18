---
title: Sort-based aggregation outputs each group once, in key order, with its correct aggregates
proves: [correctness]
status: full
---

We assume that MERGE is associative and commutative, and that $\text{state}(X \uplus Y) = \text{MERGE}(\text{state}(X), \text{state}(Y))$ for non-empty multisets $X$ and $Y$, where $\text{state}(\{\!\{v\}\!\}) = \text{INIT}(v)$. A record is a pair (key, state). For a multiset $S$ of records and a key $k$, write $S_k$ for the records of $S$ with key $k$, and $\sigma(S_k)$ for the MERGE of their states, in any order. By the assumptions, $\sigma(S_k)$ does not depend on the order, and $\sigma((S \uplus T)_k) = \text{MERGE}(\sigma(S_k), \sigma(T_k))$ when both parts are non-empty. Let $R$ also denote the multiset of level-0 records, one per input row, with key the values of $G$ and state INIT of the aggregated values. The target answer for key $k$ is $\text{FINAL}(\sigma(R_k))$.

**Lemma (COMBINE).** Let $X$ be a sequence of records sorted on the key. Lines L14 to L18 output one record $(k, \sigma(X_k))$ for each key $k$ of $X$, in the order of the keys, and nothing else.

*Proof.* Since $X$ is sorted, the records of each key $k$ form one block of consecutive positions. Invariant of line L14: if some records were read, $c$ exists, its key is the key $k$ of the last record read, and its state is $\sigma$ of the records of $k$ read so far; each key read before $k$ was output once with $\sigma$ of its whole block; no other record was output. At the first record, line L17 sets $c$ to it, which keeps the invariant. At a next record $(k', s)$: if $k' = k$, line L16 sets the state of $c$ to MERGE of the old state and $s$, which is $\sigma$ of the records of $k$ read so far. If $k' \ne k$, then the block of $k$ has ended, since blocks are consecutive, so the state of $c$ is $\sigma(X_k)$; line L17 outputs $c$ and starts $c = (k', s)$. At the end, the block of the last key has ended, and line L18 outputs it. Keys are output in the order of their blocks, which is the key order. $\square$

**Lemma (pass 0).** After the loop of line L2, the runs are sorted on the key, and for each key $k$, the multiset $U$ of records in all runs satisfies $\sigma(U_k) = \sigma(R_k)$ whenever $R_k$ is not empty, and $U_k$ is empty when $R_k$ is empty.

*Proof.* The groups of $B$ pages partition $R$. Line L3 sorts the records of one group $Y$. Without early aggregation, line L6 writes them as they are, so the run is $Y$ in sorted order. With early aggregation, line L5 replaces them by COMBINE of the sorted sequence, which is sorted by the COMBINE lemma, and holds $(k, \sigma(Y_k))$ for each key of $Y$. In both cases the run $Z$ satisfies $\sigma(Z_k) = \sigma(Y_k)$ for each key of $Y$ and has no other keys. Summing over the groups with the property of $\sigma$ on disjoint unions gives the claim. $\square$

**Lemma (merge pass).** If the claim of the pass 0 lemma holds before the body of line L7, it holds after line L12.

*Proof.* The groups of $B - 1$ runs partition the runs. The merge of line L10 of a group $W$ of sorted runs is a sequence sorted on the key that holds exactly the records of the runs of $W$. Line L11 writes it as it is, or writes COMBINE of it, which by the COMBINE lemma is sorted and has $\sigma$ equal for each key. So the new run $Z$ satisfies $\sigma(Z_k) = \sigma(W_k)$ for each key, and the union over the groups keeps $\sigma(U_k) = \sigma(R_k)$. Freeing the runs of the group removes only records that are now in $Z$. $\square$

**Theorem.** SORT-AGGREGATE stops, and outputs each key $k$ of $R$ exactly once, in key order, with $\text{FINAL}(\sigma(R_k))$, and no other row. At all times it keeps at most $B$ pages in memory.

*Proof.* If $N \le B$, the loop of line L2 has one group, which is all of $R$, and line L4 returns FINAL of COMBINE of $R$ sorted, which is the claim by the COMBINE lemma.

Otherwise, let $r$ be the number of runs. Pass 0 makes $\lceil N/B \rceil \ge 2$ runs. A pass of line L7 runs only if $r > B - 1 \ge 2$, and makes $\lceil r/(B-1) \rceil$ runs. Since $B - 1 \ge 2$ and $r \ge 3$, $\lceil r/(B-1) \rceil \le \lceil r/2 \rceil < r$, so $r$ decreases at each pass and the loop ends with $1 \le r \le B - 1$. By the pass 0 lemma and the merge pass lemma, at that time the runs are sorted, and $\sigma(U_k) = \sigma(R_k)$ for each key of $R$, with no other keys. Line L13 merges all runs into one sorted sequence of $U$, and COMBINE outputs $(k, \sigma(U_k)) = (k, \sigma(R_k))$ once per key in key order. FINAL then gives the answer of each group.

Memory: line L3 holds the $B$ pages of one group. A merge holds one page of each of at most $B - 1$ runs, plus one output page for line L11, and COMBINE holds one extra record. So the memory never holds more than $B$ pages. $\square$

**Cost.** Without early aggregation, every run of every pass holds the records of the pages it came from, so each pass reads $N$ pages, pass 0 and each pass of line L7 write $N$ pages, and line L13 writes nothing. With $P$ passes in total, the cost is $(P - 1) \cdot 2N + N = 2NP - N$. With early aggregation, the runs are formed from the same groups of pages and runs, and each run has at most as many records as the run that the plain sort makes from the same input, so the cost is never larger. A run has at most one record per key, so at most $\lceil d/p \rceil$ pages.
