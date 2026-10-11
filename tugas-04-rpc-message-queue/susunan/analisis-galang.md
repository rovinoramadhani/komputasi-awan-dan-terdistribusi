
---

## Analisis - Galang Herjuno Mulya

### 1. Hubungan antara Pembayaran dan Notifikasi

Pada simulasi FoodGo, RPC digunakan untuk mengecek saldo dan memproses pembayaran karena modul Pesanan membutuhkan hasilnya secara langsung. Message Queue digunakan untuk mengirim notifikasi agar modul Pembayaran tidak perlu menunggu modul Kurir. Kedua cara komunikasi ini sudah berjalan, tetapi programnya masih dijalankan secara terpisah.

Dalam `rpc/server.py`, fungsi `proses_pembayaran` hanya mengurangi saldo dan mengembalikan status pembayaran. Fungsi tersebut belum mengirim pesan ke RabbitMQ. Sementara itu, `mq/publisher.py` membuat pesan pembayaran melalui perulangan tanpa memeriksa hasil dari RPC. Artinya, notifikasi yang diterima Consumer belum berasal dari proses pembayaran yang sama dengan pengujian RPC.

Hal ini terlihat pada pesan untuk `user3` sebesar 60.000. Data saldo pada server RPC hanya berisi `user1` dan `user2`, tetapi Publisher tetap membuat pesan untuk `user3`. Pesan tersebut digunakan untuk simulasi MQ dan belum membuktikan bahwa pembayaran `user3` berhasil. Pada sistem FoodGo, notifikasi pembayaran seharusnya sesuai dengan transaksi dan pesanan yang telah berhasil diproses.

Jika kedua jalur dihubungkan, ada kemungkinan pembayaran berhasil tetapi pengiriman notifikasi gagal. Akibatnya, saldo pengguna sudah berkurang, sementara kurir belum menerima informasi pesanan. Program saat ini belum mencatat hubungan antara pembayaran dan pengiriman notifikasi. Karena itu, keberhasilan RPC dan MQ secara terpisah belum cukup untuk menunjukkan bahwa seluruh alur pembayaran sampai penugasan kurir berjalan dengan baik.

### 2. Waktu Tunggu dan Risiko Pembayaran Berulang pada RPC

Hasil pengujian menunjukkan bahwa client membutuhkan waktu 2,04 detik untuk mendapatkan saldo. Selama waktu tersebut, client menunggu balasan server sebelum melanjutkan proses. Namun, server memang diberi jeda dua detik melalui `time.sleep(2)`. Jadi, angka 2,04 detik menunjukkan bahwa client menunggu respons, tetapi belum dapat digunakan untuk menilai kecepatan RPC secara umum. Waktu proses pembayaran juga belum diukur dalam pengujian tersebut.

RPC membantu modul Pesanan mengetahui apakah pembayaran berhasil atau gagal. Masalah dapat muncul jika server sudah mengurangi saldo, tetapi balasannya tidak sampai ke client. Pada kondisi ini, client tidak mengetahui hasil pembayaran. Balasan yang tidak diterima belum tentu berarti transaksi gagal, sebab saldo mungkin sudah dipotong sebelum koneksi bermasalah.

Jika client mengirim ulang permintaan yang sama, saldo dapat terpotong lagi. Fungsi `proses_pembayaran` belum memiliki nomor transaksi untuk membedakan permintaan baru dengan permintaan yang diulang. Dari alur kode, dua pembayaran sebesar 20.000 untuk `user1` yang memiliki saldo awal 50.000 akan menyisakan saldo 10.000. Hal ini merupakan hasil pembacaan kode, bukan hasil pengujian yang dicatat dalam jurnal. Jika kedua permintaan tersebut sebenarnya untuk satu pesanan, pengguna dapat dikenai pembayaran dua kali.

Server sudah memeriksa pengguna yang tidak terdaftar, jumlah pembayaran nol atau negatif, dan saldo yang tidak cukup. Akan tetapi, jurnal baru mencatat hasil pembayaran yang berhasil. Selain itu, fungsi `cek_saldo` memberikan nilai nol saat pengguna tidak ditemukan. Hasil ini sama dengan pengguna yang memang memiliki saldo nol, sehingga modul Pesanan belum mendapatkan keterangan yang jelas mengenai kedua kondisi tersebut.

### 3. Batas Hasil Pengujian Message Queue

Dashboard RabbitMQ menunjukkan Ready: 9, Unacked: 0, dan Consumers: 0 ketika Consumer tidak aktif. Data ini berarti ada sembilan pesan yang menunggu di antrean. Setelah Consumer dijalankan kembali, sembilan notifikasi muncul di terminal. Hasil tersebut menunjukkan bahwa Publisher dapat mengirim pesan meskipun Consumer belum siap menerimanya.

Namun, proses pada `mq/consumer.py` masih sebatas menampilkan notifikasi di terminal, lalu mengirim tanda bahwa pesan selesai diproses melalui `basic_ack`. Program belum menyimpan notifikasi atau mencatat penugasan kurir. Dengan demikian, pengujian sudah menunjukkan bahwa pesan diterima, tetapi belum menunjukkan bahwa kurir benar-benar mendapat tugas pengiriman.

Risiko lain dapat muncul jika Consumer berhenti setelah melakukan suatu pekerjaan, tetapi belum mengirim tanda selesai ke RabbitMQ. Jika pesan tersebut diterima kembali, pekerjaan yang sama bisa dilakukan lagi. Isi pesan saat ini hanya mencakup `user_id`, `jumlah`, dan `timestamp`. Belum ada nomor pesan atau nomor transaksi yang digunakan untuk memeriksa apakah pesan sudah pernah diproses. Jika nantinya Consumer digunakan untuk menugaskan kurir, kondisi ini dapat menyebabkan satu pesanan diproses lebih dari sekali.

Sembilan pesan dalam jurnal berasal dari Publisher yang dijalankan tiga kali, dengan tiga pesan pada setiap proses. Jumlah ini menunjukkan bahwa seluruh pesan yang dikirim dapat diterima setelah Consumer aktif kembali. Hasil tersebut belum membuktikan bahwa sistem dapat mencegah pemrosesan berulang ketika terjadi gangguan.

Consumer juga belum menangani kesalahan pada isi pesan. Program langsung membaca JSON dan mengambil data pengguna serta jumlah pembayaran. Jika format JSON salah atau data yang dibutuhkan tidak tersedia, proses dapat mengalami error sebelum mengirim tanda selesai. Oleh sebab itu, keberhasilan komunikasi juga bergantung pada isi pesan yang benar dan kemampuan Consumer menangani kesalahan.

### 4. Peran RabbitMQ dan Penumpukan Pesan

Message Queue memungkinkan modul Pembayaran mengirim notifikasi tanpa menunggu modul Kurir. Meskipun demikian, Publisher tetap membutuhkan RabbitMQ sebagai perantara. Jika RabbitMQ tidak dapat dihubungi, pengiriman pesan tetap dapat gagal. Jadi, tidak aktifnya Consumer dapat ditangani melalui antrean, tetapi masalah pada RabbitMQ masih dapat mengganggu pengiriman.

Publisher belum memiliki penanganan saat koneksi gagal dan belum meminta konfirmasi dari RabbitMQ bahwa pesan telah diterima oleh broker. Karena itu, tulisan `Event sent` di terminal saja belum cukup untuk memastikan pesan tersimpan ketika terjadi gangguan. Dalam simulasi ini, bukti penyimpanan pesan diperoleh dari dashboard RabbitMQ. Pengujian juga belum mencakup kondisi RabbitMQ dimulai ulang.

Penumpukan pesan dapat terjadi jika Publisher mengirim pesan lebih cepat daripada Consumer memprosesnya. Semakin banyak pesan yang menunggu, semakin lama pula notifikasi diterima oleh kurir. Pengaturan `prefetch_count=1` membatasi pesan yang belum dikonfirmasi selesai pada Consumer menjadi satu pesan, tetapi hasil simulasi belum menunjukkan kemampuan Consumer dalam menangani antrean yang lebih besar.

Pada FoodGo, keterlambatan notifikasi dapat menunda penugasan kurir. Pembayaran memang dapat selesai tanpa menunggu notifikasi diproses, tetapi pengiriman makanan tetap membutuhkan informasi yang diterima tepat waktu. Oleh karena itu, kemampuan menyimpan pesan perlu diperhatikan bersama kecepatan Consumer dalam menyelesaikan antrean.

### 5. Kesimpulan

RPC dan Message Queue sudah sesuai dengan kebutuhan dasar komunikasi pada FoodGo. RPC digunakan ketika modul Pesanan membutuhkan hasil pembayaran secara langsung, sedangkan Message Queue digunakan untuk notifikasi yang dapat diproses kemudian. Hal ini terlihat dari client yang menunggu respons selama 2,04 detik dan sembilan pesan yang tetap tersimpan saat Consumer tidak aktif.

Meski demikian, masih ada beberapa keterbatasan pada simulasi. Proses pembayaran dan pengiriman notifikasi belum terhubung, permintaan pembayaran yang diulang dapat kembali mengurangi saldo, dan penerimaan pesan belum disertai pencatatan penugasan kurir. Pengiriman melalui MQ juga tetap bergantung pada RabbitMQ, isi pesan yang benar, dan kecepatan Consumer. Dengan demikian, kedua pola komunikasi sudah menjalankan fungsi dasarnya, tetapi hasil pengujian belum menunjukkan bahwa seluruh proses FoodGo dapat menangani gangguan tanpa menimbulkan masalah transaksi.
