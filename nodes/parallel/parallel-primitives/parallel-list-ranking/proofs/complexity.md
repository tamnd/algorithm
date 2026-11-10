---
title: Random mate list ranking ends in O(log n) rounds with high probability, with O(n) expected work and O(log^2 n) span
proves: [termination, time.expected, depth.expected]
status: full
---

We use the lines of RANDOM-MATE-RANK on the page and the notation of the correctness proof: round $r$ is the $r$-th turn of the loop of line L4, $m_r$ is the number of live nodes at its start ($m_1 = n$), $D_r$ is the set of line L6 in round $r$, and $R$ is the number of rounds. Invariant (P) of the correctness proof says that the live nodes form the input lists with the removed nodes left out.

**Lemma 1 (the expected progress).** Let a round start with $m \ge 1$ live nodes, of which $t$ are tails. Then $t \ge 1$, $\mathbb{E}[|D|] = (m + t)/4$, and the expected number of live nodes after the round is at most $(3m - 1)/4$.

*Proof.* The coins of a round are fresh and independent of all earlier steps. A live tail is in $D$ when its coin is heads, with probability $1/2$. A live node with a live successor $j$ is in $D$ when its coin is heads and the coin of $j$ is tails, with probability $1/4$. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[|D|] = t/2 + (m - t)/4 = (m + t)/4$. Since $m \ge 1$, (P) gives at least one live list, and each list has one tail, so $t \ge 1$. Then the expected number left is $m - (m + t)/4 \le (3m - 1)/4$. $\blacksquare$

**Theorem 2 (the number of rounds).** For each $r \ge 0$, $\Pr[R > r] \le (3/4)^r n$. So the loop ends with probability 1, and

$$\mathbb{E}[R] \le \log_{4/3} n + 5, \qquad \Pr\big[R > (k + 1)\log_{4/3} n\big] \le n^{-k} \text{ for each } k > 0.$$

*Proof.* Set $m_{r} = 0$ for the rounds after the last one. Lemma 1 gives $\mathbb{E}[m_{r+1} \mid m_r] \le \tfrac34 m_r$, and this also holds when $m_r = 0$. Taking expectations, $\mathbb{E}[m_{r+1}] \le \tfrac34 \mathbb{E}[m_r]$, so $\mathbb{E}[m_{r+1}] \le (3/4)^r n$. The event $R > r$ is the event $m_{r+1} \ge 1$, so by the [Markov inequality](/markov-inequality/), $\Pr[R > r] \le \mathbb{E}[m_{r+1}] \le (3/4)^r n$. This tends to 0, so the loop ends with probability 1. Then

$$\mathbb{E}[R] = \sum_{r \ge 0} \Pr[R > r] \le \sum_{r \ge 0} \min\{1, (3/4)^r n\}.$$

Let $r_0 = \lceil \log_{4/3} n \rceil$. The terms with $r < r_0$ add up to at most $r_0 \le \log_{4/3} n + 1$. For $r \ge r_0$ we have $(3/4)^{r} n \le (3/4)^{r - r_0}$, and these terms add up to at most $\sum_{j \ge 0} (3/4)^j = 4$. So $\mathbb{E}[R] \le \log_{4/3} n + 5$. With $r = (k + 1)\log_{4/3} n$ the first bound is $n \cdot n^{-(k+1)} = n^{-k}$. $\blacksquare$

**Theorem 3 (work).** Charge a parallel loop over $m$ items with a unit body $m$ units of work, and a pack of $m$ items (a work-efficient prefix sum and a scatter) $2m$ units. Then

$$W = 4n + 6\sum_{r} m_r \qquad\text{and}\qquad \mathbb{E}[W] \le 28n.$$

*Proof.* Lines L1 and L2 cost $n$ each. Round $r$ costs $m_r$ for the coins of line L5, $m_r$ for the test of line L6, $2m_r$ for the pack that forms $D_r$, $|D_r|$ for the splices of line L7, and $2m_r$ for the pack of line L8 (it reads all $m_r$ nodes). Line L10 costs $|D_r|$ for round $r$. Each node is removed in exactly one round, so $\sum_r |D_r| = n$, and $W = 2n + 6\sum_r m_r + 2n$. From the proof of Theorem 2, $\mathbb{E}[\sum_r m_r] = \sum_{r \ge 1} \mathbb{E}[m_r] \le \sum_{r \ge 0} (3/4)^r n = 4n$. So $\mathbb{E}[W] \le 4n + 24n = 28n$. $\blacksquare$

**Theorem 4 (span).** With binary forking, a parallel loop over $m \ge 1$ items with a unit body has span $\lceil \lg m \rceil + 1$, and a pack of $m$ items has span $2\lceil \lg m \rceil + 1$. Then

$$S \le 2(\lceil \lg n \rceil + 1) + R\,(8\lceil \lg n \rceil + 6),$$

so $\mathbb{E}[S] = O(\log^2 n)$, and $S = O(\log^2 n)$ with probability at least $1 - n^{-k}$ for each fixed $k$.

*Proof.* Lines L1 and L2 give the first term. In round $r$, with $m_r \le n$ and $|D_r| \le m_r$, the coins and the test have span at most $\lceil \lg n \rceil + 1$ each, the two packs at most $2\lceil \lg n \rceil + 1$ each, and the splices and the part of line L10 for this round at most $\lceil \lg n \rceil + 1$ each. The sum is $8\lceil \lg n \rceil + 6$. The rounds run one after the other, so their spans add. The bound is linear in $R$, so Theorem 2 gives both claims. $\blacksquare$
