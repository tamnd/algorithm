---
tag: R81X70
kind: algorithm
slug: castryck-decru-attack
name: Castryck-Decru attack
aliases:
- SIDH key recovery attack
- CD attack
area: cryptography/post-quantum
level: research
summary: Key recovery on SIDH and SIKE from one public key (2022). It uses the torsion images and Kani's lemma on products of curves. SIKEp434 falls in minutes on one core.
model: word-ram
complexity:
  vars: {b: "the exponent e_B of Bob's isogeny degree 3^b", a: "the exponent e_A, the length of each (2, 2)-isogeny chain; time counts operations in F_{p^2}, under the CD heuristic, with a small first block of guesses"}
  time: {worst: O(a^2 b), average: O(a^2 b), best: O(a^2 b)}
  space: {extra: O(a)}
properties: {deterministic: true, randomized: false}
history:
  year: 2022
  people: [Wouter Castryck, Thomas Decru]
  note: Posted as IACR ePrint 2022/975 on 30 July 2022, weeks after NIST moved SIKE to round 4, and published at EUROCRYPT 2023 with the follow-up attacks of Maino et al. and of Robert.
prereqs: [sidh, supersingular-isogeny-problem]
see_also: [isogeny-based-cryptography, csidh, nist-pqc-standardization, brute-force-search, meet-in-the-middle-attack, crystals-kyber, post-quantum-cryptography, elliptic-curve-cryptography]
sources:
  - paper: "Wouter Castryck and Thomas Decru, An efficient key recovery attack on SIDH, EUROCRYPT 2023, LNCS 14008; IACR ePrint 2022/975"
    locator: the glue-and-split criterion from Kani's lemma, the auxiliary isogeny from the known endomorphism of the starting curve, the digit by digit recovery of Bob's key, and the Magma run that breaks SIKEp434 (ePrint abstract, current version)
  - paper: "Luciano Maino, Chloe Martindale, Lorenz Panny, Giacomo Pope and Benjamin Wesolowski, A direct key recovery attack on SIDH, EUROCRYPT 2023, LNCS 14008"
    locator: the attack without a known endomorphism of the starting curve, which recovers the secret isogeny directly
  - paper: "Damien Robert, Breaking SIDH in polynomial time, EUROCRYPT 2023, LNCS 14008"
    locator: the proof of polynomial time for every starting curve, with isogenies between abelian varieties of dimension 4 or 8 and Zarhin's trick
  - paper: "Ernst Kani, The number of curves of genus two with elliptic differentials, Journal fur die reine und angewandte Mathematik 485, 1997"
    locator: the criterion for an isogeny of a product of two elliptic curves to split, which the attack calls Kani's lemma
  - paper: "David Jao and Luca De Feo, Towards quantum-resistant cryptosystems from supersingular elliptic curve isogenies, PQCrypto 2011, LNCS 7071"
    locator: the SIDH public key with the images of the other party's torsion basis
  - url: "https://sike.org/files/SIDH-spec.pdf"
    title: David Jao and others, Supersingular Isogeny Key Encapsulation, round 4 specification, 2022
    locator: the parameter set SIKEp434 with p = 2^216 3^137 - 1 and its starting curve
  - paper: "Tako Boris Fouotsa, Tomoki Moriya and Christophe Petit, M-SIDH and MD-SIDH: countering SIDH attacks by masking information, EUROCRYPT 2023, LNCS 14008"
    locator: the countermeasures that hide the torsion images, and their parameter sizes
  - paper: doi:10.6028/NIST.IR.8545
    title: NIST, Status report on the fourth round of the NIST post-quantum cryptography standardization process, NIST IR 8545, 2025
    locator: the section on SIKE and the attacks that broke it
---

The Castryck-Decru attack recovers the secret key of [SIDH](/sidh/) and SIKE from a single public key. Wouter Castryck and Thomas Decru posted it on 30 July 2022, a few weeks after NIST had moved SIKE to round 4. The current version of their ePrint abstract reports that a Magma program breaks SIKEp434, the category 1 set, in about ten minutes on a single core. The attack uses two things SIDH gives away: the images of the other party's torsion basis in the public key, and a small endomorphism of the public starting curve. Its core is Kani's lemma, which turns a correct guess about the secret isogeny into an isogeny of abelian surfaces that splits into a product of two elliptic curves. Maino, Martindale, Panny, Pope and Wesolowski removed the need for a special starting curve, and Robert proved polynomial time for every starting curve. The attack does not touch the general [supersingular isogeny problem](/supersingular-isogeny-problem/), [CSIDH](/csidh/) or SQIsign, which publish no such torsion images.

**Notation.** As on the SIDH page, $p = 2^a 3^b - 1$, $E_{\mathrm{start}}$ is the starting curve, $(P_A, Q_A)$ is a basis of $E_{\mathrm{start}}[2^a]$, and Bob's secret is an isogeny $\varphi_B : E_{\mathrm{start}} \to E_B$ of degree $3^b$. His public key is $(E_B, U, V)$ with $U = \varphi_B(P_A)$ and $V = \varphi_B(Q_A)$. $\hat f$ is the dual of an isogeny $f$, so $\hat f f = [\deg f]$. An $(M, M)$-isogeny is an isogeny of principally polarized abelian surfaces whose kernel is a maximal isotropic subgroup of the $M$-torsion, isomorphic to $(\mathbb{Z}/M)^2$.

## In plain words

In SIDH each party publishes the end of a secret walk and also where some public points ended up after the walk. That extra information was meant only to let the other party finish the key exchange.

The attack guesses the start of the secret walk a few steps at a time. For each guess it builds a larger object from two curves and asks a yes or no question about it. A deep result from 1997 says that the answer is yes when the guess fits the published points, and in practice it is no otherwise. So the attacker learns the secret walk piece by piece, with only a few guesses for each piece. Each question takes a moment on an ordinary computer.

## The problem

Given SIDH public parameters and Bob's public key $(E_B, \varphi_B(P_A), \varphi_B(Q_A))$, find $\varphi_B$, or equivalently Bob's secret key. This is the SIDH variant of the [supersingular isogeny problem](/supersingular-isogeny-problem/). Before 2022 the best attacks ignored the torsion images and took time about $p^{1/4}$, which set the size of the SIKE primes.

## The algorithm

**Kani's lemma.** Let $f : E \to E_1$ and $g : E \to E_2$ be isogenies of coprime degrees $d_1$ and $d_2$, with $d_1 + d_2 = M$, and let $f' : E_2 \to X$ and $g' : E_1 \to X$ complete a commutative square $g' f = f' g$, with $\deg f' = d_1$ and $\deg g' = d_2$. Then

$$\Phi = \begin{pmatrix} \hat f & \hat g \\ -g' & f' \end{pmatrix} : E_1 \times E_2 \to E \times X$$

is an $(M, M)$-isogeny with kernel $\{(f(T), g(T)) : T \in E[M]\}$. The kernel needs only the values of $f$ and $g$ on $E[M]$. An $(M, M)$-isogeny with a kernel of this shape usually lands on the Jacobian of a genus 2 curve; it lands on a product of two elliptic curves when such a square exists. The attack uses $M = 2^a$, so the values on $E[2^a]$ come from $U$ and $V$.

**The attack.** The square is set up so that $g$ is the part of Bob's isogeny that is not yet known and $f$ is an auxiliary isogeny $\gamma$ of degree $c = 2^a - 3^{r}$, where $3^r$ is the degree of that unknown part. Castryck and Decru build $\gamma$ from the known endomorphisms of $E_{\mathrm{start}}$ (for SIKE, a curve 2-isogenous to $y^2 = x^3 + x$, whose endomorphism $(x, y) \mapsto (-x, iy)$ is known). The pseudocode below is a simplified outline; the paper's notation and bookkeeping differ.

```pseudo id=attack
CD-ATTACK(E_start, P_A, Q_A, (E_B, U, V), a, b)
A1  known ← the empty string of ternary digits
A2  β ← the least number of steps with 3^(b − β) < 2^a
A3  while |known| < b do
A4      r ← b − |known| − β; c ← 2^a − 3^r
A5      find an isogeny γ of degree c from known endomorphisms     ▷ if c does not suit, raise β
A6      for each string g of β ternary digits do
A7          ψ ← the walk given by known ‖ g; χ ← the unknown rest, deg χ = 3^r
A8          K ← ⟨(γ(T), χ(T)) : T ∈ {P, Q}⟩, the images of a basis (P, Q) of the 2^a-torsion at the top of the square; χ(P), χ(Q) come from U, V and ψ
A9          if the chain of a (2, 2)-isogenies with kernel K ends at a product of two elliptic curves then
A10             known ← known ‖ g; β ← 1; break
A11 return the secret key given by known
```

Line A8 is the point where the torsion images enter: without $U$ and $V$, the values $\chi(P)$ and $\chi(Q)$ are unknown and $K$ cannot be written down. Line A9 is the yes or no question. It costs a chain of $a$ Richelot isogenies between Jacobians of genus 2 curves, followed by a check whether the last codomain is a product. After the first block of $\beta$ steps, each further ternary digit needs at most three guesses.

For SIKEp434, $a = 216$ and $b = 137$. Since $3^{137} > 2^{216} > 3^{136}$, at least one step of Bob's walk must be guessed before $c > 0$; in practice a few more are guessed so that $c$ has a suitable form.

**The toy search of the code.** The code with this page does not implement CD-ATTACK, which needs arithmetic on Jacobians of genus 2 curves. It runs the brute force below on toy SIDH. It is NOT the Castryck-Decru method; it only shows that the torsion images fix the secret.

```pseudo id=main
TOY-RECOVER(E0, (P, Q), (P', Q'), (E_A, U, V), ℓ, e)        ▷ brute force over all ℓ^e secrets
L1  found ← empty list
L2  for s ← 0 to ℓ^e − 1 do
L3      (E, U', V') ← ISOGENY(E0, P + [s]Q, ℓ, e, [P', Q'])
L4      if j(E) = j(E_A) and some isomorphism ι : E → E_A has ι(U') = U and ι(V') = V then
L5          append s to found
L6  return found
```

## Example

**The toy.** The code with this page has a local copy of the toy SIDH of the SIDH page at $p = 2^4 \cdot 3^3 - 1 = 431$, and it recovers secrets by TOY-RECOVER. **It is not the Castryck-Decru method.** It has no genus 2 arithmetic and simply tries all $16$ or $27$ secrets. What it does show is the role of the torsion images.

With the same seeds as the SIDH page, Alice's secret is $a = 15$ and Bob's is $b = 5$.

1. A check on the j-invariant alone (line L4 without the image test) keeps the three secrets $\{4, 10, 15\}$ for Alice and the two secrets $\{0, 5\}$ for Bob. These give different kernels but isomorphic codomains.
2. The full test of line L4 keeps only $15$ and $5$.
3. Over all keys, the j-invariant leaves several candidates for 11 of Alice's 16 keys and for 22 of Bob's 27, while the image test always returns exactly the true secret. It also works when the public curve is published in another model, through the isomorphisms $(x, y) \mapsto (u^2 x, u^3 y)$.

The reason is a degree count: two isogenies of degree 16 that agree on all 729 points of $E_0[27]$ must be equal, since their difference has degree at most 64.

**The real attack at scale.** The CD paper reports breaking SIKEp434 with a Magma program on one core; the current ePrint abstract gives about ten minutes. Implementations in SageMath by other authors followed within weeks of the paper.

The code is for study only, is not constant time, and runs only on toy parameters. SIDH and SIKE are broken; for key exchange use ML-KEM ([CRYSTALS-Kyber](/crystals-kyber/)) from a FIPS 140 validated module.

## Correctness

For the toy: the true secret passes line L4, and by the degree count any secret that passes has the same kernel as the true one, and different secrets give different kernels. So TOY-RECOVER returns exactly the secret. The [full proof](proofs/correctness.md) gives the details and checks the kernel of Kani's lemma.

For the real attack: if the guess is right, the square of line A7 commutes and Kani's lemma says the $(2^a, 2^a)$-isogeny splits, so line A9 accepts. That a wrong guess is rejected is a heuristic: a random $(2^a, 2^a)$-isogeny lands on a product with low probability, and the experiments of CD found no false accept. Robert's version of the attack is proven, with no such heuristic.

## Complexity

Each test of line A9 is a chain of $a = O(\log p)$ isogenies of degree $(2, 2)$, each $O(1)$ operations in $\mathbb{F}_{p^2}$ plus point evaluations, so polynomial in $\log p$. The first block needs $3^\beta$ tests with small $\beta$, and each further digit at most three, so the total is $O(b)$ tests after the first block. The whole attack is polynomial in $\log p$ under the heuristic, given a starting curve with a known small endomorphism. MMPPW drop the condition on the starting curve. Robert proves polynomial time for every starting curve, by gluing in dimension 4 or 8.

The toy search costs $\ell^e$ isogeny computations, which is exponential in $e$; it is feasible only because $\ell^e \le 27$.

## Properties

- Passive: one public key is enough, so ephemeral SIDH keys fall too, unlike the adaptive attack of Galbraith, Petit, Shani and Ti.
- Classical: no quantum computer is used.
- It needs the torsion images. It says nothing about the general isogeny problem, [CSIDH](/csidh/) or SQIsign.
- Deterministic once the auxiliary isogeny is fixed.

## Variants and improvements

- **Maino, Martindale, Panny, Pope and Wesolowski (MMPPW).** A direct attack that recovers the whole isogeny from one split, and works for starting curves with unknown endomorphism ring.
- **Robert.** Polynomial time for every starting curve, with isogenies of abelian varieties of dimension 4 or 8 built with Zarhin's trick, and with no heuristic.
- **Constructive use.** The same higher-dimensional isogenies now build schemes: FESTA uses the attack as a trapdoor, and SQIsignHD and the later two-dimensional versions of SQIsign use them to verify signatures faster.
- **Countermeasures.** M-SIDH and MD-SIDH (Fouotsa, Moriya and Petit) mask the torsion images with a secret scalar or degree, at the cost of much larger keys.

## When to use it

Use it to study cryptanalysis, or to check that a new isogeny scheme does not publish torsion images that allow such a split. It needs nothing else to break SIDH or SIKE, which no one should use now. The toy code is only for study at tiny sizes.

## Pitfalls

- **Do not mix the problems.** The attack breaks the SIDH variant with torsion images. The general [supersingular isogeny problem](/supersingular-isogeny-problem/) still has no known algorithm faster than $\tilde O(p^{1/2})$ classical.
- **Brute force is not the attack.** The toy code tries every secret. Its cost grows as $2^{e_A}$, while the real attack is polynomial.
- **Models of curves.** A check must work up to isomorphism, since a public curve can be given in any model. The toy compares images after every isomorphism $(x, y) \mapsto (u^2 x, u^3 y)$.
- **Heuristic in CD.** The original attack relies on a heuristic for wrong guesses. Robert's proof removes it.

## Implementations

## History

SIDH was proposed in 2011 and SIKE reached round 4 of the NIST process in July 2022. On 30 July 2022, Castryck and Decru posted ePrint 2022/975, with a Magma program that broke SIKEp434 on one core. Within weeks, Maino, Martindale, Panny, Pope and Wesolowski, and then Robert, extended it to all starting curves and to proven polynomial time. The three papers appeared together at EUROCRYPT 2023. NIST did not select SIKE. The attack made higher-dimensional isogenies a standard tool in isogeny-based cryptography.

## References
