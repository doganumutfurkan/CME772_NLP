# Shannon Game & Perpleksite demosu nasıl kullanılır?

Bu rehber, depodaki her dosyanın görevini anlatır, `demo.py` betiğinin
çalıştırılmasını adım adım gösterir ve projede canlandırılan kavramları daha
ayrıntılı biçimde açıklar. Hem hızlı başlangıç hem de ders notu olarak
kullanabilirsiniz.

## Proje dosyaları

- `corpus.py` – Dahili Shakespeare alıntısını veya diskteki özel bir metni
  yüklemek için yardımcı işlevler. Kendi korpusunuzu eklemek isterseniz burayı
  değiştirin.
- `demo.py` – Ana senaryo. Ön işlemeyi yapar, her N-gram derecesini eğitir,
  düzeltme (smoothing) stratejilerini uygular, Shannon örnekleri üretir ve
  perpleksite karşılaştırma tablosunu yazdırır.
- `ngram_model.py` – Sayaç tabanlı `NGramModel` sınıfını ve koşullu olasılıkları
  hesaplayan yardımcılarını içerir.
- `perplexity.py` – `perplexity(model, sentences, smoother)` yardımcı işlevini ve
  olasılıkların nasıl `PP(W)` değerine dönüştürüldüğünü açıklayan yorumları barındırır.
- `preprocessing.py` – Normalizasyon, cümle/kelime ayrıştırma. Önce NLTK'yi dener,
  NLTK veri paketleri yoksa düzenli ifadeye dayalı bir ayrıştırıcıya geri döner.
- `sampling.py` – Shannon Game üretecini uygular. Tarihçe verildiğinde, (isteğe
  bağlı olarak düzeltmeli) olasılıklara göre bir sonraki kelimeyi seçer.
- `smoothing.py` – `NoSmoothing`, `StupidBackoffSmoother`, `KatzBackoffSmoother`
  ve `InterpolationSmoother` sınıflarını içerir. Doküman içindeki denklemlerle
  çapraz referanslanmıştır.
- `requirements.txt` – Gerekli Python bağımlılıklarını listeler.

Her modül, tek başına deneme yapabilmeniz için `if __name__ == "__main__":`
korumalı küçük bir blok içerir (örneğin ham sayımları yazdırmak veya tek bir
smoother'dan örnek almak için).

## Demo nasıl çalıştırılır?

1. Gerekli paketi yükleyin:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Proje dizininden demo betiğini çalıştırın:

   ```bash
   python demo.py
   ```

3. İsteğe bağlı ayarlar:
   - `demo.py` dosyasına `--corpus` bayrağı vererek kendi metin dosyanızı
     kullanabilirsiniz.
   - Betiğin başındaki interpolasyon ağırlıklarını veya backoff katsayılarını
     değiştirip tekrar çalıştırarak tablodaki perpleksite değişimini gözleyin.

Betiğin çıktısı, her model için örnek cümleler ve farklı düzeltme yöntemleriyle
hesaplanan perpleksite değerlerini gösteren bir tablo içerir. Bu çıktıları
kullanarak hangi ayarların daha akıcı metin ürettiğini ve hangi ayarların daha
iyi tahmin performansı sunduğunu değerlendirebilirsiniz.

## Kavram özetleri

### Shannon Game

Shannon Game, modelin koşullu olasılık dağılımından sıradaki kelimeyi çekerek
metin üretir. Sanki modelle "sonraki kelime ne olur?" oyununu oynuyorsunuz.

```python
from shannon_game_perplexity_backoff_interpolation.sampling import shannon_game

for word in shannon_game(model, max_tokens=12, smoother=smoother):
    print(word, end=" ")
```

Daha yüksek dereceli modeller (bigram, trigram) daha uzun tarihçeler kullandığı
için üretim genellikle unigramlara göre daha tutarlı olur.

### Perpleksite

Perpleksite, bir dizinin modele ne kadar sürpriz olduğunu ölçer. :math:`w_1, \ldots, w_N`
için `perplexity.py` dosyasında uygulanan formül şudur:

```text
PP(W) = P(w_1, \ldots, w_N)^{-1/N}
```

Buradaki olasılık terimi koşullu olasılıkların çarpımına açılır:
:math:`P(w_1, \ldots, w_N) = \prod_{i=1}^{N} P(w_i \mid h_i)` ve :math:`h_i`
daha önceki bir veya iki kelimeyi temsil eder. Perpleksite ne kadar düşükse model
bu diziyi o kadar olası görmüştür ve tahmin yeteneği o kadar iyidir.

### Geriye dönüş (Backoff) düzeltmesi

Backoff yöntemleri, görülmeyen N-gram'lerde daha düşük dereceli modellere iner.
Demo içinde kullanılan Stupid Backoff, alt model olasılığını sabit bir
:math:`\alpha` katsayısıyla ölçekler:

```text
P_{SB}(w|h) =
  \begin{cases}
    \frac{c(hw)}{c(h)} & c(hw) > 0 \\
    \alpha P_{SB}(w|h') & \text{aksi halde}
  \end{cases}
```

Katz Backoff, gözlenen sayımları :math:`d` kadar iskonto eder ve kalan kütleyi
:math:`\alpha(h)` aracılığıyla yeniden dağıtır.

### Lineer enterpolasyon

Enterpolasyon, farklı N-gram derecelerini toplamı bire eşit olan
:math:`\lambda_i` ağırlıklarıyla karıştırır:

```text
P_{interp}(w|h) = \sum_{i=1}^{n} \lambda_i P_i(w|h_{i-1})
```

`demo.py` içindeki ağırlıkları değiştirerek uzun veya kısa tarihçelere ne kadar
ağırlık verdiğinizi kontrol edebilir ve bunun Shannon çıktıları ile perpleksite
sonuçlarını nasıl etkilediğini inceleyebilirsiniz.

---

Serbestçe deneme yapın: farklı korpuslar ekleyin, cümle sınır belirteçleri
kullanın veya yeni değerlendirme metrikleri ekleyin. Modüler yapı bu tür
uzantıları kolaylaştırmak için tasarlanmıştır.
