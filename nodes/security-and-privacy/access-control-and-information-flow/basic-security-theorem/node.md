---
tag: MPW94V
kind: theorem
slug: basic-security-theorem
name: Basic security theorem
aliases:
- Bell-LaPadula basic security theorem
area: security-and-privacy/access-control-and-information-flow
level: core
summary: A Bell-LaPadula system is secure if and only if its initial state is secure and every transition keeps the simple security, star and discretionary properties.
prereqs: [bell-lapadula-model]
see_also: [bell-lapadula-model, mandatory-access-control, safety-property, noninterference, biba-integrity-model, reference-monitor, harrison-ruzzo-ullman-model, covert-channel]
sources:
  - url: "https://csrc.nist.gov/files/pubs/conference/1998/10/08/proceedings-of-the-21st-nissc-1998/final/docs/early-cs-papers/bell76.pdf"
    title: "D. Elliott Bell and Leonard J. LaPadula, Secure Computer System: Unified Exposition and Multics Interpretation, MITRE MTR-2997 Rev. 1 (ESD-TR-75-306), March 1976"
    locator: "Section II, p. 20 (the basic security theorem and the inductive nature of security); Appendix, pp. 86 to 94 (definitions, Theorems A1, A2 and A3, Corollary A1 and Theorem A4)"
  - paper: doi:10.1016/0020-0190(85)90065-1
    title: "John McLean, A comment on the 'basic security theorem' of Bell and LaPadula, Information Processing Letters 20(2), 1985, pages 67 to 70"
    locator: the theorem holds for any property of states, and System Z
  - paper: doi:10.1109/SP.1987.10020
    title: "John McLean, Reasoning about security models, Proceedings of the 1987 IEEE Symposium on Security and Privacy"
    locator: System Z and the limits of a definition of security based on states
  - book: isbn:9780321712332
    title: "Matt Bishop, Computer Security: Art and Science, second edition, Addison-Wesley, 2018"
    locator: "Chapter 5, Confidentiality Policies (the Bell-LaPadula model, the basic security theorem and the controversy over it)"
---

The basic security theorem of the [Bell-LaPadula model](/bell-lapadula-model/) says that a system is secure if and only if it starts in a secure state and each transition that it makes produces a state with the simple security property, the \*-property and the discretionary security property. Its value is that it is local: to show that a system keeps a property in every reachable state, it is enough to check each transition by itself, and in practice each rule by itself. Bell and LaPadula proved it in their reports of 1973 to 1976. McLean showed in 1985 and 1987 that the same theorem holds for any property of states, so the theorem is sound but it does not by itself show that the property means security.

## Statement

The notation is that of the [Bell-LaPadula model](/bell-lapadula-model/). A state is $v = (b, M, f, H)$ with current access set $b$, matrix $M$, level functions $f = (f_s, f_o, f_c)$ and hierarchy $H$. The set $S'$ of subjects bound by the \*-property is fixed. An *action* is a tuple $(x, y, v^*, v)$: request $x$ in state $v$ gives decision $y$ and next state $v^* = (b^*, M^*, f^*, H^*)$. The system $\Sigma(R, D, W, z_0)$ has a set $W$ of allowed actions and an initial state $z_0$. A *run* is a finite sequence of states $z_0, z_1, \ldots, z_n$ such that for each $t \ge 1$ some $(x_t, y_t, z_t, z_{t-1}) \in W$; this action *occurs* in the run. The system is *secure* if every state of every run, $z_0$ included, has the three properties.

For a triple $(S, O, \chi)$ with access attribute $\chi \in \{e, r, a, w\}$ and a state $v^*$, call the triple

- *ss-good in $v^*$* if $\chi \in \{r, w\}$ implies $f^*_s(S)\ \text{dom}\ f^*_o(O)$;
- *\*-good in $v^*$* if $S \notin S'$, or $\chi = e$, or $\chi = a$ and $f^*_o(O)\ \text{dom}\ f^*_c(S)$, or $\chi = w$ and $f^*_o(O) = f^*_c(S)$, or $\chi = r$ and $f^*_c(S)\ \text{dom}\ f^*_o(O)$;
- *ds-good in $v^*$* if $\chi \in M^*[S, O]$.

For each of the three kinds, an action $(x, y, v^*, v)$ satisfies the *conditions* of that kind if

1. every triple in $b^* \setminus b$ is good in $v^*$, and
2. every triple in $b$ that is not good in $v^*$ is not in $b^*$.

**Theorem** (basic security theorem; Bell and LaPadula 1976, Corollary A1). $\Sigma(R, D, W, z_0)$ is secure if and only if $z_0$ is secure and every action that occurs in a run of $\Sigma$ satisfies the ss-conditions, the \*-conditions and the ds-conditions.

This is Corollary A1 of the 1976 report, with the initial state counted as part of each run. The ss-, \*- and ds-conditions are those of Theorems A1, A2 and A3 of the report. The report states the conditions for every action of $W$. The "if" direction holds in that form as well. The "only if" direction needs them only for the actions that occur, and it fails for an action of $W$ that starts in a state no run reaches.

## In plain words

A secure system is one that never enters a bad state. Checking every state that the system could ever reach is hard, because there can be very many of them. The theorem says that it is enough to check two smaller things. First, the system must start in a good state. Second, each single step must not produce a bad access: any new access that a step adds must obey the rules, and any old access that the rules no longer allow after the step must be removed by that step. If both checks pass, then every state that the system reaches is good, and if one of them fails, some reachable state is bad. A designer can therefore check each operation of the system alone, one at a time, and need not think about long chains of operations.

## Proof

**Lemma.** For each of the three kinds, an action $(x, y, v^*, v)$ satisfies the conditions of that kind if and only if every triple of $b^*$ is good in $v^*$.

*Proof of the lemma.* Split $b^*$ into two disjoint parts: $b^* = (b^* \setminus b) \cup (b^* \cap b)$. Suppose the conditions hold. A triple in $b^* \setminus b$ is good by condition 1. A triple in $b^* \cap b$ is in $b$ and in $b^*$, so by condition 2 it cannot be bad, and it is good. So every triple of $b^*$ is good. Conversely, suppose every triple of $b^*$ is good. Then every triple of $b^* \setminus b$ is good, which is condition 1. A triple of $b$ that is not good in $v^*$ cannot be in $b^*$, because every triple of $b^*$ is good, which is condition 2.

Each of the three properties of a state is a statement about each triple of the access set separately: a state $v^*$ has the ss-property if and only if every triple of $b^*$ is ss-good in $v^*$, and the same holds for the \*-property and the ds-property. So by the lemma, an action satisfies all three kinds of conditions if and only if its next state $v^*$ is secure. Call this fact (L).

**If.** Assume that $z_0$ is secure and that every action that occurs in a run satisfies the three kinds of conditions. Take any run $z_0, \ldots, z_n$ and any $t$ with $0 \le t \le n$. If $t = 0$, then $z_t = z_0$ is secure by assumption. If $t \ge 1$, the action $(x_t, y_t, z_t, z_{t-1})$ occurs in the run, so it satisfies the conditions, and by (L) its next state $z_t$ is secure. So every state of every run is secure, and $\Sigma$ is secure.

**Only if.** Assume that $\Sigma$ is secure. The sequence $z_0$ alone is a run, so $z_0$ is secure. Let $(x, y, v^*, v)$ be an action that occurs in a run $z_0, \ldots, z_n$, at step $t$, so $v^* = z_t$. Since $\Sigma$ is secure, $z_t$ is secure, and by (L) the action satisfies the three kinds of conditions. $\blacksquare$

**Example.** Let a subject $S \in S'$ hold $(S, O, r)$ with $f_c(S) = f_o(O) = \text{(S, {NATO})}$. An action raises the level of $O$ to $f^*_o(O) = \text{(TS, {NATO})}$ and leaves $b^* = b$. The triple is in $b$, it is not ss-good in $v^*$ if $f_s(S)$ is below top secret, and it is still in $b^*$, so condition 2 fails and the theorem says that the action breaks security. A correct rule that changes a level must also remove the read access, in the same step.

## Consequences

- **Rule by rule checking** (Bell and LaPadula 1976, Theorem A4 and its companions; theorem). Let the system be built from rules $\rho_1, \ldots, \rho_k$, each a function from a request and a state to a decision and a next state. If each rule maps every secure state to a secure state, then $\Sigma$ is secure for every secure initial state. The proof is the same induction. This is how Section III of the report checks its Multics rules: each rule, such as get-read or change-subject-current-security-level, is shown to keep the three properties alone.
- **Induction for invariants** (theorem). The theorem is an instance of the induction rule for invariants of a transition system: a property that holds initially and is preserved by each step holds in every reachable state. Security in this sense is a [safety property](/safety-property/): a bad state is a finite witness of failure.
- **Enforcement.** A [reference monitor](/reference-monitor/) that checks the conditions before it commits each transition keeps the system secure. The adversary is any program that runs as an untrusted subject and issues any requests; it cannot change the rules or bypass the monitor.

## Tightness

- **The initial state is needed.** Take a system whose only rule releases all accesses, so $b^* = \emptyset$. Every action satisfies the conditions, since $b^*$ is empty. If $z_0$ holds a read-up access, the run $z_0$ shows that the system is not secure. So the condition on $z_0$ cannot be dropped.
- **The new state must be used.** The conditions test the triples against $f^*$ and $M^*$, the levels and matrix after the step. A test against $f$ and $M$ would accept the action of the example above, which leaves a read access in place after the object is raised to a higher level.
- **The theorem holds for any property** (McLean 1985; theorem). The proof uses only that each property is a statement about each triple separately, and the same induction works for any property of states. McLean's System Z has one rule: on any request, it lowers every subject and every object to the lowest level and then grants the access. Every state is secure in the Bell-LaPadula sense, so System Z satisfies the theorem, yet a subject can read all data that was high before. The theorem is correct, but the definition of a secure state does not capture what users mean by security when levels can change. The usual fixes are the *tranquility* principles, which restrict changes of level, and definitions on the behavior of the whole system such as [noninterference](/noninterference/).
- **Covert channels.** The theorem is about the access set only. A system whose transitions keep the three properties can still leak through a [covert channel](/covert-channel/), for example through which requests get the answer "no".

## History

Bell and LaPadula built the model at MITRE in a series of reports from 1973 on, for the US Air Force, with the aim of a secure kernel for Multics. The *Unified Exposition and Multics Interpretation* of 1976 gives the final form: Theorems A1, A2 and A3 for the three properties separately, and Corollary A1 for all three together, which is the basic security theorem. The report calls the result the "inductive nature" of security. In 1985 McLean pointed out that the theorem holds for any property of states, and in 1987 he gave System Z. Bell answered in 1988 and defended the model as a tool to be used with a careful choice of rules. The exchange is a standard lesson on the difference between a correct proof and a correct definition, and it is one reason that later work moved to [noninterference](/noninterference/).

## References
