---
title: REV, KLA and Comb are plausible clocks
proves: [correctness]
status: full
---

We use the model of the page: $n$ sites, asynchronous message passing, channels that need not be FIFO. Each event is one call of TICK, SEND or RECEIVE. For an event $e$ we write $s(e)$ for its site and $V(e)$ for the vector part of its stamp. The relation $\to$ is [happened-before](/happened-before/). A clock with relation $\to_P$ is *plausible* if (P1) two stamps are equal as stamps only for the same event, and (P2) $a \to b$ implies $a \to_P b$. We also show (P3): $a \to_P b$ and $b \to_P a$ never hold together, so a causal pair is never reported in the wrong direction.

Every chain for $a \to b$ is a sequence of steps of two kinds: from an event to a later event of the same site, and from a send to its receive. Each step goes forward in the run.

## REV with $R$ entries

Write $\rho(i) = i \bmod R$. For REV, "equal as stamps" means the same site and the same value of entry $\rho$ of that site.

**Lemma 1.** Along one site, $V$ never decreases in any entry, and entry $\rho(i)$ of site $i$ grows by at least 1 at each event.

*Proof.* Line L6 only replaces an entry by a maximum that includes the old value. Line L2 adds 1 to entry $\rho(i)$. No other line changes $V$. $\square$

**Lemma 2.** If $a \to b$, then $V(a) \le V(b)$ in every entry.

*Proof.* By Lemma 1 for a step on one site. For a step from a send $u$ to its receive $w$, the message carries $V(u)$ (line L4), and line L6 makes each entry at least the entry of $V(u)$. Line L2 does not decrease an entry. The relation $\le$ is transitive, so it holds along the chain. $\square$

**Theorem 1.** REV is plausible and satisfies (P3).

*Proof.* (P1): two different events of one site differ in entry $\rho$ of that site by Lemma 1, and stamps of different sites have different site fields.

(P2): let $a \to b$. If $s(a) = s(b) = i$, then $a$ comes before $b$ on site $i$ and Lemma 1 gives $V(a)[\rho(i)] < V(b)[\rho(i)]$, which is the test of line L8. Let $s(b) = j \ne s(a)$. The last step of a chain for $a \to b$ goes from an event $q$ to $b$, with $q = a$ or $a \to q$, so $V(a) \le V(q)$ by Lemma 2. If $q$ is the event before $b$ on site $j$, the vector at the start of $b$ is $V(q)$. If $q$ is the send of the message that $b$ receives, line L6 makes the vector at least $V(q)$. In both cases line L2 then adds 1 to entry $\rho(j)$. So $V(b)[\rho(j)] \ge V(q)[\rho(j)] + 1 > V(a)[\rho(j)]$. With $V(a) \le V(b)$ from Lemma 2, the test of line L9 holds.

(P3): for one site, the test of line L8 is a strict order on a number. For two sites $i \ne j$, assume both $a \to_P b$ and $b \to_P a$. Line L9 gives $V(a) \le V(b)$ and $V(b) \le V(a)$, so $V(a) = V(b)$, and it also gives $V(a)[\rho(j)] < V(b)[\rho(j)]$. This is a contradiction. $\blacksquare$

## KLA with $K \ge 2$ entries

For KLA, "equal as stamps" means the same site and the same entry 0.

**Lemma 3.** In each state of each site, $V[0] \ge V[1] \ge \cdots \ge V[K-1]$. In the stamp of each event, $V[0] > V[1]$.

*Proof.* By induction over the steps of the run. The zero vector satisfies the first claim. A local event or a send adds 1 to entry 0 only, which keeps the order and makes $V[0] > V[1]$. A receive with message vector $W$, which satisfies the claim by induction, sets $V'[0] = \max(V[0], W[0]) + 1$ and $V'[k] = \max(V[k], W[k-1])$ for $k \ge 1$. For $k \ge 1$, $V[k] \ge V[k+1]$ and $W[k-1] \ge W[k]$ give $V'[k] \ge V'[k+1]$. Also $V'[0] > \max(V[0], W[0]) \ge \max(V[1], W[0]) = V'[1]$. $\square$

**Lemma 4.** Along one site, each entry never decreases and entry 0 grows by at least 1 at each event. For a send $u$ and its receive $w$, $V(w)[k] \ge V(u)[k]$ for each $k$, and $V(w)[k+1] \ge V(u)[k]$ for $k \le K-2$. So $a \to b$ implies $V(a) \le V(b)$ in every entry.

*Proof.* The first sentence follows from the rules, since each new entry is a maximum that includes the old one, and entry 0 also gets $+1$. At $w$, $V(w)[k+1] \ge W[k] = V(u)[k]$ by the rule. For $k \ge 1$, $V(w)[k] \ge W[k-1] \ge W[k]$ by Lemma 3, and $V(w)[0] > W[0]$. The last claim follows along a chain by transitivity. $\square$

**Theorem 2.** KLA is plausible and satisfies (P3).

*Proof.* (P1): by Lemma 4, entry 0 strictly grows along one site.

(P2): let $a \to b$. If $s(a) = s(b)$, entry 0 of $a$ is smaller by Lemma 4. If $s(a) \ne s(b)$, a chain for $a \to b$ has at least one message step, since steps on one site do not change the site. Let $u \to w$ be the last message step of the chain. After it, the chain stays on one site, so $w$ is $b$ or an earlier event of the site of $b$. Then, for each $k \le K - 2$,

$$V(a)[k] \le V(u)[k] \le V(w)[k+1] \le V(b)[k+1],$$

by Lemma 4 (for $a = u$ or $a \to u$), by the receive rule, and by Lemma 4 along the site of $b$. This is the test of KLA for two sites.

(P3): for one site, the test compares entry 0 with $<$. For two sites, both directions would give $V(a)[0] \le V(b)[1] < V(b)[0] \le V(a)[1] < V(a)[0]$ by the test and Lemma 3, which is a contradiction. $\blacksquare$

## Comb

**Theorem 3.** Comb, which reports $a \to_P b$ only when both REV and KLA report it, is plausible and satisfies (P3). The set of concurrent pairs that it orders is contained in the set that REV orders and in the set that KLA orders.

*Proof.* (P1) holds because the REV part already separates different events. (P2): if $a \to b$, both parts report $a \to_P b$ by Theorems 1 and 2. (P3) holds because it holds for REV. The last claim is the definition of the conjunction. $\blacksquare$

Since the clocks never miss a causal pair, a pair that a plausible clock reports as concurrent (neither $\to_P$ nor equal) is truly concurrent. The only error is the other one: a concurrent pair can be reported as ordered.
