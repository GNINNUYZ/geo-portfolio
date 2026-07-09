#choropleth
import geopandas as gpd
import matplotlib.pyplot as plt

gdf = gpd.read_file("geo-portfolio/data/coverage_result.geojson")
fig, ax = plt.subplots(figsize=(14, 12))
gdf.plot(column="cover_ratio", cmap="YlOrRd", legend=True,
         edgecolor="grey", linewidth=0.3, ax=ax)
ax.set_title("Amsterdam Building Coverage"); ax.set_axis_off()
plt.savefig("coverage_test.png", dpi=200, bbox_inches="tight")