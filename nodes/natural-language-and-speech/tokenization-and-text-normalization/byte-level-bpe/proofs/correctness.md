---
title: Byte-level BPE encodes every string without loss, and the recovery program keeps the most characters
proves: [correctness, termination]
status: full
---

Notation. A text $t$ is a string of Unicode scalar values, and $\mathrm{utf8}(t)$ is its UTF-8 byte string. A token is a nonempty byte string. A merge list is a sequence of pairs $(a, b)$ of tokens. Spans are fencepost spans: $x[i..j)$ holds the elements $i + 1$ to $j$.

**Lemma 1 (pre-tokens cover the text).** PRETOKENIZE($t$) returns strings $x_1, \ldots, x_q$ with $x_1 x_2 \cdots x_q = t$.

*Proof.* Each pass of the scanner starts at position $i$, appends $t[i..j)$ for some $j > i$, and sets $i \leftarrow j$. In the contraction branch $j = i + |c| > i$. In the letter, digit and symbol branches the run starts at $k \ge i$ and holds $t[k]$, so $j \ge k + 1 > i$. In the whitespace branch the run has length at least 1, and it is shortened by one only when its length is at least 2. So the appended pieces are consecutive, they do not overlap, and the scan ends at $i = |t|$. $\square$

**Lemma 2 (merges keep the bytes).** For any list of tokens $u$ and any pair $(a, b)$, the concatenation of MERGE($u$, $a$, $b$) equals the concatenation of $u$.

*Proof.* MERGE copies each token of $u$ in order, except that it writes two adjacent tokens $a$, $b$ as the one token $a b$, which is the same byte string. $\square$

**Theorem 1 (lossless, with no unknown token).** For every text $t$ and every merge list, every token of BBPE-ENCODE($t$) has an id, and DECODE(BBPE-ENCODE($t$)) $= t$.

*Proof.* Line E4 starts each pre-token as its single bytes, and each of the 256 byte values has an id. Line E7 creates only tokens $a b$ for pairs with a rank, which are merges and have ids. By Lemma 2 the tokens of one pre-token join to $\mathrm{utf8}(x)$, and UTF-8 maps a concatenation of strings to the concatenation of their byte strings, so by Lemma 1 all tokens join to $\mathrm{utf8}(x_1) \cdots \mathrm{utf8}(x_q) = \mathrm{utf8}(t)$. This is valid UTF-8, so decoding gives $t$ and no replacement character appears. The loop of lines E5 to E7 stops, because each pass replaces at least one pair and so shortens $u$. $\square$

**Theorem 2 (training).** BBPE-TRAIN stops after at most $K$ passes, and in each pass it merges a pair of largest count, counting non-overlapping occurrences from the left and weighting each pre-token by its count. Among pairs of equal count it takes the smallest by byte order.

*Proof.* Line L4 bounds the passes and line L6 can stop earlier. Line L5 counts the pairs of the current segmentation, and line L7 takes the largest count with ties to the smallest pair. Line L8 applies the merge to every pre-token, so the next count is taken on the segmentation that results. $\square$

Nothing here says that the merge list is the best of its length: choosing the most frequent pair is a heuristic. Nor does anything here prove that merging the pair of lowest rank first (line E6) gives the same tokens as replaying every merge in order. For the hand-made list $[(x, ab), (a, b)]$ and the text $xab$ the two differ: replay gives $x$, $ab$, and lowest rank first gives $xab$. On lists made by BBPE-TRAIN the tests found no difference.

**Theorem 3 (recovery).** For a byte string $d$ of length $n$, call a *partition* a split of $d$ into consecutive chunks of 1 to 4 bytes, and let $g(i, j) = 1$ if $d[i - 1..j)$ is the UTF-8 code of one character and 0 otherwise. Then RECOVER returns the largest number of chunks with $g = 1$ over all partitions of $d$, and a partition that reaches it.

*Proof.* Let $\mathrm{OPT}(k)$ be that largest number for the prefix $d[0..k)$, with $\mathrm{OPT}(0) = 0$. The last chunk of a partition of $d[0..k)$ is $d[k - t..k)$ for some $t \in \{1, 2, 3, 4\}$ with $t \le k$, and the rest is a partition of $d[0..k - t)$. So $\mathrm{OPT}(k) = \max_t \mathrm{OPT}(k - t) + g(k - t + 1, k)$. This is the recurrence of line R3, computed in the $(\max, +)$ semiring, and line R1 sets the base case. By induction on $k$, $f(k) = \mathrm{OPT}(k)$. Line R4 stores a $t$ that reaches the maximum, so the walk of line R5 follows a partition whose score is $f(n)$, and it keeps the chunks with $g = 1$. $\blacksquare$

Wang, Cho and Gu state that the design of UTF-8 makes the recovered characters unique. The tests check, by enumerating all partitions of short byte strings, that every best partition keeps the same characters.
