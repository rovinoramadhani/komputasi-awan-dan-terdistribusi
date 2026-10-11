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

