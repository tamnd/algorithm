---
title: BUILD gives a DDD whose value is the determinant and whose 1-paths are its terms
proves: [correctness]
status: full
---

Let $A$ be an $n \times n$ matrix whose nonzero entries are distinct symbols. For a set $C$ of $k$ columns, let $r = n - k$ and let $A_C$ be the $k \times k$ submatrix with rows $r, \ldots, n-1$ and the columns of $C$ in increasing order. Let $c_1 < \cdots < c_m$ be the columns of $C$ with $A[r, c] \neq 0$.

For a vertex $v$, the value $D(v)$ is defined by $D(0) = 0$, $D(1) = 1$ and $D(v) = s_v \, a_v \, D(\mathrm{hi}(v)) + D(\mathrm{lo}(v))$. A 1-path of $v$ is a path from $v$ to the 1-terminal. Its term is the product of the symbols of the vertices that the path leaves by a hi edge, with the product of their signs. Let $T(v)$ be the set of these signed terms.

For a permutation $\sigma$ of $C$ (a bijection from the rows $r, \ldots, n-1$ to $C$), write $t(\sigma) = \mathrm{sgn}(\sigma) \prod_i A[i, \sigma(i)]$, where the sign is the sign of the permutation of positions that $\sigma$ gives after the columns of $C$ are numbered $1, \ldots, k$ in increasing order. By the Leibniz formula, $\det A_C = \sum_\sigma t(\sigma)$. Let $L(C)$ be the set of the terms $t(\sigma)$ that are not zero, that is, whose entries are all nonzero.

**Lemma 1 (sign of a first-row choice).** Let $\sigma$ map row $r$ to column $c$, and let $j = 1 + |\{c' \in C : c' < c\}|$ be the position of $c$ in $C$. Let $\sigma'$ be the restriction of $\sigma$ to the rows $r+1, \ldots, n-1$, a bijection onto $C \setminus \{c\}$. Then $\mathrm{sgn}(\sigma) = (-1)^{j-1} \, \mathrm{sgn}(\sigma')$.

*Proof.* In positions, $\sigma$ sends the first row to position $j$. The inversions of $\sigma$ are the inversions of $\sigma'$ (the relative order of the other columns does not change when $c$ is removed) and the pairs of the first row with a later row whose column is left of $c$. There are exactly $j - 1$ columns left of $c$ in $C$, and each of them is the image of exactly one later row. So the number of inversions grows by $j - 1$. $\square$

The sign $s$ of line L7 is $(-1)^{|\{c' \in C : c' < c\}|} = (-1)^{j-1}$.

**Lemma 2.** For every set $C$ that the recursion reaches, $T(\mathrm{MINOR}(C)) = L(C)$, and $D(\mathrm{MINOR}(C)) = \det A_C$ as a polynomial. For $1 \le k \le m + 1$, $T(\mathrm{CHAIN}(C, k))$ is the set of the terms of $L(C)$ whose row $r$ uses one of the columns $c_k, \ldots, c_m$, and $D(\mathrm{CHAIN}(C, k))$ is the sum of these terms.

*Proof.* By induction on $|C|$, and for a fixed $C$ by induction on $m + 1 - k$.

If $C = \emptyset$, line L2 returns the 1-terminal. The only permutation is the empty one, with term $+1$. So $T = \{+1\} = L(\emptyset)$ and $D = 1 = \det A_\emptyset$.

Let $C \neq \emptyset$. If $k = m + 1$, line L6 returns the 0-terminal, which has no 1-path and value 0, and no term uses a column $c_j$ with $j > m$. So the claim holds.

Let $k \le m$ and $c = c_k$. A term of $L(C)$ whose row $r$ uses column $c$ is $A[r, c] \cdot (-1)^{j-1} \cdot t(\sigma')$ by Lemma 1, where $t(\sigma')$ is a term of $L(C \setminus \{c\})$, and each term of $L(C \setminus \{c\})$ gives one such term. By the outer induction, $h = \mathrm{MINOR}(C \setminus \{c\})$ of line L8 has $T(h) = L(C \setminus \{c\})$. By the inner induction, $l = \mathrm{CHAIN}(C, k+1)$ of line L9 holds the terms that use $c_{k+1}, \ldots, c_m$.

If $h$ is the 0-terminal, then $L(C \setminus \{c\})$ is empty, so no term uses column $c$, and line L10 returns $l$, which is correct. Else line L11 returns a vertex $v$ with symbol $A[r, c]$, sign $s = (-1)^{j-1}$, $\mathrm{hi}(v) = h$ and $\mathrm{lo}(v) = l$. A 1-path of $v$ either takes the hi edge and then a 1-path of $h$, which gives the term $s \, A[r, c] \, t$ for a term $t \in T(h)$, or takes the lo edge and then a 1-path of $l$. These are exactly the terms that use $c_k$, and the terms that use $c_{k+1}, \ldots, c_m$. The value is $D(v) = s \, A[r, c] \, D(h) + D(l)$, which is the sum of the same terms.

Last, MINOR returns $\mathrm{CHAIN}(C, 1)$ (line L5). Each term of $L(C)$ uses some nonzero entry $A[r, c_j]$ of row $r$, so the terms with columns $c_1, \ldots, c_m$ are all of $L(C)$, and the sum of all terms of the Leibniz formula is $\det A_C$. $\square$

**Theorem.** The root $\mathrm{BUILD}(A) = \mathrm{MINOR}(\{0, \ldots, n-1\})$ has $D(\mathrm{root}) = \det A$. The 1-paths of the root are in bijection with the nonzero terms of $\det A$, and the number of terms equals the number of 1-paths.

*Proof.* Lemma 2 with $C = \{0, \ldots, n-1\}$ gives $T(\mathrm{root}) = L(C)$ and the value. Two different permutations use two different sets of entries. The symbols are distinct, so their terms are different monomials, and no two terms cancel. Take two different 1-paths and the first vertex $w$ where they part. One path leaves $w$ by the hi edge, so its term contains the entry of $w$. The other leaves $w$ by the lo edge. After a lo edge, each vertex is in the same row with a larger column or in a later row, so this path never meets the entry of $w$ again. So the two paths give different sets of entries, and different terms. $\blacksquare$

**The memo and the unique table do not change the result.** The memo of MINOR and CHAIN returns a vertex that was built for the same arguments, so it returns the same vertex as a new call would. The unique table returns an old vertex $u$ when a new vertex would have the same row, column, sign, hi child and lo child. Then $u$ and the new vertex have the same value and the same 1-paths, because both are defined only by these five fields.

**Canonical form.** Order the entries row by row, and in a row by column. For each vertex $v$, its entry comes before every entry below it: a hi edge goes to a later row, and a lo edge goes to a later column of the same row. Its hi child is not the 0-terminal (line L10), so its entry is the first entry that occurs in a term of $T(v)$. Let $u$ and $v$ be two inner vertices with $T(u) = T(v)$. Then they have the same entry $e$. The terms of $T(\mathrm{hi})$ are the terms of $T(v)$ that contain $e$, with $e$ and its sign removed, and $T(\mathrm{lo})$ is the rest. So by induction on the depth, $u$ and $v$ have the same children, and their signs are equal because a term that contains $e$ has one sign. The unique table then makes $u = v$. So two vertices with the same set of signed terms are the same vertex. This is the canonical property of a [zero-suppressed BDD](/zero-suppressed-bdd/), which a DDD is, with a sign on each vertex.

**Evaluation and counting.** Each child has a smaller index than its parent, because a vertex is made after its two children. So one pass in index order computes $D$ for all vertices from the rule above. The number of 1-paths satisfies $P(0) = 0$, $P(1) = 1$ and $P(v) = P(\mathrm{hi}(v)) + P(\mathrm{lo}(v))$, because each 1-path of $v$ leaves $v$ by exactly one of its two edges. One pass in index order computes it.
