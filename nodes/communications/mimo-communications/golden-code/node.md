---
tag: MAAV3W
kind: definition
slug: golden-code
name: Golden code
aliases:
- golden space-time code
area: communications/mimo-communications
level: advanced
summary: A full-rate full-diversity 2x2 space-time code from cyclic division algebras with a nonvanishing determinant.
prereqs: [rank-and-determinant-criteria, diversity-multiplexing-tradeoff, lattice, orthogonal-space-time-block-codes]
see_also: [alamouti-code, space-time-trellis-codes, spatial-multiplexing, mimo-detection, fincke-pohst-enumeration, closest-vector-problem, quadrature-amplitude-modulation, mimo-capacity]
sources:
  - paper: doi:10.1109/TIT.2005.844069
    title: "Jean-Claude Belfiore, Ghaya Rekaya and Emanuele Viterbo, The golden code - a 2 x 2 full-rate space-time code with nonvanishing determinants, IEEE Transactions on Information Theory 51(4), 1432-1436, 2005"
    locator: "the construction from the golden number, the cyclic division algebra over Q(i), the minimum determinant 1/5 and the comparison with earlier 2 x 2 codes"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: Section 9.2.4 (universal code design for MIMO channels and the role of the determinant)
---

The golden code is a space-time block code for two transmit antennas that sends four QAM symbols in two time slots, so it has full rate on a $2 \times 2$ channel, and every pair of codewords differs by a full-rank matrix, so it has full diversity. Its main property is a **nonvanishing determinant**: the smallest $|\det X|^2$ over nonzero Gaussian integer symbols is $1/5$, so the smallest $|\det \Delta|^2$ over codeword differences is $16/5$ for unnormalized QAM of every size. By the [rank and determinant criteria](/rank-and-determinant-criteria/), this keeps the coding gain from falling as the constellation grows, and it makes the code reach the optimal [diversity-multiplexing tradeoff](/diversity-multiplexing-tradeoff/) of the $2 \times 2$ channel. The [Alamouti code](/alamouti-code/) and other [orthogonal space-time block codes](/orthogonal-space-time-block-codes/) are the close alternatives: they decode one symbol at a time but send only one symbol per slot. [Space-time trellis codes](/space-time-trellis-codes/) also send one symbol per slot.

## Definition

Let $\theta = (1 + \sqrt5)/2$, the golden number, and $\bar\theta = (1 - \sqrt5)/2$, its conjugate, so that $\theta + \bar\theta = 1$ and $\theta \bar\theta = -1$. Let $\alpha = 1 + j - j\theta$ and $\bar\alpha = 1 + j - j\bar\theta$. Then $|\alpha|^2 = 1.381966$, $|\bar\alpha|^2 = 3.618034$, $|\alpha|^2 + |\bar\alpha|^2 = 5$, and $\alpha \bar\alpha = 2 + j$.

The **golden code** maps four symbols $a, b, c, d$ from a QAM constellation, taken as a subset of the Gaussian integers $\mathbb{Z}[j]$, to the $2 \times 2$ codeword

$$X = \frac{1}{\sqrt5} \begin{pmatrix} \alpha (a + b\theta) & \alpha (c + d\theta) \\ j \bar\alpha (c + d\bar\theta) & \bar\alpha (a + b\bar\theta) \end{pmatrix},$$

with rows for antennas and columns for time slots. It sends 4 symbols in 2 slots, the rate of [spatial multiplexing](/spatial-multiplexing/) on two antennas.

**Unitary shaping (a closed form).** The map $(a, b) \mapsto \frac{1}{\sqrt5}(\alpha(a + b\theta), \bar\alpha(a + b\bar\theta))$ has orthonormal columns: the column norms are $(|\alpha|^2 + |\bar\alpha|^2)/5 = 1$ and $(|\alpha|^2 \theta^2 + |\bar\alpha|^2 \bar\theta^2)/5 = 1$, and the inner product is $(|\alpha|^2 \theta + |\bar\alpha|^2 \bar\theta)/5 = 0$. The same holds for $(c, d)$. So $\|X\|_F^2 = |a|^2 + |b|^2 + |c|^2 + |d|^2$, the code is a rotated copy of the lattice $\mathbb{Z}[j]^4$, and with unit-energy symbols $\mathbb{E}\|X\|_F^2 = 4$, one unit per antenna per slot.

**The determinant (a closed form).** From $\theta + \bar\theta = 1$ and $\theta\bar\theta = -1$, $(x + y\theta)(x + y\bar\theta) = x^2 + xy - y^2$. So

$$\det X = \frac{2 + j}{5}\, u, \qquad u = (a^2 + ab - b^2) - j\,(c^2 + cd - d^2) \in \mathbb{Z}[j].$$

**Nonvanishing determinant (a theorem of Belfiore, Rekaya and Viterbo).** The matrices of this form are the elements of a cyclic division algebra over $\mathbb{Q}(j)$, built from the field $\mathbb{Q}(j, \sqrt5)$ with $j$ as the non-norm element. In a division algebra, every nonzero element is invertible, so $u \ne 0$ when $(a, b, c, d) \ne 0$. Since $u$ is a nonzero Gaussian integer, $|u|^2 \ge 1$, and

$$\min_{(a, b, c, d) \in \mathbb{Z}[j]^4 \setminus 0} |\det X|^2 = \frac{|2 + j|^2}{25} = \frac{1}{5},$$

reached at $a = 1$, $b = c = d = 0$, where $\det X = (2 + j)/5$. The code is linear, so the difference of two codewords is the codeword of the symbol differences, and the same bound holds for every $\Delta$.

## Examples and non-examples

**A codeword.** For $(a, b, c, d) = (1 + j, 1 - j, -1 + j, -1 - j)$, the four 4-QAM points,

$$X = \begin{pmatrix} 1 - j & -1.3416 + 0.4472j \\ -0.4472 - 1.3416j & -1 + j \end{pmatrix}, \qquad \det X = -1.2 + 0.4j,$$

and $\|X\|_F^2 = 8 = \sum |s_k|^2$. From the closed form, $u = (2 + 4j) - j(2 - 4j) = -2 + 2j$ and $(2 + j)(-2 + 2j)/5 = -1.2 + 0.4j$.

**4-QAM differences.** Differences of points of $\{\pm 1 \pm j\}$ are 0, $\pm 2$, $\pm 2j$ or $\pm 2 \pm 2j$, all in $2\mathbb{Z}[j]$. Scaling the four symbols by 2 scales $\det X$ by 4, so the minimum $|\det \Delta|^2$ over 4-QAM is $16/5 = 3.2$. With unit-energy 4-QAM, where the points are divided by $\sqrt2$, it is $0.8$. For 16-QAM and larger, the unnormalized minimum stays at $3.2$: this is the nonvanishing determinant.

**Non-example: spatial multiplexing.** Sending $a$ and $b$ on the two antennas in slot 1 and $c$ and $d$ in slot 2 also has rate 2, but a difference in $a$ alone gives a $\Delta$ of rank one, so the diversity is only $N_r$.

**Non-example: Alamouti.** The [Alamouti code](/alamouti-code/) has $|\det \Delta|^2 = (|e_1|^2 + |e_2|^2)^2$, which never vanishes, but it sends only 2 symbols in 2 slots.

**Non-example: a code with a vanishing determinant.** Take the same matrix form with $\theta$ replaced by a transcendental number. Each fixed QAM is then full rank, but there is no algebraic lower bound, and the minimum determinant can tend to 0 as the constellation grows. Such a code can have full diversity at a fixed rate and still miss the optimal tradeoff.

## Related definitions

- **Decoding.** The receiver sees $\mathrm{vec}(Y) = G\, (a, b, c, d)^T + \mathrm{vec}(W)$ with a $2N_r \times 4$ complex matrix $G$ that depends on $H$. Maximum likelihood decoding is a [closest vector problem](/closest-vector-problem/) in 8 real dimensions, solved in practice by sphere decoding ([Fincke-Pohst enumeration](/fincke-pohst-enumeration/)); exhaustive search costs $M^4$ metric evaluations for $M$-QAM. This is the general [MIMO detection](/mimo-detection/) problem, with no decoupling as in an OSTBC.
- **Diversity-multiplexing tradeoff.** Elia and coauthors showed in 2006 that a full-rate code with a nonvanishing determinant and $T = N_t$ reaches the optimal tradeoff for every $N_r$. The golden code meets these conditions for $N_t = 2$, so it reaches $d^*(r)$ of the $2 \times N_r$ channel.
- **Perfect space-time codes.** Oggier, Rekaya, Belfiore and Viterbo extended the construction to codes for 2, 3, 4 and 6 antennas from cyclic division algebras, with full rate, nonvanishing determinant, and a unitary shaping like the one above.
- **Cyclic division algebra.** For a cyclic extension $L/K$ of degree $n$ with Galois generator $\sigma$ and an element $\gamma \in K$ such that no power $\gamma^k$, $0 < k < n$, is a norm from $L$, the matrices built from $x_0, \ldots, x_{n-1} \in L$ with $\gamma \sigma(\cdot)$ below the diagonal form a division algebra. For the golden code, $n = 2$, $L = \mathbb{Q}(j, \sqrt5)$, $K = \mathbb{Q}(j)$, $\sigma$ sends $\sqrt5$ to $-\sqrt5$, and $\gamma = j$.

## References
