---
tag: V7F709
kind: concept
slug: fpt-w1-conjecture
name: FPT ≠ W[1] conjecture
aliases:
- FPT versus W[1]
area: complexity/parameterized-complexity
level: advanced
summary: "The conjecture that FPT is not W[1], so that clique has no f(k) n^O(1) algorithm. It implies that P is not NP, and the Exponential Time Hypothesis implies it."
prereqs: [w-hierarchy, w-hardness, fixed-parameter-tractable]
see_also: [clique-w1-completeness, parameterized-clique, strong-exponential-time-hypothesis, gap-eth, p-versus-np-problem, xp, parameterized-inapproximability, conditional-lower-bound]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 13 (FPT versus W[1] as the basic assumption for hardness) and Theorem 14.21 (no f(k) n^o(k) algorithm for clique under ETH)
  - paper: doi:10.1016/j.jcss.2006.04.007
    title: "Jianer Chen, Xiuzhen Huang, Iyad A. Kanj and Ge Xia, Strong computational lower bounds via parameterized complexity, Journal of Computer and System Sciences 72(8), 1346-1367 (2006)"
    locator: the ETH lower bound for clique, which gives that ETH implies FPT is not W[1]
  - book: isbn:9781447155584
    title: Rodney G. Downey and Michael R. Fellows, Fundamentals of Parameterized Complexity, Springer, 2013
    locator: the W hierarchy and the relation of its collapse to classical complexity
  - book: isbn:9783540299523
    title: Jörg Flum and Martin Grohe, Parameterized Complexity Theory, Springer, 2006
    locator: Chapter 2 (Reductions and Parameterized Intractability) and Chapter 16 (Subexponential Fixed-Parameter Tractability)
---

The FPT versus W[1] conjecture says that $\mathsf{FPT} \ne \mathsf{W}[1]$: some problem in the class $\mathsf{W}[1]$ of the [W-hierarchy](/w-hierarchy/) has no algorithm in time $f(k) \cdot n^{O(1)}$. Since [clique is W[1]-complete](/clique-w1-completeness/), the conjecture is the same as "p-Clique is not in FPT". It is the standard assumption behind every W[1]-hardness result. It is open: it implies that P is not NP, so a proof is out of reach, and the [Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) implies it.

## In plain words

Some problems ask for a small group with a property, such as a few people who all know each other. The conjecture says that for these problems there is no method whose cost is a fixed polynomial in the size of the input times some amount that depends only on the group size.

Nobody can prove it, because a proof would also settle the most famous open question of the field, whether every problem with easy-to-check answers has a fast method. But it follows from a stronger and widely used belief about how hard logic puzzles are. So researchers treat it as true and use it to explain why some problems resist fast methods.

## The idea

**The statement.** $\mathsf{FPT} \subseteq \mathsf{W}[1]$ always holds. The conjecture is that the inclusion is proper. By W[1]-completeness, these are equivalent:

- $\mathsf{FPT} \ne \mathsf{W}[1]$;
- [p-Clique](/parameterized-clique/) has no algorithm in time $f(k) \cdot n^{c}$ for a computable $f$ and a constant $c$;
- the same for [p-Independent-Set](/parameterized-independent-set/), multicolored clique, or any other W[1]-complete problem.

The conjecture is about FPT and W[1], not about FPT and [XP](/xp/). That FPT is a proper subset of XP is a theorem, proved by diagonalization, and it needs no assumption.

**It implies that P is not NP.** Suppose $\mathsf{P} = \mathsf{NP}$. Weighted satisfiability of a circuit $C$ with weight $k$ is in NP as a classical problem: guess $k$ inputs and evaluate $C$. So it is in P, and in particular it is in FPT for every class of circuits. A problem in W[1] has a [parameterized reduction](/parameterized-reduction/) to weighted satisfiability of weft-1 circuits of constant depth, and FPT is closed under parameterized reductions. So every problem in W[1] is in FPT, and $\mathsf{FPT} = \mathsf{W}[1]$. By contraposition, $\mathsf{FPT} \ne \mathsf{W}[1]$ implies $\mathsf{P} \ne \mathsf{NP}$. A proof of the conjecture would therefore solve the [P versus NP problem](/p-versus-np-problem/).

**The Exponential Time Hypothesis implies it.** ETH says that 3-SAT on $N$ variables has no algorithm in time $2^{o(N)}$. Chen, Huang, Kanj and Xia (2006) proved that under ETH, p-Clique has no algorithm in time $f(k) \cdot n^{o(k)}$ for any computable $f$; Cygan et al. give the proof as Theorem 14.21. An algorithm in time $f(k) \cdot n^{c}$ for a constant $c$ is of this form, because $c = o(k)$. So ETH implies that p-Clique is not in FPT, and hence $\mathsf{FPT} \ne \mathsf{W}[1]$. The chain is

$$\text{ETH} \;\Rightarrow\; \mathsf{FPT} \ne \mathsf{W}[1] \;\Rightarrow\; \mathsf{P} \ne \mathsf{NP}.$$

Neither arrow is known to reverse.

**Stronger and weaker assumptions.** The conjecture rules out only time $f(k) \cdot n^{O(1)}$. ETH rules out $f(k) \cdot n^{o(k)}$ for clique, which is much more. The [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) gives exact exponents, such as no $O(n^{k - \varepsilon})$ algorithm for [dominating set](/parameterized-dominating-set/). [Gap-ETH](/gap-eth/) gives hardness of approximation in FPT time. Higher in the hierarchy, $\mathsf{FPT} \ne \mathsf{W}[2]$ is a weaker assumption than $\mathsf{FPT} \ne \mathsf{W}[1]$, because $\mathsf{W}[1] \subseteq \mathsf{W}[2]$.

## Examples

**What the conjecture rules out.** An algorithm for clique in time $2^{2^k} n^5$ would refute it, however large the constant in front.

**What it does not rule out.** An algorithm for clique in time $n^{\sqrt{k}}$ would not refute the conjecture, since the exponent still grows with $k$. It would refute ETH. The best known algorithm, by Nešetřil and Poljak, runs in time $O(n^{\omega k/3})$, where $\omega$ is the [matrix multiplication exponent](/matrix-multiplication-exponent/), and it is consistent with both assumptions.

**Two parameters of one problem.** Under the conjecture, independent set with the set size $k$ is not FPT. Vertex cover with the cover size $k$ is FPT, with an algorithm in time $O(2^k (n + m))$. The two problems are the same classical problem, since $S$ is a vertex cover exactly when $V \setminus S$ is independent, and the conjecture says that the choice of parameter matters.

**Kernels.** A decidable problem has a kernel if and only if it is FPT. So under the conjecture, clique has no kernel of any size. Lower bounds for polynomial kernels of FPT problems use a different assumption, that NP is not a subset of coNP/poly.

## Where it is used

- *Hardness results.* Each W[1]-hardness proof gives a statement "not FPT unless $\mathsf{FPT} = \mathsf{W}[1]$". This is how [W[1]-hardness](/w-hardness/) is used in practice, in the same way as NP-hardness under P versus NP.
- *Choice of parameters.* When a problem is W[1]-hard for a natural parameter, the conjecture is the reason to look for a structural parameter, a restricted input class or an [FPT approximation](/fpt-approximation/).
- *Approximation.* [Parameterized inapproximability](/parameterized-inapproximability/) asks for hardness of approximate answers in FPT time. Some results assume only $\mathsf{FPT} \ne \mathsf{W}[1]$, and others need Gap-ETH.
- *Conditional lower bounds.* When a sharper running time bound is needed, papers use ETH or SETH instead, and the conjecture follows from those. See [conditional lower bound](/conditional-lower-bound/).

## References
