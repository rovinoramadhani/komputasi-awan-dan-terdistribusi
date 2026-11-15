## Analisis Individu - Rovino Ramadhani

Berdasarkan hasil simulasi, terlihat bahwa keterlambatan replikasi data antara server Jakarta dan Bandung menyebabkan
perbedaan saldo sementara. Pada skenario tanpa Read-Your-Writes, saldo yang terbaca di server Bandung masih 0.0 meskipun
pelanggan sudah melakukan top-up sebesar 50000 melalui server Jakarta.

Setelah mekanisme Read-Your-Writes diterapkan, sistem dapat mendeteksi bahwa data di server Bandung belum diperbarui dan
mengalihkan pembacaan ke server Jakarta. Hasilnya, saldo terbaru sebesar 70000.0 berhasil ditampilkan tanpa harus
menunggu proses replikasi selesai.

### Tabel Perbandingan Hasil Simulasi

| Aspek              | Tanpa Read-Your-Writes | Dengan Read-Your-Writes   |
|--------------------|------------------------|---------------------------|
| Saldo terbaru      | 50000.0                | 70000.0                   |
| Saldo yang terbaca | 0.0                    | 70000.0                   |
| Server pembacaan   | Bandung                | Jakarta (redirect)        |
| Kondisi replikasi  | Belum selesai          | Belum selesai             |
| Konsistensi data   | Inconsistent Read      | Read-Your-Writes terjamin |
| Hasil simulasi     | BUG                    | BUG TERATASI              |