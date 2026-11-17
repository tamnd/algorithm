---
title: Bloom join returns the join as a multiset and reads M + 2N pages
proves: [correctness, io.worst]
status: full
---

We use the line numbers of the pseudocode. We treat each stored tuple as a distinct occurrence. For multisets $X \subseteq R$ and $Y \subseteq S$, write $X \bowtie Y$ for the multiset with one copy of $r \cdot s$ for each pair $(r, s) \in X \times Y$ with $r.a = s.b$, and write $R \ltimes S$ for the occurrences of $R$ that have at least one partner in $S$. We assume that the hash join of line L8 is correct, which is proved on the page [hash join](/hash-join/).

**Lemma 1 (no false negatives).** After line L2, for every key $x$ that occurs as $s.b$ for some tuple $s$ of $S$, the bits $F[g_1(x)], \dots, F[g_k(x)]$ are all 1.

*Proof.* Line L1 sets every bit to 0, and no line sets a bit back to 0. When line L2 handles a tuple $s$ with $s.b = x$, it sets the $k$ bits of $x$ to 1, and they stay 1. $\square$

**Lemma 2 (the reduced relation).** After line L6, $R \ltimes S \subseteq R' \subseteq R$ as multisets of occurrences.

*Proof.* Line L6 appends only tuples of $R$, each at most once, because line L5 visits each occurrence of $R$ once. So $R' \subseteq R$. Let $r$ be an occurrence of $R \ltimes S$. It has a partner $s$ with $s.b = r.a$, so the key $x = r.a$ occurs in $S$, and by Lemma 1 all its $k$ bits are 1. So the test of line L6 succeeds for $r$, and $r \in R'$. $\square$

**Lemma 3 (sandwich).** If $R \ltimes S \subseteq X \subseteq R$, then $X \bowtie S = R \bowtie S$.

*Proof.* Every pair counted in $X \bowtie S$ is a matching pair of $R \times S$, because $X \subseteq R$. Conversely, let $(r, s)$ be a matching pair of $R \times S$. Then $r$ has a partner, so $r \in R \ltimes S \subseteq X$, and the pair is counted in $X \bowtie S$. Each matching pair is counted once on each side, because $X$ holds each occurrence of $R$ at most once. $\square$

**Theorem 1 (correctness).** BLOOM-JOIN returns a list whose multiset of elements is $R \bowtie S$, for every $m \ge 1$ and $k \ge 1$ and every choice of the hash functions, provided lines L2 and L6 use the same functions.

*Proof.* Line L7 sends $R'$ unchanged. By the correctness of the hash join, line L8 returns $R' \bowtie S$. By Lemma 2 and Lemma 3 with $X = R'$, this is $R \bowtie S$. $\blacksquare$

**Theorem 2 (page I/O).** The algorithm reads exactly $M + 2N$ pages and writes none, without the writes of the output, when the table on $R'$ of line L8 is kept in memory.

*Proof.* Line L2 reads each of the $N$ pages of $S$ once. Lines L5 and L6 read each of the $M$ pages of $R$ once. Line L8 builds its table from $R'$, which is in memory after line L7, and reads each page of $S$ once more: $N$ reads. No line writes a page. The total is $M + 2N$ for every input. $\blacksquare$

**The size of $R'$.** Let $n$ be the number of distinct keys of $S$, and suppose the positions $g_i(x)$ of all keys are independent and uniform on $\{0, \dots, m - 1\}$. For a key $x$ not in $S$, a fixed bit is still 0 after line L2 with probability $(1 - 1/m)^{k n}$, and the test of line L6 succeeds for $x$ with probability about $(1 - (1 - 1/m)^{k n})^k \approx (1 - e^{-k n/m})^k$. This is the usual estimate of the false positive rate, and it is an approximation, because the $k$ events for the positions of $x$ are not exactly independent. By Lemma 2, $|R'| = |R \ltimes S| + (\text{the number of false positive occurrences})$, and so the expected value of $|R'|$ is about $|R \ltimes S| + \varepsilon \cdot |R \setminus (R \ltimes S)|$ under this assumption. $\blacksquare$
