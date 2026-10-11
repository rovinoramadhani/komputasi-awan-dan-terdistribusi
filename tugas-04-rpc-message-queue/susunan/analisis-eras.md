## Analisis - ditulis oleh Erastus Liubeta Septian

### 1. Analisis jalur A: Kapan RPC (Singkron) Cocok Digunakan?
Pendekatan Remote Procedur Call (RPC) yang bersifat sinkron sangat pas diterapkan untuk sistem inti seperti model pembayaran, di mana hasil sebelum proses harus segera diketahui saat itu juga.

- Kenapa RPC sesuai untuk studi kasus ini, karena dalam skenario pembayaran aplikasi klien membutuhkan kepastian secara instan, apakah saldo pengguna cukup dan apakah transaksi berhasil dikurangi dari saldo rekening. Proses ini menuntut respons langsung yang cepat. Klien harus menunggu sampai server selesai memvalidasi dan memotong saldo. Jika pembayaran gagal sistem harus langsung tahu agar proses setelahnya bisa dibatalkan.

- Apa resiko jika salah penempatan seprti Message Queue dipakai untuk pemabyaran. jika pengecekan saldo dan pembayaran menggunakan antrean asingkron, sistem pemesanan mungkin sudah menganggap transaksi selesai dan barang dikirim, padahal beberapa menit kemudian baru diketahui bahwa saldo pengguna ternyata tidak cukup atau kurang. Hal seperti ini bisa memicu kerugian karena tidak langsung di validasi secara instan.

### 2. Analisis Jalur B: Kapan Message Queue (Asinkron) Lebih Tepat?
Pendekatan Sistem Message Queue (MQ) seperti RabbitMQ sangat ideal untuk skenario notifikasi atau penugasan kurir di mana proses tidak memerlukan respons seketika dan bisa dikerjakan di latar belakang.

-  Alasan mengapa MQ cocok untuk skenrio tresebut adalah pada saat modul pembayaran berhasil memotong saldo, tugas sebenarnya sudah selesai, Pengiriman notifikasi ke kurir atau email pengguna hanyalah pekerjaan tambahan. Dengan membagi tugas ini lewat antrean RabbitMQ, sehingga modul pembayaran tidak lagi perlu menggangu kurir setiap menerima data. Modul pembayaran bisa langsung kembali melayanai transaksi lain. Pesanan akan tersimpan aman di antrean dan baru diprses oleh modul kurir kapan pun modul tersebut siap.

- Apa risiko jika salah penempatan seperti RPC dipakai untuk notifikasi kurir. Jika kita menggunakan pattern RPC yang sinkron untuk mengirim notifikasi ke kurir, sistem akan bermasalah. Modul pembayaran harus menuggu sampai modul kurir selesai mencatat data. Jika server kurir sedang bermasalah atau down, yang menyebabkan seluruh modul pembayaran akan ikut terhenti. Pengguna akan melihat layar loading yang sangat lama hanya karena sistem sedang kesulitan menghubungi kurir, padahal pembayaran sendiri sudah sukses. Hal ini jelas saja menurunkan performa dan kenyamanan customer secara keseluruhan.