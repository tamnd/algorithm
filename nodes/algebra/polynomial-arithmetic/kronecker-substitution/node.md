---
tag: VWSQV7
kind: technique
slug: kronecker-substitution
name: Kronecker substitution
aliases:
- Kronecker's trick
- Kronecker-Schonhage trick
- polynomial packing
area: algebra/polynomial-arithmetic
level: advanced
summary: Encodes a polynomial as an integer by substituting x = 2^k, so one integer product yields the polynomial product.
prereqs: [polynomial, dense-polynomial-representation, integer-multiplication]
see_also: [fft-polynomial-multiplication, evaluation-interpolation-paradigm, schonhage-strassen-multiplication, harvey-van-der-hoeven-multiplication, karatsuba-multiplication, bit-packing, kronecker-factorization-method, sparse-polynomial-multiplication]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 8.4, Multiplication in Z[x] and R[x, y] (Kronecker substitution for integer and bivariate polynomials)
  - paper: doi:10.1016/j.jsc.2009.05.004
    title: David Harvey, Faster polynomial multiplication via multipoint Kronecker substitution, Journal of Symbolic Computation 44(10), 1502-1510, 2009
    locator: the description of standard Kronecker substitution and of the new variants with evaluation at 2^k, -2^k and 2^(-k)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.3, Multiplication (integer multiplication algorithms that the substitution calls)
---

Kronecker substitution multiplies polynomials with integer coefficients by multiplying two integers. It evaluates both polynomials at $x = 2^k$, with $k$ so large that the coefficients of the product cannot overlap, multiplies the two integers, and reads the coefficients of the product from the digits of the result in base $2^k$. One call to a fast integer multiplication, such as the one in GMP, then does all the work. The same substitution $y = x^d$ turns a polynomial in two variables into a polynomial in one.

Notation: polynomials are lists of coefficients with the constant term first, $f, g \in \mathbb{Z}[x]$ have $n$ and $m$ coefficients, and $h = fg$. Costs are counted in bit operations, because the method replaces ring operations on coefficients by one integer product; $M_{\mathbb{Z}}(N)$ is the cost of multiplying two integers of $N$ bits.

## In plain words

Write the number 30201. Its digits, read in groups of two from the right, are 01, 02 and 03. So it holds the polynomial with the coefficients 1, 2 and 3: the polynomial is evaluated at 100. Multiply it by 504, which holds 4 and 5 in the same way. The answer is 15221304, and its groups of two digits are 04, 13, 22 and 15. These are the coefficients of the product of the two polynomials. This works because no coefficient of the product is 100 or more, so no carry goes from one group to the next. A computer does the same with groups of binary digits that are wide enough, and uses its fastest method to multiply large numbers.

## When it applies

The technique fits a problem when these conditions hold.

1. **The result is a polynomial expression in the inputs that integer arithmetic can compute.** For a product, evaluation at $x = 2^k$ is a ring homomorphism $\mathbb{Z}[x] \to \mathbb{Z}$, so $h(2^k) = f(2^k)\, g(2^k)$. Sums, products and powers work the same way.
2. **There is a bound on the coefficients of the result.** For a product, $|h_i| \le \min(n, m) \cdot \max_i |f_i| \cdot \max_j |g_j|$. If the coefficients are known to be nonnegative, a bound $h_i < 2^k$ is enough; if they can be negative, the method needs $|h_i| < 2^{k-1}$.
3. **The coefficients are small compared with the degree, or a fast integer multiplication is at hand.** The integer product has about $(n + m) k$ bits. When the coefficients are words or bounded residues, this is a constant times the input size, and a library product of that size is faster than most direct polynomial methods.
4. **The coefficient ring maps to $\mathbb{Z}$ in a way that respects products up to a known bound.** For $\mathbb{Z}/p\mathbb{Z}$, lift the residues to $0, \ldots, p - 1$, multiply over $\mathbb{Z}$ with the bound $\min(n, m)(p - 1)^2$, and reduce the coefficients of the result modulo $p$.

## The template

```pseudo id=template
KRONECKER-MUL(f, g)                         ▷ f, g ∈ Z[x], n and m coefficients
K1  B ← min(n, m) · max|f_i| · max|g_j|     ▷ |h_i| ≤ B for h = fg
K2  k ← the least integer with 2^(k−1) > B
K3  F ← Σ f_i 2^(ki);  G ← Σ g_j 2^(kj)       ▷ evaluate at 2^k
K4  H ← F · G                                 ▷ one integer product
K5  for i ← 0 to n + m − 2 do                 ▷ balanced digits in base 2^k
K6      h_i ← H mod 2^k, taken in [−2^(k−1), 2^(k−1))
K7      H ← (H − h_i) / 2^k
K8  return (h_0, ..., h_{n+m−2})
```

**Why it is correct.** Evaluation at $2^k$ is a ring homomorphism, so $H = h(2^k) = \sum_i h_i 2^{ki}$. Every integer has exactly one expansion $\sum_i d_i 2^{ki}$ with all digits $d_i$ in $[-2^{k-1}, 2^{k-1})$, and lines K5 to K7 compute it: $d_0$ is fixed by $H \bmod 2^k$, and $(H - d_0)/2^k$ is the rest of the expansion. By line K2 the coefficients $h_i$ lie in this range, so they are the digits. If all coefficients are nonnegative, $2^k > B$ is enough and the digits are taken in $[0, 2^k)$; then lines K3 and K5 to K7 are only copies of bit fields, with no arithmetic.

**Cost.** With coefficients of at most $b$ bits, line K2 gives $k \le 2b + \lceil \log_2 \min(n, m) \rceil + 2$. Lines K3 and K5 to K7 cost $O((n + m) k)$ bit operations, and line K4 costs $M_{\mathbb{Z}}((n + m) k)$. With the integer multiplication of Harvey and van der Hoeven, $M_{\mathbb{Z}}(N) = O(N \log N)$, so the product of two polynomials of degree less than $n$ costs $O(n (b + \log n) \log(n (b + \log n)))$ bit operations. These bounds are proved. That the method is the fastest choice for a given size is observed in practice and depends on the integer library, the machine and the coefficient size.

**Choices to make.** The bound $B$, which should be tight but must be proved; signed or unsigned digits; and whether to use one evaluation point or several (see Variations).

## Classic examples

All the numbers below were checked with a script.

**Nonnegative coefficients.** For $f = 1 + 2x + 3x^2$ and $g = 4 + 5x$, the bound is $B = 2 \cdot 3 \cdot 5 = 30$, so $2^5 = 32 > 30$ is enough for unsigned digits. Then $f(32) = 3137$, $g(32) = 164$ and $3137 \cdot 164 = 514468 = 15 \cdot 32^3 + 22 \cdot 32^2 + 13 \cdot 32 + 4$. So $fg = 4 + 13x + 22x^2 + 15x^3$. In base 100 this is the product $30201 \cdot 504 = 15221304$ from the plain words.

**Signed coefficients.** For $f = 1 - x$ and $g = 1 + x$, $B = 1$, and $k = 3$ gives digits in $[-4, 4)$. Then $f(8) = -7$, $g(8) = 9$ and $H = -63$. Balanced digits: $-63 \bmod 8 = 1$, then $(-63 - 1)/8 = -8$, whose digit is $0$, then $-1$, whose digit is $-1$. So $fg = 1 + 0x - x^2$.

**Coefficients in $\mathbb{Z}/p\mathbb{Z}$.** Over $\mathbb{Z}/7\mathbb{Z}$, take $f = 3 + 5x$ and $g = 6 + 4x$. With residues in $0, \ldots, 6$, the bound is $2 \cdot 6^2 = 72 < 2^7$. Then $f(128) = 643$, $g(128) = 518$ and $643 \cdot 518 = 333074 = 20 \cdot 128^2 + 42 \cdot 128 + 18$. The integer product is $18 + 42x + 20x^2$, and modulo 7 this is $4 + 6x^2$. Libraries for $\mathbb{Z}/p\mathbb{Z}[x]$ with word-size $p$, such as FLINT, use this method for a range of medium degrees.

**Bivariate to univariate.** For $f, g \in R[x, y]$ with $\deg_x (fg) < d$, the substitution $y = x^d$ is injective on polynomials of $x$-degree less than $d$. For $(x + y)(x - y)$, $\deg_x$ of the product is $2$, so take $d = 3$: $(x + x^3)(x - x^3) = x^2 - x^6 = x^2 - (x^3)^2$, which gives back $x^2 - y^2$. Von zur Gathen and Gerhard, Section 8.4, use both substitutions together: $R[x, y]$ to $R[x]$ and $\mathbb{Z}[x]$ to $\mathbb{Z}$.

**Multivariate factorization.** Kronecker used the substitution $x_i = x^{d^{i-1}}$ to reduce questions about polynomials in several variables to one variable. A factor of $f(x_1, \ldots, x_r)$ maps to a factor of the univariate image, so one can find the factors of the image and test which of their products come from factors of $f$. This is exponential in the worst case, and modern algorithms use Hensel lifting instead.

## Variations

- **Several evaluation points.** Harvey evaluates at $2^k$ and $-2^k$. The sum and difference of the two products give the even and odd parts of $h$, each at the point $2^{2k}$, so the two integer products have half the size. For $f = 1 + 2x + 3x^2$ and $g = 4 + 5x$ with $k = 6$, the two halves are $90116 = 4 + 22 \cdot 2^{12}$ and $3932992 = 2^6 (13 + 15 \cdot 2^{12})$. A second variant uses the reversed polynomials, which is evaluation at $2^{-k}$, and recovers each coefficient from the low part of one integer product and the high part of the other, so that the evaluation point needs only about half as many bits.
- **The reverse direction.** Fast integer multiplication splits an integer into blocks, which is a polynomial evaluated at $2^k$, multiplies the polynomials, and evaluates the product back. Schonhage-Strassen multiplication works this way. So the two problems reduce to each other, up to a constant factor and the logarithmic growth of the coefficients.
- **Extension fields.** For $\mathbb{F}_q = \mathbb{F}_p[t]/(\mu)$, write each coefficient as a polynomial in $t$ of degree less than $\deg \mu$, substitute $t = x^{d}$ with $d$ larger than the $x$-degree bound, multiply in $\mathbb{F}_p[x]$, which again can use integer packing, and reduce the coefficients of the result modulo $\mu$.
- **Squaring.** The square $f^2$ needs one integer square, which integer libraries compute faster than a general product.
- **Packing several small products.** When the coefficients are a few bits wide, as over $\mathbb{F}_2$ or $\mathbb{F}_3$, several coefficients fit in one machine word, and word operations then act on all of them at once. This is [bit packing](/bit-packing/), the same idea at word level.

## Pitfalls

- **A bound that is too small.** If some $|h_i| \ge 2^{k-1}$, a carry crosses into the next coefficient and the result is wrong with no warning. Use $\min(n, m)$ times the product of the two maxima, not only the product of the maxima.
- **Unsigned extraction with signed coefficients.** With negative coefficients, the plain base-$2^k$ digits are wrong, because each negative coefficient borrows from the next one. Use balanced digits as in line K6, or shift all coefficients to be nonnegative first.
- **The bound for $\mathbb{Z}/p\mathbb{Z}$.** The bound is $\min(n, m)(p - 1)^2$, not $(p - 1)^2$. Balanced residues in $(-p/2, p/2)$ reduce it to about $\min(n, m) p^2 / 4$ and save one or two bits per coefficient, at the cost of signed extraction.
- **The zero polynomial and constants.** An empty list has no maximum coefficient; handle it before line K1. With one constant input, the method still works but gives no gain over scaling.
- **Very unbalanced operands.** If $n \gg m$, the integer product is very unbalanced too. Split $f$ into blocks of $m$ coefficients, or rely on the integer library to handle unbalanced operands well.
- **Large coefficients.** When $b$ is much larger than $\log n$, the method is still correct, but a multimodular approach with the [number-theoretic transform](/number-theoretic-transform/) and the [Chinese remainder theorem](/chinese-remainder-theorem/) can be faster, because it multiplies polynomials with word-size coefficients.

## Exercises

1. Multiply $(2 + x)(3 + x)$ by evaluating at $10$. *Answer:* $12 \cdot 13 = 156$, so the product is $6 + 5x + x^2$.
2. Polynomials of degree less than $1000$ over $\mathbb{Z}/p\mathbb{Z}$ with $p < 2^{64}$ are to be multiplied with unsigned digits. Which $k$ is enough? *Answer:* $1000 (p - 1)^2 < 2^{10} \cdot 2^{128} = 2^{138}$, so $k = 138$.
3. Show that with nonnegative coefficients and $2^k > \max_i h_i$, line K3 is a concatenation of bit fields and lines K5 to K7 are a split into bit fields, with no additions.
4. Show that $y \mapsto x^d$ maps the monomials $x^i y^j$ with $i < d$ to distinct powers of $x$, and so is injective on $R[x, y]$ restricted to $x$-degree less than $d$.
5. With Harvey's two points $2^k$ and $-2^k$, show that $(h(2^k) + h(-2^k))/2 = h_{\mathrm{even}}(2^{2k})$, where $h_{\mathrm{even}}(z) = \sum_i h_{2i} z^i$. Why must $k$ now also satisfy a bound for the signed digits of the odd part?

## References
