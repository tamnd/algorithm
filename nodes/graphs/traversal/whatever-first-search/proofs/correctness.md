---
title: Whatever-first search marks exactly the reachable vertices and builds a tree
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a directed or undirected graph, where an undirected edge is in both adjacency lists, and let $s \in V$. The bag $B$ may follow any discipline: we only use that TAKE removes and returns some item that is in $B$. Let $R$ be the set of vertices reachable from $s$.

**Lemma 1 (pairs come from marked vertices).** At each moment, each pair $(p, v)$ in $B$ is either $(\mathrm{NIL}, s)$ or has $p$ marked and $(p, v) \in E$.

*Proof.* The pair $(\mathrm{NIL}, s)$ is put at line L2. All other pairs are put at line L7, as $(v, w)$ with $w \in \mathrm{Adj}[v]$, right after line L6 marked $v$. Marks are never removed. $\square$

**Lemma 2 (each vertex is marked once).** Line L6 runs at most one time for each vertex, and line L7 scans each list at most one time.

*Proof.* Line L6 runs for $v$ only after line L5 found $v$ unmarked, and it marks $v$, which then stays marked. Line L7 runs only right after line L6. $\square$

**Termination.** By Lemma 2, line L7 runs at most $n$ times, so at most $1 + \sum_v |\mathrm{Adj}[v]|$ pairs are ever put. Each iteration of the loop of line L3 takes one pair, so there are at most that many iterations, and the loop ends with $B$ empty.

**Lemma 3 (marked means reachable).** Each marked vertex is in $R$, and if $v \ne s$ is marked, then $\pi[v]$ was marked before $v$ and $(\pi[v], v) \in E$.

*Proof.* By induction on the order of marking. The first pair taken is $(\mathrm{NIL}, s)$, because it is the only pair until a vertex is marked, so $s$ is marked first, with $\pi[s] = \mathrm{NIL}$, and $s \in R$. If $v \ne s$ is marked later by the pair $(p, v)$, then this pair is not $(\mathrm{NIL}, s)$, since $s$ was already marked when it could be taken again; by Lemma 1, $p$ is marked and $(p, v) \in E$. Line L6 sets $\pi[v] = p$, and $p$ was marked before $v$. By the induction hypothesis $p \in R$, so $v \in R$ too. $\square$

**Lemma 4 (reachable means marked).** When the algorithm ends, each vertex of $R$ is marked.

*Proof.* Assume that some $v \in R$ is unmarked at the end, and let $s = x_0, x_1, \ldots, x_k = v$ be a path in $G$. The vertex $s$ is marked, so there is a first unmarked vertex $x_i$ on the path, with $i \ge 1$. The vertex $x_{i-1}$ is marked, so line L7 ran for it and put the pair $(x_{i-1}, x_i)$, because $x_i \in \mathrm{Adj}[x_{i-1}]$. The loop ends only when $B$ is empty, so this pair was taken at some step. At that step, line L5 either found $x_i$ marked or marked it. Either way $x_i$ is marked at the end, which contradicts its choice. $\square$

**Theorem.** WHATEVER-FIRST-SEARCH$(G, s)$ terminates for every discipline of the bag. When it ends, $\mathrm{mark}[v] = \mathrm{TRUE}$ exactly for $v \in R$, and the edges $(\pi[v], v)$ for $v \in R \setminus \{s\}$ form a tree rooted at $s$ that spans $R$, in which each path from $s$ is a path of $G$.

*Proof.* Termination was shown above. Lemmas 3 and 4 give the marked set. For the tree, take $v \in R$ and follow $v, \pi[v], \pi[\pi[v]], \ldots$. By Lemma 3, each step goes to a vertex that was marked strictly earlier, along an edge of $G$ read backwards, so no vertex repeats, and the chain ends at the only marked vertex with parent NIL, which is $s$, because line L6 sets $\pi[v] = p \ne \mathrm{NIL}$ for each $v \ne s$. Each $v \in R \setminus \{s\}$ has exactly one parent, so the $|R| - 1$ edges connect all of $R$ to $s$ without a cycle, and they form a tree rooted at $s$. Its path from $s$ to $v$ is the chain read forwards, a path of $G$. $\blacksquare$
