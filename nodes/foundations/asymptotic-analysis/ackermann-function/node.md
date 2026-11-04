---
tag: M3HCCH
kind: definition
slug: ackermann-function
name: Ackermann function
aliases:
- Ackermann-Péter function
area: foundations/asymptotic-analysis
level: advanced
summary: A total recursive function that grows faster than any primitive recursive function, used to show non-primitive-recursive growth.
prereqs: [computable-function, primitive-recursive-function]
see_also: [inverse-ackermann-function, iterated-logarithm, partial-recursive-function]
sources:
  - paper: doi:10.1007/BF01459088
    title: Wilhelm Ackermann, Zum Hilbertschen Aufbau der reellen Zahlen, Mathematische Annalen 99, 1928, pages 118 to 133
    locator: the three-argument function and the proof that it is not primitive recursive
  - paper: doi:10.1007/BF01472200
    title: Rózsa Péter, Konstruktion nichtrekursiver Funktionen, Mathematische Annalen 111, 1935, pages 42 to 60
    locator: a two-argument function that is not primitive recursive
  - paper: doi:10.1090/S0002-9904-1948-09121-2
    title: Raphael M. Robinson, Recursion and double recursion, Bulletin of the American Mathematical Society 54(10), 1948, pages 987 to 993
    locator: the two-argument form A(0, n) = n + 1, A(m + 1, 0) = A(m, 1), A(m + 1, n + 1) = A(m, A(m + 1, n))
  - paper: doi:10.1126/science.194.4271.1235
    title: Donald E. Knuth, Mathematics and computer science, coping with finiteness, Science 194(4271), 1976, pages 1235 to 1242
    locator: the up-arrow notation
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 19.4 (the function A_k(j) in the analysis of disjoint-set forests)
---

The Ackermann function is a function of two natural numbers that is defined by a short recursion, always halts, and grows faster than every primitive recursive function. This page uses the two-argument Ackermann-Péter form $A(m, n)$ unless it says otherwise. Its slow inverse appears in the cost of [union-find](/disjoint-set-forest/), see [the inverse Ackermann function](/inverse-ackermann-function/).

## Definition

The Ackermann-Péter function $A : \mathbb{N} \times \mathbb{N} \to \mathbb{N}$ is defined by three rules, for all $m, n \ge 0$.

$$A(0, n) = n + 1$$

$$A(m + 1, 0) = A(m, 1)$$

$$A(m + 1, n + 1) = A(m, A(m + 1, n))$$

**It is total.** Order the pairs $(m, n)$ by the lexicographic order: $(m', n') < (m, n)$ when $m' < m$, or $m' = m$ and $n' < n$. This order has no infinite descending chain: in a descending chain, the first component can decrease only finitely often, and while it stays fixed, the second component can decrease only finitely often. Each rule computes its value from calls on smaller pairs. Rule 1 makes no call. Rule 2 computes $A(m + 1, 0)$ with one call on $(m, 1)$, which is smaller than $(m + 1, 0)$ because $m < m + 1$. Rule 3 computes $A(m + 1, n + 1)$ with a first call on $(m + 1, n)$, which is smaller because $n < n + 1$, and then a call on $(m, k)$ with $k = A(m + 1, n)$, which is smaller because $m < m + 1$, whatever $k$ is. By induction on this order, each call halts and gives one value.

**It is computable.** The three rules are a recursive program, so $A$ is a [computable function](/computable-function/). It is a total [partial recursive function](/partial-recursive-function/).

**Basic properties.** For all $m, n \ge 0$:

1. $A(m, n) > n$.
2. $A(m, n + 1) > A(m, n)$, so each row is increasing.
3. $A(m + 1, n) \ge A(m, n + 1)$.
4. $A(m + 1, n) > A(m, n)$, so each column is increasing.

Proof of 1, by induction on $m$ and, inside it, on $n$. For $m = 0$, $A(0, n) = n + 1 > n$. For $m + 1$ and $n = 0$, the outer hypothesis gives $A(m + 1, 0) = A(m, 1) > 1 > 0$. For $A(m + 1, n + 1) = A(m, k)$ with $k = A(m + 1, n)$: the inner hypothesis gives $k \ge n + 1$, and the outer hypothesis gives $A(m, k) \ge k + 1 \ge n + 2$. Proof of 2: for $m = 0$, $A(0, n + 1) = n + 2 > n + 1 = A(0, n)$. For $m + 1$, $A(m + 1, n + 1) = A(m, A(m + 1, n)) > A(m + 1, n)$ by property 1. Proof of 3, by induction on $n$: for $n = 0$ both sides are equal by rule 2. For $n + 1$, the hypothesis and property 1 give $A(m + 1, n) \ge A(m, n + 1) \ge n + 2$, so property 2 gives $A(m + 1, n + 1) = A(m, A(m + 1, n)) \ge A(m, n + 2)$. Property 4 follows from 3 and 2: $A(m + 1, n) \ge A(m, n + 1) > A(m, n)$.

**Each row is primitive recursive.** Row 0 is the successor. If row $m$ is primitive recursive, then row $m + 1$ is defined by primitive recursion on $n$ from the constant $A(m, 1)$ and the step $A(m + 1, n + 1) = A(m, A(m + 1, n))$, so it is primitive recursive too. The function of two arguments is not, as we show next.

**It is not primitive recursive.** Ackermann (1928) proved this for his three-argument function, and Péter (1935) for a function of two arguments. Robinson (1948) gave the form used on this page. The proof below is the standard domination argument. The key statement is:

> For each [primitive recursive function](/primitive-recursive-function/) $f : \mathbb{N}^r \to \mathbb{N}$ there is a $k$ with $f(x_1, \dots, x_r) < A(k, \max_i x_i)$ for all arguments. In particular, for each primitive recursive $f : \mathbb{N} \to \mathbb{N}$ there is a $k$ with $f(n) < A(k, n)$ for all $n \ge 0$.

*A lemma.* For all $m_1, m_2, n$, with $m = \max(m_1, m_2)$: $A(m_1, A(m_2, n)) < A(m + 2, n)$. Proof: by properties 2 and 4, $A(m_1, A(m_2, n)) \le A(m, A(m, n))$. By property 2 and then rule 3, $A(m, A(m, n)) < A(m, A(m + 1, n)) = A(m + 1, n + 1)$. By property 3, $A(m + 1, n + 1) \le A(m + 2, n)$.

*Proof of the statement*, by induction on the definition of $f$. Write $X = \max_i x_i$, with $X = 0$ for a function of no arguments.

- The zero function: $0 < X + 1 = A(0, X)$, so $k = 0$.
- The successor: $x + 1 < x + 2 = A(1, x)$, so $k = 1$.
- A projection: $x_i \le X < A(0, X)$, so $k = 0$.
- Composition $f(\bar x) = h(g_1(\bar x), \dots, g_q(\bar x))$, with $h < A(k_h, \cdot)$ and each $g_j < A(k_j, \cdot)$. Let $k_g = \max_j k_j$. Then $\max_j g_j(\bar x) < A(k_g, X)$, and by property 2, $f(\bar x) < A(k_h, \max_j g_j(\bar x)) < A(k_h, A(k_g, X))$. The lemma gives $k = \max(k_h, k_g) + 2$.
- Primitive recursion $f(0, \bar y) = g(\bar y)$ and $f(t + 1, \bar y) = h(t, f(t, \bar y), \bar y)$, with $g < A(k_g, \cdot)$ and $h < A(k_h, \cdot)$. Let $c = \max(k_g, k_h) + 1$ and $M = \max_i y_i$. First, $f(t, \bar y) < A(c, t + M)$ by induction on $t$. For $t = 0$: $g(\bar y) < A(k_g, M) \le A(c, M)$ by property 4. For $t + 1$: the three arguments $t$, $f(t, \bar y)$ and $M$ are each less than $A(c, t + M)$, by the hypothesis and property 1. So, by properties 2 and 4 and rule 3, $f(t + 1, \bar y) < A(k_h, A(c, t + M)) \le A(c - 1, A(c, t + M)) = A(c, t + M + 1)$. Second, with $X = \max(t, M)$, we have $t + M \le 2X < 2X + 3 = A(2, X)$, so $f(t, \bar y) < A(c, A(2, X))$, and the lemma gives $k = \max(c, 2) + 2$.

This proves the statement. $\square$

Hence the function $n \mapsto A(n, n)$ is not primitive recursive. Suppose it were. Then $g(n) = A(n, n) + 1$ would be primitive recursive, so $g(n) < A(k, n)$ for all $n$ and some $k$. At $n = k$ this gives $A(k, k) + 1 < A(k, k)$, which is false. It follows that $A$, as a function of two arguments, is not primitive recursive: if it were, then $n \mapsto A(n, n)$ would be primitive recursive too, because it is $A$ composed with two copies of the identity.

## Examples and non-examples

The table gives $A(m, n)$ for $m \le 3$ and $0 \le n \le 6$. The values agree with the closed forms below.

| $m \backslash n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| 2 | 3 | 5 | 7 | 9 | 11 | 13 | 15 |
| 3 | 5 | 13 | 29 | 61 | 125 | 253 | 509 |

For $m = 4$ the first values are $A(4, 0) = 13$ and $A(4, 1) = 65533$ (the recursion gives $A(4,0) = A(3,1) = 13$, and $A(4,1) = A(3, 13) = 65533$). Then $A(4, 2) = 2^{65536} - 3$, a number with 19729 decimal digits. The value $A(4, 3)$ has no practical decimal form, and this page does not list it. The diagonal is $A(0, 0) = 1$, $A(1, 1) = 3$, $A(2, 2) = 7$, $A(3, 3) = 61$, and $A(4, 4) = t(7) - 3$ with the tower $t$ below.

**Closed forms.** For all $n \ge 0$:

- $A(0, n) = n + 1$.
- $A(1, n) = n + 2$.
- $A(2, n) = 2n + 3$.
- $A(3, n) = 2^{n+3} - 3$.

Each follows by induction on $n$ from the previous row. For $m = 1$: $A(1, 0) = A(0, 1) = 2$, and $A(1, n + 1) = A(0, A(1, n)) = A(1, n) + 1$. For $m = 2$: $A(2, 0) = A(1, 1) = 3$, and $A(2, n + 1) = A(1, A(2, n)) = A(2, n) + 2$. For $m = 3$: $A(3, 0) = A(2, 1) = 5 = 2^3 - 3$, and $A(3, n + 1) = A(2, A(3, n)) = 2 A(3, n) + 3 = 2(2^{n+3} - 3) + 3 = 2^{n+4} - 3$.

**Tower form for $m = 4$.** Let $t(k)$ be the tower of $k$ twos: $t(1) = 2$ and $t(k + 1) = 2^{t(k)}$. Then $A(4, n) = t(n + 3) - 3$ for all $n \ge 0$. The base case is $A(4, 0) = 13 = 16 - 3 = t(3) - 3$. The step is $A(4, n + 1) = A(3, A(4, n)) = 2^{A(4,n) + 3} - 3 = 2^{t(n+3)} - 3 = t(n + 4) - 3$. So $A(4, 1) = 2^{16} - 3 = 65533$ and $A(4, 2) = 2^{65536} - 3$, as above.

**General form.** Knuth's up-arrow notation (Knuth, 1976) sets $a \uparrow^{0} b = ab$, $a \uparrow^{k} 1 = a$ for $k \ge 1$, and $a \uparrow^{k} (b + 1) = a \uparrow^{k-1} (a \uparrow^{k} b)$ for $k \ge 1$. So $a \uparrow^1 b = a^b$, and $a \uparrow^{k} b$ for $k \ge 2$ applies $a \uparrow^{k-1} \cdot$ to $a$, $b - 1$ times. For all $m \ge 2$ and $n \ge 0$,

$$A(m, n) = 2 \uparrow^{m-2} (n + 3) - 3.$$

*Proof*, by induction on $m$, and inside it on $n$. The case $m = 2$ is $2(n + 3) - 3 = 2n + 3$. Let $m \ge 3$ and $k = m - 2 \ge 1$. First, $2 \uparrow^{j} 2 = 4$ for every $j \ge 0$: for $j = 0$ it is $2 \cdot 2$, and for $j \ge 1$ it is $2 \uparrow^{j-1} 2$. So $2 \uparrow^{k} 3 = 2 \uparrow^{k-1} (2 \uparrow^{k} 2) = 2 \uparrow^{k-1} 4$, and rule 2 with the hypothesis for $m - 1$ gives $A(m, 0) = A(m - 1, 1) = 2 \uparrow^{k-1} 4 - 3 = 2 \uparrow^{k} 3 - 3$. For the step, rule 3 and the two hypotheses give $A(m, n + 1) = A(m - 1, A(m, n)) = 2 \uparrow^{k-1} (A(m, n) + 3) - 3 = 2 \uparrow^{k-1} (2 \uparrow^{k} (n + 3)) - 3 = 2 \uparrow^{k} (n + 4) - 3$. $\square$

The rows 2, 3 and 4 above are the cases $k = 0, 1, 2$. So row $m$ is one level of the hierarchy of multiplication, power, tower and the higher operations.

**An example of the theorem.** $f(n) = 2^n$ is primitive recursive, and it is below row 3: $2^n < 2^{n+3} - 3 = A(3, n)$ for all $n \ge 0$, because $7 \cdot 2^n > 3$.

**A non-example.** The function $n \mapsto A(n, n)$ is not below any single row, as the proof above shows. Each row is below the diagonal from some point on: by property 4, $A(m, n) < A(n, n)$ for every $n > m$.

**A computation.** The rules can run as a program with an explicit stack of pending first arguments: rule 3 pushes $m$ and then $m + 1$, rule 2 pushes $m$, and rule 1 adds 1 to the current second argument. For $A(4, 1)$ this program applies a rule $2\,862\,984\,010$ times, and its stack grows to $65\,532$ entries before the result $65\,533$ appears. For $A(3, 3) = 61$ it applies a rule $2\,432$ times, with at most 60 entries on the stack.

### Pitfalls

- **Stack overflow.** A direct recursive program for $A(4, 1)$ nests more than 65 000 calls, so it fails with the usual stack size. The explicit stack above avoids the overflow, but not the billions of steps. $A(4, 2)$ is out of reach of the rules in practice: its value has 19 729 digits, and rule 1 adds only 1 at a time.
- **Fast growth alone does not leave the class.** $2^n$, $n!$ and the tower $t(n)$ are primitive recursive. The theorem is about a function that is above every row, not about fast growth in general.
- **Not every total computable function is primitive recursive.** $A$ is total and computable, but not primitive recursive. So "total and computable" and "primitive recursive" are different classes.
- **Several functions share the name.** The function of Ackermann, the function of this page, the variant $A_k(j)$ of CLRS, and the function of the first edition of CLRS give different values at the same arguments. Read the definition first.

## Related definitions

**Ackermann's original function (1928).** Ackermann used three arguments. A common statement of it is $\varphi(a, b, 0) = a + b$, $\varphi(a, 0, 1) = 0$, $\varphi(a, 0, 2) = 1$, $\varphi(a, 0, c) = a$ for $c > 2$, and $\varphi(a, b + 1, c + 1) = \varphi(a, \varphi(a, b, c + 1), c)$. So $c = 0, 1, 2$ give addition, multiplication and exponentiation. The two-argument function above is a later simplification. The names "Ackermann function" and "Ackermann-Péter function" are used for the two-argument form.

**The variant of CLRS, Section 19.4.** In the analysis of union by rank and path compression, CLRS defines for integers $k \ge 0$ and $j \ge 1$

$$A_0(j) = j + 1, \qquad A_k(j) = A_{k-1}^{(j+1)}(j) \quad (k \ge 1),$$

where $f^{(i)}$ is $f$ applied $i$ times. This $A_k(j)$ is not the same function as $A(k, j)$. Some values: $A_1(j) = 2j + 1$, $A_2(j) = 2^{j+1}(j + 1) - 1$, and $A_0(1) = 2$, $A_1(1) = 3$, $A_2(1) = 7$, $A_3(1) = 2047$. Its inverse is $\alpha(n)$, see [the inverse Ackermann function](/inverse-ackermann-function/).

**Other forms.** The first edition of the book (Cormen, Leiserson and Rivest, 1990), in the spirit of Tarjan (1975), uses another two-argument function, with $A(1, j) = 2^j$. It is given on the page of the inverse function. The forms give different values at the same arguments. When a paper uses "the Ackermann function", read its definition first.

The [iterated logarithm](/iterated-logarithm/) is the inverse of the tower function $t(k)$, and it inverts row 4 exactly up to a shift: since $t(n + 2) < t(n + 3) - 3 < t(n + 3)$, we get $\lg^* A(4, n) = n + 3$. The [inverse Ackermann function](/inverse-ackermann-function/) inverts the diagonal, or the values $A_k(1)$ in CLRS, so it grows far more slowly than $\lg^* n$.

## References
