---
title: The KLL sketch is unbiased and its rank error is below εn with probability 1 − δ
proves: [correctness]
status: full
---

We prove the claims for the sketch of lines L1 to L10 with ratio $c \in (1/2, 1)$ and top capacity $k \ge 2$, and for sketches built by merges. The parts up to Theorem 1 are complete. The last section is a sketch of the stronger bounds of the paper and is marked as such.

Fix a query value $x$. Write $R(x)$ for the number of stream items at most $x$ and $\tilde R(x) = \sum_h 2^h |\{y \in B_h : y \le x\}|$ for the estimate of line L9. Let $E = \tilde R(x) - R(x)$.

**Lemma 1 (one compaction).** Let a compaction of line L4 to L8 act on level $h$, with weight $w = 2^h$, and let $D$ be the change in $\tilde R(x)$ that it causes. Let $a$ be the number of compacted items (the sorted buffer without the item set aside) that are at most $x$. If $a$ is even, $D = 0$. If $a$ is odd, $D = +w$ or $D = -w$, each with probability $1/2$ over the bit of line L5. In all cases $\mathbb{E}[D] = 0$ and $|D| \le w$.

*Proof.* The item set aside stays at level $h$ with the same weight, so it does not change $\tilde R(x)$. The compacted items are sorted, so those at most $x$ are the first $a$ of them. Before the compaction they add $wa$ to $\tilde R(x)$. Line L7 keeps the positions $b + 1, b + 3, \ldots$ with weight $2w$. Among the positions $1, \ldots, a$ there are $\lceil a/2 \rceil$ odd ones and $\lfloor a/2 \rfloor$ even ones. So after the compaction these items add $2w\lceil a/2 \rceil$ if $b = 0$ and $2w\lfloor a/2 \rfloor$ if $b = 1$. If $a$ is even, both are $wa$ and $D = 0$. If $a$ is odd, they are $w(a + 1)$ and $w(a - 1)$, so $D = +w$ or $-w$, each with probability $1/2$. $\square$

**Lemma 2 (weight and a fixed schedule).** At all times $\sum_h 2^h|B_h| = n$. The sizes $|B_h|$, the number $H$ of levels, and the levels of the successive compactions are fixed by the sequence of operations (inserts and merges) alone and do not depend on the random bits or on the values.

*Proof.* Line L1 adds weight 1. A compaction of $2s$ items of weight $w$ at level $h$ puts $s$ items of weight $2w$ at level $h + 1$, which keeps the weight. A merge adds the weights of two sketches. For the second claim, the test of line L2, the choice of line L3, the item set aside in line L4, line L6, and the number of items moved in line L7 depend only on the sizes of the buffers and on $H$, and the new sizes depend only on the old ones. By induction on the steps, the whole sequence of sizes is fixed. $\square$

**Lemma 3 (martingale).** Let $D_1, \ldots, D_M$ be the changes of $\tilde R(x)$ caused by the $M$ compactions, in order, and let $h_i$ be the level of the $i$-th one. Then $E = D_1 + \cdots + D_M$, $\mathbb{E}[D_i \mid D_1, \ldots, D_{i-1}] = 0$, and $|D_i| \le 2^{h_i}$, where the $h_i$ and $M$ are fixed numbers.

*Proof.* Before any compaction, every item has weight 1 and is counted once, so $E = 0$. An insert raises $\tilde R(x)$ and $R(x)$ by the same amount, and a merge adds the estimates and the true ranks of two parts. So $E$ changes only at compactions, by $D_i$. The bit of the $i$-th compaction is fair and independent of everything before it, and the buffer it acts on is fixed by the earlier bits and the data. So Lemma 1 applies conditionally on the past. Lemma 2 shows that $M$ and the $h_i$ do not depend on the bits. (For a merge of two sketches, interleave their compactions in any fixed order; their bits are independent.) $\square$

**Lemma 4 (counting).** Let $k_h$ be the capacity of level $h$ at the end, and $m_h$ the number of compactions of level $h$. Then $m_h \le 2n/(k_h 2^h)$. If at least one compaction happened, $2^{H-1} \le 2n/k$.

*Proof.* The weight is conserved and only moves up. So the total weight that ever entered level $h$ is the weight now at the levels $h$ and above, at most $n$, and the compactions of level $h$ remove at most $n$ weight from it. A capacity only shrinks over time, since $H$ only grows, so each compaction of level $h$ ran on at least $k_h$ items and removed at least $k_h - 1 \ge k_h/2$ of them, which is weight at least $(k_h/2)2^h$. So $m_h (k_h/2) 2^h \le n$. For the second claim, level $H - 1$ was created by line L6 during a compaction of level $H - 2$, which was the top level then and had capacity $\lceil k c^0 \rceil = k$. That compaction removed at least $k - 1 \ge k/2$ items of weight $2^{H-2}$, so $(k/2)2^{H-2} \le n$. $\square$

**Theorem 1.** For each fixed $x$, $\mathbb{E}[\tilde R(x)] = R(x)$, and for each $t > 0$,
$$\Pr[|\tilde R(x) - R(x)| \ge t] \le 2\exp\!\Big(-\frac{t^2}{2V}\Big), \qquad V = \sum_h m_h 4^h \le \frac{8c}{2c - 1}\cdot\frac{n^2}{k^2}.$$
For $c = 2/3$, $V \le 16n^2/k^2$, so $\Pr[|\tilde R(x) - R(x)| \ge \varepsilon n] \le 2\exp(-\varepsilon^2 k^2/32)$, and $k \ge \sqrt{32\ln(2/\delta)}/\varepsilon$ makes this at most $\delta$.

*Proof.* By Lemma 3, $E$ is a sum of martingale differences with $\mathbb{E}[E] = 0$, so the estimate is unbiased. The Azuma-Hoeffding inequality for martingale differences bounded by the fixed numbers $2^{h_i}$ gives $\Pr[|E| \ge t] \le 2\exp(-t^2/(2\sum_i 4^{h_i}))$, and $\sum_i 4^{h_i} = \sum_h m_h 4^h = V$. If no compaction happened, $E = 0$. Otherwise, by Lemma 4,
$$V \le \sum_h \frac{2n}{k_h 2^h}4^h = 2n\sum_h \frac{2^h}{k_h} \le \frac{2n}{k}\sum_{h=0}^{H-1} \frac{2^h}{c^{H-1-h}} = \frac{2n}{k}\,2^{H-1}\sum_{d=0}^{H-1}(2c)^{-d},$$
with $d = H - 1 - h$ and $k_h \ge k c^{H-1-h}$. Since $2c > 1$, the sum is less than $2c/(2c - 1)$, and $2^{H-1} \le 2n/k$ by Lemma 4. So $V < (2n/k)(2n/k)(2c/(2c - 1)) = (8c/(2c - 1))\,n^2/k^2$. For $c = 2/3$ the factor is $(16/3)/(1/3) = 16$, and $t = \varepsilon n$ gives $2\exp(-\varepsilon^2 n^2/(32 n^2/k^2))$. $\square$

**Theorem 2 (space).** The sketch stores fewer than $k/(1 - c) + 2H$ items, and $H \le \log_2(n/k) + 2$. For $c = 2/3$ this is $3k + 2\log_2(n/k) + 4$.

*Proof.* After line L2 ends, every level has $|B_h| < k_h \le k c^{H-1-h} + 2$. Summing the geometric series gives the first claim, and Lemma 4 gives the bound on $H$. $\square$

With $k = \lceil\sqrt{32\ln(2/\delta)}/\varepsilon\rceil$, Theorems 1 and 2 give $O((1/\varepsilon)\sqrt{\log(1/\delta)} + \log(n/k))$ items for error $\varepsilon n$ with probability $1 - \delta$ on each query. This is Theorem 1 of Karnin, Lang and Liberty, with explicit constants for this form.

**Sketch of the stronger bounds (not proved here).** The proof of Theorem 1 shows that level $h$ adds about $2n \cdot 2^h/k_h$ to $V$, so the top few levels carry almost all of the variance. Karnin, Lang and Liberty give the top $s = O(\log\log(1/\delta))$ levels the same capacity $k$ (their Theorem 4). Then the levels below the top $s$ contribute a variance that is smaller by a factor about $2^{-2s}$, so the Azuma bound for them is about $2\exp(-\varepsilon^2 k^2 2^{2s}/C)$, which is at most $\delta$ already for $k = O(1/\varepsilon)$ when $2^{2s} \approx \log(1/\delta)$. The top $s$ levels make only $O(1)$ compactions each with this many items, and their error is bounded without probability by $O(s \cdot n/k)$, so $k = O(s/\varepsilon)$ makes it at most $\varepsilon n/2$. The space is $s$ levels of $O(s/\varepsilon)$ items, $O((1/\varepsilon)\log^2\log(1/\delta))$. Their Theorem 5 replaces the top $s$ levels with a [GK summary](/greenwald-khanna-summary/) of the items that reach them, whose deterministic error costs only $O((1/\varepsilon)\log(\varepsilon n'))$ items for the $n' = O(k 2^{2s})$ items it sees, which gives $O((1/\varepsilon)\log\log(1/\delta))$. $\blacksquare$
