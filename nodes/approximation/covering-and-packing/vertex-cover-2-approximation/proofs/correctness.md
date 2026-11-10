---
title: The endpoints of a maximal matching form a vertex cover of size at most twice the optimum
proves: [correctness]
status: full
---

The input is a graph $G = (V, E)$ with $n$ vertices and $m$ edges and no self-loops. $M$ is the list of edges appended in line L4, and $C$ is the set of vertices added in line L5. OPT is the size of a smallest vertex cover.

**Lemma 1 (the invariant).** At the start of each iteration of the loop of line L2, $M$ is a matching and $C$ is exactly the set of endpoints of the edges of $M$.

*Proof.* At the start, $M$ and $C$ are empty. Suppose the claim holds before the iteration for the edge $\{u, v\}$. If line L3 finds $u \in C$ or $v \in C$, nothing changes. Else neither $u$ nor $v$ is an endpoint of an edge of $M$, so $M$ with $\{u, v\}$ added is still a matching, and lines L4 and L5 add the edge to $M$ and its two endpoints to $C$. $\square$

**Lemma 2 (a cover).** At the end, each edge of $G$ has an endpoint in $C$.

*Proof.* Take an edge $\{u, v\}$, and look at its iteration. If line L3 finds an endpoint in $C$, this endpoint stays in $C$, because no line removes vertices. Else line L5 puts both endpoints into $C$. $\square$

**Lemma 3 (the lower bound).** Each vertex cover $C^*$ of $G$ has $|C^*| \ge |M|$.

*Proof.* Each edge of $M$ has an endpoint in $C^*$. The edges of $M$ have no common endpoint, by Lemma 1, so these endpoints are distinct, and $C^*$ has at least $|M|$ vertices. $\square$

**Theorem.** The algorithm returns a vertex cover $C$ with $|C| = 2|M| \le 2 \cdot \text{OPT}$.

*Proof.* By Lemma 2, $C$ is a vertex cover. By Lemma 1, $C$ is the set of the endpoints of the matching $M$, and these $2|M|$ endpoints are distinct, so $|C| = 2|M|$. Lemma 3 with an optimal cover gives $|M| \le \text{OPT}$. $\blacksquare$

**Remark (maximality).** Lemma 2 says that $M$ is a maximal matching: each edge not in $M$ has an endpoint matched by $M$, so no edge can be added to $M$. The proof of the ratio uses only that $M$ is a matching, and the proof that $C$ is a cover uses only that $M$ is maximal. So the endpoints of any maximal matching, found in any way, give a 2-approximation.
