import knotpy as kp
kp.settings.allowed_moves = "r1,r2,r3"


def kbsm2(k):
    kp.settings.allowed_moves = "r1,r2,r3"
    return kp.kauffman_bracket_skein_module(k, normalize=True)[0][0]

def yamada2(k):
    kp.settings.allowed_moves = "r1,r2,r3"
    ck = kp.closure(k, True, True)
    kp.settings.allowed_moves = "r1,r2,r3,r4,r5"
    y = kp.yamada(ck)
    kp.settings.allowed_moves = "r1,r2,r3"
    return y


def arrow2(k):
    kp.settings.allowed_moves = "r1,r2,r3"
    return kp.arrow_polynomial(k)

def mock2(k):
    kp.settings.allowed_moves = "r1,r2,r3"
    return kp.mock_alexander_polynomial(k)

def affine2(k):
    kp.settings.allowed_moves = "r1,r2,r3"
    return kp.affine_index_polynomial(k)

def match_invariants(invariants, values):
    matches = []
    for key, inv in invariants.items():
        if all(inv.get(k) == v for k, v in values.items()):
            matches.append(key)
    return matches


def num(name):
    return int(name.split("_")[0]), int(name.split("_")[1])

inv = kp.load_invariant_table("data/8-knotoids-invariants.csv")

processed_names = set()

def _get_by_yamada(y):
    return [k for k in inv if inv[k]["yamada"] == y]


mirror_count = [0, 0, 0]
flip_count = [0, 0, 0]
mirror_flip_count = [0, 0, 0]

count_mir_mir_fl_diff = 0

for name in inv:

    k = inv[name]["diagram"]

    print(k.name, end=" -> ",  flush=True)

    y = inv[name]["yamada"]

    mirror = kp.mirror(k, inplace=False)
    flip = kp.flip(k, inplace=False)
    mirror_flip = kp.flip(mirror, inplace=False)

    # compute invaraints of the mirror
    ym = kp.yamada_mirror(y)
    km = kbsm2(mirror)
    am = arrow2(mirror)
    mm = mock2(mirror)
    fm = affine2(mirror)

    # compute invariants of the flip
    yf = y
    kf = kbsm2(flip)
    af = arrow2(flip)
    mf = mock2(flip)
    ff = affine2(flip)

    # compute invariants of the mirror-flip
    ymf = kp.yamada_mirror(y)
    kmf = kbsm2(mirror_flip)
    amf = arrow2(mirror_flip)
    mmf = mock2(mirror_flip)
    fmf = affine2(mirror_flip)

    mirror_inv = {
        "kbsm": km,
        "affine": fm,
        "arrow": am,
        "yamada": ym,
        "mock": mm,
    }

    flip_inv = {
        "kbsm": kf,
        "affine": ff,
        "arrow": af,
        "yamada": yf,
        "mock": mf,
    }

    mirror_flip_inv = {
        "kbsm": kmf,
        "affine": fmf,
        "arrow": amf,
        "yamada": ymf,
        "mock": mmf,
    }


    mirror_others = match_invariants(inv, mirror_inv)
    print(mirror_others, end="; ", flush=True)

    flip_others = match_invariants(inv, flip_inv)
    print(flip_others, end="; ", flush=True)

    mirror_flip_others = match_invariants(inv, mirror_flip_inv)
    print(mirror_flip_others, end="; ", flush=True)
    print()

    assert len(mirror_others) <= 2
    assert len(flip_others) <= 2
    assert len(mirror_flip_others) <= 2

    mirror_count[len(mirror_others)] += 1
    flip_count[len(flip_others)] += 1
    mirror_flip_count[len(mirror_flip_others)] += 1


    inv[name]["mirror"] = " ".join(mirror_others)
    inv[name]["flip"] = " ".join(flip_others)
    #inv[name]["mirror_flip"] = " ".join(mirror_flip_others)

    assert mirror_others == mirror_flip_others




print("Mirror count:", mirror_count)
print("Flip count:", flip_count)
print("Mirror flip count:", mirror_flip_count)
print("Mirror != Mirror flip:", count_mir_mir_fl_diff)


## MANUALLY REMOVE 7_896 - checked by hand

assert "7_181 7_896" == inv["7_1324"]["mirror"]
inv["7_1324"]["mirror"] = "7_181"

assert "7_896" == inv["7_181"]["mutant"]
inv["7_181"]["mutant"] = False

assert "7_181 7_896" == inv["7_181"]["flip"]
inv["7_181"]["flip"] = "7_181"


del inv["7_896"]

print(inv["7_1324"])

kp.save_invariant_table("data/9-knotoids-invariants-with-symmetry.csv", inv)

"""

Mirror count: [0, 793, 57]
Flip count: [0, 792, 58]
Mirror flip count: [0, 793, 57]
Mirror != Mirror flip: 0

"""
