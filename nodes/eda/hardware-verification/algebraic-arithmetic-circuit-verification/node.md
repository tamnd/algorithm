---
tag: TA6P1V
kind: technique
slug: algebraic-arithmetic-circuit-verification
name: Algebraic verification of arithmetic circuits
aliases:
- backward rewriting of multipliers
- Groebner basis circuit verification
area: eda/hardware-verification
level: research
summary: Models each gate as a polynomial and rewrites the specification of a multiplier or adder backward through the gates, a Groebner basis reduction that ends in zero if correct.
prereqs: [groebner-basis, multivariate-division-algorithm, ideal-membership-problem]
see_also: [groebner-basis, buchberger-criteria, multivariate-division-algorithm, ideal-membership-problem, hilbert-nullstellensatz, wallace-tree-multiplier, booth-multiplication, taylor-expansion-diagram]
sources:
  - paper: doi:10.23919/FMCAD.2017.8102237
    title: D. Ritirc, A. Biere and M. Kauers, Column-wise verification of multipliers using computer algebra, Formal Methods in Computer-Aided Design (FMCAD 2017), 23 to 30, 2017
    locator: the gate polynomials and field polynomials of a circuit, the term order that makes them a Groebner basis, the reduction of the multiplier specification, and its split by output columns
  - paper: doi:10.1109/TCAD.2013.2259540
    title: J. Lv, P. Kalla and F. Enescu, Efficient Groebner basis reductions for formal verification of Galois field arithmetic circuits, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 32(9), 1409 to 1420, 2013
    locator: the reverse topological term order under which the gate polynomials form a Groebner basis, and the reduction over finite fields of characteristic 2 with the vanishing polynomials x^q - x
  - paper: doi:10.23919/FMCAD.2019.8894250
    title: D. Kaufmann, A. Biere and M. Kauers, Verifying large multipliers by combining SAT and computer algebra, Formal Methods in Computer-Aided Design (FMCAD 2019), 28 to 36, 2019
    locator: the combination in which SAT checks a complex final-stage adder against a simple one and computer algebra checks the rest of the multiplier
  - paper: doi:10.1145/3316781.3317898
    title: A. Mahzoon, D. Grosse and R. Drechsler, RevSCA, using reverse engineering to bring light into backward rewriting for big and dirty multipliers, Design Automation Conference (DAC 2019), 2019
    locator: the growth of the intermediate polynomials in backward rewriting of optimized multipliers, and the identification of adder blocks that avoids it
---

Algebraic verification proves that a gate-level arithmetic circuit, such as a multiplier, computes its word-level specification. Each gate becomes a polynomial equation over the rationals. An AND gate $g = a \wedge b$ gives $-g + ab$, and an XOR gate $g = a \oplus b$ gives $-g + a + b - 2ab$. Each input $x$ gets the *vanishing polynomial* $x^2 - x$, which is zero exactly when $x \in \{0, 1\}$. For an $n$-bit multiplier the specification is the polynomial $S = \sum_i 2^i s_i - \bigl(\sum_i 2^i a_i\bigr)\bigl(\sum_j 2^j b_j\bigr)$. *Backward rewriting* replaces, in $S$, each gate output by its polynomial, from the outputs back to the inputs, and replaces $x^2$ by $x$. This is division by the gate polynomials, which form a [Gröbner basis](/groebner-basis/) for a term order that puts every gate above its inputs. The remainder is zero exactly when the circuit is correct, and a nonzero remainder gives an input that shows the bug. The check does not depend on how many input values there are, so it works for multipliers of hundreds of bits where [BDDs](/binary-decision-diagram/) of the outputs are exponential. Its cost is the size of the intermediate polynomials, which depends strongly on the architecture.

## In plain words

Write each wire of the circuit as a number that is 0 or 1. Each gate is then a small formula. The output of an AND gate is $a$ times $b$, and the output of an XOR gate is $a + b - 2ab$.

The specification is also a formula: the outputs, read as a binary number, minus the product of the two inputs. It must be 0 for every input.

Start with this formula and replace the output wires by their gate formulas. Then replace the wires that those use, back to the inputs. Wherever an input appears squared, replace $x^2$ by $x$, because $0^2 = 0$ and $1^2 = 1$. If everything cancels and you get 0, the circuit is correct for all inputs. If something is left, it is a formula in the inputs, and any input where it is not 0 is a bug.

## When it applies

- The circuit $C$ is combinational, with inputs $x_1, \ldots, x_n$ and gates $g_1, \ldots, g_m$ in topological order. Each gate computes a Boolean function of earlier signals, and the outputs are some of the signals. The polynomial ring is $\mathbb{Q}[x_1, \ldots, x_n, g_1, \ldots, g_m]$, over the field $\mathbb{Q}$ of rationals, with one variable per signal.
- Each gate $g = \mathrm{op}(u_1, \ldots, u_k)$ has a polynomial $P_g(u_1, \ldots, u_k)$ that equals $\mathrm{op}$ on $\{0, 1\}^k$. For the usual gates: $\neg a \mapsto 1 - a$, $a \wedge b \mapsto ab$, $a \vee b \mapsto a + b - ab$, $a \oplus b \mapsto a + b - 2ab$. The *gate polynomial* is $-g + P_g$.
- The *gate ideal* is $J = \langle -g_j + P_{g_j} \ (1 \le j \le m),\ x_i^2 - x_i \ (1 \le i \le n) \rangle$. The polynomials $x_i^2 - x_i$ are the vanishing polynomials of $\{0, 1\}$.
- The specification is a polynomial $S$ in the signals. The circuit is *correct* if $S(a, C(a)) = 0$ for every input $a \in \{0, 1\}^n$, where $C(a)$ are the values of the gates. For an unsigned $n \times n$ multiplier with outputs $s_0, \ldots, s_{2n-1}$, $S = \sum_{i < 2n} 2^i s_i - \bigl(\sum_{i < n} 2^i a_i\bigr)\bigl(\sum_{j < n} 2^j b_j\bigr)$.
- The term order is lexicographic, with every gate variable larger than every variable in its fanin cone, for example $g_m > \cdots > g_1 > x_n > \cdots > x_1$. Then the leading term of $-g_j + P_{g_j}$ is $g_j$, since $P_{g_j}$ uses only smaller variables, and the leading term of $x_i^2 - x_i$ is $x_i^2$.

## The template

```pseudo id=main
ALGEBRAIC-CHECK(C, S)
L1  order the variables so that each gate is larger than every variable in its fanin cone
L2  G ← {−g + P_g for each gate g} ∪ {x² − x for each input x}
L3  r ← S
L4  for each gate g, from the outputs back to the inputs, do
L5      r ← r with every occurrence of g replaced by P_g         ▷ backward rewriting
L6      in r, replace every power x^k with k ≥ 2 of an input by x
L7  if r = 0 then return correct
L8  m ← a monomial of r of least degree
L9  return the counterexample: the inputs of m set to 1, all other inputs 0
```

Lines L4 to L6 are the [multivariate division](/multivariate-division-algorithm/) of $S$ by $G$, with the reductions done in a fixed order. Replacing $g$ by $P_g$ subtracts a multiple of $-g + P_g$, and replacing $x^2$ by $x$ subtracts a multiple of $x^2 - x$. When the loop ends, no term of $r$ contains a gate variable, and no input has an exponent above 1.

**$G$ is a Gröbner basis.** The leading terms $g_1, \ldots, g_m, x_1^2, \ldots, x_n^2$ are pairwise coprime. By Buchberger's product criterion ([Buchberger's criteria](/buchberger-criteria/)), the S-polynomial of two polynomials with coprime leading terms reduces to 0, so $G$ is a Gröbner basis of $J$ with no computation. So the remainder of $S$ is unique, whatever order of reductions is used, and $S \in J$ exactly when it is 0. This is the [ideal membership](/ideal-membership-problem/) test of the method.

**Theorem.** With $\mathbb{Q}$, $J$, the order and $r$ as above, the following are equivalent: (1) the circuit is correct; (2) $S \in J$; (3) $r = 0$. If $r \ne 0$, the input of line L9 makes $S(a, C(a)) \ne 0$.

*Proof.* The points of the circuit are the vectors $(a, C(a))$ with $a \in \{0, 1\}^n$. Every polynomial of $G$ vanishes at each of them: $a_i^2 - a_i = 0$ for $a_i \in \{0, 1\}$, and $-g + P_g = 0$ because $P_g$ equals the gate function on 0-1 values and $g$ is that value. So every polynomial of $J$ vanishes at every point of the circuit.

(3) implies (2): lines L4 to L6 subtract multiples of polynomials of $G$, so $S - r \in J$, and $r = 0$ gives $S \in J$. (2) implies (1): $S$ is in $J$, so it vanishes at every point of the circuit.

(1) implies (3): $r$ has no gate variable and no input with an exponent above 1, so $r$ is a multilinear polynomial in $x_1, \ldots, x_n$. Since $S - r \in J$, $r(a) = S(a, C(a))$ for every $a \in \{0, 1\}^n$, and by (1) $r$ is zero on all of $\{0, 1\}^n$. A multilinear polynomial that is zero on $\{0, 1\}^n$ is the zero polynomial. By induction on $n$: write $r = r_0 + x_n r_1$ with $r_0, r_1$ multilinear in $x_1, \ldots, x_{n-1}$. Setting $x_n = 0$ shows that $r_0$ is zero on $\{0, 1\}^{n-1}$, and setting $x_n = 1$ shows that $r_0 + r_1$ is, hence $r_1$ too. By induction both are 0, so $r = 0$.

For the counterexample, let $r \ne 0$ and let $m = \prod_{i \in T} x_i$ have least degree among the monomials of $r$. At the point $a = \mathbf{1}_T$, a monomial $\prod_{i \in U} x_i$ is 1 exactly when $U \subseteq T$. Every monomial of $r$ other than $m$ has degree at least $|T|$ and differs from $m$, so it is not a subset of $T$. So $r(a)$ is the coefficient of $m$, which is not 0, and $S(a, C(a)) = r(a) \ne 0$. $\square$

The proof does not need the Gröbner basis property; it uses only that the remainder is multilinear in the inputs. The property says more: the remainder does not depend on the order in which the reductions are done. Rewriting with the leading coefficient $-1$ of every gate polynomial never divides, so a specification with integer coefficients keeps integer coefficients throughout.

**Example.** A 2-bit multiplier has inputs $a_1 a_0$ and $b_1 b_0$, partial products $s_0 = a_0 b_0$, $p_{01} = a_0 b_1$, $p_{10} = a_1 b_0$, $p_{11} = a_1 b_1$, and two half adders: $s_1 = p_{01} \oplus p_{10}$, $c_1 = p_{01} \wedge p_{10}$, $s_2 = p_{11} \oplus c_1$, $s_3 = p_{11} \wedge c_1$. The specification is $S = 8 s_3 + 4 s_2 + 2 s_1 + s_0 - (2 a_1 + a_0)(2 b_1 + b_0)$. Write $Q = 4 a_1 b_1 + 2 a_1 b_0 + 2 a_0 b_1 + a_0 b_0$ for the product.

| step | rewrite | $r$ |
|---|---|---|
| start | | $8 s_3 + 4 s_2 + 2 s_1 + s_0 - Q$ |
| 1 | $s_3 \to p_{11} c_1$ | $8 p_{11} c_1 + 4 s_2 + 2 s_1 + s_0 - Q$ |
| 2 | $s_2 \to p_{11} + c_1 - 2 p_{11} c_1$ | $4 p_{11} + 4 c_1 + 2 s_1 + s_0 - Q$ |
| 3 | $c_1 \to p_{01} p_{10}$ | $4 p_{11} + 4 p_{01} p_{10} + 2 s_1 + s_0 - Q$ |
| 4 | $s_1 \to p_{01} + p_{10} - 2 p_{01} p_{10}$ | $4 p_{11} + 2 p_{01} + 2 p_{10} + s_0 - Q$ |
| 5 | the four partial products | $Q - Q = 0$ |

In steps 2 and 4 the products $p_{11} c_1$ and $p_{01} p_{10}$ cancel: the carry of a half adder takes over the part of the sum that the XOR loses. If the bug $c_1 = p_{01} \vee p_{10}$ replaces the AND, step 3 gives $4 p_{01} + 4 p_{10} - 4 p_{01} p_{10}$, and the remainder is $r = 4 a_0 b_1 + 4 a_1 b_0 - 8 a_0 a_1 b_0 b_1$. Its least monomial is $a_0 b_1$, so line L9 sets $a_0 = b_1 = 1$ and $a_1 = b_0 = 0$. Then $1 \cdot 2 = 2$, but the circuit gives $s_1 = 1$, $c_1 = 1$, $s_2 = 1$, so the output is $6$, and $r = 4$ is the difference.

**Cost.** Lines L1 and L2 are linear in the circuit. A rewrite at line L5 multiplies the terms that contain $g$ by $P_g$, so the number of terms of $r$ can grow. Deciding correctness is coNP-hard in general: with the specification $S = s$ for one output $s$, correctness says that $s$ is 0 on every input, which is the unsatisfiability of a circuit, a [coNP-complete](/co-np-complete/) problem. So no order of rewriting is polynomial for all circuits unless P = NP. The size of $r$ in practice is measured, not proved. For array and simple tree multipliers, the papers in the references report remainders that stay small with a good order, and for optimized multipliers with complex final adders they report a large growth that their methods avoid.

## Classic examples

- **Simple multipliers.** [Array multipliers](/array-multiplier/) and [Wallace tree](/wallace-tree-multiplier/) or [Dadda](/dadda-multiplier/) multipliers built from half and full adders. Ritirc, Biere and Kauers (2017) split the specification by output columns and rewrite one column at a time, which keeps the polynomials small.
- **Galois field multipliers.** Lv, Kalla and Enescu (2013) work over the finite field $\mathbb{F}_{2^k}$, with a word variable per operand and the vanishing polynomials $x^{2^k} - x$ for the words and $x^2 - x$ for the bits. The same term order makes the gate polynomials a Gröbner basis.
- **Optimized multipliers.** [Booth encoding](/booth-multiplication/) and parallel prefix final adders make the intermediate polynomials blow up. Kaufmann, Biere and Kauers (2019) check a complex final adder against a ripple-carry adder with SAT and use algebra for the rest. Mahzoon, Grosse and Drechsler (2019) first find the half and full adders and other blocks, then rewrite.
- **Adders and sums.** A [ripple-carry adder](/ripple-carry-adder/) with the specification $\sum_i 2^i s_i - \sum_i 2^i a_i - \sum_i 2^i b_i$ reduces to 0 in one pass, full adder by full adder.

## Variations

- **Over the integers.** All leading coefficients are $-1$, so the reduction stays in $\mathbb{Z}[X]$ and needs no fractions.
- **Forward or mixed rewriting.** Rewriting from the inputs builds the polynomial of each output, as in function extraction. Rewriting backward keeps only one polynomial but depends on the order.
- **Rewriting rules for XOR chains and adders.** Preprocessing that merges gates into half and full adders, or eliminates internal variables first, changes the gate polynomials but not the ideal of the circuit points.
- **Word-level specifications.** The specification can be any polynomial of the input words that has integer values. A [Taylor expansion diagram](/taylor-expansion-diagram/) represents such word-level polynomials canonically, and BMDs represent the bit-level ones.
- **Counterexamples.** A nonzero remainder is a polynomial in the inputs. Line L9 gives one failing input, and any zero of $r$ on $\{0, 1\}^n$ is a passing one.

## Pitfalls

- **The term order.** Rewriting a gate before every gate that uses it would leave it in the polynomial. Use a reverse topological order of the whole circuit, not of each output cone.
- **Missing vanishing polynomials.** Without $x^2 - x$, the remainder of a correct circuit can be a nonzero polynomial that is zero only on 0-1 points, such as $a^2 - a$, and the check reports a false bug.
- **Truncated outputs.** A multiplier with only $n$ outputs computes $a \cdot b$ modulo $2^n$. The specification then holds only modulo $2^n$. Over $\mathbb{Q}$ the number $2^n$ is a unit, so the check must work over the integers with $2^n$ added to the ideal, which is outside the theorem of this page, or keep all $2n$ outputs.
- **Signed numbers.** A two's complement word has the polynomial $-2^{n-1} a_{n-1} + \sum_{i < n-1} 2^i a_i$. A specification with the unsigned form fails on a correct signed multiplier.
- **Blowup without a bug.** A large remainder during rewriting is not a sign of a bug. Optimized designs need the methods above before the rewrite.

## Exercises

1. Write the gate polynomials of a full adder with sum $a \oplus b \oplus c$ and carry $ab \vee ac \vee bc$, and reduce $2 c_{\mathrm{out}} + s - a - b - c$ to 0.
2. Show that $S = s$ is in $J$ if and only if the output $s$ is 0 on every input, and conclude that the problem is coNP-hard.
3. Reduce the specification of the 2-bit multiplier of the example with $s_2 = p_{11} \vee c_1$ and find the counterexample of line L9.

## References
