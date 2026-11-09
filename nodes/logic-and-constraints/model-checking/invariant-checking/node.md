---
tag: 7XHSB1
kind: problem
slug: invariant-checking
name: Invariant checking
aliases:
- Safety verification
- Safety checking
- Invariant verification
area: logic-and-constraints/model-checking
level: core
summary: Decide whether a state predicate holds in every reachable state, and give a path to a bad state when it does not. It is reachability of the complement, the simplest safety check.
prereqs: [kripke-structure, reachability-problem]
see_also: [safety-property, reachability-problem, k-induction, ic3-pdr, bounded-model-checking, symbolic-reachability, counterexample-generation, ctl-model-checking]
sources:
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 3, Section 3.3 (invariants as a class of safety properties, and the depth-first search algorithm for invariant checking with an error path)
  - book: "Zohar Manna and Amir Pnueli, Temporal Verification of Reactive Systems: Safety, Springer, 1995"
    locator: the chapters on invariance (the rule for proving an invariant by an inductive strengthening)
  - paper: "Robert W. Floyd, Assigning meanings to programs, Proceedings of Symposia in Applied Mathematics 19, American Mathematical Society, 1967, pages 19 to 32"
    locator: the method of inductive assertions attached to program points
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Chapter 8, Section 8.1 (Savitch's theorem) and Section 8.3 (PSPACE-completeness and the encoding of configurations)
---

Invariant checking asks whether a predicate $p$ on states holds in every state that a system can reach. It is the most common question in verification ("the two processes are never both in the critical section", "the index is always inside the array"), and it is the [reachability problem](/reachability-problem/) for the target $\neg p$. A "no" answer comes with a counterexample: a finite path from an initial state to a state where $p$ is false. A "yes" answer can come with a certificate too: an *inductive invariant* that implies $p$.

## In plain words

You write down a rule that must never break, for example "at most one process is in the critical section". The checker then looks at every state the system can get into. If the rule holds in all of them, the answer is yes. If it breaks somewhere, the checker shows the exact sequence of steps that leads there, so you can replay the bug.

There is a second way to say yes without visiting every state. Find a stronger rule that holds at the start and that no single step can break. Then the stronger rule holds forever, and so does the weaker one. Such a rule is an inductive invariant, and modern checkers search for it.

## Definition

Let $M = (S, I, R, L)$ be a [Kripke structure](/kripke-structure/), or a transition system $(S, I, R)$, and let $p \subseteq S$ be a set of states given by a propositional formula over the labels (a *state predicate*).

**Invariant checking.** Input: $M$ and $p$. Question: is $\mathit{Reach}(M) \subseteq p$? If the answer is yes, $p$ is an **invariant** of $M$. If the answer is no, output a **counterexample**: a path $s_0 s_1 \ldots s_k$ with $s_0 \in I$, $(s_{i-1}, s_i) \in R$, and $s_k \notin p$.

In temporal logic, the question is $M \models \mathsf{AG}\, p$ in [CTL](/computation-tree-logic/), or $M \models \mathsf{G}\, p$ in [LTL](/linear-temporal-logic/). On state predicates the two are the same.

**Inductive invariants.** A set $q \subseteq S$ is **inductive** if it holds initially and is closed under steps:

$$I \subseteq q \qquad \text{and} \qquad \text{for all } (s, t) \in R: \; s \in q \implies t \in q.$$

*Lemma.* $p$ is an invariant of $M$ if and only if there is an inductive $q$ with $q \subseteq p$.

*Proof.* If $q$ is inductive, induction on the length of a path from $I$ shows that each reachable state is in $q$, so $\mathit{Reach}(M) \subseteq q \subseteq p$. Conversely, $\mathit{Reach}(M)$ is inductive: it contains $I$, and a successor of a reachable state is reachable. So if $p$ is an invariant, $q = \mathit{Reach}(M)$ works. $\blacksquare$

So $\mathit{Reach}(M)$ is the least inductive set, and an inductive $q \subseteq p$ is a certificate of the answer yes. Its check needs no search: it is two local conditions, one per initial state and one per transition. A pair $(s, t) \in R$ with $s \in p$ and $t \notin p$ is a **counterexample to induction** (CTI). A CTI shows that $p$ itself is not inductive, but $s$ may be unreachable, so it does not show that $p$ fails.

## Variants

- **Explicit or symbolic input.** The input is a list of states and transitions, a program that generates successors, or Boolean formulas $I(x)$, $R(x, x')$, $p(x)$ over $n$ state variables. The bounds below depend on this, as for [reachability](/reachability-problem/).
- **Inductiveness checking.** Given $p$, decide whether $p$ is inductive. For symbolic input this is the validity of $I(x) \to p(x)$ and $p(x) \wedge R(x, x') \to p(x')$, two calls to a SAT solver.
- **Bounded invariant checking.** Does $p$ hold in every state reachable in at most $k$ steps? This is [bounded model checking](/bounded-model-checking/) of $\mathsf{G}\,p$. It finds bugs but proves nothing for paths longer than $k$, unless $k$ reaches a [completeness threshold](/completeness-threshold/).
- **Regular safety properties.** A [safety property](/safety-property/) that is not about one state at a time, such as "no grant without an earlier request", is checked as an invariant of the product of $M$ with a finite automaton for its bad prefixes. So invariant checking is the general case of safety checking, which explains the aliases.
- **Infinite-state systems.** For programs with integer variables the problem is undecidable in general (it contains the halting problem). Tools then search for an inductive invariant in a restricted class, such as linear inequalities.

## Examples

**Mutual exclusion.** In the two-process structure of the [Kripke structure](/kripke-structure/) page, let $p = \neg(c_1 \wedge c_2)$. A breadth-first search from $(n, n, 1)$ visits the 8 reachable states, and $p$ holds in each. So $p$ is an invariant.

But $p$ is not inductive. Of the 18 states $(\ell_1, \ell_2, y)$, 16 satisfy $p$, and there are 2 counterexamples to induction: $(w, c, 1) \to (c, c, 0)$ and $(c, w, 1) \to (c, c, 0)$. In both, the semaphore is 1 while a process is critical, which never happens in a run. Add this fact:

$$q = \neg(c_1 \wedge c_2) \wedge \big( (c_1 \vee c_2) \leftrightarrow y = 0 \big).$$

Then $q$ holds in $(n, n, 1)$, and no transition leaves $q$: entering the critical section sets $y = 0$, and leaving it sets $y = 1$. So $q$ is an inductive strengthening of $p$, and it proves the invariant with no search. Here $q$ has exactly 8 states, the reachable ones; in general an inductive invariant can be larger than $\mathit{Reach}(M)$.

**A counterexample.** Drop the guard $y = 1$ from the step $w_i \to c_i$. Then breadth-first search finds $(n,n,1) \to (w,n,1) \to (w,w,1) \to (c,w,0) \to (c,c,0)$, and the last state violates $p$. The parent links of the search give this path, and it is a shortest one.

## Known algorithms

- **Explicit search with an error path.** Run [breadth-first search](/breadth-first-search/) or [depth-first search](/depth-first-search/) from $I$, test $p$ in each new state, and stop at the first state outside $p$. Breadth-first search gives a shortest counterexample from its parent links; depth-first search has the path on its stack (Baier and Katoen, Section 3.3). The [CTL labelling algorithm](/ctl-labelling-algorithm/) computes $\mathsf{AG}\,p$ as the complement of the backward search $\mathsf{E}[\mathit{true}\,\mathsf{U}\,\neg p]$, which gives the set of all states that satisfy the invariant, not only the answer for $I$.
- **Reductions of the search.** [Partial-order reduction](/partial-order-reduction/), [symmetry reduction](/symmetry-reduction/) and [bitstate hashing](/bitstate-hashing/) cut the number of stored states. Partial-order reduction for invariants needs a condition that keeps at least one path to each bad state.
- **Symbolic fixed points.** [Symbolic reachability](/symbolic-reachability/) computes $\mathit{Reach}$ as $\mu Z.\, I \cup \mathit{post}(Z)$ on [binary decision diagrams](/binary-decision-diagram/) and tests $\mathit{Reach} \subseteq p$; a backward variant computes $\nu Z.\, p \cap \mathit{pre}_\forall(Z)$ and tests $I \subseteq Z$.
- **Induction-based methods.** [k-induction](/k-induction/) strengthens the induction step to paths of length $k$. [Interpolation-based model checking](/interpolation-based-model-checking/) and [IC3/PDR](/ic3-pdr/) build an inductive strengthening of $p$ from CTIs, one clause at a time, with a SAT solver. When they succeed, the strengthening is a certificate that a separate checker can verify in two SAT calls.
- **Abstraction.** [CEGAR](/cegar/) checks the invariant on an abstract system, and refines the abstraction when the abstract counterexample is not a real one.

## Bounds

**Explicit input.** The search costs $O(|S| + |R|)$ time plus $|S|$ evaluations of $p$, and $O(|S|)$ space. It is optimal up to a constant factor, for the same reason as for [reachability](/reachability-problem/). The problem is complete for NL (the complement of a reachability question, and NL is closed under complement).

**Symbolic input.** Invariant checking is PSPACE-complete. It is the complement of succinct reachability with target $\neg p$, which is PSPACE-complete (see the [reachability problem](/reachability-problem/)), and PSPACE is closed under complement.

**Inductiveness.** For symbolic input, deciding whether a given $p$ is inductive is coNP-complete: it is in coNP because a counterexample is one state or one transition, and it is coNP-hard because "$\mathit{true}$ implies $p$" is already the validity of $p$ when $I$ is all states. So a certificate of an invariant is checked much more cheaply than the invariant is found. The smallest inductive strengthening can still need an exponentially large formula, and the search for one is where the PSPACE cost goes.

## Reductions

- **To and from reachability.** $p$ is an invariant if and only if $\neg p$ is unreachable. The reduction works in both directions in linear time, and the counterexample is the reachability witness.
- **From safety properties.** A regular safety property $P$ holds in $M$ if and only if the product $M \otimes A$ with a deterministic automaton $A$ for the bad prefixes of $P$ never reaches an accepting state of $A$. That is an invariant of $M \otimes A$ (Baier and Katoen, Chapter 4).
- **From liveness.** The [liveness-to-safety](/liveness-to-safety/) transformation turns the check of a liveness property into an invariant check on a system with twice as many state variables.
- **From deadlock freedom.** [Deadlock freedom](/deadlock-freedom-checking/) is the invariant "some transition is enabled".
- **Inside CTL.** $\mathsf{AG}\,p$ is a CTL formula, so [CTL model checking](/ctl-model-checking/) contains invariant checking, and the labelling algorithm decides it in linear time.

## Applications

Hardware verification is mostly invariant checking: the properties of a circuit are assertions that must hold in each cycle, and the industrial engines are [IC3/PDR](/ic3-pdr/), [interpolation](/interpolation-based-model-checking/) and [bounded model checking](/bounded-model-checking/). In software, assertions, array bounds and the absence of null dereferences are invariants at program points. Explicit-state checkers such as SPIN and TLC check invariants of protocol models, and the counterexample path is the main thing an engineer reads.

## References
