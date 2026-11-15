---
title: Blocked sort-based indexing builds the same index as a direct in-memory build
proves: [correctness]
status: full
---

Let the input be documents $(d_1, w_1), \ldots, (d_N, w_N)$ with $d_1 < d_2 < \cdots < d_N$, where $w_i$ is the token sequence of document $d_i$. Let $T = \sum_i |w_i|$. The reference index $R$ maps each term $t$ to the list of pairs $(d, \mathrm{tf}_{t,d})$ with $\mathrm{tf}_{t,d} \ge 1$, sorted by $d$, where $\mathrm{tf}_{t,d}$ is the number of times $t$ occurs in the tokens of $d$. We show that BSBI with any block size $M \ge 1$ returns $R$.

1. **The term ids are a bijection.** Line L3 gives a term the id $|termid|$ the first time the term is seen, and never changes it. So the ids are $0, 1, \ldots, V-1$ for the $V$ distinct terms, two different terms get different ids, and `term_of` inverts the map. From here on we identify a term with its id.

2. **The pair stream.** Lines L2 to L4 produce one pair $(t, d)$ for each token, in reading order. Call this stream $S$. For each $(t, d)$, the number of copies of $(t, d)$ in $S$ is $\mathrm{tf}_{t,d}$.

3. **The blocks cover the stream.** Line L5 cuts $S$ after every $M$ pairs, and line L6 flushes the last, shorter block if it is not empty. So the blocks $S_1, \ldots, S_k$ are consecutive pieces of $S$, their concatenation is $S$, and $k = \lceil T / M \rceil$. A block can end in the middle of a document, so one pair $(t, d)$ can have copies in two or more consecutive blocks.

4. **Each run is correct for its block.** Line L8 sorts block $S_r$ by $(t, d)$. In a sorted sequence, equal pairs are next to each other, so the loop of line L9 sees each distinct pair $(t, d)$ of $S_r$ as one maximal group of equal elements and outputs one triple $(t, d, f)$ with $f$ the size of the group. So run $R_r$ holds exactly one triple $(t, d, c_r(t, d))$ for each pair that occurs in $S_r$, where $c_r(t, d)$ is its number of copies in $S_r$, and the keys $(t, d)$ of $R_r$ are strictly increasing.

5. **The merge outputs the triples in key order.** The heap of lines L11 to L13 holds at most one triple of each run, the first triple of that run that is not yet output. This is the $k$-way merge of sorted sequences: the least key in the heap is the least key not yet output, because each run is sorted. So line L13 removes the triples of all runs in nondecreasing order of $(t, d)$, each one once.

6. **Lines L14 and L15 join equal keys.** Because the keys come out in nondecreasing order, all triples with one key $(t, d)$ come out one after the other. The first of them goes to the output by line L15, and each later one adds its count to that output triple by line L14. A triple with a new key starts a new output entry. So when the heap is empty, the output holds one triple $(t, d, \sum_r c_r(t, d))$ for each distinct pair of $S$, in strictly increasing key order. By steps 2 and 3, $\sum_r c_r(t, d)$ is the number of copies of $(t, d)$ in $S$, which is $\mathrm{tf}_{t,d}$.

7. **Line L16 forms the lists.** The output is sorted by $t$ and, for equal $t$, by $d$. Line L16 reads it in that order and appends $(d, f)$ to the list of term $t$. So the list of each term holds its documents in increasing order of $d$, with $f = \mathrm{tf}_{t,d}$, and a term has a list exactly when it occurs in some document. This is $R$. $\blacksquare$

The proof does not use the order of the document ids. With the ids in increasing order, as the input requires, one pair $(t, d)$ has copies in two runs only when a block boundary cuts document $d$, and only the last document of a run can be cut.
