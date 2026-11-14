---
title: The multilevel bisection is balanced, projection keeps the cut, and no phase after the coarsest level increases the cut
proves: [correctness, termination, monotonicity, running time]
status: full
---

Let $H = (V, N)$ have vertex weights $c(v) \ge 1$ and net weights $w(e) \ge 1$, all integers. A partition is a map $s : V \to \{0, 1\}$, its balance is $c_0(s) = \sum_{s(v) = 0} c(v)$, and its cut is $\mathrm{cut}(s) = \sum \{ w(e) : e \in N, \ s \text{ is not constant on } e \}$. We assume $0 \le lo \le hi \le c(V)$ and $\max_v c(v) \le \mathit{cap} \le hi - lo + 1$, which the implementation checks.

**Lemma 1 (projection).** Let $\pi : V \to V'$ be one coarsening step of HEC or EC, with coarse weights $c'(x) = \sum_{\pi(v) = x} c(v)$ and coarse nets as described on the page. For every partition $s'$ of $V'$, the projection $s = s' \circ \pi$ satisfies $c_0(s) = c'_0(s')$ and $\mathrm{cut}(s) = \mathrm{cut}'(s')$.

*Proof.* The balance: $c_0(s) = \sum_{x : s'(x) = 0} \sum_{\pi(v) = x} c(v) = c'_0(s')$. The cut: a fine net $e$ is cut by $s$ exactly when $s'$ is not constant on $\pi(e)$, because $s(v) = s'(\pi(v))$. If $|\pi(e)| = 1$, the net is not cut and is dropped, so it adds 0 on both sides. Otherwise $\pi(e)$ is a coarse net, and the coarse net $f$ has weight $w'(f) = \sum \{ w(e) : \pi(e) = f \}$. Group the fine nets by their image: $\mathrm{cut}(s) = \sum_f [s' \text{ not constant on } f] \sum_{\pi(e) = f} w(e) = \mathrm{cut}'(s')$. $\square$

By induction on the levels, the same holds for the composed map from $H_0$ to any $H_j$.

**Lemma 2 (weight cap).** Every coarse vertex weighs at most $\mathit{cap}$.

*Proof.* HEC merges the pins of a net only if their total weight is at most $\mathit{cap}$, and EC merges two vertices only if their total weight is at most $\mathit{cap}$. Each coarse vertex is formed by one such merge of vertices of the level below, or is a single vertex of weight at most $\mathit{cap}$ by induction (at level 0 by the assumption $\max_v c(v) \le \mathit{cap}$). $\square$

**Lemma 3 (greedy fill).** On a level with vertex weights at most $\mathit{cap} \le hi - lo + 1$ and total weight $c(V) \ge lo$, GREEDY-FILL returns $s$ with $lo \le c_0(s) \le hi$.

*Proof.* The fill visits the vertices in some order, stops as soon as $c_0 \ge lo$, and adds a vertex $v$ if $c_0 + c(v) \le hi$. While $c_0 < lo$, that is $c_0 \le lo - 1$, every vertex satisfies $c_0 + c(v) \le lo - 1 + hi - lo + 1 = hi$, so every visited vertex is added. Hence $c_0 \le hi$ after each addition. If the loop stops early, $c_0 \ge lo$. If it visits all vertices without stopping, all were added, so $c_0 = c(V) \ge lo$. If $lo = 0$ the loop stops at once with $c_0 = 0$. In each case $lo \le c_0 \le hi$. The total weight is the same on every level by Lemma 1, so $c(V) \ge lo$ holds on every level. $\square$

**Lemma 4 (FM).** If $lo \le c_0(s) \le hi$, then FM$(s)$ returns $s^{*}$ with $lo \le c_0(s^{*}) \le hi$ and $\mathrm{cut}(s^{*}) \le \mathrm{cut}(s)$, and it stops.

*Proof.* In a pass, a vertex is chosen only if its move keeps $c_0$ in $[lo, hi]$, so every tentative partition is balanced. The gain of a free vertex $v$ on side $f$ is $g(v) = \sum \{w(e) : e \ni v, N_f(e) = 1\} - \sum \{w(e) : e \ni v, N_{1-f}(e) = 0\}$, the decrease of the cut if $v$ moves alone. The updates in the implementation are the critical net rules of Fiduccia and Mattheyses with the net weight $w(e)$ in place of 1: the rules for the target side use the counts before the move, and the rules for the source side use the counts after it. The proof on the [Fiduccia-Mattheyses](/fiduccia-mattheyses/) page shows that they keep $g$ equal to this decrease for every free vertex, and the weights only scale each term. So after the first $k$ moves the cut is $\mathrm{cut}(s) - G_k$, where $G_k$ is the sum of the first $k$ gains. The pass keeps the prefix of largest $G_k$, with $G_0 = 0$ allowed, so the cut does not increase and the kept partition is one of the balanced tentative partitions. A new pass starts only if the best $G_k$ was positive, so the integer cut falls by at least 1 per repeated pass, and there are at most $\mathrm{cut}(s) + 1$ passes. $\square$

**Theorem 1 (balance).** The output satisfies $lo \le c_0(s) \le hi$.

*Proof.* At the coarsest level each trial starts from GREEDY-FILL, which is balanced by Lemmas 2 and 3, and FM keeps it balanced by Lemma 4. Line L7 keeps one of these. Each projection in line L9 keeps the balance by Lemma 1, and each FM in line L10 keeps it by Lemma 4. In a V-cycle, the start is the current balanced partition, projected down; by Lemma 1 it is balanced at each level, and the same steps keep it so. $\square$

**Theorem 2 (monotonicity).** Let $s_c$ be the partition chosen at the coarsest level. The cut of the partition after line L10 at level 0 is at most $\mathrm{cut}(s_c)$, and each V-cycle returns a cut at most the cut it started from.

*Proof.* Going up, line L9 keeps the cut (Lemma 1) and line L10 does not increase it (Lemma 4). For a V-cycle, restricted coarsening merges only vertices with the same side, so the current partition $s$ is constant on each preimage $\pi^{-1}(x)$ and defines a coarse partition $s'$ with $s = s' \circ \pi$. By Lemma 1 the cut of $s'$ equals the cut of $s$. FM at the coarsest level and at each level on the way up does not increase the cut, and projection keeps it. $\square$

**Theorem 3 (termination and levels).** The loop of lines L2 to L4 runs at most $n$ times, and every kept level except possibly the last has at most $9/10$ of the vertices of the level before it, so $\ell \le 1 + \log_{10/9}(n / c_0)$ when $c_0 \ge 1$.

*Proof.* Line L3 stops the loop if a step merged nothing, so each kept step lowers the number of vertices by at least 1. Line L4 stops the loop after the first kept level with more than $9/10$ of the vertices of the level before. So all earlier levels shrink by a factor of at least $9/10$, and the loop also stops when at most $c_0$ vertices remain. Every other loop of the algorithm runs over a finite list, and FM stops by Lemma 4. $\blacksquare$

**Running time.** One HEC step sorts the $m_j$ nets in $O(m_j \log m_j)$, checks the pins in $O(P_j)$, and builds the coarse nets by sorting the pin list of each, in $O(P_j \log P_j)$, with $m_j \le P_j \le P$. EC scans, for each vertex, the pins of its nets, which is $O(\sum_e |e|^2)$. One FM pass with gain buckets costs $O(n_j + P_j)$ (see the Fiduccia-Mattheyses page). The implementation uses a scan of all free vertices to pick each move, $O(n_j^2)$ per pass, and scans all pins of the nets of the moved vertex, $O(\sum_e |e|^2)$ per pass, since each vertex moves at most once. By Theorem 3 the number of levels is $O(\log n)$, which gives the bounds on the page. The levels are stored for the way back, so the space is $O(n + \ell P)$, because the vertex counts of the levels add up to at most $10 n$ and each level has at most $P$ pins.

**What is not proved.** Nothing above compares the cut with the minimum. The method can return a cut larger than the minimum, as the measured table on the page shows, and no approximation ratio is known for it.
