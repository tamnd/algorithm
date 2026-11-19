---
title: The unit selection search returns a sequence of least total cost, chosen by the tie rule
proves: [correctness]
status: full
---

Fix the targets $t_1, \ldots, t_n$ with $n \ge 1$ and the candidate lists $U_1, \ldots, U_n$ of line L1, each non-empty and in database order. Write $u \in U_i$ also for its index in $U_i$. For a sequence $s = (s_1, \ldots, s_i)$ with $s_k \in U_k$ define

$$K_i(s) = \sum_{k=1}^{i} TC(t_k, s_k) + \sum_{k=2}^{i} JC(s_{k-1}, s_k).$$

All costs are finite non-negative reals, since a candidate has the phone of its target. The work is in the tropical semiring $(\mathbb{R} \cup \{+\infty\}, \min, +, +\infty, 0)$. The costs satisfy

$$K_i(s_1, \ldots, s_i) = K_{i-1}(s_1, \ldots, s_{i-1}) + JC(s_{i-1}, s_i) + TC(t_i, s_i). \tag{1}$$

This is the length of a path in the layered graph with one node per candidate, edges from each node of layer $i - 1$ to each node of layer $i$ of length $JC + TC$, and a source joined to layer 1 by edges of length $TC$. The sequences are exactly the source to layer $n$ paths, so a sequence of least cost is a shortest path in a directed acyclic graph.

## Exact search (no beam)

**Lemma 1.** After line L2 and after the pass of line L3 for each $i \ge 2$, $C_i(u) = \min \{ K_i(s) : s_i = u \}$ for every $u \in U_i$.

*Proof.* By induction on $i$. For $i = 1$ the only sequence is $(u)$, and line L2 sets $C_1(u) = TC(t_1, u) = K_1(u)$. For $i \ge 2$, every sequence with $s_i = u$ has some $s_{i-1} = v$, and by (1) and the induction hypothesis

$$\min_{s_i = u} K_i = \min_{v \in U_{i-1}} \bigl( C_{i-1}(v) + JC(v, u) \bigr) + TC(t_i, u),$$

because adding a constant keeps the order (the principle of optimality). Line L5 takes a minimizer $B_i(u)$ of the inner term and line L6 adds $TC(t_i, u)$. $\square$

**Lemma 2.** For $i \ge 2$, the sequence obtained by following the back pointers from $u \in U_i$ to layer 1 has cost $C_i(u)$.

*Proof.* By induction on $i$, from (1): the pointer $v = B_i(u)$ has $C_{i-1}(v) + JC(v, u) + TC(t_i, u) = C_i(u)$, and the sequence from $v$ has cost $C_{i-1}(v)$. $\square$

**Theorem 1.** Without a beam, lines L8 to L10 return a sequence $s^*$ with $K_n(s^*) = \min_s K_n(s)$, and its cost.

*Proof.* Line L8 picks $u_n$ that minimizes $C_n$, which by Lemma 1 is the minimum of $K_n$ over all sequences. By Lemma 2 the traceback of line L9 gives a sequence of that cost. $\square$

**Theorem 2 (tie rule).** Among the sequences of least cost, the returned one is the smallest in the lexicographic order of $(s_n, s_{n-1}, \ldots, s_1)$, comparing indices in the candidate lists.

*Proof.* Line L8 takes the first minimizer, so $s_n$ is the smallest last index of an optimal sequence. Assume $s_n, \ldots, s_{i}$ are the smallest such indices among the optimal sequences that end with them. The optimal sequences that end with $s_{i}, \ldots, s_n$ are those whose prefix through layer $i - 1$ has $s_{i-1} = v$ with $C_{i-1}(v) + JC(v, s_i) = \min_{v'} (C_{i-1}(v') + JC(v', s_i))$ and is optimal for $v$. Line L5 scans $v$ in increasing order and replaces the stored candidate only on a strictly smaller value, so $B_i(s_i)$ is the smallest such $v$. Induction down to $i = 2$ gives the claim. $\square$

The tests compare the output, ties included, with a brute force search over all $\prod_i |U_i|$ sequences that uses this rule.

## Beam

With a beam of width $K$, line L7 keeps only the $K$ units of layer $i$ with the smallest $C_i$, and line L5 then minimizes over the kept units only. If $K \ge |U_i|$ for every layer, nothing is removed and Theorems 1 and 2 hold unchanged. For smaller $K$ the invariant of Lemma 1 becomes an upper bound: $C_i(u)$ is the least cost over the sequences whose units all survived the pruning, which is at least the true minimum. The pruning can remove the first unit of the only optimal sequence. A two-target example with one unit of target cost 0 and a costly join, and one unit of target cost 1 followed by its free join, makes a beam of 1 return a sequence of cost 45 when the optimum is 1; the tests check this case.

## Cost

Line L5 looks at $|U_{i-1}|$ predecessors for each of the $|U_i|$ units, so the time is $\Theta(\sum_{i=2}^{n} |U_{i-1}| |U_i|)$ cost evaluations, which is $\Theta(n K^2)$ when each list has $K$ units. With a beam of width $B$, the time is $O(n K B)$ plus the selection of the $B$ best per layer. The back pointers take $\Theta(n K)$ space.
