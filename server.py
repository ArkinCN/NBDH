"""学生成绩管理系统 · Web 版后端 —— 只用 Python 标准库，无需安装任何依赖

后端提供两样东西：
  1. 页面：GET /              → 返回 index.html
  2. 接口：GET /api/students  → 学生列表
          POST /api/students  → 添加 {name, score}
          PUT /api/students/<姓名>    → 修改成绩 {score}
          DELETE /api/students/<姓名> → 删除

运行：python server.py，然后浏览器打开 http://localhost:5199
（监听 0.0.0.0，端口可用环境变量 PORT 覆盖，默认 5199）
"""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "students.json")
INDEX_FILE = os.path.join(BASE_DIR, "index.html")
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "5199"))


def load_students():
    """读取学生列表；文件不存在或内容损坏时返回空列表。"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_students(students):
    """把学生列表写回 students.json。"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)


def find_student(students, name):
    """按姓名精确查找，返回学生字典；找不到返回 None。"""
    for student in students:
        if student["name"] == name:
            return student
    return None


def parse_score(value):
    """把输入转成 0-100 的分数，返回 (分数, 错误信息)，二选一为 None。"""
    try:
        score = float(value)
    except (TypeError, ValueError):
        return None, "成绩必须是数字"
    if not 0 <= score <= 100:
        return None, "成绩必须在 0 到 100 之间"
    return score, None


def student_name_from_path(path):
    """从 /api/students/张三 里取出姓名，URL 里的中文是编码过的，需要 unquote。"""
    prefix = "/api/students/"
    if not path.startswith(prefix):
        return None
    name = unquote(path[len(prefix):])
    return name or None


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            self.send_file(INDEX_FILE, "text/html; charset=utf-8")
        elif path == "/api/students":
            self.send_json(load_students())
        else:
            self.send_json({"error": "页面不存在"}, 404)

    def do_POST(self):
        if urlparse(self.path).path != "/api/students":
            self.send_json({"error": "页面不存在"}, 404)
            return
        data = self.read_json()
        name = str(data.get("name", "")).strip()
        if not name:
            self.send_json({"error": "姓名不能为空"}, 400)
            return
        score, error = parse_score(data.get("score"))
        if error:
            self.send_json({"error": error}, 400)
            return
        students = load_students()
        if find_student(students, name) is not None:
            self.send_json({"error": f"学生 {name} 已存在"}, 409)
            return
        students.append({"name": name, "score": score})
        save_students(students)
        self.send_json({"message": f"已添加 {name}"}, 201)

    def do_PUT(self):
        name = student_name_from_path(urlparse(self.path).path)
        if name is None:
            self.send_json({"error": "页面不存在"}, 404)
            return
        score, error = parse_score(self.read_json().get("score"))
        if error:
            self.send_json({"error": error}, 400)
            return
        students = load_students()
        student = find_student(students, name)
        if student is None:
            self.send_json({"error": f"没有找到学生 {name}"}, 404)
            return
        student["score"] = score
        save_students(students)
        self.send_json({"message": f"已将 {name} 的成绩改为 {score}"})

    def do_DELETE(self):
        name = student_name_from_path(urlparse(self.path).path)
        if name is None:
            self.send_json({"error": "页面不存在"}, 404)
            return
        students = load_students()
        student = find_student(students, name)
        if student is None:
            self.send_json({"error": f"没有找到学生 {name}"}, 404)
            return
        students.remove(student)
        save_students(students)
        self.send_json({"message": f"已删除 {name}"})

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path, content_type):
        if not os.path.exists(path):
            self.send_json({"error": "index.html 不存在"}, 500)
            return
        with open(path, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"学生成绩管理系统已启动：http://localhost:{PORT}")
    print("按 Ctrl+C 停止")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
