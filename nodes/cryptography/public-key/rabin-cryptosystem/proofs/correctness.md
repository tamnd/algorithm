---
title: "Rabin decryption returns the encrypted message, and a machine that inverts the squaring map factors the modulus"
proves: [correctness]
status: full
---

Throughout, $p$ and $q$ are distinct odd primes with $p \equiv q \equiv 3 \pmod 4$, and $N = pq$ is the Blum integer of the public key. Write $\mathbb{Z}_N^*$ for the units modulo $N$ and $\mathrm{QR}_N$ for the squares among them. The scheme is the one of the [node page](/rabin-cryptosystem/): encryption is $c = m^2 \bmod N$ for an encoded representative $m$, and decryption is lines 6 to 12.

## Part 1. The four roots

**Lemma 1 (a root modulo a Blum prime).** Let $r \equiv 3 \pmod 4$ be prime and let $a$ be a quadratic residue modulo $r$ with $a \not\equiv 0$. Then $(r+1)/4$ is a positive integer and

$$x_0 = a^{(r+1)/4} \bmod r$$

satisfies $x_0^2 \equiv a \pmod r$.

*Proof.* Since $r \equiv 3 \pmod 4$, $r + 1 \equiv 0 \pmod 4$, so $(r+1)/4$ is an integer, and it is positive because $r \ge 3$. Because $a$ is a residue and $r$ is an odd prime, Euler's criterion gives $a^{(r-1)/2} \equiv 1 \pmod r$. Hence

$$x_0^2 = a^{(r+1)/2} = a^{(r-1)/2 + 1} = a \cdot a^{(r-1)/2} \equiv a \cdot 1 = a \pmod r . \qquad \square$$

This is the whole reason for the congruence $3 \pmod 4$: the square root costs one modular exponentiation and needs no search, unlike the general [Tonelli-Shanks](/modular-square-root/) method.

**Lemma 2 (two roots modulo a prime).** For $r$ an odd prime and $a \not\equiv 0$ a residue modulo $r$, the congruence $x^2 \equiv a \pmod r$ has exactly the two solutions $x_0$ and $r - x_0$, and they are different.

*Proof.* If $x^2 \equiv y^2$ then $r \mid (x-y)(x+y)$, so $x \equiv \pm y$ because $r$ is prime. They differ because $x_0 \equiv -x_0$ would force $r \mid 2x_0$, impossible for odd $r$ and $x_0 \not\equiv 0$. $\square$

**Theorem 3 (four roots, and lines 6 to 10 find them).** Let $c \in \mathrm{QR}_N$. Then $x^2 \equiv c \pmod N$ has exactly four solutions in $\mathbb{Z}_N^*$, and the set computed by lines 6 to 10 of the main block is exactly that set.

*Proof.* By the [Chinese remainder theorem](/chinese-remainder-theorem/) the ring map $\mathbb{Z}_N \to \mathbb{Z}_p \times \mathbb{Z}_q$, $x \mapsto (x \bmod p, x \bmod q)$, is a bijection, and it carries squares to pairs of squares. So $x^2 \equiv c \pmod N$ holds exactly when $x^2 \equiv c \pmod p$ and $x^2 \equiv c \pmod q$ hold together. Each of the two congruences has exactly two solutions by Lemma 2, and $c$ is a residue modulo both primes because it is a residue modulo $N$. The bijection therefore gives $2 \times 2 = 4$ solutions modulo $N$, one for each pair of signs.

Line 6 computes $r_p$ with $r_p^2 \equiv c \pmod p$ and line 7 computes $r_q$ with $r_q^2 \equiv c \pmod q$, both by Lemma 1. Line 8 sets

$$w_p = q \cdot (q^{-1} \bmod p) \bmod N, \qquad w_q = p \cdot (p^{-1} \bmod q) \bmod N ,$$

the standard CRT idempotents: $w_p \equiv 1 \pmod p$ and $w_p \equiv 0 \pmod q$, and the reverse for $w_q$. So

$$u = w_p r_p + w_q r_q \bmod N \ \text{ satisfies } \ u \equiv r_p \ (\mathrm{mod}\ p), \quad u \equiv r_q \ (\mathrm{mod}\ q) ,$$

which is the sign pair $(+, +)$, and $v = w_p r_p - w_q r_q \bmod N$ is the pair $(+, -)$. Then $N - u$ is $(-, -)$ and $N - v$ is $(-, +)$, so the four values $\{u, N-u, v, N-v\}$ realize the four sign pairs and are therefore the four distinct roots. $\blacksquare$

**Remark 4.** The four roots form two pairs $\{u, N-u\}$ and $\{v, N-v\}$ that add to $N$. The test file checks this on the toy key, and the example on the node page shows it for $N = 77$: the roots of 15 are $13, 20, 57, 64$ with $20 + 57 = 13 + 64 = 77$.

**Remark 5 (the permutation).** Exactly one of the four roots is itself in $\mathrm{QR}_N$. The reason is that $-1$ is a non-residue modulo any prime $r \equiv 3 \pmod 4$, so the Legendre symbols of the four roots modulo $(p, q)$ run over $(+,+), (-,-), (+,-), (-,+)$ in some order, and only one of them is $(+,+)$. Therefore squaring is a bijection of $\mathrm{QR}_N$, which is what makes it a [trapdoor permutation](/trapdoor-one-way-function/) and why Blum integers appear in the Blum-Blum-Shub generator.

## Part 2. Decryption returns the message

**Lemma 6 (the encoding is injective and recognizable).** Let ENCODE and DECODE be the maps of the implementation: $\mathrm{ENCODE}(\mathit{msg})$ is the integer whose octet string is $\texttt{0x01} \Vert \mathit{msg} \Vert T(\mathit{msg})$ with $T(\mathit{msg})$ the first two octets of $\mathrm{SHA}\text{-}256(\mathit{msg})$. Then $\mathrm{DECODE}(\mathrm{ENCODE}(\mathit{msg})) = \mathit{msg}$ for every message that fits below $N$.

*Proof.* The leading octet is $\texttt{0x01} \ne \texttt{0x00}$, so the octet length of the integer is exactly $1 + |\mathit{msg}| + 2$ and the conversion from the integer back to octets recovers the same string. DECODE then strips the leading octet, splits off the last two octets, recomputes $T$ on the remainder and compares. The comparison succeeds by construction. $\square$

**Theorem 7 (correctness of decryption).** Let $m = \mathrm{ENCODE}(\mathit{msg})$ with $0 < m < N$ and $\gcd(m, N) = 1$, and let $c = m^2 \bmod N$. Then line 11 returns $\mathit{msg}$, unless one of the three other roots also passes DECODE.

*Proof.* $c$ is a square in $\mathbb{Z}_N^*$, so Theorem 3 says the set of line 10 is the set of its four roots, and $m$ is one of them because $m^2 \equiv c$. Line 11 tries the roots and returns the first one that decodes. By Lemma 6 the root $m$ decodes to $\mathit{msg}$. So the loop returns something, and it returns $\mathit{msg}$ unless an earlier root in the iteration order decoded. $\blacksquare$

**Proposition 8 (the failure probability).** Model $\mathrm{SHA}\text{-}256$ as a [random oracle](/random-oracle-model/). For a fixed message, the probability that a given one of the other three roots passes DECODE is at most $2^{-16}$, so the probability that decryption is ambiguous is at most $3 \cdot 2^{-16} < 2^{-14}$.

*Proof.* A wrong root $m'$ passes only if its octet string starts with $\texttt{0x01}$, has at least three octets, and ends with the two octets $T(\mathit{msg}')$ of its own stripped middle part $\mathit{msg}'$. For a value unrelated to the hash, the chance that the last two octets equal the two octets the oracle assigns to $\mathit{msg}'$ is $2^{-16}$. The union bound over the three other roots gives the second claim. $\square$

Two octets are enough for a study implementation. A deployment that wanted this scheme would use a full hash and a randomized padding, which also repairs the determinism; see the variants on the node page.

**Remark 9 (gcd and the unit condition).** If $\gcd(m, N) > 1$, then $m$ is a multiple of $p$ or of $q$ and the encrypter has factored $N$ by accident. For a random encoded message this happens with probability under $2^{-250}$ for a 512 binary digit modulus, and never in practice. The implementation filters the root list by squaring, so a non-unit input still gives correct behaviour.

**Remark 10 (not every integer is a ciphertext).** Only a quarter of $\mathbb{Z}_N^*$ lies in $\mathrm{QR}_N$. A value that is not a residue has no root, lines 6 and 7 return garbage, the filter of line 10 removes it, and line 12 raises the error. The test file checks this with $c + 1$.

## Part 3. Inverting the squaring map is as hard as factoring

This part is Rabin's theorem. We state it as a reduction with explicit probabilities, in the form the implementation uses.

**Definition 11.** A *root machine* for $N$ is an algorithm $\mathcal{A}$ that on input $c \in \mathrm{QR}_N$ returns some $y \in \mathbb{Z}_N^*$ with $y^2 \equiv c \pmod N$. Nothing is assumed about which of the four roots it returns, except where stated.

**Lemma 12 (a different root splits the modulus).** Let $x, y \in \mathbb{Z}_N^*$ with $x^2 \equiv y^2 \pmod N$ and $y \not\equiv \pm x \pmod N$. Then $\gcd(x - y, N) \in \{p, q\}$.

*Proof.* $N \mid (x-y)(x+y)$. If $p$ and $q$ both divided $x - y$ then $N \mid x - y$ and $y \equiv x$, which is excluded; if neither divided $x - y$ then both would divide $x + y$, giving $y \equiv -x$, also excluded. So exactly one of the primes divides $x - y$ and the other divides $x + y$. Therefore $\gcd(x-y, N)$ is that one prime. $\square$

**Theorem 13 (Rabin 1979).** Let $\mathcal{A}$ be a root machine for $N$ that answers a uniform choice among the four roots, independently of the query. Draw $x$ uniformly from $\mathbb{Z}_N^*$, set $c = x^2 \bmod N$ and $y = \mathcal{A}(c)$. Then

$$\Pr\left[\gcd(x - y, N) \in \{p, q\}\right] = \frac{1}{2} .$$

*Proof.* By Theorem 3 the value $c$ has exactly four roots, and $x$ is one of them. Two of the four are $x$ and $N - x$, and the other two are the pair $\{v, N-v\}$ of the opposite sign pattern. The machine sees only $c$, which does not say which of the four roots $x$ was, so its answer $y$ is independent of that choice: with probability $1/2$ it is in $\{x, N-x\}$ and with probability $1/2$ it is one of the other two. In the second case $y \not\equiv \pm x$ and Lemma 12 gives a prime factor. In the first case $\gcd(x - y, N)$ is $N$ or 1 and the query is wasted. $\blacksquare$

**Remark 14 (a machine that is not uniform).** The theorem as stated assumes a uniform oracle, which is the case the implementation builds and the worst case for the attacker. The general statement is: if $\mathcal{A}$ returns *some* root for a fraction $\epsilon$ of the residues, then the reduction succeeds with probability at least $\epsilon/2$ per query, because the choice of $x$ among the four roots of $c$ is uniform and independent of the fixed answer the machine gives to $c$. The important point is that the machine cannot tell which root was squared, whatever strategy it uses, since $c$ carries no such information.

**Corollary 15 (expected two queries).** Under the hypotheses of Theorem 13, repeating with fresh independent $x$ until a factor appears takes 2 queries on average, and the chance of failure after $t$ queries is $2^{-t}$. After 64 queries the failure probability is below $2^{-64}$.

*Proof.* The trials are independent Bernoulli trials with success probability $1/2$, so the number of trials is geometric with mean 2 and the tail is $2^{-t}$. $\square$

**Theorem 16 (the equivalence).** Inverting the Rabin map on $\mathrm{QR}_N$ and factoring $N$ are equally hard, up to a polynomial factor in the number of binary digits of $N$ and a constant factor in the success probability.

*Proof.* One direction is Theorem 13 with Corollary 15: a root machine gives a factoring algorithm with the same running time up to $O(\log^2 N)$ work per query for the greatest common divisor. The other direction is Part 1: from $p$ and $q$ the roots follow by two modular exponentiations and a CRT recombination, so a factoring algorithm gives a root machine. $\blacksquare$

This is the property that no RSA variant has. For [RSA](/rsa-cryptosystem/) the corresponding statement, that extracting $e$-th roots is as hard as factoring, is not known, and the results of Boneh and Venkatesan suggest that a straight line reduction of that kind would itself give a factoring algorithm. So the [RSA problem](/rsa-problem/) is a separate assumption, while the Rabin problem is factoring in disguise.

## Part 4. The proof is an attack

**Corollary 17 (Rabin encryption is not IND-CCA secure).** Suppose an attacker may submit chosen ciphertexts to a decryption service and see a root. Then it recovers $p$ and $q$ with two queries on average, and from then on it decrypts every ciphertext, including the challenge it was given.

*Proof.* The service is a root machine for the ciphertexts the attacker builds: the attacker picks $x$ itself, so it can satisfy any padding rule the service checks, and the answer it gets is a root of $x^2 \bmod N$. Apply Theorem 13 and Corollary 15, then decrypt with Part 1. The attacker never has to send the challenge ciphertext. $\blacksquare$

The test file does exactly this: it encrypts a secret message, never shows that ciphertext to the oracle, factors the modulus from unrelated queries, rebuilds the key and reads the secret. See [chosen ciphertext attack](/chosen-ciphertext-attack/) and [IND-CCA security](/ind-cca-security/) for the definitions this violates.

**Corollary 18 (not IND-CPA secure either).** Encryption is a deterministic function of the message, so an attacker given a challenge ciphertext for one of two messages of its own choice encrypts both and compares. The advantage is 1.

*Proof.* Immediate; the general statement is that no deterministic public-key encryption scheme is [IND-CPA](/ind-cpa-security/) secure, because the encryption key is public. $\square$

**Remark 19 (a padding does not save the bare scheme).** Making the service check the redundancy of Part 2 before answering raises the cost of a query but not the asymptotics: the attacker chooses $x$ to be an encoded message of its own, which passes the check, and the answer is still a root. The repair has to change the *map*, by adding randomness and a check the attacker cannot satisfy for arbitrary roots, as in [Blum-Goldwasser](/blum-goldwasser-cryptosystem/), an [OAEP](/rsa-oaep/) style transform, or the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/).

## Part 5. Williams' variant removes the ambiguity

Williams (1980) chooses $p \equiv 3 \pmod 8$ and $q \equiv 7 \pmod 8$. Then the [Jacobi symbol](/jacobi-symbol/) $\left(\frac{2}{N}\right) = -1$, and for any $x \in \mathbb{Z}_N^*$ exactly one element of $\{x, N-x\}$ has Jacobi symbol $+1$, while multiplication by 2 or by $-1$ moves between the two pairs of roots in a way the sender can record in two bits. The result is a map that the receiver inverts uniquely, with no redundancy in the message, and whose security is still equivalent to factoring by Theorem 16.

Two points carry over without change. The four roots and the CRT recombination of Part 1 are the same, and the reduction of Part 3 still applies, so the Williams variant is also insecure as a bare encryption scheme against chosen ciphertext attacks. What the variant buys is a clean bijection, which is why it is the form used for [Rabin signatures](/rabin-signature/), where the ambiguity would otherwise force the signer to send extra bits.

The implementation of this page uses the redundancy tag, not Williams' Jacobi symbol rule, so it is the Rabin 1979 scheme with a modern encoding and not the Rabin-Williams variant.
