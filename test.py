import panphon
import difflib
import unicodedata
ft = panphon.FeatureTable()


def prefilter(string):
    string = string.replace('d̥', "t")
    string = string.replace("ɡ̥", "k")
    string = string.replace("b̥", "b")
    string = string.replace("'", "ʼ")
    return string


s = u"thi"
errorlist = []

segdict = ft.ipa_segs(s)
segpile = u"ɪaaːăbʲbʷb̞b̥cddʒdʲdːd̚d̥d͡zd͡ʑd͡ʒd͡ʒːeeːe̞ffʲfʷfːɡɡʲɡʷɡːɡ̟ʲhhʷiiːi̞i̥i̯jkk'kxkʰkʲkʷkʷ'kːk̟ʲk̟̚k͡p̚llʲlːmmʲmʷmːnnʲnːn̺ooːo̞o̥pp'pfpʰpʲpʷpːp̚rrːssʲsːtt'tstsʰtɕtɕʰtʃtʰtʲtʷ'tːt̚t̪t̪ʰt̪̚t͡st͡sʼt͡ɕt͡ɬt͡ʃt͡ʃʲt͡ʃʼt͡ʃːuuəuːvvʲvʷvːv̞v̞ʲwxyzzʲäæçðøŋŋ̟ŋ͡mœɐɐ̞ɑɓɔɕɕːɗəɛɟɡɡ̥ɣɤɤɐ̞ɤ̆ɥɦɨɪɫɯɯ̟ɯ̥ɰɱɲɴɸɹɹ̩ɻɻ̩ɽɾɾʲɾ̠ʀʂʃʃʲːʊʋʋʲʌʎʏʐʑʒʒ͡ɣʔʝββ̞θχḁ"
segpilebad = u"ăb̥d̚d̥d͡zd͡ʑd͡ʒd͡ʒːeeːe̞ɡɡʲɡʷɡːɡ̟ʲhhʷk'kxkʰkʲkʷkʷ'k̟ʲk̟̚k͡p̚llʲlːmmʲmʷmːnnʲnːn̺ooːo̞o̥pp'pfpʰpʲpʷpːp̚rrːssʲsːtt'tstsʰtɕtɕʰtʃtʰtʲtʷ'tːt̚t̪t̪ʰt̪̚t͡st͡sʼt͡ɕt͡ɬt͡ʃt͡ʃʲt͡ʃʼt͡ʃːuuəuːvvʲvʷvːv̞v̞ʲwxyzzʲäæçðøŋŋ̟ŋ͡mœɐɐ̞ɑɓɔɕɕːɗəɛɟɡɡ̥ɣɤɤɐ̞ɤ̆ɥɦɨɪɫɯɯ̟ɯ̥ɰɱɲɴɸɹɹ̩ɻɻ̩ɽɾɾʲɾ̠ʀʂʃʃʲːʊʋʋʲʌʎʏʐʑʒʒ͡ɣʔʝββ̞θχḁ"
seglist = [u"ɪ", u"a", u"aː", u"ă", u"b", u"bʲ", u"bʷ", u"bː", u"b̞", u"b̥", u"c", u"d", u"dʒ", u"dʲ", u"dː", u"d̚", u"d̥", u"d͡z", u"d͡ʑ", u"d͡ʒ", u"d͡ʒː", u"e", u"eː", u"e̞", u"f", u"fʲ", u"fʷ", u"fː", u"ɡ", u"ɡʲ", u"ɡʷ", u"ɡː", u"ɡ̟ʲ", u"h", u"hʷ", u"i", u"iː", u"i̞", u"i̥", u"i̯", u"j", u"k", u"k'", u"kx", u"kʰ", u"kʲ", u"kʷ", u"kʷ'", u"kː", u"k̟ʲ", u"k̟̚", u"k͡p̚", u"l", u"lʲ", u"lː", u"m", u"mʲ", u"mʷ", u"mː", u"n", u"nʲ", u"nː", u"n̺", u"o", u"oː", u"o̞", u"o̥", u"p", u"p'", u"pf", u"pʰ", u"pʲ", u"pʷ", u"pː", u"p̚", u"r", u"rː", u"s", u"sʲ", u"sː", u"t", u"t'", u"ts", u"tsʰ", u"tɕ", u"tɕʰ", u"tʃ", u"tʰ", u"tʲ", u"tʷ'",
           u"tː", u"t̚", u"t̪", u"t̪ʰ", u"t̪̚", u"t͡s", u"t͡sʼ", u"t͡ɕ", u"t͡ɬ", u"t͡ʃ", u"t͡ʃʲ", u"t͡ʃʼ", u"t͡ʃː", u"u", u"uə", u"uː", u"v", u"vʲ", u"vʷ", u"vː", u"v̞", u"v̞ʲ", u"w", u"x", u"y", u"z", u"zʲ", u"ä", u"æ", u"ç", u"ð", u"ø", u"ŋ", u"ŋ̟", u"ŋ͡m", u"œ", u"ɐ", u"ɐ̞", u"ɑ", u"ɓ", u"ɔ", u"ɕ", u"ɕː", u"ɗ", u"ə", u"ɛ", u"ɟ", u"ɡ", u"ɡ̥", u"ɣ", u"ɤ", u"ɤɐ̞", u"ɤ̆", u"ɥ", u"ɦ", u"ɨ", u"ɪ", u"ɫ", u"ɯ", u"ɯ̟", u"ɯ̥", u"ɰ", u"ɱ", u"ɲ", u"ɴ", u"ɸ", u"ɹ", u"ɹ̩", u"ɻ", u"ɻ̩", u"ɽ", u"ɾ", u"ɾʲ", u"ɾ̠", u"ʀ", u"ʂ", u"ʃ", u"ʃʲː", u"ʊ", u"ʋ", u"ʋʲ", u"ʌ", u"ʎ", u"ʏ", u"ʐ", u"ʑ", u"ʒ", u"ʒ͡ɣ", u"ʔ", u"ʝ", u"β", u"β̞", u"θ", u"χ", u"ḁ"]
for seg in segpile:
    # print(ft.ipa_segs(seg))
    segsafe = ft.segs_safe(segpile)
    segfilter = ft.filter_string(segpilebad)

    # print(segsafe)
print(ft.filter_string(u"ẽ"))

cases = [(segpilebad, segfilter)]
for a in seglist:
    tempa = unicodedata.normalize("NFC", prefilter(a))
    # print('{} => {}'.format(a, b))
    b = ft.filter_string(tempa)
    for i, s in enumerate(difflib.ndiff(tempa, b)):
        if s[0] == ' ':
            continue
        elif s[0] == '-':
            print(u'Delete "{}" from position {}'.format(s[-1], i))
            tempau = ""
            for _c in tempa:
                tempau += 'U+%04x' % ord(_c) + " "
            bu = ""
            for _c in b:
                bu += 'U+%04x' % ord(_c) + " "
            errorlist.append((tempa, tempau, b, bu))
            # print(repr(segpilebad[i].decode("utf-8")))
        elif s[0] == '+':
            print(u'Add "{}" to position {}'.format(s[-1], i))
    # dst = panphon.distance.Distance()
# temp = dst.dogol_prime_distance(u"bob", u"pop")


print(errorlist)
# panphon.featuretable.seg_regex(u"thin")
