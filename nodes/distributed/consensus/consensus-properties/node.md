---
tag: 3DE9XP
kind: definition
slug: consensus-properties
name: Consensus correctness conditions (agreement, validity, termination)
aliases:
- agreement validity termination
area: distributed/consensus
level: intro
summary: The three safety and liveness requirements a consensus protocol must meet.
prereqs: [consensus-problem, safety-property, liveness-property]
see_also: [strong-validity, weak-validity, interactive-consistency, k-set-agreement, approximate-agreement, flp-impossibility, crash-failure, las-vegas-algorithm]
sources:
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 5, Section 5.1 (the weak validity condition of coordinated attack), Chapter 6, Section 6.1 (agreement, validity and termination for stopping failures, with validity as unanimity)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 5, Section 5.1 (termination, agreement and validity, with validity as unanimity)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luis Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 5 (regular consensus with termination, validity, integrity and agreement, and uniform consensus with uniform agreement)
  - paper: doi:10.1145/226643.226647
    title: Tushar Deepak Chandra and Sam Toueg, Unreliable failure detectors for reliable distributed systems, Journal of the ACM 43(2), 1996
    locator: pages 225 to 267 (consensus with termination, uniform integrity, agreement and uniform validity, where a decided value must have been proposed)
  - paper: doi:10.1145/3149.214121
    title: Michael J. Fischer, Nancy A. Lynch and Michael S. Paterson, Impossibility of distributed consensus with one faulty process, Journal of the ACM 32(2), 1985
    locator: pages 374 to 382 (partial correctness, with the non-triviality condition that both decision values are possible)
  - paper: doi:10.1016/0020-0190(85)90056-0
    title: Bowen Alpern and Fred B. Schneider, Defining liveness, Information Processing Letters 21(4), 1985
    locator: pages 181 to 185 (the formal definitions of safety and liveness properties)
---

A [consensus](/consensus-problem/) protocol is correct if every execution has four properties: agreement (no two decisions differ), validity (the decision is related to the inputs), integrity (each process decides at most once) and termination (every correct process decides). The first three are [safety properties](/safety-property/) and termination is a [liveness property](/liveness-property/). Validity is the condition that keeps consensus from being trivial, and different sources state it in different forms.

## Definition

There are $n$ processes. Each process $p_i$ has an input $v_i$ from a set $V$ of values, and it may *decide* a value by writing it once to an output. A process is *correct* if it never crashes in the execution, and *faulty* otherwise, as in the [crash-failure model](/crash-failure/).

**Agreement.** No two correct processes decide different values.

**Uniform agreement.** No two processes decide different values, whether they are correct or faulty.

**Integrity.** Every process decides at most once.

**Termination.** Every correct process eventually decides.

**Validity** has several forms.

| form | condition | used by |
|---|---|---|
| unanimity, or [strong validity](/strong-validity/) | if all processes start with the same value $v$, then $v$ is the only possible decision | Lynch, Section 6.1; Attiya and Welch, Section 5.1 |
| input validity | if a process decides $v$, then $v$ is the input of some process | Chandra and Toueg (1996), as *uniform validity*; Cachin, Guerraoui and Rodrigues, Chapter 5 |
| [weak validity](/weak-validity/) | if there are no faults and all inputs are $v$, then $v$ is the only possible decision | Lynch, Section 5.1, for coordinated attack; Byzantine agreement papers |
| non-triviality | each value of $\{0, 1\}$ is the decision of some execution | Fischer, Lynch and Paterson (1985) |
| external validity | the decision satisfies a predicate given by the application | asynchronous Byzantine protocols, for example for blocks of transactions |

For binary inputs, input validity and unanimity are the same: if all inputs are $v$, the only input is $v$. For larger $V$, input validity is stronger. In the Byzantine setting, "input" means the input of a correct process, see [strong validity](/strong-validity/).

**Consensus and uniform consensus.** Consensus asks for agreement, validity, integrity and termination; *uniform consensus* asks for uniform agreement instead of agreement. In the asynchronous model with a failure detector weaker than the perfect one, Guerraoui (1995) showed that every algorithm that solves consensus also solves uniform consensus: a process that decides cannot know whether it will crash later, so its decision must already agree with the decisions of the correct processes. In the synchronous model the two differ: early deciding consensus needs fewer rounds than uniform consensus.

**Which are safety and which are liveness.** By Alpern and Schneider (1985), a property is a *safety* property if every execution that violates it has a finite prefix after which every extension violates it, and a *liveness* property if every finite prefix can be extended to an execution that has it.

- *Agreement and uniform agreement are safety.* If an execution violates agreement, two processes have decided different values at some finite times. Take the prefix up to the later decision. Decisions are written once, so every extension still has the two different decisions.
- *Integrity is safety.* A violation is a second decision at a finite time, and it stays in every extension.
- *Each form of validity is safety.* A violation is a decision on a forbidden value at a finite time. The condition that makes the value forbidden depends only on the inputs, which are fixed at the start, and the decision stays in every extension. External validity is the same, since the predicate is fixed.
- *Termination is liveness.* Take any finite prefix. Extend it by steps in which every correct process that has not decided decides some value. The extension has termination. No finite prefix can show a violation, because a decision may still come later.

So a consensus algorithm must never take a wrong step, and must eventually take the right one. The [FLP impossibility](/flp-impossibility/) shows that in the asynchronous model the two demands cannot both be met deterministically with one crash.

**Why validity rules out the trivial protocol.** The protocol "every process decides 0 at once" has agreement, uniform agreement, integrity and termination, in every model and with any number of faults. It fails every form of validity: in the execution with all inputs 1 and no faults, it decides 0, which unanimity, input validity and weak validity forbid, and 1 is never decided, which non-triviality forbids. So without validity there is nothing to solve. Every impossibility proof for consensus uses validity, usually to get two initial configurations that must lead to different decisions.

## Examples and non-examples

- **Example: an execution that is correct.** Three processes have inputs 0, 1, 1. Process $p_1$ crashes before it decides, and $p_2$ and $p_3$ decide 1. Agreement holds, input validity holds, and termination holds because $p_1$ is faulty.
- **Non-example: agreement but not uniform agreement.** Process $p_1$ decides 0 and then crashes, while $p_2$ and $p_3$ decide 1. Agreement holds, because $p_1$ is faulty, but uniform agreement fails. If $p_1$ had acted on its decision, for example by committing a transaction, the system is now inconsistent; this is why replicated systems use uniform agreement.
- **Non-example: unanimity but not input validity.** With $V = \{0, 1, 2\}$, inputs 0, 1, 1 and decision 2, unanimity holds because the inputs are not all equal, but input validity fails.
- **Non-example: termination for only some processes.** In the FLP paper, a protocol must make only *some* process decide. This is weaker than termination, which makes the impossibility result stronger.
- **Non-example: termination with probability 1.** [Ben-Or's algorithm](/ben-or-consensus/) has every safety property in every execution, but terminates only with probability 1. There are executions, of probability 0, in which it runs for ever. Such an algorithm is of the [Las Vegas](/las-vegas-algorithm/) kind.

## Related definitions

- **[Interactive consistency](/interactive-consistency/).** All correct processes agree on a vector with one entry per process, and the entry of each correct process is its input.
- **[$k$-set agreement](/k-set-agreement/).** Agreement is weakened to "at most $k$ different values are decided".
- **[Approximate agreement](/approximate-agreement/).** Agreement is weakened to "decisions are within $\varepsilon$ of each other", with validity "decisions lie within the range of the inputs".
- **[Atomic commit](/atomic-commit/).** The decision is commit or abort, and validity says that commit needs all votes to be yes, and abort needs a no vote or a failure.
- **Byzantine forms.** With [Byzantine failures](/byzantine-failure-model/), all conditions talk only about correct processes, and validity must use their inputs, since faulty processes can claim any input.

## References
