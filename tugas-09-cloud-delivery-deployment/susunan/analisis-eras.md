## Jawaban Nomor 4 - Ditulis Oleh Erastus Liubeta Septian

### Alternatif yang Ditolak: Private Cloud Murni

Kelompok kami menolak **Private Cloud Murni** sebagai deployment model untuk Sistem Data Kependudukan, meskipun secara sepintas ia tampak ideal karena infrastruktur 100% berada di bawah kendali negara.

---

#### Alasan Penolakan Berdasarkan Karakteristik NIST SP 800-145

**1. Lemah pada *Rapid Elasticity***

Private Cloud dibatasi oleh kapasitas fisik perangkat keras yang terpasang di data center pemerintah — tidak ada mekanisme *auto-scaling* berbasis *resource pool* eksternal. Pola akses sistem kependudukan sangat tidak merata:
- Saat **Pemilu Serentak**, puluhan juta pengecekan status DPT terjadi dalam hitungan hari oleh petugas KPU/Bawaslu dan masyarakat.
- Saat **PPDB**, jutaan validasi NIK dan Kartu Keluarga terjadi dalam rentang 1–2 minggu.

Untuk tidak *downtime*, satu-satunya cara adalah *over-provisioning* — membangun kapasitas yang cukup untuk menanggung beban puncak tersebut. Di luar musim puncak, utilisasi server bisa serendah 10–15%, tetapi biaya operasional (listrik, pendingin, pemeliharaan) tetap berjalan penuh. Ini secara langsung melanggar prinsip ***Measured Service*** NIST, di mana sumber daya seharusnya digunakan dan dibayar secara proporsional terhadap konsumsi riil.

**2. Hambatan Struktural: Siklus Pengadaan Pemerintah**

Berbeda dengan Public Cloud yang elastis dalam hitungan menit, penambahan kapasitas fisik pada Private Cloud memerlukan proses pengadaan barang dan jasa pemerintah (*procurement*) yang bisa memakan waktu berminggu-minggu hingga berbulan-bulan. Ini menjadikan *rapid elasticity* secara praktis tidak dapat dipenuhi — bukan hanya karena keterbatasan teknis, tetapi karena kendala birokrasi pengadaan yang melekat pada infrastruktur fisik milik negara.

---

#### Mengapa Ini Bukan Alasan "Private Cloud Lebih Aman tanpa Detail"

Argumen penolakan di atas tidak menyentuh aspek keamanan/kerahasiaan, karena memang di sisi itu Private Cloud Murni *unggul* — data fisik sepenuhnya di bawah kendali negara dan memenuhi asas kedaulatan data UU PDP. Penolakan ini murni berbasis dua kegagalan karakteristik NIST yang tidak bisa disiasati tanpa keluar dari model Private Cloud Murni itu sendiri: **Rapid Elasticity** dan **Measured Service**.

---

#### Skenario Tandingan: "Bagaimana Jika Private Cloud Diperkuat dengan Kapasitas Cadangan?"

> *"Apakah Private Cloud Murni masih bisa diterima jika pemerintah menyiapkan server cadangan khusus untuk periode puncak?"*

**Jawaban:** Tidak. Membangun kapasitas cadangan untuk beban puncak sesungguhnya *adalah* definisi dari *over-provisioning* — masalah yang sama yang membuat model ini ditolak. Kapasitas cadangan tersebut hanya aktif 2–3 kali setahun, namun biaya kepemilikan (*CAPEX* dan *OPEX*) berjalan sepanjang tahun. Dibandingkan dengan Hybrid Cloud yang hanya membayar *resource* cloud publik saat lonjakan terjadi (*pay-as-you-go*), pendekatan ini jauh lebih mahal tanpa keuntungan fungsional tambahan.

---

#### Rekomendasi sebagai Perbandingan

Model yang kami pilih, **Hybrid Cloud**, menyelesaikan ketegangan ini secara langsung: lapisan *API Gateway* dan *stateless verification service* yang melayani ribuan instansi eksternal berjalan di Public/Community Cloud yang elastis, sementara *Master Database* biometrik dan NIK tetap terkunci di Private Cloud pemerintah — tidak pernah berpindah ke infrastruktur eksternal, sehingga kedaulatan data tetap terjaga.
