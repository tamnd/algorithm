---
title: The rank/select dictionary returns rank and select correctly
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page. $P[0 \ldots m-1]$ lists the positions of the 1s of $B$ in increasing order, so $\text{select}_1(j) = P[j - 1]$ for $1 \le j \le m$. The parameters $k_1, k_2 \ge 1$ and $T_1, T_2 \ge 1$ are fixed. The correctness does not depend on their values; only the time and the space do.

**Lemma 1 (BUILD-SELECT).** After BUILD-SELECT, for each group $g$, with $Q = Q_g = P[g k_1 \ldots \min(m, (g+1)k_1) - 1]$: $G[g] = Q[0]$; if $\max Q - \min Q \ge T_1$ then sparse$[g]$ is true and $E_1[g] = Q$; otherwise sparse$[g]$ is false and, for each $h$, with $R = Q[h k_2 \ldots \min(|Q|, (h+1)k_2) - 1]$: $S[g][h] = R[0] - Q[0]$, and $E_2[g][h]$ is the list $(r - Q[0])_{r \in R}$ if $\max R - \min R \ge T_2$, and empty otherwise.

*Proof.* The loop of line L1 runs once for each $g$ with $0 \le g < \lceil m/k_1 \rceil$, so $g k_1 < m$ and $Q$ is not empty. Lines L2 to L4 and L6 set the fields of group $g$ as stated, since $P$ is increasing and so $Q[0] = \min Q$ and $Q[\text{last}] = \max Q$. Likewise, for a dense group, the loop of line L7 runs once for each $h$ with $h k_2 < |Q|$, so $R$ is not empty, and lines L8 to L11 set $S[g][h]$ and $E_2[g][h]$ as stated. No step writes the fields of another group. $\square$

**Lemma 2 (SCAN).** If $p \le P[a]$ and no 1 lies in positions $p, \ldots, P[a] - 1$, then SCAN$(p, u)$ returns $P[a + u - 1]$ for each $u \ge 1$ with $a + u - 1 < m$.

*Proof.* The 1s at positions $\ge p$ are, in order, $P[a], P[a+1], \ldots$, so the $u$-th of them is $P[a + u - 1]$. SCAN masks the bits below $p$ in the word of $p$, so the words it reads contain exactly the 1s at positions $\ge p$, in increasing order. The loop subtracts the full counts of words that hold fewer than the remaining number of wanted 1s, as in SELECT1 of the [bit vector](/bit-vector/); by the same invariant, it stops at the word that holds the wanted 1, and the clearing of the lowest bits finds it. The loop stops because $a + u - 1 < m$, so the wanted 1 exists. $\square$

**Lemma 3 (SELECT1).** For $1 \le j \le m$, SELECT1$(j)$ returns $P[j - 1]$.

*Proof.* Write $j - 1 = g k_1 + t$ with $0 \le t < k_1$, as line L12 does. Then $P[j-1]$ is element $t$ of $Q_g$: the group $Q_g$ starts at index $g k_1$ of $P$, and $t < |Q_g|$ because $g k_1 + t = j - 1 < m$ and $t < k_1$.

*Case 1: group $g$ is sparse.* By Lemma 1, $E_1[g] = Q_g$, so line L13 returns $Q_g[t] = P[j-1]$.

*Case 2: group $g$ is dense.* Write $t = h k_2 + u$ with $0 \le u < k_2$, as line L14 does. Element $t$ of $Q_g$ is element $u$ of the subgroup $R = R_{g,h}$, and $u < |R|$ by the same argument as above.

- If $E_2[g][h]$ is not empty, by Lemma 1 it holds $R[u] - Q_g[0]$ at index $u$, and $G[g] = Q_g[0]$, so line L15 returns $R[u] = P[j-1]$.
- Otherwise, line L16 calls SCAN$(p, u + 1)$ with $p = G[g] + S[g][h] = Q_g[0] + (R[0] - Q_g[0]) = R[0]$. $R[0]$ is $P[a]$ for $a = g k_1 + h k_2$, and $p = P[a]$, so the hypothesis of Lemma 2 holds. SCAN returns $P[a + u] = R[u] = P[j - 1]$. $\square$

**Lemma 4 (SELECT0).** The same argument, applied to the list of the positions of the 0s and to the masked complement of the words, shows that SELECT0$(j)$ returns the position of the $j$-th 0. The mask of the last word removes the padding bits, which the complement would turn into false 0s.

**Lemma 5 (RANK1).** For $0 \le i \le n$, RANK1$(i)$ returns $\text{rank}_1(i)$.

*Proof.* With $k = \lfloor i/w \rfloor$ and $q = \lfloor k/s \rfloor$, the build stores $RS[q] = \text{rank}_1(q s w)$ and $RB[k] = \text{rank}_1(k w) - RS[q]$. The term POPCOUNT$(W[k] \wedge (2^{i \bmod w} - 1))$ counts the 1s at positions $kw$ to $i - 1$. The sum is $\text{rank}_1(i)$, as in the proof for [Jacobson's rank structure](/jacobson-rank/). The build stores one word past the last full word, so $W[k]$ exists for $i = n$. $\blacksquare$

**The time bound.** For the default parameters a dense subgroup has span less than $T_2$, and its $(u+1)$-th 1 lies in $[R[0], R[\text{last}]]$, so SCAN reads at most $\lceil T_2 / w \rceil + 1$ words. With $T_2 = \lceil \lg \ell \rceil^4$ and $w \ge \ell - 1$, this is $O(1)$ words for $n$ large enough, and each other line does $O(1)$ work.
