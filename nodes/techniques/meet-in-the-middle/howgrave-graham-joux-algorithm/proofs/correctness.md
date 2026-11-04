---
title: The one-level HGJ search returns a correct solution, and a round with a surviving representation succeeds
proves: [correctness, termination]
status: full
---

**Notation.** For $v \in \{0, 1\}^n$ write $\langle a, v \rangle = \sum_i a_i v_i$ and $\mathrm{supp}(v) = \{i : v_i = 1\}$. For a set $X$ of positions, $|v|_X = |\mathrm{supp}(v) \cap X|$. A *solution* is a vector $e \in \{0, 1\}^n$ with $|e|_{\{0, \ldots, n-1\}} = w$ and $\langle a, e \rangle = t$. The numbers $p, q, p_1, q_1, M$ are those of lines L1 to L3. Since $0 \le p_1 \le p$ and $0 \le q_1 \le q$, $M \ge 1$, so the residues of line L6 exist.

**Lemma 1 (LIST).** For a split $(P, Q)$ of the positions, integers $i, j \ge 0$ and a residue $r$, LIST$(P, i, Q, j, r)$ returns each vector $v \in \{0, 1\}^n$ with $|v|_P = i$, $|v|_Q = j$ and $\langle a, v \rangle \equiv r \pmod M$ exactly once, and no other vector.

*Proof.* Each such $v$ is $z' + z$ for exactly one pair: $z'$ the part of $v$ on $P$, with $i$ ones, and $z$ the part on $Q$, with $j$ ones, because $P$ and $Q$ are disjoint and cover all positions. Since $\langle a, v \rangle = \langle a, z' \rangle + \langle a, z \rangle$, the condition $\langle a, v \rangle \equiv r$ holds if and only if $\langle a, z \rangle \equiv r - \langle a, z' \rangle \pmod M$, that is, if and only if $z$ is in the bucket $G[(r - \langle a, z' \rangle) \bmod M]$ of line L12. Line L14 visits each $z'$ once and each $z$ of that bucket once, and appends $z' + z$. So it appends exactly the vectors $v$ of the statement, each once. $\square$

**Lemma 2 (soundness of a round).** If line L10 returns $v = x + y$, then $v$ is a solution.

*Proof.* By Lemma 1 (line L7), $|x|_P = p_1$ and $|x|_Q = q_1$; by Lemma 1 (line L8), $|y|_P = p - p_1$ and $|y|_Q = q - q_1$. Line L10 takes $y$ from $H[t - \langle a, x \rangle]$, so $\langle a, y \rangle = t - \langle a, x \rangle$. It returns only if $\mathrm{supp}(x) \cap \mathrm{supp}(y) = \emptyset$. Then $x + y \in \{0, 1\}^n$, its number of ones is $p_1 + q_1 + (p - p_1) + (q - q_1) = p + q = w$, and $\langle a, x + y \rangle = \langle a, x \rangle + \langle a, y \rangle = t$. $\square$

**Lemma 3 (a surviving representation is found).** Consider a round with split $(P, Q)$ and residue $R$. Suppose a solution $e$ has $|e|_P = p$ and $|e|_Q = q$, and a vector $x^* \in \{0, 1\}^n$ with $\mathrm{supp}(x^*) \subseteq \mathrm{supp}(e)$, $|x^*|_P = p_1$, $|x^*|_Q = q_1$ has $\langle a, x^* \rangle \equiv R \pmod M$. Then the round returns a solution.

*Proof.* Let $y^* = e - x^*$. Since $\mathrm{supp}(x^*) \subseteq \mathrm{supp}(e)$, $y^* \in \{0, 1\}^n$, its support is disjoint from that of $x^*$, $|y^*|_P = p - p_1$ and $|y^*|_Q = q - q_1$. Also $\langle a, y^* \rangle = t - \langle a, x^* \rangle \equiv t - R \pmod M$. By Lemma 1, $x^* \in L_x$ and $y^* \in L_y$, and line L9 puts $y^*$ in $H[\langle a, y^* \rangle] = H[t - \langle a, x^* \rangle]$. Line L10 examines the pair $(x^*, y^*)$ unless it returns earlier. At that pair the supports are disjoint, so it returns. In both cases the round returns, and by Lemma 2 the result is a solution. $\square$

The number of vectors $x^*$ as in Lemma 3 for a fixed balanced $e$ is $\binom{p}{p_1}\binom{q}{q_1} = M$: choose $p_1$ of the $p$ ones of $e$ in $P$ and $q_1$ of the $q$ ones in $Q$. This is why line L3 sets $M$ to this count.

**Theorem.** For every input and every number of rounds, HGJ stops, and it returns a solution if one exists, and NONE otherwise.

*Proof.* *Termination.* The loop of line L4 runs a fixed number of rounds. In each round the lists are finite, since there are at most $2^n$ vectors, so lines L5 to L10 stop. Line L11 checks the $\binom{n}{w}$ sets of $w$ positions, a finite number.

*Correctness.* The algorithm returns either at line L10 or at line L11. A result of line L10 is a solution by Lemma 2. Line L11 returns a $w$-subset only after it checks that its sum is $t$, which is a solution, and returns NONE only after it has checked all $w$-subsets and found none, so then no solution exists. If a solution exists, either some round returns one at line L10, or line L11 is reached, and line L11 then finds one, since it checks every $w$-subset. $\blacksquare$

**Remark (what is not proved).** Lemma 3 says when a round succeeds. That a round succeeds with constant probability, and that the lists have the heuristic sizes of the page, relies on the assumption that the residues $\langle a, x \rangle \bmod M$ of the representations and of the other list entries behave like independent uniform values. This assumption is not proved; the theorem above does not use it.
