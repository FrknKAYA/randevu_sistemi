# Randevu Sistemi

Berberler için özel olarak geliştirilen bu proje, randevu yönetimini otomatikleştirerek zaman ve kaynak tasarrufu sağlar. Projeye katkıda bulunmanızı önemle rica ederim. 

## Özellikler

- [ ] Birden fazla Dükkan oluşturulup dükkana ait berberler eklenebiliyor.
- [ ] Dükkan sahibi istediği berberin randevu listesini görüp istediği tarih ve saate randevu kaydedebiliyor.
- [ ] Dükkan sahibi berberleri istediği zaman aktif/pasif duruma çekebiliyor. Pasif durumdaki berber hesabına giriş yapamıyor.
- [ ] Dükkanın açılış ve kapanış saatleri ve çalışma günleri baz alınarak randevu listesi gün gün listeleniyor.

## Ekran Görüntüleri

![Uygulama Ekran Görüntüsü](https://s5.ezgif.com/tmp/ezgif-5-d7779f1397.gif)

## Kurulum

Projenizi yerel ortamda çalıştırmak için izlenmesi gereken adımlar.
- UYARI: Yeni bir Kullanıcı oluşturduktan sonra admin panele superuser bilgileri ile girip oluşturduğunuz kullanıcıyı aktif etmek zorundasınız. Aksi taktirde hesaba giriş yapamazsınız.

1. **Proje deposunu klonlayın:**
   ```bash
   git clone https://github.com/FrknKAYA/randevu_sistemi.git

2. **Sanal Ortam Oluşturma**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. **Veritabanı Migrasyonu**
   ```bash
   python manage.py migrate

4. **Superuser Oluşturma**
   ```bash
   python manage.py createsuperuser

5. **Sunucuyu Başlatma**
   ```bash
   python manage.py runserver

## Katkıda Bulunma
  ```bash
  Depoyu forklayın.
  Yeni bir dal oluşturun: git checkout -b yeni-özellik
  Değişikliklerinizi yapın: git commit -m 'Yeni bir özellik ekle'
  Dalı gönderin: git push origin yeni-özellik
  Bir pull request oluşturun.
