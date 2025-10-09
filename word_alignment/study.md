# Edit Distance Çalışma Rehberi

Bu rehber, `word_alignment` modülündeki kodların nasıl çalıştığını ve edit
distance kavramının temelini örnekler üzerinden açıklar. Tüm görseller derslerdeki
"sağ üstten sol alta" izlenen backtrace yönüyle uyumludur.

## 1. Modül Bileşenleri

### 1.1 `compute_edit_distance`
- İki kelime arasındaki ağırlıklı edit distance değerini hesaplar.
- DP matrisini, seçilen okları (↖, ↑, ←) ve backtrace sırasında izlenen hücreleri
  döndürür.
- Varsayılan maliyetler: ekleme = 1, silme = 1, yerine koyma = 2.

### 1.2 `plot_manual_table`
- Matrisin derslerdeki kağıt düzenini taklit eden tabloyu oluşturur.
- Kelimeler sol alt referansa göre yerleştirilir; sağ üst hücre hedef noktadır.
- Hücre etiketleri üst üste binmesin diye genişletilmiş kutular kullanılır.

### 1.3 `plot_visual_walkthrough`
- Heatmap, yön okları ve operasyon özet tablosunu aynı hikâye içerisinde sunar.
- Backtrace yolu hücre sınırları ve çizgilerle güçlendirilir.

### 1.4 `compute_library_distance`
- Varsa `textdistance` paketini kullanarak aynı ağırlıklarla doğrulama yapar.
- Paket yoksa modülde bulunan yedek Levenshtein uygulaması çağrılır.

### 1.5 `loop_similarity_demo.demonstrate_loop_similarity`
- Yukarıdaki tüm adımları tek komutla çalıştırır.
- Ek bir figürde iç içe döngülerin sözde kodunu ve elde edilen skorları anlatır.

## 2. Ağırlıklı Edit Distance Adımları

Bir hücrenin değeri her zaman üç ihtimalin en küçüğüdür:

1. **↖ Diyagonal (Eşleşme / Yerine Koyma)**
   - Karakterler aynıysa ek maliyet yoktur.
   - Farklıysa `substitution_cost` eklenir.
2. **↑ Yukarı (Silme)** – Kaynak kelimeden bir karakter çıkarılır.
3. **← Sol (Ekleme)** – Hedef kelimeye bir karakter eklenir.

Başlangıç satırı ve sütunu, boş diziyi diğer kelimeye dönüştürmenin maliyetlerini
(`i * deletion_cost`, `j * insertion_cost`) içerir. Backtrace her zaman sağ üst
hücreden başlar, sol alt köşede biter.

## 3. Örnek 1 – "kitten" → "sitting"

Bu örnek demo scriptinin varsayılan kelimeleridir.

```python
from word_alignment.edit_distance_tools import compute_edit_distance

result = compute_edit_distance("kitten", "sitting")
print(result.distance)  # 5
print(result.similarity_score)  # 0.29...
```

### 3.1 Anahtar Hücreler

| Hücre (i, j) | Karakterler | Seçilen Hareket | Açıklama |
| ------------ | ----------- | ---------------- | -------- |
| (1, 1) | `k` vs `s` | ↖ Yerine koyma | `k → s` maliyeti 2, diğer seçeneklerden daha ucuzdur. |
| (3, 4) | `t` vs `t` | ↖ Eşleşme | Karakterler aynı, ek maliyet yok. |
| (6, 7) | `n` vs `g` | ↑ Silme | `n` harfi hedefte yok, silmek toplam maliyeti düşürür. |

### 3.2 Backtrace Öyküsü

1. **Başlangıç:** Sağ üst hücre `(6, 7)` → toplam maliyet `5`.
2. **Silme:** `n` karakteri hedefte olmadığı için silinir (↑ hareketi).
3. **Yerine koyma:** `e → i` dönüşümü için ↖ adımı ve 2 maliyet eklenir.
4. **Ekleme:** Hedefte fazladan `g` olduğu için ← hareketiyle eklenir.
5. **Eşleşmeler:** Kalan `itt` bölümü ↖ ile hatasız ilerler.
6. **Bitiş:** Sol alt köşede `(0, 0)` noktasına ulaşılır.

`plot_visual_walkthrough(result)` çağrısı bu adımları hücre kenarlarıyla
belirginleştirir, `plot_manual_table(result)` ise tabloyu geniş sütunlarla tekrar
yapılandırır.

## 4. Örnek 2 – Kısa Kelimelerle Elle Çalışma

"ad" → "sad" dönüşümünü elinizle hesaplamak için şu adımları izleyin:

1. Başlangıç satırı ve sütununu doldurun:
   - `dp[0][0] = 0`
   - `dp[0][1] = 1` (s ekleme)
   - `dp[0][2] = 2` (s + a ekleme)
   - `dp[1][0] = 1` (a silme)
   - `dp[2][0] = 2` (a + d silme)
2. İç döngülerde her hücreyi hesaplayın:

```python
str1, str2 = "ad", "sad"
# dp tablosu başlangıç değerleriyle (0. satır/sütun) doldurulmuş varsayılıyor.
for i in range(1, len(str1) + 1):
    for j in range(1, len(str2) + 1):
        cost_sub = dp[i-1][j-1] + (0 if str1[i-1] == str2[j-1] else 2)
        cost_del = dp[i-1][j] + 1
        cost_ins = dp[i][j-1] + 1
        dp[i][j] = min(cost_sub, cost_del, cost_ins)
```

3. Sağ üst hücre `(2, 3)` değeri `2` çıkar; backtrace adımları:
   - `d` ile `d` eşleşir (↖).
   - `a` ile `a` eşleşir (↖).
   - Sol üst köşeye gelmek için başa `s` eklenir (←).

Bu kısa örnek, daha uzun kelimelerdeki davranışı kavramak için pratik sağlar.

## 5. Kod Çalıştırma Önerileri

- Demo sırasında kullanılan figürleri kaydetmek için:
  ```python
  from word_alignment.edit_distance_tools import compute_edit_distance, plot_manual_table

  result = compute_edit_distance("flaw", "lawn")
  fig = plot_manual_table(result, show=False)
  fig.savefig("flaw_vs_lawn_manual.png", dpi=200)
  ```
- Farklı ağırlıklar denemek istiyorsanız fonksiyona parametre gönderin:
  ```python
  compute_edit_distance("kitten", "sitting", substitution_cost=1)
  ```

## 6. NLP’de Kullanım Senaryoları

- **Yazım Düzeltme:** Kullanıcı girdisini sözlükteki en yakın kelimeye dönüştürür.
- **Otomatik Değerlendirme:** Öğrenci cevaplarını referans çözümlerle karşılaştırır.
- **Makine Çevirisi Analizi:** Çeviri çıktısı ile altın standart arasındaki farkı
  puanlamak için kullanılabilir.
- **Ses Tanıma / OCR:** Model çıktılarının doğruluğunu değerlendirmek için edit
  distance kullanılır.

## 7. Çalışma Stratejileri

1. Önce kısa kelimelerle tabloyu kağıt üzerinde doldurun.
2. Her adımı neden seçtiğinizi açıklayan küçük notlar ekleyin.
3. Modüldeki görselleri inceleyip kendi hesabınızla karşılaştırın.
4. `compute_library_distance` çıktısı ile manuel sonucu yan yana kontrol edin.
5. Ders notlarındaki yönlendirmeye (sağ üst → sol alt) uygun çizimler yapmayı
   alışkanlık haline getirin.

Başarılar ve iyi çalışmalar!
