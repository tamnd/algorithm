---
tag: QEVP9G
kind: theorem
slug: byzantine-round-lower-bound
name: Byzantine round lower bound
aliases:
- t+1 round lower bound
- Fischer-Lynch lower bound
area: distributed/byzantine-agreement
level: advanced
summary: "Deterministic synchronous Byzantine broadcast or consensus with t faults, t <= n - 2, needs t + 1 rounds in some run, with or without signatures."
prereqs: [consensus-round-lower-bound, byzantine-broadcast]
see_also: [oral-messages-algorithm, dolev-strong-algorithm, signed-messages-algorithm, byzantine-resilience-bound, authenticated-resilience-bound, weak-validity, crash-failure, feldman-micali-byzantine-agreement]
sources:
  - paper: doi:10.1016/0020-0190(82)90033-3
    title: Michael J. Fischer and Nancy A. Lynch, A lower bound for the time to assure interactive consistency, Information Processing Letters 14(4), 1982
    locator: pages 183 to 186 (t + 1 rounds are necessary for interactive consistency with t Byzantine processes)
  - paper: doi:10.1137/0212045
    title: Danny Dolev and H. Raymond Strong, Authenticated algorithms for Byzantine agreement, SIAM Journal on Computing 12(4), 1983
    locator: pages 656 to 666 (the t + 1 phase lower bound, which holds no matter what message types or protocols are allowed)
  - paper: doi:10.1016/S0020-0190(99)00100-3
    title: Marcos K. Aguilera and Sam Toueg, A simple bivalency proof that t-resilient consensus requires t + 1 rounds, Information Processing Letters 71(3-4), 1999
    locator: pages 155 to 158 (the bivalence proof for crash failures, used here through the reduction)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 6, Section 6.7 (the number of rounds, proved for stopping failures, so also for Byzantine failures)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 5, Section 5.1 (the lower bound of f + 1 rounds for crash failures, which carries over to Byzantine failures)
---

In the synchronous model, every deterministic algorithm for [Byzantine broadcast](/byzantine-broadcast/) or Byzantine consensus that tolerates $t$ faults, with $1 \le t \le n - 2$, has a run in which some correct process has not decided after $t$ rounds. This holds with or without signatures, and for weak as well as strong validity. The proof is a reduction: a crash is one kind of Byzantine behavior, so the [round lower bound for crash failures](/consensus-round-lower-bound/) applies. Fischer and Lynch proved the bound for Byzantine faults in 1982, and Dolev and Strong showed in 1983 that it holds "no matter what message types or protocols are allowed".

## Statement

**Model.** There are $n$ processes on a complete network of reliable links in the [synchronous model](/synchronous-model/). Up to $t$ processes are [Byzantine](/byzantine-failure-model/). Messages may be oral or signed: the theorem holds in the [oral messages model](/oral-messages-model/) and in the [signed messages model](/signed-messages-model/).

**Theorem.** Let $1 \le t \le n - 2$. Let $A$ be a deterministic algorithm that solves one of these problems with at most $t$ Byzantine faults:

1. Byzantine broadcast (agreement, validity for a correct sender, termination);
2. binary consensus with agreement, [weak validity](/weak-validity/) and termination;
3. binary consensus with agreement, [strong validity](/strong-validity/) and termination.

Then $A$ has a run with at most $t$ faulty processes, all of which fail by crashing, in which some correct process has not decided at the end of round $t$. So $A$ needs $t + 1$ rounds in the worst case.

The same holds for [interactive consistency](/interactive-consistency/) and for larger sets of values, since those problems give binary broadcast or consensus with the same number of rounds.

## In plain words

A liar can do anything, and one of the things it can do is to stop. So a protocol that survives liars must also survive processes that stop, and it can be no faster than the best protocol for processes that stop. For those, it is known that $t$ faults force $t + 1$ rounds: each round the adversary stops one more process just after it told something to only some of the others, and the doubt is never fully removed in $t$ rounds.

Signatures do not change this. A process that stops never signs anything false, so there is nothing for a signature to catch.

## Proof

The full proof is below. This section gives its structure.

**Crash faults are Byzantine faults.** A Byzantine process may send any messages. In particular it may follow the algorithm, then in some round send its messages to only some processes, and then send nothing more. That is a crash. In the signed model a crashed process signs only what its code tells it to sign, so all its signatures are ones a correct process could make. So every run of $A$ with at most $t$ crashes is a run of $A$ with at most $t$ Byzantine faults, and $A$ satisfies its conditions in it.

**Broadcast gives weak validity.** From a broadcast algorithm, build consensus: every process decides the output of the broadcast with sender $p_0$, where $p_0$ uses its input as the value to send. Agreement holds by the agreement of broadcast. If no process is faulty and all inputs are $v$, the sender is correct with input $v$, so every decision is $v$. The rounds are the same. Strong validity implies weak validity too. So it is enough to prove the bound for consensus with weak validity, restricted to crash runs.

**The crash bound needs validity only in failure-free runs.** The proof on the [crash bound page](/consensus-round-lower-bound/) uses validity in one place only: in its Lemma 1, to show that the initial configuration with all inputs 0 is 0-valent and the one with all inputs 1 is 1-valent. Lemma 1 needs this fact only when it assumes that these configurations are univalent, and a univalent configuration has one decision value in all its extensions. So one run from each fixes its valence, and the failure-free run can be that run. In a failure-free run weak validity gives the decision $v$. So the proof works with weak validity, and it gives a crash run with at most $t$ crashes in which a correct process is undecided after round $t$. This is the run that the theorem asks for.

The crash proof needs $t \le n - 2$, so that at least two processes are correct in every run that it builds. The case $t = n - 1$ is not covered.

## Consequences

- **Signatures do not save rounds.** The [Dolev-Strong algorithm](/dolev-strong-algorithm/) and [SM(m)](/signed-messages-algorithm/) use signatures to tolerate any number of faults, but they cannot do it in fewer than $t + 1$ rounds. Signatures improve the number of processes needed, not the time.
- **Byzantine faults do not cost more rounds than crashes.** The bound for crashes and for Byzantine faults is the same, $t + 1$. The extra power of the adversary costs processes ($n > 3t$ without signatures) and messages, but not rounds.
- **Interactive consistency.** $n$ parallel broadcasts give interactive consistency in $t + 1$ rounds, and interactive consistency gives broadcast in the same number of rounds. So $t + 1$ rounds are exact for it too. This was the problem that Fischer and Lynch studied.
- **Randomization.** The bound is for deterministic algorithms in their worst case. Randomized algorithms such as [Rabin's](/rabin-randomized-byzantine-agreement/) and the algorithm of [Feldman and Micali](/feldman-micali-byzantine-agreement/) reach agreement in an expected constant number of rounds.
- **Early stopping.** In runs where only $f < t$ processes actually fail, an algorithm can stop earlier. Dolev, Reischuk and Strong (1990) show that $\min(f + 2, t + 1)$ rounds are necessary and enough for early stopping Byzantine agreement.

## Tightness

The bound is tight in each setting. Without signatures, the [oral messages algorithm](/oral-messages-algorithm/) OM(t) uses $t + 1$ rounds for $n > 3t$, and the algorithm of Garay and Moses (1998) does so with polynomial messages. With signatures, the Dolev-Strong algorithm uses $t + 1$ rounds for any $t < n$ with $O(n^2)$ messages from correct processes. For crash faults, [FloodSet](/floodset/) uses $t + 1$ rounds.

Algorithms that are not optimal in rounds are often simpler. The [phase king algorithm](/phase-king-algorithm/) and the [phase queen algorithm](/phase-queen-algorithm/) use a constant number of rounds per phase and $t + 1$ phases, so $O(t)$ rounds, with small messages.

## History

Fischer and Lynch (1982) proved that interactive consistency with $t$ faulty processes needs $t + 1$ rounds. Dolev and Strong (1983) extended the bound to algorithms with signatures, and to any kind of message. Later proofs used crash failures, which made it clear that the bound does not depend on the power of the faults. The short bivalence proof of Aguilera and Toueg (1999) is the one that the crash bound page follows.

## References
