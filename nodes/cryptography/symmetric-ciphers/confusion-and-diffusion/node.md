---
tag: WFB1Z8
kind: concept
slug: confusion-and-diffusion
name: Confusion and diffusion
aliases:
- Shannon's properties of mixing
area: cryptography/symmetric-ciphers
level: intro
summary: Shannon's two aims for a cipher. Confusion makes the key to ciphertext relation complex (S-boxes); diffusion spreads each input bit over the whole output (the linear layer).
prereqs: [block-cipher]
see_also: [s-box, substitution-permutation-network, feistel-network, avalanche-effect, advanced-encryption-standard, data-encryption-standard, boolean-function, perfect-secrecy]
sources:
  - paper: doi:10.1002/j.1538-7305.1949.tb00928.x
    title: Claude E. Shannon, Communication theory of secrecy systems, Bell System Technical Journal 28(4), 1949
    locator: the sections on statistical methods, diffusion and confusion, and mixing transformations
  - paper: "A. F. Webster and Stafford E. Tavares, On the design of S-boxes, Advances in Cryptology, CRYPTO 1985, LNCS 218, Springer, 1986"
    locator: the strict avalanche criterion and the bit independence criterion
  - paper: "Horst Feistel, Cryptography and computer privacy, Scientific American 228(5), May 1973"
    locator: the dependence of each output bit on all input bits in a product cipher (the avalanche effect)
  - book: isbn:9783540425809
    title: Joan Daemen and Vincent Rijmen, The Design of Rijndael, Springer, 2002
    locator: Chapter 9, the wide trail strategy (branch number and active S-boxes)
---

Confusion and diffusion are the two properties that Claude Shannon named in 1949 as the aims of a practical cipher. *Confusion* makes the relation between the key and the ciphertext so complex that simple statistics of the ciphertext say little about the key. *Diffusion* spreads the influence of each plaintext symbol over many ciphertext symbols, so that the redundancy of the plaintext is lost in long-range statistics. In a modern [block cipher](/block-cipher/), the [S-boxes](/s-box/) give confusion and the linear layer gives diffusion, and the two are repeated over many rounds. The *avalanche effect* and the *strict avalanche criterion* turn diffusion into a property that can be measured.

## In plain words

A cipher has two jobs besides being reversible. First, it must hide how the key shapes the output. If each output bit were a simple sum of key bits and message bits, an attacker could solve for the key with school algebra. So the cipher mixes them through scrambled lookup tables. This is confusion.

Second, it must hide patterns in the message. If one letter of the message changes only one letter of the output, an attacker can count letters, as in old puzzles. So the cipher spreads each message bit over the whole output. This is diffusion.

One round of a cipher does a little of both. Many rounds together do it fully. A simple test: change one input bit and count the output bits that change. A good cipher changes about half of them.

## The idea

**Notation.** $E_K$ is a block cipher with $n$-bit blocks and key $K$, $\mathrm{wt}(z)$ is the number of 1 bits of $z$, and $e_i$ is the block with a single 1 in position $i$.

**Shannon's view.** Shannon modeled a cipher as a "mixing transformation". A product of simple steps, a substitution and then a transposition, repeated, can mix well even when each step is weak. This is the plan of every [substitution-permutation network](/substitution-permutation-network/) and every [Feistel network](/feistel-network/).

**The mapping to cipher parts.**

| part | gives | why |
|---|---|---|
| S-box layer | confusion | the only nonlinear step; it makes each output bit a high-degree function of key and input bits |
| linear layer (bit permutation, MixColumns) | diffusion | it sends the output of each S-box to many S-boxes of the next round |
| key addition | key dependence | it puts the key between the layers, so no layer can be undone without it |
| many rounds | both | each round raises the degree and widens the dependence |

Neither part is enough alone. Without S-boxes, the cipher is affine over GF(2), and $n + 1$ chosen plaintexts give its full description. Without the linear layer, each S-box acts on its own bits only, and the cipher splits into small independent ciphers that can be attacked one at a time.

**Avalanche.** For a fixed key, flipping input bit $i$ gives the output difference $E_K(x) \oplus E_K(x \oplus e_i)$. The cipher shows the *avalanche effect* if the expected weight of this difference is close to $n/2$ for each $i$, over random $x$ and $K$. This is what a random permutation gives: $E_K(x \oplus e_i)$ is then uniform on the other $2^n - 1$ values, and its expected distance to $E_K(x)$ is $n\,2^{n-1}/(2^n - 1) \approx n/2$.

**The strict avalanche criterion (SAC).** Webster and Tavares (1985) asked more: for each input bit $i$ and each output bit $j$, output bit $j$ must flip with probability exactly $\frac{1}{2}$ when input bit $i$ flips, over uniform $x$. For an S-box $S$ this is the matrix

$$P[i][j] = \Pr_x\bigl[\text{bit } j \text{ of } S(x) \oplus S(x \oplus e_i) = 1\bigr],$$

and SAC holds when each entry is $\frac{1}{2}$. Their *bit independence criterion* (BIC) also asks that two output bits flip independently of each other.

**Diffusion by branch number.** For a linear layer $\theta$ on $m$ words, the branch number is $\min_{a \ne 0} (w(a) + w(\theta(a)))$, where $w$ counts nonzero words. It is at most $m + 1$. The MixColumns map of AES reaches the maximum 5 for $m = 4$. A high branch number forces many active S-boxes in any differential or linear trail. This turns diffusion into a proof of resistance to differential and linear cryptanalysis: the wide trail strategy of Daemen and Rijmen.

**Measuring avalanche.** The listing below estimates the mean number of changed output bits. The code is for study only, is not constant time, and must not be used to protect real data; for real data use a FIPS 140 validated module or libsodium.

```python
import random

def avalanche(encrypt, n, k, trials=1000, seed=1):
    """Mean number of the n output bits that change when one random input bit flips."""
    rng = random.Random(seed)
    total = 0
    for _ in range(trials):
        key, x = rng.getrandbits(k), rng.getrandbits(n)
        flipped = x ^ (1 << rng.randrange(n))
        total += bin(encrypt(key, x) ^ encrypt(key, flipped)).count("1")
    return total / trials
```

## Examples

**Avalanche by number of rounds.** The table gives the mean number of changed output bits for the ciphers of this site, with random keys. Here "AES, $r$ rounds" means the first $r$ rounds of AES-128 with the last of them in the final form, without MixColumns, so it contains $r - 1$ MixColumns steps.

| rounds | 1 | 2 | 3 | 4 | 5 | full |
|---|---|---|---|---|---|---|
| AES (of 128 bits) | 4.02 | 16.69 | 63.88 | 64.00 | 64.67 | 64.39 (10 rounds) |
| DES (of 64 bits) | 2.89 | 9.90 | 22.41 | 30.03 | 31.76 | 31.96 (16 rounds) |
| Heys SPN (of 16 bits) | 2.44 | 5.94 | 7.67 | 7.94 | 7.98 | |

AES reaches full avalanche after 2 MixColumns steps, because ShiftRows and MixColumns make each byte of the state depend on all 16 input bytes after 2 rounds. DES needs about 5 rounds, because a Feistel round changes only half of the block. The ideal values are 64, 32 and 8.

**One round of AES.** A one-bit change enters one S-box. In the first round there is no MixColumns in this count, so on average only about 4 of the 8 output bits of that S-box change, and the other 15 bytes are unchanged. The mean 4.02 matches this.

**S-box SAC matrices.** For the 4-bit S-box of the Heys tutorial, the rows of $P$ for input bits 1 to 4 are (0.5, 0.5, 0.5, 0.75), (0.75, 0.5, 0.75, 0.25), (0.5, 0.75, 0.5, 0.5) and (0.75, 0.75, 0.75, 0.75), with the bits numbered from the least significant. So it does not meet SAC. For the AES S-box, the 64 entries lie between 0.453 and 0.5625: close to SAC, but not exact. No bijective S-box needs exact SAC to be strong; the DDT and the LAT matter more.

**Non-example: XOR with the key.** $E_K(x) = x \oplus K$ has confusion of a kind, since the output depends on the key, but no diffusion: a one-bit change of the input changes exactly one output bit.

**Non-example: avalanche is not security.** A cipher can show perfect avalanche and still be weak. For example, $x \mapsto A(x) \oplus K$ for a fixed public invertible linear map $A$ whose columns each have about $n/2$ ones changes about half the bits for each input flip, but it is affine, and two queries tell it from a random permutation.

## Where it is used

- **Design of block ciphers.** [AES](/advanced-encryption-standard/) and other [substitution-permutation networks](/substitution-permutation-network/) separate the two tasks into the S-box layer and the linear layer. [DES](/data-encryption-standard/) mixes both inside its round function, with the expansion E and the permutation P for diffusion.
- **Design of S-boxes.** SAC, BIC, the differential uniformity and the nonlinearity are the selection criteria. See [S-box](/s-box/) and [Boolean function](/boolean-function/).
- **Hash functions and stream ciphers.** The same aims apply to compression functions and to the update functions of stream ciphers; the [avalanche effect](/avalanche-effect/) is a standard test for both.
- **Statistical test suites.** An avalanche test is one of the first checks on a new design. Passing it is necessary, but it proves nothing about security.

## References
