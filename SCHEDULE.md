# GeoBIM 16-Week Parallel Tracks — 完整计划

**Start:** 2026-06-28 (Sunday→周一)　**Phase 1 End:** 2026-10-17 (Saturday)
**Work rhythm:** Mon-Fri 6h/day = Project 3h (morning) + Learning 2h (afternoon) + Integration 1h (evening). Sat buffer. Sun rest.
**Phase 2 (Application):** 2026-10-18 – 2026-12-31

---

## 两条并行的线

```
Week    📚 学习线 (Learning Track)              🔧 项目线 (Project Track)
        TU Delft 课程 + 教材 + 作业              输入 → 处理 → 产出

1-2     GEO1000: Think Python + Python for Eng    ──（练习积累）──▶
3-4     GEO1002: GIS & Cartography              ────────────────▶ P1 城市密度分析
5-6     GEO1004: 3D Modelling (B-rep/拓扑)       ────────────────▶ P2 Half-edge 引擎
7-8     GEO1015: Digital Terrain Modelling       ────────────────▶ P3 地形管线
        GEO1001: Sensing (LiDAR)
9-10    GEO1004: 3D Modelling (CityGML/语义)     ────────────────▶ P4 CityJSON 城市模型
11-12   GEO1004: 3D Modelling (BIM/IFC)          ────────────────▶ P5 IFC→CityJSON
        GEO1006: Geo Database
13-14   GEO1007: Geo Web & 3D Viz                ────────────────▶ P6 Web 平台
15-16   GEO1008: Data Quality                    ────────────────▶ 整合 + 文档
        GEO1009: Organisation
```

每一步学习的内容**当天就进入项目**。不是先学完再做——是学着做着。

---

## TU Delft 课程覆盖矩阵

| 课程代码 | 课程名 | EC | 教材/资源 | 在哪周 | 覆盖度 |
|---------|--------|-----|----------|--------|--------|
| **GEO1000** | Python Programming | 5 | Think Python 2e + Python for Engineers (Jupyter Book) | W1-2 | 100% |
| **GEO1002** | GIS & Cartography | 5 | GeoPandas + Rasterio + GDAL 官方文档 | W3-4 | 90% |
| **GEO1004** | 3D Modelling | 5 | 3Dbook (open textbook) + CityJSON spec + IFC docs | W5-6, W9-12 | 95% |
| **GEO1015** | Digital Terrain Modelling | 5 | Computational Modelling of Terrains (open textbook, Hugo Ledoux) | W7-8 | 90% |
| **GEO1001** | Sensing Technologies | 5 | PDAL docs + AHN data processing | W7-8 | 60% |
| **GEO1006** | Geo Database | 5 | PostgreSQL + PostGIS 官方文档 | W11-12 | 85% |
| **GEO1007** | Geo Web & 3D Viz | 5 | CesiumJS + FastAPI | W13-14 | 80% |
| **GEO1008** | Data Quality | 5 | ISO 19157 + cjio validate | W15-16 | 30% |
| **GEO1009** | Organisation & Legislation | 5 | INSPIRE directive + GDPR | W15-16 | 20% |
| GEO1003 | Positioning | 5 | — | — | 10%（仅 CRS 部分） |
| GEO1005 | Spatial Decision Support | 5 | — | — | 0% |

> 70% 的技术课程被深度覆盖。GEO1003/GEO1005/GEO1009 的缺口在动机信里主动提及"计划在硕士期间系统学习"。

---

# 周计划：双线并行

---

## Week 1: Python 基础 (Jun 29 – Jul 5)

### 📚 学习线 — GEO1000: Think Python

| 天 | 章节 | 内容 | 练习 |
|----|------|------|------|
| **Mon** | Ch1-5 | 变量、表达式、条件、函数、递归 | Jupyter Book Ch1-5 习题 |
| **Tue** | Ch6-8 | 迭代、字符串、列表 | CodingBat warmup |
| **Wed** | Ch9-12 | 字典、元组、文件读写 | Jupyter Book Ch9-12 习题 |
| **Thu** | Ch15-17 | 类与对象、方法、__init__、继承 | 写一个 Point 类、一个 Polygon 类 |
| **Fri** | Ch18-19 | 继承、多态、dunder methods | 写一个 GeoDataFrame 的简化版骨架 |
| **Sat** | 复习 | 补漏 + Python for Engineers 里没做完的题 | — |

**教材链接:**
- Think Python 2e: `https://greenteapress.com/wp/think-python-2e/`
- Python for Engineers (TU Delft 定制版): `https://oit.tudelft.nl/learn-python/2025/`

### 🔧 项目线 — 预习阶段（无独立项目）

| 天 | 任务 | 与学习线的连接 |
|----|------|--------------|
| **Mon-Wed** | 写一堆小脚本：list comprehension、dict 分组、文件读写 | Think Python Ch1-12 直接应用 |
| **Thu** | `class Point:` 带 x,y, distance_to(), __repr__ | 对应 Ch15-17 → 为 W2 的 Shapely 做铺垫 |
| **Fri** | `class Polygon:` 从点列表构造，算面积（shoelace formula） | 对应 Ch18-19 → 为 W4 的 building footprint 处理做铺垫 |
| **Sat** | 把一周写的零散代码整理成 `utils.py` | 版本控制起步 |

### 🔗 本周连线

```
Think Python → Point/Polygon class → Shapely 替代品（理解内部原理）
OOP 类设计     → 项目二 Half-edge 数据结构的类层次（远眺）
```

---

## Week 2: NumPy + Shapely + CRS (Jul 6 – Jul 12)

### 📚 学习线 — GEO1002 前段

| 天 | 主题 | 教材 | 练习 |
|----|------|------|------|
| **Mon** | NumPy 基础：ndarray、broadcasting、ufunc | NumPy Quickstart Tutorial | 100 道 NumPy 练习 |
| **Tue** | NumPy 进阶：花式索引、axis 概念、向量化思维 | From Python to NumPy (online book) | 用 NumPy 重写 Week1 的面积计算（批量） |
| **Wed** | Shapely: Point, LineString, Polygon, Multi*, buffer, union, intersection | Shapely 官方文档 | 创建几何、空间关系判断 |
| **Thu** | CRS 理论：地理 vs 投影坐标系、大地基准面、EPSG | pyproj 文档 + EPSG.io | pyproj.Transformer 实战 |
| **Fri** | pyproj: Transformer, CRS 对象, 坐标转换管线 | PROJ 文档 | 把 WGS84 → EPSG:28992 (荷兰 RD New) |
| **Sat** | 综合练习 | — | Shapely 几何 + pyproj 转换 + NumPy 批量 |

### 🔧 项目线 — 继续预习

| 天 | 任务 | 连接 |
|----|------|------|
| **Mon-Tue** | NumPy 向量化批量计算：10000 个建筑的覆盖率（模拟数据） | 为 P1 聚合做准备 |
| **Wed-Thu** | Shapely 读取 WKT、创建多边形、计算面积和 buffer | 为 P1 的空间操作做准备 |
| **Fri** | pyproj 把阿姆斯特丹坐标从 WGS84 转到 RD New | 为 P1 数据对齐做准备 |

### 🔗 本周连线

```
NumPy 向量化      → P1 按街区聚合计算（不用 for 循环）
Shapely 几何操作   → P1 建筑覆盖面积计算
pyproj CRS 转换    → P1 数据源 CRS 对齐（BAG + CBS 可能不同）
```

---

## Week 3: GeoPandas + Rasterio (Jul 13 – Jul 19)

### 📚 学习线 — GEO1002 后段

| 天 | 主题 | 教材 | 练习 |
|----|------|------|------|
| **Mon** | GeoPandas: read_file(), GeoDataFrame, CRS 管理 | GeoPandas Getting Started | 读 BAG Shapefile，探索数据 |
| **Tue** | GeoPandas: 空间查询、predicate (contains/within/intersects) | GeoPandas 官方教程 | 找出某街区内所有建筑 |
| **Wed** | GeoPandas: sjoin(), overlay(), dissolve() | 同上 | 空间连接两个图层 |
| **Thu** | Rasterio: open(), read(), transform, CRS, 波段 | Rasterio Quickstart | 读 AHN DEM 切片，查看元数据 |
| **Fri** | Rasterio: 波段运算, 重采样, 窗口读取, reprojection | Rasterio 进阶 | 裁剪 DEM 到研究区范围 |
| **Sat** | GDAL/OGR: 底层 API 概览 | GDAL Python 绑定 | ogr.Open, GetLayer, Feature 遍历 |

### 🔧 项目线 — P1 数据准备开始

| 天 | 任务 | 连接 |
|----|------|------|
| **Mon** | 下载 BAG 建筑足迹 (Amsterdam) + CBS 街区边界 | 数据获取 |
| **Tue** | GeoPandas 读入，检查 CRS、列名、几何类型 | 对应学习线 Mon-Tue |
| **Wed** | 清理：剔除空几何、无效几何、非多边形 | Shapely is_valid, buffer(0) trick |
| **Thu** | Rasterio 预览 AHN4 DEM 切片（阿姆斯特丹） | 对应学习线 Thu |
| **Fri** | 探索性分析：街区大小分布、建筑面积分布、数据量 | matplotlib 直方图 |

### 🔗 本周连线

```
GeoPandas sjoin  → P1 核心操作：建筑归属到街区
Rasterio 读写    → P3 DEM 生成（远眺）
GDAL/OGR 底层    → P3 .laz → .tif 管线的底层控制
```

---

## Week 4: Project 1 — 城市建筑密度分析 (Jul 20 – Jul 26)

### 📚 学习线 — GEO1002 收尾 + 制图

| 天 | 主题 | 教材 |
|----|------|------|
| **Mon** | Matplotlib 进阶：subplot、colorbar、custom colormap | Matplotlib 官方教程 |
| **Tue** | 专题图设计：分类方法（等间隔/分位数/自然断点）、配色 | ColorBrewer 2.0 |
| **Wed** | Fiona: 写 Shapefile/GeoJSON | Fiona 文档 |
| **Thu** | 空间统计基础：Global Moran's I, LISA | PySAL 入门 |
| **Fri** | 复习 + 文档写作 | — |

### 🔧 项目线 — P1 完整管线

**技术路线（详细步骤）：**

```
Step 1: 数据加载与 CRS 对齐
─────────────────────────────
buildings = gpd.read_file("bag_pand_amsterdam.shp")
neighborhoods = gpd.read_file("cbs_wijk_2024.shp")
# 确保两者都是 EPSG:28992 (RD New)
buildings = buildings.to_crs("EPSG:28992")
neighborhoods = neighborhoods.to_crs("EPSG:28992")

Step 2: 面积计算
────────────────
buildings["area"] = buildings.geometry.area
neighborhoods["nb_area"] = neighborhoods.geometry.area

Step 3: 空间连接
────────────────
# 每个建筑属于哪个街区
joined = gpd.sjoin(buildings, neighborhoods, predicate="within")

Step 4: 聚合
────────────────
agg = joined.groupby("wijk_code").agg(
    building_area_sum=("area", "sum"),
    building_count=("area", "count")
).reset_index()
result = neighborhoods.merge(agg, on="wijk_code", how="left")
result["coverage_ratio"] = result["building_area_sum"] / result["nb_area"]
result["coverage_ratio"] = result["coverage_ratio"].fillna(0)

Step 5: 分级着色
────────────────
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
result.plot(
    column="coverage_ratio",
    scheme="quantiles", k=7,
    cmap="YlOrRd",
    legend=True,
    legend_kwds={"title": "建筑覆盖率"},
    edgecolor="grey", linewidth=0.3,
    ax=ax
)
ax.set_title("Amsterdam Building Coverage Ratio per Neighborhood", fontsize=14)
ax.set_axis_off()

Step 6: 导出
────────────────
result.to_file("amsterdam_building_coverage.geojson", driver="GeoJSON")
plt.savefig("amsterdam_coverage.png", dpi=300, bbox_inches="tight")
```

| 天 | 任务 | 产出 |
|----|------|------|
| **Mon** | 数据加载 + CRS 对齐 + 数据清洗 | `buildings_clean.gpkg` |
| **Tue** | 空间连接 + 聚合计算 | `coverage_stats.csv` |
| **Wed** | 可视化：分级着色 + 图例 + 排版 | `coverage_map.png` |
| **Thu** | 空间自相关分析（Moran's I） | 统计分析段落 |
| **Fri** | README + 导出 GeoJSON + 提交 | P1 完成 |
| **Sat** | Buffer: 复盘 + 修复 | — |

### 🔗 本周连线

```
GeoPandas sjoin + groupby → P1 管线脊骨
Matplotlib 分级着色        → 最终产出可视化
Fiona/GeoJSON 导出         → P4 CityJSON 的数据源（建筑 footprint + 属性）
PySAL Moran's I            → 进阶分析（可选，加分）
```

**🏁 P1 完成。产出:** `amsterdam_coverage.png` + `analysis.py` + GeoJSON.

---

## Week 5: 3D 数据结构 — Half-edge (Jul 27 – Aug 2)

### 📚 学习线 — GEO1004: 3D Modelling (Week 1/2)

**教材:** 3Dbook (open textbook), 对应 GEO1004 Q2 课程。

| 天 | 章节 | 内容 | 练习 |
|----|------|------|------|
| **Mon** | 3Dbook Ch1 | 3D 建模概念：B-rep、CSG、扫掠、体素。几何 vs 拓扑 | 概念图：用纸笔画出立方体的 B-rep 表示 |
| **Tue** | 3Dbook Ch2 | B-rep 深入：面、边、顶点、邻接关系。Euler-Poincaré 公式 V-E+F=2 | 验证不同多面体 |
| **Wed** | 3Dbook Ch2 续 | Half-edge 数据结构：为什么需要半边。next/prev/twin/origin/face 五指针设计 | 在白板上遍历一个四面体的所有半边 |
| **Thu** | 3Dbook Ch3 | Delaunay 三角剖分、Voronoi 图 | `scipy.spatial.Delaunay` 跑一组 2D 点，画出 TIN |
| **Fri** | 3Dbook Ch4 | 体素化：Mesh → Voxel Grid | 用 `trimesh` 加载 OBJ，手写一个简单体素化 |

**GEO1004 作业思路（参考）：**
- HW1: 手工构建一个简单网格的半边结构（纸笔 → 代码）
- HW2: 实现从 OBJ 构建半边的算法

### 🔧 项目线 — P2: Half-edge 网格引擎

**技术路线：**

```
数据结构设计（5 个核心类）：

┌──────────────────────────────────────┐
│  Mesh                                 │
│    .vertices   : list[Vertex]         │
│    .faces      : list[Face]           │
│    .halfedges  : list[HalfEdge]       │
│                                        │
│  方法：                                │
│    build_from_obj(path) → Mesh        │
│    to_obj(mesh, path)                 │
│    is_valid(mesh) → bool              │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│  Vertex                               │
│    .x, .y, .z  : float               │
│    .halfedge   : HalfEdge  # 任意外出半边│
│                                        │
│  方法：                                │
│    vertex_edges(v) → list[HalfEdge]   │
│    vertex_faces(v) → list[Face]       │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│  Face                                 │
│    .halfedge   : HalfEdge  # 面内任意半边│
│                                        │
│  方法：                                │
│    face_vertices(f) → list[Vertex]    │
│    adjacent_faces(f) → list[Face]     │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│  HalfEdge                             │
│    .origin   : Vertex                 │
│    .twin     : HalfEdge | None        │
│    .next     : HalfEdge               │
│    .prev     : HalfEdge               │
│    .face     : Face                   │
└──────────────────────────────────────┘
```

**build_from_obj 算法（核心）：**

```
输入：OBJ 文件路径
输出：Mesh 对象

1. 解析 OBJ：
   - 读 v 行 → 创建 Vertex 列表
   - 读 f 行 → 每面是一组顶点索引

2. 为每个面的每条边创建 HalfEdge：
   for face_verts in faces:
       for i in range(len(face_verts)):
           v_i = face_verts[i]
           v_j = face_verts[(i+1) % len(face_verts)]
           he = HalfEdge(origin=v_i)
           he.face = current_face
           # 链表连接
           prev_he.next = he
           he.prev = prev_he

3. 找 twin（最难步骤）：
   - 建字典 edge_map[(v_start, v_end)] = halfedge
   - 遍历所有半边：如果 (v_end, v_start) 在 map 里 → 配对 twin
   - 找不到 → twin = None → 边界边

4. 设置顶点到半边的引用：
   for he in halfedges:
       if he.origin.halfedge is None:
           he.origin.halfedge = he
```

| 天 | 任务 | 产出 |
|----|------|------|
| **Mon** | 阅读 3Dbook Ch1-2，画 B-rep 图 | 理解笔记 |
| **Tue** | 设计类接口（Vertex, Face, HalfEdge, Mesh） | `halfedge.py` 骨架 |
| **Wed** | 实现 __init__ 和基础属性 | 类定义完成 |
| **Thu** | 实现 build_from_obj 第1-2步（解析 + 创建半边） | 单向半边列表 |
| **Fri** | 实现 twin 配对算法（edge_map 字典） | 完整半边结构 |
| **Sat** | 测试：cube.obj, tetrahedron.obj | 验证拓扑正确性 |

### 🔗 本周连线

```
3Dbook Ch2 B-rep 理论 → HalfEdge 类的 5 个指针设计
Delaunay 三角剖分       → P3 构建 TIN 的理论基础
体素化                  → 为 P6 的 3D Tiles 理解空间划分
```

---

## Week 6: Half-edge 完成 + 更多 3D 结构 (Aug 3 – Aug 9)

### 📚 学习线 — GEO1004: 3D Modelling (Week 2/2)

| 天 | 章节 | 内容 | 练习 |
|----|------|------|------|
| **Mon** | 3Dbook Ch5 | CSG (Constructive Solid Geometry) + Nef 多面体 | pycsg 或手写简单布尔运算（并、交、差） |
| **Tue** | 3Dbook Ch6 | 曲线曲面：Bezier, B-spline, NURBS | matplotlib 画 Bezier 曲线（de Casteljau 算法） |
| **Wed** | 3Dbook Ch7 | MAT (Medial Axis Transform), 骨架化 | `skimage.morphology.skeletonize_3d` 示例 |
| **Thu** | 3Dbook Ch8 | G-map (Generalized Map), dart 结构 | 概念理解（不要求实现） |
| **Fri** | 复习 GEO1004 | 回看 Ch1-8 笔记，总结 B-rep/CSG/体素/NURBS 四类表示法的优劣 |

### 🔧 项目线 — P2 完成

| 天 | 任务 | 产出 |
|----|------|------|
| **Mon** | 实现 face_vertices(face): 沿 he.next 走一圈收集顶点 | 面遍历 |
| **Tue** | 实现 adjacent_faces(face): he.twin.face（过滤 None） | 邻接查询 |
| **Wed** | 实现 boundary_edges(mesh): he.twin is None | 边界检测 |
| **Thu** | 实现 is_2_manifold(mesh): 每个顶点的面构成一个环 | 流形检查 |
| **Fri** | 实现 to_obj(mesh, path): 顶点编号 + 面索引输出 | 导出 |
| **Sat** | 全面测试 + 文档 + README | P2 完成 |

### 🔗 本周连线

```
CSG 布尔运算 → P5 IFC 构件之间的空间关系理解
Bezier/B-spline → 理解 IFC 里 IfcRationalBSplineSurface 等高级几何
G-map → 拓展现有 Half-edge 的替代方案认知
```

**🏁 P2 完成。产出:** `halfedge.py` (~300-500 行) + 测试用例 + README.

---

## Week 7: 数字地形建模理论 (Aug 10 – Aug 16)

### 📚 学习线 — GEO1015: Digital Terrain Modelling (Week 1/2)

**教材:** [Computational Modelling of Terrains](https://tudelft3d.github.io/terrainbook/) (Hugo Ledoux, open textbook)

**对应 TU Delft GEO1015 课程：5 EC, Q2/Q4 开设，教师 Hugo Ledoux**

| 天 | 章节 | 内容 | 对应 GEO1015 作业 |
|----|------|------|-------------------|
| **Mon** | Ch1 | 什么是地形。采集方法：LiDAR、摄影测量、卫星 | — |
| **Tue** | Ch2 | TIN + Voronoi 图。Delaunay 三角剖分的性质（空圆、最大化最小角） | HW1: TIN + Voronoi |
| **Wed** | Ch3 | 空间插值 (1/2): IDW, 线性在 TIN 中, Natural Neighbour | HW1 续: 实现线性 TIN 插值 |
| **Thu** | Ch4 | 空间插值 (2/2): Kriging (半变异函数、普通克里金) | HW1 续: pykrige 实验 |
| **Fri** | Ch5 | 地形属性：坡度、坡向、山体阴影、曲率 | HW3 前段 |

**GEO1015 核心作业（参考 2024）：**
- **HW1:** TIN 构建 + Voronoi 图 + 空间插值（IDW, 线性TIN, Natural Neighbour）
- **HW2:** 从 AHN4 构建 DTM（实现 ground filtering: GFTIN）
- **HW3:** 格网 DTM 处理（坡度、坡向、山体阴影、等值线）

### 🔧 项目线 — P3 准备阶段

| 天 | 任务 | 连接 |
|----|------|------|
| **Mon** | 下载 AHN4 .laz 切片（Delft 区域 2×2 km） | PDOK AHN4 下载 |
| **Tue** | `scipy.spatial.Delaunay` 在样本点上构建 TIN | 对应 GEO1015 Ch2 |
| **Wed** | 实现线性 TIN 插值：点在哪个三角形 → 重心坐标 → 高程 | 对应 GEO1015 HW1 |
| **Thu** | pykrige 实验：普通克里金插值 | 对应 GEO1015 Ch4 |
| **Fri** | PDAL 安装 + 基础 pipeline: `readers.las → writers.las` | 对应 GEO1015 Ch1 |

### 🔗 本周连线

```
GEO1015 Ch2 TIN      → P3 地形重建的数学基础
GEO1015 Ch3 插值     → P3 DEM 生成的核心算法
GEO1015 Ch4 Kriging  → P3 可选的统计插值方案
PDAL pipeline        → P3 点云处理的工程工具
```

---

## Week 8: 地形建模 — 点云到 DEM (Aug 17 – Aug 23)

### 📚 学习线 — GEO1015 (Week 2/2) + GEO1001 传感

| 天 | 章节 | 内容 | 对应 |
|----|------|------|------|
| **Mon** | GEO1015 Ch6 | 地面滤波：GFTIN 算法详解（渐进式 TIN 加密） | HW2 |
| **Tue** | GEO1015 Ch7 | 大规模地形处理：kd-tree、空间索引、out-of-core | — |
| **Wed** | GEO1015 Ch8 | 径流建模：D8 流向、汇流累积、河网提取 | HW3 后段 |
| **Thu** | GEO1001  | LiDAR 物理原理、点云属性（强度、回波、分类） | — |
| **Fri** | GEO1001  | 最小二乘平差概念、粗差检测 | — |

### 🔧 项目线 — P3: 从点云到 DEM

**技术路线（详细步骤）：**

```
Step 1: PDAL 地面滤波管线
────────────────────────────
{
  "pipeline": [
    {"type": "readers.las", "filename": "ahn4_delft.laz"},
    {"type": "filters.outlier", "method": "statistical", "mean_k": 8, "multiplier": 3.0},
    {"type": "filters.smrf", "cell": 1.0, "threshold": 0.5, "scalar": 1.2},
    {"type": "filters.range", "limits": "Classification[2:2]"},
    {"type": "writers.las", "filename": "ground_points.laz"}
  ]
}

Step 2: 加载地面点 → 构建 TIN
────────────────────────────────
import laspy
import numpy as np
from scipy.spatial import Delaunay

las = laspy.read("ground_points.laz")
points = np.vstack([las.x, las.y]).T
z = np.array(las.z)
tri = Delaunay(points)

Step 3: TIN → 格网 DEM (线性插值)
──────────────────────────────────
def tin_to_grid(tri, points, z, resolution=1.0, bounds=None):
    xmin, ymin, xmax, ymax = bounds
    cols = int((xmax - xmin) / resolution)
    rows = int((ymax - ymin) / resolution)
    grid = np.full((rows, cols), np.nan)

    for i in range(rows):
        for j in range(cols):
            x = xmin + j * resolution
            y = ymax - i * resolution
            simplex = tri.find_simplex([x, y])
            if simplex >= 0:
                # 重心坐标插值
                b = tri.transform[simplex, :2].dot([x, y, 1] - tri.transform[simplex, 2])
                b = np.append(b, 1 - b.sum())
                indices = tri.simplices[simplex]
                grid[i, j] = np.dot(b, z[indices])
    return grid, (xmin, ymin, xmax, ymax)

Step 4: 导出 GeoTIFF
─────────────────────
import rasterio
from rasterio.transform import from_origin

transform = from_origin(xmin, ymax, resolution, resolution)
with rasterio.open("dem_delft.tif", "w",
    driver="GTiff", height=rows, width=cols,
    count=1, dtype=grid.dtype, crs="EPSG:28992",
    transform=transform) as dst:
    dst.write(grid, 1)
```

| 天 | 任务 | 产出 |
|----|------|------|
| **Mon** | PDAL pipeline: 统计滤波 + SMRF 地面滤波 | `ground_points.laz` |
| **Tue** | 加载地面点，构建 TIN | `tri` 对象 |
| **Wed** | TIN → 1m 格网 DEM（线性插值）| `dem_array` |
| **Thu** | 导出 GeoTIFF + 山体阴影可视化 | `dem_delft.tif` |
| **Fri** | 验证：与 AHN 官方 DSM/DTM 对比 | 精度报告 |

### 🔗 本周连线

```
GEO1015 Ch6 GFTIN  → SMRF 滤波器的理论依据
GEO1015 Ch3 线性TIN → tin_to_grid 的插值算法
GEO1001 点云属性    → 理解 .laz 里的 Classification/Intensity
```

---

## Week 9: 水文分析 + P3 完成 (Aug 24 – Aug 30)

### 📚 学习线 — GEO1015 收尾

| 天 | 主题 | 教材 |
|----|------|------|
| **Mon** | pysheds: 填洼算法 (FillDepressions)、D8 流向 | pysheds 文档 |
| **Tue** | richdem: 并行填洼、流量累积 | richdem 文档 |
| **Wed** | 河网提取：阈值选择、Strahler 分级 | GEO1015 Ch8 |
| **Thu** | 汇水区划分：pour point 选择、分水岭算法 | GEO1015 Ch8 |
| **Fri** | 复习 GEO1015: 重点回顾插值、滤波、水文 |

### 🔧 项目线 — P3 水文 + 完成

**水文管线（详细步骤）：**

```
Step 5: 填洼 (Pit Filling)
────────────────────────────
import richdem as rd

dem_rd = rd.LoadGDAL("dem_delft.tif")
dem_filled = rd.FillDepressions(dem_rd, epsilon_inf=False, in_place=False)

Step 6: 流向 + 汇流累积
──────────────────────────
flow_dir = rd.FlowDirectionD8(dem_filled)
flow_acc = rd.FlowAccumulation(flow_dir)

Step 7: 河网提取
──────────────────
threshold = flow_acc > 1000  # 汇流面积 > 1000 cells = 1 km²
# 矢量化河网
# 方法：rasterio 读取 → skimage.morphology.skeletonize → gpd
streams = extract_streams(flow_acc, threshold=1000)

Step 8: 汇水区划分
────────────────────
# 选 Delft 附近一个出水口
pour_point = (x, y)
watershed = delineate_watershed(flow_dir, pour_point)
```

| 天 | 任务 | 产出 |
|----|------|------|
| **Mon** | 填洼 + D8 流向 | `dem_filled.tif` |
| **Tue** | 汇流累积 + 河网提取 | 河网栅格 |
| **Wed** | 河网矢量化 → Shapefile | `streams.shp` |
| **Thu** | 汇水区划分 | `watershed.shp` |
| **Fri** | matplotlib/folium 叠加可视化 + README | P3 完成 |

### 🔗 本周连线

```
pysheds/richdem  → P3 水文全流程
GEO1015 全课程   → P3 项目 = GEO1015 作业的工程化版本
```

**🏁 P3 完成。产出:** 一个 Python 脚本 `.laz → DEM → 河网.shp + 汇水区.shp`.

---

## Week 10: 3D 标准 + CityJSON (Aug 31 – Sep 6)

### 📚 学习线 — GEO1004: 3D Modelling (CityGML/CityJSON 部分)

| 天 | 章节 | 内容 | 练习 |
|----|------|------|------|
| **Mon** | 3Dbook Ch9 | ISO 19107 几何原语：GM_Solid, GM_Surface, 有效性规则（封闭、定向、简单） | 手工验证几个 Solid 的有效性 |
| **Tue** | 3Dbook Ch10 | CityGML UML 模型全景：Building, Relief, Transportation, Vegetation, LOD 0-4 | 画出 Building 的 LOD 层次示意 |
| **Wed** | CityJSON 2.0 规范 | 全文通读：CityObjects, geometry templates, semantics, materials | cjio 安装 + validate 示例文件 |
| **Thu** | 3Dbook Ch12 | 3dfier 算法原理：从 2D footprint + 点云自动生成 LoD1.2/1.3 | 理解 extrusion + roof reconstruction |
| **Fri** | 3Dbook Ch13 | 论文泛读：找感兴趣的 3D GIS 方向，做文献笔记 | Zotero 建仓库 |

### 🔧 项目线 — P4: CityJSON 城市模型

**技术路线（详细步骤）：**

```
Step 1: 输入数据准备
─────────────────────
- P1 产出: amsterdam_building_coverage.geojson (建筑 footprint + 高度)
- P3 产出: dem_delft.tif (地形 DEM)
- 补充: 如果没有高度属性，从 AHN DSM 采样

Step 2: 建筑 LOD 1.2 几何生成
───────────────────────────────
def footprint_to_solid(polygon_2d, ground_z, height, roof_type="flat"):
    """
    polygon_2d: Shapely Polygon (2D)
    ground_z:   float (从 DEM 采样的地面高程)
    height:     float (建筑高度)
    roof_type:  "flat" | "skillion" | "gable"
    """
    vertices_3d = []   # [(x0,y0,z0), ...]
    boundaries = []    # [[[v0,v1,v2,v3]], ...]  每个面一个环
    
    # 底面: polygon_2d 所有点 + z = ground_z
    # 顶面: polygon_2d 所有点 + z = ground_z + height
    # 侧面: 每条边成面 (i → i+1 → i+1_top → i_top → i)
    
    if roof_type == "gable":
        # 找最长边 → 添加屋脊线 → 分割顶面
        ...
    elif roof_type == "skillion":
        # 单向倾斜
        ...
    
    return {"vertices": all_vertices, "boundaries": all_faces}

Step 3: 组装 CityJSON
───────────────────────
cityjson = {
    "type": "CityJSON",
    "version": "2.0",
    "metadata": {"referenceSystem": "..."},
    "vertices": [],
    "CityObjects": {},
    "geometry-templates": {}
}
global_vertex_idx = 0
for bldg in buildings:
    geom = footprint_to_solid(bldg.geometry, bldg.ground_z, bldg.height)
    # 顶点去重 + 全局索引化
    cityjson["CityObjects"][bldg.id] = {
        "type": "Building",
        "attributes": {
            "roofType": bldg.roof_type,
            "measuredHeight": bldg.height
        },
        "geometry": [{
            "type": "Solid",
            "lod": "1.2",
            "boundaries": [[[geom.boundaries]]]  # CityJSON 的深层嵌套格式
        }]
    }
```

| 天 | 任务 | 产出 |
|----|------|------|
| **Mon** | 阅读 CityJSON 2.0 规范 + cjio 实验 | 理解笔记 |
| **Tue** | 设计建筑生成器架构 + 实现 footprint_to_solid (flat roof) | 基础 solid 生成 |
| **Wed** | 实现 gable / skillion 屋顶类型 | 屋顶几何 |
| **Thu** | 集成 DEM: 从 dem_delft.tif 采样地面高程 | 地形贴合 |
| **Fri** | 组装 ≥50 栋建筑的 CityJSON | `delft_city.json` 初版 |

### 🔗 本周连线

```
ISO 19107 有效性  → 确保生成的 Solid 合法
CityGML LOD 0-4  → 理解为什么选 LOD 1.2
3dfier 算法       → 理解从 footprint + 点云 自动重建建筑的原理
```

---

## Week 11: CityJSON 完成 + IFC 入门 (Sep 7 – Sep 13)

### 📚 学习线 — GEO1004: BIM/IFC + GEO1006: Database

| 天 | 章节 | 内容 | 练习 |
|----|------|------|------|
| **Mon** | 3Dbook Ch11 | IFC 结构：EXPRESS 语言、IfcProject → IfcSite → IfcBuilding → IfcBuildingStorey 层级 | 画 IFC 实体继承树 |
| **Tue** | IFC 深入 | IfcWall, IfcSlab, IfcWindow, IfcDoor, IfcRoof — 几何路径 + 属性集 | 用 IfcOpenShell 打开 Duplex.ifc 浏览 |
| **Wed** | IfcOpenShell | Python API: 遍历实体、获取 GlobalId、提取属性、获取几何 | 提取 Duplex 里所有墙的顶点 |
| **Thu** | GEO1006 | 关系数据库基础 + PostgreSQL 安装 | 建第一个 database |
| **Fri** | GEO1006 | PostGIS: geometry/geography 类型、空间索引 (GiST)、ST 函数 | 导入 P1 的 GeoJSON 进 PostGIS |

### 🔧 项目线 — P4 完成 + P5 准备

| 天 | 任务 | 产出 |
|----|------|------|
| **Mon** | 为每个建筑添加 TerrainIntersection 面（底面） | 语义完整性 |
| **Tue** | 导出 CityJSON 中集成 Relief (地形) | 地形对象 |
| **Wed** | cjio validate → 修复所有错误 | 合法 CityJSON |
| **Thu** | P4 README + 截图 + 提交 | P4 完成 |
| **Fri** | 下载 Duplex.ifc + 安装 IfcOpenShell + 浏览模型结构 | P5 环境就绪 |

### 🔗 本周连线

```
IFC 层级结构      → P5 建筑构件分类
IfcOpenShell API  → P5 几何提取管道
PostGIS 空间索引  → P6 后端数据库
```

**🏁 P4 完成。产出:** 合法 CityJSON `delft_city.json` (≥50 buildings + Relief).

---

## Week 12: Project 5 — IFC 解析与几何提取 (Sep 14 – Sep 20)

### 📚 学习线 — GEO1004 (BIM 深入) + GEO1006 (Database)

| 天 | 主题 | 教材 |
|----|------|------|
| **Mon** | IfcLocalPlacement: 局部坐标 → 世界坐标变换链 | IFC 2x3 规范 |
| **Tue** | IfcProductDefinitionShape → IfcShapeRepresentation → IfcPolyLoop | IFC 几何提取路径 |
| **Wed** | IfcOpeningElement: 门窗开洞的几何减运算 | IFC 规范 |
| **Thu** | PostGIS 进阶: 3D 空间查询, ST_3DIntersects, ST_3DDistance | PostGIS 文档 |
| **Fri** | 数据库设计: 范式化、索引策略、JSONB vs 关系列 | — |

### 🔧 项目线 — P5: IFC → CityJSON 转换器

**技术路线（详细步骤）：**

```
Step 1: 解析 IFC — 坐标系
────────────────────────────
def get_local_placement(product):
    """遍历 IfcLocalPlacement 链，构建世界变换矩阵"""
    placement = product.ObjectPlacement
    transform = np.eye(4)
    while placement:
        if placement.RelativePlacement:
            loc = placement.RelativePlacement.Location
            # axis2placement3d → 4×4 matrix
            t = placement_to_matrix(placement.RelativePlacement)
            transform = t @ transform
        placement = placement.PlacementRelTo
    return transform

Step 2: 提取几何（面列表）
──────────────────────────
def extract_faces(product):
    """从 IfcProduct 提取所有面（三角形/多边形）"""
    faces = []
    for rep in product.Representation.Representations:
        for item in rep.Items:
            if item.is_a("IfcFacetedBrep"):
                for face in item.Outer.CfsFaces:
                    points = []
                    for bound in face.Bounds:
                        poly = bound.Bound.Polygon
                        pts = [(p.x, p.y, p.z) for p in poly]
                        points.extend(pts)
                    faces.append(points)
    return faces

Step 3: 语义映射
─────────────────
IFC_SEMANTIC_MAP = {
    "IfcWall":             "WallSurface",
    "IfcWallStandardCase": "WallSurface",
    "IfcSlab":             "FloorSurface",      # 需要区分楼层/屋顶/地面
    "IfcRoof":             "RoofSurface",
    "IfcWindow":           "Window",
    "IfcDoor":             "Door",
    "IfcRailing":          "Railing",
    "IfcStair":            "Stair",
}

def classify_surface(product):
    """根据 IFC 类型 + 语义属性 映射到 CityGML 语义面"""
    ifc_type = product.is_a()
    if ifc_type in ("IfcSlab",):
        # 区分 GroundSlab / RoofSlab / FloorSlab
        predefined = product.PredefinedType
        if predefined == "BASESLAB":
            return "GroundSurface"
        elif predefined == "ROOF":
            return "RoofSurface"
        else:
            return "FloorSurface"
    return IFC_SEMANTIC_MAP.get(ifc_type, "GenericSurface")

Step 4: 构件 → CityJSON Building
─────────────────────────────────
def ifc_to_cityjson(ifc_path):
    ifc = ifcopenshell.open(ifc_path)
    cityjson = {"type": "CityJSON", "version": "2.0", "vertices": [], "CityObjects": {}}

    building_children = []
    for product in ifc.by_type("IfcProduct"):
        transform = get_local_placement(product)
        faces = extract_faces(product)
        semantic_type = classify_surface(product)

        # 世界坐标变换
        faces_world = [transform_face(f, transform) for f in faces]

        # 添加顶点 + 创建 CityJSON geometry
        obj_id = product.GlobalId
        cityjson["CityObjects"][obj_id] = {
            "type": "Building",   # 子构件也用 Building type + children
            "attributes": {"semanticSurface": semantic_type, ...},
            "geometry": [create_geometry(faces_world)]
        }
        building_children.append(obj_id)

    # 创建父 Building
    building_id = "building-1"
    cityjson["CityObjects"][building_id] = {
        "type": "Building",
        "children": building_children,
        "geometry": []  # 子构件的几何组合
    }
    return cityjson
```

| 天 | 任务 | 产出 |
|----|------|------|
| **Mon** | 实现 IfcLocalPlacement → 4×4 变换矩阵 | 坐标工具函数 |
| **Tue** | 实现 extract_faces: 遍历 IfcProduct → 所有三角面 | 几何提取 |
| **Wed** | 测试：提取 Duplex 全部构件的几何并可视化（pyvista） | 验证几何正确 |
| **Thu** | 实现语义映射: IFC type → CityGML semantic surface | 语义分类 |
| **Fri** | 组装 CityJSON + 测试单构件导出 | 初版 CityJSON |

### 🔗 本周连线

```
IfcLocalPlacement    → P5 坐标变换
IfcPolyLoop → 多边形 → P5 几何提取 = P2 半边结构的反向操作
PostGIS 3D 查询      → P6 空间查询 API
```

---

## Week 13: Project 5 — 转换器完成 (Sep 21 – Sep 27)

### 📚 学习线 — GEO1004 收尾 + GEO1006 收尾

| 天 | 主题 | 教材 |
|----|------|------|
| **Mon** | CityGML Building 语义面完整规范 | CityGML 3.0 文档 |
| **Tue** | 地形匹配: 建筑底面与 DEM 的对齐策略 | — |
| **Wed** | 数据质量: ISO 19157 质量维度（完整性、一致性、精度） | ISO 19157 概述 |
| **Thu** | PostGIS 批量导入: shp2pgsql, ogr2ogr | — |
| **Fri** | GeoServer 基础: 发布 WMS/WFS 图层 | GeoServer 教程 |

### 🔧 项目线 — P5 完成

| 天 | 任务 | 产出 |
|----|------|------|
| **Mon** | 实现完整的 ifc_to_cityjson + 父 Building 聚合 | 完整转换器 |
| **Tue** | 地形贴合：从 DEM 采样地面高程，调整建筑 Z 偏移 | 精准放置 |
| **Wed** | cjio validate → 修复所有几何/模式错误 | 合法输出 |
| **Thu** | 边界情况：Opening 处理、缺失几何、空 Reference | 鲁棒性 |
| **Fri** | README + pipeline 图 + 示例输出截图 | P5 完成 |

**核心算法——坐标变换矩阵构建：**

```python
def placement_to_matrix(axis2placement):
    """IfcAxis2Placement3D → 4×4 numpy array"""
    loc = axis2placement.Location.Coordinates
    axis = axis2placement.Axis.DirectionRatios if axis2placement.Axis else (0,0,1)
    refdir = axis2placement.RefDirection.DirectionRatios if axis2placement.RefDirection else (1,0,0)

    z = np.array(axis) / np.linalg.norm(axis)
    x = np.array(refdir) / np.linalg.norm(refdir)
    y = np.cross(z, x)
    y = y / np.linalg.norm(y)
    x = np.cross(y, z)  # 重新正交化

    M = np.eye(4)
    M[:3, 0] = x
    M[:3, 1] = y
    M[:3, 2] = z
    M[:3, 3] = loc
    return M
```

### 🔗 本周连线

```
CityGML 语义面规范  → P5 映射表的设计依据
ISO 19157 质量      → P6 API 数据验证
PostGIS 批量导入    → P6 数据入库
```

**🏁 P5 完成。产出:** `ifc2cityjson.py` — 整个 portfolio 的核心作品.

---

## Week 14: PostGIS + Backend API (Sep 28 – Oct 4)

### 📚 学习线 — GEO1007: Geo Web

| 天 | 主题 | 教材 |
|----|------|------|
| **Mon** | GEO1007 概览: Web GIS 架构、OGC 标准 (WMS/WFS/WCS) | GEO1007 课件 |
| **Tue** | FastAPI: 路由、Pydantic 模型、async/await | FastAPI 官方教程 |
| **Wed** | FastAPI: 中间件、依赖注入、错误处理 | 同上 |
| **Thu** | PostGIS 3D: 3D 空间索引、ST_3DIntersects 查询优化 | PostGIS 文档 |
| **Fri** | OGC API Features: RESTful 空间数据标准 | OGC API 规范 |

### 🔧 项目线 — P6: GeoBIM Web Platform (Backend)

**技术路线：**

```
Step 1: 数据库
────────────────
CREATE EXTENSION postgis;

CREATE TABLE buildings (
    id          TEXT PRIMARY KEY,
    name        TEXT,
    geom3d      GEOMETRY(POLYHEDRALSURFACEZ, 28992),
    attributes  JSONB,
    components  JSONB,      -- 构件列表
    bbox3d      GEOMETRY(POLYHEDRALSURFACEZ, 28992)
);

CREATE INDEX idx_buildings_geom3d ON buildings USING GIST (geom3d);

-- 导入：Python 脚本读取 CityJSON → INSERT
-- 每个 CityObject → 一行，geometry 转 POLYHEDRALSURFACEZ

Step 2: FastAPI Backend
─────────────────────────
from fastapi import FastAPI, HTTPException
from geoalchemy2 import Geometry
import asyncpg

app = FastAPI(title="GeoBIM API")

@app.get("/api/buildings")
async def get_buildings(bbox: str = None):
    """返回 bbox 内所有建筑的 GeoJSON"""
    ...

@app.get("/api/buildings/{building_id}")
async def get_building(building_id: str):
    """返回单个建筑的完整 CityJSON"""
    ...

@app.get("/api/buildings/{building_id}/components")
async def get_components(building_id: str):
    """返回建筑的构件列表（墙/窗/门）"""
    ...

@app.post("/api/query/spatial")
async def spatial_query(request: SpatialQuery):
    """3D 空间查询：ST_3DIntersects, ST_3DDistance"""
    ...
```

| 天 | 任务 | 产出 |
|----|------|------|
| **Mon** | 安装 PostgreSQL + PostGIS，创建 database + 表 | 数据库就绪 |
| **Tue** | 写 CityJSON → PostGIS 导入脚本 | 数据入库 |
| **Wed** | FastAPI 项目骨架 + GET /api/buildings | 第一个 API |
| **Thu** | GET /api/buildings/{id} → CityJSON 响应 | 单建筑查询 |
| **Fri** | POST /api/query/spatial (ST_3DIntersects) | 空间查询 |

### 🔗 本周连线

```
OGC API Features  → API 设计符合标准
PostGIS 3D 查询   → 后端空间查询能力
FastAPI async     → 高性能 Web 服务
```

---

## Week 15: Project 6 — CesiumJS Frontend (Oct 5 – Oct 11)

### 📚 学习线 — GEO1007: 3D Visualization

| 天 | 主题 | 教材 |
|----|------|------|
| **Mon** | CesiumJS: Viewer, scene, camera, imagery layers | CesiumJS 教程 |
| **Tue** | 3D Tiles: 规范理解、LOD 机制、批量表/要素表 | 3D Tiles 1.1 规范 |
| **Wed** | cj23dtiles: CityJSON → 3D Tiles 转换工具 | cj23dtiles 文档 |
| **Thu** | CesiumJS: ScreenSpaceEventHandler, picking, 属性查询 | CesiumJS 文档 |
| **Fri** | 前端-后端集成: fetch API, 异步加载, 状态管理 | — |

### 🔧 项目线 — P6: Frontend

**架构图：**

```
┌──────────────────────────────────────────────────────┐
│  Browser (CesiumJS)                                    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │  Cesium.Viewer                                    │  │
│  │  ├── imageryProvider: Bing/OSM                   │  │
│  │  ├── terrainProvider: Cesium World Terrain      │  │
│  │  │    (or custom DEM from P3)                    │  │
│  │  ├── 3D Tileset: delft_buildings (from P4/P5)   │  │
│  │  │    url: /tiles/delft_city/tileset.json        │  │
│  │  └── primitives: 可选点云/矢量叠加              │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  Click Handler:                                         │
│    handler.setInputAction(click_building,              │
│      Cesium.ScreenSpaceEventType.LEFT_CLICK)           │
│                                                         │
│  Attribute Panel (HTML overlay):                        │
│    ┌─────────────────────────┐                         │
│    │ Building: BAG-1234567   │                         │
│    │ Height: 12.5m           │                         │
│    │ Roof: Flat              │                         │
│    │ Components:             │                         │
│    │  ├── Wall-001 (IfcWall) │                         │
│    │  ├── Roof-001 (IfcSlab) │                         │
│    │  └── Window-001 (...)   │                         │
│    └─────────────────────────┘                         │
└──────────────┬───────────────────────────────────────────┘
               │ HTTP
┌──────────────▼──────────────────────────────────┐
│  FastAPI (:8000)                                  │
│  /api/buildings          → GeoJSON (for list)    │
│  /api/buildings/{id}     → CityJSON (for detail) │
└──────────────────────────────────────────────────┘
```

| 天 | 任务 | 产出 |
|----|------|------|
| **Mon** | CesiumJS 场景搭建 + 基础图层 | 3D 地球 |
| **Tue** | cj23dtiles: 转换 CityJSON → 3D Tiles | tileset.json |
| **Wed** | 加载 3D Tiles 图层 + 相机飞到 Delft | 建筑可见 |
| **Thu** | 点击交互: pick → fetch API → 弹出属性面板 | 交互完成 |
| **Fri** | 图层切换: 建筑/地形/语义面 | 图层控制 |
| **Sat** | 端到端测试 + 截图 + README | P6 完成 |

### 🔗 本周连线

```
CesiumJS 3D Tiles  → P4/P5 CityJSON 的最终展示层
GEO1007 全课程     → P6 = GEO1007 的工程化实践
```

**🏁 P6 完成。产出:** 可访问的 Web 应用 — 浏览器 3D 建筑 + 点击查属性.

---

## Week 16: 整合 + 文档 + 动机信 (Oct 12 – Oct 18)

### 📚 学习线 — GEO1008 + GEO1009 补课

| 天 | 主题 | 教材 |
|----|------|------|
| **Mon** | GEO1008: 数据质量维度（完整性、逻辑一致性、位置精度、时间精度） | ISO 19157 |
| **Tue** | GEO1008: 元数据标准 (ISO 19115)、开放数据原则 | INSPIRE metadata |
| **Wed** | GEO1009: 地理信息组织、法律框架 (GDPR/INSPIRE) | 泛读 INSPIRE Directive |
| **Thu** | 技术写作: 英文技术博文结构、叙事设计 | — |
| **Fri-Sat** | 录视频 + 动机信 | — |

### 🔧 项目线 — 最终整合

**GitHub Monorepo 结构：**

```
geo-portfolio/
├── README.md                          ← 管线图 + 截图 + 视频链接
├── SCHEDULE.md                        ← 这个文件
├── .gitignore                         ← Python/Node
│
├── 01-urban-density/                  ← P1: 城市密度分析
│   ├── README.md                      ← 项目说明 + 截图
│   ├── density_analysis.py            ← 主分析脚本
│   ├── data/                          ← 示例数据（.gitignore 排除大文件）
│   ├── output/                        ← 产出图 + GeoJSON
│   └── requirements.txt               ← geopandas, matplotlib, pysal
│
├── 02-halfedge-engine/                ← P2: Half-edge 网格引擎
│   ├── README.md                      ← API 文档 + 示例
│   ├── halfedge.py                    ← 核心库
│   ├── tests/                         ← pytest
│   └── examples/                      ← cube.obj, tetrahedron.obj
│
├── 03-terrain-pipeline/               ← P3: 地形水文管线
│   ├── README.md                      ← 管线图 + 结果截图
│   ├── pipeline.py                    ← 主脚本: .laz → DEM → 河网
│   ├── pdal_pipeline.json             ← PDAL 配置
│   ├── data/                          ← 示例 .laz 切片
│   └── output/                        ← DEM .tif, 河网 .shp
│
├── 04-cityjson-model/                 ← P4: CityJSON 城市模型
│   ├── README.md                      ← 数据结构说明 + 截图
│   ├── build_cityjson.py              ← 主生成脚本
│   ├── output/                        ← delft_city.json
│   └── validate_report.txt            ← cjio validate 输出
│
├── 05-ifc2cityjson/                   ← P5: IFC → CityJSON 转换器 ★核心
│   ├── README.md                      ← 转换流程图 + 语义映射表
│   ├── ifc2cityjson.py                ← 主转换脚本
│   ├── coordinate_utils.py            ← 坐标变换工具
│   ├── semantic_map.py                ← 语义映射
│   ├── sample/                        ← Duplex_A.ifc + 输出
│   └── tests/                         ← pytest
│
├── 06-3d-web-platform/                ← P6: GeoBIM Web 平台
│   ├── README.md                      ← 架构图 + 截图
│   ├── backend/
│   │   ├── main.py                    ← FastAPI app
│   │   ├── database.py                ← PostGIS 连接
│   │   └── requirements.txt
│   ├── frontend/
│   │   ├── index.html                 ← CesiumJS 页面
│   │   ├── app.js                     ← 交互逻辑
│   │   └── style.css
│   └── tiles/                         ← 3D Tiles (生成)
│
├── docs/
│   ├── tech-blog-zh.md                ← 中文技术文章
│   ├── tech-blog-en.md                ← 英文技术文章
│   ├── pipeline-diagram.png           ← 全管线示意图
│   └── motivation-letter.md           ← 动机信草稿
│
└── data/
    ├── README.md                      ← 数据来源 + 下载链接
    └── links.txt                      ← 所有外部数据 URL
```

| 天 | 任务 | 产出 |
|----|------|------|
| **Mon** | 建 monorepo 结构 + push 所有代码 | GitHub 仓库 |
| **Tue** | 写每个子目录的 README | 6 个 README |
| **Wed** | 写主 README: 管线图 + 项目表格 + 截图 + 视频位置 | 主 README |
| **Thu** | 写中英技术博文 (2000 字 × 2) | 博文 |
| **Fri** | 录 5 分钟视频: 从 .laz → DEM → CityJSON → 浏览器全流程 | 视频 |
| **Sat** | 写动机信: 4 段，每段锚定一个技术细节 | 动机信 |
| **Sun** | 最终检查：链接、脚本可复现性、格式统一 | 最终交付 |

---

# 全管线依赖图

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                        │
│  📚 Learning                                                          │
│                                                                        │
│  GEO1000 ──▶ GEO1002 ──▶ GEO1004 ──▶ GEO1015 ──▶ GEO1004 ──▶ GEO1007 │
│  (Python)    (GIS)       (3D B-rep)  (DTM)       (CityGML)   (Web 3D) │
│      │           │           │           │           │           │     │
│      ▼           ▼           ▼           ▼           ▼           ▼     │
│  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐    │
│  │  P1   │  │  P2   │  │  P3   │  │  P4   │  │  P5   │  │  P6   │    │
│  │ 密度  │  │Half-  │  │ 地形  │  │CityJSON│  │ IFC→  │  │ Web   │    │
│  │ 分析  │  │ edge  │  │ 水文  │  │ 城市   │  │CityJSON│  │ 平台  │    │
│  └───┬───┘  └───┬───┘  └───┬───┘  └───┬───┘  └───┬───┘  └───┬───┘    │
│      │          │          │          │          │          │          │
│      └──────────┼──────────┼──────────┼──────────┼──────────┘          │
│                 │          │          │          │                      │
│                 ▼          ▼          ▼          ▼                      │
│            ┌─────────────────────────────────────────┐                 │
│            │  每步产出 = 下步输入（数据管线）            │                 │
│            │  BAG → P1 → footprints ──▶ P4           │                 │
│            │  AHN4 → P3 → DEM ───────▶ P4, P5       │                 │
│            │  P4 + P5 → CityJSON ────▶ P6            │                 │
│            │  P1 → GeoJSON ──────────▶ P6 属性查询    │                 │
│            └─────────────────────────────────────────┘                 │
│                                                                        │
└──────────────────────────────────────────────────────────────────────┘
```

---

# 周总结表

| Week | Dates | 📚 学习线 | 🔧 项目线 | 🏁 里程碑 |
|------|-------|----------|----------|----------|
| 1 | Jun 28 | GEO1000: Think Python Ch1-19 | 预习：Point/Polygon class | — |
| 2 | Jul 5 | GEO1000: NumPy + Shapely + CRS | 预习：向量化 + 空间操作 | — |
| 3 | Jul 12 | GEO1002: GeoPandas + Rasterio | P1: 数据加载+探索 | — |
| 4 | Jul 19 | GEO1002: 制图 + 空间统计 | **P1 城市密度** | ✅ Jul 25 |
| 5 | Jul 26 | GEO1004: B-rep + Half-edge | P2: 数据结构+OBJ解析 | — |
| 6 | Aug 2 | GEO1004: CSG/NURBS/MAT/G-map | **P2 Half-edge** | ✅ Aug 8 |
| 7 | Aug 9 | GEO1015: TIN/插值/Kriging | P3: AHN4+PDAL+TIN | — |
| 8 | Aug 16 | GEO1015: 地面滤波+水文 | P3: DEM生成 | — |
| 9 | Aug 23 | GEO1015: 水文收尾 | **P3 地形管线** | ✅ Aug 29 |
| 10 | Aug 30 | GEO1004: CityGML/CityJSON | P4: LoD1.2生成 | — |
| 11 | Sep 6 | GEO1004: IFC + GEO1006 | **P4 CityJSON** | ✅ Sep 12 |
| 12 | Sep 13 | GEO1004: IFC深入 + GEO1006 | P5: 几何提取 | — |
| 13 | Sep 20 | GEO1004收尾 + 质量 | **P5 IFC2CityJSON** | ✅ Sep 26 |
| 14 | Sep 27 | GEO1007: Geo Web + API | P6: Backend | — |
| 15 | Oct 4 | GEO1007: 3D Viz | **P6 Web平台** | ✅ Oct 10 |
| 16 | Oct 11 | GEO1008/1009: 质量+法律 | 整合+文档+动机信 | ✅ Oct 17 |

---

# 日常节奏

```
08:00-11:00  🔧 项目线：写代码、调试、出产出（上午脑子最清醒）
11:00-13:00  📚 学习线：阅读教材、看课件、做练习题
14:00-15:00  整合：写文档、记录笔记、git commit
```

周六=缓冲（修复这周坏的、补没做完的），周日=休息。
不再设 DL 维持时间——16 周管线密度足够，上下文切换成本不值得。

---

# Phase 2: 申请冲刺（2026.10.18 – 2026.12.31）

| 时间段 | 做什么 | 产出 |
|--------|--------|------|
| **10.18 – 10.28** | CV 定稿：六项目摘要 + 技能矩阵 + GitHub 链接。每个项目一句话概括技术栈和成果 | `cv.pdf` |
| **10.18 – 11.10** | 联系推荐人：爱丁堡导师 + 本科导师。提前发 CV + 项目摘要 + 要强调的点 | 2 封推荐信 |
| **10.28 – 11.10** | Motivation Letter v1 → v2 → v3。每段嵌入一个项目的具体技术细节作为能力证据 | `motivation-letter-v3.pdf` |
| **11.10 – 11.20** | TUD 申请材料最终检查 + 提交。目标：11 月中旬，早于奖学金截止 (2027-02-01) | TUD 提交确认 |
| **11.20 – 12.20** | 其他项目投递：UCL Geospatial Sciences / UPann Urban Spatial Analytics / AI Conversion（如适用） | 各校提交确认 |
| **12.20 – 12.31** | 跟进 + 面试准备（如有）+ 补材料 | — |

## 申请截止速查

| 学校 | 项目 | 申请开放 | 奖学金 | 最终截止 |
|------|------|---------|--------|---------|
| **TU Delft** | MSc Geomatics | 2026-10-15 | 2027-02-01 | 2027-04-01 |
| **UCL** | Geospatial Sciences MSc | 2026-10-20 | — | 2027-06-26 |
| **UPenn** | Urban Spatial Analytics | 未确认 | — | 通常 12-1 月 |

**策略:** TUD 10 月中旬开门即投（滚动审核，早投早出结果）。奖学金 2 月截止前补材料。UCL 截止晚，不急。

---

# 数据清单

| 数据 | 来源 | 需要时间 | 大小 |
|------|------|----------|------|
| BAG building footprints (Amsterdam) | [PDOK](https://www.pdok.nl/) | Week 4 | ~500 MB |
| CBS neighborhood boundaries | [CBS Wijk- en Buurtkaart](https://www.cbs.nl/) | Week 4 | ~50 MB |
| AHN4 .laz tile (Delft) | [PDOK AHN4](https://www.pdok.nl/geo-services/-/article/actueel-hoogtebestand-nederland-ahn4-) | Week 8 | ~2 GB / tile |
| Duplex_A_20110505.ifc | [buildingSMART](https://github.com/buildingSMART/Sample-Test-Files) | Week 12 | ~10 MB |
| DEM .tif (自产) | Project 3 产出 | Week 11 | ~100 MB |
| city.json (自产) | Projects 4+5 产出 | Week 14 | ~5 MB |

---

# 工具链

| 层 | 工具 | 安装 |
|----|------|------|
| Python | 3.11+ | `conda create -n geo python=3.11` |
| 点云 | PDAL + laspy | `conda install -c conda-forge pdal python-pdal` |
| GIS | GDAL/OGR + GeoPandas + Shapely + Fiona + Rasterio | `conda install -c conda-forge gdal geopandas shapely fiona rasterio` |
| 3D | scipy + trimesh + pyvista | `pip install trimesh pyvista` |
| 插值/水文 | pykrige + richdem | `pip install pykrige richdem` |
| 城市模型 | cjio + IfcOpenShell | `pip install cjio ifcopenshell` |
| 数据库 | PostgreSQL + PostGIS | `conda install -c conda-forge postgis` |
| Web | FastAPI + uvicorn | `pip install fastapi uvicorn asyncpg geoalchemy2` |
| 前端 | CesiumJS (CDN) | 不需安装 |
| 可视化 | matplotlib + folium | `pip install matplotlib folium` |
