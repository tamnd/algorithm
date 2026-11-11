---
tag: KQRAAQ
kind: definition
slug: identity-based-encryption
name: Identity-based encryption
aliases:
- IBE
area: cryptography/public-key
level: advanced
summary: "Public-key encryption in which any string, such as an email address, is the public key. A trusted key generator holds a master key and gives each user the private key for its identity."
prereqs: [public-key-encryption, ind-cpa-security]
see_also: [boneh-franklin-ibe, bilinear-diffie-hellman, bilinear-pairing, attribute-based-encryption, functional-encryption, quadratic-residuosity-problem, ind-cca-security, random-oracle-model]
sources:
  - paper: "Adi Shamir, Identity-based cryptosystems and signature schemes, Crypto 1984, LNCS 196, pages 47 to 53"
    locator: the idea of an identity as the public key with a trusted key generation center, the open problem of identity-based encryption, and the identity-based signature scheme from RSA
  - paper: "Dan Boneh and Matthew Franklin, Identity-based encryption from the Weil pairing, SIAM Journal on Computing 32(3), 2003, pages 586 to 615"
    locator: the four algorithms of an IBE scheme, the IND-ID-CPA and IND-ID-CCA games, the threshold PKG, revocation by identities with a date, and the remark of Naor that an IBE scheme gives a signature scheme
  - paper: "Clifford Cocks, An identity based encryption scheme based on quadratic residues, Cryptography and Coding, 8th IMA International Conference, 2001, LNCS 2260, pages 360 to 363"
    locator: the scheme with N = pq, p and q = 3 (mod 4), the private key r with r^2 = a or -a, and the decryption by a Jacobi symbol
  - paper: "Ran Canetti, Shai Halevi and Jonathan Katz, A forward-secure public-key encryption scheme, Eurocrypt 2003, LNCS 2656, pages 255 to 271"
    locator: the selective-node (selective identity) security notion, in which the adversary names the target before it sees the public parameters
  - paper: "Dan Boneh and Xavier Boyen, Efficient selective-ID secure identity based encryption without random oracles, Eurocrypt 2004, LNCS 3027, pages 223 to 238"
    locator: the two selective-ID secure schemes in the standard model, under DBDH and under decisional q-BDHI
  - paper: "Brent Waters, Efficient identity-based encryption without random oracles, Eurocrypt 2005, LNCS 3494, pages 114 to 127"
    locator: the fully secure scheme under DBDH in the standard model, with public parameters that grow with the length of the identity
  - paper: "Ran Canetti, Shai Halevi and Jonathan Katz, Chosen-ciphertext security from identity-based encryption, Eurocrypt 2004, LNCS 3027, pages 207 to 222"
    locator: the transform from a selective-ID IND-ID-CPA scheme and a one-time signature to an IND-CCA public-key scheme
  - paper: "Craig Gentry, Chris Peikert and Vinod Vaikuntanathan, Trapdoors for hard lattices and new cryptographic constructions, STOC 2008, pages 197 to 206"
    locator: the identity-based encryption scheme from lattice trapdoors under LWE in the random oracle model
  - paper: "Sattam S. Al-Riyami and Kenneth G. Paterson, Certificateless public key cryptography, Asiacrypt 2003, LNCS 2894, pages 452 to 473"
    locator: the model that removes key escrow by combining a partial key from the authority with a secret of the user
---

Identity-based encryption (IBE) is [public-key encryption](/public-key-encryption/) in which the public key of a user is any string that names the user, such as an email address. The sender needs no certificate and no key lookup: with one set of public parameters, it can encrypt to an identity before the owner has even asked for its private key. The price is a trusted **private key generator** (PKG), which holds a master secret and derives the private key of every identity. Adi Shamir proposed the idea in 1984 and built identity-based signatures, but left encryption open. The first practical schemes came in 2001: [Boneh-Franklin](/boneh-franklin-ibe/) from [bilinear pairings](/bilinear-pairing/), and Clifford Cocks's scheme from quadratic residues. IBE later grew into [attribute-based](/attribute-based-encryption/) and [functional encryption](/functional-encryption/).

**Notation.** $\kappa$ is the security parameter, $\mathsf{mpk}$ and $\mathsf{msk}$ are the master public and secret keys, $\mathsf{id} \in \{0,1\}^*$ is an identity, $\mathsf{sk}_{\mathsf{id}}$ is its private key, $\mathcal{M}$ is the message space, and $\mathcal{A}$ is an adversary.

## Definition

An **identity-based encryption scheme** is a tuple of four probabilistic polynomial time algorithms.

- $\mathsf{Setup}(1^\kappa) \to (\mathsf{mpk}, \mathsf{msk})$. The PKG runs it once and publishes $\mathsf{mpk}$.
- $\mathsf{Extract}(\mathsf{msk}, \mathsf{id}) \to \mathsf{sk}_{\mathsf{id}}$. The PKG runs it when the owner of $\mathsf{id}$ proves that it owns the identity.
- $\mathsf{Enc}(\mathsf{mpk}, \mathsf{id}, m) \to c$ for $m \in \mathcal{M}$.
- $\mathsf{Dec}(\mathsf{sk}_{\mathsf{id}}, c) \to m$ or $\bot$.

**Correctness.** For all $(\mathsf{mpk}, \mathsf{msk})$ output by $\mathsf{Setup}$, all identities $\mathsf{id}$, all $\mathsf{sk}_{\mathsf{id}}$ output by $\mathsf{Extract}(\mathsf{msk}, \mathsf{id})$ and all $m \in \mathcal{M}$, $\mathsf{Dec}(\mathsf{sk}_{\mathsf{id}}, \mathsf{Enc}(\mathsf{mpk}, \mathsf{id}, m)) = m$.

### Security

The adversary of an IBE scheme may hold the private keys of many users, so the games give it a key oracle. Boneh and Franklin defined the following game.

**IND-ID-CPA game.**

1. The challenger runs $\mathsf{Setup}$ and gives $\mathsf{mpk}$ to $\mathcal{A}$.
2. $\mathcal{A}$ asks for keys $\mathsf{sk}_{\mathsf{id}}$ of identities of its choice.
3. $\mathcal{A}$ outputs a target $\mathsf{id}^*$, whose key it has not asked for, and two messages $m_0, m_1$ of the same length.
4. The challenger picks a uniform bit $\beta$ and returns $c^* = \mathsf{Enc}(\mathsf{mpk}, \mathsf{id}^*, m_\beta)$.
5. $\mathcal{A}$ asks for more keys, but not for $\mathsf{sk}_{\mathsf{id}^*}$, and outputs a bit $\beta'$.

The advantage is $\mathrm{Adv}(\mathcal{A}) = |\Pr[\beta' = \beta] - 1/2|$. The scheme is **IND-ID-CPA secure** if every efficient $\mathcal{A}$ has negligible advantage.

**IND-ID-CCA.** The adversary also gets a decryption oracle for any pair $(\mathsf{id}, c)$ other than $(\mathsf{id}^*, c^*)$. This is the analog of [IND-CCA](/ind-cca-security/) security.

**Selective-ID security.** Canetti, Halevi and Katz (2003) made the adversary commit to $\mathsf{id}^*$ before step 1. This notion, IND-sID-CPA, is weaker. It is easier to prove, because the reduction can plant the target in $\mathsf{mpk}$. The notion above, with the target chosen at the end, is called **full** or **adaptive** security. A selective-ID scheme is fully secure if the reduction guesses $\mathsf{id}^*$ in advance, but with $2^n$ identities that loses a factor $2^n$. In the random oracle model, with identities hashed first, the loss is only the number $q_H$ of hash queries, since the reduction guesses which query gives the target.

### Facts

- **IBE gives signatures.** Boneh and Franklin credit Moni Naor with this remark. Let the master key pair be the signing key pair, and let the signature on $m$ be $\mathsf{sk}_m$. To check a signature, encrypt a random value to the identity $m$ and test that the signature decrypts it. Forging a signature means finding the key of an identity that was not asked for. Shamir's 1984 signature scheme is identity-based in a different sense: there the identity is the verification key.
- **IBE gives CCA security.** Canetti, Halevi and Katz (2004) turn a selective-ID IND-ID-CPA scheme and a strong one-time signature into an [IND-CCA](/ind-cca-security/) public-key scheme: encrypt to the identity that is the one-time verification key, and sign the ciphertext.
- **Key escrow is built in.** The PKG can compute $\mathsf{sk}_{\mathsf{id}}$ for every $\mathsf{id}$, so it can read all mail. Boneh and Franklin suggest a threshold PKG, with $\mathsf{msk}$ shared among several servers. Certificateless cryptography (Al-Riyami and Paterson 2003) adds a user secret, so the authority alone cannot decrypt, but then the public key is no longer only the identity.
- **Revocation** is harder than with certificates. A simple method, from Boneh and Franklin, is to encrypt to "$\mathsf{id}$ for a given date", so that a key is valid only for that date and the PKG stops giving keys to revoked users.

### Schemes

| scheme | year | assumption | model | security |
|---|---|---|---|---|
| [Boneh-Franklin](/boneh-franklin-ibe/) | 2001 | [BDH](/bilinear-diffie-hellman/) | random oracles | IND-ID-CCA (FullIdent) |
| Cocks | 2001 | [quadratic residuosity](/quadratic-residuosity-problem/) | random oracles | IND-ID-CPA |
| Boneh-Boyen (BB1) | 2004 | DBDH | standard | IND-sID-CPA |
| Boneh-Boyen (BB2) | 2004 | decisional q-BDHI | standard | IND-sID-CPA |
| Waters | 2005 | DBDH | standard | IND-ID-CPA, full |
| Gentry-Peikert-Vaikuntanathan | 2008 | [LWE](/learning-with-errors/) | random oracles | IND-ID-CPA |

Waters's scheme was the first practical one with full security in the standard model. Its public parameters hold about one group element per binary digit of the identity, and its reduction loses a factor that grows with the number of key queries. Hierarchical IBE, in which a user can derive keys for its sub-identities, was introduced by Horwitz and Lynn and built by Gentry and Silverberg in 2002.

## Examples and non-examples

**Boneh-Franklin.** The public parameters are $P$ and $P_{\mathrm{pub}} = sP$ in a pairing group, and the private key of $\mathsf{id}$ is $s \cdot H_1(\mathsf{id})$, where $H_1$ hashes to the group. A ciphertext is $(rP, m \oplus H_2(e(H_1(\mathsf{id}), P_{\mathrm{pub}})^r))$. The page [Boneh-Franklin IBE](/boneh-franklin-ibe/) gives the details, a proof and code.

**Cocks with toy numbers.** The PKG picks primes $p = 7$ and $q = 11$, both $3 \bmod 4$, and publishes $N = 77$. A hash maps the identity to $a$ with Jacobi symbol $(a/N) = 1$; say $a = 6$. Then $(6/7) = (6/11) = -1$, so $a$ is not a square, but $-a = 71$ is. The private key is $r = a^{(N + 5 - p - q)/8} = 6^8 \bmod 77 = 15$, and $r^2 = 225 \equiv 71 = -a$. To encrypt a bit $x = -1$, the sender, who does not know whether $a$ or $-a$ is the square, picks $t = 3$ and $t' = 2$, both with Jacobi symbol $-1$, and sends $s = t + a/t = 3 + 2 = 5$ and $s' = t' - a/t' = 2 + 71 \cdot 39 \equiv 76 \pmod{77}$. Since $r^2 = -a$, the owner uses $s'$: $s' + 2r = (t' + r)^2/t'$, and $(106 \bmod 77 / 77) = (29/77) = (29/7)(29/11) = 1 \cdot (-1) = -1 = x$. The scheme sends two elements of $\mathbb{Z}_N$ for every bit of the message, so it is used only for short keys. These numbers are far too small to be secure.

**Non-example: RSA with a shared modulus.** Let the PKG keep the factors of $N$ and give each user the exponent $e = H(\mathsf{id})$ and its inverse $d$. This is not secure: any user who knows one pair $(e, d)$ can factor $N$, and then compute the private key of every other user. Shamir notes that RSA does not give IBE in this simple way.

**Non-example: a certificate directory.** In ordinary public-key infrastructure, the key of a user is chosen by the user and bound to its name by a certificate. The sender must fetch and check the certificate first, and cannot encrypt to someone who has no key yet. There is no key escrow, which is the main reason why certificates are still used more than IBE.

## Related definitions

- **[Public-key encryption](/public-key-encryption/)**: IBE with only one identity is ordinary public-key encryption, with $\mathsf{sk}_{\mathsf{id}}$ as the secret key.
- **[IND-CPA](/ind-cpa-security/)** and **[IND-CCA](/ind-cca-security/)**: IND-ID-CPA and IND-ID-CCA add the key oracle to them.
- **[Bilinear Diffie-Hellman](/bilinear-diffie-hellman/)**: the assumption of Boneh-Franklin, and in its decisional form, of Boneh-Boyen and Waters.
- **[Quadratic residuosity problem](/quadratic-residuosity-problem/)**: the assumption of Cocks's scheme.
- **[Attribute-based encryption](/attribute-based-encryption/)**: keys and ciphertexts carry attributes and policies, and IBE is the case of one attribute and an equality test.
- **[Functional encryption](/functional-encryption/)**: the general notion, of which IBE is a special case in which the function reveals $m$ only when the identity matches.
- **[Random oracle model](/random-oracle-model/)**: the model of the first proofs for Boneh-Franklin and Cocks.

## References
