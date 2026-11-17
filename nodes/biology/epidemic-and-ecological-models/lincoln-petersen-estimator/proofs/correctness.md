---
title: The counts, the moment and likelihood estimates, and the exact mean of Chapman's estimate
proves: [correctness]
status: full
---

**Setting.** A closed population has $N$ animals. The first sample marks a set $A$ of $M$ distinct animals. The second sample is a set $B$ of $C$ distinct animals, drawn so that every set of $C$ animals has probability $1 / \binom{N}{C}$, independently of $A$. Let $R = |A \cap B|$. We use $\binom{a}{b} = 0$ when $b < 0$ or $b > a$.

**Claim 1 (the counts).** Lines L1 to L3 return $M = |A|$, $C = |B|$ and $R = |A \cap B|$.

*Proof.* Line L1 puts the $M$ distinct identifiers of the first list into a set, so the set has size $M$. Line L2 counts the $C$ distinct identifiers of the second list. Line L3 adds 1 for each element of $B$ that is in $A$ and 0 for every other element. Each element of $B$ is seen once, so the sum is $|A \cap B|$. $\square$

**Claim 2 (the law of $R$ and the moment estimate).** $\Pr(R = r) = \binom{M}{r}\binom{N - M}{C - r} / \binom{N}{C}$ and $\mathbb{E}[R] = M C / N$. For $R \ge 1$, the value $N = M C / R$ of line L6 is the unique solution of $R = M C / N$.

*Proof.* A set $B$ with $|A \cap B| = r$ is a choice of $r$ marked and $C - r$ unmarked animals, and there are $\binom{M}{r}\binom{N - M}{C - r}$ such sets, each with probability $1 / \binom{N}{C}$. For the mean, write $R = \sum_{a \in A} \mathbf{1}[a \in B]$. Each animal is in $B$ with probability $\binom{N - 1}{C - 1} / \binom{N}{C} = C / N$, so by linearity of expectation $\mathbb{E}[R] = M C / N$. The map $N \mapsto M C / N$ is strictly decreasing on $N > 0$ when $M C > 0$, so the equation has one solution. If $M C = 0$ then $R = 0$, and line L6 returns no value. $\square$

**Claim 3 (the likelihood estimate).** Let $R = r \ge 1$ and $L(N) = \Pr(R = r \mid N)$ for the integers $N \ge M + C - r$, the values for which $L(N) > 0$. Then $L$ is largest at $N^* = \lfloor M C / r \rfloor$, and $N^*$ is the largest maximizer.

*Proof.* For $N - 1 \ge M + C - r$, both $L(N)$ and $L(N - 1)$ are positive, and the factorials cancel to give

$$\frac{L(N)}{L(N - 1)} = \frac{(N - M)(N - C)}{N (N - M - C + r)}.$$

The ratio is $\ge 1$ if and only if $(N - M)(N - C) \ge N (N - M - C + r)$. Expand both sides: $N^2 - N(M + C) + M C \ge N^2 - N(M + C) + N r$, that is, $N \le M C / r$, with equality of the two sides exactly when $N = M C / r$. So $L$ increases strictly while $N < M C / r$, takes the same value at $N - 1$ and $N$ when $N = M C / r$ is an integer, and decreases strictly for $N > M C / r$. Hence the maximizers are the integers in $[M C / r - 1, M C / r]$ that are $\ge M + C - r$, and the largest one is $\lfloor M C / r \rfloor$. This value is allowed, because $M C / r - (M + C - r) = (M - r)(C - r) / r \ge 0$ and $M + C - r$ is an integer. $\square$

**Claim 4 (the exact mean of Chapman's estimate).** Let $\hat N_C = (M + 1)(C + 1)/(R + 1) - 1$, the value of line L4. Then

$$\mathbb{E}[\hat N_C] = N - (C + 1) \frac{\binom{N - M}{C + 1}}{\binom{N}{C}}.$$

So $\mathbb{E}[\hat N_C] = N$ when $N \le M + C$, and $\mathbb{E}[\hat N_C] = N - (N - M - C)\Pr(R = 0)$ when $N \ge M + C$.

*Proof.* Step 1. For every integer $r \ge 0$, $\frac{M + 1}{r + 1}\binom{M}{r} = \binom{M + 1}{r + 1}$. So

$$\mathbb{E}\left[\frac{(M + 1)(C + 1)}{R + 1}\right] = \frac{C + 1}{\binom{N}{C}} \sum_{r \ge 0} \binom{M + 1}{r + 1}\binom{N - M}{C - r} = \frac{C + 1}{\binom{N}{C}} \sum_{s \ge 1} \binom{M + 1}{s}\binom{N - M}{C + 1 - s}.$$

Step 2. By Vandermonde's identity, the sum over all $s \ge 0$ is $\binom{N + 1}{C + 1}$. The term $s = 0$ is $\binom{N - M}{C + 1}$. So the sum over $s \ge 1$ is $\binom{N + 1}{C + 1} - \binom{N - M}{C + 1}$.

Step 3. $(C + 1)\binom{N + 1}{C + 1} / \binom{N}{C} = N + 1$, because $\binom{N + 1}{C + 1} = \frac{N + 1}{C + 1}\binom{N}{C}$. Subtract 1 to get the formula for $\mathbb{E}[\hat N_C]$.

Step 4. If $N \le M + C$, then $N - M < C + 1$ and $\binom{N - M}{C + 1} = 0$. If $N \ge M + C$, then $\binom{N - M}{C + 1} = \binom{N - M}{C} \frac{N - M - C}{C + 1}$, and $\binom{N - M}{C} / \binom{N}{C} = \Pr(R = 0)$ by Claim 2. Substitute to get $\mathbb{E}[\hat N_C] = N - (N - M - C)\Pr(R = 0)$. $\square$

**Claim 5 (the classic estimate has no finite mean when $N > M + C$).** If $N > M + C$, then $\Pr(R = 0) = \binom{N - M}{C} / \binom{N}{C} > 0$, because $N - M \ge C$. On this event line L6 has no value, so $\hat N_{LP}$ is not a finite random variable, and any convention that assigns it the value $+\infty$ gives an infinite mean. Chapman's estimate is finite for every $R$, and Claim 4 bounds its bias. $\square$

The variance estimate of line L5 is a formula from the literature (Seber 1982). Lines L5 and L7 compute it and return all values, and no claim on its accuracy is proved here.

Claims 1 to 5 together show that the algorithm returns the exact counts, the moment estimate, the value whose floor is the likelihood estimate, and an estimate whose exact mean is given by Claim 4. $\blacksquare$
