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
4. Bebas Menggunakan Teknologi yang Berbeda: Dengan memisahkan modul menjadi 7 memungkinkan setiap tim pengembang memilih bahasa pemrograman sesuai kebutuhan dari modul yang ingin dikembangkan. Misalnya, Modul Lokasi menggunakan bahasa C++ agar perhitungan koordinat GPS berjalan lebih cepat atau Modul Autentikasi menggunakan Java untuk standar keamanan yang tinggi.

### Penyelesaian Trade Off

1. Kompleksitas Infrastruktur: Arsitektur kombinasi mewajibkan pengelolaan 7 komponen secara terpisah beserta perawatan
   infrastruktur Message Broker. Kondisi ini meningkatkan beban operasional pemantauan server secara drastis
   dibandingkan dengan aplikasi monolitik.
2. Konsistensi Data: Penggunaan gaya Publish-Subscribe menghasilkan sifat eventual consistency. Terdapat jeda waktu
   antara status keberhasilan pada Modul Pesanan dengan pembaruan status ketersediaan pada Modul Katalog Resto.
3. Kesulitan Debugging: Alur eksekusi pesan berjalan secara tidak linear. Masalah kegagalan pesanan mewajibkan teknisi
   untuk membaca log pada banyak server yang berbeda secara bersamaan untuk menemukan titik pasti berhentinya aliran
   data.
4. Risiko Modul Tertahan (Stuck/Hang) pada RPC Sinkron: Ada dua jalur penting yang menggunakan RPC Sinkron, yaitu antara "Modul Pesanan ke Pembayaran" dan "Modul Realtime ke Lokasi". Jika Modul Pembayaran atau Lokasi merespons dengan lambat maka modul pengirimnya bisa ikut tertahan (stuck) menunggu.