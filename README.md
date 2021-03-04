
`version: 0.0.1`

# __Install Guide__

## __Status__
- 2 nginx workers (nginx.conf)
- 10 waitress threads (server.py)

## __Install Step__
1. Install python
2. Install python libraries(pip)
3. Edit django setting.py (api\setting.py)
4. Edit folder path in ocr.py
5. Install nginx
6. Edit nginx.conf (conf\nginx.conf)
7. Install abbyy
8. Make amd edit waitress.bat file whith serves a web and keep watching it, if it deads make it run.
9. Make and edit nginx.bat file whith serving a server and keep watching it, if it deads make it run.
10. Make and edit auto.vbs which makes batch files run in background.
11. Run auto.vbs when system starts (by admin - can't run automatically by window service)
12. `(Not Used)` ~~Run Task Scheduler (window program) and make a new task which automatically run vbs file when system restarts.~~<br>
    - Error! `(If it runs by window service or Task Scheduler, only can handle two tasks at once. Over than two tasks occurs an Error..)`

## __Version & Library Info__

- __python__
	- version: 3.8.2
	- package list: django, waitress, pdfminer3

- __nginx__
	- download: <http://nginx.org/en/download.html>
	- version: 1.17.10
	
- __abbyy__
	- version: FineReader 12
	
	

## __Folder/File description__

- __Folder__
	- api: include web & ocr/xml codes(django, python)
	- abbyy: install abbyy
- __File__
	- nginx.conf: nginx configuration file
	- waitress.bat: running waitress batchfile
	- nginx.bat: running nginx batchfile
	- auti.vbs: runnung waitress.bat and nginx.bat in backend


# __API Guide__

## __General Info__

|Service| Method | URL | Encoding |
|:----------|:----------|:----------|:----------|
|__XML__| POST | 252.231.51.53/api/ocr/xml/ | UTF-8 |
|__OCR__| POST | 252.231.51.53/api/ocr/ocr/ | UTF-8 |

## __Request Parameter__ `(form-data)`
- __252.231.51.53/api/ocr/xml/__

    |Key| Type | Necessary | Description |
    |:----------|:----------|:----------|:----------|
    |job_id| UUID4 | Y | Running Job ID |
    |lang| [language](#language-list) | Y | Target language to do OCR |
    |file| file `(file name should be well formatted)` | Y | Input file |
    |extension| __'<U>pdf</U>'__ `(fixed argument)` | Y | Output file extension |
    |xml_type| __'<U>page</U>'__ or __'<U>letter</U>'__ `(only one)`  | Y | Output xml file main hierarchy |
    
- __252.231.51.53/api/ocr/ocr/__

    |Key| Type | Necessary | Description |
    |:----------|:----------|:----------|:----------|
    |job_id| UUID4 | Y | Running Job ID |
    |lang| [language](#language-list) | Y | Target language to do OCR |
    |file| file `(file name should be well formatted)` | Y | Input file |
    |extension| [extension](#extension-list) | Y | Output file extension |

## __Response__
- __Header__

    |Key | Description |
    |:----------|:----------|
    | job_id | Output Job ID |
    | status | [Result status](#status/message-list) |
    | message | [Result message](#status/message-list) corresponds with status |

- __Body__

    |Type| Description |
    |:----------|:----------|
    | File `(XML)` | Output XML File |

### Status/Message List

| Status | Message |
|:----------:|:----------:|
| 000 | Done |
| 001 | Input value error |
| 010 | Empty input file |
| 100 | Runtime error |
| 300 | URL error |
| 500 | Request type error |

### Extension List
- docx
- doc
- rtf
- odt
- pdf
- htm
- txt
- xlsx
- xlx
- pptx
- csv
- fb2
- epub
- djvu

### Language List

- [Natural Languages](#natural-languages)
- [Artificial Languages](#artificial-languages)
- [Formal Languages](#formal-languages)

    #### [Natural languages](#natural-languages)
    - Abkhaz
    - Adyghe
    - Afrikaans
    - Agul
    - Albanian
    - Altai
    - Arabic (Saudi Arabia)
    - Armenian (Eastern, Western, Grabar)*
    - Avar
    - Aymara
    - Azeri (Cyrillic), Azeri (Latin)
    - Bashkir*
    - Basque
    - Belarusian
    - Bemba
    - Blackfoot
    - Breton
    - Bugotu
    - Bulgarian*
    - Buryat
    - Catalan*
    - Cebuano
    - Chamorro
    - Chechen
    - Chinese Simplified, Chinese Traditional
    - Chukchee
    - Chuvash
    - Corsican
    - Crimean Tatar
    - Croatian*
    - Crow
    - Czech*
    - Dakota
    - Danish*
    - Dargwa
    - Dungan
    - Dutch, Dutch (Belgian)*
    - English*
    - Eskimo (Cyrillic), Eskimo (Latin)
    - Estonian*
    - Even
    - Evenki
    - Faroese
    - Fijian
    - Finnish*
    - French*
    - Frisian
    - Friulian
    - Gagauz
    - Galician
    - Ganda
    - German (New Spelling), German*
    - German (Luxembourg)
    - Greek*
    - Guarani
    - Hani
    - Hausa
    - Hawaiian
    - Hebrew*
    - Hungarian*
    - Icelandic
    - Indonesian*
    - Ingush
    - Irish
    - Italian*
    - Japanese
    - Jingpo
    - Kabardian
    - Kalmyk
    - Karachay-balkar
    - Karakalpak
    - Kashubian
    - Kawa
    - Kazakh
    - Khakass
    - Khanty
    - Kikuyu
    - Kirghiz
    - Kongo
    - Korean, Korean (Hangul)
    - Koryak
    - Kpelle
    - Kumyk
    - Kurdish
    - Lak
    - Latin*
    - Latvian*
    - Lezgi
    - Lithuanian*
    - Luba
    - Macedonian
    - Malagasy
    - Malay (Malaysian)
    - Malinke
    - Maltese
    - Mansi
    - Maori
    - Mari
    - Maya
    - Miao
    - Minangkabau
    - Mohawk
    - Moldavian
    - Mongol
    - Mordvin
    - Nahuatl
    - Nenets
    - Nivkh
    - Nogay
    - Norwegian (Bokmal), Norwegian (Nynorsk)*
    - Nyanja
    - Polish*
    - Portuguese, Portuguese (Brazilian)*
    - Ojibway
    - Ossetian
    - Papiamento
    - Occitan
    - Quechua (Bolivia)
    - Rhaeto-Romanic
    - Romanian*
    - Romany
    - Rundi
    - Russian*
    - Russian (Old Spelling)
    - Russian with accent
    - Rwanda
    - Sami (Lappish)
    - Samoan
    - Scottish Gaelic
    - Selkup
    - Serbian (Cyrillic), Serbian (Latin)
    - Shona
    - Slovak*
    - Slovenian*
    - Somali
    - Sorbian
    - Sotho
    - Spanish*
    - Sunda
    - Swahili
    - Swazi
    - Swedish*
    - Tabasaran
    - Tagalog
    - Tahitian
    - Tajik
    - Tatar*
    - Thai*
    - Tok Pisin
    - Tongan
    - Tswana
    - Tun
    - Turkish*
    - Turkmen (Cyrillic), Turkmen (Latin)
    - Tuvinian
    - Udmurt
    - Uighur (Cyrillic), Uighur (Latin)
    - Ukrainian*
    - Uzbek (Cyrillic), Uzbek (Latin)
    - Vietnamese*
    - Welsh
    - Wolof
    - Xhosa
    - Yakut
    - Yiddish
    - Zapotec
    - Zulu
    #### [Artificial Languages](#artificial-languages)
    - Esperanto
    - Interlingua
    - Ido
    - Occidental
    #### [Formal Languages](#formal-languages)
    - Basic
    - C/C++
    - COBOL
    - Digits
    - Fortran
    - Java
    - Pascal
    - Simple chemical formulas

    \* Dictionary support is available for this language, enabling ABBYY FineReader to identify unreliably recognized characters and detect spelling errors in texts written in this language.