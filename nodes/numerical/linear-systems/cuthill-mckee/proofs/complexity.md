---
title: Cost of the Cuthill-McKee ordering
proves: [time.worst, space.extra, numbering.worst]
status: full
---

Adjacency lists with degrees stored; $n$ vertices, $m$ edges, largest degree $\Delta$. Let $n_C$ and $m_C$ be the vertex and edge counts of a component $C$.

**Numbering (lines L1 to L10 except L3).** Line L1 is $O(n)$. Sorting all vertices by $(d, \text{index})$ for line L2 is $O(n \log n)$. In the inner loop, each vertex is processed once at line L7 (Theorem 1 of the correctness proof); processing $v$ scans its $d(v)$ neighbours and sorts at most $d(v)$ of them, $O(d(v) \log(d(v) + 1) + 1)$. Summing over $v$, with $\sum_v d(v) = 2m$ and $\log(d(v)+1) \le \log(\Delta + 1)$, gives $O(n + m \log \Delta)$. Total $O(n \log n + m \log \Delta)$. (With a counting sort by degree, both sorts are linear and the numbering is $O(n + m)$.)

**Root search (line L3).** One level structure of $C$ costs $O(n_C + m_C)$, and choosing the minimum degree vertex of the last level is $O(n_C)$. By Lemma 1 of the correctness proof there are at most $e + 1 \le n_C$ level structures. So line L3 costs $O(n_C (n_C + m_C))$ for $C$, and summing over components, $O(n (n + m))$. Adding the numbering, the worst case time is $O(n(n + m))$.

**Space.** The flags take $n$ words, $\pi$ (which is also the queue) $n$ words, one level structure and the visited set of a search $O(n)$ words, and the sorted neighbour list at line L8 at most $\Delta \le n$ words. So $\Theta(n)$ extra space, besides the input. $\blacksquare$
