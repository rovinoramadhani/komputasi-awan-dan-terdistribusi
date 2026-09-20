## Bandwith is Infinite — ditulis oleh Galang

**Bukti di skenario:** 
1. Aplikasi menjadi lambat, beberapa timeout
2. Server backend kadang crash total dan perlu di-restart manual.
3. Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama.


**Kenapa ini keliru:** Bandwith adalah besaran yang memiliki batas, jika developer berpikir jika bandwith adalah infinite, maka bisa saja tidak ada request limit, sehingga membanjiri queue sehingga dapat menyebabkan congestion collapse

**Dampak ke FoodGo:** Server backend kerap crash total dan perlu di-restart manual.

**Solusi desain awal:** [usulan solusi]

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

---