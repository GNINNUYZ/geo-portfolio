# 01 - Urban Density (Amsterdam)

Analyses building density per neighbourhood in Amsterdam using GeoPandas.

## Pipeline

1. Load building footprints and neighbourhood boundaries
2. Clean geometries and unify CRS (EPSG:28992)
3. Spatial join buildings to neighbourhoods
4. Compute building coverage ratio per neighbourhood

## Files

- `Amsterdam_architecture_density.py` — main script
- `exploratory_analysis.py` — data exploration
- `data/coverage_map.png`, `data/building_distribution.png` — result maps

## Run

```bash
python Amsterdam_architecture_density.py
```

**Interpreter note:** this script needs `geopandas` + `mapclassify`, which on this machine are
installed in the **Anaconda** environment, **not** in the project's `.venv` (that one is PyTorch-only).
Run it with the Anaconda interpreter:

```powershell
& 'D:\Users\Administration\anaconda3\python.exe' Amsterdam_architecture_density.py
```

`plt.show()` blocks when run from a terminal — set `MPLBACKEND=Agg` to run headless.

## Output

- `data/coverage_status.csv`
- `data/Amsterdam_architecture_density.geojson`
- PNG result maps

## Three classification schemes compared

`data/Amsterdam_arch_density.png` shows the **same** `cover_ratio` data classified three ways
(数据：111 个街区，`cover_ratio` 范围 0 – 0.00662，均值 0.00078，中位数 0，
51.4% 为零值，偏度 2.04、峰度 5.23):

| panel | scheme | class breaks | neighbourhoods per class |
|---|---|---|---|
| left | `equal_interval` | 0.00221 / 0.00441 | 96 / 13 / 2 |
| middle | `quantiles` | 0.0 / 0.00082 | 57 / 17 / 37 |
| right | `natural_breaks` | 0.00093 / 0.00275 | 76 / 28 / 7 |

Pairwise，分档不同的街区占比：`equal_interval` vs `quantiles` **46.8%**，
`quantiles` vs `natural_breaks` **42.3%**，`equal_interval` vs `natural_breaks` **22.5%**。

差异集中在最高密度档：三种方案分别只有 **2 / 37 / 7** 个街区落入最高档。
等距表示绝对量/分位看各自相对排名/自然断点看数据结构
