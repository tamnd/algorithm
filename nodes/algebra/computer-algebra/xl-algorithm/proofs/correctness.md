---
title: Correctness of XL with field equations
proves: [correctness]
status: full
---

We prove that one XL step returns only true information about the first coordinates of the solutions, that at the full degree it returns the exact projection, and that the solver returns exactly the solutions in $\mathbb{F}_p^n$.

**Setting.** $p$ is a prime, $\mathbb{F}_p = \mathbb{Z}/p\mathbb{Z}$, and $A = \mathbb{F}_p[x_1, \ldots, x_n] / (x_1^p - x_1, \ldots, x_n^p - x_n)$. Every element of $A$ has a unique representative in which every exponent is at most $p - 1$ (reduce $x^e$ to $x^{e - (p-1)}$ while $e \ge p$; uniqueness follows from Lemma 1 by counting dimensions). The code works with these representatives. For $F = \{f_1, \ldots, f_m\}$, let $I = (F) \subseteq A$ and $S = \{a \in \mathbb{F}_p^n : f_i(a) = 0 \text{ for all } i\}$. Let $A_1 \subset A$ be the span of $1, x_1, \ldots, x_1^{p-1}$, the univariate part.

**Lemma 1 (functions).** Evaluation gives an isomorphism of $A$ with the ring of all functions $\mathbb{F}_p^n \to \mathbb{F}_p$, and $I = \{g \in A : g(a) = 0 \text{ for all } a \in S\}$.

*Proof.* For $a \in \mathbb{F}_p^n$, $a_i^p = a_i$ by Fermat's little theorem, so evaluation at $a$ is a well-defined ring map on $A$. For $b \in \mathbb{F}_p^n$ the element $\delta_b = \prod_i (1 - (x_i - b_i)^{p-1})$ takes the value $1$ at $b$ and $0$ elsewhere, again by Fermat. So evaluation is onto the $p^n$-dimensional space of functions, and the reduced monomials, $p^n$ of them, span $A$; hence the map is bijective and the reduced representatives are unique. Every $g \in I$ vanishes on $S$. Conversely, let $g$ vanish on $S$. For $b \notin S$ some $f_i(b) \ne 0$, and $\delta_b = f_i \cdot f_i(b)^{-1} \delta_b$ as functions, so $\delta_b \in I$. Then $g = \sum_{b \notin S} g(b)\, \delta_b \in I$. $\square$

**Lemma 2 (echelon form).** Let $E$ be the reduced row echelon form of a matrix whose columns are split into a left block $N$ and a right block $U$. Then the vectors of the row space with zero entries in $N$ are exactly the combinations of the rows of $E$ that are zero in $N$.

*Proof.* Such combinations are in the row space and are zero in $N$. Conversely, let $w = \sum_i c_i E_i$ be zero in $N$. A row $E_i$ that is not zero in $N$ has its pivot, its first nonzero entry, in $N$, and in reduced form the pivot column of $E_i$ is zero in every other row. So $w$ at that column equals $c_i$, and $c_i = 0$. Hence $w$ is a combination of the rows that are zero in $N$. $\square$

**Theorem 1 (one step).** Let XL-STEP$(F, D)$ run with the columns of the univariate monomials $x_1^j$ last.

- (a) If it returns "none", then $S = \emptyset$.
- (b) If it returns univariate polynomials $g_1, \ldots, g_s$, then $g_j(a_1) = 0$ for every $a \in S$.
- (c) If $D \ge n(p-1) + \max_i \deg f_i$, the step returns "fail" exactly when $\{a_1 : a \in S\} = \mathbb{F}_p$, and otherwise the common roots of the $g_j$ are exactly $\{a_1 : a \in S\}$, or it returns "none" exactly when $S = \emptyset$.

*Proof.* Every row is a reduced product $u f_i$, an element of $I$, and so is every row of the echelon form. A row with zero entries outside the univariate block is an element $g \in I \cap A_1$. (a) A nonzero constant in $I$ vanishes on $S$ by Lemma 1 and is nowhere zero, so $S$ is empty. (b) Each $g_j \in I$ vanishes on $S$, so $g_j(a_1) = 0$.

(c) For this $D$ every reduced monomial $u$ satisfies $\deg u \le n(p-1) \le D - \deg f_i$, so the rows span $\sum_i A f_i = I$. By Lemma 2 the rows found at line L4 span $I \cap A_1$. By Lemma 1, $I \cap A_1$ is the set of univariate $g$ of degree less than $p$ that vanish on $\pi(S) = \{a_1 : a \in S\}$. If $S = \emptyset$, then $1 \in I \cap A_1$, and the reduced echelon form of a space containing the constant has the constant row $1$, so the answer is "none"; if $S \ne \emptyset$, no constant is in $I$ and the answer is not "none". If $\pi(S) = \mathbb{F}_p$, a univariate $g$ of degree less than $p$ vanishing on all of $\mathbb{F}_p$ is $0$, so no row is found and the answer is "fail". Otherwise, for $b \notin \pi(S)$ the element $1 - (x_1 - b)^{p-1}$ is in $I \cap A_1$ and equals $1$ at $b$; it is a combination of the $g_j$, so some $g_j(b) \ne 0$. With (b), the common roots are exactly $\pi(S)$, and since the span is nonzero, "fail" is not returned. $\square$

**Theorem 2 (solver).** XL-SOLVE$(F)$ terminates and returns exactly $S$.

*Proof.* Termination: the inner loop raises $D$ at most up to the full degree of Theorem 1 (c). Each stack entry with $k$ free variables pushes at most $p$ entries with $k - 1$, so at most $\sum_k p^k$ entries are processed.

We show by induction on $k$ that an entry $(\text{prefix}, G, k)$ adds to the output exactly the points $\text{prefix} \times S_G$, where $S_G \subseteq \mathbb{F}_p^k$ is the set of common zeros of $G$. For $k = 0$ each $g$ is a constant, and the prefix is output exactly when all are $0$. If $G$ has no nonzero polynomial, every point is a zero, and the code outputs them all. Otherwise the loop stops at the first $D$ with a non-"fail" answer, or at the full degree. If the answer is "none", $S_G = \emptyset$ by (a). If it returns univariate polynomials, their common roots contain $\pi(S_G)$ by (b). If it returns "fail" at the full degree, $\pi(S_G) = \mathbb{F}_p$ by (c), and the code tries all values. So the tried values contain every first coordinate of a point of $S_G$. For a tried value $c$, the substituted system $G(c, x_2, \ldots, x_k)$ has zero set $\{b : (c, b) \in S_G\}$, and by induction the child entry outputs $\text{prefix} \times \{c\} \times$ this set. The union over the tried values is $\text{prefix} \times S_G$, because values outside $\pi(S_G)$ contribute nothing. The first entry has empty prefix, $G = F$ and $k = n$, so the output is $S$. Distinct entries have distinct prefixes, so no point is output twice. $\blacksquare$
