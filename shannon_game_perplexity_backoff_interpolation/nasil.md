# Shannon Game & Perpleksite demosu nasıl kullanılır?

Bu belge projedeki dosyaları açıklar, `demo.py` betiğini nasıl çalıştıracağınızı
gösterir ve temel kavramlar hakkında kısa özetler sunar.

## Proje dosyaları

- `corpus.py` – Dahili Shakespeare alıntısını veya diskten metin okumayı sağlar.
- `demo.py` – Ön işleme, model eğitimi, Shannon örneklemesi ve perpleksite
  değerlendirmesini yürütür.
- `ngram_model.py` – Tüm düzeltme yöntemlerinin paylaştığı N-gram modellerini
  uygular.
- `perplexity.py` – `perplexity(model, sentences, smoother)` fonksiyonunu içerir.
- `preprocessing.py` – Metni normalleştirir ve NLTK ile cümle/kelime
  tokenizasyonu yapar (NLTK bulunamazsa düzenli ifade tabanlı bir yedek kullanır).
- `sampling.py` – Tarihçe verildiğinde bir sonraki kelimeyi çeken Shannon Game
  üretecini sağlar.
- `smoothing.py` – `NoSmoothing`, `StupidBackoffSmoother`,
  `KatzBackoffSmoother` ve `InterpolationSmoother` stratejilerini tanımlar.
- `requirements.txt` – Gerekli Python bağımlılığını (NLTK) listeler.

Her modül hızlı denemeler için `if __name__ == "__main__":` bloğu içerir.

## Demo nasıl çalıştırılır?

```bash
python -m pip install -r requirements.txt
python demo.py
```

## Kavram özetleri

### Shannon Game

Shannon Game, öğrenilen olasılık dağılımından ardışık kelimeler seçer. Koddan bir
örnek:

```python
history = ("to", "be")
next_word = model.distribution(history)["that"]
```

### Perpleksite

Perpleksite, bir dizinin modele ne kadar sürpriz olduğunu ölçer. :math:`w_1, \ldots, w_N`
için formül `perplexity.py` içerisinde uygulanır:

```text
PP(W) = P(w_1, \ldots, w_N)^{-1/N}
```

### Geriye dönüş (Backoff) düzeltmesi

Geriye dönüş yaklaşımları, gözlenmeyen N-gram'lerde daha düşük dereceli modele
iner. Stupid Backoff için olasılık:

```text
P_{SB}(w|h) =
  \begin{cases}
    \frac{c(hw)}{c(h)} & c(hw) > 0 \\
    \alpha P_{SB}(w|h') & \text{aksi halde}
  \end{cases}
```

### Katz backoff

Katz yöntemi gözlenen sayımları :math:`d` ile iskonto eder ve kalan kütleyi
paylaştırır:

```text
P_{K}(w|h) =
  \begin{cases}
    \frac{c(hw) - d}{c(h)} & c(hw) > 0 \\
    \alpha(h) P_{K}(w|h') & \text{aksi halde}
  \end{cases}
```

### Lineer enterpolasyon

Enterpolasyon farklı N-gram derecelerini :math:`\lambda_i` ağırlıklarıyla
karıştırır:

```text
P_{interp}(w|h) = \sum_{i=1}^{n} \lambda_i P_i(w|h_{i-1})
```

Ağırlıklarla `demo.py` içerisinde oynayarak dağılımın nasıl değiştiğini
inceleyebilirsiniz.
