---
tag: M3FGR1
kind: theorem
slug: luby-rackoff-theorem
name: Luby-Rackoff theorem
aliases:
- Luby-Rackoff construction
area: cryptography/symmetric-ciphers
level: research
summary: A Feistel network with independent pseudorandom round functions is a pseudorandom permutation after 3 rounds and a strong one after 4, with advantage about q^2/2^h on halves of h bits.
prereqs: [feistel-network, prp-prf-switching-lemma, pseudorandom-function]
see_also: [pseudorandom-permutation, data-encryption-standard, block-cipher, birthday-paradox, ideal-cipher-model, hybrid-argument, union-bound, random-permutation]
sources:
  - paper: doi:10.1137/0217022
    title: Michael Luby and Charles Rackoff, How to construct pseudorandom permutations from pseudorandom functions, SIAM Journal on Computing 17(2), 1988
    locator: the main theorem (three rounds give a pseudorandom permutation generator) and the theorem on four rounds and super-pseudorandom permutations
  - paper: "Jacques Patarin, Luby-Rackoff: 7 rounds are enough for 2^(n(1-epsilon)) security, Advances in Cryptology, CRYPTO 2003, LNCS 2729, Springer, 2003"
    locator: security of Feistel networks with random round functions beyond the birthday bound
  - paper: "Jacques Patarin, Security of random Feistel schemes with 5 or more rounds, Advances in Cryptology, CRYPTO 2004, LNCS 3152, Springer, 2004"
    locator: the bounds for 5 or more rounds, close to 2^h queries
---

The Luby-Rackoff theorem says that a [Feistel network](/feistel-network/) on blocks of $2h$ bits whose round functions are independent [pseudorandom functions](/pseudorandom-function/) on $h$ bits is a [pseudorandom permutation](/pseudorandom-permutation/) after 3 rounds and a strong pseudorandom permutation, secure also against inverse queries, after 4 rounds. The loss in advantage is of order $q^2/2^h$ for $q$ queries, a birthday bound in the half-block length. Michael Luby and Charles Rackoff proved it in 1988, and it was the first proof that the structure of DES can give a secure block cipher from a secure keyed function. The round counts are the least possible: 2 rounds are not a PRP, and 3 rounds are not a strong PRP.

## Statement

Let $h \ge 1$ and let blocks be pairs $(L, R)$ of $h$-bit strings. For $f : \{0,1\}^h \to \{0,1\}^h$, the Feistel round is $\Phi_f(L, R) = (R, L \oplus f(R))$, and for functions $f_1, \ldots, f_r$ the $r$-round network is

$$\Psi(f_1, \ldots, f_r) = \Phi_{f_r} \circ \cdots \circ \Phi_{f_1},$$

a permutation of $\{0,1\}^{2h}$ for any $f_i$, with no final swap. Let $F : \{0,1\}^k \times \{0,1\}^h \to \{0,1\}^h$ be a function family, and let $\Psi^r_F$ be the family with key $(K_1, \ldots, K_r)$ and permutation $\Psi(F_{K_1}, \ldots, F_{K_r})$. For time $t$ and $q$ queries, let $\varepsilon_F(t, q)$ be the largest PRF advantage against $F$ of an adversary with time $t$ and $q$ queries, and let $T_F$ be the time to evaluate $F$.

**Theorem 1 (three rounds).** For every adversary $A$ that runs in time $t$ and makes $q$ forward queries,

$$\mathrm{Adv}^{\mathrm{prp}}_{\Psi^3_F}(A) \le 3\,\varepsilon_F\bigl(t + O(q\,T_F), q\bigr) + \frac{q(q-1)}{2^h} + \frac{q(q-1)}{2^{2h+1}}.$$

With truly random round functions, $\varepsilon_F = 0$ and the bound is $q(q-1)/2^h + q(q-1)/2^{2h+1}$.

**Theorem 2 (four rounds).** For every adversary $A$ that makes $q$ queries in total to the permutation and its inverse, $\mathrm{Adv}^{\mathrm{sprp}}_{\Psi^4_F}(A) \le 4\,\varepsilon_F + O(q^2/2^h)$. Luby and Rackoff proved this order of bound; Patarin gave sharper constants and showed that more rounds give security for $q$ close to $2^h$.

**Theorem 3 (the round counts are least).** $\Psi^2$ is not a PRP, and $\Psi^3$ is not a strong PRP, for any round functions and $h \ge 2$: in each case an adversary with at most 3 queries has advantage at least $1 - 2^{1-h}$.

## In plain words

A Feistel round can turn any function into a permutation, even a function that is not one-to-one. The theorem says that if the functions inside look random, three rounds already make the whole thing look like a random shuffle of all blocks, as long as the attacker only encrypts. If the attacker can also decrypt, four rounds are needed.

The only way for an attacker to see through three rounds is to wait for an accidental repeat inside the network, like two people in a room sharing a birthday. With halves of $h$ bits, that takes about $2^{h/2}$ queries. Fewer rounds fail at once: with two rounds, changing the left half of the input changes the left half of the output in the same way.

## Proof

We prove Theorem 1 in three steps, and Theorem 3 after it.

*Step 1: from PRFs to random functions.* For $j = 0, 1, 2, 3$, let $H_j$ be the network whose first $j$ round functions are independent uniformly random functions and whose other rounds use $F$ with independent uniform keys. $H_0$ is $\Psi^3_F$, and $H_3$ uses only random functions. Given $A$, build a PRF adversary $B_j$ with an oracle $O$: it samples random functions for rounds $1, \ldots, j-1$ lazily, uses $O$ for round $j$, picks keys for rounds $j+1, \ldots, 3$, and runs $A$ on the network so formed. If $O = F_K$, $A$ sees $H_{j-1}$; if $O$ is random, $A$ sees $H_j$. $B_j$ asks $O$ at most once per query of $A$, so at most $q$ times, and runs in time $t + O(q\,T_F)$. By the triangle inequality, $|\Pr[A^{H_0} = 1] - \Pr[A^{H_3} = 1]| \le 3\,\varepsilon_F$.

*Step 2: three random rounds against a random function.* Let $f_1, f_2, f_3$ be independent random functions, sampled lazily, and $\rho$ a random function on $2h$ bits. We may assume that $A$ makes $q$ distinct queries $(L_i, R_i)$, as a repeated query can be answered from memory. For query $i$, the network computes

$$X_i = L_i \oplus f_1(R_i), \quad S_i = R_i \oplus f_2(X_i), \quad T_i = X_i \oplus f_3(S_i),$$

and returns $(S_i, T_i)$. Define a game G that answers query $i$ as follows.

1. Choose $S^*, T^*$ uniformly in $\{0,1\}^h$. Compute $X_i = L_i \oplus f_1(R_i)$.
2. If $X_i = X_j$ for some $j < i$: set bad, and compute $(S_i, T_i)$ by the formulas above.
3. Else, if $S^* = S_j$ for some $j < i$: set bad, let $S_i = S^*$ and $f_2(X_i) = S^* \oplus R_i$, and let $T_i = X_i \oplus f_3(S_i)$, with the value $f_3(S_i)$ already stored.
4. Else: let $S_i = S^*$, $T_i = T^*$, and store $f_2(X_i) = S^* \oplus R_i$ and $f_3(S^*) = T^* \oplus X_i$.

In cases 3 and 4, $X_i$ is a new point of $f_2$, so storing $f_2(X_i) = S^* \oplus R_i$ with $S^*$ uniform gives it the uniform value of a lazily sampled $f_2$. In case 4, $S^*$ is a new point of $f_3$, and the same holds for $f_3(S^*) = T^* \oplus X_i$. In case 2, G uses the formulas directly. So G answers exactly as the network with random $f_1, f_2, f_3$. Let G' be G except that it always returns $(S^*, T^*)$. Then G' answers with independent uniform strings, exactly as $\rho$ on distinct queries. G and G' are identical until bad, so by the fundamental lemma of game playing (see the [switching lemma](/prp-prf-switching-lemma/)),

$$\bigl| \Pr[A^{H_3} = 1] - \Pr[A^{\rho} = 1] \bigr| \le \Pr[\text{G' sets bad}].$$

In G', the answers do not depend on $f_1$, so the queries of $A$ are independent of $f_1$. For $j < i$, the event $X_i = X_j$ is $f_1(R_i) \oplus f_1(R_j) = L_i \oplus L_j$. If $R_i = R_j$, then $L_i \ne L_j$ since the queries differ, and the event is impossible. If $R_i \ne R_j$, the two values of $f_1$ are independent and uniform, and the event has probability $2^{-h}$. The event $S^*_i = S^*_j$ has probability $2^{-h}$, as $S^*_i$ is uniform and independent of $S^*_j$. By the [union bound](/union-bound/) over the $\binom{q}{2}$ pairs and the two events,

$$\Pr[\text{G' sets bad}] \le 2 \binom{q}{2} 2^{-h} = \frac{q(q-1)}{2^h}.$$

*Step 3: random function against random permutation.* By the switching lemma on $2h$-bit blocks, $|\Pr[A^{\rho} = 1] - \Pr[A^{\pi} = 1]| \le q(q-1)/2^{2h+1}$ for a random permutation $\pi$.

Adding the three steps with the triangle inequality proves Theorem 1. $\square$

*Theorem 3, two rounds.* Round 1 maps $(L, R)$ to $(R, X)$ with $X = L \oplus f_1(R)$, and round 2 maps this to $(X, R \oplus f_2(X))$. So the left half of the output is $X$. Two queries $(L, R)$ and $(L', R)$ with $L \ne L'$ give left halves $X$ and $X'$ with $X \oplus X' = L \oplus L'$, always. For a random permutation, the second output is uniform over the $2^{2h} - 1$ blocks other than the first output, and exactly $2^h$ of them have the required left half, which differs from the first left half. So the relation holds with probability $2^h/(2^{2h} - 1) \le 2^{1-h}$. The adversary that outputs 1 when the relation holds has advantage at least $1 - 2^{1-h}$.

*Theorem 3, three rounds with an inverse query.* Ask $(L_1, R)$ and $(L_2, R)$ with $L_1 \ne L_2$, getting $(S_1, T_1)$ and $(S_2, T_2)$, then ask the inverse at $(S_2, T_2 \oplus L_1 \oplus L_2)$, getting $(L_3, R_3)$. With $X_j = L_j \oplus f_1(R)$, we have $T_2 = X_2 \oplus f_3(S_2)$, so undoing round 3 gives the state $(X_2 \oplus L_1 \oplus L_2, S_2) = (X_1, S_2)$. Undoing round 2 gives $(S_2 \oplus f_2(X_1), X_1) = (S_2 \oplus S_1 \oplus R, X_1)$, since $S_1 = R \oplus f_2(X_1)$. Undoing round 1 gives right half $S_1 \oplus S_2 \oplus R$. So $R_3 = S_1 \oplus S_2 \oplus R$ always. For a random permutation, the inverse query point differs from $(S_2, T_2)$. It equals $(S_1, T_1)$ with probability at most $1/(2^{2h} - 1)$. Otherwise its answer is uniform over the $2^{2h} - 2$ inputs not yet used, of which at most $2^h$ have the required right half. So the relation holds with probability at most $1/(2^{2h} - 1) + 2^h/(2^{2h} - 2) \le 2^{1-h}$ for $h \ge 2$, and the advantage is at least $1 - 2^{1-h}$. $\blacksquare$

## Consequences

- **A PRP from a one-way function.** One-way functions give PRGs, PRGs give PRFs by the GGM construction, and PRFs give PRPs and strong PRPs by this theorem. So block ciphers exist in theory if one-way functions do.
- **A design argument for Feistel ciphers.** The theorem explains why the Feistel structure of DES is sound in principle: the weakness of a Feistel cipher must lie in its round functions or its few rounds, not in the structure. Real ciphers use 16 or more rounds with weak round functions, outside the theorem.
- **Format-preserving encryption.** Small-domain ciphers such as FF1 of NIST SP 800-38G are Feistel networks with an AES-based round function. Their security arguments start from Luby-Rackoff style bounds, and on small domains the term $q^2/2^h$ forces many rounds.
- **The bound is in the half length.** The birthday term is $q^2/2^h$, not $q^2/2^{2h}$. A 3-round or 4-round Luby-Rackoff cipher on 64-bit blocks is safe only for $q$ well below $2^{16}$.

## Tightness

The term $q(q-1)/2^h$ is tight up to a factor of about 2 for 3 rounds. Fix $R$ and ask $(L_i, R)$ for $q$ distinct $L_i$. The values $X_i = L_i \oplus f_1(R)$ are distinct, and $S_i = R \oplus f_2(X_i)$. When $S_i = S_j$, which happens with probability $2^{-h}$ for each pair, $T_i \oplus T_j = X_i \oplus X_j = L_i \oplus L_j$. So the test "some pair has equal left halves of output and $T_i \oplus T_j = L_i \oplus L_j$" succeeds with probability about $1 - e^{-q(q-1)/2^{h+1}}$ on the network, and with probability about $q^2/2^{2h+1}$ on a random permutation.

The implementation with this page runs the three distinguishers with $h = 8$, against the Feistel network with lazily sampled random round functions and against a lazily sampled random permutation, in 2000 trials each. The code is for study only, uses Python's non-cryptographic generator and is not constant time.

| distinguisher | rounds | success on the network | success on a random permutation |
|---|---|---|---|
| two queries, same $R$ | 2 | 1.0 | 0.0065 |
| two queries, same $R$ | 3 | 0.0045 | 0.004 |
| two forward and one inverse query | 3 | 1.0 | 0.005 |
| two forward and one inverse query | 4 | 0.0035 | 0.0055 |
| birthday, $q = 8$ | 3 | 0.1035 | 0.0 |
| birthday, $q = 16$ | 3 | 0.3715 | 0.0025 |
| birthday, $q = 32$ | 3 | 0.86 | 0.007 |
| birthday, $q = 64$ | 3 | 1.0 | 0.0195 |

For $q = 8$ the predicted value is $1 - e^{-56/512} \approx 0.104$, and for $q = 16$ it is $1 - e^{-240/512} \approx 0.374$.

The two short distinguishers, as in the tests:

```python
H = 8
MASK = (1 << H) - 1

def split(x):
    return x >> H, x & MASK

def two_round_distinguisher(oracle):
    """For 2 rounds, the left output halves satisfy L2 XOR L2' = L XOR L'."""
    l1, l2, r = 0x00, 0x5A, 0x33
    a, _ = split(oracle.enc((l1 << H) | r))
    b, _ = split(oracle.enc((l2 << H) | r))
    return a ^ b == l1 ^ l2

def three_round_inverse_distinguisher(oracle):
    """For 3 rounds, decrypting (S2, T2 XOR L1 XOR L2) gives right half S1 XOR S2 XOR R."""
    l1, l2, r = 0x00, 0xC3, 0x77
    s1, _ = split(oracle.enc((l1 << H) | r))
    s2, t2 = split(oracle.enc((l2 << H) | r))
    _, r3 = split(oracle.dec((s2 << H) | (t2 ^ l1 ^ l2)))
    return r3 == s2 ^ s1 ^ r
```

## History

Feistel designed the network for IBM's Lucifer cipher in the early 1970s, and DES used it with 16 rounds. Luby and Rackoff asked in the 1980s whether the structure itself could be proved secure, and showed in their 1988 paper that 3 rounds with pseudorandom round functions give a pseudorandom permutation and 4 rounds give a super-pseudorandom one, now called a strong PRP. Patarin studied the exact bounds over many papers from 1990 on, and showed that with more rounds the security of random Feistel networks approaches $2^h$ queries: 7 rounds in 2003, and 5 or more rounds in 2004.

## References
