# 【内容】
# マンホイットニーの U 検定

from scipy.stats import mannwhitneyu

data = """
0	0	0
1	0	0
2	0	0
3	0	0
4	0	0
5	0	0
6	0	0
7	2	0
8	4	0
9	2	2
10	6	0
11	2	0
12	7	3
13	8	4
14	8	2
15	11	0
16	11	1
17	5	2
18	2	1
19	0	1
20	0	0
21	0	0
22	0	0
23	1	2
24	0	0
25	0	0
26	0	0
27	0	0
""".strip()

n_data, a_data, b_data = [], [], []
for line in data.split("\n"):
    n, a, b = line.split("\t")
    n_data.append(int(n))
    a_data.append(int(a))
    b_data.append(int(b))

samples_a = sum([[n] * freq for n, freq in zip(n_data, a_data)], [])
samples_b = sum([[n] * freq for n, freq in zip(n_data, b_data)], [])

stat, p_value = mannwhitneyu(samples_a, samples_b, alternative='two-sided')

print(f"U統計量: {stat}")
print(f"p値: {p_value}")
