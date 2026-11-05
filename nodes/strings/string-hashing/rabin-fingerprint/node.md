---
tag: TPQWFQ
kind: technique
slug: rabin-fingerprint
name: Rabin fingerprint
aliases:
- Rabin fingerprinting
- GF(2) polynomial fingerprint
area: strings/string-hashing
level: advanced
summary: Fingerprint a bit string as its residue modulo a randomly chosen irreducible polynomial over GF(2).
prereqs: [fingerprinting, irreducible-polynomial]
see_also: [rabin-karp, dedup, cyclic-redundancy-check, string-equality-testing, polynomial-rolling-hash, shingling, polynomial-gcd, universal-string-hashing]
sources:
  - paper: doi:10.1007/978-1-4613-9323-8_11
    title: Andrei Z. Broder, Some applications of Rabin's fingerprinting method, in Sequences II, Methods in Communication, Security, and Computer Science, Springer (1993), 143-152
    locator: the fingerprint modulo a random irreducible polynomial over Z2, its collision probability, its fast table-driven computation, and its applications
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition, Cambridge University Press, 2009
    locator: Section 19.3, Theorem 19.12 (between q^l/(2l) and q^l/l monic irreducible polynomials of degree l), and Section 20.1, Algorithms IPT and RIP (testing and generating random irreducible polynomials)
  - paper: doi:10.1145/502034.502052
    title: Athicha Muthitacharoen, Benjie Chen and David Mazières, A low-bandwidth network file system, Proceedings of the 18th ACM Symposium on Operating Systems Principles (SOSP 2001), 174-187
    locator: the division of files into chunks at positions chosen by Rabin fingerprints of a 48-byte sliding window
---

A Rabin fingerprint reads a string of $n$ bits $a_0 a_1 \cdots a_{n-1}$ as the polynomial $A(t) = a_0 t^{n-1} + a_1 t^{n-2} + \cdots + a_{n-1}$ over the two-element field GF(2), and takes as fingerprint the remainder $f_P(A) = A(t) \bmod P(t)$, where $P$ is an [irreducible polynomial](/irreducible-polynomial/) of degree $k$ drawn at random. The fingerprint has $k$ bits, needs only shifts and exclusive ors, and can be updated in $O(1)$ word operations when a window slides by one bit or, with a table, by one byte. Two fixed different strings of $n$ bits get the same fingerprint with probability at most $(n-1)/(2^k - 2^{\lfloor k/2 \rfloor + 1})$ for $k \ge 3$, about $n/2^k$, over the choice of $P$. Michael Rabin proposed it in 1981, and it is used for content-defined chunking in deduplicating storage and for comparing files and documents.

## In plain words

Treat a string of zeros and ones as a polynomial: each bit is a coefficient. Divide it by another polynomial, chosen at random from a special kind, and keep the remainder. The remainder is short, for example 64 bits, and it is the fingerprint.

Equal strings always have equal fingerprints. Two different strings have equal fingerprints only if the random divisor divides their difference, and a difference can have only a few such divisors among a very large number of candidates. So the chance is tiny.

The arithmetic has no carries: adding is the same as exclusive or. So computers do it fast, and the fingerprint of a window that moves one step can be found from the old one with a few operations.

## When it applies

- **Equality tests on long bit strings.** Strings, file blocks or windows of a stream are compared by $k$-bit fingerprints, as in [string equality testing](/string-equality-testing/), and a small one-sided error is acceptable.
- **Sliding windows.** The fingerprint of every window of a fixed length in a stream is needed, for example to choose chunk boundaries or to find repeated blocks.
- **Hardware or bit-level code.** Shifts and exclusive ors are cheap, and a modular multiplication of integers is not wanted.
- **Inputs fixed before the polynomial is drawn.** The bound holds for strings that do not depend on $P$. The fingerprint is linear, so anyone who knows $P$ can make collisions at will.

## The template

Strings are over the binary alphabet; a byte string is the bit string of its bytes, most significant bit first. Indices are 0-based. All polynomials have coefficients in GF(2), where addition and subtraction are both the exclusive or, and a polynomial of degree less than $k$ is stored as a $k$-bit word.

```pseudo id=main
RABIN-FINGERPRINT(a[0 .. n-1])
L1  k ← the fingerprint length                                       ▷ hole: k from the error target
L2  repeat P ← t^k + (k random lower coefficients) until P is irreducible   ▷ hole: the irreducibility test
L3  f ← 0
L4  for i ← 0 to n − 1 do
L5      f ← (f · t + a[i]) mod P                                     ▷ hole: bit, byte or word steps
L6  return f                                                          ▷ equals A(t) mod P
SLIDE(f, out, in)                                                     ▷ window of w bits moves right by one
L7  return ((f · t + in) mod P) + out · (t^w mod P)                   ▷ hole: what to do with each window
```

**The holes.**

- *The length $k$.* For $N$ comparisons of strings of at most $n$ bits, the union bound gives a total error of about $N n / 2^k$; $k = 64$ is common.
- *The irreducibility test.* Line L2 draws a monic polynomial of degree $k$ and tests it. A monic $P$ of degree $k$ is irreducible if and only if $\gcd(t^{2^i} - t, P) = 1$ for $i = 1, \ldots, \lfloor k/2 \rfloor$ (Shoup's Algorithm IPT, with $q = 2$). At least a fraction $1/(2k)$ of the monic polynomials of degree $k$ are irreducible (Shoup, Theorem 19.12), so the expected number of draws is at most $2k$; it is about $k$ in fact.
- *The step size.* Line L5 handles one bit: shift left by one, add the new bit, and if the coefficient of $t^k$ is 1, add $P$. A byte at a time uses a table of 256 entries $U[x] = x(t) \cdot t^k \bmod P$ indexed by the top 8 bits of $f$: $f \leftarrow ((f \bmod t^{k-8}) \cdot t^8 + \text{byte}) + U[\lfloor f / t^{k-8} \rfloor]$.
- *The use of a window.* Compare it, store it in a table, or cut a chunk when some of its bits match a fixed value.

**Why it is correct.** Line L5 keeps $f = a_0 t^{i} + \cdots + a_i \bmod P$ after step $i$, by Horner's rule, so line L6 returns $A(t) \bmod P$. For SLIDE, the window $W = a_s \cdots a_{s+w-1}$ and the next window $W'$ satisfy $W'(t) = W(t)\, t + a_{s+w} - a_s t^w$, and minus is plus in GF(2).

**The collision bound.** Let $A \ne B$ be fixed strings of $n$ bits, and $D = A - B$, a nonzero polynomial of degree at most $n - 1$. Then $f_P(A) = f_P(B)$ if and only if $P$ divides $D$. Since GF(2)[t] has unique factorization and the degrees of the factors add up to at most $n - 1$, at most $(n-1)/k$ different irreducible polynomials of degree $k$ divide $D$. Let $I_k$ be the number of irreducible monic polynomials of degree $k$. Then

$$\Pr_P\big[f_P(A) = f_P(B)\big] \le \frac{(n-1)/k}{I_k}.$$

Counting by degree gives $\sum_{d \mid k} d\, I_d = 2^k$, and Möbius inversion gives $k I_k = \sum_{d \mid k} \mu(d)\, 2^{k/d}$. The terms with $d > 1$ have the distinct exponents $k/d \le \lfloor k/2 \rfloor$, so their absolute values add up to at most $2^{\lfloor k/2 \rfloor + 1} - 2$, and $k I_k > 2^k - 2^{\lfloor k/2 \rfloor + 1}$. Hence, for $k \ge 3$, the probability is below $(n-1)/(2^k - 2^{\lfloor k/2 \rfloor + 1})$. For $k = 64$ there are $I_{64} = 288230376084602880$ such polynomials, just under $2^{64}/64$, and the bound is about $(n - 1)/2^{64}$.

| $k$ | 4 | 8 | 16 | 32 | 64 |
|---|---|---|---|---|---|
| $I_k$ | 3 | 30 | 4080 | 134215680 | 288230376084602880 |
| $2^k / k$ | 4 | 32 | 4096 | 134217728 | $2.88 \times 10^{17}$ |

**Example.** Take $k = 4$ and $P = t^4 + t + 1$, written 10011; the three irreducible polynomials of degree 4 are 10011, 11001 and 11111. For $A = $ 11010110, line L5 runs as follows; "reduce" adds 10011 when the shifted value has 5 places.

| bit | $f \cdot t + a_i$ | after reduction |
|---|---|---|
| 1 | 1 | 1 |
| 1 | 11 | 11 |
| 0 | 110 | 110 |
| 1 | 1101 | 1101 |
| 0 | 11010 | 1001 |
| 1 | 10011 | 0 |
| 1 | 1 | 1 |
| 0 | 10 | 10 |

So $f_P(A) = 0010$. The string $B = A + P \cdot t = $ 11010110 + 00100110 = 11110000 has the same fingerprint 0010, since $D = P \cdot t$. Of the three irreducible polynomials of degree 4, only 10011 divides $D$, so a random choice makes $A$ and $B$ collide with probability $1/3$, below the bound $(n-1)/(k I_k) = 7/12$.

Sliding a window of $w = 6$ bits over 1101011010, with $t^6 \bmod P = $ 1100:

| start $s$ | window | in | out | $(f \cdot t + \text{in}) \bmod P$ | fingerprint |
|---|---|---|---|---|---|
| 0 | 110101 | | | | 0000 |
| 1 | 101011 | 1 | 1 | 0001 | 1101 |
| 2 | 010110 | 0 | 1 | 1001 | 0101 |
| 3 | 101101 | 1 | 0 | 1011 | 1011 |
| 4 | 011010 | 0 | 1 | 0101 | 1001 |

Each fingerprint equals the one computed directly from the window. The first window, $t^5 + t^4 + t^2 + 1 = (t + 1) P$, has fingerprint 0.

## Classic examples

- **Content-defined chunking.** The Low-Bandwidth File System computes the Rabin fingerprint of every 48-byte window of a file and ends a chunk where the low 13 bits of the fingerprint equal a fixed value, which gives chunks of 8 KB on average. An insertion then changes only the chunks near it, so [deduplication](/dedup/) and network transfer can reuse the others.
- **[Rabin-Karp](/rabin-karp/) over GF(2).** Slide a window of the pattern length over the text and compare its fingerprint with that of the pattern; each step costs $O(1)$ word operations.
- **[String equality testing](/string-equality-testing/).** Two parties compare files of $n$ bits by sending $P$ and a $k$-bit fingerprint, about $2k$ bits in all, with error about $n/2^k$.
- **Document resemblance.** [Shingling](/shingling/) needs a short hash of every window of words, and a rolling fingerprint gives all of them in one pass.

## Variations

- **Integer fingerprints.** Karp and Rabin's integer version reduces the number $\sum a_i 2^{n-1-i}$ modulo a random prime, and the [polynomial rolling hash](/polynomial-rolling-hash/) evaluates the polynomial at a random point modulo a fixed prime. Both have bounds of the same form; the GF(2) version avoids carries and integer multiplication.
- **Fixed polynomial: CRC.** A [cyclic redundancy check](/cyclic-redundancy-check/) is the same remainder with a fixed public polynomial. It detects random and burst errors, but it has no collision bound for chosen inputs.
- **Several polynomials.** Fingerprints modulo independent random polynomials multiply their error bounds. One polynomial of degree $2k$ is about as good as two of degree $k$ and costs about the same.
- **Composition.** $f_P(AB) = f_P(A) \cdot (t^{|B|} \bmod P) + f_P(B) \bmod P$, so fingerprints of concatenations, prefixes and blocks combine as for the integer hash.

## Pitfalls

- **Leading zeros.** The strings 0101 and 101 give the same polynomial and the same fingerprint. Compare only strings of equal length, add the length to the fingerprint, or put a 1 bit in front of each string.
- **Reducible polynomials.** The bound counts the irreducible divisors of $D$. A reducible $P$, such as $t^k + 1$ or a fixed product, can divide many more differences; for $P = t^k$ the fingerprint is just the last $k$ bits.
- **Linearity.** $f_P(A + B) = f_P(A) + f_P(B)$ and $f_P(0 \cdots 0) = 0$ for every $P$. If $P$ becomes known, adding any multiple of $P$ to a string gives a collision. This is a fingerprint, not a cryptographic hash.
- **The wrong end of the window.** In SLIDE the leaving bit has weight $t^w$ after the shift, not $t^{w-1}$; use the precomputed $t^w \bmod P$.
- **Error for many pairs.** The bound is for one pair. A system that stores $N$ fingerprints and looks for any collision among them has error up to $\binom{N}{2}$ times the bound; choose $k$ for that total.

## Exercises

1. Prove the composition rule $f_P(AB) = f_P(A)\, (t^{|B|} \bmod P) + f_P(B) \bmod P$.
2. Derive the byte-step formula of line L5 and the table $U$, and show that it uses one table lookup, two shifts, one mask and two exclusive ors per byte.
3. Show that 10011, 11001 and 11111 are the only irreducible polynomials of degree 4 over GF(2), and check the formula $k I_k = \sum_{d \mid k} \mu(d) 2^{k/d}$ for $k = 4$.
4. Show that $t^{2^k} - t$ is the product of all monic irreducible polynomials whose degree divides $k$, and explain why this proves the test of line L2.
5. In content-defined chunking with a boundary when 13 chosen bits of the fingerprint of the window match a fixed value, and fingerprints that behave like random values, what is the expected chunk length? *Answer:* $2^{13} = 8192$ bytes, since each position is a boundary with probability $2^{-13}$.

## References
