---
title: The r-index counts and locates correctly from O(r) samples
proves: [correctness]
status: full
---

Let $t = S\$$ with $|t| = N = n + 1$, where $\$$ is the unique smallest symbol and $t[N-1] = \$$. Let $SA$ be its suffix array, $ISA$ the inverse, and $BWT[i] = t[(SA[i] - 1) \bmod N]$. Let $C[c]$ be the number of symbols of $t$ smaller than $c$ and $rank_c(i)$ the number of $c$ in $BWT[0 \ldots i-1]$. Define $LF(i) = C[c] + rank_c(i)$ for $c = BWT[i]$. A row $i$ is a *run start* if $i = 0$ or $BWT[i] \ne BWT[i-1]$, and a *run end* if $i = N - 1$ or $BWT[i] \ne BWT[i+1]$.

**Lemma 1 (LF).** $SA[LF(i)] = (SA[i] - 1) \bmod N$. Moreover, if $X$ is a string and $[sp, ep)$ is the set of rows whose suffixes start with $X$, then the rows whose suffixes start with $cX$ are $[C[c] + rank_c(sp),\ C[c] + rank_c(ep))$, and for each row $i \in [sp, ep)$ with $BWT[i] = c$, $LF(i)$ is in this range, in the same order.

*Proof.* Let $j = SA[i]$ and $c = BWT[i] = t[j-1]$ (cyclically). The suffixes that start with $c$ are the rows $C[c]$ to $C[c + 1] - 1$, sorted by what follows $c$. The suffix $t_{j-1} = c\,t_j$ is preceded, among those starting with $c$, exactly by the $c\,t_{j'}$ with $t_{j'} < t_j$, that is with $BWT$ value $c$ in a row before $i$; there are $rank_c(i)$ of them. So the row of $t_{j-1}$ is $C[c] + rank_c(i)$. (For $c = \$$, $j = 0$ and $t_{N-1} = \$$ is row 0 $= C[\$] + 0$.) The suffixes starting with $cX$ are the $c\,t_j$ with $t_j$ starting with $X$, that is with rows in $[sp, ep)$ and $BWT = c$; these are mapped by $LF$ in order onto consecutive rows starting at $C[c] + rank_c(sp)$, and their number is $rank_c(ep) - rank_c(sp)$. $\square$

**Lemma 2 (run-length rank).** Let the runs of $c$ be $[s_1, e_1], \ldots, [s_q, e_q]$ in order and $b_j$ the number of $c$ before $s_j$. For $0 \le i \le N$, let $j$ be the largest index with $s_j \le i - 1$ (none if $i - 1 < s_1$). Then $rank_c(i) = 0$ if there is no such $j$, and otherwise $rank_c(i) = b_j + \min(i, e_j + 1) - s_j$.

*Proof.* Every $c$ before row $i$ lies in a run of $c$ that starts before $i$, so in runs $1, \ldots, j$. Runs $1$ to $j - 1$ end before $s_j$ and contribute $b_j$ in total. Run $j$ contributes the rows from $s_j$ to $\min(e_j, i - 1)$. $\square$

Similarly, $BWT[i]$ is the head of the last run with start at most $i$. So the run tables compute $C$, $rank$ and $BWT$ exactly.

**Lemma 3 (toehold).** Suppose $[sp, ep)$ is nonempty, $s = SA[ep - 1]$, and some row in $[sp, ep)$ has $BWT = c$. Let $q$ be the last such row and $[sp', ep')$ the new range from Lemma 1. Then $SA[ep' - 1] = SA[q] - 1$, and $SA[q] = s$ if $q = ep - 1$, while otherwise $q$ is a run end of a run of $c$, namely the end of the last run of $c$ that starts before $ep$.

*Proof.* By Lemma 1, $LF$ maps the rows of $[sp, ep)$ with $BWT = c$ in order onto $[sp', ep')$, so the last one, $q$, goes to $ep' - 1$, and $SA[ep' - 1] = SA[q] - 1$ (not cyclic, since $c \ne \$$ gives $SA[q] \ge 1$). If $q < ep - 1$, then $BWT[q + 1] \ne c$ because $q$ is the last $c$ in the range and $q + 1 \le ep - 1$; so $q$ is a run end. The run of $q$ starts at or before $q < ep$, and no later run of $c$ starts before $ep$, since its rows would be $c$ rows in $(q, ep)$. $\square$

**Search.** By induction on the number of symbols read, SEARCH keeps $[sp, ep)$ as the rows of the current suffix of $P$, and $s = SA[ep - 1]$ when the range is not empty. At the start, the range is all rows and $s = SA[N - 1]$, which is the sample at the end of the last run. In a step, line L4 or L5 finds $SA[q]$ by Lemma 3; if no row of the range has $BWT = c$, then the last run of $c$ that starts before $ep$ ends before $sp$, or does not exist, and the new range is empty by Lemma 1, so returning empty is correct. Lines L6 to L8 compute the new range and the new toehold. So `count(P)` $= ep - sp$ is the number of suffixes of $t$ that start with $P$, which is the number of occurrences of $P$ in $S$, since $P$ contains no $\$$.

**Lemma 4 ($\phi$).** Let $\phi(j) = SA[ISA[j] - 1]$ for each $j$ with $ISA[j] \ge 1$. If $j \ge 1$, $ISA[j] \ge 1$, and $ISA[j]$ is not a run start, then $\phi(j - 1) = \phi(j) - 1$.

*Proof.* Let $i = ISA[j] \ge 1$. As $i$ is not a run start, $BWT[i - 1] = BWT[i] = c$, and $c \ne \$$ because $\$$ occurs once in the BWT. By Lemma 1, $LF(i - 1) = LF(i) - 1$. Then $SA[LF(i)] = j - 1$, so $ISA[j - 1] = LF(i) \ge 1$, and $\phi(j - 1) = SA[LF(i) - 1] = SA[LF(i - 1)] = SA[i - 1] - 1 = \phi(j) - 1$. $\square$

**Lemma 5 ($\phi$ from samples).** Let $K = \{SA[p] - 1 : p \text{ a run start}, SA[p] \ge 1\}$, with the value $\phi(y)$ stored for each $y \in K$. For each $x$ with $0 \le x$ and $ISA[x] \ge 1$, the set $K$ has an element $y \ge x$, and for the smallest one, $\phi(x) = \phi(y) - (y - x)$.

*Proof.* Row 0 is a run start, with $SA[0] = N - 1$, so $N - 2 \in K$ when $N \ge 2$; every $x$ with $ISA[x] \ge 1$ has $x \le N - 2$, since $ISA[N - 1] = 0$. So $y$ exists. For each $z$ with $x < z \le y$, the row $ISA[z]$ is not a run start: if it were, $z - 1 \in K$ (note $SA[ISA[z]] = z \ge 1$) with $x \le z - 1 < y$, against the choice of $y$. Also $ISA[z] \ge 1$ since $z \le N - 2$. By Lemma 4 applied to $z = y, y - 1, \ldots, x + 1$, $\phi(z - 1) = \phi(z) - 1$, and so $\phi(x) = \phi(y) - (y - x)$. $\square$

**Locate.** After SEARCH, $s = SA[ep - 1]$. Each application of $\phi$ in line L9 maps $SA[i]$ to $SA[i - 1]$ for a row $i \ge sp + 1 \ge 1$, which is defined, and Lemma 5 computes it from the samples. So line L9 reports $SA[ep - 1], SA[ep - 2], \ldots, SA[sp]$, the positions of all occurrences, each once. $\blacksquare$
