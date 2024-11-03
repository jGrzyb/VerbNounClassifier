import re
import json
import fpdf

with open('text.txt') as file:
    text = file.read()

# get words
words = [w.lower() for w in re.split(r'\W+', text) if w]

# dict key=verb, value=set(noun)
d = {}

# if verb find next nearest noun and add to dictionary d
for i, w in enumerate(words):
    if(w.endswith('s')):
        # change verb to present tense
        present = w[:-2] + 'as'
        for j in range(i, i+4):
            if words[j].endswith(('o', 'on', 'oj' 'ojn')):
                if present not in d:
                    d[present] = set()
                d[present].add(words[j].rstrip('jn'))

# Take 100 with the most verbs
result = sorted(d, key=lambda x: len(d[x]), reverse=True)[:100]

with open('result.json', 'w') as file:
    json.dump({k: sorted(v) for k, v in d.items()}, file, indent=4)

common_nouns = {}
for i in range(len(result)):
    for j in range(i+1, len(result)):
        common_nouns[result[i] + " " + result[j]] = d[result[i]] & d[result[j]]


res = sorted(common_nouns, key=lambda x: len(common_nouns[x]), reverse=True)[:100]

with open('common_nouns.json', 'w') as file:
    json.dump({k: sorted(v) for k, v in common_nouns.items()}, file, indent=4)


pdf = fpdf.FPDF()
pdf.add_font("DejaVu", "", "DejaVuSans.ttf")
pdf.add_font("DejaVu", "B", "DejaVuSans-Bold.ttf")
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Title
pdf.set_font("DejaVu", "B", 24)
pdf.cell(200, 10, text="Analiza dystrybucyjna", align='C')
pdf.ln(10)
pdf.set_font("DejaVu", "", 16)
pdf.cell(200, 10, text="Paweł Froń, Jakub Grzyb", align='C')
pdf.ln(20)

pdf.set_font("DejaVu", "B", 12)
pdf.cell(200, 5, text="Link do repozytorium", link="https://github.com/jGrzyb/VerbNounClassifier")
pdf.ln(10)

# 1. Wstęp
pdf.set_font("DejaVu", "B", 16)
pdf.cell(200, 10, text="1. Wstęp", align="L")
pdf.ln(10)
pdf.set_font("DejaVu", "", 12)
pdf.multi_cell(0, 5, text="Analiza dystrybucyjna jest to metoda która zakłada, że słowa występujące w podobnych kontekstach mają podobne znaczenie. Zgodnie z tą hipotezą rzeczowniki, które często współwystępują z tymi samymi czasownikami (np. „jeść” i „gotować”), mogą być semantycznie powiązane i oznaczać podobne rzeczy, jak „jedzenie”.")
pdf.ln(10)

# 2. Analiza
pdf.set_font("DejaVu", "B", 16)
pdf.cell(200, 10, text="2. Analiza", align="L")
pdf.ln(10)
pdf.set_font("DejaVu", "", 12)
pdf.multi_cell(0, 5, text="Program stworzony do celów tej analizy przyjmuje tekst w postaci pliku txt w języku esperanto. Na potrzeby tej analizy naszym tekstem jest Biblia. Jest to duża baza tekstu mająca ponad 30 tys lini tekstu")
pdf.ln(10)

# 3. Przypisanie
pdf.set_font("DejaVu", "B", 16)
pdf.cell(200, 10, text="3. Czasowniki i przypisane im rzeczowniki", align="L")
pdf.ln(10)
pdf.set_font("DejaVu", "", 11)
for i in range(5):
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(200, 5, text=result[i] + ": ")
    pdf.ln(5)
    pdf.set_font("DejaVu", "", 9)
    pdf.multi_cell(0, 4, text=str.join(", ", d[result[i]]))
    pdf.ln(10)

# 4. Część wspólna
pdf.set_font("DejaVu", "B", 16)
pdf.cell(200, 10, text="4. Rzeczowniki wspólne dla par czasowników", align="L")
pdf.ln(10)
pdf.set_font("DejaVu", "", 11)
for i in range(5):
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(200, 5, text=res[i] + ": ")
    pdf.ln(5)
    pdf.set_font("DejaVu", "", 9)
    pdf.multi_cell(0, 4, text=str.join(", ", common_nouns[res[i]]))
    pdf.ln(10)

# 5. Wnioski
pdf.set_font("DejaVu", "B", 16)
pdf.cell(200, 10, text="5. Zakończenie", align="L")
pdf.ln(10)
pdf.set_font("DejaVu", "", 12)
pdf.multi_cell(0, 5, text="Analiza dystrybucyjna wskazuje grupy rzeczowników o podobnym znaczeniu dla powyższych par czasowników. Można zauważyć, że w podanych parah często występuje czasownik \"estas\" oznaczający \"być\" co jest zrozumiałe jako że jest to jeden z najczęściej używanych i najogólniejszych czasowników. Po więcej danych odsyłamy do repozytorium na github-ie: link", link="https://github.com/jGrzyb/VerbNounClassifier")
pdf.ln(10)



pdf.output("Analiza dystrybucyjna.pdf")

