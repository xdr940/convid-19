import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
sns.set()
plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题-设置字体为黑体
# Load the example flights dataset and convert to long-form
#flights_long = sns.load_dataset("flights")
#lights = flights_long.pivot("month", "year", "passengers")
df_edges = pd.read_csv('./data/edge_edition.csv')
df_edges =pd.DataFrame(df_edges,dtype=int)
# Draw a heatmap with the numeric values in each cell
f, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(df_edges.T, annot=True, fmt='d', linewidths=.5, ax=ax)
plt.show()
print('12')