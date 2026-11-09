---
title: Dwyer's algorithm runs in O(n log n) worst-case time and O(n) space
proves: [complexity]
status: full
---

**Claim.** In the real RAM model, with the two predicates counted as $O(1)$ operations, and if no four of the distinct points lie on one circle, DWYER takes $O(n \log n)$ time in the worst case and $O(n)$ space, for every number of strips $k$ with $1 \le k \le n/2$. The average time $O(n \log \log n)$ for points uniform in a square is Dwyer's result and is not proved here.

**Notation.** $m_1, \ldots, m_k$ are the sizes of the strips, with $m_1 + \cdots + m_k = n$.

**Proof.** We use the [Guibas-Stolfi complexity proof](/guibas-stolfi-algorithm/): BUILD on $m$ points takes $O(m \log m)$ time, and one merge of a run of $m$ points takes $O(m)$ time. By the rotation lemma of the correctness proof, BUILD on a strip makes the same steps as on the rotated strip, so the same bounds hold.

- Line L1 sorts in $O(n \log n)$ time. Line L2 takes $O(1)$ time.
- Lines L4 and L5 take $O(m_j \log m_j)$ time for strip $j$. Line L6 walks the outer face once; each edge is on the walk at most twice and there are at most $3 m_j$ edges, so it takes $O(m_j)$ time. The sum over all strips is $O(\sum_j m_j \log m_j) = O(n \log n)$.
- In one pass of line L7, the merges of line L8 act on disjoint runs whose sizes add up to at most $n$, so the pass takes $O(n)$ time. There are $\lceil \log_2 k \rceil$ passes, so lines L7 and L8 take $O(n \log k)$ time.
- Line L9 visits every edge a constant number of times.

The total is $O(n \log n)$. At every moment the live edges form plane graphs on disjoint sets of points, so there are at most $3n$ of them, and the free list keeps the number of edge records at most $3n$. The handles take $O(k)$ space. So the space is $O(n)$. $\blacksquare$

*Remark on the average bound.* With $k = 1$ the algorithm is the Guibas-Stolfi algorithm with cuts by $y$. The claim gives no gain from strips in the worst case. The gain is in the average case: for uniform points, a merge across a short cut changes few edges in expectation, and Dwyer's analysis bounds the total by $O(n \log \log n)$ when the sorts are done by bucketing. That analysis is cited, not proved here, and the code uses comparison sorts, which cost $O(n \log n)$.
