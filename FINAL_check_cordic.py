# Usage:  python3 FINAL_check_cordic.py <word_length> <console_output.txt>
# Example: python3 FINAL_check_cordic.py 12 out12.txt
# Compares the simulator's printed lines against the reference outputs from the original parameterized-module runs.
import re, sys

EXPECTED = {
8:  [(-90,0,-63),(-80,12,-62),(-70,21,-59),(-60,33,-57),(-50,43,-49),(-40,48,-38),(-30,58,-32),(-20,62,-24),(-10,63,-13),(0,64,3),(10,63,11),(20,58,24),(30,56,32),(40,48,42),(50,42,48),(60,32,56),(70,24,58),(80,11,63),(90,1,64)],
12: [(-90,6,-1025),(-80,181,-1008),(-70,358,-959),(-60,518,-887),(-50,658,-784),(-40,785,-658),(-30,884,-515),(-20,966,-344),(-10,1008,-181),(0,1024,6),(10,1008,181),(20,959,359),(30,887,515),(40,784,659),(50,659,784),(60,515,887),(70,343,965),(80,181,1008),(90,6,1024)],
16: [(-90,115,-16386),(-80,2898,-16128),(-70,5717,-15355),(-60,8259,-14154),(-50,10541,-12546),(-40,12547,-10542),(-30,14153,-8258),(-20,15358,-5720),(-10,16129,-2899),(0,16387,116),(10,16129,2899),(20,15354,5720),(30,14153,8258),(40,12545,10542),(50,10542,12545),(60,8258,14153),(70,5720,15354),(80,2899,16129),(90,116,16387)],
}

if len(sys.argv) != 3 or int(sys.argv[1]) not in EXPECTED:
    sys.exit("usage: python3 FINAL_check_cordic.py <8|12|16> <console_output.txt>")
wl = int(sys.argv[1])
pat = re.compile(r"angle=(-?\d+)\s+cos_out=(-?\d+)\s+sin_out=(-?\d+)")
got = [tuple(map(int, m.groups())) for m in pat.finditer(open(sys.argv[2]).read())]
exp = EXPECTED[wl]
bad = [(g, e) for g, e in zip(got, exp) if g != e]
if len(got) != len(exp):
    print(f"FAIL: found {len(got)} result lines, expected {len(exp)}")
elif bad:
    print(f"FAIL: {len(bad)} line(s) differ")
    for g, e in bad:
        print(f"  got {g}   expected {e}")
else:
    print(f"PASS: all {len(exp)} lines match for WL={wl}")
