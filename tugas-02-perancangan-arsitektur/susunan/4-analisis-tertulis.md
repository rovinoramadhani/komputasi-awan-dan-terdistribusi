## Analisis Tertulis

### Penyelesaian Masalah

1. Penyelesaian Masalah Coupling: Arsitektur ini membebaskan Modul Pesanan dari proses tunggu. Modul Pesanan memberikan
   respons sukses kepada pengguna setelah pembayaran selesai, tanpa memiliki kewajiban menunggu proses pencarian kurir
   dari Modul Notifikasi berkat penggunaan Message Broker.
2. Isolasi Kegagalan Server: Message Broker bertindak sebagai penampung pesan sementara. Apabila server Modul Katalog
   Resto mengalami crash, data pesanan tidak hilang melainkan tertahan di antrean Message Broker hingga server Modul
   Katalog Resto hidup kembali dan siap memproses data.
3. Penskalaan Independen: Arsitektur terdistribusi memberikan kapasitas penskalaan spesifik untuk setiap komponen.
   Lonjakan permintaan pemantauan rute kurir mewajibkan penambahan server hanya untuk Modul Realtime dan Modul Lokasi,
   tanpa menyita memori atau CPU pada server Modul Pesanan.

### Penyelesaian Trade Off

1. Kompleksitas Infrastruktur: Arsitektur kombinasi mewajibkan pengelolaan 7 komponen secara terpisah beserta perawatan
   infrastruktur Message Broker. Kondisi ini meningkatkan beban operasional pemantauan server secara drastis
   dibandingkan dengan aplikasi monolitik.
2. Konsistensi Data: Penggunaan gaya Publish-Subscribe menghasilkan sifat eventual consistency. Terdapat jeda waktu
   antara status keberhasilan pada Modul Pesanan dengan pembaruan status ketersediaan pada Modul Katalog Resto.
3. Kesulitan Debugging: Alur eksekusi pesan berjalan secara tidak linear. Masalah kegagalan pesanan mewajibkan teknisi
   untuk membaca log pada banyak server yang berbeda secara bersamaan untuk menemukan titik pasti berhentinya aliran
   data.
4. Risiko Kehilangan Data: Aplikasi menyimpan draf secara otomatis setiap kali pengguna mengubah data, sebelum tombol
   submit ditekan. Draf disimpan di penyimpanan lokal browser dan dimuat kembali saat aplikasi dibuka setelah browser
   mengalami crash, sehingga pengguna tidak perlu mengisi ulang seluruh formulir.
5. Beban Komputasi Berpindah ke Pengguna: Aplikasi memeriksa kemampuan perangkat sebelum memproses data besar. Jika
   perangkat memiliki sumber daya terbatas, pemrosesan dialihkan ke server agar antarmuka tetap responsif dan penggunaan
   CPU serta baterai pada smartphone tidak meningkat secara berlebihan.
6. Fleksibilitas Pengguna: Batas ukuran file ditampilkan sebelum pengguna memilih berkas. Untuk berkas yang melebihi
   batas, aplikasi menawarkan kompresi otomatis atau unggah bertahap, sehingga pengguna tetap dapat mengirim berkas
   tanpa harus menyederhanakannya sendiri terlebih dahulu.