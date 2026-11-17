---
title: Greedy motif search returns valid windows with the best score over its seeds
proves: [correctness]
status: full
---

Let $s_1, \ldots, s_n$ be DNA sequences, each with at least $L$ letters, and let $b \ge 0$ be an integer pseudocount. The claim is about what GREEDY-MOTIF returns. It does not claim that the result is optimal, and the last part of this note shows that it is not always optimal.

**Lemma 1 (the counts).** When line L6 runs for sequence $s_i$, $c_j(a) = b + \#\{k < i : t_k[j] = a\}$ for every column $j$ and letter $a$.

*Proof.* Line L3 sets every count to $b$. Before line L6 runs for $s_i$, line L5 has run once for each of $s_2, \ldots, s_i$, and the run for $s_k$ adds the letters of $t_{k-1}$. So the windows added are $t_1, \ldots, t_{i-1}$, each once. $\square$

**Lemma 2 (line L6 picks a most probable window).** Let $P_j(a) = c_j(a) / (i - 1 + 4b)$ be the profile of the counts of Lemma 1. Line L6 returns the first window $w$ of $s_i$ with the largest $\prod_j P_j(w_j)$.

*Proof.* By Lemma 1, $\sum_a c_j(a) = i - 1 + 4b$ for every column, so $\prod_j P_j(w_j) = \prod_j c_j(w_j) / (i - 1 + 4b)^L$ for every window $w$. The denominator is positive and the same for all windows, so the order of the probabilities is the order of the integer products. The code computes the products exactly with integers, keeps a window only when its product is strictly larger than the best so far, and starts with the value $-1$, so the first window with the largest product is returned. If every product is 0, the first window has the largest product and is returned. $\square$

**Lemma 3 (the result is a choice of windows).** Each tuple formed in a seed run, and the start tuple of line L1, has one window of length $L$ from each sequence, and the start recorded for $s_i$ is the start of that window.

*Proof.* Line L1 takes the first window of each sequence. In a seed run, $t_1$ is a window of $s_1$ by line L3, and each $t_i$ for $i \ge 2$ is a window of $s_i$ by line L6. The code stores the start $p$ and the window $s_i[p .. p + L - 1]$ together. $\square$

**Theorem.** GREEDY-MOTIF returns a tuple $(t_1, \ldots, t_n)$ with $t_i$ a window of $s_i$, and its motif score is the smallest score among the start tuple of line L1 and the $W$ tuples of the seed runs. Among tuples with this score, it is the first one in the order start tuple, seed 1, seed 2, and so on.

*Proof.* By Lemma 3 every candidate is a valid choice of windows. The value of $best$ changes only at line L7, and only to a candidate with a strictly smaller score. So after all seeds, $bestscore$ is the minimum of the scores of the candidates, and $best$ is the first candidate that reached it. Line L8 returns it. $\square$

**Cost.** There are $W$ seeds. In each seed run, line L5 costs $O(L)$ per sequence, and line L6 looks at $W$ windows of $L$ letters, so a seed run costs $O(n W L)$, and line L7 adds $O(nL)$. The total is $O(W^2 n L)$ time. The counts take $4L$ integers and the current tuple $n$ windows, so the extra space is $O(nL)$.

**The result is not always optimal.** Take $s_1 = $ CAGAACCT, $s_2 = $ GCTGTGAC, $s_3 = $ ATAAACTA, $L = 3$ and $b = 0$. The tuple AAC, GAC, AAC (1-based starts 4, 6, 4) has score 1, and no tuple has score 0, since no window of $s_1$ occurs in all three sequences. The six seed runs give scores 6, 3, 4, 3, 2 and 4. For the seed AAC, no window of $s_2$ equals AAC, so every product is 0 and Lemma 2 gives the first window GCT. The start tuple CAG, GCT, ATA has score 6. So the result has score 2, above the optimum 1. With $b = 1$ the seed AAC gives GAC a positive probability, and the search returns the optimum. The tests check both runs, and check on random inputs that the greedy score is never below the brute-force optimum.
