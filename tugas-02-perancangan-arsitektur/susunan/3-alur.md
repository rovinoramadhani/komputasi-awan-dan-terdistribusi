## Alur Skenario Serta Jenis Komunikasi

1. Pelanggan memvalidasi sesi masuk pada Modul Autentikasi secara sinkron.
2. Pelanggan menekan tombol pesan pada Modul Pesanan secara sinkron.
3. Modul Pesanan memanggil Modul Pembayaran secara sinkron untuk memverifikasi transaksi.
4. Modul Pesanan mempublikasikan status pesanan sukses ke Message Broker secara asinkron.
5. Modul Katalog Resto membaca status dari Message Broker secara asinkron untuk memulai proses masak.
6. Modul Notifikasi membaca status dari Message Broker secara asinkron untuk mencari pengemudi.
7. Modul Realtime memanggil Modul Lokasi secara sinkron untuk menampilkan pergerakan titik koordinat pengemudi.