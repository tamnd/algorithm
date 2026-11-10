---
title: The Munro-Paterson algorithm returns the k-th smallest item, and p passes need O(n^(1/p) (log n)^(2 - 2/p)) storage
proves: [correctness]
status: full
---

We prove that MP-SELECT (lines L1 to L14) returns the $k$-th smallest item, that the population shrinks as stated, and the storage bound for $p$ passes. All keys are distinct (ties are broken by position), and imaginary items $+\infty$ are larger than all real items and distinct from each other. For a sample $Q$ with population $P$ and an item $y \in Q$, write $b(y)$ for the number of items of $P$ strictly below $y$.

**Lemma 1 (the samples are well spread).** Let $Q$ be a sample at level $i$ with $s$ items, and let $y$ be its $j$-th smallest item, $1 \le j \le s$. Then
$$L_{ij} := j2^i - 1 \;\le\; b(y) \;\le\; (i + j - 1)2^i =: M_{ij}.$$

*Proof.* By induction on $i$. At level 0, $Q$ is its whole population, sorted, so $b(y) = j - 1 = L_{0j} = M_{0j}$.

Let $i \ge 1$, and let $Q$ be the merge of $\mathrm{thin}(A)$ and $\mathrm{thin}(C)$, where $A$ and $C$ are samples at level $i - 1$ of the two halves $P_A$ and $P_C$ of $P$. Say $y$ comes from $A$, and among the $j$ smallest items of $Q$, $p \ge 1$ come from $\mathrm{thin}(A)$ and $q = j - p \ge 0$ from $\mathrm{thin}(C)$. The $p$-th item of $\mathrm{thin}(A)$ is the $2p$-th item of $A$, so $y$ is the $2p$-th item of $A$, and the number of items of $P_A$ below $y$ is between $L_{i-1,2p}$ and $M_{i-1,2p}$ by induction. The items of $\mathrm{thin}(C)$ below $y$ are its first $q$ items, which are the items $2, 4, \ldots, 2q$ of $C$. So the $2q$-th item of $C$ is below $y$ (if $q \ge 1$) and the $(2q + 2)$-th item of $C$ is above $y$ (if it exists).

*Lower bound.* All items of $P_C$ up to and including the $2q$-th item of $C$ are below $y$. By induction that is at least $L_{i-1,2q} + 1 = 2q 2^{i-1} = q2^i$ items; for $q = 0$ the count $0 = q2^i$ holds trivially. So $b(y) \ge (2p 2^{i-1} - 1) + q 2^i = (p + q)2^i - 1 = j2^i - 1$.

*Upper bound.* Every item of $P_C$ below $y$ is below the $(2q + 2)$-th item of $C$. By induction there are at most $M_{i-1,2q+2} = (i - 1 + 2q + 1)2^{i-1} = (i + 2q)2^{i-1}$ of them. If $C$ has fewer than $2q + 2$ items, then $2q + 2 > s$, and the bound still holds since all of $P_C$ has $2^{i-1}s < (i + 2q)2^{i-1}$ items. So $b(y) \le (i + 2p - 2)2^{i-1} + (i + 2q)2^{i-1} = (2i + 2j - 2)2^{i-1} = (i + j - 1)2^i$.

The case where $y$ comes from $C$ is the same with the roles of $A$ and $C$ exchanged. $\square$

The construction of lines L11 to L14 builds exactly such a sample: CARRY works like a binary counter, so the waiting sample at level $i$ was made from the $2^i$ blocks just before the blocks of the new level $i$ sample, and the two populations are the two halves of the population of the merged sample. With $2^r$ blocks in all, the last CARRY returns a sample at level $r$ whose population is the whole padded population of $2^r s$ items.

**Lemma 2 (the invariant).** At the start of each pass, the answer $x^*$ (the $k$-th smallest item of $\sigma$) satisfies $lo \le x^* \le hi$. In that pass, line L5 gives $k' = k - |\{x : x < lo\}|$, which is the rank of $x^*$ in the population $P = \{x : lo \le x \le hi\}$.

*Proof.* At the first pass $lo = -\infty$ and $hi = +\infty$. The second claim follows from the first: the items below $x^*$ are those below $lo$ and those of $P$ below $x^*$. Assume the claim for one pass that is not final, and let $Q$ be its sample at level $r$, built over $P$ padded to $2^r s$ items with $+\infty$. The padding is above $x^*$, so $x^*$ still has exactly $k' - 1$ items of the padded population below it, and $1 \le k' \le |P| \le 2^r s$.

Let $u = \lfloor (k' - 1)/2^r \rfloor - r + 1$, the largest integer with $M_{ru} = (r + u - 1)2^r \le k' - 1$. If $u \ge 1$, Lemma 1 says that $Q[u]$ has at most $k' - 1$ items below it, so $Q[u] \le x^*$. Also $Q[u]$ is real: an imaginary item has all $|P| \ge k'$ real items below it. So the new $lo$ is at most $x^*$, and if $u < 1$, $lo$ does not change.

Let $v = \lceil k'/2^r \rceil$, the smallest integer with $L_{rv} = v2^r - 1 \ge k' - 1$. Then $1 \le v \le s$ since $k' \le 2^r s$. By Lemma 1, $Q[v]$ has at least $k' - 1$ items below it, so $Q[v] \ge x^*$. If $Q[v]$ is imaginary, $hi$ stays, and $x^* \le hi$ still holds. So the new filters keep $x^*$ between them. If they are equal, they are $x^*$, which line L9 returns. $\square$

**Lemma 3 (the population shrinks).** After a pass at level $r$ that is not final, the next population has at most $\min\{(2r - 1)2^r + 2, |P|\}$ items, which is the value $B$ of line L10.

*Proof.* The new filters are items of $P$ or old filters, so the new population is a subset of $P$. For integer $k' \ge 1$, $\lceil k'/2^r \rceil = \lfloor (k'-1)/2^r \rfloor + 1$, so $v - u = r$. If both filters were set from $Q$, the items of the padded population strictly between $Q[u]$ and $Q[v]$ number at most $b(Q[v]) - b(Q[u]) - 1 \le M_{rv} - L_{ru} - 1 = (r + v - 1)2^r - u2^r = (2r - 1)2^r$. With the two filters themselves this is at most $(2r - 1)2^r + 2$. If $u < 1$, the lower filter is the old one and every population item below $Q[v]$ counts, at most $M_{rv} \le (r - 1 + r + u)2^r \le (2r - 1)2^r$ since $u \le 0$; with $Q[v]$ this is at most $(2r - 1)2^r + 1$. If $Q[v]$ is imaginary, no imaginary item lies below it, and the real items between the filters are counted in the same way, so the same bound holds. $\square$

**Theorem 1 (correctness).** If MP-SELECT returns, it returns $x^*$.

*Proof.* By Lemma 2 the answer is in the population of every pass, with rank $k'$. A return at line L9 returns $lo = hi = x^*$. A final pass stores the population, which has at most $B \le M$ items by Lemma 3, and returns its $k'$-th smallest item, which is $x^*$. $\square$

**Theorem 2 (storage and passes).** A sampling pass holds at most $rs/2 + s + 2$ items. With storage $S = \Theta(n^{1/p}(\log n)^{2 - 2/p})$ and a suitable $s$, MP-SELECT ends within $p$ passes for all large $n$.

*Proof.* During a pass the algorithm holds the two filters, the current block of at most $s$ items, and for each level $i < r$ at most one thinned sample of $s/2$ items. During a CARRY, the sample being merged up replaces the block (which has just been emptied) and the waiting halves it consumes. So it holds at most $rs/2 + s + 2$ items.

Let the population of a pass have $n'$ items. Then $2^{r-1}s < n'$ when $r \ge 1$, so $2^r < 2n'/s$, and by Lemma 3 the next population has at most $(2r - 1)2^r + 2 < 2(2r - 1)n'/s + 2 \le 4rn'/s$ items for $n' \ge s$. Take $s$ the even number nearest to $S/\log_2 n$, so $r \le \log_2 n$ and the storage $rs/2 + s + 2 \le S$ for large $n$. Then the population after $t$ passes is at most $n(4(\log_2 n)^2/S)^t$. The last pass can store the population if $n(4(\log_2 n)^2/S)^{p-1} \le S$, that is $S^p \ge n(4(\log_2 n)^2)^{p-1}$, which holds for $S = 4n^{1/p}(\log_2 n)^{2(p-1)/p}$, and $2(p - 1)/p = 2 - 2/p$. This $S$ is $\Omega((\log n)^2)$ for fixed $p$ and large $n$, so $s > 4r$ and every pass makes progress. $\square$

**Lower bound (a sketch of Theorem 4 of the paper, not used above).** Munro and Paterson show $\Omega(n^{1/p})$ storage for $p$ passes. Their Lemma 3 gives an adversary that, against any algorithm with $S$ locations, orders the input so that after one pass a set $X$ of at least $\lfloor n/(2S - 1) \rfloor$ items has no item in storage and no known order among its items, and the median of the input is the median of $X$. Each time the algorithm discards an item, the adversary makes the next input item take the same place in the order relative to the stored items, so the discarded items of one location are never compared. Repeating this for each pass divides the problem size by $O(S)$ per pass, so $p$ passes need $S^p = \Omega(n)$. $\blacksquare$
