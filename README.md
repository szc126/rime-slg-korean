# Soolegi (SLG) Korean Input / 쓰레기 한국어 입력

Soolegi (SLG) Korean Input (쓰레기 한국어 입력) for [RIME](https://rime.im/).

이 프로젝트를 “쓰레기 한국어 입력”라고 이름을 짓고, 본작에서 사용된 자작한 한국어 표기법을 “쓰레기 로마자”라고 이름을 짓습니다.

……

Soolegi (SLG) Korean Input (スレギ韓国語入力) for [RIME](https://rime.im/).

此のプロジェクトを「スレギ韓国語入力」と名付け、本作で使用されている自作の韓国語ローマ字表記法を「スレギローマ字」と名付けます。

## notes

설명서는 현재 없습니다.

RIME 라서 자판 배열/한글 표기법은 마음대로 바꿀 수 있어

작업중이라서 현재는 파일을 편집해도 버전 번호는 올리지 않습니다.

변태 기능에 후회 없음.

……

説明書は現在ありません。

RIME なんだからキーボード配列・ハングル表記法は自由に変えられるぞ

作業中なので現在はファイルを編集してもバージョン番号は上げません。

変態機能に後悔無し。

## schemata

* 쓰레기 로마자
  * `soolegi_hangugeo` 현대 한국어.
    * (bad idea)
  * `soolegi_yethangeul` 옛한글.
  * `soolegi_hanja` 한자 색인.
* 두벌식 자판
  * `slg_dubeolsik_yethangeul` 마개조(魔改造)된 두벌식 배열로 옛한글.

## dictionaries

* `ko__gyoyugyong_gicho_hanja` 《교육용 기초 한자》
* `ko__hangugeo_hakseubyong_eohwi` 국립국어연구원《한국어 학습용 어휘》
* `ko__unicode_hangul_compatibility_jamo`
* `ko__unicode_hangul_jamo`
* `ko__unicode_hangul_syllables`

### -

* `slg_hangugeo`
  * `ko__hangugeo_hakseubyong_eohwi`
  * `ko__unicode_hangul_compatibility_jamo`
  * `ko__unicode_hangul_jamo`
  * `ko__unicode_hangul_syllables`
* `slg_hanja`
  * `ko__gyoyugyong_gicho_hanja`
* `slg_yethangeul`
  * `ko__unicode_hangul_compatibility_jamo`
  * `ko__unicode_hangul_jamo`

## screenshots

### `soolegi_hangugeo`

<img src="https://gist.githubusercontent.com/szc126/b50caf5ceb06b50f72ea08ed95eb0051/raw/hangugeo_sagwa_a.png" />
<img src="https://gist.githubusercontent.com/szc126/b50caf5ceb06b50f72ea08ed95eb0051/raw/hangugeo_sagwa_b.png" />

### `soolegi_hanja`

<img src="https://gist.githubusercontent.com/szc126/b50caf5ceb06b50f72ea08ed95eb0051/raw/hanja_eum_a.png" />
<img src="https://gist.githubusercontent.com/szc126/b50caf5ceb06b50f72ea08ed95eb0051/raw/hanja_hun_geul.png" />

### `soolegi_yethangeul`

<img src="https://gist.githubusercontent.com/szc126/b50caf5ceb06b50f72ea08ed95eb0051/raw/yethangeul_ckjujelgg.png" />
<img src="https://gist.githubusercontent.com/szc126/b50caf5ceb06b50f72ea08ed95eb0051/raw/yethangeul_nogeoldae.png" />

### `slg_dubeolsik_yethangeul`

<img src="https://gist.githubusercontent.com/szc126/b50caf5ceb06b50f72ea08ed95eb0051/raw/yethangeul_ckjujelgg_dubeolsik.png" />
<img src="https://gist.githubusercontent.com/szc126/b50caf5ceb06b50f72ea08ed95eb0051/raw/yethangeul_nalasmal_dubeolsik.png" />

## 사용예

* [중간노걸대언해 - 위키문헌, 우리 모두의 도서관](https://ko.wikisource.org/wiki/중간노걸대언해)
  * 쓰레기 옛한글 × [地球拼音](https://github.com/rime/rime-terra-pinyin)

## 같이 보기

* RIME
  * https://github.com/biopolyhedron/rime-qyeyshanglr-hanja
  * https://github.com/einverne/rime-hangul
  * https://github.com/rime-aca/rime-hangyl
  * https://github.com/sgalal/rime-hanja
  * https://github.com/sgqy/rime-korean
  * http://cheonhyeong.com/Simplified/download.html
* online
  * https://akorn.bab2min.pe.kr/input
    * https://github.com/bab2min/akorn-input
  * https://mujjingun.github.io/oko.html
  * https://ohi.pat.im/
    * https://github.com/pat-al/Online-Hangeul-IME
