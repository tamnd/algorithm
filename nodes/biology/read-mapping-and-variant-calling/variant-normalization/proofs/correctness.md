---
title: Normalization returns the unique left-aligned and parsimonious form
proves: [correctness]
status: full
---

Strings are indexed from 0 in this proof, and the variant position $p$ is 1-based as in VCF, so the alleles start at index $i = p - 1$ of the reference. Let $R$ be the reference and let a variant be $(i, x_0, x_1, \ldots, x_k)$ with $k \ge 1$, $x_0 = R[i : i + |x_0|]$ the reference allele, and all alleles non-empty and pairwise different. Allele $x_j$ gives the haplotype

$$H_j = R[0 : i] \; x_j \; R[i + |x_0| : |R|],$$

so $H_0 = R$. Two variants are *equivalent* when they give the same haplotypes $H_0, \ldots, H_k$ in the same order.

Write $P$ for the length of the longest common prefix of $H_0, \ldots, H_k$, $S$ for the length of their longest common suffix, and $m = \min_j |H_j|$. The haplotypes are pairwise different, since the alleles are.

**Hypothesis.** $S < m$, that is, no haplotype is a suffix of all the others. If a haplotype is such a suffix, the event can slide to the start of the reference, and VCF then pads the alleles with the base after the event instead of the base before. The code raises an error in that case.

## Representations as pairs of numbers

**Lemma 1.** The variants equivalent to a given one are in one-to-one correspondence with the pairs of integers $(t, c)$ such that

$$0 \le t \le P, \qquad 0 \le c \le S, \qquad t + c \le m - 1.$$

The pair $(t, c)$ stands for the variant at index $t$ with alleles $y_j = H_j[t : |H_j| - c]$. Its total allele length is $\sum_j |H_j| - (k + 1)(t + c)$.

*Proof.* Take an equivalent variant at index $t$ whose reference allele ends $c$ bases before the end of $R$. Then each $H_j$ is $R[0 : t]\, y_j\, R[|R| - c : |R|]$, so $R[0 : t]$ is a common prefix and $R[|R| - c :]$ a common suffix of all the haplotypes, which gives $t \le P$ and $c \le S$. Each $y_j$ is non-empty, so $t + c \le |H_j| - 1$ for every $j$, that is $t + c \le m - 1$. The alleles are fixed by $t$ and $c$, since $y_j$ is what is left of $H_j$ after the prefix and the suffix.

Conversely, take a pair in the region. The prefix of length $t$ and the suffix of length $c$ are common to all the haplotypes, and since $t + c < |H_j|$ they do not overlap inside any $H_j$. So the strings $y_j = H_j[t : |H_j| - c]$ are non-empty, $y_0 = R[t : |R| - c]$ matches the reference at index $t$, and replacing $y_0$ by $y_j$ gives $H_j$. The $y_j$ are pairwise different, because $y_j = y_l$ would give $H_j = H_l$. The length formula follows from $|y_j| = |H_j| - t - c$. $\square$

## The normalized form

Following Tan, Abecasis and Kang (2015), a variant is *parsimonious* when no equivalent variant has a smaller total allele length, and *left-aligned* when it cannot move one base to the left with all allele lengths kept the same. It is *normalized* when it is both.

**Lemma 2.** The normalized form is the unique pair $(t^*, c^*)$ with

$$c^* = S, \qquad t^* = \min(P,\; m - 1 - S).$$

*Proof.* By Lemma 1 a parsimonious variant maximizes $t + c$ over the region. The largest value is $M = \min(P + S,\; m - 1)$: it is an upper bound by the three constraints, and the pair $(\min(P, m - 1 - S), S)$ reaches it. This pair is in the region because $S \le m - 1$.

Moving one base to the left with the lengths kept is the move from $(t, c)$ to $(t - 1, c + 1)$. On the line $t + c = M$ it is possible exactly when $t \ge 1$ and $c + 1 \le S$. So a pair on that line is left-aligned exactly when $c = S$ or $t = 0$. If $t = 0$, then $c = M \le S$; if also $c < S$, then $M < S$, which is impossible since $M \ge \min(S, m - 1) = S$. So in both cases $c = S$ and $t = M - S = \min(P, m - 1 - S)$. $\square$

## The algorithm reaches the normalized form

Phase 1 is the loop of lines L1 to L5, and phase 2 is the loop of lines L6 and L7. During phase 1 an allele may be empty for a moment. Extend the notation: the state is the index $t$ and the alleles $y_j$, and we track $c = |R| - t - |y_0|$, the number of reference bases after the reference allele.

**Invariant.** At the start of each round of phase 1, and after phase 1, every $H_j$ equals $R[0 : t]\, y_j\, R[|R| - c :]$, with $0 \le t \le P$ and $0 \le c \le S$.

*Proof.* It holds at the start, for the input variant, by the definition of $H_j$ and the argument of Lemma 1. Line L3 removes the last base of every allele when they all end with the same base. The haplotypes do not change, $c$ grows by 1, and the new suffix of length $c$ is common to all $H_j$, so $c \le S$ still holds. Line L5 moves the index one base left and puts $R[t - 1]$ in front of every allele. The haplotypes do not change, $t$ drops by 1, and $c$ stays the same. $\square$

At the start of each round every allele is non-empty: this holds for the input, and an allele that line L3 empties gets one base back from line L5 in the same round. So line L3 always has a last base to compare.

**Termination of phase 1.** Each round that changes something either raises $c$ by 1 or lowers $t$ by 1, so the number $t + (S - c)$, which is at least 0 by the invariant, drops by at least 1 in each such round. So phase 1 stops after at most $t_0 + S$ changes, where $t_0$ is the input index.

**No error under the hypothesis.** Line L5 raises an error only if an allele $y_j$ is empty while $t = 0$. Then $H_j = R[|R| - c :]$ is a common suffix of all the haplotypes, so $S \ge |H_j| \ge m$, which the hypothesis excludes.

**Lemma 3.** When phase 1 stops, $c = S$ and every allele is non-empty.

*Proof.* Phase 1 stops when a full round changes nothing: no allele is empty, and the alleles do not all end with the same base. The last base of $y_j$ is $H_j[|H_j| - c - 1]$. So the haplotypes have a common suffix of length $c$ but not of length $c + 1$, and $c = S$. $\square$

**Lemma 4.** Phase 2 stops with $t = \min(P, m - 1 - S)$ and $c = S$.

*Proof.* Phase 2 moves the index right by one while all alleles start with the same base and all have length at least 2. It does not change $c$ or the haplotypes. At the start of phase 2, $t \le P$ by the invariant, and $t \le m - 1 - S$ because every allele is non-empty, so $t$ starts at most at $t^* = \min(P, m - 1 - S)$.

While $t < t^*$, the step applies. The first base of $y_j$ is $H_j[t]$, and $t < P$ means these bases are all equal. The length of $y_j$ is $|H_j| - t - S \ge m - t - S \ge 2$ since $t \le m - 2 - S$. After the step, $t$ is still at most $t^*$.

When $t = t^*$, the step does not apply. If $t^* = P$, the bases $H_j[P]$ exist since $P \le m - 1 - S < m$, and they are not all equal, by the definition of $P$. If $t^* = m - 1 - S$, some haplotype has $|H_j| = m$, and its allele has length $m - t - S = 1$. $\square$

**Theorem.** If no haplotype is a suffix of all the others, `normalize` returns the normalized form of the variant, and this form depends only on the reference and the haplotypes. So all equivalent variants give the same output.

*Proof.* By Lemmas 3 and 4 the output is the pair $(t^*, S)$, which is the normalized form by Lemma 2. Its values depend only on $P$, $S$ and $m$, which are functions of $H_0, \ldots, H_k$. $\square$

## Cost

Let $L$ be the largest allele length during the run. Each change in phase 1 or phase 2 copies the $k + 1$ alleles, in $O(k L)$ time. Phase 1 makes at most $t_0 + S$ changes, and the alleles reach their final length plus the distance the variant moved, so with $s$ the number of bases the variant moves left, the time is $O(k L (s + L))$. A version that keeps index pairs into the strings instead of copying them runs in $O(k (s + L))$ time.
