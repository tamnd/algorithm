---
tag: AYY19J
kind: concept
slug: good-characterization
name: Good characterization (NP ∩ co-NP)
aliases:
- Good characterization
area: complexity/complexity-classes
level: core
summary: "A problem with short certificates for both yes and no answers, so it is in NP intersect coNP. Such a problem is not NP-complete unless NP = coNP, and it is often later found to be in P."
prereqs: [np, co-np]
see_also: [co-np, konig-theorem, lp-duality, pratt-certificate, max-flow-min-cut-theorem, tutte-berge-formula, integer-factorization, aks-primality-test]
sources:
  - paper: doi:10.6028/jres.069B.004
    title: Jack Edmonds, Minimum partition of a matroid into independent subsets, Journal of Research of the National Bureau of Standards 69B (1965), 67 to 72
    locator: the notion of a good characterization
  - paper: doi:10.4153/CJM-1965-045-4
    title: Jack Edmonds, Paths, trees, and flowers, Canadian Journal of Mathematics 17 (1965), 449 to 467
    locator: Section 2, good algorithms
  - paper: doi:10.1137/0204018
    title: Vaughan R. Pratt, Every prime has a succinct certificate, SIAM Journal on Computing 4(3) (1975), 214 to 220
    locator: primality is in NP
  - paper: "Leonid G. Khachiyan, A polynomial algorithm in linear programming, Doklady Akademii Nauk SSSR 244(5) (1979), 1093 to 1096; English translation in Soviet Mathematics Doklady 20 (1979), 191 to 194"
    locator: the ellipsoid method for linear programming
  - paper: doi:10.4007/annals.2004.160.781
    title: Manindra Agrawal, Neeraj Kayal and Nitin Saxena, PRIMES is in P, Annals of Mathematics 160(2) (2004), 781 to 793
    locator: the main theorem
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Chapter 10, coNP and function problems (NP intersect coNP and primality)
---

A decision problem has a *good characterization* when every yes-instance and every no-instance has a short certificate that can be checked in polynomial time. In the language of complexity classes, the problem is in $\mathsf{NP} \cap \mathsf{coNP}$. Jack Edmonds introduced the term in 1965, in his work on matchings and matroids, where min-max theorems give such certificates. A problem with a good characterization is not NP-complete unless $\mathsf{NP} = \mathsf{coNP}$, and many such problems were later shown to be in [P](/p/).

## In plain words

Suppose you claim that a graph has a large matching. You can prove it by showing the matching. Suppose instead you claim that the graph has no large matching. For some problems there is a short proof of that too, such as a small set of vertices that touches every edge.

A problem has a good characterization when both claims, yes and no, always have short proofs that anyone can check quickly. Such problems are special. They are unlikely to be among the hardest problems in their class, because those hardest problems seem to have short proofs only for the yes side. Several famous problems, such as matching, linear programming and testing whether a number is prime, first got a good characterization and later a fast algorithm.

## The idea

### Definition

A language $L$ is in [NP](/np/) when its yes-instances have certificates of polynomial length that a polynomial-time verifier checks. It is in [coNP](/co-np/) when its no-instances have such certificates. A good characterization of $L$ is a pair of verifiers, one for each side, and so

$$L \text{ has a good characterization} \iff L \in \mathsf{NP} \cap \mathsf{coNP}.$$

Every problem in P has a good characterization with empty certificates, so $\mathsf{P} \subseteq \mathsf{NP} \cap \mathsf{coNP}$. Whether this inclusion is strict is open.

### Min-max theorems

Most good characterizations come from a min-max theorem: a theorem that says that the maximum of one quantity equals the minimum of another. Consider "does the graph have a matching with at least $k$ edges?" for a bipartite graph.

- A matching with $k$ edges is a yes-certificate.
- Every edge of a matching needs its own vertex in a vertex cover, so the size of a maximum matching is at most the size of a minimum vertex cover. A vertex cover with fewer than $k$ vertices is therefore a no-certificate.
- [König's theorem](/konig-theorem/) says that the two numbers are equal for bipartite graphs, so a no-certificate always exists.

The easy inequality (weak duality) shows that the certificates are sound. The hard equality (strong duality) shows that they always exist. Other min-max theorems of this kind are [LP duality](/lp-duality/), the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) and the [Tutte-Berge formula](/tutte-berge-formula/) for matchings in general graphs.

### A good characterization is evidence against NP-completeness

**Claim.** If a problem $L \in \mathsf{NP} \cap \mathsf{coNP}$ is NP-complete under polynomial-time many-one reductions, then $\mathsf{NP} = \mathsf{coNP}$.

**Proof.** Let $A \in \mathsf{NP}$. Then $A \le_p L$ by some map $f$, so $x \in A$ exactly when $f(x) \in L$. Since $L \in \mathsf{coNP}$, a no-instance $f(x)$ of $L$ has a short certificate, and that certificate shows $x \notin A$. So $A \in \mathsf{coNP}$, and $\mathsf{NP} \subseteq \mathsf{coNP}$. Taking complements gives $\mathsf{coNP} \subseteq \mathsf{NP}$. $\square$

The claim also holds for polynomial-time Turing reductions, because a polynomial-time machine that asks questions to an oracle in $\mathsf{NP} \cap \mathsf{coNP}$ decides only languages in $\mathsf{NP} \cap \mathsf{coNP}$: a certificate lists the oracle answers together with a certificate for each answer.

Most researchers believe $\mathsf{NP} \ne \mathsf{coNP}$, so a good characterization is taken as strong evidence that a problem is not NP-complete. It is weaker evidence that the problem is in P.

### History

Edmonds gave a polynomial-time algorithm for maximum matching in general graphs in 1965, and in the same year he used the phrase "good characterization" for a description of a problem that gives short proofs of both answers. The pattern of a good characterization followed by an algorithm repeated:

| Problem | Good characterization | Polynomial-time algorithm |
|---|---|---|
| Maximum matching | König (bipartite), Tutte and Berge (general) | Edmonds, 1965 ([blossom algorithm](/edmonds-blossom/)) |
| Linear programming | LP duality | Khachiyan, 1979 ([ellipsoid method](/ellipsoid-method/)) |
| Primality | Pratt, 1975 | Agrawal, Kayal and Saxena, 2004 ([AKS test](/aks-primality-test/)) |
| Factoring (decision version) | prime factorization with primality certificates | not known |

Factoring is the main problem in $\mathsf{NP} \cap \mathsf{coNP}$ with no known polynomial-time algorithm. Much of public-key cryptography assumes that no such algorithm exists.

## Examples

**König's theorem on a small graph.** Take the bipartite graph with left vertices $a_1, a_2, a_3, a_4$, right vertices $b_1, b_2, b_3, b_4$ and the 7 edges $a_1 b_1$, $a_1 b_2$, $a_2 b_1$, $a_3 b_1$, $a_3 b_3$, $a_3 b_4$, $a_4 b_1$. The matching $\{a_1 b_2, a_2 b_1, a_3 b_3\}$ has 3 edges, which proves that a matching of size 3 exists. The vertex set $\{a_1, a_3, b_1\}$ touches all 7 edges, which proves that no matching of size 4 exists. An exhaustive search confirms that 3 is the maximum matching size and the minimum vertex cover size, and that $\{a_1, a_3, b_1\}$ and $\{a_3, b_1, b_2\}$ are the only vertex covers of size 3.

**LP duality.** Maximize $x + y$ subject to $x + 2y \le 4$, $3x + y \le 6$, $x, y \ge 0$. Is the maximum at least $14/5$? The point $(x, y) = (8/5, 6/5)$ satisfies both constraints with equality and has $x + y = 14/5$, so the answer is yes. Is the maximum at least $3$? Add the first constraint times $2/5$ and the second times $1/5$:

$$\tfrac{2}{5}(x + 2y) + \tfrac{1}{5}(3x + y) = x + y \le \tfrac{2}{5} \cdot 4 + \tfrac{1}{5} \cdot 6 = \tfrac{14}{5}.$$

So every feasible point has $x + y \le 14/5 < 3$, and the multipliers $(u, v) = (2/5, 1/5)$ are the no-certificate. They form an optimal solution of the [dual program](/lp-duality/) "minimize $4u + 6v$ subject to $u + 3v \ge 1$, $2u + v \ge 1$, $u, v \ge 0$", whose value is also $14/5$. The vertices of the feasible region are $(0, 0)$, $(2, 0)$, $(0, 2)$ and $(8/5, 6/5)$.

**A Pratt certificate.** A divisor proves that a number is composite. To prove that $p = 1009$ is prime, Pratt's certificate gives a generator $g = 11$ of the multiplicative group modulo $p$ and the factorization $p - 1 = 1008 = 2^4 \cdot 3^2 \cdot 7$. The checks are $11^{1008} \equiv 1$, $11^{504} \equiv 1008$, $11^{336} \equiv 374$ and $11^{144} \equiv 935 \pmod{1009}$: the first value is 1 and the other three are not, so 11 has order exactly 1008 and $p$ is prime. The prime factors 2, 3 and 7 get their own certificates in the same way (generator 2 for 3, generator 3 for 7), and the whole tree has 8 nodes. See [Pratt certificate](/pratt-certificate/).

**Factoring.** Let $\text{FACT} = \{ (N, k) : N \text{ has a prime factor at most } k \}$. A yes-certificate is a divisor $d$ of $N$ with $1 < d \le k$, because the smallest prime factor of $d$ is then a prime factor of $N$ at most $k$. A no-certificate is the complete prime factorization of $N$ with a Pratt certificate for each prime, all primes being greater than $k$. Both certificates have polynomial length in the bit length of $N$, so $\text{FACT} \in \mathsf{NP} \cap \mathsf{coNP}$. Binary search on $k$ with a decision algorithm for FACT would find the smallest prime factor, so a polynomial-time algorithm for FACT would factor integers in polynomial time. See [integer factorization](/integer-factorization/).

## Where it is used

In combinatorial optimization, a min-max theorem is the usual first step toward an algorithm, and the dual certificate is the usual proof that an algorithm's output is optimal. Primal-dual algorithms, such as the [Hungarian algorithm](/hungarian-algorithm/), output a solution together with a dual certificate of its optimality. In complexity theory, membership in $\mathsf{NP} \cap \mathsf{coNP}$ is the standard argument that a problem, such as factoring or the discrete logarithm, is not NP-complete, and so the standard candidates for [NP-intermediate](/np-intermediate/) problems are taken from this class.

## References
