---
tag: A636EJ
kind: theorem
slug: external-sorting-lower-bound
name: External sorting I/O lower bound
aliases:
- Aggarwal-Vitter sorting bound
- External sorting lower bound
- I/O sorting lower bound
area: foundations/lower-bounds
level: advanced
summary: In the external memory model with indivisible items, every comparison-based sort of N items needs Omega((N/B) log_{M/B}(N/B)) block reads in the worst case, and external merge sort meets this bound.
prereqs: [external-memory-model, comparison-sort-lower-bound, counting-argument, stirling-approximation]
see_also: [external-merge-sort, distribution-sort, permuting-lower-bound, external-permuting, funnelsort, red-blue-pebble-game, pebbling-lower-bound, external-sorting-io-lower-bound]
sources:
  - paper: doi:10.1145/48529.48535
    title: "Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9) (1988), 1116-1127"
    locator: Theorem 3.1 (sorting), Theorem 3.2 (permuting), Section 4 (the lower bound proofs, including the comparison argument for sorting and the constant 2 for merge sort)
  - paper: doi:10.1007/BF01185207
    title: "Jeffrey Scott Vitter and Elizabeth A. M. Shriver, Algorithms for parallel memory, I: Two-level memories, Algorithmica 12(2-3) (1994), 110-147"
    locator: the parallel disk model with D disks and the randomized distribution sort
  - paper: doi:10.1109/SFFCS.1999.814600
    title: "Matteo Frigo, Charles E. Leiserson, Harald Prokop and Sridhar Ramachandran, Cache-oblivious algorithms, 40th Annual Symposium on Foundations of Computer Science (1999), 285-297"
    locator: funnelsort and the tall-cache assumption
  - paper: doi:10.1145/780542.780589
    title: "Gerth Stølting Brodal and Rolf Fagerberg, On the limits of cache-obliviousness, Proceedings of the 35th Annual ACM Symposium on Theory of Computing (2003), 307-315"
    locator: the main theorems (a tall cache is necessary for optimal cache-oblivious comparison sorting)
  - paper: doi:10.1007/978-1-4684-2001-2_10
    title: "Robert W. Floyd, Permuting information in idealized two-level storage, in Complexity of Computer Computations (1972), 105-109"
    locator: the permuting bound for a special case of the parameters
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.4 (external sorting)
---

The external sorting lower bound says that in the [external memory model](/external-memory-model/), with indivisible items and comparisons as the only way to learn about keys, sorting $N$ items with an internal memory of $M$ items and blocks of $B$ items needs $\Omega\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$ block transfers. Aggarwal and Vitter proved it in 1988, with the matching upper bound. The proof is a [counting argument](/counting-argument/): one block read can tell the algorithm only a bounded amount about the order of the keys. [External merge sort](/external-merge-sort/) meets the bound, so this is the I/O cost of sorting.

## Statement

**Model.** The machine is the one of the [external memory model](/external-memory-model/) page, with one disk: an internal memory of $M$ cells, and a disk of blocks of $B$ cells. Block $i$ holds the cells $iB$ to $(i+1)B - 1$. A read copies one whole block into $B$ cells of the internal memory, and a write copies $B$ cells of the internal memory into one whole block. The parameters satisfy $1 \le B \le M/2$. The input is $N$ items with distinct keys in blocks $0$ to $N/B - 1$, where $B$ divides $N$. The output must be the same items in increasing order of key, in blocks $0$ to $N/B - 1$.

**The class of algorithms.** The algorithm is deterministic. Items are *indivisible*: the algorithm copies and moves whole items, and it learns about the keys only by comparing the keys of two items that are both in the internal memory. Computation in the internal memory is free. The cost is the number of reads and writes.

**Theorem (exact form).** Let $t$ be the largest number of reads that the algorithm makes on an input of $N$ items, over all $N!$ orders of the input. Then

$$t \cdot \lg\binom{M}{B} \;+\; \frac{N}{B}\,\lg(B!) \;\ge\; \lg(N!).$$

**Corollary (asymptotic form).** Under the same hypotheses,

$$t \;\ge\; \frac{N}{B}\cdot\frac{\ln\frac{N}{eB}}{\ln\frac{eM}{B}},$$

and if also $N \ge e^2 B$, then

$$t \;\ge\; \frac{1}{5}\cdot\frac{N}{B}\,\log_{M/B}\frac{N}{B}.$$

So the worst-case number of I/Os of a comparison-based external sort is $\Omega\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$. With the upper bound below, sorting costs $\Theta\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$ I/Os for $N > M \ge 3B$. Aggarwal and Vitter (Theorem 3.1) write the bound as $\Theta\big(\frac{N}{B}\frac{\log(1 + N/B)}{\log(1 + M/B)}\big)$, a form that stays positive for small $N/B$. They prove it for the average case as well as the worst case.

## In plain words

A sorting program on a disk can look at keys only when they are in its small fast memory. It brings in a block of items, compares them with the items already in memory, and writes blocks back. To finish, it must know the full order of all the items.

Count how much one block read can tell the program. The new items fall among the items already in memory in only so many ways. The first time an input block comes in, its items can also be in any order among themselves, but this happens once for each block. The program must tell apart every possible order of the input, and there are very many of them. So it needs many reads. The count gives a few passes over the data: a logarithm of the data size in blocks, to the base of the memory size in blocks.

## Proof

**Setup.** Take the keys $1, 2, \ldots, N$. An input is one of the $N!$ arrangements of these keys in the $N$ input cells. Fix a correct algorithm $\mathcal{A}$. Write $C = \binom{M}{B}$.

**Step 1: give the algorithm more information.** Let $\mathcal{A}'$ be $\mathcal{A}$ with one change: right after each read, $\mathcal{A}'$ is told the relative order of all the items that are then in the internal memory. We call this total order the *outcome* of the read. Between two reads no item enters the internal memory, because only a read brings items in. So every comparison that $\mathcal{A}$ makes between read $r$ and read $r + 1$ is between two items that were in memory right after read $r$, and its result follows from the outcome of read $r$ (or of an earlier read, if no read happened yet, and then there is nothing to compare). Hence the whole run of $\mathcal{A}$, that is, which blocks it reads and writes and how it moves items in memory, is a function of the sequence of outcomes. We bound the number of different sequences of outcomes.

**Step 2: what one read can reveal.** Look at one read, and fix all the earlier outcomes. Let $X$ be the set of items that are in memory just before the read and that the read does not overwrite. The read writes $B$ cells, so $|X| \le M - B$. Each item of $X$ was in memory right after the previous read, so the previous outcome gives the order of $X$. Let $Y$ be the items of the block that are not in $X$, so $|Y| \le B$. The new outcome is a total order of $X \cup Y$ that agrees with the known order of $X$.

- If the order of $Y$ is already known, the outcome is fixed by the positions of the items of $Y$ among those of $X$, so there are at most $\binom{|X| + |Y|}{|Y|}$ outcomes. Since $|X| + |Y| \le M$, $|Y| \le B$ and $B \le M/2$, this is at most $\binom{M}{|Y|} \le \binom{M}{B} = C$. The first inequality holds because $\binom{a}{b}$ grows with $a$, and the second because $\binom{M}{b}$ grows with $b$ for $b \le M/2$.
- In any case there are at most $|Y|!\,\binom{|X|+|Y|}{|Y|} \le B!\,C$ outcomes: choose the order of $Y$, then the positions among $X$.

**Step 3: the order of a block is known except at the first read of an input block.** Look at the block that the read copies.

- If the block was written earlier, take the last write to it. All its items were in memory at the time of that write, so they were all in memory right after the read before that write. The outcome of that read gives their order.
- If the block was never written and was read before, all its items were in memory together right after that earlier read, whose outcome gives their order.
- If the block was never written and is outside blocks $0$ to $N/B - 1$, it holds no item.

So the factor $B!$ of step 2 can appear only at the first read of one of the $N/B$ input blocks. On each run there are at most $N/B$ such *fresh* reads.

**Step 4: count the runs.** Draw the runs of $\mathcal{A}'$ on all inputs as a tree. Each node is a read, each edge is one possible outcome of it, and each leaf is a complete run. We show by induction from the leaves up that the number of leaves below a node $v$ is at most the largest value of $C^{r(P)} (B!)^{f(P)}$ over the paths $P$ from $v$ to a leaf, where $r(P)$ is the number of reads on $P$ and $f(P)$ the number of fresh reads on $P$. A leaf has one leaf below it, and the empty path gives $1$. If $v$ is a read with $d$ children, then $d \le C$, or $d \le B!\,C$ when $v$ is fresh, by steps 2 and 3. The number of leaves below $v$ is the sum over the children, so it is at most $d$ times the largest bound of a child, and this is the bound for the best path through $v$. On every path, $r(P) \le t$ by the definition of $t$, and $f(P) \le N/B$ by step 3. So the tree has at most $C^t (B!)^{N/B}$ leaves.

**Step 5: every input needs its own leaf.** Suppose that two different inputs reach the same leaf. Then $\mathcal{A}'$ performs the same reads, writes and moves on both. These moves send the item in input cell $i$ to the same output cell on both inputs, for each $i$. The two inputs place the keys differently, so the two outputs differ, and at most one of them is sorted. This contradicts the correctness of $\mathcal{A}$. So the tree has at least $N!$ leaves.

**Step 6: conclude.** Steps 4 and 5 give $C^t (B!)^{N/B} \ge N!$. Taking $\lg$ gives the exact form. $\square$

**Proof of the corollary.** Three standard estimates are used. First, $N! \ge (N/e)^N$, because $e^N = \sum_k N^k/k! \ge N^N/N!$. Second, $B! \le B^B$. Third, $\binom{M}{B} \le \frac{M^B}{B!} \le \left(\frac{eM}{B}\right)^B$, by the first estimate for $B$. Since $B < M$, $\binom{M}{B} \ge 2$, so $\ln\binom{M}{B} > 0$ and the exact form gives

$$t \ge \frac{\ln N! - \frac{N}{B}\ln B!}{\ln\binom{M}{B}} \ge \frac{N\ln\frac{N}{e} - N \ln B}{B \ln\frac{eM}{B}} = \frac{N}{B}\cdot\frac{\ln\frac{N}{eB}}{\ln\frac{eM}{B}}.$$

If the numerator is negative, the bound says nothing, and it is still true. Now let $N \ge e^2 B$, so $\ln\frac{N}{B} \ge 2$ and $\ln\frac{N}{eB} = \ln\frac{N}{B} - 1 \ge \frac12 \ln\frac{N}{B}$. Since $M/B \ge 2$, $1 \le \ln\frac{M}{B} / \ln 2$, so $\ln\frac{eM}{B} = 1 + \ln\frac{M}{B} \le \frac{1 + \ln 2}{\ln 2}\ln\frac{M}{B}$. Together,

$$t \ge \frac{\ln 2}{2(1 + \ln 2)}\cdot\frac{N}{B}\cdot\frac{\ln(N/B)}{\ln(M/B)} \ge \frac15 \cdot \frac{N}{B}\log_{M/B}\frac{N}{B},$$

because $\frac{\ln 2}{2(1+\ln 2)} \approx 0.2047$. $\square$

## Consequences

- **Sorting is a few passes, not $\lg N$ passes.** One pass over the data costs $2N/B$ I/Os. The bound says that sorting costs $\Theta(\log_{M/B}(N/B))$ passes. With $M/B$ in the thousands, this is a small number, often 1 to 3.
- **The case $B = 1$, $M = 2$.** Then the exact form reads $t \ge \lg(N!)$, and each read is one comparison of a new item with the one item kept. So the bound contains the [comparison sort lower bound](/comparison-sort-lower-bound/) of the [comparison model](/comparison-model/).
- **Permuting.** If the keys are known to form the permutation $1, \ldots, N$, the algorithm knows the target of each item in advance, and the bound changes. Aggarwal and Vitter (Theorem 3.2) prove that permuting takes $\Theta\big(\min\big\{N, \frac{N}{B}\log_{M/B}\frac{N}{B}\big\}\big)$ I/Os for indivisible items. The proof counts the permutations that $t$ I/Os can produce, and it has an extra factor of about $N/B + t$ for each I/O, for the choice of the block. The term $N$ is the naive method that moves one item per I/O. It wins only when $B\log(M/B) = o(\log(N/B))$, that is, for tiny blocks or a tiny memory. In that range sorting still costs the full sort bound, and the proof above, with comparisons, is what shows it. See [permuting lower bound](/permuting-lower-bound/) and [external permuting](/external-permuting/).
- **Many disks.** In the parallel disk model of Vitter and Shriver (1994), one I/O moves up to one block on each of $D$ disks. A parallel I/O can be replaced by $D$ single I/Os, so the bound divided by $D$ is a lower bound there. Vitter and Shriver gave a randomized distribution sort that meets $O\big(\frac{N}{DB}\log_{M/B}\frac{N}{B}\big)$.
- **Cache-oblivious sorting.** A [cache-oblivious](/cache-oblivious-model/) algorithm is an external memory algorithm that does not know $M$ and $B$, so the same lower bound holds for it. Frigo, Leiserson, Prokop and Ramachandran (1999) gave [funnelsort](/funnelsort/), which meets the bound when $M = \Omega(B^2)$ (the *tall-cache assumption*). Brodal and Fagerberg (2003) proved that some assumption of this kind is necessary: no cache-oblivious comparison sort meets the bound for all $M$ and $B$.

### Worked example

Take $N = 10^{10}$ records of 100 bytes (one terabyte), an internal memory of $M = 8 \cdot 10^7$ records (8 GB) and blocks of $B = 10^4$ records (1 MB). So $N/B = 10^6$ blocks and $M/B = 8000$.

| Quantity | Value |
|---|---|
| $\lg(N!)$ | about $3.1777 \times 10^{11}$ bits |
| $\frac{N}{B}\lg(B!)$, the order inside the input blocks | about $1.1846 \times 10^{11}$ bits |
| $\lg\binom{M}{B}$, the most that one later read can reveal | about $144\,076$ bits |
| exact bound on reads $t$ | about $1.383 \times 10^6$, that is 1.38 scans |
| $\frac{N}{B}\log_{M/B}\frac{N}{B}$ | about $1.537 \times 10^6$ |
| merge sort: runs of $M$ items | $125$ runs |
| merge sort: merge passes with $k = M/B - 1 = 7999$ | $1$ |
| merge sort: reads, and all I/Os | $2 \times 10^6$ reads, $4 \times 10^6$ I/Os |

Merge sort reads every block twice, and the bound says that every algorithm must make at least 1.38 million reads. The two differ by a factor of about 1.45. With a smaller memory, $M = 10^6$ records, $M/B = 100$ and $\log_{M/B}(N/B) = 3$. Then the exact bound is about $2.467 \times 10^6$ reads, and merge sort makes $10^4$ runs, which need 3 merge passes with $k = 99$ (since $99^2 = 9801 < 10^4$), for $4 \times 10^6$ reads and $8 \times 10^6$ I/Os.

### Pitfalls

- **The model of the bound.** The theorem is about indivisible items and comparisons. It says nothing about an algorithm that computes with the bits of the keys, such as a radix sort or a hash of the keys. For keys that are integers in a word, the proof does not apply. This page makes no claim about that case.
- **Sorting has no $\min$ with $N$.** The term $\min\{N, \cdot\}$ belongs to the permuting bound. For sorting with comparisons, the bound is the full $\Omega\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$ even when it is larger than $N$, for example $\Theta(N \log N/\log M)$ when $B = 1$.
- **The hypothesis $B \le M/2$.** Step 2 needs $\binom{M}{b} \le \binom{M}{B}$ for $b \le B$, which uses $B \le M/2$. The model page assumes it too.
- **Reads, not all I/Os.** The bound counts reads. The total number of I/Os is larger: merge sort makes as many writes as reads.
- **The base of the logarithm.** The bound has $\log_{M/B}$. Writing $\log_2$ or $\log_M$ gives a wrong count of passes.
- **Worst case and average case.** The proof above is for the worst case. Aggarwal and Vitter prove the same order for the average over all input orders, with a separate argument on the external path length of the tree.

## Tightness

**Upper bound.** [External merge sort](/external-merge-sort/) sorts with $O\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$ I/Os when $N > M$. It makes sorted runs of $M$ items and merges $M/B - 1$ runs at a time with a [k-way merge](/k-way-merge/). The page of the [external memory model](/external-memory-model/) proves the explicit bound $8\lceil N/B\rceil\log_{M/B}(N/B)$ for $M \ge 3B$. [Distribution sort](/distribution-sort/), which splits the items into buckets by sampled splitters, meets the same bound (Aggarwal and Vitter, Section 5). So the theorem is tight up to a constant factor for $N > M \ge 3B$.

**The constant.** The constant $1/5$ of the corollary comes from rough estimates. Aggarwal and Vitter (Section 4) show more: if $B = o(M)$ and $\log(M/B)$ divides $\log(N/B)$ or is $o(\log(N/B))$, the average number of I/Os for sorting is at least about $\frac{2N}{B}\cdot\frac{\log(N/B)}{\log(M/B)}$, and merge sort meets this. The factor 2 is one read and one write of each block in each pass.

**When the bound is trivial.** If $N \le M$, one read and one write of each block sort the items, so the cost is $\Theta(N/B)$. The exact form is consistent with this, because an algorithm with $N/B$ reads exists.

## History

Floyd (1972) studied permuting in a two-level storage and proved the first bounds, for special values of the parameters. Hong and Kung (1981) introduced the [red-blue pebble game](/red-blue-pebble-game/), which models a memory hierarchy with $B = 1$ for a fixed computation graph. Aggarwal and Vitter (1988) defined the model with general $M$ and $B$, and proved tight bounds for sorting, permuting, the FFT, permutation networks and matrix transposition. Their sorting lower bound uses the permuting argument in the main range and the comparison argument of this page when $B\log(M/B) = o(\log(N/B))$. The argument of this page uses the comparison count for every range. Vitter and Shriver (1994) moved the bounds to the model with $D$ independent disks. Frigo, Leiserson, Prokop and Ramachandran (1999) gave optimal cache-oblivious sorting under the tall-cache assumption, and Brodal and Fagerberg (2003) showed that such an assumption is necessary.

## References
