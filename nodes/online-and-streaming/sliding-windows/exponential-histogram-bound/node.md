---
tag: RHHHWB
kind: theorem
slug: exponential-histogram-bound
name: Exponential histogram space bound
aliases:
- Datar et al. space theorem
- DGIM space bound
- space bound for basic counting
area: online-and-streaming/sliding-windows
level: advanced
summary: Basic counting over the last W bits with relative error eps needs and can be done in Theta((1/eps) log^2 W) bits, for eps not too small; the upper bound is the exponential histogram.
prereqs: [basic-counting, dgim-algorithm, pigeonhole-principle, adversary-argument]
see_also: [dgim-algorithm, exponential-histogram, basic-counting, sliding-window-model, lower-bound, index-problem-lower-bound, sliding-window-distinct-count, smooth-histogram]
sources:
  - paper: doi:10.1137/S0097539701398363
    title: Mayur Datar, Aristides Gionis, Piotr Indyk and Rajeev Motwani, Maintaining stream statistics over sliding windows, SIAM Journal on Computing 31(6), 2002
    locator: the space bound of the exponential histogram and the lower bound Omega((1/eps) log^2(eps N)) for deterministic and randomized algorithms
  - paper: doi:10.1145/564870.564880
    title: Phillip B. Gibbons and Srikanta Tirthapura, Distributed streams algorithms for sliding windows, SPAA 2002
    locator: pp. 63 to 72, the statement of the DGIM bounds and of the lower bound for randomized and deterministic algorithms
  - book: isbn:9781107077232
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, second edition, Cambridge University Press, 2014
    locator: Chapter 4, Section 4.6, Counting Ones in a Window (the space of DGIM)
---

The exponential histogram space bound says that [basic counting](/basic-counting/) over a window of the last $W$ bits, with [relative error](/relative-error/) $\varepsilon$, can be done in $O(\frac{1}{\varepsilon} \log^2 W)$ bits and needs $\Omega(\frac{1}{\varepsilon} \log^2(\varepsilon W))$ bits. Datar, Gionis, Indyk and Motwani (DGIM) proved both bounds in 2002: the upper bound with the [exponential histogram](/exponential-histogram/), and the lower bound for deterministic and for randomized algorithms. This page proves the upper bound and the deterministic lower bound in full and cites the randomized one. The model is the [sliding window model](/sliding-window-model/) with a [count-based window](/count-based-window/) of size $W$.

## Statement

**Theorem.** Let $W \ge 1$ and $0 < \varepsilon \le 1/3$. Consider algorithms that read a bit stream and answer, at every time, the number $c$ of 1s among the last $W$ bits with an answer $\hat c$ such that $|\hat c - c| \le \varepsilon c$.

1. (Upper bound.) The [DGIM algorithm](/dgim-algorithm/) with $k = \lceil 1/\varepsilon \rceil$ meets the guarantee, deterministically, with at most $(L + 1)(\rho + 1)$ buckets of $\lceil \log_2 W \rceil$ bits each, where $L = \lceil k/2 \rceil$ and $\rho = \lfloor \log_2((W - 1)/L + 1) \rfloor$, plus $O(\log W \log k)$ further bits. This is $O(\frac{1}{\varepsilon} \log^2 W)$ bits.
2. (Deterministic lower bound.) Let $m = \lfloor (1/\varepsilon + 1)/4 \rfloor$ and $q = \lfloor \frac{1}{2} \log_2 (W/m) \rfloor$. Each deterministic algorithm that meets the guarantee has at least $2^{m q^2}$ memory states, so it uses at least $m q^2$ bits. If $\varepsilon W \ge 2$, this is at least $\frac{1}{128\,\varepsilon} \log_2^2 (3 \varepsilon W)$ bits, which is $\Omega(\frac{1}{\varepsilon} \log^2 (\varepsilon W))$.
3. (Randomized lower bound, cited.) DGIM prove that the bound $\Omega(\frac{1}{\varepsilon} \log^2(\varepsilon W))$ also holds for randomized algorithms.

## In plain words

To count the ones in a moving window with a small percentage of error, you need memory that grows with the square of the number of digits of the window size, times the inverse of the error. The exponential histogram reaches this. No method can do better, because the memory must tell apart many different recent histories. The proof builds such histories: blocks of ones of sizes one, two, four and so on, each placed at one of many possible offsets. For two different histories, waiting the right time lets the window cut through one block in a way that gives the two histories counts too far apart to share one answer.

## Proof

**Part 1.** By Lemma 2 of the [DGIM proof](/dgim-algorithm/), the answer has relative error less than $1/(2L) \le 1/k \le \varepsilon$. By Lemma 3 there, the number of buckets is at most $(L + 1)(\rho + 1)$, and the space paragraph there shows that each timestamp takes $\lceil \log_2 W \rceil$ bits and that the levels, the counts, $t \bmod W$ and the total take $O(\log W \log k)$ further bits. With $L + 1 \le 1/(2\varepsilon) + 2$ and $\rho + 1 \le \log_2 W + 1$, the total is $O(\frac{1}{\varepsilon} \log^2 W)$ bits.

**Part 2.** Fix a deterministic algorithm $A$ that meets the guarantee. We have $1/\varepsilon \ge 3$, so $(1/\varepsilon + 1)/4 \ge 1$ and $m \ge 1$. If $q = 0$ there is nothing to prove, so let $q \ge 1$, and put $P = 2^q$ and $B = q$.

*The strings.* A **unit of level $i$**, for $0 \le i < B$, is a string of $P \cdot 2^i$ bits that is 0 except for one run of $2^i$ ones, which starts at the offset $\alpha \cdot 2^i$ for a choice $\alpha \in \{0, \ldots, P - 1\}$. For a vector $a$ of $mB$ choices, the string $X(a)$ is the concatenation of $m$ units of level $B - 1$, then $m$ units of level $B - 2$, and so on down to $m$ units of level 0, with the choices taken from $a$ in order. Its length is
$$T = \sum_{i=0}^{B-1} m P 2^i = mP(2^B - 1) < m\, 2^{2q} \le W,$$
because $2q \le \log_2(W/m)$. There are $P^{mB} = 2^{mq^2}$ vectors $a$.

*Distinct vectors give distinct states.* Let $a \ne a'$, and suppose that $A$ is in the same state after reading $X(a)$ and after reading $X(a')$. Let $u$ be the last unit in the string where the choices differ. Let $i$ be its level, and name the two vectors so that the choice of $a$ at $u$ is $\alpha$ and the choice of $a'$ is $\beta$, with $\alpha < \beta$. Let $p_0$ be the position where unit $u$ starts, counting the first bit of the stream as position 0.

Append $z = p_0 + \beta 2^i + W - T$ zeros to both streams; $z \ge 0$ because $T \le W$. After the $T + z$ bits, the window holds the positions $p_0 + \beta 2^i$ to $T + z - 1$. Then:

- The units before $u$ end before position $p_0$, so they are outside the window.
- In $X(a')$, the run of unit $u$ starts at $p_0 + \beta 2^i$, so its $2^i$ ones are inside. In $X(a)$, the run ends at $p_0 + (\alpha + 1) 2^i - 1 < p_0 + \beta 2^i$, so it is outside.
- The units after $u$ are the same in both strings, by the choice of $u$, and they are inside. Let $R$ be their number of 1s. They are at most $m - 1$ units of level $i$ and $m$ units of each level $j < i$, so
$$R \le (m - 1) 2^i + m(2^i - 1) = (2m - 1) 2^i - m.$$
- The appended zeros add nothing.

So the counts are $c = R$ for $X(a)$ and $c' = R + 2^i$ for $X(a')$. The algorithm is deterministic and in the same state, and it reads the same zeros, so it gives the same answer $o$ in both runs. The guarantee gives $o \le (1 + \varepsilon) R$ and $o \ge (1 - \varepsilon)(R + 2^i)$. So $(1 - \varepsilon)(R + 2^i) \le (1 + \varepsilon) R$, which is $2^i \le \varepsilon (2R + 2^i)$. But
$$\varepsilon(2R + 2^i) \le \varepsilon\left((4m - 1) 2^i - 2m\right) < \varepsilon (4m - 1) 2^i \le 2^i,$$
because $m \le (1/\varepsilon + 1)/4$ gives $\varepsilon(4m - 1) \le 1$. This is a contradiction. So the $2^{mq^2}$ strings lead to $2^{mq^2}$ distinct states, and a memory of $s$ bits, with at most $2^s$ states, has $s \ge mq^2$.

*The asymptotic form.* Put $x = (1/\varepsilon + 1)/4 \ge 1$. Then $m = \lfloor x \rfloor \ge x/2 > 1/(8\varepsilon)$. Also $x \le 1/(3\varepsilon)$, because $1/\varepsilon + 1 \le 4/(3\varepsilon)$ when $1/\varepsilon \ge 3$; so $W/m \ge 3\varepsilon W$ and $q \ge \lfloor \frac{1}{2}\log_2(3 \varepsilon W) \rfloor$. If $\varepsilon W \ge 2$, then $y = \log_2(3\varepsilon W) \ge \log_2 6 > 2$, and $\lfloor y/2 \rfloor \ge y/4$ for $y \ge 2$. So
$$m q^2 > \frac{1}{8 \varepsilon} \cdot \frac{y^2}{16} = \frac{\log_2^2(3 \varepsilon W)}{128\, \varepsilon}. \qquad \square$$

**Part 3** is cited from DGIM.

## Consequences

- **DGIM is optimal.** For $\varepsilon \ge W^{-c}$ with a constant $c < 1$, $\log(\varepsilon W) = \Theta(\log W)$, and the two bounds meet: basic counting needs $\Theta(\frac{1}{\varepsilon} \log^2 W)$ bits.
- **Windows cost more than prefixes.** Without expiry, an exact count of the whole stream needs only $O(\log W)$ bits for streams of length at most $W$. With a window, even an answer with relative error $1/3$ needs $\Omega(\log^2 W)$ bits.
- **Other problems.** Each problem to which basic counting reduces inherits the bound. The sum of integers in $\{0, \ldots, R\}$ contains basic counting as the case $R = 1$; DGIM prove the stronger bound $\Omega(\frac{1}{\varepsilon} \log W (\log W + \log R))$ for it. The known lower bound for the [distinct count over a window](/sliding-window-distinct-count/) has the same term $\frac{1}{\varepsilon} \log^2 W$.

## Tightness

The upper bound and the lower bound differ only in $\log^2 W$ against $\log^2(\varepsilon W)$. When $\varepsilon < 1/W$, an error of $\varepsilon c < 1$ forces the exact answer, and then $W$ bits are needed and enough (see [basic counting](/basic-counting/)); the polylogarithmic bounds apply only when $\varepsilon W$ is large. The constant $1/128$ of Part 2 is not tight; the construction gives the order of growth only. The proof above needs $\varepsilon \le 1/3$, so that $m \ge 1$.

## History

Datar, Gionis, Indyk and Motwani proved the upper bound and the lower bound for basic counting at SODA 2002 and in SIAM Journal on Computing in 2002, together with the bounds for sums. Gibbons and Tirthapura (2002) restated the lower bound for randomized and deterministic algorithms and matched the upper bound with worst-case constant time per bit. The construction of Part 2, with runs of 1s of sizes $2^i$ at many offsets, is written for this page with parameters chosen for a short proof; the original proof is in the paper of DGIM.

## References
