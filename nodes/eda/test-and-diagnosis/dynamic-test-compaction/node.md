---
tag: 9KNJ7Z
kind: technique
slug: dynamic-test-compaction
name: Dynamic test compaction
aliases:
- Goel-Rosales compaction
area: eda/test-and-diagnosis
level: core
summary: After ATPG finds a test cube for one fault, it fills the unspecified inputs to detect more faults, so fewer patterns are generated.
prereqs: [automatic-test-pattern-generation, podem]
see_also: [static-test-compaction, fault-simulation, ternary-simulation, set-cover, n-detect-test, scan-design, fault-coverage, embedded-deterministic-test]
sources:
  - paper: "P. Goel and B. C. Rosales, Test generation and dynamic compaction of tests, Digest of Papers, IEEE Test Conference, 189 to 192, 1979"
    title: P. Goel and B. C. Rosales, Test generation and dynamic compaction of tests, Digest of Papers, IEEE Test Conference, 189 to 192, 1979
    locator: the dynamic compaction of tests during PODEM-based test generation, by targeting more faults with the inputs that the first test leaves unspecified
  - paper: doi:10.1145/288548.288615
    title: I. Hamzaoglu and J. H. Patel, Test set compaction algorithms for combinational circuits, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design, 1998
    locator: the MinTest system, which combines dynamic compaction with Redundant Vector Elimination and Essential Fault Reduction
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter on combinational test generation (test compaction, static and dynamic)
---

Dynamic test compaction makes a test generator produce fewer vectors by packing more faults into each one while it is being made. A generator such as [PODEM](/podem/) usually finds a test for its target fault with only a few inputs set; the others stay unspecified (X). Instead of filling those X positions at once, dynamic compaction keeps the set positions fixed and runs the generator again on a second fault, then a third, using only the positions that are still X. When no more faults fit, it fills the rest, [fault-simulates](/fault-simulation/) the vector and drops every fault it detects. Goel and Rosales introduced the method in 1979. It is called dynamic because it works during generation, in contrast with [static test compaction](/static-test-compaction/), which shrinks a finished test set. This page proves that every fault packed into a vector stays detected, and shows on a small circuit how the method reaches the minimum where plain generation does not.

## In plain words

A test generator writes a test for one fault at a time, and each test usually cares about only a few inputs. The other inputs are free. Plain generation fills them with anything, and hopes.

Dynamic compaction uses the free inputs on purpose. It keeps the inputs the first fault needs, then asks: can I also test a second fault with the inputs that are still free? If yes, it fixes a few more inputs. It goes on until no free inputs are left or no more faults fit. One test now does the work of several.

## When it applies

- Test generation for combinational logic, or for scan designs where the logic between scan cells is combinational.
- The generator returns **test cubes**: vectors over $\{0, 1, X\}$ whose every completion detects the target fault. PODEM, the [D-algorithm](/d-algorithm/) and [SAT-based ATPG](/sat-based-atpg/) all can.
- The generator accepts constraints: some inputs are fixed in advance, and it must find a test that agrees with them or report that none exists.
- The test set must be small, because tester time and tester memory grow with the number of vectors.

## The template

```pseudo id=main
DYNAMIC-COMPACT(C, F)
L1  T ← empty; R ← F
L2  while R is not empty
L3      f ← the first fault of R
L4      c ← a test cube of f from ATPG; if there is none, remove f from R and go to L2
L5      for each other fault g of R, while c has an X position
L6          if some completion of c may fail to detect g
L7              c' ← a test cube of g from ATPG, with the specified positions of c fixed
L8              if c' exists then c ← c'
L9      v ← c with every X filled
L10     remove from R every fault that v detects; append v to T
L11 return T
```

The fault $f$ at line L3 is the **primary target** and the faults $g$ at line L5 are **secondary targets**. The holes are the order of $R$, the choice of secondary targets, the limits on the effort per secondary target, and the fill at line L9. The check at line L6 is usually a three-valued simulation of $c$, which is safe by the monotonicity of [ternary simulation](/ternary-simulation/): if the simulation of $c$ already detects $g$, every completion does.

**Why every packed fault stays detected.** At line L7 the generator returns a cube $c'$ that agrees with $c$ on every specified position of $c$, so every completion of $c'$ is a completion of $c$. By induction over the secondary targets accepted at line L8, every completion of the final cube is a completion of each earlier cube. The cube for $f$ at line L4 was a test cube of $f$, and each accepted cube was a test cube of its target $g$. So every completion of the final cube, and in particular $v$ at line L9, detects $f$ and every accepted secondary target. Line L10 removes them all from $R$.

**Why it stops.** Each pass of the loop at line L2 removes at least the primary target $f$ from $R$: at line L4 if it has no test, or at line L10 because $v$ detects it. So the loop runs at most $|F|$ times and $T$ has at most $|F|$ vectors. If the generator is complete, a fault removed at line L4 is undetectable, a [redundant fault](/redundant-fault/), and $T$ detects every detectable fault of $F$. Tools stop the generator after a backtrack limit, and an aborted fault is then removed without a proof.

**What it does not give.** The result is not a minimum test set. Finding one is NP-hard, as proved on the [static test compaction](/static-test-compaction/) page, and the greedy packing here depends on the order of the faults. It is not even guaranteed to use fewer vectors than plain generation on every circuit, because the fills differ and luck plays a part. Measured results below show what it gains on toy circuits.

**Example.** Take two separate cones, $z = ab$ and $y = c + d$, with outputs $z$ and $y$. There are 6 lines and 12 stuck-at faults, in the order a/0, a/1, b/0, b/1, c/0, c/1, d/0, d/1, z/0, z/1, y/0, y/1. The generator returns the cube of a fault with only the needed positions set, and the fill is 0. Plain generation with fault dropping makes 5 vectors:

| target | cube | vector | faults it detects that are still in $R$ |
|---|---|---|---|
| a/0 | 11XX | 1100 | a/0, b/0, z/0, c/1, d/1, y/1 |
| a/1 | 01XX | 0100 | a/1, z/1 |
| b/1 | 10XX | 1000 | b/1 |
| c/0 | XX10 | 0010 | c/0, y/0 |
| d/0 | XX01 | 0001 | d/0 |

Dynamic compaction makes 3:

| primary | secondaries accepted | final cube | faults it detects that are still in $R$ |
|---|---|---|---|
| a/0 (11XX) | c/0 (XX10) | 1110 | a/0, b/0, c/0, z/0, y/0 |
| a/1 (01XX) | c/1 (XX00) | 0100 | a/1, c/1, d/1, z/1, y/1 |
| b/1 (10XX) | d/0 (XX01) | 1001 | b/1, d/0 |

In the first vector, a/1 and b/1 are rejected at line L7 because they need $a = 0$ or $b = 0$, and b/0 is skipped at line L6 because the cube 11XX already detects it. After c/0 the cube has no X, so the loop at line L5 stops. The faults a/0, a/1 and b/1 are pairwise independent (no vector detects two of them: their tests are 11XX, 01XX and 10XX), so every complete test set has at least 3 vectors, and 3 is the minimum.

**Cost.** Each vector costs one generator call for the primary target and up to $|R|$ calls for secondary targets, each of which can take exponential time in the worst case, as on the [ATPG](/automatic-test-pattern-generation/) page. In the worst case that is $O(|F|^2)$ generator calls instead of $O(|F|)$. Tools bound it by trying only a limited number of secondary targets per vector and a small backtrack limit for each, and by picking secondary targets that are likely to fit, for example faults whose cones do not overlap the inputs already set.

**Measured, not proved.** These numbers come from toy inputs, not from benchmark circuits. With `random.Random(3)`, 200 random circuits of 3 to 5 inputs and 3 to 8 gates, 6090 detectable stuck-at faults in a random order, and a brute-force generator (it takes the first detecting vector in input order, then turns each free position into X while every completion still detects the fault), plain generation with fault dropping and a 0 fill used 1222 vectors, dynamic compaction 970, and the exact minimum test sets 928. Dynamic compaction was above the minimum in 38 of the 200 circuits, and it never used more vectors than plain generation in this run, though that is not guaranteed.

## Classic examples

- **Goel and Rosales (1979).** Dynamic compaction inside a PODEM-based generator, where the unspecified inputs of each test are used for more faults.
- **MinTest.** Hamzaoglu and Patel (1998) combine dynamic compaction with Redundant Vector Elimination and Essential Fault Reduction to come close to estimated minimum test set sizes.
- **Production ATPG for scan.** Scan designs have thousands of inputs and each test cube sets only a small share of them, so dynamic compaction packs many faults into each vector. It is a standard part of production test generation.
- **With static compaction.** A dynamic pass makes the vectors, and a static pass such as reverse-order fault simulation removes those that later vectors made unnecessary.

## Variations

- **Secondary target choice.** Pick faults whose test is likely to agree with the current cube, such as faults in other output cones, or faults with few tests first, since they are the hardest to place later.
- **Maximal compaction.** Keep trying secondary targets until the cube has no X left, with higher effort per target. This gives fewer vectors and costs more time.
- **Leaving X for compression.** With test compression such as [embedded deterministic test](/embedded-deterministic-test/), each vector can only have a limited number of specified bits, so packing stops at that limit instead of at the last X.
- **Fill choices.** A random fill at line L9 detects more faults by chance. A fill that repeats the neighbouring value lowers switching during shift and test power, at the cost of chance detections.
- **N-detect packing.** For [N-detect tests](/n-detect-test/), a fault stays in $R$ until it has been detected $N$ times.

## Pitfalls

- **Order matters.** The same circuit gives very different vector counts for different primary and secondary orders. Do not read one run as a property of the method.
- **Wasted effort on hard secondary faults.** A secondary target that has no test agreeing with the cube can make the generator search a long time before it fails. Use a small backtrack limit for secondary targets.
- **Aborted is not redundant.** A fault removed at line L4 because the generator gave up is not proved undetectable. Report it separately from the faults the generator proved redundant.
- **Counting only targeted faults.** The vector also detects faults by chance through the fill. Always fault-simulate the filled vector at line L10, or some faults are targeted again for nothing.

## Exercises

1. In the example, run plain generation with a 1 fill instead of a 0 fill. Show that it makes 6 vectors, and list them.
2. Prove that if every fault of $F$ is detectable and every generator call is complete, dynamic compaction with any order returns a test set that detects all of $F$.
3. Give a circuit and a fault order for which dynamic compaction uses more vectors than plain generation with the same fill.

## References
