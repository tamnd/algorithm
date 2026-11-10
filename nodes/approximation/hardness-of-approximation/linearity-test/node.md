---
tag: T53VFT
kind: technique
slug: linearity-test
name: Linearity test
aliases:
- BLR test
- Blum-Luby-Rubinfeld test
area: approximation/hardness-of-approximation
level: advanced
summary: A three-query randomized test that accepts every linear function and rejects a function with probability at least its distance to the nearest linear function.
prereqs: [fourier-analysis-of-boolean-functions, hadamard-code, hamming-distance]
see_also: [low-degree-test, dictatorship-test, long-code, hastad-3bit-pcp, pcp-theorem, probabilistically-checkable-proof, locally-decodable-codes]
sources:
  - book: isbn:9781107038325
    title: Ryan O'Donnell, Analysis of Boolean Functions, Cambridge University Press, 2014
    locator: Section 1.6 (Highlight, the Blum-Luby-Rubinfeld linearity test, Theorem 1.30 and its Fourier proof)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 11 (the PCP theorem, the exponential-size PCP from the Walsh-Hadamard code and its linearity test) and Chapter 22, Section 22.5 (the Fourier proof of the linearity test)
  - paper: "Manuel Blum, Michael Luby and Ronitt Rubinfeld, Self-testing/correcting with applications to numerical problems, Journal of Computer and System Sciences 47(3), 549 to 595, 1993 (STOC 1990)"
    locator: the linearity test and self-correction for functions between finite groups
  - paper: "Mihir Bellare, Don Coppersmith, Johan Håstad, Marcos Kiwi and Madhu Sudan, Linearity testing in characteristic two, IEEE Transactions on Information Theory 42(6), 1781 to 1795, 1996"
    locator: the Fourier analysis of the test over GF(2), the bound that the rejection probability is at least the distance to the nearest linear function
---

The linearity test, or BLR test after Blum, Luby and Rubinfeld, reads a function $f$ at two random points $x, y$ and at $x + y$, and accepts when $f(x) + f(y) = f(x + y)$. Every linear function passes with probability $1$, and a function that passes with probability $1 - \varepsilon$ agrees with some linear function on all but an $\varepsilon$ fraction of inputs. Over $\mathbb{F}_2$ the linear functions are the codewords of the [Hadamard code](/hadamard-code/), so the test is a local test for that code, and it was the first step of the [PCP theorem](/pcp-theorem/) and of the Fourier method of [hardness of approximation](/hastad-3bit-pcp/).

## In plain words

Suppose someone gives you a huge table and claims that it lists the values of a very simple kind of function, where the value of a sum is the sum of the values. You cannot read the whole table. So you pick two random entries, add their positions, read the entry at the sum, and check the rule once. If the table is honest the check never fails. The surprise is the other direction: if the check almost never fails, then the table is almost exactly one of the simple functions, with only a few wrong entries. Better still, you can then read the correct value at any position with two lookups at random positions, even at a position whose entry is wrong.

## When it applies

The test applies to a function $f : \mathbb{F}_2^n \to \mathbb{F}_2$ given as an oracle. The function is *linear* when $f(x + y) = f(x) + f(y)$ for all $x, y$, which holds exactly when $f(x) = \sum_{i \in S} x_i$ for some $S \subseteq [n]$. The relative distance of two functions is $\operatorname{dist}(f, g) = \Pr_x[f(x) \ne g(x)]$, and $\operatorname{dist}(f, \mathrm{LIN})$ is the minimum over the $2^n$ linear functions.

For the Fourier proof we use the $\pm 1$ notation of [Fourier analysis of Boolean functions](/fourier-analysis-of-boolean-functions/): $F(x) = (-1)^{f(x)}$ on $\{-1,1\}^n$, addition in $\mathbb{F}_2^n$ becomes the coordinatewise product $x \circ y$, and the linear functions become the characters $\chi_S$. The test then accepts when $F(x) F(y) F(x \circ y) = 1$.

The test is used when a proof or a code word is a large table that a verifier cannot read in full. The verifier makes three queries, uses $2n$ random bits, and either accepts or rejects. Hardness of approximation pages on this site use the convention $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$ for maximization, and a verifier with acceptance gap $1$ versus $s$ gives a gap of that form for the CSP of its checks.

## The template

**The test.** Pick $x, y \in \mathbb{F}_2^n$ uniformly and independently. Query $f(x)$, $f(y)$ and $f(x + y)$. Accept if $f(x) + f(y) = f(x + y)$.

**Completeness.** If $f$ is linear then every check holds, so $f$ is accepted with probability $1$.

**Soundness (Bellare, Coppersmith, Håstad, Kiwi and Sudan).** For every $f$,

$$\Pr[\text{the test rejects } f] \ge \operatorname{dist}(f, \mathrm{LIN}).$$

*Proof, in full.* In the $\pm 1$ notation, $[F(x)F(y)F(x \circ y) = 1] = \tfrac12 + \tfrac12 F(x) F(y) F(x \circ y)$, so

$$\Pr[\text{accept}] = \tfrac12 + \tfrac12\, \mathbb{E}_{x,y}[F(x) F(y) F(x \circ y)].$$

The inner expectation over $y$ is the convolution $(F * F)(x) = \mathbb{E}_y[F(y) F(x \circ y)]$, whose Fourier coefficients are $\hat F(S)^2$. By Plancherel,

$$\mathbb{E}_x[F(x) (F*F)(x)] = \sum_S \hat F(S) \cdot \hat F(S)^2 = \sum_S \hat F(S)^3 .$$

Let $M = \max_S \hat F(S)$. Then $\sum_S \hat F(S)^3 \le M \sum_S \hat F(S)^2 = M$ by Parseval. For each $S$, $\hat F(S) = \mathbb{E}[F \chi_S] = 1 - 2 \operatorname{dist}(f, \chi_S)$, so $M = 1 - 2 \operatorname{dist}(f, \mathrm{LIN})$. Together, $\Pr[\text{accept}] \le \tfrac12 + \tfrac12 (1 - 2\operatorname{dist}(f, \mathrm{LIN})) = 1 - \operatorname{dist}(f, \mathrm{LIN})$. $\square$

**An upper bound on the rejection.** If $g$ is linear and $\operatorname{dist}(f, g) = \delta$, then the test rejects $f$ with probability at most $3\delta$. *Proof.* The test can reject only if one of the three queried points lies in the set where $f \ne g$, since at the other points the answers satisfy the linear rule of $g$. Each of $x$, $y$ and $x + y$ is uniform, so the union bound gives $3\delta$. $\square$ So the rejection probability lies between $\operatorname{dist}(f, \mathrm{LIN})$ and three times that distance.

**Self-correction (Blum, Luby and Rubinfeld).** Let $g$ be linear with $\operatorname{dist}(f, g) = \delta$. For each fixed $x$, pick $y$ uniformly and output $f(x + y) - f(y)$. *Claim:* the output equals $g(x)$ with probability at least $1 - 2\delta$. *Proof.* Both $y$ and $x + y$ are uniform, so $f(y) \ne g(y)$ with probability $\delta$ and $f(x+y) \ne g(x+y)$ with probability $\delta$. If neither happens, the output is $g(x + y) - g(y) = g(x)$. The union bound gives the claim. $\square$ When $\delta < 1/4$ the linear function $g$ is unique, because two distinct linear functions differ on exactly half of the points, and a majority vote over repeated trials recovers $g(x)$ with high probability.

**Amplification.** Repeating the test $t$ times with fresh randomness keeps completeness $1$ and accepts a function at distance $\delta$ from $\mathrm{LIN}$ with probability at most $(1 - \delta)^t$.

## Classic examples

**Majority on three inputs.** $\operatorname{Maj}_3$ has coefficients $\tfrac12$ on the three singletons and $-\tfrac12$ on $\{1,2,3\}$. The test accepts it with probability $\tfrac12 + \tfrac12 (3 \cdot \tfrac18 - \tfrac18) = \tfrac58$, so it rejects with probability $\tfrac38$. Each dictator differs from $\operatorname{Maj}_3$ on $2$ of the $8$ points, so $\operatorname{dist}(\operatorname{Maj}_3, \mathrm{LIN}) = \tfrac14 \le \tfrac38 \le \tfrac34$, as the two bounds say.

**A negated parity.** The function $f(x) = 1 + \sum_{i \in S} x_i$ is affine but not linear. Each check gives $f(x) + f(y) = f(x+y) + 1$, so the test rejects it with probability $1$, and its distance to $\mathrm{LIN}$ is $\tfrac12$ (the nearest linear functions differ from it on half of the points, and $\chi_S$ itself on all of them).

**The exponential-size PCP.** In the PCP for NP of Arora, Lund, Motwani, Sudan and Szegedy, the prover writes the Hadamard encoding of an assignment and of its tensor square. The verifier runs the linearity test on each table, then uses self-correction to read the values it needs, and checks the constraints with a random linear combination. This gives $\mathrm{NP} \subseteq \mathrm{PCP}(\mathrm{poly}(n), O(1))$, the inner verifier of the full [PCP theorem](/pcp-theorem/) (Arora and Barak, Chapter 11).

**The long code test.** Håstad's test reads a [long code](/long-code/) table at $x$, $y$ and $x \circ y \circ z$ with a sparse noise vector $z$. It is the linearity test with noise, and its acceptance probability is $\tfrac12 + \tfrac12 \sum_S \hat F(S)^3 (1 - 2\delta)^{|S|}$. The noise kills the large sets, so only functions close to a few coordinates pass, which is the [dictatorship test](/dictatorship-test/) that drives the [3-bit PCP](/hastad-3bit-pcp/).

## Variations

- **Three functions.** For $f, g, h$ the test $F(x) G(y) H(x \circ y) = 1$ accepts with probability $\tfrac12 + \tfrac12 \sum_S \hat F(S) \hat G(S) \hat H(S)$, by the same convolution argument. This is the form used when the queries go to different tables of a proof.
- **Affine functions.** The four-query test $F(x) F(y) F(z) = F(x \circ y \circ z)$ accepts every $\pm \chi_S$ and accepts with probability $\tfrac12 + \tfrac12 \sum_S \hat F(S)^4$.
- **Other groups.** Blum, Luby and Rubinfeld stated the test for maps between finite groups, with a combinatorial proof based on self-correction. The Fourier proof above is special to $\mathbb{F}_2$, and over other abelian groups it uses the characters of the group.
- **Higher degree.** The [low-degree test](/low-degree-test/) checks that a function on $\mathbb{F}^m$ is close to a polynomial of degree at most $d$, and the linearity test is its case $d = 1$ without a constant term.

## Pitfalls

- **Linear, not affine.** Over $\mathbb{F}_2$ the test rejects negated parities with probability $1$. A proof system that allows affine encodings must use the four-query version or fold the table.
- **Distance to the code, not to the function you want.** The test certifies that $f$ is close to some linear function. It does not say which one, and a reduction must decode it, usually by a large Fourier coefficient or by self-correction.
- **Do not read $f$ directly after the test.** A function at distance $\delta$ can be wrong at any fixed point. Read $g(x)$ through self-correction, not as $f(x)$.
- **The bound is one-sided in strength.** A rejection probability of $\varepsilon$ gives distance at most $\varepsilon$, not $\varepsilon / 3$. The two bounds above differ by a factor of up to $3$.
- **Independence of the queries.** The convolution step needs $x$ and $y$ uniform and independent. A test that reuses a point or uses correlated points needs a new analysis.

## Exercises

1. Show that a function $f : \mathbb{F}_2^n \to \mathbb{F}_2$ with $f(x+y) = f(x) + f(y)$ for all $x, y$ is of the form $\sum_{i \in S} x_i$.
2. Compute the acceptance probability of the test for the function that is $1$ exactly at one nonzero point $a$, and compare it with the bounds.
3. Prove the acceptance formula of the four-query affine test.
4. Show that if the test accepts $f$ with probability $\tfrac12 + \gamma$ with $\gamma > 0$, then $f$ agrees with some linear function on at least a $\tfrac12 + \gamma$ fraction of inputs.
5. Show that for $\delta < 1/4$ at most one linear function is at distance $\delta$ from $f$.

## References
