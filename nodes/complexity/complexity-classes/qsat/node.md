---
tag: 5TE80S
kind: problem
slug: qsat
name: "Quantified Boolean formulas (QSAT / QBF)"
area: complexity/complexity-classes
level: core
summary: Decide whether a Boolean formula whose variables are all bound by "for all" and "there exists" quantifiers is true. The canonical PSPACE-complete problem.
prereqs: [pspace, sat, polynomial-time-reduction, alternating-turing-machine]
see_also: [qbf, generalized-geography, savitch-theorem, polynomial-hierarchy, tseitin-transformation, regex-equivalence-pspace-completeness, strips-plan-existence-pspace-complete, ltl-model-checking-pspace-completeness]
sources:
  - paper: doi:10.1145/800125.804029
    title: Larry J. Stockmeyer and Albert R. Meyer, Word problems requiring exponential time, Proceedings of the 5th Annual ACM Symposium on Theory of Computing, 1 to 9 (1973)
    locator: the truth of quantified Boolean formulas is complete for polynomial space
  - paper: doi:10.1016/0304-3975(76)90061-X
    title: Larry J. Stockmeyer, The polynomial-time hierarchy, Theoretical Computer Science 3(1), 1 to 22 (1976)
    locator: quantified formulas with k alternations are complete for the k-th level
  - paper: doi:10.1145/322234.322243
    title: Ashok K. Chandra, Dexter C. Kozen and Larry J. Stockmeyer, Alternation, Journal of the ACM 28(1), 114 to 133 (1981)
    locator: alternating polynomial time equals PSPACE
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage (2013)
    locator: Section 8.3, PSPACE-Completeness (TQBF and formula games)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley (1994)
    locator: Chapter 19, Section 19.1 (QSAT is PSPACE-complete)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 4, Space Complexity (TQBF is PSPACE-complete)
---

QSAT, also called TQBF, asks whether a quantified Boolean formula is true. Every variable of the formula is bound by a quantifier, $\forall$ or $\exists$, so the formula has no free variables and is either true or false. [SAT](/sat/) is the case where all quantifiers are $\exists$. QSAT is PSPACE-complete under polynomial-time and logspace many-one reductions (Stockmeyer and Meyer 1973), so it plays for [PSPACE](/pspace/) the role that SAT plays for NP. This page gives the completeness proof and the view of the problem as a game and as alternating computation. For solvers and the special cases that are easy, see [QBF](/qbf/), which covers the same problem from the side of practice.

## In plain words

Two players fill in the variables of a logic formula, in a fixed order. One player owns the "there exists" variables and wants the formula to come out true. The other owns the "for all" variables and wants it false. Each player sees the earlier choices. The question is whether the first player can always win, whatever the second player does.

Plain satisfiability is the case where the first player owns every variable. With a second player, the question gets much harder. A short answer no longer suffices as proof, because a winning plan must answer every move of the opponent.

The problem can be solved by trying all the moves in turn, with little memory but a lot of time. It is the hardest problem among those that need only a reasonable amount of memory: every such problem can be written as one of these games.

## Definition

**Instance:** a closed quantified Boolean formula in prenex form, $\Phi = Q_1 x_1\, Q_2 x_2 \cdots Q_n x_n\ \varphi(x_1, \ldots, x_n)$, where each $Q_i$ is $\exists$ or $\forall$ and $\varphi$ is a Boolean formula over $x_1, \ldots, x_n$.

**Question:** is $\Phi$ true?

Truth is defined by recursion on the prefix: $\exists x\, \Psi$ is true if $\Psi[x := 0]$ or $\Psi[x := 1]$ is true, and $\forall x\, \Psi$ is true if both are. With no quantifier left, $\varphi$ has no variables and is evaluated. The size of an instance is $N = n + m$, where $m$ is the length of $\varphi$. In the standard form $\varphi$ is in conjunctive normal form; this does not change the complexity (see Variants).

**The game.** Player $\exists$ chooses the values of the existential variables and player $\forall$ the values of the universal ones, in the order $x_1, \ldots, x_n$, each seeing the earlier values. Player $\exists$ wins if $\varphi$ is true at the end. By induction on $n$, $\Phi$ is true if and only if player $\exists$ has a winning strategy. A strategy for $\exists$ maps the earlier values to the next value, so it can be exponentially large; this is why a true instance has no obvious short certificate.

**Alternation.** An [alternating Turing machine](/alternating-turing-machine/) decides QSAT in polynomial time: it guesses $x_i$ in an existential state when $Q_i = \exists$ and in a universal state when $Q_i = \forall$, and it then evaluates $\varphi$ deterministically. So QSAT is in AP, alternating polynomial time. Chandra, Kozen and Stockmeyer (1981) proved $\mathsf{AP} = \mathsf{PSPACE}$, and the hardness proof below is the special case of their simulation of space by alternating time.

## Variants

- **General formulas.** A formula with quantifiers inside it can be put in prenex form in polynomial time: rename the bound variables so that they are distinct, and move the quantifiers to the front. With distinct names, $A \to \exists z\, B$ is equivalent to $\exists z\, (A \to B)$ when $z$ is not free in $A$, and the same holds for the other connectives as long as negations are first pushed to the variables.
- **CNF matrix.** QSAT stays PSPACE-complete when $\varphi$ is in 3-CNF. The [Tseitin transformation](/tseitin-transformation/) adds new variables for the gates of $\varphi$, and they are quantified existentially at the innermost level.
- **Strict alternation.** The prefix can be assumed to be $\exists \forall \exists \forall \cdots$, by adding dummy variables that do not occur in $\varphi$.
- **Bounded alternation.** $\Sigma_k$-QSAT allows $k$ blocks of quantifiers, starting with $\exists$. It is complete for the level $\Sigma_k^p$ of the [polynomial hierarchy](/polynomial-hierarchy/) (Stockmeyer 1976; Wrathall 1976), with $\varphi$ in CNF when $k$ is odd and in DNF when $k$ is even. $\Sigma_1$-QSAT is SAT and $\Pi_1$-QSAT is the tautology problem. $\Pi_k$-QSAT starts with $\forall$ and is complete for $\Pi_k^p$.
- **Easy matrices.** Quantified 2-CNF formulas can be decided in linear time, and quantified Horn formulas in polynomial time. See [QBF](/qbf/).

## Examples

**The order of the quantifiers matters.** Let $\varphi = (x \lor y) \land (\lnot x \lor \lnot y)$, which says $y \ne x$. Then $\forall x\, \exists y\, \varphi$ is true: player $\exists$ answers $y = \lnot x$. But $\exists y\, \forall x\, \varphi$ is false: for $y = 0$, player $\forall$ picks $x = 0$, and for $y = 1$ he picks $x = 1$.

**A strategy.** Let

$$\Phi = \exists x_1\, \forall x_2\, \exists x_3\ (x_1 \lor x_2) \land (\lnot x_2 \lor x_3) \land (\lnot x_1 \lor \lnot x_3 \lor x_2).$$

The choice $x_1 = 0$ loses, because $\forall$ answers $x_2 = 0$ and the first clause fails. The choice $x_1 = 1$ wins with the strategy $x_3 = x_2$: for $x_2 = 0$ the assignment $(1, 0, 0)$ satisfies all three clauses, and for $x_2 = 1$ the assignment $(1, 1, 1)$ does. So $\Phi$ is true. The strategy is a function of $x_2$, not a single value, which is the difference from SAT.

## Known algorithms

- Recursive evaluation on the prefix uses $O(N)$ space and $O(2^n N)$ time on a multitape Turing machine; see [QBF](/qbf/).
- Search procedures with learning (QDPLL, QCDCL) and expansion of universal variables solve large practical instances but take exponential time in the worst case; see [QBF](/qbf/).
- Quantified 2-CNF formulas are decided in linear time by a test on the strongly connected components of the implication graph; see [QBF](/qbf/) and [2-SAT](/2-sat/).

## Bounds

- **PSPACE-complete** under polynomial-time and logspace many-one reductions (Stockmeyer and Meyer 1973). So QSAT is in P if and only if $\mathsf{P} = \mathsf{PSPACE}$, and in NP if and only if $\mathsf{NP} = \mathsf{PSPACE}$. Both are open.
- **Not in polylogarithmic space**, unconditionally. Suppose QSAT were in $\mathsf{DSPACE}(\log^k n)$. Every language in PSPACE reduces to QSAT by a logspace reduction $f$ with $|f(x)| \le |x|^c$. Composing gives a machine with space $O(\log |x|) + O(\log^k (|x|^c)) = O(\log^k |x|)$ for each language in PSPACE. Then $\mathsf{DSPACE}(n) \subseteq \mathsf{DSPACE}(\log^k n)$, which the [space hierarchy theorem](/space-hierarchy-theorem/) rules out. In particular QSAT is not in [NL](/nondeterministic-logspace/), by [Savitch's theorem](/savitch-theorem/).
- No time lower bound better than what follows from the above is known. QSAT might be in P, as far as anyone has proved.

## Reductions

**Membership in PSPACE.** The recursive evaluation stores, for each of the $n$ levels, the current value of $x_i$ and whether the first branch is done, and it evaluates $\varphi$ under a full assignment in $O(m)$ space. After a branch returns, its space is used again. The total space is $O(n + m)$.

**Hardness (Stockmeyer and Meyer 1973).** The reduction is a polynomial-time many-one reduction, and it is also logspace computable.

*Source and target.* Let $A$ be in PSPACE, decided by a deterministic one-tape Turing machine $M$ with space $p(n)$ for a polynomial $p$; one tape suffices, since $k$ tapes fit on $k$ tracks with the same space. As in the proof of [Savitch's theorem](/savitch-theorem/), change $M$ so that it has one accepting configuration. The map sends an input $x$ to a closed formula $\Phi_x$ such that $x \in A$ if and only if $\Phi_x$ is true.

*Configurations as bit vectors.* A configuration of $M$ on $x$ is a row of $p(n)$ cells. Encode each cell by a fixed number of bits that give its symbol, whether the head is on it, and the state if it is. A configuration is then a vector of $s = O(p(n))$ Boolean variables. Write $c = d$ for the conjunction of $c_j \leftrightarrow d_j$ over the $s$ positions, a formula of size $O(s)$. The formula $\mathrm{step}(c, d)$ says that $d$ follows $c$ in one move. Cell $j$ of $d$ is fixed by cells $j - 1$, $j$ and $j + 1$ of $c$ and the transition table, so $\mathrm{step}$ is a conjunction of $p(n)$ local conditions of constant size, and it has size $O(s)$. The vectors $c_0$ and $c_{\mathrm{acc}}$ of the start and accepting configurations are constants that depend on $x$.

*The formulas $R_i$.* Let $R_i(c, d)$ say that $d$ is reachable from $c$ in at most $2^i$ moves. Define

$$R_0(c, d) = (c = d) \lor \mathrm{step}(c, d),$$

$$R_{i+1}(c, d) = \exists m\ \forall u\ \forall v\ \Big[\big((u = c \land v = m) \lor (u = m \land v = d)\big) \rightarrow R_i(u, v)\Big],$$

where $m$, $u$ and $v$ are new vectors of $s$ variables at each level. The universal pair $(u, v)$ lets one copy of $R_i$ check both halves.

*Claim.* For all configurations $c$ and $d$, $R_i(c, d)$ is true if and only if $M$ can go from $c$ to $d$ in at most $2^i$ moves. The proof is by induction on $i$. For $i = 0$ it is the definition of $\mathrm{step}$.

- *Reachable implies true.* Let a computation go from $c$ to $d$ in $\ell \le 2^{i+1}$ moves, and let $m$ be the configuration after $\min(\ell, 2^i)$ moves. Take any $u, v$. If the premise is false, the implication holds. If $(u, v) = (c, m)$ or $(u, v) = (m, d)$, then $v$ is reachable from $u$ in at most $2^i$ moves, so $R_i(u, v)$ is true by induction.
- *True implies reachable.* Let some $m$ make the bracket true for all $u, v$; this is any $m$ that the formula admits, not one built in the other direction. Take $u = c$ and $v = m$: the premise holds, so $R_i(c, m)$ is true. Take $u = m$ and $v = d$: so $R_i(m, d)$ is true. By induction, $m$ is reachable from $c$ and $d$ from $m$, each in at most $2^i$ moves, so $d$ is reachable from $c$ in at most $2^{i+1}$ moves.

*The output.* $M$ has at most $2^{a s}$ configurations for a constant $a$, and a halting deterministic machine does not repeat one, so it accepts within $2^{a s}$ moves if it accepts at all. Let $\Phi_x = R_{a s}(c_0, c_{\mathrm{acc}})$. By the claim, $\Phi_x$ is true if and only if $M$ accepts $x$, which proves both directions.

*Cost.* $R_0$ has size $O(s)$ and each level adds $O(s)$ symbols and $3s$ quantified variables, so $|\Phi_x| = O(s \cdot a s) = O(p(n)^2)$. The formula is built level by level from fixed patterns, and a machine needs only counters for the level and the position to write it, so the map runs in polynomial time and in logarithmic space.

*Prenex form and CNF.* The quantifiers of $R_i$ stand to the right of an implication, in a positive position, and all variables are distinct. So they move to the front, in the order of the levels, and give a prenex formula of the same size. The Tseitin transformation then turns the matrix into 3-CNF with new existential variables at the innermost level.

*Why not two copies.* The direct definition $R_{i+1}(c, d) = \exists m\, [R_i(c, m) \land R_i(m, d)]$ is also correct, but it doubles the size at each level, so $R_{a s}$ would have size $2^{a s} \cdot O(s)$. The universal quantifier is what keeps the formula small. For a nondeterministic $M$ the same construction works, with $\mathrm{step}$ the relation of legal moves; it shows again that NPSPACE reduces to QSAT, so $\mathsf{NPSPACE} = \mathsf{PSPACE}$.

*Worked example.* Let $M$ be a saturating counter with 2 bits: its configurations are the values 0, 1, 2 and 3, and it moves from $k$ to $k + 1$ for $k < 3$ and has no move from 3. Write $c = d$ as $(c_0 \leftrightarrow d_0) \land (c_1 \leftrightarrow d_1)$, with 4 variable occurrences, and $\mathrm{step}(c, d)$ as the disjunction, over $k = 0, 1, 2$, of the 4 literals that fix $c = k$ and $d = k + 1$, with 12 occurrences. So $R_0$ has 16 occurrences. Each level adds the four equalities $u = c$, $v = m$, $u = m$ and $v = d$, of 4 occurrences each, so 16 occurrences, and the 6 quantified variables of $m$, $u$ and $v$. The table gives the number of variable occurrences in $R_i$ and in the version with two copies.

| $i$ | $R_i$ | quantified variables | two copies | $R_i(0, 3)$ |
|---|---|---|---|---|
| 0 | 16 | 0 | 16 | false |
| 1 | 32 | 6 | 32 | false |
| 2 | 48 | 12 | 64 | true |
| 3 | 64 | 18 | 128 | true |

The counter needs 3 moves to go from 0 to 3, so $R_1(0, 3)$ is false and $R_2(0, 3)$ is true. In the direction from the machine to the formula, the path $0 \to 1 \to 2 \to 3$ gives the witness $m = 1$ for $R_2(0, 3)$, and then $m' = 0$ or $m' = 1$ works for the inner $R_1(0, 1)$ and $m' = 2$ for $R_1(1, 3)$. In the other direction, any witness that makes $R_2(0, 3)$ true, such as $m = 2$, gives two halves $R_1(0, 2)$ and $R_1(2, 3)$, and so a run $0 \to 1 \to 2 \to 3$ of the machine. For all 16 pairs $(c, d)$ and $i \le 3$, $R_i(c, d)$ is true exactly when $c \le d \le c + 2^i$.

**From QSAT to games.** QSAT reduces to [generalized geography](/generalized-geography/) by a polynomial-time reduction (Schaefer 1978) that turns the prefix into a chain of diamonds, one for each variable, and the clauses into a final choice of $\forall$. That page gives the reduction. Chains of reductions from QSAT or from generalized geography give the PSPACE-hardness of [regular expression equivalence](/regex-equivalence-pspace-completeness/), [STRIPS planning](/strips-plan-existence-pspace-complete/) and [LTL model checking](/ltl-model-checking-pspace-completeness/).

## Applications

QSAT is the usual starting point of PSPACE-hardness proofs for games, puzzles, planning and verification, because its game form matches the structure of these problems. In the other direction, problems in PSPACE can be encoded as quantified formulas and given to a QBF solver; examples are planning under uncertainty, synthesis and some bounded model checking tasks. See [QBF](/qbf/) for the encodings and the solvers.

## References
