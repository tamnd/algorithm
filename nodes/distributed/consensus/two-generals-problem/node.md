---
tag: 6MJM6Y
kind: problem
slug: two-generals-problem
name: Two generals problem
aliases:
- coordinated attack problem
area: distributed/consensus
level: intro
summary: Two parties over an unreliable channel cannot agree with certainty on a joint action.
prereqs: [synchronous-model]
see_also: [consensus-problem, atomic-commit, two-phase-commit, byzantine-failure-model, oral-messages-algorithm, flp-impossibility, adversary-argument, consensus-round-lower-bound]
sources:
  - paper: doi:10.1145/800213.806523
    title: E. A. Akkoyunlu, K. Ekanadham and R. V. Huber, Some constraints and tradeoffs in the design of network communications, SOSP 1975
    locator: pages 67 to 74 (the first statement of the problem, with two groups that must coordinate over a lossy channel)
  - paper: doi:10.1007/3-540-08755-9_9
    title: Jim Gray, Notes on data base operating systems, in Operating Systems, An Advanced Course, LNCS 60, Springer, 1978
    locator: pages 393 to 481; the section on two-phase commit, where the problem is told as the two generals paradox
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 5, Section 5.1 (the coordinated attack problem, deterministic version, and the impossibility proof by removing messages) and Section 5.2 (the randomized version)
  - paper: doi:10.1145/79147.79161
    title: Joseph Y. Halpern and Yoram Moses, Knowledge and common knowledge in a distributed environment, Journal of the ACM 37(3), 1990
    locator: pages 549 to 587 (coordinated attack needs common knowledge, which unreliable communication cannot give)
---

The two generals problem, also called the coordinated attack problem, asks two processes to agree on one bit when any message between them can be lost. Akkoyunlu, Ekanadham and Huber stated it in 1975, and Gray told it as the two generals paradox in 1978. No protocol with a finite number of messages solves it: the proof removes the last delivered message, one message at a time, until the inputs no longer matter. It is about lossy links between correct processes, and it is a different problem from the [Byzantine generals](/byzantine-failure-model/) problem, which is about faulty processes on reliable links.

## In plain words

Two armies sit on two hills, with the enemy in the valley between them. They win only if they attack together. The generals can talk only by messengers, who must cross the valley and can be caught.

The first general sends "attack at dawn". The second general gets it, but he knows that the first general does not know that the message arrived. So he sends a reply. Now the first general does not know if the reply arrived, so the second general still waits for news. Every message needs one more message to confirm it.

The proof turns this into a strict argument. Take the last message that arrived and imagine it was caught. Its sender sees no change, so it must act the same. Repeat this for every message, and the generals end up acting the same even when nobody wanted to attack.

## Definition

There are two processes $A$ and $B$ connected by one link in each direction. Each has an input bit, where 1 means "attack". Computation runs in synchronous rounds: in each round each process may send a message to the other, and then changes its state. The adversary can lose any message, in any round, with no limit. Processes do not fail. Each process must eventually decide a bit. A solution must give these properties in every run, in the form that Lynch uses:

- **Agreement.** Both processes decide the same value.
- **Validity.** If both inputs are 0, the decision is 0. If both inputs are 1 and no message is lost, the decision is 1.
- **Termination.** Both processes decide.

The second half of validity is the one that makes the problem hard. Without it, the protocol "always decide 0" is correct.

**Theorem (Lynch, Theorem 5.1).** No deterministic protocol solves the coordinated attack problem.

*Proof.*

1. Assume that a protocol $P$ solves the problem. Without loss of generality each process sends a message in every round. Where $P$ sends nothing, let it send a dummy message that the receiver ignores. The ignored messages change no state, so the new protocol decides as $P$ does in every run.
2. Let $\alpha$ be the run with both inputs 1 and no loss. By validity both decide 1 in $\alpha$. Let $r$ be a round by which both have decided.
3. Let $\alpha_0$ be $\alpha$ with every message after round $r$ lost. Up to round $r$, no process can tell $\alpha_0$ from $\alpha$, so both decide 1 in $\alpha_0$, at the same times.
4. List the $2r$ messages of rounds $1$ to $r$ from the last round to the first. Let $\alpha_{j}$ be $\alpha_0$ with the first $j$ messages of this list also lost. So $\alpha_{2r}$ is the run with inputs $(1, 1)$ in which every message is lost.
5. Compare $\alpha_{j-1}$ and $\alpha_j$. They differ only in the delivery of one message $m$, sent by a process $s$ in some round $k$. Every message to $s$ after round $k$ is lost in both runs. The message to $s$ in round $k$, if any, has the same fate in both. So $s$ has the same state at every time in both runs, and it decides the same value at the same time. By agreement, the other process decides that value too. So the decision is the same in $\alpha_{j-1}$ and in $\alpha_j$. By induction, both decide 1 in $\alpha_{2r}$.
6. Let $\beta$ be $\alpha_{2r}$ with the input of $A$ changed to 0. Process $B$ gets no message in either run, so it has the same state at every time, and it decides 1 in $\beta$. By agreement, $A$ decides 1 in $\beta$.
7. Let $\gamma$ be $\beta$ with the input of $B$ changed to 0. Process $A$ gets no message in either run, so it decides 1 in $\gamma$. But $\gamma$ has both inputs 0, and validity requires 0. This is a contradiction. $\blacksquare$

The proof never uses a bound on the number of rounds of the whole protocol. It uses only one run, $\alpha$, and the round $r$ by which that run decides. So a protocol that sends more and more messages does not help.

## Variants

- **Coordinated attack on a network.** The same proof works for any connected network of $n \ge 2$ processes with lossy links. Remove messages one at a time from the last, and each step changes the state of the receiver only, so a process that sees no change exists. With all messages lost, change the inputs one at a time.
- **Bounded loss.** If at most $L$ messages can be lost, the problem is easy. Each process sends its input in each of $L + 1$ rounds, so each gets the other input at least once, and both decide the AND of the inputs.
- **Randomized coordinated attack.** Lynch, Section 5.2, lets each process use random bits and asks that disagreement have small probability. Her algorithm with $r$ rounds bounds this probability by about $1/r$, and she proves a lower bound of the same order. So more rounds buy more confidence, but never certainty.
- **Weaker validity.** If the decision must be 1 only when both inputs are 1, without the "no message lost" part, no protocol can work either, because the run with all messages lost forces the same contradiction. If only the first half of validity is kept, "always decide 0" works.
- **Knowledge view.** Halpern and Moses show that coordinated attack needs *common knowledge* of the plan: $A$ knows, $B$ knows that $A$ knows, and so on for ever. Over a link that can lose messages, common knowledge cannot be gained, so no protocol can reach it.

## Examples

Take the protocol with two messages: $A$ sends its input to $B$, then $B$ sends its input to $A$, and each decides the AND of the inputs it knows, or 0 if it got nothing. The chain of the proof for this protocol, with the decision forced by each run, is below. The column "same state" names the process that cannot tell the run from the previous one.

| run | inputs of $A$, $B$ | lost messages | same state | decision forced |
|---|---|---|---|---|
| 1 | 1, 1 | none | | 1, by validity |
| 2 | 1, 1 | the reply of $B$ | $B$ | 1 |
| 3 | 1, 1 | both | $A$ | 1 |
| 4 | 0, 1 | both | $B$ | 1 |
| 5 | 0, 0 | both | $A$ | 1, but validity says 0 |

In run 2, $B$ decides 1, and $A$ has no reply and decides 0. So this protocol breaks agreement already there. Any other protocol breaks agreement or validity somewhere along the same chain.

An exhaustive search over small cases agrees with the theorem. Every full-information protocol, which sends its whole state in each message, fails when the two processes alternate for up to 8 messages, and when both send in each of up to 4 rounds. Every decision rule on these views fails, so every deterministic protocol with these message patterns fails. Of the protocols that alternate one-bit messages, there are 4 with one message, 256 with two and 16384 with three, and none of them works with any decision rule. A finite search can only cover small cases. The proof above covers all.

## Known algorithms

No deterministic algorithm solves the problem. Systems work around it by changing the problem:

- **Accept a small risk.** Send messages and acknowledgements with retries and a timeout, as the TCP connection close does. The risk of disagreement shrinks with the number of exchanges but stays above 0.
- **Randomize.** The randomized algorithm of Lynch, Section 5.2, has a disagreement probability of about $1/r$ after $r$ rounds.
- **Weaken termination.** [Two-phase commit](/two-phase-commit/) makes the decision safe and lets a participant wait, or *block*, until the coordinator can be reached. Agreement then holds always, and termination holds only when messages get through.
- **Assume reliable links.** Over a link that delivers each message in the end, retransmission gives reliable delivery, and then [consensus](/consensus-problem/) can be solved under the timing assumptions of its models.

## Bounds

- **Deterministic.** Impossible with any finite number of messages and rounds, by the theorem above.
- **Randomized.** With $r$ rounds, the best disagreement probability is of order $1/r$ (Lynch, Section 5.2).
- **Bounded loss.** With at most $L$ lost messages, $L + 1$ rounds of exchange are enough.

## Reductions

- **From consensus with link failures.** Coordinated attack is the [consensus problem](/consensus-problem/) for two correct processes whose links can drop messages. Any consensus algorithm for lossy links would solve it, so none exists.
- **Not Byzantine generals.** In the Byzantine generals problem of Lamport, Shostak and Pease, links are reliable and some processes lie. It is solvable when $n > 3f$, by the [oral messages algorithm](/oral-messages-algorithm/), and it is about [faulty processes](/byzantine-failure-model/). In the two generals problem, the processes are correct and the links are faulty, and it is unsolvable for every $n \ge 2$.
- **Same method as other lower bounds.** The chain of runs in which one process sees no change at each step is the method of the [round lower bound](/consensus-round-lower-bound/) and of the [FLP theorem](/flp-impossibility/).

## Applications

- **Atomic commit.** Gray used the problem to explain why [atomic commit](/atomic-commit/) protocols can block. A participant that voted yes and then lost contact with the coordinator cannot decide alone.
- **Connection close.** In the TCP close handshake, the side that sends the last acknowledgement cannot know that it arrived. It waits in the TIME_WAIT state for a fixed time and accepts the small risk.
- **Exactly-once claims.** A sender over a lossy link cannot be sure that its last message arrived, so "exactly once" delivery needs retries plus removal of duplicates, not a single message.

## References
