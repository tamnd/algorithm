---
title: PBKDF2 is well defined, has the prefix property, and in the random oracle model each block needs c sequential PRF calls
proves: [correctness]
status: full
---

We use the notation of the page. $\mathrm{PRF}(P, \cdot)$ maps byte strings to $hLen$-byte strings, $l = \lceil dkLen / hLen \rceil$, and
$$T_i = U_1^{(i)} \oplus \cdots \oplus U_c^{(i)}, \qquad U_1^{(i)} = \mathrm{PRF}(P, S \| \mathrm{INT}(i)), \qquad U_j^{(i)} = \mathrm{PRF}(P, U_{j-1}^{(i)}).$$

**Lemma 1 (the block inputs are distinct).** If line L1 does not stop, then the strings $S \| \mathrm{INT}(i)$ for $1 \le i \le l$ are pairwise distinct.

*Proof.* Line L1 ensures $dkLen \le (2^{32} - 1)\, hLen$, so $l \le 2^{32} - 1$, and every $i \le l$ has a 4-byte big-endian form $\mathrm{INT}(i)$. This map is injective on $1 \le i < 2^{32}$. The strings $S \| \mathrm{INT}(i)$ share the prefix $S$ and differ in the last four bytes. $\square$

**Lemma 2 (the prefix property).** For $k \le n$, the first $k$ bytes of $\mathrm{PBKDF2}(P, S, c, n)$ equal $\mathrm{PBKDF2}(P, S, c, k)$.

*Proof.* Block $T_i$ is a function of $(P, S, c, i)$ only; it does not depend on the requested length. Both outputs are prefixes of the same infinite sequence $T_1 \| T_2 \| \cdots$, cut at $n$ and at $k$ bytes. $\square$

**Lemma 3 (verification).** $\mathrm{VERIFY}(P, S, c, \mathrm{PBKDF2}(P, S, c, n))$ returns true.

*Proof.* PBKDF2 is deterministic, and VERIFY recomputes it with the same inputs and the length $n$ of the stored value. $\square$

**Theorem (sequential cost in the ROM).** Model $\mathrm{PRF}(P, \cdot)$ for the unknown password $P$ as a random function $R$ to which the adversary has oracle access, and fix $i$. Let $A$ be any algorithm that asks $R$ at most $c - 1$ queries along the chain, that is, it does not ask all of $x_1 = S \| \mathrm{INT}(i)$, $x_2 = U_1^{(i)}$, ..., $x_c = U_{c-1}^{(i)}$. Then $A$ outputs $T_i$ with probability at most $2^{-8 hLen} + q^2 2^{-8 hLen}$, where $q$ is the total number of queries of $A$.

*Proof.* We assume first that the chain has no repeats: the values $x_1, \ldots, x_c$ are pairwise distinct and no query of $A$ outside the chain hits a chain value by chance. Each of these events fails with probability at most $q^2 2^{-8 hLen}$ in total, by a union bound over pairs of values that are uniform and independent.

Under this assumption, the queries along the chain must come in order: $x_{j+1} = R(x_j)$ is uniform and unknown to $A$ until it asks $x_j$, so $A$ can ask $x_{j+1}$ only after it asks $x_j$, except by a chance hit that we excluded. So if $A$ does not ask all of $x_1, \ldots, x_c$, it does not ask $x_c$, and $U_c^{(i)} = R(x_c)$ is uniform and independent of everything $A$ has seen. Then $T_i = (U_1^{(i)} \oplus \cdots \oplus U_{c-1}^{(i)}) \oplus U_c^{(i)}$ is uniform from the view of $A$, and $A$ outputs it with probability $2^{-8 hLen}$. Adding the probability of the excluded events gives the bound. $\blacksquare$

**Consequence for guessing.** To test one password guess against a stored block $T_1$, an attacker who does not want to rely on luck must make the $c$ chain queries for that guess. With the salt in $x_1$, the chains of different users and different guesses start at different points, so they share no queries. So $q$ queries test at most about $q / c$ (user, guess) pairs. This is the informal content of the analysis of Bellare, Ristenpart and Tessaro (CRYPTO 2012), which also handles many users and the case where the PRF is HMAC built from a random compression function. The theorem says nothing about memory: the chain needs only the current $U_j$ and $T$, which is why PBKDF2 is not memory hard.
