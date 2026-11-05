---
title: The Batagelj-Zaversnik algorithm computes the core numbers
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a simple undirected graph with $n$ vertices. For a set $S \subseteq V$ and a vertex $u$, write $r_S(u)$ for the number of neighbours of $u$ in $S$. Recall that $\mathrm{core}(v)$ is the largest $k$ such that some set $S \ni v$ has $r_S(x) \ge k$ for all $x \in S$.

**Termination.** Lines L1 to L6 are loops over $V$ and over $0, \ldots, \mathrm{md}$. Line L7 runs $n$ times, and line L9 runs over the finite list $\mathrm{Adj}[v]$. So the algorithm stops.

In iteration $i$ of line L7 (counting from 0), call the vertices $\mathrm{vert}[i], \ldots, \mathrm{vert}[n-1]$ at its start the *remaining* vertices, and let $R_i$ be their set. We show below that the loop never writes to $\mathrm{vert}[j]$ for $j \le i$ in iteration $i$, so the vertex removed in iteration $i$ is $v_i = \mathrm{vert}[i]$, and $R_{i+1} = R_i \setminus \{v_i\}$. Let $D_i$ be the value of $\mathrm{deg}[v_i]$ at line L8, and let $D_{-1} = 0$.

Lemmas 1 and 2 are proved together, by induction on $i$.

**Lemma 1 (the array).** At the start of iteration $i$:

1. $\mathrm{vert}$ is a permutation of $V$ and $\mathrm{pos}$ is its inverse;
2. $\mathrm{deg}[\mathrm{vert}[i]] \le \mathrm{deg}[\mathrm{vert}[i+1]] \le \cdots \le \mathrm{deg}[\mathrm{vert}[n-1]]$;
3. for each $d$ with $\mathrm{deg}[\mathrm{vert}[i]] < d \le \mathrm{md}$, $\mathrm{bin}[d]$ is the least index $j \ge i$ with $\mathrm{deg}[\mathrm{vert}[j]] \ge d$, or $n$ if there is none.

*Proof.* At $i = 0$: lines L3 and L4 set $\mathrm{bin}[d]$ to the number of vertices of degree less than $d$. Line L5 places the vertices of degree $d$ at the indices $\mathrm{bin}[d], \mathrm{bin}[d] + 1, \ldots$, so $\mathrm{vert}$ is sorted by degree and $\mathrm{pos}$ is its inverse, and after line L5 each $\mathrm{bin}[d]$ holds the number of vertices of degree at most $d$. Line L6 shifts these values up by one place, from the top down so that no value is overwritten before it is read, so $\mathrm{bin}[d]$ is again the number of vertices of degree less than $d$, which is the least index of a vertex of degree at least $d$. This gives 1 to 3.

Now assume 1 to 3 at the start of iteration $i$, and let $v = \mathrm{vert}[i]$ and $D = \mathrm{deg}[v]$. In the iteration, line L13 only changes $\mathrm{deg}[u]$ for a neighbour $u$ with $\mathrm{deg}[u] > D$, and lowers it by 1, so it never goes below $D$; and $u \ne v$ since there are no self-loops, so $\mathrm{deg}[v] = D$ during the whole iteration. We show that one run of lines L11 to L13 keeps 1 and 2, and keeps 3 for all $d > D$, with $j \ge i$ read as $j > i$.

Let $du = \mathrm{deg}[u] > D$. By 3, $pw = \mathrm{bin}[du]$ is the least index $\ge i$ whose vertex has degree at least $du$. Since $\mathrm{deg}[v] = D < du$, $pw > i$. Since $u$ has degree $du$ and sits at index $pu \ge i$ (it is remaining, because each removed vertex $v_j$ keeps $\mathrm{deg}[v_j] = D_j \le D$ by Lemma 2), $pw \le pu$, and by 2 every index from $pw$ to $pu$ holds a vertex of degree exactly $du$. Line L12 swaps the entries at $pw$ and $pu$ and updates $\mathrm{pos}$, so 1 holds, and the degrees along the array are unchanged, so 2 holds. Line L13 lowers the degree at index $pw$ to $du - 1$. All indices from $i$ to $pw - 1$ hold degrees at most $du - 1$, and all indices after $pw$ hold degrees at least $du$, so 2 still holds. For $d = du$, the least index with degree at least $du$ is now $pw + 1$ (or $n$), and line L13 sets $\mathrm{bin}[du] = pw + 1$. For other $d > D$, the set of indices with degree at least $d$ did not change, so $\mathrm{bin}[d]$ stays right. No entry at an index $\le i$ was written, since $pw > i$ and $pu \ge pw$.

At the end of the iteration, the next vertex $\mathrm{vert}[i+1]$ has degree at least $D$ by 2, so each $d > \mathrm{deg}[\mathrm{vert}[i+1]]$ has $d > D$, and the least index $j > i$ is the least index $j \ge i + 1$. So 1 to 3 hold at the start of iteration $i + 1$. $\square$

By Lemma 1, part 2, $v_i$ has the least $\mathrm{deg}$ value among the remaining vertices.

**Lemma 2 (the degrees).** At the start of iteration $i$, $D_{i-1} \le \mathrm{deg}[u]$ and

$$\mathrm{deg}[u] = \max(D_{i-1}, r_{R_i}(u)) \qquad \text{for each } u \in R_i,$$

and $\mathrm{deg}[v_j] = D_j$ for each $j < i$. Moreover $D_{i-1} \le D_i$.

*Proof.* At $i = 0$, $R_0 = V$, $D_{-1} = 0$ and $\mathrm{deg}[u] = |\mathrm{Adj}[u]| = r_V(u)$. Assume the claim at the start of iteration $i$, and let $v = v_i$ and $D = D_i = \mathrm{deg}[v]$. Since $v$ has the least $\mathrm{deg}$ among the remaining vertices and each of them has $\mathrm{deg} \ge D_{i-1}$, we get $D \ge D_{i-1}$. Let $R' = R_{i+1} = R_i \setminus \{v\}$. Take $u \in R'$.

- If $u$ is a neighbour of $v$ and $\mathrm{deg}[u] > D$: then $\max(D_{i-1}, r_{R_i}(u)) > D \ge D_{i-1}$, so $\mathrm{deg}[u] = r_{R_i}(u)$. Line L13 sets $\mathrm{deg}[u] = r_{R_i}(u) - 1 = r_{R'}(u)$, which is at least $D$. So $\mathrm{deg}[u] = \max(D, r_{R'}(u))$.
- If $u$ is a neighbour of $v$ and $\mathrm{deg}[u] \le D$: then $\mathrm{deg}[u] = D$ by the choice of $v$, so $r_{R_i}(u) \le D$ and $r_{R'}(u) < D$. The value stays $D = \max(D, r_{R'}(u))$.
- If $u$ is not a neighbour of $v$: $r_{R'}(u) = r_{R_i}(u)$ and $\mathrm{deg}[u]$ does not change. If $r_{R_i}(u) \ge D_{i-1}$, then $\mathrm{deg}[u] = r_{R'}(u) \ge D$ by the choice of $v$, which is $\max(D, r_{R'}(u))$. Else $\mathrm{deg}[u] = D_{i-1} \ge D \ge D_{i-1}$, so $D = D_{i-1} = \mathrm{deg}[u] > r_{R'}(u)$, and again $\mathrm{deg}[u] = \max(D, r_{R'}(u))$.

The value $\mathrm{deg}[v] = D$ is not changed in iteration $i$, as shown in Lemma 1. In later iterations, line L13 only lowers $\mathrm{deg}[x]$ when $\mathrm{deg}[x] > D_j \ge D$ for the removed $v_j$, and $\mathrm{deg}[v] = D$, so it never touches $v$ again; the same holds for each earlier $v_j$. This gives the claim at the start of iteration $i + 1$. $\square$

So $D_0 \le D_1 \le \cdots \le D_{n-1}$, and the returned value for $v_i$ is $D_i$.

**Theorem.** For each $i$, $D_i = \mathrm{core}(v_i)$.

*Proof.* *Lower bound.* Let $j \le i$ be the least index with $D_j = D_i$. If $j = 0$, then $D_0 = \min_u r_V(u)$, so every vertex of $R_0 = V$ has at least $D_i$ neighbours in $R_0$. If $j > 0$, then $D_j > D_{j-1}$. By Lemma 2, $D_j = \min_{u \in R_j} \max(D_{j-1}, r_{R_j}(u))$, so for each $u \in R_j$, $\max(D_{j-1}, r_{R_j}(u)) \ge D_j > D_{j-1}$, which forces $r_{R_j}(u) \ge D_j$. In both cases $R_j$ is a set in which every vertex has at least $D_i$ neighbours, and it contains $v_i$ since $j \le i$. So $\mathrm{core}(v_i) \ge D_i$.

*Upper bound.* Let $S \ni v_i$ be a set with $r_S(x) \ge k$ for all $x \in S$. Let $v_j$ be the vertex of $S$ that is removed first, so $j \le i$ and $S \subseteq R_j$. Then $r_{R_j}(v_j) \ge r_S(v_j) \ge k$, and by Lemma 2, $D_j = \mathrm{deg}[v_j] \ge r_{R_j}(v_j) \ge k$. Since the $D$ values do not decrease, $D_i \ge D_j \ge k$. Taking $k = \mathrm{core}(v_i)$ gives $D_i \ge \mathrm{core}(v_i)$.

Line L14 returns $\mathrm{deg}$, and by Lemma 2 at the end, $\mathrm{deg}[v_i] = D_i = \mathrm{core}(v_i)$ for every $i$. $\blacksquare$
