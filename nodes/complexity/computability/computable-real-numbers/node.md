---
tag: 6ZM0MB
kind: definition
slug: computable-real-numbers
name: Computable real numbers
aliases:
- computable reals
area: complexity/computability
level: advanced
summary: "A real x is computable if a Turing machine outputs, for each n, a rational within 2^-n of x. Decimal digits give the same reals, but addition is not computable on decimal expansions."
prereqs: [computable-function]
see_also: [computable-function, chaitins-constant, uncomputable-function, interval-arithmetic, real-ram, floating-point-arithmetic, bisection-method, countability]
sources:
  - paper: doi:10.1112/plms/s2-42.1.230
    title: "Alan M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proceedings of the London Mathematical Society (2) 42 (1936), with a correction in volume 43 (1937), pp. 544 to 546"
    locator: "pp. 230 to 265, the introduction and Section 10 (examples of large classes of computable numbers), and the correction (representation by nested intervals)"
  - paper: doi:10.2307/2267043
    title: "Ernst Specker, Nicht konstruktiv beweisbare Sätze der Analysis, Journal of Symbolic Logic 14(3) (1949)"
    locator: "pp. 145 to 158 (a bounded increasing computable sequence of rationals with no computable limit)"
  - paper: doi:10.1090/S0002-9939-1954-0063328-5
    title: "Henry Gordon Rice, Recursive real numbers, Proceedings of the American Mathematical Society 5(5) (1954)"
    locator: "pp. 784 to 791 (the computable reals form a field)"
  - book: isbn:9783540668176
    title: "Klaus Weihrauch, Computable Analysis, An Introduction, Springer, 2000"
    locator: "Chapter 4, Computability on the Real Numbers"
---

A real number is computable if some algorithm approximates it to any requested precision. The standard definition uses fast Cauchy sequences: $x$ is computable if a [computable function](/computable-function/) maps each $n$ to a rational $q_n$ with $|q_n - x| \le 2^{-n}$. All the usual constants, such as $\sqrt{2}$, $\pi$ and $e$, are computable, and so are sums, products, quotients and roots of computable reals. There are only countably many algorithms, so almost every real is not computable. Turing defined computable numbers in 1936 by their decimal expansions. A real has a computable decimal expansion exactly when it is computable in the sense above, so the two definitions give the same set of reals. The decimal form is still the wrong way to compute with them: no algorithm adds two reals given as decimal digit streams. Turing changed the representation in his correction of 1937. In the form used today, computing with reals means computing with approximations, and equality of two computable reals is not decidable.

## Definition

**Computable real.** A real number $x$ is *computable* if there is a total computable function $n \mapsto q_n$ from $\mathbb{N}$ to the rationals, each $q_n$ given as a pair of integers, such that
$$|q_n - x| \le 2^{-n} \quad \text{for all } n.$$
The sequence $(q_n)$ is a *fast Cauchy sequence* for $x$, and an index of a machine that computes it is a *name* of $x$. A real has infinitely many names.

**Equivalent definitions.** For a real $x$ the following are equivalent:

1. $x$ has a computable fast Cauchy sequence;
2. there is a computable sequence of nested closed intervals with rational end points and lengths going to $0$ whose intersection is $\{x\}$;
3. the left cut $\{ q \in \mathbb{Q} : q < x \}$ is a [decidable](/decidable-language/) set;
4. $x$ has a computable decimal expansion (or a computable expansion in any fixed base $b \ge 2$).

The equivalence of 4 with the others is not uniform. If $x$ is rational, its expansion is computable by long division. If $x$ is irrational, approximations of $x$ eventually show which digit interval it lies in, since $x$ is never on a boundary between two such intervals. No single algorithm turns every name of $x$ into its digits, because it cannot tell whether $x$ sits on a boundary such as $1 = 0.999\ldots$.

**Representations.** A *representation* of the reals is a way to give a real to a machine as an infinite input. Fast Cauchy sequences, nested intervals and signed-digit expansions (base 2 with digits $-1, 0, 1$) are the standard representations of computable analysis, and they can be converted into each other by algorithms. Decimal and binary expansions are also representations, but they are not equivalent to these: algorithms can go from digits to a Cauchy sequence but not back.

**Computable function on reals.** A function $f : \mathbb{R} \to \mathbb{R}$ is computable if one machine, given any fast Cauchy sequence for $x$ as an oracle, outputs a fast Cauchy sequence for $f(x)$. To output $q_n$ it reads only finitely many terms of the input.

## Examples and non-examples

**$\sqrt{2}$.** Let $q_n = \lfloor \sqrt{2 \cdot 4^n} \rfloor / 2^n$, computed with integer arithmetic only. Since $a = \lfloor \sqrt{2 \cdot 4^n} \rfloor$ satisfies $a^2 \le 2 \cdot 4^n < (a + 1)^2$, the rational $q_n$ is at most $\sqrt{2}$ and less than $q_n + 2^{-n}$, so $|q_n - \sqrt{2}| < 2^{-n}$. The values are $q_0 = 1$, $q_2 = 5/4$, $q_5 = 45/32$, $q_{10} = 181/128 = 1.4140625$ and $q_{20} = 741455/524288 \approx 1.4142132$. The same method of exact integer bounds works for every algebraic number.

**$\pi$ and $e$.** Series with a known error bound give fast Cauchy sequences, for example Machin's formula $\pi = 16 \arctan(1/5) - 4 \arctan(1/239)$ with the alternating-series bound on each arctangent, or $e = \sum 1/k!$, where the tail after the term $1/k!$ is below $2/(k+1)!$. Turing noted in 1936 that the computable numbers include the real parts of all algebraic numbers, $\pi$, $e$ and the real parts of the zeros of the Bessel functions.

**Field operations.** If $x$ and $y$ are computable, so are $x + y$, $x - y$, $xy$, and $x / y$ for $y \ne 0$. For $x + y$, output $p_{n+1} + q_{n+1}$, where $p$ and $q$ are names of $x$ and $y$. For $x / y$, first search for an $m$ with $|q_m| > 2^{-m}$, which ends because $y \ne 0$, and then use a precision that depends on $m$. Rice (1954) proved that the computable reals form a field.

**Addition of decimal expansions.** Let $a = 0.333\ldots$ and $b = 0.666\ldots$, given as digit streams. After reading $k$ digits of each, a machine knows only that $a + b$ lies between $0.99\ldots9$ and $1.00\ldots01$, with $k$ digits after the point, for every $k$. If it outputs the first digit $0$, the next digits of $a$ could be all $4$s, making $a + b > 1$. If it outputs $1$, the next digits could be all $2$s, making $a + b < 1$. So no machine outputs the decimal expansion of $a + b$ from those of $a$ and $b$, even though $a$, $b$ and $a + b = 1$ are all computable. With fast Cauchy sequences or signed digits, addition is computable.

**Non-example: a real that codes the halting problem.** Let $x_K = \sum_{n \in K} 2^{-(n+1)}$, where $K$ is the [halting](/halting-problem/) set. Its binary digits are the characteristic sequence of $K$, so it is not computable. It is still the limit of the increasing computable sequence $x_s = \sum_{n \in K_s} 2^{-(n+1)}$, where $K_s$ is the set of $n < s$ with $\varphi_n(n)$ halting within $s$ steps. Such reals are called *left-c.e.*: they can be approximated from below, but no algorithm says how close the approximation is. [Chaitin's constant](/chaitins-constant/) is another left-c.e. real that is not computable.

**Specker's theorem.** Specker (1949) built a bounded increasing computable sequence of rationals whose limit is not computable. So the monotone convergence theorem fails if "real" means "computable real". The sequence $x_s$ above is an example of the same kind.

**Countability.** Every computable real has a name, and names are natural numbers, so the computable reals are [countable](/countability/). The real line is not, so most reals are not computable.

**Equality is not decidable.** No algorithm decides, for names of two computable reals $x$ and $y$, whether $x = y$. For a machine index $e$, let $x_e = 2^{-s}$ if $\varphi_e(e)$ halts at step $s$, and $x_e = 0$ if it never halts; $x_e$ is computable from $e$, and $x_e = 0$ exactly when $e \notin K$. The relation $x \ne y$ is c.e.: search for an $n$ with $|p_n - q_n| > 2^{1-n}$, where $p$ and $q$ are names of $x$ and $y$. In the same way $x < y$ is c.e.: search for an $n$ with $q_n - p_n > 2^{1-n}$.

**Continuity.** Every computable function on the reals is continuous, because each output approximation depends on finitely many input terms (Weihrauch, Chapter 4). So the floor function, the sign function and the test $x = 0$ are not computable on all of $\mathbb{R}$.

## Related definitions

- [Computable function](/computable-function/): a computable real is a total computable function from $\mathbb{N}$ to $\mathbb{Q}$ that meets the precision condition.
- [Real RAM](/real-ram/): the model of computational geometry, which stores exact reals and compares them in one step. It allows the test $x = 0$, which a machine on computable reals cannot carry out.
- [Interval arithmetic](/interval-arithmetic/): computing with rational intervals that contain the true value is the nested-interval representation, run to a fixed precision.
- [Floating-point arithmetic](/floating-point-arithmetic/): a fixed-precision approximation, with no guarantee that the error goes to $0$.
- [Bisection method](/bisection-method/): finds a root of a continuous function with a sign change; on computable reals it needs care at points where the sign is $0$, because that test is not computable.
- [Chaitin's constant](/chaitins-constant/) and [uncomputable functions](/uncomputable-function/): examples of reals and functions outside the computable ones.

## References
