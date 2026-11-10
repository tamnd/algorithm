---
title: The polar method gives two independent standard normal variates, after a geometric number of tries
proves: [correctness, time.expected]
status: full
---

The input is a stream of independent uniform reals. Each try of lines L2 to L4 takes $V_1, V_2$ independent and uniform on $[-1, 1)$, so the point $V = (V_1, V_2)$ is uniform on the square $Q = [-1, 1)^2$ of area 4. Let $D = \{v : 0 < v_1^2 + v_2^2 < 1\}$ be the open unit disk without its center, of area $\pi$. Line L4 accepts the try when $V \in D$.

**Lemma 1 (the accepted point).** The number of tries $N$ has $\Pr[N = k] = (1 - \pi/4)^{k-1} (\pi/4)$ for $k \ge 1$, so $\mathbb{E}[N] = 4/\pi$. The accepted point is uniform on $D$.

*Proof.* A single try is accepted with probability $\operatorname{area}(D)/\operatorname{area}(Q) = \pi/4$, and the tries are independent, so $N$ is geometric with success probability $\pi/4$ and mean $4/\pi$. For a measurable set $A$, a single try gives $\Pr[V \in A \cap D] = \operatorname{area}(A \cap D)/4$. The accepted point is in $A$ if the first accepted try lands in $A$, so

$$\Pr[\text{output point} \in A] = \sum_{k \ge 1} \Bigl(1 - \frac{\pi}{4}\Bigr)^{k-1} \frac{\operatorname{area}(A \cap D)}{4} = \frac{\operatorname{area}(A \cap D)}{4} \cdot \frac{4}{\pi} = \frac{\operatorname{area}(A \cap D)}{\pi}.$$

This is the uniform law on $D$. $\square$

**Lemma 2 (radius and angle).** Let $V$ be uniform on $D$. Write $V = \sqrt{S}\,(\cos\Theta, \sin\Theta)$ with $S = V_1^2 + V_2^2 \in (0, 1)$ and $\Theta \in [0, 2\pi)$. Then $S$ is uniform on $(0, 1)$, $\Theta$ is uniform on $[0, 2\pi)$, and $S$ and $\Theta$ are independent.

*Proof.* For $0 < s \le 1$ and $0 < t \le 2\pi$, the event $\{S \le s, \Theta < t\}$ is the sector of $D$ with radius $\sqrt{s}$ and angle $t$, without the center. Its area is $\frac{1}{2} (\sqrt{s})^2 t = st/2$. By Lemma 1 the probability is $(st/2)/\pi = s \cdot \frac{t}{2\pi}$. The joint distribution function is the product of the distribution function $s$ of the uniform law on $(0, 1)$ and the distribution function $t/(2\pi)$ of the uniform law on $[0, 2\pi)$. So $S$ and $\Theta$ are independent with these laws. $\square$

**Theorem.** The pair returned by line L6 is a pair of independent standard normal variates.

*Proof.* Line L5 sets $F = \sqrt{-2 \ln S / S}$, so the output is

$$(V_1 F, V_2 F) = \sqrt{S}\,(\cos\Theta, \sin\Theta) \cdot \sqrt{\frac{-2\ln S}{S}} = \sqrt{-2 \ln S}\,(\cos\Theta, \sin\Theta).$$

Put $U_1 = S$ and $U_2 = \Theta/(2\pi)$. By Lemma 2 these are independent, $U_1$ is uniform on $(0, 1)$ and $U_2$ is uniform on $[0, 1)$. The output is $\bigl(\sqrt{-2\ln U_1}\cos(2\pi U_2), \sqrt{-2\ln U_1}\sin(2\pi U_2)\bigr)$, which is the Box-Muller transform of $(U_1, U_2)$. The correctness theorem of the [Box-Muller transform](/box-muller-transform/), proved there with the Jacobian of the map, says that this pair is a pair of independent standard normal variates. (The value $U_1 = 1$, allowed there, has probability 0 and does not change the law.) $\blacksquare$

**Cost.** By Lemma 1 a pair takes $4/\pi \approx 1.2732$ tries in expectation, so $8/\pi \approx 2.5465$ uniforms, $4/\pi$ uniforms per normal variate. The number of tries has a geometric tail: $\Pr[N > k] = (1 - \pi/4)^k \approx 0.2146^k$. There is no bound for every random string: an adversarial stream of uniforms can stay outside $D$ forever.

**Floating point.** With $V_i = 2U - 1$ and 53-bit uniforms, $V_i$ is a multiple of $2^{-52}$, so the smallest positive $S$ is $2^{-104}$, and $|Z_i| \le \sqrt{-2 \ln S} \le \sqrt{208 \ln 2} \approx 12.01$. The output takes finitely many values, and the rounding of $\ln$, the division and the square root moves each value by a few units in the last place. The theorem holds only in exact arithmetic.
