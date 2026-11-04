---
title: The false positive rate of a cuckoo filter
proves: [complexity]
status: full
---

**Model.** Assume ideal hashing: for a key $x \notin S$, the pair $(\phi(x), i_1(x))$ is uniform on $\{1, \ldots, 2^f - 1\} \times \{0, \ldots, m-1\}$ and independent of the table $T$ and of the victim, which depend only on the hashes of other keys, on $g$ and on the random choices of the inserts. Fix $T$, the victim and $g$. Write $q = 2^f - 1$.

**Theorem.** $\Pr[\text{QUERY}(x) = \text{true}] \le (b + \bar{b} + 1)/q \le (2b+1)/q$, where $\bar{b} \le b$ is the mean number of entries in a bucket.

*Proof.* QUERY$(x)$ returns true only if $\phi(x)$ is in $T[i_1]$, in $T[\mathrm{alt}(i_1, \phi(x))]$ or in the victim slot. By the [union bound](/union-bound/) it is enough to bound the three probabilities.

*First bucket.* Fix $i_1$. The bucket $T[i_1]$ holds at most $b$ fingerprints, so at most $b$ values of $\phi(x)$ match one of them. Each has probability $1/q$, so the probability is at most $b/q$.

*Second bucket.* For a fingerprint value $\phi$ and a stored entry $(j, \psi)$, the entry is in bucket $\mathrm{alt}(i_1, \phi)$ and matches only if $\psi = \phi$ and $j = \mathrm{alt}(i_1, \phi)$, that is $i_1 = \mathrm{alt}(j, \psi)$ by the involution. So the expected number of matching entries is
$$ \sum_{(j, \psi)} \Pr[\phi(x) = \psi] \Pr[i_1(x) = \mathrm{alt}(j, \psi)] = \frac{N}{q m} = \frac{\bar b}{q}, $$
where the sum is over the $N$ stored entries, and the two events are independent. The probability of at least one match is at most this.

*Victim.* The victim has one fingerprint, matched with probability at most $1/q$. $\square$

**Fingerprint size.** For the rate to be at most $\varepsilon$ it suffices that $(2b+1)/(2^f - 1) \le \varepsilon$, which holds for $f \ge \log_2((2b + 1)/\varepsilon + 1)$, and for $b = 4$ this is about $\log_2(1/\varepsilon) + 3.2$. The paper uses the simpler estimate $2b/2^f$.

**Time.** QUERY reads two buckets of $b$ slots and the victim, so it takes $\Theta(b)$ time in the worst case on the word RAM. DELETE does the same and may run one insert of the victim. An insert takes $O(b)$ time when line L4 succeeds and $O(b \cdot \text{MaxKicks})$ in the worst case. $\blacksquare$
