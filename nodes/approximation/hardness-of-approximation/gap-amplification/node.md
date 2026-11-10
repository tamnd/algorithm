---
tag: 6NC3JW
kind: technique
slug: gap-amplification
name: Gap amplification
aliases:
- gap amplifying reduction
area: approximation/hardness-of-approximation
level: advanced
summary: Turning a small NP-hard gap into a large one by a product construction, such as graph powers for clique, repetition of verifiers and games, and the powering step of Dinur.
prereqs: [gap-preserving-reduction, pcp-theorem]
see_also: [parallel-repetition-theorem, clique-inapproximability, label-cover, two-prover-one-round-game, expander-walk-sampler, gap-problem, constraint-graph, lovasz-theta-function]
sources:
  - paper: doi:10.1145/1236457.1236459
    title: Irit Dinur, The PCP theorem by gap amplification, Journal of the ACM 54(3), 2007
    locator: The main amplification lemma (powering of a constraint graph) and the overall proof of the PCP theorem
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 22, Proofs of PCP theorems and the Fourier transform technique, Section 22.2 (Dinur's gap amplification, Sections 22.2.2 to 22.2.4) and the expander construction for independent set
  - paper: doi:10.1137/S0097539795280895
    title: Ran Raz, A parallel repetition theorem, SIAM Journal on Computing 27(3), 1998
    locator: The main theorem on the value of a repeated two-prover one-round game
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 16, Theorem 16.12 and Corollaries 16.13 and 16.14 (graph products for independent set)
  - paper: doi:10.1145/226643.226652
    title: Uriel Feige, Shafi Goldwasser, László Lovász, Shmuel Safra and Mario Szegedy, Interactive proofs and the hardness of approximating cliques, Journal of the ACM 43(2), 1996
    locator: The reduction from a PCP verifier to clique and the use of repetition to enlarge the gap
---

**Gap amplification** is the technique of taking an NP-hard [gap problem](/gap-problem/) with a small gap and producing one with a large gap, by a reduction from the problem to itself (or to a close relative) that keeps YES instances good and makes NO instances much worse. The usual tool is a product: the $k$-th power of a graph, $k$ independent runs of a verifier, or $k$ parallel copies of a game. It turns "no PTAS" into "no constant ratio", and constant gaps into polynomial ones. Dinur (2007) used a careful version of it to give a combinatorial proof of the [PCP theorem](/pcp-theorem/).

## In plain words

Suppose it is hard to tell a puzzle that can be solved perfectly from one where every attempt fails a small part of the time. To make the difference easier to see, combine many copies of the puzzle into one bigger puzzle that is solved only when every copy is solved at once. A perfect solver still wins every copy. A solver who fails a little each time now fails the combined puzzle most of the time, because the small failures add up. So the hard question, which separates "perfect" from "a little imperfect", becomes a question that separates "perfect" from "mostly wrong". The cost is a bigger puzzle, so the number of copies must stay small enough for the construction to run in reasonable time. The hard part of each use is the proof that a clever solver cannot do better on the combined puzzle than on the copies.

## When it applies

- There is already an NP-hard gap $[c, s]$ for a problem $\Pi$, for example from the PCP theorem or from a [gap-preserving reduction](/gap-preserving-reduction/).
- $\Pi$ has a product operation that is closed in the problem: the power of a graph is a graph, a repeated verifier is a verifier, a repeated game is a game.
- Completeness behaves well: a good solution of $x$ gives a good solution of the product, usually with value $c^k$ or still 1.
- Soundness can be bounded: every solution of the product, not only the products of solutions, has value at most about $s^k$, or at least the gap grows.
- The size of the product is acceptable: polynomial for constant $k$, quasi-polynomial for $k = \mathrm{polylog}\, n$, which gives hardness under a weaker assumption than P $\ne$ NP.

## The template

Notation: $x$ is an instance of a maximization problem with $\mathrm{OPT}(x)$; ratios follow the site convention ($\mathrm{ALG} \ge \alpha\,\mathrm{OPT}$ with $\alpha \le 1$ for maximization, $\mathrm{ALG} \le \rho\,\mathrm{OPT}$ with $\rho \ge 1$ for minimization).

```pseudo id=main
GAP-AMPLIFY(x, k)
L1  ▷ hole: SOURCE  an NP-hard gap [c, s]: OPT(x) ≥ c or OPT(x) < s
L2  y ← PRODUCT(x, k)                         ▷ hole: graph power, sequential or parallel repetition, walks
L3  prove OPT(x) ≥ c ⇒ OPT(y) ≥ C(c, k)        ▷ hole: COMPLETENESS, lift a solution of x to y
L4  prove OPT(x) < s ⇒ OPT(y) < S(s, k)        ▷ hole: SOUNDNESS, bound every solution of y
L5  choose k = k(n) so that |y| is polynomial  ▷ hole: SIZE, or quasi-polynomial under a weaker assumption
L6  y ← CLEANUP(y)                             ▷ hole: optional, reduce degree or alphabet, keep the gap
L7  return y                                   ▷ the new gap is [C(c, k), S(s, k)]
```

Line L1 fixes the starting point. Line L2 is the construction; it is always a polynomial-time map once $k$ is fixed. Line L3 is usually easy: the product of good solutions is a good solution of the product. Line L4 is the heart of each use, because a solution of the product need not be a product of solutions; it may correlate the copies. Line L5 decides the assumption: constant $k$ gives a gap ratio $(s/c)^k$ for each constant under P $\ne$ NP, and larger $k$ needs a larger instance. Line L6 appears in Dinur's proof, where powering blows up the alphabet and an extra step brings it back to a constant while losing only a constant factor of the gap.

### Worked case: clique and the strong product

For graphs $G$ and $H$, the *strong product* $G \boxtimes H$ has vertex set $V(G) \times V(H)$, and two distinct pairs $(u, v)$ and $(u', v')$ are adjacent when ($u = u'$ or $uu' \in E(G)$) and ($v = v'$ or $vv' \in E(H)$).

*Claim.* $\omega(G \boxtimes H) = \omega(G)\,\omega(H)$.

*Proof.* If $K$ and $L$ are cliques of $G$ and $H$, then $K \times L$ is a clique of the product, by the definition. Conversely, let $Q$ be a clique of $G \boxtimes H$. For two of its elements, the first coordinates are equal or adjacent, so the set $Q_1$ of first coordinates is a clique of $G$; in the same way the set $Q_2$ of second coordinates is a clique of $H$. Then $Q \subseteq Q_1 \times Q_2$, so $|Q| \le \omega(G)\,\omega(H)$. $\blacksquare$

Now fill the holes. SOURCE: an NP-hard clique gap with $\omega \ge cN$ versus $\omega < sN$ on $N$ vertices (from [clique inapproximability](/clique-inapproximability/), for some constants $c > s$). PRODUCT: $G^{\boxtimes k}$, with $N^k$ vertices. COMPLETENESS and SOUNDNESS: by the claim, $\omega(G^{\boxtimes k}) = \omega(G)^k$, so the gap becomes $[c^k N^k, s^k N^k]$, of ratio $(s/c)^k$. SIZE: for each constant $k$ the map is polynomial. So for each constant $\alpha > 0$, clique has no $\alpha$-approximation unless P = NP. For the 5-cycle, $\omega(C_5) = 2$ and $\omega(C_5 \boxtimes C_5) = 4$.

## Classic examples

- **Graph products for clique and independent set.** The worked case above; Williamson and Shmoys, Theorem 16.12 and Corollaries 16.13 and 16.14, square the independence number by a graph product and conclude that [independent set](/maximum-independent-set/) has no constant ratio unless P = NP.
- **Sequential repetition of a PCP verifier, then FGLSS.** Running a verifier $k$ times with fresh randomness keeps completeness 1 and makes soundness $s^k$, with $kr$ random bits and $kq$ queries. The FGLSS graph of the repeated verifier has a clique gap of ratio $s^k$. With $k = \Theta(\log n)$ the graph is quasi-polynomial. With [expander walks](/expander-walk-sampler/) for the random strings, the randomness stays $O(\log n)$ and the gap is $n^{-\varepsilon}$ in polynomial size. See [clique inapproximability](/clique-inapproximability/).
- **Parallel repetition of two-prover games.** For a [two-prover one-round game](/two-prover-one-round-game/) $\mathcal{G}$ with value $1 - \varepsilon$ and answer alphabet $\Sigma$, Raz proved $\mathrm{val}(\mathcal{G}^{\otimes k}) \le (1 - \varepsilon^{c})^{\Omega(k / \log |\Sigma|)}$ for a universal constant $c$; Holenstein later gave $c = 3$. This turns a gap $[1, 1 - \varepsilon]$ for [label cover](/label-cover/) into $[1, \delta]$ for each constant $\delta > 0$. See [parallel repetition theorem](/parallel-repetition-theorem/).
- **Dinur's proof of the PCP theorem (sketch only).** The objects are [constraint graphs](/constraint-graph/) $G$ over a constant alphabet, and $\mathrm{UNSAT}(G)$ is the least fraction of violated constraints. One round has three steps. (1) Preprocessing makes $G$ a regular expander with self-loops, losing a constant factor in UNSAT. (2) Powering builds $G^t$, whose vertices hold opinions about their neighbourhoods within distance $t$ and whose constraints are walks; Dinur's main lemma gives $\mathrm{UNSAT}(G^t) \ge \Omega(\sqrt{t}) \cdot \min(\mathrm{UNSAT}(G), 1/t)$. (3) Alphabet reduction with an assignment tester (a constant-size PCP) brings the alphabet back to a constant, losing a constant factor. For a large constant $t$ the round doubles UNSAT, until it reaches a constant, and multiplies the size by a constant. Start from a 3-coloring instance with $\mathrm{UNSAT} \ge 1/|E|$ if unsatisfiable; after $O(\log |E|)$ rounds the size is polynomial and UNSAT is a constant. This is the PCP theorem. Satisfiable instances stay satisfiable at each step. Arora and Barak, Section 22.2, give the full proof.

## Variations

- **Products for minimization.** For [chromatic number](/chromatic-number/), products of graphs and the clique gap are combined in the reductions of Lund and Yannakakis and of Feige and Kilian; see [graph coloring inapproximability](/graph-coloring-inapproximability/).
- **Randomness-efficient repetition.** Instead of $k$ independent random strings, take the strings along a random walk on an expander graph. The soundness still decays exponentially in $k$, with $r + O(k)$ random bits instead of $kr$.
- **Amplification with imperfect completeness.** When completeness is $c < 1$, repetition gives $c^k$ as well as $s^k$. The ratio is still $(s/c)^k$, but problems that need completeness close to 1, such as [unique games](/unique-games-conjecture/), need other tools.
- **Amplification of a tiny gap.** Dinur's step multiplies UNSAT by a factor of order $\sqrt{t}$ only while UNSAT is below about $1/t$, and keeps the size linear. It grows a gap of $1/|E|$ to a constant, which repetition cannot do in polynomial size, because repetition needs $k \approx |E|$ copies for that.

## Pitfalls

- **The wrong product.** For the tensor product (pairs adjacent when both coordinates are adjacent), $\omega(G \times H) = \min(\omega(G), \omega(H))$, so clique does not amplify. Each problem needs a product that matches its structure.
- **Independent sets and the strong product.** The independence number is not multiplicative under the strong product: $\alpha(C_5) = 2$ but $\alpha(C_5 \boxtimes C_5) = 5$, not 4. This is the start of the theory of the Shannon capacity and of the [Lovász theta function](/lovasz-theta-function/). For independent sets, use the complement graph and the clique argument, or the product of Williamson and Shmoys.
- **Parallel repetition is not multiplicative.** There are games for which the value of two parallel copies equals the value of one copy, because the provers correlate their answers across copies. Raz's theorem gives exponential decay, but with a worse base and an exponent that depends on the alphabet size.
- **Size and assumption.** With $k$ growing, the product has $n^k$ elements. $k = \Theta(\log n)$ gives size $n^{O(\log n)}$, and the result then needs NP $\not\subseteq$ DTIME$(n^{O(\log n)})$, not P $\ne$ NP.
- **The problem changes.** A power of a MAX 3SAT instance is not a MAX 3SAT instance. Amplification for constraint problems works on general constraint graphs or label cover; a separate gap-preserving reduction must bring the result back, and it can lose part of the gap.

## Exercises

1. Show that $\omega(G \times H) = \min(\omega(G), \omega(H))$ for the tensor product, where distinct pairs are adjacent when both coordinates are adjacent.
2. Show that $\alpha(G \boxtimes H) \ge \alpha(G)\,\alpha(H)$ for all graphs, and find an independent set of size 5 in $C_5 \boxtimes C_5$.
3. A PCP verifier for 3SAT uses $r = O(\log n)$ random bits, $q$ queries, completeness 1 and soundness $1/2$. Run it $k$ times with independent random strings. Show that the soundness of the repeated verifier is at most $2^{-k}$, and bound the number of vertices of its FGLSS graph in terms of $n$, $k$ and $q$.
4. With $k = \log_2 n$ in Exercise 3, write the clique gap as a function of the number $N$ of vertices of the graph, and show that it is $2^{\Omega(\sqrt{\log N})}$ when the graph has $N = n^{\Theta(\log n)}$ vertices.
5. Use the strong product and an NP-hard clique gap of some constant ratio to show that, for each constant $\alpha \in (0, 1]$, maximum clique has no polynomial-time $\alpha$-approximation unless P = NP.

## References
