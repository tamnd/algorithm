---
title: The ziggurat method returns a standard normal variate when the layers have equal area and cover the density
proves: [correctness, time.expected]
status: full
---

Let $f(x) = e^{-x^2/2}$ on $[0, \infty)$, and let $G = \{(x, h) : x \ge 0,\ 0 \le h < f(x)\}$ be the region under it, of area $\int_0^\infty f = \sqrt{\pi/2}$. The table has $N \ge 2$ layers and numbers $x_0 > x_1 = r > x_2 > \dots > x_{N-1} > x_N = 0$ and $0 = y_0 < y_1 < \dots < y_N$, with these properties:

- (T1) $y_i = f(x_i)$ for $1 \le i \le N - 1$, and $y_N \ge 1$;
- (T2) $v = r f(r) + T$, where $T = \int_r^\infty f$ is the tail area, and $x_0 = v / f(r)$;
- (T3) $x_i (y_{i+1} - y_i) = v$ for $1 \le i \le N - 1$.

The builder in the implementation makes (T2) and (T3) hold by definition and checks $y_N \ge 1$.

**The layers.** The base layer is $B = [0, r) \times [0, y_1) \cup \{(x, h) : x \ge r,\ 0 \le h < f(x)\}$, a rectangle plus the tail region. Its area is $r f(r) + T = v$. For $1 \le i \le N - 1$, layer $i$ is the rectangle $L_i = [0, x_i) \times [y_i, y_{i+1})$, of area $v$ by (T3). Write $L_0 = B$.

**Lemma 1 (cover).** The layers are pairwise disjoint and $G \subseteq L_0 \cup \dots \cup L_{N-1}$.

*Proof.* Points of $L_0$ have $h < y_1$ (in the tail, $h < f(x) \le f(r) = y_1$), and points of $L_i$ have $h \in [y_i, y_{i+1})$. These height ranges are disjoint. Take $(x, h) \in G$. If $h < y_1$: either $x < r$ and the point is in the rectangle part of $B$, or $x \ge r$ and $h < f(x)$ puts it in the tail part. If $h \ge y_1$: since $h < f(x) \le 1 \le y_N$, there is an $i$ with $1 \le i \le N - 1$ and $y_i \le h < y_{i+1}$. Then $f(x) > h \ge y_i = f(x_i)$, and $f$ is decreasing, so $x < x_i$. The point is in $L_i$. $\square$

**Lemma 2 (the tail).** The tail method returns a variate with density $f(t)/T$ on $(r, \infty)$.

*Proof.* It draws $E_1 = -\ln(U_1)/r$, with density $r e^{-rs}$ on $(0, \infty)$, and an independent standard exponential $E_2$, and accepts when $2E_2 > E_1^2$. Given $E_1 = s$, this has probability $\Pr[E_2 > s^2/2] = e^{-s^2/2}$. So an accepted value has density proportional to $e^{-rs} e^{-s^2/2} = e^{r^2/2} e^{-(r + s)^2/2}$, and $r + E_1$ has density proportional to $f$ on $(r, \infty)$. This is [rejection sampling](/rejection-sampling/) with a bound of 1 on the ratio, which is exact. $\square$

**Lemma 3 (one try).** For a measurable set $A \subseteq [0, \infty)$, one try (lines L2 to L7) returns a value with absolute value in $A$ with probability $\frac{1}{Nv} \int_A f$. It returns a value with probability $\frac{\sqrt{\pi/2}}{Nv}$.

*Proof.* Line L2 picks a layer $i$ uniformly. Take first $1 \le i \le N - 1$. Line L3 makes $u$ uniform on $[0, x_i)$, and line L6 makes $h$ uniform on $[y_i, y_{i+1})$, independent of $u$. So $(u, h)$ is uniform on $L_i$. The try returns $u$ exactly when $h < f(u)$: line L7 tests this directly, and line L4 returns $u$ only when $u < x_{i+1}$, which happens only for $i \le N - 2$; then $f(u) > f(x_{i+1}) = y_{i+1} > h$ by (T1), so the point is under $f$ whatever $h$ is. Hence the try returns a value in $A$ with probability $\operatorname{area}(L_i \cap G \cap \{x \in A\}) / v$.

Now take $i = 0$. Line L3 makes $u$ uniform on $[0, x_0)$. With probability $r / x_0 = r f(r) / v$, $u < r$, and line L4 returns $u$, uniform on $[0, r)$. This is the $x$ coordinate of a uniform point in the rectangle part of $B$, which lies under $f$. With probability $1 - r f(r)/v = T/v$, line L5 returns a tail variate with density $f/T$ (Lemma 2), the $x$ coordinate of a uniform point in the tail part of $B$. So the base layer always returns a value, and the value is in $A$ with probability

$$\frac{r f(r)}{v} \cdot \frac{|A \cap [0, r)|}{r} + \frac{T}{v} \int_{A \cap [r, \infty)} \frac{f}{T} = \frac{\operatorname{area}(B \cap G \cap \{x \in A\})}{v},$$

since $B \subseteq G$ up to the boundary. Average over the $N$ layers and use Lemma 1: the layers are disjoint and cover $G$, so

$$\frac{1}{N} \sum_{i=0}^{N-1} \frac{\operatorname{area}(L_i \cap G \cap \{x \in A\})}{v} = \frac{\operatorname{area}(G \cap \{x \in A\})}{Nv} = \frac{1}{Nv} \int_A f.$$

With $A = [0, \infty)$ this is $\sqrt{\pi/2}/(Nv)$. $\square$

**Theorem.** The returned value $Z$ has the standard normal density, and the number of tries is geometric with mean $Nv/\sqrt{\pi/2}$.

*Proof.* The tries are independent and alike. Let $p = \sqrt{\pi/2}/(Nv)$. By Lemma 3,

$$\Pr[|Z| \in A] = \sum_{k \ge 1} (1 - p)^{k-1} \frac{1}{Nv} \int_A f = \frac{1}{p N v} \int_A f = \frac{\int_A f}{\sqrt{\pi/2}}.$$

So $|Z|$ has the half-normal density $\sqrt{2/\pi}\, e^{-x^2/2}$ on $[0, \infty)$. The sign $s$ in line L2 is independent of the rest of the try and takes each value with probability $1/2$, so $Z = s|Z|$ has density $\frac{1}{2}\sqrt{2/\pi}\, e^{-z^2/2} = \varphi(z)$. The number of tries is geometric with success probability $p$, so its mean is $1/p = Nv/\sqrt{\pi/2}$. $\blacksquare$

**Cost.** For $N = 128$ and $r = 3.44261985589$, $v \approx 9.9126 \times 10^{-3}$ and the mean number of tries is $Nv/\sqrt{\pi/2} \approx 1.0124$. One try takes the fast path in line L4 with probability $\frac{1}{N}\bigl(\frac{r}{x_0} + \sum_{i=1}^{N-1} \frac{x_{i+1}}{x_i}\bigr) \approx 0.9724$. The tail method in line L5 runs with probability $T/(Nv) \approx 5.7 \times 10^{-4}$ per try, and itself takes $1/\mathbb{E}[e^{-E_1^2/2}]$ rounds in expectation, where $\mathbb{E}[e^{-E_1^2/2}] = rT/f(r) \approx 0.93$ for this $r$.

**Exactness.** The proof uses only (T1) to (T3). It does not need $y_N = 1$ exactly: if the top layer reaches above $f(0) = 1$, its extra part is never accepted, and the method is still exact. If $y_N < 1$, Lemma 1 fails near $x = 0$: points with $h \in [y_N, f(x))$ are never produced, and the density is too small there. In floating point the table entries carry rounding errors of order $10^{-16}$, $u$ lies on a grid, and $\ln$ and $\exp$ are rounded, so the theorem holds only in exact arithmetic.
