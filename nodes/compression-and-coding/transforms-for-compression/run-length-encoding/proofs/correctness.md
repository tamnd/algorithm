---
title: The encoder outputs the unique canonical run-length form, and the decoder inverts it
proves: [correctness, termination]
status: full
---

We use the notation of the page. A list of pairs $(c_1, \ell_1), \ldots, (c_r, \ell_r)$ is *canonical* if each $\ell_k \ge 1$ and $c_k \ne c_{k+1}$ for $1 \le k < r$. It *represents* $X$ if $X = c_1^{\ell_1} \cdots c_r^{\ell_r}$.

**Lemma 1 (uniqueness).** Each sequence $X$ is represented by exactly one canonical list.

*Proof.* By induction on $n = |X|$. For $n = 0$, only the empty list represents $X$, since each pair adds at least one symbol. For $n \ge 1$, let $(c_1, \ell_1), \ldots$ be a canonical list for $X$. Then $c_1 = X[0]$, and $X[0 \ldots \ell_1 - 1]$ are copies of $c_1$. If $r \ge 2$, then $X[\ell_1] = c_2 \ne c_1$; if $r = 1$, then $\ell_1 = n$. So $\ell_1$ is the length of the longest prefix of $X$ made of copies of $X[0]$, which depends only on $X$. The rest of the list is a canonical list for $X[\ell_1 \ldots n-1]$, which is unique by induction. $\square$

**Theorem 1 (the encoder).** $\mathrm{RLE\text{-}ENCODE}(X)$ ends and returns the canonical list of $X$.

*Proof.* Invariant at line L2: $0 \le i \le n$, $out$ is a canonical list that represents $X[0 \ldots i-1]$, and if $out$ is not empty, its last symbol is $X[i-1]$ and, when $i < n$, differs from $X[i]$.

*Start.* $i = 0$ and $out$ is empty.

*Step.* Let $i < n$. Line L4 starts with $j = i$, and $X[i] = X[i]$, so $j$ becomes at least $i + 1$. It stops at the first $j > i$ with $j = n$ or $X[j] \ne X[i]$. So $X[i \ldots j-1]$ are copies of $X[i]$, and the pair $(X[i], j - i)$ has count at least 1. By the invariant, the last symbol of $out$ differs from $X[i]$, so after line L5 the list is still canonical, and it represents $X[0 \ldots j-1]$. Its last symbol is $X[i] = X[j-1]$, and if $j < n$, then $X[j] \ne X[i]$. Line L6 sets $i = j$, so the invariant holds again.

*End.* Each step increases $i$ by at least 1 and $i \le n$, so the loop ends after at most $n$ steps, with $i = n$. Then $out$ is a canonical list that represents $X$, which is the canonical list of $X$ by Lemma 1. $\blacksquare$

**Theorem 2 (the decoder).** For each list of pairs with counts at least 1, $\mathrm{RLE\text{-}DECODE}$ returns the sequence it represents. So $\mathrm{RLE\text{-}DECODE}(\mathrm{RLE\text{-}ENCODE}(X)) = X$, and $\mathrm{RLE\text{-}ENCODE}(\mathrm{RLE\text{-}DECODE}(P)) = P$ for each canonical list $P$.

*Proof.* After step $k$ of line D2, $out = c_1^{\ell_1} \cdots c_k^{\ell_k}$, by induction on $k$, and the loop has $r$ steps. The first identity follows from Theorem 1. For the second, $P$ is canonical and represents $\mathrm{RLE\text{-}DECODE}(P)$, so by Lemma 1 and Theorem 1 the encoder returns $P$. $\blacksquare$

**Remark (byte formats).** A byte format is correct if it writes each pair as one or more packets that the decoder reads back as the same symbols. Splitting a run of length $\ell$ into runs of lengths $\ell'_1 + \cdots + \ell'_s = \ell$ of the same symbol represents the same sequence, so the split of long runs in the count-and-byte form, in PackBits, and in the first stage of bzip2 keeps the decoder's output equal to $X$. The resulting list of pairs is not canonical, which does not matter for decoding.
