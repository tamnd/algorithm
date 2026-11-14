---
tag: KNN3V9
kind: algorithm
slug: generalized-symbolic-trajectory-evaluation
name: Generalized symbolic trajectory evaluation
aliases:
- GSTE
area: eda/hardware-verification
level: research
summary: Yang and Seger's extension of STE to assertion graphs that express properties over unbounded time, checked by a fixed point on ternary symbolic states.
model: word-ram
complexity:
  vars: {N: the number of nodes of the circuit, P: the number of gate inputs, E: the number of edges of the assertion graph, B: "the number of nodes of the largest rail BDD (at most 2^(v + 1), v the number of symbolic constants)"}
  time: {worst: "O(N E^2 (N + P) B^2)"}
  space: {extra: "O(E N B)"}
properties: {deterministic: true, exact: false, complete: false, recursive: false}
history:
  year: 2001
  people: [Jin Yang, Carl-Johan H. Seger]
  note: Yang and Seger presented GSTE at ICCD 2001 and in IEEE Transactions on VLSI Systems in 2003, and described its abstraction and refinement at FMCAD 2002. It was used at Intel on large designs.
prereqs: [symbolic-trajectory-evaluation, fixed-point, safety-property]
see_also: [symbolic-trajectory-evaluation, ternary-simulation, product-machine, kleene-fixed-point-theorem, abstract-interpretation, symbolic-model-checking, liveness-property, assertion-based-verification]
sources:
  - paper: doi:10.1109/TVLSI.2003.812320
    title: J. Yang and C.-J. H. Seger, Introduction to generalized symbolic trajectory evaluation, IEEE Transactions on VLSI Systems 11(3), 345 to 353, 2003
    locator: assertion graphs with antecedent and consequent labels on edges, the strong semantics over finite initial paths, and the model checking algorithm by a fixed point over the edges
  - paper: "J. Yang and C.-J. H. Seger, Introduction to generalized symbolic trajectory evaluation, Proceedings of the IEEE International Conference on Computer Design (ICCD 2001), 360 to 367, 2001"
    title: J. Yang and C.-J. H. Seger, Introduction to generalized symbolic trajectory evaluation, ICCD 2001, 360 to 367
    locator: the conference version of the journal paper
  - paper: doi:10.1007/3-540-36126-X_5
    title: J. Yang and C.-J. H. Seger, Generalized symbolic trajectory evaluation, abstraction in action, Formal Methods in Computer-Aided Design (FMCAD 2002), LNCS 2517, 70 to 87, 2002
    locator: how the assertion graph and the symbolic constants set the abstraction of the check, and how to refine it when a check fails
  - paper: doi:10.1007/BF01383966
    title: C.-J. H. Seger and R. E. Bryant, Formal verification by symbolic evaluation of partially-ordered trajectories, Formal Methods in System Design 6(2), 147 to 189, 1995
    locator: the lattice of ternary states and the monotone circuit model that GSTE keeps
---

Generalized symbolic trajectory evaluation (GSTE) checks properties of a circuit over unbounded time. [STE](/symbolic-trajectory-evaluation/) checks an assertion whose times run from 0 to a fixed depth $d$. GSTE replaces this line of times by an *assertion graph*: a directed graph whose edges carry an antecedent and a consequent, each about one clock cycle. A path through the graph is a pattern of cycles, and loops in the graph give patterns of any length. The check computes, for each edge, one ternary symbolic state that lies below every state in which a run can take that edge. It finds these states by a fixed point that starts at $\top$ (no state) and goes down the lattice. The lattice, the dual-rail encoding and the monotone gate evaluation are those of [STE](/symbolic-trajectory-evaluation/). This page covers the assertion graph and what it adds.

## In plain words

Take a register that loads $d$ when $en$ is 1 and keeps its value when $en$ is 0. The property is "after a load of $x$, while $en$ stays 0, the register holds $x$". That holds for 1 cycle, 2 cycles, a thousand cycles. STE needs one check per length.

GSTE draws the property as a small graph. One edge says "load $x$ now". A loop says "$en$ is 0 now, and the register must hold $x$". A path that takes the loop $k$ times is a hold of $k$ cycles. GSTE goes around the loop with ternary simulation until the state stops changing. That final state covers every number of turns, so one finite computation checks all lengths. As in STE, unknown values are X, and a pass is a proof.

## The problem

**Assertion graphs.** An assertion graph is $G = (V, v_0, E)$ with a finite set of vertices $V$, an initial vertex $v_0$, and edges $e = (\mathrm{src}(e), \mathrm{dst}(e))$. Each edge has an antecedent $\mathrm{ant}(e)$ and a consequent $\mathrm{cons}(e)$. Each is a set of constraints $(u, a, g)$, read "if $g$ then node $u$ is $a$" at the time the edge is taken, where $a$ and $g$ are Boolean expressions over symbolic constants. The constants keep one value along a whole run. An assignment of them is $\phi$.

**Strong semantics.** A run $\rho$ of the circuit, as on the STE page, gives each node a binary value $\rho_t(u)$ at each time $t$. The graph *holds* when for every $\phi$, every path $e_0 e_1 \cdots e_k$ with $\mathrm{src}(e_0) = v_0$ and $\mathrm{dst}(e_i) = \mathrm{src}(e_{i+1})$, and every run that meets $\mathrm{ant}(e_i)$ at time $i$ under $\phi$ for all $i \le k$, the run meets $\mathrm{cons}(e_k)$ at time $k$ under $\phi$. A consequent is excused only by the antecedents up to its own time. Yang and Seger call this the strong semantics. For each $k$ it is a bounded statement, but there is no bound on $k$.

**The task.** Compute the set of $\phi$ where the graph fails, as a BDD, or a superset of it that is exact in the common cases.

## The algorithm

$\delta(F)$ is the least ternary state that a set of constraints asks for, as on the STE page. The meet $\sqcap$ is the AND of the rails, so $0 \sqcap 1 = \mathrm{X}$, and $\top \sqcap a = a$. A ternary state with a $\top$ node stands for the empty set of states, and line L7 then sets all its nodes to $\top$.

```pseudo id=main
GSTE(C, G)
L1  for each edge e do sim(e) ← ⊤ on every node
L2  repeat
L3      for each edge e do
L4          pre ← (X on every node if src(e) = v₀, else ⊤) ⊓ the meet of sim(e′) over the edges e′ into src(e)
L5          σ ← δ(ant(e)); for each latch s do σ(s) ← σ(s) ⊔ pre(next(s))
L6          for each gate u in topological order do σ(u) ← σ(u) ⊔ op̂(u)(σ of the fanins of u)
L7          new(e) ← σ, with every node set to ⊤ where pre or σ has a ⊤ node
L8  until new = sim; otherwise sim ← new and repeat
L9  residual ← the OR over all edges e of ¬[δ(cons(e)) ⊑ sim(e)]
L10 return residual
```

Line L4 gathers the states in which a run can be just before it takes $e$. A path may start at $v_0$ from any state, so $v_0$ adds the all-X state. The meet over several in-edges keeps only what they share. It is an over-approximation of the union of the state sets. Lines L5 and L6 are one step of ternary symbolic simulation from that state with the antecedent of $e$ added. Line L7 marks the edge as not taken where the previous state set or the new one is empty. Line L8 stops when a whole round changes no BDD. Line L9 is the STE comparison, done once per edge on the fixed point.

A chain $v_0 \to v_1 \to \cdots \to v_{d+1}$ with the constraints of time $t$ on its $t$-th edge is an STE assertion. GSTE then does the STE computation, except that a conflict in a later antecedent does not excuse an earlier consequent. The new parts are the loops, the meets at vertices with several in-edges, and the fixed point.

## Example

The circuit has inputs $en$ and $d$, one latch $r$ with $\mathrm{next}(r) = m$, and gates $\overline{en} = \neg en$, $t_1 = en \wedge d$, $t_2 = \overline{en} \wedge r$, $m = t_1 \vee t_2$. The graph has vertices $v_0, v_1$ and three edges:

- $e_0 = (v_0, v_0)$, no antecedent and no consequent: wait any number of cycles.
- $e_1 = (v_0, v_1)$, antecedent "$en$ is 1, $d$ is $x$": load $x$.
- $e_2 = (v_1, v_1)$, antecedent "$en$ is 0", consequent "$r$ is $x$": hold.

The fixed point, by rounds, shows $r$ and $m$ (other nodes follow from them):

| round | $\mathrm{sim}(e_0)$ | $\mathrm{sim}(e_1)$: $r$, $m$ | $\mathrm{sim}(e_2)$: $r$, $m$ |
|---|---|---|---|
| 0 | all $\top$ | all $\top$ | all $\top$ |
| 1 | all X | X, $x$ | all $\top$ (pre is $\mathrm{sim}_0(e_1) \sqcap \mathrm{sim}_0(e_2) = \top$) |
| 2 | all X | X, $x$ | $x$, $x$ |
| 3 | all X | X, $x$ | $x$, $x$ (pre is $\mathrm{sim}_2(e_1) \sqcap \mathrm{sim}_2(e_2)$, with $m = x$ in both) |

Round 3 changes nothing, so the loop stops. On $e_1$, $t_1 = 1 \wedge x = x$ and $t_2 = 0 \wedge \mathrm{X} = 0$, so $m = x$ although $r$ is X. On $e_2$, $r = x$ satisfies the consequent, and the residual is 0. The property holds for holds of every length, after a load at any time, from every initial state. The run used one symbolic constant.

Now replace $m$ by $t_1 \vee r$, a register that can set but never clear. On $e_1$, $m = x \vee \mathrm{X}$, which is 1 when $x = 1$ and X when $x = 0$. Then $\mathrm{sim}(e_2)$ has $r$ with one-rail $x$ and zero-rail 0, and the consequent asks for zero-rail $\neg x$. The residual is $\neg x$. The failure is real: start with $r = 1$, load 0, hold, and $r$ is still 1. The tests find this run by enumeration.

## Correctness

**Claim (soundness).** If the residual is 0 at $\phi$, the graph holds at $\phi$ under the strong semantics. More exactly, for every edge $e$, the consequent of $e$ holds at every time at which some run takes $e$ along a path from $v_0$ whose antecedents it meets, wherever $\neg[\delta(\mathrm{cons}(e)) \sqsubseteq \mathrm{sim}(e)]$ is 0.

**Key lemma.** At the fixed point, for every path $e_0 \cdots e_k$ from $v_0$ and every run $\rho$ that meets $\mathrm{ant}(e_i)$ at time $i$ for all $i \le k$, $\mathrm{sim}(e_k)(\phi) \sqsubseteq \rho_k$ at every node. The proof is by induction on $k$. The state $\mathrm{pre}$ of $e_k$ is X at $k = 0$. At $k > 0$ it is a meet that includes $\mathrm{sim}(e_{k-1})$, so it lies below $\mathrm{sim}(e_{k-1})$ and hence below $\rho_{k-1}$. So $\mathrm{pre}(\mathrm{next}(s)) \sqsubseteq \rho_k(s)$ for each latch. From there, lines L5 and L6 are one step of the STE lemma: joins of values below a binary value stay below it, and the gate tables are monotone. Since $\mathrm{pre}$ and $\sigma$ lie below binary states, neither has a $\top$, and line L7 changes nothing. With the lemma, $\delta(\mathrm{cons}(e_k)) \sqsubseteq \mathrm{sim}(e_k) \sqsubseteq \rho_k$, so $\rho$ meets $\mathrm{cons}(e_k)$.

**Termination.** Each round applies a map $F$ that is monotone in the information order, since meet, join, the gate tables and the step of line L7 are all monotone. The first round gives $\mathrm{sim}_1 \sqsubseteq \top = \mathrm{sim}_0$, and monotonicity gives $\mathrm{sim}_{n+1} \sqsubseteq \mathrm{sim}_n$ for all $n$. At one $\phi$, each of the $N E$ values can go down at most twice, from $\top$ to 0 or 1 to X. A round that changes nothing at $\phi$ stays unchanged at $\phi$ for ever. So the loop ends after at most $2 N E + 1$ rounds, at the greatest fixed point of $F$ in the information order. The proofs are in [the correctness proof](proofs/correctness.md).

**What is lost.** The check is not complete for binary runs, for two reasons. X loses information, as in STE. The meet at a vertex also loses it: if one in-edge brings $r = 0$ and another brings $r = 1$, the meet has $r = \mathrm{X}$. When every input and every initial latch value is fixed and the graph is a chain, each $\mathrm{sim}(e)$ is the exact binary state of the one run, and the check is exact. The tests check this case.

## Complexity

The model is the word RAM with hashing in expected constant time. Let $N$ be the number of nodes, $P$ the number of gate inputs, $E$ the number of edges and $B$ the largest rail BDD.

- Line L4 costs $O(N)$ meets per in-edge of $\mathrm{src}(e)$. Computing it once per vertex, a round costs $O(E N)$ meets for line L4 over all vertices.
- Lines L5 to L7 cost $O(N + P)$ BDD operations per edge, so a round costs $O(E (N + P))$ operations, each $O(B^2)$ by [Apply](/bdd-apply/).
- There are at most $2 N E + 1$ rounds, which gives $O(N E^2 (N + P) B^2)$ time in the worst case.
- The states of all edges take $O(E N)$ BDD roots, and the nodes they share take $O(E N B)$ space.

The round bound is a worst case. In the example the states settle after two rounds, and a third round sees that nothing changed. The tests check the bound on random circuits and graphs. As in STE, the variables come from the symbolic constants of the graph, not from the circuit, and nodes outside the property stay X. Deciding whether a property holds is at least as hard as the STE case, which is coNP-hard.

## Properties

- Sound for all runs and all path lengths under the strong semantics.
- Not complete: X and the meets at vertices can cause failures that no run shows. A failure must be checked against a binary run.
- Terminates on every input, because the lattice of ternary symbolic states over a fixed set of variables is finite.
- One fixed point covers patterns of any length, which a bounded method such as STE or [bounded model checking](/bounded-model-checking/) cannot do.
- The precision is set by the user through the shape of the graph, not by a fixed abstraction in the tool.

## Variants and improvements

- **Other semantics.** Under the strong semantics only past antecedents count. Yang and Seger also define a semantics over infinite paths in which antecedents later on the path count too. That needs more than the forward fixed point of this page. Restricting the infinite paths by fairness conditions leads to [liveness properties](/liveness-property/).
- **Refinement by the graph.** When a meet loses needed information, split the vertex into two copies, one per in-edge, or replace a set of concrete constants by one symbolic constant, so that one edge covers all the cases. Yang and Seger (2002) treat these choices as the abstraction of the check.
- **Concrete version.** Replace ternary states by sets of binary states, meet by union and join by intersection. The fixed point is then reachability in the [product](/product-machine/) of the circuit and the graph, and the check is exact. This is [symbolic model checking](/symbolic-model-checking/) of a safety property, at the cost of variables for all latches.
## When to use it

Use GSTE for properties of unbounded length on circuits too large for a [symbolic model checker](/symbolic-model-checking/), where the property reads only part of the state: data integrity in a memory or queue over any number of cycles, a register file that keeps a value until it is written, a control protocol given as a small graph of phases. If a bound is known and small, [STE](/symbolic-trajectory-evaluation/) is simpler. If much of the state matters, a model checker with exact sets gives no false failures. For property languages with assertions on a simulator, see [assertion-based verification](/assertion-based-verification/).

## Pitfalls

- **No wait loop at $v_0$.** Without the edge $e_0$ of the example, every path starts with a load at time 0, and the check says nothing about a load at a later time. Most properties need a loop at the initial vertex with an empty antecedent.
- **Merging cases at one vertex.** Two edges "load 0" and "load 1" into one vertex give $r = \mathrm{X}$ there, and every later consequent on $r$ fails. Use one edge with a symbolic constant $x$, or two vertices.
- **Reading the strong semantics as implication over the whole path.** A consequent at time $k$ is not excused by a contradiction in the antecedent at time $k + 1$. A property that relies on future inputs needs another semantics.
- **Vacuous edges.** An edge whose antecedent conflicts with the circuit is never taken, and its consequents pass. Check which edges have $\mathrm{sim}(e) = \top$ everywhere, as the antecedent failure is checked in STE.
- **Symbolic variables that change.** A symbolic constant has the same value on the whole path. To talk about a fresh value at each step, use X and a consequent that compares two nodes, or add a vertex per value.

## Implementations

## History

Seger and Bryant (1995) built [STE](/symbolic-trajectory-evaluation/) on a lattice of ternary states, with assertions of bounded depth. Jin Yang and Carl-Johan Seger at Intel extended the antecedent and consequent to the edges of an assertion graph. They presented GSTE at ICCD 2001 and in the IEEE Transactions on VLSI Systems in 2003, with the strong semantics, a semantics over infinite paths, and fixed point algorithms for the check. At FMCAD 2002 they described how the graph and the symbolic constants set the abstraction and how to refine it. GSTE was used at Intel on large circuits where the property reads only part of the state.

## References
