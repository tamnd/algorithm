---
tag: 53AB3R
kind: definition
slug: locally-decodable-codes
name: Locally decodable codes
aliases:
- LDC
- locally decodable code
- q-query locally decodable code
area: compression-and-coding/error-correcting-codes
level: research
summary: "Codes in which any one message symbol can be recovered with good probability from a few random queries to a codeword, even after a constant fraction of it is corrupted."
history:
  year: 2000
  people: [Jonathan Katz, Luca Trevisan]
  note: Katz and Trevisan defined locally decodable codes and proved the first lower bounds at STOC 2000. Local decoding of the Hadamard and Reed-Muller codes is older and comes from program checking and self-correction.
prereqs: [hadamard-code, reed-muller-code]
see_also: [private-information-retrieval, pcp-theorem, linearity-test, low-degree-test, schwartz-zippel-lemma, list-decoding, union-bound, minimum-distance]
sources:
  - paper: doi:10.1145/335305.335315
    title: Jonathan Katz and Luca Trevisan, On the efficiency of local decoding procedures for error-correcting codes, Proceedings of the 32nd ACM Symposium on Theory of Computing (STOC), 2000, pages 80 to 86
    locator: The definition of (q, δ, ε) locally decodable codes and of smooth codes, the reduction from local decoding to smooth codes, the lower bound on the length of q-query codes, and the relation to private information retrieval
  - paper: doi:10.1016/j.jcss.2004.04.007
    title: Iordanis Kerenidis and Ronald de Wolf, Exponential lower bound for 2-query locally decodable codes via a quantum argument, Journal of Computer and System Sciences 69(3), 2004, pages 395 to 420 (STOC 2003)
    locator: The main theorem (a binary 2-query LDC has length 2^(Ω(k)))
  - paper: doi:10.1145/1326554.1326555
    title: Sergey Yekhanin, Towards 3-query locally decodable codes of subexponential length, Journal of the ACM 55(1), 2008, pages 1 to 16
    locator: The 3-query construction from a large Mersenne prime, and the bound that holds if there are infinitely many Mersenne primes
  - paper: doi:10.1137/090772721
    title: Klim Efremenko, 3-query locally decodable codes of subexponential length, SIAM Journal on Computing 41(6), 2012, pages 1694 to 1703 (STOC 2009)
    locator: The unconditional 3-query construction from matching vector families, and the 2^r-query generalization
  - paper: "Sergey Yekhanin, Locally Decodable Codes, Foundations and Trends in Theoretical Computer Science, 2012"
    title: Locally Decodable Codes
    locator: The survey chapters on Reed-Muller codes, matching vector codes, lower bounds and applications
---

A locally decodable code lets a reader recover one symbol of the message by looking at only a few positions of the codeword, chosen at random, even when an adversary has corrupted a constant fraction of the codeword. Ordinary decoding reads the whole codeword. Local decoding reads a constant number of positions, or a number that grows very slowly, so the codeword can be huge. The price is length: with a constant number of queries, every known code is longer than any polynomial in the message length. Katz and Trevisan defined these codes in 2000.

## Definition

**Notation.** A code is a map $C : \Sigma^k \to \Gamma^n$. The relative distance between two words $w, w' \in \Gamma^n$ is the fraction of positions where they differ. A decoder has *oracle access* to $w$: it asks for single positions $w_j$, and each asked position is a *query*.

**Definition (Katz and Trevisan 2000).** $C$ is a $(q, \delta, \varepsilon)$ *locally decodable code* if there is a randomized algorithm $D$ such that, for every message $x \in \Sigma^k$, every index $i \in \{1, \ldots, k\}$ and every word $w$ within relative distance $\delta$ of $C(x)$:

1. $D^{w}(i)$ makes at most $q$ queries to $w$;
2. $\Pr[D^{w}(i) = x_i] \ge 1/2 + \varepsilon$ for binary messages (in general, at least a constant above $1/|\Sigma|$).

The probability is over the random choices of $D$ only; the corruption is worst case. Repeating the decoder and taking the majority makes the success probability as close to 1 as needed, with more queries.

**Smooth codes.** A decoder is *smooth* if each of its queries, taken alone, is close to uniform over the $n$ positions. If every query is uniform and the decoder is right on an uncorrupted codeword, then by the [union bound](/union-bound/) it is right on a word with a fraction $\delta$ of corrupted positions with probability at least $1 - q\delta$. Katz and Trevisan showed the converse in spirit: every LDC gives a smooth code with similar parameters. Smoothness is the property behind the lower bounds and the link to private information retrieval.

**The Hadamard code: 2 queries.** The [Hadamard code](/hadamard-code/) maps $x \in \{0,1\}^k$ to the $n = 2^k$ bits $C(x)_a = \langle x, a \rangle \bmod 2$, one for each $a \in \{0,1\}^k$. Since $\langle x, a \rangle \oplus \langle x, a \oplus e_i \rangle = x_i$, the decoder for $x_i$ chooses $a$ uniformly, queries $w_a$ and $w_{a \oplus e_i}$, and returns their XOR. Each query alone is uniform, so with a fraction $\delta$ corrupted, both are right with probability at least $1 - 2\delta$, and then the answer is right. So this is a $(2, \delta, 1/2 - 2\delta)$ LDC for every $\delta < 1/4$. Its length is exponential in $k$.

**Reed-Muller codes: $r + 1$ queries.** A message is a polynomial $f$ over $\mathrm{GF}(p)$ in $m$ variables of total degree at most $r$, with $r + 1 < p$; the codeword lists $f$ on all of $\mathrm{GF}(p)^m$. To recover $f(x)$, choose a nonzero direction $y$ at random and query $w$ at $x + t y$ for $t = 1, \ldots, r + 1$. The restriction $t \mapsto f(x + ty)$ is a polynomial of degree at most $r$ in one variable, so Lagrange interpolation at $t = 0$ gives $f(x)$ when the queries are right. Each query is uniform over the points other than $x$, so the decoder succeeds with probability at least $1 - (r+1)\delta'$, with $\delta'$ slightly above $\delta$. The message symbols are the values of $f$ at a fixed set of points (or its coefficients, recovered from such values). The choice of parameters gives a range of tradeoffs:

- a fixed number of queries $q = r + 1$ with length $n = \exp(O(k^{1/(q-1)}))$;
- $m$ near $\log k / \log \log k$ and $r$ a fixed power of $\log k$, which gives polylogarithmic queries with polynomial length. With $m$ and $r$ both near $\log k$, the length is $k^{\Theta(\log \log k)}$, which is not polynomial.

**Matching vector codes: 3 queries.** Yekhanin (2008) built 3-query LDCs of subexponential length from a large Mersenne prime. If there are infinitely many Mersenne primes his length is $\exp(\exp(O(\log k / \log \log k)))$ for infinitely many $k$. Efremenko (2009) removed the number theory: his codes, built from matching vector families, have 3 queries and length $\exp(\exp(O(\sqrt{\log k \log\log k})))$ for all $k$, and $2^r$ queries give a still shorter length.

**Lower bounds.**

- Katz and Trevisan proved that a $q$-query LDC has length at least about $k^{q/(q-1)}$, so no constant-query LDC is linear in length, and 1-query LDCs do not exist for large $k$.
- Goldreich, Karloff, Schulman and Trevisan (2002) proved that *linear* 2-query LDCs have length $2^{\Omega(k)}$.
- Kerenidis and de Wolf (2003) proved $2^{\Omega(k)}$ for every binary 2-query LDC, with a quantum argument. So the Hadamard code is optimal for 2 queries up to the constant in the exponent.
- For 3 queries the gap is wide: the best lower bounds are polynomial, near $k^3$ (Alrabiah, Guruswami, Kothari and Manohar 2023), and the best codes are subexponential.

**Two different ideas with similar names.**

*Locally testable codes.* A locally testable code has a tester that reads a few positions of a word, always accepts a codeword, and rejects with good probability a word that is far from every codeword. It decides membership; it does not recover the message. The Hadamard code is locally testable by the [linearity test](/linearity-test/) of Blum, Luby and Rubinfeld, and Reed-Muller codes by the [low-degree test](/low-degree-test/). Local testing is a central part of [PCP](/pcp-theorem/) constructions.

*Locally recoverable codes.* In a locally recoverable code (also called a code with locality $r$), each codeword symbol is a fixed function of at most $r$ other symbols. It is designed for distributed storage: one lost disk is rebuilt by reading $r$ others, not $k$. The model is a single erasure at a known place, and the repair reads a fixed set; an LDC instead survives a constant fraction of adversarial errors and needs randomness. Gopalan, Huang, Simitci and Yekhanin (2012) proved $d \le n - k - \lceil k/r \rceil + 2$ for such codes, and Microsoft Azure storage uses them.

## Examples and non-examples

**The Hadamard code for $k = 4$.** For $x = 0101$ ($x_0 = 1$, $x_2 = 1$), the 16 bits $C(x)_a$ for $a = 0, \ldots, 15$ are 0101 1010 0101 1010. To decode $x_1$ with $a = 5$, read $C(x)_5 = 0$ and $C(x)_{5 \oplus 2} = C(x)_7 = 0$; the XOR is $0 = x_1$. If an adversary flipped position 7, this choice of $a$ gives the wrong answer, but only the 2 of the 16 choices of $a$ that touch position 7 are spoiled.

**Measured with $k = 8$.** With 25 of the 256 positions flipped at random ($\delta \approx 0.098$, so $1 - 2\delta \approx 0.805$), the exact success probabilities of the 8 bit decoders, over all 256 choices of $a$, range from 0.805 to 0.836. The bound is tight: if all corrupted positions have $a_i = 0$, the sets of corrupted $a$ and $a \oplus e_i$ do not meet, and the decoder for $x_i$ succeeds with probability exactly $1 - 2\delta$. At $\delta = 1/4$ this corruption leaves the decoder for $x_i$ at $1/2$, a coin toss. With $\delta \approx 0.098$, a majority of 31 local decodings for each bit recovered the whole message in all 10 tests. The Reed-Muller line decoder with $p = 13$, $m = 2$, $r = 3$ (4 queries, $n = 169$) met its bound $1 - 4\delta'$ at every tested point.

**Non-example: a Reed-Solomon code.** A [Reed-Solomon code](/reed-solomon-code/) of dimension $k$ is a polynomial of degree less than $k$ evaluated at $n$ points. The value at a new point depends on all $k$ coefficients, and any $k - 1$ positions say nothing about it. So a decoder needs at least $k$ queries: the code has good distance and rate but no locality. Reed-Muller codes gain locality by using many variables and low degree.

**Non-example: a repetition code.** Repeat $x$ in full $t$ times. To read $x_i$ one can query its $t$ copies and take the majority, so the query count is $t$. But the adversary can corrupt all copies of $x_i$ with a fraction of only $1/k$ of the positions. The code fails as soon as $\delta \ge 1/k$, so it is not an LDC for any constant $\delta$.

## Related definitions

- [Hadamard code](/hadamard-code/) and [Reed-Muller code](/reed-muller-code/): the classical LDCs. They are also *locally correctable*: any codeword symbol, not just a message symbol, can be recovered locally.
- [Private information retrieval](/private-information-retrieval/): a smooth $q$-query LDC gives a $q$-server PIR scheme in which each server sees one uniform query, and the converse also holds (Katz and Trevisan 2000).
- [PCP theorem](/pcp-theorem/): proofs are encoded with locally testable and locally decodable codes, and checked with a few queries.
- [Linearity test](/linearity-test/) and [low-degree test](/low-degree-test/): the local testers of the Hadamard and Reed-Muller codes.
- [Schwartz-Zippel lemma](/schwartz-zippel-lemma/): the bound on roots of low-degree polynomials behind the distance of Reed-Muller codes.
- [List decoding](/list-decoding/): local list decoding of the Hadamard code is the Goldreich-Levin algorithm, which works beyond $\delta = 1/4$.

## References

- Jonathan Katz and Luca Trevisan, "On the efficiency of local decoding procedures for error-correcting codes", STOC 2000, pages 80 to 86.
- Iordanis Kerenidis and Ronald de Wolf, "Exponential lower bound for 2-query locally decodable codes via a quantum argument", STOC 2003; Journal of Computer and System Sciences 69(3), 2004.
- Sergey Yekhanin, "Towards 3-query locally decodable codes of subexponential length", Journal of the ACM 55(1), 2008.
- Klim Efremenko, "3-query locally decodable codes of subexponential length", STOC 2009; SIAM Journal on Computing 41(6), 2012.
- Oded Goldreich, Howard Karloff, Leonard J. Schulman and Luca Trevisan, "Lower bounds for linear locally decodable codes and private information retrieval", Computational Complexity 15(3), 2006 (CCC 2002).
- Sergey Yekhanin, Locally Decodable Codes, Foundations and Trends in Theoretical Computer Science, 2012.
