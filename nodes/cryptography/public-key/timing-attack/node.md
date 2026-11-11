---
tag: M5SV5X
kind: concept
slug: timing-attack
name: Timing attack
aliases:
- side-channel timing attack
area: cryptography/public-key
level: advanced
summary: The time a secret operation takes is a function of the secret. Measure it on many inputs and the key comes out, even when the algorithm itself is sound.
history:
  year: 1996
  people: [Paul C. Kocher, David Brumley, Dan Boneh, Daniel J. Bernstein]
  note: Kocher opened the field in 1996 with a timing attack on modular exponentiation. Brumley and Boneh made it remote in 2003, and the cache work of 2005 and 2006 made it general.
prereqs: [modular-exponentiation]
see_also: [rsa-blinding, montgomery-multiplication, binary-exponentiation, rsa-fault-attack, padding-oracle-attack, rsa-cryptosystem, diffie-hellman]
sources:
  - paper: "Paul C. Kocher, Timing attacks on implementations of Diffie-Hellman, RSA, DSS, and other systems, CRYPTO 1996, LNCS 1109, pages 104 to 113"
    locator: Sections 2 and 3 (the attack on square and multiply, the bit by bit recovery with a statistical test, and the countermeasures)
  - url: "https://www.usenix.org/legacy/events/sec03/tech/brumley.html"
    title: David Brumley and Dan Boneh, Remote timing attacks are practical, USENIX Security Symposium 2003
    locator: Sections 3 and 4 (the Montgomery extra reductions and the multiplication routine switch, and the factor recovery over a network)
  - url: "https://cr.yp.to/antiforgery/cachetiming-20050414.pdf"
    title: Daniel J. Bernstein, Cache-timing attacks on AES, 2005
    locator: Sections 2 and 4 (the table lookup leak, the correlation attack, and why "load from a secret index" is not constant time)
  - paper: "Dag Arne Osvik, Adi Shamir and Eran Tromer, Cache attacks and countermeasures, the case of AES, CT-RSA 2006, LNCS 3860, pages 1 to 20"
    locator: Sections 3 and 4 (Evict+Time and Prime+Probe, and the number of samples each needs)
  - url: "http://www.daemonology.net/papers/cachemissing.pdf"
    title: Colin Percival, Cache missing for fun and profit, BSDCan 2005
    locator: Section 5 (the exponent window table of OpenSSL RSA read out through a shared cache on a hyperthreaded core)
  - url: "https://www.usenix.org/conference/usenixsecurity14/technical-sessions/presentation/yarom"
    title: Yuval Yarom and Katrina Falkner, FLUSH+RELOAD, a high resolution, low noise, L3 cache side-channel attack, USENIX Security Symposium 2014
    locator: Sections 4 and 5 (the last level cache channel, and the recovery of the exponent of GnuPG RSA)
---

A timing attack reads a secret out of the time that a computation takes. The algorithm can be perfect on paper: if the implementation does more work for a 1 bit of the key than for a 0 bit, or if the work depends on a value the attacker chooses, then the running time is a function that leaks. Kocher (1996) broke [modular exponentiation](/modular-exponentiation/) this way, and Brumley and Boneh (2003) did it over a network against a TLS server. The defences are to make the work independent of the secret, by a [Montgomery ladder](/binary-exponentiation/) or constant-time code, and to make it independent of the input, by [blinding](/rsa-blinding/). The code of this page measures no wall clock; it counts the operations exactly, which is the cost model an attacker is trying to estimate.

## In plain words

A safe that takes longer to reject a wrong digit than a right one can be opened one digit at a time. Software does this without meaning to.

A program that uses a private key often takes a short cut: skip a step when a key bit is zero, stop early when a check fails, or read a table at a place that depends on the data. Each short cut saves work, and the saving shows up from outside as a shorter run. An attacker who can run the program again and again, and see roughly how long each run took, adds up those small savings and gets the key.

The repair is to do the same work every time, whatever the key and the data, and to mix the input with a random value, so that a repeated question is never the same question twice.

## The idea

Model the device as a function the attacker can call. The device holds a secret $d$. On input $c$ it returns the answer and, without meaning to, a cost

$$T(c) = f(c, d) + \text{noise} .$$

The attack is to invert $f$ in the first argument, piece by piece. Three things decide whether this is possible.

1. **Is the cost a function of the secret at all?** If the code takes the same path for every key, there is nothing to recover.
2. **How fine is the measurement?** One number for each run (a stopwatch) is weak. A number for each *step* of the run, which a power trace or a cache probe can give, is strong.
3. **Can the attacker repeat a query?** Noise falls as $1/\sqrt{k}$ over $k$ repeats of the same query, so a stable leak of a fraction of a cycle is enough, given time. This is why [blinding](/rsa-blinding/) is the first countermeasure: it makes a repeat impossible.

### The leak of square and multiply

Left to right [square and multiply](/modular-exponentiation/) computes $c^d \bmod N$ with one squaring for every bit of $d$ and one extra multiplication for every 1 bit:

$$\text{cost of iteration } i = 1 + d_i .$$

At the coarse level, the total cost is $k + \mathrm{wt}(d)$ for a $k$-bit exponent, so a single stopwatch reading gives the Hamming weight of the key, which is a real loss but not a break. At the fine level, where the attacker sees the cost of each iteration, the list of costs *is* the key: a 2 is a 1 bit and a 1 is a 0 bit. For $d = 157 = 10011101_2$ the costs are

$$2,\ 1,\ 1,\ 2,\ 2,\ 2,\ 1,\ 2 .$$

A power trace of a smart card shows exactly this pattern, which is why it is also called simple power analysis. A window method hides less than it seems: the table entry that is read is chosen by a group of exponent bits, so the *address* carries the secret even when the *count* does not. That is what Percival (2005) and Flush+Reload (2014) read out of a shared cache.

### The leak Kocher used, and the leak over a network

Kocher's attack does not need per-iteration costs. It needs only that the cost of one step depends on the data in a way the attacker can predict. Recover the bits of $d$ from the top. Suppose $d_{k-1}, \ldots, d_{i+1}$ are known. For each of many inputs $c$, simulate the device up to bit $i$ under the guess $d_i = 1$, and predict whether the next operation is an expensive one. Split the inputs into the predicted-expensive set and the predicted-cheap set, and compare the mean measured cost of the two sets. If the guess is right, the prediction is right and the two means differ; if the guess is wrong, the split is unrelated to the device and the means agree. The unknown lower bits act as noise with the same distribution on both sides, so they do not bias the test.

For that to work, some operation must cost more for some data. [Montgomery multiplication](/montgomery-multiplication/) supplies one for free. Its last step holds a value below $2n$ and subtracts $n$ when it must:

$$u = \frac{ab + mn}{R}, \qquad \text{if } u \ge n \text{ then } u \leftarrow u - n .$$

Whether that extra reduction happens depends on $a$ and $b$, so it depends on the ciphertext. Brumley and Boneh (2003) used this, together with the switch between the schoolbook and the Karatsuba multiplication routine at a size boundary, against an OpenSSL server. As a chosen ciphertext $c$ approaches a prime factor $p$ from below, the number of extra reductions in the CRT half modulo $p$ rises, and at $c = p$ it drops; the position of that drop gives the bits of $p$ from the top. They recovered a factor of a 1024-bit key from a machine on the same network, and the answer was the OpenSSL advisory of 17 March 2003, which switched [blinding](/rsa-blinding/) on for every key.

### The fixes, in order of strength

- **Remove the secret from the control flow.** No branch on a secret bit, no loop whose length depends on a secret, no early return. A [Montgomery ladder](/binary-exponentiation/) does one squaring and one multiplication for every exponent bit, in both branches, so its cost list is constant.
- **Remove the secret from the addresses.** No table index and no memory offset derived from a secret, because the cache turns an address into a time. Bernstein (2005) showed this for the AES S-box tables, where "constant time" code with lookups was not.
- **Blind the input.** [RSA blinding](/rsa-blinding/) makes every run use a fresh random number, so a repeated query is no longer a repeated measurement and averaging gets nothing.
- **Make the error path uniform.** One error value, computed with the same work. A fast rejection is an oracle; see [padding oracle attack](/padding-oracle-attack/) and Lucky Thirteen.
- **Check the result, do not trust the count.** A constant operation count is necessary and not sufficient. On real hardware a multiplication can be faster for small operands, a division can be data dependent, and a compiler can turn a careful select back into a branch. Measure the final binary, and prefer primitives that were designed for this, such as [X25519](/x25519/).

## Examples

**A toy device.** The code of this page holds a toy RSA key with a 127 binary digit modulus $N = pq$ for $p = 18446744073709551557$ and $q = 9223372036854775783$, and the private exponent $d$ of 126 binary digits with 56 one bits. Nothing reads a clock; the device reports the number of modular multiplications it did for each exponent bit.

| what the attacker sees | what it gives |
|---|---|
| the total, 182 multiplications, with 126 squarings | the Hamming weight of $d$, which is $182 - 126 = 56$ |
| the per-bit list, which starts $2, 2, 1, 1, 2, 2, 1, 1, \ldots$ | the bits of $d$, which start $1, 1, 0, 0, 1, 1, 0, 0, \ldots$ |
| the per-bit list of the Montgomery ladder, $2, 2, 2, \ldots$ | the length of $d$, which is public |

The test file recovers the whole private exponent from the per-bit list and checks it against the key, and it checks that the ladder gives two identical lists for two different exponents of the same length.

**The extra reduction leak, and blinding.** The same key, now with Montgomery multiplication and with only the extra reductions counted. The private operation costs 183 Montgomery multiplications. For the chosen ciphertext $c_1 = \texttt{0x1234567890abcdef}$, 21 of them need the extra reduction; for $c_2 = \texttt{0x0fedcba098765432}$, 36 do. Those two numbers never change, so an attacker who can repeat a query can measure a 15 operation gap through any amount of noise. With blinding switched on and 30 fresh random blinds for each ciphertext, the means are 29.3 and 27.9 with a spread of 5.9, so the gap is lost inside one standard deviation and no amount of repeating brings it back.

**Lucky Thirteen, 2013.** In TLS with CBC and MAC-then-encrypt, the number of hash compression calls in the MAC check depends on how many octets the padding claimed. The difference is a few microseconds, and it was enough to rebuild the padding oracle that the protocol had tried to close. The story is on the [padding oracle attack](/padding-oracle-attack/) page.

**Nonce length leaks in signatures, 2019 and 2020.** The Minerva and TPM-Fail work timed ECDSA signing and saw the bit length of the random nonce, because the scalar multiplication ran one iteration for each bit of it. A few hundred signatures with slightly short nonces give the private key through a lattice attack. The algorithm was fine; the loop bound was the leak.

## Where it is used

Timing analysis is now a standard part of cryptographic engineering, on both sides.

- **As an attack.** Against RSA and [Diffie-Hellman](/diffie-hellman/) exponentiation, against AES table lookups, against the comparison of MAC tags with `memcmp`, against the branch in a modular reduction, against lattice schemes whose rejection sampling loops on secret data, and against anything that decompresses, caches or compresses secret data.
- **As a design rule.** Every modern primitive specification has a constant-time note, and the libraries carry constant-time backends: no secret branches, no secret indexes, arithmetic with masks instead of `if`, and a fixed number of rounds. [X25519](/x25519/) was designed so that the natural implementation is already constant time, and the ML-KEM and ML-DSA specifications say which comparisons must be uniform.
- **As a test.** Tools measure the distribution of the run time of a binary on two input classes and report whether they differ, which turns the rule above into a check that runs in a build. The cost model of this page is the same idea with the noise removed: count the operations, and look at whether the count moves with the secret.
- **In the security model.** All of this sits outside the proofs. A proof of [IND-CCA](/ind-cca-security/) security treats the decryption as a black box that returns a value, while a timing attack returns a value *and* a number. Side channel resistance is an implementation property, and it has to be argued separately from the scheme.

**The code of this page is for study only.** It is not constant time, it is not a secure implementation, and the attacks in it run on a toy key against a local simulated device.

## References
