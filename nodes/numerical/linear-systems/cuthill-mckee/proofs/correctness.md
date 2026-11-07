---
title: Cuthill-McKee numbers every vertex once, follows the level structure, and has bandwidth below twice the level width
proves: [correctness, termination]
status: full
---

Notation of the page: $G = (V, E)$ undirected, $n = |V|$, $\pi$ the output list, $f(\pi_k) = k$. For a root $r$, $L_i(r)$ is the set of vertices at distance $i$ from $r$, $e(r)$ the eccentricity, and "levels from $r$" means $L_0(r), \ldots, L_{e(r)}(r)$.

**Lemma 1 (the root search terminates).** PSEUDO-PERIPHERAL$(G, s)$ stops after at most $n$ level structure computations and returns a vertex of the component of $s$.

*Proof.* Each accepted move replaces $r$ by a vertex $x$ of the same component with $e(x) > e(r)$. Eccentricities are integers in $[0, n - 1]$, so there are at most $n - 1$ accepted moves, and each iteration computes one level structure. Every $x$ is taken from a level of the current structure, which lies in the component. $\square$

**Lemma 2 (each vertex is appended once).** A vertex is appended to $\pi$ only at line L4 or L9, and in both cases $\mathrm{seen}$ is false just before and set to true at that moment. Since seen is never reset, no vertex is appended twice.

**Lemma 3 (one component per root).** When the loop of lines L6 to L9 for root $r$ ends, the vertices appended during it are exactly the component $C(r)$ of $r$, and they are appended in breadth-first order: all of $L_i(r)$ before any of $L_{i+1}(r)$.

*Proof.* Before the root is chosen at line L3, every seen vertex belongs to a component already processed (induction over the outer loop, using the claim for earlier roots), so no vertex of $C(r)$ is seen. Lines L6 to L9 are a breadth-first search from $r$ that uses $\pi$ from position head as its queue: a vertex is appended when it is first discovered from an already appended vertex, and vertices are removed in the order appended. The standard BFS invariant holds: the queue, read from head to the end, consists of vertices of some level $L_i$ followed by vertices of $L_{i+1}$. Hence the vertices are appended in nondecreasing order of distance, and every vertex reachable from $r$, that is every vertex of $C(r)$, is appended. No vertex outside $C(r)$ is adjacent to $C(r)$, so none is appended. $\square$

**Theorem 1 (permutation, termination).** The algorithm terminates and $\pi$ is a permutation of $V$.

*Proof.* The outer loop of line L2 has $n$ iterations. Each inner loop advances head by one per iteration and stops when head reaches $|\pi| \le n$ (Lemma 2). Each call of line L3 terminates by Lemma 1. Every vertex $s$ is either seen when line L2 reaches it, hence already in $\pi$, or it becomes a root's component member by Lemma 3; so all $n$ vertices appear, and by Lemma 2 exactly once. $\square$

**Theorem 2 (characterization).** Let $C$ be a component with root $r$, numbered $f(r) = c, c + 1, \ldots, c + |C| - 1$. For $v \in C \setminus \{r\}$ let $p(v) = \min\{f(w) : w \sim v\}$. Then $p(v) < f(v)$, and listing $C \setminus \{r\}$ in the order of $\pi$ lists the keys $(p(v), d(v), v)$ in strictly increasing order. Conversely, a numbering of $C$ that starts with $r$ and has this property is the one produced.

*Proof.* Contiguity follows from Lemma 3, since a component is appended in one inner loop. Fix $v \ne r$. It is appended at line L9 while some vertex $u$ is being processed at line L7. Every neighbour of $v$ processed before $u$ would have appended $v$ earlier, so none exists, and $u$ itself is a neighbour; vertices are processed in the order of their numbers, so $u$ is the neighbour with the smallest number and $p(v) = f(u) < f(v)$. Vertices appended while processing the same $u$ have the same $p$ and are appended in increasing $(d, \text{index})$ order by line L8. Vertices appended while processing $u$ come before those appended while processing a later $u'$, which have $p = f(u') > f(u)$. So the keys increase strictly along $\pi$. For the converse, the keys are distinct (they contain $v$), so the property fixes the order of $C \setminus \{r\}$ once $f$ is known on earlier vertices; by induction on position this order is unique, and the produced order has it. $\square$

**Theorem 3 (bandwidth bound).** With the levels $L_0, \ldots, L_e$ from the root of a component, every edge $\{v, w\}$ of that component satisfies $|f(v) - f(w)| \le \max_i (|L_i| + |L_{i+1}|) - 1$, with the convention $|L_{e+1}| = 0$. Hence $\beta_f \le 2 w - 1$ where $w$ is the largest level width over all components.

*Proof.* In a breadth-first level structure, the endpoints of an edge are at distances differing by at most one, so $v, w \in L_i \cup L_{i+1}$ for some $i$. By Lemma 3, $L_i \cup L_{i+1}$ occupies a contiguous block of $|L_i| + |L_{i+1}|$ numbers. Two numbers in a block of that size differ by at most $|L_i| + |L_{i+1}| - 1$. Edges join vertices of the same component only, so the bound for $G$ is the maximum over components, which is at most $2w - 1$. $\blacksquare$
