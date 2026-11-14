---
tag: DV4CEE
kind: technique
slug: static-test-compaction
name: Static test compaction
aliases:
- reverse-order fault simulation
- test set compaction
area: eda/test-and-diagnosis
level: core
summary: Shrinks a finished test set by merging compatible cubes and by dropping patterns that reverse-order fault simulation or set covering shows are not needed.
prereqs: [fault-simulation, automatic-test-pattern-generation]
see_also: [set-cover, greedy-set-cover, dynamic-test-compaction, n-detect-test, fault-coverage, np-hard, ppsfp, scan-design]
sources:
  - paper: "B. Krishnamurthy and S. B. Akers, On the complexity of estimating the size of a test set, IEEE Transactions on Computers C-33(8), 750 to 753, 1984"
    title: B. Krishnamurthy and S. B. Akers, On the complexity of estimating the size of a test set, IEEE Transactions on Computers C-33(8), 750 to 753, 1984
    locator: the proof that finding the size of a minimum test set of a combinational circuit is NP-hard
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum, 85 to 103, 1972
    locator: set covering in the list of NP-complete problems
  - paper: "P. Goel and B. C. Rosales, Test generation and dynamic compaction of tests, Digest of Papers, IEEE Test Conference, 189 to 192, 1979"
    title: P. Goel and B. C. Rosales, Test generation and dynamic compaction of tests, Digest of Papers, IEEE Test Conference, 189 to 192, 1979
    locator: test cubes with unspecified inputs and their compaction during generation, the counterpart of the compaction after generation on this page
  - paper: doi:10.1145/288548.288615
    title: I. Hamzaoglu and J. H. Patel, Test set compaction algorithms for combinational circuits, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design, 1998
    locator: Redundant Vector Elimination, Essential Fault Reduction, and the estimate of the minimum test set size
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter on combinational test generation (test compaction, static and dynamic)
---

Static test compaction takes a test set that is already finished and makes it smaller without losing fault coverage. A test set from [automatic test pattern generation](/automatic-test-pattern-generation/) usually holds one test cube per targeted fault, with many inputs left unspecified (X). Two cheap steps remove most of the waste. First, merge cubes that do not conflict in any specified position into one cube. Second, fill the remaining X positions and [fault-simulate](/fault-simulation/) the vectors from the last one to the first, keeping a vector only when it detects a fault that the vectors already kept do not. Test time on the tester and tester memory grow with the number of vectors, so each vector removed saves money on every chip. This page proves that the second step never loses a fault, that the first step never loses a fault that a cube was made for, and that finding a minimum test set is NP-hard, as hard as [set cover](/set-cover/).

## In plain words

A test generator works one fault at a time and writes down each test as soon as it finds it. Later tests often happen to catch the faults that earlier tests were made for, so some early tests do nothing new. Also, a test usually fixes only a few inputs and does not care about the others, so two tests that fix different inputs can be joined into one.

Static compaction cleans up after the generator. It joins tests that fit together, then walks the list from the end and throws away every test that catches nothing new. Walking from the end works well because the last tests were made for the hardest faults, and such tests tend to catch many easy faults along the way.

## When it applies

- The circuit under test is combinational, or a full [scan design](/scan-design/) makes it so. A test is one input vector.
- The fault list $F$ is fixed, for example all single stuck-at faults, and a fault simulator can tell which faults a vector detects. With [PPSFP](/ppsfp/) this is fast even for large circuits.
- The test set is given as a list $T$ of test cubes, vectors over $\{0, 1, X\}$. A **test cube** of a fault $f$ is a cube whose every completion (every way to replace each X by 0 or 1) detects $f$.
- The goal is fewer vectors with the same coverage. Compaction that merges tests during generation is [dynamic test compaction](/dynamic-test-compaction/), and the two are used together.

## The template

Two cubes are **compatible** when no position holds 0 in one and 1 in the other. Their **intersection** $u \cap t$ takes, at each position, the specified value of either cube, and X where both have X. Its completions are exactly the vectors that are completions of both cubes.

```pseudo id=main
STATIC-COMPACT(T, F)
L1  C ← empty list of cubes
L2  for each cube t in T, in order
L3      if some cube u in C is compatible with t then u ← u ∩ t
L4      else append t to C
L5  V ← the cubes of C with every X filled
L6  R ← F; K ← empty
L7  for each vector v of V, last first
L8      D ← the faults of R that v detects
L9      if D is not empty then add v to K; R ← R \ D
L10 return K
```

Lines L1 to L4 merge cubes by first fit: each cube joins the first merged cube it is compatible with. Line L5 fills the X positions, with a constant or with random values. Lines L6 to L10 are the reverse-order pass: one fault simulation with fault dropping over the vectors in reverse order. The holes are the rule that picks $u$ at line L3, the fill at line L5 and the order of $V$ at line L7.

**Why the reverse-order pass never loses a fault.** Let $f$ be a fault of $F$ that some vector of $V$ detects, and let $v_j$ be the last vector of $V$ that detects it. Line L7 handles $v_j$ after all the vectors behind it. A fault leaves $R$ only at line L9, and only when the vector being handled detects it. No vector after $v_j$ detects $f$, so $f$ is still in $R$ when line L8 handles $v_j$. So $f \in D$, $D$ is not empty, and line L9 keeps $v_j$. So $K$ detects every fault of $F$ that $V$ detects, and $K$ is a subset of $V$. The same argument works with any fault simulator that answers correctly, and with any order of $V$. The order changes only which vectors are kept.

**Why merging never loses a target fault.** Say $t$ is a test cube of $f$, and $t$ ends up inside the merged cube $u$. Each intersection at line L3 keeps the specified values of both cubes, so by induction on the cubes that join $u$, every specified position of $t$ holds the same value in the final $u$. Any filling of $u$ at line L5 then agrees with $t$ on every specified position, so it is a completion of $t$, and it detects $f$. If every fault of $F$ has a test cube in $T$, the vectors $V$ detect all of $F$, and by the step before so does $K$. The proof needs the cube to be a test cube for every completion. A fault that a filled cube detects only through the values chosen for its X positions is not protected, as the pitfalls show.

**Why a minimum test set is hard to find.** The decision problem is: given a circuit, a fault list $F$ and a number $k$, is there a set of at most $k$ vectors that detects every fault of $F$? It is in NP, since the $k$ vectors are a certificate that fault simulation checks in polynomial time, and one may take $k \le |F|$. It is NP-hard by a reduction from set cover, which Karp (1972) proved NP-complete. Take sets $S_0, \ldots, S_{m-1}$, $m \ge 2$, over a universe $U$. Build a circuit with inputs $x_0, \ldots, x_{m-1}$:

- a NAND gate $n_{ij}$ of $x_i$ and $x_j$ for each pair $i < j$, and $a = $ the AND of all $n_{ij}$, so $a = 1$ exactly when at most one input is 1;
- for each element $e$, $y_e = $ the OR of the $x_i$ with $e \in S_i$, and an output $z_e = y_e$ AND $a$;
- the fault list $F = \{\, y_e \text{ stuck-at } 0 : e \in U \,\}$.

A vector with no 1 makes every good $y_e$ equal to 0, the faulty value, so it detects nothing. A vector with two or more 1s makes $a = 0$, so every $z_e$ is 0 in both circuits, and it detects nothing either. The fault on $y_e$ does not reach $a$. The vector with a single 1 at $x_i$ makes $a = 1$ and $z_e = y_e$, so it detects $y_e$/0 exactly when $e \in S_i$. So the useful vectors are the $m$ unit vectors, unit vector $i$ detects the faults of the elements of $S_i$, and test sets of size $k$ correspond to set covers of size $k$. The circuit has $O(m^2 + \sum |S_i|)$ gates, so the reduction is polynomial, and it keeps sizes exactly. So any approximation ratio for minimum test sets would give the same ratio for set cover, and the limits on approximating set cover hold here too.

Krishnamurthy and Akers (1984) proved that finding the size of a minimum test set is NP-hard. This page does not repeat their proof; the reduction above is a simple one for a given fault list, in the same spirit. Note that the hardness here does not come from test generation: in this circuit every fault has an easy test, and only the choice among them is hard.

**The set cover view.** Fault-simulate every vector of $V$ against $F$ without fault dropping. The result is the detection matrix: vector $v$ detects the set $S_v \subseteq F$. A smallest subset of $V$ with the same coverage is a minimum set cover of $\bigcup_v S_v$ by the sets $S_v$. This is exactly the set cover problem, with the vectors as sets and the faults as elements. [Greedy set cover](/greedy-set-cover/) picks the vector that detects the most faults not yet detected, and it uses at most $H_d$ times the minimum number of vectors, where $d$ is the largest number of faults one vector detects and $H_d \le \ln d + 1$. The reverse-order pass gives no such bound. It is cheaper, because it needs only one simulation with fault dropping, not the full matrix.

**A lower bound.** Call faults **independent** when no vector detects two of them. If $F$ contains $r$ pairwise independent faults, every complete test set has at least $r$ vectors, because each vector detects at most one of them. This bound is how one can show that a compacted set is a minimum without searching all subsets.

**Example.** Take $g = ab$, $h = c + d$ and $z = \mathrm{NAND}(g, h)$ with inputs $abcd$. It has 7 lines and 14 single stuck-at faults, all detectable. Some faults have one test only: $c$/0 needs 1110, $d$/0 needs 1101, and $c$/1, $d$/1 and $h$/1 need 1100. The tests of $a$/1 are 01X1 and 0110, and those of $b$/1 are 10X1 and 1010. Say a test generator, with no fault dropping, made these 8 cubes in this order:

| cube | made for | first-fit merged cube after this cube |
|---|---|---|
| XX00 | $z$/0 | 1: XX00 |
| 11X1 | $a$/0 | 2: 11X1 |
| 01X1 | $a$/1 | 3: 01X1 |
| 10X1 | $b$/1 | 4: 10X1 |
| 1110 | $c$/0 | 5: 1110 |
| 1100 | $c$/1 | 1: 1100 |
| 1101 | $d$/0 | 2: 1101 |
| X0X1 | $g$/1 | 4: 10X1 |

Merging leaves 5 cubes: 1100, 1101, 01X1, 10X1 and 1110. Filling with 0 gives 1100, 1101, 0101, 1001 and 1110. The reverse-order pass keeps all 5: 1110 detects $a$/0, $b$/0, $c$/0, $g$/0, $h$/0 and $z$/1; 1001 adds $b$/1, $g$/1 and $z$/0; 0101 adds $a$/1; 1101 adds $d$/0; 1100 adds $c$/1, $d$/1 and $h$/1. The faults $a$/1, $b$/1, $c$/0, $d$/0 and $h$/1 are pairwise independent, so 5 is the minimum, and this result is optimal. The reverse-order pass alone, on the 8 cubes filled with 0, keeps 6 vectors: it drops 1101 (the filling of 11X1), whose faults the later 1101 detects, and 0000, whose only fault $z$/0 the last vector 0001 detects.

**Cost.** Merging by first fit takes $O(|T|^2 n)$ time for $n$ inputs, or less with an index on the specified positions. The reverse-order pass is one fault simulation with fault dropping, which is the main cost on large circuits. Building the detection matrix for set covering needs a simulation without dropping, which costs more, and the greedy cover then takes time about linear in the size of the matrix with a bucket queue.

**Tests.** The implementation is checked against brute force on random circuits of 2 to 4 inputs and up to 7 gates, with fixed seeds. The reverse-order pass keeps exactly the coverage of its input and keeps a vector exactly when it detects a fault that no later vector detects. Merged and filled cubes detect every fault that some cube of the input is a test cube for. The result of the whole method is never smaller than the minimum test set found by trying all subsets of the input vectors, and the greedy cover is within $H_d$ of that minimum. On random set systems with up to 5 sets and 5 elements, the minimum test set of the reduction circuit has the size of the minimum set cover found by enumeration. The example above and the loss example below are checked as given.

**Measured, not proved.** These numbers come from toy inputs, not from benchmark circuits. With `random.Random(7)`, 200 random circuits of 3 or 4 inputs and 3 to 7 gates, and one test cube per detectable fault (5073 cubes in total, each made by turning positions of a random detecting vector into X while it stays a test cube), merging left 853 cubes, and the reverse-order pass then left 825 vectors. The reverse-order pass alone, on the 5073 filled cubes, left 1030. Greedy set cover over all input vectors used 822, and the exact minimum is 804. The compacted set was larger than the minimum in 19 of the 200 circuits, the greedy cover in 18, and the reverse-order pass alone in 136.

## Classic examples

- **Compaction after ATPG.** Every production test flow for scan designs runs a pass like lines L6 to L10 after test generation, often several times with different orders.
- **Redundant Vector Elimination.** Hamzaoglu and Patel (1998) drop vectors whose faults are all detected by other vectors, and reduce the faults that only one vector detects, which they call essential faults, to bring the test set close to their estimate of the minimum size.
- **Set covering with the detection matrix.** When the matrix is affordable, greedy set covering or an integer linear program on it gives smaller sets than the reverse-order pass.
- **N-detect test sets.** An [N-detect test](/n-detect-test/) set must detect each fault $N$ times. Compaction then becomes set multicover, and the reverse-order pass keeps a vector while some fault still needs a detection.

## Variations

- **Several orders.** Repeat the reverse-order pass with the vectors sorted in other orders, for example by the number of faults each detects or at random. Each pass is safe, so the best result can be kept.
- **Forward then reverse.** A pass in the original order with fault dropping, then a pass in reverse, removes vectors whose faults the earlier and later vectors share.
- **Merging with a fault check.** Instead of merging any compatible cubes, merge only when the result still detects the faults of both cubes, or fault-simulate after merging and keep the lost faults as new targets.
- **Better merge order.** First fit depends on the cube order. Merging is a coloring problem on the graph whose edges join incompatible cubes, so graph coloring heuristics can be used, and the minimum number of merged cubes is itself NP-hard to find.
- **X filling for compression.** With test compression, leave the X positions open for the decompressor rather than filling them at line L5.

## Pitfalls

- **Merging loses chance detections.** After the fill, a cube can detect faults it was not made for, and a generator with fault dropping then skips those faults. Merging changes the fill, and those faults can be lost. In the circuit $g = \lnot a$, $h = \mathrm{NAND}(b, g)$ with outputs $h$ and $c$, the cubes 11X, 01X and XX1 fill to 110, 010 and 001, and 001 detects $b$/1. First fit merges them into 111 and 01X, which fill to 111 and 010, and neither detects $b$/1, whose only tests are 00X. Measured with `random.Random(7)` on 200 random circuits of 3 or 4 inputs and 3 to 7 gates, with cubes made as a generator with fault dropping makes them, merging lost 472 faults in 111 circuits. Always fault-simulate after merging.
- **Reverse order is not minimal.** The pass keeps a vector when it detects a fault that the later kept vectors miss, but an earlier vector may detect that fault too. The result can still hold vectors that could be removed, and it can be far from the minimum.
- **Keeping coverage of the wrong fault list.** Compaction keeps the faults it is told about. A test set compacted for stuck-at faults can lose detections of bridges, delays or other unmodelled defects that the extra vectors caught by chance. This is one reason for [N-detect tests](/n-detect-test/).
- **Fill and compression.** A fill that is good for compaction (random values catch more faults by chance) is bad for test power and for compression, which want long runs of equal values.

## Exercises

1. In the example, the reverse-order pass on the 8 filled cubes keeps 6 vectors. Find an order of the same 8 vectors for which the pass keeps 5.
2. Prove that the minimum number of merged cubes from a list of cubes equals the chromatic number of the graph whose vertices are the cubes and whose edges join incompatible cubes.
3. Change the reduction so that the fault list is all single stuck-at faults of the circuit. Which faults must you remove or make easy so that the minimum test set still equals the minimum set cover?

## References
