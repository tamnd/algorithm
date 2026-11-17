---
title: The all-point AP is the mean over objects of the best precision at or after each hit, and depends only on the ranking
proves: [correctness]
status: full
---

We use the notation of the page. After matching, a class has a ranked list of detections, each a true positive (TP) or a false positive (FP), and $N > 0$ objects that count (the difficult objects of VOC are left out, and so are detections matched to them). Let $P_k$ and $R_k$ be the precision and recall after rank $k$, so $R_k = \mathrm{tp}_k / N$ and $P_k = \mathrm{tp}_k / k$, where $\mathrm{tp}_k$ is the number of TPs among the first $k$ ranks. The interpolated precision is $p_{\mathrm{interp}}(r) = \max\{P_k : R_k \ge r\}$, and 0 when no rank reaches recall $r$. The all-point AP of line L9 is $\sum_k (R_k - R_{k-1}) \, p_{\mathrm{interp}}(R_k)$ with $R_0 = 0$.

**Claim.** Let $r_1 < r_2 < \cdots < r_T$ be the ranks of the $T$ true positives. Then

1. $\mathrm{AP} = \dfrac{1}{N} \sum_{j=1}^{N} p_{\mathrm{interp}}(j / N) = \dfrac{1}{N} \sum_{j=1}^{T} \max_{k \ge r_j} P_k$;
2. $0 \le \mathrm{AP} \le 1$, and $\mathrm{AP} = 1$ exactly when $T = N$ and no FP is ranked before $r_N$;
3. AP depends on the scores only through the ranking, so any strictly increasing change of all scores leaves it unchanged;
4. the 11-point and 101-point values are the means of $p_{\mathrm{interp}}$ at the recall levels $0, 0.1, \ldots, 1$ and $0, 0.01, \ldots, 1$.

*Proof.* Part 1. Recall changes only at a TP rank, and there it grows by exactly $1/N$: $R_{r_j} - R_{r_j - 1} = 1/N$ and $R_{r_j} = j/N$. All other terms of the sum have $R_k - R_{k-1} = 0$. So $\mathrm{AP} = \frac{1}{N} \sum_{j=1}^{T} p_{\mathrm{interp}}(j/N)$. For $j > T$ no rank has recall $j/N$, so $p_{\mathrm{interp}}(j/N) = 0$, and the sum can run to $N$. Finally, $R_k \ge j/N$ holds exactly when $\mathrm{tp}_k \ge j$, that is, when $k \ge r_j$, so $p_{\mathrm{interp}}(j/N) = \max_{k \ge r_j} P_k$.

Part 2. Each $P_k$ is in $[0, 1]$, so each term of part 1 is in $[0, 1]$, and AP is in $[0, 1]$. If $T = N$ and no FP comes before $r_N$, then $P_{r_N} = N / r_N = 1$, and every $j$ has $r_j \le r_N$, so every term is 1. Conversely, $\mathrm{AP} = 1$ needs all $N$ terms equal to 1, so $T = N$, and the term for $j = N$ needs some $k \ge r_N$ with $P_k = 1$, that is, with no FP among the first $k$ ranks; then no FP comes before $r_N$.

Part 3. The matching of line L4 to L6 visits the detections in the order of line L1 and uses only their boxes, so the TP and FP labels depend only on the order. $P_k$ and $R_k$ depend only on the labels. A strictly increasing change of all scores keeps the order, and the tie rule (the input order) is the same.

Part 4 is the definition of the two sums in the code: each evaluates $p_{\mathrm{interp}}$ at a fixed grid of recall levels and divides by the number of levels. $\square$

**Remark.** Part 1 is the form that the tests use as an independent reference: it needs no sorting of recall values and no envelope, only the precision after each rank. It also shows that a missed object costs exactly $1/N$ of the AP, and that an FP costs something only when it is ranked before a TP.
