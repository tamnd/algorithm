---
title: The suffix array test finds exactly the MUMs, and the chain is the heaviest increasing set
proves: [correctness]
status: full
---

Let $S = A\#B\$$, where $\#$ and $\$$ occur nowhere else. Let $SA$ be the suffix array of $S$ and $LCP[r]$ the length of the longest common prefix of the suffixes of ranks $r-1$ and $r$. A *maximal unique match* (MUM) of length at least $\ell$ is a triple $(i, j, L)$ with $L \ge \ell$, $A[i \ldots i+L-1] = B[j \ldots j+L-1] = u$, $u$ occurs exactly once in $A$ and exactly once in $B$, and the match can be extended neither to the left ($i = 0$, $j = 0$ or $A[i-1] \ne B[j-1]$) nor to the right ($i + L = |A|$, $j + L = |B|$ or $A[i+L] \ne B[j+L]$).

**Fact (intervals).** The suffixes of $S$ that start with a nonempty string $u$ without $\#$ and $\$$ have consecutive ranks $r_1 \ldots r_2$, and $LCP[r] \ge |u|$ exactly for $r_1 < r \le r_2$. This holds because the suffixes are in sorted order, and the common prefix of two suffixes is the minimum of the $LCP$ values between their ranks.

**Lemma 1 (soundness of L3 to L7).** Every triple that line L7 outputs is a MUM.

*Proof.* At L7, ranks $r-1$ and $r$ hold one suffix from $A$ and one from $B$ (L4) with $LCP[r] = L \ge \ell$, so $u = A[i \ldots i+L-1] = B[j \ldots j+L-1]$. The common prefix cannot contain $\#$ or $\$$, since each occurs once, so it lies inside $A$ and inside $B$. The prefix stops at $L$, so the letters after it differ or one side ends: the match is right-maximal. L5 checks $LCP[r-1] < L$ and $LCP[r+1] < L$, so by the Fact the interval of $u$ is exactly $\{r-1, r\}$, and $u$ occurs once in $A$ and once in $B$. L6 checks left-maximality. $\square$

**Lemma 2 (completeness).** Every MUM $(i, j, L)$ with $L \ge \ell$ is output.

*Proof.* The string $u$ occurs exactly twice in $S$, at $i$ and at $|A| + 1 + j$. By the Fact the two suffixes have adjacent ranks $r-1$ and $r$, and $LCP[r-1] < L$ and $LCP[r+1] < L$ (when they exist). The match is right-maximal, so $LCP[r] = L$ exactly: if $i + L < |A|$ and $j + L < |B|$ the next letters differ, and if one side ends, the next letter of $S$ there is $\#$ or $\$$, which the other side cannot match. So L4, L5 and L6 all pass and L7 outputs $(i, j, L)$. $\square$

**Lemma 3 (distinct starts).** No two MUMs share a start in $A$, and no two share a start in $B$.

*Proof.* Let $(i, j, L)$ and $(i, j', L')$ be MUMs with $L \le L'$. Then $A[i \ldots i+L-1]$ is a prefix of $A[i \ldots i+L'-1] = B[j' \ldots j'+L'-1]$, so it occurs in $B$ at $j'$. It occurs once in $B$, so $j = j'$, and then $L = L'$ by right-maximality. The same argument holds for $B$. $\square$

**Theorem (chaining).** Lines L8 to L13 return a chain $C$ of MUMs whose starts increase strictly in $A$ and in $B$ and whose total length is the largest among all such chains.

*Proof.* By Lemma 3, sorting by the start in $A$ (L8) gives a strict order. Let $f(x)$ be the largest weight of a valid chain that ends with the MUM $x$. A valid chain that ends with $x$ is either $x$ alone or a valid chain that ends with some $y$ before $x$ in the order with $b_y < b_x$, followed by $x$. So $f(x) = L_x + \max(0, \max\{f(y) : y \text{ before } x,\ b_y < b_x\})$. When $x$ is processed, the Fenwick tree holds $f(y)$ at the rank of $b_y$ for exactly the MUMs $y$ before $x$, and the query at L10 returns the largest of them over ranks below the rank of $b_x$, which are the $y$ with $b_y < b_x$ since the starts in $B$ are distinct. So L11 computes $f(x)$. L13 takes the largest $f$, and the pointers rebuild a chain of that weight. $\square$

This is the longest increasing subsequence of the starts in $B$, in the order of the starts in $A$, weighted by length. Each step costs $O(\log u)$ for $u$ MUMs.

**Gap closing.** Lines L14 to L17 build an alignment of $A$ with $B$: the parts covered by the chain, after the trimming at L15, are matched letter for letter, and each gap between them is aligned by an optimal global alignment of the two gap strings. The trimmed parts stay in order, because the starts increase and the trim moves a start to the end of the previous part. So the result is a valid alignment, and its cost is at least the edit distance of $A$ and $B$. It is not always optimal: the chain fixes the matched blocks, and a cheaper alignment may use other matches.
