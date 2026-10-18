# Tugas 5 (Pekan 5) - Koordinasi & Konsensus

**Kelompok:** Kelompok 2

| **Nama**                | **NIM**      | **Kontribusi** |
|-------------------------|--------------|----------------|
| Rovino Ramadhani        | 103072400031 |                |
| Galang Herjuno Mulya    | 103072430006 |                |
| Erastus Liubeta Septian | 103072400020 |                |
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

## Analisis - Galang Herjuno Mulya

### Banyaknya pesan saat pemilihan leader

Dari log setelah Node 5 dimatikan, terlihat Node 1 mengirim pesan `ELECTION` ke Node 2, 3, dan 4. Node 2 mengirim pesan yang sama ke Node 3 dan 4, sedangkan Node 3 mengirimnya ke Node 4. Jadi, ada enam pesan `ELECTION` yang berhasil dikirim antar-node yang masih hidup. Semua pesan tersebut dibalas dengan `OK`. Setelah itu, Node 4 mengirim `COORDINATOR` ke Node 1, 2, dan 3. Pesan ke Node 5 yang sudah mati tidak tercatat sebagai pesan yang berhasil dikirim.

Hal ini menunjukkan bahwa ketika beberapa node memulai pemilihan bersamaan, jumlah pesan bisa menjadi banyak. Jika jumlah node ditambah, komunikasi antarnode juga akan semakin ramai. Kekurangan Bully ini perlu disebutkan saat membandingkannya dengan cara memilih leader yang lain.

### Waktu yang dibutuhkan untuk memilih pengganti

Pada program `src/node.py`, node memeriksa keadaan leader setiap 3 detik. Setelah pemilihan dimulai, node juga menunggu hingga 2 detik untuk melihat apakah ada balasan `OK`. Bahkan Node 5, yang tidak memiliki node dengan ID lebih tinggi, tetap menunggu 2 detik sebelum menyatakan diri sebagai leader. Node 4 juga perlu menunggu saat memastikan Node 5 sudah tidak merespons.

Akibatnya, ada waktu ketika antrean pusat FoodGo belum memiliki pengelola yang pasti. Untuk mempercepat proses, node yang memang tidak memiliki ID lebih tinggi bisa langsung menyatakan diri sebagai leader. Namun, bila masih ada node ber-ID lebih tinggi, waktu tunggu tetap diperlukan agar node tersebut punya kesempatan membalas.

### Bukti dan jurnal yang masih perlu dilengkapi

Gambar dan log di folder `bukti` sudah menunjukkan urutan pemilihan, tetapi tidak mencantumkan waktu pada setiap kejadian. Karena itu, kita belum bisa mengetahui dengan pasti berapa lama waktu dari Node 5 dimatikan sampai semua node mengenali Node 4 sebagai leader. Saat pengujian berikutnya, waktu penghentian Node 5 dan waktu pengumuman leader baru sebaiknya dicatat.

`JURNAL.md` juga masih berisi tanda `...` pada bagian kendala, hasil pengujian, lama pemilihan ulang, dan penggunaan AI. Bagian-bagian itu perlu diisi sesuai kejadian yang benar-benar diamati. Jika AI digunakan, pemakaiannya juga perlu dicatat sesuai petunjuk jurnal.

### Bagian laporan yang perlu diperbaiki

Soal pada `README.md` meminta penjelasan mengapa node dengan ID tertinggi yang masih hidup akan menjadi leader dan apa kelemahan Bully dibanding Raft. Jawaban untuk bagian ini belum ada di `README.md` tugas. Penjelasannya bisa memakai hasil log: node dengan ID lebih rendah berhenti mencalonkan diri setelah mendapat `OK`, sedangkan node dengan ID tertinggi yang masih hidup tidak mendapat balasan dari node yang lebih tinggi lalu mengumumkan dirinya. Bully hanya memilih leader; Raft juga mengatur agar beberapa node menyepakati catatan data yang sama, tetapi cara kerjanya lebih rumit.

Selain itu, `Kesimpulan Kelompok` di `ANALISIS.md` masih membahas multithreading, `Lock`, dan Docker dari tugas lain. Kesimpulan tersebut perlu disesuaikan dengan hasil dua skenario Tugas 5. Tabel kontribusi anggota yang masih kosong juga perlu diisi berdasarkan pekerjaan masing-masing.

## Kesimpulan Kelompok

Berdasarkan hasil pengujian dan analisis kelompok, penggunaan multithreading memungkinkan beberapa pekerjaan diproses
secara bersamaan, tetapi penggunaan data bersama tanpa mekanisme sinkronisasi dapat menyebabkan *race condition*. Pada
percobaan tanpa `threading.Lock()`, nilai `processed_count` hanya mencapai 46 dari 100 pesanan karena beberapa thread
membaca dan memperbarui nilai yang sama secara bersamaan sehingga terjadi *lost update*.

Setelah menggunakan `threading.Lock()`, seluruh 100 pesanan berhasil tercatat dengan benar. Lock memastikan bagian
*critical section* hanya diakses oleh satu thread pada satu waktu sehingga perubahan data bersama tetap konsisten.
Konsekuensinya, thread lain harus menunggu ketika Lock sedang digunakan sehingga bagian yang dilindungi sebaiknya dibuat
sesingkat mungkin agar tidak mengurangi keuntungan pemrosesan secara konkuren.

Pengujian menggunakan Docker juga menghasilkan 100 dari 100 pesanan, sama dengan eksekusi langsung yang menggunakan
Lock. Hal ini menunjukkan bahwa program dan mekanisme sinkronisasi tetap menghasilkan perilaku yang konsisten ketika
dijalankan di dalam container.

Secara keseluruhan, multithreading tepat digunakan untuk menjalankan pekerjaan secara konkuren, sedangkan Lock
diperlukan ketika beberapa thread mengakses dan mengubah data bersama. Docker berperan dalam menyediakan lingkungan
eksekusi yang konsisten tanpa mengubah logika sinkronisasi pada program.

