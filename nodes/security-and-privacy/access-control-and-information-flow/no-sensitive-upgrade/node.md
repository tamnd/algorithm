---
tag: V9BYDH
kind: algorithm
slug: no-sensitive-upgrade
name: No-sensitive-upgrade check
aliases:
- NSU monitor
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: A dynamic information flow monitor that stops a run when it assigns to a public variable under a secret branch, which gives termination-insensitive noninterference.
model: word-ram
complexity:
  vars: {t: the number of steps of the run, n: the number of nodes of the syntax tree of the program}
  time: {worst: O(t n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: true, sound: true, complete: false}
history:
  year: 2009
  people: [Thomas H. Austin, Cormac Flanagan]
  note: Austin and Flanagan named the check and proved that it gives termination-insensitive noninterference at PLAS 2009. They credit the rule to the 2002 thesis of Steve Zdancewic.
prereqs: [implicit-flow, security-type-system, noninterference]
see_also: [termination-insensitive-noninterference, secure-multi-execution, faceted-execution, taint-analysis, reference-monitor, hyperproperty, covert-channel, decentralized-label-model]
sources:
  - paper: doi:10.1145/1554339.1554353
    title: Thomas H. Austin and Cormac Flanagan, Efficient purely-dynamic information flow analysis, Proceedings of the 4th ACM SIGPLAN Workshop on Programming Languages and Analysis for Security (PLAS 2009)
    locator: pp. 113 to 124, the no-sensitive-upgrade rule and the proof of termination-insensitive noninterference
  - paper: doi:10.1145/1814217.1814220
    title: Thomas H. Austin and Cormac Flanagan, Permissive dynamic information flow analysis, Proceedings of the 5th ACM SIGPLAN Workshop on Programming Languages and Analysis for Security (PLAS 2010)
    locator: pp. 1 to 12, the permissive-upgrade variant
  - paper: doi:10.1007/978-3-642-11486-1_30
    title: Andrei Sabelfeld and Alejandro Russo, From dynamic to static and back, riding the roller coaster of information-flow control research, Perspectives of Systems Informatics (PSI 2009), LNCS 5947
    locator: pp. 352 to 365, purely dynamic monitors and their comparison with static analysis
  - paper: doi:10.1145/2103656.2103677
    title: Thomas H. Austin and Cormac Flanagan, Multiple facets for dynamic information flow, Proceedings of the 39th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL 2012)
    locator: pp. 165 to 178, the comparison of no-sensitive-upgrade with faceted values
  - paper: doi:10.1093/comjnl/17.2.143
    title: J. S. Fenton, Memoryless subsystems, The Computer Journal 17(2), 1974
    locator: pp. 143 to 147, the example of a flow through a branch that is not taken
---

The no-sensitive-upgrade (NSU) check is a dynamic monitor for information flow. It runs the program, keeps a label for each variable and a label $pc$ for the program counter, and changes the label of a variable at each assignment, so that a public variable can hold a secret for a while. It adds one rule: under a secret program counter, an assignment to a variable that is now public stops the run. This rule closes the [implicit flows](/implicit-flow/) through branches that are not taken, which a monitor cannot see. Austin and Flanagan (2009) proved that the monitor gives termination-insensitive [noninterference](/noninterference/) ([TINI](/termination-insensitive-noninterference/)).

## In plain words

The monitor watches the program while it runs. Each variable has a tag, public or secret, and the tag can change: copying a secret into a variable makes the variable secret. Inside an if or a while whose condition reads a secret, everything the program writes is marked secret, because the fact that the write happened tells something about the secret. The problem is the branch that did not run. If a secret branch would have changed a public variable but did not, that variable keeps its public tag, and its value still tells something about the secret. The monitor cannot see writes that did not happen. So it forbids the dangerous case in the branch that does run: a write to a public variable inside a secret branch stops the program. A program that is never stopped has public results that do not depend on the secrets.

## The problem

The input is a program $c$ in a small while language (assignments $x := e$, sequences, if statements and while loops), a security lattice $(\mathcal{L}, \le, \sqcup, \sqcap)$ in which $\ell_1 \le \ell_2$ means that information may flow from $\ell_1$ to $\ell_2$, an initial store $s$ and an initial label $\lambda(x)$ for each variable. The output is the final store and the final labels, or "stop" when the monitor stops the run. Write $\mathrm{lab}_\lambda(e)$ for the join of $\lambda(y)$ over the variables $y$ of $e$.

The goal is soundness: for each observer level $\ell$ and each two initial stores that agree on the variables with $\lambda(x) \le \ell$, if both monitored runs end normally, the observer sees the same final values. The observer sees a variable only if its final label is at most $\ell$. A [security type system](/security-type-system/) gives the same guarantee before the run, but with a fixed label for each variable.

## The algorithm

The monitor runs the program with an explicit stack of pairs (command, label of the program counter). Each pair carries its own label, so the label of a branch ends when its last command ends.

```pseudo id=main
NSU-RUN(c, s, λ)                           ▷ the final (s, λ), or stop
L1  S ← a stack that holds the pair (c, ⊥)
L2  while S is not empty do
L3      (d, p) ← pop(S)
L4      if d = (x := e) then
L5          if p ≰ λ(x) then stop the run
L6          (v, k) ← the value and label of e in (s, λ); s(x) ← v
L7          λ(x) ← k ⊔ p
L8      if d = (d1; d2) then push (d2, p), then (d1, p)
L9      if d = (if e then d1 else d2) then (v, k) ← the value and label of e
L10         push (d1 if v ≠ 0 else d2, p ⊔ k)
L11     if d = (while e do d1) then (v, k) ← the value and label of e
L12         if v ≠ 0 then q ← p ⊔ k; push (d, q), then (d1, q)
L13 return (s, λ)
```

A skip command does nothing. Line L7 is the flow-sensitive part: the new label of $x$ is the label of the data, $k$, joined with the label of the context, $p$. So "$l := h$" makes $l$ secret, and a later "$l := 0$" at a public program counter makes it public again. Lines L10 and L12 raise the program counter label for the commands that a secret condition controls. Line L5 is the no-sensitive-upgrade check: when the program counter label is not below the current label of $x$, line L7 would raise the label of $x$ on a secret path. The monitor would raise it in this run, but a run with a different secret could skip the branch and leave $x$ public. So the monitor stops instead.

## Example

The example is the one of Fenton (1974). Take the two-point lattice $L \le H$, $\lambda(l) = \lambda(m) = L$, $\lambda(h) = H$ and

$$c = (l := 1);\ (m := 1);\ (\mathtt{if}\ h\ \mathtt{then}\ m := 0\ \mathtt{else}\ \mathtt{skip});\ (\mathtt{if}\ m\ \mathtt{then}\ l := 0\ \mathtt{else}\ \mathtt{skip}).$$

Without the check of line L5, the final public $l$ is 1 when $h \ne 0$ and 0 when $h = 0$: a copy of one bit of $h$. The table shows the run with $h = 1$, after the two first assignments, which give $l = m = 1$ with label $L$.

| step | popped $(d, p)$ | NSU | without line L5 |
|---|---|---|---|
| 1 | (if $h$ ..., $L$) | $v = 1$, $k = H$, push $(m := 0, H)$ | the same |
| 2 | $(m := 0, H)$ | $H \not\le \lambda(m) = L$: stop | $m = 0$, $\lambda(m) = H$ |
| 3 | (if $m$ ..., $L$) | | $v = 0$, $k = H$, push $(\mathtt{skip}, H)$ |
| 4 | $(\mathtt{skip}, H)$ | | end: $l = 1$, $\lambda(l) = L$ |

With $h = 0$, both monitors run "skip" at $H$, then the second if at $L$, since $m = 1$ has label $L$, and they end with $l = 0$ and $\lambda(l) = L$. So without line L5 the observer sees $l = 1$ or $l = 0$, which tells whether $h \ne 0$. With NSU, the observer sees $l = 0$ or a stopped run. TINI compares only the runs that end, and there is one, so there is no leak in this sense. The stop itself is a signal; see Pitfalls.

## Correctness

**Theorem (Austin and Flanagan 2009).** *Hypotheses:* the deterministic while language above; an observer at level $\ell$ who sees the final value of each variable whose final label is at most $\ell$, and sees which variables are hidden. *Statement:* if two initial stores agree on each $x$ with $\lambda(x) \le \ell$, and both monitored runs end normally at line L13, the observer sees the same final state.

The proof below uses two lemmas. Lemma 2 (confinement) says that a command run at a program counter label $p \not\le \ell$ changes no variable whose label is at most $\ell$: line L5 stops each such write. This is where the check is needed. Lemma 3 is an induction on the two runs, with the program counter labels of the two runs either both at most $\ell$ or both not. A secret branch may run different commands in the two runs, and Lemma 2 shows that neither run changes what the observer sees.

When the monitor ends normally, the final store is the store of the plain run, because the monitor only adds labels and tests. The theorem says nothing about runs that stop or do not end.

## Complexity

The model is the [word-RAM](/word-ram/). Let $t$ be the number of steps of the run, one for each pop at line L3, and $n$ the number of nodes of the syntax tree. A step evaluates at most one expression, in time linear in its size, which is at most $n$, and does $O(1)$ joins and tests of labels. For a fixed finite lattice, or for labels that are sets of at most $w$ categories stored as one machine word, each join and test takes $O(1)$ time. So the time is $O(t n)$, and $O(t)$ when each expression has constant size. The plain run takes the same number of steps, so the monitor costs a constant factor. Each stack entry is a distinct pending part of the program, so the stack holds $O(n)$ entries; the labels take one word for each variable. The extra space is $O(n)$.

## Properties

- **Sound for TINI.** Each pair of runs that end is noninterferent (Correctness).
- **Not complete.** The secure program "if $h$ then $l := 0$ else $l := 0$" is stopped, since $l$ is public and the program counter is $H$.
- **Flow-sensitive.** The label of a variable follows its current content. The program "$l := h$; $l := 0$" ends with $l$ public.
- **Transparent on the runs it does not stop.** A run that ends normally has the same final store as the plain run.
- **Online.** The monitor needs only the current state, not the rest of the program, so it works for code that is known only at run time.
- **Stopping is the only defense.** The monitor never changes a value. It either lets a step run or stops the run.

## Variants and improvements

- **Permissive upgrade.** Austin and Flanagan (2010) replace the stop at line L5 by a mark: the variable gets a special "partially leaked" label, and the run stops only if the program later branches on such a value. This accepts more programs and keeps TINI.
- **Hybrid monitors.** A static analysis of the branch that is not taken finds the variables it could write, and the monitor raises their labels too. Then line L5 is not needed for those variables. The survey of Sabelfeld and Russo (2009) compares such monitors with purely dynamic ones.
- **Secure multi-execution.** [Secure multi-execution](/secure-multi-execution/) runs the program once for each level and gives each run only the inputs it may see. It never stops a run and gives termination-sensitive noninterference, at the cost of one run per level.
- **Faceted execution.** [Faceted execution](/faceted-execution/) keeps a secret and a public value for each variable that a secret branch writes, and runs both branches only where they differ. On Fenton's program it gives the observer $l = 0$ in both runs, where NSU stops.
- **Taint tracking.** [Taint analysis](/taint-analysis/) usually keeps only lines L6 and L7 without $p$. It tracks explicit flows and misses implicit ones.

On Fenton's program with $h = 1$ the three dynamic methods behave as follows.

| method | runs | what the public observer gets |
|---|---|---|
| NSU | 1 | stop |
| secure multi-execution | 2 | $l = 0$, from the run with $h$ replaced by a default value 0 |
| faceted execution | 1, split where the facets differ | $l = 0$, the public facet of $l$ |

## When to use it

Use NSU when the program is known only at run time, for example a script on a web page, and a stop is an acceptable answer to a possible leak. It needs one run and a small cost at each step. Use a [security type system](/security-type-system/) when the program is known in advance, because a static check costs nothing at run time and gives the same TINI guarantee for all inputs. Use [secure multi-execution](/secure-multi-execution/) or [faceted execution](/faceted-execution/) when false stops are not acceptable. NSU does not protect against the time a run takes or against the fact that it stops; see [covert channels](/covert-channel/).

## Pitfalls

- **No check at line L5.** A monitor with only lines L6 and L7 is unsound. On Fenton's program it gives the public result $l = 1$ when $h \ne 0$ and $l = 0$ when $h = 0$ (Example). The right line L5 stops the run when $p \not\le \lambda(x)$.
- **No program counter at line L7.** With "$\lambda(x) \leftarrow k$", the program "if $h$ then $h := 0$ else skip" passes the check, since $h$ is secret, but gives $h$ the label $L$ when $h \ne 0$ and leaves it at $H$ when $h = 0$. The observer learns whether $h \ne 0$ from the label. The right line L7 is "$\lambda(x) \leftarrow k \sqcup p$".
- **The plain label at line L10 or L12.** Pushing the branch with $p$ instead of $p \sqcup k$ accepts "if $h$ then $l := 1$ else $l := 0$", which copies $h$ to $l$. The right lines push $p \sqcup k$, and line L12 also pushes the loop itself with $q$, so that each later test of the loop condition runs at the raised label.
- **A shared program counter.** A single variable $pc$ that is raised at line L10 and never lowered stops each later public assignment, and one that is lowered at the end of the if command lowers it before the branch has run. Keep the label in each stack entry, as in lines L8, L10 and L12.
- **Treating the stop as invisible.** The stop at line L5 depends on the secret: in the Example, the run stops exactly when $h \ne 0$. If the observer sees that a run stops, NSU leaks through this channel, as each TINI method does. With public output during the run, Askarov et al. (2008) show that such a channel can reveal a secret of $N$ binary digits, but only in time exponential in $N$; see [TINI](/termination-insensitive-noninterference/).

## Implementations

## History

Fenton (1974) described the flow through a branch that is not taken, and the certification of Denning and Denning (1977), based on the [lattice model](/denning-lattice-model/), handled it statically. For a long time, it was widely held that dynamic monitors were unable to enforce noninterference, because they see only one run. Austin and Flanagan (2009) took the no-sensitive-upgrade rule, which they credit to the 2002 thesis of Zdancewic, gave it its name, and proved that a purely dynamic monitor with this rule gives TINI for a language with references. Their later papers give the permissive-upgrade variant (2010) and faceted values (2012). The survey of Sabelfeld and Russo (2009) places these monitors with respect to static analysis.

## References
