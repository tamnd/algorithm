---
tag: EYC3KG
kind: technique
slug: control-flow-integrity
name: Control-flow integrity
aliases:
- CFI
area: security-and-privacy/memory-safety-defenses
level: core
summary: Checks at each indirect branch that the target is allowed by a control flow graph computed in advance, so hijacked flow stops.
history:
  year: 2005
  people: [Martin Abadi, Mihai Budiu, Ulfar Erlingsson, Jay Ligatti]
  note: Abadi et al. (CCS 2005) defined CFI, proved its guarantee under three assumptions, and built it by binary rewriting on x86. Compilers and processors later shipped coarser forms.
prereqs: [control-flow-graph, return-oriented-programming]
see_also: [shadow-stack, control-flow-bending, code-pointer-integrity, points-to-analysis, class-hierarchy-analysis, disjoint-set, inline-reference-monitor, software-fault-isolation]
sources:
  - paper: doi:10.1145/1102120.1102165
    title: Martin Abadi, Mihai Budiu, Ulfar Erlingsson and Jay Ligatti, Control-flow integrity, CCS 2005, pages 340-353
    locator: the definition of CFI, the label instrumentation, and the assumptions of unique labels, non-writable code and non-executable data
  - paper: doi:10.1145/1609956.1609960
    title: Martin Abadi, Mihai Budiu, Ulfar Erlingsson and Jay Ligatti, Control-flow integrity, principles, implementations, and applications, ACM Transactions on Information and System Security 13(1), article 4, 2009, pages 1-40
    locator: the formal model and the proof of the guarantee, the loss of precision from shared labels, and the measured overhead on SPEC benchmarks with and without a protected shadow call stack
  - paper: doi:10.1145/3054924
    title: Nathan Burow, Scott A. Carr, Joseph Nash, Per Larsen, Michael Franz, Stefan Brunthaler and Mathias Payer, Control-flow integrity, precision, security, and performance, ACM Computing Surveys 50(1), article 16, 2017, pages 1-33
    locator: the classification of CFI designs by the precision of the forward and backward edges, and the comparison of their security and cost
  - paper: "Nicholas Carlini, Antonio Barresi, Mathias Payer, David Wagner and Thomas R. Gross, Control-flow bending, on the effectiveness of control-flow integrity, 24th USENIX Security Symposium, 2015, pages 161-176"
    locator: the results under fully precise static CFI with and without a shadow stack
---

Control-flow integrity (CFI) is a defense that fixes, before the program runs, the set of targets each indirect branch may go to, and checks at run time that every indirect call, jump and return goes to one of them. The allowed sets come from a [control flow graph](/control-flow-graph/) that a compiler or a binary analysis builds: direct branches are fixed in the code, and for each indirect branch site $s$ the analysis gives a set $T(s)$ of allowed targets, using [points-to analysis](/points-to-analysis/) or types for calls through pointers and the [call graph](/call-graph/) for returns. A memory error can still change a code pointer or a return address, but if the new target is not in $T(s)$, the check stops the program before the branch. So code reuse in the style of [return-oriented programming](/return-oriented-programming/), which jumps into the middle of functions, fails. Abadi, Budiu, Erlingsson and Ligatti (CCS 2005) defined CFI and proved its guarantee under three assumptions: code cannot be written, data cannot run, and the labels that mark valid targets appear nowhere else. The guarantee is exactly as strong as the graph is precise. A coarse graph leaves many allowed targets, and even a fully precise static graph leaves enough for general attacks when returns are not checked by a [shadow stack](/shadow-stack/), as [control-flow bending](/control-flow-bending/) showed in 2015.

## In plain words

A program has a map of the ways it can move from one piece of code to another. Most moves are fixed in the code itself. A few are decided while the program runs: a call through a function pointer, or a return that reads its address from the stack. An attacker who changes those addresses changes where the program goes.

CFI writes down, before the program runs, the allowed destinations of each such move. Then it adds a small check before each move. If the destination is not on the list, the program stops.

The checks are only as good as the lists. If a list allows almost every function, the attacker can still choose among many. And for returns the list says "any place that calls this function", not "the place that called it this time", which is why CFI is paired with a shadow stack.

## When it applies

- **The threat is control-flow hijacking**: an attacker can change code pointers or return addresses in writable memory, through a [buffer overflow](/buffer-overflow/) or another memory error, but cannot change code.
- **Data execution prevention holds.** Code pages are not writable and data pages are not executable, as [data execution prevention](/data-execution-prevention/) provides. These are two of the three assumptions of the guarantee.
- **A control flow graph can be built.** The compiler has the source, or a binary analysis can find the functions and their indirect branches. The precision of the policy depends on how well the analysis resolves function pointers and virtual calls ([class hierarchy analysis](/class-hierarchy-analysis/), types, [points-to analysis](/points-to-analysis/)).
- **The whole program is instrumented.** Every module, including the libraries, must be built or rewritten with checks, or an unchecked module offers free targets.

## The template

The defense has a build phase that turns the allowed graph into labels, and a check before each indirect transfer. The named holes are the choices of each system. The build below gives one label to each connected component of the bipartite graph between sites and targets, which is the labeling of Abadi et al.

```pseudo id=main
BUILD-LABELS(allowed sets T(s) for each indirect branch site s)
L1  E ← the edges (s, t) with t ∈ T(s), from ⟨graph analysis⟩
L2  for each (s, t) in E do UNION(s, t)                          ▷ union-find over sites and targets
L3  give one label to each union-find class                      ▷ ⟨label encoding⟩ in code
L4  at each target t, place label(t) in non-writable code
L5  at each site s, store expected(s) ← label of the class of s

CHECK(s, x)                                                       ▷ inserted before the branch at s, with run-time target x
L6  if x carries no label or label(x) ≠ expected(s) then fault "CFI violation"
L7  branch to x
```

**Walk-through.** Line L1 is the analysis, which decides precision. Line L2 merges a site with every target it may reach, using a [disjoint set](/disjoint-set/) structure. If two sites share one target, their whole target sets merge, because one target can carry only one label. Line L3 assigns the labels, and lines L4 and L5 place them: at each target, a label that the check can read from the code, and at each site, the label it expects. Line L6 is the run-time check, a load and a compare. Line L7 is the original branch.

**Correctness.** Let $T^*(s)$ be the set of targets in the connected component of $s$ in the bipartite graph of line L1. Under the three assumptions, a transfer from $s$ to $x$ passes line L6 if and only if $x \in T^*(s)$. Two consequences follow. First, $T(s) \subseteq T^*(s)$, so a run that follows the graph never faults. Second, if any two allowed sets are equal or disjoint, then $T^*(s) = T(s)$, so the check is exactly the policy. When sets overlap without being equal, the check accepts more than the policy, and no labeling with one label per target can do better. The full proofs are in [the proof file](proofs/correctness.md).

**Example.** Take three sites with $T(s_1) = \{f, g\}$, $T(s_2) = \{g, h\}$ and $T(s_3) = \{k\}$. Line L2 joins $s_1$, $f$ and $g$, then $s_2$ and $h$ through $g$, so there are two classes: $\{s_1, s_2, f, g, h\}$ and $\{s_3, k\}$. Now run the transfers $(s_1, g)$, $(s_2, h)$, $(s_1, h)$, $(s_3, f)$. The first two follow the graph and pass. The third is not in $T(s_1)$, but $h$ carries the label of $s_1$'s class, so it passes: this is the loss of precision from the shared target $g$. The fourth fails at line L6, because $f$ carries the first label and $s_3$ expects the second.

**Cost.** The build takes $O((V + E)\,\alpha(V))$ time in the [word RAM](/word-ram/) model for $V$ sites and targets and $E$ allowed edges, and each check takes $O(1)$. Measured overhead is a different matter. Abadi et al. report an average of 16 percent on SPEC benchmarks for their binary rewriter, with a range of 0 to 45 percent, and 21 percent on average with a protected shadow call stack added (TISSEC 2009). Compiler-based designs since then are cheaper; Burow et al. (2017) compare them.

**Code.** The Python file `impl/python/control_flow_integrity.py` builds the labels of lines L1 to L5 from an allowed graph with a union-find, checks transfers at lines L6 and L7, and runs a sequence of abstract transfers. It works on names of sites and targets only, with no machine code. The tests compare the accepted sets with the connected components found by [breadth-first search](/breadth-first-search/) on 700 random graphs.

## Classic examples

- **The original design (2005).** Abadi et al. rewrote x86 binaries with labels in the code, checked every indirect call, jump and return, and paired the checks with a protected shadow call stack for exact returns. Their guarantee needs non-writable code, non-executable data and unique labels.
- **Stopping [return-oriented programming](/return-oriented-programming/).** Sequences used by ROP mostly start in the middle of functions or of instructions. None of these places carry a label, so the first transfer to one fails at line L6.
- **Coarse CFI in practice.** Several deployed forms allow any indirect call to reach any function entry that has been marked, and any return to reach any instruction after a call. They are cheap and need no precise analysis, but research in 2014 built general attacks inside such policies. The forward-edge marks of recent processors are of this coarse kind and are meant to be combined with a hardware [shadow stack](/shadow-stack/).
- **[Control-flow bending](/control-flow-bending/) (2015).** Carlini et al. assumed fully precise static CFI, the most restrictive static policy that does not break the program, and still found powerful attacks in five of six real programs, through functions that are allowed targets and that themselves take pointers, such as copy and formatted output functions. A shadow stack added to CFI removed arbitrary code execution in three of the six.
- **[Code-pointer integrity](/code-pointer-integrity/).** CPI takes another path: it protects the code pointers themselves, so that their values stay correct, rather than checking their targets against a graph.

## Variations

- **Forward edges and backward edges.** Indirect calls and jumps (forward edges) are checked against sets from types or points-to analysis. Returns (backward edges) are better checked by a [shadow stack](/shadow-stack/), which requires the matching call site rather than any call site.
- **Type-based sets.** A compiler can allow an indirect call to reach only functions whose type matches the type of the pointer, and a virtual call to reach only the methods of the class hierarchy of the static type. This is cheap and common; its precision depends on how many functions share a type.
- **More than one label per target.** To avoid the merge of line L2, a system can give a target several labels, test the target against a set, or duplicate code. The optimality theorem in the proof file shows that one label per target cannot avoid the loss.
- **Dynamic and context-sensitive CFI.** Some designs narrow the allowed set at run time, using the history of the path or the points-to facts that hold at this moment. They come closer to the ideal of one allowed target, at a higher cost.
- **Hardware support.** Instruction set extensions mark valid targets of indirect branches and check them in the processor, at little cost, with a coarse policy. Their value comes from the combination with a hardware shadow stack.
- **Relation to inline monitors.** CFI is an [inline reference monitor](/inline-reference-monitor/) for a safety policy on control flow, and it is the base that lets [software fault isolation](/software-fault-isolation/) keep its checks from being skipped.

## Pitfalls

- **Coarse policies.** A policy that allows every function or every call-preceded instruction leaves enough targets for general computation. Report the size of the allowed sets, not only that CFI is on.
- **Returns without a shadow stack.** A static policy allows a function to return to any of its callers. The return of a function called from many places can then go to any of them, which [control-flow bending](/control-flow-bending/) uses.
- **Missing the assumptions.** If code is writable, the attacker changes the check or the labels. If data can run, the attacker writes a jump with no check. If a label's bit pattern appears elsewhere, that place becomes a target. Each of these voids the theorem.
- **Uninstrumented modules.** A library built without CFI, or code generated at run time without checks, gives free targets.
- **Data-only attacks.** CFI says nothing about the data the program uses. An attacker who changes a decision variable or the arguments of an allowed call stays inside the graph; see [data-oriented programming](/data-oriented-programming/).

## Exercises

1. Run the build of the template on $T(s_1) = \{a\}$, $T(s_2) = \{a, b\}$, $T(s_3) = \{b, c\}$, $T(s_4) = \{d\}$. List the classes and the effective sets $T^*(s)$, and give one transfer that the policy forbids but the check accepts.
2. Prove that if each target belongs to at most one allowed set, then $T^*(s) = T(s)$ for every site. Is the converse true?
3. A function $F$ is called from $m$ call sites. Under a static CFI policy for returns, how many targets does a return of $F$ have? How many does a [shadow stack](/shadow-stack/) allow?
4. Explain, with the three assumptions of the guarantee, why an attacker who can write one byte of a code page can defeat a check at line L6.

## References
