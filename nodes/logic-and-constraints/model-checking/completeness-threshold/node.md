---
tag: ZCF7GV
kind: concept
slug: completeness-threshold
name: Completeness threshold
aliases:
- Bound for completeness
- CT
area: logic-and-constraints/model-checking
level: research
summary: A bound k such that, if bounded model checking finds no counterexample of length at most k, the property holds; the diameter and the recurrence diameter bound it for safety.
prereqs: [bounded-model-checking, safety-property, kripke-structure]
see_also: [sat-based-bounded-model-checking, k-induction, interpolation-based-model-checking, ic3-pdr, invariant-checking, liveness-property, reachability-problem, breadth-first-search]
sources:
  - paper: doi:10.1007/3-540-36384-X_24
    title: Daniel Kroening and Ofer Strichman, Efficient computation of recurrence diameters, VMCAI 2003, LNCS 2575
    locator: pages 298 to 309 (the recurrence diameter as a completeness threshold for safety properties, and a smaller SAT encoding of the simple-path constraint)
  - paper: doi:10.1007/3-540-49059-0_14
    title: Armin Biere, Alessandro Cimatti, Edmund M. Clarke and Yunshan Zhu, Symbolic model checking without BDDs, TACAS 1999, LNCS 1579
    locator: pages 193 to 207 (the diameter of a system as a bound for the completeness of BMC)
  - paper: "Edmund M. Clarke, Daniel Kroening, Joël Ouaknine and Ofer Strichman, Completeness and complexity of bounded model checking, VMCAI 2004, LNCS 2937"
    title: Completeness and complexity of bounded model checking
    locator: the general definition of the completeness threshold for LTL, and bounds through the product with a Büchi automaton
---

A completeness threshold for a finite system $M$ and a property $\varphi$ is a number $k$ such that the following holds: if $M$ has no counterexample to $\varphi$ of length at most $k$, then $M$ satisfies $\varphi$. [Bounded model checking](/bounded-model-checking/) up to a completeness threshold is therefore a proof, not only a search for bugs. For a safety property $\mathbf{G}\,p$, every reachable state is reached by a path no longer than the *diameter* of $M$, so the diameter is a completeness threshold (Biere, Cimatti, Clarke and Zhu, 1999). The diameter is hard to compute, so one uses the larger *recurrence diameter*, the length of the longest path without repeated states, which a sequence of SAT queries can find; Kroening and Strichman (2003) studied this bound for safety and gave an efficient way to compute it. For liveness properties, thresholds also exist, but they depend on the property, for example through the longest simple path in the states that a counterexample may visit.

## In plain words

Bounded model checking looks for bad runs up to some length $k$. If it finds none, we only know that short runs are fine. A completeness threshold is a length that is "long enough": if no bad run of that length or shorter exists, then no bad run exists at all.

For the question "can the system reach a bad state?", one such length is the number of steps that it takes to reach the hardest-to-reach state. Any bad state that can be reached at all is reached within that many steps. That number is hard to know exactly, so tools use a larger number that is easier to check: the length of the longest walk that never visits a state twice.

## The idea

**Definitions.** Let $M$ be a finite Kripke structure with initial states $I$ and a total transition relation. The length of a path is its number of steps.

- The *diameter* (or *reachability diameter*) $d(M)$ is the least $d$ such that every reachable state is reached by a path from $I$ of length at most $d$.
- A path is *simple* if no state occurs twice. The *recurrence diameter* $rd(M)$ is the length of the longest simple path in $M$; the *initialized* recurrence diameter $rd_I(M)$ is the length of the longest simple path that starts in $I$.
- A number $k$ is a *completeness threshold* for $M$ and $\varphi$ if, whenever $M$ has no counterexample to $\varphi$ of length at most $k$, $M \models \varphi$. For an LTL property, a counterexample of length $k$ is a finite path that already violates the property, or a lasso $s_0, \ldots, s_k$ with a back edge from $s_k$ to some $s_l$.

**Bounds for safety.** For $\varphi = \mathbf{G}\,p$,
$$\mathrm{CT}(M, \mathbf{G}\,p) \;\le\; d(M) \;\le\; rd_I(M) \;\le\; rd(M) \;\le\; |S| - 1.$$
The first inequality holds because a reachable state with $\neg p$ is reached by a path of length at most $d(M)$. The second holds because a shortest path to a state is simple. The others are clear. Any number above a threshold is again a threshold.

**The least threshold tells the answer.** If $M \models \varphi$, the condition in the definition is always met, so $0$ is a threshold. If $M \not\models \varphi$, a threshold must be at least the length of a shortest counterexample. So knowing the least threshold together with one BMC run up to it decides the property. This is why practical thresholds depend on $M$ only, or on $M$ and the shape of $\varphi$, and are upper bounds, not the least value.

**Computing the bounds.** $rd_I(M) \ge k$ if and only if the formula
$$I(s_0) \wedge \bigwedge_{i<k} T(s_i, s_{i+1}) \wedge \bigwedge_{0 \le i < j \le k} s_i \ne s_j$$
is satisfiable. So $rd_I$ is found by increasing $k$ until this formula is unsatisfiable. The direct encoding of the simple-path constraint has $O(k^2)$ comparisons of state vectors, and Kroening and Strichman gave a smaller encoding. The diameter $d(M)$, in contrast, needs a statement of the form "every state reachable in $k + 1$ steps is reachable in at most $k$ steps", which has an alternation of quantifiers; Biere et al. wrote it as a quantified Boolean formula.

**Gap between the bounds.** $rd$ can be much larger than $d$. Take states $0, 1, \ldots, m$ with the initial state 0, edges from 0 to every other state, and a path $1 \to 2 \to \cdots \to m$. Then $d = 1$ but $rd_I = m$.

**Bounds for liveness.** For $\varphi = \mathbf{F}\,p$, a counterexample is an infinite path from $I$ on which $p$ never holds. Cut it before the first repeated state: this gives a simple path through $\neg p$-states with a back edge, a lasso of length at most the longest simple path from $I$ through $\neg p$-states. So that length is a threshold for $\mathbf{F}\,p$. For general LTL properties, Clarke, Kroening, Ouaknine and Strichman (2004) bound the threshold through the product of $M$ with a Büchi automaton for $\neg\varphi$.

## Examples

- **A counter.** An $n$-bit counter that starts at 0 and adds 1 in each step has $d = rd = 2^n - 1$. Here the threshold for "the counter is never $2^n - 1$" cannot be smaller than $2^n - 1$, because that is the length of the only counterexample.
- **The star with a path.** In the system with edges from 0 to every state and a path through all states, BMC up to $d = 1$ proves every safety property, while the recurrence diameter asks for $m$ steps.
- **A shift register.** For the register with $x'_0 = 0$, $x'_1 = x_0$, $x'_2 = x_1$ from $(0, 0, 0)$, only the initial state is reachable, so $d = 0$ and $rd_I = 0$. But $rd = 3$: the path $(1, 1, 1) \to (0, 1, 1) \to (0, 0, 1) \to (0, 0, 0)$ is simple. This is why the initialized version matters.
- **A self-loop.** If $\neg p$ holds only in a state with a self-loop that is reachable in one step, the threshold for $\mathbf{F}\,p$ is reached at the lasso of length 1.

## Where it is used

- **Bounded model checking as proof.** Hardware tools compute $rd_I$ or other bounds and stop BMC there, which works when the bound is small, for example in shallow pipelines.
- **k-induction.** The simple-path constraint of [k-induction](/k-induction/) makes it complete exactly because the step case holds once $k$ exceeds the longest simple path through $P$-states. This is a recurrence diameter of the part of the system where $P$ holds.
- **Software BMC.** Tools such as CBMC add *unwinding assertions* that fail if a loop can run longer than the unwinding bound. If they hold, the bound is complete for that program.
- **Methods that avoid thresholds.** [Interpolation](/interpolation-based-model-checking/) and [IC3](/ic3-pdr/) prove properties without any threshold. Their termination arguments still use quantities of the same kind, such as the backward depth of the bad states, but they do not need to know them in advance.

## References
