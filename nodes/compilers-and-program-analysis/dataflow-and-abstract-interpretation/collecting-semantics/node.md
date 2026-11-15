---
tag: AR4EWF
kind: definition
slug: collecting-semantics
name: Collecting semantics
aliases:
- static semantics of reachable states
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: The semantics that maps each program point to the set of all states that reach it, the most precise property an analysis can compute.
prereqs: [control-flow-graph, fixed-point, knaster-tarski-theorem]
see_also: [abstract-interpretation, abstract-domain, galois-connection, kleene-fixed-point-theorem, meet-over-all-paths-solution, inductive-invariant, rice-theorem]
sources:
  - paper: doi:10.1145/512950.512973
    title: "Patrick Cousot and Radhia Cousot, Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints, POPL 1977, pages 238 to 252"
    locator: the static semantics of a program as the least fixed point of a system of equations over sets of environments, one per program point, and the correctness of abstract interpretations with respect to it
  - paper: "Patrick Cousot and Radhia Cousot, Static determination of dynamic properties of programs, Proceedings of the Second International Symposium on Programming, B. Robinet (ed.), Dunod, Paris, 1976, pages 106 to 130"
    locator: the semantic equations of a flowchart program and the correctness of the interval analysis with respect to them
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Chapter 4 (Abstract Interpretation), the correctness relations and the collecting semantics against which the analyses are proved correct
  - book: isbn:9780262043410
    title: Xavier Rival and Kwangkeun Yi, Introduction to Static Analysis, An Abstract Interpretation Perspective, MIT Press, 2020
    locator: Chapter 3 and Chapter 4 (the concrete semantics as a least fixed point over sets of states, the reachable states of a transition system)
  - book: isbn:9780262044905
    title: Patrick Cousot, Principles of Abstract Interpretation, MIT Press, 2021
    locator: the chapters on the structural fixpoint semantics and on the reachability semantics
---

The collecting semantics of a program maps each program point to the set of all states that some run of the program has at that point. It is the least fixed point of a set of equations over sets of states, so it is the strongest property of each point that holds in every run. Every analysis in [abstract interpretation](/abstract-interpretation/) is proved sound against it, and no algorithm computes it in general.

## Definition

The programs are in the toy IR: three-address code in basic blocks, with unbounded integers. This page uses the Cousot convention for the order: sets of states are ordered by inclusion $\subseteq$, the join is union, and the bottom element $\emptyset$ means that no state reaches the point. Lower is more precise. The dataflow pages, such as [maximal fixed-point solution](/maximal-fixed-point-solution/), use the dual meet order of Kildall; turning the order upside down maps one convention onto the other.

**States.** Let $V$ be the set of names of the program. An environment is a partial map $\rho : V \rightharpoonup \mathbb{Z}$. A state at the start of block $\ell$ is the pair $(\ell, \rho)$. Let $\mathit{Env}$ be the set of all environments.

**Edge transformers.** For each CFG edge $\ell \to \ell'$, let $\mathit{post}_{\ell \to \ell'}(X)$ be the set of environments $\rho'$ such that some $\rho \in X$, run through the instructions of $\ell$, gives $\rho'$, and the terminator of $\ell$ then goes to $\ell'$. A run that traps or returns in $\ell$ adds nothing. Since $\mathit{post}_{\ell \to \ell'}$ is defined one element at a time, it preserves all unions:

$$ \mathit{post}_{\ell \to \ell'}\Bigl(\bigcup_{i} X_i\Bigr) = \bigcup_{i} \mathit{post}_{\ell \to \ell'}(X_i). $$

**The equations.** Let $\mathit{Init} \subseteq \mathit{Env}$ be the set of initial environments: each one binds the parameters to integers, or to the integers that a precondition allows. The lattice is $L = \mathcal{P}(\mathit{Env})^{\mathit{Labels}}$ with the pointwise order. It is a complete lattice. The function $F : L \to L$ is

$$ F(S)(\ell) = [\ell = \mathit{entry}]\,\mathit{Init} \ \cup \bigcup_{\ell' \to \ell} \mathit{post}_{\ell' \to \ell}\bigl(S(\ell')\bigr), $$

where $[\ell = \mathit{entry}]\,\mathit{Init}$ is $\mathit{Init}$ at the entry block and $\emptyset$ elsewhere. $F$ is monotone. The **collecting semantics** is

$$ \mathit{Coll} = \mathrm{lfp}\, F . $$

It exists by the [Knaster-Tarski theorem](/knaster-tarski-theorem/), and it is the intersection of all $S$ with $F(S) \subseteq S$.

**The reachable states.** Let $R(\ell)$ be the set of environments $\rho$ such that some run from an initial environment arrives at the start of block $\ell$ with environment $\rho$. Then $\mathit{Coll} = R$.

*Proof.* $R$ is a fixed point of $F$: a state at the start of $\ell$ is reached either at the start of the run ($\ell = \mathit{entry}$, $\rho \in \mathit{Init}$) or by one block step from a state that is reached at a predecessor, and each such step gives a state in $R(\ell)$. So $\mathit{Coll} \subseteq R$. For the other inclusion, take any $S$ with $F(S) \subseteq S$. By induction on the number $k$ of block steps of a run, the state after $k$ steps is in $S$: for $k = 0$ it is in $\mathit{Init} \subseteq F(S)(\mathit{entry}) \subseteq S(\mathit{entry})$, and one more step applies a $\mathit{post}$ of an edge, which stays inside $F(S) \subseteq S$. So $R \subseteq S$ for every such $S$, and $R \subseteq \mathit{Coll}$. $\square$

**Iteration.** Since each $\mathit{post}$ preserves unions, $F$ preserves the unions of increasing chains, so the [Kleene fixed-point theorem](/kleene-fixed-point-theorem/) gives $\mathit{Coll} = \bigcup_{k \ge 0} F^k(\bot)$. By induction on $k$, $F^k(\bot)(\ell)$ is the set of states that runs of fewer than $k$ block steps reach at $\ell$. The union may need infinitely many steps.

**Paths.** Unfold the union over the steps of a run. For a path $p = \ell_0 \to \ell_1 \to \cdots \to \ell_k$ with $\ell_0 = \mathit{entry}$ and $\ell_k = \ell$, let $\mathit{post}_p$ be the composition of the edge transformers along $p$. Then

$$ \mathit{Coll}(\ell) = \bigcup_{p \,:\, \mathit{entry} \leadsto \ell} \mathit{post}_p(\mathit{Init}). $$

This is the join over all paths, in the Cousot order, of the concrete transfer functions. Every path counts, also a path that no run follows, because $\mathit{post}_p$ is empty for such a path. The equation solution and the path solution agree because each $\mathit{post}$ distributes over union; this is the case of equality in the [MOP and MFP coincidence theorem](/mop-mfp-coincidence-theorem/), read in the dual order.

**Soundness of an analysis.** An analysis gives, for each block $\ell$, an abstract value $A(\ell)$ with a meaning $\gamma(A(\ell)) \subseteq \mathit{Env}$ (see [abstract domain](/abstract-domain/)). It is *sound* when

$$ \forall \ell : \quad \mathit{Coll}(\ell) \subseteq \gamma(A(\ell)). $$

**Not computable.** A toy IR program with unbounded integers can simulate a [register machine](/register-machine/). So the question "is $\mathit{Coll}(\ell) = \emptyset$?" for the block that holds `ret` is the [halting problem](/halting-problem/), and it is undecidable. By [Rice's theorem](/rice-theorem/), every nontrivial question about $\mathit{Coll}$ is undecidable. An analysis therefore computes an over-approximation in an [abstract domain](/abstract-domain/).

## Examples and non-examples

**A loop with a parameter.** The parameter is `n`.

```
entry:
  i = 0
  jump head
head:
  t = i < n
  br t body exit
body:
  i = i + 1
  jump head
exit:
  ret i
```

The edges are entry $\to$ head, head $\to$ body, head $\to$ exit and body $\to$ head. With $\mathit{Init} = \{ \{n \mapsto 3\} \}$, round-robin iteration in the order entry, head, body, exit gives these values of `i` at the start of each block. Each value computed this way stays inside $\mathit{Coll}$, since $F$ is monotone and each step applies one component of $F$ to values inside $\mathit{Coll}$, and each round is at least the Kleene iterate of the same number, so it ends at $\mathit{Coll}$.

| round | head | body | exit |
|---|---|---|---|
| 1 | $\{0\}$ | $\{0\}$ | $\emptyset$ |
| 2 | $\{0, 1\}$ | $\{0, 1\}$ | $\emptyset$ |
| 3 | $\{0, 1, 2\}$ | $\{0, 1, 2\}$ | $\emptyset$ |
| 4 | $\{0, 1, 2, 3\}$ | $\{0, 1, 2\}$ | $\{3\}$ |
| 5 | no change | | |

The plain Kleene iterates $F^k(\bot)$ reach the same result and are stable from $k = 9$, because they move one block per step.

With $\mathit{Init}$ equal to all values of `n`, the result is an infinite set at each block. Write the states as pairs $(n, i)$:

$$ \mathit{Coll}(\mathit{head}) = \{ (n, i) : 0 \le i \le \max(n, 0) \}, \qquad \mathit{Coll}(\mathit{exit}) = \{ (n, i) : i = \max(n, 0) \}. $$

Here $F^k(\bot)$ grows at each step, and only the infinite union reaches the fixed point. An analysis in the [interval domain](/interval-domain/) finds $i \ge 0$ at head; one in the [polyhedra domain](/polyhedra-domain/) also finds $i \le n$ when $n \ge 0$ holds on entry.

**An unreachable block.** Change the terminator of head to `jump head`. Then no edge leads to exit, and $\mathit{Coll}(\mathit{exit}) = \emptyset$, the bottom element. In the Cousot order $\emptyset$ means "no state", not "no information".

**Non-example: one value set per name.** Two runs reach a point with $(x, y) = (1, 2)$ and $(2, 1)$. The collecting semantics is the set $\{(1, 2), (2, 1)\}$, so it proves $x + y = 3$. The map that keeps one set of values per name, $x \in \{1, 2\}$ and $y \in \{1, 2\}$, also allows $(1, 1)$. That map is an abstraction of the collecting semantics (the cartesian abstraction), not the collecting semantics itself.

**Non-example: one run.** The outcome of one run, `run(prog, args)`, is a concrete execution. The collecting semantics collects the states of all runs from all initial states in $\mathit{Init}$.

**Non-example: the trace semantics.** The set of all finite runs, each one a sequence of states, is more precise than the collecting semantics. It can say "at head, `i` grows by one between two visits", and the set of reachable states cannot. The collecting semantics is the abstraction of the trace semantics that keeps, for each point, the set of last states of the traces that end there.

## Related definitions

- [Abstract domain](/abstract-domain/): a set of descriptions of sets of states, with a concretization $\gamma$, used to approximate $\mathit{Coll}$.
- [Galois connection](/galois-connection/): the pair $(\alpha, \gamma)$ that gives the best description of a set of states.
- [Abstract interpretation](/abstract-interpretation/): the general technique that computes a sound approximation of $\mathrm{lfp}\, F$; this page gives its concrete side.
- [Inductive invariant](/inductive-invariant/): a family $I$ with $F(I) \subseteq I$. Each one contains $\mathit{Coll}$, and $\mathit{Coll}$ is itself inductive, so it is the strongest inductive invariant.
- [Meet-over-all-paths solution](/meet-over-all-paths-solution/): the path formula above, in the dataflow convention and over an abstract lattice.
- [Fixed point](/fixed-point/), [Knaster-Tarski theorem](/knaster-tarski-theorem/) and [Kleene fixed-point theorem](/kleene-fixed-point-theorem/): the existence of $\mathrm{lfp}\, F$ and its computation as a limit.
- Variants. The *relational* collecting semantics collects pairs (initial environment, current environment); procedure summaries use it. The *backward* collecting semantics collects the states from which an error state can be reached, with $\mathit{pre}$ in place of $\mathit{post}$.

## References
