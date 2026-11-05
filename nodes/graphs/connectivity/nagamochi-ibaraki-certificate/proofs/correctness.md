---
title: The Nagamochi-Ibaraki scan gives a certificate for k-edge connectivity
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be an undirected graph with $n$ vertices and $m$ edges, where parallel edges and self-loops are allowed. Run NI-CERTIFICATE. Write $x_1, \ldots, x_n$ for the vertices in the order line L4 picks them, and call the pass of lines L4 to L9 that scans $x_s$ *step $s$*. Write $\rho_s$ for the value $r[x_s]$ at the moment line L4 picks $x_s$. For $i \ge 1$ let $F_i$ be the set of edges with final label $i$, and $H_k = F_1 \cup \cdots \cup F_k$. For $X \subseteq V$, $d_A(X)$ is the number of edges of $A \subseteq E$ with exactly one end in $X$, and $\lambda_A(u, v) = \min\{d_A(X) : u \in X,\ v \notin X\}$.

**Lemma 0 (termination and labels).** The algorithm stops after $n$ steps. Every self-loop has label 0, and every other edge $e = \{x, y\}$ gets a label exactly once: in the step that scans the first of its ends, say $x$, and the label is the value of $r[y]$ just after line L7 increases it for $e$.

*Proof.* Each step scans one unscanned vertex, and there are $n$ of them, so line L4 always finds one and the loop of line L3 ends after $n$ steps; each step looks at finitely many edges. Line L6 skips loops, so they keep label 0 from line L2. A non-loop edge $\{x, y\}$ is treated in line L6 in a step that scans one of its ends while the other is unscanned. That happens in the step that scans the earlier end, and in no other: in the step of the later end, the earlier end is scanned. $\square$

So $r[y]$ is, at every moment, the number of edges between $y$ and the scanned vertices, for $y$ unscanned. When an edge $\{x_s, y\}$ gets label $i$, $y$ is unscanned and is scanned in a later step.

**Lemma 1.** Each $F_i$ is a forest, and $|F_i| \le n - 1$.

*Proof.* Direct each edge of $F_i$ from the end scanned first to the end scanned later. A vertex $y$ has $r[y] = i$ right after exactly one execution of line L7 for $y$, since $r[y]$ only grows by 1 at a time, so exactly one edge into $y$ has label $i$, or none. So every vertex has in-degree at most 1 in $F_i$, and every arc goes from an earlier to a later scanned vertex, so there is no directed cycle. Suppose $F_i$ had an undirected cycle $C$. Every vertex of $C$ has degree 2 in $C$; the vertex of $C$ scanned last has both its $C$ edges coming from earlier vertices, so in-degree 2, a contradiction. A forest on $n$ vertices has at most $n - 1$ edges. $\square$

Fix $i \ge 1$. Call step $s$ a *reset* if $\rho_s < i$. Step 1 is a reset, since $\rho_1 = 0$. If step $s$ is a reset, then at the start of step $s$ every unscanned vertex $v$ has $r[v] \le \rho_s < i$, by the choice in line L4.

**Lemma 2.** Let step $t$ be a reset, and let $t' > t$ be the next reset, or $t' = n + 1$ if there is none. For each $s$ with $t \le s < t'$, at the end of step $s$, every vertex of
$$A_s = \{x_t, \ldots, x_s\} \cup \{v \text{ unscanned} : r[v] \ge i\}$$
is joined to $x_t$ by a path of edges that have label $i$ at that moment.

*Proof.* By induction on $s$. Consider step $s$, and assume the claim for $s - 1$ if $s > t$. First, $x_s$ is joined to $x_t$: for $s = t$ trivially, and for $s > t$ step $s$ is not a reset, so $\rho_s \ge i$, and $x_s$ was an unscanned vertex with $r \ge i$ at the end of step $s - 1$, hence in $A_{s-1}$, joined to $x_t$ by the induction hypothesis. The vertices $x_t, \ldots, x_{s-1}$ are joined to $x_t$ by the induction hypothesis, and labels never change once set. Now let $v$ be unscanned with $r[v] \ge i$ at the end of step $s$. If $r[v] \ge i$ already held at the start of step $s$, then $s > t$, because at the start of a reset no unscanned vertex has $r \ge i$, and $v \in A_{s-1}$, joined to $x_t$. Otherwise $r[v]$ took the value $i$ during step $s$, at line L7 for some edge $e = \{x_s, v\}$, and line L8 gave $e$ label $i$; so $v$ is joined to $x_s$, hence to $x_t$. $\square$

**Lemma 3.** If an edge $e = \{x, y\}$ has label $j > i$, then $x$ and $y$ are joined by a path in $F_i$.

*Proof.* By Lemma 0, $e$ got its label in the step $s$ that scans $x = x_s$, say, and $r[y]$ went from $j - 1 \ge i$ to $j$ for $e$. Two cases.

If $r[y] < i$ at the start of step $s$, then $r[y]$ took the value $i$ during step $s$, through an edge $\{x_s, y\}$ that got label $i$. That edge joins $x$ and $y$ in $F_i$.

If $r[y] \ge i$ at the start of step $s$, then $\rho_s \ge r[y] \ge i$ by the choice of $x_s$ in line L4, so step $s$ is not a reset. Let $t < s$ be the last reset before it. Both $x_s$ and $y$ were unscanned with $r \ge i$ at the end of step $s - 1$, so both lie in $A_{s-1}$, and Lemma 2 joins both to $x_t$ by edges of label $i$. So $x$ and $y$ are joined in $F_i$. $\square$

**Lemma 4 (cut lemma).** Let $k \ge 1$ and $X \subseteq V$. Then $d_{H_k}(X) \ge \min(k, d_E(X))$.

*Proof.* If every edge of $E$ that crosses $X$ is in $H_k$, then $d_{H_k}(X) = d_E(X)$. Otherwise some edge $e = \{x, y\}$ crosses $X$ and is not in $H_k$. It is not a loop, since a loop crosses no cut, so its label is some $j > k$. For each $i \le k$, Lemma 3 gives a path from $x$ to $y$ in $F_i$. That path starts in $X$ and ends outside, so one of its edges crosses $X$. The forests $F_1, \ldots, F_k$ are disjoint, because each edge has one label, so these are $k$ distinct edges of $H_k$, and $d_{H_k}(X) \ge k$. $\square$

**Theorem.** For every $k \ge 1$, $|H_k| \le k(n - 1)$, and for all $u \ne v$,
$$\min(k, \lambda_{H_k}(u, v)) = \min(k, \lambda_E(u, v)).$$
In particular, $H_k$ is $k$-edge-connected if and only if $G$ is.

*Proof.* The size bound follows from Lemma 1. Since $H_k \subseteq E$, $d_{H_k}(X) \le d_E(X)$ for every $X$, so $\lambda_{H_k}(u, v) \le \lambda_E(u, v)$. For the other direction, take $X$ with $u \in X$, $v \notin X$ and $d_{H_k}(X) = \lambda_{H_k}(u, v)$. By Lemma 4, $\lambda_{H_k}(u, v) = d_{H_k}(X) \ge \min(k, d_E(X)) \ge \min(k, \lambda_E(u, v))$. Taking the minimum with $k$ on both sides gives the equality. A graph with at least two vertices is $k$-edge-connected exactly when $\lambda(u, v) \ge k$ for all pairs, and $H_k$ has the same vertex set as $G$, so the last claim follows. Line L10 returns exactly $H_k$, and by Lemma 0 the algorithm terminates. $\blacksquare$

The vertex version, that $H_k$ is $k$-vertex-connected when $G$ is simple and $k$-vertex-connected, is proved by Nagamochi and Ibaraki (1992) and is not reproved here. The page gives an example with parallel edges where it fails.
