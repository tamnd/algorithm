---
tag: 69GK5B
kind: definition
slug: strong-validity
name: Strong validity
aliases:
- strong unanimity
area: distributed/byzantine-agreement
level: core
summary: In Byzantine consensus, if all correct processes have the same input v, every correct process must decide v. Faulty inputs do not count.
prereqs: [consensus-properties, byzantine-failure-model]
see_also: [weak-validity, interactive-consistency, authenticated-resilience-bound, byzantine-resilience-bound, approximate-agreement, phase-king-algorithm, byzantine-broadcast, consensus-problem]
sources:
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 6, Section 6.3 (the validity condition of Byzantine agreement, stated for nonfaulty processes)
  - paper: doi:10.1016/0020-0190(94)90055-8
    title: Gil Neiger, Distributed consensus revisited, Information Processing Letters 49(4), 1994
    locator: pages 195 to 201 (strong consensus, in which the decision is the input of a correct process, needs n > max(3t, mt) for m values)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 5 (weak and strong Byzantine consensus, where strong validity allows a special value when correct inputs differ)
  - paper: doi:10.4230/LIPIcs.OPODIS.2015.22
    title: David Stolz and Roger Wattenhofer, Byzantine Agreement with Median Validity, OPODIS 2015
    locator: Sections 1 and 2 (median validity, a decision close to the median of the correct inputs)
  - paper: doi:10.1145/2484239.2484256
    title: Nitin H. Vaidya and Vijay K. Garg, Byzantine vector consensus in complete graphs, PODC 2013
    locator: Sections 1 to 3 (the decision vector must lie in the convex hull of the correct input vectors)
  - paper: doi:10.1145/2488608.2488657
    title: Hammurabi Mendes and Maurice Herlihy, Multidimensional approximate agreement in Byzantine asynchronous systems, STOC 2013
    locator: Section 1 (outputs in the convex hull of the correct inputs, approximate version)
---

Strong validity is the validity condition of Byzantine consensus that refers only to the correct processes: if all correct processes have the same input $v$, then every correct process decides $v$. The inputs of faulty processes do not count, because a faulty process can claim any input. It is the condition that makes consensus useful when processes may lie, and it is also the condition that makes consensus need more processes than [Byzantine broadcast](/byzantine-broadcast/). With signatures, broadcast works for any $t < n$, but consensus with strong validity needs $n > 2t$.

## Definition

Each process $p$ has an input $x_p$ from a set $V$ of values, and each correct process decides a value. Let $C$ be the set of correct processes in a run.

**Strong validity.** If $x_p = v$ for every $p \in C$, then every $p \in C$ decides $v$.

This is the condition of Lynch, Section 6.3, and it is sometimes called *strong unanimity*. When the correct inputs differ, it allows any decision, even a value that no process had as input. It says nothing about the inputs of faulty processes, and it holds in every run with at most $t$ faults, not only in runs without faults. That last point is what separates it from [weak validity](/weak-validity/), which asks for the same conclusion only when no process is faulty.

**Stronger forms.**

- **Correct-input validity.** Every correct decision is the input of some correct process. Neiger (1994) calls consensus with this condition *strong consensus*. It implies strong validity. For binary values the two conditions are the same: if the correct inputs differ, both 0 and 1 are correct inputs. For $|V| = m$ values, strong consensus in the synchronous model needs $n > \max(3t, mt)$: with $mt$ processes or fewer, each value may be held by at most $t$ processes, so for each value the processes that hold it might all be faulty.
- **Strong validity with a special value.** Cachin, Guerraoui and Rodrigues define strong validity so that, when the correct inputs differ, a correct process may decide the input of some correct process or a special value $\square$ that means "no agreement on a correct input".
- **Median validity.** For ordered values, Stolz and Wattenhofer (2015) ask that the decision is close to the median of the correct inputs, in the sense of the number of correct inputs on each side.
- **Convex validity.** For real values or vectors, the decision must lie in the convex hull of the correct inputs. Vaidya and Garg (2013) and Mendes and Herlihy (2013) study this for vectors in $d$ dimensions, where it needs more processes as $d$ grows. For $d = 1$ it says that the decision lies between the smallest and the largest correct input, as in [approximate agreement](/approximate-agreement/).

## Examples and non-examples

- **Example: majority of a common vector.** With $n > 2t$, the processes run [interactive consistency](/interactive-consistency/) and decide the majority of the vector. If all correct inputs are $v$, at least $n - t > n/2$ entries are $v$. This satisfies strong validity. The implementation checks it for $n = 5$ and $t = 2$ on all 32 binary inputs and all faulty sets of size at most 2.
- **Example: phase king.** The [phase king algorithm](/phase-king-algorithm/) satisfies strong validity for $n > 3t$: if all correct processes start with $v$, they keep $v$ in every phase, whatever the king says.
- **Non-example: broadcast of one process.** Deciding the value broadcast by process $p_0$ fails when $p_0$ is faulty. With $n = 4$, $t = 1$, $p_0$ faulty with input 1 and all correct inputs 0, the implementation decides 1. All correct inputs are 0, so strong validity fails. Weak validity holds, since a process is faulty. The majority rule decides 0 in the same run.
- **Non-example: majority with $n \le 2t$.** With $n = 4$, $t = 2$, inputs $(0, 0, 1, 1)$ and processes 0 and 1 faulty but acting correctly, the vector has no majority, and the implementation decides the default 0 at processes 2 and 3, whose inputs are both 1. No algorithm does better: the [authenticated resilience bound](/authenticated-resilience-bound/) shows that strong validity is impossible for $n \le 2t$.
- **Non-example: validity over all inputs.** "If all inputs are $v$, decide $v$", where faulty inputs count, is not strong validity. A faulty process can act as if it had any input, so its input is not a meaningful part of the run. This form is used for crash failures, not for Byzantine ones.

## Related definitions

- **[Weak validity](/weak-validity/).** The same conclusion, but only in runs without faults. It is solvable with signatures for any $t < n$.
- **Validity for crash faults.** The [consensus properties](/consensus-properties/) page states validity for crash failures, where a decision must be some process's input. Crashed processes do not lie about inputs, so that form is natural there.
- **Validity of broadcast.** In [Byzantine broadcast](/byzantine-broadcast/), validity is about one input: if the sender is correct, every correct process outputs its value. Consensus with strong validity gives broadcast, and broadcast gives consensus with strong validity when $n > 2t$.
- **Bounds.** Without signatures, consensus with strong validity needs $n > 3t$, by the [Byzantine resilience bound](/byzantine-resilience-bound/). With signatures it needs $n > 2t$. Correct-input validity needs $n > \max(3t, mt)$.

## References
