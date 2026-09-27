# Catatan Git Pull dan Pull Request

Sebelum mulai memperbaiki atau menambahkan tugas, selalu ambil perubahan terbaru dari branch `main`.

## 1. Update Branch Sebelum Mengerjakan

Pastikan sedang berada di branch masing-masing.

```bash
git branch
```

Kemudian ambil perubahan terbaru dari `main`:

```bash
git pull origin main
```

Setelah itu baru mulai mengedit file.

Tujuannya supaya branch masing-masing tidak tertinggal dari perubahan anggota lain yang sudah masuk ke `main`.

---

## 2. Setelah Selesai Mengerjakan

Commit perubahan seperti biasa.

```bash
git add .
git commit -m "[Update] Tugas-02: memperbarui diagram arsitektur"
git push origin Nama-Branch
```

Contoh:

```bash
git push origin Rovino-Ramadhani
```

---

## 3. Mengumpulkan Pekerjaan ke Branch `main`

Setelah perubahan sudah selesai dan sudah di-push:

1. Buka repository kelompok di GitHub.
2. Masuk ke tab `Pull requests`.
3. Klik `New pull request`.
4. Periksa repository sebelum membuat Pull Request.

Karena repository ini merupakan hasil fork, jangan sampai Pull Request diarahkan ke repository milik dosen.

Pastikan konfigurasi seperti berikut:

```text id="o5mxql"
base repository:
rovinoramadhani/komputasi-awan-dan-terdistribusi

base:
main

head repository:
rovinoramadhani/komputasi-awan-dan-terdistribusi

compare:
Nama-Branch
```

Contoh:

```text id="z3qnbh"
base repository:
rovinoramadhani/komputasi-awan-dan-terdistribusi

base:
main

compare:
Rovino-Ramadhani
```

Artinya:

```text id="zd0p58"
Rovino-Ramadhani
        ↓
       main
```

Bukan:

```text id="96dbwg"
Fork Kelompok
      ↓
Repository Dosen
```

---

## 4. Sebelum Klik Create Pull Request

Periksa kembali:

```text id="clmsnd"
base repository = repository kelompok
base            = main
compare         = branch kalian
```

Jika `base repository` menunjukkan repository milik dosen, jangan lanjutkan.

Ganti terlebih dahulu ke repository kelompok.

---

## 5. Setelah Pull Request Dibuat

Gunakan format title:

```text id="l67i7m"
[Submit] Tugas-02: Perancangan Arsitektur - Nama Anggota
```

Setelah diperiksa dan tidak ada konflik, Pull Request dapat di-merge ke:

```text id="3p43an"
main
```

Setelah PR berhasil di-merge, anggota lain yang ingin melanjutkan pekerjaan harus menjalankan lagi:

```bash
git pull origin main
```

Jadi alur kerja kelompoknya:

```text id="uy4e4v"
git pull origin main
        ↓
Kerjakan tugas
        ↓
git add .
        ↓
git commit
        ↓
git push origin Nama-Branch
        ↓
Pull Request
        ↓
Branch anggota → main
        ↓
Merge
        ↓
Anggota lain git pull origin main
```

## Catatan Penting

Setiap sebelum mulai mengerjakan tugas atau revisi:

```bash
git pull origin main
```

Setiap setelah selesai:

```text id="16e4eg"
Commit → Push Branch → Pull Request → Merge ke main
```

Jangan melakukan Pull Request ke repository asli milik dosen.

# Git Commit & Pull Request Convention

## 1. Format Commit

```text
[Status] Tugas-XX: deskripsi singkat perubahan
```

Status yang digunakan:

```text
[Add]       Menambahkan file, bagian, diagram, atau fitur baru
[Update]    Memperbarui isi yang sudah ada
[Fix]       Memperbaiki kesalahan
[Remove]    Menghapus file atau bagian yang tidak digunakan
[Docs]      Perubahan dokumentasi, README, atau JURNAL
[Refactor]  Merapikan struktur tanpa mengubah isi utama
```

Contoh:

```text
[Add] Tugas-02: menambahkan diagram arsitektur Publish-Subscribe

[Update] Tugas-02: memperbarui penjelasan alur komunikasi modul

[Fix] Tugas-02: memperbaiki arah komunikasi pada diagram arsitektur

[Docs] Tugas-02: memperbarui JURNAL pengerjaan

[Remove] Tugas-02: menghapus diagram versi lama
```

Hindari commit seperti:

```text
update
revisi
fix
tugas 2
update terbaru
final
final fix
final beneran
```

---

## 2. Format Pull Request Title

```text
[Status] Tugas-XX: ringkasan perubahan
```

Contoh:

```text
[Add] Tugas-02: Perancangan Arsitektur Publish-Subscribe

[Update] Tugas-02: Penyempurnaan Diagram dan Analisis Arsitektur

[Fix] Tugas-02: Perbaikan Diagram Komunikasi Antar Modul
```

Untuk PR yang berisi pekerjaan utama satu anggota, gunakan:

```text
[Submit] Tugas-02: Perancangan Arsitektur - Rovino Ramadhani
```

---

## 3. Template Pull Request Description

```markdown
## Informasi

Nama:
Tugas:
Branch:

## Ringkasan Perubahan

Jelaskan secara singkat pekerjaan yang dilakukan pada Pull Request ini.

## Perubahan

1.
2.
3.

## File yang Diubah

1. `path/file`
2. `path/file`

## Checklist

1. [ ] Pekerjaan sudah sesuai bagian yang diberikan.
2. [ ] File ditempatkan pada folder tugas yang benar.
3. [ ] Tidak mengubah pekerjaan anggota lain tanpa koordinasi.
4. [ ] Sudah melakukan pull dari branch `main` terbaru.
5. [ ] Tidak terdapat konflik sebelum dilakukan merge.
```

## 4. Contoh Pull Request

Title:

```text
[Add] Tugas-02: Perancangan Arsitektur Publish-Subscribe
```

Description:

```markdown
## Informasi

Nama: Rovino Ramadhani
Tugas: Tugas 02 - Perancangan Arsitektur
Branch: Rovino-Ramadhani

## Ringkasan Perubahan

Menambahkan hasil perancangan arsitektur Publish-Subscribe untuk studi kasus FoodGo beserta diagram dan penjelasan
komunikasi antar modul.

## Perubahan

1. Menambahkan diagram arsitektur Publish-Subscribe.
2. Menambahkan penjelasan komunikasi sinkron dan asinkron.
3. Memperbarui dokumentasi hasil pengerjaan.

## File yang Diubah

1. `tugas-02-perancangan-arsitektur/diagram/...`
2. `tugas-02-perancangan-arsitektur/susunan/...`

## Checklist

1. [x] Pekerjaan sudah sesuai bagian yang diberikan.
2. [x] File ditempatkan pada folder tugas yang benar.
3. [x] Tidak mengubah pekerjaan anggota lain tanpa koordinasi.
4. [x] Sudah melakukan pull dari branch `main` terbaru.
5. [x] Tidak terdapat konflik sebelum dilakukan merge.
```