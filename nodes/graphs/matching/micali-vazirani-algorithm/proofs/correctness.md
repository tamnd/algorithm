---
title: The Micali-Vazirani algorithm returns a maximum matching
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a finite general graph with $n$ vertices, and let $M$ be the matching at the start of a phase. Write $l_m$ for the length of a shortest $M$-augmenting path ($\infty$ if there is none). The proof has a part that is proved here and one lemma about the search that is cited.

**Lemma 1 (the search, cited).** In a phase:

(a) for every vertex $v$ of tenacity at most $l_m$, MIN and MAX assign the correct minlevel and maxlevel of $v$, and every bridge of tenacity $2i + 1 \le l_m$ is in the list of level $i$ by the end of MIN at level $i$;

(b) for a bridge $(u, v)$ processed in line L5, DDFS either returns the highest bottleneck below $\text{bud}^*(u)$ and $\text{bud}^*(v)$, or two distinct free vertices with vertex-disjoint paths to them in the graph of predecessors and buds;

(c) a vertex erased in line L8 lies on no shortest augmenting path that is vertex-disjoint from the paths found so far in the phase, and opening petals in line L7 gives an augmenting path of length $l_m$ that uses no erased vertex.

This is Theorem 34, Lemma 33, Theorem 28 and Section 7.3 of Vazirani, *A simplification of the MV matching algorithm and its proof* (arXiv:1210.4594, 2013). The rest of this page shows how the result of the algorithm follows from it.

**Lemma 2 (one phase).** If $l_m < \infty$, the phase augments $M$ along a nonempty set of vertex-disjoint augmenting paths of length $l_m$, and no augmenting path of length $l_m$ is disjoint from all of them. If $l_m = \infty$, the phase augments nothing.

*Proof.* Each augmentation in line L8 uses a path $P$ built in line L7. Before it changes $M$, the implementation checks that $P$ is simple, that its ends are free, and that its edges alternate between edges outside and inside the current matching, starting and ending outside. So $P$ is an augmenting path of the current matching, and flipping its edges gives a matching with one more edge. Line L8 then erases all vertices of $P$. Lines L5 and L7 never use erased vertices, so the paths of one phase are vertex-disjoint. A vertex on none of them keeps its mate, so each path is also an augmenting path of $M$, with the same edges outside and inside the matching.

If $l_m = \infty$, there is no augmenting path, and by the check above no path is ever flipped. Let $l_m = 2j + 1$. The levels and bridges up to tenacity $l_m$ are correct by Lemma 1(a). At each level $i < j$, every DDFS ends at a bottleneck or with an empty support, because two free vertices with disjoint paths from the ends of a bridge of tenacity $2i + 1$ would give an augmenting path of length $2i + 1 < l_m$, by Lemma 1(c). At level $j$, some bridge of tenacity $l_m$ lies on a shortest augmenting path, so the first DDFS on such a bridge whose ends are not erased returns two free vertices by Lemma 1(b), and a path is found. Line L9 then ends the phase after level $j$, so all paths found have length $l_m$. Finally, suppose an augmenting path $Q$ of length $l_m$ is disjoint from all paths found. By Lemma 1(c), none of its vertices is erased. It contains a bridge of tenacity $l_m$, which is processed at level $j$, and Lemma 1(b) and (c) then give another path disjoint from those found, which the algorithm would have flipped. This contradicts the choice of $Q$. $\square$

**Lemma 3 (shortest lengths grow).** Let a phase start with $M$ and $l_m = \ell < \infty$, find the paths $P_1, \ldots, P_k$, and end with $M' = M \triangle P_1 \triangle \cdots \triangle P_k$. Then every $M'$-augmenting path has more than $\ell$ edges.

*Proof.* Let $P$ be an $M'$-augmenting path. If $P$ shares no vertex with the $P_i$, it is $M$-augmenting, so it has at least $\ell$ edges, and by Lemma 2 it does not have exactly $\ell$. Otherwise $P$ meets some $P_i$ at a vertex $v$. Every vertex of $P_i$ is matched in $M'$ by an edge of $P_i$, so $v$ is not an end of $P$, and $P$ contains that edge. Now $N = M' \triangle P$ is a matching with $|M| + k + 1$ edges, and $M \triangle N = (P_1 \cup \cdots \cup P_k) \triangle P$. The symmetric difference of two matchings is a union of vertex-disjoint paths and cycles, and since $N$ has $k + 1$ more edges than $M$, it contains at least $k + 1$ vertex-disjoint $M$-augmenting paths, each with at least $\ell$ edges. So $|(P_1 \cup \cdots \cup P_k) \triangle P| \ge (k + 1)\ell$. The left side equals $k\ell + |P| - 2|P \cap (P_1 \cup \cdots \cup P_k)| \le k\ell + |P| - 2$, so $|P| \ge \ell + 2$. Nothing here uses bipartiteness. $\square$

**Termination.** Each phase that finds a path increases $|M|$, and $|M| \le n/2$. A phase that finds no path makes line L10 return. So there are at most $n/2 + 1$ phases. Within a phase, the loop of line L3 runs at most $2n + 2$ times, and each DDFS and each petal opening only moves to unvisited vertices or down to lower levels, so each step stops.

**Theorem.** The algorithm returns a maximum matching of $G$.

*Proof.* By Lemma 2, each phase keeps $M$ a matching. The algorithm stops after a phase that finds no augmenting path. By Lemma 2 this happens only when $l_m = \infty$, that is, when $M$ has no augmenting path. By [Berge's lemma](/berge-lemma/), $M$ is then a maximum matching. By Lemma 3 and the argument of Hopcroft and Karp, the number of phases is also $O(\sqrt n)$. $\blacksquare$
