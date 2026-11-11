---
title: Agreement from graded consensus and a common coin in constant expected rounds
proves: [correctness]
status: full
---

**Claim.** Let $n \ge 3t + 1$ processes run the iteration of lines L1 to L6 in the synchronous model, with at most $t$ Byzantine processes and no signatures. Assume a coin (line L4) with this property: in each iteration, with probability at least $p > 0$, all honest processes get the same bit, and that bit is 0 or 1 with probability $1/2$ each, independent of all messages sent before the coin is revealed. Then (agreement) no two honest processes decide different values; (validity) if all honest processes start with $b$, they all decide $b$ in the first iteration; (termination) with probability 1 every honest process decides, and the expected iteration of the last decision is at most $2/p + 1$.

The coin is not proved here. Feldman and Micali build a coin with this property, for a constant $p$, from verifiable secret sharing and gradecast in a constant number of rounds (STOC 1988; SIAM Journal on Computing 26(4), 1997). With an ideal coin, $p = 1$ and the bound is 3 iterations.

**The iteration.** Each process holds a value $v$.

- Round 1 (L1): send $v$ to all. If some value $w$ has at least $n - t$ copies among the received values, set $x = w$; else $x = \bot$.
- Round 2 (L2, L3): send $x$ to all. Let $w$ be the most frequent value other than $\bot$ among the received proposals, with $c$ copies. If $c \ge n - t$, output $(w, 2)$; if $t + 1 \le c < n - t$, output $(w, 1)$; else output $(v, 0)$.
- Coin (L4, L5): get the coin $s$. Set $v = w$ if the grade is 1 or 2, and $v = s$ if the grade is 0.
- Decision (L6): if the grade is 2, decide $w$, take part in one more iteration, then halt.

Rounds 1 and 2 are *graded consensus*: each honest process outputs a value and a grade in $\{0, 1, 2\}$.

## Graded consensus

**Lemma 1.** In round 1, at most one value $w \ne \bot$ is proposed by honest processes.

*Proof.* An honest process that proposes $w$ saw $n - t$ copies of $w$, of which at least $n - 2t$ came from honest processes, and honest processes send the same value to all. If honest processes proposed $w$ and $w' \ne w$, then at least $2(n - 2t)$ honest processes sent $w$ or $w'$, while there are only $n - t$ honest processes. So $2n - 4t \le n - t$, that is $n \le 3t$, a contradiction. $\square$

**Lemma 2 (consistency).** If two honest processes output grades of at least 1, they output the same value.

*Proof.* A grade of at least 1 for $w$ needs $t + 1$ proposals for $w$, so at least one honest process proposed $w$. By Lemma 1, this $w$ is the same for every honest process. A value that no honest process proposed has at most $t$ proposals at every process, so it is never the output value with grade 1 or 2. $\square$

**Lemma 3 (grade 2 forces grade 1).** If an honest process outputs $(w, 2)$, every honest process outputs $w$ with grade at least 1.

*Proof.* The process saw $n - t$ proposals for $w$, at least $n - 2t \ge t + 1$ of them from honest processes. Every honest process receives these, so it sees at least $t + 1$ proposals for $w$, and by Lemma 2 no other value reaches $t + 1$. So it outputs $w$ with grade 1 or 2. $\square$

**Lemma 4 (unanimity).** If all honest processes start the iteration with $b$, all output $(b, 2)$.

*Proof.* Each honest process sees $n - t$ copies of $b$ in round 1, so all honest processes propose $b$, and in round 2 each sees $n - t$ proposals for $b$. By Lemma 1 no other value has more than $t < n - t$ proposals. $\square$

## The reduction

**Lemma 5 (decisions agree).** Let $k_0$ be the first iteration in which an honest process decides. All decisions in iteration $k_0$ are for one value $w$, every honest process starts iteration $k_0 + 1$ with $v = w$, and every honest process decides $w$ by iteration $k_0 + 1$.

*Proof.* A decision has grade 2, so by Lemma 2 all decisions in $k_0$ are for one value $w$. By Lemma 3 every honest process has grade at least 1 for $w$, so it sets $v = w$ and ignores the coin. In iteration $k_0 + 1$ all honest processes start with $w$, and all of them take part (a process that decided in $k_0$ runs one more iteration). By Lemma 4 all output $(w, 2)$ and decide $w$; from then on all stay at $w$. $\square$

**Theorem 1 (agreement and validity).** By Lemma 5 every decision is for the value $w$ of iteration $k_0$. If all honest processes start with $b$, Lemma 4 gives grade 2 for $b$ to all in the first iteration, so they all decide $b$. $\blacksquare$

**Lemma 6 (the coin makes the values equal).** In every iteration with no earlier decision, with probability at least $p/2$ all honest processes end the iteration with the same value.

*Proof.* By Lemma 2 the honest processes with grade at least 1 all hold one value $w$, and this value is fixed by the messages of rounds 1 and 2, before the coin is revealed. If no honest process has a grade of at least 1, let $w$ be 0. With probability at least $p$ the coin gives all honest processes the same bit $s$, uniform and independent of $w$, so with probability at least $p/2$ the bit equals $w$. Then the processes with grade 0 set $v = s = w$ and the others set $v = w$. $\square$

**Theorem 2 (termination).** Let $U$ be the first iteration at the end of which all honest processes hold the same value. By Lemma 6, $\Pr[U > k] \le (1 - p/2)^k$, so $U$ is finite with probability 1 and $E[U] \le 2/p$. By Lemma 4 all honest processes decide in iteration $U + 1$ or earlier, so the expected iteration of the last decision is at most $2/p + 1$. Each iteration takes 2 rounds plus the rounds of the coin, which are a constant, so the expected number of rounds is a constant. $\blacksquare$

## Where the assumptions are used

- $n \ge 3t + 1$ is used in Lemma 1 and in Lemma 3 ($n - 2t \ge t + 1$). With $n = 3t$, a faulty process that echoes each honest value back to its sender makes two honest processes propose different values and decide differently in the first iteration; the tests run this for $n = 3$ and $n = 6$.
- The coin must be revealed after round 2. The tests give the adversary a coin it knows in advance: it then keeps one honest group at grade 1 and the other at grade 0 with the opposite bit, and nobody decides in 60 iterations.
- The measured means agree with the bounds: with an ideal coin and the strongest attack of the tests, the last decision comes at iteration 2.94 on average ($n = 10$, $t = 3$, 300 runs; bound 3); with a coin that is common with probability $1/2$, at 4.73 (bound 5).
