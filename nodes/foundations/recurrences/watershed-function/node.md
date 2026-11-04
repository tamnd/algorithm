---
tag: 5HPFXZ
kind: definition
slug: watershed-function
name: Watershed function
area: foundations/recurrences
level: intro
summary: The function n raised to log base b of a, compared against the driving function to decide which case of the master theorem applies.
prereqs: [divide-and-conquer-recurrence, logarithms]
see_also: [master-theorem, recursion-tree-method, akra-bazzi-theorem, continuous-master-theorem, strassen-algorithm, karatsuba-multiplication]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 4.5, The master method for solving recurrences (the watershed function and the driving function)
  - paper: doi:10.1145/1008861.1008865
    title: Jon L. Bentley, Dorothea Haken and James B. Saxe, A general method for solving divide-and-conquer recurrences, SIGACT News 12(3), 36 to 44 (1980)
  - url: "https://courses.csail.mit.edu/6.046/spring04/handouts/akrabazzi.pdf"
    locator: Tom Leighton, Notes on Better Master Theorems for Divide-and-Conquer Recurrences, MIT, October 9, 1996 (the exponent p with the sum of a_i b_i^p equal to 1)
---

The watershed function of a [divide-and-conquer recurrence](/divide-and-conquer-recurrence/) $T(n) = aT(n/b) + f(n)$ is the function $n^{\log_b a}$. It is the order of growth of the solution when the driving function $f$ is zero beyond the base case, and it equals, up to a constant factor, the number of leaves of the recursion tree. The [master theorem](/master-theorem/) decides its case by comparing $f(n)$ with the watershed function; the name is from CLRS, fourth edition.

## Definition

Let $a > 0$ and $b > 1$ be constants. The *watershed function* of the recurrence $T(n) = aT(n/b) + f(n)$ is

$$n^{\log_b a},$$

and $\log_b a$ is the *watershed exponent*. It depends on $a$ and $b$ only, not on $f$.

Two facts make it the natural point of comparison.

1. **It counts the leaves.** In the recursion tree, level $j$ has $a^j$ nodes of size $n/b^j$. The nodes reach constant size at depth $\log_b n$, where there are $a^{\log_b n}$ of them, and $a^{\log_b n} = n^{\log_b a}$. Proof: take $\log_b$ of both sides; each side gives $\log_b a \cdot \log_b n$.
2. **It solves the recurrence with no driving function.** If $f = 0$ beyond the base case, $T(n) = a^{\lfloor \log_b n\rfloor + 1} T(n/b^{\lfloor \log_b n \rfloor + 1}) = \Theta(n^{\log_b a})$; see Lemma 2 of the [master theorem](/master-theorem/). Equivalently, $g(n) = n^{\log_b a}$ satisfies $g(n) = a\, g(n/b)$ exactly, since $a (n/b)^{\log_b a} = a\, n^{\log_b a}/a$.

With $w = \log_b a$, the cost of level $j$ of the recursion tree is $a^j f(n/b^j)$. If $f(n) = n^w$ exactly, each level costs $a^j (n/b^j)^w = n^w$, because $b^w = a$. So the watershed function is the driving function for which all the levels of the tree cost the same. A driving function that is larger by a polynomial factor makes the costs shrink from the root down; one that is smaller makes them grow towards the leaves.

## Examples and non-examples

All examples use $\lg = \log_2$.

| Recurrence | $a$, $b$ | Watershed function | Driving function | Comparison |
|---|---|---|---|---|
| [Binary search](/binary-search/): $T(n/2) + 1$ | 1, 2 | $n^0 = 1$ | $1$ | equal: $\Theta(\log n)$ |
| [Merge sort](/merge-sort/): $2T(n/2) + n$ | 2, 2 | $n$ | $n$ | equal: $\Theta(n\log n)$ |
| [Karatsuba](/karatsuba-multiplication/): $3T(n/2) + n$ | 3, 2 | $n^{\lg 3} \approx n^{1.585}$ | $n$ | smaller: $\Theta(n^{\lg 3})$ |
| [Strassen](/strassen-algorithm/): $7T(n/2) + n^2$ | 7, 2 | $n^{\lg 7} \approx n^{2.807}$ | $n^2$ | smaller: $\Theta(n^{\lg 7})$ |
| $3T(n/4) + n\lg n$ | 3, 4 | $n^{\log_4 3} \approx n^{0.792}$ | $n\lg n$ | larger: $\Theta(n\log n)$ |
| [Stooge sort](/stooge-sort/): $3T(2n/3) + 1$ | 3, 3/2 | $n^{\log_{3/2} 3} \approx n^{2.710}$ | $1$ | smaller: $\Theta(n^{2.710})$ |
| $\frac12 T(n/2) + 1/n$ | 1/2, 2 | $n^{-1}$ | $1/n$ | equal: $\Theta((\log n)/n)$ |

- **The design lever.** Karatsuba and Strassen lower $a$ by one, from 4 to 3 and from 8 to 7. This lowers the watershed exponent from 2 to $\lg 3$ and from 3 to $\lg 7$. Since the driving function is smaller than the watershed function in both cases, the watershed function is the running time, so the saving in $a$ is the whole gain.
- **A watershed exponent below zero.** For $a < 1$ the exponent is negative. The last row shows that the definition and the comparison still work.
- **Non-example: the size of the input.** The watershed function is not $n$ in general. It equals $n$ exactly when $a = b$.
- **Non-example: unequal parts.** For $T(n) = T(n/3) + T(2n/3) + n$ the recurrence is not of the form $aT(n/b)$, and $n^{\log_b a}$ is not defined. The role of the watershed exponent is played by the number $p$ with $(1/3)^p + (2/3)^p = 1$, so $p = 1$; see the [Akra-Bazzi theorem](/akra-bazzi-theorem/).
- **Non-example: a comparison by constant factors.** $f(n) = 100\,n^{\log_b a}$ and $f(n) = n^{\log_b a}/100$ are both $\Theta(n^{\log_b a})$, the middle case. The cases of the master theorem compare orders of growth, and the boundaries between them are polynomial factors $n^\varepsilon$, with an extra rule for powers of $\log n$.

## Related definitions

- The *driving function* $f(n)$, called the toll function by Roura, is the cost of a call outside its recursive calls. The watershed function is compared with it.
- For $T(n) = \sum_i a_i T(b_i n) + g(n)$ the analogue of the watershed function is $n^p$, where $p$ is the unique real number with $\sum_i a_i b_i^p = 1$, as in the [Akra-Bazzi theorem](/akra-bazzi-theorem/). For a single term, $a b^{-p} = 1$ gives $p = \log_b a$.
- For full-history recurrences the analogue is $n^\alpha$ with $\varphi(\alpha) = 1$, in the [continuous master theorem](/continuous-master-theorem/).
- In the [recursion-tree method](/recursion-tree-method/), the watershed function is the cost of the leaf level.

## References
