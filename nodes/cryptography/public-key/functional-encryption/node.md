---
tag: YYQV99
kind: definition
slug: functional-encryption
name: Functional encryption
area: cryptography/public-key
level: research
summary: "Public-key encryption in which a key for a function f lets its holder learn f(x) from an encryption of x, and nothing else. IBE, ABE and inner-product FE are special cases."
prereqs: [attribute-based-encryption, decisional-diffie-hellman]
see_also: [identity-based-encryption, homomorphic-encryption, baby-step-giant-step, elgamal-encryption, learning-with-errors, broadcast-encryption, semantic-security, secure-multiparty-computation]
sources:
  - paper: "Dan Boneh, Amit Sahai and Brent Waters, Functional encryption, definitions and challenges, TCC 2011, LNCS 6597, pages 253 to 273"
    locator: the definition of a functionality with the empty key, the indistinguishability game, the simulation-based definition, the example where indistinguishability is too weak, and the impossibility of simulation security for IBE with key queries after the challenge
  - paper: "Adam O'Neill, Definitional issues in functional encryption, Cryptology ePrint Archive, Report 2010/556"
    locator: the simulation-based definition and its equivalence with the indistinguishability definition for preimage sampleable functionalities with non-adaptive key queries
  - paper: "Michel Abdalla, Florian Bourse, Angelo De Caro and David Pointcheval, Simple functional encryption schemes for inner products, PKC 2015, LNCS 9020, pages 733 to 751"
    locator: the inner-product scheme from DDH with decryption by a small discrete logarithm, and its selective security
  - paper: "Shweta Agrawal, Benoit Libert and Damien Stehle, Fully secure functional encryption for inner products, from standard assumptions, Crypto 2016, LNCS 9816, pages 333 to 362"
    locator: adaptively secure inner-product FE from DDH, from LWE and from DCR
  - paper: "Shweta Agrawal, Sergey Gorbunov, Vinod Vaikuntanathan and Hoeteck Wee, Functional encryption, new perspectives and lower bounds, Crypto 2013, LNCS 8043, pages 500 to 518"
    locator: the lower bounds for simulation-secure FE with many key queries or many ciphertexts
  - paper: "Sanjam Garg, Craig Gentry, Shai Halevi, Mariana Raykova, Amit Sahai and Brent Waters, Candidate indistinguishability obfuscation and functional encryption for all circuits, FOCS 2013, pages 40 to 49"
    locator: functional encryption for all circuits from indistinguishability obfuscation
  - paper: "Prabhanjan Ananth and Abhishek Jain, Indistinguishability obfuscation from compact functional encryption, Crypto 2015, LNCS 9215, pages 308 to 326"
    locator: the construction of iO from compact functional encryption
  - paper: "Nir Bitansky and Vinod Vaikuntanathan, Indistinguishability obfuscation from functional encryption, FOCS 2015, pages 171 to 190"
    locator: the construction of iO from compact functional encryption
  - paper: "Aayush Jain, Huijia Lin and Amit Sahai, Indistinguishability obfuscation from well-founded assumptions, STOC 2021, pages 60 to 73"
    locator: iO, and so FE for all circuits, from the subexponential hardness of well-studied assumptions, among them LPN over fields, a PRG in NC0 and an assumption on pairing groups
---

Functional encryption (FE) is [public-key encryption](/public-key-encryption/) with keys for functions. The owner of a master secret key gives out a key $\mathsf{sk}_f$ for a function $f$, and anyone who holds $\mathsf{sk}_f$ and an encryption of $x$ learns $f(x)$, and nothing more about $x$. Ordinary encryption gives all or nothing; FE gives exactly the result of a chosen computation. [Identity-based](/identity-based-encryption/) and [attribute-based encryption](/attribute-based-encryption/) are special cases. Dan Boneh, Amit Sahai and Brent Waters gave the general definitions in 2011, and Adam O'Neill independently studied them in 2010. The simplest practical class is **inner-product FE**, where a key for a vector $y$ reveals $\langle x, y \rangle$; Abdalla, Bourse, De Caro and Pointcheval built it from DDH in 2015. FE for all circuits is closely linked to indistinguishability obfuscation.

**Notation.** $\kappa$ is the security parameter. A **functionality** is a function $F : \mathcal{K} \times \mathcal{X} \to \mathcal{Y}$; a key $k \in \mathcal{K}$ names a function $F(k, \cdot)$. As in Boneh, Sahai and Waters, $\mathcal{K}$ has a special **empty key** $\varepsilon$, and $F(\varepsilon, x)$ is what every ciphertext leaks anyway, such as the length of $x$, or the attributes in ABE. For inner-product FE, $\mathbb{G} = \langle g \rangle$ is a group of prime order $q$, $\ell$ is the dimension, and $\langle x, y \rangle = \sum_i x_i y_i$.

## Definition

A **functional encryption scheme** for $F$ consists of four probabilistic polynomial time algorithms.

- $\mathsf{Setup}(1^\kappa) \to (\mathsf{mpk}, \mathsf{msk})$.
- $\mathsf{KeyGen}(\mathsf{msk}, k) \to \mathsf{sk}_k$ for $k \in \mathcal{K}$.
- $\mathsf{Enc}(\mathsf{mpk}, x) \to c$ for $x \in \mathcal{X}$.
- $\mathsf{Dec}(\mathsf{sk}_k, c) \to y$.

**Correctness.** $\mathsf{Dec}(\mathsf{sk}_k, \mathsf{Enc}(\mathsf{mpk}, x)) = F(k, x)$ for all $k$ and $x$, with probability 1, or with all but negligible probability.

### Indistinguishability security

In the **IND game**, the adversary gets $\mathsf{mpk}$, asks for keys $\mathsf{sk}_{k_1}, \mathsf{sk}_{k_2}, \ldots$, outputs two messages $x_0, x_1$, gets $\mathsf{Enc}(\mathsf{mpk}, x_\beta)$ for a uniform bit $\beta$, asks for more keys, and guesses $\beta$. The rule is that $F(k_i, x_0) = F(k_i, x_1)$ for every key it asks for, before or after the challenge, and also for $k = \varepsilon$. Without this rule the adversary would win at once by decrypting. The scheme is IND-secure if every efficient adversary has negligible advantage. In the **selective** game, the adversary names $x_0, x_1$ before it sees $\mathsf{mpk}$.

The game includes collusion: the adversary holds many keys, and they together must reveal no more than all their function values.

### Simulation security

IND security can be too weak. Boneh, Sahai and Waters give a functionality and a scheme that is IND-secure but leaks more than the function value; the problem arises when $F(k, \cdot)$ is hard to invert, so that no two messages have the same outputs and the IND rule leaves nothing to prove. **Simulation (SIM) security** asks instead that, for every adversary, a simulator that sees only the values $F(k_i, x)$ for the keys asked for can produce the same view. SIM security is stronger, but it cannot always be met:

- Boneh, Sahai and Waters show that no IBE scheme is SIM-secure in the standard model when the adversary may ask for keys after it sees the challenge ciphertexts.
- Agrawal, Gorbunov, Vaikuntanathan and Wee (2013) show lower bounds for SIM security when the adversary may ask for many keys before the challenge, or sees many ciphertexts.
- O'Neill shows that the two notions agree for a large class of functionalities (the preimage sampleable ones) when all key queries come before the challenge.

So positive results for general functionalities are stated with IND security, and SIM security holds only for bounded numbers of keys or special functionalities.

### Special cases

| scheme type | key $k$ | $F(k, x)$ | $F(\varepsilon, x)$ |
|---|---|---|---|
| [public-key encryption](/public-key-encryption/) | one key | $m$ | $\lvert m \rvert$ |
| [identity-based encryption](/identity-based-encryption/), $x = (\mathsf{id}, m)$ | an identity $\mathsf{id}'$ | $m$ if $\mathsf{id}' = \mathsf{id}$, else $\bot$ | $(\mathsf{id}, \lvert m \rvert)$ |
| [attribute-based encryption](/attribute-based-encryption/), $x = (\gamma, m)$ | a policy $\mathbb{A}$ | $m$ if $\mathbb{A}(\gamma) = 1$, else $\bot$ | $(\gamma, \lvert m \rvert)$ |
| predicate encryption, $x = (\gamma, m)$ | a predicate $P$ | $m$ if $P(\gamma) = 1$, else $\bot$ | $\lvert m \rvert$ |
| inner-product FE | a vector $y$ | $\langle x, y \rangle$ | $\ell$ |

### Inner-product FE from DDH (ABDP 2015)

```pseudo
SETUP(ℓ)
1   s_1, …, s_ℓ ← uniform in Z_q
2   return mpk = (h_i = g^(s_i))_i and msk = (s_i)_i

KEYGEN(msk, y)
3   return sk_y = ⟨s, y⟩ mod q

ENCRYPT(mpk, x)                     ▷ x ∈ Z^ℓ with small entries
4   r ← uniform in Z_q
5   return (c_0 = g^r, c_i = h_i^r · g^(x_i) for i = 1..ℓ)

DECRYPT(sk_y, y, c)
6   z ← (∏ c_i^(y_i)) / c_0^(sk_y)       ▷ z = g^⟨x, y⟩
7   return the discrete logarithm of z, found in a small range
```

Line 6 gives $\prod_i c_i^{y_i} = g^{r\langle s, y \rangle + \langle x, y \rangle}$ and $c_0^{\mathsf{sk}_y} = g^{r\langle s, y \rangle}$, so $z = g^{\langle x, y \rangle}$. Line 7 needs a discrete logarithm, so the scheme works only when $|\langle x, y \rangle| \le B$ for a known bound $B$; [baby-step giant-step](/baby-step-giant-step/) then takes $O(\sqrt{B})$ group operations. This is the same limit as exponential [ElGamal](/elgamal-encryption/), which the scheme extends. ABDP prove it selectively IND-secure under [DDH](/decisional-diffie-hellman/). Agrawal, Libert and Stehle (2016) gave adaptively secure schemes from DDH, from [LWE](/learning-with-errors/) and from DCR; the DCR scheme decrypts without a small discrete logarithm.

A key is one number, and a ciphertext has $\ell + 1$ group elements. Keys for $\ell$ linearly independent vectors reveal $x$ completely, and they also reveal $s$. This is not a break: those function values already determine $x$, and the definition promises only that nothing beyond them leaks.

### FE for all circuits and obfuscation

Garg, Gentry, Halevi, Raykova, Sahai and Waters (2013) built FE for all circuits from indistinguishability obfuscation (iO). In the other direction, Ananth and Jain and, independently, Bitansky and Vaikuntanathan (2015) built iO from **compact** FE, in which the size of a ciphertext grows less than the size of the circuits. So general compact FE and iO are essentially equivalent. Jain, Lin and Sahai (2021) built iO from well-founded assumptions, which gives FE for all circuits, but far from a practical cost. Inner-product and quadratic FE remain the practical cases.

## Examples and non-examples

**Inner-product FE with toy numbers.** Take $p = 23$ and the subgroup of squares, of order $q = 11$, generated by $g = 4$. Let $\ell = 2$ and $s = (3, 5)$, so $\mathsf{mpk} = (4^3, 4^5) = (18, 12)$. Encrypt $x = (2, 1)$ with $r = 6$: $c_0 = 4^6 = 2$, $c_1 = 18^6 \cdot 4^2 = 13$ and $c_2 = 12^6 \cdot 4 = 13$, all modulo 23. The key for $y = (1, 3)$ is $\mathsf{sk}_y = 3 + 15 = 18 \equiv 7 \pmod{11}$. Decryption computes $c_1 \cdot c_2^3 = 13^4 = 18$ and $c_0^7 = 2^7 = 13$, and $18 / 13 = 18 \cdot 16 = 12 = 4^5$ modulo 23, so $\langle x, y \rangle = 5$, which is $2 + 3$. A group of 11 elements is, of course, not secure.

**The code with this page.** The Python file implements the ABDP scheme in the subgroup of squares modulo a 129-binary-digit safe prime, with a local baby-step giant-step search. The group is too small to be secure, and the code is for study only and is not constant time. For real use, take a maintained FE library, such as CiFEr or GoFE from the FENTEC project. There are no official test vectors for inner-product FE. The tests check the toy example above, random inner products, that a key for one vector does not give the inner product with another, and that $\ell$ unit-vector keys reveal $x$, with fixed seeds.

**Example: a statistic over encrypted data.** A hospital encrypts the vector of risk factors $x$ of each patient. A researcher with a key for the weights $y$ of a linear model gets each score $\langle x, y \rangle$, but no single factor, as long as it does not hold keys that together span the unit vectors.

**Non-example: fully homomorphic encryption.** [Homomorphic encryption](/homomorphic-encryption/) lets anyone compute an encryption of $f(x)$ from an encryption of $x$, but the result is still encrypted, and only the holder of the full secret key can read it. FE gives $f(x)$ in the clear to the holder of $\mathsf{sk}_f$ and does not let it read $x$.

**Non-example: handing out the decryption key.** Giving an analyst the secret key of an ordinary scheme, with the instruction to compute only $f(x)$, is not FE: the key reveals all of $x$. FE enforces the limit by cryptography.

**Non-example: inner products out of range.** If $\langle x, y \rangle$ is a large number modulo $q$, line 6 still gives $g^{\langle x, y \rangle}$, but line 7 cannot find it. The DDH scheme computes the functionality only for small results.

## Related definitions

- **[Identity-based encryption](/identity-based-encryption/)** and **[attribute-based encryption](/attribute-based-encryption/)** are the FE schemes for equality tests and policies with public attributes. They were the starting point of the general notion.
- **[Homomorphic encryption](/homomorphic-encryption/)** computes on ciphertexts but keeps the results secret; FE reveals the results to key holders.
- **[Semantic security](/semantic-security/)**: the simulation definition of FE extends it, with the function values given to the simulator.
- **[Secure multiparty computation](/secure-multiparty-computation/)** also reveals only a function value, but needs interaction among the parties; FE is non-interactive with a trusted key authority.
- **[Broadcast encryption](/broadcast-encryption/)** can be seen as FE for the functionality "$m$ if the user is in the set $S$".

## References
