---
tag: 91890R
kind: problem
slug: password-hashing
name: Password hashing
aliases:
- secure password storage
area: cryptography/hash-functions
level: core
summary: Store password verifiers so offline guessing is slow even after a breach.
prereqs: [cryptographic-hash-function]
see_also: [pbkdf2, bcrypt, scrypt, argon2, memory-hard-function, rainbow-table, hmac, password-authenticated-key-exchange]
sources:
  - url: "https://pages.nist.gov/800-63-4/sp800-63b.html"
    title: NIST SP 800-63B-4, Digital Identity Guidelines, Authentication and Authenticator Management, 2025 (doi 10.6028/NIST.SP.800-63B-4)
    locator: Section 3.1.1.2 (password verifiers), the paragraphs on salted hashing, the salt of at least 32 bits, the cost factor and the secret key held only by the verifier
  - url: "https://pages.nist.gov/800-63-3/sp800-63b.html"
    title: NIST SP 800-63B, Digital Identity Guidelines, Authentication and Lifecycle Management, June 2017, includes updates as of 03-02-2020
    locator: Section 5.1.1.2 (memorized secret verifiers), PBKDF2 and Balloon as examples, at least 10,000 iterations, the secret salt
  - url: "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"
    title: OWASP Cheat Sheet Series, Password Storage Cheat Sheet
    locator: the introduction list of minimum settings and the sections Argon2id, scrypt, bcrypt, PBKDF2 and Peppering
  - url: "https://www.password-hashing.net/"
    title: Password Hashing Competition
    locator: the PHC section (2013 to 2015, 24 submissions by March 31 2014, 9 finalists in December 2014, Argon2 the winner in July 2015, special recognition for Catena, Lyra2, Makwa and yescrypt)
  - paper: "Robert Morris and Ken Thompson, Password security: a case history, Communications of the ACM 22(11), 1979, pages 594 to 597"
    locator: the salted and iterated DES-based crypt of Unix
  - paper: "Mihir Bellare, Thomas Ristenpart and Stefano Tessaro, Multi-instance security and its application to password-based cryptography, CRYPTO 2012, LNCS 7417"
    locator: the analysis of salted and iterated password-based key derivation in the random oracle model
---

Password hashing is the problem of storing, for each user, a value that lets a server check a typed password but makes the password expensive to recover if the stored values leak. A good scheme forces an attacker who has the database to pay a fixed, tunable cost for every guess and for every user, and it makes precomputed tables useless. The standard answer is a salted, deliberately slow, and preferably memory-hard function such as [PBKDF2](/pbkdf2/), [bcrypt](/bcrypt/), [scrypt](/scrypt/) or [Argon2](/argon2/).

**Notation.** $p$ a password, $s$ a salt, $\theta$ the cost parameters, $F_\theta(s, p)$ the password hash function, $y$ the stored value. $H$ a [cryptographic hash function](/cryptographic-hash-function/). $D$ the distribution of passwords, and $q$ the number of guesses the attacker can afford. The security analyses cited here are in the random oracle model (ROM), with $H$ an ideal function.

## In plain words

A server must remember enough about your password to check it, but it should not keep the password. If it keeps a fast hash such as SHA-256 of the password, a thief who copies the database can try billions of guesses per second on a graphics card, and most human passwords fall in hours.

So the server does three things. It mixes a random value, the salt, into each password, so that the thief must attack each user alone and cannot use a table computed in advance. It uses a function that is slow on purpose, so each guess costs the thief as much as one login costs the server. And it makes the function need much memory, so that special hardware cannot run many guesses in parallel cheaply.

## Definition

**Setup.** At registration the server picks a fresh random salt $s$ and stores the record $(s, \theta, y)$ with $y = F_\theta(s, p)$. At login it receives $p'$, recomputes $F_\theta(s, p')$, and compares it with $y$ in constant time.

**Requirements.**

1. *Correctness.* The right password is always accepted, and a wrong one is accepted only with negligible probability (a collision of $F$).
2. *Cost per guess.* An attacker who holds the record must spend about the cost of one evaluation of $F_\theta$ for each guess. No shortcut computes $F_\theta$ on many passwords much faster than one by one.
3. *Cost per user.* Distinct users have distinct salts, so one evaluation tests a guess against one record only. Tables computed before the leak, such as [rainbow tables](/rainbow-table/), do not help.
4. *Cost on the attacker's hardware.* The cost that counts is the cost for the attacker on GPUs, FPGAs or ASICs, not the time on the server. A function whose evaluation needs much memory raises the chip area times time of each guess. This is the aim of a [memory-hard function](/memory-hard-function/).
5. *Tunable cost.* $\theta$ can grow over time, and the record stores $\theta$ so that old records stay valid.

**Attacker model.** The attacker gets the records after a breach. This is an offline attack: no rate limit applies, and the attacker can guess in the order of the most likely passwords of $D$. If the scheme meets the requirements, the attacker who can pay for $q$ evaluations of $F$ recovers a given user's password with probability at most about the total probability of the $q$ most likely passwords under $D$. No scheme can do better: weak passwords stay weak, and the scheme only multiplies the cost of each guess.

**Salt and pepper.** A salt is public and unique per record; NIST SP 800-63B-4 requires at least 32 bits. A pepper is a secret key shared by all records and kept apart from the database, for example in a hardware security module. NIST calls it an additional keyed hashing or encryption step with a secret key. A pepper helps only when the database leaks without the key; it cannot be changed without asking every user for the password again.

## Variants

- **Password-based key derivation.** The output is a key for encryption, for example of a disk or a password vault, instead of a verifier. The same functions are used, and the output length is chosen by the caller.
- **Server relief.** The client runs the expensive function and the server stores only a fast hash of its output, so a busy server is not overloaded.
- **Password-authenticated key exchange.** [PAKE](/password-authenticated-key-exchange/) protocols such as [SRP](/secure-remote-password/) avoid sending the password to the server at all; the stored verifier still needs a slow salted function.
- **Hashing with delegation.** Makwa, a PHC finalist, lets a weak client hand the heavy work to an untrusted helper.

## Examples

**Plain hash, salted fast hash, and slow hash.** Take an 8-letter lowercase password, so there are $26^8 \approx 2.1 \times 10^{11}$ candidates. Assume an attacker who computes $10^{10}$ SHA-256 compressions per second (a round number for illustration, not a measurement).

| stored value | compressions per guess | time to try all $26^8$ | precomputation possible |
|---|---|---|---|
| $H(p)$ | 1 | about 21 seconds | yes, for all users at once |
| $H(s \| p)$ | 1 | about 21 seconds per user | no |
| PBKDF2-HMAC-SHA-256, 600,000 iterations | about $1.2 \times 10^{6}$ | about 290 days per user | no |

The salt removes the gain from precomputation and from attacking many users at once. Only the iteration count raises the cost of one guess, and it raises it by the same factor for the server.

**Comparison of the main schemes.**

| scheme | year | core primitive | memory hard | cost parameters | standard or status | OWASP minimum |
|---|---|---|---|---|---|---|
| [PBKDF2](/pbkdf2/) | 2000 | iterated [HMAC](/hmac/) | no | iteration count $c$ | RFC 8018, NIST SP 800-132 | 600,000 iterations with HMAC-SHA-256 |
| [bcrypt](/bcrypt/) | 1999 | Eksblowfish key setup | no, needs 4 KB of fast memory | cost $2^{\text{cost}}$ key setups | de facto, OpenBSD | cost 10, passwords of at most 72 bytes |
| [scrypt](/scrypt/) | 2009 | ROMix over Salsa20/8 | yes, data dependent | $N$, $r$, $p$ | RFC 7914 | $N = 2^{17}$, $r = 8$, $p = 1$ (128 MiB) |
| [Argon2id](/argon2/) | 2015 | BLAKE2b-based compression | yes, hybrid | memory $m$, passes $t$, lanes $p$ | RFC 9106, PHC winner | $m$ = 19 MiB, $t = 2$, $p = 1$ |

The OWASP column is from the Password Storage Cheat Sheet. OWASP lists Argon2id first, scrypt when Argon2id is not available, bcrypt for legacy systems, and PBKDF2 when FIPS 140 compliance is needed.

## Known algorithms

- **Unix crypt** (Morris and Thompson, 1979): 25 iterations of a modified DES with a 12-bit salt. It introduced salting and deliberate slowness. Its 8-character limit and small cost are obsolete.
- **[PBKDF2](/pbkdf2/)**: iterates HMAC $c$ times. Simple and approved by NIST, but cheap on GPUs and ASICs, because it needs almost no memory.
- **[bcrypt](/bcrypt/)**: runs the Blowfish key schedule $2^{\text{cost}}$ times. Its 4 KB of S-boxes that change all the time slowed early GPUs.
- **[scrypt](/scrypt/)**: fills $N$ blocks of memory and reads them in an order that depends on the data. The first widely used memory-hard function.
- **[Argon2](/argon2/)**: the winner of the Password Hashing Competition. Argon2d uses data-dependent addressing, Argon2i data-independent addressing, and Argon2id both. RFC 9106 recommends Argon2id.
- **Other PHC finalists and later designs**: Catena, Lyra2, Makwa and yescrypt got special recognition in the PHC. Balloon hashing (Boneh, Corrigan-Gibbs and Schechter, Asiacrypt 2016) was named by NIST SP 800-63B (2017) as an example of a suitable function.

## Bounds

- **Upper bound on what any scheme can give.** An attacker who can pay for $q$ evaluations succeeds with probability at least the total probability of the $q$ most likely passwords. A scheme can only make $q$ smaller for a given budget.
- **Iterated hashing in the ROM.** Bellare, Ristenpart and Tessaro (CRYPTO 2012) analyze salted iterated key derivation in the random oracle model and show that, with distinct salts, breaking $m$ users costs about $m$ times as much as breaking one, and that $c$ iterations multiply the work by about $c$. The bounds are in terms of oracle queries, so they say nothing about memory.
- **Memory hardness.** The cost of a guess on custom hardware is better measured by cumulative memory complexity, the sum of memory used over time. Lower bounds for scrypt and for data-independent functions come from pebbling arguments; see [memory-hard function](/memory-hard-function/).

## Reductions

- Recovering the password from a record is a [preimage search](/preimage-finding/) over a small, non-uniform domain. Preimage resistance of $H$ is not enough because the domain is small; only the cost per evaluation and the salt help.
- Without a salt, the attack becomes a [time-memory tradeoff](/time-memory-tradeoff/) problem: one table built once breaks every record. The salt multiplies the table size by the number of salts.
- A password hash with a pepper is a keyed function. If the pepper is secret, the records are outputs of a pseudorandom function and leak nothing useful.

## Applications

Login systems of web services and operating systems store password records. Disk encryption tools derive keys from passphrases: LUKS2 in Linux uses Argon2 by default, and WPA2 personal mode derives its key with PBKDF2-HMAC-SHA-1 with 4096 iterations. Password managers, encrypted backups and cryptocurrency wallets use the same functions to turn a passphrase into a key.

## References
