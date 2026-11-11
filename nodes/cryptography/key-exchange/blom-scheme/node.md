---
tag: 809KWA
kind: algorithm
slug: blom-scheme
name: Blom's scheme
aliases:
- Blom key predistribution
area: cryptography/key-exchange
level: advanced
summary: A key predistribution scheme. A center gives each user a row of a secret symmetric matrix times a Vandermonde matrix, and any two users get a common key with no message.
solves: [key-predistribution-problem]
model: word-ram
complexity:
  vars: {n: the number of users, k: the largest coalition the scheme resists}
  time: {worst: Θ(n k^2), average: Θ(n k^2), best: Θ(n k^2)}
  space: {extra: Θ(k^2 + n k)}
properties: {deterministic: false, randomized: true}
history:
  year: 1984
  people: [Rolf Blom]
  note: Blom presented the scheme at EUROCRYPT 1984, "An optimal class of symmetric key generation systems", with a proof that its storage is the least possible.
prereqs: [key-predistribution-problem, vandermonde-matrix]
see_also: [key-predistribution-problem, key-distribution-problem, vandermonde-matrix, reed-solomon-code, shamir-secret-sharing, lagrange-interpolation, gaussian-elimination, identity-based-encryption]
sources:
  - paper: doi:10.1007/3-540-39757-4_22
    title: Rolf Blom, An optimal class of symmetric key generation systems, EUROCRYPT 1984, LNCS 209, pages 335 to 338, 1985
    locator: the construction from a symmetric matrix and the generator matrix of an MDS code, and the lower bound on the stored key material
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 12.4, Definition 12.32 (key distribution system), Definition 12.33 (j-secure), Fact 12.34 (Blom's bound), Mechanism 12.35, Note 12.36 (MDS codes) and Remark 12.37 (the choice of k)
  - paper: doi:10.1007/3-540-48071-4_33
    title: Carlo Blundo, Alfredo De Santis, Amir Herzberg, Shay Kutten, Ugo Vaccaro and Moti Yung, Perfectly-secure key distribution for dynamic conferences, CRYPTO 1992, LNCS 740
    locator: the symmetric polynomial form of the two-party scheme, which is Blom's scheme with a Vandermonde generator matrix
  - paper: doi:10.1145/948109.948118
    title: Wenliang Du, Jing Deng, Yunghsiang S. Han and Pramod K. Varshney, A pairwise key pre-distribution scheme for wireless sensor networks, ACM CCS 2003, pages 42 to 51
    locator: the multiple-space scheme that gives each sensor several Blom key spaces chosen at random
---

Blom's scheme is a key predistribution scheme in which a trusted center gives each of $n$ users a short secret vector, after which any two users can compute a common key from their own vector and the other's public identity, with no message and no further help. The keys are entries of a symmetric matrix $K = G^T D G$, where $D$ is a secret random symmetric $(k + 1) \times (k + 1)$ matrix and $G$ is a public [Vandermonde](/vandermonde-matrix/) matrix. Any $k$ users who pool their vectors learn nothing about a key between two others, while $k + 1$ users can recover $D$ and every key. Each user stores $k + 1$ field elements, the least possible for this level of security, which is why Blom called the class optimal.

**Notation.** $q$ is a prime (or prime power) and all arithmetic is in the field $\mathbb{F}_q$. User $i$ has a public identity $x_i \in \mathbb{F}_q$, all distinct, and the public column $g_i = (1, x_i, x_i^2, \dots, x_i^k)^T$. $D$ is the center's secret symmetric matrix and $a_i = D g_i$ is user $i$'s secret vector. $K_{ij} = a_i \cdot g_j$ is the key of users $i$ and $j$. The scheme is called $k$-secure if every coalition of at most $k$ users, not including $i$ and $j$, has no information about $K_{ij}$. HAC uses a $k \times k$ matrix and calls that scheme $j$-secure for $j \le k - 1$; our $k$ is HAC's $k - 1$.

## In plain words

A trusted office makes a secret table of numbers that reads the same across and down. It gives each user a short list of numbers made from that table and the user's public name.

When two users want to talk, each combines their own list with the other's public name. Because the table is symmetric, both get the same number, and that is their key. They do not need to send anything.

The office chooses a number $k$. Any group of up to $k$ users who pool their lists still knows nothing about the key of two other users. A group of $k + 1$ users can rebuild the whole table, so $k$ must be larger than any group of thieves the system must survive.

## The problem

There are $n$ users, and every pair needs a secret key, but the users are small devices that cannot run public key cryptography or talk to a server at the time of use. A trusted center may load secret data into each device before deployment. This is the [key predistribution problem](/key-predistribution-problem/). Storing a separate key for every partner costs $n - 1$ keys per device; Blom's scheme stores $k + 1$ elements and resists coalitions of up to $k$ users.

## The algorithm

```pseudo id=main
BLOM(x_1, …, x_n, k, q)
L1  center: pick a random symmetric (k + 1) × (k + 1) matrix D over F_q
L2  for each user i: g_i ← (1, x_i, x_i^2, …, x_i^k)
L3      give user i the secret vector a_i ← D g_i, over a secure channel
L4  user i, to talk to user j: K_ij ← a_i · g_j
```

**About the code.** The Python code works over $\mathbb{F}_q$ with $q = 2^{61} - 1$, a Mersenne prime, and its tests use $k$ from 1 to 5. Line L1 draws the $(k + 1)(k + 2)/2$ entries on and above the diagonal and mirrors them. The code also has the attack by $k + 1$ users, which solves $G_C^T D = A_C^T$ by [Gaussian elimination](/gaussian-elimination/); here $G_C$ is the Vandermonde matrix of the coalition and $A_C$ its matrix of secret vectors. It is for study only and is not constant time.

## Example

Take $q = 17$, $k = 1$ and

$$D = \begin{pmatrix} 3 & 5 \\ 5 & 7 \end{pmatrix}.$$

Users 1, 2 and 3 have $x = 1, 2, 3$, so $g_1 = (1, 1)$, $g_2 = (1, 2)$ and $g_3 = (1, 3)$. The center hands out $a_1 = D g_1 = (8, 12)$, $a_2 = D g_2 = (13, 2)$ and $a_3 = D g_3 = (1, 9)$, all modulo 17.

| pair | one side | other side | key |
|---|---|---|---|
| 1, 2 | $a_1 \cdot g_2 = 8 + 24 = 32$ | $a_2 \cdot g_1 = 13 + 2 = 15$ | 15 |
| 1, 3 | $a_1 \cdot g_3 = 8 + 36 = 44$ | $a_3 \cdot g_1 = 1 + 9 = 10$ | 10 |
| 2, 3 | $a_2 \cdot g_3 = 13 + 6 = 19$ | $a_3 \cdot g_2 = 1 + 18 = 19$ | 2 |

This is the same as the polynomial $f(x, y) = 3 + 5(x + y) + 7xy$ of the [key predistribution](/key-predistribution-problem/) page: $a_i$ holds the coefficients of $f(x_i, y)$.

**One user learns nothing.** User 3 knows $a_3 = (1, 9)$, which fixes $d_{00} + 3d_{01}$ and $d_{01} + 3d_{11}$. For each of the 17 values of $d_{01}$ there is exactly one matrix that fits, and these give 17 different values of $K_{12} = d_{00} + 3d_{01} + 2d_{11}$, so $K_{12}$ is uniform from user 3's view. The code checks this exhaustively for $q = 7$.

**Two users learn everything.** Users 1 and 2 together know $a_1$ and $a_2$, four linear equations in the three unknowns of $D$, and they solve them to get $D$ back, and then $K_{13}$ and $K_{23}$.

## Correctness

Since $D$ is symmetric, $K_{ij} = a_i \cdot g_j = g_j^T D g_i = (g_j^T D g_i)^T = g_i^T D^T g_j = g_i^T D g_j = a_j \cdot g_i = K_{ji}$, so the two users get the same key.

**Security.** Let $C$ be a coalition of at most $k$ users, not including $i$ and $j$. The polynomial $w(t) = \prod_{c \in C} (t - x_c)$ has degree at most $k$; its coefficient vector $w$ satisfies $w \cdot g_c = w(x_c) = 0$ for $c \in C$, and $w(x_i)$, $w(x_j) \ne 0$. Changing $D$ to $D + \lambda w w^T$ keeps every $a_c$ the same but adds $\lambda w(x_i) w(x_j)$ to $K_{ij}$, so every key value is consistent with the coalition's data, each with the same number of matrices. A coalition of $k + 1$ users has an invertible Vandermonde matrix $G_C$ and finds $D = (G_C^T)^{-1} A_C^T$. The full proof is below.

## Complexity

The center computes $a_i = D g_i$ for each user, $(k + 1)^2$ multiplications, so $\Theta(nk^2)$ in all, and stores $D$, $\Theta(k^2)$ elements. Each user stores $k + 1$ elements, and computing one key takes $k$ multiplications to build $g_j$ and $k + 1$ for the dot product, $\Theta(k)$. No messages are sent. Fact 12.34 of HAC states the matching lower bound: a scheme that is secure against coalitions of $k$ users and gives keys of $\log_2 q$ bits needs at least $(k + 1)\log_2 q$ bits of secret storage per user, and Blom's scheme meets it exactly.

## Properties

- **Non-interactive.** Two users compute their key with no message; only the identity $x_j$ is needed.
- **Unconditionally secure** against coalitions of at most $k$ users: the guarantee does not depend on any hardness assumption.
- **Sharp threshold.** $k + 1$ users learn every key, with one linear solve.
- **Optimal storage**, $k + 1$ field elements per user (Blom 1984; HAC Fact 12.34).
- **Static keys.** Each pair has one fixed key; derive session keys from it with a nonce and a KDF.

## Variants and improvements

- **Any MDS code.** HAC's form uses the generator matrix $G$ of any $(n, k + 1)$ maximum distance separable code; the Vandermonde matrix is the [Reed-Solomon](/reed-solomon-code/) case.
- **Symmetric polynomials.** Blundo et al. (1992) write the key as $f(x_i, x_j)$ for a random symmetric polynomial $f$ of degree $k$ in each variable, which is the same scheme, and extend it to conference keys for groups of $t$ users with a symmetric polynomial in $t$ variables.
- **Multiple key spaces.** Du, Deng, Han and Varshney (2003) give each sensor several Blom spaces chosen at random from a pool of $\omega$ spaces; two sensors with a common space use it. A coalition must then capture many more nodes before it learns a large fraction of the keys.
- **Random key predistribution.** The Eschenauer-Gligor scheme gives each node a random subset of a large key pool, with no algebra at all.

## When to use it

Use Blom's scheme, or its multiple-space form, when devices cannot afford public key operations, a trusted party loads them before deployment, and a bound $k$ on the number of devices an attacker can capture is acceptable. Wireless sensor networks and some low-power industrial devices fit this profile. When the devices can run elliptic curve operations, non-interactive Diffie-Hellman with certified static keys gives security against any number of captured devices, and is usually the better choice.

## Pitfalls

- **Choosing $k$ too small.** An attacker who captures $k + 1$ devices and reads their memory recovers every key in the system, past and future, at once.
- **Repeated identities.** Two users with the same $x$ get the same secret vector and so share all their keys; the code rejects repeated identities.
- **Leaking $D$.** The center holds a master secret for the whole network and should erase it after setup if no more devices will join.
- **Static keys used directly.** $K_{ij}$ never changes, so encrypting with it directly reuses keys across sessions; derive fresh keys with a nonce.
- **Field size.** Keys are elements of $\mathbb{F}_q$; a small $q$ means short keys, however large $k$ is.

## Implementations

## History

Rolf Blom presented the scheme at EUROCRYPT 1984 (proceedings 1985), building on earlier work of his on reducing key storage with commutative functions, and proved that its storage is optimal. Blundo, De Santis, Herzberg, Kutten, Vaccaro and Yung (1992) gave the symmetric polynomial form and the extension to conferences. The scheme returned to wide use in the early 2000s for sensor networks, in the multiple-space form of Du et al. and in schemes that combine it with random key predistribution.

## References
