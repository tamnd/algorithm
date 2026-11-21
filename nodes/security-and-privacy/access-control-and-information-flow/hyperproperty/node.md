---
tag: 5SWFTZ
kind: definition
slug: hyperproperty
name: Hyperproperty
aliases:
- hypersafety
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: A property of sets of execution traces rather than single traces, which can state noninterference and other policies that relate runs.
prereqs: [safety-property, liveness-property, noninterference]
see_also: [termination-insensitive-noninterference, self-composition, em-enforceable-policies-theorem, security-automaton, linear-temporal-logic, constant-time-verification, secure-multi-execution, reference-monitor]
sources:
  - paper: doi:10.1109/CSF.2008.7
    title: Michael R. Clarkson and Fred B. Schneider, Hyperproperties, Proceedings of the 21st IEEE Computer Security Foundations Symposium (CSF 2008)
    locator: pp. 51 to 65, the definitions of hyperproperty, hypersafety, k-safety and hyperliveness, and the decomposition theorem
  - paper: doi:10.3233/JCS-2009-0393
    title: Michael R. Clarkson and Fred B. Schneider, Hyperproperties, Journal of Computer Security 18(6), 2010
    locator: pp. 1157 to 1210, the journal version, with the proofs, the reduction of k-safety to safety by self-composition, and the classification of security policies
  - paper: doi:10.1007/11547662_24
    title: Tachio Terauchi and Alex Aiken, Secure information flow as a safety problem, Proceedings of SAS 2005, LNCS 3672
    locator: pp. 352 to 367, 2-safety properties and noninterference as one of them
  - paper: doi:10.1145/353323.353382
    title: Fred B. Schneider, Enforceable security policies, ACM Transactions on Information and System Security 3(1), 2000
    locator: pp. 30 to 50, security automata and the result that each policy an execution monitor can enforce is a safety property
---

A hyperproperty is a set of sets of traces. A trace property, such as "each request gets an answer", says which single runs are allowed. A hyperproperty says which *systems*, as sets of runs, are allowed, so it can compare runs with each other. Clarkson and Schneider (2008) introduced the notion to give security policies such as [noninterference](/noninterference/) the same theory that [safety](/safety-property/) and [liveness](/liveness-property/) give trace properties. Noninterference is not a trace property, because no single run shows a leak; it is a hyperproperty, and more exactly a 2-safety hyperproperty.

## Definition

**Traces and properties.** A state is a value of the system variables. A trace is a finite or infinite sequence of states; Clarkson and Schneider use infinite traces, and $\Psi_{\mathrm{fin}}$ for the finite ones. A *property* is a set of traces. A system is modeled by the set $S$ of its traces, and $S$ satisfies the property $P$ if $S \subseteq P$.

**Hyperproperty.** A *hyperproperty* is a set $\mathbf{H}$ of sets of traces. A system $S$ satisfies $\mathbf{H}$ if $S \in \mathbf{H}$. Each property $P$ gives the hyperproperty $[P] = \{S : S \subseteq P\}$, the set of all subsets of $P$, and $S \in [P]$ exactly when $S$ satisfies $P$. So hyperproperties include all properties. The interesting ones are those that are not of the form $[P]$.

**Prefixes.** For a finite set $M$ of finite traces and a set $T$ of traces, write $M \le T$ if each trace of $M$ is a prefix of some trace of $T$.

**Hypersafety.** $\mathbf{H}$ is a *hypersafety* hyperproperty if for each $T \notin \mathbf{H}$ there is a finite set $M$ of finite traces with $M \le T$ such that no $T' \ge M$ is in $\mathbf{H}$. The set $M$ is the "bad thing": a finite set of finite observations that no extension can repair.

**k-safety.** $\mathbf{H}$ is $k$-safety if it is hypersafety and the bad thing can always be chosen with $|M| \le k$. The 1-safety hyperproperties are the properties $[P]$ with $P$ a safety property. Terauchi and Aiken (2005) earlier named the 2-safety class for programs.

**Hyperliveness.** $\mathbf{H}$ is a *hyperliveness* hyperproperty if for each finite set $M$ of finite traces there is a $T \in \mathbf{H}$ with $M \le T$: no finite observation is beyond repair.

**Theorem (Clarkson and Schneider).** Each hyperproperty is the intersection of a hypersafety hyperproperty and a hyperliveness hyperproperty. A $k$-safety hyperproperty of a system $S$ is a safety property of the $k$-fold self-composition of $S$, whose traces are $k$-tuples of traces of $S$ run side by side. This reduction is the basis of [self-composition](/self-composition/).

**Theorem (Schneider 2000).** *Hypotheses:* an execution monitor sees one run of the system, one step at a time, and stops the run when the policy is about to be broken. *Statement:* each policy such a monitor can enforce is a safety property of single traces (the condition is necessary, not sufficient). A hyperproperty that is not of the form $[P]$ is not a property at all, so an execution monitor cannot enforce it in general: no run that it watches is bad by itself. This is the reason the dynamic monitors for information flow change the run, as [no-sensitive-upgrade](/no-sensitive-upgrade/) does by stopping it on a possible leak, or run the program more than once, as [secure multi-execution](/secure-multi-execution/) does. See the [EM-enforceable policies theorem](/em-enforceable-policies-theorem/) and [security automata](/security-automaton/).

The alias "hypersafety" names the subclass above, not the general notion.

## Examples and non-examples

- **Noninterference: 2-safety, not a property.** Take a system whose traces start with a secret input $h$ and a public input $l$ and end with a public output. Noninterference says: two traces with the same $l$ have the same output. A violation is shown by two finite traces with the same $l$ and different outputs, so it is 2-safety. It is not a property: the system $S = \{(h{=}0, l{=}0, \mathit{out}{=}0), (h{=}1, l{=}0, \mathit{out}{=}1)\}$ leaks, but each of its traces also belongs to a system that does not leak, such as the system with only that trace. The page [noninterference](/noninterference/) gives the proof.
- **TINI: 2-safety.** [Termination-insensitive noninterference](/termination-insensitive-noninterference/) compares only runs that stop. Its bad thing is a pair of finite runs.
- **Constant-time execution: 2-safety.** Two runs with the same public inputs must have the same sequence of branches and memory addresses. This is the property that [constant-time verification](/constant-time-verification/) checks by self-composition.
- **Observational determinism: 2-safety.** Each pair of traces with equal public inputs is equivalent on public state.
- **Generalized noninterference: hyperliveness.** For each two traces there must be a third trace that has the secret inputs of the first and the public behaviour of the second. A finite set of observations can always be extended with such traces, so this is not hypersafety. Clarkson and Schneider classify it as hyperliveness.
- **Mean response time: neither k-safety nor a property.** A bound on the average response time over all runs depends on the whole set of runs.
- **Non-example of a proper hyperproperty: "no state has $x < 0$".** This is the safety property $P$, and the hyperproperty $[P]$ adds nothing to it. It is 1-safety.

## Related definitions

- **[Safety](/safety-property/) and [liveness](/liveness-property/)** are the trace-property classes that hypersafety and hyperliveness lift. The decomposition theorem lifts the theorem of Alpern and Schneider that each property is the intersection of a safety and a liveness property.
- **[Noninterference](/noninterference/)** is the main example. TINI is 2-safety. The termination-sensitive form needs to compare a run that stops with one that does not, which no finite set of finite traces can show; it is not 2-safety.
- **[Self-composition](/self-composition/)** turns a $k$-safety hyperproperty into a safety property of a product program, so that ordinary tools such as Hoare logic and model checkers apply.
- **Logics.** [Linear temporal logic](/linear-temporal-logic/) states properties of one trace. Logics such as HyperLTL quantify over several traces and state hyperproperties; this site has no page on them.
- **[Reference monitors](/reference-monitor/)** and [security automata](/security-automaton/) see one trace and enforce only safety properties, so they cannot enforce information flow policies directly.

## References
