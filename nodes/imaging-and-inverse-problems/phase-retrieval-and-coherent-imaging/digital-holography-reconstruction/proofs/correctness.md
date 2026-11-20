---
title: Off-axis reconstruction is exact when the sidebands separate
proves: [correctness]
status: full
---

The setting is that of the algorithm. Images are $n_1 \times n_2$ arrays on a periodic grid with spacing $d$. For an array $x$, $\hat x = F x$ is its unnormalized 2D DFT, and an index $k = (k_1, k_2)$ is read as its signed value $\bar k$ with $-n_a/2 \le \bar k_a < n_a/2$. Index arithmetic is modulo $(n_1, n_2)$. For an integer $B \ge 0$ and an index $c$, let

$$Q_B(c) = \{k : |\overline{k - c}_1| \le B \text{ and } |\overline{k - c}_2| \le B\},$$

the square of half-width $B$ around $c$. A field $O$ on the sensor is *band-limited to* $B$ if $\hat O$ is zero outside $Q_B(0)$. The reference is the tilted plane wave $R_{ij} = r\, e^{2\pi i (c_1 i/n_1 + c_2 j/n_2)}$ with $r > 0$ and an integer carrier $c$, and the hologram is $h = |R + O|^2$.

**Lemma 1 (the four terms).** $h = r^2 + |O|^2 + \overline{R} O + R \overline{O}$, and for $O$ band-limited to $B$:

1. $\widehat{r^2}$ is zero outside $\{0\}$;
2. $\widehat{|O|^2}$ is zero outside $Q_{2B}(0)$;
3. $\widehat{\overline{R} O}(k) = r\, \hat O(k + c)$, which is zero outside $Q_B(-c)$;
4. $\widehat{R \overline{O}}(k) = r\, \overline{\hat O(c - k)}$, which is zero outside $Q_B(c)$.

*Proof.* The expansion is $|R + O|^2 = (R + O)\overline{(R + O)}$ with $|R|^2 = r^2$. Item 1: the DFT of a constant is zero except at index $0$. Item 2: the DFT of a pixelwise product is the cyclic convolution of the DFTs divided by $n_1 n_2$, and the DFT of $\overline{O}$ at $k$ is $\overline{\hat O(-k)}$; so $\widehat{|O|^2}(k) = (n_1 n_2)^{-1} \sum_q \hat O(q)\, \overline{\hat O(q - k)}$, and a nonzero term needs $q \in Q_B(0)$ and $q - k \in Q_B(0)$, so $k \in Q_{2B}(0)$. Item 3: multiplying by $e^{-2\pi i (c_1 i/n_1 + c_2 j/n_2)}$ moves the DFT by $-c$. Item 4: the same with $+c$ and $\overline{O}$. $\square$

**Lemma 2 (separation).** Suppose that for one axis $a$,

$$3B < |c_a| \quad \text{and} \quad |c_a| + B < n_a/2. \tag{S}$$

Then $Q_B(-c)$ is disjoint from $\{0\}$, $Q_{2B}(0)$ and $Q_B(c)$.

*Proof.* Take $c_a > 0$; the other case is the mirror image. By (S), $4B < n_a/2$, so the integers in $[-c_a - B, -c_a + B]$, in $[-2B, 2B]$ and in $[c_a - B, c_a + B]$ all lie in $[-n_a/2, n_a/2)$, where the signed value of an index is unique. The first interval ends at $-c_a + B < -2B$, so it is disjoint from the second. The third starts at $c_a - B > 2B > -c_a + B$, so it is disjoint from the first. Along axis $a$ the three other sets lie in $[-2B, c_a + B]$, and $Q_B(-c)$ lies in $[-c_a - B, -c_a + B]$, which is disjoint from it. Two sets whose coordinates along one axis are disjoint are disjoint. $\square$

**Theorem.** Let $O$ be band-limited to $B$ and let (S) hold. Then lines L1 to L4 compute the array $S$ with $S = \hat O$, and the output of line L6 is $P_{-z} O$, where $P_{-z}$ is angular spectrum propagation by $-z$ with evanescent waves dropped. If moreover $O = P_z O_0$ for a field $O_0$ in the object plane that is band-limited to $B$, and every frequency in $Q_B(0)$ propagates, then the output is $O_0$.

*Proof.* Line L1 gives $\hat h$, the sum of the four DFTs of Lemma 1. Lines L2 to L4 set, for $k \in Q_B(0)$, $S(k) = \hat h(k - c)/r$, and $S(k) = 0$ otherwise. For $k \in Q_B(0)$, the index $k - c$ lies in $Q_B(-c)$, where by Lemma 2 only the third term of Lemma 1 is nonzero. So $S(k) = \hat O(k - c + c) = \hat O(k)$. For $k \notin Q_B(0)$, $S(k) = 0 = \hat O(k)$ because $O$ is band-limited. Line L5 multiplies by the transfer function of $-z$ and line L6 inverts the DFT, which is $P_{-z} O$ by the definition of the [angular spectrum method](/angular-spectrum-method/). For the last claim, $P_{-z} P_z$ keeps the propagating frequencies and deletes the rest, so it is the identity on fields whose spectrum lies in the propagating set. $\square$

**Corollary 1 (noise).** If the recorded hologram is $h + e$ with any real noise $e$, the output changes by $W e$, where $\|W e\| \le \|e\|/r$ in the Euclidean norm of the samples.

*Proof.* Every line is linear in the hologram, so the change is the output for the input $e$. In the DFT basis that output keeps the entries of $\hat e$ in $Q_B(-c)$, moves them, divides by $r$ and multiplies by numbers of modulus at most $1$. With the [Parseval theorem](/parseval-theorem/), $\|W e\|^2 = (n_1 n_2)^{-1} \sum |\text{entries}|^2 \le (n_1 n_2)^{-1} \sum_k |\hat e(k)|^2 / r^2 = \|e\|^2/r^2$. $\square$

Only the fraction of the noise energy inside the window passes. For white noise this fraction is about $|Q_B(-c)|/(n_1 n_2)$, so the filter also removes most of the noise; this is a statement about averages, not a bound for every $e$.

**Corollary 2 (the in-line case and the twin).** For $c = 0$ the separation fails. If the whole spectrum of $(h - r^2)/r$ is propagated by $-z$, with $O = P_z O_0$, the result is

$$P_{-z} \frac{h - r^2}{r} = O_0 + P_{-z} \overline{P_z O_0} + \frac{1}{r} P_{-z} |O|^2.$$

The second term, the twin image, has the same energy as $O_0$ on the propagating band, and it is the wave $\overline{O_0}$ propagated by $-2z$: $P_{2z}$ applied to it gives $\overline{O_0}$ when every frequency of $\overline{O_0}$ propagates.

*Proof.* With $c = 0$, $R = r$, so $(h - r^2)/r = O + \overline{O} + |O|^2/r$. Apply $P_{-z}$ and use $P_{-z} O = P_{-z} P_z O_0 = O_0$. The DFT of $\overline{P_z O_0}$ at $k$ is $\overline{H_z(-k)\, \hat O_0(-k)}$, and $\overline{H_z(-k)} = H_{-z}(k)$ on propagating frequencies, because $H_z$ depends on $|f|$ only and has modulus $1$ there. So $\overline{P_z O_0} = P_{-z} \overline{O_0}$, the twin term is $P_{-2z} \overline{O_0}$, and $P_{2z}$ of it is $\overline{O_0}$. The energy statement follows from $|H| = 1$ and the Parseval theorem. $\square$

So in an in-line hologram the twin is a defocused copy of the conjugate object, which lies on the reconstruction at full energy. The off-axis carrier moves it to a different place in Fourier space, where the window of line L3 removes it.
