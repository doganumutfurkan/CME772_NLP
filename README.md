# CME772_NLP

CME772 Natural Language Processing dersine ait görsel materyaller, mini demolar ve
çalışma notlarını tek bir yerde toplamak için hazırlanmış bir repo. Her çalışma
konu odaklı kendi klasöründe yer alır; böylece ileride eklenecek projeler
birbirini bozmadan geliştirilebilir.

## İçerik Haritası

| Dizin | Başlık | Açıklama |
| ----- | ------ | -------- |
| `word_alignment/` | Edit Distance ve Hizalama Görselleştirmeleri | Ağırlıklı edit distance hesabını, backtrace izleğini ve döngü tabanlı kod taslaklarını anlatan modül. |
| *(yeni eklemeler)* | | Yeni konular eklendikçe her biri kendi dizininde README ve çalışma notlarıyla yer alacak. |

## Genel Kullanım

1. **Bağımlılıkları kurun**
   - Python 3.9+
   - Ortak kullanılan kütüphaneler: `matplotlib`, `numpy`
   - Modül özelinde ek kütüphaneler ilgili klasörün README dosyasında listelenir

2. **İlgili modül klasörüne geçin** ve README/çalışma notlarını inceleyin.
   - Örneğin edit distance demosu için `word_alignment/` dizinine bakın.
   - Çalıştırma komutları ve örnek çıktılar her modülün README’sinde adım adım açıklanır.

3. **Figürler ve açıklamalar** konsola yazdırılmak yerine çoğunlukla Matplotlib
   pencerelerinde gösterilir. Çizimler kapatılana kadar scriptler bekler.

## Yeni Çalışmalar Eklemek İçin

- Her yeni konu için ayrı bir dizin açın (`language_models/`, `tokenization/` gibi).
- Bu dizinin içerisinde en az bir `README.md` ve ihtiyaç varsa `study.md`
  dokümanı bulunsun.
- Modül içi Python paketlerini dışarıya açmak için `__init__.py` dosyası
  ekleyebilir, tekrar kullanılabilir fonksiyonları burada listeleyebilirsiniz.
- Ortak bağımlılıkların veya veri setlerinin nasıl edinileceği README’de
  belirtilmelidir.

## Yardımcı Dokümanlar

- `word_alignment/README.md`: Edit distance modülünün kullanım talimatları ve
  çıktı görsellerine dair notlar.
- `word_alignment/study.md`: Edit distance ve hizalama konusunu örneklerle
  açıklayan çalışma rehberi.

Katkılar ve geri bildirimler ders arkadaşlarıyla paylaşılabilir; yeni içerik
önerileri için ilgili klasörde bir taslak oluşturmanız yeterli.
