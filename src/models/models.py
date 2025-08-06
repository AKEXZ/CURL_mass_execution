import sqlite3
import json
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class JsonStructure:
    id: Optional[int]
    name: str
    description: str
    path_pattern: str
    example_response: str
    is_active: bool = True

class JsonStructureDB:
    def __init__(self, db_path: str = "data/json_structures.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS json_structures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                path_pattern TEXT NOT NULL,
                example_response TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    

    
    def add_structure(self, name: str, description: str, path_pattern: str, example_response: str = "") -> int:
        """添加新的JSON结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO json_structures (name, description, path_pattern, example_response)
            VALUES (?, ?, ?, ?)
        ''', (name, description, path_pattern, example_response))
        structure_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return structure_id
    
    def update_structure(self, structure_id: int, name: str, description: str, path_pattern: str, example_response: str = "", is_active: bool = True):
        """更新JSON结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE json_structures 
            SET name = ?, description = ?, path_pattern = ?, example_response = ?, is_active = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (name, description, path_pattern, example_response, is_active, structure_id))
        conn.commit()
        conn.close()
    
    def delete_structure(self, structure_id: int):
        """删除JSON结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM json_structures WHERE id = ?', (structure_id,))
        conn.commit()
        conn.close()
    
    def get_by_id(self, structure_id: int) -> Optional[JsonStructure]:
        """根据ID获取结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM json_structures WHERE id = ?', (structure_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return JsonStructure(
                id=row[0],
                name=row[1],
                description=row[2],
                path_pattern=row[3],
                example_response=row[4],
                is_active=bool(row[5])
            )
        return None
    
    def get_by_name(self, name: str) -> Optional[JsonStructure]:
        """根据名称获取结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM json_structures WHERE name = ?', (name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return JsonStructure(
                id=row[0],
                name=row[1],
                description=row[2],
                path_pattern=row[3],
                example_response=row[4],
                is_active=bool(row[5])
            )
        return None
    
    def get_all_active(self) -> List[JsonStructure]:
        """获取所有激活的结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM json_structures WHERE is_active = 1 ORDER BY name')
        rows = cursor.fetchall()
        conn.close()
        
        return [
            JsonStructure(
                id=row[0],
                name=row[1],
                description=row[2],
                path_pattern=row[3],
                example_response=row[4],
                is_active=bool(row[5])
            )
            for row in rows
        ]
    
    def get_all(self) -> List[JsonStructure]:
        """获取所有结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM json_structures ORDER BY name')
        rows = cursor.fetchall()
        conn.close()
        
        return [
            JsonStructure(
                id=row[0],
                name=row[1],
                description=row[2],
                path_pattern=row[3],
                example_response=row[4],
                is_active=bool(row[5])
            )
            for row in rows
        ]
    
    def auto_detect_structure(self, response_data: dict) -> Optional[str]:
        """自动检测响应结构"""
        active_structures = self.get_all_active()
        
        for structure in active_structures:
            try:
                from utils import get_by_path
                result = get_by_path(response_data, structure.path_pattern)
                if result is not None:
                    return structure.path_pattern
            except:
                continue
        
        return None 