---
tag: DQHM28
kind: definition
slug: noninterference
name: Noninterference
aliases:
- secure information flow
area: compilers-and-program-analysis/verification-and-synthesis
level: advanced
summary: A program is noninterfering if its public outputs do not depend on its secret inputs, a property checked by type systems or analysis.
prereqs: [hoare-triple, safety-property]
see_also: [self-composition, taint-analysis, type-system, type-soundness, timing-attack, equivalence-checking, liveness-property, rice-theorem]
sources:
  - paper: doi:10.1109/SP.1982.10014
    title: Joseph A. Goguen and Jose Meseguer, Security policies and security models, Proceedings of the 1982 IEEE Symposium on Security and Privacy
    locator: pp. 11 to 20, the definition of noninterference between groups of users of a system
  - paper: doi:10.1145/360051.360056
    title: Dorothy E. Denning, A lattice model of secure information flow, Communications of the ACM 19(5), 1976
    locator: pp. 236 to 243, security classes ordered in a lattice and the explicit and implicit flows of a program
  - paper: doi:10.3233/JCS-1996-42-304
    title: Dennis Volpano, Cynthia Irvine and Geoffrey Smith, A sound type system for secure flow analysis, Journal of Computer Security 4(2-3), 1996
    locator: pp. 167 to 187, the security type system for a while language and its soundness theorem, which states noninterference for typable programs
  - paper: doi:10.1109/JSAC.2002.806121
    title: Andrei Sabelfeld and Andrew C. Myers, Language-based information-flow security, IEEE Journal on Selected Areas in Communications 21(1), 2003
    locator: pp. 5 to 19, the semantic definition of noninterference, termination and timing channels, and declassification
  - paper: doi:10.1007/11547662_24
    title: Tachio Terauchi and Alex Aiken, Secure information flow as a safety problem, Proceedings of SAS 2005, LNCS 3672
    locator: the definition of 2-safety and the observation that noninterference is a 2-safety property and not a safety property
  - paper: doi:10.3233/JCS-2009-0393
    title: Michael R. Clarkson and Fred B. Schneider, Hyperproperties, Journal of Computer Security 18(6), 2010
    locator: pp. 1157 to 1210, hyperproperties as sets of trace properties, and noninterference as a hyperproperty that is not a trace property
---

Noninterference says that the public outputs of a program depend only on its public inputs: if two runs start with the same public values, they end with the same public values, whatever the secrets were. It is the standard meaning of "the program does not leak its secrets", and it covers both direct copies of a secret and leaks through the control flow. It is a property of pairs of runs, not of single runs, so one [Hoare triple](/hoare-triple/) cannot state it; it is a 2-safety property, and [self-composition](/self-composition/) turns it into an ordinary [safety property](/safety-property/). Security [type systems](/type-system/) check a stronger condition that implies it.

## Definition

**Setting.** A program $P$ in a small deterministic while language runs over integer variables. Each variable has a level: low ($L$, public) or high ($H$, secret). A state $s$ maps the variables to integers, and two states are *low-equivalent*, $s =_L t$, if they agree on every low variable. $[\![P]\!](s)$ is the final state of the run of $P$ from $s$, or $\bot$ if the run does not stop.

**Noninterference (termination-insensitive).** $P$ is *noninterfering* if for all states $s_1 =_L s_2$, whenever $[\![P]\!](s_1) = t_1 \ne \bot$ and $[\![P]\!](s_2) = t_2 \ne \bot$, then $t_1 =_L t_2$.

**Termination-sensitive noninterference** adds: $[\![P]\!](s_1) = \bot$ if and only if $[\![P]\!](s_2) = \bot$. So the secret cannot decide whether the program stops.

**More levels.** With a lattice of levels, as in Denning's model, $P$ is noninterfering if for every level $\ell$ the inputs at levels at or below $\ell$ fix the outputs at levels at or below $\ell$. The two-level case is the one above. For nondeterministic or concurrent programs the usual form is *possibilistic*: for $s_1 =_L s_2$, every final state from $s_1$ is low-equivalent to some final state from $s_2$.

**Runs and k-safety.** A *run* of $P$ is a pair $(s, t)$ with $[\![P]\!](s) = t \ne \bot$. A property of programs is a *trace property* if there is a set $\Pi$ of runs such that $P$ has the property exactly when every run of $P$ is in $\Pi$. It is a *k-safety property*, as Terauchi and Aiken call it, if there is a set $B$ of $k$-tuples of runs such that $P$ has the property exactly when no $k$ runs of $P$ form a tuple in $B$.

**Theorem.** (1) Noninterference is a 2-safety property. (2) It is not a trace property. (3) It is undecidable.

*Proof.* (1) Let $B$ be the set of pairs $((s_1, t_1), (s_2, t_2))$ with $s_1 =_L s_2$ and $t_1 \ne_L t_2$. By the definition, $P$ is noninterfering exactly when no two runs of $P$ form a pair in $B$.

(2) Suppose $\Pi$ is a set of runs that defines noninterference as a trace property. Take one low variable $l$ and one high variable $h$, and the program $P = (l := h)$. Its runs are the pairs $(s, t)$ with $t(l) = t(h) = s(h)$. Fix one run $(s, t)$ and let $c = s(h)$. The program $l := c$, for the constant $c$, is noninterfering, since its low output is always $c$. The run $(s, t)$ is one of its runs, so $(s, t) \in \Pi$. This holds for every run of $P$, so $P$ has the property. But $P$ leaks: the states with $l = 0, h = 0$ and $l = 0, h = 1$ are low-equivalent, and the outputs have $l = 0$ and $l = 1$. This contradicts the choice of $\Pi$.

(3) For a program $Q$ that does not use $l$ or $h$, let $P_Q = (Q;\ l := h)$. If $Q$ stops, then $P_Q$ leaks $h$ as in (2). If $Q$ does not stop, $P_Q$ has no runs and is noninterfering. So a decision procedure for noninterference would decide the [halting problem](/halting-problem/). This is also an instance of [Rice's theorem](/rice-theorem/). The complement is recursively enumerable, since one can search over pairs of inputs and run them. $\square$

Termination-sensitive noninterference is not a 2-safety property: a violation can need a run that does not stop, and no finite part of it shows the violation.

## Examples and non-examples

Take $l$ low and $h$ high.

| program | noninterfering? | why |
|---|---|---|
| $l := h$ | no | explicit flow: $h = 0$ and $h = 1$ give different $l$ |
| $\mathbf{if}\ h > 0\ \mathbf{then}\ l := 1\ \mathbf{else}\ l := 0$ | no | implicit flow: no assignment copies $h$, but the branch does |
| $l := h;\ l := 0$ | yes | the final $l$ is always 0 |
| $l := h - h$ | yes | the final $l$ is always 0 |
| $h := l + 1$ | yes | flow from low to high is allowed |
| $\mathbf{while}\ h > 0\ \mathbf{do}\ \mathbf{skip}$ | yes, termination-insensitive; no, termination-sensitive | the secret decides whether the program stops |
| $\mathbf{if}\ h > 0\ \mathbf{then}\ \mathit{slow}\ \mathbf{else}\ \mathbf{skip};\ l := 0$ | yes | but the time it takes leaks $h$, a [timing attack](/timing-attack/) that this definition does not model |
| $l := (h = \mathit{guess})$ | no | a password check leaks one bit; real policies allow it with declassification |

The third and fourth rows show that the definition is semantic. The flow-insensitive type system of Volpano, Irvine and Smith rejects $l := h;\ l := 0$, because $l$ receives a high value at some point, and it rejects $l := h - h$ too. Its soundness theorem says that typable programs are noninterfering; the converse fails, as it must, since the property is undecidable. A flow-sensitive analysis accepts the third row but still rejects the fourth.

A [taint analysis](/taint-analysis/) tracks explicit flows only, so it does not prove noninterference: the implicit flow in the second row passes it. A check for noninterference must also mark everything assigned under a branch on a secret.

## Related definitions

- **Safety and liveness.** Safety and [liveness](/liveness-property/) properties are trace properties. Noninterference is neither, because it compares runs. Clarkson and Schneider call such a property a hyperproperty, a set of sets of traces, and noninterference is a safety hyperproperty.
- **Self-composition.** Because noninterference is 2-safety, it holds exactly when a program that runs two renamed copies of $P$ one after the other satisfies the safety triple $\{l_1 = l_2\}\ P_1; P_2\ \{l_1 = l_2\}$. See [self-composition](/self-composition/).
- **Program equivalence.** Noninterference says that $P$ is equivalent to itself when the inputs are related by $=_L$ and the outputs are compared by $=_L$. It is a relational property, like the [equivalence](/equivalence-checking/) of a program and its compiled form in [translation validation](/translation-validation/).
- **Type soundness.** A security type system is sound when every typable program is noninterfering. This is the analog of [type soundness](/type-soundness/), but it is stated about two runs.
- **Timing and constant-time code.** If the time of a run is an output, the definition becomes "constant-time" execution, the usual defense in cryptographic code.

## References
