---
tag: 15YWCY
kind: theorem
slug: sauer-shelah-lemma
name: Sauer-Shelah lemma
aliases:
- Sauer-Shelah-Perles lemma
- Sauer's lemma
area: machine-learning/supervised-learning
level: advanced
summary: "A class of VC dimension d realizes at most sum over i <= d of C(n, i) <= (en/d)^d labelings of n points, so its growth is polynomial in n, not exponential."
prereqs: [vc-dimension, binomial-coefficient-bounds]
see_also: [fundamental-theorem-of-statistical-learning, epsilon-net-theorem, range-space, rademacher-complexity, hypothesis-class, pac-learning]
sources:
  - paper: doi:10.1016/0097-3165(72)90019-2
    title: N. Sauer, On the density of families of sets, Journal of Combinatorial Theory, Series A 13(1), 1972
    locator: pp. 145 to 147
  - paper: doi:10.2140/pjm.1972.41.247
    title: S. Shelah, A combinatorial problem; stability and order for models and theories in infinitary languages, Pacific Journal of Mathematics 41(1), 1972
    locator: pp. 247 to 261 (the lemma, credited there also to M. Perles)
  - paper: doi:10.1137/1116025
    title: V. N. Vapnik and A. Ya. Chervonenkis, On the uniform convergence of relative frequencies of events to their probabilities, Theory of Probability and Its Applications 16(2), 1971
    locator: pp. 264 to 280 (a polynomial bound on the growth function)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, From Theory to Algorithms, Cambridge University Press, 2014
    locator: Definition 6.9 (growth function), Lemma 6.10 (Sauer-Shelah-Perles) and its proof, Section 6.7 (bibliographic remarks)
  - book: isbn:9780262039406
    title: Mehryar Mohri, Afshin Rostamizadeh and Ameet Talwalkar, Foundations of Machine Learning, second edition, MIT Press, 2018
    locator: Theorem 3.17 (Sauer's lemma) and Corollary 3.18 (the bound (em/d)^d)
  - paper: "T. M. Cover, Geometrical and statistical properties of systems of linear inequalities with applications in pattern recognition, IEEE Transactions on Electronic Computers EC-14(3), 1965"
    locator: pp. 326 to 334 (the number of labelings of points in general position by halfspaces)
---

The Sauer-Shelah lemma bounds the number of ways a binary [hypothesis class](/hypothesis-class/) can label $n$ points. If the class has [VC dimension](/vc-dimension/) $d$, it realizes at most $\sum_{i=0}^{d} \binom{n}{i}$ labelings, which is at most $(en/d)^d$ for $n \ge d$. Below $d$ points the count can be $2^n$; past $d$ it can only grow like $n^d$. Sauer (1972) and Shelah (1972, with Perles) proved it, and Vapnik and Chervonenkis (1971) had a polynomial bound of the same kind. In learning theory it is the step that turns a finite VC dimension into uniform convergence, and so into the [fundamental theorem of statistical learning](/fundamental-theorem-of-statistical-learning/).

## Statement

Let $H$ be a class of functions $X \to \{0, 1\}$. For a finite $C \subseteq X$, let $H_C$ be the set of restrictions of members of $H$ to $C$. The *growth function* is $\tau_H(n) = \max_{C \subseteq X,\ |C| = n} |H_C|$ (Shalev-Shwartz and Ben-David, Definition 6.9).

**Theorem (Sauer-Shelah-Perles).** If $\mathrm{VC}(H) \le d < \infty$, then for every $n$,
$$\tau_H(n) \le \sum_{i=0}^{d} \binom{n}{i}.$$
Moreover, for $n \ge d \ge 1$,
$$\sum_{i=0}^{d} \binom{n}{i} \le \left(\frac{en}{d}\right)^d.$$

The proof gives a stronger statement, sometimes credited to Pajor: for every finite $C$,
$$|H_C| \le |\{B \subseteq C : H \text{ shatters } B\}|. \tag{$\ast$}$$
Shalev-Shwartz and Ben-David state the lemma as Lemma 6.10, with the closed form for $n > d + 1$; Mohri, Rostamizadeh and Talwalkar give it as Theorem 3.17 and Corollary 3.18, with the closed form for $n \ge d$.

## In plain words

Suppose a family of rules can produce every colouring of some small group of points, but never of any larger group. Then, on a big set of points, the family still cannot produce most colourings. The number it can produce grows only like a fixed power of the number of points, while the number of all colourings doubles with each new point. The power is the size of the largest group the family can fully colour. So a family that fails to fully colour even a modest group behaves, on large data, like a small finite family.

## Proof

**Proof of $(\ast)$, by induction on $m = |C|$.** For $m = 1$, $C = \{c\}$. If $|H_C| = 2$, both $\emptyset$ and $\{c\}$ are shattered, and the right side is 2. If $|H_C| = 1$, the empty set is shattered, and the right side is at least 1.

Let $m \ge 2$, $C = \{c_1, \ldots, c_m\}$ and $C' = \{c_2, \ldots, c_m\}$. Split the labelings of $C'$ into two sets:

- $Y_0 = \{(y_2, \ldots, y_m) : (0, y_2, \ldots, y_m) \in H_C \text{ or } (1, y_2, \ldots, y_m) \in H_C\}$,
- $Y_1 = \{(y_2, \ldots, y_m) : (0, y_2, \ldots, y_m) \in H_C \text{ and } (1, y_2, \ldots, y_m) \in H_C\}$.

Each labeling of $C'$ that extends in one way to $C$ is counted once, and each one that extends in two ways is counted twice, so $|H_C| = |Y_0| + |Y_1|$.

*First term.* $Y_0 = H_{C'}$. By the induction hypothesis,
$$|Y_0| \le |\{B \subseteq C' : H \text{ shatters } B\}| = |\{B \subseteq C : c_1 \notin B,\ H \text{ shatters } B\}|.$$

*Second term.* Let $H' \subseteq H$ be the set of $h$ for which some $h' \in H$ agrees with $h$ on $C'$ and differs from it at $c_1$. Then $Y_1 = H'_{C'}$. If $H'$ shatters some $B \subseteq C'$, it also shatters $B \cup \{c_1\}$, because each labeling of $B$ comes from a pair of members that take both values at $c_1$. By the induction hypothesis applied to $H'$ and $C'$,
$$|Y_1| \le |\{B \subseteq C' : H' \text{ shatters } B\}| = |\{B \subseteq C' : H' \text{ shatters } B \cup \{c_1\}\}| \le |\{B \subseteq C : c_1 \in B,\ H \text{ shatters } B\}|.$$
The last step uses $H' \subseteq H$ and the map $B \mapsto B \cup \{c_1\}$, which is one to one.

Adding the two bounds gives $(\ast)$ for $C$. $\blacksquare$

**From $(\ast)$ to the lemma.** If $\mathrm{VC}(H) \le d$, no set of more than $d$ points is shattered. So every shattered $B \subseteq C$ has at most $d$ elements, and there are at most $\sum_{i=0}^{d} \binom{n}{i}$ subsets of $C$ of size at most $d$. Take the maximum over $C$ with $|C| = n$. $\blacksquare$

**The closed form.** Let $n \ge d \ge 1$. Since $d/n \le 1$, $(d/n)^d \le (d/n)^i$ for $i \le d$. Then
$$\left(\frac{d}{n}\right)^d \sum_{i=0}^{d} \binom{n}{i} \le \sum_{i=0}^{d} \binom{n}{i} \left(\frac{d}{n}\right)^i \le \sum_{i=0}^{n} \binom{n}{i} \left(\frac{d}{n}\right)^i = \left(1 + \frac{d}{n}\right)^n \le e^d,$$
by the binomial theorem and $1 + t \le e^t$. Multiply by $(n/d)^d$. $\blacksquare$ See also [binomial coefficient bounds](/binomial-coefficient-bounds/).

## Consequences

- **Dichotomy.** For every binary class, either $\tau_H(n) = 2^n$ for all $n$ (infinite VC dimension), or $\tau_H(n) \le (en/d)^d$ for $n \ge d$. There is nothing in between, such as growth like $2^{\sqrt n}$.
- **Uniform convergence.** A symmetrization argument shows that the gap $\sup_{h \in H} |L_D(h) - L_S(h)|$ depends on $H$ only through $\tau_H(2n)$. With the lemma, a class of VC dimension $d$ has, with probability at least $1 - \delta$, a gap of order $\sqrt{(d \ln(n/d) + \ln(1/\delta))/n}$ (Shalev-Shwartz and Ben-David, Theorem 6.11). This is the main step of the [fundamental theorem of statistical learning](/fundamental-theorem-of-statistical-learning/).
- **Rademacher complexity.** By Massart's lemma, the [Rademacher complexity](/rademacher-complexity/) of a class on $n$ points is at most $\sqrt{2 \ln \tau_H(n)/n}$, so at most $\sqrt{2d \ln(en/d)/n}$.
- **$\varepsilon$-nets.** In a [range space](/range-space/) of VC dimension $d$, a random sample of size $O((d/\varepsilon) \ln(1/\varepsilon) + (1/\varepsilon)\ln(1/\delta))$ is an $\varepsilon$-net with probability $1 - \delta$; see the [$\varepsilon$-net theorem](/epsilon-net-theorem/). The proof counts the ranges on a double sample with this lemma.
- **Realizable PAC bounds.** The same double sample argument with this count gives the realizable [PAC](/pac-learning/) bound $O((d \ln(1/\varepsilon) + \ln(1/\delta))/\varepsilon)$ for every consistent learner.

## Tightness

**The sum is attained.** Let $X = \{1, \ldots, n\}$ and let $H$ be the class of all labelings with at most $d$ ones. A set of $d$ points is shattered, because every labeling of it has at most $d$ ones and extends by zeros. No set of $d + 1$ points is shattered, because the all-ones labeling is missing. So $\mathrm{VC}(H) = d$ and $|H_X| = \sum_{i=0}^{d} \binom{n}{i}$, which is the bound. A natural class also attains it for $d = 2$: intervals on $n$ points of a line give the empty labeling, $n$ single points and $\binom{n}{2}$ runs of length at least 2, so $1 + n + \binom{n}{2}$ labelings.

**The exponent is right.** For $n \ge d$, $\sum_{i=0}^{d} \binom{n}{i} \ge \binom{n}{d} \ge (n/d)^d$. So $\ln \tau_H(n)$ is $d \ln(n/d) + O(d)$ in the worst case, and the closed form loses at most the factor $e^d$.

**The bound need not be attained.** Halfspaces in the plane have VC dimension 3. On $n$ points in general position they give $n^2 - n + 2$ labelings (Cover 1965), against $\sum_{i \le 3} \binom{n}{i}$, which is cubic in $n$. An exact count with the implementation of the [VC dimension](/vc-dimension/) page gives:

| $n$ | labelings by halfspaces | $n^2 - n + 2$ | $\sum_{i \le 3} \binom{n}{i}$ | $2^n$ |
|---|---|---|---|---|
| 4 | 14 | 14 | 15 | 16 |
| 5 | 22 | 22 | 26 | 32 |
| 6 | 32 | 32 | 42 | 64 |
| 8 | 58 | 58 | 93 | 256 |

**Size of the numbers.** For $d = 3$ and $n = 100$, the sum is $166751$, the closed form is about $7.44 \times 10^5$, and $2^n$ is about $1.27 \times 10^{30}$. For $d = 10$ and $n = 1000$, the sum is about $2.66 \times 10^{23}$, the closed form about $2.20 \times 10^{24}$, and $2^n$ about $1.07 \times 10^{301}$.

The implementation checks $(\ast)$ on random finite classes, checks $\tau_H(n) \le \sum_{i \le d} \binom{n}{i}$ by enumeration, checks the closed form for $1 \le d \le 11$ and $d \le n < 60$, and checks equality for the two classes above.

## History

Vapnik and Chervonenkis (1971) introduced the growth function and proved a polynomial bound on it when some size of point set is not shattered, to show uniform convergence of frequencies. In 1972 the exact bound appeared twice, independently. Sauer proved it in answer to a question of Erdős about the density of families of sets. Shelah proved it in model theory, for his work on stable theories, and credited it also to Perles. For this reason Shalev-Shwartz and Ben-David call it the Sauer-Shelah-Perles lemma. Later proofs use the inequality $(\ast)$ or a shifting argument that compresses the family without lowering its size or raising its VC dimension.

## References
