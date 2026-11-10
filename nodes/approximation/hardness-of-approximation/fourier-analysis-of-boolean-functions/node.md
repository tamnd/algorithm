---
tag: 05ZBBK
kind: technique
slug: fourier-analysis-of-boolean-functions
name: Fourier analysis of Boolean functions
aliases:
- Boolean Fourier analysis
- Walsh-Fourier analysis
- harmonic analysis on the Boolean cube
area: approximation/hardness-of-approximation
level: research
summary: Write a function on the Boolean cube in the basis of parity functions, then read its tests, influences and noise stability off the coefficients.
prereqs: [boolean-function, walsh-hadamard-transform, linearity-of-expectation]
see_also: [linearity-test, dictatorship-test, long-code, hastad-3bit-pcp, max-cut-ugc-hardness, fast-walsh-hadamard-transform, hadamard-code, discrete-fourier-transform]
sources:
  - book: isbn:9781107038325
    title: Ryan O'Donnell, Analysis of Boolean Functions, Cambridge University Press, 2014
    locator: Chapter 1 (Sections 1.2 to 1.5, the Fourier expansion, orthonormality, Plancherel, Parseval and convolution), Chapter 2 (Sections 2.2 to 2.4, influence, total influence, the Poincaré inequality and noise stability, Theorem 2.45 for the noise stability of majority), Chapter 9 (Section 9.6, the KKL theorem and Friedgut's junta theorem)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 22, Section 22.5 (the Fourier transform technique) and Section 22.6 (coordinate functions and the long code)
  - paper: "Jeff Kahn, Gil Kalai and Nathan Linial, The influence of variables on Boolean functions, Proceedings of the 29th IEEE Symposium on Foundations of Computer Science (FOCS), 1988"
    locator: the main theorem, a variable of influence at least a constant times Var[f] log n / n
---

Fourier analysis of Boolean functions writes each function $f : \{-1,1\}^n \to \mathbb{R}$ as a unique linear combination of the $2^n$ parity functions $\chi_S(x) = \prod_{i \in S} x_i$. Each probabilistic test that reads a few values of $f$ at correlated random points then becomes a sum over sets $S$ of products of Fourier coefficients, and this sum is easy to bound. The technique is the main tool in the analysis of the [linearity test](/linearity-test/), [dictatorship tests](/dictatorship-test/) and the [long code](/long-code/), and so of the tight hardness results of [Håstad](/hastad-3bit-pcp/) and of [max cut under the UGC](/max-cut-ugc-hardness/).

## In plain words

Think of a yes or no function of several yes or no inputs as a table of plus ones and minus ones. For each group of inputs there is a parity table: it says plus one when an even number of the inputs in the group are minus one. These tables are at right angles to each other, so every table is a unique weighted mix of them. The weights describe the function. A function that depends on one input puts all its weight on a group of size one. A function where most inputs matter a little spreads its weight over many large groups. A random test that reads the function at a few related points accepts with a probability that is a short formula in these weights, so a high pass rate forces a few large weights, and a large weight names a few important inputs.

## When it applies

The domain is the cube $\{-1,1\}^n$ with the uniform probability measure. We write $+1$ for false and $-1$ for true, so that the product of two values is their exclusive or. A point $x \in \{0,1\}^n$ of the usual notation maps to $((-1)^{x_1}, \ldots, (-1)^{x_n})$. All expectations are over uniform inputs. For two functions $f, g : \{-1,1\}^n \to \mathbb{R}$ the inner product is

$$\langle f, g \rangle = \mathbb{E}_x [f(x) g(x)] = 2^{-n} \sum_{x} f(x) g(x).$$

For $S \subseteq [n]$ the character is $\chi_S(x) = \prod_{i \in S} x_i$, with $\chi_\emptyset = 1$, and the Fourier coefficient is $\hat f(S) = \langle f, \chi_S \rangle$. The method applies when a quantity can be written as the expectation of a product of values of $f$ (or of several functions) at points whose coordinates are independent across $i$. Acceptance probabilities of property tests, the value of a [PCP](/probabilistically-checkable-proof/) verifier on a proof built from tables of Boolean functions, the number of cut edges in a product graph and the correlation of $f$ with a noisy copy of itself are all of this form.

On this site an approximation ratio for a maximization problem means $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$. The hardness results that this technique gives are stated in that form.

## The template

All identities in this section are proved here. The two results at the end are cited.

**Step 1, the expansion.** Every $f : \{-1,1\}^n \to \mathbb{R}$ has the unique expansion

$$f(x) = \sum_{S \subseteq [n]} \hat f(S) \chi_S(x).$$

*Proof.* For $S, T \subseteq [n]$, $\chi_S(x) \chi_T(x) = \chi_{S \triangle T}(x)$, because $x_i^2 = 1$ for each $i$ in $S \cap T$. For $U \ne \emptyset$ the coordinates are independent and $\mathbb{E}[x_i] = 0$, so $\mathbb{E}[\chi_U] = \prod_{i \in U} \mathbb{E}[x_i] = 0$, while $\mathbb{E}[\chi_\emptyset] = 1$. So $\langle \chi_S, \chi_T \rangle = 1$ if $S = T$ and $0$ otherwise. The $2^n$ characters are orthonormal, hence linearly independent, in the space of real functions on the cube, which has dimension $2^n$. So they form a basis, and the coefficient of $\chi_S$ in the expansion of $f$ is $\langle f, \chi_S \rangle = \hat f(S)$. $\square$

**Step 2, Plancherel and Parseval.** For all $f, g$, $\langle f, g \rangle = \sum_S \hat f(S) \hat g(S)$. If $f$ takes values in $\{-1,1\}$, then $\sum_S \hat f(S)^2 = 1$.

*Proof.* Expand both functions and use bilinearity: $\langle f, g \rangle = \sum_{S,T} \hat f(S) \hat g(T) \langle \chi_S, \chi_T \rangle = \sum_S \hat f(S) \hat g(S)$. With $g = f$ this gives $\sum_S \hat f(S)^2 = \mathbb{E}[f^2]$, which is $1$ when $f^2 = 1$ at every point. $\square$

It follows that $\mathbb{E}[f] = \hat f(\emptyset)$ and $\operatorname{Var}[f] = \mathbb{E}[f^2] - \mathbb{E}[f]^2 = \sum_{S \ne \emptyset} \hat f(S)^2$. For Boolean $f$ every coefficient lies in $[-1, 1]$, and $\hat f(S) = 1 - 2 \Pr[f(x) \ne \chi_S(x)]$, so a coefficient near $1$ means that $f$ is close to the parity $\chi_S$.

**Step 3, convolution.** Write $x \circ y$ for the coordinatewise product. Define $(f * g)(x) = \mathbb{E}_y[f(y) g(x \circ y)]$. Then $\widehat{f * g}(S) = \hat f(S) \hat g(S)$ for every $S$.

*Proof.* $\widehat{f*g}(S) = \mathbb{E}_x \mathbb{E}_y [f(y) g(x \circ y) \chi_S(x)]$. Put $z = x \circ y$. For each fixed $y$ the map $x \mapsto z$ is a bijection of the cube, so $y$ and $z$ are independent and uniform. Also $x = y \circ z$, because $y_i^2 = 1$, and $\chi_S(y \circ z) = \chi_S(y) \chi_S(z)$. So the expectation is $\mathbb{E}_y[f(y) \chi_S(y)] \cdot \mathbb{E}_z[g(z) \chi_S(z)] = \hat f(S) \hat g(S)$. $\square$

**Step 4, influence.** For $f : \{-1,1\}^n \to \{-1,1\}$ the influence of coordinate $i$ is $\operatorname{Inf}_i[f] = \Pr_x[f(x) \ne f(x^{\oplus i})]$, where $x^{\oplus i}$ is $x$ with coordinate $i$ negated. Then

$$\operatorname{Inf}_i[f] = \sum_{S \ni i} \hat f(S)^2, \qquad \mathbf{I}[f] = \sum_{i=1}^n \operatorname{Inf}_i[f] = \sum_S |S| \hat f(S)^2 .$$

*Proof.* Let $x^{i \to b}$ be $x$ with coordinate $i$ set to $b$, and define the derivative $D_i f(x) = \tfrac12 (f(x^{i \to 1}) - f(x^{i \to -1}))$. Apply this to each character: $D_i \chi_S = \chi_{S \setminus \{i\}}$ if $i \in S$ and $0$ if $i \notin S$. By linearity $D_i f = \sum_{S \ni i} \hat f(S) \chi_{S \setminus \{i\}}$, and the sets $S \setminus \{i\}$ for $S \ni i$ are distinct. So Plancherel gives $\mathbb{E}[(D_i f)^2] = \sum_{S \ni i} \hat f(S)^2$. For Boolean $f$, $D_i f(x) \in \{-1, 0, 1\}$, and it is nonzero exactly when $f(x^{i \to 1}) \ne f(x^{i \to -1})$, that is when $f(x) \ne f(x^{\oplus i})$. So $\mathbb{E}[(D_i f)^2] = \operatorname{Inf}_i[f]$. Sum over $i$: each $S$ is counted $|S|$ times. $\square$

Since $|S| \ge 1$ for every $S \ne \emptyset$, Step 2 and Step 4 give the Poincaré inequality $\operatorname{Var}[f] \le \mathbf{I}[f]$.

**Step 5, noise stability.** For $\rho \in [-1, 1]$ and a fixed $x$, a $\rho$-correlated copy $y$ of $x$ has independent coordinates with $y_i = x_i$ with probability $(1+\rho)/2$ and $y_i = -x_i$ otherwise. So $y$ is uniform and $\mathbb{E}[y_i \mid x] = \rho x_i$. The noise stability is $\operatorname{Stab}_\rho[f] = \mathbb{E}[f(x) f(y)]$, and

$$\operatorname{Stab}_\rho[f] = \sum_S \rho^{|S|} \hat f(S)^2 .$$

*Proof.* By bilinearity it suffices to show $\mathbb{E}[\chi_S(x) \chi_T(y)] = \rho^{|S|}$ if $S = T$ and $0$ otherwise. Given $x$ the coordinates of $y$ are independent, so $\mathbb{E}[\chi_T(y) \mid x] = \prod_{i \in T} \rho x_i = \rho^{|T|} \chi_T(x)$. Then $\mathbb{E}[\chi_S(x) \chi_T(y)] = \rho^{|T|} \langle \chi_S, \chi_T \rangle$, which is the claim by Step 1. $\square$

For Boolean $f$, $f(x) f(y) = 1 - 2 \cdot [f(x) \ne f(y)]$, so $\Pr[f(x) \ne f(y)] = \tfrac12 - \tfrac12 \operatorname{Stab}_\rho[f]$.

**Step 6, decode.** A test is analyzed in the same way each time. Write the acceptance probability as an expectation of a product of values of $f$. Expand each value by Step 1. Use independence across coordinates, as in Steps 3 and 5, to collapse the sum to a sum over a single set $S$. Then a large acceptance probability forces $\sum_S (\text{weight}) \hat f(S)^k$ to be large, and Parseval turns this into one large coefficient $\hat f(S)$ with $|S|$ small. The small set $S$ names a few coordinates, which become a label in a reduction from [label cover](/label-cover/).

**Two deeper results (cited).** The Kahn, Kalai and Linial theorem says that every $f : \{-1,1\}^n \to \{-1,1\}$ has a coordinate with $\operatorname{Inf}_i[f] \ge c \operatorname{Var}[f] \log n / n$ for an absolute constant $c > 0$. Friedgut's junta theorem says that if $\mathbf{I}[f] \le K$ then $f$ agrees with a function of at most $2^{O(K/\varepsilon)}$ coordinates on all but an $\varepsilon$ fraction of inputs. Both are proved in O'Donnell, Section 9.6, with hypercontractivity.

## Classic examples

**Majority on three inputs.** $\operatorname{Maj}_3(x) = \tfrac12 x_1 + \tfrac12 x_2 + \tfrac12 x_3 - \tfrac12 x_1 x_2 x_3$. The weights by level are $0, \tfrac34, 0, \tfrac14$, and they sum to $1$ as Parseval says. Each $\operatorname{Inf}_i = \tfrac14 + \tfrac14 = \tfrac12$: coordinate $1$ decides the vote exactly when $x_2 \ne x_3$. The total influence is $\tfrac32 \ge \operatorname{Var} = 1$. At $\rho = \tfrac12$ the stability is $\tfrac34 \cdot \tfrac12 + \tfrac14 \cdot \tfrac18 = \tfrac{13}{32}$, and at $\rho = -\tfrac12$ it is $-\tfrac{13}{32}$.

**Majority on more inputs.** For $\operatorname{Maj}_5$ the weights by level are $0, \tfrac{45}{64}, 0, \tfrac{5}{32}, 0, \tfrac{9}{64}$, each influence is $\binom{4}{2}/2^4 = \tfrac38$, and $\operatorname{Stab}_{1/2}[\operatorname{Maj}_5] = \tfrac{769}{2048} \approx 0.37549$. For odd $n$ every influence of majority is $\binom{n-1}{(n-1)/2} / 2^{n-1}$, which is asymptotic to $\sqrt{2/(\pi n)}$ (at $n = 101$ it is $0.07959$ against $0.07939$). The values of $\operatorname{Stab}_{1/2}[\operatorname{Maj}_n]$ for $n = 3, 5, 11, 51, 101$ are $0.40625, 0.37549, 0.35096, 0.33697, 0.33516$. They tend to $1 - \tfrac{2}{\pi} \arccos \tfrac12 = \tfrac13$, which is Sheppard's formula $\lim_n \operatorname{Stab}_\rho[\operatorname{Maj}_n] = 1 - \tfrac{2}{\pi}\arccos \rho$ (O'Donnell, Theorem 2.45).

**Dictators and parities.** A dictator $\chi_{\{i\}}$ has all its weight on one set of size $1$, influence $1$ at coordinate $i$ and $0$ elsewhere, and stability $\rho$. The full parity $\chi_{[n]}$ has every influence equal to $1$ and stability $\rho^n$, so it is the least stable Boolean function for $0 < \rho < 1$. Majority sits in between: no coordinate has a large influence, but the stability stays bounded away from $0$. The [Majority Is Stablest theorem](/max-cut-ugc-hardness/) says that this is the best possible for functions with small influences.

**The linearity test.** The [BLR test](/linearity-test/) accepts $f$ when $f(x) f(y) f(x \circ y) = 1$. By Step 3 the acceptance probability is $\tfrac12 + \tfrac12 \sum_S \hat f(S)^3$. For $\operatorname{Maj}_3$ this is $\tfrac12 + \tfrac12 (3 \cdot \tfrac18 - \tfrac18) = \tfrac58$.

**The noise test for max cut.** Accept when $f(x) \ne f(y)$ for a $\rho$-correlated pair with $\rho < 0$. By Step 5 this happens with probability $\tfrac12 - \tfrac12 \sum_S \rho^{|S|} \hat f(S)^2$. A dictator passes with probability $\tfrac{1 - \rho}{2}$, which is $\tfrac34$ at $\rho = -\tfrac12$, while $\operatorname{Maj}_3$ passes with $\tfrac{45}{64} \approx 0.703$. This test is the core of the [UG-hardness of max cut](/max-cut-ugc-hardness/).

## Variations

- **Other product spaces.** For functions on $\Omega^n$ with a product measure, the Efron-Stein decomposition plays the role of the expansion, and influences and noise stability are defined in the same way (O'Donnell, Chapter 8). This is the setting of [unique games](/unique-games-conjecture/) reductions over larger alphabets.
- **Biased measures.** On the $p$-biased cube the characters are replaced by products of normalized coordinates $(x_i - \mu)/\sigma$, and the same identities hold.
- **Gaussian space.** The Hermite polynomials replace the characters, and the invariance principle compares low-influence functions on the cube with functions of Gaussians (O'Donnell, Chapter 11).
- **Computation.** The vector of all $2^n$ coefficients is the [Walsh-Hadamard transform](/walsh-hadamard-transform/) of the truth table divided by $2^n$, and the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/) computes it with $n 2^n$ additions and subtractions.

## Pitfalls

- **Sign and range conventions.** Parseval in the form $\sum_S \hat f(S)^2 = 1$ needs values in $\{-1,1\}$. For a $0/1$-valued function the sum is $\mathbb{E}[f]$, and the weights of the two conventions differ by the map $f \mapsto 1 - 2f$.
- **Normalization.** The inner product uses the expectation, not the sum. With the sum, Parseval picks up a factor $2^n$ and Step 3 is off by the same factor.
- **The direction of the domain map.** Writing true as $+1$ instead of $-1$ on the inputs replaces $f(x)$ by $f(-x)$, which multiplies $\hat f(S)$ by $(-1)^{|S|}$ but keeps the weights $\hat f(S)^2$. Mixing the two conventions in one proof gives wrong signs in formulas with cubes, such as the BLR formula.
- **Negative correlation.** For $\rho < 0$ the terms $\rho^{|S|} \hat f(S)^2$ have alternating signs, so bounds that are monotone in $\rho$ for $\rho > 0$ fail. The max cut analysis handles this by moving to the odd part of $f$.
- **Influence of real-valued functions.** For $f$ with real values, $\operatorname{Inf}_i[f]$ is defined as $\mathbb{E}[(D_i f)^2]$, which is not a probability. The KKL theorem as stated above needs $f$ to be Boolean.

## Exercises

1. Compute all Fourier coefficients of the function on $\{-1,1\}^2$ that is $-1$ exactly when both inputs are $-1$, and check Parseval.
2. Show that $\sum_S \hat f(S) = f(1, \ldots, 1)$ and that $\hat f(S) = 2^{-n} \sum_x f(x) \chi_S(x)$ is the Walsh-Hadamard transform of the truth table, scaled by $2^{-n}$.
3. Prove that a Boolean function with $\sum_{|S| = 1} \hat f(S)^2 = 1$ is a dictator or a negated dictator.
4. Prove that $\mathbf{I}[\operatorname{Maj}_n]$ is asymptotic to $\sqrt{2n/\pi}$ for odd $n$. Then show that a monotone Boolean function has $\operatorname{Inf}_i[f] = \hat f(\{i\})$, and use $\sum_i \hat f(\{i\}) = \mathbb{E}[f(x)(x_1 + \cdots + x_n)]$ to show that majority has the largest total influence among monotone functions.
5. Let $T_\rho f(x) = \mathbb{E}[f(y)]$ for a $\rho$-correlated $y$. Show that $T_\rho \chi_S = \rho^{|S|} \chi_S$ and that $\operatorname{Stab}_\rho[f] = \langle f, T_\rho f \rangle$.

## References
