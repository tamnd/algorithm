---
title: SLOW-APSP computes hop-bounded distances and all distances
proves: [correctness, termination]
status: full
---

The graph has vertices $1, \ldots, n$ and real weights. $W$ is built as on the main page: $W[i][i] = \min(0, c)$ over the self-loops $i \to i$ of weight $c$ (0 if there are none), $W[i][j]$ is the least weight of an arc $i \to j$ for $i \ne j$, and $\infty$ if there is none. For $r \ge 1$ let $\lambda_r(i, j)$ be the infimum of $w(p)$ over walks $p$ from $i$ to $j$ with at most $r$ arcs, where the empty walk $\langle i \rangle$ counts for $i = j$. There are finitely many such walks, so $\lambda_r(i, j)$ is a real number or $\infty$. Let $L^{(r)}$ be the value of $L$ after the loop step for $r$ (and $L^{(1)} = W$).

**Lemma 1.** For every $r \ge 1$ and all $i, j$, $L^{(r)}[i][j] = \lambda_r(i, j)$.

*Proof.* By induction on $r$. For $r = 1$: a walk with at most one arc from $i$ to $j \ne i$ is one arc $i \to j$, and the least weight is $W[i][j]$. For $i = j$ the walks are $\langle i \rangle$ of weight 0 and the self-loops, and the least weight is $W[i][i]$.

Step from $r - 1$ to $r \ge 2$. Line L8 gives $L^{(r)}[i][j] = \min_k \big(\lambda_{r-1}(i, k) + W[k][j]\big)$.

($\ge$) Each term is the weight of a walk from $i$ to $j$ with at most $r$ arcs, or $\infty$. If $W[k][j]$ is finite and $k \ne j$, it is an arc $k \to j$, and a best walk to $k$ with at most $r - 1$ arcs followed by that arc has at most $r$ arcs. If $k = j$, then $W[j][j]$ is 0 (append nothing) or a self-loop (append it). So each term is at least $\lambda_r(i, j)$.

($\le$) Let $p$ be a walk from $i$ to $j$ with at most $r$ arcs. If $p$ has no arc, then $i = j$, and the term $k = j$ is at most $\lambda_{r-1}(j, j) + W[j][j] \le 0 + 0 = w(p)$. Otherwise let $k \to j$ be its last arc and $p'$ the rest, which has at most $r - 1$ arcs. The term for $k$ is at most $w(p') + W[k][j] \le w(p') + w(k, j) = w(p)$; for $k = j$ this uses $W[j][j] \le$ the weight of every self-loop at $j$. So the minimum is at most $\lambda_r(i, j)$. $\square$

**Lemma 2.** If the graph has no negative cycle, then $\lambda_{n-1}(i, j) = \lambda_n(i, j) = \delta(i, j)$ for all $i, j$.

*Proof.* Every walk from $i$ to $j$ that repeats a vertex contains a cycle, and removing it gives a shorter walk from $i$ to $j$ of weight at most as large, since the cycle has weight at least 0. Repeating this gives a simple path, with at most $n - 1$ arcs and weight at most $w(p)$. So the infimum over all walks equals the infimum over walks with at most $n - 1$ arcs, and also over walks with at most $n$ arcs, since these lie in between. For an unreachable pair both sides are $\infty$. $\square$

**Lemma 3.** The graph has a negative cycle if and only if $\lambda_n(i, i) < 0$ for some $i$.

*Proof.* ($\Rightarrow$) A negative cycle $C$ has at most $n$ arcs, as its vertices are distinct. For a vertex $i$ on $C$, the walk around $C$ from $i$ is a walk from $i$ to $i$ with at most $n$ arcs and negative weight, so $\lambda_n(i, i) < 0$. ($\Leftarrow$) If there is no negative cycle, Lemma 2 gives $\lambda_n(i, i) = \delta(i, i) = 0$, because the empty walk has weight 0 and no closed walk is negative. $\square$

**Theorem.** SLOW-APSP returns "negative cycle" if and only if the graph has a negative cycle. Otherwise it returns $L[i][j] = \delta(i, j)$ for all $i, j$, with $\infty$ exactly for the pairs where $j$ is not reachable from $i$.

*Proof.* After the loop of lines L2 and L3, $L = L^{(n)}$ (for $n = 1$ the loop is empty and $L = L^{(1)} = W$). By Lemma 1, $L = \lambda_n$. Line L4 tests the condition of Lemma 3. If it does not return, there is no negative cycle, and Lemma 2 gives $L = \delta$. A pair has a finite entry exactly when some walk joins it, which is reachability. $\square$

**Termination.** All loops have fixed bounds: $n - 1$ calls of EXTEND, each with $n^3$ steps, and $n$ tests in line L4. $\blacksquare$
