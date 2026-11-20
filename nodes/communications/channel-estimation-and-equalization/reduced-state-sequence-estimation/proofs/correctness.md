---
title: RSSE is a well-defined trellis search, exact ML with full partitions, the DFE with none, and error-free without noise for every partition
proves: [correctness]
status: full
---

The channel taps are $f_0, \ldots, f_{L-1}$ with $f_0 \ne 0$, the alphabet $\mathcal{A}$ has $M$ points, and the known symbols before the block are $x_{-1}, \ldots, x_{-L+1}$. The samples are $y_k = \sum_l f_l x_{k-l} + n_k$ for $k = 0, \ldots, N-1$. For a sequence $x$ write $J_k(x) = \sum_{j \le k} |y_j - \sum_l f_l x_{j-l}|^2$.

There are $K \le L-1$ partitions $\Omega(1), \ldots, \Omega(K)$ of $\mathcal{A}$, and $\ell_i(a)$ is the label of the subset of $\Omega(i)$ that holds $a$. They are nested: $\ell_i(a) = \ell_i(b)$ implies $\ell_{i+1}(a) = \ell_{i+1}(b)$ (the function `check_partitions` tests this). The state of a sequence at time $k$ is $t_k = (\ell_1(x_{k-1}), \ldots, \ell_K(x_{k-K}))$.

**Lemma 1 (the trellis is well defined).** $t_{k+1}$ is a function of $t_k$ and $\ell_1(x_k)$. So the number of states is $J_1 J_2 \cdots J_K$, and the symbols with the same $\ell_1$ are parallel branches between the same pair of states.

*Proof.* $t_{k+1} = (\ell_1(x_k), \ell_2(x_{k-1}), \ldots, \ell_K(x_{k-K+1}))$. For $i \ge 2$, $\ell_i(x_{k-i+1})$ is a function of $\ell_{i-1}(x_{k-i+1})$ by the nesting, and $\ell_{i-1}(x_{k-i+1})$ is entry $i-1$ of $t_k$. $\square$

The code computes $t_{k+1}$ from the survivor's own symbols (line L6), which gives the same value by Lemma 1.

**Lemma 2 (survivor metrics).** After step $k$, each survivor is a sequence $(x_0, \ldots, x_k)$, with the known symbols before it, and its stored metric equals $J_k$ of that sequence. Its stored history holds its own last $L-1$ symbols.

*Proof.* By induction. At the start there is one survivor with metric 0 and the known history (line L1). A step extends a survivor by a symbol $a$ and adds $|y_k - f_0 a - \sum_{l \ge 1} f_l x_{k-l}|^2$, where $x_{k-l}$ come from the survivor's own history (lines L3 to L5). This is the term $j = k$ of $J_k$ for the extended sequence. The new history is $a$ followed by the old one, cut to $L - 1$ symbols, and line L7 stores it with the metric. $\square$

So the output is the sequence with the smallest $J_{N-1}$ among the final survivors (line L8). RSSE is suboptimal only because the compare step at line L7 drops a path when another path with a smaller metric enters the same reduced state. Two such paths can differ in symbols that the state does not hold, so their future branch metrics differ, and the dropped one can be the better full path.

**Theorem 1 (full partitions give ML).** If $K = L - 1$ and every $\Omega(i)$ is the partition into single points, RSSE returns a sequence that minimizes $J_{N-1}$ over $\mathcal{A}^N$.

*Proof.* The state is then $(x_{k-1}, \ldots, x_{k-L+1})$, the full channel memory, with $M^{L-1}$ states. The history that a survivor uses at line L3 is fixed by its state, so two paths into the same state have the same future branch metrics, and the compare step keeps a path that can be extended to an optimal one. This is the Viterbi equalizer, and its proof applies. $\square$

**Theorem 2 (no partition gives the DFE).** If $K = 0$, there is one state and one survivor, and RSSE decides $\hat x_k = \arg\min_{a \in \mathcal{A}} |y_k - \sum_{l \ge 1} f_l \hat x_{k-l} - f_0 a|$. This is the zero-forcing DFE on $f$: subtract the ISI of the past decisions and take the nearest point to $(y_k - \sum_{l \ge 1} f_l \hat x_{k-l})/f_0$.

*Proof.* With $K = 0$ the state tuple is empty, so all branches enter the same state, and line L7 keeps the branch with the smallest metric. All candidates share the same survivor metric, so the smallest metric is the smallest branch metric. And $|v - f_0 a| = |f_0| \cdot |v/f_0 - a|$, so this is the nearest point to $v/f_0$. $\square$

**Theorem 3 (no noise, no errors).** If $n = 0$, RSSE returns the transmitted sequence for every choice of nested partitions.

*Proof.* First, a sequence $x'$ with $J_k(x') = 0$ equals the transmitted $x$ up to time $k$. Indeed, $J_k(x') = 0$ gives $f_0 x'_j = y_j - \sum_{l \ge 1} f_l x'_{j-l}$ for every $j \le k$, and $f_0 \ne 0$, so $x'_0 = x_0$ from the known past, and then $x'_1 = x_1$, and so on. Now show by induction that after step $k$ the true state $t_k(x)$ has a survivor equal to $x$ up to time $k$, with metric 0. Before the loop this holds. If it holds after step $k - 1$, the extension of that survivor by $x_k$ enters $t_{k+1}(x)$ with metric 0 by Lemma 2. Every candidate has metric at least 0, and a candidate with metric 0 is the true sequence by the first part, so the survivor kept in $t_{k+1}(x)$ is the true sequence. At the end, the best final survivor has metric 0 and is the true sequence. $\square$

**Theorem 4 (the cost).** Each step costs $O(S(M + L))$ for $S = J_1 \cdots J_K$ states: the ISI of the survivor history in $O(L)$, then $M$ branch metrics in $O(1)$ each. The traceback pointers need $O(N S)$ space. Against the $M^{L-1}$ states of the Viterbi equalizer, the saving is the factor $M^{L-1}/S$. For DDFSE with memory $\mu$, $S = M^\mu$, a factor of $M^{L-1-\mu}$.

*Proof.* Count the operations in lines L2 to L7. $\square$
