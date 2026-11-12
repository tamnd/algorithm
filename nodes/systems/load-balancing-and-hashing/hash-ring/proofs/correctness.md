---
title: The sorted array of a hash ring answers successor queries correctly, its arcs partition the ring, and an insert or remove changes the arc of one other point only
proves: [correctness]
status: full
---

The ring is $\mathbb{Z}_R = \{0, \ldots, R - 1\}$ with wrap-around. The *clockwise distance* from $x$ to $p$ is $d(x, p) = (p - x) \bmod R$. The structure holds a set $P$ of $N$ points with owners, in an array $pos$, and the representation invariant is

> **(I)** $pos[0] < pos[1] < \cdots < pos[N-1]$, and $owner[i]$ is the owner of the point $pos[i]$.

The *successor* of $x$ is the point $p \in P$ with the least $d(x, p)$; it is unique because the points are distinct. The *arc* of the point $pos[i]$ is the set of positions $\{x : \mathrm{succ}(x) = pos[i]\}$. We use the pseudocode of the page.

## Lemma 1 (the invariant is kept)

**Claim.** RING-INSERT and RING-REMOVE keep (I).

*Proof.* RING-INSERT finds at line L4 the least $i$ with $pos[i] \ge p$, by [binary search](/binary-search/), which is correct on a sorted array. Line L5 rejects $p$ if $pos[i] = p$. Otherwise $pos[i-1] < p < pos[i]$ (with the missing ends left out), and line L6 places $p$ between them, so the array stays strictly increasing. RING-REMOVE deletes one entry, and a subsequence of a strictly increasing sequence is strictly increasing. In both cases the owner array is changed at the same index. $\square$

## Lemma 2 (successor)

**Claim.** Under (I) with $N \ge 1$, RING-SUCCESSOR returns the successor of $x$.

*Proof.* Let $i$ be the index from line L1. If $i < N$, then $d(x, pos[i]) = pos[i] - x$. For $j > i$, $d(x, pos[j]) = pos[j] - x$ is larger. For $j < i$, $pos[j] < x$, so $d(x, pos[j]) = pos[j] - x + R$, and this is larger than $pos[i] - x$ because $pos[i] < R \le pos[j] + R$. If $i = N$, every point lies below $x$, every distance is $pos[j] - x + R$, and the least is at $j = 0$, which line L2 selects. $\square$

## Lemma 3 (arcs)

**Claim.** Under (I) with $N \ge 2$, the arc of $pos[i]$ is the half-open circular interval $(pos[i-1], pos[i]]$, with $pos[-1] = pos[N-1]$, and it has $(pos[i] - pos[i-1]) \bmod R$ positions. With $N = 1$ the single point owns the whole ring. The arcs of the $N$ points partition the ring, so their lengths add up to $R$.

*Proof.* Each position $x$ has exactly one successor, so the arcs are disjoint and cover the ring. Let $a = pos[i-1]$ and $b = pos[i]$, and take $x$ in the circular interval $(a, b]$, that is $0 < d(a, x) \le d(a, b)$. Then $d(x, b) = d(a, b) - d(a, x) < d(a, b)$. The point $a$ has $d(x, a) = R - d(a, x) > d(a, b) - d(a, x) = d(x, b)$, because $d(a, b) < R$. Any other point $q \ne a, b$ lies outside $(a, b]$ by (I), since $a$ and $b$ are consecutive, so $d(a, q) > d(a, b) \ge d(a, x)$ and $d(x, q) = d(a, q) - d(a, x) > d(a, b) - d(a, x) = d(x, b)$. So $b$ is the successor of $x$. The $N$ intervals $(pos[i-1], pos[i]]$ together cover the ring, so each arc is exactly its interval. $\square$

## Lemma 4 (local change)

**Claim.** Inserting a point $p$ changes the successor of exactly the positions in $(a, p]$, where $a$ is the point before $p$; they all had the successor $b = \mathrm{succ}(p)$ before, and they get $p$. Removing a point $p$ gives its whole arc to the next point clockwise and changes nothing else.

*Proof.* Before the insert, $(a, b]$ is the arc of $b$ by Lemma 3, and $p$ lies in it. After the insert the arcs are $(a, p]$ for $p$ and $(p, b]$ for $b$, and every other arc is unchanged, since its two end points are unchanged. Removal is the reverse of an insert. $\blacksquare$

**Consequence.** If the owners are servers and the keys hash to positions, an insert moves only keys that land in $(a, p]$, all to the owner of $p$, and a removal moves only the keys of the arc of $p$, all to one owner. This is the [monotonicity property](/monotonicity-property/) of consistent hashing at the level of single points.
