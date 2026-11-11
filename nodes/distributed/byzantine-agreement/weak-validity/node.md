---
tag: T3PNQR
kind: definition
slug: weak-validity
name: Weak validity
aliases:
- weak Byzantine agreement validity
- weak unanimity
area: distributed/byzantine-agreement
level: core
summary: In Byzantine consensus, if no process is faulty and all inputs are v, every process must decide v. Runs with a fault are not constrained.
prereqs: [strong-validity]
see_also: [byzantine-broadcast, authenticated-resilience-bound, byzantine-resilience-bound, byzantine-round-lower-bound, interactive-consistency, dolev-strong-algorithm, consensus-properties, consensus-problem]
sources:
  - paper: doi:10.1145/2402.322398
    title: Leslie Lamport, The Weak Byzantine Generals Problem, Journal of the ACM 30(3), 1983
    locator: pages 668 to 676 (the weak form of the problem, which constrains the value only when all processes are nonfaulty)
  - paper: doi:10.1007/BF01843568
    title: Michael J. Fischer, Nancy A. Lynch and Michael Merritt, Easy impossibility proofs for distributed consensus problems, Distributed Computing 1(1), 1986
    locator: the section on weak agreement (the bound n >= 3t + 1 also holds for the weak problem)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 5 (weak Byzantine consensus with weak validity, and strong Byzantine consensus)
  - paper: doi:10.1137/0212045
    title: Danny Dolev and H. Raymond Strong, Authenticated algorithms for Byzantine agreement, SIAM Journal on Computing 12(4), 1983
    locator: pages 656 to 666 (authenticated broadcast for any number of faults, which gives weak validity for any t < n)
---

Weak validity is the validity condition of Byzantine consensus that applies only when nothing goes wrong: if no process is faulty and all processes have the same input $v$, then every process decides $v$. In a run with even one faulty process it asks nothing, so the correct processes may agree on any value. Lamport introduced the weak form of the Byzantine generals problem in 1983. It is weaker than [strong validity](/strong-validity/), and with signatures this makes a real difference: weak validity is solvable for any number of faults $t < n$, but strong validity needs $n > 2t$. Without signatures both need $n > 3t$.

## Definition

Each process $p$ has an input $x_p$ from a set $V$ of values, and each correct process decides a value.

**Weak validity.** If no process is faulty and $x_p = v$ for every process $p$, then every process decides $v$.

The condition only constrains failure-free runs with equal inputs. In every other run, any common decision is allowed, together with agreement and termination. So weak validity mainly rules out the trivial algorithm that always decides a fixed value.

**Comparison with strong validity.** Strong validity says: if all *correct* processes have input $v$, every correct process decides $v$, in every run with at most $t$ faults. In a failure-free run the two conditions say the same thing. They differ only in runs with faults:

- with a fault and equal correct inputs, strong validity forces the common input, and weak validity allows anything;
- so every algorithm with strong validity has weak validity, and not the other way round.

**The broadcast form.** Lamport's weak Byzantine generals problem relaxes the generals problem in the same way: the loyal generals must agree, and their value is constrained only when all generals are loyal. The consensus form above and the broadcast form give each other with at most one extra round.

## Examples and non-examples

- **Example: decide the broadcast of $p_0$.** All processes run [Byzantine broadcast](/byzantine-broadcast/) with sender $p_0$ and decide its output. Agreement comes from broadcast. If no process is faulty and all inputs are $v$, then $p_0$ is correct with input $v$, and every process decides $v$. With the [Dolev-Strong algorithm](/dolev-strong-algorithm/) this works for any $t < n$. The implementation checks it for $n = 4$ and every faulty set of up to 3 processes on all 16 binary inputs.
- **Example: a run that separates the two conditions.** With $n = 4$, $t = 1$, process 0 faulty with input 1 and processes 1, 2, 3 correct with input 0, the "broadcast of $p_0$" algorithm decides 1. This satisfies weak validity, since a process is faulty, and breaks strong validity, since all correct inputs are 0. The algorithm that decides the majority of [interactive consistency](/interactive-consistency/) decides 0 in the same run, and it satisfies both conditions.
- **Example: any strong algorithm.** [OM(m)](/oral-messages-algorithm/) applied to every input, followed by a majority vote, satisfies strong validity for $n > 3t$, so it also satisfies weak validity.
- **Non-example: always decide 0.** Agreement and termination hold, but in the failure-free run with all inputs 1 the decision is 0. This breaks weak validity.
- **Non-example: decide your own input.** Weak validity holds in failure-free runs with equal inputs, but agreement fails when the inputs differ.

## Related definitions

- **[Strong validity](/strong-validity/).** The same conclusion for the correct processes in every run.
- **Bounds without signatures.** Weak validity does not lower the number of processes: Fischer, Lynch and Merritt show that the weak problem needs $n \ge 3t + 1$ too, see the [Byzantine resilience bound](/byzantine-resilience-bound/).
- **Bounds with signatures.** Weak validity is solvable for any $t < n$, and strong validity only for $n > 2t$. See the [authenticated resilience bound](/authenticated-resilience-bound/).
- **Rounds.** Weak validity does not save rounds. The proof of the [Byzantine round lower bound](/byzantine-round-lower-bound/) needs validity only in failure-free runs, so $t + 1$ rounds are needed for weak validity as well.
- **Crash validity.** For crash failures, the [consensus properties](/consensus-properties/) page uses unanimity over all inputs, which crashed processes do not falsify. Weak validity is the Byzantine form that keeps only the failure-free case.
- **External validity.** In blockchain protocols, the decision must satisfy a public predicate, such as "the block is signed and its transactions are valid". This is a different kind of condition and does not refer to the inputs at all.

## References
