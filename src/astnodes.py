from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

@dataclass
class ASTNode:
    kind: str
    value: Optional[str] = None
    children: List["ASTNode"] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "value": self.value,
            "children": [c.to_dict() for c in self.children],
        }