---
title: Ring lookup returns the first point clockwise, adding a server moves keys only to it, and the expected share that moves is 1/(n+1), against n/(n+1) for mod-n hashing
proves: [correctness]
status: full
---

We use the pseudocode of the page. The ring is the set $\{0, 1, \ldots, R - 1\}$ of positions, with $R = 2^{64}$ in the code. The *clockwise distance* from $x$ to $p$ is $(p - x) \bmod R$. The ring holds a finite set $P$ of points, each with an owner. The arrays $pos$ and $owner$ list the points in increasing order of position, and no two points share a position (the code rejects a collision).

**Definition.** The *successor* $\mathrm{succ}_P(x)$ of a position $x$ is the point $p \in P$ with the least clockwise distance from $x$. It is unique because the positions are distinct. The owner of key $k$ is the owner of $\mathrm{succ}_P(h(k))$.

## Lemma 1 (lookup)

**Claim.** If $P$ is not empty, CH-LOOKUP returns the owner of $\mathrm{succ}_P(h(key))$.

*Proof.* Let $x = h(key)$ (line L1) and $N = |P|$. Line L2 finds by [binary search](/binary-search/) the least index $i$ with $pos[i] \ge x$, or $i = N$ if there is none.

If $i < N$, the point $pos[i]$ has clockwise distance $pos[i] - x \ge 0$. Every point $pos[j]$ with $j < i$ has $pos[j] < x$ and clockwise distance $pos[j] - x + R$, which is larger than $pos[i] - x$ because $pos[i] < R \le pos[j] + R$. Every point with $j > i$ has $pos[j] > pos[i]$, so its distance $pos[j] - x$ is larger. So $pos[i]$ is the successor.

If $i = N$, every point is below $x$, and the clockwise distance of $pos[j]$ is $pos[j] - x + R$, which is least for the least $pos[j]$, that is $pos[0]$. Line L3 sets $i = 0$. Line L4 returns the owner of $pos[i]$ in both cases. $\square$

## Lemma 2 (monotonicity when a server joins)

**Claim.** Let $Q$ be the points of a new server $s$, with $Q \cap P = \emptyset$. For every key, the owner after the insert is either the owner before the insert or $s$.

*Proof.* Fix $x = h(key)$. The successor in $P \cup Q$ is the point of least clockwise distance in $P \cup Q$. If this point lies in $P$, it has the least distance among the points of $P$ as well, so it is $\mathrm{succ}_P(x)$ and the owner does not change. Otherwise it lies in $Q$, and the owner is $s$. Lines L5 and L6 insert the points of $Q$ in sorted order, so after the insert the arrays describe $P \cup Q$ and Lemma 1 applies. $\square$

## Lemma 3 (when a server leaves)

**Claim.** Let server $s$ own the points $Q \subseteq P$. After lines L7 and L8 remove $Q$, a key changes owner only if its owner was $s$.

*Proof.* Apply Lemma 2 to the ring $P \setminus Q$ and the joining server $s$: for every key, the owner in $P$ is either the owner in $P \setminus Q$ or $s$. So if the owner in $P$ is not $s$, it equals the owner in $P \setminus Q$. $\square$

## Lemma 4 (how many keys move)

**Model.** The positions $h(s, r)$ of the points and the positions $h(k)$ of the keys are independent and uniform on the ring, and positions do not collide. (For $R = 2^{64}$ and a good hash function this is a close model; collisions have probability about $N^2/R$.)

**Claim.** Let $n$ servers each have $v$ points, and let a new server with $v$ points join. The expected fraction of keys that change owner is exactly $1/(n+1)$.

*Proof.* By Lemma 2, a key moves exactly when its new owner is the new server. Consider the ring after the join, with $n + 1$ servers. The joint law of all points is symmetric under a permutation of the servers, because each server's $v$ points are independent and uniform. So for a fixed key the new owner is each of the $n + 1$ servers with the same probability, $1/(n+1)$. By linearity of expectation the expected fraction of keys that move is $1/(n+1)$. $\square$

## Lemma 5 (mod-n hashing moves most keys)

**Claim.** Let $x$ be uniform on $\{0, 1, \ldots, M - 1\}$, where $n(n+1)$ divides $M$. Then $\Pr[x \bmod n = x \bmod (n+1)] = 1/(n+1)$. So when the mod-$n$ scheme goes from $n$ to $n + 1$ servers, a key moves with probability $n/(n+1)$.

*Proof.* Since $n(n+1)$ divides $M$, the residue $y = x \bmod n(n+1)$ is uniform on $\{0, \ldots, n(n+1) - 1\}$, and $x \bmod n = y \bmod n$, $x \bmod (n+1) = y \bmod (n+1)$. Suppose $y \bmod n = y \bmod (n+1) = r$. Then $r < n$, and $y - r$ is divisible by $n$ and by $n + 1$, which are coprime, so by $n(n+1)$. As $0 \le y < n(n+1)$, this means $y = r$. Conversely each $y = r \in \{0, \ldots, n-1\}$ has both residues equal to $r$. So exactly $n$ of the $n(n+1)$ values of $y$ keep their server, and the probability is $n/(n(n+1)) = 1/(n+1)$. $\blacksquare$

For $R = 2^{64}$ the divisibility holds only approximately; the error is at most $n(n+1)/R$.

## Balance

By the same symmetry as in Lemma 4, each server owns each key with probability $1/n$, so the expected load of each server is $1/n$ of the keys. The largest share is larger: $\Theta(\log n/n)$ with one point per server and $(1 + \epsilon)/n$ with $v = \Theta(\log n)$ points, which is proved on the page of the [consistent hashing load bound](/consistent-hashing-max-load-bound/).
