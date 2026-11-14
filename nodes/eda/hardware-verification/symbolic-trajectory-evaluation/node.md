---
tag: NEAHJQ
kind: algorithm
slug: symbolic-trajectory-evaluation
name: Symbolic trajectory evaluation
aliases:
- STE
- Seger-Bryant trajectory evaluation
area: eda/hardware-verification
level: advanced
summary: Seger and Bryant's model checking of bounded properties over a lattice of ternary states by symbolic simulation, used on large memories and datapaths.
model: word-ram
complexity:
  vars: {d: the largest time in the assertion, P: the number of gate inputs of the circuit, B: "the number of nodes of the largest rail BDD of the run (at most 2^(v + 1), v the number of symbolic variables of the assertion)"}
  time: {worst: "O(d P B^2)"}
  space: {extra: "O(d P B^2)"}
properties: {deterministic: true, exact: false, complete: false, recursive: false}
history:
  year: 1995
  people: [Carl-Johan H. Seger, Randal E. Bryant]
  note: Bryant showed in 1991 that ternary simulation with X is a sound way to verify circuits. Seger and Bryant defined trajectory formulas over a lattice of states and the symbolic check in 1995. The Voss and Forte systems of Seger made the method a tool for large designs.
prereqs: [ternary-simulation, symbolic-simulation, reduced-ordered-bdd]
see_also: [generalized-symbolic-trajectory-evaluation, ternary-simulation, symbolic-simulation, bounded-model-checking, abstract-interpretation, galois-connection, symbolic-model-checking, cegar]
sources:
  - paper: doi:10.1007/BF01383966
    title: C.-J. H. Seger and R. E. Bryant, Formal verification by symbolic evaluation of partially-ordered trajectories, Formal Methods in System Design 6(2), 147 to 189, 1995
    locator: the lattice of ternary states, the monotone excitation function, trajectory formulas, the defining sequence and the defining trajectory, and the theorem that an assertion holds exactly when the defining sequence of the consequent lies below the defining trajectory of the antecedent
  - paper: doi:10.1145/103516.103519
    title: R. E. Bryant, A methodology for hardware verification based on logic simulation, Journal of the ACM 38(2), 299 to 328, 1991
    locator: ternary simulation with X as a sound abstraction of binary behavior, and the monotonicity of the ternary circuit model
  - paper: doi:10.1109/43.372367
    title: S. Hazelhurst and C.-J. H. Seger, A simple theorem prover based on symbolic trajectory evaluation and BDDs, IEEE Transactions on Computer-Aided Design 14(4), 413 to 422, 1995
    locator: inference rules that join STE results, such as conjunction and sequential composition of assertions
  - paper: doi:10.1109/TC.1986.1676819
    title: R. E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 677 to 691, 1986
    locator: the reduced ordered BDD and the cost O(|f| |g|) of Apply
---

Symbolic trajectory evaluation (STE) checks an assertion $A \Rightarrow C$ on a gate-level circuit. Here $A$ and $C$ are trajectory formulas, which say which nodes hold which values at which of the first few clock cycles, under guards over symbolic variables. The method runs [ternary simulation](/ternary-simulation/) with BDD values, so each node holds 0, 1 or X under each assignment of the variables. Nodes that $A$ does not mention stay X and cost nothing. One run of this simulation builds the *defining trajectory* of $A$, the least information that every run satisfying $A$ must contain. Then a single comparison in the information order tests whether that trajectory already contains what $C$ asks for. If the comparison holds for all assignments, every binary run of the circuit that satisfies $A$ satisfies $C$. The method checks bounded properties: the depth of the check is the largest time in the formulas. Assertion graphs for unbounded time are the subject of [generalized STE](/generalized-symbolic-trajectory-evaluation/).

## In plain words

You want to prove: "if the inputs $a$ and $b$ hold $x$ and $y$ now, and $c$ holds $z$ in the next cycle, then two cycles from now the register $r_2$ holds $(x \wedge y) \oplus z$". Here $x$, $y$ and $z$ are names for any bits.

STE simulates the circuit once. It puts $x$, $y$ and $z$ where the assertion says, and X (unknown) on every other input and register. A node gets a formula only when its inputs force one, so a node that does not matter stays X. At the end, STE asks if $r_2$ holds the wanted formula at cycle 2. If yes, the property holds for all values of $x$, $y$, $z$ and of the X nodes. If no, the failing cases form a formula. X only hides information, so it can make a true property fail but never makes a false property pass.

## The problem

**The lattice.** A node value is one of X, 0, 1 and $\top$, ordered by information: X $\sqsubseteq$ 0, X $\sqsubseteq$ 1, 0 $\sqsubseteq \top$ and 1 $\sqsubseteq \top$, with 0 and 1 not comparable. X means "no information", and $\top$ means "conflicting information", which no real run has. The join $a \sqcup b$ is the least upper bound, so $0 \sqcup 1 = \top$. A binary value $b$ is above $a$ exactly when $a$ is X or $a = b$. This page puts X at the bottom. The [ternary simulation](/ternary-simulation/) page uses the order of definedness with 0 and 1 below X, so the two orders are opposite. The meaning is the same.

**The circuit.** A synchronous circuit has primary inputs, latches with a next-state node $\mathrm{next}(s)$, and gates in topological order. In the binary model a *run* gives every node $u$ a value $\rho_t(u) \in \{0, 1\}$ at each time $t \ge 0$. The inputs and the initial latch values are free. Each gate has the value of its function on its fanins at the same time, and $\rho_{t+1}(s) = \rho_t(\mathrm{next}(s))$. Seger and Bryant allow any monotone next-state function on the lattice of states. This page uses the zero-delay gate model, which is one instance.

**Ternary gates.** Each gate operator $\mathrm{op}$ is extended to $\widehat{\mathrm{op}}$ on the lattice. On X, 0 and 1 the result is binary when all ways of replacing the X arguments by 0 or 1 give the same binary result, and X otherwise. So $\widehat{\mathrm{AND}}(0, \mathrm{X}) = 0$ and $\widehat{\mathrm{AND}}(1, \mathrm{X}) = \mathrm{X}$. The extension agrees with $\mathrm{op}$ on binary arguments and is monotone: $a_i \sqsubseteq b_i$ for all $i$ gives $\widehat{\mathrm{op}}(a) \sqsubseteq \widehat{\mathrm{op}}(b)$.

**Trajectory formulas.** Let $V$ be a set of symbolic variables and $\phi$ an assignment of them. The formulas here are conjunctions of constraints $(t, u, e, g)$, read "if $g$ then node $u$ is $e$ at time $t$", where $e$ and $g$ are Boolean expressions over $V$. In Seger and Bryant's syntax this is $\mathbf{N}^t (g \rightarrow (u \text{ is } e))$, built from the atoms "$u$ is 0" and "$u$ is 1", conjunction, a Boolean guard $\rightarrow$ and the next-time operator $\mathbf{N}$. A run $\rho$ *satisfies* a formula $F$ at $\phi$ when every constraint with $g(\phi) = 1$ has $\rho_t(u) = e(\phi)$. The assertion $A \Rightarrow C$ *holds* when, for every $\phi$, every run that satisfies $A$ at $\phi$ satisfies $C$ at $\phi$.

**Defining sequence and trajectory.** The *defining sequence* $\delta_F$ of a formula gives each node at each time the least lattice value that the formula asks for: the join, over the constraints on $(t, u)$ whose guard holds, of the value of $e$. A run satisfies $F$ at $\phi$ exactly when $\delta_F(\phi) \sqsubseteq \rho$ at every node and time. The *defining trajectory* $\tau_A$ is the least sequence above $\delta_A$ that is closed under the circuit: each gate holds at least $\widehat{\mathrm{op}}$ of its fanins, and each latch at time $t + 1$ holds at least the value of its next-state node at time $t$. The task is to compute, as a BDD, the set of assignments $\phi$ where $\delta_C(\phi) \sqsubseteq \tau_A(\phi)$ fails.

## The algorithm

Each lattice value under all assignments is a pair of BDDs (one, zero): at $\phi$ the value is X when neither holds, 1 when only *one* holds, 0 when only *zero* holds, and $\top$ when both hold. The join is the OR of the rails, and $a \sqsubseteq b$ is $(a_1 \rightarrow b_1) \wedge (a_0 \rightarrow b_0)$. A constraint $(t, u, e, g)$ adds $(g \wedge e,\ g \wedge \neg e)$ to $\delta(t, u)$.

```pseudo id=main
STE(C, A, Cons)
L1  d ← the largest time in A and Cons
L2  for t ← 0 to d do
L3      for each node u do τ_t(u) ← δ_A,t(u)
L4      if t > 0 then for each latch s do τ_t(s) ← τ_t(s) ⊔ τ_(t−1)(next(s))
L5      for each gate u in topological order do τ_t(u) ← τ_t(u) ⊔ op̂(u)(τ_t of the fanins of u)
L6  AF ← the OR over all t and u of [τ_t(u) = ⊤]
L7  OK ← the AND over all t and u of [δ_Cons,t(u) ⊑ τ_t(u)]
L8  return the residual ¬(OK ∨ AF), and AF
```

Lines L2 to L5 are one pass of ternary symbolic simulation. Line L3 puts in the antecedent. Line L4 is the clock edge. Line L5 evaluates each gate on dual rails: for AND, the one-rail is the AND of the one-rails of the fanins and the zero-rail is the OR of their zero-rails, and NOT swaps the rails. The join at L5 keeps a value that the antecedent puts on an internal node. Line L6 collects the assignments where the antecedent contradicts itself or the circuit. At those $\phi$ no run satisfies $A$, so the assertion holds there without content. This is an *antecedent failure*, and a tool reports it, since it often means a wrong antecedent. Line L7 is the one-step check. The assertion holds where the residual is 0, and any assignment in the residual is a counterexample to inspect.

## Example

The circuit has inputs $a$, $b$, $c$, latches $r_1$ with $\mathrm{next}(r_1) = g_1 = a \wedge b$ and $r_2$ with $\mathrm{next}(r_2) = g_2 = r_1 \oplus c$, and an unrelated latch $q$ with $\mathrm{next}(q) = \neg q$. The assertion is

$A$: $a$ is $x$ at time 0, $b$ is $y$ at time 0, $c$ is $z$ at time 1, and $C$: $r_2$ is $(x \wedge y) \oplus z$ at time 2.

The defining trajectory, with each node shown by its value as a function of $x$, $y$, $z$:

| time | $a$ | $b$ | $c$ | $r_1$ | $r_2$ | $q$ | $g_1$ | $g_2$ |
|---|---|---|---|---|---|---|---|---|
| 0 | $x$ | $y$ | X | X | X | X | $x \wedge y$ | X |
| 1 | X | X | $z$ | $x \wedge y$ | X | X | X | $(x \wedge y) \oplus z$ |
| 2 | X | X | X | X | $(x \wedge y) \oplus z$ | X | X | X |

At time 0, $g_2 = \widehat{\mathrm{XOR}}(\mathrm{X}, \mathrm{X}) = \mathrm{X}$, and $g_1$ is binary under every $\phi$. At time 1, $r_1$ takes $g_1$ from time 0 at line L4. At time 2 the consequent asks $r_2$ for $(x \wedge y) \oplus z$, and $\tau_2(r_2)$ is that value, so OK is the constant 1. No node is $\top$, so AF is 0, and the residual is 0. The assertion holds.

The run used three variables. Symbolic simulation of the same three cycles needs a variable for each input in each cycle and for each latch, which is 12 variables, and $q$ would carry them through every cycle. Here $q$ stays X.

Now replace $g_2$ by $r_1 \vee c$. Then $\tau_2(r_2) = (x \wedge y) \vee z$. The two values differ exactly when $x \wedge y$ and $z$ are both 1, where the circuit gives 1 and $C$ asks for 0. So $\tau_2(r_2)$ has one-rail 1 and $\delta_C$ has zero-rail 1 there, and the residual is $x \wedge y \wedge z$. The counterexample is $x = y = z = 1$. The tests build both runs and compare them with all binary runs of the circuit.

## Correctness

**Claim (soundness).** For every assignment $\phi$ where the residual is 0 and every binary run $\rho$ that satisfies $A$ at $\phi$, $\rho$ satisfies $C$ at $\phi$. Where AF holds, no run satisfies $A$.

The proof rests on one lemma: if $\rho$ satisfies $A$ at $\phi$, then $\tau_t(u)(\phi) \sqsubseteq \rho_t(u)$ at every node and time. It goes by induction on $t$ and, inside a time, on the order inputs, latches, gates. Each line that writes $\tau_t(u)$ joins values that are all below $\rho_t(u)$. The antecedent part is below because $\rho$ satisfies $A$. The latch part is below by induction at time $t - 1$, because $\rho_t(s) = \rho_{t-1}(\mathrm{next}(s))$. The gate part is below because $\widehat{\mathrm{op}}$ is monotone and agrees with $\mathrm{op}$ on binary values: $\widehat{\mathrm{op}}(\tau \text{ of the fanins}) \sqsubseteq \widehat{\mathrm{op}}(\rho \text{ of the fanins}) = \rho_t(u)$. A join of values below a binary value is below it, since the join is the least upper bound. Monotonicity is the reason X is safe. Replacing a binary argument by X can only move the result down, to X, and never to the other binary value.

With the lemma, take $\phi$ where OK holds. Then $\delta_C(\phi) \sqsubseteq \tau(\phi) \sqsubseteq \rho$, so $\rho$ satisfies $C$. If AF holds at $\phi$, some $\tau_t(u)(\phi) = \top$, and no binary value lies above $\top$, so no run satisfies $A$ at $\phi$. A residual of 0 means that one of the two cases holds at each $\phi$. The full proof, with the dual-rail encoding, is in [the correctness proof](proofs/correctness.md).

The converse fails for binary runs. Seger and Bryant prove that the check is exact for the ternary model: the assertion holds in every trajectory of the ternary circuit exactly when $\delta_C \sqsubseteq \tau_A$. But a ternary trajectory need not be the image of a binary run. With $z = a \vee \neg a$ and $a$ left at X, $\tau(z) = \mathrm{X}$, so the check "$z$ is 1" fails, though $z$ is 1 in every binary run. When the antecedent fixes every input and every initial latch value to an expression, the trajectory is binary at each $\phi$, and the check is then exact for binary runs too.

## Complexity

The model is the word RAM with hashing in expected constant time. Let $d$ be the largest time, $P$ the number of gate inputs, $v$ the number of symbolic variables and $B$ the largest rail BDD.

- Lines L3 and L4 cost one OR of rails per node and latch per time, and line L5 costs $O(1)$ BDD operations per gate input. Each operation costs $O(B^2)$ by [Apply](/bdd-apply/). Over $d + 1$ times this is $O(d P B^2)$.
- Lines L6 and L7 cost $O(1)$ operations per node and time, which stays within the same bound.
- The BDDs are over $v$ variables, so $B \le 2^{v + 1} - 1$. The variables come from the assertion only, not from the circuit.

The last point is the gain. A circuit with a million latches costs a million X values, not a million variables. For a memory, an antecedent that writes one symbolic word to one address and reads it back leaves all other cells at X. The exponent cannot be removed in general: with $A$ empty except for the inputs set to variables, and $C$ asking one output to be 1, the residual is 0 exactly when the output function is a tautology, which is coNP-hard to decide.

## Properties

- Sound for binary runs: a passing check proves the assertion for all binary runs and all values of the variables. A failing check gives a set of assignments to inspect, which may be false failures caused by X.
- Exact for the ternary model of the circuit (Seger and Bryant 1995).
- Bounded: the check covers times $0$ to $d$, and every run of the circuit from any state, since the latches start at X unless $A$ sets them.
- The cost depends on the variables in the assertion and the depth, not on the number of latches.
- Deterministic. The result is the same BDD for every gate order that is topological.

## Variants and improvements

- **Generalized STE.** [GSTE](/generalized-symbolic-trajectory-evaluation/) replaces the linear sequence of times by an assertion graph and computes a fixed point, so a property can talk about unbounded time.
- **Theorem proving on top.** Hazelhurst and Seger (1995) give inference rules that join STE results, for example two assertions checked apart whose conjunction or sequential composition is then known to hold. This splits a check that is too large for one run.
- **Refinement by variables.** When a check fails because of X, the user replaces the X on a node by a fresh variable, as in the $a \vee \neg a$ case. This is a manual form of [abstraction refinement](/cegar/). Too many fresh variables bring back the cost of [symbolic simulation](/symbolic-simulation/).
- **Abstract interpretation.** The ternary lattice is an [abstract domain](/abstract-interpretation/) for sets of binary values, with a [Galois connection](/galois-connection/) between sets of bits and lattice values. STE is a forward abstract run with one step per clock cycle.
- **Other value encodings.** The dual-rail pair of BDDs can be replaced by a pair of SAT formulas, so the check becomes a SAT call. This is close to [bounded model checking](/bounded-model-checking/) with an X abstraction of the unconstrained nodes.

## When to use it

Use STE for properties of bounded length on large circuits where most of the state does not matter for the property: a read after a write in a memory array, one pass of a datapath pipeline, the result of one instruction from any state. It was built for these cases, and the X abstraction keeps the cost to the part of the circuit that the property reads. For properties over unbounded time use [GSTE](/generalized-symbolic-trajectory-evaluation/) or a [symbolic model checker](/symbolic-model-checking/). For small control circuits where much of the state matters, plain [symbolic simulation](/symbolic-simulation/) or [bounded model checking](/bounded-model-checking/) has no false failures to deal with.

## Pitfalls

- **False failures from X.** A node that the property needs but that the antecedent leaves at X gives a failing check with no real bug, as in $z = a \vee \neg a$. Before you report a bug, replay the counterexample in a binary simulator with values for the X nodes. If the failure goes away, add a variable to the antecedent.
- **Vacuous passes.** Where AF holds, the assertion passes because no run satisfies $A$. An antecedent with "$a$ is 1" and "$a$ is 0" at the same time passes every consequent. Check that AF is 0, or at least that it is the expected set.
- **The order of the lattice.** Code that copies the convention of [ternary simulation](/ternary-simulation/) with 0 below X computes the join as a meet. Fix one order for the whole tool.
- **Values on internal nodes.** An antecedent may set an internal node, and line L5 joins it with the gate output. If the circuit drives the other value, the result is $\top$ and the assertion passes without content there. Use this on purpose only, for example to cut a part of the circuit, and look at AF.
- **Depth one too short.** A latch takes its value at the next time. A consequent at time 1 on a register that is written from a value at time 1 sees only X.

## Implementations

## History

Bryant (1991) showed that ternary simulation, with X for unknown values and a monotone circuit model, verifies circuits soundly, and he used it for switch-level designs. Seger and Bryant (1995) built symbolic trajectory evaluation on top of it. They defined the lattice of states, trajectory formulas with the next-time operator, and the defining sequence and trajectory, and they proved that the one-step check is exact for the ternary model. The method went into Seger's Voss system and then into Forte at Intel, where it was used on memory arrays and arithmetic datapaths. Hazelhurst and Seger (1995) added a small theorem prover to join STE runs. Yang and Seger extended the method to assertion graphs as [generalized STE](/generalized-symbolic-trajectory-evaluation/).

## References
