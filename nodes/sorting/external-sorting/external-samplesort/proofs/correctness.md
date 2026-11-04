---
title: External samplesort sorts stably, and its buckets are small with high probability
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode. For a file $G$, write $\operatorname{st}(G)$ for its stable sort.

## Correctness

**Lemma 1 (buckets).** Let $s_1 < \cdots < s_k$ be the splitters of line L4, with $k \ge 1$, and let $U_0, E_1, U_1, \ldots, E_k, U_k$ be the buckets of line L5, each in the order of $G$. Then

$$\operatorname{st}(G) = \operatorname{st}(U_0)\, E_1\, \operatorname{st}(U_1)\, E_2 \cdots E_k\, \operatorname{st}(U_k).$$

*Proof.* Each item goes to exactly one bucket: either it equals some $s_j$, or it lies strictly between two consecutive splitters, with $s_0 = -\infty$ and $s_{k+1} = +\infty$. Every item of $U_{j-1}$ is less than $s_j$, every item of $E_j$ equals $s_j$, and every item of $U_j$ is greater than $s_j$. So in $\operatorname{st}(G)$ the items appear grouped in the order $U_0, E_1, U_1, \ldots, U_k$. Inside a group, $\operatorname{st}(G)$ keeps the items of equal keys in the order of $G$, and sorts the others; for $U_j$ this is $\operatorname{st}(U_j)$, and for $E_j$, whose keys are all equal, it is $E_j$ itself in the order of $G$. $\blacksquare$

**Lemma 2 (progress).** If $|G| > M$, each bucket $U_j$ has fewer than $|G|$ items.

*Proof.* The sample is not empty, because $aS \ge 1$, and $(S - 1)a \ge a$ is a rank of the sample, so $k \ge 1$. The splitter $s_1$ is an item of $G$, and it is in $E_1$, not in any $U_j$. $\blacksquare$

**Theorem.** EXTERNAL-SAMPLESORT returns $\operatorname{st}(F)$.

*Proof.* By strong induction on $N$. If $N \le M$, line L1 returns the stable sort of $F$. Else, by Lemma 2, each recursive call of line L7 is on a smaller file, so by induction it returns $\operatorname{st}(U_j)$. Line L8 writes the buckets in the order of Lemma 1, which is $\operatorname{st}(F)$. $\blacksquare$

## The size of the buckets

**Lemma 3.** Let $S \ge 2$ and $a \ge 8 \ln S$, let the sample be $aS$ positions of $G$ drawn uniformly and independently, and let $N = |G|$ and $L = \lceil 2N/S \rceil$. Then, with probability at least $1 - 1/(2S)$, each bucket $U_j$ has at most $2L - 2$ items, that is, fewer than $4N/S + 2$.

*Proof.* Order the items of $G$ by key, and by position for equal keys, and number them $0, \ldots, N - 1$ in this order. Each $U_j$ is a set of consecutive numbers, because it is the set of items with keys in an open interval.

*Few sample items in a bucket.* The chosen ranks of line L4 are $a, 2a, \ldots, (S - 1)a$ in the sorted sample of $aS$ items. For $1 \le j < k$, let $r$ be the largest chosen rank with the value $s_j$. The next chosen rank, $r + a$, has a value that is greater than $s_j$ and is a splitter, so it is $s_{j+1}$. A sample item in $U_j$ has a value strictly between $s_j$ and $s_{j+1}$, so its rank is strictly between $r$ and $r + a$: at most $a - 1$ ranks. In the same way, a sample item in $U_0$ has a rank below the first chosen rank $a$, and one in $U_k$ has a rank above the largest chosen rank with the value $s_k$, which is $(S - 1)a$. So each $U_j$ holds at most $a$ sample items.

*A chunk with few sample items.* Cut the numbers into the chunks $C_c = \{cL, \ldots, cL + L - 1\}$ for $c = 0, 1, \ldots$, and call a chunk *full* if it lies inside $\{0, \ldots, N - 1\}$. There are at most $N/L \le S/2$ full chunks. A set of at least $2L - 1$ consecutive numbers contains a full chunk: the first multiple of $L$ in it is at most $L - 1$ after its start, and the chunk that begins there ends at most $2L - 2$ after its start. So if some $U_j$ has $2L - 1$ or more items, some full chunk holds at most $a$ sample items.

*The probability.* For a fixed full chunk, the number $X$ of sample positions in it is binomial with $aS$ trials and success probability $L/N \ge 2/S$, so $\mu = \mathbb{E}[X] \ge 2a$. By the Chernoff bound $\Pr[X \le (1 - \delta)\mu] \le e^{-\delta^2 \mu / 2}$ with $\delta = 1/2$,

$$\Pr[X \le a] \le \Pr[X \le \mu/2] \le e^{-\mu/8} \le e^{-a/4} \le S^{-2}.$$

A union bound over at most $S/2$ full chunks gives a probability of at most $1/(2S)$ that some full chunk holds at most $a$ sample positions. $\blacksquare$

**Corollary.** If $S \ge 4N/M$, then with probability at least $1 - 1/(2S)$ every bucket $U_j$ fits in memory, so each recursive call of line L7 stops at line L1.

*Proof.* $2N/S \le M/2$, so $L \le \lceil M/2 \rceil$ and $2L - 2 \le M$. $\blacksquare$
