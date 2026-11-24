from dataclasses import dataclass
from datetime import datetime

@dataclass
class Session:
    app_name: str
    started_at: datetime
    process_name: str | None = None
    ended_at: datetime | None = None

    @property
    def duration(self) -> int:
        if self.ended_at == None:
            return 0

        return int((self.ended_at - self.started_at).total_seconds())