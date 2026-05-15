# Snake Pathfinding — Perbandingan BFS vs DFS

**Mata kuliah:** Desain & Analisis Algoritma (DAA) — Quiz 2  
**Bahasa:** Python 3  
**Antarmuka:** Pygame (visualisasi game) + terminal (menu & laporan eksperimen)

---

## Ringkasan proyek

Proyek ini adalah **game Snake otomatis** di mana ular bergerak sendiri menuju makanan dengan bantuan algoritma pencarian jalur. Kami membandingkan dua algoritma dari materi kuliah:

| Algoritma | Peran dalam game |
|-----------|------------------|
| **BFS** (Breadth-First Search) | Mencari jalur ke makanan; pada graf tak berbobot menghasilkan **jalur terpendek** (langkah minimum). |
| **DFS** (Depth-First Search) | Mencari jalur ke makanan dengan eksplorasi **mendalam**; tidak menjamin jalur terpendek. |

Peta permainan dimodelkan sebagai **graf grid**: setiap sel = simpul, gerakan atas/bawah/kiri/kanan = tepi (jika tidak terhalang dinding, rintangan, atau tubuh ular).

Tujuan eksperimen: melihat perbedaan **skor (makanan)**, **jumlah langkah**, **waktu keputusan pathfinding**, dan **jumlah node diekspansi** antara BFS dan DFS pada level kesulitan yang sama.

---

## Kesesuaian dengan instruksi Quiz 2

| Persyaratan | Pemenuhan |
|-------------|-----------|
| Program kelompok (game) | Game Snake dengan rintangan statis & dinamis |
| Minimal satu algoritma kuliah | **BFS** dan **DFS** untuk pathfinding |
| Bahasa bebas | Python |

---

## Anggota kelompok

| Nama | NIM | Kontribusi |
|------|-----|------------|
| *Jorell Ramos Sinaga* | *5025241202* | *BFS & DFS (find_path_bfs, find_path_dfs), replanning di run_simulation, metrik waktu & node ekspansi, tabel perbandingan BFS vs DFS* |
| *Angela Vania Sugiyono* | *5025241226* | *SnakeGame (gerak, makanan, tabrakan), layout level, Pygame, README, video demo, push ke GitHub* |


---

## Cara menjalankan

### Prasyarat

- Python 3.10+ (diuji dengan Python 3.13)
- Windows / Linux / macOS

### Instalasi

```bash
cd quiz2
pip install -r requirements.txt
```

### Menjalankan program

```bash
python main.py
```

1. Pilih level: **Easy** / **Medium** / **Hard**
2. Program menjalankan **5 simulasi BFS** lalu **5 simulasi DFS** (total 10 run per batch)
3. Setiap run membuka **jendela Pygame**; ular bergerak otomatis mengikuti jalur dari algoritma
4. Setelah selesai, terminal menampilkan **tabel perbandingan** BFS vs DFS
5. Jawab `y` / `n` jika ingin mengulang batch dengan level yang sama

---

## Alur program (alur kerja)

```
Input level (terminal)
    → 5× run_simulation(..., "BFS")
    → 5× run_simulation(..., "DFS")
    → print_comparison()  (tabel rata-rata)
    → append hasil ke snake_experiment_log.csv
    → tanya lanjut batch? (y/n)
```

Pada setiap langkah game:

1. Jika tidak ada jalur tersisa di antrian → **replan**: panggil BFS atau DFS dari kepala ular ke posisi makanan
2. Jalur disimpan di antrian langkah; ular bergerak satu sel per frame
3. Jika makanan dimakan / rintangan dinamis muncul → kondisi berubah → **replan** lagi
4. Game berakhir jika: tabrakan, terjebak (no path), atau batas **1000 langkah**

---

## Level kesulitan

| Level | Ukuran grid | Rintangan statis | Rintangan dinamis |
|-------|-------------|------------------|-------------------|
| **Easy** | 15×15 | Tidak ada | Tidak ada |
| **Medium** | 20×20 | Dua pilar vertikal | Setelah 7 makanan: spawn 1–2 rintangan acak |
| **Hard** | 25×25 | Bentuk plus (+) | Setelah 5 makanan: spawn 1–5 rintangan acak |

**Legenda warna (Pygame):**

- Hijau — ular | Merah — makanan  
- Abu gelap — rintangan statis | Abu terang — rintangan dinamis  

---

## Metrik yang dicatat

| Metrik | Arti |
|--------|------|
| **Total Food** | Banyak makanan yang dimakan (skor) |
| **Total Steps** | Langkah sampai game over (maks. 1000) |
| **Average Time (ms)** | Rata-rata waktu CPU per keputusan pathfinding |
| **Average Expansion** | Rata-rata node yang diekspansi per replan |
| **Replans** | Berapa kali pathfinding dijalankan ulang |
| **Game Over Reason** | Penyebab berakhir (mis. trapped, step limit, tabrakan) |

Hasil tiap run ditambahkan ke file **`snake_experiment_log.csv`** untuk dokumentasi dan analisis lanjut.

---

## Contoh output terminal

```
Pilih Level Eksperimen (Easy/Medium/Hard): Medium

==============================
Menjalankan Batch (Level: Medium)
==============================
Menjalankan 5x BFS...
  [BFS Run 1/5]... Selesai. Makanan: 40  | Langkah: 714  | Alasan: No Path Found (Trapped)
  ...

Menjalankan 5x DFS...
  [DFS Run 1/5]... Selesai. Makanan: 13  | Langkah: 1000 | Alasan: Step Limit Reached
  ...

==============================================================
                 HASIL PERBANDINGAN BFS vs DFS
==============================================================
  Metrik                        BFS        DFS     Pemenang
  ...
  >>> PEMENANG BATCH INI: *** BFS *** (3/4 kategori)
```

**Catatan interpretasi:** hasil bisa berbeda tiap batch karena penempatan makanan dan rintangan dinamis **acak**. BFS cenderung unggul pada makanan dan langkah karena jalur ke makanan lebih pendek; DFS sering memakan lebih banyak langkah sebelum mencapai batas 1000.

---

## Struktur file

```
quiz2/
├── main.py                      # Seluruh logika: game, BFS, DFS, simulasi, UI
├── requirements.txt             # Dependensi Python
├── README.md                    # Dokumentasi ini
├── daa_snake.mp4                # Video demo gameplay & eksperimen
└── snake_experiment_log.csv     # Log hasil run (dibuat otomatis)
```

### Bagian penting di `main.py`

| Bagian | Baris (perkiraan) | Fungsi |
|--------|-------------------|--------|
| `SnakeGame` | 26–134 | State game, gerak, rintangan, tetangga valid |
| `find_path_bfs` | 139–160 | Implementasi BFS |
| `find_path_dfs` | 163–184 | Implementasi DFS |
| `run_simulation` | 225–334 | Loop Pygame + replanning |
| `print_comparison` | 337–386 | Tabel perbandingan batch |

---

## Algoritma (ringkas)

**Graf:** Grid 4-arah; simpul = sel kosong atau sel yang boleh dilewati (termasuk ekor saat ular bergerak).

**BFS:** Antrian `deque`, kunjungi per level → jalur pertama ke makanan = jalur terpendek (dalam jumlah langkah).

**DFS:** Stack (LIFO), kunjungi dalam-dulu → jalur ditemukan bisa lebih panjang.

Kedua algoritma menghitung **jumlah node yang diekspansi** untuk membandingkan beban komputasi per replan.

---

## Demo video

Cuplikan gameplay dan batch eksperimen BFS vs DFS:

<video src="./daa_quiz2.mp4" controls="controls" style="max-width: 100%;">
</video>

Video menampilkan jendela Pygame (ular, makanan, rintangan) serta alur menjalankan simulasi hingga tabel perbandingan di terminal.

---
