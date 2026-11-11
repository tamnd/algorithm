---
title: Scuttlebutt keeps the invariant C(p, q), sends no delta the receiver has, and converges after the writes stop
proves: [correctness]
status: full
---

**Setting.** Participants $1, \dots, n$ run lines L1 to L8. Versions are positive integers, and $0$ stands for "no mapping" (the $\perp$ of the paper). For a participant $r$ and a key $k$, let $c_r(k)$ be the current version of $k$ at $r$, that is, the version of $\mu_r(r)(k)$. An exchange between $p$ and $q$ is atomic: $q$ builds its delta set for $p$ from its state and $p$'s digest, $p$ builds its delta set for $q$ in the same way, and then each applies what it received (lines L7 and L8). Messages are at most $mtu \ge 1$ deltas long, and the order used at lines L4 to L6 may be any order that satisfies the ordering constraint: for each $r$, the deltas of $r$ in a message are the deltas of $A(r)$ with the smallest versions.

**Lemma 1 (origin of versions).** At all times, for all $p$, $r$ and $k$: the pair $\mu_p(r)(k)$ is a pair that $r$ wrote for $k$ at line L1 (or the empty pair); its version is at most $c_r(k)$; and $\max_p(r) \le \max_r(r)$.

*Proof.* By induction on the steps. Initially all copies are empty and all maxima are $0$. A write at $r$ (line L1) creates a pair of $r$ with a version above every earlier version of $r$, so it raises $c_r(k)$ and $\max_r(r)$ and keeps all three claims for every copy. An exchange copies, at lines L7 and L8, pairs and versions that the sender holds, which satisfy the claims by the induction hypothesis; line L7 keeps the larger version and line L8 the larger maximum, so the claims still hold. $\square$

**Lemma 2 (every delta is news).** If $q$ receives a delta $(r, k, v, n)$ in an exchange, then $n$ is larger than the version of $\mu_q(r)(k)$ when the delta arrives, so line L7 replaces the copy.

*Proof.* The sender put the delta in $A(r)$ at line L4 only if $n > d(r)$, where $d(r) = \max_q(r)$ from $q$'s digest. Within an atomic exchange the state of $q$ does not change between its digest and the arrival of the deltas, except by earlier deltas of the same message. The sender holds one pair per key, so the message has at most one delta for key $k$ of $r$, and the earlier deltas are for other keys. So when the delta arrives, the version of $q$'s copy of $k$ is still at most $\max_q(r) = d(r) < n$. $\square$

**Theorem 1 (the invariant).** For all participants $r$ and $q$, at all times, the paper's invariant holds:

$$C(r, q):\quad \text{for every key } k \text{ of } r,\quad \mu_q(r)(k) = \mu_r(r)(k) \ \text{ or } \ c_r(k) > \max_q(r).$$

*Proof.* By induction on the steps. Initially every map is empty, so the first disjunct holds for every key.

*A write at $r$ (line L1) to key $k_0$.* The new version $n_0$ is larger than $\max_r(r)$, which is at least $\max_q(r)$ by Lemma 1. So $c_r(k_0) = n_0 > \max_q(r)$ and the second disjunct holds for $k_0$. Other keys and all copies do not change. For $q = r$ the first disjunct holds for every key, since the write changes $\mu_r(r)$ itself.

*An exchange in which $q$ receives a set $S$ of deltas from $p$.* If $S$ has no delta of $r$, then $\mu_q(r)$ and $\max_q(r)$ do not change. Otherwise, let $d = \max_q(r)$ before the exchange and let $n^*$ be the largest version of a delta of $r$ in $S$. After the exchange, $\max_q(r) = \max(d, n^*) = n^*$, because $n^* > d$. Fix a key $k$ of $r$ that is not current at $q$ after the exchange. We show $c_r(k) > n^*$.

- If $k$ was current at $q$ before the exchange, it stays current: line L7 only replaces it with a larger version, and no pair of $k$ has a version above $c_r(k)$ (Lemma 1). So this case does not occur.
- So $k$ was not current before, and by the induction hypothesis $c_r(k) > d$. Suppose, for a contradiction, that $c_r(k) \le n^*$. By Lemma 1, $n^* \le \max_p(r)$, so $c_r(k) \le \max_p(r)$, and by the induction hypothesis for $C(r, p)$, $p$ holds the current pair of $k$, with version $c_r(k)$. That version is above $d$, so the delta $(r, k, \cdot, c_r(k))$ is in $p$'s list $A(r)$ for $q$. Its version is at most $n^*$, and a delta of $A(r)$ with version $n^*$ is in $S$, so by the ordering constraint the delta for $k$ is in $S$ too. By Lemma 2, $q$ applies it, and $k$ is current at $q$ after the exchange, which is a contradiction.

So every key of $r$ that is not current at $q$ has $c_r(k) > n^* = \max_q(r)$, and $C(r, q)$ holds. The exchange does not change $\mu_r(r)$ unless $r$ is $p$ or $q$, and $r$ never receives a delta of its own state: by Lemma 1, $\max_p(r) \le \max_r(r)$, so $A(r)$ for $r$ is empty. $\square$

The proof uses the ordering constraint in one place: if the newest delta of $r$ in the message has version $n^*$, every delta of $r$ with a smaller version that the receiver lacks is in the message too. The same proof works if $q$'s digest is older than its state, as long as the digest is not larger than $\max_q(r)$, because then $A(r)$ only gets larger.

**Corollary 1 (property (3) of the paper).** If $\max_q(r) = \max_r(r)$, then $\mu_q(r) = \mu_r(r)$.

*Proof.* Every key of $r$ has $c_r(k) \le \max_r(r) = \max_q(r)$, so the second disjunct of $C(r, q)$ is false and the first holds for every key. $\square$

**Theorem 2 (convergence).** Suppose that after some time no participant writes and no participant crashes, and each participant picks, in each round, a partner uniformly at random among the others. Then, for every $mtu \ge 1$ and every order that satisfies the constraint, with probability 1 there is a round after which $\mu_p(r) = \mu_r(r)$ for all $p$ and $r$.

*Proof.* Let $\Phi = \sum_{p, r} \sum_{k} \bigl(c_r(k) - v_p(r, k)\bigr)$, where $v_p(r, k)$ is the version of $p$'s copy of $k$ of $r$ and the sum is over the keys of $r$. By Lemma 1 every term is a nonnegative integer, and $\Phi = 0$ exactly when all copies are current. No write happens, so the $c_r(k)$ are fixed. Line L7 only raises versions, so $\Phi$ never grows, and by Lemma 2 every delta that is sent lowers $\Phi$ by at least 1.

Suppose some copy is not current: $\mu_q(r) \ne \mu_r(r)$. By Corollary 1, $\max_q(r) < \max_r(r)$. The key of $r$ with version $\max_r(r)$ is in $r$'s list $A(r)$ for $q$, so in an exchange between $r$ and $q$ the delta set from $r$ is not empty, and at least one delta is sent because $mtu \ge 1$. In each round, $q$ picks $r$ with probability $1/(n - 1)$, independently of the past. So in each round in which $\Phi > 0$, $\Phi$ falls by at least 1 with probability at least $1/(n - 1)$. Since $\Phi$ starts at a finite value, the number of rounds until $\Phi = 0$ is at most a sum of $\Phi$ geometric variables, which is finite with probability 1. $\square$

**Proposition 3 (comparison with push-pull).** Let the writes stop, let $mtu \ge nK$, and fix a participant $r$. Call $p$ current for $r$ when $\mu_p(r) = \mu_r(r)$. In every round, the set of participants that are current for $r$ at the end of the round contains the set that the push-pull rule gives from the set at the start of the round with the same calls: the start set together with every participant that calls, or is called by, a member of the start set.

*Proof.* Take a call in the round between $p$ and $q$, where $p$ was current at the start of the round. Current participants stay current (Theorem 2's proof: versions only grow and never pass $c_r(k)$). If $q$ is not current when the exchange happens, then $\max_q(r) < \max_r(r)$ by Corollary 1. The list $A(r)$ that $p$ builds for $q$ contains every current pair of $r$ with a version above $\max_q(r)$, and with $mtu \ge nK$ the whole delta set fits in the message, so $q$ receives all of them. After the exchange, every key of $r$ with $c_r(k) > \max_q(r)$ is current at $q$, and every other key was current already by $C(r, q)$ (Theorem 1). So $q$ is current. The exchanges of the round run one at a time, and each call of the push-pull rule is one of them, so the claim follows by induction over the calls. $\square$

**Not proved here.** The time bound of push-pull, $\log_3 n + O(\log \log n)$ rounds with high probability, is cited from Karp, Schindelhauer, Shenker and Vöcking (2000). The bound of $O(\log n)$ rounds for all $n$ states together is a sketch: it needs, for each $r$, a failure probability below $1/n$ and a union bound. The comparisons between the orders (scuttle-depth, scuttle-breadth, precise) and the behavior of the flow control are measurements, from the paper and from the simulator, not theorems.
