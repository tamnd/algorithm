---
tag: EJZEEB
kind: concept
slug: arbitrary-precision-arithmetic
name: Arbitrary-precision arithmetic
aliases:
- bignum arithmetic
- multiple-precision arithmetic
area: algebra/integer-arithmetic
level: intro
summary: Computing exactly with integers limited only by available memory, not by machine word size.
prereqs: [positional-number-system, word-ram, asymptotic-notation]
see_also: [big-integer, multiprecision-integer, integer-addition, integer-multiplication, integer-division, karatsuba-multiplication, radix-conversion, integer-overflow]
sources:
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Chapter 1, Integer arithmetic (Section 1.1 for the representation in base β with n words, Sections 1.2 to 1.4 for addition, multiplication and division, Section 1.3.2 for the range of the Karatsuba threshold)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3, Multiple-precision arithmetic (4.3.1 the classical algorithms, 4.3.3 how fast can we multiply)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 2, Fundamental algorithms (the representation of integers and the cost of the classical operations), and Chapter 8, Fast multiplication
---

Arbitrary-precision arithmetic computes exactly with integers whose size is limited only by the memory of the machine, not by the size of a machine word. A number is stored as an array of machine words called *limbs*, which are the digits of the number in the base $\beta = 2^w$, and each operation is a loop or a recursion over the limbs. The cost of an operation is a function of the number of limbs $n$: addition takes $\Theta(n)$ limb operations, and the cost $M(n)$ of a [multiplication](/integer-multiplication/) sets the cost of almost everything else. Libraries such as GMP, the integers of Python and the `BigInteger` class of Java are built this way.

## In plain words

A computer word holds a number of a fixed size, for example up to about 18 followed by 18 zeros. Some programs need larger numbers: a key for encryption has hundreds of digits, and an exact factorial or a fraction in a computer algebra system can have thousands.

The answer is the method that children learn at school. You write the number as a list of digits and you add, multiply and divide digit by digit, with carries and borrows. The only change is the size of a digit. A computer uses one full word as one digit, so each digit has billions of possible values, and the processor handles one digit in one step.

The work grows with the length of the numbers. Adding two long numbers takes time in proportion to their length. Multiplying them is the expensive step, and much research has gone into making it fast.

## The idea

**The notation of this area.** All pages of this area use the same notation. A nonnegative integer $A$ is stored in the base $\beta = 2^w$, where $w$ is the word size, as $n$ limbs $a_0, a_1, \ldots, a_{n-1}$ with

$$A = \sum_{i=0}^{n-1} a_i \beta^i, \qquad 0 \le a_i < \beta .$$

The limb $a_0$ is the least significant one. The representation is *normalized* when $a_{n-1} \ne 0$, so that $n$ is the length of $A$; zero has $n = 0$. Then $\beta^{n-1} \le A < \beta^n$, and $n = \lfloor \log_\beta A \rfloor + 1$ for $A \ge 1$. We write $M(n)$ for the cost of multiplying two $n$-limb numbers, and $D(n)$ for the cost of dividing a $2n$-limb number by an $n$-limb number.

**The cost models.** Each algorithm page states its model. In the [word RAM](/word-ram/) with words of $w$ bits, one *limb operation* costs one unit: an addition of two limbs with a carry, a product of two limbs into a two-limb result, a division of a two-limb number by a limb, a comparison, a shift, a read or a write. In the *bit complexity* model, the cost is the number of bit operations, as in a [Boolean circuit](/boolean-circuit/) or a [multitape Turing machine](/multitape-turing-machine/), and the size of the input is its number of bits, $nw$. A bound in limb operations becomes a bound in bit operations when we multiply by the cost of one limb operation, which is $O(w^2)$ at most for a word product done by schoolbook. The fast multiplication results of [Schönhage-Strassen](/schonhage-strassen-multiplication/), [Fürer](/furer-multiplication/) and [Harvey and van der Hoeven](/harvey-van-der-hoeven-multiplication/) are bounds in the bit model.

**Signs.** A [big integer](/big-integer/) usually keeps a sign and a magnitude ([sign-magnitude representation](/sign-magnitude-representation/)): the sign is a separate field, and the limb array holds $|A|$. Some libraries use a [two's complement](/twos-complement/) form of infinite length instead. The algorithms on the limb arrays work on magnitudes, and a short case analysis of the signs is done around them.

**The cost of the basic operations.** The table gives the known costs on two operands of $n$ limbs. The first three rows are in limb operations on the word RAM and are proved. The bounds for $M(n)$ from Schönhage-Strassen on are in bit operations for $N = nw$ bits.

| operation | method | cost |
|---|---|---|
| addition, subtraction, comparison | [carry loop](/integer-addition/) | $\Theta(n)$ |
| multiplication | [schoolbook](/schoolbook-multiplication/) | $\Theta(n^2)$ |
| multiplication | [Karatsuba](/karatsuba-multiplication/) (1962) | $O(n^{\log_2 3})$, about $O(n^{1.585})$ |
| multiplication | [Toom-Cook](/toom-cook-multiplication/) 3-way (Toom 1963, Cook 1966) | $O(n^{\log_3 5})$, about $O(n^{1.465})$ |
| multiplication | [Schönhage-Strassen](/schonhage-strassen-multiplication/) (1971) | $O(N \log N \log\log N)$ bit operations |
| multiplication | [Fürer](/furer-multiplication/) (2007) | $N \log N \cdot 2^{O(\log^* N)}$ bit operations |
| multiplication | [Harvey and van der Hoeven](/harvey-van-der-hoeven-multiplication/) (2019, published 2021) | $O(N \log N)$ bit operations |
| division with remainder | [long division](/long-division/) | $\Theta(n^2)$ for a $2n$ by $n$ division |
| division with remainder | [Newton's method](/newton-raphson-division/) | $O(M(n))$ |
| square root | [Newton's method](/newton-integer-root/) | $O(M(n))$ |
| conversion to decimal | [divide and conquer](/radix-conversion/) | $O(M(n) \log n)$ |
| greatest common divisor | [half-gcd](/half-gcd/) | $O(M(n) \log n)$ |

**What is proved and what is observed.** The bounds in the table are theorems. Which method is fastest for a given size is not a theorem: it depends on the processor, the word size, the cache and the quality of the code. Brent and Zimmermann (Section 1.3.2) report that the best size at which to switch from schoolbook to Karatsuba multiplication is between about 10 and 100 words, depending on the processor. Libraries such as GMP measure such crossover points on each machine and store them in tuning tables. The algorithms of Fürer and of Harvey and van der Hoeven are not used in practice: their constant factors are so large that Schönhage-Strassen or a floating-point or modular FFT is faster at each size that a computer can store.

**Why the multiplication sets the cost.** Division, square roots, radix conversion and the greatest common divisor all reduce to multiplication. With [Newton's method](/newton-iteration/), a reciprocal to $n$ limbs costs a constant times $M(n)$, because each step doubles the precision and the costs of the steps form a geometric series. This needs the mild condition that $M(n)/n$ does not decrease, which holds for each method in the table.

**Exactness.** The results are exact. There is no rounding and no overflow, as long as memory lasts. This is the difference from [floating-point arithmetic](/floating-point-arithmetic/), which keeps a fixed number of significant bits and rounds, and from machine integers, which wrap around ([integer overflow](/integer-overflow/)).

## Examples

**Representation.** The number $30! = 265252859812191058636308480000000$ has 108 bits. In the base $\beta = 2^8$ it has $n = 14$ limbs. From the least significant limb up, they are

$$0, 0, 0, 84, 221, 245, 93, 134, 150, 15, 55, 246, 19, 13 .$$

The three low limbs are zero because $2^{26}$ divides $30!$, and $26 \ge 24$. In CPython, an `int` uses limbs of 30 bits (`sys.int_info.bits_per_digit` is 30 on common 64-bit builds), so the same number takes 4 limbs.

**A carry into a new limb.** In the base $\beta = 2^8$, the number $A = 2^{24} - 1$ is the array $[255, 255, 255]$, with all limbs equal to $\beta - 1$. Adding $B = 1$ makes a carry at each position: the sum is $[0, 0, 0, 1]$, which is $2^{24}$. The sum has one more limb than the larger operand. This is the largest growth possible, because $A + B < 2\beta^n \le \beta^{n+1}$.

**The size of a product.** A product of an $m$-limb number and an $n$-limb number has $m + n$ or $m + n - 1$ limbs, because $\beta^{m-1}\beta^{n-1} \le AB < \beta^m \beta^n$. For example, in base $2^8$, $255 \cdot 255 = 65025 = [1, 254]$ has two limbs, and $1 \cdot 1 = 1$ has one.

**The schoolbook cost.** Multiplying two numbers of $n$ limbs by the school method takes $n^2$ limb products. For $n = 1000$ this is $10^6$ limb products, while Karatsuba's recursion on $1000 = 2^{10}$ rounded up to $1024$ limbs, cut down to single limbs, takes $3^{10} = 59049$ limb products and $O(n^{\log_2 3})$ additions. The count of products alone does not decide which is faster: Karatsuba also does more additions and more memory traffic, which is why the crossover point is a measured value.

## Where it is used

- **Public-key cryptography.** RSA works with moduli of 2048 bits or more, which is 32 limbs of 64 bits. Its core is [modular exponentiation](/modular-exponentiation/), with [Montgomery multiplication](/montgomery-multiplication/) or [Barrett reduction](/barrett-reduction/) for the products.
- **Computer algebra.** Exact linear algebra and polynomial arithmetic over the integers and the rationals produce large coefficients ([expression swell](/expression-swell/)). The [Bareiss algorithm](/bareiss-algorithm/) keeps them as small as possible, but they still need many words.
- **Number theory.** Primality tests such as the [Lucas-Lehmer test](/lucas-lehmer-test/) on Mersenne numbers multiply numbers of millions of bits.
- **Exact computation of constants and functions.** Records for the digits of $\pi$ use FFT-based multiplication on numbers of many billions of digits.
- **Language runtimes.** Python, Ruby, Haskell, Lisp and Scheme give integers of unbounded size by default. Java has `BigInteger`, and C and C++ programs use GMP.
- **Exact geometric predicates.** Some predicates of computational geometry evaluate the sign of a determinant exactly to avoid wrong answers from rounding.

## References
