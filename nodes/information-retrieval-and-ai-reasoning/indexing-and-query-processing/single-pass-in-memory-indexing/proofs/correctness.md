---
title: Single-pass in-memory indexing builds the same index as a direct in-memory build
proves: [correctness]
status: full
---

Let the input be documents $(d_1, w_1), \ldots, (d_N, w_N)$ with $d_1 < d_2 < \cdots < d_N$, where $w_i$ is the token sequence of $d_i$, and let $T = \sum_i |w_i|$. The reference index $R$ maps each term $t$ that occurs in the collection to the list of pairs $(d, \mathrm{tf}_{t,d})$ with $\mathrm{tf}_{t,d} \ge 1$, in increasing order of $d$. We show that SPIMI with any block size $M \ge 1$ returns $R$.

1. **The blocks cut the token stream into pieces.** Let $S$ be the sequence of (term, document) pairs of the tokens in reading order. Lines L7 and L8 count the tokens of the current block and write the block after every $M$ tokens; line L9 writes the last block if it is not empty. So the blocks correspond to consecutive pieces $S_1, \ldots, S_k$ of $S$ with $S = S_1 S_2 \cdots S_k$.

2. **Invariant of one block.** While a block is open, the dictionary holds, for each term $t$ that occurs in the part of the current piece read so far, a list of pairs $(d, c)$ in strictly increasing order of $d$, where $c \ge 1$ is the number of tokens of $t$ in document $d$ inside this piece so far. The invariant holds for the empty dictionary. Take one more token $w$ of document $d$. If $w$ is new, line L3 adds an empty list. Because documents are read in increasing order and the tokens of one document are consecutive, every pair already in the list of $w$ has an id at most $d$, and only the last one can equal $d$. If it does, line L5 adds 1 to its count. Else line L6 appends $(d, 1)$, which keeps the ids strictly increasing. Lists of other terms do not change. So the invariant holds after the token.

3. **Each written block is sorted and correct for its piece.** Line L11 lists the terms of the dictionary in sorted order with their lists. By step 2, block $i$ holds, for each term $t$ of piece $S_i$, the list of $(d, c_i(t, d))$ with $c_i(t, d)$ the number of tokens of $t$ in $d$ inside $S_i$, in increasing order of $d$.

4. **Document ranges of the blocks.** Every document id of block $i$ is at most every document id of block $i + 1$, because the pieces follow the reading order. Equality holds only for the one document that the boundary between $S_i$ and $S_{i+1}$ cuts, and that id is the last id of block $i$ and the first id of block $i + 1$.

5. **The merge order.** The heap of lines L12 to L14 holds at most one entry of each block, keyed by (term, block number). Each block is sorted by term, so this is a $k$-way merge, and line L14 takes the entries of all blocks in increasing order of term, and for one term in increasing order of block number.

6. **Lines L15 and L16 build the list of each term.** For a fixed term $t$, let $i_1 < i_2 < \cdots < i_r$ be the blocks that contain $t$. The first entry starts the output list of $t$ at line L16. Each later entry of block $i_j$ is joined to the output list at line L15. By step 4, the ids of the list from block $i_j$ are at least the last id already in the output list. Only the first of them can be equal to it, and only when the blocks between share one document that block boundaries cut. In that case the first pair has the same id as the last output pair and line L15 adds the counts. Else all ids are larger and the list is appended. So after the last block, the output list of $t$ is strictly increasing in $d$, and the count for $d$ is $\sum_i c_i(t, d)$, the number of tokens of $t$ in $d$ over all pieces, which is $\mathrm{tf}_{t,d}$.

7. **Conclusion.** Every term of the collection occurs in some block and so gets an output list, and no other term does. With step 6, line L17 returns $R$. $\blacksquare$

A document with more than $M$ tokens can span more than two blocks. The argument covers this case: each join adds the count of one more block to the same last pair, and a block in the middle that does not contain $t$ changes nothing.
