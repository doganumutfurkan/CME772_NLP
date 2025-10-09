# Word Alignment & Edit Distance Modülü

Bu klasör, derslerde elle doldurulan edit distance tablolarını yeniden üretmek ve
süreci görsel olarak açıklamak için hazırlanmış araçları içerir. Görseller hem
Dinamik Programlama (DP) matrisini hem de backtrace adımlarını derslerdeki
"sağ üstten sol alta" anlatımıyla sunar.

## Dosya Özeti

- **`edit_distance_tools.py`** – Edit distance hesabını yapan veri sınıfları,
  DP matrisini ve backtrace’i oluşturan yardımcı fonksiyonlar, ayrıca görselleri
  üreten yüksek seviyeli arabirimler.
- **`loop_similarity_demo.py`** – Döngü odaklı anlatımı, manuel tabloyu ve
  kütüphane doğrulamasını arka arkaya gösteren örnek script.
- **`__init__.py`** – Modülün dışarı açtığı sınıf ve fonksiyonların kısayol
  importlarını içerir.
- **`study.md`** – Edit distance kavramını, kullanılan kodları ve örnekleri
  adım adım açıklayan çalışma rehberi.

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate  # Windows için: .venv\\Scripts\\activate
pip install -r requirements.txt  # Eğer toplu bağımlılık dosyası yoksa aşağıdaki bireysel kurulumları uygulayın
pip install matplotlib numpy textdistance
```

> `textdistance` isteğe bağlıdır. Script, kütüphane bulunmazsa dahili yedek
> fonksiyonla hesap yapmaya devam eder.

## Demo Nasıl Çalıştırılır?

```bash
python -m word_alignment.loop_similarity_demo
```

Script şu sıralamayla Matplotlib pencereleri açar:

1. **DP Heatmap** – Hücre değerleri, yön bilgisi ve backtrace yolu sağ üstten
   sol alta doğru vurgulanır.
2. **Manuel Tablo** – Derslerdeki gibi kelimeler sol alt köşeyi referans alır,
   her satır adımının açıklaması tabloda yer alır.
3. **Kütüphane Karşılaştırması** – Manuel sonuç ile `textdistance`
   kütüphanesinden gelen sonuç yan yana gösterilir.

Tüm figürler kapatılmadan script sonlanmaz; böylece anlatımı durdurarak not
alabilirsiniz.

## Özelleştirme

- `compute_edit_distance` fonksiyonuna farklı kelimeler ve maliyetler vererek
  yeni tablolar oluşturun:
  ```python
  from word_alignment.edit_distance_tools import compute_edit_distance

  result = compute_edit_distance("flaw", "lawn", substitution_cost=1)
  ```
- Görselleri dosyaya aktarmak için üretilen figürleri kaydedin:
  ```python
  from word_alignment.edit_distance_tools import plot_manual_table

  fig = plot_manual_table(result, show=False)
  fig.savefig("manual_table.png", dpi=200)
  ```
- `loop_similarity_demo.demonstrate_loop_similarity` fonksiyonu kendi kelimelerinizle
  çağrıldığında aynı öyküyü yeni örnek için tekrar oluşturur.

## İlgili Dokümanlar

- [study.md](./study.md): Kavram özeti, kod akışı ve örnek çözümler.
- Repodaki kök [README](../README.md): Farklı modüller eklenirken izlenecek
  genel kuralları listeler.

Sorularınız veya geliştirme önerileriniz için ders tartışma kanallarını
kullanabilir, görselleri özelleştirmek adına pull request açabilirsiniz.
