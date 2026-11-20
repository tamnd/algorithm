---
title: The Even-Paz algorithm is proportional and uses at most 2n ceil(lg n) - n queries
proves: [correctness]
status: full
---

**Setting.** The cake is $[0, 1]$, and agent $i \in \{1, \dots, n\}$ has a nonnegative, additive and nonatomic valuation $V_i$ with $V_i([0, 1]) = 1$. For $a \in [0, 1]$, the map $t \mapsto V_i([a, t])$ is continuous and nondecreasing on $[a, 1]$, since $V_i$ is nonatomic. So $\mathrm{Cut}_i(a, t)$ has an answer whenever $0 \le t \le V_i([a, 1])$, and the least answer $m$ has $V_i([a, m]) = t$. Single points have value 0. We refer to the lines L1 to L9 of the page, and we write $L = \lceil \lg n \rceil$.

**Lemma 1 (the cut queries have answers).** In a call on $S$ and $[a, b]$, the query of line L5 asks for $w_i k_1/k \le w_i = V_i([a, b])$, and its answer $m_i$ lies in $[a, b]$.

*Proof.* $k_1/k \le 1$, so the asked value is at most $V_i([a, b]) \le V_i([a, 1])$, and an answer exists. The least answer is at most $b$, because $V_i([a, b]) \ge w_i k_1/k$. $\square$

So the cut point $x$ of line L7 lies in $[a, b]$, and the calls of lines L8 and L9 are on intervals inside $[a, b]$ that meet only at $x$.

**Lemma 2 (the split).** After the sort of line L6, every agent $i \in L$ has $m_i \le x$ and every agent $i \in R$ has $m_i \ge x$, and $|L| = k_1 \ge 1$, $|R| = k - k_1 \ge 1$.

*Proof.* The sort is by $m_i$ first, and $x$ is the mark of the $k_1$-th agent in sorted order. For $k \ge 2$, $k_1 = \lfloor k/2 \rfloor \ge 1$ and $k - k_1 = \lceil k/2 \rceil \ge 1$. $\square$

**Theorem 1 (each agent gets its share of the interval).** A call on a set $S$ of $k \ge 1$ agents and an interval $[a, b]$ gives the agents of $S$ disjoint intervals that cover $[a, b]$, and agent $i \in S$ gets an interval worth at least $V_i([a, b])/k$ to it.

*Proof.* By strong induction on $k$. For $k = 1$, line L1 gives all of $[a, b]$ to the one agent, worth $V_i([a, b])$.

Let $k \ge 2$ and $w = V_i([a, b])$ for an agent $i \in S$. By Lemma 2 the two recursive calls have fewer than $k$ agents, so the induction hypothesis applies to them, and together they cover $[a, x] \cup [x, b] = [a, b]$.

If $i \in L$, then $m_i \le x$, and monotonicity gives $V_i([a, x]) \ge V_i([a, m_i]) = w k_1/k$. The call on $L$ gives agent $i$ at least
$$\frac{V_i([a, x])}{k_1} \ge \frac{w k_1 / k}{k_1} = \frac{w}{k}.$$

If $i \in R$, then $m_i \ge x$, so $V_i([a, x]) \le V_i([a, m_i]) = w k_1/k$, and additivity gives $V_i([x, b]) = w - V_i([a, x]) \ge w (k - k_1)/k$. The call on $R$ gives agent $i$ at least
$$\frac{V_i([x, b])}{k - k_1} \ge \frac{w (k - k_1)/k}{k - k_1} = \frac{w}{k}. \qquad \square$$

**Corollary (proportional).** The first call has $S = \{1, \dots, n\}$, $[a, b] = [0, 1]$ and $V_i([0, 1]) = 1$, so each agent gets one interval worth at least $1/n$, and the intervals partition $[0, 1]$. The root uses $w_i = 1$ without a query; this is correct because the valuations are normalized.

**Remark (safe for an honest agent).** The proof for agent $i$ uses only the answers of agent $i$ and the fact that $x$ is chosen so that agent $i$ lands on the side of $x$ that its own mark selects. It uses nothing about the answers of other agents, except that their marks lie in $[a, b]$. So an agent that answers by $V_i$ gets at least $1/n$ whatever the others answer.

**Lemma 3 (the shape of the recursion).** For $n \ge 2$, the tree of calls has $n$ leaves, every internal call has two children, and every leaf has depth $L - 1$ or $L$. Exactly $2n - 2^L$ leaves have depth $L$, and $2^L - n$ leaves have depth $L - 1$.

*Proof.* The sizes of the calls at depth $d$ are $\lfloor n/2^d \rfloor$ or $\lceil n/2^d \rceil$, by induction on $d$: halving $\lfloor m \rfloor$ or $\lceil m \rceil$ into floor and ceiling parts gives $\lfloor m/2 \rfloor$ or $\lceil m/2 \rceil$. Since $2^{L-1} < n \le 2^L$, every call at depth $d \le L - 2$ has size at least $\lfloor n/2^{L-2} \rfloor \ge 2$, so it is internal. Hence depth $L - 1$ has $2^{L-1}$ calls, each of size $\lceil n/2^{L-1} \rceil \le 2$ or $\lfloor n/2^{L-1} \rfloor \ge 1$, so of size 1 or 2. Let $c$ be the number of size 1. Then $c + 2(2^{L-1} - c) = n$, so $c = 2^L - n$ leaves have depth $L - 1$, and the $2^{L-1} - c$ calls of size 2 have $2(2^{L-1} - c) = 2n - 2^L$ children of size 1 at depth $L$. $\square$

**Theorem 2 (query count).** For $n \ge 2$, the protocol makes $nL - 2^L + n \le nL$ cut queries and $nL - 2^L$ eval queries, so
$$2nL - 2^{L+1} + n \le 2nL - n$$
queries in total, with equality when $n$ is a power of 2. For $n = 1$ it makes no query.

*Proof.* A call on $k \ge 2$ agents asks each of its agents one cut query, and one eval query unless it is the root. So agent $i$ gets one cut query for each internal call on the path from the root to its leaf, that is, as many cut queries as the depth of its leaf, and one eval fewer. By Lemma 3 the sum of the depths is
$$L(2n - 2^L) + (L - 1)(2^L - n) = nL - 2^L + n.$$
This is the count of cut queries. It is at most $nL$ because $n \le 2^L$. The eval queries number $n$ fewer, $nL - 2^L$. The total is $2nL - 2^{L+1} + n$, and $2^{L+1} \ge 2n$ gives the bound $2nL - n$, with equality exactly when $n = 2^L$. For $n = 1$, line L1 returns at once. $\blacksquare$
