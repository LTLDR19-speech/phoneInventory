import csv
import json
import ipapy
import panphon
from functools import reduce
import unicodedata
from ipapy import UNICODE_TO_IPA
from ipapy import is_valid_ipa
from ipapy.ipastring import IPAString


def concat(x1, x2): return x1 + x2


def prefilter(string):
    string = string.replace('d̥', "t")
    string = string.replace("ɡ̥", "k")
    string = string.replace("b̥", "b")
    string = string.replace("'", "ʼ")
    string = string.replace(":", "ː")
    uString = unicodedata.normalize("NFD", string)
    return uString


s = " "
ft = panphon.FeatureTable()

# Source: 'https://raw.githubusercontent.com/phoible/dev/master/data/phoible.csv'
with open('data/phoible.csv', mode='r') as infile:
    reader = csv.reader(infile)
    with open('data/phoible_new.csv', mode='w') as outfile:
        #writer = csv.writer(outfile)
        results = {}
        frequency = {}
        SaneFrequency = {}
        worldPhoneList = []
        index = []
        IPAErrors = []
        for rows in reader:
            # print(rows)
            rowNum = 1
            if rows[0] == "InventoryID":
                rowIndex = rows
            else:
                rowNum += 1
                if not rows[1] in results:
                    results[rows[1]] = {}
                    results[rows[1]]["GlottoCode"] = rows[1]
                    results[rows[1]]["LanguageName"] = rows[3]
                    results[rows[1]]["ISO6393"] = rows[2]
                    results[rows[1]]["SpecificDialect"] = rows[4]
                    results[rows[1]]["phones"] = {}
                    index.append({"GlottoCode": rows[1],
                                  "LanguageName": rows[3],
                                  "ISO6393": rows[2],
                                  "SpecificDialect": rows[4],
                                  "profile": rows[1] + ".json",
                                  "phonelists": rows[1] + ".txt"
                                  })
                names = []
                if not "|" in rows[6]:
                    glyphs = [prefilter(rows[6])]
                    names = [rows[1]]
                else:
                    glyphs = prefilter(rows[6]).split("|")
                    for glyph in glyphs:
                        idx = 0
                        for char in glyph:
                            if idx == 0:
                                item = '%04x' % ord(char)
                                name = item
                                idx += 1
                            else:
                                item = "+" + '%04x' % ord(char)
                                name = name + item
                        names.append("thing")
                # Todo:, Only keeps one of pair, handle both
                # s_glyph = IPAString(unicode_string=glyph)
                glyph = glyphs[0]

                if ft.validate_word(glyph) and is_valid_ipa(glyph):
                    results[rows[1]]["phones"][rows[5]] = {
                        "glyph": glyph
                    }
                    if not rows[5] == "NA":
                        results[rows[1]]["phones"][rows[5]
                                                   ]["allophones"] = prefilter(rows[7])
                elif not is_valid_ipa(glyph) and not ft.validate_word(glyph):
                    descrip = "both: " + glyph
                    if descrip not in IPAErrors:
                        IPAErrors.append(descrip)
                else:
                    if not is_valid_ipa(glyph):
                        descrip = "ipapy: " + glyph
                        if descrip not in IPAErrors:
                            IPAErrors.append(descrip)
                    if not ft.validate_word(glyph):
                        descrip = "panphon: " + glyph
                        if descrip not in IPAErrors:
                            IPAErrors.append(descrip)


langPhoneSets = []
saneLangPhoneSets = []
LangSegs = set()
# Languages
for key, val in results.items():
    # Calc Long-Form World Frequency:
    phoneList = val["phones"]
    langPhoneSet = []
    langPhones = set()

    # Language Phone Sets
    for key2, val2 in phoneList.items():
        # Collect All Glyphs per Language:
        langPhoneSet.append(val2["glyph"])

        if not val2["glyph"] in frequency:
            frequency[key2] = {"glyph": val2["glyph"], "freq": 1}
        else:
            frequency[key2]["freq"] += 1

    # Sort and Filter Phoneme List
    langPhoneList = list(dict.fromkeys(langPhoneSet))s
    langPhoneList.sort()
    langPhoneString = s.join(langPhoneList)
    results[key]["ComplexPhoneList"] = langPhoneString

    # Simplify Phone List
    SaneLangPhoneList = ft.ipa_segs(langPhoneString)
    SaneLangPhoneClean = list(set(SaneLangPhoneList))
    SaneLangPhoneClean.sort()
    SaneLangPhoneString = s.join(SaneLangPhoneClean)
    if len(SaneLangPhoneString) == len(ft.filter_string(SaneLangPhoneString)):
        print("Error")
    # saneLangPhoneSets.append([key, saneLangPhoneString])
    results[key]["ComponentList"] = SaneLangPhoneString
    # for phone in SaneLangPhoneclean:
    #    langPhones.add(phone)
    for line in SaneLangPhoneClean:
        idx = 1
        name = ""
        for char in line:
            if idx == 1:
                name = '%04x' % ord(char)
                idx += 1
            else:
                name += "+" + '%04x' % ord(char)
        if not name in SaneFrequency:
            SaneFrequency[name] = {"glyph": line, "freq": 1}
        else:
            SaneFrequency[name]["freq"] += 1

    # Output Language Profile
    filename = key
    path = "profiles/"
    with open(path + filename + ".json", 'w', encoding="utf-8") as fp:
        json.dump(val, fp, indent=2)
    with open("components/" + filename + ".txt", 'w', encoding="utf-8") as fp:
        components = val["ComponentList"].split(" ")
        i = 1
        for x in components:
            fp.write(x + " " + str(i) + "\n")
            i += 1
    with open("attested_components/" + filename + ".txt", 'w', encoding="utf-8") as fp:
        attestedComponents = val["ComplexPhoneList"].split(" ")
        i = 1
        for x in attestedComponents:
            fp.write(x + " " + str(i) + "\n")
            i += 1


# Export Results
with open(path + "!Index.json", 'w', encoding="utf-8") as fp:
    json.dump(index, fp, indent=2)
with open(path + "!WorldFrequency.json", 'w', encoding="utf-8") as fp:
    json.dump(frequency, fp, indent=2)
with open(path + "!SaneWorldFrequency.json", 'w', encoding="utf-8") as fp:
    json.dump(SaneFrequency, fp, indent=2)
with open(path + "!WorldPhoneList.txt", 'w', encoding="utf-8") as fp:
    for phone in frequency.items():
        fp.write(phone[1]["glyph"]+"\n")
with open(path + "!SaneWorldPhoneList.txt", 'w', encoding="utf-8") as fp:
    for phone in SaneFrequency.items():
        fp.write(phone[1]["glyph"]+"\n")
with open(path + "!IPAErrors.txt", 'w', encoding="utf-8") as fp:
    for phone in IPAErrors:
        fp.write(phone+"\n")
