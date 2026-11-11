---
tag: 1M8WNB
kind: definition
slug: hard-core-predicate
name: Hard-core predicate
aliases:
- Goldreich-Levin theorem
area: cryptography/public-key
level: research
summary: A single digit of the input of a one-way function that stays unpredictable from the output. Goldreich and Levin proved that the inner product with a public random string is such a digit.
prereqs: [one-way-function]
see_also: [trapdoor-one-way-function, pseudorandom-generator, hill-prg-from-one-way-functions, hadamard-code, list-decoding, pairwise-independence, blum-micali, rsa-problem]
sources:
  - paper: doi:10.1145/73007.73010
    title: Oded Goldreich and Leonid A. Levin, A hard-core predicate for all one-way functions, Proceedings of the 21st ACM Symposium on Theory of Computing, STOC 1989, pages 25 to 32
    locator: the whole paper (the inner product predicate, the proof with pairwise independent queries, and the statement that every one way function has a hard core predicate)
  - paper: doi:10.1137/0217013
    title: Werner Alexi, Benny Chor, Oded Goldreich and Claus P. Schnorr, RSA and Rabin functions, certain parts are as hard as the whole, SIAM Journal on Computing 17(2), pages 194 to 209, 1988
    locator: the whole paper (the least significant bit of the RSA function and of the Rabin function is hard core, and the low order log log N digits are simultaneously secure)
  - book: isbn:9780521791724
    title: Oded Goldreich, Foundations of Cryptography, Volume 1, Basic Tools, Cambridge University Press, 2001
    locator: Section 2.5 (the definition of a hard core predicate, the Goldreich-Levin theorem with the full proof, and the exercises on the easier variants)
  - paper: doi:10.1137/0213053
    title: Manuel Blum and Silvio Micali, How to generate cryptographically strong sequences of pseudo-random bits, SIAM Journal on Computing 13(4), pages 850 to 864, 1984
    locator: Sections 3 and 4 (the most significant digit of the discrete logarithm is as hard as the whole logarithm, and the generator built from one hard digit per step)
  - paper: "Andrew C. Yao, Theory and application of trapdoor functions, Proceedings of the 23rd IEEE Symposium on Foundations of Computer Science, FOCS 1982, pages 80 to 91"
    locator: the computational entropy of one way functions and the first use of single hard digits to build a pseudorandom generator
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2021
    locator: the chapter on theoretical constructions (the Goldreich-Levin theorem and the step from it to a pseudorandom generator)
---

A hard-core predicate of a function $f$ is one digit of the input that nobody can guess from the output much better than by a coin flip. The idea answers a gap in the definition of a [one-way function](/one-way-function/): a one-way function hides its whole input, but it may still leak parts of it, and a protocol that needs one unpredictable digit cannot use those parts. Goldreich and Levin (1989) proved that every one-way function has a hard-core predicate of a simple fixed form, the inner product of the input with a public random string. That theorem is the bridge from one-way functions to [pseudorandom generators](/pseudorandom-generator/), and its proof is a local [list decoder](/list-decoding/) for the [Hadamard code](/hadamard-code/).

**Notation.** $n$ is the input length, $x \leftarrow \{0,1\}^n$ a uniform input, and $\mathrm{negl}(n)$ a function that falls below $1/n^t$ for every $t$ and all large $n$. For $x, r \in \{0,1\}^n$ the inner product modulo 2 is $\langle x, r \rangle = \bigoplus_{i=1}^{n} x_i r_i$, and $e_i$ is the string with 1 in position $i$ and 0 elsewhere. "Efficient" means probabilistic polynomial time. $B$ is a predicting algorithm, $A$ the inverter built from it, and $\varepsilon = \varepsilon(n)$ the advantage of $B$.

## Definition

**Definition.** Let $f$ and $b$ be computable in polynomial time, with $b: \{0,1\}^* \to \{0,1\}$. Then $b$ is a *hard-core predicate* of $f$ if for every efficient algorithm $B$

$$\Pr_{x \leftarrow \{0,1\}^n}\left[B(f(x)) = b(x)\right] \le \tfrac{1}{2} + \mathrm{negl}(n).$$

Three remarks follow at once from the definition.

- The predicate must be nearly unbiased. If $\Pr[b(x) = 1] \ge 1/2 + 1/n$, the algorithm that ignores its input and answers 1 already beats the bound.
- No part of $b$ may survive in the output. If $f(x)$ keeps the first digit of $x$, then $b(x) = x_1$ is not hard core for $f$.
- If $f$ is one-to-one and has a hard-core predicate, then $f$ is one way. An inverter would return $x$, and $b(x)$ would follow by one more evaluation. So a hard-core predicate is a stronger object than a one-way function, and the theorem below says that the two are equivalent up to a change of the function.

**The Goldreich-Levin theorem.** Let $f$ be one way, and define

$$g(x, r) = (f(x), r), \qquad b(x, r) = \langle x, r \rangle, \qquad |r| = |x| = n.$$

Then $g$ is one way and $b$ is a hard-core predicate of $g$. In words: the pair $(f(x), r)$ hides the single digit $\langle x, r \rangle$. The theorem is proved as a reduction, and the reduction is what the rest of this section gives.

**Theorem (the reduction).** Suppose $B$ runs in time $t(n)$ and

$$\Pr_{x, r \leftarrow \{0,1\}^n}\left[B(f(x), r) = \langle x, r \rangle\right] \ge \tfrac{1}{2} + \varepsilon(n).$$

Then there is an algorithm $A$ that runs in time $O\!\left(t(n) \cdot n^2/\varepsilon^2\right)$ plus $O(n/\varepsilon^2)$ evaluations of $f$ and satisfies $\Pr_x[f(A(f(x))) = f(x)] \ge \varepsilon/2$ for infinitely many $n$ when $\varepsilon \ge 1/\mathrm{poly}(n)$. Since $f$ is one way, no such $B$ exists, so $\varepsilon$ is negligible.

### The easy version, with the full proof

First take the stronger hypothesis $3/4 + \varepsilon$ in place of $1/2 + \varepsilon$. The whole decoder is two queries per vote.

```pseudo id=easy
GL-DECODE-EASY(y, B, n, m)
L1  for i ← 1 to n
L2      votes ← 0
L3      repeat m times
L4          r ← a uniform string of n digits
L5          if B(y, r) ⊕ B(y, r ⊕ e_i) = 1 then votes ← votes + 1
L6      x'_i ← 1 if votes > m/2, else 0
L7  return x' = x'_1 ... x'_n
```

**Claim.** If $\Pr_{x, r}[B(f(x), r) = \langle x, r \rangle] \ge 3/4 + \varepsilon$ and $m = \lceil \ln(2n) / (2\varepsilon^2) \rceil$, then $\mathrm{GL\text{-}DECODE\text{-}EASY}(f(x), B, n, m)$ returns $x$ with probability at least $\varepsilon$ over the choice of $x$ and its own coins.

*Proof.*

**Step 1: a good set of inputs.** For each $x$ write $s(x) = \Pr_r[B(f(x), r) = \langle x, r \rangle]$, so that $\mathbb{E}_x[s(x)] \ge 3/4 + \varepsilon$. Let $G = \{x : s(x) \ge 3/4 + \varepsilon/2\}$ and $p = \Pr_x[x \in G]$. Splitting the expectation over $G$ and its complement, and using $s \le 1$ inside $G$ and $s < 3/4 + \varepsilon/2$ outside it,

$$\tfrac{3}{4} + \varepsilon \le p \cdot 1 + (1 - p)\left(\tfrac{3}{4} + \tfrac{\varepsilon}{2}\right) = \tfrac{3}{4} + \tfrac{\varepsilon}{2} + p\left(\tfrac{1}{4} - \tfrac{\varepsilon}{2}\right).$$

Hence $\varepsilon/2 \le p(1/4 - \varepsilon/2) \le p/4$, so $p \ge 2\varepsilon$. This is the [averaging argument](/markov-inequality/): at least a $2\varepsilon$ fraction of the inputs are good ones. Fix $x \in G$ and write $y = f(x)$ for the rest of the proof.

**Step 2: two queries give one digit.** The predicate is linear in its second argument, so

$$\langle x, r \oplus e_i \rangle = \langle x, r \rangle \oplus \langle x, e_i \rangle = \langle x, r \rangle \oplus x_i .$$

So $B(y, r) \oplus B(y, r \oplus e_i) = x_i$ whenever both queries get the right answer. When $r$ is uniform, both $r$ and $r \oplus e_i$ are uniform on their own, so each query is wrong with probability at most $1/4 - \varepsilon/2$. They are not independent, but the [union bound](/union-bound/) needs no independence:

$$\Pr_r\left[B(y, r) \oplus B(y, r \oplus e_i) \ne x_i\right] \le 2\left(\tfrac{1}{4} - \tfrac{\varepsilon}{2}\right) = \tfrac{1}{2} - \varepsilon .$$

Each vote in line L5 is therefore right with probability at least $1/2 + \varepsilon$. This step is the whole reason the hypothesis is $3/4$: with a predictor that is right on only $1/2 + \varepsilon$ of the strings, the same union bound gives the useless value $1 - 2\varepsilon$.

**Step 3: the majority of the votes.** For a fixed $i$ the $m$ strings $r$ of line L4 are independent, so the votes are independent, each right with probability $q \ge 1/2 + \varepsilon$. Let $V$ be the number of right votes. The majority of line L6 is wrong only if $V \le m/2$, which asks for a deviation of at least $\varepsilon m$ below the mean $qm$. The [Chernoff bound](/chernoff-bound/) in Hoeffding's form gives

$$\Pr\left[V \le m/2\right] \le \exp\left(-2\varepsilon^2 m\right) \le \frac{1}{2n}$$

for $m = \lceil \ln(2n)/(2\varepsilon^2) \rceil$.

**Step 4: all $n$ digits.** By the union bound over the $n$ digits, the probability that some digit is wrong is at most $n \cdot 1/(2n) = 1/2$. So for every $x \in G$ the decoder returns $x$ with probability at least $1/2$.

**Step 5: the whole algorithm.** Let $A(y)$ run the decoder and return its output. Then

$$\Pr_x\left[A(f(x)) = x\right] \ge \Pr_x[x \in G] \cdot \tfrac{1}{2} \ge 2\varepsilon \cdot \tfrac{1}{2} = \varepsilon .$$

The cost is $2nm = O(n \log n / \varepsilon^2)$ calls to $B$ and no call to $f$. If $\varepsilon$ is at least $1/\mathrm{poly}(n)$, then $A$ is efficient and inverts $f$ with probability $1/\mathrm{poly}(n)$, which contradicts the one-wayness of $f$. $\blacksquare$

### The full version, as a sketch

The real theorem allows a predictor that is right on only $1/2 + \varepsilon$ of the strings. The idea of Goldreich and Levin is to make each vote cost one query instead of two: ask $B$ about $r \oplus e_i$ only, and obtain $\langle x, r \rangle$ by guessing. A guess is affordable if it serves many votes at once, and it must still leave the votes spread out enough for a concentration bound. [Pairwise independence](/pairwise-independence/) is exactly the right amount of spread.

```pseudo id=full
GL-DECODE(y, B, n, l)
L1  r_1, ..., r_l ← independent uniform strings of n digits
L2  candidates ← empty list
L3  for each guess (σ_1, ..., σ_l) in {0,1}^l
L4      for i ← 1 to n
L5          votes ← 0
L6          for each nonempty S ⊆ {1, ..., l}
L7              r_S ← XOR of the r_j for j in S;  σ_S ← XOR of the σ_j for j in S
L8              if σ_S ⊕ B(y, r_S ⊕ e_i) = 1 then votes ← votes + 1
L9          x'_i ← 1 if votes > (2^l - 1)/2, else 0
L10     append x' to candidates
L11 return the candidate x' with f(x') = y, if there is one
```

- **One guess is right.** The $l$ values $\sigma_j$ are meant to be $\langle x, r_j \rangle$. The loop of line L3 tries all $2^l$ patterns, so one pass has them all right. The other passes produce rubbish, which line L11 throws away.
- **The guesses spread by linearity.** For a nonempty set $S$, line L7 builds $r_S = \bigoplus_{j \in S} r_j$, and linearity gives $\langle x, r_S \rangle = \bigoplus_{j \in S} \langle x, r_j \rangle = \sigma_S$ in the right pass. So $2^l - 1$ strings come with known predicate values for the price of $l$ guesses, and no query was spent on them.
- **The strings are pairwise independent.** For distinct nonempty sets $S \ne T$, the pair $(r_S, r_T)$ is distributed as a pair of independent uniform strings. So each $r_S$ is uniform, each vote of line L8 is right with probability at least $1/2 + \varepsilon$ when $x$ is good, and the votes for one digit are pairwise independent.
- **Chebyshev in place of Chernoff.** Pairwise independence makes the variance of the vote count add up, so the count $V$ over $m = 2^l - 1$ votes has $\mathrm{Var}(V) \le m/4$. [Chebyshev's inequality](/chebyshev-inequality/) gives $\Pr[V \le m/2] \le \mathrm{Var}(V)/(\varepsilon m)^2 \le 1/(4 \varepsilon^2 m)$. Taking $l = \lceil \log_2(2n/\varepsilon^2 + 1) \rceil$, so that $m \ge 2n/\varepsilon^2$, makes this at most $1/(8n)$, and the union bound over the $n$ digits leaves a failure probability of at most $1/8$ for a good $x$.
- **The count.** The averaging argument of Step 1 with the threshold $1/2 + \varepsilon/2$ gives a good set of density at least $\varepsilon$. So the right pass returns $x$ with probability at least $7/8$ for a good $x$, and $A$ succeeds with probability at least $7\varepsilon/8$. The cost is $(2^l - 1) \cdot n = O(n^2/\varepsilon^2)$ queries, because the answers of line L8 do not depend on the guess and can be computed once, plus $O(n/\varepsilon^2)$ evaluations of $f$ in line L11.

Line L11 is the only place that uses $f$. Without it the algorithm returns a list of $2^l = O(n/\varepsilon^2)$ candidates, one of which is $x$. That weaker output is enough for the reduction, since a random member of the list is right with probability $\Omega(\varepsilon^3/n)$, and it is the right statement when there is nothing to check against.

### The code view: list decoding of the Hadamard code

Fix $x$. The table of all values $r \mapsto \langle x, r \rangle$, for the $2^n$ strings $r$, is the [Hadamard](/hadamard-code/) codeword of $x$: a code of length $2^n$, dimension $n$ and relative distance $1/2$. A predictor $B(f(x), \cdot)$ with advantage $\varepsilon$ is a copy of that codeword with a $1/2 - \varepsilon$ fraction of the entries corrupted. Then

- a corruption rate below $1/4$ is inside the unique decoding radius, and $\mathrm{GL\text{-}DECODE\text{-}EASY}$ is the classic local self-corrector of the Hadamard code: two queries per digit;
- a rate of $1/2 - \varepsilon$ is past that radius, where the answer is no longer unique, so the output must be a list. The Johnson bound caps the list at $O(1/\varepsilon^2)$ codewords;
- $\mathrm{GL\text{-}DECODE}$ is a *local* list decoder: it never reads the whole corrupted word of length $2^n$, only $O(n^2/\varepsilon^2)$ entries of it, and it outputs the list in time polynomial in $n/\varepsilon$.

In the language of [Fourier analysis of Boolean functions](/fourier-analysis-of-boolean-functions/), the decoder finds every character $\chi_x$ whose correlation with the predictor is at least $2\varepsilon$, so it is an algorithm that lists the large Fourier coefficients of a function it can only query.

### Single digits of RSA and Rabin

The Goldreich-Levin theorem needs the extra random string $r$, which is a cost: a generator built with it stretches the input by one digit per application of $f$ and has to carry $r$ along. For particular functions one can do better and show that a *natural* digit of the input is hard core.

- **The least significant digit of RSA.** Alexi, Chor, Goldreich and Schnorr (1988) proved that an efficient algorithm which computes the last digit of $x$ from $(N, e, x^e \bmod N)$ with probability $1/2 + 1/\mathrm{poly}$ over a uniform $x$ gives an efficient algorithm that solves the whole [RSA problem](/rsa-problem/). So the last digit is hard core for the RSA function, under no assumption beyond the hardness of RSA itself.
- **The least significant digit of Rabin.** The same paper proves the matching statement for $x \mapsto x^2 \bmod N$: predicting the last digit with advantage $1/\mathrm{poly}$ gives a factoring algorithm. See the [Rabin cryptosystem](/rabin-cryptosystem/) for the root-to-factor step that this builds on.
- **Several digits at once.** The paper also shows that the low order $O(\log \log N)$ digits are *simultaneously* secure: the whole block of them is indistinguishable from a random block of the same length, which is what the [Blum-Blum-Shub](/blum-blum-shub/) generator needs in order to output more than one digit per squaring.
- **The method.** The proof is older than the inner product predicate and does not use it. It works from the multiplicative self-reducibility of the two functions, since $x \mapsto 2x \bmod N$ is easy to apply to a ciphertext, and recovers $x$ by a binary search on the interval that holds it, with a sampling trick that reuses a few random points to keep the query count low. Earlier results of Ben-Or, Chor and Shamir and of Vazirani and Vazirani needed a larger advantage, such as $3/4$, which is the same gap that separates the two decoders above.
- **The first example of all.** Blum and Micali (1984) showed that the most significant digit of the [discrete logarithm](/discrete-logarithm-problem/) is as hard to find as the logarithm itself, and used it to build the first generator with a proof, the [Blum-Micali generator](/blum-micali/). That paper introduced the whole pattern: one hard digit per step of a one-way permutation.

## Examples and non-examples

- **The inner product, for every one-way function.** $b(x, r) = \langle x, r \rangle$ is hard core for $g(x, r) = (f(x), r)$. This is the theorem, and it is the only construction that works for an arbitrary one-way function.
- **The exclusive or of all digits is not enough.** $b(x) = \bigoplus_i x_i$ is the inner product with the fixed string $1^n$. It is not hard core in general: for the one-way function $f'(x) = (f(x), \bigoplus_i x_i)$, which is still one way when $f$ is, the digit sits in the output. The random $r$ is what rules this out, and it is why the theorem changes the function rather than the predicate alone.
- **A digit of the input, copied out.** $b(x) = x_1$ is not hard core for $f'(x) = (f(x), x_1)$, for the same reason. A hard-core predicate is always a property of the pair $(f, b)$, never of $b$ alone.
- **The Jacobi symbol is not hard core for RSA.** The symbol $\left(\frac{x}{N}\right)$ takes the values $\pm 1$ and is multiplicative, so for an odd exponent $e$ one gets $\left(\frac{x^e}{N}\right) = \left(\frac{x}{N}\right)^e = \left(\frac{x}{N}\right)$. Anybody holding the ciphertext computes the symbol of the plaintext in polynomial time, with no key and no error. Compare this with the previous item: RSA leaks this one function of $x$ exactly, while the last digit of $x$ is as hard as all of $x$.
- **A constant predicate.** $b(x) = 0$ is predicted with probability 1. The bias rules it out.
- **Where the digits are used.** One hard-core digit per step turns a one-way permutation into a [pseudorandom generator](/pseudorandom-generator/), which is the Blum-Micali shape. The general case, a one-way function that is not a permutation, needs much more work and is the subject of the [HILL construction](/hill-prg-from-one-way-functions/). A single hidden digit is also what lets [probabilistic encryption](/probabilistic-encryption/) schemes such as [Goldwasser-Micali](/goldwasser-micali-cryptosystem/) and [Blum-Goldwasser](/blum-goldwasser-cryptosystem/) mask one message digit at a time, with [semantic security](/semantic-security/) from the [indistinguishability](/computational-indistinguishability/) of the masked digit from a coin flip.

**The code.** The implementation folder has the predicate, the two decoders and a simulated predictor. The toy function is $f(x) = 14^x \bmod 1031$ on inputs of 10 digits; 14 generates the whole group of order 1030, so $f$ is one-to-one there and a candidate can be checked. The function is far too small to be one way, and that is on purpose: the code is the reduction, not an attack, and the predictor it talks to is a simulation that knows the secret and answers with a fixed error pattern of a chosen density. The pattern is a deterministic function of $r$, which is the honest model, because an oracle that flipped a fresh coin on each call could be cleaned up by asking the same question twice.

The measured runs, with fixed seeds, are these. A predictor whose true accuracy is $842/1024 \approx 0.822$, above the $3/4$ threshold, lets $\mathrm{GL\text{-}DECODE\text{-}EASY}$ with 200 trials per digit recover the secret $x = 339$ from 4000 queries. The same decoder recovers 40 further secrets at accuracy $0.85$ with only 80 trials each. A predictor at accuracy $0.5$ is a coin flip, and the decoder returns a wrong string from the same 4000 queries. For the full decoder, a predictor of true accuracy $0.619$, which is far below $3/4$, is enough: with $l = 8$ seed strings the decoder asks $(2^8 - 1) \cdot 10 = 2550$ questions, builds 256 candidates, and the check against $f$ leaves the right one. At accuracy $0.591$ and $l = 9$ it needs 5110 questions. The whole test file runs in about 1.2 seconds.

There is no official test vector for the Goldreich-Levin decoder, as there is no standard that specifies it; the tests compare the predicate against an independent digit-by-digit oracle on 600 random pairs, and check the recovered secret against the known one. The code is for study only, it is not constant time, and it runs only in one local process against a simulated oracle.

## Related definitions

- **[One-way function](/one-way-function/).** The object whose input is hidden as a whole. A hard-core predicate says which single digit of it is hidden.
- **[Trapdoor one-way function](/trapdoor-one-way-function/).** The same question with a key that inverts. The theorem applies unchanged, which is how public-key schemes get a hidden digit.
- **Hard-core function.** A function $h: \{0,1\}^n \to \{0,1\}^{k}$ whose whole output is indistinguishable from $k$ random digits given $f(x)$. One digit is the case $k = 1$; the Goldreich-Levin proof extends to $k = O(\log n)$ digits, and the simultaneous security of $O(\log\log N)$ digits of RSA is the same notion for that function.
- **Hard-core set.** A different and unrelated use of the words, from Impagliazzo: a set of inputs of noticeable density on which a mildly hard function is almost perfectly hard. It is a statement about where the hardness sits, not about a digit of the input.
- **[Pairwise independence](/pairwise-independence/).** The property of the query strings $r_S$ that makes the full decoder work, with [Chebyshev's inequality](/chebyshev-inequality/) in place of the [Chernoff bound](/chernoff-bound/).
- **[List decoding](/list-decoding/) and the [Hadamard code](/hadamard-code/).** The coding view of the same theorem, where a hard-core predicate is a codeword and the reduction is a local list decoder.
- **[Computational indistinguishability](/computational-indistinguishability/).** The definition says that $(f(x), r, \langle x, r \rangle)$ and $(f(x), r, c)$ for a random digit $c$ are indistinguishable, so a hard-core predicate is a one-digit indistinguishability statement.

## References
