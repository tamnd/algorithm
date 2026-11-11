---
title: Substitution decryption inverts encryption, and the hill-climbing attack ends with a permutation
proves: [correctness]
status: full
---

We identify A to Z with $\mathbb{Z}_{26}$. A key is a permutation $\pi$ of $\mathbb{Z}_{26}$, and characters that are not letters are copied unchanged.

**Claim 1.** For each key $\pi$ and each message $P$, SUBSTITUTION-ENCRYPT with $\pi$ returns $E_\pi(P)$, and SUBSTITUTION-ENCRYPT with $\pi^{-1}$ applied to $E_\pi(P)$ returns $P$.

*Proof.* Line L1 sets $T[x] = \pi(x)$ for the 26 letters $x$. Lines L2 and L3 set $c_i = T[p_i] = \pi(p_i)$ for each letter $p_i$ and copy each other character, and line L4 returns the result, which is $E_\pi(P)$ by definition. Because $\pi$ is a bijection of a finite set, $\pi^{-1}$ exists, and the second run gives $\pi^{-1}(\pi(p_i)) = p_i$ at each letter position and the copied character at each other position. So it returns $P$. Case is kept in both runs, because the table maps the lower case form of $x$ to the lower case form of $\pi(x)$. $\square$

**Claim 2.** The function `invert_key` returns $\pi^{-1}$.

*Proof.* For each index $i$, it stores the letter $i$ at the position $\pi(i)$. So the output $\sigma$ satisfies $\sigma(\pi(i)) = i$ for each $i$. Since $\pi$ is onto, each position is written exactly once, and $\sigma = \pi^{-1}$. $\square$

**Claim 3.** Each restart of HILL-CLIMB ends after finitely many swaps, and HILL-CLIMB returns a permutation $\sigma$ of $\mathbb{Z}_{26}$.

*Proof.*

1. The start key of line L6 maps the $j$-th cipher letter in the frequency order to the $j$-th English letter in the frequency order. Both orders list each of the 26 letters once, so the key is a permutation.
2. A swap of the images of two letters maps a permutation to a permutation. So the keys of lines L7 and L10 are permutations, and by induction each $\sigma$ that the search holds is a permutation.
3. Let $s$ be the score at the start of a restart. Each accepted swap (line L11) strictly raises $s$. The score is a function of $\sigma$, and $\sigma$ takes at most $26!$ values. So a restart accepts at most $26! - 1$ swaps.
4. Between two accepted swaps, line L12 raises `stale` by 1 at each rejected swap, and the loop of line L9 stops when `stale` reaches $M$. So at most $M$ swaps are rejected in a row, and the restart tries at most $26! \cdot (M + 1)$ swaps in total.
5. Line L13 keeps the best of $R$ permutations, so line L14 returns a permutation. $\square$

**What the claims do not say.** The returned $\sigma$ is a local maximum of the score for single swaps, and the score is only an estimate of how much a text looks like English. So no claim says that $\sigma = \pi^{-1}$. The page shows an example in which the true key has a lower score than the key that HILL-CLIMB returns.

Claims 1 and 2 prove that decryption inverts encryption, and Claim 3 proves that the attack ends and returns a valid key. $\blacksquare$
