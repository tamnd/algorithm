---
tag: 40P13C
kind: theorem
slug: shannon-perfect-secrecy-theorem
name: Shannon's theorem on perfect secrecy
aliases:
- Shannon's perfect secrecy bound
area: cryptography/symmetric-ciphers
level: intro
summary: A perfectly secret cipher needs at least as many keys as messages. When the counts are equal, it is perfectly secret exactly when keys are uniform and one key maps each message to each ciphertext.
prereqs: [perfect-secrecy, one-time-pad]
see_also: [perfect-secrecy, one-time-pad, shannon-entropy, conditional-entropy, stream-cipher, pseudorandom-generator, semantic-security, symmetric-encryption]
sources:
  - paper: doi:10.1002/j.1538-7305.1949.tb00928.x
    title: Claude E. Shannon, Communication theory of secrecy systems, Bell System Technical Journal 28(4), 1949, pp. 656-715
    locator: Part II, the section on perfect secrecy (the number of keys is at least the number of messages, and the characterization of perfect systems with equal numbers of keys, messages and cryptograms)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Section 2.3 (limitations of perfect secrecy, the bound on the key space) and Section 2.4 (Shannon's theorem)
  - book: isbn:9781138197015
    title: Douglas R. Stinson and Maura B. Paterson, Cryptography, Theory and Practice, fourth edition, CRC Press, 2018
    locator: Section 3.3 (the theorem for cryptosystems with equal numbers of keys, plaintexts and ciphertexts) and Section 3.4 (entropy)
---

Shannon's theorem on perfect secrecy gives the price of [perfect secrecy](/perfect-secrecy/). First, a perfectly secret encryption scheme needs at least as many keys as messages, and in terms of entropy, at least as much key uncertainty as message uncertainty. Second, when the numbers of messages, keys and ciphertexts are equal, a scheme is perfectly secret exactly when every key is equally likely and, for each message and each ciphertext, exactly one key maps the message to the ciphertext. The [one-time pad](/one-time-pad/) is the standard scheme that meets both parts with equality. Three things must be kept apart here: the *scheme* (the one-time pad), the *definition* (perfect secrecy), and the *theorem*, which says what every scheme that meets the definition must look like.

## Statement

Let $\Pi = (\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec})$ be an encryption scheme with finite message space $\mathcal{M}$, key space $\mathcal{K}$ and ciphertext space $\mathcal{C}$, and with $\mathrm{Dec}_k(\mathrm{Enc}_k(m)) = m$ for all $k, m$. Decryption is deterministic. Assume that every key in $\mathcal{K}$ has positive probability under $\mathrm{Gen}$.

**Theorem 1 (the key bound).** If $\Pi$ is perfectly secret, then $\lvert \mathcal{K} \rvert \ge \lvert \mathcal{M} \rvert$. Moreover, for every distribution of the message $M$, $H(K) \ge H(M)$, where $H$ is the [Shannon entropy](/shannon-entropy/).

**Theorem 2 (the characterization).** Let encryption be deterministic, let $\lvert \mathcal{M} \rvert = \lvert \mathcal{K} \rvert = \lvert \mathcal{C} \rvert$, and assume that every ciphertext in $\mathcal{C}$ is $\mathrm{Enc}_k(m)$ for some $k$ and $m$. Then $\Pi$ is perfectly secret if and only if

1. $\mathrm{Gen}$ chooses each key with probability $1 / \lvert \mathcal{K} \rvert$, and
2. for every $m \in \mathcal{M}$ and every $c \in \mathcal{C}$ there is exactly one key $k$ with $\mathrm{Enc}_k(m) = c$.

## In plain words

To hide a message completely, you need at least as many possible keys as possible messages. If there were fewer keys, then a ciphertext, tried with every key, could only decrypt to some of the messages, and the others would be ruled out. That is already information.

When keys, messages and ciphertexts come in equal numbers, perfect secrecy has an exact shape. Every key must be equally likely, and any message must be able to turn into any ciphertext, by exactly one key. The one-time pad has this shape.

## Proof

We use the equivalent form of perfect secrecy proved on the [perfect secrecy](/perfect-secrecy/) page: $\Pi$ is perfectly secret if and only if $\Pr[\mathrm{Enc}_K(m) = c] = \Pr[\mathrm{Enc}_K(m') = c]$ for all $m, m', c$.

**Theorem 1, the count.** Suppose $\lvert \mathcal{K} \rvert < \lvert \mathcal{M} \rvert$. Let $M$ be uniform on $\mathcal{M}$, and take a ciphertext $c$ with $\Pr[C = c] > 0$. Let $\mathcal{M}(c) = \{\mathrm{Dec}_k(c) : k \in \mathcal{K}\}$ be the set of messages that $c$ can decrypt to. Since decryption is deterministic, $\lvert \mathcal{M}(c) \rvert \le \lvert \mathcal{K} \rvert < \lvert \mathcal{M} \rvert$, so some message $m$ is not in $\mathcal{M}(c)$. If $C = c$ and the key is $k$, then $M = \mathrm{Dec}_k(c) \in \mathcal{M}(c)$, by correctness. So $\Pr[M = m \mid C = c] = 0$, while $\Pr[M = m] = 1 / \lvert \mathcal{M} \rvert > 0$. This contradicts perfect secrecy. $\square$

**Theorem 1, the entropy.** By correctness, $M$ is a function of $K$ and $C$, so $H(M \mid K, C) = 0$. Perfect secrecy says that $M$ and $C$ are independent, so $H(M) = H(M \mid C)$, with the [conditional entropy](/conditional-entropy/). Then
$$H(M) = H(M \mid C) \le H(M, K \mid C) = H(K \mid C) + H(M \mid K, C) = H(K \mid C) \le H(K).$$
The first inequality holds because adding a variable cannot lower the entropy, the equality is the chain rule, and the last step holds because conditioning cannot raise the entropy. $\square$

**Theorem 2, "if".** Assume 1 and 2. For $m$ and $c$, let $k_{m,c}$ be the unique key with $\mathrm{Enc}_{k_{m,c}}(m) = c$. Then $\Pr[\mathrm{Enc}_K(m) = c] = \Pr[K = k_{m,c}] = 1 / \lvert \mathcal{K} \rvert$, the same value for every $m$. By the equivalent form, $\Pi$ is perfectly secret. $\square$

**Theorem 2, "only if".** Assume that $\Pi$ is perfectly secret.

*Condition 2.* Fix $m$. Take any $c \in \mathcal{C}$. By assumption $c = \mathrm{Enc}_{k'}(m')$ for some $k', m'$, and $\Pr[K = k'] > 0$, so $\Pr[\mathrm{Enc}_K(m') = c] > 0$. By the equivalent form, $\Pr[\mathrm{Enc}_K(m) = c] > 0$ as well, so some key maps $m$ to $c$. So the map $k \mapsto \mathrm{Enc}_k(m)$ from $\mathcal{K}$ to $\mathcal{C}$ is onto. Since $\lvert \mathcal{K} \rvert = \lvert \mathcal{C} \rvert$, it is a bijection, and exactly one key maps $m$ to $c$. Call it $k_{m,c}$.

*Condition 1.* Fix $c$. The keys $k_{m,c}$ for different messages $m$ are different: if $k_{m,c} = k_{m',c} = k$, then $m = \mathrm{Dec}_k(c) = m'$. So $m \mapsto k_{m,c}$ is a one-to-one map from $\mathcal{M}$ to $\mathcal{K}$, and since $\lvert \mathcal{M} \rvert = \lvert \mathcal{K} \rvert$, every key is $k_{m,c}$ for exactly one $m$. By the equivalent form, $\Pr[K = k_{m,c}] = \Pr[\mathrm{Enc}_K(m) = c]$ has the same value for all $m$. So all keys have the same probability, which is $1 / \lvert \mathcal{K} \rvert$. $\blacksquare$

## Consequences

- **The one-time pad is optimal.** On $N$-bit messages it uses $2^N$ keys, the fewest that Theorem 1 allows. With $\lvert \mathcal{M} \rvert = \lvert \mathcal{K} \rvert = \lvert \mathcal{C} \rvert = 2^N$, Theorem 2 says that every perfectly secret scheme of this size looks like it: uniform keys, and one key from each message to each ciphertext.
- **Latin squares.** Under the conditions of Theorem 2, the table with a row for each key, a column for each message and the ciphertext in each cell is a Latin square: each ciphertext occurs once in each row (correctness) and once in each column (condition 2). Every Latin square with a uniformly chosen row gives a perfectly secret scheme.
- **Keys cannot be reused or stretched.** To send messages with a total of $L$ bits of entropy with perfect secrecy, the parties need at least $L$ bits of key entropy, agreed in advance. A [pseudorandom generator](/pseudorandom-generator/) cannot help: it gives a [stream cipher](/stream-cipher/), which can be at best computationally secure.
- **Modern definitions are computational.** Because of this bound, practical encryption aims for [semantic security](/semantic-security/) against attackers with bounded resources, with short keys.

## Tightness

- **The bound is met.** The one-time pad has $\lvert \mathcal{K} \rvert = \lvert \mathcal{M} \rvert$ and $H(K) = H(M)$ when $M$ is uniform.
- **The equal sizes are needed in Theorem 2.** Take one-bit messages and four keys $0, 1, 2, 3$, where key $k$ encrypts by XOR with $k \bmod 2$, with probabilities $0.4, 0.1, 0.1, 0.4$. The bit $k \bmod 2$ is uniform, so the scheme is perfectly secret. But the keys are not uniform, and two keys map each message to each ciphertext. Here $\lvert \mathcal{K} \rvert = 4 > 2 = \lvert \mathcal{M} \rvert$.
- **Theorem 1 does not imply uniform keys.** In the same example the key bound holds with room to spare, and the key distribution is not uniform.
- **Uniform keys are not enough.** The shift cipher on two letters has 26 uniform keys but $26^2$ messages, so it is not perfectly secret.

## History

Claude Shannon wrote the theory in a classified report at Bell Labs in 1945, "A Mathematical Theory of Cryptography", and published it in 1949 as "Communication theory of secrecy systems" in the Bell System Technical Journal 28(4). In it he defined perfect secrecy by a posteriori probabilities of messages equal to their a priori probabilities, showed that perfect secrecy requires at least as many keys as messages, characterized the perfect systems with equal numbers of messages, keys and cryptograms, and showed that the Vernam system with a random key meets the definition. The same paper introduced the unicity distance, and the ideas of confusion and diffusion. Modern textbooks, such as Katz and Lindell, state the result for schemes with randomized encryption and prove the bound by the counting argument above.

## References
