---
title: Globally adaptive Simpson quadrature terminates, returns a composite Boole rule on a partition of the interval, and has an asymptotically correct error estimate
proves: [correctness, termination, estimate]
status: full
---

We use the notation of the page. For a panel $[l, r]$ with $h = r - l$ and the values $f_0, \ldots, f_4$ of $f$ at $l + ih/4$, the panel quantities are

$$S_1 = \tfrac{h}{6}(f_0 + 4f_2 + f_4), \quad S_2 = \tfrac{h}{12}(f_0 + 4f_1 + 2f_2 + 4f_3 + f_4), \quad Q = S_2 + \tfrac{S_2 - S_1}{15}, \quad e = \tfrac{|S_2 - S_1|}{15}.$$

Claims 1 to 4 are about the algorithm in exact arithmetic, except where floating point is named. Claim 5 is about the estimate $e$.

## Claim 1: termination

Each pass of the loop of line L5 either stops at line L6 or line L8, or reaches line L9, which adds 4 to the evaluation count $k$. Line L6 lets a pass reach line L9 only when $k + 4 \le N$. So $k$ never exceeds $N$, and the number of passes is at most $(N - 5)/4 + 1$. Each pass does a bounded number of heap operations, so the algorithm stops.

## Claim 2: the invariant

Before each test of line L5, the following holds.

> **(P)** The panels in $H$ have disjoint interiors and their union is $[a, b]$. Each panel $[l, r]$ in $H$ stores the values of $f$ at the five points $l + i(r - l)/4$, $i = 0, \ldots, 4$, and its $Q$ and $e$ computed from them. In exact arithmetic $Q_{tot} = \sum_{H} Q$ and $E_{tot} = \sum_{H} e$.

*Initialization.* After lines L2 to L4, $H$ holds only $[a, b]$ with its five values, and $Q_{tot}$, $E_{tot}$ are its $Q$ and $e$.

*Maintenance.* A pass that reaches line L11 removes one panel $[l, r]$ and inserts $[l, m]$ and $[m, r]$ with $m = l + (r - l)/2$. These two panels have disjoint interiors and their union is $[l, r]$, so the first statement of (P) stays true. The five points of $[l, m]$ are $l, l + (r-l)/8, l + (r-l)/4, l + 3(r-l)/8, m$. The first, third and fifth are points $0, 1, 2$ of the old panel, whose values are stored; the second and fourth are evaluated at line L9. The same holds for $[m, r]$ with old points $2, 3, 4$. Line L10 subtracts the old $Q$ and $e$ and adds the two new ones, so the sums stay equal to the sums over $H$. A pass that stops at line L6 or L8 leaves $H$ as it was.

*Termination of the loop.* When the loop ends, (P) holds.

## Claim 3: the output

Line L12 returns $\sum_H Q$ and $\sum_H e$, recomputed from the panels, so drift in the running sums of line L10 does not reach the output. By (P), $\sum_H Q$ is the composite rule that applies the panel rule $Q$ on each panel of a partition of $[a, b]$. The flag is true exactly when $\sum_H e \le \tau$.

The panel rule is Boole's rule. Indeed $16 S_2 - S_1 = \tfrac{h}{12}(14, 64, 24, 64, 14) \cdot (f_0, \ldots, f_4)$, so

$$Q = \frac{16 S_2 - S_1}{15} = \frac{h}{90}\bigl(7f_0 + 32f_1 + 12f_2 + 32f_3 + 7f_4\bigr).$$

On $[0, 1]$ this rule integrates $x^k$ exactly for $k = 0, \ldots, 5$ and gives the errors $1/2688$ for $x^6$ and $1/768$ for $x^7$ (rational arithmetic). So its degree of precision is $5$, and the output is exact for each polynomial of degree at most 5, whatever partition the loop builds.

## Claim 4: polynomials of degree at most 3

If $f$ is a polynomial of degree at most 3, then $S_1 = S_2 = \int_l^r f$ on every panel, because Simpson's rule has degree of precision 3. So $e = 0$ on $[a, b]$, the loop of line L5 does not run, and the algorithm returns the exact integral after 5 evaluations.

## Claim 5: the estimate is asymptotically correct for smooth f

**Lemma.** Let $f \in C^6$ near a point $c$, and let $S(h)$ be Simpson's rule on $[c - h/2, c + h/2]$. Then

$$\int_{c-h/2}^{c+h/2} f - S(h) = -\frac{h^5}{2880} f^{(4)}(c) + R, \qquad |R| \le C h^7 \max|f^{(6)}|,$$

with a constant $C$ that does not depend on $f$ or $h$, and the maximum over the panel.

*Proof.* Write $f(x) = T_5(x) + \rho(x)$ with $T_5$ the Taylor polynomial of degree 5 at $c$ and $|\rho(x)| \le \max|f^{(6)}|\,|x - c|^6/720$. Simpson's rule is exact for $1, (x-c), (x-c)^2, (x-c)^3$, and for $(x-c)^5$ both the integral and the rule are $0$ by symmetry. For $(x - c)^4$ the integral is $h^5/80$ and the rule gives $\tfrac{h}{6} \cdot 2 (h/2)^4 = h^5/48$, a difference of $-h^5/120$. With the factor $f^{(4)}(c)/24$ this gives $-h^5 f^{(4)}(c)/2880$. The error on $\rho$ is at most $(h + h)\max|\rho| \le 2h \cdot (h/2)^6 \max|f^{(6)}|/720$, which is $O(h^7)$. $\square$

**Claim.** On a panel $[l, r]$ of width $h$ with center $c$, for $f \in C^6$,

$$\int_l^r f - S_2 = \frac{S_2 - S_1}{15} + O(h^7).$$

*Proof.* By the lemma, $\int_l^r f - S_1 = -\frac{h^5}{2880} f^{(4)}(c) + O(h^7)$. $S_2$ is Simpson's rule on two panels of width $h/2$ with centers $c \pm h/4$. By the lemma on each, and by $f^{(4)}(c \pm h/4) = f^{(4)}(c) \pm \tfrac{h}{4} f^{(5)}(c) + O(h^2)$, whose first-order terms cancel in the sum,

$$\int_l^r f - S_2 = -\frac{(h/2)^5}{2880}\bigl(2 f^{(4)}(c) + O(h^2)\bigr) + O(h^7) = -\frac{h^5}{16 \cdot 2880} f^{(4)}(c) + O(h^7).$$

Subtracting the two expansions gives $S_2 - S_1 = -\frac{15}{16} \cdot \frac{h^5}{2880} f^{(4)}(c) + O(h^7)$, so $(S_2 - S_1)/15 = -\frac{h^5}{16 \cdot 2880} f^{(4)}(c) + O(h^7)$, which is the error of $S_2$ up to $O(h^7)$. $\square$

So, when $f^{(4)}(c) \ne 0$, the ratio of $e$ to the true error of $S_2$ tends to $1$ as $h \to 0$. This is an asymptotic statement only. It gives no bound for a fixed panel, and it needs $f \in C^6$ on the panel. When the hypothesis fails, for example on $[0, h]$ for $f(x) = \sqrt{x}$, the error of $S_2$ scales like $h^{3/2}$, the right divisor would be $2^{3/2} - 1 \approx 1.83$ instead of $15$, and $e$ is too small. When $f$ is small at all sample points, $S_1 = S_2$ and $e = 0$ whatever the integral is. So the bound $\sum_H e \le \tau$ that the algorithm reaches is a heuristic estimate of the error, not a guarantee. $\blacksquare$
