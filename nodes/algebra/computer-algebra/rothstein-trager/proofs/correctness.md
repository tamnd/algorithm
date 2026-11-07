---
title: The Rothstein-Trager algorithm returns the logarithmic part of the integral
proves: [correctness]
status: full
---

**Setting.** $K$ is a field of characteristic $0$ with algebraic closure $\overline{K}$. $A, D \in K[x]$, $D$ squarefree, $n = \deg D \ge 1$, $\deg A < n$. $\alpha_1, \ldots, \alpha_n \in \overline{K}$ are the roots of $D$, which are distinct, so $D'(\alpha_j) \ne 0$. The residue at $\alpha_j$ is $r_j = A(\alpha_j)/D'(\alpha_j)$. $R(z) = \operatorname{res}_x(D, A - z D')$, with the Sylvester matrix of formal degrees $n$ and $n - 1$. All gcds are monic. $\log$ is a formal symbol with $(\log v)' = v'/v$, and equalities of integrals are equalities of derivatives.

**Lemma 1 (the resultant).** $R(z) = \operatorname{LC}(D)^{n-1} \prod_{j=1}^n \big(A(\alpha_j) - z D'(\alpha_j)\big)$. So $R$ has degree exactly $n$, and its roots are $r_1, \ldots, r_n$, with multiplicity.

*Proof.* For $f$ of degree $n$ with leading coefficient $a$ and roots $\alpha_j$, and any $g$ of formal degree $k$, the Sylvester determinant of formal degrees $n$ and $k$ is $a^k \prod_j g(\alpha_j)$; this is the product formula on the [resultant](/resultant/) page, and it holds for every $g$ of degree at most $k$, because both sides are polynomials in the coefficients of $g$. Apply it in $K[z]$ with $f = D$ and $g = A - z D'$, of formal degree $n - 1$. The factor $j$ is $D'(\alpha_j)(r_j - z)$, with $D'(\alpha_j) \ne 0$. So $R(z) = \operatorname{LC}(D)^{n-1} \prod_j D'(\alpha_j) \cdot \prod_j (r_j - z)$, with a nonzero constant in front. $\square$

**Lemma 2 (the gcds).** For $c \in \overline{K}$, $\gcd(D, A - c D') = \prod_{j : r_j = c} (x - \alpha_j)$ in $\overline{K}[x]$. If $c \in K$, this gcd lies in $K[x]$.

*Proof.* $D$ is squarefree, so its monic divisors in $\overline{K}[x]$ are the products of distinct $x - \alpha_j$, and $\gcd(D, G)$ is the product over the roots $\alpha_j$ of $D$ with $G(\alpha_j) = 0$. For $G = A - c D'$, $G(\alpha_j) = 0$ exactly when $A(\alpha_j) = c D'(\alpha_j)$, that is $r_j = c$, because $D'(\alpha_j) \ne 0$. If $c \in K$, the Euclidean algorithm for $D$ and $A - c D'$ runs in $K[x]$, and the monic gcd does not depend on the field. $\square$

**Theorem.** $\displaystyle \int \frac{A}{D} \, dx = \sum_{c} c \log \gcd(D, A - c D')$, where $c$ runs over the distinct nonzero roots of $R$.

*Proof.* Since $\deg A < n$ and the $\alpha_j$ are distinct, partial fractions over $\overline{K}$ give $A/D = \sum_j \lambda_j/(x - \alpha_j)$. Multiply by $x - \alpha_j$ and let $x \to \alpha_j$: since $D/(x - \alpha_j)$ at $\alpha_j$ is $D'(\alpha_j)$, $\lambda_j = A(\alpha_j)/D'(\alpha_j) = r_j$. So $A/D = \sum_j r_j/(x - \alpha_j)$. For each distinct value $c$ of the residues, with $G_c = \prod_{r_j = c} (x - \alpha_j)$, $(\log G_c)' = \sum_{r_j = c} 1/(x - \alpha_j)$. Hence

$$\Big( \sum_c c \log G_c \Big)' = \sum_c \sum_{r_j = c} \frac{c}{x - \alpha_j} = \sum_j \frac{r_j}{x - \alpha_j} = \frac{A}{D}.$$

Terms with $c = 0$ contribute $0$ and can be dropped. By Lemma 1 the distinct values $c$ are the distinct roots of $R$, and by Lemma 2 $G_c = \gcd(D, A - c D')$. $\square$

**Lemma 3 (gcd in a product of fields).** Let $q \in K[z]$ be monic and squarefree of positive degree, $L = K[z]/(q)$, and $F, G \in L[x]$. Suppose the Euclidean algorithm on $F, G$ in $L[x]$, as on line L6, finds an inverse for every leading coefficient it needs, and returns the monic $S$. Then for every root $c \in \overline{K}$ of $q$, $S(c, x) = \gcd(F(c, x), G(c, x))$.

*Proof.* The map $\phi_c : L \to \overline{K}$, $z \mapsto c$, is a well defined ring homomorphism because $q(c) = 0$; extend it to $L[x] \to \overline{K}[x]$ coefficientwise. If $u \in L$ has an inverse, then $\phi_c(u)\phi_c(u^{-1}) = 1$, so $\phi_c(u) \ne 0$. The algorithm removes leading coefficients that are $0$ in $L$, so every polynomial it keeps has an exact degree in $L[x]$, and every one that is used as a divisor, or returned, has an invertible leading coefficient. Consider one division step $a = Q b + r$ in $L[x]$, with $\operatorname{LC}(b)$ invertible and $\deg r < \deg b$. Then $\phi_c(a) = \phi_c(Q) \phi_c(b) + \phi_c(r)$, $\deg \phi_c(b) = \deg b$, and $\deg \phi_c(r) \le \deg r < \deg \phi_c(b)$, so $\phi_c(r)$ is the remainder of $\phi_c(a)$ by $\phi_c(b)$ in $\overline{K}[x]$, and $\gcd(\phi_c(a), \phi_c(b)) = \gcd(\phi_c(b), \phi_c(r))$. By induction over the steps, $\gcd(\phi_c(F), \phi_c(G)) = \gcd(\phi_c(a_{\text{last}}), 0)$, where $a_{\text{last}}$ is the last nonzero remainder. Its leading coefficient is invertible, so $\phi_c(a_{\text{last}})$ has the same degree and $\phi_c(S) = \phi_c(a_{\text{last}})/\phi_c(\operatorname{LC}(a_{\text{last}}))$ is its monic form. So $S(c, x) = \gcd(F(c, x), G(c, x))$. $\square$

**Lemma 4 (splitting).** If $u \in L$ is nonzero (as a polynomial of degree less than $\deg q$) and has no inverse, then $g = \gcd(u, q)$ in $K[z]$ has $0 < \deg g < \deg q$, and $g$ and $q/g$ are monic, squarefree and coprime, and the roots of $q$ are the disjoint union of the roots of $g$ and of $q/g$.

*Proof.* $u$ has an inverse modulo $q$ exactly when $\gcd(u, q) = 1$, by the extended Euclidean algorithm. So $\deg g > 0$. Since $u \ne 0$ and $\deg u < \deg q$, $q \nmid u$, so $g \ne q$. A factorization of a squarefree polynomial has squarefree, coprime factors, and their roots partition the roots of $q$. $\square$

**The algorithm.** We show that the output pairs $(q_i, S_i)$ satisfy $\sum_i \sum_{q_i(c) = 0} c \log S_i(c, x) = \int A/D \, dx$.

*Lines L1 to L3.* Line L1 computes $R$. The implementation evaluates the Sylvester determinant at $z = 0, \ldots, n$ and interpolates; this is exact because $\deg R \le n$ by Lemma 1. For each rational root $c \ne 0$, line L3 outputs $c \log \gcd(D, A - c D')$, the term of the theorem for $c$.

*Line L4.* Let $C_{\mathbb{Q}}$ be the set of rational roots of $R$. $q$ is the squarefree part of $R / \prod_{c \in C_{\mathbb{Q}}} (z - c)^{\mu_c}$, where $\mu_c$ is the multiplicity, made monic. So the roots of $q$ are the distinct roots of $R$ not in $C_{\mathbb{Q}}$, each simple, and $0$ is not among them. If $\deg q = 0$, all terms of the theorem are already output.

*Lines L5 to L8.* Invariant: the roots of the polynomials on the stack and of the $q_i$ already output are, together, the roots of the $q$ of line L4, each exactly once; each polynomial on the stack is monic and squarefree of positive degree. It holds at the start. A pass pops $q$ and runs the Euclidean algorithm for $F = D$ and $G = A - z D'$ in $(K[z]/(q))[x]$. If an inverse fails at line L7, Lemma 4 shows that the two pushed factors keep the invariant. Otherwise, by Lemma 3, $S(c, x) = \gcd(D, A - c D')$ for every root $c$ of $q$, so the pair $(q, S)$ of line L8 stands for exactly the terms of the theorem for the roots of $q$, and the invariant holds.

*Termination.* Each split replaces $q$ by two factors of smaller positive degree, so the total number of splits is less than the degree of the $q$ of line L4, and each pass either splits or outputs. So the loop ends, with an empty stack.

*Result.* When the loop ends, by the invariant every distinct nonzero root of $R$ is a root of exactly one output $q_i$ (degree 1 for the rational ones from line L3). By Lemma 2 and Lemma 3 the term for each root $c$ is $c \log \gcd(D, A - c D')$. So the output sum is the sum of the theorem, which is $\int A/D \, dx$. $\blacksquare$
