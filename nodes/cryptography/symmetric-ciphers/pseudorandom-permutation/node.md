---
tag: MQ7VH2
kind: definition
slug: pseudorandom-permutation
name: Pseudorandom permutation
aliases:
- PRP
area: cryptography/symmetric-ciphers
level: advanced
summary: A keyed permutation family that no efficient adversary can tell from a random permutation. A strong PRP also resists inverse queries. It is the security notion of a block cipher.
prereqs: [pseudorandom-function, block-cipher]
see_also: [prp-prf-switching-lemma, luby-rackoff-theorem, feistel-network, ideal-cipher-model, key-recovery, advanced-encryption-standard, random-permutation, semantic-security]
sources:
  - paper: doi:10.1137/0217022
    title: Michael Luby and Charles Rackoff, How to construct pseudorandom permutations from pseudorandom functions, SIAM Journal on Computing 17(2), 1988
    locator: the definitions of pseudorandom and super-pseudorandom permutation generators and the Feistel constructions
  - paper: doi:10.1006/jcss.1999.1694
    title: Mihir Bellare, Joe Kilian and Phillip Rogaway, The security of the cipher block chaining message authentication code, Journal of Computer and System Sciences 61(3), 2000
    locator: the concrete definitions of PRP security and the use of a block cipher as a PRP
  - paper: doi:10.1007/PL00003817
    title: Moni Naor and Omer Reingold, On the construction of pseudorandom permutations, Luby-Rackoff revisited, Journal of Cryptology 12(1), 1999
    locator: the strong PRP notion and the constructions with pairwise independent rounds
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: the sections on pseudorandom permutations, strong pseudorandom permutations and block ciphers
---

A pseudorandom permutation (PRP) is a family of keyed permutations $E_K$ of $\{0,1\}^n$ that no efficient adversary can tell apart from a permutation chosen uniformly from all $(2^n)!$ permutations, when it may query the permutation but not see the key. A *strong* PRP (sPRP), called super-pseudorandom by Luby and Rackoff, resists an adversary that may also query the inverse. These are the standard security notions for a [block cipher](/block-cipher/): proofs of modes such as CTR, CBC and GCM assume that AES is a PRP or an sPRP. A PRP is also a [PRF](/pseudorandom-function/) up to the birthday bound, by the [switching lemma](/prp-prf-switching-lemma/), and a PRF gives a PRP by the [Luby-Rackoff theorem](/luby-rackoff-theorem/).

## Definition

**Permutation family.** Let $E : \{0,1\}^k \times \{0,1\}^n \to \{0,1\}^n$ be such that each $E_K = E(K, \cdot)$ is a permutation of $\{0,1\}^n$, and both $E_K$ and $E_K^{-1}$ are computable in polynomial time from $K$. Let $\mathrm{Perm}(n)$ be the set of all permutations of $\{0,1\}^n$.

**The PRP game.**

1. The challenger picks a bit $b$ uniformly.
2. If $b = 1$, it picks $K$ uniformly and sets $O = E_K$. If $b = 0$, it picks $\pi$ uniformly from $\mathrm{Perm}(n)$ and sets $O = \pi$. Lazily: on a new query $x$, $\pi(x)$ is uniform over the values not yet used as outputs.
3. $A$ makes adaptive queries $x_i$ and gets $O(x_i)$.
4. $A$ outputs a bit $b'$.

$$\mathrm{Adv}^{\mathrm{prp}}_E(A) = \Bigl| \Pr_K\bigl[A^{E_K} = 1\bigr] - \Pr_\pi\bigl[A^{\pi} = 1\bigr] \Bigr|.$$

**The strong PRP game.** The same, except that $A$ gets two oracles: $O$ and $O^{-1}$, that is $E_K$ and $E_K^{-1}$ if $b = 1$, and $\pi$ and $\pi^{-1}$ if $b = 0$. Lazily, a new inverse query $y$ gets $\pi^{-1}(y)$ uniform over the inputs not yet used.

$$\mathrm{Adv}^{\mathrm{sprp}}_E(A) = \Bigl| \Pr_K\bigl[A^{E_K, E_K^{-1}} = 1\bigr] - \Pr_\pi\bigl[A^{\pi, \pi^{-1}} = 1\bigr] \Bigr|.$$

**Security.** $E$ is a $(t, q, \varepsilon)$-PRP, or sPRP, if every adversary that runs in time at most $t$ and makes at most $q$ queries in total has advantage at most $\varepsilon$ in the matching game. Asymptotically, $E$ is a PRP if the advantage of every probabilistic polynomial-time adversary is negligible in the security parameter. Every sPRP is a PRP, since an adversary in the PRP game is an adversary in the sPRP game that does not use $O^{-1}$.

**Generic bounds.** Exhaustive key search gives an adversary with $t \approx s \cdot 2^k$ cipher calls and $s = \lceil k/n \rceil + 1$ queries and advantage close to 1, so no PRP has $\varepsilon$ small when $t \ge 2^k$. More generally, an adversary with time $t$ has advantage at least about $t/2^k$. Any key recovery attack with success $\delta$ gives a PRP adversary with advantage at least $\delta - 1/(2^n - q)$; see [key recovery](/key-recovery/).

## Examples and non-examples

- **AES.** AES is conjectured to be an sPRP with $\varepsilon \approx t/2^{k}$ for the key length $k$; no attack contradicts this beyond the small factor of the biclique attack.
- **Four-round Luby-Rackoff.** A Feistel network of 4 rounds with independent PRFs as round functions is an sPRP, with advantage at most about $q^2/2^{n/2}$ on $n$-bit blocks, plus the PRF terms. See the [Luby-Rackoff theorem](/luby-rackoff-theorem/).
- **A PRP that is not strong: three-round Luby-Rackoff.** Three Feistel rounds are a PRP, but two forward queries and one inverse query tell them from a random permutation with advantage close to 1.
- **A PRP that is not strong, by design.** Let $E$ be an sPRP. Define $E'_K$ equal to $E_K$, except that it swaps the outputs of the two inputs $K$ and $E_K^{-1}(0^n)$, so $E'_K(K) = 0^n$. Forward queries hit these two inputs with probability about $2q/2^n$ unless the adversary breaks $E$, so $E'$ is a PRP. One inverse query at $0^n$ returns the key.
- **Non-example: two-round Feistel.** With halves $L, R$ and the round map $(L, R) \mapsto (R, L \oplus f(R))$, two queries $(L, R)$ and $(L', R)$ give outputs whose left halves differ by $L \oplus L'$. Advantage $1 - 2^{-n/2}$.
- **Non-example: an affine cipher.** $E_K(x) = Ax \oplus K$ with a public invertible matrix $A$. Then $E_K(x) \oplus E_K(x') = A(x \oplus x')$, checked with two queries.
- **Non-example: DES today.** DES is not a $(t, q, \varepsilon)$-PRP for any small $\varepsilon$ at $t = 2^{56}$, since exhaustive search finds the key; the EFF machine did this in 1998.
- **Non-example: the complement property.** DES satisfies $E_{\bar K}(\bar x) = \overline{E_K(x)}$. This alone does not break the PRP game, because the game uses one key, but it does break related-key notions.

## Related definitions

- **[Pseudorandom function](/pseudorandom-function/).** The same game with a random function. A PRP on $n$ bits is a PRF with an extra loss of at most $q(q-1)/2^{n+1}$, by the switching lemma. Conversely, a PRF gives a PRP by three Feistel rounds and an sPRP by four.
- **[Ideal cipher model](/ideal-cipher-model/).** Every key gives an independent random permutation, and the adversary may query any key. It is a model for proofs, not a property of a real cipher.
- **Tweakable PRP.** The permutation takes a public tweak $T$ as well, and each tweak must look like an independent random permutation. XTS and the OCB mode use this notion.
- **Related-key PRP.** The adversary may ask for $E_{\phi(K)}$ for functions $\phi$ from an allowed class. AES-256 is not secure in this sense for some classes; see [related-key attack](/related-key-attack/).
- **Small-domain PRPs.** Permutations of small sets, such as 16-digit card numbers, used in format-preserving encryption (NIST SP 800-38G). The term $q^2/2^n$ is large on small sets, so such designs need many Feistel rounds.
- **[Semantic security](/semantic-security/).** A PRP alone on single blocks is a deterministic encryption and is not IND-CPA secure. A mode with random IVs or nonces built on a PRP is.

## References
