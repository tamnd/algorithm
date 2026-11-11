---
tag: T16K3P
kind: theorem
slug: dolev-reischuk-lower-bound
name: Dolev-Reischuk lower bound
aliases:
- Dolev-Reischuk message bound
- quadratic message lower bound
area: distributed/byzantine-agreement
level: research
summary: "Deterministic Byzantine broadcast with t faults needs Omega(nt) signatures with authentication, and Omega(n + t^2) messages from correct processes even with signatures."
prereqs: [byzantine-broadcast, message-complexity]
see_also: [dolev-strong-algorithm, authenticated-resilience-bound, byzantine-round-lower-bound, oral-messages-algorithm, hotstuff, threshold-signature, quorum-certificate, adversary-argument]
sources:
  - paper: doi:10.1145/2455.214112
    title: Danny Dolev and Rüdiger Reischuk, Bounds on information exchange for Byzantine agreement, Journal of the ACM 32(1), 1985
    locator: pages 191 to 204 (Omega(nt) signatures for authenticated algorithms, Omega(nt) messages without authentication, Omega(n + t^2) messages with authentication)
  - paper: doi:10.1145/3293611.3331629
    title: Ittai Abraham, T.-H. Hubert Chan, Danny Dolev, Kartik Nayak, Rafael Pass, Ling Ren and Elaine Shi, Communication complexity of Byzantine agreement, revisited, PODC 2019
    locator: Section 3 (a short proof of the Omega(f^2) bound for deterministic protocols, and Theorem 4, the bound for randomized protocols against a strongly adaptive adversary)
  - url: https://arxiv.org/abs/2311.08060
    title: Pierre Civit, Seth Gilbert, Rachid Guerraoui, Jovan Komatovic, Anton Paramonov and Manuel Vidigueira, All Byzantine Agreement Problems are Expensive, PODC 2024
    locator: Abstract and Section 1 (the Omega(t^2) message bound holds for every non-trivial validity property)
  - paper: doi:10.1137/0212045
    title: Danny Dolev and H. Raymond Strong, Authenticated algorithms for Byzantine agreement, SIAM Journal on Computing 12(4), 1983
    locator: pages 656 to 666 (authenticated broadcast with O(n^2) messages, which matches the bound when t is a constant fraction of n)
---

Byzantine agreement cannot be cheap in messages. Dolev and Reischuk (1985) proved that every deterministic algorithm for [Byzantine broadcast](/byzantine-broadcast/) that tolerates $t$ faults has a run in which the correct processes send $\Omega(n + t^2)$ messages, even with signatures, and $\Omega(nt)$ signatures in total if it uses signatures. Without signatures the message bound is $\Omega(nt)$. So for $t = \Theta(n)$, the $O(n^2)$ [message complexity](/message-complexity/) of the [Dolev-Strong algorithm](/dolev-strong-algorithm/) is optimal. The proof of the $\Omega(t^2)$ part on this page is an isolation argument, in a corrected form of the short proof of Abraham et al. (2019).

## Statement

**Model.** There are $n$ processes on a complete network of reliable links in the [synchronous model](/synchronous-model/). A designated sender $s$ has a binary input. At most $t$ processes are [Byzantine](/byzantine-failure-model/), chosen before the run by a static adversary. Signatures may be available. The algorithm is deterministic. The *message count* of a run is the number of messages that correct processes send in it. Messages that faulty processes send are not counted.

**Theorem (Dolev and Reischuk, 1985).** Let $A$ be a deterministic algorithm for Byzantine broadcast with at most $t < n$ faults.

1. In some run of $A$, the correct processes send at least $\lfloor t/2 \rfloor^2 / 2$ messages. This holds with signatures, and even if the faulty processes only omit messages.
2. In some failure-free run of $A$, at least $(n - 1)/2$ messages are sent.
3. *(Cited.)* If $A$ uses signatures, the correct processes send $\Omega(nt)$ signatures in some run. If $A$ uses no signatures, they send $\Omega(nt)$ messages in some run.

Parts 1 and 2 together give $\Omega(n + t^2)$ messages. Parts 1 and 2 are proved on this page in full. For part 3 see the paper of Dolev and Reischuk.

The bounds hold for consensus too, since consensus with strong validity gives broadcast with one more round of the same kind of messages. Civit et al. (2024) show the $\Omega(t^2)$ bound for every validity property that is not trivial.

## In plain words

To be safe against $t$ liars, many processes must hear from many others. Suppose that some honest process hears almost nothing. Then the liars can make it hear nothing at all: a few liars just do not send to it. A process that hears nothing must give some fixed answer, and the adversary picks the sender's value to be the other one. Everyone else answers correctly, so the honest process that heard nothing disagrees with them.

So no honest process may be left out, and the adversary can corrupt up to about $t/2$ senders around any one process. Each of about $t/2$ processes must hear from more than $t/2$ others. That makes about $t^2/4$ messages in total.

## Proof

The full proof is below. This section gives its structure. Let $k = \lfloor t/2 \rfloor \ge 1$. Assume that in every run of $A$ the correct processes send fewer than $k^2/2$ messages.

**Two runs with a silent group.** Fix a set $V$ of $k$ processes, not containing the sender, and let $U$ be the others. In run $E_b$ the sender has input $b$, the processes of $U$ are correct, and the processes of $V$ are faulty in a mild way: each follows $A$, but never sends to another process of $V$, and acts as if it did not receive the first $k$ messages sent to it. The sender is correct, so every process of $U$ outputs $b$ in $E_b$.

**One process that hears little.** In $E_0$ and $E_1$ together, fewer than $k^2$ messages are sent, so fewer than $k^2$ go to $V$. If each of the $k$ processes in $V$ received more than $k$ messages in $E_0$ or in $E_1$, there would be more than $k^2$. So some $p \in V$ receives at most $k$ messages in each of the two runs. In both runs, $p$ ignores all of them, so it acts like a correct process that has received nothing.

**Isolate $p$.** Let $S_b$ be the set of processes that send to $p$ in $E_b$, with $|S_b| \le k$. In run $E'_b$, the sender has input $b$, $p$ is correct, the processes of $V \setminus \{p\}$ act as in $E_b$, and the processes of $S_b$ are faulty: they act as in $E_b$ but do not send to $p$. This is at most $(k - 1) + k < t$ faults, and only omissions. Now $p$ receives nothing, so it sends what it sent in $E_b$, and the processes of $U \setminus S_b$ see exactly what they saw in $E_b$. They output $b$. There are at least $n - t \ge 1$ of them, and they are correct.

**The contradiction.** A correct process that receives nothing is deterministic, so $p$ outputs one fixed value $c$ in both $E'_0$ and $E'_1$. Take $b = 1 - c$. In $E'_b$, the correct process $p$ outputs $c$ and the correct processes of $U \setminus S_b$ output $b \ne c$. This breaks agreement.

**The $\Omega(n)$ part.** In the failure-free run with input $b$, a process that receives no message outputs its fixed value for an empty view. That value cannot be both 0 and 1. So each non-sender receives a message in at least one of the two failure-free runs, and one of the two runs has at least $(n - 1)/2$ messages.

## Consequences

- **Quadratic cost is the price of determinism.** For $t = \Theta(n)$, every deterministic Byzantine broadcast or consensus algorithm sends $\Omega(n^2)$ messages in its worst case. The Dolev-Strong algorithm, with $O(n^2)$ messages from correct processes, is optimal up to a constant factor. The [oral messages algorithm](/oral-messages-algorithm/), with $n^{\Theta(t)}$ messages, is far from it.
- **Signatures do not remove it.** The $\Omega(t^2)$ part holds with signatures, and even against faults that only omit messages. Combining signatures into one [threshold signature](/threshold-signature/) or a [quorum certificate](/quorum-certificate/) shrinks the size of messages, not their number in the worst case. [HotStuff](/hotstuff/) sends $O(n)$ messages per view, but when $t$ leaders in a row are faulty it needs $t + 1$ views, so $O(nt)$ messages.
- **Signatures are counted too.** With authentication, $\Omega(nt)$ signatures are needed. This bounds the computation of signing and checking, not only the traffic.
- **Randomized algorithms.** Abraham et al. (2019, Theorem 4) extend the bound. A randomized algorithm that reaches agreement with probability at least $3/4 + \varepsilon$ against a *strongly adaptive* adversary, which can corrupt a process and remove the messages it just sent, needs $(\varepsilon t)^2$ messages in expectation. Against weaker adversaries, randomized algorithms with fewer messages exist, for example that of King and Saia (2011).

## Tightness

Part 1 is tight up to constants when $t = \Theta(n)$: Dolev-Strong sends at most $(n - 1) + 2(n - 1)(n - 2)$ messages from correct processes. Part 2 is tight up to a factor of 2 in the failure-free case, since the sender alone can send $n - 1$ messages. The proof on this page gives the constant $1/8$ for $t^2$, and no attempt is made to improve it.

The bound is for the worst case. In runs without faults, many protocols need only $O(n)$ messages.

## History

Dolev and Reischuk (1985) proved the bounds on messages and signatures, with an argument about how information spreads. The short isolation argument for the $\Omega(t^2)$ part appears in Abraham, Chan, Dolev, Nayak, Pass, Ren and Shi (2019), as a warmup for the randomized bound. The version on this page fixes the isolated process with both runs $E_0$ and $E_1$ before the input is chosen, which makes the choice of the input value exact. Civit, Gilbert, Guerraoui, Komatovic, Paramonov and Vidigueira (2024) extended the bound to all non-trivial forms of Byzantine agreement.

## References
