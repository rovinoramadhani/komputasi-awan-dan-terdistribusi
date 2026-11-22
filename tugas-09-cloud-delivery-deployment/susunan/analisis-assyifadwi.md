## Jawaban Nomor 3 - Ditulis oleh Assyifa Dwi Safitri

### a. Risiko layanan verifikasi tidak mampu menampung lonjakan permintaan

Pada puncak musim pemilu atau penerimaan sekolah, banyak instansi bisa mengirim permintaan dalam waktu hampir bersamaan. Karena Private Cloud bergantung pada kapasitas perangkat yang dimiliki pemerintah, penambahan instans aplikasi tidak akan membantu apabila CPU, memori, atau database sudah mencapai batas fisik. Akibatnya, permintaan menumpuk dan proses validasi identitas terlambat.

#### Mitigasi:

- Menyusun *Capacity Planning* berdasarkan perkiraan permintaan puncak dan menyediakan cadangan server serta kapasitas basis data.
- Menggunakan *load balancer*, autoscaling internal, antrean pemrosesan, serta pembatasan laju permintaan (*rate limiting*) per instansi.
- Menjalankan pengujian beban sebelum periode sibuk dan menetapkan prioritas layanan penting.

### b. Risiko penyalahgunaan hak akses oleh pengguna dari instansi mitra

Ribuan petugas dan sistem terhubung ke layanan kependudukan. Akun yang dicuri atau izin akses yang terlalu luas dapat digunakan untuk melakukan pencarian NIK massal, melihat data yang tidak terkait tugas, atau mengumpulkan identitas warga. Risiko ini tetap ada walaupun seluruh data ditempatkan dalam Private Cloud.

#### Mitigasi:

- Menggunakan autentikasi multifaktor untuk petugas, identitas aplikasi yang kuat untuk API, dan prinsip *least privilege* dengan RBAC/ABAC.
- Mewajibkan otoritasi berdasarkan tujuan penggunaan, membatasi atribut dalam respons, serta menerapkan kuota pencarian per lembaga.
- Menerapkan pemantauan anomali, audit aksese, dan prosedur pencabutan akun/token serta tidak menyimpan NIK lengkap pada log operasional.

### c. Risiko gangguan pusat data pemerintah menyebabkan layanan nasional terhenti

Jika pusat data utama mengalami gangguan listrik, jaringan, bencana, atau kegagalan penyimpanan, layanan verifikasi dari berbagai daerah bisa ikut terdampak. Konsentrasi infrastruktur di bawah satu operator memperbesar dampak apabila tidak ada rancangan pemulihan.

#### Mitigasi:

- Menyediakan pusat data cadangan pemerintah di lokasi geografis berbeda, dengan replikasi terenkripsi dan hak akses setara.
- Menentukan target pemulihan (RTO/RPO), menyiapkan prosedur *failover*, dan menguji pemulihan secara berkala.
- Memisahkan sistem cadangan dari hak akses operasional sehari-hari untuk mengurangi risiko kerusakan atau penghapusan serentak.

### Kesimpulan - Soal Nomor 3

Berdasarkan analisis risiko dan mitigasi, penggunaan Private Cloud pada Sistem Data Kependudukan memiliki beberapa tantangan, yaitu keterbatasan kapasitas saat terjadi lonjakan akses, penyalahgunaan hak akses oleh instansi, serta gangguan pada pusat data pemerintah. Risiko tersebut dapat diminimalkan melalui perencanaan kapasitas, penerapan *load balancing* dan *autoscaling*, pengaturan hak akses yang ketat, serta penyediaan pusat data cadangan. Dengan mitigasi yang tepat, Private Cloud dapat menjaga keamanan dan kerahasiaan data penduduk sekaligus mendukung ketersediaan layanan bagi ribuan instansi. Oleh karena itu, keberhasilan Private Cloud tidak hanya bergantung pada pemilihan model cloud, tetapi juga pada pengelolaan keamanan, kapasitas, dan keandalan infrastruktur secara berkelanjutan.
