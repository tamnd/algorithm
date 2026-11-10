---
title: Greedy online matching returns a maximal matching and is 1/2-competitive, and no deterministic rule does better
proves: [correctness]
status: full
---

We use the pseudocode of the page. $G = (U \cup V, E)$ is the bipartite graph, $v_1, \ldots, v_n$ are the online vertices in arrival order, $M$ is the output and $M^*$ is a maximum matching of $G$.

**Claim 1.** After each step, $M$ is a matching, each edge of $M$ is an edge of $G$, and $F$ is exactly the set of offline vertices not covered by $M$.

*Proof.* By induction on $t$. Before step 1, $M = \emptyset$ and $F = U$. At step $t$, line L4 gives $C \subseteq N(v_t) \cap F$, so the vertex $u$ of line L6 is a neighbour of $v_t$ that $M$ does not cover. The vertex $v_t$ is new, so $M$ does not cover it either. So line L7 adds an edge of $G$ whose two endpoints are not covered, and $M$ stays a matching. Line L8 removes $u$ from $F$, so $F$ is again the set of uncovered offline vertices. If $C = \emptyset$, nothing changes. $\square$

**Claim 2.** The algorithm is online: the decision for $v_t$ uses only $N(v_1), \ldots, N(v_t)$ and the earlier decisions, and it is never changed.

*Proof.* Lines L3 to L8 read only $N(v_t)$ and $F$, and $F$ depends only on the earlier steps. No line removes an edge from $M$ or returns a vertex to $F$. $\square$

**Claim 3.** $M$ is a maximal matching of $G$: each edge of $G$ has an endpoint covered by $M$.

*Proof.* Take an edge $(u, v_t)$. If $v_t$ is covered, we are done. If not, then at step $t$ line L5 found $C = \emptyset$, so $u \notin F$ at that time. By Claim 1, $u$ was covered by $M$ then, and by Claim 2 it stays covered. $\square$

**Theorem 1.** For each rule CHOOSE and each input, $\lvert M \rvert \ge \lvert M^* \rvert / 2$.

*Proof.* By Claim 3, each edge of $M^*$ has an endpoint covered by $M$. The edges of $M^*$ are disjoint, so these endpoints are $\lvert M^* \rvert$ distinct vertices. The matching $M$ covers exactly $2 \lvert M \rvert$ vertices. So $\lvert M^* \rvert \le 2 \lvert M \rvert$. $\square$

**Theorem 2.** For each deterministic online algorithm, greedy or not, and each $k \ge 1$, there is an input with $\lvert M^* \rvert = 2k$ on which the algorithm matches at most $k$ vertices. So the ratio $1/2$ of Theorem 1 is tight, and no deterministic online algorithm has a ratio above $1/2$.

*Proof.* Use $k$ disjoint gadgets. Gadget $i$ has offline vertices $a_i, b_i$ and two online vertices. The first one is adjacent to $a_i$ and $b_i$. The adversary knows the algorithm, so it knows what it does with this vertex. If it is matched to $x \in \{a_i, b_i\}$, the second vertex is adjacent only to $x$, which is no longer free. If it is not matched, the second vertex is adjacent only to $a_i$. In both cases the algorithm matches at most one of the two vertices of the gadget, and the gadget has a matching of size 2: the first vertex with the other offline vertex and the second vertex with $x$ (or with $a_i$, with the first vertex taking $b_i$). The gadgets share no vertex, so $\lvert M^* \rvert = 2k$ and the algorithm gets at most $k$. $\square$

**Remark (randomized rules and adaptive adversaries).** If CHOOSE is random and the adversary sees the choice for the first vertex of each gadget before it builds the second (an adaptive online adversary), the same argument gives at most $k$ for every outcome of the coins. Against an oblivious adversary, Karp, Vazirani and Vazirani (1990) showed that a uniform random choice still has ratio $1/2 + o(1)$ on a family of graphs, while the [Ranking algorithm](/ranking-algorithm/) gets $1 - 1/e$. $\blacksquare$
