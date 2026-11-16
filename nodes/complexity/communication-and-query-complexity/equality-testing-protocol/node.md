---
tag: SVFWAE
kind: algorithm
slug: equality-testing-protocol
name: Randomized equality testing protocol
aliases:
- hashing-based equality test
- polynomial fingerprint protocol for equality
area: complexity/communication-and-query-complexity
level: intro
summary: Alice sends a random point r and the value of her string's polynomial at r. Bob compares it with his own value, so equality of n-bit strings costs O(log n) bits with one-sided error below 1/n.
solves: [equality-problem]
model: communication-model
complexity:
  vars: {n: the length in bits of each input string}
  communication: {worst: Θ(log n)}
  time: {worst: O(n)}
  space: {extra: O(log n)}
properties: {deterministic: false, one_sided_error: true, private_coin: true, two_way: true, messages: 2}
prereqs: [equality-problem, communication-model, fingerprinting, schwartz-zippel-lemma]
see_also: [randomized-communication-complexity, polynomial-hash-collision-bound, string-equality-testing, universal-hash-family, rabin-karp, greater-than-problem, one-sided-error, monte-carlo-algorithm]
sources:
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press, 1997
    locator: Chapter 3, Randomization (the randomized protocol for equality and the private-coin lower bound)
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 3, Randomized Protocols (section Some Protocols)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 7, Algebraic techniques (fingerprinting and the verification of string equality)
---

The randomized equality testing protocol decides the [equality problem](/equality-problem/) in the two-party [communication model](/communication-model/): Alice holds $x \in \{0,1\}^n$, Bob holds $y \in \{0,1\}^n$, and both must learn whether $x = y$. Alice reads her string as a polynomial over a prime field of size $q \approx n^2$, picks a random point, and sends the point and the value there; Bob evaluates his own polynomial at the same point and sends one answer bit. The protocol sends $2\lceil \log_2 q \rceil + 1 = O(\log n)$ bits, against the $n + 1$ bits that every deterministic protocol needs, and it errs only on unequal inputs, with probability at most $(n-1)/q < 1/n$. It is the communication form of [fingerprinting](/fingerprinting/).

## In plain words

Two people far apart each have a long row of zeros and ones. They want to know if the two rows are the same without sending a whole row.

The first person turns her row into a short code that depends on a number she picks at random. She sends the random number and the code. The second person makes the code of his own row with the same random number. If the codes differ, the rows differ for sure. If the codes agree, the rows are almost surely the same. He sends back one bit with the answer.

Equal rows always give equal codes. Different rows give equal codes only for a few bad choices of the random number, so the chance of a wrong answer is small. The message grows like the number of digits of the row length, not like the row length.

## The problem

The input is a pair of bit strings: $x = x_1 \ldots x_n$ goes to Alice and $y = y_1 \ldots y_n$ goes to Bob. Both know $n$. The output is $\mathrm{EQ}(x, y) = 1$ if $x = y$ and $0$ otherwise, and both players must know it at the end. This is the [equality problem](/equality-problem/). The cost of a protocol is the number of bits sent in the worst case, as defined on the [communication model](/communication-model/) page. Each player has private random bits, and a protocol may err with a small probability on each input, as in [randomized communication complexity](/randomized-communication-complexity/).

## The algorithm

For a string $s$ of length $n$, let $A_s(z) = s_1 + s_2 z + s_3 z^2 + \cdots + s_n z^{n-1}$. The protocol works in the field $\mathbb{F}_q$ of integers modulo a prime $q$, and writes each element of $\mathbb{F}_q$ as a binary number of $w = \lceil \log_2 q \rceil$ bits.

```pseudo id=main
EQUALITY-TEST(x, y)              ▷ Alice holds x, Bob holds y, both in {0,1}^n
L1  q ← the least prime with q ≥ max(2, n^2)          ▷ both players compute q from n
L2  Alice picks r uniformly at random in {0, ..., q-1}
L3  Alice computes a ← A_x(r) mod q
L4  Alice sends r and a, each as a ⌈lg q⌉-bit binary number
L5  Bob computes b ← A_y(r) mod q
L6  if a = b then Bob sends 1 else Bob sends 0
L7  both players output the bit that Bob sent
```

Line L1 needs no communication, because $q$ depends only on $n$. Lines L3 and L5 evaluate the polynomial by Horner's rule, $v \leftarrow (v \cdot r + s_i) \bmod q$ for $i = n, n-1, \ldots, 1$, so each player does $n$ multiplications and additions modulo $q$.

## Example

Let $n = 5$, $x = 10110$ and $y = 10011$. The least prime at least $25$ is $q = 29$, so $w = 5$. The two polynomials are

$$A_x(z) = 1 + z^2 + z^3, \qquad A_y(z) = 1 + z^3 + z^4.$$

Suppose Alice draws $r = 7$. She computes $A_x(7) = 1 + 49 + 343 = 393 = 13 \cdot 29 + 16$, so $a = 16$. She sends $r$ as `00111` and $a$ as `10000`. Bob computes $A_y(7) = 1 + 343 + 2401 = 2745 = 94 \cdot 29 + 19$, so $b = 19$. The values differ, so Bob sends `0`, and both output "not equal". The transcript is `00111 10000 0`, which is 11 bits, while the trivial protocol needs $n + 1 = 6$ bits for this small $n$.

The protocol is wrong only when $A_x(r) = A_y(r)$ in $\mathbb{F}_{29}$. Here $A_x(z) - A_y(z) = z^2 - z^4 = z^2 (1 - z)(1 + z)$, whose roots are $r = 0$, $r = 1$ and $r = 28 \equiv -1$. For those three values both sides get the same value (1, 3 and 1), and Bob wrongly answers "equal". The error on this pair is $3/29$, below the bound $(n-1)/q = 4/29$. For $n = 1$ to $5$, an exact count over every pair and every $r$ shows that the worst pair reaches the bound: for $n = 5$ it is $x = 00000$, $y = 01111$, with error $4/29$.

## Correctness

The protocol never errs when $x = y$, because then $A_x$ and $A_y$ are the same polynomial and $a = b$ for every $r$. When $x \ne y$, the difference $D = A_x - A_y$ has a coefficient $x_i - y_i = \pm 1$, which is not zero modulo $q$, so $D$ is a nonzero polynomial over $\mathbb{F}_q$ of degree at most $n - 1$. Such a polynomial has at most $n - 1$ roots, so at most $n - 1$ of the $q$ values of $r$ make Bob answer "equal". The error is therefore at most $(n-1)/q \le (n-1)/n^2 < 1/n$. This is the one-variable case of the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), and the same bound as the [polynomial hash collision bound](/polynomial-hash-collision-bound/). The full proof, with the count of the transcript length, is below.

## Complexity

Every run sends exactly $2\lceil \log_2 q \rceil + 1$ bits: two field elements from Alice and one bit from Bob. By Bertrand's postulate there is a prime between $n^2$ and $2n^2$, so $q < 2n^2$ and the cost is at most $4 \log_2 n + 5$ bits for $n \ge 2$. The exact costs for some values of $n$:

| $n$ | $q$ | bits sent | $n + 1$ | error bound $(n-1)/q$ |
|---|---|---|---|---|
| 5 | 29 | 11 | 6 | 0.138 |
| 64 | 4099 | 27 | 65 | 0.0154 |
| 1000 | 1000003 | 41 | 1001 | 0.000999 |
| $10^6$ | 1000000000039 | 81 | 1000001 | about $10^{-6}$ |
| $2^{33}$ (1 GiB) | 73786976294838206473 | 135 | $2^{33} + 1$ | about $1.2 \cdot 10^{-10}$ |

The protocol is first shorter than the trivial $n + 1$ bits at $n = 19$, where $q = 367$ and it sends 19 bits.

The cost is optimal up to a constant factor among private-coin protocols. Every private-coin protocol with error $1/3$ for a function $f$ sends $\Omega(\log D^{cc}(f))$ bits, where $D^{cc}(f)$ is the [deterministic communication complexity](/deterministic-communication-complexity/), and $D^{cc}(\mathrm{EQ}) = n + 1$. So the private-coin cost of equality is $\Theta(\log n)$.

Each player does $n$ multiplications and additions on numbers below $q$, which is $O(n)$ time on a machine whose words hold $O(\log n)$ bits, and keeps $O(\log n)$ bits of state.

## Properties

- One-sided error. An answer "not equal" is always correct. An answer "equal" is wrong with probability at most $(n-1)/q$ on each fixed pair. See [one-sided error](/one-sided-error/).
- Private coins. Only Alice uses random bits, and she sends the point $r$ that she drew. Bob needs no random bits.
- Two messages. Alice sends one message and Bob sends one bit. If only Bob must learn the answer, the protocol is one-way and sends $2\lceil \log_2 q \rceil$ bits.
- Fixed length. The transcript has the same length for every input and every random choice.
- Monte Carlo. The running time is fixed and the answer may be wrong, as in a [Monte Carlo algorithm](/monte-carlo-algorithm/).

## Variants and improvements

- Random prime. Alice reads $x$ as a number $X < 2^n$, picks a random prime $p$ from the primes up to a bound $T$, and sends $p$ and $X \bmod p$. A nonzero number below $2^n$ has fewer than $n$ distinct prime factors, so the error is at most $(n-1)/\pi(T)$, where $\pi(T)$ is the [number of primes](/prime-counting-function/) up to $T$. With $T = n^2$ the error is $O(\log n / n)$ and the cost is $O(\log n)$. For $n = 10$ and $T = 100$, an exact count over the 25 primes and all pairs gives a worst error of $4/25$ and a cost of 15 bits.
- Smaller error. With $q \ge n/\varepsilon$ the error is below $\varepsilon$ and the cost is $O(\log n + \log(1/\varepsilon))$ bits. Repeating the protocol $k$ times with independent points gives error at most $((n-1)/q)^k$ for $k$ times the cost.
- Public coins. If Alice and Bob share the random point, Alice sends only $a$, and the cost drops to $\lceil \log_2 q \rceil + 1$. With shared random strings $s$ the cost is $O(1)$: Alice sends the parities $\langle x, s \rangle \bmod 2$ for two independent random strings, and Bob compares them with his own. Two parities give error $1/4$ with 3 bits. Newman's theorem says that a private-coin protocol can replace the shared randomness at an extra cost of $O(\log n)$ bits, which explains the gap between the two models.
- Simultaneous messages. In the [simultaneous message model](/simultaneous-message-model/) with private coins, where each player sends one message to a referee, equality needs about $\sqrt{n}$ bits. The protocol above has no short form there, because Bob cannot learn Alice's random point.
- Other fingerprints. Any [universal hash family](/universal-hash-family/) with short keys works the same way: Alice sends the key and the hash of $x$. The polynomial family is a good choice because its keys and values are both $O(\log n)$ bits.

## When to use it

Use it to check that two copies of a large file, database or memory image are the same without sending either copy. Use it as a subroutine: the randomized protocol for the [greater-than problem](/greater-than-problem/) runs a binary search on prefixes and tests each prefix for equality this way. The [string equality testing](/string-equality-testing/) problem and the [Rabin-Karp](/rabin-karp/) algorithm use the same fingerprint inside one machine. Do not use it when the answer must be certain: a deterministic protocol must send $n + 1$ bits.

## Pitfalls

- The point must be random and drawn after the inputs are fixed. A fixed point $r$ gives a deterministic protocol, and then some pair $x \ne y$ is accepted for sure.
- The field must be larger than $n - 1$. If $q \le n - 1$, the difference polynomial may vanish on every point, and the bound $(n-1)/q$ says nothing. The choice $q \ge n^2$ makes the error below $1/n$.
- With private coins, Alice must send $r$. Forgetting to count those bits makes the protocol look twice as cheap as it is.
- The bound holds for each fixed pair $(x, y)$, over the random point. It is not an average over inputs.
- The error is one-sided. Repetition multiplies the error of "equal" answers, but a single "not equal" answer is final.

## Implementations

## History

Yao's 1979 paper, which defined the two-party model, also defined protocols that use random bits. The equality protocol became the standard first example of the power of randomness in communication: the deterministic cost is $n + 1$ bits and the private-coin cost is $\Theta(\log n)$. It uses the same fingerprint idea as the pattern matching algorithm of Karp and Rabin. Kushilevitz and Nisan (1997) and Rao and Yehudayoff (2020) give it in their chapters on randomized protocols.

## References
