---
tag: FZH3WE
kind: theorem
slug: unique-games-subexponential-algorithm
name: Subexponential algorithm for Unique Games
aliases:
- Arora-Barak-Steurer algorithm
- ABS algorithm
- threshold rank algorithm for unique games
area: approximation/hardness-of-approximation
level: research
summary: An algorithm of time exp(k·n^O(ε)) that turns a 1 - ε^6 satisfiable unique game into a 1 - O(ε log(1/ε)) satisfying assignment, so any reduction proving the UGC must make instances much larger.
prereqs: [unique-games-conjecture, spectral-gap, cheeger-inequality, subexponential-time]
see_also: [sparsest-cut-ugc-hardness, max-cut-ugc-hardness, semidefinite-programming, gap-eth, quasi-polynomial-time, label-cover]
sources:
  - paper: "Sanjeev Arora, Boaz Barak and David Steurer, Subexponential algorithms for unique games and related problems, Proceedings of the 51st IEEE Symposium on Foundations of Computer Science (FOCS), 2010, 563 to 572"
    locator: Theorem 1.1 and Theorem 5.1 (the algorithm), Theorem 2.2 (eigenspace enumeration), Theorem 2.3 (rank bound for small-set expanders), Theorem 4.1 (decomposition) and Lemma 5.2 (label-extended graph), in the full version
  - paper: doi:10.1145/2775105
    title: Sanjeev Arora, Boaz Barak and David Steurer, Subexponential algorithms for unique games and related problems, Journal of the ACM 62(5), Article 42, 2015
    locator: the journal version of the same results
  - paper: "Alexandra Kolla and Madhur Tulsiani, Playing random and expanding unique games, manuscript, 2007; and Alexandra Kolla, Spectral algorithms for unique games, Proceedings of the 25th IEEE Conference on Computational Complexity (CCC), 2010"
    locator: the enumeration over the top eigenspace of the label-extended graph
  - paper: "Moses Charikar, Konstantin Makarychev and Yury Makarychev, Near-optimal algorithms for unique games, Proceedings of the 38th ACM Symposium on Theory of Computing (STOC), 2006"
    locator: the polynomial-time algorithm with guarantee 1 - O(sqrt(epsilon log k)), for comparison
---

Arora, Barak and Steurer (ABS, 2010) gave an algorithm that, on a [unique game](/unique-games-conjecture/) with $n$ vertices and $k$ labels that has an assignment satisfying a $1 - \varepsilon^6$ fraction of its constraints, finds an assignment satisfying a $1 - O(\varepsilon \log(1/\varepsilon))$ fraction in time $\exp(k \, n^{O(\varepsilon)}) \operatorname{poly}(n)$. For fixed $\varepsilon$ this is [subexponential](/subexponential-time/) but not polynomial, so it does not refute the [Unique Games Conjecture](/unique-games-conjecture/). It shows that unique games are much easier than 3SAT or [label cover](/label-cover/), which are believed to need time $2^{\Omega(n)}$, and so a reduction from 3SAT that proves the conjecture must produce instances of size $n^{1/\varepsilon^{c}}$ if the exponential time hypothesis holds. The method splits the constraint graph into pieces with few eigenvalues near $1$, and on each piece searches the span of the top eigenvectors.

## Statement

On this page a maximization ratio means $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$. A unique game has a regular constraint graph $G$ on $n$ vertices, a label set $[k]$ and a bijection on each edge, and its value is the largest fraction of edges that one labeling satisfies. For a regular graph $G$, viewed as a symmetric stochastic matrix, the *threshold rank* $\operatorname{rank}_{\tau}(G)$ is the number of eigenvalues $\lambda$ with $|\lambda| > \tau$, counted with multiplicity.

**Theorem (ABS 2010, Theorem 5.1).** There is an algorithm that, given $\varepsilon > 0$ and a unique game on $n$ vertices with $k$ labels and value at least $1 - \varepsilon^6$, outputs an assignment that satisfies at least a $1 - O(\varepsilon \log(1/\varepsilon))$ fraction of the constraints, in time $\exp(k \, n^{O(\varepsilon)}) \operatorname{poly}(n)$.

Their Theorem 1.1 states the result in another form: there is an absolute constant $\alpha > 0$ and an algorithm of time $\exp(k n^{\varepsilon^\alpha})$ that turns a unique game of value at least $1 - \varepsilon$ into an assignment of value at least $1 - \varepsilon^{\alpha}$. ABS report that $\alpha$ is about $\tfrac16$, which matches the power $6$ above.

The proof uses three results of the same paper, which are stated here with their numbers in the full version.

- **Eigenspace enumeration (Theorem 2.2).** In time $\exp(\operatorname{rank}_{1-\eta}(G)) \operatorname{poly}(n)$ one can list sets so that, if $G$ has a set $S$ with expansion $\Phi(S) \le \varepsilon$, one listed set differs from $S$ in at most $8(\varepsilon/\eta)|S|$ vertices.
- **Rank bound for small-set expanders (Theorem 2.3).** If $\operatorname{rank}_{1-\eta}(G) \ge n^{100\eta/\gamma}$, then $G$ has a set of at most $n^{1-\eta/\gamma}$ vertices with expansion at most $\sqrt{\gamma}$, and one can find it in polynomial time.
- **Decomposition (Theorem 4.1).** In polynomial time one can partition the vertices of $G$ into parts $A_1, \ldots, A_q$ so that at most an $O(\varepsilon \log(1/\varepsilon))$ fraction of the edges cross between parts, and each part satisfies $\operatorname{rank}_{1-\varepsilon^5}(G[A_i]) \le n^{100\varepsilon}$.

## In plain words

Unique games are the puzzle behind a famous guess about which problems are hard to solve even roughly. This result gives a method that is much faster than trying everything, though not fast in the usual sense. The key fact is about networks: if a network has many patterns of slow mixing, then it contains a small group of points that is nearly cut off from the rest. So the method keeps cutting off such groups, which removes only a few links, until every piece has only a few slow patterns. In a piece like that, every near-perfect answer looks like a mix of those few patterns, and the method can try all such mixes. The result does not show the guess is false, but it shows that any proof of the guess must turn small puzzles into very large ones.

## Proof

A proof sketch is in [proofs/sketch.md](proofs/sketch.md). It proves in full the eigenspace enumeration (Theorem 2.2), the bound on the threshold rank of the label-extended graph (Lemma 5.2), and the final counting (Lemma 5.4). It cites the rank bound for small-set expanders and the decomposition theorem, and describes their proofs in outline.

The algorithm has four steps.

1. Make the game *lazy*: add self-loops with the identity bijection that carry half of the weight at each vertex. This changes values by a factor of at most $2$ in the distance from $1$.
2. Partition the constraint graph into parts of small threshold rank by the decomposition theorem, and drop the constraints between parts.
3. On each part, form the *label-extended graph*, which has a vertex $(i, a)$ for each vertex $i$ and label $a$, and an edge between $(i, a)$ and $(j, \pi(a))$ for each constraint $(i, j, \pi)$. A good labeling is a set with one vertex per cloud and small expansion. Its threshold rank is at most $k$ times that of the part, by a count of closed walks.
4. Run eigenspace enumeration on each label-extended part, turn each listed set into a labeling of the part, and keep the best one.

The running time is $\exp(k n^{100\varepsilon})$ times a polynomial, from step 4. The guarantee comes from the expansion of the set of the optimal labeling, which is at most the fraction of its violated constraints, and from the bound $8(\varepsilon_t / \varepsilon^5)$ on the error of enumeration in a part where the optimum violates an $\varepsilon_t$ fraction.

## Consequences

- **Limits on proofs of the UGC.** Suppose a reduction maps 3SAT instances of size $n$ to unique games of size $N$ with completeness $1 - \varepsilon^6$ and soundness below $1 - O(\varepsilon\log(1/\varepsilon))$. Composed with the algorithm, it solves 3SAT in time $\exp(k N^{O(\varepsilon)})$. Under the exponential time hypothesis, which says that 3SAT needs time $2^{\Omega(n)}$, this forces $N \ge n^{\Omega(1/\varepsilon)}$ when $k$ is a constant. So the reduction cannot have size linear in $n$, as the gadget reductions from label cover of [Håstad's 3-bit PCP](/hastad-3bit-pcp/) do.
- **Limits on UG-hardness.** A problem that is UG-hard cannot be shown, by a reduction from unique games, to need time $2^{n^{1 - o(1)}}$, because unique games with constant parameters take time $\exp(n^{O(\varepsilon)})$.
- **Small-set expansion.** The same method gives an algorithm of time $\exp(n^{O(\varepsilon)}/\delta)$ for finding small non-expanding sets in graphs (Theorem 1.2 of the paper), and subexponential algorithms with improved guarantees for multicut and for [max cut](/max-cut-ugc-hardness/), [sparsest cut](/sparsest-cut-ugc-hardness/) and vertex cover on graphs of low threshold rank (Section 6).
- **Comparison with SDP algorithms.** The polynomial-time algorithm of Charikar, Makarychev and Makarychev satisfies a $1 - O(\sqrt{\varepsilon \log k})$ fraction of the constraints. Its loss grows with $k$, while the loss of the ABS algorithm does not depend on $k$, but ABS need subexponential time.

## Tightness

**Not polynomial.** For a fixed $\varepsilon$ the running time is $\exp(n^{O(\varepsilon)})$. If an algorithm of time $\exp(n^{o(1)})$ existed for every fixed $\varepsilon$, the UGC would be false under the exponential time hypothesis, so improving the exponent to $o(1)$ is as hard as refuting the conjecture in that form.

**Completeness.** The algorithm needs value $1 - \varepsilon^6$ to output value $1 - O(\varepsilon \log(1/\varepsilon))$, so it loses a power of $\varepsilon$. ABS note obstacles to making the exponent in the form of their Theorem 1.1 smaller than $\tfrac12$, so for small $k$ the polynomial-time guarantee of Charikar, Makarychev and Makarychev is better.

**The rank bound.** Theorem 2.3 extends the hard direction of [Cheeger's inequality](/cheeger-inequality/): Cheeger gives a non-expanding set of measure up to $\tfrac12$ from one eigenvalue near $1$, while Theorem 2.3 gives a set of measure inversely related to the number of such eigenvalues. ABS make no attempt to optimize the constant $100$ in the exponent.

## History

Kolla and Tulsiani (2007) gave an algorithm whose time is exponential in the threshold rank of the label-extended graph, and used it for unique games on expanders. Kolla (2010) related this to the threshold rank of the constraint graph for some graphs. Arora, Barak and Steurer presented the subexponential algorithm at FOCS 2010, with the decomposition theorem as the new part, and the journal version appeared in 2015.

## References
