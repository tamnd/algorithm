---
title: The Caesar cipher decrypts correctly, has exactly 26 keys, and the search lists the plaintext
proves: [correctness]
status: full
---

We identify the letters with $\mathbb{Z}_{26} = \{0, \ldots, 25\}$ and write $E_k(p) = (p + k) \bmod 26$ and $D_k(c) = (c - k) \bmod 26$ for one letter. On a string, $E_k$ and $D_k$ act letter by letter (lines L1 to L3).

**Claim 1 (decryption).** For each $k \in \mathbb{Z}$ and each string $P$ over $\mathbb{Z}_{26}$, $D_k(E_k(P)) = P$ and $E_k(D_k(P)) = P$.

*Proof.* Both maps act on each position alone, so it is enough to prove the claim for one letter $p$. Let $c = (p + k) \bmod 26$. Then $c \equiv p + k \pmod{26}$, so $c - k \equiv p \pmod{26}$. Because $0 \le p \le 25$, the remainder $(c - k) \bmod 26$ is $p$. The second equation follows in the same way from $(c - k) + k \equiv c$. $\square$

**Claim 2 (exactly 26 keys).** Two keys $k, k'$ give the same map $E_k = E_{k'}$ if and only if $k \equiv k' \pmod{26}$. So the keys $0, \ldots, 25$ give 26 different maps, and no other key gives a new one.

*Proof.* If $k \equiv k'$, then $p + k \equiv p + k'$ for each $p$, so the maps are equal. If the maps are equal, then they agree on the letter $0$, so $k \bmod 26 = k' \bmod 26$. $\square$

**Claim 3 (the search).** Let $C = E_{k_0}(P)$ for some key $k_0$. Then the list that CAESAR-BREAK returns holds each key of $\{0, \ldots, 25\}$ exactly once, and the decryption with the key $k_0 \bmod 26$ is $P$. If $P$ has a strictly smaller chi-squared score than each other string $D_k(C)$, then the first key of the list is $k_0 \bmod 26$.

*Proof.* The loop of line L4 runs over $k = 0, \ldots, 25$ and gives each key one score, and line L8 sorts these 26 pairs, so each key is in the list once. By Claim 2, the key $k_0 \bmod 26$ gives the same map as $k_0$, and by Claim 1, $D_{k_0}(C) = P$. Line L8 sorts by score with the smallest first. If the score of $P$ is strictly smaller than the score of each other candidate, then the pair of $k_0 \bmod 26$ is first. $\square$

The condition of Claim 3 is a property of the plaintext. It can fail: CHEER and JOLLY are shifts of each other by 7, so for the ciphertext JOLLY of the plaintext JOLLY under the key 0, the candidate CHEER has the smaller score and the search ranks the key 7 first. The search always lists the plaintext; only the ranking is a heuristic. $\blacksquare$
