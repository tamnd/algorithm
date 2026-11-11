---
title: Correctness of EKE2 with the page's encoding
proves: [correctness]
status: full
---

We prove that the page's encoding is a permutation of the group $G$ for each password, that two honest parties with the same password compute the same session key, and that line L7 never aborts in an honest run. Notation is that of the page: $p = 2q + 1$ a safe prime with $q$ an odd prime, $G$ the quadratic residues modulo $p$, of order $q$, and $g$ a generator of $G$.

**Lemma 1 (folding).** The map $\phi(y) = \min(y, p - y)$ is a bijection from $G$ onto $[1, q]$, and its inverse sends $z \in [1, q]$ to whichever of $z$ and $p - z$ lies in $G$.

*Proof.* Since $q$ is odd, $p = 2q + 1 \equiv 3 \pmod 4$, so $-1$ is not a quadratic residue modulo $p$. Hence for each $z \in [1, p - 1]$ exactly one of $z$ and $-z = p - z$ is a residue. The pairs $\{z, p - z\}$ with $z \in [1, q]$ partition $[1, p - 1]$, and $\phi$ maps both members of a pair to $z$. So $\phi$ restricted to $G$ takes each value $z \in [1, q]$ exactly once, at the member of the pair that lies in $G$. As $|G| = q$, $\phi$ is a bijection onto $[1, q]$, with the stated inverse. $\square$

**Lemma 2 (Feistel permutation).** For a fixed key, $F(L, R) = (R, L \oplus f(R))$ on pairs of $h$-binary-digit numbers is a permutation, and so is the composition of 8 such rounds on $[0, 2^k)$ with $k = 2h$.

*Proof.* The map $(L', R') \mapsto (R' \oplus f(L'), L')$ inverts $F$: it sends $(R, L \oplus f(R))$ to $(L \oplus f(R) \oplus f(R), R) = (L, R)$. A composition of permutations is a permutation. The decryption loop of the code applies these inverses in reverse order. $\square$

**Lemma 3 (cycle walking).** Let $\pi$ be a permutation of a finite set $S$ and $T \subseteq S$. For $t \in T$ let $\rho(t)$ be the first element of the sequence $\pi(t), \pi^2(t), \ldots$ that lies in $T$. Then $\rho$ is a well defined permutation of $T$, and its inverse is obtained in the same way from $\pi^{-1}$.

*Proof.* The orbit of $t$ under $\pi$ is a finite cycle that contains $t \in T$, so the sequence reaches $T$ after at most $|S|$ steps, and $\rho$ is well defined. Inside one cycle, the elements of $T$ appear in cyclic order $t_1, t_2, \ldots, t_r$, and $\rho$ sends $t_i$ to $t_{i+1}$ (indices modulo $r$). This is a cyclic shift of the elements of $T$ on that cycle, hence a bijection on them; the cycles partition $S$, so $\rho$ is a permutation of $T$. Walking backward with $\pi^{-1}$ sends $t_{i+1}$ to $t_i$, which is $\rho^{-1}$. $\square$

**Lemma 4 (the encoding is a permutation of G).** For each password, $E_{pw}(y) = \rho(\phi(y) - 1)$, with $\rho$ built from the Feistel network on $[0, 2^k)$ and $T = [0, q)$, is a bijection from $G$ onto $[0, q)$, and $D_{pw}$ of the code inverts it. Every $c \in [0, q)$ decrypts under every password to an element of $G$.

*Proof.* The code chooses $k$ with $2^k > q$, so $[0, q) \subseteq [0, 2^k)$. By Lemma 1, $y \mapsto \phi(y) - 1$ is a bijection from $G$ onto $[0, q)$. By Lemmas 2 and 3, $\rho$ is a permutation of $[0, q)$ for each key. The composition is a bijection from $G$ onto $[0, q)$. $D_{pw}$ applies $\rho^{-1}$, adds 1 and applies the inverse of Lemma 1, so it inverts $E_{pw}$ and maps every $c \in [0, q)$ into $G$, whatever the password. $\square$

**Lemma 5 (agreement).** If both parties use the same password, both compute $K = g^{xy} \ne 1$ and the same session key.

*Proof.* By Lemma 4, $A$ decrypts $Y_c = E_{pw}(Y)$ to $Y = g^y$ and $B$ decrypts $X_c$ to $X = g^x$. Then $A$ computes $Y^x = g^{yx}$ and $B$ computes $X^y = g^{xy}$, which are equal. The order of $g$ is the prime $q$, and $x, y \in [1, q)$, so $q \nmid xy$ and $g^{xy} \ne 1$; line L7 does not abort. Both parties hash the same tuple $(\texttt{"A"}, \texttt{"B"}, X, Y, K)$ in line L8: the code puts the initiator's name and share first on both sides. $\square$

**Theorem.** In an honest run with the same password, EKE2 with the page's encoding terminates with both parties holding the same session key, and every ciphertext an eavesdropper sees decrypts to a valid share under every password.

*Proof.* Lemma 5 gives the first claim and Lemma 4 the second. $\blacksquare$

The second claim is what defeats the partition attack: no password can be ruled out because a decryption is invalid. It does not by itself prove security; that needs the ideal cipher argument of Bellare, Pointcheval and Rogaway.
