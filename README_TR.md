# CareerRAG — Yapay Zekâ Destekli İş Eşleştirme

[English](README.md) | [Türkçe](README_TR.md)

CareerRAG, özgeçmişleri iş ilanlarıyla eşleştiren ve kişiye özel mülakat hazırlığı sağlayan bir sistemdir.

## Özellikler

- PDF ve DOCX özgeçmişlerinden profil bilgisi çıkarma
- Beceri (%60), kıdem (%20) ve konum (%20) temelli ATS uyum puanı
- İş ilanı bağlantılarından ilan metni aktarma
- Eksik beceri analizi ve eğitim yol haritası
- Aday profiline özel teknik deneme mülakatı soruları
- Maaş aralığı görselleştirmesi
- Vektör veritabanındaki ilanlarla toplu eşleştirme

## Kurulum

```bash
pip install -r backend/requirements.txt
```

Gemini kullanmak için API anahtarını tanımlayın. Anahtar verilmezse uygulama test amaçlı sahte veri modunda çalışır.

```bash
export GEMINI_API_KEY="gemini-api-anahtariniz"
uvicorn backend.main:app --port 8003 --reload
```

Başka bir terminalde arayüzü başlatın:

```bash
streamlit run frontend/app.py --server.port 8503
```

