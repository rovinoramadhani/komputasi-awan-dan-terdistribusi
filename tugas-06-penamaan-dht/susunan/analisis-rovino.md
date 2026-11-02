## Analisis Individu - Rovino Ramadhani

### 1. Analisis Penggunaan DHT/Chord

Pada sistem FoodGo, setiap kurir memiliki ID tetap, tetapi alamat IP dapat berubah ketika berpindah jaringan. Penggunaan
DHT/Chord memungkinkan pemetaan ID kurir ke alamat IP dilakukan menggunakan consistent hashing tanpa bergantung pada
satu server pusat.

Dibandingkan flat naming dengan tabel pusat yang berisiko mengalami single point of failure, DHT/Chord membagi tanggung
jawab mapping ke beberapa node. Sementara itu, DNS konvensional memiliki mekanisme caching yang berpotensi menyebabkan
penggunaan alamat IP lama ketika terjadi perubahan jaringan.

### 2. Analisis Hasil Pengujian Lookup

Berdasarkan hasil eksekusi `chord_simulation.py`, simulasi menggunakan ruang identifier 8-bit dengan empat node awal,
yaitu 40, 102, 136, dan 177.

Pengujian menunjukkan bahwa `kurir-001` dengan hash 50 berhasil ditemukan pada node 102 dengan IP `192.168.1.10`.
Sementara itu, `kurir-002` dengan hash 28 ditemukan pada node 40 dengan IP `192.168.1.11`.

Hasil tersebut menunjukkan bahwa fungsi lookup berhasil menerapkan aturan successor, yaitu memilih node dengan ID
terkecil yang lebih besar atau sama dengan nilai hash kurir.

### 3. Analisis Penambahan Node (Join)

Pada pengujian pertama, penambahan node Medan dengan ID 123 belum menghasilkan perpindahan mapping karena belum terdapat
data kurir pada rentang hash yang menjadi tanggung jawab node baru.

Setelah menambahkan `kurir-012` dengan hash 116 dan `kurir-005` dengan hash 175, pengujian menunjukkan perubahan
pembagian tanggung jawab. Ketika node Medan bergabung, mapping `kurir-012` berpindah dari node 136 ke node 123.

Hasil ini menunjukkan bahwa consistent hashing hanya mengubah tanggung jawab mapping pada rentang tertentu ketika node
baru bergabung. Mapping lain tetap berada pada node sebelumnya sehingga tidak diperlukan perubahan seluruh pemetaan
data.

### 4. Analisis Penghapusan Node (Leave)

Pengujian leave dilakukan dengan mengeluarkan node Jakarta 1 yang memiliki ID 177. Sebelum dikeluarkan, node tersebut
bertanggung jawab atas `kurir-005` dengan hash 175.

Setelah node 177 keluar, program mengalihkan tanggung jawab mapping `kurir-005` ke node 40 melalui mekanisme
wrap-around. Output menunjukkan satu mapping berpindah dan susunan ring berubah menjadi `[40, 102, 123, 136]`.

Pengujian lookup setelah perubahan topologi juga menunjukkan bahwa `kurir-001` dan `kurir-002` tetap dapat ditemukan
dengan alamat IP yang sesuai.

### 5. Evaluasi Hasil Implementasi

Berdasarkan pengujian, fungsi lookup, join, dan leave berhasil menunjukkan mekanisme dasar algoritma Chord DHT.
Perubahan jumlah node dapat memengaruhi pembagian tanggung jawab mapping tanpa harus mengubah seluruh data yang
terdaftar.

Namun, implementasi masih berjalan dalam satu proses Python dengan penyimpanan data menggunakan dictionary bersama. Oleh
karena itu, perpindahan mapping yang ditampilkan merupakan perubahan tanggung jawab secara logis, bukan perpindahan data
fisik antarserver. Simulasi juga belum menerapkan replikasi dan mekanisme penanganan kegagalan node secara nyata.