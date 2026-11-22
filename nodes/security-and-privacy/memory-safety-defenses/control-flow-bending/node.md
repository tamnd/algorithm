---
tag: TF4J63
kind: technique
slug: control-flow-bending
name: Control-flow bending
aliases:
- CFB attack
area: security-and-privacy/memory-safety-defenses
level: research
summary: Attacks programs under fully precise static CFI by steering flow along allowed edges, often through functions such as memcpy and printf.
history:
  year: 2015
  people: [Nicholas Carlini, Antonio Barresi, Mathias Payer, David Wagner, Thomas R. Gross]
  note: Carlini et al. (USENIX Security 2015) showed that fully precise static CFI still allows powerful attacks in five of six real programs, and that a shadow stack is needed.
prereqs: [control-flow-integrity, shadow-stack]
see_also: [code-pointer-integrity, data-oriented-programming, return-oriented-programming, format-string-vulnerability, turing-completeness, points-to-analysis, call-graph, memory-safety]
sources:
  - url: "https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/carlini"
    title: Nicholas Carlini, Antonio Barresi, Mathias Payer, David Wagner and Thomas R. Gross, Control-flow bending, on the effectiveness of control-flow integrity, 24th USENIX Security Symposium, 2015, pages 161-176
    locator: the abstract (fully precise static CFI, Turing-complete computation with calls to the standard library, five of six programs, and the effect of a shadow stack in three of six), and the evaluation sections
  - paper: doi:10.1145/1609956.1609960
    title: Martin Abadi, Mihai Budiu, Ulfar Erlingsson and Jay Ligatti, Control-flow integrity, principles, implementations, and applications, ACM Transactions on Information and System Security 13(1), article 4, 2009
    locator: the statement of the CFI guarantee, which limits targets to the graph and says nothing about which allowed target is taken
  - paper: doi:10.1145/3054924
    title: Nathan Burow, Scott A. Carr, Joseph Nash, Per Larsen, Michael Franz, Stefan Brunthaler and Mathias Payer, Control-flow integrity, precision, security, and performance, ACM Computing Surveys 50(1), article 16, 2017, pages 1-33
    locator: the discussion of the precision of backward edges and of the attacks on CFI
  - paper: "Shuo Chen, Jun Xu, Emre C. Sezer, Prachi Gauriar and Ravishankar K. Iyer, Non-control-data attacks are realistic threats, 14th USENIX Security Symposium, 2005, pages 177-191"
    locator: the thesis that corrupting data other than code pointers is enough for serious attacks, which control-flow bending generalizes
---

Control-flow bending (CFB) is the class of attacks that stay inside the control flow graph of [control-flow integrity](/control-flow-integrity/) and still take over a program. Every indirect transfer goes to a target that the policy allows, so every check passes, but the attacker chooses among the allowed targets and changes the data that the allowed functions work on. Carlini, Barresi, Payer, Wagner and Gross (USENIX Security 2015) studied the strongest case for the defender: *fully precise static CFI*, the most restrictive static policy that does not break the program, in which each indirect branch may go only to targets it can really reach in some correct run. They showed that a memory error still gave Turing-complete computation using only calls to the standard library, and that on six real programs, powerful attacks remained possible in five. Their second finding is the main lesson for defenders: CFI without a [shadow stack](/shadow-stack/) lets each function return to any of its callers, and adding a shadow stack removed arbitrary code execution in three of the six. CFB generalizes the non-control-data attacks of Chen et al. (2005) and sits between [return-oriented programming](/return-oriented-programming/) and [data-oriented programming](/data-oriented-programming/). This page describes the class, the conditions, the history and the defenses, with no code and no details of real software.

## In plain words

CFI gives each jump in a program a list of allowed destinations and stops the program if a jump goes anywhere else. That stops attacks that jump into the middle of code.

But the lists are made before the program runs, so they must allow every destination that any correct run might need. A common function, such as a copy routine, is called from hundreds of places, so its return may go back to any of them. A call through a pointer may go to any of the functions that pointer could hold.

An attacker who can change data can make the program take allowed paths in an order it never intended, and can change the inputs of the functions on those paths. Each step looks legal. Together they do the attacker's work. A shadow stack takes away the freedom at returns, which is the biggest part of it.

## When it applies

The class needs these conditions. Each defense removes one.

- **A memory error that writes program data.** The attacker can change memory that the program later reads, by an overflow or an arbitrary write. Bounds checks and [memory safety](/memory-safety/) remove it.
- **CFI is the main defense.** The program runs under a CFI policy, perhaps fully precise, so direct hijacks to arbitrary code fail. Without CFI, simpler attacks such as [return-oriented programming](/return-oriented-programming/) are open.
- **Allowed sets with more than one element.** Some indirect calls may go to several functions, and, without a shadow stack, each return may go to any caller of its function. The [call graph](/call-graph/) of a large program gives common functions many callers.
- **Functions whose effect depends on attacker data.** Some allowed targets do a lot of work from their arguments: copy routines that write memory, and formatted output routines whose format argument controls what they read and write. When their arguments are corrupted, they can change memory, including control data, while every transfer stays allowed.

## The template

The class has the shape below. Each named hole is a condition from the list, and each comment names the defense that breaks the chain at that line. It is a description of the class, not a procedure.

```pseudo id=main
CONTROL-FLOW-BENDING-CLASS(program P under CFI with allowed sets T(s))
L1  need ⟨memory error⟩: the attacker can change data that P reads              ▷ broken by bounds checks and memory safety
L2  every indirect transfer from a site s goes to some x ∈ T(s): all CFI checks pass
L3  need ⟨choice at a site⟩: |T(s)| > 1 and the choice depends on changed data  ▷ narrower sets: better analysis, types, context
L4  need ⟨free returns⟩: a return may go to any caller of its function           ▷ shadow stack: only the matching call site
L5  need ⟨powerful allowed function⟩: an allowed target whose effect depends on its arguments   ▷ CPI and data-flow checks keep its inputs correct
L6  effect: allowed edges in an unintended order, with corrupted arguments, compute what the attacker wants   ▷ least privilege limits the damage
```

**Walk-through.** Line L1 is the memory error, the same as for every attack on this site; the class does not exist without it. Line L2 is the defining property of the class: the CFI guarantee holds, and the attack works inside it. That is consistent with the theorem of [control-flow integrity](/control-flow-integrity/), which bounds the set of targets but says nothing about which allowed target a transfer takes. Line L3 is the choice that the policy leaves. Line L4 is the largest source of freedom in static policies: a function called from $m$ places has $m$ allowed return targets, and a [shadow stack](/shadow-stack/) reduces them to one. Line L5 is the use of allowed functions as building blocks: if a copy or a formatting routine runs with corrupted arguments, it can change memory, including return addresses in its own frame, without any transfer leaving the graph. Line L6 is the effect.

**What the template shows about each defense.** Better static analysis shrinks line L3 but cannot go below fully precise static CFI, which was the assumption of the paper. A shadow stack breaks line L4 and was the most effective single addition in the paper. Lines L1 and L5 are broken only by defenses that protect data: [memory safety](/memory-safety/), [code-pointer integrity](/code-pointer-integrity/) for the pointers, or data-flow checks for other data.

**An abstract model of line L4.** Let a function $D$ be called from sites $c_1, \ldots, c_m$, and suppose that, with corrupted arguments, $D$ can change its own saved return address before it returns. Under a static policy, the allowed return targets of $D$ are the $m$ instructions after $c_1, \ldots, c_m$, so the corrupted return can go to any of them and the check passes. Under a shadow stack, the return of an instance of $D$ called from $c_i$ must go to the instruction after $c_i$, so the change is caught, by the theorem on the [shadow stack](/shadow-stack/) page. The model uses made-up names only; it shows why the number of callers, not the number of instructions, measures the freedom at line L4.

## Classic examples

- **Non-control-data attacks (2005).** Chen et al. showed that changing data other than code pointers, such as user identities, configuration values or decision flags, is enough for serious attacks on real servers. CFB extends this to attacks that also use the freedom of allowed control flow.
- **Coarse CFI broken (2014).** Several research groups built general attacks under coarse policies that allow any call-preceded instruction as a return target. The open question was whether precise policies would be enough, which led to the CFB study.
- **Fully precise static CFI (2015).** Carlini et al. assumed the best static policy and evaluated six real programs. Powerful attacks were still possible in five. They also showed that a formatted output function, with an attacker-controlled format argument, can carry out general computation by itself, which ties the class to the [format string vulnerability](/format-string-vulnerability/).
- **The shadow stack as the needed addition.** With a shadow stack added, arbitrary code execution was removed in three of the six programs. The lesson that CFI needs a backward-edge check is why hardware CFI now pairs forward-edge marks with a hardware [shadow stack](/shadow-stack/).
- **Object-oriented code.** Later work on C++ programs built attacks from chains of allowed virtual calls, which showed that forward-edge policies must use the class hierarchy and not only function types; see [class hierarchy analysis](/class-hierarchy-analysis/).

## Variations

- **Bending at forward edges.** The attacker changes a function pointer to another allowed target of the same site. Type-based policies allow every function of the matching type, which can be many.
- **Bending at returns.** The attacker changes a return address to another caller of the same function. Only a shadow stack, or a policy with context, stops it.
- **Imprecise analysis.** If the [points-to analysis](/points-to-analysis/) that builds the allowed sets is imprecise, the sets grow, and the class becomes easier. Attacks have used exactly this gap between fully precise and practical policies.
- **Data only.** If the attacker needs no change of control flow at all, the class becomes [data-oriented programming](/data-oriented-programming/), which no control-flow defense sees.

## Pitfalls

These are mistakes defenders make about the class.

- **Measuring CFI by the average size of allowed sets.** The paper argues that common metrics fail to show security. One site with a powerful allowed target can be enough. Evaluate a policy against the attacks it must stop.
- **CFI without a shadow stack.** Static return policies give each function as many return targets as callers. Deploy a [shadow stack](/shadow-stack/) with any CFI.
- **Leaving powerful functions unguarded.** Copy and formatting routines with arguments from attacker-reachable memory are the building blocks of line L5. Bounds-checked versions, a constant format argument, and [code-pointer integrity](/code-pointer-integrity/) reduce the risk.
- **Treating control flow as the whole story.** If the memory error remains, the attacker can change data. Only defenses of line L1 end the class.

## Exercises

1. In the abstract model of line L4, a function $D$ has $m$ callers. Under a static policy, how many return targets does a corrupted return of $D$ have? Under a shadow stack? Prove the second answer with the theorem on the [shadow stack](/shadow-stack/) page.
2. Explain why the CFI theorem of [control-flow integrity](/control-flow-integrity/), which says that every transfer from $s$ goes to a target in $T^*(s)$, is not contradicted by the existence of CFB attacks.
3. A site may call any function of one type, and the program has $k$ functions of that type. Another policy uses the results of a points-to analysis and allows $j \le k$ of them. Which line of the template does the second policy improve, and why can it not remove line L5?
4. For each line L1 to L6 of the template, name one defense that breaks it and say whether it protects control flow or data.

## References
