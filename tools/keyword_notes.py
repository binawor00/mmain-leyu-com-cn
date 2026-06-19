from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    """Represents a single keyword note with metadata."""
    keyword: str
    note: str
    url: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def to_brief(self) -> str:
        """Return a short representation of the note."""
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return f"[{self.keyword}] {self.note[:30]}... | 标签: {tag_str}"

    def to_detailed(self) -> str:
        """Return a detailed string representation."""
        parts = [
            f"关键词: {self.keyword}",
            f"笔记: {self.note}",
            f"关联URL: {self.url}" if self.url else "关联URL: 无",
            f"标签: {', '.join(self.tags) if self.tags else '无'}",
            f"创建时间: {self.created_at}",
        ]
        return "\n".join(parts)


@dataclass
class KeywordNoteCollection:
    """A collection of keyword notes with filtering and formatting methods."""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [note for note in self.notes if tag in note.tags]

    def filter_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [note for note in self.notes if keyword in note.keyword]

    def formatted_output(self, style: str = "brief", tag_filter: Optional[str] = None) -> str:
        """
        Generate formatted output for all notes.
        style: 'brief' or 'detailed'
        """
        filtered = self.notes
        if tag_filter:
            filtered = self.filter_by_tag(tag_filter)

        if not filtered:
            return "没有匹配的笔记。"

        lines = [f"共 {len(filtered)} 条笔记"]
        for idx, note in enumerate(filtered, start=1):
            if style == "brief":
                lines.append(f"{idx}. {note.to_brief()}")
            else:
                lines.append(f"{idx}.\n{note.to_detailed()}")
                lines.append("---")

        return "\n".join(lines)

    def export_to_markdown(self, title: str = "关键词笔记") -> str:
        """Export all notes to Markdown format."""
        md_lines = [f"# {title}", ""]
        for note in self.notes:
            md_lines.append(f"## {note.keyword}")
            md_lines.append(f"**笔记**: {note.note}")
            if note.url:
                md_lines.append(f"**URL**: {note.url}")
            if note.tags:
                md_lines.append(f"**标签**: {', '.join(note.tags)}")
            md_lines.append("")
        return "\n".join(md_lines)


def demo_usage() -> None:
    """Demonstrate the usage of KeywordNote and KeywordNoteCollection."""
    collection = KeywordNoteCollection()

    # Sample data with given URL and keyword
    collection.add_note(
        KeywordNote(
            keyword="乐鱼体育",
            note="关于乐鱼体育平台的笔记：提供体育赛事直播和竞猜服务。",
            url="https://mmain-leyu.com.cn",
            tags=["体育", "直播", "乐鱼"]
        )
    )

    collection.add_note(
        KeywordNote(
            keyword="Python",
            note="Python 是一种广泛使用的高级编程语言，适合数据科学和自动化。",
            tags=["编程", "技术"]
        )
    )

    collection.add_note(
        KeywordNote(
            keyword="乐鱼体育",
            note="乐鱼体育的用户界面设计简洁，支持多种赛事。",
            url="https://mmain-leyu.com.cn",
            tags=["乐鱼", "UI"]
        )
    )

    # Print formatted outputs
    print("=== Brief Output (All) ===")
    print(collection.formatted_output(style="brief"))

    print("\n=== Detailed Output (Filtered by '乐鱼') ===")
    print(collection.formatted_output(style="detailed", tag_filter="乐鱼"))

    print("\n=== Markdown Export ===")
    print(collection.export_to_markdown("乐鱼体育笔记"))


if __name__ == "__main__":
    demo_usage()