---
title: Generic join computes the join, and its work at each attribute is at most the AGM bound
proves: [correctness, complexity]
status: full
---

Notation. The query has hypergraph $H = (V, E)$ and the global order $v_1, \ldots, v_k$ of $V$. Write $V_{<i} = \{v_1, \ldots, v_{i-1}\}$ and $V_{\le i} = V_{<i} \cup \{v_i\}$. For a tuple $t$ over $V_{<i}$ and an edge $e \ni v_i$, let

$$R_e[t] = \{ a : \text{some } r \in R_e \text{ has } r[e \cap V_{<i}] = t[e \cap V_{<i}] \text{ and } r[v_i] = a \}.$$

In the trie of $R_e$, whose levels follow the global order, $R_e[t]$ is the set of keys of the node reached from the root by the values $t[e \cap V_{<i}]$; this is the set $C_e$ of line L3. Let $P_i$ be the set of tuples over $V_{\le i}$ whose projection on $e \cap V_{\le i}$ lies in $\pi_{e \cap V_{\le i}} R_e$ for each edge $e$ (an empty projection condition is true). $P_0$ holds the empty tuple, and $P_k = Q(D)$.

**Lemma 1 (prefixes).** The tuples pushed with level $i$ are exactly the tuples of $P_i$, each pushed once.

*Proof.* By induction on $i$. For $i = 0$, line L1 pushes only the empty tuple. Let $i \ge 1$. A tuple $(t, a)$ with $t$ over $V_{<i}$ is in $P_i$ if and only if $t \in P_{i-1}$ and $a \in R_e[t]$ for each $e \ni v_i$. Indeed, for an edge $e \not\ni v_i$ the condition on $(t, a)$ is the condition on $t$. For an edge $e \ni v_i$, the condition says that some $r \in R_e$ agrees with $t$ on $e \cap V_{<i}$ and has $r[v_i] = a$, which is $a \in R_e[t]$, and it implies the condition of $P_{i-1}$ on $e$. Now the pass for a popped $t \in P_{i-1}$ (pushed once, by the induction hypothesis) loops over $C_{e^*} = R_{e^*}[t]$ at line L5 and pushes $(t, a)$ exactly when $a$ is in every $C_e = R_e[t]$ (lines L6 and L7). Each $a$ is looked at once, so each $(t, a)$ is pushed at most once, and the pushed tuples are exactly the members of $P_i$ that extend $t$. $\square$

**Theorem 1 (correctness).** Generic join outputs each tuple of $Q(D)$ exactly once, and nothing else.

*Proof.* Line L2 outputs exactly the popped tuples of level $k$, which by Lemma 1 are the tuples of $P_k = Q(D)$, each once. Since each stack entry is popped once and each level is finite, the loop ends. $\blacksquare$

**The work.** Let $W_i = \sum_{t \in P_{i-1}} \min_{e \ni v_i} |R_e[t]|$, the number of iterations of line L5 at level $i$. Each iteration makes at most $|E_i| - 1$ membership tests, where $E_i$ is the set of edges that hold $v_i$.

**Theorem 2 (work bound).** For each fractional edge cover $x$ of $H$ and each level $i$, $W_i \le \prod_{e \in E} |R_e|^{x_e}$.

*Proof.* Assume $W_i > 0$, otherwise there is nothing to prove; then each $R_e$ is non-empty. For $t \in P_{i-1}$, let $e^*(t)$ be the edge chosen at line L4, and let

$$S = \{ (t, a) : t \in P_{i-1},\ a \in R_{e^*(t)}[t] \},$$

so $|S| = W_i$. Let $(T, A)$ be uniform over $S$, with $T = (T_{v_1}, \ldots, T_{v_{i-1}})$. Logarithms are to base 2, and $H$ is the Shannon entropy. Then

$$\log W_i = H(T, A) = H(T) + H(A \mid T).$$

*The last attribute.* Given $T = t$ (an event of positive probability), $A$ takes at most $|R_{e^*(t)}[t]| = \min_{e \in E_i} |R_e[t]|$ values, and this minimum is at least 1. For numbers $b_e \ge 1$ and weights $x_e \ge 0$ with $s = \sum_{e \in E_i} x_e \ge 1$, we have $\log \min_e b_e \le \sum_e (x_e / s) \log b_e \le \sum_e x_e \log b_e$. So

$$H(A \mid T) \le \sum_{e \in E_i} x_e \, \mathbb{E}\bigl[\log |R_e[T]|\bigr].$$

*The prefix.* Write $T_e$ for the restriction of $T$ to $e \cap V_{<i}$, and $h_j = H(T_{v_j} \mid T_{v_1}, \ldots, T_{v_{j-1}})$ for $j < i$. By the chain rule and because conditioning does not increase entropy, $H(T_e) \ge \sum_{j < i,\, v_j \in e} h_j$ for each $e$. With the cover condition and $h_j \ge 0$:

$$H(T) = \sum_{j < i} h_j \le \sum_{j < i} h_j \sum_{e \ni v_j} x_e = \sum_e x_e \sum_{j < i,\, v_j \in e} h_j \le \sum_e x_e H(T_e).$$

*Each edge.* For $e \notin E_i$: $T_e$ takes values in $\pi_{e \cap V_{<i}} R_e$ (because $T \in P_{i-1}$), so $H(T_e) \le \log |R_e|$. For $e \in E_i$: the size $|R_e[T]|$ depends only on $T_e$; write it $f_e(T_e)$. By Gibbs' inequality (Jensen's inequality for the concave $\log$), for any random variable $Y$ with distribution $p$ and any $f \ge 1$,

$$H(Y) + \mathbb{E}[\log f(Y)] = \sum_y p(y) \log \frac{f(y)}{p(y)} \le \log \sum_{y : p(y) > 0} f(y).$$

With $Y = T_e$, the sum $\sum_y f_e(y)$ over prefixes $y$ counts distinct pairs $(y, a)$ with $(y, a) \in \pi_{e \cap V_{\le i}} R_e$, so it is at most $|R_e|$. Hence $H(T_e) + \mathbb{E}[\log |R_e[T]|] \le \log |R_e|$.

*Together.*

$$\log W_i \le \sum_{e \notin E_i} x_e H(T_e) + \sum_{e \in E_i} x_e \bigl( H(T_e) + \mathbb{E}[\log |R_e[T]|] \bigr) \le \sum_{e \in E} x_e \log |R_e|. \qquad \blacksquare$$

**Corollary (running time).** Building the hash tries takes $O(\sum_e |e| \cdot |R_e|)$ expected time. At level $i$, the pass for one $t \in P_{i-1}$ takes $O(|E_i|)$ time for lines L3 and L4, plus $O(|E_i|)$ expected time per iteration of line L5. The number of passes at level $i$ is $|P_{i-1}| \le W_{i-1}$ for $i \ge 2$ (each tuple of $P_{i-1}$ is a pushed candidate of level $i-1$), and 1 for $i = 1$. So the expected time is

$$O\Bigl(\sum_e |e| \, |R_e| + |E| \sum_{i=1}^{k} (W_i + 1)\Bigr) = O\bigl(\textstyle\sum_e |e|\,|R_e| + k\,|E| \cdot \text{AGM}(Q, D)\bigr),$$

with $\text{AGM}(Q, D) = \min_x \prod_e |R_e|^{x_e}$ by Theorem 2, applied with the best cover. Output tuples are counted in $W_k$, since each one is an iteration of level $k$. With sorted arrays and binary search in place of hash tables, each step costs $O(\log n)$ in the worst case instead, where $n$ is the largest relation size.
