---
title: WORK-AND-SPAN returns the work and the span of a DAG, and CRITICAL-PATH returns a longest path
proves: [correctness, complexity]
status: full
---

We use the pseudocode of the page. Let $G = (V, E)$ have $n$ strands and $m$ edges. For a strand $v$, let $D(v)$ be the largest number of strands on a path of $G$ that ends at $v$. When $G$ is acyclic, each path is simple, $D(v)$ is finite, and

$$D(v) = 1 + \max\{D(w) : w \to v \in E\},$$

with the maximum of the empty set taken as 0. This holds because a path that ends at $v$ is $v$ alone or a path that ends at a predecessor $w$ followed by $v$. The span is $S(G) = \max_v D(v)$, and the work is $W(G) = n$.

**Lemma 1 (the queue).** Each strand enters $Q$ at most once, and a strand $v$ enters $Q$ only after all its predecessors have been removed from $Q$ in line L5.

*Proof.* Line L1 sets $indeg[v]$ to the number of predecessors of $v$. Line L11 lowers $indeg[v]$ by one for each edge $w \to v$, at the time when $w$ is removed. If each $w$ is removed at most once, $indeg[v]$ counts the predecessors of $v$ that are not yet removed, so it reaches 0 exactly once, after the last predecessor is removed. A strand with no predecessor enters in line L2 and a strand with predecessors enters in line L12 at that moment, and in both cases only once. Since a strand is removed only after it enters, and it enters once, it is removed at most once, which closes the induction over the steps of the loop. $\blacksquare$

So the order in which strands leave $Q$ is a topological order of the set $R$ of removed strands.

**Lemma 2 (the counts).** For each removed strand $u$, the value $d[u]$ right after line L7 is $D(u)$, and it does not change later.

*Proof.* By induction on the order of removal. When $u$ is removed, each predecessor $w$ of $u$ was removed earlier (Lemma 1), and by the induction hypothesis $d[w] = D(w)$ from its line L7 on. At its removal, $w$ ran line L10 for the edge $w \to u$. Line L10 is the only line that changes $d[u]$ before $u$ is removed, and each time it sets $d[u]$ to the maximum of $d[u]$ and the count of a predecessor. So when $u$ is removed, $d[u] = \max_w D(w)$, or 0 if $u$ has no predecessor. Line L7 adds one, which gives $D(u)$ by the recurrence above. After that, line L10 could change $d[u]$ only when a predecessor of $u$ is removed, and all predecessors of $u$ were removed before $u$ (Lemma 1). $\blacksquare$

**Lemma 3 (the cycle test).** $R = V$ if and only if $G$ is acyclic.

*Proof.* Suppose $G$ has a cycle $v_1 \to v_2 \to \cdots \to v_k \to v_1$. If some strand of the cycle were removed, take the first one removed, $v_i$. Its predecessor on the cycle was removed earlier by Lemma 1, which is a contradiction. So $R \ne V$. Suppose now that $R \ne V$, and take $v_0 \notin R$. At the end, $indeg[v_0] > 0$, so some predecessor $v_1$ of $v_0$ is not in $R$. In the same way $v_1$ has a predecessor $v_2 \notin R$, and so on. The graph is finite, so some strand repeats in $v_0, v_1, v_2, \ldots$, and the strands between the two copies form a cycle. $\blacksquare$

**Theorem.** If $G$ is acyclic, WORK-AND-SPAN returns $(W, S) = (n, S(G))$. If $G$ has a cycle, it reports a cycle.

*Proof.* Line L6 counts the removed strands, so at line L13, $W = |R|$. By Lemma 3, $W = n$ exactly when $G$ is acyclic, so line L13 reports a cycle exactly when there is one. If $G$ is acyclic, line L8 has taken the maximum of $d[u]$ right after line L7 over all strands, which by Lemma 2 is $\max_u D(u) = S(G)$. $\blacksquare$

**CRITICAL-PATH.** The loop runs over a topological order and updates the counts in the same way, so by the argument of Lemma 2, after the loop, $d[v] = D(v)$ for each $v$. A pointer $back[v] = u$ is set only when $d[v]$ takes the value $d[u] = D(u)$, and the last such update leaves $d[v] = D(u)$ before the increment at $v$, so $D(v) = D(back[v]) + 1$. If $v$ has a predecessor $u$, then $D(u) \ge 1 > 0$, so the test $d[u] > d[v]$ succeeds at least once and $back[v] \ne$ NIL. So $back[v] =$ NIL exactly when $v$ is a source, and then $D(v) = 1$. Starting from a strand $z$ with $D(z) = S(G)$, the walk $z, back[z], back[back[z]], \ldots$ follows edges backwards, the count drops by one at each step, and it stops at a source with count 1. So it visits $S(G)$ strands, and reversed it is a path of $G$ with $S(G)$ strands, a longest path. $\blacksquare$

**Complexity.** By Lemma 1 each strand enters and leaves $Q$ at most once, so lines L5 to L8 run at most $n$ times. The loop of line L9 looks at each edge once, when its tail is removed, so lines L10 to L12 run at most $m$ times. Line L1 takes $\Theta(n + m)$ time to read the list sizes, or $\Theta(n)$ if the sizes are stored. The total is $\Theta(n + m)$ in the worst case, and the space for $indeg$, $d$ and $Q$ is $\Theta(n)$. CRITICAL-PATH takes the time of a topological sort, $\Theta(n + m)$, plus $O(S(G))$ for the walk. $\blacksquare$
