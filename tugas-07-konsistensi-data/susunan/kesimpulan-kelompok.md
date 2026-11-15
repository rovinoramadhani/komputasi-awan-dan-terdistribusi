## Kesimpulan Kelompok

Berdasarkan analisis seluruh anggota kelompok dan hasil simulasi pada studi kasus e-wallet FoodGo, dapat disimpulkan
bahwa Eventual Consistency saja tidak cukup untuk menjamin pelanggan memperoleh saldo terbaru setelah melakukan
top-up. Keterlambatan replikasi antara server Jakarta dan Bandung dapat menyebabkan pembacaan saldo lama (*inconsistent
read*) dan berpotensi mengakibatkan penolakan transaksi.

Sequential Consistency memberikan jaminan keterurutan operasi yang lebih kuat, tetapi penerapannya perlu
mempertimbangkan biaya koordinasi antarserver. Oleh karena itu, kelompok mengusulkan pendekatan Client-Centric
Consistency, khususnya Read-Your-Writes, untuk menjamin pelanggan dapat membaca perubahan saldo yang telah
berhasil dilakukan.

Hasil simulasi membuktikan bahwa tanpa Read-Your-Writes, saldo Rp50.000 yang telah diperbarui di Jakarta masih terbaca
Rp0 di Bandung akibat keterlambatan replikasi selama 2 detik. Setelah mekanisme Read-Your-Writes diterapkan, sistem
berhasil mendeteksi perbedaan versi data dan mengalihkan pembacaan ke Jakarta sehingga saldo terbaru Rp70.000 dapat
ditampilkan.

Dengan demikian, Read-Your-Writes efektif mengatasi permasalahan pembacaan saldo lama pada skenario yang diuji,
tanpa harus menunggu seluruh replika selesai melakukan sinkronisasi. Namun, transaksi keuangan tetap memerlukan
mekanisme tambahan untuk menjaga keamanan dan konsistensi perubahan saldo secara bersamaan.