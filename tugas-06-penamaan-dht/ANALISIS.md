# Tugas 6 (Pekan 6) — Penamaan & Resolusi Lokasi

**Kelompok:** Kelompok 2

| Nama                    | NIM          | Kontribusi                                                                                                                                                                                 |
|-------------------------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Rovino Ramadhani        | 103072400031 | Implementasi simulasi Chord DHT (lookup, join, leave), pengujian dan dokumentasi hasil program, penyusunan jurnal, penulisan analisis individu, serta penyiapan struktur dokumen kelompok. |
| Galang Herjuno Mulya    | 103072430006 |                                                                                                                                                                                            |
| Erastus Liubeta Septian | 103072400020 |                                                                                                                                                                                            |
## Analisis - ditulis oleh Rovino Ramadhani

### 1. Alasan Penggunaan DHT/Chord pada FoodGo

Pada studi kasus FoodGo, setiap kurir memiliki ID tetap, tetapi alamat IP dapat berubah ketika kurir berpindah lokasi
atau menggunakan jaringan yang berbeda. Kondisi ini membutuhkan mekanisme pencarian alamat IP yang mampu memperbarui
mapping tanpa bergantung pada satu server pusat.

Penggunaan DHT dengan algoritma Chord dinilai lebih sesuai karena:

1. Flat naming dengan tabel pusat menyimpan seluruh mapping ID kurir dan alamat IP dalam satu server. Ketika jumlah
   kurir meningkat, server tersebut berpotensi mengalami bottleneck. Jika server mengalami gangguan, proses pencarian
   alamat IP juga dapat terhenti.
2. DNS konvensional menggunakan struktur penamaan hierarkis dan mekanisme caching. Meskipun DNS mendukung pembaruan
   alamat IP, perubahan yang terlalu sering dapat menyebabkan cache menyimpan alamat lama hingga masa TTL berakhir.
3. Chord DHT mendistribusikan tanggung jawab penyimpanan mapping berdasarkan hasil hashing. Setiap ID kurir dipetakan ke
   node successor sehingga proses pencarian tidak harus bergantung pada satu server pusat.

Dengan pendekatan tersebut, FoodGo dapat mempertahankan ID kurir yang sama meskipun alamat IP berubah. Pembaruan IP
cukup dilakukan pada mapping ID kurir, sedangkan penentuan node penanggung jawab mengikuti algoritma consistent hashing.

### 2. Consistent Hashing dan Ring Topology

Simulasi menggunakan ruang identifier 8-bit dengan rentang hash 0 sampai 255. Fungsi SHA-1 digunakan untuk menghasilkan
nilai hash yang kemudian disesuaikan dengan ukuran ring menggunakan operasi modulo 256.

Pada kondisi awal, terdapat empat node yang tersusun berdasarkan nilai hash:

1. Node Bandung dengan ID 40.
2. Node Jakarta 2 dengan ID 102.
3. Node Surabaya dengan ID 136.
4. Node Jakarta 1 dengan ID 177.

Susunan tersebut membentuk ring dengan urutan 40 -> 102 -> 136 -> 177 -> 40.

Setiap ID kurir ditempatkan pada node yang memiliki nilai hash terkecil yang lebih besar atau sama dengan hash key.
Sebagai contoh, `kurir-001` memiliki hash 50 sehingga menjadi tanggung jawab node 102. Sementara itu, `kurir-002`
memiliki hash 28 sehingga ditempatkan pada node 40.

Penggunaan consistent hashing memungkinkan perubahan jumlah node tanpa harus mengubah seluruh pembagian tanggung jawab
mapping. Hanya key pada rentang tertentu yang perlu dialihkan ketika node bergabung atau keluar.

### 3. Perubahan Topologi Saat Join

Pada pengujian join, node Medan dengan ID 123 dan alamat IP `10.0.0.5` ditambahkan ke dalam ring.

Sebelum node tersebut bergabung, `kurir-012` dengan hash 116 menjadi tanggung jawab node 136. Setelah node 123
bergabung, node tersebut menjadi successor terdekat untuk hash 116.

Hasil pengujian menunjukkan:

1. Jumlah node meningkat dari empat menjadi lima.
2. Susunan ring berubah menjadi `[40, 102, 123, 136, 177]`.
3. Mapping `kurir-012` berpindah dari node 136 ke node 123.
4. Total mapping yang berpindah sebanyak satu.

Hasil ini menunjukkan bahwa penambahan node hanya memengaruhi mapping yang berada dalam rentang tanggung jawab node
baru, sedangkan mapping pada node lain tetap dipertahankan.

### 4. Perubahan Topologi Saat Leave

Pada pengujian leave, `node-jakarta-1` dengan ID 177 dikeluarkan dari ring. Sebelum keluar, node tersebut bertanggung
jawab atas `kurir-005` yang memiliki hash 175.

Ketika node 177 dihapus, algoritma mencari successor berikutnya untuk mengambil alih tanggung jawab mapping. Karena
tidak terdapat node dengan ID lebih besar dari 177, pencarian kembali ke awal ring dan menemukan node 40.

Hasil pengujian menunjukkan:

1. Jumlah node berkurang dari lima menjadi empat.
2. Susunan ring berubah menjadi `[40, 102, 123, 136]`.
3. Mapping `kurir-005` berpindah dari node 177 ke node 40.
4. Total mapping yang berpindah sebanyak satu.
5. Lookup `kurir-001` dan `kurir-002` tetap menghasilkan alamat IP yang sesuai.

Perpindahan tersebut menunjukkan bahwa algoritma successor dapat menentukan node pengganti ketika terjadi perubahan
topologi. Mekanisme wrap-around juga memastikan bahwa key tetap memiliki node penanggung jawab selama ring tidak kosong.
## Analisis - Galang Herjuno Mulya

## Analisis - ditulis oleh Erastus Liubeta Septian

## Kesimpulan Kelompok

