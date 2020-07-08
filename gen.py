#!/usr/bin/env python3

import re
import unicodedata
import csv
import json

# it just Werks™

u_blocks = [
	{'name': 'hangul jamo', 'range': (0x1100, 0x11ff)},
	{'name': 'hangul jamo extended-a', 'range': (0xa960, 0xa97f)},
	{'name': 'hangul jamo extended-b', 'range': (0xd7b0, 0xd7ff)},
]

# ucn - unicode character name
ucn_word_to_rom = {
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

jamo_to_rom = None

def convert_ucn_to_rom(ucn_words):
	rom = []
	for word in ucn_words:
		rom.append(ucn_word_to_rom[word])
	return ''.join(rom)

def romanize_syllable(syllable):
	# i could do smart people math
	# using the something whatever algorithm
	# or i could do this
	rom = ''
	syllable_nfd = unicodedata.normalize('NFD', syllable)
	for jamo in syllable_nfd:
		rom += jamo_to_rom[jamo]
	return rom

def collect_ucn_words():
	ucn_words_collection = {
		'c': set([]),
		'v': set([]),
	}

	for u_block in u_blocks:
		for dec in range(u_block['range'][0], u_block['range'][1] + 1):
			ucn = unicodedata.name(chr(dec), 'null').lower()
			print(hex(dec) + '\t' + chr(dec) + '\t' + ucn)

			ucn_words = re.findall(r'[a-z]+', ucn)
			ucn_words_collection['v' if 'jungseong' in ucn else 'c'].update(ucn_words)

	print()
	print(' '.join(ucn_words_collection['c']).lower())
	print()
	print(' '.join(ucn_words_collection['v']).lower())

def generate_map_jamo_to_rom():
	jamo_to_rom = {}

	for u_block in u_blocks:
		for dec in range(u_block['range'][0], u_block['range'][1] + 1):
			ucn = unicodedata.name(chr(dec), 'null').lower()

			if ucn != 'null':
				ucn_words = re.findall(r'[a-z]+', ucn)
				rom = convert_ucn_to_rom(ucn_words)
				jamo_to_rom[chr(dec)] = rom

	return jamo_to_rom

def generate_dict_jamo():
	dict_lines = {}

	for u_block in u_blocks:
		for dec in range(u_block['range'][0], u_block['range'][1] + 1):
			ucn = unicodedata.name(chr(dec), 'null').lower()

			if ucn != 'null':
				ucn_words = re.findall(r'[a-z]+', ucn)
				rom = convert_ucn_to_rom(ucn_words)
				#print(hex(dec) + '\t' + chr(dec) + '\t' + rom + '\t' + ucn)
				classification = u_block['name'] + ' : ' + ucn_words[1]

				if ucn_words[1] == 'jongseong':
					rom = rom.upper()

				if not classification in dict_lines:
					dict_lines[classification] = []
				dict_lines[classification].append(chr(dec) + '\t' + '~~' + rom)

	for classification in dict_lines:
		#print('# ' + classification)
		for dict_line in dict_lines[classification]:
			print(dict_line)

def generate_dict_compat_jamo():
	dict_lines = []

	for dec in range(0x3130, 0x318f + 1):
		ucn = unicodedata.name(chr(dec), 'null').lower()

		if ucn != 'null':
			ucn_words = re.findall(r'[a-z]+', ucn)
			rom = convert_ucn_to_rom(ucn_words)

			dict_lines.append(chr(dec) + '\t' + '~' + rom)

	print('\n'.join(dict_lines))

def generate_dict_syllable():
	for dec in range(0xac00, 0xd7a3 + 1):
		print(chr(dec) + '\t' + romanize_syllable(chr(dec)))

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
			'version: "alpha-2005-12"',
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

jamo_to_rom = generate_map_jamo_to_rom()
