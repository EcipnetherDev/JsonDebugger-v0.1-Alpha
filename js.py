import json
import re

DOSYA = "/root/AI/data/knowledge.json"

print("🔍 JSON taranıyor...\n")

with open(DOSYA, "r", encoding="utf-8") as f:
    satirlar = f.readlines()

# Önce normal JSON parser'ı dene
try:
    json.loads("".join(satirlar))
    print("🟢 JSON tamamen geçerli!")
    exit()

except json.JSONDecodeError as e:
    print(f"⚠️ Parser ilk hatayı buldu:")
    print(f"   Satır : {e.lineno}")
    print(f"   Sütun : {e.colno}")
    print(f"   Hata  : {e.msg}\n")


print("🔎 Şüpheli satırlar aranıyor...\n")

supheli = []

for numara, satir in enumerate(satirlar, 1):
    temiz = satir.strip()

    if not temiz:
        continue

    # JSON key/value satırlarında tırnak sayısını kontrol et
    if ":" in temiz:
        tirnak = 0
        kacisli = False

        for karakter in temiz:
            if karakter == "\\" and not kacisli:
                kacisli = True
                continue

            if karakter == '"' and not kacisli:
                tirnak += 1

            kacisli = False

        # Normal bir "key": "value" satırında genellikle çift sayıda tırnak olur
        if tirnak % 2 != 0:
            supheli.append(
                (numara, "Tek sayıda tırnak", temiz)
            )

        # Değer içerisinde kaçışlanmamış tırnak ihtimali
        eslesme = re.search(r':\s*"(.+)"\s*,?\s*$', temiz)

        if not eslesme:
            supheli.append(
                (numara, "Şüpheli değer yapısı", temiz)
            )

    # JSON'un içinde üç nokta bırakılmışsa
    if "..." in temiz:
        supheli.append(
            (numara, "Literal ... bulundu", temiz)
        )


print("=" * 70)
print(f"🚨 Toplam şüpheli satır: {len(supheli)}")
print("=" * 70)

for numara, sebep, satir in supheli:
    print(f"\n📍 Satır {numara}")
    print(f"   Sebep : {sebep}")
    print(f"   İçerik: {satir}")

print("\n✅ Tarama tamamlandı.")
