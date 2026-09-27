## Alur Skenario Serta Jenis Komunikasi

1. Pengguna melakukan login dan memvalidasi sesi melalui Modul Autentikasi menggunakan komunikasi sinkron berupa HTTP
   request dan response.
2. Pengguna mengirimkan permintaan pembuatan pesanan menuju Modul Pesanan menggunakan protokol HTTP dengan komunikasi
   sinkron.
3. Modul Pesanan mengeksekusi Remote Procedure Call (RPC) ke Modul Pembayaran dengan komunikasi sinkron untuk
   memvalidasi transaksi secara langsung.
4. Modul Pesanan bertindak sebagai publisher untuk mengirimkan event berisi data pesanan sukses ke dalam Message Broker
   menggunakan komunikasi asinkron.
5. Modul Katalog Resto bertindak sebagai subscriber pada Message Broker untuk membaca event secara asinkron, lalu
   memulai instruksi pengurangan stok ke restoran.
6. Modul Notifikasi bertindak sebagai subscriber pada Message Broker untuk membaca event secara asinkron, lalu memicu
   pencarian kurir terdekat.
7. Modul Realtime memanggil Modul Lokasi menggunakan komunikasi sinkron untuk menarik data koordinat, kemudian
   meneruskannya ke antarmuka aplikasi pengguna.