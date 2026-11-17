---
title: Each restart of randomized motif search ends in a local optimum within a bounded number of steps
proves: [correctness]
status: full
---

Let $s_1, \ldots, s_n$ be DNA sequences with at least $L$ letters each. For windows $t = (t_1, \ldots, t_n)$ with $t_i$ a window of $s_i$, let $c_j(a)$ be the number of windows with letter $a$ in column $j$, and $\mathrm{Score}(t) = \sum_{j=1}^{L} (n - \max_a c_j(a))$. The profile with pseudocount 1 is $P_j(a) = (c_j(a) + 1)/(n + 4)$.

**Lemma 1 (line L7 picks a most probable window).** For each $i$, line L7 returns the first window $w$ of $s_i$ with the largest $\prod_j P_j(w_j)$.

*Proof.* For every column, $\sum_a (c_j(a) + 1) = n + 4$, so $\prod_j P_j(w_j) = \prod_j (c_j(w_j) + 1)/(n + 4)^L$. The denominator is the same positive number for all windows, so the order of the probabilities is the order of the integer products. The code computes these products exactly, starts from the value $-1$ and keeps a window only when its product is strictly larger, so it returns the first window with the largest product. $\square$

**Lemma 2 (the score bound).** For every choice of windows, $\mathrm{Score}(t) \le L(n - \lceil n/4 \rceil)$.

*Proof.* In column $j$ the four counts sum to $n$, so the largest is at least $n/4$, and since it is an integer, at least $\lceil n/4 \rceil$. Each column term is at most $n - \lceil n/4 \rceil$, and there are $L$ columns. $\square$

**Theorem.** Let a restart start from windows $t^{(0)}$. Then:

1. Every tuple it holds has one window from each sequence, and the scores of the tuples it holds strictly decrease.
2. It makes at most $\mathrm{Score}(t^{(0)}) + 1 \le L(n - \lceil n/4 \rceil) + 1$ profile steps, so it stops.
3. When it stops with windows $t$, the windows $t'$ that the profile of $t$ picks by Lemma 1 have $\mathrm{Score}(t') \ge \mathrm{Score}(t)$.

*Proof.* (1) Line L3 picks a window of each sequence, and line L7 picks a window of each sequence. Line L8 replaces $t$ only by a tuple with a strictly smaller score.

(2) Number the profile steps $1, 2, \ldots$. Every step but the last is accepted at line L8 and lowers the integer score by at least 1. The score is at least 0, so at most $\mathrm{Score}(t^{(0)})$ steps are accepted, and the next step is rejected and ends the loop. So there are at most $\mathrm{Score}(t^{(0)}) + 1$ steps, and Lemma 2 gives the second bound.

(3) The loop ends only at line L9, which runs when the test of line L8 fails, that is, when $\mathrm{Score}(t') \ge \mathrm{Score}(t)$ for the windows $t'$ that line L7 picked from the profile of the current $t$. $\square$

**Corollary (the best restart).** RANDOMIZED-MOTIF returns the tuple of the first restart with the smallest final score over the $R$ restarts. Line L10 replaces $best$ only by a strictly smaller score, as in the proof for the greedy search. The result is a valid choice of windows, and its score is at least the optimum of the motif finding problem.

**Cost.** A profile step builds the counts in $O(nL)$ time and scans $nW$ windows at $O(L)$ each, so it takes $O(nWL)$ time. By the theorem, a restart makes $O(nL)$ steps, and $R$ restarts take $O(R L^2 n^2 W)$ time in the worst case. The extra space is the counts and the current windows, $O(nL)$.

The theorem does not say that a restart reaches an optimum, and it often does not: on the Rosalind sample BA2F, 2 of 1000 restarts with seed 0 reach the optimal score 9. The success rate over restarts is a measurement, given on the page.
