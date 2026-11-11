---
title: The phase queen algorithm reaches agreement and strong validity when n > 4t
proves: [correctness]
status: full
---

**Claim.** In the synchronous model with $n$ processes, reliable authenticated point-to-point channels and at most $t$ Byzantine processes, with $n > 4t$, every run of PHASE-QUEEN has these properties. (Agreement) All honest processes decide the same bit. (Strong validity) If all honest processes start with $v$, they all decide $v$. (Termination) Every honest process decides after round $2(t + 1)$.

The adversary is static and rushing, and it sees all honest messages before it chooses its own. The proof does not limit what it knows.

**Setup.** Let $t' \le t$ be the number of faulty processes and $H$ the set of honest processes, $|H| = n - t'$. In round 1 of a phase, an honest process $p$ gets at most one bit from each sender. Let $h_b$ be the number of honest processes that send $b$ in round 1; it is the same for all receivers, because honest processes send the same bit to all. The count $c_p(b)$ of $p$ satisfies $h_b \le c_p(b) \le h_b + t'$. Line L4 sets $maj_p$ to the more frequent bit (0 on a tie) and $mult_p = c_p(maj_p)$. The test of line L6 is $mult_p > n/2 + t$.

**Lemma 1 (a strong count is an honest majority).** If honest $p$ passes the test of line L6 with $maj_p = b$, then $h_b > n/2$.

*Proof.* $h_b \ge c_p(b) - t' > n/2 + t - t' \ge n/2$. $\square$

**Lemma 2 (all strong counts agree).** If honest $p$ and $q$ both pass the test of line L6, then $maj_p = maj_q$.

*Proof.* By Lemma 1, $h_{maj_p} > n/2$ and $h_{maj_q} > n/2$. If $maj_p \ne maj_q$, then $h_0 + h_1 > n$, but $h_0 + h_1 = |H| \le n$. $\square$

**Lemma 3 (an honest queen).** If the queen $k$ of a phase is honest, all honest processes have the same value at the end of the phase.

*Proof.* The queen sends $maj_k$ to all. If no honest process passes the test of line L6, all honest processes take $maj_k$ at line L7. Otherwise let honest $p$ pass it with $maj_p = b$. By Lemma 1, $h_b > n/2$, so $c_k(b) \ge h_b > n/2$, and $c_k(1 - b) \le n - c_k(b) < n/2$. So $maj_k = b$. Every honest process that passes the test takes $b$ by Lemma 2, and every other one takes $maj_k = b$. $\square$

**Lemma 4 (persistence).** If all honest processes have $x = v$ at the start of a phase, all of them have $x = v$ at the end of it.

*Proof.* Each honest $p$ has $c_p(v) \ge h_v = n - t' \ge n - t$. Since $n > 4t$, $n - t > n/2 + t$, so $c_p(v) > n/2 + t > n/2$. The count of the other bit is at most $t' < n/2$, so $maj_p = v$, and $p$ passes the test of line L6 and keeps $v$, whatever the queen sends. $\square$

**Theorem.** PHASE-QUEEN has agreement, strong validity and termination.

*Proof.* Termination holds because the loop has $t + 1$ phases of two rounds. The $t + 1$ queens are different processes, so at least one is honest. By Lemma 3 the honest processes agree at the end of that phase, and by Lemma 4 and induction they still agree at the end of phase $t + 1$. If all honest processes start with $v$, Lemma 4 and induction from phase 1 give $v$ at the end. $\blacksquare$

**Where n > 4t is used.** Only Lemma 4 needs it: an honest count of $n - t$ must pass the test $mult > n/2 + t$. Lemmas 1 to 3 hold for every $n$. With $n = 4t$ and all honest processes on $v$, the faulty processes send $1 - v$, so each honest count is $n - t = n/2 + t$ and fails the test. Every honest process then takes the value of the queen, and a faulty queen in the last phase sends 0 to some and 1 to others. Both agreement and validity fail. This only shows that this algorithm needs $n > 4t$. The [phase king algorithm](/phase-king-algorithm/) reaches $n > 3t$ with a third round per phase.
