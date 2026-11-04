---
tag: AGN1TE
kind: model
slug: real-ram
name: Real RAM
aliases:
- real random access machine
area: foundations/models-of-computation
level: advanced
summary: RAM whose registers hold exact real numbers with unit-cost arithmetic and comparisons.
prereqs: [random-access-machine, unit-cost-model, word-ram]
see_also: [algebraic-computation-tree, algebraic-decision-tree, blum-shub-smale-machine, comparison-model, orientation-test, graham-scan, closest-pair-of-points, floating-point-arithmetic]
sources:
  - book: isbn:9780387961316
    title: "Franco P. Preparata and Michael Ian Shamos, Computational Geometry: An Introduction, Springer (1985)"
    locator: Section 1.4, Models of Computation, pp. 26 to 35; Section 6.4, Gaps and Covers, pp. 255 to 262
  - paper: "arXiv:1912.02278"
    title: "Jeff Erickson, Ivor van der Hoog and Tillmann Miltzow, Smoothing the gap between NP and ER, full version of the paper in FOCS 2020 (doi:10.1109/FOCS46700.2020.00099), pp. 1022 to 1033"
    locator: Section 1 (the real RAM and the floor function), Section 2 (Theorem 2) and Section 6.1, What is the Real RAM?
  - paper: "Michael Ian Shamos, Computational Geometry, PhD thesis, Yale University (1978)"
    locator: the model of computation of the thesis
  - paper: doi:10.1145/800061.808735
    title: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983), 80 to 86"
    locator: the main theorem and its application to element distinctness
  - paper: doi:10.1007/3-540-09510-1_42
    title: "Arnold Schönhage, On the power of random access machines, Automata, Languages and Programming (ICALP 1979), Lecture Notes in Computer Science 71, 520 to 529"
    locator: pp. 520 to 529 (PSPACE in polynomial time with +, -, x and integer division)
  - paper: doi:10.1109/SWAT.1974.20
    title: "Juris Hartmanis and Janos Simon, On the power of multiplication in random access machines, 15th Annual Symposium on Switching and Automata Theory (1974), 13 to 23"
    locator: the main theorem (polynomial time equals polynomial space)
  - paper: doi:10.1016/0020-0190(72)90045-2
    title: "Ronald L. Graham, An efficient algorithm for determining the convex hull of a finite planar set, Information Processing Letters 1(4) (1972), 132 to 133"
    locator: the O(n log n) algorithm
  - paper: doi:10.1109/SFCS.1975.8
    title: "Michael Ian Shamos and Dan Hoey, Closest-point problems, 16th Annual Symposium on Foundations of Computer Science (FOCS 1975), 151 to 162"
    locator: the O(n log n) closest pair algorithm
  - paper: doi:10.1007/BF01840442
    title: "D. T. Lee and Y. F. Wu, Geometric complexity of some location problems, Algorithmica 1 (1986), 193 to 211"
    locator: the lower bound for the maximum gap problem
  - paper: doi:10.1137/0215021
    title: "David G. Kirkpatrick and Raimund Seidel, The ultimate planar convex hull algorithm?, SIAM Journal on Computing 15(1) (1986), 287 to 299"
    locator: the O(n log h) algorithm and the matching lower bound
  - paper: doi:10.1007/BF02712873
    title: "Timothy M. Chan, Optimal output-sensitive convex hull algorithms in two and three dimensions, Discrete and Computational Geometry 16 (1996), 361 to 368"
    locator: the O(n log h) algorithm in the plane
  - paper: doi:10.1007/PL00009321
    title: "Jonathan Richard Shewchuk, Adaptive precision floating-point arithmetic and fast robust geometric predicates, Discrete and Computational Geometry 18 (1997), 305 to 363"
    locator: the adaptive orientation and incircle predicates
  - paper: doi:10.1145/77635.77639
    title: "Herbert Edelsbrunner and Ernst Peter Mücke, Simulation of simplicity: a technique to cope with degenerate cases in geometric algorithms, ACM Transactions on Graphics 9(1) (1990), 66 to 104"
    locator: the symbolic perturbation scheme
  - paper: doi:10.1090/S0273-0979-1989-15750-9
    title: "Lenore Blum, Mike Shub and Steve Smale, On a theory of computation and complexity over the real numbers, Bulletin of the American Mathematical Society 21(1) (1989), 1 to 46"
    locator: the introduction (the machine over the reals)
---

The real RAM is a [random access machine](/random-access-machine/) whose registers hold exact real numbers, and where each arithmetic operation and each comparison on them costs one step. It is the model in which most algorithms of computational geometry are stated and analysed, from the thesis of Shamos (1978) and the book of Preparata and Shamos (1985) on. It has no rounding and no limit on the size of a number, so it is an idealisation. With algebraic operations only, its lower bounds are those of the [algebraic computation tree](/algebraic-computation-tree/), and it becomes much stronger if a floor function is added at unit cost.

## The machine

Definitions in the literature differ in details. This page uses the definition of Erickson, van der Hoog and Miltzow (2020, Section 6.1), which makes precise the model that Preparata and Shamos describe in their Section 1.4.

**Memory.** The memory has two arrays of registers. Each *real register* holds a real number exactly. Each *integer register* holds an integer, as on the [word RAM](/word-ram/). Addresses are integers, so the machine reads and writes a real register through an index in an integer register.

**Input.** The input is $n$ real numbers in the first $n$ real registers, and the integer $n$ in an integer register. A point in the plane is two registers, and a set of $n$ points is $2n$ registers. The size of the input is the number of reals, not the number of bits.

**Instructions.** Each of these costs one step.

- Real arithmetic: $x \leftarrow y \circ z$ with $\circ \in \{+, -, \times, \div\}$ (division only by a non-zero value), on real registers or real constants such as $0$, $1$ and $\tfrac12$.
- Integer arithmetic on integer registers: addition, subtraction, multiplication, integer division and the usual bit operations of the word RAM.
- A comparison of two real registers with $<$, $\le$ or $=$, or of two integer registers, followed by a jump.
- Copy, read and write through an integer index, and conversion of an integer to a real.

**What the machine cannot do.** No instruction converts a real register into an integer. There is no floor function $\lfloor x \rfloor$, no test whether a real is an integer, and no access to the bits of a real. So every integer value is determined by $n$ and by the outcomes of the comparisons made so far. This rule is what keeps the model reasonable.

**Extra functions.** Some authors add the square root, which a Euclidean distance needs. Others add the exponential, the logarithm or the trigonometric functions. A result should say which it uses. The lower bounds and the unrolling to algebraic computation trees below hold when the extra functions are algebraic, such as the square root. They do not hold for the sine, since $\sin(\pi x) = 0$ exactly when $x$ is an integer, and this is the integer test that the definition forbids. The model with a unit-cost floor function is called here the *real RAM with floor*. It is a different and much stronger model (see below).

## What it counts

The **time** of a run is the number of instructions. The **space** is the number of registers in use. No cost depends on the value or on the number of bits of a register. Bounds are usually for the worst case over all inputs of $n$ reals.

So an algorithm that squares a number $k$ times pays $k$ steps. Starting from $2$, the value after $k$ squarings is $2^{2^k}$, which has $2^k + 1$ bits: for $k = 5$ the number has 33 bits after 5 steps. This is the weak point of the unit cost. On the real RAM without floor it does no harm to the lower bounds, because they come from the algebraic tree model, where a large value does not help. It matters when the model gets operations that read the digits of a number.

**Exact arithmetic is an assumption, and floating point breaks it.** A real RAM algorithm assumes that each predicate, such as the sign of a determinant, is evaluated exactly. Run with floating point, it can give inconsistent answers on inputs that are close to degenerate: wrong hulls, invalid triangulations or crashes. For example, take the [orientation test](/orientation-test/) $\det = (q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$ with $q = (12, 12)$, $r = (24, 24)$ and $p = (0.5 + 41 u, 0.5 + 48 u)$ for $u = 2^{-53}$. These coordinates are exact IEEE 754 double values. The exact determinant is about $+9.3 \times 10^{-15}$, so $p$ is to the left of the line $qr$. Evaluated in double precision in the order of the formula, the result is about $-5.7 \times 10^{-14}$, the wrong sign. There are three standard remedies:

- exact or adaptive-precision predicates, which compute the sign exactly and are fast when the answer is clear (Shewchuk 1997);
- exact integer arithmetic on integer input, with enough bits for each intermediate value (see the bound below);
- symbolic perturbation for degenerate input, such as the simulation of simplicity of Edelsbrunner and Mücke (1990).

**From the real RAM to the word RAM.** The orientation test of three points $p, q, r$ with integer coordinates in $[0, 2^\ell)$ needs a known number of bits. The value $|\det|$ is twice the area of the triangle $pqr$. The triangle lies in a square of side $2^\ell - 1$, so its area is at most $(2^\ell - 1)^2 / 2$ and $|\det| \le (2^\ell - 1)^2 < 2^{2\ell}$. Each difference lies strictly between $-2^\ell$ and $2^\ell$, so each of the two products has absolute value less than $2^{2\ell}$. The difference of two such products has absolute value less than $2^{2\ell + 1}$, but it equals $\det$, which is less than $2^{2\ell}$ in absolute value. So a two's complement word of $w \ge 2\ell + 1$ bits holds every intermediate value exactly, and the test is exact on a word RAM in $O(1)$ steps. For $\ell = 2$ the largest value of $|\det|$ is $9 = (2^2 - 1)^2$, for $p = (0,0)$, $q = (3,0)$, $r = (0,3)$. A predicate that is a polynomial of degree $d$ in the coordinates needs about $d \ell$ bits in the same way.

## Relation to other models

- **Algebraic computation tree.** Without floor, a run of at most $t$ steps on $n$ inputs unrolls to an [algebraic computation tree](/algebraic-computation-tree/) of height at most $t$, with one node for each real instruction and one branch node for each real comparison. The integer registers add no branching that depends on the reals: their values are determined by $n$ and the path, so each indexed access refers to a register that the path fixes. So each lower bound of the tree model is a lower bound for the real RAM. With a floor function this unrolling fails, because floor is not an algebraic operation, and an integer computed by floor depends on the real input. An address computed in this way selects one of $n$ registers in one step. A tree with at most three exits at each node needs depth $\Omega(\log n)$ and at least $n$ leaves to make that choice, and it still cannot compute the floor itself.
- **Blum-Shub-Smale machine.** The [Blum-Shub-Smale machine](/blum-shub-smale-machine/) is a formal machine over the reals with unit-cost arithmetic and comparisons, with a complexity theory of classes $\mathrm{P}_{\mathbb{R}}$ and $\mathrm{NP}_{\mathbb{R}}$. It has no integer registers and no indirect addressing. Erickson, van der Hoog and Miltzow (2020, Section 2) describe their definition of the real RAM as a generalization of both the word RAM and the BSS model.
- **Word RAM.** The [word RAM](/word-ram/) holds integers of $w$ bits and has bit operations. The real RAM adds exact reals with no bit access. The word RAM can run radix sort and hashing, which read the bits of the keys. The real RAM cannot do this with real keys, since it has no access to the bits of a real. A real RAM algorithm runs on a word RAM for integer input only if each intermediate value fits in a word, as in the bound above.
- **Comparison model.** The [comparison model](/comparison-model/) is the part of the real RAM where the algorithm only compares the inputs. The real RAM adds arithmetic on them.

## Known results in the model

**Upper bounds.** These worst-case bounds are for $n$ points in the plane. [Graham scan](/graham-scan/) finds the convex hull in $O(n \log n)$ time (Graham 1972). The closest pair is found in $O(n \log n)$ time (Shamos and Hoey 1975), see [closest pair of points](/closest-pair-of-points/). Output-sensitive algorithms find the hull in $O(n \log h)$ time, where $h$ is the number of hull vertices (Kirkpatrick and Seidel 1986; Chan 1996, see [Chan's algorithm](/chan-algorithm/)).

**Lower bounds.** Because a run without floor unrolls to an algebraic computation tree, the theorem of Ben-Or (1983) gives $\Omega(n \log n)$ steps for [element distinctness](/element-distinctness/) in the worst case. A closest pair algorithm decides element distinctness (the minimum distance is $0$ exactly when two points are equal), and a hull algorithm that lists the vertices in order sorts $n$ numbers (put $x_i$ at the point $(x_i, x_i^2)$). So both problems need $\Omega(n \log n)$ steps, and the Graham scan and the Shamos and Hoey algorithm are optimal. Kirkpatrick and Seidel (1986) also proved an $\Omega(n \log h)$ lower bound in the [algebraic decision tree](/algebraic-decision-tree/) model, so their algorithm and Chan's are optimal too. All these bounds are for the worst case and for the model without floor.

**Discrete problems and $\exists\mathbb{R}$.** Erickson, van der Hoog and Miltzow (2020, Theorem 2) proved a real RAM form of the [Cook-Levin theorem](/cook-levin-theorem/). A discrete decision problem is in the class $\exists\mathbb{R}$ (the problems that reduce in polynomial time to the existential theory of the reals) if and only if it has a polynomial-time *real verification algorithm*: a real RAM program that gets the instance and a witness made of reals and integers, and accepts exactly when the witness shows a yes-instance. So $\exists\mathbb{R}$ is to the real RAM what [NP](/np/) is to the word RAM.

**The floor function pitfall.** Suppose the real RAM is given a unit-cost floor function. The bounds above fail, and the model becomes too strong to be a model of real computing. There are two kinds of evidence.

1. *Bucketing beats the tree bounds.* The **maximum gap** problem asks, for $n \ge 2$ reals, for the largest difference between two neighbours in sorted order. In the algebraic computation tree model it needs $\Omega(n \log n)$ steps (Lee and Wu 1986). With floor it takes $O(n)$ steps, by an algorithm of Gonzalez (1975) that Preparata and Shamos present in Section 6.4. Let $a$ and $b$ be the minimum and the maximum, and assume $a < b$ (otherwise the answer is $0$). Let $\delta = (b - a)/(n-1)$ and put $x$ into bucket $k(x) = \min(\lfloor (x - a)/\delta \rfloor, n-1)$, for $k$ in $0, \ldots, n-1$. For each bucket keep its smallest and its largest element. The $n - 1$ gaps in the sorted order add up to $b - a$, so the largest gap is at least $\delta$. Two numbers in one bucket differ by less than $\delta$ (the last bucket holds only $b$), so no largest gap lies inside a bucket. Hence the answer is the largest difference between the maximum of a non-empty bucket and the minimum of the next non-empty bucket. This takes $O(n)$ steps. For example, for the numbers $3, 17, 5, 20, 6, 11$ we have $\delta = 17/5$, the buckets are $0, 4, 0, 5, 0, 2$, and the answer is $17 - 11 = 6$.
2. *Floor gives unit-cost integer arithmetic on huge numbers.* With floor, the machine computes $\lfloor x / y \rfloor$ for integers $x$ and $y$ in two steps, and repeated squaring makes integers with exponentially many bits in a linear number of steps. So the real RAM with floor simulates a unit-cost integer RAM with $+$, $-$, $\times$ and integer division on unbounded integers. Schönhage (1979) showed that such a RAM solves every problem in [PSPACE](/pspace/) in polynomial time; he solved the PSPACE-complete problem of quantified Boolean formulas in a polynomial number of these operations. An earlier result of Hartmanis and Simon (1974) is of the same kind: with unit-cost multiplication and bitwise Boolean operations on unbounded integers, polynomial time equals polynomial space.

For this reason the literature on computational geometry either excludes the floor function or states that a result uses it. The model with floor resembles the word RAM, but it has no bound on the size of a number.

## References
