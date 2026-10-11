## Kesimpulan Kelompok

### 1. Hasil Pengujian

Pengujian Tugas 4 menunjukkan bahwa RPC dan Message Queue berhasil menjalankan komunikasi sesuai karakteristik
masing-masing. Pada jalur RPC, pemanggilan `cek_saldo("user1")` menghasilkan saldo 50.000 dengan waktu respons 2,04
detik. Setelah `proses_pembayaran("user1", 20000)` dijalankan, saldo berkurang menjadi 30.000. Waktu respons tersebut
termasuk jeda 2 detik yang sengaja ditambahkan pada server untuk memperlihatkan bahwa client menunggu balasan
(*blocking*), bukan sebagai ukuran performa RPC secara umum.

Pada jalur Message Queue, RabbitMQ dijalankan melalui Docker untuk menghubungkan Publisher dan Consumer. Saat Consumer
tidak aktif, Publisher dijalankan tiga kali dengan total 9 pesan. Dashboard RabbitMQ menunjukkan 9 pesan berstatus
*Ready*, 0 *Unacked*, dan 0 Consumer aktif. Setelah Consumer dinyalakan kembali, seluruh 9 notifikasi muncul pada
terminal. Pengujian ini membuktikan bahwa pesan tetap berada di antrean ketika Consumer tidak aktif dan diproses setelah
Consumer tersedia kembali (*asynchronous decoupling*).

### 2. Kesesuaian Pola Komunikasi

RPC sesuai untuk pengecekan saldo dan pembayaran karena modul Pesanan harus memperoleh keputusan secara langsung sebelum
transaksi dilanjutkan. Konsekuensinya, modul pemanggil ikut menunggu jika server Pembayaran lambat atau tidak merespons.
Sementara itu, Message Queue sesuai untuk notifikasi ke modul Kurir karena pengiriman event tidak harus menunggu
Consumer memprosesnya. Jika RPC digunakan untuk notifikasi, waktu respons pembayaran akan bergantung pada modul Kurir;
jika antrean asinkron digunakan untuk pengecekan saldo, diperlukan mekanisme tambahan untuk menerima dan mencocokkan
hasil transaksi.

### 3. Batasan dan Evaluasi

Simulasi saat ini masih menjalankan proses pembayaran RPC dan pengiriman pesan RabbitMQ secara terpisah. Publisher
membuat event contoh tanpa mengambil hasil transaksi dari server RPC, sehingga keberhasilan notifikasi belum membuktikan
keterhubungan seluruh alur pembayaran FoodGo. Consumer juga baru menampilkan notifikasi, belum mencatat penugasan kurir.
Selain itu, pengujian belum mencakup restart RabbitMQ, kegagalan koneksi broker, penanganan pesan rusak, maupun
pencegahan pembayaran atau pemrosesan pesan berulang.

Dengan demikian, kedua pendekatan telah memenuhi tujuan pengujian dasar: RPC memperlihatkan komunikasi sinkron yang
menunggu respons, sedangkan RabbitMQ memperlihatkan komunikasi asinkron dengan penyimpanan pesan saat Consumer tidak
aktif. Untuk diterapkan pada alur transaksi nyata, masih diperlukan integrasi antar modul, identitas transaksi,
pencegahan pemrosesan ganda, serta penanganan kegagalan yang lebih lengkap.