---
title: Triangle listing by degree ordering reports each triangle exactly once
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a simple undirected graph, and let $r(v) = (d(v), v)$ with the lexicographic order. Write $u \prec v$ when $r(u) < r(v)$. Since the second entries are the distinct vertex numbers, $\prec$ is a strict total order on $V$.

**Lemma 1 (the oriented graph).** After line L2, for each edge $\{v, w\} \in E$ exactly one of $w \in \mathrm{Out}[v]$ and $v \in \mathrm{Out}[w]$ holds, namely the one from the $\prec$-smaller end. No other pair appears in an out-list, and no out-list holds a vertex twice.

*Proof.* Line L2 puts $w$ in $\mathrm{Out}[v]$ exactly when $w$ is a neighbour of $v$ and $v \prec w$. Since $\prec$ is a strict total order and $v \ne w$, exactly one of $v \prec w$ and $w \prec v$ holds. The graph has no repeated edges, so a neighbour occurs once in $\mathrm{Adj}[v]$. $\square$

We write $v \to w$ for $w \in \mathrm{Out}[v]$. By Lemma 1, $v \to w$ if and only if $\{v, w\} \in E$ and $v \prec w$.

**Lemma 2 (marks).** At the start of each iteration of line L5, every mark is false. During lines L7 to L9 of the iteration for $u$, $\mathrm{mark}[x]$ is true if and only if $u \to x$.

*Proof.* By induction on the iterations. Before the first one, line L3 sets every mark to false. In the iteration for $u$, line L6 sets $\mathrm{mark}[x]$ to true for exactly the $x$ with $u \to x$, and lines L7 to L9 do not change any mark. So the second claim holds. Line L10 sets the same marks back to false, so every mark is false at the start of the next iteration. $\square$

**Lemma 3 (soundness).** Each set appended at line L9 is a triangle $\{u, v, w\}$ with $u \prec v \prec w$.

*Proof.* At line L9 we have $u \to v$ (line L7), $v \to w$ (line L8), and $\mathrm{mark}[w]$ true, so $u \to w$ by Lemma 2. By Lemma 1, the three pairs $\{u, v\}$, $\{v, w\}$ and $\{u, w\}$ are edges, and $u \prec v \prec w$. Since $\prec$ is strict, the three vertices are distinct. $\square$

**Lemma 4 (completeness and uniqueness).** Each triangle of $G$ is appended exactly once.

*Proof.* Let $\{a, b, c\}$ be a triangle, named so that $a \prec b \prec c$. By Lemma 1, $a \to b$, $a \to c$ and $b \to c$.

*At least once.* In the iteration for $u = a$, line L7 reaches $v = b$ because $a \to b$, line L8 reaches $w = c$ because $b \to c$, and $\mathrm{mark}[c]$ is true by Lemma 2 because $a \to c$. So line L9 appends $\{a, b, c\}$.

*At most once.* Suppose line L9 appends $\{a, b, c\}$ at the step $(u, v, w)$. By Lemma 3, $\{u, v, w\} = \{a, b, c\}$ and $u \prec v \prec w$. The order $\prec$ is total, so the only way to list the three vertices in increasing order is $(a, b, c)$. Hence $(u, v, w) = (a, b, c)$. Each value of $u$ is taken once at line L5, each $v \in \mathrm{Out}[u]$ once at line L7, and each $w \in \mathrm{Out}[v]$ once at line L8 (Lemma 1, no repeats), so the step $(a, b, c)$ happens once. $\square$

**Theorem.** TRIANGLES-BY-DEGREE$(G)$ stops, and the list $T$ it returns holds each triangle of $G$ exactly once and nothing else.

*Proof.* Termination: every loop runs over a finite list that the loop body does not change, so the algorithm stops after at most $n + \sum_u (2d^+(u) + \sum_{v \in \mathrm{Out}[u]} d^+(v))$ steps of the loops, a finite number. By Lemma 3, every entry of $T$ is a triangle, and by Lemma 4, every triangle is an entry of $T$ exactly once. $\blacksquare$

**The cost bound.** For an arc $v \to w$, $r(v) < r(w)$ gives $d(v) \le d(w)$. So every out-neighbour of $v$ has degree at least $d(v)$. If $k$ vertices have degree at least $d(v) \ge 1$, then $k\, d(v) \le \sum_x d(x) = 2m$, and the out-neighbours of $v$ are among these $k$ vertices, so $d^+(v) \le k \le 2m/d(v)$. Hence $d^+(v) \le \min(d(v), 2m/d(v)) \le \sqrt{2m}$ for $d(v) \ge 1$, and $d^+(v) = 0$ when $d(v) = 0$. The work of lines L7 to L9 over the whole run is $\sum_u \sum_{v : u \to v} (1 + d^+(v)) \le m + m\sqrt{2m}$, so the time is $O(n + m^{3/2})$.
