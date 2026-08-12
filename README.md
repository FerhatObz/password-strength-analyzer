# Password Strength Analyzer

Python ile geliştirdiğim, terminal üzerinden çalışan bir parola güvenlik analiz aracıdır.

Bu projeyi yapma amacım sadece kullanıcıdan bir parola alıp ekrana `Güçlü` veya `Zayıf` yazdırmak değil. Bir parolanın neden güçlü veya zayıf kabul edildiğini teknik olarak anlamak ve bu mantığı Python ile kendim uygulamak.

Parola güvenliği ilk bakışta basit bir konu gibi görünüyor. Bir parolanın uzun olması, büyük harf ve rakam içermesi bize güçlü olduğu izlenimini verebilir. Fakat gerçek değerlendirme bundan biraz daha karmaşık. Örneğin `Password123!` farklı karakter türleri içeriyor olmasına rağmen tahmin edilmesi zor bir parola değildir.

Bu yüzden bu projede bir parolayı tek bir kurala göre değerlendirmek yerine birkaç farklı kriteri birlikte inceleyeceğim.

---

## Proje Ne Yapıyor?

Program kullanıcıdan bir parola alıyor ve bu parolayı farklı güvenlik kriterlerine göre analiz ediyor.

Temel olarak şu kontrolleri yapmayı hedefliyorum:

- Parolanın uzunluğu
- Küçük harf kullanımı
- Büyük harf kullanımı
- Rakam kullanımı
- Özel karakter kullanımı
- Yaygın parola listesinde bulunup bulunmadığı
- Basit tekrar veya tahmin edilebilir desenler
- Tahmini entropy değeri
- Belirlediğimiz parola politikalarına uyup uymadığı

Sonunda bu bilgileri bir araya getirerek parolanın genel durumunu kullanıcıya anlaşılır bir şekilde göstereceğim.

Buradaki önemli nokta şu:

> Bu araç bir parola kırma aracı değildir. Girilen parolayı tahmin etmeye veya brute-force saldırısı gerçekleştirmeye çalışmaz. Amaç verilen parolanın güvenlik açısından analiz edilmesidir.

---

# Neden Böyle Bir Araca İhtiyacım Var?

Bir parolanın güvenliğini sadece uzunluğuna bakarak değerlendirmek doğru değildir.

Örneğin:

```text
aaaaaaaaaaaaaaaa
````

uzun bir parola gibi görünebilir. Fakat yalnızca tek bir karakterin tekrarından oluştuğu için tahmin edilebilirliği yüksektir.

Buna karşılık:

```text
T9!qL2#vP7@xK4$m
```

gibi bir parola farklı karakter kümelerini kullanır ve çok daha geniş bir olası kombinasyon alanına sahiptir.

Buradan şu sonucu çıkarabiliriz:

> Parola güvenliğini değerlendirirken tek bir özelliğe güvenmek yerine birden fazla özelliği birlikte incelemek gerekir.

Benim bu projedeki temel yaklaşımım da tam olarak bu olacak.

---

# Algoritmanın Genel Mantığı

Programın çalışma mantığını en basit hâliyle şöyle düşünebiliriz:

```text
Kullanıcı parolayı girer
        ↓
Parola analiz edilir
        ↓
Uzunluk kontrol edilir
        ↓
Karakter türleri belirlenir
        ↓
Yaygın parola listesi kontrol edilir
        ↓
Tekrar ve basit desenler kontrol edilir
        ↓
Entropy hesaplanır
        ↓
Parola politikası değerlendirilir
        ↓
Sonuçlar birleştirilir
        ↓
Kullanıcıya rapor gösterilir
```

Burada bütün kontrolleri tek bir if-else bloğuna doldurmak yerine mümkün olduğunca ayrı sorumluluklar hâlinde tasarlayacağım.

Bunun sebebi sadece kodun güzel görünmesi değil.

Örneğin ileride entropy hesaplama yöntemini değiştirmek istersem bütün analiz sistemini değiştirmek istemiyorum. Sadece entropy ile ilgili kısmı değiştirebilmeliyim.

Bu yüzden proje ilerledikçe kodu modüler hâle getireceğim.

---

# 1. Parola Uzunluğu

İlk kontrol edeceğimiz şey parolanın uzunluğu.

Uzunluk önemlidir çünkü kullanılabilecek karakter sayısı sabit kaldığında parola uzadıkça mümkün olan kombinasyonların sayısı da büyür.

Teorik olarak kullanılabilecek karakter sayısına `K`, parola uzunluğuna `L` dersek olası kombinasyon sayısını:

```text
K^L
```

şeklinde düşünebiliriz.

Örneğin 10 farklı karakter kullanılabiliyor ve parola 4 karakterden oluşuyorsa:

```text
10^4 = 10.000
```

farklı kombinasyon ortaya çıkar.

Parola uzunluğu arttıkça bu sayı çok hızlı şekilde büyür.

Fakat burada önemli bir problem var.

```text
aaaaaaaaaaaaaaaa
```

gibi bir parola uzun olsa bile tahmin edilmesi kolay olabilir.

Dolayısıyla uzunluk önemli bir kriterdir fakat tek başına yeterli değildir.

---

# 2. Karakter Kümeleri

Parolada hangi karakter türlerinin bulunduğunu da kontrol edeceğim.

Temel olarak dört karakter grubuna bakabiliriz:

```text
Lowercase       → küçük harf
Uppercase       → büyük harf
Digits          → rakam
Special Chars   → özel karakter
```

Örneğin:

```text
password123
```

şunları içerir:

```text
Küçük harf  ✓
Büyük harf  ✗
Rakam       ✓
Özel karakter ✗
```

Başka bir örnek:

```text
Password123!
```

ise dört grubun tamamını kullanıyor.

Fakat burada da önemli bir nokta var.

```text
Password123!
```

karakter çeşitliliği açısından iyi görünebilir fakat oldukça bilinen bir parola yapısına sahiptir.

Bu yüzden:

> Karakter çeşitliliği güvenlik açısından faydalıdır fakat tek başına yeterli değildir.

---

# 3. Common Password Kontrolü

Bir parolanın yaygın olarak kullanılan parolalar arasında bulunup bulunmadığını da kontrol edeceğim.

Örneğin:

```text
password
123456
qwerty
admin
```

gibi parolalar kullanıcı tarafından güçlü sanılabilir ancak saldırganların ilk deneyeceği parola adayları arasında bulunabilir.

Bu nedenle sadece:

> "Parola kaç karakter?"

sorusunu sormak yeterli değildir.

Aynı zamanda:

> "Bu parola daha önce çok fazla kişi tarafından kullanılmış mı?"

sorusunu da sormamız gerekir.

Bu kontrol için proje içerisinde bir wordlist kullanacağım:

```text
data/
└── common_passwords.txt
```

Program girilen parolayı bu listedeki değerlerle karşılaştıracak.

Buradaki amaç parola kırmak değil.

Amaç, girilen parolanın bilinen ve yaygın parola örneklerinden biri olup olmadığını kontrol etmek.

---

# 4. Pattern ve Repetition Kontrolü

Bir parola farklı karakter türlerini kullansa bile basit bir yapıya sahip olabilir.

Örneğin:

```text
aaaaaaaa
11111111
abababab
12345678
qwerty123
```

gibi örneklerde belirgin tekrar veya tahmin edilebilir desenler vardır.

Bu nedenle karakter çeşitliliğinin yanında parolanın yapısını da incelemek istiyorum.

İlk aşamada özellikle:

* Aynı karakterin tekrar etmesi
* Basit tekrarlar
* Çok belirgin sıralı yapılar
* Kolay tahmin edilebilecek kalıplar

üzerinde duracağım.

Buradaki amaç mükemmel bir yapay zekâ destekli parola tahmin sistemi oluşturmak değil.

Amaç, bariz zayıflıkları yakalayabilecek mantıklı bir analiz katmanı oluşturmak.

---

# 5. Entropy Nedir?

Bu projenin en önemli konularından biri entropy.

Parola güvenliğini konuşurken entropy, parolanın oluşturabileceği teorik belirsizlik veya olası kombinasyon alanını ifade etmek için kullanılabilir.

Basitleştirilmiş bir hesaplamada:

```text
Entropy = L × log2(K)
```

formülünü kullanabiliriz.

Burada:

```text
L = parola uzunluğu
K = kullanılabilecek karakter havuzunun büyüklüğü
```

anlamına gelir.

Örneğin sadece küçük harflerden oluşan bir parola ile küçük harf, büyük harf, rakam ve özel karakterlerden oluşan bir parola aynı uzunlukta olsa bile karakter havuzları aynı değildir.

Karakter havuzu büyüdükçe teorik arama alanı da büyür.

Bu yüzden entropy hesabı bize parolanın teorik karmaşıklığı hakkında önemli bir fikir verebilir.

---

# 6. Entropy Neden Tek Başına Yeterli Değil?

Burada özellikle dikkat etmek istediğim nokta şu:

> Yüksek entropy değeri tek başına gerçek hayatta güçlü parola garantisi vermez.

Örneğin insan tarafından oluşturulmuş bazı parolalar belirli kelime ve kalıplara dayanabilir.

Şöyle bir parola düşünelim:

```text
Password123!
```

İçerisinde:

* Büyük harf var
* Küçük harf var
* Rakam var
* Özel karakter var

Dolayısıyla yüzeysel bir complexity kontrolünden geçebilir.

Fakat parola yapısı oldukça tahmin edilebilirdir.

Bu yüzden projede entropy hesabını diğer kontrollerden bağımsız kullanmayacağım.

Entropy:

```text
Uzunluk
+
Karakter havuzu
+
Common password kontrolü
+
Pattern analizi
+
Password policy
```

ile birlikte değerlendirilecek.

Bu yaklaşımın amacı tek bir matematiksel değeri "parola güvenliği" olarak kabul etmemek.

---

# 7. Password Policy

Password policy, sistemin kabul edeceği parolalar için belirlediği güvenlik kurallarıdır.

Bu projede örnek olarak:

```text
Minimum uzunluk
Büyük harf zorunluluğu
Küçük harf zorunluluğu
Rakam zorunluluğu
Özel karakter zorunluluğu
Yaygın parola reddi
```

gibi kurallar kullanılabilir.

Buradaki amacım gerçek bir şirketin parola politikasını birebir kopyalamak değil.

Bir sistemin:

> "Bu parolayı neden kabul ediyorum veya neden reddediyorum?"

sorusuna teknik olarak cevap verebilmesini göstermek.

---

# 8. Güvenlik Skoru

Analizin sonunda kullanıcıya sadece:

```text
Güçlü
```

veya:

```text
Zayıf
```

demek yerine bir skor üretmek istiyorum.

Örneğin:

```text
0 - 39     Weak
40 - 69    Moderate
70 - 89    Strong
90 - 100   Very Strong
```

gibi bir model kullanılabilir.

Ancak burada önemli bir ayrım var.

Bu skor evrensel bir güvenlik standardı değildir.

Örneğin:

```text
91/100
```

alan bir parola için:

> "Bu parola kesinlikle kırılamaz."

diyemeyiz.

Bu skor yalnızca bizim oluşturduğumuz kriterlere göre yapılan değerlendirmeyi ifade eder.

Bu nedenle README'de ve programın çıktısında bu ayrımı açık tutacağım.

---

# 9. Neden Birden Fazla Kontrol Kullanıyoruz?

Bu projenin temel mantığı aslında burada ortaya çıkıyor.

Sadece uzunluğa bakarsak:

```text
aaaaaaaaaaaaaaaaaaaaaaaa
```

gibi bir parola güçlü görünebilir.

Sadece karakter çeşitliliğine bakarsak:

```text
Password123!
```

gibi bir parola güçlü görünebilir.

Sadece entropy hesabına bakarsak insan tarafından oluşturulmuş tahmin edilebilir kalıpları yeterince değerlendiremeyebiliriz.

Sadece common password listesine bakarsak listede bulunmayan zayıf parolaları kaçırabiliriz.

Bu yüzden farklı sinyalleri bir araya getiriyoruz.

```text
Length
   +
Character Analysis
   +
Common Password Check
   +
Pattern Analysis
   +
Entropy
   +
Password Policy
   ↓
Overall Assessment
```

Buradaki düşünceyi ileride yapacağımız diğer güvenlik araçlarında da kullanabiliriz:

> Güvenlik değerlendirmelerinde tek bir sinyale güvenmek yerine birden fazla göstergenin birlikte değerlendirilmesi daha anlamlıdır.

---

# 10. Proje Mimarisi

Başlangıçta proje yapımızı sade tutuyorum:

```text
password-strength-analyzer/
│
├── src/
│   └── analyzer.py
│
├── data/
│   └── common_passwords.txt
│
├── tests/
│
├── README.md
│
└── .gitignore
```

Kod büyüdükçe gerekli gördüğümüz yerleri ayıracağız.

Örneğin ileride:

```text
src/
├── analyzer.py
├── entropy.py
├── policy.py
└── report.py
```

gibi bir yapıya geçebiliriz.

Buradaki amaç sırf proje profesyonel görünsün diye onlarca dosya oluşturmak değil.

Her dosyanın belirli bir sorumluluğu olması.

Örneğin entropy hesaplayan bir fonksiyonun aynı zamanda terminal ekranını hazırlamasına gerek yok.

---

# 11. Ana Analiz Fonksiyonu

Şu anda ilk temel fonksiyonumuz:

```python
def analyze_password(password):
    pass
```

Bu fonksiyon projenin analiz merkezini oluşturacak.

Fakat bu fonksiyonun içerisine bütün kodu doldurmak istemiyorum.

İdeal olarak analiz süreci şu mantıkta ilerleyecek:

```text
password
    ↓
analyze
    ↓
individual checks
    ↓
analysis result
    ↓
score
    ↓
report
```

Böylece bir gün entropy hesaplama yöntemini değiştirmek istediğimde bütün programı değiştirmek zorunda kalmayacağım.

---

# 12. Test Yaklaşımı

Bu projede sadece programın çalışmasıyla yetinmeyeceğim.

`tests/` klasöründe farklı senaryoları test edeceğim.

Örneğin:

```text
Boş parola
Çok kısa parola
Sadece küçük harf
Sadece rakam
Yaygın parola
Tekrarlayan karakterler
Sıralı karakterler
Karışık karakter kümeleri
Uzun ve rastgele görünümlü parola
```

gibi durumları ayrı ayrı ele alacağım.

Bunun amacı sadece bug bulmak değil.

Asıl amaç yazdığım algoritmanın hangi girdide nasıl davranması gerektiğini açık şekilde tanımlamak.

---

# 13. Güvenlik ve Gizlilik

Bu araç bir parola analiz aracı olduğu için kendisinin yeni bir güvenlik problemi oluşturmaması gerekiyor.

Bu nedenle tasarımın temel prensiplerinden biri:

> Girilen parola mümkün olduğunca yerel olarak analiz edilecek ve dışarı gönderilmeyecek.

Program:

* Parola kırmaz.
* Brute-force saldırısı gerçekleştirmez.
* Dictionary attack çalıştırmaz.
* Girilen parolayı internet üzerindeki bir servise göndermez.
* Bir API'ye parola göndermeyi gerektirmez.

Bu proje eğitim ve parola güvenliği analizi amacıyla tasarlanmıştır.

---

# 14. Kullanım

Program tamamlandığında temel kullanım:

```bash
python src/analyzer.py
```

şeklinde olacak.

Örnek bir çıktı:

```text
========================================
        PASSWORD STRENGTH ANALYZER
========================================

Length          : 14
Lowercase       : Yes
Uppercase       : Yes
Digits          : Yes
Special Chars   : Yes
Common Password : No
Entropy         : 82.4 bits

Score           : 91/100
Rating          : VERY STRONG

========================================
```

Burada amaç sadece sonuç göstermek değil.

Kullanıcı mümkün olduğunca:

> "Neden bu sonucu aldım?"

sorusunun cevabını da görebilecek.

---

# 15. Geliştirme Planı

Projeyi tek seferde yazmak yerine aşamalı olarak geliştireceğim.

### Aşama 1 — Temel analiz

Önce:

* Parola uzunluğu
* Küçük harf
* Büyük harf
* Rakam
* Özel karakter

kontrollerini oluşturacağım.

### Aşama 2 — Common Password Detection

Yaygın parola listesini okuyup girilen parolayla karşılaştıracağım.

### Aşama 3 — Pattern Analysis

Tekrar ve basit tahmin edilebilir yapıları kontrol edeceğim.

### Aşama 4 — Entropy

Entropy hesabını matematiksel mantığıyla uygulayacağım.

### Aşama 5 — Password Policy

Belirlediğimiz güvenlik kurallarını ayrı bir değerlendirme katmanında ele alacağım.

### Aşama 6 — Scoring

Bütün analiz sonuçlarını anlamlı bir skora dönüştüreceğim.

### Aşama 7 — CLI

Programın terminal kullanımını daha düzgün hâle getireceğim.

### Aşama 8 — Tests

Farklı senaryolar için testler yazacağım.

### Aşama 9 — Documentation

README, kullanım örnekleri ve öğrendiğim konuları güncelleyeceğim.

---

# 16. Bu Projede Ne Öğrenmek İstiyorum?

Bu projeyi tamamladığımda sadece bir parola kontrol programına sahip olmak istemiyorum.

Şu konuları gerçekten anlamış olmak istiyorum:

* Python ile string analizi
* Karakter sınıflandırma
* Liste ve set kullanımı
* Dosya okuma
* CLI uygulaması geliştirme
* Entropy mantığı
* Parola politikaları
* Algoritma tasarımı
* Modüler kod yazımı
* Unit testing
* Git ve GitHub çalışma düzeni

Buradaki amaç bunları ayrı ayrı ezberlemek değil.

Hepsini aynı proje içerisinde kullanarak birbirleriyle nasıl bağlantılı olduklarını görmek.

---

# 17. Öğrendiklerim

Bu bölüm proje geliştikçe benim tarafımdan doldurulacak.

Özellikle şu sorulara cevap verebilmek istiyorum:

* Uzunluk parola güvenliğini neden etkiliyor?
* Karakter havuzu entropy hesabını nasıl değiştiriyor?
* Entropy ile gerçek parola tahmin edilebilirliği arasındaki fark nedir?
* Common password kontrolü neden gerekiyor?
* Complexity kuralları neden tek başına yeterli değil?
* İnsanların oluşturduğu parolalar neden matematiksel olarak rastgele görünen parolalardan farklı davranıyor?
* Bir güvenlik skoru nasıl tasarlanmalı?
* Bir güvenlik aracında neden birden fazla kontrol kullanılıyor?
* Kod neden modüler tasarlanmalı?
* Testler güvenlik araçlarında neden önemli?

---

# 18. Geliştirilebilecekler

İlk sürümde her şeyi yapmaya çalışmayacağım.

İleride ihtiyaç olursa:

* Daha gelişmiş pattern detection
* Daha büyük common password listeleri
* Daha ayrıntılı entropy analizi
* JSON çıktı desteği
* CLI argümanları
* Yapılandırılabilir parola politikaları
* Daha gelişmiş raporlama
* Daha kapsamlı testler

eklenebilir.

Ancak burada temel prensibim şu:

> Bir özellik sadece projede bulunması güzel göründüğü için eklenmeyecek.

Eklenen her özellik ya analiz kalitesine ya da projenin öğrenme değerine katkı sağlamalı.

---

# 19. Git Çalışma Düzeni

Bu projede Git'i sadece son hâli GitHub'a atmak için kullanmayacağım.

Geliştirme sürecini anlamlı commit'lerle takip edeceğim.

Örneğin:

```text
docs: add project documentation
feat: add password character analysis
feat: add common password detection
feat: add entropy calculation
feat: add password policy
feat: add password scoring
test: add analyzer test cases
refactor: separate analysis modules
docs: update usage examples
```

gibi commit mesajları kullanacağım.

Böylece repository'ye sonradan bakan biri sadece son kodu değil, projenin nasıl geliştirildiğini de görebilecek.

---

# 20. Sonuç

Bu proje dışarıdan bakıldığında küçük bir CLI uygulaması gibi görünüyor.

Fakat benim için asıl amaç bundan daha büyük.

Bir güvenlik problemini önce anlamak, sonra problemi parçalara ayırmak, uygun algoritmayı tasarlamak, bunu Python ile uygulamak, test etmek ve sonunda anlaşılır bir rapor hâline getirmek istiyorum.

Bu yüzden projeyi şu zincir üzerinden ilerletiyorum:

```text
Security Concept
       ↓
Problem Definition
       ↓
Algorithm
       ↓
Implementation
       ↓
Testing
       ↓
Reporting
       ↓
Documentation
```

Bu projeyi tamamladığımda elimde sadece çalışan bir Python scripti değil, neden o şekilde çalıştığını açıklayabildiğim bir güvenlik aracı olmasını hedefliyorum.

```