---
tag: DWHJ3K
kind: algorithm
slug: rainbow-signature
name: Rainbow signature
aliases:
- Rainbow
- multilayer unbalanced oil and vinegar
area: cryptography/post-quantum
level: advanced
summary: Multivariate signature that stacks UOV layers to shrink keys. A NIST round 3 finalist, broken in 2022 when Beullens recovered a level 1 key in about 53 hours on a laptop.
model: word-ram
complexity:
  vars: {n: "the number of variables, v1 + o1 + o2", m: "the number of equations, o1 + o2"}
  time: {worst: O(m n^2), average: O(m n^2), best: O(m n^2)}
  space: {extra: O(m n^2)}
properties: {deterministic: false, randomized: true}
history:
  year: 2005
  people: [Jintai Ding, Dieter Schmidt]
  note: Ding and Schmidt stacked layers of unbalanced oil and vinegar in 2005. Rainbow became a NIST round 3 finalist in 2020 and was broken by Beullens in 2022.
prereqs: [unbalanced-oil-and-vinegar]
see_also: [multivariate-cryptography, multivariate-quadratic-problem, hidden-field-equations, existential-unforgeability, hash-and-sign-paradigm, crystals-dilithium, xl-algorithm, f4-algorithm]
sources:
  - paper: "Jintai Ding and Dieter Schmidt, Rainbow, a new multivariable polynomial signature scheme, ACNS 2005, LNCS 3531, pages 164 to 175"
    locator: the whole paper (the layered construction and the first parameters)
  - paper: "Ward Beullens, Breaking Rainbow takes a weekend on a laptop, Crypto 2022, LNCS 13508, pages 464 to 479"
    locator: the simple attack, its combination with the rectangular MinRank attack, and the key recovery for the security level 1 parameters in about 53 hours
  - url: "https://eprint.iacr.org/2022/214"
    title: Ward Beullens, Breaking Rainbow takes a weekend on a laptop, IACR ePrint 2022/214
    locator: the abstract and the experiments (the 53 hour key recovery on a laptop)
  - paper: "Ward Beullens, Improved cryptanalysis of UOV and Rainbow, Eurocrypt 2021, LNCS 12696, pages 348 to 373"
    locator: the rectangular MinRank attack and the intersection attack, which lowered the security of the Rainbow parameter sets
  - paper: "Olivier Billet and Henri Gilbert, Cryptanalysis of Rainbow, SCN 2006, LNCS 4116, pages 336 to 347"
    locator: the whole paper (a MinRank key recovery on the first Rainbow parameters)
  - paper: "Jintai Ding, Bo-Yin Yang, Chia-Hsin Owen Chen, Ming-Shing Chen and Chen-Mou Cheng, New differential-algebraic attacks and reparametrization of Rainbow, ACNS 2008, LNCS 5037, pages 242 to 257"
    locator: the Rainbow band separation attack and new parameters
  - url: "https://doi.org/10.6028/NIST.IR.8309"
    title: NIST IR 8309, Status Report on the Second Round of the NIST Post-Quantum Cryptography Standardization Process, July 2020
    locator: the list of round 3 finalists, which has Rainbow as a signature finalist
  - url: "https://doi.org/10.6028/NIST.IR.8413"
    title: NIST IR 8413, Status Report on the Third Round of the NIST Post-Quantum Cryptography Standardization Process, July 2022
    locator: the section on Rainbow (not selected, because of the attacks of Beullens)
---

Rainbow is a [multivariate](/multivariate-cryptography/) [signature](/digital-signature/) scheme by Ding and Schmidt (2005). It stacks layers of [unbalanced oil and vinegar](/unbalanced-oil-and-vinegar/) (UOV): the variables of each layer, oil included, are the vinegar of the next layer. A signer solves one layer at a time, and each layer is a linear system. The layers let Rainbow use fewer variables than UOV for the same number of equations, which gives shorter signatures and smaller keys. Rainbow was one of the three signature finalists of round 3 of the NIST post-quantum process in 2020. **Rainbow is broken.** In 2022 Beullens recovered a secret key for the security level 1 parameters in about 53 hours on a laptop (Crypto 2022, IACR ePrint 2022/214), with an attack that uses exactly the layer structure, and NIST did not select it. Do not use Rainbow.

**Notation.** $q$ is the field size. A two layer Rainbow has $v_1$ vinegar variables, $o_1$ oil variables in layer 1 and $o_2$ in layer 2; $v_2 = v_1 + o_1$, $n = v_1 + o_1 + o_2$ and $m = o_1 + o_2$. $F_j$ is the symmetric matrix of the central form $f_j(x) = x^T F_j x$, $S$ an invertible $n \times n$ matrix and $T$ an invertible $m \times m$ matrix. The public map is $\mathcal{P} = T \circ \mathcal{F} \circ S$, with matrices $P_k = \sum_j T_{kj} S^T F_j S$. $O_2$ is the secret space of the layer 2 oil variables and $W$ the image of the layer 2 outputs under $T$. $P'(x, y) = \mathcal{P}(x + y) - \mathcal{P}(x) - \mathcal{P}(y)$ is the polar form. $H$ hashes a message and a salt to $\mathbb{F}_q^m$. $\lambda$ is the security parameter, $\mathcal{A}$ an adversary and $\mathrm{Adv}$ its advantage. **Security model.** The goal is existential unforgeability under chosen message attack ([EUF-CMA](/existential-unforgeability/)): $\mathrm{Adv}$ is the probability that $\mathcal{A}$, with the public key and a signing oracle, outputs a valid signature on a new message. As for UOV, a salted Rainbow is EUF-CMA secure in the random oracle model if the public map is hard to invert. The attacks below do not break that reduction. They recover the secret key, which shows that the public map is easy to invert for the proposed parameters.

## In plain words

UOV hides quadratic equations in which oil unknowns never multiply each other. Guess the vinegar unknowns, and the oil unknowns follow from linear equations. Rainbow does this twice. First guess a few vinegar unknowns and solve a small linear system for the oil unknowns of layer 1. Then treat all of these as vinegar for layer 2, and solve a second linear system for the oil unknowns of layer 2. Secret linear changes on the unknowns and on the equations hide the layers.

The layers save space, but they also leave a trace. The oil unknowns of the last layer form a hidden subspace with special properties that anyone can test from the public equations. Beullens found a fast way to find one vector of that subspace, and from it the whole secret key follows.

## The problem

Build a [hash-and-sign](/hash-and-sign-paradigm/) signature from a quadratic map $\mathcal{P} : \mathbb{F}_q^n \to \mathbb{F}_q^m$ that anyone can evaluate but only the key owner can invert, with fewer variables per equation than UOV needs.

## The algorithm

```pseudo id=main
KEYGEN(q, v1, o1, o2)                        ▷ n = v1 + o1 + o2, m = o1 + o2, v2 = v1 + o1
L1  for j = 1..o1: F_j ← a random symmetric matrix that uses only the first v2 variables, with a zero oil 1 × oil 1 block
L2  for j = o1+1..m: F_j ← a random symmetric n × n matrix with a zero oil 2 × oil 2 block
L3  S ← a random invertible n × n matrix; T ← a random invertible m × m matrix
L4  for k = 1..m: P_k ← Σ_j T_kj Sᵀ F_j S
L5  return pk = (P_1, ..., P_m) and sk = (F, S, T)

SIGN(sk, M)
L6  salt ← 16 random bytes; t ← T⁻¹ H(M ‖ salt)
L7  x_v ← a random vector of F_q^v1
L8  x_1 ← the solution of the o1 × o1 linear system f_j(x_v, x_1) = t_j, j = 1..o1; if it is not unique, go back to L7
L9  x_2 ← the solution of the o2 × o2 linear system f_j(x_v, x_1, x_2) = t_j, j = o1+1..m; if it is not unique, go back to L7
L10 return σ = (S⁻¹ (x_v, x_1, x_2), salt)

VERIFY(pk, M, σ = (s, salt))
L11 return true if sᵀ P_k s = H(M ‖ salt)_k for every k, else false
```

Line L8 is linear in $x_1$ because layer 1 has no oil 1 $\times$ oil 1 terms, and it does not involve $x_2$ at all. Line L9 is linear in $x_2$ for the same reason. In odd characteristic a symmetric matrix holds a quadratic form; the NIST submission worked over $\mathbb{F}_{16}$ and $\mathbb{F}_{256}$ with upper triangular matrices.

**What the layers leak.** Every vector $o \in O_2$ has $\mathcal{P}(o) = 0$, and $P'(y, o)$ lies in the space $W$ of dimension $o_2$ for every $y$. So the $m \times n$ matrix with rows $(P_k o)^T$ has rank at most $o_2$ instead of $m$, a property that anyone can test.

- **Rectangular MinRank attack** (Beullens, 2021). The matrix above depends linearly on $o$. Finding an $o$ that makes its rank at most $o_2$ is an instance of MinRank, the problem of finding a low rank combination of given matrices, here $n$ matrices of size $m \times n$. Beullens solved it with the support minors modeling, which lowered the security of every Rainbow parameter set.
- **Simple attack** (Beullens, 2022). For a random $x$, the map $D_x : o \mapsto P'(x, o)$ sends $O_2$ into $W$, two spaces of dimension $o_2$. With probability about $1/q$ this map is singular, and then a nonzero $o \in O_2$ lies in the kernel of $D_x$. So the attacker solves $\mathcal{P}(o) = 0$ for $o$ in that kernel, a system of $m$ quadratic equations in $n - m$ variables. The attack costs about $q$ times one such solve, done with [XL](/xl-algorithm/) or [F4](/f4-algorithm/). Beullens also combined it with the MinRank attack for the larger parameter sets.

Once one vector $o \in O_2$ is known, the rest is linear algebra. The vectors $P'(y, o)$ span $W$. The combinations $c$ orthogonal to $W$ give the layer 1 forms $\sum_k c_k P_k$, whose common kernel is $O_2$. What remains is a smaller UOV instance with $v_1$ vinegar and $o_1$ oil variables, whose oil space $O_1$ follows from the known attacks on UOV. With $O_1$ and $O_2$ the attacker signs like the key owner.

```pseudo id=attack
SIMPLE-ATTACK(P_1, ..., P_m)                  ▷ toy version in the code
A1  repeat
A2      x ← a random vector of F_q^n
A3      K ← the kernel of the m × n matrix of y ↦ P'(x, y)
A4      look for o ≠ 0 in K with P(o) = 0 and rank(P_1 o, ..., P_m o) ≤ o2
A5  until such an o is found
A6  C ← {c : Σ_k c_k P_k o = 0}                ▷ a basis of the space orthogonal to W
A7  O_2 ← the common kernel of the matrices Σ_k c_k P_k, c ∈ C
A8  O_1 ← an oil space of the layer 1 forms restricted to a complement of O_2
A9  return (C, O_1, O_2)                       ▷ enough to sign any message
```

## Example

**A hand example over $\mathbb{F}_{31}$.** Take $v_1 = o_1 = o_2 = 1$ with variables $x_1$ (vinegar), $x_2$ (oil of layer 1) and $x_3$ (oil of layer 2), and the central forms $f_1 = x_1^2 + 3 x_1 x_2$ and $f_2 = x_2^2 + x_1 x_3 + 2 x_2 x_3$. Neither has a square of its own oil variable, and $f_1$ does not use $x_3$. Sign the target $(7, 9)$. Choose $x_1 = 1$. Then $f_1 = 1 + 3 x_2 = 7$, so $x_2 = 2$. Now $f_2 = 4 + x_3 + 4 x_3 = 4 + 5 x_3 = 9$, so $x_3 = 1$. Check: $f_1(1, 2, 1) = 1 + 6 = 7$ and $f_2(1, 2, 1) = 4 + 1 + 4 = 9$.

**Toy keys.** The tests use $q = 31$ with $(v_1, o_1, o_2) = (4, 2, 2)$ and $(6, 3, 3)$. For $(6, 3, 3)$, $n = 12$ and $m = 6$, the public key has $6 \cdot \binom{13}{2} = 468$ field elements, and a signature is 12 field elements and a 16 byte salt. The toy key recovery runs on $(2, 2, 2)$ and $(2, 2, 3)$. It finds the true $O_2$ from the public key alone in about a second, and the forged signatures verify.

**Real sizes.** The level 1 parameters of the round 3 submission used $\mathbb{F}_{16}$ with $(v_1, o_1, o_2) = (36, 32, 32)$, so $n = 100$ and $m = 64$. Signatures had 66 bytes and public keys about 158 kilobytes. Beullens' attack recovered such a key in about 53 hours on a laptop.

## Correctness

By the shape of the layer 1 forms, line L8 builds exactly the equations $f_j(x) = t_j$ for $j \le o_1$, and its solution stays valid whatever $x_2$ is. Line L9 then builds exactly the equations of layer 2. So $x$ satisfies $\mathcal{F}(x) = t = T^{-1} H(M \,\|\, \mathrm{salt})$, and $s = S^{-1} x$ gives $\mathcal{P}(s) = T \mathcal{F}(Ss) = H(M \,\|\, \mathrm{salt})$, which line L11 checks. The proof file also proves the properties of $O_2$ and $W$ that the attack uses, and that the signatures forged with a recovered key verify.

## Complexity

- **Signing.** The two linear systems cost $O(o_1^3 + o_2^3)$ and building them $O(m n^2)$, plus $O(n^2)$ for $S^{-1} x$, so $O(m n^2)$ field operations per try. A try fails only when a system is singular, so the expected number of tries is $O(1)$.
- **Verification.** $m$ quadratic forms in $n$ variables: $O(m n^2)$ field operations.
- **Key generation.** $O(m n^3)$ for the products $S^T F_j S$, plus $O(m^2 n^2)$ for the mix by $T$.
- **Space.** The public key has $m \binom{n+1}{2}$ field elements.
- **The attack.** The simple attack costs about $q$ times one solve of $m$ quadratic equations in $n - m$ variables. The toy code instead searches the small kernel and the small remaining UOV instance exhaustively, which is exponential and works only at toy sizes.

## Properties

- **Randomized signing** with a salt and fresh vinegar values.
- **Short signatures and fast verification**, with public keys smaller than UOV for the same level, but still large.
- **Broken.** The layer structure that makes Rainbow smaller than UOV is what the 2022 attack uses. Plain UOV, which has one layer, is not affected by the simple attack.

## Variants and improvements

- **More layers.** Ding and Schmidt allowed any number of layers. The round 2 and round 3 submissions used two.
- **Cyclic and compressed variants.** The NIST submission also had variants that generate part of the public key from a seed. They had the same structure and fell to the same attacks.
- **Earlier attacks.** Billet and Gilbert (2006) attacked the first parameters with a MinRank attack. Ding, Yang and others (2008) found the Rainbow band separation attack and gave new parameters. Later parameter sets accounted for these attacks, the UOV attack on the last layer and the direct attack.
- **After the break.** The multivariate candidates in the NIST process for additional signatures are UOV and variants of it, such as MAYO, QR-UOV and SNOVA; see [UOV](/unbalanced-oil-and-vinegar/).

## When to use it

Never for new systems. Rainbow is broken: a level 1 key falls in a weekend on a laptop. For a post-quantum signature pick a standard scheme from a vetted library, such as [ML-DSA](/crystals-dilithium/) in a FIPS 140 validated module. Study Rainbow to learn how a structure that helps the signer can also help the attacker.

## Pitfalls

- **Layers leak.** Each layer adds a public, testable property, here the rank condition on $O_2$. Any new layered scheme must be checked against MinRank and the simple attack.
- **Reused vinegar values.** As in UOV, two signatures with the same vinegar values leak secret information.
- **No salt.** Without the salt the security proof does not apply.
- **Timing.** The retry loop in lines L7 to L9 and the field arithmetic must not leak secret data through timing. The code of this page does not try to avoid that.

## Implementations

The Python code is for study only. It is not constant time, it uses the random module, and the toy sizes give no security. It works over $\mathbb{F}_{31}$ with symmetric matrices, hashes with SHAKE256, and is not the Rainbow of the NIST submission: there is no $\mathbb{F}_{16}$ or $\mathbb{F}_{256}$ and no official encoding, so the official known answer tests do not apply, and there are no official vectors for these toy keys. Do not use Rainbow from any library; for real signatures use ML-DSA from a vetted library.

The toy key recovery follows the simple attack, but it is not Beullens' full attack. It solves the small system in line A4 by exhaustive search instead of XL or F4, it finds $O_1$ in line A8 by exhaustive search instead of the attacks on UOV, and it does not implement the rectangular MinRank attack. It runs only on toy keys with $v_1 + o_1 \le 4$. The tests check the hand example above, the linear algebra against brute force, the layer shape of the central map, the public key against the secret composition, sign and verify round trips, the properties of $O_2$, and the toy key recovery with forgeries, all with fixed seeds.

## History

Ding and Schmidt proposed Rainbow at ACNS 2005, as a way to make UOV more efficient. Billet and Gilbert attacked its first parameters in 2006, and Ding, Yang and others found the band separation attack in 2008; Rainbow survived with new parameters. It entered the NIST process in 2017 and became a round 3 finalist in July 2020. In 2020 and 2021 Beullens found the rectangular MinRank and intersection attacks, which lowered the security of all parameter sets. In February 2022 he published the simple attack and recovered a level 1 key in about 53 hours on a laptop. In July 2022 NIST chose CRYSTALS-Dilithium (now ML-DSA), Falcon and SPHINCS+ as signatures and did not select Rainbow.

## References
