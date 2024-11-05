# 知识图谱（Knowledge Graph, KG）

> [知识图谱的技术与应用 | 机器之心](https://www.jiqizhixin.com/articles/2018-06-19)
>
> [Review-on-Knowledge-Graph-Techniques.pdf](https://www.researchgate.net/profile/Yongpan-Sheng/publication/341505212_Review_on_Knowledge_Graph_Techniques/links/5ec48ef492851c11a8778610/Review-on-Knowledge-Graph-Techniques.pdf)
>
> [知识图谱构建技术综述（刘峤）.pdf](assets/知识图谱构建技术综述（刘峤）-20241104150022-rz7vyek.pdf)
>
> [大厂技术实现 | 详解知识图谱的构建全流程 @ 自然语言处理系列](https://www.showmeai.tech/article-detail/94)
>
> [北京科技大学信息化建设与管理办公室](https://info.ustb.edu.cn/ITxy/jswd/f9c69c2f22a04495931f2d5cca087297.htm)

## 什么是知识图谱？

知识图谱（Knowledge Graph, KG）是由 Google 在 2012 年提出来的概念，是一个用于增强其搜索引擎功能的**知识库**。

从数据结构角度来看，知识图谱是一种**异构图（包含多种类型的节点和多种类型的边）** 。

​![image](assets/image-20241101143533-q89s9i0.png)​

在知识图谱里，我们通常用**实体（Entity）** 来表达图里的节点、用**关系（Relation）** 来表达图里的边。

实体指的是现实世界中的事物，比如人、地名、概念、公司等；关系则用来表达不同实体之间的某种联系，比如小明-“就读于”-清北大学、李老师和王老师是同事。

​![image](assets/image-20241101160731-jletlz7.png)​

## 知识图谱表示方式

### 1、属性图（**Property Graphs）**

节点和关系都可以包含属性，每个属性是一个键值对，用于存储节点的属性信息。

​![image](assets/image-20241104093249-n00t4n9.png)​

‍

### 2、RDF（资源描述框架）

RDF 使用“主语-谓词-宾语”的**三元组**形式来表示，

* **主语（Subject）** ：实体，例如小红、小明、李老师、王老师、清北大学。
* **谓词（Predicate）** ：描述实体的属性或关系，例如年龄、导师。
* **宾语（Object）** ：实体的属性值或与之相关的另一个实体，例如 25、男。

​![image](assets/image-20241104092213-cgrj997.png)​

### 3、RDF vs 属性图

‍

|特性|RDF（资源描述框架）|属性图（Property Graph）|
| ----| ------------------------------------------------| ----------------------------------------------|
|**基本单位**|三元组（subject-predicate-object）|节点（node）、边（edge）、属性（properties）|
|**数据结构**|三元组集合，采用图的形式，但严格基于三元组的结构|基于节点和边的图结构，边和节点都可以有多个属性|
|**关系的表达**|通过谓词（predicate）表示关系，关系是**单向**的|边表示关系，可以是**单向或双向**的|
|**属性的表示**|通常通过附加三元组（如 `subject-predicate-object`​）来描述属性|属性可以直接附加到节点和边上，属性可以是键值对|
|**应用场景**|多为学术界场景|多为工业界场景，如图数据库|

‍

## 知识图谱关键技术

​![image](assets/image-20241104101158-jg6u2x5.png)​

### 1、知识抽取

 **（1）实体抽取**：从非/半结构化数据中识别和提取出具有特定意义的实体（如人名、地名、机构名等）的过程

​![image](assets/image-20241104100431-yngsp92.png)​

 **（2）关系抽取**：从非/半结构化数据中抽取出两个或多个实体之间的语义关系，

​![image](assets/image-20241104100642-lv7pejq.png)​

 **（3）属性抽取：** 从非/半结构化数据中提取实体的属性，如人的姓名、年龄、国籍等

### 2、知识融合

 **（1）实体消歧(Entity Disambiguation)** ：同一个实体名称可能具有多个不同的含义，比如“苹果”可以指一种水果，也可以指一家科技公司。实体消歧就是根据上下文信息来确定实体的准确含义。

​![image](assets/image-20241104145024-vrtri0f.png)​

 **（2）实体统一(Entity Normalization)** ：有些实体写法上不一样，但其实是指向同一个实体。比如“病人”和“患者”表面上是不同的字符串，但实际上是同一个意思；单词缩写，如“NYC”和“New York”同理。

​![image](assets/image-20241104145115-5n1djts.png)​

 **（3）指代消解(Coreference Resolution)** ：分析代词和实体的指代关系。

​![image](assets/image-20241104152950-fmqd0ds.png)​

### 3、知识加工

 **（1）本体抽取(Ontology Extraction)** ：

**本体**是对特定领域之中某套概念及其相互之间关系的形式化表达（wikipedia）。例如：猫、熊、鲸都是“哺乳动物”本体，哺乳动物又是“动物”本体。

​![image](assets/image-20241104155125-j0keci9.png)​

本体抽取过程包含三个阶段：实体并列关系相似度计算 ➡️ 实体上下位关系抽取 ➡️ 本体的生成。

​![image](assets/image-20241104153049-132487x.png)​

 **（2）知识推理(Knowledge Inference)** ：从已知的实体关系数据出发，经过计算机推理，建立实体间新的关联，从而拓展和丰富知识图谱。例如：已知叶莉是姚明的妻子，姚明是姚沁蕾的爸爸，可以推出叶莉是姚沁蕾的母亲。

​![image](assets/image-20241104152436-4701yjd.png)​

 **（3）质量评估(Quality Evaluation)** ：对知识的可信度进行量化，通过舍弃置信度较低的知识来保障知识库的质量。

‍

## 图数据库

### 1、常用图数据库

> [DB-Engines Ranking - popularity ranking of graph DBMS](https://db-engines.com/en/ranking/graph+dbms)

​![image](assets/image-20241101141123-q4vj1ga.png)​

### 2、Neo4j

> [Neo4j Graph Database &amp; Analytics | Graph Database Management System](https://neo4j.com/)
>
> [手把手教你快速入门知识图谱 - Neo4J 教程 - 知乎](https://zhuanlan.zhihu.com/p/88745411)
>
> [Windows 10 64 位系统下 Neo4j 安装教程（2021.1.13）_desktop 与 java jdk 版本 17 和 11 以及 bloom、browser 和 neo4j enter-CSDN 博客](https://blog.csdn.net/jing_zhong/article/details/112557084)

#### 1）简介

* 一个用 Java 编写的开源图数据库，支持 Java、Python 等多种开发语言
* 查询语言是 Cypher，类似于 SQL，设计简洁，易于上手
* 支持 ACID 事务
* ...

#### 2）安装运行（社区版 or 桌面版 二选一）

#### 2.1）**社区版**

去官方地址 [Neo4j Deployment Center - Graph Database &amp; Analytics](https://neo4j.com/deployment-center/)，下载 **4.4.38** 社区版的 window 安装包（**不要下载 5.25.1 版本，因为需要 java17 的环境，java11 环境跑不起来**）

​![image](assets/image-20241105082306-zxlsweh.png)​

将安装包解压，在解压后的目录下，用 CMD 输入命令 `bin\neo4j console` ​启动 neo4j 服务器

​![image](assets/image-20241105082430-w3905jc.png)​

浏览器中打开地址：[http://localhost:7474/]()，进入 neo4j 服务器页面，输入用户名：**neo4j，** 输入密码：**neo4j**

​![image](assets/image-20241105082759-9b74rt5.png)​

进入后会强制要求修改密码

​![image](assets/image-20241105082902-qo1fbmu.png)​

修改完成后进入主页

​![image](assets/image-20241105082959-z5nzgwy.png)​

‍

#### 2.2）**桌面版**

下载地址：[Neo4j Desktop Download | Free Graph Database Download](https://neo4j.com/download/)

​![image](assets/image-20241105080936-z5w6dhv.png)​

点击 download 按钮后会要求你填写一堆信息

​![image](assets/image-20241105083446-hhcz6m9.png)​

填写完成后就可以下载了，它会给你一个激活码，保存下来，后续会用到

​![image](assets/image-20241105081045-spvds2x.png)​

```python
eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Ii4rQC4rIiwibWl4cGFuZWxJZCI6IiRkZXZpY2U6MTkyZjYyYzU2ZDkzMmMtMDJjODU0Yjc1ZTA3MTgtNGM2NTdiNTgtMWZhNDAwLTE5MmY2MmM1NmQ5MzJjIiwibWl4cGFuZWxQcm9qZWN0SWQiOiI0YmZiMjQxNGFiOTczYzc0MWI2ZjA2N2JmMDZkNTU3NSIsIm9yZyI6Ii4qIiwicHViIjoibmVvNGouY29tIiwicmVnIjoiICIsInN1YiI6Im5lbzRqLWRlc2t0b3AiLCJleHAiOjE3NjIzMDE0MTgsInZlciI6IioiLCJpc3MiOiJuZW80ai5jb20iLCJuYmYiOjE3MzA3NjU0MTgsImlhdCI6MTczMDc2NTQxOCwianRpIjoiVVUxenBjZGtZIn0.NDy0HBh1QO5CjIkaRe6tFZQ7Od_W4Qx-QWmDWRJi7zFMIEumocQTHo_q9jVCVvY0qkUoKiJ9rWMZ7W-HsUEqYmDkJzx8K2fIRf-93jWcvBC7esF2r1bzXZhIDsRHgorE9dyZiKVULtg2y_XpAYa0qanG6IFuA_PcnMyKwrmbq222Ka3xD9-D4U9Q-mzRwhgBvG64Oh83ia8nGj_F0lFXGHa43ci5XUKU5nl3sjtX-uoYfvj57EOiG8BH0YO0bRpIQxk_o2IwJ1qcK9SmLqXwwLXkfsCJ-QTopZk56KsN9LX5E35IMXgcjIbc7bZ_wi8DCQqqacavktIRcNWIaX_uMA
```

双击下载好的安装包，选择安装目录，一直点击下一步即可安装成功

​![image](assets/image-20241105083719-75b5r7j.png)​

启动后选择一个目录保存应用数据

​![image](assets/image-20241105083852-lrz6q0u.png)​

在弹出的注册界面中，将激活码粘贴到右侧文本框中

​![image](assets/image-20241105083958-nngopz0.png)​

让他自己准备一会。。。

​![image](assets/image-20241105084123-e3qbsvh.png)​

准备好后进入主页面

​![image](assets/image-20241105085155-nkzh4l9.png)​

#### 3）使用

按照这篇文章的例子一步步做一遍：[手把手教你快速入门知识图谱 - Neo4J 教程 - 知乎](https://zhuanlan.zhihu.com/p/88745411)

‍
