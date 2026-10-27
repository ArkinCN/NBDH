"""学生成绩管理系统 —— Python 入门教学项目

一个小而完整的命令行程序：菜单循环 + 列表/字典存数据 + JSON 文件持久化。
运行方式：python main.py
"""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.json")


def load_students():
    """从 students.json 读取学生列表；文件不存在或内容损坏时返回空列表。"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("提示：students.json 内容已损坏，本次按空数据启动。")
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


def input_score(prompt):
    """反复询问，直到用户输入 0-100 之间的数字。"""
    while True:
        text = input(prompt).strip()
        try:
            score = float(text)
        except ValueError:
            print("  输入无效，请输入数字，例如 85 或 92.5")
            continue
        if 0 <= score <= 100:
            return score
        print("  成绩必须在 0 到 100 之间")


def level_of(score):
    """把百分制成绩换算成等级。"""
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "E"


def add_student(students):
    name = input("学生姓名：").strip()
    if not name:
        print("姓名不能为空")
        return
    if find_student(students, name) is not None:
        print(f"学生 {name} 已存在，如需改分请用“修改成绩”")
        return
    score = input_score("成绩（0-100）：")
    students.append({"name": name, "score": score})
    save_students(students)
    print(f"已添加：{name}，成绩 {score:.1f}，等级 {level_of(score)}")


def list_students(students):
    if not students:
        print("暂无学生记录，请先添加")
        return
    print(f"共 {len(students)} 名学生：")
    for index, student in enumerate(students, start=1):
        print(f"  {index}. {student['name']}  成绩 {student['score']:.1f}  等级 {level_of(student['score'])}")


def query_students(students):
    keyword = input("要查询的姓名（支持部分匹配）：").strip()
    if not keyword:
        print("关键字不能为空")
        return
    results = [s for s in students if keyword in s["name"]]
    if not results:
        print(f"没有找到包含“{keyword}”的学生")
        return
    print(f"找到 {len(results)} 条记录：")
    for student in results:
        print(f"  {student['name']}  成绩 {student['score']:.1f}  等级 {level_of(student['score'])}")


def update_score(students):
    name = input("要修改的姓名：").strip()
    student = find_student(students, name)
    if student is None:
        print(f"没有找到学生 {name}")
        return
    print(f"当前成绩：{student['score']:.1f}")
    student["score"] = input_score("新成绩（0-100）：")
    save_students(students)
    print(f"已将 {name} 的成绩改为 {student['score']:.1f}")


def delete_student(students):
    name = input("要删除的姓名：").strip()
    student = find_student(students, name)
    if student is None:
        print(f"没有找到学生 {name}")
        return
    students.remove(student)
    save_students(students)
    print(f"已删除 {name}")


def show_statistics(students):
    if not students:
        print("暂无数据，无法统计")
        return
    scores = [s["score"] for s in students]
    total = len(scores)
    passed = len([x for x in scores if x >= 60])
    print(f"  学生人数：{total}")
    print(f"  平均分：{sum(scores) / total:.1f}")
    print(f"  最高分：{max(scores):.1f}")
    print(f"  最低分：{min(scores):.1f}")
    print(f"  及格率：{passed / total * 100:.1f}%（及格 {passed} 人）")


def show_menu():
    print()
    print("=" * 32)
    print("  学生成绩管理系统")
    print("=" * 32)
    print("  1. 添加学生")
    print("  2. 查看全部")
    print("  3. 按姓名查询")
    print("  4. 修改成绩")
    print("  5. 删除学生")
    print("  6. 成绩统计")
    print("  0. 退出")
    print("=" * 32)


def main():
    students = load_students()
    print("欢迎使用学生成绩管理系统（数据保存在 students.json）")
    while True:
        show_menu()
        choice = input("请输入选项（0-6）：").strip()
        if choice == "1":
            add_student(students)
        elif choice == "2":
            list_students(students)
        elif choice == "3":
            query_students(students)
        elif choice == "4":
            update_score(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            show_statistics(students)
        elif choice == "0":
            print("已退出，数据已保存。")
            break
        else:
            print("无效选项，请输入 0-6 之间的数字")


if __name__ == "__main__":
    main()
