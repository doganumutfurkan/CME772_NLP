# Edit Distance Study Guide

Bu doküman, `word_alignment` modülündeki araçların nasıl çalıştığını ve aynı zamanda edit distance gibi temel NLP kavramlarının ne ifade ettiğini özetler.

## 1. Modüldeki Bileşenler

### 1.1 `EditDistanceConfig`
- `source_word` ve `target_word` alanlarında kıyaslanacak kelimeleri tutar.
- `costs` alanı ekleme (`insertion`), silme (`deletion`) ve yerine koyma (`substitution`) işlemlerinin ağırlıklarını belirler. Ders notlarında olduğu gibi ekleme ve silme 1, yerine koyma 2 değerindedir.

### 1.2 `EditDistanceComputation`
- Dinamik programlama (DP) tablosunu oluşturur ve her hücre için toplam maliyeti hesaplar.
- Her adım için hangi hareketin (sol → ekleme, aşağı → silme, diagonal → yerine koyma) seçildiğini kaydeder.
- `_orient_operations_for_display` fonksiyonu sayesinde tabloyu derslerdeki sağ-üstten sol-alta ilerleyen anlatıma göre düzenler.

### 1.3 Görselleştirme Yardımcıları
- `build_alignment_figures` DP heatmap’ini, manuel tabloyu ve anlatım metinlerini döndürür.
- Hücrelerdeki değerler ve oklar çakışmasın diye etiketler yarı saydam kutuların içine yerleştirilir.
- Backtrace yolu hem heatmap’te hem de manuel tabloda belirgin renklerle vurgulanır.

### 1.4 Döngü Odaklı Demo (`loop_similarity_demo.py`)
- `run_loop_similarity_demo` fonksiyonu derslerdeki “her karakteri döngüyle gez ve karşılaştır” yaklaşımını adım adım gösterir.
- Önce manuel DP tablosu ve sözel anlatım gelir, ardından kütüphane kontrolü ile sonuç doğrulanır.

### 1.5 Kütüphane Doğrulaması
- `LibraryDistanceCheck` sınıfı tercihen `textdistance` paketini kullanır.
- Paket yoksa projedeki yedek fonksiyon aynı ağırlıklarla mesafeyi hesaplar; böylece sonuç hep alınır.

## 2. Edit Distance Algoritması

1. **Başlangıç Satırı ve Sütunu**: Sol alt köşedeki 0, iki kelime de boşken maliyetin sıfır olduğunu gösterir. İlk satır ve sütuna doğru ilerledikçe artan ekleme/silme maliyetleri doldurulur.
2. **DP Tablosu Doldurma**: Her hücrede üç ihtimal hesaplanır:
   - Sol hücre + ekleme maliyeti (`insertion`)
   - Alt hücre + silme maliyeti (`deletion`)
   - Diyagonal hücre + (aynı karakterse 0, farklıysa `substitution` maliyeti)
   En küçük değer seçilir ve adım türü kaydedilir.
3. **Backtrace**: Sağ üst köşeden başlayarak seçilen adımları takip eder, sol alt köşede biter. Bu yol en düşük maliyetli düzenleme sırasını verir.

## 3. Döngü ile Karakter Karşılaştırması

- İki kelimenin uzunluklarına göre iç içe döngü kurulur.
- Her kombinasyon için yukarıdaki üç maliyet olasılığı hesaplanır.
- Python’da `for i, src_char in enumerate(source_word):` şeklinde dış döngü, `for j, tgt_char in enumerate(target_word):` şeklinde iç döngü kullanmak yaygındır.
- Hesaplanan değerler DP matrisine yazılır, seçilen operasyon ayrı bir matriste tutulur.

## 4. Sonucun Doğrulanması

- Manuel hesaplanan değer ile `textdistance` (veya yedek fonksiyon) sonucu karşılaştırılır.
- Demo, her iki sonucu aynı figürde yan yana göstererek hataları hızlıca fark etmenizi sağlar.

## 5. NLP’de Edit Distance Kullanımları

- **Yazım Düzeltme**: Yanlış yazılan kelimenin sözlükteki hangi kelimeye en az adımla dönüştüğünü bulur.
- **Otomatik Değerlendirme**: Öğrenci yanıtları veya çeviri çıktıları ile referans metinler arasındaki farkı ölçer.
- **Konuşma Tanıma**: Ses tanıma sistemlerinin çıktılarıyla referans transkriptler arasındaki edit distance, doğruluk ölçütü olarak kullanılır.
- **DNA/Sekans Analizi**: NLP dışındaki alanlarda da diziler arasındaki benzerlik için aynı mantık kullanılır.

## 6. Çalışma Tavsiyeleri

1. Önce küçük kelimelerle tabloyu elle doldurun.
2. Backtrace yolunu farklı renklerle çizin; hangi adımı neden seçtiğinizi açıklayın.
3. Modüldeki `EditDistanceConfig` ile farklı maliyetler verip sonuçların nasıl değiştiğini inceleyin.
4. `textdistance` çıktısı ile kendi hesabınızı kıyaslayın; farklı sonuç varsa DP tablosundaki ilgili hücreleri tekrar kontrol edin.
5. Derslerdeki örnek yönelim (sağ üst → sol alt) ile projedeki görselleştirmelerin birebir uyduğunu unutmayın.

Başarılar!
