## Analisis - ditulis oleh Rovino Ramadhani

### 1. Pemilihan Pemimpin Awal

**Hasil pengujian:** Saat kelima proses dijalankan dalam waktu berdekatan, Node 1, 2, 3, dan 4 sempat mendeklarasikan diri sebagai *leader*. Setelah Node 5 aktif dan mengirim pesan `COORDINATOR`, Node 1–4 mencatat Node 5 sebagai pemimpin akhir.

**Analisis:** Deklarasi pemimpin sementara terjadi karena beberapa node belum menerima balasan `OK` sebelum batas waktu pemilihan berakhir. Dalam algoritma Bully, node dengan identitas tertinggi yang masih aktif menjadi pemimpin. Oleh karena itu, keberhasilan skenario ini ditentukan oleh keadaan akhir seluruh node, bukan hanya pesan pemilihan yang pertama kali muncul.

### 2. Pemilihan Ulang Setelah Pemimpin Berhenti

**Hasil pengujian:** Setelah Node 5 dihentikan, Node 1, 2, dan 4 mencatat bahwa pemimpin tidak tersedia. Pesan `ELECTION` dikirim ke node beridentitas lebih tinggi dan direspons dengan `OK` oleh node yang masih aktif. Node 4 kemudian mendeklarasikan diri sebagai pemimpin dan mengirim pesan `COORDINATOR` kepada Node 1–3. Log ketiga node tersebut menunjukkan bahwa pemimpin yang tercatat berubah menjadi Node 4.

**Analisis:** Node 4 menjadi pemimpin baru karena tidak ada node beridentitas lebih tinggi yang merespons pemilihannya setelah Node 5 berhenti. Proses ini memperlihatkan fungsi mekanisme pendeteksian kegagalan dan pemilihan ulang sehingga node lain dapat mengetahui pemimpin pengganti tanpa perlu menjalankan ulang seluruh sistem.

### 3. Relevansi Pemimpin terhadap Antrean Pesanan FoodGo

**Kebutuhan sistem:** Pada kasus FoodGo, dua peladen dapat mencatat urutan pesanan secara berbeda ketika jam tidak sinkron. Jika setiap peladen menentukan urutan pemrosesan sendiri, terdapat risiko keputusan antrean yang saling bertentangan.

**Analisis:** Penetapan satu node sebagai pemimpin dapat menjadi dasar penentuan pihak yang mengatur antrean pesanan pusat. Algoritma Bully membantu memilih pengelola tersebut ketika terjadi pergantian pemimpin. Namun, pemilihan pemimpin saja tidak menyinkronkan jam, menjamin urutan pesanan, ataupun mencegah pemrosesan ganda. Penerapan nyata tetap membutuhkan mekanisme pengurutan pesanan, pencatatan status yang konsisten, dan pencegahan pemrosesan berulang.

### 4. Batasan Pengujian

**Cakupan bukti:** Log yang diperoleh membuktikan pemilihan Node 5 pada kondisi awal dan pemilihan ulang Node 4 setelah Node 5 dihentikan. Pengujian belum mencakup gangguan jaringan, pemulihan node, maupun pemrosesan antrean pesanan FoodGo secara langsung.

**Analisis:** Simulasi ini menunjukkan berjalannya mekanisme pemilihan pemimpin pada dua skenario yang ditentukan dalam tugas. Hasil tersebut belum membuktikan terselesaikannya seluruh persoalan koordinasi sistem terdistribusi. Berbeda dari algoritma konsensus seperti Raft, algoritma Bully dalam simulasi ini berfokus pada pemilihan pemimpin, bukan replikasi log atau kesepakatan atas urutan data pesanan.
