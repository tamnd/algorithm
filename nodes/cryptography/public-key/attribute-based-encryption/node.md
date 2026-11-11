---
tag: Q5ZTFT
kind: definition
slug: attribute-based-encryption
name: Attribute-based encryption
aliases:
- ABE
area: cryptography/public-key
level: research
summary: "Public-key encryption in which keys and ciphertexts carry attributes and access policies, and a key decrypts only if its policy matches. Colluding users cannot pool keys. KP-ABE and CP-ABE."
prereqs: [identity-based-encryption, bilinear-diffie-hellman, shamir-secret-sharing]
see_also: [functional-encryption, boneh-franklin-ibe, broadcast-encryption, bilinear-pairing, secret-sharing, lagrange-interpolation, threshold-cryptography, learning-with-errors]
sources:
  - paper: "Amit Sahai and Brent Waters, Fuzzy identity-based encryption, Eurocrypt 2005, LNCS 3494, pages 457 to 473"
    locator: the scheme in which a key for a set of attributes decrypts a ciphertext for another set when at least d attributes are shared, the use of random polynomials per key against collusion, and the selective security under DBDH
  - paper: "Vipul Goyal, Omkant Pandey, Amit Sahai and Brent Waters, Attribute-based encryption for fine-grained access control of encrypted data, ACM CCS 2006, pages 89 to 98"
    locator: the names key-policy and ciphertext-policy ABE, the small-universe construction with access trees of threshold gates, the selective-set security game and proof under DBDH, the large-universe construction, and the extension to linear secret sharing schemes
  - paper: "John Bethencourt, Amit Sahai and Brent Waters, Ciphertext-policy attribute-based encryption, IEEE Symposium on Security and Privacy 2007, pages 321 to 334"
    locator: the first ciphertext-policy construction, its security argument in the generic group model, and the implementation
  - paper: "Brent Waters, Ciphertext-policy attribute-based encryption, an expressive, efficient, and provably secure realization, PKC 2011, LNCS 6571, pages 53 to 70"
    locator: CP-ABE for policies given as LSSS matrices, with selective security under a q-type parallel BDHE assumption
  - paper: "Allison Lewko, Tatsuaki Okamoto, Amit Sahai, Katsuyuki Takashima and Brent Waters, Fully secure functional encryption, attribute-based encryption and (hierarchical) inner product encryption, Eurocrypt 2010, LNCS 6110, pages 62 to 91"
    locator: adaptively secure KP-ABE and CP-ABE by dual system encryption
  - paper: "Sergey Gorbunov, Vinod Vaikuntanathan and Hoeteck Wee, Attribute-based encryption for circuits, STOC 2013, pages 545 to 554"
    locator: KP-ABE for all circuits of bounded depth under LWE
  - book: "Amos Beimel, Secure schemes for secret sharing and key distribution, PhD thesis, Technion, 1996"
    locator: linear secret sharing schemes and their equivalence with monotone span programs
---

Attribute-based encryption (ABE) is [public-key encryption](/public-key-encryption/) for access control. A ciphertext and a key each carry part of a rule: one side has a set of **attributes**, such as "doctor" and "cardiology", and the other has a **policy**, such as "doctor AND (cardiology OR emergency)". A key decrypts a ciphertext only when the attributes satisfy the policy. The essential security property is **collusion resistance**: users whose keys each fail cannot combine them to decrypt. Amit Sahai and Brent Waters introduced the idea in 2005 as fuzzy [identity-based encryption](/identity-based-encryption/). Goyal, Pandey, Sahai and Waters named key-policy ABE in 2006 and built it from [bilinear pairings](/bilinear-pairing/), and Bethencourt, Sahai and Waters built ciphertext-policy ABE in 2007.

**Notation.** $\kappa$ is the security parameter and $\mathcal{U}$ the attribute universe. A **policy** (access structure) $\mathbb{A}$ is a monotone set of subsets of $\mathcal{U}$, given as a formula of AND, OR and threshold gates, or as a linear secret sharing scheme; $\mathbb{A}(\gamma) = 1$ means that the attribute set $\gamma$ satisfies it. In the construction, $\mathbb{G}_1 = \langle P \rangle$ and $\mathbb{G}_T$ have prime order $r$, $e$ is a symmetric pairing, and $\Delta_{i,S}(x) = \prod_{j \in S, j \ne i} (x - j)/(i - j)$ is a Lagrange coefficient modulo $r$.

## Definition

A **key-policy ABE scheme** (KP-ABE) consists of four probabilistic polynomial time algorithms.

- $\mathsf{Setup}(1^\kappa, \mathcal{U}) \to (\mathsf{mpk}, \mathsf{msk})$.
- $\mathsf{KeyGen}(\mathsf{msk}, \mathbb{A}) \to \mathsf{sk}_{\mathbb{A}}$: a key for a policy.
- $\mathsf{Enc}(\mathsf{mpk}, \gamma, m) \to c$: a ciphertext labeled with an attribute set $\gamma \subseteq \mathcal{U}$.
- $\mathsf{Dec}(\mathsf{sk}_{\mathbb{A}}, c) \to m$ or $\bot$.

**Correctness.** If $\mathbb{A}(\gamma) = 1$, then $\mathsf{Dec}(\mathsf{sk}_{\mathbb{A}}, \mathsf{Enc}(\mathsf{mpk}, \gamma, m)) = m$.

A **ciphertext-policy ABE scheme** (CP-ABE) swaps the roles: $\mathsf{KeyGen}$ takes an attribute set $\gamma$, $\mathsf{Enc}$ takes a policy $\mathbb{A}$, and decryption works when $\mathbb{A}(\gamma) = 1$. KP-ABE suits data that is labeled when it is stored, such as audit logs, with keys that say what each analyst may read. CP-ABE suits a sender who decides who may read, like role-based access control.

**Security (KP-ABE).** In the IND-CPA game, the challenger gives $\mathsf{mpk}$ to the adversary. The adversary asks for keys for policies $\mathbb{A}_1, \mathbb{A}_2, \ldots$ of its choice, then names a target set $\gamma^*$ and two messages, and gets an encryption of one of them under $\gamma^*$. It may ask for more keys, and it wins if it guesses which message was encrypted. The one rule is that $\mathbb{A}_i(\gamma^*) = 0$ for **every** key it asked for. The scheme is secure if every efficient adversary has negligible advantage. Since the adversary holds many keys at once, this game already demands collusion resistance. In the **selective-set** game, the adversary must name $\gamma^*$ before it sees $\mathsf{mpk}$; GPSW prove security in this weaker game. Lewko, Okamoto, Sahai, Takashima and Waters (2010) reached full (adaptive) security with dual system encryption.

IBE is the special case of KP-ABE in which each key has the policy "the attribute is $\mathsf{ID}$" and each ciphertext has one attribute. Fuzzy IBE is the case of a single threshold gate: a key for the attribute set $\omega$ opens a ciphertext for $\omega'$ when $|\omega \cap \omega'| \ge d$, for example for biometric readings that differ a little.

### The GPSW construction

GPSW (2006) handle **access trees**: every inner node $x$ is a threshold gate "$k_x$ of $n_x$ children" (AND is $n_x$ of $n_x$, OR is 1 of $n_x$), every leaf is an attribute, and the children of a node have the indices $1, \ldots, n_x$. This is the small-universe construction, which the code implements.

```pseudo
SETUP(U)
1   for each attribute a ∈ U: t_a ← uniform in Z_r^*, T_a ← t_a·P
2   y ← uniform in Z_r^*, Y ← e(P, P)^y
3   return mpk = (P, {T_a}, Y), msk = ({t_a}, y)

KEYGEN(msk, tree)
4   for each node x, top down: pick a random polynomial q_x of degree k_x − 1 with
5       q_x(0) = y at the root and q_x(0) = q_parent(x)(index(x)) elsewhere
6   for each leaf x with attribute a: D_x ← (q_x(0) / t_a)·P
7   return the tree and all D_x

ENCRYPT(mpk, γ, M)                            ▷ M ∈ G_T
8   s ← uniform in Z_r^*
9   return (γ, E' = M·Y^s, {E_a = s·T_a : a ∈ γ})

DECRYPT-NODE(x)                               ▷ returns e(P, P)^(s·q_x(0)) or ⊥
10  if x is a leaf with attribute a: return e(D_x, E_a) if a ∈ γ, else ⊥
11  S ← the indices of k_x children z with DECRYPT-NODE(z) = F_z ≠ ⊥; if there are fewer, return ⊥
12  return ∏ over i ∈ S of F_i^(Δ_{i,S}(0))

DECRYPT(key, ciphertext)
13  return E' / DECRYPT-NODE(root)
```

At a leaf, $e(D_x, E_a) = e(\frac{q_x(0)}{t_a}P, s t_a P) = e(P, P)^{s q_x(0)}$. At an inner node with $k_x$ good children, Lagrange interpolation in the exponent gives $\sum_{i \in S} \Delta_{i,S}(0) \, s \, q_x(i) = s \, q_x(0)$, because $q_x$ has degree $k_x - 1$. By induction the root gives $e(P, P)^{sy} = Y^s$, and line 13 returns $M$. GPSW prove the scheme selective-set secure under [DBDH](/bilinear-diffie-hellman/). A ciphertext has $|\gamma| + 1$ group elements, a key has one per leaf, and decryption needs one pairing per leaf used.

**Why collusion fails.** Each key has its own random polynomials, all with the same constant term $y$. Shares from two keys are points on different polynomials, so interpolating them gives a random value, not $sy$. Each user can only use its shares together with its own other shares.

**Linear secret sharing.** Any monotone policy that has a linear secret sharing scheme (LSSS) can replace the tree: a matrix $M$ with rows labeled by attributes, and the shares $M v$ for a vector $v$ with first entry $y$. A set of rows that spans $(1, 0, \ldots, 0)$ recovers $y$ by a linear combination. Threshold trees are a special case, and LSSS matrices are equivalent to monotone span programs (Beimel 1996). Waters (2011) built CP-ABE for LSSS policies.

### Other constructions

| scheme | year | type | policy | assumption | security |
|---|---|---|---|---|---|
| Sahai-Waters (fuzzy IBE) | 2005 | threshold | one $d$-of-$n$ gate | DBDH | selective |
| GPSW | 2006 | KP | threshold trees, LSSS | DBDH | selective |
| BSW | 2007 | CP | threshold trees | generic group model | generic |
| Waters | 2011 | CP | LSSS | q-type parallel BDHE | selective |
| LOSTW | 2010 | KP and CP | LSSS | decision linear and related | adaptive |
| GVW | 2013 | KP | circuits of bounded depth | [LWE](/learning-with-errors/) | selective |

## Examples and non-examples

**A hand-sized key and ciphertext.** Track every element of $\mathbb{G}_T$ as a power of $e(P, P)$ and every point as a multiple of $P$, with exponents modulo $r = 11$, as in a group of order 11. The universe is $\{A, B, C\}$ with $t_A = 2$, $t_B = 3$, $t_C = 5$, and $y = 7$. The key policy is $A \text{ AND } (B \text{ OR } C)$: a 2-of-2 root with children $A$ (index 1) and an OR gate (index 2), whose children are $B$ and $C$.

| step | computation | result |
|---|---|---|
| root polynomial | $q_{\mathrm{root}}(x) = 7 + 3x$ | $q(1) = 10$, $q(2) = 13 \equiv 2$ |
| OR gate | degree 0, $q_{\mathrm{OR}}(x) = 2$ | $B$ and $C$ both get 2 |
| leaves | $D_A = \frac{10}{2}P$, $D_B = \frac{2}{3}P$, $D_C = \frac{2}{5}P$ | $5P$, $8P$, $7P$ |
| encrypt to $\{A, C\}$ with $s = 4$ | $E_A = 4 \cdot 2 P$, $E_C = 4 \cdot 5P$ | $8P$, $9P$; $Y^s = e(P,P)^{28} = e(P,P)^6$ |
| leaf $A$ | $e(5P, 8P)$ | $e(P,P)^{40} = e(P,P)^7 = e(P,P)^{s \cdot 10}$ |
| leaf $C$, then OR | $e(7P, 9P)$, one child, $\Delta = 1$ | $e(P,P)^{63} = e(P,P)^8 = e(P,P)^{s \cdot 2}$ |
| root, $S = \{1, 2\}$ | $\Delta_{1,S}(0) = 2$, $\Delta_{2,S}(0) = -1$ | $2 \cdot 7 - 8 = 6$, so $e(P,P)^6 = Y^s$ |

A ciphertext for $\{A, B\}$ also opens; one for $\{B, C\}$ does not, since the root needs the share at index 1, which only $A$ gives.

**The code with this page.** The Python file implements GPSW KP-ABE with threshold trees on a toy curve with a 128-binary-digit $p$ and $r = 2^{63} + 29$. The curve is not secure, and the code is for study only and is not constant time. For real use, take a maintained ABE library, such as the schemes in the Charm framework, on a curve such as BLS12-381. There are no official test vectors for ABE. The tests check the table above, decryption for satisfied and unsatisfied policies, a 2-of-3 gate, and a collusion: Alice with $A \text{ AND } C$ and Bob with $D \text{ AND } B$ pool their $A$ and $B$ shares against a ciphertext for $\{A, B\}$ and get a wrong value, while a single key for $A \text{ AND } B$ succeeds.

**Non-example: one key per attribute.** Give every attribute $a$ an ordinary key pair, give a user the secret keys of its attributes, and encrypt for "$A$ AND $B$" by encrypting under both keys in turn. This is correct but not collusion resistant: a user with only $A$ and a user with only $B$ together decrypt. The per-key randomness of real ABE is what prevents it.

**Non-example: encryption to a list of users.** Encrypting a key separately to every user whose attributes fit the policy is not ABE. The sender must know all users in advance, and a user who joins later cannot read older data. In ABE the sender needs only the policy and $\mathsf{mpk}$.

## Related definitions

- **[Identity-based encryption](/identity-based-encryption/)** is ABE with one attribute and an equality policy. ABE, like IBE, has a key authority that can decrypt everything.
- **[Functional encryption](/functional-encryption/)** generalizes ABE. ABE reveals the whole message to a key that matches, and nothing otherwise; the attributes themselves are public. Predicate encryption also hides the attributes.
- **[Shamir secret sharing](/shamir-secret-sharing/)** and **[secret sharing](/secret-sharing/)** give the shares in the keys; recombination uses [Lagrange interpolation](/lagrange-interpolation/) in the exponent.
- **[Bilinear Diffie-Hellman](/bilinear-diffie-hellman/)**: the decisional form is the assumption of the fuzzy IBE and GPSW schemes.
- **[Broadcast encryption](/broadcast-encryption/)** is related: it targets a set of users instead of a policy over attributes, and also needs collusion resistance.

## References
