---
tag: GE0SFH
kind: concept
slug: counterexample-generation
name: Counterexample generation
aliases:
- Witness and counterexample traces
- error trace generation
- witness generation
area: logic-and-constraints/model-checking
level: core
summary: When a model checker finds that a property fails, it returns an execution that shows the failure, a finite path for a safety property and a lasso for a liveness property.
prereqs: [linear-temporal-logic, kripke-structure]
see_also: [shortest-counterexample, nested-depth-first-search, ltl-model-checking, explicit-state-model-checking, symbolic-model-checking, bounded-model-checking, cegar, vacuity-checking]
sources:
  - paper: "Edmund M. Clarke, Orna Grumberg, Kenneth L. McMillan and Xudong Zhao, Efficient generation of counterexamples and witnesses in symbolic model checking, 32nd Design Automation Conference (DAC 1995), ACM/IEEE, 1995"
    locator: the symbolic construction of witnesses for EG under fairness constraints, and of counterexamples from the onion rings of a fixed-point computation
  - paper: "Edmund M. Clarke, Somesh Jha, Yuan Lu and Helmut Veith, Tree-like counterexamples in model checking, 17th IEEE Symposium on Logic in Computer Science (LICS 2002)"
    locator: the shape of counterexamples for ACTL and the fragments with linear counterexamples
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 3, Section 3.3 (counterexamples for invariants from the DFS stack), Chapter 4, Section 4.4 (lasso counterexamples from nested depth-first search), and Chapter 6, Section 6.6 (counterexamples and witnesses for CTL)
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 6 (symbolic model checking, with the construction of counterexamples and witnesses)
  - paper: doi:10.1007/BF00121128
    title: Costas Courcoubetis, Moshe Y. Vardi, Pierre Wolper and Mihalis Yannakakis, Memory-efficient algorithms for the verification of temporal properties, Formal Methods in System Design 1(2/3), 1992, pages 275 to 288
    locator: the accepting lasso read from the two stacks of the nested search
---

Counterexample generation is the part of a model checker that turns a "no" answer into evidence: an execution of the system that breaks the property. For a [safety property](/safety-property/) the evidence is a finite path from an initial state to a bad state. For an LTL property in general it is a *lasso*, a finite stem followed by a cycle that repeats forever. For a branching-time property it can be a tree of paths. The counterexample is the main output that engineers use, because it can be replayed, simulated and debugged, and it is also the input of refinement loops such as [CEGAR](/cegar/). The dual notion for an existential property, such as "some path reaches $p$", is a *witness*.

## In plain words

A model checker that only says "the property is false" is of little use. You want to see how it fails. So the checker also returns a run of the system: start here, then this step, then this one, and here the rule is broken. You can replay the run in a simulator and watch the bug happen.

For a rule like "this bad thing never happens", the run is a finite list of steps that ends in the bad thing. For a rule like "this good thing keeps happening", no finite run can show a failure, because the good thing might still come later. The checker then returns a run that reaches a loop in which the good thing never happens. Going round the loop forever is the failure.

## The idea

**Shapes.** For a [Kripke structure](/kripke-structure/) $M$ and an LTL formula $\varphi$, the following hold.

- If $M \not\models \varphi$, then some *lasso* path $u\, v^\omega$ violates $\varphi$, where $u$ (the stem) and $v$ (the cycle) are finite paths, the last state of $u$ leads to the first state of $v$, and the last state of $v$ leads back to the first state of $v$. Moreover, $|u| + |v| \le |S| \cdot |Q|$ for a Büchi automaton with state set $Q$ for $\neg\varphi$. The reason is that the [automata-theoretic approach](/automata-theoretic-approach/) reduces $M \not\models \varphi$ to an accepting cycle in the product, and a shortest such cycle visits each product state at most once.
- If $\varphi$ is a safety property, then every violating path has a finite *bad prefix*: every extension of the prefix violates $\varphi$. A finite path is then a complete counterexample. For an invariant $\mathsf{G}\, P$, the bad prefix ends in a state that violates $P$.
- For a liveness property, no finite prefix is bad, so the cycle part is essential.
- For CTL, a counterexample to a universal formula (ACTL) is a witness for its negation, an existential formula, and in general it needs several paths: $\mathsf{AX}\, p \vee \mathsf{AX}\, q$ fails in a state with one successor where $p$ is false and another where $q$ is false, and no single path shows both. Clarke, Jha, Lu and Veith (2002) showed that tree-like counterexamples are always enough for ACTL.

**Where the trace comes from.**

- **Depth-first search.** The search stack is a path from the initial state to the current state. When the check fails, the stack is the counterexample. [Nested depth-first search](/nested-depth-first-search/) gives the lasso from its two stacks: the outer stack is the stem and the inner stack is the cycle.
- **Breadth-first search.** Each state stores a pointer to the state it was reached from, and the counterexample is read backwards from the bad state. It is a shortest one for an invariant; see [shortest counterexample](/shortest-counterexample/).
- **Symbolic search.** A BDD-based reachability computation keeps the *onion rings*: $R_0 = I$ and $R_{i+1}$ the states first reached at step $i+1$. If a bad state is in $R_k$, pick one, then pick a predecessor of it in $R_{k-1}$ with one pre-image computation, and so on back to $R_0$. This costs $k$ pre-images and gives a shortest path. For $\mathsf{EG}$ under fairness, Clarke, Grumberg, McMillan and Zhao (1995) build a witness by walking through the fair states and closing a cycle that meets every fairness set.
- **Bounded model checking.** The satisfying assignment of the SAT formula is the trace; see [bounded model checking](/bounded-model-checking/). For liveness, the formula includes the loop-back.
- **Through abstraction.** An abstract counterexample may not be real. [CEGAR](/cegar/) replays it on the concrete system; if it is spurious, the failure point gives the predicates that refine the abstraction.

**What makes a counterexample useful.** Short traces are easier to read, so tools shorten them by BFS or by a second search. Traces with few context switches between threads are easier to follow. Some tools add an explanation: which inputs matter, which steps are causes, or how the trace differs from a passing one. A counterexample to a property that holds only vacuously, the dual problem, is treated on the [vacuity checking](/vacuity-checking/) page.

## Examples

**A lasso.** In the structure with states 0, 1 and 2, transitions $0 \to 1$, $1 \to 2$, $2 \to 0$ and $2 \to 2$, and $p$ true only in state 1, the formula $\mathsf{G}\mathsf{F}\, p$ fails. The model checker on the [LTL model checking](/ltl-model-checking/) page returns the stem $0\, 1\, 2$ and the cycle $2$: the run $0\, 1\, 2\, 2\, 2 \ldots$ stays in state 2 forever, so $p$ is not true infinitely often. No finite path can show this failure, since any finite path can still be continued by $2 \to 0 \to 1$.

**An invariant with onion rings.** In the Peterson model with the two assignments swapped, from the [explicit-state model checking](/explicit-state-model-checking/) page, breadth-first reachability produces rings with $1, 2, 3, 4, 6, 7, 8, 7$ and $6$ new states for depths 0 to 8, a total of 44 states. Ring 8 holds 2 states in which both processes are in the critical section. Walking back from one of them through one predecessor per ring gives a trace of 8 steps, the shortest possible.

**A tree-like counterexample.** Let $s_0$ have two successors $s_1$ and $s_2$ with self-loops, where $q$ holds only in $s_1$ and $p$ only in $s_2$. Then $s_0 \not\models \mathsf{AX}\, p \vee \mathsf{AX}\, q$. The path through $s_1$ shows that $\mathsf{AX}\, p$ fails, and the path through $s_2$ shows that $\mathsf{AX}\, q$ fails; both are needed.

## Where it is used

- Debugging designs: the trace is replayed in a simulator or a debugger. In hardware verification, a counterexample is a waveform.
- [CEGAR](/cegar/) and [lazy abstraction](/lazy-abstraction/): the abstract counterexample drives the refinement.
- Test generation: a witness for "the system reaches state $s$" is a test case that covers $s$, and tools ask the checker for witnesses of coverage goals on purpose.
- Planning: a witness for "the goal is reachable" is a plan; see [planning as model checking](/planning-as-model-checking/).
- Certification: a witness lets a third party check the claim "the property fails" by replay, without trusting the model checker.

## References
