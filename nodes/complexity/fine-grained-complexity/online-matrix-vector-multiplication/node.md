---
tag: RH4M3N
kind: problem
slug: online-matrix-vector-multiplication
name: Online Matrix-Vector multiplication
aliases:
- OMv
area: complexity/fine-grained-complexity
level: advanced
summary: "Given an n-by-n Boolean matrix M, answer n vectors v one at a time with Mv before the next arrives. The naive cost is n^3; the best known saves a 2^(sqrt(log n)) factor."
prereqs: [matrix-vector-multiplication, boolean-matrix-multiplication, online-algorithm]
see_also: [omv-conjecture, dynamic-lower-bounds, boolean-matrix-multiplication, matrix-vector-multiplication, combinatorial-bmm-conjecture, four-russians-method, cell-probe-model, fine-grained-equivalence-class]
sources:
  - paper: arxiv:1511.06773
    title: "Monika Henzinger, Sebastian Krinninger, Danupon Nanongkai and Thatchaphol Saranurak, Unifying and strengthening hardness for dynamic problems via the online matrix-vector multiplication conjecture, STOC 2015, 21-30"
    locator: the introduction (the definition of OMv, the known algorithms and Conjecture 1.1), Section 1.2 (OMv and combinatorial BMM), Definition 2.6 and Lemmas 2.10 and 2.11 (OuMv and the reduction from OMv) of the arXiv version, which the page relies on
  - paper: arxiv:1605.01695
    title: "Kasper Green Larsen and R. Ryan Williams, Faster online matrix-vector multiplication, SODA 2017, 2182-2189"
    locator: the abstract (an algorithm with total time n^3/2^Omega(sqrt(log n)) and the cell probe upper bound)
  - paper: "Ryan Williams, Matrix-vector multiplication in sub-quadratic time (some preprocessing required), SODA 2007, 995-1001"
    locator: the main theorem (O(n^(2+e)) preprocessing and O(n^2/(e log^2 n)) time per vector), as cited by Henzinger et al.
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: the introduction (the hinted OMv variants are refuted; plain OMv is not affected); not yet refereed
---

Online Matrix-Vector multiplication, or OMv, gives an algorithm an $n \times n$ Boolean matrix $M$ and then $n$ Boolean vectors $v_1, \ldots, v_n$, one at a time. The algorithm must output the Boolean product $M v_i$ before it sees $v_{i+1}$. Multiplying each vector directly costs $O(n^2)$, so $O(n^3)$ in total. If all vectors were known in advance, one fast matrix product would do the whole job in $O(n^{\omega})$ time with $\omega < 2.372$. The online order is what makes the problem hard: the best known algorithm saves only a factor $2^{\Omega(\sqrt{\log n})}$ over $n^3$.

Henzinger, Krinninger, Nanongkai and Saranurak (STOC 2015) conjectured that no algorithm solves OMv in time $O(n^{3-\varepsilon})$, and showed that this one conjecture gives tight lower bounds for many dynamic problems. The conjecture is on [OMv conjecture](/omv-conjecture/) and the bounds are on [dynamic lower bounds](/dynamic-lower-bounds/). This page is about the problem.

## In plain words

You get a big fixed grid of yes and no marks. Then someone hands you a list of marks, one list at a time. For each list, you must say which rows of the grid share at least one marked spot with it, and you must answer before you get the next list.

Checking every row against every list is slow. If you could see all the lists at once, a clever method for multiplying grids would be much faster. But you get them one by one.

Experts believe that, under these rules, no method is much faster than checking. Many questions about graphs that change over time contain this problem, so it explains why those questions are hard.

## Definition

**OMv**

- Instance: an integer $n$ and an $n \times n$ Boolean matrix $M$; then $n$ Boolean column vectors $v_1, \ldots, v_n$, given one at a time.
- Question: for each $i$, output $M v_i$ over the Boolean semiring, so $(M v_i)_r = \bigvee_{c} (M_{rc} \wedge (v_i)_c)$, before $v_{i+1}$ is given.

**The model.** The [word RAM](/word-ram/) with words of $\Theta(\log n)$ bits. The cost is the total time over the preprocessing of $M$ and all $n$ rounds. Randomized algorithms with error probability at most $1/3$ are allowed in the conjecture of Henzinger et al., so lower bounds based on it also hold against them.

## Variants

- **OuMv.** Each round gives a pair of vectors $(u_i, v_i)$, and the answer is the single bit $u_i^{T} M v_i$. Henzinger et al. (Definition 2.6) also define $\gamma$-OuMv, with an $n_1 \times n_2$ matrix and $n_3$ rounds, where $n_1 = n_2^{\gamma}$. The case with one round is uMv. OuMv is easier to embed in graph problems, because one bit is one query.
- **Polynomial preprocessing.** The algorithm may spend any polynomial time on $M$ before the first vector. Henzinger et al. show that the conjecture still gives the same bounds in this setting (Theorem 2.7 of the arXiv version).
- **Offline.** All vectors are known in advance. This is [Boolean matrix multiplication](/boolean-matrix-multiplication/) with $V = [v_1 \cdots v_n]$, which takes $O(n^{\omega})$ time; see [matrix multiplication exponent](/matrix-multiplication-exponent/).
- **One vector.** Plain [matrix-vector multiplication](/matrix-vector-multiplication/), with or without preprocessing of $M$.
- **Other semirings.** Over the integers or over $(\min, +)$, the online problem is also studied, but the conjecture is stated for the Boolean semiring.

## Examples

**A small instance.** Let

$$M = \begin{pmatrix} 1 & 0 & 1 & 0 \\ 0 & 1 & 1 & 0 \\ 0 & 0 & 0 & 1 \\ 1 & 1 & 0 & 0 \end{pmatrix}.$$

For $v_1 = (1, 0, 0, 1)^T$, row 1 meets $v_1$ in column 1, row 2 meets it nowhere, row 3 in column 4 and row 4 in column 1, so $M v_1 = (1, 0, 1, 1)^T$. For $v_2 = (0, 1, 0, 0)^T$, only rows 2 and 4 have a 1 in column 2, so $M v_2 = (0, 1, 0, 1)^T$. For $v_3 = 0$, $M v_3 = 0$. Each answer must be given before the next vector is seen, so the algorithm cannot combine the three vectors into one matrix product.

**From OMv to OuMv by binary search.** To find $M v$ with OuMv queries, ask $u^{T} M v$ for $u$ the indicator of a set of rows. If the answer is 1, some row in the set has $(M v)_r = 1$, and halving the set finds one such row. Remove it and repeat until the answer is 0. Henzinger et al. (Lemma 2.10) show that this lists all $w$ such rows with $1 + O(w \log n)$ queries. For a random $8 \times 8$ matrix with rows (as bit strings) $00000110$, $00000001$, $00000100$, $01000000$, $00000110$, $00000000$, $00000001$, $00000000$ and $v$ with ones in columns 2 and 6, the product $M v$ has ones in rows 1, 3, 4 and 5. The search finds all four with 16 queries, within the bound $1 + w(1 + \log_2 n) = 17$ for $w = 4$ and $n = 8$.

## Known algorithms

- **Direct.** $O(n^2)$ per vector, $O(n^3)$ in total, deterministic.
- **Four Russians.** With $O(n^2)$ preprocessing, each product takes $O(n^2 / \log n)$ time, by tables of all products of blocks of $\Theta(\log n)$ columns; see [Four Russians method](/four-russians-method/). Total $O(n^3 / \log n)$.
- **Williams (SODA 2007).** With $O(n^{2+\varepsilon})$ preprocessing, each product takes $O(n^2 / (\varepsilon \log^2 n))$ time for any $0 < \varepsilon < 1/2$. Total $O(n^3 / \log^2 n)$. Henzinger et al. call this the best known in 2015.
- **Larsen and Williams (SODA 2017).** Total time $n^3 / 2^{\Omega(\sqrt{\log n})}$, randomized. In the [cell probe model](/cell-probe-model/), they give $O(n^{7/4} / \sqrt{w})$ time per vector with word size $w$.

None of these is $O(n^{3-\varepsilon})$. For example, $2^{\sqrt{\log_2 n}}$ is larger than $n^{0.01}$ until $\log_2 n = 10000$; at $\log_2 n = 64$ it is $256$ against about $1.56$. But for larger $n$ the polynomial factor wins.

## Bounds

- **Unconditional.** $\Omega(n^2)$ in total, to read $M$ and the vectors. No better bound is known on the word RAM. The cell probe algorithm of Larsen and Williams shows that cell probe lower bounds cannot prove the conjecture: the cell probe model allows $O(n^{7/4} / \sqrt{w})$ per vector.
- **Conditional.** No $O(n^{3-\varepsilon})$ algorithm, conditional on the [OMv conjecture](/omv-conjecture/). For combinatorial algorithms, the same bound follows from the [combinatorial BMM conjecture](/combinatorial-bmm-conjecture/), by the reduction below.
- **Status in 2026.** Alman and Vassilevska Williams (arXiv:2610.06783, not yet refereed) refute three hinted variants of the OMv conjecture of van den Brand, Nanongkai and Saranurak, but state that plain OMv is not affected.

## Reductions

- **From Boolean matrix multiplication to OMv.** Deterministic, $a(n) = b(n) = n^3$. Feed the columns of the second matrix as the vectors. So an $O(n^{3-\varepsilon})$ OMv algorithm gives an $O(n^{3-\varepsilon})$ algorithm for BMM. Henzinger et al. note the consequence: any lower bound proved from OMv can also be proved from the combinatorial BMM conjecture, but only for combinatorial algorithms.
- **Between OMv and OuMv.** From OuMv to OMv is direct: compute $M v$ and take the inner product with $u$. From OMv to OuMv, Henzinger et al. (Lemma 2.11) cut $M$ into blocks, give each block its own OuMv instance, and find the 1 entries of $M v$ block by block with the binary search above. Each 1 entry is found once, so the total number of queries stays small. Both are deterministic with $a(n) = b(n) = n^3$, so the two problems are equivalent; see [fine-grained equivalence class](/fine-grained-equivalence-class/).
- **From OuMv to dynamic problems.** Each round of OuMv becomes $O(n)$ updates and one query on a graph or data structure built from $M$. This gives the bounds on [dynamic lower bounds](/dynamic-lower-bounds/), for example for [dynamic reachability](/dynamic-reachability/).

## Applications

- **Dynamic graph algorithms.** OMv is the base problem for tight conditional lower bounds on dynamic reachability, shortest paths, subgraph connectivity, decremental shortest paths and many other problems. See [dynamic lower bounds](/dynamic-lower-bounds/).
- **Data structures with preprocessing.** Matrix-vector products with a fixed matrix occur in graph queries, in databases and in iterative methods. OMv bounds how much any preprocessing of the matrix can help in the worst case.
- **Fine-grained complexity.** OMv and SETH together were enough, in 2015, to explain all known polynomial lower bounds for dynamic problems with polynomial preprocessing.

## References
