---
tag: 75R68H
kind: technique
slug: compositional-verification
name: Compositional verification
aliases:
- Compositional model checking
- Modular verification
area: logic-and-constraints/model-checking
level: advanced
summary: Verify a parallel composition by checking each component, or a small abstraction of it, and combining the results by a sound rule, so that the full product is never built.
prereqs: [kripke-structure, labelled-transition-system, product-construction, state-explosion-problem]
see_also: [assume-guarantee-reasoning, simulation-relation, bisimulation, trace-equivalence, equivalence-checking, cegar, lstar-algorithm, partial-order-reduction]
sources:
  - paper: "Edmund M. Clarke, David E. Long and Kenneth L. McMillan, Compositional model checking, Fourth Annual IEEE Symposium on Logic in Computer Science (LICS), 1989"
    title: Compositional model checking
    locator: the interface rule, checking a component together with an abstraction of its environment, and the preservation of universal formulas
  - paper: doi:10.1145/177492.177725
    title: Orna Grumberg and David E. Long, Model checking and modular verification, ACM TOPLAS 16(3), 1994
    locator: pages 843 to 871 (the simulation preorder, its preservation of ACTL, the composition is simulated by each component, and the assume-guarantee use of tableaux)
  - paper: "Susanne Graf and Bernhard Steffen, Compositional minimization of finite state systems, CAV 1990, LNCS 531"
    title: Compositional minimization of finite state systems
    locator: minimizing components before composition, and interface specifications that keep the intermediate products small
  - book: isbn:9780521806084
    title: Willem-Paul de Roever, Frank de Boer, Ulrich Hannemann, Jozef Hooman, Yassine Lakhnech, Mannes Poel and Job Zwiers, Concurrency Verification, Introduction to Compositional and Noncompositional Methods, Cambridge University Press, 2001
    locator: the chapters on Owicki-Gries, on rely-guarantee and on assumption-commitment reasoning
---

Compositional verification proves a property of a system $M_1 \parallel M_2 \parallel \cdots \parallel M_n$ from facts about the components, without building the whole product. The product of $n$ components with $m$ states each can have $m^n$ states; this is the [state explosion problem](/state-explosion-problem/), and compositional methods attack it by "divide and conquer". Three families are common. *Property decomposition* splits the property into local parts and uses the fact that each component, or a sound abstraction of it, already restricts the behaviour of the composition: for example, every universal (ACTL) formula true of $M_1$ is true of $M_1 \parallel M_2$, because the composition is [simulated](/simulation-relation/) by $M_1$ (Clarke, Long and McMillan 1989; Grumberg and Long 1994). *Compositional minimization* replaces each component by its quotient under an equivalence, such as [bisimulation](/bisimulation/), that is a congruence for $\parallel$, and composes the small quotients. *Assume-guarantee reasoning* checks each component under an assumption about its environment and discharges the assumptions on the other components; it has its own page, [assume-guarantee reasoning](/assume-guarantee-reasoning/). This page is the general technique and the rules that make it sound.

## In plain words

A system made of many parts that run together can have more states than a computer can store, because the number of combined states multiplies. Compositional verification avoids the combined system. It checks each part on its own, or with a small summary of the other parts, and then uses a rule to conclude something about the whole.

The rules must be sound: whatever is true of the small checks must really carry over to the whole. Some properties carry over easily, such as "this part never sends a bad message". Others need care, because one part's good behaviour often depends on what the other parts do. Then each part is checked under an assumption about the others, and the assumptions are checked too.

## When it applies

- **The system is a parallel composition.** Hardware made of modules, protocols with several processes, software with threads or components that talk through interfaces.
- **The interfaces are narrow.** Each component interacts with the others through few signals or actions, so a summary of its environment can be small.
- **The property is local or decomposes.** For example $\mathbf{AG}(p_1 \wedge p_2)$ with $p_i$ over the variables of $M_i$, or a property of one interface.
- **The composition operator has good algebraic properties.** The equivalence or preorder in use is a congruence or precongruence for $\parallel$: if $M_1 \preceq A_1$ then $M_1 \parallel M_2 \preceq A_1 \parallel M_2$.

## The template

Let $\preceq$ be a preorder on components that is a precongruence for $\parallel$ and preserves the class of properties in use: if $M \preceq A$ and $A \models \varphi$ then $M \models \varphi$. [Simulation](/simulation-relation/) with ACTL, and trace inclusion with linear-time safety properties, are the standard choices.

```pseudo id=main
COMPOSITIONAL-CHECK(M_1, ..., M_n, φ)
L1  choose local properties φ_1, ..., φ_n and a sound rule that gives φ from them
L2  for i ← 1 to n do
L3      E_i ← a small abstraction of the environment of M_i         ▷ a quotient, an assumption, or the universal environment
L4      check E_i ∥ M_i ⊨ φ_i                                          ▷ a model checking run on a small system
L5      if it fails, test the counterexample on the full system; if it is real, return FAILS
L6      if it fails and is not real, refine E_i or the decomposition, and repeat from L2
L7  discharge the side conditions of the rule (for example M_j ⪯ E_i for the components j that E_i stands for)
L8  return HOLDS
```

**Why it is sound.** Suppose $E_i$ abstracts $M_{\ne i} = \parallel_{j \ne i} M_j$, that is $M_{\ne i} \preceq E_i$. By precongruence, $M_i \parallel M_{\ne i} \preceq M_i \parallel E_i$. By preservation, $M_i \parallel E_i \models \varphi_i$ gives $M_1 \parallel \cdots \parallel M_n \models \varphi_i$. The rule of line L1 then combines the $\varphi_i$. For universal properties a conjunction is enough: $\varphi_1 \wedge \cdots \wedge \varphi_n \Rightarrow \varphi$.

**The simplest case.** The universal environment, which can do anything at the interface, simulates every environment. So if $M_1$ with free inputs satisfies an ACTL formula over its own variables, then so does every composition that contains $M_1$. This is the first step of Clarke, Long and McMillan (1989).

**Minimization in place of abstraction.** If $\sim$ is a congruence for $\parallel$, then $M_1 \parallel M_2 \sim (M_1/{\sim}) \parallel (M_2/{\sim})$, where $M/{\sim}$ is the quotient. One composes the components in some order and minimizes after each step; the [equivalence checking](/equivalence-checking/) algorithms compute the quotients. An intermediate product can still be larger than the final one, because a partial composition lacks the constraints that later components add. Graf and Steffen (1990) used *interface specifications* that restrict an intermediate product to the behaviour that the rest of the system allows.

## Classic examples

- **Universal formulas and simulation.** Grumberg and Long (1994) showed for their composition of Moore machines that $M_1 \parallel M_2 \preceq M_1$, and that simulation preserves ACTL\*. So ACTL\* properties proved for a component, or for a component with an environment model that simulates the real one, hold for the system.
- **Process algebra toolsets.** CADP and other tools for CCS, CSP and LOTOS compose labelled transition systems step by step and minimize each step modulo strong or branching bisimulation, both congruences for parallel composition with hiding.
- **CSP refinement.** In CSP, trace refinement is a precongruence for parallel composition. So FDR can check a specification against a system in which some components were replaced by smaller processes that they refine.
- **Learned assumptions.** Cobleigh, Giannakopoulou and Păsăreanu (2003) learn the assumption $E_1$ about $M_2$ with the [L\* algorithm](/lstar-algorithm/), and check $M_2 \preceq E_1$ afterwards; see [assume-guarantee reasoning](/assume-guarantee-reasoning/).
- **Deductive methods.** For shared-variable programs, Owicki and Gries (1976) prove each thread and then check that no thread's step invalidates another thread's assertions. Jones's rely-guarantee method (1983) makes this compositional: each thread is proved under a *rely* condition on the other threads' steps and gives a *guarantee* about its own.

## Variations

- **Assume-guarantee reasoning.** The environment model is a property, not a component. Non-circular rules need no side condition beyond checking the assumption; circular rules need extra conditions. See [assume-guarantee reasoning](/assume-guarantee-reasoning/).
- **Abstraction refinement.** The environment abstraction of line L3 can come from [CEGAR](/cegar/), which refines it with spurious counterexamples.
- **Parameterized systems.** For $n$ identical processes, a property of one process and a model of "the rest" that does not depend on $n$ can prove the property for all $n$, when combined with symmetry or induction.
- **Compositional reasoning about time.** For synchronous circuits, McMillan's refinement method splits a property by time and by data, and uses circular assume-guarantee rules with time induction.

## Pitfalls

- **Wrong preservation class.** Simulation preserves universal properties only. An existential property such as $\mathbf{EF}\,p$ for a component need not hold in the composition, because the other components may block the path.
- **Deadlock.** Trace inclusion does not preserve the absence of deadlock. A component abstraction can have more traces and still deadlock less. Use a failures or simulation-based notion for deadlock freedom.
- **Equivalences that are not congruences.** Weak bisimulation is not a congruence for the CCS choice operator, so one must use the coarsest congruence inside it (observation congruence) when choice appears.
- **Large intermediate products.** Composing in a bad order can create a product much larger than the final system. Choose the order by the interfaces, and use interface specifications.
- **Circular reasoning.** Using each component's guarantee as the other's assumption is unsound without extra conditions; see the counterexamples on [assume-guarantee reasoning](/assume-guarantee-reasoning/).

## Exercises

1. Show that the universal environment over an interface simulates every component with that interface.
2. Prove that if $M_1 \preceq A_1$ for simulation then $M_1 \parallel M_2 \preceq A_1 \parallel M_2$, for the synchronous product of Kripke structures that agree on shared variables.
3. Give two components $M_1$ and $M_2$ such that $M_1 \models \mathbf{EF}\,p$ with $p$ over the variables of $M_1$, but $M_1 \parallel M_2 \not\models \mathbf{EF}\,p$.
4. For $n$ components with $m$ states each, in a ring where each component talks only with its two neighbours, how large can the product be, and how large is each check $E_i \parallel M_i$ if $E_i$ models the two neighbours?

## References
