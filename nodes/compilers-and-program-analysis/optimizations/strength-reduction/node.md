---
tag: FGNWMJ
kind: technique
slug: strength-reduction
name: Strength reduction
aliases:
- reduction in strength
area: compilers-and-program-analysis/optimizations
level: core
summary: Replaces costly operations by cheaper ones, such as a multiply by an induction variable in a loop by an add each iteration.
prereqs: [loop-invariant-code-motion, natural-loop, induction-variable-analysis]
see_also: [operator-strength-reduction, peephole-optimization, chains-of-recurrences, ssapre, copy-propagation, dead-code-elimination, constant-folding, static-single-assignment-form]
sources:
  - book: isbn:9780137296811
    title: Frances E. Allen, John Cocke and Ken Kennedy, Reduction of operator strength, in Steven S. Muchnick and Neil D. Jones (eds.), Program Flow Analysis, Theory and Applications, Prentice-Hall, 1981
    locator: pp. 79-101, the reduction of products of induction variables and region constants in strongly connected regions, and linear function test replacement
  - paper: doi:10.1145/359863.359888
    title: John Cocke and Ken Kennedy, An algorithm for reduction of operator strength, Communications of the ACM 20(11), 1977, 850-856
    locator: the algorithm with a table of temporaries indexed by the reduced expression, and the extension to linear function test replacement
  - paper: doi:10.1145/504709.504710
    title: Keith D. Cooper, L. Taylor Simpson and Christopher A. Vick, Operator strength reduction, ACM Transactions on Programming Languages and Systems 23(5), 2001, 603-625
    locator: the formulation on SSA form, with induction variables found as strongly connected components
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 9.1.8 (Induction Variables and Reduction in Strength)
  - paper: doi:10.1145/178243.178249
    title: Torbjörn Granlund and Peter L. Montgomery, Division by invariant integers using multiplication, Proceedings of the ACM SIGPLAN 1994 Conference on Programming Language Design and Implementation (PLDI), 1994, 61-72
    locator: the replacement of a division by a constant or by a loop-invariant divisor with a multiplication and shifts, for unsigned and signed operands
---

Strength reduction replaces an operation by a cheaper one that gives the same result. In one instruction, a multiply by 8 becomes a shift by 3. In a loop, the important case, a product `i * k` of an *induction variable* `i`, which the loop changes by the same amount each time, and a value `k` that the loop does not change, becomes a new variable `t`. The loop keeps `t` equal to `i * k` with one add each time it changes `i`. The multiply goes away. Often `i` is then used only to test for the end of the loop, and *linear function test replacement* rewrites that test in terms of `t`, so that `i` dies.

## In plain words

Some operations cost more than others: a multiply costs more than an add, and a divide costs much more. If a loop counts 0, 1, 2, 3 and multiplies the count by 7 each time, the products are 0, 7, 14, 21. The compiler can keep a second counter that starts at 0 and goes up by 7 each time, and drop the multiply. In the same way, a multiply by 8 can become a shift, which is cheaper. The new form must give the same answer for every input. A divide by 8 is not the same as a shift for negative numbers, so that change needs extra work.

## When it applies

**Local strength reduction.** Inside one instruction, the rewrite is an identity of the target arithmetic. On integers, and on two's complement integers that wrap, `x * 2^s` equals `x << s`, and `x * 2` equals `x + x`. A multiply by another constant can become a few shifts and adds, and a division by a constant can become a multiply by a precomputed constant and a shift, as Granlund and Montgomery show. The identity must hold for every value of the operand, including negative ones, see the pitfalls. [Peephole optimization](/peephole-optimization/) and instruction selection do most of these rewrites.

**Loop strength reduction.** Take a [natural loop](/natural-loop/) $L$ with a preheader $p$: a block that runs once on each entry of the loop and jumps to the header, as defined in [loop-invariant code motion](/loop-invariant-code-motion/). A value is *invariant in $L$* if it is a constant or a name that no instruction of $L$ defines and that is not address-taken. The rewrite applies to an instruction $I$: `x = i * k` in $L$ when:

- **(C1) A basic induction variable.** `i` is not address-taken, and every instruction of $L$ that defines `i` has the form `i = i + c` or `i = i - c`, with $c$ invariant in $L$. Different definitions may use different $c$.
- **(C2) An invariant factor.** `k` is invariant in $L$.

The same rewrite works for `x = k * i`, and with an add in place of the product for `x = i + k`. A name `j` defined only by such reduced forms is a *derived induction variable*, and a product of `j` with an invariant can be reduced in turn. [Induction variable analysis](/induction-variable-analysis/) finds these families.

## The template

**The rewrite.** Pick fresh names `t` and, for each definition `i = i + c` in $L$, a name `d`. At the end of $p$, before its jump, add `t = i * k` and `d = c * k`. Right after each `i = i + c` in $L$, add `t = t + d`, and right after each `i = i - c`, add `t = t - d`. Replace $I$ by the copy `x = t`. [Copy propagation](/copy-propagation/) then replaces the uses of `x` by `t`, and [constant folding](/constant-folding/) simplifies `d = 1 * k` and `t = 0 * k`.

**Linear function test replacement.** If after the rewrite `i` is read only by its own updates and by an exit test `c = i < n` with `n` invariant, and `k` is known to be positive, replace the test by `c = t < m`, with `m = n * k` added at the end of $p$. For $k > 0$, $i < n$ holds exactly when $i k < n k$. For $k < 0$ the comparison turns around. Then `i` is read only by its updates, and [dead code elimination](/dead-code-elimination/) removes it.

**Legality.** (C1) and (C2) are found by a scan of the definitions in $L$, or on SSA form as a strongly connected component of the graph of definitions, as in [operator strength reduction](/operator-strength-reduction/). The test replacement also needs the sign of `k`, and on machine integers it needs `n * k` and every value of `t` to fit without wrapping.

**Profit.** The cost model is the cost of the instructions executed, with a multiply more costly than an add. The rewrite removes one multiply per execution of $I$ and adds one add per execution of each update of `i`, plus two multiplies per entry of the loop. It pays when $I$ runs about as often as the updates. If $I$ sits behind a test that rarely holds, or the loop body runs zero times, the adds and the preheader multiplies can cost more than the multiplies saved. The new name `t` also stays live through the whole loop, which adds register pressure. On machines where a multiply costs about as much as an add, the gain is small, and the main benefit is that addresses `base + i * w` become pointers that move by `w`.

**Proof that behavior stays the same.** Let $Q$ be the program with the preheader $p$ and let $Q'$ be the result. The two programs have the same blocks and the same terminators. $Q'$ has extra instructions that write only the fresh names `t` and `d`, and $I$ is a copy instead of a product. None of these can trap. Run both on the same input, block by block. Every name of $Q$ has the same value in both runs, and the memory is the same, at every matched point, except perhaps `x` right after $I$. We show that `x` also agrees, so this holds everywhere and the runs have the same outcome.

Consider one visit of the loop, from an arrival at $p$ until the run leaves $L$. Inside it, no instruction writes `k` or any $c$, by (C1) and (C2): they are not defined in $L$, and a store or a call cannot write a name that is not address-taken. So `k` and each $c$ keep the values they have at the end of $p$. Claim: in $Q'$, at every point of the visit outside the gap between an update of `i` and the add that follows it, $t = i \cdot k$ and $d = c \cdot k$ for each `d`.

- At the end of $p$, `t = i * k` and `d = c * k` have just run.
- `i` changes only at an update `i = i + c`, which the add `t = t + d` follows at once. After both, $t = i k + c k = (i + c) k$. The same holds for `i = i - c` with a minus. This identity holds on the integers and on integers modulo $2^w$, so it holds for wrapping machine arithmetic too.
- No other instruction writes `t`, `d`, `i`, `k` or $c$.

At $I$, which is outside every gap, `x = t` therefore writes $i \cdot k$, the same value that `x = i * k` writes in $Q$. Outside the visits, `t` and `d` are never read. So the two runs agree on every name of $Q$ and on the memory at every matched point, take the same branches, and end the same way.

For the test replacement: at the test, $t = i k$ and $m = n k$ by the same argument, and for $k > 0$, $i < n$ exactly when $i k < n k$, as long as no product wraps. So `c` gets the same value. Removing the dead `i` is then a case of dead code elimination.

## Classic examples

**A product in a loop.** The parameters are `k` and `n`. The block `entry` is the only way into the loop and ends with `jump h`, so it serves as the preheader.

```
entry:
  i = 0
  s = 0
  jump h
h:
  c = i < n
  br c body done
body:
  x = i * k
  s = s + x
  i = i + 1
  jump h
done:
  ret s
```

`i` is defined in the loop only by `i = i + 1`, and `k` is a parameter that the loop does not change. The rewrite adds `t = i * k` and `d = 1 * k` to `entry`, adds `t = t + d` after `i = i + 1`, and turns `x = i * k` into `x = t`. After constant folding and copy propagation, `d` is `k`:

```
entry:
  i = 0
  s = 0
  t = i * k
  jump h
h:
  c = i < n
  br c body done
body:
  x = t
  s = s + x
  i = i + 1
  t = t + k
  jump h
done:
  ret s
```

For $k = 3$, $n = 4$ both return $0 + 3 + 6 + 9 = 18$. The multiply in the loop is gone.

**Test replacement.** Let the factor be the constant 4. `i` is now read only by `i = i + 1` and the test `i < n`. Since $4 > 0$, the test becomes `t < m` with `m = n * 4`, and `i` dies:

```
entry:
  s = 0
  t = 0
  m = n * 4
  jump h
h:
  c = t < m
  br c body done
body:
  s = s + t
  t = t + 4
  jump h
done:
  ret s
```

For $n = 4$ it returns $0 + 4 + 8 + 12 = 24$, as the loop with `x = i * 4` does. On 64-bit integers, `n * 4` wraps when $n \ge 2^{61}$, and the new test is wrong, so a compiler must know that this cannot happen, for example because $n$ bounds the index of an array.

**Array addresses.** The most common case in practice. In `for (i = 0; i < n; i++) s += a[i];` with 8-byte elements, the address of `a[i]` is `a + i * 8`. Strength reduction gives a pointer `q` that starts at `a` and moves by 8, and test replacement compares `q` with `a + n * 8`.

**A local rewrite.** `y = x * 8` becomes `y = x << 3`, and `y = x * 9` becomes `y = (x << 3) + x`. Both are identities for all integers, and also for wrapping integers.

## Variations

- **On SSA form.** [Operator strength reduction](/operator-strength-reduction/) by Cooper, Simpson and Vick finds the induction variables as strongly connected components of the SSA graph, reduces each candidate as it visits the components, and does the test replacement. It gets results equal to those of the earlier algorithm of Allen, Cocke and Kennedy with a simpler method.
- **Polynomials.** A product of two induction variables, such as `i * i`, is a polynomial in the iteration number. Its finite differences are again induction variables: $(i+1)^2 = i^2 + 2i + 1$. [Chains of recurrences](/chains-of-recurrences/) describe this and reduce a polynomial of degree $r$ to $r$ adds per iteration.
- **Division by invariants.** A division by a constant, or by a value that the loop does not change, can be replaced by a multiply by a precomputed inverse and a shift. The magic constant comes from Granlund and Montgomery, and signed division needs a fix for negative dividends.
- **With partial redundancy elimination.** Strength reduction can be done inside [SSAPRE](/ssapre/), which treats the product at each iteration as partly redundant with the product of the iteration before.
- **Induction variable elimination.** After the test replacement, a basic induction variable that is read only by its own updates is dead. Removing it saves a register and an add per iteration.

## Pitfalls

- **Signed division by a shift.** The toy IR, C and Java round integer division toward zero, but an arithmetic shift rounds down. For $x = -1$, `x / 8` is 0 while `x >> 3` is $-1$. The correct sequence adds 7 to negative dividends before the shift. In the same way `x % 8` is not `x & 7` for negative `x`: $-1 \bmod 8$ is $-1$ in these languages, but $-1 \mathbin{\&} 7$ is 7.
- **Wrapping in the test replacement.** `i < n` and `i * k < n * k` agree only if neither product wraps. A compiler that cannot rule out wrapping must keep the old test.
- **The sign of the factor.** For $k < 0$ the test turns around, and for $k = 0$ it says nothing about `i`. Test replacement with an unknown `k` needs a runtime test or must be skipped.
- **Floating point.** Replacing `x = i * h` with repeated `t = t + h` changes the rounding, and the error grows with the number of iterations. Compilers do not reduce floating-point products unless the programmer allows inexact math.
- **Rarely executed products.** If the product sits in a branch that rarely runs, the new add runs on every update of `i` and can cost more than it saves.
- **Pointers past the end.** A reduced pointer and the test bound `a + n * 8` may point past the end of an array. In C, forming a pointer more than one past the end is undefined, so the compiler that makes such pointers must make sure the target machine does not care.

## Exercises

1. In the first example, why is `t = i * k` in the preheader and not simply `t = 0`? *Answer.* The rewrite does not assume the start value of `i`. Here `i = 0` reaches the preheader, so constant folding turns `t = i * k` into `t = 0` afterward.
2. The loop holds `i = i + 2` in one branch and `i = i + 3` in the other. Can `x = i * k` be reduced? *Answer.* Yes. (C1) allows several updates with different invariant steps. Add `d2 = 2 * k` and `d3 = 3 * k` to the preheader, and the matching add after each update.
3. Why must `k` not be address-taken? *Answer.* A store through a pointer to `k`, or a call that gets such a pointer, could change `k` inside the loop without naming it. Then $t = i k$ would no longer hold.
4. Give the rewrite for `x = i + k`. *Answer.* `t = i + k` in the preheader, `t = t + c` after each `i = i + c`, and `x = t` in place of $I$. The invariant is $t = i + k$.
5. For which $n$ does the test-replaced loop of the second example give a different result from the original on 64-bit wrapping integers? *Answer.* When `n * 4` wraps, that is for $n \ge 2^{61}$ or $n < -2^{61}$. For large positive $n$, `m` becomes negative or small and the new loop stops too early.

## References
