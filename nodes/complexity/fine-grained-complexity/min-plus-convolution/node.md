---
tag: QB5TFW
kind: problem
slug: min-plus-convolution
name: Min-plus convolution
aliases:
- (min,+) convolution
- min-plus product of sequences
area: complexity/fine-grained-complexity
level: advanced
summary: "Given integer sequences a and b, compute c[k] = min over i+j=k of a[i]+b[j]. It is equivalent to knapsack variants; 2026 preprints make it truly subquadratic."
prereqs: [convolution, fine-grained-reduction]
see_also: [min-plus-matrix-multiplication, convolution-3sum, 3sum, apsp-conjecture, knapsack-problem, unbounded-knapsack, fine-grained-equivalence-class, convolution]
sources:
  - paper: doi:10.1145/3293465
    title: "Marek Cygan, Marcin Mucha, Karol Węgrzycki and Michał Włodarczyk, On problems equivalent to (min,+)-convolution, ACM Transactions on Algorithms 15(1), 2019, article 14 (conference version in ICALP 2017, LIPIcs 80, 22:1-22:15; arXiv:1702.07669)"
    locator: Conjecture 1, Theorem 2 and Figure 2 (the equivalence class), Figure 1 (relations to 3SUM, APSP and SETH), Section 2.2 (known algorithms) and Appendix A, Theorem 25; the locators are from the arXiv version, which the page relies on
  - paper: doi:10.4230/LIPIcs.ICALP.2017.21
    title: "Marvin Künnemann, Ramamohan Paturi and Stefan Schneider, On the fine-grained complexity of one-dimensional dynamic programming, ICALP 2017, LIPIcs 80, 21:1-21:15"
    locator: the results on knapsack and min-plus convolution, found at the same time as those of Cygan et al.
  - paper: doi:10.1007/s00453-012-9734-3
    title: "David Bremner, Timothy M. Chan, Erik D. Demaine, Jeff Erickson, Ferran Hurtado, John Iacono, Stefan Langerman, Mihai Pătraşcu and Perouz Taslakian, Necklaces, convolutions, and X+Y, Algorithmica 69(2), 2014, 294-314 (conference version in ESA 2006, LNCS 4168, 160-171, without Pătraşcu as an author)"
    locator: the O(n^2/log n) algorithm for min-plus convolution, the O(n^1.5) nonuniform decision tree, and the reduction to APSP (cited by Cygan et al. as Theorem 13 of the ESA version)
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: the abstract and the introduction (the list of refuted hypotheses, which includes the (min,+)-convolution hypothesis); not yet refereed
---

Min-plus convolution takes two integer sequences $a_0, \ldots, a_{n-1}$ and $b_0, \ldots, b_{n-1}$ and computes $c_k = \min_{i+j=k} (a_i + b_j)$ for each $k$. It is ordinary [convolution](/convolution/) with the operations $(+, \times)$ replaced by $(\min, +)$. The direct method takes $O(n^2)$ time. The [fast Fourier transform](/fast-fourier-transform/) does not apply, because $\min$ has no inverse, and for decades only subpolynomial factors were saved.

In 2017, Cygan, Mucha, Węgrzycki and Włodarczyk proposed the hypothesis that min-plus convolution has no $O(n^{2-\varepsilon})$ algorithm, and showed that it is equivalent to several other problems, among them 0/1 knapsack and unbounded knapsack with capacity $t$ in time $O((n+t)^{2-\varepsilon})$. Künnemann, Paturi and Schneider found some of the same results at the same time. Min-plus convolution reduces both to [3SUM](/3sum/) and to [APSP](/apsp-conjecture/), so its hypothesis was weaker than both. In October 2026, Alman and Vassilevska Williams posted a preprint that makes 3SUM truly subquadratic. Through the reduction to 3SUM, this makes min-plus convolution truly subquadratic too, if the preprint is correct.

## In plain words

You have two lists of numbers. For each target position, look at every way to pick one number from the first list and one from the second list so that their positions add up to the target. Add each picked pair, and keep the smallest total.

Doing this for every target takes work that grows with the square of the list length. A famous trick makes the same job fast when you multiply and add instead of add and take the smallest, but the trick fails here.

Many other problems, such as packing a bag with items of the most value, turn out to be exactly as hard as this one. In 2026, a new method made a closely related number problem faster, and that gives a slightly faster method here too.

## Definition

**Min-plus convolution**

- Instance: two sequences $a_0, \ldots, a_{n-1}$ and $b_0, \ldots, b_{n-1}$ of integers in $[-W, W]$.
- Question: output $c_0, \ldots, c_{2n-2}$ with $c_k = \min \{ a_i + b_j : i + j = k \}$. Some sources output only $c_0, \ldots, c_{n-1}$; this changes nothing below.

**The model.** The [word RAM](/word-ram/) with words of $\Theta(\log n + \log W)$ bits, so an addition or a comparison costs $O(1)$. Following the APSP conjecture, Cygan et al. allow factors polylogarithmic in $W$ in a subquadratic time bound.

**Max-plus form.** Negating every entry turns min-plus convolution into max-plus convolution, $c_k = \max_{i+j=k}(a_i + b_j)$. Cygan et al. state their theorems for the max form.

## Variants

- **Upper bound test.** Given $a$, $b$ and $c$, decide whether $c_k \ge \max_{i+j=k}(a_i + b_j)$ for all $k$. This decision form is equivalent to the output form (Cygan et al., Theorem 7, also given by Backurs, Indyk and Schmidt).
- **Superadditivity test.** Given one sequence $a$, decide whether $a_k \ge \max_{i+j=k}(a_i + a_j)$ for all $k$. In the min form this asks whether $a$ is subadditive: $a_{i+j} \le a_i + a_j$.
- **Convex or monotone sequences.** If $a$ and $b$ are convex, the problem takes linear time by merging the slopes. For increasing sequences with values bounded by $O(n)$, Chan and Lewenstein gave $O(n^{1.859})$ randomized and $O(n^{1.864})$ deterministic time, as cited by Cygan et al.
- **Approximation.** With relative error $1 + \varepsilon$, nearly linear time is possible.
- **Matrix form.** The [min-plus matrix product](/min-plus-matrix-multiplication/) $C_{ij} = \min_k (A_{ik} + B_{kj})$ is a different problem. It is the core of the [APSP conjecture](/apsp-conjecture/) and takes about $n^3$ time on $n \times n$ matrices.

## Examples

**A small instance.** Let $a = (0, 3, 5, 9)$ and $b = (0, 2, 7, 8)$. Then

$$c = (0, 2, 5, 7, 11, 13, 17).$$

For example, $c_2 = \min(a_0 + b_2, a_1 + b_1, a_2 + b_0) = \min(7, 5, 5) = 5$, and the minimum is reached by $(i, j) = (1, 1)$ and $(2, 0)$. For $c_4$, the candidates are $a_1 + b_3 = 11$, $a_2 + b_2 = 12$ and $a_3 + b_1 = 11$, so $c_4 = 11$, reached by $(1, 3)$ and $(3, 1)$. Each $c_k$ takes at most $\min(k, 2n - 2 - k) + 1$ additions, so the direct method uses $n^2 = 16$ additions in all.

**A subadditivity test.** Let $s = (0, 2, 3, 5, 8)$. The min-plus convolution of $s$ with itself, cut to the first 5 entries, is $(0, 2, 3, 5, 6)$. The sequence is subadditive exactly when the two agree, since the term $s_0 + s_k = s_k$ is always a candidate. They differ at $k = 4$: $s_2 + s_2 = 6 < 8 = s_4$. So $s$ is not subadditive. Changing $s_4$ to any value at most 6 makes it subadditive.

## Known algorithms

- **Direct.** $O(n^2)$ time, deterministic.
- **Bremner et al.** (ESA 2006, Algorithmica 2014). $O(n^2 / \log n)$ time on the word RAM, and a nonuniform decision tree of depth $O(n^{1.5})$, by the method of Fredman.
- **Through APSP.** With the reduction of Bremner et al. to APSP, the APSP algorithm of Williams (STOC 2014) gives $O(n^2 / 2^{\Omega(\sqrt{\log n})})$ time.
- **Random inputs.** Bussieck et al. compute it in $O(n \log n)$ expected time for random inputs and $O(n^2)$ in the worst case, as cited by Cygan et al.
- **2026.** The reduction to 3SUM below, with the deterministic $O(n^{1.9992})$ 3SUM algorithm of Alman and Vassilevska Williams (arXiv:2610.06783), gives a truly subquadratic algorithm for $W$ bounded by a polynomial in $n$. Their paper lists the (min,+)-convolution hypothesis among those it refutes. The exponent depends on the losses in the chain of reductions. The preprint is not yet refereed.

## Bounds

- **Unconditional.** $\Omega(n)$, to read the input. In the nonuniform decision tree model, depth $O(n^{1.5})$ is enough, so no quadratic lower bound can be proved there.
- **Conditional, before 2026.** The hypothesis below. Since min-plus convolution reduces to both 3SUM and APSP, the 3SUM conjecture and the APSP conjecture each implied it. No relation to SETH or to [Orthogonal Vectors](/orthogonal-vectors/) is known. Cygan et al. prove that there is no deterministic reduction from SAT to unbounded knapsack that rules out time $O(n^{1-\varepsilon} t)$, unless the nondeterministic form of SETH fails.

### Hypothesis (min-plus convolution)

For every $\varepsilon > 0$, there is no $O(n^{2-\varepsilon} \operatorname{polylog}(W))$ algorithm for min-plus convolution of integer sequences of length $n$ with entries in $[-W, W]$ (Cygan et al., Conjecture 1).

- The model is the word RAM.
- The range is $[-W, W]$, with a factor polylogarithmic in $W$ allowed.
- Conjecture 1 does not say whether randomized algorithms count. Theorem 2 of Cygan et al., the equivalence with knapsack, is stated with randomized algorithms allowed, so it is safest to read the hypothesis as excluding randomized algorithms too.

Status: refuted for $W$ bounded by a polynomial in $n$, through 3SUM, if the October 2026 preprints are correct.

## Reductions

All of these have $a(n) = b(n) = n^2$ in $n$, or $(n + t)^2$ for the knapsack problems with capacity $t$.

- **The equivalence class** (Cygan et al., Theorem 2). Max-plus convolution, its upper bound test, the superadditivity test, unbounded knapsack and 0/1 knapsack are equivalent: a truly subquadratic algorithm for one gives one for all. The ring of reductions runs from max-plus convolution to the upper bound test (Theorem 7), to the superadditivity test (Theorem 6), to [unbounded knapsack](/unbounded-knapsack/) (Theorem 5), to 0/1 [knapsack](/knapsack-problem/) (Theorem 3), and back to max-plus convolution (Theorem 13). Only Theorem 13 is randomized.
- **More equivalent problems.** The maximum consecutive subsums problem, which asks for the largest sum of $k$ consecutive entries for each $k$, is equivalent (Laber, Bardales Roncalla and Cicalese, ISIT 2014, and a simpler proof by Cygan et al.). Tree sparsity is equivalent: max-plus convolution reduces to it by Backurs, Indyk and Schmidt, and it reduces back by Theorem 19 of Cygan et al.
- **To APSP** (Bremner et al.). Deterministic. A truly subcubic APSP algorithm gives a truly subquadratic min-plus convolution algorithm.
- **To 3SUM** (Cygan et al., Appendix A, after Vassilevska Williams and Williams). Deterministic. Max-plus convolution reduces to its upper bound test (Theorem 7). The upper bound test reduces to $O(\log W)$ instances of [Convolution 3SUM](/convolution-3sum/), one pair for each length of binary prefix (Theorem 25). Convolution 3SUM reduces to 3SUM in linear time. No step of this chain is randomized.
- **Not known.** No reduction is known from 3SUM or APSP to min-plus convolution. Such a reduction would link 3SUM and APSP, which was a major open question.

Together, the first two items make one [fine-grained equivalence class](/fine-grained-equivalence-class/).

## Applications

- **Knapsack.** The textbook [dynamic program](/knapsack-dynamic-programming/) for knapsack takes $O(nt)$ time. Combining the best answers of two groups of items for every capacity is a max-plus convolution, which is why the problems are equivalent.
- **Strings.** Fast min-plus convolution gives $o(n^2)$ algorithms for indexed permutation matching and for jumbled pattern matching, as surveyed by Cygan et al.
- **Necklace alignment.** Bremner et al. reduced the $\ell_\infty$ form of necklace alignment to min-plus convolution, which gave a slightly subquadratic algorithm.
- **Hardness.** Before 2026, the hypothesis gave conditional quadratic bounds for the problems of the class. After the 2026 preprints, these bounds have no base, for numbers bounded by a polynomial.

## References
