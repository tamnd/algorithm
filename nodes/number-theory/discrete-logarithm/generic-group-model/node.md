---
tag: SECCP4
kind: model
slug: generic-group-model
name: Generic group model
aliases:
- GGM
- generic group
- generic algorithm model
area: number-theory/discrete-logarithm
level: advanced
summary: Group elements are opaque labels, and an algorithm may only ask an oracle to multiply, invert and compare them. Cost is the number of queries; a discrete logarithm needs about q^(1/2).
prereqs: [discrete-logarithm-problem, cyclic-group]
see_also: [shoup-generic-lower-bound, baby-step-giant-step, pollard-rho-discrete-logarithm, pohlig-hellman, random-oracle-model, ideal-cipher-model, comparison-model, index-calculus]
sources:
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 13, Section 13.4, Lower bound on complexity of generic algorithms for the DLP (13.4.1 Shoup's model, Definition 13.4.1; 13.4.2 Maurer's model; 13.4.3 the lower bound, Lemma 13.4.4, Theorem 13.4.5 and Corollary 13.4.7)
  - paper: doi:10.1007/3-540-69053-0_18
    title: Victor Shoup, Lower bounds for discrete logarithms and related problems, EUROCRYPT 1997, Lecture Notes in Computer Science 1233
    locator: pages 256 to 266 (the model with random encodings, and lower bounds for the discrete logarithm and Diffie-Hellman problems)
  - paper: doi:10.1007/bf02113297
    title: V. I. Nechaev, Complexity of a determinate algorithm for the discrete logarithm, Mathematical Notes 55(2), 1994
    locator: pages 165 to 172 (the first square root lower bound, for deterministic algorithms)
  - paper: doi:10.1007/11586821_1
    title: Ueli Maurer, Abstract models of computation in cryptography, Cryptography and Coding 2005, Lecture Notes in Computer Science 3796
    locator: pages 1 to 12 (the register model without encodings)
  - paper: doi:10.1007/3-540-36178-2_6
    title: Alexander W. Dent, Adapting the weaknesses of the random oracle model to the generic group model, ASIACRYPT 2002, Lecture Notes in Computer Science 2501
    locator: pages 100 to 109 (a scheme secure in the generic group model but insecure for every concrete group)
---

The generic group model is a model of computation for algorithms on a finite group in which the elements are opaque labels: an algorithm sees only the labels, and it can learn about the elements only by asking an oracle to multiply, invert and compare them. The cost of an algorithm is the number of oracle queries. In this model the [discrete logarithm problem](/discrete-logarithm-problem/) in a group of prime order $q$ needs $\Theta(\sqrt q)$ queries: [baby-step giant-step](/baby-step-giant-step/) and [Pollard's rho](/pollard-rho-discrete-logarithm/) meet the [lower bound of Nechaev and Shoup](/shoup-generic-lower-bound/). The model explains why elliptic curve groups resist all known attacks except the generic ones, and it is used to argue the security of cryptographic schemes.

## The machine

There are two standard formulations; they give the same bounds for the discrete logarithm.

**Shoup's model (random encodings).** Let $G$ be a cyclic group of order $n$. An *encoding* is an injective map $\sigma : G \to S$ into a set of bit strings, for example $S = \{0, 1\}^{\lceil 2 \lg n \rceil}$. A generic algorithm receives $n$ and the encodings $\sigma(g_1), \dots, \sigma(g_k)$ of its input elements. It has access to an oracle that, given $\sigma(a)$ and $\sigma(b)$, returns $\sigma(a b^{-1})$; from it one gets the identity $\sigma(1)$, inverses and products. The algorithm may compute anything it likes with the strings it holds, use random bits, store strings in tables and sort them, but it has no other access to the group. The encoding $\sigma$ is chosen uniformly at random among all injective maps, and success probabilities are taken over $\sigma$, the instance and the algorithm's coins (Galbraith, Definition 13.4.1).

**Maurer's model (registers).** The group is $\mathbb{Z}/n\mathbb{Z}$ inside a black box of registers. Register $1$ holds $1$ (standing for $g$) and register $2$ holds the unknown $x$ (standing for $h = g^x$). The algorithm can ask the box to put the sum or difference of two registers into a new register, and to say whether two registers are equal. It never sees the contents. For the discrete logarithm, it must output the content of register $2$. Baby-step giant-step and rho need a sorting relation on the registers as an extra query.

**Earlier forms.** Babai and Szemerédi (1984) defined black box groups, with elements given as strings, possibly not unique, and oracles for the operations and for identity testing. Nechaev (1994) used a deterministic model in which equality testing is free and proved the first $\Omega(\sqrt q)$ bound for discrete logarithms.

## What it counts

The cost of a run is the number of oracle queries: group operations in Shoup's model, register operations and equality tests in Maurer's model. All other work, such as hashing labels, sorting tables or solving linear equations modulo $n$, is free. An algorithm with $m$ queries has seen at most $m + 2$ distinct group elements, and every element it has seen is $g^{a + b x}$ for coefficients $a, b$ that it knows. The lower bound proofs rest on this: the only information an algorithm gets is which of these elements coincide.

For a concrete group, a generic algorithm with $m$ queries translates into a real algorithm with $m$ group operations plus the bookkeeping, so upper bounds in the model are real upper bounds. Lower bounds in the model hold only for algorithms that respect it.

## Relation to other models

- **Concrete groups.** In $(\mathbb{Z}/p\mathbb{Z})^*$ and in $\mathbb{F}_{p^k}^*$, elements are integers or polynomials, and [index calculus](/index-calculus/) uses this: it factors the integers that represent group elements. These algorithms are not generic, and they beat the generic bound by far. For most elliptic curves no such use of the representation is known, so the generic bound is believed to describe them.
- **The comparison model.** The [comparison model](/comparison-model/) restricts sorting algorithms to comparisons in the same way, and its lower bounds hold only for comparison based sorts; [radix sort](/radix-sort/) escapes them as index calculus escapes the generic bound.
- **Idealized models in cryptography.** The [random oracle model](/random-oracle-model/) replaces a hash function by a random function, and the [ideal cipher model](/ideal-cipher-model/) replaces a block cipher by a random permutation. The generic group model replaces a group by a random encoding of $\mathbb{Z}/n\mathbb{Z}$. Like the random oracle model, it can be fooled: Dent (2002) gave a scheme that is secure in the generic group model but insecure in every concrete group.
- **Extensions.** Versions with a [pairing](/bilinear-pairing/) oracle, with a decision Diffie-Hellman oracle, or with groups of hidden order are used to study pairing based cryptography and groups of unknown order.

## Known results in the model

Let $n$ be the group order and $q$ its largest prime factor.

- **Discrete logarithm, upper bound.** [Pohlig-Hellman](/pohlig-hellman/) with [baby-step giant-step](/baby-step-giant-step/) uses $O(\sum e_i (\log n + \sqrt{l_i}))$ queries for $n = \prod l_i^{e_i}$, deterministically. Rho uses about $\sqrt{\pi q / 2}$ queries per prime order subgroup, heuristically, with constant memory.
- **Discrete logarithm, lower bound.** In a cyclic group of prime order $q$, a generic algorithm with $m$ queries finds the logarithm with probability at most $(m + 2)^2 / (2q)$ (Galbraith, Theorem 13.4.5, in Shoup's model). So constant success probability needs $\Omega(\sqrt q)$ queries, and success probability $1/\log^c q$ needs $\Omega(\sqrt{q / \log^c q})$ (Corollary 13.4.7). For composite $n$, the bound is $\Omega(\sqrt q)$, so Pohlig-Hellman is optimal up to logarithmic factors. See [Shoup's generic lower bound](/shoup-generic-lower-bound/).
- **Diffie-Hellman problems.** Shoup proved $\Omega(\sqrt q)$ bounds also for the [computational](/computational-diffie-hellman/) and [decisional](/decisional-diffie-hellman/) Diffie-Hellman problems.
- **Group order.** If the order is not given, computing it from a bound $M$ with $\sqrt M < n < M$ needs $\Omega(n^{1/3})$ queries (Sutherland, cited in Galbraith, Section 13.4.1).
- **The key lemma.** The proofs use the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/): a nonzero polynomial of degree $d$ over $\mathbb{F}_q$ vanishes at a random point with probability at most $d/q$ (Galbraith, Lemma 13.4.4).

## References
