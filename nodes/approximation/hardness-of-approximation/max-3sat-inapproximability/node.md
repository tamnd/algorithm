---
tag: VXQ2G0
kind: theorem
slug: max-3sat-inapproximability
name: MAX 3SAT inapproximability
aliases:
- Håstad 7/8 hardness
area: approximation/hardness-of-approximation
level: advanced
summary: The PCP theorem gives a constant ε > 0 such that MAX 3SAT has no (1 - ε)-approximation unless P = NP. Håstad sharpened this to 7/8 + ε for MAX E3SAT, which a random assignment matches.
prereqs: [pcp-theorem, gap-problem, max-sat]
see_also: [hastad-3bit-pcp, random-assignment-max-3-sat, apx-completeness, approximation-resistance, gap-preserving-reduction, vertex-cover-inapproximability, probabilistically-checkable-proof, max-sat-lp-rounding]
sources:
  - paper: doi:10.1145/278298.278306
    title: Sanjeev Arora, Carsten Lund, Rajeev Motwani, Madhu Sudan and Mario Szegedy, Proof verification and the hardness of approximation problems, Journal of the ACM 45(3), 1998
    locator: The PCP theorem and the corollary that MAX 3SAT has no PTAS unless P = NP
  - paper: doi:10.1145/502090.502098
    title: Johan Håstad, Some optimal inapproximability results, Journal of the ACM 48(4), 2001
    locator: The 3-query PCP with soundness close to 1/2 and the theorem that MAX E3SAT has no 7/8 + ε approximation unless P = NP
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 11, Sections 11.2 and 11.3 (the gap view of the PCP theorem and its equivalence with the verifier view), and Chapter 22, Section 22.4 (Håstad's 3-bit PCP and MAX 3SAT)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 16, Section 16.3, Theorem 16.18 (the PCP theorem) and Theorem 16.22 (MAX E3SAT has no 7/8 + ε approximation)
  - paper: doi:10.1016/0022-0000(91)90023-X
    title: Christos H. Papadimitriou and Mihalis Yannakakis, Optimization, approximation, and complexity classes, Journal of Computer and System Sciences 43(3), 1991
    locator: The MAX SNP-completeness of MAX 3SAT
---

MAX 3SAT asks for a truth assignment that satisfies as many clauses as possible of a CNF formula with at most three literals per clause. The [PCP theorem](/pcp-theorem/) implies that there is a constant $\varepsilon_0 > 0$ such that no polynomial-time algorithm can guarantee a fraction $1 - \varepsilon_0$ of the optimum, unless P = NP; this page proves that step in full. Håstad (2001) found the exact constant for MAX E3SAT, where each clause has exactly three literals: no algorithm beats $7/8$, while a random assignment already reaches $7/8$. This theorem is the base of most constant-factor hardness results, through [gap-preserving reductions](/gap-preserving-reduction/) and [APX-completeness](/apx-completeness/).

## Statement

**Notation.** A formula has $M$ clauses, each with at most 3 literals; MAX E3SAT asks for exactly 3 literals on distinct variables. $\mathrm{OPT}$ is the largest number of clauses that one assignment satisfies. MAX 3SAT is a maximization problem, so an $\alpha$-approximation returns an assignment with $\mathrm{ALG} \ge \alpha\,\mathrm{OPT}$, $\alpha \le 1$.

**The PCP theorem (cited).** There are constants $q$ and $s < 1$ such that each language $L$ in NP has a verifier $V$ with these properties. On input $w$ of length $n$, $V$ uses $r = O(\log n)$ random bits, reads $q$ bits of a proof $\pi$ at positions that depend on $w$ and the random bits, and accepts or rejects as a function of those $q$ bits. If $w \in L$, some $\pi$ makes $V$ accept for all random strings (completeness 1). If $w \notin L$, each $\pi$ makes $V$ accept for at most a fraction $s$ of the random strings (soundness $s$). The standard statement uses $s = 1/2$.

**Theorem 1 (a constant gap from the PCP theorem; proved here).** Let $K = 2^q \cdot \max(1, q - 2)$ and $\varepsilon_0 = (1 - s)/K$. There is a polynomial-time map from formulas $\varphi$ to 3CNF formulas $\psi$ such that:

1. if $\varphi$ is satisfiable, then $\psi$ is satisfiable;
2. if $\varphi$ is not satisfiable, then each assignment leaves at least $\varepsilon_0 M$ of the $M$ clauses of $\psi$ unsatisfied.

So gap-MAX 3SAT with "all clauses" versus "at most $(1 - \varepsilon_0)M$ clauses" is NP-hard, and for each $\alpha > 1 - \varepsilon_0$, MAX 3SAT has no polynomial-time $\alpha$-approximation unless P = NP. In particular MAX 3SAT has no PTAS unless P = NP.

**Theorem 2 (Håstad 2001; cited).** For each $\varepsilon > 0$ it is NP-hard to distinguish satisfiable MAX E3SAT instances from those in which no assignment satisfies more than a fraction $7/8 + \varepsilon$ of the clauses. So, for each $\varepsilon > 0$, MAX E3SAT has no polynomial-time $(7/8 + \varepsilon)$-approximation unless P = NP.

## In plain words

A probabilistically checkable proof lets a checker look at only a few bits of a long proof and still catch a false claim at least half of the time. Each small check can be written as a few short clauses over the bits of the proof. If the claim is true, an honest proof passes every check, so all clauses can be satisfied. If the claim is false, any proof fails many checks, and each failed check leaves at least one clause unsatisfied. So a fixed fraction of the clauses must always stay unsatisfied. An algorithm that always came close enough to the best answer would tell these two cases apart, and that would solve every problem in NP quickly. Håstad later built a much stronger checker, which shows that guessing at random is already the best possible for clauses with exactly three literals.

## Proof

This section proves Theorem 1 from the PCP theorem. Theorem 2 is only cited; its proof uses [Håstad's 3-bit PCP](/hastad-3bit-pcp/), the [long code](/long-code/) and Fourier analysis, and it is not given here.

Take $L = $ SAT and its verifier $V$. Fix an input $\varphi$ of length $n$. Let $R = 2^r$, a polynomial in $n$, and list the random strings $\rho_1, \ldots, \rho_R$. Only proof positions that some $\rho_i$ reads matter, so the proof has at most $Rq$ relevant bits; make one Boolean variable $z_p$ for each such position $p$. For each $\rho_i$, the verifier reads positions $p_1, \ldots, p_q$ (list repeated positions once and drop them; this only lowers $q$) and accepts on a set $A_i \subseteq \{0, 1\}^q$ of bit patterns. The map runs $V$ on all $R$ random strings and, for each pattern, computes whether $V$ accepts it. This takes $R \cdot 2^q$ runs of $V$, a polynomial.

**Step 1: each test as a CNF.** For each rejected pattern $a \in \{0, 1\}^q \setminus A_i$, write the clause

$$D_a = \bigvee_{j = 1}^{q} \ell_j, \qquad \ell_j = z_{p_j} \text{ if } a_j = 0, \quad \ell_j = \lnot z_{p_j} \text{ if } a_j = 1.$$

$D_a$ is false exactly when $(z_{p_1}, \ldots, z_{p_q}) = a$. So the conjunction $\Phi_i$ of these at most $2^q$ clauses is true exactly when test $i$ accepts.

**Step 2: clauses of width 3.** A clause $(\ell_1 \lor \cdots \lor \ell_w)$ with $w > 3$ is replaced by the $w - 2$ clauses

$$(\ell_1 \lor \ell_2 \lor y_1),\ (\lnot y_1 \lor \ell_3 \lor y_2),\ \ldots,\ (\lnot y_{w-4} \lor \ell_{w-2} \lor y_{w-3}),\ (\lnot y_{w-3} \lor \ell_{w-1} \lor \ell_w)$$

with $w - 3$ new variables $y_1, \ldots, y_{w-3}$ that occur nowhere else. *Claim:* for a fixed setting of the $\ell$'s, the new clauses can all be satisfied by some setting of the $y$'s exactly when some $\ell_j$ is true; if all $\ell_j$ are false, each setting of the $y$'s leaves at least one new clause unsatisfied. *Proof.* If $\ell_j$ is true, set $y_t = 1$ for $t \le j - 2$ and $y_t = 0$ for $t \ge j - 1$. The clause that contains $\ell_j$ is true. Each clause before it contains a positive $y_t$ with $t \le j - 2$, so it is true; each clause after it contains a negated $y_t$ with $t \ge j - 1$, so it is true. If all $\ell_j$ are false, then the clauses force $y_1 = 1$, then $y_2 = 1$, and so on up to $y_{w-3} = 1$, and the last clause $(\lnot y_{w-3} \lor \ell_{w-1} \lor \ell_w)$ is false. $\blacksquare$ Clauses of width at most 3 stay as they are.

Let $G_i$ be the group of clauses that test $i$ produces. It has at most $2^q \cdot \max(1, q - 2) = K$ clauses. Let $\psi$ be the conjunction of all groups and $M$ its number of clauses, so $M \le KR$. If $\psi$ has no clause at all, every test accepts every pattern, $V$ accepts each proof, and soundness forces $\varphi$ to be satisfiable; in that case output a fixed satisfiable formula.

**Step 3: completeness.** Let $\varphi$ be satisfiable, and let $\pi$ be a proof that $V$ accepts for all $R$ random strings. Set $z_p = \pi_p$. Each $\Phi_i$ is true, so each of its clauses has a true literal, and by the claim the new variables of each split clause can be set to satisfy all of its parts. The new variables of different clauses are disjoint, so these settings do not conflict. All $M$ clauses of $\psi$ are satisfied.

**Step 4: soundness.** Let $\varphi$ be unsatisfiable, and fix any assignment to all variables of $\psi$. Its values on the $z_p$ form a proof $\pi$. By soundness, $V$ rejects $\pi$ for at least $(1 - s)R$ random strings. For each such string $\rho_i$, the bit pattern $a$ read by test $i$ is rejected, so the clause $D_a$ has all literals false. If $D_a$ has width at most 3 it is itself unsatisfied; otherwise, by the claim, one of its parts is unsatisfied. So each rejecting test leaves at least one clause of its own group unsatisfied, and the groups are disjoint. The number of unsatisfied clauses is at least

$$(1 - s)R = \frac{1 - s}{K} \cdot KR \ge \frac{1 - s}{K}\,M = \varepsilon_0 M.$$

**Step 5: the ratio.** Let $\mathcal{A}$ be an $\alpha$-approximation with $\alpha > 1 - \varepsilon_0$. On a satisfiable $\varphi$, $\mathcal{A}(\psi) \ge \alpha M > (1 - \varepsilon_0)M$. On an unsatisfiable $\varphi$, $\mathcal{A}(\psi) \le \mathrm{OPT}(\psi) \le (1 - \varepsilon_0)M$. Comparing $\mathcal{A}(\psi)$ with $(1 - \varepsilon_0)M$ decides SAT in polynomial time, so P = NP. A PTAS would give such an $\alpha$. $\blacksquare$

With the standard values $s = 1/2$ and a verifier with $q$ queries, $\varepsilon_0 = 1/(2K)$. For example, $q = 3$ gives $K = 8$, and $q = 5$ gives $K = 96$. The constant from this proof is small; Theorem 2 gives the best constant.

**The converse.** A gap for MAX 3SAT also gives a PCP, so the two statements are equivalent (Arora and Barak, Section 11.3). Given an NP-hard gap with $M$ clauses, "all satisfiable" versus "at most $(1 - \varepsilon_0)M$", the verifier reads an assignment as its proof, picks a random clause with $O(\log n)$ random bits, reads its at most 3 variables and accepts if the clause is satisfied. Completeness is 1 and soundness is $1 - \varepsilon_0$. Repeating the test $\lceil \ln 2 / \varepsilon_0 \rceil$ times with independent random bits gives soundness at most $(1 - \varepsilon_0)^{\ln 2/\varepsilon_0} \le 1/2$, with a constant number of queries.

**Brute-force check.** The Python code of this page builds $\psi$ from small random verifiers and checks Steps 1 to 4 by enumeration: each $\Phi_i$ is false exactly on the rejected patterns, the split keeps satisfiability, each rejecting test loses exactly one clause of its group under the best setting of the new variables, and $\mathrm{OPT}(\psi) = M - (R - \mathrm{acc})$, where $\mathrm{acc}$ is the largest number of tests that one proof passes.

## Consequences

- **No PTAS.** MAX 3SAT is not in [PTAS](/ptas/) unless P = NP. With its membership in [APX](/apx-class/), this makes it the first [APX-complete](/apx-completeness/) problem, and every APX-hard problem inherits "no PTAS".
- **Vertex cover and independent set.** The strict reduction from MAX 3SAT to [independent set](/maximum-independent-set/) (see [gap-preserving reduction](/gap-preserving-reduction/)) carries the gap, and the complement map gives a constant for [vertex cover](/vertex-cover/); with Theorem 2, independent set has no $(7/8 + \varepsilon)$-approximation and vertex cover no $(17/16 - \varepsilon)$-approximation. See [vertex cover inapproximability](/vertex-cover-inapproximability/).
- **Approximation resistance.** Theorem 2 says that MAX E3SAT is [approximation resistant](/approximation-resistance/): no algorithm beats the ratio of a uniformly random assignment, even on satisfiable instances.
- **Other constraint problems.** Gadgets from MAX E3SAT and from Håstad's linear equations result give constants for MAX 2SAT, MAX CUT and others, through [gadget reductions](/gadget-reduction/).

## Tightness

**MAX E3SAT.** A clause with exactly 3 literals on distinct variables is false under a uniformly random assignment with probability $1/8$. By [linearity of expectation](/linearity-of-expectation/) the expected number of satisfied clauses is $7M/8 \ge 7\,\mathrm{OPT}/8$, and the [method of conditional expectations](/method-of-conditional-expectations/) makes this deterministic. So Theorem 2 is tight: see [random assignment for MAX 3SAT](/random-assignment-max-3-sat/).

**Clauses of width 1 to 3.** For MAX 3SAT with short clauses a random assignment only guarantees $1/2$ on a clause of width 1. Karloff and Zwick (1997) gave a semidefinite programming algorithm with ratio $7/8$ for MAX 3SAT; its analysis for all instances rests on a computer-assisted proof by Zwick. So $7/8$ is the threshold for MAX 3SAT as well (cited). [LP rounding for MAX SAT](/max-sat-lp-rounding/) gives $3/4$ for general MAX SAT.

**Theorem 1.** The constant $\varepsilon_0$ of the proof above is far from tight; its value depends on $q$ and $s$, and the proof only shows that some constant exists.

## History

Papadimitriou and Yannakakis (1991) defined MAX SNP and showed that MAX 3SAT is complete for it under [L-reductions](/l-reduction/), so a PTAS for MAX 3SAT would give one for all of MAX SNP. Arora, Lund, Motwani, Sudan and Szegedy proved the PCP theorem in 1992 (journal version 1998) and concluded that MAX 3SAT has no PTAS unless P = NP; this built on the work of Arora and Safra and on the FGLSS connection between proofs and clique. Bellare, Goldreich, Sudan and others then improved the constant. Håstad proved the $7/8 + \varepsilon$ bound in 1997 (journal version 2001) with a 3-query PCP whose test is a linear equation modulo 2. Dinur (2007) gave a combinatorial proof of the PCP theorem by [gap amplification](/gap-amplification/), which also proves Theorem 1 with a different constant.

## References
