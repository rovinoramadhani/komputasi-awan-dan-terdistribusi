## Kesimpulan Kelompok

Berdasarkan implementasi dan hasil pengujian simulasi Chord DHT pada studi kasus FoodGo, dapat disimpulkan bahwa
mekanisme Distributed Hash Table (DHT) mampu menentukan node penanggung jawab untuk menyimpan mapping ID kurir ke alamat
IP menggunakan consistent hashing dan successor lookup. Penggunaan ruang identifier 8-bit dengan rentang 0 sampai 255
memungkinkan ID node dan ID kurir dipetakan ke dalam satu ring topology yang terstruktur.

Hasil pengujian menunjukkan bahwa:

1. Algoritma `find_successor()` berhasil menentukan node penanggung jawab berdasarkan nilai hash terkecil yang lebih
   besar atau sama dengan hash key.
2. Proses `lookup()` berhasil menemukan alamat IP kurir sesuai mapping yang terdaftar.
3. Proses `join()` berhasil menambahkan node dengan ID 123 dan mengalihkan tanggung jawab mapping `kurir-012` dari node
   136 ke node 123.
4. Proses `leave()` berhasil mengeluarkan node dengan ID 177 dan mengalihkan tanggung jawab mapping `kurir-005` ke node
   40 menggunakan mekanisme wrap-around.
5. Perubahan topologi hanya memengaruhi mapping pada rentang tertentu, sedangkan mapping kurir lainnya tetap dapat
   ditemukan.

Dari sisi penerapan, Chord DHT lebih sesuai untuk kebutuhan FoodGo dibandingkan tabel pusat sederhana karena tanggung
jawab penyimpanan mapping dapat didistribusikan ke beberapa node. Pendekatan ini juga memungkinkan alamat IP kurir
diperbarui tanpa harus mengubah identitas kurir yang digunakan dalam proses pencarian.

Simulasi yang dikembangkan telah memenuhi konsep dasar consistent hashing, ring topology, successor lookup, join, dan
leave. Namun, implementasi masih menggunakan satu proses Python dengan struktur data bersama sehingga perpindahan
mapping yang ditunjukkan merupakan perubahan tanggung jawab secara logis, bukan transfer data antarmesin. Pengujian pada
jaringan terdistribusi sebenarnya masih diperlukan untuk membuktikan ketahanan terhadap kegagalan node dan kemampuan
sistem dalam menangani pembaruan alamat IP secara dinamis.