---
tag: TY9RCP
kind: theorem
slug: sensitivity-theorem
name: Sensitivity theorem
aliases:
- Huang's theorem
- sensitivity conjecture
area: complexity/communication-and-query-complexity
level: research
summary: "For every total Boolean function, s(f) is at least the square root of deg(f), so bs(f) is at most s(f)^4. Huang proved it in 2019 with a signed adjacency matrix of the hypercube."
prereqs: [sensitivity, block-sensitivity, eigenvalue, cauchy-interlacing-theorem]
see_also: [sensitivity, block-sensitivity, certificate-complexity, query-complexity, rayleigh-quotient, cauchy-interlacing-theorem, fourier-analysis-of-boolean-functions, polynomial-method]
sources:
  - paper: doi:10.4007/annals.2019.190.3.6
    title: Hao Huang, Induced subgraphs of hypercubes and a proof of the sensitivity conjecture, Annals of Mathematics 190(3) (2019)
    locator: "pp. 949 to 955; numbered as in arXiv:1907.00847 version 2: Theorem 1.1 (induced subgraphs on 2^(n-1) + 1 vertices), Lemmas 2.1 to 2.3 (interlacing, the signed matrix, the bound by the maximum degree), Theorems 1.3 to 1.5 (Gotsman-Linial, s(f) at least the square root of deg(f), bs(f) at most s(f)^4)"
  - paper: "Craig Gotsman and Nathan Linial, The equivalence of two problems on the cube, Journal of Combinatorial Theory, Series A 61(1), 142 to 146, 1992"
    locator: the equivalence between the induced subgraph problem on the cube and the relation between sensitivity and degree
  - paper: doi:10.1007/BF01263419
    title: Noam Nisan and Mario Szegedy, On the degree of Boolean functions as real polynomials, Computational Complexity 4(4) (1994)
    locator: pp. 301 to 313 (bs(f) at most 2 deg(f)^2, and the question whether s and bs are polynomially related); conference version in STOC 1992, pp. 462 to 467
  - paper: doi:10.1137/0220062
    title: Noam Nisan, CREW PRAMs and decision trees, SIAM Journal on Computing 20(6) (1991)
    locator: pp. 999 to 1007 (block sensitivity and C(f) at most s(f) bs(f))
  - paper: "Fan R. K. Chung, Zoltán Füredi, Ronald L. Graham and Paul Seymour, On induced subgraphs of the cube, Journal of Combinatorial Theory, Series A 49(1), 180 to 187, 1988"
    locator: the lower bound of order log n and the induced subgraph on 2^(n-1) + 1 vertices with maximum degree the ceiling of the square root of n
  - paper: "Avishay Tal, Properties and applications of Boolean function composition, 4th Innovations in Theoretical Computer Science Conference (ITCS 2013), 441 to 454"
    locator: the bound bs(f) at most deg(f)^2, as used in Huang, Theorem 1.5
  - paper: doi:10.1007/BF01200762
    title: David Rubinstein, Sensitivity vs. block sensitivity of Boolean functions, Combinatorica 15(2) (1995)
    locator: pp. 297 to 299 (a function with bs(f) = s(f)^2 / 2)
  - paper: doi:10.1145/3406325.3451047
    title: Scott Aaronson, Shalev Ben-David, Robin Kothari, Shravas Rao and Avishay Tal, Degree vs. approximate degree and quantum implications of Huang's sensitivity theorem, 53rd ACM Symposium on Theory of Computing (STOC 2021)
    locator: pp. 1330 to 1342 (D(f) = O(Q(f)^4) and deg(f) = O(adeg(f)^2) for total f, using Huang's theorem)
---

The sensitivity theorem says that the [sensitivity](/sensitivity/) of a total Boolean function is polynomially related to its degree, and so to its [block sensitivity](/block-sensitivity/) and to every other standard measure of [query complexity](/query-complexity/). Nisan and Szegedy asked the question in 1992, and it stayed open as the sensitivity conjecture until Hao Huang proved it in 2019. Huang's proof is about the hypercube graph: any set of more than half of its vertices induces a subgraph with a vertex of degree at least $\sqrt n$. A short argument of Gotsman and Linial turns this into $\mathrm{s}(f) \ge \sqrt{\deg(f)}$. This page gives the whole proof; the pages on sensitivity and block sensitivity define the measures.

## Statement

Let $Q^n$ be the $n$-dimensional cube graph: its vertices are the strings in $\{0,1\}^n$, and two strings are adjacent when they differ in exactly one position. For a graph $H$, $\Delta(H)$ is its largest vertex degree, and $\lambda_1(M)$ is the largest [eigenvalue](/eigenvalue/) of a symmetric matrix $M$. An induced subgraph on a vertex set $V$ keeps all edges of $Q^n$ between vertices of $V$.

**Theorem 1 (Huang 2019).** For every $n \ge 1$, every induced subgraph $H$ of $Q^n$ with $2^{n-1} + 1$ vertices has $\Delta(H) \ge \sqrt n$.

**Theorem 2 (the sensitivity theorem).** For every total Boolean function $f : \{0,1\}^n \to \{0,1\}$,

$$\mathrm{s}(f) \ge \sqrt{\deg(f)}.$$

**Corollary.** For every total $f$, $\mathrm{bs}(f) \le 2 \, \mathrm{s}(f)^4$, and with a bound of Tal, $\mathrm{bs}(f) \le \mathrm{s}(f)^4$. So sensitivity is polynomially related to $D^{dt}$, $R$, $Q$, $C$, $\mathrm{bs}$, $\deg$ and the approximate degree.

The theorem is for total functions. Here $\deg(f)$ is the degree of the unique multilinear real polynomial that equals $f$ on $\{0,1\}^n$.

## In plain words

Picture a cube in many dimensions, with one corner for each row of bits and an edge between rows that differ in one bit. Half of the corners can be chosen so that no two of them share an edge: take the rows with an even number of ones. Huang showed that if you choose one corner more than half, some chosen corner must touch many other chosen corners, at least the square root of the dimension. This fact about the cube settles an old question about yes or no rules. It shows that a rule whose answer changes under only a few single-bit flips must be simple: it can be written as a polynomial of low degree. And from there, it can be computed with few looks at its input.

## Proof

**Lemma 1 (the signed matrix).** Define $2^n \times 2^n$ matrices by

$$A_1 = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \qquad A_n = \begin{pmatrix} A_{n-1} & I \\ I & -A_{n-1} \end{pmatrix}.$$

Then $A_n^2 = n I$. The entries of $A_n$ are in $\{-1, 0, 1\}$, and $A_n[u][v] \ne 0$ exactly when $u$ and $v$ are adjacent in $Q^n$. The eigenvalues of $A_n$ are $\sqrt n$ and $-\sqrt n$, each with multiplicity $2^{n-1}$.

*Proof.* $A_1^2 = I$. By induction,

$$A_n^2 = \begin{pmatrix} A_{n-1}^2 + I & A_{n-1} - A_{n-1} \\ A_{n-1} - A_{n-1} & I + A_{n-1}^2 \end{pmatrix} = \begin{pmatrix} n I & 0 \\ 0 & n I \end{pmatrix}.$$

Order the vertices so that the first half has last bit 0. The two diagonal blocks are signed copies of $Q^{n-1}$ on the two halves, and the identity blocks join each vertex to the one that differs in the last bit. These are exactly the edges of $Q^n$. Since $A_n^2 = nI$, each eigenvalue $\lambda$ has $\lambda^2 = n$. The trace of $A_n$ is 0, so the two values $\pm \sqrt n$ have equal multiplicity. $\square$

**Lemma 2 (a large eigenvalue).** Let $V$ be a set of $2^{n-1} + 1$ vertices, and let $A_V$ be the principal submatrix of $A_n$ on the rows and columns in $V$. Then $\lambda_1(A_V) \ge \sqrt n$.

*Proof.* Let $E$ be the eigenspace of $A_n$ for $\sqrt n$, of dimension $2^{n-1}$, and let $W$ be the space of vectors that are zero outside $V$, of dimension $2^{n-1} + 1$. The dimensions add up to more than $2^n$, so there is a nonzero $v \in E \cap W$. Let $v_V$ be its restriction to $V$. Then $v_V^T A_V v_V = v^T A_n v = \sqrt n \, |v|^2 = \sqrt n \, |v_V|^2$, and the [Rayleigh quotient](/rayleigh-quotient/) gives $\lambda_1(A_V) \ge \sqrt n$. (Huang states this step with the [Cauchy interlacing theorem](/cauchy-interlacing-theorem/); the argument above is the same idea.) $\square$

**Lemma 3 (eigenvalue and degree).** Let $H$ be a graph and $M$ a symmetric matrix with $|M[u][v]| \le 1$ when $u v$ is an edge of $H$ and $M[u][v] = 0$ otherwise. Then $\lambda_1(M) \le \Delta(H)$.

*Proof.* Let $M v = \lambda_1 v$ with $v \ne 0$, and choose $u$ with $|v_u|$ largest. Then $|\lambda_1| \, |v_u| = |\sum_w M[u][w] v_w| \le \sum_{w \sim u} |v_w| \le \Delta(H) \, |v_u|$. $\square$

*Proof of Theorem 1.* Let $H$ be induced on $V$ with $|V| = 2^{n-1} + 1$. The matrix $A_V$ satisfies the condition of Lemma 3 for $H$. So $\Delta(H) \ge \lambda_1(A_V) \ge \sqrt n$ by Lemmas 2 and 3. $\square$

*Proof of Theorem 2 (Gotsman and Linial).* Let $d = \deg(f)$; if $d = 0$ there is nothing to prove. Choose a monomial $x_S = \prod_{i \in S} x_i$ with $|S| = d$ and a nonzero coefficient. Fix every variable outside $S$ to 0. Every monomial that contains such a variable vanishes, and the monomials inside $S$ keep their coefficients, so the restriction $g$ is a function of the $d$ variables in $S$ with $\deg(g) = d$. A sensitive position of $g$ at an input is also a sensitive position of $f$ at the extended input, so $\mathrm{s}(g) \le \mathrm{s}(f)$. It is enough to show $\mathrm{s}(g) \ge \sqrt d$.

The coefficient of $x_S$ in $g$ is $c = \sum_{y \in \{0,1\}^d} (-1)^{d - |y|} g(y) \ne 0$. Let $G(y) = (-1)^{g(y) + |y|}$. Since $(-1)^{g} = 1 - 2g$ and $\sum_y (-1)^{|y|} = 0$,

$$\sum_y G(y) = \sum_y (-1)^{|y|} (1 - 2 g(y)) = -2 (-1)^d c \ne 0.$$

So one of the sets $\{G = 1\}$ and $\{G = -1\}$ has more than $2^{d-1}$ vertices. Take $2^{d-1} + 1$ of them and apply Theorem 1 in $Q^d$: some chosen vertex $y$ has at least $\sqrt d$ chosen neighbors $z$. Each such $z$ has $|z| = |y| \pm 1$ and $G(z) = G(y)$, so $(-1)^{g(z)} = -(-1)^{g(y)}$, that is, $g(z) \ne g(y)$. So $g$ is sensitive at $y$ in at least $\sqrt d$ positions. $\square$

*Proof of the corollary.* Nisan and Szegedy proved $\mathrm{bs}(f) \le 2 \deg(f)^2$ (see the [polynomial method](/polynomial-method/)), so $\mathrm{bs}(f) \le 2 (\mathrm{s}(f)^2)^2 = 2 \mathrm{s}(f)^4$. Tal improved their bound to $\mathrm{bs}(f) \le \deg(f)^2$, which gives $\mathrm{bs}(f) \le \mathrm{s}(f)^4$. The other measures are polynomial in $\mathrm{bs}$; see [block sensitivity](/block-sensitivity/). $\square$

**A worked case.** Take $f = \mathrm{MAJ}_3$, with $\deg = 3$. The coefficient of $x_1 x_2 x_3$ is $-2$. The set $\{G = 1\}$ is $\{000, 111\}$ and $\{G = -1\}$ has the other 6 vertices, more than $2^2 = 4$. In the subgraph on these 6 vertices, the vertex $011$ has the neighbors $001$ and $010$, and $2 \ge \sqrt 3$. Indeed $\mathrm{MAJ}_3(011) = 1$, while flipping bit 2 or bit 3 gives value 0.

A direct computation confirms Lemma 1: for $n = 1, \ldots, 5$, the recursion gives $A_n^2 = nI$, and the nonzero entries of $A_n$ are exactly the edges of $Q^n$.

## Consequences

- **Sensitivity joins the other measures.** With the chain of known bounds, $C(f) \le \mathrm{s}(f) \, \mathrm{bs}(f) \le \mathrm{s}(f)^5$ and $D^{dt}(f) \le C_1(f) \, \mathrm{bs}(f) \le \mathrm{s}(f)^9$. Sharper chains give smaller exponents. In the other direction, $\mathrm{s}(f) \le D^{dt}(f)$ always.
- **Smooth functions are simple.** A function whose value changes under at most $k$ single flips at every input has degree at most $k^2$, and so a decision tree of depth bounded by a polynomial in $k$. Before 2019, the best bound on $\mathrm{bs}$ in terms of $\mathrm{s}$ was exponential: $\mathrm{bs}(f) = O(e^{\mathrm{s}(f)} \sqrt{\mathrm{s}(f)})$ by Kenyon and Kutin.
- **Quantum query complexity.** Aaronson, Ben-David, Kothari, Rao and Tal used Huang's theorem to prove $D^{dt}(f) = O(Q(f)^4)$ and $\deg(f) = O(\widetilde{\deg}(f)^2)$ for total $f$. The second bound is tight for OR.
- **The spectral method.** The signed matrix is a new tool for the cube. The proof uses only linear algebra, and it fits on two pages.

## Tightness

- **Theorem 1 with $2^{n-1}$ vertices fails.** The $2^{n-1}$ strings with an even number of ones form an independent set, so $\Delta = 0$. One more vertex makes $\Delta \ge \sqrt n$.
- **The constant in Theorem 1.** Chung, Füredi, Graham and Seymour built an induced subgraph on $2^{n-1} + 1$ vertices with $\Delta = \lceil \sqrt n \rceil$, so the bound is tight when $n$ is a perfect square. A full search over all vertex sets gives the least possible $\Delta$ as 2 for $n = 2$ (3 vertices), 2 for $n = 3$ (5 vertices) and 2 for $n = 4$ (9 vertices), which matches $\lceil \sqrt n \rceil$.
- **Lemma 2 is tight for every $n$.** Take the even strings and one odd string. The induced graph is a star with $n$ edges plus isolated vertices, and the largest eigenvalue of a star with $n$ edges is exactly $\sqrt n$. Here $\Delta = n$, so the gap is in Lemma 3, not in Lemma 2.
- **Theorem 2 is tight.** The OR of $k$ ANDs of $k$ bits has $n = k^2$, $\deg = k^2$ and $\mathrm{s} = k$, so $\mathrm{s} = \sqrt{\deg}$. A brute-force check for $k = 3$ gives $\mathrm{s} = 3$ and $\deg = 9$.
- **The corollary is not known to be tight.** Rubinstein's function has $\mathrm{bs}(f) = \mathrm{s}(f)^2 / 2$, and later constructions improve the constant but keep the exponent 2. Whether the exponent 4 can be lowered to 2 is open.

## History

Nisan introduced block sensitivity in 1989 to bound the time of CREW PRAMs, and he proved $C(f) \le \mathrm{s}(f) \, \mathrm{bs}(f)$. Nisan and Szegedy (STOC 1992, journal 1994) proved $\mathrm{bs}(f) \le 2 \deg(f)^2$ and asked whether $\mathrm{bs}(f)$ is at most a polynomial in $\mathrm{s}(f)$; this became the sensitivity conjecture. In 1988, Chung, Füredi, Graham and Seymour had proved that an induced subgraph of $Q^n$ on more than $2^{n-1}$ vertices has a vertex of degree at least about $\frac{1}{2} \log_2 n$, and they had built one with largest degree $\lceil \sqrt n \rceil$. Gotsman and Linial (1992) showed that a lower bound on $\mathrm{s}(f)$ in terms of $\deg(f)$ is equivalent to a lower bound on the larger of $\Delta(H)$ and $\Delta(Q^n - H)$, for every induced subgraph $H$ whose number of vertices is not $2^{n-1}$; the proof of Theorem 2 above is one direction of their equivalence. Rubinstein (1995) gave the quadratic gap between $\mathrm{s}$ and $\mathrm{bs}$. Huang posted his proof in July 2019 (arXiv:1907.00847), and it appeared in the Annals of Mathematics in the same year.

## References
