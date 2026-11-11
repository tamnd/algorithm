# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sha-3/. The authors are listed in prov/J553RH.jsonl.

import hashlib

from sha_3 import keccak_f, sha3_224, sha3_256, sha3_384, sha3_512

M1600 = bytes([0xA3]) * 200  # the 1600-bit message of the NIST examples: 0xA3 repeated

# NIST, Cryptographic Standards and Guidelines, Example Values: SHA3-224_Msg0.pdf,
# SHA3-224_1600.pdf, SHA3-256_Msg0.pdf, SHA3-256_1600.pdf, SHA3-384_Msg0.pdf,
# SHA3-384_1600.pdf, SHA3-512_Msg0.pdf and SHA3-512_1600.pdf, copied by hand.
NIST = [
    (sha3_224, b"", "6b4e03423667dbb73b6e15454f0eb1abd4597f9a1b078e3f5b5a6bc7"),
    (sha3_224, M1600, "9376816aba503f72f96ce7eb65ac095deee3be4bf9bbc2a1cb7e11e0"),
    (sha3_256, b"", "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"),
    (sha3_256, M1600, "79f38adec5c20307a98ef76e8324afbfd46cfd81b22e3973c65fa1bd9de31787"),
    (sha3_384, b"", "0c63a75b845e4f7d01107d852e4c2485c51a50aaaa94fc61"
                    "995e71bbee983a2ac3713831264adb47fb6bd1e058d5f004"),
    (sha3_384, M1600, "1881de2ca7e41ef95dc4732b8f5f002b189cc1e42b74168e"
                      "d1732649ce1dbcdd76197a31fd55ee989f2d7050dd473e8f"),
    (sha3_512, b"", "a69f73cca23a9ac5c8b567dc185a756e97c982164fe25859e0d1dcc1475c80a6"
                    "15b2123af1f5f94c11e3e9402c3ac558f500199d95b6d3e301758586281dcd26"),
    (sha3_512, M1600, "e76dfad22084a8b1467fcf2ffa58361bec7628edf5f3fdc0e4805dc48caeeca8"
                      "1b7c13c30adf52a3659584739a2df46be589c51ca1a4a8416df6545a1ce8ba00"),
]

# "abc" has no NIST example for SHA-3. These come from a secondary source, D. Ireland,
# "Test vectors for SHA-1, SHA-2 and SHA-3", https://www.di-mgt.com.au/sha_testvectors.html.
ABC = [
    (sha3_224, "e642824c3f8cf24ad09234ee7d3c766fc9a3a5168d0c94ad73b46fdf"),
    (sha3_256, "3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532"),
    (sha3_384, "ec01498288516fc926459f58e2c6ad8df9b473cb0fc08c25"
               "96da7cf0e49be4b298d88cea927ac7f539f1edf228376d25"),
    (sha3_512, "b751850b1a57168a5693cd924b6b096e08f621827444f70d884f5d0240d2712e"
               "10e116e9192af3c91a7ec57647e3934057340b4cf408d5a56592f8274eec53f0"),
]


def test_nist_examples() -> None:
    for fn, msg, want in NIST:
        assert fn(msg).hex() == want, (fn.__name__, len(msg))


def test_abc_secondary() -> None:
    for fn, want in ABC:
        assert fn(b"abc").hex() == want, fn.__name__


def test_keccak_f_zero_state() -> None:
    # XKCP, KeccakF-1600-IntermediateValues.txt, all-zero input: lanes [0,0] and [4,4] of the output.
    out = keccak_f([0] * 25)
    assert out[0] == 0xF1258F7940E1DDE7 and out[24] == 0xEAF1FF7B5CECA249


def test_rate_boundaries_against_hashlib() -> None:
    # Lengths around the rates 144, 136, 104 and 72 bytes, where the padding takes one byte or a new block.
    fns = [(sha3_224, "sha3_224", 144), (sha3_256, "sha3_256", 136),
           (sha3_384, "sha3_384", 104), (sha3_512, "sha3_512", 72)]
    for fn, name, rate in fns:
        for n in (rate - 2, rate - 1, rate, rate + 1, 2 * rate - 1, 2 * rate):
            msg = bytes((5 * i + 3) & 255 for i in range(n))
            assert fn(msg) == hashlib.new(name, msg).digest(), (name, n)
