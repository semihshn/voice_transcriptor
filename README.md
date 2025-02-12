# Ses Transkripsiyon Uygulaması

Bu proje, mikrofon aracılığıyla ses kaydı alıp, Hugging Face Whisper modeli kullanarak transkripsiyon yapan bir Python uygulamasıdır. Uygulama, kullanıcının "q" tuşu ile kaydı durdurmasına olanak tanır, alınan ses verisini WAV dosyası olarak kaydeder ve transkripsiyonu hem konsolda gösterir hem de `transcription.txt` dosyasına ekler. Konsol çıktıları, [Rich](https://rich.readthedocs.io/en/stable/) kütüphanesi kullanılarak kullanıcı dostu hale getirilmiştir.

> **Önemli:** Bu projede, modelin çalışması için PyTorch yerine **TensorFlow** kullanılmaktadır. Dolayısıyla gereksinim listesinde `tensorflow` paketi yer almaktadır.

---

## Özellikler

- **Interaktif Ses Kaydı:**  
  Kaydı başlatmak için Enter tuşuna basın, kaydı durdurmak için "q" tuşuna basın.

- **Ses Kaydı Dosyası:**  
  Kaydedilen ses verisi, `recorded_audio.wav` dosyası olarak saklanır.

- **Transkripsiyon:**  
  Hugging Face’in Whisper modeli kullanılarak alınan ses dosyası metne dönüştürülür.

- **Kullanıcı Dostu Konsol Çıktıları:**  
  [Rich](https://rich.readthedocs.io/en/stable/) kütüphanesi ile stilize edilmiş paneller, renkli mesajlar ve interaktif promptlar kullanılır.

- **Sürekli Kullanım:**  
  Her kayıttan sonra kullanıcıya yeni kayıt yapıp yapmayacağını sorar; varsayılan cevap "y"dir.

---

## Gereksinimler

- **Python:** 3.8 veya daha yeni bir sürüm (özellikle Python 3.10 önerilir)
- **pip:** Python paket yöneticisi

### Gerekli Python Paketleri

Bu projede aşağıdaki kütüphaneler kullanılmaktadır:

- `numpy`
- `sounddevice`
- `pynput`
- `transformers`
- `rich`
- `tensorflow`

Projeyi çalıştırmadan önce bu kütüphaneleri yüklemeniz gerekmektedir. Bunun için `requirements.txt` dosyasını kullanabilirsiniz.

---

## Kurulum Adımları

Bu projeyi sıfırdan çalıştırmak isteyenler için adım adım yapılması gerekenler aşağıdadır:

1. **Repo'yu Klonlayın / İndirin:**  
   Proje dosyalarını bilgisayarınıza indirin veya repoyu klonlayın.

2. **Virtual Environment Oluşturun:**  
   Terminali açın ve proje dizinine gidin. Aşağıdaki komutla sanal ortam oluşturun:
   ```bash
   python3 -m venv .venv

3. **Virtual Environment'ı Aktif Edin:**
   Oluşturduğunuz sanal ortamı şu komut ile aktif edin:
   ```bash
   source .venv/bin/activate
(Windows kullanıyorsanız .\.venv\Scripts\activate komutunu kullanabilirsiniz.)

4. **Python 3.10 Yüklemesi (macOS için):**  
   Eğer macOS kullanıyorsanız ve sisteminizde uygun bir Python sürümü yoksa, Homebrew üzerinden Python 3.10 yükleyebilirsiniz:
   ```bash
   brew install python@3.10

5. **Mimari Kontrolü (Apple Silicon için):**
   Projenin ARM64 mimaride çalıştığından emin olmak isterseniz aşağıdaki komutları çalıştırın:
    ```bash
   python3 -c "import platform; print(platform.machine())"

   ve

    uname -m

Her iki komut da arm64 çıktısı vermelidir. Özellikle Apple Silicon (M1/M2) cihazlarda doğru mimaride çalıştığınız bu şekilde doğrulanır.

6. **Gerekli Paketleri Yükleyin:**  
   Proje dizininde bulunan requirements.txt dosyasını kullanarak gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   
7. **Uygulamayı Çalıştırın:**
Terminalde aşağıdaki komutu kullanarak uygulamayı başlatın (dosya adını kendi script adınıza göre değiştirebilirsiniz):
    ```bash
    python meeting-transcriptor.py

## Kullanım

### Uygulamayı Başlatma:
Terminalde scripti çalıştırdığınızda, "Ses Transkripsiyon Uygulamasına Hoşgeldiniz!" mesajı görüntülenecektir.

### Kayda Başlama:
Kayıt yapmak için Enter tuşuna basın. Kayıt başladıktan sonra, kaydı durdurmak için "q" tuşuna basın.

### Transkripsiyon:
Kayıt durduktan sonra, ses dosyası `recorded_audio.wav` olarak kaydedilir ve model (Whisper) otomatik olarak transkripsiyon yapar. Sonuç, konsolda görüntülenecek ve `transcription.txt` dosyasına eklenmiş olacaktır.

### Yeni Kayıt:
Uygulama, "Yeni bir kayıt yapmak ister misiniz? (y/n)" diye soracaktır.

- Varsayılan cevap "y" olduğundan, sadece Enter'a basarsanız yeni kayıt başlatılır.
- "n" girerseniz, uygulama kapanır.

### Notlar:
- macOS ortamında "This process is not trusted! Input event monitoring will not be possible until it is added to accessibility clients." uyarısı alabilirsiniz. Bu, sistem erişilebilirlik izinleriyle ilgilidir ve uygulamanın çalışmasını etkilemez. Uyarının görünmemesini istiyorsanız, Terminal veya kullandığınız IDE'yi Erişilebilirlik listesine eklemeniz gerekebilir.