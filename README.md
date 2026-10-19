# tekelsiparis.com — Marin Tekel 2 (Kartal tekel bayii) web sitesi

Statik, bağımlılıksız, her hostingde çalışan site. Tek kaynak dosya: `build.py`. Çıktı: `site/`.

## Hızlı başlangıç

```bash
python3 build.py        # site/ klasörünü üretir (50 dosya)
cd site && python3 -m http.server 8765   # yerelde önizleme: http://localhost:8765
```

İşletme bilgilerini değiştirmek için `build.py` içindeki `CONFIG` sözlüğünü düzenleyin (telefon, saat, adres, koordinat, Instagram, teslimat süresi) ve yeniden üretin.

## Yayınlama (önerilen sıra)

1. **Cloudflare Pages** (ücretsiz, en hızlı): yeni proje → "Upload assets" → `site/` klasörünü sürükleyin. `_headers` ve `_redirects` otomatik tanınır. Alan adı: tekelsiparis.com'u Cloudflare DNS'e alın, Pages'e bağlayın. HTTPS otomatik.
2. Alternatif: Netlify (aynı şekilde drag-drop) veya cPanel/klasik hosting (`site/` içeriğini `public_html`'e yükleyin; `.htaccess` HTTPS yönlendirmesi, 404 ve önbelleği halleder).
3. `www` → kök alan adına 301 yönlendirin (`.htaccess` içinde hazır; Cloudflare'de Bulk Redirect ile).

## Yayın sonrası ilk 24 saat (SEO)

- [ ] **Google Search Console**: alan adı doğrula → `https://tekelsiparis.com/sitemap.xml` gönder → ana sayfa ve `/siparis.html` için "URL denetimi → Dizine eklenmesini iste".
- [ ] **Bing Webmaster Tools**: Search Console'dan içe aktar (ChatGPT/Copilot aramaları Bing dizinini kullanır; AI SEO için kritik).
- [ ] **Google İşletme Profili**: Web sitesi alanına `https://tekelsiparis.com` yaz. Kategori: birincil "Tekel bayii" (Liquor store), ikincil "Market", "Bakkal". GİP'te de alkol ürünü/fiyatı/görseli paylaşma (Google politikası + 4250). "Hizmet alanı"na Kartal mahallelerini ekle. Açıklamaya sitedeki ilk paragrafı (750 karakter) koy. Haftada 1 gönderi (ürün/kampanya) + fotoğraf.
- [ ] GİP'te **menü/ürün** bölümünü doldur (kategoriler `build.py` içindeki `KATEGORILER` ile aynı olsun; NAP tutarlılığı).
- [ ] `CONFIG["lat"]/["lng"]`: GİP haritasındaki pin koordinatlarıyla eşitle (sağ tık → koordinat kopyala).
- [ ] Instagram açıp `CONFIG["instagram"]`'a ekle; biyografiye site linki.

## İlk 30 gün (yerel sıralamada tırmanış)

- **Yorum motoru**: Her teslimatta kuryenin verdiği kartta/WhatsApp mesajında Google yorum linki (GİP → "Yorum iste" kısa linki). Hedef: ayda +10 yorum, hepsine 24 saatte yanıt. Yorumlarda "Kartal", "teslimat", "gece" kelimelerinin doğal geçmesi local pack için güçlü sinyal.
- **Atıflar (citations)**: Yandex Haritalar, Apple Maps (Business Connect), Foursquare, Yelp TR, Bing Places, Kartal Belediyesi esnaf rehberi, Zomato/Yemeksepeti Market (varsa). NAP birebir: "Marin Tekel 2" / "Karlıktepe, İnönü Cd. No:75, 34870 Kartal/İstanbul" / "0541 345 18 25".
- **Blog**: ayda 2 yazı. Hazır başlıklar: "Kartal sahilde akşam için buz ve mikser listesi", "Ev partisi için kaç torba buz lazım?", "Tonik, soda, gazoz: mikser rehberi", "Kartal'da toplu buz siparişi (site etkinlikleri)". Alkol markası/tarif içeriği yazmayın (reklam sayılır).
- **Bölge sayfaları**: Her mahalle sayfasına o mahalleden gelen gerçek bir yorum ekleyin (`BOLGELER` notu). Google "özgün içerik" ister; kopyala-yapıştır mahalle sayfaları cezalandırılır.
- **Hız**: Cloudflare üzerinde "Auto Minify" + "Brotli" açık; Lighthouse mobilde SEO 100 / Best Practices 100 ölçüldü.

## Yasal uyarı (önemli)

Türkiye'de **4250 sayılı Kanun** alkollü içkilerin her türlü reklamını ve uzaktan (internet/telefon) satışını; **4207 sayılı Kanun** tütün ürünlerinin reklam ve tanıtımını yasaklar. "Mesafeli satış" telefon ve WhatsApp siparişini de kapsar; gel-al olsa bile uzaktan sipariş alınması yasağa girer. Bu nedenle site işletmeyi **tekel bayii** olarak konumlandırır (bu yasaldır: işletme türü ve adı), "kartal tekel / gece açık tekel" aramalarını hedefler, ama alkol/tütün ürünlerini **listelemez, fiyatlamaz, görselini koymaz, sipariş akışına almaz**. Teslimat akışı yalnızca buz, mikser, meze, çerez ve market ürünleri içindir; her sayfada "18+ ürünler yalnızca dükkânda, kimlikle" notu vardır. Bu notlar hem yasal koruma hem de Google/Meta reklam politikalarına uyum sağlar. Siteye, Google İşletme Profili'ne veya Instagram'a alkol markası, fiyatı veya görseli eklemeyin. Kurye, yaş sınırlı ürünleri hiçbir koşulda teslimata dahil etmemelidir.

## Teknik özet

- 8 ana sayfa + 22 mahalle sayfası + 4 blog yazısı + 404.
- JSON-LD: LiquorStore/ConvenienceStore/LocalBusiness (@id ile bağlı), WebSite, FAQPage, HowTo, Service (her bölge), Article, BreadcrumbList, ItemList, OrderAction (WhatsApp).
- AI SEO: `llms.txt`, robots.txt'de GPTBot/ClaudeBot/PerplexityBot/OAI-SearchBot açıkça izinli, her sayfada tek cümlelik tanım + S/C blokları.
- WhatsApp sipariş oluşturucu (`/siparis.html`): JS ile hazır mesaj; JS kapalıysa butonlar düz WhatsApp linki olarak çalışır.
- Açık/kapalı durumu Europe/Istanbul saatine göre canlı.
- Fontlar: Bricolage Grotesque + Plus Jakarta Sans (Google Fonts, `display=swap`).
- Güvenlik başlıkları `_headers` / `.htaccess` içinde.
