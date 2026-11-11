---
title: Rabin's coin protocol agrees, and ends in constant expected rounds
proves: [correctness]
status: full
---

**Claim.** Let $n \ge 8t + 1$ processes run the protocol of this page in the synchronous model, with at most $t$ Byzantine processes and a dealer's coin whose shares cannot be forged. Let $L = \lfloor n/2 \rfloor + t + 1$, $H = L + t$ and $G = L + 2t$. Then (agreement) no two honest processes decide different values; (validity) if all honest processes start with $b$, they all decide $b$ in round 1; (termination) with probability 1 all honest processes decide, and the expected round of the last decision is at most 3.

The protocol, for each round $r$: each process sends its value $v$ to all (L1); it computes $maj$, the value with more than half of the received copies (0 if none), and $tally$, the number of copies of $maj$ (L2); it rebuilds the coin $s_r$ of the round from $t + 1$ valid shares (L3); it sets $T = L$ if $s_r = 0$ and $T = H$ if $s_r = 1$ (L4); it sets $v \leftarrow maj$ if $tally \ge T$ and $v \leftarrow 0$ otherwise (L5); it decides $maj$ if $tally \ge G$ (L6), then takes part in one more round and halts.

For a value $x$, let $h_x$ be the number of honest processes that sent $x$ in the round, and $tally_i(x)$ the number of copies of $x$ that process $i$ received.

**Lemma 1 (spread).** For honest $i$, $j$ and every value $x$: $h_x \le tally_i(x) \le h_x + t$, so $|tally_i(x) - tally_j(x)| \le t$.

*Proof.* The model is synchronous with reliable links, so every honest process receives the message of every honest process. Each faulty process adds at most one copy of $x$ to each tally. $\square$

**Lemma 2 (one value above $L$).** In one round, if $tally_i(x) \ge L$ and $tally_j(y) \ge L$ for honest $i$, $j$, then $x = y$.

*Proof.* By Lemma 1, $h_x \ge L - t$ and $h_y \ge L - t$. If $x \ne y$ then $h_x + h_y \le n - t$, so $2L - 2t \le n - t$, that is $2L \le n + t$. But $2L \ge 2(n - 1)/2 + 2t + 2 = n + 2t + 1$. $\square$

A process whose tally reaches $T \ge L > n/2$ has its $maj$ equal to the value of Lemma 2, because a value with more than $n/2$ copies has more than half of what the process received.

**Lemma 3 (unanimity is kept and decides).** If all honest processes start round $r$ with the value $x$, then every honest process sets $v = x$ and decides $x$ in round $r$.

*Proof.* By Lemma 1, $tally_i(x) \ge h_x = n - t$ and the other value has at most $t$ copies, so $maj = x$. The bound $n \ge 8t + 1$ gives $\lceil n/2 \rceil \ge 4t + 1$, so $n - t = \lfloor n/2 \rfloor + \lceil n/2 \rceil - t \ge \lfloor n/2 \rfloor + 3t + 1 = G$. So $tally_i(x) \ge G \ge T$: the process keeps $x$ and decides it. $\square$

**Lemma 4 (a decision forces unanimity).** If an honest process decides $x$ in round $r$, every honest process ends round $r$ with $v = x$.

*Proof.* $tally_i(x) \ge G$, so by Lemma 1 every honest $j$ has $tally_j(x) \ge G - t = H \ge T$, whichever the coin. By Lemma 2 and the remark after it, $maj_j = x$, so $j$ sets $v = x$. $\square$

**Theorem 1 (agreement and validity).** Let $r_0$ be the first round in which an honest process decides. All decisions of round $r_0$ are for one value $x$, by Lemma 2 (since $G \ge L$). By Lemma 4 all honest processes start round $r_0 + 1$ with $x$, and by Lemma 3 they keep $x$ and decide $x$ in round $r_0 + 1$ and every later round. So every decision is $x$. A process that decided in round $r_0$ takes part in round $r_0 + 1$, so all honest processes are present in that round, and all decide in it. If all honest processes start with $b$, Lemma 3 with $r = 1$ gives validity. $\blacksquare$

**Lemma 5 (the coin ends disagreement).** In each round, whatever happened before, with probability at least $1/2$ all honest processes end the round with the same value.

*Proof.* The messages of round $r$ are sent before any honest process sends its share of $s_r$, and the $t$ shares of the faulty processes give no information about $s_r$ (Shamir sharing with threshold $t + 1$). So the messages of the faulty processes in round $r$ are independent of $s_r$, and $s_r$ is a fair coin.

If no honest process has a tally of at least $L$ for any value, all honest processes set 0. Otherwise let $x$ be the unique value of Lemma 2, and let $m$ and $M$ be the least and the largest $tally_i(x)$ over honest $i$; by Lemma 1, $M - m \le t$. If $T \le m$, every honest process sets $x$; if $T > M$, every honest process sets 0. The honest values differ only if $m < T \le M$. This cannot hold for both $T = L$ and $T = H = L + t$, because that would need $m < L$ and $M \ge L + t$, so $M - m > t$. So at most one of the two values of the coin splits the honest processes, and the coin avoids it with probability at least $1/2$. $\square$

**Theorem 2 (termination in constant expected rounds).** Let $U$ be the first round at the end of which all honest processes hold the same value. By Lemma 5, $\Pr[U > k] \le 2^{-k}$, so $U$ is finite with probability 1 and $E[U] \le 2$. By Lemma 3 all honest processes decide in round $U + 1$ at the latest, so the expected round of the last decision is at most 3, and each process halts one round after its decision. $\blacksquare$

## Where the bounds and the coin are used

- $n \ge 8t + 1$ is used only in Lemma 3, to make $n - t \ge G$. With $n = 8t$ and $t$ silent faulty processes, honest processes with the same input see $n - t = G - 1$ copies and never decide; the tests run this case.
- $2L > n + t$ (Lemma 2) keeps two processes from keeping different values.
- The gap $H - L = t$ equals the spread of Lemma 1, so the coin has two thresholds that no spread can straddle together. With one fixed threshold the adversary sees it and keeps the honest processes split in every round; the tests show a run of 60 rounds with no decision.
- The secrecy of the coin until the round's messages are sent is what makes Lemma 5 hold; a coin that the adversary learns early is no better than a fixed threshold.
