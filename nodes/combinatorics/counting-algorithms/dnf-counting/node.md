---
tag: Y18288
kind: problem
slug: dnf-counting
name: Counting satisfying assignments of a DNF
aliases:
- '#DNF'
- DNF counting
- DNF model counting
area: combinatorics/counting-algorithms
level: advanced
summary: Counts assignments that satisfy a formula in disjunctive normal form.
prereqs: [sat, model-counting, inclusion-exclusion-principle]
see_also: [karp-luby-algorithm, fpras, approximate-counting, karp-luby-estimator, counting-csp, parsimonious-reduction, monte-carlo-algorithm, exact-exponential-algorithms]
sources:
  - paper: doi:10.1137/0208032
    title: Leslie G. Valiant, The complexity of enumeration and reliability problems, SIAM Journal on Computing 8(3), 410 to 421, 1979
    locator: "the #P-completeness results for counting problems with easy decision versions, including monotone 2-CNF"
  - paper: doi:10.1137/0212053
    title: J. Scott Provan and Michael O. Ball, The complexity of counting cuts and of computing the probability that a graph is connected, SIAM Journal on Computing 12(4), 777 to 788, 1983
    locator: "the #P-completeness of counting independent sets and vertex covers"
  - paper: doi:10.1109/SFCS.1983.35
    title: Richard M. Karp and Michael Luby, Monte-Carlo algorithms for enumeration and reliability problems, 24th Annual Symposium on Foundations of Computer Science (FOCS 1983), 56 to 64
    locator: the FPRAS for DNF counting
  - paper: doi:10.1016/0196-6774(89)90038-2
    title: Richard M. Karp, Michael Luby and Neal Madras, Monte-Carlo approximation algorithms for enumeration problems, Journal of Algorithms 10(3), 429 to 448, 1989
    locator: the union of sets problem, with DNF counting as the main example
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 11, Approximate Counting (the DNF counting problem)
  - paper: doi:10.1007/BF01940873
    title: Michael Luby and Boban Veličković, On deterministic approximation of DNF, Algorithmica 16(4-5), 415 to 433, 1996
    locator: the whole paper (deterministic approximate counting for DNF)
  - paper: doi:10.1007/s00037-013-0068-6
    title: Parikshit Gopalan, Raghu Meka and Omer Reingold, DNF sparsification and a faster deterministic counting algorithm, Computational Complexity 22(2), 275 to 310, 2013
    locator: the whole paper (a faster deterministic approximate counter)
  - url: https://oeis.org/A005061
    title: OEIS A005061, a(n) = 4^n - 3^n
    locator: the sequence 0, 1, 7, 37, 175, 781, ...
---

DNF counting, written #DNF, asks for the number of truth assignments that satisfy a formula $F = C_1 \lor \cdots \lor C_m$ in disjunctive normal form, where each clause $C_i$ is a conjunction of literals. Deciding whether a DNF is satisfiable is trivial, since it is enough that one clause has no complementary pair of literals, but counting is #P-complete. Exactly, #DNF is as hard as counting the solutions of CNF formulas, because the negation of a DNF is a CNF and the two counts add up to $2^n$. Approximately, the two problems are very different: the [Karp-Luby estimator](/karp-luby-algorithm/) is an [FPRAS](/fpras/) for #DNF, while #SAT for CNF has no FPRAS unless NP = RP. #DNF is the standard first example of a #P-complete problem with an efficient randomized approximation, and it appears in network reliability and in probabilistic databases.

## In plain words

A DNF formula is a list of conditions joined by "or". Each condition says that certain switches must be on and certain switches must be off, and it does not care about the other switches. A setting of all the switches satisfies the formula if it meets at least one condition.

Each condition alone is easy to count: every switch it does not mention can be on or off. The difficulty is overlap. A setting can meet many conditions, and adding up the counts of the conditions counts it many times. Finding the exact size of the overlap is hard in general. Estimating it with random samples, however, is easy and reliable.

## Definition

**Input.** A DNF formula $F = C_1 \lor \cdots \lor C_m$ over the Boolean variables $x_1, \ldots, x_n$. Each clause $C_i$ is a conjunction $\ell_1 \land \cdots \land \ell_k$ of literals, where a literal is $x_v$ or $\lnot x_v$. The size of the input is $L = \sum_i |C_i|$ plus $n$ and $m$.

**Output.** The number $\#F = |S|$, where $S = \{ a \in \{0, 1\}^n : F(a) = 1 \}$.

Let $S_i$ be the set of assignments that satisfy $C_i$, so that $S = S_1 \cup \cdots \cup S_m$. If $C_i$ contains $x_v$ and $\lnot x_v$, then $S_i = \emptyset$. Otherwise $C_i$ fixes $|C_i|$ variables, $S_i$ is a subcube of $\{0, 1\}^n$, and $|S_i| = 2^{n - |C_i|}$. So #DNF is the problem of finding the size of a union of $m$ subcubes.

## Variants

- **Weighted DNF.** Each variable $x_v$ is true with its own probability $q_v$, independently, and the output is $\Pr[F]$. This is the form used in reliability and probabilistic databases. The case $q_v = 1/2$ is $\#F / 2^n$.
- **Monotone DNF.** No negated literals. This is still #P-complete, even with two literals per clause.
- **$k$-DNF.** Every clause has at most $k$ literals.
- **Approximate #DNF.** Output $Y$ with $(1 - \varepsilon)\#F \le Y \le (1 + \varepsilon)\#F$ with probability at least $1 - \delta$, or deterministically.
- **The complement.** Counting the assignments that do not satisfy $F$ is #SAT for the CNF $\lnot F$.

## Examples

- **Three clauses.** Let $F = (x_1 \land x_2) \lor (x_2 \land x_3) \lor \lnot x_1$ with $n = 3$. Writing assignments as $x_1 x_2 x_3$, the satisfying assignments are 000, 001, 010, 011, 110 and 111, so $\#F = 6$. Inclusion-exclusion over the clauses gives the same: the clauses have $2 + 2 + 4 = 8$ assignments; the pairs $\{C_1, C_2\}$, $\{C_1, C_3\}$ and $\{C_2, C_3\}$ have $1$, $0$ and $1$ in common, since $C_1 \land C_3$ contains $x_1$ and $\lnot x_1$; all three have 0 in common. So $\#F = 8 - 2 + 0 = 6$. The [Karp-Luby page](/karp-luby-algorithm/) runs its estimator on this formula.
- **Disjoint pairs.** For $F_k = (x_1 \land x_2) \lor (x_3 \land x_4) \lor \cdots \lor (x_{2k-1} \land x_{2k})$ with $n = 2k$, an assignment fails exactly when each of the $k$ pairs avoids the value 11, which leaves 3 choices per pair. So $\#F_k = 4^k - 3^k$, which is $0, 1, 7, 37, 175, 781, \ldots$ for $k = 0, 1, 2, \ldots$ (OEIS A005061). The sum of the clause sizes is $k 4^{k-1}$, which overcounts: for $k = 3$ it is 48 instead of 37.
- **Independent sets.** For a graph $G = (V, E)$, the monotone 2-DNF $F_G = \bigvee_{uv \in E} (y_u \land y_v)$ fails exactly when $\{ v : y_v = 1 \}$ is an independent set of $G$. So $\#F_G = 2^{|V|} - (\text{number of independent sets of } G)$. For the path with 4 vertices, which has 8 independent sets, $\#F_G = 16 - 8 = 8$.

## Known algorithms

- **Enumeration.** Test all $2^n$ assignments in $O(2^n L)$ time. This is the method of choice for $n$ up to about 25.
- **Inclusion-exclusion.** $\#F = \sum_{\emptyset \ne T \subseteq [m]} (-1)^{|T|+1} |\bigcap_{i \in T} S_i|$, where each intersection is empty or a subcube whose size is a power of 2. This takes $O(2^m L)$ time and is exact; it suits formulas with few clauses and many variables. See [inclusion-exclusion](/inclusion-exclusion-principle/).
- **Branching and knowledge compilation.** Split on a variable, $\#F = \#F|_{x = 0} + \#F|_{x = 1}$, and cache the subformulas, as in exact [model counting](/model-counting/) tools. Exponential in the worst case, but often fast on structured formulas.
- **Karp-Luby estimator.** Sample a clause $C_i$ with probability proportional to $|S_i|$ and a uniform $a \in S_i$, and count the sample only if $C_i$ is the first clause that $a$ satisfies. With $N = \lceil 3m \ln(2/\delta)/\varepsilon^2 \rceil$ samples this is an FPRAS, with time $O(m (n + L) \log(1/\delta)/\varepsilon^2)$. See the [Karp-Luby estimator](/karp-luby-algorithm/).
- **Self-adjusting coverage.** Karp, Luby and Madras improved the estimator so that the total work is about $O(nm \log(1/\delta)/\varepsilon^2)$.
- **Deterministic approximation.** Luby and Veličković gave a deterministic algorithm that approximates #DNF, and Gopalan, Meka and Reingold gave a faster one. Their running times are not polynomial, and a deterministic FPTAS for #DNF is not known.

## Bounds

- **#P-completeness.** Exact #DNF is #P-complete under polynomial-time Turing reductions, even for monotone 2-DNF. By the independent set example, $\#F_G$ gives the number of independent sets of $G$, which is #P-complete (Valiant; Provan and Ball).
- **Not under parsimonious reductions.** #DNF is not #P-complete under [parsimonious reductions](/parsimonious-reduction/) unless P = NP: such a reduction from #SAT would map an unsatisfiable CNF to a DNF with no solution, which is easy to recognize, and so decide SAT.
- **Approximation.** #DNF has an FPRAS. Relative approximation of the complement count $2^n - \#F$ is as hard as approximate #SAT for CNF, which has no FPRAS unless NP = RP.
- **Inclusion-exclusion.** The sum has $2^m - 1$ terms. Many of them can be zero, but in the worst case the method takes exponential time in $m$.

## Reductions

- **CNF counting.** $\#\lnot F = 2^n - \#F$, and $\lnot F$ is a CNF with the same number of clauses and literals, by De Morgan's laws. So exact #DNF and exact #SAT reduce to each other with one query and a subtraction.
- **Union of sets.** #DNF is the special case of the union of sets problem where each set is a subcube: its size, a uniform element and membership are all easy. The Karp-Luby method works for any family with these three operations.
- **Network reliability.** For a network with independent edge failures, the event "the network is disconnected" is the union, over the minimal cuts, of the events "every edge of the cut fails". This is a monotone weighted DNF over the edges, one clause per cut. When the number of relevant cuts is polynomial, as in Karger's algorithm for small failure probabilities, the Karp-Luby method estimates it.
- **Probabilistic databases.** The lineage of a query without negation over a database with independent uncertain tuples is a monotone DNF over the tuples, and the probability of the answer is the weighted #DNF of the lineage.

## Applications

- **Reliability.** Estimating the probability that a network, a circuit or a fault tree fails, when failures are rare and plain simulation sees too few of them.
- **Probabilistic databases.** Computing the probability of query answers, where exact evaluation is #P-hard for many queries.
- **Probabilistic inference.** Weighted model counting of formulas in DNF form, and estimating the probability of a union of rare events in general.
- **Teaching.** #DNF is the standard example of a #P-complete problem with an FPRAS, and of the gap between relative and additive error.

## References
