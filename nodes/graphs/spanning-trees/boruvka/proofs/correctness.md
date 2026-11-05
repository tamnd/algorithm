---
title: Borůvka's algorithm returns a minimum spanning forest in at most floor(lg n) + 1 rounds
proves: [correctness, termination]
status: full
---

**Claim.** Let $G = (V, E)$ be a finite undirected graph with $n \ge 1$ vertices and a real weight $w(e)$ on each edge, with ties, parallel edges and self-loops allowed, and $G$ not necessarily connected. Let $\prec$ be the strict total order on $E$ given by $(w(e), \mathrm{id}(e))$ in lexicographic order, with distinct ids. Then BORŮVKA$(G, w)$ stops after at most $\lfloor \lg n \rfloor + 1$ rounds and returns a minimum spanning forest of $G$.

**Setup.** Let $c$ be the number of components of $G$. Each spanning forest of $G$ has $n - c$ edges. For $S \subseteq V$, an edge *crosses* $S$ when it has exactly one end in $S$. Let $T^*$ be the output of [Kruskal's algorithm](/kruskal/) when line L3 of that algorithm sorts the edges by $\prec$. Since $\prec$ lists the edges in non-decreasing order of weight, $T^*$ is a minimum spanning forest of $G$, by the correctness of Kruskal's algorithm.

**Lemma 1.** If $S \subseteq V$ and $e$ is the $\prec$-least edge that crosses $S$, then $e \in T^*$.

*Proof.* Let $e = (u, v)$ with $u \in S$, $v \notin S$. When Kruskal's algorithm reaches $e$, it has seen only edges $f \prec e$, and none of them crosses $S$. So each tree of its current forest has all its vertices in $S$ or all outside $S$, and $u$ and $v$ are in different trees. Kruskal's algorithm therefore adds $e$. $\square$

**Lemma 2 (invariant).** At the start of each round, $F \subseteq T^*$. In particular $F$ is a forest.

*Proof.* By induction on the rounds. Before the first round $F = \emptyset$. Assume $F \subseteq T^*$ at the start of a round. Line L3 labels the trees of $(V, F)$. For a tree $C$, after the loop of lines L5 to L8, $\mathrm{best}[C]$ is nil if no edge crosses the vertex set of $C$, and otherwise it is the $\prec$-least edge that crosses it, because the loop looks at every edge that crosses $C$ (each such edge has $\mathrm{comp}[u] \ne \mathrm{comp}[v]$ with $C$ one of the two) and keeps the least one. By Lemma 1, each edge of $A$ is in $T^*$. So $F \cup A \subseteq T^*$ after line L10. A subset of a forest is a forest. $\square$

**Lemma 3 (rounds).** Call a tree of $F$ *open* if some edge of $G$ crosses its vertex set. If a round starts with $k$ open trees, the next round starts with at most $\lfloor k/2 \rfloor$ open trees.

*Proof.* A tree that is not open is a whole component of $G$. It picks nothing, no edge reaches it, and it stays as it is and not open. Each open tree $C$ picks the edge $\mathrm{best}[C]$, which joins $C$ to a different tree $C'$, and $C'$ is open too, since that edge crosses it. So after line L10, each new tree that contains an open tree contains at least two old open trees. A new tree that is open contains at least one old open tree, because a new tree made only of closed trees is a single closed tree. So each new open tree contains at least two old open trees, the new open trees are disjoint, and there are at most $\lfloor k/2 \rfloor$ of them. $\square$

**Termination and the count.** At the start of round 1 there are $k_1 \le n$ open trees. By Lemma 3, round $r$ starts with $k_r \le n / 2^{r-1}$ open trees. A round adds an edge if and only if $k_r \ge 1$, and if $k_r \ge 1$ then $k_r \ge 2$, because an open tree has an edge to another tree of its component, and that tree is open too. So a round that adds edges needs $n / 2^{r-1} \ge 2$, that is $r \le \lg n$, so at most $\lfloor \lg n \rfloor$ rounds add edges. The round after the last of them has $A = \emptyset$ and stops the loop at line L11. In total there are at most $\lfloor \lg n \rfloor + 1$ rounds. Each round does a finite amount of work, so the algorithm stops.

**Conclusion.** In the last round $A = \emptyset$, so no edge crosses the vertex set of any tree of $F$. Then each edge of $G$ has both ends in one tree of $F$, so each component of $G$ lies inside one tree of $F$. Since $F \subseteq E$, each tree of $F$ lies inside one component of $G$. So $F$ has the components of $G$ and, by Lemma 2, is a forest: it is a spanning forest with $n - c$ edges. Lemma 2 also gives $F \subseteq T^*$, and $T^*$ has $n - c$ edges, so $F = T^*$, a minimum spanning forest. $\blacksquare$

**Why the strict order is needed.** In a triangle $a, b, c$ with three edges of weight 1, the order by weight alone allows $\mathrm{best}[a] = ab$, $\mathrm{best}[b] = bc$ and $\mathrm{best}[c] = ca$. Then $A$ is the whole triangle, which is a cycle. Lemma 1 fails for such picks, because each of the three edges is a lightest edge of its cut but they are not all in one spanning tree.
