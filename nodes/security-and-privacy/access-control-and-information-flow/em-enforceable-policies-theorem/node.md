---
tag: APF8E3
kind: theorem
slug: em-enforceable-policies-theorem
name: Execution monitors enforce only safety properties
aliases:
- EM-enforceable policies theorem
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: Every policy that an execution monitor can enforce is a safety property. The converse fails, and policies such as availability or noninterference need other mechanisms.
prereqs: [security-automaton, safety-property, liveness-property]
see_also: [inline-reference-monitor, reference-monitor, hyperproperty, noninterference, halting-problem, rice-theorem, secure-multi-execution, turing-machine]
sources:
  - paper: doi:10.1145/353323.353382
    title: Fred B. Schneider, Enforceable security policies, ACM Transactions on Information and System Security 3(1), 2000
    locator: pp. 30 to 50, the definitions of security policy, property and execution monitoring, the conditions that an EM-enforceable policy must meet, and the conclusion that it is a safety property
  - paper: doi:10.1016/0020-0190(85)90056-0
    title: Bowen Alpern and Fred B. Schneider, Defining liveness, Information Processing Letters 21(4), 1985
    locator: pp. 181 to 185, the formal definitions of safety and liveness and the theorem that every property is the intersection of a safety property and a liveness property
  - paper: doi:10.1145/1111596.1111601
    title: Kevin W. Hamlen, Greg Morrisett and Fred B. Schneider, Computability classes for enforcement mechanisms, ACM Transactions on Programming Languages and Systems 28(1), 2006
    locator: pp. 175 to 205, the computability constraint on monitors, the gap between safety and EM-enforceability, and the classes of statically enforceable and rewriting-enforceable policies
  - paper: doi:10.1007/s10207-004-0046-8
    title: Jay Ligatti, Lujo Bauer and David Walker, Edit automata, enforcement mechanisms for run-time security policies, International Journal of Information Security 4(1-2), 2005
    locator: pp. 2 to 16, monitors that insert and suppress actions and the policies they enforce
  - paper: doi:10.3233/JCS-2009-0393
    title: Michael R. Clarkson and Fred B. Schneider, Hyperproperties, Journal of Computer Security 18(6), 2010
    locator: pp. 1157 to 1210, security policies as sets of sets of traces, and noninterference as a hyperproperty that is not a property
---

The theorem of Schneider (2000) says what a run-time monitor cannot do. A monitor that watches one run of a program, action by action, and whose only power is to stop the program, can enforce only policies that are [safety properties](/safety-property/): a run is bad exactly when some finite prefix of it is already bad. The condition is necessary, not sufficient: some safety properties cannot be enforced by any monitor that is a program, because deciding when to stop would decide the [halting problem](/halting-problem/). Policies such as availability (a liveness property) and noninterference (a [hyperproperty](/hyperproperty/)) are not safety properties, so they need static analysis, program rewriting or monitors with more power.

## Statement

**Setting.** Let $\Psi$ be a countable set of actions. An execution is a finite or infinite sequence over $\Psi$. Write $\Psi^\infty$ for the set of all executions and, for an execution $\sigma$, write $\sigma[..i]$ for its prefix of length $i$ (so $\sigma[..0]$ is the empty sequence $\varepsilon$). A target is described by the set $\Sigma \subseteq \Psi^\infty$ of its possible executions. A security policy is a predicate $P$ on sets of executions; the target satisfies $P$ when $P(\Sigma)$ holds.
- $P$ is a **property** if there is a predicate $\hat P$ on single executions with $P(\Sigma) \iff \forall \sigma \in \Sigma : \hat P(\sigma)$, for every $\Sigma$.
- A property is a **safety property** if every execution that breaks it has a finite prefix after which nothing can repair it: for every $\sigma$ with $\neg \hat P(\sigma)$ there is an $i$ such that $\neg \hat P(\sigma[..i]\,\tau)$ for every $\tau \in \Psi^\infty$.

**Execution monitor.** An execution monitor is a function $M$ from finite sequences to $\{\text{ok}, \text{stop}\}$. It is applied to the target as follows: before the action $\sigma_{i}$ runs, the monitor sees the prefix $\sigma[..i]$ (the actions so far and the next one) and, if $M(\sigma[..i]) = \text{stop}$, it ends the execution so that $\sigma_i$ does not run. The monitor lets $\sigma$ run in full when $M(\sigma[..i]) = \text{ok}$ for every finite prefix $\sigma[..i]$, including $\varepsilon$. These are the three hypotheses of the model:
1. the monitor sees only the current execution, and only the part of it that has happened or is about to happen;
2. its only intervention is to stop the target before an action;
3. a policy $P$ is **EM-enforceable** if some monitor $M$ satisfies, for every set $\Sigma \subseteq \Psi^\infty$: $P(\Sigma)$ holds if and only if $M$ lets every execution of $\Sigma$ run in full.

Hypothesis 3 asks that the monitor stop exactly the executions of targets that break the policy. The adversary is an arbitrary target: $\Sigma$ ranges over all sets of executions, so the target may produce any sequence of actions.

**Theorem (Schneider 2000).** Every EM-enforceable policy is a safety property.

## In plain words

A monitor that can only watch and stop must make up its mind at some moment, from what it has seen so far. If it stops a run, that run must already be bad, whatever would have come next, because the monitor cannot wait to see the rest. And it decides each run on its own, so the policy cannot be about how runs compare with each other. Policies with both features are exactly the safety properties: "nothing bad ever happens", where a bad thing is something you can point at in a finite piece of the run. "Something good eventually happens" is not of this kind, because no finite piece shows that it will not happen later.

## Proof

Let $M$ be a monitor that enforces $P$ in the sense of hypothesis 3. Define the predicate on single executions

$$ \hat P(\sigma) \iff M(\sigma[..i]) = \text{ok for every finite prefix } \sigma[..i] \text{ of } \sigma, $$

that is, $\hat P(\sigma)$ holds when the monitor lets $\sigma$ run in full.

*$P$ is a property.* Take any $\Sigma$. By hypothesis 3, $P(\Sigma)$ holds if and only if $M$ lets every execution of $\Sigma$ run in full, that is, if and only if $\hat P(\sigma)$ for every $\sigma \in \Sigma$. This is the definition of a property with predicate $\hat P$. (In particular $\hat P(\sigma) \iff P(\{\sigma\})$, so $\hat P$ is fixed by $P$ alone.)

*$\hat P$ is a safety property.* Let $\neg \hat P(\sigma)$. Then some finite prefix has $M(\sigma[..i]) = \text{stop}$. Take any $\tau \in \Psi^\infty$ and the execution $\rho = \sigma[..i]\,\tau$. The prefix of $\rho$ of length $i$ is $\sigma[..i]$, so $M(\rho[..i]) = \text{stop}$ and $\neg \hat P(\rho)$. So the prefix $\sigma[..i]$ cannot be repaired by any continuation, which is the definition of safety. $\blacksquare$

The proof uses each hypothesis once. Hypothesis 1 makes the decision a function of the prefix, which gives the second part. Hypothesis 3 over all sets $\Sigma$, including singletons, gives the first part. Hypothesis 2 is what makes "stop" final: a monitor that could take back a decision, or replace an action, would not fit the definition of $M$.

## Consequences

- **Liveness and availability are out.** A liveness property has the feature that every finite sequence can be extended to an execution in the property (Alpern and Schneider 1985). If such a property is also a safety property, every execution is in it, so it is trivial. Hence no non-trivial liveness property is EM-enforceable. "Every request is eventually served" and "the service stays available" are of this kind. A bound such as "every request is served within 100 steps" is a safety property and is enforceable, since a run that breaks it does so at a finite step.
- **Noninterference is out.** [Noninterference](/noninterference/) compares runs. Take runs with a secret input $h$ and a public output: the set with the single run "$h = 0$, output 0" satisfies noninterference, and so does the set with the single run "$h = 1$, output 1", since there is nothing to compare. Their union does not. A property holds on a union when it holds on each part, so noninterference is not a property and no execution monitor enforces it. Monitors for information flow, such as no-sensitive-upgrade, therefore enforce a stronger safety property and also stop some secure runs; this is a consequence of the theorem, not a design flaw of one monitor.
- **What monitors are good for.** Access control decisions, the [Chinese wall](/chinese-wall-model/) policy, "no send after a file read", bounds on resources and the protocols of an interface ("open before read") are safety properties, written as [security automata](/security-automaton/). An [inline reference monitor](/inline-reference-monitor/) enforces them by putting the automaton inside the program.
- **Where to go beyond.** Static analysis can enforce policies that depend on all runs, such as noninterference via [security type systems](/security-type-system/) or [self-composition](/self-composition/). Monitors that can suppress or insert actions (edit automata) enforce some non-safety policies. Program rewriting is the strongest of the three in the classification of Hamlen, Morrisett and Schneider.

## Tightness

**The converse is false for computable monitors.** A monitor is a program, so $M$ must be computable. Let the actions be the natural numbers, read as codes $\langle T, x \rangle$ of a [Turing machine](/turing-machine/) $T$ and an input $x$. Let $\hat P(\sigma)$ say: no action of $\sigma$ is the code of a pair such that $T$ halts on $x$. This is a safety property: a bad execution contains a bad action at a finite position, and every extension keeps that action. Suppose a computable monitor $M$ enforced it. Hypothesis 3 on the one-action execution $\langle T, x \rangle$ says that $M$ stops it if and only if $T$ halts on $x$, so the program "run $M$ on $\varepsilon$ and on the one-action sequence $\langle T, x \rangle$" decides the halting problem, which is impossible. So this safety property is not EM-enforceable by any computable monitor. Hamlen, Morrisett and Schneider (2006) make this gap precise: with the computability constraint, every EM-enforceable policy is a co-recursively enumerable safety property, and some safety properties of that kind are still not enforceable.

**The converse is true without computability.** If $M$ may be any function, every safety property $\hat P$ is EM-enforceable. Let $M(\tau) = \text{stop}$ exactly when no execution in $\hat P$ has $\tau$ as a prefix. If $\hat P(\sigma)$, every prefix of $\sigma$ is a prefix of a member (namely $\sigma$), so the monitor lets $\sigma$ run in full. If $\neg \hat P(\sigma)$, safety gives a prefix $\sigma[..i]$ none of whose extensions is in $\hat P$, so $M(\sigma[..i]) = \text{stop}$. This is the same construction as the automaton of prefixes on the [security automaton](/security-automaton/) page. So, as a statement about the information a monitor has, the theorem is tight: safety is exactly what a run-by-run, stop-only observer can enforce, and computability is the only further loss.

**The hypotheses matter.** Drop hypothesis 2 and the class grows: edit automata (Ligatti, Bauer and Walker) enforce some properties that are not safety properties. Drop hypothesis 1 and let the monitor see all runs, and the mechanism becomes a static analysis. Weaken hypothesis 3 so that the monitor may also stop some good runs, and the policy actually enforced is a safety property that implies $P$, as in the information flow monitors above.

## History

The words safety and liveness for "nothing bad happens" and "something good eventually happens" go back to Lamport's work on concurrent programs in 1977. Alpern and Schneider gave the formal definitions in 1985 and proved that every property is the intersection of a safety property and a liveness property. Schneider's paper of 2000 defined the class EM of enforcement mechanisms that monitor a target and stop it, introduced security automata to describe the policies they enforce, and showed that an EM-enforceable policy must be a safety property; he noted that the condition is necessary and not sufficient. Viswanathan's thesis and the paper of Hamlen, Morrisett and Schneider (2006) added the computability constraint and compared monitors with static analysis and program rewriting. Ligatti, Bauer and Walker (2005, 2009) studied monitors that edit the action stream. Clarkson and Schneider (2010) placed noninterference among the hyperproperties, which explains in general why no monitor of single runs enforces it.

## References
