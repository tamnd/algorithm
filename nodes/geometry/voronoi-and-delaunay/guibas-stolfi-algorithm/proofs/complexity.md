---
title: The Guibas-Stolfi algorithm runs in O(n log n) worst-case time and O(n) space
proves: [complexity]
status: full
---

**Claim.** In the real RAM model, with the orientation test and the in-circle test counted as $O(1)$ operations, and under the hypothesis of the correctness proof that no four of the distinct points lie on one circle, GUIBAS-STOLFI takes $O(n \log n)$ time in the worst case and $O(n)$ space.

**Notation.** $m$ is the number of points in a call of BUILD, $L$ and $R$ are its halves, and $U = L \cup R$.

**Edge counts.** By the correctness proof, the structure of a call is a plane straight-line graph on its points at every moment, with at most $\max(3m - 6, m - 1) \le 3m$ edges by [Euler's formula](/euler-formula/). At the end of a call, the edges are the Delaunay edges of the points of the call.

**Lemma 1.** The merge of a call on $m$ points takes $O(m)$ time.

*Proof.* Line L6: by Lemma 3 of the correctness proof, ldi moves only along the hull chain of $L$ and rdi only along the hull chain of $R$, each pointer moves forward and never passes its tangent point, so the walk takes at most $|L| + |R| = m$ steps of $O(1)$ time. Line L11 adds one cross edge per pass, and by the correctness proof these are the cross edges $e_1, \ldots, e_k$ of the final triangulation, which are never deleted. So there are at most $k + 1 \le 3m$ passes. Lines L8 and L9 delete only edges of the two halves, each at most once, so there are at most $3|L| + 3|R| = 3m$ deletions. Every pass does $O(1)$ work besides its deletions, and every deletion takes $O(1)$ time. $\square$

**Proof of the claim.** Line L1 sorts in $O(n \log n)$ time and removes duplicates in $O(n)$ time. Let $T(m)$ be the worst-case time of BUILD on $m$ points. Then $T(m) = O(1)$ for $m \le 3$, and $T(m) \le T(\lfloor m/2 \rfloor) + T(\lceil m/2 \rceil) + cm$ for $m \ge 4$, by Lemma 1. By the [master theorem](/master-theorem/), $T(n) = O(n \log n)$. Listing the triangles visits every edge a constant number of times, which is $O(n)$.

Space: at every moment, the live edges of all calls form plane graphs on disjoint blocks of points, so there are at most $3n$ of them. A deleted record goes on the free list and is used again by the next new edge, so the number of records is at most the largest number of live edges at one moment, which is at most $3n$. Each record has $O(1)$ words. The recursion has depth $O(\log n)$ with $O(1)$ words per level. So the space is $O(n)$. $\blacksquare$

*Without the free list* the number of records is the number of edges ever made. Each merge of $m$ points makes $O(m)$ edges, so this number is $O(n \log n)$ in the worst case.

*Cocircular input.* With four or more points on one circle, the bounds above are observed in the tests on grids, not proved here.
