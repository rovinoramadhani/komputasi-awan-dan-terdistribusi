# Tugas 4 (Pekan 4) - RPC Message Queue

**Kelompok:** Kelompok 2

| **Nama**                | **NIM**      | **Kontribusi** |
|-------------------------|--------------|----------------|
| Rovino Ramadhani        | 103072400031 |                |
| Galang Herjuno Mulya    | 103072430006 |                |
| Erastus Liubeta Septian | 103072400020 |                |
## Analisis - ditulis oleh Rovino Ramadhani

### 1. Analisis Komunikasi RPC (Sinkron)

Pada jalur RPC, modul Pesanan berkomunikasi langsung dengan modul Pembayaran melalui pemanggilan fungsi `cek_saldo` dan
`proses_pembayaran`. Pengujian menunjukkan bahwa `cek_saldo("user1")` mengembalikan saldo **50.000** dengan waktu
respons **2,04 detik**. Setelah pembayaran sebesar **20.000** diproses, server mengembalikan status `sukses` dan saldo
akhir **30.000**.

Waktu tunggu tersebut menjadi bukti sifat sinkron (blocking): modul Pesanan harus menunggu hasil dari modul
Pembayaran sebelum melanjutkan proses. Pola ini tepat untuk pengecekan saldo dan pembayaran karena hasil transaksi
dibutuhkan langsung untuk menentukan langkah berikutnya. Namun, ketergantungan terhadap respons server juga menjadi
kekurangan RPC. Jika server Pembayaran lambat atau tidak merespons, proses pada modul Pesanan ikut tertahan.

**Bukti pengujian:** `bukti/rpc.png`

### 2. Analisis Message Queue Saat Consumer Aktif

Pada jalur Message Queue, modul Pembayaran bertindak sebagai *Publisher*, sedangkan modul Kurir/Notifikasi bertindak
sebagai *Consumer*. RabbitMQ dijalankan melalui Docker sebagai perantara komunikasi. Saat Consumer aktif, Publisher
mengirimkan 3 event pembayaran, masing-masing untuk `user1`, `user2`, dan `user3`, dengan nominal **20.000**,
**40.000**, dan **60.000**. Ketiga event tersebut diterima dan diproses oleh Consumer.

Hasil ini memperlihatkan bahwa Publisher cukup mengirimkan event ke antrean tanpa harus memanggil modul Kurir secara
langsung. Dengan pemisahan tersebut, proses pengiriman notifikasi tidak perlu dijadikan bagian dari respons langsung
modul Pembayaran.

**Bukti pengujian:** `bukti/mq.docker.png` dan `bukti/mq.kondisi_consumer_aktif.png`

### 3. Analisis *Asynchronous Decoupling* Saat Consumer Tidak Aktif

Pengujian berikutnya dilakukan dengan menghentikan Consumer, kemudian menjalankan Publisher sebanyak **3 kali**. Setiap
eksekusi mengirimkan 3 event sehingga total terdapat 9 pesan. Dashboard RabbitMQ menunjukkan Ready: 9,
Unacked: 0, dan Consumers: 0. Artinya, tidak ada Consumer yang aktif, tetapi seluruh pesan tetap berada dalam
antrean dan siap dikirim ketika Consumer tersedia.

Setelah Consumer dijalankan kembali, terminal menampilkan **9 notifikasi** yang diproses. Hasil ini membuktikan
*asynchronous decoupling*: Publisher tetap dapat mengirimkan pesan ketika Consumer tidak aktif, sementara RabbitMQ
menahan pesan untuk diproses kemudian. Implementasi juga menggunakan antrean `durable=True`, pesan persisten, serta
*manual acknowledgement* setelah pemrosesan.

Bukti tersebut berlaku untuk skenario **Consumer dimatikan lalu diaktifkan kembali**. Ketahanan pesan terhadap *restart*
RabbitMQ sendiri belum diuji dalam dokumentasi ini.

**Bukti pengujian:** `bukti/mq.kondisi_asynchronous_decoupling_1.png`,
`bukti/mq.kondisi_asynchronous_decoupling_dashboard_rabbitMQ.png`, dan `bukti/mq.kondisi_asynchronous_decoupling_2.png`

### 4. Analisis Pemilihan Pola Komunikasi

1. RPC untuk pengecekan saldo dan proses pembayaran. Kedua operasi membutuhkan jawaban langsung agar modul Pesanan
   mengetahui apakah pembayaran dapat dilanjutkan atau harus ditolak. Keuntungannya adalah alur permintaan dan respons
   jelas; kekurangannya adalah proses menunggu ketersediaan server.
2. Message Queue untuk notifikasi keberhasilan pembayaran. Notifikasi tidak harus selesai pada saat transaksi
   dilakukan. Keuntungannya adalah modul Pembayaran tidak bergantung pada kondisi modul Kurir ketika mengirimkan event;
   konsekuensinya adalah notifikasi diproses secara tertunda jika antrean menumpuk atau Consumer tidak aktif.
3. Risiko jika pola digunakan tidak sesuai kebutuhan. RPC untuk notifikasi membuat modul Pembayaran ikut menunggu
   modul Kurir. Sebaliknya, Message Queue untuk pengecekan saldo memerlukan mekanisme tambahan untuk menghubungkan
   permintaan dengan balasan, sehingga alurnya lebih rumit untuk kebutuhan respons langsung.

### 5. Kesimpulan

Pengujian menunjukkan bahwa **RPC berhasil menjalankan komunikasi sinkron** dengan waktu tunggu terukur **2,04 detik**,
sedangkan **Message Queue berhasil mempertahankan 9 pesan** saat Consumer tidak aktif dan memprosesnya setelah Consumer
kembali berjalan. Karena itu, pemisahan RPC untuk operasi yang membutuhkan respons langsung dan Message Queue untuk
notifikasi asinkron merupakan pilihan yang sesuai dengan kebutuhan komunikasi antar modul FoodGo.

---

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

## Analisis - ditulis oleh Erastus Liubeta Septian

### 1. Analisis jalur A: Kapan RPC (Singkron) Cocok Digunakan?
Pendekatan Remote Procedur Call (RPC) yang bersifat sinkron sangat pas diterapkan untuk sistem inti seperti model pembayaran, di mana hasil sebelum proses harus segera diketahui saat itu juga.

- Kenapa RPC sesuai untuk studi kasus ini, karena dalam skenario pembayaran aplikasi klien membutuhkan kepastian secara instan, apakah saldo pengguna cukup dan apakah transaksi berhasil dikurangi dari saldo rekening. Proses ini menuntut respons langsung yang cepat. Klien harus menunggu sampai server selesai memvalidasi dan memotong saldo. Jika pembayaran gagal sistem harus langsung tahu agar proses setelahnya bisa dibatalkan.

- Apa resiko jika salah penempatan seprti Message Queue dipakai untuk pemabyaran. jika pengecekan saldo dan pembayaran menggunakan antrean asingkron, sistem pemesanan mungkin sudah menganggap transaksi selesai dan barang dikirim, padahal beberapa menit kemudian baru diketahui bahwa saldo pengguna ternyata tidak cukup atau kurang. Hal seperti ini bisa memicu kerugian karena tidak langsung di validasi secara instan.

### 2. Analisis Jalur B: Kapan Message Queue (Asinkron) Lebih Tepat?
Pendekatan Sistem Message Queue (MQ) seperti RabbitMQ sangat ideal untuk skenario notifikasi atau penugasan kurir di mana proses tidak memerlukan respons seketika dan bisa dikerjakan di latar belakang.

-  Alasan mengapa MQ cocok untuk skenrio tresebut adalah pada saat modul pembayaran berhasil memotong saldo, tugas sebenarnya sudah selesai, Pengiriman notifikasi ke kurir atau email pengguna hanyalah pekerjaan tambahan. Dengan membagi tugas ini lewat antrean RabbitMQ, sehingga modul pembayaran tidak lagi perlu menggangu kurir setiap menerima data. Modul pembayaran bisa langsung kembali melayanai transaksi lain. Pesanan akan tersimpan aman di antrean dan baru diprses oleh modul kurir kapan pun modul tersebut siap.

- Apa risiko jika salah penempatan seperti RPC dipakai untuk notifikasi kurir. Jika kita menggunakan pattern RPC yang sinkron untuk mengirim notifikasi ke kurir, sistem akan bermasalah. Modul pembayaran harus menuggu sampai modul kurir selesai mencatat data. Jika server kurir sedang bermasalah atau down, yang menyebabkan seluruh modul pembayaran akan ikut terhenti. Pengguna akan melihat layar loading yang sangat lama hanya karena sistem sedang kesulitan menghubungi kurir, padahal pembayaran sendiri sudah sukses. Hal ini jelas saja menurunkan performa dan kenyamanan customer secara keseluruhan.
## Kesimpulan Kelompok

