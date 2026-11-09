---
title: Seidel's point location answers every query correctly, for every insertion order
proves: [correctness, termination]
status: full
---

**Setting.** $S$ is a finite set of $n$ segments, any two meeting at most in a common end point, and all geometry is in the sheared plane of the symbolic shear $(x, y) \mapsto (x + \varepsilon y, y)$, as on the [trapezoidal map](/trapezoidal-map/) page. $\pi$ is any permutation of $S$, and $D$ the DAG after line L4.

**Claim.** (1) For every $\pi$ and every point $q$, SEIDEL-QUERY returns the vertex $q$ if $q$ is an end point; otherwise the segment that contains $q$ if there is one; otherwise the pair (top, bottom) of the segments directly above and below $q$ (each possibly none). (2) Each round of lines L2 to L4 terminates. (3) If the loop of line L5 ends, every query visits at most $L$ inner nodes of $D$. (4) If $L$ is at least the longest path of the DAG for some permutation, each round ends the loop with probability at least $1/n!$, so the loop ends with probability $1$.

**Step 1 (each insertion keeps the invariant).** Let $I(R)$ be the statement: the trapezoid records are the faces of the trapezoidal map $T(R)$ with correct fields and neighbor pointers, and for each face $F$ the region of its leaf in $D$ is $F$. $I(\emptyset)$ holds: one trapezoid with no sides, the whole plane, and a DAG with one leaf. The correctness proof of the trapezoidal map shows that if $I(R)$ holds and $s$ meets the segments of $R$ only at shared end points, then TM-INSERT$(s)$ makes $I(R \cup \{s\})$ hold, and that it terminates. This uses no property of the order. Every prefix $R = \{\pi(1), \ldots, \pi(i)\}$ is a subset of $S$, so its segments meet only at end points, and by induction on $i$, $I(S)$ holds after line L4. This also proves (2).

**Step 2 (the query).** By $I(S)$ and Step 7 of the trapezoidal map proof, TM-QUERY returns the vertex for an end point, the segment for a point in the relative interior of a segment, and otherwise ends at the leaf of the face $F$ of $T(S)$ that contains $q$. The top and bottom of $F$ are the first segments hit by the vertical rays from $q$, since the open vertical interval of $F$ through $q$ meets no segment and ends on top$(F)$ and bottom$(F)$ (Step 1 of that proof). This proves (1).

**Step 3 (the depth bound).** Every query follows one root-to-leaf path of $D$, or a prefix of one when it returns early at an X-node or a Y-node. The number of inner nodes it visits is at most the number of inner nodes on that path, which is at most the longest path of $D$. When the test of line L5 succeeds, that is at most $L$. This proves (3).

**Step 4 (termination of the loop).** Each round draws a uniform permutation independently of the earlier rounds. If some permutation $\pi_0$ gives a DAG whose longest path is at most $L$, each round picks $\pi_0$ with probability $1/n!$, so the probability that the first $k$ rounds all fail is at most $(1 - 1/n!)^k \to 0$. So the loop ends with probability $1$. The expected number of rounds for $L = c \ln(n+1)$ is bounded in [the complexity proof](complexity/). $\blacksquare$
