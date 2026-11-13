---
title: RRT* keeps a tree of free paths with exact, non-increasing costs, and is probabilistically complete
proves: [correctness]
status: full
---

We assume that the checker is exact: it calls a segment free only if every point of it is in $\mathcal{C}_{free}$. The cost of a path is its length, and $\mathrm{len}(v)$ is the length of the path in the tree from $x_{init}$ to the vertex $v$. Line numbers refer to the pseudocode on the [RRT\*](/rrt-star/) page.

**Lemma 1 (no cycle).** In line L13, the vertex $x$ is never an ancestor of $x_{new}$.

*Proof.* Assume that the stored costs are exact before line L11, which Lemma 2 proves by induction. The ancestors of $x_{new}$ are $x_{min}$ and the ancestors of $x_{min}$. Costs along a tree path do not decrease from the root, so every ancestor $a$ of $x_{new}$ has $\mathrm{cost}(a) \le \mathrm{cost}(x_{min}) \le c_{min}$, since $c_{min} = \mathrm{cost}(x_{min}) + \lVert x_{min} - x_{new} \rVert$. The test of line L12 needs $c_{min} + \lVert x_{new} - x \rVert < \mathrm{cost}(x)$, so $\mathrm{cost}(x) > c_{min}$, and $x$ is not an ancestor. A rewiring in line L13 changes only the parent of $x$ and the costs of $x$ and its descendants. None of these is an ancestor of $x_{new}$, so the ancestors of $x_{new}$ and their costs, and $\mathrm{cost}(x_{new}) = c_{min}$, stay the same for the rest of the loop of line L11, and the argument holds for each $x$ in turn. $\square$

**Lemma 2 (a tree with exact costs).** After every iteration, the vertices and parent links form a tree rooted at $x_{init}$, every edge is a free segment, and $\mathrm{cost}(v) = \mathrm{len}(v)$ for every vertex $v$.

*Proof.* By induction on the iterations. Line L1 makes a tree with one vertex and cost 0. In an iteration that passes line L6, line L10 adds $x_{new}$ as a leaf with parent $x_{min}$. The edge from $x_{min}$ to $x_{new}$ is free: for $x_{min} = x_{nearest}$ line L6 tested it, and otherwise line L9 tested it. Its cost $c_{min} = \mathrm{len}(x_{min}) + \lVert x_{min} - x_{new} \rVert = \mathrm{len}(x_{new})$.

In line L13, line L12 has tested the segment from $x_{new}$ to $x$, so the new edge is free. By Lemma 1 the new parent is not a descendant of $x$, so the structure stays a tree. The tree path to $x$ and to each descendant $u$ of $x$ now goes through $x_{new}$, and its length drops by $\Delta = \mathrm{cost}(x) - c_{min} - \lVert x_{new} - x \rVert$. Line L13 lowers the cost of $x$ and of each descendant by the same $\Delta$, so the costs stay exact. The other vertices keep their tree paths and costs. $\square$

**Lemma 3 (costs never increase).** For each vertex $v$, $\mathrm{cost}(v)$ never increases. So the best cost $Y_n$ of a vertex in $\mathcal{X}_{goal}$ is non-increasing in $n$, and every answer is a free path from $x_{init}$ into $\mathcal{X}_{goal}$ of length $Y_n$.

*Proof.* Line L10 does not change old costs, and line L13 changes costs only by $-\Delta < 0$. The set of vertices in $\mathcal{X}_{goal}$ only grows, and each of their costs is non-increasing, so their minimum is non-increasing. By Lemma 2, the answer is the tree path of a vertex in $\mathcal{X}_{goal}$, made of free segments, with length equal to its cost. $\square$

**Lemma 4 (the same vertices as the RRT).** Run the RRT without goal bias and RRT\* with the same step size and on the same sequence of random points $x_{rand}$. Then after each iteration both have the same set of vertices.

*Proof.* By induction. In an iteration, lines L4 to L6 of RRT\* depend only on the set of vertices, not on the edges: the nearest vertex, the point $x_{new}$ and the test of the segment are the same in the RRT. Both add $x_{new}$ if and only if the test passes. Lines L7 to L13 change only edges and costs. $\square$

**Theorem (probabilistic completeness).** Let $\mathcal{X}_{goal}$ contain the ball $B(x_{goal}, r_{goal})$, and let $\tau$ be a path from $x_{init}$ to $x_{goal}$ of length $L$ with clearance $\delta > 0$. With $\nu = \min(\delta/4, \eta/3, r_{goal})$, $m = \lceil L/\nu \rceil$ and $p = \zeta_d \nu^d / \mu(\mathcal{C})$, after $N \ge 2m/p$ iterations RRT\* has a vertex in $\mathcal{X}_{goal}$ with probability at least $1 - e^{-pN/8}$.

*Proof.* The [RRT proof](/rapidly-exploring-random-tree/proofs/correctness/), with $p_{goal} = 0$, shows that with this probability the RRT adds a vertex in $B(x_{goal}, \nu) \subseteq \mathcal{X}_{goal}$ within $N$ iterations, if it does not stop at the goal earlier. Its argument uses only the vertices and lines L3 to L7 of RRT, and it still holds when the run does not stop at the goal. By Lemma 4, RRT\* has the same vertex. By Lemma 2, that vertex has a free tree path from $x_{init}$. $\blacksquare$

This is Theorem 23 of Karaman and Frazzoli (2011), with explicit constants for the geometric case. Their proof also uses the equality of the vertex sets.

**What is not proved here.** The lemmas show that RRT\* never returns a wrong path and never makes a path worse. The convergence of $Y_n$ to the optimal cost $c^*$ needs the radius of line L7 and is a separate theorem with a careful probabilistic proof. See the page on [asymptotic optimality](/rrt-star-asymptotic-optimality/), which states the hypotheses of Karaman and Frazzoli, the gap that Solovey, Janson, Schmerling, Frazzoli and Pavone found in their proof, and the corrected theorem.
