---
tag: VJBGTJ
kind: problem
slug: ctl-satisfiability
name: CTL satisfiability
aliases:
- CTL satisfiability problem
- CTL validity
area: logic-and-constraints/model-checking
level: advanced
summary: Decide whether some Kripke structure satisfies a given CTL formula. It is EXPTIME-complete, and every satisfiable formula has a model of exponential size, found by a tableau.
prereqs: [computation-tree-logic, exptime, alternating-turing-machine]
see_also: [computation-tree-logic, ctl-model-checking, ctl-star, ltl-satisfiability, modal-mu-calculus, exptime, alternating-turing-machine, temporal-logic]
sources:
  - paper: doi:10.1016/0022-0000(85)90001-7
    title: E. Allen Emerson and Joseph Y. Halpern, Decision procedures and expressiveness in the temporal logic of branching time, Journal of Computer and System Sciences 30(1), 1985, pages 1 to 24
    locator: the exponential-time decision procedure for CTL (Hintikka structures and elimination), the small model theorem, and the EXPTIME lower bound
  - paper: doi:10.1016/0022-0000(79)90046-1
    title: Michael J. Fischer and Richard E. Ladner, Propositional dynamic logic of regular programs, Journal of Computer and System Sciences 18(2), 1979, pages 194 to 211
    locator: the EXPTIME lower bound for PDL by the encoding of alternating linear-space machines, and the small model property by filtration
  - paper: doi:10.1145/322234.322243
    title: Ashok K. Chandra, Dexter C. Kozen and Larry J. Stockmeyer, Alternation, Journal of the ACM 28(1), 1981, pages 114 to 133
    locator: the theorem that alternating polynomial space equals deterministic exponential time
  - paper: "E. Allen Emerson, Temporal and modal logic, in Jan van Leeuwen (editor), Handbook of Theoretical Computer Science, Volume B, Elsevier and MIT Press, 1990, pages 995 to 1072"
    locator: the tableau decision procedure for CTL and the table of the complexity of satisfiability for LTL, CTL and CTL*
---

CTL satisfiability asks whether a [CTL](/computation-tree-logic/) formula has a model: some [Kripke structure](/kripke-structure/) with a state where the formula holds. Its complement is validity, so it decides whether a specification is consistent, whether one specification implies another, and, through a model built from the proof, it gives synthesis. The problem is EXPTIME-complete. The upper bound is the tableau method of Emerson and Halpern (1985), which also shows that a satisfiable formula has a model with $2^{O(|\varphi|)}$ states. The lower bound comes from Fischer and Ladner's proof for propositional dynamic logic (1979). This is very different from [CTL model checking](/ctl-model-checking/), where the structure is given and the problem is in linear time.

## In plain words

In model checking you have a system and a requirement, and you ask whether the system meets it. In satisfiability you have only the requirement, and you ask whether any system at all could meet it. If no system can, the requirement contradicts itself, which is a bug in the specification.

The algorithm builds every possible "kind of state" that the formula could describe, then throws away kinds that cannot exist: a kind that needs a next state that is not there, or a kind that promises something will happen but can never deliver it. If a kind that makes the formula true survives, the survivors form a system that meets it.

There are exponentially many kinds, so this takes exponential time, and a matching lower bound shows that no algorithm can do much better in the worst case.

## Definition

**Input.** A CTL formula $\varphi$ over atomic propositions $AP$.

**Question.** Is there a Kripke structure $M = (S, R, L)$ with total $R$ and a state $s \in S$ with $M, s \models \varphi$?

$\varphi$ is **valid** if $\neg\varphi$ is not satisfiable. Since EXPTIME is closed under complement, validity is EXPTIME-complete too. The size $|\varphi|$ is the number of symbols.

## Variants

- **Finite models.** CTL has the finite model property, so satisfiability over all structures and over finite structures are the same problem.
- **Synthesis.** Clarke and Emerson (1981) used the tableau to build a model, and read a synchronization skeleton of a concurrent program from it. This is the first form of temporal synthesis.
- **Other logics.** [LTL satisfiability](/ltl-satisfiability/) is PSPACE-complete (Sistla and Clarke 1985). [CTL*](/ctl-star/) satisfiability is 2EXPTIME-complete. The [modal mu-calculus](/modal-mu-calculus/) and propositional dynamic logic are EXPTIME-complete, like CTL.
- **Fragments.** The fragment with only $\mathsf{EX}$, $\mathsf{AX}$ and $\mathsf{AG}$ is still EXPTIME-hard, by the proof below. Without $\mathsf{AG}$, $\mathsf{AU}$ and $\mathsf{EU}$ (only $\mathsf{EX}$ and $\mathsf{AX}$) the logic is the modal logic K with a total relation, whose satisfiability is PSPACE-complete.

## Examples

**Satisfiable.** $p \wedge \mathsf{AG}(p \to \mathsf{AX}\,\neg p) \wedge \mathsf{AG}(\neg p \to \mathsf{AX}\,p)$: the two-state cycle with $p$ in one state is a model.

**Unsatisfiable.** $\mathsf{AG}\,\mathsf{EF}\,p \wedge \mathsf{EF}\,\mathsf{AG}\,\neg p$. The second part gives a reachable state $t$ with $t \models \mathsf{AG}\,\neg p$, so no $p$-state is reachable from $t$; but the first part gives $t \models \mathsf{EF}\,p$. Also unsatisfiable: $\mathsf{EG}\,p \wedge \mathsf{AF}\,\neg p$, and $\mathsf{E}[p\,\mathsf{U}\,q] \wedge \mathsf{AG}\,\neg q$.

**Models must be large.** Let $b_1, \ldots, b_n$ be propositions that encode a number. The formula "all $b_i$ are false" $\wedge$ $\mathsf{AG}$("each successor encodes the number plus one, modulo $2^n$") $\wedge$ $\mathsf{EF}$("all $b_i$ are true") has size $O(n^2)$, since bit $i$ flips if and only if bits $1, \ldots, i - 1$ are all true. Each of its models visits all $2^n$ numbers on one path, so it has at least $2^n$ states. The exponential small model bound below cannot be improved to a polynomial one.

## Known algorithms

**Tableau with elimination (Emerson and Halpern 1985).** Let $\mathit{cl}(\varphi)$ be the closure of $\varphi$: its subformulas, their negations, and the formulas $\mathsf{EX}\,\mathsf{E}[\alpha\,\mathsf{U}\,\beta]$, $\mathsf{AX}\,\mathsf{A}[\alpha\,\mathsf{U}\,\beta]$, $\mathsf{EX}\,\mathsf{EG}\,\alpha$ and so on that the unfolding laws use. It has $O(|\varphi|)$ elements. An **atom** is a subset of $\mathit{cl}(\varphi)$ that is propositionally consistent and closed under the unfolding laws, for example it contains $\mathsf{E}[\alpha\,\mathsf{U}\,\beta]$ if and only if it contains $\beta$, or $\alpha$ and $\mathsf{EX}\,\mathsf{E}[\alpha\,\mathsf{U}\,\beta]$. There are at most $2^{O(|\varphi|)}$ atoms.

1. Start with the set $D$ of all atoms. Put an edge from atom $a$ to atom $b$ if $b$ contains $\alpha$ for each $\mathsf{AX}\,\alpha \in a$.
2. Repeat until nothing changes:
   - delete an atom that contains $\mathsf{EX}\,\alpha$ but has no successor in $D$ that contains $\alpha$, or that has no successor at all;
   - delete an atom that contains an eventuality $\mathsf{E}[\alpha\,\mathsf{U}\,\beta]$ or $\mathsf{A}[\alpha\,\mathsf{U}\,\beta]$ that is not *fulfilled* in $D$. Fulfilment is a least fixed point on the graph $D$: an atom fulfils $\mathsf{E}[\alpha\,\mathsf{U}\,\beta]$ if it contains $\beta$, or contains $\alpha$ and has a successor that fulfils it; for $\mathsf{A}[\alpha\,\mathsf{U}\,\beta]$, the successors that witness its $\mathsf{EX}$ formulas must all fulfil it.
3. $\varphi$ is satisfiable if and only if some atom in the final $D$ contains $\varphi$.

Each round costs time polynomial in the number of atoms, and each round but the last deletes an atom, so the total time is $2^{O(|\varphi|)}$. Soundness builds a model from the final $D$, with copies of atoms that unwind the eventualities; completeness maps the states of any model to the atoms of the formulas they satisfy, and shows that none of these atoms is ever deleted.

**Automata.** Build an alternating or nondeterministic tree automaton for the tree models of $\varphi$ and test it for emptiness. This is the method that generalizes to CTL* and the mu-calculus.

**Tableau-based provers.** Implementations use one-pass or goal-directed tableaux that avoid building all atoms; they are exponential in the worst case but much faster on typical formulas.

## Bounds

**Theorem.** CTL satisfiability is EXPTIME-complete.

*Upper bound.* The elimination algorithm above runs in time $2^{O(|\varphi|)}$ (Emerson and Halpern 1985). As a by-product, every satisfiable formula has a model with at most $2^{O(|\varphi|)}$ states (the **small model theorem**).

*Lower bound.* By Chandra, Kozen and Stockmeyer (1981), alternating polynomial space equals EXPTIME. So fix an alternating Turing machine $A$ that uses space $p(n)$ and decides an EXPTIME-complete language; we may assume that it has a step counter, so that every computation path halts in an accepting or a rejecting state. For an input $w$ of length $n$, build a formula $\varphi_w$ of polynomial size over the propositions $c_{i,a}$ (cell $i$ holds symbol $a$), $h_{i,q}$ (the head is at cell $i$ and the state is $q$), and $d_\tau$ (the last step used transition $\tau$), for $1 \le i \le p(n)$:

- $\mathit{Init}$: the propositions describe the initial configuration on $w$.
- $\mathsf{AG}\,\mathit{Conf}$: in each reachable state, each cell holds exactly one symbol, and exactly one $h_{i,q}$ holds.
- $\mathsf{AG}\,\mathit{Branch}$: if the state $q$ at the head is existential, $\bigvee_\tau \mathsf{EX}\,d_\tau$ over the transitions $\tau$ that apply; if it is universal, $\bigwedge_\tau \mathsf{EX}\,d_\tau$.
- $\mathsf{AG}\,\mathit{Step}$: for each applicable transition $\tau$, $\mathsf{AX}(d_\tau \to$ the cell under the head and the head position are updated by $\tau)$, and for each cell $i$ not under the head, $c_{i,a} \to \mathsf{AX}\,c_{i,a}$.
- $\mathsf{AG}\,\neg\mathit{reject} \wedge \mathsf{AF}\,\mathit{accept}$.

If $A$ accepts $w$, its accepting computation tree, with a self-loop at each leaf, is a model of $\varphi_w$. Conversely, in a model, each reachable state encodes a configuration, and its successors encode the configurations after the transitions that $\mathit{Branch}$ asks for; choosing one $d_\tau$-successor at each existential state and all of them at each universal state gives a computation tree of $A$ on $w$. $\mathsf{AF}\,\mathit{accept}$ makes each of its branches reach an accepting configuration, and the tree is finitely branching, so by König's lemma it is a finite accepting computation tree. So $\varphi_w$ is satisfiable if and only if $A$ accepts $w$, and the map $w \mapsto \varphi_w$ is computable in polynomial time. $\blacksquare$

The proof uses only $\mathsf{AX}$, $\mathsf{EX}$, $\mathsf{AG}$ and one $\mathsf{AF}$, and with a step counter in the formula the $\mathsf{AF}$ can be avoided. Fischer and Ladner (1979) gave the same encoding for PDL, and Emerson and Halpern (1985) noted that it carries over to CTL.

## Reductions

- **Validity and implication.** $\varphi \to \psi$ is valid if and only if $\varphi \wedge \neg\psi$ is unsatisfiable. So checking that a refined specification implies an abstract one is CTL satisfiability.
- **Not to model checking.** Satisfiability does not reduce to [model checking](/ctl-model-checking/) in polynomial time unless EXPTIME $=$ P, because model checking is in P.
- **To the mu-calculus.** CTL translates in linear size into the alternation-free [modal mu-calculus](/modal-mu-calculus/), whose satisfiability is EXPTIME-complete (Emerson and Jutla 1988), which gives another proof of the upper bound.
- **From alternating machines.** The lower bound above is a direct reduction from the acceptance problem of alternating polynomial-space machines, as in Fischer and Ladner's proof for PDL.

## Applications

Satisfiability checking finds contradictions and vacuous parts in specifications, before any system exists, and it checks that one specification implies another. The model built by the tableau is the basis of the synthesis of synchronization skeletons by Clarke and Emerson (1981). Because of the EXPTIME cost, practical use is limited to short formulas, and modern specification tools more often check LTL satisfiability, which is PSPACE-complete.

## References
