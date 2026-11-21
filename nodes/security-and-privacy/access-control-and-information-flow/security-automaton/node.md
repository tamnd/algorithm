---
tag: MN9D48
kind: model
slug: security-automaton
name: Security automaton
aliases:
- Schneider security automaton
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: An automaton that watches the actions of a program and halts it on the first action that would break the policy.
model: word-ram
prereqs: [safety-property, deterministic-finite-automaton, reference-monitor]
see_also: [em-enforceable-policies-theorem, inline-reference-monitor, buchi-automaton, linear-temporal-logic, chinese-wall-model, access-control-matrix, hyperproperty, noninterference]
sources:
  - paper: doi:10.1145/353323.353382
    title: Fred B. Schneider, Enforceable security policies, ACM Transactions on Information and System Security 3(1), 2000
    locator: pp. 30 to 50, the definition of execution monitoring, the definition of security automata and their use as monitors, and the proof that every policy an execution monitor enforces is a safety property
  - paper: doi:10.1145/1111596.1111601
    title: Kevin W. Hamlen, Greg Morrisett and Fred B. Schneider, Computability classes for enforcement mechanisms, ACM Transactions on Programming Languages and Systems 28(1), 2006
    locator: pp. 175 to 205, the computability constraints on execution monitors, static analysis and program rewriting, and the taxonomy of enforceable policies
  - paper: doi:10.1007/s10207-004-0046-8
    title: Jay Ligatti, Lujo Bauer and David Walker, Edit automata, enforcement mechanisms for run-time security policies, International Journal of Information Security 4(1-2), 2005
    locator: pp. 2 to 16, truncation, suppression, insertion and edit automata and the policies each can enforce
  - paper: doi:10.1145/1455526.1455532
    title: Jay Ligatti, Lujo Bauer and David Walker, Run-time enforcement of nonsafety policies, ACM Transactions on Information and System Security 12(3), 2009
    locator: the renewal properties that edit automata enforce, which include policies that are not safety properties
  - paper: doi:10.1016/0020-0190(85)90056-0
    title: Bowen Alpern and Fred B. Schneider, Defining liveness, Information Processing Letters 21(4), 1985
    locator: pp. 181 to 185, the definitions of safety and liveness properties of executions
---

A security automaton is the formal model of what a run-time monitor can enforce. Fred Schneider defined it in 2000 as a possibly infinite, possibly nondeterministic automaton that reads the actions of a target program one at a time and moves to a new set of states; when the set becomes empty, the monitor stops the target before the offending action runs. Every policy written as a security automaton is a [safety property](/safety-property/), and every safety property over a countable set of actions can be written as one. The [reference monitor](/reference-monitor/) is the concept of a mediator that checks every access, the [inline reference monitor](/inline-reference-monitor/) is one way to implement it by rewriting the program, and the security automaton is the mathematical object both of them run.

## The machine

**States and transitions.** A security automaton has
- a countable set $Q$ of states,
- a set $Q_0 \subseteq Q$ of initial states,
- a countable set $I$ of input symbols, the security-relevant actions of the target (for example "read a file", "send a message", "call a method with these arguments"),
- a transition function $\delta : Q \times I \to 2^Q$.

The automaton is not required to be finite or deterministic. There are no accepting states: every state is good, and a missing transition is how the automaton says no. In the figures of Schneider's paper, the edges are labeled by predicates on the input symbols, so one edge can stand for many symbols.

**Runs.** The automaton keeps the set $Q'$ of states it may be in. It starts with $Q' = Q_0$. On the input symbol $s$, it moves to $\bigcup_{q \in Q'} \delta(q, s)$. If this set is empty, the input is rejected at $s$. A finite or infinite sequence is accepted when it is never rejected. This is the usual subset simulation of a nondeterministic automaton, done one step at a time.

**Use as a monitor.** As a monitor, the automaton gets each action of the target before the action runs, and it either lets the action run or stops the target:

```pseudo id=main
MONITOR(Q0, δ, actions s1 s2 s3 ...)
L1  Q′ ← Q0
L2  for i ← 1, 2, 3, ... while the target runs do
L3      N ← union of δ(q, si) over all q in Q′
L4      if N = ∅ then stop the target before si runs; return i
L5      Q′ ← N;  let si run
L6  return accept                         ▷ the target ended and every action was allowed
```

The monitor sees only the actions of the current run, and only those so far. It cannot look ahead, cannot see other runs, and cannot change an action. Its only power is to stop the target. These limits are what the [EM-enforceable policies theorem](/em-enforceable-policies-theorem/) uses.

**Example.** The policy "no message is sent after a file is read" over the actions read, send and other has two states, clean and tainted, with $Q_0 = \{\text{clean}\}$. From clean, read goes to tainted, and send and other stay in clean. From tainted, read and other stay in tainted, and send has no transition. On the run other, send, read, other, send, send:

| step | action | $Q'$ before | next set | decision |
| --- | --- | --- | --- | --- |
| 1 | other | {clean} | {clean} | allow |
| 2 | send | {clean} | {clean} | allow |
| 3 | read | {clean} | {tainted} | allow |
| 4 | other | {tainted} | {tainted} | allow |
| 5 | send | {tainted} | $\emptyset$ | stop before step 5 |

The sixth action never happens. The implementation of this page returns the index of the stopped action and is tested against the policy written directly as a predicate on all 3280 traces of length at most 7.

**A larger state space.** The [Chinese wall](/chinese-wall-model/) policy, "after a consultant reads data of one company, it may not read data of a competitor", is a security automaton whose state is the set of companies read so far. A policy such as "at most $k$ failed logins" needs $k + 1$ states. A policy such as "no more sends than receives" needs a counter, so its automaton has a countably infinite set of states. This is allowed by the definition.

## What it counts

The model decides one thing: whether a finite sequence of actions is allowed, that is, whether it is a prefix of an accepted sequence. The set of accepted sequences has two features that every policy in the model shares:
- **Prefix closed.** If a sequence is accepted, every prefix of it is accepted, because a run that is never rejected is also not rejected on a shorter input.
- **Closed under limits.** An infinite sequence is accepted when all its finite prefixes are accepted. Rejection always happens at a finite step.

Together these say that the set of accepted infinite sequences is a safety property in the sense of [Alpern and Schneider](/safety-property/): a sequence is bad exactly when some finite prefix of it is already bad, and no extension can repair that prefix.

The cost of the monitor is the work per action. For an automaton with a finite state set, step L3 costs $O(|Q| \cdot d)$ set operations, where $d$ bounds the number of next states of one transition, and the memory is $O(|Q|)$ for the set $Q'$. A deterministic automaton keeps one state and costs one lookup per action. The overhead in practice depends on how many actions are security-relevant and on how the check is placed in the program. The [inline reference monitor](/inline-reference-monitor/) page covers that.

## Relation to other models

- **Finite automata.** A security automaton with a finite state set and a finite alphabet is a nondeterministic finite automaton in which every state is accepting. Its language of finite words is a prefix-closed regular language, and the subset construction turns it into a [deterministic finite automaton](/deterministic-finite-automaton/) with one dead state for rejection.
- **Büchi automata.** On infinite inputs it is a [Büchi automaton](/buchi-automaton/) in which every state is accepting, so a run is accepting if and only if it is infinite. Such automata recognize exactly the closed (safety) regular languages of infinite words. A Büchi automaton with some non-accepting states can express liveness, such as "the lock is eventually released", which no security automaton can. A safety formula of [linear temporal logic](/linear-temporal-logic/) can be compiled into a security automaton.
- **Access control models.** A static [access control matrix](/access-control-matrix/) is a security automaton with one state, in which each allowed access is a self-loop and each forbidden access has no transition. History-based policies, such as the Chinese wall, need more states.
- **Reference monitor.** The reference monitor is the requirement that a mediator checks every access, cannot be bypassed and cannot be tampered with. The security automaton says what such a mediator can decide when it sees only the current run.
- **Edit automata.** Ligatti, Bauer and Walker extend the model with monitors that can suppress an action or insert actions of their own, not only stop the target. Edit automata can enforce policies that are not safety properties, so they fall outside the theorem below.
- **Hyperproperties.** [Noninterference](/noninterference/) relates pairs of runs, so it is a [hyperproperty](/hyperproperty/) and not a set of runs. No security automaton can express it, because the automaton reads a single run.

## Known results in the model

- **Every EM-enforceable policy is a safety property** (theorem, Schneider 2000). The adversary is a target program that may produce any sequence of actions; the monitor sees each action before it runs and can only stop the target. The proof and its exact hypotheses are on the page [EM-enforceable policies theorem](/em-enforceable-policies-theorem/).
- **Every safety property is a security automaton** (theorem). Let $I$ be countable and let $P$ be a safety property. Take as states the finite sequences $\sigma$ that are prefixes of some member of $P$, with $Q_0 = \{\varepsilon\}$ and $\delta(\sigma, s) = \{\sigma s\}$ when $\sigma s$ is such a prefix and $\emptyset$ otherwise. The state set is countable because $I^*$ is. The automaton accepts a sequence exactly when all its finite prefixes are prefixes of members of $P$, and since $P$ is a safety property, that is exactly membership in $P$. So security automata express exactly the safety properties.
- **Expressible is not enforceable** (theorem, Hamlen, Morrisett and Schneider 2006). A monitor is a program, so its transition function must be computable. With this constraint, a policy that an execution monitor enforces is a co-recursively enumerable property as well as a safety property, and there are safety properties that no computable monitor enforces. The same paper shows that statically enforceable policies are the recursively decidable properties of programs, and that program rewriting, the basis of inline monitors, can enforce policies that no execution monitor enforces.
- **More power, more policies** (theorem, Ligatti, Bauer and Walker 2005 and 2009). Monitors that can insert and suppress actions enforce a larger class than truncation monitors, which includes the renewal properties, some of which are not safety properties.
- **Not hyperproperties.** No set of runs equals noninterference, so neither a security automaton nor any monitor that decides one run at a time enforces it in general. Monitors for information flow either over-approximate (they also stop some secure runs) or change the execution itself, as [secure multi-execution](/secure-multi-execution/) does by running the program once for each security level.

## References
