---
title: Cole-Vishkin 3-colours an oriented ring in exactly T(N) + 3 rounds, and T(N) is at most log* N
proves: [correctness, termination, complexity]
status: full
---

**Setting.** The ring has nodes $v_0, \dots, v_{n-1}$ with $n \ge 3$ and successor $s(v_j) = v_{(j+1) \bmod n}$. The identifiers are distinct integers in $[0, N)$ with $N \ge 1$. Let $c_t$ be the colouring after $t$ runs of the loop of line L2, and $b_t$ the value of $b$ then, so $c_0 = \mathrm{id}$, $b_0 = N$ and $b_{t+1} = 2 \lceil \lg b_t \rceil$. For $c \ne d$, $f(c, d) = 2i + \operatorname{bit}_i(c)$ where $i$ is the least index with $\operatorname{bit}_i(c) \ne \operatorname{bit}_i(d)$.

**Lemma 1 (one step).** Let $c, d, e$ be integers in $[0, b)$ with $b \ge 2$, $c \ne d$ and $d \ne e$. Then $f(c, d) \ne f(d, e)$ and $f(c, d) < 2 \lceil \lg b \rceil$.

*Proof.* Let $i$ be the least index where $c$ and $d$ differ, and $i'$ the least index where $d$ and $e$ differ. If $i \ne i'$, then $f(c, d) \in \{2i, 2i + 1\}$ and $f(d, e) \in \{2i', 2i' + 1\}$, and these two sets are disjoint. If $i = i'$, then $f(c, d) - f(d, e) = \operatorname{bit}_i(c) - \operatorname{bit}_i(d) \ne 0$, by the choice of $i$. For the range, let $L = \lceil \lg b \rceil$. Then $c, d < b \le 2^L$, so all bits of index $L$ or more are 0 in both, and $i \le L - 1$. So $f(c, d) \le 2(L - 1) + 1 = 2L - 1$. $\square$

**Lemma 2 (invariant of the loop).** For every $t \le T(N)$, $c_t$ is a proper colouring of the ring and all its values lie in $[0, b_t)$.

*Proof.* For $t = 0$ the identifiers are distinct and lie in $[0, N)$. Assume the claim for $t < T(N)$; then $b_t \ge 7$. Node $v$ computes $c_{t+1}(v) = f(c_t(v), c_t(s(v)))$, which is defined since $c_t(v) \ne c_t(s(v))$. For the edge $\{v, s(v)\}$, apply Lemma 1 with $c = c_t(v)$, $d = c_t(s(v))$, $e = c_t(s(s(v)))$; the condition $d \ne e$ holds because $c_t$ is proper. So $c_{t+1}(v) \ne c_{t+1}(s(v))$, and every edge of the ring has this form. Lemma 1 also gives $c_{t+1}(v) < 2 \lceil \lg b_t \rceil = b_{t+1}$. $\square$

**Lemma 3 (the loop stops with at most 6 colours).** The loop runs a finite number $T(N)$ of times, and $b_{T(N)} \le 6$. If $N \ge 7$ then $b_{T(N)} = 6$.

*Proof.* For $b \ge 7$ we have $2 \lceil \lg b \rceil < b$: this holds for $7 \le b \le 8$ (value 6), and for $b \ge 9$ the function $2\lceil \lg b \rceil \le 2 \lg b + 2$ is less than $b$. So $b_t$ decreases by at least 1 while $b_t \ge 7$, and the loop stops. When it stops, $b \le 6$. If $N \ge 7$, the last step starts from some $b \ge 7$, which has $\lceil \lg b \rceil \ge 3$, so the last value is at least 6. $\square$

**Lemma 4 (the final rounds).** After the three rounds of lines L7 and L8, the colouring is proper and uses only $\{0, 1, 2\}$.

*Proof.* By Lemmas 2 and 3 the colouring before line L7 is proper with values in $[0, 6)$. Consider the round for the class $x$, and assume the colouring before it is proper with values in $\{0, 1, 2\} \cup \{y : 3 \le y \le x\}$. The nodes of colour $x$ are pairwise non-adjacent, so in this round no two neighbours both change. A node $v$ of colour $x$ has two neighbours, which use at most two colours, so a colour of $\{0, 1, 2\}$ is free, and $v$ takes a colour different from the colours that its neighbours have in this round. Every other node keeps its colour. So the colouring stays proper, and the colour $x$ disappears. After $x = 5, 4, 3$, only $\{0, 1, 2\}$ remain. $\square$

**Theorem 1 (correctness and exact round count).** The algorithm returns a proper 3-colouring of the ring after exactly $T(N) + 3$ rounds.

*Proof.* Each run of the loop is one round (line L3), and each value of $x$ in line L7 is one round, since a node needs the current colours of its neighbours. Lemmas 2, 3 and 4 give the output. $\square$

**Theorem 2 ($T(N) \le \log^* N$).** Let $\operatorname{tower}(0) = 1$, $\operatorname{tower}(k + 1) = 2^{\operatorname{tower}(k)}$, and $\log^* N = \min\{k \ge 0 : N \le \operatorname{tower}(k)\}$. Then $T(N) \le \log^* N$ for every $N \ge 1$.

*Proof.* If $N \le 6$, then $T(N) = 0$. Assume $N \ge 7$ and let $K = \log^* N$; since $\operatorname{tower}(2) = 4 < N$, we have $K \ge 3$. Let $L_t = \lceil \lg b_t \rceil$. Then $b_{t+1} = 2 L_t$, so $L_{t+1} = \lceil \lg (2 L_t) \rceil = 1 + \lceil \lg L_t \rceil$.

*Claim.* If $k \ge 1$ and $L \le \operatorname{tower}(k) + 2$, then $1 + \lceil \lg L \rceil \le \operatorname{tower}(k - 1) + 2$. Indeed, let $a = \operatorname{tower}(k - 1) \ge 1$. Then $L \le 2^a + 2 \le 2^a + 2^a = 2^{a + 1}$, because $2^a \ge 2$. So $\lceil \lg L \rceil \le a + 1$, which gives the claim.

Since $N \le \operatorname{tower}(K) = 2^{\operatorname{tower}(K - 1)}$, we get $L_0 = \lceil \lg N \rceil \le \operatorname{tower}(K - 1) \le \operatorname{tower}(K - 1) + 2$. Apply the claim $s$ times, for $s \le K - 1$: as long as $b$ stays above 6, $L_s \le \operatorname{tower}(K - 1 - s) + 2$. In particular $L_{K - 1} \le \operatorname{tower}(0) + 2 = 3$ if the loop runs that long, and then $b_K = 2 L_{K-1} \le 6$. So the loop stops after at most $K$ runs. If it stops earlier, the bound holds as well. $\square$

**Corollary.** The algorithm uses at most $\log^* N + 3$ rounds. With $N = n^{O(1)}$ this is $\log^* n + O(1)$. $\blacksquare$
