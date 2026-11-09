---
tag: X424VA
kind: problem
slug: 3-sat
name: 3-SAT
aliases:
- 3-CNF satisfiability
- 3-satisfiability
- 3SAT
- k-SAT
area: logic-and-constraints/sat-solving
level: intro
summary: SAT restricted to clauses of at most three literals. It is NP-complete by Karp's reduction from SAT, and the best known algorithms take about 1.307^n time.
prereqs: [sat, conjunctive-normal-form, clause, np-complete]
see_also: [k-sat, 2-sat, cook-levin-theorem, schoning-algorithm, ppsz-algorithm, satisfiability-threshold, max-sat, karps-21-np-complete-problems]
sources:
  - paper: "Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (eds.), Complexity of Computer Computations, Plenum Press, 85 to 103 (1972)"
    locator: the reduction from SATISFIABILITY to SATISFIABILITY WITH AT MOST 3 LITERALS PER CLAUSE
  - paper: doi:10.1145/800157.805047
    title: Stephen A. Cook, The complexity of theorem-proving procedures, Proceedings of the 3rd ACM Symposium on Theory of Computing (STOC 1971), 151 to 158
    locator: the NP-completeness of SAT and of 3-SAT
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness (1979)
    locator: Section 3.1.1 (3-SATISFIABILITY) and problem LO2 in the appendix
  - paper: doi:10.1006/jcss.2000.1727
    title: Russell Impagliazzo and Ramamohan Paturi, On the complexity of k-SAT, Journal of Computer and System Sciences 62(2), 367 to 375 (2001)
    locator: the exponential time hypothesis
  - paper: doi:10.1007/s00453-001-0094-7
    title: Uwe Schöning, A probabilistic algorithm for k-SAT based on limited local search and restart, Algorithmica 32(4), 615 to 623 (2002)
    locator: the (4/3)^n bound for 3-SAT
  - paper: doi:10.1137/120868177
    title: Timon Hertli, 3-SAT faster and simpler, unique-SAT bounds for PPSZ hold in general, SIAM Journal on Computing 43(2), 718 to 729 (2014)
    locator: the PPSZ bound of about 1.308^n for general 3-SAT
  - paper: "Craig A. Tovey, A simplified NP-complete satisfiability problem, Discrete Applied Mathematics 8(1), 85 to 89 (1984)"
    locator: the result on 3-SAT with few occurrences of each variable
  - paper: "David Lichtenstein, Planar formulae and their uses, SIAM Journal on Computing 11(2), 329 to 343 (1982)"
    locator: the NP-completeness of planar 3-SAT
  - paper: "Vasek Chvátal and Endre Szemerédi, Many hard examples for resolution, Journal of the ACM 35(4), 759 to 768 (1988)"
    locator: the exponential resolution lower bound for random 3-CNF formulas
---

3-SAT is the [satisfiability problem](/sat/) for formulas in [conjunctive normal form](/conjunctive-normal-form/) where each [clause](/clause/) has at most three literals. It is [NP-complete](/np-complete/): Karp in 1972 reduced general SAT to it by splitting long clauses with new variables, and it became the usual starting point for proofs of NP-hardness. One literal less per clause gives [2-SAT](/2-sat/), which is solvable in linear time. The best known algorithms for 3-SAT take exponential time, about $1.307^n$ for $n$ variables, and the [exponential time hypothesis](/k-sat/) says that $2^{o(n)}$ time is impossible. The general case with $k$ literals per clause is on the page [k-SAT](/k-sat/).

## In plain words

You have many yes-or-no choices, and a list of rules. Each rule names at most three choices and says that at least one of them must go a certain way. The question is whether some way of making all the choices obeys every rule.

This looks like a small change from rules with two parts, which are easy. But with three parts, no fast method is known, and there is good reason to think none exists: every problem whose answers can be checked quickly can be rewritten as such a list of rules. A rule with many parts can be cut into rules with three parts, with a few new helper choices that pass the "at least one" along the chain. So rules with three parts are as hard as rules of any size.

## Definition

We use the notation of the area: $n$ variables, $m$ clauses, and $|F|$ literal occurrences.

**Input.** A CNF formula $F = C_1 \wedge \cdots \wedge C_m$ over $x_1, \ldots, x_n$ where each clause $C_j$ has at most 3 literals.

**Output.** The decision version asks whether some $x \in \{0,1\}^n$ makes each clause true. The search version also asks for such an $x$. By self-reduction the two are equally hard up to a factor $n$: fix $x_1 = 1$, ask the decision version, keep the value if the answer is yes and else set $x_1 = 0$, then go on with $x_2$.

**Exactly three literals.** Some authors ask for exactly three distinct literals per clause (E3-SAT). The two versions are equally hard. A clause $(\ell_1 \vee \ell_2)$ is equivalent to $(\ell_1 \vee \ell_2 \vee z) \wedge (\ell_1 \vee \ell_2 \vee \neg z)$ with a new variable $z$, and a unit clause is padded in the same way with two new variables and four clauses.

## Variants

- **MAX-3-SAT.** Satisfy as many clauses as possible. A random assignment satisfies $7/8$ of the clauses of exactly three literals in expectation, and Håstad proved that $7/8 + \varepsilon$ is NP-hard to reach. See [MAX-SAT](/max-sat/) and [the inapproximability of MAX-3-SAT](/max-3sat-inapproximability/).
- **#3-SAT.** Count the models. It is #P-complete, as for SAT; see [model counting](/model-counting/).
- **Not-all-equal 3-SAT and 1-in-3-SAT.** Each clause must have a true and a false literal, or exactly one true literal. Both are NP-complete, even with no negated literals (Schaefer 1978), and both are standard sources of reductions.
- **Few occurrences.** With exactly three distinct variables per clause, 3-SAT stays NP-complete when each variable occurs at most four times, while each such formula where each variable occurs at most three times is satisfiable (Tovey 1984).
- **Planar 3-SAT.** The graph of variables and clauses is planar. It stays NP-complete (Lichtenstein 1982) and is used for hardness proofs of geometric problems.
- **Random 3-SAT.** Draw $m = \alpha n$ clauses at random. Formulas are almost always satisfiable for small $\alpha$ and almost never for large $\alpha$, and the change is predicted at $\alpha \approx 4.267$. See [the satisfiability threshold](/satisfiability-threshold/).

## Examples

**A satisfiable formula.** The four clauses

$$(x_1 \vee x_2 \vee x_3) \wedge (\neg x_1 \vee \neg x_2 \vee x_3) \wedge (x_1 \vee \neg x_2 \vee \neg x_3) \wedge (\neg x_1 \vee x_2 \vee \neg x_3)$$

each exclude one of the four assignments of even parity, so the models are the four assignments with $x_1 \oplus x_2 \oplus x_3 = 1$: $100$, $010$, $001$ and $111$. This is the CNF form of one [XOR clause](/xor-sat/).

**An unsatisfiable formula.** The eight clauses on $x_1, x_2, x_3$ with all eight sign patterns exclude all eight assignments, so the formula has no model. Any seven of them have exactly one model, the assignment that the missing clause would exclude.

**Karp's split of a long clause.** The clause $(x_1 \vee x_2 \vee x_3 \vee x_4 \vee x_5)$ becomes

$$(x_1 \vee x_2 \vee y_1) \wedge (\neg y_1 \vee x_3 \vee y_2) \wedge (\neg y_2 \vee x_4 \vee x_5).$$

If all five $x_i$ are false, the first clause forces $y_1$, the second forces $y_2$, and the third is false. If $x_3$ is true, then $y_1 = 1$ and $y_2 = 0$ satisfy all three.

## Known algorithms

| algorithm | bound | notes |
|---|---|---|
| Brute force over all assignments | $O(2^n \lvert F \rvert)$ worst case | checks each model |
| Monien and Speckenmeyer (1985), branching on a short clause | $O^*(1.619^n)$ worst case | deterministic, a refined version of [DPLL](/dpll/) |
| [Schöning's random walk](/schoning-algorithm/) (1999) | $O^*((4/3)^n)$ expected, one-sided error | proved on its page |
| [PPSZ](/ppsz-algorithm/) (2005), with Hertli (2014) | $O^*(1.3071^n)$ expected, one-sided error | random order plus bounded resolution |
| Biased PPSZ (Hansen, Kaplan, Zamir and Zwick 2019) | $O^*(1.30698^n)$ expected | a small gain over PPSZ |
| [CDCL](/cdcl/) solvers | exponential in the worst case | the method of choice in practice |
| [WalkSAT](/walksat/) and other [local search](/local-search/) | no bound; cannot prove UNSAT | fast on many satisfiable random formulas, measured |

Here $O^*$ hides factors polynomial in $n$ and $|F|$. A deterministic version of Schöning's bound, $O^*((4/3 + \varepsilon)^n)$ for each $\varepsilon > 0$, is due to Moser and Scheder (2011).

## Bounds

- **NP-complete.** 3-SAT is in NP, since a model is a certificate that is checked in $O(|F|)$ time. It is NP-hard by the reduction below from SAT, which is NP-complete by the [Cook-Levin theorem](/cook-levin-theorem/).
- **No polynomial algorithm is known.** One would give P = NP.
- **Exponential time hypothesis (ETH).** Impagliazzo and Paturi (2001) state the hypothesis that some $\delta > 0$ exists such that 3-SAT has no $O(2^{\delta n})$ algorithm. ETH is not proved. With the sparsification lemma of Impagliazzo, Paturi and Zane, ETH also rules out $2^{o(m)}$ time, and through linear-size reductions it rules out $2^{o(n)}$ time for many graph problems. See [k-SAT](/k-sat/) for ETH and the strong version SETH.
- **Resolution.** Random 3-CNF formulas with $m = c n$ clauses for a large constant $c$ have no model, and each resolution proof of this has size $2^{\Omega(n)}$ (Chvátal and Szemerédi 1988). So DPLL and CDCL solvers, whose runs on UNSAT formulas are resolution proofs, take exponential time on them.

## Reductions

**SAT reduces to 3-SAT (Karp 1972).** *Construction.* Keep each clause with at most 3 literals. Replace a clause $C = (\ell_1 \vee \cdots \vee \ell_k)$ with $k \ge 4$ by the $k - 2$ clauses

$$(\ell_1 \vee \ell_2 \vee y_1) \wedge (\neg y_1 \vee \ell_3 \vee y_2) \wedge \cdots \wedge (\neg y_{k-4} \vee \ell_{k-2} \vee y_{k-3}) \wedge (\neg y_{k-3} \vee \ell_{k-1} \vee \ell_k),$$

with new variables $y_1, \ldots, y_{k-3}$ for this clause only. Call the result $C'$.

*Claim.* An assignment $x$ makes $C$ true if and only if some values of $y_1, \ldots, y_{k-3}$ make $C'$ true together with $x$.

*Proof.* Suppose $x$ makes $\ell_i$ true. Set $y_j = 1$ for $j \le i - 2$ and $y_j = 0$ for $j \ge i - 1$. The clauses before the one that holds $\ell_i$ are true by their last literal $y_j = 1$, the clause that holds $\ell_i$ is true by $\ell_i$, and the clauses after it are true by their first literal $\neg y_j$ with $y_j = 0$. Conversely, suppose $x$ makes each $\ell_i$ false, and take any values of the $y_j$. Then the first clause forces $y_1 = 1$, and the clause $(\neg y_j \vee \ell_{j+2} \vee y_{j+1})$ forces $y_{j+1} = 1$ from $y_j = 1$. So $y_{k-3} = 1$, and the last clause $(\neg y_{k-3} \vee \ell_{k-1} \vee \ell_k)$ is false. $\square$

The new variables of different clauses are distinct, so by the claim $F$ has a model if and only if the new formula $F'$ has one. $F'$ has fewer than $|F|$ new variables and at most $3|F|$ literal occurrences, and it is built in $O(|F|)$ time. So SAT $\le_p$ 3-SAT, and with the Cook-Levin theorem and the membership in NP, 3-SAT is NP-complete. $\blacksquare$

A small script checked the claim on 400 random formulas with up to 6 variables and clauses of up to 7 literals, by brute force over all assignments of the old and new formulas. The reduction keeps satisfiability but not the count of models: a clause with two true literals allows more than one value of the $y_j$.

**From 3-SAT to other problems.** 3-SAT reduces to [independent set](/independent-set/) and [clique](/clique/) (a triangle for each clause, edges between opposite literals), to [vertex cover](/vertex-cover/), to 3-coloring of [graphs](/graph-coloring/), to subset sum and to hundreds of other problems, see [Karp's 21 problems](/karps-21-np-complete-problems/) and [polynomial-time reductions](/polynomial-time-reduction/).

## Applications

- **Hardness proofs.** To show that a new problem is NP-hard, one usually reduces 3-SAT to it. Its fixed small clauses make gadgets simple.
- **Fine-grained hardness.** Through ETH, 3-SAT gives exponential lower bounds, under the hypothesis, for many problems with exact exponential algorithms.
- **Benchmarks.** Random 3-SAT near the threshold is a standard test set for complete and incomplete solvers.
- **Encodings.** Every circuit becomes a 3-CNF formula of linear size by the [Tseitin transformation](/tseitin-transformation/), with gates of fan-in two.

## References
