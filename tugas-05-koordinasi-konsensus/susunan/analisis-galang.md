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