# 学生成绩管理系统（Python 入门教学项目）

同一个项目提供了两个版本，建议按顺序学习：

- **命令行版** `main.py`：只讲 Python 基础语法。
- **Web 版** `server.py` + `index.html`：浏览器页面 + 后端接口，看前后端怎么配合。

两个版本共用同一份 `students.json` 数据（不要同时运行两个版本的写操作）。

## 一、这个项目能学到什么

| 知识点 | 在代码里的位置 |
| --- | --- |
| 变量、字符串、f-string 格式化 | `print(f"...{score:.1f}...")` |
| `if / elif / else` | `level_of()`、菜单分发、接口参数校验 |
| `while` / `for` 循环、`enumerate()` | `main()` 主循环、`find_student()` |
| 列表、字典、列表推导式 | `students` 数据、`query_students()`、统计 |
| 函数、参数、返回值、元组 | `parse_score()` 返回 `(分数, 错误信息)` |
| `try / except` 异常处理 | 输入非数字、JSON 文件损坏 |
| 文件读写、JSON 序列化 | `load_students()` / `save_students()` |
| HTTP 请求与接口 | `server.py` 的 `do_GET / do_POST / do_PUT / do_DELETE` |
| 前后端通信（fetch） | `index.html` 里的 `request()` 函数 |
| 前端渲染与事件 | `render()`、`addEventListener` |

## 二、运行方式

### 命令行版

```bash
cd D:\test
python main.py
```

### Web 版（不需要安装任何依赖）

```bash
cd D:\test
python server.py
```

看到 `学生成绩管理系统已启动：http://localhost:5199` 后，用浏览器打开 <http://localhost:5199>，按 `Ctrl+C` 停止服务。

如果系统提示找不到 `python` 命令，说明 Python 没加入 PATH，可以用完整路径：

```bash
"E:\Software_Installation\07_Programming_Languages\Miniconda3\python.exe" main.py
"E:\Software_Installation\07_Programming_Languages\Miniconda3\python.exe" server.py
```

## 三、文件说明

```
D:\test
├── main.py        命令行版（全部代码）
├── server.py      Web 版后端（只用 Python 标准库）
├── index.html     Web 版前端（HTML + CSS + JS，单文件）
├── students.json  数据文件（运行后自动生成，可删除重置）
├── Dockerfile     容器镜像构建文件
├── .dockerignore  构建时排除的文件
└── README.md      本说明
```

`students.json` 的内容就是一个列表，每个元素是一个字典：

```json
[
  { "name": "张三", "score": 85.0 },
  { "name": "李四", "score": 59.5 }
]
```

## 四、命令行版功能

菜单包含：添加学生、查看全部、按姓名查询（支持部分匹配）、修改成绩、删除学生、成绩统计、退出。数据在每次修改后自动保存到 `students.json`。

一次操作示例（示例数据，不是真实数据）：

```
请输入选项（0-6）：1
学生姓名：张三
成绩（0-100）：85
已添加：张三，成绩 85.0，等级 B

请输入选项（0-6）：6
  学生人数：2
  平均分：72.3
  最高分：85.0
  最低分：59.5
  及格率：50.0%（及格 1 人）
```

## 五、Web 版：页面和接口

### 页面功能

顶部表单输入姓名和成绩点“添加”；表格显示姓名、成绩、等级；每行有“改分”和“删除”按钮；表格下方实时显示人数、平均分、最高分、最低分、及格率。错误提示（重名、成绩非法等）显示在表单下方。

### 后端接口

| 方法 | 地址 | 请求体 | 作用 | 成功状态码 |
| --- | --- | --- | --- | --- |
| GET | `/` | 无 | 返回页面 | 200 |
| GET | `/api/students` | 无 | 查询全部学生 | 200 |
| POST | `/api/students` | `{"name":"张三","score":85}` | 添加学生 | 201 |
| PUT | `/api/students/张三` | `{"score":90}` | 修改成绩 | 200 |
| DELETE | `/api/students/张三` | 无 | 删除学生 | 200 |

失败时返回 `{"error": "错误原因"}`，状态码为 400（参数不对）、404（学生不存在）或 409（重名）。

### 一次“添加”是如何完成的

1. 用户点“添加”，前端 `event.preventDefault()` 阻止表单默认刷新页面。
2. 前端用 `fetch("/api/students", { method: "POST", body: JSON.stringify(...) })` 发送 JSON。
3. 后端 `do_POST` 读请求体 → 校验姓名和成绩 → 写入 `students.json` → 返回 `{"message": "..."}`。
4. 前端收到成功响应后清空输入框，再 `GET /api/students` 拉取最新列表并重新渲染表格。

两个安全习惯：页面用 `textContent` 写入姓名（不拼 HTML，避免 XSS）；成绩范围、重名等校验放在**后端**，前端只负责显示错误。

## 六、建议的阅读顺序

1. `main()` —— 程序骨架：加载数据 → 循环显示菜单 → 按选项调用函数。
2. `load_students()` / `save_students()` —— 数据怎么存到文件、怎么读回来。
3. `find_student()` —— 最典型的“遍历列表找元素”。
4. `add_student()` —— 读输入、校验、改数据、存文件，四步走。
5. `parse_score()` —— 用 `try/except` 防止输入字母导致崩溃。
6. `server.py` —— `do_GET` 返回页面和列表，`do_POST` / `do_PUT` / `do_DELETE` 分别对应增、改、删。
7. `index.html` 的 `<script>` —— 从 `loadStudents()` 开始，再看 `render()` 和表单提交事件。

## 七、练习题

命令行版：

1. **排序**：加“按成绩从高到低排序”，用 `sorted(students, key=..., reverse=True)`。
2. **清空数据**：加“清空所有数据”，要求输入 `y` 二次确认。
3. **增加字段**：给每个学生加“班级”，并支持按班级查询。
4. **换成 CSV**：数据文件从 JSON 改成 CSV，用标准库 `csv` 模块，体会两种格式的区别。
5. **多门课程**：数据结构改成 `{"name": "张三", "scores": {"数学": 85, "英语": 90}}`，按科目统计。

Web 版：

6. **前端搜索框**：按姓名过滤表格，不用改后端（在前端对列表 `filter` 后重新渲染）。
7. **排序按钮**：点一下按成绩排序，再点一下恢复，只改前端的渲染逻辑。
8. **统计接口**：后端增加 `GET /api/statistics` 返回统计结果，前端改成调用这个接口而不是自己算。
9. **换 Flask**：`pip install flask` 后用 Flask 重写 `server.py`，对比两者代码量。

## 八、Docker 部署

```bash
docker build -t nbdh-score:test .
docker run -d --name nbdh-score -p 5199:5199 --memory 512m --cpus 1.0 nbdh-score:test
curl -fsS http://localhost:5199/
```

- 容器内监听 `0.0.0.0:5199`，可用 `PORT` 环境变量覆盖；镜像内以非 root 用户 `app`（uid 10001）运行。
- 镜像自带 `HEALTHCHECK`，探测 `http://127.0.0.1:5199/`。
- 数据存在容器的 `/app/students.json`，删除或重建容器会丢失；需要持久化时用文件挂载 `-v 宿主机students.json:/app/students.json`，并保证容器内 `app` 用户（uid 10001）可写。
- 实测常驻内存约 16MB，512MB 限额足够。

## 九、常见问题

- **`python` 不是内部或外部命令**：Python 未加入 PATH，用第二节的完整路径，或安装时勾选 “Add Python to PATH”。
- **`http://localhost:5199` 打不开**：确认 `server.py` 正在运行且没有报错。5199 端口被占用时，改 `server.py` 顶部的 `PORT` 默认值，或临时用环境变量覆盖（Windows PowerShell：`$env:PORT=5200; python server.py`）。
- **不要直接双击 `index.html`**：页面里的接口请求需要后端，必须通过 `python server.py` 启动后访问。
- **中文显示乱码**：Windows 终端编码问题，可执行 `chcp 65001` 切到 UTF-8，或在 PyCharm 里运行。
- **启动时提示 JSON 内容损坏**：手动改坏了 `students.json`，删掉该文件重新开始即可。
- **改坏代码想看效果**：每次改完都要重启 `server.py`（命令行版同理）。
