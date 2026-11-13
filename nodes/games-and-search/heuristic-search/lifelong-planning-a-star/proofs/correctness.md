---
title: Each call of COMPUTE-SHORTEST-PATH stops after at most 2n expansions with g(goal) equal to the start distance of the goal
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The graph is finite and directed, with $n$ vertices and no self-loops. Each edge cost $c(u, v)$ is a positive real number or $\infty$. The heuristic is finite and consistent for the current costs: $h(s_{goal}) = 0$ and $h(u) \le c(u, v) + h(v)$ for each edge. Adding this along a path gives $h(x) \le C + h(y)$ when a path from $x$ to $y$ costs $C$. We write $g^*(s)$ for the start distance of $s$ under the current costs. Keys are pairs compared in lexicographic order. A vertex is *consistent* when $g(s) = \mathrm{rhs}(s)$, *overconsistent* when $g(s) > \mathrm{rhs}(s)$ and *underconsistent* when $g(s) < \mathrm{rhs}(s)$.

The edge costs change only between calls, at lines L21 to L23. Everything below is about one call of COMPUTE-SHORTEST-PATH, with the costs fixed during the call.

**Fact 1 (invariants).** At line L9, and after each call of UPDATE-VERTEX that ends a group of updates:

- (I1) $\mathrm{rhs}(s_{start}) = 0$ and $\mathrm{rhs}(s) = \min_{p \in \mathrm{Pred}(s)} (g(p) + c(p, s))$ for $s \ne s_{start}$;
- (I2) $U$ holds exactly the vertices that are not consistent, each with the key CALCULATE-KEY$(s)$ of its current $g$ and $\mathrm{rhs}$;
- (I3) $g(s) \ge 0$ and $\mathrm{rhs}(s) \ge 0$ for each $s$.

*Proof.* INITIALIZE makes all values $\infty$ except $\mathrm{rhs}(s_{start}) = 0$, and puts only $s_{start}$ in $U$. A change of $c(u, v)$ changes only the right side of (I1) for $v$, and line L23 recomputes $\mathrm{rhs}(v)$ and its queue entry. Line L12 or line L15 changes only $g(u)$. This changes the right side of (I1) only for the successors of $u$, because there are no self-loops, and it changes whether $u$ itself is consistent. Lines L13 and L16 call UPDATE-VERTEX on exactly these vertices. After line L12, $u$ is consistent and was removed at line L10, so it is correctly out of $U$. The key of a vertex depends only on its own $g$ and $\mathrm{rhs}$, so the keys of the other vertices stay correct. For (I3), each finite value is $0$ or a sum of an earlier finite value and a positive cost. $\square$

**Lemma 2 (keys do not go down).** Let line L10 remove $x$ with the key $k_x$. After lines L11 to L16:

- (a) each vertex in $U$ has a key $\ge k_x$;
- (b) each vertex that is in $U$ now but was not in $U$ before the removal, or that is $x$ itself, has a key $> k_x$.

*Proof.* By (I2), $k_x$ was the least key in $U$. We use that $[a_1; a_2] > [b_1; b_2]$ when $a_1 \ge b_1$ and $a_2 > b_2$.

*Overconsistent $x$.* Write $r = \mathrm{rhs}(x)$, so $k_x = [r + h(x); r]$ and $r < \infty$. Line L12 lowers $g(x)$ to $r$, so for a successor $s$, $\mathrm{rhs}(s)$ becomes $\min(\mathrm{rhs}_{old}(s), r + c(x, s))$. If $\min(g(s), \mathrm{rhs}(s))$ did not change, the key of $s$ did not change, and if $s$ is in $U$ it was in $U$ before, with a key $\ge k_x$. Otherwise the new minimum is $r + c(x, s)$, and the key is
$$ [r + c(x, s) + h(s);\ r + c(x, s)] > [r + h(x);\ r] = k_x , $$
because $h(x) \le c(x, s) + h(s)$ and $c(x, s) > 0$. A vertex $s$ that was consistent before and is not now must be in this second case, because $\mathrm{rhs}(s)$ went down below $g(s) = \mathrm{rhs}_{old}(s)$. The vertex $x$ is consistent after line L12.

*Underconsistent $x$.* Now $k_x = [g_{old}(x) + h(x); g_{old}(x)]$ with $g_{old}(x) < \mathrm{rhs}(x)$, so $g_{old}(x) < \infty$. Line L15 raises $g(x)$ to $\infty$, so the values $\mathrm{rhs}(s)$ of the successors can only go up, and so can $\min(g(s), \mathrm{rhs}(s))$ and the keys. A vertex in $U$ before keeps a key $\ge k_x$. Let $s \ne x$ be consistent before and not after. Then $\mathrm{rhs}(s)$ went up, so the old minimum of (I1) was reached only through $x$: $g(s) = \mathrm{rhs}_{old}(s) = g_{old}(x) + c(x, s)$. The new key of $s$ is $[g(s) + h(s); g(s)] > k_x$, as in the first case. For $x$ itself, $\mathrm{rhs}(x)$ did not change. If it is $\infty$, $x$ is consistent. If not, the key of $x$ is $[\mathrm{rhs}(x) + h(x); \mathrm{rhs}(x)] > k_x$, because $\mathrm{rhs}(x) > g_{old}(x)$. $\square$

So the keys removed at line L10 form a nondecreasing sequence during a call. And once a vertex leaves $U$, it can come back only with a key larger than every key removed so far: the vertex comes back in the expansion of some $x$, and by Lemma 2(b) its key is $> k_x$, which is at least every earlier removed key. Later changes keep its key above each later $k_x$ by the same lemma.

**Lemma 3 (the low chain).** Call a vertex *low* when $g(s) < g^*(s)$. Let $s$ be low and consistent. Then $U$ holds a low vertex $q$ with $g(q) < g(s)$, and $h(q) \le g(s) - g(q) + h(s)$.

*Proof.* The start is not low, since $g(s_{start}) \ge 0 = g^*(s_{start})$. So $s \ne s_{start}$, and $\mathrm{rhs}(s) = g(s) < \infty$ is $g(y) + c(y, s)$ for some predecessor $y$, by (I1). Then $g(y) = g(s) - c(y, s) < g^*(s) - c(y, s) \le g^*(y)$, so $y$ is low, and $g(y) < g(s)$. If $y$ is not consistent, take $q = y$. If it is, repeat from $y$. The values of $g$ go down strictly along the chain, so no vertex repeats, and the chain ends at a low vertex $q$ that is not consistent, so $q \in U$ by (I2). The edges of the chain form a path from $q$ to $s$ of cost exactly $g(s) - g(q)$, so consistency gives $h(q) \le g(s) - g(q) + h(s)$. $\square$

**Lemma 4 (an overconsistent expansion is exact).** If line L10 removes an overconsistent vertex $u$, then $\mathrm{rhs}(u) = g^*(u)$. So after line L12, $g(u) = g^*(u)$.

*Proof.* Let $r = \mathrm{rhs}(u) < g(u)$, so $r < \infty$ and the key of $u$ is $[r + h(u); r]$, the least in $U$.

Suppose $r < g^*(u)$. Then $u \ne s_{start}$, and $r = g(p) + c(p, u)$ for a predecessor $p$ with $g(p) < g^*(p)$, so $p$ is low. If $p$ is consistent, Lemma 3 gives a low $q \in U$ with $g(q) \le g(p)$ and $h(q) \le g(p) - g(q) + h(p)$. If $p$ is not consistent, take $q = p$. In both cases the key of $q$ is at most $[g(q) + h(q); g(q)]$, and
$$ g(q) + h(q) \le g(p) + h(p) \le g(p) + c(p, u) + h(u) = r + h(u), \qquad g(q) \le g(p) < r . $$
So the key of $q$ is less than the key of $u$. Also $q \ne u$, because $g(q) < r < g(u)$. This contradicts the choice of $u$.

Suppose $r > g^*(u)$. Then $g^*(u) < \infty$. Let $p_0 = s_{start}, \ldots, p_k = u$ be a shortest path. If $g(p_i) \le g^*(p_i)$ for all $i < k$, then $r \le g(p_{k-1}) + c(p_{k-1}, u) \le g^*(u)$ by (I1), which is false. So let $i < k$ be the least index with $g(p_i) > g^*(p_i)$. If $i = 0$, then $g(s_{start}) > 0 = \mathrm{rhs}(s_{start})$, and $s_{start}$ is in $U$ with the key $[h(s_{start}); 0]$. If $i \ge 1$, then $\mathrm{rhs}(p_i) \le g(p_{i-1}) + c(p_{i-1}, p_i) \le g^*(p_i) < g(p_i)$, and $p_i$ is in $U$ with a key at most $[g^*(p_i) + h(p_i); g^*(p_i)]$. In both cases the key of $p_i$ is at most $[g^*(p_i) + h(p_i); g^*(p_i)]$, and since the rest of the path costs $g^*(u) - g^*(p_i)$,
$$ g^*(p_i) + h(p_i) \le g^*(u) + h(u) < r + h(u), $$
so the key of $p_i$ is less than the key of $u$, and $p_i \ne u$. This contradicts the choice of $u$ again. $\square$

**Theorem 5 (termination).** During one call, each vertex is expanded at most once as an overconsistent vertex and at most once as an underconsistent vertex, and an underconsistent expansion of a vertex comes before its overconsistent expansion. So the call stops after at most $2n$ passes of the loop.

*Proof.* The value $g(u)$ changes only when $u$ itself is expanded.

*Nothing after an overconsistent expansion.* Let $u$ be expanded as overconsistent with the key $k_1 = [r + h(u); r]$, where $r = g^*(u)$ by Lemma 4. After line L12, $g(u) = r$ and $u$ is consistent and out of $U$. Suppose $u$ is removed again later with the key $k_2$. By the remark after Lemma 2, $k_2 > k_1$. Its $g$ is still $r$. If it is overconsistent, Lemma 4 gives $\mathrm{rhs}(u) = r = g(u)$, which is false. If it is underconsistent, $k_2 = [r + h(u); r] = k_1$, which is false too.

*At most one underconsistent expansion.* After line L15, $g(u) = \infty$. A later expansion of $u$ must then be overconsistent, because an underconsistent vertex has a finite $g$, and $g(u)$ stays $\infty$ until $u$ is expanded. By the first part, nothing follows it.

So the expansions of a vertex in one call are one of: none, one overconsistent, one underconsistent, or an underconsistent one followed by an overconsistent one. Each pass of the loop removes a vertex from $U$, which is not empty: if it were, TOPKEY would be $[\infty; \infty]$ and $s_{goal}$ would be consistent by (I2), so the loop condition would be false. $\square$

**Theorem 6 (the result).** When the call returns, $g(s_{goal}) = g^*(s_{goal})$.

*Proof.* At the return, $s_{goal}$ is consistent and no key in $U$ is less than the key of $s_{goal}$, which is $[G; G]$ with $G = g(s_{goal}) = \mathrm{rhs}(s_{goal})$, because $h(s_{goal}) = 0$.

*$G \ge g^*(s_{goal})$.* If not, $s_{goal}$ is low and consistent. Lemma 3 gives a low $q \in U$ with $g(q) < G$ and $h(q) \le G - g(q)$. Its key is at most $[g(q) + h(q); g(q)]$, and $g(q) + h(q) \le G$ and $g(q) < G$, so its key is less than $[G; G]$. This is false.

*$G \le g^*(s_{goal})$.* If not, $g^*(s_{goal}) < \infty$. Take a shortest path $p_0 = s_{start}, \ldots, p_k = s_{goal}$. Since $s_{goal}$ is consistent, the argument of Lemma 4 with $u = s_{goal}$ and $r = G$ gives a vertex $p_i$ in $U$ whose key is at most $[g^*(p_i) + h(p_i); g^*(p_i)]$, where $g^*(p_i) + h(p_i) \le g^*(s_{goal}) < G$. So its key is less than $[G; G]$. This is false. $\square$

**Theorem 7 (the path).** When the call returns and $G < \infty$, start at $s_{goal}$ and repeat: go from $s$ to a predecessor $p$ that minimizes $g(p) + c(p, s)$. This reaches $s_{start}$, and the reversed walk is a shortest path of cost $G$.

*Proof.* We show by induction that each vertex $s$ that the trace reaches is consistent, has $g(s) = g^*(s)$, and has $g^*(s) + h(s) \le G$. For $s_{goal}$ this is Theorem 6. Let $s \ne s_{start}$ have these properties and let $p$ be the next vertex. By (I1), $g(p) + c(p, s) = \mathrm{rhs}(s) = g(s) = g^*(s) \le g^*(p) + c(p, s)$, so $g(p) \le g^*(p)$, and $h(p) \le c(p, s) + h(s)$ gives $g(p) + h(p) \le g^*(s) + h(s) \le G$.

If $g(p) < g^*(p)$, then $p$ is low. If $p$ is consistent, Lemma 3 gives a low $q \in U$ with $g(q) + h(q) \le g(p) + h(p) \le G$ and $g(q) < g(p)$, and if $p$ is not consistent, $q = p$ is in $U$. In both cases the key of $q$ is at most $[g(q) + h(q); g(q)]$, with $g(q) + h(q) \le G$ and $g(q) \le g(p) < g^*(s) \le G$. So its key is less than $[G; G]$, which is false. Hence $g(p) = g^*(p)$, and $g^*(p) + h(p) \le G$.

If $p$ were not consistent, its key would be at most $[g^*(p) + h(p); g^*(p)]$ with $g^*(p) + h(p) \le G$ and $g^*(p) = g^*(s) - c(p, s) < G$, which is less than $[G; G]$. So $p$ is consistent.

Along the trace, $g^*$ goes down strictly, so the trace ends, and it can end only at $s_{start}$, where $g = 0$. The costs of its edges add up to $g(s_{goal}) - g(s_{start}) = G$. $\square$

**Remark (the cost of a call).** Theorem 5 gives at most $2n$ expansions. An overconsistent expansion of $u$ calls UPDATE-VERTEX $|\mathrm{Succ}(u)|$ times, and an underconsistent one $|\mathrm{Succ}(u)| + 1$ times. Each call of UPDATE-VERTEX takes the minimum over $|\mathrm{Pred}(s)|$ predecessors and does $O(1)$ queue operations. Summed over at most two expansions per vertex, this is $O(n + m)$ calls of UPDATE-VERTEX, which is the bound of the page.
