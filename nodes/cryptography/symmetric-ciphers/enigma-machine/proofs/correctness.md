---
title: Enigma decrypts in the same setting, never fixes a letter, and has paired cycles
proves: [correctness]
status: full
---

Work in the symmetric group on $\mathbb{Z}_{26}$ and compose from right to left. At a fixed rotor position, let $R_L, R_M, R_R$ be the rotor maps of line L5, $U$ the reflector and $S$ the plugboard. The reflector is a product of 13 disjoint swaps, so $U^2 = 1$ and $U(x) \ne x$ for all $x$. The plugboard is a product of disjoint swaps, so $S^2 = 1$ and $S^{-1} = S$.

**Claim 1.** The letter map of lines L4 to L8 is $E = T^{-1} U T$ with $T = R_L R_M R_R S$, and $E^2 = 1$ and $E(x) \ne x$ for every letter $x$.

*Proof.* Line L4 applies $S$, line L5 applies $R_R$, then $R_M$, then $R_L$, line L6 applies $U$, line L7 applies $R_L^{-1}$, then $R_M^{-1}$, then $R_R^{-1}$, and line L8 applies $S = S^{-1}$. So $E = S^{-1} R_R^{-1} R_M^{-1} R_L^{-1} U R_L R_M R_R S = T^{-1} U T$. Then $E^2 = T^{-1} U T T^{-1} U T = T^{-1} U^2 T = 1$. If $E(x) = x$, then $U(T(x)) = T(x)$, so $U$ has a fixed point, which is false. $\square$

**Claim 2.** For every start position and every text, ENIGMA applied to the output with the same settings returns the text.

*Proof.* Line L3 computes the positions from the start position and the number of letters processed so far, and from nothing else. So the $i$-th letter of the text and the $i$-th letter of the ciphertext are processed at the same position, with the same map $E_i$. The $i$-th output letter is $E_i(x_i)$, and processing it again gives $E_i(E_i(x_i)) = x_i$ by Claim 1. $\square$

**Claim 3.** No letter encrypts to itself. So in a crib placement, an offset where a crib letter equals the cipher letter above it is impossible.

*Proof.* The $i$-th output letter is $E_i(x_i) \ne x_i$ by Claim 1. If the crib sat at that offset, some plaintext letter would equal its own cipher letter. $\square$

**Claim 4 (Rejewski).** Let $A$ and $B$ be permutations of a finite set with $A^2 = B^2 = 1$ and no fixed points. Then the cycles of $X = BA$ come in pairs of equal length.

*Proof.* First, $A X A = A B A A = A B = B^{-1} A^{-1} = (BA)^{-1} = X^{-1}$, so $A X^k = X^{-k} A$ for every integer $k$. Take a cycle $C = \{x, Xx, \ldots, X^{L-1} x\}$ of $X$ of length $L$. Then $A X^k x = X^{-k} (A x)$, so $A$ maps $C$ onto the cycle $C'$ of $X$ that contains $Ax$, which has the same length $L$.

Suppose $C' = C$, so $A x = X^j x$ for some $j$. Then $A X^k x = X^{-k} X^j x = X^{j-k} x$, so on $C$ the map $A$ sends the point with index $k$ to the point with index $j - k \bmod L$. Since $B = X A^{-1} = X A$, the map $B$ sends the index $k$ to $j - k + 1 \bmod L$. A fixed point of $A$ on $C$ is an index $k$ with $2k \equiv j \pmod L$, and a fixed point of $B$ is an index $k$ with $2k \equiv j + 1 \pmod L$. If $L$ is odd, 2 is invertible modulo $L$, and both congruences have a solution. If $L$ is even, one of $j$ and $j + 1$ is even, say $2m$, and $k = m$ solves the corresponding congruence. In both cases $A$ or $B$ has a fixed point, which is false. So $C' \ne C$.

So $A$ maps each cycle $C$ to a different cycle $C'$ of the same length, and since $A^2 = 1$ it maps $C'$ back to $C$. These pairs $\{C, C'\}$ partition the cycles of $X$. $\square$

**Claim 5.** The cycle type of a product $A_j A_i$ of two letter maps does not depend on the plugboard.

*Proof.* By Claim 1, $A_i = S^{-1} V_i S$ with $V_i = Q_i^{-1} U Q_i$ and $Q_i = R_L R_M R_R$ at position $i$, which does not involve $S$. Then $A_j A_i = S^{-1} V_j S S^{-1} V_i S = S^{-1} (V_j V_i) S$, a conjugate of $V_j V_i$. Conjugate permutations have the same cycle type. $\square$

**Claim 6.** The number of ways to place $c$ cables on $n$ letters is $n! / ((n - 2c)! \, c! \, 2^c)$.

*Proof.* List the $n$ letters in one of $n!$ orders, and pair the first two, the next two, and so on up to $2c$ letters; leave the last $n - 2c$ letters unplugged. Each placement arises from exactly $(n-2c)! \cdot c! \cdot 2^c$ orders: the unplugged letters may be in any order, the $c$ pairs in any order, and the two letters of each pair in either order. $\square$

Claims 1 and 2 prove that the simulator decrypts what it encrypts. Claim 3 is the property behind crib placement, Claims 4 and 5 are the facts behind Rejewski's characteristic, and Claim 6 gives the plugboard term of the key count. $\blacksquare$
