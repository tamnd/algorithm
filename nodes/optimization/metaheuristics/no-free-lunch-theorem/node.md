---
tag: MA8DGV
kind: theorem
slug: no-free-lunch-theorem
name: No free lunch theorem
aliases:
- NFL theorems
- no free lunch theorems for optimization
- sharpened no free lunch theorem
area: optimization/metaheuristics
level: advanced
summary: Over all functions on a finite set, every search algorithm sees the same values as often. This holds exactly for the sets of functions closed under permutation of the inputs.
prereqs: [black-box-optimization, query-model]
see_also: [global-optimization, fitness-function, metaheuristic, local-search, simulated-annealing, genetic-algorithm, lower-bound]
sources:
  - paper: doi:10.1109/4235.585893
    title: David H. Wolpert and William G. Macready, No free lunch theorems for optimization, IEEE Transactions on Evolutionary Computation 1(1), 1997
    locator: pages 67 to 82, Section III (Theorem 1, the sum over all functions does not depend on the algorithm)
  - paper: "Christopher Schumacher, Michael D. Vose and L. Darrell Whitley, The no free lunch and problem description length, Proceedings of the Genetic and Evolutionary Computation Conference (GECCO 2001), Morgan Kaufmann, 2001"
    title: Christopher Schumacher, Michael D. Vose and L. Darrell Whitley, The no free lunch and problem description length
    locator: the main theorem (no free lunch holds for a set of functions if and only if the set is closed under permutation)
  - paper: "Christian Igel and Marc Toussaint, A no-free-lunch theorem for non-uniform distributions of target functions, Journal of Mathematical Modelling and Algorithms 3(4), 2004"
    title: Christian Igel and Marc Toussaint, A no-free-lunch theorem for non-uniform distributions of target functions
    locator: pages 313 to 322 (the condition on the distribution, and the fraction of subsets that are closed under permutation)
  - paper: "Anne Auger and Olivier Teytaud, Continuous lunches are free plus the design of optimal optimization algorithms, Algorithmica 57(1), 2010"
    title: Anne Auger and Olivier Teytaud, Continuous lunches are free plus the design of optimal optimization algorithms
    locator: pages 121 to 146 (the case of continuous domains)
---

The no free lunch (NFL) theorem says that, when all functions from a finite set $X$ to a finite set $Y$ count equally, every [black-box](/black-box-optimization/) search algorithm has the same distribution of observed values, and so the same average performance under any measure that depends only on these values. Wolpert and Macready proved it in 1997. Schumacher, Vose and Whitley sharpened it in 2001: the same conclusion holds for a set $F$ of functions if and only if $F$ is closed under permutation of the inputs. So a claim that one search method is better than another is a claim about a class of functions that is not closed under permutation, and it must name that class.

## Statement

Let $X$ and $Y$ be finite sets, with $|X| = N$ and $|Y| = k$, and let a function be any $f : X \to Y$. A *deterministic non-revisiting algorithm* $a$ with $m \le N$ steps chooses a point $x_1 \in X$, and for $t = 1, \dots, m - 1$ chooses a point $x_{t+1}$ that is not in $\{x_1, \dots, x_t\}$ as a function of the values $(f(x_1), \dots, f(x_t))$ seen so far. Its *trace* on $f$ is the sequence $T_a(f) = (f(x_1), \dots, f(x_m)) \in Y^m$. A *performance measure* is any function $\Phi : Y^m \to \mathbb{R}$, for example the least value seen, or the first $t$ at which a given value appears.

A set $F$ of functions is *closed under permutation* (c.u.p.) if $f \circ \sigma \in F$ for every $f \in F$ and every bijection $\sigma : X \to X$.

**Theorem (Wolpert and Macready 1997).** Let $F = Y^X$ be the set of all $k^N$ functions. For every algorithm $a$ with $m$ steps and every $y \in Y^m$, the number of $f \in F$ with $T_a(f) = y$ is $k^{N-m}$. Hence for any two algorithms $a$ and $b$ with $m$ steps and any $\Phi$,
$$\sum_{f \in F} \Phi(T_a(f)) = \sum_{f \in F} \Phi(T_b(f)).$$

**Theorem (sharpened NFL, Schumacher, Vose and Whitley 2001).** Let $F \subseteq Y^X$ be any set of functions. The following are equivalent.

1. $F$ is closed under permutation.
2. For every $m \le N$ and every two algorithms $a$ and $b$ with $m$ steps, the multisets $\{T_a(f) : f \in F\}$ and $\{T_b(f) : f \in F\}$ are equal. So $\sum_{f \in F} \Phi(T_a(f)) = \sum_{f \in F} \Phi(T_b(f))$ for every $\Phi$.
3. Statement 2 holds for $m = N$.

## In plain words

Suppose you must find the lowest point of an unknown landscape, and you can only ask for the height at one spot at a time. Some search rules look clever. This theorem says that, if every possible landscape is just as likely, no rule is better than any other, and none is better than picking spots at random. A rule that wins on some landscapes loses by the same amount on the others.

The sharper form says exactly when this happens. It happens when the set of landscapes you care about stays the same after you shuffle the spots. If your landscapes have some order, for example if close spots tend to have close heights, then the set changes under a shuffle, and a rule that uses that order can win.

## Proof

**The count over all functions.** Fix $a$ with $m$ steps and $y = (y_1, \dots, y_m) \in Y^m$. Since $a$ is deterministic and its choices depend only on the values seen, the points it would visit if it saw $y$ are fixed: $x_1$ is the first choice, $x_2$ is the choice after $y_1$, and so on. They are distinct, since $a$ does not revisit. Now $T_a(f) = y$ holds if and only if $f(x_t) = y_t$ for $t = 1, \dots, m$. To see the "if" part, use induction on $t$: if $f$ has these values, then $a$ on $f$ sees $y_1, \dots, y_{t}$ and so goes to $x_{t+1}$. The "only if" part holds because $a$ on $f$ visits $x_1, \dots, x_m$ when it sees $y$. So the functions with trace $y$ are exactly those with $m$ fixed values on $m$ fixed points and any values on the other $N - m$ points. There are $k^{N-m}$ of them, a number that does not depend on $a$. Then
$$\sum_{f \in F} \Phi(T_a(f)) = \sum_{y \in Y^m} \Phi(y) \cdot \#\{f : T_a(f) = y\} = k^{N-m} \sum_{y \in Y^m} \Phi(y),$$
which is the same for every algorithm.

**Closed under permutation implies equal multisets (1 implies 2).** Fix $m$ and two algorithms $a$ and $b$. Fix also an order on $X$. For $f \in F$, run $a$ on $f$. It visits $x_1, \dots, x_m$ and sees $y = T_a(f)$. Now let $b$ "see" the same values: let $x'_1$ be the first choice of $b$, let $x'_2$ be its choice after the value $y_1$, and so on. The points $x'_1, \dots, x'_m$ are distinct. Let $\sigma$ be the bijection of $X$ that maps $x'_t$ to $x_t$ for each $t$, and maps the other points $X \setminus \{x'_t\}$ to the other points $X \setminus \{x_t\}$ in increasing order. Define $\varphi(f) = f \circ \sigma$. Then $\varphi(f) \in F$, since $F$ is c.u.p., and $\varphi(f)(x'_t) = f(x_t) = y_t$. By the same induction as above, $b$ on $\varphi(f)$ visits $x'_1, \dots, x'_m$ and sees $y$, so $T_b(\varphi(f)) = T_a(f)$.

Define $\psi : F \to F$ in the same way with the roles of $a$ and $b$ exchanged. For $f \in F$, the run of $b$ on $\varphi(f)$ sees $y$, and $a$ fed with $y$ visits $x_1, \dots, x_m$, the same points as $a$ on $f$. So the bijection built for $\psi$ maps $x_t$ to $x'_t$ and the other points in increasing order, which is $\sigma^{-1}$. Hence $\psi(\varphi(f)) = f \circ \sigma \circ \sigma^{-1} = f$. In the same way $\varphi(\psi(g)) = g$. So $\varphi$ is a bijection of $F$ with $T_b \circ \varphi = T_a$, and the two multisets of traces are equal. Summing $\Phi$ over them gives the equality of the sums.

**2 implies 3.** Take $m = N$.

**Equal multisets for full traces implies closed under permutation (3 implies 1).** For a bijection $\pi$ of $\{1, \dots, N\}$ onto $X$, the algorithm $a_\pi$ that visits $\pi(1), \dots, \pi(N)$ in this order, whatever it sees, is deterministic and non-revisiting, and $T_{a_\pi}(f) = (f(\pi(1)), \dots, f(\pi(N)))$. Fix one such $\pi_0$. For any bijection $\sigma$ of $X$, statement 3 for $a_{\pi_0}$ and $a_{\sigma \circ \pi_0}$ says that the multisets $\{f \circ \pi_0 : f \in F\}$ and $\{f \circ \sigma \circ \pi_0 : f \in F\}$ are equal. Both are sets with no repeats, since $f \mapsto f \circ \pi_0$ is injective. Since composing with $\pi_0^{-1}$ on the right is also injective, $\{f : f \in F\} = \{f \circ \sigma : f \in F\}$ as sets. So $f \circ \sigma \in F$ for every $f \in F$, which is statement 1. $\square$

**Randomized and revisiting algorithms.** On a finite problem, a randomized algorithm that uses its random bits only to make its choices is a probability mixture of deterministic algorithms, so the equalities hold for the expected value of $\Phi$. An algorithm that revisits points gains nothing from a revisit. The theorem applies to it if $\Phi$ is computed on the sequence of distinct points only, as Wolpert and Macready do.

## Consequences

- **Average over all functions.** For every algorithm, the mean of $\Phi$ over $Y^X$ equals the mean for random search without repeats. On the $3^4 = 81$ functions from 4 points to $\{0, 1, 2\}$, all 55296 deterministic non-revisiting algorithms with 4 steps need on average $158/81 \approx 1.95$ evaluations to first see the least value of the function. The implementation checks this kind of equality for every algorithm on small domains.
- **Conservation.** If $a$ beats $b$ on a set $G \subset F$ of functions, with $F$ c.u.p., then $b$ beats $a$ by the same total on $F \setminus G$, since the two sums over $F$ are equal.
- **Free lunches exist on structured classes.** Let $F$ be the 15 nondecreasing functions from $\{0, 1, 2, 3\}$ to $\{0, 1, 2\}$. This set is not c.u.p. The algorithm that evaluates the point 0 first sees the least value in 1 evaluation on every function in $F$. The order $3, 2, 1, 0$ needs $41/15 \approx 2.73$ evaluations on average, the worst of all 55296 algorithms. A method that uses the order of the domain, like the local moves of [hill climbing](/hill-climbing/), can only gain on classes like this one.
- **Closed classes are rare.** A set is c.u.p. if and only if it is a union of orbits $\{f \circ \sigma\}$, and an orbit is fixed by the number of points that take each value. There are $\binom{N + k - 1}{k - 1}$ orbits, so $2^{\binom{N+k-1}{k-1}}$ of the $2^{k^N}$ subsets of $Y^X$ are c.u.p. For $N = 3$ and $k = 2$ this is 16 of 256. For $N = 4$ and $k = 3$ it is $2^{15}$ of $2^{81}$. Igel and Toussaint used such counts to argue that the classes met in practice are almost never c.u.p.
- **Closed classes that are not all functions.** The 4 needle functions on 4 points, with value 0 at one point and 1 at the others, form a c.u.p. set. On it every algorithm needs $(1 + 2 + 3 + 4)/4 = 2.5$ evaluations on average to find the needle. No cleverness helps on a needle in a haystack.
- **Non-uniform distributions.** Igel and Toussaint showed that the equality of expected performance under a distribution $p$ on $F$ holds for all algorithms if and only if $p(f) = p(f \circ \sigma)$ for all $f$ and $\sigma$. A distribution that prefers smooth functions breaks it.

## Tightness

The sharpened theorem is an equivalence, so its hypothesis cannot be weakened for full traces. For a fixed $m < N$ the equality can hold on a set that is not c.u.p.: on 3 points with values in $\{0, 1\}$, the set $\{(0, 1, 0), (1, 0, 1)\}$ is not c.u.p., but with $m = 1$ every algorithm sees the value 0 once and the value 1 once. The theorem needs a finite $X$ and $Y$. On continuous domains the natural analogues are different: Auger and Teytaud showed that for random fitness functions on continuous domains, NFL in this strong form does not hold. The theorem also does not apply when the algorithm knows more than the values, for example a gradient or the formula of $f$, or when the performance measure depends on the points and not only on the values.

## History

Wolpert and Macready circulated the result as a Santa Fe Institute report in 1995 and published it in the IEEE Transactions on Evolutionary Computation in 1997. They used the name from the saying "there is no such thing as a free lunch". Radcliffe and Surry gave a related result for search in 1995. Schumacher, Vose and Whitley proved the equivalence with closure under permutation in 2001. Igel and Toussaint extended it to non-uniform distributions in 2004, and Auger and Teytaud studied continuous domains in 2007 and 2010.

## References
