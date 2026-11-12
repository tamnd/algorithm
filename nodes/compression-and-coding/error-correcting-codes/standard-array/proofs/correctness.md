---
title: The standard array partitions the space into cosets with least weight leaders, and its decoder returns a nearest codeword
proves: [correctness]
status: full
---

Let $C$ be an $[n, k]$ linear code over $\mathrm{GF}(q)$ with codewords $c_0 = 0, c_1, \ldots, c_{M-1}$, $M = q^k$. Vectors are rows, $\mathrm{wt}$ is the Hamming weight and $d(x, y) = \mathrm{wt}(x - y)$. Line L2 visits the words of $\mathrm{GF}(q)^n$ in a fixed total order $\prec$ in which a lighter word always comes before a heavier word.

**Lemma 1 (cosets).** For $a, b \in \mathrm{GF}(q)^n$, the cosets $a + C$ and $b + C$ are equal if $b - a \in C$ and disjoint otherwise. Each coset has exactly $q^k$ words, and there are $q^{n-k}$ cosets.

*Proof.* If $x \in (a + C) \cap (b + C)$, then $x = a + c = b + c'$ for codewords $c, c'$, so $b - a = c - c' \in C$. If $b - a = c'' \in C$, then $b + c = a + (c'' + c)$ for each $c \in C$, and $c'' + c$ runs over all of $C$ as $c$ does, so $b + C = a + C$. The map $c \mapsto a + c$ is one to one, so $|a + C| = |C| = q^k$. The cosets partition $\mathrm{GF}(q)^n$, because $a \in a + C$, so there are $q^n / q^k = q^{n-k}$ of them. $\square$

**Lemma 2 (BUILD).** When BUILD-STANDARD-ARRAY returns, its rows are $q^{n-k}$ distinct cosets of $C$, row $i$ is $(\ell_i + c_0, \ldots, \ell_i + c_{M-1})$, every word of $\mathrm{GF}(q)^n$ is in exactly one row, and for every row $i$ the leader $\ell_i$ is the first word of its coset in the order $\prec$. In particular $\mathrm{wt}(\ell_i) = \min \{\, \mathrm{wt}(x) : x \in \ell_i + C \,\}$.

*Proof.* We prove this invariant for the loop of line L2:

> **(B)** The rows built so far are distinct cosets, the set of used words is their union, and each row's leader is the first word of its coset in $\prec$. Every word that L2 has already visited is used.

Before the loop, the only row is row 0, which is $C = 0 + C$, line L1. Its leader is $0$, the only word of weight 0, so it is the first word of $C$. No word has been visited. So (B) holds.

Consider the visit of a word $v$. If $v$ is used, nothing changes, and $v$ is used, so (B) holds. If $v$ is not used, lines L4 to L6 add the row of $v + C$ and mark its words. This coset is not among the earlier rows: if it were, $v$ would be in that row and so used. By Lemma 1 it is disjoint from them, so the rows stay distinct cosets and the used set stays their union. Each word $x \prec v$ was visited before $v$ and so is used, so it lies in an earlier row, which is a coset different from $v + C$. Hence no word of $v + C$ comes before $v$, and $v$ is the first word of its coset. Now $v$ is used. So (B) holds after the visit.

Line L7 returns when there are $q^{n-k}$ rows. By (B) these are distinct cosets, so by Lemma 1 they are all the cosets, and their union is all of $\mathrm{GF}(q)^n$. If L7 never fires, the loop visits all words, and by (B) all words are used, so the rows cover the space and are again all $q^{n-k}$ cosets; the test of L7 then fires at the last new row. Either way every word is in exactly one row. Finally, since a lighter word comes earlier in $\prec$, the first word of a coset has the least weight in it. $\square$

**Theorem (DECODE).** For each $r \in \mathrm{GF}(q)^n$, DECODE$(r)$ returns a codeword $c_j$ with $d(r, c_j) = \min_{c \in C} d(r, c)$.

*Proof.* By Lemma 2, $r$ is in exactly one row $i$, at exactly one column $j$, since the entries $\ell_i + c_j$ of a row are distinct. So line L8 finds $r = \ell_i + c_j$, and line L9 returns $c_j$, with $d(r, c_j) = \mathrm{wt}(r - c_j) = \mathrm{wt}(\ell_i)$. For any codeword $c$, $r - c = \ell_i + (c_j - c) \in \ell_i + C$, so by Lemma 2, $d(r, c) = \mathrm{wt}(r - c) \ge \mathrm{wt}(\ell_i) = d(r, c_j)$. $\square$

**Corollary 1 (which errors are corrected).** Let $c$ be sent and $r = c + e$ be received. Then DECODE$(r) = c$ if and only if $e$ is the leader of its coset.

*Proof.* $r$ lies in the coset $e + C$, say row $i$, so $r = \ell_i + c_j$ and DECODE returns $c_j = c + e - \ell_i$. This equals $c$ if and only if $e = \ell_i$. $\square$

**Corollary 2 (t errors).** Let $C$ have minimum distance $d$ and $t = \lfloor (d - 1)/2 \rfloor$. Every error $e$ with $\mathrm{wt}(e) \le t$ is corrected.

*Proof.* Let $\ell$ be the leader of $e + C$. Then $\mathrm{wt}(\ell) \le \mathrm{wt}(e) \le t$, and $e - \ell \in C$ has weight at most $\mathrm{wt}(e) + \mathrm{wt}(\ell) \le 2t < d$. The only codeword of weight less than $d$ is $0$, so $e = \ell$, and Corollary 1 applies. $\square$

On a binary symmetric channel with crossover probability $p < 1/2$, an error of weight $w$ has probability $p^w (1 - p)^{n-w}$, which falls as $w$ grows. So by the Theorem the standard array decoder is a maximum likelihood decoder on that channel, and by Corollary 1 its probability of correct decoding is $\sum_i p^{\mathrm{wt}(\ell_i)} (1 - p)^{n - \mathrm{wt}(\ell_i)}$. $\blacksquare$
