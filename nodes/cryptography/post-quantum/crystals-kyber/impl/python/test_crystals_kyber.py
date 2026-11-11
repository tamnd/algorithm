# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crystals-kyber/. The authors are listed in prov/X4A2D0.jsonl.

import hashlib
import random

from crystals_kyber import (
    PARAMS,
    Q,
    byte_decode,
    byte_encode,
    check_ek,
    compress,
    decaps,
    decaps_internal,
    decompress,
    encaps,
    encaps_internal,
    keygen,
    keygen_internal,
    multiply_ntts,
    ntt,
    ntt_inv,
    sizes,
)

# Official vectors: NIST ACVP-Server, gen-val/json-files/ML-KEM-keyGen-FIPS203,
# prompt.json (d, z) and expectedResults.json (ek, dk). The keys are long, so the
# test compares SHA-256 of our output with SHA-256 of the official hex.
KEYGEN_VECTORS = [
    # (tcId, parameter set, d, z, SHA-256(ek), SHA-256(dk))
    (
        1,
        "ML-KEM-512",
        "47B893474672BA92E4B12EE44FB32953AF8E8503B5FB471D1614FB8A021A660A",
        "1F8CB39E9E30BC458A0DC5408884B1187FB217018DF760FA57317703B844A0A9",
        "7e4a2b716a684c1ad33c43c808782da9e1a72f14ccda82723f712d49f53a9f28",
        "c725c25ca8636d75653a07e7a9ccf0b3c2b927617e8f99f0f05ab1f9cb7e046d",
    ),
    (
        26,
        "ML-KEM-768",
        "E582B7D75E6C80B05AE392A1FC9F7153B12390FD99930368CC67A768BAEBC8A0",
        "1CDACB8740C0B87C4A379575F187B367CBFA3B300BF591B109F79816E9CBE8F0",
        "4158f6afb5e516c99f1da07da8c651348422b17c1f4e9a08ad73fb1f91249b3e",
        "7aab35839207f72b310abe36e2daa1cc7ff6f7fa8941e439967cd47d9b437079",
    ),
    (
        51,
        "ML-KEM-1024",
        "F3A706FAF090C03DB506863AB0B20BD8A1627956318E88C67EB875E8E7266009",
        "35D2BC43DD1CC879F765BF2A0C5E297889DDE910E57E2BB0EAE417B90AB7A275",
        "b78619e4fceeeb86dee3fedb945eca6da61dae312771ef8fa871951d391bd7b6",
        "925ed6f1cf0379ede29d8209432d6e08c73ed0423883febf85416343f4fa1f86",
    ),
]

# Official vector: NIST ACVP-Server, gen-val/json-files/ML-KEM-encapDecap-FIPS203,
# test group 1 (ML-KEM-512, encapsulation), tcId 1. ek and m are from prompt.json,
# k and SHA-256 of c from expectedResults.json.
ENC_EK_HEX = (
    "17E5129B2029F3281987D6624725B64C51CF8DCA3562372BACB7AE15FA9F2FF6AB47659B7D305B61F55F571315FF69AA49E1388100319A650E86C59BA3024C3D"
    "EC83D4AAAB661C452F6CB6A8D2638C133C599045329CCC8F677D24683DF1146EE1C7318C3763A47ACFF81A03927B9BAC5A49DC285C4EE204C4D72DBB1C97FE53"
    "C622E621338669FCFAC1E30A36F0A9769BBB2BA408787EE629CEC383F29AAAABD46E22133F339C08E29B82C4FAAF0F676E1C2B04377975DC3A3B246488EDD163"
    "6C58ABCD65B8198B6FA8A8475EF541DAF34B5ADB9DB0589D8958B62A88930EEB1C0C352B1E57BC7882C89EFA318457813F2B55B96881E7F75C3DC97357681E54"
    "553AE099095AC38B34C00199952602C481C0F1CF74B550CE7C4F6C5876AFF076DD921942DB377E1749F0306F77443A2F058D785854C7E32B67F49BCB99A5E18A"
    "AB607C649B892B4DA7CC7AF31557149F02B19460FB49E5051A7251ADE0083CDC1B0B0CA9633220C2B3C532FA2CBC0DC6CFFCD4455E0005D06CAFC727C778375C"
    "B67AC461B3627A653C843BAEAEF866C7F67746262FF6D76536255C89045A172CBFAA123D6ECA3E56FC922F437A14F78D1ADB54B3E54E8DD530450B8500E15A54"
    "C97471CB26AB437394480282BA6B7A786C28857BAF387725BB4342B4C3ABE4CBF90612B04C8BDC1599C2D4C66B80B1A1941440040A42AABE03E1CCB0B4190780"
    "B6603BB69EC199B063826BEAA5447C88427C6BD7A06E4164A490B955152979B8F5BC9417598AF01BCC371577189E1775165B9610B9F75AEEA277018B1C2C0439"
    "1115B6F353AFEECBAA18AA4001DB94FCDC5F46EA520E9836BC5A4576B58C59FC3F75634946D8CC1B1081CE93ABA8566304169332FA316D4BA675A086AD879379"
    "63511E4A1845EA38689B564E11295672098CF01D5D4BAB0338121128A682B048E6AA31B83C65FF861E123010433A3C7607AE5E90C438067F637B44ADF8798CD0"
    "980EC83BDAEB4D427A8F8D88C519E52542F07734A645A2A5BD4D6521A4B64A96A10F35002780169B35E35F01CA74FE6207B8B475EBC079647CC10AEC3C29683E"
    "071D87B82ABBDD6D369E326E475325ED5AE7ED232B37F49388C06A740D421204"
)
ENC_EK_SHA256 = "a2fe4eaaaf5aaa40234661947c990c8fc8d403364008644515014a1a0bd783e1"
ENC_M = "DCACFE4DE1C115DA106ACD1EEFEAFDC7F0F4E5707453EE2D6B0D69D34CC0EF4A"
ENC_K = "2D74374B55D29AA585E144A29BA4F0A96537A73B4F176C5527075F66E38E8858"
ENC_C_SHA256 = "081d14f479358be7af78d18d6282832b81d8b7e71faa119571719e1b07b81e4a"


def test_acvp_keygen():
    for tc, name, d, z, ek_sha, dk_sha in KEYGEN_VECTORS:
        ek, dk = keygen_internal(bytes.fromhex(d), bytes.fromhex(z), PARAMS[name])
        assert len(ek) == sizes(PARAMS[name])["ek"], tc
        assert len(dk) == sizes(PARAMS[name])["dk"], tc
        assert hashlib.sha256(ek).hexdigest() == ek_sha, tc
        assert hashlib.sha256(dk).hexdigest() == dk_sha, tc


def test_acvp_encapsulation_512():
    ek = bytes.fromhex(ENC_EK_HEX)
    assert hashlib.sha256(ek).hexdigest() == ENC_EK_SHA256  # the copy is exact
    key, c = encaps_internal(ek, bytes.fromhex(ENC_M), PARAMS["ML-KEM-512"])
    assert len(c) == 768
    assert key.hex().upper() == ENC_K
    assert hashlib.sha256(c).hexdigest() == ENC_C_SHA256


def test_sizes_match_fips203_table3():
    assert sizes(PARAMS["ML-KEM-512"]) == {"ek": 800, "dk": 1632, "c": 768}
    assert sizes(PARAMS["ML-KEM-768"]) == {"ek": 1184, "dk": 2400, "c": 1088}
    assert sizes(PARAMS["ML-KEM-1024"]) == {"ek": 1568, "dk": 3168, "c": 1568}


def test_ntt_round_trip_and_product():
    rng = random.Random(1)
    f = [rng.randrange(Q) for _ in range(256)]
    g = [rng.randrange(Q) for _ in range(256)]
    assert ntt_inv(ntt(f)) == f
    # schoolbook product in Z_q[X]/(X^256 + 1)
    h = [0] * 256
    for i in range(256):
        for j in range(256):
            if i + j < 256:
                h[i + j] += f[i] * g[j]
            else:
                h[i + j - 256] -= f[i] * g[j]
    h = [x % Q for x in h]
    assert ntt_inv(multiply_ntts(ntt(f), ntt(g))) == h


def test_compress_error_bound():
    # |Decompress_d(Compress_d(x)) - x| mod+- q is at most round(q / 2^(d+1))
    for d in (1, 4, 5, 10, 11):
        bound = (Q + (1 << d)) // (1 << (d + 1))
        for x in range(Q):
            y = decompress(compress(x, d), d)
            diff = (y - x) % Q
            diff = min(diff, Q - diff)
            assert diff <= bound


def test_byte_encode_round_trip():
    rng = random.Random(2)
    for d in (1, 4, 10, 11, 12):
        f = [rng.randrange(min(1 << d, Q)) for _ in range(256)]
        assert byte_decode(byte_encode(f, d), d) == f


def test_round_trip_all_sets():
    for name in PARAMS:
        ek, dk = keygen(name)
        key, c = encaps(ek, name)
        assert decaps(dk, c, name) == key


def test_implicit_rejection():
    params = PARAMS["ML-KEM-768"]
    d, z = bytes(range(32)), bytes(range(32, 64))
    ek, dk = keygen_internal(d, z, params)
    key, c = encaps_internal(ek, bytes(32), params)
    bad = bytearray(c)
    bad[0] ^= 1
    bad = bytes(bad)
    got = decaps_internal(dk, bad, params)
    assert got != key
    assert got == hashlib.shake_256(z + bad).digest(32)  # K_bar = J(z || c)


def test_modulus_check_rejects_bad_ek():
    params = PARAMS["ML-KEM-512"]
    ek, _ = keygen("ML-KEM-512")
    assert check_ek(ek, params)
    bad = bytearray(ek)
    bad[0], bad[1] = 0xFF, bad[1] | 0x0F  # first coefficient = 4095 >= q
    assert not check_ek(bytes(bad), params)
