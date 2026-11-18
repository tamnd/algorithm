---
title: "Binary comparison of UCA sort keys is the comparison level by level, and SORT-KEY terminates"
proves: [correctness, termination]
status: full
---

**Setup.** Let $W = w_1 \cdots w_r$ be the weight array after step S2.3, where each $w_j$ has the weights $w_j^{(1)}, \ldots, w_j^{(k)}$ for the $k$ levels of the option ($k = 3$ for non-ignorable and blanked, $k = 4$ for shifted and shift-trimmed). All weights are integers in $[0, \mathrm{FFFF}]$. For a level $\ell$, let $P_\ell(W)$ be the sequence of the non-zero weights $w_j^{(\ell)}$ in the order of $j$. For shift-trimmed, $P_4(W)$ also has its trailing FFFF weights removed. The UCA order compares $P_1$ of the two strings in lexicographic order, then $P_2$ if they are equal, and so on up to $P_k$. In lexicographic order a proper prefix is smaller.

**Claim 1 (the key).** Lines L9 to L14 return $K(W) = P_1(W)\,0\,P_2(W)\,0 \cdots 0\,P_k(W)$.

*Proof.* Invariant of the loop of line L10: before the iteration for level $\ell$, $K = P_1\,0 \cdots 0\,P_{\ell-1}$ (empty for $\ell = 1$). Line L11 appends the separator if $\ell > 1$, line L12 appends the non-zero weights of level $\ell$ in order, and line L13 removes trailing FFFF weights of level 4 for shift-trimmed. Line L13 only removes weights appended in the same iteration, because the separator 0 before them is not FFFF. So after the iteration $K = P_1\,0 \cdots 0\,P_\ell$. $\square$

**Claim 2.** For two weight arrays $W$ and $V$, the lexicographic comparison of $K(W)$ and $K(V)$ is equal to the comparison level by level.

*Proof.* Let $\ell$ be the first level with $P_\ell(W) \ne P_\ell(V)$. If there is none, the keys are equal and the comparison level by level gives equal too. Otherwise, the two keys have the same prefix $P_1\,0 \cdots 0$ up to the start of level $\ell$, of the same length. Compare $p = P_\ell(W)$ and $q = P_\ell(V)$ from that point.

- If $p$ and $q$ differ at some place $t \le \min(|p|, |q|)$, the keys differ first at the same place, with the same two weights, so both comparisons give the same answer.
- If $p$ is a proper prefix of $q$, then after $p$ the key $K(W)$ has either the separator 0 (if $\ell < k$) or its end (if $\ell = k$). At the same place $K(V)$ has the next weight of $q$, which is non-zero by the definition of $P_\ell$. So $K(W) < K(V)$, and $p < q$ in lexicographic order too. The case where $q$ is a proper prefix of $p$ is symmetric. $\square$

This is the reason why the separator must be lower than every weight and why zero weights must be left out of the key: a 0 inside a level could be read as the end of the level.

**Claim 3 (step S2).** Lines L1 to L7 append, for each match of step S2.1, the elements of that match in the table, or the implicit weights of a code point with no match, in the order of the matches.

*Proof.* Invariant of the loop of line L3: $C$ holds the elements of the matches of $X[0 \ldots i-1]$ in order, and every code point removed from $X$ by line L5 has been added to one of these matches. At line L4, $j$ is the end of the longest prefix of $X[i \ldots]$ that is a key of $T$, which is the rule S2.1, or $i + 1$ if no key starts at $i$. Line L5 visits the non-starters after $j - 1$ in order and stops at the first code point with ccc 0. It keeps the largest ccc $b$ of the non-starters that it skips. Because $X$ is in NFD, a non-starter $c$ is unblocked with respect to the match exactly when $b < \mathrm{ccc}(c)$: a skipped code point with ccc at least $\mathrm{ccc}(c)$ blocks it, and no starter lies in between. If the match plus $c$ is a key, line L5 extends the match and removes $c$, as S2.1.3 says. Line L6 appends the elements of the match or the implicit weights (S2.2, S2.4), and line L7 moves to the code point after the contiguous part of the match (S2.5). The removed code points are later in $X$, so the positions before $j$ do not change and the invariant holds. $\square$

**Claim 4 (variable weighting).** VARIABLE-WEIGHTING follows Table 11 of UTS 10 for shifted, and the definitions of section 4 for the other options.

*Proof.* The implementation keeps a flag that is true when the last element with a non-zero primary weight was variable. For shifted, a variable element becomes $(0, 0, 0, p)$ and sets the flag; a completely ignorable element becomes $(0, 0, 0, 0)$; an element with primary 0 and the flag set becomes $(0, 0, 0, 0)$; any other element keeps its three weights and gets FFFF, and an element with a non-zero primary clears the flag. These are the five rows of Table 11. Blanked is the same with the fourth weight 0 and only three levels. Shift-trimmed is shifted with the trailing FFFF removed in line L13. Non-ignorable keeps all weights. $\square$

**Corollary.** By Claims 1 to 4, COMPARE($A$, $B$) returns the UCA order of $A$ and $B$ for the table $T$ and the option.

**Termination.** In each iteration of the loop of line L3, $j \ge i + 1$, so $i$ increases and the loop runs at most $|X|$ times. The loop of line L5 either removes a code point from $X$ or increases its index, so it stops. The loops of lines L10 and L12 are over finite arrays.
