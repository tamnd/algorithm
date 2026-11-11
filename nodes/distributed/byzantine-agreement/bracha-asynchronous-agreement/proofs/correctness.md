---
title: Bracha's agreement protocol is always safe and terminates with probability 1 when n > 3t
proves: [correctness]
status: full
---

**Claim.** In the asynchronous model with $n$ processes, reliable authenticated links and at most $t$ Byzantine processes, with $n > 3t$, BRACHA-AGREEMENT has these properties. (Agreement) No two honest processes decide different bits. (Validity) If all honest processes start with $v$, every honest decision is $v$, and every honest process decides in round 1. (Termination) Against an adversary whose actions in round $r$ do not depend on the coins flipped in round $r$, every honest process decides with probability 1, and the expected number of rounds is at most $2^{n} + 1$.

Agreement and validity hold in every run, for every schedule and every outcome of the coins.

**Setup.** Let $t' \le t$ be the number of faulty processes. All messages go through [Bracha reliable broadcast](/bracha-reliable-broadcast/), which has validity, consistency and totality when $n > 3t$. So for each sender $j$, round $r$ and step $k$ there is at most one value $u_j(r, k)$ that any honest process delivers, and if one honest process delivers it, all do. A message is *valid* at $p$ when $p$ has delivered $n - t$ valid messages of the step before, from different senders, which would make an honest process send that value (line L12). Whether a message is valid depends only on the set of messages delivered, and a larger set can only make more messages valid. A *quorum* is a set of $n - t$ valid messages of one step from different senders. Write $(d, w)$ for the marked value of step 2 and ? for the unmarked one.

**Lemma 1 (progress).** Every honest process that has not halted eventually completes each step that it starts.

*Proof.* By induction on the order of steps. An honest process $q$ sends its step $(r, k)$ value after it got a quorum $S$ of the step before. By reliable broadcast every honest process delivers the same messages of $S$, and by induction they become valid there too, so the message of $q$ becomes valid at every honest process. At least $n - t' \ge n - t$ honest processes run step $(r, k)$, as long as no honest process halts before it (Lemma 4 shows that a halted process is no longer needed), so every honest process gets a quorum. $\square$

**Lemma 2 (one marked value).** In one round, no two valid step-3 messages are $(d, 0)$ and $(d, 1)$.

*Proof.* A valid $(d, w)$ needs a quorum of step-2 messages in which more than $n/2$ senders sent $w$, and a valid $(d, 1 - w)$ needs more than $n/2$ senders that sent $1 - w$. Two sets of more than $n/2$ senders share a sender $j$. By consistency of reliable broadcast, $j$ has one step-2 value $u_j(r, 2)$, so it cannot be both $w$ and $1 - w$. This holds also when $j$ is faulty. $\square$

**Lemma 3 (unanimity).** If all honest step-1 messages of round $r$ are $w$, then every honest process that runs round $r$ decides $w$ in it (or has decided before), ends it with $v = w$, and every valid step-1 message of round $r + 1$ is $w$.

*Proof.* A quorum of step-1 messages has at least $n - t - t' \ge n - 2t$ honest messages, all $w$, and at most $t' \le t$ others. Since $n > 3t$, $n - 2t > t$, so $w$ is the strict majority of every quorum. Hence every valid step-2 message, honest or not, is $w$. Every quorum of step-2 messages then has $n - t > n/2$ values $w$, because $n > 2t$, so every valid step-3 message is $(d, w)$. Every quorum of step-3 messages has $n - t > 2t$ messages $(d, w)$, so each honest process decides $w$ at line L8 and sets $v = w$ at line L9. A step-1 message of round $r + 1$ is valid only if some quorum of step-3 messages leads to it, and every such quorum has more than $t$ copies of $(d, w)$, which lead to $w$. $\square$

**Lemma 4 (agreement).** If an honest process $p$ decides $w$ in round $r$, every honest process decides $w$, in round $r$ or $r + 1$.

*Proof.* $p$ saw a quorum with a set $A$ of more than $2t$ senders of $(d, w)$. Let $q$ be honest, with a step-3 quorum from a set $B$ of $n - t$ senders. Then $|A \cap B| > 2t + (n - t) - n = t$, and by consistency of reliable broadcast the senders in $A \cap B$ sent $(d, w)$ to $q$ too. So $q$ sees more than $t$ copies of $(d, w)$, and by Lemma 2 no $(d, 1 - w)$. If $q$ decides in round $r$, it decides $w$. In any case $q$ sets $v = w$ at line L9. So all honest step-1 messages of round $r + 1$ are $w$, and by Lemma 3 every honest process decides $w$ by the end of round $r + 1$. A process that decided in round $r' \ge r$ halts only after round $r' + 1$ (line L11), so all honest processes run round $r + 1$, and Lemma 1 applies to it. $\square$

Let $r$ be the first round in which an honest process decides. By Lemma 4 every honest decision is the value decided first, which gives agreement.

**Validity.** If all honest processes start with $v$, all honest step-1 messages of round 1 are $v$, and Lemma 3 gives a decision $v$ in round 1 at every honest process.

**Termination with probability 1.** Assume an adversary whose actions in round $r$ (the order of deliveries of messages of round $r$ and the values that faulty processes send in round $r$) do not depend on the coins flipped in round $r$. A coin of round $r$ is first used in step 1 of round $r + 1$. So, given the coins of the earlier rounds, the following are fixed before the coins of round $r$: the value $w_r$ of the valid messages $(d, w_r)$ of round $r$ if there is one (unique by Lemma 2), and the set $F_r$ of honest processes that flip a coin at line L10 in round $r$. Let $t_r = w_r$ if $w_r$ exists and $t_r = 0$ otherwise.

Every honest process that does not flip sets $v = w_r$ at line L9. If every process in $F_r$ gets $t_r$ from its coin, then all honest step-1 messages of round $r + 1$ are $t_r$, and by Lemma 3 every honest process decides in round $r + 1$. Call such a round *good*. The coins are independent and fair, and $|F_r| \le n - t' \le n$, so a round is good with probability at least $2^{-n}$, given any outcome of the earlier rounds. The first good round $G$ has $\Pr[G > k] \le (1 - 2^{-n})^k$, which tends to 0, and $\mathbb{E}[G] \le 2^{n}$. All honest processes decide by round $G + 1$, so the expected number of rounds is at most $2^n + 1$. $\blacksquare$

**Where n > 3t is used.** Reliable broadcast needs it. Lemma 3 needs $n - 2t > t$ for the strict majority of step 1 and $n - t > 2t$ for the decision. Lemma 4 needs $|A \cap B| > t$, which holds for every $n$, and Lemma 1 needs $n - t$ honest senders for a quorum.

**On the adversary.** The bound $2^{-n}$ per round uses that $t_r$ and $F_r$ do not depend on the coins of round $r$. An adversary that sees a coin flipped early in round $r$ before it chooses the step-2 messages of slow processes may try to make $w_r$ the opposite value; the bound then needs a more careful argument, as for [Ben-Or's algorithm](/ben-or-consensus/).
