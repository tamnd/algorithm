---
title: Proof of membership for Karp's 21 problems and of five of his reductions
proves: [statement]
status: partial
---

This page proves that each of the 21 problems is in NP and proves five of Karp's twenty reductions in full: SAT to clique, clique to node cover, exact cover to knapsack, knapsack to partition, and partition to max cut. The other fifteen reductions are proved on the pages of the problems, on [Karp's reduction tree](/karp-21-np-complete/), and in Karp (1972), pages 97 to 100, where each reduction is given only as a map and the checks are left to the reader. The proof of the [Cook-Levin theorem](/cook-levin-theorem/) gives the root: SAT is NP-complete. All reductions are polynomial-time many-one (Karp) reductions, and all numbers are in binary.

## Membership in NP

Karp (1972, page 97) calls membership in NP clear. For each problem, the certificate below has length polynomial in the input, and the check runs in polynomial time on a deterministic multitape Turing machine.

- SAT and 3-SAT: an assignment; evaluate each clause.
- 0-1 integer programming: a vector $x \in \{0,1\}^n$; compute $Cx$ and compare with $d$. The entries of $Cx$ have at most $\log_2 n$ more bits than the entries of $C$.
- Clique: a set of $k$ vertices; check every pair. Node cover and feedback node set: a set of at most $l$ or $k$ vertices; check every edge, or check by depth-first search that the digraph without the set has no cycle.
- Set packing, set covering, exact cover, hitting set: the chosen sets (or the set $W$); count the elements.
- Feedback arc set: a set of at most $k$ arcs; check that the rest is acyclic.
- Directed and undirected Hamilton circuit: an ordering of the vertices; check $n$ arcs or edges.
- Chromatic number and clique cover: a map from vertices to $\{1, \ldots, k\}$; check each edge, or each class for being a clique.
- Steiner tree: a set of edges; check that it is a tree, that it contains $R$, and that its weight is at most $k$.
- 3-dimensional matching: the set $W$; check that $|W| = |T|$ and that no two triples agree in a coordinate.
- Knapsack and partition: a subset of the numbers; add them.
- Job sequencing: a permutation $\pi$; compute the finishing times and the total penalty of the late jobs.
- Max cut: a set $S$ of vertices; add the weights of the edges with one end in $S$.

## SAT to clique

Let the formula have clauses $C_1, \ldots, C_p$ and $L$ literal occurrences in total.

The map. The graph has a vertex $\langle \sigma, i\rangle$ for each literal $\sigma$ in clause $C_i$. Two vertices $\langle \sigma, i\rangle$ and $\langle \delta, j\rangle$ are joined when $i \ne j$ and $\sigma \ne \bar\delta$. Set $k = p$.

Cost. $L$ vertices, at most $\binom{L}{2}$ edges, and time $O(L^2)$.

If the formula is satisfiable: fix a satisfying assignment and pick one true literal $\sigma_i$ in each clause. The vertices $\langle \sigma_i, i\rangle$ lie in different clauses, and no two are complementary because both would be true. So every pair is joined, and they form a clique of size $p$.

If the graph has a clique $K$ of size $p$: vertices of the same clause are never joined, so $K$ has exactly one vertex in each clause. No two literals in $K$ are complementary, because complementary vertices are not joined. So there is an assignment that makes every literal of $K$ true (set the remaining variables to 0), and it satisfies every clause.

Example. For $\varphi = (x_1 \lor x_2) \land (\lnot x_1 \lor x_2 \lor x_3) \land (\lnot x_2 \lor \lnot x_3)$, the graph has 7 vertices and 12 edges, and $k = 3$. A script found 3 satisfying assignments, $(x_1, x_2, x_3) \in \{(0,1,0), (1,0,1), (1,1,0)\}$, and 4 cliques of size 3. The assignment $(0, 1, 0)$ gives the clique $\{\langle x_2, 1\rangle, \langle x_2, 2\rangle, \langle \lnot x_3, 3\rangle\}$. The clique $\{\langle x_1, 1\rangle, \langle x_3, 2\rangle, \langle \lnot x_2, 3\rangle\}$ gives $x_1 = 1$, $x_2 = 0$, $x_3 = 1$, which satisfies $\varphi$. A script also ran the map on 300 random formulas (seed 1972, up to 4 variables and 4 clauses) and compared both sides by brute force: no mismatch.

## Clique to node cover

The map. $(G, k) \mapsto (\bar G, l)$, where $\bar G$ has the same vertex set $N$ and joins two vertices exactly when $G$ does not, and $l = |N| - k$. Cost: $O(|N|^2)$.

Both directions. For any set $K \subseteq N$: $K$ is a clique of $G$ if and only if no edge of $\bar G$ has both ends in $K$, if and only if every edge of $\bar G$ has an end in $N \setminus K$, that is, $N \setminus K$ is a node cover of $\bar G$. Since $|N \setminus K| = |N| - |K|$, a clique of size $k$ gives a node cover of size $l$, and any node cover $D$ of size $l$ gives the clique $N \setminus D$ of size $k$.

Example. The complement of the graph above has 9 edges, and $l = 7 - 3 = 4$. The script found 4 node covers of size 4, and they are exactly the complements of the 4 cliques.

## Exact cover to knapsack

Karp's knapsack is the subset sum form: given integers $a_1, \ldots, a_r$ and $b$, is there a 0-1 vector $x$ with $\sum_j a_j x_j = b$?

The map. Let the universe be $\{u_1, \ldots, u_t\}$ and the family be $S_1, \ldots, S_r$. Let $d = r + 1$, $a_j = \sum_{i : u_i \in S_j} d^{\,i-1}$ and $b = \sum_{i=1}^{t} d^{\,i-1} = (d^t - 1)/(d - 1)$.

Cost. Each number has $t$ digits in base $d$, so $O(t \log r)$ bits, and there are $r + 1$ numbers.

Both directions. Write the sum of any subfamily $J$ in base $d$. Digit $i - 1$ of $\sum_{j \in J} a_j$ is the number of sets in $J$ that contain $u_i$, which is at most $r < d$, so no carry occurs. Hence $\sum_{j \in J} a_j = b$ if and only if every digit is 1, that is, every element lies in exactly one set of $J$. So $J$ is an exact cover if and only if its numbers sum to $b$.

Example. Universe $\{1, 2, 3, 4\}$, family $\{1, 2\}, \{3, 4\}, \{2, 3\}, \{1\}, \{4\}$. Then $d = 6$, the numbers are $7, 252, 42, 1, 216$, and $b = 259$. The script found two subsets with sum 259: $7 + 252$ (the sets $\{1,2\}, \{3,4\}$) and $42 + 1 + 216$ (the sets $\{2,3\}, \{1\}, \{4\}$), which are the two exact covers.

## Knapsack to partition

The map. Given $a_1, \ldots, a_r$ and $b$ with $A = \sum_i a_i$: if $b > A$, output a fixed no-instance such as $(1, 2)$. Otherwise output the $r + 2$ numbers $c_i = a_i$ for $i \le r$, $c_{r+1} = b + 1$ and $c_{r+2} = A + 1 - b$. Cost: linear.

The total is $2A + 2$, so a partition puts $A + 1$ on each side.

If some $J \subseteq \{1, \ldots, r\}$ has $\sum_{J} a_j = b$: the side $J \cup \{r+2\}$ has sum $b + A + 1 - b = A + 1$.

If the numbers $c$ have a partition: take either side of an arbitrary partition. Since $c_{r+1} + c_{r+2} = A + 2 > A + 1$, the two numbers lie on different sides. Let $I \subseteq \{1, \ldots, r\}$ be the other numbers on the side of $c_{r+2}$. Then $\sum_I a_i + A + 1 - b = A + 1$, so $\sum_I a_i = b$.

Example. For $a = (3, 5, 7, 9)$ and $b = 12$, the map gives $(3, 5, 7, 9, 13, 13)$ with total 50. The subset $\{3, 9\}$ maps to the side $\{3, 9, 13\}$ with sum 25. For $a = (3, 5, 7)$ and $b = 11$, which has no solution, the map gives $(3, 5, 7, 12, 5)$ with total 32, and the script found no side with sum 16. On 500 random instances (seed 1972, up to 6 numbers at most 12), the script found no mismatch.

## Partition to max cut

The map. Given $c_1, \ldots, c_s$ with total $C$, build the complete graph on $\{1, \ldots, s\}$ with $w(\{i, j\}) = c_i c_j$, and set $W = \lceil C^2/4 \rceil$. The question is whether some cut has weight at least $W$. Cost: $\binom{s}{2}$ weights of at most twice the bit length of the largest $c_i$.

Karp's paper prints $W = \lceil \frac14 \sum c_i^2 \rceil$. That threshold is wrong: for $c = (1, 1, 4)$ there is no partition, but the maximum cut has weight 8 and $\lceil 18/4 \rceil = 5$. The threshold must be $\lceil (\sum_i c_i)^2 / 4 \rceil$. A script compared both thresholds with brute force on 500 random instances (seed 1972, up to 6 numbers at most 9): the corrected threshold gave no mismatch, and the printed one gave 294.

The key identity. For $S \subseteq \{1, \ldots, s\}$ with $\sigma = \sum_{i \in S} c_i$, the cut between $S$ and its complement has weight $\sum_{i \in S} \sum_{j \notin S} c_i c_j = \sigma (C - \sigma)$, and $\sigma(C - \sigma) = C^2/4 - (C/2 - \sigma)^2$.

If a partition exists: its side $S$ has $\sigma = C/2$, and $C$ is even, so the cut weight is $C^2/4 = W$.

If some cut has weight at least $W$: take an arbitrary such $S$. Then $\sigma(C - \sigma) \ge W \ge C^2/4$, so $(C/2 - \sigma)^2 \le 0$ and $\sigma = C/2$. So $S$ is a side of a partition.

Example. For $c = (1, 2, 3)$, $C = 6$ and $W = 9$; the cut $\{3\}$ against $\{1, 2\}$ has weight $3 \cdot 1 + 3 \cdot 2 = 9$. For $c = (1, 1, 4)$, $W = 9$ and the maximum cut is 8, so the answer is no, as it must be.

## The remaining reductions

The other edges of the tree are: SAT to 0-1 integer programming and to 3-SAT; clique to set packing; node cover to set covering, feedback node set, feedback arc set and directed Hamilton circuit; directed to undirected Hamilton circuit; 3-SAT to chromatic number; chromatic number to clique cover and to exact cover; exact cover to hitting set, Steiner tree and 3-dimensional matching; knapsack to job sequencing. Each is proved on the page of its target problem or on [Karp's reduction tree](/karp-21-np-complete/), and in Karp (1972). Together with membership and the transitivity of Karp reductions, they show that all 21 problems are NP-complete.
