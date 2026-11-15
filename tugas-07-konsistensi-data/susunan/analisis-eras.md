## Analisis Individu - Erastus Liubeta Septian

### 1. Kebutuhan Model Konsistensi Data: Eventual vs. Sequential Consistency
Pada sistem e-wallet FoodGo, model **Eventual Consistency murni jelas tidak cukup**. Model ini membiarkan data antar-server berbeda sementara waktu sebelum akhirnya sinkron. Untuk urusan saldo uang, jeda replikasi tersebut berdampak langsung pada operasional:
- **Dampak Bisnis & Finansial:** Kasus saldo e-wallet sangat berbeda dengan jumlah *like* di media sosial. Pada media sosial, perbedaan beberapa angka like selama beberapa detik tidak merugikan siapa pun. Namun pada e-wallet, jika pelanggan baru saja top-up di server Jakarta lalu memesan makanan di server Bandung dan saldonya masih terbaca 0, transaksi akan langsung ditolak. Pelanggan merasa uangnya hilang, komplain melonjak, dan reputasi aplikasi akan jatuh.

Meski begitu, menerapkan **Sequential Consistency penuh** pada seluruh replika (Jakarta dan Bandung) juga kurang tepat karena membutuhkan koordinasi sinkron global setiap kali ada penulisan data. Hal ini akan membuat proses transaksi menjadi lambat dan sistem mudah terganggu jika jaringan antar-kota mengalami kendala.

### 2. Solusi Tepat: Client-Centric Consistency (Read-Your-Writes)
Pendekatan yang paling pas untuk kasus ini adalah **Client-Centric Consistency**, khususnya **Read-Your-Writes**:
- Pelanggan sebenarnya tidak menuntut seluruh pengguna lain melihat saldo terbarunya seketika itu juga, melainkan dirinya sendiri yang harus selalu melihat hasil transaksinya yang paling baru.
- **Cara kerjanya:** Setiap kali top-up berhasil, server mencatat nomor versi terbaru (misal versi 1, versi 2). Saat pelanggan membaca saldo dari server Bandung, aplikasi menyertakan versi minimum yang diharapkan. Jika data di server Bandung masih versi lama, sistem otomatis mengalihkan (*redirect*) pembacaan ke server Jakarta yang memegang data terbaru. Replikasi antar-server tetap bisa berjalan asinkron di latar belakang tanpa mengganggu kenyamanan pengguna.

### 3. Analisis Hasil Simulasi Program (`replica_simulation.py`)
Dari hasil pengujian simulasi pada file `replica_simulation.py`:
- **Skenario Naif (Tanpa Read-Your-Writes):** Pelanggan top-up Rp50.000 di Jakarta, lalu 0.5 detik kemudian mengecek saldo dari server Bandung. Karena ada delay replikasi 2.0 detik, server Bandung mengembalikan saldo `0.0`. Ini membuktikan terjadinya *inconsistent read* yang menyebabkan transaksi ditolak.
- **Skenario dengan Read-Your-Writes:** Setelah top-up kedua menjadi Rp70.000 (versi 2), server Bandung mendeteksi bahwa versinya masih versi 1. Sistem langsung mengalihkan pembacaan ke Jakarta, sehingga saldo Rp70.000 berhasil terbaca dengan benar dan bug teratasi tanpa harus menunggu replikasi selesai.

### 4. Skenario Tambahan (Aplikasi Transportasi Online)
Sebagai pembanding pada kasus aplikasi ojek online:
- **Penerimaan Order / Booking Driver:** Membutuhkan **Sequential Consistency**. Ketika dua pelanggan memesan driver yang sama di waktu bersamaan, sistem wajib memastikan urutan pemesanan secara ketat agar tidak terjadi *double booking* pada satu driver.
- **Pelacakan Posisi GPS Driver:** Cukup menggunakan **Eventual / Monotonic-Read Consistency**. Jika koordinat driver di peta penumpang sedikit terlambat diperbarui antar-server, hal tersebut tidak membatalkan pesanan atau merugikan keuangan pengguna.

### 5. Kesimpulan
1. Saldo e-wallet tidak bisa mengandalkan *Eventual Consistency* murni karena menyangkut uang nyata dan kepercayaan pelanggan.
2. Mekanisme *Read-Your-Writes* adalah solusi paling seimbang: menjamin pelanggan selalu melihat data terbarunya sendiri tanpa harus membebani sistem dengan koordinasi global yang lambat.
3. Simulasi program membuktikan bahwa pengecekan nomor versi dan mekanisme pengalihan baca (*redirect*) berhasil mencegah pembacaan data lama (*stale read*) saat proses replikasi sedang tertunda.
