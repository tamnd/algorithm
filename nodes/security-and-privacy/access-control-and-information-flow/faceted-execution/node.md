---
tag: 5EDZCZ
kind: algorithm
slug: faceted-execution
name: Faceted execution
aliases:
- faceted values
area: security-and-privacy/access-control-and-information-flow
level: research
summary: Runs one program on values with a secret and a public facet, so that each observer sees the result computed from what it may know. This gives termination-insensitive noninterference.
model: word-ram
complexity:
  vars: {a: the number of steps of the plain run on the true inputs, b: the number of steps of the plain run on the public view, n: the number of nodes of the syntax tree of the program}
  time: {worst: O((a + b) n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: true, sound: true, complete: false}
history:
  year: 2012
  people: [Thomas H. Austin, Cormac Flanagan]
  note: Austin and Flanagan gave faceted values and the projection theorem at POPL 2012, as a dynamic analysis that does not stop the run where no-sensitive-upgrade does.
prereqs: [implicit-flow, termination-insensitive-noninterference, secure-multi-execution]
see_also: [no-sensitive-upgrade, security-type-system, self-composition, hyperproperty, declassification, covert-channel, denning-lattice-model, taint-analysis]
sources:
  - paper: doi:10.1145/2103656.2103677
    title: Thomas H. Austin and Cormac Flanagan, Multiple facets for dynamic information flow, Proceedings of the 39th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL 2012)
    locator: pp. 165 to 178, faceted values, the semantics of branches and assignments under a program counter of branches, the projection theorem and termination-insensitive noninterference
  - paper: doi:10.1007/978-3-319-45744-4_25
    title: Nataliia Bielova and Tamara Rezk, Spot the difference, secure multi-execution and multiple facets, ESORICS 2016, LNCS 9878
    locator: pp. 501 to 519, the comparison of faceted execution with secure multi-execution
  - paper: doi:10.1109/SP.2010.15
    title: Dominique Devriese and Frank Piessens, Noninterference through secure multi-execution, Proceedings of the 2010 IEEE Symposium on Security and Privacy
    locator: pp. 109 to 124, the method that faceted execution simulates in one run
  - paper: doi:10.1145/1554339.1554353
    title: Thomas H. Austin and Cormac Flanagan, Efficient purely-dynamic information flow analysis, Proceedings of the 4th ACM SIGPLAN Workshop on Programming Languages and Analysis for Security (PLAS 2009)
    locator: pp. 113 to 124, the no-sensitive-upgrade monitor that faceted execution makes more permissive
---

Faceted execution runs a program once, on values that can have two facets: a value $\langle a : b \rangle$ shows $a$ to an observer who may see secrets and $b$ to an observer who may not. A secret input $h$ starts as $\langle h : d \rangle$, with a fixed default value $d$. Most of the program runs once for both observers. Only where the two facets of a condition differ does the run split, and each observer's view takes its own branch. Austin and Flanagan (2012) proved the projection theorem: the view of each observer is exactly the plain run of the program on the inputs that observer may see. This gives termination-insensitive [noninterference](/noninterference/) ([TINI](/termination-insensitive-noninterference/)) without the stops of [no-sensitive-upgrade](/no-sensitive-upgrade/).

## In plain words

Think of each variable as a pair of values. One is for people who may know the secret, and the other is for everyone else. At the start, a secret variable holds the real secret on the first side and a fake value, such as 0, on the second side. Public variables hold the same value on both sides. The program then runs on these pairs. Adding two pairs adds each side. When the program must choose a branch and both sides agree, it takes that branch once. When they disagree, it runs each branch for one side only, and an assignment there changes only that side. At the end, the public side is what the program would give with the fake secret. So it cannot depend on the real secret.

## The problem

The input is a program $c$ in a small while language, a set of secret variables (level $H$) and public variables (level $L$), an initial store $s$ and a default value $d$. The output is a final faceted store $\sigma$. The observer at $H$ sees the $H$ facet $\pi_H(\sigma)$ of every variable, and the observer at $L$ sees the $L$ facet $\pi_L(\sigma)$.

The goal is the projection property: $\pi_H(\sigma)$ is the plain result $[\![c]\!](s)$, and $\pi_L(\sigma)$ is the plain result $[\![c]\!](s_L)$, where $s_L$ is $s$ with each secret input replaced by $d$. Since $s_L$ depends only on the public inputs, so does the view of the public observer. The program may be any program, secure or not.

## The algorithm

The run uses an explicit stack of pairs (command, program counter). The program counter is none outside a split, $H$ in a branch that only the $H$ view takes, and $L$ in a branch that only the $L$ view takes. Here $\langle a : b \rangle$ is a plain value when $a = b$, and the faceted value of an expression is the pair of its values in the two views.

```pseudo id=main
FACETED-RUN(c, σ)                          ▷ the final faceted store
L1  S ← a stack that holds the pair (c, none)
L2  while S is not empty do
L3      (d, p) ← pop(S)
L4      if d = (x := e) then v ← the faceted value of e in σ
L5          if p = none then σ(x) ← v
L6          if p = H then σ(x) ← ⟨H view of v : L view of σ(x)⟩
L7          if p = L then σ(x) ← ⟨H view of σ(x) : L view of v⟩
L8      if d = (d1; d2) then push (d2, p), then (d1, p)
L9      if d is an if or a while on e then (bH, bL) ← the truth of e in each view
L10         if p = none and bH ≠ bL then
L11             A ← [(L, bL), (H, bH)]     ▷ split: each view takes its own arm
L12         else A ← [(p, b)], with b = bL if p = L and b = bH otherwise
L13         for each (q, b) in A, if d = (if e then d1 else d2): push (d1 if b else d2, q)
L14         for each (q, b) in A, if d = (while e do d1) and b: push (d, q), then (d1, q)
L15 return σ
```

Lines L6 and L7 are the faceted form of an assignment in a secret context: the write changes only the view that takes the branch, and the other view keeps the old value. This is how faceted execution handles the [implicit flows](/implicit-flow/) of a branch that one view does not take: that view simply never sees the write. Line L10 splits the run only when the two views disagree on a condition. Inside a split (line L12), each view follows its own condition, and there is no second split, because there are only two views. A program that does not branch on secrets never splits and costs about as much as the plain run.

## Example

Take Fenton's program, with $h$ secret, $l$ and $m$ public, and the default value $d = 0$:

$$(l := 1);\ (m := 1);\ (\mathtt{if}\ h\ \mathtt{then}\ m := 0\ \mathtt{else}\ \mathtt{skip});\ (\mathtt{if}\ m\ \mathtt{then}\ l := 0\ \mathtt{else}\ \mathtt{skip}).$$

With $h = 1$ the start store is $h = \langle 1 : 0 \rangle$. The steps for the sequences are left out, and the two first assignments give $l = m = 1$, the same in both views.

| step | popped $(d, p)$ | action | $m$ | $l$ |
|---|---|---|---|---|
| 1 | (if $h$ ..., none) | $b_H = 1$, $b_L = 0$: split, push $(\mathtt{skip}, L)$, then $(m := 0, H)$ | 1 | 1 |
| 2 | $(m := 0, H)$ | change the $H$ view only (L6) | $\langle 0 : 1 \rangle$ | 1 |
| 3 | $(\mathtt{skip}, L)$ | nothing | $\langle 0 : 1 \rangle$ | 1 |
| 4 | (if $m$ ..., none) | $b_H = 0$, $b_L = 1$: split, push $(l := 0, L)$, then $(\mathtt{skip}, H)$ | $\langle 0 : 1 \rangle$ | 1 |
| 5 | $(\mathtt{skip}, H)$ | nothing | $\langle 0 : 1 \rangle$ | 1 |
| 6 | $(l := 0, L)$ | change the $L$ view only (L7) | $\langle 0 : 1 \rangle$ | $\langle 1 : 0 \rangle$ |

The final store is $h = \langle 1 : 0 \rangle$, $l = \langle 1 : 0 \rangle$, $m = \langle 0 : 1 \rangle$. The $H$ view $(h, l, m) = (1, 1, 0)$ is the plain run with $h = 1$. The $L$ view $(0, 0, 1)$ is the plain run with $h = 0$. With $h = 0$ the two views agree everywhere, no split happens, and the run ends with $l = 0$, $m = 1$. So the public observer sees $l = 0$ in both runs, while the plain program gives $l = 1$ when $h \ne 0$. [No-sensitive-upgrade](/no-sensitive-upgrade/) stops the run with $h = 1$ at step 2.

## Correctness

**Theorem 1 (projection, Austin and Flanagan 2012).** *Hypotheses:* a deterministic while language and two levels; any program and any faceted start store $\sigma_0$. *Statement:* the faceted run ends if and only if the plain runs from $\pi_H(\sigma_0)$ and from $\pi_L(\sigma_0)$ both end, and then $\pi_X$ of the final store is the result of the plain run from $\pi_X(\sigma_0)$, for $X = H$ and $X = L$.

The proof below shows that each step of the faceted run is a step of the plain run of one view or of both, and changes nothing in the other view. Lines L6 and L7 keep the other view, and line L11 gives each view the arm that its own condition chooses.

**Theorem 2 (TINI).** *Hypotheses:* two start stores that agree on the public inputs, each secret input $x$ given as $\langle s(x) : d \rangle$. *Statement:* if both faceted runs end, the observer at $L$ sees the same final store. Both $L$ views start from the same store $s_L$, so by Theorem 1 both are $[\![c]\!](s_L)$.

The $H$ view is the plain run on the true inputs. When the program is TINI and the faceted run ends, the $L$ view also gives the true values of the public variables, so faceted execution changes nothing that the public observer should see.

## Complexity

The model is the [word-RAM](/word-ram/). Let $a$ and $b$ be the numbers of steps of the plain runs on the $H$ and $L$ views, and $n$ the number of nodes of the syntax tree. Each step of the faceted run is a step of at least one plain run (Theorem 1), so there are at most $a + b$ steps. A step evaluates at most one expression in both views, in time $O(n)$. So the time is $O((a + b) n)$, and $O(a n)$ when the run never splits, since then $a = b$ and each step serves both views. Each variable holds at most two values, and the stack holds the pending parts of the program for the two views, $O(n)$ entries. The extra space is $O(n)$.

With more levels there are more views, and a value can have one facet for each view. In the worst case, when all views differ, the faceted run does the work of one plain run per view, as [secure multi-execution](/secure-multi-execution/) does.

## Properties

- **Sound for TINI.** The public view of the final store depends only on the public inputs (Theorem 2).
- **Not termination-sensitive.** The single run does not end when the $H$ view does not end. For "while $h = 1$ do skip; $l := 1$", the public observer sees no result exactly when $h = 1$. [Secure multi-execution](/secure-multi-execution/) gives TSNI here.
- **No stops.** Faceted execution never stops a run for security. Where no-sensitive-upgrade stops, it splits instead.
- **Transparent for TINI programs.** If the program is TINI and the faceted run ends, the public observer sees the true public results.
- **Not complete.** A TINI program whose run on the public view does not end, such as "while $h = 0$ do skip; $l := 1$" with $h = 1$ and $d = 0$, gives no result, although the plain run ends.
- **Shared work.** The parts of the run that do not depend on secrets run once for both views.

## Variants and improvements

- **Many levels.** Austin and Flanagan label each facet with a principal $k$ and write $\langle k ? V_H : V_L \rangle$. Facets nest, and the program counter is a set of branches, each "$k$" or "not $k$". A value then has a view for each set of principals, and the projection theorem holds for each view.
- **Secure multi-execution.** [Secure multi-execution](/secure-multi-execution/) runs one plain copy per level instead of one faceted run. It shares no work, but its public copy does not wait for the secret one, so it is TSNI. Bielova and Rezk (2016) compare the two methods and show that, in their original forms, secure multi-execution gives the stronger guarantee.
- **No-sensitive-upgrade.** [No-sensitive-upgrade](/no-sensitive-upgrade/) is the one-view form: it keeps a label instead of a second value and stops where faceted execution would split.
- **Faceted values for policies.** Faceted values have also been used to enforce privacy policies in languages where a value shows different data to different users; this page does not cover those languages.

## When to use it

Use faceted execution when the program is known only at run time, stops for security are not acceptable, and most of the program does not depend on secrets, so that the shared run saves work over [secure multi-execution](/secure-multi-execution/). Use secure multi-execution when the termination channel matters. Use [no-sensitive-upgrade](/no-sensitive-upgrade/) when a stop is acceptable and you want the smallest cost. Use the [security type system](/security-type-system/) when the program is known in advance. Like the others, faceted execution does not protect against the running time of the program; see [covert channels](/covert-channel/).

## Pitfalls

- **Both views at line L6.** Writing "$\sigma(x) \leftarrow v$" under the program counter $H$ changes the $L$ view too. For "if $h$ then $l := 1$ else skip" and $h = 1$, the public view of $l$ becomes 1, and with $h = 0$ it keeps its old value, so it copies a bit of $h$. The right line L6 keeps the $L$ view of the old value, as line L7 keeps the $H$ view.
- **No split at line L10.** Choosing the branch by the $H$ view alone and running it with the program counter none makes each assignment in it change both views, which is the plain run with its leaks. The right line L10 splits when $b_H \ne b_L$, and line L11 gives each view its own arm.
- **The wrong view at line L12.** Inside a split with the program counter $H$, the condition must be read in the $H$ view. Reading $b_L$ there makes the $H$ view follow the branches of the public view, and $\pi_H$ is then not the plain run on the true inputs. The right line L12 uses $b_H$ when $p = H$ and $b_L$ when $p = L$.
- **A default value from the secret.** The value $d$ of the public facet of a secret input must be fixed in advance. A value computed from the secret makes the public view depend on it.
- **Expecting TSNI.** The run does not end if either view does not end, so the public observer can learn about the secret from termination.

## Implementations

## History

Austin and Flanagan (2009) had shown that the purely dynamic [no-sensitive-upgrade](/no-sensitive-upgrade/) monitor gives TINI, at the price of stops on secure programs. Devriese and Piessens (2010) avoided the stops with [secure multi-execution](/secure-multi-execution/), at the price of one run per level. Austin and Flanagan (2012) combined the two ideas: faceted values simulate the runs of all levels in one run and split only where the runs differ, and the projection theorem shows that each view is a plain run. Bielova and Rezk (2016) compared faceted execution and secure multi-execution in detail.

## References
