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
