---
tag: PW3Y2B
kind: theorem
slug: laurent-decomposition
name: Laurent decomposition
aliases:
- Laurent representation of CPM
area: communications/modulation-and-detection
level: advanced
summary: Any binary CPM signal with a non-integer modulation index is an exact sum of 2^(L-1) linearly modulated PAM signals, so linear receivers can be built for it.
prereqs: [continuous-phase-modulation, pulse-amplitude-modulation]
see_also: [continuous-phase-modulation, minimum-shift-keying, gaussian-minimum-shift-keying, offset-qpsk, maximum-likelihood-sequence-estimation, viterbi-equalizer, reduced-state-sequence-estimation, matched-filter]
sources:
  - paper: doi:10.1109/TCOM.1986.1096504
    title: Pierre A. Laurent, Exact and approximate construction of digital phase modulations by superposition of amplitude modulated pulses (AMP), IEEE Transactions on Communications 34(2), 150-160, 1986
    locator: the exact decomposition of binary CPM into 2^(L-1) PAM components, the pulses c_k and the pseudo-symbols, and the approximation by the main pulse
  - paper: doi:10.1109/18.412675
    title: Umberto Mengali and Michele Morelli, Decomposition of M-ary CPM signals into PAM waveforms, IEEE Transactions on Information Theory 41(5), 1265-1275, 1995
    locator: the extension to M = 2^P levels with (2^P - 1) 2^(P(L-1)) pulses, for a modulation index that is not an integer
  - book: isbn:9780306421952
    title: John B. Anderson, Tor Aulin and Carl-Erik Sundberg, Digital Phase Modulation, Plenum Press, 1986
    locator: the CPM signal model and the phase pulse used in the statement
---

The Laurent decomposition writes a binary [continuous phase modulation](/continuous-phase-modulation/) signal as an exact, finite sum of linearly modulated pulse trains, like [PAM](/pulse-amplitude-modulation/) signals. A CPM signal is a nonlinear function of the data, since the data sits in the exponent. The theorem shows that it is still linear in a set of derived symbols, the pseudo-symbols. For a frequency pulse of $L$ symbols there are $2^{L-1}$ pulse trains, and in the usual cases the first one carries almost all the energy. So a receiver for [MSK](/minimum-shift-keying/) or [GMSK](/gaussian-minimum-shift-keying/) can use one matched filter and a small trellis instead of the full CPM receiver. Laurent proved the binary case in 1986; Mengali and Morelli extended it to $M$-ary CPM in 1995.

## Statement

**Signal model.** Let $T > 0$ be the symbol period, $L \ge 1$ an integer and $q$ a phase pulse with $q(t) = 0$ for $t \le 0$ and $q(t) = 1/2$ for $t \ge LT$. Let $h > 0$ be the modulation index, **not an integer**. Let $(a_i)_{i \in \mathbb{Z}}$ be binary symbols, $a_i \in \{+1, -1\}$, and let $(A_i)$ be integers with $A_i - A_{i-1} = a_i$ for every $i$ (the running sum of the symbols, fixed up to a constant). The CPM signal of unit amplitude is $s(t) = e^{j\phi(t)}$, where $j$ is the imaginary unit and, for $nT \le t < (n+1)T$,

$$\phi(t) = \pi h A_{n-L} + 2\pi h \sum_{i = n-L+1}^{n} a_i\, q(t - iT).$$

This is the phase $2\pi h\sum_i a_i q(t - iT)$ of the CPM page, with the finished symbols collected in $\pi h A_{n-L}$.

**The basic pulse.** Define $\psi(t) = 2\pi h\, q(t)$ for $0 \le t < LT$, $\psi(t) = \pi h - 2\pi h\, q(t - LT)$ for $LT \le t < 2LT$, and $\psi(t) = 0$ otherwise, and

$$S_0(t) = \frac{\sin \psi(t)}{\sin \pi h}.$$

**The pulses and the pseudo-symbols.** For $k = 0, 1, \ldots, 2^{L-1} - 1$, let $\beta_{k,1}, \ldots, \beta_{k,L-1} \in \{0, 1\}$ be the binary digits of $k$, so $k = \sum_{i=1}^{L-1} 2^{i-1}\beta_{k,i}$. Define

$$c_k(t) = S_0(t)\prod_{i=1}^{L-1} S_0\big(t + (i + L\beta_{k,i})T\big), \qquad b_{k,n} = \exp\Big(j\pi h\Big(A_n - \sum_{i=1}^{L-1} a_{n-i}\,\beta_{k,i}\Big)\Big).$$

**Theorem (Laurent).** For every real $t$,

$$s(t) = \sum_{k=0}^{2^{L-1}-1}\ \sum_{n \in \mathbb{Z}} b_{k,n}\; c_k(t - nT),$$

and at each $t$ only finitely many terms are nonzero. The pulse $c_k$ is zero outside $[0, D_k T]$ with $D_k = \min_{1 \le i \le L-1}\big(L(2 - \beta_{k,i}) - i\big)$ for $L \ge 2$ and $D_0 = 2$ for $L = 1$; the main pulse $c_0$ is the longest, with $D_0 = L + 1$.

## In plain words

A phase-modulated signal hides the data inside an angle, so it does not look like the sum of pulses that ordinary linear receivers expect. The theorem says the hiding is only on the surface. The same signal is exactly a sum of a few pulse trains, each with its own fixed pulse shape and its own stream of unit-size complex symbols made from the data. For a pulse that spans one symbol there is one train, and for a pulse that spans two symbols there are two. In practice the first train is far stronger than all the others, so a receiver that listens to it alone loses very little.

## Proof

Fix $n$ and $t \in [nT, (n+1)T)$, and put $\tau = t - nT \in [0, T)$.

**Step 1: a two-term identity.** For $a \in \{+1, -1\}$ and every real $\theta$,

$$\sin(\pi h)\, e^{ja\theta} = \sin(\pi h - \theta) + e^{j\pi h a}\sin\theta.$$

Indeed, the right side is $\sin\pi h\cos\theta - \cos\pi h\sin\theta + (\cos\pi h + ja\sin\pi h)\sin\theta = \sin\pi h(\cos\theta + ja\sin\theta)$, using $a^2 = 1$. Since $h$ is not an integer, $\sin \pi h \ne 0$ and we can divide.

**Step 2: one factor for each active symbol.** Write the active symbols as $a_{n-\ell}$ with $\ell = 0, \ldots, L-1$, and put $\theta_\ell = 2\pi h\, q(\tau + \ell T)$. Then $s(t) = e^{j\pi h A_{n-L}}\prod_{\ell=0}^{L-1} e^{j a_{n-\ell}\theta_\ell}$. The point $\tau + \ell T$ is in $[0, LT)$, so $\sin\theta_\ell/\sin\pi h = S_0(\tau + \ell T)$. The point $\tau + (\ell + L)T$ is in $[LT, 2LT)$, where $\psi = \pi h - \theta_\ell$, so $\sin(\pi h - \theta_\ell)/\sin\pi h = S_0(\tau + (\ell + L)T)$. Step 1 gives

$$e^{j a_{n-\ell}\theta_\ell} = S_0\big(\tau + (\ell + L)T\big) + e^{j\pi h a_{n-\ell}}\, S_0(\tau + \ell T).$$

**Step 3: expand the product.** Multiply the $L$ factors out. Each term chooses the second summand for the indices in a set $D \subseteq \{0, \ldots, L-1\}$ and the first for the others. Put $p_\ell = \ell$ if $\ell \in D$ and $p_\ell = \ell + L$ if $\ell \notin D$. Then

$$s(t) = \sum_{D} e^{j\pi h\left(A_{n-L} + \sum_{\ell \in D} a_{n-\ell}\right)}\ \prod_{\ell=0}^{L-1} S_0(\tau + p_\ell T). \qquad (1)$$

The set $P_D = \{p_0, \ldots, p_{L-1}\}$ lies in $\{0, \ldots, 2L-1\}$ and has exactly one element in each residue class modulo $L$. Conversely, every such set is $P_D$ for exactly one $D$: $\ell \in D$ if and only if the element of residue $\ell$ is less than $L$.

**Step 4: the terms of the right side.** A term of the right side of the theorem with pulse start $m = n - r$ is

$$b_{k,n-r}\, c_k(\tau + rT) = b_{k,n-r}\ S_0(\tau + s_0 T)\prod_{i=1}^{L-1} S_0(\tau + s_i T), \qquad s_0 = r,\quad s_i = r + i + L\beta_{k,i}.$$

$S_0(x) = 0$ when $x \le 0$ or $x \ge 2LT$, because $\psi(0) = 0$ and $\psi(2LT) = \pi h - 2\pi h \cdot \tfrac12 = 0$. Since $\tau \in [0, T)$, a factor $S_0(\tau + sT)$ with an integer $s < 0$ or $s \ge 2L$ is zero. So the term is zero unless $S_{k,r} = \{s_0, \ldots, s_{L-1}\} \subseteq \{0, \ldots, 2L-1\}$. Such a set has one element in each residue class modulo $L$, because $s_i \equiv r + i$. Its smallest element is $s_0 = r$, since $s_i > r$ for $i \ge 1$.

**Step 5: the sets match one to one.** Let $P$ be a set in $\{0, \ldots, 2L-1\}$ with one element in each residue class, and let $r = \min P$. For $1 \le i \le L-1$, the element $x$ of $P$ with residue $r + i$ satisfies $x > r$ and $x \equiv r + i$, and $x \le 2L - 1 < r + i + 2L$; so $x = r + i$ or $x = r + i + L$. Put $\beta_i = (x - r - i)/L \in \{0, 1\}$ and let $k$ have these digits. Then $S_{k,r} = P$, and $(k, r)$ is the only pair with this property, because $r$ must be the minimum and then each $\beta_i$ is forced. So the map $D \mapsto P_D \mapsto (k, r)$ is a bijection from the subsets $D$ onto the pairs $(k, r)$ whose terms can be nonzero, and the product of $S_0$ factors in (1) for $D$ equals the product in Step 4 for $(k, r)$. All other pairs give zero terms.

**Step 6: the phases match.** It remains to show that $b_{k,n-r}$ equals the phase factor of $D$ in (1). Note that $r = \min P_D \le p_0 \le L$, since $p_0 \in \{0, L\}$. Compare the elements of $P_D$ with the index $\ell$:
- For $\ell < r$: $p_\ell \ge r > \ell$, so $p_\ell = \ell + L$ and $\ell \notin D$.
- For $\ell = r \le L - 1$: $p_r$ is the element of residue $r$, which is $r$ itself, so $r \in D$. If $r = L$, every $p_\ell \ge L$ and $D$ is empty.
- For $r < \ell \le L - 1$, with $i = \ell - r$: the element of residue $\ell$ is $s_i = \ell + L\beta_{k,i}$, so $\ell \in D$ exactly when $\beta_{k,i} = 0$.
- For $i$ with $r + i \ge L$: the element of residue $r + i - L < r$ is $p_{r+i-L} = r + i$ by the first case, so $\beta_{k,i} = 0$.

Hence $\sum_{\ell \in D} a_{n-\ell} = \sum_{\ell=r}^{L-1} a_{n-\ell} - \sum_{i=1}^{L-1} a_{n-r-i}\beta_{k,i}$, where the first sum is empty when $r = L$. Since $A_{n-r} = A_{n-L} + \sum_{\ell=r}^{L-1} a_{n-\ell}$,

$$A_{n-L} + \sum_{\ell \in D} a_{n-\ell} = A_{n-r} - \sum_{i=1}^{L-1} a_{n-r-i}\,\beta_{k,i},$$

and $e^{j\pi h(\cdot)}$ of the right side is $b_{k,n-r}$. So the right side of the theorem at $t$ is the sum (1), which is $s(t)$. Only pairs with $0 \le r \le L$ contribute, so the sum at $t$ is finite.

**The support.** $c_k(t) \ne 0$ needs $0 < t < 2LT$ and $0 < t + (i + L\beta_{k,i})T < 2LT$ for each $i$, so $t < (2L - i - L\beta_{k,i})T$. This gives $D_k$; for $k = 0$ the binding factor is $i = L - 1$, with $D_0 = L + 1$, and every $k \ne 0$ has some $\beta_{k,i} = 1$, which gives $D_k \le L - 1$. $\blacksquare$

## Consequences

- **Full response is one PAM signal.** For $L = 1$ there is one pulse, $c_0 = S_0$, of length $2T$, and $s(t) = \sum_n e^{j\pi h A_n} c_0(t - nT)$ for every non-integer $h$. For MSK, $h = 1/2$, $c_0(t) = \sin(\pi t/(2T))$ on $[0, 2T]$ and $b_{0,n} = j^{A_n}$: this is offset QPSK with half-sine pulses.
- **The main pulse.** The pseudo-symbols $b_{0,n} = e^{j\pi h A_n}$ satisfy $b_{0,n} = b_{0,n-1}e^{j\pi h a_n}$, a differential encoding of the data. The pulse $c_0$ is the longest. For the usual smooth pulses it also carries most of the energy; this is an observation about these pulses, not part of the theorem. By numerical integration, $c_0$ holds $98.87\%$ of the total pulse energy for 2REC with $h = 1/2$, $99.48\%$ for 3RC with $h = 1/2$, and $99.63\%$ for GMSK with $BT = 0.3$ and $L = 4$; for 3REC with $h = 1/2$ it holds only $93.51\%$.
- **Linear receivers.** A receiver can filter with $c_0$ (or with $c_0$ and $c_1$), and then run a [Viterbi equalizer](/viterbi-equalizer/) or [reduced-state sequence estimation](/reduced-state-sequence-estimation/) on the pseudo-symbols. For GMSK the result is close to the full CPM receiver with far fewer states. The pulses $c_k$ are not orthogonal and their shifts overlap, so the matched filter outputs have [intersymbol interference](/intersymbol-interference/), which the trellis handles.
- **Linear transmitters.** A transmitter can make a close copy of a GMSK signal with one linear filter $c_0$ and the symbols $j^{A_n}$. GSM EDGE uses this main pulse as the transmit pulse of its 8-PSK mode.
- **$M$-ary CPM.** With $M = 2^P$ levels, write each symbol as a weighted sum of $P$ binary symbols. Mengali and Morelli show that the signal is a sum of $(2^P - 1)\,2^{P(L-1)}$ PAM signals when $h$ is not an integer; for $M = 4$ and $L = 1$ this gives $3$ pulses.

## Tightness

- **The integer case fails.** The proof divides by $\sin\pi h$, and for integer $h$ this is zero. The decomposition with these pulses does not exist then, and the $M$-ary result also excludes integer $h$. Integer indices are also bad CPM designs, so this restriction costs little.
- **Binary symbols are needed in Step 1.** The identity uses $a^2 = 1$. For $a = \pm 3$ the same two-term form does not hold, which is why the $M$-ary case needs the binary expansion of the symbols and more pulses.
- **The approximation by $c_0$ is not exact unless $L = 1$.** For $L \ge 2$ the other pulses are not zero; the share of energy they carry depends on the pulse shape, from about $0.01\%$ for 2RC with $h = 1/2$ to $6.5\%$ for 3REC with $h = 1/2$.

## History

Pierre Laurent published the decomposition in 1986 under the name "superposition of amplitude modulated pulses" (AMP), for binary CPM. It explained why MSK equals offset QPSK and gave a way to build simple receivers for partial response CPM such as GMSK. In 1995 Umberto Mengali and Michele Morelli extended it to $M$-ary CPM with $M$ a power of two, and later work used it for synchronization and for reduced-complexity detection of CPM.

## References
