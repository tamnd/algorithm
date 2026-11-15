---
tag: 9QN3G8
kind: theorem
slug: loop-transformation-legality
name: Legality of loop reordering
aliases:
- lexicographically positive dependence theorem
area: compilers-and-program-analysis/loop-transformations
level: core
summary: A reordering of loop iterations keeps the meaning if every dependence distance vector remains lexicographically positive after it.
prereqs: [data-dependence, dependence-distance-vector, lexicographic-order]
see_also: [loop-carried-dependence, dependence-direction-vector, unimodular-transformations, loop-interchange, loop-skewing, loop-tiling, doall-loop, lamport-hyperplane-method]
sources:
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 2 (reordering transformations, Theorem 2.2, the fundamental theorem of dependence, and the direction vector condition for loop interchange)
  - paper: "Michael E. Wolf and Monica S. Lam, A loop transformation theory and an algorithm to maximize parallelism, IEEE Transactions on Parallel and Distributed Systems 2(4), 1991"
    locator: the legality condition for unimodular transformations on distance and direction vectors, and fully permutable loop nests
  - paper: "Leslie Lamport, The parallel execution of DO loops, Communications of the ACM 17(2), 1974"
    locator: the hyperplane method, which reorders the iterations of a nest by a linear map that keeps all dependences
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Chapter 11 (the legality of affine transforms and of blocking, and fully permutable loops)
  - paper: "Arthur J. Bernstein, Analysis of programs for parallel processing, IEEE Transactions on Electronic Computers EC-15(5), 1966"
    locator: the conditions on read and write sets under which two program parts can run in either order or in parallel
---

## Statement

A program $P$ runs a finite set $I$ of *statement instances* in a total order $<_P$ (see [data dependence](/data-dependence/)). Assume:

- each instance $x$ reads a fixed set of memory locations and writes a fixed set, which do not depend on the order of the run;
- the values that $x$ writes are a function of the values that $x$ reads.

A pair $(x, y)$ with $x <_P y$ is a **dependence** if $x$ and $y$ access a common location and at least one of them writes it. It is a flow, anti or output dependence when the write is in $x$ only, in $y$ only, or in both. A **reordering** of $P$ is a program $P'$ that runs the same instances in another total order $<_{P'}$.

**Theorem 1 (reordering).** If $x <_{P'} y$ for every dependence $(x, y)$ of $P$, then from every initial memory state, every instance reads the same values in $P'$ as in $P$, and $P'$ ends in the same memory state as $P$.

Now take a perfect loop nest of depth $k$ with iteration domain $D \subseteq \mathbb{Z}^k$. The body runs once per iteration vector in lexicographic order $\prec$, and the statements of one iteration run in the order of the text. A dependence from $S(\vec{i})$ to $T(\vec{j})$ has the [distance vector](/dependence-distance-vector/) $\vec{d} = \vec{j} - \vec{i}$, and $\vec{d} \succeq \vec{0}$. A zero distance means a loop-independent dependence inside one iteration; a nonzero one is [carried](/loop-carried-dependence/) by the loop of its first nonzero entry.

**Theorem 2 (unimodular transformation).** Let $T$ be a $k \times k$ integer matrix with $\det T = \pm 1$. Let $P'$ run the iteration $\vec{i}$ at the new iteration vector $T\vec{i}$: the new nest scans $T(D)$ in lexicographic order and runs the unchanged body at $\vec{i} = T^{-1}\vec{y}$ for each new point $\vec{y}$. If $T\vec{d} \succ \vec{0}$ for every nonzero distance vector $\vec{d}$ of a dependence of the nest, then $P'$ is a reordering of $P$ with the same meaning, in the sense of Theorem 1.

With direction vectors, Theorem 2 needs $T\vec{d} \succ \vec{0}$ for every distance $\vec{d}$ that the [direction vector](/dependence-direction-vector/) allows. This page uses Wolfe's notation: the entry $<$ at level $l$ means $i_l < j_l$, that is $d_l > 0$; $=$ means $d_l = 0$; $>$ means $d_l < 0$; and $*$ means any. A direction vector is lexicographically positive if its first entry that is not $=$ is $<$.

## In plain words

A compiler may run the parts of a program in another order, as long as it keeps the order of every pair of parts that touch the same memory and where at least one of them writes. Then every read still sees the value from the same write, so every part computes the same thing, and the last write to each location is still the same. For loops, the order of two iterations is given by the difference of their loop counters. A change of the loops keeps the order of a dependent pair exactly when that difference, after the change, still points forward: its first nonzero entry is positive. So a compiler checks each dependence once, and if all of them still point forward, the new loops compute the same result.

## Proof

### Proof of Theorem 1

For a location $\ell$ and an instance $x$ that reads $\ell$, let $w_P(x, \ell)$ be the last instance before $x$ in $<_P$ that writes $\ell$, or "initial" if there is none. Define $w_{P'}(x, \ell)$ in the same way for $<_{P'}$. The value that $x$ reads from $\ell$ is the value written by $w(x, \ell)$, or the initial value of $\ell$.

**Lemma 1.** If the dependences are kept, then $w_{P'}(x, \ell) = w_P(x, \ell)$ for every read.

*Proof.* Suppose first that $w = w_P(x, \ell)$ is an instance. The pair $(w, x)$ is a flow dependence, so $w <_{P'} x$. Let $v \ne w$ be any other writer of $\ell$ with $v <_{P'} x$; we show $v <_{P'} w$. In $<_P$, the instance $v$ is not between $w$ and $x$, because $w$ is the last writer before $x$. If $v <_P w$, then $(v, w)$ is an output dependence, so $v <_{P'} w$. If $x <_P v$, then $(x, v)$ is an anti dependence, so $x <_{P'} v$, against the choice of $v$. So every writer of $\ell$ before $x$ in $P'$ comes before $w$, and $w_{P'}(x, \ell) = w$.

If $w_P(x, \ell)$ is "initial", then every writer $v$ of $\ell$ has $x <_P v$, so $(x, v)$ is an anti dependence and $x <_{P'} v$. No writer comes before $x$ in $P'$, so $w_{P'}(x, \ell)$ is "initial" too. $\square$

**Proof of the theorem.** Use induction on the position of $x$ in $<_{P'}$. Assume that every instance before $x$ in $<_{P'}$ reads the same values in $P'$ as in $P$; then, by the second assumption, it also writes the same values. For each location $\ell$ that $x$ reads, Lemma 1 gives the same writer $w$ in both runs (or the initial value), and $w <_{P'} x$, so $w$ wrote the same value in both runs. So $x$ reads the same values. This proves the claim for all instances.

For the final state, take a location $\ell$. Any two writers of $\ell$ form an output dependence, so they run in the same order in $P$ and $P'$, and the last writer of $\ell$ is the same instance in both runs. It writes the same value, by the first part. A location that no instance writes keeps its initial value in both runs. $\square$

### Proof of Theorem 2

**The new nest runs the same instances.** Since $\det T = \pm 1$, the inverse $T^{-1} = \operatorname{adj}(T) / \det T$ is an integer matrix (see [unimodular matrix](/unimodular-matrix/)). So $\vec{i} \mapsto T\vec{i}$ maps $\mathbb{Z}^k$ onto $\mathbb{Z}^k$ one to one, and it maps $D$ one to one onto $T(D)$. Each new point $\vec{y} \in T(D)$ runs the body at the integer point $T^{-1}\vec{y} \in D$, and each $\vec{i} \in D$ is reached from exactly one $\vec{y}$. So $P'$ runs each instance $S(\vec{i})$ exactly once: it is a reordering of $P$.

**The new order.** In $P'$, the instance $S(\vec{i})$ runs before $T(\vec{j})$ if $T\vec{i} \prec T\vec{j}$, or if $T\vec{i} = T\vec{j}$ (then $\vec{i} = \vec{j}$) and $S$ comes before $T$ in the body. Since $T$ is linear, $T\vec{i} \prec T\vec{j}$ holds exactly when $T(\vec{j} - \vec{i}) \succ \vec{0}$.

**The dependences are kept.** Take a dependence from $S(\vec{i})$ to $T(\vec{j})$ with distance $\vec{d}$.

- If $\vec{d} = \vec{0}$, both instances are in one iteration, with $S$ before $T$ in the body (or $S = T$ with the read before the write of one statement run, which is not changed). The body is unchanged, so their order is kept.
- If $\vec{d} \ne \vec{0}$, then $T\vec{d} \succ \vec{0}$ by the hypothesis, so $S(\vec{i})$ runs before $T(\vec{j})$ in $P'$.

So all dependences are kept, and Theorem 1 applies. $\square$

The proof does not use $\det T = \pm 1$ for the order, only for the claim that the new nest is easy to write: with $\det T = \pm 1$, the image $T(D)$ has no holes, and the new loops have unit steps. For any one to one map of the iterations, Theorem 1 gives the same condition: the map must keep the order of each dependent pair.

## Consequences

### Worked example

The nest `for i: for j: A[i][j] = f(A[i-1][j+1])` on a $4 \times 4$ domain has one flow dependence with distance $\vec{d} = (1, -1)$, direction $(<, >)$.

| transformation | $T$ | $T\vec{d}$ | legal? |
|---|---|---|---|
| interchange | $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ | $(-1, 1)$ | no |
| skew $j$ by $i$ | $\begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$ | $(1, 0)$ | yes |
| skew, then interchange | $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$ | $(0, 1)$ | yes |

A run with symbolic values (each $A[i][j]$ a term) confirms it: the interchanged nest computes different terms, and the two skewed nests compute the same terms as the original. The last one runs the anti-diagonals $t = i + j$ one after the other, and inside each anti-diagonal the inner loop carries no dependence, so its iterations can run in parallel, as in the [hyperplane method](/lamport-hyperplane-method/).

### Parallel loops

The loop at level $l$ can run its iterations in any order, with the outer loops fixed, if no dependence is carried at level $l$. Proof: such a run keeps the order of the outer loops, so it keeps every dependence carried at a level below $l$. A dependence carried at a level above $l$, or loop-independent, has $d_l = 0$, so both instances are in one iteration of level $l$ and their order inside it is unchanged. Theorem 1 gives the same result for each order of the level-$l$ iterations, which is the condition for a [DOALL loop](/doall-loop/). Allen and Kennedy state a general form of this as their Theorem 2.4.

### Permutation and reversal

- **[Loop interchange](/loop-interchange/)** and any permutation of the loops is legal if each permuted direction vector is lexicographically positive. A dependence with direction $(<, >)$ blocks the interchange of the two loops, and $(<, <)$ or $(<, =)$ does not.
- **Reversal** of the loop at level $l$ is the unimodular matrix that negates entry $l$. It is legal if no dependence is carried at level $l$: such a dependence has $d_l > 0$ and earlier entries 0, so its new vector has $-d_l < 0$ at its first nonzero entry.

### Fully permutable bands and tiling

Call the loops at levels $p, \dots, q$ **fully permutable** if every dependence that is not carried outside this band has $d_l \ge 0$ for $p \le l \le q$. Then every permutation of the band is legal. A permutation of the band does not change the entries before or after the band. A dependence carried in the band stays nonnegative and nonzero on the band, so it stays lexicographically positive; any other dependence keeps its first nonzero entry.

[Loop tiling](/loop-tiling/) of a fully permutable band is also legal, although it is not linear. Take the band to be the whole nest, for short. With tile size $B$, tiling runs the iteration $\vec{i}$ at the new vector $(\lfloor \vec{i}/B \rfloor, \vec{i})$, compared lexicographically. For a dependence with $\vec{d} \ge \vec{0}$ entrywise, $\lfloor \vec{j}/B \rfloor - \lfloor \vec{i}/B \rfloor$ is also $\ge \vec{0}$ entrywise. If it is nonzero, it is lexicographically positive; if it is zero, the two instances are in one tile and the second part, $\vec{d}$, is lexicographically positive. So the dependence is kept, and Theorem 1 applies. The nest of the worked example has $d_2 = -1$ and cannot be tiled as it is: a run with $2 \times 2$ tiles changes the result. After the skew $\begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$ the distance is $(1, 0) \ge \vec{0}$, and the tiled skewed nest computes the original result. This is why [loop skewing](/loop-skewing/) comes before tiling in many compilers.

### Zero distances

A zero distance vector stands for a loop-independent dependence. $T\vec{0} = \vec{0}$ for every $T$, so Theorem 2 cannot use $T\vec{d} \succ \vec{0}$ for it, and does not need to: the body is not changed, so the order inside an iteration stays. A transformation that also changes the body, such as loop distribution or statement reordering, must keep the loop-independent dependences by other means.

## Tightness

**The condition is sufficient, not necessary.** Three examples show reorderings that break a dependence and still keep the meaning.

- **Overwritten values.** `X = 1; X = 2; X = 3` has an output dependence from the first write to the second. Swapping them gives the same final state, because the third write hides both, and no read lies between them.
- **Reductions.** `for i: s = s + A[i]` has flow, anti and output dependences on `s` between every pair of iterations. Running the loop backwards breaks all of them. On integers the sum is the same, for example $23$ for $A = (3, 1, 4, 1, 5, 9)$ in both orders, because integer addition is associative and commutative. On floating-point numbers it can differ: $(0.1 + 10^{16}) - 10^{16} = 0$, while $(-10^{16} + 10^{16}) + 0.1 = 0.1$. Compilers handle reductions as a separate case.
- **Equal values.** If both statements of a dependence write the same constant, any order gives the same state.

Each example uses the meaning of the operations or the fact that a value is never read. The theorem uses neither: it holds for every function in the second assumption. So it is the best rule that looks only at which locations each instance reads and writes, not at what the operations do.

**Memory-based dependences are more than needed.** The proof of Lemma 1 only needs three kinds of pairs: a write and a read that sees its value, a read and the next write of the location, and two consecutive writes of the location. The other dependences follow from these by transitivity. Value-based dependence analysis keeps only the pairs from a write to the reads that see its value (see [array privatization](/array-privatization/)); after privatization or renaming of storage, fewer orders need to be kept.

**Unimodular matrices are not all transformations.** Theorem 2 covers the reorderings by one linear map of the whole nest. Tiling, as shown above, and the affine schedules of the [polyhedral model](/polyhedral-model/), which give each statement its own map, need Theorem 1 directly.

**Direction vectors lose precision.** A direction vector stands for a set of distances, and Theorem 2 needs $T\vec{d} \succ \vec{0}$ for all of them. A test with $(<, *)$ must assume that $d_2$ can be negative, so it can reject a transformation that the real distances allow.

## History

Bernstein (1966) gave conditions on the read and write sets of two program parts under which they can run in either order or in parallel. Lamport (1974) reordered the iterations of DO loops by linear maps that keep all dependences, the hyperplane method. The theorem that a reordering transformation keeps the meaning of a program if it keeps every dependence is Theorem 2.2 of Allen and Kennedy, who call it the fundamental theorem of dependence, with a proof by the order of the instances. Banerjee, and Wolf and Lam (1991), stated the condition for unimodular transformations, $T\vec{d} \succ \vec{0}$, which unifies interchange, reversal and skewing, and Wolf and Lam used fully permutable nests for tiling. The dragon book states the same conditions for affine transforms and blocking.

## References
