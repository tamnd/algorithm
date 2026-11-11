---
title: Playfair decryption inverts encryption on every prepared pair
proves: [correctness]
status: full
---

Let $S$ be a key square: a bijection from the cells $\{0, \ldots, 4\}^2$ to the 25 letters without J. Indices of rows and columns are taken modulo 5. For a letter $x$ write $\rho(x)$ and $\gamma(x)$ for its row and column. Let $E$ be the pair map of lines L3 to L6 and $D$ the same map with $-1$ in place of $+1$.

**Claim 1.** The preparation of line L1 splits the message into pairs $ab$ with $a \ne b$, and removing the fillers that it inserts gives back the letters of the message, with J written as I.

*Proof.* The procedure reads the letters from left to right. At each step it either takes two different letters $a \ne b$ as a pair, or it takes one letter $a$ and adds a filler $f$, where $f = $ X if $a \ne$ X and $f = $ Q if $a = $ X, so $f \ne a$ in both cases. Each step consumes at least one letter, so it ends, and each pair has two different letters. The message letters appear in the pairs in their order, and each pair holds at most one filler, at its second place. $\square$

**Claim 2.** For each pair $ab$ with $a \ne b$, $E(ab) = cd$ is a pair with $c \ne d$, the pair $cd$ falls in the same case of the three rules as $ab$, and $D(cd) = ab$.

*Proof.* Let $a = S[r_1, k_1]$ and $b = S[r_2, k_2]$. Since $a \ne b$ and $S$ is a bijection, $(r_1, k_1) \ne (r_2, k_2)$.

1. *Same row*, $r_1 = r_2$ and so $k_1 \ne k_2$. Then $c = S[r_1, k_1 + 1]$ and $d = S[r_1, k_2 + 1]$. The columns $k_1 + 1 \ne k_2 + 1$ modulo 5, so $c \ne d$, and $c, d$ are in the same row $r_1$. So $D$ applies the row rule with $-1$: it maps $c$ to $S[r_1, k_1] = a$ and $d$ to $S[r_1, k_2] = b$.
2. *Same column*, $k_1 = k_2$ and $r_1 \ne r_2$. The same argument with rows and columns swapped gives $c \ne d$ in the column $k_1$, and $D(cd) = ab$. The pair $cd$ is not in the same row, since $r_1 + 1 \ne r_2 + 1$, so $D$ uses the column rule, as it must.
3. *Rectangle*, $r_1 \ne r_2$ and $k_1 \ne k_2$. Then $c = S[r_1, k_2]$ and $d = S[r_2, k_1]$. These are different cells, so $c \ne d$, and they are in different rows and different columns, so $D$ uses the rectangle rule too. It maps $c$ to $S[\rho(c), \gamma(d)] = S[r_1, k_1] = a$ and $d$ to $S[\rho(d), \gamma(c)] = S[r_2, k_2] = b$.

In each case, $cd$ satisfies the condition of the same rule as $ab$, the conditions of the rules are checked in the same order by $E$ and $D$, and $D(cd) = ab$. $\square$

**Claim 3.** For each message $P$, decryption of PLAYFAIR-ENCRYPT$(P, S)$ returns the prepared plaintext of $P$, the concatenation of the pairs of line L1.

*Proof.* By Claim 1, line L1 gives pairs of different letters, and line L2 encrypts them one by one. By Claim 2 each cipher pair $cd$ has $c \ne d$, so the ciphertext has an even length and splits into the same pairs, and decryption maps each $cd$ back to its $ab$. $\square$

Claims 1 to 3 prove that decryption inverts encryption up to the fillers and the merging of J with I, which the preparation introduces on purpose. $\blacksquare$
