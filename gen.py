#!/usr/bin/env python3

import re
import unicodedata
import csv
import json

# it just Werks™

unicode_word_to_rom = {
	'kiyeok': 'g',
	'khieukh': 'k',
	'yesieung': '0', #
	'ssangkiyeok': 'gg',

	'tikeut': 'd',
	'thieuth': 't',
	'nieun': 'n',
	'ssangtikeut': 'dd',
	'ssangthieuth': 'tt',
	'ssangnieun': 'nn',

	'pieup': 'b',
	'phieuph': 'p',
	'mieum': 'm',
	'ssangpieup': 'bb',
	'ssangmieum': 'mm',

	'cieuc': 'z',
	'chieuch': 'c',
	'sios': 's',
	'ssangcieuc': 'zz',
	'ssangsios': 'ss',

	'yeorinhieuh': 'x',
	'hieuh': 'h',
	'ieung': 'q',
	'ssangyeorinhieuh': 'xx',
	'ssanghieuh': 'hh',
	'ssangieung': 'qq',

	'rieul': 'l',
	'pansios': 'r',
	'ssangrieul': 'll',

	'chitueumcieuc': '`z',
	'chitueumchieuch': '`c',
	'chitueumsios': '`s',
	'chitueumssangcieuc': '`zz',
	'chitueumssangsios': '`ss',

	'ceongchieumcieuc': 'z`',
	'ceongchieumchieuch': 'c`',
	'ceongchieumsios': 's`',
	'ceongchieumssangcieuc': 'zz`',
	'ceongchieumssangsios': 'ss`',

	'kapyeounpieup': 'v',
	'kapyeounphieuph': 'f',
	'kapyeounmieum': 'w',
	'kapyeounssangpieup': 'vv',

	'kapyeounrieul': '7', #

	'a': 'a',
	'ae': 'ai',
	'ya': 'ja',
	'yae': 'jai',
	'eo': 'e',
	'e': 'ei',
	'yeo': 'je',
	'ye': 'jei',
	'o': 'o',
	'wa': 'oa',
	'wae': 'oai',
	'oe': 'oi',
	'yo': 'jo',
	'u': 'u',
	'weo': 'ue',
	'we': 'uei',
	'wi': 'ui',
	'yu': 'ju',
	'eu': 'y',
	'yi': 'yi',
	'i': 'i',
	'araea': '9', #
	'ssangaraea': '99', #
	'araeae': '9i', #

	'hangul': '',
	'filler': 'FILLER', #
	'choseong': '',
	'jungseong': '',
	'jongseong': '',
	'letter': '',
}

unicode_ranges = [
	[0x1100, 0x11ff],
	[0xa960, 0xa97f],
	[0xd7b0, 0xd7ff],
]

unicode_ranges_names = [
	"hangul jamo",
	"hangul jamo extended-a",
	"hangul jamo extended-b",
]

j_forms = {
	"choseong": "xform/(^| ){}/{}/",
	"jungseong": "xform/{}/{}/",
	"jongseong": "xform/{}( |$)/{}/",
}

def collect_unicode_name_words():
	unicode_name_words_collection = {
		"c": set([]),
		"v": set([]),
	}

	for block in range(0, len(unicode_ranges)):
		for dec in range(unicode_ranges[block][0], unicode_ranges[block][1] + 1):
			name = unicodedata.name(chr(dec), "NULL").lower()
			print(hex(dec) + "\t" + chr(dec) + "\t" + name)

			name_words = re.findall(r'[a-z]+', name)
			unicode_name_words_collection["v" if "jung" in name else "c"].update(name_words)
		#input()

	print(" ".join(unicode_name_words_collection["c"]))
	print(" ".join(unicode_name_words_collection["v"]))

def romanize_jamo_from_unicode_name(name_words):
	rom = []
	for i, word in enumerate(name_words):
		rom.append(unicode_word_to_rom[word])
	return "".join(rom)

def romanize_syllable(syllable, jamo_to_latn):
	ret = ""
	syllable_nfd = unicodedata.normalize('NFD', syllable)
	for z in syllable_nfd:
		ret += jamo_to_latn[z]
	return str(ret)

def generate_jamo_dict():
	pflines = {}

	for block in range(0, len(unicode_ranges)):
		for dec in range(unicode_ranges[block][0], unicode_ranges[block][1] + 1):
			name = unicodedata.name(chr(dec), "NULL").lower()

			if name != "null":
				name_words = re.findall(r'[a-z]+', name)

				rom = romanize_jamo_from_unicode_name(name_words)

				#print(hex(dec) + "\t" + chr(dec) + "\t" + rom + "\t" + name)

				classification = unicode_ranges_names[block] + " : " + name_words[1]
				if name_words[1] == 'choseong':
					rom = rom.upper()
				pfline = chr(dec) + "\t" + "~~" + rom
				if not classification in pflines:
					pflines[classification] = []
				pflines[classification].append(pfline)

	for classification in pflines:
		print("# " + classification)
		for pfline in pflines[classification]:
			print(pfline)

def generate_jamo_to_latn_mapping():
	jamo_to_latn = {}

	for dec in range(unicode_ranges[0][0], unicode_ranges[0][1] + 1):
		name = unicodedata.name(chr(dec), "NULL").lower()

		if name != "null":
			name_words = re.findall(r'[a-z]+', name)

			rom = romanize_jamo_from_unicode_name(name_words)

			jamo_to_latn[chr(dec)] = rom

	return jamo_to_latn

def generate_compat_jamo_dict():
	dictlines = []

	for dec in range(0x3130, 0x318f + 1):
		name = unicodedata.name(chr(dec), "NULL").lower()

		if name != "null":
			name_words = re.findall(r'[a-z]+', name)

			rom = romanize_jamo_from_unicode_name(name_words)

			if dec >= 0x314f:
				rom = "~" + rom # append "~" to vowels and exotic consonants

			dictlines.append(chr(dec) + "\t" + rom)

	print("\n".join(dictlines))

def generate_syllable_dict():
	jamo_to_latn = generate_jamo_to_latn_mapping()

	for dec in range(0xac00, 0xd7a3 + 1):
		# i could do smart people math
		# using the something whatever algorithm
		# or i could do this
		f = unicodedata.normalize('NFD', chr(dec))
		rom = ""
		for z in f:
			rom += jamo_to_latn[z]

		print(chr(dec) + "\t" + rom)

def generate_hakseubyong_dict():
	jamo_to_latn = generate_jamo_to_latn_mapping()
	collection = {}

	# TODO: verb/adj conjugation
	# 오다 왔-
	# 춥다 추워-
	# 등

	with open('hakseubyong.tsv', mode='r', encoding='utf-8') as f_in:
		f_in = csv.reader(f_in, delimiter='\t')

		next(f_in) # skip header

		#max_freq = 0
		#for row in f_in:
			#freq = (int(row[0]) if row[0] != '' else 0)
			#max_freq = (freq if freq > max_freq else max_freq)
		max_freq = 57151 # <하얀색>

		for row in f_in:
			#print("\t" + str(row))

			freq = row[0]
			word = row[1]
			pos = row[2]
			explanation = row[3]

			if freq == '':
				freq = None # place names do not have a frequency
			else:
				# high number = low frequency
				# (i.e. ranking)
				# reverse this for RIME
				freq = (max_freq + 2) - int(freq)

			#if re.search(r'[^가-힣\d]', word):
				#print(word)
			# only 2 entries:
			# <도쿄(동경)>
			# <베이징(북경)>

			words = re.findall(r'[가-힣]+', word)
			roms = []
			hanja = None

			for i, word in enumerate(words):
				roms.append([])
				for geul in word:
					roms[i].append(romanize_syllable(geul, jamo_to_latn))
				roms[i] = " ".join(roms[i])

			#print(str(words) + "\t" + str(roms))
			# grep "베이징"

			explanation = unicodedata.normalize('NFC', explanation) # un-compat CJK compat chars

			if re.search(r'[㐀-鿕]', explanation):
				exp_2 = explanation

				if "." in exp_2:
					# "數. ~를 세다"
					exp_2 = re.sub(r'\..+', '', exp_2)

				if re.search(r'^[㐀-鿕]+$', exp_2):
					hanja = exp_2
				elif exp_2.startswith("-") and exp_2.endswith("-"):
					# "-傷-"
					pass
				elif exp_2.startswith("-"):
					word_head = word[:-len(exp_2[1:])]
					word_tail = exp_2[1:]
					hanja = word_head + word_tail
				elif exp_2.endswith("-"):
					word_head = exp_2[:-1]
					word_tail = word[len(exp_2[:-1]):]
					hanja = word_head + word_tail
				else:
					# "市內bus"
					pass

			#for i, word in enumerate(words):
				#exp_3 = ""
				#if explanation:
					#exp_3 = ":::" + re.sub(r' ', '___', explanation)

				#print(freq + "\t" + words[i] + "\t" + roms[i] + exp_3)
				#if hanja:
					#print(freq + "\t" + hanja + "\t" + roms[i] + exp_3)

			for word in words:
				if not word in collection:
					collection[word] = {}
					collection[word]["freq"] = []
					#collection[word]["word"] = []
					collection[word]["rom"] = ""
					#collection[word]["pos"] = []
					collection[word]["explanation"] = []
					collection[word]["hanja"] = {}
					#collection[word]["hanja"]["hanja"] = ""
					#collection[word]["hanja"]["explanation"] = ""
				if freq:
					collection[word]["freq"].append(freq)
				#collection[word]["word"].append(word)
				collection[word]["rom"] = roms[i]
				#collection[word]["pos"].append(pos)
				collection[word]["explanation"].append(explanation)
				if hanja:
					# <가구>
					collection[word]["hanja"][hanja] = explanation

		for word in collection:
			freq = collection[word]["freq"]
			if freq:
				freq = max(freq)
			rom = collection[word]["rom"]
			explanation = collection[word]["explanation"]

			# remove duplicate explanations, as with <수> and <현재>
			# https://stackoverflow.com/questions/7961363/removing-duplicates-in-lists
			explanation = list(dict.fromkeys(explanation))
			# XXX: sort explanation by frequency?
			explanation = ";;".join(explanation)
			#if explanation != "":
				#explanation = "::" + re.sub(r" ", "__", explanation)
			explanation = "::" + "[" + word + "]" + re.sub(r" ", "__", explanation) + "=="
			# →"yes, this word is in the dictionary"

			print((str(freq) if freq else "") + "\t" + word + "\t" + rom + explanation)

			if collection[word]["hanja"]:
				for hanja in collection[word]["hanja"]:
					if freq:
						freq -= 1
					explanation = "::" + "[" + word + "]" + "=="
					print((str(freq) if freq else "") + "\t" + hanja + "\t" + rom + explanation)


def generate_gyoyugyong_gicho_hanja_dict():
	jamo_to_latn = generate_jamo_to_latn_mapping()
	collection = {}

	with open('gyoyugyong gicho hanja.json', mode='r', encoding='utf-8') as f_in:
		f_in = json.load(f_in)
		for syllChars in f_in:
			for grade in syllChars:
				if syllChars[grade]:
					syllChars[grade] = re.sub(r'\s*•\s*', ',', syllChars[grade])
					syllChars[grade] = re.sub(r'\s*\(', ':', syllChars[grade])
					syllChars[grade] = re.sub(r'\s*[()]\s*', '', syllChars[grade])
					syllChars[grade] = re.sub(r'\[\d+\]', '', syllChars[grade])
					syllChars[grade] = syllChars[grade].split(',')
					for temp in syllChars[grade]:
						temp = temp.split(':')
						chars = re.split(r'\s*/\s*', temp[0])
						eumhun = temp[1]
						eumhun_rom = []
						eumhun_rom_caps = False
						for char in eumhun:
							if char != " ":
								syllable_rom = romanize_syllable(char, jamo_to_latn)
								eumhun_rom.append(syllable_rom)
						eumhun_rom = "_".join(eumhun_rom)
						eumhun_rom = re.sub(r'([a-z]+)$', lambda z: str(z[1]).upper(), eumhun_rom) # <象> "코 끼리 상"
						eumhun = eumhun.replace(" ", "_")
						reading = eumhun_rom + ":" + eumhun + ("[" + "·".join(chars) + "]" if len(chars) > 1 else "")
						for char in chars:
							print(('2' if grade == 'mid' else '1') + '\t' + char + '\t' + reading)

def generate_bindo_dict():
	jamo_to_latn = generate_jamo_to_latn_mapping()
	names = {
		#'자모통계': ['자모 통계', 'jamo'],
		'음절통계': ['음절 통계', 'eumjeol'],
		'일반어휘통계': ['일반 어휘 통계', 'ilban_eohwi'],
		#'조사통계': ['조사 통계', 'josa'],
		'어미통계': ['어미 통계', 'eomi'],
		#'구통계': ['구(句) 통계', 'gu'],
	}

	def create_header(filename, name_ko, name_lat):
		return '\n'.join([
			'# Rime dictionary',
			'# encoding: utf-8',
			'#',
			'# 국립국어원《현대 국어 사용 빈도 조사 2》' + name_ko,
			'# https://www.korean.go.kr/front/reportData/reportDataView.do?mn_id=45&report_seq=1',
			'---',
			'name: "ko__hyeondae_gugeo_sayong_bindo_josa_2__' + name_lat + '"',
			'version: "1.0.0-2005-12"',
			'sort: "by_weight"',
			'columns:',
			'  - "weight"',
			'  - "text"',
			'  - "code"',
			'...',
		])

	for filename in names:
		with open('bindo_new/utf8/' + filename + '.txt', mode='r', encoding='utf8') as f_in:
			f_in = csv.reader(f_in, delimiter='\t')

			next(f_in) # skip header

			print(create_header(filename, names[filename][0], names[filename][1]))

#generate_hakseubyong_dict()
generate_gyoyugyong_gicho_hanja_dict()
#generate_bindo_dict()
