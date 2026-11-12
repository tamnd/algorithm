---
title: BUILD-OVERLAP-GRAPH returns exactly the arcs of the overlap graph, with the longest overlaps
proves: [correctness, termination]
status: full
---

**Notation.** The reads are $r_0, \ldots, r_{m-1}$, nonempty strings over a finite alphabet, indexed from 0, and $\ell \ge 1$. For $i \ne j$, $\mathrm{ov}(i, j)$ is the length of the longest string that is a proper suffix of $r_i$ and a proper prefix of $r_j$. The overlap graph has the arc $(i, j)$ with weight $\mathrm{ov}(i, j)$ exactly when $i \ne j$ and $\mathrm{ov}(i, j) \ge \ell$. Strings are compared in lexicographic order, and a proper prefix of a string is smaller than the string.

**Lemma 1 (prefix ranges).** Let $K$ be a sorted list of strings and $u$ a string of length $k$. The strings of $K$ that start with $u$ form one interval $[lo, hi)$ of positions, and the two binary searches of line L5 return it.

*Proof.* If a string $s$ starts with $u$, then $s \ge u$, and every $t$ with $u \le t \le s$ also starts with $u$: if $t$ differed from $u$ at a first position $q < k$, then $t > u$ forces $t[q] > u[q] = s[q]$ while $s$ agrees with $t$ before $q$, so $t > s$; and $t$ cannot be a proper prefix of $u$, since $t \ge u$. So the strings that start with $u$ are the strings $t$ with $u \le t$ and $t[..k) = u$, and they are consecutive in $K$. The first search finds $lo$, the first position with $K[lo] \ge u$. For $p \ge lo$ we have $K[p] \ge u$, hence $K[p][..k) \ge u$, so the predicate $K[p][..k) > u$ is false on the interval and true after it; it is monotone on $[lo, |K|)$, and the second search finds its first true position $hi$. $\square$

**Lemma 2 (each arc is found with the right weight).** After line L2 has processed read $i$, for every $j \ne i$, $\mathit{out}[i]$ contains $j$ exactly when $\mathrm{ov}(i, j) \ge \ell$, and then $\mathit{out}[i][j] = \mathrm{ov}(i, j)$.

*Proof.* Line L3 tries $k = |r_i| - 1, |r_i| - 2, \ldots, \ell$ in decreasing order, so the suffix $u$ of line L4 is always proper. By Lemma 1, line L6 visits exactly the reads $j$ that start with $u$, and it keeps those with $j \ne i$ and $|r_j| > k$, that is, those for which $u$ is a proper prefix of $r_j$. So a read $j \ne i$ passes the first two tests of line L6 at the value $k$ exactly when $u$ of length $k$ is a proper suffix of $r_i$ and a proper prefix of $r_j$. The set of such $k \ge \ell$ is empty when $\mathrm{ov}(i, j) < \ell$, and then $j$ is never added. Otherwise its largest element is $\mathrm{ov}(i, j)$, which is tried first since $k$ decreases; line L7 adds $j$ with this weight, and the test "no arc yet" keeps it from later, smaller $k$. Arcs out of $i$ are added only while $i$ is processed. $\square$

**The in-lists.** Line L7 writes $\mathit{in}[j][i] = k$ together with $\mathit{out}[i][j] = k$ and nowhere else, so $\mathit{in}[j][i] = \mathit{out}[i][j]$ for every arc.

**Termination.** Line L2 runs $m$ times, line L3 at most $|r_i|$ times for read $i$, and line L6 at most $m$ times for each $k$; each binary search halves an interval of at most $m$ positions. So the build stops after finitely many steps.

**Spelling.** For a path $i_0 \to i_1 \to \cdots \to i_t$ of arcs, SPELL writes $r_{i_0}$ and then each $r_{i_q}$ without its first $\mathrm{ov}(i_{q-1}, i_q)$ letters. That prefix equals the suffix of $r_{i_{q-1}}$ of the same length, which is the end of the text written so far. By induction on $q$, the text ends with $r_{i_q}$, contains $r_{i_0}, \ldots, r_{i_q}$, and has length $\sum_{q} |r_{i_q}| - \sum_{q \ge 1} \mathrm{ov}(i_{q-1}, i_q)$. $\blacksquare$
