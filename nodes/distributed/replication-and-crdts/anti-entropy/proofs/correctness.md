---
title: Anti-entropy converges, the Merkle comparison is exact, and the round recurrences
proves: [correctness]
status: full
---

**Setting.** Replicas run lines L1 to L8 in the asynchronous model with crash-recovery failures; a replica keeps its stored entries across a crash. An entry is a pair (stamp, value), and stamps are pairs (time, replica id) ordered lexicographically, so distinct writes have distinct stamps. For a key $k$ and a replica $x$, let $e_x(k)$ be the entry of $x$ for $k$, or $\bot$ if $x$ has none, with $\bot$ below every entry.

**Lemma 1 (monotone entries).** For every $x$ and $k$, $e_x(k)$ never decreases, and it is always $\bot$ or an entry written by some write.

*Proof.* Only line L5 changes $e_x(k)$: a local write is also merged by line L5, with its new stamp. Line L5 stores $e$ only when $e$ is larger. Line L5 stores entries that it receives from another replica, which by induction are written entries. $\square$

**Lemma 2 (Merkle comparison is exact).** Assume the hash function has no collision on the values compared. Then MERKLE-DIFF of two trees with the same bucket split returns exactly the set of keys $k$ with $e_p(k) \ne e_q(k)$.

*Proof.* By induction on the height of the nodes. For leaves: the leaf hash is a function of the sorted list of the bucket's entries, so with no collision, equal hashes mean equal lists, and line L6 returns $\emptyset$ correctly; different hashes mean the lists differ, and line L7 returns exactly the keys of the bucket whose entries differ. For an inner node $u$ with children $u_\ell$ and $u_r$: its hash is a function of the two child hashes, so equal hashes mean equal child hashes and, by induction, equal contents below $u$, and line L6 is correct. Otherwise line L8 returns the union of the two exact answers for the children. The buckets of the two children partition the keys below $u$, so the union is exact. $\square$

With a hash of $b$ bits modelled as random, a node whose contents differ has equal hashes with probability $2^{-b}$, so a session with $d$ differing keys and $B$ buckets misses a difference with probability at most $(1 + 2d \log_2 B) 2^{-b}$.

**Lemma 3 (a push-pull session).** After a push-pull session between $p$ and $q$, $e_p(k) = e_q(k) = \max(e_p(k), e_q(k))$ for every key $k$, where the entries are those at the start of the session.

*Proof.* By Lemma 2, $D$ is the set of keys on which they differ. For $k \notin D$ the claim is immediate. For $k \in D$, line L3 merges $e_p(k)$ into $q$ and line L4 merges $e_q(k)$ into $p$, when they exist, and line L5 keeps the larger entry at both. $\square$

**Theorem 1 (convergence).** Suppose that after some time there are no writes, every replica is up, messages between up replicas arrive, and every replica keeps starting push-pull sessions with partners chosen uniformly at random. Then with probability 1, there is a time after which every replica holds, for every key $k$, the largest entry $e^*(k)$ written for $k$.

*Proof.* Fix $k$. By Lemma 1, some replica $r$ holds $e^*(k)$ from the time writes stop, and every replica that holds it keeps it, since no entry is larger. Let $x$ be a replica without it. In each round, $x$ calls $r$ with probability $1/(n - 1) > 0$, so with probability 1 it eventually does, and by Lemma 3 it then holds $e^*(k)$. There are finitely many keys and replicas, so with probability 1 all of them reach $e^*$. $\square$

The same argument works for push alone when the holder of $e^*(k)$ calls $x$, and for pull alone when $x$ calls the holder; both happen with probability 1. By Lemma 1, the final state does not depend on the order of sessions, on lost sessions, or on repeated ones.

**The recurrences.** Consider one update, a large $n$, and a fraction $p_i$ of the replicas that lack it at the start of round $i$, in the random phone call model.

- *Pull.* A replica that lacks the update still lacks it after round $i$ only if its pull went to a replica that also lacks it. Ignoring pushes, this happens with probability $p_i$ (up to a factor $1 + O(1/n)$), so $\mathrm{E}[p_{i+1}] = p_i^2$.
- *Push.* A replica $x$ that lacks the update gets it only if some replica that has it calls $x$. Each of the $n(1 - p_i)$ informed replicas calls $x$ with probability $1/(n - 1) \approx 1/n$, independently, so $\mathrm{E}[p_{i+1}] = p_i (1 - 1/n)^{n(1 - p_i)} \approx p_i e^{-(1 - p_i)}$, which is about $p_i e^{-1}$ once $p_i$ is small.
- *Push-pull.* Both events must fail, so $\mathrm{E}[p_{i+1}] \approx p_i^2 e^{-(1 - p_i)}$.

Under pull, once $p_i \le 1/2$, the fraction squares in each round, so $p_i$ falls below $1/n$ after $O(\log \log n)$ more rounds. Under push, it falls by a factor of about $e$ per round, which takes about $\ln n$ rounds. In the early phase, while the informed fraction is small, push and pull each about double the number of informed replicas per round, which takes about $\log_2 n$ rounds, and push-pull about triples it. This gives the counts $\log_2 n + \ln n + O(1)$ for push, proved with high probability by Frieze and Grimmett (1985) and Pittel (1987), and $\log_3 n + O(\log \log n)$ for push-pull, proved by Karp et al. (2000). The tests compare these counts and recurrences with simulation.
