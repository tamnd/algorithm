---
title: Dürr-Høyer minimum finding returns a minimum index with probability at least 1/2
proves: [correctness]
status: full
---

We use the pseudocode of the page with $\lambda = 6/5$. The table is $T[0], \ldots, T[N-1]$. Let $v_1 < v_2 < \cdots < v_K$ be its distinct values, let $n_k$ be the number of indices with $T[x] = v_k$, and let $R_k = n_1 + \cdots + n_k$ be the number of indices with $T[x] \le v_k$, so $R_K = N$. While the threshold index is $y$, the marked items are the $x$ with $T[x] < T[y]$; if $T[y] = v_k$, there are $t = R_{k-1}$ of them. A *phase* is the time between two changes of $y$. Let $L = \log_{6/5}\sqrt N + 5$.

**Theorem.** Let $C$ be the number of queries that the run without a budget makes until $T[y] = v_1$. Then

$$\mathbb{E}[C] \le Q(N) = 1 + 18\sqrt N + L\ln N.$$

With a budget $B \ge 2Q(N)$, DURR-HOYER-MINIMUM returns an index of a minimum with probability at least $1/2$. Every run makes fewer than $B + \sqrt N + 2$ queries, and the returned $y$ is a valid index.

**Claim 1 (a phase is a BBHT run).** In each phase, lines L4 to L8 are the rounds of [BBHT search](/bbht-search/) for the marking $f(x) = [T[x] < T[y]]$, from $m = 1$: line L4 is BBHT line L3, line L5 is BBHT lines L4 and L5, the test in line L7 is the classical check, and line L8 is the growth of $m$ with the cap $\sqrt N$. Line L7 resets $m$ to 1 when $y$ changes, so each phase starts a fresh BBHT run with fresh random choices. Each round makes $j$ oracle queries in line L5 and one classical query in line L7, which is what line L6 counts.

**Claim 2 (rounds for many marked items).** If $t > 3N/4$, each round of a phase succeeds with probability at least $1/4$, and the phase has fewer than 5 expected iterations and at most 4 expected rounds.

*Proof.* Let $\sin^2\theta = t/N$. Since $t > 3N/4$, $\theta > \pi/3$. If $t = N$, every $j$ succeeds, because $\sin^2((2j+1)\pi/2) = 1$. Let $t < N$ and $\varphi = \pi - 2\theta \in (0, \pi/3)$. By Claim 2 of the BBHT proof, a round with $c$ choices of $j$ succeeds with probability

$$P_c = \frac{1}{2} - \frac{\sin(4c\theta)}{4c\sin 2\theta} = \frac{1}{2} + \frac{\sin(2c\varphi)}{4c\sin\varphi},$$

because $4c\theta = 2c\pi - 2c\varphi$ and $\sin 2\theta = \sin\varphi$. So $P_c \ge 1/4$ if and only if $-\sin(2c\varphi) \le c\sin\varphi$. If $\sin(2c\varphi) \ge 0$ this is clear. Otherwise $2c\varphi > \pi$, so $c\varphi > \pi/2$. Since $\sin$ is concave on $[0, \pi/3]$, $\sin\varphi \ge \varphi\sin(\pi/3)/(\pi/3) = (3\sqrt3/(2\pi))\varphi$, so $c\sin\varphi > (3\sqrt3/(2\pi))(\pi/2) = 3\sqrt3/4 > 1 \ge -\sin(2c\varphi)$.

So round $r$ of the phase is reached with probability at most $(3/4)^{r-1}$. In round $r$, $m_r \le (6/5)^{r-1}$ and $j$ is uniform on $\{0, \ldots, c_r - 1\}$ with $c_r < m_r + 1$, so $\mathbb{E}[j] < m_r/2$. The expected iterations are less than $\sum_{r \ge 1}(3/4)^{r-1}(6/5)^{r-1}/2 = \frac{1}{2}\cdot\frac{1}{1 - 9/10} = 5$, and the expected rounds are at most $\sum_{r \ge 1}(3/4)^{r-1} = 4$. $\square$

**Claim 3 (the cost of one phase).** A phase with $t \ge 1$ marked items makes, in expectation, fewer than $9\sqrt{N/t}$ iterations and fewer than $L$ rounds.

*Proof.* If $t \le 3N/4$, Claims 3 and 4 of the BBHT proof give fewer than $9m_0$ iterations and fewer than $\log_{6/5}m_0 + 5$ rounds, with $m_0 = 1/\sin 2\theta \le \sqrt{N/t} \le \sqrt N$. If $t > 3N/4$, Claim 2 gives fewer than $5 < 9\sqrt{N/t}$ iterations and at most $4 < L$ rounds. $\square$

**Claim 4 (Lemma 1 of Dürr and Høyer, with ties).** For $k \ge 1$, the probability that some threshold $y$ has $T[y] = v_k$ is at most $n_k/R_k$, with equality in the run without a budget.

*Proof.* Line L7 changes $y$ only to an $x$ with $T[x] < T[y]$, so $T[y]$ never increases. Let $\tau$ be the first moment when $T[y] \le v_k$, if there is one. Then the value $v_k$ is ever a threshold if and only if $\tau$ exists and $T[y_\tau] = v_k$. We show that $y_\tau$ is uniform on the set $S_k = \{x : T[x] \le v_k\}$, which has $R_k$ elements. If $\tau$ is line L1, $y$ is uniform on all indices, so given $y \in S_k$ it is uniform on $S_k$. Otherwise $\tau$ is line L7 with an old threshold $y'$ with $T[y'] > v_k$, so $S_k$ is a subset of the marked set $\{x : T[x] < T[y']\}$. The state $G^j|s\rangle$ of line L5 does not change when two marked items are swapped, because the uniform state, the oracle and the diffusion do not change, so all marked items have the same amplitude. So, given that $x$ is in $S_k$, it is uniform on $S_k$. In both cases $T[y_\tau] = v_k$ with probability $n_k/R_k$. In the run without a budget, every phase with $t \ge 1$ ends with probability 1 by Claim 3, so $\tau$ exists. $\square$

**Claim 5 (two sums).** $\sum_{k=2}^{K}\frac{n_k}{R_k\sqrt{R_{k-1}}} \le 2$ and $\sum_{k=2}^{K}\frac{n_k}{R_k} \le \ln N$.

*Proof.* Let $a = R_{k-1}$ and $b = R_k$, so $n_k = b - a$ and $1 \le a < b \le N$. Then

$$\int_a^b x^{-3/2}\,dx = \frac{2(\sqrt b - \sqrt a)}{\sqrt{ab}} = \frac{2(b - a)}{\sqrt{ab}(\sqrt a + \sqrt b)} \ge \frac{2(b-a)}{\sqrt{ab}\cdot 2\sqrt b} = \frac{b - a}{b\sqrt a}.$$

The intervals $[R_{k-1}, R_k]$ do not overlap, so the first sum is at most $\int_1^\infty x^{-3/2}\,dx = 2$. Also $(b - a)/b = 1 - a/b \le \ln(b/a)$, because $1 - 1/z \le \ln z$ for $z \ge 1$. The second sum is at most $\sum_k\ln(R_k/R_{k-1}) = \ln(N/R_1) \le \ln N$. $\square$

**Proof of the theorem.** Line L1 makes one query to read $T[y]$. After that, $C$ is the sum of the costs of the phases whose threshold value is $v_k$ for some $k \ge 2$; the phase with value $v_1$ starts when $C$ is reached. A phase with threshold value $v_k$ has $t = R_{k-1} \ge 1$ marked items, and by Claim 1 its cost, iterations plus rounds, does not depend on the earlier phases. By Claims 3 and 4 and linearity of expectation,

$$\mathbb{E}[C] \le 1 + \sum_{k=2}^{K}\frac{n_k}{R_k}\left(9\sqrt{\frac{N}{R_{k-1}}} + L\right) \le 1 + 18\sqrt N + L\ln N,$$

where the last step uses Claim 5.

Now take the budget $B \ge 2Q(N)$. The run with the budget and the run without it do the same steps until the budget stops the first. Let the round that sets $T[y] = v_1$ end with $C$ queries in total. That round starts with fewer than $C$ queries made, so it runs if $C \le B$. After it, $y$ never changes. So the run fails only if $C > B$, and by [Markov's inequality](/markov-inequality/)

$$\Pr[C > B] \le \frac{\mathbb{E}[C]}{B} \le \frac{Q(N)}{2Q(N)} = \frac{1}{2}.$$

A round starts only when fewer than $B$ queries have been made, and it makes $j + 1 \le \lceil\sqrt N\rceil$ queries with $j < \sqrt N$, so a run makes fewer than $B + \sqrt N + 2$ queries. Each $y$ is an index from line L1 or a measured index $x$ with $T[x] < T[y]$, which is a valid index. $\blacksquare$
