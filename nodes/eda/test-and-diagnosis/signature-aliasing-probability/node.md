---
tag: BP75TZ
kind: theorem
slug: signature-aliasing-probability
name: Signature aliasing probability
aliases:
- MISR aliasing bound
- LFSR aliasing probability
area: eda/test-and-diagnosis
level: advanced
summary: For independent random bit errors, the chance that a k-bit signature register with feedback term 1 ends with the good signature after a faulty response tends to 2^(-k).
prereqs: [multiple-input-signature-register, markov-chain]
see_also: [built-in-self-test, stationary-distribution, ergodic-theorem, perron-frobenius-theorem, cyclic-redundancy-check, linear-code, x-compact, gf2-polynomial-arithmetic]
sources:
  - paper: doi:10.1109/TC.1980.1675610
    title: J. E. Smith, Measures of the effectiveness of fault signature analysis, IEEE Transactions on Computers C-29(6), 510 to 514, 1980
    locator: the aliasing probability when all nonzero error streams are equally likely
  - paper: doi:10.1109/43.3132
    title: T. W. Williams, W. Daehn, M. Gruetzner and C. W. Starke, Bounds and analysis of aliasing errors in linear feedback shift registers, IEEE Transactions on Computer-Aided Design 7(1), 75 to 83, 1988
    locator: the Markov chain model of the error state under independent bit errors, the limit of the aliasing probability, and the transient for primitive and non-primitive polynomials
  - paper: "T. W. Williams, W. Daehn, M. Gruetzner and C. W. Starke, Aliasing errors in signature analysis registers, IEEE Design and Test of Computers 4(2), 39 to 45, April 1987"
    title: T. W. Williams, W. Daehn, M. Gruetzner and C. W. Starke, Aliasing errors in signature analysis registers, IEEE Design and Test of Computers 4(2), 39 to 45, April 1987
    locator: the first account of aliasing under the independent error model
  - book: isbn:9780471624639
    title: Paul H. Bardell, William H. McAnney and Jacob Savir, Built-In Test for VLSI, Pseudorandom Techniques, Wiley-Interscience, 1987
    locator: the chapter Test Response Compression Techniques (aliasing of signature registers under several error models)
---

This theorem says how often a signature register misses an error. A $k$-bit [multiple-input signature register](/multiple-input-signature-register/) maps a faulty response to the good signature exactly when the error polynomial is a multiple of its feedback polynomial $q$. Under two random models of the error, the chance of this tends to $2^{-k}$ for long tests: the model in which every nonzero error stream is equally likely, and the model in which every response bit is wrong with probability $p$, independently. The second limit holds for every $q$ with the term 1, primitive or not. The theorem also shows where the number stops being true: errors made by real faults are not random, and some of them alias with probability 1.

## Statement

Use the notation of the MISR page. The register has $k \ge 1$ stages and the feedback polynomial $q$ of degree $k$ over GF(2), with $q_0 = 1$. A test of $m$ clocks gives the error words $e_0, \ldots, e_{m-1}$ (the faulty words minus the good words), and the error polynomial is $E = \sum_t x^{m-1-t} e_t$. By the MISR page, the faulty chip passes exactly when $q \mid E$. Say that the test **aliases** when $E \ne 0$ and $q \mid E$, and let $P_m$ be the probability of this. A single-input register (SISR) is the case where each error word is 0 or 1, the constant polynomial, entering stage 0.

**Theorem.**

1. **Equally likely streams.** For every $q$ of degree $k$ and every $m \ge 1$, exactly $2^{(m-1)k} - 1$ of the $2^{mk} - 1$ nonzero error streams of a $k$-input MISR alias. If every nonzero stream is equally likely,
$$P_m = \frac{2^{(m-1)k} - 1}{2^{mk} - 1} < 2^{-k}, \qquad P_m \to 2^{-k}.$$
For a SISR and $m \ge k$ the count is $2^{m-k} - 1$ of $2^m - 1$.
2. **Independent bit errors.** Let every error bit be 1 with probability $p$, $0 < p < 1$, independently of all others. Then for a MISR and for a SISR, $P_m \to 2^{-k}$ as $m \to \infty$, for every $q$ with $q_0 = 1$. For a MISR, with $\delta = \min(p, 1-p)^k$,
$$\big| P_m + (1 - p)^{mk} - 2^{-k} \big| \le (1 - 2^k \delta)^m.$$
For $p = 1/2$ the error state is uniform after one clock of a MISR and after $k$ clocks of a SISR, so $P_m = 2^{-k} - 2^{-mk}$ for $m \ge 1$ (MISR) and $P_m = 2^{-k} - 2^{-m}$ for $m \ge k$ (SISR).
3. **Structured errors.** The limit is not a bound for a given fault. In a MISR, an error on input $i$ at clock $t$ together with one on input $i + 1$ at clock $t + 1$ aliases for every $q$. In a SISR with a primitive $q$ of degree $k \ge 2$, the error that inverts every bit of the stream aliases exactly when $2^k - 1$ divides $m$.

## In plain words

At the end of a test, the signature register holds a short code. A bad chip passes only if its errors happen to give the same code as a good chip.

If the errors look random, every one of the possible codes is about equally likely at the end, so the chance of the one good code is about one in two to the power of the length of the register. With 32 bits that is about one in four billion. This holds whether each bit is wrong half the time or rarely, as long as the test is long and the wrong bits do not depend on each other.

But a real fault does not make random errors. It can make the same error again and again, or errors that cancel in the register, and then the bad chip passes every time.

## Proof

**Part 1.** The map $\Phi : (e_0, \ldots, e_{m-1}) \mapsto E \bmod q$ from $mk$ bits to $k$ bits is linear over GF(2). It is onto, since the last word enters with $x^0$: for any $r$ of degree less than $k$, the stream $(0, \ldots, 0, r)$ maps to $r$. So its kernel has $2^{mk - k}$ elements, and the nonzero ones, $2^{(m-1)k} - 1$ of them, are the aliasing streams. Then $P_m < 2^{-k}$ because $2^k (2^{(m-1)k} - 1) = 2^{mk} - 2^k < 2^{mk} - 1$, and $P_m \to 2^{-k}$ because $P_m = 2^{-k} (1 - 2^{-(m-1)k}) / (1 - 2^{-mk})$. The SISR case is the same count with $m$ one-bit words and the map onto when $m \ge k$, as on the [built-in self-test](/built-in-self-test/) page. No property of $q$ is used.

**Part 2.** Let $s_t = \big(\sum_{u < t} x^{t-1-u} e_u\big) \bmod q$ be the error state after $t$ clocks, the register of a MISR that starts at 0 and is fed only with the errors. By the MISR page, $s_{t+1} = (x\,s_t + e_t) \bmod q$, and $s_m = E \bmod q$. The words $e_t$ are independent of each other, so $(s_t)$ is a [Markov chain](/markov-chain/) on the $N = 2^k$ polynomials of degree less than $k$, with
$$\Pr[s_{t+1} = b \mid s_t = a] = \pi_e\big(b - \varphi(a)\big), \qquad \varphi(a) = x\,a \bmod q,$$
where $\pi_e(c)$ is the probability that an error word equals $c$.

*The uniform law is stationary.* Since $q_0 = 1$, $x$ and $q$ have no common factor, so $\varphi$ is one to one on the $N$ states (if $x\,a \equiv x\,a' \pmod q$, then $q \mid x (a - a')$, so $q \mid a - a'$, so $a = a'$). Hence for a fixed $b$, the values $b - \varphi(a)$ run once over all states as $a$ does, and the column sum of the transition matrix is $\sum_a \pi_e(b - \varphi(a)) = \sum_c \pi_e(c) = 1$. The matrix is doubly stochastic, so the uniform law $(1/N, \ldots, 1/N)$ is a [stationary distribution](/stationary-distribution/).

*Convergence for a MISR.* Here $\pi_e(c) = p^{|c|} (1-p)^{k - |c|} \ge \delta$ for every $c$, where $|c|$ is the number of ones. So every entry of the matrix is at least $\delta$, and $N\delta \le 1$. Write the matrix as $N\delta\, U + (1 - N\delta)\, Q$, where every entry of $U$ is $1/N$. If $N\delta < 1$, the matrix $Q$ has entries at least 0 and rows that sum to 1. For two laws $\mu$ and $\nu$ on the states, $(\mu - \nu) U = 0$, so one step maps $\mu - \nu$ to $(1 - N\delta)(\mu - \nu) Q$, and $\|(\mu - \nu) Q\|_1 \le \|\mu - \nu\|_1$. With $\nu$ uniform and stationary, after $m$ steps $\|\mu_m - \nu\|_1 \le (1 - N\delta)^m \|\mu_0 - \nu\|_1 \le 2 (1 - N\delta)^m$. The entries of $\mu_m - \nu$ sum to 0, so each one is at most half the $\ell_1$ norm in absolute value, which gives $|\Pr[s_m = 0] - 2^{-k}| \le (1 - N\delta)^m$. If $N\delta = 1$, then $p = 1/2$, every $\pi_e(c) = 1/N$, and $s_1$ is already uniform.

*Convergence for a SISR.* Now $e_t \in \{0, 1\}$, so a single step does not reach every state. But after $k$ steps from $s_t = a$,
$$s_{t+k} = \Big(x^k a + \sum_{j=0}^{k-1} e_{t+j}\, x^{k-1-j}\Big) \bmod q,$$
and the sum is any polynomial of degree less than $k$, each one for exactly one choice of $(e_t, \ldots, e_{t+k-1})$, which has probability at least $\min(p, 1-p)^k = \delta$. So the $k$-step matrix has every entry at least $\delta$ and is again doubly stochastic, and the argument above gives $|\Pr[s_m = 0] - 2^{-k}| \le (1 - N\delta)^{\lfloor m/k \rfloor}$.

In both cases $\Pr[s_m = 0] \to 2^{-k}$. The test aliases when $s_m = 0$ and the stream is not all zero, so $P_m = \Pr[s_m = 0] - (1-p)^{n}$, where $n$ is the number of error bits, $mk$ or $m$, and $(1-p)^n \to 0$. This proves the limit and the bound. For $p = 1/2$ the state is exactly uniform after one clock of a MISR and after $k$ clocks of a SISR, which gives the two exact formulas.

**Part 3.** For the MISR pair, the error bit on input $i$ at clock $t$ gives the monomial $x^{m-1-t+i}$, and the one on input $i + 1$ at clock $t + 1$ gives $x^{m-1-(t+1)+(i+1)}$, the same monomial $x^a$. With only these two error bits, $E = x^a + x^a = 0$ although the stream is not zero, and $q \mid 0$. For the SISR, the stream of all ones gives $E = 1 + x + \cdots + x^{m-1}$, and $(x + 1) E = x^m + 1$. A primitive $q$ of degree $k \ge 2$ is irreducible and is not $x + 1$, so it has no common factor with $x + 1$, and $q \mid E$ exactly when $q \mid x^m + 1$. The least $n \ge 1$ with $q \mid x^n + 1$ is the order $2^k - 1$ of $x$ modulo $q$, and $q \mid x^m + 1$ exactly when this order divides $m$. $\blacksquare$

## Consequences

- **Choosing the length of the register.** Under either random model, a 16-bit register misses about one error in 65 536 and a 32-bit register about one in $4.3 \times 10^9$. Designers pick $k$ from this number and then check the faults that matter with fault simulation of the real signature.
- **Primitivity is not needed for the limit.** Part 2 needs only $q_0 = 1$, which makes the step $s \mapsto x\,s \bmod q$ one to one. Primitivity matters for the speed of convergence and for structured errors, as the next section shows.
- **Unbiased errors converge at once.** When $p = 1/2$, $P_m$ differs from $2^{-k}$ only by the chance $2^{-n}$ of an all-zero stream, from the first clock of a MISR and from clock $k$ of a SISR. For small $p$ the convergence can be slow, as the table under Tightness shows.
- **Linear codes.** The aliasing streams of Part 1 are the nonzero codewords of the [linear code](/linear-code/) that is the kernel of $\Phi$. The same count gives the miss rate of a [cyclic redundancy check](/cyclic-redundancy-check/) on random errors.
- **Space compactors.** An XOR network before the register adds its own cancellations: an error that cancels inside the network never reaches the register. The [X-compact](/x-compact/) design states which errors its network keeps.

## Tightness

- **The strict bound in Part 1 is the best constant.** $P_m < 2^{-k}$ for every $m$, and $P_m \to 2^{-k}$, so no smaller constant bounds all $m$.
- **Part 2 is a limit, not a bound.** For finite $m$, $P_m$ can be far above $2^{-k}$. Exact computation with the Markov chain for a 4-bit SISR ($2^{-4} = 0.0625$) gives these values.

| $q$ | $p$ | $P_{15}$ | $P_{60}$ | $P_{200}$ | largest $P_m$ for $m \le 200$ |
|---|---|---|---|---|---|
| $x^4 + x + 1$ (primitive) | 0.05 | 0.0028 | 0.0486 | 0.0625 | 0.0625, approached from below |
| $x^4 + x + 1$ (primitive) | 0.95 | 0.4661 | 0.0947 | 0.0625 | 0.4661 at $m = 15$ |
| $x^4 + x^2 + 1$ | 0.05 | 0.0177 | 0.0703 | 0.0628 | 0.0712 at $m = 69$ |
| $x^4 + 1$ | 0.05 | 0.0275 | 0.0861 | 0.0638 | 0.0862 at $m = 58$ |

With $p = 0.95$ nearly every bit is wrong, the stream is close to all ones, and at $m = 15 = 2^4 - 1$ Part 3 makes it alias with probability about $0.95^{15} \approx 0.46$. With $p = 0.05$ the non-primitive polynomials pass above $2^{-4}$ on the way to the limit, while $x^4 + x + 1$ stays below it up to $m = 200$.
- **The condition $q_0 = 1$ is needed.** For $q = x^k$ a SISR is a plain shift register that keeps only the last $k$ error bits, so $P_m \to (1 - p)^k$ under independent errors, which is far above $2^{-k}$ when $p$ is small.
- **Independence is needed.** Part 3 gives faults whose aliasing probability is 1 for every $m$ (the MISR pair) or for every multiple of $2^k - 1$ (the SISR with all bits inverted).

## History

Smith (1980) counted the aliasing streams under the model in which every nonzero error stream is equally likely, which gives Part 1. Williams, Daehn, Gruetzner and Starke (1987, 1988) replaced it by the model of independent bit errors with probability $p$, wrote the error state as a Markov chain, and studied the limit and the transient for primitive and non-primitive polynomials. The bound with $\delta$ in Part 2 is the standard Doeblin argument for a chain whose transition probabilities are all positive, written here for this chain. The cancellation of errors in neighbor stages of a MISR follows from the description of the register as polynomial division.

## References
