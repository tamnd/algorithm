---
title: The suffix array search returns the maximal mappable prefix with all its places, the stitching is optimal over the seed diagonals, and exact reads are found
proves: [correctness]
status: full
---

We use the pseudocode of the page and the code. The genome is $G$ of length $n$ and the read is $R$ of length $L$. Positions here are 0-based, as in the code. For a string $s$, the *maximal mappable prefix* is the longest prefix $s[0..\ell - 1]$ that occurs in $G$, with $\ell = 0$ if no letter of $s$ occurs. A *diagonal* $d$ aligns read base $x$ to genome base $x + d$. The scores are $+1$ for a match and $-1$ for a mismatch, and an intron costs a penalty $\pi > 0$ that depends on its first two and last two bases.

## 1. The seed search

The suffix array $SA$ lists the starts of the suffixes of $G$ in lexicographic order. Write $T_j = G[SA[j]..n - 1]$ and $\mathrm{lcp}(a, b)$ for the length of the longest common prefix.

**Lemma 1.** For strings $A \le B \le C$, $\mathrm{lcp}(A, C) = \min(\mathrm{lcp}(A, B), \mathrm{lcp}(B, C))$.

*Proof.* Let $m = \min(\mathrm{lcp}(A, B), \mathrm{lcp}(B, C))$. All three agree on the first $m$ letters, so $\mathrm{lcp}(A, C) \ge m$. Suppose $\mathrm{lcp}(A, C) > m$, and say $m = \mathrm{lcp}(A, B)$ (the other case is the same with the roles of $A$ and $C$ swapped). Then $A$ and $C$ agree at position $m$, and $B$ differs from $A$ there or ends there. If $B$ ends at $m$, then $B$ is a proper prefix of $A$ and $B < A$, against $A \le B$. If $B[m] < A[m] = C[m]$ then $B < A$, and if $B[m] > A[m] = C[m]$ then $B > C$. Both contradict the order. $\square$

**Lemma 2.** Let $p$ be the first index with $T_p \ge s$ (in the order where a string is compared with $s$ cut to the length of $s$). Then $\max_j \mathrm{lcp}(s, T_j)$ is attained at $j = p - 1$ or $j = p$.

*Proof.* For $j < p - 1$ we have $T_j \le T_{p-1} < s$, so by Lemma 1, $\mathrm{lcp}(T_j, s) \le \mathrm{lcp}(T_{p-1}, s)$. For $j > p$ we have $s \le T_p \le T_j$, so in the same way $\mathrm{lcp}(s, T_j) \le \mathrm{lcp}(s, T_p)$. Comparing $T_j$ cut to $|s|$ with $s$ gives the same order as comparing $T_j$ with $s$, except that a $T_j$ that has $s$ as a prefix counts as equal, which is also $\ge s$. So the lemma holds for the order that the code uses. $\square$

**Theorem 1 (seed search).** MMP returns the length $\ell$ of the maximal mappable prefix of $s$ and the sorted list of all positions where $s[0..\ell - 1]$ occurs in $G$.

*Proof.* A prefix of $s$ of length $m$ occurs in $G$ if and only if some suffix $T_j$ has $\mathrm{lcp}(s, T_j) \ge m$. So $\ell = \max_j \mathrm{lcp}(s, T_j)$, which the code computes at the two neighbors of Lemma 2. The suffixes that start with $P = s[0..\ell - 1]$ form one contiguous block of $SA$, since they are exactly those with $T_j$ cut to $\ell$ equal to $P$, and the cut suffixes are sorted. The two binary searches find the first index with cut suffix $\ge P$ and the first with cut suffix $> P$, which are the ends of this block. $\square$

## 2. The stitching

Let $\Delta$ be a finite set of diagonals. An *alignment over $\Delta$* chooses a read interval $[s, e]$, soft-clips the rest, and gives each $x \in [s, e]$ a diagonal $d_x \in \Delta$ with $0 \le x + d_x < n$, such that for each $x < e$ either $d_{x+1} = d_x$, or $d_{x+1} - d_x \in [\mathrm{min\_intron}, \mathrm{max\_intron}]$, which is an intron from $G[x + 1 + d_x]$ to $G[x + d_{x+1}]$. Its score is the sum of the base scores minus the penalties of its introns.

**Theorem 2 (stitching is optimal).** STITCH returns an alignment over $\Delta$ of the best score, and its CIGAR, read from left to right, spells exactly this alignment. If no alignment over $\Delta$ has a positive score, it returns nothing.

*Proof.* Let $F(x, d)$ be the best score of an alignment over $\Delta$ whose last base is $x$ on diagonal $d$. The last step of such an alignment is one of three cases: $x$ is also its first base, the base $x - 1$ is on $d$ as well, or the base $x - 1$ is on an allowed $d'$ with an intron in between. So
$$F(x, d) = \sigma(x, d) + \max\bigl(0,\ F(x - 1, d),\ \max_{d'} F(x - 1, d') - \pi(x, d', d)\bigr),$$
where the inner maximum runs over the $d'$ in $\Delta$ with $d - d'$ in the intron range and a defined $F(x - 1, d')$. This is the recurrence of the code, by induction on $x$; the value 0 stands for starting a new alignment at $x$. Every alignment ends at some $(x, d)$, so the best of all $F(x, d)$ is the best score. The back pointers record which case gave each value, so following them from the best cell spells an alignment with that score. The CIGAR starts with the soft-clip of the bases before the start, gives one M block per run of equal diagonals, an N block of length $d_{x+1} - d_x$ between runs, and a final soft-clip, so it spells the same alignment. The code returns nothing when the best value is at most 0. $\square$

Each base adds at most $+1$ and each intron subtracts $\pi > 0$, so every alignment has score at most $L$, with equality only if every base is aligned, matches, and there is no intron.

## 3. Exact reads

**Theorem 3 (an exact unspliced read).** Suppose $R$ occurs in $G$ at exactly one position $p$, $L \ge s_{\min}$, $n_{\max} \ge 1$ and $\mathrm{min\_frac} \le 1$. Then the algorithm returns the score $L$, the position $p$ and the CIGAR $L$M.

*Proof.* By Theorem 1, the first search gives $\ell = L$ and the places $\{p\}$, so line L4 adds the diagonal $p$, and line L5 moves past the end of the read. So $\Delta = \{p\}$. The alignment of all of $R$ on $p$ scores $L$, the most possible, and by the remark after Theorem 2 any alignment of score $L$ over $\Delta$ is this one. In the code, $F(x, p) = x + 1$ grows strictly, so the best cell is the last base, and each back pointer goes to the base before, because $F(x - 1, p) = x > 0$. So the code returns this alignment, and line L7 accepts it since $L \ge \mathrm{min\_frac} \cdot L$. $\square$

**Theorem 4 (an exact read across one intron).** Suppose $R[0..j - 1]$ matches $G$ on the diagonal $d_1$ and $R[j..L - 1]$ matches on $d_2$, with $d_2 - d_1$ in the intron range and penalty $\pi$ for this intron. Let $\ell$ be the length of the maximal mappable prefix of $R$. Suppose $G[d_1 .. d_1 + \ell - 1] = R[0..\ell - 1]$, $\ell \ge s_{\min}$, $L - \ell - 1 \ge s_{\min}$, and the first two searches find at most $n_{\max}$ places each. Then the returned alignment has score at least $L - \pi$.

*Proof.* The first search gives $\ell \ge j$, because $R[0..j - 1]$ occurs at $d_1$. Its places hold $d_1$ by the assumption, so $d_1 \in \Delta$. The second search starts at $\ell + 1 > j$, and $R[\ell + 1..L - 1]$ occurs in $G$ on $d_2$, so its maximal mappable prefix is all of it, of length $L - \ell - 1 \ge s_{\min}$, with the place on $d_2$ among its places. So $d_2 \in \Delta$. The true alignment, $j$ bases on $d_1$ and then the rest on $d_2$, is an alignment over $\Delta$ of score $L - \pi$, and by Theorem 2 the result scores at least this. $\square$

## 4. What is not proved

Theorem 4 does not say that the result is the true alignment. Another alignment over $\Delta$ can have the same score: for example the junction can often move by a base when the end of one exon equals the end of the intron, and then the penalty of the motif decides. The conditions of Theorem 4 can also fail. When one side of the junction has fewer than about $s_{\min}$ bases, the second seed is not found and the short end is soft-clipped, and when the first MMP runs past the junction on another place than $d_1$, the diagonal $d_1$ is missing. How often reads are still placed exactly is a measurement, which the tests make. $\blacksquare$
