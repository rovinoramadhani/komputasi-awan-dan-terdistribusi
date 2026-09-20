## Bandwith is Infinite — ditulis oleh Galang

**Bukti di skenario:** 
1. Aplikasi menjadi lambat, beberapa timeout
2. Server backend kadang crash total dan perlu di-restart manual.
3. Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama.


**Kenapa ini keliru:** Bandwith adalah besaran yang memiliki batas, jika developer berpikir jika bandwith adalah infinite, maka bisa saja tidak ada request limit, sehingga membanjiri queue dan dapat menyebabkan network congestion

**Dampak ke FoodGo:** FoodGo dapat mengalami kebanjiran Request dari client karena tidak adanya batasan. Server dapat mengalami lonjakan data yang perlu diolah ataupun request, yang mana ini dapat membebankan server pada saat traffic sedang tinggi. beban server yang melebihi kapasitasnya dapat membuat server menjadi panas, mengalami lag atau yang paling parah down dan perlu direset secara manual. 

Secara biaya, bisa dibilang ini adalah kegagalan dengan biaya yang tidak murah, banyaknya request menyebabkan biaya cloud yang dapat membengkak secara masif. Pemanggilan API yang berlebihan dalam satu siklus (misalnya hanya ada perubahan 1 query melalui pemanggilan API) dapat menyebabkan packet loss pada router, load balancer dan jaringan server

**Solusi desain awal:** jika ada pengisian form, fitur *auto-save* dilakukan pada perangkat client/lokal, data  akan dikirim ketika *user* 

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

---