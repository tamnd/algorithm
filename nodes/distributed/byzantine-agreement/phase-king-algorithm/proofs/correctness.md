---
title: The phase king algorithm reaches agreement and strong validity when n > 3t
proves: [correctness]
status: full
---

**Claim.** In the synchronous model with $n$ processes, reliable authenticated point-to-point channels and at most $t$ Byzantine processes, with $n > 3t$, every run of PHASE-KING has these properties. (Agreement) All honest processes decide the same value. (Strong validity) If all honest processes start with $v$, they all decide $v$. (Termination) Every honest process decides at the end of round $3(t + 1)$.

The adversary is static: it picks the faulty set before the run. It is also rushing and sees everything: in each round it chooses the messages of the faulty processes after it has seen the messages of the honest processes in that round. The proof does not use any limit on what it knows.

**Setup.** Let $t' \le t$ be the number of faulty processes in the run, and $H$ the set of honest processes, so $|H| = n - t'$. A process receives at most one message from each sender in each round, and the channel gives the receiver the true identity of the sender. A message is a bit, or the symbol "no proposal". For a phase $\varphi$, write $x_p$ for the value of $p$ at the start of the phase, $x'_p$ for its value after line L6 and $x''_p$ for its value at the end of the phase (after line L9).

**Lemma 1 (one honest proposal).** In each phase, all honest processes that send a proposal at line L4 propose the same value.

*Proof.* Let honest $p$ propose $y$. Then $p$ got value$(y)$ from at least $n - t$ different senders at line L3. At most $t'$ of them are faulty, so at least $n - t - t'$ honest processes have $x = y$ at the start of the phase. Assume that honest $q$ proposes $y' \ne y$. The same count gives at least $n - t - t'$ honest processes with $x = y'$. An honest process sends the same value to every receiver, so these two sets are disjoint, and $2(n - t - t') \le |H| = n - t'$. This gives $n \le 2t + t' \le 3t$, which is false. $\square$

**Lemma 2 (the propose round).** In each phase, if an honest process changes its value at line L6 to $z$, then $z$ is the value of Lemma 1.

*Proof.* Line L6 needs more than $t$ messages propose$(z)$ from different senders. At most $t' \le t$ senders are faulty, so at least one honest process proposed $z$. By Lemma 1, $z$ is the unique honest proposal. $\square$

So in one phase at most one value $z$ can pass the test of line L6, and line L6 is well defined.

**Lemma 3 (persistence).** If all honest processes have $x = v$ at the start of a phase, all honest processes have $x = v$ at the end of it.

*Proof.* Each honest process gets value$(v)$ from all $n - t'$ honest processes, and $n - t' \ge n - t$, so the test of line L4 holds for $v$. It cannot also hold for $1 - v$: that needs $n - t$ more messages, and $2(n - t) > n$ because $n > 2t$. So every honest process proposes $v$. Each honest process then gets propose$(v)$ from the $n - t'$ honest processes, and $n - t' \ge n - t > t$, so line L6 sets $x = v$. At line L8 it has at least $n - t$ messages propose$(v)$, so it keeps $v$ and does not use the value of the king. $\square$

**Lemma 4 (an honest king).** If the king $k$ of a phase is honest, all honest processes have the same value at the end of the phase.

*Proof.* The king sends $w = x'_k$ to all at line L7. Take an honest $p$.

- If $p$ does not keep its value at line L8, it sets $x''_p = w$.
- If $p$ keeps its value, it got at least $n - t$ messages propose$(x'_p)$. At most $t'$ of them are faulty, so at least $n - t - t' \ge 1$ honest processes proposed $x'_p$. By Lemma 1, $x'_p = z$, the unique honest proposal. The same $n - t - t'$ honest processes also sent propose$(z)$ to the king. Since $n > 3t \ge 2t + t'$, we have $n - t - t' > t$, so the king got more than $t$ messages propose$(z)$ and set $x'_k = z$ at line L6, by Lemma 2. So $w = z = x''_p$.

In both cases $x''_p = w$. $\square$

**Theorem.** PHASE-KING has agreement, strong validity and termination.

*Proof.* Termination: the loop runs $t + 1$ phases of three rounds each, and every honest process decides at line L10 after round $3(t + 1)$. Agreement: the kings of the $t + 1$ phases are $t + 1$ different processes, and at most $t$ processes are faulty, so some phase $\varphi$ has an honest king. By Lemma 4, all honest processes have the same value $u$ at the end of phase $\varphi$. By Lemma 3 and induction on the later phases, they all still have $u$ at the end of phase $t + 1$, and they all decide $u$. Strong validity: if all honest processes start with $v$, Lemma 3 and induction on the phases give $x = v$ at every honest process at the end of phase $t + 1$. $\blacksquare$

**Where n > 3t is used.** Lemma 1 needs $2(n - t - t') > n - t'$, and Lemma 4 needs $n - t - t' > t$. With $t' = t$ both are $n > 3t$. With $n = 3t$ the test of line L4 can pass for both values: the run of the split attack on the page shows two honest groups that each see $n - t$ copies of their own value in every phase, keep their values at line L8, and never listen to an honest king. This shows only that this algorithm fails at $n = 3t$. The bound $n > 3t$ for every algorithm without signatures is the [Byzantine resilience bound](/byzantine-resilience-bound/).
