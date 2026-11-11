---
tag: C3GSSY
kind: definition
slug: indifferentiability-framework
name: Indifferentiability framework
aliases:
- indifferentiability
- Maurer-Renner-Holenstein framework
area: cryptography/hash-functions
level: research
summary: "When a hash built from an ideal primitive can replace a random oracle: a simulator must fake the primitive so well that no distinguisher with access to both sees a difference."
prereqs: [random-oracle-model, merkle-damgard-construction]
see_also: [sponge-construction, length-extension-attack, nmac, hmac, ideal-cipher-model, compression-function, sha-2, sha-3]
sources:
  - paper: "Ueli Maurer, Renato Renner and Clemens Holenstein, Indifferentiability, impossibility results on reductions, and applications to the random oracle methodology, Theory of Cryptography Conference, TCC 2004, LNCS 2951, Springer, 2004"
    locator: the definition of indifferentiability for systems with a public and a private interface, and the composition theorem
  - paper: "Jean-Sébastien Coron, Yevgeniy Dodis, Cécile Malinaud and Prashant Puniya, Merkle-Damgard revisited, how to construct a hash function, Advances in Cryptology, CRYPTO 2005, LNCS 3621, Springer, 2005"
    locator: full version of September 4, 2007, Definition 1, Definition 2, Theorem 2.1, Section 3.2 (plain MD), Theorems 3.1, 3.3, 3.4 and 3.5, and Theorem 4.1
  - paper: "Guido Bertoni, Joan Daemen, Michaël Peeters and Gilles Van Assche, On the indifferentiability of the sponge construction, Advances in Cryptology, EUROCRYPT 2008, LNCS 4965, Springer, 2008"
    locator: Section 3.5 (the cost N), Lemmas 4 and 5, Theorem 1 with equation (4), and Theorem 2 with equation (6)
  - paper: "Thomas Ristenpart, Hovav Shacham and Thomas Shrimpton, Careful with composition, limitations of the indifferentiability framework, Advances in Cryptology, EUROCRYPT 2011, LNCS 6632, Springer, 2011"
    locator: single-stage and multi-stage games, the hash-based storage auditing counterexample, and reset indifferentiability
  - paper: "Ran Canetti, Oded Goldreich and Shai Halevi, The random oracle methodology, revisited, 30th ACM Symposium on Theory of Computing, STOC 1998"
    locator: schemes secure in the random oracle model that are insecure with any real hash function
---

Indifferentiability is the condition under which a hash function built from an ideal primitive can be used in place of a [random oracle](/random-oracle-model/), in any protocol, without losing the protocol's proof. It was defined by Maurer, Renner and Holenstein (2004) for general systems and applied to hash functions by Coron, Dodis, Malinaud and Puniya (2005). The difference from plain indistinguishability is that the attacker may also query the primitive inside the hash, such as the compression function or the permutation, because that primitive is public. The plain [Merkle-Damgard construction](/merkle-damgard-construction/) fails the test because of [length extension](/length-extension-attack/). Chop-MD, prefix-free MD, NMAC and HMAC pass it, and the [sponge construction](/sponge-construction/) passes it with an advantage of about $N^2/2^{c+1}$ (Bertoni, Daemen, Peeters and Van Assche 2008).

**Notation.** $G$ is the ideal primitive of the construction: a random function $f : \{0,1\}^{n+\kappa} \to \{0,1\}^n$, an ideal cipher $E$, or a random permutation $F$ on $\{0,1\}^{r+c}$. $C^G$ is the construction, for example $\mathrm{MD}^f$. $\mathcal{F}$ is the ideal object it should behave like, here a random oracle $\mathcal{RO} : \{0,1\}^* \to \{0,1\}^n$. $S$ is a simulator with oracle access to $\mathcal{F}$, and $D$ a distinguisher. $q$ is the number of queries of $D$, $\ell$ the maximum message length in blocks, and $t_D$ and $t_S$ the running times. For the sponge, $r$ is the rate, $c$ the capacity and $N$ the cost (defined below). The toy numbers come from the code of this page, which is for study only, uses Python's non-cryptographic `random` module, and is not constant time.

## Definition

### The two worlds

The distinguisher $D$ has two oracles, a left one for the hash and a right one for the primitive.

- In the **real world**, the left oracle is $C^G$ and the right oracle is $G$ itself.
- In the **ideal world**, the left oracle is $\mathcal{F}$ and the right oracle is a simulator $S^{\mathcal{F}}$. The simulator may query $\mathcal{F}$, but it does not see the queries that $D$ sends to $\mathcal{F}$.

$D$ outputs a bit. The construction is good if the two worlds look the same to every $D$: the simulator can invent a primitive whose answers are consistent with the random oracle.

### Indifferentiability

**Definition (CDMP 2005, Definition 1, after MRH 2004).** $C^G$ is $(t_D, t_S, q, \varepsilon)$-indifferentiable from $\mathcal{F}$ if there is a simulator $S$ that runs in time at most $t_S$ such that, for every distinguisher $D$ that runs in time at most $t_D$ and makes at most $q$ queries,

$$\bigl|\Pr[D^{C^G,\, G} = 1] - \Pr[D^{\mathcal{F},\, S^{\mathcal{F}}} = 1]\bigr| < \varepsilon.$$

$C^G$ is (computationally) indifferentiable from $\mathcal{F}$ if $\varepsilon$ is negligible in the security parameter for polynomial $t_D$ and $t_S$.

The order of the quantifiers matters: one simulator must work for all distinguishers. Indistinguishability is the special case where $D$ has no right oracle, and that is far too weak for a public hash: a hash $C$ can be indistinguishable from a random oracle when $G$ is secret, and still be useless when anyone can compute $G$.

### The composition theorem

A cryptosystem $P$ uses its ideal primitive through a private interface; the attacker $A$ gets the public interface. In the $G$ model, $P$ calls $C^G$ and $A$ calls $G$. In the $\mathcal{F}$ model, both call $\mathcal{F}$. An environment $\mathcal{E}$ runs $P$ and $A$ and outputs a bit.

**Theorem (MRH 2004; CDMP Theorem 2.1).** If $C^G$ is indifferentiable from $\mathcal{F}$, then every cryptosystem $P$ is at least as secure in the $G$ model with $C$ as in the $\mathcal{F}$ model: for every environment $\mathcal{E}$ and attacker $A$ in the $G$ model there is an attacker $A'$ in the $\mathcal{F}$ model with $|\Pr[\mathcal{E}(P^{C}, A^{G}) = 1] - \Pr[\mathcal{E}(P^{\mathcal{F}}, A'^{\mathcal{F}}) = 1]|$ negligible.

*Proof.* Let $A' = A^{S}$: run $A$, and answer its queries to $G$ with the simulator $S^{\mathcal{F}}$. Treat $\mathcal{E}$, $P$ and $A$ together as one distinguisher $D$: its left oracle serves $P$ and its right oracle serves $A$. In the real world $D$ sees $(C^G, G)$, which is the run $\mathcal{E}(P^{C}, A^{G})$. In the ideal world $D$ sees $(\mathcal{F}, S^{\mathcal{F}})$, which is the run $\mathcal{E}(P^{\mathcal{F}}, A'^{\mathcal{F}})$. The two runs differ by at most $\varepsilon$ by the definition, and $A'$ runs in the time of $A$ plus the simulator's time for each of its queries. $\square$

So a proof in the random oracle model carries over to a hash that is indifferentiable from a random oracle when its primitive is ideal. The loss is $\varepsilon$ in advantage and $t_S$ in the attacker's running time, so an efficient simulator matters.

### Limits

- **Single-stage games only.** Ristenpart, Shacham and Shrimpton (2011) showed that the proof above silently uses one attacker with one state. In a multi-stage game, the attacker is split into stages that may not share state, and the merged attacker $A^S$ would need one simulator state shared across the stages. Their example is hash-based storage auditing: a server proves that it still stores a file $M$ by returning $H(M \| C)$ for a fresh challenge $C$. With a random oracle the server must keep $M$. With any iterated hash, chop-MD and the sponge included, the server can keep only the internal state after $M$, a few hundred bits, and still answer every challenge. They defined reset indifferentiability, which does compose for multi-stage games, and showed that the usual iterated constructions do not meet it.
- **Ideal primitives only.** The theorem is about a random $f$, an ideal cipher or a random permutation. A real compression function or permutation is a fixed algorithm, and the random oracle model itself has known counterexamples: Canetti, Goldreich and Halevi (1998) built schemes that are secure with a random oracle and insecure with any concrete hash.
- **Not a property of the primitive.** Indifferentiability says nothing about the real SHA-256 compression function or Keccak-f. It says that the mode of operation adds no structural weakness, so that any attack must use the primitive's internals.

## Examples and non-examples

### Plain Merkle-Damgard is not indifferentiable

The code of this page hashes lists of 32-bit blocks with a random function $f$ as compression function and appends one block holding the number of message blocks. So $H(m_1) = f(f(IV, m_1), 1)$, and the three-block message $(m_1, 1, s)$ is padded to $(m_1, 1, s, 3)$. The distinguisher of CDMP Section 3.2, adapted to this padding, is:

```pseudo id=main
LENGTH-EXTENSION-DISTINGUISHER(L, R)       ▷ L: H or RO; R: f or S
L1  m_1 ← a random block
L2  s ← a random block
L3  y ← L(m_1)                             ▷ the hash of one block
L4  z ← R(R(y, s), 3)                      ▷ extend y by s and the new length block
L5  return 1 if L(m_1, 1, s) = z, else 0
```

**Real world.** $L(m_1, 1, s) = f(f(f(f(IV, m_1), 1), s), 3) = f(f(y, s), 3) = z$, so $D$ outputs 1 every time. With $f$ from seed 42 and the random blocks $m_1 = \texttt{52e6b438}$ and $s = \texttt{f2a74de4}$, $y = \texttt{1c80317f}$ and $z = \texttt{bdd640fb}$, and the hash of $(m_1, 1, s)$ is $\texttt{bdd640fb}$.

**Ideal world.** The simulator gets the queries $(y, s)$ and then $(z', 3)$, and must answer with $\mathcal{RO}(m_1, 1, s)$. It does not know $m_1$; it sees only $y = \mathcal{RO}(m_1)$. It can find $m_1$ only by trying candidates on $\mathcal{RO}$, about $q_S/2^{\kappa}$ for $q_S$ queries over $\kappa$-bit blocks, or guess the output, with probability $2^{-n}$. So every simulator has $\Pr[D = 1]$ near 0, and the advantage is near 1. In the code, the real world gives $\Pr[D = 1] = 1.0$ and the ideal world with a simulator that answers at random gives $0.0$, over 300 trials. The test checks both numbers.

MD strengthening does not help: the attack above uses it. Plain MD is still collision resistant by the [Merkle-Damgard theorem](/merkle-damgard-theorem/). Indifferentiability is a much stronger goal.

### The fixes for Merkle-Damgard

All four bounds below are from CDMP, with $t_S = \ell \cdot O(q^2)$; each works with a random compression function (Section 3) and with Davies-Meyer over an ideal cipher (Theorem 4.1).

| Construction | Definition | $\varepsilon$ |
|---|---|---|
| Prefix-free MD | $\mathrm{MD}^f(g(M))$ for a prefix-free encoding $g$ | $2^{-n} \ell^2 O(q^2)$ (Theorem 3.1) |
| Chop-MD | the first $n - s$ bits of $\mathrm{MD}^f(M)$ | $2^{-s} \ell^2 O(q^2)$ (Theorem 3.3) |
| NMAC | $g(\mathrm{MD}^f(M))$ for an independent $g : \{0,1\}^n \to \{0,1\}^{n'}$ | $2^{-\min(n, n')} \ell^2 O(q^2)$ (Theorem 3.4) |
| HMAC (CDMP form) | $\mathrm{MD}^f(y')$ with $y$ from $\mathrm{MD}^f(0^\kappa, M)$ | $2^{-\min(n, \kappa)} \ell^2 O(q^2)$ (Theorem 3.5) |

- **Prefix-free MD.** No encoded message is a prefix of another, so the extension in line L4 never lands on a valid hash query. CDMP give two encodings: put the bit length in the first block, or spend one bit per block to mark the last block.
- **Chop-MD.** $D$ sees only $n - s$ bits of the chaining value and must guess the other $s$ to extend. SHA-384 and SHA-512/256 are chop-MD over SHA-512 with $s = 128$ and $s = 256$. SHA-224 has $s = 32$, which gives a weak bound. In the code, the same attack on chop-MD with $s = 16$ wins 0 times in 300 trials; with $s = 4$ it wins 16 times, close to the expected $300/16$.
- **NMAC.** The outer function hides the chaining value. In the code, the distinguisher wins 0 times in 300 trials. See [NMAC](/nmac/).
- **HMAC.** CDMP's keyless HMAC prepends a zero block and then hashes the result again with the same $f$ and $IV$, which gives NMAC from one compression function. This is the shape of [HMAC](/hmac/) with fixed keys, not a statement about HMAC as a MAC.

### The sponge

The sponge with a random permutation or random transformation $F$ on $b = r + c$ bits is indifferentiable from a random oracle. BDPV measure the attacker by its cost $N$: the total number of calls to $F$ or $F^{-1}$ that its queries would cause in the real world. A query to the hash with an $\ell$-bit input and $n$-bit output costs $\lfloor \ell / r \rfloor + \lceil n / r \rceil$ (BDPV Section 3.5).

**Theorem (BDPV 2008, Theorems 1 and 2).** The padded sponge calling a random transformation is $(t_D, t_S, N, \varepsilon)$-indifferentiable from a random oracle for any $t_D$, $t_S = O(N^2)$, $N < 2^c$ and any $\varepsilon > f_T(N)$, where

$$f_T(N) = 1 - \prod_{i=1}^{N} \Bigl(1 - \frac{i}{2^c}\Bigr) \approx 1 - e^{-N(N+1)/2^{c+1}} < \frac{N(N+1)}{2^{c+1}}.$$

With a random permutation, the same holds with $\varepsilon > f_P(N)$, where

$$f_P(N) = 1 - \prod_{i=0}^{N-1} \frac{1 - (i+1) 2^{-c}}{1 - i\, 2^{-(r+c)}} \approx 1 - e^{-\frac{(1 - 2^{-r}) N^2 + (1 + 2^{-r}) N}{2^{c+1}}} < \frac{(1 - 2^{-r}) N^2 + (1 + 2^{-r}) N}{2^{c+1}}.$$

The approximations hold for $N$ much smaller than $2^c$. For $c = 16$ and $r = 8$: at $N = 10$, $f_T = 0.000839$ and $f_P = 0.000836$; at $N = 300$, $f_T = 0.4984$, $f_P = 0.4971$, while the linear bound $N(N+1)/2^{17} = 0.6889$ is no longer close. For SHA3-256 ($c = 512$) and $N = 2^{128}$, the bound is about $2^{-257}$; for SHAKE128 ($c = 256$) and $N = 2^{64}$, about $2^{-129}$. This is the flat sponge claim: generic attacks cost about $2^{c/2}$.

### Other non-examples

- **$f(h(x))$** for a random oracle $f$ and a fixed collision-resistant $h$ (CDMP Section 3.1). $D$ computes $u = h(m)$, asks the right oracle for $f(u)$ and compares it with the hash of $m$. The simulator sees only $u$ and cannot recover $m$.
- **Davies-Meyer as a fixed-input function.** $f(h, m) = E_m(h) \oplus h$ is not indifferentiable from a random function: $D$ asks $E_m^{-1}(0)$ and gets a fixed point, which a random function would not reveal. This does not stop the iterated constructions above from being indifferentiable in the ideal cipher model (CDMP Theorem 4.1).

## Related definitions

- **[Random oracle model](/random-oracle-model/).** The ideal world $\mathcal{F}$ of the definition.
- **[Ideal cipher model](/ideal-cipher-model/).** A common choice for $G$ when the compression function is built from a block cipher.
- **Indistinguishability, as for a [pseudorandom function](/pseudorandom-function/).** The case with no right oracle and a secret primitive. It suffices for keyed uses such as a MAC, not for a public hash.
- **[Collision resistance](/collision-resistance/).** Implied by indifferentiability for an ideal primitive, up to $\varepsilon$, but much weaker: plain MD has it and fails indifferentiability.
- **Reset indifferentiability** (RSS 2011). A stronger notion in which the distinguisher may reset the simulator; it composes for multi-stage games.
- **[Sponge construction](/sponge-construction/).** The mode with the cleanest indifferentiability bound, used by SHA-3.

## References
