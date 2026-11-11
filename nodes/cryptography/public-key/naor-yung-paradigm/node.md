---
tag: Q7BDF9
kind: technique
slug: naor-yung-paradigm
name: Naor-Yung double-encryption paradigm
aliases:
- Naor-Yung transform
- double encryption
area: cryptography/public-key
level: research
summary: Encrypt the message twice under two keys and attach a non-interactive zero-knowledge proof that both ciphertexts agree. Gives IND-CCA1, and IND-CCA2 with simulation-sound proofs.
prereqs: [ind-cca-security, zero-knowledge-proof]
see_also: [cramer-shoup-cryptosystem, non-malleability, fiat-shamir-heuristic, sigma-protocol, proof-of-knowledge, threshold-cryptography, elgamal-encryption, fujisaki-okamoto-transform]
sources:
  - paper: "Moni Naor and Moti Yung, Public-key cryptosystems provably secure against chosen ciphertext attacks, STOC 1990, pages 427 to 437"
    locator: the double-encryption construction and its IND-CCA1 security
  - paper: "Amit Sahai, Non-malleable non-interactive zero knowledge and adaptive chosen-ciphertext security, FOCS 1999, pages 543 to 553"
    locator: simulation-sound NIZK and the proof that Naor-Yung with it is IND-CCA2 secure
  - paper: "Danny Dolev, Cynthia Dwork and Moni Naor, Nonmalleable cryptography, SIAM Journal on Computing 30(2), pages 391 to 437, 2000"
    locator: the non-malleable encryption scheme with many encryptions, a one-time signature and a NIZK proof
  - paper: "Yehuda Lindell, A simpler construction of CCA2-secure public-key encryption under general assumptions, Eurocrypt 2003, LNCS 2656, pages 241 to 254"
    locator: Naor-Yung with a one-time signature and a one-time simulation-sound proof
  - paper: "Manuel Blum, Paul Feldman and Silvio Micali, Non-interactive zero-knowledge and its applications, STOC 1988, pages 103 to 112"
    locator: non-interactive zero-knowledge proofs with a common random string
  - paper: "Charles Rackoff and Daniel R. Simon, Non-interactive zero-knowledge proof of knowledge and chosen ciphertext attack, CRYPTO 1991, LNCS 576, pages 433 to 444"
    locator: the adaptive chosen-ciphertext attack and a construction from proofs of knowledge
  - paper: "Victor Shoup and Rosario Gennaro, Securing threshold cryptosystems against chosen ciphertext attack, Eurocrypt 1998, LNCS 1403, pages 1 to 16"
    locator: ElGamal with a Fiat-Shamir proof (TDH1 and TDH2), CCA secure in the random oracle model
  - paper: "Jens Groth and Amit Sahai, Efficient non-interactive proof systems for bilinear groups, Eurocrypt 2008, LNCS 4965, pages 415 to 432"
    locator: efficient NIZK proofs in pairing groups that make Naor-Yung practical in the standard model
  - paper: "David Bernhard, Olivier Pereira and Bogdan Warinschi, How not to prove yourself, pitfalls of the Fiat-Shamir heuristic and applications to Helios, Asiacrypt 2012, LNCS 7658, pages 626 to 643"
    locator: weak and strong Fiat-Shamir, and the attacks on encryption with weak Fiat-Shamir proofs
  - book: isbn:9780521830843
    title: Oded Goldreich, Foundations of Cryptography, Volume 2, Basic Applications, Cambridge University Press, 2004
    locator: Chapter 5, the constructions of encryption secure against chosen-ciphertext attacks from NIZK proofs
---

The Naor-Yung paradigm turns any [IND-CPA](/ind-cpa-security/) secure public-key scheme into one secure against chosen-ciphertext attacks. The sender encrypts the message twice, under two independent public keys, and attaches a non-interactive [zero-knowledge proof](/zero-knowledge-proof/) that the two ciphertexts hold the same message; the receiver checks the proof and decrypts one of them. Naor and Yung (1990) proved the result [IND-CCA1](/ind-cca-security/) secure, and Sahai (1999) proved it IND-CCA2 secure when the proof is simulation sound. It was the first route to chosen-ciphertext security from general assumptions, and it is still the template for encryption that must come with proofs, as in voting and threshold decryption.

**Notation.** $\Pi = (\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec})$ is an IND-CPA scheme. A NIZK proof system $(\mathcal{P}, \mathcal{V})$ works with a common reference string $\sigma$ and has a simulator $\mathcal{S}$ that makes $\sigma$ with a trapdoor and then makes proofs without witnesses. $L$ is the language of consistent pairs (defined below). $\lambda$ is the security parameter, $\mathcal{A}$ an adversary that runs in time $t$ and makes $q_d$ decryption queries, and $\mathrm{Adv}$ an advantage. The results here are in the standard model with a common reference string; the Fiat-Shamir variants are in the [random oracle model](/random-oracle-model/).

## In plain words

An encryption scheme that is safe against listeners can still fail when the attacker may ask the receiver to decrypt ciphertexts of its own. The attacker changes the target ciphertext a little, asks for the decryption, and learns something about the target.

Naor and Yung stop this by making every ciphertext carry evidence that its sender knew what it encrypted. The sender locks the message in two boxes with two different public keys and adds a short proof that both boxes hold the same thing. The proof shows nothing else. The receiver rejects any ciphertext whose proof fails. In the security argument this lets a simulator decrypt with either key, so it can always use the key that is not under attack.

## When it applies

- You have an IND-CPA secure public-key scheme $\Pi$ and want CCA security without random oracles.
- You have a NIZK proof system for the NP language $L$ below. NIZK proofs for all of NP exist under standard assumptions, for example from trapdoor permutations (Blum, Feldman and Micali, 1988, and later work), so the paradigm gives CCA security from general assumptions.
- For IND-CCA2 the proof must be *simulation sound*: an adversary that has seen simulated proofs, even of false statements, still cannot make a valid proof of a new false statement (Sahai, 1999). Plain soundness gives IND-CCA1.
- The ciphertext must be checked with a proof anyway, for example in voting or in threshold decryption, where each party must show that its input is well formed.

## The template

The language is $L = \{(pk_1, pk_2, c_1, c_2) : \exists\, m, r_1, r_2 \text{ with } c_1 = \mathrm{Enc}(pk_1, m; r_1) \text{ and } c_2 = \mathrm{Enc}(pk_2, m; r_2)\}$.

```pseudo id=main
NY-KEYGEN(1^λ)
L1  (pk1, sk1) ← Gen(1^λ);  (pk2, sk2) ← Gen(1^λ)
L2  σ ← a uniform common reference string
L3  return pk = (pk1, pk2, σ) and sk = sk1        ▷ sk2 is thrown away

NY-ENCRYPT(pk, m)
L4  c1 ← Enc(pk1, m; r1);  c2 ← Enc(pk2, m; r2)  ▷ fresh r1, r2
L5  π ← P(σ, (pk1, pk2, c1, c2), witness (m, r1, r2))
L6  return (c1, c2, π)

NY-DECRYPT(sk, (c1, c2, π))
L7  if V(σ, (pk1, pk2, c1, c2), π) rejects then return ⊥
L8  return Dec(sk1, c1)
```

Line L8 may use either key. Honest decryption uses $sk_1$; the proof uses whichever key the reduction has.

### Why it works

**Theorem (Naor and Yung, 1990; Sahai, 1999).** If $\Pi$ is IND-CPA secure and $(\mathcal{P}, \mathcal{V})$ is an adaptively sound NIZK proof system for $L$, the scheme above is IND-CCA1 secure. If the proof system is also simulation sound, it is IND-CCA2 secure. The advantage of $\mathcal{A}$ is bounded by a sum of two IND-CPA advantages, two zero-knowledge advantages and the soundness or simulation-soundness error, with reductions that run in time $t$ plus $q_d$ decryptions. No term is multiplied by $q_d$, so the reductions are tight up to small constants.

*Proof sketch (IND-CCA2 version).* Use a sequence of games with challenge $(c_1^*, c_2^*, \pi^*)$.

1. *Game 0* is the real IND-CCA2 game for message $m_0$, with decryption under $sk_1$.
2. *Game 1.* Make $\sigma$ with the simulator and replace $\pi^*$ by a simulated proof. This changes the view by at most the zero-knowledge advantage.
3. *Game 2.* Replace $c_2^*$ by an encryption of $m_1$. The reduction to IND-CPA under $pk_2$ knows $sk_1$, so it answers every decryption query; it does not need the witness for $\pi^*$, which is simulated. The change is at most $\mathrm{Adv}^{\mathrm{ind\text{-}cpa}}$.
4. *Game 3.* Decrypt queries with $sk_2$ instead of $sk_1$. The answers differ only if $\mathcal{A}$ submits a query with an accepted proof of a false statement, where $c_1$ and $c_2$ hold different messages. In Game 2 the challenge statement itself is false, and $\mathcal{A}$ has seen a simulated proof of it; simulation soundness bounds the chance that it makes a new false statement with an accepted proof. For IND-CCA1 all queries come before $\pi^*$, so plain soundness suffices.
5. *Game 4.* Replace $c_1^*$ by an encryption of $m_1$, by IND-CPA under $pk_1$; the reduction now decrypts with $sk_2$.
6. Undo steps 4, 3 and 1 in reverse order, with the same arguments, to reach the real game for $m_1$. $\square$

The proof shows the role of the two keys: at every step the reduction holds the key that is not under attack, and the proof guarantees that the two keys decrypt every accepted ciphertext to the same message.

## Classic examples

- **Naor-Yung (1990)**, the original: any IND-CPA scheme and a general NIZK for NP, giving IND-CCA1.
- **Dolev, Dwork and Naor (1991, journal 2000)**: a [non-malleable](/non-malleability/) scheme with many encryptions selected by a one-time signature key, and a NIZK proof. It reached IND-CCA2 before Sahai's analysis of Naor-Yung.
- **Sahai (1999) and Lindell (2003)**: simulation-sound NIZK makes Naor-Yung IND-CCA2 secure; Lindell gets the same with a one-time signature over the ciphertext and a simpler, one-time simulation-sound proof.
- **[Cramer-Shoup](/cramer-shoup-cryptosystem/) (1998)**: the tag $v$ plays the role of a proof of validity that only the receiver can check. Cramer and Shoup later described this as a hash proof system, a designated-verifier form of the same idea, and it is far cheaper than a general NIZK.
- **Encrypt with a Fiat-Shamir proof.** [ElGamal](/elgamal-encryption/) with a [sigma protocol](/sigma-protocol/) proof made non-interactive by the [Fiat-Shamir heuristic](/fiat-shamir-heuristic/). Shoup and Gennaro (1998) used it for [threshold decryption](/threshold-cryptography/) (TDH1 and TDH2), and voting systems use it for ballots. This is a single encryption with a [proof of knowledge](/proof-of-knowledge/) of the plaintext, not double encryption, and its security proofs need the random oracle model.
- **Groth-Sahai proofs (2008)** in pairing groups give efficient NIZK proofs for statements about group elements, which make Naor-Yung practical in the standard model for schemes such as linear encryption.

## Variations

- **Proof of knowledge instead of double encryption.** If the proof extracts the plaintext (Rackoff and Simon, 1991, with a proof of knowledge), one encryption suffices, because the extractor plays the role of the second key.
- **Strong simulation soundness and labels.** Bind the proof to the whole ciphertext and to a label (context) by including them in the statement, so that the proof cannot be moved to another ciphertext.
- **One-time signatures.** Sign $(c_1, c_2, \pi)$ with a fresh one-time signature key and put the verification key in the statement (Dolev, Dwork and Naor; Lindell). This stops the adversary from reusing parts of the challenge.
- **Weaker goals.** Rerandomizable proofs give replayable CCA (RCCA) security at best, which some voting and mix-net protocols want, since ballots can then be rerandomized while staying valid.
- **Fiat-Shamir instantiations** replace the NIZK by a sigma protocol and a hash; they are efficient but are proved only in the random oracle model.

## Pitfalls

- **Plain soundness for IND-CCA2.** After seeing a simulated proof of the false challenge statement, an adversary may be able to make proofs of other false statements. Naor and Yung's proof covers only CCA1; IND-CCA2 needs simulation soundness or the one-time signature of Lindell.
- **Malleable proofs.** If anyone can turn $\pi$ into another valid proof $\pi'$ for the same statement, the attacker queries $(c_1^*, c_2^*, \pi')$, which differs from the challenge, and gets the message. Use proofs that are simulation sound in the strong sense, or sign the whole ciphertext with a one-time signature.
- **Weak Fiat-Shamir.** Hashing only the prover's first message, and not the statement (the public keys and ciphertexts), lets an attacker reuse a proof for a different statement. Bernhard, Pereira and Warinschi (2012) showed this kind of flaw in the Helios voting system. Always hash the full statement.
- **Decrypting before verifying.** Line L7 must run first, and a failed proof must give the same $\perp$ as every other failure. If the receiver decrypts $c_1$ before checking $\pi$ and reveals anything about the result, the scheme is no stronger than $\Pi$.
- **Cost.** With a general NIZK for NP the scheme is far too slow. Use it with proofs designed for the statement, such as sigma protocols or Groth-Sahai proofs, or use a direct construction such as Cramer-Shoup.

## Exercises

1. Let $\Pi$ be ElGamal in a group $G = \langle g \rangle$ of prime order $q$, with keys $h_1 = g^{x_1}$ and $h_2 = g^{x_2}$. Write the statement $(c_1, c_2) \in L$ for $c_1 = (g^{r_1}, m h_1^{r_1})$ and $c_2 = (g^{r_2}, m h_2^{r_2})$ as knowledge of $(r_1, r_2)$ satisfying three equations in $G$ that do not involve $m$, and give a sigma protocol for it. (Hint: divide the second components.)
2. Show that if the proof system lets anyone compute a second valid proof $\pi' \ne \pi$ for any statement with a valid proof $\pi$, then the Naor-Yung scheme is not IND-CCA2 secure, by giving an adversary that wins with advantage 1 using one decryption query.
3. In the proof sketch, explain why Game 3 needs the challenge proof to be simulated before the decryption key is switched, and why the order of steps 3 and 4 cannot be swapped.

## References
