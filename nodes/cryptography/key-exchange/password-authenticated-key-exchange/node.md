---
tag: EJCGN9
kind: problem
slug: password-authenticated-key-exchange
name: Password-authenticated key exchange
aliases:
- PAKE
- password-based authenticated key exchange
area: cryptography/key-exchange
level: advanced
summary: Two parties who share only a low-entropy password agree on a strong session key, so that an attacker can test at most one password guess for each active run and none offline.
prereqs: [authenticated-key-exchange, password-hashing]
see_also: [encrypted-key-exchange, secure-remote-password, spake2, cpace, j-pake, opaque, key-agreement-problem, man-in-the-middle-attack]
sources:
  - paper: "Steven M. Bellovin and Michael Merritt, Encrypted key exchange: password-based protocols secure against dictionary attacks, IEEE Symposium on Research in Security and Privacy 1992, pages 72 to 84"
    locator: the problem statement, the offline dictionary attack on naive protocols, and the partition attack
  - paper: doi:10.1007/3-540-45539-6_11
    title: Mihir Bellare, David Pointcheval and Phillip Rogaway, Authenticated key exchange secure against dictionary attacks, EUROCRYPT 2000, LNCS 1807, pages 139 to 155
    locator: the BPR model (oracles Send, Execute, Reveal, Corrupt and Test) and the definition of security as advantage at most the number of active sessions divided by the dictionary size, plus a negligible term
  - paper: "Ran Canetti, Shai Halevi, Jonathan Katz, Yehuda Lindell and Philip MacKenzie, Universally composable password-based key exchange, EUROCRYPT 2005, LNCS 3494"
    locator: the ideal functionality for PAKE with one TestPwd query for each session, and a construction in the common reference string model
  - paper: "Shai Halevi and Hugo Krawczyk, Public-key cryptography and password protocols, ACM CCS 1998"
    locator: the result that password protocols that resist offline guessing need public-key techniques
  - paper: "Jonathan Katz, Rafail Ostrovsky and Moti Yung, Efficient password-authenticated key exchange using human-memorable passwords, EUROCRYPT 2001"
    locator: the first efficient PAKE with a proof in the standard model, with a common reference string
  - paper: "Craig Gentry, Philip MacKenzie and Zulfikar Ramzan, A method for making password-based key exchange resilient to server compromise, CRYPTO 2006"
    locator: the UC functionality for augmented PAKE and a generic transform from a balanced PAKE
  - paper: "Stanislaw Jarecki, Hugo Krawczyk and Jiayu Xu, OPAQUE: an asymmetric PAKE protocol secure against pre-computation attacks, EUROCRYPT 2018, LNCS 10822, pages 456 to 486"
    locator: the strong aPAKE functionality, which forbids precomputation attacks before a server compromise
  - url: "https://github.com/cfrg/pake-selection"
    title: IRTF Crypto Forum Research Group, PAKE selection process, 2019 to 2020
    locator: the candidate list, the reviews, and the result that CPace is the balanced PAKE and OPAQUE the augmented PAKE that the CFRG recommends
  - paper: "Mathy Vanhoef and Eyal Ronen, Dragonblood: analyzing the Dragonfly handshake of WPA3 and EAP-pwd, IEEE Symposium on Security and Privacy 2020"
    locator: timing and cache side channels in the hash-to-group step of Dragonfly that leak information for offline password guessing
---

Password-authenticated key exchange (PAKE) asks two parties who share only a password, which may be short and easy to guess, to agree on a strong [session key](/session-key/) over a network that an attacker controls. A man in the middle can always guess a password and try it in one run, so the goal is that this is the best attack: each active run tests at most one guess, and a recorded transcript gives nothing that the attacker can test offline. The problem was stated by Bellovin and Merritt in 1992 with [encrypted key exchange](/encrypted-key-exchange/), and it is a special case of [authenticated key exchange](/authenticated-key-exchange/) in which the long-term secret has low entropy and there is no public-key infrastructure.

**Notation.** $\lambda$ is the security parameter. $C$ is a client and $S$ a server. $\mathcal{D}$ is the dictionary, the set from which the password $pw$ is drawn; $N = |\mathcal{D}|$. $\mathcal{A}$ is the adversary, $n_{\mathrm{act}}$ the number of sessions in which $\mathcal{A}$ sends its own messages, and $\mathrm{Adv}$ its advantage. $\mathrm{negl}(\lambda)$ is a negligible function. $G = \langle g \rangle$ is a cyclic group of prime order $q$.

## In plain words

Two people share a short password, such as a PIN of four digits. They want to use it to make a long, strong key over a network where a spy can read, change and send messages.

A spy can always guess the PIN, act as one person, and see if the run works. That costs one guess for each run, and the honest side can count failed runs and stop. The danger is a different attack: the spy records one run, goes away, and tests all 10 000 PINs on its own computer. Many simple designs allow this.

A PAKE stops the offline test. A recorded run must look the same for every possible password, so the spy learns nothing without a new live run for each guess.

## Definition

**Syntax.** A PAKE is a pair of interactive algorithms run by $C$ and $S$ on input $(1^\lambda, pw)$. Each run of a party (an instance) ends with accept and a key $k$ in $\{0,1\}^\lambda$, or with reject. In an honest run with equal passwords, both instances accept with the same key.

**The BPR model.** Bellare, Pointcheval and Rogaway (2000) give the adversary these oracles over many instances of many users: Send (deliver any message to an instance and get its reply), Execute (get the transcript of an honest run), Reveal (get the key of an instance), Corrupt (get a password) and Test (get the key of a fresh instance or a random string, by a hidden bit $b$). The password of each pair is uniform in $\mathcal{D}$. The protocol is secure if for every efficient $\mathcal{A}$

$$\mathrm{Adv}(\mathcal{A}) = 2\Pr[\mathcal{A} \text{ guesses } b] - 1 \le \frac{n_{\mathrm{act}}}{N} + \mathrm{negl}(\lambda).$$

Execute queries do not count in $n_{\mathrm{act}}$: passive attacks must give no useful information at all, and this is the formal form of resistance to offline dictionary attacks.

**The UC model.** Canetti, Halevi, Katz, Lindell and MacKenzie (2005) define an ideal functionality $\mathcal{F}_{\mathrm{pwKE}}$. Each party gives it a password; the ideal adversary may call TestPwd once for each session, with one guess, and learns only whether it is correct. If it is, the adversary chooses the key; if it is not, the key is random. Since the environment chooses the passwords, this model covers passwords that are not uniform, related passwords for different users, and a user who mistypes. A protocol that realizes $\mathcal{F}_{\mathrm{pwKE}}$ stays secure when it runs together with other protocols.

**Balanced and augmented.** In a balanced (symmetric) PAKE, both parties hold $pw$. In an augmented (asymmetric, verifier-based) PAKE, the server holds only a file $F(pw, \text{salt})$, and an attacker who steals the file must still do a dictionary search to log in as the client.

## Variants

- **Balanced PAKE.** Peers with equal knowledge of the password, for example two devices that pair with a code: [EKE](/encrypted-key-exchange/), [SPAKE2](/spake2/), [CPace](/cpace/) and [J-PAKE](/j-pake/).
- **Augmented PAKE (aPAKE).** Client and server, where the server stores a verifier: augmented EKE, [SRP](/secure-remote-password/), SPAKE2+ and [OPAQUE](/opaque/). After a server compromise, the attacker can always test guesses against the file offline; the protocol must force it to do that work and give nothing more.
- **Strong aPAKE.** Jarecki, Krawczyk and Xu (2018) also forbid precomputation: the attacker must not be able to compute a table of guesses before it steals the file. A public salt does not give this, since the attacker can ask for it; OPAQUE gets it with an oblivious PRF.
- **Implicit and explicit authentication.** In the basic form, a party with the wrong password gets a different key and only finds out later. Key confirmation messages give explicit authentication and also make forward security stronger.
- **Relaxed UC PAKE.** Abdalla and others (2020) define a weaker functionality, in which the attacker may test a guess after the session ends, and prove that SPAKE2 and similar protocols realize it.
- **Three-party, group and threshold PAKE.** Two clients that share passwords only with a server; a group with one password; or a password file split over several servers so that one compromised server gives no dictionary attack.
- **Quantum-annoying PAKE.** A PAKE in which a quantum attacker must solve one discrete logarithm for each password guess.

## Examples

**Offline attack on a MAC keyed by the password.** Run unauthenticated [Diffie-Hellman](/diffie-hellman/) and let each side send $\mathrm{HMAC}(H(pw), \text{its share})$. A passive attacker who records $X$ and the tag $t = \mathrm{HMAC}(H(pw), X)$ tests each $pw' \in \mathcal{D}$ by computing $\mathrm{HMAC}(H(pw'), X)$. In the code on this page, the dictionary has 2003 words, and one recorded run of the client with password `sunshine` gives back exactly that word, with no interaction.

**Offline attack after one active run.** Use the generator $g_{pw} = g^{w}$, with $w = H(pw)$, and send $X = g_{pw}^x$; the client then sends a confirmation tag under $K = Y^x$. An attacker acts as the server once: it sends $Y = g^y$ for a $y$ that it knows, without a password, and receives the tag. Offline, it tests each guess $w'$ by computing $K' = X^{y/w'}$; if $w' = w$, then $K' = g^{w x y / w} = g^{xy} = Y^x$, and the tag verifies. In the code, one such run against a client with password `pass1234` gives back that password from the same 2003-word dictionary. The protocol thus allows one active run to test all guesses, which a PAKE must not allow.

**Partition attack.** If an encrypted share is a number modulo $p$ that was padded to a fixed length, a wrong password often decrypts it to a value at or above $p$, which removes that password from the list. Each recorded run removes a fixed part of the dictionary; see [encrypted key exchange](/encrypted-key-exchange/).

**A secure protocol.** In [SPAKE2](/spake2/), the client sends $X = g^x M^{w}$ and the server $Y = g^y N^{w}$. For each guess $w'$, the value $X / M^{w'}$ is a valid share $g^{x'}$ for some $x'$, so a transcript is consistent with every password, and an attacker who wants to test $w'$ must compute $g^{x' y'}$, a Diffie-Hellman value.

The attack code is for study only, it is not constant time, and it runs only on a toy 128-bit group against local simulated parties.

## Known algorithms

| Protocol | Year | Type | Proof setting |
|---|---|---|---|
| [EKE](/encrypted-key-exchange/) (EKE2 form) | 1992, 2000 | balanced | ideal cipher and random oracle |
| Augmented EKE | 1993 | augmented | none in the original paper |
| SPEKE | 1996 | balanced | later analyses in the random oracle model |
| [SRP](/secure-remote-password/) | 1998 | augmented | no full proof |
| PAK, PPK | 2000 | balanced and augmented | random oracle |
| KOY | 2001 | balanced | standard model with a reference string |
| [SPAKE2](/spake2/) | 2005 | balanced | random oracle (relaxed UC) |
| [J-PAKE](/j-pake/) | 2008 | balanced | random oracle and algebraic adversaries |
| Dragonfly (SAE in WPA3) | 2008 | balanced | random oracle, with side channel issues |
| [CPace](/cpace/) | 2019 | balanced | UC, random oracle |
| [OPAQUE](/opaque/) | 2018 | strong augmented | UC, random oracle |

In 2019 and 2020 the IRTF Crypto Forum Research Group ran a selection process with eight candidates. It recommended CPace as the balanced PAKE and OPAQUE as the augmented PAKE.

## Bounds

**The online bound is tight.** An adversary that picks $pw' \in \mathcal{D}$, runs the honest protocol with $pw'$ against a real party, and checks if it accepts (or if a later message decrypts) wins with probability $1/N$ for each run. So no PAKE can have advantage below about $n_{\mathrm{act}}/N$, and the BPR bound $n_{\mathrm{act}}/N + \mathrm{negl}(\lambda)$ is the best possible. With $N = 10^4$ and a limit of 10 failed attempts, the attacker wins with probability at most about $10^{-3}$.

**Server compromise.** For an augmented PAKE, the server file lets the attacker run the client side with any guess against itself, so a full dictionary search of $N$ steps after compromise is always possible. A strong aPAKE makes this search start only after the compromise.

**Public-key techniques are needed.** A PAKE solves [key agreement](/key-agreement-problem/) when the password space has one element, so it cannot be built from one-way functions alone in a black-box way. Halevi and Krawczyk (1998) also showed that password protocols that resist offline guessing need public-key cryptography.

**Cost.** The common protocols cost two or three messages and a small constant number of exponentiations in $G$ for each party: two for SPAKE2 and CPace, about 14 for J-PAKE, because of its zero-knowledge proofs.

## Reductions

- **PAKE implies key agreement.** Fix the password; a passive adversary must have no advantage, which is the eavesdropper experiment of key agreement.
- **Balanced to augmented.** The method of Gentry, MacKenzie and Ramzan (2006) turns a balanced UC PAKE into an augmented one: the server stores a hash of the password and a public key, and the client proves after the PAKE that it knows the matching private key, which it decrypts with the password.
- **OPRF plus AKE gives strong aPAKE.** [OPAQUE](/opaque/) composes an oblivious PRF, which turns the password into a strong key without showing it to the server, with an AKE that resists key-compromise impersonation.
- **High-entropy case.** A PAKE run with a uniform 256-bit key in place of a password is a symmetric-key AKE; the converse fails, because symmetric AKE protocols such as a MAC over the transcript allow the offline attack in the first example.

## Applications

- TLS with SRP (RFC 5054), and SRP in some password managers and in Apple iCloud Keychain recovery.
- WPA3 personal Wi-Fi uses Simultaneous Authentication of Equals (SAE), the Dragonfly PAKE; side channel attacks on its first version (Dragonblood, 2019) led to a hash-to-curve fix.
- Thread uses EC-J-PAKE to admit a new device with a commissioning code, and Matter uses SPAKE2+ with the setup code of a device.
- Magic Wormhole uses SPAKE2 to send files between two computers with a short code.
- Kerberos has a pre-authentication mechanism based on SPAKE that stops offline guessing of the user password from a captured exchange.
- End-to-end encrypted backups and password logins that never send the password to the server use OPAQUE.

## References

Bellovin and Merritt (1992) state the problem and the dictionary attacks. Bellare, Pointcheval and Rogaway (2000) give the game-based model, and Canetti, Halevi, Katz, Lindell and MacKenzie (2005) the universally composable one. Gentry, MacKenzie and Ramzan (2006) and Jarecki, Krawczyk and Xu (2018) define augmented and strong augmented security. The CFRG selection pages describe the standard choices.
