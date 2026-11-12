---
title: STRING-GRAPH keeps exactly the irreducible overlap edges, and every overlap edge is spelled by a path of kept edges
proves: [correctness, termination]
status: full
---

**Notation.** After line L1 the reads $r_0, \ldots, r_{m-1}$ are nonempty, pairwise distinct, and no read is a substring of another read. Fix $\ell \ge 1$. An overlap edge $(u, x, d)$ exists when $u \ne x$, $1 \le d \le |u| - \ell$, and the suffix $u[d..)$ is a proper prefix of $x$. Place $u$ at position 0 of a line and $x$ at position $d$. Then the two reads spell the same letters on $[d, |u|)$, this interval has length at least $\ell$, and $x$ ends at $d + |x| > |u|$. So along an edge both the start and the end move strictly to the right. An edge $(v, x, D)$ is transitive when there are edges $(v, w, a)$ and $(w, x, D - a)$ for some read $w$ and offset $a$; we call $(w, a)$ a witness. Since edges have no self-loops, a witness has $w \ne v$ and $w \ne x$, and $1 \le a < D$. The graph is irreducible at $(v, x, D)$ when that edge has no witness.

**Lemma 1 (the overlap edges).** Line L2 creates exactly the overlap edges.

*Proof.* Let $\pi$ be the prefix function of $t = x \, \# \, u$, where $\#$ is a separator that occurs in no read. The last value of $\pi$ is the length of the longest suffix of $u$ that is a prefix of $x$, because a border of $t$ cannot contain $\#$. The chain $k, \pi[k - 1], \pi[\pi[k-1] - 1], \ldots$ lists all lengths $k > 0$ of suffixes of $u$ that are prefixes of $x$, in decreasing order. The function keeps those with $k < \min(|u|, |x|)$, so the match is proper on both sides, and line L2 keeps those with $k \ge \ell$ and writes the offset $d = |u| - k$, which then satisfies $1 \le d \le |u| - \ell$. $\square$

**Lemma 2 (soundness).** Every edge that the algorithm removes is transitive.

*Proof.* Line L9 removes $(v, x, D)$ only when the mark $(x, D)$ is eliminated. Only line L8 sets this state, while it processes an edge $(v, w, a)$ and an edge $(w, x, b)$ with $a + b = D$, and only when the mark $(x, D)$ exists, that is, when $(v, x, D)$ is an edge. So $(w, a)$ is a witness. $\square$

**Lemma 3 (order of eliminations).** While line L5 processes the edge $(v, w, a)$, line L8 changes only marks $(x, s)$ with $s > a$.

*Proof.* Line L8 changes the mark $(x, a + b)$ for an edge $(w, x, b)$, and $b \ge 1$. $\square$

So when line L6 reaches $(w, a)$, its mark has its final state: later steps process offsets at least $a$ and change only larger offsets.

**Lemma 4 (moving a witness back).** Let $(v, w', a')$, $(w', w, a - a')$, $(w, x, D - a)$ and $(v, x, D)$ be edges, with $w' \ne x$. Then $(w', x, D - a')$ is an edge.

*Proof.* Place $v$ at 0, $w'$ at $a'$, $w$ at $a$ and $x$ at $D$; then $0 < a' < a < D$. Each edge says that its two reads spell the same letters where they overlap, and that the second read ends after the first. So $w'$ ends at $e' = a' + |w'|$, with $|v| < e' < a + |w| < D + |x|$. The reads $w'$ and $w$ agree on $[a, e')$, and $w$ and $x$ agree on $[D, a + |w|)$. Since $D > a$ and $e' < a + |w|$, the interval $[D, e')$ lies in both, so $w'$ and $x$ agree on it. Its length is $e' - D > |v| - D \ge \ell$, since $(v, x, D)$ is an edge. So the suffix of $w'$ that starts at offset $D - a' \ge 1$ is a prefix of $x$ of length at least $\ell$, and it is proper because $e' < D + |x|$. With $w' \ne x$, this is the edge $(w', x, D - a')$. $\square$

**Lemma 5 (completeness).** Every transitive edge $(v, x, D)$ is removed.

*Proof.* Among the witnesses of $(v, x, D)$, take one, $(w, a)$, with the smallest $a$. First, line L5 reaches $(w, a)$ and does not skip it. If $v$ has two edges to the same read, line L6 never skips. Otherwise, suppose that the mark $(w, a)$ is eliminated when line L6 reaches it. By Lemma 3 and line L8, some earlier edge $(v, w', a')$ with $a' < a$ and an edge $(w', w, a - a')$ caused this. If $w' = x$, then $v$ has the two edges $(v, x, a')$ and $(v, x, D)$ with $a' < D$, which the skip test excludes. So $w' \ne x$, and by Lemma 4, $(w', a')$ is a witness with $a' < a$, which contradicts the choice of $(w, a)$. Next, line L7 scans the edges out of $w$ by increasing offset while $a + b \le$ longest, and $D \le$ longest since $(v, x, D)$ is an edge out of $v$. So the scan reaches the edge $(w, x, D - a)$. At that moment the mark $(x, D)$ is in play or already eliminated, and after line L8 it is eliminated. Line L9 removes the edge. $\square$

**Theorem 1.** For each read $v$, line L9 keeps exactly the edges out of $v$ that have no witness.

*Proof.* Line L4 marks every edge out of $v$ in play, so line L9 keeps an edge unless its mark was eliminated. Lemma 2 says that removed edges are transitive, and Lemma 5 says that transitive edges are removed. Line L9 then clears all marks, so the marks of one vertex do not affect the next. $\square$

**Lemma 6 (spelling).** If a walk from $v$ to $x$ uses edges whose offsets add up to $D \le |v| - \ell$, then the walk spells $v[..D) \cdot x$.

*Proof.* By induction on the number of edges. A walk with no edges has $x = v$ and $D = 0$, and spells $v$. A walk that starts with $(v, w, a)$ continues with a walk from $w$ to $x$ of total offset $D - a$. The read $w$ ends after $v$, so $|w| > |v| - a$ and $D - a \le |v| - \ell - a < |w| - \ell$. By induction the rest spells $w[..D - a) \cdot x$, so the whole walk spells $v[..a) \cdot w[..D - a) \cdot x$. The read $w$ agrees with $v$ on $[a, |v|)$ and $D < |v|$, so $w[..D - a) = v[a..D)$, and the result is $v[..D) \cdot x$. $\square$

**Theorem 2 (nothing is lost).** For every overlap edge $(v, x, D)$, the string graph has a walk from $v$ to $x$ whose offsets add up to $D$, and this walk spells the same string $v[..D) \cdot x$ as the edge.

*Proof.* By strong induction on $D$. If the edge is kept, it is the walk. Otherwise, by Theorem 1 it has a witness $(w, a)$ with $1 \le a < D$. The edges $(v, w, a)$ and $(w, x, D - a)$ have smaller offsets, so by induction the string graph has a walk from $v$ to $w$ of total offset $a$ and a walk from $w$ to $x$ of total offset $D - a$. Their concatenation has total offset $D \le |v| - \ell$, so by Lemma 6 it spells $v[..D) \cdot x$, which is also the string of the edge. $\square$

**Cost of the skip.** If $v$ has at most one edge to each read, line L7 runs for $(w, a)$ only when its mark is in play at line L6. By Lemma 3 this mark then stays in play, so the edge is irreducible. Hence the inner loop runs only over the irreducible edges $(v, w)$, as in Myers' analysis.

**Termination.** Line L1 compares at most $m^2$ pairs of reads, and line L2 does the same. For each $v$, lines L4 to L9 scan the at most $\deg(v)$ edges out of $v$, and for each of them line L7 scans at most $\deg(w)$ edges. All these lists are finite, so the algorithm stops. $\blacksquare$
