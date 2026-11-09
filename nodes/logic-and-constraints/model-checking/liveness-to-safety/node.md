---
tag: 91PX75
kind: technique
slug: liveness-to-safety
name: Liveness-to-safety reduction
area: logic-and-constraints/model-checking
level: research
summary: Turn the search for an accepting cycle into an invariant check by adding a saved copy of the state and two flags; a bad state is a return to the saved state after an accepting one.
prereqs: [liveness-property, safety-property, automata-theoretic-approach, invariant-checking]
see_also: [safety-property, liveness-property, ic3-pdr, k-induction, bounded-model-checking, nested-depth-first-search, shortest-counterexample, fairness]
sources:
  - paper: "Armin Biere, Cyrille Artho and Viktor Schuppan, Liveness checking as safety checking, 7th International Workshop on Formal Methods for Industrial Critical Systems (FMICS 2002), Electronic Notes in Theoretical Computer Science 66(2), Elsevier, 2002"
    locator: the translation with a copy of the state variables and a loop flag, its correctness, and the result that shortest counterexamples are preserved
  - paper: "Koen Claessen and Niklas Sörensson, A liveness checking algorithm that counts, Formal Methods in Computer-Aided Design (FMCAD 2012), IEEE, 2012"
    locator: k-liveness, which proves that an accepting condition holds only finitely often by safety checks with a counter
  - paper: "Armin Biere, Alessandro Cimatti, Edmund M. Clarke and Yunshan Zhu, Symbolic model checking without BDDs, Tools and Algorithms for the Construction and Analysis of Systems (TACAS 1999), Lecture Notes in Computer Science 1579, Springer, 1999"
    locator: the encoding of lasso-shaped counterexamples of bounded length, which the reduction moves into the model
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 3, Sections 3.3 and 3.4 (invariants and safety properties) and Chapter 4, Section 4.4 (accepting cycles in the product with a Büchi automaton)
---

The liveness-to-safety reduction turns a liveness check into a [safety](/safety-property/) check. A liveness property fails when the system has a reachable cycle that visits an accepting state, a lasso; a safety property fails when the system reaches a bad state. Biere, Artho and Schuppan (2002) showed how to find lassos with a safety checker: add to the system a copy of its state variables, which can save the current state once, and two flags. A bad state is one where the system is back in the saved state and has passed an accepting state since saving it. The new model has twice as many state variables, but every tool for invariants, including [IC3](/ic3-pdr/), [k-induction](/k-induction/) and BDD reachability, can now check liveness.

## In plain words

A safety rule says that something bad never happens; a single bad moment proves it false. A liveness rule says that something good keeps happening; to prove it false, one must show an endless run where the good thing stops, which in a finite system means a loop.

Many strong tools only look for bad moments. The trick lets them see loops. The system gets a notebook with room for one copy of its own state. At some moment it may copy its state into the notebook. From then on, if it ever comes back to exactly the copied state, it has gone round a loop, and it can go round forever. If it also passed a marked state on the way, the loop is a bad endless run. "Back at the copied state, after a marked state" is a single bad moment, which the tools can find.

## When it applies

- The system is finite-state, given by state variables $x$, an initial condition $I(x)$ and a transition relation $T(x, x')$, as in hardware model checking.
- The question is whether there is a reachable cycle through an accepting condition $F(x)$: an LTL property after forming the product with a [Büchi automaton](/buchi-automaton/) for its negation, a [fairness](/fairness/) condition, or a property of the form $\mathsf{F}\mathsf{G}\, \neg F$.
- The available engines are better at invariants than at cycles: SAT-based [IC3](/ic3-pdr/) and [k-induction](/k-induction/), interpolation, or BDD reachability.

The reduction needs equality of states to mean the same future, so it does not apply directly to infinite-state systems, where a lasso of states may not exist.

## The template

The holes are in capitals. A primed variable is the value in the next state.

```pseudo id=main
LIVENESS-TO-SAFETY(x, I, T, F)
L1  add state variables s (a copy of x), saved and seen
L2  I′ ← I(x) ∧ ¬saved ∧ ¬seen
L3  T′ ← T(x, x′) ∧ (   (¬saved ∧ ¬saved′ ∧ ¬seen′ ∧ s′ = s)                ▷ not yet
                      ∨ (¬saved ∧ saved′ ∧ s′ = x ∧ seen′ = F(x))           ▷ save the current state
                      ∨ (saved ∧ saved′ ∧ s′ = s ∧ seen′ = (seen ∨ F(x))) )  ▷ after the save
L4  Bad ← saved ∧ seen ∧ x = s
L5  r ← SAFETY-CHECK(I′, T′, ¬Bad)
L6  if r is a path to Bad then return its x-part as a lasso: the loop starts at the save
L7  return "no reachable cycle through F"
```

The holes:

- **F.** The accepting condition. For an LTL property, build the product of the system with an automaton for the negated property and use its acceptance set. For a generalized condition $F_1, \ldots, F_k$, use flags $\mathit{seen}_1, \ldots, \mathit{seen}_k$ and require all of them in Bad.
- **SAVE.** The variables to copy. All of $x$ is always correct. Variables that cannot differ on a cycle, such as inputs that are not part of the state, need no copy.
- **SAFETY-CHECK.** Any invariant checker: BDD reachability, [bounded model checking](/bounded-model-checking/) for counterexamples, and [k-induction](/k-induction/) or [IC3](/ic3-pdr/) for proofs.

### Example

A 2-bit counter $x$ moves $0 \to 1 \to 2 \to 3 \to 0$, and in state $2$ it may also stay. The property $\mathsf{F}\mathsf{G}(x \ne 2)$ says that the counter eventually leaves $2$ for good. It fails exactly when there is a reachable cycle through $x = 2$, so $F(x)$ is $x = 2$.

The new model has 6 state bits: $x$, $s$, saved and seen. A breadth-first search of it reaches 26 of its 36 possible states (4 before the save and 22 after it), and the first bad state it meets is reached by:

| Step | $x$ | saved | $s$ | seen | move |
|---|---|---|---|---|---|
| 0 | 0 | 0 | | 0 | start |
| 1 | 1 | 0 | | 0 | wait |
| 2 | 2 | 0 | | 0 | wait |
| 3 | 2 | 1 | 2 | 1 | save $x = 2$, which is accepting; take the loop $2 \to 2$ |

At step 3, saved and seen hold and $x = s$, so Bad holds. The lasso is the stem $0, 1, 2$ and the loop $2 \to 2$, of length $2 + 1 = 3$, which is the shortest lasso of the system. The other lasso, round the whole counter, gives a longer path to Bad.

### Why it is correct

Write a path of the new model as states $(x_j, s_j, \mathit{saved}_j, \mathit{seen}_j)$, $j = 0, 1, \ldots$. Its $x$-part is a path of the system from $I$, since every disjunct of $T'$ contains $T(x, x')$.

*From a lasso to a bad state.* Let $x_0 \ldots x_i$ be a path from $I$ and $x_i x_{i+1} \ldots x_{i+m}$ a cycle with $x_{i+m} = x_i$, $m \ge 1$, through a state where $F$ holds. Follow the path with the first disjunct of $T'$ for the first $i$ steps, take the second disjunct on the step from $x_i$, and the third after that. Then $s_j = x_i$ for $j > i$, and by induction $\mathit{seen}_j$ is the disjunction of $F(x_i), \ldots, F(x_{j-1})$. At $j = i + m$ we get $x_j = x_i = s_j$, saved, and seen, because some $x_l$ with $i \le l < i + m$ satisfies $F$. So Bad is reached in $i + m$ steps.

*From a bad state to a lasso.* Let a path of the new model reach Bad at step $t$. Since saved holds at $t$ and is false at step $0$, the second disjunct was used exactly once, on the step from some $i < t$, and the third after it. So $s_t = x_i$, and by the same induction $\mathit{seen}_t$ is the disjunction of $F(x_i), \ldots, F(x_{t-1})$. Bad gives $x_t = x_i$ and some $F(x_l)$ with $i \le l < t$. So $x_0 \ldots x_i$ is a stem and $x_i \ldots x_t$ is a cycle of $t - i \ge 1$ edges through an accepting state.

Both directions keep the length, so the shortest path to Bad has the length of the shortest lasso, and a breadth-first or bounded search of the new model gives a [shortest counterexample](/shortest-counterexample/). The invariant $\neg\mathit{Bad}$ holds iff the system has no reachable cycle through $F$.

### Size and time

The new model has $2n + 2$ state variables for $n$ variables in the system, plus $n$ equality comparisons for $x = s$. Its reachable states are at most $|S| + 2|S|^2$: a state of the system before the save, or a pair of the saved state and the current state, with a value of seen. So the doubling of the variables squares the state space in the worst case. For explicit-state tools this is a poor trade, and they use [nested depth-first search](/nested-depth-first-search/) instead. For symbolic and SAT-based tools, whose cost is not set by the number of states, the reduction often pays off, because their invariant engines are strong. Like every reduction, it leaves the worst case of the [state explosion problem](/state-explosion-problem/) unchanged.

## Classic examples

- **Hardware liveness checking.** Hardware model checkers offer the reduction as a preprocessing step, so that an IC3 engine proves or refutes liveness properties of circuits.
- **Bounded model checking.** The loop condition of bounded model checking for LTL compares the last state with an earlier one; the reduction moves the same comparison into the model, so that one safety engine handles both.
- **Fairness constraints.** Properties under fairness assumptions become generalized acceptance conditions, handled by one seen flag per fairness constraint.

## Variations

- **Save at an accepting state.** Allow the save only when $F(x)$ holds, and drop the seen flag: Bad is saved $\wedge\ x = s$. Every cycle through $F$ can be rotated to start at an accepting state, so the reduction stays correct, but the shortest lasso may get longer, since the loop can no longer start at a state before the accepting one.
- **k-liveness.** Claessen and Sörensson (2012) prove that $F$ holds only finitely often by proving, for increasing $k$, the safety property "$F$ holds at most $k$ times". In a finite system with no reachable cycle through $F$, no path passes through the same accepting state twice, so the property holds for $k$ equal to the number of accepting states; in practice a small $k$ is often enough for IC3.
- **Bounded variants.** Combine the reduction with a bound on the stem or the loop, as a cheaper check that is complete only up to the bound.
- **Infinite-state systems.** Extensions use abstraction to define when two states may be treated as equal, but the plain reduction is complete only for finite-state systems.

## Pitfalls

- **Forgetting the product.** The accepting condition must come from the automaton of the *negated* property, as in the [automata-theoretic approach](/automata-theoretic-approach/), or from the fairness constraints; using the property itself checks the wrong thing.
- **Saving inputs.** If the inputs are part of $x$, the copy compares them too, which can miss lassos that return to the same state with a different input. Copy the state variables only.
- **The variable order.** For BDDs, interleave the bits of $x$ and $s$ in the order; with $x$ above $s$, the BDD of $x = s$ is exponential.
- **Hard invariants.** The invariant $\neg\mathit{Bad}$ is usually not inductive, and its proof by induction or IC3 must find a strengthening that relates the saved state to the current one. This is where the reduction can be slow on correct systems.
- **Fairness on the stem.** Only the loop matters for acceptance. Accepting states on the stem must not set seen, which is why seen starts only at the save.

## Exercises

1. In the example, remove the loop $2 \to 2$. Find the shortest path to Bad and its length, and the lasso it gives.
2. Extend the template to a generalized acceptance condition with sets $F_1$ and $F_2$, and prove the correctness of your extension.
3. Show that the variation that saves only at accepting states can give a longer shortest counterexample, with a system of four states.
4. Explain why the reduction is complete for finite-state systems but not for a counter that increases forever.

## References
