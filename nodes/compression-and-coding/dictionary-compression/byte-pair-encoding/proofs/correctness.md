---
title: Byte-pair encoding stops and its output expands back to the input
proves: [correctness]
status: full
---

We prove three facts about BPE-COMPRESS-BLOCK on a block $B_0$ of bytes with threshold $t \ge 2$: the loop stops, each code it takes does not occur in $B_0$, and expanding the output gives $B_0$ again. Then we show the same for the container that holds several blocks, and one fact about the tokenizer.

Write $V_0$ for the set of byte values that occur in $B_0$, $B$ for the current block, and $T$ for the current table. For a table $T$, the *expansion* $E_T$ of a byte $x$ is $x$ itself if $x$ is not a code of $T$, and $E_T(a)\,E_T(b)$ if $(x, a, b) \in T$. The expansion of a sequence is the concatenation of the expansions of its bytes.

**Invariant.** Each time line L3 tests $U$:

1. $U$, the codes in $T$ and $V_0$ are pairwise disjoint, and together they are all 256 byte values.
2. Each byte of $B$ is in $V_0$ or is a code of $T$.
3. For each entry $(c, a, b)$ of $T$, the bytes $a$ and $b$ are in $V_0$ or are codes of entries that come before $(c, a, b)$ in $T$.
4. $E_T(B) = B_0$.

Part 3 makes $E_T$ well defined: following an entry only goes to earlier entries, so the expansion of a code ends after at most $|T|$ steps, and no code is used in its own expansion.

*Initialization.* Line L1 sets $U$ to the values not in $V_0$, and line L2 makes $T$ empty, so part 1 holds. $B = B_0$, so parts 2 and 4 hold, and part 3 holds because $T$ is empty.

*Maintenance.* Suppose the loop body runs to line L9 with the pair $ab$, of count at least $t$, and the code $c$ from line L7.

- Part 1: $c$ moves from $U$ to the codes of $T$, so the three sets stay disjoint and cover all values.
- Part 2: line L8 writes only $c$, which is now a code of $T$.
- Part 3: $a$ and $b$ are bytes of $B$, so by part 2 they are in $V_0$ or are codes of the old $T$, which come before the new entry.
- Part 4: $c$ was in $U$, so by parts 1 and 2 it did not occur in $B$ and was not a code before. Line L9 adds $(c, a, b)$, which does not change $E_T$ of any old byte, and $E_T(c) = E_T(a)\,E_T(b)$. Line L8 replaces each chosen occurrence $ab$ by $c$, and this keeps the expansion of $B$. So $E_T(B) = B_0$ still holds.

If the body stops at line L6, or the counts are empty, nothing changes.

**Termination.** Each pass of the loop that does not stop takes one value from $U$. $U$ has $256 - |V_0| \le 255$ values when $B_0$ is not empty. So the loop runs at most $256 - |V_0|$ times. Each pass replaces at least $t \ge 2$ occurrences, so it also shortens $B$ by at least 2.

**The codes do not occur in the input.** By part 1, each code of $T$ was in $U$ at the start, so it is not in $V_0$. This is what lets the decoder tell a code from a literal byte: a byte of the output is a code exactly when it has an entry in $T$.

**Round trip of one block.** EXPAND-BLOCK reads $B$ and replaces each byte that has an entry in $T$ by its pair, with an explicit stack, until only bytes without an entry are left. By parts 1 and 3 this computes $E_T(B)$, and by part 4 this is $B_0$.

**Round trip of the container.** COMPRESS splits the data into blocks of the chosen size and, for each block, writes one byte $k = |T|$, then $3k$ bytes for the entries, then the length of the packed block in 4 bytes, then the packed block. Since $k \le 255$, it fits in one byte, and since the block size is less than $2^{32}$, so does the length. DECOMPRESS reads the same fields in the same order, so each field it reads is the one written. It expands each block as above and joins the results in order, which gives the data. The data is empty exactly when there are no blocks, and then both sides give the empty string.

**The tokenizer.** LEARN-MERGES starts each training word as its characters followed by the end symbol, and applies merge $i$ to all words before it counts pairs for merge $i + 1$. SEGMENT starts each word in the same way and applies the merges in the same order, with the same left to right replacement. So by induction on $i$, after merge $i$ the symbols of a training word are the same in both procedures, and SEGMENT returns the segmentation that the training produced. Each merge joins two adjacent strings into their concatenation, so for any word, the units that SEGMENT returns, joined together, are the word followed by the end symbol. $\blacksquare$
