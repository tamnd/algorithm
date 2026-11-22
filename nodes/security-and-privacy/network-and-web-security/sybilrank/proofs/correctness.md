---
title: Correctness of SybilRank
proves: [correctness]
status: full
---

Let $G = (V, E)$ be an undirected graph with $n$ nodes and $m$ edges, every node of degree at least 1. Let $S$ be a nonempty set of seeds and $T_G > 0$. Write $T^{(i)}$ for the vector $T$ after line L5 of the algorithm has run $i$ times, and $T^{(0)}$ for the vector set by line L1. Let $P$ be the transition matrix of the simple random walk on $G$: $P(u, v) = 1 / \deg(u)$ if $\{u, v\} \in E$, and $0$ otherwise.

**Lemma 1 (one step).** For $i \ge 1$ and every node $v$,

$$
T^{(i)}(v) = \sum_{u : \{u, v\} \in E} \frac{T^{(i-1)}(u)}{\deg(u)} = \sum_{u \in V} T^{(i-1)}(u) P(u, v) .
$$

*Proof.* Line L3 sets $T'(v) = 0$. Line L4 visits each node $u$ once and, for each neighbor $v$ of $u$, adds $T^{(i-1)}(u) / \deg(u)$ to $T'(v)$. So $T'(v)$ receives exactly one term for each neighbor $u$ of $v$. Line L5 sets $T^{(i)} = T'$. The second form follows from the definition of $P$. $\square$

**Lemma 2 (conservation).** $\sum_v T^{(i)}(v) = T_G$ for every $i \ge 0$.

*Proof.* For $i = 0$, line L1 puts $T_G / |S|$ on each of the $|S|$ seeds. For $i \ge 1$, by Lemma 1,

$$
\sum_v T^{(i)}(v) = \sum_u T^{(i-1)}(u) \sum_v P(u, v) = \sum_u T^{(i-1)}(u) ,
$$

since each row of $P$ sums to 1, because $u$ has $\deg(u) \ge 1$ neighbors and gives $1 / \deg(u)$ to each. Induction on $i$ completes the proof. $\square$

**Theorem 1 (what is computed).** Let $X_0$ be uniform on $S$ and let $X_0, X_1, \ldots$ be the simple random walk on $G$. Then $T^{(i)}(v) = T_G \Pr[X_i = v]$ for every $i \ge 0$ and every $v$.

*Proof.* By induction on $i$. For $i = 0$, $\Pr[X_0 = v] = 1 / |S|$ for $v \in S$ and $0$ otherwise, which matches line L1 after multiplication by $T_G$. For $i \ge 1$, by the Markov property, $\Pr[X_i = v] = \sum_u \Pr[X_{i-1} = u] P(u, v)$. By the induction hypothesis and Lemma 1, $T^{(i)}(v) = \sum_u T_G \Pr[X_{i-1} = u] P(u, v) = T_G \Pr[X_i = v]$. $\square$

**Corollary (limit, cited fact).** If $G$ is connected and not bipartite, the walk is irreducible and aperiodic, and its unique [stationary distribution](/stationary-distribution/) is $\pi(v) = \deg(v) / (2m)$, since $\sum_u \pi(u) P(u, v) = \sum_{u \sim v} \frac{\deg(u)}{2m} \cdot \frac{1}{\deg(u)} = \frac{\deg(v)}{2m}$. By the convergence theorem for finite irreducible aperiodic Markov chains, $\Pr[X_i = v] \to \pi(v)$ for every start. So $T^{(i)}(v) \to T_G \deg(v) / (2m)$, and the score $R(v) = T(v) / \deg(v)$ of line L6 tends to $T_G / (2m)$ for every $v$. Only the convergence theorem is cited; the stationarity check is the computation above.

**Lemma 3 (escape bound).** Let $H \subseteq V$ be the honest nodes, $Y = V \setminus H$ the Sybil nodes, and $A$ the set of attack edges $\{u, s\}$ with $u \in H$ and $s \in Y$. If $S \subseteq H$, then for every $w \ge 0$,

$$
\sum_{s \in Y} T^{(w)}(s) \le \sum_{i=0}^{w-1} \sum_{\{u, s\} \in A} \frac{T^{(i)}(u)}{\deg(u)} .
$$

The bound holds for every graph on $Y$ and every choice of $A$, so it holds against an attacker who controls all Sybil nodes and their edges.

*Proof.* Let $\sigma_i = \sum_{s \in Y} T^{(i)}(s)$. Since $S \subseteq H$, $\sigma_0 = 0$. Fix $i \ge 1$. By Lemma 1, each node $x$ sends $T^{(i-1)}(x) / \deg(x)$ along each of its $\deg(x)$ edge ends, and $T^{(i)}(v)$ is the sum of what arrives at $v$. Split the trust that arrives in $Y$ by the sender. A Sybil sender $x \in Y$ sends at most $T^{(i-1)}(x)$ in total, so all Sybil senders together deliver at most $\sigma_{i-1}$ to $Y$. An honest sender $u \in H$ delivers to $Y$ only along its attack edges, $T^{(i-1)}(u) / \deg(u)$ on each. Hence

$$
\sigma_i \le \sigma_{i-1} + \sum_{\{u, s\} \in A} \frac{T^{(i-1)}(u)}{\deg(u)} .
$$

Summing this inequality from $i = 1$ to $w$ and using $\sigma_0 = 0$ gives the claim. $\square$

**Corollary (per-step cap).** If $T^{(i)}(u) / \deg(u) \le \tau$ for every honest node $u$ that has an attack edge and every $i < w$, then $\sum_{s \in Y} T^{(w)}(s) \le w |A| \tau = w g \tau$. This is the form used by Cao et al.: in a fast-mixing honest region, $T^{(i)}(u) / \deg(u)$ is close to $T_G / (2m)$ after a few steps, so the Sybil region gains about $g T_G / (2m)$ per step and $O(g T_G \log n / m)$ after $w = O(\log n)$ steps, however many Sybil nodes there are. The step from "close to" to a bound on the ranking is the security analysis of Cao et al. and is not proved here.

**Theorem 2 (the output).** Line L7 returns the nodes of $V$, each exactly once, in nondecreasing order of $R(v) = T^{(w)}(v) / \deg(v)$, with ties broken by the string form of the node.

*Proof.* Line L6 defines $R(v)$ for every $v$; the division is defined because $\deg(v) \ge 1$. Line L7 sorts the list of all nodes by the key $(R(v), \text{name}(v))$, and a sort returns a permutation of its input in nondecreasing key order. $\square$

**Cost.** Lines L3 and L5 take $O(n)$ per iteration, and line L4 takes $O(\deg(u))$ for each $u$, so $O(n + m)$ per iteration in total. Line L1 and line L6 take $O(n)$, and line L7 takes $O(n \log n)$ comparisons. With $w$ iterations the time is $O(w (n + m) + n \log n)$, which is $O((n + m) \log n)$ for $w = \lceil \log_2 n \rceil$. Two vectors of $n$ values are kept, so the extra space is $O(n)$. $\blacksquare$
