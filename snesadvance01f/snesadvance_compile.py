#!/usr/bin/python3

import sys, os.path, struct, argparse, bz2, base64, zlib
from sys import argv

EMU_HEADER = 64
SNES_HEADER = 512
SRAM_SAVE = 65536

default_outputfile = "snesadv-compilation.gba"
default_emubinary = "SNESAdvance.bin"
default_database = "snesadvance.dat"
header_struct_format = "<31sx8I" # https://docs.python.org/3/library/struct.html

# ROM header
#
# from gbadefs.h in the SNESAdvance source code and technotes.txt
# https://web.archive.org/web/20080209182322/http://www.snesadvance.org/files/txt/technotes.txt
#
#typedef struct {
#	char title[32];	//ROM title, null terminated
#	u32 romsize;	//ROM size
#	u32 crc32;
#	u32 flags;
#		bit0:           0=Mode20 (LoROM), 1=Mode21 (HiROM)
#		bit1:           0=NTSC, 1=PAL
#		bit2:           0=SRAM disable, 1=SRAM enable
#		bit3:           0=scroll by (addr1)  1=scroll by (addr1)-(addr2)
#		bit4:           1=autoscroll value is a 16 bit number
#		bits 16-31:     "more settings"
#		bits 32-63:     "even more settings"
#	u32 moreflags;
#	u32 autoscroll_val1;
#	u32 autoscroll_val2;
#	u32 autoscroll_scale;
#	int autoscroll_offset;
#} romheader;


def readfile(name):
	with open(name, "rb") as fh:
		contents = fh.read()
	return contents

def writefile(name, contents):
	with open(name, "wb") as fh:
		fh.write(contents)
		if name == default_outputfile:
			print("...wrote", name)	

#def get_bit(value, n):
#    return ((value >> n & 1) != 0)

def set_bit(value, n):
    return value | (1 << n)

#def clear_bit(value, n):
#    return value & ~(1 << n)


background_bin_lz77 = \
	  b'QlpoOTFBWSZTWdtX09EAB9l/////////////////////////////////////////////4DoLduT7t672u2M926zTbFUq2Vg0d2FO' \
	+ b'tGmatoSoX2Yld9nOz7dy2UbZlrfe869r23Rp21s16yrdjl6r193d99N9e+t9ZvWus9fTz17esu99T3X3maiz5ffbr76yVKh0TbvN' \
	+ b'9H29XPq9t6Zfauh8vDPfc9Xfe9vKenXX3Y4zld9nPeG2m+t1ENaAAIgAFAAFhXqHVU/8CYmJkGk2QZAaAAAAmaAAACZNpM00RjQA' \
	+ b'EYAEYTTTTVPwTU2jI00MIYAjJgIwCY1GRNgAI0YQ0T1UOqp/4CYQZNNMmCaZKbABoABMTTGkyMj0AJkNMaTTDQNE8mgDQ0NT0CYN' \
	+ b'I2mhGEyZT0npqemhkTaaAamT0yaBPUzQankA01NUx1U/9A00AJkyDImGTIBNMyjTZTTTxAaanoaNGmgaNRtGjRMBJ5GhMJ6ntCMm' \
	+ b'KnjAmmFMaBpPBGmKPFMTyU9oKfkamGjKanlN6ieTFPU2UMqn+BGg0AJhGmJtATBNMmBGIAgabSepo000yaniNNCn6p+IyZGgaT0p' \
	+ b'4ZDTQk80aJiZpoE2iYm1GBpNFPzRkJgiJ+TEwp6n6oeqfppT8oZVP8AABMQAATJoAmIymxGTATJhNDKegZJ4pgwp4mibJgmhPUxo' \
	+ b'KeA0BTynkaYjCMRk9TE9RT/KaYhoap+TRTY9U9TJ6aZJ6NR5UIqfoCNAg0EwhoxBqaemgmEaNGQ0mBqbQ0aNNCbQNGkwmKn+plMM' \
	+ b'NU9J5KeYjCMmmk1PJ5GjUYNGSZGNBM1Tyaan6U9qnlN6U8U9T1NHiaNI2kfFshQaNX/wSpp/fkPPOhW0J9JqO8Ll0lRobT+krVNl' \
	+ b'AkFVZfKJhjuMlvoxJJl57dSJCVaNk4m97NREKJjyEBtdXfC7V1rXzfxtFkVFMl4TqlQHuQgF7V2YhHylJ/kg300kSASY9WBLFoaQ' \
	+ b'uBwwEVrYqd+2yOmSXoibHcRJxg0rrHzTFaGsXNBQe9/cnyPCfDXSrCE2na1X8x6JXZzeqZ1pLXA6QLKco2WtuFKTt7jo6hNMAyW1' \
	+ b'JSTueKP+kqa2jsWLUOkFIiAn3xpsaNFk7QVXLdqPp+qpH6gUwzHO5QFzNbdIybkCegGeyvugNO7qxibkpmC7ehcczQ4tvm1/6s7g' \
	+ b'aYb5OhT63AOuYgTCAWZCJb6UlF2rV/OXx9YmdaxI78XbXfRkqlxMre8agFUx3SHOmkuUL2khTmw7pTxW9TODV0PLSM/5P+uhBVsJ' \
	+ b'U5fI1pK3uHw7uK8hRU2f3350i9aF0kqSW17WnV/TWTy4mWtm9ivgm64ng1Tja2JhD56fg4K7IWZX7xo+nDIfrIaDJh/NAofzHMKY' \
	+ b'wXBHNy4lk9qzd7NffiN3MXInD7TUsTgpOsKgOWR5OSQCyk+sIfkwL6FWNerMfMtgyTjDf9UOBoN/63ATs/02HQRp0bkbmV1pHR5v' \
	+ b'i1tMvI2aTs8jjjQbHU7racN4QVtsdI9pAiG4qAIO573U317ZaXehlQbNUHLAgLgZ53OF6HC0ug0S5yjradyfyZVa4jCMwom2HZPN' \
	+ b'myMMKXeIVGmtiVRVshVSEarupu3jJrpq/Np6DlSOQfkEe9YVdH6zsq9f5R/t1w8T/Sy8dpvESYzOuILlGjU3HfIi586C4Qy88W9D' \
	+ b'2W61ULCAG766yhpacXz55KnqsGZJ9J2H7Xp7Va3tCsfyluu+9xZppHG4BvPH3528GBXVSMR7mg4eSeev/d/fpzF4pMEfEGFZgOHt' \
	+ b'/pPc/J3X1OHeN8Ilvs9t3blAgvCNmfQNNznwlc+9FKfQbTPkMdo8vH8eRZ0MvpNExZNB86+lYJgKRhIwbslFDfeoIcmZ3ukRMhxJ' \
	+ b'Sqho2bbVuzw/RGdWCTrETjuiyLWyHt8ldqaXEgo2OurjpUQ8vE8Jj1sxFyVa79yPiQy5xQ2jgOwXEjXqk3r3hQBhdDR1Q/ZDUpNu' \
	+ b'hnKZrVRAaZx235GBmGFRs/iMqBnt32SYqkMrLN1Fn/iyNrVHxd3yXH2tlsBlbZ+R1Si5NyS7vwcov/IfEnwB705RPAFO3sbowJMu' \
	+ b'nBmgKEVk2/YLfKeSlkHaU8/VE8CflKB9k9Fawy23tBgECy7s7T72cKbk5U1sub9qNn13Mn8YBDixbktHgPW1o2yuVWl75AIsZR9i' \
	+ b'rqdeszSGgWcEEXFNJHOZ9UqiWnYdbo67Q9hjarzDr2VEZPLsQ4Mp/Qa6eNBqivCBWZSxlfXKo3YxQiwJttacxkippaYfxz1R5tFo' \
	+ b'zDcdLLjlSXP8YUDJZYd/oc6RAwM2Olz+yp8OsMerqRK7i1Z1c91outaVRQ5RVHJ4mI7zlG5K7Q+BfDIaXcT3cQk73AtXjK4Z1vaD' \
	+ b'VYdY510Umdzyr84lmIv0PqUlOPNERtStRS83q/JBXL8/KQH2EKUanJIhESzMdn5opiBhC7ZuVX6mqUjBCUwIP5m0pn1CLireIOLy' \
	+ b'ohG9KjCDBVpsSjRt3wQooF7ooj9V9405cF6mgNhoNdiLRJEFrh+JPT0ioKFI66c2hn8qBw4jZHocPmh8INLfC40mYtBIBseurnQA' \
	+ b'y070F8niPtCGAHfuqHFD6lFOvYuDJZjSrLnaSlWahQ0bWQiOKydj8gfrm8D00inpVrUVBeA/J00QHnjSeCBubJZJlb/04x7vdarv' \
	+ b'Ruwg2zI27ynS1nElJLH0eSbc/Knx9gby/X2Nqla4WvoMhM1XjDY7o69Q4274pLwY0LHNarkMcBtVP5XoE7Fd1y9/RxwQx+4H+/nI' \
	+ b'oJnve7NuN5+3OedPBdItbYkUm9iVHIpqJxyWansF9wH+YBph16Yjod0j2B9vQlSrTL+6CKidcklvynySi79RwyG919xq4Dm7r2xi' \
	+ b'U7FodXl6PZWysyQPvz+zWLB/3bP9K55yqk5nnbP6dvTKvK4FDrZz8HAKoMB26WBbggAX93Tb8PJ3sUe6NEVycnkbH0LPOzmCovJZ' \
	+ b'nAuPYpLepa49xb3ezY7tOwMp2DtVW6UwMIyL5Jg0IvzU1pp/iAeKhTg5R5izo35OXFPi9DjHCP5E40Yjmv0eq5jXDrH3jiHxNXgU' \
	+ b'nrJRIiCv63QtCG8H9I9zakoVksAj8SAVAV15Vte3eqJwG2uUGR71aVL+YPeye+fljBx/1Uzkacb6wEhm+1GuglKFLDY+7dc4xOCC' \
	+ b'XiFAIktb+mJj/E8IMPTrBxRxBvsez1/N6upbCMUIl7NoA/ahNLT9urfKirdGMDUlgOgZJLhn7+NPW8iL8B3ZuYfTlCH46RGKbuTk' \
	+ b'EXFkpAI/jmEBt7ZjNK8T8pKLoUgPuXQxf8xKlRb/E7XsmvGrTyzzOXxdVQSTDn2QceO+F319vd1muW3Os/zMnaLv+Xev8z58YxYQ' \
	+ b'a+XlMgsYuJi2i46xfTDjdT9G1LCMNa0oBCnKC3ixmzfmzXPEJN6cciPu/R8lkT4RJR8L9rWwxJ8r49o0W/dsOTfzZPsaFDzDB6T7' \
	+ b'Jv4NapIQvPkMLq9CsXLn182/GXme7Wl3PNcNKExd2Fta+3hwVkjTYv0hZMxSJWbx8teVY5taG1u/c1reUwD+Nbn7vs9Og/LSwdLE' \
	+ b'QMrn6uXa6EE21+v9FuBXKaC4Ku+W1x/an5Zo6+y5nLl2Yy0d/a7tscEQ2wsRPEbHgn+NFY7u0xsjOQIi4SnG5jmHSTtbfUYGFFry' \
	+ b'1tgPsHT/GWSo4oMN0GqsnxTVnRSB60WD7SFBO0Tciy+1gYJm0yatqTPyYymksZsgqF/1lhXMeJ25uxQi+w3VYtbR/I8ptaK3xJY+' \
	+ b'efLTPOI9CWe6dfPTWzGM41O5dUkpbP7lxBuygLvQ74lIFtjdso3O2tetitafEHnlrliO7fNxSfymKxW3WTrxmEc2+emW8XE/2mzq' \
	+ b'KvD5Z9ubxk7NPDHZe9rnKWIUW3RUJuDQnFRT3e8yXefIln87tmqBJ20TJ75ud+e2fDuTlMJaGfvKwkGx73DJUd9H8hCnCaHHZ6Na' \
	+ b'sZaEk3G8MxOZ4CeStLXbUJzUlagcR+i9xd33ubi93tB3Of1BpadIWukv8PPg5n2SttrLkhc2BNEi45xNAJnpLiHRMHBb+wkfnnjE' \
	+ b'icFBgr0iVVse9/aBlHV0FVIzH6YsWwj1krc+z4bPJV+G/ZzrmgR5C56rU8hD+zAyLE31UldAxAV/URfs03rzWdJcMPOfaTs4j/8f' \
	+ b'cyaOJlYGPOd+nrNRWsLjHimGObUXWsSv2MrLmvjduVPCkp5Qut0hZnstq55gBxVJ52Pb8NH+Epc4Gd1jwyplDkuC9+n5q/wUAC6t' \
	+ b'/D9MuCWr5lzvu+0TGUsETjlYuT0PTVstXzgdYezDhD3QZYvggsjxFWxUHf4lNulv/25gYWRVIwSr61DQEtgjelMZm+A71NYeV+3y' \
	+ b'GeFzxFD3f4xSikrTSuPfSvBIx/9jyWL+cWp/v6Yliy+ersdf9sGlBx0YwQ+Zr4xFhNulIrWit19JhlQvdbzoxz4Wk+QKiv7R9voK' \
	+ b'QUpi/iM3121D/zIf0bz4h0CmF+uuAKjGb5pL4HQZ5V2IoPRqpv2I8m4/nyv2qBw/GRXXRK/r5r5xxth3R3p1aHSpoLaNppBmd0GB' \
	+ b't/c+zagabW1Xg8rxoH8WMMRFTjGddIkvdyDaeVbDkwK9gUHr13GTuFj1GJVhSf8yEcVL1w5Xp8i5mUHZQ4y7uvyTMdXuL0sQHNgT' \
	+ b'EuzXHrDQlrbI3UZ1JXk/9qLr1dtFltOdw03yhAOgwRRZC/1c5ro6M4hQ/fkJdbi+g7nRPjHdWlTY7qHVLOrGlYzeIPyS3QVpfJy5' \
	+ b'tQPcGcpN9Zib3/YtywADVvA3iBv9vR89cvVQhBIoYEF9/Q4GJ5p2YmW6yZk7fwJmJ25dBCzSs7A/c/2cCW5eGE8C8h2oY0tK048f' \
	+ b'VsrbqYQHCswKYTA/6nsNw3SMd523by8ShWsNMuBsg4Hip/T/gfsUuXaBZ/vkNdTXMmj8DZ1fnuPx4bak0bWoWWMsj8KdJ8AP51ZC' \
	+ b'GYcpJ6X9iWs/hw28ueJhaZPO+MKjiDVxXe2/vnix4azPX/FsbNi8VRZrM69kZL1XofxGByp7F/VQnZyj4dkYoVuHaV4blsZS9ouJ' \
	+ b'oveq1bT/sVryR12K0/pF24V4OgvKOholNo2xg1C2Mn/iIL8MyMi3k0Ejhs1BtXGjpJyylmxntfP22NG01vUmsQBdofF1ZJ8EStlt' \
	+ b'RiV3HNTqoqLop1LUAkaCX3vHPgCD9JbVbb4GsfPPfFv7ac/MTTfq29+Z+7ySzvJ7IL1CBw+STTfDRctBcaaTwTWsDD8GUlFD3qEG' \
	+ b'RqW2aYkgSF3ghbvOZsIs52rg4nJrnh3eCH9s4n7dSwcf7i9KlwouM0pM6wbqO74GppuUXLKh6XlbTN7SXfsSYFXGltX0d0WA+Una' \
	+ b'PCgXZ0yPY6r31lTB1rqBx66yZqlthMRtG3P8jslcd+9z5R4HkdrjJayxxmfpgznbbrDGa4pRh7l6lC3mYXOZK/FBzFrPuG/9CsRl' \
	+ b'IO3T9fIQG17VY/B23DYQQ/uH9C3eI2jQ1p+XzaZcb3chcOylHMEr7IsYSeY8icBg8hBeVRp23OpIB9JslbOa27zpMtNIiex2amas' \
	+ b'1hYLvqnX8BI9cFT2phIQm2pRHRyjQ2h4KdDMkWyIBWSKDu69WmRk+5GLXFfLN1v8xhz05n43vCHoWYBHOQqfoQTx0UCpMDn//Bhm' \
	+ b'r1Fanq7WMkSz3hGA+PtPvkN/yR0G7PjWutqplBtq3PMHBKY+bT+39NjPToYF+LT19Gt15CdvTLnCfJKwhPgXgT89yIWHYoQLOJ6s' \
	+ b'HmLtJyPalJBvl1CFm/3+0X4Lrg2/n+dR/Rzxxe3dvVHN4zECHFa/ciYd+YXnEhVU/spxZ+5ymeZd1PuVf+gy2s/OgpxD9pK1uchC' \
	+ b'FLUVPA2xN9dXcQ3cqtc1eX0uw7jkWPePfq6HlVP0AfVS/e9aybCl10cI2YrNm9Bcf0HDJ8uBcuI1F4I6vCv0BoFCbfvpzP6A9m4Y' \
	+ b'o4plMxlR9N2m1hSbd8DY+kjK5InuZh4uFc7UYSLlTSil/DqaTIE3s8lFyI70JdJOhI7nKZZ2X+TEQ1em90AuLy2tV/74U14p4JEB' \
	+ b'MuEhcfbbxs/09e541CAUhFqk1DbX+aFYxs9LIsp0Xpu3X9+qmYn2esMtWlFW+erw0ohZRiXYAFbZ7ZxtjvIuSVi0Nrd/ljDkRKxX' \
	+ b'RfcewSODVD5r7tcEYlAKbHONl6bWLn0XjHhQOF5pyFlSbdgm3Acbub/J+EdIqAXrFDg8O6uYTMMwVs+tECNVmWDm7SUxRIe12p1e' \
	+ b'XG4qSoROBNNXR0u7qi/McMj5R6L8u3Xfq1gOM/Qhnx23DrTIyvZ1XEuiM9bk6qb9U66Lz4Fd46Wpqk/tv2BbQY0fgcBmvI+X16JN' \
	+ b'JAP7f7IiHq+/jnKk3pmq1pVeSFcOd35SpdbCROOTdEq+Mw8TeXTSEP0vOzXRhD0D4xQ26Jjkgy7zBGnzu3z2/r1NRYbOnXXqdPDn' \
	+ b'W3LP9FwNgI0UoaNm4/FvnCVQBWjG/f92JtP5ZKlSrfbSQMapl5/2P1NnclNGDPeV8wNhzXIUlHAn7vg1aads8E00661nOCHn/i8Z' \
	+ b'hJFDtjtVvNn/HbFTw1ZZv4Xgn3P6Hyj3/5NJN/WaK0XAgYvmyqfr4yQwoRy/35p9RGu3f5LA/8X5YaUg7FatzLcN18DQoK0iUmdw' \
	+ b'/FJN57vHwqm2u+yvs+Iy30rV2RDPNyLdBarZ5dD/IVbPhPDlE6ZzRV43dGdLPz0DldyBYC4K2lnuAkX/lCPIf1G5Z+6jmZKMWHZW' \
	+ b'UsypIk7RpbHiWni0fIBvhDrdGja6FJ4jevqIyOZk8anyHj62zVZyyK2vsvZxqAAKq95rC9/llshJsHUazTgfL2N8M46A3hMVN8zu' \
	+ b'+g6orNboq5P5217evk1TX5wEu4sJ4aybvs3S/XXPqZCn81+QBYVyC0ocnB39jYVPl+zWQwdPhMwKx9M6mq+wciEkOKCR1g/g58Db' \
	+ b'L8TVo42hNgGa1fWLU8fLXbmCv+UfH4+/FRf+Fvij5VA//H+JrhVEjvspBOkTsAbhbISf53ngnHZblHw/24JOmKbyBOXdzVZO6/Kq' \
	+ b'ft6PMcJh+aFXYfw26Qm3tLOHzQ/eDcx9/x1QPt1bD0HQ143N9pfN5poLQtQHNgSuNe2mr0YRubi2z3cPAojfFDmYKXhkwGZLsINw' \
	+ b'DSNcD4w/f8VgFNv4m09BenFbuVRyW8sQPwNhd5BQvzXEX/tkd75jGDj4C1EXX0enOKRIEnBnQOO9JqNq0+FSJAiPsZX7SGpLuYHU' \
	+ b'vfjyYlzqkpWAw8D8z2O/kKLyfELiyBrN+ELNnICjwaI2yah7R7Bkl1hVuQ/8mN58ELRMDa/7WB6lFfceJ4XfkQRyJcgbfml9LSbw' \
	+ b'lQIlvVjvtJHeKSVNsUM4NG6mhvJT2U1VhvITnvotOE7BacjrJEpChhgqGvweGJ7fo0Rmlb3/8m9htwMLln+VREBEIqHmXQygxGes' \
	+ b'XtBy9BGSpP8rQ46GJmnYYP9KoTH+DJCVuC3dPBto3tKfJv1mva7BVz33leXR72b4bDoHiHM7JqhGE1RpalcX/4buPlfFgraCibUN' \
	+ b'CADklhUHabyu8nSPgv7ffu04OL9gOAOhgdfSapmlQjZPO3ZfhS98PxUI7/lf5AaMISChQe0TDmx3yO0vcWQxITkSdC8Jag8sM/U+' \
	+ b'f+M50+RvxiyX+jXyrhGZRctBhkitgD5r0t3v4lmHrDXu+LyYq7je7pApugKIpPfU3W2+zMgFkXM/3dYQ/+b+OUZTnv3l3vwLnkO/' \
	+ b'T5aJZxKEqvoM6I8Vo/FSUbGQFgg1REMw5fkhCOU+wo0Vrz8WE7fQRzGHvt01fNwlrOnwcDvv1QIw+gE/caqDb/5VvuD/y+9MJdgR' \
	+ b'ZAYmeVFIQQDmy78TeDmscYrww+/V975s7zaPEnMffnl8LF9bkraj1VT1bhLStSq0lXyPmpmM2513SbAQrUr4+TFLW4MeQBmX6tT8' \
	+ b'5Ii5XM+EpJN98O+Bxro45mqNXfKpFuwUp5AOw81BuH2Uo3Ov+QyjWkkpqABUzoNHT+kU+QzULZ04crBwbgFJ86ez8w96N9kDKzmP' \
	+ b'lEEPkqpTX+noQYQWuaigrah+bb41IjNi2gaPst3/ipBzZgJsElgqq9Z2kPvlpvC+hKDugeqIGWQ576waWJ9PsfTntH7a8TLNepG5' \
	+ b'Zbe1f5XvXZuw9LSHFOF68Bp5aXFyk/puRBW6b9IY6z8w2EK5apXPxymIzoCB3jbYKOFa2gZm6lMJigtdrxnNNoz5mVbryH5Df1dm' \
	+ b'fRLGGuNU6k+X/cTN1r85RpTsdG7H37RX4xFJlqw/RpyhYvg1v1TvK5bPb+9VWhmjBd463fblur6T2p75bvgTIG8rG4HJr37/R4RX' \
	+ b'05NeunU/sgC47/5SKxYdCGW9cNnPJubv8Ei47fz7tUkLKW/qIAZLs8uIBh5gfH+Hb7BZql2htpWtJ8miKxPEGWJBcGenhSZ6kDAi' \
	+ b'KvqH45cr67yT5ipDIoKzO3+G79TM3dG7qnuLgkk/mp9IrJTkxXRNul9oBg66QLVRuF4Pf4oXeO/pl+Jphrx69HXEkn3yRqrFw33c' \
	+ b'Y1XWeJJPFJP+Y6jO7g5WeNfOybV0xO29fYhyfGmwoSpsvfLGLCubo9MWJ1cdXNvsFbgewQfR/5w3JdasnlwvuJSx99MJmv/Hey3/' \
	+ b'PmL9Sc3gm0fvvu9qlHzx+CtyVEisXPfhU+nSOpMf8+K73iWK4k5ZU+W3Ptvx0EErPyxJqlH+Ov9Ld7mSzBYrC6Eft8p189fCYcvd' \
	+ b'zjQQwxrxZVUITgnm7I3KAl8fQTHzK9CSaHN5BsU282fgz6l0nuNCPrftvn0thBOL4wf4zRb/TivxZCtecjnQLlfVvOHtVdhrJl+V' \
	+ b'U2fMIjfxfLGLRty9b6+T3YlHYYyaqO28NDWHCsoroBhog1hAhdEZJdXNqeC3U6iLy2J0mwEafGgNgxi9es4RDZLX0iWRERJXZb2P' \
	+ b'D2oh3yL01+90dEHHcuE0c0cOUGW5wG8wjOuYGUYT/Rg+NYGgisNAZ5lKMoZ7gUf4qFpCZzhzt0d9Ak5n0OI/HUVMhtMGmDNkG6iY' \
	+ b'1II9T3AdndWA8exmQXjOydLjhI3/mCGxNOE272LLVr9ZE95/jJCex1R5PySekb4jfTLDnfUD7v0CvLbOj8UX/XZP2xKHwO4QcVa1' \
	+ b'Whho/J+m7/w6OvV/tJviUashstlgiDpr1Nvcm+ZmU8hvQxAwoOOhUQscaoZ/URpIl3IaREqMjbtX8B70db1NL+NJ7GZd1vmQJKhx' \
	+ b'VTov6o1biVwOJozQhxvdZuje2/9OO3V3PKYFC8YMVtM7xCmjyl5b+eakYeMMbOtRRjxZrbKBwfOeUnoJvg5U2GiDOaQ55RT4HqvU' \
	+ b'Mgmzqz8KP0Vwvwn9snSyk2QYsULQlS4o2nsq7SfT3izLQnSo1znNL32s8wLpfdLoPAL5GnKtLyb9j1wvtj5YnxhFb9+gT47mmMrX' \
	+ b'p3Wvr7bjshc2S2ZdZ5jkZ3AZXrzFJFpqxKE9Ske+2fjmWMSNB6tck4Rv3UljQiSB8Q2XpsjMRqYW8fm9FEVU0FqFWVsofc3gP/Nr' \
	+ b'yLlkXuIfv+D2Uzd2j3TvSoiHWIeR3VezRaLJQuplOGLbCaV4N7THsSyiHsv62b92JEVzpiZqUhpGQiGl18zoVGTgBkW5GPoRfAtR' \
	+ b'w5Qtk9TRsUFB81ZGIwm++VNySrTM3zYgdcZAs+QPy/HW8OywT8husb8b2A22Qf1Yxjdk3FYa6pGk8Idvfk77pVJBfomMRoVxJRGZ' \
	+ b'S8GKn4P+Nf9EiOlvhGi2PXxtxEd1lfPzY+7o6uBzOepjESrvnyTAKj4HqoBUDmkw+OExTvkk2y0/jgRyuojYl63TBbrmJ4pS6wN2' \
	+ b'gQ7RIrsaBpbzfewg6mNZE64lP+5oo1L9BjGWT4sc0QcQzdCuMcoIH4pxM0/jkf0Ugk8LYG6hjxCrbiGvaY1IR68cYeYOV1oxFP7L' \
	+ b'nbRPsqjQlwDGCDu6talvhJe4Joo8DxUN9xoD459rVkMzR71EzoDAr3v/609Zgx/exKZJfts6e1Xmd2qJtLXx7sLz0AqCvJ86ifar' \
	+ b'ved6lrW6bcsuqFeQq/u5MjkWVDyt6njVjmTvhmtGrNXZmQHAbVWyzm4+nXeeNmBCtuoeQhzhZlFIkJquAVStwY+61nTquFgGRLSx' \
	+ b'lmyjNvJCgEKrdANs3+jFtKHKmtPGax0okeh47Nf8UM+bfUbCWttONCrLAbwmufUgbd61cfh9e5vRq+knPr1ObS7K+IgPjCUH8/lD' \
	+ b'HuQvK4jhNktoMs8aNv3jEePAln5gWDZZyNxDC+opnz7h9ccdK3ce+UjTuZ8EgSG78qO6Z2vX/XFjeZv7RlEYXp53BeHBw6Pj8xc6' \
	+ b'8RdPzZyKc/4vZLOjILWAg9X72hYtTCF0YjFXLjngNBMZTPrt68CXcFwaGhfHh9KYJAkw/ropnvIFWDqA3eN0oj1tvUOY7PdWRQcX' \
	+ b'MOTEEOsqxQ/1KjzH6N6XoBDxj48Go2z6x3NaMWTIDIibedIcadg7Jlf5awgH2km9PeiwINpsjCvgsoy1zvzY4zQCxIMVWPRKT6F4' \
	+ b'FWNYQ8nKkMekvcz1y0vg346UYafp6Tbrtc+z4K9gj9HtM1Pekxy99f1caemfWD2eaccyLD28G8hbnB9eb8lIK8xodrqWx8e00lbP' \
	+ b'gwA27gofp7ZzJQnLrrNL25oIub8jF9F2+niuZFLxykYWVEk+/UWDPDjw2wDS+wIonQtnukD14ePg928z+9eowbJZ8Nh9LGZDslav' \
	+ b'V/Bwyjv4VRsUY5ou0hcwMWgA8yihqkri4TBtp9VoMATaLBIQ+hwl+CHDCo2bD4ux20asrZmKp54MpDwzz0U3T7+MSi4VAyScxvtF' \
	+ b'edmKSrM0uUgnWZQEuNZh6p0aqVsASBjEh7VpujV6hiwvYPL1OsUyKo1qkuNN9HM9OQ14WQZ6x1VOmvNA/tmvGSqIC/kSTgdu1DdP' \
	+ b'k4PwWUrVnbH50itTml02XW8xvY3gJIH2aVpHX5Ek4jNIx0NNPxvckNtswGKh1ofq8Z1EfjfUo6vNVbuKh03n6ilz9OkLNj4tehzp' \
	+ b'eX94KvVTY5g+Kfs9Psc5yWd/zJtp4PkD3Uk5HprBWPEI9AN4C+MkABt8oI/UYU2cgVEB/Ff/42DJ+P78nfGCw9X56zpxAu/O4pvm' \
	+ b'b1NP9hERkpC9KcynLg5XTJBQaksOV7tO2X1fJpNinRLDcXdcsv0R/4QN4avrPTgp7vp9hgrj2lR5LqAduBQP3tNgN+GCA1RICdqw' \
	+ b'qqm0AOOB0eJ71loPVm8fqoYRrd1ngb4UHv5DH1S2mNszvk/FN+3zWYSySjA03iXhbHjlS/QunHNb4fyMXSVf7xtNVF7rp/JA5iSp' \
	+ b'cWGQ5hIvbZFxvwxcFrEEbtj6vI0Q3dbvaq0OFlw/TSQnZokEQIAK83FEYmJGdcTYHF+GmJYsFyIPjGpktMuAIPwsMahZlA1MbUxT' \
	+ b'FxXO5FshAjqRDry/C459/OfBtAEtmLW16FuFvu5KmyC/zJkGcBPOsNMJDX0F8PJo1zw9QC6jnMyLWGYzM1N4hrRrU+UEKghVOpvI' \
	+ b'nCAm92cKzGkSFxXo2fY0w1xwP+aTx7UErCxnQTyGIMqbu6lIbs5zsTCCaNGTamTiPwPpDDy998oxom1hFerT4rvEiZHT+8HrM3j8' \
	+ b'z7+XgmEQlaERrPvbiQQUZXwS5yE08O1nJK4mBekspJRGgN9EPi1QqOC3R4yBF/o9eD2K3oNiWVUHA/32M579mhCWPj0SxtPpu17v' \
	+ b'fw8kPa97QUxU/vvbAh2okzN9YvRzcgwLUacOjE778vQWTU7y1J68nQKm1N+LMC1AHE/9heJRQki7fm8C7V4b3wgoJsY1ppKnbSH9' \
	+ b'yvAUpdKWxv1VTX2RYv1xDNQeJdQJzg2V2gxaQ3i2MZuND8wVkcWeh4FDejuOh5HDV0bT8L3XJEXgUo/y7e3k9PzTTa2wnJRFZiNw' \
	+ b'Efzt22U/Fvk/htCffFDjSf1ubWifAPH44qyPyHLp5Yre+VPIDi5fOf8kHQx48HkqsDLeNqzk+qW5J0K2RO6ZyyI2Sh9s91gn/E2n' \
	+ b'vziKm6K8S4FRvMneRfg7MHbkfAQeRCA9A/VVnmeh9Z7leYXPjMQHgGRhAw0LV5pz81SiReDKCpjsGR/5YL5R7vD5Bn1TIxEEOd2B' \
	+ b'Z9IV14LLVzLvjlOc0yt51Lbe9WzamVYYa4s3zIYZ5PErn6jFLO54pGxOJ+sO7MwnkF3znKakwHxiWiXPu14U2DV4bnW6RuWsTiM8' \
	+ b'ANIfaWjyysXSjlFrvkUi7hZgUveRv+zsLVYUForETaPrzbLrJQOiQvXcRr3gmT02QfqWIZBu152zqnmTAt11wdkrM+WLgV/QXgyj' \
	+ b'UNrdE2oXsSNsB4G8qQlHUtdGl2uZXyOi1/2jAHq/NfXIjjdIaxXZnhkw4XkyzC+3OY0QChwgX7QBv5dOQMtEVISZHqPgC8+FrlQb' \
	+ b'bOa8tlULWjkr8zyczlLbJ9o5ZUaYOCzPCFxUPELgeDIZsqr5q0K+zp6JFZpUUk/bG4LsUVP1bti74PbLZlP5HS3FMfjOHx/g+j3H' \
	+ b'FqqHiIscdPp3bV9cRRFi3+xiseuA8MQaadWuVDCMd85NMK9nFQ0PmCnN6jhMZmoPQQ50yueiLpNy6SqCbururTn4TiMMiU56yeXZ' \
	+ b'0l00CuuFzDP3fI0fiQgbfFPTol17cTc9KxYTdV3D2qTFLLs7bDnM/usofNmiDz1eO4Qa976irsm7YoKTkq1QYcpklRxR1MerPT1a' \
	+ b'RWtwtS9biFFLLZI/ZUD0s0mVAY8TXC/Db8Tf7ObImXsE8gqho/OqEAMz1MM55nnxgpqfZP+TwUS1vNgMFFUQB2DNsCufdMhKUQXT' \
	+ b'YaRPAKsO4DrioVae38NXVXA0YtFl3OXzlLCSpObTwjHqAzikCjO77aMIQAqPHEGZr+/G4z1kbhvtqeInIAxRexZL/jM4uoPrfTvP' \
	+ b'bYwjNP5N4Ce6LT2t8o1HNdGhxmB4Ytw7xrjqF32Zbv3IwOKt1u2WcCV87DbBVdqibVivPHva3mF988pOty6nkmVqA3IuuhO2xEzA' \
	+ b'YiOYBGLfI19iY6ysf4lhK0vZqxgAn0tfNHDymUh3sT568WJKY20NTyAqDPbYQZOpRZBxeSwkMxjhkYuwg91xK6qjTFF38S8IcdOm' \
	+ b'I7klqeTRRhwskgSaSBYdYbliDeIy7OB4syt6KDHzazCxo7BTzHSbj8uvrcPpQ3Gh4Tqy6mJYZhMBuDraksjr0b8e+zkV/tc4Cr51' \
	+ b'a6n2vLCPd/WHYikeN7N1unE+J+IvjfFNK72+ffzMMfJRpLx62N/spN8mSdwogj2/sIaRkg1T1vbkOY2gXAdi5I7tcYvT9SgwT4/u' \
	+ b'TWXu3faelvOdl/pHza2Qgz4bzzzyXCJ5WbKUVEDf+2WJ0OtkkjNOvziKsW3YztlNNWPMtek+C+BvNUSZeZWJgFpNAHqfE8RD5HJS' \
	+ b'xcn47lcf4OoNMP4y5YS3verfN1lC8+b5tN6zRtKOVyMoWhv+i12jQolqOua0W4MnAUzWnfzm1sfRa38rkQyOERRlhHlXiY26DrfX' \
	+ b'74wRMvERFQMp+7ob8b6iSO1IATDN9AlPBRlDxL29nPsezYn5BTscFTdtDK0EkpdY0j+wc4LkZvV7dCAicEbkoAFP3pQ6x4lQVclc' \
	+ b'rtHhQe0NWto0Dak5H6Bc5Ma76b2UoUIz7aCW7jMtqwcuxzIHoO1+lsLkM3LzVha2ozUiuIuQ7vG+rxuYOJ7Wfg3LAjAT1RJXa5IQ' \
	+ b'/w96R4joVoVnpBqXNvsSQpxWVp9Qmot0V91THvL1v+1UehRZ6PX8+vHbnGRXdjouKwgwCddFhxhy/ENUTfvtn4Q2q78ZELt5s8bC' \
	+ b'3SoKIOD5rjSCYJNt/fO6fFd2sfDWHzhpy5j7Ffg1H6lzy/QcCT77tL4nT0Xt9Zs7dbI4XIvkYomluSHpB41z7R2dIjDocG86TiG+' \
	+ b'1Ivdb7Gva/0lXP5iWnQ4mHGgxEeQr4aVQEREe1pVzeillr/8tNYuXszwqNZ8lFh8cMnAvXakbxa9DrEGjs2iE/SGVQKZ84sHooAH' \
	+ b'cHEZ4lzszVNg2UzoiDrk5Y9hOfj/0dbnz1ZX+UEfZXD2KdSDHnamXqkAWh6F1IyAn4ZoaPpAxYrb+RzM8/U+tRDPtWgWywb3QBeT' \
	+ b'AFnib1rwRfsHUvCKE8a54VmWc4Eqy5huDPUNe1bGvjLYX7RXs9kyH47+E2+jIdxLDZVNl1Ci2lsLzNtVnMbfp/E2inNbG58+y9Qw' \
	+ b'fbgzuV81T15IeVydZlL1eCBPhDFupLwXJs8ICg28ig5L2CJNj/31mBvQ1n4GtHcBiYSK6BkeZP7S/33yhog5CaYALTgjKzoPvAq9' \
	+ b'wXQa0A92padh4JW+b4lPMsQzbxSFqvj4UpT+5PdEUIl9GZoMCdcRPie+BSmzChnOGDj2j/zo/ARwzs7cN/DDtUr6tlsdfx2RVTQ6' \
	+ b'9/rHkh9iQC3QGiYluAHzYnQ8vNKdNcy2ivt9pj8qjInWd1x/w7Kh5TJInIpWkXeIl62Q5/GFKa0tEzuxcJijQA9UNEs9uypReCT0' \
	+ b'Aprhf7L/pTz3UxqPArIRlbGTUectPyZMYVBm2nawfH65nsr/q6eEOYsVli4W3g2wdftBHnF+Kp+IvjbStVyXYOqPb+E254WqwB+C' \
	+ b'16djLtuuFMUCxpelA3LV9q5/G6e50HMuD8XtGfgplE9nBzbjxuRFfKbLXoTJ8dVlCl8dV3uXMAubA6iEzO4ZKOw+RcaEWCqEQKTg' \
	+ b'fb/J2HdSSQrvR07XScgfsFb/p9X9Ed8LBssUuyk9Z/7qjV6VKoPkwghvSFnhWItEXMKVVksWQGYqTa9l7IJgsUiozK2vviBNL+76' \
	+ b'XCSN8VjwIyyWC815d2E0x6WlXEGINBiXn+yRnussBXJdsb5YEelq7o/sP7BEUvfUD2X0KUinM84lBFP8gvRq6jeKHB8FQC/EUbDb' \
	+ b'Bb1nG0Ra1alzraZN9gDB4LStoy12h5CodEiUMrgNu5hi2HJZfmFmkmPA37gUPFalUUynmLgIOAPV0vH9ZG/BstTg6OOCunFLwktS' \
	+ b'1xfRgYKZP/cktqEEUqZSFgarnMtg401nLngfTwUMo0T4hv1OWX+Wy5G4G8maykaA2kfoWafOoim8Mu6t01PR7rERZpm6V3YqIk8R' \
	+ b'bPvApV9ZIDxRsAoOuYntx1ESkY5MLIDeHXTsUIkmMVazFp6NOTXSyjC6R4A9oAsx4yRZQ/rs+Opk7dh1+VbWJZUzsMhTHDoMJMP1' \
	+ b'Fw3QORyBHUApl23T/0sb02u3FqnRz6KRwCGIcf/TD/yn8iXIXUMhW7XL3icyz7qeX4GRivqrjYHjy8LElg5qZOY3KcFZskIBFDDA' \
	+ b'zOKYlvPdVRk0Eqr21bulufrZzRLhcPhtdL1v4spJvrfhD2tnNzcz4KagrVyKpSb5Sh9yPZVUYBBbu1yWH8LVxX/EJCYqLSKRtV3H' \
	+ b'8tlOLzTrylhVN7vPd9ZV2QZd++VsyGmZvfmvb7u3riAyYBvJWuHBWJRHFR9A3S80iwa9ArXZ/MuglHc6CjGLxaQ5d/wTfFGQKEa7' \
	+ b'HFOzA68tEA0gToQ5aNTLCBgNQkUJPn3ETMy/RKrS2jNjKpcNmF7AafPuF/jkvTSF8/8QojQEQq+4iTd6NIE22nkCSyH0XIxx3eX9' \
	+ b'W3lRAEhpIwjrJeAsDmSPSr5zXm+BK6fVXwsfUjHQW3BsSCBbVpOBVtgq10I2NN85E7dNiOxFy3L/Owhl6vxq7ollUfwMr9afuCL1' \
	+ b't0JTO45TFWTSmBZYm9Rbxy4v4HoqcmUVJ+8BW2jumyNvcmCIJ+VBgiM7EGyeEOwK2kJmKEDAjAafJAmsuJ1RLtdDgZfxvI6SHTdt' \
	+ b'MbRurowjimR/r4NxDnjtYogMBGRF7HjX99+hGyl/2e8iwAH7a2UfSe193iOtSN3zziQye5rWz11aSoNMl3jqRl+ukr1zPlwDu+R1' \
	+ b'QC3gaYca8xKlRuvqoe8Lljd4zk5zYAj5UIVQ6gxTYflxoWax2FoMi8QZOHInbuOENgHYkqSi+UgGEKF17sewskrPPksLKXZYFR44' \
	+ b'oF7SMIZqyBdHzHCQhKFN50MRDWvSQn4ssurAQDqd8fDfC1DJmHK/oIsFgs3+kFSuVhx4X3W8fMxN3fZ1fj5mqJBvz3K1kCsSZSwa' \
	+ b'yENL1BYEErDGJbRyyEr6J1BjKLuh0d/VXeWtRMCpJ7DpHtibxahZUz0QfO+xQUbpyI6xnjl1kuQt4Ke06P2OlO0QTFQ/L83Gft5V' \
	+ b'SADtLms8VnaFkA3BKPo+QMmdMe09elYdcoAe4ZprG93z+MItj+d+jVYDOOzUPh97SuhqHnVnFTM8KJu4sEsxbtimWE100cM1XHLr' \
	+ b'7bdPd/lfwWy/xwQ1XP+4jjXQnMudpVPtgTNal/NA/vDjaH5Bb4Gd5aLp7nLDLtSZjiQTJC0oAV6vg+wXrIgKVSa2F4CT7hXw1u61' \
	+ b'hbq2g7xPzYsH+Xd0Ta/s81MLkOhxeExkYsVrZu7ZNZnrxrIw9DYhwVROJk0/XJ8jsH3wu+5ldyfqu1QSyfddZ92YfysRWHsOgmxR' \
	+ b'bytZv/CltjGrSRDOnUZxsms9VO6GVi9GCnFTS/8h7gBwx15aA/ITBfh/IcLr2brPBPH410iIFaAM1FGf4QBgM111vwKRCdbjcuZ2' \
	+ b'XJ1Lx/TxxazMYsKnsjn5SOuJb6m4iIdvEHU4+/um9viOEEHgPLXBU8gheL4xJnZDJw6M5uEuEmcjjRhLiduAdFoGYM3s5zJLP5kd' \
	+ b'Pee6cmPoHoeGVr0XNUTx1vvSrpY47Y1O89ozFGtt3j7/nfPfcjufcG/blgaqjBbDDMy99Tcfd0EC4pjOb+UiwaZEY+8eFckimY4w' \
	+ b'pvobPzCgfavtn0GX3M1CVL4eAXUjJv1D4MfPz+mrzpIkbrRHZn7VXIQWFm8BsFmAVJW+Yh/MdMl6t1b8kAPpG769bUtxsJmax5Ec' \
	+ b'rtd2q2LhBAEAIzQBDTzpnNc39AGHON9Zl58zllZqG+R44bTxhQvfZluW4ugDZaozo0NsSFIt1Y/f0aXTYcQ73DjCxeRGzX6+HHzS' \
	+ b'0KCmfqC23dhezI+Rw9NohwUqjuM/eB5+8zsJMYlrGcIC3O3DQ8ZPZDOYcR93xG7DPMGl7SCBbAR9TXQfmgy8ce+L16YSGYPcNRMG' \
	+ b'pEO2SKU+OD5i5gXU+iPB6gC0AuR2AY3o0B2F0J8vI1DdfX3zrnKFy6Xc8bFJVoLTBMANipzuDZCgbmOowQ59Hc++Jpsa9Dvu7C1y' \
	+ b'6plyjybDWjpPRSR4/yP/LZLm8ukS2hDh/Er3JWSvDcD1fRg9gK16GaP6QsSt/ft5XrdFOi4/Plc1VHTicwbbCh094dYWm1XTYC7u' \
	+ b'Ljj2jbO/lR01uvE97dAM1MoKQkUJ6UsyUs5HvCWnxblJxZMqcbDecj217/eECiSTlg1xc1JN27hc5hrVr4yPLtwetlgkS8tmCGSo' \
	+ b'wl1BXzT8x4aaZ2SgmRQN8hwcpYsCK9RZ6zgiXEzjCnIDz64S1uKz/7r32ViPSk3JwphVeggVQt2G6cxiUFAFVIky/n9zRu5bK8D7' \
	+ b'iCJDt7P1Umiu4tBsGktW+1VHcZyYPU8VDtPW4x44D4gWlViACnE/q+iIn7LNaM28b/E07SaI+39AuKPOcgh/8VAzNDDmUnD1i8SP' \
	+ b'SssRfK5tZaM8QWDBR2MI9y5Ugev4BScqyKnoiWhnpsHiVQLk29Cd3D6Y9u0fCsjYuHyzmwdu2H9DEUgOGSbYkBguFxZcqB5/VFKD' \
	+ b'KM7IKBhbywIIxPzxa39h3si4xfsdF00T30g+V4PoDv2jAMG460mBrk8BVRhORZfp+pjft5Publ1+5qnsCsNLcENOVAXKeBAcAGlB' \
	+ b'RdxDOCALW/JOvyqcBCBmywlXLu6vzCbtFfyHARZ5K1hZiekW3Ou8kwUslfttuFaAmwLtr0hUpxGisjGjKRatdj0Bb30YhWBd1fty' \
	+ b'sO77xhRvaKxhRWJ3eUz8Q+uCj654BTGY67e9MbIMchXAFDmHNf5WzFxY5VjE2ARDG6MOfc+uuzvp7QLePROYf2p9PQGFBz545z7s' \
	+ b'f+PG8tirHyiEsCjh/WyAmGdSC+v3w0VPaA/9QjgWhFL31pD9lc4RP8ktx6tfRpkU3n9luSiaY7diFBYjqb/h4QeQ2PE0w/fKFvUT' \
	+ b'fJjCSrNt7bp2p1zoc00w6/D1ciwOai1zGkvCAcc9lnHRXIqgW3yuxapLtTwsaaewVJ2mr+EcGbRxpYXsoKmZIWLXV4qhCgExyhQ+' \
	+ b'PVY2UNlHzIkNSJei2k1HFvNhl4QQQKsJVOzAC6ea+sM00S6+7J/bnCu+Lu18Up5eUALiSSrkGnrfDewXXfjndcf+ZYdUmWHgTTxd' \
	+ b'9jZxo30NzU/OdMSWq+wMeyBeyojoTEpOytRVHEHLri+7nxX16KB05hrKpmV/N3rK3keWrzIlx32OlRuwLx+KdqwG8mSISpcfztXK' \
	+ b'HPHtQSZITVUcrqFU2YBgb4CLaVNONr4D4uKZbSMC35KAHx7FvZskcwTm+l7fVtoqowCIGbgoEmhRN/sSxlWLt3GtWY19npLfg5BJ' \
	+ b'HEKq97XOSw130CKfj9M24O7C/LwHCYOWYnc2a1jSvo8Tut2xRfN1Ai62fb1dBc65YTlQkjCQQJjg1LLQSWYaOwowCTqAqo3fa/ma' \
	+ b'b4dTw9VDkSeQvt62CxjAGEoKD2zGQc6LvY8eoUkgdgEMhwWOW3kFosO072xIYyPGH5K90q9LrVqOUFjRNZnQgXlebro1Qf1Xs2hY' \
	+ b'PCPk76tlcnGVVUnA0WJrcmtW44mwafpLiW03wVMnTwiVzw/kiKpCrXRUBDfdrGFQVFjRv43hul6kDdQ37j8P6mR82ciq9PYBmyND' \
	+ b'klpY9nu7q2tV02SiovEFWLWq5F4j5fjaGFeV3x5vbfui1F8XgO1KoO2vKY7y1Kxf+YPQg2Z/ndHzcI3sjDQidAUJuFt25VYRA4Mw' \
	+ b'q4VvOP9iLLXAwrX02K3hlNRZfvHYTLkVKy8vg2mwHp3P1FiD3zEQ5etmHkMUVVkRhWwDkpN7NViPwInMveBLea8MUaX7Oe9F3TLA' \
	+ b'xZsPaOYTawo1yg157gUPtK48dU1wYns4RQg26gw7n/lEwtialc1DpepLzwquaq9lYN4qiair1uvs52p15BHlxxOuMrNCCoyp0H6f' \
	+ b'HfNuHQKCcibE5QGP6RHy7vwMrwFjcEzb1/emKJeghr+EJQglKqLsK7JZzoxy/w678EqUHbHU8SVI/kdMiuPEdPGsUjwKStK+6h9I' \
	+ b'b2Tk9aarQa4/NYGT21ORM2wD49ERTaODiEakQtoZyf6hyrnOZGroDvW4YfP324xPpgYwsJqFDDeTJmWTum0em9nNZ2U21yl+sD9N' \
	+ b'i4qid2imVmEAgIehrt2Z0OcP/EjVWZjgtccGGT7GAJn0YnIiT66LUSTJeq4Dr1/PBrOwLE8wpawD+8kKR4drIMX3wp//G4BGc+lU' \
	+ b'/LlyGxmZC9KQ5xeDIehCBl5Zcy8kTzRqqqaJGipMPdi40eCDUHIXRZyALwjB18x3w2mXL61/JHJCOkYISj3nkorb61Tvl2e4Vnrr' \
	+ b'K/Md14BfdYirj2B9rOJLKiEYEEJI8ylgmWJnfhxWcwwi5U3Va3GE79dcbo/BHsigqCgY8mMTw+ho9eOgidjdvwuvAhGTFSD5k6q+' \
	+ b'ZyykR3EYILsleYav1oBc/P2HvG51umspDogpCGjw7S08GoFJHteMNt0BwU/JGu4zq6HbCvxk6shxiYXGZAd+dHPbAdKVCozkvrDF' \
	+ b'vHATeWERjR7ixsOGDOD5VVIusNvqtAEA+UzF9wvgDFRLNy+syAcSOSnpDkAXR1HkR2wHvDYEyLLE/dWMqoMOdjBwp2ulnsnnYKQ6' \
	+ b'3+t3xvS8o2myhIDHIpWe6lEA3HGXp1We+R9vfQDZRJ6vdsb1RTi+K5YmeZFp+OXFxMPdKha3U1c7JxYMKCrj+zRlsBoYGvQaVTtF' \
	+ b'Wrx72KeoRzivh0ZP/h/nUt6QsVf4LEP4g7byS1vYMAMv0StXVggCG31xvF+ao8JorkxG23k/7uq5LgrOSkg1QhFZGbN2NuVStuYC' \
	+ b'RVWnwXPsq1f6OlT9G2hVzZ6y3c1FqmcsG+Xh3X/hjO32xz2vVZgy7ljMw+d0X5kwd20Gzh26+MdoTowneSpIwdy0fWzMwdTJz2Oj' \
	+ b'40hqClTdl4MBVSNVCso1YUMxQ7GozxorQV3oswlLbF4xjrghG28WTAUG1VcY9SqkSaGMGwodF9dBIuD+BHN2NS9BmCsXHduWabKl' \
	+ b'DJFJKJ399lrL9eZtes4trVHsRyFRmihiYqgWjBLqEH4djMpETRZ0e9nMseGn+rFJ9dXvNMu3TZmS+KSG2LWRJNgdvwRmbddvSLWG' \
	+ b'11ZoDeKY745nc+/4nkOoRylYjuq3xUYqKhoMhW6N/YNeRssDBmscCuUXBMq/j+Ypsk4kLId6KC+yCB9vPYUhuHJdem2Zh7IqVFHg' \
	+ b'p+OMjHDZhh9qHfFWDSCYjK5wSfy+wfWmKXE/v0sNRbHNuR1tZKILG8l3nNtH6YlovhZcz7Fycy+ehDXdxib8SaMNZpI2eqOOlkdw' \
	+ b'p3iPaK8uF2Kyyhx1MhvvPi3MyDRJe5hBXuyJaWDTeX+p9jVR17JJ1gNjoUfELn/RHvOghaIb6d9er3ma8gePJ+1A9cDM0hK8tnT4' \
	+ b'RXesZu9Fke0ndyuVSkGMABRTlNx8Nwo+SGbiIgB5vTLSVNzu8Lpqoa7U+nafbXDUbfmIH52HnuBdc7t0e6rkrJYe//ed6MRQ4PTH' \
	+ b'V+rMRb2cGposMyMo3IYCmSWnVNnbm6Wnp9n5Ndgo1NKDlPhzOYovQu+gFe63F0LMww4syTomtPLDb6xAnBCuY/TtooiaufEK4PEB' \
	+ b'WTZUYamR2bUjfnBbAHzkJ/mYazgZrf/MLWRR5gYUqGw2wULp9vpHiFv9vKN6n51tXnujFu7aBwEFQT7i2k0WBS8O3kjS3f5PRSt+' \
	+ b'sLoqTvQKxufoJtFn2mPEEtePJ6ClMhGsWtGgh5ZepjJHP+WPC1EjCKPXcnJov9KTC7Z9TL0OPTw/6Tov8MThbk3aqU43tyoTaLna' \
	+ b'YOQHCB59JYikSpcxwBqbj1rLwG2t6WVuqoiOf+dJsR/L96dGML5u6Fz9sT5lQoJy4QHitwChNDlx9eaTCBdltWgzN0kDdEwcLKzl' \
	+ b'IBpZb+cpTbn0VkuPmubhUA30DV2iEjXXsZKxa4vGL70d1WxOKpeUdIU2E98UUUYGGKKdAqLyxyrzfQJzUTIY0QcHSntxDOyyzUW6' \
	+ b'FMul5Vboaeq3SHX6u8DONaGcZhxYN4w4S6M9vd1s+8+6BUe2AZzdFbT4ug4vPSN5Evp7FZKFrzcbMAGy22mNbqjgyIpsg6DKjtao' \
	+ b'PIgDYWQHpCc/LRNpuayus24tpgkrEwxMo91KfDJhVOa4i7JXqOPZQGpbK1oKE2y3X8IWcGtMV4DEG9vjMPfKaPJ5ZUcKzZGCA4iA' \
	+ b'yVJWzH3tyujKhHuQGASGCGGxdhReVvh8Z5+iiTMsvA5PClAKkNjn5lGeTGOllnGcYN0FwznpNaTz/V2DwWYWwR4LqAVcbzuMbjql' \
	+ b'DMpy74HhPqcxqeXtbhuH0L+6uSwPqdLzlzvixN+IwodjoU1Ikp3t17AsZ0j3NGNtierSh9mPCot75Nsr3+WTMVXNwSzCn9nf9zwl' \
	+ b'8DD/Bv5XxNVCxkzq6RNKn+NMf0kTCKKJ0GltIa81SE/bdaU6neVUPzDySnBugGtztSC1wxSZTHWtHjsAk5/fSZVHcvj4tfXeHoxe' \
	+ b'/3sP7nZlmnU+ObOpCdksJrgXNOKEx5RG5bhT7I1wYcWIZfGhkihx2k/WmHGea30fhmE7PLyrYW6I+fPtptwbtlvHtGfVo/9T0BJl' \
	+ b'jHND0pF8BWtn+9caMrWqIqYIZmEC681APAA/Jr5A+T693kuAvEIsPdvwShMaAljxLIDhvG2O240IbnPollbTXDYip6T2HNSpm1xr' \
	+ b'5AFEdLwZGwKxUEVv2o2PCHVJWJpa9zAAFzvAYs5ZJnJpgfTapJO6uthyq972PfQwjYt0GtXbOEN5z4vzna62OHDPGgN1LFheY+YS' \
	+ b'QpavTiQyX4SXxLywIfuVUVpi74vE/7ras7t2A2ajOiwlx7hZf93+DwuTQM2jy4sUnyUE/wyc8qOxsiP+EhVjMv7cmIvyUpCoTkBW' \
	+ b'US2qREPA+oItOFfIJd7Moa3tWGgmCwffDl6UdNNzwQY0W+5fLM0cj4AIsITWBb9uUndBH9D2egjvep/irqjmSHE4RrjQ0yPr0o66' \
	+ b'9cZkHxTrOZee1tWROqUIoqvS0UI7JI5Jw07H5Y6Cn2yyaAV3jkVRVumMePpOUzA24JqeL2iflU1XllMzQuJrS8psRHGjOMe9EyPa' \
	+ b'/NmGYo5d97CjHmjYsIJZAkMhVWZLjMyhbi763maumSICZdE7s2k5tpFM47mzG7r6rTQGreobIMcAIlgtaon6aEFBB6+MrqHQ7Dfz' \
	+ b'OfXAdGpXAp4U7pzzhb4MuIdOynYvwpVnXgm6RCjJg8GzqWdFNNN+Sz2iYKAs9nPw6H95I/Du74r+4bgy2hxY11bbYdUpg+WsZKjy' \
	+ b'l3wz9ZtxhOfvsIVS0cFzoqHyL95OBBt9909rf6gi5AI/xMxtsqkX3x3c+NeDQKA551BdZGwvnZmvsO5Jo/hgZedO7GShXiINawUr' \
	+ b'PfM/8o0mFK+Jd/SuGG7xDWd5upwYEfxTZqOXGvq0v0eJBZGW0nteMSJxCvQ4VKSf/Kfg3NGXMXalJm/BAlni1bxeHqlSd0imCs6f' \
	+ b'enYvpQrGpFwlRBVCvBsbdq+2S6VOidH4p0/OnwoTrfUWPoGnIXF7fQuUymdxl+hQ7gfvrNZBX7nFS9GLcsCp8yi1CF7jN/gPFcHu' \
	+ b'kUkusm/J0zpq7v11chGBQhcSnvazipPuuo7lCYa8DcsRctuOVLahN4YtsO6cZXYsAi1wTGnXoKJDQ5DM2hmgSHymkyQ8g5C+uIQc' \
	+ b'qVQRxMGvqBAMypRd7dq+KJyZGvkVspnR8JWIY7wXlRz0n93A5IhEs1FHSHjUhOl4qqe+x5cPdOhqxNdgdjwBawBuGs6XS4qCT4a3' \
	+ b'N4v8/gSPv5uNa9m5iLd3dgxRIACBe7DBkHdH02MTkrTL/WsOXQHUWzCbp2koih6CXyDTSHVmh+bPPKtnb/gBVEENr/Y0oNHhpfky' \
	+ b'3t6ODLNcmCbAk/Ha8GaiDVgLiidgVkWp/rpRSitSwRxrvqlIFP2b8H13/PR+Fek+Nj3t3b+waqSMsvc/PO66GfzSGKAp8bfV3wdD' \
	+ b'ka3vrBihveLesHZLp/ph4zxGRLBthQq+toq2dhy/WCC1S4gEispD/iQqbeQM0TvoWI4u59jIsgkkwUx+cIGTYLRGlGabl+T8urvC' \
	+ b'zjWzIy+wZWcSdA4HrtljgGGnBizosXO5kaSpLBeIcjMgoWG9M8Kj7tVBQunn6mC/271EIatyhFNM+uEg9sBQqFvM/fy8jgrvsRa2' \
	+ b'BhqC9A5MTzmJQT2z2AZc2Skw/3KFmaT8WXNEz2XcABS8+l5GKb2yb/gPQAvzV8S6W287ojHB7cdtCzVVECtiNiyvdl1z5+ClQzrN' \
	+ b'D6zAhPbY7JN3DGFPeDdf2Kx01oO1oYVfj57UiESxI9Bsi9uKpJeDL2MJnhtM8AHYQkIjRLzJm9W5ZzM5e9pSpz64sShhfG5f6Hng' \
	+ b'0gETUeoNtDBE4wFA4B+jFdtVbgeqZQGMdMoxejtBx2UNomPpFqMyPp9bMunkEkQ8JD7Qk8PKveivIHjoPnrNj+Oivz5sb5u1vvFB' \
	+ b'vo8g9Jl+N+jUNaRIMNblrcRHCTIqyEvRMoKwYRtUKCATbv4oQBYkWfDR9Geqbn/nT/VnW1CsN30kutpmEf0Sxm2YBqt3qEc23Ypl' \
	+ b'EY0aDuiecC9Iwi1yA1knkxAlyQhUmniwLIhgxzmY5+8wkYFZtaJoCv0PCjdFsexo7NjotFhZDPPW4Yz7PdAN68pqYTxFQm0A1xaI' \
	+ b'uI9Ao6HyqhbWlfkWu5fy0nsKcvIsfBISYq4BNpG64qOSsEAcSTj0+0zFHCKVL8iaKi9ev0Ks24cWVNdUouV/6lf7bOBbBCFiGad/' \
	+ b'jQcaeHVrfv+lrhSRyO/1CUiHUAF9v5L8RNPLQcZAxScFzSX57MS0taXUb+sYMJERc3G8x8f1zGSd+JWIhiF2whFDwdflCmCkHdGq' \
	+ b'PjO9URls6u/cOluZu/dzlGEP+ZvxIBREcddk9oOWe4bF5ygMhMicZ8Ejsytaczd2SUyD4XWbY3IKTmxDuQeM1zbXtMKhBxYhQAlU' \
	+ b'qjiMrTN4K6Pykg7jSVIkF9wQu7KA6S81xnpWTJF6ytDUG88ujXw0S2TleOZzU5rg7Da+TotZSbrtLQsfiYzE8abpUgse1nG00rcJ' \
	+ b'I3a69FdPMIjgCRkSDtLUvZMdkMDL8iqgLMCPOE2drsyS869q2DXAyz/TcVc9xxMRu14voEZRk91S2yv/dIlRmyqENdWebJ/gmz+z' \
	+ b'TfumsaPgybsnPh9h77XbIovDHKfvI2tqUTLI9h5XOxV8qY2xwyBGgFMFswllU9XRtpZCFQsRpH/lCyAZsEV704lZWHikMfE0Yk1N' \
	+ b'SuwSMJKVV5Vj7sOBDGmOscVpglTheKNRnzxSG4avp8y3ehCpdWMYt/ORIzqEd5Lw7mU5M2ujg4nnQxrpWpI1JXFxy88zas4JNJvq' \
	+ b'5/JQUiYjRR+LcvtWQD0zLhG36YpjG1C8sPLPobMWia8OsJNvdd4JERg+nrl8eZgclzn5yGmNPoNra7MjoRZH1j5lj7FPpBAvC3wY' \
	+ b'mHHvjl65dFjQ+wOpPJekmRHRBpMi7QjEAcylrd9ns4/gMpqMh32iDfxlo7S8G+++IzzMvd+aBaygbEM/bN9Y/sqjVRAxiYiansGo' \
	+ b'E6l6SVTysirdVOY0Q7vbJdCmyqy58ZtCprhe0m0kkg35m173Y06e1tK7lkWgWve3p0JoyMMHYu6ugPiwSRw//oC1pIFH0GPoT1ty' \
	+ b'bF9nJknCZa8uSODWh5wrvQtPu+6Kt3prUucuGKJNq7LVKObtHeplXV3RWh8AaF8QBNWriU5iQmG8JNFdJE7UQYhZ8IDehQ5flTk6' \
	+ b'GLk6PFITtUQbhsG5rBRVunwPdJzn4bjkQa7YupBJbnlXrSnvc4bWRbaWnYHQUN3Y7vao9Et9bfecU5GEvj4Amzk6Ubx7azExxVGq' \
	+ b'/1rdt1GbkR6fzLmi3ZGtiioCw8G1+gq+bOxtccOx/pP9KUmG3Ug0kygrWFhizawsxCMm4k5sWId4UNKRgPqfncmMvsyDgb6OGTf5' \
	+ b'qvwaoyDXHSNQu/4443lQeFNub3ZN3NnvTTZIPaaziFp2ODR8zZEwFm0mIRx7Aaa0KWrIIwwo0EC0+hXNyKvbGHkNTJpNgfXvx3E7' \
	+ b'Chui7tv1cEPp5ErtrSnqNco6Q+O2Si3m/MvaUxmc6P6auP18MvnZp4Yse2QDFD2kfQDTdjEExp8+Yd7gwDxm6eucZUWOpUeSHI18' \
	+ b'0j8e9ZkW3du89dEgVDnIySQYDAduCHjyWp97LMXOHpbjz6N0A8LI/sjAbogg1yf7INa/ADbAdWWZMqP31A7NwiOHG5OkwHqbtDWc' \
	+ b'nJ+EyQHvlKnRg3ya5lRKRwFFbsaB4jZXo5sc6LFahukq84sP4X+1qyutIt7cQnlc76NmnFRIm0bzlQnVoYkEXjeevxNfIdWC14ZO' \
	+ b'+dze2uHxtji8y6rr4Hyq6WhGcf4xqL13+FpIIXCCqT49SaItx8g/n8kSBlqEkOenIID3UBmjAntXZfcCOfKyKNdo91aLahkk+j05' \
	+ b'VdzQ3LMfw4lPoXUKm1Nln8KMwx2PHcq0R4Js0YkDr2w1ybuBLOSpfKYVf9vX4MWM4vZyaHHbY5KKsixfD6dwnQL0GzNaZhgs9Gcw' \
	+ b'I1OmPZyCa4QNTIuiEc9rTsHokZciiOpapZENER/KoIwRm+CY6zSUh0Xw2m3gALjUSKMe5CeD1FIVfVFJxd7kECEdpVKg0/pNspVo' \
	+ b'0jwchv4RfP6csFOPMN2ghrALgJ9Aho/nVsHZZgfhJ15jDVupyVrHhgUORmWTYrrmGOl0tBKmae3CMQMf8WCHxFM/EcDdzmNmvgl8' \
	+ b'wXVzhnAHMCSL76XlUJdY9T50ZBeDK2ndH+YerrjpvzcbM6oEz+Sj2xFns4b0PWjhiQJ4l3Am3K28rIeBtUIBmbzGPThUwk1zAQBl' \
	+ b'/H5376UtUSiQVysSb8kdvgprixOO7cAZG40Sl46AvckQPNOvNr+1U6eWK8fb8AhwKAh4TNSTFHTn5Z48/5fLil4i3rZYTcwmtwyD' \
	+ b'JnLMCoxXlELZkFGSudWvbEXxwnkoo7MCuIkDIca7aJJqhc1cWLBXcXhCsMpDTvVZb57O1hu9Q+vj8UpB7HbR5AZ/1hHaGsj9+Vjp' \
	+ b'F2bdotkRZ4rfxgjFZ4wk/+8PQ3PHZfLT8TLKyqQLCoDWX5ORiawctmJe8bCtqc6JWV0iTvdobuIegf49fEsWeC0xQDDKvh9M9rbO' \
	+ b'm9vmNvQaYIsYxSDXk/wb/i3ZYfAKnfpDtN52EXuKxZcQekBdGMjHOGz6PumCevOqDPNW0oPjkrSJGe4iVTJJKY2PKoI4xLAiNYN5' \
	+ b'Q504mXKTZCD40E4RKQ1hhwIVYCwNusrhwrOD5ZzvV2CxWn95es6KCsUBJAT6bWz6mk2fPrTzZsr9QjaocxsyhQ05CnYDxNyYuE/6' \
	+ b'1mH6c6rU+472/sdAvwrgNg3C+RQAClBs6OcUgvHgMiyAsD/y1ZcXBcrONzfx9VyeWrr1tRyfdiPYRDkYsp1WWLY8Xe8tArFLkDtj' \
	+ b'82kOdldSj0rfhzaGUkUYoGZFEmzxjmpWdNh2ixEbKFqrHNkZgm9fma5iqQ7ZHNfyYiH/OXLE0TbyriECEft3unLmEKzMZ7pHt6jt' \
	+ b'L+Ko36SfmhXQwTcqok0NRU37qmEKud2cpbG8N+2pdo9H6Skj9lM05vzqm/1l+sw6kd6TRSdjqGThMJ6NyVDBJZMBKp6oq1F3ksyV' \
	+ b'ZKWuDqmYBk4YgwlH5B8SYbm2H5YiQyHf4kpp7YCT6v1OxLUjnWWcrOYegbQXKRKvJdn3/ZQfho3vjm/aZfe/g9zUXDxm2kT4jcX3' \
	+ b'HDbcc5H4KjY0ySvKSnIgv1/Bit2ur9cRbdH2P7GqoTQ7LIaGag2rglWAcvjp+ef04m1EddgaGEzKflehi0gVGhlkYO/7glmsQws7' \
	+ b'AOZCM2kmigt0LjCLZYCpMIvTIlQ0bQ7Cxkyj45sxXS5kxYz5Sl3yjXcmOYz7Hr2xzwskWPaP7CNx2mf3wid+wlsCAPl6EkAyYJDU' \
	+ b'BCG3JEGDSFgSTEFgaE4DDIBROJBUIgQpZBSAaNIpGD+dATeCfAzna85pQPhAmQWJkYvJaS6jYucIp82Qg885ZIkd4blmKyJ1BSFq' \
	+ b'G8XRXB5TBHNiJpuY/7R067pZh79tr9a3Qa1wl7AWaeNNNqVENjRXt6eNYCigWWlyc7ve7/ktjF/awGAP8JwliGUpPITsaNMZW4w4' \
	+ b'zNhV8Zk542T656btrpZ4Vuh+WuMzSkSDo2hPo6dWVkiYi0CZr82jluYLMRSiaDCMZySwCp+XfRzzvAplXZ40NyB3RwqnKgs1BM5Q' \
	+ b'W9U5C8lylU9OgkpmQ1Xl8eCSqjr3WB/GtolkVEoqoD+nTBEwcfTJPH3LMdtFHqKJpd76yqJYTIY2y5QKCkzGAft0Ixs5YFRLY4sA' \
	+ b'ShBTHTJrh1QxxmoguOt6U5vRyxCy9ZthqfcohVjRyjhFaGT9Qte8bv2KXJLkWBQFreqppoioaKMh1fQMUBQJIq9YatHr0o9UqEgR' \
	+ b'KzsJZKaPCGmFkaxoMj8yZjgsEMcLWEOLp5IiYw5cpGg7eIj2dTD5Fd1ePUQob7MtZFvMn27OTsTFbJIsSMVJ3haSmanpMcHa9apM' \
	+ b'tp7spViVotyaeKYgsAya6+ehK+lMZA0rJQFMtCK1jSl3p44whZkFRPOCjnKh/Rm0dK969FBXrtp+bJm8RsIkZZZSapIHkiQTf5iS' \
	+ b'e5jSrJOVBTlJCEEVBiziQ64hBXILSDBaOHOchyPAEjadLnUceCku2GcyYZuNaeMpI7WlRYPU8Z0kFoFMEmHmseci2XI3XiEYZJgk' \
	+ b'bincipWGIYNxS3CkBaD47gLQwLTPbE9VfT9sdGI37jIf+OVw/6rYJu2e6aIhYxKKUYvZscZ21R6e7qks+bYSmDwMcxZvQIolMnWn' \
	+ b'MeAcxBMV4SoI0UjwMoIXwo3s+qMDwAYIRzcqAcvFzz2JZehL/FJgtuQNG2rz7/qOfXyoal2Oznv16acv0RvGMq60vIvrIiQaEhCT' \
	+ b'5WWLfC2IKWpgGxoYGd0TeVlsI6U4kYyWZ7j2pvO9HxC4xSgY4GPMxlmQbLiilz4mzaQtDEqWhINwYt7y5c9rax1mP+lIkGiNuur3' \
	+ b'S68qCuhc+qplnhxMJMQQghiWaQtLjGWqmx2T3NaZUD+3YFgGFOCwUD6EXRmP70xI5D1r0kKzOFCCRJyOxREtxrlNSV73xTlsBmMX' \
	+ b'y5pPM+Nsym/DM7God7pq0qGmLJ9WsGCwWLraKwv4XmN3DON32yaziaeiruRI0KdTAz9Ai0i/Q42rBrkTaA8pJJiiNZx6RDh4QloV' \
	+ b'wKVyAEB2FF5flQRBngiDTPTfs3yMXLSlHvhxvMDXJx7dDBmVw2k90LVygTE1Rcnsbwsrck2WIc0+Ua2uIU2fqECaYnfbfSNTPe00' \
	+ b'ytr1BV283qmfi1sIjGZl0DcSstKVmitCM7AhMo2QoJwvXrVeMNCmX3kgtiipahRCW9GhYM3nyfUmK4PmPkK/txoZvvoqOU/f029f' \
	+ b'NThnIMILSpdtAjPk4wjAhDHIpusv2fDyOkWnC1SjiKeEUlw3soK5Rejnlg8GSGgbaBJgjkkjEXO9WPORGLSoTVLnBjcIMI15yXZF' \
	+ b'tYYvtRSV4gb9C7OsqUpu1ilzRCipqnXhoWEDiQBGgKUH4pEDjtiPNJkTYQmCxGYomOI0LJo7cGEZ4wImSAEnCZCTuiU0wakUhuSB' \
	+ b'JwlU6IA/lweKv7N9T32Vke9tb6rbCD0sNuAf0aOPQ76jQC1OTo4+MuqyXXNEKUKyAczNNm+kshwLfFGBfJECgKnyJpyuE17BAS4O' \
	+ b'ge1VfLmYGJVm9J0pHtQJD992qU+V5lEmZR6uvfMoSXlFYBA/em/n+JHVtEAQMjRFlNAdIh7xqkoHEctyo657oQRv1yhi2jw7Y5QY' \
	+ b'cWs2oiIlf8ijIpG7g7Beck2j+fFSd4cKqcRZ4rJuFM/rqA2WEQ9R+sZCxicgoHFZDzAGgH+UDXUkIuWuCPPl7IlCIHEA7j0Kf1Qp' \
	+ b'/kR8X7tGQoM4mg+6LD0K+YpaUJ6Ku4LJa2rNMX4vwkn182XBAyrk4Ke2yO80VF1DZwBq1XaqP9UtE7HfkYNbsv506T+J9vvJIFLF' \
	+ b'v1NaymGXG3UBRoPruxqphqlOB8DUbsuROAkmYFHmMZiR5YCAJ93dWpsWxiMRWnl9kSDS0mEaZsH2VHS30tu0AcE6d4KUnWO6d0lO' \
	+ b'GMneTyF1j0x9yD86ggEBPHqV7DWKpZ+TSI0QPHaj45W8PaEzHzKHXsyMyUxnWkLV/GtibTuuZVIYArZkryfGYjYyWdFEQTjMmmho' \
	+ b'bMxP2CUXxtDdmsa0V43wHqqPtv76M+nLdwgqud/50ke+LTRO6bqRTU83htFy16xmdljPYYExSb0HZgkFy/GUBFpWzozxHP4o7BGT' \
	+ b'LlrUif8jZrIV6Fd4T0nD+Kbfbg+fQfnnk78Ia2mGcnkZclpXGF5MLGTcpIRqH1UReg+kUZG4VHzzNVrs1lahQ40LErh11xZiRj/a' \
	+ b'pCrKqRWQxaRqa+2UI6oOE0wVID024Xdqr+XypBxDxFQAOsKXS/4QJCItnHYmxPBXwv8eANtqE69HoKhUiSLwl6ehCJd1JVUjjd7q' \
	+ b'zD8plptYnGcjBDaOwl7mUdtqEBgPSUUKcGxlsBq7pYPuB7AUN7Z4i08DtWh8dmS8cfb9vV58TmVmN9wyQdwlKG5y8mLpv4nojsxC' \
	+ b'5RrR79BqGh+ae6ooysKnq85jFLUeuRfTVRGQnW3w0EHP9x6/BERBvG1iu307+lGOp8cydG2qYP6M9V/pNtUk596t2pHRH1vwfvMN' \
	+ b'xQX1bfhWsWkyfGOP//F3JFOFCQ21fT0Q'

background_pal_lz77 = \
	  b'QlpoOTFBWSZTWXXqYsUAACZ///HkxMR2cnIjc3l5Efh4HAA+Hg4ADwdHAAOHAwAD4cDAMAEi1sOemKeyBU2ppptRphkm1Bk9IGh6' \
	+ b'hoPUABoGgHqeoBzRg0yaIAAAAAAAAAANA00NADt6AU9IPUzUTTBGjCYI0GCMmTCAxA00w0mmDhKqbbXV5hqoQOnC9Y0oocrRy6yD' \
	+ b'maTGpVkHfswtoPvKJSQFF3JR2/k+eW4SmhtQynr2qacBMixDrGeFyddakl+IvR09SpJONXFu15WgrEnEwVjhA9DnFPnLMmK6MwhM' \
	+ b'uPb1EMAV6ceBO5fuMDlLbiE2cBYVNqjPOPLbMwYQ6B4xCEAMogssGglEgzSkgFJDWBIlI3mMLKcrjmcZNT1OxACQcyD+S/BJzp2X' \
	+ b'33yn4wG+hDIWGazh9o6MyCmstZBAk0xlNSTFCzFD+54wrLfleUqahtCqqivaE/Pfs4Q/g0PpQDigp/7936eG1tS+ov1JIE2vmvGu' \
	+ b'FyzwJgKFFQGfKQjCnKVmekjzQY4NwgER+gYIKyRQnrZFPiuXysAEGDwA0RiWDSuZoyjQty9q1mZdu23RCoAY4C2lGW6pnEwAEbiQ' \
	+ b'94u5IpwoSDr1MWKA'

font_bin_lz77 = \
	  b'QlpoOTFBWSZTWVsXYv8AAZp//////6//3/n/7//7u/tK/8/+3fKv/775+v7Z+/v78v//0AP973eb3O6be7O4PZvFVP1MUHpo0p+m' \
	+ b'gITZMjQ1NkagYNJppgDRMJkyehMQ0GmRggxqZMaJmgmhppkZAwGppptCGBlNG1NNA0zUxlT/VPJPU2pmpP00mnkhmoTeqaY00Ixl' \
	+ b'MnpNHiBPU02mgB6ibU0zUwjGpoGBHqaGhhADRiYExGATRhMmjCGJhNMVVP9JiKbNTxFPyKbaU9T9U9MU/VGNTaNDU0BgTCM00Qyb' \
	+ b'TSegaQaaYamR6RoMQAGaRpiGTEYTJpkGmmExBoDIMdPRkCGEyAGgDRoBoA0ZAAAaAGgAANDIDQAAAANAAADQAAADQAAMk1EDIKeo' \
	+ b'9I2p6mgNAaBkADQaABoMmhoAAAAekNGgAAAAAAAAA0AADQB6gBwAoYEhFy+QdBLKIpnBVACp4wRDjmlWLGqAQQtSY8EAe2jibUfJ' \
	+ b'fqMajDBnA6wSnYLc22BnbwwF9xGEAAACQhAfITJTLoQQA8TMykUakVFmB7a6pJpCLsIEFJ6txsJJDwoGiAH4kg9hIx/XkeCyPAMn' \
	+ b'dCUaRI21nRgu4/JH8Z3y6peOTvITzB6EILdSpnm8Fzl3qFObnQ/65+9x8Ff/LwMEAIjj8aBTIyE5OMg/eyYviE47I4tg7v/E46vh' \
	+ b'bcBPsyk0YicwkvSfWHLLWnzG65aUweCn540Kc140FrS6GJLLAjStOidQ71gS66Xw5hBNDhCoqMlFAx6gQLwe1wNPHlT7X+nyNpdg' \
	+ b'UXdycZNa4BbgMI8y5QowQ5+Rd4iNHIhaF0b0kSSBudpgbIk3hfSMGBIB0Ej/guboEi0pP7kAtNNizhQE9tbCMIYlnWgyQ5R0fyQr' \
	+ b'cNSZJYcji9bucDrjEtWeDb2NBFO4ARAa4LkMFs1QQttotSMJcave7FWvIRTiNJGjFBZp7BKiOBbVa+nwIA4DBvSRKw0qzFogh5ki' \
	+ b'yBWLQ9aLULNk4549fw1KawOkCANuWwEv7rV6sdLPzSSVAqbGCm8jxMqQ0dIQOKhq0GBRfQq5gFWgBGoKYIOAUBFEiMBdqBGvJTWA' \
	+ b'+gxAfbtyI6oHHULXB4hq1dwRKgyi6uFwxbWOVORTvf1BsU+2D9Dh3ntgTehivJsUPpnlgCKYxOEsdI41a5jAkJsZcceg0NoZun28' \
	+ b'+LT8ktc5OhuKrCoHEH+TSpK9sgosBIjyfU3DztkDyiRbPItShzE0jKRYgT/DEMHpSzjJn0qHyIMLzpjKDHG4IqGcXCxzNN83GaDy' \
	+ b'Wq7O8fjGFJt/0oTmfRRtLZtAZCSheIBoMbTjBK9SAoAkhawZ9kjWu2zBLq7SRMBjIMad471kgzFTUxj5ZpJ8P9iYlPzAajXSF8nr' \
	+ b'U+yhSwoAPsq07xsLYv3ORuzWqRqdf37aPljPrr1slgpmXYjxDwkhVi6N0E/QKaTrq1bCSzsx3g3YhyB02olqvGpOvEPGY+JVXDb3' \
	+ b'pO8yigAcye77KUBFqW6iDOKGFMEd4gSfWygPx+i2Wl3fi6KJWJRzmIWRZtiNTBHfKLxqBfzlysghbIqyJx6pXuda822Y/1cMm+4R' \
	+ b'RtNicK8krH4ReWkhpbbs3ojROpt9oXgVydlZd7tcIrOwzv3VzlJAJmnRjS1bDiTApYWKgy9rJeVAMBLiN1Rsd1q1bC2q2cXFaf2Y' \
	+ b'SoxEDW3+jWzVEtEAkTTFQDcpU0bTYoaZFT+IbWizGUCKRKQh3G2N6QSWvEkNCISEkFpDuEIJLE7CEkmeQFUBAAoEAkoSSeogIIDQ' \
	+ b'+aMOAQx7PBX4I1HYCSZCGyY5kiQ69wbBzoDNXOV6WcbcZLqGKyefh1YduamOTKlUXBwsneuxEot3n1iUbwLqENIkUd1jaJVUrGpn' \
	+ b'WCmvj22zbCz9Mrs0/WXRBPpdMEgQ0wanRGBxN7XCGTdYx4RRCRIgEmAQCEkER4IoEMHkSp9bcUMAEMRUuaRU00To6wxI4GKVOieE' \
	+ b'K+LplRHt4tErFOAD30eXYlDZP9Pp+3uhTCul8YBZyov+dlji28x80EzztndEusv0IHmbk7xvQyx78tsClal1aBlvScHkvbjwJvDm' \
	+ b'I4bRc2uT9339PkbfcMDFJJLia/2rDoItDClK8EFHEImWoUVyO81yxIA8ABlIvUXxv2ssHfF3JFOFCQWxdi/w'

font_pal = b'QlpoOTFBWSZTWZdPTegAAAjK+UABIAABAAgDwAQABEAAAgBABCAAIppoNNPakKYAA41xpEFCRJXxdyRThQkJdPTegA=='



if __name__ == "__main__":

	if os.path.dirname(argv[0]) and os.path.dirname(argv[0]) != ".":
		localpath = os.path.dirname(argv[0]) + os.path.sep
	else:
		localpath = ""

	parser = argparse.ArgumentParser(
		description="This script will assemble the SNESAdvance emulator and SNES ROMs into a Gameboy Advance ROM image. It is recommended to type the script name, then drag and drop multiple ROM files onto the shell window, then add any additional arguments as needed. A SuperDAT file is required.",
		epilog="coded by patters in 2022"
	)

	parser.add_argument(
		dest = 'romfile',
		help = ".sfc/.smc ROM image to add to compilation. Drag and drop multiple files onto your shell window.",
		type = argparse.FileType('rb'),
		nargs = '+'
	)
	parser.add_argument(
		'-e', 
		dest = 'emubinary',
		help = "SNESAdvance binary, defaults to " + localpath + default_emubinary,
		type = argparse.FileType('rb'),
		default = localpath + default_emubinary
	)
	parser.add_argument(
		'-db', 
		dest = 'database',
		help = "SuperDAT database file which stores optimal flags, patches to disable audio, speed hacks, and sprite follow settings for many games, defaults to " + localpath + default_database,
		type = str,
		default = localpath + default_database
	)
	parser.add_argument(
		'-dbn',
		help = "use game titles from SuperDAT database",
		action = 'store_true'
	)	
	parser.add_argument(
		'-c',
		help = "clean brackets from ROM titles",
		action = 'store_true'
	)
	parser.add_argument(
		'-v',
		help = "verbose ouput, to show patches applied to game ROMs",
		action = 'store_true'
	)

	# don't use FileType('wb') here because it writes a zero-byte file even if it doesn't parse the arguments correctly
	parser.add_argument(
		'-o',
		dest = 'outputfile',
		help = "compilation output filename, defaults to " + default_outputfile,
		type = str,
		default = default_outputfile
	)
	parser.add_argument(
		'-sav',
		help = "for EZ-Flash IV firmware 1.x - create a blank 64KB .sav file for the compilation, store in the SAVER folder, not needed for firmware 2.x which creates its own blank saves",
		action = 'store_true'
	)
	parser.add_argument(
		'-pat',
		help = "for EZ-Flash IV firmware 2.x - create a .pat file for the compilation to force 64KB SRAM saves, store in the PATCH folder",
		action = 'store_true'
	)
	parser.add_argument(
		'-strip',
		help = "strip headered ROMs (.smc) and export as headerless (.sfc)",
		action = 'store_true'
	)
	args = parser.parse_args()


	compilation = args.emubinary.read()

	# prefer external art assets if present
	if os.path.exists(localpath + "background.bin"):
		background_bin_lz77 = readfile(localpath + "background.bin")
	else:
		background_bin_lz77 = bz2.decompress(base64.b64decode(background_bin_lz77))
	if os.path.exists(localpath + "background.pal"):
		background_pal_lz77 = readfile(localpath + "background.bin")
	else:
		background_pal_lz77 = bz2.decompress(base64.b64decode(background_pal_lz77))
	if os.path.exists(localpath + "font.bin"):
		font_bin_lz77 = readfile(localpath + "font.bin")
	else:
		font_bin_lz77 = bz2.decompress(base64.b64decode(font_bin_lz77))
	if os.path.exists(localpath + "font.pal"):
		font_pal = readfile(localpath + "font.pal")
	else:
		font_pal = bz2.decompress(base64.b64decode(font_pal))

	compilation += struct.pack("<I", len(background_bin_lz77)) + background_bin_lz77
	compilation += struct.pack("<I", len(background_pal_lz77)) + background_pal_lz77
	compilation += struct.pack("<I", len(font_bin_lz77)) + font_bin_lz77
	compilation += struct.pack("<I", len(font_pal)) + font_pal # this one isn't lz77 packed (too small)
	compilation += struct.pack("<I", len(args.romfile)) # number of ROMs in compilation

	for item in args.romfile:

		flags1 = 0
		flags2 = 0
		autoscroll1 = 0
		autoscroll2 = 0
		scale = 0
		offset = 0
		db_match = "  "

		romfilename = os.path.split(item.name)[1]
		romtype = os.path.splitext(romfilename)[1]
		romtitle = os.path.splitext(romfilename)[0]

		if romtype.lower() == ".sfc" or romtype.lower() == ".smc":

			rom = item.read()

			if len(rom)%1024 == SNES_HEADER:
				# rom header is present, it needs to be removed to checksum only the rom data
				romdata = rom[SNES_HEADER:]
				if args.strip:
					if not os.path.exists(romtitle + ".sfc"):
						writefile(romtitle + ".sfc", romdata)
			else:
				romdata = rom

			crcstr = hex(zlib.crc32(romdata))
			crcstr = str(crcstr)[2:].upper()

			if args.c:
				romtitle = romtitle.split(" [")[0] # strip the square bracket parts of the name
				romtitle = romtitle.split(" (")[0] # strip the bracket parts of the name

			romtitle = romtitle[:31].upper() # font.bin is upper case only

			with open(args.database, "r", encoding='latin-1') as fh:
				lines = fh.readlines()
				for record in lines:
					# CRC32|title|flags1|flags2|autoscroll1|autoscroll2|scale|offset[|patches]
					if crcstr in record:
						db_match = "db"
						recorddata = record.split("|")
						if args.dbn:
							romtitle = recorddata[1]
							if args.c:
								romtitle = romtitle.split(" [")[0] # strip the square bracket parts of the name
								romtitle = romtitle.split(" (")[0] # strip the bracket parts of the name
							romtitle = romtitle[:31].upper() # font.bin is upper case only
						print(db_match, romtitle)
						flags1 = int(recorddata[2],16)
						flags2 = int(recorddata[3],16)
						autoscroll1 = int(recorddata[4],16)
						autoscroll2 = int(recorddata[5],16)
						scale = int(recorddata[6],16)

						# the original SNESAdvance.exe builder further transforms this value before writing it to the header (undocumented)
						# https://github.com/patters-syno/gba-emu-compilation-builders/issues/1
						scale = int((scale * 0x100) / 0x64)

						offset = int(recorddata[7].split("\n")[0],16) # remove any trailing newline char
						if len(recorddata) > 8:
							if args.v:
								print("\t", "Patch:")
							patches = recorddata[8].split(",")
							romarray = bytearray(romdata)
							for patch in patches:
								patch = patch.split("\n")[0] # remove any trailing newline char
								address = int(patch.split("=")[0],16)
								payload = patch.split("=")[1]
								payloadbytes = bytes.fromhex(payload)
								romarray[address:address+int(len(payloadbytes))] = payloadbytes
								if args.v:
									print("\t", hex(address), "=", payload)
							rom = romarray
					
			if db_match == "  ":
				print(db_match, romtitle)

		else:
			raise Exception(f'unsupported filetype for compilation - {romfilename}')

		rom += b"\0" * ((4 - (len(rom)%4))%4)
		romheader = struct.pack(header_struct_format, romtitle.encode('latin-1'), len(rom), int(crcstr,16), flags1, flags2, autoscroll1, autoscroll2, scale, offset)
		compilation += romheader + rom



	writefile(args.outputfile, compilation)
	if len(args.romfile) > 1:
		print()
		print("press Start+Select+A+B for the emulator menu")
		print("press Select+Up/Down to change screen offset")

	if args.pat:
		# EZ-Flash IV fw2.x GSS patcher metadata to force 64KB SRAM saves - for PATCH folder on SD card
		patchname = os.path.splitext(args.outputfile)[0] + ".pat"
		patchdata = b'QlpoOTFBWSZTWRbvmZEAAAT44fyAgIAAEUAAAACIAAQAAAQESaAAVEIaaGRoxBKeqQD1GTJoks40324rSIskHSFhIywXzTCaqwSzf4exCBTgBk/i7kinChIC3fMyIA=='
		writefile(patchname, bz2.decompress(base64.b64decode(patchdata)))

	if args.sav:
		# EZ-Flash IV fw1.x blank save - for SAVER folder on SD card
		savename = os.path.splitext(args.outputfile)[0] + ".sav"
		saveempty = b"\xff" * SRAM_SAVE
		if not os.path.exists(savename): # careful not to overwrite an existing save
			writefile(savename, saveempty)


