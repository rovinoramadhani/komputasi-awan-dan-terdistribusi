## Analisis Individu - Galang Herjuno Mulya

Berdasarkan kasus FoodGo, permasalahan utamanya terletak pada keterlambatan sinkronisasi data antara server Jakarta dan Bandung. Ketika pelanggan melakukan top-up di Jakarta, saldo memang sudah berhasil diperbarui. Namun, saat pelanggan berpindah dan mengakses server Bandung, belum tentu saldo tersebut sudah ikut diperbarui. Akibatnya, pelanggan bisa mengalami penolakan saat memesan makanan, padahal sebenarnya saldo mereka sudah mencukupi.

### Penilaian Model Konsistensi

Menurut saya, Eventual Consistency saja masih kurang tepat, terutama untuk data yang berhubungan dengan saldo pelanggan. Memang pada akhirnya kedua server akan memiliki data yang sama, tetapi masalahnya adalah pelanggan membutuhkan informasi saldo yang akurat pada saat melakukan transaksi, bukan beberapa detik setelahnya.

Keterlambatan seperti ini cukup berisiko bagi FoodGo. Bayangkan pelanggan sudah melakukan top-up, tetapi tetap tidak bisa memesan makanan karena sistem membaca saldo lama. Selain membuat pelanggan kesal, hal tersebut juga bisa mengurangi kepercayaan terhadap aplikasi. Kondisi ini tentu berbeda dengan keterlambatan pembaruan jumlah like atau informasi lain yang tidak berpengaruh langsung terhadap transaksi.

Sequential Consistency sebagai model yang digunakan dalam analisis. Model ini mempertimbangkan urutan operasi, sehingga proses top-up dan pembacaan saldo dapat dipahami secara berurutan. Selain itu, kami juga mengusulkan penggunaan Read-Your-Writes agar pelanggan tetap bisa melihat saldo terbaru setelah melakukan top-up, meskipun berpindah server. Untuk melihat bagaimana mekanisme tersebut bekerja, kami melakukan simulasi dengan membandingkan versi data pada masing-masing server.
