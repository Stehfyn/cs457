import base64
import os
import tempfile

MYRIADPRO_LIGHT="xIDwkYCA0IDilIDEgAAAyIAAxIAAAADEgNyAxIDkgIAA5aCC5aCC4oiB6JyCxIAA5JWC6byB6oiC75CBAOS0ge2sgO+0ge+Qge2sgO+8geqQggHrhILpnILrpILnsIHmtIAAxIDvv7/mr6Pug6EAAAAAAAAAAADlsIAAAAAAAAAAAAAA5piAAOi4gOmYgO24geaUguacggDmqILmtILngIIAAADpiIIA6ZiCAOmkggAAAOyUguyYgu2MggDuoILwv7yC4ZyDAOKogwDirIMAAAAAyIAAyIAAAAAAAAAAxIDpmIDllIHpkpTUgOC4gNyAw53hvIDDjwtbw53tgIHum6oo6LS14aiT7ZSC4ZiAwp3niY/hjIAm4piA56WlR+KYgOe1q+GUgOGok+GIgBov3IDiiIDjpIDgvIDqiovhnIDpqobDvcK6J17DqSjlu73hpIDlvofhoIDktY3ijIDigIDChsSAacK46Ie+4rO97ZCC7JiBxIDCiuKMgA3ijIDhoLty4pSAEOG8gGbiuIDtr77gsIDhoIDto77hpIAo4oyA4bi64pyA4qyB4oO+75u+4LyMGATgtIDwo5mN4pyAJNyA46CASuGcgOGcoGjijIDhiKngrIDrkrTtn7/jiIDmuY3wlLSC4ZyA4LyA8JuogcKK4aST4ZyA4KyAwrTihIAB4pCC47iAAeKMgHFx4pSAF+KUgOOAoOGggOWIm8Ki4LyA54eA4LyA54eA4YyAF9yA54S33IDnhLfgrIDhvIDimIDnhrXnhrXhjJTivIBc4ZSA4ZSAceGkgOSpihfhhIDhpIBy6Kim6Kim4YiU46iAF+OogOKQlmfoqZPoqZPjnIDhnKDcgNyA4KyAY+KogOOEgBLCisKKEuOEgOGcoD7htIDhtIDoq5DihIAX4ayA4oSA4bS2KDTihIDjjIAN4ayA4aSA6KqR4byASuG0gOKEgOGgnuG8gBjhvIBK4bSA4byA4rSA9IOpg+C8gCco4ZyA45C04ZSAGOGcluOIgOaYoeGMgOKMgOaNo+KcgOOQtOSUv+KQgOKcgOOAreGMgOSpiuKIgErhnIAz4ZiA4YyU4ZiA3IAn3IDiopXgvIDjkLThhIDqiILhqIDDoOC0gBjhgIBS4pSA4ZCA5KmK4ZSA4aiA4aiA4KSA54S33IBx4YSA4LyA44Ct4YSA4ZCA1IXgvIAY4LSAw6Q/4ZyA4byAworhvIDjgK3inIDjgK3hrIDkqYrijIDioIDgsLTCqCfjkLTklL/ihIDmta3ihIDCgOKMgMKn5pi74aCA4oCAMOSpiuGwgOaRpOKUgHHijIDipIDinIDmjaPhqYbknIfipIDinIDmkaThjIDihIDgvIDiiIAM4qCB4pCA4rCA4YiU4ZSA4bSAKOG0gOKcgOKQluiCgCvijIDijIBj4ZSASuG8gGPgvIDhjIDCiuGQgBjhpIDhjIDkqYrhnIDuoqbipIDilIDhsKvhpKbijJfknIDoqZPitIDnhJfirIDoqK3itIDjgK3irIAw4YyA4oSA6oWu4YSA4p+h4ayA4qGS8JS0guSUv+GYgCQ3EtyAwoDhiIDCiuGcoMiA4LyA6LyryIDgvIDIgNyA6L6izIDovoXIgOG4gMiA4pyA4oSA4LyA4LSAWsO9XsOpwqLlu73io53hpIDCteqIguGggOS1je2rvsKGwrjlu73puorisIDklK7ikIDguIDjlIDiqIDjgIDnrYrkiJHisIBz4bSn5LWPxYPhpIDijIDCmeKQgFtw4oiA55WP5aSBwoZw56Ga4oCAcOK0gOeoguCkgF7ipIDlhqzigIB64aiAceKcgOqmqeC8gOG4gCThnIDliILDvQh44oyA5bu94aSA5b6HwobhoIDktY3qiovChsK45bu94aSA4aSA4oSA65W64qSA8JWBhOKMgA3isIDxsZCp5Ke+4ZyA6YCB4byAZvGTuYJmJOKIgEDDocO74aSAKEjijIDhuLpy4LyM4oO+4bCA4bCAEVnhuIDipIDhgK/jnIDhnKDjuILgpIDgsIDhoIDipIAR4oyA4aCA6Kqw4pCAD+mel8KG4biA4byAceG8gOG8gHHhvIDhnKI8I+GsgOK8gOGsgOK8gOKogOKInOO4gOKogOO4gOKEgOOUgOG8gGPjlIDhvIA145SAReK0gDXkkIDklL/iuIA15JCA4pSAGOOsgOGUgBjhtIDjsJo/4biA4YyUEuaOtOKsgOKsgOOogOOogOOAgOGgoOGUgOOwmuGYgOKMoeC0gOGgniI/4pCA4pSA4pCA4pSA45CA45CA4oSc45CA45CA4YiV4qyA4qiAGOiqpuKIneO8neGgnuGgoOGsgOKMgOGgoOKMgOKwgCPigIDnhZbipIDigIDipIDiuIDjoIDijKHivIDjoIDimIDivIDhhIDhrIDhnIDhoJ7ihIAY4byA4qiA4oyh4oCA4rSA4pyS4pyS6LS14LyAwobgvIDChuC8gAXxkrCF4aiT5a2I65K06oCC4ZSA5amP4YyAAeuUhOKQgELilIDhlIBa8Ja3v+KQguKMmOGMgMK04pCA8JW4geKcm+KUgOSUuOimiOKIgEnivIDinIDrgIzikIDWtOKUgOC0gPC7p77ioJ/qgILhpJPjmKnigLDkjIDihIjpmKjgrIDgrIDhjIAM4riA4YyU4oyA5KmK4ayA5KmK45SA5o2j4oyAw5fkiLPirIDyspyt4YSA5JS+4YSA4byA5JS/4oCA5JS+4KyA4KyA4aiA4oSc4aiA4YiVP+KkoeC8gGTguIDhtIDjlLXhuIA14KyA4KyA4aiA4oSc4aiA4pygNDfgpKXhmIAgE/CxhJ7xs6Sk6KaI8bOkpOimiOOkgOOAreSIs+GYgMKd54mP4YyAJuKYgOelpcSA8KW8gkfimIDntavhlIDnprbEguGMgOatm+KAgOaRhEbihIDlgY034byAwrLworWW8oSssOWNieGUgFripKHwkICAJOGMgPCYvKPrlITikIBD4pSA5JS4E+GUgOWpj/CQqIHhiIAB65CE4pCAQ+KUgOGMj+2Age6bquKzve2QguC0gOKMgOCsgOuStOCsgOuStOKdneKdneGphuSch+OArXHhlIDhnKLnhaHnhaFx3IBtNdyAcdyAwonoqbPoqbPwoYSfWPGzpKQT4YyP4ZSA56a25JikxILhjIDmrZvigIDmkYTihIDlgY3wm6iB4LCA4oyA4Yip4ZyA6oCCAAAAAAAAAAAAAAAAAOeQgOOEgOOEt+eRqOelrOeRqMiAAAAAAAAA5YCD8K+8geaNocSA4LCA4YCAyIDQgMiAxIDQgOGAgADQgOGAgOGAgOGEgOGEgNCA4KiA4LyAzIDguIDhgIDgtIDgsIDEgMyAxIDEgMSAxIDEgNiAxIDQgNiA3IDcgOGIgMSA1IPwt5SC8LmcgvC0tIPwt5SC8LmcgvC0tIPhiIDEgO2EguiAgOGQgMSA7YSC6ICA3IDttILMgNyAxIDQgMyA0IDMgNCAzIDiiIDigIDEgAAA0IDxjriD8JGkgOKYgO2rvwAAAAAAAAAA76u/AAAAAAAAAO+bvwAAAAAAAADgrIDhjIAAAAAA75e/AADuk78AAAAAAAAAANCAAAAAAO+bvwAA7ou/AAAAAADYgAAAAAAAAADvi78AAO2PvwAAAAAAAAAA75u/AAAAAAAAAO+TvwAAAADgrIDhjIAA4LyAAOGQgAAA7pO/AAAAAAAAAAAAAAAAAADvn78AAO23vwAAAAAAAAAAAADuu78AAO+bvwAAAAAA75e/4aiAAO2PvwAA7ru/AAAAAAAAAAAAAAAAAADvl78AAO6fvwAAAAAA76e/AOCggAAA4oyAAADtu78AAO67vwAAAAAAAOC0gOCwgAAAAAAAAADvh78AAAAAAADvo78A4oiAAAAAAAAAAAAAAO+zvwAAAO+3vwAAAADMgADgqIAAAAAAAO+XvwAA4piAAAAA76u/75O/AAAA7ru/4ZiAAAAAAAAA77O/77O/77e/AAAAAAAAAADus78AAOqvv+27v+6rvwDur78A6a+/AAAAAOCsgAAA4byA4oSA4ZiAAADri78AAO6/v+6vvwAAAAAAAO+jvwAA74u/4KCA4KyA4LyAAAAAAAAA74+/ANiA4ZCA4YSAANyAAADui78AAO+Xv++zvwAA75e/AOebvwAA4LyAAADUgOGggOGQgAAAAAAAAADrk7/tj78AAAAAAADtq78A4KCAANiAAAAAAO6LvwAAAOyTvwDti78AAOCkgO67v++rvwDvq7/vo78AAAAAAAAAAOubv+q/vwAAAADvo7/vq78A74u/76+/AAAAAO+jvwAAAAAAAAAAANSAANSAAAAAAAAAAAAAAAAAAADguIAA4ZiAAAAAAAAAAAAAAAAA0IAA4LyAAAAAAOOwgO+HvwAAAAAAAAAAANSAAO+3vwAAAAAAAAAAAAAAAAAA4KSAAAAAAO6LvwAAAAAAAAAA76u/AOCsgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA77e/76+/AAAAAAAAAAAAAAAA77e/AOGQgADvo78AAAAAAAAAAADvq78AAO+zvwAAAOOsgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO+XvwAAAAAAAAAAAAAAAAAAAAAA75e/AADvo78A66u/AO+vv+GkgOG4gAAAAAAAAOmfvwAAAOu/vwAAAOyrv+mTvwAAAAAAAAAAAAAAAAAAAAAAAAAA6pO/76+/AAAAAAAAAAAAAAAAANSAAAAAAAAAAO2bvwAAAAAAAAAAAAAAAOqjvwDok78AAAAAAAAAAAAAAAAAAAAAAADjgIDirIAA4pyAAOKggAAAAAAAAAAAAAAAAAAAAAAA4pCA4piAAAAAAAAA4pSAAOGwgOCkgAAA4rSA4KiA4KiA4oyA4KiAAAAAAADhlIAAAOGYgOGggADhvIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOC0gOC0gOC0gOC0gOC0gOC0gOC0gOC0gOC0gOC0gOC0gOC0gOK8gADioIDjhIAAAAAAAAAAAAAAAAAAAAAA44SAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADgpIAAAAAAAAAAAAAAAAAAAAAAAAAAAADhuIDhtIAAAAAAAOGkgAAA4KSA0IAA0IAAzIDQgNCAAOG0gAAA4bSA4oiAAAAAAAAAAAAAAAAAAAAAAADQgOC8gOGYgOGUgOGUgOGUgOGUgOGUgOGYgOGYgOGYgADhkIAAAAAAAAAAAAAAAAAA4KiA0IDMgAAA3IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADgsIDgvIDgvIDgvIDgvIDgvIDgvIDgvIDgvIDhmIDhjIAA4aiAAAAAAAAAAAAAAAAAAAAAAAAAAAAAzIDhmIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4pCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADgtIAAzIDQgOm7vwAAAAAAAAAAAAAAAADur78AAAAAAMyAAAAAAAAAAAAAAADrn78AAADQgAAAAADvg78AAADgpIAAAADhjIDhgIAA4LCAAAAAAAAAAAAA6Yu/AADru7/us78A4byAAAAAAAAAAAAAAO6jvwAAAAAAAAAAAOCggNCAAAAAAAAA4KCA7qu/AAAA4ZSAAADhgIDui7/vo78AAO+bv+GUgAAAAAAAAAAA75u/AAAAAO6bvwAAAAAAAAAA7L+/AADvm7/hlIAAAAAA4KCA7re/75e/0IDuk7/vm7/un7/tm78AAADvi78AAO+PvwAA77O/AAAAAADtu7/gvIAAAADui7/st78A7Z+/AAAAAADur78AAOqXv+6zvwDtg78AAO+Lv+CogAAAAAAAAAAAAAAAAOCggAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4KCA76O/AAAAAAAAAAAAAAAAAAAAAO+jv++zvwAAAAAAAAAAAAAA75u/AOGAgAAAAADMgAAAAAAAAAAA4KSA77O/AAAAAAAAAAAAAAAAAAAAAO+zvwAAAAAAAAAAAAAAAAAA75u/4aCAAAAA4YCAAAAAAAAAAADYgO+jvwAAAO6zvwAAAAAAAADvq78AAAAAAAAAAAAAAAAAAAAAAAAA4LCAAAAAAAAAAO+vvwAA4KCAAAAAAAAAAAAAAAAAAADYgAAAAO6zvwAAAAAAAAAA4YCAAADhnIAAAAAAAAAAAAAAAADus78AAAAAAAAAAAAAAAAAAAAA4YCA76+/AAAAAAAAAADgoIDiqIAAAOGYgAAAAAAAAAAAAAAA2IDimIAAAAAA75O/7KO/AMyAAADgoIAA4YCAAADtg78AAADsu78AAAAAAAAAAOC0gO2HvwAAAADhgIAAAAAA4YiAAADvr7/hgIAAAAAA64O/AAAAAAAAAAAAAAAAAAAAAADuq78AAAAAAADsm7/hiIAAAO6rv+GcgMyAAAAA64e/6Ze/7Iu/4oSAAADitIAAAAAAAAAAAMyAAO+bv++DvwAAAAAAAADtp78AAO63vwAAAAAAAOCggAAA4KSAAO67v++fvwAAAAAAAAAAANCAAAAA76+/ANSAAAAAAAAAAAAA77O/1IDcgAAAAAAA4LSA76+/4LiAAADvl7/uv7/goIAAAOCggAAAAADvp78AAO+PvwDMgAAAAAAAAOCkgO+jv+67vwAAAAAAAAAA77O/75+/0IAA7pO/AADth7/gqIDhjIDgvIAA74O/AOC8gAAAAAAAAAAAAAAA4KiA4KSAAAAAAAAAAO67v++Dv9CA2IAA7ru/AOCogADQgOCogAAAAAAAAADvi78A76O/4pCAAAAAAOuHv++nvwDgoIAA74O/74+/AAAAAAAA7Ju/AO6rv++Xv++vv+CogO6zvwAAAO+bvwAAAAAAAAAAAAAAAAAAAADgoIAA77e/AAAAAAAAAAAAAAAAAADvo78AAAAAAAAAAAAAAAAAAAAAAAAAAO+fv9yAAAAAAAAAAAAAAAAAAAAAAO+TvwDQgAAAAAAAAAAAAAAAAAAAAADvq78AAAAAAAAAAAAAAAAAAO+zv9iA4YCAAAAAAAAAAAAAAAAAAAAAAOGYgAAAAAAAAAAAAAAAAAAA7qe/7qO/AAAAAAAAAAAAAOGQgAAAAAAA74+/AAAAAAAAAAAA7oe/AMyAAAAAAOyTvwAAAAAAAAAAAAAAANyAAAAAAAAAAAAAAAAAAAAA77O/0IAAAAAAAAAAAAAAAAAAAADgoIAAAAAA3IAAAAAAAAAAAAAAAAAAAADgqIDvs7/vq7/hjIDgsIAAAAAAAAAAAAAAAAAAAO+3v++zvwAAAAAAAAAAAAAAAADvh7/cgAAAAAAAAAAAAAAAAAAAAO+Tv+CggADvp78AAAAAAAAAAAAAAAAAAO+rvwAA7Zu/zIAAAAAAAAAAAAAAAO+rv8yA76+/AAAAAAAAAAAAAAAAAADjgIAAAAAAAAAAAAAA74O/AO6DvwAAAO+bv++TvwDhmIAAAAAA7b+/74O/76+/AO+fvwDvk7/vs78AAAAAAAAAAAAAAAAA3IAAAAAAAAAAAO6Lv++vvwDvs78A76u/AO+jvwAAAAAAANCA6ru/AAAAAOKcgO6LvwDvq78AAAAAAAAA76O/AAAAAAAAAAAAAAAAAAAAAADwoICC8KCAguCsgOawgMSA4KCA2IAAxIDYgADEgAAAAA=="
UNR_256x256="AMSAxIDigKAAxIDigIDqoJAA4ZiAAOKggADigIAA5ICAAMSA4oCAAAAQAOGMiwDhjIsAAAAAAOiAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iEgsu/6a2P5L+/6p2z54+/6pmx54e/6pmx54e/6pmx54e/6pmx54e/6pmx54e/6pmx54e/6pmx54e/6pmy54u/6oGf5b+/6IyJ4Ke/6ICAw7/ogIDDv+iEhNO/6bWV5Ze/6p2z54+/6pmx54e/6pmx54e/6pmx54e/6pmx54e/6pmx54e/6p2z54+/6a2P5L+/6ISCy7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ohIPPv+q2iOijv+yHheyXv+yHheyXv+yLh+yfv+yLh+yfv+yLh+yfv+yLh+yfv+yLh+yfv+yLhuybv+yHhOyTv+uapOqTv+iUkOGDv+e8gMO/57iAw7/ogIffv+uGlumbv+yPiuyrv+yLh+yfv+yLh+yfv+yLh+yfv+yLh+yfv+yHheyXv+yHheyXv+q2iOijv+iEg8+/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ISDz7/sipzps7/ug6Puj7/rrpfpn7/qhaTmk7/qiabmm7/qiabmm7/qiabmm7/qhaTmk7/rhoTok7/tt5zts7/svrzrs7/ooJLhi7/olIngp7/rjaXml7/rsbnnp7/qoarmq7/qiabmm7/qiabmm7/qiabmm7/qiabmm7/qhaTmk7/rrpfpn7/ug6Puj7/sipzps7/ohIPPv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iIhNO/7aaz64+/77+/77+/64mp5qe/56yAw7/nuIDDv+e8gMO/57iAw7/nrIDDv+m0v+O/v++zue+nv+6vmO2jv+iglOGTv+iglOGTv+6vmO2jv++zue+nv+m8v+O/v+e0gMO/57yAw7/nvIDDv+e4gMO/56yAw7/rianmp7/vv7/vv7/tprPrj7/oiITTv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iIhNO/7Kqk6pO/7q+u7ru/7JqV6Ze/6rWZ5ae/6aCw44O/57yAw7/pgKDig7/qsZjlo7/rsb3nt7/uo6bum7/ug5Ptj7/riabmm7/rgaDmg7/ssprpq7/tgqDqg7/pkKnip7/nvIDDv+iAgMO/57yAw7/poLDjg7/qtZnlp7/smpXpl7/ur67uu7/sqqTqk7/oiITTv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iEg8+/6rqJ6Ke/7IuG7Ju/7pum7pu/77+/77+/7I6H6J+/57CAw7/qtZrlq7/vv7/vv7/vg7Dvg7/si4Tsk7/sr4zss7/vq7vvr7/vl6ruq7/pkKjio7/nvIDDv+iAgMO/6ICAw7/ogIDDv+e4gMO/7I6H6J+/77+/77+/7pum7pu/7IuG7Ju/6rqJ6Ke/6ISDz7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ohILLv+qJpuabv+uCk+mPv+2/ku2Lv++/v++/v+yOh+ifv+ewgMO/6rWa5au/77+/77+/7rOk7pO/64qU6ZO/656Y6aO/7bK967e/7aKw64O/6Lye4bu/57yAw7/ogIDDv+iAgMO/6ICAw7/nuIDDv+yOh+ifv++/v++/v+2/ku2Lv+uCk+mPv+qJpuabv+iEgsu/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ohITTv+iEhNO/7LKZ6ae/77+/77+/7I6H6J+/57CAw7/qtZrlq7/vv7/vv7/ug4Hsh7/olIzgs7/ohITTv+iQieCnv+iQiOCjv+iAgce/57yAw7/nvIDDv+e8gMO/6ICAw7/nuIDDv+yOh+ifv++/v++/v+yymemnv+iEhNO/6ISE07/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/nvIDDv+yulumbv++/v++/v+yOh+ifv+ewgMO/6rWa5au/77+/77+/7peK7Ku/6aCv4r+/6YSg4oO/6IiDz7/oiIPPv+mEouKLv+mQqOKjv+mQqOKjv+mQqOKjv+icjuC7v+e4gMO/7I6H6J+/77+/77+/7K6W6Zu/57yAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+e8gMO/7K6W6Zu/77+/77+/7I6H6J+/57CAw7/qtZrlq7/vv7/vv7/vt7rvq7/vn67uu7/uj4bsm7/opJLhi7/opJLhi7/uj4bsm7/vm6zus7/vk6ruq7/vk6ruq7/qpZPlj7/nsIDDv+yOh+ifv++/v++/v+yulumbv+e8gMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/nvIDDv+yulumbv++/v++/v+yOh+ifv+ewgMO/6rWa5au/77+/77+/77e676u/75+u7ru/7o+G7Ju/6KSS4Yu/6KiU4ZO/7p+U7ZO/76++77u/77u+77u/77+/77+/6rWa5au/57CAw7/sjofon7/vv7/vv7/srpbpm7/nvIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/57yAw7/srpbpm7/vv7/vv7/sjofon7/nsIDDv+q1muWrv++/v++/v+6Xiuyrv+mgsOODv+mEoeKHv+iEgsu/6JiR4Ye/67qq6qu/7LeO7Lu/74uy74u/77+/77+/6rWa5au/57CAw7/sjofon7/vv7/vv7/srpbpm7/nvIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/57yAw7/srpbpm7/vv7/vv7/sjofon7/nsIDDv+qtl+Wfv++3ue+nv+2yueunv+iMiOCjv+iAgce/6IyH37/opJjho7/rkp3pt7/sgr3rt7/uv67uu7/vv7/vv7/qtZrlq7/nsIDDv+yOh+ifv++/v++/v+yulumbv+e8gMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/nvIDDv+yulumbv++/v++/v+yOh+ifv+e4gMO/6KyW4Zu/6b2A5IO/6Zyw44O/6ICAw7/ovJ7hu7/torHrh7/tqrXrl7/psYXkl7/pjLTjk7/uk4zss7/vv7/vv7/qtZrlq7/nsIDDv+yOh+ifv++/v++/v+yulumbv+e8gMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/nvIDDv+yulumbv++/v++/v+yOh+ifv+e4gMO/57yAw7/nuIDDv+e4gMO/57yAw7/pkKjio7/vl6vur7/vl6vur7/pjKfin7/oiIbbv+6DgOyDv++/v++/v+q1muWrv+ewgMO/7I6H6J+/77+/77+/7K6W6Zu/57yAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ISDz7/rqbTnk7/tkqjqo7/rsbnnp7/qtZrlq7/poLDjg7/nvIDDv+iAgMO/57yAw7/pkKnip7/tgqDqg7/ssprpq7/rgaDmg7/rgaDmg7/sspnpp7/thqPqj7/rmazms7/qsZnlp7/pgKDig7/nvIDDv+mgsOODv+q1muWrv+uxueenv+2SqOqjv+uptOeTv+iEg8+/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6IiE07/tprPrj7/vv7/vv7/rianmp7/nqIDDv+e0gMO/57iAw7/nuIDDv+ewgMO/6bi/47+/77O576e/7q+Y7aO/6KCU4ZO/6KCU4ZO/7q+Y7aO/77O576e/6bC/47+/56iAw7/ntIDDv+e4gMO/57SAw7/nqIDDv+uJqeanv++/v++/v+2ms+uPv+iIhNO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6IiE07/tprPrj7/vv7/vv7/tsrjro7/sioXol7/sjofon7/sjofon7/sjofon7/sjofon7/shoPoj7/rtbrnq7/rjaXml7/okIngp7/oqJXhl7/ur5jto7/vu77vu7/tiqXql7/sioXol7/sjofon7/sjofon7/sjofon7/sioXol7/tsrjro7/vv7/vv7/tprPrj7/oiITTv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iIhNO/7aaz64+/77+/77+/77+/77+/77+/77+/77+/77+/77+/77+/77+/77+/77+/77+/7b+A7IO/6IiJ4Ke/57iAw7/nvIDDv+isleGXv+6vl+2fv++/v++/v++/v++/v++/v++/v++/v++/v++/v++/v++/v++/v++/v++/v++/v++/v++/v++/v+2ms+uPv+iIhNO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ISCy7/rlanmp7/sspnpp7/srpbpm7/srpbpm7/srpbpm7/srpbpm7/srpbpm7/sspjpo7/rpbHnh7/ojIXXv+iAgMO/6ICAw7/omI3gt7/rvb/nv7/sspjpo7/srpbpm7/srpbpm7/srpbpm7/srpbpm7/srpbpm7/srpbpm7/srpbpm7/sspnpp7/rlanmp7/ohILLv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/57yAw7/nvIDDv+e8gMO/57yAw7/nvIDDv+e8gMO/57yAw7/nvIDDv+e8gMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/nvIDDv+e8gMO/57yAw7/nvIDDv+e8gMO/57yAw7/nvIDDv+e8gMO/57yAw7/nvIDDv+e8gMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDv+iAgMO/6ICAw7/ogIDDvwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="

class EmbeddedResource:
    __resources = {
        "MyriadPro-Light.ttf": MYRIADPRO_LIGHT,
        "unr-256x256.ico": UNR_256x256
    }
    def __enter__(self, resource: str) -> tempfile:
        if resource in __resources.keys():
            self.tmp = tempfile.NamedTemporaryFile(delete=False)
            self.tmp.close()

            with open(tmp.name, "w") as file:
                data = base64.b64decode(__resources.get(resource))
                file.write(data)
            
            return self.tmp

        else:
            raise Exception("Resource Not Found")

    def __exit__(self, et, ev, etb):
        os.unlink(self.tmp.name)
        return True 