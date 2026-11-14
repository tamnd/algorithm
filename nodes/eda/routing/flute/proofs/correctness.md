---
title: The table lookup of FLUTE gives a rectilinear Steiner minimal tree for small nets, and net breaking gives a valid tree
proves: [correctness, linear wirelength, pareto pruning, vector recursion, net breaking]
status: full
---

Let $P$ be a net of $n$ pins with position sequence $\pi$, sorted coordinates $x_1 \le \cdots \le x_n$ and $y_1 \le \cdots \le y_n$, and gaps $g = (h_1, \ldots, h_{n-1}, v_1, \ldots, v_{n-1}) \ge 0$. The *grid graph* $\Gamma_\pi$ has the nodes $(i, j)$ for $0 \le i, j < n$, and an edge between nodes that differ by one in one index. Pin $k$ in $x$ order is the node $(k, \pi(k))$. Under the gaps $g$, the horizontal edge between columns $i$ and $i + 1$ has length $h_{i+1}$, and the vertical edge between rows $j$ and $j + 1$ has length $v_{j+1}$, with indices from 1 for the gaps.

**Lemma 1 (lengths are linear in the gaps).** For every subgraph $T$ of $\Gamma_\pi$ there is a vector $w(T) \in \mathbb{Z}_{\ge 0}^{2(n-1)}$ that does not depend on $g$, such that the length of $T$ under $g$ is $w(T) \cdot g$. A grid tree for $\pi$ is a tree for every net with the sequence $\pi$.

*Proof.* Let $w(T)_i$ be the number of horizontal edges of $T$ between columns $i - 1$ and $i$, and $w(T)_{n-1+j}$ the number of vertical edges between rows $j - 1$ and $j$. Each edge contributes its gap once, so the length is $w(T) \cdot g$. The nodes that are pins depend only on $\pi$, so the same subgraph spans the pins of every net with this sequence. $\square$

**Lemma 2 (the optimum is a minimum of linear forms).** Let $W_\pi$ be the set of vectors $w(T)$ of the trees $T$ in $\Gamma_\pi$ that contain all pin nodes. Then the length of a rectilinear Steiner minimal tree of $P$ is $\min_{w \in W_\pi} w \cdot g$.

*Proof.* First let all $x$ values be distinct and all $y$ values be distinct. Each tree in $\Gamma_\pi$ maps to a rectilinear Steiner tree of $P$ with the same length, by placing node $(i, j)$ at $(x_{i+1}, y_{j+1})$, so the minimum is at least the optimum. By Hanan's theorem there is an optimal tree whose Steiner points lie on the grid of lines through the pins, and whose edges can be drawn as L shapes along these lines without changing the length. Split its edges at every grid point they pass. The result is a connected subgraph of the drawn grid that contains the pins, of the same length, and a spanning tree of it is a tree in $\Gamma_\pi$ that is no longer. So the minimum is at most the optimum.

If some coordinates are equal, some gaps are 0. The optimal length is a continuous function of the coordinates, since moving one pin by $\delta$ in L1 changes it by at most $\delta$. Both sides of the formula are continuous in $g$ and agree for all gaps that are positive, so they agree in the limit. $\square$

**Lemma 3 (pruning is safe).** Let $W$ be a finite set of vectors and let $W'$ be the set of its Pareto minima, the vectors $a \in W$ such that no other $b \in W$ has $b \le a$ in every entry. Then $\min_{a \in W'} a \cdot g = \min_{a \in W} a \cdot g$ for every $g \ge 0$.

*Proof.* Let $a \in W$. The relation "at most in every entry" is a partial order on the finite set $W$, so there is a minimal element $b \le a$, and $b \in W'$. Since $g \ge 0$, $b \cdot g \le a \cdot g$. So the minimum over $W'$ is at most the minimum over $W$, and it is not less, since $W' \subseteq W$. $\square$

**Lemma 4 (the vector recursion).** For a set $X$ of pins and a node $v$, let $F(X, v)$ be the set computed by the recursion

- $F(\{k\}, v) = \{\mathrm{box}(k, v)\}$, the vector of the gaps between pin $k$ and $v$,
- $G(X, u) = \mathrm{Pareto}\{a + b : a \in F(X', u),\ b \in F(X \setminus X', u),\ \emptyset \ne X' \subsetneq X\}$,
- $F(X, v) = \mathrm{Pareto}\{a + \mathrm{box}(u, v) : u \text{ a node},\ a \in G(X, u)\}$.

Then for every $g \ge 0$, $\min_{a \in F(X, v)} a \cdot g$ is the length of a shortest Steiner tree of $X \cup \{v\}$ in $\Gamma_\pi$ under $g$.

*Proof.* Fix $g \ge 0$ and write $c(A) = \min_{a \in A} a \cdot g$ for a set of vectors $A$. The map $a \mapsto a \cdot g$ is linear, so $c(\{a + b : a \in A, b \in B\}) = c(A) + c(B)$ and $c(A \cup B) = \min(c(A), c(B))$, and $c(\mathrm{Pareto}(A)) = c(A)$ by Lemma 3. The vector $\mathrm{box}(u, v)$ has a 1 for each gap between the columns of $u$ and $v$ and between their rows, so $\mathrm{box}(u, v) \cdot g$ is the shortest path length from $u$ to $v$ in $\Gamma_\pi$. Applying $c$ to the recursion therefore gives exactly the Dreyfus-Wagner recursion for the Steiner tree problem in the graph $\Gamma_\pi$ with these lengths, which computes shortest Steiner trees. The restriction that $X'$ contains the lowest pin of $X$, used by the implementation, only skips splits that are the same as another split with the parts exchanged. $\square$

**Theorem 1 (lookup gives the optimum).** For a net with $2 \le n \le D$ pins, the least $a \cdot g$ over the table entry of $\pi$ is the length of a rectilinear Steiner minimal tree, and the tree stored with it, placed on the coordinates, has this length.

*Proof.* The entry is $F(\text{all pins but the last}, \text{the last pin})$, so by Lemma 4 its least value is the shortest Steiner tree of all pins in $\Gamma_\pi$, which is $\min_{w \in W_\pi} w \cdot g$. By Lemma 2 this is the optimal length. Each vector in the entry comes from a tree in $\Gamma_\pi$ whose branch nodes are recorded with it. Placing these nodes at their coordinates and joining the pins and these points by their L1 minimum spanning tree gives a tree no longer than the grid tree, since the grid tree is a connected graph on these points whose edges are at least the L1 distances of their ends. For $n \le 1$ the length is 0. $\square$

**Lemma 5 (net breaking).** If $T_1$ is a tree that spans $P_1$ and $T_2$ is a tree that spans $P_2$, with $P_1 \cup P_2 = P$, $P_1 \cap P_2 = \{p\}$, and the Steiner points of the two trees kept apart, then $T_1 \cup T_2$ is a rectilinear Steiner tree of $P$ of length $|T_1| + |T_2|$.

*Proof.* The union is connected, since both trees contain $p$. Its number of edges is $(|V_1| - 1) + (|V_2| - 1) = |V_1 \cup V_2| - 1$, since the vertex sets meet only in $p$. A connected graph with one edge fewer than vertices is a tree. Its length is the sum. Two drawn wires may overlap in the plane, in which case the drawn length is at most the sum. $\square$

For $n > D$ the median split gives two nets of $\lfloor n/2 \rfloor + 1$ and $\lceil n/2 \rceil$ pins, both less than $n$ when $n \ge 3$, so the recursion ends, and by Lemma 5 and induction the output is a valid tree. No bound on its ratio to the optimum is claimed. $\square$
