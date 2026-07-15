import json
import os
import uuid
from datetime import datetime

class Character:
    def __init__(self, name="Новый персонаж", id=None, role="Главный герой", age="", gender="", 
                 appearance="", personality="", goal="", backstory="", custom_fields=None, image_path=""):
        self.id = id if id else uuid.uuid4().hex
        self.name = name
        self.role = role
        self.age = age
        self.gender = gender
        self.appearance = appearance
        self.personality = personality
        self.goal = goal
        self.backstory = backstory
        self.custom_fields = custom_fields if custom_fields is not None else {}
        self.image_path = image_path

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "age": self.age,
            "gender": self.gender,
            "appearance": self.appearance,
            "personality": self.personality,
            "goal": self.goal,
            "backstory": self.backstory,
            "custom_fields": self.custom_fields,
            "image_path": self.image_path
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            name=d.get("name", ""),
            id=d.get("id"),
            role=d.get("role", "Главный герой"),
            age=d.get("age", ""),
            gender=d.get("gender", ""),
            appearance=d.get("appearance", ""),
            personality=d.get("personality", ""),
            goal=d.get("goal", ""),
            backstory=d.get("backstory", ""),
            custom_fields=d.get("custom_fields", {}),
            image_path=d.get("image_path", "")
        )


class Location:
    def __init__(self, name="Новая локация", id=None, description="", significance="", climate="", 
                 custom_fields=None, image_path=""):
        self.id = id if id else uuid.uuid4().hex
        self.name = name
        self.description = description
        self.significance = significance
        self.climate = climate
        self.custom_fields = custom_fields if custom_fields is not None else {}
        self.image_path = image_path

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "significance": self.significance,
            "climate": self.climate,
            "custom_fields": self.custom_fields,
            "image_path": self.image_path
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            name=d.get("name", ""),
            id=d.get("id"),
            description=d.get("description", ""),
            significance=d.get("significance", ""),
            climate=d.get("climate", ""),
            custom_fields=d.get("custom_fields", {}),
            image_path=d.get("image_path", "")
        )


class Scene:
    def __init__(self, title="Новая сцена", id=None, summary="", content="", 
                 characters=None, locations=None, status="В плане", word_count=0):
        self.id = id if id else uuid.uuid4().hex
        self.title = title
        self.summary = summary
        self.content = content
        self.characters = characters if characters is not None else []
        self.locations = locations if locations is not None else []
        self.status = status  # "В плане", "В процессе", "Завершено"
        self.word_count = word_count

    def update_word_count(self):
        # Простой подсчет слов для кириллицы/латиницы
        words = self.content.strip().split()
        self.word_count = len([w for w in words if w])
        return self.word_count

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "content": self.content,
            "characters": self.characters,
            "locations": self.locations,
            "status": self.status,
            "word_count": self.word_count
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            title=d.get("title", ""),
            id=d.get("id"),
            summary=d.get("summary", ""),
            content=d.get("content", ""),
            characters=d.get("characters", []),
            locations=d.get("locations", []),
            status=d.get("status", "В плане"),
            word_count=d.get("word_count", 0)
        )


class Chapter:
    def __init__(self, title="Новая глава", id=None, order=0, scenes=None):
        self.id = id if id else uuid.uuid4().hex
        self.title = title
        self.order = order
        self.scenes = [Scene.from_dict(s) for s in scenes] if scenes is not None else []

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "order": self.order,
            "scenes": [s.to_dict() for s in self.scenes]
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            title=d.get("title", ""),
            id=d.get("id"),
            order=d.get("order", 0),
            scenes=d.get("scenes", [])
        )


class Relationship:
    def __init__(self, char_a, char_b, description="Знакомые"):
        self.char_a = char_a
        self.char_b = char_b
        self.description = description

    def to_dict(self):
        return {
            "char_a": self.char_a,
            "char_b": self.char_b,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            char_a=d.get("char_a"),
            char_b=d.get("char_b"),
            description=d.get("description", "Знакомые")
        )


class WorldNote:
    def __init__(self, title="Новая запись", id=None, category="Магия / Технологии", content=""):
        self.id = id if id else uuid.uuid4().hex
        self.title = title
        self.category = category
        self.content = content

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "content": self.content
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            title=d.get("title", "Новая запись"),
            id=d.get("id"),
            category=d.get("category", "Магия / Технологии"),
            content=d.get("content", "")
        )


class Project:
    def __init__(self, title="Мой роман", file_path=None):
        self.id = uuid.uuid4().hex
        self.title = title
        self.file_path = file_path
        self.author = ""
        self.genre = ""
        self.synopsis = ""
        self.logline = ""
        self.themes = ""
        self.cover_image = ""
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.characters = []
        self.locations = []
        self.chapters = []
        self.relationships = []
        self.world_notes = []

    def get_character_by_id(self, char_id):
        for char in self.characters:
            if char.id == char_id:
                return char
        return None

    def get_location_by_id(self, loc_id):
        for loc in self.locations:
            if loc.id == loc_id:
                return loc
        return None

    def get_total_words(self):
        total = 0
        for ch in self.chapters:
            for sc in ch.scenes:
                total += sc.word_count
        return total

    def save(self):
        if not self.file_path:
            raise ValueError("Путь к файлу не установлен.")
        
        self.last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "synopsis": self.synopsis,
            "logline": self.logline,
            "themes": self.themes,
            "cover_image": self.cover_image,
            "created_at": self.created_at,
            "last_modified": self.last_modified,
            "characters": [c.to_dict() for c in self.characters],
            "locations": [l.to_dict() for l in self.locations],
            "chapters": [ch.to_dict() for ch in self.chapters],
            "relationships": [r.to_dict() for r in self.relationships],
            "world_notes": [n.to_dict() for n in self.world_notes]
        }
        
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @classmethod
    def load(cls, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден.")
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        project = cls(title=data.get("title", "Без названия"), file_path=file_path)
        project.id = data.get("id", uuid.uuid4().hex)
        project.author = data.get("author", "")
        project.genre = data.get("genre", "")
        project.synopsis = data.get("synopsis", "")
        project.logline = data.get("logline", "")
        project.themes = data.get("themes", "")
        project.cover_image = data.get("cover_image", "")
        project.created_at = data.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        project.last_modified = data.get("last_modified", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        project.characters = [Character.from_dict(c) for c in data.get("characters", [])]
        project.locations = [Location.from_dict(l) for l in data.get("locations", [])]
        project.chapters = [Chapter.from_dict(ch) for ch in data.get("chapters", [])]
        project.relationships = [Relationship.from_dict(r) for r in data.get("relationships", [])]
        project.world_notes = [WorldNote.from_dict(n) for n in data.get("world_notes", [])]
        
        # Сортируем главы по порядку
        project.chapters.sort(key=lambda x: x.order)
        return project
