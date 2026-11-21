---
tag: 8ST8W9
kind: definition
slug: implicit-flow
name: Implicit flow
aliases:
- indirect flow
- control dependence flow
area: security-and-privacy/access-control-and-information-flow
level: core
summary: Flow of information from a secret condition to a variable assigned in a branch, even when the secret value is never copied.
prereqs: [denning-lattice-model, control-flow-graph]
see_also: [noninterference, security-type-system, taint-analysis, program-dependence-graph, no-sensitive-upgrade, program-slicing, covert-channel, dataflow-analysis]
sources:
  - paper: doi:10.1145/359636.359712
    title: Dorothy E. Denning and Peter J. Denning, Certification of programs for secure information flow, Communications of the ACM 20(7), 1977
    locator: "pp. 504 to 513; Section 2.2, explicit and implicit flows and the example y := 1; if x = 0 then y := 0; Section 3, the certification of if and while statements"
  - paper: doi:10.1145/360051.360056
    title: Dorothy E. Denning, A lattice model of secure information flow, Communications of the ACM 19(5), 1976
    locator: pp. 236 to 243, flows caused by the execution of conditional structures
  - paper: doi:10.1093/comjnl/17.2.143
    title: J. S. Fenton, Memoryless subsystems, The Computer Journal 17(2), 1974
    locator: pp. 143 to 147, the data mark machine and the leak through a branch that does not run
  - paper: doi:10.1109/JSAC.2002.806121
    title: Andrei Sabelfeld and Andrew C. Myers, Language-based information-flow security, IEEE Journal on Selected Areas in Communications 21(1), 2003
    locator: pp. 5 to 19, implicit flows and the program counter label in security type systems
---

An implicit flow is a flow of information from the condition of a branch or a loop to a variable that the branch assigns. No assignment copies the secret, but the value of the variable after the branch tells which way the branch went, and so tells something about the condition. Denning and Denning (1977) named the two kinds of flow, *explicit* (through an assignment) and *implicit* (through the control flow), in the [lattice model](/denning-lattice-model/). A checker that sees only explicit flows, as most [taint analyses](/taint-analysis/) do, misses implicit flows and so does not give [noninterference](/noninterference/).

## Definition

**Setting.** A program is in a small while language with assignments $x := e$, sequences, if statements and while loops. Each variable $x$ has a class $\Gamma(x)$ in a security lattice $(\mathcal{L}, \le, \sqcup, \sqcap)$, where $\ell_1 \le \ell_2$ means that information may flow from $\ell_1$ to $\ell_2$. The label of an expression, $\mathrm{label}(e)$, is the join of the classes of its variables.

**Explicit flow.** An assignment $x := e$ makes an explicit flow from each variable of $e$ to $x$.

**Implicit flow.** Let $S$ be an if statement or a while loop with condition $e$. A statement $T$ is *in the scope of* $S$ if $T$ is in a branch or in the body of $S$. Then each assignment $x := e'$ in the scope of $S$ makes an implicit flow from each variable of $e$ to $x$. The flow happens on every run that tests $e$, also on a run where the assignment does not execute: the fact that $x$ keeps its old value is itself information about $e$.

For programs with arbitrary jumps, the scope of a branch is the set of nodes that are control dependent on it in the [control flow graph](/control-flow-graph/): the nodes between the branch and its immediate post-dominator. This is the control dependence of the [program dependence graph](/program-dependence-graph/).

**The program counter class.** A checker accounts for implicit flows with a class $pc$ for the program counter. At the start $pc = \bot$. In the scope of a branch on $e$, the checker uses $pc \sqcup \mathrm{label}(e)$, and at the end of the scope it restores the old value. An assignment $x := e'$ is allowed when

$$\mathrm{label}(e') \sqcup pc \le \Gamma(x).$$

The term $\mathrm{label}(e')$ covers the explicit flow and the term $pc$ covers the implicit flows.

**Syntactic and semantic flows.** The definition above is syntactic: it says where a flow can happen. A flow from $h$ to $x$ *happens* in the semantic sense when two runs that differ only in $h$ end with different values of $x$. Each semantic flow through the control flow is a syntactic implicit flow, but not each syntactic flow is a semantic one.

## Examples and non-examples

Take $h$ high and $l$ low, in the two-point lattice $L \le H$.

- **A copy of one bit.** `if h then l := 1 else l := 0`. After the run, $l = 1$ exactly when $h \ne 0$. No assignment reads $h$, and the flow is implicit.
- **The branch that does not run.** Denning and Denning give `y := 1; if x = 0 then y := 0`. Take $x$ high and $y$ low. If $x \ne 0$ the assignment $y := 0$ does not run, but $y = 1$ still shows that $x \ne 0$. A run-time check that looks only at the assignments that run misses this flow. Fenton (1974) found the same problem in his data mark machine.

  | $x$ | runs $y := 0$? | final $y$ |
  |---|---|---|
  | 0 | yes | 0 |
  | 1 | no | 1 |
  | 2 | no | 1 |

- **A copy of a whole value.** `l := 0; while h > l do l := l + 1`, for $h \ge 0$. The loop ends with $l = h$, so the loop copies $h$ to $l$ through implicit flows only.
- **Two steps.** `if h then m := 1 else m := 0; l := m`, with $m$ low. The flow from $h$ to $m$ is implicit and the flow from $m$ to $l$ is explicit. The checker rejects the first assignment, because $pc = H$ and $\Gamma(m) = L$.
- **Non-example: a flow to a high variable.** `if h then h2 := 1`, with $h2$ high. This is an implicit flow, but it is allowed, since $H \le H$.
- **Non-example: a low condition.** `if l then h := 0 else l := 2`. The flows go from $l$ to $h$ and from $l$ to $l$, and both are allowed.
- **Syntactic but not semantic.** `if h then l := 0 else l := 0`. The definition gives an implicit flow from $h$ to $l$, but $l = 0$ after each run, so no information flows. A sound static checker still rejects this program.
- **Not an implicit flow: termination.** `while h = 0 do skip; l := 1`. The assignment to $l$ is after the loop, not in its scope. The secret decides only whether the program stops. This is a termination channel. [Termination-insensitive noninterference](/termination-insensitive-noninterference/) ignores it, and a checker in the style above accepts this program.

## Related definitions

- **[Noninterference](/noninterference/)** is the semantic property that a sound treatment of explicit and implicit flows gives. A program with no disallowed semantic flow of either kind is noninterferent.
- **[Security type system](/security-type-system/).** The implicit flow is the phenomenon. The type system of Volpano, Irvine and Smith is the algorithm that checks it with the program counter class above, and its soundness theorem shows that this check is enough for TINI.
- **[Taint analysis](/taint-analysis/)** tracks explicit flows only in most tools. It is useful to find a copy of untrusted input in a dangerous place, but it does not show that a secret stays secret.
- **Dynamic monitors.** At run time the branch that does not run is not seen. The [no-sensitive-upgrade](/no-sensitive-upgrade/) check stops the run instead, [secure multi-execution](/secure-multi-execution/) runs the program once per level, and [faceted execution](/faceted-execution/) keeps a value for each observer.
- **[Covert channels](/covert-channel/)** such as the termination and timing channels carry information through how the program runs, not through the final values. They are outside the definition above.
- **[Program slicing](/program-slicing/)** and the [program dependence graph](/program-dependence-graph/) use the same control dependence. A backward slice of $x$ contains each branch that makes an implicit flow to $x$.

## References
