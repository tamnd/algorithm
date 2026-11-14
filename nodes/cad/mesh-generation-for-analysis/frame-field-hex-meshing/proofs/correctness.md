---
title: A local frame update never increases the smoothness energy
proves: [correctness, termination]
status: full
---

**Setting.** The cells of a grid carry rotations $R_i \in SO(3)$. The octahedral group $O$ is the set of the 24 signed permutation matrices with determinant $+1$. It is a subgroup of $SO(3)$, so for $g \in O$ also $g^{-1} = g^{\mathsf T} \in O$. For two face-adjacent cells,

$$e(i, j) = \min_{g \in O} \lVert R_i - R_j g \rVert_F^2, \qquad E = \sum_{\{i, j\}} e(i, j),$$

where the sum is over the unordered pairs of face-adjacent cells. FRAME-SWEEP visits the free cells in a fixed order (L1). At the cell $i$ it takes, for each neighbour $j$, a $g_j \in O$ that maximizes $\operatorname{tr}(R_i^{\mathsf T} R_j g_j)$ (L4), forms $M = \sum_j R_j g_j$ (L2, L3 and L5), and replaces $R_i$ by a rotation $R'$ that maximizes $\operatorname{tr}(R'^{\mathsf T} M)$ (L6). The rotation of L6 is found by Horn's method. For a quaternion $q = (w, x, y, z)$, let $R(q)$ be the matrix with entries that are the usual quadratic forms in $q$, so that $R(q)$ is a rotation when $|q| = 1$. Let $N$ be the symmetric $4 \times 4$ matrix with $N_{aa} = f(e_a)$ and $N_{ab} = \frac12 (f(e_a + e_b) - f(e_a) - f(e_b))$ for $a \ne b$, where $f(q) = \operatorname{tr}(R(q)^{\mathsf T} M)$, and let $q$ be a unit eigenvector for the largest eigenvalue of $N$. Then $R' = R(q)$.

**Claim.** In exact arithmetic:

1. $e(i, j) = 6 - 2 \max_{g \in O} \operatorname{tr}(R_i^{\mathsf T} R_j g)$, and $e(i, j) \ge 0$. The value does not change if $R_i$ is replaced by $R_i h$ or $R_j$ by $R_j h$ with $h \in O$, and $e(i, j) = e(j, i)$.
2. $R(q)$ from L6 maximizes $\operatorname{tr}(R^{\mathsf T} M)$ over all rotations $R$.
3. One update at a cell does not increase $E$. It lowers $E$ strictly unless the old $R_i$ already maximizes $\operatorname{tr}(R^{\mathsf T} M)$.
4. A sweep stops after $O(F)$ steps for $F$ free cells, and the energies of repeated sweeps form a sequence that does not increase and converges.

**Proof of part 1.** For rotations $A$ and $B$, $\lVert A - B \rVert_F^2 = \operatorname{tr}(A^{\mathsf T} A) + \operatorname{tr}(B^{\mathsf T} B) - 2 \operatorname{tr}(A^{\mathsf T} B) = 6 - 2 \operatorname{tr}(A^{\mathsf T} B)$, because $A^{\mathsf T} A = B^{\mathsf T} B = I$. Take $A = R_i$ and $B = R_j g$, and the minimum over $g$ becomes the maximum of the trace. A squared norm is at least $0$. If $R_j$ is replaced by $R_j h$, then $g$ runs over $h g$, which is all of $O$ again because $O$ is a group. If $R_i$ is replaced by $R_i h$, then $\lVert R_i h - R_j g \rVert = \lVert R_i - R_j g h^{-1} \rVert$, because right multiplication by a rotation keeps the Frobenius norm, and $g h^{-1}$ runs over $O$. For the symmetry, $\lVert R_i - R_j g \rVert = \lVert R_i g^{-1} - R_j \rVert = \lVert R_j - R_i g^{-1} \rVert$.

**Proof of part 2.** Each entry of $R(q)$ is a quadratic form in $q$, so $f(q) = \operatorname{tr}(R(q)^{\mathsf T} M)$ is a quadratic form in $q$. A quadratic form $q^{\mathsf T} N q$ with $N$ symmetric has $q^{\mathsf T} N q = N_{aa}$ at $e_a$ and $N_{aa} + 2 N_{ab} + N_{bb}$ at $e_a + e_b$, so the formulas for $N$ recover the unique symmetric matrix with $f(q) = q^{\mathsf T} N q$ for every $q$. Every rotation is $R(q)$ for some unit quaternion $q$. Hence the largest value of $\operatorname{tr}(R^{\mathsf T} M)$ over rotations is the largest value of $q^{\mathsf T} N q$ over unit vectors $q \in \mathbb{R}^4$. By the Rayleigh quotient theorem for symmetric matrices, this is the largest eigenvalue of $N$, and it is taken at each unit eigenvector of that eigenvalue.

**Proof of part 3.** Only the edges at $i$ depend on $R_i$. With the $g_j$ of L4, the energy of these edges before the update is

$$\sum_j e(i, j) = \sum_j \big(6 - 2 \operatorname{tr}(R_i^{\mathsf T} R_j g_j)\big) = 6 d - 2 \operatorname{tr}(R_i^{\mathsf T} M),$$

with $d$ the number of neighbours, by part 1 and the choice of $g_j$. After the update, with the same $g_j$, the sum $6 d - 2 \operatorname{tr}(R'^{\mathsf T} M)$ is at most the old value by part 2. The true energy after the update takes the best $g$ for each edge, which is at most the value with the fixed $g_j$. So the edges at $i$ do not gain energy, and the other edges are unchanged. If the old $R_i$ does not maximize $\operatorname{tr}(R^{\mathsf T} M)$, the inequality of part 2 is strict, and so is the decrease.

**Proof of part 4.** A sweep visits each free cell once. A cell has at most 6 neighbours, L4 tries 24 matrices for each, and L6 works on a fixed $4 \times 4$ matrix, so each visit takes $O(1)$ steps. By part 3 the energy does not increase after any visit, and by part 1 it is at least $0$. A sequence of reals that does not increase and is bounded below converges. $\blacksquare$

**Remarks.** The limit need not be the least energy. A field can stop at a local minimum with singular curves inside. The code works in floating point and runs a cyclic Jacobi solver until the off-diagonal part is tiny, so the tests check the claims up to a tolerance of $10^{-9}$. The claims say nothing about the integer grid map or the hex mesh that a full method builds from the field. That step has no general guarantee.
