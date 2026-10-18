## Kesimpulan Kelompok

Berdasarkan hasil implementasi dan pengujian, kelompok berhasil menerapkan Bully Algorithm untuk melakukan pemilihan
pemimpin (leader election) pada sistem terdistribusi yang terdiri dari lima node virtual. Pada skenario pertama, Node 5
berhasil terpilih sebagai pemimpin karena memiliki ID tertinggi. Meskipun Node 1 hingga Node 4 sempat mendeklarasikan
diri sebagai pemimpin sementara akibat perbedaan waktu komunikasi dan timeout, seluruh node pada akhirnya mengenali Node
5 sebagai pemimpin aktif setelah menerima pesan COORDINATOR.

Pada skenario kedua, ketika Node 5 dihentikan, node yang tersisa berhasil melakukan pemilihan ulang (re-election) secara
otomatis. Proses ini melibatkan pengiriman pesan ELECTION, penerimaan balasan OK, dan pengumuman pemimpin baru melalui
pesan COORDINATOR. Hasil pengujian menunjukkan bahwa Node 4 berhasil mengambil alih kepemimpinan sebagai node dengan ID
tertinggi yang masih aktif, tanpa perlu menjalankan ulang seluruh sistem.

Dari hasil analisis kelompok, Bully Algorithm memiliki keunggulan berupa mekanisme pemilihan pemimpin yang terstruktur
dan kemampuan melakukan pergantian pemimpin ketika terjadi kegagalan. Namun, algoritma ini memiliki keterbatasan berupa
meningkatnya jumlah pesan komunikasi ketika beberapa node memulai pemilihan secara bersamaan serta adanya waktu tunggu
sebelum pemimpin baru ditetapkan. Dibandingkan Raft, Bully hanya berfokus pada pemilihan pemimpin dan tidak menyediakan
mekanisme konsensus untuk replikasi data.

Dalam konteks FoodGo, penerapan Bully Algorithm dapat menjadi dasar penentuan satu node yang bertanggung jawab mengelola
antrean pesanan pusat. Namun, pemilihan pemimpin saja belum menjamin konsistensi urutan pesanan maupun mencegah
pemrosesan ganda. Oleh karena itu, sistem tetap membutuhkan mekanisme pengurutan, sinkronisasi data, dan pengendalian
pemrosesan pesanan agar koordinasi antarnode berjalan secara konsisten.