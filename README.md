# Mahsül Öneri Sistemi

Toprak ve iklim verilerine göre en uygun mahsülün yetiştirilmesini öneren çok sınıflı makine öğrenmesi projesi. 2200 örnekten oluşan Crop Recommendation Dataset üzerinde 5 farklı algoritma eğitilmiş, en iyi model Streamlit arayüzüyle canlıya alınmıştır.

🔗 **Canlı uygulama:** [https://mahsul-oneri-sistemi.streamlit.app/](https://mahsul-oneri-sistemi.streamlit.app/)

## Özellikler

- 7 girdi değişkeni: N, P, K, sıcaklık, nem, pH, yağış
- 22 mahsül sınıfı arasından tahmin
- 5 algoritma karşılaştırması: Random Forest, Decision Tree, KNN, SVM, Gradient Boosting
- SHAP ile model açıklaması
- Tarım temalı özel CSS tasarımlı Streamlit web arayüzü
  - 3 kolonlu girdi düzeni (Toprak Besinleri / İklim Koşulları / Toprak Özellikleri)
  - Sonuç kartı: Türkçe mahsül adı, emoji ve güven oranı
  - İlk 3 adayın gradient olasılık çubukları
  - Sidebar: NPK, pH ve yağış referans tabloları
  - pH'a göre dinamik toprak durumu göstergesi


## Kurulum

```bash
pip install --prefer-binary -r requirements.txt
```

> Python başlatıcıları bozuksa `python -m pip install --prefer-binary -r requirements.txt` kullanın.

## Çalıştırma

```bash
streamlit run app.py
```

> Başlatıcı sorunu yaşıyorsanız: `python -m streamlit run app.py`

Uygulama tarayıcıda `http://localhost:8501` adresinde açılır.

## Kullanım

1. Sayfadaki 3 kolonlu formu doldurun: Toprak Besinleri (N, P, K), İklim Koşulları (sıcaklık, nem, yağış) ve Toprak Özellikleri (pH)
2. **Mahsül Analizi Yap** butonuna tıklayın
3. Sonuç kartında önerilen mahsül, Türkçe adı ve güven oranı görüntülenir
4. "En Olası 3 Mahsül" bölümünde alternatif adaylar olasılık çubuklarıyla listelenir
5. "Kullanılan Değerler" alanından girilen parametreler doğrulanabilir

> **Güven oranı:** Modelin 22 sınıfa dağıttığı olasılık içinden en yüksek payı alan mahsülün yüzdesidir; mutlak doğruluk garantisi değil, modelin emin olma derecesini gösterir.

## Proje Yapısı

```
smart-crop-recommender/
├── data/
│   └── Crop_recommendation.csv      # 2200 örnek, 7 özellik, 22 sınıf
├── models/
│   ├── best_model.pkl               # Eğitilmiş en iyi model
│   ├── scaler.pkl                   # StandardScaler
│   ├── label_encoder.pkl            # LabelEncoder
│   └── feature_names.pkl            # Özellik isimleri
├── analiz_ve_modelleme.ipynb        # Veri ön işleme, özellik seçimi, modelleme
├── app.py                           # Streamlit uygulaması
├── requirements.txt
└── README.md
```

## Notebook (analiz_ve_modelleme.ipynb)

Modelleri sıfırdan eğitmek için notebook'u sırayla çalıştırın. Eğitim tamamlandığında model dosyaları `models/` klasörüne otomatik kaydedilir.

| Adım | İçerik |
|------|--------|
| Görev 1 | IQR yöntemiyle aykırı değer temizleme |
| Görev 2 | Pearson, ANOVA F-testi, Mutual Information, Random Forest önem skoru ile özellik seçimi |
| Görev 3 | 5 algoritma eğitimi, %60/%20/%20 stratified bölme, karışıklık matrisleri |
| Görev 4 | Accuracy/Precision/Recall, ROC analizi, SHAP açıklaması |

## Gereksinimler

- Python 3.9+
- Paketler: pandas, numpy, scikit-learn, matplotlib, seaborn, streamlit, joblib, shap, scipy
