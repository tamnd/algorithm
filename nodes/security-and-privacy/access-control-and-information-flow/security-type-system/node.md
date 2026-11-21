---
tag: 8RQ898
kind: algorithm
slug: security-type-system
name: Volpano-Smith-Irvine type system
aliases:
- security type system
- VSI type system
area: security-and-privacy/access-control-and-information-flow
level: core
summary: A type system that labels variables with security levels and the program counter with a level, and whose well-typed programs are termination-insensitive noninterferent.
model: word-ram
complexity:
  vars: {n: the number of nodes of the syntax tree of the program}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: false, sound: true, complete: false}
history:
  year: 1996
  people: [Dennis Volpano, Cynthia Irvine, Geoffrey Smith]
  note: Volpano, Irvine and Smith gave the type system and its soundness proof in the Journal of Computer Security in 1996. It recasts the certification of Denning and Denning (1977).
prereqs: [implicit-flow, noninterference, type-system]
see_also: [termination-insensitive-noninterference, type-soundness, taint-analysis, no-sensitive-upgrade, secure-multi-execution, self-composition, declassification, decentralized-label-model]
sources:
  - paper: doi:10.3233/JCS-1996-42-304
    title: Dennis Volpano, Cynthia Irvine and Geoffrey Smith, A sound type system for secure flow analysis, Journal of Computer Security 4(2-3), 1996
    locator: pp. 167 to 187, the typing rules for a while language and the soundness theorem
  - paper: doi:10.1145/359636.359712
    title: Dorothy E. Denning and Peter J. Denning, Certification of programs for secure information flow, Communications of the ACM 20(7), 1977
    locator: pp. 504 to 513, Section 3, the certification mechanism that the type system recasts
  - paper: doi:10.1109/JSAC.2002.806121
    title: Andrei Sabelfeld and Andrew C. Myers, Language-based information-flow security, IEEE Journal on Selected Areas in Communications 21(1), 2003
    locator: pp. 5 to 19, the type system in program counter form and its extensions
  - paper: doi:10.1007/978-3-540-88313-5_22
    title: Aslan Askarov, Sebastian Hunt, Andrei Sabelfeld and David Sands, Termination-insensitive noninterference leaks more than just a bit, ESORICS 2008, LNCS 5283
    locator: pp. 333 to 348, Section 3 (a Denning-style type system with output, Fig. 3, and Theorem 1, typable programs are TINI)
  - paper: doi:10.1109/CSFW.1997.596807
    title: Dennis Volpano and Geoffrey Smith, Eliminating covert flows with minimum typings, Proceedings of the 10th IEEE Computer Security Foundations Workshop, 1997
    locator: pp. 156 to 168, the restriction of loop conditions that closes the termination channel
---

The Volpano-Smith-Irvine type system checks a program for secure information flow before it runs. Each variable has a security level, and the checker keeps a level $pc$ for the program counter, so that it sees both the explicit flows of assignments and the [implicit flows](/implicit-flow/) of branches. The checker is a single pass over the syntax tree and takes linear time. Its soundness theorem says that a well-typed program is termination-insensitive noninterferent ([TINI](/termination-insensitive-noninterference/)): the public outputs of two runs that both stop do not depend on the secrets. This is the [type system](/type-system/) view of the certification of Denning and Denning, and the base of languages such as Jif.

## In plain words

Each variable is public or secret. The checker reads the program and asks one question at each assignment: can secret data reach this variable here? Secret data can arrive in two ways. The assigned expression can read a secret variable. Or the assignment can be inside an if or a while whose condition reads a secret, because then the fact that the assignment ran tells something about the secret. The checker keeps a "context level" for the second way. It is public at the start, it becomes secret inside a branch on a secret, and it goes back when the branch ends. An assignment to a public variable is an error when the expression or the context is secret. If no assignment is an error, the program cannot leak its secrets through its final public values, provided it stops.

## The problem

The input is a program $c$ in a small while language (assignments $x := e$, sequences, if statements and while loops), a security lattice $(\mathcal{L}, \le, \sqcup, \sqcap)$ in which $\ell_1 \le \ell_2$ means that information may flow from $\ell_1$ to $\ell_2$, a level $\Gamma(x)$ for each variable, and a start level $pc$ (usually $\bot$). The output is true when $pc \vdash c$ holds in the rules below, and false otherwise. Here $\mathrm{label}(e)$ is the join of $\Gamma(y)$ over the variables $y$ of $e$.

- $x := e$ is typable at $p$ if $\mathrm{label}(e) \sqcup p \le \Gamma(x)$.
- $c_1; c_2$ is typable at $p$ if both parts are typable at $p$.
- if $e$ then $c_1$ else $c_2$ is typable at $p$ if both branches are typable at $p \sqcup \mathrm{label}(e)$.
- while $e$ do $c_1$ is typable at $p$ if $c_1$ is typable at $p \sqcup \mathrm{label}(e)$.

The goal of the type system is the semantic property [noninterference](/noninterference/), in its termination-insensitive form.

## The algorithm

The checker walks the syntax tree with an explicit stack of pairs (command, level of the program counter), so that a deep program does not overflow a call stack.

```pseudo id=main
TYPECHECK(c, Γ, pc)                        ▷ true if pc ⊢ c
L1  S ← a stack that holds the pair (c, pc)
L2  while S is not empty do
L3      (d, p) ← pop(S)
L4      if d = skip then continue
L5      if d = (x := e) then
L6          if label(e) ⊔ p ≰ Γ(x) then return false
L7      if d = (d1; d2) then push (d2, p), then (d1, p)
L8      if d = (if e then d1 else d2) then
L9          q ← p ⊔ label(e); push (d2, q), then (d1, q)
L10     if d = (while e do d1) then push (d1, p ⊔ label(e))
L11 return true
```

Line L6 is the only test. The term $\mathrm{label}(e)$ catches explicit flows and the term $p$ catches implicit flows. Lines L9 and L10 raise the program counter level for the commands inside a branch or a loop on $e$. The level is part of each stack entry, so it goes back to the old value for the command after the branch: line L7 gives $d_2$ the level $p$ of the sequence, not the level of a branch inside $d_1$. The loop condition can be secret; line L10 accepts this, and this is the reason the result is TINI and not termination-sensitive.

## Example

Take the two-point lattice $L \le H$, $\Gamma(l) = \Gamma(m) = L$, $\Gamma(h) = H$ and the program

$$c = (l := l + 1);\ (\mathtt{if}\ h\ \mathtt{then}\ h := l\ \mathtt{else}\ \mathtt{skip});\ (m := h)$$

parsed as $c_1; (c_2; c_3)$. The stack is listed with its top at the right.

| step | popped $(d, p)$ | check or action | stack after the step |
|---|---|---|---|
| 1 | $(c, L)$ | sequence | $(c_2; c_3, L), (c_1, L)$ |
| 2 | $(l := l + 1, L)$ | $L \sqcup L \le L$, true | $(c_2; c_3, L)$ |
| 3 | $(c_2; c_3, L)$ | sequence | $(c_3, L), (c_2, L)$ |
| 4 | $(c_2, L)$ | if on $h$, $q = H$ | $(c_3, L), (\mathtt{skip}, H), (h := l, H)$ |
| 5 | $(h := l, H)$ | $L \sqcup H \le H$, true | $(c_3, L), (\mathtt{skip}, H)$ |
| 6 | $(\mathtt{skip}, H)$ | nothing | $(c_3, L)$ |
| 7 | $(m := h, L)$ | $H \sqcup L \le L$, false | return false |

At step 7 the level of the program counter is $L$ again, so the program would be typable if the last command were $m := l$. The flow from $h$ to $m$ is explicit and real, and the checker rejects the program.

## Correctness

There are two claims, both proved in full below.

1. **The checker decides typability.** TYPECHECK$(c, \Gamma, pc)$ returns true if and only if $pc \vdash c$. The invariant of line L2 is: $pc \vdash c$ holds if and only if $p \vdash d$ holds for every pair $(d, p)$ on the stack. The rules are syntax directed, so each pop replaces a pair by exactly the premises of its rule, or finds a false side condition.
2. **Soundness (Volpano, Irvine and Smith 1996).** *Hypotheses:* the deterministic while language above, with integer variables and no output during the run, and an observer who sees the final values of the variables at levels at or below $\ell$. *Statement:* if $\bot \vdash c$, then for all stores $s_1 =_\ell s_2$, if both runs of $c$ stop, the final stores are $\ell$-equivalent. The proof uses three lemmas: an expression of level at most $\ell$ has the same value in $\ell$-equivalent stores; a command typable at $p$ changes only variables $x$ with $p \le \Gamma(x)$ (confinement); and an induction on the two runs. The theorem says nothing about runs that do not stop, and nothing about time.

The same theorem holds for a language with output statements, when an output to a public channel needs a public expression and a public program counter. This is Theorem 1 of Askarov, Hunt, Sabelfeld and Sands (2008). Their later theorems show how much such a TINI program can still leak through termination; see [TINI](/termination-insensitive-noninterference/).

## Complexity

The model is the [word-RAM](/word-ram/). Let $n$ be the number of nodes of the syntax tree. Each command node is pushed and popped at most once (proof, Part 1), and each expression is read once, by line L6, L9 or L10. So the checker performs $\Theta(n)$ joins and comparisons of levels. For a fixed finite lattice, or for a lattice of subsets of at most $w$ categories stored as one machine word, each join and comparison takes $O(1)$ time, so the time is $\Theta(n)$ in each case. The stack holds at most one entry for each node of the tree, so the extra space is $O(n)$.

## Properties

- **Sound for TINI.** Each accepted program is TINI (Correctness, claim 2).
- **Not complete.** The program $l := h - h$ always stores 0 and is secure, but line L6 rejects it, because $\mathrm{label}(h - h) = H$. The program "if $h$ then $l := 0$ else $l := 0$" is also secure and rejected. No sound checker is complete, because noninterference is undecidable.
- **Flow-insensitive.** $\Gamma(x)$ is fixed for the whole program. The program $l := h;\ l := 0$ is secure but is rejected.
- **Compositional.** A sequence is typable when its parts are typable at the same level, so a library can be checked one procedure at a time.
- **Static.** The checker never runs the program. It needs no secret input and adds no cost at run time.

## Variants and improvements

- **Termination-sensitive typing.** Volpano and Smith (1997) close the termination channel by restricting loops. In the simplest form, line L10 also requires $p \sqcup \mathrm{label}(e) = \bot$: a loop is accepted only with a public condition and outside every secret branch. Then low-equivalent stores give the same termination behaviour, and a typable program is termination-sensitive noninterferent. This rejects many useful loops.
- **The original form.** Volpano, Irvine and Smith write the types as "$\tau$ var" for a variable and "$\tau$ cmd" for a command, where a command of type $\tau$ cmd assigns only to variables of level at least $\tau$. A branch on $e$ is typable when $\mathrm{label}(e) \le \tau$ for the types of its arms. This is equivalent to the program counter form; the tests of the code check both forms against each other.
- **Output channels.** Add an output statement that is typable only when the expression and the program counter are public. This is the system of Askarov et al. (2008).
- **Flow-sensitive types.** Let the level of a variable change from one program point to the next, so that $l := h;\ l := 0$ is accepted. The dynamic analogue is [no-sensitive-upgrade](/no-sensitive-upgrade/).
- **Declassification.** Add a construct that lowers the level of an expression on purpose; see [declassification](/declassification/). Jif, the language of the [decentralized label model](/decentralized-label-model/), combines such a construct with labels of several owners.
- **Relational verification.** [Self-composition](/self-composition/) proves noninterference of a program that the type system rejects, at the price of a full program proof.

## When to use it

Use the type system when the program is known before it runs and you want a guarantee for all inputs at no cost at run time. It is the standard choice in a language designed for information flow. Use a dynamic monitor when the program is known only at run time, for example a script on a web page: [no-sensitive-upgrade](/no-sensitive-upgrade/) stops the run on a possible leak, [secure multi-execution](/secure-multi-execution/) runs the program once per level, and [faceted execution](/faceted-execution/) runs it once on values with a facet per level. Use [taint analysis](/taint-analysis/) when you only need to find explicit copies of untrusted data; it tracks explicit flows only in most tools and gives no noninterference guarantee. If the program must leak through termination or time, the type system does not help; see [TINI](/termination-insensitive-noninterference/) and [constant-time verification](/constant-time-verification/).

## Pitfalls

- **No program counter at line L6.** The test $\mathrm{label}(e) \le \Gamma(x)$ without $p$ accepts "if $h$ then $l := 1$ else $l := 0$", which copies a bit of $h$ to $l$. The right test is $\mathrm{label}(e) \sqcup p \le \Gamma(x)$.
- **A global program counter.** If line L9 raises one shared variable $pc$ and never lowers it, every assignment after the first secret branch is checked at $H$, and the program "if $h$ then $h := 0$ else skip; $l := 1$" is rejected. If the variable is lowered too early, before the second branch $d_2$ is checked, the checker becomes unsound. Keep the level in each stack entry, as in lines L7 and L9.
- **The plain level at line L10.** Pushing $(d_1, p)$ instead of $(d_1, p \sqcup \mathrm{label}(e))$ accepts "while $h > l$ do $l := l + 1$", which copies $h$ to $l$.
- **Reading the theorem as termination-sensitive.** Line L10 accepts "while $h = 0$ do skip; $l := 1$". Whether this program stops depends on $h$. With public output, a typable program can reveal a whole secret of $N$ binary digits through termination, although it needs time exponential in $N$ (Askarov et al. 2008). Use the termination-sensitive variant if this matters.

## Implementations

## History

Denning and Denning (1977) gave a certification mechanism for secure flow and proved that a certified program is secure in the sense of the [lattice model](/denning-lattice-model/). Volpano, Irvine and Smith (1996) wrote the mechanism as a type system and proved soundness with respect to a semantic noninterference property, which made the guarantee precise: it covers runs that stop and does not cover termination or time. Volpano and Smith (1997) gave the version that closes the termination channel. The survey of Sabelfeld and Myers (2003) presents the program counter form used on this page and many later extensions, such as declassification, concurrency and the Jif and FlowCaml languages.

## References
