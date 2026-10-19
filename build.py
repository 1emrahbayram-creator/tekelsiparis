#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tekelsiparis.com — Marin Tekel 2 (Kartal) statik site üreticisi.
Çalıştır:  python3 build.py   →  site/ klasörü oluşur. Tek komut, bağımlılık yok.
Tüm işletme bilgileri CONFIG içinde; değiştir → yeniden üret.
"""
import json, os, re, datetime, html as htmlmod

# ─────────────────────────────── KONFİG ───────────────────────────────
CONFIG = {
    "brand": "Marin Tekel 2",
    "short": "Marin",
    "domain": "https://tekelsiparis.com",
    "phone_e164": "+905413451825",
    "phone_display": "0541 345 18 25",
    "phone_intl": "+90 541 345 18 25",
    "whatsapp": "905413451825",
    "street": "İnönü Cd. No:75",
    "district": "Karlıktepe",
    "ilce": "Kartal",
    "city": "İstanbul",
    "postal": "34870",
    "address_full": "Karlıktepe, İnönü Cd. No:75, 34870 Kartal/İstanbul",
    "lat": "40.8966",   # Yaklaşık — Google İşletme Profili'ndeki pin ile eşitleyin
    "lng": "29.1852",
    "opens": "08:00",
    "closes": "02:00",
    "rating": "5.0",
    "review_count": "9",
    "maps_url": "https://www.google.com/maps/search/?api=1&query=Marin+Tekel+2+%C4%B0n%C3%B6n%C3%BC+Cd.+No:75+Karl%C4%B1ktepe+Kartal",
    "maps_embed": "https://www.google.com/maps?q=Marin+Tekel+2+%C4%B0n%C3%B6n%C3%BC+Cd.+No:75+Karl%C4%B1ktepe+Kartal+%C4%B0stanbul&output=embed&z=16",
    "instagram": "",  # varsa: https://instagram.com/...
    "eta": "20–40 dk",
    "founded": "2019",
}
C = CONFIG
TODAY = datetime.date.today().isoformat()
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

def esc(s): return htmlmod.escape(s, quote=True)
def wa(msg): 
    from urllib.parse import quote
    return f"https://wa.me/{C['whatsapp']}?text={quote(msg)}"

WA_DEFAULT = wa("Merhaba Marin, sipariş vermek istiyorum.\nAdres: \nÜrünler: ")

# ─────────────────────────────── BÖLGELER ───────────────────────────────
# (slug, ad, tahmini süre, yakın yerler, özgün not, ilçe)
BOLGELER = [
 ("karliktepe","Karlıktepe","10–20 dk","İnönü Caddesi ve Tecerdağı Caddesi çevresi","Dükkânımız tam burada, İnönü Caddesi üzerinde. Karlıktepe içinde siparişler çoğu zaman 15 dakikayı bulmadan kapıda.","Kartal"),
 ("yukari","Yukarı Mahalle","15–25 dk","Kartal Belediyesi ve Kartal Çarşı çevresi","Kartal'ın en işlek merkezine iki adım mesafedeyiz. Çarşı trafiğine takılmadan ara sokaklardan ulaşırız.","Kartal"),
 ("orta","Orta Mahalle","15–25 dk","Kartal Meydanı ve Üsküdar Caddesi hattı","Meydan çevresindeki apartman ve sitelere düzenli servisimiz var; akşam saatlerinde yoğun talep gelen bölgelerimizden.","Kartal"),
 ("kordonboyu","Kordonboyu","15–30 dk","Kartal sahili, iskele ve Kartal Meydanı","Sahil kenarında oturan ya da iskele civarında akşam geçirenlerin en çok aradığı adres biziz: içecek, buz ve atıştırmalık tek seferde.","Kartal"),
 ("cumhuriyet","Cumhuriyet Mahallesi","15–25 dk","E-5 kuzeyi, Ankara Caddesi çevresi","E-5'in kuzey tarafındaki sitelere düzenli gidiyoruz; gece geç saatlerde bile servis devam eder.","Kartal"),
 ("hurriyet","Hürriyet Mahallesi","15–25 dk","E-5 ile Yakacık Caddesi arası","Yoğun konut dokusu nedeniyle aynı sokağa birden fazla teslimatı birleştirir, süreyi kısa tutarız.","Kartal"),
 ("petrol-is","Petrol-İş Mahallesi","15–25 dk","Petrol-İş Caddesi çevresi","Karlıktepe'ye komşu mahalle; motorlu kuryeyle çoğu adrese 20 dakikanın altında ulaşırız.","Kartal"),
 ("esentepe","Esentepe","15–30 dk","Anadolu Adliyesi ve Ankara Caddesi çevresi","Adliye çevresindeki ofisler için gündüz, siteler için akşam teslimatı yapıyoruz.","Kartal"),
 ("cavusoglu","Çavuşoğlu Mahallesi","15–30 dk","Yakacık Caddesi çevresi","Yakacık yönüne giden ana hat üzerinde olduğu için rotamızın doğal bir parçası.","Kartal"),
 ("yali","Yalı Mahallesi","20–30 dk","Kartal sahil yolu, Dragos yönü","Sahil siteleri ve yazlık havasındaki Dragos yamaçlarına düzenli servis.","Kartal"),
 ("yunus","Yunus Mahallesi","20–30 dk","Yunus sahili ve Cevizli yönü","Sahil kenarı sitelere akşam saatlerinde hızlı servis; buz ve soğuk içecek talebi burada yüksek.","Kartal"),
 ("atalar","Atalar","20–30 dk","Atalar Çarşı ve Atalar sahili","Atalar'ın çarşı ve sahil tarafına tek rotada ulaşıyoruz.","Kartal"),
 ("topselvi","Topselvi","15–30 dk","Topselvi Caddesi, Soğanlık metro yakını","Metro çevresindeki yeni siteler için en sık aranan adreslerden biriyiz.","Kartal"),
 ("gumuspinar","Gümüşpınar","20–30 dk","Yakacık'a geçiş hattı","Yakacık rotasında olduğu için siparişleri birleştirip hızla ulaşıyoruz.","Kartal"),
 ("ugur-mumcu","Uğur Mumcu Mahallesi","20–35 dk","Aydos Ormanı etekleri, Samandıra sınırı","Kartal'ın kuzey ucunda olmasına rağmen akşam servisi düzenli devam eder.","Kartal"),
 ("soganlik","Soğanlık","15–30 dk","Soğanlık metro (M4) ve Soğanlık Caddesi","Metro çıkışı çevresindeki apartmanlara sık gittiğimiz için adresleri iyi biliriz.","Kartal"),
 ("cevizli","Cevizli","20–40 dk","Hastane metro, Dr. Lütfi Kırdar Şehir Hastanesi, Maltepe sınırı","Hastane çevresinde refakatçiler için gece de servis veriyoruz.","Kartal"),
 ("orhantepe","Orhantepe","20–35 dk","Dragos sahili ve Orhantepe sırtları","Dragos'un yokuşlarına motorlu kuryeyle sorunsuz çıkıyoruz.","Kartal"),
 ("yakacik-carsi","Yakacık Çarşı","20–35 dk","Yakacık meydanı ve Aydos Ormanı girişi","Yakacık'ın tarihi çarşısı ve çevresindeki konutlara akşam servisi.","Kartal"),
 ("yakacik-yeni","Yakacık Yeni Mahalle","20–35 dk","Yakacık–Adnan Kahveci metro, E-5 hattı","E-5 kenarındaki siteler ve metro çevresi için sık gittiğimiz bir rota.","Kartal"),
 ("maltepe","Maltepe (Cevizli–Altayçeşme hattı)","30–45 dk","Maltepe sahil, Altayçeşme, Cevizli sınırı","Kartal sınırına yakın Maltepe adreslerine de gidiyoruz; sipariş öncesi adresinizi WhatsApp'tan teyit ediyoruz.","Maltepe"),
 ("pendik-kaynarca","Pendik Kaynarca","30–45 dk","Kaynarca metro ve Pendik sınırı","Kartal–Pendik sınırındaki Kaynarca adreslerine akşam saatlerinde servis.","Pendik"),
]

# ─────────────────────────────── ÜRÜN KATEGORİLERİ ───────────────────────────────
KATEGORILER = [
 ("Buz","🧊","Torba buz her saat, derin dondurucudan termal çantaya. Kartal'da gece buz arayanların ilk adresi.",["Torba buz (küp)","Buz kalıbı","Kırık buz"]),
 ("Soda, Tonik & Mikserler","🍋","Tonik, soda, gazoz, kola, limon, nane, zencefil. Masanın eksiği kalmasın.",["Tonik","Soda & sade soda","Kola / gazoz","Limonata","Limon & nane","Enerji içeceği","Meyve suyu"]),
 ("Meze & Çerez","🥜","Leblebi, fıstık, çekirdek, cips, kraker, zeytin, peynir, turşu. Sofraya bir tur daha.",["Kuruyemiş & leblebi","Çekirdek","Cips çeşitleri","Kraker & çubuk kraker","Beyaz peynir & zeytin","Turşu","Salatalık, domates, limon"]),
 ("Soğuk İçecekler","🥤","Su, ayran, soğuk kahve, buzlu çay. Hepsi dolaptan çıkar.",["Su (0,5L / 1,5L / 5L)","Ayran","Soğuk kahve","Buzlu çay","Maden suyu"]),
 ("Çikolata & Tatlı","🍫","Tablet çikolata, gofret, sakız, şeker, dondurma.",["Tablet çikolata","Gofret","Sakız & şeker","Algida dondurma"]),
 ("Çakmak, Kibrit, Pil & Küçük Eşya","🔌","Çakmak, kibrit, pil, şarj kablosu, ampul, çöp poşeti, bardak.",["Çakmak & kibrit","Pil (AA/AAA)","Şarj kablosu","Çöp poşeti","Peçete, bardak, tabak"]),
 ("Kahvaltılık & Temel Gıda","🥚","Ekmek, süt, yumurta, peynir, çay, şeker, makarna. Sabah için de buradayız.",["Ekmek","Süt & yoğurt","Yumurta","Çay & kahve","Makarna, pirinç","Tuz, şeker, yağ"]),
 ("Kişisel Bakım & Temizlik","🧴","Gece yarısı biten şampuan, diş macunu, deterjan, tuvalet kağıdı.",["Şampuan, sabun","Diş macunu & fırçası","Tıraş ürünleri","Deterjan","Tuvalet kağıdı"]),
 ("Bebek & Evcil Hayvan","🍼","Bebek bezi, ıslak mendil, mama. Acil ihtiyaçta bizi arayın.",["Bebek bezi","Islak mendil","Kedi & köpek maması"]),
]

# ─────────────────────────────── SSS ───────────────────────────────
SSS = [
 ("Alkollü içecek veya sigara sipariş edebilir miyim?", "Hayır. 4250 ve 4207 sayılı kanunlar gereği alkollü içki ve tütün ürünleri telefon, WhatsApp ya da internetten sipariş edilemez, eve gönderilemez. Bu ürünler yalnızca dükkânımızda, 18 yaş üstüne kimlik kontrolüyle satılır. Buz, tonik, soda, meze, çerez ve diğer her şeyi kapınıza getiriyoruz."),
 ("Kartal'da tekel siparişi nasıl veririm?", f"Üç yol var: <strong>{C['phone_display']}</strong> numarasını arayın, aynı numaraya WhatsApp'tan yazın ya da bu sitedeki sipariş sayfasından ürünleri seçip tek dokunuşla WhatsApp mesajı oluşturun. Adres ve ürünleri alır, hazırlar, yola çıkarırız."),
 ("Teslimat ne kadar sürer?", f"Karlıktepe ve komşu mahallelerde ortalama {C['eta']}. Cevizli, Yakacık ve Dragos gibi uzak noktalarda 40 dakikaya kadar çıkabilir. Yoğun saatlerde sipariş alırken tahmini süreyi söyleriz."),
 ("Eve teslimatta fiyat farkı var mı?", "Hayır. Teslimatta da dükkândaki raf fiyatı geçerlidir. &ldquo;Gel-al fiyatına eve teslim&rdquo; sözümüzün anlamı tam olarak budur. Varsa teslimat ücreti sipariş sırasında açıkça söylenir."),
 ("Saat kaça kadar açıksınız?", f"Her gün {C['opens']}&ndash;{C['closes']} arası açığız. Gece 02:00'ye kadar sipariş alırız; bayram ve özel günlerde saat değişirse Google İşletme Profilimizde ve bu sitede duyururuz."),
 ("Hangi bölgelere teslimat yapıyorsunuz?", "Kartal'ın tüm mahallelerine (yaş sınırlı ürünler hariç): Karlıktepe, Yukarı, Orta, Kordonboyu, Cumhuriyet, Hürriyet, Petrol-İş, Esentepe, Çavuşoğlu, Yalı, Yunus, Atalar, Topselvi, Gümüşpınar, Uğur Mumcu, Soğanlık, Cevizli, Orhantepe, Yakacık. Ayrıca Maltepe'nin Cevizli sınırı ve Pendik Kaynarca'ya da gidiyoruz."),
 ("Minimum sipariş tutarı var mı?", "Küçük siparişleri de alıyoruz. Bölgeye göre minimum tutar değişebilir; WhatsApp'tan adresinizi yazın, anında söyleyelim."),
 ("Ödeme nasıl yapılıyor?", "Kapıda nakit veya kredi/banka kartıyla ödeyebilirsiniz. Kurye yanında POS cihazı taşır."),
 ("Listede olmayan bir ürün istesem?", "Sorun. Dükkânda yoksa ve bulabiliyorsak sizin için temin ederiz (yaş sınırlı ürünler hariç). Müşterilerimizin Google yorumlarında en çok övdüğü şey bu."),
 ("Siparişimi nasıl takip ederim?", "Kurye yola çıkınca WhatsApp'tan haber veririz. Kapıya yaklaştığında sizi arar."),
 ("Buz ve soğuk içecek gerçekten soğuk mu geliyor?", "Evet. İçecekler dolaptan, buz derin dondurucudan çıkar ve termal çantayla taşınır."),
 ("Gece 00:00'dan sonra da açık mısınız?", "Evet, 02:00'ye kadar hem dükkân açık hem teslimat devam ediyor. Kartal'da gece açık tekel arayanların çoğu bize ulaşır; buz ve mikser siparişleri 02:00'ye kadar kapıda."),
 ("Toplu buz ve mikser siparişi veriyor musunuz?", "Evet. Ev partisi, site etkinliği ve ofisler için toplu buz, tonik, soda ve çerez siparişi alıyoruz. Bir gün önceden haber verirseniz stok hazırlarız."),
]

# ─────────────────────────────── BLOG ───────────────────────────────
BLOG = [
 {
  "slug":"kartal-gece-acik-tekel",
  "title":"Kartal'da Gece Açık Tekel: 02:00'ye Kadar Açığız",
  "desc":"Kartal'da gece açık tekel mi arıyorsunuz? Marin her gün 02:00'ye kadar açık; buz, tonik, soda ve meze eve geliyor. Yaş sınırlı ürünler dükkânda, kimlikle.",
  "date":"2026-10-10",
  "body":"""
<p>Saat gece 00:30. Misafir var, buz bitti, tonik yok. Kartal'da bu saatte açık tekel bulmak sandığınızdan zor: çoğu dükkân 23:00'te, geç kalanı 00:00'da kepenk indirir.</p>
<h2>Marin neden gece de açık?</h2>
<p>Karlıktepe'de, İnönü Caddesi üzerindeki dükkânımız her gün <strong>08:00'den 02:00'ye</strong> kadar açık. Bu saat aralığını özellikle sahil ve site yoğunluğu olan Kartal için seçtik: akşam yürüyüşünden dönen, geç saatte çalışan, hastane çevresinde refakatçi olarak kalan insanlar için.</p>
<h2>Gece siparişi nasıl verilir?</h2>
<ol>
<li><strong>Arayın:</strong> <a href="tel:%(tel)s">%(phone)s</a></li>
<li><strong>WhatsApp yazın:</strong> adresinizi ve istediklerinizi tek mesajda gönderin.</li>
<li><strong>Siteden seçin:</strong> <a href="/siparis.html">sipariş sayfasında</a> ürünleri işaretleyin, tek dokunuşla WhatsApp mesajı hazır.</li>
</ol>
<h2>Gece hangi bölgelere gidiyoruz?</h2>
<p>Gündüz hangi mahalleye gidiyorsak gece de aynı: Karlıktepe, Kordonboyu, Yukarı, Orta, Hürriyet, Cumhuriyet, Soğanlık, Cevizli, Yakacık ve diğer tüm Kartal mahalleleri. Gece trafiği olmadığı için teslimat çoğu zaman gündüzden bile hızlı, ortalama <strong>%(eta)s</strong>.</p>
<h2>Gece en çok ne isteniyor?</h2>
<p>Sırasıyla: torba buz, tonik ve soda, limon-nane, çerez ve cips, çikolata, çakmak. Hepsi stokta, hepsi raf fiyatına.</p>
<h2>Alkollü içecek eve geliyor mu?</h2>
<p>Hayır ve bunu açıkça yazıyoruz: 4250 sayılı Kanun alkollü içkilerin uzaktan satışını ve eve teslimini yasaklıyor. Bu ürünler yalnızca dükkânımızda, 18 yaş üstüne kimlik kontrolüyle satılır. Dükkân 02:00'ye kadar açık; masanın geri kalanını biz kapınıza getiriyoruz.</p>
<h2>Gece teslimatta fiyat farkı var mı?</h2>
<p>Yok. Gündüz ne ödüyorsanız gece de onu ödersiniz. <a href="/blog/gel-al-fiyatina-eve-teslim.html">Gel-al fiyatı sözümüzü</a> gece de tutuyoruz.</p>
"""},
 {
  "slug":"kartal-tekel-siparisi-nasil-verilir",
  "title":"Kartal'da Tekelden Eve Sipariş Nasıl Verilir? Kısa Rehber",
  "desc":"Kartal'da WhatsApp veya telefonla tekelden buz, mikser ve meze siparişi vermenin en hızlı yolu. Adres ipuçları, hangi ürünler gelir, ödeme ve süreler.",
  "date":"2026-10-05",
  "body":"""
<p>Uygulama indirmek, üye olmak, sepet doldurup minimum tutara takılmak... Mahalle tekelinden sipariş vermek bunların hiçbirini gerektirmez. İşte Kartal'da Marin'den buz, mikser ve meze siparişi vermenin en kısa yolu. (Alkollü içki ve tütün ürünleri mevzuat gereği sipariş akışında yoktur; yalnızca dükkânda, kimlikle.)</p>
<h2>1. Adresinizi tek seferde doğru yazın</h2>
<p>Kuryenin en çok zaman kaybettiği şey eksik adrestir. Şu kalıp hiç şaşmaz: <em>Mahalle, cadde/sokak, bina adı veya no, daire, varsa site adı ve blok, kapı zili/isim.</em> Örnek: "Kordonboyu Mah. Ankara Cad. No:12 Deniz Apt. D:5, zil: Yılmaz".</p>
<h2>2. Ürünleri yazın ya da siteden seçin</h2>
<p>"2 torba buz, 4 tonik, 2 soda, 1 limon, 1 kuruyemiş" gibi kısa yazmanız yeter. Markayı belirtmezseniz en çok tercih edileni göndeririz. <a href="/siparis.html">Sipariş sayfasında</a> ürünleri işaretleyip tek dokunuşla hazır WhatsApp mesajı da oluşturabilirsiniz.</p>
<h2>3. Onay ve süre</h2>
<p>Mesajınızı aldığımızda stok ve tahmini süreyi yazarız. Karlıktepe ve çevresi için ortalama %(eta)s.</p>
<h2>4. Ödeme</h2>
<p>Kapıda nakit ya da kart. Kurye POS taşır, üstü eksik kalmaz.</p>
<h2>5. Teslimat</h2>
<p>Kurye kapınıza yaklaşınca arar. Soğuk ürünler termal çantada gelir.</p>
<h2>Sık yapılan 3 hata</h2>
<ul>
<li>Konum atıp bina numarasını yazmamak. Konumla beraber mutlaka kapı numarasını ekleyin.</li>
<li>Telefonu sessize almak. Kurye ulaşamazsa bir sonraki teslimata geçmek zorunda kalır.</li>
<li>Site girişinde isim bırakmamak. Güvenlikli sitelerde kuryeyi önceden bildirin.</li>
</ul>
<p>Hazırsanız: <a href="%(wa)s">WhatsApp'tan sipariş verin</a> ya da <a href="tel:%(tel)s">%(phone)s</a> numarasını arayın.</p>
"""},
 {
  "slug":"gel-al-fiyatina-eve-teslim",
  "title":"Gel-Al Fiyatına Eve Teslim Ne Demek? Fiyat Farkı Neden Yok",
  "desc":"Teslimat uygulamalarında ürünler raf fiyatından yüzde 15-30 pahalı olabilir. Marin Kartal'da eve teslimatta aynı raf fiyatını uygular. Nasıl ve neden.",
  "date":"2026-09-28",
  "body":"""
<p>Hızlı teslimat uygulamalarından sipariş verenler bilir: aynı ürün rafta başka, uygulamada başka fiyattır. Üstüne servis ücreti, üstüne minimum sepet. Biz Kartal'da işi tersine kurduk.</p>
<h2>Kural basit: raf fiyatı = teslimat fiyatı</h2>
<p>Dükkâna gelip aldığınız buzun, toniğin, çerezin fiyatı neyse kapınıza gelen de aynı fiyattır. Etiketi kurye getirir, isterseniz karşılaştırırsınız.</p>
<h2>Bunu nasıl karşılıyoruz?</h2>
<ul>
<li><strong>Kendi kuryemiz var.</strong> Platform komisyonu (çoğu uygulamada yüzde 20 ve üzeri) ödemiyoruz, o farkı size yansıtmıyoruz.</li>
<li><strong>Rota kısa.</strong> Yalnızca Kartal ve sınır komşularına gidiyoruz; motor bir turda birkaç siparişi birleştiriyor.</li>
<li><strong>Dükkân zaten açık.</strong> Gece 02:00'ye kadar açık olan bir esnaf için teslimat ek bir maliyet merkezi değil, aynı tezgâhın uzantısı.</li>
</ul>
<h2>Hiç ek ücret yok mu?</h2>
<p>Bazı uzak bölgelerde ya da çok küçük siparişlerde cüzi bir teslimat ücreti olabilir. Ama şunu garanti ediyoruz: ücret varsa sipariş sırasında, kapıya gelmeden önce söylenir. Sürpriz yok.</p>
<h2>Neden Google'da 5.0?</h2>
<p>Müşterilerimizin yorumlarında tekrar eden iki şey: "aradığım her şey var, yoksa getiriyorlar" ve "fiyat farkı yok". <a href="/hakkimizda.html">Hikâyemizi</a> okuyun, sonra bir sipariş verip kendiniz görün.</p>
"""},
 {
  "slug":"kartal-mahalleleri-teslimat-sureleri",
  "title":"Kartal Mahalleleri: Hangi Mahalleye Kaç Dakikada Geliyoruz?",
  "desc":"Karlıktepe'den yola çıkan kuryemiz Kartal'ın 20 mahallesine kaç dakikada ulaşıyor? Mahalle mahalle tahmini teslimat süreleri ve rotalar.",
  "date":"2026-09-20",
  "body":"""
<p>Kartal, sahilden Aydos Ormanı'na kadar uzanan geniş bir ilçe. Karlıktepe'deki tekelimiz tam ortada olduğu için buz ve mikser siparişlerinde çoğu mahalleye 30 dakikanın altında ulaşıyoruz. Aşağıdaki süreler akşam trafiği dahil gerçekçi ortalamalardır.</p>
%(tablo)s
<h2>Süreyi ne etkiler?</h2>
<ul>
<li><strong>Saat:</strong> 18:00–20:00 E-5 geçişleri yavaşlar; gece ise en hızlı dilim.</li>
<li><strong>Adres netliği:</strong> Kapı numarası ve zil ismi yazan siparişler ortalama 5 dakika daha erken teslim edilir.</li>
<li><strong>Sipariş birleştirme:</strong> Aynı mahalleden iki sipariş aynı turda gider; bu bazen 2-3 dakika gecikme, çoğu zaman da hız demek.</li>
</ul>
<p>Mahallenizin kendi sayfasında daha fazla ayrıntı var: <a href="/teslimat-bolgeleri.html">tüm teslimat bölgeleri</a>.</p>
"""},
]

# ─────────────────────────────── CSS ───────────────────────────────
CSS = r"""
/* tekelsiparis.com — Marin design system */
:root{
  --navy:#0B1B45;--navy-2:#122866;--blue:#1E49C8;--blue-soft:#DCE6FF;
  --sea:#0FB5A8;--sea-deep:#06675F;
  --amber:#FFB628;--amber-deep:#E39A00;--red:#E23D28;
  --paper:#F7F3EA;--paper-2:#EFE9DC;--line:#DED6C5;
  --ink:#0E1430;--ink-2:#3C4260;--ink-3:#5A6080;--white:#fff;
  --r:18px;--r-sm:10px;--shadow:0 12px 40px -12px rgba(11,27,69,.35);
  --font-d:"Bricolage Grotesque",ui-sans-serif,system-ui,sans-serif;
  --font-b:"Plus Jakarta Sans",ui-sans-serif,system-ui,sans-serif;
  --max:1180px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;font-family:var(--font-b);color:var(--ink);background:var(--paper);line-height:1.6;font-size:17px;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.35;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .05 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
img,svg{max-width:100%;height:auto;display:block}
a{color:var(--blue)}
h1,h2,h3,h4{font-family:var(--font-d);line-height:1.08;letter-spacing:-.02em;margin:0 0 .5em;font-weight:800}
h1{font-size:clamp(2.3rem,5.5vw,4.4rem)}
h2{font-size:clamp(1.7rem,3.4vw,2.6rem)}
h3{font-size:1.25rem;font-weight:700}
p{margin:0 0 1em}
.wrap{max-width:var(--max);margin:0 auto;padding:0 clamp(16px,4vw,32px);position:relative;z-index:1}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.skip{position:absolute;left:-999px;top:8px;background:var(--amber);color:var(--ink);padding:8px 12px;border-radius:8px;z-index:100}
.skip:focus{left:8px}

/* buttons */
.btn{display:inline-flex;align-items:center;gap:.55em;font-family:var(--font-d);font-weight:700;font-size:1.02rem;padding:.9em 1.35em;border-radius:999px;text-decoration:none;border:2px solid transparent;transition:transform .15s,box-shadow .15s,background .15s;cursor:pointer;line-height:1;min-height:48px;white-space:nowrap}
.btn:active{transform:translateY(1px)}
.btn-wa{background:#25D366;color:#062b16;border-color:#25D366}
.btn-wa:hover{background:#1fbf5a;box-shadow:0 10px 24px -8px rgba(37,211,102,.7)}
.btn-tel{background:var(--amber);color:var(--ink);border-color:var(--amber)}
.btn-tel:hover{background:#ffc247;box-shadow:0 10px 24px -8px rgba(255,182,40,.8)}
.btn-ghost{background:transparent;color:var(--white);border-color:rgba(255,255,255,.45)}
.btn-ghost:hover{border-color:#fff;background:rgba(255,255,255,.08)}
.btn-ink{background:var(--navy);color:#fff;border-color:var(--navy)}
.btn-ink:hover{background:var(--navy-2)}
.btn svg{width:1.15em;height:1.15em;flex:none}

/* header */
.top{position:sticky;top:0;z-index:50;background:rgba(247,243,234,.85);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;height:68px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);font-family:var(--font-d);font-weight:800;font-size:1.15rem;letter-spacing:-.02em;white-space:nowrap;flex:none}
.logo .mark{width:40px;height:40px;border-radius:11px;background:var(--navy);display:grid;place-items:center;color:var(--amber);font-size:1.1rem;box-shadow:inset 0 -3px 0 rgba(0,0,0,.25)}
.logo small{display:block;font-family:var(--font-b);font-weight:600;font-size:.68rem;color:var(--ink-3);letter-spacing:.08em;text-transform:uppercase;line-height:1}
nav.main ul{display:flex;gap:4px;list-style:none;margin:0;padding:0}
nav.main a{text-decoration:none;color:var(--ink-2);font-weight:600;font-size:.9rem;padding:.55em .7em;border-radius:999px;white-space:nowrap}
nav.main a:hover,nav.main a[aria-current]{background:var(--paper-2);color:var(--ink)}
.top .cta{display:flex;gap:8px;align-items:center}
.status{display:inline-flex;align-items:center;gap:7px;font-size:.82rem;font-weight:700;padding:.4em .8em;border-radius:999px;background:var(--paper-2);color:var(--ink-2);white-space:nowrap}
.top .cta{flex:none}
@media(max-width:1260px){.top .status{display:none}}
.status i{width:9px;height:9px;border-radius:50%;background:#9aa;box-shadow:0 0 0 3px rgba(0,0,0,.05)}
.status.open i{background:#16a34a;box-shadow:0 0 0 3px rgba(22,163,74,.2);animation:pulse 1.6s infinite}
.status.closed i{background:var(--red)}
@keyframes pulse{0%,100%{box-shadow:0 0 0 3px rgba(22,163,74,.2)}50%{box-shadow:0 0 0 6px rgba(22,163,74,.05)}}
.burger{display:none;background:none;border:0;padding:8px;cursor:pointer}
.burger span{display:block;width:24px;height:2.5px;background:var(--ink);margin:5px 0;border-radius:2px}
@media(max-width:1080px){
  nav.main{display:none;position:absolute;left:0;right:0;top:68px;background:var(--paper);border-bottom:1px solid var(--line);padding:12px 16px 20px}
  nav.main.open{display:block}
  nav.main ul{flex-direction:column}
  nav.main a{display:block;font-size:1.05rem;padding:.75em .9em}
  .burger{display:block}
  .top .cta .btn-tel{display:none}
}

/* hero */
.hero{position:relative;background:var(--navy);color:#fff;overflow:hidden;isolation:isolate}
.hero::before{content:"";position:absolute;inset:0;z-index:-1;
  background:
   radial-gradient(900px 500px at 85% -10%,rgba(30,73,200,.9),transparent 60%),
   radial-gradient(600px 400px at -10% 110%,rgba(15,181,168,.45),transparent 60%),
   linear-gradient(180deg,var(--navy) 0%,#0B1B45 100%)}
.hero::after{content:"";position:absolute;inset:0;z-index:-1;opacity:.12;
  background-image:linear-gradient(rgba(255,255,255,.5) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.5) 1px,transparent 1px);
  background-size:56px 56px;mask-image:radial-gradient(ellipse at 70% 30%,#000 20%,transparent 70%)}
.hero .wrap{display:grid;grid-template-columns:1.25fr .9fr;gap:clamp(24px,5vw,64px);align-items:center;padding-top:clamp(56px,8vw,110px);padding-bottom:clamp(64px,9vw,120px)}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-d);font-weight:700;font-size:.85rem;letter-spacing:.12em;text-transform:uppercase;color:var(--amber);margin-bottom:18px}
.eyebrow::before{content:"";width:28px;height:2px;background:var(--amber)}
.hero h1{margin-bottom:.4em}
.hero h1 em{font-style:normal;color:var(--amber);position:relative;white-space:nowrap}
.hero h1 em::after{content:"";position:absolute;left:0;right:0;bottom:.04em;height:.22em;background:var(--amber);opacity:.25;border-radius:4px;z-index:-1}
.hero .lead{font-size:clamp(1.05rem,1.6vw,1.3rem);color:rgba(255,255,255,.82);max-width:34em;margin-bottom:1.6em}
.hero .actions{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:22px}
.hero .proof{display:flex;flex-wrap:wrap;gap:18px 28px;font-size:.92rem;color:rgba(255,255,255,.75)}
.hero .proof b{color:#fff;font-family:var(--font-d);font-size:1.15rem;display:block;letter-spacing:-.01em}
.hero .proof .stars{color:var(--amber);letter-spacing:.05em}
.card{background:#fff;color:var(--ink);border-radius:var(--r);padding:clamp(20px,3vw,32px);box-shadow:var(--shadow)}
.ordercard{position:relative;transform:rotate(-1.2deg)}
.ordercard::before{content:"";position:absolute;inset:-6px;border:2px dashed rgba(255,182,40,.6);border-radius:calc(var(--r) + 6px);transform:rotate(1.8deg);pointer-events:none}
.ordercard h2{font-size:1.35rem;margin-bottom:.3em}
.ordercard .hours{display:flex;justify-content:space-between;align-items:center;padding:12px 14px;background:var(--paper);border-radius:var(--r-sm);margin:14px 0;font-weight:600}
.ordercard .hours b{font-family:var(--font-d);font-size:1.25rem;color:var(--navy)}
.ordercard .stack{display:grid;gap:10px}
.ordercard .stack .btn{justify-content:center;width:100%}
.ordercard .note{font-size:.85rem;color:var(--ink-3);margin:12px 0 0;text-align:center}
.ordercard .addr{font-size:.9rem;color:var(--ink-2);margin-top:14px;padding-top:14px;border-top:1px solid var(--line)}
@media(max-width:900px){.hero .wrap{grid-template-columns:1fr}.ordercard{transform:none}.ordercard::before{display:none}}

/* marquee */
.marquee{background:var(--amber);color:var(--ink);overflow:hidden;border-top:3px solid var(--navy);border-bottom:3px solid var(--navy);font-family:var(--font-d);font-weight:800;text-transform:uppercase;letter-spacing:.06em;font-size:.95rem}
.marquee .track{display:flex;gap:0;width:max-content;animation:scroll 48s linear infinite}
.marquee span{padding:12px 22px;white-space:nowrap;display:inline-flex;align-items:center;gap:22px}
.marquee span::after{content:"✦";opacity:.6}
@keyframes scroll{to{transform:translateX(-50%)}}
@media(prefers-reduced-motion:reduce){.marquee .track{animation:none}.status.open i{animation:none}}

/* sections */
section{padding:clamp(56px,8vw,104px) 0}
.sec-head{max-width:720px;margin-bottom:clamp(28px,4vw,48px)}
.sec-head .eyebrow{color:var(--sea-deep)}.sec-head .eyebrow::before{background:var(--sea)}
.sec-head p{color:var(--ink-2);font-size:1.1rem}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;counter-reset:s}
.step{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:28px 26px 26px;position:relative;overflow:hidden}
.step::before{counter-increment:s;content:"0" counter(s);position:absolute;right:16px;top:8px;font-family:var(--font-d);font-size:4.5rem;font-weight:800;color:var(--paper-2);line-height:1}
.step h3{position:relative}
.step p{position:relative;color:var(--ink-2);margin:0}
@media(max-width:800px){.steps{grid-template-columns:1fr}}

.cats{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.cat{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:22px;transition:transform .2s,box-shadow .2s;text-decoration:none;color:inherit;display:block}
.cat:hover{transform:translateY(-4px);box-shadow:var(--shadow)}
.cat .ico{font-size:1.9rem;line-height:1;margin-bottom:12px}
.cat p{color:var(--ink-2);font-size:.95rem;margin:0 0 10px}
.cat ul{margin:0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:6px}
.cat li{font-size:.78rem;background:var(--paper);border:1px solid var(--line);border-radius:999px;padding:3px 9px;color:var(--ink-2)}
@media(max-width:900px){.cats{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.cats{grid-template-columns:1fr}}

.why{background:var(--navy);color:#fff;position:relative;overflow:hidden}
.why::before{content:"";position:absolute;width:60vw;height:60vw;max-width:700px;max-height:700px;border-radius:50%;right:-20vw;top:-20vw;background:radial-gradient(circle,rgba(15,181,168,.35),transparent 65%)}
.why .sec-head .eyebrow{color:var(--amber)}.why .sec-head .eyebrow::before{background:var(--amber)}
.why .sec-head p{color:rgba(255,255,255,.78)}
.why-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.why-item{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:var(--r);padding:26px}
.why-item b{display:block;font-family:var(--font-d);font-size:2.4rem;color:var(--amber);letter-spacing:-.03em;line-height:1;margin-bottom:10px}
.why-item h3{color:#fff}
.why-item p{color:rgba(255,255,255,.75);margin:0}
@media(max-width:800px){.why-grid{grid-template-columns:1fr}}

.areas{display:flex;flex-wrap:wrap;gap:8px}
.areas a{text-decoration:none;font-weight:600;font-size:.92rem;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 14px;transition:all .15s}
.areas a:hover{background:var(--navy);color:#fff;border-color:var(--navy)}
.areas a small{color:var(--ink-3);font-weight:500;margin-left:6px}
.areas a:hover small{color:rgba(255,255,255,.7)}

.reviews{display:grid;grid-template-columns:1.1fr .9fr;gap:24px;align-items:start}
.review{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:28px}
.review blockquote{margin:0 0 14px;font-family:var(--font-d);font-size:1.25rem;font-weight:600;line-height:1.35;letter-spacing:-.01em}
.review .who{display:flex;align-items:center;gap:10px;color:var(--ink-3);font-size:.9rem}
.review .who .av{width:36px;height:36px;border-radius:50%;background:var(--blue-soft);color:var(--navy);display:grid;place-items:center;font-weight:800;font-family:var(--font-d)}
.gbox{background:var(--amber);border-radius:var(--r);padding:28px;color:var(--ink)}
.gbox b{font-family:var(--font-d);font-size:3.6rem;display:block;line-height:1;letter-spacing:-.03em}
.gbox .stars{font-size:1.4rem;letter-spacing:.08em}
@media(max-width:800px){.reviews{grid-template-columns:1fr}}

.faq details{background:#fff;border:1px solid var(--line);border-radius:var(--r-sm);margin-bottom:10px;overflow:hidden}
.faq summary{cursor:pointer;padding:16px 20px;font-family:var(--font-d);font-weight:700;font-size:1.05rem;list-style:none;display:flex;justify-content:space-between;gap:12px;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font-size:1.5rem;color:var(--sea-deep);flex:none;transition:transform .2s}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq .a{padding:0 20px 18px;color:var(--ink-2)}

.cta-band{background:linear-gradient(120deg,var(--sea-deep),var(--sea));color:#fff;border-radius:var(--r);padding:clamp(28px,4vw,48px);display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap}
.cta-band h2{color:#fff;margin:0 0 .2em}
.cta-band p{margin:0;color:rgba(255,255,255,.85)}
.cta-band .actions{display:flex;gap:10px;flex-wrap:wrap}

/* page */
.page-head{background:var(--navy);color:#fff;padding:clamp(40px,6vw,72px) 0 clamp(36px,5vw,56px);position:relative;overflow:hidden}
.page-head::before{content:"";position:absolute;inset:0;background:radial-gradient(700px 400px at 90% 0%,rgba(30,73,200,.8),transparent 60%)}
.page-head .wrap{position:relative}
.page-head h1{margin-bottom:.3em}
.page-head p{color:rgba(255,255,255,.8);max-width:40em;font-size:1.1rem;margin:0}
.crumbs{font-size:.85rem;color:rgba(255,255,255,.6);margin-bottom:14px}
.crumbs a{color:rgba(255,255,255,.8);text-decoration:none}
.crumbs span{margin:0 6px;opacity:.5}
.prose{max-width:760px}
.prose h2{margin-top:1.6em;font-size:1.6rem}
.prose h3{margin-top:1.3em}
.prose li{margin-bottom:.4em}
.prose table{border-collapse:collapse;width:100%;font-size:.95rem;margin:1em 0}
.prose th,.prose td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line)}
.prose th{font-family:var(--font-d);background:var(--paper-2)}
.two{display:grid;grid-template-columns:1.2fr .8fr;gap:40px;align-items:start}
@media(max-width:860px){.two{grid-template-columns:1fr}}
.side{position:sticky;top:88px}
.side .card{padding:22px}
.side .card h3{margin-top:0}
.kv{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;font-size:.95rem}
.kv dt{color:var(--ink-3);font-weight:600}.kv dd{margin:0}
.map{border-radius:var(--r);overflow:hidden;border:1px solid var(--line);aspect-ratio:16/10;background:var(--paper-2)}
.map iframe{width:100%;height:100%;border:0}

/* order builder */
.builder{display:grid;grid-template-columns:1.3fr .8fr;gap:28px;align-items:start}
@media(max-width:900px){.builder{grid-template-columns:1fr}}
.pgroup{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:18px 20px;margin-bottom:14px}
.pgroup h3{display:flex;align-items:center;gap:8px;margin-bottom:10px}
.pgroup .items{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:8px}
.pitem{display:flex;align-items:center;justify-content:space-between;gap:8px;background:var(--paper);border:1px solid var(--line);border-radius:var(--r-sm);padding:8px 10px;font-size:.92rem}
.pitem .q{display:flex;align-items:center;gap:4px}
.pitem button{width:30px;height:30px;border-radius:8px;border:1px solid var(--line);background:#fff;font-weight:800;cursor:pointer;font-size:1rem;line-height:1}
.pitem button:hover{background:var(--navy);color:#fff;border-color:var(--navy)}
.pitem output{min-width:22px;text-align:center;font-weight:700;font-family:var(--font-d)}
.pitem.has{border-color:var(--sea);background:#E8FBF9}
.summary textarea,.summary input{width:100%;font:inherit;padding:12px;border:1px solid var(--line);border-radius:var(--r-sm);background:var(--paper);resize:vertical}
.summary label{display:block;font-weight:700;font-size:.9rem;margin:12px 0 6px;font-family:var(--font-d)}
.summary ul{list-style:none;padding:0;margin:0 0 8px;font-size:.95rem}
.summary li{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px dashed var(--line)}
.summary .empty{color:var(--ink-3);font-style:italic;font-size:.92rem}
.summary .btn{width:100%;justify-content:center;margin-top:12px}

/* blog */
.posts{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
.post{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:24px;text-decoration:none;color:inherit;display:block;transition:transform .2s,box-shadow .2s}
.post:hover{transform:translateY(-3px);box-shadow:var(--shadow)}
.post time{font-size:.82rem;color:var(--ink-3);font-weight:600}
.post h3{margin:6px 0 8px;font-size:1.25rem}
.post p{color:var(--ink-2);margin:0;font-size:.95rem}
@media(max-width:700px){.posts{grid-template-columns:1fr}}

/* footer */
footer{background:var(--ink);color:rgba(255,255,255,.75);padding:56px 0 100px;font-size:.93rem}
footer .grid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:32px}
footer .h4{color:#fff;font-family:var(--font-d);font-weight:800;margin:0 0 14px;font-size:.9rem;text-transform:uppercase;letter-spacing:.1em;margin-bottom:14px}
footer ul{list-style:none;margin:0;padding:0}
footer li{margin-bottom:8px}
footer a{color:rgba(255,255,255,.85);text-decoration:none}
footer a:hover{color:var(--amber)}
footer address{font-style:normal;line-height:1.7}
footer .legal{margin-top:36px;padding-top:20px;border-top:1px solid rgba(255,255,255,.12);font-size:.8rem;color:rgba(255,255,255,.5);display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}
@media(max-width:860px){footer .grid{grid-template-columns:1fr 1fr}}
@media(max-width:520px){footer .grid{grid-template-columns:1fr}}

/* mobile sticky bar */
.mbar{position:fixed;left:0;right:0;bottom:0;z-index:60;display:none;gap:8px;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:rgba(14,20,48,.92);backdrop-filter:blur(10px)}
.mbar .btn{flex:1;justify-content:center;font-size:.98rem}
@media(max-width:760px){.mbar{display:flex}}
@media(min-width:761px){footer{padding-bottom:56px}}

/* reveal (içerik asla gizlenmez; görünür olunca yumuşak giriş) */
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
html.js .rv.in{animation:rise .6s ease both}
@media(prefers-reduced-motion:reduce){html.js .rv.in{animation:none}}
"""

# ─────────────────────────────── JS ───────────────────────────────
JS = r"""
(function(){
  // Açık/Kapalı durumu (Europe/Istanbul). 08:00–02:00
  function istanbulNow(){try{var s=new Date().toLocaleString('en-US',{timeZone:'Europe/Istanbul'});return new Date(s);}catch(e){return new Date();}}
  function isOpen(){var d=istanbulNow();var m=d.getHours()*60+d.getMinutes();return (m>=8*60)||(m<2*60);}
  function paint(){var o=isOpen();document.querySelectorAll('[data-status]').forEach(function(el){
    el.classList.toggle('open',o);el.classList.toggle('closed',!o);
    var t=el.querySelector('[data-status-text]');if(t)t.textContent=o?'Şu an açık · 02:00\'ye kadar':'Şu an kapalı · 08:00\'de açılıyor';
  });}
  paint();setInterval(paint,60000);

  // Mobil menü
  var b=document.querySelector('.burger'),n=document.querySelector('nav.main');
  if(b&&n){b.addEventListener('click',function(){var open=n.classList.toggle('open');b.setAttribute('aria-expanded',open);});}

  // Reveal
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.rv').forEach(function(el){var r=el.getBoundingClientRect();if(r.top<innerHeight)el.classList.add('in');else io.observe(el);});}
  else{document.querySelectorAll('.rv').forEach(function(el){el.classList.add('in');});}

  // Lazy map
  var mp=document.querySelector('.map[data-src]');
  if(mp){var load=function(){if(mp.dataset.done)return;mp.dataset.done=1;var f=document.createElement('iframe');f.src=mp.dataset.src;f.loading='lazy';f.title='Marin Tekel 2 harita';f.referrerPolicy='no-referrer-when-downgrade';mp.appendChild(f);};
    if('IntersectionObserver' in window){var mo=new IntersectionObserver(function(es){if(es[0].isIntersecting){load();mo.disconnect();}},{rootMargin:'200px'});mo.observe(mp);}else load();}

  // Sipariş oluşturucu
  var bl=document.querySelector('.builder');
  if(bl){
    var cart={},list=bl.querySelector('#cartlist'),empty=bl.querySelector('#cartempty'),addr=bl.querySelector('#addr'),note=bl.querySelector('#note'),btn=bl.querySelector('#sendwa');
    var WA='https://wa.me/__WA__?text=';
    function render(){var keys=Object.keys(cart).filter(function(k){return cart[k]>0});list.innerHTML='';empty.style.display=keys.length?'none':'block';
      keys.forEach(function(k){var li=document.createElement('li');li.innerHTML='<span>'+k+'</span><b>×'+cart[k]+'</b>';list.appendChild(li);});
      var lines=keys.map(function(k){return '• '+k+' × '+cart[k]});
      var msg='Merhaba Marin, sipariş vermek istiyorum.\n\n'+(lines.length?lines.join('\n'):'(ürünler)')+'\n\nAdres: '+(addr.value||'')+(note.value?'\nNot: '+note.value:'');
      btn.href=WA+encodeURIComponent(msg);
      try{localStorage.setItem('marin_addr',addr.value);}catch(e){}
    }
    bl.querySelectorAll('.pitem').forEach(function(it){var name=it.dataset.name,out=it.querySelector('output');
      it.querySelector('.plus').addEventListener('click',function(){cart[name]=(cart[name]||0)+1;out.value=cart[name];it.classList.add('has');render();});
      it.querySelector('.minus').addEventListener('click',function(){cart[name]=Math.max(0,(cart[name]||0)-1);out.value=cart[name];it.classList.toggle('has',cart[name]>0);render();});
    });
    addr.addEventListener('input',render);note.addEventListener('input',render);
    try{var a=localStorage.getItem('marin_addr');if(a)addr.value=a;}catch(e){}
    render();
  }
})();
""".replace("__WA__", C["whatsapp"])

# ─────────────────────────────── SVG İKONLAR ───────────────────────────────
I_WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5.1-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 12 12 0 0 0 4.6 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .1-1.2c0-.2-.2-.2-.4-.3z"/></svg>'
I_TEL = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11.4 11.4 0 0 0 .57 3.6 1 1 0 0 1-.25 1z"/></svg>'

# ─────────────────────────────── ŞABLON ───────────────────────────────
NAV = [("/","Ana Sayfa"),("/kartal-tekel.html","Kartal Tekel"),("/siparis.html","Sipariş Ver"),("/urunler.html","Ürünler"),("/teslimat-bolgeleri.html","Teslimat Bölgeleri"),("/sss.html","SSS"),("/blog/","Blog"),("/hakkimizda.html","Hakkımızda"),("/iletisim.html","İletişim")]

def local_business(extra=None):
    d = {
      "@context":"https://schema.org",
      "@type":["LiquorStore","ConvenienceStore","LocalBusiness"],
      "@id": C["domain"]+"/#business",
      "name": C["brand"],
      "alternateName":["Marin Tekel","Marin Tekel Kartal","Kartal Marin Tekel 2","Karlıktepe Tekel","Kartal Tekel","Kartal Tekel Bayii","Kartal Gece Açık Tekel"],
      "keywords":"kartal tekel, kartal tekel bayii, karlıktepe tekel, kartal gece açık tekel, kartal en yakın tekel, kartal sahil tekel, kartal merkez tekel, kartal tekel telefon, tekel siparişi kartal, buz siparişi kartal",
      "description": f"{C['brand']}, Kartal Karlıktepe'de her gün {C['opens']}–{C['closes']} açık tekel bayii. Buz, soğuk içecek, soda-tonik, meze ve atıştırmalığı Kartal'ın tüm mahallelerine gel-al fiyatına, ortalama {C['eta']} içinde teslim eder. Yaş sınırlı ürünler yalnızca dükkânda, kimlik kontrolüyle satılır.",
      "url": C["domain"]+"/",
      "telephone": C["phone_e164"],
      "image": C["domain"]+"/assets/og.png",
      "logo": C["domain"]+"/assets/logo.svg",
      "priceRange":"₺",
      "currenciesAccepted":"TRY",
      "paymentAccepted":"Nakit, Kredi Kartı, Banka Kartı",
      "foundingDate": C["founded"],
      "address":{"@type":"PostalAddress","streetAddress":C["street"],"addressLocality":C["ilce"],"addressRegion":C["city"],"postalCode":C["postal"],"addressCountry":"TR"},
      "geo":{"@type":"GeoCoordinates","latitude":C["lat"],"longitude":C["lng"]},
      "hasMap": C["maps_url"],
      "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":C["opens"],"closes":C["closes"]}],
      "aggregateRating":{"@type":"AggregateRating","ratingValue":C["rating"],"reviewCount":C["review_count"],"bestRating":"5"},
      "areaServed":[{"@type":"Place","name":f"{b[1]}, {b[5]}, İstanbul"} for b in BOLGELER],
      "hasOfferCatalog":{"@type":"OfferCatalog","name":"Ürün kategorileri","itemListElement":[{"@type":"OfferCatalog","name":k[0]} for k in KATEGORILER]},
      "potentialAction":[{"@type":"OrderAction","target":{"@type":"EntryPoint","urlTemplate":WA_DEFAULT,"actionPlatform":["http://schema.org/MobileWebPlatform","http://schema.org/DesktopWebPlatform"]},"deliveryMethod":"http://purl.org/goodrelations/v1#DeliveryModeOwnFleet"},
                         {"@type":"CommunicateAction","target":{"@type":"EntryPoint","urlTemplate":"tel:"+C["phone_e164"]}}],
      "sameAs":[s for s in [C["maps_url"], C["instagram"]] if s],
      "slogan":"Kartal'ın gece 02:00'ye kadar açık tekeli.",
      "knowsLanguage":"tr",
    }
    if extra: d.update(extra)
    return d

def jsonld(*objs):
    return "".join('<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False,separators=(",",":"))+'</script>' for o in objs)

def breadcrumb(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":C["domain"]+u} for i,(u,n) in enumerate(items)]}

def faq_schema(qs):
    strip=lambda s: re.sub(r"<[^>]+>","",s).replace("&ldquo;","“").replace("&rdquo;","”").replace("&ndash;","–")
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":strip(a)}} for q,a in qs]}

def head(title, desc, path, schemas, og_type="website", noindex=False):
    url = C["domain"]+path
    return f"""<!DOCTYPE html>
<html lang="tr" prefix="og: https://ogp.me/ns#">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
{'<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">'}
<meta name="theme-color" content="#0B1B45">
<meta name="geo.region" content="TR-34"><meta name="geo.placename" content="Kartal, İstanbul"><meta name="geo.position" content="{C['lat']};{C['lng']}"><meta name="ICBM" content="{C['lat']}, {C['lng']}">
<meta property="og:locale" content="tr_TR"><meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{esc(C['brand'])} · tekelsiparis.com">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{C['domain']}/assets/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{esc(C['brand'])} – Kartal tekel, buz ve mikser kapında">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{C['domain']}/assets/og.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/icon-180.png"><link rel="manifest" href="/manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600..800&family=Plus+Jakarta+Sans:wght@500;600;700&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600..800&family=Plus+Jakarta+Sans:wght@500;600;700&display=swap">
<link rel="stylesheet" href="/assets/styles.css">
<script>document.documentElement.classList.add("js")</script>
{jsonld(*schemas)}
</head>
<body>
<a class="skip" href="#main">İçeriğe geç</a>
<header class="top">
 <div class="wrap">
  <a class="logo" href="/" title="Ana sayfa"><span class="mark">M</span><span>{esc(C['brand'])}<small>Kartal · Tekel · 02:00'ye kadar</small></span></a>
  <nav class="main" aria-label="Ana menü"><ul>{''.join(f'<li><a href="{u}"{" aria-current=page" if (u==path or (u!="/" and path.startswith(u.replace(".html","")) and u.endswith("/"))) else ""}>{n}</a></li>' for u,n in NAV)}</ul></nav>
  <div class="cta">
   <span class="status" data-status><i></i><span data-status-text>{C['opens']}–{C['closes']}</span></span>
   <a class="btn btn-tel" href="tel:{C['phone_e164']}">{I_TEL}{C['phone_display']}</a>
   <button class="burger" aria-label="Menüyü aç" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
  </div>
 </div>
</header>
<main id="main">
"""

def foot():
    areas = "".join(f'<li><a href="/bolge/{b[0]}.html">{esc(b[1])}</a></li>' for b in BOLGELER[:10])
    return f"""
</main>
<footer>
 <div class="wrap">
  <div class="grid">
   <div>
    <p class="h4">{esc(C['brand'])}</p>
    <address itemscope itemtype="https://schema.org/LocalBusiness">
     <span itemprop="name">{esc(C['brand'])}</span><br>
     <span itemprop="address">{esc(C['address_full'])}</span><br>
     <a itemprop="telephone" href="tel:{C['phone_e164']}">{C['phone_display']}</a> · <a href="{WA_DEFAULT}" rel="noopener">WhatsApp</a><br>
     Her gün <time itemprop="openingHours" datetime="Mo-Su {C['opens']}-{C['closes']}">{C['opens']}–{C['closes']}</time>
    </address>
    <p style="margin-top:12px"><a href="{C['maps_url']}" rel="noopener" target="_blank">Google Haritalar'da aç ↗</a></p>
   </div>
   <div><p class="h4">Site</p><ul>{''.join(f'<li><a href="{u}">{n}</a></li>' for u,n in NAV)}</ul></div>
   <div><p class="h4">Teslimat Bölgeleri</p><ul>{areas}<li><a href="/teslimat-bolgeleri.html">Tüm bölgeler →</a></li></ul></div>
   <div><p class="h4">Blog</p><ul>{''.join(f'<li><a href="/blog/{p["slug"]}.html">{esc(p["title"][:48])}…</a></li>' for p in BLOG)}</ul></div>
  </div>
  <div class="legal"><span>© {datetime.date.today().year} {esc(C['brand'])} · Kartal, İstanbul · tekelsiparis.com</span><span>18 yaş altına alkollü içki ve tütün satışı yapılmaz. Alkollü içki ve tütün ürünleri uzaktan satılmaz ve eve gönderilmez (4250 ve 4207 sayılı kanunlar). Teslimat süreleri tahminidir.</span></div>
 </div>
</footer>
<div class="mbar">
 <a class="btn btn-tel" href="tel:{C['phone_e164']}">{I_TEL}Ara</a>
 <a class="btn btn-wa" href="{WA_DEFAULT}" rel="noopener">{I_WA}WhatsApp Sipariş</a>
</div>
<script src="/assets/main.js" defer></script>
</body></html>"""

def page_head(h1, lead, crumbs):
    cr = '<div class="crumbs">' + ''.join((f'<a href="{u}">{n}</a><span>/</span>' if i<len(crumbs)-1 else f'<span style="margin:0;opacity:1">{n}</span>') for i,(u,n) in enumerate(crumbs)) + '</div>'
    return f'<div class="page-head"><div class="wrap">{cr}<h1>{h1}</h1><p>{lead}</p></div></div>'

def cta_band(title="Şimdi sipariş ver, {eta} içinde kapında.", sub="Telefon ya da WhatsApp. Raf fiyatı, fiyat farkı yok."):
    return f"""<section><div class="wrap"><div class="cta-band rv"><div><h2>{title.format(eta=C['eta'])}</h2><p>{sub}</p></div>
<div class="actions"><a class="btn btn-wa" href="{WA_DEFAULT}" rel="noopener">{I_WA}WhatsApp'tan Sipariş</a><a class="btn btn-ghost" href="tel:{C['phone_e164']}">{I_TEL}{C['phone_display']}</a></div></div></div></section>"""

def faq_block(qs, title="Sık sorulanlar", lead=None):
    items = "".join(f'<details><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for q,a in qs)
    return f'<section class="faq"><div class="wrap"><div class="sec-head"><span class="eyebrow">SSS</span><h2>{title}</h2>{f"<p>{lead}</p>" if lead else ""}</div>{items}</div></section>'

def write(path, content):
    full = os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full,"w",encoding="utf-8") as f: f.write(content)

# ─────────────────────────────── ANA SAYFA ───────────────────────────────
def build_index():
    title = "Kartal Tekel | 02:00'ye Kadar Açık, Buz & Mikser Kapına | Marin"
    desc = f"Kartal Karlıktepe'de her gün {C['opens']}–{C['closes']} açık tekel. Buz, tonik, soda, meze raf fiyatına {C['eta']} içinde kapında. 18+ ürünler dükkânda, kimlikle. {C['phone_display']}"
    schemas = [
      local_business(),
      {"@context":"https://schema.org","@type":"WebSite","@id":C["domain"]+"/#website","url":C["domain"]+"/","name":"tekelsiparis.com","publisher":{"@id":C["domain"]+"/#business"},"inLanguage":"tr"},
      faq_schema(SSS[:6]),
      {"@context":"https://schema.org","@type":"HowTo","name":"Kartal'da tekel siparişi (buz, mikser, meze) nasıl verilir","totalTime":"PT3M","step":[
        {"@type":"HowToStep","name":"Ara ya da yaz","text":f"{C['phone_display']} numarasını arayın veya WhatsApp'tan yazın."},
        {"@type":"HowToStep","name":"Adres ve ürünler","text":"Mahalle, sokak, bina, daire ve istediğiniz ürünleri tek mesajda gönderin."},
        {"@type":"HowToStep","name":"Kapıda teslim","text":f"Ortalama {C['eta']} içinde kurye kapınızda; nakit veya kartla ödeyin."}]},
    ]
    cats = "".join(f'<a class="cat rv" href="/urunler.html#{slug(k[0])}"><div class="ico">{k[1]}</div><h3>{k[0]}</h3><p>{k[2]}</p><ul>{"".join(f"<li>{i}</li>" for i in k[3][:4])}</ul></a>' for k in KATEGORILER[:6])
    areas = "".join(f'<a href="/bolge/{b[0]}.html">{esc(b[1])}<small>{b[2]}</small></a>' for b in BOLGELER)
    marq = "".join(f"<span>{esc(b[1])}</span>" for b in BOLGELER)
    body = f"""
<section class="hero">
 <div class="wrap">
  <div>
   <span class="eyebrow">Kartal · Karlıktepe · Tekel · Her gün {C['opens']}–{C['closes']}</span>
   <h1>Kartal'ın gece 02:00'ye kadar açık tekeli. Buz ve mikser <em>gel-al fiyatına</em> kapında.</h1>
   <p class="lead">Torba buz, tonik, soda, limon, meze, çerez, cips. Dükkânda ne kadarsa kapında da o kadar; ortalama <strong>{C['eta']}</strong> içinde Kartal'ın her mahallesine. Yaş sınırlı ürünler yalnızca dükkânda, kimlik kontrolüyle.</p>
   <div class="actions">
    <a class="btn btn-wa" href="{WA_DEFAULT}" rel="noopener">{I_WA}WhatsApp'tan Sipariş Ver</a>
    <a class="btn btn-ghost" href="tel:{C['phone_e164']}">{I_TEL}{C['phone_display']}</a>
   </div>
   <div class="proof">
    <div><b><span class="stars">★★★★★</span> {C['rating']}</b>Google yorumları</div>
    <div><b>{C['eta']}</b>ortalama teslimat</div>
    <div><b>%0</b>fiyat farkı</div>
    <div><b>02:00</b>gece açık tekel</div>
    <div><b>Kartal</b>tekel bayii</div>
   </div>
  </div>
  <aside class="card ordercard" aria-labelledby="oc">
   <h2 id="oc">Hemen sipariş ver</h2>
   <p style="color:var(--ink-2);margin:0">Uygulama yok, üyelik yok. Yaz ya da ara, gerisi bizde.</p>
   <div class="hours"><span class="status" data-status><i></i><span data-status-text>{C['opens']}–{C['closes']}</span></span><b>{C['opens']}–{C['closes']}</b></div>
   <div class="stack">
    <a class="btn btn-wa" href="{WA_DEFAULT}" rel="noopener">{I_WA}WhatsApp ile yaz</a>
    <a class="btn btn-tel" href="tel:{C['phone_e164']}">{I_TEL}{C['phone_display']}</a>
    <a class="btn btn-ink" href="/siparis.html">Ürün seçerek sipariş oluştur →</a>
   </div>
   <p class="note">Kapıda nakit veya kart · Soğuk ürünler termal çantada</p>
   <div class="addr">📍 {esc(C['address_full'])}</div>
  </aside>
 </div>
</section>
<div class="marquee" aria-hidden="true"><div class="track">{marq}{marq}</div></div>

<section>
 <div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Nasıl çalışır</span><h2>Üç adımda kapında</h2><p>Mahalle tekeli hızı, dijital kolaylık. Sepet, minimum tutar, uygulama derdi yok.</p></div>
  <div class="steps">
   <div class="step rv"><h3>Ara ya da WhatsApp'tan yaz</h3><p>{C['phone_display']}. Adresini ve istediklerini tek mesajda gönder. İstersen <a href="/siparis.html">ürün seçerek</a> hazır mesaj oluştur.</p></div>
   <div class="step rv"><h3>Hazırlayıp yola çıkarırız</h3><p>Stok ve tahmini süreyi hemen yazarız. Tonik ve sodalar dolaptan, buz derin dondurucudan çıkar; termal çantaya girer.</p></div>
   <div class="step rv"><h3>Kapıda öde, keyfine bak</h3><p>Nakit ya da kart, kurye POS taşır. Fiyat dükkândaki raf fiyatıyla aynıdır.</p></div>
  </div>
 </div>
</section>

<section style="padding-top:0">
 <div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Ne var?</span><h2>Masanın eksiği neyse, kapında</h2><p>Buz, mikser, meze, çerez ve mahalle tekelinde olan her şey. Listede olmayan bir şey mi lazım? Yaz, varsa getiririz; yoksa bulup getiririz.</p></div>
  <div class="cats">{cats}</div>
  <p style="margin-top:20px"><a class="btn btn-ink" href="/urunler.html">Tüm kategoriler →</a></p>
 </div>
</section>

<section class="why">
 <div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Neden Marin?</span><h2>Kartal'ın tekeli: 02:00'ye kadar açık, raf fiyatına kapında</h2><p>Kendi kuryemiz, kendi dükkânımız. Platform komisyonu ödemiyoruz, o farkı size yansıtmıyoruz.</p></div>
  <div class="why-grid">
   <div class="why-item rv"><b>%0</b><h3>Fiyat farkı yok</h3><p>Teslimat fiyatı = raf fiyatı. Varsa teslimat ücreti sipariş anında açıkça söylenir, sürpriz yok.</p></div>
   <div class="why-item rv"><b>18 sa</b><h3>Her gün {C['opens']}–{C['closes']}</h3><p>Kartal'da gece açık tekel arayanların adresi. Dükkân ve teslimat 02:00'ye kadar.</p></div>
   <div class="why-item rv"><b>5.0</b><h3>Google'da tam puan</h3><p>"Aradığım her şey var, yoksa getiriyorlar." Müşterilerimizin sözü, bizim sözümüz değil.</p></div>
  </div>
 </div>
</section>

<section style="padding-bottom:0">
 <div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Kartal tekel</span><h2>Kartal'da tekel arayanların adresi</h2><p>"Kartal tekel", "Karlıktepe tekel", "Kartal gece açık tekel", "en yakın tekel": hepsinin cevabı İnönü Caddesi No:75. Kartal merkeze, metroya ve sahile dakikalar mesafede, her gün 02:00'ye kadar açık tekel bayii. <a href="/kartal-tekel.html">Kartal tekel sayfasına gidin →</a></p></div>
  <div class="card rv" style="border-left:6px solid var(--amber)"><h3 style="margin-bottom:.3em">18+ ürünler hakkında</h3><p style="margin:0;color:var(--ink-2)">Alkollü içki ve tütün ürünleri mevzuat gereği (4250 ve 4207 sayılı kanunlar) telefon, WhatsApp veya internetten sipariş edilemez ve eve gönderilemez. Bu ürünler yalnızca dükkânımızda, 18 yaş üstüne kimlik kontrolüyle satılır. Buz, tonik, soda, meze ve diğer her şeyi kapınıza getiriyoruz.</p></div>
 </div>
</section>

<section>
 <div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Teslimat bölgeleri</span><h2>Kartal'ın her mahallesine</h2><p>Karlıktepe'den yola çıkıyoruz. Süreler akşam trafiği dahil gerçekçi ortalamalardır.</p></div>
  <div class="areas rv">{areas}</div>
  <p style="margin-top:18px;color:var(--ink-2)">Mahallen listede yok mu? <a href="{wa('Merhaba, adresime teslimat yapıyor musunuz? Adres: ')}" rel="noopener">WhatsApp'tan sor</a>, hemen söyleyelim.</p>
 </div>
</section>

<section style="padding-top:0">
 <div class="wrap">
  <div class="reviews">
   <div class="review rv">
    <blockquote>"İş yeri sahipleri çok düzgün esnaflar. Tertemiz, saygılı bir işletme. Aradığım tüm ürünler var. Yoksa da getiriyorlar."</blockquote>
    <div class="who"><span class="av">Ö</span><span>Özkan Y. · Google yorumu · ★★★★★</span></div>
   </div>
   <div class="gbox rv"><b>{C['rating']}</b><span class="stars">★★★★★</span><p style="margin:10px 0 16px;font-weight:600">{C['review_count']} Google yorumu, hepsi 5 yıldız.</p><a class="btn btn-ink" href="{C['maps_url']}" rel="noopener" target="_blank">Google'da gör ↗</a></div>
  </div>
 </div>
</section>

{faq_block(SSS[:6], "Sık sorulanlar", 'Daha fazlası <a href="/sss.html">SSS sayfasında</a>.')}
{cta_band()}
"""
    write("/index.html", head(title, desc, "/", schemas) + body + foot())

def slug(s):
    t = s.lower()
    for a,b in [("ı","i"),("ş","s"),("ğ","g"),("ü","u"),("ö","o"),("ç","c"),("&","ve")]: t=t.replace(a,b)
    return re.sub(r"[^a-z0-9]+","-",t).strip("-")

# ─────────────────────────────── SİPARİŞ ───────────────────────────────
def build_siparis():
    title = "Sipariş Ver | Buz, Mikser, Meze WhatsApp Siparişi | Marin Kartal"
    desc = f"Buz, tonik, soda, meze ve çerezi seç, adresini yaz, tek dokunuşla WhatsApp siparişi oluştur. Kartal'ın her mahallesine {C['eta']} içinde, raf fiyatına."
    groups = "".join(f'<div class="pgroup"><h3><span>{k[1]}</span>{k[0]}</h3><div class="items">' + "".join(f'<div class="pitem" data-name="{esc(i)}"><span>{esc(i)}</span><span class="q"><button class="minus" type="button" aria-label="{esc(i)} azalt">−</button><output>0</output><button class="plus" type="button" aria-label="{esc(i)} ekle">+</button></span></div>' for i in k[3]) + '</div></div>' for k in KATEGORILER)
    schemas = [breadcrumb([("/","Ana Sayfa"),("/siparis.html","Sipariş Ver")]), {"@context":"https://schema.org","@type":"WebPage","name":title,"description":desc,"url":C["domain"]+"/siparis.html","isPartOf":{"@id":C["domain"]+"/#website"},"about":{"@id":C["domain"]+"/#business"}}]
    body = page_head("Sipariş oluştur", "Ürünleri işaretle, adresini yaz, WhatsApp'a gönder. Mesajı biz okur, stok ve süreyi hemen yazarız.", [("/","Ana Sayfa"),("/siparis.html","Sipariş Ver")]) + f"""
<section><div class="wrap"><div class="builder">
 <div><p style="background:#FFF4D6;border:1px solid #F3D48A;border-radius:10px;padding:12px 16px;font-size:.92rem;color:var(--ink-2)"><strong>Not:</strong> Alkollü içki ve tütün ürünleri mevzuat gereği uzaktan sipariş edilemez ve eve gönderilmez; yalnızca dükkânda, kimlikle. Bu liste teslimata uygun ürünleri içerir.</p>{groups}<p style="color:var(--ink-2)">Listede olmayan bir ürün mü var? Sağdaki "Not" alanına yaz, varsa getiririz.</p></div>
 <div class="side"><div class="card summary">
  <h3>Siparişin</h3>
  <ul id="cartlist"></ul><p class="empty" id="cartempty">Henüz ürün seçmedin. Soldan + ile ekle.</p>
  <label for="addr">Adres (mahalle, sokak, bina, daire, zil)</label>
  <textarea id="addr" rows="3" placeholder="Örn: Kordonboyu Mah. Ankara Cad. No:12 Deniz Apt. D:5, zil: Yılmaz"></textarea>
  <label for="note">Not (marka tercihi, kapı kodu vb.)</label>
  <input id="note" type="text" placeholder="İsteğe bağlı">
  <a id="sendwa" class="btn btn-wa" href="{WA_DEFAULT}" rel="noopener">{I_WA}WhatsApp'a Gönder</a>
  <a class="btn btn-tel" href="tel:{C['phone_e164']}" style="margin-top:8px">{I_TEL}Ya da ara: {C['phone_display']}</a>
  <p style="font-size:.85rem;color:var(--ink-3);margin:12px 0 0">Kapıda nakit/kart · Raf fiyatı · Her gün {C['opens']}–{C['closes']}</p>
 </div></div>
</div></div></section>
{faq_block(SSS[:4])}
"""
    write("/siparis.html", head(title, desc, "/siparis.html", schemas) + body + foot())

# ─────────────────────────────── ÜRÜNLER ───────────────────────────────
def build_urunler():
    title = "Ürünler | Buz, Tonik, Soda, Meze, Çerez | Marin Tekel Kartal"
    desc = "Kartal'da tekelden eve teslim: torba buz, tonik, soda, mikserler, meze, çerez, cips, çikolata, temel gıda. Raf fiyatına. Yaş sınırlı ürünler yalnızca dükkânda."
    cats = "".join(f'<div class="cat" id="{slug(k[0])}"><div class="ico">{k[1]}</div><h3>{k[0]}</h3><p>{k[2]}</p><ul>{"".join(f"<li>{i}</li>" for i in k[3])}</ul></div>' for k in KATEGORILER)
    schemas=[breadcrumb([("/","Ana Sayfa"),("/urunler.html","Ürünler")]),{"@context":"https://schema.org","@type":"ItemList","name":"Marin ürün kategorileri","itemListElement":[{"@type":"ListItem","position":i+1,"name":k[0],"url":C["domain"]+"/urunler.html#"+slug(k[0])} for i,k in enumerate(KATEGORILER)]}]
    body = page_head("Tekelde ne varsa (teslimata uygun olanlar)", "Fiyatlar dükkândaki raf fiyatıyla birebir aynı. Marka belirtmezseniz en çok tercih edileni göndeririz. Alkollü içki ve tütün ürünleri mevzuat gereği yalnızca dükkânda, kimlik kontrolüyle satılır.", [("/","Ana Sayfa"),("/urunler.html","Ürünler")]) + f"""
<section><div class="wrap"><div class="cats">{cats}</div>
<div class="card" style="margin-top:28px"><h3>Fiyat listesi neden yok?</h3><p style="margin:0;color:var(--ink-2)">Çünkü fiyatlar raf etiketiyle aynı ve sık değişiyor; sitede eski fiyat görüp kapıda farklı fiyatla karşılaşmanızı istemiyoruz. Belirli bir ürünün fiyatını <a href="{wa('Merhaba, şu ürünün fiyatını öğrenebilir miyim: ')}" rel="noopener">WhatsApp'tan sorun</a>, saniyeler içinde yazalım.</p></div>
</div></section>
{cta_band("Seçtin mi? {eta} içinde kapında.")}
"""
    write("/urunler.html", head(title, desc, "/urunler.html", schemas) + body + foot())

# ─────────────────────────────── BÖLGELER ───────────────────────────────
def build_bolgeler():
    title = "Teslimat Bölgeleri | Kartal'ın Tüm Mahalleleri | Marin Tekel"
    desc = "Kartal'ın tekeli Marin'den Karlıktepe, Kordonboyu, Yukarı, Orta, Hürriyet, Soğanlık, Cevizli, Yakacık, Dragos'a buz ve mikser servisi. Mahalle mahalle süreler."
    rows = "".join(f'<tr><td><a href="/bolge/{b[0]}.html">{esc(b[1])}</a></td><td>{b[5]}</td><td>{b[2]}</td><td>{esc(b[3])}</td></tr>' for b in BOLGELER)
    schemas=[breadcrumb([("/","Ana Sayfa"),("/teslimat-bolgeleri.html","Teslimat Bölgeleri")]),{"@context":"https://schema.org","@type":"ItemList","name":"Marin teslimat bölgeleri","itemListElement":[{"@type":"ListItem","position":i+1,"name":b[1],"url":C["domain"]+f"/bolge/{b[0]}.html"} for i,b in enumerate(BOLGELER)]}]
    body = page_head("Kartal'ın her mahallesine gidiyoruz", f"Karlıktepe'deki dükkânımızdan motorlu kuryeyle. Süreler akşam trafiği dahil ortalamadır; gece daha hızlıdır.", [("/","Ana Sayfa"),("/teslimat-bolgeleri.html","Teslimat Bölgeleri")]) + f"""
<section><div class="wrap">
<div class="prose" style="max-width:100%"><div style="overflow-x:auto"><table><thead><tr><th>Mahalle</th><th>İlçe</th><th>Tahmini süre</th><th>Yakın noktalar</th></tr></thead><tbody>{rows}</tbody></table></div></div>
<p style="color:var(--ink-2)">Adresiniz listede değilse de yazın; Kartal sınırına yakın Maltepe ve Pendik adreslerine çoğu zaman gidebiliyoruz.</p>
</div></section>
{cta_band()}
"""
    write("/teslimat-bolgeleri.html", head(title, desc, "/teslimat-bolgeleri.html", schemas) + body + foot())

def build_bolge(b):
    s,name,eta,near,note,ilce = b
    path = f"/bolge/{s}.html"
    title = f"{name.split(' (')[0].replace(' Mahallesi','').replace('Yakacık Yeni Mahalle','Yakacık Yeni')} Tekel | Gece Açık, {eta} Kapında | Marin Kartal"
    desc = f"{name.split(' (')[0]} ({ilce}) için gece 02:00'ye kadar açık tekel. Buz, tonik, soda, meze, çerez raf fiyatına ortalama {eta} içinde kapında. {C['phone_display']}"
    qs = [
      (f"{name}'e en yakın tekel hangisi?", f"{C['brand']}, Karlıktepe İnönü Caddesi No:75'te; {name} bölgesine {eta} mesafede ve her gün {C['closes']}'ye kadar açık. Kartal'da bu saate kadar açık tekel sayısı çok azdır."),
      (f"{name} bölgesine ne kadar sürede geliyorsunuz?", f"{name} için ortalama {eta}. Gece saatlerinde trafik olmadığından genelde daha hızlı."),
      (f"{name}'e alkollü içecek gönderiyor musunuz?", "Hayır. Mevzuat gereği alkollü içki ve tütün ürünleri uzaktan sipariş edilemez, eve gönderilemez; yalnızca dükkânımızda kimlik kontrolüyle satılır. Buz, tonik, soda, meze ve çerez kapınıza gelir."),
      (f"{name}'e gece de teslimat var mı?", f"Evet. Her gün {C['closes']}'ye kadar sipariş alıyor ve teslim ediyoruz."),
      (f"{name}'de teslimat ücreti var mı?", "Ürün fiyatları raf fiyatıyla aynıdır. Bölgeye ve sipariş tutarına göre cüzi bir teslimat ücreti olabilir; varsa sipariş sırasında söylenir."),
      ("Hangi ürünleri gönderiyorsunuz?", "Torba buz, tonik, soda, gazoz, limon-nane, meze, kuruyemiş, cips, çikolata, dondurma, ekmek-süt-yumurta, temizlik ve kişisel bakım, bebek bezi, çakmak, pil. Listede olmayanı sorun, varsa getiririz."),
    ]
    others = [x for x in BOLGELER if x[0]!=s][:8]
    schemas = [
      local_business({"@id":C["domain"]+path+"#business","url":C["domain"]+path,"name":f"{C['brand']} – {name} Teslimat","areaServed":{"@type":"Place","name":f"{name}, {ilce}, İstanbul"}}),
      breadcrumb([("/","Ana Sayfa"),("/teslimat-bolgeleri.html","Teslimat Bölgeleri"),(path,name)]),
      faq_schema(qs),
      {"@context":"https://schema.org","@type":"Service","name":f"{name} tekel teslimatı (buz, mikser, meze)","serviceType":"Tekel ürünleri eve teslimat (yaş sınırlı ürünler hariç)","provider":{"@id":C["domain"]+"/#business"},"areaServed":{"@type":"Place","name":f"{name}, {ilce}, İstanbul"},"hoursAvailable":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":C["opens"],"closes":C["closes"]},"offers":{"@type":"Offer","priceCurrency":"TRY","description":"Raf fiyatına teslimat"}},
    ]
    wa_msg = wa(f"Merhaba Marin, {name} bölgesine sipariş vermek istiyorum.\nAdres: \nÜrünler: ")
    body = page_head(f"{name} tekel: gece 02:00'ye kadar açık", f"{ilce}, {name} için Kartal'ın tekeli. Buz, tonik, soda, meze ve çerez raf fiyatına, ortalama <strong>{eta}</strong> içinde kapında. Her gün {C['opens']}–{C['closes']}.", [("/","Ana Sayfa"),("/teslimat-bolgeleri.html","Teslimat Bölgeleri"),(path,name)]) + f"""
<section><div class="wrap"><div class="two">
 <div class="prose">
  <p><strong>{name}</strong> ({ilce}) için en yakın gece açık tekel {C['brand']}. Karlıktepe İnönü Caddesi'ndeki dükkânımızdan torba buz, tonik, soda, gazoz, limon-nane, meze, kuruyemiş, cips ve çikolatayı kendi kuryemizle {name} bölgesine ortalama <strong>{eta}</strong> içinde ulaştırıyoruz. Alkollü içki ve tütün ürünleri mevzuat gereği yalnızca dükkânda, kimlik kontrolüyle satılır; sipariş akışına dahil değildir.</p>
  <h2>{name} tekel bayii: en yakın gece açık tekel</h2>
  <p>{name}'de tekel arayanlar için {C['brand']} en pratik seçenek: her gün {C['opens']}–{C['closes']} açık, {name} bölgesine {eta} içinde kurye. Alkollü içki ve tütün ürünleri için dükkâna gelin (18+ kimlik); buz, mikser ve meze için yazın, kapınıza gelsin.</p>
  <h2>{name} için teslimat notu</h2>
  <p>{note} Yakın noktalar: {near}.</p>
  <h2>Nasıl sipariş verilir?</h2>
  <ol>
   <li><a href="tel:{C['phone_e164']}">{C['phone_display']}</a> numarasını arayın ya da <a href="{wa_msg}" rel="noopener">WhatsApp'tan yazın</a>.</li>
   <li>Adresinizi tam yazın: {name}, sokak, bina, daire, zil.</li>
   <li>Ürünleri yazın ya da <a href="/siparis.html">sipariş sayfasından</a> seçin.</li>
   <li>Kapıda nakit veya kartla ödeyin.</li>
  </ol>
  <h2>{name}'de en çok ne isteniyor?</h2>
  <p>Akşam saatlerinde torba buz, tonik ve soda; gece yarısından sonra çerez, cips ve çikolata; sabahları ekmek, süt ve yumurta. Hepsi dükkândaki raf fiyatıyla.</p>
  <h2>Yakın bölgeler</h2>
  <div class="areas">{''.join(f'<a href="/bolge/{o[0]}.html">{esc(o[1])}<small>{o[2]}</small></a>' for o in others)}</div>
 </div>
 <aside class="side"><div class="card">
  <h3>{name} için sipariş</h3>
  <dl class="kv"><dt>Süre</dt><dd>{eta}</dd><dt>Saat</dt><dd>Her gün {C['opens']}–{C['closes']}</dd><dt>Fiyat</dt><dd>Raf fiyatı, fark yok</dd><dt>Ödeme</dt><dd>Kapıda nakit / kart</dd></dl>
  <div class="stack" style="display:grid;gap:8px;margin-top:16px"><a class="btn btn-wa" href="{wa_msg}" rel="noopener" style="justify-content:center">{I_WA}WhatsApp'tan Sipariş</a><a class="btn btn-tel" href="tel:{C['phone_e164']}" style="justify-content:center">{I_TEL}{C['phone_display']}</a></div>
 </div></aside>
</div></div></section>
{faq_block(qs, f"{name} teslimatı hakkında")}
{cta_band("{name} için buz ve mikser siparişi ver.".replace("{name}",name))}
"""
    write(path, head(title, desc, path, schemas) + body + foot())


# ─────────────────────────────── KARTAL TEKEL (hedef: "kartal tekel" sorguları) ───────────────────────────────
def build_kartal_tekel():
    path="/kartal-tekel.html"
    title = "Kartal Tekel | Gece 02:00'ye Kadar Açık Tekel Bayii | Marin"
    desc = f"Kartal'da tekel mi arıyorsunuz? Marin Tekel 2, Karlıktepe İnönü Cd. No:75'te her gün {C['opens']}–{C['closes']} açık tekel bayii. Kartal merkez, sahil ve metroya yakın. {C['phone_display']}"
    qs = [
      ("Kartal'da gece açık tekel var mı?", f"Evet. {C['brand']} her gün {C['closes']}'ye kadar açık. Kartal'da 02:00'ye kadar açık tekel bayii sayısı çok azdır; Karlıktepe İnönü Caddesi No:75'teyiz."),
      ("Kartal'da 24 saat açık tekel var mı?", "Kartal'da 7/24 açık tekel yoktur; mevzuat gereği alkollü içki satışı 22:00–06:00 arasında yapılamaz. Dükkânımız 02:00'ye kadar açıktır ve bu saatlerde buz, mikser, meze, çerez ve market ürünleri satışı ile teslimatı sürer."),
      ("Kartal'da en yakın tekel nerede?", "Karlıktepe'deyseniz İnönü Caddesi No:75. Kartal merkez, Kordonboyu sahil, Yukarı ve Orta Mahalle'den 5–10 dakika; Soğanlık metro ve Hürriyet'ten 10–15 dakika."),
      ("Kartal tekel telefon numarası nedir?", f"{C['phone_display']}. Aynı numara WhatsApp'tır; buz, mikser ve meze siparişi için yazabilirsiniz."),
      ("Tekelden eve sipariş verebilir miyim?", "Buz, tonik, soda, limon, meze, çerez, cips, çikolata ve market ürünleri için evet, raf fiyatına kapınıza geliyor. Alkollü içki ve tütün ürünleri mevzuat gereği (4250 ve 4207 sayılı kanunlar) uzaktan satılamaz ve eve gönderilemez; bunlar için dükkâna gelin, 18+ kimlik kontrolüyle."),
      ("Kartal sahilden tekele nasıl giderim?", "Kordonboyu'ndan İnönü Caddesi'ne kuzeye çıkın; yürüyerek 10–12 dakika, araçla 4–5 dakika. Yol tarifi için Google Haritalar linkine tıklayın."),
    ]
    mahalle_links = "".join(f'<a href="/bolge/{b[0]}.html">{esc(b[1])} tekel<small>{b[2]}</small></a>' for b in BOLGELER)
    schemas=[breadcrumb([("/","Ana Sayfa"),(path,"Kartal Tekel")]), faq_schema(qs),
      {"@context":"https://schema.org","@type":"WebPage","name":title,"description":desc,"url":C["domain"]+path,"isPartOf":{"@id":C["domain"]+"/#website"},"about":{"@id":C["domain"]+"/#business"},"speakable":{"@type":"SpeakableSpecification","cssSelector":[".page-head h1",".page-head p"]}}]
    body = page_head("Kartal tekel: Karlıktepe'de, 02:00'ye kadar açık", f"Kartal'da tekel arıyorsanız adres belli: {C['brand']}, İnönü Caddesi No:75. Kartal merkez, sahil ve metroya dakikalar uzaklıkta, her gün {C['opens']}–{C['closes']} açık tekel bayii.", [("/","Ana Sayfa"),(path,"Kartal Tekel")]) + f"""
<section><div class="wrap"><div class="two">
 <div class="prose">
  <p><strong>{C['brand']}</strong>, Kartal'ın Karlıktepe Mahallesi'nde faaliyet gösteren bir tekel bayiidir. Kartal'da tekel arayanların en sık sorduğu üç şey için kısa cevap: <strong>Nerede?</strong> İnönü Caddesi No:75, Kartal merkezin hemen kuzeyi. <strong>Kaça kadar açık?</strong> Her gün {C['closes']}'ye kadar. <strong>Telefon?</strong> <a href="tel:{C['phone_e164']}">{C['phone_display']}</a>.</p>
  <h2>Kartal'da gece açık tekel</h2>
  <p>Kartal'da çoğu tekel 23:00–00:00 arasında kapanır. Biz dükkânı {C['closes']}'ye kadar açık tutuyoruz; sahilden dönenler, geç çalışanlar ve hastane çevresinde kalanlar için. Alkollü içki satışı mevzuat gereği 22:00'den sonra yapılmaz; gece saatlerinde buz, tonik, soda, meze, çerez ve market ürünleri satışı ile teslimatı devam eder.</p>
  <h2>Kartal merkez, sahil ve metroya yakın tekel</h2>
  <ul>
   <li><strong>Kartal Meydanı / Kordonboyu sahil:</strong> 4–5 dk araçla, 10–12 dk yürüyerek.</li>
   <li><strong>Kartal metro (M4):</strong> 5–7 dk araçla.</li>
   <li><strong>Soğanlık metro:</strong> 8–10 dk araçla.</li>
   <li><strong>Kartal Belediyesi / Yukarı Mahalle:</strong> 3–5 dk araçla.</li>
   <li><strong>Dr. Lütfi Kırdar Şehir Hastanesi (Cevizli):</strong> 10–12 dk araçla.</li>
  </ul>
  <h2>Kartal tekel bayii: dükkânda ne var?</h2>
  <p>Geniş soğuk içecek dolabı, her saat torba buz, tonik-soda-gazoz ve mikserler, meze ve çerez rafı, çikolata, dondurma, temel gıda, kişisel bakım ve temizlik. Alkollü içki ve tütün ürünleri 18 yaş üstüne, kimlik kontrolüyle, yalnızca dükkânda satılır.</p>
  <h2>Tekelden eve ne sipariş edilir?</h2>
  <p>Buz, mikser, meze, çerez, cips, çikolata, su, ayran, ekmek-süt-yumurta, temizlik ve kişisel bakım ürünleri: hepsi raf fiyatına, ortalama {C['eta']} içinde Kartal'ın her mahallesine. <a href="/siparis.html">Sipariş oluşturun</a> ya da <a href="{WA_DEFAULT}" rel="noopener">WhatsApp'tan yazın</a>. Alkollü içki ve tütün ürünleri mevzuat gereği sipariş akışında yoktur.</p>
  <h2>Kartal'ın mahallelerine en yakın tekel</h2>
  <div class="areas">{mahalle_links}</div>
 </div>
 <aside class="side"><div class="card">
  <h3>Marin Tekel 2</h3>
  <dl class="kv"><dt>Adres</dt><dd>{esc(C['address_full'])}</dd><dt>Saat</dt><dd>Her gün {C['opens']}–{C['closes']}</dd><dt>Telefon</dt><dd><a href="tel:{C['phone_e164']}">{C['phone_display']}</a></dd><dt>Google</dt><dd>★ {C['rating']} ({C['review_count']} yorum)</dd><dt>Durum</dt><dd><span class="status" data-status><i></i><span data-status-text>{C['opens']}–{C['closes']}</span></span></dd></dl>
  <div style="display:grid;gap:8px;margin-top:16px"><a class="btn btn-ink" href="{C['maps_url']}" rel="noopener" target="_blank" style="justify-content:center">Yol tarifi al ↗</a><a class="btn btn-wa" href="{WA_DEFAULT}" rel="noopener" style="justify-content:center">{I_WA}WhatsApp</a><a class="btn btn-tel" href="tel:{C['phone_e164']}" style="justify-content:center">{I_TEL}{C['phone_display']}</a></div>
 </div><div class="map" data-src="{C['maps_embed']}" style="margin-top:14px"></div></aside>
</div></div></section>
{faq_block(qs, "Kartal tekel hakkında sık sorulanlar")}
{cta_band("Buz ve mikser için yaz, dükkân için gel.", "Her gün 02:00'ye kadar. Raf fiyatı, fark yok.")}
"""
    write(path, head(title, desc, path, schemas) + body + foot())

# ─────────────────────────────── SSS ───────────────────────────────
def build_sss():
    title = "SSS | Kartal Tekel Siparişi Hakkında Her Şey | Marin"
    desc = "Kartal'ın tekeli Marin: hangi ürünler eve gelir, alkol neden gönderilmez, teslimat süresi, fiyat farkı, çalışma saatleri, bölgeler ve ödeme."
    schemas=[breadcrumb([("/","Ana Sayfa"),("/sss.html","SSS")]), faq_schema(SSS)]
    body = page_head("Sık sorulan sorular", "Cevabını bulamadığınız soru için WhatsApp'tan yazın, dakikalar içinde dönelim.", [("/","Ana Sayfa"),("/sss.html","SSS")]) + faq_block(SSS, "Her şeyi sorduk, cevapladık") + cta_band()
    write("/sss.html", head(title, desc, "/sss.html", schemas) + body + foot())

# ─────────────────────────────── HAKKIMIZDA ───────────────────────────────
def build_hakkimizda():
    title = "Hakkımızda | Karlıktepe'nin Tekeli | Marin Tekel 2 Kartal"
    desc = "Marin Tekel 2, Kartal Karlıktepe İnönü Caddesi'nde esnaf bir tekel bayii. Google'da 5.0 puan. Neden 02:00'ye kadar açığız, neden fiyat farkı almıyoruz."
    schemas=[breadcrumb([("/","Ana Sayfa"),("/hakkimizda.html","Hakkımızda")]),{"@context":"https://schema.org","@type":"AboutPage","name":title,"url":C["domain"]+"/hakkimizda.html","about":{"@id":C["domain"]+"/#business"}}]
    body = page_head("Karlıktepe'nin tekeli, Kartal'ın gece adresi", "İnönü Caddesi'nde bir esnaf tekeli. Geniş içecek rafları, her saat buz, masanın tüm eksikleri.", [("/","Ana Sayfa"),("/hakkimizda.html","Hakkımızda")]) + f"""
<section><div class="wrap"><div class="two">
 <div class="prose">
  <p><strong>{C['brand']}</strong>, Kartal'ın Karlıktepe Mahallesi'nde, İnönü Caddesi No:75'te bulunan bir tekel bayiidir. Tabeladaki "2", Kartal'daki ikinci dükkânımız olduğu anlamına gelir; aynı esnaf anlayışıyla, daha geniş raflarla. Yaş sınırlı ürünler yalnızca dükkânda, 18 yaş üstüne kimlik kontrolüyle satılır; buz, mikser, meze ve diğer her şeyi eve getiriyoruz.</p>
  <h2>Neden gece 02:00'ye kadar açığız?</h2>
  <p>Kartal sahili, hastane çevresi ve geç saatte çalışanlar için 22:00'de kapanan market işe yaramıyor. Biz de kepengi en son indiren olduk. Gece gelen müşterilerimiz için eve teslimatı da aynı saatlere uzattık.</p>
  <h2>Neden fiyat farkı almıyoruz?</h2>
  <p>Teslimat uygulamalarının komisyonu yüzde 20'nin üzerinde; o fark ya fiyata ya esnafa yansıyor. Kendi kuryemizle çalışıyoruz ve dükkân zaten açık. Kapıya giden ürünün fiyatı raf fiyatıyla aynı, bu kadar basit. Detayı <a href="/blog/gel-al-fiyatina-eve-teslim.html">blogda</a> anlattık.</p>
  <h2>"Yoksa getiriyorlar"</h2>
  <p>Google yorumlarımızda tekrar eden cümle bu. Rafta olmayan bir ürün istediğinizde mümkünse temin edip getiriyoruz. Bu, bir uygulamanın yapamayacağı, sadece mahalle esnafının yapabileceği bir şey.</p>
  <h2>Bize ulaşın</h2>
  <p>Telefon: <a href="tel:{C['phone_e164']}">{C['phone_display']}</a> · WhatsApp: <a href="{WA_DEFAULT}" rel="noopener">aynı numara</a> · Adres: {esc(C['address_full'])}</p>
 </div>
 <aside class="side">
  <div class="card"><h3>Künye</h3><dl class="kv"><dt>İşletme</dt><dd>{esc(C['brand'])}</dd><dt>Tür</dt><dd>Tekel bayii / market</dd><dt>Adres</dt><dd>{esc(C['address_full'])}</dd><dt>Telefon</dt><dd><a href="tel:{C['phone_e164']}">{C['phone_display']}</a></dd><dt>Saatler</dt><dd>Her gün {C['opens']}–{C['closes']}</dd><dt>Google</dt><dd>★ {C['rating']} ({C['review_count']} yorum)</dd></dl></div>
  <div class="map" data-src="{C['maps_embed']}" style="margin-top:14px"></div>
 </aside>
</div></div></section>
{cta_band()}
"""
    write("/hakkimizda.html", head(title, desc, "/hakkimizda.html", schemas) + body + foot())

# ─────────────────────────────── İLETİŞİM ───────────────────────────────
def build_iletisim():
    title = f"İletişim | {C['phone_display']} | Marin Kartal Karlıktepe"
    desc = f"{C['brand']} iletişim: {C['phone_display']} (telefon ve WhatsApp). {C['address_full']}. Her gün {C['opens']}–{C['closes']}."
    schemas=[breadcrumb([("/","Ana Sayfa"),("/iletisim.html","İletişim")]),{"@context":"https://schema.org","@type":"ContactPage","name":title,"url":C["domain"]+"/iletisim.html","about":{"@id":C["domain"]+"/#business"}}]
    body = page_head("İletişim", "Tek numara, iki kanal: ara ya da WhatsApp'tan yaz.", [("/","Ana Sayfa"),("/iletisim.html","İletişim")]) + f"""
<section><div class="wrap"><div class="two">
 <div>
  <div class="card" style="margin-bottom:16px"><h3>Sipariş ve bilgi</h3>
   <div style="display:grid;gap:10px;margin-top:12px"><a class="btn btn-tel" href="tel:{C['phone_e164']}" style="justify-content:center">{I_TEL}{C['phone_display']}</a><a class="btn btn-wa" href="{WA_DEFAULT}" rel="noopener" style="justify-content:center">{I_WA}WhatsApp'tan yaz</a></div>
   <p style="margin:14px 0 0;color:var(--ink-2);font-size:.95rem">Uluslararası format: <a href="tel:{C['phone_e164']}">{C['phone_intl']}</a></p>
  </div>
  <div class="card"><h3>Dükkân</h3>
   <dl class="kv"><dt>Adres</dt><dd>{esc(C['address_full'])}</dd><dt>Saatler</dt><dd>Her gün {C['opens']}–{C['closes']}</dd><dt>Durum</dt><dd><span class="status" data-status><i></i><span data-status-text>{C['opens']}–{C['closes']}</span></span></dd><dt>Yol tarifi</dt><dd><a href="{C['maps_url']}" rel="noopener" target="_blank">Google Haritalar'da aç ↗</a></dd></dl>
  </div>
 </div>
 <div class="map" data-src="{C['maps_embed']}"></div>
</div></div></section>
"""
    write("/iletisim.html", head(title, desc, "/iletisim.html", schemas) + body + foot())

# ─────────────────────────────── BLOG ───────────────────────────────
def build_blog():
    title = "Blog | Kartal Tekel, Buz, Mikser ve Mahalle Rehberi | Marin"
    desc = "Kartal'da gece açık market, eve sipariş rehberi, gel-al fiyatı ve mahalle mahalle teslimat süreleri."
    schemas=[breadcrumb([("/","Ana Sayfa"),("/blog/","Blog")]),{"@context":"https://schema.org","@type":"Blog","name":"Marin Blog","url":C["domain"]+"/blog/","publisher":{"@id":C["domain"]+"/#business"}}]
    posts = "".join(f'<a class="post rv" href="/blog/{p["slug"]}.html"><time datetime="{p["date"]}">{tr_date(p["date"])}</time><h3>{esc(p["title"])}</h3><p>{esc(p["desc"])}</p></a>' for p in BLOG)
    body = page_head("Blog", "Kartal'da yaşayanlar için kısa, işe yarar yazılar.", [("/","Ana Sayfa"),("/blog/","Blog")]) + f'<section><div class="wrap"><div class="posts">{posts}</div></div></section>' + cta_band()
    write("/blog/index.html", head(title, desc, "/blog/", schemas) + body + foot())
    tablo = '<table><thead><tr><th>Mahalle</th><th>Süre</th></tr></thead><tbody>' + "".join(f'<tr><td><a href="/bolge/{b[0]}.html">{esc(b[1])}</a></td><td>{b[2]}</td></tr>' for b in BOLGELER) + '</tbody></table>'
    for p in BLOG:
        path = f"/blog/{p['slug']}.html"
        content = p["body"] % {"tel":C["phone_e164"],"phone":C["phone_display"],"eta":C["eta"],"wa":WA_DEFAULT,"tablo":tablo}
        schemas=[breadcrumb([("/","Ana Sayfa"),("/blog/","Blog"),(path,p["title"])]),
          {"@context":"https://schema.org","@type":"Article","headline":p["title"],"description":p["desc"],"datePublished":p["date"],"dateModified":p["date"],"inLanguage":"tr","mainEntityOfPage":C["domain"]+path,"image":C["domain"]+"/assets/og.png",
           "author":{"@type":"Organization","name":C["brand"],"url":C["domain"]+"/"},"publisher":{"@type":"Organization","name":C["brand"],"logo":{"@type":"ImageObject","url":C["domain"]+"/assets/logo.svg"}},"about":{"@id":C["domain"]+"/#business"}}]
        others = "".join(f'<a class="post" href="/blog/{o["slug"]}.html"><time datetime="{o["date"]}">{tr_date(o["date"])}</time><h3>{esc(o["title"])}</h3></a>' for o in BLOG if o["slug"]!=p["slug"])
        body = page_head(esc(p["title"]), esc(p["desc"]), [("/","Ana Sayfa"),("/blog/","Blog"),(path,p["title"][:40]+"…")]) + f"""
<section><div class="wrap"><div class="two"><article class="prose"><p style="color:var(--ink-3);font-size:.9rem"><time datetime="{p['date']}">{tr_date(p['date'])}</time> · {C['brand']}</p>{content}</article>
<aside class="side"><div class="card"><h3>Hemen sipariş</h3><div style="display:grid;gap:8px;margin-top:10px"><a class="btn btn-wa" href="{WA_DEFAULT}" rel="noopener" style="justify-content:center">{I_WA}WhatsApp</a><a class="btn btn-tel" href="tel:{C['phone_e164']}" style="justify-content:center">{I_TEL}{C['phone_display']}</a></div></div></aside></div>
<h2 style="margin-top:48px">Diğer yazılar</h2><div class="posts">{others}</div></div></section>
"""
        write(path, head(p["title"], p["desc"], path, schemas, og_type="article") + body + foot())

def tr_date(iso):
    y,m,d = iso.split("-")
    ay = ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"][int(m)-1]
    return f"{int(d)} {ay} {y}"

# ─────────────────────────────── 404 ───────────────────────────────
def build_404():
    body = page_head("Sayfa bulunamadı", "Aradığınız sayfa taşınmış ya da hiç olmamış olabilir. Ama sipariş hattı her zaman açık.", [("/","Ana Sayfa"),("/404.html","404")]) + f"""
<section><div class="wrap"><div class="areas">{''.join(f'<a href="{u}">{n}</a>' for u,n in NAV)}</div></div></section>{cta_band()}"""
    write("/404.html", head("Sayfa bulunamadı | "+C["brand"], "Sayfa bulunamadı.", "/404.html", [], noindex=True) + body + foot())

# ─────────────────────────────── TEKNİK DOSYALAR ───────────────────────────────
def build_tech():
    urls = [("/",1.0,"daily"),("/kartal-tekel.html",0.9,"weekly"),("/siparis.html",0.9,"weekly"),("/urunler.html",0.8,"weekly"),("/teslimat-bolgeleri.html",0.8,"weekly"),("/sss.html",0.7,"monthly"),("/hakkimizda.html",0.6,"monthly"),("/iletisim.html",0.7,"monthly"),("/blog/",0.6,"weekly")]
    urls += [(f"/bolge/{b[0]}.html",0.7,"monthly") for b in BOLGELER]
    urls += [(f"/blog/{p['slug']}.html",0.6,"monthly") for p in BLOG]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{C['domain']}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{cf}</changefreq><priority>{p}</priority></url>\n" for u,p,cf in urls) + "</urlset>\n"
    write("/sitemap.xml", sm)
    write("/robots.txt", f"User-agent: *\nAllow: /\n\n# AI arama botları açıkça izinli (AI SEO / GEO)\nUser-agent: GPTBot\nAllow: /\nUser-agent: ChatGPT-User\nAllow: /\nUser-agent: OAI-SearchBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: Claude-SearchBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\nUser-agent: Applebot-Extended\nAllow: /\nUser-agent: Bingbot\nAllow: /\n\nSitemap: {C['domain']}/sitemap.xml\n")
    llms = f"""# {C['brand']} (tekelsiparis.com)

> Kartal (İstanbul) Karlıktepe'de her gün {C['opens']}–{C['closes']} açık tekel bayii. Kartal'ın tüm mahallelerine ve Maltepe–Pendik sınırına kendi kuryesiyle buz, tonik, soda, meze, çerez ve market ürünlerini raf fiyatına ("gel-al fiyatına"), ortalama {C['eta']} içinde teslim eder. Alkollü içki ve tütün ürünleri Türkiye mevzuatı (4250 ve 4207 sayılı kanunlar) gereği uzaktan sipariş edilemez ve eve gönderilmez; yalnızca dükkânda 18+ kimlik kontrolüyle satılır. Sipariş telefon veya WhatsApp ile verilir: {C['phone_intl']}.

## Temel bilgiler

- [Künye]({C['domain']}/hakkimizda.html): İşletme bilgileri aşağıda özetlenmiştir
- İşletme adı: {C['brand']}
- Tür: Tekel bayii (liquor store) ve market; teslimat yalnızca yaş sınırsız ürünler için
- Alkol/tütün: Sadece dükkânda, 18+ kimlik kontrolü; telefon/WhatsApp/internet siparişi ve eve teslim yapılmaz (yasal zorunluluk)
- Adres: {C['address_full']}
- Telefon ve WhatsApp: {C['phone_intl']} ({C['phone_display']})
- Çalışma saatleri: Her gün {C['opens']}–{C['closes']} (gece 02:00'ye kadar sipariş)
- Google puanı: {C['rating']}/5 ({C['review_count']} yorum)
- Fiyat politikası: Teslimatta raf fiyatı, fiyat farkı yok. Varsa teslimat ücreti sipariş anında söylenir.
- Ödeme: Kapıda nakit veya kart (POS)
- Teslimat süresi: Ortalama {C['eta']}; uzak mahallelerde 45 dk'ya kadar
- Eve gelen ürünler: Torba buz, tonik, soda, gazoz, limon-nane, meze, kuruyemiş, cips, çikolata, dondurma, ekmek-süt-yumurta, temizlik ve kişisel bakım, bebek bezi, çakmak, pil

## Teslimat bölgeleri
{chr(10).join(f"- [{b[1]} tekel teslimatı]({C['domain']}/bolge/{b[0]}.html): {b[5]}, tahmini {b[2]}, {b[3]}" for b in BOLGELER)}

## Sayfalar
- [Ana sayfa]({C['domain']}/): Kartal'ın gece 02:00'ye kadar açık tekeli; buz ve mikser gel-al fiyatına kapında
- [Kartal Tekel]({C['domain']}/kartal-tekel.html): Kartal'da tekel arayanlar için adres, saat, telefon, yol tarifi; "kartal tekel", "gece açık tekel", "en yakın tekel" sorularının cevabı
- [Sipariş oluştur]({C['domain']}/siparis.html): Ürün seçip tek dokunuşla WhatsApp siparişi
- [Ürünler]({C['domain']}/urunler.html): Su, buz, içecek, atıştırmalık, temel gıda, temizlik
- [Teslimat bölgeleri]({C['domain']}/teslimat-bolgeleri.html): Kartal mahalleleri ve tahmini süreler
- [SSS]({C['domain']}/sss.html): Teslimat süresi, fiyat, saat, ödeme
- [Hakkımızda]({C['domain']}/hakkimizda.html): Karlıktepe'nin tekeli
- [İletişim]({C['domain']}/iletisim.html): {C['phone_display']}, adres, harita

## Blog
{chr(10).join(f"- [{p['title']}]({C['domain']}/blog/{p['slug']}.html): {p['desc']}" for p in BLOG)}

## Sık sorulanlar
{chr(10).join(f"- S: {q}{chr(10)}  C: {re.sub(r'<[^>]+>','',a).replace('&ldquo;','“').replace('&rdquo;','”').replace('&ndash;','–')}" for q,a in SSS)}
"""
    write("/llms.txt", llms)
    write("/manifest.webmanifest", json.dumps({"name":C["brand"]+" – Kartal Tekel","short_name":"Marin","start_url":"/","display":"standalone","background_color":"#F7F3EA","theme_color":"#0B1B45","lang":"tr","icons":[{"src":"/assets/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/assets/icon-512.png","sizes":"512x512","type":"image/png"}]},ensure_ascii=False,indent=1))
    write("/_headers", "/*\n  X-Content-Type-Options: nosniff\n  X-Frame-Options: SAMEORIGIN\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: geolocation=(), camera=(), microphone=()\n  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n/*.html\n  Cache-Control: public, max-age=0, must-revalidate\n")
    write("/_redirects", "/bolge /teslimat-bolgeleri.html 301\n/blog /blog/ 301\n/index.html / 301\n")
    write("/.htaccess", "RewriteEngine On\nRewriteCond %{HTTPS} off\nRewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\nRewriteCond %{HTTP_HOST} ^www\\.(.*)$ [NC]\nRewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]\nErrorDocument 404 /404.html\nAddDefaultCharset UTF-8\n<IfModule mod_deflate.c>\nAddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml text/plain\n</IfModule>\n<IfModule mod_expires.c>\nExpiresActive On\nExpiresByType text/css \"access plus 1 year\"\nExpiresByType application/javascript \"access plus 1 year\"\nExpiresByType image/svg+xml \"access plus 1 year\"\nExpiresByType image/png \"access plus 1 year\"\nExpiresByType text/html \"access plus 0 seconds\"\n</IfModule>\n<IfModule mod_headers.c>\nHeader set X-Content-Type-Options nosniff\nHeader set Referrer-Policy strict-origin-when-cross-origin\nHeader set Strict-Transport-Security \"max-age=31536000; includeSubDomains\"\n</IfModule>\n")
    write("/.nojekyll", "")
    write("/CNAME", C["domain"].replace("https://",""))
    write("/assets/styles.css", CSS.strip()+"\n")
    write("/assets/main.js", JS.strip()+"\n")
    logo = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Marin"><rect width="64" height="64" rx="14" fill="#0B1B45"/><path d="M14 46V18h8l10 14 10-14h8v28h-8V31l-10 13-10-13v15z" fill="#FFB628"/><path d="M8 52c6-4 10-4 16 0s10 4 16 0 10-4 16 0" fill="none" stroke="#0FB5A8" stroke-width="3" stroke-linecap="round"/></svg>'
    write("/assets/logo.svg", logo); write("/favicon.svg", logo)

def build_images():
    from PIL import Image, ImageDraw, ImageFont
    def font(sz, bold=True):
        for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf","/System/Library/Fonts/Helvetica.ttc","/Library/Fonts/Arial.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
        return ImageFont.load_default()
    # OG 1200x630
    im = Image.new("RGB",(1200,630),"#0B1B45"); d = ImageDraw.Draw(im)
    for i in range(0,1200,56): d.line([(i,0),(i,630)],fill="#13245a",width=1)
    for j in range(0,630,56): d.line([(0,j),(1200,j)],fill="#13245a",width=1)
    d.ellipse([820,-200,1400,380],fill="#1E49C8")
    d.ellipse([-200,420,400,900],fill="#0FB5A8")
    d.rounded_rectangle([60,60,160,160],radius=24,fill="#FFB628"); d.text((110,110),"M",fill="#0B1B45",font=font(64),anchor="mm")
    d.text((60,200),"Kartal'ın 02:00'ye kadar açık tekeli.",fill="white",font=font(56))
    d.text((60,270),"Buz & mikser gel-al fiyatına kapında.",fill="#FFB628",font=font(56))
    d.text((60,370),f"Her gün {C['opens']}–{C['closes']}  ·  Ortalama {C['eta']}  ·  Google ★ {C['rating']}",fill="#DCE6FF",font=font(30,False))
    d.rounded_rectangle([60,440,560,520],radius=40,fill="#25D366"); d.text((310,480),f"WhatsApp  {C['phone_display']}",fill="#062b16",font=font(32),anchor="mm")
    d.text((60,560),f"{C['brand']}  ·  {C['address_full']}",fill="#9AA6D6",font=font(22,False))
    d.text((1140,590),"tekelsiparis.com",fill="white",font=font(26),anchor="rm")
    im.save(os.path.join(OUT,"assets","og.png"),optimize=True)
    # icons
    for sz,name in [(512,"icon-512.png"),(192,"icon-192.png"),(180,"icon-180.png")]:
        ic = Image.new("RGB",(sz,sz),"#0B1B45"); dd=ImageDraw.Draw(ic)
        dd.text((sz/2,sz/2-sz*0.04),"M",fill="#FFB628",font=font(int(sz*0.62)),anchor="mm")
        dd.arc([sz*0.12,sz*0.62,sz*0.5,sz*0.95],180,360,fill="#0FB5A8",width=max(4,sz//28)); dd.arc([sz*0.5,sz*0.62,sz*0.88,sz*0.95],180,360,fill="#0FB5A8",width=max(4,sz//28))
        ic.save(os.path.join(OUT,"assets",name),optimize=True)

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT,"assets"),exist_ok=True)
    build_tech(); build_images()
    build_index(); build_kartal_tekel(); build_siparis(); build_urunler(); build_bolgeler()
    for b in BOLGELER: build_bolge(b)
    build_sss(); build_hakkimizda(); build_iletisim(); build_blog(); build_404()
    n = sum(len(f) for _,_,f in os.walk(OUT))
    print(f"✓ {n} dosya üretildi → {OUT}")
