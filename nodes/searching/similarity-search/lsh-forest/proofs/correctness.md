---
title: The LSH forest returns the best of the candidates at the stopping depth, and finds near points with the probability of LSH at any reached depth
proves: [correctness]
status: full
---

We use the names of the pseudocode on the page. Fix the points $P$, $|P| = n \ge 1$, the directions, and the query $q$. Let $\lambda_i(v)$ be the label of $v$ in tree $i$, and $\mathrm{lcp}_i(p) \in \{0, \ldots, K\}$ the length of the longest common prefix of $\lambda_i(p)$ and $\lambda_i(q)$. For $0 \le x \le K$ let $C_x = \{p \in P : \mathrm{lcp}_i(p) \ge x \text{ for some } i\}$, and $C_{K+1} = \emptyset$.

**Lemma 1 (nesting).** $C_0 = P$ and $C_{x+1} \subseteq C_x$ for $0 \le x \le K$.

*Proof.* Every $\mathrm{lcp}_i(p) \ge 0$, and $\mathrm{lcp}_i(p) \ge x + 1$ implies $\mathrm{lcp}_i(p) \ge x$. $\square$

**Lemma 2 (one round).** For a given $x$, line L6 sets $C = C_x$.

*Proof.* Tree $i$ stores the points sorted by label (line L3). The labels that begin with the $x$-bit prefix $\lambda_i(q)[1..x]$ are those $\ge$ the prefix and $<$ the prefix followed by a symbol larger than both bits, in lexicographic order, so they form a contiguous range, and line L6 takes exactly the points with $\mathrm{lcp}_i(p) \ge x$. The union over $i$ is $C_x$. $\square$

**Lemma 3 (the start).** Line L4 sets $x$ to $x_0 = \max_{i, p} \mathrm{lcp}_i(p)$, and $C_{x_0} \ne \emptyset$ while $C_x = \emptyset$ for $x > x_0$.

*Proof.* In lexicographic order, among the stored labels, one with the longest common prefix with $\lambda_i(q)$ is adjacent to the position of $\lambda_i(q)$: if a label $\mu$ shares $t$ bits with $\lambda_i(q)$, every label between $\mu$ and $\lambda_i(q)$ in sorted order also begins with those $t$ bits. So the two neighbors of that position give $\max_p \mathrm{lcp}_i(p)$, and line L4 takes the maximum over the trees. The rest is the definition of $C_x$. $\square$

**Theorem 1 (the candidates).** QUERY stops with $x = x^* = \max\{x : |C_x| \ge \min(M, n)\}$ and $C = C_{x^*}$, and returns the $\min(k, |C|)$ points of $C$ of smallest angle to $q$. If $M \ge n$, they are the $k$ points of $P$ of smallest angle.

*Proof.* The set over which the maximum is taken contains 0, since $|C_0| = n$, so $x^*$ exists. If $x^* > x_0$ then $C_{x^*} = \emptyset$ by Lemma 3, but $|C_{x^*}| \ge \min(M, n) \ge 1$ for $M \ge 1$; so $x^* \le x_0$. The loop tests $x = x_0, x_0 - 1, \ldots$ in turn and, by Lemma 2, computes $C_x$; it exits at the first $x$ with $|C_x| \ge \min(M, n)$ or at $x = 0$. Every $x > x^*$ fails the test by the definition of $x^*$, and $x^*$ passes it, so the loop exits at $x^*$ (at $x = 0$ the test passes too, and $x^* = 0$ then). Line L9 ranks $C$. If $M \ge n$, the test needs $|C_x| = n$, and $C = P$. $\square$

**Theorem 2 (comparison with LSH of fixed length).** If $x^* \le k_0$, then every point that collides with $q$ in some tree on the first $k_0$ bits, that is every candidate of standard LSH with these $l$ tables and key length $k_0$, is in $C$.

*Proof.* Such a point is in $C_{k_0} \subseteq C_{x^*}$ by Lemma 1. $\square$

**Theorem 3 (success probability).** Let the $lK$ directions be independent standard Gaussian vectors, and let $p \in P$ be at angle $\theta$ to $q$, with $s = 1 - \theta/\pi$. For every $0 \le k_0 \le K$,
$$\Pr[p \notin C] \le (1 - s^{k_0})^l + \Pr[x^* > k_0] \le (1 - s^{k_0})^l + \frac{\mathbb{E}\,|C_{k_0 + 1}|}{\min(M, n)}.$$

*Proof.* If $p \in C_{k_0}$ and $x^* \le k_0$, then $p \in C$ by Theorem 2. So $p \notin C$ implies $p \notin C_{k_0}$ or $x^* > k_0$, and the union bound gives the first inequality, once we show $\Pr[p \notin C_{k_0}] = (1 - s^{k_0})^l$. A single bit $b_{i,j}$ agrees on $p$ and $q$ with probability $1 - \theta/\pi = s$, since a Gaussian direction is uniform in angle and the hyperplane it defines separates $p$ and $q$ with probability $\theta/\pi$; the bits are independent. So $\mathrm{lcp}_i(p) \ge k_0$ with probability $s^{k_0}$, independently over the trees, and $p \notin C_{k_0}$ with probability $(1 - s^{k_0})^l$. For the second inequality, if $x^* > k_0$ then $|C_{k_0 + 1}| \ge |C_{x^*}| \ge \min(M, n)$ by Lemma 1, and Markov's inequality gives $\Pr[|C_{k_0+1}| \ge \min(M, n)] \le \mathbb{E}|C_{k_0+1}| / \min(M, n)$. For $k_0 = K$, $C_{K+1} = \emptyset$ and $x^* \le K$ always. $\blacksquare$
