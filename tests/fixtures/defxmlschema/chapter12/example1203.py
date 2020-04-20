from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Product:
    """
    :ivar number:
    :ivar name:
    :ivar size:
    """
    class Meta:
        name = "product"

    number: Optional[int] = field(
        default=None,
        metadata=dict(
            type="Element",
            namespace="",
            required=True
        )
    )
    name: Optional[str] = field(
        default=None,
        metadata=dict(
            type="Element",
            namespace="",
            required=True
        )
    )
    size: Optional[int] = field(
        default=None,
        metadata=dict(
            type="Element",
            namespace="",
            required=True
        )
    )
