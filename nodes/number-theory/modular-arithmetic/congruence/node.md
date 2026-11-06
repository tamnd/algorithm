---
tag: N9EC3Z
kind: definition
slug: congruence
name: Congruence relation
aliases:
- congruence modulo n
- a ≡ b (mod n)
area: number-theory/modular-arithmetic
level: intro
summary: Integers a and b are congruent mod n when n divides a minus b.
prereqs: [divisibility, division-with-remainder, equivalence-relation]
see_also: [additive-group-modulo-n, multiplicative-group-modulo-n, modular-inverse, linear-congruence, chinese-remainder-theorem, modular-exponentiation, fermat-little-theorem, residue-number-system]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.1, Elementary number-theoretic notions (the division theorem, remainders and equivalence classes modulo n), and Section 31.3, Modular arithmetic
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 3.4, 'MOD', the binary operation, and Section 4.6, 'MOD', the congruence relation (the rules for addition, multiplication and division of congruences)
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Chapter 2, Congruences (Section 2.1 on equivalence relations, Section 2.2 on the basic properties, Section 2.5 on residue classes)
  - book: "Carl Friedrich Gauss, Disquisitiones Arithmeticae, 1801; English translation by Arthur A. Clarke, Yale University Press, 1966"
    locator: Section 1, Articles 1 and 2 (the definition of congruent numbers and the sign ≡)
---

Two integers $a$ and $b$ are congruent modulo a positive integer $n$, written $a \equiv b \pmod n$, when $n$ [divides](/divisibility/) their difference $a - b$. Equivalently, $a$ and $b$ leave the same remainder on [division with remainder](/division-with-remainder/) by $n$. Congruence modulo $n$ is an [equivalence relation](/equivalence-relation/) that is compatible with addition and multiplication, so a computation with integers can be done on remainders only. This is the base of modular arithmetic and of every page in this area, from [modular exponentiation](/modular-exponentiation/) to the [Chinese remainder theorem](/chinese-remainder-theorem/).

## Definition

Let $n \ge 1$ be an integer, the **modulus**. For integers $a$ and $b$,

$$a \equiv b \pmod n \quad \Longleftrightarrow \quad n \mid (a - b) \quad \Longleftrightarrow \quad \exists k \in \mathbb{Z} : a = b + kn.$$

We write $a \not\equiv b \pmod n$ when this is false. Some authors also allow $n = 0$, where the relation is equality, and negative $n$, where it is the same as for $|n|$. This page takes $n \ge 1$.

**The remainder.** By the division theorem, each integer $a$ has a unique pair $(q, r)$ with $a = qn + r$ and $0 \le r < n$. We write $a \bmod n = r = a - n \lfloor a/n \rfloor$. Then

$$a \equiv b \pmod n \quad \Longleftrightarrow \quad a \bmod n = b \bmod n.$$

*Proof.* Write $a = q_1 n + r_1$ and $b = q_2 n + r_2$ with $0 \le r_1, r_2 < n$. Then $a - b = (q_1 - q_2) n + (r_1 - r_2)$, so $n \mid a - b$ if and only if $n \mid r_1 - r_2$. Since $-n < r_1 - r_2 < n$, the only multiple of $n$ in this range is $0$, so this holds if and only if $r_1 = r_2$. $\square$

So the binary operation $\bmod$ gives a canonical representative of each class. The symbol $\bmod$ in $a \bmod n$ is an operation that returns a number; the symbol $\pmod n$ in a congruence is a part of a relation. Mixing the two is a common source of errors.

**An equivalence relation.** For each $n \ge 1$ and all integers $a, b, c$:

- reflexive: $a \equiv a$, because $n \mid 0$;
- symmetric: if $n \mid a - b$, then $n \mid -(a - b) = b - a$;
- transitive: if $n \mid a - b$ and $n \mid b - c$, then $n$ divides the sum $(a - b) + (b - c) = a - c$.

**Residue classes.** The class of $a$ is $[a]_n = \{a + kn : k \in \mathbb{Z}\}$. By the remainder property, there are exactly $n$ classes, $[0]_n, [1]_n, \ldots, [n-1]_n$, and the numbers $0, 1, \ldots, n-1$ are a **complete residue system** modulo $n$. The set of classes is written $\mathbb{Z}/n\mathbb{Z}$ or $\mathbb{Z}_n$.

**Compatibility with the ring operations.** If $a \equiv b$ and $c \equiv d \pmod n$, then

$$a + c \equiv b + d, \qquad a - c \equiv b - d, \qquad ac \equiv bd \pmod n,$$

and $a^k \equiv b^k \pmod n$ for each integer $k \ge 0$.

*Proof.* Write $a = b + sn$ and $c = d + tn$. Then $a \pm c = (b \pm d) + (s \pm t)n$. For the product, $ac = bd + (bt + ds + stn)n$. The power follows by induction on $k$ from the product rule, with $a^0 = b^0 = 1$. $\square$

Because of this, the operations $[a] + [c] = [a + c]$ and $[a][c] = [ac]$ on classes are well defined. With them, $\mathbb{Z}/n\mathbb{Z}$ is a commutative ring with $n$ elements. Its additive group is the [additive group modulo n](/additive-group-modulo-n/), and its invertible elements form the [multiplicative group modulo n](/multiplicative-group-modulo-n/).

**Division.** Division does not carry over in general. The correct rule for cancellation is

$$ac \equiv bc \pmod n \quad \Longleftrightarrow \quad a \equiv b \pmod{n / \gcd(c, n)}.$$

*Proof.* Let $g = \gcd(c, n)$, $c = g c'$ and $n = g n'$, so $\gcd(c', n') = 1$. Then $n \mid (a - b)c$ if and only if $n' \mid (a - b)c'$, and since $\gcd(n', c') = 1$, this holds if and only if $n' \mid a - b$ by [Euclid's lemma](/euclids-lemma/) in its general form. $\square$

In particular, when $\gcd(c, n) = 1$, the factor $c$ can be cancelled. Then $c$ has a [modular inverse](/modular-inverse/) $c^{-1}$ with $c c^{-1} \equiv 1 \pmod n$, and "division by $c$" means multiplication by $c^{-1}$.

**Change of modulus.** If $a \equiv b \pmod n$ and $m \mid n$, then $a \equiv b \pmod m$. Conversely, $a \equiv b$ modulo each of $n_1, \ldots, n_k$ if and only if $a \equiv b \pmod{\operatorname{lcm}(n_1, \ldots, n_k)}$, because a number is a multiple of each $n_i$ exactly when it is a multiple of their [least common multiple](/least-common-multiple/).

**Representation on a computer.** A residue modulo $n$ is stored as its least non-negative representative, an integer in $0$ to $n - 1$. In C, C++, Java, Go and Rust, the operator `%` truncates the quotient toward zero, so `-7 % 3` is `-1`, not $2$. Python's `%` returns a result with the sign of the divisor, so `-7 % 3` is `2`. Portable code reduces a possibly negative value $x$ with `((x % n) + n) % n`, or with a conditional add of $n$.

## Examples and non-examples

- $38 \equiv 14 \pmod{12}$, because $38 - 14 = 24 = 2 \cdot 12$. Both leave remainder $2$. This is clock arithmetic: 38 hours after midnight, a 12-hour clock shows 2.
- $-7 \equiv 3 \pmod{10}$, because $-7 - 3 = -10$. The least non-negative residue of $-7$ is $3$, while C computes `-7 % 10` as `-7`.
- Every pair of integers is congruent modulo $1$, so $\mathbb{Z}/1\mathbb{Z}$ has one class. Modulo $2$ there are two classes, the even and the odd numbers.
- Since $10 \equiv 1 \pmod 9$, the rule for powers gives $10^k \equiv 1 \pmod 9$, so a number is congruent modulo $9$ to the sum of its decimal digits. For example $12345 \equiv 1 + 2 + 3 + 4 + 5 = 15 \equiv 6 \pmod 9$. This is the rule behind "casting out nines" and the [divisibility tests](/divisibility-tests/) for $3$ and $9$.
- **Cancellation fails without coprimality.** $2 \cdot 3 \equiv 2 \cdot 8 \pmod{10}$, since both sides are $6$ modulo $10$, but $3 \not\equiv 8 \pmod{10}$. Here $\gcd(2, 10) = 2$, and the correct rule gives only $3 \equiv 8 \pmod 5$, which is true.
- **Non-example: exponents.** Congruent bases give congruent powers, but congruent exponents do not. We have $1 \equiv 6 \pmod 5$, but $2^1 = 2$ and $2^6 = 64 \equiv 4 \pmod 5$. Exponents work modulo the order of the base, which divides $\varphi(n)$ by [Euler's theorem](/euler-theorem/) when the base is coprime to $n$.
- **Non-example: floor division.** $7 \equiv 9 \pmod 2$, but $\lfloor 7/2 \rfloor = 3$ and $\lfloor 9/2 \rfloor = 4$ are not congruent modulo $2$. Operations other than $+$, $-$ and $\times$ need not respect the relation.

## Related definitions

- [Divisibility](/divisibility/): the relation $n \mid a - b$ that defines a congruence.
- [Division with remainder](/division-with-remainder/): gives the canonical representative $a \bmod n$.
- [Equivalence relation](/equivalence-relation/): congruence modulo $n$ is one, and its classes are the residue classes.
- [Additive group modulo n](/additive-group-modulo-n/) and [multiplicative group modulo n](/multiplicative-group-modulo-n/): the groups that the classes form.
- [Modular inverse](/modular-inverse/): the class $c^{-1}$ that makes division by $c$ possible when $\gcd(c, n) = 1$.
- [Linear congruence](/linear-congruence/): the equation $ax \equiv b \pmod n$ in the unknown $x$.
- [Chinese remainder theorem](/chinese-remainder-theorem/): a system of congruences with pairwise coprime moduli has one solution modulo the product.
- [Euler's totient function](/euler-totient/): the number of classes modulo $n$ that are coprime to $n$.

## References
