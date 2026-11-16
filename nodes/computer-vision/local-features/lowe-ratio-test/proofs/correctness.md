---
title: Properties of the ratio test
proves: [correctness]
status: full
---

Let $A$ and $B$ be finite lists of vectors in $\mathbb{R}^D$ with $|B| \ge 2$, let $\lVert \cdot \rVert$ be the Euclidean norm, and let $0 < r \le 1$. For $a \in A$ let $d_1(a) \le d_2(a)$ be the two smallest values of $\lVert a - b \rVert$ over the entries $b$ of $B$, counted with repetition, and let $j(a)$ be the smallest index of $B$ at distance $d_1(a)$. The template keeps $(i, j(a_i))$ exactly when $d_1(a_i) < r \, d_2(a_i)$. The code tests $d_1^2 < r^2 d_2^2$.

**Lemma 1 (the nearest two).** The scan of `nearest_two` returns $j(a)$, $d_1(a)^2$ and $d_2(a)^2$.

*Proof.* Invariant: after the entries $0, \dots, t$ of $B$, `best` and `second` are the two smallest squared distances among them, counted with repetition, and `j1` is the smallest index with distance `best`. Initially both are $\infty$. For the next entry with value $d$: if $d <$ `best`, the old `best` becomes the second smallest and $d$ the smallest, with the new index; if `best` $\le d <$ `second`, only `second` changes; else nothing changes. A value equal to `best` goes to `second` and does not change `j1`, so the smallest index is kept. After all entries the invariant gives the claim. $\square$

**Lemma 2 (squares).** For $d_1, d_2 \ge 0$ and $r > 0$, $d_1 < r d_2$ if and only if $d_1^2 < r^2 d_2^2$.

*Proof.* Both sides are non-negative, and $t \mapsto t^2$ is strictly increasing on $[0, \infty)$. $\square$

**Lemma 3 (scale).** Multiplying all vectors of $A$ and $B$ by the same $c > 0$, or translating all of them by the same vector, or applying the same orthogonal map to all of them, does not change the kept pairs.

*Proof.* Each map multiplies every distance $\lVert a - b \rVert$ by the same factor $c$ (or by 1). The order of the distances, the index $j(a)$ and the truth of $d_1 < r d_2$ do not change. $\square$

**Lemma 4 (monotone in r).** If $r \le r'$, every pair kept with $r$ is kept with $r'$.

*Proof.* $d_1 < r d_2 \le r' d_2$. $\square$

**Lemma 5 (ambiguity is rejected).** If two entries of $B$ are at the same smallest distance from $a$, in particular if $B$ holds the nearest vector twice, then $a$ is rejected for every $r \le 1$. With $r = 1$, a query is kept exactly when its nearest neighbor is unique.

*Proof.* Then $d_1 = d_2$, and $d_1 < r d_1$ is false for $r \le 1$. With $r = 1$ the test is $d_1 < d_2$, which holds exactly when one entry is strictly closer than all others. $\square$

**Lemma 6 (not a matching).** The kept pairs can use the same $j$ for several $i$.

*Proof.* Take $B = \{(0), (10)\}$ and $A = \{(1), (-1)\}$. Both queries have $d_1 = 1$ at index 0 and $d_2 = 9$ or $11$, so both are kept with $r = 0.8$. $\square$

**Theorem.** `ratio_test_match` returns, in order of $i$, exactly the pairs $(i, j(a_i))$ with $d_1(a_i) < r \, d_2(a_i)$, together with the two distances. The kept set does not change under a common scaling, translation or rotation of the descriptors, grows with $r$, never contains a query with a tie for the nearest, and is not always a matching.

*Proof.* Lemma 1 gives the values, Lemma 2 shows that the test of line L3 is the ratio test, and Lemmas 3 to 6 give the properties. $\blacksquare$
