---
tag: W71HC5
kind: concept
slug: sensitivity
name: Sensitivity
aliases:
- s(f)
area: complexity/communication-and-query-complexity
level: advanced
summary: "s(f) is the largest number, over inputs x, of single bits whose flip changes f(x). It is the smallest of the usual query measures, and by Huang's theorem it is at least the square root of deg(f)."
prereqs: [query-model, boolean-function]
see_also: [block-sensitivity, sensitivity-theorem, certificate-complexity, query-complexity, decision-tree-complexity, fourier-analysis-of-boolean-functions, hamming-weight, boolean-function]
sources:
  - paper: doi:10.1016/S0304-3975(01)00144-X
    title: Harry Buhrman and Ronald de Wolf, Complexity measures and decision tree complexity, a survey, Theoretical Computer Science 288(1) (2002)
    locator: pp. 21 to 43; Section 4.2 (sensitivity and block sensitivity, Simon's lower bound, Rubinstein's example), Section 6.1 (symmetric functions, Turán's bound)
  - paper: doi:10.1137/0220062
    title: Noam Nisan, CREW PRAMs and decision trees, SIAM Journal on Computing 20(6) (1991)
    locator: pp. 999 to 1007 (sensitivity, block sensitivity and CREW PRAM time)
  - paper: doi:10.1007/BF01263419
    title: Noam Nisan and Mario Szegedy, On the degree of Boolean functions as real polynomials, Computational Complexity 4(4) (1994)
    locator: pp. 301 to 313 (the question whether s and bs are polynomially related; the function with deg 2 and s 3)
  - paper: doi:10.1007/BF01200762
    title: David Rubinstein, Sensitivity vs. block sensitivity of Boolean functions, Combinatorica 15(2) (1995)
    locator: pp. 297 to 299 (a function with bs(f) = s(f)^2 / 2)
  - paper: doi:10.4007/annals.2019.190.3.6
    title: Hao Huang, Induced subgraphs of hypercubes and a proof of the sensitivity conjecture, Annals of Mathematics 190(3) (2019)
    locator: pp. 949 to 955; Theorem 1.4 in arXiv:1907.00847 version 2 (s(f) at least the square root of deg(f))
---

The sensitivity of a Boolean function counts how many single bits of one input can change the value. For an input $x$, $\mathrm{s}(f, x)$ is the number of positions $i$ such that flipping $x_i$ changes $f(x)$, and $\mathrm{s}(f)$ is the largest such count over all inputs. It is the simplest of the measures of [query complexity](/query-complexity/) and the smallest: $\mathrm{s}(f) \le \mathrm{bs}(f) \le C(f) \le D^{dt}(f)$. This page defines the measure and gives its values and bounds. The [block sensitivity](/block-sensitivity/) page treats the version with blocks of bits, and the [sensitivity theorem](/sensitivity-theorem/) page proves that the two are polynomially related.

## In plain words

Take a yes or no rule about a row of bits, and one particular row. Flip one bit and see whether the answer changes. Do this for each bit in turn and count the flips that change the answer. That count is the sensitivity of the rule at that row. The sensitivity of the rule is the largest count over all rows. A rule like "is the number of ones odd" changes with every flip, so its count is the length of the row. A rule like "is the first bit 1" has count one. A rule with low counts everywhere is smooth: its answer is stable under small changes. For about thirty years it was not known whether such smooth rules are always easy to compute. In 2019 Huang proved that they are.

## The idea

**Definitions.** Let $f : \{0,1\}^n \to \{0,1\}$, and write $x^i$ for $x$ with bit $i$ flipped.

$$\mathrm{s}(f, x) = |\{ i : f(x^i) \ne f(x) \}|, \qquad \mathrm{s}_b(f) = \max_{x : f(x) = b} \mathrm{s}(f, x), \qquad \mathrm{s}(f) = \max(\mathrm{s}_0(f), \mathrm{s}_1(f)).$$

Older papers call $\mathrm{s}(f)$ the **critical complexity**. In the language of graphs: color each vertex $x$ of the $n$-dimensional cube with $f(x)$. Then $\mathrm{s}(f, x)$ is the number of neighbors of $x$ with the other color, and $\mathrm{s}(f)$ is the largest such number. To compute it from the truth table takes $n 2^n$ steps.

**Where it sits.** For total $f$, $\mathrm{s}(f) \le \mathrm{bs}(f) \le C(f) \le D^{dt}(f)$; see [query complexity](/query-complexity/). The other direction is the hard one. Nisan proved $C(f) \le \mathrm{s}(f) \, \mathrm{bs}(f)$, and Nisan and Szegedy asked in 1992 whether $\mathrm{bs}(f)$ is bounded by a polynomial in $\mathrm{s}(f)$. All the other measures ($D^{dt}$, $R$, $Q$, $C$, $\mathrm{bs}$, $\deg$, $\widetilde{\deg}$) were known to be polynomially related. Huang settled the question in 2019: $\mathrm{s}(f) \ge \sqrt{\deg(f)}$, so $\mathrm{bs}(f) \le 2 \mathrm{s}(f)^4$ and, with a bound of Tal, $\mathrm{bs}(f) \le \mathrm{s}(f)^4$. See the [sensitivity theorem](/sensitivity-theorem/).

**Sensitivity is not bounded by degree.** One might expect $\mathrm{s}(f) \le \deg(f)$, but it is false. The function on three bits that is 1 when $|x| \in \{1, 2\}$ has the polynomial $x_1 + x_2 + x_3 - x_1 x_2 - x_1 x_3 - x_2 x_3$, of degree 2, and at $x = 000$ every flip changes the value, so $\mathrm{s}(f) = 3$. The true relation goes the other way: $\deg(f) \le \mathrm{s}(f)^2$ by Huang, and in general $\mathrm{s}(f) \le \mathrm{bs}(f) \le 2 \deg(f)^2$ by Nisan and Szegedy.

**Lower bounds on sensitivity.** Three bounds hold for any total $f$.

- **Simon (1983).** If $f$ depends on all $n$ bits, then $\mathrm{s}(f) \ge \frac{1}{2} \log_2 n - \frac{1}{2} \log_2 \log_2 n + \frac{1}{2}$. The address function shows that $\Theta(\log n)$ can occur.
- **Turán (1984).** If $f$ is symmetric (its value depends only on the number of ones $|x|$) and not constant, then $\mathrm{s}(f) \ge \lceil (n + 1)/2 \rceil$. Proof: there is a $k$ with $f$ different at weights $k$ and $k + 1$. An input of weight $k$ is sensitive to its $n - k$ zeros, and an input of weight $k + 1$ is sensitive to its $k + 1$ ones. One of $n - k$ and $k + 1$ is at least $(n + 1)/2$.
- **Huang (2019).** $\mathrm{s}(f) \ge \sqrt{\deg(f)}$.

**Average sensitivity.** The mean $\mathbb{E}_x[\mathrm{s}(f, x)]$ over a uniform input is the **average sensitivity**, or total influence. It is a different measure: it equals the sum of $|S| \hat f(S)^2$ over the [Fourier coefficients](/fourier-analysis-of-boolean-functions/) of $f$ in the $\pm 1$ form, and it can be far below $\mathrm{s}(f)$. For OR on $n$ bits, the all-zero input has sensitivity $n$ and the $n$ inputs of weight 1 have sensitivity 1, and all other inputs have sensitivity 0, so the average is $2n / 2^n$ while $\mathrm{s}(\mathrm{OR}) = n$.

## Examples

These values were computed by brute force over all inputs.

| function | $n$ | $\mathrm{s}_0$ | $\mathrm{s}_1$ | $\mathrm{s}$ | $\mathrm{bs}$ | $D^{dt}$ |
|---|---|---|---|---|---|---|
| OR | 5 | 5 | 1 | 5 | 5 | 5 |
| PARITY | 5 | 5 | 5 | 5 | 5 | 5 |
| MAJORITY (more than half) | 6 | 3 | 4 | 4 | 4 | 6 |
| MAJORITY | 7 | 4 | 4 | 4 | 4 | 7 |
| OR of 3 ANDs of 3 bits | 9 | 3 | 3 | 3 | 3 | 9 |
| address function, $k = 2$ | 6 | 3 | 3 | 3 | 3 | 3 |
| $|x| \in \{1, 2\}$ | 3 | 3 | 1 | 3 | 3 | 3 |

Some points in the table:

- **OR.** At the all-zero input every flip turns the value to 1, so $\mathrm{s}_0 = n$. At a 1-input, only a lone 1 can be flipped to change the value, so $\mathrm{s}_1 = 1$.
- **MAJORITY.** For odd $n$, an input with $(n+1)/2$ ones is sensitive to each of its ones, and no input is sensitive to more, so $\mathrm{s} = (n + 1)/2$. This meets Turán's bound. For even $n$ with the rule "more than half", the counts are $\mathrm{s}_0 = n/2$ and $\mathrm{s}_1 = n/2 + 1$.
- **OR of ANDs.** With $k$ blocks of $k$ bits, $\mathrm{s} = k = \sqrt n$ and $\deg = n$, so Huang's bound $\mathrm{s} \ge \sqrt{\deg}$ is tight for this function.

**Rubinstein's function.** It shows that $\mathrm{bs}$ can be the square of $\mathrm{s}$, up to a factor $1/2$. Let $n = k^2$ with $k$ even, split into $k$ blocks of $k$ bits. A block is good if it has exactly two ones and they sit at positions $2j - 1$ and $2j$ for some $j$. Let $f(x) = 1$ when at least one block is good.

- At $x = 0$, each of the $k^2/2$ pairs $\{2j - 1, 2j\}$ in each block is a sensitive block, and they are disjoint. So $\mathrm{bs}(f) \ge k^2 / 2$.
- At a 0-input, a flip changes the value only if it makes its own block good. A block with one 1 becomes good only by a flip of the partner of that 1. A block with three ones becomes good only if two of them form a pair and the third is flipped. A block with any other content cannot become good by one flip. So each block has at most one sensitive position, and $\mathrm{s}_0(f) \le k$.
- At a 1-input with two or more good blocks, no single flip changes the value. At a 1-input with exactly one good block, each of the $k$ positions of that block is sensitive, and no other position is. So $\mathrm{s}_1(f) = k$, and $\mathrm{s}(f) = k$.

For $k = 4$, a brute-force pass over all $2^{16}$ inputs gives $\mathrm{s}_0 = \mathrm{s}_1 = 4$, while $\mathrm{bs} \ge 8$. Later constructions by Virza and by Ambainis and Sun improve the constant but keep the gap quadratic. No function is known with $\mathrm{bs}(f)$ larger than a constant times $\mathrm{s}(f)^2$, while the best upper bound is $\mathrm{s}(f)^4$.

## Where it is used

- **Parallel computation.** Lower bounds on the time of CREW PRAMs use sensitivity and block sensitivity (Nisan 1991).
- **The sensitivity theorem.** Its statement is that $\mathrm{s}$ is polynomially related to the other measures; see the [sensitivity theorem](/sensitivity-theorem/).
- **Hypercube combinatorics.** By the reduction of Gotsman and Linial, bounds on $\mathrm{s}(f)$ in terms of $\deg(f)$ are the same as bounds on the largest degree of induced subgraphs of the cube; see the sensitivity theorem page.
- **Lower bounds on decision trees.** Since $\mathrm{s}(f) \le D^{dt}(f)$, an input with many sensitive bits gives a quick lower bound. For example, PARITY has $\mathrm{s} = n$, so $D^{dt}(\mathrm{PARITY}) = n$; see the [parity problem](/parity-problem/).

## References
