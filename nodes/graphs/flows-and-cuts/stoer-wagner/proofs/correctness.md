---
title: The Stoer-Wagner algorithm returns a global minimum cut
proves: [correctness]
status: full
---

**Setting.** $G = (V, E)$ is an undirected graph with $n \ge 2$ vertices and weights $w \ge 0$; parallel edges are summed into one weight $w(u, v)$ and self-loops are ignored. For disjoint sets $X$, $Y$, $w(X, Y)$ is the total weight of the edges with one end in $X$ and the other in $Y$, and $w(X, v) = w(X, \{v\})$. A cut is a set $C$ with $\emptyset \ne C \subsetneq V$, with weight $w(C) = w(C, V \setminus C)$. It *separates* $x$ and $y$ if exactly one of them is in $C$.

**Lemma 1 (keys).** In MINIMUM-CUT-PHASE, let $v_1, \ldots, v_k$ be the order of line L9, with $v_1 = a$, and let $A_i = \{v_1, \ldots, v_{i-1}\}$. When $v_i$ is chosen, $\mathrm{key}(v_i) = w(A_i, v_i)$, and $v_i$ maximizes $w(A_i, x)$ over all $x \notin A_i$.

*Proof.* By induction: line L7 sets $\mathrm{key}(x) = w(\{v_1\}, x)$, and line L10 adds $w(v_i, x)$ to every $x$ outside $A_{i+1}$ after $v_i$ is chosen. Line L9 takes the largest key. $\square$

**Lemma 2 (cut of the phase).** Let $s = v_{k-1}$ and $t = v_k$. Then $w(A_k, t) = w(V \setminus \{t\}, t)$ is the weight of a minimum cut of $G$ among the cuts that separate $s$ and $t$.

*Proof.* The set $\{t\}$ is a cut that separates $s$ and $t$, and its weight is $w(A_k, t)$. Let $C$ be any cut that separates $s$ and $t$. We show $w(A_k, t) \le w(C)$.

Call $v_i$ with $i \ge 2$ *active* if $v_i$ and $v_{i-1}$ are on different sides of $C$. Since $s$ and $t$ are on different sides, $t$ is active. For each $i$ let $C_i$ be the set of edges of $C$, that is, edges between $C$ and $V \setminus C$, that have both ends in $A_i \cup \{v_i\}$, and $w(C_i)$ their weight. We claim that $w(A_i, v_i) \le w(C_i)$ for every active $v_i$.

*First active vertex.* Let $v_i$ be the first active vertex. Then $v_1, \ldots, v_{i-1}$ are all on one side of $C$, and $v_i$ is on the other, so every edge between $A_i$ and $v_i$ is in $C_i$: $w(A_i, v_i) \le w(C_i)$.

*Induction step.* Let $v_i$ be active, and let $v_j$, $j < i$, be the active vertex before it. By the hypothesis, $w(A_j, v_j) \le w(C_j)$. Then

$$w(A_i, v_i) = w(A_j, v_i) + w(A_i \setminus A_j, v_i) \le w(A_j, v_j) + w(A_i \setminus A_j, v_i) \le w(C_j) + w(A_i \setminus A_j, v_i).$$

The first inequality holds by Lemma 1: when $v_j$ was chosen, $v_i$ was also outside $A_j$, so $w(A_j, v_j) \ge w(A_j, v_i)$. The vertices $v_j, \ldots, v_{i-1}$, which form $A_i \setminus A_j$, are all on the side of $v_j$, because none of $v_{j+1}, \ldots, v_{i-1}$ is active, and $v_i$ is on the other side because it is active. So every edge between $A_i \setminus A_j$ and $v_i$ is in $C_i$. These edges are not in $C_j$, because $v_i \notin A_j \cup \{v_j\}$. The edges of $C_j$ are also in $C_i$. Since weights are nonnegative, $w(C_j) + w(A_i \setminus A_j, v_i) \le w(C_i)$, which proves the claim.

Apply the claim to $t = v_k$, which is active: $w(A_k, t) \le w(C_k) = w(C)$, since $A_k \cup \{t\} = V$. $\square$

**Lemma 3 (merging).** Let $G'$ be the graph obtained by merging $t$ into $s$. The cuts of $G'$ correspond exactly, with the same weights, to the cuts of $G$ that do not separate $s$ and $t$.

*Proof.* A cut $C'$ of $G'$ corresponds to the cut $C$ of $G$ in which the merged vertex is replaced by both $s$ and $t$. An edge of $G'$ from the merged vertex to $x$ has weight $w(s, x) + w(t, x)$, so it crosses $C'$ exactly when the two edges $sx$, $tx$ cross $C$; the edge $st$ disappears, and it does not cross $C$. Every cut of $G$ with $s$ and $t$ on one side arises in this way. $\square$

**Theorem.** STOER-WAGNER returns the weight $\lambda$ of a global minimum cut of $G$, and a set $S$, the group of the last vertex of the best phase, with $w(S) = \lambda$.

*Proof.* By induction on $n$. Each value recorded at line L4 is the weight of a real cut of the original graph: the group of $t$ against the rest, by Lemma 3 applied to all earlier merges. So the result is at least $\lambda$, and it is the weight of the returned $S$. For $n = 2$ there is one phase, and the only cut is $\{t\}$, which the phase records. For $n > 2$, let $C$ be a minimum cut of $G$, and let $s$, $t$ be the last two vertices of the first phase. If $C$ separates $s$ and $t$, the phase records at most $w(C) = \lambda$ by Lemma 2. If not, $C$ corresponds to a cut of the merged graph $G'$ of the same weight by Lemma 3, so the minimum cut of $G'$ is $\lambda$, and by the induction hypothesis the remaining phases, which form the algorithm run on $G'$, record a cut of weight $\lambda$. In both cases the smallest recorded value is $\lambda$. $\blacksquare$
