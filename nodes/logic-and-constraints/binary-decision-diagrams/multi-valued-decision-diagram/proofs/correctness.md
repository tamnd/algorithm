---
title: Reduced MDDs are canonical, APPLY computes the pointwise operation with O(|f| |g|) calls, and COUNT counts the inputs with a given value
proves: [correctness]
status: full
---

The variables are $x_1, \ldots, x_n$ in this order, and $x_i$ has the domain $D_i = \{0, \ldots, d_i - 1\}$. A sink $(n + 1, c)$ has the level $n + 1$ and the function $f \equiv c$. An inner node $u = (v, (c_0, \ldots, c_{d_v - 1}))$ has the level $v$, all children have larger levels, and $f_u(x) = f_{c_j}(x)$ where $x_v = j$. By induction from the sinks, $f_u$ depends only on the variables $x_v, \ldots, x_n$, where $v$ is the level of $u$. The store is *reduced* if no inner node has all children equal, no two sinks have the same value, and no two inner nodes have the same variable and the same tuple of children. CONST and MK keep it reduced: line L1 never makes a node with equal children, and line L2 returns a stored node when the key exists.

**Theorem 1 (canonicity).** In a reduced store, (a) every inner node $u$ depends on the variable of its level, and (b) two distinct nodes compute distinct functions.

*Proof.* By induction on $k$ from $n + 1$ down to 1, for the nodes on the levels $k$ and above. For $k = n + 1$ the nodes are sinks with distinct values, so (b) holds and (a) is empty.

Let $k \le n$ and let $u = (k, (c_0, \ldots, c_{d_k - 1}))$. The children are on levels larger than $k$, and they are not all equal, say $c_i \ne c_j$. By (b) for those levels, $f_{c_i} \ne f_{c_j}$. Neither depends on $x_k$, so $f_u|_{x_k = i} = f_{c_i} \ne f_{c_j} = f_u|_{x_k = j}$, and $f_u$ depends on $x_k$. This is (a).

For (b), let $u \ne w$ be nodes on levels $k$ and above with $f_u = f_w$. If both are on levels above $k$, (b) for those levels gives a contradiction. If $u$ is on level $k$ and $w$ is on a level above $k$, then $f_u$ depends on $x_k$ by (a) and $f_w$ does not, which is a contradiction. If both are on level $k$, with children $c_j$ and $c'_j$, then $f_{c_j} = f_u|_{x_k = j} = f_w|_{x_k = j} = f_{c'_j}$ for each $j$, so $c_j = c'_j$ by (b) for the higher levels. Then $u$ and $w$ have the same key, and the merging rule gives $u = w$. $\square$

So EQUAL by ids is correct: two nodes are equal if and only if their functions are equal. Also, for each function there is exactly one reduced MDD for the order: the nodes are the distinct subfunctions $f|_{x_1 = a_1, \ldots, x_{k-1} = a_{k-1}}$ that depend on $x_k$, for each $k$, plus the sinks for the values.

**Lemma 2 (child).** If $v$ is at most the level of $u$, then $f_{\mathrm{child}(u, v, j)} = f_u|_{x_v = j}$ for each $j \in D_v$, and $\mathrm{child}(u, v, j)$ is on a level larger than $v$.

*Proof.* If $u$ is on level $v$, the children are the restrictions by definition. Otherwise $u$ is on a level larger than $v$, so $f_u$ does not depend on $x_v$, and $f_u|_{x_v = j} = f_u$, which is what child returns. $\square$

**Lemma 3 (EVALUATE).** EVALUATE$(u, x)$ returns $f_u(x)$ after at most $n$ steps.

*Proof.* Lines L4 and L5 keep the invariant $f_u(x) = f_{u_0}(x)$, where $u_0$ is the start node, since $f_u(x) = f_{c_j}(x)$ for $j = x_{\mathrm{var}(u)}$. Every step goes to a larger level, so there are at most $n$ steps, and line L6 returns the value of the sink, which is $f_{u_0}(x)$. $\square$

**Theorem 4 (APPLY).** APPLY$(\mathrm{op}, f, g)$ returns the node of $x \mapsto \mathrm{op}(f_f(x), f_g(x))$. At most $\lvert f \rvert \cdot \lvert g \rvert$ calls reach line L8, and the result has at most $\lvert f \rvert \cdot \lvert g \rvert$ nodes, where $\lvert f \rvert$ is the number of nodes reachable from $f$.

*Proof.* Correctness is by induction on the sum of the levels of the two arguments, which grows in every recursive call, by Lemma 2. Line L7 is correct for two sinks. The cache only returns results of earlier calls with the same arguments. At line L8, $v$ is at most both levels, so Lemma 2 applies. For each $j \in D_v$, the result at $x_v = j$ must be $\mathrm{op}(f_f|_{x_v = j}, f_g|_{x_v = j}) = \mathrm{op}(f_{\mathrm{child}(f, v, j)}, f_{\mathrm{child}(g, v, j)})$, which the call of line L9 computes by induction. No $r_j$ depends on $x_v$: by induction, a call returns a node whose level is at least the smaller level of its arguments, since MK at level $w$ returns a node of level $w$ or one of its children, and the arguments of the calls in line L9 are on levels larger than $v$. So the node MK$(v, (r_0, \ldots, r_{d_v - 1}))$ of line L10 has the function $x \mapsto f_{r_{x_v}}(x)$, which is the required function.

For the cost, every pair of arguments is $(f', g')$ with $f'$ reachable from $f$ and $g'$ reachable from $g$, since child returns the node or one of its children. With the cache, each pair reaches line L8 at most once, so there are at most $\lvert f \rvert \cdot \lvert g \rvert$ such calls. Each does $O(d_v)$ expected work besides the recursion: $d_v$ calls in line L9 and one MK, which hashes a tuple of length $d_v$. Each node of the result is returned by one of these calls or by line L7 for a pair of sinks, so the result has at most $\lvert f \rvert \cdot \lvert g \rvert$ nodes. $\square$

**Theorem 5 (COUNT).** Let $P = \prod_{i=1}^n d_i$. Define $c(s) = P$ for a sink $s$ with the value $r$, $c(s) = 0$ for the other sinks, and $c(u) = \frac{1}{d_v} \sum_{j} c(c_j)$ for an inner node $u = (v, (c_0, \ldots, c_{d_v - 1}))$. Then $c(u) = \lvert \{ x \in D_1 \times \cdots \times D_n : f_u(x) = r \} \rvert$ for every node $u$.

*Proof.* Write $N(u)$ for the right side. By induction from the sinks. For a sink, $f_u$ is constant, so $N(u)$ is $P$ if its value is $r$ and 0 otherwise. For an inner node $u$ on level $v$, split the inputs by the value of $x_v$: $N(u) = \sum_j \lvert \{ x : x_v = j, f_{c_j}(x) = r \} \rvert$. The child $c_j$ is on a level larger than $v$, so $f_{c_j}$ does not depend on $x_v$, and the map that changes $x_v$ is a bijection between the inputs with $x_v = j$ and those with $x_v = j'$ that keeps $f_{c_j}(x)$. So the inputs with $f_{c_j}(x) = r$ are spread evenly over the $d_v$ values of $x_v$, and $\lvert \{ x : x_v = j, f_{c_j}(x) = r \} \rvert = N(c_j) / d_v$. By induction $N(c_j) = c(c_j)$, so $N(u) = \frac{1}{d_v} \sum_j c(c_j) = c(u)$. The division is exact because each term $N(c_j)$ is a multiple of $d_v$, by the same bijection. With one pass over the nodes in order of level, COUNT makes $O(\lvert f \rvert \cdot d)$ arithmetic operations. $\blacksquare$
