---
tag: 5CZD19
kind: technique
slug: polynomial-method
name: Polynomial method
aliases:
- polynomial degree lower bound
area: complexity/communication-and-query-complexity
level: advanced
summary: "A query lower bound: after T queries, the acceptance probability is a polynomial of degree at most 2T in the input, so f needs at least half its approximate degree in quantum queries."
prereqs: [approximate-degree, quantum-query-model]
see_also: [approximate-degree, quantum-query-complexity, quantum-adversary-method, grover-optimality, block-sensitivity, parity-problem, majority-problem, element-distinctness]
sources:
  - paper: doi:10.1145/502090.502097
    title: Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de Wolf, Quantum lower bounds by polynomials, Journal of the ACM 48(4) (2001)
    locator: pp. 778 to 797 (amplitudes after T queries have degree at most T; Q(f) at least half the approximate degree; bounds for OR, PARITY and symmetric functions)
  - paper: doi:10.1007/BF01263419
    title: Noam Nisan and Mario Szegedy, On the degree of Boolean functions as real polynomials, Computational Complexity 4(4) (1994)
    locator: pp. 301 to 313 (bs(f) at most 2 deg(f)^2, the approximate version, and the lemma of Ehlich and Zeller and of Rivlin and Cheney)
  - paper: doi:10.1145/129712.129758
    title: Ramamohan Paturi, On the degree of polynomials that approximate symmetric Boolean functions, 24th ACM Symposium on Theory of Computing (STOC 1992)
    locator: pp. 468 to 474 (approximate degree of symmetric functions)
  - paper: doi:10.1145/1008731.1008735
    title: Scott Aaronson and Yaoyun Shi, Quantum lower bounds for the collision and the element distinctness problems, Journal of the ACM 51(4) (2004)
    locator: pp. 595 to 605 (Omega(n^(1/3)) for collision and Omega(n^(2/3)) for element distinctness)
  - paper: doi:10.1016/j.jcss.2005.06.006
    title: Andris Ambainis, Polynomial degree vs. quantum query complexity, Journal of Computer and System Sciences 72(2) (2006)
    locator: pp. 220 to 238 (a total function whose quantum query complexity is polynomially larger than its degree)
  - paper: doi:10.1016/S0304-3975(01)00144-X
    title: Harry Buhrman and Ronald de Wolf, Complexity measures and decision tree complexity, a survey, Theoretical Computer Science 288(1) (2002)
    locator: pp. 21 to 43; Section 4.3 (degree and symmetrization), Section 4.4 (approximate degree), Section 5.3 (quantum query complexity)
---

The polynomial method proves lower bounds on the number of queries by turning an algorithm into a polynomial. After $T$ queries, the acceptance probability of a quantum algorithm is a real polynomial of degree at most $2T$ in the input bits, so an algorithm that computes $f$ with error $1/3$ gives a polynomial that approximates $f$, and $Q(f) \ge \widetilde{\deg}(f)/2$. A lower bound on the [approximate degree](/approximate-degree/) then comes from approximation theory: symmetrization reduces the problem to one variable, and the inequalities of Markov and Chebyshev bound the degree. This page is the technique; the approximate degree page is the measure that it bounds.

## In plain words

A quantum algorithm reads its input by asking about bits. Each question can multiply the answer formula by at most one more input bit. So after a few questions, the chance that the algorithm says "yes" is a formula with only small powers of the input. If the algorithm is mostly right, this formula is close to the true answer on every input. To prove that many questions are needed, show that every formula close to the right answers must have a high power. For that, average the formula over inputs that look alike, which leaves a formula in one number. A formula in one number that stays small on many points but jumps between two neighbours must have a high power.

## When it applies

- **Query models.** The input is reached only by queries, and the cost is their number: deterministic, randomized and quantum query algorithms, and also protocols built on them. The degree lemma holds in each case: $D^{dt}(f) \ge \deg(f)$, $R(f) \ge \widetilde{\deg}(f)$, $Q_E(f) \ge \deg(f)/2$ and $Q(f) \ge \widetilde{\deg}(f)/2$.
- **Symmetric problems.** The second half of the method is easiest when $f$ is symmetric, or can be made symmetric by a reduction, so that the polynomial depends only on the Hamming weight. OR, PARITY, MAJORITY, threshold functions, block sensitivity and collision problems all fit.
- **Partial functions.** The polynomial only has to be close to $f$ on the promise set. The method still applies, and it gives the best known bounds for collision and element distinctness.
- **Not for time or space.** It counts queries only, so it gives no bound on the time or space of a computation once the input bits are known.

## The template

**Step 1, the degree lemma (Beals et al.).** Write the quantum query as $O_x \lvert i, b, w \rangle = \lvert i, b \oplus x_i, w \rangle$, where $w$ is the work space. Claim: after $t$ queries, each amplitude is a complex polynomial of degree at most $t$ in $x_1, \ldots, x_n$. At the start the amplitudes are constants. A unitary that does not depend on $x$ makes each new amplitude a fixed linear combination of old ones, so the degree does not grow. A query maps the amplitude $\alpha_{i,b,w}$ to $(1 - x_i) \alpha_{i,b,w} + x_i \alpha_{i, 1-b, w}$, which raises the degree by at most one. The acceptance probability is the sum of $|\alpha|^2 = (\mathrm{Re}\,\alpha)^2 + (\mathrm{Im}\,\alpha)^2$ over accepting basis states, a real polynomial of degree at most $2T$. Using $x_i^2 = x_i$ makes it multilinear without raising the degree.

So an algorithm with error at most $1/3$ gives $P$ with $|P(x) - f(x)| \le 1/3$ and $\deg(P) \le 2T$, which is $Q(f) \ge \widetilde{\deg}(f)/2$. An exact algorithm gives $P = f$, so $Q_E(f) \ge \deg(f)/2$. A deterministic tree of depth $T$ gives $P$ of degree $T$ directly, as the sum over 1-leaves of products of $x_i$ and $1 - x_i$, and a randomized one gives an average of these.

**Step 2, symmetrization (Minsky and Papert).** Let $p$ be multilinear on $\{0,1\}^m$. Average it over all permutations of the variables: the result is $\sum_j c_j V_j(y)$ with $V_j(y) = \sum_{|S| = j} \prod_{i \in S} y_i$ and $j \le \deg(p)$. Since $V_j(y) = \binom{|y|}{j}$, a polynomial of degree $j$ in $|y|$, there is a univariate $q$ with $\deg(q) \le \deg(p)$ and $q(k)$ equal to the average of $p$ over the inputs of weight $k$. If $p$ satisfies bounds that hold on whole weight classes, $q$ satisfies them at the integers $k$.

**Step 3, the lemma (Ehlich and Zeller; Rivlin and Cheney).** Let $q$ be a real polynomial of degree $d$, let $N \ge 1$ be an integer, let $b_1 \le q(i) \le b_2$ for $i = 0, 1, \ldots, N$, and let $|q'(\xi)| \ge c > 0$ for some $\xi \in [0, N]$. Then

$$d \ge \sqrt{\frac{c N}{c + b_2 - b_1}}.$$

*Proof.* Markov's inequality for derivatives says: if $|r(t)| \le M$ on $[-1, 1]$ and $\deg(r) \le d$, then $|r'(t)| \le d^2 M$ there. On $[0, N]$, after the change of variable $t \mapsto 2t/N - 1$, this reads $|r'| \le 2 d^2 M / N$. Let $m = (b_1 + b_2)/2$, let $D = \max_{[0, N]} |q - m|$, and let $\lambda = \max_{[0, N]} |q'|$. Markov's inequality applied to $q - m$ gives $\lambda \le 2 d^2 D / N$. Each $t \in [0, N]$ is within $1/2$ of an integer $i \in [0, N]$, where $|q(i) - m| \le (b_2 - b_1)/2$, so by the mean value theorem $|q(t) - m| \le (b_2 - b_1)/2 + \lambda/2$. So $D \le (b_2 - b_1 + \lambda)/2$, and then $\lambda N \le d^2 (b_2 - b_1 + \lambda)$, that is, $d^2 \ge \lambda N / (\lambda + b_2 - b_1)$. The right side grows with $\lambda$, and $\lambda \ge c$, which gives the claim. $\square$

```pseudo id=main
POLYNOMIAL-METHOD(f, model)
L1  from an algorithm with T queries, get P with deg(P) ≤ ⟨k⟩·T     ▷ k = 1 classical, k = 2 quantum
L2  from correctness, get |P(x) - f(x)| ≤ ⟨ε⟩ on the domain of f
L3  restrict P along ⟨reduction⟩ to a function of m new bits, without raising the degree
L4  average over ⟨symmetry⟩ to get q(k) with deg(q) ≤ deg(P), for k = 0, ..., N
L5  read off ⟨constraints⟩: bounds b_1 ≤ q(k) ≤ b_2 and a jump of c between two neighbours
L6  apply ⟨degree bound⟩: the lemma, a count of sign changes, or a dual polynomial
L7  return T ≥ d / k
```

The holes are the factor $\langle k \rangle$ of the model, the error $\langle \varepsilon \rangle$ ($0$ for exact algorithms), the $\langle$reduction$\rangle$ that makes the problem symmetric, the $\langle$symmetry$\rangle$ group, usually all permutations of the new bits, the $\langle$constraints$\rangle$ on $q$, and the $\langle$degree bound$\rangle$ that turns them into a lower bound on $d$.

## Classic examples

**OR and Grover search.** For $\mathrm{OR}_n$, no reduction is needed. Symmetrization gives $q(0) \le 1/3$ and $q(1) \ge 2/3$, so $q' \ge 1/3$ somewhere in $[0, 1]$, and $-1/3 \le q(k) \le 4/3$ at $k = 0, \ldots, n$. The lemma with $c = 1/3$ and $b_2 - b_1 = 5/3$ gives $d^2 \ge n/6$, so $Q(\mathrm{OR}_n) \ge \sqrt{n/24}$. This proves that [Grover search](/grover-search/) is optimal up to a constant factor; see [Grover optimality](/grover-optimality/) for the hybrid proof.

| $n$ | 100 | $10^4$ | $10^6$ |
|---|---|---|---|
| lower bound $\sqrt{n/24}$ | 2.04 | 20.41 | 204.12 |
| Grover, $\lfloor (\pi/4) \sqrt n \rfloor$ queries | 7 | 78 | 785 |

The constant in the lower bound is weaker than the hybrid argument, but the shape $\Theta(\sqrt n)$ is the same.

**Block sensitivity against degree (Nisan and Szegedy).** Claim: $\mathrm{bs}(f) \le 2 \deg(f)^2$ for every total $f$. Take $x$ with $b = \mathrm{bs}(f)$ disjoint sensitive blocks $B_1, \ldots, B_b$, and assume $f(x) = 0$; otherwise use $1 - f$, which has the same degree. For $y \in \{0,1\}^b$ let $g(y) = f(x^{B(y)})$, where $B(y)$ is the union of the $B_j$ with $y_j = 1$ and $x^B$ is $x$ with the bits in $B$ flipped. This is the reduction of line L3: in the polynomial of $f$, replace $x_i$ by the constant $x_i$ if $i$ is in no block, by $y_j$ if $i \in B_j$ and $x_i = 0$, and by $1 - y_j$ if $i \in B_j$ and $x_i = 1$. Each replacement has degree at most 1, so $\deg(g) \le \deg(f)$. Now $g(0) = f(x) = 0$, $g(e_j) = f(x^{B_j}) = 1$ for each unit vector $e_j$, and $g$ takes values in $\{0, 1\}$. Symmetrize $g$ over the permutations of the $b$ new bits: $q(0) = 0$, $q(1) = 1$ and $0 \le q(k) \le 1$ for $k = 0, \ldots, b$. By the mean value theorem $q'(\xi) = 1$ for some $\xi \in [0, 1]$. The lemma with $N = b$, $c = 1$ and $b_2 - b_1 = 1$ gives $\deg(f)^2 \ge \deg(q)^2 \ge b/2$. $\square$

With an approximating polynomial the same steps give $q(0) \le 1/3$, $q(1) \ge 2/3$ and $-1/3 \le q(k) \le 4/3$, so $c = 1/3$, $b_2 - b_1 = 5/3$, and $\mathrm{bs}(f) \le 6 \, \widetilde{\deg}(f)^2$. With Step 1 this gives $Q(f) \ge \sqrt{\mathrm{bs}(f)/24}$ for every total $f$; see [block sensitivity](/block-sensitivity/).

**PARITY.** For the [parity problem](/parity-problem/), symmetrization gives $q(k) \le 1/3$ at even $k$ and $q(k) \ge 2/3$ at odd $k$, for $k = 0, \ldots, n$. Here line L6 uses a count of sign changes instead of the lemma: $q - 1/2$ changes sign $n$ times, so $\deg(q) \ge n$ and $Q(\mathrm{PARITY}_n) \ge n/2$. The pairing algorithm makes $\lceil n/2 \rceil$ queries, so the bound is exact.

**MAJORITY and symmetric functions.** For the [majority problem](/majority-problem/), the jump is at the middle weight, where the lemma gives a bound of only order $\sqrt n$ if applied directly to $[0, n]$. Paturi's sharper analysis gives $\widetilde{\deg}(f) = \Theta(\sqrt{n (n - \Gamma(f))})$ for every symmetric $f$, where $\Gamma(f)$ is the distance of the jump from the middle, so $Q(\mathrm{MAJ}_n) = \Theta(n)$.

**Collision and element distinctness (Aaronson and Shi).** For the collision problem, a function on $n$ points that is either one-to-one or two-to-one, the reduction of line L3 is to a family of inputs that depend on a few integer parameters, and the symmetry is over relabellings of the domain and range. The result is a polynomial in a few variables, and a lemma of the same kind gives $\Omega(n^{1/3})$ queries. A reduction then gives $\Omega(n^{2/3})$ for [element distinctness](/element-distinctness/). Both bounds are tight.

## Variations

- **Exact and one-sided algorithms.** An exact algorithm gives $P = f$, and the bound uses $\deg(f)$. An algorithm that never errs on 0-inputs gives $P(x) = 0$ there, which leads to the one-sided approximate degree.
- **Dual polynomials.** Instead of symmetrization, write the approximate degree as a linear program and exhibit a dual solution: a function $\psi$ that has correlation more than $\varepsilon$ with $f$ and zero correlation with every polynomial of degree at most $d$. By [LP duality](/lp-duality/) this proves $\widetilde{\deg}_\varepsilon(f) > d$. This variant handles functions that are not symmetric, such as compositions; see [approximate degree](/approximate-degree/).
- **Threshold degree.** If only the sign of $P - 1/2$ must be right, the measure is the threshold degree. This bounds unbounded-error algorithms and gives the lower bounds of Minsky and Papert for the [perceptron](/perceptron/), where PARITY needs degree $n$.
- **Communication complexity.** Lower bounds on approximate degree and its dual polynomial lift to lower bounds for [communication complexity](/communication-complexity/), and threshold degree lifts to [sign rank](/sign-rank/).
- **The other main method.** The [quantum adversary method](/quantum-adversary-method/) bounds how fast the states for different inputs can move apart; it is not the classical [adversary argument](/adversary-argument/). The two quantum methods are incomparable: each one gives a stronger bound than the other for some functions.

## Pitfalls

- **The factor two.** The acceptance probability has degree at most $2T$, not $T$, because it is a sum of squared amplitudes. The bound is $Q(f) \ge \widetilde{\deg}(f)/2$.
- **Averaging needs uniform constraints.** Symmetrization keeps a bound only if it holds on the whole weight class. If $f$ is not symmetric, a reduction must first make the constraints depend on the weight alone, as in the block sensitivity proof.
- **Values between the integers.** The constraints hold only at integer points, and $q$ can be large between them. The lemma accounts for this with the term $\lambda/2$; a proof that applies Markov's inequality directly to the integer bounds is wrong.
- **Not always tight.** The degree can be much smaller than the query complexity. Ambainis (2006) gave a total function whose quantum query complexity is polynomially larger than its degree.
- **Other methods with the same name.** The polynomial method of combinatorics, as in Dvir's proof of the finite field Kakeya conjecture, and the method of Razborov and Smolensky for circuits with modular gates, are different techniques. They use polynomials over finite fields, not real approximation.

## Exercises

1. Show that $\deg(\mathrm{AND}_n) = n$ and $\widetilde{\deg}(\mathrm{AND}_n) = \widetilde{\deg}(\mathrm{OR}_n)$, using $\mathrm{AND}_n(x) = 1 - \mathrm{OR}_n(1 - x_1, \ldots, 1 - x_n)$.
2. Show that a deterministic decision tree of depth $T$ computes a polynomial of degree at most $T$, and deduce $D^{dt}(f) \ge \deg(f)$. Use it to show $D^{dt}(\mathrm{OR}_n) = n$.
3. Let $f$ be symmetric with $f(0) \ne f(1)$. Use the lemma to show $\widetilde{\deg}(f) \ge \sqrt{n/6}$.
4. Show that $\mathrm{EXACT}_k$, the function that is 1 when $|x| = k$, has $Q_E(\mathrm{EXACT}_k) \ge n/2$. Hint: compute its degree with a finite difference.
5. In the proof of the lemma, where does it matter that $q$ is bounded at every integer from 0 to $N$, and not only at a few of them? Give a polynomial of degree 3 that is 0 at $k = 0, 1$ and $N$ but large at $N/2$.

## References
