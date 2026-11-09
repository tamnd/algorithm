---
tag: J5EAMW
kind: problem
slug: ctl-model-checking
name: CTL model checking
aliases:
- Branching-time model checking
- CTL verification
area: logic-and-constraints/model-checking
level: core
summary: Decide whether the initial states of a Kripke structure satisfy a CTL formula. It takes O(|M||phi|) time, it is P-complete, and it is PSPACE-complete when the structure is given succinctly.
prereqs: [computation-tree-logic, kripke-structure, reachability-problem]
see_also: [ctl-labelling-algorithm, ctl-model-checking-linear-time, computation-tree-logic, symbolic-model-checking, ltl-model-checking, mu-calculus-model-checking, fairness, ctl-satisfiability]
sources:
  - paper: doi:10.1145/5397.5399
    title: Edmund M. Clarke, E. Allen Emerson and A. Prasad Sistla, Automatic verification of finite-state concurrent systems using temporal logic specifications, ACM Transactions on Programming Languages and Systems 8(2), 1986, pages 244 to 263
    locator: the model checking algorithm for CTL, linear in the size of the structure and of the formula, with fairness
  - paper: doi:10.1007/3-540-11494-7_22
    title: Jean-Pierre Queille and Joseph Sifakis, Specification and verification of concurrent systems in CESAR, International Symposium on Programming 1982, Lecture Notes in Computer Science 137, pages 337 to 351
    locator: model checking of a branching-time logic by fixed-point computation on the state graph
  - paper: "Philippe Schnoebelen, The complexity of temporal logic model checking, Advances in Modal Logic 4, King's College Publications, 2003, pages 393 to 436"
    locator: the survey of the complexity of model checking for CTL, LTL, CTL* and their fragments, including the P-completeness of CTL model checking
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 6, Section 6.4 (CTL model checking, the algorithm and its time complexity), Section 6.5 (fairness) and Section 6.6 (counterexamples and witnesses)
  - paper: "Orna Kupferman, Moshe Y. Vardi and Pierre Wolper, An automata-theoretic approach to branching-time model checking, Journal of the ACM 47(2), 2000, pages 312 to 360"
    locator: the program complexity of branching-time model checking, PSPACE-complete for concurrent programs given as a product of processes
---

CTL model checking is the problem of deciding whether a [Kripke structure](/kripke-structure/) satisfies a formula of [computation tree logic](/computation-tree-logic/). It was the first temporal model checking problem to be solved efficiently: Clarke and Emerson (1981) and Queille and Sifakis (1982) gave fixed-point algorithms, and Clarke, Emerson and Sistla (1986) showed that it can be decided in time $O(|M|\,|\varphi|)$. The problem is P-complete for explicit structures. For structures given as programs or circuits it is PSPACE-complete, and that is where the practical difficulty, the [state explosion problem](/state-explosion-problem/), lives. This page is about the problem and its complexity; the [CTL labelling algorithm](/ctl-labelling-algorithm/) is the algorithm, and the [linear-time theorem](/ctl-model-checking-linear-time/) is its proof of cost.

## In plain words

You have a model of a system as a graph of states, and a requirement written in CTL, such as "from every state the system can get back to its start" or "every request is eventually granted on every path". The model checker answers yes or no, and on a no it shows a path or a state where the requirement fails.

The surprise is the cost. If the graph is already written out, the check takes time proportional to the size of the graph times the size of the formula, so it scales well to graphs with millions of states. The hard part is that real systems have far more states than that, because each added variable or process multiplies the count.

## Definition

**Input.** A finite Kripke structure $M = (S, I, R, L)$ with total $R$, and a CTL formula $\varphi$.

**Question.** Is $M \models \varphi$, that is, does each initial state satisfy $\varphi$?

**Global form.** Compute $[\![\varphi]\!] = \{s \in S : s \models \varphi\}$. The standard algorithms solve this form, and the decision follows by testing $I \subseteq [\![\varphi]\!]$.

**Size.** $|M| = |S| + |R|$ and $|\varphi|$ is the number of symbols of $\varphi$. For succinct inputs (below), the input size is the size of the description, not $|M|$.

## Variants

- **Local model checking.** Decide $s \models \varphi$ for one state, exploring only the part of $M$ that the answer needs. [Local model checking](/local-model-checking/) and [on-the-fly model checking](/on-the-fly-model-checking/) do this with depth-first search over (state, subformula) pairs.
- **Succinct (symbolic) structures.** The structure is given by Boolean formulas, circuits or a product of processes over $n$ state variables, so it can have $2^n$ states. [Symbolic model checking](/symbolic-model-checking/) solves this form with [BDDs](/binary-decision-diagram/).
- **Fair CTL.** Path quantifiers range over the paths that meet [fairness](/fairness/) constraints. The cost grows by a factor that depends on the number of constraints only.
- **Witnesses and counterexamples.** For $\mathsf{EF}$, $\mathsf{EU}$ and $\mathsf{EG}$ a witness is a finite path or a lasso, found from the same search. For nested formulas such as $\mathsf{AG}\,\mathsf{EF}\,p$ a counterexample can need a tree, not a single path; [counterexample generation](/counterexample-generation/) discusses which fragments have linear counterexamples.
- **Fixed formula (data complexity).** For one fixed formula, only $M$ is the input.

## Examples

**Mutual exclusion.** On the two-process structure of the [Kripke structure](/kripke-structure/) page (8 reachable states, 14 transitions):

| formula | meaning | result |
|---|---|---|
| $\mathsf{AG}\,\neg(c_1 \wedge c_2)$ | never both critical | holds |
| $\mathsf{AG}(w_1 \to \mathsf{AF}\,c_1)$ | a waiting process 1 must enter | fails |
| $\mathsf{AG}(w_1 \to \mathsf{EF}\,c_1)$ | a waiting process 1 can enter | holds |
| $\mathsf{AG}\,\mathsf{EF}(n_1 \wedge n_2)$ | the start stays reachable | holds |

The failure of the second formula has the witness $(n,n,1) \to (w,n,1)$, followed by the cycle $(w,n,1)\,(w,w,1)\,(w,c,0)$ repeated forever: a path from a $w_1$-state that satisfies $\mathsf{EG}\,\neg c_1$. Under strong [fairness](/fairness/) for process 1 the second formula holds.

**A worked labelling.** The [CTL labelling algorithm](/ctl-labelling-algorithm/) page computes $\mathsf{EG}\,p$, $\mathsf{E}[p\,\mathsf{U}\,q]$ and $\mathsf{A}[p\,\mathsf{U}\,q]$ on a structure with 6 states, step by step.

## Known algorithms

- **The labelling algorithm** of Clarke, Emerson and Sistla (1986). Process the subformulas from the inside out; compute $\mathsf{EX}$ by one pass over the edges, $\mathsf{EU}$ by backward [breadth-first search](/breadth-first-search/), and $\mathsf{EG}$ by the [strongly connected components](/strongly-connected-components/) of the subgraph where the argument holds. Time $O(|M|\,|\varphi|)$. See the [CTL labelling algorithm](/ctl-labelling-algorithm/) and the [linear-time theorem](/ctl-model-checking-linear-time/).
- **Fixed-point iteration.** Compute $\mathsf{EU}$ as $\mu Z.\, \psi \vee (\varphi \wedge \mathsf{EX}\,Z)$ and $\mathsf{EG}$ as $\nu Z.\, \varphi \wedge \mathsf{EX}\,Z$ by [Kleene iteration](/fixed-point/) (Queille and Sifakis 1982). On sets of states this costs $O(|S| \cdot |M|)$ per operator, but on BDDs it is the standard [symbolic model checking](/symbolic-model-checking/) algorithm, because each iteration is a few BDD operations.
- **Translation to the mu-calculus** or to games. CTL is the alternation-free part of the [modal mu-calculus](/modal-mu-calculus/), so every [mu-calculus model checking](/mu-calculus-model-checking/) algorithm applies, and alternation-free formulas take linear time.
- **SAT-based methods.** [Bounded model checking](/bounded-model-checking/) and [IC3/PDR](/ic3-pdr/) handle the invariants $\mathsf{AG}\,p$, and extensions handle other operators.

## Bounds

**Explicit structures: $O(|M|\,|\varphi|)$ time.** This is the [linear-time theorem](/ctl-model-checking-linear-time/) of Clarke, Emerson and Sistla. With $k$ fairness constraints the bound becomes $O(|M|\,|\varphi|\,k)$ for justice, and stays polynomial with compassion.

**P-complete.** *In P* by the bound above. *P-hard*, under logarithmic-space reductions, from the monotone circuit value problem in its synchronous alternating form, which is P-complete (Greenlaw, Hoover and Ruzzo): the gates are arranged in layers $0, \ldots, d$, layer $0$ holds the inputs, each gate of layer $i + 1$ reads gates of layer $i$, and the layers alternate between $\wedge$ and $\vee$. Make a state for each gate with an edge to each of its inputs, give each input a self-loop, and label the inputs that are $1$ with $\mathit{one}$. Let $\varphi_0 = \mathit{one}$, and $\varphi_{i+1} = \mathsf{AX}\,\varphi_i$ if layer $i + 1$ is a layer of $\wedge$ gates, $\mathsf{EX}\,\varphi_i$ otherwise. By induction on $i$, a gate of layer $i$ satisfies $\varphi_i$ if and only if its value is $1$, and $|\varphi_d| = O(d)$. So the circuit outputs $1$ if and only if the output state satisfies $\varphi_d$ (Schnoebelen 2003 gives this and finer results).

**Fixed formula: NL.** For a fixed formula the problem is in NL, since $\mathsf{EX}$, $\mathsf{EU}$ and $\mathsf{EG}$ are reachability questions and NL is closed under complement (Immerman and Szelepcsényi). Already $\mathsf{EF}\,p$ is NL-hard, because it is directed [reachability](/reachability-problem/). So the P-hardness needs formulas of growing nesting depth.

**Succinct structures: PSPACE-complete.** *In PSPACE.* Decide $s \models \varphi$ by recursion on $\varphi$: an $\mathsf{EX}$ guesses a successor, an $\mathsf{EU}$ guesses a path of length less than $2^n$ and checks the subformulas on it by recursive calls, and an $\mathsf{EG}$ guesses a lasso. Each level of the recursion needs polynomial space, the depth is at most $|\varphi|$, and negation is free because NPSPACE $=$ PSPACE is closed under complement. *PSPACE-hard.* Already $\mathsf{EF}\,p$ is succinct [reachability](/reachability-problem/), which is PSPACE-complete. For concurrent programs given as a product of processes the same holds (Kupferman, Vardi and Wolper 2000). This is the same class as [LTL model checking](/ltl-model-checking/) for explicit structures, but for a different reason: there the formula is the exponential part, here the structure is.

## Reductions

- **From reachability and invariants.** [Reachability](/reachability-problem/) is $\mathsf{EF}$, [invariant checking](/invariant-checking/) is $\mathsf{AG}$, and [deadlock freedom](/deadlock-freedom-checking/) is $\mathsf{AG}\,\mathsf{EX}\,\mathit{true}$ before totalization.
- **To the mu-calculus.** The fixed-point equations translate a CTL formula into a mu-calculus formula of alternation depth 1 and linear size, so CTL model checking is a special case of [mu-calculus model checking](/mu-calculus-model-checking/).
- **To games.** $s \models \varphi$ is the winner of a reachability or [parity game](/parity-game/) on the product of $M$ and the subformulas of $\varphi$, which the local algorithms solve by depth-first search.
- **CTL*.** [CTL*](/ctl-star/) model checking reduces to LTL model checking on the innermost path formulas, and costs PSPACE even for explicit structures; CTL is the fragment where each path formula is a single operator, and that is why it is easy.

## Applications

CTL was the logic of the first model checkers, EMC and SMV, and it is still used in NuSMV, nuXmv and other tools for hardware, protocols and planning. $\mathsf{AG}$ formulas are safety properties, $\mathsf{AF}$ and $\mathsf{AG}\,\mathsf{AF}$ formulas are liveness properties checked under fairness, and $\mathsf{AG}\,\mathsf{EF}$ formulas ("reset is always possible") are the branching properties that LTL cannot state. [Planning as model checking](/planning-as-model-checking/) uses $\mathsf{EF}$ and $\mathsf{AF}$ to find plans under nondeterminism.

## References
