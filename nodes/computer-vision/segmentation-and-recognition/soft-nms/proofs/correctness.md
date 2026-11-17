---
title: Soft-NMS terminates, outputs nonincreasing scores with a closed form, and its hard rule is greedy NMS
proves: [correctness]
status: full
---

We use the notation of the page. The input is $n$ boxes $B_1, \ldots, B_n$ with scores $s_1, \ldots, s_n \ge 0$, a decay function $f$ with $0 \le f(o) \le 1$ for every overlap $o$, and a pruning threshold $s_{\min} \ge 0$. The linear rule, $f(o) = 1$ for $o < N_t$ and $1 - o$ otherwise, and the Gaussian rule $f(o) = e^{-o^2/\sigma}$ both take values in $[0, 1]$ because $o = \mathrm{IoU} \in [0, 1]$. The loop keeps a current score $S_i$ for each index and a set $R$ of remaining indices. Let $m_1, m_2, \ldots, m_r$ be the indices that line L3 selects, in order.

**Claim.**

1. (termination) The loop runs at most $n$ times, and each index is output at most once.
2. (closed form) The score output with $m_k$ is $s_{m_k} \prod_{j < k} f(o(B_{m_j}, B_{m_k}))$.
3. (order) The output scores are nonincreasing: $S_{m_1} \ge S_{m_2} \ge \cdots \ge S_{m_r}$.
4. (no loss with the Gaussian rule) If $s_{\min} = 0$, every index is output.
5. (hard rule) If $f(o) = 1$ for $o < N_t$ and $f(o) = 0$ otherwise, and $0 < s_{\min} \le \min_i s_i$, the selected indices are exactly the output of greedy NMS that removes a box when its overlap with a kept box is at least $N_t$, in the same order.

**Invariant.** At the start of each iteration of line L2, after $k$ selections, every $i \in R$ has $S_i = s_i \prod_{j \le k} f(o(B_{m_j}, B_i))$, and $i \notin \{m_1, \ldots, m_k\}$.

*Proof.* Before the first iteration, line L1 sets $S = s$ and $R$ to all indices, and the product is empty. In iteration $k + 1$, lines L3 and L4 take $m_{k+1}$ out of $R$. Lines L5 to L7 multiply $S_i$ by $f(o(B_{m_{k+1}}, B_i))$ for every other $i \in R$, which extends the product by one factor. Line L8 only removes indices from $R$. No line changes the score of an index outside $R$, and no line puts an index back into $R$. $\square$

*Proof of the claim.* Part 1: each iteration removes $m_k$ from $R$ in line L4 and nothing is added to $R$, so $|R|$ falls by at least one in each iteration, and the loop of line L2 stops after at most $n$ iterations. An index leaves $R$ when it is output, so it is output at most once.

Part 2 is the invariant at the moment line L4 outputs $m_k$, before the iteration changes any score.

Part 3: when $m_k$ is selected, line L3 gives $S_{m_k} \ge S_i$ for every $i$ in $R$. In the same iteration, line L7 multiplies each $S_i$ by a factor in $[0, 1]$, and the scores are nonnegative, so they do not increase. The next selected index $m_{k+1}$ is in $R$ at that time, so $S_{m_{k+1}} \le S_{m_k}$.

Part 4: with $s_{\min} = 0$ the test of line L8 never removes an index, because every score is nonnegative. Each iteration then removes exactly one index from $R$, so all $n$ indices are output.

Part 5: with the hard rule, a factor is 1 or 0. If an index $i$ gets a factor 0, its score becomes 0, which is below $s_{\min}$, and line L8 removes it at once. If it gets only factors 1, its score stays $s_i \ge s_{\min}$, and it stays in $R$. So the indices in $R$ always have their input scores, and line L3 selects them in the rank order of the input scores with ties by the smaller index. An index $i$ leaves $R$ without being output exactly when some selected $m$ before it has $o(B_m, B_i) \ge N_t$. These are the two properties that characterize greedy NMS with the test "at least $N_t$": no selected index has an earlier selected index that overlaps it that much, and every other index has one. The argument in the correctness file of [box non-maximum suppression](/box-non-maximum-suppression/) shows that only one set has both properties, with the comparison "greater than" there; replacing it with "at least" changes nothing in that argument. So the two outputs are the same set, and both are in rank order. $\square$

**Remark (the floating-point case).** Part 2 is an equality of real numbers. In floating point the code multiplies the factors in the order of selection, and the reference implementation in the tests does the same, so the two agree to the last bit; a program that multiplies in another order can differ in the last bits and can then break a tie in the other direction.

**Cost.** Iteration $k$ scans $R$ twice, once in line L3 and once in lines L5 to L8, with $|R| \le n - k + 1$. The total is $O(n^2)$ overlaps and decays. With $s_{\min} = 0$, part 4 gives $|R| = n - k + 1$ exactly, and lines L5 to L8 evaluate $\sum_{k=1}^{n} (n - k) = n(n-1)/2$ overlaps, so the bound is tight. The extra space is the copy of the scores and the set $R$, $\Theta(n)$.
