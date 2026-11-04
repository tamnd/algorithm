---
title: Balanced merge sort sorts stably in ceil(log_P S) passes
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode. Let $P = \lfloor T/2 \rfloor \ge 2$. Let $R_0, R_1, \ldots, R_{S-1}$ be the runs made by line L4, in this order, and let $F_j$ be the part of $F$ that run $R_j$ came from. So $F = F_0 F_1 \cdots F_{S-1}$ and $R_j$ is the stable sort of $F_j$. For a sequence $X$, write $\operatorname{st}(X)$ for its stable sort.

**Lemma (merge).** If $X_1, \ldots, X_g$ are sequences and the merge of $\operatorname{st}(X_1), \ldots, \operatorname{st}(X_g)$ takes the run with the smaller index on equal keys, the result is $\operatorname{st}(X_1 \cdots X_g)$.

This is Lemma 1 of the proof page of [external merge sort](/external-merge-sort/); the same proof applies.

**Invariant.** At each test of line L5 there are a number $s \ge 0$ and consecutive parts $G_0, \ldots, G_{s-1}$ of $F$, with $F = G_0 \cdots G_{s-1}$, such that for each $c < s$ the run $\operatorname{st}(G_c)$ is the run at index $\lfloor c/P \rfloor$ of tape $A_{c \bmod P}$, and the tapes $A$ hold no other runs.

*Initialization.* Line L4 writes run $R_j$ to tape $A_{j \bmod P}$, and it is the $\lfloor j/P \rfloor$-th run written to that tape, because the runs $j' < j$ with $j' \equiv j \pmod P$ are exactly $\lfloor j/P \rfloor$ in number. So the invariant holds with $s = S$ and $G_c = F_c$.

*Maintenance.* In iteration $i$ of line L7, the tapes $A_d$ that still have a run at index $i$ are those with $iP + d < s$, so line L8 merges the runs $\operatorname{st}(G_c)$ for $iP \le c < \min(iP + P, s)$, in the order of $d$, which is the order of $c$. By the lemma, the result is $\operatorname{st}(G'_i)$ with $G'_i = G_{iP} \cdots G_{\min(iP+P, s) - 1}$. The loop of line L7 runs for $i = 0, \ldots, \lceil s/P \rceil - 1$. Line L8 writes $\operatorname{st}(G'_i)$ to $B_{i \bmod P}$, and it is the $\lfloor i/P \rfloor$-th run written to that tape, by the same count as in the initialization. The parts $G'_i$ are consecutive and their concatenation is $F$. After line L9 renames $B$ to $A$, the invariant holds with $s' = \lceil s/P \rceil$ and the parts $G'_i$.

**Termination and the pass count.** The loop of line L5 runs while $s \ge 2$, and a pass maps $s$ to $\lceil s/P \rceil$. For $s \ge 2$ and $P \ge 2$, $\lceil s/P \rceil \le \lceil s/2 \rceil \le s - 1$, so the loop stops. For integers $x \ge 1$, $\lceil \lceil x/P^q \rceil / P \rceil = \lceil x/P^{q+1} \rceil$, so after $q$ passes $s = \lceil S/P^q \rceil$. This is 1 exactly when $P^q \ge S$. So for $S \ge 1$ the number of passes is $\lceil \log_P S \rceil$.

**Theorem.** BALANCED-MERGE-SORT returns $\operatorname{st}(F)$ on tape $A_0$.

*Proof.* If $N = 0$, there are no runs, and the result is empty. Else the loop stops with $s = 1$, and by the invariant the only run is $\operatorname{st}(G_0)$ with $G_0 = F$, at index 0 of tape $A_{0}$. $\blacksquare$
