---
tag: EXNMQY
kind: theorem
slug: authenticated-resilience-bound
name: Authenticated resilience bound
aliases:
- authenticated t < n bound
- honest majority bound for authenticated consensus
area: distributed/byzantine-agreement
level: advanced
summary: "With signatures, Byzantine broadcast is solvable for any t < n faults, but consensus with strong validity is solvable if and only if n > 2t."
prereqs: [signed-messages-model, dolev-strong-algorithm, strong-validity]
see_also: [byzantine-resilience-bound, signed-messages-algorithm, interactive-consistency, weak-validity, byzantine-round-lower-bound, dolev-reischuk-lower-bound, partial-synchrony, digital-signature]
sources:
  - paper: doi:10.1145/357172.357176
    title: Leslie Lamport, Robert Shostak and Marshall Pease, The Byzantine Generals Problem, ACM Transactions on Programming Languages and Systems 4(3), 1982
    locator: Section 4 (with signed messages, SM(m) solves the problem for any number of traitors, Theorem 2)
  - paper: doi:10.1145/322186.322188
    title: Marshall Pease, Robert Shostak and Leslie Lamport, Reaching Agreement in the Presence of Faults, Journal of the ACM 27(2), 1980
    locator: pages 228 to 234 (with authenticated messages, interactive consistency for any n >= m >= 0)
  - paper: doi:10.1137/0212045
    title: Danny Dolev and H. Raymond Strong, Authenticated algorithms for Byzantine agreement, SIAM Journal on Computing 12(4), 1983
    locator: pages 656 to 666 (authenticated Byzantine agreement for any number of faults in t + 1 phases, with polynomial messages)
  - url: https://eprint.iacr.org/2002/053
    title: Matthias Fitzi, Extended Validity and Consistency in Byzantine Agreement, IACR Cryptology ePrint Archive 2002/053
    locator: Section 1 (with signatures, broadcast is possible for t < n and consensus for t < n/2, and both bounds are tight)
  - paper: doi:10.1145/42282.42283
    title: Cynthia Dwork, Nancy Lynch and Larry Stockmeyer, Consensus in the presence of partial synchrony, Journal of the ACM 35(2), 1988
    locator: Section 1, Table 1 (authenticated Byzantine faults still need n >= 3t + 1 in partial synchrony)
---

Signatures move the resilience bound of Byzantine agreement, but by different amounts for different problems. In the synchronous [signed messages model](/signed-messages-model/), [Byzantine broadcast](/byzantine-broadcast/) and [interactive consistency](/interactive-consistency/) are solvable for any number of faults $t < n$, for example by the [Dolev-Strong algorithm](/dolev-strong-algorithm/). Consensus with [weak validity](/weak-validity/) is also solvable for any $t < n$. But consensus with [strong validity](/strong-validity/) is solvable if and only if $n > 2t$, and the lower bound holds for every algorithm, with or without signatures. Without signatures, all of these problems need $n > 3t$, by the [Byzantine resilience bound](/byzantine-resilience-bound/).

## Statement

**Model.** There are $n$ processes on a complete network of reliable links in the [synchronous model](/synchronous-model/). Each process has a signing key, and every process knows every verification key. Signatures are unforgeable: no process can produce a signature of a correct process on a message that the correct process did not sign. Up to $t$ processes are [Byzantine](/byzantine-failure-model/) and act together, with a static adversary.

**Theorem.**

1. *(Broadcast.)* For every $n \ge 1$ and $0 \le t < n$, Byzantine broadcast is solvable, in $t + 1$ rounds. So is interactive consistency.
2. *(Weak validity.)* For every $0 \le t < n$, consensus with agreement, weak validity and termination is solvable.
3. *(Strong validity.)* Let $t \ge 1$ and $n \ge 2$. Consensus with agreement, strong validity and termination is solvable if and only if $n > 2t$. The "only if" part holds for every algorithm, deterministic or randomized, with or without signatures, in every timing model.

Strong validity here is the unanimity form: if all correct processes have the same input $v$, every correct decision is $v$.

## In plain words

A signature lets a process prove what another process said. A liar can still say different things to different processes, but it cannot invent words for an honest process. That is enough for one sender to spread one value to everyone, however many processes lie.

Consensus is a different task. Every process starts with its own value, and if all honest processes start with the same value, they must end with it. Now suppose half of the processes start with 0 and the other half with 1. Each half could be the honest one, and the other half could be liars that just follow the rules. Nobody can tell which half is honest, so nobody knows which value is required. No signature can help, because nobody lies at all.

## Proof

The full proof is below. This section gives its structure.

**Broadcast for any $t < n$.** The Dolev-Strong algorithm solves broadcast in $t + 1$ rounds for any $t < n$. A value counts in round $r$ only if it carries $r$ distinct valid signatures, the first of them by the sender. If a correct process accepts a value in round $r \le t$, it signs and relays it, so every correct process accepts it by round $r + 1$. A value accepted in round $t + 1$ carries $t + 1$ signatures, so a correct process signed it earlier, and every correct process has it. The proof is on the [Dolev-Strong page](/dolev-strong-algorithm/). [SM(m)](/signed-messages-algorithm/) of Lamport, Shostak and Pease also works for any $t < n$. Run $n$ instances in parallel, one per sender, and the result is interactive consistency.

**Weak validity for any $t < n$.** All processes decide the value that process $p_0$ broadcasts. Agreement comes from the agreement of broadcast. If no process is faulty and all inputs are $v$, then $p_0$ is correct with input $v$, and the validity of broadcast gives $v$.

**Strong validity for $n > 2t$.** Run interactive consistency, and decide the strict majority of the vector, or a fixed default if there is none. All correct processes have the same vector, so they decide the same value. If all correct processes have input $v$, at least $n - t$ entries of the vector are $v$, and $n - t > n/2$, so the majority is $v$.

**No strong validity for $n \le 2t$.** Split the processes into two nonempty sets $A$ and $B$ with $|A| \le t$ and $|B| \le t$. Look at one run in which $A$ has input 0, $B$ has input 1, and every process follows the algorithm.

- Read this run as one in which the processes of $B$ are faulty but behave correctly. They use only their own keys, so signatures do not detect them. All correct processes have input 0, so strong validity makes every process of $A$ decide 0.
- Read the same run with $A$ as the faulty set. Then every process of $B$ decides 1.
- But in this run no process is faulty, and agreement fails.

The implementation shows this case. It runs interactive consistency with $n$ parallel Dolev-Strong instances and decides the majority. For $n = 5$ and $t = 2$, it reaches agreement and strong validity on all 32 binary inputs, for every faulty set of size at most 2 and three attack strategies. For $n = 4$ and $t = 2$, with inputs $(0, 0, 1, 1)$ and processes 0 and 1 faulty but acting correctly, the vector is $(0, 0, 1, 1)$. It has no majority, so the correct processes 2 and 3 decide the default 0, although both have input 1.

## Consequences

- **Broadcast and consensus differ.** With oral messages the two problems are equivalent for $n > 3t$, and both need $n > 3t$. With signatures, broadcast is solvable for any $t < n$, but consensus with strong validity only for $n > 2t$. Consensus is made from broadcast by broadcasting all inputs and taking the majority, and that majority is the step that needs $n > 2t$.
- **The validity condition matters.** Weak validity asks for nothing in runs with a fault, so for $t \ge n/2$ it is solvable when strong validity is not. The implementation shows one run that separates them. With $n = 4$, $t = 1$, process 0 faulty with input 1 and all correct inputs 0, the "decide the broadcast of $p_0$" algorithm decides 1. That satisfies weak validity and breaks strong validity. The majority algorithm decides 0 in the same run.
- **Signatures help only with synchrony.** In [partial synchrony](/partial-synchrony/), Dwork, Lynch and Stockmeyer show that Byzantine consensus needs $n \ge 3t + 1$ even with signatures. In the [asynchronous model](/asynchronous-model/), no deterministic algorithm solves consensus even with one crash, by [FLP](/flp-impossibility/).
- **Rounds do not improve.** Signatures do not beat the [round lower bound](/byzantine-round-lower-bound/): $t + 1$ rounds are still needed in the worst case, since crash faults already force them.
- **Cost.** With signatures, the number of signatures and messages is still $\Omega(nt)$ and $\Omega(n + t^2)$ in the worst case, by the [Dolev-Reischuk lower bound](/dolev-reischuk-lower-bound/).

## Tightness

All three parts are exact. Part 1 needs no condition on $t$ at all. For $t = n$ there is no correct process, and the problem is empty. Part 3 is solved at $n = 2t + 1$ by the majority of interactive consistency in $t + 1$ rounds. With randomization, Katz and Koo (2006) give authenticated Byzantine agreement for $t < n/2$ in an expected constant number of rounds.

The bound in part 3 depends on the form of validity. A stronger form asks that the decision is the input of some correct process. For binary values the two forms are the same, but for $m > 2$ values the stronger form needs more processes. The [strong validity](/strong-validity/) page gives the bounds.

## History

Pease, Shostak and Lamport (1980) showed that with authenticated messages, interactive consistency is possible for any number of faults. Lamport, Shostak and Pease (1982) gave the signed messages algorithm SM(m) for broadcast with any number of traitors. Dolev and Strong (1983) gave a version with polynomial messages and the $t + 1$ round lower bound. The $n > 2t$ bound for consensus with strong validity is a short folklore argument. It appears in the survey part of many papers, for example in Fitzi (2002), which gives the bounds for broadcast and consensus side by side.

## References
