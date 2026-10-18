# Tugas 5 (Pekan 5) - Koordinasi & Konsensus

**Kelompok:** Kelompok 2

| Nama                    | NIM          | Kontribusi                                                                                                                                                                                                                                                                                                                 |
|-------------------------|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Rovino Ramadhani        | 103072400031 | Mengimplementasikan Bully Algorithm pada `src/node.py`, melakukan pengujian pemilihan pemimpin awal dan pemilihan ulang, mendokumentasikan hasil pengujian melalui log dan screenshot, serta menyusun analisis hasil simulasi dan keterbatasan implementasi. Melakukan integrasi hasil pekerjaan kelompok ke branch utama. |
| Galang Herjuno Mulya    | 103072430006 | Menyusun analisis jumlah pesan selama proses pemilihan pemimpin, mengevaluasi mekanisme timeout dan waktu pemilihan ulang, serta mengidentifikasi keterbatasan implementasi, kelengkapan bukti pengujian, dan bagian laporan yang memerlukan perbaikan.                                                                    |
| Erastus Liubeta Septian | 103072400020 | Menyusun analisis alur kerja Bully Algorithm pada skenario start normal dan kegagalan pemimpin, menjelaskan proses komunikasi `ELECTION`, `OK`, dan `COORDINATOR`, serta membahas hasil implementasi dan relevansinya terhadap permasalahan koordinasi pada sistem FoodGo.                                                 |
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
## Analisis - ditulis oleh Erastus Liubeta Septian

### Skenario 1: Start Normal
1. Saat sistem dinyalakan secara bersamaan, kelima node akan mealakukan proses inisiasi di port masing-masing.
2. Node mengirim pesan **ELECTION** ke node lain yang memiliki ID lebih besar.
3. Karena Node 5 adalah node dengan ID teringgi, daftar target node yang lebih besar bernilai kosong.
4. Node 5 tidak menerima pesan **OK** dalam batas watktu tertentu, sehingga node tersebut terpilih menjadi leader.
5. Node 5 mem-broadcast pesan **COORDINATOR** ke Node lainnya.
6. Node 1 - 4 menerima pesan tersebut dan secara sereantak mencatat Node 5 sebagai leader aktif.

### Skenario 2: Leader Mati (Re-election)
1. Proses pada Node 5 dimatikan secara paksa, mensimulasikan terjadinya kegagalan pada node leader.
2. Node yang tersisa 1 - 4 mendeteksi bahawa leader tidak merespons, yang memicu proses pemilihan leader baru.
3. Node yang mendeteksi kegagalan mengirim pesan **ELECTION** ke node dengan ID lebih besar.
4. Node 2 - 4 membalas pesan **ELECTION** dari node yang lebih rendah dengan pesan **OK**, lalu melajutkan pencalonan dirinya sendiri ke atas.
5. Node 4 mengirim pesan **ELECTION** ke node 5, namun tidak menerima balasan **OK** karena node 5 mati.
6. Setelah timeout habis tanpa respon, node 4 menetapkan dirinya sebagai leader baru.
7. Node 4 mengirim pesan **COORDINATOR** ke node 1 - 3, yang sebelumnya menerima pesan **OK**.
8. Node 1, 2 dan 3 mencatat Node 4 sebagai leader aktif.

### Pembahasan
Pelaksanaan sismulasi ini bertujuan untuk menyelesaikan masalh konfilik pemrosesan ganda pada pesanan FoodGo melalui penerapann algoritma Bully, yang memastikan hanya ada satu node leader yang aktif untuk mengelola antran pusat. Algoritma ini beroperasi dengan prisnsip hierarki yang terstruktur, dimana sistem secara mutlak mendelegasi wewenang leader ke node aktif yang memiliki ID tertinggi.

Pada skenario start normal, kelima node dijalakan secara bersamaan, dan sistem berhasil menetapkan node 5 sebagai leader. Penetapan ini terjadi karena node 5 beroperasi dengan ID terbesar, sehingga ketika proses election dimulai, tidak ada node dengan ID yang lebih tinggi mengirimkan pesan **OK** untuk menginterupsi pencalonannya. Setelah batas waktu habis, node 5 secara otomatis mengambil alih leader dan membroadcast pesan **COORDINATOR** ke seluruh node di bawahnya.

Pada skenario kedua sistem diuji dengan mematikan proses pada node 5 secara paksa untuk mensimulasikan server down, hilangnya respon dari node 5 segera dideteksi olehh node-node dibawahnya, yang kemudian secara otomatis memicu proses re-election, Node-node yang tesisa mengirimkan pesan **ELECTION** ke atas dan prose eliminasi terjadi melaluibalasan pesan **OK**. Karena node 5 sudah mati, node 4 tidak menerima pesan **OK** dari node manapun sehingga node 4 berhak mengambil posisi leader yang baru. Meskipun Node 4 memproklamasikan dirinya sebagai leader, node ini baru dapat beroperasi penuh setelah mengirimkan pesan **COORDINATOR** dan menerima konfirmasi dari node lainnya, yang sekali lagi menunjukkan bagaimana pesan **OK** dan **COORDINATOR** berfungsi krusial dalam menjaga konsistensi status pemimpin di seluruh jaringan.

### Kesimpulan
Algoritma Bully berhasil diterapkan untuk mengatasi masalah koordinasi pemrosesan ganda pada sistem FoodGo. Pada implementasi ini, algoritma mampu mendeteksi kondisi kegagalan leader dan memicu pemilihan ulang secara otomatis, sehingga sistem tetap berjalan meskipun terjadi gangguan. Meskipun demikian, algoritma Bully memiliki beberapa keterbatasan, seperti tidak efektifnya mekanisme pemilihan ulang ketika node pemimpin dengan ID tertinggi mati bersamaan dengan node lainnya. Selain itu, efisiensi algoritma ini dalam kondisi jaringan yang sibuk patut dipertimbangkan karena membutuhkan jumlah pesan yang cukup banyak selama proses pemilihan leader.

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
