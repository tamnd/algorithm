---
tag: 5EGZEC
kind: algorithm
slug: secure-multi-execution
name: Secure multi-execution
aliases:
- SME
area: security-and-privacy/access-control-and-information-flow
level: research
summary: Runs a program once per security level and gives each run only the inputs it may see. This gives termination-sensitive noninterference and keeps each ending run of a TSNI program.
model: word-ram
complexity:
  vars: {k: the number of distinct levels of the variables, t: the largest number of steps of one copy, n: the number of nodes of the syntax tree of the program, v: the number of variables}
  time: {worst: O(k (t n + v))}
  space: {extra: O(k v + n)}
properties: {deterministic: true, recursive: false, online: false, sound: true, complete: true}
history:
  year: 2010
  people: [Dominique Devriese, Frank Piessens]
  note: Devriese and Piessens gave secure multi-execution and proved it sound and precise at the IEEE Symposium on Security and Privacy in 2010. Capizzi et al. (2008) had used a public and a private copy of a run in shadow executions.
prereqs: [noninterference, termination-insensitive-noninterference, implicit-flow]
see_also: [no-sensitive-upgrade, faceted-execution, security-type-system, self-composition, hyperproperty, covert-channel, declassification, denning-lattice-model]
sources:
  - paper: doi:10.1109/SP.2010.15
    title: Dominique Devriese and Frank Piessens, Noninterference through secure multi-execution, Proceedings of the 2010 IEEE Symposium on Security and Privacy
    locator: pp. 109 to 124, the construction, the soundness theorem (Theorem 1) and the precision theorem for termination-sensitive noninterferent programs (Theorem 2)
  - paper: doi:10.1109/ACSAC.2008.50
    title: Roberto Capizzi, Antonio Longo, V. N. Venkatakrishnan and A. Prasad Sistla, Preventing information leaks through shadow executions, Proceedings of the 2008 Annual Computer Security Applications Conference (ACSAC)
    locator: pp. 322 to 331, a public and a private copy of a process
  - paper: doi:10.1145/2382196.2382275
    title: Willem De Groef, Dominique Devriese, Nick Nikiforakis and Frank Piessens, FlowFox, a web browser with flexible and precise information flow control, Proceedings of the 2012 ACM Conference on Computer and Communications Security
    locator: pp. 748 to 759, secure multi-execution of JavaScript in a browser
  - paper: doi:10.1007/978-3-319-45744-4_25
    title: Nataliia Bielova and Tamara Rezk, Spot the difference, secure multi-execution and multiple facets, ESORICS 2016, LNCS 9878
    locator: pp. 501 to 519, the comparison of secure multi-execution with faceted execution
  - paper: doi:10.1007/978-3-540-88313-5_22
    title: Aslan Askarov, Sebastian Hunt, Andrei Sabelfeld and David Sands, Termination-insensitive noninterference leaks more than just a bit, ESORICS 2008, LNCS 5283
    locator: pp. 333 to 348, the leak through termination that termination-insensitive methods allow and secure multi-execution closes
---

Secure multi-execution (SME) enforces [noninterference](/noninterference/) by running the program several times, once for each security level. The copy at level $k$ gets the true value of each input that $k$ may see and a fixed default value for every other input, and only this copy may produce the outputs of level $k$. So a public output is computed from public inputs only, whatever the program does. Devriese and Piessens (2010) proved that SME is termination-sensitive noninterferent (TSNI) for every program, and that it does not change the ending runs of a program that is already TSNI. The price is one run for each level.

## In plain words

Suppose a program reads a secret and a public number and writes a public result. You cannot know if the program leaks the secret into the result. So you do not ask. You run the program twice. The first copy gets the public number and a fake secret, for example 0, and you take only its public result. The second copy gets the real inputs, and you take only its secret results. The public result cannot depend on the real secret, because the copy that made it never saw the secret. If the program does not leak, both copies agree on everything public, and you lose nothing. If it leaks, the public result is the one computed from the fake secret. The cost is that you run the program once for each level.

## The problem

The input is a program $c$ in a small while language, a security lattice $(\mathcal{L}, \le, \sqcup, \sqcap)$ in which $\ell_1 \le \ell_2$ means that information may flow from $\ell_1$ to $\ell_2$, a level $\Gamma(x)$ for each variable, an initial store $s$ and a default value $d$. The initial values are the inputs and the final values are the outputs; the output on $x$ is visible to an observer at level $\ell$ if $\Gamma(x) \le \ell$. Write $[\![c]\!](s)$ for the final store of the plain run, or $\bot$ if it does not end.

The output is a value or "no output" for each variable, such that:

- **Soundness.** For each level $\ell$ and each two stores that agree on the inputs of level at most $\ell$, the observer at $\ell$ sees the same outputs, including the same "no output".
- **Precision.** If $c$ is TSNI and the plain run ends, the outputs are those of the plain run.

TSNI is defined on the page [TINI](/termination-insensitive-noninterference/).

## The algorithm

```pseudo id=main
SME(c, s, Γ, d)                            ▷ an output or ⊥ for each variable
L1  K ← the levels Γ(x), each level after the levels below it
L2  for each k in K do
L3      s_k ← the store with s_k(x) = s(x) if Γ(x) ≤ k, and d otherwise
L4      t_k ← the plain run of c from s_k   ▷ ⊥ if it does not end
L5  for each variable x do
L6      t ← t_Γ(x)
L7      out(x) ← ⊥ if t = ⊥, and t(x) otherwise
L8  return out
```

Line L3 is the whole defense. The copy at level $k$ cannot read an input above $k$, because it has the default value in its place. Line L6 takes each output from the copy of its own level, and no other copy may produce it. No line of the algorithm looks at the program or its labels during the run, so explicit flows, [implicit flows](/implicit-flow/) and flows through termination are all cut in the same way. Line L1 runs the lower copies first, so that a higher copy that does not end cannot delay a lower one. The copies are independent, and they can also run at the same time.

## Example

Take the diamond lattice $\bot \le A, B \le A \sqcup B$, with $\Gamma(x) = \bot$, $\Gamma(y) = A$, $\Gamma(z) = B$, $\Gamma(w) = A \sqcup B$, the default value $d = 0$, the initial store $(x, y, z, w) = (1, 2, 3, 4)$ and the program

$$y := y + z;\ w := y + z;\ x := w.$$

The program is not secure: it copies $z$ into $y$, although $A$ and $B$ are not comparable, and it copies $w$ into the public $x$.

| copy $k$ | input $(x, y, z, w)$ | final $(x, y, z, w)$ | output taken |
|---|---|---|---|
| $\bot$ | $(1, 0, 0, 0)$ | $(0, 0, 0, 0)$ | $x = 0$ |
| $A$ | $(1, 2, 0, 0)$ | $(2, 2, 0, 2)$ | $y = 2$ |
| $B$ | $(1, 0, 3, 0)$ | $(6, 3, 3, 6)$ | $z = 3$ |
| $A \sqcup B$ | $(1, 2, 3, 4)$ | $(8, 5, 3, 8)$ | $w = 8$ |

SME gives $(x, y, z, w) = (0, 2, 3, 8)$. The plain run is the last copy and gives $(8, 5, 3, 8)$. The public $x$ is now 0 for every value of $y$, $z$ and $w$, and $y$ no longer depends on $z$. The top output $w$ is unchanged, because the top copy sees all inputs.

## Correctness

The proof below shows two theorems for the batch form on this page, where the inputs are the initial store and the outputs are the final store.

**Theorem 1 (soundness).** *Hypotheses:* the plain semantics is deterministic. *Statement:* for every program $c$, every level $\ell$ and every two stores $s, s'$ that agree on each input of level at most $\ell$, the outputs of SME of level at most $\ell$ are equal, and either both are "no output" or both are the same value. The reason: an output $x$ with $\Gamma(x) = k \le \ell$ comes from the copy at $k$, whose input by line L3 is the same for $s$ and $s'$.

**Theorem 2 (precision).** *Hypotheses:* $c$ is TSNI at each level. *Statement:* if the plain run from $s$ ends in $t$, SME gives $t$. The reason: $s$ and $s_k$ agree on the inputs of level at most $k$, so by TSNI the copy at $k$ ends and agrees with $t$ on each variable of level $k$.

These are Theorems 1 and 2 of Devriese and Piessens, who prove them for programs with input and output channels during the run. The hypothesis of Theorem 2 cannot be weakened to TINI (Pitfalls).

## Complexity

The model is the [word-RAM](/word-ram/). Let $k$ be the number of distinct levels in $\Gamma$, $t$ the largest number of steps of one copy, $n$ the number of nodes of the syntax tree and $v$ the number of variables. Line L3 takes $O(v)$ time for each level, and a copy of $t$ steps takes $O(t n)$ time, since each step evaluates at most one expression of size at most $n$. Line L1 sorts $k \le v$ levels. The time is $O(k (t n + v))$: about $k$ times the plain run. Only the levels that occur in $\Gamma$ need a copy, not every level of the lattice. The stores of the copies take $O(k v)$ space and the stack of one run $O(n)$, so the extra space is $O(k v + n)$. A version that keeps only the outputs of each copy needs less.

## Properties

- **Sound for TSNI.** Every program, secure or not, gives TSNI outputs (Theorem 1). This is stronger than the TINI guarantee of [no-sensitive-upgrade](/no-sensitive-upgrade/) and of the [security type system](/security-type-system/).
- **Precise for TSNI programs.** A TSNI program gives the same outputs as its plain run, also when that run does not end (Theorem 2 and the proof). There are no false alarms on such programs, and the property "complete" above means this.
- **Not transparent for TINI programs.** A TINI program that is not TSNI can lose its public outputs (Pitfalls).
- **A black box.** SME does not read the program. It needs only a way to run it and to control its inputs and outputs, so it works for any language and for code known only at run time.
- **Cost.** One run for each level, in time or in parallel hardware.

## Variants and improvements

- **Interactive programs.** In the original form, the inputs and outputs are channels with levels, read and written during the run. The copy at level $k$ reads the inputs of levels at most $k$ and gets the default value for the others, and only the copy at level $k$ writes to the outputs of level $k$. An input of a low level is read once and given to each higher copy that needs it. Devriese and Piessens also discuss the timing channel and the choice of a scheduler for the copies; this page does not model time.
- **Shadow executions.** Capizzi et al. (2008) run a public and a private copy of a process, which is the two-level case.
- **Browsers.** FlowFox (De Groef et al. 2012) runs the JavaScript of a web page with SME, to enforce information flow policies on the scripts of the page.
- **Faceted execution.** [Faceted execution](/faceted-execution/) simulates the copies in one run: it keeps a value for each level only where the copies differ. Bielova and Rezk (2016) compare the two and show that they do not give the same guarantees in general.
- **Declassification.** Later work lets a release of selected data from a high copy to a low copy, so that SME can work with a [declassification](/declassification/) policy.

## When to use it

Use SME when you cannot change or analyze the program, false alarms are not acceptable, and you can pay for one run per level, for example for scripts of a few origins in a browser. Use the [security type system](/security-type-system/) when the program is known in advance and TINI is enough. Use [no-sensitive-upgrade](/no-sensitive-upgrade/) when one run is all you can pay for and a stop is acceptable. Use [faceted execution](/faceted-execution/) when most of the program does not depend on secrets, so that most of the work is shared. SME does not help when a public output is meant to depend on a secret, such as the result of a password check; the low copy computes it from the default value.

## Pitfalls

- **The true inputs at line L3.** A copy that gets $s$ itself, and not $s_k$, computes the public outputs from the secrets, and "$l := h$" leaks. The right line L3 replaces each input above $k$ by the default value.
- **The wrong copy at line L6.** Taking all outputs from the top copy gives the plain run, with all its leaks. Taking an output from a copy above its level leaks too. The right line L6 takes the output on $x$ from the copy at $\Gamma(x)$.
- **A high copy first at line L1.** If the copies run one after the other and the high copy runs first and does not end, the low copy never runs. Then the public output exists or not depending on the secret. The right line L1 runs the lower copies first, or the copies run side by side.
- **Expecting the plain result from a TINI program.** For "while $h = 0$ do skip; $l := 1$" and $h = 1$, the plain run gives $l = 1$, but the public copy sees $h = d = 0$ and does not end, so SME gives no public output. This is correct for TSNI and is not a bug.
- **A default value that depends on the secret.** The default value $d$ at line L3 must be fixed in advance. A default value computed from the real input is the real input under another name.

## Implementations

## History

Capizzi, Longo, Venkatakrishnan and Sistla (2008) used a public and a private copy of a process to prevent leaks. Devriese and Piessens (2010) gave the general construction for a lattice of levels, with inputs and outputs during the run, named it secure multi-execution, and proved soundness for TSNI and precision for TSNI programs. De Groef et al. (2012) built FlowFox, a web browser that runs scripts with SME. Austin and Flanagan (2012) gave [faceted execution](/faceted-execution/), which shares the work of the copies, and Bielova and Rezk (2016) compared the two methods.

## References
