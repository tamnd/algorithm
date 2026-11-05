---
title: The chordal coloring algorithm is correct and optimal
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a finite simple undirected graph. Maximum cardinality search visits the vertices one at a time and always visits next an unvisited vertex with the largest number of visited neighbors. Let $\sigma$ be its visit order and $t(v)$ the step at which $v$ is visited. For each $v$, $\mathrm{Earlier}(v) = \{ w \in N(v) : t(w) < t(v) \}$, and if it is not empty, $p(v)$ is its element with the largest $t$.

Termination is clear: maximum cardinality search makes $n$ steps, and lines L2 to L7 are loops over the vertices, their adjacency lists and the recorded requests. We prove that the answer is right.

**Lemma 1 (the search property).** If $t(a) < t(b) < t(c)$, $ac \in E$ and $ab \notin E$, then there is a vertex $d$ with $t(d) < t(b)$, $db \in E$ and $dc \notin E$.

*Proof.* Let $S$ be the set of vertices visited before $b$. Then $a \in S$ and $c \notin S$. When $b$ was chosen, $|N(b) \cap S| \ge |N(c) \cap S|$. The vertex $a$ is in $N(c) \cap S$ but not in $N(b)$. If $N(b) \cap S \subseteq N(c)$, then $N(c) \cap S$ would contain $N(b) \cap S$ and also $a$, so it would be larger. So some $d \in N(b) \cap S$ has $d \notin N(c)$. $\square$

**Lemma 2.** If $G$ is chordal, then $\mathrm{Earlier}(v)$ is a clique for every vertex $v$.

*Proof.* Suppose some $\mathrm{Earlier}(v)$ contains two non-adjacent vertices $x, y$. We call a path $P = p_0 p_1 \cdots p_L$ *good* if $L \ge 2$, $P$ is an induced path of $G$ (no edges between its vertices besides $p_i p_{i+1}$), and every inner vertex $p_1, \ldots, p_{L-1}$ has a larger $t$ than both ends $p_0$ and $p_L$. The path $x\, v\, y$ is good: $xy \notin E$, and $t(v) > t(x), t(y)$. For a good path let $\Phi(P) = t(p_0) + t(p_L)$. We show that every good path $P$ gives a good path $P'$ with $\Phi(P') < \Phi(P)$. This is impossible, since $\Phi$ takes only finitely many values, so the lemma follows.

Let $P$ be good, and name its ends so that $e = p_0$ has the smaller time and $f = p_L$ the larger: $t(e) < t(f)$. Let $q = p_1$, the inner neighbor of $e$. Then $t(e) < t(f) < t(q)$, $eq \in E$, and $ef \notin E$ because $P$ is induced and $L \ge 2$. Lemma 1 with $a = e$, $b = f$, $c = q$ gives a vertex $d$ with $t(d) < t(f)$, $df \in E$ and $dq \notin E$.

The vertex $d$ is not on $P$: it is not $f$, since $df \in E$; it is not $e$, since $ef \notin E$; and it is not an inner vertex, since those have $t$ larger than $t(f) > t(d)$.

Let $J = \{ j : d p_j \in E \}$; then $L \in J$ and $1 \notin J$. Suppose $J$ has two elements $i < i'$ with no element of $J$ strictly between them and $i' \ge i + 2$. Then $d, p_i, p_{i+1}, \ldots, p_{i'}, d$ is a cycle of length $i' - i + 2 \ge 4$. It has no chord: $P$ is induced, and $d$ is not adjacent to $p_{i+1}, \ldots, p_{i'-1}$. This contradicts chordality. So $J$ is a set of consecutive integers $\{r, r+1, \ldots, L\}$, and since $1 \notin J$, $r \ge 2$.

Let $P' = p_0 p_1 \cdots p_r\, d$. It has at least 3 vertices, since $r \ge 2$. It is induced: its part $p_0 \cdots p_r$ is part of $P$, and $d$ is adjacent to $p_r$ and to no $p_j$ with $j < r$. Its inner vertices are $p_1, \ldots, p_r$. Each of them is an inner vertex of $P$ or equals $f = p_L$, so its time is at least $t(f)$, which is larger than $t(e)$ and larger than $t(d)$; inner vertices of $P$ other than $p_L$ have time larger than $t(f)$. So $P'$ is good, with the ends $e$ and $d$, and $\Phi(P') = t(e) + t(d) < t(e) + t(f) = \Phi(P)$. $\square$

**Lemma 3 (the check of lines L2 to L5).** Every $\mathrm{Earlier}(v)$ is a clique if and only if, for every $v$ with $\mathrm{Earlier}(v) \ne \emptyset$, $\mathrm{Earlier}(v) \setminus \{p(v)\} \subseteq N(p(v))$.

*Proof.* If $\mathrm{Earlier}(v)$ is a clique, $p(v)$ is adjacent to its other elements. Conversely, assume the condition, and show by induction on $t(v)$ that $\mathrm{Earlier}(v)$ is a clique. Let $w_1 \ne w_2$ be in $\mathrm{Earlier}(v)$ and $p = p(v)$. If one of them is $p$, the condition gives $w_1 w_2 \in E$. Otherwise both are adjacent to $p$ and have $t(w_i) < t(p)$, by the choice of $p$, so both lie in $\mathrm{Earlier}(p)$. As $t(p) < t(v)$, the induction hypothesis says that $\mathrm{Earlier}(p)$ is a clique, so $w_1 w_2 \in E$. $\square$

Line L5 tests exactly the condition of Lemma 3: for each $u$ it marks $N(u)$ and checks every $w$ recorded for $u$, and the recorded pairs are $(p(v), w)$ for $w \in \mathrm{Earlier}(v) \setminus \{p(v)\}$.

**Lemma 4.** If every $\mathrm{Earlier}(v)$ is a clique, then $G$ is chordal.

*Proof.* Let $C$ be a cycle of length at least 4, and $v$ its vertex with the largest $t$. The two neighbors of $v$ on $C$ have smaller times, so they lie in $\mathrm{Earlier}(v)$ and are adjacent. They are not consecutive on $C$, because $C$ has length at least 4, so this edge is a chord. $\square$

**The answer NOT CHORDAL.** If $G$ is chordal, Lemma 2 and Lemma 3 show that line L5 finds no failure. If line L5 finds no failure, Lemma 3 and Lemma 4 show that $G$ is chordal. So the algorithm returns NOT CHORDAL exactly when $G$ is not chordal.

**The coloring.** Assume $G$ is chordal, so each $\mathrm{Earlier}(v)$ is a clique. Lines L6 and L7 color the vertices in the order $\sigma$, and when $v$ is colored, its colored neighbors are exactly $\mathrm{Earlier}(v)$. The colors of these $|\mathrm{Earlier}(v)|$ vertices exclude at most $|\mathrm{Earlier}(v)|$ values, so the smallest free value $c(v)$ is at most $|\mathrm{Earlier}(v)| + 1$, and it differs from the color of each vertex of $\mathrm{Earlier}(v)$. Every edge $vw$ with $t(w) < t(v)$ has $w \in \mathrm{Earlier}(v)$, so the coloring is proper. The set $\{v\} \cup \mathrm{Earlier}(v)$ is a clique of size $|\mathrm{Earlier}(v)| + 1$, so

$$\max_v c(v) \le \max_v \big(|\mathrm{Earlier}(v)| + 1\big) \le \omega(G) \le \chi(G).$$

A proper coloring uses at least $\chi(G)$ colors, so the coloring uses exactly $\chi(G) = \omega(G)$ colors and is optimal. $\blacksquare$
