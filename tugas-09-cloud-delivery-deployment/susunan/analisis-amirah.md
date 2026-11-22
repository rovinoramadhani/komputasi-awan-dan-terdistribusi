## Jawaban Nomor 1 - Ditulis Oleh Amirah Essary Yunsarah Sujuthi

## 1. Rekomendasi Deployment Model

Deployment model yang direkomendasikan untuk Sistem Data Kependudukan adalah **Private Cloud**, yaitu model cloud computing yang infrastrukturnya digunakan secara khusus dan dikelola dalam kendali penuh pemerintah.

Pemilihan Private Cloud didasarkan pada kebutuhan sistem yang menyimpan data pribadi bersifat sensitif, seperti nama, NIK, alamat, dan data biometrik. Data tersebut membutuhkan perlindungan ketat agar tidak diakses atau disalahgunakan oleh pihak yang tidak berwenang. Melalui Private Cloud, pemerintah dapat mengendalikan lokasi penyimpanan, pengelolaan server, keamanan jaringan, serta hak akses terhadap data kependudukan.

Selain menjaga kerahasiaan, sistem juga harus mampu melayani ribuan instansi dengan jumlah akses yang tidak selalu sama. Oleh karena itu, Private Cloud perlu dilengkapi dengan pengelolaan sumber daya yang fleksibel, penambahan kapasitas server, dan pembagian beban (*load balancing*) agar layanan tetap tersedia ketika terjadi peningkatan akses.

### Analisis Berdasarkan Karakteristik NIST SP 800-145

Berdasarkan NIST SP 800-145, terdapat lima karakteristik utama cloud computing yang menjadi dasar pertimbangan dalam penerapan Private Cloud.

**a. On-Demand Self-Service**
Karakteristik ini memungkinkan administrator menyediakan sumber daya komputasi secara mandiri melalui sistem pengelolaan cloud. Pada Sistem Data Kependudukan, pemerintah dapat menambah kapasitas server, penyimpanan, atau layanan aplikasi sesuai kebutuhan tanpa harus melakukan konfigurasi manual setiap saat. Proses tersebut tetap dibatasi oleh kebijakan keamanan dan kewenangan administrator.

**b. Broad Network Access**
Layanan cloud dapat diakses melalui jaringan menggunakan berbagai perangkat yang mendukung. Dalam sistem ini, instansi seperti Dukcapil daerah, kepolisian, dan bank dapat mengakses layanan verifikasi sesuai kewenangannya. Akses dilakukan melalui jaringan yang aman dengan autentikasi dan pembatasan hak akses agar data kependudukan tidak dapat diakses secara bebas.

**c. Resource Pooling**
Sumber daya komputasi, seperti server, penyimpanan, dan jaringan, dikumpulkan untuk melayani banyak pengguna secara bersama. Pemerintah dapat mengalokasikan sumber daya kepada berbagai instansi berdasarkan kebutuhan masing-masing. Dengan demikian, penggunaan infrastruktur menjadi lebih efisien, sementara pemisahan akses tetap diterapkan untuk menjaga kerahasiaan data.

**d. Rapid Elasticity**
Karakteristik ini memungkinkan kapasitas komputasi ditambah atau dikurangi dengan cepat mengikuti kebutuhan sistem. Ketika terjadi lonjakan akses saat pemilu atau pendaftaran sekolah, kapasitas layanan dapat ditingkatkan untuk mengurangi risiko gangguan. Namun, kemampuan tersebut tetap bergantung pada sumber daya fisik yang tersedia sehingga pemerintah perlu menyiapkan kapasitas cadangan.

**e. Measured Service**
Penggunaan sumber daya cloud dapat dipantau dan diukur secara otomatis. Pemerintah dapat memantau penggunaan CPU, penyimpanan, jaringan, serta jumlah permintaan layanan dari setiap instansi. Hasil pemantauan digunakan untuk mengevaluasi kinerja, mengoptimalkan penggunaan sumber daya, dan merencanakan peningkatan kapasitas.

### Kesesuaian dengan Kerahasiaan dan Skalabilitas
Dari sisi **kerahasiaan**, Private Cloud memungkinkan pemerintah memiliki kendali langsung terhadap infrastruktur dan pengelolaan data kependudukan. Perlindungan dapat dilakukan melalui enkripsi, autentikasi, pembatasan hak akses, dan pemantauan aktivitas pengguna. Hal ini sesuai dengan persyaratan bahwa data sensitif harus berada dalam infrastruktur yang sepenuhnya dikendalikan negara.

Dari sisi **skalabilitas**, Private Cloud mendukung penggunaan virtualisasi, penambahan kapasitas komputasi, dan *load balancing* untuk menangani permintaan dari ribuan instansi. Meskipun kemampuan peningkatan kapasitasnya bergantung pada infrastruktur yang tersedia, pemerintah dapat mengantisipasinya melalui perencanaan kapasitas, penyediaan server cadangan, dan pengelolaan beban layanan.

### Kesimpulan
**Private Cloud menjadi deployment model yang direkomendasikan** karena mampu memberikan kendali penuh terhadap penyimpanan dan pemrosesan data kependudukan sekaligus mendukung kebutuhan akses dari banyak instansi. Dengan perencanaan kapasitas dan penerapan keamanan yang tepat, Private Cloud dapat mendukung sistem yang aman, stabil, dan dapat dikembangkan sesuai kebutuhan pemerintah.