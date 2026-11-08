---
title: WELL512a has period 2^512 - 1 from every non-zero state and is maximally equidistributed
proves: [correctness]
status: full
---

Identify a 32-bit word with a vector in $\mathrm{GF}(2)^{32}$, so that XOR is addition, and the WELL512a state, read in logical order $v_{n,0}, \ldots, v_{n,15}$ starting at index $i$, with a vector $V_n \in \mathrm{GF}(2)^{512}$. Every operation in lines L1 to L5 is a XOR, a shift within 32 bits, or an AND with a constant mask, so each new word is a linear function of the old words. Line L6 only moves the index, which relabels positions: the new logical order is $v_{n+1,0} = $ the word written in L5, $v_{n+1,1} = $ the word written in L4, and $v_{n+1,j} = v_{n,j-1}$ for $2 \le j \le 15$. Hence $V_{n+1} = A V_n$ for a fixed $512 \times 512$ matrix $A$ over $\mathrm{GF}(2)$, and the output of line L7 is $v_{n+1,0}$, the first 32 coordinates of $A V_n$, a linear function of $V_n$. Let $P$ be the characteristic polynomial of $A$.

**Lemma 1 (period).** If $P$ is primitive, every non-zero state has period exactly $2^{512} - 1$, so one period visits every non-zero state once.

*Proof.* A primitive $P$ is irreducible with $P(0) = 1$, so $A$ is invertible, its minimal polynomial is $P$, and $\mathrm{GF}(2)[A] \cong \mathrm{GF}(2)[z]/(P)$ is a field of $2^{512}$ elements in which $A$, the image of $z$, has order $N = 2^{512} - 1$. If a non-zero $V$ has period $\rho$, then $A^\rho - I$ is a field element that kills $V \neq 0$, so it is not invertible, so it is 0, and $N \mid \rho$; also $A^N = I$, so $\rho = N$. There are $N$ non-zero states, so one cycle contains them all. This is Lemmas 2 and 3 of the [xorshift](/xorshift/) proof. $\square$

**Lemma 2 (finding $P$ from the output).** Let $s_n$ be the lowest bit of the $n$-th output from a non-zero seed. If the Berlekamp-Massey algorithm, run on $s_0, \ldots, s_{1023}$, returns linear complexity 512, its polynomial $Q$ equals $P$.

*Proof.* $s_n = h^\top A^{n} W$ for a fixed vector $h$ and $W = A V_0$, and $P(A) = 0$ by Cayley-Hamilton, so the sequence satisfies the recurrence of $P$ and has linear complexity at most 512. A sequence of linear complexity $L \le 512$ is determined by $2 \cdot 512$ consecutive terms, and Berlekamp-Massey returns its minimal polynomial $Q$, which divides every annihilating polynomial, in particular $P$. If $\deg Q = 512 = \deg P$ and both are monic, $Q = P$. $\square$

**Lemma 3 (primitivity test).** Write $N = 2^{512} - 1$. If $z^N \equiv 1 \pmod Q$ and $z^{N/q} \not\equiv 1 \pmod Q$ for every prime $q \mid N$, then $Q$ is primitive.

*Proof.* The order $d$ of $z$ modulo $Q$ divides $N$. If $d < N$, some prime $q$ divides $N/d$, and then $z^{N/q} \equiv 1$, a contradiction. So $d = N$, the $N$ powers of $z$ are distinct non-zero residues, every non-zero residue is a power of $z$ and hence invertible, $\mathrm{GF}(2)[z]/(Q)$ is a field, and $Q$ is irreducible with $z$ of maximal order: primitive. $\square$

**The factorization of $2^{512} - 1$.** Since $(2^{2^i} - 1)(2^{2^i} + 1) = 2^{2^{i+1}} - 1$, induction gives $2^{512} - 1 = F_0 F_1 \cdots F_8$ with the Fermat numbers $F_i = 2^{2^i} + 1$. The tests list 13 numbers, check that their product is exactly $2^{512} - 1$, and prove each one prime: the twelve below $3.3 \cdot 10^{24}$ by the Miller-Rabin test with the first 13 prime bases, which is exact in that range, and the 62-digit factor of $F_8$ by Pocklington's criterion. That criterion says: if $F \mid n - 1$, $F^2 > n$, and for each prime $q \mid F$ some $a$ has $a^{n-1} \equiv 1$ and $\gcd(a^{(n-1)/q} - 1, n) = 1$, then $n$ is prime. For the 62-digit factor, $F$ is the product of the prime powers $2^{11}, 3, 5, 7, 13$, a 14-digit prime and a 43-digit number, which is itself proved prime by Pocklington's criterion with the complete factorization of its predecessor into primes below $3.3 \cdot 10^{24}$.

**Lemma 4 (equidistribution).** For $1 \le \ell \le 32$ and $k \ge 1$, let $\phi_{\ell,k}(V)$ be the vector of the top $\ell$ bits of the first $k$ outputs from state $V$, a linear map $\mathrm{GF}(2)^{512} \to \mathrm{GF}(2)^{\ell k}$. If $\phi_{\ell,k}$ has rank $\ell k$, then over one period each non-zero $\ell k$-bit tuple occurs exactly $2^{512 - \ell k}$ times and the zero tuple $2^{512 - \ell k} - 1$ times.

*Proof.* A surjective linear map has every fibre of size $2^{512 - \ell k}$. By Lemma 1, one period runs through every non-zero state once, and the outputs from consecutive states are consecutive windows of the output sequence; only the zero state, whose fibre is the zero tuple, is missing. $\square$

**Theorem.** WELL512a has period $2^{512} - 1$ from every non-zero state and is maximally equidistributed: for every $\ell = 1, \ldots, 32$, the top $\ell$ bits of $\lfloor 512 / \ell \rfloor$ consecutive outputs are equidistributed in the sense of Lemma 4.

*Proof.* The tests run Berlekamp-Massey on 1024 output bits and get linear complexity 512, so by Lemma 2 they obtain $P$; they verify the conditions of Lemma 3 with exact polynomial arithmetic and the proved factorization, so $P$ is primitive and Lemma 1 gives the period. For equidistribution, the tests build $\phi_{\ell,k}$ column by column, as the images of the 512 unit states (linearity), and find rank $\ell k$ with $k = \lfloor 512/\ell \rfloor$ for every $\ell$, so Lemma 4 applies. $\blacksquare$

The same tests find that $P$ has 225 non-zero coefficients. That number, and the speed of escape from states with few ones, are the WELL design criteria; they are measured, not part of the theorem.
